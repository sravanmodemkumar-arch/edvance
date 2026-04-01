# C-04 — Source Monitoring Engine (Admin)

> **URL:** `/admin/exam/monitoring/`
> **File:** `c-04-source-monitoring.md`
> **Priority:** P1
> **Data:** `notification_source` + `monitoring_log` — admin-only; the system that watches official websites

---

## 1. Monitoring Dashboard (Admin)

```
SOURCE MONITORING ENGINE — Admin Panel
EduForge Content Team | 84 sources monitored | Last sweep: 31 Mar 2026, 6:00 AM

  STATUS:  ✅ 78 sources OK  |  🟡 4 sources slow  |  ❌ 2 sources unreachable

  SOURCE LIST  [from notification_source ORDER BY last_checked DESC]
  ┌───────────────────────────────────────────────────────────────────────────────┐
  │  Source             │ URL                        │ Check Freq │ Last Check│ St│
  ├─────────────────────┼────────────────────────────┼────────────┼───────────┼───┤
  │  SSC (Notifications)│ ssc.nic.in/noticeboards    │ Every 30min│ 6:00 AM  │ ✅│
  │  APPSC (Updates)    │ psc.ap.gov.in/Updates      │ Every 1hr  │ 5:58 AM  │ ✅│
  │  TSPSC (Notif.)     │ tspsc.gov.in/notification  │ Every 1hr  │ 5:55 AM  │ ✅│
  │  IBPS (Notifications│ ibps.in/recent-notifications│ Every 1hr  │ 5:50 AM  │ ✅│
  │  AP Police (SLPRB)  │ slprb.ap.gov.in/notifications│ Every 2hr│ 5:30 AM  │ 🟡│
  │  TS Police (TSLPRB) │ tslprb.telangana.gov.in    │ Every 2hr  │ 5:28 AM  │ ✅│
  │  RRB Secunderabad   │ rrbsecunderabad.gov.in     │ Every 2hr  │ 5:15 AM  │ ❌│
  │  UPSC               │ upsc.gov.in                │ Every 1hr  │ 6:00 AM  │ ✅│
  │  [+ 76 more sources]│                            │            │          │   │
  └───────────────────────────────────────────────────────────────────────────────┘

  DETECTION QUEUE (unverified — awaiting content team review):
    1. SSC CGL 2026 — new PDF detected on ssc.nic.in — 5 min ago ⏳ VERIFY
    2. ONGC recruitment — new page on ongcindia.com — 2 hrs ago ⏳ VERIFY
    3. RRB page change detected — rrbsecunderabad.gov.in — unreachable ❌ SKIP

  RECENT VERIFIED (last 24 hrs):
    ✅ AP Police Constable result — verified by Priya M. at 10:30 AM ✅
    ✅ TSPSC Group 2 final result — verified by Rajan K. at 9:15 AM ✅
```

---

## 2. Source Monitoring Mechanism

```
HOW MONITORING WORKS

  notification_source {
    id,
    conducting_body_id,
    url,                    ← the specific page to monitor
    check_frequency_min,    ← 30, 60, 120 minutes
    detection_method,       ← "page_hash" | "rss" | "new_links" | "pdf_count" | "dom_selector"
    selector (nullable),    ← CSS selector for dynamic sites (e.g., "table.notifications tr")
    last_hash,              ← SHA-256 of last fetched content
    last_checked_at,
    last_change_detected_at,
    status,                 ← "active" | "slow" | "unreachable" | "paused"
    failures_consecutive,   ← count of consecutive fetch failures
  }

  DETECTION METHODS:
    page_hash:   Fetch page → compute SHA-256 → compare with last_hash
                 If different → "change detected" → queue for review
    rss:         Parse RSS feed → check for new <item> entries
    new_links:   Scan page for <a href> → find links not seen before
    pdf_count:   Count PDF links on page → if count increased → new notification
    dom_selector:Extract specific DOM section → hash that section only
                 (for pages with dynamic ads/timestamps that cause false positives)

  FLOW:
    Scheduler (cron) → Fetch each source at its frequency
    → Compare content with last snapshot
    → If change detected → create notification (verified=false) + alert content team
    → Content team reviews → sets verified=true + enriches metadata
    → Notification appears in public feed + alerts sent to subscribers
```

---

## 3. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/admin/exam/monitoring/sources/` | All monitored sources with status |
| 2 | `POST` | `/api/v1/admin/exam/monitoring/sources/` | Add new monitoring source |
| 3 | `GET` | `/api/v1/admin/exam/monitoring/queue/` | Unverified detection queue |
| 4 | `PATCH` | `/api/v1/admin/exam/monitoring/queue/{id}/verify/` | Verify and publish a detection |
| 5 | `GET` | `/api/v1/admin/exam/monitoring/log/` | Monitoring run log |

---

## 5. Business Rules

- The monitoring engine is EduForge's core competitive advantage for the exam portal; an aspirant who receives an SSC CGL notification alert 30 minutes after SSC publishes it (vs discovering it 2 days later on social media) trusts EduForge as their primary exam information source; the 30-minute monitoring frequency for SSC and other high-traffic bodies is the SLA; reducing this to 15 minutes for peak notification periods (March–April for SSC, October for APPSC) would further strengthen this advantage
- Government websites (ssc.nic.in, tspsc.gov.in, psc.ap.gov.in) are notoriously unreliable — they go down during result declarations, have inconsistent HTML structure, and sometimes publish notifications as image PDFs instead of HTML; the monitoring engine must handle: connection timeouts (retry 3 times with exponential backoff), SSL certificate issues (some .gov.in sites have expired certs — fetch with relaxed verification but log the issue), and content served as images (use OCR for PDF detection but rely on human verification for content extraction)
- False positive management is critical; government websites change their page layout, add new ads, or update copyright year footers — all of which change the page hash without a new notification being published; the `dom_selector` detection method addresses this by monitoring only the notification-specific section of the page (e.g., "table.notifications tr"); the content team tunes selectors per source; a new source starts with `page_hash` and is upgraded to `dom_selector` after the first false positive
- Source failures (❌ unreachable) trigger an escalation: 1 failure → auto-retry in 10 minutes; 3 consecutive failures → alert content team lead; 10 consecutive failures → source marked as "unreachable" and removed from monitoring cycle until manually reactivated; government websites occasionally go offline for maintenance or get moved to new domains; when RRB Secunderabad's website is unreachable, the content team checks if the URL has changed (common in government website redesigns) and updates the `notification_source.url` if needed
- Adding a new monitoring source is part of the new conducting body onboarding process; when a content admin adds a new conducting body (A-03), they also add at least one `notification_source` for that body's official notification page; a conducting body without a monitored source will never generate automatic notifications — all notifications would have to be manually entered; the goal is 100% of active conducting bodies having at least one monitored source; currently 78 of 84 bodies have active monitoring (93%)

---

*Last updated: 2026-03-31 · Group 6 — Exam Domain Portal · Division C*
