# C-01 — Notification Feed

> **URL:** `/exam/notifications/`
> **File:** `c-01-notification-feed.md`
> **Priority:** P1
> **Data:** `notification` table — each entry is one official notification ingested from a conducting body's website

---

## 1. Notification Feed

```
EXAM NOTIFICATIONS — EduForge
All exams · Central + State · Live from official sources

  FILTER BAR:
  Type:   [All ▼]  Central  State  PSU  Banking  Defence  Teaching  Police …
  State:  [All ▼]  AP  TS  KA  TN  National …
  Event:  [All ▼]  Notification  Application  Admit Card  Result  Answer Key  Schedule
  Body:   [All ▼]  SSC  APPSC  TSPSC  IBPS  RRB  UPSC  TSLPRB  SLPRB-AP …

  FEED  [from notification ORDER BY published_at DESC, paginated]
  ┌──────────────────────────────────────────────────────────────────────┐
  │  🔴 Apr 2, 2026 — NOTIFICATION RELEASED                             │
  │  SSC CGL 2026 — Staff Selection Commission                          │
  │  Vacancies: 18,517 | Application: 2 Apr – 30 Jun 2026              │
  │  Source: ssc.nic.in ✅ verified                                      │
  │  [View at source ↗]  [Apply]  [View exam on EduForge]  [Share]      │
  │  🔔 Alerts sent to 4,28,000 subscribers                              │
  ├──────────────────────────────────────────────────────────────────────┤
  │  ✅ Mar 30, 2026 — RESULT DECLARED                                   │
  │  AP Police Constable 2025 (CBT) — SLPRB Andhra Pradesh              │
  │  Qualified: 84,240 / 6,28,000 | Next: Physical test (Apr 20)       │
  │  Source: slprb.ap.gov.in ✅ verified                                  │
  │  [View results ↗]  [Check your result]  [View exam]                  │
  ├──────────────────────────────────────────────────────────────────────┤
  │  ✅ Mar 28, 2026 — FINAL RESULT                                      │
  │  TSPSC Group 2 2025 — Telangana State PSC                           │
  │  Selected: 783 candidates | Merit list available                     │
  │  Source: tspsc.gov.in ✅ verified                                     │
  │  [View merit list ↗]  [Download PDF]  [View exam]                    │
  ├──────────────────────────────────────────────────────────────────────┤
  │  🟡 Mar 25, 2026 — APPLICATION EXTENDED                              │
  │  VRO/VRA AP 2025 — AP Revenue Department                            │
  │  New deadline: 10 April 2026 (was 31 Mar 2026)                      │
  │  Source: gramasachivalayam.ap.gov.in ✅ verified                      │
  ├──────────────────────────────────────────────────────────────────────┤
  │  📋 Mar 22, 2026 — ADMIT CARD RELEASED                              │
  │  TSPSC Group 1 Mains 2024 — Hall tickets available                  │
  │  Download from: tspsc.gov.in (login required)                        │
  │  Source: tspsc.gov.in ✅ verified                                     │
  └──────────────────────────────────────────────────────────────────────┘
  [Load older notifications...]  Page 1 of 48
```

---

## 2. Notification Data Model

```
notification {
  id,
  exam_id,                 ← FK to exam (nullable — for body-level announcements)
  conducting_body_id,      ← FK to conducting_body
  event_type,              ← notification | application_open | application_extended |
                              admit_card | exam_schedule | answer_key | result |
                              corrigendum | vacancy_revision | other
  title,
  summary,
  source_url,              ← official URL where this was published
  source_pdf_url,          ← direct link to PDF (if applicable)
  verified,                ← bool — content team confirmed from official source
  verified_by,             ← user_id of content team member
  published_at,            ← when official source published (not when EduForge ingested)
  ingested_at,             ← when EduForge system detected it
  alerts_sent_count,       ← how many users were notified
  metadata: {},            ← JSON: { vacancies, application_start, application_end, … }
}
```

---

## 3. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/exam/notifications/?type=state&state=AP&event=result&page=1` | Filtered notification feed |
| 2 | `GET` | `/api/v1/exam/notifications/{nid}/` | Single notification detail |
| 3 | `GET` | `/api/v1/exam/notifications/my/?uid={uid}` | Notifications for user's subscribed exams |

---

## 5. Business Rules

- Every notification entry must have `verified = true` before it appears in the public feed; the ingestion pipeline (C-04) detects new entries on official websites and creates notification records with `verified = false`; the content team reviews, confirms against the official source, and sets `verified = true`; the SLA is: verification within 2 hours of ingestion during business hours (8 AM – 10 PM IST); unverified notifications sit in a pending queue visible only to the content team; publishing an incorrect notification (wrong exam date, wrong vacancy count) could cause aspirants to miss deadlines or submit wrong applications — the verification step is non-negotiable
- The `event_type` field enables intelligent filtering; an aspirant who has already applied for APPSC Group 2 doesn't need "Application Open" events — they need "Admit Card" and "Result" events; the feed's event filter allows them to see only result/admit card events for their saved exams; the event types are an open enum — if a new type emerges ("Revised Answer Key" or "Re-examination Notice"), the content team can use `other` with a descriptive title until the enum is formally extended
- `source_url` is mandatory and must point to the exact official page where the notification was published; aspirants should be able to click through to the official source and verify the information themselves; a notification without a source URL is not trustworthy; the source URL also serves as the deduplication key — if the same URL is detected twice, the system does not create a duplicate notification entry
- The `metadata` JSON field captures structured data from the notification that is useful for programmatic processing; when an "Application Open" notification is ingested, the metadata includes `{ application_start, application_end }`; the system uses this to update the exam record's `application_start` and `application_end` fields automatically; when a "Result Declared" notification is ingested, the metadata includes `{ qualified_count, total_appeared }`; this auto-update mechanism keeps exam records fresh without manual edits for every notification
- Alerts sent count (4,28,000 for SSC CGL) is computed from the notification engine's delivery log; the engine sends alerts via: push notification (app), WhatsApp (if opted in), email (if opted in), and SMS (for critical events like "application deadline tomorrow"); the delivery is queued and processed asynchronously — 4 lakh+ alerts cannot be sent synchronously; the `alerts_sent_count` is updated as deliveries complete; failed deliveries are retried 3 times; permanently failed deliveries (invalid email, uninstalled app) are logged and the user's contact status is flagged for cleanup

---

*Last updated: 2026-03-31 · Group 6 — Exam Domain Portal · Division C*
