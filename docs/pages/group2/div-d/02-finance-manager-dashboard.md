# 02 — Group Finance Manager Dashboard

- **URL:** `/group/finance/manager/`
- **Template:** `portal_base.html`
- **Priority:** P0
- **Role:** Group Finance Manager (Role 31, G1)

---

## 1. Purpose

The Finance Manager Dashboard is the operational hub for day-to-day cross-branch financial management. While the CFO has strategic oversight, the Finance Manager executes monthly reconciliations, tracks audit report status, and monitors branch-level financial health indicators. This role bridges between the CFO's strategic view and the transactional work done by branch accountants.

The dashboard surfaces which branches have submitted monthly reports, which reconciliations are pending or have discrepancies, and which audit reports are awaiting sign-off. The Finance Manager is the primary escalation point when branch-level anomalies — unmatched bank entries, unexplained variances — are detected. Every alert on this page represents an action item the Finance Manager must resolve or escalate to the CFO.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Finance Manager | G1 | Full read — all sections | Primary owner; no data entry |
| Group CFO / Finance Director | G1 | Read — all sections | Can view but this is the manager's workspace |
| Group Internal Auditor | G1 | Read — Section 5.3 (audit report status) only | |

> **Enforcement:** G1 = read-only access. No create/edit/delete actions are available.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Finance → Finance Manager Dashboard
```

### 3.2 Page Header
- **Title:** `Finance Manager Dashboard`
- **Subtitle:** `Reconciliation & Audit Reports · FY [Year] · Month: [Month]`
- **Role Badge:** `Group Finance Manager`
- **Right-side controls:** `[Financial Year ▾]` `[Month ▾]` `[Export ↓]`

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| Branch reconciliation overdue (> 15th of month) | "[N] branch(es) have not submitted monthly reports for [Month]." | Red |
| Reconciliation discrepancy detected | "Discrepancy of ₹[X] detected in [Branch]. Investigate immediately." | Red |
| Audit report pending sign-off > 7 days | "[N] audit reports pending Finance Manager sign-off." | Amber |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Reconciliations Submitted | Branches submitted / Total for month | Green = 100% · Amber < 100% · Red < 75% | → Page 15 |
| Reconciliation Discrepancies | Count of unresolved discrepancies | Green = 0 · Red > 0 | → Page 15 |
| Audit Reports Pending | Reports awaiting sign-off | Green = 0 · Amber 1–3 · Red > 3 | → Page 16 |
| Total Variance This Month | ₹ sum of all unresolved variances | Red if > ₹0 | → Page 15 |
| Branch Financial Health Score | Avg health score across branches | Green ≥ 80 · Amber 60–79 · Red < 60 | → Page 17 |

---

## 5. Section 5.1 — Monthly Reconciliation Status Table

| Column | Type | Sortable |
|---|---|---|
| Branch | Text | ✅ |
| Report Submitted | Badge (Yes / No / Late) | ✅ |
| Submitted Date | Date | ✅ |
| Opening Balance | ₹ | ✅ |
| Closing Balance | ₹ | ✅ |
| Variance | ₹ (red if non-zero) | ✅ |
| Status | Badge: Matched · Discrepancy · Pending | ✅ |
| Actions | View · Comment | — |

**Filters:** Branch · Month · Status
**Search:** Branch name
**Pagination:** 20 rows/page

**[View Full Reconciliation →]** links to Page 15.

---

## 5.2 Section 5.2 — Audit Report Queue

| Column | Type | Sortable |
|---|---|---|
| Report Title | Text | ✅ |
| Branch | Text | ✅ |
| Submitted By | Text | ✅ |
| Date Submitted | Date | ✅ |
| Type | Badge: Monthly · Quarterly · Annual | ✅ |
| Status | Badge: Awaiting Review · Under Review · Signed Off · Rejected | ✅ |
| Actions | Review · Sign Off · Reject | — |

**[View All Reports →]** links to Page 16.

---

## 5.3 Section 5.3 — Branch Financial Health Monitor

| Column | Type | Notes |
|---|---|---|
| Branch | Text | |
| Health Score | Number (0–100) | Colour-coded |
| Collection Rate % | % | |
| Outstanding Dues % | % | |
| Last Report Date | Date | |
| Trend | Sparkline | 6-month |

**[View Full Health Report →]** links to Page 17.

---

## 6. Charts

### 6.1 Monthly Reconciliation Completion % (Bar)
- **X-axis:** Branches
- **Y-axis:** % completion
- **Colour:** Green ≥ 100% · Red < 100%

### 6.2 Variance by Branch (Bar)
- **Data:** Unresolved variance ₹ per branch
- **Colour:** Red = has variance · Grey = zero variance

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Audit report signed off | "Audit report signed off for [Branch]." | Success | 3s |
| Audit report rejected | "Report rejected. Branch notified to resubmit." | Warning | 4s |
| Export triggered | "Report export ready." | Info | 3s |

---

## 8. Empty States

| Condition | Heading | Description |
|---|---|---|
| All reconciliations matched | "All reconciled" | "All branches have matched reconciliations for this month." |
| No audit reports pending | "No pending reports" | "All audit reports are reviewed and signed off." |

---

## 9. Loader States

| Trigger | Loader |
|---|---|
| Page load | Skeleton KPIs + two table skeletons |
| Month switch | Inline skeleton on reconciliation table |
| Sign-off action | Spinner on sign-off button |

---

## 10. Role-Based UI Visibility

| Element | Finance Mgr G1 | CFO G1 | Internal Auditor G1 |
|---|---|---|---|
| Reconciliation table | ✅ | ✅ | ❌ |
| Audit Report Queue | ✅ | ✅ | ✅ |
| [Sign Off] action | ✅ | ❌ | ❌ |
| Branch Health table | ✅ | ✅ | ❌ |
| Export | ✅ | ✅ | ❌ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/finance/manager/kpis/` | JWT (G1+) | KPI cards |
| GET | `/api/v1/group/{id}/finance/manager/reconciliation-status/` | JWT (G1+) | Reconciliation table |
| GET | `/api/v1/group/{id}/finance/manager/audit-queue/` | JWT (G1+) | Audit report queue |
| PUT | `/api/v1/group/{id}/finance/manager/audit-reports/{rid}/sign-off/` | JWT (G1) | Sign off report |
| PUT | `/api/v1/group/{id}/finance/manager/audit-reports/{rid}/reject/` | JWT (G1) | Reject report |
| GET | `/api/v1/group/{id}/finance/manager/branch-health/` | JWT (G1+) | Branch health table |
| GET | `/api/v1/group/{id}/finance/manager/export/` | JWT (G1+) | Export report |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Month switch | `change` | GET `.../reconciliation-status/?month=` | `#recon-table` | `innerHTML` |
| Sign off | `click` | PUT `.../audit-reports/{id}/sign-off/` | `#report-row-{id}` | `outerHTML` |
| Page load KPIs | `load` | GET `.../manager/kpis/` | `#kpi-bar` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
