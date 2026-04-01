# C-02 — Unified Exam Calendar

> **URL:** `/exam/calendar/`
> **File:** `c-02-unified-calendar.md`
> **Priority:** P1
> **Data:** Computed from `exam.application_start/end`, `exam.exam_dates[]`, `exam.result_dates[]` — all exams, all states

---

## 1. Calendar View

```
UNIFIED EXAM CALENDAR — EduForge
All exams · All states · April 2026

  VIEW: [Month ▼]  [Week]  [List]  [Timeline]
  FILTER: [All ▼] State: [AP ✕] [TS ✕]  Type: [All ▼]  My Exams Only: [○]

  ┌────────┬────────┬────────┬────────┬────────┬────────┬────────┐
  │  Mon   │  Tue   │  Wed   │  Thu   │  Fri   │  Sat   │  Sun   │
  ├────────┼────────┼────────┼────────┼────────┼────────┼────────┤
  │   1    │   2    │   3    │   4    │   5    │   6    │   7    │
  │        │🔴 SSC  │        │        │ Mock   │        │        │
  │        │CGL app │        │        │ SSC #1 │        │        │
  │        │opens   │        │        │        │        │        │
  ├────────┼────────┼────────┼────────┼────────┼────────┼────────┤
  │   8    │   9    │  10    │  11    │  12    │  13    │  14    │
  │        │        │⏰VRO/  │        │        │        │        │
  │        │        │VRA AP  │        │        │        │        │
  │        │        │last day│        │        │        │        │
  ├────────┼────────┼────────┼────────┼────────┼────────┼────────┤
  │  15    │  16    │  17    │  18    │  19    │  20    │  21    │
  │🟡TS    │        │        │        │        │AP Police│        │
  │Police  │        │        │        │        │Physical │        │
  │app last│        │        │        │        │test day │        │
  ├────────┼────────┼────────┼────────┼────────┼────────┼────────┤
  │  22    │  23    │  24    │  25    │  26    │  27    │  28    │
  │        │        │        │📋TSPSC │        │        │        │
  │        │        │        │Gr 1    │        │        │        │
  │        │        │        │Mains D1│        │        │        │
  ├────────┼────────┼────────┼────────┼────────┼────────┼────────┤
  │  29    │  30    │                                             │
  │        │🔴TDS  │  ← system events (compliance) shown if admin│
  └────────┴────────┘
```

---

## 2. List View (Dense)

```
LIST VIEW — April 2026 (filtered: AP + TS + Central)

  Date        │ Exam                          │ Event                    │ Type    │ State
  ────────────┼───────────────────────────────┼──────────────────────────┼─────────┼──────
  Apr 2       │ SSC CGL 2026                  │ Application opens        │ Central │ 🇮🇳
  Apr 5       │ SSC CGL Mock #1 (EduForge)    │ Platform mock test       │ Central │ 🇮🇳
  Apr 10      │ VRO/VRA AP 2025               │ Application deadline ⚠️  │ State   │ AP
  Apr 15      │ TS Police Constable 2025      │ Application deadline     │ Police  │ TS
  Apr 20      │ AP Police Constable 2025      │ Physical test starts     │ Police  │ AP
  Apr 25–27   │ TSPSC Group 1 Mains 2024      │ Mains exam (3 days)     │ State   │ TS
  Apr 30      │ SSC CGL 2026                  │ —                        │ Central │ 🇮🇳
  ────────────┴───────────────────────────────┴──────────────────────────┴─────────┴──────

  UPCOMING (next 90 days):
    May 2026:  APPSC AEE CBT, IBPS RRB notification expected
    Jun 2026:  SSC CGL application closes, UPSC CSE Prelims, IBPS PO notification
    Jul 2026:  SSC CGL Tier-I starts, AP DSC notification expected

  [Export to Google Calendar]  [Download ICS]  [Subscribe (auto-update)]
```

---

## 3. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/exam/calendar/?month=2026-04&state=AP,TS&type=state,central` | Calendar events for a month with filters |
| 2 | `GET` | `/api/v1/exam/calendar/my/?uid={uid}&months=3` | Calendar for user's saved exams (next N months) |
| 3 | `GET` | `/api/v1/exam/calendar/export/?format=ics&exams={slug1,slug2}` | Export as ICS for Google/Outlook Calendar |

---

## 5. Business Rules

- Calendar events are computed from exam date fields — `application_start`, `application_end`, `exam_dates[]`, `result_dates[]`, `admit_card_date`; each non-null date generates a calendar entry; this means adding a new exam with dates automatically populates the calendar without manual calendar editing; a date change in the exam record (exam postponed) automatically updates the calendar; there is no separate "calendar entry" table — the calendar is a view of exam dates
- The "My Exams Only" toggle filters the calendar to show only events for exams the user has saved in My Exams (A-05); this reduces noise dramatically — a student preparing for APPSC Group 2 and SSC CGL does not need to see TSPSC Group 1 Mains dates unless they have added TSPSC Group 1; the default for authenticated users is "My Exams Only" — they can switch to "All" to discover new exams
- Application deadline events (VRO/VRA AP application last date: Apr 10) are the highest-urgency calendar events; the system sends reminder alerts at D-7, D-3, and D-1 before the deadline to subscribed users; missing an application deadline means waiting an entire cycle (1–3 years) for the next opportunity; the reminder cadence is aggressive for application deadlines and lighter for other event types (exam date reminder: D-7 and D-1 only)
- ICS export and Google Calendar subscription enable aspirants to merge EduForge's exam calendar with their personal calendar; the ICS feed URL is per-user (scoped to their saved exams) and auto-updates when dates change; this is the most reliable way to ensure aspirants see exam dates on their phone's native calendar app alongside their personal events; the ICS feed includes `VALARM` entries (reminders) at D-7 and D-1 matching EduForge's in-app reminders
- Tentative dates (marked "tentative" in the exam record because the conducting body has not confirmed them) are shown on the calendar with a different visual treatment (dashed border, lighter colour) and a "tentative" label; when the date is confirmed (notification published), the treatment changes to solid; this prevents aspirants from confusing tentative estimates with confirmed dates; a student who books travel for a "tentative" exam date and then finds it moved to a different month would blame EduForge for the false signal

---

*Last updated: 2026-03-31 · Group 6 — Exam Domain Portal · Division C*
