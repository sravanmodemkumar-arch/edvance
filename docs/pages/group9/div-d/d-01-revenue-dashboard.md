# D-01 — Revenue Dashboard

> **URL:** `/content-partner/revenue/dashboard/`
> **File:** `d-01-revenue-dashboard.md`
> **Priority:** P1
> **Roles:** Content Partner (own data) · EduForge Finance Team (all partners)

---

## 1. Monthly Revenue Summary

```
REVENUE DASHBOARD — Dr. Venkat Rao (Partner ID: CP-0472)
March 2026 | 18,500 questions in pool | Quality Score: 82/100

  ┌──────────────────────────────────────────────────────────────────────┐
  │  MARCH 2026 EARNINGS SUMMARY                                       │
  ├──────────────────────────────────────────────────────────────────────┤
  │                                                                     │
  │  Gross Revenue (usage-based)      :   Rs. 54,285                    │
  │  EduForge Commission (30%)        : - Rs. 16,285                    │
  │                                    ─────────────                    │
  │  Net Revenue (Partner Share 70%)  :   Rs. 38,000                    │
  │  TDS Deducted (10% u/s 194J)     : - Rs.  3,800                    │
  │                                    ─────────────                    │
  │  Payout Amount                    :   Rs. 34,200                    │
  │                                                                     │
  │  Payout Status: [PROCESSED]  Date: 08-Apr-2026  Ref: NEFT-20260408 │
  │  Bank: SBI Main Branch Visakhapatnam | A/c: 3456XXXXXXX789         │
  │                                                                     │
  ├──────────────────────────────────────────────────────────────────────┤
  │  FY 2025-26 (Apr 2025 – Mar 2026) CUMULATIVE                       │
  │  Total Gross: Rs. 6,51,214  |  Total Net: Rs. 4,55,850             │
  │  Total TDS:   Rs. 45,585    |  Total Paid Out: Rs. 4,10,400        │
  │  Pending (Mar 2026 payout):  Rs. 34,200  [Scheduled: 08-Apr-2026]  │
  └──────────────────────────────────────────────────────────────────────┘
```

---

## 2. Revenue Trend (6-Month View)

```
MONTHLY REVENUE TREND — Dr. Venkat Rao

  Rs.
  60,000 ┤
  54,000 ┤                                              ████  54,285
  48,000 ┤                          ████  49,100  ████  ████
  42,000 ┤              ████  ████  ████          ████  ████
  36,000 ┤  ████  ████  ████  ████  ████  ████   ████  ████
  30,000 ┤  ████  ████  ████  ████  ████  ████   ████  ████
  24,000 ┤  ████  ████  ████  ████  ████  ████   ████  ████
  18,000 ┤  ████  ████  ████  ████  ████  ████   ████  ████
  12,000 ┤  ████  ████  ████  ████  ████  ████   ████  ████
   6,000 ┤  ████  ████  ████  ████  ████  ████   ████  ████
       0 ┼──Oct───Nov───Dec───Jan───Feb───Mar──────────────
          34,120 36,800 42,550 45,200 49,100 54,285  (Gross)
          23,884 25,760 29,785 31,640 34,370 38,000  (Net)

  [+] Month-on-Month Growth: +10.5% (Feb → Mar)
  [+] 6-Month Avg Gross: Rs. 43,676/month
  [i] Trend: Upward — content adoption increasing across 3 new TSPs
```

---

## 3. Content-wise Revenue Breakdown

```
REVENUE BY CONTENT CATEGORY — March 2026

  ┌─────┬───────────────────────────────────┬────────┬────────┬──────────┐
  │  #  │ Content Category                  │ Qs Used│ Gross  │ Share %  │
  ├─────┼───────────────────────────────────┼────────┼────────┼──────────┤
  │  1  │ APPSC Group 2 — General Studies   │  4,200 │ 14,820 │  27.3%   │
  │  2  │ TSPSC Group 1 — Indian Polity     │  3,800 │ 12,540 │  23.1%   │
  │  3  │ SSC CGL — Quantitative Aptitude   │  3,100 │  9,920 │  18.3%   │
  │  4  │ APPSC Group 1 — Indian Economy    │  2,600 │  7,280 │  13.4%   │
  │  5  │ IBPS PO — Reasoning Ability       │  2,400 │  5,425 │  10.0%   │
  │  6  │ Other (7 exam categories)         │  2,400 │  4,300 │   7.9%   │
  ├─────┴───────────────────────────────────┼────────┼────────┼──────────┤
  │  TOTAL                                  │ 18,500 │ 54,285 │ 100.0%   │
  └─────────────────────────────────────────┴────────┴────────┴──────────┘

  Top Performing Question (by attempts):
  Q-ID: Q-28471 "Which Article grants Right to Constitutional Remedies?"
  Attempts: 1,24,000 | Revenue Contribution: Rs. 2,480 | Used by 6 TSPs
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|--------|----------|-------------|
| 1 | `GET` | `/api/v1/content-partner/revenue/dashboard/` | Current month revenue summary for authenticated partner |
| 2 | `GET` | `/api/v1/content-partner/revenue/dashboard/trend/?months=6` | Monthly revenue trend for specified period |
| 3 | `GET` | `/api/v1/content-partner/revenue/dashboard/breakdown/?month=2026-03` | Content-wise revenue breakdown for a given month |
| 4 | `GET` | `/api/v1/content-partner/revenue/dashboard/cumulative/?fy=2025-26` | FY cumulative earnings summary |
| 5 | `GET` | `/api/v1/content-partner/revenue/dashboard/top-questions/?month=2026-03&limit=10` | Top revenue-generating questions |

---

## 5. Business Rules

- The revenue dashboard is the first screen a content partner sees after login, and it must load within 2 seconds even for partners with 50,000+ questions in the pool; the gross revenue figure is computed by summing per-question usage across all TSPs and institutions that licensed the partner's content during the billing month, applying the rate of Rs. 0.02 per student per question per month weighted by actual usage (if a student attempted the question at least once during the month, it counts as one usage unit); the dashboard caches the current month's running total and refreshes every 4 hours from the usage pipeline, while the previous month's figures are frozen on the 1st of the next month and never recalculated unless a dispute is upheld.

- The EduForge commission rate displayed on the dashboard is determined by the partner's quality score at the time of monthly settlement; a partner with a quality score above 85 receives the top-tier rate of 25% commission (75% partner share), while partners at or below 85 receive the standard 30% commission (70% partner share); Dr. Venkat Rao's current quality score of 82 places him in the standard tier, meaning his March 2026 gross of Rs. 54,285 yields a net of Rs. 38,000 after 30% commission; should his quality score improve to 86 next month, the same gross would yield Rs. 40,714 instead, and the dashboard must clearly show the applicable tier and the commission percentage so the partner understands the deduction.

- Month-on-month comparison and trend visualisation are essential for partner retention because they demonstrate that consistent content contribution leads to growing revenue; the 6-month trend chart shows both gross and net figures, and the month-on-month growth percentage is calculated as ((current_month_net - previous_month_net) / previous_month_net) * 100; a negative trend triggers an advisory banner suggesting the partner review content quality, update outdated questions, or add questions for newly announced exams; the platform never hides a declining trend — transparency in earnings builds trust with partners who treat content creation as a professional income source.

- The content-wise breakdown table attributes revenue to each exam category based on the exam tags of the questions used; a single question tagged to both APPSC Group 2 and TSPSC Group 1 may generate revenue from both exam pools, and the breakdown shows this correctly by splitting the usage count by source TSP and exam; the top-performing question highlight helps partners understand which type of content generates the most revenue (high-attempt questions on fundamental topics like Constitutional Remedies tend to outperform niche questions), guiding them to create more content in high-demand areas without sacrificing coverage of the full syllabus.

---

*Last updated: 2026-03-31 · Group 9 — B2B Content Partner Portal · Division D*
