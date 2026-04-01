# 46 — SAC 9993 Invoice Register

- **URL:** `/group/finance/tax/sac-9993/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Role:** GST/Tax Officer G1 (primary) · Finance Manager G1

---

## 1. Purpose

The SAC 9993 Invoice Register is the master register of all taxable coaching invoices issued across the group. SAC 9993 covers "Education services — other than pre-school, school, higher secondary education by recognised institutions" — i.e., coaching and tutorial services attract 18% GST (9% CGST + 9% SGST for intra-state).

School education fees (classes 1–12 by a recognised board-affiliated institution) are **exempt** under GST. The Tax Officer must ensure: every coaching fee invoice is raised with a GST-compliant invoice number, correct SAC code, GSTIN details, and 18% tax calculation. This register feeds into GSTR-1 filing.

Invoice numbering: sequential per GSTIN per FY (e.g., BRN-GST-2526-001). E-invoice mandate applies if aggregate turnover > ₹5 crore.

---

## 2. Role Access

| Role | Level | Access |
|---|---|---|
| Group GST/Tax Officer | G1 | Full read + add invoices + mark void |
| Group Finance Manager | G1 | Read |
| Group CFO | G1 | Read — summary |
| Group Internal Auditor | G1 | Read — audit |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Finance → GST & Tax → SAC 9993 Invoice Register
```

### 3.2 Page Header
- **Title:** `SAC 9993 Invoice Register`
- **Subtitle:** `FY [Year] · [N] Invoices · Taxable Value: ₹[X] · GST: ₹[Y]`
- **Right-side controls:** `[FY ▾]` `[Month ▾]` `[Branch ▾]` `[GSTIN ▾]` `[+ Add Invoice]` `[Export ↓]`

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule |
|---|---|---|
| Total Invoices (Month) | Count | Neutral |
| Taxable Value | ₹ | Neutral |
| CGST | ₹ | Neutral |
| SGST | ₹ | Neutral |
| IGST | ₹ | Neutral (interstate only) |
| Void / Cancelled | Count | Red if > 0 |

---

## 5. Main Table

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Invoice No | Text | ✅ | — |
| Invoice Date | Date | ✅ | — |
| Branch | Text | ✅ | ✅ |
| GSTIN (Supplier) | Text | ✅ | ✅ |
| Student / Recipient | Text | ✅ | — |
| Recipient GSTIN | Text | ✅ | — |
| Supply Type | Badge: B2B · B2C · Export | ✅ | ✅ |
| SAC Code | Text (9993) | — | — |
| Service Description | Text | — | — |
| Taxable Value | ₹ | ✅ | — |
| GST Rate | % (18%) | — | — |
| CGST | ₹ | ✅ | — |
| SGST | ₹ | ✅ | — |
| IGST | ₹ | ✅ | — |
| Total Invoice Value | ₹ | ✅ | — |
| Status | Badge: Active · Void · Amended | ✅ | ✅ |
| E-Invoice IRN | Text | ✅ | — |
| Actions | View · Void · Download PDF | — | — |

### 5.1 Filters

| Filter | Type |
|---|---|
| Branch | Multi-select |
| GSTIN | Select |
| Supply Type | Select |
| Status | Multi-select |
| Month | Month picker |
| Amount Range | Number range |

### 5.2 Search
- Invoice number · Student name · Recipient GSTIN

### 5.3 Pagination
- 25 rows/page · Sort: Invoice Date desc

---

## 6. Drawers

### 6.1 Drawer: `invoice-add` — Add Invoice
- **Trigger:** [+ Add Invoice]
- **Width:** 760px

**Step 1: Invoice Header**

| Field | Type | Required | Validation |
|---|---|---|---|
| Branch | Select | ✅ | |
| GSTIN (Supplier) | Select (from branch's GSTIN) | ✅ | |
| Invoice Date | Date | ✅ | Cannot be future date |
| Invoice Number | Auto-generated (editable) | ✅ | Sequential per GSTIN |
| Supply Type | Select: B2B · B2C · Export | ✅ | |
| Recipient Name | Text | ✅ | |
| Recipient GSTIN | Text | Required if B2B | 15-char GST format |
| Place of Supply | Select (state) | ✅ | |

**Step 2: Invoice Lines**

| # | Description | SAC | Qty | Rate | Taxable Value | GST % | CGST | SGST | IGST | Total |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Coaching Fee — [Stream] | 9993 | 1 | ₹ | ₹ | 18% | ₹ | ₹ | ₹ | ₹ |
| [+ Add Line] | | | | | | | | | | |

- Tax type auto-determined: CGST+SGST if intra-state, IGST if inter-state
- Total auto-calculated

**Step 3: Notes**
- Narration · Payment Terms · Due Date

**Actions:** [Cancel] [Save Draft] [Save & Generate PDF]

### 6.2 Drawer: `invoice-detail` — View Invoice
- **Width:** 800px

**Invoice Preview:**
- Logo · Branch Name · GSTIN · Address
- Invoice number, date, supply type
- Recipient details
- Line items table
- Tax calculation breakup
- Grand total
- **[Download PDF]** **[Send to Student Email]**

**E-Invoice Panel (if applicable):**
- IRN Number · Signed QR Code (display)
- **[Generate E-Invoice / Cancel E-Invoice]**

### 6.3 Drawer: `invoice-void` — Void Invoice
| Field | Type | Required |
|---|---|---|
| Void Reason | Select: Data Entry Error · Service Not Rendered · Duplicate · Other | ✅ |
| Notes | Textarea | ✅ |
| Credit Note Required | Toggle | — |

- Once voided: status = Void, reflected in GSTR-1 as credit note

---

## 7. Charts

### 7.1 Monthly Invoice Value Trend (Bar — Last 12 Months)
- **Series:** Taxable Value (blue) · GST Collected (orange)

### 7.2 Invoice Volume by Branch (Bar)
- **Sort:** Desc

### 7.3 Supply Type Split (Donut)
- **Segments:** B2B · B2C · Export

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Invoice created | "Invoice [No] created for [Branch]." | Success | 4s |
| Invoice voided | "Invoice [No] voided. Credit note reference recorded." | Warning | 4s |
| PDF generated | "Invoice PDF ready for download." | Info | 3s |
| E-invoice generated | "IRN generated: [IRN]. QR code embedded." | Success | 4s |
| Export | "SAC 9993 register exported." | Info | 3s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No invoices | "No invoices this month" | "No SAC 9993 invoices raised for this period." | [+ Add Invoice] |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Page load | Skeleton KPIs + table |
| Month switch | Table skeleton |
| Invoice drawer | Spinner + form skeleton |

---

## 11. Role-Based UI Visibility

| Element | Tax Officer G1 | Finance Mgr G1 | Internal Auditor G1 |
|---|---|---|---|
| [+ Add Invoice] | ✅ | ❌ | ❌ |
| [Void Invoice] | ✅ | ❌ | ❌ |
| [Generate E-Invoice] | ✅ | ❌ | ❌ |
| [Download PDF] | ✅ | ✅ | ✅ |
| Export | ✅ | ✅ | ✅ |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/finance/tax/sac-9993/` | JWT (G1+) | Invoice list |
| POST | `/api/v1/group/{id}/finance/tax/sac-9993/` | JWT (G1) | Create invoice |
| GET | `/api/v1/group/{id}/finance/tax/sac-9993/{inv}/` | JWT (G1+) | Invoice detail |
| POST | `/api/v1/group/{id}/finance/tax/sac-9993/{inv}/void/` | JWT (G1) | Void invoice |
| POST | `/api/v1/group/{id}/finance/tax/sac-9993/{inv}/e-invoice/` | JWT (G1) | Generate IRN |
| GET | `/api/v1/group/{id}/finance/tax/sac-9993/{inv}/pdf/` | JWT (G1+) | Download PDF |
| GET | `/api/v1/group/{id}/finance/tax/sac-9993/export/` | JWT (G1+) | Export register |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Month filter | `change` | GET `.../sac-9993/?month=&branch=` | `#invoice-section` | `innerHTML` |
| Create drawer | `click` | GET `.../sac-9993/create-form/` | `#drawer-body` | `innerHTML` |
| Detail drawer | `click` | GET `.../sac-9993/{id}/` | `#drawer-body` | `innerHTML` |
| Submit invoice | `submit` | POST `.../sac-9993/` | `#invoice-table-body` | `afterbegin` |
| Void invoice | `click` | GET `.../sac-9993/{id}/void-form/` | `#drawer-body` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
