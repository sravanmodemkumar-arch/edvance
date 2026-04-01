# F-05 — Result Analytics (Platform-Level)

> **URL:** `/admin/exam/results/analytics/`
> **File:** `f-05-result-analytics.md`
> **Priority:** P2
> **Data:** `exam_result` (shared by users) + `mock_attempt` — correlating mock performance with actual results

---

## 1. Mock-to-Actual Correlation

```
RESULT ANALYTICS — Admin / Content Team
How well do EduForge mocks predict actual exam performance?

  CORRELATION REPORT — TSPSC Group 2 — 2025 (42 confirmed results)

  MOCK PERFORMANCE vs ACTUAL RESULT:
    EduForge mock avg │ Actual Prelims │ Cleared? │ Correlation
    ──────────────────┼────────────────┼──────────┼────────────
    130–150 (top tier)│    92–112      │  42/42 ✅│  r = 0.84
    110–129 (strong)  │    78–96       │  38/42   │  Strong ✅
    90–109 (moderate) │    68–82       │  18/26   │  Moderate
    70–89 (developing)│    52–72       │   4/14   │  Weak
    <70 (low)         │    <58         │   0/8    │  Expected

  KEY INSIGHT:
    Students scoring 130+ on EduForge mocks: 100% Prelims clearance
    Correlation coefficient (mock avg → actual score): r = 0.84 ✅
    This validates: EduForge mock difficulty is well-calibrated to TSPSC Group 2

  CALIBRATION ADJUSTMENT:
    EduForge mock scores are ~18% higher than actual exam scores on average
    Mock avg 124/150 → Actual avg ~102/150 (ratio: 0.82)
    This ratio is used in the rank predictor (F-03) for calibration
```

---

## 2. Platform Impact Metrics

```
PLATFORM IMPACT — AY 2025–26

  EduForge users who shared actual exam results: 8,420 (voluntary)

  RESULTS BY EXAM:
    Exam                 │ Users shared │ Cleared │ Success Rate │ vs National
    ─────────────────────┼──────────────┼─────────┼──────────────┼───────────
    TSPSC Group 2 2025   │     42       │    38   │   90.5%      │ vs 20.1% *
    SSC CGL 2024         │    284       │   196   │   69.0%      │ vs 5.2% *
    APPSC Group 2 2022   │     86       │    62   │   72.1%      │ vs 4.8% *
    IBPS PO 2025         │    124       │    84   │   67.7%      │ vs 3.8% *
    AP Police Const 2025 │    168       │    96   │   57.1%      │ vs 13.4%*
    ─────────────────────┴──────────────┴─────────┴──────────────┴───────────
    * National success rate = qualified / total applied (from official data)
    ⚠️ Self-selection bias: users who share results are more likely to have cleared

  MARKETING SAFE CLAIM:
    "Among EduForge users who shared their results, X% cleared exam Y"
    NOT: "X% of EduForge users clear exam Y"
    (because users who didn't clear are less likely to share)
```

---

## 3. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/admin/exam/results/analytics/correlation/?exam={slug}` | Mock-to-actual correlation |
| 2 | `GET` | `/api/v1/admin/exam/results/analytics/impact/` | Platform impact metrics |
| 3 | `GET` | `/api/v1/admin/exam/results/analytics/calibration/?exam={slug}` | Calibration factor for predictor |

---

## 5. Business Rules

- The mock-to-actual correlation is the single most important quality metric for the mock test engine; a correlation coefficient of r = 0.84 means EduForge mocks strongly predict actual exam performance — this validates that the mock question quality, difficulty, and pattern accurately reflect the real exam; if the correlation drops below r = 0.70, it signals that mocks are either too easy, too hard, or testing the wrong topics; the content team reviews and recalibrates mock difficulty annually using this data
- Self-selection bias in result sharing must be communicated transparently; users who cleared the exam are 3–5× more likely to share their results than users who didn't; the "90.5% success rate among TSPSC Group 2 result sharers" does NOT mean 90.5% of all EduForge users cleared TSPSC Group 2; the actual success rate among all EduForge users is likely 40–60% (still higher than the national 20.1%, but not 90.5%); all published claims must use the phrasing "among users who shared their results" — anything else is misleading
- The calibration factor (EduForge mock ≈ 18% higher than actual exam) is used by the rank predictor (F-03) to adjust score projections; this factor varies by exam: SSC CGL mocks may be 12% easier than the actual exam (SSC is predictable); UPSC CSE mocks may be 25% easier (UPSC is highly unpredictable); the calibration is updated after each exam cycle when new actual result data is available; using a generic "one size fits all" calibration across all exams would produce inaccurate predictions
- The correlation data is also used to improve mock quality; if "AP Economy" questions in APPSC mocks have low correlation with actual AP Economy performance (students score high in mocks but low in actual exam on this topic), it means the mock questions are easier or differently focused than the actual exam; the content team responds by: reviewing actual exam questions (from PYQs), adjusting mock question difficulty, and adding questions that test the same cognitive level as the actual exam
- Platform impact metrics (success rates, correlation data, improvement trends) are shared with the product team to drive investment decisions; an exam where EduForge users have r = 0.90 correlation and 72% success rate (vs 5% national) is a strong validation of the content; an exam with r = 0.55 and 30% success rate needs investment in content quality; these metrics justify the content team's headcount and budget allocation to the business leadership

---

*Last updated: 2026-03-31 · Group 6 — Exam Domain Portal · Division F*
