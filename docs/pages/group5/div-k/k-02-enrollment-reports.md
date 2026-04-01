# K-02 — Enrollment & Admissions Reports

> **URL:** `/coaching/analytics/enrollment/`
> **File:** `k-02-enrollment-reports.md`
> **Priority:** P2
> **Roles:** Branch Manager (K6) · Director (K7) · Admissions Head (K4)

---

## 1. Enrollment Summary

```
ENROLLMENT REPORT — AY 2025–26
Toppers Coaching Centre | As of 31 March 2026

  BATCH-WISE ENROLLMENT:
    Batch                    │ Target │ Enrolled │ Util% │ Dropouts │ Net  │ Trend
    ─────────────────────────┼────────┼──────────┼───────┼──────────┼──────┼───────
    SSC CGL Morning          │  140   │   138    │ 98.6% │    3     │  135 │ ↑ +8%
    SSC CGL Evening          │  130   │   138    │106.3% │    2     │  136 │ ↑ +12%
    SSC CHSL (Morning)       │  120   │   112    │ 93.3% │    4     │  108 │ → 0%
    SSC MTS Afternoon        │  100   │    96    │ 96.0% │    1     │   95 │ ↑ +5%
    IBPS PO Batch A          │  130   │   124    │ 95.4% │    3     │  121 │ ↑ +7%
    IBPS Clerk (Evening)     │  120   │   118    │ 98.3% │    2     │  116 │ ↑ +9%
    RRB PO Morning           │  100   │    92    │ 92.0% │    2     │   90 │ ↓ -3%
    State PSC (Weekend)      │   60   │    54    │ 90.0% │    1     │   53 │ → 0%
    Online (SSC CGL)         │  200   │   196    │ 98.0% │    6     │  190 │ ↑ +15%
    Online (IBPS PO)         │  150   │   138    │ 92.0% │    4     │  134 │ ↑ +11%
    Foundation (Class 10+2)  │   80   │    76    │ 95.0% │    2     │   74 │ ↑ +4%
    Spoken English           │   60   │    58    │ 96.7% │    0     │   58 │ ↑ +6%
    ─────────────────────────┴────────┴──────────┴───────┴──────────┴──────┴───────
    TOTAL                    │ 1,390  │  1,340   │ 96.4% │   30     │ 1310 │ ↑ +9%

  ADDITIONAL (Franchise students enrolled via TCC test series): 500
  GRAND TOTAL ACTIVE STUDENTS: 1,840
```

---

## 2. Admissions Funnel

```
ADMISSIONS FUNNEL — AY 2025–26 (Full Year)

  Stage                     │  Count  │ Conversion │ vs LY
  ──────────────────────────┼─────────┼────────────┼───────
  Enquiries received        │  8,640  │    —       │ ↑ 14%
  Demo class attended       │  3,240  │  37.5%     │ ↑ 8%
  Counselling session done  │  2,180  │  67.3%     │ ↑ 12%
  Application submitted     │  1,920  │  88.1%     │ ↑ 5%
  Enrolled (fee paid)       │  1,840  │  95.8%     │ ↑ 9%
  ──────────────────────────┴─────────┴────────────┴───────

  LEAD SOURCES (enrolled students):
    Walk-in:            612  (33.3%)
    Online (website):   460  (25.0%)
    Alumni referral:    368  (20.0%)
    Student referral:   220  (12.0%)
    Social media:       110  ( 6.0%)
    Other:               70  ( 3.8%)

  TOP CONVERTING COUNSELLORS:
    Ms. Anitha R.:   conversion 68.4% (from counselling to enrollment)
    Mr. Rajan K.:    conversion 62.1%
    Ms. Deepa M.:    conversion 58.8%
```

---

## 3. Dropout Analysis

```
DROPOUT ANALYSIS — AY 2025–26

  Total dropouts (AY):   30 students (1.6% of enrolled)

  REASON BREAKDOWN:
    Reason                          │ Count │ %
    ────────────────────────────────┼───────┼────
    Got a job / selected in exam    │   8   │ 26.7%  ← POSITIVE reason
    Financial difficulty            │   7   │ 23.3%
    Relocated / personal reasons    │   6   │ 20.0%
    Dissatisfied with quality       │   4   │ 13.3%  ← Actionable
    Health issues                   │   3   │ 10.0%
    Switched to competitor          │   2   │  6.7%  ← Actionable
    TOTAL                           │  30   │ 100%

  ACTIONABLE DROPOUT RATE:
    (Dissatisfied + Competitor):    6 students (20% of dropouts = 0.3% of total)
    Target: < 0.5% total actionable dropout

  INTERVENTION OUTCOMES:
    Students counselled before dropout: 18 of 30
    Retained after counselling:          4 (22.2% save rate)
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/analytics/enrollment/?year=2025-26` | Enrollment summary by batch |
| 2 | `GET` | `/api/v1/coaching/{id}/analytics/enrollment/funnel/?period=AY2025-26` | Admissions funnel data |
| 3 | `GET` | `/api/v1/coaching/{id}/analytics/enrollment/dropout/?year=2025-26` | Dropout analysis with reasons |
| 4 | `GET` | `/api/v1/coaching/{id}/analytics/enrollment/sources/` | Lead source attribution |
| 5 | `GET` | `/api/v1/coaching/{id}/analytics/enrollment/counsellor-performance/` | Counsellor conversion rates |

---

## 5. Business Rules

- Batch utilisation above 100% (SSC CGL Evening at 106.3%) is an operational flag, not a success metric; over-capacity batches degrade quality — students cannot find seats, faculty cannot manage the group effectively, and test hall capacity may be exceeded; the Branch Manager must either open a new section or manage waitlists; accepting 138 students into a 130-seat batch is a short-term revenue decision with a long-term quality cost; the target range is 90–100% utilisation, not "as many as possible"
- Dropout reasons are categorised carefully: "Got a job" is a success event (the student achieved their goal); "Financial difficulty" is a welfare concern (referred to scholarship or EMI options); "Dissatisfied with quality" is an actionable quality issue that must be investigated; combining these into a single "dropout rate" without categorisation produces a misleading metric; TCC's 1.6% raw dropout rate sounds low, but understanding the 0.3% quality-related dropout is what drives improvement
- The admissions funnel conversion rates (37.5% enquiry-to-demo, 67.3% demo-to-counselling, 95.8% application-to-enrollment) are tracked monthly; a significant drop in any stage indicates a problem; if demo class attendance drops to 25%, the demo session quality or scheduling may need review; if application-to-enrollment drops to 80%, there may be a fee structure or payment convenience issue; the funnel is a diagnostic tool for the admissions process
- Lead source attribution (alumni 20%, student referrals 12%) determines where TCC's marketing investment should go; word-of-mouth (alumni + student referrals = 32%) outperforms paid social media (6%) in quality and cost; a new student referred by an alumnus has a higher enrollment completion rate and lower dropout rate than a cold walk-in; the marketing budget should be weighted toward alumni engagement and referral incentives, not just digital advertising
- Counsellor conversion rates are monitored to identify both high performers and those needing support; a counsellor with a 58.8% conversion rate is not underperforming if their average is 62% — but the variance should be investigated; high conversion counsellors are asked to share their approach (pitch, objection handling, demo quality) with lower performers in a peer learning session; conversion rates are not used punitively — they are a coaching and process improvement tool

---

*Last updated: 2026-03-31 · Group 5 — Coaching Portal · Division K*
