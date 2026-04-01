# 55 — Vendor Ledger

- **URL:** `/group/finance/procurement/vendor-ledger/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Role:** Procurement Finance G1 (primary) · Accounts Manager G1

---

## 1. Purpose

The Vendor Ledger provides a complete account statement for each vendor — all POs raised, invoices received, TDS deducted, payments made, credit notes, and outstanding balance. It is the reconciliation source for vendor balance confirmation letters (monthly or quarterly), and is used by the Accounts Manager to reconcile vendor balances in the group's books against vendor statements.

Vendor balance reconciliation is a mandatory internal control — differences are flagged as reconciliation items and tracked to resolution.

---

## 2. Role Access

| Role | Level | Access |
|---|---|---|
| Group Procurement Finance | G1 | Full read |
| Group Accounts Manager | G1 | Full read + reconcile |
| Group Finance Manager | G1 | Read |
| Group Internal Auditor | G1 | Read — audit |
| Group CFO | G1 | Read — top vendors |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Finance → Procurement → Vendor Ledger
```

### 3.2 Page Header
- **Title:** `Vendor Ledger`
- **Subtitle:** `[N] Active Vendors · Total Payable: ₹[X]`
- **Right-side controls:** `[Vendor ▾]` `[Branch ▾]` `[FY ▾]` `[Export ↓]`

---

## 4. Vendor List (Left Panel / Selector)

A search-and-select vendor list:
- Search by vendor name / GSTIN
- Shows: Vendor Name · Outstanding Balance · Last Transaction Date
- Select a vendor to view their ledger on the right

---

## 5. Vendor Ledger Statement (Main Panel)

**Selected Vendor Header:**
- Vendor Name · GSTIN · PAN · Category · Bank Account (masked) · Contact
- **Outstanding Balance:** ₹[X] (Dr / Cr)

**Statement Table:**

| Date | Particulars | PO No | Invoice No | Debit (₹) | Credit (₹) | Balance (₹) |
|---|---|---|---|---|---|---|
| [Date] | Opening Balance | — | — | — | — | ₹[X] |
| [Date] | Invoice received | [PO] | [INV] | ₹ | — | ₹ |
| [Date] | TDS deducted | — | — | — | ₹(TDS) | ₹ |
| [Date] | Payment (NEFT) | — | — | — | ₹ | ₹ |
| [Date] | Credit Note | — | [CN] | ₹ | — | ₹ |
| **Closing Balance** | | | | **₹** | **₹** | **₹[X]** |

**Filter controls:**
- Date Range · Transaction Type (All · Invoices · Payments · TDS · Credit Notes)

### 5.1 Pagination
- 50 rows/page (statement view)

---

## 6. Ageing Summary

| Bucket | Amount | Count |
|---|---|---|
| Current (0–30 days) | ₹ | [N] |
| 31–60 days | ₹ | [N] |
| 61–90 days | ₹ | [N] |
| 91–120 days | ₹ | [N] |
| > 120 days | ₹ | [N] |
| **Total Outstanding** | **₹** | |

---

## 7. Drawers

### 7.1 Drawer: `vendor-recon` — Vendor Balance Reconciliation
- **Trigger:** [Reconcile] button on vendor header
- **Width:** 760px

| Item | Balance in Books | Vendor Statement | Difference |
|---|---|---|---|
| Outstanding Invoices | ₹ | ₹ | ₹ |
| Payments Made | ₹ | ₹ | ₹ |
| TDS Deducted | ₹ | ₹ | ₹ |
| Credit Notes | ₹ | ₹ | ₹ |
| **Net Balance** | **₹** | **₹** | **₹** |

**Reconciling Items:**
| Description | Amount | Action |
|---|---|---|
| Invoice not yet received | ₹ | Awaiting vendor |
| Payment in transit | ₹ | Confirm UTR |

**[Upload Vendor Statement]** (PDF) **[Mark Reconciled]**

### 7.2 Drawer: `send-confirmation` — Send Balance Confirmation
| Field | Type | Required |
|---|---|---|
| As of Date | Date | ✅ |
| Vendor Email | Text (pre-filled) | ✅ |
| Message | Textarea (template) | ✅ |
| Attach Statement | Toggle (default ON) | — |

- [Send Balance Confirmation Letter]

---

## 8. Charts

### 8.1 Vendor Payment History — Last 12 Months (Bar)
- **Series:** Invoiced (orange) · Paid (green) · Outstanding (red)

### 8.2 TDS Deducted on Vendor (Bar — Monthly)

---

## 9. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Reconciled | "[Vendor] ledger marked as reconciled as of [Date]." | Success | 4s |
| Confirmation sent | "Balance confirmation letter sent to [Vendor]." | Info | 3s |
| Export | "Vendor ledger exported." | Info | 3s |

---

## 10. Empty States

| Condition | Heading | Description |
|---|---|---|
| No vendor selected | "Select a vendor" | "Search and select a vendor to view their ledger." |
| No transactions | "No transactions" | "No transactions found for the selected period." |

---

## 11. Loader States

| Trigger | Loader |
|---|---|
| Page load | Skeleton vendor list + statement |
| Vendor switch | Statement skeleton |
| Drawer | Spinner |

---

## 12. Role-Based UI Visibility

| Element | Procurement Finance G1 | Accounts Mgr G1 | Finance Mgr G1 |
|---|---|---|---|
| [Reconcile] | ❌ | ✅ | ✅ |
| [Send Confirmation] | ❌ | ✅ | ✅ |
| View all vendors | ✅ | ✅ | ✅ |
| Export | ✅ | ✅ | ✅ |

---

## 13. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/finance/procurement/vendor-ledger/` | JWT (G1+) | Vendor list |
| GET | `/api/v1/group/{id}/finance/procurement/vendor-ledger/{vid}/` | JWT (G1+) | Vendor statement |
| POST | `/api/v1/group/{id}/finance/procurement/vendor-ledger/{vid}/reconcile/` | JWT (G1) | Mark reconciled |
| POST | `/api/v1/group/{id}/finance/procurement/vendor-ledger/{vid}/confirm/` | JWT (G1) | Send confirmation |
| GET | `/api/v1/group/{id}/finance/procurement/vendor-ledger/{vid}/export/` | JWT (G1+) | Export statement |

---

## 14. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Vendor select | `click` | GET `.../vendor-ledger/{id}/` | `#ledger-panel` | `innerHTML` |
| Date range filter | `change` | GET `.../vendor-ledger/{id}/?from=&to=` | `#statement-table` | `innerHTML` |
| Reconcile drawer | `click` | GET `.../vendor-ledger/{id}/recon-form/` | `#drawer-body` | `innerHTML` |
| Submit recon | `submit` | POST `.../vendor-ledger/{id}/reconcile/` | `#vendor-status` | `outerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
