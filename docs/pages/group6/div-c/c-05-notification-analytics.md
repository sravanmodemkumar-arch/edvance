# C-05 — Notification Analytics

> **URL:** `/admin/exam/notifications/analytics/`
> **File:** `c-05-notification-analytics.md`
> **Priority:** P2
> **Data:** `notification` + `notification_delivery` + `monitoring_log` — admin-only analytics

---

## 1. Notification Performance

```
NOTIFICATION ANALYTICS — March 2026
EduForge Exam Portal | Content Team Dashboard

  SUMMARY:
    Notifications published:    42
    Total alerts delivered:     48,40,000 (across all channels)
    Avg time: detection → publish: 1 hr 24 min (target: < 2 hrs) ✅
    Avg time: official → detection: 38 min (target: < 1 hr) ✅
    False positives suppressed: 18 (content team caught before publish)
    Missed notifications:       0 ✅ (detected all known official publications)

  BY EVENT TYPE:
    Event Type          │ Count │ Avg alerts per event │ Engagement (click rate)
    ────────────────────┼───────┼──────────────────────┼──────────────────────
    Notification released│   8  │  2,84,000            │  42.6%
    Application open     │   6  │  1,28,000            │  38.4%
    Result declared      │   4  │  4,82,000            │  68.2%  ← highest
    Admit card           │   6  │  1,64,000            │  54.8%
    Answer key           │   4  │    96,000            │  32.4%
    Application extended │   3  │  1,42,000            │  28.6%
    Exam schedule        │   5  │    84,000            │  22.8%
    Other                │   6  │    48,000            │  18.2%

  BY CHANNEL PERFORMANCE:
    Channel     │ Delivered │ Read/Open │ CTR   │ Failures
    ────────────┼───────────┼───────────┼───────┼──────────
    Push (app)  │ 22,40,000 │ 14,28,000 │ 63.8% │  1.2%
    WhatsApp    │ 18,60,000 │ 12,42,000 │ 66.8% │  0.4%
    Email       │  6,20,000 │  1,86,000 │ 30.0% │  2.8%
    SMS         │  1,20,000 │    N/A    │  N/A  │  0.2%
```

---

## 2. Source Health

```
SOURCE HEALTH — March 2026

  Source Status Distribution:
    Active & healthy:       78 (92.9%)
    Slow (response > 10s):   4 ( 4.8%)
    Unreachable:             2 ( 2.4%)

  Detection Accuracy:
    True positives:         42 (published notifications)
    False positives:        18 (suppressed by content team — page layout changes)
    False negatives:         0 (no missed notifications known)
    Precision:              70% (42 / 60 detections were real) — improve selectors
    Recall:                100% (all known publications detected) ✅

  IMPROVEMENT ACTIONS:
    → Upgrade 4 sources from page_hash to dom_selector (reduce false positives)
    → Fix RRB Secunderabad URL (moved to new domain: rrbsecunderabad.nic.in)
    → Add monitoring for HMRL (Hyderabad Metro) — new conducting body added
```

---

## 3. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/admin/exam/notifications/analytics/?month=2026-03` | Monthly notification analytics |
| 2 | `GET` | `/api/v1/admin/exam/monitoring/health/` | Source health summary |
| 3 | `GET` | `/api/v1/admin/exam/notifications/analytics/channels/` | Channel-wise delivery analytics |

---

## 5. Business Rules

- Detection-to-publish SLA (1 hr 24 min avg, target < 2 hrs) is the content team's most important KPI; the clock starts when the monitoring engine detects a change and stops when the verified notification appears in the public feed; reducing this time directly increases EduForge's competitive advantage — if EduForge publishes 30 minutes before competing platforms, the aspirant who receives the EduForge alert first develops a habit of relying on EduForge; during peak periods (SSC notification months), the content team extends working hours to ensure coverage
- Result declaration notifications have the highest engagement rate (68.2% click-through) because result day is the most emotionally charged moment in an aspirant's preparation journey; EduForge must ensure result-day infrastructure can handle the traffic spike — when TSPSC Group 2 results are declared and 3.92 lakh subscribers receive alerts, the subsequent traffic to EduForge's result page spikes 20–50× normal; CDN caching, database read replicas, and queue-based alert delivery are essential for result-day resilience
- False positive rate of 30% (18 false detections out of 60 total) indicates that the `page_hash` method is too sensitive for many government websites; the content team must systematically upgrade these sources to `dom_selector` monitoring which targets only the notification-relevant section of the page; a source that triggers false positives wastes content team time (each false positive requires a manual review and dismissal) and delays verification of real notifications
- Channel comparison shows WhatsApp has the highest engagement (66.8% read rate) but email has the broadest reach for aspirants who don't use the app; the optimal channel strategy is: push + WhatsApp for real-time alerts (immediate, high engagement), email for weekly digests and application-related documents (receipts, admit card links), SMS only for critical events (exam cancelled, deadline tomorrow) where the aspirant may not have internet access; SMS is the most expensive channel and the least trackable — it should be reserved for high-urgency, low-frequency events
- The "missed notifications: 0" metric is the most important quality indicator; a single missed notification (APPSC releases a notification and EduForge doesn't detect it for 48 hours) damages trust more than 18 false positives combined; false positives are invisible to aspirants (they are caught internally); missed notifications are visible to anyone who follows the official source directly; the content team must cross-verify against manual checks of top 20 conducting bodies' websites every morning, independent of the automated monitoring

---

*Last updated: 2026-03-31 · Group 6 — Exam Domain Portal · Division C*
