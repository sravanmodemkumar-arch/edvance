# L-14 — HR Reports & Analytics

> **URL:** `/school/hr/reports/`
> **File:** `l-14-hr-reports.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** HR Officer (S4) — generate and export reports · Principal (S6) — view all HR analytics · Vice Principal (S5) — operational HR reports · Accounts Officer (S3) — payroll-related reports only

---

## 1. Purpose

HR Reports consolidate data from all L-module sub-systems into actionable insights for school management. Key audiences:
- **Principal:** Strategic view — attrition, performance distribution, training compliance, payroll cost
- **VP:** Operational — attendance patterns, workload balance, substitute burden
- **HR Officer:** Compliance — CBSE staff register, EPF/PT/TDS statutory reports, CBSE inspection packages
- **Accounts:** Payroll cost, EPF ECR, TDS summaries

Regulatory context: CBSE requires schools to maintain staff registers in prescribed format; during inspections, the following are verified: total teaching staff vs PTR, qualification register, training records, service records. This module generates these in CBSE inspection-ready format.

---

## 2. HR Dashboard — Principal View

```
HR DASHBOARD — GREENFIELDS SCHOOL
As of: 27 March 2026

WORKFORCE OVERVIEW:
  Total Staff: 127
  ┌──────────────────────────────────────────────┐
  │  Teaching Staff (full-time):        52       │
  │  Non-Teaching Staff (admin/support): 38      │
  │  Drivers + Escorts:                 24       │
  │  Hostel Staff:                       8       │
  │  Contract/Part-time:                 5       │
  └──────────────────────────────────────────────┘
  On leave today: 4 (3 approved, 1 absent-unintimated ⚠)
  New joiners this month: 2 (Ms. Anita Rao – TCH, Mr. Suresh R. – TCH)
  Separations this month: 1 (Ms. Priya Iyer – resignation, LWD 14 Apr 2026)

PAYROLL SUMMARY — March 2026:
  Gross payroll:              ₹47,32,840
  EPF (employer contribution): ₹5,27,940  (12% of eligible basic)
  Professional Tax (TS):         ₹24,500
  TDS (Sec 192) deducted:      ₹3,18,200
  Net payroll (NEFT):          ₹43,44,200
  Disbursed on: 7 March 2026 ✅

COMPLIANCE ALERTS:
  ⚠ 3 staff pending BGV renewal (>5 years, K-05)
  ⚠ 1 teacher (Mr. Vijay P.) on PIP — review due 30 July 2026
  ✅ POCSO training: 85/87 staff (Jun 2025) — next annual: Jun 2026
  ✅ EPF ECR submitted: Mar 2026 (by 15 Mar) ✅
  ✅ TDS Q3 return filed: 31 Jan 2026 ✅

ATTRITION (2025–26):
  Separations YTD: 5 (2 resignations, 2 non-renewals, 1 retirement)
  Attrition rate: 5/127 = 3.9% ✅ (Target: <10%)
  Average tenure at separation: 4.2 years
```

---

## 3. Staff Register — CBSE Format

```
STAFF REGISTER — CBSE AFFILIATION FORMAT
School: GREENFIELDS, Hyderabad | Affiliation No.: 1200XXX
Academic Year: 2025–26

─────────────────────────────────────────────────────────────────────────────────────────────────
S# Emp-ID  Name              Designation    Subject      Qual              TET    Date-Join  Basic
─────────────────────────────────────────────────────────────────────────────────────────────────
1  TCH-001 Ms. Meena Rao     Principal      —            M.Ed, Ph.D        N/A    01-Jun-12  82,000
2  TCH-003 Ms. Kavitha N.    HOD-Maths      Mathematics  M.Sc, B.Ed        CTET   15-Jun-15  62,000
3  TCH-012 Mr. Ravi Kumar    Sr. Teacher    Physics      M.Sc Phys, B.Ed   CTET   10-Jul-17  52,000
4  TCH-031 Ms. Geeta Sharma  Sr. Teacher    Soc Science  B.A., B.Ed        CTET   10-Jul-18  51,000
5  TCH-032 Mr. Arjun R.      Teacher        Soc Science  B.A., B.Ed        CTET   5-Jun-19   42,000
...
[52 teaching staff total]

QUALIFICATION COMPLIANCE (CBSE Bye-Laws):
  All Classes I–VIII teachers with TET:    47/49  ✅ (2 have TET in process — noted)
  All Classes IX–XII teachers:             27/27  ✅ (TET not required for senior secondary)
  Principal qualification (PG + B.Ed):    ✅
  PTR compliance (≤30:1):                 ✅ (23.8:1)

[Download CBSE Staff Register PDF]  [Export Excel]
```

---

## 4. Attendance Analytics

```
ATTENDANCE ANALYTICS — 2025–26 (April 2025 – March 2026)

Overall staff attendance:
  Working days: 220 (K-11)
  Average staff attendance rate: 94.7%

ATTENDANCE PATTERN ANALYSIS:
  ┌─────────────────────────────────────────────────────┐
  │ Month-wise absenteeism (unplanned leave + LOP):     │
  │                                                     │
  │  Apr 25: 3.2%  │  Oct 25: 2.8%                     │
  │  May 25: 2.9%  │  Nov 25: 3.1%                     │
  │  Jun 25: 4.1%  │  Dec 25: 5.8% ← spike (winter)   │
  │  Jul 25: 3.3%  │  Jan 26: 3.6%                     │
  │  Aug 25: 3.5%  │  Feb 26: 2.9% ← exam period low  │
  │  Sep 25: 3.0%  │  Mar 26: 3.4%                     │
  └─────────────────────────────────────────────────────┘
  Observation: Dec spike likely weather-related; Feb low is expected (exam duty)

HIGH-ABSENCE STAFF (>12 days unplanned absence this year):
  Mr. Vijay P. (TCH-044): 18 days — also on PIP (HR flag: pattern correlation)
  Ms. Radha N. (TCH-028): 14 days — personal reasons disclosed to HR (noted)

  [Welfare referral recommended for Mr. Vijay P. — absence + performance flag]

MONDAY/FRIDAY PATTERN FLAGS (potential attendance gaming):
  Flagged staff (>3 Monday/Friday absences in 6 months):
    None flagged this period ✅
```

---

## 5. Payroll Cost Report

```
PAYROLL COST ANALYSIS — 2025–26

Annual payroll cost (gross, all staff):     ₹5,62,84,080
Employer EPF contribution:                  ₹46,42,320
EDLI + EPF admin charges:                   ₹5,40,000
PT employer (not applicable in TS)          ₹0
Total employment cost:                      ₹6,14,66,400

COST BREAKDOWN BY CATEGORY:
  Category              Headcount   Annual Gross       % of Total
  Teaching — Senior         18      ₹2,28,96,000        40.7%
  Teaching — Regular        34      ₹1,86,42,000        33.1%
  Non-teaching (admin)      38      ₹95,04,000          16.9%
  Transport (drivers/esc)   24      ₹38,40,000           6.8%
  Hostel staff               8      ₹14,40,000           2.6%
  Part-time/Contract         5      ₹(as incurred)       —

SALARY TREND (year-on-year growth):
  2023–24 → 2024–25: +8.2% (increment + 2 new hires)
  2024–25 → 2025–26: +7.8% (increment + 1 promotion + 3 new hires)
  Projected 2025–26 → 2026–27: +8.5% (planned increments + 2 new hires)

GRATUITY PROVISION (actuarial):
  Total gratuity liability (all staff): ₹42,18,500
  New accrual this year:                ₹4,86,000
  Paid this year (1 retirement):        ₹3,24,000
  Closing provision:                    ₹43,80,500
  [Provision recommended in school accounts as per AS-15]
```

---

## 6. Training Compliance Report

```
TRAINING COMPLIANCE — 2025–26

MANDATORY TRAINING STATUS:
  Training             Due Date    Completed   Pending   Compliance
  POCSO Awareness      Jun 2025    85/87       2/87      97.7% ⚠ (2 pending)
  DPDPA Awareness      Jun 2025    85/87       2/87      97.7% ⚠
  Fire Safety          Jul 2025    87/87       0/87      100% ✅
  First Aid Refresh    Jul 2025    72/87       15/87     82.8% ⚠

  Pending (POCSO):  Ms. Anita Rao (new joiner — due within 30 days of joining),
                    Ms. Radha N. (missed June session — makeup scheduled 10 Apr)
  Note: Both are tracked; neither is a final compliance failure at this point.

CBSE i-EXCEL COMPLETION:
  Social Science (new pattern):  4/4 ✅
  Mathematics:                   5/5 ✅
  Science new NCERT:             3/3 ✅

PROFESSIONAL DEVELOPMENT (CEP points):
  Teachers exceeding 12 CEP target: 31/52 (59.6%)
  Teachers meeting 12 CEP exactly:  14/52 (26.9%)
  Teachers below 12 CEP:             7/52 (13.5%) ⚠ — flag for next appraisal cycle

[Export training compliance for CBSE inspection]
```

---

## 7. Appraisal Distribution Report

```
APPRAISAL DISTRIBUTION — 2025–26

TEACHING STAFF (52):
  Rating                Count   %
  Outstanding            6     11.5%
  Exceeds Expectations  22     42.3%
  Meets Expectations    20     38.5%
  Needs Improvement      3      5.8%
  Unsatisfactory         1      1.9%

  Average score: 74.2/100 (vs benchmark 70+)
  Promoted (T-2→T-3): 3 staff
  PIP initiated: 1 staff (Mr. Vijay P.)
  Merit increment granted: 6 staff

DISTRIBUTION CHECK:
  Bell-curve target: Outstanding <15%, Exceeds 35–45%, Meets 35–45%, Needs/Unsat <10%
  Actual: Within targets ✅

NON-TEACHING STAFF (38):
  Satisfactory or above: 36/38 (94.7%)
  Needs review: 2/38 (HR follow-up in progress)

[Export appraisal summary for board]  [Individual report links → L-06]
```

---

## 8. Attrition Report

```
ATTRITION ANALYSIS — 2025–26

SEPARATION SUMMARY:
  Type                  Count   Average Tenure   Key Reasons
  Resignation           2       4.5 years        Personal (relocation, family)
  Non-renewal           2       1.2 years        Performance + probation failure
  Retirement            1       18 years         Age (Ms. Kamala V.)
  Termination           0       —                —
  Total                 5       —

ATTRITION RATE: 5/127 = 3.9% ✅ (industry average for CBSE schools: 12–15%/year)

EXIT INTERVIEW THEMES (from 3 conducted):
  Positive (reasons for staying long):
    ● School culture and Principal leadership (mentioned by 2)
    ● Salary competitiveness (within Hyderabad CBSE market)
    ● Work environment
  Improvement areas:
    ● Communication of timetable changes (mentioned by 2)
    ● Extra duty compensation could be higher

STAY RISK ASSESSMENT:
  High-flight-risk staff (voluntary):
    [Identified through combination: PIP + Attendance + Manager feedback]
    Mr. Vijay P. (TCH-044): PIP + 18 absences + salary at lower band → Risk: High
    [1 other staff — name hidden in summary view; Principal can see details]

  Action recommended: VP retention conversation with at-risk staff before year-end

TENURE DISTRIBUTION:
  <1 year: 8 staff (new joiners)
  1–3 years: 22 staff
  3–7 years: 45 staff
  7–15 years: 38 staff
  >15 years: 14 staff
  Average tenure: 7.3 years ✅ (stable workforce)
```

---

## 9. Statutory Reports

```
STATUTORY REPORTS — GENERATED ON DEMAND

EPF Reports:
  EPFO ECR (Electronic Challan-cum-Return) — monthly by 15th
    Apr 2026 ECR: Generated ✅ | Submitted to EPFO: ✅ | Challan: ₹5,18,640
  Annual PF passbook update: April (for employees to verify)
  Form 3A (annual return): September ✅ (filed)
  Form 6A (annual consolidated):  ✅

TDS Reports:
  Form 16 (employee TDS certificate): Issued to all employees by 30 April ✅
  Form 24Q (quarterly TDS return):
    Q1 (Apr–Jun): Filed 31 Jul ✅
    Q2 (Jul–Sep): Filed 31 Oct ✅
    Q3 (Oct–Dec): Filed 31 Jan 2026 ✅
    Q4 (Jan–Mar): Due 31 May 2026 ⬜
  Form 26AS reconciliation: Monthly (payroll officer reviews) ✅

Professional Tax (Telangana):
  Monthly PT deduction: ₹24,500 (slab-wise from L-04)
  Remittance to TS Govt: By 10th of following month ✅
  Annual PT return: April ✅

Gratuity:
  Payment of Gratuity Act — register of employees eligible for gratuity maintained ✅
  Separations paid: 1 (Ms. Kamala V., retirement) — ₹3,24,000 paid 28 Feb 2026 ✅

[Generate EPF ECR]  [Generate Form 16 bulk]  [Download PT register]
```

---

## 10. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/hr/reports/dashboard/` | HR dashboard (Principal view) |
| 2 | `GET` | `/api/v1/school/{id}/hr/reports/staff-register/` | CBSE staff register (download) |
| 3 | `GET` | `/api/v1/school/{id}/hr/reports/attendance-analytics/` | Attendance patterns and flags |
| 4 | `GET` | `/api/v1/school/{id}/hr/reports/payroll-cost/` | Payroll cost and gratuity provision |
| 5 | `GET` | `/api/v1/school/{id}/hr/reports/training-compliance/` | Mandatory training status |
| 6 | `GET` | `/api/v1/school/{id}/hr/reports/appraisal-distribution/` | Appraisal distribution |
| 7 | `GET` | `/api/v1/school/{id}/hr/reports/attrition/` | Attrition and tenure analytics |
| 8 | `GET` | `/api/v1/school/{id}/hr/reports/statutory/epf-ecr/` | Generate EPF ECR |
| 9 | `GET` | `/api/v1/school/{id}/hr/reports/statutory/form16/?year={yr}` | Form 16 bulk generation |
| 10 | `GET` | `/api/v1/school/{id}/hr/reports/cbse-package/` | Full CBSE inspection package (ZIP) |

---

## 11. Business Rules

- The CBSE staff register must be maintained in the prescribed format (Affiliation Bye-Laws Schedule V); it includes every teacher's qualification, TET status, and date of joining; inspectors cross-verify this with individual service books (L-11); EduForge generates this automatically from the staff directory (L-01) and qualification records
- EPF ECR must be submitted to EPFO by the 15th of the following month; late submission incurs a penalty of ₹5/day per defaulting employee under EPF Act; the HR reports module generates the ECR text file in the EPFO upload format, which the Accounts Officer downloads and uploads to the EPFO employer portal
- Form 16 must be issued to all employees (including those who resigned mid-year) by 30 April; a Form 16 not issued is a TDS compliance failure; for separated employees, the Form 16 covers the period they were employed (e.g., Apr–Sep for someone who resigned in September); EduForge generates these automatically from the payroll data
- Attrition rate calculation uses total separations (all types) ÷ average headcount; a rate below 10% is considered healthy for Indian CBSE schools; the benchmark is important context for the Principal when reviewing HR reports
- The stay-risk / flight-risk identification is a sensitive feature — names of at-risk staff are visible only to Principal and HR Officer, not to VP (who may be the direct line manager and the reason for the risk); this prevents conflicts and ensures objective assessment
- The CBSE inspection package (endpoint 10) bundles all HR-related inspection documents in a single ZIP: staff register, qualification certificates (links to K-06), training records, timetable, workload register, service book exports for the last 3 years; this reduces inspection preparation from days to minutes

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division L*
