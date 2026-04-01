# A-01 — Exam Hub Landing

> **URL:** `/exam/`
> **File:** `a-01-exam-hub.md`
> **Priority:** P1
> **Data:** `exam` table · `conducting_body` table · `notification` table · `user_exam_profile` (if authenticated)

---

## 1. Hub Landing — Guest View

```
EDUFORGE EXAM HUB
One platform for every competitive exam — Central · State · PSU · Banking · Teaching · Defence · and more
Language: [English ▼]  [తెలుగు ▼]  [हिंदी ▼]  [தமிழ் ▼]

  ┌──────────────────────────────────────────────────────────────────────┐
  │  🔍 FIND YOUR EXAM                                                   │
  │  [Search exam name, post, conducting body, state...      ] [Search] │
  │                                                                      │
  │  Filters:                                                            │
  │  Type:    [All ▼]  Central  State  PSU  Banking  Teaching  Defence  │
  │  State:   [All ▼]  Andhra Pradesh  Telangana  Karnataka  Tamil Nadu…│
  │  Qualify: [All ▼]  10th  12th  Graduate  PG  Diploma  B.Ed  Any    │
  │  Age:     [All ▼]  18–25  18–30  18–32  18–35  No limit            │
  └──────────────────────────────────────────────────────────────────────┘

  BROWSE BY TYPE  [rendered from distinct exam.type values in DB]
  ┌──────────┬──────────┬──────────┬──────────┬──────────┬──────────┐
  │  Central │  State   │  PSU     │  Banking │  Teaching│  Defence │
  │  32 exams│  48 exams│  18 exams│  14 exams│  12 exams│  9 exams │
  ├──────────┼──────────┼──────────┼──────────┼──────────┼──────────┤
  │ Railway  │Insurance │University│Municipal │ Police   │ Revenue  │
  │ 8 exams  │ 6 exams  │ 22 exams │ 5 exams  │ 16 exams │ 8 exams  │
  └──────────┴──────────┴──────────┴──────────┴──────────┴──────────┘
  (counts are live from DB — update automatically as exams are added)

  BROWSE BY STATE  [rendered from distinct exam.state_code values in DB]
    🇮🇳 National/Central  │  AP  Andhra Pradesh  │  TS  Telangana
    KA  Karnataka         │  TN  Tamil Nadu      │  MH  Maharashtra
    RJ  Rajasthan         │  UP  Uttar Pradesh   │  + any state admin adds

  LIVE NOTIFICATIONS (latest 5 — from notification engine)
  ┌──────────────────────────────────────────────────────────────────────┐
  │  🔴 SSC CGL 2026 — Notification released 2 Apr 2026 [Apply Now]    │
  │  ✅ TSPSC Group 2 2025 — Final results declared 28 Mar 2026         │
  │  🟡 APPSC Group 1 — Mains result expected May 2026 [Set Alert]     │
  │  🔴 IBPS PO 2026 — Notification expected Jun 2026 [Set Alert]      │
  │  ✅ AP Police SI 2025 — CBT results published 30 Mar 2026           │
  │                                      [View all notifications →]     │
  └──────────────────────────────────────────────────────────────────────┘
```

---

## 2. Hub Landing — Authenticated View

```
EXAM HUB — Welcome back, Ravi Kumar
Profile: Graduate · Age 24 · OBC · Domicile: Andhra Pradesh · Language: Telugu

  MY ACTIVE EXAMS  [from user_exam_profile + exam table]
  ┌───────────────────────────────────────┬────────────────────────────────┐
  │  APPSC Group 2 2025                   │  SSC CGL 2026                  │
  │  Conducting: APPSC | State: AP        │  Conducting: SSC | Central     │
  │  Status: Application submitted ✅     │  Status: Notification released  │
  │  Exam date: Aug 2026 (tentative)      │  Apply by: 30 Jun 2026         │
  │  Mock avg: 124/200  Rank: 4,820       │  Mock avg: 138/200  Rank: 2,14k│
  │  Syllabus coverage: 68% ✅           │  Syllabus coverage: 45% 🟡     │
  │  [Continue Prep →]                    │  [Continue Prep →]             │
  └───────────────────────────────────────┴────────────────────────────────┘

  RECOMMENDED FOR YOU  [eligibility engine — matches profile to open exams]
  ┌──────────────────────────────────────────────────────────────────────┐
  │  ✨ VRO/VRA AP 2025 — Application open till Apr 10 — You're eligible │
  │  ✨ TSPSC Group 3 2026 — Notification expected. Profile matches ✅   │
  │  ✨ IBPS Clerk 2026 — Graduate eligible. Mock bank ready              │
  │                                     [View all eligible exams →]      │
  └──────────────────────────────────────────────────────────────────────┘

  YOUR UPCOMING DATES
    Apr 5:   SSC CGL mock #26 (scheduled by Toppers CC)
    Apr 10:  VRO/VRA AP — application deadline ⚠️
    Jun 30:  SSC CGL 2026 application last date
    Aug 2026: APPSC Group 2 CBT (tentative)
```

---

## 3. Search Results — Dynamic Rendering

```
SEARCH RESULTS — "group 2"
Showing 8 exams matching "group 2"  [rendered from exam table WHERE name ILIKE '%group 2%']

  ┌─────────────────────────────────────────────────────────────────────┐
  │  APPSC Group 2 2025                              [STATE — AP]        │
  │  Andhra Pradesh Public Service Commission                           │
  │  Qualification: Graduate | Age: 18–42 | Medium: Telugu / English    │
  │  Posts: Junior Assistant, Surveyor, Revenue Inspector, 60+ posts    │
  │  Vacancies: 897 | Notification: Oct 2025 | Exam: Aug 2026           │
  │  Mocks available: 28 | Aspirants: 4,28,000                          │
  │  [View Exam →]  [Take Mock →]  [Save to My Exams]                  │
  ├─────────────────────────────────────────────────────────────────────┤
  │  TSPSC Group 2 2026                              [STATE — TS]        │
  │  Telangana State Public Service Commission                          │
  │  Qualification: Graduate | Age: 18–44 | Medium: Telugu / English    │
  │  Posts: Junior Assistant, Village Revenue Officer, 50+ posts        │
  │  Vacancies: 783 (expected) | Notification: Sep 2026 (tentative)     │
  │  Mocks available: 22 | Aspirants: 3,92,000                          │
  │  [View Exam →]  [Take Mock →]  [Save to My Exams]                  │
  ├─────────────────────────────────────────────────────────────────────┤
  │  KPSC Group B 2025                               [STATE — KA]        │
  │  Karnataka Public Service Commission                                │
  │  …                                                                  │
  └─────────────────────────────────────────────────────────────────────┘

  FILTER (live):  [AP ✕] [Graduate ✕]   Sort by: [Relevance ▼]
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/exam/hub/` | Hub data — notifications, types, state list, counts (guest + auth) |
| 2 | `GET` | `/api/v1/exam/hub/search/?q=group+2&type=state&state=AP&qual=graduate` | Full-text + filtered exam search |
| 3 | `GET` | `/api/v1/exam/hub/categories/` | Exam type counts — rendered dynamically from DB |
| 4 | `GET` | `/api/v1/exam/hub/states/` | State list — from distinct state_code values in DB |
| 5 | `GET` | `/api/v1/exam/hub/recommended/?uid={uid}` | Eligibility-matched recommendations for logged-in user |
| 6 | `GET` | `/api/v1/exam/hub/live-alerts/?limit=5` | Latest 5 notifications across all exams |

---

## 5. Business Rules

- Search is full-text across `exam.name_en`, `exam.name_regional`, `conducting_body.name`, `exam.tags[]`, and `post_names[]`; a user searching "VRO" finds "Village Revenue Officer" exams even if "VRO" is only in the tags; a user searching "గ్రూప్ 2" (Telugu) finds APPSC/TSPSC Group 2 exams because `name_regional` is indexed; the search engine must support bilingual queries — a Telugu-language user should not need to type in English to find their exam
- The "type" browse grid (Central: 32 exams, State: 48 exams …) is computed live from the DB using `COUNT(*)` grouped by `exam.type` WHERE `active = true`; when an admin adds a new exam of type `municipal`, the "Municipal" tile count increments automatically without any UI change; new exam types that don't exist yet are surfaced once the first exam of that type is added — the frontend renders the type list from a DB query, not a hardcoded list
- State filter populates from `DISTINCT exam.state_code WHERE active = true ORDER BY aspirant_count DESC`; states with many exams and many aspirants appear first (AP, TS, KA, TN, MH typically); a new state exam added by admin automatically adds that state to the filter; the state list is never hardcoded — removing it from the filter would require removing all exams of that state from the DB
- Authenticated user's "Recommended" list is computed by the eligibility engine (D-01) in real time: it queries all active exams, runs each against the user's profile (age, qualification, category, domicile), filters to eligible exams where `application_end > today OR notification_date < today + 90 days`, sorts by `days_to_application_deadline ASC`, and returns the top 5; this means a user who turns 25 tomorrow automatically becomes eligible for exams with `age_min = 25` in tomorrow's recommendations
- All exam counts, notification statuses, and dates shown on the hub are cached at the CDN layer for 5 minutes for anonymous users (high traffic, low personalisation need) and fetched fresh for authenticated users (personalisation requires current data); the 5-minute CDN cache is invalidated immediately when the notification engine publishes a new notification so that breaking news (SSC notification released) reaches anonymous users within 5 minutes, not 5 minutes after the next cache cycle

---

*Last updated: 2026-03-31 · Group 6 — Exam Domain Portal · Division A*
