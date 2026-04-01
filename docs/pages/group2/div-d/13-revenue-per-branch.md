# 13 — Revenue per Branch Report

- **URL:** `/group/finance/revenue-branch/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Roles:** CFO G1 · Finance Manager G1 · Chairman G5

---

## 1. Purpose

The Revenue per Branch Report provides a cross-branch comparison of fee revenue collected, demand raised, and collection rates. Unlike the P&L Report which shows profitability, this report focuses exclusively on revenue — the top line — to identify high-performing branches and branches at risk of missing revenue targets.

The CFO uses this report to track whether each branch is on track for its revenue target, to identify branches where fee demand has not been raised correctly, and to spot seasonal patterns in collection. It supports branch-level accountability conversations: if Branch X has 60% collection by Month 6 while Branch Y has 85%, the CFO needs an explanation.

---

## 2. Role Access

| Role | Level | Access |
|---|---|---|
| Group CFO | G1 | Full read + export |
| Group Finance Manager | G1 | Full read + export |
| Group Chairman | G5 | Full read |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Finance → Revenue per Branch Report
```

### 3.2 Page Header
- **Title:** `Revenue per Branch Report`
- **Subtitle:** `AY [Year] · FY [Year] · [N] Branches`
- **Right-side controls:** `[AY ▾]` `[Term ▾ (All/1/2/3)]` `[Branch ▾]` `[Fee Type ▾]` `[Export ↓]`

---

## 4. Main Table — Branch Revenue Comparison

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Branch | Text | ✅ | |
| Fee Demand Raised | ₹ | ✅ | Total billed to students |
| Amount Collected | ₹ | ✅ | Actual receipts |
| Outstanding | ₹ | ✅ | Demand − Collected |
| Collection Rate % | % badge | ✅ | Colour: Green ≥ 90% · Amber 75–89% · Red < 75% |
| Target Revenue | ₹ | ✅ | From annual budget |
| Achievement % | % | ✅ | Collected / Target |
| Day Scholar Revenue | ₹ | ✅ | Sub-component |
| Hosteler Revenue | ₹ | ✅ | Sub-component |
| Transport Revenue | ₹ | ✅ | Sub-component |
| Coaching Revenue | ₹ | ✅ | Sub-component |
| Actions | View Detail | — | |

### 4.1 Filters

| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Term | Select | All · Term 1 · Term 2 · Term 3 |
| Fee Type | Multi-select | Day Scholar · Hosteler · Transport · Coaching · All |
| Revenue Range | Range slider | ₹0 – ₹[Max] |
| Achievement % | Range slider | 0% – 150% |

### 4.2 Search
- Branch name · 300ms debounce

### 4.3 Pagination
- Server-side · 25 rows/page · Sort: Collection Rate % ascending (worst first, default)

---

## 5. Drawers

### 5.1 Drawer: `branch-revenue-detail` — Branch Revenue Detail
- **Trigger:** View Detail action
- **Width:** 720px

**Tab: Fee Component Breakdown**

| Fee Component | Demand | Collected | Outstanding | % |
|---|---|---|---|---|
| Tuition Fee | ₹ | ₹ | ₹ | % |
| Hostel Fee (Non-AC Boys) | ₹ | ₹ | ₹ | % |
| Hostel Fee (AC Boys) | ₹ | ₹ | ₹ | % |
| Hostel Fee (Non-AC Girls) | ₹ | ₹ | ₹ | % |
| Hostel Fee (AC Girls) | ₹ | ₹ | ₹ | % |
| Mess Fee | ₹ | ₹ | ₹ | % |
| Transport Fee | ₹ | ₹ | ₹ | % |
| Coaching Fee | ₹ | ₹ | ₹ | % |
| **Total** | **₹** | **₹** | **₹** | **%** |

**Tab: Monthly Trend**
- Line chart: Monthly collection trend for this branch (current AY vs previous AY)

**Tab: Defaulter Summary**
- Count of defaulters by aging bucket (0–30, 31–60, >60 days)

---

## 6. Charts

### 6.1 Collection Rate Ranking (Horizontal Bar)
- **Y-axis:** Branches (sorted by collection rate asc)
- **X-axis:** Collection %
- **Colour:** Green ≥ 90% · Amber 75–89% · Red < 75%
- **Benchmark line:** Group average
- **Export:** PNG

### 6.2 Revenue Composition by Branch (Stacked Bar)
- **Stacks:** Day Scholar · Hosteler · Transport · Coaching
- **Sort:** By total revenue desc

### 6.3 Revenue Trend — Group Total (Line)
- **X-axis:** Months of AY
- **Series:** Demand (dashed) · Collected (solid) · Previous AY (grey)

---

## 7. Summary Row (Table Footer)
- **Group Total:** Sum of all branches for each column
- **Group Average:** Avg collection rate (bold)

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Export CSV | "Revenue report exported as CSV." | Success | 3s |
| Export PDF | "Revenue report PDF ready." | Success | 3s |

---

## 9. Empty States

| Condition | Heading | Description |
|---|---|---|
| No data for AY | "No revenue data" | "No fee collections recorded for this academic year." |
| Branch filter returns none | "No branches match" | "Adjust your filters to see branch data." |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Page load | Skeleton table (25 rows) + chart skeletons |
| Filter change | Inline table skeleton |
| Branch detail drawer | Spinner + skeleton tabs |

---

## 11. Role-Based UI Visibility

| Element | CFO G1 | Finance Mgr G1 | Chairman G5 |
|---|---|---|---|
| Full table | ✅ | ✅ | ✅ |
| Branch detail drawer | ✅ | ✅ | ✅ |
| Export | ✅ | ✅ | ❌ |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/finance/revenue-branch/` | JWT (G1+) | Revenue table |
| GET | `/api/v1/group/{id}/finance/revenue-branch/{bid}/detail/` | JWT (G1+) | Branch fee breakdown |
| GET | `/api/v1/group/{id}/finance/revenue-branch/{bid}/trend/` | JWT (G1+) | Monthly trend chart data |
| GET | `/api/v1/group/{id}/finance/revenue-branch/charts/` | JWT (G1+) | All chart data |
| GET | `/api/v1/group/{id}/finance/revenue-branch/export/?format=csv` | JWT (G1+) | Export |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Search | `input delay:300ms` | GET `.../revenue-branch/?q=` | `#revenue-table-body` | `innerHTML` |
| Filter | `change` | GET `.../revenue-branch/?term=&type=` | `#revenue-section` | `innerHTML` |
| Sort column | `click` | GET `.../revenue-branch/?sort=&dir=` | `#revenue-table` | `innerHTML` |
| Pagination | `click` | GET `.../revenue-branch/?page=` | `#revenue-section` | `innerHTML` |
| Branch detail | `click` | GET `.../revenue-branch/{bid}/detail/` | `#drawer-body` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
