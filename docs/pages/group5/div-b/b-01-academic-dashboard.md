# B-01 — Academic Director Dashboard

> **URL:** `/coaching/academic/dashboard/`
> **File:** `b-01-academic-dashboard.md`
> **Priority:** P1
> **Roles:** Academic Director (K6) · Course Head — SSC/RRB (K5) · Course Head — Banking (K5)

---

## 1. Academic Overview

```
ACADEMIC DASHBOARD — TOPPERS COACHING CENTRE
Academic Director: Mr. Suresh Kumar
As of 30 March 2026

ACADEMIC VITALS:
  ┌────────────────────────────────────────────────────────────────────────────┐
  │  24 Active      88.1%          14 Tests       186               4.3/5.0   │
  │  Batches        Avg            Scheduled      Selections        Avg Faculty│
  │                 Attendance     (Apr 2026)      (FY 2025–26)      Rating    │
  └────────────────────────────────────────────────────────────────────────────┘

BATCH PERFORMANCE SNAPSHOT (last mock test):
  ┌──────────────────────────────────┬────────────┬────────────┬─────────────────┐
  │ Batch                            │ Avg Score  │ Attend %   │ Flag            │
  ├──────────────────────────────────┼────────────┼────────────┼─────────────────┤
  │ SSC CGL Morning (Main)           │ 162/200    │ 85.2%      │ ✅              │
  │ SSC CGL Evening (Dilsukhnagar)   │ 154/200    │ 80.4%      │ ⚠️ score drop  │
  │ SSC CHSL Evening (Main)          │ 141/200    │ 80.1%      │ ✅              │
  │ RRB NTPC Weekend (Main)          │ 158/200    │ 77.6%      │ ⚠️ attendance  │
  │ Banking Morning (Main)           │ 158/200    │ 83.4%      │ ✅              │
  │ Foundation 9-10 (Main)           │  78%       │ 88.9%      │ ✅              │
  │ Dropper JEE (Hostel)             │ 174/360    │ 91.2%      │ ✅              │
  │ ... 17 more batches              │            │            │                 │
  └──────────────────────────────────┴────────────┴────────────┴─────────────────┘

ACTIVE ALERTS:
  🔴 SSC CGL Eve (Dilsukhnagar): Score dropped 12 pts vs last month — review needed
  🟡 RRB NTPC Weekend: Attendance 77.6% — below 80% threshold; 3 consecutive weeks
  🟡 2 faculty: Rating < 3.5/5.0 in Feb survey — PIP discussion scheduled 2 Apr
  🟢 Banking Morning: 2 students cleared IBPS PO prelim (mock rank → real result ✅)
```

---

## 2. Today's Academic Schedule

```
TODAY — 30 March 2026 (Monday)

CLASSES RUNNING NOW / TODAY:
  Time        │ Batch                 │ Faculty              │ Subject          │ Room
  ────────────┼───────────────────────┼──────────────────────┼──────────────────┼──────
  06:00–08:00 │ SSC CGL Morning       │ Mr. Suresh Kumar     │ Quant — Mensurat.│ Hall A
  06:00–08:00 │ Banking Morning       │ Ms. Meena Iyer       │ English — RC     │ Hall B
  06:00–08:00 │ Foundation 9-10       │ Ms. Divya Nair       │ Maths — Algebra  │ Room 4
  08:30–10:30 │ Dropper JEE           │ Mr. Kiran Sharma     │ Physics — Optics │ Room 6
  17:00–19:00 │ SSC CHSL Evening      │ Mr. Rajesh Varma     │ GK — Polity      │ Hall A
  17:00–19:00 │ RRB NTPC Evening      │ Mr. Ravi Naidu       │ Reasoning        │ Hall B
  17:30–19:30 │ Banking Evening       │ Mr. Praveen Rao      │ Banking Aware.   │ Room 3
  ────────────────────────────────────────────────────────────────────────────────────
  Cancelled today: 0 classes ✅
  Substitution needed: 0 ✅
```

---

## 3. Upcoming Exam & Test Calendar

```
EXAM & TEST CALENDAR — April 2026

  Date    │ Type          │ Batch                │ Duration │ Marks │ Status
  ────────┼───────────────┼──────────────────────┼──────────┼───────┼──────────
  Apr 2   │ Monthly Mock  │ SSC CGL All batches  │ 60 min   │ 200   │ ⬜ Scheduled
  Apr 3   │ Sprint Test   │ RRB NTPC Weekend     │ 90 min   │ 100   │ ⬜ Scheduled
  Apr 5   │ Full Mock #24 │ Banking All batches  │ 60 min   │ 100   │ ⬜ Scheduled
  Apr 8   │ Chapter Test  │ Foundation 9-10      │ 45 min   │  60   │ ⬜ Scheduled
  Apr 10  │ JEE Mock #18  │ Dropper JEE          │ 3 hrs    │ 300   │ ⬜ Scheduled
  Apr 12  │ GK Weekly     │ All SSC batches      │ 15 min   │  50   │ ⬜ Scheduled
  Apr 15  │ Mid-month Mock│ Banking All batches  │ 60 min   │ 100   │ ⬜ Scheduled
  Apr 20  │ Full Mock #25 │ SSC CGL All batches  │ 60 min   │ 200   │ ⬜ Scheduled
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/academic/dashboard/` | Academic director overview |
| 2 | `GET` | `/api/v1/coaching/{id}/academic/today/` | Today's schedule across all batches |
| 3 | `GET` | `/api/v1/coaching/{id}/academic/batch-performance/` | Latest mock scores per batch |
| 4 | `GET` | `/api/v1/coaching/{id}/academic/alerts/` | Academic alerts (score drops, attendance) |
| 5 | `GET` | `/api/v1/coaching/{id}/academic/exam-calendar/?month=2026-04` | Upcoming tests |

---

## 5. Business Rules

- Batch score comparison across branches must account for paper difficulty — a Dilsukhnagar batch scoring 154/200 on a harder paper may actually outperform a Main batch scoring 162/200 on an easier paper; EduForge computes a difficulty-adjusted score (DAS) using the question discrimination index from each test; the Academic Director should review DAS, not raw scores, when comparing cross-branch performance
- The Academic Director sees aggregated batch data, not individual student scores; individual student performance is the domain of the Batch Coordinator (Division D) and Counsellor (Division J); this separation ensures the Academic Director focuses on systemic improvements (curriculum, faculty quality, test design) rather than micromanaging individual students
- A score drop of more than 8% from the previous mock in any batch must trigger an automatic investigation flag; the Course Head must log a root cause within 48 hours (e.g., difficult paper, topic not yet covered, batch disruption); unexplained score drops that persist for 2+ consecutive tests indicate either a faculty quality issue or a curriculum sequencing problem — both requiring Academic Director intervention
- Faculty substitution policy: if a faculty member is absent, the class must be covered by a substitute of equivalent subject expertise within 30 minutes; an uncovered class is logged as an academic failure event; more than 3 uncovered class events in a month for any faculty triggers a formal counselling; the Academic Director reviews uncovered class data weekly to identify patterns (recurring absences, specific time slots)
- The Course Head for each exam category (SSC, Banking, RRB) has autonomous authority over curriculum sequencing and topic scheduling within their category; the Academic Director sets the overall academic calendar (test dates, revision weeks, crash course windows) and quality standards; Course Heads report to the Academic Director weekly; this delegation model allows specialisation while maintaining cross-category coordination

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division B*
