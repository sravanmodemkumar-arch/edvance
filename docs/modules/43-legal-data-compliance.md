# Module 43 — Legal & Data Compliance

## 1. Purpose

Educational institutions in India operate under a web of overlapping regulatory obligations — GST, TDS, EPF, ESIC, Gratuity, Minimum Wages, POSH, RTE, UGC/AICTE affiliation, Anti-Ragging (UGC), Consumer Protection, RTI, FCRA, Motor Vehicles Act, Fire Safety, Environmental norms — spread across central statutes, state rules, and board-specific circulars. Each law has its own filing deadlines, penalty structure, and inspection readiness requirements. Most institution admin teams discover compliance gaps only when they receive a legal notice or a regulatory inspection catches them unprepared.

Module 42 covers DPDPA and the audit log — the data governance layer. Module 43 is the broader legal and regulatory compliance engine: the centralised compliance calendar, filing status tracking, legal notice register, penalty exposure estimation, inspection readiness scoring, and the one-click annual compliance summary for management committee review. Together, Modules 42 and 43 form EduForge's complete governance stack.

This module does not replace a legal counsel or a CA — it ensures that no filing deadline is missed, no document is unfiled, and no legal notice goes unanswered due to administrative oversight.

---

## 2. Regulatory Framework

### 2.1 Applicable Laws by Institution Type

| Law | School | College/University | Coaching | Hostel | All |
|---|---|---|---|---|---|
| GST (SAC 9993) | Partially exempt | Partially exempt | 18% taxable | Partially | ✅ |
| Income Tax (TDS) | ✅ | ✅ | ✅ | ✅ | ✅ |
| EPF Act | ✅ (≥20 staff) | ✅ | ✅ | ✅ | ✅ |
| ESIC Act | ✅ (≥10 staff) | ✅ | ✅ | ✅ | ✅ |
| Gratuity Act | ✅ (≥10 staff) | ✅ | ✅ | ✅ | ✅ |
| POSH Act 2013 | ✅ (≥10 staff) | ✅ | ✅ | ✅ | ✅ |
| RTE Act 2009 | ✅ (Classes 1–8) | ❌ | ❌ | ❌ | Partial |
| UGC Regulations | ❌ | ✅ | ❌ | ❌ | Partial |
| AICTE Regulations | ❌ | ✅ (technical) | ❌ | ❌ | Partial |
| Anti-Ragging (UGC) | ❌ | ✅ | ❌ | ✅ | Partial |
| Consumer Protection | ✅ | ✅ | ✅ | ✅ | ✅ |
| RTI Act | ✅ (aided) | ✅ (aided) | ❌ | ❌ | Partial |
| Motor Vehicles Act | ✅ (bus) | ✅ (bus) | Partial | ✅ | Partial |
| Fire Safety NOC | ✅ | ✅ | ✅ | ✅ | ✅ |
| FCRA | NGO/trust only | NGO/trust only | NGO only | ❌ | Partial |

Institution admin configures which laws apply at onboarding (Module 04); compliance calendar auto-populates applicable tasks.

### 2.2 GST Classification

The GST treatment of education-related services is nuanced:

| Service | GST Treatment | SAC Code |
|---|---|---|
| Tuition fee — CBSE/ICSE/State Board school | **Exempt** | 9992 |
| Tuition fee — UGC/AICTE-recognised college | **Exempt** | 9992 |
| Tuition fee — coaching institute (not recognised) | **18% GST** | 9992 |
| Hostel accommodation ≤ ₹1,000/day per person | **Exempt** | 9963 |
| Hostel accommodation > ₹1,000/day | **18% GST** | 9963 |
| Transport (school bus for students) | **Exempt** (included in school service) | — |
| Commercial canteen (non-school mess) | **5% GST** | 9963 |
| Library fine | **Exempt** | — |
| Lab fee — recognised institution | **Exempt** | 9992 |
| Sports / activity fee — recognised institution | **Exempt** | 9992 |
| Training / certificate course (short-duration) | **18% GST** | 9992 |
| Stationery sold to students | **Standard GST rates** | — |

Institution type at onboarding determines default GST treatment per fee type. Institution admin can override per fee head.

---

## 3. GST Compliance

### 3.1 GSTIN Management

- GSTIN validated at tenant onboarding via GSTN Taxpayer API: status must be ACTIVE
- Invalid or suspended GSTIN blocks fee invoice generation with clear error: "GST registration inactive — contact finance admin"
- Multi-campus institutions: each campus may have separate GSTIN (different states); managed per campus
- GST registration threshold: ₹20 lakh aggregate turnover (₹10 lakh for NE states); system alerts when approaching threshold

### 3.2 E-Invoicing (IRN)

For institutions with aggregate annual turnover > ₹5 crore (B2B invoices):
1. Invoice data POSTed to Invoice Registration Portal (IRP) via API before delivery
2. IRP returns IRN (Invoice Reference Number) + QR code
3. IRN and QR embedded in the invoice PDF (WeasyPrint template updated)
4. Invoice with IRN is the valid GST invoice for recipient's ITC claim

```python
# E-invoicing integration
async def generate_irn(invoice: Invoice) -> IRNResponse:
    payload = build_irn_payload(invoice)
    response = await irp_client.post("/ei/api/invoice", json=payload)
    return IRNResponse(**response.json())
```

### 3.3 GSTR Filing Support

| Return | Frequency | Due Date | System Output |
|---|---|---|---|
| GSTR-1 | Monthly (>₹5Cr) / Quarterly (≤₹5Cr) | 11th / 13th | JSON export in GSTR-1 format |
| GSTR-3B | Monthly | 20th | JSON export in GSTR-3B format |
| GSTR-9 | Annual | Dec 31 | Full year consolidated export |
| GSTR-9C | Annual (>₹2Cr) | Dec 31 | Reconciliation export for CA |

System generates the JSON; institution finance team uploads to GST portal. Direct API filing integration planned for Phase 2.

### 3.4 ITC Tracking

Input Tax Credit on purchases:
- GST paid on: lab equipment, computers, furniture, stationery (institution purchases)
- ITC eligible only for taxable supplies; blocked if institution's output is fully exempt (school)
- ITC register maintained; reconciled against GSTR-2B (auto-populated by GSTN from supplier's GSTR-1)

### 3.5 Compliance Calendar — GST

```
Monthly (by 20th): GSTR-3B submission
                   TDS deposit on GST payments to unregistered (if applicable)
Monthly (by 11th): GSTR-1 (if monthly filer — turnover > ₹5Cr)
Quarterly (by 13th): GSTR-1 (if quarterly filer — turnover ≤ ₹5Cr)
Annual (by Dec 31): GSTR-9 + GSTR-9C
```

---

## 4. Income Tax (TDS) Compliance

### 4.1 TDS Sections Applicable

| Section | Nature of Payment | Rate | Threshold |
|---|---|---|---|
| 192 | Salaries | Slab rate | Any amount |
| 194C | Contractor payments | 1% (individual/HUF), 2% (others) | > ₹30,000 single / ₹1 lakh annual |
| 194J | Professional fees (CA, doctor, lawyer, technical) | 10% | > ₹30,000 |
| 194I | Rent (building, equipment) | 10% (land/building), 2% (plant/machinery) | > ₹1.8 lakh annual |
| 194H | Commission/brokerage (agents, brokers) | 5% | > ₹15,000 |
| 194Q | Purchase of goods from resident | 0.1% | > ₹50 lakh annual from single vendor |

### 4.2 TDS Deposit & Returns

**Challan due dates:**
- TDS deducted in a month: deposited by 7th of following month
- TDS for March: deposited by April 30

**Quarterly TDS return due dates:**

| Quarter | Period | Due Date |
|---|---|---|
| Q1 | Apr–Jun | July 15 |
| Q2 | Jul–Sep | October 15 |
| Q3 | Oct–Dec | January 15 |
| Q4 | Jan–Mar | May 31 |

Forms: 24Q (salary), 26Q (non-salary), 27Q (NRI payments), 27EQ (TCS).

### 4.3 Form 16 / 16A Generation

**Form 16** (salary TDS certificate):
- Generated per employee from payroll annual summary (Module 27)
- PDF via WeasyPrint with: salary details, deductions (80C/80D), TDS computation, challan details
- Issued before June 15 each year
- Delivered via email (Module 37) + in-app Download Centre

**Form 16A** (non-salary TDS certificate):
- Generated per contractor/professional per quarter
- Delivered via email within 15 days of each quarterly return

### 4.4 TDS Reconciliation (26AS / AIS)

System exports:
- TAN-wise TDS deposited (by section, month, amount, challan number)
- Deductee-wise TDS details (PAN, name, amount, TDS deposited)

Finance team reconciles against Form 26AS / AIS downloaded from income tax portal. Discrepancies flagged for correction before return filing.

---

## 5. EPF & ESIC Compliance

### 5.1 EPF (Employees' Provident Fund)

**Contribution rates:**

| Component | Employee | Employer |
|---|---|---|
| EPF | 12% of Basic+DA | 3.67% of Basic+DA |
| EPS | — | 8.33% of Basic+DA (capped at ₹15,000) |
| EDLI | — | 0.5% of Basic+DA (capped at ₹15,000) |
| Admin charges | — | 0.50% of total wages |

**Monthly ECR filing:**
- ECR (Electronic Challan cum Return) filed by 15th of following month
- Generated from payroll data: employee UAN, wages, contribution amounts
- Uploaded to EPFO Unified Portal; challan paid via net banking

**UAN management:**
- New employee joining: UAN activation + KYC (Aadhaar, PAN, bank) within 30 days
- UAN already exists (portability): existing UAN linked; previous employer PF balance visible
- Exit: PF transfer (Form 13) or withdrawal (Form 19/10C) initiated within 30 days of leaving

### 5.2 ESIC (Employee State Insurance)

**Contribution rates:**

| Category | Rate |
|---|---|
| Employee | 0.75% of gross wages |
| Employer | 3.25% of gross wages |

**Applicable employees:** gross salary ≤ ₹21,000/month (₹25,000 for persons with disability).

**Monthly ESIC challan:** paid by 15th of following month via ESIC portal.

**IP registration:** every ESIC-covered employee receives an IP (Insured Person) number. IP number stored in staff profile (Module 08). Employee can access ESIC benefits using ESIC card.

**Maternity benefit through ESIC:** HR notified when female employee reports pregnancy; ESIC claim process guided in system.

### 5.3 Half-Yearly Returns (ESIC)

ESIC half-yearly returns (Form 5 / Form 6): filed for periods April–September (by November 12) and October–March (by May 12). Generated from ESIC contribution data.

---

## 6. Gratuity

### 6.1 Eligibility & Computation

Eligible after 5 years continuous service (4 years + 240 days for workers with less than 6-day weeks):

```
Gratuity = (Last Basic + DA) × 15 × Completed Years of Service / 26
```

Maximum gratuity: ₹20 lakhs (tax-exempt under Section 10(10)).

### 6.2 Module 27 Integration

- Module 27 (Payroll) computes monthly gratuity provision per employee (1/26 × 15 days of basic)
- Cumulative provision shown in staff profile as "gratuity liability"
- On resignation/retirement trigger in Module 08: gratuity computation auto-triggered; HR notified
- Gratuity payment: within 30 days of eligible departure; system alert at 20 days

### 6.3 Gratuity Fund

Options tracked in compliance module:
- LIC Group Gratuity Policy — policy number, premium payment, surrender value
- Approved Gratuity Trust — trust deed stored in Module 40; annual actuarial valuation recorded

---

## 7. POSH Act 2013 Compliance

### 7.1 Internal Complaints Committee (ICC)

**Composition:**
- Presiding Officer: senior woman employee
- ≥2 members (≥50% women)
- 1 external member: NGO / legal background

ICC term: 3 years. Renewal alert: 90 days before expiry.

**ICC records maintained in system:**
- Member roster with name, designation, contact
- Meeting minutes
- Complaint register

### 7.2 Complaint Process

```
Complaint received → Acknowledged within 7 days
                   → Conciliation attempt (if requested by complainant)
                   → If conciliation fails → Investigation within 90 days
                   → Report with recommendations → Management action within 60 days
```

Complaint register: complaint ID, date, disposition, timeline, outcome. Restricted access: ICC Presiding Officer + Principal.

### 7.3 POSH Annual Report

Due: January 31 to District Officer (under the Sexual Harassment of Women at Workplace Act).

System auto-generates:
- Number of complaints received in the calendar year
- Number disposed
- Number pending
- Awareness sessions conducted
- External member meetings held

Report reviewed by Presiding Officer → signed → submitted (submission tracked with reference).

### 7.4 Awareness & Policy

- POSH awareness training: all employees annually; Module 41 pattern (in-app training + completion tracking)
- POSH policy: written + acknowledged by all staff at joining and annually
- Display: POSH notice with ICC contact — at notice board, website
- External member engagement letter stored in Module 40

---

## 8. RTE Act Compliance (Schools)

### 8.1 25% EWS/DG Reservation

Private unaided schools (Classes 1–8) must reserve 25% seats for children from EWS and Disadvantaged Groups.

**Lottery system (Module 31):**
- Applications in RTE category collected via Module 31 (Admission CRM)
- Lottery conducted on the state-specified date; results published
- Lottery audit trail maintained for state authority review

**RTE reimbursement:**
- State government reimburses at per-child cost (notified annually)
- Claim filed with state education department; system generates student-wise list of RTE admissions
- Reimbursement tracking: claim filed date, amount claimed, amount received, balance pending

### 8.2 Other RTE Obligations

| Obligation | Module | Compliance Tracking |
|---|---|---|
| No entrance test / interview | Module 31 | Admission workflow blocks aptitude tests for RTE entries |
| Free TC (no dues block) | Module 39 | RTE tag disables dues-gate for TC |
| No detention up to Class 8 | Module 21 | Result module disables fail-status for RTE-applicabile grades (configurable) |
| No capitation fee | Module 24 | Fee structure validation; alert if unapproved fee heads exist |
| Age-appropriate admission | Module 31 | DOB validation at admission |

### 8.3 School Recognition

Recognition order from State Education Department and Board affiliation — stored in Module 40 with expiry tracking; renewal compliance in calendar.

---

## 9. Anti-Ragging Compliance (UGC 2009)

### 9.1 Committee Structure

| Committee | Composition | Role |
|---|---|---|
| Anti-Ragging Committee | Head: Principal; senior teachers; student representatives; police liaison | Policy, oversight, complaint investigation |
| Anti-Ragging Squad | Faculty members; rotating duty; hostels + campus | Mobile monitoring, prevention |

Both committees: members in system; contact numbers published on notice board, website, and anti-ragging portal.

### 9.2 Student/Parent Undertaking

At admission: anti-ragging affidavit from student and parent — submitted online via UGC anti-ragging portal + signed copy stored in Module 40.

For hostels: separate hostel anti-ragging undertaking at check-in.

### 9.3 Incident Register

Anti-ragging incident register (distinct from POCSO incident register):
- Same encrypted, restricted-access architecture as Module 41
- Incident: nature, accused (senior student / staff), victim, action taken, UGC portal report reference

### 9.4 Annual Compliance

Annual compliance certificate submitted electronically to UGC/AICTE:
- Certification that no ragging incident was reported, OR
- Full report if incidents occurred: number, actions taken, FIR lodged

Submission reference stored; acknowledgement tracked.

---

## 10. UGC / AICTE / NAAC Regulatory Compliance

### 10.1 AISHE (All India Survey on Higher Education)

Annual submission to MoE by November 30. Data auto-exported from:
- Module 07 (Student Enrolment): student count, gender, category, course-wise
- Module 08 (Staff): faculty count, qualification-wise
- Module 05 (Academic Year): program list, duration

AISHE portal upload format (JSON/CSV) generated; submission reference tracked.

### 10.2 NIRF (National Institutional Ranking Framework)

Annual submission by January 31. NIRF parameters drawn from:

| Parameter | Source Module |
|---|---|
| Teaching, Learning & Resources | Modules 08, 15, 16, 17 |
| Research & Professional Practice | Module 53 Analytics |
| Graduation Outcomes | Module 21 Results |
| Outreach & Inclusivity | Module 31, 32 |
| Perception | External survey |

System generates parameter-wise data export; finance data imported from accounts system.

### 10.3 NAAC AQAR

Annual Quality Assurance Report submitted to NAAC by September 30.

7 criteria mapped to data sources:

| Criterion | Data from EduForge |
|---|---|
| 1 — Curricular Aspects | Module 15 (Syllabus), Module 05 (Calendar) |
| 2 — Teaching-Learning | Modules 10, 11, 14, 16, 17 |
| 3 — Research | Module 53 Analytics |
| 4 — Infrastructure | Module 40 Documents (infrastructure compliance) |
| 5 — Student Support | Modules 31, 32, 33, 41 |
| 6 — Governance | Modules 03, 43 (this module), 40 |
| 7 — Institutional Values | Modules 41, 42 |

AQAR template auto-populated; institution fills narrative sections; submitted via NAAC portal.

### 10.4 Faculty Qualification Compliance

UGC norms monitored via Module 08 (Staff Management):
- Assistant Professor: NET/SET; M.Phil./PhD
- Associate Professor: PhD + 8 years experience + research publications
- Professor: PhD + 10 years experience

Qualification gap report — staff not meeting UGC norms highlighted; compliance risk flagged.

**Faculty:Student Ratio tracking:**

| Program Type | UGC Norm | Monitoring |
|---|---|---|
| UG Arts | 1:30 | Module 08 + 07 integration |
| UG Science | 1:20 | — |
| PG | 1:12 | — |
| PhD | 1:8 | — |

---

## 11. Consumer Protection Compliance

### 11.1 Fee Refund Policy

UGC/AICTE refund norms for annual programs (> 1 year):

| Withdrawal Timing | Refund % | Deduction |
|---|---|---|
| Before start of academic year | 100% | Processing fee only (max ₹1,000) |
| Within 15 days of start | 90% | — |
| Within 30 days of start | 80% | — |
| Within 60 days of start | 50% | — |
| After 60+ days | 0% | — |

Module 24 (Fee) refund engine applies these norms at the time of withdrawal; any deviation from UGC norms requires Principal override with documented reason (compliance risk flag).

### 11.2 Consumer Complaint Tracking

| Step | System Action |
|---|---|
| Complaint received (notice from consumer forum) | Logged in legal notice register; response deadline set (30 days typically) |
| Complaint acknowledged | Sent via Module 37 (email) with tracking ID |
| Response prepared | Legal counsel engaged; documents pulled from Module 40 |
| Hearing dates | Calendar entries; alerts 3 days before |
| Outcome | Recorded; appeal filed if unfavourable |

### 11.3 National Consumer Helpline / INGRAM

INGRAM (Integrated Grievance Redressal Mechanism) complaints from government portals routed to institution's grievance system; tracked as consumer complaints.

---

## 12. RTI Act Compliance (Government-aided Institutions)

### 12.1 PIO & FAA

Public Information Officer (PIO) and First Appellate Authority (FAA):
- Designated from staff (typically Vice Principal and Principal respectively)
- Name and contact published: website, notice board, and in-app (Settings → About Institution)
- Designation tracked in system; replacement protocol when staff leaves

### 12.2 Section 4 Proactive Disclosure

17 categories of information published without RTI request:

1. Institution's functions and duties
2. Powers and duties of officers
3. Procedure followed in decision-making
4. Norms for discharge of functions
5. Rules and regulations
6. Documents held (categories)
7. Consultative committees
8. Policy statements (fee, admission)
9. Directory of officers and staff
10. Monthly remuneration of staff (salary range, not individual)
11. Budget and expenditure
12. Implementation of subsidy programmes
13. Concessions / permits / authorisations
14. Electronic data available
15. Particulars of information available in electronic form
16. Names and designations of PIOs
17. Other useful information

System generates a Section 4 disclosure PDF from live data annually; published on institution website.

### 12.3 RTI Application Processing

RTI application received → logged in legal notice register with 30-day deadline:
- Admin reviews relevant documents in Module 40
- Response drafted (documents attached or summary provided)
- Fees collected (₹10 per application, ₹2 per page)
- Response sent; acknowledgement stored

Annual return to Information Commission: number of applications received, disposed, pending, appeals.

---

## 13. Compliance Calendar

### 13.1 Calendar Structure

The compliance calendar is the operational centre of this module:

```
┌─────────────────────────────────────────────────────────────────────┐
│  Compliance Calendar — April 2026                                   │
├──────────────┬──────────────────┬────────────┬──────────┬──────────┤
│  Due Date    │  Task            │  Law       │  Owner   │  Status  │
├──────────────┼──────────────────┼────────────┼──────────┼──────────┤
│  07 Apr      │  TDS Deposit     │  IT Act    │  Finance │  ✅ Done │
│  10 Apr      │  PF/ESIC Challan │  EPF/ESIC  │  HR      │  ⏳ Due  │
│  11 Apr      │  GSTR-1 (Q4)     │  GST       │  Finance │  ⏳ Due  │
│  15 Apr      │  ECR Filing      │  EPF       │  HR      │  ⏳ Due  │
│  15 Apr      │  ESIC Return     │  ESIC      │  HR      │  ⏳ Due  │
│  20 Apr      │  GSTR-3B (Mar)   │  GST       │  Finance │  ⬜ Open │
│  30 Apr      │  RTI Annual Rtn  │  RTI       │  PIO     │  ⬜ Open │
│  30 Apr      │  TDS Deposit Mar │  IT Act    │  Finance │  ⬜ Open │
└──────────────┴──────────────────┴────────────┴──────────┴──────────┘
```

### 13.2 Task Completion Flow

1. System sends push + email alert to task owner at configured intervals (30/15/7/3/1 day before due)
2. Owner completes filing externally; returns to system
3. Owner marks task complete: filing reference number, date filed, attachment (acknowledgement in Module 40)
4. Task turns green; compliance score updated
5. If overdue: escalation to Principal; penalty exposure estimated and displayed

### 13.3 Penalty Estimation Engine

System calculates estimated penalty for overdue filings:

| Filing | Penalty | Estimated Exposure |
|---|---|---|
| GSTR-1 late filing | ₹200/day (nil return: ₹50/day) | Computed from days overdue × rate |
| TDS late filing (234E) | ₹200/day | Computed from days overdue × rate |
| EPF late deposit | 12–18% interest p.a. | Computed from overdue amount × rate |
| ESIC late deposit | 12% interest p.a. | Computed from overdue amount |
| POSH annual report late | Penalty on company (no fixed rate; up to ₹25,000 fine) | Flag only |

Penalty exposure total shown on compliance dashboard as "Estimated Penalty Risk: ₹XX,XXX" — drives urgency for overdue tasks.

---

## 14. Legal Notice Register

### 14.1 Notice Intake

When an institution receives a legal notice:

```
Log Legal Notice
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Type:           ○ Consumer Forum  ○ Labour Court  ○ High Court
                ○ GST/TDS Notice  ○ POCSO         ○ Other
From:           [Complainant / Court / Authority]
Date Received:  [date]
Subject:        [brief description]
Claim Amount:   ₹ [if applicable]
Response Due:   [date] ← auto-calculated based on notice type
Legal Counsel:  [name, firm]
Attach Notice:  [upload — Module 40 storage]
[Save]
```

### 14.2 Notice Tracking

```
Legal Notices — Active (8)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Case                         │ Type         │ Due    │ Status
──────────────────────────────┼──────────────┼────────┼────────
 Sharma vs School (Fee Refund)│ Consumer     │ 5 Apr  │ ⚠️ 3 days
 EPF Inspection Notice        │ Labour       │ 15 Apr │ In progress
 GST Scrutiny Notice          │ GST Dept     │ 30 Apr │ Pending
 [...]
```

### 14.3 Hearing Calendar Integration

Court/forum hearing dates added to compliance calendar:
- Alert 3 days before hearing: "Consumer Forum hearing for Sharma vs School tomorrow — Documents needed: [list from Module 40]"
- Hearing outcome recorded: Pending / Stayed / Decided-Favourable / Decided-Unfavourable / Settled / Appeal
- Appeal filed: new case linked to original; timeline continues

---

## 15. FCRA Compliance

### 15.1 Applicable Institutions

FCRA applies to: NGO-managed institutions, trust-run schools/colleges receiving foreign donations/grants from international bodies, USAID, World Bank, foreign alumni, or NRI donors.

### 15.2 FCRA Filing Calendar

| Filing | Due Date | Generated From |
|---|---|---|
| FC-4 (Quarterly return) | 15 days after quarter end | Foreign receipt records |
| FC-6 (Annual return) | December 31 | Full year foreign receipts + utilisation |
| FCRA registration renewal | 6 months before expiry | Registration expiry tracker |
| Intimation of change | Within 15 days of change | Org change events |

### 15.3 FCRA Fund Tracking

- Designated FCRA bank account (SBI mandatory since 2020): account number stored; all foreign receipts must flow through this account
- Utilisation tracking: 80% minimum for stated charitable purpose; system flags diversion attempts
- 20% available for administrative expenses: tracked separately
- Separate FCRA audit by CA: certificate stored in Module 40

---

## 16. Fire Safety & Environmental Compliance

### 16.1 Fire Safety

| Compliance Item | Frequency | Tracking |
|---|---|---|
| Fire NOC from Fire Department | Annual | Expiry in Module 40; alert 90 days before |
| Fire drill | ≥ 2/year | Drill date, participants, findings logged |
| Fire extinguisher service | Annual | Serial number, service date, next due; per extinguisher |
| Fire warden training | Annual | Module 40 certificate; staff roster |
| Sprinkler system inspection (> 4 floors) | Annual | Certificate in Module 40 |

### 16.2 Environmental Compliance

| Compliance Item | Authority | Frequency |
|---|---|---|
| Pollution Control Board NOC (DG sets, labs) | State PCB | Annual |
| Solid waste management records | Municipality | Ongoing |
| Biomedical waste disposal cert (medical colleges) | Authorised agency | Per pickup |
| E-waste disposal cert | Registered recycler | Per disposal |
| Energy audit (buildings > 500 kW connected load) | BEE | Every 3 years |

All certificates stored in Module 40; expiry tracked in compliance calendar.

---

## 17. Compliance Score & Inspection Readiness

### 17.1 Compliance Score

```
Institutional Compliance Score — April 2026

GST Filing         [████████████████████] 100%  ✅ All returns filed on time
TDS Filing         [██████████████████░░]  90%  ⚠️ Form 16A Q3 — 5 days late
EPF Compliance     [████████████████████] 100%  ✅
ESIC Compliance    [████████████████████] 100%  ✅
Labour Law         [████████████████░░░░]  80%  ⚠️ POSH annual report pending
Education Regulatory [██████████████████░]  90%  ⚠️ AISHE filing — 12 days pending
Fire & Safety      [████████████████████] 100%  ✅
Legal Notices      [██████████████████░░]  90%  ⚠️ 2 notices pending response

Overall            [███████████████████░]  93.4%
```

### 17.2 CBSE / NAAC Inspection Readiness

System checks which documents are required for a specific inspection type and their availability in Module 40:

```
CBSE Inspection Readiness
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Required Documents:          Present  Missing
  Affiliation certificate      ✅       —
  Child Protection Policy      ✅       —
  Staff qualification certs    42/44   2 missing ⚠️
  Fire NOC                     ✅       —
  Building plan approval       ✅       —
  POCSO committee constitution ✅       —
  Annual compliance report     ✅       —
  ─────────────────────────────────────────
  Readiness Score: 94% — Upload 2 missing documents
```

### 17.3 Monthly Management Report

One-page compliance status PDF generated at month-end for management committee:
- Filings due this month: filed / pending / overdue
- Legal notices: new, in progress, resolved this month
- Penalty exposure: ₹X
- Inspection readiness: X%

---

## 18. Database Schema

```sql
-- Compliance calendar tasks
CREATE TABLE compliance_tasks (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id       UUID NOT NULL REFERENCES tenants(id),
  law             TEXT NOT NULL,        -- GST / TDS / EPF / ESIC / POSH / UGC / RTE / FIRE etc.
  task_name       TEXT NOT NULL,
  description     TEXT,
  frequency       TEXT NOT NULL,        -- MONTHLY / QUARTERLY / ANNUAL / ONCE
  due_date        DATE NOT NULL,
  owner_id        UUID REFERENCES staff(id),
  status          TEXT DEFAULT 'PENDING',  -- PENDING / IN_PROGRESS / DONE / OVERDUE / NA
  completed_at    DATE,
  reference_number TEXT,               -- filing reference / challan number
  document_id     UUID REFERENCES documents(id),  -- acknowledgement document
  penalty_per_day NUMERIC,             -- for penalty estimation
  estimated_penalty NUMERIC GENERATED ALWAYS AS (
    CASE WHEN status = 'OVERDUE' AND penalty_per_day IS NOT NULL
    THEN penalty_per_day * (CURRENT_DATE - due_date)
    ELSE 0 END
  ) STORED,
  alert_days      INT[] DEFAULT ARRAY[30, 15, 7, 3, 1],
  created_at      TIMESTAMPTZ DEFAULT now()
);

-- Legal notice register
CREATE TABLE legal_notices (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id       UUID NOT NULL REFERENCES tenants(id),
  notice_type     TEXT NOT NULL,        -- consumer_forum / labour / high_court / gst / tds / pocso / other
  from_party      TEXT NOT NULL,
  received_date   DATE NOT NULL,
  subject         TEXT NOT NULL,
  claim_amount    NUMERIC,
  response_due    DATE NOT NULL,
  legal_counsel   TEXT,
  document_id     UUID REFERENCES documents(id),
  status          TEXT DEFAULT 'PENDING',  -- PENDING / IN_PROGRESS / HEARING_SCHEDULED / DECIDED_FAVOURABLE / DECIDED_UNFAVOURABLE / SETTLED / APPEAL / CLOSED
  outcome_notes   TEXT,
  created_at      TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE legal_hearings (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  notice_id       UUID NOT NULL REFERENCES legal_notices(id),
  hearing_date    DATE NOT NULL,
  forum           TEXT NOT NULL,
  outcome         TEXT,       -- Adjourned / Decided / Settled / etc.
  next_date       DATE,
  notes           TEXT
);

-- GST configuration
CREATE TABLE gst_config (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id       UUID NOT NULL REFERENCES tenants(id) UNIQUE,
  gstin           TEXT NOT NULL,
  gstin_status    TEXT,           -- ACTIVE / SUSPENDED / CANCELLED — from GSTN API
  gstin_verified_at TIMESTAMPTZ,
  pan             TEXT,
  tan             TEXT,
  annual_turnover NUMERIC,        -- determines GSTR-1 frequency and e-invoicing threshold
  e_invoicing_enabled BOOLEAN DEFAULT FALSE,
  gstr1_frequency TEXT DEFAULT 'QUARTERLY',  -- MONTHLY / QUARTERLY
  updated_at      TIMESTAMPTZ DEFAULT now()
);

-- Fee type GST mapping
CREATE TABLE fee_gst_mapping (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id       UUID NOT NULL REFERENCES tenants(id),
  fee_type        TEXT NOT NULL,
  sac_code        TEXT NOT NULL,
  gst_rate        NUMERIC NOT NULL DEFAULT 0,  -- 0 = exempt, 5, 12, 18
  taxable         BOOLEAN DEFAULT FALSE,
  override_reason TEXT
);

-- POSH complaint register
CREATE TABLE posh_complaints (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id       UUID NOT NULL REFERENCES tenants(id),
  complaint_ref   TEXT NOT NULL UNIQUE,
  received_date   DATE NOT NULL,
  complainant_anon_id TEXT NOT NULL,  -- anonymised
  accused_anon_id TEXT NOT NULL,
  nature          TEXT NOT NULL,
  status          TEXT DEFAULT 'PENDING',  -- PENDING / CONCILIATION / INVESTIGATION / DECIDED / CLOSED
  conciliation_outcome TEXT,
  investigation_outcome TEXT,
  management_action TEXT,
  closed_date     DATE,
  created_at      TIMESTAMPTZ DEFAULT now()
);

-- RTE reimbursement tracking
CREATE TABLE rte_reimbursements (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id       UUID NOT NULL REFERENCES tenants(id),
  academic_year   TEXT NOT NULL,
  student_count   INT NOT NULL,
  per_child_amount NUMERIC NOT NULL,
  total_claimed   NUMERIC NOT NULL,
  claim_filed_date DATE,
  amount_received NUMERIC DEFAULT 0,
  balance_pending NUMERIC GENERATED ALWAYS AS (total_claimed - amount_received) STORED,
  state_reference TEXT
);
```

---

## 19. RBAC Matrix

| Action | Finance Manager | HR Manager | Compliance Officer | Principal | Super Admin |
|---|---|---|---|---|---|
| View GST compliance | ✅ | ❌ | ✅ | ✅ | ✅ |
| Mark GST tasks complete | ✅ | ❌ | ✅ | ✅ | ✅ |
| View TDS compliance | ✅ | ❌ | ✅ | ✅ | ✅ |
| View EPF/ESIC compliance | ❌ | ✅ | ✅ | ✅ | ✅ |
| View POSH complaint register | ❌ | ✅ (Presiding Officer) | ✅ | ✅ | ✅ |
| View legal notice register | ❌ | ❌ | ✅ | ✅ | ✅ |
| Log legal notice | ❌ | ❌ | ✅ | ✅ | ✅ |
| View compliance calendar | ✅ | ✅ | ✅ | ✅ | ✅ |
| Generate AISHE / NAAC export | ❌ | ❌ | ✅ | ✅ | ✅ |
| View full compliance score | ❌ | ❌ | ✅ | ✅ | ✅ |
| View penalty exposure | ✅ | ❌ | ✅ | ✅ | ✅ |

---

## 20. API Reference

```
# Compliance calendar
GET    /api/v1/compliance/tasks/                   # All tasks (filtered by status, law, owner)
PATCH  /api/v1/compliance/tasks/{id}/complete/     # Mark task complete
GET    /api/v1/compliance/tasks/overdue/           # Overdue tasks with penalty estimates
GET    /api/v1/compliance/score/                   # Institution compliance score

# GST
GET    /api/v1/compliance/gst/gstr1-export/        # GSTR-1 JSON export
GET    /api/v1/compliance/gst/gstr3b-export/       # GSTR-3B JSON export
GET    /api/v1/compliance/gst/gstr9-export/        # GSTR-9 annual export

# TDS
GET    /api/v1/compliance/tds/form24q/?quarter=    # Form 24Q export
GET    /api/v1/compliance/tds/form26q/?quarter=    # Form 26Q export
GET    /api/v1/compliance/tds/form16/              # Form 16 bulk generation trigger

# Legal notices
POST   /api/v1/compliance/legal-notices/           # Log new notice
GET    /api/v1/compliance/legal-notices/           # All notices
PATCH  /api/v1/compliance/legal-notices/{id}/      # Update status
POST   /api/v1/compliance/legal-notices/{id}/hearings/ # Add hearing date

# Regulatory exports
GET    /api/v1/compliance/aishe-export/            # AISHE data export
GET    /api/v1/compliance/nirf-export/             # NIRF data export
GET    /api/v1/compliance/naac-aqar/               # NAAC AQAR export
GET    /api/v1/compliance/inspection-readiness/?type=CBSE  # Inspection readiness

# POSH
GET    /api/v1/compliance/posh/complaints/         # ICC complaint register
POST   /api/v1/compliance/posh/annual-report/      # Generate POSH annual report
GET    /api/v1/compliance/posh/annual-report/{id}/download-url/
```

---

## 21. Cross-Module Integration Map

| Module | Integration |
|---|---|
| Module 05 — Academic Calendar | AISHE, NAAC program and calendar data |
| Module 07 — Student Enrolment | AISHE student count; RTE admission tracking; consumer protection refund data |
| Module 08 — Staff Management | EPF/ESIC enrolment; TDS deduction records; faculty qualification compliance |
| Module 15 — Syllabus | NAAC Criterion 1 data |
| Module 21 — Results | NIRF graduation outcomes; NAAC Criterion 2 |
| Module 24 — Fee Structure | GST per fee-type mapping; fee refund policy compliance |
| Module 27 — Payroll | TDS Form 16; EPF ECR data; ESIC challan; Gratuity computation |
| Module 29 — Transport | Motor Vehicles Act compliance; bus permit tracking |
| Module 31 — Admission CRM | RTE lottery; admission quota compliance |
| Module 40 — Document Management | All compliance certificates, filing acknowledgements, legal notice documents |
| Module 41 — POCSO | POCSO legal notices tracked here; POCSO compliance integrated into inspection readiness |
| Module 42 — DPDPA & Audit Log | All compliance task changes, legal notice accesses, POSH complaint accesses logged |
| Module 53 — Platform Analytics | NIRF and NAAC data sourced from analytics |

---

*Module 43 — Legal & Data Compliance — EduForge Platform Specification*
*Version 1.0 | 2026-03-26*
