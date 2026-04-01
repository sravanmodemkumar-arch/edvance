# B-02 — Batch Calendar & Timetable

> **URL:** `/coaching/academic/calendar/`
> **File:** `b-02-batch-calendar.md`
> **Priority:** P1
> **Roles:** Academic Director (K6) · Academic Coordinator (K5) · Course Head (K5)

---

## 1. Weekly Timetable View

```
BATCH TIMETABLE — SSC CGL MORNING BATCH (Main Branch)
Week of 30 March – 5 April 2026

  Time       │ Monday      │ Tuesday     │ Wednesday   │ Thursday    │ Friday      │ Saturday
  ───────────┼─────────────┼─────────────┼─────────────┼─────────────┼─────────────┼──────────────
  06:00–07:00│ Quant       │ Reasoning   │ Quant       │ English     │ Quant       │ GK / CA
  07:00–08:00│ Mr. Suresh  │ Mr. Kiran   │ Mr. Suresh  │ Ms. Meena   │ Mr. Suresh  │ Mr. Rajesh
             │ Mensuration │ Syllogism   │ Algebra     │ RC+Grammar  │ Speed-Time  │ Current Affairs
  ───────────┼─────────────┼─────────────┼─────────────┼─────────────┼─────────────┼──────────────
  08:00–08:30│ Doubt Clear │ Doubt Clear │ Doubt Clear │ Doubt Clear │ Doubt Clear │ Weekly Quiz
             │ (Suresh/Kim)│ (Kiran)     │ (Suresh)    │ (Meena)     │ (Suresh)    │ (30 marks)
  ───────────────────────────────────────────────────────────────────────────────────────────────
  Hall:      Hall A        Hall A        Hall A        Hall A        Hall A        Hall A
  Students:  240           240           240           240           240           240

TIMETABLE COVERAGE — Week:
  Quant: 3 sessions (6 hrs)  Reasoning: 1 (2 hrs)  English: 1 (2 hrs)
  GK/CA: 1 (1 hr)  Doubt: 5 (2.5 hrs)  Quiz: 1 (0.5 hr)
  Total contact hours: 14 hrs/week ✅ (target: 12–15 hrs/week)
```

---

## 2. All Batches Calendar View

```
MASTER BATCH CALENDAR — March – April 2026

  BATCH                │ Days      │ Time          │ Room    │ Starts     │ Ends
  ─────────────────────┼───────────┼───────────────┼─────────┼────────────┼────────────
  SSC CGL Morning      │ Mon–Sat   │ 06:00–08:30   │ Hall A  │ Jun 2025   │ Mar 2026
  SSC CGL Eve (New)    │ Mon–Sat   │ 17:00–19:30   │ Hall A  │ Jan 2026   │ Sep 2026
  SSC CHSL Morning     │ Mon–Fri   │ 06:00–08:00   │ Hall B  │ Aug 2025   │ Mar 2026
  RRB NTPC Weekend     │ Sat–Sun   │ 07:00–11:00   │ Hall C  │ Sep 2025   │ May 2026
  Banking Morning      │ Mon–Sat   │ 06:00–08:00   │ Room 3  │ Oct 2025   │ May 2026
  Banking Eve          │ Mon–Fri   │ 17:00–19:00   │ Room 3  │ Jan 2026   │ Aug 2026
  Foundation 9-10      │ Mon–Fri   │ 16:00–18:00   │ Room 4  │ Jun 2025   │ Mar 2026
  Dropper JEE          │ Mon–Sat   │ 06:00–12:00   │ Room 6  │ Jun 2025   │ May 2026
  Crash Course Apr'26  │ Mon–Sat   │ 07:00–09:00   │ Room 5  │ Apr 2026   │ May 2026
  Online Live SSC      │ Mon–Fri   │ 19:00–21:00   │ Zoom    │ Feb 2026   │ Sep 2026

UPCOMING BATCH STARTS:
  ⭐ New SSC CGL batch: 1 May 2026 (180 seats — 94 enrolled so far)
  ⭐ New Foundation batch: 1 June 2026 (100 seats — 28 enrolled)
  ⭐ Crash Course (May): 15 May 2026 (60 seats — open for enrollment)
```

---

## 3. Room Utilisation

```
ROOM / HALL UTILISATION — MAIN BRANCH (March 2026)

  Room     │ Capacity │ Sessions/Day │ Peak Hour Usage │ Utilisation
  ─────────┼──────────┼──────────────┼─────────────────┼────────────
  Hall A   │   250    │      2       │ 06:00 + 17:00   │ 96%
  Hall B   │   200    │      2       │ 06:00 + 17:30   │ 90%
  Hall C   │   200    │      1       │ Saturday 07:00  │ 64% (weekends only)
  Room 3   │    60    │      2       │ 06:00 + 17:00   │ 88%
  Room 4   │    40    │      1       │ 16:00 weekdays  │ 75%
  Room 5   │    60    │      1       │ Variable         │ 40% (crash courses)
  Room 6   │    80    │      1       │ 06:00–12:00     │ 100% (Dropper)
  Counsell.│    10    │      4       │ 10:00–17:00     │ 85%

  ⚠️ Hall A at 96% — new batch (May) must use Hall B or stagger timing
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/academic/timetable/?batch={id}` | Weekly timetable for a batch |
| 2 | `GET` | `/api/v1/coaching/{id}/academic/batches/calendar/` | All active batches list |
| 3 | `POST` | `/api/v1/coaching/{id}/academic/timetable/` | Create/update timetable slot |
| 4 | `GET` | `/api/v1/coaching/{id}/academic/rooms/utilisation/` | Room utilisation report |
| 5 | `GET` | `/api/v1/coaching/{id}/academic/timetable/conflicts/` | Detect faculty or room conflicts |

---

## 5. Business Rules

- Timetable conflicts (same faculty, same time, two batches) must be detected automatically at the time of scheduling, not discovered on the day; EduForge's conflict detection checks faculty availability and room availability simultaneously before saving a timetable slot; a conflict detected at scheduling time costs 2 minutes to resolve; a conflict discovered on the day costs the institute a cancelled class and student dissatisfaction
- Room utilisation above 95% for any room is a risk indicator; at 96% utilisation, any unexpected event (power cut, maintenance, faculty swap requiring a larger room) has no buffer; the Academic Coordinator must plan the new May 2026 batch without using Hall A at peak hours; the utilisation report is reviewed monthly to identify infrastructure bottlenecks before they become crises
- Batch end dates must be set realistically relative to the target exam; SSC CGL batches should end 2–3 weeks before the actual SSC CGL exam date (to allow self-revision time); a batch that continues classes until the day before the exam overloads students; EduForge's exam calendar (Division B, B-05) feeds into batch end date recommendations automatically
- Online batch timetables (Zoom) must be published at least 72 hours in advance with Zoom links; students who join Zoom links 30 seconds before the class starts from different time zones or connectivity conditions need buffer; last-minute link sharing via WhatsApp creates confusion and reduces punctuality; TCC's standard is: Zoom link on EduForge platform 72 hours before class, with WhatsApp reminder 30 minutes before
- The master batch calendar is visible to all K3+ staff; students can see only their own batch schedule; a student in the SSC CGL Morning batch cannot see the Banking batch timetable — this prevents informal "batch hopping" where students attend sessions from other batches without enrolling, which disrupts class size management and dilutes the enrolled students' attention

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division B*
