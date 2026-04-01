# 53 — Purchase Order Register

- **URL:** `/group/finance/procurement/po-register/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Role:** Procurement Finance G1 (primary) · CFO G1 · Finance Manager G1

---

## 1. Purpose

The Purchase Order Register is the master log of all Purchase Orders (POs) raised across all branches. Every procurement above ₹10,000 must have a PO before payment is released. The PO register links to vendor invoices, tracks fulfilment status (partially fulfilled / fully fulfilled), and acts as the control point to prevent unauthorised payments.

The Procurement Finance officer monitors: POs raised vs invoices received, GRN (Goods Receipt Notes) confirmation, PO expiry, and budget against which each PO is allocated. Vendor payments without a linked PO are flagged by the irregularity detection system (Page 41).

---

## 2. Role Access

| Role | Level | Access |
|---|---|---|
| Group Procurement Finance | G1 | Full read + approve PO matching |
| Group Finance Manager | G1 | Read + final payment approval |
| Group CFO | G1 | Read — high-value POs |
| Group Internal Auditor | G1 | Read — audit |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Finance → Procurement → Purchase Order Register
```

### 3.2 Page Header
- **Title:** `Purchase Order Register`
- **Subtitle:** `FY [Year] · [N] Active POs · Total Value: ₹[X]`
- **Right-side controls:** `[FY ▾]` `[Quarter ▾]` `[Branch ▾]` `[Status ▾]` `[Export ↓]`

### 3.3 Alert Banner

| Condition | Banner | Severity |
|---|---|---|
| POs expiring in ≤ 7 days | "[N] PO(s) expiring soon. Review for extension or closure." | Amber |
| Invoice without PO | "[N] vendor invoice(s) received without linked PO." | Red |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule |
|---|---|---|
| Open POs | Count | Neutral |
| Fully Fulfilled | Count | Green |
| Partially Fulfilled | Count | Amber |
| PO Value (FY) | ₹ | Neutral |
| Invoiced Against POs | ₹ | Neutral |
| Uninvoiced PO Value | ₹ | Amber if > 20% |
| Invoices Without PO | Count | Red if > 0 |

---

## 5. Main Table

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| PO Number | Text | ✅ | — |
| Branch | Text | ✅ | ✅ |
| Vendor | Text | ✅ | ✅ |
| Category | Badge: IT · Furniture · Stationery · Housekeeping · Maintenance · Services · Other | ✅ | ✅ |
| PO Date | Date | ✅ | — |
| PO Value | ₹ | ✅ | — |
| Invoiced Amount | ₹ | ✅ | — |
| Balance | ₹ | ✅ | — |
| GRN Status | Badge: Pending · Partial · Confirmed | ✅ | ✅ |
| Payment Status | Badge: Unpaid · Partially Paid · Fully Paid | ✅ | ✅ |
| PO Status | Badge: Open · Fulfilled · Expired · Cancelled | ✅ | ✅ |
| Expiry Date | Date | ✅ | — |
| Actions | View · Match Invoice · Extend · Cancel | — | — |

### 5.1 Filters

| Filter | Type |
|---|---|
| Branch | Multi-select |
| Vendor | Multi-select |
| Category | Multi-select |
| Status | Multi-select |
| PO Value Range | Number range |
| Date Range | Date picker |

### 5.2 Search
- PO number · Vendor name

### 5.3 Pagination
- 25 rows/page · Sort: PO Date desc

---

## 6. Drawers

### 6.1 Drawer: `po-detail` — Purchase Order Detail
- **Width:** 800px

**Tabs:** PO Details · Invoices · GRN · Payments

**PO Details Tab:**
- PO Number · Branch · Vendor · Vendor GSTIN
- Category · Budget Head
- Authorised by · Raised Date · Expiry Date

**PO Line Items:**
| # | Description | Unit | Qty | Rate | Amount | Tax | Total |
|---|---|---|---|---|---|---|---|
| 1 | [Item] | Nos | [N] | ₹ | ₹ | ₹ | ₹ |

**Invoices Tab:**
| Invoice No | Date | Amount | Status |
|---|---|---|---|
| [INV001] | [Date] | ₹ | Matched |
| [+ Match Invoice] | | | |

**GRN Tab:**
| GRN No | Date | Items Received | Received By |
|---|---|---|---|
| [GRN001] | [Date] | [Description] | [Staff] |

**Payments Tab:**
| Payment Date | Amount | UTR | Mode |
|---|---|---|---|
| [Date] | ₹ | [UTR] | NEFT |

### 6.2 Drawer: `po-match-invoice` — Match Invoice to PO
| Field | Type | Required |
|---|---|---|
| Invoice Number | Text | ✅ |
| Invoice Date | Date | ✅ |
| Invoice Amount | Number | ✅ |
| Invoice File | PDF upload | ✅ |
| GRN Number | Text | ✅ |
| GRN Date | Date | ✅ |
| Items Received | Textarea | ✅ |

- 3-way matching: PO × Invoice × GRN
- Alert if invoice amount > PO balance

### 6.3 Drawer: `po-extend` — Extend PO
| Field | Type | Required |
|---|---|---|
| New Expiry Date | Date | ✅ |
| Reason | Textarea | ✅ |

---

## 7. Charts

### 7.1 PO Value by Category (Donut)
### 7.2 PO vs Invoice vs Payment (Bar — Monthly)
### 7.3 Open PO Ageing (Bar — 0–30 / 31–60 / 61–90 / 90+ days)

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Invoice matched | "Invoice [No] matched to PO [No]. 3-way match: ✅" | Success | 4s |
| PO extended | "PO [No] extended to [Date]." | Info | 3s |
| PO cancelled | "PO [No] cancelled." | Warning | 3s |
| No-PO alert | "Invoice [No] has no linked PO. Flag for review." | Warning | 5s |

---

## 9. Empty States

| Condition | Heading | Description |
|---|---|---|
| No POs | "No purchase orders" | "No POs raised for the selected period." |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Page load | Skeleton KPIs + table |
| Drawer | Spinner + tab skeleton |

---

## 11. Role-Based UI Visibility

| Element | Procurement Finance G1 | Finance Mgr G1 | CFO G1 | Auditor G1 |
|---|---|---|---|---|
| [Match Invoice] | ✅ | ✅ | ❌ | ❌ |
| [Extend PO] | ✅ | ✅ | ❌ | ❌ |
| [Cancel PO] | ✅ | ✅ | ❌ | ❌ |
| View all POs | ✅ | ✅ | ✅ | ✅ |
| Export | ✅ | ✅ | ✅ | ✅ |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/finance/procurement/po/` | JWT (G1+) | PO list |
| GET | `/api/v1/group/{id}/finance/procurement/po/{pid}/` | JWT (G1+) | PO detail |
| POST | `/api/v1/group/{id}/finance/procurement/po/{pid}/match-invoice/` | JWT (G1) | Match invoice |
| POST | `/api/v1/group/{id}/finance/procurement/po/{pid}/extend/` | JWT (G1) | Extend PO |
| POST | `/api/v1/group/{id}/finance/procurement/po/{pid}/cancel/` | JWT (G1) | Cancel PO |
| GET | `/api/v1/group/{id}/finance/procurement/po/export/` | JWT (G1+) | Export |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Filter | `change` | GET `.../po/?status=&branch=` | `#po-table` | `innerHTML` |
| Detail drawer | `click` | GET `.../po/{id}/` | `#drawer-body` | `innerHTML` |
| Match invoice | `click` | GET `.../po/{id}/match-invoice-form/` | `#drawer-body` | `innerHTML` |
| Submit match | `submit` | POST `.../po/{id}/match-invoice/` | `#po-row-{id}` | `outerHTML` |
| Tab switch | `click` | GET `.../po/{id}/?tab=invoices` | `#po-tab-content` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
