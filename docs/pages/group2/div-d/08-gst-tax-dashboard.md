# 08 — Group GST / Tax Officer Dashboard

- **URL:** `/group/finance/tax/`
- **Template:** `portal_base.html`
- **Priority:** P0
- **Role:** Group GST / Tax Officer (Role 37, G1)

---

## 1. Purpose

The GST / Tax Dashboard manages all indirect and direct tax compliance obligations for the institution group. Indian education taxation is complex: school tuition fees are exempt under GST, but integrated JEE/NEET coaching fees attract 18% GST (SAC 9993). Hostel accommodation for students is exempt up to ₹1,000/day; above that threshold, GST applies. This nuance must be tracked per branch, per student type, per fee component.

The Tax Officer (G1) tracks GSTR-1, GSTR-3B, and annual returns; manages TDS deducted on vendor payments (194C for contractors, 194J for professionals) and TDS on interest; and maintains the Input Tax Credit register. The filing calendar ensures no return deadline is missed — GST penalties accumulate daily.

This dashboard is the early-warning system: overdue filings, ITC mismatches, TDS shortfalls, and pending challan payments are all surfaced before they become liabilities.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group GST / Tax Officer | G1 | Full read + update filing status | Primary owner |
| Group CFO | G1 | Read — all sections | |
| Group Finance Manager | G1 | Read — filing calendar + TDS | |
| Group Internal Auditor | G1 | Read — all sections | Audit access |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Finance → GST & Tax Dashboard
```

### 3.2 Page Header
- **Title:** `GST & Tax Compliance Dashboard`
- **Subtitle:** `FY [Year] · GSTIN: [Group GSTIN] · [N] Branch GSTINs`
- **Role Badge:** `Group GST / Tax Officer`
- **Right-side controls:** `[FY ▾]` `[Export ↓]`

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| GSTR-3B due within 5 days | "GSTR-3B due on [Date]. [N] branches have pending invoices." | Red |
| TDS payment overdue | "TDS challan for [Month] not paid. Due date: [Date]. Late fee accruing." | Red |
| ITC mismatch detected | "ITC mismatch of ₹[X] in [Branch] for [Month]. Reconcile with GSTR-2B." | Amber |
| Annual return (GSTR-9) due within 30 days | "GSTR-9 annual return due on [Date]. Begin compilation now." | Amber |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| GST Returns Filed (YTD) | Count filed / Expected | Green = 100% | → Page 44 |
| Pending GST Returns | Count | Red if > 0 | → Page 44 |
| TDS Deducted (YTD) | ₹ | Informational | → Page 45 |
| TDS Deposited (YTD) | ₹ | Green if = Deducted | → Page 45 |
| ITC Available | ₹ | Informational | → Page 48 |
| Tax Filing Events This Month | Count | Informational | → Page 47 |

---

## 5. Section 5.1 — GST Return Status (Current Month)

| Column | Type | Sortable |
|---|---|---|
| Branch / Entity | Text | ✅ |
| GSTIN | Text | ✅ |
| GSTR-1 Status | Badge: Filed · Pending · Overdue | ✅ |
| GSTR-1 Due Date | Date | ✅ |
| GSTR-3B Status | Badge: Filed · Pending · Overdue | ✅ |
| GSTR-3B Due Date | Date | ✅ |
| Tax Payable | ₹ | ✅ |
| Tax Paid | ₹ | ✅ |
| Actions | View · Mark Filed | — |

**[View Full GST Returns →]** links to Page 44.

---

## 5.2 Section 5.2 — TDS Status (Current Quarter)

| Column | Type | Sortable |
|---|---|---|
| Section | Badge: 194C · 194J · 194I · 192 (Salary) | ✅ |
| Deductee Type | Text | ✅ |
| TDS Deducted | ₹ | ✅ |
| TDS Deposited | ₹ | ✅ |
| Shortfall | ₹ (red if > 0) | ✅ |
| Challan Date | Date | ✅ |
| Status | Badge: Deposited · Pending · Overdue | ✅ |

**[View Full TDS Tracker →]** links to Page 45.

---

## 5.3 Section 5.3 — Tax Filing Calendar (Next 30 Days)

| Date | Filing | Branch / Entity | Status |
|---|---|---|---|
| [Date] | GSTR-3B | [Entity] | Pending |
| [Date] | TDS Challan (Q2) | All | Due |

**[View Full Calendar →]** links to Page 47.

---

## 6. Charts

### 6.1 GST Liability vs ITC Utilised (Bar — Monthly)
- **Series:** Liability (orange) · ITC Utilised (blue) · Cash Paid (green)
- **Export:** PNG

### 6.2 TDS Compliance Rate (Donut)
- **Segments:** Deposited on time · Late · Pending

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Return marked filed | "GSTR-[N] marked as filed for [Entity]." | Success | 3s |
| Export | "Tax compliance report exported." | Info | 3s |

---

## 8. Empty States

| Condition | Heading | Description |
|---|---|---|
| All returns filed | "All returns filed" | "All GST returns are filed for this period." |
| No TDS obligations | "No TDS this period" | "No TDS deductions recorded for this period." |

---

## 9. Loader States

| Trigger | Loader |
|---|---|
| Page load | Skeleton KPIs + 3 section skeletons |
| Month/FY switch | Table skeletons |

---

## 10. Role-Based UI Visibility

| Element | Tax Officer G1 | CFO G1 | Finance Mgr G1 | Auditor G1 |
|---|---|---|---|---|
| [Mark Filed] action | ✅ | ❌ | ❌ | ❌ |
| All sections | ✅ | ✅ | ✅ | ✅ |
| Export | ✅ | ✅ | ✅ | ✅ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/finance/tax/kpis/` | JWT (G1+) | KPI cards |
| GET | `/api/v1/group/{id}/finance/tax/gst-status/` | JWT (G1+) | GST return status table |
| PUT | `/api/v1/group/{id}/finance/tax/gst-returns/{rid}/mark-filed/` | JWT (G1) | Mark return filed |
| GET | `/api/v1/group/{id}/finance/tax/tds-status/` | JWT (G1+) | TDS status |
| GET | `/api/v1/group/{id}/finance/tax/filing-calendar/` | JWT (G1+) | Next 30 days events |
| GET | `/api/v1/group/{id}/finance/tax/export/` | JWT (G1+) | Export |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| FY switch | `change` | GET `.../tax/?fy=` | `#dashboard-body` | `innerHTML` |
| Mark filed | `click` | PUT `.../gst-returns/{id}/mark-filed/` | `#gst-row-{id}` | `outerHTML` |
| Page load | `load` | GET `.../tax/kpis/` | `#kpi-bar` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
