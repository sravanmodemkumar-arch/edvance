# O-02 — Parent Dashboard

> **URL:** `/coaching/parent-portal/`
> **File:** `o-02-parent-dashboard.md`
> **Priority:** P1
> **Roles:** Parent/Guardian (linked to enrolled student)

---

## 1. Parent Dashboard

```
PARENT PORTAL — Toppers Coaching Centre
Logged in as: Mr. Rajesh Kumar (Parent of Akhil Kumar — TCC-2401)
Last login: 15 March 2026

  ┌──────────────────────────────────────────────────────────────────────┐
  │  AKHIL'S PROGRESS SNAPSHOT                     [Notifications 🔔 (1)]│
  ├──────────────┬──────────────┬──────────────┬─────────────────────────┤
  │  ATTENDANCE  │  LAST TEST   │  BATCH RANK  │  FEE STATUS             │
  │   95.4%  ✅  │  186/200    │   #1 / 276   │  ₹0 due ✅              │
  │  (Mar 2026)  │  (Mock #25) │  (batch)     │  Fully paid ✅          │
  └──────────────┴──────────────┴──────────────┴─────────────────────────┘

  RECENT NOTIFICATIONS:
    30 Mar — Mock #25 completed: Score 186/200 (Rank #1) ✅
    28 Feb — Attendance this month: 95.4% (above 75% minimum) ✅
    28 Feb — February progress report available [View Report]

  SCHEDULE (Upcoming):
    Tue 1 Apr:   Quant — Data Interpretation (9:00 AM)
    Wed 2 Apr:   English — Reading Comprehension (9:00 AM)
    Sun 5 Apr:   Mock Test #26 — Full Length (9:00 AM – 12:00 PM)
    Sun 20 Apr:  Parent-Teacher Meeting (10:00 AM – 1:00 PM)

  [📩 Message Counsellor]  [📋 View Full Progress]  [📅 Upcoming Events]
```

---

## 2. Parent Progress View

```
PARENT PROGRESS VIEW — Akhil Kumar

  ATTENDANCE HISTORY (AY 2025–26):
    Month     │ Classes │ Attended │ Rate  │ Status
    ──────────┼─────────┼──────────┼───────┼────────
    Aug 2025  │   20    │   19     │ 95.0% │ ✅
    Sep 2025  │   22    │   21     │ 95.5% │ ✅
    Oct 2025  │   24    │   23     │ 95.8% │ ✅
    Nov 2025  │   22    │   21     │ 95.5% │ ✅
    Dec 2025  │   20    │   18     │ 90.0% │ ✅ (exam prep period)
    Jan 2026  │   24    │   23     │ 95.8% │ ✅
    Feb 2026  │   22    │   21     │ 95.5% │ ✅
    Mar 2026  │   24    │   23     │ 95.8% │ ✅
    ──────────┴─────────┴──────────┴───────┴────────
    YTD:       178/186 (95.7%) ✅

  SCORE PROGRESS:
    Mock #1:  124/200 (Aug 2025) → Mock #25: 186/200 (Mar 2026) | +62 pts ✅

  PARENT-TEACHER MEETING RECORD:
    Last PTM: 10 March 2026
    Feedback from faculty: "Exceptional student — consistent performance, always prepared"
    Counsellor note: "No welfare concerns — student well-adjusted and motivated"
    Next PTM: 20 April 2026

  HOSTEL (N/A — Akhil is a day scholar; hostel data not shown)
```

---

## 3. Parent Communication Preferences

```
COMMUNICATION PREFERENCES — Mr. Rajesh Kumar

  NOTIFICATION CHANNELS:
    (●) WhatsApp: +91-98765-XXXXX   ← Primary [Active ✅]
    (●) Email:    rajesh.k@email.com [Active ✅]
    (○) SMS:      +91-98765-XXXXX   [Inactive]

  NOTIFICATION TYPES:
    [✅] Attendance alert (if < 75% monthly)
    [✅] Test score notification (after each mock)
    [✅] Fee due reminder (7 days before)
    [✅] PTM date and reminders
    [  ] Class cancellation (not selected — parent preference)
    [✅] Emergency / safety alerts (always on — cannot be disabled)

  PRIVACY NOTE:
    Parent portal shows: Attendance, test scores (aggregated), fee status, schedule
    Parent portal does NOT show: Doubt session details, counselling notes, welfare aid,
                                  disciplinary records (student privacy for students ≥ 18)
    Akhil Kumar is 22 years old — full adult privacy rights apply
    Parents see only what the student has explicitly consented to share
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/parent-portal/dashboard/` | Parent dashboard for linked student |
| 2 | `GET` | `/api/v1/coaching/{id}/parent-portal/progress/` | Student progress data (scoped to parent view) |
| 3 | `GET` | `/api/v1/coaching/{id}/parent-portal/notifications/` | Parent notifications |
| 4 | `PATCH` | `/api/v1/coaching/{id}/parent-portal/preferences/` | Update communication preferences |
| 5 | `POST` | `/api/v1/coaching/{id}/parent-portal/message/` | Send message to counsellor |

---

## 5. Business Rules

- The parent portal is scoped by the student's age and consent; for students above 18 (the majority of TCC's enrollment — competitive exam aspirants are typically 20–27), the parent portal shows only what the student has agreed to share; by default, an adult student's counselling notes, welfare aid receipt, and grievance history are not visible to parents even if the parent created the account; this respects the student's right to privacy as an adult; a parent who demands to see their 24-year-old child's counselling session notes is told politely that these are private; only the student can grant access to this data
- For students below 18 (Foundation Batch — Class 10+2), the parent portal has broader access because the student is a minor and parents have parental rights over the minor's educational data; parents of minors can see attendance, scores, disciplinary records, and welfare information; however, even for minors, the POCSO provision protects disclosures made to the counsellor — a minor student's disclosure to the counsellor about abuse at home must be handled by the counsellor per POCSO protocol, not disclosed to the parent who may be the abuser; this is a nuanced but legally critical boundary
- Parent access to student data requires a verified linking process; at enrollment, the student provides the parent's mobile number; the system sends the parent a WhatsApp/SMS link to activate their parent portal account; the parent must verify their identity (OTP to their registered number); a parent who did not go through the verification process cannot access the portal with just the student's roll number; this prevents unauthorised access (e.g., an ex-spouse claiming to be the guardian without the student's knowledge)
- The parent portal notification system for fee reminders is a standard customer service feature (parents who co-fund the fee want to know about upcoming due dates); the notification is sent to the parent, not through the student; this is appropriate for the parental financial relationship; however, TCC must be careful not to send "your son/daughter failed the test" notifications to parents of adult students without the student's consent — this would be a DPDPA violation (sharing the adult student's academic performance with a third party without consent); the default is that score notifications to parents are opt-in for adult students
- Emergency and safety alerts (e.g., "class is cancelled today due to a safety incident", "there is a situation at the hostel and all parents of hostel residents are asked to contact") are always sent to parents regardless of their other notification preferences; there is no opt-out for safety alerts; this is a statutory requirement for institutions serving students who are also residents; the Branch Manager authorises safety alerts before they are sent; a false safety alert (sent in error) must be immediately corrected with a follow-up message to prevent panic

---

*Last updated: 2026-03-31 · Group 5 — Coaching Portal · Division O*
