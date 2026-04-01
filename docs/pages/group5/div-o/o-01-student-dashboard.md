# O-01 — Student Dashboard

> **URL:** `/coaching/student-portal/`
> **File:** `o-01-student-dashboard.md`
> **Priority:** P1
> **Roles:** Student (self) — authenticated view

---

## 1. Student Dashboard

```
STUDENT PORTAL — Toppers Coaching Centre
Welcome, Akhil Kumar (TCC-2401) | SSC CGL Morning Batch 2025–26
Last login: 31 March 2026, 9:14 AM

  ┌──────────────────────────────────────────────────────────────────────┐
  │  MY OVERVIEW                                  [Notifications 🔔 (2)] │
  ├──────────────┬──────────────┬──────────────┬─────────────────────────┤
  │  ATTENDANCE  │  RANK        │  NEXT TEST   │  PENDING                │
  │  95.4%  ✅   │  #1 / 1,183  │  Mock #26    │  Rank Certificate ✅    │
  │  (281/294)   │  (last mock) │  Apr 5, 2026 │  (processing)           │
  │              │  Score: 186  │  Countdown:  │  Feedback survey ⏳     │
  │              │  /200        │  5 days      │  (due Apr 5)            │
  └──────────────┴──────────────┴──────────────┴─────────────────────────┘

  QUICK ACTIONS:
    [📝 Submit Doubt]   [📊 View Results]   [📅 Schedule]   [📜 Certificates]
    [💬 Contact Counsellor]   [💳 Fee Status]   [📚 Study Material]

  RECENT ACTIVITY:
    31 Mar — Attended: Quant — Caselet DI Practice (Suresh K.) ✅
    30 Mar — Mock #25 result: 186/200 | Rank #1 | 99.6%ile ✅
    29 Mar — Doubt answered: "Pipe & Cistern Q#48" — 4.5/5 rating ✅
    28 Mar — Fee receipt: ₹0 due (fully paid) ✅
```

---

## 2. Academic Progress

```
ACADEMIC PROGRESS — Akhil Kumar (TCC-2401)

  MOCK TEST HISTORY (last 5):
    Mock # │ Date      │ Score  │ Rank (batch) │ %ile  │ vs Previous
    ───────┼───────────┼────────┼──────────────┼───────┼────────────
    Mock 21│ 25 Jan 26 │ 178/200│    #1        │ 99.4% │  —
    Mock 22│ 8 Feb 26  │ 180/200│    #1        │ 99.5% │  +2 pts
    Mock 23│ 22 Feb 26 │ 182/200│    #1        │ 99.5% │  +2 pts
    Mock 24│ 8 Mar 26  │ 184/200│    #1        │ 99.6% │  +2 pts
    Mock 25│ 30 Mar 26 │ 186/200│    #1        │ 99.6% │  +2 pts ↑

  SUBJECT-WISE (Mock #25):
    Quantitative:  48/50 (96%)  ✅ Strongest
    English:       49/50 (98%)  ✅
    Reasoning:     46/50 (92%)  ✅
    General Aware: 43/50 (86%)  🟡 (room to improve)

  IMPROVEMENT JOURNEY:
    Mock #1 (Aug 2025): 124/200 (Rank #94)
    Mock #25 (Mar 2026): 186/200 (Rank #1)
    Total gain: +62 points | Rank gain: +93 positions ✅

  DOUBTS SUBMITTED (AY):
    Total: 28 | Answered: 27 | Pending: 1 | Avg rating given: 4.3/5
```

---

## 3. Fee & Certificate Status

```
FEE STATUS — Akhil Kumar (TCC-2401)

  Course fee:       ₹32,000 (SSC CGL Morning — full payment)
  Paid:             ₹32,000 ✅ (Aug 2025 — single payment)
  Balance due:      ₹0 ✅
  Next instalment:  N/A (fully paid)

  RECEIPT HISTORY:
    TCC-RCP-2025-0342: ₹32,000 | Aug 12, 2025 | UPI ✅

CERTIFICATE STATUS:
  Enrollment Certificate:    ✅ Available (issued Aug 2025) [Download]
  Rank Certificate (#25):    ⏳ Processing (requested 30 Mar — due Apr 1) [Status]
  Course Completion:         📅 Available at batch end (Jun 2026)
  Digital ID Card:           ✅ [View Digital ID]
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/student-portal/dashboard/` | Student dashboard data |
| 2 | `GET` | `/api/v1/coaching/{id}/student-portal/progress/` | Academic progress and mock history |
| 3 | `GET` | `/api/v1/coaching/{id}/student-portal/fees/` | Fee status and receipts |
| 4 | `GET` | `/api/v1/coaching/{id}/student-portal/certificates/` | Available certificates |
| 5 | `GET` | `/api/v1/coaching/{id}/student-portal/schedule/` | Upcoming classes and tests |
| 6 | `POST` | `/api/v1/coaching/{id}/student-portal/doubts/` | Submit a doubt |

---

## 5. Business Rules

- The student dashboard is the student's single interface with TCC's digital ecosystem; it aggregates attendance, scores, fee status, study material, doubt submission, and certificate access in one view; the design principle is "zero friction for common tasks" — submitting a doubt, viewing a result, or downloading a certificate should each take < 3 taps; a student who has to navigate through multiple menus to find their attendance data will call the front desk instead, creating avoidable staff workload; the dashboard is designed for the 18–26 age group who are comfortable with digital-first experiences
- Student data shown in the dashboard is personalised and private; Akhil Kumar sees only his own data; he cannot see Priya Reddy's attendance or Mohammed R.'s fee status; the API endpoints are scoped to the authenticated student's ID — the `student-portal` endpoints require the student's JWT token and return only that student's data; the API must not accept a different student ID as a path parameter unless the requesting user has counsellor or admin roles; insecure direct object reference (IDOR) is a critical API vulnerability that must be prevented
- Rank display (Rank #1 / 1,183 students) is visible to the student and motivates continued performance; however, the dashboard does not show other students' names or scores; the student sees their rank number and percentile but not a leaderboard with peers' names; the top-performers leaderboard (E-04 test result processing) is anonymised for display in common areas; publishing named rankings where every student can see every other student's score creates unhealthy comparison and potential harassment; TCC publishes only the student's own position in the cohort
- The dashboard shows a "Pending" section for time-sensitive action items; the two pending items for Akhil Kumar (rank certificate processing and feedback survey due Apr 5) are surfaced prominently because TCC needs his survey response and he is waiting for his certificate; this "what requires my attention right now" framing is more effective than a comprehensive notification inbox; items that are not time-sensitive (an old announcement) are not shown in the "pending" section — they are in the notifications archive; dashboard design prioritises action over information
- Students access the portal with their TCC-issued credentials (mobile number + OTP, or username + password); the portal uses HTTPS; OTP-based login (via registered mobile) is the primary method to avoid password reset friction for young, mobile-first users; if a student's registered mobile changes, they must notify the front desk or update via the student profile (O-03) with verification; a student who cannot access their portal (phone lost or number changed) is verified in person at the reception before credentials are reset; this prevents credential hijacking

---

*Last updated: 2026-03-31 · Group 5 — Coaching Portal · Division O*
