# 44 — GST Returns Dashboard

- **URL:** `/group/finance/tax/gst-returns/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Role:** GST/Tax Officer G1 (primary) · CFO G1 · Finance Manager G1

---

## 1. Purpose

The GST Returns Dashboard manages GSTR-1 (outward supply register), GSTR-3B (monthly summary return), and GSTR-9 (annual return) for all registered GSTINs in the group. Each branch operating as a coaching centre (taxable supply — SAC 9993) has its own GSTIN; the group GSTIN covers group-level taxable services.

School fees are exempt; coaching fees attract 18% GST. The Tax Officer must ensure: every invoice is classified correctly, GSTR-1 is filed by the 11th, GSTR-3B by the 20th, and tax liability is paid by 20th of the following month. Late filing penalty: ₹50/day (₹20 for nil returns).

---

## 2. Role Access

| Role | Level | Access |
|---|---|---|
| Group GST/Tax Officer | G1 | Full read + mark filed + add invoices |
| Group CFO | G1 | Read — liability + compliance |
| Group Finance Manager | G1 | Read |
| Group Internal Auditor | G1 | Read — audit |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Finance → GST & Tax → GST Returns Dashboard
```

### 3.2 Page Header
- **Title:** `GST Returns Dashboard`
- **Subtitle:** `FY [Year] · [N] GSTINs · Filing Month: [Month]`
- **Right-side controls:** `[FY ▾]` `[Month ▾]` `[GSTIN ▾]` `[Export ↓]`

---

## 4. Filing Status Table — Current Month

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Entity / Branch | Text | ✅ | ✅ |
| GSTIN | Text | ✅ | — |
| GSTR-1 Due | Date | ✅ | — |
| GSTR-1 Status | Badge: Filed · Pending · Overdue | ✅ | ✅ |
| GSTR-1 Filed Date | Date | ✅ | — |
| GSTR-3B Due | Date | ✅ | — |
| GSTR-3B Status | Badge: Filed · Pending · Overdue | ✅ | ✅ |
| GSTR-3B Filed Date | Date | ✅ | — |
| Tax Liability | ₹ | ✅ | — |
| ITC Available | ₹ | ✅ | — |
| Net Tax Payable | ₹ | ✅ | — |
| Paid | Badge: Yes · No | ✅ | ✅ |
| Actions | View Detail · Mark Filed | — | — |

### 4.1 Filters
- GSTIN · Filing Status · Month

### 4.2 Pagination
- 20 rows/page

---

## 5. Drawers

### 5.1 Drawer: `gstr1-detail` — GSTR-1 Invoice Register
- **Trigger:** View Detail (GSTR-1)
- **Width:** 900px

**Tabs:** B2B Invoices · B2C Invoices · Exempt Supplies · Nil Supplies · HSN/SAC Summary

**B2B Tab:**
| Invoice No | Date | Recipient GSTIN | Taxable Value | IGST | CGST | SGST | Total |
|---|---|---|---|---|---|---|---|
| [INV001] | [Date] | [GSTIN] | ₹ | ₹ | ₹ | ₹ | ₹ |

**SAC 9993 Breakdown:**
- SAC 9993 (Coaching services — 18% GST)
- SAC 9992 (School education — Exempt)

**Actions:** [Export GSTR-1 JSON] [Mark as Filed]

### 5.2 Drawer: `gstr3b-detail` — GSTR-3B Summary
- **Width:** 720px

| Section | Value |
|---|---|
| 3.1 Outward Taxable Supplies | ₹[X] (taxable) + ₹[Y] (exempt) |
| 3.2 Inward Supplies (Reverse Charge) | ₹ |
| 4 Eligible ITC | ₹[ITC available] |
| 5 Values of Exempt/Nil/Non-GST | ₹ |
| 6 Payment of Tax | CGST: ₹ · SGST: ₹ · IGST: ₹ |
| Net Payable | ₹ |

**Actions:** [Mark GSTR-3B Filed] [Download Summary PDF]

### 5.3 Drawer: `mark-filed` — Mark Return as Filed
| Field | Type | Required |
|---|---|---|
| Return Type | Read-only | — |
| Filed Date | Date | ✅ |
| ARN Number | Text | ✅ |
| Challan Reference | Text | ✅ (if tax paid) |
| Tax Paid Amount | Number | ✅ |
| Payment Mode | Select: Cash Ledger · ITC | ✅ |

---

## 6. Charts

### 6.1 Monthly GST Liability vs ITC Utilised (Bar)
- **Series:** Liability (orange) · ITC Used (blue) · Cash Paid (green)

### 6.2 Filing Compliance Rate by Month (Line)
- **Y-axis:** % of GSTINs filed on time

---

## 7. Annual Return Section (GSTR-9)

Shown in November – December panel:

| GSTIN | Turnover | GSTR-9 Status | Due Date |
|---|---|---|---|
| [GSTIN] | ₹ | Not Started · In Progress · Filed | 31 Dec |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Return marked filed | "GSTR-[N] filed for [Entity]. ARN: [Number]." | Success | 4s |
| Overdue warning | "GSTR-3B for [Entity] is overdue. Late fee: ₹[X] so far." | Warning | 6s |
| Export | "GST returns report exported." | Info | 3s |

---

## 9. Empty States

| Condition | Heading | Description |
|---|---|---|
| All returns filed | "All returns filed" | "All GSTINs have filed returns for this month." |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Page load | Skeleton table |
| Month switch | Table skeleton |
| Drawer | Spinner + tab skeleton |

---

## 11. Role-Based UI Visibility

| Element | Tax Officer G1 | CFO G1 | Finance Mgr G1 |
|---|---|---|---|
| [Mark Filed] | ✅ | ❌ | ❌ |
| [Export GSTR JSON] | ✅ | ❌ | ❌ |
| View all GSTINs | ✅ | ✅ | ✅ |
| Export report | ✅ | ✅ | ✅ |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/finance/tax/gst-returns/` | JWT (G1+) | Filing status |
| GET | `/api/v1/group/{id}/finance/tax/gst-returns/{gstin}/{month}/gstr1/` | JWT (G1+) | GSTR-1 detail |
| GET | `/api/v1/group/{id}/finance/tax/gst-returns/{gstin}/{month}/gstr3b/` | JWT (G1+) | GSTR-3B detail |
| PUT | `/api/v1/group/{id}/finance/tax/gst-returns/{rid}/mark-filed/` | JWT (G1) | Mark filed |
| GET | `/api/v1/group/{id}/finance/tax/gst-returns/export/` | JWT (G1+) | Export |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Month switch | `change` | GET `.../gst-returns/?month=` | `#gst-table` | `innerHTML` |
| Detail drawer | `click` | GET `.../gst-returns/{gstin}/{month}/gstr1/` | `#drawer-body` | `innerHTML` |
| Mark filed | `click` | GET `.../gst-returns/{id}/mark-filed-form/` | `#drawer-body` | `innerHTML` |
| Submit mark filed | `submit` | PUT `.../gst-returns/{id}/mark-filed/` | `#gst-row-{id}` | `outerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
