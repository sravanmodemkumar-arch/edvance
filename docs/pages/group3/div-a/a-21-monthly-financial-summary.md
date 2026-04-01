# A-21 — Monthly Financial Summary

> **URL:** `/school/admin/finance/monthly/`
> **File:** `a-21-monthly-financial-summary.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Promoter (S7) — full · Principal (S6) — view · VP Admin (S5) — view

---

## 1. Purpose

Month-by-month income and expenditure summary for the Promoter and Principal. Answers: Did we collect what we expected? Did we spend within budget? What's our surplus/deficit this month? This page does not handle transaction-level detail (that's the Accountant's domain in div-e), but gives leadership the P&L view for governance decisions.

---

## 2. Page Layout

### 2.1 Header
```
Monthly Financial Summary — 2025–26         [Export] [Print Report]
Month: March 2026 ▼     View: [Monthly ▼] [Quarterly] [Annual]
```

---

## 3. Income vs Expenditure (current month)

### 3.1 Income Summary

| Income Head | Budget | Actual | Variance | % Achievement |
|---|---|---|---|---|
| Tuition Fee | ₹6.85L | ₹6.60L | -₹0.25L | 96.4% |
| Transport Fee | ₹0.80L | ₹0.72L | -₹0.08L | 90.0% |
| Hostel Fee | ₹1.24L | ₹1.01L | -₹0.23L | 81.5% |
| Exam Fee | ₹0.35L | ₹0.32L | -₹0.03L | 91.4% |
| Other Income | ₹0.10L | ₹0.14L | +₹0.04L | 140.0% |
| **Total Income** | **₹9.34L** | **₹8.79L** | **-₹0.55L** | **94.1%** |

### 3.2 Expenditure Summary

| Expense Head | Budget | Actual | Variance | Note |
|---|---|---|---|---|
| Staff Salaries (Teaching) | ₹4.20L | ₹4.18L | -₹0.02L | |
| Staff Salaries (Non-Teaching) | ₹0.85L | ₹0.84L | -₹0.01L | |
| Transport Operations | ₹0.42L | ₹0.44L | +₹0.02L | Diesel price increase |
| Hostel Operations | ₹0.38L | ₹0.36L | -₹0.02L | |
| Utilities (Electricity/Water) | ₹0.18L | ₹0.21L | +₹0.03L | Above budget |
| Maintenance & Repairs | ₹0.12L | ₹0.09L | -₹0.03L | |
| Academic Resources | ₹0.08L | ₹0.06L | -₹0.02L | |
| Marketing & Admissions | ₹0.05L | ₹0.04L | -₹0.01L | |
| Miscellaneous | ₹0.05L | ₹0.07L | +₹0.02L | |
| **Total Expenditure** | **₹6.33L** | **₹6.29L** | **-₹0.04L** | |

### 3.3 Net Surplus/Deficit
```
Income:      ₹8.79L
Expenditure: ₹6.29L
───────────────────
Surplus:     ₹2.50L  ✅ (Budget: ₹3.01L — 83.1% of target)
```

---

## 4. Year-to-Date Summary

Cumulative P&L for April 2025 – March 2026:

| Category | Full Year Budget | YTD Actual | YTD % | Remaining |
|---|---|---|---|---|
| Total Income | ₹1.24 Cr | ₹1.02 Cr | 82.3% | ₹22.4L |
| Total Expenditure | ₹0.96 Cr | ₹0.91 Cr | 94.8% | ₹5.2L |
| Net Surplus | ₹28L | ₹11L | 39.3% | — |

---

## 5. Charts

### 5.1 Income vs Expenditure Trend (12 months)
- Dual line: Income (blue) vs Expenditure (red)
- Surplus area: green shaded between lines
- Deficit periods: red shade

### 5.2 Expenditure Breakdown (donut)
- Largest slices: Salaries typically 65–75% of total expenditure
- Useful for Promoter to see if salary % is within norms

---

## 6. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/finance/monthly-summary/?month={month}` | Monthly P&L |
| 2 | `GET` | `/api/v1/school/{id}/finance/ytd-summary/` | Year-to-date P&L |
| 3 | `GET` | `/api/v1/school/{id}/finance/income-expense-trend/?months=12` | Trend chart data |
| 4 | `GET` | `/api/v1/school/{id}/finance/expense-breakdown/?month={month}` | Expense category breakdown |
| 5 | `GET` | `/api/v1/school/{id}/finance/monthly-report/pdf/?month={month}` | PDF report download |

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division A*
