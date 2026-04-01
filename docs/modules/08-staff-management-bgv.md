# EduForge — Module 08: Staff Management & BGV

> Every staff member on EduForge has a complete, verified profile from day one.
> Indian national standards — CBSE teacher qualifications, UGC pay scales, EPF, ESI,
> TDS, POCSO clearance, police verification — all enforced at the platform level.

---

## Staff Types

| # | Type | Description | Examples |
|---|---|---|---|
| 1 | Teaching — Regular | Full-time permanent teacher | Subject teacher, class teacher |
| 2 | Teaching — Senior | Experienced with additional duties | Senior teacher, HOD |
| 3 | Teaching — Probationary | New staff within probation period | Newly joined teacher |
| 4 | Teaching — Contract | Fixed-term contract | Annual contract teacher |
| 5 | Teaching — Part-time | Teaches select periods only | Part-time music, sports teacher |
| 6 | Teaching — Guest Faculty | External expert for specific sessions | Industry expert, alumni |
| 7 | Teaching — Visiting | Assigned to multiple branches | Covers multiple campuses |
| 8 | Non-Teaching — Admin | Administrative functions | Clerk, office assistant |
| 9 | Non-Teaching — Academic Support | Lab, library, IT support | Lab assistant, librarian |
| 10 | Non-Teaching — Finance | Fee, accounts | Accountant, fee clerk |
| 11 | Support Staff | Infrastructure, security, transport | Guard, driver, cook, housekeeping |
| 12 | Management Staff | Senior leadership | Principal, Vice Principal, HOD |
| 13 | Aided Staff | Government-funded salary position | Aided school teachers |
| 14 | Unaided Staff | Institution-funded salary position | Private school teachers |
| 15 | Deputed Staff | Sent from another institution temporarily | Govt deputation |

---

## Staff Onboarding Process

```
Step 1 — Recruitment approval
  Position approved by Management
  Interview panel formed — existing senior staff included

Step 2 — Documents collected
  Qualification certificates, Aadhaar, PAN, photos, experience letters

Step 3 — BGV initiated
  Identity, address, education, employment, POCSO, police verification

Step 4 — Admin creates staff profile
  Employee ID auto-generated
  Designation, department, employment type assigned

Step 5 — Joining report submitted
  Formal joining report on Day 1 — Indian govt standard

Step 6 — Code of conduct + NDA signed
  Stored in system — timestamped

Step 7 — Staff background check consent taken
  DPDPA 2023 compliant

Step 8 — IT assets assigned
  Laptop, phone, projector remote — logged in asset management

Step 9 — Institutional email created
  format: firstname.lastname@institution.edu.in

Step 10 — Login credentials delivered via email

Step 11 — Timetable + subject + class assignment
  Admin configures — Principal approves

Step 12 — Appointment letter generated
  Python auto-generates — signed by Principal
```

---

## Employee ID — Indian Standard Format

| Item | Details |
|---|---|
| Format | Institution Code + Department Code + Sequence Number |
| Example | DPS001-MATH-0012 |
| Auto-generated | System generates on profile creation |
| Used in | Salary slip, ID card, attendance, all records |
| Immutable | Cannot change after first salary processed |

---

## Staff Profile — Complete Data Fields

### Personal Information

| Field | Required | Notes |
|---|---|---|
| Full name (as per Aadhaar) | Mandatory | Legal name |
| Date of birth | Mandatory | Age verification + retirement tracking |
| Gender | Mandatory | Male / Female / Other |
| Nationality | Mandatory | Indian / Foreign national |
| Religion | Optional | For minority institution tracking |
| Mother tongue | Optional | |
| Blood group | Mandatory | Medical emergency |
| Marital status | Optional | For insurance, dependent tracking |
| Aadhaar number | Mandatory | Encrypted — TDS, PF, ESI |
| PAN number | Mandatory | TDS deduction |
| Passport number | If foreign national | |
| Work permit / Visa | If foreign national | Type, expiry — system alert before expiry |

### Address Details

| Field | Required | Notes |
|---|---|---|
| Permanent address | Mandatory | As per Aadhaar |
| Current / correspondence address | Mandatory | For HR correspondence |
| City, district, state, PIN | Mandatory | |
| HRA city category | Auto-derived | Metro / Tier-2 / Other — affects HRA slab |

### Contact Information

| Field | Required | Notes |
|---|---|---|
| Personal mobile | Mandatory | Primary contact |
| Personal email | Mandatory | For HR communication |
| Institutional email | Auto-generated | @institution.edu.in |
| WhatsApp number | Optional | For institutional communication |

### Disability / Special Needs

| Field | Options | Notes |
|---|---|---|
| Differently abled | Yes / No | |
| Disability type | Visual / Hearing / Locomotor / Intellectual | |
| Accommodation needed | Modified workstation, ramp access, etc. | |
| Disability certificate number | Govt issued | |

---

## Staff Qualifications

### Academic Qualifications

| Field | Details |
|---|---|
| Degree name | B.A., B.Sc., B.Tech, M.A., M.Sc., M.Tech, PhD, etc. |
| Specialization | Subject / stream |
| University | Name of university |
| Year of passing | |
| Percentage / CGPA | |
| Certificate number | For BGV verification |

### Teaching Qualifications — Indian Standard

| Qualification | Required For | Standard |
|---|---|---|
| B.Ed | Secondary / Senior secondary teacher | NCTE norm |
| D.El.Ed | Primary school teacher | NCTE norm |
| TET (State) | State board school teacher | State government |
| CTET | CBSE school teacher | CBSE / Central govt |
| NET | College lecturer | UGC norm |
| SET | College lecturer (state) | State UGC |
| PhD | College assistant professor | UGC minimum standard |

- System flags if teacher assigned to class without required qualification
- Warning shown to admin — Principal must acknowledge

### Subject Specialization

| Item | Details |
|---|---|
| Primary subject | Main subject qualified to teach |
| Secondary subjects | Additional subjects can teach |
| Class range | Classes eligible to teach (e.g. Classes 9–12) |
| Subject combination | Multi-subject teacher in primary school |
| Board qualification | CBSE / ICSE / State Board — may differ |

### Teaching Experience

| Item | Details |
|---|---|
| Total experience | Years |
| Previous institutions | Name, designation, duration, leaving reason |
| Experience certificate | Verified during BGV |
| In-service experience | Counts from date of joining current institution |

### State Education Authority Registration

| Item | Details |
|---|---|
| Applicable to | Some states mandate teacher registration |
| States | Andhra Pradesh, Telangana, Tamil Nadu, Kerala, etc. |
| Registration number | Admin enters — system tracks expiry |
| Renewal alert | 30 days before expiry |

---

## Employment Details

| Field | Options | Notes |
|---|---|---|
| Employment type | Permanent / Temporary / Contract / Probation / Part-time / Guest | |
| Aided / Unaided | Aided (govt funded) / Unaided (institution funded) | |
| Date of joining | | |
| Date of confirmation | After probation cleared | |
| Probation period | 6 months / 1 year — institution defines | |
| Retirement date | Auto-calculated from DOB | |
| Mandatory retirement age | 58 / 60 / 62 — per state / institution type | |

### Designation Hierarchy

```
Support Staff
    ↓
Teacher / Clerk / Lab Assistant / Librarian
    ↓
Senior Teacher / Senior Clerk
    ↓
Head of Department (HOD)
    ↓
Vice Principal / Dean
    ↓
Principal / Director
    ↓
Management (Chairman / CEO / MD)
```

---

## BGV — Background Verification

### BGV Components

| # | Component | Mandatory | Method |
|---|---|---|---|
| 1 | Identity verification | Mandatory | Aadhaar + PAN cross-check |
| 2 | Address verification — current | Mandatory | Physical / digital verification |
| 3 | Address verification — permanent | Mandatory | As per Aadhaar |
| 4 | Education certificate verification | Mandatory | University / board direct check |
| 5 | Previous employment verification | Mandatory | Reference from previous employer |
| 6 | POCSO clearance | Mandatory | Police record check — child safety |
| 7 | Police verification / character certificate | Mandatory | Local police station |
| 8 | Criminal background check | Mandatory | Court record check |
| 9 | Reference check | Mandatory | 2 professional references |
| 10 | Medical fitness certificate | Optional | Some institutions require |

### BGV Status Lifecycle

| Status | Meaning |
|---|---|
| Not Initiated | Staff joined — BGV not started |
| In Progress | BGV submitted to agency / being checked |
| Pending Documents | Staff yet to submit required documents |
| Cleared | All checks passed — staff fully verified |
| Failed | One or more checks failed |
| Conditionally Cleared | Minor issues — Principal + Management decision |

- Staff can be onboarded before BGV cleared — flagged as unverified
- POCSO clearance: mandatory before first interaction with students
- BGV failed: immediate suspension — Management reviews

### BGV Agency

| Item | Details |
|---|---|
| Type | Third-party agency or in-house verification |
| Agency name | Admin enters — EduForge maintains approved agency list |
| BGV reference number | Per staff per verification round |
| Cost | Institution bears BGV cost |
| Turnaround | 7–15 working days typically |

### BGV Periodic Renewal

| Item | Details |
|---|---|
| Frequency | Every 3 years — or on role change |
| POCSO | Renewed every 2 years |
| Trigger | System reminds admin 60 days before renewal due |
| Staff on renewal | Still active — flagged as renewal pending |
| Renewal failed | Same action as initial failure — suspension review |

### BGV Consent — DPDPA 2023

| Item | Details |
|---|---|
| Consent taken | Before BGV initiated — staff signs consent |
| Stored | Timestamped in system |
| Purpose | Background screening for child safety and institutional integrity |
| Withdrawal | Staff can withdraw consent — must inform institution |

---

## Financial & Statutory Compliance

### Salary Structure — Indian Standard

| Component | Type | Notes |
|---|---|---|
| Basic salary | Fixed | Per pay scale / band |
| Dearness Allowance (DA) | % of basic | Government / aided staff — Central / State DA |
| House Rent Allowance (HRA) | % of basic | Metro / Tier-2 / Other city slab |
| Travel Allowance (TA) | Fixed | Official duty travel |
| Medical Allowance | Fixed | Monthly medical benefit |
| Special Allowance | Fixed | Institution-specific |
| Performance Bonus | Variable | Annual — based on appraisal |
| Overtime / Extra Periods | Variable | Beyond standard teaching load |
| EPF Contribution | Deduction | 12% of basic — employee share |
| ESI Contribution | Deduction | 0.75% of gross — employee share |
| TDS on Salary | Deduction | Per income tax slab |
| Professional Tax | Deduction | State-specific — varies |
| Loan Repayment | Deduction | If staff loan taken |

### Pay Scales — Indian Standard

| Institution Type | Pay Scale |
|---|---|
| Government school teachers | 7th Pay Commission — Level 7/8/9/10 |
| Aided school teachers | State government pay scale |
| CBSE private school | Institution-defined — market rate |
| College lecturers | UGC 7th Pay Commission — Academic Level 10/11/12/13 |
| Government college professors | UGC pay scale |

### Statutory Deductions

| Deduction | Applicable To | Rate |
|---|---|---|
| EPF (Employee Provident Fund) | All employees with basic < ₹15,000 — optional above | 12% employee + 12% employer |
| ESI (Employee State Insurance) | Salary < ₹21,000/month | 0.75% employee + 3.25% employer |
| NPS (National Pension System) | Government institution staff | 10% employee + 14% employer |
| GPF (General Provident Fund) | Government / aided staff | As per contribution |
| Professional Tax | State-specific | Varies by state and salary slab |
| TDS | All staff above tax threshold | Per income tax slab |

### Gratuity

| Item | Details |
|---|---|
| Eligibility | 5 years continuous service — Payment of Gratuity Act 1972 |
| Formula | (Last drawn basic + DA) × 15/26 × years of service |
| Maximum | ₹20 lakhs (as per latest amendment) |
| Tracked | System calculates auto — shown to admin |
| On exit | Processed in full and final settlement |

### PF / NPS Nominee

| Item | Details |
|---|---|
| Nominee name | Mandatory — family member |
| Relationship | Spouse / Child / Parent |
| % share | If multiple nominees |
| Aadhaar of nominee | For KYC |
| Change | Staff requests → admin processes |

---

## Leave Management — Indian Standard

### Leave Types

| Leave Type | Full Name | Entitlement | Notes |
|---|---|---|---|
| CL | Casual Leave | 12 days/year | Cannot accumulate |
| EL | Earned Leave | 30 days/year | Accumulates — encashable |
| SL | Sick / Medical Leave | 10 days/year | Medical certificate if > 3 days |
| ML | Maternity Leave | 26 weeks | Maternity Benefit Act 1961 |
| PL | Paternity Leave | 15 days | Some states mandate |
| CCL | Child Care Leave | 730 days in service | For women — govt institutions |
| Study Leave | Study Leave | As per rules | For higher qualification |
| Election Duty | Special Duty Leave | As notified | Government school teachers |
| Census Duty | Special Duty Leave | As notified | Government school teachers |
| Examination Duty | Special Duty Leave | External board duty | |
| On-Duty | On Duty Leave | As assigned | Official work outside campus |
| Emergency Leave | Emergency | 2–3 days | Family emergency — Principal discretion |

### Leave Application Workflow

| Step | Action |
|---|---|
| 1 | Staff submits leave request — leave type, dates, reason |
| 2 | Class teacher / HOD notified — substitute arranged |
| 3 | HOD approves (< 3 days) / Principal approves (3+ days) |
| 4 | Leave balance deducted automatically |
| 5 | Attendance updated — leave marked |
| 6 | Substitute assigned for that period |

### Leave Balance Tracking

| Item | Details |
|---|---|
| Real-time | Balance shown to staff after every approval |
| Year-end | EL carry forward — CL lapses |
| Leave encashment | EL encashment on retirement or as per policy |
| Negative leave | Not allowed — admin must approve with reason |

---

## Staff Attendance

| Item | Details |
|---|---|
| Marking | Daily — in-time + out-time |
| Methods | Biometric / manual / mobile app |
| Biometric | Fingerprint enrolment — linked to attendance module |
| Late arrival | Grace period configurable — after grace = late mark |
| Half day | Before or after grace — counts as 0.5 day |
| Absent | Deducted from leave balance |
| Monthly report | Admin sees staff attendance report per month |
| Integration | Linked to payroll — absent days affect salary |

---

## Staff Duty Management

### Subject Assignment

| Item | Details |
|---|---|
| Who assigns | Admin — Principal approves |
| Fields | Subject, class, section, academic year |
| Multiple subjects | Teacher can be assigned multiple subjects |
| Qualification check | System warns if not qualified for subject |
| Change | Admin updates — teacher notified in-app |

### Class Teacher Assignment

| Item | Details |
|---|---|
| One per section | One class teacher per section per academic year |
| Responsibilities | Attendance, conduct, parent communication, report card |
| Change | Admin reassigns — Principal approves |
| Indian standard | Class teacher system — CBSE / State Board |

### HOD Assignment

| Item | Details |
|---|---|
| One per department | HOD manages all teachers in department |
| Responsibilities | Academic coordination, appraisal recommendation, timetable input |
| Additional pay | HOD allowance added to salary |
| Term | Annual — Principal recommends — Management approves |

### Teaching Load

| Level | Standard Periods Per Week |
|---|---|
| Primary school teacher | 30–35 periods |
| Secondary teacher | 24–30 periods |
| Senior secondary teacher | 20–24 periods |
| College lecturer (UGC) | 16 hours direct teaching |
| HOD (UGC) | 14 hours direct teaching |
| Principal | 6 hours minimum — CBSE norm |

- System warns if teacher exceeds standard load — workload balance enforced
- System warns if teacher has too few periods — underutilization flagged

### Substitute Teacher Management

| Step | Action |
|---|---|
| 1 | Staff applies for leave |
| 2 | Admin identifies available teacher for vacant periods |
| 3 | Substitute assigned — timetable updated |
| 4 | Substitute teacher notified in-app |
| 5 | Overtime tracked if substitute already at full load |

### Invigilator Assignment

| Item | Details |
|---|---|
| Assigned per exam | Admin assigns — Principal approves |
| Rotation | Different teachers per exam — no repeated invigilation |
| External exam | External invigilators from board — tracked separately |
| Duty chart | Published in-app 7 days before exam |
| Indian standard | One invigilator per 30 students — CBSE norm |

### Extra Duty Assignment

| Duty Type | Examples |
|---|---|
| Event duty | Sports day, annual day, cultural function |
| Election duty | Government school teachers — state / national election |
| Census duty | National census — government school teachers |
| Exam centre duty | Board exam centre — chief superintendent, invigilator |
| Extracurricular coach | Sports, music, drama, debate coach |
| Committee assignment | POCSO committee, admission committee, exam committee |

### Staff Period Diary — Indian Standard

| Item | Details |
|---|---|
| What | Teacher records topic taught in each period |
| Who enters | Teacher — daily after each period |
| Content | Class, subject, topic, chapter reference, remarks |
| Visibility | HOD + Principal can view |
| Indian standard | CBSE / State Board — lesson diary mandatory |
| Audit | Part of annual academic audit |

---

## Staff Performance

### Probation Review

| Item | Details |
|---|---|
| Period | 6 months or 1 year — institution defines |
| Review | HOD + Principal evaluate |
| Outcomes | Confirmed / Extended / Terminated |
| Extension | Max 1 additional year |
| Confirmation letter | Python generates on confirmation |

### Annual Appraisal

| Item | Details |
|---|---|
| KRA / KPI | Defined per designation at start of year |
| Self-assessment | Staff fills own assessment |
| HOD rating | HOD rates staff |
| Principal review | Final rating |
| Score | 1–5 scale |
| Outcome | Increment / Bonus / Training need / Warning |
| Indian standard | Required for NAAC — faculty appraisal system |

### Staff Feedback from Students — College Level

| Item | Details |
|---|---|
| Applicable | College level only |
| Anonymous | Student identity not revealed to teacher |
| Frequency | Once per semester |
| Parameters | Teaching quality, subject knowledge, communication, punctuality |
| Visible to | HOD + Principal + teacher (own rating only) |
| Used for | Appraisal input — not sole criteria |
| Indian standard | NAAC requirement — student feedback system |

### Staff Training & CPD Records

| Item | Details |
|---|---|
| Types | In-house training, external workshop, online course, FDP (Faculty Development) |
| Mandatory | CBSE requires teachers to complete 50 CPD hours/year |
| Record | Training name, date, hours, certificate number |
| Needs identification | Based on appraisal gap — admin assigns training |
| Senior mentor | Senior teacher assigned to guide new teacher |
| Indian standard | CBSE CPD mandate — DIKSHA platform integration |

### Staff Research / Publications — College NAAC

| Item | Details |
|---|---|
| Publications | Journal name, title, year, ISSN/ISBN |
| Research projects | Funded / unfunded — funding agency |
| Patents | Patent number, filing date, status |
| Industry experience | Years + sector — for technical institution accreditation |
| Conferences | Paper presented — national / international |
| Indian standard | NAAC API score — faculty research mandatory |

---

## Disciplinary Actions

### Warning

| Item | Details |
|---|---|
| Issued by | Principal |
| Reason | Misconduct, attendance issues, performance |
| Written | Issued in writing — stored in system |
| Staff response | Staff can submit written response — 7 days |
| Audit log | Immutable record |

### Staff Suspension During Inquiry

| Item | Details |
|---|---|
| Trigger | Serious misconduct — Principal + Management decision |
| Pay during suspension | 50% salary (subsistence allowance) — Indian labour law |
| Duration | Until inquiry complete |
| Access | System access suspended immediately |
| Inquiry committee | Formed — management nominates |
| Indian standard | Natural justice principles — notice + hearing |

### Staff Reinstatement

| Item | Details |
|---|---|
| After inquiry cleared | Full reinstatement — back pay if applicable |
| After inquiry adverse | Termination or demotion |
| System access | Restored on reinstatement order |

### Staff Termination

| Item | Details |
|---|---|
| Cause | Misconduct, BGV failure, repeated warnings |
| Process | Show cause notice → response → inquiry → order |
| Indian standard | Industrial Disputes Act — due process mandatory |
| Benefits | PF, gratuity paid as per law |
| Documents | Termination letter — no experience certificate |

### Increment Freeze

| Item | Details |
|---|---|
| Trigger | Disciplinary action — warning stage |
| Duration | 1 year — admin sets |
| Approval | Principal + Management |
| Lifted | After review — Principal recommends |

---

## Staff Exit Process

### Resignation

| Step | Action |
|---|---|
| 1 | Staff submits resignation — notice period starts |
| 2 | HOD + Principal acknowledge |
| 3 | Notice period | 1 month standard — as per appointment letter |
| 4 | Handover checklist — classes, assets, records |
| 5 | No-dues certificate — all assets returned |
| 6 | Full and final settlement processed |
| 7 | Experience certificate generated — Python |
| 8 | Relieving letter generated — Python |
| 9 | System access revoked on last working day |
| 10 | ID card deactivated |

### Full and Final Settlement

| Item | Details |
|---|---|
| Salary dues | Remaining salary for days worked |
| EL encashment | Pending earned leave encashed |
| Gratuity | If eligible (5+ years) — calculated + paid |
| PF settlement | PF withdrawal or transfer — employee choice |
| Loan recovery | Pending loan deducted from F&F |
| Bonus | Pro-rated if applicable |

### Staff Offboarding Checklist

| Item | Verified By |
|---|---|
| ID card returned | Admin |
| IT assets returned | Admin |
| Keys / access cards returned | Admin |
| Library books returned | Librarian |
| Hostel quarters vacated | Warden (if residential) |
| Class records handed over | HOD |
| Pending student assessment submitted | Principal |

### Documents Generated on Exit — Python

| Document | Details |
|---|---|
| Experience certificate | Name, designation, period, conduct |
| Relieving letter | Last working date, cleared of dues |
| Form 16 | TDS certificate — end of financial year |
| PF transfer / withdrawal form | UAN-based — staff submits online |

---

## Staff Loan & Advance

| Item | Details |
|---|---|
| Types | Salary advance / Staff loan (larger amount) |
| Approval | Principal + Management |
| Amount | Max 2 months salary — advance / 6 months — loan |
| Recovery | Monthly deduction from salary |
| Prepayment | Allowed — no penalty |
| Outstanding | Deducted from F&F if not cleared |

---

## Staff Insurance

### Medical Insurance

| Item | Details |
|---|---|
| Type | Group health insurance — institution policy |
| Coverage | Staff + dependents |
| Sum insured | Per institution policy |
| Cashless | Empanelled hospitals |
| Claim | Staff submits — admin processes |

### Accidental Insurance

| Item | Details |
|---|---|
| Type | Group personal accident policy |
| Coverage | On-duty accidents — 24×7 coverage |
| Sum insured | Per institution policy |

---

## Staff Welfare

### Staff Children Admission

| Item | Details |
|---|---|
| Discount | Fee concession for staff wards — institution policy |
| Quota | Reserved seats for staff children |
| Eligibility | Current full-time staff only |
| Tracking | Linked in system — staff profile ↔ student profile |

### Staff Quarters / Residential Accommodation

| Item | Details |
|---|---|
| Applicable | Boarding schools, rural schools, college campuses |
| Allotment | Management approves — admin records |
| HRA impact | HRA not payable if quarters allotted |
| Vacation | On resignation — vacate within 30 days |

### Staff Grievance

| Item | Details |
|---|---|
| Who can raise | Any staff member |
| Type | HR complaint, workload issue, pay discrepancy, harassment |
| Routes to | HR / Management — not Principal if complaint against Principal |
| Anonymous | Option available |
| Resolution | 15 working days — auto-escalates |
| POSH | Sexual harassment complaint → POSH committee (Indian law) |

---

## Staff Deputation

| Item | Details |
|---|---|
| Definition | Staff sent to another branch / institution temporarily |
| Approval | Management at both institutions |
| Duration | Fixed period — start + end date |
| Salary | Paid by home institution |
| DA for deputation | Deputation allowance — as per rules |
| Return | Automatic on end date — admin confirms |

---

## Staff NOC (No Objection Certificate)

| Purpose | Details |
|---|---|
| Higher studies | Staff pursuing further qualification |
| Guest lecture elsewhere | Teaching at another institution |
| Part-time work outside | Only if not conflicting |
| Passport application | Govt requirement for govt employees |
| Approval | Principal + Management |
| Generated by | Python |

---

## Service Book — Indian Government Standard

| Item | Details |
|---|---|
| Applicable | Government / aided school teachers |
| Contents | Joining date, qualifications, increments, leave record, promotions, awards, disciplinary actions |
| Maintained by | Admin — Principal certifies annually |
| Indian standard | Mandatory — Government of India / State education department |
| Format | Physical + digital copy in system |

---

## Staff Certification Tracking

| Certification | Renewal | Alert |
|---|---|---|
| First aid | 2 years | 30 days before |
| Fire safety | Annual | 30 days before |
| POCSO awareness | Annual | 30 days before |
| CPR | 2 years | 30 days before |
| State TET | No expiry | One-time |
| CTET | 7 years (changed to lifetime) | System updates |

---

## Staff Academic Standing

| Status | Trigger | Action |
|---|---|---|
| Active | Normal | Full access |
| On Leave | Approved leave | Access maintained |
| On Duty | Official duty outside campus | Marked OD |
| Under Probation | New joinee | Flagged — limited access |
| Suspended | Disciplinary | Access removed |
| Terminated | Termination order | All access removed |
| Retired | Reached retirement age | All access removed |

---

## Staff Multi-Role Management

| Item | Details |
|---|---|
| Multiple roles | Teacher + HOD + Exam Coordinator + POCSO Committee member |
| System | All roles shown — staff sees unified interface |
| Permissions | Each role adds specific permissions |
| Reporting | Each role reports to different authority |
| Workload | System calculates total load across all roles |

---

## Staff Audit Log

| Item | Details |
|---|---|
| What is logged | All profile changes, role changes, salary changes, BGV updates, disciplinary actions |
| Logged fields | Who changed, what, old value, new value, date/time, reason |
| Immutable | Cannot be edited or deleted |
| Visible to | Principal + Group admin + EduForge super-admin |
| Retention | Per criticality tiers — Module 04 |

---

## Staff Profile — DB Schema Reference

**shard.staff**

| Column | Type | Notes |
|---|---|---|
| id | UUID | Primary key |
| tenant_id | UUID | Institution |
| employee_id | TEXT | Unique per institution |
| full_name | TEXT | Legal name |
| dob | DATE | |
| gender | TEXT | |
| aadhaar_hash | TEXT | Encrypted |
| pan_number | TEXT | Encrypted |
| designation | TEXT | |
| department_id | UUID | |
| employment_type | TEXT | permanent/contract/probation/part-time/guest |
| aided_status | TEXT | aided/unaided |
| date_of_joining | DATE | |
| date_of_confirmation | DATE | Nullable |
| retirement_date | DATE | Auto-calculated |
| bgv_status | TEXT | not_initiated/in_progress/cleared/failed |
| pocso_cleared | BOOLEAN | |
| status | TEXT | active/on_leave/suspended/terminated/retired |
| bank_account | TEXT | Encrypted |
| ifsc_code | TEXT | |
| pf_account_number | TEXT | |
| esi_number | TEXT | Nullable |
| nps_pran | TEXT | Nullable |
| created_at | TIMESTAMPTZ | |
