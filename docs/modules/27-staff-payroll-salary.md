# Module 27 — Staff Payroll & Salary

## 1. Purpose

Process, disburse, comply, and report on staff payroll across every institution type on EduForge —
schools (CBSE/state board/KVS/NVS/government-aided/unaided), colleges (UGC/AICTE/university-
affiliated), coaching institutes (JEE/NEET/UPSC/Banking/SSC), skill centres (NCVT/PMKVY/DDU-GKY),
and online programmes. Enforce EPF (12% employee + 12% employer split into EPS + EPF + EDLI),
ESI (0.75% employee + 3.25% employer; Rs. 21,000 gross threshold), Professional Tax (28-state
rule engine), TDS Section 192 (old vs new regime; investment declarations; Form 16; Form 24Q),
Gratuity (Payment of Gratuity Act 1972; Rs. 20 lakh ceiling), Maternity Benefit Act 1961
(26 weeks full pay), Payment of Bonus Act 1965, Minimum Wages Act, UGC/AICTE/state pay scale
compliance, Central DA revision (January + July), NPS (PRAN; 10%+14% contribution; CRA upload),
GPF (OPS employees), aided staff grant tracking, and 7-year immutable audit retention for all
payroll records. Module 27 owns salary structure, payroll computation, statutory deductions,
payslip generation, bank transfer file, F&F settlement, and all statutory filings. Module 08
owns attendance and staff profile. Module 26 owns ward fee dues recovery linked to F&F.
Module 39 owns relieving letter and experience certificate issuance.

---

## 2. Module Boundaries

### 2.1 What This Module Owns
- Salary structure definition per employee (CTC, components, deductions)
- Monthly payroll computation and approval workflow
- Statutory deduction calculation (EPF, ESI, PT, TDS, LWF, EDLI)
- Payslip generation and delivery
- Salary bank transfer file generation (NEFT bulk)
- EPF ECR, ESI challan, PT challan, TDS challan (ITNS 281) generation
- Form 16 (Part A + Part B), Form 24Q, Form 3A, Form 6A generation
- Gratuity accrual and provision
- Full & Final settlement computation
- Statutory registers (Form B, Form D, Overtime Register)
- Leave encashment computation
- NPS / GPF contribution tracking and CRA file generation
- Aided staff grant tracking and reconciliation

### 2.2 What This Module Reads
| Source | Data Read |
|---|---|
| Module 08 | Staff profile (joining date, designation, department, PAN, Aadhaar, bank account, UAN, PRAN); attendance (days worked, LWP days, OT hours) |
| Module 05 | Holidays (for overtime, compensatory off computation) |
| Module 26 | Ward fee dues (deducted from F&F salary if applicable) |
| Module 30 | Library book dues (no-dues clearance for F&F) |

### 2.3 What This Module Writes
| Destination | Data Written |
|---|---|
| Module 39 | Relieving letter trigger; experience certificate clearance flag |
| Module 26 | F&F deduction for ward fee outstanding |
| Module 08 | Payroll-linked flags: salary-on-hold, suspension subsistence allowance status |

---

## 3. Salary Structure

### 3.1 Earnings Components

| Component | Type | Taxability | Notes |
|---|---|---|---|
| Basic Salary | Fixed | Fully taxable | Foundation; all % components derived from this |
| Dearness Allowance (DA) | Fixed / DA-linked | Fully taxable | Govt/aided: Central/State DA rates; private: own % |
| HRA (House Rent Allowance) | Fixed | Partially exempt | Exemption = min(actual HRA, 50%/40% basic, rent−10% basic) |
| Special Allowance | Fixed | Fully taxable | Balances CTC; catch-all component |
| Conveyance Allowance | Fixed | Rolled into Rs. 50,000 standard deduction | Standard deduction covers from FY 2019-20 |
| Medical Allowance | Fixed | Rolled into standard deduction | Standard deduction covers |
| Education Allowance | Fixed | Rs. 100/child/month exempt (2 children) | Balance taxable |
| Children Education Allowance (CEA) | Fixed | Rs. 2,250/child/month exempt (govt; 2 children) | Private: own policy |
| LTA (Leave Travel Allowance) | Fixed | Exempt: 2 journeys / 4-year block within India | Proof required; excess taxable |
| Overtime Allowance | Variable | Fully taxable | Non-teaching + support staff only |
| Night Duty Allowance | Fixed | Fully taxable | Hostel wardens, security staff, night shift |
| Shift Allowance | Fixed | Fully taxable | Admin staff on alternate shifts |
| Research Allowance | Fixed | Exempt (if for research use) | UGC-linked; college professors only |
| NPA (Non-Practicing Allowance) | Fixed | Fully taxable | Medical college faculty; 25% of basic |
| Rural / Tribal Area Allowance | Fixed | Exempt per notified area | Govt staff posted to notified areas |
| Washing Allowance | Fixed | Taxable above Rs. 1,000/month | Housekeeping, sanitation staff |
| Risk Allowance | Fixed | Fully taxable | Lab assistants, security staff |
| Variable / Performance Pay | Variable | Fully taxable | Coaching institutes; formula-linked to student results |
| Retention Bonus | Event | Fully taxable | Annual; on completion of X years; not monthly |
| Festival Advance | Event | Not taxable at receipt; deducted from salary | Advance; no tax impact |

### 3.2 CTC vs Gross vs Net
- **CTC** (Cost to Company) = Gross salary + Employer EPF (12%) + Employer ESI (3.25% if applicable) + Employer EDLI (0.5%) + Employer EPF admin (0.5%) + Gratuity provision (4.81% of basic+DA) + any other employer cost
- **Gross Salary** = All earnings before deductions
- **Net Salary** (take-home) = Gross − all deductions (EPF employee + ESI employee + PT + TDS + LWF + loan EMI + other deductions)
- System stores and displays all three clearly; employees often confused about CTC vs take-home

### 3.3 UGC Pay Scales (7th Central Pay Commission)

| Designation | Pay Level | Pay Range |
|---|---|---|
| Assistant Professor | Level 10 | Rs. 57,700 – 1,82,400 |
| Assistant Professor (Senior Scale) | Level 11 | Rs. 67,700 – 2,08,700 |
| Assistant Professor (Selection Grade) | Level 12 | Rs. 78,800 – 2,09,200 |
| Associate Professor | Level 13A | Rs. 1,31,400 – 2,04,700 |
| Professor | Level 14 | Rs. 1,44,200 – 2,18,200 |
| Senior Professor | Level 15 | Rs. 1,82,200 – 2,24,100 |

### 3.4 State Pay Scales
- System stores pay matrix for each state's school teacher grades
- 28 state matrices maintained; updated on state pay revision
- States using Central pay scales: KVS, NVS, Sainik Schools, central university staff
- States with own scales: all 28 states + UT administrations
- Institution selects applicable state pay scale during Module 04 onboarding

### 3.5 Salary Grade / Pay Level per Employee
- Each employee assigned: pay_level, current_cell (position in pay matrix), annual_increment_date
- Pay matrix lookup: level × cell = basic pay
- Increment: moves employee to next cell in same level (July 1 for government; configurable for private)
- Promotion: moves employee to next level; pay fixed at next higher cell above current basic

---

## 4. Statutory Deductions — Deep Compliance

### 4.1 EPF (Employee Provident Fund) — EPF Act 1952

#### Employee Contribution
- 12% of (Basic + DA)
- If basic + DA ≤ Rs. 15,000: statutory contribution = 12% = Rs. 1,800 max
- If basic + DA > Rs. 15,000: employee may contribute on full salary (VPF) but statutory min = Rs. 1,800
- Employee can opt for higher contribution via VPF declaration

#### Employer Contribution Split
| Component | Rate | Basis | Cap |
|---|---|---|---|
| EPF (employer) | 3.67% | Basic + DA | No cap if employee contributes on full salary |
| EPS (Employee Pension Scheme) | 8.33% | Basic + DA | Capped at Rs. 1,250/month (Rs. 15,000 × 8.33%) |
| EDLI (Employee Deposit Linked Insurance) | 0.5% | Basic + DA | No cap; employer only |
| EPF Admin Charges | 0.5% | EPF wages | Reduced from 1.1% in 2020; employer only |

#### Higher EPS Pension Option (Supreme Court 2022)
- Employees hired before Sep 1, 2014 with basic > Rs. 15,000 can opt for EPS on actual basic (not Rs. 15,000 ceiling)
- Higher pension = higher EPS contribution by employer; retrospective arrears may apply
- System supports both options: employee declares choice; system calculates accordingly

#### UAN Management
- UAN (Universal Account Number): one per employee for lifetime (EPFO-assigned)
- New employee: system checks UAN via EPFO API (if existing employee from previous employer)
- If no UAN: system initiates UAN generation via ECR
- UAN stored against employee; links all EPF accounts across employers

#### ECR (Electronic Challan cum Return)
- Monthly upload to EPFO e-Sewa portal by 15th of next month
- ECR format: UAN, member name, gross wages, EPF wages, EPS wages, EPF contribution, EPS contribution, EDLI contribution, arrears if any
- System generates ECR file automatically from payroll data
- One-click upload to EPFO e-Sewa via API; alert on failure; penalty 12% per annum on late payment
- TRRN (Temporary Return Reference Number) generated on upload; stored against month

### 4.2 ESI (Employee State Insurance) — ESI Act 1948

#### Applicability
- Employees with gross salary ≤ Rs. 21,000/month (Rs. 25,000 for persons with disability)
- Establishments with 10+ employees (in most states; some states: 20+ employees)
- System auto-flags ESI applicability per employee monthly

#### Contribution Rates
| Party | Rate | Basis |
|---|---|---|
| Employee | 0.75% | Gross salary |
| Employer | 3.25% | Gross salary |

#### Threshold Crossing
- Employee's gross exceeds Rs. 21,000 mid-contribution period:
  - April–September contribution period: if gross > Rs. 21,000 in any month, continues till September
  - New period (October) starts: ESI not applicable if gross > Rs. 21,000
- System tracks contribution periods and auto-manages applicability

#### ESI Challan
- Monthly challan to ESIC portal by 21st of next month
- System generates challan; tracks payment; ESIC challan number stored
- IP (Insurance Person) number per employee stored in system
- Maternity benefit via ESIC: employer files claim; ESIC pays 100% daily wages × 26 weeks directly to employee

### 4.3 Professional Tax — State-wise Rule Engine

| State | Rate / Slab | Frequency | Notes |
|---|---|---|---|
| Karnataka | Rs. 200/month (above Rs. 15,000 gross) | Monthly | Fixed; Rs. 2,400/year |
| Maharashtra | Rs. 0–300/month (slab-based by gross) | Monthly | Highest slab Rs. 2,500/year |
| Tamil Nadu | Rs. 135/month (above Rs. 21,000) | Monthly | Rs. 1,620/year |
| Andhra Pradesh | Rs. 0–208/month (slab) | Monthly | Max Rs. 2,500/year |
| Telangana | Rs. 0–208/month (slab) | Monthly | Same as AP |
| West Bengal | Rs. 0–200/month (slab) | Monthly | |
| Gujarat | Rs. 0–200/month (slab) | Monthly | |
| Madhya Pradesh | Rs. 208/month (above Rs. 25,000) | Monthly | |
| Odisha | Rs. 0–250/month (slab) | Monthly | |
| Assam | Rs. 0–208/month (slab) | Monthly | |
| Bihar | Rs. 0–250/month (slab) | Monthly | |
| Jharkhand | Rs. 0–250/month (slab) | Monthly | |
| Meghalaya | Rs. 0–208/month (slab) | Monthly | |
| Sikkim | Rs. 0–250/month (slab) | Monthly | |
| Kerala | Abolished (2023) | — | No PT in Kerala |
| Delhi | No PT | — | |
| Rajasthan | No PT | — | |
| Uttar Pradesh | No PT | — | |
| Haryana | No PT | — | |
| Punjab | No PT | — | |

- System applies correct state PT rule based on institution's state (Module 04)
- Multi-state institution group: each branch taxed per its own state
- PT remittance: monthly/quarterly per state; system generates PT challan in state-specific format
- PT registration certificate per establishment: stored in system; renewed annually in applicable states

### 4.4 Labour Welfare Fund (LWF)
- Applicable states: Maharashtra, Karnataka, Gujarat, AP, Telangana, MP, Tamil Nadu, Punjab, others
- Employer + employee contribution (small amounts: Rs. 6–Rs. 25/employee/year each party)
- Frequency: annual or half-yearly (state-wise)
- System generates LWF challan; tracks payment

### 4.5 TDS on Salary — Section 192

#### Computation Method
- Not a fixed % — computed on estimated annual income basis each month
- Formula: (estimated annual taxable income × applicable slab rate − rebates) / 12 = monthly TDS
- Recomputed every month as salary components change

#### Tax Regime (Employee Declares at April — Financial Year Start)

| Regime | Key Differences |
|---|---|
| Old Regime | HRA exemption, LTA exemption, 80C, 80D, standard deduction Rs. 50,000; higher slab rates |
| New Regime (Default FY25-26 onwards) | No exemptions except standard deduction Rs. 75,000 (FY25-26); lower slab rates; simpler |

- Employee declares choice at April; system calculates TDS accordingly
- Change allowed once mid-year (employee can switch once before March)
- If no declaration: employer defaults to new regime (FY 2024-25 onwards)

#### Investment Declaration Workflow
```
April — Employee submits Form 12BB (projected investments)
System computes estimated annual TDS based on declarations
       │
January — Employee submits actual investment proofs
System recalculates TDS for remaining 3 months (Jan–Mar)
       │
March — Final TDS true-up; arrears deducted or excess adjusted
       │
April (next year) — Form 16 Part B generated
```

#### Section 80C Eligible Investments
- EPF employee contribution, VPF, PPF, LIC premium, NSC, ELSS, home loan principal,
  children's tuition fee (Module 25 fee certificate feeds this), Sukanya Samriddhi, 5-year FD

#### HRA Exemption — Minimum of Three
```
1. Actual HRA received
2. 50% of basic (metro: Delhi/Mumbai/Chennai/Kolkata) or 40% of basic (non-metro)
3. Actual rent paid minus 10% of basic
```
- Landlord PAN mandatory if monthly rent > Rs. 8,333 (Rs. 1 lakh/year)
- System calculates exemption and applies; employee submits rent receipts

#### Section 89 Relief — Arrears
- If DA arrears / pay revision arrears received in current year relating to previous years
- Tax computed: as if income spread across original years
- Difference = Section 89 relief; reduces current year TDS
- Form 10E must be filed by employee on IT portal; system generates calculation

### 4.6 Form 16 Generation
- **Part A**: TDS deducted and deposited (from TRACES after Form 24Q processed)
  - Employer TAN, employee PAN, quarterly TDS summary, total TDS for year
- **Part B**: Salary breakup + deductions (employer-generated)
  - All earnings components, all exemptions, all deductions, net taxable income, tax computed, TDS deducted
- Delivery: by June 15 each year; WhatsApp + in-app + DigiLocker push (TRACES-DigiLocker API)
- Password-protected PDF: password = employee PAN (uppercase)
- Employee can use Form 16 Part B data directly in ITR filing

### 4.7 Form 24Q (TDS Quarterly Return)
- Quarterly TDS return filed with Income Tax Department
- Due dates: Q1 (Apr–Jun) by July 31; Q2 (Jul–Sep) by Oct 31; Q3 (Oct–Dec) by Jan 31; Q4 (Jan–Mar) by May 31
- Format: NSDL/TIN FVU format; system generates 24Q file
- Filed via TRACES portal or authorised intermediary
- Correction: if PAN mismatch or challan error; system generates correction file

### 4.8 TDS Challan (ITNS 281)
- Monthly TDS deposit by 7th of following month (30th April for March)
- Challan: ITNS 281; BSR code + date + challan serial number → entered in 24Q
- System generates challan details; Finance Head deposits via net banking; BAN tracked

---

## 5. Government & Aided Staff Specific

### 5.1 Central DA Revision
- DA revised twice yearly: effective January 1 and July 1
- Based on AICWPI (All India Consumer Price Index for Industrial Workers) 12-month average
- System stores DA revision history table: effective date, % of basic, applicable institution types
- Auto-applies on effective date for all govt / aided staff
- Arrears auto-calculated: difference between old DA and new DA × months from effective date to notification date
- Arrears payment: system creates arrear component in payroll; TDS recalculated; Section 89 relief assessed

### 5.2 Annual Increment
- Government staff: automatic increment on July 1 (moves to next cell in pay matrix)
- No approval needed unless staff is under suspension / adverse entry on increment date
- System auto-applies July 1 increment; HR notified if any employee flagged for withholding
- Increment withholding: only by order of competent authority; documented in system

### 5.3 Stagnation Increment
- Employee reaches maximum cell of their pay level (no further increment possible in same level)
- Every 2 years: 3% additional amount as stagnation increment (not promotion)
- System tracks: date of reaching maximum + 2-year anniversaries; auto-applies

### 5.4 Promotion — Pay Fixation
```
Step 1 — Find employee's current basic pay in current level
Step 2 — Look up next higher level in pay matrix
Step 3 — Find next cell in higher level that is greater than current basic
Step 4 — That becomes the new basic pay
Step 5 — Annual increment date: 6 months from promotion date (for increment purpose)
```
- System performs pay fixation automatically using pay matrix lookup
- Finance Head reviews and approves before activation

### 5.5 MACP (Modified Assured Career Progression)
- If promotion not received in 10 years from joining (or last promotion): financial upgrade to next level
- If again not received in 20 years: second MACP
- If again not received in 30 years: third MACP
- System tracks service years; alerts Finance Head at 9 years / 19 years / 29 years for preparation
- MACP is financial upgrade only (pay fixation as promotion); actual designation unchanged

### 5.6 Pay Anomaly Detection
- After pay revision / increment cycle: junior employee's pay may exceed senior's
- System scans for anomalies: employee in lower grade earning more than same-grade senior
- Flags to Finance Head; resolution requires appropriate government order / management decision

### 5.7 Aided Staff Grant Tracking
- State government releases salary grant per approved aided post
- Grant may be delayed by months (common in AP, Telangana, Maharashtra, UP)
- System tracks: grant expected (based on approved posts × monthly salary) vs grant released
- Gap = institution bridges from own funds (interest-free internal advance)
- When grant arrives: internal advance recovered; aided staff account reconciled
- Aided post count: system enforces sanctioned strength; cannot process payroll for more than approved aided posts

### 5.8 Deputed Staff Payroll
- Deputed employee: home institution pays salary; host institution reimburses
- Deputation allowance: additional % of basic (varies: 5–10%) paid for deputation period
- System generates: salary in home institution payroll + deduction request to host institution
- Host institution approves and transfers amount to home institution; tracked

---

## 6. Payroll Types & Staff Categories

### 6.1 Monthly Payroll Types
| Type | EPF | ESI | TDS | Payslip |
|---|---|---|---|---|
| Regular teaching (confirmed) | ✅ | If ≤ Rs. 21,000 | ✅ | ✅ |
| Regular non-teaching (confirmed) | ✅ | If ≤ Rs. 21,000 | ✅ | ✅ |
| Probationary staff | ✅ | If ≤ Rs. 21,000 | ✅ | ✅ |
| Contract (fixed-term) | ✅ | If ≤ Rs. 21,000 | ✅ | ✅ |
| Part-time (regular engagement) | ✅ (if monthly wage ≥ Rs. 15,000 notional) | Check | ✅ | ✅ |
| Guest / Visiting faculty (monthly) | May be exempt (check contract type) | Check | Section 194J if contract | ✅ |
| Daily wage workers | EPF if monthly ≥ Rs. 15,000 | Check | Rarely applicable | ✅ |
| Casual / temporary | EPF after 3 months continuous | Check | Only if above threshold | ✅ |

### 6.2 Guest Faculty — TDS Complication
- If guest faculty engaged as "employee": TDS Section 192 (salary); EPF applicable
- If guest faculty engaged as "professional": TDS Section 194J (10% if annual payment > Rs. 30,000); NO EPF
- Determination: control test (does institution control how work is done?) → if yes = employee
- Misclassification risk: EPF department can reclassify contractors as employees; demand arrears + penalty
- System flags: if same guest faculty paid for 3+ consecutive months → Finance Head to review classification

### 6.3 Daily Wage Workers
- Rate per day × days worked (calendar / working days — institution configures)
- EPF: if monthly wage crosses Rs. 15,000 → EPF applicable
- ESI: if monthly gross ≤ Rs. 21,000 → ESI applicable
- Minimum wages: checked per state applicable category (unskilled/semi-skilled/skilled)
- Weekly day-off: mandatory (Factories Act / Shops Act); if worked on weekly off → double wages

### 6.4 Retired Re-employed Staff
- Receiving pension from EPFO/state government + salary from institution
- Combined income: pension + salary = total income for TDS
- TDS: institution deducts on salary portion; employee submits pension details in Form 12BB
- EPF on re-employed: voluntary; EPF not mandatory if employee is drawing EPS pension
- Gratuity: new gratuity cycle starts from re-employment date (separate from original service)

### 6.5 NRI Staff
- Foreign national working in India: India-source salary fully taxable in India
- TDS at applicable slab rate (or 30% if non-resident and treaty not applicable)
- DTAA (Double Taxation Avoidance Agreement): if employee's home country has DTAA with India; Form 10F + Tax Residency Certificate required; TDS at DTAA rate
- Salary remittance abroad: FEMA compliance; Form 15CA + 15CB for remittance > Rs. 5 lakh/year
- EPF: International Workers EPF — applicable if from non-social security agreement country; exempt if from SSA country (Germany, Japan, Korea, etc.)

---

## 7. Attendance-Linked Payroll

### 7.1 LWP (Leave Without Pay) Calculation
- Attendance data from Module 08 daily feed to payroll
- Basis: institution configures — calendar days (÷30) OR paid days (÷26)
- LWP deduction = (gross salary / basis days) × LWP days
- Late arrival policy: accumulated late marks → LWP (e.g., 3 lates = 1 LWP day); configurable

### 7.2 Leave Types & Payroll Impact
| Leave Type | Pay Impact | Notes |
|---|---|---|
| CL (Casual Leave) | Full pay | Not carried forward; lapses at year end |
| EL/PL (Earned/Privileged Leave) | Full pay | Carried forward; encashed on exit |
| ML/SL (Medical/Sick Leave) | Full pay (limited days) | Medical certificate required |
| Maternity Leave | Full pay (26 weeks) | Maternity Benefit Act 1961; 12 weeks for 3rd child |
| Paternity Leave | Full pay (institution policy) | No central statute for private institutions |
| CCL (Child Care Leave) | Full pay | Central govt: 730 days lifetime for women; state-wise |
| Study Leave | Half pay / full pay | College: UGC rules; institution configures |
| Sabbatical | Varies | College professors; half pay or full pay per UGC |
| EOL (Extra Ordinary Leave) | LWP | Approved absence; no pay |
| Unauthorized Absence | LWP + possible disciplinary | Finance Head alert |

### 7.3 Overtime Computation
- Applicable: non-teaching staff, support staff
- Rate: basic / 26 × 2 per OT hour (overtime = double rate per Factories Act)
- Teaching staff OT: legally complex; generally not applicable; extra class = duty; coaching institutes may pay extra session allowance (different from OT)
- OT approval: supervisor approval mandatory before OT; retroactive OT claims flagged

### 7.4 Compensatory Off
- Staff worked on declared holiday or weekly off day
- CO credit: 1 day CO per day worked on holiday
- CO register: maintained in system; CO utilised within 30 days (configurable)
- Lapsed CO: after 30 days if not taken; no cash equivalent for regular staff
- Daily wage staff: no CO system; extra payment directly

### 7.5 Maternity Leave — Deep Compliance
- Maternity Benefit Act 1961 (as amended 2017)
- 26 weeks full pay for first 2 children (12 weeks pre-delivery + 14 weeks post)
- 12 weeks for 3rd child and beyond
- 26 weeks for adoption of child below 3 months (adoptive mother)
- 6 weeks commissioning mother (surrogacy)
- No ESI contribution during maternity leave (leave pay continues but no ESI)
- If under ESI: ESIC pays maternity benefit directly to employee; institution does NOT pay during ESI maternity period (ESIC substitutes)
- If not under ESI (salary > Rs. 21,000): institution pays full salary
- System tracks: maternity leave start, expected delivery date, return date; payroll auto-adjusts

---

## 8. NPS & GPF (Government Pension Schemes)

### 8.1 NPS (National Pension System)
- Mandatory for: central government employees joining after Jan 1, 2004; most state government employees (varies by state)
- Private institutions: NPS is optional but increasingly offered as retirement benefit

#### Contribution Rates
| Party | Rate | From FY |
|---|---|---|
| Employee | 10% of basic + DA | Mandatory |
| Central Govt Employer | 14% of basic + DA | Enhanced from 10% in 2019 |
| State Govt Employer | 10% or 14% | Varies by state |
| Private Institution | Voluntary; institution configures | — |

#### PRAN Management
- PRAN (Permanent Retirement Account Number): unique per employee; issued by NSDL/KFintech
- New employee: PRAN opened via institution (if first job) or ported from previous employer
- System stores PRAN; used in CRA upload

#### CRA Monthly Upload
- NCIS (NPS Contribution Instruction Slip) generated monthly
- Uploaded to CRA (NSDL / KFintech) by last working day of month
- Acknowledgement number stored; contribution credited to employee's NPS account
- System generates NCIS file in prescribed format; Finance Head reviews and uploads

#### NPS Tier I & II
- Tier I (pension account): mandatory; lock-in till age 60; partial withdrawal allowed (after 3 years: up to 25% for specific purposes)
- Tier II (savings account): optional; no lock-in; freely withdrawable
- Both tracked in system; monthly deduction for both if employee enrolled in Tier II

### 8.2 GPF (General Provident Fund) — OPS Employees
- For government employees on Old Pension Scheme (OPS)
- Minimum contribution: 6% of basic + DA; no maximum
- No employer contribution (unlike EPF)
- Interest rate: notified by government annually (currently ~7.1%)
- Withdrawal rules: different from EPF; advance allowed for specific purposes (marriage, education, medical)
- System maintains GPF passbook: opening balance + contributions + interest + withdrawals = closing balance
- GPF maturity: on retirement; final settlement + interest

### 8.3 OPS vs NPS
| Feature | Old Pension Scheme (OPS) | New Pension System (NPS) |
|---|---|---|
| Pension amount | 50% of last basic (defined benefit) | Market-linked (defined contribution) |
| Employer contribution | Nil (funded by government) | 10–14% of basic+DA |
| Employee contribution | GPF (not toward pension) | 10% of basic+DA |
| Certainty | High (guaranteed pension) | Variable (market returns) |
| Portability | No | Yes (UAN/PRAN portable) |

- Political issue: multiple states reverting to OPS (Rajasthan, Himachal Pradesh, Jharkhand, Chhattisgarh, Punjab)
- System supports both; employee tagged with scheme type; payroll processes accordingly

---

## 9. Gratuity

### 9.1 Eligibility
- 5 years continuous service (Payment of Gratuity Act 1972)
- Exceptions: death, permanent disability (eligible regardless of years of service)
- Part-time staff: courts have held part-time employees also eligible (if continuous engagement)
- System tracks service years; flags approaching 5-year mark 3 months before

### 9.2 Gratuity Formula
```
Gratuity = (Last drawn basic + DA) × 15 / 26 × completed years of service
```
- Rounding: service > 6 months in last year = rounded up to next year
- Examples: 7 years 7 months = 8 years; 7 years 5 months = 7 years
- Ceiling: Rs. 20 lakh (2018 amendment; government employees: no ceiling)

### 9.3 Tax Treatment
| Category | Exemption |
|---|---|
| Government employee | Fully exempt (no ceiling) |
| Non-government employee (Gratuity Act covered) | Min of: actual gratuity OR Rs. 20 lakh OR 15 days salary × years |
| Non-government employee (not covered) | Min of: actual gratuity OR Rs. 20 lakh OR half month salary × years |

- Balance above exempt = taxable; included in F&F TDS computation

### 9.4 Gratuity Provision (Monthly Accrual)
- Accounting: institution accrues gratuity liability monthly (not just on payment)
- Simplified accrual: 4.81% of (basic + DA) per employee per month
  (derived: 15/26 × 1 year = 57.69% of monthly salary × 1/12 ≈ 4.81%)
- Journal entry: Dr Gratuity Expense (P&L) → Cr Gratuity Provision (Balance Sheet liability)
- System generates monthly provision entry; Finance Head reviews quarterly
- Actuarial valuation: recommended by CA for AS 15 (Revised) compliance; discount rate from IRDAI notified rates; system supports actuarial inputs

### 9.5 Group Gratuity Scheme
- Institution takes group gratuity policy from LIC / private insurer
- Annual premium paid to insurer; insurer covers gratuity liability
- On employee exit: institution claims from insurer; insurer pays to institution; institution pays employee
- System tracks: policy number, insurer, premium paid, claims raised, claims received

### 9.6 Gratuity Forfeiture
| Reason | Forfeiture |
|---|---|
| Termination for misconduct causing financial loss | Up to amount of loss (partial forfeiture) |
| Termination for violence/riot/offence | Full forfeiture |
| POCSO conviction or criminal conviction | Full forfeiture |
| Voluntary resignation | NOT forfeitable (must pay full gratuity if 5 years served) |

- System flags gratuity forfeiture only when management explicitly records forfeiture order with reason

---

## 10. Full & Final Settlement

### 10.1 F&F Triggers
- Resignation (accepted)
- Retirement (superannuation)
- Termination / dismissal
- Fixed-term contract end (not renewed)
- Death in service (payable to nominee)
- Abandonment (absent > 8 continuous days without intimation; deemed resignation after notice period)

### 10.2 F&F Components
```
(+) Salary for days worked in last month (pro-rata)
(+) Leave encashment — EL/PL balance × (basic + DA) / 26
(+) Gratuity — if ≥ 5 years service
(+) Pro-rata bonus — if Bonus Act applicable (salary ≤ Rs. 21,000)
(+) LTA encashment — if pending LTA block not claimed
(+) Arrears — any pending arrears
(+) Notice pay — if institution waives notice period
(−) Notice period recovery — if not served (net salary for unserved days)
(−) Salary advance recovery — outstanding advance balance
(−) Vehicle/housing loan recovery — outstanding EMI × remaining months
(−) Cooperative society loan recovery — as per society instruction
(−) Ward fee dues recovery — from Module 26 outstanding
(−) TDS on F&F — computed on all taxable components
───────────────────────────────────────────────────────
= Net F&F payable (or recoverable from employee if deductions > earnings)
```

### 10.3 Leave Encashment Tax Treatment
| Scenario | Tax Treatment |
|---|---|
| Government employee — retirement | Exempt up to Rs. 25 lakh (7th CPC enhanced; FY 2023-24) |
| Non-government employee — retirement | Exempt: min(actual encashment, Rs. 3 lakh, 10 months' salary) |
| Any employee — resignation | Fully taxable (no exemption on resignation) |

### 10.4 No-Dues Clearance for F&F
```
Library clearance (Module 30) — books returned
IT assets returned — laptop, phone, projector
Lab equipment returned (college) — lab in-charge sign-off
Ward fee dues cleared (Module 26) — or deducted from F&F with employee consent
Housing colony vacated (if institution housing provided)
Module 39 — no-dues certificate generated
       │
F&F processing unlocked
```

### 10.5 F&F Payment Timeline
- Industry standard: 30–45 days from last working day
- Payment of Wages Act: if applicable, wages must be paid within 2 working days of removal / 7 days of resignation
- System tracks F&F due date; alerts Finance Head
- Delay: employee can approach Labour Commissioner; system log serves as evidence

### 10.6 Relieving Letter & Experience Certificate
- Relieving letter: issued on last working day (or within 3 days); system generates from Module 08 data
- Experience certificate: issued after F&F completion; Module 39 trigger
- Both in-app delivery; shareable link; NOT PDF (platform policy — employee screenshots or uses link)

---

## 11. Salary Bank Transfer

### 11.1 Bank Account Management
- One active salary account per employee (IFSC + account number + bank + branch)
- Account change: employee request → HR verification → Finance Head approval → 2-month parallel notification before switch
- Wrong account alert: NEFT return triggers immediate alert; correction within 24 hours

### 11.2 Bulk NEFT File Generation
- Bank-specific formats:
  - SBI: CINB / YONO Batch Payment format (text / CSV)
  - HDFC: NetBanking bulk upload (Excel)
  - Axis: Bulk payment (CSV with specific headers)
  - Kotak: NetBanking (CSV)
  - ICICI: CIB bulk upload (Excel)
- System generates correct format per institution's banker
- File: institution account, date, employee account, IFSC, amount, reference (employee ID + month)
- Finance Head downloads file; uploads to bank NetBanking; bank processes batch transfer

### 11.3 Salary Transfer Date
- Configurable: 1st / 5th / 7th / last working day of month
- Weekday logic: if configured date falls on Sunday/holiday → Friday before OR Monday after (institution configures)
- Public sector teaching staff: typically last working day of month
- Private institutions: typically 1st–5th of next month

### 11.4 Salary on Hold — Suspension
- Employee under suspension: salary withheld; subsistence allowance paid
- Central govt rules (applicable to govt-aided institutions):
  - First 90 days suspension: 50% of basic + DA as subsistence allowance
  - After 90 days (if not employee's fault): 75% of basic + DA
  - After 90 days (if employee's fault): 25% of basic + DA
- Private institution: own policy (document clearly to avoid labour dispute)
- System handles: salary → HOLD; subsistence allowance computation and payment

### 11.5 Court Attachment of Salary
- Court order attaching portion of employee's salary (matrimonial disputes, debt recovery)
- Maximum attachable: salary above Rs. 1,000 or 1/3 of net salary (whichever is lower, per CPC Order XXI Rule 33)
- System: deducts attached amount monthly; remits to court registry; issues deduction certificate to employee
- Attachment order stored; released when court orders

### 11.6 Salary Advance
- Employee requests advance: up to 2 months net salary (configurable)
- Finance Head approval; documented
- Recovery: equal deductions over 1–3 months payroll
- Maximum outstanding advance: 1 advance at a time (configurable)
- Festival advance: separate category; larger amount allowed; recovered over 3–6 months

---

## 12. Payslip Generation & Delivery

### 12.1 Payslip Components
**Earnings section:**
- All earnings components with amount per component

**Deductions section:**
- EPF employee, ESI employee, Professional Tax, TDS, LWF, loan EMI, advance recovery, other deductions

**Summary:**
- Gross earnings, total deductions, net pay (in figures and words)

**Employer contribution (shown separately; not deducted):**
- Employer EPF (3.67%), Employer EPS (8.33%), Employer EDLI (0.5%), Employer EPF admin (0.5%), Employer ESI (3.25%), Gratuity provision (4.81%)
- Shown for transparency; CTC reconciliation

**Employee information:**
- Name, employee ID, designation, department, branch, PAN (masked), EPF UAN, ESI IP number, bank account (last 4 digits), month-year, days in month, days worked, LWP days, OT hours (if any)

### 12.2 PDF Payslip
- WeasyPrint generation; password-protected
- Password: employee's date of birth (DDMMYYYY format) — standard industry practice
- Stored on Cloudflare R2: `{tenant_id}/payroll/{employee_id}/{YYYY-MM}.pdf`
- Download link valid 7 days (regenerated on each access)
- 7-year retention on R2 with immutable flag

### 12.3 Delivery
- WhatsApp: password-protected PDF + message: "Payslip for [Month YYYY] — Password: your DOB (DDMMYYYY)"
- In-app: downloadable from "My Payslips" section; past 24 months available directly; older on request
- Email: optional; parent preference setting

### 12.4 Payslip Dispute Workflow
```
Employee disputes component (in-app dispute ticket)
       │
HR / Accountant reviews (48-hour SLA)
       │
       ├── Error found → Correction in next month's payroll (with arrear) OR revised payslip
       │
       └── No error → Explanation provided to employee; dispute closed
```
- Dispute does NOT hold salary payment (salary released on schedule; correction in next cycle)

### 12.5 Income Tax Computation View (In-App)
- Employee sees running tax calculation each month:
  - Estimated annual gross income
  - Exemptions applied (HRA, LTA, standard deduction)
  - Deductions declared (80C, 80D, etc.)
  - Net taxable income
  - Tax computed (slab-wise)
  - TDS deducted to date
  - Balance TDS to be deducted in remaining months
- Helps employee plan investments before March deadline

---

## 13. Annual Statutory Filings

### 13.1 EPF Annual Returns
| Form | Content | Due Date |
|---|---|---|
| Form 3A | Annual member-wise contribution statement | April 30 |
| Form 6A | Annual consolidated statement of all members | April 30 |

### 13.2 ESIC Annual Return
- Annual return: total wages paid, ESI contributions, headcount
- State-wise return formats
- Due: April 30 for previous year

### 13.3 Professional Tax Annual Return
- State-wise annual returns
- Karnataka: Form 9 (employer); Maharashtra: Form III (annual); AP/TS: Form V; varies per state
- System generates state-specific format

### 13.4 Payment of Bonus Act
| Form | Content |
|---|---|
| Form A | Allocation of bonus (surplus computation) |
| Form B | Set-on and set-off of allocable surplus |
| Form C | Bonus paid to each employee |
| Form D | Annual return of bonus |
- Applicable: establishments with 20+ employees (10+ in some states)
- Salary threshold: employees earning up to Rs. 21,000/month gross are eligible
- Minimum bonus: 8.33% of annual salary (even if no profit)
- Maximum: 20% of annual salary
- System computes allocable surplus; generates all Bonus Act forms

### 13.5 Labour Welfare Fund Annual Return
- State-specific; system generates

---

## 14. Statutory Registers

### 14.1 Form B — Register of Wages
- Payment of Wages Act / Minimum Wages Act
- Per employee per month: name, designation, days worked, wages earned, deductions, net paid, signature
- System generates Form B in prescribed format; available for labour inspector on demand
- Maintained per establishment (branch-wise)

### 14.2 Form D — Register of Deductions
- All deductions from wages listed with reason (EPF, ESI, loan, absence, etc.)
- System generates automatically from payroll data

### 14.3 Minimum Wages Compliance
- Payment of Minimum Wages Act: state-wise minimum wages per skill category
- Categories: Unskilled, Semi-skilled, Skilled, Highly Skilled; construction, commercial establishment, etc.
- System checks each employee's gross against applicable minimum wage
- Alert: if any employee's gross falls below applicable minimum wage → Finance Head alert before payroll approval

### 14.4 Leave Register
- Per employee per year: opening balance per leave type, leaves taken month-wise, closing balance
- Module 08 feeds leave data to payroll

### 14.5 Overtime Register
- OT hours per employee per month; approval record; rate; amount paid
- Labour inspector commonly checks OT register

---

## 15. Payroll Approval Workflow

### 15.1 Monthly Payroll Process
```
Step 1 — Attendance data locked in Module 08 (by HR by 25th of month)
       │
Step 2 — Payroll engine computes: LWP deductions, OT, all earnings, all deductions, net pay
       │
Step 3 — Variance check: current month vs previous month
         Flag: any employee variance > 5% (salary component change, LWP excess, etc.)
         Flag: total payroll variance > 2% (unusual)
       │
Step 4 — Accountant reviews variance flags; resolves or accepts with reason
       │
Step 5 — Finance Head reviews payroll summary + flagged items; approves
       │
Step 6 — Principal / Management final approval (above threshold amounts)
       │
Step 7 — Payroll locked: no changes after lock
       │
Step 8 — Bank transfer file generated; uploaded to bank
       │
Step 9 — Payslips generated and delivered (WhatsApp + in-app)
       │
Step 10 — Statutory challans generated (EPF ECR, ESI, PT, TDS ITNS 281)
```

### 15.2 Ghost Employee Detection
- Employee in system, salary being processed, but attendance = 0 for 30+ consecutive days
- System flags: "Employee [name] has zero attendance for 30 days but salary is being processed"
- HR investigation triggered; do NOT auto-stop salary (wrongful stoppage = labour dispute)
- Finance Head must explicitly hold salary after investigation

### 15.3 Duplicate Bank Account Detection
- System checks: if two or more employees share the same bank account number
- Flag: "Duplicate bank account detected — [Employee A] and [Employee B] share account XXXX"
- Potential ghost employee / payroll fraud signal; Finance Head investigation mandatory

---

## 16. Access Control

### 16.1 Role-Wise Permissions
| Action | HR / Admin | Accountant | Principal | Finance Head | Management | Employee (Self) |
|---|---|---|---|---|---|---|
| View own payslip | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| View all payslips | ❌ | ✅ (process) | ✅ (read) | ✅ | ✅ | ❌ |
| Create salary structure | ✅ (draft) | ✅ (draft) | ❌ | ✅ (approve) | ✅ (approve) | ❌ |
| Process monthly payroll | ❌ | ✅ | ❌ | Approve | Final approve | ❌ |
| Lock payroll | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ |
| Generate bank transfer file | ❌ | ✅ | ❌ | ✅ | ❌ | ❌ |
| Hold salary (suspension) | ❌ | ❌ | Recommend | ✅ | ✅ | ❌ |
| Process F&F | ❌ | Compute | Approve | Final approve | Final approve | ❌ |
| View EPF / ESI reports | ❌ | ✅ | ❌ | ✅ | ❌ | ✅ (own) |
| Generate Form 16 | ❌ | ✅ | ❌ | ✅ | ❌ | ✅ (own) |
| Export payroll data | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ |
| View payroll audit log | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ |

---

## 17. Reports & MIS

### 17.1 Monthly Reports
| Report | Audience | Content |
|---|---|---|
| Payroll Summary | Finance Head, Management | Total wages; head-wise; branch-wise; CTC vs gross vs net |
| Statutory Liability Report | Finance Head, CA | EPF payable, ESI payable, PT payable, TDS payable, LWF payable |
| Variance Report | Finance Head | Employee-wise current vs previous month; explanation for flags |
| LWP Deduction Report | HR, Finance Head | Employees with LWP; days deducted; amount deducted |
| OT Report | HR, Finance Head | OT hours, approved by, amount paid |
| Ghost Employee Flag Report | Finance Head, Principal | Employees with zero attendance but salary processed |

### 17.2 Quarterly / Annual Reports
| Report | Audience | Content |
|---|---|---|
| Form 24Q | Finance Head, CA | TDS quarterly return data; ready for NSDL upload |
| EPF Annual (Form 3A / 6A) | Finance Head | Member-wise annual contribution |
| Bonus Act Returns (Form A–D) | Finance Head, CA | Allocable surplus, bonus paid |
| PT Annual Return | Finance Head | State-wise professional tax return |
| Labour Welfare Fund Return | Finance Head | LWF annual return |
| Gratuity Provision Statement | Finance Head, CA | Provision balance, movement, actuarial note |
| Salary Cost Analysis | Management | Payroll cost as % of fee revenue; trend; branch-wise |
| Increment Due Report | HR, Principal | Staff due for increment / MACP in next 3 months |

### 17.3 Employee Self-Service Reports (In-App)
- Payslips: last 24 months
- Form 16: last 3 years
- EPF passbook (estimated balance from system; actual on EPFO portal)
- NPS statement
- Leave balance
- Loan balance + repayment schedule
- Income tax computation (running)
- Investment declaration status

---

## 18. Audit Trail & Retention

### 18.1 Immutable Payroll Log
- Every change to salary structure, component, deduction, tax regime, bank account
- Log fields: field_changed, old_value, new_value, changed_by, changed_at, reason
- No log entry editable by any role

### 18.2 7-Year Retention
- Payslips, payroll registers (Form B, Form D), TDS challans, Form 16, Form 24Q,
  EPF ECR files, ESI challans, F&F settlements: all stored on Cloudflare R2 with immutable flag
- Labour law requirement: 3–5 years depending on act; system retains 7 years to be safe

### 18.3 CA / Auditor Access
- Read-only; specific to: payroll registers, statutory challans, Form 16, Form 24Q, F&F register, gratuity provision
- No access to individual employee communication or leave correspondence

---

## 19. Architect's Strategic Recommendations

### 19.1 Automated Form 24Q E-Filing (High ROI)
Most institutions pay CA/consultant Rs. 5,000–20,000 per quarter to prepare and file Form 24Q.
System generates 24Q in NSDL FVU format directly from payroll data. One-click upload to TRACES
portal via API. Zero consultant dependency. At 10,000 institutions on platform: Rs. 200 crore/year
in aggregate consultant cost saved across the EduForge ecosystem. This single feature drives
Finance Head adoption and platform stickiness.

### 19.2 EPF ECR + ESIC Auto-Upload (Compliance Automation)
ECR and ESIC challan are currently the most error-prone monthly compliance tasks in Indian
payroll. Wrong ECR format, wrong UAN, mismatched amounts → EPFO sends notices → institution
panics → CA called → Rs. 5,000–10,000 per incident. System generates ECR from payroll data
(zero human intervention) and uploads to EPFO e-Sewa via API. Same for ESIC. Penalty for
late EPF payment: 12% per annum. Penalty for missed ESIC: Rs. 5,000 + 12%. Auto-upload
with alert on failure eliminates this risk entirely.

### 19.3 DigiLocker Form 16 Delivery (Employee Delight)
CBDT has enabled employer → employee Form 16 delivery via DigiLocker (TRACES-DigiLocker API).
Employee gets Form 16 directly in their DigiLocker; automatically pre-populates in ClearTax,
Quicko, IT portal for ITR filing. No WhatsApp, no email, no password. EduForge should implement
TRACES-DigiLocker push for all institutions. Employee perception: "This platform takes care of my taxes."
Teacher retention signal: good payroll experience → lower attrition.

### 19.4 Professional Tax Rule Engine — 28-State Automation
Professional Tax is the single most ignored compliance in Indian payroll. Most institutions
either don't deduct it (non-compliance risk) or deduct wrong amount (liability risk). 28 states,
different slabs, different return formats, different payment portals. System maintains a
live PT rule engine updated whenever any state revises PT slabs. Finance Head never calculates
PT manually. Multi-state institution groups (like DPS, Narayana, Sri Chaitanya) especially benefit:
one Finance Head managing PT across Karnataka, AP, Telangana, Maharashtra simultaneously.

### 19.5 Teacher Retention Analytics (Payroll + Attendance + Resignation)
High teacher attrition is the #1 operational risk for schools and coaching institutes.
Combine payroll data + attendance trend + years since last increment + market salary benchmarks
(anonymized platform data) → compute retention risk score per teacher.
Flag: "Physics teacher X has not received increment in 3 years; attendance declining; peer at
similar institution earns 25% more." Finance Head + Principal can act before resignation.
Expected impact: 20–30% reduction in unexpected mid-year teacher departures. Coaching institutes
(where star faculty = revenue) benefit most.

### 19.6 One-Click ITR Readiness for Employees
Every March, employees flood HR with: "What is my Form 16 status? Can you give me salary breakup?
What is total 80C deduction from salary?" System should auto-generate for each employee:
- Form 12BB (investment declaration summary)
- Salary income summary in ITR-ready format
- Total TDS deducted for the year
- Downloadable XML pre-filled for ITR upload
Employee does not need a CA for salary income ITR filing. This feature makes EduForge the most
employee-friendly payroll platform in Indian education — a differentiator in recruitment marketing
("Staff welfare: EduForge makes your taxes easy").

### 19.7 Payroll Cost as Platform Health Signal
Payroll cost as % of fee revenue is the single most important financial health metric of an
institution. Healthy range: 50–60% (school), 45–55% (college), 35–45% (coaching).
Above threshold = institution is financially stressed → risk of salary delays → staff attrition →
institutional quality decline. EduForge Platform Analytics (Module 53) should track this metric
per institution, per district, per institution type. Institutions trending above threshold for
3+ months → Customer Success proactive outreach (fee collection problem? over-staffing?).
This is both a platform health signal and a sales opportunity (Module 27 advisory services).
