# 54 — Vendor Payment Tracker

- **URL:** `/group/finance/procurement/vendor-payments/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Role:** Procurement Finance G1 (primary) · Finance Manager G1 · Accounts Manager G1

---

## 1. Purpose

The Vendor Payment Tracker manages the full cycle of vendor payment processing — from approved invoice to payment confirmation. After the 3-way match (PO × Invoice × GRN) is confirmed on Page 53, the invoice enters the payment queue. This page tracks: invoice approval status, payment scheduling (batch payment runs), UTR/NEFT confirmation, TDS deduction at source, and payment advices sent to vendors.

Bulk payment runs are scheduled twice a month (1st and 16th). Urgent payments can be processed on-demand with Finance Manager approval.

---

## 2. Role Access

| Role | Level | Access |
|---|---|---|
| Group Procurement Finance | G1 | Read + prepare payment batch |
| Group Finance Manager | G1 | Full read + approve + mark paid |
| Group Accounts Manager | G1 | Read + record UTR |
| Group CFO | G1 | Read — high-value |
| Group Internal Auditor | G1 | Read — audit |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Finance → Procurement → Vendor Payment Tracker
```

### 3.2 Page Header
- **Title:** `Vendor Payment Tracker`
- **Subtitle:** `[N] Pending Payments · Total: ₹[X] · Next Batch Run: [Date]`
- **Right-side controls:** `[Month ▾]` `[Branch ▾]` `[Status ▾]` `[Export ↓]`

### 3.3 Alert Banner

| Condition | Banner | Severity |
|---|---|---|
| Payment overdue > 45 days | "[N] vendor invoice(s) overdue 45+ days. Risk of vendor dispute." | Red |
| TDS not deducted | "[N] payment(s) require TDS deduction before processing." | Amber |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule |
|---|---|---|
| Pending Payment Queue | Count + ₹ | Amber if > ₹5L |
| Approved for Payment | Count + ₹ | Neutral |
| Paid This Month | ₹ | Neutral |
| Overdue (> 30 days) | Count | Red if > 0 |
| TDS to Deduct | ₹ | Amber if > 0 |
| Advances Outstanding | ₹ | Informational |

---

## 5. Main Table — Payment Queue

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Invoice No | Text | ✅ | — |
| Vendor | Text | ✅ | ✅ |
| Branch | Text | ✅ | ✅ |
| PO Number | Text | ✅ | — |
| Invoice Date | Date | ✅ | — |
| Invoice Amount | ₹ | ✅ | — |
| TDS Deductible | ₹ | ✅ | — |
| Net Payable | ₹ | ✅ | — |
| Payment Due Date | Date | ✅ | — |
| Days to Due | Number (red if negative) | ✅ | — |
| Payment Status | Badge: Awaiting Approval · Approved · Scheduled · Paid · On Hold · Disputed | ✅ | ✅ |
| Payment Date | Date | ✅ | — |
| UTR / Reference | Text | ✅ | — |
| Actions | Approve · Mark Paid · Put On Hold | — | — |

### 5.1 Filters

| Filter | Type |
|---|---|
| Branch | Multi-select |
| Vendor | Multi-select |
| Status | Multi-select |
| Payment Due Date Range | Date picker |
| Amount Range | Number range |

### 5.2 Search
- Invoice number · Vendor · UTR

### 5.3 Pagination
- 25 rows/page · Sort: Payment Due Date asc

---

## 6. Drawers

### 6.1 Drawer: `payment-approve` — Approve Payment
- **Trigger:** Approve action (Finance Manager only)
- **Width:** 640px

**Invoice Summary:**
- Invoice No · Vendor · PO Link · 3-way match status

**TDS Deduction:**
| Section | Rate | TDS Amount |
|---|---|---|
| 194C (if contractor) | 2% | ₹[X] |
| 194J (if professional) | 10% | ₹[Y] |

| Field | Type | Required |
|---|---|---|
| Confirm TDS Deduction | Checkbox | ✅ |
| Payment Batch | Select: Next Regular Run · Urgent | ✅ |
| Approval Notes | Textarea | ❌ |

- [Approve Payment]

### 6.2 Drawer: `mark-paid` — Mark as Paid
| Field | Type | Required |
|---|---|---|
| Payment Date | Date | ✅ |
| Bank Account (from) | Select | ✅ |
| UTR / Reference No | Text | ✅ |
| Payment Mode | Select: NEFT · RTGS · IMPS · Cheque | ✅ |
| Amount Paid | Number | ✅ |
| Payment Proof | File upload | ❌ |
| Send Payment Advice | Toggle | — |

### 6.3 Drawer: `payment-detail` — Full Payment Detail
- **Width:** 760px
- Invoice → PO → GRN → Approval → Payment chain view
- All documents (invoice PDF, GRN, payment proof)

### 6.4 Drawer: `batch-payment-run` — Schedule Batch Run
- **Width:** 680px

**Payments selected for this run:**

| Vendor | Invoice | Net Payable | Bank Account |
|---|---|---|---|
| [Vendor] | [INV] | ₹ | [Account] |

**Total batch amount:** ₹[X] (from [N] invoices)

- [Download NEFT File] [Confirm Batch Dispatch]

---

## 7. Charts

### 7.1 Payment Status Distribution (Donut)
### 7.2 Monthly Vendor Payables Cleared (Bar)
### 7.3 Top 10 Vendors by Payable Amount (Horizontal Bar)

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Payment approved | "Invoice [No] approved for payment in [Batch]." | Success | 4s |
| Payment recorded | "Payment of ₹[X] to [Vendor] recorded. UTR: [No]." | Success | 4s |
| Batch confirmed | "Payment batch dispatched — [N] payments totalling ₹[X]." | Success | 4s |
| Hold placed | "Invoice [No] put on hold. Reason: [X]." | Warning | 4s |
| TDS missing | "TDS must be deducted before approving this payment." | Error | 5s |

---

## 9. Empty States

| Condition | Heading | Description |
|---|---|---|
| No pending | "No payments pending" | "All vendor invoices are processed." |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Page load | Skeleton KPIs + table |
| Drawer | Spinner |

---

## 11. Role-Based UI Visibility

| Element | Procurement Finance G1 | Finance Mgr G1 | Accounts Mgr G1 |
|---|---|---|---|
| [Approve Payment] | ❌ | ✅ | ❌ |
| [Mark Paid] | ❌ | ✅ | ✅ |
| [Batch Run] | ❌ | ✅ | ❌ |
| [Put On Hold] | ✅ | ✅ | ❌ |
| View all payments | ✅ | ✅ | ✅ |
| Export | ✅ | ✅ | ✅ |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/finance/procurement/vendor-payments/` | JWT (G1+) | Payment queue |
| POST | `/api/v1/group/{id}/finance/procurement/vendor-payments/{pid}/approve/` | JWT (G1, Finance Mgr) | Approve |
| POST | `/api/v1/group/{id}/finance/procurement/vendor-payments/{pid}/mark-paid/` | JWT (G1) | Record payment |
| POST | `/api/v1/group/{id}/finance/procurement/vendor-payments/{pid}/hold/` | JWT (G1) | Put on hold |
| POST | `/api/v1/group/{id}/finance/procurement/vendor-payments/batch/` | JWT (G1, Finance Mgr) | Batch run |
| GET | `/api/v1/group/{id}/finance/procurement/vendor-payments/export/` | JWT (G1+) | Export |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Filter | `change` | GET `.../vendor-payments/?status=&branch=` | `#payment-table` | `innerHTML` |
| Approve drawer | `click` | GET `.../vendor-payments/{id}/approve-form/` | `#drawer-body` | `innerHTML` |
| Mark paid drawer | `click` | GET `.../vendor-payments/{id}/mark-paid-form/` | `#drawer-body` | `innerHTML` |
| Submit approval | `submit` | POST `.../vendor-payments/{id}/approve/` | `#payment-row-{id}` | `outerHTML` |
| Submit payment | `submit` | POST `.../vendor-payments/{id}/mark-paid/` | `#payment-row-{id}` | `outerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
