# 15 — Monthly Branch Reconciliation

- **URL:** `/group/finance/reconciliation/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Roles:** Finance Manager G1 (primary) · Accounts Manager G1 · CFO G1

---

## 1. Purpose

Monthly Branch Reconciliation ensures that every branch's reported fee collections, expenses, and bank balance match the group's consolidated records. Each branch submits a monthly financial report to the group; this page tracks submission status, flags discrepancies, and manages the resolution workflow.

Reconciliation catches: under-reported collections, double entries, missing bank credits, and timing differences. An unreconciled branch is a financial governance failure. The Finance Manager investigates discrepancies, requests branch explanations, and signs off on reconciled reports.

---

## 2. Role Access

| Role | Level | Access |
|---|---|---|
| Group Finance Manager | G1 | Full read + comment + sign-off |
| Group Accounts Manager | G1 | Full read + comment |
| Group CFO | G1 | Read — summary only |
| Group Internal Auditor | G1 | Read — all (for audit trail) |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Finance → Monthly Branch Reconciliation
```

### 3.2 Page Header
- **Title:** `Monthly Branch Reconciliation`
- **Subtitle:** `[Month Year] · [N] Submitted · [X] Reconciled · [Y] Discrepancy · [Z] Pending`
- **Right-side controls:** `[Month ▾]` `[Branch ▾]` `[Status ▾]` `[Export ↓]`

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| Submission deadline passed (15th) with missing branches | "[N] branch(es) have not submitted the monthly report for [Month]." | Red |
| Discrepancy not resolved > 10 days | "[N] discrepancy(ies) unresolved for more than 10 days." | Red |
| All branches reconciled | "All branches reconciled for [Month]." | Success (green) |

---

## 4. Main Table — Branch Reconciliation Status

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Branch | Text | ✅ | ✅ |
| Submission Status | Badge: Submitted · Pending · Late | ✅ | ✅ |
| Submitted Date | Date | ✅ | — |
| Opening Balance (Branch) | ₹ | ✅ | — |
| Opening Balance (Group Ledger) | ₹ | ✅ | — |
| Fee Collected (Branch) | ₹ | ✅ | — |
| Fee Collected (Group Ledger) | ₹ | ✅ | — |
| Closing Balance (Branch) | ₹ | ✅ | — |
| Variance | ₹ (red if non-zero) | ✅ | — |
| Reconciliation Status | Badge: Matched · Discrepancy · Under Review · Reconciled | ✅ | ✅ |
| Sign-off | Badge: Pending · Signed Off | ✅ | ✅ |
| Actions | View · Comment · Sign Off · Request Resubmit | — | — |

### 4.1 Filters

| Filter | Type |
|---|---|
| Month | Month picker |
| Branch | Multi-select |
| Submission Status | Multi-select |
| Reconciliation Status | Multi-select |

### 4.2 Search
- Branch name · 300ms debounce

### 4.3 Pagination
- Server-side · 20 rows/page

---

## 5. Drawers

### 5.1 Drawer: `recon-detail` — Branch Reconciliation Detail
- **Trigger:** View action
- **Width:** 800px

**Tab: Summary**

| Item | Branch Report | Group Ledger | Variance |
|---|---|---|---|
| Opening Balance | ₹ | ₹ | ₹ |
| Fee Collected | ₹ | ₹ | ₹ |
| Other Income | ₹ | ₹ | ₹ |
| Total Credits | ₹ | ₹ | ₹ |
| Expenses Paid | ₹ | ₹ | ₹ |
| Transfers to Group | ₹ | ₹ | ₹ |
| Closing Balance | ₹ | ₹ | ₹ |

**Tab: Discrepancy Log**
| # | Item | Branch Amount | Ledger Amount | Variance | Root Cause | Status |
|---|---|---|---|---|---|---|
| 1 | [Item] | ₹ | ₹ | ₹ | [Reason] | Open · Resolved |

- [Add Discrepancy] [Mark Resolved]

**Tab: Comments**
- Threaded comments between Finance Manager and Branch Accountant
- [Add Comment]

**Tab: Documents**
- Branch report upload (PDF/Excel)
- Bank statement attachment

**Actions (bottom of drawer):**
- [Request Resubmit] — sends notification to branch
- [Sign Off] — marks reconciliation complete (Finance Manager only)

### 5.1.1 Sign-off Confirmation
- "Sign off reconciliation for [Branch] — [Month]?"
- Requires: Confirmation toggle + note (optional)
- Warning if variance > ₹0: "Sign off with unresolved variance of ₹[X]?"

---

## 6. Bulk Actions
- Select multiple branches → [Bulk Request Resubmit] · [Export Selected]

---

## 7. Charts

### 7.1 Reconciliation Status by Branch (Donut)
- **Segments:** Reconciled · Discrepancy · Pending

### 7.2 Variance Amount by Branch (Bar)
- **Sort:** Desc by variance
- **Colour:** Red = has variance · Green = zero

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Sign off | "Reconciliation signed off for [Branch] — [Month]." | Success | 4s |
| Request resubmit | "Resubmission requested from [Branch]. They have been notified." | Info | 4s |
| Comment added | "Comment added to [Branch] reconciliation." | Info | 3s |
| Discrepancy resolved | "Discrepancy marked as resolved for [Branch]." | Success | 3s |
| Export | "Reconciliation report exported." | Info | 3s |

---

## 9. Empty States

| Condition | Heading | Description |
|---|---|---|
| No submissions yet | "No reports submitted" | "No branches have submitted monthly reports for [Month] yet." |
| All reconciled | "All reconciled" | "All branch reports reconciled for [Month]." |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Page load | Skeleton KPIs + table skeleton |
| Month switch | Table skeleton |
| Detail drawer | Spinner + skeleton tabs |
| Sign-off action | Spinner on sign-off button |

---

## 11. Role-Based UI Visibility

| Element | Finance Mgr G1 | Accounts Mgr G1 | CFO G1 | Auditor G1 |
|---|---|---|---|---|
| [Sign Off] | ✅ | ❌ | ❌ | ❌ |
| [Request Resubmit] | ✅ | ✅ | ❌ | ❌ |
| [Add Comment] | ✅ | ✅ | ❌ | ✅ (read comments) |
| View all branches | ✅ | ✅ | ✅ | ✅ |
| Export | ✅ | ✅ | ✅ | ✅ |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/finance/reconciliation/` | JWT (G1+) | Reconciliation list |
| GET | `/api/v1/group/{id}/finance/reconciliation/{bid}/{month}/` | JWT (G1+) | Branch detail |
| POST | `/api/v1/group/{id}/finance/reconciliation/{bid}/{month}/sign-off/` | JWT (G1, Finance Mgr) | Sign off |
| POST | `/api/v1/group/{id}/finance/reconciliation/{bid}/{month}/request-resubmit/` | JWT (G1) | Request resubmit |
| POST | `/api/v1/group/{id}/finance/reconciliation/{bid}/{month}/comments/` | JWT (G1+) | Add comment |
| PUT | `/api/v1/group/{id}/finance/reconciliation/{bid}/{month}/discrepancy/{did}/resolve/` | JWT (G1) | Resolve discrepancy |
| GET | `/api/v1/group/{id}/finance/reconciliation/export/` | JWT (G1+) | Export |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Month switch | `change` | GET `.../reconciliation/?month=` | `#recon-table` | `innerHTML` |
| Search | `input delay:300ms` | GET `.../reconciliation/?q=` | `#recon-table-body` | `innerHTML` |
| Detail drawer | `click` | GET `.../reconciliation/{bid}/{month}/` | `#drawer-body` | `innerHTML` |
| Sign off | `click` | POST `.../reconciliation/{bid}/{month}/sign-off/` | `#recon-row-{id}` | `outerHTML` |
| Comments tab | `click` | GET `.../reconciliation/{bid}/{month}/comments/` | `#comments-tab-body` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
