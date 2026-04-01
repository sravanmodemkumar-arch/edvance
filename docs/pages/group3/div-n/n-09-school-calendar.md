# N-09 — School Calendar & Events (Parent View)

> **URL:** `/parent/calendar/`
> **File:** `n-09-school-calendar.md`
> **Template:** `parent_portal.html`
> **Priority:** P1
> **Roles:** Parent/Guardian (S1-P)

---

## 1. Purpose

Parents see the school's academic and events calendar — exam schedules, PTM dates, holidays, annual events, and class-specific activities. This view is curated from G-series (Events) and K-11 (Compliance Calendar) for the public-facing events.

The parent calendar is read-only — parents see events but cannot modify them. They can add events to their personal device calendar (Google Calendar / Apple Calendar via ICS export).

---

## 2. Calendar View

```
SCHOOL CALENDAR — Greenfields School (Parent View)
Academic Year: 2025–26 (April 2025 – March 2026)

APRIL 2026:
  Mon  Tue  Wed  Thu  Fri  Sat
  —    —    1    2    3    4
  6    7    8    9    10   11
  13   14   15   16   17   18
  20   21   22   23   24   25
  27   28   29   30

EVENTS (April 2026):
  🎭  5 Apr (Sat): Annual Day Rehearsal — All students (2–4 PM)
  📋  6 Apr (Mon): PTM — Class X [Book slot → N-07]
  🎓  10 Apr (Fri): Annual Day celebration (evening programme, 5:30 PM)
  🏖  14 Apr (Mon): Dr. B.R. Ambedkar Jayanti — SCHOOL HOLIDAY
  ✈  Ms. Priya Iyer: Last working day (TCH-015 — not shown to parents)

UPCOMING KEY DATES:
  31 Mar: Term 3 fee due date [Pay now → N-04]
  6 Apr:  PTM — Class X [Book → N-07]
  10 Apr: Annual Day (5:30 PM — children in school by 4:30 PM)
  15 Apr: Summer vacation begins
  2 Jun:  School reopens 2026–27

EXAMINATION SCHEDULE:
  Half-Yearly Examinations: 1–12 October 2025 (Classes VI–IX)
  Unit Test 2: 2–10 December 2025
  Annual Examinations: 1–15 March 2026 (Classes VI–IX)
  Board Exams (Class X): 15 Feb – 20 Mar 2026 (CBSE schedule — external)
  Board Exams (Class XII): 15 Feb – 20 Mar 2026 (CBSE schedule — external)

[Download full academic calendar PDF]  [Add all events to Google Calendar]
```

---

## 3. Class-Specific Events

```
CLASS X — RAHUL RAO — SPECIFIC EVENTS (April 2026):

  6 Apr (Mon): PTM [Book slot →]
  10 Apr (Fri): Annual Day — Class X students in Skit (report 4:30 PM)
               [Rahul is in the skit — confirm attendance by 5 Apr → N-11 consent]
  15 Apr: Summer vacation begins
  [CBSE Board results expected: May 2026 — notification when published]

PARENT REMINDERS:
  ● Annual Day costume: "White formal shirt + black trousers + school tie"
    (Class X skit uniform — teacher instructions sent via diary 22 Mar)
  ● Fee due: 31 March ← 4 days remaining [Pay now]
```

---

## 4. Holiday List

```
HOLIDAYS — 2025–26

Date        Day    Holiday                              Type
─────────────────────────────────────────────────────────────────
15 Aug 25   Fri    Independence Day                     National
3 Sep 25    Wed    Ganesh Chaturthi                     State (TS)
2 Oct 25    Thu    Gandhi Jayanti                       National
2 Nov 25    Sun    —
5 Nov 25    Wed    Diwali                               State
15 Nov 25   Sat    Gurunanak Jayanti                    National (partial Sat)
25 Dec 25   Thu    Christmas                            National
26 Jan 26   Mon    Republic Day                         National
1 Mar 26    Sun    —
14 Apr 26   Mon    Dr. B.R. Ambedkar Jayanti            National
15 Apr 26   Tue    Summer vacation begins               School calendar
─────────────────────────────────────────────────────────────────
Total holidays (working days excluded): 12 days ✅
Working days: 220 ✅ (K-11 compliance)

[Download full holiday list]  [Download academic calendar PDF]
```

---

## 5. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/parent/{parent_id}/child/{student_id}/calendar/events/` | All school events (this academic year) |
| 2 | `GET` | `/api/v1/parent/{parent_id}/child/{student_id}/calendar/events/?month=2026-04` | Events for a specific month |
| 3 | `GET` | `/api/v1/parent/{parent_id}/child/{student_id}/calendar/holidays/` | Full holiday list |
| 4 | `GET` | `/api/v1/school/{id}/calendar/ics/` | ICS file for calendar app import |

---

## 6. Business Rules

- The parent calendar shows only school-confirmed events (published by G-series); draft or internal planning events are not visible; a PTM is only visible once the school has confirmed the date and opened slot booking
- Events marked as "class-specific" (e.g., Class X skit rehearsal) are only visible to parents of students in that class; general announcements (Annual Day) are visible to all parents
- The ICS export is a snapshot at generation time — it does not sync dynamically; parents who import the ICS file will not see schedule changes made after import; the app's live calendar always reflects the latest information
- Exam schedules shown in the parent calendar are derived from the school's internal exam calendar (B-series + G-series); for board exams, the school publishes the CBSE-announced schedule (which is sourced from CBSE.nic.in, not EduForge — the school manually enters this)
- Holiday changes (emergency closures, additional holidays due to elections, weather) are notified via WhatsApp push (I-10 template mechanism) immediately and reflected in the calendar; parents should treat the app calendar as the authoritative source, not the printed academic calendar distributed at year-start

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division N*
