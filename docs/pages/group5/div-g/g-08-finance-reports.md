# G-08 — Finance MIS & Reports

> **URL:** `/coaching/finance/reports/`
> **File:** `g-08-finance-reports.md`
> **Priority:** P1
> **Roles:** Accounts (K5) · Branch Manager (K6) · Director (K7)

---

## 1. Monthly Finance MIS

```
FINANCE MIS — March 2026
Toppers Coaching Centre, Hyderabad Main Branch
Generated: 31 March 2026, 11:00 PM

  ┌──────────────────────────────────────────────────────────────────────────────┐
  │  REVENUE: ₹ 62.2 L  │  EBITDA: ₹ 30.4 L  │  MARGIN: 48.9%  │  GST: ₹7.8L │
  └──────────────────────────────────────────────────────────────────────────────┘

  REVENUE BREAKDOWN:
    Enrollment fee collected:      ₹ 46,83,444  (75.3%)
    Test series packages:          ₹  7,92,248  (12.7%)
    Hostel revenue:                ₹  3,15,896   (5.1%)
    Franchise royalty:             ₹  4,28,400   (6.9%)
    ─────────────────────────────────────────────
    TOTAL REVENUE:                 ₹ 62,19,988  (100%)

  vs TARGET (March):
    Revenue target:  ₹ 58,00,000
    Achieved:        ₹ 62,19,988  (+7.2% above target) ✅

  vs PREVIOUS MONTH (February 2026):
    Feb revenue:     ₹ 54,80,000
    Mar revenue:     ₹ 62,19,988  (+13.5% MoM) ✅
    Reason:          Pre-batch enrollment surge (May 2026 batches filling up)

  OUTSTANDING RECEIVABLES:
    Instalment 2 (upcoming, Apr 2026):  ₹ 25,60,800  (262 students)
    Overdue (all aging):                ₹  5,87,200   (62 students)
    TOTAL RECEIVABLE:                   ₹ 31,48,000
```

---

## 2. Quarterly P&L Summary

```
QUARTERLY P&L — Q4 FY 2025–26 (Jan – Mar 2026)

                     │  Jan 2026    │  Feb 2026    │  Mar 2026    │  Q4 TOTAL
  ───────────────────┼──────────────┼──────────────┼──────────────┼──────────────
  Revenue            │ ₹  48.6 L   │ ₹  54.8 L   │ ₹  62.2 L   │ ₹ 165.6 L
  Faculty salaries   │ ₹  18.0 L   │ ₹  18.2 L   │ ₹  18.4 L   │ ₹  54.6 L
  Other salaries     │ ₹   4.1 L   │ ₹   4.2 L   │ ₹   4.2 L   │ ₹  12.5 L
  Rent & utilities   │ ₹   4.8 L   │ ₹   4.9 L   │ ₹   5.0 L   │ ₹  14.7 L
  Marketing          │ ₹   2.4 L   │ ₹   2.4 L   │ ₹   2.5 L   │ ₹   7.3 L
  Other expenses     │ ₹   1.6 L   │ ₹   1.7 L   │ ₹   1.7 L   │ ₹   5.0 L
  ───────────────────┼──────────────┼──────────────┼──────────────┼──────────────
  TOTAL EXPENSES     │ ₹  30.9 L   │ ₹  31.4 L   │ ₹  31.8 L   │ ₹  94.1 L
  EBITDA             │ ₹  17.7 L   │ ₹  23.4 L   │ ₹  30.4 L   │ ₹  71.5 L
  MARGIN             │   36.4%     │   42.7%     │   48.9%     │   43.2%
  ───────────────────┴──────────────┴──────────────┴──────────────┴──────────────
  FY 2025–26 Annual Revenue target:  ₹ 6.00 Cr
  FY 2025–26 Revenue (Apr 25–Mar 26):₹ 6.22 Cr ✅ (+3.7% above annual target)
```

---

## 3. Custom Report Builder

```
FINANCE REPORT BUILDER

  Report Type:   [Monthly P&L ▼]
  Period:        [1 Apr 2025] to [31 Mar 2026]  (Full FY)
  Branch:        [Hyderabad Main ▼]  (or All branches)
  Format:        (●) PDF  ( ) Excel  ( ) Dashboard view

  Include:
    [✓] Revenue by stream (enrollment, test series, hostel, royalty)
    [✓] Expense breakdown (salaries, rent, marketing, others)
    [✓] EBITDA and margin
    [✓] GST collected and paid
    [✓] Outstanding receivables (aging)
    [✓] Comparison vs budget / target
    [ ] Individual student fee details (restricted)
    [ ] Franchise branch breakdown (separate report)

  Access:  [Accounts + Branch Manager + Director ▼]
  Auto-send: [1st of every month to: director@tcc.in, branchmgr@tcc.in] ✅

  [Generate Report]   [Download FY 2025–26 Annual Report]
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/finance/reports/monthly/?month=2026-03` | Monthly finance MIS |
| 2 | `GET` | `/api/v1/coaching/{id}/finance/reports/quarterly/?quarter=Q4&year=2026` | Quarterly P&L |
| 3 | `GET` | `/api/v1/coaching/{id}/finance/reports/annual/?year=2025-26` | Annual P&L summary |
| 4 | `POST` | `/api/v1/coaching/{id}/finance/reports/custom/` | Generate custom finance report |
| 5 | `GET` | `/api/v1/coaching/{id}/finance/reports/receivables/` | Outstanding receivables aging |
| 6 | `GET` | `/api/v1/coaching/{id}/finance/reports/variance/?month=2026-03` | Actual vs budget variance |

---

## 5. Business Rules

- The monthly Finance MIS is auto-generated on the last day of the month and auto-sent to the Director, Branch Manager, and Accounts lead; the report is not manually curated — it is pulled directly from the system's transactional data (receipts, payroll, vendor payments, GST); this eliminates the possibility of the Accounts team adjusting numbers before presentation; the Director's access to the raw data ensures oversight without going through intermediaries
- The EBITDA margin (48.9% in March 2026) is TCC's headline financial KPI; a margin below 35% triggers a cost review; a margin consistently above 50% suggests underinvestment in faculty quality or marketing; the target range is 42–50%; the Director reviews margin monthly in the context of one-time items (a month with heavy marketing spend for batch launch will show a lower margin that should be evaluated in context, not in isolation)
- Finance reports containing individual student fee data are restricted to the Accounts team only; the Branch Manager and Director see aggregate revenue (total enrollment fee collected) but not per-student records in the finance report; per-student fee data is available in the Accounts team's working documents for reconciliation; this separation follows DPDPA 2023 data minimisation — the Director does not need to know that "Akhil Kumar paid ₹9,000 on March 15" to make financial decisions
- The quarterly P&L is the basis for franchise performance reviews; each franchise branch submits their quarterly revenue and expense data by the 10th of the following month; TCC headquarters compares franchise margins against the owned branch benchmarks; a franchise with a margin consistently below 30% (vs TCC's 43%) is either operating inefficiently or under-pricing; TCC's franchise support team investigates and provides remediation; a franchise that cannot reach 30% margin over 2 consecutive quarters may be reviewed for termination under the franchise agreement's performance clause
- Annual accounts are the responsibility of the Director and are reviewed by the CA firm; the annual report (full FY P&L, balance sheet, cash flow) is not published in EduForge's standard reports — it is prepared offline by the CA using EduForge's data exports; EduForge provides: complete invoice register, complete expense voucher register, payroll summary, GST filing records, and bank reconciliation data; the CA uses these to prepare the formal accounts under the Companies Act 2013 (or Partnership Act if TCC is a firm)

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division G*
