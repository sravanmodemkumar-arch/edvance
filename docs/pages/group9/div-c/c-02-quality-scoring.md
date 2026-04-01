# C-02 — Quality Scoring & Metrics

> **URL:** `/content-partner/quality/scores/` (partner view) · `/internal/quality/scores/` (admin view)
> **File:** `c-02-quality-scoring.md`
> **Priority:** P1
> **Roles:** Content Partner (author) · EduForge Editor (reviewer) · EduForge QA Lead (final approval)

---

## 1. Per-Question Quality Score Breakdown

```
QUALITY SCORE — Question QID-884210
Batch: BTH-2026-03-28-00472-017 | Partner: Dr. Venkat Rao | Subject: Quant

  Question: A train 240m long crosses a pole in 16 seconds. How long
  will it take to cross a platform 360m long?
  Answer: (B) 40 sec | Difficulty: 3/5 | Exam Tag: SSC CGL

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  QUALITY SCORE: 86 / 100                                               │
  │                                                                        │
  │  COMPONENT            WEIGHT    RAW     WEIGHTED    DETAIL             │
  │  ─────────────────────────────────────────────────────────────────────  │
  │  Accuracy              40%      95/100   38.0       Answer key correct;│
  │                                                     explanation has    │
  │                                                     complete working   │
  │                                                                        │
  │  Clarity               20%      90/100   18.0       No ambiguity;      │
  │                                                     all options are    │
  │                                                     distinct values    │
  │                                                                        │
  │  Difficulty            15%      70/100   10.5       Tagged 3/5 but     │
  │  Calibration                                        actual p-value     │
  │                                                     0.72 (easy side);  │
  │                                                     slight miscalib.   │
  │                                                                        │
  │  Discrimination        15%      80/100   12.0       D-index = 0.38    │
  │  Index                                              (good); top-27%   │
  │                                                     got it right 85%   │
  │                                                     vs bottom-27% 47% │
  │                                                                        │
  │  Student Feedback      10%      75/100    7.5       4,200 attempts;    │
  │                                                     12 reports (3      │
  │                                                     "too easy", 9      │
  │                                                     "good question")   │
  │                                                                        │
  │  ─────────────────────────────────────────────────────────────────────  │
  │  TOTAL                100%               86.0                          │
  │                                                                        │
  │  VERDICT: HIGH QUALITY — eligible for featured mock tests              │
  └─────────────────────────────────────────────────────────────────────────┘

  QUALITY THRESHOLDS:
  90-100  EXCEPTIONAL — featured in "Top Questions" + premium mocks
  75-89   HIGH        — included in all mock pools
  60-74   ACCEPTABLE  — included but flagged for improvement
  40-59   BELOW PAR   — removed from active pool, partner notified
  0-39    REJECTED    — question retired, partner quality alert
```

---

## 2. Partner Aggregate Quality Dashboard

```
PARTNER QUALITY DASHBOARD — Dr. Venkat Rao (CP-00472)
Organisation: QuizCraft Edu Pvt Ltd | Tier: Gold | Since: 2024-06-15

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  AGGREGATE QUALITY SCORE: 88.4 / 100    Rank: #12 of 340 partners     │
  │                                                                        │
  │  COMPONENT AVERAGES (across 2,840 live questions):                     │
  │  Accuracy ............ 93.2  ████████████████████░░  (weight 40%)      │
  │  Clarity ............. 89.7  █████████████████████░  (weight 20%)      │
  │  Diff. Calibration ... 78.4  ███████████████░░░░░░  (weight 15%)      │
  │  Discrimination ...... 82.1  ████████████████░░░░░  (weight 15%)      │
  │  Student Feedback .... 84.6  █████████████████░░░░  (weight 10%)      │
  │                                                                        │
  │  TREND (last 6 months):                                                │
  │  Oct 85.2 → Nov 86.1 → Dec 87.0 → Jan 87.8 → Feb 88.1 → Mar 88.4   │
  │  Direction: IMPROVING (+3.2 over 6 months)                             │
  │                                                                        │
  │  TIER IMPACT:                                                          │
  │  Current tier: Gold (score >= 85) | Revenue share: 75%                 │
  │  Next tier: Platinum (score >= 92) | Revenue share: 78%                │
  │  Gap to Platinum: +3.6 points — focus on Difficulty Calibration        │
  │                                                                        │
  │  CONTENT BREAKDOWN:                                                    │
  │  ┌──────────────────┬──────┬───────┬────────────┐                      │
  │  │ Subject          │ Qs   │ Score │ Trend      │                      │
  │  ├──────────────────┼──────┼───────┼────────────┤                      │
  │  │ Quant Aptitude   │ 1,420│ 90.1  │ +1.2       │                      │
  │  │ Reasoning        │   680│ 87.3  │ +0.8       │                      │
  │  │ English Language  │   440│ 86.2  │ +2.1       │                      │
  │  │ General Awareness │   300│ 84.8  │ -0.3       │                      │
  │  └──────────────────┴──────┴───────┴────────────┘                      │
  │                                                                        │
  │  FEATURED: "Top Contributors" page — YES (rank <= 20)                  │
  │  MARKETPLACE VISIBILITY: BOOSTED (score >= 85 gets 1.5x weight)       │
  └─────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Discrimination Index Deep Dive (IRT Analysis)

```
DISCRIMINATION INDEX — Question QID-884210
Item Response Theory (IRT) Analysis | 4,200 student attempts

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  ITEM STATISTICS:                                                      │
  │  p-value (facility): 0.72  (72% got it correct — moderately easy)     │
  │  D-index:            0.38  (good discrimination)                       │
  │  Point-biserial r:   0.41  (strong positive correlation with total)   │
  │                                                                        │
  │  RESPONSE DISTRIBUTION:                                                │
  │  Option A (36 sec):   8.2%  ░░░░                                      │
  │  Option B (40 sec):  72.1%  ████████████████████████████████████  *    │
  │  Option C (42 sec):  11.4%  ██████                                    │
  │  Option D (48 sec):   7.1%  ████                                      │
  │  Unattempted:         1.2%  ░                                          │
  │  * = correct answer                                                    │
  │                                                                        │
  │  TOP vs BOTTOM 27% COMPARISON:                                         │
  │  ┌──────────┬──────────┬──────────┬──────────┬──────────┐             │
  │  │ Group    │ Opt A    │ Opt B *  │ Opt C    │ Opt D    │             │
  │  ├──────────┼──────────┼──────────┼──────────┼──────────┤             │
  │  │ Top 27%  │   2.1%   │  85.4%   │   8.3%   │   3.1%   │             │
  │  │ Bot 27%  │  14.8%   │  47.2%   │  21.6%   │  14.2%   │             │
  │  └──────────┴──────────┴──────────┴──────────┴──────────┘             │
  │  D-index = 0.854 - 0.472 = 0.382                                      │
  │                                                                        │
  │  INTERPRETATION:                                                       │
  │  Strong students (top 27%) overwhelmingly select the correct answer.  │
  │  Weak students (bottom 27%) are distributed across distractors,       │
  │  especially C (42 sec — common error: forgetting to add train length) │
  │  and A (36 sec — divides 360 by 10 instead of 600 by 15).            │
  │  This question discriminates well between prepared and unprepared     │
  │  students. D-index >= 0.30 is considered good.                        │
  │                                                                        │
  │  QUALITY RATING FOR THIS COMPONENT: 80/100 (good, not exceptional)   │
  └─────────────────────────────────────────────────────────────────────────┘
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|--------|----------|-------------|
| 1 | `GET` | `/api/v1/content-partner/quality/scores/questions/{qid}/` | Per-question quality score with component breakdown |
| 2 | `GET` | `/api/v1/content-partner/quality/scores/batches/{batch_id}/` | Batch-level aggregate quality score |
| 3 | `GET` | `/api/v1/content-partner/quality/scores/partners/{partner_id}/` | Partner aggregate score with trend and subject breakdown |
| 4 | `GET` | `/api/v1/content-partner/quality/scores/partners/{partner_id}/history/` | Monthly quality score history for trend analysis |
| 5 | `GET` | `/api/v1/content-partner/quality/scores/questions/{qid}/irt/` | IRT statistics: p-value, D-index, point-biserial, response distribution |
| 6 | `GET` | `/api/v1/content-partner/quality/scores/leaderboard/` | Partner quality leaderboard (top contributors ranking) |
| 7 | `GET` | `/api/v1/content-partner/quality/scores/partners/{partner_id}/tier-impact/` | Current tier, revenue share, gap to next tier |
| 8 | `POST` | `/api/v1/content-partner/quality/scores/questions/{qid}/recalculate/` | Trigger score recalculation after new student data |

---

## 5. Business Rules

- The quality score is a weighted composite of five components: Accuracy (40%), Clarity (20%), Difficulty Calibration (15%), Discrimination Index (15%), and Student Feedback (10%). The weights reflect the relative importance of each dimension to the student's learning outcome. Accuracy carries the highest weight because a wrong answer key is the single most damaging defect — a student who memorises a wrong answer from EduForge's platform and reproduces it in the actual SSC CGL exam loses marks due to negative marking and loses trust in the platform. Clarity is second because an ambiguous question wastes the student's time and creates exam anxiety ("Did I misread the question or is it badly worded?"). The remaining three components — difficulty calibration, discrimination, and student feedback — are data-driven metrics that can only be computed after the question has been attempted by a sufficient number of students (minimum 500 attempts for statistical validity), so they start at a default value of 70/100 for newly published questions and are recalculated weekly as attempt data accumulates.

- A partner's aggregate quality score directly determines their tier and revenue share. Bronze tier (score below 70) receives a 65% revenue share, Silver tier (70-84) receives 70%, Gold tier (85-91) receives 75%, and Platinum tier (92-100) receives 78%. The tier is recalculated on the first of every month based on the trailing 90-day quality score across all live questions. A partner cannot game the system by submitting a few exceptional questions and many poor ones — the aggregate is a weighted average across all their live questions, so every low-quality question drags down the overall score. If a partner's score drops below their current tier threshold for two consecutive months, they are downgraded. Upgrades happen immediately when the monthly recalculation shows the partner has crossed the threshold. The tier also affects marketplace visibility: Gold and Platinum partners' content is boosted by a 1.5x weight factor in the content selection algorithm, meaning their questions are more likely to appear in premium mock tests.

- Difficulty Calibration measures how accurately the partner tags the difficulty level (1-5 scale) relative to the empirical p-value (facility index) observed after students attempt the question. A question tagged as difficulty 3 (medium) should have a p-value between 0.40 and 0.65. If the p-value is 0.88 (very easy) for a question tagged as difficulty 3, the calibration score for that question is penalised. The mapping is: difficulty 1 expects p-value 0.80-1.00, difficulty 2 expects 0.65-0.80, difficulty 3 expects 0.40-0.65, difficulty 4 expects 0.20-0.40, and difficulty 5 expects 0.00-0.20. A partner who consistently over-tags or under-tags difficulty causes problems for the mock test assembly algorithm, which selects questions based on target difficulty distribution. If mock tests end up too easy or too hard because of miscalibrated difficulty tags, students get an inaccurate assessment of their preparation level. Partners receive a monthly "Calibration Report" showing which questions have the largest gap between tagged and empirical difficulty, along with recommended re-tags.

- The Discrimination Index (D-index) measures how effectively a question differentiates between high-performing and low-performing students, derived from Item Response Theory. It is calculated by comparing the percentage of correct responses in the top 27% of scorers versus the bottom 27% on the same test. A D-index above 0.30 is considered good, above 0.40 is excellent, and below 0.15 indicates the question fails to discriminate (either too easy, too hard, or poorly constructed). Questions with a negative D-index (where weak students outperform strong students) are automatically flagged for review because this typically indicates a flawed answer key or a misleading question stem. The D-index component of the quality score awards 100/100 for D-index above 0.45, scales linearly from 50 to 100 for D-index between 0.20 and 0.45, and awards 0/100 for D-index below 0.10. This metric incentivises partners to write questions with well-constructed distractors that represent common student errors rather than obviously wrong options that every student can eliminate.

---

*Last updated: 2026-03-31 · Group 9 — B2B Content Partner Portal · Division C*
