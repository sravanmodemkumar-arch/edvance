# 59 — Cash Flow Dashboard

- **URL:** `/group/finance/cash-flow/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Role:** CFO G1 (primary) · Finance Manager G1

---

## 1. Purpose

The Cash Flow Dashboard gives the CFO and Finance Manager a real-time and forward-looking view of cash inflows and outflows across the group. It aggregates: fee collections received (inflows), vendor payments made and scheduled (outflows), salary disbursements, tax payments, and scholarship disbursements to produce a net cash position for each branch and the group overall.

A 30-day cash forecast is generated from: expected fee receipts (due dates from fee schedule), scheduled vendor payments, upcoming payroll dates, and pending scholarship disbursements. This allows the CFO to identify potential cash shortfalls before they occur and plan inter-branch fund transfers.

---

## 2. Role Access

| Role | Level | Access |
|---|---|---|
| Group CFO | G1 | Full read |
| Group Finance Manager | G1 | Full read |
| Group Accounts Manager | G1 | Read |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Finance → Cash Flow Dashboard
```

### 3.2 Page Header
- **Title:** `Cash Flow Dashboard`
- **Subtitle:** `Group Cash Position: ₹[X] · As of [Date]`
- **Right-side controls:** `[Month ▾]` `[Branch ▾]` `[View: Summary / Detailed ▾]` `[Export ↓]`

### 3.3 Alert Banner

| Condition | Banner | Severity |
|---|---|---|
| Cash shortfall forecast in 15 days | "[Branch] projected cash shortfall of ₹[X] in 15 days." | Red |
| Large outflow pending | "Vendor batch payment of ₹[X] scheduled for [Date]." | Amber |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule |
|---|---|---|
| Total Cash (Bank + Petty Cash) | ₹ | Neutral |
| Inflows (Month to Date) | ₹ | Neutral |
| Outflows (Month to Date) | ₹ | Neutral |
| Net Cash Flow (Month) | ₹ | Green if +ve · Red if -ve |
| Scheduled Outflows (Next 30 Days) | ₹ | Amber if > cash balance |
| Expected Inflows (Next 30 Days) | ₹ | Neutral |

---

## 5. Cash Flow Statement

### 5.1 Period View — Monthly Cash Flow Statement

| Section | Category | Amount |
|---|---|---|
| **Operating Inflows** | Fee Collections (day scholars) | ₹ |
| | Hostel Fees | ₹ |
| | Coaching Fees (GST incl.) | ₹ |
| | Other income | ₹ |
| **Total Inflows** | | **₹** |
| **Operating Outflows** | Salaries (net) | ₹ |
| | Vendor Payments | ₹ |
| | Scholarship Disbursements | ₹ |
| | Tax Payments (GST/TDS) | ₹ |
| | Hostel Operating Costs | ₹ |
| | Other Expenses | ₹ |
| **Total Outflows** | | **₹** |
| **Net Operating Cash Flow** | | **₹** |
| **Financing** | Inter-branch Transfers In | ₹ |
| | Inter-branch Transfers Out | ₹ |
| **Net Cash Flow** | | **₹** |
| **Opening Balance** | | ₹ |
| **Closing Balance** | | **₹** |

### 5.2 Branch-wise Cash Position Table

| Branch | Bank Balance | Petty Cash | Total | Net Cash Flow (Month) | 30-Day Forecast |
|---|---|---|---|---|---|
| [Branch] | ₹ | ₹ | ₹ | ₹ | ₹ (surplus / shortfall) |

Colour: Red if 30-day forecast is negative.

---

## 6. 30-Day Cash Forecast

### 6.1 Forecast Table

| Date | Expected Inflows | Expected Outflows | Net | Cumulative Balance |
|---|---|---|---|---|
| [Date + 1] | ₹ (fee due) | ₹ (vendor batch) | ₹ | ₹ |
| [Date + 2] | ₹ | ₹ | ₹ | ₹ |
| ... | | | | |

**Forecast assumptions:**
- Fee inflows: based on fee schedule due dates + historical collection rate
- Salary outflow: scheduled on last working day
- Vendor payments: next batch run date

---

## 7. Drawers

### 7.1 Drawer: `branch-cash-detail` — Branch Cash Detail
- **Width:** 760px

**Bank Accounts:**
| Account | Bank | Balance | Last Updated |
|---|---|---|---|
| [Acc No masked] | [Bank] | ₹ | [Date] |

**Cash Flow Breakdown (current month):**
- Inflows by category · Outflows by category

**Petty Cash Log:**
| Date | Description | Debit | Credit | Balance |
|---|---|---|---|---|

### 7.2 Drawer: `inflow-detail` — Expected Inflows Detail
- List of upcoming fee due dates, expected amounts, and collection probability

### 7.3 Drawer: `outflow-detail` — Scheduled Outflows Detail
- Vendor batch payments · Upcoming payroll dates · Tax payment deadlines

---

## 8. Charts

### 8.1 Monthly Cash Flow — Inflows vs Outflows (Bar — Last 12 Months)
### 8.2 30-Day Cash Balance Forecast (Area Chart)
- Running balance line with shaded forecast band
### 8.3 Outflow Breakdown by Category (Donut)
- **Segments:** Salaries · Vendors · Taxes · Scholarships · Other

---

## 9. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Export | "Cash flow report exported." | Info | 3s |
| Shortfall alert | "Cash shortfall projected for [Branch] in [N] days." | Warning | 5s |

---

## 10. Empty States

| Condition | Heading | Description |
|---|---|---|
| No data | "Cash flow data unavailable" | "No cash flow data for the selected period." |

---

## 11. Loader States

| Trigger | Loader |
|---|---|
| Page load | Skeleton KPIs + statement |
| Branch switch | Statement skeleton |
| Forecast load | Spinner: "Computing 30-day forecast..." |
| Drawer | Spinner |

---

## 12. Role-Based UI Visibility

| Element | CFO G1 | Finance Mgr G1 | Accounts Mgr G1 |
|---|---|---|---|
| 30-Day Forecast | ✅ | ✅ | ❌ |
| Branch cash detail | ✅ | ✅ | ✅ |
| View petty cash log | ✅ | ✅ | ✅ |
| Export | ✅ | ✅ | ❌ |

---

## 13. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/finance/cash-flow/` | JWT (G1+) | Cash flow summary |
| GET | `/api/v1/group/{id}/finance/cash-flow/statement/?month=` | JWT (G1+) | Monthly statement |
| GET | `/api/v1/group/{id}/finance/cash-flow/forecast/` | JWT (G1+) | 30-day forecast |
| GET | `/api/v1/group/{id}/finance/cash-flow/{bid}/` | JWT (G1+) | Branch detail |
| GET | `/api/v1/group/{id}/finance/cash-flow/export/` | JWT (G1+) | Export |

---

## 14. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Month filter | `change` | GET `.../cash-flow/statement/?month=` | `#cashflow-statement` | `innerHTML` |
| Branch filter | `change` | GET `.../cash-flow/?branch=` | `#cashflow-section` | `innerHTML` |
| Forecast load | `load` | GET `.../cash-flow/forecast/` | `#forecast-section` | `innerHTML` |
| Branch drawer | `click` | GET `.../cash-flow/{id}/` | `#drawer-body` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
