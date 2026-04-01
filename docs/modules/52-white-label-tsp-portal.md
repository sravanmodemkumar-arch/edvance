# Module 52 — White-label TSP Portal

## 1. Purpose & Scope

A Technology Service Provider (TSP) is a company that re-brands EduForge and sells it to educational institutions under their own name. EduForge operates as the invisible infrastructure; the TSP's brand, domain, and support presence are what institutions and students see.

This module provides:
- **Brand configuration**: custom domain, logo, colors, email sender, AI persona name
- **Tenant portfolio management**: provision, monitor, suspend, and support institutions
- **On-behalf support access**: time-limited, read-only, fully audited
- **Wholesale billing**: EduForge invoices TSP once per month for total active students
- **White-label Flutter app pipeline**: custom-branded Android/iOS app per TSP

**TSP types served:**
| Type | Example | Scale |
|------|---------|-------|
| EdTech product company | SaaS startup bundling EduForge | 10–500 institutions |
| IT consulting firm | System integrator for school ERP | 5–50 institutions |
| State government partner | State-level EdTech deployment | 1,000–10,000 institutions |
| Coaching chain owner | Multi-branch coaching under one brand | 5–200 branches |
| NGO education program | Non-profit running 100 rural schools | 50–500 schools |

**Scope boundaries:**
- Module 51 (B2B API) provides the underlying TSP API endpoints (`is_tsp=true` keys)
- Module 50 (Subscription) manages TSP wholesale plan entitlements
- Module 56 (Platform Billing) generates and delivers wholesale invoices to TSP
- TSP never has access to student personal data — only institution-level metadata

---

## 2. White-label Architecture

### Domain & TLS

```
TSP configures domain: app.academiaplus.com
    │
    ├─ EduForge calls Cloudflare API:
    │     POST /zones/{zone_id}/custom_hostnames
    │     {hostname: "app.academiaplus.com", ssl: {method: "http"}}
    │
    ├─ TSP adds DNS CNAME: app.academiaplus.com → eduforge.in
    │
    ├─ Cloudflare provisions Let's Encrypt cert for app.academiaplus.com
    │   (auto-renews; EduForge monitors expiry)
    │
    └─ Incoming request to app.academiaplus.com:
         Cloudflare → injects X-TSP-Brand: brand_uuid header
         EduForge Django middleware reads brand_id → loads brand config from DynamoDB (1h TTL)
         → renders page with TSP brand assets
```

### Brand CSS Injection

```python
# middleware/brand.py

class BrandMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        brand_id = request.META.get("HTTP_X_TSP_BRAND")
        if brand_id:
            brand    = get_brand_config_cached(brand_id)   # DynamoDB cache
            request.brand = brand
        else:
            request.brand = DEFAULT_EDUFORGE_BRAND         # EduForge default

        response = self.get_response(request)
        return response

# In base template:
# <link rel="stylesheet" href="/static/brand/{{ request.brand.brand_id }}.css">
# <link rel="icon" href="{{ request.brand.favicon_url }}">
# <title>{{ request.brand.app_name }}</title>
```

### Dynamic Brand CSS (per request)

```css
/* Generated at brand creation and cached in R2 */
/* /static/brand/{brand_id}.css */

:root {
  --primary-color: #1A73E8;
  --secondary-color: #34A853;
  --accent-color: #FBBC04;
  --sidebar-bg: #1A1A2E;
  --logo-url: url('https://cdn.eduforge.in/brands/{brand_id}/logo.svg');
}

.brand-logo { content: var(--logo-url); }
.btn-primary { background-color: var(--primary-color); }
.sidebar    { background-color: var(--sidebar-bg); }
```

### Email Branding

```python
# Email template context for branded emails
def get_brand_email_context(brand: BrandProfile) -> dict:
    return {
        "brand_name":     brand.brand_name,
        "app_name":       brand.app_name,
        "logo_url":       f"https://cdn.eduforge.in/brands/{brand.brand_id}/logo.png",
        "footer_text":    brand.custom_footer_html or f"© {year} {brand.brand_name}. All rights reserved.",
        "support_email":  brand.email_sender_address,
        "primary_color":  brand.primary_color,
    }

# SES sender configuration
def get_ses_sender(brand: BrandProfile) -> str:
    if brand.ses_domain_verified and brand.email_sender_address:
        return f'"{brand.email_sender_name}" <{brand.email_sender_address}>'
    return '"EduForge" <noreply@eduforge.in>'   # fallback
```

---

## 3. Tenant Portfolio Management

### TSP Portal Dashboard

```python
# views.py
class TSPDashboardView(TSPLoginRequired, ListView):
    template_name = "tsp/dashboard.html"

    def get_context_data(self):
        tsp_id = self.request.tsp.tsp_id
        return {
            "stats": db.execute("""
                SELECT
                    COUNT(*)                                           AS total_institutions,
                    COUNT(*) FILTER (WHERE tt.billing_status='active') AS active_count,
                    COUNT(*) FILTER (WHERE tt.billing_status='trial')  AS trial_count,
                    SUM((SELECT COUNT(*) FROM students s
                         WHERE s.tenant_id = tt.tenant_id
                           AND s.status = 'active'))                   AS total_students,
                    COUNT(*) FILTER (
                        WHERE NOT EXISTS (
                            SELECT 1 FROM user_sessions us
                            WHERE us.tenant_id = tt.tenant_id
                              AND us.created_at >= NOW() - INTERVAL '30 days'
                        ))                                             AS churn_risk_count
                FROM tsp_tenants tt WHERE tt.tsp_id = $1
            """, tsp_id).fetchone(),
            "institutions": get_tsp_institution_list(tsp_id),
        }
```

### Provisioning New Institution

```python
# POST /api/v1/tsp/tenants/
# Executed via TSP API key (is_tsp=true)

def provision_institution(tsp_id: str, req: ProvisionRequest) -> dict:
    tsp = get_tsp(tsp_id)

    # Create tenant record
    tenant = Tenant(
        institution_name = req.institution_name,
        institution_type = req.institution_type,
        state_code       = req.state_code,
        subdomain        = slugify(req.institution_name) + "-" + random_suffix(4),
        primary_domain   = f"{slugify(req.institution_name)}.{tsp.brand.primary_domain}",
        plan_id          = req.plan_id,
        status           = "trial",
    )
    db.add(tenant)

    # Create default admin user
    admin_password = generate_secure_password()
    admin = User(
        tenant_id  = tenant.tenant_id,
        email      = req.admin_email,
        role       = "institution_admin",
        password   = hash_password(admin_password),
        must_reset_password = True,
    )
    db.add(admin)

    # Create tsp_tenants bridge record
    bridge = TspTenant(
        tsp_id           = tsp_id,
        tenant_id        = tenant.tenant_id,
        brand_profile_id = req.brand_profile_id or tsp.default_brand_profile_id,
        billing_status   = "trial",
        onboarding_step  = 0,
    )
    db.add(bridge)
    db.commit()

    # Send welcome email with TSP branding
    send_institution_welcome_email(
        to           = req.admin_email,
        brand        = tsp.brand,
        institution  = req.institution_name,
        login_url    = f"https://{tenant.primary_domain}/login",
        temp_password = admin_password,
    )

    return {
        "tenant_id":       tenant.tenant_id,
        "domain":          tenant.primary_domain,
        "admin_email":     req.admin_email,
        "status":          "provisioned",
        "trial_ends_at":   (date.today() + timedelta(days=30)).isoformat(),
    }
```

### Onboarding Checklist Tracker

```python
ONBOARDING_STEPS = [
    ("institution_profile",  "Configure institution profile"),
    ("academic_year",        "Create academic year"),
    ("classes_created",      "Create classes and sections"),
    ("students_enrolled",    "Enroll at least 5 students"),
    ("staff_invited",        "Invite teachers and staff"),
    ("fee_structure",        "Configure fee structure"),
    ("timetable",            "Set up timetable"),
    ("parent_invites",       "Send parent app invites"),
    ("first_attendance",     "Mark first day attendance"),
    ("notifications_config", "Configure notifications"),
]

def compute_onboarding_progress(tenant_id: str) -> int:
    """Returns step index (0–10) of current completion."""
    completed = 0
    for step_key, _ in ONBOARDING_STEPS:
        if is_step_completed(tenant_id, step_key):
            completed += 1
    return completed

def is_step_completed(tenant_id: str, step: str) -> bool:
    checks = {
        "institution_profile":  lambda: tenant_has_logo(tenant_id),
        "students_enrolled":    lambda: count_students(tenant_id) >= 5,
        "first_attendance":     lambda: attendance_records_exist(tenant_id),
        # ... etc.
    }
    return checks.get(step, lambda: False)()
```

---

## 4. On-Behalf Support Access

```python
# POST /api/v1/tsp/tenants/{tenant_id}/onbehalof/
# Body: {"reason": "Investigating fee configuration issue", "duration_hours": 2}

def create_onbehalof_session(tsp_id: str, agent_id: str,
                              tenant_id: str, reason: str,
                              duration_hours: int = 4) -> dict:
    # Verify institution is in TSP's portfolio
    bridge = db.scalar("""
        SELECT 1 FROM tsp_tenants WHERE tsp_id = $1 AND tenant_id = $2
    """, tsp_id, tenant_id)
    if not bridge:
        raise HTTPException(403, "Institution not in your portfolio")

    session = TspOnbehalfSession(
        tsp_id       = tsp_id,
        agent_id     = agent_id,
        tenant_id    = tenant_id,
        expires_at   = datetime.utcnow() + timedelta(hours=min(duration_hours, 4)),
        access_level = "read_only",
        reason       = reason,
    )
    db.add(session); db.commit()

    # Notify institution admin
    send_onbehalof_notification(
        tenant_id    = tenant_id,
        agent_name   = get_staff_name(agent_id),
        tsp_name     = get_tsp_name(tsp_id),
        expires_at   = session.expires_at,
        revoke_url   = f"/admin/support/revoke/{session.session_id}/",
    )

    # Generate signed session token for TSP agent
    token = generate_session_token(
        user_id  = get_institution_admin_id(tenant_id),  # act as admin
        scope    = "read_only",
        metadata = {"onbehalof_session": session.session_id},
        ttl      = duration_hours * 3600,
    )
    return {
        "session_id":  session.session_id,
        "expires_at":  session.expires_at.isoformat(),
        "login_url":   f"https://{get_tenant_domain(tenant_id)}/admin/?session_token={token}",
    }
```

### Institution Admin Banner (Django Template)

```html
{% if request.session.onbehalof_session_id %}
<div class="on-behalf-banner alert-warning" role="alert">
  ⚠️ <strong>{{ tsp_name }}</strong> support agent
  <strong>{{ agent_name }}</strong> is currently viewing this portal
  (read-only access · expires {{ expires_at | timesince }}).
  <a hx-post="/admin/support/revoke/{{ session_id }}/"
     hx-confirm="Revoke support access immediately?"
     class="btn btn-sm btn-danger ms-2">
    Revoke Access
  </a>
</div>
{% endif %}
```

---

## 5. White-label Flutter App Pipeline

### GitHub Actions Workflow

```yaml
# .github/workflows/tsp_flavor_build.yml
name: TSP White-label Build

on:
  workflow_dispatch:
    inputs:
      brand_id: { required: true }
      tsp_id:   { required: true }

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Fetch brand config
        run: |
          curl -H "Authorization: Bearer ${{ secrets.PLATFORM_TOKEN }}" \
            https://api.eduforge.in/api/v1/platform/brands/${{ inputs.brand_id }} \
            -o brand_config.json

      - name: Patch Flutter flavor
        run: |
          python scripts/patch_flavor.py \
            --brand-config brand_config.json \
            --flavor tsp_${{ inputs.brand_id }}

      - name: Build Android APK
        run: |
          flutter build apk \
            --flavor tsp_${{ inputs.brand_id }} \
            --dart-define BRAND_ID=${{ inputs.brand_id }} \
            --dart-define API_BASE=https://api.eduforge.in

      - name: Build iOS IPA
        run: |
          flutter build ipa \
            --flavor tsp_${{ inputs.brand_id }} \
            --dart-define BRAND_ID=${{ inputs.brand_id }}

      - name: Publish to Play Store (internal track)
        uses: r0adkll/upload-google-play@v1
        with:
          serviceAccountJsonPlainText: ${{ secrets[format('GOOGLE_PLAY_{0}', inputs.tsp_id)] }}
          packageName: ${{ fromJSON(steps.brand.outputs.bundle_id) }}
          releaseFiles: build/app/outputs/bundle/release/*.aab
          track: internal
```

### Flutter Brand Injection

```dart
// lib/config/brand_config.dart
// Values injected at build time via --dart-define

const brandId    = String.fromEnvironment('BRAND_ID',    defaultValue: 'eduforge');
const brandName  = String.fromEnvironment('BRAND_NAME',  defaultValue: 'EduForge');
const apiBase    = String.fromEnvironment('API_BASE',    defaultValue: 'https://api.eduforge.in');
const primaryHex = String.fromEnvironment('PRIMARY_HEX', defaultValue: '#1A73E8');

class BrandTheme {
  static ThemeData get theme => ThemeData(
    primaryColor: Color(int.parse(primaryHex.replaceFirst('#', '0xFF'))),
    // ...
  );
}
```

### OTA Updates (Shorebird)

```bash
# Non-UI hotfix — no app store review needed
shorebird patch android \
  --flavor tsp_brand_xyz \
  --dart-define BRAND_ID=brand_xyz

# Rolls out to all users of that flavor automatically
```

---

## 6. TSP Wholesale Billing

### Monthly Invoice Calculation

```python
# Lambda: tsp_billing_calculator — runs D+1 of each month

def calculate_tsp_invoice(tsp_id: str, period_start: date, period_end: date) -> dict:
    # Count active students across all TSP institutions
    active_students = db.scalar("""
        SELECT COUNT(DISTINCT s.student_id)
        FROM   students s
        JOIN   tsp_tenants tt ON tt.tenant_id = s.tenant_id
        WHERE  tt.tsp_id = $1
          AND  EXISTS (
              SELECT 1 FROM user_sessions us
              WHERE us.user_id = s.student_id
                AND us.created_at BETWEEN $2 AND $3
          )
    """, tsp_id, period_start, period_end)

    tsp               = get_tsp(tsp_id)
    wholesale_plan    = get_plan(tsp.wholesale_plan_id)
    base_rate         = wholesale_plan.price_inr   # per student per month
    base_amount       = active_students * float(base_rate)

    # Volume discount
    discount_pct      = tsp.volume_discount_pct
    if active_students > 100000:
        discount_pct = max(discount_pct, 25.0)
    discount_amount   = base_amount * discount_pct / 100

    net_amount        = base_amount - discount_amount
    gst_amount        = net_amount * 0.18    # 18% GST on SaaS (not education exempt)

    # Create billing cycle record
    cycle = TspBillingCycle(
        tsp_id          = tsp_id,
        period_start    = period_start,
        period_end      = period_end,
        total_active_students = active_students,
        base_rate       = base_rate,
        wholesale_amount = base_amount,
        volume_discount  = discount_amount,
        net_amount       = net_amount,
        gst_amount       = gst_amount,
        payment_status  = "pending",
    )
    db.add(cycle); db.commit()

    # Generate invoice via Module 56
    invoice_id = module56.generate_invoice(
        seller_gstin  = EDUFORGE_GSTIN,
        buyer_gstin   = tsp.gstin,
        buyer_name    = tsp.company_name,
        line_items    = [{
            "description": f"EduForge Platform — {active_students:,} active students "
                           f"({period_start.strftime('%b %Y')})",
            "sac_code":   "998431",    # 18% GST — SaaS for coaching
            "amount":     net_amount,
        }],
    )
    cycle.invoice_id = invoice_id
    db.commit()
    return {"cycle_id": cycle.cycle_id, "invoice_id": invoice_id, "amount": net_amount + gst_amount}
```

---

## 7. Data Model

```sql
-- tsps
CREATE TABLE tsp.tsps (
    tsp_id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_name            VARCHAR(200) NOT NULL,
    contact_name            VARCHAR(100) NOT NULL,
    contact_email           VARCHAR(200) NOT NULL UNIQUE,
    phone                   VARCHAR(15),
    gstin                   VARCHAR(15),
    website                 TEXT,
    status                  VARCHAR(20) DEFAULT 'pending'
                            CHECK (status IN ('pending','active','suspended','terminated')),
    tier                    VARCHAR(20) DEFAULT 'standard'
                            CHECK (tier IN ('standard','professional','enterprise')),
    wholesale_plan_id       UUID REFERENCES subscriptions.subscription_plans(plan_id),
    credit_terms_days       INT DEFAULT 0,
    volume_discount_pct     NUMERIC(5,2) DEFAULT 0,
    tsp_agreement_signed_at TIMESTAMPTZ,
    approved_by             UUID,
    created_at              TIMESTAMPTZ DEFAULT NOW()
);

-- tsp_brand_profiles
CREATE TABLE tsp.tsp_brand_profiles (
    brand_id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tsp_id                  UUID NOT NULL REFERENCES tsp.tsps(tsp_id),
    brand_name              VARCHAR(100) NOT NULL,
    app_name                VARCHAR(50) NOT NULL,
    primary_domain          TEXT UNIQUE,
    logo_r2_key             TEXT,
    favicon_r2_key          TEXT,
    primary_color           VARCHAR(7) DEFAULT '#1A73E8',
    secondary_color         VARCHAR(7) DEFAULT '#34A853',
    accent_color            VARCHAR(7) DEFAULT '#FBBC04',
    sidebar_bg_color        VARCHAR(7) DEFAULT '#1A1A2E',
    email_sender_name       VARCHAR(100),
    email_sender_address    VARCHAR(200),
    ses_domain_verified     BOOLEAN DEFAULT FALSE,
    sms_sender_id           VARCHAR(6),
    custom_footer_html      TEXT,
    hide_eduforge_branding  BOOLEAN DEFAULT FALSE,
    ai_persona_name         VARCHAR(50) DEFAULT 'EduForge AI',
    flutter_bundle_id       VARCHAR(100),
    cloudflare_hostname_id  VARCHAR(60),
    tls_status              VARCHAR(20) DEFAULT 'pending',
    is_default              BOOLEAN DEFAULT FALSE,
    created_at              TIMESTAMPTZ DEFAULT NOW(),
    updated_at              TIMESTAMPTZ DEFAULT NOW()
);

-- tsp_tenants (bridge: TSP ↔ tenant)
CREATE TABLE tsp.tsp_tenants (
    tsp_tenant_id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tsp_id                  UUID NOT NULL REFERENCES tsp.tsps(tsp_id),
    tenant_id               UUID NOT NULL REFERENCES tenants(tenant_id) UNIQUE,
    brand_profile_id        UUID NOT NULL REFERENCES tsp.tsp_brand_profiles(brand_id),
    provisioned_at          TIMESTAMPTZ DEFAULT NOW(),
    activated_at            TIMESTAMPTZ,
    go_live_date            DATE,
    retail_plan_id          UUID REFERENCES subscriptions.subscription_plans(plan_id),
    billing_status          VARCHAR(20) DEFAULT 'trial'
                            CHECK (billing_status IN ('trial','active','overdue','suspended')),
    onboarding_step         SMALLINT DEFAULT 0,
    onboarding_completed_at TIMESTAMPTZ,
    notes                   TEXT
);

CREATE INDEX idx_tsp_tenants_tsp ON tsp.tsp_tenants (tsp_id);

-- tsp_feature_config
CREATE TABLE tsp.tsp_feature_config (
    config_id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tsp_id              UUID NOT NULL REFERENCES tsp.tsps(tsp_id) UNIQUE,
    enabled_modules     TEXT[] DEFAULT '{}'::TEXT[],
    custom_terminology  JSONB DEFAULT '{}',
    custom_help_url     TEXT,
    fcm_project_id      VARCHAR(100),
    fcm_service_account JSONB,           -- encrypted at rest
    whatsapp_bsp_config JSONB,           -- encrypted at rest
    created_at          TIMESTAMPTZ DEFAULT NOW(),
    updated_at          TIMESTAMPTZ DEFAULT NOW()
);

-- tsp_onbehalof_sessions
CREATE TABLE tsp.tsp_onbehalof_sessions (
    session_id      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tsp_id          UUID NOT NULL REFERENCES tsp.tsps(tsp_id),
    agent_id        UUID NOT NULL REFERENCES staff(staff_id),
    tenant_id       UUID NOT NULL REFERENCES tenants(tenant_id),
    started_at      TIMESTAMPTZ DEFAULT NOW(),
    expires_at      TIMESTAMPTZ NOT NULL,
    ended_at        TIMESTAMPTZ,
    access_level    VARCHAR(20) DEFAULT 'read_only',
    reason          TEXT,
    revoked_by      UUID,
    revoked_at      TIMESTAMPTZ
);

CREATE INDEX idx_obo_tenant ON tsp.tsp_onbehalof_sessions (tenant_id, started_at DESC);

-- tsp_billing_cycles
CREATE TABLE tsp.tsp_billing_cycles (
    cycle_id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tsp_id                  UUID NOT NULL REFERENCES tsp.tsps(tsp_id),
    period_start            DATE NOT NULL,
    period_end              DATE NOT NULL,
    total_active_students   INT NOT NULL,
    base_rate               NUMERIC(10,4) NOT NULL,
    wholesale_amount        NUMERIC(12,2) NOT NULL,
    volume_discount         NUMERIC(12,2) DEFAULT 0,
    net_amount              NUMERIC(12,2) NOT NULL,
    gst_amount              NUMERIC(12,2) NOT NULL,
    total_amount            NUMERIC(12,2) GENERATED ALWAYS AS (net_amount + gst_amount) STORED,
    invoice_id              UUID,
    payment_status          VARCHAR(20) DEFAULT 'pending'
                            CHECK (payment_status IN ('pending','paid','overdue','waived')),
    paid_at                 TIMESTAMPTZ,
    created_at              TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE (tsp_id, period_start)
);
```

---

## 8. API Reference (TSP-specific)

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| `POST` | `/api/v1/tsp/tenants/` | TSP API Key | Provision new institution |
| `GET` | `/api/v1/tsp/tenants/` | TSP API Key | List all managed institutions |
| `GET` | `/api/v1/tsp/tenants/{id}/` | TSP API Key | Institution metadata + usage summary |
| `PATCH` | `/api/v1/tsp/tenants/{id}/status/` | TSP API Key | Activate / suspend institution |
| `POST` | `/api/v1/tsp/tenants/bulk-provision/` | TSP API Key | Bulk provision from CSV |
| `POST` | `/api/v1/tsp/tenants/{id}/onbehalof/` | TSP API Key | Create support session |
| `DELETE` | `/api/v1/tsp/tenants/{id}/onbehalof/{sid}/` | TSP API Key | Revoke support session |
| `GET` | `/api/v1/tsp/analytics/portfolio/` | TSP API Key | Portfolio analytics |
| `GET` | `/api/v1/tsp/analytics/churn-risk/` | TSP API Key | Churn-risk institutions list |
| `GET` | `/api/v1/tsp/billing/current/` | TSP API Key | Current billing cycle |
| `GET` | `/api/v1/tsp/billing/invoices/` | TSP API Key | Invoice history |
| `POST` | `/api/v1/tsp/brands/` | TSP Portal Session | Create brand profile |
| `PATCH` | `/api/v1/tsp/brands/{id}/` | TSP Portal Session | Update brand config |
| `POST` | `/api/v1/tsp/brands/{id}/activate-domain/` | TSP Portal Session | Provision Cloudflare hostname |
| `POST` | `/api/v1/tsp/brands/{id}/build-app/` | TSP Portal Session | Trigger Flutter app build |
| `GET` | `/api/v1/tsp/brands/{id}/app-build-status/` | TSP Portal Session | Build pipeline status |

---

## 9. Background Jobs

| Job | Trigger | Function |
|-----|---------|----------|
| `tsp_billing_calculator` | EventBridge D+1 of month | Count active students → generate wholesale invoice |
| `tsp_churn_monitor` | EventBridge daily 8 AM | Flag institutions not logged in 30+ days |
| `tsp_onboarding_monitor` | EventBridge daily | Alert TSP for stuck onboarding (7 days same step) |
| `cloudflare_hostname_provisioner` | On brand domain save | Cloudflare API → TLS provisioning |
| `tls_expiry_monitor` | EventBridge monthly | Check Cloudflare cert validity; alert at T-30 |
| `tsp_app_rebuilder` | On EduForge platform release | Trigger GitHub Actions for all active TSP flavors |
| `onbehalof_session_cleanup` | EventBridge every 30 min | Expire sessions past `expires_at` |

---

## 10. TSP Portal — Web Interface (HTMX)

### Portfolio Grid

```html
<!-- HTMX live search -->
<input type="search"
       hx-get="/tsp/institutions/"
       hx-trigger="keyup changed delay:300ms"
       hx-target="#institution-grid"
       placeholder="Search institutions…">

<div id="institution-grid"
     hx-get="/tsp/institutions/"
     hx-trigger="load">
  Loading…
</div>

<!-- _institution_card.html partial -->
{% for inst in institutions %}
<div class="institution-card {% if inst.churn_risk %}border-danger{% endif %}">
  <h5>{{ inst.institution_name }}</h5>
  <span class="badge {{ inst.billing_status }}">{{ inst.billing_status | title }}</span>
  <div class="meta">
    <span>{{ inst.active_students }} students</span>
    <span>Last login: {{ inst.last_login_at | timesince }}</span>
    <span>Onboarding: {{ inst.onboarding_step }}/10</span>
  </div>
  <div class="actions">
    <a href="/tsp/institutions/{{ inst.tenant_id }}/">View Details</a>
    <button hx-post="/api/v1/tsp/tenants/{{ inst.tenant_id }}/onbehalof/"
            hx-prompt="Reason for support access:"
            class="btn btn-sm btn-outline-secondary">
      Support Access
    </button>
  </div>
</div>
{% endfor %}
```

---

## 11. DPDPA & Legal

| Aspect | Implementation |
|--------|---------------|
| **TSP agreement** | Digitally signed before TSP activation. Governs wholesale pricing, sub-processor obligations, incident notification. Stored as PDF in R2. |
| **No student data access** | TSP API endpoints return only institution-level metadata (student count, last login). Zero access to student names, Aadhaar, results, or any PII. |
| **On-behalf sessions** | Read-only. Every session logged with reason. Institution admin sees banner and can revoke. All access events written to Module 42 audit. |
| **Data isolation** | TSP `tsp_id` filter enforced on every portfolio query. Cross-TSP data access architecturally impossible (row-level security + API key scope). |
| **Sub-processor obligations** | TSP must include DPDPA-equivalent data handling clauses in their institution contracts. Annual compliance check by EduForge. |
| **Incident notification** | TSP must notify EduForge within 24 hours of any data incident involving managed institutions. EduForge notifies DPBI within 72 hours. |
| **Termination & data return** | On TSP termination: 90-day transition period; institutions can migrate directly to EduForge or export all data; TSP given no further access after termination notice. |
