# 14 — Annual Budget vs Actual

- **URL:** `/group/finance/budget/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Roles:** CFO G1 (primary) · Finance Manager G1 · Chairman G5

---

## 1. Purpose

The Annual Budget vs Actual page tracks the group's approved annual budget against actual expenditure and revenue across all branches and expense categories. It answers: Are we within budget? Which categories are over-run? Which branches are consuming budget disproportionately?

Budget data is entered at the beginning of the financial year (or approved by the board) and actuals flow in monthly from branch reports. The CFO uses this page to identify variances early and take corrective action — reallocating budgets, curtailing excess spend, or raising budget revision requests.

---

## 2. Role Access

| Role | Level | Access |
|---|---|---|
| Group CFO | G1 | Full read + create/edit budget entries + export |
| Group Finance Manager | G1 | Full read + export |
| Group Chairman | G5 | Full read |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Finance → Annual Budget vs Actual
```

### 3.2 Page Header
- **Title:** `Annual Budget vs Actual`
- **Subtitle:** `FY [Year] · Approved Budget: ₹[X] Cr · YTD Actual: ₹[Y] Cr`
- **Right-side controls:** `[FY ▾]` `[Branch ▾ (All / Specific)]` `[+ Enter Budget]` `[Export ↓]`

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| Any category over budget | "[N] budget category/categories over budget. Total overage: ₹[X]." | Red |
| Budget not entered for current FY | "Annual budget for FY [Year] not entered. Please enter budget before [Date]." | Amber |
| YTD actual > 90% of annual budget | "Group budget [X]% consumed with [N] months remaining." | Amber |

---

## 4. Main Budget Table

### 4.1 Revenue Budget

| Line Item | Annual Budget | Q1 Actual | Q2 Actual | Q3 Actual | Q4 Actual | YTD Actual | YTD Variance | % Achieved |
|---|---|---|---|---|---|---|---|---|
| Tuition Fee — Day Scholar | ₹ | ₹ | ₹ | ₹ | ₹ | ₹ | ₹ | % |
| Tuition Fee — Coaching | ₹ | ₹ | ₹ | ₹ | ₹ | ₹ | ₹ | % |
| Hostel Fee | ₹ | ₹ | ₹ | ₹ | ₹ | ₹ | ₹ | % |
| Transport Fee | ₹ | ₹ | ₹ | ₹ | ₹ | ₹ | ₹ | % |
| Government Grants | ₹ | ₹ | ₹ | ₹ | ₹ | ₹ | ₹ | % |
| **Total Revenue** | **₹** | **₹** | **₹** | **₹** | **₹** | **₹** | **₹** | **%** |

### 4.2 Expenditure Budget

| Line Item | Annual Budget | Q1 Actual | Q2 Actual | Q3 Actual | Q4 Actual | YTD Actual | YTD Variance | % Consumed |
|---|---|---|---|---|---|---|---|---|
| Salaries — Teaching | ₹ | ₹ | ₹ | ₹ | ₹ | ₹ | ₹ | % |
| Salaries — Non-Teaching | ₹ | ₹ | ₹ | ₹ | ₹ | ₹ | ₹ | % |
| PF / ESI | ₹ | ₹ | ₹ | ₹ | ₹ | ₹ | ₹ | % |
| Books & Procurement | ₹ | ₹ | ₹ | ₹ | ₹ | ₹ | ₹ | % |
| Uniforms | ₹ | ₹ | ₹ | ₹ | ₹ | ₹ | ₹ | % |
| Lab Equipment | ₹ | ₹ | ₹ | ₹ | ₹ | ₹ | ₹ | % |
| Infrastructure | ₹ | ₹ | ₹ | ₹ | ₹ | ₹ | ₹ | % |
| Scholarships | ₹ | ₹ | ₹ | ₹ | ₹ | ₹ | ₹ | % |
| EduForge Platform | ₹ | ₹ | ₹ | ₹ | ₹ | ₹ | ₹ | % |
| GST & Tax Payments | ₹ | ₹ | ₹ | ₹ | ₹ | ₹ | ₹ | % |
| Miscellaneous | ₹ | ₹ | ₹ | ₹ | ₹ | ₹ | ₹ | % |
| **Total Expenditure** | **₹** | **₹** | **₹** | **₹** | **₹** | **₹** | **₹** | **%** |
| **Net Surplus / (Deficit)** | **₹** | **₹** | **₹** | **₹** | **₹** | **₹** | **₹** | |

Variance colour coding: Green = within ±5% · Amber = 5–15% over · Red = >15% over budget

---

## 5. Branch-Level Budget View

Toggle: `[Consolidated ↔ Per Branch]`

When Per Branch selected — branch selector appears. Shows same table for single branch.

---

## 6. Drawers

### 6.1 Drawer: `budget-entry` — Enter / Edit Budget
- **Trigger:** [+ Enter Budget]
- **Width:** 720px

| Field | Type | Required | Notes |
|---|---|---|---|
| Financial Year | Select | ✅ | Cannot enter budget for past FYs after lock |
| Scope | Radio: Group-level · Per Branch | ✅ | |
| Line Items | Budget amount per line | ✅ | All line items from table |
| Notes / Board Resolution Ref | Textarea | ❌ | |
| Budget Locked | Toggle | ❌ | Once locked, no edits without CFO override |

- [Cancel] [Save Draft] [Submit Budget]

### 6.2 Drawer: `variance-note` — Add Variance Note
- **Trigger:** Click on any high-variance cell
- Explain reason for variance — stored in audit trail

---

## 7. Charts

### 7.1 Budget vs Actual by Category (Horizontal Bar)
- **Bars:** Budget (grey) · Actual (blue)
- **Threshold line:** 100% (budget limit)
- **Export:** PNG

### 7.2 Monthly Burn Rate (Line)
- **Series:** Budgeted monthly spend · Actual monthly spend
- **Export:** PNG

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Budget saved | "Budget for FY [Year] saved." | Success | 4s |
| Budget locked | "Budget locked. Contact CFO to make changes." | Info | 4s |
| Export | "Budget report exported." | Success | 3s |
| Variance note saved | "Variance note recorded." | Info | 3s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No budget entered | "No budget for this FY" | "Enter the annual budget to track variances." | [+ Enter Budget] |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Page load | Skeleton: header + table sections |
| FY switch | Full table skeleton |
| Budget entry drawer | Spinner + skeleton form |

---

## 11. Role-Based UI Visibility

| Element | CFO G1 | Finance Mgr G1 | Chairman G5 |
|---|---|---|---|
| [+ Enter Budget] | ✅ | ❌ | ❌ |
| Edit budget entries | ✅ | ❌ | ❌ |
| Lock budget | ✅ | ❌ | ❌ |
| Variance notes | ✅ | ✅ | ❌ |
| View full table | ✅ | ✅ | ✅ |
| Export | ✅ | ✅ | ❌ |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/finance/budget/` | JWT (G1+) | Budget vs actual table |
| POST | `/api/v1/group/{id}/finance/budget/` | JWT (G1, CFO only) | Create budget |
| PUT | `/api/v1/group/{id}/finance/budget/{fy}/` | JWT (G1, CFO only) | Update budget |
| POST | `/api/v1/group/{id}/finance/budget/{fy}/lock/` | JWT (G1, CFO only) | Lock budget |
| GET | `/api/v1/group/{id}/finance/budget/charts/` | JWT (G1+) | Chart data |
| POST | `/api/v1/group/{id}/finance/budget/variance-notes/` | JWT (G1+) | Add note |
| GET | `/api/v1/group/{id}/finance/budget/export/` | JWT (G1+) | Export |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| FY switch | `change` | GET `.../budget/?fy=` | `#budget-body` | `innerHTML` |
| Branch toggle | `change` | GET `.../budget/?branch=` | `#budget-table` | `innerHTML` |
| Entry drawer | `click` | GET `.../budget/entry-form/` | `#drawer-body` | `innerHTML` |
| Save budget | `submit` | POST `.../budget/` | `#drawer-body` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
