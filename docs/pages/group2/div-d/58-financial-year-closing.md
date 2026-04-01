# 58 — Financial Year Closing Workflow

- **URL:** `/group/finance/fy-closing/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Role:** CFO G1 (primary) · Finance Manager G1

---

## 1. Purpose

The Financial Year Closing Workflow manages the structured end-of-year financial close process for the group. Closing a financial year requires completion of a multi-step checklist — reconciliations, audit sign-off, provisioning, tax filings, and ledger lock. Once the FY is locked, no further entries can be posted to that year.

The workflow ensures: all branch reconciliations are submitted and signed off, audit is formally closed for all branches, GST annual return (GSTR-9) is filed, TDS annual returns are filed, statutory audit report is uploaded, and the Balance Sheet is finalised.

Only the CFO can initiate the FY lock. The Finance Manager manages the pre-close checklist.

---

## 2. Role Access

| Role | Level | Access |
|---|---|---|
| Group CFO | G1 | Full — initiate close + FY lock |
| Group Finance Manager | G1 | Full — manage pre-close checklist |
| Group Internal Auditor | G1 | Read + confirm audit closure |
| Group GST/Tax Officer | G1 | Read + confirm GST filings |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Finance → FY Closing Workflow
```

### 3.2 Page Header
- **Title:** `Financial Year Closing — FY [Year]`
- **Subtitle:** `[X/Y] Pre-close tasks complete · Status: [Open / In Progress / Locked]`
- **Right-side controls:** `[FY ▾]` `[Export ↓]`

### 3.3 Alert Banner

| Condition | Banner | Severity |
|---|---|---|
| FY close date approaching | "FY [Year] closes in [N] days. [X] tasks remaining." | Amber |
| FY locked | "FY [Year] is locked. No further entries permitted." | Blue (informational) |

---

## 4. Pre-Close Checklist

Displayed as a step-by-step progress tracker:

### Step 1: Branch Reconciliations

| Branch | Monthly Recon Submitted | Signed Off | Status |
|---|---|---|---|
| [Branch A] | ✅ All 12 months | ✅ | Complete |
| [Branch B] | ✅ 11/12 | ❌ | Incomplete |

**Required:** All 12 monthly reconciliations submitted and signed off for all branches.

**[View Reconciliation Status →]** (links to Page 15)

---

### Step 2: Audit Closure

| Audit | Branch | Status |
|---|---|---|
| Q1 | [Branch] | Closed ✅ |
| Q2 | [Branch] | Pending ❌ |

**Required:** All quarterly audits formally closed.

**[View Audit Closure →]** (links to Page 43)

---

### Step 3: Tax Filings

| Filing | Due Date | Status |
|---|---|---|
| GSTR-9 (All GSTINs) | 31 Dec | Filed ✅ |
| Form 26Q (Q4) | 31 May | Pending ❌ |
| Form 24Q (Q4) | 31 May | Pending ❌ |
| Advance Tax (Final) | 15 Mar | Paid ✅ |

**[View Tax Calendar →]** (links to Page 47)

---

### Step 4: Provisions & Accruals

| Item | Amount | Status |
|---|---|---|
| Accrued Salaries | ₹[X] | Posted ✅ |
| Audit Fees Provision | ₹[X] | Posted ✅ |
| Bad Debt Provision | ₹[X] | Pending ❌ |
| Depreciation | ₹[X] | Pending ❌ |

**[Add Provision Entry]** — opens drawer for journal entry

---

### Step 5: Statutory Audit Report

| Item | Status |
|---|---|
| External Auditor Report uploaded | ❌ |
| Auditor Sign-off obtained | ❌ |
| Board Resolution uploaded | ❌ |

**[Upload Statutory Audit Report]**

---

### Step 6: Final Balance Sheet Review

- Trial balance exported and reviewed: ❌
- All inter-branch transfers reconciled: ❌
- Closing stock / asset register verified: ❌

**[View P&L Report →]** (links to Page 12)

---

### Step 7: FY Lock

**Enabled only when Steps 1–6 are all complete.**

| Field | Type | Required |
|---|---|---|
| Lock Date | Date | ✅ |
| CFO Confirmation | Checkbox: "I confirm FY [Year] is ready for lock" | ✅ |
| Lock Notes | Textarea | ✅ |

**[Lock Financial Year]** — irreversible; requires CFO credentials confirmation

---

## 5. Drawers

### 5.1 Drawer: `provision-entry` — Add Provision / Accrual
| Field | Type | Required |
|---|---|---|
| Account Head | Select | ✅ |
| Description | Text | ✅ |
| Amount | Number | ✅ |
| Narration | Textarea | ✅ |
| Reference | Text | ❌ |

- [Save Provision]

### 5.2 Drawer: `audit-report-upload` — Upload Statutory Report
| Field | Type | Required |
|---|---|---|
| Report Type | Select: Statutory Audit · Tax Audit · Internal Audit | ✅ |
| Auditor Name | Text | ✅ |
| Report Date | Date | ✅ |
| Report File | PDF upload | ✅ |
| Board Resolution | PDF upload | ❌ |

---

## 6. Progress Summary

| Milestone | Target Date | Status |
|---|---|---|
| All reconciliations | 15 April | ✅ |
| Audit closure | 30 April | ❌ Pending |
| Tax filings | 31 May | ❌ Pending |
| Provisions | 15 May | ❌ Pending |
| Statutory audit | 30 June | ❌ Not started |
| FY lock | 31 July | — |

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Provision saved | "Provision entry for [Account] saved — ₹[X]." | Success | 4s |
| Report uploaded | "Statutory audit report uploaded." | Success | 4s |
| FY locked | "FY [Year] is now locked. All entries are frozen." | Success | 6s |
| Lock blocked | "Cannot lock FY — [N] pre-close tasks incomplete." | Error | 5s |

---

## 8. Empty States

| Condition | Heading | Description |
|---|---|---|
| No FY selected | "Select financial year" | "Select a financial year to view the closing workflow." |

---

## 9. Loader States

| Trigger | Loader |
|---|---|
| Page load | Skeleton checklist |
| FY lock | Full-page progress: "Locking FY [Year]..." |
| Drawer | Spinner |

---

## 10. Role-Based UI Visibility

| Element | CFO G1 | Finance Mgr G1 | Internal Auditor G1 | Tax Officer G1 |
|---|---|---|---|---|
| [Lock Financial Year] | ✅ | ❌ | ❌ | ❌ |
| [Add Provision] | ✅ | ✅ | ❌ | ❌ |
| [Upload Audit Report] | ✅ | ✅ | ✅ | ❌ |
| View checklist | ✅ | ✅ | ✅ | ✅ |
| Export | ✅ | ✅ | ❌ | ❌ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/finance/fy-closing/{fy}/` | JWT (G1+) | Checklist status |
| POST | `/api/v1/group/{id}/finance/fy-closing/{fy}/provision/` | JWT (G1) | Add provision |
| POST | `/api/v1/group/{id}/finance/fy-closing/{fy}/audit-report/` | JWT (G1) | Upload report |
| POST | `/api/v1/group/{id}/finance/fy-closing/{fy}/lock/` | JWT (G1, CFO) | Lock FY |
| GET | `/api/v1/group/{id}/finance/fy-closing/{fy}/export/` | JWT (G1+) | Export checklist |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| FY select | `change` | GET `.../fy-closing/{fy}/` | `#fy-closing-content` | `innerHTML` |
| Provision drawer | `click` | GET `.../fy-closing/{fy}/provision-form/` | `#drawer-body` | `innerHTML` |
| Submit provision | `submit` | POST `.../fy-closing/{fy}/provision/` | `#provisions-list` | `beforeend` |
| FY lock | `click` | POST `.../fy-closing/{fy}/lock/` | `#fy-status` | `outerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
