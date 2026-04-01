# B-27 — Coaching Test Planner

> **URL:** `/school/academic/coaching/tests/`
> **File:** `b-27-coaching-test-planner.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Academic Coordinator (S4) — full · Exam Cell Head (S4) — coaching test logistics · Subject Teacher (S3) — read/view results · Principal (S6) — full

> ⚡ **Feature Flag:** Visible only for schools with `coaching_integration: true` in school settings.

---

## 1. Purpose

Plans and manages the coaching test series for JEE/NEET/Foundation-integrated schools. These are different from board exams — they follow JEE/NEET paper patterns (MCQ only, negative marking, subject-wise cutoffs), run weekly/fortnightly, are competitive rank-based, and track each student's JEE/NEET preparation trajectory. A typical integrated school runs:
- **Weekly tests:** Sunday morning, 1–1.5 hours, recent topics (JEE pattern)
- **Monthly tests:** Full 3-hour JEE/NEET mock (all topics covered so far)
- **AITS (All India Test Series):** Partnered with AAKASH/Allen/FIITJEE — centrally conducted, national rank

The Academic Coordinator plans this test calendar alongside the board exam calendar to ensure students aren't overwhelmed. Results from these tests are viewed by students, parents, teachers, and counsellors — they are a parallel academic performance track alongside CBSE marks.

---

## 2. Page Layout

### 2.1 Header
```
Coaching Test Planner                             [+ Schedule Test]  [Weekly Test Results]  [AITS Tracker]
Class: [XI-A JEE ▼]  Year: 2025–26
Tests Scheduled: 48  ·  Completed: 38  ·  In Progress: 1  ·  Upcoming: 9
This week: JEE Weekly Test W-12 — Sunday 30 Mar 2026
```

---

## 3. Test Calendar Overview

| # | Test Name | Type | Pattern | Classes | Date | Duration | Max Marks | Status |
|---|---|---|---|---|---|---|---|---|
| W-01 | JEE Weekly Test 1 | Weekly | JEE Main MCQ | XI-JEE | 6 Apr 2025 | 90 min | 90 | ✅ Done |
| W-02 | JEE Weekly Test 2 | Weekly | JEE Main MCQ | XI-JEE | 13 Apr 2025 | 90 min | 90 | ✅ Done |
| M-01 | Monthly Test 1 | Monthly | JEE Main Full | XI-JEE | 25 May 2025 | 180 min | 300 | ✅ Done |
| W-10 | JEE Weekly Test 10 | Weekly | JEE Main MCQ | XI-JEE | 23 Mar 2026 | 90 min | 90 | ✅ Done |
| W-11 | JEE Weekly Test 11 | Weekly | JEE Main MCQ | XI-JEE | 30 Mar 2026 | 90 min | 90 | ⏳ Upcoming |
| AITS-1 | AAKASH AITS 1 | AITS | JEE Advanced | XI, XII | 5 Apr 2026 | 180 min | 300 | ⏳ Upcoming |
| M-06 | Monthly Test 6 (Pre-Board Mock) | Monthly | JEE Main Full | XII-JEE | 15 Apr 2026 | 180 min | 300 | ⏳ Upcoming |

**Test types:**
- **Weekly:** Short test (specific recent chapters), 90 min, JEE Main MCQ pattern
- **Monthly:** Full mock (all covered topics), 3 hours, JEE Main/NEET Full
- **AITS:** All India Test Series — partnered with national coaching institutes; students get national rank
- **Revision Test:** Before board exams — focuses on CBSE topics simultaneously
- **NEET Pattern:** For BiPC section — same structure but NEET paper pattern (Physics 45Q, Chemistry 45Q, Biology 90Q)

---

## 4. Schedule Test

[+ Schedule Test] → form:

| Field | Value |
|---|---|
| Test Name | JEE Weekly Test 12 |
| Type | Weekly / Monthly / AITS / Revision / NEET Pattern |
| Date | 6 Apr 2026 (Sunday) |
| Time | 8:00 AM – 9:30 AM |
| Duration | 90 minutes |
| Classes | XI-JEE (30 students), XI-NEET (25 students) |
| Pattern | JEE Main MCQ (PCM only) |
| Subjects & Marks | Physics: 30Q (4m/-1m), Chemistry: 30Q (4m/-1m), Maths: 30Q (4m/-1m) |
| Total Marks | 360 (before negative) |
| Topics Covered | Recent (Weeks 11–12): Wave Optics, Electrochemistry, Integration |
| Hall | Computer Lab 1 or Exam Hall (TBD) |
| Question Paper | Upload PDF [Browse] |
| Answer Key | Upload Answer Key PDF |

**Negative Marking** — JEE/NEET pattern: +4 for correct, -1 for wrong, 0 for unattempted. The system computes scores with negative marking.

---

## 5. Test Results Entry

After each test, scores are entered:

```
JEE Weekly Test W-11 — Results Entry
XI-A (JEE Foundation) — 30 students

Roll  Name              Physics(90) Chemistry(90) Maths(90) Total(270) Correct/Wrong  %ile
001   Arjun Sharma       72          78            84         234        57C/9W         87.4%
002   Priya Venkat       68          74            76         218        53C/8W         78.2%
003   Rohit Kumar        80          82            88         250        61C/5W         93.8%
...

Class Avg:     184.2 / 270  ·  68.2%
Topper:        Rohit Kumar — 250 (93.8%ile in class)
```

For AITS (centrally conducted): National rank is imported from the external institute's data export.

---

## 6. Student Performance Trajectory

For each student, coaching test performance across the year:

```
Arjun Sharma — JEE Performance Trend (XI-JEE)

Month    Test           PCM Score    Percentile  Rank
Apr      Weekly W-1     142/270      62.4%       18/30
May      Monthly M-1    198/300      71.8%       14/30
Jun      Weekly W-5     164/270      68.2%       16/30
Aug      Monthly M-2    218/300      78.4%       11/30
Nov      AITS-3         210/300      72.1%       National: 14,280
Jan      Monthly M-5    238/300      84.2%       9/30
Mar      Weekly W-11    234/270      87.4%       6/30  ← improving trend ↑
```

Visible to student, parents, class teacher, Academic Coordinator.

---

## 7. AITS (All India Test Series) Tracker

| AITS Round | Partner | Date | XII Students | National Rank (Avg) | National Rank (Topper) |
|---|---|---|---|---|---|
| AAKASH AITS-1 | AAKASH | 5 Apr 2026 | 28 | 18,400 | 4,200 (Rohit K) |
| Allen AITS-2 | Allen | 12 Apr 2026 | 28 | 16,800 | 3,900 (Rohit K) |
| FIITJEE AITS-1 | FIITJEE | 19 Apr 2026 | 25 | 19,200 | 5,100 (Arjun S) |

National rank tracking allows the Academic Coordinator to assess whether school students are competitive nationally, and where to focus coaching attention.

---

## 8. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/coaching/tests/?class_id={id}&year={year}` | Test schedule |
| 2 | `POST` | `/api/v1/school/{id}/coaching/tests/` | Schedule new test |
| 3 | `GET` | `/api/v1/school/{id}/coaching/tests/{test_id}/` | Test detail |
| 4 | `PATCH` | `/api/v1/school/{id}/coaching/tests/{test_id}/results/` | Enter results |
| 5 | `GET` | `/api/v1/school/{id}/coaching/tests/student/{student_id}/trajectory/` | Student performance trajectory |
| 6 | `GET` | `/api/v1/school/{id}/coaching/tests/aits/` | AITS tracker |
| 7 | `GET` | `/api/v1/school/{id}/coaching/tests/analytics/?class_id={id}` | Class performance analytics |

---

## 9. Business Rules

- Coaching tests (weekly/monthly) do not contribute to CBSE marks — they are purely for JEE/NEET preparation tracking
- Negative marking computation is done server-side; raw correct/incorrect counts are stored and the score is computed from them
- AITS results (national rank) are imported via CSV from external institutes; format varies by institute — EduForge accepts standard 3-column format (student_id, national_rank, percentile)
- Coaching test schedules should not overlap with CBSE board exam dates or major school exams — the system warns if a weekly test is scheduled within 3 days of a board exam date
- This module requires the `coaching_integration` feature flag — all APIs return 403 for schools without the flag

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division B*
