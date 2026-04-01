# 12 — Group P&L Report

- **URL:** `/group/finance/pl-report/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Roles:** CFO G1 (primary) · Finance Manager G1 · Chairman G5 · MD G5 · CEO G4

---

## 1. Purpose

The Group P&L Report provides a consolidated Profit & Loss view across all branches for any selected financial year and month range. It aggregates fee revenue (tuition, hostel, transport, coaching), scholarship disbursements, vendor payments, payroll costs, and infrastructure expenses to produce a group-level income statement. Each revenue and expense line can be drilled into by branch to identify which branches are profitable and which are running deficits.

This is the primary report reviewed by the Chairman and Board in monthly/quarterly meetings. All figures are sourced from branch-submitted reports (not live bank data), making this a management reporting layer rather than a statutory P&L.

---

## 2. Role Access

| Role | Level | Access |
|---|---|---|
| Group CFO | G1 | Full read + export |
| Group Finance Manager | G1 | Full read + export |
| Group Chairman | G5 | Full read + export |
| Group MD | G5 | Full read |
| Group CEO | G4 | Full read |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Finance → Group P&L Report
```

### 3.2 Page Header
- **Title:** `Group Profit & Loss Report`
- **Subtitle:** `FY [Year] · [Month Range] · [N] Branches Consolidated`
- **Right-side controls:** `[FY ▾]` `[From Month ▾]` `[To Month ▾]` `[Branch ▾ (All / Specific)]` `[Export PDF ↓]` `[Export Excel ↓]`

---

## 4. P&L Summary Table

### 4.1 Revenue Section

| Line Item | Current Period | YTD | Budget | Variance |
|---|---|---|---|---|
| **Fee Revenue** | | | | |
| Tuition Fee — Day Scholar | ₹ | ₹ | ₹ | ₹ (Green/Red) |
| Tuition Fee — Integrated Coaching | ₹ | ₹ | ₹ | ₹ |
| Hostel Fee — Non-AC | ₹ | ₹ | ₹ | ₹ |
| Hostel Fee — AC | ₹ | ₹ | ₹ | ₹ |
| Mess Fee | ₹ | ₹ | ₹ | ₹ |
| Transport Fee | ₹ | ₹ | ₹ | ₹ |
| Exam / Lab / Activity Fee | ₹ | ₹ | ₹ | ₹ |
| **Total Fee Revenue** | **₹** | **₹** | **₹** | **₹** |
| **Other Income** | | | | |
| Government Grants Received | ₹ | ₹ | ₹ | ₹ |
| Interest Income | ₹ | ₹ | — | — |
| **Total Revenue** | **₹** | **₹** | **₹** | **₹** |

### 4.2 Expenditure Section

| Line Item | Current Period | YTD | Budget | Variance |
|---|---|---|---|---|
| **Employee Costs** | | | | |
| Teaching Staff Salaries | ₹ | ₹ | ₹ | ₹ |
| Non-Teaching Staff Salaries | ₹ | ₹ | ₹ | ₹ |
| PF / ESI / Gratuity | ₹ | ₹ | ₹ | ₹ |
| **Total Employee Costs** | **₹** | **₹** | **₹** | **₹** |
| **Procurement** | | | | |
| Books & Educational Materials | ₹ | ₹ | ₹ | ₹ |
| Uniforms | ₹ | ₹ | ₹ | ₹ |
| Lab Equipment | ₹ | ₹ | ₹ | ₹ |
| **Infrastructure & Maintenance** | | | | |
| Rent (if applicable) | ₹ | ₹ | ₹ | ₹ |
| Utilities | ₹ | ₹ | ₹ | ₹ |
| Repairs & Maintenance | ₹ | ₹ | ₹ | ₹ |
| **Technology** | | | | |
| EduForge Subscription | ₹ | ₹ | ₹ | ₹ |
| Other IT | ₹ | ₹ | ₹ | ₹ |
| **Scholarship Disbursements** | ₹ | ₹ | ₹ | ₹ |
| **Total Expenditure** | **₹** | **₹** | **₹** | **₹** |
| **Net Surplus / (Deficit)** | **₹** | **₹** | **₹** | **₹** |

All row amounts are clickable → drill-down to branch breakdown modal.

### 4.3 Filters

| Filter | Type |
|---|---|
| Branch | Multi-select (default: All) |
| Financial Year | Select |
| Period | Month range picker |
| View Mode | Consolidated · Per Branch |

### 4.4 Pagination
- N/A for P&L table (not paginated — full statement shown)
- Branch breakdown modal is paginated (20 branches/page)

---

## 5. Branch-Level Drill-down Modal

**Trigger:** Click any P&L line item
- **Title:** `[Line Item] — Branch Breakdown`

| Column | Type | Sortable |
|---|---|---|
| Branch | Text | ✅ |
| Current Period | ₹ | ✅ |
| YTD | ₹ | ✅ |
| Budget | ₹ | ✅ |
| Variance | ₹ (colour-coded) | ✅ |

---

## 6. Charts

### 6.1 Revenue vs Expenditure (Monthly Bar)
- **Series:** Revenue (blue) · Expenditure (red)
- **X-axis:** Months in selected range
- **Export:** PNG

### 6.2 Net Surplus / Deficit by Branch (Bar)
- **Colour:** Green = surplus · Red = deficit
- **Sort:** Desc by surplus

### 6.3 Revenue Composition (Donut)
- **Segments:** Day Scholar Tuition · Hostel · Transport · Coaching · Other

---

## 7. Drawers

### 7.1 Drawer: `pl-notes` — Add Management Note
- Allows CFO to annotate the P&L for board presentation
- Note: Text · Author · Date (stored, included in PDF export)

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| PDF export | "P&L report PDF ready. Download starting." | Success | 4s |
| Excel export | "P&L report Excel ready. Download starting." | Success | 4s |
| Note saved | "Management note saved." | Info | 3s |

---

## 9. Empty States

| Condition | Heading | Description |
|---|---|---|
| No data for period | "No financial data" | "No branch reports submitted for the selected period." |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Page load | Skeleton: header + P&L table sections |
| Period change | Inline P&L table skeleton |
| Branch filter | Inline table skeleton |
| Export | Spinner on export button |

---

## 11. Role-Based UI Visibility

| Element | CFO G1 | Finance Mgr G1 | Chairman G5 | CEO G4 |
|---|---|---|---|---|
| Full P&L table | ✅ | ✅ | ✅ | ✅ |
| Branch drill-down | ✅ | ✅ | ✅ | ✅ |
| [Add Note] | ✅ | ❌ | ❌ | ❌ |
| Export PDF | ✅ | ✅ | ✅ | ❌ |
| Export Excel | ✅ | ✅ | ❌ | ❌ |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/finance/pl-report/` | JWT (G1+) | Full P&L data |
| GET | `/api/v1/group/{id}/finance/pl-report/drilldown/?line=tuition_day_scholar&branch=all` | JWT (G1+) | Branch breakdown |
| GET | `/api/v1/group/{id}/finance/pl-report/charts/` | JWT (G1+) | Chart data |
| POST | `/api/v1/group/{id}/finance/pl-report/notes/` | JWT (G1) | Add note |
| GET | `/api/v1/group/{id}/finance/pl-report/export/?format=pdf` | JWT (G1+) | PDF export |
| GET | `/api/v1/group/{id}/finance/pl-report/export/?format=excel` | JWT (G1+) | Excel export |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Period change | `change` | GET `.../pl-report/?fy=&from=&to=` | `#pl-table` | `innerHTML` |
| Branch filter | `change` | GET `.../pl-report/?branch=` | `#pl-table` | `innerHTML` |
| Drill-down click | `click` | GET `.../pl-report/drilldown/?line=` | `#modal-body` | `innerHTML` |
| Export PDF | `click` | GET `.../pl-report/export/?format=pdf` | `#export-btn` | `outerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
