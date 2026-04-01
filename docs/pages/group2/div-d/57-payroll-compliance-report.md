# 57 — Payroll Compliance Report

- **URL:** `/group/finance/payroll/compliance/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Role:** Payroll Coordinator G0 (read-only) · Finance Manager G1

---

## 1. Purpose

The Payroll Compliance Report tracks statutory compliance obligations for payroll across all branches — PF (Provident Fund under EPF Act), ESI (Employees' State Insurance), PT (Profession Tax, state-specific), and TDS on salary (Form 24Q). Each compliance item has a due date, payment status, and challan reference.

This is the group-level consolidated compliance dashboard. Non-compliance with PF/ESI attracts penalties and damages; TDS non-compliance attracts interest (1.5% per month) and prosecution risk.

Data is sourced from the external payroll software and supplemented with challan references entered manually by the Payroll Coordinator.

---

## 2. Role Access

| Role | Level | Access |
|---|---|---|
| Group Payroll Coordinator | G0 | Read + add challan references |
| Group Finance Manager | G1 | Full read + approve |
| Group CFO | G1 | Read — summary |
| Group Internal Auditor | G1 | Read — audit |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Finance → Payroll → Payroll Compliance Report
```

### 3.2 Page Header
- **Title:** `Payroll Compliance Report`
- **Subtitle:** `[Month Year] · [N] Compliant · [X] Pending`
- **Right-side controls:** `[Month ▾]` `[Branch ▾]` `[Type ▾]` `[Export ↓]`

### 3.3 Alert Banner

| Condition | Banner | Severity |
|---|---|---|
| PF not deposited by 15th | "PF deposit for [Month] overdue for [N] branch(es)." | Red |
| ESI not deposited by 15th | "ESI deposit for [Month] overdue for [N] branch(es)." | Red |
| TDS not deposited | "TDS on salaries not deposited on time — penalty accruing." | Red |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule |
|---|---|---|
| PF Liability (Month) | ₹ | Neutral |
| PF Deposited | ₹ | Green if = liability |
| ESI Liability | ₹ | Neutral |
| ESI Deposited | ₹ | Green if = liability |
| PT Liability | ₹ | Neutral |
| TDS on Salary (Form 24Q) | ₹ | Neutral |
| Non-compliant Branches | Count | Red if > 0 |

---

## 5. Tabs

| Tab | Content |
|---|---|
| PF Compliance | Branch-wise PF status |
| ESI Compliance | Branch-wise ESI status |
| Profession Tax | Branch-wise PT status |
| Form 24Q (TDS Salary) | Quarterly return status |

---

## 6. Tab: PF Compliance

| Column | Type | Sortable |
|---|---|---|
| Branch | Text | ✅ |
| Eligible Employees | Count | ✅ |
| Employee PF (12%) | ₹ | ✅ |
| Employer PF (12%) | ₹ | ✅ |
| Admin Charges | ₹ | ✅ |
| Total PF | ₹ | ✅ |
| Due Date | Date (15th of month) | — |
| Challan No (ECR) | Text | ✅ |
| Deposit Date | Date | ✅ |
| Status | Badge: Deposited · Pending · Overdue | ✅ |
| Actions | Add Challan | — |

**PF Rates Reference:**
- Employee: 12% of Basic + DA
- Employer: 8.33% EPS + 3.67% EPF + 0.5% EDLI + 0.5% Admin

---

## 7. Tab: ESI Compliance

| Column | Type | Sortable |
|---|---|---|
| Branch | Text | ✅ |
| Eligible Employees (gross ≤ ₹21,000) | Count | ✅ |
| Employee ESI (0.75%) | ₹ | ✅ |
| Employer ESI (3.25%) | ₹ | ✅ |
| Total ESI | ₹ | ✅ |
| Due Date | Date (15th of month) | — |
| Challan No | Text | ✅ |
| Deposit Date | Date | ✅ |
| Status | Badge: Deposited · Pending · Overdue | ✅ |
| Actions | Add Challan | — |

---

## 8. Tab: Profession Tax (State-specific)

| Column | Type |
|---|---|
| Branch | Text |
| State | Text |
| PT Rate | ₹ per employee slab |
| Total PT | ₹ |
| Due Date | Date |
| Challan No | Text |
| Status | Badge |

---

## 9. Tab: Form 24Q (TDS on Salary)

| Quarter | Period | TDS Amount | Due Date | Status | ACK No | Filed Date |
|---|---|---|---|---|---|---|
| Q1 | Apr–Jun | ₹ | 31 Jul | Filed | [ACK] | [Date] |
| Q2 | Jul–Sep | ₹ | 31 Oct | Pending | — | — |
| Q3 | Oct–Dec | ₹ | 31 Jan | — | — | — |
| Q4 | Jan–Mar | ₹ | 31 May | — | — | — |

- [Mark Q[N] Filed] → opens drawer with ACK No entry

---

## 10. Drawers

### 10.1 Drawer: `add-challan` — Record Compliance Challan
| Field | Type | Required |
|---|---|---|
| Compliance Type | Read-only (PF/ESI/PT) | — |
| Branch | Read-only | — |
| Challan No (ECR/ESIC/PT) | Text | ✅ |
| Payment Date | Date | ✅ |
| Amount | Number | ✅ |
| Bank Account | Select | ✅ |
| Challan File | PDF upload | ❌ |

- [Save Challan]

### 10.2 Drawer: `form24q-file` — Mark Form 24Q Filed
| Field | Type | Required |
|---|---|---|
| Quarter | Read-only | — |
| ACK Number | Text | ✅ |
| Filed Date | Date | ✅ |
| FVU File No | Text | ❌ |

---

## 11. Charts

### 11.1 Monthly Compliance Status — PF+ESI+PT (Stacked Bar)
- **Series:** On time · Late · Pending

### 11.2 Total Payroll Deduction Composition (Donut)
- **Segments:** PF · ESI · PT · TDS · Others

---

## 12. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Challan saved | "PF/ESI/PT challan for [Branch] — [Month] recorded." | Success | 4s |
| Form 24Q filed | "Form 24Q for Q[N] filed. ACK: [No]." | Success | 4s |
| Overdue | "[Type] deposit for [Branch] is overdue. Penalty accruing." | Warning | 5s |
| Export | "Compliance report exported." | Info | 3s |

---

## 13. Empty States

| Condition | Heading | Description |
|---|---|---|
| All compliant | "Fully compliant" | "All payroll compliance obligations met for this month." |

---

## 14. Loader States

| Trigger | Loader |
|---|---|
| Page load | Skeleton KPIs + table |
| Tab switch | Table skeleton |
| Drawer | Spinner |

---

## 15. Role-Based UI Visibility

| Element | Payroll Coord G0 | Finance Mgr G1 | CFO G1 |
|---|---|---|---|
| [Add Challan] | ✅ | ✅ | ❌ |
| [Mark Form 24Q Filed] | ✅ | ✅ | ❌ |
| View all branches | ✅ | ✅ | ✅ |
| Export | ✅ | ✅ | ✅ |

---

## 16. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/finance/payroll/compliance/` | JWT (G0+) | Compliance summary |
| GET | `/api/v1/group/{id}/finance/payroll/compliance/?tab=pf` | JWT (G0+) | PF/ESI/PT/24Q |
| POST | `/api/v1/group/{id}/finance/payroll/compliance/{bid}/challan/` | JWT (G0) | Add challan |
| POST | `/api/v1/group/{id}/finance/payroll/compliance/24q/{qid}/file/` | JWT (G0) | Mark 24Q filed |
| GET | `/api/v1/group/{id}/finance/payroll/compliance/export/` | JWT (G0+) | Export |

---

## 17. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Month filter | `change` | GET `.../compliance/?month=&tab=pf` | `#compliance-section` | `innerHTML` |
| Tab switch | `click` | GET `.../compliance/?tab=esi` | `#compliance-tab-content` | `innerHTML` |
| Challan drawer | `click` | GET `.../compliance/{id}/challan-form/` | `#drawer-body` | `innerHTML` |
| Submit challan | `submit` | POST `.../compliance/{id}/challan/` | `#compliance-row-{id}` | `outerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
