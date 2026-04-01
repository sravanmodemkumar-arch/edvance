# E-02 — Question Difficulty & Discrimination Analysis

> **URL:** `/content-partner/analytics/question-analysis/`
> **File:** `e-02-question-analysis.md`
> **Priority:** P2
> **Roles:** Content Partner (own content IRT metrics) · EduForge Content Team (quality oversight)

---

## 1. IRT Scatter Plot — Difficulty vs Discrimination

```
EDUFORGE — QUESTION DIFFICULTY & DISCRIMINATION ANALYSIS
Partner: Dr. Venkat Rao                        Exam: SSC CGL Tier 1 Quant
Questions Analysed: 7,200 (minimum 200 attempts each)

  DIFFICULTY (b) vs DISCRIMINATION (a) — IRT 2-Parameter Model

  a (discrimination)
  2.0 |                                            *
      |                                  *    *  *   *
  1.8 |                              *  *  * *  **
      |                          * * ** * ***  * *
  1.6 |                        * *** **** *** *
      |                      * ***** ******** *
  1.4 |                    * ****  IDEAL  **** *
      |                   * **** ZONE  ***** *
  1.2 |                  * ***** (62%) ****  *
      |                 * * **** ****** ** *
  1.0 |               *  * ** **** *** *  *
      |              *   * * ** ** ** *       *
  0.8 |            *    *  * *  * * *    *        *
      |           *       * *   *  *        *
  0.6 |         *          *  *    *              *          *
      |        *            *        *                 *
  0.4 |···*····················*·····························*··········
      |  *             *         *           LOW DISC.           *
  0.2 |      *     Q#4521*          *    ZONE (8.3%)     *
      | *          (0.12)     *               *               *
  0.0 +----+----+----+----+----+----+----+----+----+----+----+----+--
     -3.0 -2.5 -2.0 -1.5 -1.0 -0.5  0.0 +0.5 +1.0 +1.5 +2.0 +2.5 +3.0
                             b (difficulty)

  LEGEND:
  *  = Individual question (7,200 plotted)
  ··· = Discrimination threshold (a = 0.40) — below this line = flagged
  IDEAL ZONE: a > 0.5, b between -1.0 and +1.0 (62% of questions)
  LOW DISCRIMINATION ZONE: a < 0.40 (8.3% of questions = 598 flagged)
  TOO EASY: b < -2.0 (3.1% = 223 questions)
  TOO HARD: b > +2.0 (2.4% = 173 questions)

  DISTRIBUTION SUMMARY:
  ┌───────────────────────┬──────────┬──────────┐
  │ Zone                  │ Count    │ % of All │
  ├───────────────────────┼──────────┼──────────┤
  │ Ideal Zone            │   4,464  │   62.0%  │
  │ Acceptable (a > 0.4)  │   1,965  │   27.3%  │
  │ Low Discrimination    │     598  │    8.3%  │
  │ Too Easy (b < -2.0)   │     223  │    3.1%  │
  │ Too Hard (b > +2.0)   │     173  │    2.4%  │
  └───────────────────────┴──────────┴──────────┘
  Note: Categories overlap — a question can be both "Too Easy" and "Low Discrimination"
```

---

## 2. Flagged Questions — Low Discrimination Detail

```
FLAGGED QUESTIONS — LOW DISCRIMINATION (a < 0.40)
Sorted by discrimination index (ascending)        Showing 10 of 598

  ┌────────┬─────────────────────────────────┬───────┬───────┬────────┬──────────────────────┐
  │ Q#     │ Topic                           │ a     │ b     │ Acc.   │ Diagnosis            │
  ├────────┼─────────────────────────────────┼───────┼───────┼────────┼──────────────────────┤
  │ Q#4521 │ Profit & Loss                   │  0.12 │ -0.85 │ 89.4%  │ Too easy — even weak │
  │        │                                 │       │       │        │ students get it right│
  │ Q#6103 │ Number System                   │  0.15 │ +0.22 │ 58.3%  │ Random guessing      │
  │        │                                 │       │       │        │ pattern detected     │
  │ Q#2887 │ Percentage                      │  0.18 │ -1.42 │ 92.1%  │ Trivially easy —     │
  │        │                                 │       │       │        │ remove or raise diff │
  │ Q#5412 │ Ratio & Proportion              │  0.21 │ +2.34 │ 18.7%  │ Too hard — only top  │
  │        │                                 │       │       │        │ 5% get it right      │
  │ Q#3299 │ Time & Work                     │  0.23 │ -0.11 │ 63.2%  │ Ambiguous options —  │
  │        │                                 │       │       │        │ 2 close distractors  │
  │ Q#7810 │ SI / CI                         │  0.25 │ +0.88 │ 42.1%  │ Misleading stem —    │
  │        │                                 │       │       │        │ good students err    │
  │ Q#1456 │ Speed, Distance & Time          │  0.27 │ -0.33 │ 72.5%  │ Calculation-heavy —  │
  │        │                                 │       │       │        │ time pressure skews  │
  │ Q#4088 │ Mensuration                     │  0.30 │ +1.78 │ 28.9%  │ Missing diagram info │
  │        │                                 │       │       │        │ — guessing prevalent │
  │ Q#6521 │ Algebra                         │  0.33 │ -0.67 │ 78.4%  │ Straightforward —    │
  │        │                                 │       │       │        │ consider harder dist.│
  │ Q#2190 │ Geometry                        │  0.36 │ +2.61 │ 14.2%  │ Beyond syllabus —    │
  │        │                                 │       │       │        │ most skip or guess   │
  ├────────┴─────────────────────────────────┴───────┴───────┴────────┴──────────────────────┤
  │ [Load More (588 remaining)]                                                              │
  ├──────────────────────────────────────────────────────────────────────────────────────────┤
  │ BULK ACTIONS:  [Select All Visible]  [Retire Selected]  [Send to Recalibration Queue]   │
  └──────────────────────────────────────────────────────────────────────────────────────────┘

  RECALIBRATION SUGGESTIONS FOR Q#4521 (Profit & Loss, a=0.12, b=-0.85):
  ┌─────────────────────────────────────────────────────────────────────────┐
  │ Current: "A sells a book at 10% profit. Find selling price if          │
  │           cost is Rs. 200."                                             │
  │                                                                         │
  │ Problem: Single-step calculation. Even weak students apply              │
  │          SP = CP x (1 + profit%). No reasoning required.                │
  │                                                                         │
  │ Suggestion 1: Add a second transaction (A sells to B, B sells to C)    │
  │               Expected new difficulty: b = +0.3 to +0.6                 │
  │                                                                         │
  │ Suggestion 2: Introduce marked price and discount before profit calc   │
  │               Expected new difficulty: b = +0.5 to +0.8                 │
  │                                                                         │
  │ Suggestion 3: Change to "Find cost price given selling price and       │
  │               profit%" (reverse calculation)                            │
  │               Expected new difficulty: b = -0.2 to +0.2                 │
  │                                                                         │
  │ [Apply Suggestion 1]  [Apply Suggestion 2]  [Apply Suggestion 3]       │
  │ [Edit Manually]       [Retire Question]                                 │
  └─────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Difficulty Distribution & Calibration Health

```
DIFFICULTY DISTRIBUTION — Dr. Venkat Rao (All Exams, 18,500 Questions)

  Ideal bell-curve target shown as dotted line (···)

  Count
  3500 |
       |                      ___
  3000 |                     |   |
       |                ___  |   |  ___
  2500 |           ___ |   | |   | |   |
       |          |   ||   | |   | |   |
  2000 |     ···  |   ||   | |   | |   |  ···
       |    · ___ |   ||   | |   | |   | ___ ·
  1500 |   ·|   ||   ||   | |   | |   ||   |·
       |  · |   ||   ||   | |   | |   ||   | ·
  1000 | ·  |   ||   ||   | |   | |   ||   |  ·
       |·___|   ||   ||   | |   | |   ||   |___·
   500 ||   |   ||   ||   | |   | |   ||   |   |
       ||   |   ||   ||   | |   | |   ||   |   |___
     0 +|___|___|+___|___|_+___|___|+___|___|+___|___|+----
       -3   -2      -1       0       +1      +2      +3
                        Difficulty (b)

  ┌─────────────────────┬──────────┬──────────┬───────────────────┐
  │ Range               │ Count    │ Actual % │ Ideal Target %    │
  ├─────────────────────┼──────────┼──────────┼───────────────────┤
  │ Very Easy (< -2)    │   1,110  │    6.0%  │    5%             │
  │ Easy (-2 to -1)     │   2,775  │   15.0%  │   15%             │
  │ Medium-Easy (-1, 0) │   4,625  │   25.0%  │   25%             │
  │ Medium-Hard (0, +1) │   4,810  │   26.0%  │   25%             │
  │ Hard (+1 to +2)     │   3,330  │   18.0%  │   20%             │
  │ Very Hard (> +2)    │   1,850  │   10.0%  │   10%             │
  ├─────────────────────┼──────────┼──────────┼───────────────────┤
  │ TOTAL               │  18,500  │  100.0%  │  100%             │
  └─────────────────────┴──────────┴──────────┴───────────────────┘

  CALIBRATION HEALTH: GOOD
  Overall deviation from ideal curve: 2.1% (threshold: < 5% = GOOD)
  Action: Slight deficit in Hard (+1 to +2) range. Consider adding
          240 hard-level questions to SSC CGL Quant and IBPS Reasoning.
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|--------|----------|-------------|
| 1 | `GET` | `/api/v1/content-partner/analytics/irt/scatter/` | IRT scatter plot data (a, b values per question) |
| 2 | `GET` | `/api/v1/content-partner/analytics/irt/flagged/` | Flagged questions below discrimination threshold |
| 3 | `GET` | `/api/v1/content-partner/analytics/irt/distribution/` | Difficulty distribution histogram data |
| 4 | `GET` | `/api/v1/content-partner/analytics/irt/question/{question_id}/` | Single-question IRT detail with recalibration suggestions |
| 5 | `POST` | `/api/v1/content-partner/analytics/irt/recalibrate/` | Submit question to recalibration queue |
| 6 | `POST` | `/api/v1/content-partner/analytics/irt/bulk-retire/` | Retire multiple flagged questions |
| 7 | `GET` | `/api/v1/content-partner/analytics/irt/calibration-health/` | Difficulty distribution vs ideal curve deviation |
| 8 | `GET` | `/api/v1/content-partner/analytics/irt/export/` | Export IRT analysis as CSV or PDF |

---

## 5. Business Rules

- IRT parameters (difficulty b and discrimination a) are estimated using the two-parameter logistic model and are only computed for questions that have accumulated at least 200 unique student attempts; questions with fewer than 200 attempts display a "Calibrating..." status with a progress bar showing current attempt count vs the 200 threshold; Dr. Venkat Rao's 18,500 questions include approximately 14,820 that meet this threshold (they are active in live tests), while 3,680 archived questions retain their last-computed IRT parameters but are marked as "Historical — no longer in active rotation"; IRT parameters are recomputed weekly by the EduForge analytics pipeline using the most recent 90 days of attempt data, which means a question's difficulty and discrimination values evolve over time as the student population changes, and partners should expect small fluctuations (typically within 0.1 on both parameters) between weekly recalculations.

- The discrimination threshold for flagging is set at a = 0.40 by default, based on established psychometric standards where questions with discrimination below 0.40 are considered poor discriminators that fail to meaningfully separate high-ability from low-ability students; the EduForge Content Team can adjust this threshold per exam category — for instance, banking reasoning questions may have a slightly lower threshold of 0.35 because the item format (statement-assumption, syllogism) naturally yields lower discrimination due to the binary nature of logical reasoning, while quantitative aptitude questions typically achieve higher discrimination and may warrant a threshold of 0.45; partners are not able to modify these thresholds themselves but can view the active threshold for each exam category on the analysis page, and can appeal a flagging decision through the feedback mechanism if they believe the question is pedagogically sound despite low measured discrimination.

- Recalibration suggestions are generated by a rule-based engine that analyses the flagged question's stem, options, and response pattern to diagnose the likely cause of poor discrimination; the system identifies five primary failure patterns — trivially easy (b < -1.5 with a < 0.3, suggesting the question requires only a single obvious step), too hard (b > +2.0 with a < 0.3, suggesting even high-ability students resort to guessing), ambiguous distractors (two options receiving near-equal selection rates among the top 25% of students, suggesting both appear correct), misleading stem (high-ability students selecting a specific wrong option more frequently than low-ability students, suggesting a trick or poorly worded condition), and calculation-heavy (time-per-question more than 2x the topic average, suggesting the question tests speed rather than conceptual understanding); for Q#4521 in Dr. Venkat Rao's Profit & Loss set, the diagnosis is "trivially easy" and the system proposes three specific modifications ranked by expected difficulty shift, each with an estimated new b parameter based on similar questions in the pool.

- Partners can retire flagged questions individually or in bulk using the "Retire Selected" action, which immediately removes the question from all future test generation pools but preserves it in the partner's archive with full historical IRT data; retired questions do not count towards the partner's active question count for quality score calculation or revenue share tier eligibility; however, bulk retirement is capped at 500 questions per day to prevent partners from gaming the quality score by mass-retiring all poorly-performing questions right before a quarterly review — the system requires at least a 7-day gap between the flagging date and the retirement action for questions flagged as "Low Discrimination" to give partners adequate time to consider recalibration instead of retirement; the EduForge Content Team receives a notification when any partner retires more than 100 questions in a single week, triggering a content health review.

---

*Last updated: 2026-03-31 · Group 9 — B2B Content Partner Portal · Division E*
