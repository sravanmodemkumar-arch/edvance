# L-04 — Payroll Processing

> **URL:** `/school/hr/payroll/`
> **File:** `l-04-payroll.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Payroll Officer (S3) — process payroll · HR Officer (S4) — review and approve · Principal (S6) — final disbursement approval · Staff (S2–S6) — view own payslip only

---

## 1. Purpose

Monthly salary computation and disbursement for all staff. Payroll in India involves:
- **Gross salary computation** from L-05 salary structure
- **Statutory deductions:** EPF (Provident Fund), ESI (if applicable), Professional Tax (PT), TDS (income tax under Section 192)
- **Variable deductions:** LOP, loan EMI, advance recovery
- **Net pay disbursement** via bank transfer by 7th of following month (Payment of Wages Act)
- **Statutory filings:** EPF returns (monthly), ESI returns, TDS returns (quarterly)
- **Form 16:** Annual TDS certificate issued by April 30

---

## 2. Payroll Dashboard

```
Payroll Processing — March 2026                      [Run Payroll]  [Approve & Disburse]
Processing status: ⏳ In progress (run on 28 March; approval pending)

Employees: 87
Attendance data pulled from L-02: ✅ March 2026 (23 working days)
Leave data pulled from L-03: ✅ March 2026 (all approved leaves verified)

Summary (before approval):
  Total gross payroll: ₹28,45,600
  Total deductions: ₹5,12,340
    EPF (employee share 12%): ₹2,18,400
    Professional Tax: ₹32,500
    TDS: ₹1,84,200
    LOP deductions: ₹18,240 (4 employees with LOP)
    Other (loan EMI, advance): ₹59,000
  Total net payroll: ₹23,33,260
  Previous month: ₹23,18,400 (₹14,860 increase — 1 increment + 1 new joiner)

Employer contributions (not in net pay):
  EPF employer 12% (EPS 8.33% + EPF 3.67%): ₹2,18,400
  Total employer cost: ₹30,64,000

[Preview payslips]  [Export payroll register]  [Request Principal approval]
```

---

## 3. Individual Payslip

```
SALARY SLIP — March 2026

GREENFIELDS SCHOOL
Chaitanyapuri, Hyderabad — 500060

Employee: Ms. Geeta Sharma                Employee ID: TCH-031
Designation: Senior Teacher (Grade II)    Department: Social Science
Bank A/c: XXXXXX5678 (SBI)               PAN: ABCDE1234F
PF Account: HY/HYD/XXXXX                  Month: March 2026
Working days: 23  ·  Days paid: 23  ·  LOP: 0

EARNINGS:
  Basic Salary:              ₹42,000
  House Rent Allowance (HRA): ₹10,500  (25% of basic — hyderabad metro)
  Dearness Allowance (DA):    ₹4,200   (10% of basic — school policy)
  Conveyance Allowance:       ₹800     (standard)
  Medical Allowance:          ₹1,250   (standard ₹15,000/yr)
  Special Allowance:          ₹2,850   (to make up to CTC)
  ─────────────────────────────────────
  GROSS EARNINGS:            ₹61,600

DEDUCTIONS:
  EPF (Employee — 12% of basic):        ₹5,040
  Professional Tax (TS slab ₹400–₹300 for ₹61,600 bracket): ₹200
  TDS (Income Tax — estimated monthly):  ₹4,500
  ─────────────────────────────────────
  TOTAL DEDUCTIONS:          ₹9,740

NET SALARY PAYABLE:          ₹51,860

EMPLOYER'S CONTRIBUTION (for information):
  EPF Employer 12% (EPS 8.33% + EPF 3.67%): ₹5,040
  Total CTC:  ₹66,640/month (₹7,99,680/year)

Generated: 28 March 2026  ·  Disbursement date: 31 March 2026
[Download PDF payslip]
```

---

## 4. Payroll Processing Steps

```
Payroll Processing — March 2026 — Step by Step

Step 1: Import data (automatic)
  ☑ L-02 attendance: 23 working days — all staff ✅
  ☑ L-03 leave: All approved leaves imported (LOP: 4 employees × partial days) ✅
  ☑ L-05 salary structure: March increments applied (Ms. Sunita K. — annual increment) ✅
  ☑ Advance/loan repayments: 3 employees (from HR loan records) ✅

Step 2: Compute gross (28 March)
  ☑ Gross computed for all 87 employees ✅

Step 3: Statutory deductions
  ☑ EPF: Computed for all employees with basic ≤₹15,000 (mandatory) + voluntary contributions ✅
  ☑ PT: Computed per TS state slab ✅
  ☑ TDS: Computed per individual tax projections (annual TDS calculation / 12) ✅

Step 4: Review
  ⏳ Payroll Officer review (28 March — today)
  ⬜ HR Officer approval
  ⬜ Principal final approval

Step 5: Disbursement (31 March)
  ⬜ Bank file generated (NEFT bulk transfer)
  ⬜ Salary credited via NEFT (31 March target)

Step 6: Statutory filings (by 15th April)
  ⬜ EPF contribution upload to EPFO portal (by 15 Apr)
  ⬜ TDS deposit to government (by 7 Apr)
  ⬜ PT remittance to state (by 15 Apr)
```

---

## 5. TDS (Income Tax) Management

```
TDS — Section 192 — March 2026

All employees are employees per Income Tax Act; school is the "employer" responsible
for TDS deduction.

Employee TDS computation:
  Annual projected salary → Tax slabs (New vs Old regime — employee choice at start of year)
  Monthly TDS = (Annual tax liability) / 12

  Example: Ms. Geeta Sharma
    Annual CTC: ₹7,99,680
    Old regime: After standard deduction (₹50,000) + HRA exemption + 80C (PF = ₹60,480):
    Taxable: ~₹4,20,000 → Tax: ₹9,000 (at 5% above ₹2.5L slab) → Monthly TDS: ₹750
    (Simplified; actual computation uses Form 12BB submitted by employee)

Form 12BB collection:
  ☑ All employees submitted Form 12BB (investment declaration) by June 2025 ✅
  Proof collection (actual): March 2026 (before year end)
  Adjustments in Q4 for under/over deduction ✅

Form 16:
  Issued by: 30 April 2026 (statutory deadline)
  Issued to: All employees who had TDS deducted
  [Generate Form 16 for all employees]  [Download individual Form 16]

Quarterly TDS returns:
  Q1 (Apr–Jun): Due 31 Jul 2025 ✅ Filed
  Q2 (Jul–Sep): Due 31 Oct 2025 ✅ Filed
  Q3 (Oct–Dec): Due 31 Jan 2026 ✅ Filed
  Q4 (Jan–Mar): Due 31 May 2026 ⬜ Pending
```

---

## 6. EPF Management

```
EPF (Employees' Provident Fund) — March 2026

Applicable to: All employees (mandatory for basic ≤₹15,000; voluntary for higher)
  Current mandate: 44 employees with basic ≤₹15,000 (mandatory)
  Voluntary (higher salary, opted in): 28 employees
  Not enrolled (higher salary, opted out): 15 employees

Contribution:
  Employee: 12% of basic + DA = Employee EPF share
  Employer: 12% of basic + DA
    → 8.33% → EPS (Employee Pension Scheme — max ₹15,000 base)
    → 3.67% → EPF (Employer EPF share)
    → 0.5% → EDLI (Employee Deposit-Linked Insurance — employer only)
    → 0.85% → Admin charges

Monthly upload to EPFO (ECR — Electronic Challan-cum-Return):
  ☑ March ECR uploaded: 10 April 2026 deadline
  EPFO UAN (Universal Account Number): Allocated to all employees ✅
  [Upload March ECR]  [Pay challan]
```

---

## 7. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `POST` | `/api/v1/school/{id}/hr/payroll/run/` | Trigger payroll computation |
| 2 | `GET` | `/api/v1/school/{id}/hr/payroll/{month}/` | Payroll summary for month |
| 3 | `GET` | `/api/v1/school/{id}/hr/payroll/{month}/{staff_id}/` | Individual payslip |
| 4 | `POST` | `/api/v1/school/{id}/hr/payroll/{month}/approve/` | HR approve payroll |
| 5 | `POST` | `/api/v1/school/{id}/hr/payroll/{month}/disburse/` | Generate bank transfer file |
| 6 | `GET` | `/api/v1/school/{id}/hr/payroll/form16/{year}/{staff_id}/` | Form 16 for employee |
| 7 | `GET` | `/api/v1/school/{id}/hr/payroll/epf/{month}/` | EPF contribution summary |
| 8 | `GET` | `/api/v1/school/{id}/hr/payroll/export/?month={m}` | Payroll register export |

---

## 8. Business Rules

- Salary must be paid by the 7th of the following month (Payment of Wages Act Section 5); delayed payment exposes the school to wage dispute complaints; EduForge flags if payroll is not approved by the 5th
- EPF contributions must be deposited with EPFO by the 15th of the following month; default (delay) attracts penalty interest at 12% per annum + damages (3%–25% of arrears)
- TDS must be deposited with the income tax department by the 7th of the following month; delay attracts interest (1.5% per month) and penalty (under Sections 271C and 276B — up to prosecution for serious defaults)
- Professional Tax (PT) is state-specific; schools in different states configure the applicable slab; TS Professional Tax slabs are pre-loaded in EduForge for Telangana schools
- Form 16 (Part A from TRACES + Part B from employer) must be issued by April 30; employees use this for filing their income tax returns; failure to issue is a compliance violation
- Salary structure changes (increments, revisions) take effect from the date specified in the revision order; they cannot be backdated without Principal's written order; EduForge tracks the effective date of each revision

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division L*
