# 11 — Group Payroll Coordinator Dashboard

- **URL:** `/group/finance/payroll/`
- **Template:** `portal_base.html`
- **Priority:** P0
- **Role:** Group Payroll Coordinator (Role 40, G0)

---

## 1. Purpose

The Payroll Coordinator Dashboard provides a read-only summary view of payroll disbursement status across all branches. The Group Payroll Coordinator (G0 — no platform access for posting transactions) uses an external payroll software (e.g., GreytHR, Keka, Saral Paypack) for actual payroll processing; this EduForge dashboard receives a payroll data feed from that software via API to surface key metrics.

The dashboard answers three questions: Has salary been disbursed this month for every branch? Are there branches with payroll compliance issues (PF, ESI, PT)? Are there anomalies in headcount vs payroll amounts that suggest data errors?

This is a governance and exception-management dashboard — not a payroll processing system. Any discrepancy surfaced here must be resolved in the payroll software and the data feed re-synced.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Payroll Coordinator | G0 | Read-only — all sections | Primary owner; G0 = no platform CRUD access |
| Group CFO | G1 | Read — salary cost summary only | |
| Group HR Director | G3 | Read — headcount + disbursement status | |
| Group Finance Manager | G1 | Read — compliance section | |

> **Note:** G0 means this user has no write access to any EduForge data. The payroll dashboard is purely a read-only intelligence layer sourced from the external payroll system.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Finance → Payroll Dashboard
```

### 3.2 Page Header
- **Title:** `Payroll Summary Dashboard`
- **Subtitle:** `[Month Year] · Salary Disbursement Status — Data from [Payroll Software]`
- **Role Badge:** `Group Payroll Coordinator`
- **Right-side controls:** `[Month ▾]` `[Sync Payroll Data ↻]` `[Export ↓]`

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| Salary not disbursed for any branch by 7th of month | "[N] branch(es) have not disbursed salary for [Month] yet." | Red |
| PF/ESI payment overdue | "PF/ESI challan for [Month] not deposited. Due date: [Date]." | Red |
| Payroll data not synced for > 24 hours | "Payroll data last synced: [Timestamp]. Sync to get latest status." | Amber |
| Headcount variance > 5% vs last month | "Headcount for [Branch] changed by [X]% from last month. Verify." | Amber |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Total Salary Disbursed (Month) | ₹ | Informational | → Page 56 |
| Branches Salary Paid | Count / Total | Green = all | → Page 56 |
| Branches Salary Pending | Count | Red if > 0 | → Page 56 |
| Total Headcount (Active) | Count | Informational | → Page 56 |
| PF Compliance | Branches compliant / Total | Green = 100% | → Page 57 |
| ESI Compliance | Branches compliant / Total | Green = 100% | → Page 57 |

---

## 5. Section 5.1 — Branch Salary Disbursement Status

| Column | Type | Sortable |
|---|---|---|
| Branch | Text | ✅ |
| Total Staff | Count | ✅ |
| Salary Month | Text | ✅ |
| Gross Salary | ₹ | ✅ |
| Net Salary (Paid) | ₹ | ✅ |
| Disbursement Date | Date | ✅ |
| Status | Badge: Paid · Pending · Partial · Overdue | ✅ |
| Actions | View Details | — |

**Filters:** Branch · Status · Month
**Search:** Branch name
**Pagination:** 20 rows/page

**[View Full Report →]** links to Page 56.

---

## 5.2 Section 5.2 — Payroll Compliance Summary

| Compliance Item | Status | Due Date | Deposited Date | Actions |
|---|---|---|---|---|
| PF (Provident Fund) | Badge | [Date] | [Date] / — | View |
| ESI (Employee State Insurance) | Badge | [Date] | [Date] / — | View |
| PT (Professional Tax) | Badge | [Date] | [Date] / — | View |
| TDS on Salary (Form 24Q) | Badge | [Date] | [Date] / — | View |

**[View Compliance Report →]** links to Page 57.

---

## 5.3 Section 5.3 — Last Sync Status

| Item | Value |
|---|---|
| Payroll Software | [Software Name] |
| Last Sync Timestamp | [Date Time] |
| Sync Status | Badge: Success · Failed · In Progress |
| Records Synced | Count |
| Errors | Count (red if > 0) |

- **[Sync Now ↻]** — triggers manual sync with payroll software API

---

## 6. Charts

### 6.1 Monthly Salary Cost Trend (Line)
- **X-axis:** Last 12 months
- **Y-axis:** ₹ net salary disbursed
- **Export:** PNG

### 6.2 Salary by Branch (Bar)
- **Sort:** Desc by salary amount
- **Colour:** Green = paid · Red = pending

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Sync triggered | "Payroll data sync initiated. Refresh in 2 minutes." | Info | 5s |
| Sync complete | "Payroll data synced. [N] records updated." | Success | 4s |
| Sync failed | "Payroll sync failed. Check API connection. Error: [Code]." | Error | 6s |
| Export | "Payroll summary exported." | Info | 3s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No payroll data synced | "No payroll data" | "Sync payroll data from [Software] to view disbursement status." | [Sync Now] |
| All branches paid | "All salaries disbursed" | "All branches have disbursed salary for [Month]." | — |

---

## 9. Loader States

| Trigger | Loader |
|---|---|
| Page load | Skeleton KPIs + table skeleton |
| Sync in progress | Progress bar: "Syncing payroll data..." |
| Month switch | Table skeleton |

---

## 10. Role-Based UI Visibility

| Element | Payroll Coord G0 | CFO G1 | Finance Mgr G1 | HR Director G3 |
|---|---|---|---|---|
| Disbursement table | ✅ | ✅ (cost view) | ✅ | ✅ |
| Compliance table | ✅ | ✅ | ✅ | ✅ |
| Sync button | ✅ | ❌ | ❌ | ❌ |
| Charts | ✅ | ✅ | ✅ | ✅ |
| Export | ✅ | ✅ | ✅ | ❌ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/finance/payroll/kpis/` | JWT (G0+) | KPI cards |
| GET | `/api/v1/group/{id}/finance/payroll/branch-status/` | JWT (G0+) | Branch salary status |
| GET | `/api/v1/group/{id}/finance/payroll/compliance/` | JWT (G0+) | PF/ESI/PT compliance |
| POST | `/api/v1/group/{id}/finance/payroll/sync/` | JWT (G0+, Payroll role) | Trigger payroll data sync |
| GET | `/api/v1/group/{id}/finance/payroll/sync-status/` | JWT (G0+) | Last sync status |
| GET | `/api/v1/group/{id}/finance/payroll/export/` | JWT (G0+) | Export |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Month switch | `change` | GET `.../payroll/branch-status/?month=` | `#payroll-table` | `innerHTML` |
| Sync trigger | `click` | POST `.../payroll/sync/` | `#sync-status` | `outerHTML` |
| Sync poll | `load, every 10s` (while syncing) | GET `.../payroll/sync-status/` | `#sync-status` | `outerHTML` |
| Export | `click` | GET `.../payroll/export/` | `#export-btn` | `outerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
