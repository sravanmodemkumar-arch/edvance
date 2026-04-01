# 10 — Group Procurement Finance Dashboard

- **URL:** `/group/finance/procurement/`
- **Template:** `portal_base.html`
- **Priority:** P0
- **Role:** Group Procurement Finance (Role 39, G1)

---

## 1. Purpose

The Procurement Finance Dashboard tracks all vendor payments related to group-wide bulk procurement: textbooks, notebooks, uniforms, lab equipment, stationery, and educational materials. The Group Procurement Finance Officer (G1) validates invoices, tracks purchase order fulfilment, monitors vendor payment schedules, and ensures procurement spend stays within sanctioned budgets.

This role works in coordination with the Group Procurement Manager (Division G, Role 65) who issues POs and manages delivery; the Finance Officer handles the payment side — invoice verification, payment release authorisation, and vendor ledger maintenance.

Key risk managed: duplicate invoice payments, inflated vendor bills, payments before goods are received, and budget overruns on procurement categories.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Procurement Finance | G1 | Full read + update payment status | Primary owner |
| Group CFO | G1 | Read — all sections | |
| Group Finance Manager | G1 | Read — all sections | |
| Group Accounts Manager | G1 | Read — vendor ledger | |
| Group Internal Auditor | G1 | Read — all sections | |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Finance → Procurement Finance Dashboard
```

### 3.2 Page Header
- **Title:** `Procurement Finance Dashboard`
- **Subtitle:** `Vendor Payments & PO Tracking · FY [Year]`
- **Role Badge:** `Group Procurement Finance`
- **Right-side controls:** `[FY ▾]` `[Category ▾]` `[Export ↓]`

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| Vendor invoice overdue > 30 days | "[N] vendor invoice(s) overdue for payment. Total: ₹[X]." | Red |
| PO budget consumed > 90% | "Procurement budget at [X]% consumption for FY. Review remaining POs." | Amber |
| Goods received but invoice not submitted > 15 days | "[N] PO(s) have delivery confirmed but no invoice received." | Amber |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Total POs Raised (FY) | Count | Informational | → Page 53 |
| PO Value (FY) | ₹ | Informational | → Page 53 |
| Invoices Pending Payment | Count | Red if > 0 overdue | → Page 54 |
| Amount Payable | ₹ | Red if overdue > ₹10L | → Page 54 |
| Budget Consumed % | YTD spend / Annual procurement budget | Green < 80% · Red > 95% | → Page 53 |
| Vendor Count Active | Count | Informational | → Page 55 |

---

## 5. Section 5.1 — PO vs Invoice Status Table

| Column | Type | Sortable |
|---|---|---|
| PO Number | Text | ✅ |
| Vendor | Text | ✅ |
| Category | Badge | ✅ |
| PO Amount | ₹ | ✅ |
| Delivery Status | Badge: Pending · Partial · Delivered | ✅ |
| Invoice Submitted | Badge: Yes · No | ✅ |
| Invoice Amount | ₹ | ✅ |
| Payment Status | Badge: Paid · Pending · Overdue · Disputed | ✅ |
| Actions | View · Approve Payment · Flag Dispute | — |

**Filters:** Category · Payment Status · Vendor · Date range
**Search:** PO number · Vendor name
**Pagination:** 20 rows/page

---

## 5.2 Section 5.2 — Procurement Budget vs Actual

| Category | Budget (FY) | Actual Spend | Balance | % Used |
|---|---|---|---|---|
| Textbooks & Notebooks | ₹ | ₹ | ₹ | % |
| Uniforms | ₹ | ₹ | ₹ | % |
| Lab Equipment | ₹ | ₹ | ₹ | % |
| Stationery | ₹ | ₹ | ₹ | % |
| IT Equipment | ₹ | ₹ | ₹ | % |
| Other | ₹ | ₹ | ₹ | % |

**[View Full Budget →]** links to Page 14.

---

## 5.3 Section 5.3 — Top Vendors by Payable Amount

| Vendor | Category | Invoices Pending | Amount Due |
|---|---|---|---|
| [Vendor A] | Books | 3 | ₹ |
| [Vendor B] | Uniforms | 2 | ₹ |

---

## 6. Charts

### 6.1 Procurement Spend by Category (Donut)
- **Segments:** Books · Uniforms · Lab · IT · Stationery · Other
- **Export:** PNG

### 6.2 Monthly PO Value vs Payments Made (Bar)
- **Series:** PO Value (blue) · Payments Made (green)
- **Export:** PNG

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Payment approved | "Payment of ₹[X] to [Vendor] approved. Ref: [PO]." | Success | 4s |
| Dispute flagged | "Dispute flagged for PO [Number]. Finance Manager notified." | Warning | 4s |
| Export | "Procurement finance report exported." | Info | 3s |

---

## 8. Empty States

| Condition | Heading | Description |
|---|---|---|
| No pending invoices | "No pending invoices" | "All vendor invoices are cleared for this period." |
| No POs raised | "No purchase orders" | "No POs raised for this financial year." |

---

## 9. Loader States

| Trigger | Loader |
|---|---|
| Page load | Skeleton KPIs + table skeleton + budget skeleton |
| FY switch | Full skeleton |
| Payment approval | Spinner on approve button |

---

## 10. Role-Based UI Visibility

| Element | Procurement Finance G1 | CFO G1 | Accounts Mgr G1 | Auditor G1 |
|---|---|---|---|---|
| [Approve Payment] | ✅ | ❌ | ❌ | ❌ |
| [Flag Dispute] | ✅ | ❌ | ❌ | ❌ |
| View PO table | ✅ | ✅ | ✅ | ✅ |
| Budget section | ✅ | ✅ | ✅ | ✅ |
| Export | ✅ | ✅ | ❌ | ✅ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/finance/procurement/kpis/` | JWT (G1+) | KPI cards |
| GET | `/api/v1/group/{id}/finance/procurement/po-status/` | JWT (G1+) | PO vs invoice table |
| PUT | `/api/v1/group/{id}/finance/procurement/invoices/{iid}/approve/` | JWT (G1) | Approve payment |
| PUT | `/api/v1/group/{id}/finance/procurement/invoices/{iid}/dispute/` | JWT (G1) | Flag dispute |
| GET | `/api/v1/group/{id}/finance/procurement/budget/` | JWT (G1+) | Budget vs actual |
| GET | `/api/v1/group/{id}/finance/procurement/export/` | JWT (G1+) | Export |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Filter | `change` | GET `.../po-status/?category=` | `#po-table` | `innerHTML` |
| Search | `input delay:300ms` | GET `.../po-status/?q=` | `#po-table-body` | `innerHTML` |
| Approve payment | `click` | PUT `.../invoices/{id}/approve/` | `#po-row-{id}` | `outerHTML` |
| Pagination | `click` | GET `.../po-status/?page=` | `#po-section` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
