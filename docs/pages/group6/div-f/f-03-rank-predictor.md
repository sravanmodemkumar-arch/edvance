# F-03 — Rank & Score Predictor

> **URL:** `/exam/{slug}/predict/`
> **File:** `f-03-rank-predictor.md`
> **Priority:** P1
> **Data:** `mock_attempt` (user's performance) + `cut_off` (historical) + `exam_cycle` (applicant counts)

---

## 1. Rank Predictor

```
RANK & SCORE PREDICTOR — {exam.name}
[Example: APPSC Group 2 — 2025]

  YOUR INPUT:
    Method: (●) From my mock scores  (○) Enter estimated score manually
    Mock data: 14 mocks, avg 124/150, trend +2/mock

  ┌──────────────────────────────────────────────────────────────────────┐
  │  PREDICTION RESULT                                                   │
  │                                                                      │
  │  Your projected Prelims score:    136–140 / 150                      │
  │  Projected cut-off (General):     76–82 / 150                        │
  │  Your margin above cut-off:       +54 to +64 marks ✅✅               │
  │  Probability of clearing Prelims: 98.4%                              │
  │                                                                      │
  │  Projected EduForge rank:         ~1,200 / 4,28,000                  │
  │  Estimated actual exam rank:      ~2,400–3,600 / 8,00,000 applicants│
  │  (EduForge users are self-selected — actual rank is typically 2–3×)  │
  │                                                                      │
  │  FINAL MERIT PROJECTION (if Mains performance is proportional):     │
  │  Estimated Mains score:           310–340 / 600                      │
  │  + Interview (avg):                40–50 / 75                         │
  │  Estimated final score:           350–390 / 675                      │
  │  Required for selection (General): ~298 / 675 (2022 cycle)          │
  │  Selection probability:           82–90% ✅                          │
  │                                                                      │
  │  ⚠️ Predictions are statistical estimates based on historical data   │
  │  and your mock performance. Actual results may vary significantly.   │
  └──────────────────────────────────────────────────────────────────────┘

  WHAT-IF SCENARIOS:
    If I improve by 10 marks → Selection probability: 94–97%
    If I maintain current level → 82–90% (as above)
    If exam is harder than average → Selection probability: 72–80%
```

---

## 2. Prediction Model

```
PREDICTION ENGINE — How it works

  INPUTS:
    User's mock scores (last 5 mocks) → compute trend line + projected score
    Historical cut-offs (last 3–4 cycles) → compute cut-off trend
    Historical applicant counts → estimate competition level
    EduForge-to-actual rank multiplier → calibrated from known EduForge user results

  COMPUTATION:
    1. SCORE PROJECTION:
       Linear regression on user's mock scores → extrapolate to exam date
       Confidence interval: ±1 standard deviation of score variance

    2. CUT-OFF PROJECTION:
       Linear regression on historical cut-offs → extrapolate to current cycle
       Adjusted for: estimated applicant count change, exam difficulty indicator

    3. RANK ESTIMATION:
       EduForge mock rank → multiply by 2–3× (calibration factor)
       Calibration: In 2022 APPSC Group 2, EduForge rank 1,200 corresponded
       to actual rank ~3,000 (verified from users who shared their results)

    4. SELECTION PROBABILITY:
       P(selection) = P(score > projected_cutoff)
       Using normal distribution of user's score variance around projected score
       Result: probability as percentage (e.g., 82–90%)
```

---

## 3. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `POST` | `/api/v1/exam/{slug}/predict/` | Run prediction (from mock data or manual input) |
| 2 | `POST` | `/api/v1/exam/{slug}/predict/what-if/` | What-if scenario (change in score) |

---

## 5. Business Rules

- The rank predictor is EduForge's most psychologically impactful feature; it gives aspirants a concrete probability of success which directly affects their motivation, study intensity, and exam strategy; a prediction of "98% probability of clearing Prelims" is reassuring but risks complacency; a prediction of "42% probability" creates urgency; the system must be accurate enough that aspirants trust it, but transparent enough that they understand it is an estimate — overconfident predictions that turn out wrong destroy trust permanently
- The EduForge-to-actual rank multiplier (2–3×) acknowledges that EduForge users are not representative of the full exam applicant pool; EduForge users are self-selected (they proactively use a preparation platform) and therefore tend to perform above the overall average; a user ranked 1,200th among 4.28 lakh EduForge users will likely rank ~3,000th among 8 lakh total applicants because the bottom half of applicants (casual or unprepared) are not on EduForge; the multiplier is calibrated from post-result data where EduForge users voluntarily shared their actual exam rank
- What-if scenarios prevent the predictor from being a single static number; "If I improve by 10 marks, my selection probability goes from 82% to 94%" directly motivates the aspirant to work for that improvement; "If the exam is harder than average, probability drops to 72%" manages expectations for variable exam difficulty; the what-if scenarios use the same model with adjusted inputs — they are not separate predictions but parameter variations of the same computation
- The prediction explicitly does NOT guarantee outcomes; the disclaimer "Actual results may vary significantly" is not legal boilerplate — it is a genuine warning; exam difficulty, the specific question set on exam day, the aspirant's mental state during the exam, and thousands of random factors can push the actual result outside the predicted range; an aspirant who sues EduForge because "the predictor said 98% and I didn't clear" should find the disclaimer prominently displayed at the point of prediction
- Mains score projection ("310–340/600") for exams with subjective Mains papers (APPSC Group 1, TSPSC Group 1 — essay-type) is inherently less reliable than Prelims prediction (objective MCQ — directly comparable to mocks); the system applies a wider confidence interval for Mains predictions and notes: "Mains prediction is less reliable because your mock tests are MCQ-based, while Mains is descriptive — prepare for potential variance"

---

*Last updated: 2026-03-31 · Group 6 — Exam Domain Portal · Division F*
