# E-07 — Paper Difficulty Analysis

> **URL:** `/coaching/tests/paper-analysis/`
> **File:** `e-07-paper-analysis.md`
> **Priority:** P2
> **Roles:** Test Series Coordinator (K4) · Academic Director (K5) · Faculty (K2)

---

## 1. Paper Difficulty Overview

```
PAPER DIFFICULTY ANALYSIS — SSC CGL Full Mock #25
Difficulty review post-publication | 5 Apr 2026

  PAPER-LEVEL DIFFICULTY SCORE:
    ┌──────────────────────────────────────────────────────────────────────────┐
    │  Overall Difficulty:  MEDIUM-HARD  (Score: 6.4 / 10)                   │
    │  Target for full mocks: 5.5–7.0 ✅ Within range                        │
    └──────────────────────────────────────────────────────────────────────────┘

  SECTION BREAKDOWN:
    Section    │ Difficulty │ Score │ Target  │ Status
    ───────────┼────────────┼───────┼─────────┼──────────────────────
    Quant      │ Medium     │  5.8  │ 5.0–7.0 │ ✅ Good
    English    │ Easy–Med   │  4.8  │ 4.5–6.5 │ ✅ Good
    Reasoning  │ Hard       │  7.2  │ 5.5–7.5 │ ✅ Acceptable (high)
    GK / CA    │ Very Hard  │  8.8  │ 4.0–6.0 │ 🔴 Too Hard (out of range)
    ───────────┴────────────┴───────┴─────────┴──────────────────────

  GK FLAG: Difficulty 8.8 is outside target range (4.0–6.0).
    Cause: 8 questions from Feb–Mar 2026 CA period not yet covered in class
    Resolution: 2 questions marked as bonus (Q58, Q61) — scores recalculated ✅
    Remaining 6 GK questions: syllabus items not covered yet — noted for rebalancing
```

---

## 2. Question Difficulty Distribution

```
QUESTION DIFFICULTY DISTRIBUTION — Full Mock #25 (100 Questions)

  Intended vs Actual (post-test recalibration):

  Difficulty Band │ Intended │ Actual │ Diff  │ Flag
  ────────────────┼──────────┼────────┼───────┼──────────────────────────────
  Easy (1–3)      │  25 Qs   │  22 Qs │  -3   │ ⚠️ Slightly fewer easy Qs
  Medium (4–6)    │  45 Qs   │  42 Qs │  -3   │ ⚠️ Slightly fewer medium Qs
  Hard (7–8)      │  22 Qs   │  24 Qs │  +2   │ ✅ Within tolerance
  Very Hard (9–10)│   8 Qs   │  12 Qs │  +4   │ 🔴 Too many very hard Qs
  ────────────────┴──────────┴────────┴───────┴──────────────────────────────

  TARGET DISTRIBUTION: 25/45/22/8 (Easy/Med/Hard/VH)
  ACTUAL DISTRIBUTION: 22/42/24/12
  → Paper skewed harder than intended; mainly driven by GK very-hard questions

  QUESTION CALIBRATION ACTION:
    • 4 VH GK questions reclassified to Hard for future bank tagging
    • 2 questions (Q58, Q61) retired from active bank (syllabus mismatch)
    • 6 questions flagged for replacement in next GK sprint paper
```

---

## 3. Comparative Difficulty (Mock Trend)

```
DIFFICULTY TREND — SSC CGL Full Mock Series (Last 5 Papers)

  Mock   │ Date     │ Difficulty │ Avg Score │ Pass Rate │ Notes
  ───────┼──────────┼────────────┼───────────┼───────────┼────────────────────
  #21    │ Feb 15   │   5.8      │  102.4    │   8.4%    │ Slightly easy
  #22    │ Feb 28   │   6.2      │  108.4    │  10.2%    │ Balanced ✅
  #23    │ Mar 15   │   6.0      │  118.4    │  12.8%    │ Balanced ✅
  #24    │ Mar 22   │   6.1      │  124.6    │  13.6%    │ Balanced ✅
  #25    │ Apr 5    │   6.4      │  106.4    │  14.2%    │ GK skew ⚠️

  ⚠️ Pass rate rose from 8.4% → 14.2% over 5 mocks:
    Partly reflects student improvement (+22.2 pts trend) ✅
    Partly reflects difficulty calibration — Mock #25 GK was harder → pass rate
    might have been higher with balanced GK (~15–16% estimated)

  ACTION: Next full mock (Mock #26, Apr 14) — target overall difficulty 6.0
  GK section: all questions from covered syllabus only (till Mar 31 CA)
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/tests/{tid}/paper-analysis/` | Full paper difficulty report |
| 2 | `GET` | `/api/v1/coaching/{id}/tests/{tid}/paper-analysis/questions/` | Per-question actual difficulty |
| 3 | `GET` | `/api/v1/coaching/{id}/test-series/{sid}/difficulty-trend/` | Difficulty trend across a series |
| 4 | `PATCH` | `/api/v1/coaching/{id}/tests/{tid}/paper-analysis/questions/{qid}/` | Update question difficulty tag |
| 5 | `POST` | `/api/v1/coaching/{id}/tests/{tid}/paper-analysis/retire/` | Retire questions from bank |

---

## 5. Business Rules

- Paper difficulty is measured on a 1–10 scale where 1 is trivially easy and 10 is impossible; the target for full mocks is 5.5–7.0 (medium-hard); papers below 5.5 are "too easy" — students score high, feel confident, but are not prepared for the actual exam's harder questions; papers above 7.0 (routinely) demoralise students and generate complaints; the target band simulates the typical SSC CGL paper which is characterised as medium-hard by most coaching institutions
- The actual difficulty score is calculated post-test from student performance data (correct%, time spent, skip rate) and overrides the intended difficulty set during question tagging; this post-hoc calibration is more accurate than pre-tagging; the difference between intended and actual difficulty for each question updates the question's difficulty tag in the bank; over time, this calibration makes the question bank's difficulty tags progressively more accurate
- GK difficulty calibration is inherently harder to control than other sections because GK covers current affairs; a question about a budget clause announced 3 weeks ago is easy for a student who read the news and very hard for one who didn't; the coordinator must audit every GK question against the "syllabus cut date" — the latest CA event the batch has been taught; any question beyond the cut date is excluded from scoring; this audit is mandatory before result publication (E-04)
- Paper difficulty analysis is shared with faculty after each test; the faculty who contributed questions to the paper see only the difficulty stats for their questions, not for other faculty's questions; the Academic Director sees the complete analysis; faculty whose questions consistently deviate from the intended difficulty (e.g., a question tagged "Medium" that 80% get wrong) receive calibration coaching to improve their difficulty estimation; this is a skill that improves with feedback
- The comparative difficulty trend over 5+ mocks is a quality indicator for the test design process; the trend should show difficulty consistency (between 5.5–7.0 for all mocks) and rising average scores (student improvement); if difficulty is consistent but scores are flat or declining, the teaching is the issue; if scores are rising partly because difficulty is declining, the trend is misleading; separating difficulty calibration from teaching effectiveness is the purpose of this analysis page

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division E*
