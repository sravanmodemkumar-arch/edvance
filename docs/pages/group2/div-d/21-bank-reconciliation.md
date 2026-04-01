# 21 — Bank Reconciliation Statement

- **URL:** `/group/finance/bank-recon/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Roles:** Accounts Manager G1 (primary) · Finance Manager G1 · CFO G1

---

## 1. Purpose

The Bank Reconciliation Statement page tracks the reconciliation of each branch's bank account(s) against the group's internal cash/fee ledger. Every month, branch accountants submit bank statements and the Accounts Manager reconciles: credits that appear in the bank but not in the ledger (e.g., direct deposits from parents), debits in the ledger not yet cleared in the bank, and timing differences.

Unreconciled entries are the primary indicator of either missing transactions in the ledger or fraud. This page surfaces all such entries, tracks their resolution, and maintains a monthly reconciliation sign-off trail required by the statutory auditor.

---

## 2. Role Access

| Role | Level | Access |
|---|---|---|
| Group Accounts Manager | G1 | Full read + upload bank statement + mark reconciled |
| Group Finance Manager | G1 | Full read + sign off |
| Group CFO | G1 | Read — status overview |
| Group Internal Auditor | G1 | Read — all (audit trail) |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Finance → Bank Reconciliation Statement
```

### 3.2 Page Header
- **Title:** `Bank Reconciliation Statement`
- **Subtitle:** `[Month Year] · [N] Bank Accounts · [X] Reconciled · [Y] Pending`
- **Right-side controls:** `[Month ▾]` `[Branch ▾]` `[+ Upload Bank Statement]` `[Export ↓]`

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| Bank statement not uploaded for any branch | "[N] branch bank statement(s) not uploaded for [Month]." | Amber |
| Unreconciled entries > ₹50,000 | "Unreconciled entries totalling ₹[X] in [Branch]. Investigate immediately." | Red |
| Reconciliation not signed off by 20th | "[N] branch reconciliation(s) not signed off for [Month]." | Amber |

---

## 4. Main Table — Bank Account Reconciliation Status

| Column | Type | Sortable |
|---|---|---|
| Branch | Text | ✅ |
| Bank Name | Text | ✅ |
| Account Number | Text (masked) | ✅ |
| Account Type | Badge: Current · Savings | ✅ |
| Statement Uploaded | Badge: Yes · No | ✅ |
| Bank Closing Balance | ₹ | ✅ |
| Ledger Closing Balance | ₹ | ✅ |
| Difference | ₹ (red if non-zero) | ✅ |
| Unreconciled Entries | Count | ✅ |
| Status | Badge: Reconciled · Pending · Discrepancy | ✅ |
| Sign-off | Badge: Signed Off · Pending | ✅ |
| Actions | View Recon · Upload Statement · Sign Off | — |

### 4.1 Filters

| Filter | Type |
|---|---|
| Branch | Multi-select |
| Status | Multi-select |
| Month | Month picker |

### 4.2 Search
- Branch name · Bank name

### 4.3 Pagination
- Server-side · 20 rows/page

---

## 5. Drawers

### 5.1 Drawer: `bank-recon-detail` — Bank Reconciliation Workbook
- **Trigger:** View Recon action
- **Width:** 900px

**Section A: Opening Balances**

| Item | As per Bank | As per Ledger | Difference |
|---|---|---|---|
| Opening Balance | ₹ | ₹ | ₹ |

**Section B: Transactions in Bank but not in Ledger**

| Date | Particulars | Amount | Reason | Action |
|---|---|---|---|---|
| [Date] | Parent transfer (NEFT) | ₹ | Not posted to ledger yet | [Mark Posted] |

**Section C: Transactions in Ledger but not in Bank**

| Date | Particulars | Amount | Reason | Action |
|---|---|---|---|---|
| [Date] | Cheque issued but not cleared | ₹ | Cheque in transit | [Mark Cleared] |

**Section D: Closing Balances**

| Item | As per Bank | As per Ledger | Difference |
|---|---|---|---|
| Closing Balance | ₹ | ₹ | ₹ (should be ₹0 after recon) |

**Actions:**
- [Mark Entry Reconciled]
- [Add Explanation]
- [Sign Off Reconciliation] (Finance Manager)

### 5.2 Drawer: `upload-statement` — Upload Bank Statement
| Field | Type | Required |
|---|---|---|
| Branch | Select | ✅ |
| Bank Account | Select | ✅ |
| Month | Month picker | ✅ |
| Bank Statement | File (PDF/Excel) | ✅ |
| Closing Balance (as per bank) | Number | ✅ |

---

## 6. Charts

### 6.1 Reconciliation Status Overview (Donut)
- **Segments:** Reconciled · Pending · Discrepancy

### 6.2 Unreconciled Entry Count by Branch (Bar)
- **Sort:** Desc

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Statement uploaded | "Bank statement uploaded for [Branch] — [Month]." | Success | 4s |
| Entry reconciled | "Entry reconciled for [Branch]." | Success | 3s |
| Signed off | "Bank reconciliation signed off for [Branch] — [Month]." | Success | 4s |
| Export | "Bank reconciliation exported." | Info | 3s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No statements uploaded | "No bank statements" | "Upload branch bank statements to begin reconciliation." | [+ Upload Bank Statement] |
| All reconciled | "All accounts reconciled" | "All bank accounts reconciled for [Month]." | — |

---

## 9. Loader States

| Trigger | Loader |
|---|---|
| Page load | Skeleton table |
| Month switch | Table skeleton |
| Detail drawer | Spinner + workbook skeleton |

---

## 10. Role-Based UI Visibility

| Element | Accounts Mgr G1 | Finance Mgr G1 | CFO G1 |
|---|---|---|---|
| [Upload Statement] | ✅ | ❌ | ❌ |
| [Mark Reconciled] | ✅ | ❌ | ❌ |
| [Sign Off] | ❌ | ✅ | ❌ |
| View reconciliation workbook | ✅ | ✅ | ✅ (summary) |
| Export | ✅ | ✅ | ✅ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/finance/bank-recon/` | JWT (G1+) | Recon status list |
| GET | `/api/v1/group/{id}/finance/bank-recon/{bid}/{month}/` | JWT (G1+) | Recon workbook |
| POST | `/api/v1/group/{id}/finance/bank-recon/upload/` | JWT (G1) | Upload statement |
| PUT | `/api/v1/group/{id}/finance/bank-recon/{bid}/{month}/entry/{eid}/reconcile/` | JWT (G1) | Mark entry reconciled |
| POST | `/api/v1/group/{id}/finance/bank-recon/{bid}/{month}/sign-off/` | JWT (G1, Finance Mgr) | Sign off |
| GET | `/api/v1/group/{id}/finance/bank-recon/export/` | JWT (G1+) | Export |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Month switch | `change` | GET `.../bank-recon/?month=` | `#recon-table` | `innerHTML` |
| Detail drawer | `click` | GET `.../bank-recon/{bid}/{month}/` | `#drawer-body` | `innerHTML` |
| Mark reconciled | `click` | PUT `.../bank-recon/{bid}/{month}/entry/{eid}/reconcile/` | `#entry-row-{id}` | `outerHTML` |
| Upload drawer | `click` | GET `.../bank-recon/upload-form/` | `#drawer-body` | `innerHTML` |
| Submit upload | `submit` | POST `.../bank-recon/upload/` | `#drawer-body` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
