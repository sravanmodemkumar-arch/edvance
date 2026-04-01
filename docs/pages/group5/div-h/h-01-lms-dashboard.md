# H-01 — LMS Dashboard

> **URL:** `/coaching/online/lms/`
> **File:** `h-01-lms-dashboard.md`
> **Priority:** P1
> **Roles:** Online Coordinator (K4) · Academic Director (K5) · Branch Manager (K6)

---

## 1. LMS Overview

```
LMS DASHBOARD — Toppers Coaching Centre
As of 30 March 2026  |  Online Coordinator: Mr. Aditya Menon

  ┌──────────────────────────────────────────────────────────────────────────────┐
  │  ONLINE STUDENTS: 1,284  │  ACTIVE TODAY: 486  │  CONTENT ITEMS: 2,842     │
  │  Live sessions this week: 36  │  Recordings viewed (Mar): 14,840           │
  └──────────────────────────────────────────────────────────────────────────────┘

  ONLINE BATCH STATUS:
    Batch                    │ Enrolled │ Active Today │ Live Now      │ Status
    ─────────────────────────┼──────────┼─────────────-┼───────────────┼──────────────
    SSC CGL Online (May 26)  │   392    │    186       │ No (7 PM eve) │ ✅ Active
    SSC CGL Live Online 2026 │   186    │     88       │ No (7 PM eve) │ ✅ Active
    Banking Online (May 26)  │   280    │    124       │ No (7 PM eve) │ ✅ Active
    RRB Online               │   180    │     52       │ No            │ ✅ Active
    Foundation Online        │   120    │     36       │ No            │ ✅ Active
    Test Series Only         │   126    │     —        │ No test today │ ✅ Active

  CONTENT HEALTH:
    Total content items:      2,842
    Videos (recorded):        1,240
    PDFs / Study material:      824
    Question bank (active):     624  (shareable via tests)
    Other (notes, diagrams):    154

  STORAGE USED:  2.84 TB / 5 TB  (56.8%) ✅ Healthy
```

---

## 2. Today's Online Schedule

```
TODAY'S ONLINE SCHEDULE — 30 March 2026

  Time        │ Batch                    │ Session Type    │ Faculty         │ Status
  ────────────┼──────────────────────────┼─────────────────┼─────────────────┼──────────────
  7:00–8:00 PM│ SSC CGL Live Online      │ Quant (live)    │ Mr. Suresh K.   │ ⏳ Upcoming
  7:00–8:00 PM│ Banking Online           │ Reasoning (live)│ Mr. Mohan R.    │ ⏳ Upcoming
  8:00–9:00 PM│ SSC CGL Live Online      │ Reasoning (live)│ Mr. Mohan R.    │ ⏳ Upcoming
  8:00–9:00 PM│ Banking Online           │ Quant (live)    │ Mr. Suresh K.   │ ⏳ Upcoming
  9:00–10:00PM│ RRB Online               │ GK/CA (live)    │ Mr. Ravi S.     │ ⏳ Upcoming
  All day     │ All online batches       │ Recorded access │ Self-paced      │ ✅ Always on

  REMINDERS SENT:
    6:30 PM push notification: "Live class in 30 min — SSC CGL & Banking" ✅
    6:45 PM SMS reminder: Sent to opted-in students ✅
```

---

## 3. Platform Health

```
LMS PLATFORM HEALTH — 30 March 2026, 11:40 AM

  UPTIME (last 30 days):     99.7%  (2.2 hours downtime — Apr 12 maintenance)
  RESPONSE TIME (avg):        280 ms  ✅ (target: < 500 ms)
  CDN STATUS:                 ✅ All nodes active (Mumbai, Hyderabad, Chennai)
  ZOOM INTEGRATION:           ✅ Active

  ACTIVE SESSIONS NOW:
    Students logged in:    486
    Videos being streamed: 142  (peak: 8:00–10:00 PM)
    Tests in progress:       0  (no test scheduled now)

  LAST INCIDENTS:
    29 Mar 11:20 PM: Video buffering — 38 students reported — CDN cache miss
    Resolved: 11:42 PM (22 min) | Cause: Large file (3.2 GB video) cache miss
    Action: Pre-warm cache before heavy content updates ✅

  SUPPORT TICKETS OPEN: 6 (see H-08 Technical Support)
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/online/lms/dashboard/` | Full LMS dashboard data |
| 2 | `GET` | `/api/v1/coaching/{id}/online/lms/batches/` | Online batch summary |
| 3 | `GET` | `/api/v1/coaching/{id}/online/lms/schedule/?date=2026-03-30` | Today's online session schedule |
| 4 | `GET` | `/api/v1/coaching/{id}/online/lms/health/` | Platform uptime and performance metrics |
| 5 | `GET` | `/api/v1/coaching/{id}/online/lms/content/stats/` | Content library stats by type |

---

## 5. Business Rules

- The LMS is the primary interface for all online students; it must maintain 99.5%+ uptime during peak hours (7 PM–10 PM on weekdays); planned maintenance must be scheduled between 2 AM–5 AM and communicated to students 24 hours in advance; an unexpected outage during live class hours triggers the Online Coordinator to immediately post an outage notice on the batch WhatsApp group and the students' notifications; the make-up session for an outage is mandatory within 48 hours
- Content storage management (currently 2.84 TB / 5 TB) is reviewed monthly; videos older than 2 years with fewer than 10 views in the last 6 months are candidates for archival (moved to cold storage, not deleted); archived content is retrievable within 24 hours if needed; the Online Coordinator reviews the archival list with the Academic Director before proceeding; content is never permanently deleted without Academic Director sign-off, as even old recordings may be referenced by current students
- The LMS must be accessible on mobile (Android, iOS) and low-bandwidth conditions; TCC's student base includes students in areas with 2G–4G connectivity; videos must offer multiple quality settings (240p, 360p, 480p, 720p); a student who cannot access content due to bandwidth limitations must have a path to download low-quality offline versions (available for 7 days per download); this accessibility commitment is part of TCC's online product proposition and is communicated in the online batch enrollment
- CDN (Content Delivery Network) is used for all video delivery; videos must not be served directly from the origin server; the CDN ensures fast delivery regardless of the student's location (Hyderabad, Bengaluru, Mumbai, Tier-3 towns); the CDN also serves as a security layer — direct access to the origin storage is blocked; all video URLs are signed (expire after 4 hours) to prevent link sharing and unauthorised access
- Online student engagement data (login frequency, content consumption, test performance) feeds the Academic Director's dashboard; a student who hasn't logged in for 7 consecutive days triggers a "silent disengagement" alert; the Online Coordinator follows up via WhatsApp; online students who disengage are harder to re-engage than offline students (no physical presence reminder); the 7-day alert is designed to catch early disengagement before it becomes dropout

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division H*
