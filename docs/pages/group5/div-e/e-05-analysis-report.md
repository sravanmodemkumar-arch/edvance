# E-05 — Test Analysis Report

> **URL:** `/coaching/tests/analysis/`
> **File:** `e-05-analysis-report.md`
> **Priority:** P2
> **Roles:** Test Series Coordinator (K4) · Academic Director (K5) · Faculty (K2)

---

## 1. Test Analysis Overview

```
TEST ANALYSIS — SSC CGL Full Mock #25
Published: 5 Apr 2026, 11:28 AM  |  Students: 1,183 graded

  OVERALL STATS:
    Average:   106.4 / 200   (53.2%)
    Median:    102 / 200
    Top Score: 186 / 200  (TCC-2401 — Akhil Kumar)
    StdDev:    28.4
    Pass Rate (> 145 est. cutoff):  14.2%  (168/1,183)

  SECTION PERFORMANCE:
    Section          │ Max │ Avg   │ Attempt% │ Accuracy% │ Flag
    ─────────────────┼─────┼───────┼──────────┼───────────┼────────────────────
    Quant            │  50 │ 32.4  │  91.2%   │  71.1%    │ ✅ Good
    English          │  50 │ 35.8  │  94.8%   │  75.4%    │ ✅ Good
    Reasoning        │  50 │ 30.2  │  88.4%   │  68.2%    │ ⚠️ Below avg
    GK / CA          │  50 │  8.0  │  62.1%   │  25.8%    │ 🔴 Critical
    ─────────────────┴─────┴───────┴──────────┴───────────┴────────────────────
    TOTAL            │ 200 │106.4  │  84.1%   │  53.2%    │

  GK FLAG: 25.8% accuracy is extremely low — likely caused by 8 current affairs
  questions from Feb–Mar 2026 that the batch has not covered yet (verified ✅)
  Action: GK session scheduled Apr 6 to cover Mar 2026 current affairs
```

---

## 2. Question-Level Analysis

```
QUESTION ANALYSIS — Top 10 Hardest Questions (by % wrong)

  Q#  │ Section   │ Topic                   │ Correct% │ Wrong% │ Skip% │ Avg time │ Flag
  ────┼───────────┼─────────────────────────┼──────────┼────────┼───────┼──────────┼──────────
  Q58 │ GK        │ Feb 2026 Budget clause  │   8.2%   │  72.4% │ 19.4% │ 22 sec   │ 🔴 Too Hard
  Q61 │ GK        │ Mar PM Economic speech  │   9.8%   │  68.1% │ 22.1% │ 18 sec   │ 🔴 Too Hard
  Q42 │ Reasoning │ Input-Output 6-step     │  24.4%   │  61.2% │ 14.4% │ 3.2 min  │ 🔴 Time-sink
  Q14 │ Quant     │ Mensuration 3D frustum  │  31.2%   │  52.8% │ 16.0% │ 2.8 min  │ 🟡 Hard
  Q19 │ English   │ One-word substitution   │  38.4%   │  48.2% │ 13.4% │ 42 sec   │ 🟡 Hard
  Q38 │ Reasoning │ Caselet seating 5-var   │  28.8%   │  56.4% │ 14.8% │ 3.6 min  │ 🔴 Time-sink
  Q11 │ Quant     │ Caselet DI — ratio      │  34.2%   │  50.4% │ 15.4% │ 2.4 min  │ 🟡 Hard
  Q74 │ GK        │ ISRO mission detail     │  18.4%   │  64.8% │ 16.8% │ 14 sec   │ 🔴 Too Hard
  Q82 │ GK        │ State CM Jan 2026       │  22.4%   │  60.2% │ 17.4% │ 16 sec   │ 🟡 Hard
  Q21 │ English   │ Reading comp — inference│  42.4%   │  44.8% │ 12.8% │ 2.2 min  │ 🟡 Acceptable

  ⚠️ Q58 and Q61: GK from uncovered period — recommend excluding from scoring
     Review: [Mark as Bonus (+2 all)] or [Exclude Q58+Q61 from scores] → Awaiting sign-off
```

---

## 3. Time Analysis

```
TIME MANAGEMENT — SSC CGL Full Mock #25

  TIME USAGE DISTRIBUTION:
    Submitted in < 45 min:  68  ( 5.7%)  → rushed, likely low accuracy
    Submitted in 45–55 min: 284 (24.0%)  → efficient
    Submitted in 55–60 min: 642 (54.3%)  → used full time (ideal)
    Auto-submitted (60 min):186 (15.7%)  → ran out of time (concern)

  ⚠️ 186 students (15.7%) ran out of time — Reasoning section most affected
  Avg time on Reasoning: 18.4 min (of allotted ~15 min for 25 Qs at 1 min avg)
  Action: Time management workshop scheduled for at-risk students

  SECTION ORDER (most common strategy):
    1. Reasoning → English → Quant → GK:  48% of students
    2. English → Reasoning → GK → Quant:  22% of students
    3. GK → English → Reasoning → Quant:  18% of students
    Other strategies:                      12%

  RECOMMENDATION: Students who attempted GK last scored 22% lower on GK
  (ran out of time). Coordinator note: encourage students to do GK early.
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/tests/{tid}/analysis/` | Full test analysis report |
| 2 | `GET` | `/api/v1/coaching/{id}/tests/{tid}/analysis/questions/` | Per-question difficulty stats |
| 3 | `GET` | `/api/v1/coaching/{id}/tests/{tid}/analysis/time/` | Time management breakdown |
| 4 | `GET` | `/api/v1/coaching/{id}/tests/{tid}/analysis/sections/` | Section-level performance |
| 5 | `POST` | `/api/v1/coaching/{id}/tests/{tid}/analysis/questions/{qid}/bonus/` | Mark question as bonus (award to all) |
| 6 | `GET` | `/api/v1/coaching/{id}/tests/{tid}/analysis/compare/?prev={tid2}` | Compare with previous test |

---

## 5. Business Rules

- The test analysis report is auto-generated after results are published; it is available to the Test Series Coordinator, Academic Director, and subject faculty (faculty see only their subject's section analysis, not full test data); the analysis feeds into three downstream processes: faculty performance review (B-07), batch performance tracking (D-05), and the rank predictor (E-06); a test without a completed analysis is incomplete in the pipeline
- Questions with correct-answer rates below 20% trigger an automatic "difficulty review" flag; the coordinator and faculty must jointly review whether the question was genuinely hard (good) or poorly framed / from uncovered syllabus (problem); if the review finds a syllabus mismatch, the question is awarded to all (bonus) and retired from the bank; if the review finds the question was valid, it is tagged as "high difficulty" and kept in the bank for future advanced mocks
- Time-sink questions (average time > 3 minutes) are flagged separately from difficulty flags; a question can be easy but time-consuming (detailed calculation) or hard and quick (GK recall); time-sink questions in a timed exam disproportionately penalise students who don't skip strategically; the analysis identifies time-sinks so faculty can teach the "skip and return" strategy explicitly; questions averaging > 4 minutes are reviewed for whether they are appropriate for a 60-minute paper
- Analysis reports are retained permanently in the test archive; a coordinator cannot delete a test analysis report; historical analysis across 6+ months of mocks shows improvement curves that are used in quarterly reviews, franchise assessments, and marketing materials; the retention policy is minimum 3 years for regulatory audit purposes and indefinite for operational use
- Section-level analysis data for each batch (Reasoning average 30.2/50) is compared automatically with the previous 3 tests to generate a trend; a downward trend in any section for two consecutive tests triggers an alert to the Academic Director; the alert includes the faculty responsible for that section, the topics covered in the period, and the question difficulty calibration; this creates accountability without manual monitoring by the Academic Director

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division E*
