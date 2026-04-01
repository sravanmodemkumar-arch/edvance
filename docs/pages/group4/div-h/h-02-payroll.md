# H-02 — Payroll Processing & TDS

> **URL:** `/college/hr/payroll/`
> **File:** `h-02-payroll.md`
> **Priority:** P1
> **Roles:** HR Officer (S3) · Finance Manager (S4) · Accounts Officer (S3) · Principal/Director (S6)

---

## 1. Payroll Structure

```
PAYROLL STRUCTURE — GCEH Faculty (AICTE Pay Scales 2019)

PAY SCALE (AICTE — 7th CPC rationalized):
  Level  | Designation              | Pay (min–max)         | AGP
  ───────────────────────────────────────────────────────────────────────────
  10     | Assistant Professor      | ₹57,700 – ₹1,82,400  | ₹6,000
  11     | Assistant Professor Sr.  | ₹68,900 – ₹2,05,500  | ₹7,000
  12     | Associate Professor      | ₹1,01,500 – ₹2,15,900| ₹9,000
  14     | Professor                | ₹1,44,200 – ₹2,18,200| ₹10,000

SALARY COMPONENTS (sample — Dr. Suresh K., Associate Professor):
  Basic Pay:                ₹1,12,400/month  (Level 12, Stage 4)
  Academic Grade Pay:       ₹9,000 (included in basic — AICTE 7th CPC unified)
  Dearness Allowance (DA):  ₹44,960 (DA rate: 40% of basic — central DA rate)
  House Rent Allowance:     ₹20,232 (HRA 18% — X city: Hyderabad)
  Transport Allowance:      ₹3,600 (standard unaided college rate)
  Medical Allowance:        ₹1,000 (GCEH policy — above minimum)
  Special Allowance:        ₹2,000 (departmental coordinator — Dr. Suresh)

GROSS SALARY:              ₹1,83,192/month

DEDUCTIONS:
  EPF Employee (12%):      ₹13,488 (12% of basic ₹1,12,400)
  Professional Tax:         ₹200
  TDS (Income Tax):         ₹22,800 (estimated monthly; recomputed quarterly)
  Health Insurance:         ₹1,200 (group mediclaim — employee share)

NET SALARY:                ₹1,45,504/month

PAYROLL TOTAL — GCEH (62 faculty + 38 non-teaching = 100 staff):
  Gross salaries:           ₹47.32L/month (faculty ₹38.2L + non-teaching ₹9.12L)
  Total deductions:         ₹9.84L
  Net disbursement:         ₹37.48L/month
  Annual payroll:           ₹5.67Cr
```

---

## 2. TDS on Salary (Section 192)

```
TDS — SECTION 192 (Salary)
(Annual computation for each employee; deducted monthly)

TDS COMPUTATION — Dr. Suresh K. (FY 2026–27):

GROSS INCOME:
  Gross salary (annual):               ₹21,98,304
  Less: HRA exemption (metro city):
    Actual HRA: ₹2,42,784
    50% of basic: ₹6,74,400
    Rent paid - 10% basic: ₹3,60,000 - ₹1,12,400×10% = ₹2,47,600
    HRA exemption = min(₹2,42,784, ₹6,74,400, ₹2,47,600) = ₹2,42,784 ✅
  Standard Deduction: ₹75,000 (Budget 2024 revision — effective from FY 2024-25)
  Professional Tax: ₹2,400/year (Sec 16(iii))

TAXABLE SALARY:                        ₹19,78,120

CHAPTER VI-A DEDUCTIONS:
  Section 80C: ₹1,50,000 (EPF ₹1,61,856 → capped at ₹1,50,000)
  Section 80D: ₹25,000 (health insurance — self + family)
  Section 80CCD(1B): ₹50,000 (NPS — if enrolled; Dr. Suresh enrolled ✅)
  Total deductions: ₹2,25,000

NET TAXABLE INCOME: ₹17,53,120

TAX COMPUTATION (FY 2026–27 — Old Regime opted):
  0–2,50,000:       Nil
  2,50,001–5,00,000: 5% × ₹2,50,000 = ₹12,500
  5,00,001–10,00,000: 20% × ₹5,00,000 = ₹1,00,000
  10,00,001–17,53,120: 30% × ₹7,53,120 = ₹2,25,936
  Tax before surcharge: ₹3,38,436
  Health & Education Cess (4%): ₹13,537
  Total tax: ₹3,51,973
  Monthly TDS: ₹29,331

INVESTMENT PROOF COLLECTION:
  Date: January 2027 (annual proof collection — not just declaration)
  Proofs: LIC premium receipt, EPF passbook, NPS statement, health insurance
  Tax regime choice: Mandatory by April (start of FY); cannot change mid-year
  New regime vs Old: Dr. Suresh: Old regime more beneficial (heavy deductions)
  EduForge: Both regimes computed; system recommends optimal regime

FORM 16:
  Due: 15 June 2027 (for FY 2026–27)
  Part A: TDS deducted and deposited (generated from 24Q)
  Part B: Salary details + deductions + tax computation
  EduForge: Auto-generates Form 16 for all employees + digital signature
```

---

## 3. Payroll Processing Calendar

```
PAYROLL CALENDAR — Monthly Process

Day 1–3:   HR Officer finalises attendance (biometric data + leave deductions)
Day 3–4:   Leave deductions: LOP (Loss of Pay) computed
           New joins / exits this month: Salary pro-rated
Day 4:     Payroll inputs locked (no further changes after lock)
Day 5:     Finance Manager reviews payroll (anomaly check)
           System flags: Any salary >110% of last month (possible error)
           System flags: Any new join without appointment letter ← hard block
Day 6:     Principal approves payroll (digital approval in EduForge)
Day 7:     Salary NEFT batch uploaded to bank (HDFC/SBI payroll account)
Day 8:     Salaries credited to employee accounts
           Payslips: Auto-generated and emailed + EduForge app notification
Day 9:     EPF challan computed (Month's total EPF)
Day 15:    EPF ECR filed and challan paid ← mandatory deadline
Day 20:    GST returns (if applicable)
TDS:       Quarterly (June/Sep/Dec/Mar) — 24Q TDS return filed
           Monthly: TDS deposited by 7th of following month

MARCH 2027 PAYROLL:
  Salaries disbursed: ✅ 8 March 2027
  EPF challan: ⬜ Due 15 April 2027
  Q4 TDS (Jan–Mar): ⬜ Due 31 May 2027 (24Q)
  Form 16 (FY 2026–27): ⬜ Due 15 June 2027
```

---

## 4. Contract / Visiting Faculty Payroll

```
CONTRACT / VISITING FACULTY

CONTRACT FACULTY (full-time, fixed-term):
  Pay: ₹35,000–₹60,000/month (consolidated; no DA/HRA/EPF for contract)
  TDS: Section 192 (if salary) or Section 194J (professional fees — 10%)
       If on payroll as "salary": Section 192
       If on invoice as "honorarium/professional fees": Section 194J (10%)
  GCEH policy: Contract faculty on payroll (Section 192) for administrative clarity

VISITING FACULTY (per-lecture basis):
  Pay: ₹1,000–₹2,000/lecture (agreed per session)
  Payment: Monthly consolidated invoice
  TDS: Section 194J — 10% TDS (professional services)
  No EPF (not a regular employee)
  Threshold: TDS if total payment >₹30,000 in a year

GUEST LECTURERS (1-2 sessions per year):
  Payment: ₹2,000–₹5,000 per session (honorarium)
  TDS: Section 194J if >₹30,000/year total to same person
  Receipt: Acknowledge receipt in writing (EduForge generates)

CONSOLIDATED VISITING/CONTRACT TDS:
  March 2027: ₹28,400 TDS collected (Section 194J — visiting faculty)
  Deposited: ✅ 7 April 2027 (within deadline)
```

---

## 5. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/college/{id}/hr/payroll/monthly/?month=2027-03` | Monthly payroll register |
| 2 | `POST` | `/api/v1/college/{id}/hr/payroll/process/` | Trigger payroll processing |
| 3 | `GET` | `/api/v1/college/{id}/hr/payroll/tds/{employee_id}/` | TDS computation for employee |
| 4 | `GET` | `/api/v1/college/{id}/hr/payroll/form16/` | Form 16 generation (all employees) |
| 5 | `GET` | `/api/v1/college/{id}/hr/payroll/epf/ecr/` | EPF ECR data |

---

## 6. Business Rules

- TDS on salary is the employer's statutory duty under Section 192; non-deduction, under-deduction, or failure to deposit TDS by the 7th of the following month attracts interest at 1.5% per month and penalties; the employee's PAN must be available at the time of payment, or TDS must be deducted at 20% (higher rate — Section 206AA); EduForge validates PAN format before allowing an employee on payroll
- HRA exemption requires the employee to submit rent receipts if rent >₹1L/year (requires landlord PAN for amounts >₹1L/month per payment); employer must collect this proof; failure to obtain and retain proof makes the HRA exemption invalid in an audit; EduForge's annual proof collection module tracks who has submitted HRA receipts vs rent declaration only
- Salary to contract faculty vs visiting faculty has different TDS treatment; using Section 192 (payroll) vs 194J (professional fees) is a genuine choice that has tax consequences for both the college and the recipient; the choice should be consistent and defensible — EduForge's contract faculty module flags the TDS treatment at appointment time for Finance Manager review
- New Regime vs Old Regime choice by employees must be documented; from FY 2023-24, the new regime is the default; employees must opt-in to old regime in writing each year; employers who apply old regime without written opt-in are non-compliant; EduForge's TDS module presents both computations to each employee at year-start and records their written choice
- Payroll anomaly detection (salary >110% of previous month) is a critical internal control; payroll fraud is more common in educational institutions than perceived — ghost employees, inflated salaries, unauthorized increments; automated anomaly detection with mandatory Finance Manager review is the first line of defence

---

*Last updated: 2026-03-27 · Group 4 — College Portal · Division H*
