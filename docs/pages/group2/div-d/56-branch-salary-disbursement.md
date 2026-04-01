# 56 — Branch-wise Salary Disbursement Report

- **URL:** `/group/finance/payroll/salary-disbursement/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Role:** Payroll Coordinator G0 (read-only; data fed by external payroll software)

---

## 1. Purpose

The Branch-wise Salary Disbursement Report provides the Payroll Coordinator and Finance Manager with a consolidated view of salary disbursement status across all branches for each payroll month. Data is read from the external payroll software via API sync (triggered manually or scheduled). No payroll computation happens here — this page is purely reporting and status tracking.

Key information: branch-wise gross salary, net disbursement, salary payment status (pending/disbursed), bank transfer batch status, and reconciliation with the group's expense ledger.

---

## 2. Role Access

| Role | Level | Access |
|---|---|---|
| Group Payroll Coordinator | G0 | Read-only (all branches) |
| Group Finance Manager | G1 | Read + approve disbursement |
| Group CFO | G1 | Read — summary |
| Group Internal Auditor | G1 | Read — audit |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Finance → Payroll → Salary Disbursement Report
```

### 3.2 Page Header
- **Title:** `Branch-wise Salary Disbursement Report`
- **Subtitle:** `[Month Year] · Total Net Payroll: ₹[X] · Last Sync: [Datetime]`
- **Right-side controls:** `[Month ▾]` `[Branch ▾]` `[Sync ↻]` `[Export ↓]`

### 3.3 Alert Banner

| Condition | Banner | Severity |
|---|---|---|
| Disbursement not done by 30th | "[N] branch(es) salary not disbursed by 30th." | Red |
| Sync older than 24 hours | "Payroll data last synced [X] hours ago. Sync now for latest." | Amber |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule |
|---|---|---|
| Total Employees (Group) | Count | Neutral |
| Gross Salary (Month) | ₹ | Neutral |
| Total Deductions | ₹ | Neutral |
| Net Disbursement | ₹ | Neutral |
| Disbursed | ₹ | Green if = Net |
| Pending Disbursement | ₹ | Red if > 0 |

---

## 5. Main Table — Branch Summary

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Branch | Text | ✅ | ✅ |
| Employees | Count | ✅ | — |
| Gross Salary | ₹ | ✅ | — |
| PF Deduction | ₹ | ✅ | — |
| ESI Deduction | ₹ | ✅ | — |
| PT Deduction | ₹ | ✅ | — |
| TDS (Salary) | ₹ | ✅ | — |
| Other Deductions | ₹ | ✅ | — |
| Net Salary | ₹ | ✅ | — |
| Disbursement Status | Badge: Not Processed · Processing · Disbursed · Partially Disbursed | ✅ | ✅ |
| Disbursement Date | Date | ✅ | — |
| Bank Batch Reference | Text | ✅ | — |
| Actions | View Detail | — | — |

### 5.1 Filters
- Branch · Status · Month

### 5.2 Pagination
- 20 rows/page · Sort: Branch name

---

## 6. Drawers

### 6.1 Drawer: `branch-payroll-detail` — Branch Payroll Detail
- **Width:** 800px
- **Tabs:** Employee Summary · Deduction Breakup · Bank Transfer Log

**Employee Summary Tab:**

| Employee | Department | Gross | Deductions | Net | Status |
|---|---|---|---|---|---|
| [Name] | [Dept] | ₹ | ₹ | ₹ | Paid · Failed |

**Deduction Breakup Tab:**

| Deduction | Rate | Amount |
|---|---|---|
| PF (Employee) | 12% of basic | ₹ |
| ESI (Employee) | 0.75% of gross | ₹ |
| Profession Tax | State-specific | ₹ |
| TDS (Form 24Q) | As per slab | ₹ |
| Loan Deduction | Per schedule | ₹ |
| **Total** | | **₹** |

**Bank Transfer Log Tab:**

| Batch Date | Amount | UTR | Bank | Status |
|---|---|---|---|---|
| [Date] | ₹ | [UTR] | [Bank] | Successful · Failed |

---

## 7. Charts

### 7.1 Month-wise Net Payroll Trend (Bar — Last 12 Months)
### 7.2 Payroll by Branch (Horizontal Bar — current month)
### 7.3 Deduction Composition (Donut)
- **Segments:** PF · ESI · PT · TDS · Others

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Sync complete | "Payroll data synced from payroll software. [Month] data loaded." | Info | 4s |
| Export | "Salary disbursement report exported." | Info | 3s |
| Disbursement alert | "[Branch] salary disbursement overdue." | Warning | 5s |

---

## 9. Empty States

| Condition | Heading | Description |
|---|---|---|
| No data | "No payroll data" | "Sync payroll software to load disbursement data." |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Page load | Skeleton table |
| Sync | Progress bar: "Syncing from payroll software..." |
| Drawer | Spinner + tab skeleton |

---

## 11. Role-Based UI Visibility

| Element | Payroll Coord G0 | Finance Mgr G1 | CFO G1 |
|---|---|---|---|
| [Sync] | ✅ | ✅ | ❌ |
| View full employee detail | ✅ | ✅ | ❌ |
| View branch summary | ✅ | ✅ | ✅ |
| Export | ✅ | ✅ | ✅ |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/finance/payroll/disbursement/` | JWT (G0+) | Branch summary |
| POST | `/api/v1/group/{id}/finance/payroll/disbursement/sync/` | JWT (G0) | Sync from payroll |
| GET | `/api/v1/group/{id}/finance/payroll/disbursement/{bid}/` | JWT (G0+) | Branch detail |
| GET | `/api/v1/group/{id}/finance/payroll/disbursement/export/` | JWT (G0+) | Export |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Month filter | `change` | GET `.../disbursement/?month=` | `#payroll-table` | `innerHTML` |
| Sync | `click` | POST `.../disbursement/sync/` | `#sync-status` | `outerHTML` |
| Detail drawer | `click` | GET `.../disbursement/{id}/` | `#drawer-body` | `innerHTML` |
| Tab switch | `click` | GET `.../disbursement/{id}/?tab=deductions` | `#payroll-tab-content` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
