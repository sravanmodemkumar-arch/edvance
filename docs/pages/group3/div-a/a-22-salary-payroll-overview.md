# A-22 — Salary & Payroll Overview

> **URL:** `/school/admin/finance/payroll/`
> **File:** `a-22-salary-payroll-overview.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Promoter (S7) — full · Principal (S6) — view · VP Admin (S5) — view · Accountant (S4 Finance) — full

---

## 1. Purpose

Overview of the school's monthly payroll — salary disbursement status, salary register, PF/ESI compliance, and total salary expenditure vs budget. The detailed salary slip generation and salary structure editing are in div-e (Finance module), but leadership views payroll summary here.

**Indian payroll context:**
- All employees with salary > ₹15,000/month must be covered under EPFO (Provident Fund): 12% employee + 12% employer contribution
- Employees with salary < ₹21,000/month: ESIC (Employee State Insurance Corporation) mandatory
- Professional Tax: state-specific; applicable in Maharashtra, Karnataka, TS, AP, WB etc.
- TDS: deducted for employees with income tax liability
- Salary disbursement by 7th of the following month (standard Indian practice)

---

## 2. Page Layout

### 2.1 Header
```
Salary & Payroll — March 2026               [Process Payroll]  [Export Salary Register]  [PF Statement]
Month: March 2026 ▼      Status: 🟡 PENDING DISBURSEMENT
```

Payroll status flow: DRAFT → REVIEWED → APPROVED → DISBURSED → CLOSED

---

## 3. Monthly Payroll Summary (current month)

| Component | Amount |
|---|---|
| Gross Salary (all staff) | ₹5.18L |
| — Teaching Staff (78) | ₹4.18L |
| — Non-Teaching (24) | ₹0.85L |
| — Contract Staff (8) | ₹0.15L |
| Deductions |
| — Employee PF (12%) | ₹0.28L |
| — Employee ESI (0.75%) | ₹0.02L |
| — Professional Tax | ₹0.012L |
| — TDS | ₹0.04L |
| **Net Pay (Total take-home)** | **₹4.84L** |
| Employer Contributions |
| — Employer PF (12%) | ₹0.28L |
| — Employer ESI (3.25%) | ₹0.07L |
| **Total Employer Cost** | **₹5.53L** |

---

## 4. Salary Register Table

| Staff Name | Dept | Basic | DA | HRA | Other Allow | Gross | PF | ESI | PT | TDS | Net Pay | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Ms. Sudha Rani | Science | ₹42,000 | ₹4,200 | ₹6,300 | ₹2,500 | ₹55,000 | ₹5,040 | — | ₹200 | ₹1,200 | ₹48,560 | PENDING |
| … | … | … | … | … | … | … | … | … | … | … | … | … |

Exportable as Excel/PDF.

---

## 5. Disbursement Status

| Disbursement Method | Staff Count | Amount | Status |
|---|---|---|---|
| Bank Transfer (NEFT) | 94 | ₹4.62L | Pending (due 7 Apr) |
| Cash (class IV employees) | 16 | ₹0.22L | Pending |
| **Total** | **110** | **₹4.84L** | **PENDING** |

[Mark as Disbursed] button (Principal / Promoter confirmation required).

---

## 6. PF & ESI Compliance

| Statutory | Due Date | Status | Payment |
|---|---|---|---|
| EPF Monthly Return (ECR) | 15th of next month | Pending | ₹0.56L (both shares) |
| ESIC Monthly Return | 15th of next month | Pending | ₹0.09L (both shares) |
| PT (Professional Tax) | 10th of next month | Pending | State-specific |

[Generate EPF ECR File] → standard ECR file format for EPFO portal upload
[Generate ESIC Challan] → ESIC challan for portal submission

---

## 7. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/payroll/?month={month}` | Monthly payroll summary |
| 2 | `GET` | `/api/v1/school/{id}/payroll/register/?month={month}` | Full salary register |
| 3 | `POST` | `/api/v1/school/{id}/payroll/disburse/` | Mark payroll as disbursed |
| 4 | `GET` | `/api/v1/school/{id}/payroll/epf-ecr/?month={month}` | EPF ECR file download |
| 5 | `GET` | `/api/v1/school/{id}/payroll/esic-challan/?month={month}` | ESIC challan |
| 6 | `GET` | `/api/v1/school/{id}/payroll/export/?month={month}` | Salary register Excel/PDF |

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division A*
