# Module 51 — B2B API & Partner Portal

## 1. Purpose & Scope

The B2B API & Partner Portal opens EduForge data and services to authorised external systems. It provides a RESTful JSON API, OAuth 2.0 authentication, event-driven webhooks, and a self-service developer portal — giving ERP vendors, government portals, assessment companies, and technology partners a secure, rate-limited, audited way to integrate.

**Integration patterns supported:**

| Pattern | Mechanism | Typical Use Case |
|---------|-----------|-----------------|
| Server-to-server | API Key | ERP sync, nightly student import |
| Partner app on behalf of institution | OAuth 2.0 + PKCE | Parent app, analytics dashboard |
| Real-time event feed | Webhooks | Trigger actions on fee payment, result publication |
| Public verification | Unauthenticated endpoint | Certificate authenticity check |

**Relationship to other modules:**
- Module 50 (Subscription & Access Control) gates which partner tiers can access which endpoints
- Module 52 (White-label TSP Portal) builds on this module's TSP-extended endpoints
- Module 42 (DPDPA Audit Log) receives every API call event
- Module 35 (Notifications) can be triggered via the Notifications API

---

## 2. Authentication

### API Key

```
Authorization: Bearer sk_live_AbCdEf1234567890XyZw
                          │      │
                          prefix  random 32-char token
```

**Key lifecycle:**

```
Partner creates key in portal
    └─ System generates random 40-char token
    └─ key_prefix = first 10 chars (stored plaintext for lookup)
    └─ key_hash   = HMAC-SHA256(token, HMAC_SECRET) (stored — plaintext never saved)
    └─ Full key shown ONCE to partner (copy prompt)

Request arrives
    └─ Extract token from Authorization header
    └─ Compute HMAC-SHA256(token, HMAC_SECRET) = request_hash
    └─ SELECT from api_keys WHERE key_prefix = $1 (fast lookup)
    └─ Constant-time compare: request_hash == stored key_hash
    └─ If matched: extract tenant_id, scopes, ip_allowlist
    └─ IP allowlist check (if configured)
    └─ Rate limit check (DynamoDB sliding window)
```

### OAuth 2.0 + PKCE

```
1. Partner redirects user to:
   GET /oauth/authorize
       ?client_id=app_xyz
       &scope=students:read+attendance:read
       &redirect_uri=https://partner.example.com/callback
       &response_type=code
       &state=random_csrf_token
       &code_challenge=BASE64URL(SHA256(code_verifier))
       &code_challenge_method=S256

2. EduForge shows consent screen to institution admin:
   "PartnerApp wants to:
    ✓ Read student list
    ✓ Read attendance records
    ✗ Write attendance (not requested)"

3. Admin approves → redirect to:
   https://partner.example.com/callback?code=AUTH_CODE&state=...

4. Partner exchanges code:
   POST /oauth/token
   {
     "grant_type":    "authorization_code",
     "code":          "AUTH_CODE",
     "redirect_uri":  "https://partner.example.com/callback",
     "code_verifier": "original_verifier"  ← PKCE verification
   }

5. Response:
   {
     "access_token":  "eyJ...",   ← RS256 JWT, 1-hour TTL
     "token_type":    "Bearer",
     "expires_in":    3600,
     "refresh_token": "rt_...",   ← 30-day TTL (if offline_access scope)
     "scope":         "students:read attendance:read"
   }
```

---

## 3. Rate Limiting

### DynamoDB Sliding Window

```python
# Per-key per-minute sliding window
# Key: "rate#{key_id}#{current_minute}"

async def check_and_increment_rate_limit(key_id: str, tier: str) -> bool:
    limits  = {"free_dev": 2, "standard": 100, "professional": 1000, "enterprise": 10000}
    limit   = limits[tier]
    minute  = datetime.utcnow().strftime("%Y%m%d%H%M")
    ddb_key = f"rate#{key_id}#{minute}"

    response = await dynamodb.update_item(
        TableName = "rate-limit-counters",
        Key       = {"pk": ddb_key},
        UpdateExpression = "ADD #c :one SET #t = :ttl",
        ExpressionAttributeNames  = {"#c": "count", "#t": "ttl"},
        ExpressionAttributeValues = {":one": 1, ":ttl": int(time.time()) + 120},
        ReturnValues = "UPDATED_NEW"
    )
    current = int(response["Attributes"]["count"])
    return current <= limit
```

### Rate Limit Headers

```python
# Middleware adds to every response
response.headers["X-RateLimit-Limit"]         = str(limit)
response.headers["X-RateLimit-Remaining"]     = str(max(0, limit - current))
response.headers["X-RateLimit-Reset-Seconds"] = str(60 - datetime.utcnow().second)
```

---

## 4. Webhook Delivery System

### Event Topics

| Topic | Trigger | Key Fields |
|-------|---------|-----------|
| `student.enrolled` | New student added | student_id, name, class_id, tenant_id |
| `student.profile_updated` | Student profile changed | student_id, changed_fields[] |
| `attendance.daily_marked` | Daily attendance finalised for a class | class_id, date, present_count, absent_count |
| `fee.payment_recorded` | Fee payment received | student_id, amount, receipt_no, payment_mode |
| `fee.payment_overdue` | Fee overdue threshold crossed | student_id, overdue_amount, due_date |
| `exam.result_published` | Exam results published | exam_id, class_id, published_at |
| `certificate.issued` | Certificate generated | cert_id, student_id, cert_type, qr_hash |
| `homework.graded` | Homework graded by teacher | assignment_id, student_id, score |

### Delivery Lambda

```python
# Lambda webhook_dispatcher — triggered by SQS
# SQS message: {delivery_id, sub_id, event_topic, payload}

def deliver_webhook(delivery_id: str):
    delivery = get_delivery(delivery_id)
    sub      = get_subscription(delivery.sub_id)

    # Build signature
    payload_bytes = json.dumps(delivery.payload, separators=(',', ':')).encode()
    signature     = hmac.new(sub.secret.encode(), payload_bytes, hashlib.sha256).hexdigest()

    headers = {
        "Content-Type":         "application/json",
        "X-EduForge-Event":     delivery.event_topic,
        "X-EduForge-Signature": f"sha256={signature}",
        "X-Request-ID":         str(delivery_id),
        "X-EduForge-Timestamp": str(int(time.time())),
    }

    try:
        response = requests.post(
            delivery.delivery_url,
            json    = delivery.payload,
            headers = headers,
            timeout = 10,                  # 10-second timeout
        )
        status = 'delivered' if response.status_code < 400 else 'failed'
        update_delivery(delivery_id, status=status, http_status=response.status_code)
    except requests.Timeout:
        update_delivery(delivery_id, status='failed', http_status=0)
        schedule_retry(delivery_id)
    except Exception as e:
        update_delivery(delivery_id, status='failed', http_status=-1)
        schedule_retry(delivery_id)

def schedule_retry(delivery_id: str):
    delivery = get_delivery(delivery_id)
    if delivery.attempt_count >= 3:
        mark_as_dead_letter(delivery_id)
        notify_partner_of_failure(delivery.sub_id)
        return

    backoff = {1: 300, 2: 1800, 3: 7200}   # 5min, 30min, 2h
    next_at = datetime.utcnow() + timedelta(seconds=backoff[delivery.attempt_count + 1])
    update_delivery(delivery_id, next_attempt_at=next_at,
                    attempt_count=delivery.attempt_count + 1, status='retrying')
```

### Webhook Signature Verification (Partner Side)

```python
# Python example for partner's webhook handler
import hmac, hashlib

def verify_webhook(body: bytes, signature_header: str, secret: str) -> bool:
    expected = "sha256=" + hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature_header)

@app.post("/webhook")
async def handle_webhook(request: Request):
    body       = await request.body()
    sig_header = request.headers.get("X-EduForge-Signature", "")
    secret     = os.environ["EDUFORGE_WEBHOOK_SECRET"]

    if not verify_webhook(body, sig_header, secret):
        raise HTTPException(400, "Invalid signature")

    event   = json.loads(body)
    topic   = request.headers.get("X-EduForge-Event")

    if topic == "fee.payment_recorded":
        await process_fee_payment(event)

    return {"status": "ok"}   # Return 200 within 10 seconds
```

---

## 5. Core Data APIs

### Students API

```
GET /api/v1/students/
  ?class_id=uuid
  &page_size=100          (max 100)
  &cursor=opaque_cursor   (cursor-based pagination)

Response: {
  "data": [{
    "student_id":  "uuid",
    "name":        "Priya Sharma",
    "email":       "priya@school.com",
    "class_id":    "uuid",
    "class_name":  "Class X-A",
    "roll_number": "2024-001",
    "dob":         "2010-05-15",
    "category":    "General",
    "status":      "active"
  }],
  "pagination": {
    "next_cursor": "eyJpZCI6InV1aWQifQ==",
    "has_more":    true,
    "total":       243
  }
}
```

### Attendance API

```
GET /api/v1/attendance/{class_id}/{date}/

Response: {
  "class_id":    "uuid",
  "date":        "2026-03-26",
  "total":       45,
  "present":     41,
  "absent":      3,
  "late":        1,
  "records": [{
    "student_id":  "uuid",
    "status":      "P",    // P=Present, A=Absent, L=Late, H=Holiday
    "marked_at":   "2026-03-26T09:05:00Z",
    "marked_by":   "teacher_uuid"
  }]
}
```

### Certificate Verification (Unauthenticated)

```
GET /api/v1/certificates/verify/{cert_hash}/

Response (valid): {
  "valid":          true,
  "certificate_type": "Leaving Certificate",
  "student_name":   "Rahul Verma",     // ← no Aadhaar / DOB (minimised)
  "institution":    "ABC Public School",
  "issued_date":    "2026-03-15",
  "cert_id":        "uuid"
}

Response (invalid): {
  "valid": false,
  "message": "Certificate not found or tampered"
}
```

### Bulk Enrollment (Async)

```
POST /api/v1/students/bulk-enroll/
Content-Type: multipart/form-data
Authorization: Bearer sk_live_... (requires students:write scope)

Body: CSV file with columns:
  name, email, mobile, dob, category, class_name, roll_number

Response: {
  "job_id":     "uuid",
  "status":     "queued",
  "total_rows": 248,
  "status_url": "/api/v1/jobs/uuid/status"
}

GET /api/v1/jobs/{job_id}/status
Response: {
  "status":    "completed",
  "processed": 248,
  "succeeded": 245,
  "failed":    3,
  "errors":    [{"row": 12, "reason": "Duplicate email"}, ...]
}
```

---

## 6. Sandbox Environment

```
Base URL:  https://sandbox-api.eduforge.in/api/v1/
Key prefix: sk_test_...
Tenant:     SANDBOX_{partner_id}  (isolated DB + R2 bucket)

Pre-seeded data:
  ├─ 50 students across 3 classes (Class IX-A, X-B, XI-C)
  ├─ 6 months of attendance records
  ├─ 10 exam results (5 subjects each)
  ├─ 30 fee payment records
  └─ 5 issued certificates (for verification API testing)

Reset: POST /api/v1/sandbox/reset/ → wipes + re-seeds in 60 seconds
       Available only to partner with sandbox key (no auth needed for reset)
```

---

## 7. Python SDK

```python
# pip install eduforge-sdk

from eduforge import EduForge, EduForgeError

ef = EduForge(
    api_key    = "sk_live_abc...",
    base_url   = "https://api.eduforge.in",  # optional override for self-hosted
    timeout    = 30,
    max_retries = 3,   # auto-retry on 429 with Retry-After
)

# Pagination helper
for student in ef.students.iter_all(class_id="uuid-class-x"):
    print(student.name)

# Attendance
records = ef.attendance.get(class_id="uuid-class-x", date="2026-03-26")
print(f"Present: {records.present}/{records.total}")

# Error handling
try:
    student = ef.students.get("nonexistent-uuid")
except EduForgeError as e:
    print(e.status_code, e.message)   # 404, "Student not found"

# Webhook subscription
sub = ef.webhooks.subscribe(
    events = ["student.enrolled", "fee.payment_recorded"],
    url    = "https://myapp.example.com/webhooks/eduforge",
    secret = "whsec_my_secret_here",
)
print(sub.id)

# Async version
from eduforge.async_ import AsyncEduForge
import asyncio

async def main():
    async with AsyncEduForge(api_key="sk_live_...") as ef:
        students = await ef.students.list(class_id="uuid")

asyncio.run(main())
```

---

## 8. Data Model

```sql
-- api_partners
CREATE TABLE partner.api_partners (
    partner_id        UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_name      VARCHAR(200) NOT NULL,
    contact_name      VARCHAR(100) NOT NULL,
    contact_email     VARCHAR(200) NOT NULL,
    website           TEXT,
    use_case          TEXT NOT NULL,
    status            VARCHAR(20) DEFAULT 'sandbox'
                      CHECK (status IN ('sandbox','pending_review','active','suspended')),
    partner_tier      VARCHAR(20) DEFAULT 'free_dev',
    is_tsp            BOOLEAN DEFAULT FALSE,
    dpa_signed_at     TIMESTAMPTZ,
    approved_by       UUID REFERENCES platform_admins(admin_id),
    approved_at       TIMESTAMPTZ,
    created_at        TIMESTAMPTZ DEFAULT NOW()
);

-- api_keys
CREATE TABLE partner.api_keys (
    key_id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    partner_id       UUID NOT NULL REFERENCES partner.api_partners(partner_id),
    tenant_id        UUID NOT NULL REFERENCES tenants(tenant_id),
    key_hash         VARCHAR(64) NOT NULL,          -- HMAC-SHA256
    key_prefix       VARCHAR(10) NOT NULL,          -- first 10 chars for lookup
    key_type         VARCHAR(10) DEFAULT 'production'
                     CHECK (key_type IN ('sandbox','production')),
    scopes           TEXT[] NOT NULL,
    ip_allowlist     INET[] DEFAULT '{}',
    expires_at       TIMESTAMPTZ,
    is_revoked       BOOLEAN DEFAULT FALSE,
    revoked_at       TIMESTAMPTZ,
    revoke_reason    TEXT,
    description      VARCHAR(100),
    created_at       TIMESTAMPTZ DEFAULT NOW(),
    last_used_at     TIMESTAMPTZ,
    UNIQUE (key_prefix)
);

CREATE INDEX idx_ak_prefix ON partner.api_keys (key_prefix) WHERE is_revoked = FALSE;

-- oauth_applications
CREATE TABLE partner.oauth_applications (
    app_id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    partner_id          UUID NOT NULL REFERENCES partner.api_partners(partner_id),
    app_name            VARCHAR(100) NOT NULL,
    client_id           VARCHAR(40) UNIQUE NOT NULL DEFAULT gen_random_uuid(),
    client_secret_hash  VARCHAR(64) NOT NULL,
    redirect_uris       TEXT[] NOT NULL,
    allowed_scopes      TEXT[] NOT NULL,
    logo_r2_key         TEXT,
    is_active           BOOLEAN DEFAULT TRUE,
    created_at          TIMESTAMPTZ DEFAULT NOW()
);

-- oauth_authorization_codes
CREATE TABLE partner.oauth_authorization_codes (
    code_hash        VARCHAR(64) PRIMARY KEY,
    app_id           UUID NOT NULL REFERENCES partner.oauth_applications(app_id),
    tenant_id        UUID NOT NULL,
    scopes           TEXT[] NOT NULL,
    code_challenge   VARCHAR(200),
    redirect_uri     TEXT NOT NULL,
    expires_at       TIMESTAMPTZ NOT NULL,
    used             BOOLEAN DEFAULT FALSE
);

-- oauth_tokens
CREATE TABLE partner.oauth_tokens (
    token_id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    app_id               UUID NOT NULL REFERENCES partner.oauth_applications(app_id),
    tenant_id            UUID NOT NULL,
    access_token_hash    VARCHAR(64),
    refresh_token_hash   VARCHAR(64),
    scopes               TEXT[] NOT NULL,
    access_expires_at    TIMESTAMPTZ NOT NULL,
    refresh_expires_at   TIMESTAMPTZ,
    is_revoked           BOOLEAN DEFAULT FALSE,
    created_at           TIMESTAMPTZ DEFAULT NOW()
);

-- webhook_subscriptions
CREATE TABLE partner.webhook_subscriptions (
    sub_id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    partner_id      UUID NOT NULL REFERENCES partner.api_partners(partner_id),
    tenant_id       UUID NOT NULL REFERENCES tenants(tenant_id),
    event_topics    TEXT[] NOT NULL,
    delivery_url    TEXT NOT NULL,
    secret_hash     VARCHAR(64) NOT NULL,
    is_active       BOOLEAN DEFAULT TRUE,
    is_paused       BOOLEAN DEFAULT FALSE,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

-- webhook_deliveries (partitioned by month)
CREATE TABLE partner.webhook_deliveries (
    delivery_id      UUID DEFAULT gen_random_uuid(),
    sub_id           UUID NOT NULL REFERENCES partner.webhook_subscriptions(sub_id),
    event_topic      VARCHAR(60) NOT NULL,
    payload          JSONB NOT NULL,
    delivery_url     TEXT NOT NULL,
    status           VARCHAR(20) DEFAULT 'pending'
                     CHECK (status IN ('pending','delivered','failed','retrying','dead_letter')),
    http_status      INT,
    attempt_count    SMALLINT DEFAULT 0,
    next_attempt_at  TIMESTAMPTZ,
    last_attempt_at  TIMESTAMPTZ,
    created_at       TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (delivery_id, created_at)
) PARTITION BY RANGE (created_at);

-- api_usage_log (partitioned by month, kept 3 months)
CREATE TABLE partner.api_usage_log (
    log_id       UUID DEFAULT gen_random_uuid(),
    key_id       UUID NOT NULL,
    tenant_id    UUID NOT NULL,
    endpoint     VARCHAR(200) NOT NULL,
    method       VARCHAR(10) NOT NULL,
    status_code  SMALLINT NOT NULL,
    latency_ms   INT NOT NULL,
    request_id   UUID,
    ip_address   INET,
    created_at   TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (log_id, created_at)
) PARTITION BY RANGE (created_at);

-- partner_dpa_agreements
CREATE TABLE partner.partner_dpa_agreements (
    dpa_id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    partner_id      UUID NOT NULL REFERENCES partner.api_partners(partner_id),
    signed_by_name  VARCHAR(100) NOT NULL,
    signed_by_email VARCHAR(200) NOT NULL,
    signed_at       TIMESTAMPTZ DEFAULT NOW(),
    dpa_version     VARCHAR(20) NOT NULL,
    ip_address      INET,
    pdf_r2_key      TEXT
);
```

---

## 9. API Reference

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| `GET` | `/api/v1/students/` | API Key (students:read) | Paginated student list |
| `GET` | `/api/v1/students/{id}/` | API Key (students:read) | Single student |
| `POST` | `/api/v1/students/` | API Key (students:write) | Enroll student |
| `POST` | `/api/v1/students/bulk-enroll/` | API Key (students:write) | Bulk enroll via CSV |
| `GET` | `/api/v1/attendance/{class_id}/{date}/` | API Key (attendance:read) | Daily attendance |
| `POST` | `/api/v1/attendance/` | API Key (attendance:write) | Mark attendance |
| `GET` | `/api/v1/results/{exam_id}/` | API Key (results:read) | Exam results |
| `GET` | `/api/v1/students/{id}/results/` | API Key (results:read) | Student result history |
| `GET` | `/api/v1/fees/{student_id}/outstanding/` | API Key (fees:read) | Outstanding fees |
| `GET` | `/api/v1/fees/collections/` | API Key (fees:read) | Fee collection records |
| `POST` | `/api/v1/notifications/send/` | API Key (notifications:send) | Push notification |
| `GET` | `/api/v1/certificates/verify/{hash}/` | Public (no auth) | Certificate verification |
| `GET` | `/api/v1/jobs/{job_id}/status` | API Key | Async job status |
| `GET` | `/api/v1/openapi.json` | Public | OpenAPI 3.0 spec |
| `GET` | `/api/v1/health` | Public | Health check |
| `GET` | `/oauth/authorize` | User (institution admin) | OAuth authorization |
| `POST` | `/oauth/token` | OAuth client credentials | Token exchange |
| `POST` | `/oauth/revoke` | OAuth client credentials | Token revocation |
| `POST` | `/api/v1/partner/keys/` | Portal session | Create API key |
| `DELETE` | `/api/v1/partner/keys/{id}` | Portal session | Revoke API key |
| `POST` | `/api/v1/partner/webhooks/` | Portal session | Subscribe to webhook |
| `POST` | `/api/v1/partner/webhooks/{id}/test/` | Portal session | Send test event |
| `GET` | `/api/v1/partner/usage/` | Portal session | API usage dashboard |

---

## 10. Partner Portal — Web (HTMX)

### API Key Management

```html
<!-- Key list — masked display -->
{% for key in api_keys %}
<div class="key-card">
  <span class="key-prefix">{{ key.prefix }}...</span>
  <span class="badge {{ key.type }}">{{ key.key_type | title }}</span>
  <span class="scopes">{{ key.scopes | join(', ') }}</span>
  <small>Last used: {{ key.last_used_at | timesince }}</small>
  <button hx-delete="/api/v1/partner/keys/{{ key.id }}/"
          hx-confirm="Revoke this API key? This cannot be undone."
          hx-target="closest .key-card"
          hx-swap="outerHTML">
    Revoke
  </button>
</div>
{% endfor %}
```

### Webhook Delivery Log

```html
<!-- HTMX-paginated webhook delivery history -->
<table id="delivery-log">
  <thead><tr><th>Time</th><th>Event</th><th>Status</th><th>HTTP</th><th></th></tr></thead>
  <tbody hx-get="/api/v1/partner/webhooks/{{ sub_id }}/deliveries/"
         hx-trigger="load"
         hx-swap="innerHTML">
    Loading…
  </tbody>
</table>

{% for delivery in deliveries %}
<tr>
  <td>{{ delivery.created_at | date:"d M H:i" }}</td>
  <td><code>{{ delivery.event_topic }}</code></td>
  <td><span class="badge {{ delivery.status }}">{{ delivery.status }}</span></td>
  <td>{{ delivery.http_status }}</td>
  <td>
    <button hx-get="/partner/webhooks/delivery/{{ delivery.id }}/payload/"
            hx-target="#payload-modal"
            class="btn btn-sm">View</button>
  </td>
</tr>
{% endfor %}
```

---

## 11. Background Jobs

| Job | Trigger | Function |
|-----|---------|----------|
| `webhook_dispatcher` | SQS `webhook-delivery.fifo` | POST to partner URL; update delivery status |
| `webhook_retry` | EventBridge every 5 min | Re-queue retrying deliveries whose `next_attempt_at <= NOW()` |
| `api_usage_aggregator` | EventBridge hourly | Aggregate `api_usage_log` → `partner_usage_summary` |
| `key_expiry_notifier` | EventBridge daily 8 AM | Alert partners with keys expiring in 30 days |
| `webhook_failure_notifier` | On 3rd consecutive failure | Email partner contact |
| `sandbox_data_seeder` | On partner sandbox registration | Seed test data for new sandbox tenant |
| `usage_log_cleanup` | EventBridge monthly | Drop `api_usage_log` partition older than 3 months |

---

## 12. DPDPA & Compliance

| Obligation | Implementation |
|------------|---------------|
| **Data Processing Agreement** | DPA digitally signed (checkbox + timestamp + IP) before production key creation. Stored as PDF in R2. |
| **Purpose limitation** | Partner's `use_case` + `scopes` define permitted access. `api_usage_log` audited monthly for scope violations. |
| **Institution consent** | Institution admin must explicitly grant partner API access to their tenant. Consent event logged. |
| **Partner audit trail** | Institution admin can view `GET /admin/api-access-log/` — all partner API calls with endpoint + timestamp. |
| **Suspension** | EduForge can call `PATCH /api/v1/platform/partners/{id}/?status=suspended` with 24-hour notice for violations. |
| **No cross-tenant** | `tenant_id` extracted from API key — impossible to query another tenant's data even with valid key. |
| **Data minimisation** | `?fields=student_id,name` parameter — partner receives only requested fields. |
| **CERT-In 6h** | API security incidents involving partner data leakage: CERT-In notification per Module 42 obligations. |
| **Annual review** | EventBridge annual trigger → alert EduForge partnerships team to review active partner DPA compliance. |
