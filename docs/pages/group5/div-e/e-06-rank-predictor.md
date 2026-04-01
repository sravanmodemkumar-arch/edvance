# E-06 — Rank Predictor

> **URL:** `/coaching/tests/rank-predictor/`
> **File:** `e-06-rank-predictor.md`
> **Priority:** P2
> **Roles:** Test Series Coordinator (K4) · Academic Director (K5) · Student (read-only via O-01)

---

## 1. Individual Rank Prediction

```
RANK PREDICTOR — TCC-2401 Akhil Kumar (SSC CGL Morning)
Based on: Last 5 Full Mocks + Historical SSC CGL data (2019–2025)

  RECENT MOCK SCORES:
    Mock #25 (Apr 5):   186/200 — Rank 1/1,183 (TCC)
    Mock #24 (Mar 22):  178/200 — Rank 2/1,183
    Mock #23 (Mar 15):  178/200 — Rank 1/1,183
    Mock #22 (Feb 28):  172/200 — Rank 1/1,183
    Mock #21 (Feb 15):  168/200 — Rank 2/1,183

  TREND: +18 pts over last 5 mocks ✅ Strong improvement

  PREDICTED RANGE (SSC CGL 2025 Tier-I):
    ┌───────────────────────────────────────────────────────────────────────────┐
    │  Expected Score:  148 – 162 / 200                                        │
    │  TCC Difficulty Calibration:  × 0.92 (TCC mocks are ~8% harder)         │
    │  Adjusted Prediction:  171 / 200                                         │
    │  Estimated National Rank:  800 – 2,200 (out of ~25 lakh candidates)     │
    │  Probability of clearing Tier-I:  94%  ✅                                │
    │  Probability of final selection (CSS/IT Inspector):  72%  ✅             │
    └───────────────────────────────────────────────────────────────────────────┘

  WEAK AREAS (impact on rank if improved):
    Caselet DI (current 68%) → if 85%: +4 pts → rank moves up ~200 positions
    Input-Output (current 62%) → if 80%: +3 pts → rank moves up ~150 positions

  Disclaimer: Predictions are based on historical data. Actual results depend on
  paper difficulty, normalisation, and candidate pool. Not a guarantee.
```

---

## 2. Batch Rank Prediction Summary

```
BATCH RANK PREDICTION — SSC CGL MORNING (Apr 2026)
Based on Mock #25 scores | 1,183 students analysed

  TIER-I CLEARING PROBABILITY:
    > 90% probability:  168 students  (14.2%)  ← strong candidates
    60–90% probability: 348 students  (29.4%)  ← preparation gap closeable
    30–60% probability: 386 students  (32.6%)  ← need significant improvement
    < 30% probability:  281 students  (23.8%)  ← high risk (crash course needed?)

  SCORE NEEDED TO CLEAR (estimated cutoff: 145/200):
    Currently above 145:    168 students (14.2%)
    Need 1–15 more marks:   248 students (20.9%)  ← actionable with 4 weeks
    Need 16–30 more marks:  318 students (26.9%)  ← hard but possible
    Need > 30 more marks:   449 students (37.9%)  ← need extended preparation

  ACTION FOR COORDINATOR:
    → Schedule targeted sessions for "need 1–15 more marks" group (248 students)
    → Counselling for "< 30% probability" group (281 students): discuss extending course

  [Export Group List]   [Send Targeted SMS]   [Create Intervention Batch]
```

---

## 3. Rank Predictor Settings (Calibration)

```
RANK PREDICTOR CALIBRATION — Admin / Academic Director

  DIFFICULTY MULTIPLIER:
    TCC mocks vs SSC actual (based on 3 years of result comparison):
      2023 cohort: TCC avg 112 → actual avg 103.2 → multiplier: 0.921
      2024 cohort: TCC avg 118 → actual avg 108.4 → multiplier: 0.919
      2025 cohort: TCC avg 106 → actual avg  97.8 → multiplier: 0.923
      Current multiplier applied: × 0.921 (last updated: Mar 2026)

  HISTORICAL CUTOFF DATA:
    SSC CGL 2024 Tier-I cutoff (General):  148.75
    SSC CGL 2023 Tier-I cutoff (General):  143.25
    SSC CGL 2022 Tier-I cutoff (General):  140.50
    Trend adjustment: +2.5 pts/year (applied to 2025 estimate = 145)

  CANDIDATE POOL ASSUMPTION:
    Expected 2025 applicants: 28 lakh (used for percentile calculation)
    Last updated: Based on SSC notification Oct 2025

  [Update Multiplier]   [Add Cutoff Year]   [Recalculate All Predictions]
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/tests/rank-predictor/student/{sid}/` | Individual student rank prediction |
| 2 | `GET` | `/api/v1/coaching/{id}/tests/rank-predictor/batch/{bid}/` | Batch-level rank distribution |
| 3 | `GET` | `/api/v1/coaching/{id}/tests/rank-predictor/config/` | Calibration settings |
| 4 | `PATCH` | `/api/v1/coaching/{id}/tests/rank-predictor/config/` | Update multiplier or cutoff data |
| 5 | `GET` | `/api/v1/coaching/{id}/tests/rank-predictor/batch/{bid}/intervention-list/` | Students in each probability band |

---

## 5. Business Rules

- The rank predictor output is explicitly labelled as a prediction with a confidence range, not a guarantee; coordinators who present the rank predictor's output to students as a firm prediction ("you will definitely clear at this score") create false expectations; TCC's policy requires coordinators to always share the disclaimer text alongside any rank prediction; the disclaimer is mandatory in printed and digital form; a student who fails despite a high predicted probability cannot hold TCC legally liable if the disclaimer was acknowledged
- The difficulty multiplier (TCC mocks ≈ 8% harder than the actual exam) is recalibrated annually after SSC results are declared; it is updated by the Academic Director after comparing the previous year's cohort TCC average with their actual exam performance; the multiplier prevents students from feeling deflated by lower TCC mock scores — a student scoring 106/200 on a TCC mock may score 115 on the actual exam; communicating this multiplier to students is part of the Academic Director's monthly briefing
- The "intervention list" (students needing 1–15 more marks) is the highest-priority group for targeted coaching; these students are close to the cutoff and a focused effort on their specific weak areas can push them over; the coordinator uses this list to schedule remedial sessions, assign targeted topic tests, and increase counsellor interaction; this group represents the best ROI for TCC's teaching effort in the final 4 weeks before the exam
- Rank predictor data (individual student predicted rank) is visible to the student themselves in the Student Portal (O-01) and to the coordinator and Academic Director; it is not visible to other students, parents (except for minor students), or faculty; a student's predicted rank is sensitive personal data — knowing another student's predicted rank could create unhealthy competition or demoralization; this access restriction enforces DPDPA 2023 data minimisation
- The batch-level prediction (14.2% > 90% probability) is a key performance indicator for the branch; if the year-end result shows significant deviation from the predicted rates (e.g., only 8% cleared despite 14.2% at 90%+ probability), the Academic Director investigates whether the calibration was off, whether the exam was unusually hard, or whether teaching quality declined; this post-mortem drives calibration updates for the next year's cohort

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division E*
