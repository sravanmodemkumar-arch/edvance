# 32 — Fee Receipt Register

- **URL:** `/group/finance/collection/receipts/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Role:** Fee Collection Head G3 · Accounts Manager G1 · Finance Manager G1

---

## 1. Purpose

The Fee Receipt Register provides a cross-branch transaction-level log of all fee receipts — every payment made by students, the payment mode, receipt number, and bank reference. This is the source-of-truth for fee collection reporting and is used by the Accounts Manager for bank reconciliation (matching receipts to bank credits) and by the Internal Auditor for transaction verification.

Key tracking: cheque bounces (a receipt is recorded but the cheque fails — the amount must be reversed), cash vs online payment ratios (cash collections require additional controls), and duplicate receipts (same student, same amount, same day — potential error).

---

## 2. Role Access

| Role | Level | Access |
|---|---|---|
| Group Fee Collection Head | G3 | Full read + export |
| Group Accounts Manager | G1 | Full read + export + flag bounce |
| Group Finance Manager | G1 | Read + export |
| Group Internal Auditor | G1 | Read — audit access |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Finance → Fee Collection → Fee Receipt Register
```

### 3.2 Page Header
- **Title:** `Fee Receipt Register`
- **Subtitle:** `[N] Receipts · ₹[Total] · [Date Range]`
- **Right-side controls:** `[Date Range ▾]` `[Branch ▾]` `[Payment Mode ▾]` `[Export ↓]`

---

## 4. Summary Cards

| Card | Value |
|---|---|
| Total Receipts (period) | Count |
| Total Amount (period) | ₹ |
| Online Payments | ₹ (%) |
| Cash Payments | ₹ (%) |
| Cheque Payments | ₹ (%) |
| Cheque Bounces | Count (red if > 0) |

---

## 5. Main Table

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Receipt Number | Text | ✅ | — |
| Date | Date | ✅ | ✅ (range) |
| Student Name | Text | ✅ | — |
| Student ID | Text | ✅ | — |
| Branch | Text | ✅ | ✅ |
| Fee Components | Text | — | — |
| Amount | ₹ | ✅ | — |
| Payment Mode | Badge: Online · Cash · Cheque · DD | ✅ | ✅ |
| UTR / Cheque No. | Text | ✅ | — |
| Bank | Text | ✅ | ✅ |
| Recorded By | Text | ✅ | — |
| Status | Badge: Cleared · Pending Clearance · Bounced · Reversed | ✅ | ✅ |
| Duplicate Flag | ⚠️ if detected | — | ✅ |
| Actions | View · Flag Bounce | — | — |

### 5.1 Filters

| Filter | Type |
|---|---|
| Date Range | Date picker |
| Branch | Multi-select |
| Payment Mode | Multi-select |
| Status | Multi-select |
| Amount Range | ₹ range |
| Duplicate Only | Toggle |

### 5.2 Search
- Student name · Receipt number · UTR

### 5.3 Pagination
- 25 rows/page · Sort: Date desc

---

## 6. Drawers

### 6.1 Drawer: `receipt-detail` — Receipt Detail
- **Trigger:** View action
- **Width:** 620px

| Field | Value |
|---|---|
| Receipt Number | [Number] |
| Date | [Date] |
| Student Name | [Name] |
| Student ID | [ID] |
| Branch | [Name] |
| Fee Components | Listed with amounts |
| Total Amount | ₹[X] |
| Payment Mode | [Mode] |
| UTR / Cheque / DD | [Reference] |
| Bank | [Name] |
| Clearance Date | [Date / Pending] |
| Recorded By | [Name] |
| Status | [Badge] |
| Duplicate Alert | If flagged: "Similar receipt exists: [Number] on [Date] for ₹[X]" |

**Actions:**
- [Flag as Cheque Bounce] — if mode is Cheque and bounced
- [Print Receipt]
- [Download Receipt PDF]

### 6.2 Drawer: `flag-bounce` — Record Cheque Bounce
| Field | Type | Required |
|---|---|---|
| Bounce Date | Date | ✅ |
| Bounce Reason | Select: Insufficient Funds · Sig Mismatch · Stale Cheque · Other | ✅ |
| Bank Charges | Number | ❌ |
| Action Taken | Select: Re-presented · Reversed · Legal Notice | ✅ |

---

## 7. Charts

### 7.1 Daily Collection by Payment Mode (Stacked Bar)
- **X-axis:** Days in selected range
- **Stacks:** Online · Cash · Cheque

### 7.2 Cheque Bounce Rate (Line)
- **X-axis:** Monthly
- **Y-axis:** % of cheque payments bounced

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Bounce flagged | "Cheque bounce recorded for [Student]. Receipt reversed." | Warning | 5s |
| Export | "Receipt register exported." | Info | 3s |

---

## 9. Empty States

| Condition | Heading | Description |
|---|---|---|
| No receipts | "No receipts" | "No fee receipts recorded for the selected period." |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Page load | Skeleton cards + table |
| Date change | Table skeleton |
| Receipt drawer | Spinner |

---

## 11. Role-Based UI Visibility

| Element | Collection Head G3 | Accounts Mgr G1 | Finance Mgr G1 | Auditor G1 |
|---|---|---|---|---|
| [Flag Bounce] | ❌ | ✅ | ❌ | ❌ |
| View all receipts | ✅ | ✅ | ✅ | ✅ |
| Export | ✅ | ✅ | ✅ | ✅ |
| Print receipt | ✅ | ✅ | ❌ | ❌ |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/finance/collection/receipts/` | JWT (G1+) | Receipt list |
| GET | `/api/v1/group/{id}/finance/collection/receipts/{rid}/` | JWT (G1+) | Receipt detail |
| POST | `/api/v1/group/{id}/finance/collection/receipts/{rid}/bounce/` | JWT (G1, Accounts Mgr) | Flag bounce |
| GET | `/api/v1/group/{id}/finance/collection/receipts/{rid}/pdf/` | JWT (G1+) | Receipt PDF |
| GET | `/api/v1/group/{id}/finance/collection/receipts/export/` | JWT (G1+) | Export |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Date range change | `change` | GET `.../receipts/?from=&to=` | `#receipt-section` | `innerHTML` |
| Search | `input delay:300ms` | GET `.../receipts/?q=` | `#receipt-table-body` | `innerHTML` |
| Filter | `change` | GET `.../receipts/?mode=&status=` | `#receipt-section` | `innerHTML` |
| Detail drawer | `click` | GET `.../receipts/{id}/` | `#drawer-body` | `innerHTML` |
| Flag bounce | `click` | GET `.../receipts/{id}/bounce-form/` | `#drawer-body` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
