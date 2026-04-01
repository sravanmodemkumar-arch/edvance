# 48 — Input Tax Credit (ITC) Tracker

- **URL:** `/group/finance/tax/itc/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Role:** GST/Tax Officer G1 (primary) · CFO G1

---

## 1. Purpose

The ITC Tracker manages Input Tax Credit eligibility and utilisation for all registered GSTINs in the group. Coaching centres registered under GST can claim ITC on business inputs (stationery, IT equipment, services) but **cannot** claim ITC attributable to exempt supplies (school education). Mixed-use inputs require apportionment under Rule 42/43.

The Tax Officer must: reconcile ITC claimed with GSTR-2B (auto-populated from supplier returns), identify blocked credits (Section 17(5) — personal expenses, motor vehicles, food), apportion mixed-use ITC, and ensure net ITC is correctly utilised in GSTR-3B before cash payment.

---

## 2. Role Access

| Role | Level | Access |
|---|---|---|
| Group GST/Tax Officer | G1 | Full read + claim + reconcile |
| Group CFO | G1 | Read — ITC utilisation summary |
| Group Finance Manager | G1 | Read |
| Group Internal Auditor | G1 | Read — audit |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Finance → GST & Tax → ITC Tracker
```

### 3.2 Page Header
- **Title:** `Input Tax Credit Tracker`
- **Subtitle:** `FY [Year] · Month: [Month] · Available ITC: ₹[X] · Utilised: ₹[Y]`
- **Right-side controls:** `[FY ▾]` `[Month ▾]` `[GSTIN ▾]` `[Export ↓]`

### 3.3 Alert Banner

| Condition | Banner | Severity |
|---|---|---|
| GSTR-2B mismatch detected | "[N] ITC claims not matching GSTR-2B. Reconcile before filing." | Amber |
| Blocked credit claimed | "Potential blocked credit detected: ₹[X]. Review before filing." | Red |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule |
|---|---|---|
| ITC Available (GSTR-2B) | ₹ | Neutral |
| ITC Claimed in Books | ₹ | Red if > GSTR-2B |
| Eligible ITC (post-apportionment) | ₹ | Neutral |
| Blocked Credits | ₹ | Red if > 0 |
| ITC Utilised (GSTR-3B) | ₹ | Neutral |
| Cash Paid | ₹ | Informational |

---

## 5. Tabs

| Tab | Content |
|---|---|
| ITC Ledger | Monthly ITC entries |
| GSTR-2B Reconciliation | Match books vs GSTR-2B |
| Blocked Credits | Section 17(5) entries |
| ITC Apportionment | Rule 42/43 calculation |

---

## 6. Tab: ITC Ledger

| Column | Type | Sortable |
|---|---|---|
| Entry Date | Date | ✅ |
| Vendor Name | Text | ✅ |
| Vendor GSTIN | Text | ✅ |
| Invoice No | Text | ✅ |
| Invoice Date | Date | ✅ |
| Taxable Value | ₹ | ✅ |
| IGST Credit | ✅ | — |
| CGST Credit | ₹ | — |
| SGST Credit | ₹ | — |
| Total ITC | ₹ | ✅ |
| Eligibility | Badge: Eligible · Blocked · Partially Eligible | ✅ |
| GSTR-2B Match | Badge: Matched · Mismatched · Pending | ✅ |
| Actions | View Detail | — |

### 6.1 Pagination
- 25 rows/page · Sort: Invoice Date desc

---

## 7. Tab: GSTR-2B Reconciliation

Compares ITC in books vs GSTR-2B auto-populated data:

| Vendor | Vendor GSTIN | Invoice No | ITC in Books | ITC in GSTR-2B | Difference | Status |
|---|---|---|---|---|---|---|
| [Vendor] | [GSTIN] | [INV] | ₹ | ₹ | ₹ | Matched · Mismatch · Only in Books · Only in 2B |

**Mismatch Actions:**
- Accept GSTR-2B value (if supplier error in books)
- Query supplier (if supplier hasn't filed)
- Defer to next month

**Summary Counts:**
- Matched: [N] · Mismatch: [N] · Only in Books: [N] · Only in 2B: [N]

---

## 8. Tab: Blocked Credits (Section 17(5))

| Category | Description | GST Paid | ITC Blocked |
|---|---|---|---|
| Motor vehicles (non-transport) | Vehicles for executive use | ₹ | ₹ |
| Food & beverages | Staff canteen (not mandated by law) | ₹ | ₹ |
| Personal expenses | Expenses for personal use | ₹ | ₹ |
| Works contract (immovable property) | Civil construction for own building | ₹ | ₹ |

**Total Blocked:** ₹[X]

---

## 9. Tab: ITC Apportionment (Rule 42/43)

For mixed-use suppliers (both taxable coaching + exempt school fees):

| Month | Total ITC | Taxable Turnover | Exempt Turnover | Total Turnover | Eligible % | Eligible ITC | Reversal Required |
|---|---|---|---|---|---|---|---|
| Apr 2025 | ₹X | ₹Y | ₹Z | ₹W | [%] | ₹A | ₹B |

**Formula:** Eligible ITC = Total ITC × (Taxable Turnover / Total Turnover)

**[Recalculate]** — refreshes on latest turnover data

---

## 10. Drawers

### 10.1 Drawer: `itc-entry-detail` — ITC Entry Detail
- **Width:** 680px

- Invoice details · Vendor GSTIN · SAC/HSN · Tax breakup
- Eligibility determination with reason
- GSTR-2B match status + matched entry detail
- [Mark as Blocked] [Mark as Eligible]

### 10.2 Drawer: `gstr2b-mismatch` — Resolve Mismatch
- **Width:** 720px

| Field | Type | Required |
|---|---|---|
| Resolution Action | Select: Accept GSTR-2B · Defer · Query Supplier | ✅ |
| Notes | Textarea | ✅ |
| Follow-up Date | Date | If Query Supplier |

---

## 11. Charts

### 11.1 Monthly ITC Available vs Utilised (Bar — Last 12 Months)
### 11.2 ITC Composition (Donut)
- **Segments:** IGST · CGST · SGST

---

## 12. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Mismatch resolved | "GSTR-2B mismatch for [Vendor] resolved." | Success | 4s |
| Blocked credit flagged | "Entry flagged as blocked credit — excluded from ITC claim." | Warning | 4s |
| Apportionment recalculated | "ITC apportionment recalculated for [Month]." | Info | 3s |
| Export | "ITC tracker exported." | Info | 3s |

---

## 13. Empty States

| Condition | Heading | Description |
|---|---|---|
| No ITC entries | "No ITC this month" | "No input tax credit entries for the selected period." |
| All reconciled | "GSTR-2B fully reconciled" | "All entries match GSTR-2B for this month." |

---

## 14. Loader States

| Trigger | Loader |
|---|---|
| Page load | Skeleton KPIs + tab |
| Tab switch | Skeleton table |
| GSTR-2B load | Progress spinner: "Fetching GSTR-2B data..." |

---

## 15. Role-Based UI Visibility

| Element | Tax Officer G1 | CFO G1 | Finance Mgr G1 |
|---|---|---|---|
| [Mark Blocked/Eligible] | ✅ | ❌ | ❌ |
| [Recalculate Apportionment] | ✅ | ❌ | ❌ |
| [Resolve Mismatch] | ✅ | ❌ | ❌ |
| View all tabs | ✅ | ✅ | ✅ |
| Export | ✅ | ✅ | ✅ |

---

## 16. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/finance/tax/itc/` | JWT (G1+) | ITC ledger |
| GET | `/api/v1/group/{id}/finance/tax/itc/gstr2b-recon/` | JWT (G1+) | GSTR-2B recon |
| PUT | `/api/v1/group/{id}/finance/tax/itc/{eid}/eligibility/` | JWT (G1) | Set eligibility |
| POST | `/api/v1/group/{id}/finance/tax/itc/gstr2b-recon/{mid}/resolve/` | JWT (G1) | Resolve mismatch |
| GET | `/api/v1/group/{id}/finance/tax/itc/apportionment/` | JWT (G1+) | Apportionment |
| POST | `/api/v1/group/{id}/finance/tax/itc/apportionment/recalculate/` | JWT (G1) | Recalculate |
| GET | `/api/v1/group/{id}/finance/tax/itc/export/` | JWT (G1+) | Export |

---

## 17. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Month filter | `change` | GET `.../itc/?month=` | `#itc-section` | `innerHTML` |
| Tab switch | `click` | GET `.../itc/?tab=gstr2b` | `#itc-tab-content` | `innerHTML` |
| Detail drawer | `click` | GET `.../itc/{id}/` | `#drawer-body` | `innerHTML` |
| Resolve mismatch | `submit` | POST `.../itc/gstr2b-recon/{id}/resolve/` | `#recon-row-{id}` | `outerHTML` |
| Recalculate | `click` | POST `.../itc/apportionment/recalculate/` | `#apportionment-table` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
