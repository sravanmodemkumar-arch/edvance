# 01 — Group CFO / Finance Director Dashboard

- **URL:** `/group/finance/cfo/`
- **Template:** `portal_base.html`
- **Priority:** P0
- **Role:** Group CFO / Finance Director (Role 30, G1)

---

## 1. Purpose

The CFO Dashboard is the top-level financial command centre for the entire institution group. It surfaces consolidated P&L health, fee collection velocity, outstanding dues, audit status, and EduForge platform billing in a single authoritative view across all branches. The CFO (G1 — read-only on the platform) uses this dashboard to govern financial performance without needing to navigate individual branch portals.

Key decisions enabled here: identifying which branches are underperforming on fee collection, flagging overdue audit closures, tracking annual budget consumption, and monitoring the group's EduForge subscription cost. Every metric links through to a detailed report page so the CFO can drill from summary to granular data without context-switching.

This dashboard is the only page in the platform where all financial streams — tuition, hostel, transport, scholarship disbursement, vendor payables, payroll, and GST — are visible in one consolidated layout.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group CFO / Finance Director | G1 | Full read — all sections | Primary owner; no data entry |
| Group Finance Manager | G1 | Read — sections 4, 5 (reconciliation + audit) | Cannot see EduForge billing section |
| Group Chairman / Founder | G5 | Read — all sections | Strategic oversight |
| Group MD | G5 | Read — all sections | |
| Group CEO | G4 | Read — all sections | |

> **Enforcement:** All access is enforced server-side via `@role_required` decorator. G1 access is read-only — no create/edit/delete actions are exposed.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Finance → CFO Dashboard
```

### 3.2 Page Header
- **Title:** `CFO Dashboard`
- **Subtitle:** `Group Finance Overview · FY [Year] · AY [Year]`
- **Role Badge:** `Group CFO / Finance Director`
- **Right-side controls:** `[Financial Year ▾]` `[Academic Year ▾]` `[Export Full Report ↓]`

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| Any branch overdue on fee reconciliation > 30 days | "Fee reconciliation overdue for [N] branch(es). Last reconciled: [Date]." | Red |
| EduForge subscription renewal due within 15 days | "EduForge subscription renewing on [Date]. Cost: ₹[X]. Confirm renewal." | Amber |
| GST filing due within 7 days | "GSTR-3B due on [Date]. [N] invoices pending classification." | Amber |
| Internal audit pending for any branch (> 90 days since last) | "[N] branch(es) have not been audited in the last 90 days." | Amber |
| Annual budget consumed > 90% | "Group budget at [X]% consumption with [N] months remaining in FY." | Red |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Total Fee Revenue (YTD) | Sum of all fee collections across branches | Informational (blue) | → Page 13 Revenue per Branch |
| Collection Rate | Collected / Demand × 100 | Green ≥ 90% · Amber 75–89% · Red < 75% | → Page 28 Fee Collection Dashboard |
| Outstanding Dues | Total pending fee cross-branch | Red if > 5% of annual demand | → Page 31 Outstanding Dues |
| Budget Consumed % | YTD spend / Annual budget | Green < 75% · Amber 75–90% · Red > 90% | → Page 14 Budget vs Actual |
| Scholarship Disbursed (YTD) | Total scholarship amount disbursed | Informational | → Page 34 Disbursement Tracker |
| Audit Compliance | Branches with completed Q audits / Total | Green = 100% · Amber 75–99% · Red < 75% | → Page 39 Audit Planner |

**HTMX Refresh:**
```html
<div id="kpi-bar"
     hx-get="/api/v1/group/{{ group_id }}/finance/cfo/kpis/"
     hx-trigger="load, every 5m"
     hx-target="#kpi-bar"
     hx-swap="innerHTML">
```

---

## 5. Section 5.1 — P&L Summary (Cross-Branch)

Mini table — top 5 branches by revenue vs top 5 by outstanding dues side-by-side.

| Column | Notes |
|---|---|
| Branch | Name |
| Fee Demand (FY) | ₹ |
| Collected | ₹ |
| Outstanding | ₹ |
| Collection % | Colour-coded badge |

**[View Full P&L Report →]** links to Page 12.

---

## 5.2 Section 5.2 — Fee Collection Trend (Chart)

- **Type:** Line chart — monthly collection (₹) across the financial year
- **Series:** Current FY vs Previous FY
- **X-axis:** April → March
- **Y-axis:** ₹ in lakhs
- **Export:** PNG

---

## 5.3 Section 5.3 — Budget vs Actual (Chart)

- **Type:** Horizontal bar chart — per expense category
- **Categories:** Salaries · Procurement · Infrastructure · IT/EduForge · Scholarship · Misc
- **Bars:** Budget (grey) vs Actual Spend (blue)
- **Export:** PNG

---

## 5.4 Section 5.4 — Branch Audit Status

| Column | Notes |
|---|---|
| Branch | Name |
| Last Audit Date | Date |
| Next Due | Date |
| Status | Badge: Completed · Pending · Overdue |
| Findings Open | Count |

**[View Audit Planner →]** links to Page 39.

---

## 5.5 Section 5.5 — EduForge Billing Summary

| Item | Value |
|---|---|
| Active Branches on Platform | [N] |
| Current Plan | [Plan Name] |
| Monthly Cost | ₹[X] |
| Annual Cost | ₹[X] |
| Next Renewal Date | [Date] |
| Support Tickets Open | [N] |

**[Manage Billing →]** links to Page 09.

---

## 6. Charts

### 6.1 Revenue vs Outstanding by Branch (Bar)
- **Type:** Grouped bar — Collected (green) + Outstanding (red) per branch
- **Sort:** By outstanding amount (desc)
- **Export:** PNG

### 6.2 GST Filing Status (Donut)
- **Segments:** Filed · Pending · Overdue
- **Centre text:** "GSTR compliance [X]%"

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Export triggered | "Full financial report export started. Download ready in 30s." | Info | 5s |
| KPI refresh | "Dashboard data refreshed." | Success | 2s |

---

## 8. Empty States

| Condition | Heading | Description |
|---|---|---|
| No financial data for FY | "No financial data" | "No transactions recorded for this financial year." |
| No branches active | "No active branches" | "No branches are currently active on the platform." |

---

## 9. Loader States

| Trigger | Loader |
|---|---|
| Page load | Skeleton: KPI bar (6 cards) + 3 section skeletons |
| Chart load | Spinner inside chart container |
| Export | Spinner on export button |

---

## 10. Role-Based UI Visibility

| Element | CFO G1 | Finance Mgr G1 | Chairman G5 | CEO G4 |
|---|---|---|---|---|
| KPI Bar | ✅ | ✅ (partial) | ✅ | ✅ |
| P&L Summary | ✅ | ✅ | ✅ | ✅ |
| Fee Collection Trend | ✅ | ✅ | ✅ | ✅ |
| Budget vs Actual | ✅ | ❌ | ✅ | ✅ |
| Branch Audit Status | ✅ | ✅ | ✅ | ✅ |
| EduForge Billing Summary | ✅ | ❌ | ✅ | ✅ |
| Export Full Report | ✅ | ❌ | ✅ | ❌ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/finance/cfo/kpis/` | JWT (G1+) | KPI summary cards |
| GET | `/api/v1/group/{id}/finance/cfo/pl-summary/` | JWT (G1+) | P&L mini table |
| GET | `/api/v1/group/{id}/finance/cfo/collection-trend/` | JWT (G1+) | Monthly collection chart data |
| GET | `/api/v1/group/{id}/finance/cfo/budget-summary/` | JWT (G1+) | Budget vs actual chart |
| GET | `/api/v1/group/{id}/finance/cfo/audit-status/` | JWT (G1+) | Branch audit status table |
| GET | `/api/v1/group/{id}/finance/cfo/eduforge-billing/` | JWT (G1+) | EduForge billing summary |
| GET | `/api/v1/group/{id}/finance/cfo/export/` | JWT (G1+) | Full report export |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| KPI auto-refresh | `every 5m` | GET `.../cfo/kpis/` | `#kpi-bar` | `innerHTML` |
| FY switch | `change` | GET `.../cfo/?fy=` | `#dashboard-body` | `innerHTML` |
| Export | `click` | GET `.../cfo/export/` | `#export-btn` | `outerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
