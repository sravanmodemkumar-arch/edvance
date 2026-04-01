# D-02 — Batch Schedule & Timetable

> **URL:** `/coaching/batches/schedule/`
> **File:** `d-02-batch-schedule.md`
> **Priority:** P1
> **Roles:** Batch Coordinator (K4) · Branch Manager (K6)

---

## 1. Weekly Timetable View

```
WEEKLY TIMETABLE — SSC CGL MORNING BATCH
Week of 30 March – 5 April 2026  |  Hall A, Main Campus

  Time        │ Mon 30  │ Tue 31   │ Wed 1    │ Thu 2    │ Fri 3    │ Sat 4
  ────────────┼─────────┼──────────┼──────────┼──────────┼──────────┼──────────
  06:00–07:00 │ Quant   │ English  │ Quant    │ Reasoning│ English  │ Full Mock
              │ Suresh K│ Kavita M │ Suresh K │ Mohan R  │ Kavita M │ (All subj)
  07:00–08:00 │ Quant   │ English  │ Quant    │ Reasoning│ English  │ Full Mock
              │ contd.  │ contd.   │ contd.   │ contd.   │ contd.   │ contd.
  08:00–09:00 │ Reasoning│ GK/CA   │ Reasoning│ Quant    │ Reasoning│ Full Mock
              │ Mohan R │ Ravi S   │ Mohan R  │ Suresh K │ Mohan R  │ review
  ────────────┴─────────┴──────────┴──────────┴──────────┴──────────┴──────────
  Hall:         Hall A   Hall A    Hall A    Hall A    Hall A    Hall A
  Capacity:     250       250       250       250       250       250
  Enrolled:     240       240       240       240       240       240

  NEXT WEEK (6–11 Apr):
  ⚠️ Hall A booked for SSC CGL Mock #25 on Apr 5 (Sun 9:00 AM–11:00 AM)
  ⚠️ No classes scheduled after Apr 18 — exam proximity blackout
```

---

## 2. All Batches Timetable (Coordinator View)

```
MASTER TIMETABLE — All Active Batches (30 March 2026)

  Slot      │ Hall A (cap 250)      │ Hall B (cap 200)      │ Hall C (cap 150)
  ──────────┼───────────────────────┼───────────────────────┼───────────────────
  6:00–9:00 │ SSC CGL Morning (240) │ Banking Morn. (200)   │ RRB NTPC (120)
  9:00–12:00│ SSC CHSL Morning(180) │ Foundation Batch (140)│ [FREE]
  12:00–3pm │ [FREE]                │ Banking Aftn. (80)    │ SSC CGL Crash(90)
  4:00–7:00 │ SSC CGL Evening (220) │ SSC CHSL Eve. (160)   │ RRB Evening (110)
  7:00–9:00 │ Banking Evening (160) │ [FREE]                │ Foundation Eve(80)
  ──────────┴───────────────────────┴───────────────────────┴───────────────────

  HALL UTILISATION:
    Hall A: 94.2% | Hall B: 76.0% | Hall C: 68.8%
    ⚠️ Hall A oversubscribed: SSC CGL Morning has 240/250 (96%) — near capacity
    Action: 18 new admissions deferred to SSC CGL Evening

  CONFLICTS:
    ✅ No double-booking detected
    ✅ Faculty break slots respected (min 30-min gap between back-to-back batches)
```

---

## 3. Edit / Add Schedule Slot

```
EDIT SCHEDULE — SSC CGL MORNING BATCH

  Day:      [Monday ▼]
  Slot:     [06:00 ▼]  to  [09:00 ▼]
  Hall:     [Hall A ▼]  (capacity: 250)
  Subject:  [Quantitative Aptitude ▼]
  Faculty:  [Suresh Kumar ▼]   (load this week: 38 hrs — ⚠️ near max 40)
  Topic:    [Mensuration 3D — Chapter 9 ▼]  (linked to curriculum tracker)
  Type:     (●) Regular Class  ( ) Extra Class  ( ) Doubt Session  ( ) Test

  CONFLICT CHECK:
    Hall A Mon 06:00–09:00 — ✅ Free
    Suresh Kumar Mon 06:00–09:00 — ✅ Available
    Batch Monday slot — ✅ Not already occupied

  [Save Slot]   [Cancel]

  NOTE: Changes to published schedule notify students via WhatsApp within 5 min
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/batches/{bid}/schedule/?week=2026-W14` | Weekly timetable for a batch |
| 2 | `GET` | `/api/v1/coaching/{id}/schedule/master/?date=2026-03-30` | All-batch master timetable for a day |
| 3 | `POST` | `/api/v1/coaching/{id}/batches/{bid}/schedule/` | Add new schedule slot |
| 4 | `PATCH` | `/api/v1/coaching/{id}/batches/{bid}/schedule/{sid}/` | Update existing slot |
| 5 | `DELETE` | `/api/v1/coaching/{id}/batches/{bid}/schedule/{sid}/` | Remove slot (notifies students) |
| 6 | `GET` | `/api/v1/coaching/{id}/schedule/conflicts/?hall={h}&date=2026-03-30` | Conflict check for a hall and date |

---

## 5. Business Rules

- Schedule changes made within 12 hours of a class trigger an automatic WhatsApp notification to all enrolled students with the old and new timings; changes made more than 12 hours in advance are sent as a daily digest at 7 PM; this prevents students from arriving at the wrong time and reduces coordinator call volume for "is class cancelled?" queries
- Faculty load must not exceed 40 teaching hours per week; the schedule editor prevents assigning a slot that would push a faculty member past 40 hours; a pop-up suggests available substitute faculty sorted by subject match and current availability; chronic overloading of specific faculty (because they are popular with students) is a retention risk — overloaded faculty resign at higher rates
- Hall double-booking is blocked at the API level, not just the UI level; a direct API call that attempts to create two batches in the same hall at the same time returns a 409 Conflict; the UI conflict check is a convenience feature, not the enforcement mechanism; this prevents race conditions when two coordinators try to book the same hall simultaneously
- The exam proximity blackout (no classes scheduled within 5 days of SSC CGL, IBPS, or RRB exam dates) is enforced automatically from the government exam calendar (B-05); students who are appearing for exams need revision time, not new content; classes scheduled in the blackout window require Academic Director override with a written justification
- Batch schedule data is published to the student-facing portal (O-01) and the parent app; any change immediately propagates to both; coordinators must note that parents rely on the schedule for logistics (transport, tuition timing for children) — frequent last-minute changes generate parent complaints tracked in the CRM

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division D*
