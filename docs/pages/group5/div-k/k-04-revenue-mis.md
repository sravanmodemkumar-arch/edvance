# K-04 — Revenue & Financial MIS

> **URL:** `/coaching/analytics/revenue/`
> **File:** `k-04-revenue-mis.md`
> **Priority:** P2
> **Roles:** Director (K7) · Branch Manager (K6) · Accounts Manager (K5)

---

## 1. Revenue Summary

```
REVENUE MIS — AY 2025–26
Toppers Coaching Centre | As of 31 March 2026

  MONTHLY REVENUE (₹ Lakhs):
    Month  │ Target │ Actual │ Variance │ Collection % │ New Admissions
    ───────┼────────┼────────┼──────────┼──────────────┼───────────────
    Apr-25 │  12.0  │  11.4  │  -0.6    │    85.2%     │  162
    May-25 │  12.5  │  12.8  │  +0.3    │    88.4%     │  284
    Jun-25 │  13.0  │  13.4  │  +0.4    │    89.6%     │  196
    Jul-25 │  12.0  │  11.8  │  -0.2    │    86.1%     │   84  (mid-yr)
    Aug-25 │  13.0  │  13.6  │  +0.6    │    91.2%     │  248
    Sep-25 │  12.5  │  12.2  │  -0.3    │    87.8%     │   72  (mid-yr)
    Oct-25 │  12.0  │  11.8  │  -0.2    │    86.3%     │   68  (mid-yr)
    Nov-25 │  12.5  │  12.4  │  -0.1    │    87.9%     │   76  (mid-yr)
    Dec-25 │  13.0  │  13.1  │  +0.1    │    88.5%     │   96  (new batch)
    Jan-26 │  13.5  │  13.6  │  +0.1    │    90.4%     │   88
    Feb-26 │  14.0  │  14.0  │   0.0    │    91.8%     │  108
    Mar-26 │  13.5  │  14.2  │  +0.7    │    92.3%     │  128
    ───────┴────────┴────────┴──────────┴──────────────┴───────────────
    YTD    │ 153.5  │ 154.3  │  +0.8    │    88.9%     │  1,610 (YTD)

  REVENUE BY STREAM:
    Tuition fees:       ₹128.4 L  (83.2%)
    Hostel fees:        ₹  14.8 L  ( 9.6%)
    Test series packages: ₹  6.2 L  ( 4.0%)
    Study material:     ₹   2.8 L  ( 1.8%)
    Certif./misc fees:  ₹   2.1 L  ( 1.4%)
    TOTAL:              ₹ 154.3 L
```

---

## 2. Cost & Profitability

```
PROFITABILITY MIS — AY 2025–26 YTD

  REVENUE:                        ₹154.3 L
  ─────────────────────────────────────────
  DIRECT COSTS:
    Faculty salaries:    ₹ 42.6 L  (27.6%)
    Hostel operations:   ₹  8.4 L  ( 5.4%)
    Study material:      ₹  4.2 L  ( 2.7%)
    Online platform:     ₹  3.6 L  ( 2.3%)
  ─────────────────────────────────────────
  GROSS PROFIT:          ₹ 95.5 L  (61.9%)

  OVERHEAD:
    Admin & support:     ₹ 12.4 L  ( 8.0%)
    Rent & utilities:    ₹ 10.8 L  ( 7.0%)
    Marketing:           ₹  6.2 L  ( 4.0%)
    Welfare programs:    ₹  6.82 L ( 4.4%)
    Technology:          ₹  4.4 L  ( 2.9%)
    Scholarships:        ₹  6.5 L  ( 4.2%)
  ─────────────────────────────────────────
  NET PROFIT (before tax): ₹ 48.38 L (31.4%)
  GST collected (remitted):₹ 14.2 L
  TDS obligations:         ₹  5.8 L

  PROFITABILITY vs LY:
    Revenue: ↑ 18.2%  │  Gross margin: ↑ 1.4 pp  │  Net margin: ↑ 2.1 pp
```

---

## 3. Outstanding & Recovery

```
OUTSTANDING DUES — 31 March 2026

  Ageing Bucket     │ Students │ Amount (₹L) │ % of Receivables
  ──────────────────┼──────────┼─────────────┼──────────────────
  0–30 days         │    62    │    8.4      │  47.9%
  31–60 days        │    28    │    4.8      │  27.4%
  61–90 days        │    10    │    2.2      │  12.6%
  >90 days          │     8    │    2.1      │  12.0%
  ──────────────────┴──────────┴─────────────┴──────────────────
  TOTAL OUTSTANDING │   108    │   17.5      │  100%

  COLLECTION EFFICIENCY:
    Target:          < ₹15L outstanding at month-end
    Actual:          ₹17.5L  ⚠️ (above target by ₹2.5L)
    Action:          Accounts team calling 31–60 day bucket (28 students)

  WRITE-OFF HISTORY (AY 2025–26):
    Amounts written off: ₹1.2 L (3 students — verified hardship post-exit)
    Write-off approval:  Director only (> ₹10,000 per case)
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/analytics/revenue/?year=2025-26` | Annual revenue summary |
| 2 | `GET` | `/api/v1/coaching/{id}/analytics/revenue/monthly/?from=2025-04&to=2026-03` | Month-wise revenue trend |
| 3 | `GET` | `/api/v1/coaching/{id}/analytics/revenue/profitability/` | P&L summary |
| 4 | `GET` | `/api/v1/coaching/{id}/analytics/revenue/outstanding/` | Outstanding dues ageing |
| 5 | `GET` | `/api/v1/coaching/{id}/analytics/revenue/streams/` | Revenue by stream breakdown |

---

## 5. Business Rules

- Revenue MIS separates revenue recognition from cash collection; revenue is recognised when service is delivered (monthly, proportional to the academic calendar), not when fees are received; a student who paid ₹60,000 upfront for a 10-month course contributes ₹6,000 per month to revenue recognition, regardless of when cash was received; this accounting treatment aligns with Ind AS and prevents misleading spikes in reported revenue from large upfront collections
- The net profit margin of 31.4% is healthy for a coaching centre of this scale but should not be maximised at the expense of quality investment; TCC's Director's philosophy is to reinvest 8% of revenue in welfare, scholarships, and faculty development (items that directly protect quality and brand); a coaching centre that cuts these costs to reach 40% margin will see quality decline within 2 years as faculty morale drops and student success stories reduce; margin targets must be balanced against quality investment
- GST compliance on coaching fees requires careful categorisation; pure educational coaching (SSC/banking exam prep) is exempt from GST under SAC 9992 for not-for-profit institutions; TCC as a private coaching centre charges GST at 18% on its fees; hostel services (SAC 9963) have separate treatment based on tariff per day; TCC files monthly GSTR-1 and GSTR-3B; the Revenue MIS captures GST collected and remitted separately to ensure the P&L reflects true economic performance (GST collected is a liability, not revenue)
- The outstanding dues ageing report (₹17.5 lakh total) distinguishes between students still enrolled (expected to pay) and those who have left without paying (bad debt risk); accounts team prioritises collection from enrolled students (0–60 days bucket) through reminder calls and EMI restructuring; students in the >90-day bucket who have left TCC are reviewed for escalation to legal notice or write-off based on the Director's assessment; legal recovery action for amounts below ₹5,000 is not cost-effective
- Revenue by stream analysis informs strategic decisions; hostel revenue (9.6%) at ₹14.8 lakh is significant but requires ₹8.4 lakh in operating costs — the hostel's contribution margin is only 43%; the test series package revenue (4%) is pure high-margin digital revenue with near-zero marginal cost; the Director uses stream analysis to consider whether expanding online test series subscriptions (to students outside TCC) could be a scalable revenue opportunity without proportional cost increase

---

*Last updated: 2026-03-31 · Group 5 — Coaching Portal · Division K*
