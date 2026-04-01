# C-23 — API Rate Limiting & Abuse Prevention

> **Route:** `/engineering/rate-limiting/`
> **Division:** C — Engineering
> **Primary Role:** Security Engineer (Role 16, Level 5) · Backend Engineer (Role 11, Level 4)
> **Read Access:** Platform Admin (Role 10) · DevOps/SRE (Role 14) · CTO (Role 3)
> **File:** `c-23-rate-limiting.md`
> **Priority:** P0 — 74K concurrent exam submissions; one abusive tenant can DoS the entire platform
> **Status:** ✅ New page — rate limiting policy and monitoring console

---

## 1. Purpose

EduForge is a multi-tenant platform where 2,050 institutions share the same infrastructure. Without rate limiting: (1) a coaching centre running a 15,000-student exam could monopolize API capacity and degrade service for 2,049 other institutions, (2) a misconfigured integration script could send 100,000 API calls/minute, (3) a credential-stuffing attack on the login endpoint could lock out legitimate users, and (4) a rogue webhook consumer could retry failed deliveries infinitely.

This page provides: (1) real-time rate limit dashboard showing current consumption per tenant/endpoint/IP, (2) rate limit policy configuration (per-tenant, per-endpoint, per-IP, per-user), (3) abuse detection (anomalous traffic patterns), (4) throttle event log (every 429 response logged), (5) allowlist/blocklist management, and (6) exam-day burst capacity allocation (pre-scheduled rate limit increases for known exam windows).

---

## 2. Rate Limiting Architecture

```
RATE LIMITING LAYERS — EduForge

LAYER 1: Cloudflare WAF (Edge)
  → DDoS protection (automatic)
  → IP reputation blocking
  → Challenge pages for suspicious IPs
  → Rate: 1,000 req/min per IP (global)

LAYER 2: Django Middleware (Application)
  → Per-tenant rate limiting (based on API key / session tenant)
  → Per-endpoint rate limiting (login endpoint stricter than read endpoints)
  → Per-user rate limiting (individual user within a tenant)
  → Implementation: Token bucket algorithm
  → Storage: In-memory (process-level) + PostgreSQL for persistence
  → NO REDIS (per EduForge architecture — Redis prohibited)

LAYER 3: Exam Engine (Custom)
  → Exam submission endpoint: Special rate handling
  → During active exam: 1 submit per student per exam (not rate-limited by frequency
    but by business rule — duplicate submit = idempotent, not blocked)
  → Answer save: Auto-save every 30s per student → rate = exam_students × 2/min
  → Pre-computed capacity: 74,000 concurrent × 2/min = 148,000 saves/min peak

RATE LIMIT STORAGE (No Redis):
  In-memory: Python `collections.defaultdict` with TTL (per-process)
  Cross-process: PostgreSQL `rate_limit_counter` table with window-based counting
  Trade-off: Slightly less precise than Redis (eventual consistency across workers)
             but eliminates Redis as infrastructure dependency
  Accuracy: ±5% at high concurrency (acceptable for rate limiting)
```

---

## 3. Page Layout

```
┌─────────────────────────────────────────────────────────────────────┐
│  API Rate Limiting & Abuse Prevention                               │
├─────────────────────────────────────────────────────────────────────┤
│  RATE LIMIT KPI (5 tiles)                                           │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ │
│  │ 42K/min  │ │ 148      │ │ 0        │ │ 3        │ │ 2        │ │
│  │ Current  │ │ Throttled│ │ Blocked  │ │ Tenants  │ │ Exam Day │ │
│  │ API Rate │ │ (429s)   │ │ IPs      │ │ >80%     │ │ Burst    │ │
│  │ (global) │ │ last 1h  │ │ Today    │ │ Capacity │ │ Scheduled│ │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘ │
├─────────────────────────────────────────────────────────────────────┤
│  [Live Traffic] [Policies] [Throttle Log] [Abuse Detection] [Exam Burst] │
├─────────────────────────────────────────────────────────────────────┤
│  LIVE TRAFFIC — Top 10 Tenants by API Rate                          │
│                                                                     │
│  Tenant              │ Rate/min │ Limit  │ Usage% │ Status         │
│  ─────────────────────────────────────────────────────────────────  │
│  ABC Coaching (T-042)│ 8,240    │ 10,000 │ 82.4%  │ ⚠️ Near limit │
│  XYZ Schools (T-108) │ 4,120    │ 5,000  │ 82.4%  │ ⚠️ Near limit │
│  PQR College (T-215) │ 2,840    │ 5,000  │ 56.8%  │ ✅ Normal     │
│  DEF Coaching (T-067)│ 2,100    │ 10,000 │ 21.0%  │ ✅ Normal     │
│  ...                 │          │        │        │               │
│                                                                     │
│  ENDPOINT HEAT MAP (top 5 by traffic):                              │
│  /api/v1/exam/save-answer/   ████████████████████ 38,200/min       │
│  /api/v1/auth/verify-otp/    █████████ 12,400/min                  │
│  /api/v1/attendance/mark/     ████ 4,800/min                       │
│  /api/v1/student/dashboard/   ███ 3,200/min                        │
│  /api/v1/fee/status/          ██ 2,100/min                         │
├─────────────────────────────────────────────────────────────────────┤
│  RATE LIMIT POLICIES                                                │
│                                                                     │
│  Endpoint Pattern        │ Per Tenant │ Per User  │ Per IP  │ Notes │
│  ─────────────────────────────────────────────────────────────────  │
│  /api/v1/auth/login/     │ 100/min    │ 5/min     │ 10/min  │ Strict│
│  /api/v1/auth/otp/       │ 200/min    │ 3/min     │ 5/min   │ OTP   │
│  /api/v1/exam/save-*/    │ 50K/min    │ 120/min   │ —       │ Exam  │
│  /api/v1/exam/submit/    │ 20K/min    │ 1/exam    │ —       │ Idmpt │
│  /api/v1/*/              │ 5K/min     │ 60/min    │ 100/min │ Default│
│  /webhook/*/             │ 500/min    │ —         │ —       │ Inbound│
│                                                                     │
│  [Edit Policy]  [Add Override]  [View Throttle Log]                 │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 4. Data Models

```python
class RateLimitPolicy(models.Model):
    """Rate limit rules per endpoint pattern."""
    endpoint_pattern = models.CharField(max_length=200)  # "/api/v1/auth/login/"
    scope = models.CharField(choices=[
        ('TENANT', 'Per Tenant'), ('USER', 'Per User'), ('IP', 'Per IP'), ('GLOBAL', 'Global')
    ])
    requests_per_minute = models.IntegerField()
    burst_allowance = models.IntegerField(default=0)  # Extra capacity during burst
    response_on_limit = models.CharField(choices=[
        ('THROTTLE', '429 Too Many Requests'), ('QUEUE', 'Queue and Retry'),
        ('DEGRADE', 'Return Cached Response')
    ], default='THROTTLE')
    enabled = models.BooleanField(default=True)
    applies_to_exam_day = models.BooleanField(default=True)  # Some policies relaxed on exam day

class RateLimitCounter(models.Model):
    """PostgreSQL-based rate counter (no Redis)."""
    scope_type = models.CharField(max_length=10)  # "TENANT", "USER", "IP"
    scope_id = models.CharField(max_length=100)  # tenant_id, user_id, or IP
    endpoint_pattern = models.CharField(max_length=200)
    window_start = models.DateTimeField()  # Start of the 1-minute window
    request_count = models.IntegerField(default=0)

    class Meta:
        unique_together = ('scope_type', 'scope_id', 'endpoint_pattern', 'window_start')
        indexes = [models.Index(fields=['window_start'])]  # For cleanup

class ThrottleEvent(models.Model):
    """Every 429 response logged for analysis."""
    timestamp = models.DateTimeField(auto_now_add=True)
    scope_type = models.CharField(max_length=10)
    scope_id = models.CharField(max_length=100)
    endpoint = models.CharField(max_length=200)
    request_count_at_throttle = models.IntegerField()
    limit_applied = models.IntegerField()
    ip_address = models.GenericIPAddressField()
    user_agent = models.CharField(max_length=500, null=True)

class ExamDayBurst(models.Model):
    """Pre-scheduled rate limit increases for known exam windows."""
    tenant_id = models.IntegerField()
    exam_id = models.IntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    expected_concurrent = models.IntegerField()
    burst_multiplier = models.FloatField(default=2.0)  # 2× normal rate limit
    approved_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)

class IPBlocklist(models.Model):
    ip_address = models.GenericIPAddressField()
    reason = models.CharField(max_length=200)
    blocked_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True)  # null = permanent
    blocked_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)
```

---

## 5. Celery Tasks

| Task ID | Task | Schedule | Description |
|---|---|---|---|
| C-RL-1 | `cleanup_rate_counters` | Every 5 min | Delete `RateLimitCounter` rows older than 5 minutes |
| C-RL-2 | `detect_abuse_patterns` | Every 15 min | Analyse throttle events for patterns (same IP hitting login from 50 tenants = credential stuffing) |
| C-RL-3 | `exam_burst_activate` | Every 1 min | Check `ExamDayBurst` for upcoming exams; apply burst multiplier 15 min before exam start |
| C-RL-4 | `daily_rate_report` | Daily 7 AM | Summary of yesterday's rate limiting: top throttled tenants, blocked IPs, abuse detections |

---

## 6. Business Rules

- **No Redis rule compliance:** EduForge's architecture explicitly prohibits Redis. Rate limiting typically uses Redis for atomic counters. This page implements PostgreSQL-based window counting with `RateLimitCounter` — slightly less precise (±5%) but eliminates an infrastructure dependency. The trade-off is acceptable: rate limiting is not an exact science; ±5% variance at 5,000 req/min means ±250 requests which does not meaningfully affect platform protection.
- **Exam-day burst scheduling is critical.** ABC Coaching running a 15,000-student exam needs ~30,000 save-answer requests/minute (2 saves/student/min). Their default tenant limit is 10,000/min. Without pre-scheduled burst capacity, their exam breaks. The exam scheduling system (F-01) automatically creates `ExamDayBurst` records for exams with >1,000 students. DevOps approves the burst allocation.
- **Login endpoint rate limiting prevents credential stuffing.** 5 attempts per user per minute, 10 per IP per minute, 100 per tenant per minute. After 5 failed attempts: account locked for 15 minutes (not permanent — students forget passwords frequently). After 10 from same IP: CAPTCHA challenge. This protects student accounts without creating excessive friction for legitimate users who simply mistype passwords.
- **OTP endpoint is the most abused endpoint.** Automated scripts requesting OTPs to random phone numbers (OTP bombing) costs money (₹0.25/SMS via MSG91) and constitutes harassment of the phone number owner. 3 OTP requests per user per minute; 5 per IP per minute. After 3 failed OTP verifications: 30-minute cooldown. This prevents both financial drain and harassment.
- **Webhook inbound rate limiting (500/min) protects against webhook replay attacks.** Razorpay webhooks during high payment volume can spike; legitimate Razorpay traffic should not exceed 200/min at current scale (2,050 invoices/month). A sustained 500+/min from a webhook source IP that is not Razorpay's known range is suspicious and auto-blocked.

---

*Last updated: 2026-03-30 · Group 1 — Platform Admin · Division C*
