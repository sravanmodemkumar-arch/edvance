# 34 — Scholarship Disbursement Tracker

- **URL:** `/group/finance/scholarship/disbursements/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Role:** Scholarship Finance Officer G3 (primary) · CFO G1 · Finance Manager G1

---

## 1. Purpose

The Scholarship Disbursement Tracker maintains a complete record of all scholarship amounts disbursed to students — merit scholarships, need-based scholarships, and government scholarships. It tracks the full disbursement workflow: from scholarship approval (by the Group Scholarship Manager in Division C) through bank account verification, payment, UTR recording, and confirmation.

Every disbursement must be traceable: who approved it, when was the bank account verified, when was the transfer made, what is the UTR, and has the student confirmed receipt. This trace is mandatory for government grant audits and statutory auditor reviews.

---

## 2. Role Access

| Role | Level | Access |
|---|---|---|
| Group Scholarship Finance Officer | G3 | Full read + disburse + export |
| Group CFO | G1 | Read — amounts + status |
| Group Finance Manager | G1 | Read + export |
| Group Internal Auditor | G1 | Read — full audit trail |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Finance → Scholarship Finance → Disbursement Tracker
```

### 3.2 Page Header
- **Title:** `Scholarship Disbursement Tracker`
- **Subtitle:** `AY [Year] · [N] Disbursements · ₹[Total] Disbursed`
- **Right-side controls:** `[AY ▾]` `[Scholarship Type ▾]` `[Branch ▾]` `[Status ▾]` `[Export ↓]`

### 3.3 Alert Banner

| Condition | Banner | Severity |
|---|---|---|
| Approved scholarships pending disbursement > 7 days | "[N] scholarships approved but not disbursed for 7+ days." | Red |
| Bank accounts missing | "[N] students missing verified bank account. Disbursement blocked." | Red |

---

## 4. Main Table

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Student Name | Text | ✅ | — |
| Student ID | Text | ✅ | — |
| Branch | Text | ✅ | ✅ |
| Class / Stream | Text | ✅ | — |
| Scholarship Type | Badge: Merit · Need-Based · Govt · RTE | ✅ | ✅ |
| Scholarship Scheme | Text | ✅ | — |
| Approved Amount | ₹ | ✅ | — |
| Disbursed Amount | ₹ | ✅ | — |
| Bank Account Status | Badge: Verified · Unverified · Missing | ✅ | ✅ |
| Disbursement Date | Date | ✅ | — |
| UTR / Reference | Text | ✅ | — |
| Status | Badge: Approved · Bank Pending · Ready to Disburse · Disbursed · Failed | ✅ | ✅ |
| Actions | View · Disburse · Request Bank Details | — | — |

### 4.1 Filters

| Filter | Type |
|---|---|
| Scholarship Type | Multi-select |
| Status | Multi-select |
| Branch | Multi-select |
| Bank Account Status | Multi-select |
| AY | Select |
| Date Range | Disbursement date range |

### 4.2 Search
- Student name · Student ID

### 4.3 Pagination
- 25 rows/page · Sort: Status (Ready to Disburse first)

### 4.4 Bulk Actions
- Select bank-verified students → [Bulk Disburse] (generates batch payment file)

---

## 5. Drawers

### 5.1 Drawer: `disbursement-detail` — View Full Disbursement Record
- **Trigger:** View action
- **Width:** 720px

**Tab: Student & Scholarship**
| Field | Value |
|---|---|
| Student | Name · ID · Branch · Class |
| Scholarship Type | [Type] |
| Scholarship Scheme | [Scheme Name] |
| Approved By | [Name] ([Date]) |
| Approved Amount | ₹[X] |
| Purpose | [Tuition Fee Assistance / Hostel Fee / All] |

**Tab: Bank Details**
| Field | Value |
|---|---|
| Account Holder Name | [Name] |
| Bank Name | [Bank] |
| Account Number | [XXXX masked] |
| IFSC Code | [Code] |
| Verification Status | [Badge] |
| Verified By | [Name] ([Date]) |

**Tab: Disbursement Record**
| Field | Value |
|---|---|
| Disbursed Amount | ₹[X] |
| Payment Date | [Date] |
| Payment Mode | NEFT / RTGS / Cheque |
| UTR Number | [UTR] |
| Disbursed By | [Name] |
| Student Confirmation | [Received / Pending] |

**Tab: Audit Trail**
- Full chronological log of all actions

### 5.2 Drawer: `disburse-form` — Record Disbursement
| Field | Type | Required |
|---|---|---|
| Student | Read-only | — |
| Approved Amount | Read-only | — |
| Disbursement Date | Date | ✅ |
| Payment Mode | Select: NEFT · RTGS · DD | ✅ |
| UTR / Reference | Text | ✅ |
| Disbursed Amount | Number | ✅ |
| Remarks | Textarea | ❌ |

### 5.3 Drawer: `bank-request` — Request Bank Details
- Sends notification to branch to collect and verify student bank details
- Fields: Branch · Student · Deadline

---

## 6. Charts

### 6.1 Disbursement Status Pipeline (Funnel)
- Stages: Approved → Bank Verified → Disbursed

### 6.2 Monthly Disbursement Amount (Bar)
- **X-axis:** Months
- **Y-axis:** ₹

### 6.3 Disbursement by Scholarship Type (Donut)

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Disbursement recorded | "₹[X] disbursed to [Student]. UTR: [Y]." | Success | 4s |
| Bulk disburse queued | "Batch disbursement for [N] students queued." | Info | 4s |
| Bank request sent | "Bank detail request sent to [Branch] for [Student]." | Info | 3s |
| Export | "Disbursement report exported." | Info | 3s |

---

## 8. Empty States

| Condition | Heading | Description |
|---|---|---|
| No pending disbursements | "No pending disbursements" | "All approved scholarships have been disbursed." |

---

## 9. Loader States

| Trigger | Loader |
|---|---|
| Page load | Skeleton table |
| Filter change | Table skeleton |
| Disburse drawer | Spinner + fields |
| Bulk disburse | Progress bar |

---

## 10. Role-Based UI Visibility

| Element | Scholarship Finance G3 | CFO G1 | Finance Mgr G1 |
|---|---|---|---|
| [Disburse] | ✅ | ❌ | ❌ |
| [Bulk Disburse] | ✅ | ❌ | ❌ |
| [Request Bank Details] | ✅ | ❌ | ❌ |
| View all | ✅ | ✅ | ✅ |
| Export | ✅ | ✅ | ✅ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/finance/scholarship/disbursements/` | JWT (G1+) | Disbursement list |
| GET | `/api/v1/group/{id}/finance/scholarship/disbursements/{sid}/` | JWT (G1+) | Detail |
| POST | `/api/v1/group/{id}/finance/scholarship/disbursements/{sid}/disburse/` | JWT (G3) | Record disbursement |
| POST | `/api/v1/group/{id}/finance/scholarship/disbursements/bulk-disburse/` | JWT (G3) | Bulk disbursement |
| POST | `/api/v1/group/{id}/finance/scholarship/disbursements/{sid}/request-bank/` | JWT (G3) | Request bank details |
| GET | `/api/v1/group/{id}/finance/scholarship/disbursements/export/` | JWT (G1+) | Export |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Search | `input delay:300ms` | GET `.../disbursements/?q=` | `#disburse-table-body` | `innerHTML` |
| Filter | `change` | GET `.../disbursements/?type=&status=` | `#disburse-section` | `innerHTML` |
| Detail drawer | `click` | GET `.../disbursements/{id}/` | `#drawer-body` | `innerHTML` |
| Disburse form | `click` | GET `.../disbursements/{id}/disburse-form/` | `#drawer-body` | `innerHTML` |
| Submit disburse | `submit` | POST `.../disbursements/{id}/disburse/` | `#drawer-body` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
