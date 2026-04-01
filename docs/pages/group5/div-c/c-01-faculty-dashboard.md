# C-01 — Faculty Dashboard

> **URL:** `/coaching/faculty/dashboard/`
> **File:** `c-01-faculty-dashboard.md`
> **Priority:** P1
> **Roles:** Faculty — all subjects (K2) · Senior Faculty (K2)

---

## 1. Faculty Home View

```
FACULTY DASHBOARD — Mr. Suresh Kumar
Subject: Quantitative Aptitude | Branch: Main (Himayatnagar)
As of 30 March 2026 (Monday)

  ┌─────────────────────────────────────────────────────────────────────────────┐
  │  4 Batches      38 hrs/wk    1,240 Qs     4.6/5.0     0 Pending           │
  │  Assigned       Load         in Bank      My Rating   Doubt Queue          │
  └─────────────────────────────────────────────────────────────────────────────┘

TODAY'S SCHEDULE:
  ┌────────────┬────────────────────────────┬─────────┬─────────────────────────┐
  │ Time       │ Batch                      │ Room    │ Topic                   │
  ├────────────┼────────────────────────────┼─────────┼─────────────────────────┤
  │ 06:00–07:00│ SSC CGL Morning            │ Hall A  │ Mensuration — 3D shapes │
  │ 07:00–07:30│ Doubt clearing (CGL Morn)  │ Hall A  │ Open Q&A                │
  │ 07:00–08:00│ Banking Morning            │ Room 3  │ DI — Pie Chart          │
  │            │ ⚠️ CONFLICT: overlaps with │         │ → Sub: Ms. Divya Nair   │
  │            │ CGL doubt session          │         │ (already arranged)      │
  └────────────┴────────────────────────────┴─────────┴─────────────────────────┘

UPCOMING THIS WEEK:
  Mon 06:00 — SSC CGL Morning — Mensuration 3D (today)
  Tue 06:00 — SSC CHSL Morning — Time & Work (revision)
  Wed 06:00 — SSC CGL Morning — DI Mixed Practice
  Thu 06:00 — Banking Morning — Approximation + Simplification
  Fri 06:00 — SSC CGL Morning — Full chapter test (Mensuration + DI)
  Sat 06:00 — All batches — Doubt marathon (2 hrs)

RECENT TEST RESULTS (my batches):
  SSC CGL Mock #23 (15 Mar):  Avg Quant score: 16.4/25  (65.6%) → up from 14.8 last month ✅
  Banking Mock #17 (18 Mar):  Avg Quant score: 15.8/25  (63.2%)
```

---

## 2. My Batches Overview

```
MY BATCHES — Mr. Suresh Kumar (Quant)

  Batch               │ Students │ Syllabus Done │ Next Class    │ Avg Quant Score
  ────────────────────┼──────────┼───────────────┼───────────────┼─────────────────
  SSC CGL Morning     │   236    │ 95.8%  ✅     │ Today 06:00   │ 65.6% (↑)
  SSC CHSL Morning    │   178    │ 88.2%  ✅     │ Tue 06:00     │ 62.4% (→)
  Banking Morning     │   196    │ 91.0%  ✅     │ Thu 06:00     │ 63.2% (→)
  Crash Course Apr'26 │    48    │ 40.0%  ⚠️     │ Mon 07:00     │ 58.8% (↓)
  ────────────────────────────────────────────────────────────────────────────────
  ⚠️ Crash Course: Only 40% done in 2 weeks — accelerate from 3 topics/week to 5
```

---

## 3. Quick Actions

```
QUICK ACTIONS:

  [📋 Take Attendance — SSC CGL Morning]   [Today's class — starts in 14 min]

  [📤 Upload Today's Notes]
  [❓ View Doubt Queue (0 pending)]
  [📝 Create Quick Quiz]
  [📊 View My Students' Performance]
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/faculty/{fid}/dashboard/` | Faculty home data |
| 2 | `GET` | `/api/v1/coaching/{id}/faculty/{fid}/today/` | Today's schedule |
| 3 | `GET` | `/api/v1/coaching/{id}/faculty/{fid}/batches/` | My batches with stats |
| 4 | `GET` | `/api/v1/coaching/{id}/faculty/{fid}/recent-results/` | Recent test scores in my subject |

---

## 5. Business Rules

- Faculty see only their own batches, their own question bank contributions, and aggregated scores for their subject; they cannot see other faculty members' ratings, salaries, or batch assignments; this role isolation prevents inter-faculty comparison tensions while still giving each faculty member the information they need to do their job
- The "conflict" flag on today's schedule (two classes at the same time) is automatically detected when a substitute is already arranged; EduForge shows it as informational, not as an alert requiring action; if no substitute is arranged, the flag becomes a red alert requiring the faculty to contact the Academic Coordinator immediately
- Faculty load (38 hrs/week for Suresh Kumar) is visible on the dashboard as a self-awareness tool; faculty who can see their own load proactively approach the Academic Coordinator when they are approaching burnout, rather than letting quality slip silently; the load figure includes teaching hours and doubt sessions but not question bank or administrative time
- The "Crash Course 40% done — accelerate" alert is system-generated based on the batch timeline; crash courses have compressed timelines (6 weeks) and require faster topic progression; a faculty who teaches at their normal pace will undershoot the syllabus; the dashboard alert prompts the faculty to adapt, not to wait for the Academic Director to notice
- The faculty dashboard is the first screen faculty see on login; it must load within 2 seconds and show only actionable today-information; deep analytics are in separate pages (C-06); a dashboard overloaded with historical data distracts from the faculty's immediate task — preparing for and conducting today's class

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division C*
