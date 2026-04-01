# 45 — TDS Compliance Tracker

- **URL:** `/group/finance/tax/tds/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Role:** GST/Tax Officer G1 (primary) · CFO G1 · Finance Manager G1

---

## 1. Purpose

The TDS Compliance Tracker manages Tax Deducted at Source obligations across the group. This covers:

- **Section 194C** — TDS on payments to contractors/sub-contractors (1% individual/HUF, 2% others)
- **Section 194J** — TDS on professional fees, technical services (10%)
- **Section 192** — TDS on salaries (as per slab; Form 24Q)
- **Section 194I** — TDS on rent (10% if > ₹2.4 lakh/year)

TDS must be deposited by the 7th of the following month (except March — 30 April). Quarterly returns: Form 26Q (non-salary) — 31 July, 31 Oct, 31 Jan, 31 May. Form 24Q (salary) — same schedule. Late filing: ₹200/day penalty.

---

## 2. Role Access

| Role | Level | Access |
|---|---|---|
| Group GST/Tax Officer | G1 | Full read + mark deposited + file return |
| Group CFO | G1 | Read — liability summary |
| Group Finance Manager | G1 | Read + approve challan |
| Group Internal Auditor | G1 | Read — audit |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Finance → GST & Tax → TDS Compliance Tracker
```

### 3.2 Page Header
- **Title:** `TDS Compliance Tracker`
- **Subtitle:** `FY [Year] · Quarter [Q] · Total TDS Liability: ₹[X]`
- **Right-side controls:** `[FY ▾]` `[Quarter ▾]` `[Section ▾]` `[Branch ▾]` `[Export ↓]`

### 3.3 Alert Banner

| Condition | Banner | Severity |
|---|---|---|
| TDS deposit due in ≤ 3 days | "TDS deposit due by [Date]. Pending: ₹[X] across [N] sections." | Amber |
| Return filing overdue | "Form [26Q/24Q] for Q[N] is overdue. Penalty accruing." | Red |
| TDS not deducted (detected) | "[N] payments found without TDS deduction." | Red |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule |
|---|---|---|
| Total TDS Deducted (QTR) | ₹ | Neutral |
| TDS Deposited | ₹ | Green if = deducted |
| Pending Deposit | ₹ | Red if > 0 |
| Returns Filed | N/N (quarter) | Green if all filed |
| 26AS Mismatches | Count | Red if > 0 |

---

## 5. Main Table — TDS Deduction Register

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Deduction ID | Text | ✅ | — |
| Branch | Text | ✅ | ✅ |
| Deductee Name | Text | ✅ | ✅ |
| Deductee PAN | Text | ✅ | — |
| Section | Badge: 192 · 194C · 194J · 194I | ✅ | ✅ |
| Payment Nature | Text | — | — |
| Payment Date | Date | ✅ | — |
| Gross Amount | ₹ | ✅ | — |
| TDS Rate | % | ✅ | — |
| TDS Deducted | ₹ | ✅ | — |
| Deposit Status | Badge: Deposited · Pending · Overdue | ✅ | ✅ |
| Challan No | Text | ✅ | — |
| Deposit Date | Date | ✅ | — |
| Actions | View · Mark Deposited | — | — |

### 5.1 Filters

| Filter | Type |
|---|---|
| Branch | Multi-select |
| Section | Multi-select |
| Deposit Status | Multi-select |
| Month | Month picker |
| PAN | Text search |

### 5.2 Search
- Deductee name · PAN · Challan number

### 5.3 Pagination
- 25 rows/page · Sort: Payment Date desc

---

## 6. Drawers

### 6.1 Drawer: `tds-deposit` — Mark TDS as Deposited
- **Trigger:** Mark Deposited action
- **Width:** 640px

| Field | Type | Required |
|---|---|---|
| BSR Code | Text (7 digits) | ✅ |
| Challan Serial No | Text | ✅ |
| Deposit Date | Date | ✅ |
| Bank Name | Select | ✅ |
| Amount Deposited | Number | ✅ |
| Section | Read-only | — |
| Challan File | File upload (PDF) | ❌ |

- [Cancel] [Save Deposit]

### 6.2 Drawer: `tds-deduction-detail` — Deduction Detail
- **Width:** 680px

**Transaction Details:**
- Deductee · PAN · Section · Nature of Payment
- Gross Amount · TDS Rate · TDS Amount
- Certificate No (if issued)

**Deposit Details:**
- Challan Reference · BSR Code · Date
- Challan PDF download link

**26AS Status:**
- Matched / Mismatch / Pending

### 6.3 Drawer: `return-filing` — TDS Return Filing Status
- **Width:** 720px

**Quarterly Returns:**

| Quarter | Form | Due Date | Status | Acknowledgement No | Filed Date |
|---|---|---|---|---|---|
| Q1 (Apr–Jun) | 26Q | 31-Jul | Filed | [ACK] | [Date] |
| Q2 (Jul–Sep) | 26Q | 31-Oct | Pending | — | — |
| Q3 (Oct–Dec) | 26Q | 31-Jan | — | — | — |
| Q4 (Jan–Mar) | 26Q | 31-May | — | — | — |

**Actions:** [Mark Return Filed] [Download FVU File]

### 6.4 Drawer: `26as-reconciliation` — Form 26AS Reconciliation
- **Width:** 800px

| Entry in Books | Entry in 26AS | Difference | Status |
|---|---|---|---|
| Deductee · PAN · TDS Amount | TDS reflected in 26AS | ₹ diff | Matched · Mismatch |

**Mismatch Reasons (if any):**
- Short deduction · Wrong PAN · Deposit timing difference

---

## 7. Tabs

| Tab | Content |
|---|---|
| Deduction Register | Main table (Section 5) |
| Deposit Challans | All challans with BSR code, bank, amount |
| Return Status | Quarterly returns per form |
| 26AS Reconciliation | Mismatch log |

---

## 8. Charts

### 8.1 Monthly TDS Liability vs Deposited (Bar)
- **Series:** Liability (orange) · Deposited (green) · Pending (red)

### 8.2 TDS by Section — Proportion (Donut)
- **Segments:** 192 · 194C · 194J · 194I

---

## 9. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Challan saved | "TDS challan recorded. BSR: [Code], Serial: [No]." | Success | 4s |
| Return filed | "Form [26Q/24Q] Q[N] marked as filed. ACK: [Number]." | Success | 4s |
| Overdue alert | "TDS deposit for [Month] is overdue. Penalty: ₹200/day." | Warning | 6s |
| Export | "TDS register exported." | Info | 3s |

---

## 10. Empty States

| Condition | Heading | Description |
|---|---|---|
| No deductions | "No TDS deductions" | "No TDS deductions recorded for this quarter." |
| All deposited | "All TDS deposited" | "All TDS for this quarter has been deposited on time." |

---

## 11. Loader States

| Trigger | Loader |
|---|---|
| Page load | Skeleton KPIs + table |
| Quarter switch | Table skeleton |
| Drawer | Spinner + form skeleton |

---

## 12. Role-Based UI Visibility

| Element | Tax Officer G1 | CFO G1 | Finance Mgr G1 |
|---|---|---|---|
| [Mark Deposited] | ✅ | ❌ | ✅ |
| [Mark Return Filed] | ✅ | ❌ | ❌ |
| 26AS Reconciliation tab | ✅ | ✅ | ✅ |
| View all branches | ✅ | ✅ | ✅ |
| Export | ✅ | ✅ | ✅ |

---

## 13. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/finance/tax/tds/` | JWT (G1+) | Deduction register |
| POST | `/api/v1/group/{id}/finance/tax/tds/{did}/deposit/` | JWT (G1) | Record challan |
| GET | `/api/v1/group/{id}/finance/tax/tds/returns/` | JWT (G1+) | Return status |
| POST | `/api/v1/group/{id}/finance/tax/tds/returns/{rid}/file/` | JWT (G1) | Mark return filed |
| GET | `/api/v1/group/{id}/finance/tax/tds/26as-recon/` | JWT (G1+) | 26AS mismatch list |
| GET | `/api/v1/group/{id}/finance/tax/tds/export/` | JWT (G1+) | Export |

---

## 14. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Quarter filter | `change` | GET `.../tds/?quarter=&section=` | `#tds-section` | `innerHTML` |
| Detail drawer | `click` | GET `.../tds/{id}/` | `#drawer-body` | `innerHTML` |
| Deposit form | `click` | GET `.../tds/{id}/deposit-form/` | `#drawer-body` | `innerHTML` |
| Submit deposit | `submit` | POST `.../tds/{id}/deposit/` | `#tds-row-{id}` | `outerHTML` |
| Tab switch | `click` | GET `.../tds/?tab=challans` | `#tds-tab-content` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
