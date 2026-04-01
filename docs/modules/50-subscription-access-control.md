# Module 50 — Subscription & Access Control

## 1. Purpose & Scope

Subscription & Access Control is the commercial and entitlement layer of EduForge. Every feature unlock, usage limit, trial expiry, dunning retry, and plan upgrade flows through this module. It is deliberately separated from billing (Module 56) and payment processing (Module 57) — this module manages *what* is accessible; the other modules manage *how money flows*.

**Three dimensions of access:**

| Dimension | Where enforced | Mechanism |
|-----------|---------------|-----------|
| **Feature gate** | API middleware + Flutter route guard | `feature_gates` table → DynamoDB cache → 402 if locked |
| **Usage limit** | API middleware + background counter | DynamoDB atomic counter per student per day |
| **Subscription status** | API middleware | `tenant_subscriptions.status` check in cache |

**Guiding principles:**
- Never block student access to already-viewed content (exam results, certificates) due to subscription lapse
- Downgrade to Free — never delete data — on expiry or payment failure
- 7-day refund, no-dark-patterns cancellation (Consumer Protection Act 2019 compliance)
- Additive entitlements: student's individual plan supplements (never reduces) the institution plan

---

## 2. Plan Catalog

### Institution Plans (B2B)

| Plan | Max Students | Storage | AI Doubts/Student/Day | Price |
|------|-------------|---------|----------------------|-------|
| **Free** | 50 | 10 GB | 0 | Rs. 0 |
| **Standard** | 500 | 100 GB | 10 | Rs. 15/student/month |
| **Professional** | Unlimited | 1 TB | 50 | Rs. 50/student/month |
| **Enterprise** | Unlimited | Custom | Unlimited | Custom contract |

### Individual Plans (B2C)

| Plan | AI Doubts/Day | Mock Tests/Month | PYQ Access | Video Downloads | Price |
|------|--------------|-----------------|------------|-----------------|-------|
| **Free** | 10 | 5 | None | 0 | Rs. 0 |
| **Standard** | 50 | Unlimited | 1 exam | 5/month | Rs. 99/month |
| **Premium** | Unlimited | Unlimited | All exams | 30/month | Rs. 299/month |
| **Competitive Bundle** | Unlimited | Unlimited | All exams | 30/month | Rs. 499/month |

Annual billing: 20% discount vs monthly.

### Feature Gate Matrix

| Feature Key | Free | Standard | Professional / Premium |
|-------------|------|----------|----------------------|
| `core_modules` (attendance, timetable, homework) | ✓ | ✓ | ✓ |
| `ai_doubt_solver` | Limited (10/day) | Limited (50/day) | Unlimited |
| `ai_performance_analytics` | ✗ | ✗ | ✓ |
| `ai_content_generation` | ✗ | ✗ | ✓ |
| `video_downloads` | ✗ | ✗ | ✓ |
| `live_classes` (host) | ✗ | ✓ | ✓ |
| `pyq_access` | ✗ | Partial (1 exam) | All exams |
| `leaderboard_public` | ✗ | ✓ | ✓ |
| `certificate_generation` | ✗ | ✓ | ✓ |
| `api_access` | ✗ | ✗ | ✓ |
| `white_label` | ✗ | ✗ | Enterprise only |
| `advanced_reports` | ✗ | ✗ | ✓ |

---

## 3. Access Control Middleware

### FastAPI Middleware

```python
# middleware/subscription.py

from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

class SubscriptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Skip for public routes
        if is_public_route(request.url.path):
            return await call_next(request)

        user      = request.state.user
        feature   = get_required_feature(request.url.path, request.method)

        if feature:
            entitlement = await get_entitlement(user.tenant_id, user.student_id)

            if feature not in entitlement.features:
                raise HTTPException(
                    status_code = 402,
                    detail = {
                        "error":       "feature_not_in_plan",
                        "feature":     feature,
                        "current_plan": entitlement.plan_name,
                        "upsell_url":  "/plans/",
                        "message":     f"'{feature}' requires {FEATURE_PLANS[feature]} plan or higher."
                    }
                )

            # Check usage limit (hard-gated features only)
            gate = get_feature_gate(feature)
            if gate.has_daily_limit:
                limit   = entitlement.limits.get(feature, 0)
                current = await get_usage_count(user.student_id, feature)
                if current >= limit:
                    raise HTTPException(
                        status_code = 429,
                        detail = {
                            "error":      "usage_limit_reached",
                            "feature":    feature,
                            "used":       current,
                            "limit":      limit,
                            "resets_at":  tomorrow_midnight_iso(),
                            "upsell_url": "/plans/",
                        }
                    )
                # Increment usage counter (atomic)
                await increment_usage(user.student_id, feature)

        return await call_next(request)
```

### Entitlement Resolution

```python
# Additive: student's individual plan supplements institution plan

async def get_entitlement(tenant_id: str, student_id: str) -> Entitlement:
    # 1. Try DynamoDB cache (TTL 300 seconds)
    cache_key  = f"{tenant_id}#{student_id}"
    cached     = await dynamodb.get_item(TableName="subscription-cache", Key={"pk": cache_key})
    if cached.get("Item"):
        return Entitlement.from_dynamo(cached["Item"])

    # 2. Cache miss → build from PostgreSQL
    tenant_plan  = await get_tenant_plan(tenant_id)
    student_plan = await get_student_plan(student_id)   # may be None

    # Merge: union of features, max of limits
    features = set(tenant_plan.features)
    limits   = dict(tenant_plan.limits)
    if student_plan:
        features |= set(student_plan.features)
        for k, v in student_plan.limits.items():
            limits[k] = max(limits.get(k, 0), v)

    entitlement = Entitlement(
        features   = list(features),
        limits     = limits,
        plan_name  = higher_plan(tenant_plan.name, student_plan.name if student_plan else "free"),
        valid_until = min_date(tenant_plan.period_end, student_plan.period_end if student_plan else FAR_FUTURE),
    )

    # 3. Write to DynamoDB with TTL
    await dynamodb.put_item(
        TableName = "subscription-cache",
        Item      = {
            "pk":          cache_key,
            "features":    list(features),
            "limits":      limits,
            "plan_name":   entitlement.plan_name,
            "valid_until": entitlement.valid_until.isoformat(),
            "ttl":         int(time.time()) + 300
        }
    )
    return entitlement
```

### Usage Counter (Atomic DynamoDB)

```python
async def get_usage_count(student_id: str, feature: str) -> int:
    today = date.today().isoformat()
    resp  = await dynamodb.get_item(
        TableName = "usage-counters",
        Key       = {"pk": f"{student_id}#{feature}#{today}"}
    )
    return int(resp.get("Item", {}).get("count", 0))

async def increment_usage(student_id: str, feature: str):
    today = date.today().isoformat()
    await dynamodb.update_item(
        TableName = "usage-counters",
        Key       = {"pk": f"{student_id}#{feature}#{today}"},
        UpdateExpression = "ADD #c :one",
        ExpressionAttributeNames  = {"#c": "count"},
        ExpressionAttributeValues = {":one": 1},
    )
    # TTL: expire at midnight tomorrow + 1 day (for analytics read window)
    await dynamodb.update_item(
        TableName = "usage-counters",
        Key       = {"pk": f"{student_id}#{feature}#{today}"},
        UpdateExpression = "SET #t = :ttl",
        ExpressionAttributeNames  = {"#t": "ttl"},
        ExpressionAttributeValues = {":ttl": int(next_midnight_ts()) + 86400},
    )
```

---

## 4. Trial Management

### Trial State Machine

```
NEW SIGNUP
    └─ status = 'trial', trial_end = NOW() + 30d (institution) / 7d (individual)

T-7 days → reminder_email_1 + push notification
T-3 days → reminder_email_2 + WhatsApp + in-app banner
T-1 day  → reminder_email_3 + urgent in-app banner

Trial end (no payment)
    └─ +3 day grace → status stays 'trial' (procrastinator buffer)
    └─ Grace end → status = 'active' on Free plan
    └─ Win-back email: "You missed out — 30% off first year if you upgrade in 7 days"

Trial end (payment received before expiry)
    └─ status = 'active', current_period_start = payment_date
    └─ Welcome + receipt email
    └─ Invalidate DynamoDB cache → rebuild with paid plan features
```

### Trial Conversion Lambda

```python
# EventBridge cron: daily 8 AM
def process_trial_reminders():
    for days_out in [7, 3, 1]:
        target_date = date.today() + timedelta(days=days_out)
        expiring = db.execute("""
            SELECT ts.sub_id, ts.tenant_id, t.primary_contact_email,
                   ts.trial_end, sp.plan_name
            FROM   tenant_subscriptions ts
            JOIN   tenants t ON t.tenant_id = ts.tenant_id
            JOIN   subscription_plans sp ON sp.plan_id = ts.plan_id
            WHERE  ts.status = 'trial'
              AND  ts.trial_end = $1
        """, target_date).fetchall()

        for sub in expiring:
            send_trial_reminder_email(sub, days_remaining=days_out)
            send_fcm_push(sub.tenant_id, f"Your trial ends in {days_out} day(s). Upgrade to keep all features.")
```

---

## 5. Dunning Management

### Dunning State Machine

```
PAYMENT FAILED (Razorpay webhook: subscription.charged.failed)
    │
    D+0: Retry immediately (same payment method)
    D+1: Try alternate saved payment method
    D+3: Email + SMS + WhatsApp: "Action required — update payment method"
    D+7: Sub status → 'grace' — suspend AI doubts, new video access
         In-app banner: "Service suspended — update payment to restore"
    D+14: Sub status → 'suspended' — only profile + certificates accessible
    D+30: Sub status → 'cancelled' — data in retention (preserved 90 days)
```

### Dunning Lambda

```python
# EventBridge daily 7 AM
def process_dunning():
    failed_subs = db.execute("""
        SELECT sub_id, tenant_id, last_payment_at, status,
               DATE_PART('day', NOW() - last_payment_at) AS days_overdue
        FROM   tenant_subscriptions
        WHERE  status IN ('active','grace','suspended')
          AND  last_payment_at < NOW() - INTERVAL '1 day'
          AND  auto_renew = true
    """).fetchall()

    for sub in failed_subs:
        days = sub.days_overdue
        if days >= 30 and sub.status != 'cancelled':
            update_status(sub.sub_id, 'cancelled')
            schedule_data_retention(sub.tenant_id, delete_after=90)
        elif days >= 14 and sub.status not in ('suspended','cancelled'):
            update_status(sub.sub_id, 'suspended')
            send_suspension_notice(sub.tenant_id)
            invalidate_cache(sub.tenant_id)
        elif days >= 7 and sub.status == 'active':
            update_status(sub.sub_id, 'grace')
            reduce_features_to_grace_set(sub.tenant_id)
            invalidate_cache(sub.tenant_id)
        elif days in (3, 1):
            send_payment_reminder(sub.tenant_id, days_overdue=days)
```

---

## 6. Proration & Billing Logic

### Upgrade Proration

```python
def compute_upgrade_proration(current_plan_price: float,
                               new_plan_price: float,
                               days_remaining: int,
                               billing_period_days: int) -> float:
    unused_credit  = current_plan_price * (days_remaining / billing_period_days)
    new_plan_cost  = new_plan_price * (days_remaining / billing_period_days)
    charge_now     = max(0, new_plan_cost - unused_credit)
    return round(charge_now, 2)

# Example: upgrading from Standard (Rs. 7,500/month) to Professional (Rs. 50,000/month)
# with 15 days remaining in billing period
# unused_credit = 7500 × (15/30) = 3,750
# new_plan_cost = 50000 × (15/30) = 25,000
# charge_now    = 25,000 - 3,750 = Rs. 21,250
```

### Annual Discount

```python
def annual_price(monthly_price: float, discount_pct: float = 20) -> float:
    return round(monthly_price * 12 * (1 - discount_pct / 100), 2)

# Standard: Rs. 99 × 12 × 0.80 = Rs. 950.40/year
# Premium:  Rs. 299 × 12 × 0.80 = Rs. 2,870.40/year
```

---

## 7. Feature Flag System

```sql
-- feature_flags: separate from subscription gates — for rollout/kill switches
CREATE TABLE platform.feature_flags (
    flag_key            VARCHAR(100) PRIMARY KEY,
    description         TEXT,
    is_globally_enabled BOOLEAN DEFAULT TRUE,
    enabled_for_tenants UUID[] DEFAULT '{}',
    rollout_pct         SMALLINT DEFAULT 100
                        CHECK (rollout_pct BETWEEN 0 AND 100),
    ab_test_variants    JSONB,           -- {"control": 50, "variant_a": 50}
    created_at          TIMESTAMPTZ DEFAULT NOW(),
    updated_at          TIMESTAMPTZ DEFAULT NOW()
);

-- Sample flags
INSERT INTO platform.feature_flags VALUES
    ('ai_doubt_solver_v2',      'Streaming SSE answer (v2)',     true,  '{}', 100, null),
    ('ai_content_generation',   'AI content generation feature', false, '{}', 0,   null),
    ('dark_mode',               'Dark mode UI',                  true,  '{}', 100, null),
    ('maintenance_mode',        'Global maintenance kill switch',false, '{}', 100, null);
```

### Flag Check in FastAPI

```python
async def is_feature_enabled(flag_key: str, tenant_id: str) -> bool:
    flag = await get_flag_from_cache(flag_key)  # Redis-free: DynamoDB cache
    if not flag.is_globally_enabled:
        return False
    if tenant_id in flag.enabled_for_tenants:
        return True
    if flag.rollout_pct == 100:
        return True
    if flag.rollout_pct == 0:
        return False
    # Deterministic rollout: hash(tenant_id + flag_key) mod 100 < rollout_pct
    hash_val = int(hashlib.md5(f"{tenant_id}{flag_key}".encode()).hexdigest(), 16) % 100
    return hash_val < flag.rollout_pct
```

---

## 8. Subscription Lifecycle — End-to-End

### Razorpay Subscription (B2C)

```python
# POST /api/v1/me/subscription/upgrade/
# Creates Razorpay subscription, returns checkout URL

def initiate_subscription_upgrade(student_id: str, plan_id: str) -> dict:
    plan = get_plan(plan_id)

    razorpay_sub = razorpay_client.subscription.create({
        "plan_id":        plan.razorpay_plan_id,
        "total_count":    120,            # 10 years max
        "quantity":       1,
        "customer_notify": 1,
        "notify_info": {
            "notify_phone": student.phone,
            "notify_email": student.email,
        },
        "notes": {
            "eduforge_student_id": student_id,
            "eduforge_plan_id":    plan_id,
        }
    })

    # Store pending subscription
    db.execute("""
        INSERT INTO student_subscriptions
            (student_id, plan_id, status, razorpay_sub_id)
        VALUES ($1, $2, 'pending', $3)
    """, student_id, plan_id, razorpay_sub["id"])

    return {
        "subscription_id":  razorpay_sub["id"],
        "short_url":        razorpay_sub["short_url"],
        "payment_link":     razorpay_sub["short_url"],
    }
```

### Razorpay Webhook Handler

```python
# POST /webhooks/razorpay/ (unauthenticated, HMAC-verified)

def handle_razorpay_webhook(event: dict, signature: str, body: bytes):
    # Verify HMAC-SHA256
    expected = hmac.new(settings.RAZORPAY_WEBHOOK_SECRET.encode(),
                        body, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, signature):
        raise HTTPException(400, "Invalid signature")

    event_type = event["event"]

    if event_type == "subscription.charged":
        handle_subscription_charged(event["payload"]["subscription"]["entity"])
    elif event_type == "subscription.charge_failed":
        handle_charge_failed(event["payload"]["subscription"]["entity"])
    elif event_type == "subscription.cancelled":
        handle_subscription_cancelled(event["payload"]["subscription"]["entity"])
    elif event_type == "subscription.completed":
        handle_subscription_expired(event["payload"]["subscription"]["entity"])

def handle_subscription_charged(sub: dict):
    razorpay_sub_id = sub["id"]
    db.execute("""
        UPDATE student_subscriptions
        SET    status = 'active',
               current_period_start = NOW(),
               current_period_end   = NOW() + INTERVAL '1 month',
               last_payment_at      = NOW()
        WHERE  razorpay_sub_id = $1
    """, razorpay_sub_id)

    # Invalidate DynamoDB cache + emit event
    invalidate_cache_for_sub(razorpay_sub_id)
    emit_event("subscription.renewed", {"razorpay_sub_id": razorpay_sub_id})
    send_receipt_email(razorpay_sub_id)
```

---

## 9. Data Model

```sql
-- subscription_plans
CREATE TABLE subscriptions.subscription_plans (
    plan_id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    plan_name        VARCHAR(50) NOT NULL,
    plan_type        VARCHAR(20) NOT NULL
                     CHECK (plan_type IN ('institution','individual','addon')),
    billing_cycle    VARCHAR(20) NOT NULL
                     CHECK (billing_cycle IN ('monthly','annual','one_time')),
    price_inr        NUMERIC(10,2) NOT NULL,
    price_inr_annual NUMERIC(10,2),
    max_students     INT,                      -- NULL = unlimited
    max_storage_gb   INT,
    features         JSONB NOT NULL,           -- ["ai_doubt_solver", "live_classes", ...]
    limits           JSONB NOT NULL,           -- {"ai_doubt_solver": 50, "video_downloads": 30}
    razorpay_plan_id VARCHAR(50),
    is_active        BOOLEAN DEFAULT TRUE,
    version          SMALLINT DEFAULT 1,       -- plan versioning for grandfathering
    created_at       TIMESTAMPTZ DEFAULT NOW()
);

-- feature_gates
CREATE TABLE subscriptions.feature_gates (
    feature_key                 VARCHAR(100) PRIMARY KEY,
    description                 TEXT,
    minimum_plan_institution    VARCHAR(50),   -- 'free', 'standard', 'professional', 'enterprise'
    minimum_plan_individual     VARCHAR(50),
    has_daily_limit             BOOLEAN DEFAULT FALSE,
    is_hard_gated               BOOLEAN DEFAULT TRUE,   -- false = JWT plan OK; true = always DynamoDB
    created_at                  TIMESTAMPTZ DEFAULT NOW()
);

-- tenant_subscriptions
CREATE TABLE subscriptions.tenant_subscriptions (
    sub_id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id               UUID NOT NULL REFERENCES tenants(tenant_id) UNIQUE,
    plan_id                 UUID NOT NULL REFERENCES subscriptions.subscription_plans(plan_id),
    status                  VARCHAR(20) DEFAULT 'trial'
                            CHECK (status IN ('trial','pending','active','grace',
                                              'suspended','cancelled')),
    trial_end               DATE,
    current_period_start    DATE,
    current_period_end      DATE,
    razorpay_subscription_id VARCHAR(50),
    payment_method          VARCHAR(30),      -- 'upi_autopay', 'card', 'neft', 'po'
    auto_renew              BOOLEAN DEFAULT TRUE,
    gstin                   VARCHAR(15),
    last_payment_at         TIMESTAMPTZ,
    dunning_level           SMALLINT DEFAULT 0,    -- 0=ok, 1=D+3, 2=D+7, 3=D+14
    created_at              TIMESTAMPTZ DEFAULT NOW(),
    updated_at              TIMESTAMPTZ DEFAULT NOW()
);

-- student_subscriptions (B2C)
CREATE TABLE subscriptions.student_subscriptions (
    sub_id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id              UUID NOT NULL REFERENCES students(student_id),
    tenant_id               UUID REFERENCES tenants(tenant_id),
    plan_id                 UUID NOT NULL REFERENCES subscriptions.subscription_plans(plan_id),
    status                  VARCHAR(20) DEFAULT 'trial',
    trial_end               DATE,
    current_period_start    DATE,
    current_period_end      DATE,
    razorpay_sub_id         VARCHAR(50),
    auto_renew              BOOLEAN DEFAULT TRUE,
    last_payment_at         TIMESTAMPTZ,
    created_at              TIMESTAMPTZ DEFAULT NOW()
);

-- addon_purchases
CREATE TABLE subscriptions.addon_purchases (
    purchase_id       UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entity_type       VARCHAR(10) NOT NULL CHECK (entity_type IN ('tenant','student')),
    entity_id         UUID NOT NULL,
    addon_type        VARCHAR(30) NOT NULL,    -- 'pyq_pack', 'doubt_credits', 'recording_archive'
    addon_key         VARCHAR(100),            -- e.g., exam_id for pyq_pack
    quantity          INT DEFAULT 1,
    amount_inr        NUMERIC(10,2),
    valid_from        DATE NOT NULL,
    valid_until       DATE,
    razorpay_payment_id VARCHAR(50),
    created_at        TIMESTAMPTZ DEFAULT NOW()
);

-- usage_tracking
CREATE TABLE subscriptions.usage_tracking (
    entity_type   VARCHAR(10) NOT NULL,
    entity_id     UUID NOT NULL,
    feature_key   VARCHAR(100) NOT NULL,
    period_date   DATE NOT NULL,
    usage_count   INT DEFAULT 0,
    limit_count   INT,
    PRIMARY KEY   (entity_type, entity_id, feature_key, period_date)
);

-- subscription_events
CREATE TABLE subscriptions.subscription_events (
    event_id    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sub_id      UUID,    -- FK tenant or student subscription
    sub_type    VARCHAR(10),
    event_type  VARCHAR(50) NOT NULL,
    metadata    JSONB,
    created_at  TIMESTAMPTZ DEFAULT NOW()
);
```

---

## 10. API Reference

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| `GET` | `/api/v1/plans/` | Public | All plans + feature matrix |
| `GET` | `/api/v1/me/subscription/` | Student | Current plan, status, expiry, usage |
| `POST` | `/api/v1/me/subscription/upgrade/` | Student | Initiate upgrade → Razorpay checkout |
| `POST` | `/api/v1/me/subscription/cancel/` | Student | Cancel with 7-day data preservation |
| `GET` | `/api/v1/me/subscription/usage/` | Student | Per-feature usage this period |
| `GET` | `/api/v1/me/subscription/invoices/` | Student | Past invoices (PDF links) |
| `POST` | `/api/v1/me/subscription/restore/` | Student | Resume after cancellation (within 90 days) |
| `GET` | `/api/v1/admin/subscription/` | Admin | Institution subscription dashboard |
| `POST` | `/api/v1/admin/subscription/upgrade/` | Admin | Institution plan upgrade |
| `GET` | `/api/v1/admin/subscription/utilisation/` | Admin | Seat + feature + storage utilisation |
| `POST` | `/api/v1/admin/subscription/grant-override/` | Admin | Emergency feature grant (audit-logged) |
| `POST` | `/webhooks/razorpay/` | Internal (HMAC) | Razorpay subscription + payment webhooks |
| `GET` | `/api/v1/platform/plans/` | Platform Admin | All plans management |
| `GET` | `/api/v1/platform/feature-flags/` | Platform Admin | Feature flag list |
| `PATCH` | `/api/v1/platform/feature-flags/{key}` | Platform Admin | Toggle flag / rollout % |
| `GET` | `/api/v1/platform/revenue/mrr/` | Platform Admin | MRR/ARR by plan tier |

---

## 11. Flutter App

### Subscription Status Card

```dart
// On profile screen
SubscriptionCard(
  planName:    subscription.planName,
  expiryDate:  subscription.currentPeriodEnd,
  status:      subscription.status,
  usageItems: [
    UsageItem(
      label: 'AI Doubts Today',
      used:  subscription.usageToday['ai_doubt_solver'],
      limit: subscription.limits['ai_doubt_solver'],
    ),
    UsageItem(
      label: 'Video Downloads',
      used:  subscription.usageThisMonth['video_downloads'],
      limit: subscription.limits['video_downloads'],
    ),
  ],
)
```

### Feature Locked Gate

```dart
// Wraps any feature widget — shows upgrade prompt if not entitled
class FeatureGate extends StatelessWidget {
  final String featureKey;
  final Widget child;
  final Widget? lockedPlaceholder;

  @override
  Widget build(BuildContext context) {
    final entitled = context.watch<SubscriptionProvider>()
        .isFeatureEntitled(featureKey);

    if (entitled) return child;

    return lockedPlaceholder ?? FeatureLockedCard(
      featureKey: featureKey,
      onUpgrade: () => context.push('/plans/'),
    );
  }
}
```

### Plan Comparison Screen

```dart
// Three-column plan comparison table
PlansComparisonScreen(
  plans: plans,
  currentPlan: subscription.planName,
  onSelect: (planId) async {
    final result = await SubscriptionApi.initiateUpgrade(planId);
    // Open Razorpay checkout
    await RazorpayCheckout.open(result.paymentLink);
  },
)
```

---

## 12. Web Interface (HTMX)

### Institution Subscription Page

```html
<!-- Subscription management for institution admin -->
<div class="subscription-card">
  <div class="plan-badge">{{ subscription.plan_name | title }}</div>
  <p>Renews: {{ subscription.current_period_end | date:"d M Y" }}</p>

  <!-- Seat utilisation gauge -->
  <div class="usage-gauge">
    <div class="label">Students: {{ active_students }} / {{ plan.max_students or "Unlimited" }}</div>
    <progress value="{{ active_students }}" max="{{ plan.max_students or active_students }}"></progress>
  </div>

  <!-- Upgrade button -->
  {% if can_upgrade %}
  <button hx-get="/admin/subscription/upgrade-modal/"
          hx-target="#modal-container"
          class="btn btn-primary">
    Upgrade Plan
  </button>
  {% endif %}
</div>

<!-- Utilisation dashboard (HTMX lazy load) -->
<div hx-get="/admin/subscription/utilisation/"
     hx-trigger="load"
     hx-swap="innerHTML"
     id="utilisation-charts">
  Loading…
</div>
```

---

## 13. Background Jobs

| Job | Trigger | Function |
|-----|---------|----------|
| `trial_reminders` | EventBridge daily 8 AM | Send T-7/3/1 reminders for expiring trials |
| `dunning_manager` | EventBridge daily 7 AM | Advance dunning state; suspend/cancel overdue |
| `subscription_renewer` | Razorpay webhook `subscription.charged` | Update period dates; refresh DynamoDB cache |
| `usage_daily_sync` | EventBridge midnight | Sync DynamoDB usage counters → PostgreSQL |
| `cache_warmer` | EventBridge 6:30 AM | Pre-warm DynamoDB cache for all active tenants |
| `storage_monitor` | EventBridge daily | Compute R2 storage per tenant; alert at 90% |
| `win_back_campaign` | EventBridge D+7 after trial_expired | Send 30% discount offer to non-converted trials |
| `data_retention_cleanup` | EventBridge monthly | Delete cancelled-for-90-days tenant data |

---

## 14. Consumer Protection & DPDPA

| Obligation | Implementation |
|------------|---------------|
| **7-day refund** | `POST /api/v1/me/subscription/refund/` — no-questions refund within 7 days of purchase. Razorpay refund initiated instantly. |
| **Easy cancellation** | Single-tap cancel in Flutter app; max 3 confirmation steps; no support ticket required. |
| **Auto-renewal disclosure** | Shown prominently at signup: "Your plan auto-renews on [date] for Rs. [amount]. Cancel any time." |
| **Price transparency** | Full feature matrix shown before payment — no hidden charges at checkout. |
| **Data preservation** | Cancelled subscription: data preserved 90 days. Student can restore within 90 days with no data loss. |
| **Right to portability** | `GET /api/v1/me/data-export/` — ZIP of all student data (notes, results, certificates, doubts). Available during and after active subscription. |
| **No dark patterns** | Cancellation UI as prominent as subscribe UI. No forced upsell on cancellation flow. |
| **GST compliance** | B2C: GST invoice via Module 56; B2B: buyer GSTIN on invoice. |
| **Subscription data retention** | Billing records (invoices, payment IDs) retained 7 years per GST audit requirement. |
| **DPDPA audit** | All subscription status changes + feature overrides logged to Module 42 `audit.events`. |
