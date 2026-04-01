# 06 — Group Scholarship Finance Officer Dashboard

- **URL:** `/group/finance/scholarship/`
- **Template:** `portal_base.html`
- **Priority:** P0
- **Role:** Group Scholarship Finance Officer (Role 35, G3)

---

## 1. Purpose

The Scholarship Finance Dashboard manages the financial lifecycle of all scholarship and grant disbursements across the group. This officer (G3) tracks merit and need-based internal scholarships, government scholarships (NSP, PRERANA, Post-Matric), and RTE reimbursements from state governments. Disbursement without proper tracking creates audit vulnerabilities — this page eliminates that risk.

Key functions: verifying student bank account details before disbursement, recording UTR numbers after transfer, tracking government grant claims submitted to state/central agencies, monitoring scholarship budget consumption, and managing the approval workflow for scholarship finance releases.

This role works closely with the Group Scholarship Manager (from Division C) who handles merit evaluation; the Finance Officer handles the money movement after approval.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Scholarship Finance Officer | G3 | Full read + disburse + track | Primary owner |
| Group CFO | G1 | Read — all sections | Cannot disburse |
| Group Finance Manager | G1 | Read — all sections | Cannot disburse |
| Group Scholarship Manager (Div C) | G3 | Read — approved scholarship list | Can view disbursement status |
| Group Internal Auditor | G1 | Read — all sections | Audit trail access |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Finance → Scholarship Finance Dashboard
```

### 3.2 Page Header
- **Title:** `Scholarship Finance Dashboard`
- **Subtitle:** `Scholarship & Grant Disbursement · AY [Year]`
- **Role Badge:** `Group Scholarship Finance Officer`
- **Right-side controls:** `[AY ▾]` `[Export ↓]`

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| Approved scholarships pending disbursement > 7 days | "[N] approved scholarships awaiting disbursement. Total: ₹[X]." | Red |
| Bank account not verified for pending disbursement | "[N] students missing verified bank accounts. Disbursement blocked." | Red |
| Government grant claim overdue submission | "Grant claim for [Scheme] due on [Date]. Not yet submitted." | Amber |
| RTE reimbursement claim pending state response > 60 days | "RTE reimbursement claim submitted [Date] — no response in 60 days." | Amber |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Total Scholarships Approved | Count (AY) | Informational | → Page 37 |
| Amount Disbursed (AY) | ₹ | Informational | → Page 34 |
| Pending Disbursement | Count + ₹ | Red if > 0 | → Page 34 |
| Government Grants Received (AY) | ₹ | Informational | → Page 35 |
| RTE Claims Pending | Count | Amber if > 0 | → Page 38 |
| Scholarship Budget Utilised % | % | Green < 90% · Amber 90–100% · Red > 100% | → Page 36 |

---

## 5. Section 5.1 — Disbursement Queue

| Column | Type | Sortable |
|---|---|---|
| Student Name | Text | ✅ |
| Branch | Text | ✅ |
| Scholarship Type | Badge | ✅ |
| Approved Amount | ₹ | ✅ |
| Bank Account Status | Badge: Verified · Unverified · Missing | ✅ |
| Approved Date | Date | ✅ |
| Actions | Disburse · View · Request Bank Details | — |

**Filters:** Branch · Scholarship Type · Bank Status · Approval Date range
**Search:** Student name · 300ms debounce
**Pagination:** 20 rows/page
**Bulk action:** [Bulk Disburse] (only for bank-verified students)

---

## 5.2 Section 5.2 — Government Grant Summary

| Column | Type | Sortable |
|---|---|---|
| Scheme | Text | ✅ |
| Agency | Text (NSP / State Govt / PRERANA) | ✅ |
| Claim Amount | ₹ | ✅ |
| Students Covered | Count | ✅ |
| Submitted Date | Date | ✅ |
| Status | Badge: Claim Submitted · Received · Pending · Rejected | ✅ |
| Amount Received | ₹ | ✅ |
| Actions | View · Update Status | — |

**[View Full Grant Tracker →]** links to Page 35.

---

## 5.3 Section 5.3 — Scholarship Budget Snapshot

| Budget Line | Allocated | Disbursed | Balance | % Used |
|---|---|---|---|---|
| Merit Scholarship | ₹ | ₹ | ₹ | % |
| Need-Based Scholarship | ₹ | ₹ | ₹ | % |
| RTE (reimbursable) | ₹ | ₹ | ₹ | % |
| Govt. Grants (pass-through) | ₹ | ₹ | ₹ | % |

**[View Full Budget →]** links to Page 36.

---

## 6. Charts

### 6.1 Disbursement by Scholarship Type (Donut)
- **Segments:** Merit · Need-Based · Govt · RTE
- **Centre:** "₹[Total] disbursed"

### 6.2 Monthly Disbursement Trend (Bar)
- **X-axis:** Months of AY
- **Y-axis:** ₹ disbursed

---

## 7. Drawers

### 7.1 Drawer: `disburse` — Record Disbursement
- **Trigger:** Disburse action on student
- **Width:** 580px

| Field | Type | Required | Validation |
|---|---|---|---|
| Student Name | Read-only | — | |
| Scholarship Type | Read-only | — | |
| Approved Amount | ₹ (read-only) | — | |
| Disbursement Date | Date | ✅ | ≤ Today |
| Payment Mode | Select | ✅ | NEFT · RTGS · DD · Cash |
| Bank / UTR Reference | Text | ✅ | Required for NEFT/RTGS |
| Remarks | Textarea | ❌ | |

- [Cancel] [Record Disbursement]

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Disbursement recorded | "Disbursement of ₹[X] recorded for [Student]. UTR: [Y]." | Success | 4s |
| Bulk disburse | "[N] disbursements recorded. Total: ₹[X]." | Success | 5s |
| Bank details requested | "Bank detail request sent to [Branch] for [Student]." | Info | 3s |
| Export | "Scholarship finance report exported." | Info | 3s |

---

## 9. Empty States

| Condition | Heading | Description |
|---|---|---|
| No pending disbursements | "No pending disbursements" | "All approved scholarships have been disbursed." |
| No government grants | "No grant claims" | "No government grant claims recorded for this AY." |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Page load | Skeleton KPIs + 3 section skeletons |
| Disburse drawer | Spinner + skeleton fields |
| Bulk disburse | Progress bar: "[N] of [M] processed" |

---

## 11. Role-Based UI Visibility

| Element | Scholarship Finance G3 | CFO G1 | Finance Mgr G1 | Auditor G1 |
|---|---|---|---|---|
| [Disburse] action | ✅ | ❌ | ❌ | ❌ |
| [Bulk Disburse] | ✅ | ❌ | ❌ | ❌ |
| [Request Bank Details] | ✅ | ❌ | ❌ | ❌ |
| View all sections | ✅ | ✅ | ✅ | ✅ |
| Export | ✅ | ✅ | ✅ | ✅ |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/finance/scholarship/kpis/` | JWT (G1+) | KPI cards |
| GET | `/api/v1/group/{id}/finance/scholarship/disbursement-queue/` | JWT (G1+) | Pending disbursements |
| POST | `/api/v1/group/{id}/finance/scholarship/disburse/{sid}/` | JWT (G3) | Record disbursement |
| POST | `/api/v1/group/{id}/finance/scholarship/bulk-disburse/` | JWT (G3) | Bulk disbursement |
| GET | `/api/v1/group/{id}/finance/scholarship/grants/` | JWT (G1+) | Government grants list |
| GET | `/api/v1/group/{id}/finance/scholarship/budget/` | JWT (G1+) | Budget snapshot |
| GET | `/api/v1/group/{id}/finance/scholarship/export/` | JWT (G1+) | Export |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Search | `input delay:300ms` | GET `.../disbursement-queue/?q=` | `#disburse-table-body` | `innerHTML` |
| Filter | `change` | GET `.../disbursement-queue/?type=` | `#disburse-section` | `innerHTML` |
| Disburse drawer | `click` | GET `.../disburse/{id}/form/` | `#drawer-body` | `innerHTML` |
| Submit disbursement | `submit` | POST `.../disburse/{id}/` | `#drawer-body` | `innerHTML` |
| Pagination | `click` | GET `.../disbursement-queue/?page=` | `#disburse-section` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
