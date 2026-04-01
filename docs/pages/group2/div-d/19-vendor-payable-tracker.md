# 19 — Vendor Payable Tracker

- **URL:** `/group/finance/vendor-payable/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Roles:** Accounts Manager G1 (primary) · Procurement Finance G1 · Finance Manager G1

---

## 1. Purpose

The Vendor Payable Tracker manages all outstanding invoices from vendors supplying goods and services to the group: textbook publishers, uniform manufacturers, lab equipment suppliers, IT vendors, maintenance contractors, and catering vendors. The Accounts Manager tracks payment status, payment due dates, and payment modes to prevent supply disruptions from delayed payments.

This page also flags potential duplicate invoices (same vendor, same amount, close dates) and enables the Accounts Manager to maintain a clean vendor ledger. Payment authorisation happens externally (in the banking system), but the Accounts Manager updates payment status here to keep the group ledger current.

---

## 2. Role Access

| Role | Level | Access |
|---|---|---|
| Group Accounts Manager | G1 | Full read + update payment status |
| Group Procurement Finance | G1 | Full read + mark payment made |
| Group Finance Manager | G1 | Full read |
| Group Internal Auditor | G1 | Read — audit access |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Finance → Vendor Payable Tracker
```

### 3.2 Page Header
- **Title:** `Vendor Payable Tracker`
- **Subtitle:** `[N] Invoices Outstanding · Total: ₹[X] · Overdue: ₹[Y]`
- **Right-side controls:** `[FY ▾]` `[Branch ▾]` `[Category ▾]` `[+ Log Invoice]` `[Export ↓]`

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| Invoices overdue > 30 days | "[N] invoices overdue by 30+ days. Total: ₹[X]. Vendor relations at risk." | Red |
| Potential duplicate detected | "Potential duplicate invoice detected: [Vendor] submitted similar invoice on [Date]." | Amber |
| Vendor with all invoices overdue | "All invoices from [Vendor] are overdue. Possible supply stoppage risk." | Red |

---

## 4. Main Table

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Invoice Number | Text | ✅ | — |
| Vendor | Text | ✅ | ✅ |
| Category | Badge: Books · Uniforms · Lab · IT · Maintenance · Catering · Other | ✅ | ✅ |
| Branch | Text | ✅ | ✅ |
| Invoice Date | Date | ✅ | — |
| Due Date | Date | ✅ | — |
| Invoice Amount | ₹ | ✅ | — |
| Amount Paid | ₹ | ✅ | — |
| Balance | ₹ | ✅ | — |
| Age (Days) | Number (red if >30) | ✅ | — |
| Status | Badge: Unpaid · Partially Paid · Paid · Overdue · Disputed | ✅ | ✅ |
| Duplicate Flag | Badge: ⚠️ if flagged | ✅ | ✅ |
| Actions | View · Mark Paid · Dispute | — | — |

### 4.1 Filters

| Filter | Type |
|---|---|
| Vendor | Multi-select |
| Category | Multi-select |
| Branch | Multi-select |
| Status | Multi-select |
| Age | Select: All · 0–30 · 31–60 · 61–90 · >90 days |
| Date Range | Date picker |

### 4.2 Search
- Invoice number · Vendor name · 300ms debounce

### 4.3 Pagination
- Server-side · 25 rows/page · Default sort: Due date ascending (oldest due first)

### 4.4 Bulk Actions
- Select rows → [Bulk Mark Paid] · [Export Selected]

---

## 5. Drawers

### 5.1 Drawer: `invoice-log` — Log New Invoice
- **Trigger:** [+ Log Invoice]
- **Width:** 600px

| Field | Type | Required | Validation |
|---|---|---|---|
| Vendor | Select | ✅ | From vendor master |
| Category | Select | ✅ | |
| Branch | Select | ✅ | |
| Invoice Number | Text | ✅ | Unique per vendor |
| Invoice Date | Date | ✅ | |
| Due Date | Date | ✅ | ≥ Invoice date |
| Invoice Amount | Number | ✅ | > 0 |
| GST Amount | Number | ❌ | |
| Linked PO | Select | ❌ | Link to PO register |
| Attachment | File upload | ❌ | PDF max 20MB |
| Notes | Textarea | ❌ | |

- [Cancel] [Log Invoice]

### 5.2 Drawer: `invoice-detail` — Invoice Detail
- **Trigger:** View action
- **Width:** 640px

| Section | Content |
|---|---|
| Invoice Details | All fields from log form |
| Linked PO | PO number + delivery status |
| Payment History | Table: Date · Amount · Mode · UTR · Recorded By |
| Duplicate Alert | If flagged: "Similar invoice: [Number] dated [Date] for ₹[X]" |
| Audit Trail | Create → Update → Payment entries |

**Actions:**
- [Mark Payment Made] — requires: Date · Amount · Mode · UTR
- [Dispute Invoice] — requires: Reason
- [Download Invoice PDF]

### 5.3 Drawer: `mark-paid` — Record Payment

| Field | Type | Required |
|---|---|---|
| Payment Date | Date | ✅ |
| Amount Paid | Number | ✅ |
| Payment Mode | Select: NEFT · RTGS · Cheque · Cash | ✅ |
| UTR / Cheque Number | Text | ✅ (except cash) |
| Bank Account | Select | ✅ |
| Remarks | Textarea | ❌ |

---

## 6. Charts

### 6.1 Payable Ageing (Donut)
- **Segments:** 0–30 · 31–60 · 61–90 · >90 days
- **Centre:** "₹[Total] outstanding"

### 6.2 Top 10 Vendors by Outstanding Amount (Bar)
- **Sort:** Desc
- **Export:** PNG

### 6.3 Monthly Invoice Volume (Bar)
- **X-axis:** Last 6 months
- **Y-axis:** Invoice count

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Invoice logged | "Invoice [Number] from [Vendor] logged. Amount: ₹[X]." | Success | 4s |
| Payment recorded | "Payment of ₹[X] to [Vendor] recorded. UTR: [Y]." | Success | 4s |
| Dispute raised | "Invoice [Number] disputed. [Vendor] to be notified." | Warning | 4s |
| Duplicate detected | "Warning: Possible duplicate invoice detected from [Vendor]." | Warning | 5s |
| Export | "Vendor payable report exported." | Info | 3s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No invoices | "No vendor invoices" | "No invoices logged for this period." | [+ Log Invoice] |
| All paid | "All invoices cleared" | "No outstanding vendor invoices." | — |

---

## 9. Loader States

| Trigger | Loader |
|---|---|
| Page load | Skeleton KPIs + table skeleton |
| Filter/search | Inline table skeleton |
| Detail drawer | Spinner + skeleton |
| Mark paid | Spinner on button |

---

## 10. Role-Based UI Visibility

| Element | Accounts Mgr G1 | Proc Finance G1 | Finance Mgr G1 |
|---|---|---|---|
| [+ Log Invoice] | ✅ | ✅ | ❌ |
| [Mark Paid] | ✅ | ✅ | ❌ |
| [Dispute] | ✅ | ✅ | ❌ |
| View all invoices | ✅ | ✅ | ✅ |
| Export | ✅ | ✅ | ✅ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/finance/vendor-payable/` | JWT (G1+) | Invoice list |
| POST | `/api/v1/group/{id}/finance/vendor-payable/` | JWT (G1) | Log invoice |
| GET | `/api/v1/group/{id}/finance/vendor-payable/{iid}/` | JWT (G1+) | Invoice detail |
| POST | `/api/v1/group/{id}/finance/vendor-payable/{iid}/payment/` | JWT (G1) | Record payment |
| POST | `/api/v1/group/{id}/finance/vendor-payable/{iid}/dispute/` | JWT (G1) | Dispute invoice |
| GET | `/api/v1/group/{id}/finance/vendor-payable/duplicates/` | JWT (G1+) | Flagged duplicates |
| GET | `/api/v1/group/{id}/finance/vendor-payable/export/` | JWT (G1+) | Export |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Search | `input delay:300ms` | GET `.../vendor-payable/?q=` | `#invoice-table-body` | `innerHTML` |
| Filter | `change` | GET `.../vendor-payable/?vendor=&status=` | `#invoice-section` | `innerHTML` |
| Log drawer | `click` | GET `.../vendor-payable/log-form/` | `#drawer-body` | `innerHTML` |
| Detail drawer | `click` | GET `.../vendor-payable/{id}/` | `#drawer-body` | `innerHTML` |
| Mark paid | `click` | GET `.../vendor-payable/{id}/payment-form/` | `#drawer-body` | `innerHTML` |
| Submit payment | `submit` | POST `.../vendor-payable/{id}/payment/` | `#drawer-body` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
