# 03 — Group Accounts Manager Dashboard

- **URL:** `/group/finance/accounts/`
- **Template:** `portal_base.html`
- **Priority:** P0
- **Role:** Group Accounts Manager (Role 32, G1)

---

## 1. Purpose

The Accounts Manager Dashboard centralises the ledger view for the entire group — vendor payables outstanding across branches, student fee receivables, and bank reconciliation status. The Accounts Manager (G1) does not post transactions directly to the platform; instead, this dashboard aggregates data fed by branch accountants and provides a consolidated group-level ledger intelligence layer.

Critical decisions enabled here: which vendors are overdue for payment (risking supply disruption), which branches have the highest student fee receivables (cash flow risk), and whether all branch bank accounts are reconciled for the period. The Accounts Manager is also responsible for detecting duplicate or erroneous entries before they flow into the Finance Manager's reconciliation.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Accounts Manager | G1 | Full read — all sections | Primary owner |
| Group Finance Manager | G1 | Read — all sections | |
| Group CFO | G1 | Read — all sections | |
| Group Internal Auditor | G1 | Read — all sections | |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Finance → Accounts Manager Dashboard
```

### 3.2 Page Header
- **Title:** `Accounts Manager Dashboard`
- **Subtitle:** `Cross-Branch Ledger Overview · FY [Year]`
- **Role Badge:** `Group Accounts Manager`
- **Right-side controls:** `[Financial Year ▾]` `[As-of Date ▾]` `[Export ↓]`

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| Vendor invoice overdue > 30 days | "[N] vendor invoices overdue by more than 30 days. Total: ₹[X]." | Red |
| Bank reconciliation not done for any branch in current month | "[N] branch(es) missing bank reconciliation for [Month]." | Amber |
| Student receivable > 60 days | "₹[X] in student fee receivables aged > 60 days." | Amber |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Total Vendor Payable | Sum outstanding | Red if > ₹50L | → Page 19 |
| Overdue Vendor Invoices | Count > 30 days | Green = 0 · Red > 0 | → Page 19 |
| Total Student Receivable | Sum outstanding | Red if > 10% of annual demand | → Page 20 |
| Bank Recon Status | Branches reconciled / Total | Green = 100% | → Page 21 |
| Aged Payable > 60 days | ₹ sum | Red if > ₹0 | → Page 19 |

---

## 5. Section 5.1 — Vendor Payable Summary

| Column | Type | Sortable |
|---|---|---|
| Vendor | Text | ✅ |
| Category | Badge: Books · Uniforms · Lab · IT · Infra · Other | ✅ |
| Total Invoices | Number | ✅ |
| Amount Due | ₹ | ✅ |
| Overdue Amount | ₹ (red if > 0) | ✅ |
| Oldest Invoice | Date | ✅ |
| Actions | View Details | — |

**[View Full Payable Tracker →]** links to Page 19.

---

## 5.2 Section 5.2 — Student Fee Receivable Summary (by Branch)

| Column | Type | Sortable |
|---|---|---|
| Branch | Text | ✅ |
| Total Outstanding | ₹ | ✅ |
| 0–30 days | ₹ | ✅ |
| 31–60 days | ₹ | ✅ |
| > 60 days | ₹ (red) | ✅ |
| Defaulters | Count | ✅ |
| Actions | View Branch | — |

**[View Full Receivable Tracker →]** links to Page 20.

---

## 5.3 Section 5.3 — Bank Reconciliation Status

| Column | Type | Sortable |
|---|---|---|
| Branch | Text | ✅ |
| Bank Account | Text | ✅ |
| Last Reconciled | Date | ✅ |
| Status | Badge: Reconciled · Pending · Discrepancy | ✅ |
| Unreconciled Entries | Count | ✅ |
| Actions | View | — |

**[View Full Bank Reconciliation →]** links to Page 21.

---

## 6. Charts

### 6.1 Payable Ageing (Stacked Bar)
- **Groups:** 0–30 days · 31–60 days · 61–90 days · > 90 days
- **Series:** Per vendor category
- **Export:** PNG

### 6.2 Student Receivable by Branch (Bar)
- **Data:** ₹ outstanding per branch
- **Colour:** Green < 5% of demand · Amber 5–10% · Red > 10%

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Export | "Accounts summary exported." | Success | 3s |

---

## 8. Empty States

| Condition | Heading | Description |
|---|---|---|
| No vendor payables | "No outstanding payables" | "All vendor invoices are cleared." |
| No receivables | "No outstanding receivables" | "All student fee dues are collected." |

---

## 9. Loader States

| Trigger | Loader |
|---|---|
| Page load | Skeleton KPIs + 3 section skeletons |
| FY switch | Full page skeleton |

---

## 10. Role-Based UI Visibility

| Element | Accounts Mgr G1 | Finance Mgr G1 | CFO G1 |
|---|---|---|---|
| All sections | ✅ | ✅ | ✅ |
| Export | ✅ | ✅ | ✅ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/finance/accounts/kpis/` | JWT (G1+) | KPI cards |
| GET | `/api/v1/group/{id}/finance/accounts/payable-summary/` | JWT (G1+) | Vendor payable table |
| GET | `/api/v1/group/{id}/finance/accounts/receivable-summary/` | JWT (G1+) | Student receivable by branch |
| GET | `/api/v1/group/{id}/finance/accounts/bank-recon-status/` | JWT (G1+) | Bank reconciliation status |
| GET | `/api/v1/group/{id}/finance/accounts/export/` | JWT (G1+) | Export |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| FY switch | `change` | GET `.../accounts/?fy=` | `#dashboard-body` | `innerHTML` |
| Page load | `load` | GET `.../accounts/kpis/` | `#kpi-bar` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
