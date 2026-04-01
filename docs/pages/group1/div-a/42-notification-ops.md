# 42 — Notification Operations

---

## 1. Page Metadata

| Field | Value |
|---|---|
| Page title | Notification Operations |
| Route | `/exec/notification-ops/` |
| Django view | `NotificationOpsView` |
| Template | `exec/notification_ops.html` |
| Priority | **P2** |
| Nav group | Operations |
| Required roles | `coo` · `notification_manager` · `exam_ops_manager` · `ceo` · `superadmin` |
| CTO access | Read-only (no notification actions) |
| CFO | Denied |
| HTMX poll — delivery stats | Every 60s |
| HTMX poll — queue depth | Every 30s |
| Cache | Delivery stats: Redis TTL 55s · Queue depth: Redis TTL 25s |
| Theme tokens | bg-base `#040810` · surface-1 `#08101E` · accent `#6366F1` · danger `#EF4444` · warn `#F59E0B` · success `#22C55E` |

---

## 2. Purpose & Business Logic

**Why notification operations is a P2 executive concern:**

EduForge sends notifications across three channels:
1. **WhatsApp** (via Kaleyra / Exotel) — exam reminders, results, OTPs, institution alerts
2. **SMS** (via TRAI DLT-registered sender ID `EDUFGE`) — OTPs, fallback when WhatsApp fails
3. **Email** (via AWS SES) — invoices, reports, system alerts, onboarding

At 74K concurrent exam students, the OTP delivery window is 60 seconds. If OTP SMS delivery drops below 95%, students cannot log in → exam failures → institution SLA breaches. This page ensures the Notification Manager and COO can see delivery health in real-time and intervene before it cascades.

**TRAI DLT Compliance:**
- Every SMS must be sent from a DLT-registered Sender ID and Template ID
- Using an unregistered template = carrier drops the SMS silently = students miss OTPs
- This page surfaces DLT compliance status so the team knows before exam day

---

## 3. User Roles & Access

| Role | Can View | Can Act |
|---|---|---|
| CEO | All | Read-only |
| COO | All | Trigger manual broadcast, pause channel |
| Notification Manager | All | All notification actions |
| Exam Ops Manager | Delivery stats + OTP section | Read-only |
| CTO | Delivery stats + gateway health | Read-only |
| CFO | No access | Redirect |

---

## 4. Section-wise UI Breakdown

---

### Section 1 — Delivery Summary Strip

**Purpose:** At-a-glance health of all three notification channels.

**UI elements — 6 cards:**

```
╔══════════════╦══════════════╦══════════════╦══════════════╦══════════════╦══════════════╗
║ OTP SUCCESS  ║ WHATSAPP DEL ║ SMS DEL RATE ║ EMAIL DEL    ║ QUEUE DEPTH  ║ DLT ISSUES   ║
║   99.2%      ║   97.8%      ║   98.4%      ║   99.7%      ║     0        ║     0        ║
║  1h window   ║  last 24h   ║  last 24h    ║  last 24h    ║  ● Clear     ║  ● Compliant ║
╚══════════════╩══════════════╩══════════════╩══════════════╩══════════════╩══════════════╝
```

| Card | Alert condition |
|---|---|
| OTP Success % | < 98%: amber · < 95%: red (exam blocker) |
| WhatsApp Delivery | < 95%: amber · < 90%: red |
| SMS Delivery Rate | < 96%: amber · < 92%: red |
| Email Delivery | < 98%: amber |
| Queue Depth | > 500: amber · > 2,000: red |
| DLT Issues | Any > 0: red (TRAI compliance breach) |

**HTMX:** `id="notif-summary"` poll every 60s.

---

### Section 2 — OTP Delivery Deep Dive

**Purpose:** OTP is the most time-sensitive notification. Students have 60–120 seconds to receive and enter their OTP before the exam login window closes.

**UI elements:**
```
OTP DELIVERY ANALYSIS (Last 1 Hour)
─────────────────────────────────────────────────────────────────────────────
Total OTPs sent:  12,842    Delivered within 30s: 11,980 (93.3%)
Delivered 30–60s:    628 (4.9%)  Delivered > 60s: 142 (1.1%)  Failed: 92 (0.7%)

DELIVERY TIME DISTRIBUTION (Chart.js Histogram)
< 10s   ████████████████████████████████  62.4%
10–20s  ████████████████                  28.1%
20–30s  ██                                2.8%
30–60s  █                                 4.9%
> 60s   ░                                 1.1%
Failed  ░                                 0.7%

FAILED OTPs (Last 1h)
+91-98765XXXXX  Reason: Invalid number   Retried: Yes  [View →]
+91-88410XXXXX  Reason: DND registry     Retried: No   [View →]
```

- Failed OTP table: masked phone numbers (last 5 digits only — privacy), reason, retry status
- "Retry Failed OTPs" bulk action (Notification Manager): POST → re-queues failed OTPs via Celery

**HTMX:** `id="otp-detail"` poll every 30s.

---

### Section 3 — Channel-wise Delivery Charts

**Purpose:** 24-hour delivery rate trend per channel — spot degradation before it becomes critical.

**UI elements:**
```
CHANNEL DELIVERY RATES — Last 24 Hours
[WhatsApp ●] [SMS] [Email] — toggle series

Chart.js Line: X = last 24h (hourly), Y = delivery %
Threshold lines: WhatsApp 95%, SMS 96%, Email 98%
```

- Three toggle-able series on one chart
- Any hour dipping below threshold: point highlighted with red dot
- Tooltip: "14:00 — WhatsApp: 97.8% (1,240 sent, 27 failed)"

---

### Section 4 — Queue Monitor

**Purpose:** The notification queue is a Celery/SQS queue. Queue depth = pending notifications waiting to be sent. During exam day, queue can spike to thousands. Depth > 0 for > 5 min = delivery delays.

**UI elements:**
```
NOTIFICATION QUEUE                               Queue Depth: 0 ✅ Clear
─────────────────────────────────────────────────────────────────────────────
Queue Name          Depth   Workers  Oldest Item  Throughput/min
──────────────────────┼───────┼─────────┼─────────────┼──────────────
whatsapp_priority     0       4        —            420/min
sms_otp_priority      0       2        —            180/min
sms_bulk              12      2        2 min ago    280/min
email_transactional   0       2        —             84/min
email_bulk            48      1        8 min ago     62/min
```

- Queue with depth > 0: shows oldest item age — if > 10 min, amber; > 30 min, red
- Worker count: click → shows individual worker status (Celery Flower integration)
- Throughput trend: small sparkline per row

**HTMX:** `id="queue-monitor"` poll every 30s.

---

### Section 5 — TRAI DLT Compliance

**Purpose:** All SMS must use TRAI-registered templates. This section shows all registered templates, their DLT approval status, and flags any outgoing SMS that used an unregistered template.

**UI elements:**
```
TRAI DLT COMPLIANCE                    Sender ID: EDUFGE · DLT PE ID: 1201XXXXXXXX
─────────────────────────────────────────────────────────────────────────────
Template Name          Template ID   Status      Used Today  Last Used
───────────────────────┼─────────────┼────────────┼───────────┼────────────
OTP Login              DLT-001       ✅ Approved   12,842      2 min ago
Exam Reminder          DLT-002       ✅ Approved    4,280      1h ago
Result Notification    DLT-003       ✅ Approved      480      3h ago
New Password Reset     DLT-004       ⚠ Pending       0        —
Custom Announcement    DLT-005       🔴 Rejected      0        —
```

- Rejected template: red row. "Rejected" templates cannot be used — attempting to use = DLT carrier drop
- Pending template: amber. Cannot use until approved.
- "DLT-005 Rejected" — shows rejection reason in drawer

---

### Section 6 — Gateway Health

**Purpose:** Which SMS/WhatsApp gateway vendor is currently healthy?

**UI elements:**
```
GATEWAY HEALTH
─────────────────────────────────────────────────────────────────────────────
Gateway          Type       Status    Latency  Delivery%  Balance
─────────────────┼───────────┼──────────┼─────────┼─────────┼───────────
Kaleyra          WhatsApp   ✅ Active  180ms    97.8%      ₹48,400 (API)
Exotel           SMS        ✅ Active   92ms    98.4%      ₹82,200 credits
AWS SES          Email      ✅ Active   45ms    99.7%      Unlimited (paid)
Exotel (backup)  SMS        ⏸ Standby  —       —          ₹24,000 credits
```

- Balance / credits: amber if < ₹10,000 (risk of service interruption)
- Degraded gateway: row highlighted amber + "Failover available" badge if backup exists
- "Switch to Backup" action (Notification Manager / COO): flips the active SMS gateway

---

## 5. Full Page Wireframe

```
╔══════════════════════════════════════════════════════════════════════════════╗
║  Notification Operations                              [↺ Refresh]           ║
╠══════════╦══════════╦══════════╦══════════╦══════════╦══════════════════════╣
║ OTP 99.2%║ WA 97.8% ║ SMS 98.4%║ EMAIL    ║ QUEUE: 0 ║ DLT: ✅ Compliant    ║
╠══════════╩══════════╩══════════╩══════════╩══════════╩══════════════════════╣
║  OTP DELIVERY (1h)                    QUEUE MONITOR                        ║
║  Total: 12,842  Success < 30s: 93.3%  whatsapp_priority   0 ✅              ║
║  Histogram: [█████████░░░]            sms_otp_priority     0 ✅              ║
║  Failed: 92   [Retry Failed OTPs]     sms_bulk            12 ⏱ 2min ago     ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  CHANNEL DELIVERY — 24h                TRAI DLT COMPLIANCE                  ║
║  [WA ●] [SMS] [Email]                  OTP Login     DLT-001 ✅  12,842 sent ║
║  [Trend chart — delivery % over 24h]   Exam Reminder DLT-002 ✅   4,280 sent ║
║                                        Custom Announ. DLT-005 🔴 Rejected    ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  GATEWAY HEALTH                                                             ║
║  Kaleyra  WhatsApp  ✅ 180ms  97.8%  ₹48,400 balance                        ║
║  Exotel   SMS       ✅  92ms  98.4%  ₹82,200 credits                        ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 6. Component Architecture

| Component | File | Props |
|---|---|---|
| `NotifSummaryCard` | `components/notif/summary_card.html` | `label, value, subline, alert_level` |
| `OTPHistogram` | `components/notif/otp_histogram.html` | `buckets (list of {range, count, pct})` |
| `FailedOTPRow` | `components/notif/failed_otp_row.html` | `masked_number, reason, retried` |
| `QueueRow` | `components/notif/queue_row.html` | `name, depth, workers, oldest_age_min, throughput` |
| `DLTTemplateRow` | `components/notif/dlt_row.html` | `name, template_id, status, used_today` |
| `GatewayHealthRow` | `components/notif/gateway_row.html` | `name, type, status, latency_ms, delivery_pct, balance, has_backup, can_switch` |
| `ChannelDeliveryChart` | `components/notif/delivery_chart.html` | `hours (list of {label, wa_pct, sms_pct, email_pct})` |

---

## 7. HTMX Architecture

| `?part=` | Target | Poll | Trigger |
|---|---|---|---|
| `summary` | `#notif-summary` | 60s | load |
| `otp-detail` | `#otp-detail` | 30s | load |
| `channel-chart` | `#channel-chart` | None | load |
| `queue` | `#queue-monitor` | 30s | load |
| `dlt` | `#dlt-compliance` | None | load |
| `gateways` | `#gateway-health` | 60s | load |

---

## 8. Backend View & API

```python
class NotificationOpsView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "portal.view_notification_ops"

    def get(self, request):
        allowed = {"coo","notification_manager","exam_ops_manager","ceo","cto","superadmin"}
        if request.user.role not in allowed:
            return redirect("exec:dashboard")

        can_act = request.user.role in {"coo","notification_manager","superadmin"}

        if _is_htmx(request):
            part = request.GET.get("part","")
            ctx = {"can_act": can_act}
            dispatch = {
                "summary":      "exec/notif/partials/summary.html",
                "otp-detail":   "exec/notif/partials/otp_detail.html",
                "channel-chart":"exec/notif/partials/channel_chart.html",
                "queue":        "exec/notif/partials/queue_monitor.html",
                "dlt":          "exec/notif/partials/dlt_compliance.html",
                "gateways":     "exec/notif/partials/gateway_health.html",
            }
            if part in dispatch:
                return render(request, dispatch[part], ctx)
        return render(request, "exec/notification_ops.html", {"can_act": can_act})
```

**Action endpoints:**

| Method | URL | Permission | Action |
|---|---|---|---|
| POST | `/exec/notification-ops/actions/retry-otps/` | `portal.manage_notifications` | Re-queue failed OTPs from last 1h via Celery |
| POST | `/exec/notification-ops/actions/switch-gateway/` | `portal.manage_notifications` | Flip active SMS gateway in Redis config key |
| POST | `/exec/notification-ops/actions/pause-channel/` | `portal.manage_notifications` | Set `notif:channel:{name}:paused` Redis key |

---

## 9. Database Schema

```python
class NotificationLog(models.Model):
    channel      = models.CharField(max_length=20,
                       choices=[("whatsapp","WhatsApp"),("sms","SMS"),("email","Email")])
    notif_type   = models.CharField(max_length=50)  # otp / exam_reminder / result / etc.
    recipient    = models.CharField(max_length=200)  # phone/email (masked in UI)
    status       = models.CharField(max_length=20,
                       choices=[("queued","Queued"),("sent","Sent"),
                                ("delivered","Delivered"),("failed","Failed")])
    gateway      = models.CharField(max_length=50)
    sent_at      = models.DateTimeField(null=True, db_index=True)
    delivered_at = models.DateTimeField(null=True)
    delivery_latency_ms = models.IntegerField(null=True)
    failure_reason = models.CharField(max_length=200, blank=True)
    dlt_template_id = models.CharField(max_length=50, blank=True)
    retried      = models.BooleanField(default=False)
    institution  = models.ForeignKey("Institution", null=True, on_delete=models.SET_NULL)

    class Meta:
        indexes = [
            models.Index(fields=["channel","status","sent_at"]),
            models.Index(fields=["notif_type","sent_at"]),
        ]


class DLTTemplate(models.Model):
    name         = models.CharField(max_length=100)
    template_id  = models.CharField(max_length=50, unique=True)
    content      = models.TextField()
    status       = models.CharField(max_length=20,
                       choices=[("approved","Approved"),("pending","Pending"),
                                ("rejected","Rejected")])
    rejection_reason = models.TextField(blank=True)
    registered_at = models.DateField(null=True)
```

---

## 10. Validation Rules

| Action | Validation |
|---|---|
| Retry failed OTPs | Only OTPs from last 1 hour. Exam must still be in progress (no retrying after exam ends). Max 1 retry per OTP. |
| Switch gateway | Cannot switch if both gateways are down. Must have backup gateway with > ₹5,000 balance. COO must confirm. |
| Pause channel | Cannot pause SMS during exam peak (`war:peak_active` flag check). |

---

## 11. Security Considerations

- Phone numbers and email addresses: stored hashed in delivery logs for analytics. Raw values only in Celery task context (not persisted after delivery). UI shows masked values (last 5 digits of phone).
- Gateway API keys: in AWS Secrets Manager. Never in NotificationLog records.
- DLT Template IDs: public (TRAI-registered), safe to display.
- Bulk retry action: rate-limited (1 retry batch per 10 minutes per user).

---

## 12. Edge Cases

| State | Behaviour |
|---|---|
| OTP success rate < 95% during exam | Auto-creates P1 incident. War Room command strip "OTP SUCCESS %" card turns red. Exam Ops Manager notified. |
| Queue depth > 2,000 | Auto-alert to Notification Manager + COO. Celery worker count auto-scaled via AWS Lambda concurrency if `auto_scale_workers=True` config flag is set. |
| SMS gateway balance < ₹10,000 | Amber alert in gateway health section. Auto-email to COO: "Exotel SMS credits low — recharge before next exam." |
| DLT template rejected mid-campaign | All pending notifications using that template ID marked "failed — DLT rejected". COO notified. Active sending paused for that template. |
| Both primary and backup SMS gateways down | Red full-page banner: "SMS GATEWAY UNAVAILABLE — OTP delivery impossible. Students cannot log in to new exams." P0 incident auto-created. |

---

## 13. Performance & Scaling

| Endpoint | Target |
|---|---|
| Summary strip | < 80ms (Redis) |
| OTP detail | < 150ms (Redis aggregation) |
| Queue monitor | < 50ms (Celery/SQS queue depth from Redis) |
| Channel chart | < 200ms |
| DLT compliance | < 100ms |
| Gateway health | < 100ms (Redis) |

- `NotificationLog` grows at ~75,000 records/peak-day. Index on `(channel, status, sent_at)` — queries always scoped to last 1h or 24h.
- OTP histogram: pre-computed by Celery beat every 30s during exam hours, stored in Redis `notif:otp:histogram:1h`. Page reads from Redis only.
- Queue depth from Redis `LLEN` command — O(1), sub-millisecond.

---

*Last updated: 2026-03-20*
