# Module 26 — Fee Defaulters & Recovery

## 1. Purpose

Identify, classify, track, escalate, and recover outstanding fee dues across every institution type
on EduForge — schools (CBSE/state board/KVS/NVS/government-aided), colleges (UGC/AICTE/university-
affiliated), coaching institutes (JEE/NEET/UPSC/Banking/SSC), skill centres (NCVT/PMKVY/DDU-GKY),
and online programmes. Module 26 receives outstanding balances from Module 25 (year-end lock +
daily outstanding feed), manages the full defaulter lifecycle from first overdue flag through
structured recovery, legal action, Lok Adalat settlement, and write-off, while enforcing the
no-embarrassment policy, DPDPA 2023 data minimisation for recovery agents, Limitation Act 1963
3-year clock management, Section 138 Negotiable Instruments Act prerequisites for cheque bounce
criminal complaints, UGC/AICTE student protection regulations, and 7-year immutable audit
retention. Module 26 owns defaulter identification, classification, communication escalation,
recovery planning, legal case management, write-off, and bad debt provisioning only. Module 25
owns payment posting and receipt generation. Module 39 owns TC and certificate hold enforcement.

---

## 2. Module Boundaries

### 2.1 What This Module Owns
- Defaulter identification and status lifecycle management
- Risk scoring and defaulter profiling
- Communication escalation (soft reminder → formal notice → pre-legal → legal)
- Recovery plan creation, tracking, breach detection
- Legal case register (Section 138, civil suit, Consumer Forum, Lok Adalat)
- Write-off approval workflow and write-off register
- Bad debt provisioning (accounting)
- Defaulter MIS and portfolio health reports
- Limitation Act clock tracking

### 2.2 What This Module Reads
| Source | Data Read |
|---|---|
| Module 25 | Outstanding balance per student; daily feed + year-end locked outstanding |
| Module 07 | Student category (RTE, EWS, OBC/SC/ST), admission status, dropout flag |
| Module 09 | Parent/guardian contact; court-order split; NRI flag |
| Module 24 | Default interest rate config; grace period config; write-off threshold |
| Module 28 | Hostel occupancy (for eviction workflow) |
| Module 29 | Transport route assignment (for route cancellation) |

### 2.3 What This Module Writes
| Destination | Data Written |
|---|---|
| Module 19 | Hall ticket block flag |
| Module 21 | Result / marksheet hold flag |
| Module 25 | Recovery plan demand schedule (new instalment dates) |
| Module 30 | Library card suspension flag |
| Module 32 | Counselor referral for financially stressed students |
| Module 39 | TC / certificate / degree withhold flag |

---

## 3. Defaulter Definition & Identification

### 3.1 Defaulter Threshold (Institution-Configurable)
- System does NOT hardcode "X days = defaulter" — institution configures per fee head
- Default config (pre-loaded; institution modifies):

| Fee Head | Grace Period | Overdue Flag | Defaulter Flag |
|---|---|---|---|
| Tuition Fee | 15 days | D+1 after grace | D+30 after grace |
| Hostel Fee | 5 days | D+1 after grace | D+15 after grace |
| Transport Fee | 7 days | D+1 after grace | D+20 after grace |
| Exam Fee | 0 days | D+1 after due date | D+7 after due date |
| Board Passthrough Fee | 0 days | D+1 | D+5 (board deadline sensitive) |

### 3.2 Defaulter Status Lifecycle
```
CURRENT (within due date + grace)
       │
OVERDUE (grace expired; payment not received)
       │
DELINQUENT (7–30 days overdue; soft communication active)
       │
DEFAULTER (30+ days overdue; formal notice issued)
       │
CHRONIC (90+ days overdue; 2+ academic years or 3+ instalments defaulted)
       │
LEGAL (legal notice issued; suit filed or Section 138 complaint filed)
       │
       ├── SETTLED (Lok Adalat / negotiated settlement)
       │
       ├── DECREE (court decree obtained; execution in progress)
       │
       └── WRITTEN_OFF (irrecoverable; approved by Finance Head + Management)
```

### 3.3 Automated Daily Job
- Runs at midnight: scans all outstanding demands from Module 25
- Compares due_date + grace_period vs today
- Updates defaulter status for each student automatically
- Generates next-day action list for Accountant (new defaulters, escalation-due, legal-due)
- Logs every status change with timestamp; immutable

### 3.4 Partial Payer Classification
- Student paid some but not all of an instalment
- Classification: `PARTIAL_DEFAULT` (separate from full default)
- Recovery target = outstanding balance only (not full instalment)
- Communication tone: softer than full default; acknowledge partial payment

### 3.5 Defaulter Feed from Module 25
- Daily feed: Module 25 pushes outstanding_balance per student per demand per head
- Year-end feed: Module 25 locks outstanding and transfers all unpaid demands to Module 26
- Carried-forward dues: tagged with original academic_year_id; treated as historical default

---

## 4. Defaulter Classification & Risk Scoring

### 4.1 Risk Score Components
| Factor | Weight | Notes |
|---|---|---|
| Days overdue | 30% | More days = higher score |
| Amount outstanding | 20% | Larger amount = higher score |
| Bounce count (history) | 20% | Each bounce adds significantly |
| Default history (prior years) | 15% | First-time vs repeat vs chronic |
| Instalment number | 10% | Last-instalment default more common; weighted lower |
| NACH/UPI AutoPay failure count | 5% | Repeated mandate failures = higher score |

### 4.2 Risk Tiers
| Tier | Score | Days Overdue | Action Level |
|---|---|---|---|
| LOW | 0–25 | 1–30 days; first-time | Automated soft reminders only |
| MEDIUM | 26–50 | 31–90 days | Accountant personal outreach |
| HIGH | 51–75 | 91–180 days | Finance Head review; recovery plan offer |
| CRITICAL | 76–100 | 180+ days or chronic | Legal escalation; write-off assessment |

### 4.3 Defaulter Type Tags
- `FIRST_TIME` — never defaulted before in any academic year
- `REPEAT` — defaulted in a previous academic year; paid eventually
- `CHRONIC` — defaulted in 3+ consecutive instalments or 2+ academic years
- `SEASONAL` — consistently defaults in specific months (agricultural family pattern)
- `PARTIAL_PAYER` — always pays something but never full amount
- `SCHEME_PENDING` — not a true defaulter; scheme disbursement delayed
- `DISPUTE_HOLD` — amount under formal dispute (Module 25 grievance)
- `HARDSHIP` — financial hardship certified; special recovery track
- `FORCE_MAJEURE` — natural disaster / pandemic / court-ordered suspension

### 4.4 Seasonal Defaulter Pattern
- System identifies students who default in same months across 2+ academic years
- Flags as `SEASONAL`; suppresses escalation during expected default window
- Agricultural families: system allows "harvest schedule" — no escalation until Oct/Nov (post-harvest)
- Institution configures harvest month per branch (varies: Kharif Oct, Rabi Mar/Apr)

### 4.5 Defaulter Portfolio Analysis
- Cluster analysis by: risk tier, amount bucket, vintage (which academic year), fee head
- Drives recovery strategy: CRITICAL tier → legal; HIGH → Finance Head personal call; MEDIUM → WhatsApp + payment link; LOW → automated only
- Portfolio health score: weighted average risk score across all defaulters; tracked monthly

---

## 5. Exclusions — Who Is Never a Defaulter

### 5.1 Absolute Exclusions
| Category | Reason | System Action |
|---|---|---|
| RTE students | Zero tuition demand; no default possible | Excluded from all defaulter jobs |
| Fully govt-scheme-covered students | Zero demand | Excluded |
| Sponsored students (sponsor paying) | Sponsor is accountable, not student | Student excluded; sponsor tracked separately |
| Students with active scheme verification | Scholarship pending Finance Head review | Clock paused; SCHEME_PENDING tag |
| Students with active fee dispute (Module 25) | Amount contested | DISPUTE_HOLD tag; clock paused for disputed amount |
| Board passthrough for board exams | Cannot block board exam | Separate recovery; never academic hold |

### 5.2 Special Circumstance Suspensions
| Circumstance | Action | Duration |
|---|---|---|
| Student death | Debt forgiveness; write-off initiated immediately | Permanent |
| Parent/guardian death | Compassionate deferral; no escalation | 6 months minimum |
| Natural disaster (flood/earthquake/cyclone) | Force majeure; recovery suspended | Until state government declares relief period over |
| Pandemic / epidemic | Bulk force majeure flag for affected cohorts | Per government order |
| Student serious illness (hospitalised) | Recovery suspended; instalment rescheduled | Duration of treatment + 30 days |
| Court-ordered suspension | System enforces court order; no recovery action | Per court order duration |

---

## 6. Academic & Service Consequences

### 6.1 Consequence Triggers (Configurable Thresholds)
- Institution configures which consequences activate at which overdue threshold
- Default configuration (institution can modify):

| Consequence | Threshold | Module |
|---|---|---|
| Portal access restricted to payment screen | 30 days overdue | All modules |
| Library card suspended | 30 days overdue | Module 30 |
| Coaching batch attendance blocked | 30 days overdue (coaching only) | Module 12 |
| Online content access locked | 30 days overdue (online/hybrid) | Module 44 |
| Hall ticket blocked | 45 days overdue | Module 19 |
| Report card / result hold | 60 days overdue | Module 21 |
| Bonafide / character certificate hold | 60 days overdue | Module 39 |
| TC issuance blocked | Any outstanding dues | Module 39 |
| Migration certificate blocked | Any outstanding dues | Module 39 |
| Degree certificate blocked | Any outstanding dues (college) | Module 39 |
| Convocation access blocked | Any outstanding dues (college) | Module 39 |
| Semester registration blocked | Any outstanding dues (college) | Module 07 |
| ATKT/KT registration blocked | Any outstanding dues (Maharashtra/Gujarat college) | Module 07 |
| Class promotion blocked | Any outstanding dues (school; institution-configurable) | Module 07 |

### 6.2 What Is NEVER Blocked (Absolute Limits)
- Attendance marking — teacher marks attendance regardless of fee status (legal obligation)
- Emergency notifications (safety, health, disaster alerts)
- Access to student in medical emergency
- RTE students — zero consequences, no exceptions
- Students with active court stay order against institution
- CWSN (Children With Special Needs) — default: no service blocks; configurable

### 6.3 CRITICAL Legal Risk — Mid-Year Expulsion
- Indian courts (multiple High Courts) have held: institution cannot expel a student
  mid-academic-year solely for fee non-payment
- System generates mandatory LEGAL RISK alert when Principal attempts mid-year expulsion for fee default
- Alert text: "WARNING: Expelling a student mid-academic-year for fee non-payment has been
  restrained by High Courts in multiple states. This action carries significant legal risk.
  Consult legal counsel before proceeding."
- Principal must explicitly acknowledge the alert to proceed; acknowledgement is audit-logged
- EduForge Customer Success notified of the acknowledgement (platform liability protection)

### 6.4 Board Exam Protection
- Student cannot be blocked from board exam (CBSE/State Board) for unpaid passthrough fee
- Institution has legal obligation to submit student's board exam form
- Institution recovers passthrough dues from student separately after exam
- System enforces this: passthrough default never triggers hall ticket block

### 6.5 Hostel Eviction Process
```
Step 1 — Hostel eviction notice (formal letter from Warden + Accountant)
       │ 7-day notice period mandatory
       │
Step 2 — Finance Head + Principal approval for eviction
       │
Step 3 — Inventory of student's belongings (room inspection; logged)
       │
Step 4 — Eviction date set; student given notice to vacate
       │
Step 5 — Module 28 (Hostel) room status → VACANT on eviction date
       │
Step 6 — Security deposit adjusted against dues (Finance Head approval)
       │
Step 7 — Student contacts logged for ongoing fee recovery
```

### 6.6 Transport Route Cancellation
- Module 29 integration: student removed from transport route
- 3-day notice to parent before cancellation (WhatsApp + in-app)
- Re-admission to route: dues clearance + Module 29 admin approval + seat availability check

### 6.7 Consequence Override
- Principal can temporarily lift any consequence for a specific student
- Override fields: student_id, consequence_type, lifted_until_date, reason, approved_by
- Maximum override duration: 30 days (configurable)
- Override is audit-logged; parent NOT shown the override reason (privacy)
- Parent sees: "Temporary access restored. Please clear dues by [date]."

---

## 7. No-Embarrassment & Confidentiality Policy

### 7.1 Absolute Rules (Cannot Be Configured Away)
- Defaulter status NEVER communicated to student in classroom or in presence of peers
- Defaulter list NEVER published on notice board, WhatsApp group, or any public channel
- Class teacher is NOT notified of fee default (zero teacher access to defaulter data)
- Batch coordinator (coaching) notified only that student's "access is restricted" — amount never revealed
- No "send the child home" instructions; student attends class regardless of fee status

### 7.2 Data Access Control
| Role | Access |
|---|---|
| Cashier | Own session only; no defaulter list |
| Class Teacher | No access |
| Batch Coordinator | Access restricted flag only (no amount) |
| Accountant | Full defaulter list for own branch |
| Principal | Full defaulter list for own branch |
| Finance Head | Full defaulter list all branches |
| Management / Owner | Full defaulter list all branches |
| Recovery Agent (external) | Name + amount + parent contact only (DPDPA minimised) |
| Auditor | Read-only; aging report + write-off register only |
| EduForge Platform Admin | Cross-tenant only for platform-level MIS (no PII without cause) |

### 7.3 Recovery Agent DPDPA Compliance
- Written consent from parent required before sharing data with third-party recovery agent
- Data Processing Agreement (DPA) between institution and recovery agent mandatory
- Data shared: student name, parent name, contact number, outstanding amount, overdue days
- Data NOT shared: Aadhaar, marks, attendance, medical records, class/section, other family details
- Recovery agent portal: separate login; read-only; limited fields; every access audit-logged
- Agent access auto-expires: 90 days (configurable); must be renewed

### 7.4 Student Mental Health
- Financial stress flag: students with 60+ days default → counselor referral suggestion to Module 32
- System generates suggestion (not automatic referral): "Student [name] has been on fee hold for 60+ days.
  Consider a counselor check-in for financial stress."
- Principal/Counselor decides whether to act
- Referral is confidential; fee status not shared with counselor unless parent consents

### 7.5 WhatsApp Group Risk
- System has no "send to group" feature for defaulter communication — design-level prevention
- All defaulter communication = individual messages only
- Platform support team trained to never share defaulter lists via WhatsApp groups

---

## 8. Parent Communication & Counseling Escalation

### 8.1 Automated Communication Sequence
| Day | Type | Channel | Content |
|---|---|---|---|
| D+1 (grace end) | Soft reminder | WhatsApp + in-app | "Your fee of Rs. X was due. Pay now: [link]" |
| D+7 | Reminder with late fee notice | WhatsApp + in-app | "Rs. X overdue. Late fee of Rs. Y now accruing. Pay: [link]" |
| D+15 | Formal demand notice | WhatsApp + in-app + email | System-generated letterhead notice; due date warning |
| D+30 | Second formal notice | WhatsApp + email | Consequence statement; escalation warning |
| D+45 | Pre-legal notice | WhatsApp + email + registered post | "Legal action will be initiated if payment not received by [date]" |
| D+60+ | Legal notice (if approved) | Registered post + email | Lawyer-drafted; sent via Module 39 legal track |

### 8.2 Communication Moratorium
- During board exams (CBSE/State Board exam schedule): all automated escalation paused
- During final semester exams (college): automated escalation paused
- Manual communications (by Accountant/Principal) can continue at their discretion
- Moratorium dates loaded from Module 05 (Academic Calendar) and Module 19 (Exam Schedule)
- Hardship-flagged students: additional moratorium during hardship assessment period

### 8.3 Registered Post Tracking
- Notice sent via India Post registered post (AD — Acknowledgement Due)
- Tracking number logged against notice record
- Delivery confirmation: "Delivered" / "Refused" / "Not found" — entered by Accountant on receipt of AD card
- "Refused" status is legally equivalent to delivery in Indian court proceedings
- AD card scanned and stored in system (camera capture)

### 8.4 Parent Counseling Call Log
- Formal call from Accountant / Principal after D+15
- Call log fields: date, time, duration, called_by, parent_name, outcome, commitment_made, follow_up_date
- Outcome codes: COMMITTED_FULL_PAYMENT / COMMITTED_PARTIAL / REQUESTED_RESCHEDULING / HARDSHIP_CLAIMED / NO_ANSWER / DISPUTED / REFUSED
- Follow-up task auto-created in system based on commitment

### 8.5 Parent Visit Log
- Parent visits counter to discuss dues
- Visit record: date, visitor_name, relationship_to_student, conversation_summary, outcome, follow_up
- Documents received (income certificate etc.): logged with reference; Accountant reviews

### 8.6 Personalized Notice Generation
- Each notice is personalized: student name, class, admission number, fee head-wise breakdown,
  days overdue per head, late fee accrued, total payable, payment modes, payment link
- NOT a generic mass mailer — every parent receives their specific figures
- Available in English + Hindi (regional language options per institution config)

### 8.7 Bulk WhatsApp to a Class/Batch
- Accountant sends bulk reminder to all defaulters of a class/batch
- System sends individual WhatsApp messages (not group) — each parent sees only their own data
- Batch job: queued via SQS; sent at configured time (default: 10 AM IST weekdays)
- Unsubscribe from WhatsApp: parent can opt out of marketing messages; cannot opt out of
  statutory notices (formal demand notices are not marketing)

### 8.8 Financial Hardship Assessment
- Triggered by: parent's hardship claim during counseling call / visit / in-app request
- System generates hardship assessment form (digital; parent fills in-app or at counter)
- Form collects: monthly household income, number of dependents, employment status,
  specific hardship event (job loss / medical / disaster), supporting documents
- Finance Head reviews; assigns hardship tier: MILD / MODERATE / SEVERE

### 8.9 Hardship Tier Effects
| Tier | Late Fee | Escalation | Recovery Plan | Legal Action |
|---|---|---|---|---|
| MILD | Accrues normally | Normal timeline | Optional rescheduling | Normal trigger |
| MODERATE | Accrued late fee waived | Timeline +30 days | Mandatory rescheduling offered | Delayed 60 days |
| SEVERE | All late fee waived | Timeline +60 days | Customised long plan | Suspended; NGO referral |

### 8.10 Hardship Appeal Workflow
```
Parent submits appeal (in-app or at counter)
       │
Accountant reviews; collects documents
       │
Finance Head assesses; assigns hardship tier
       │
Principal approves hardship tag + relief measures
       │
Committee review (if relief > Rs. 10,000): Principal + Finance Head + Management
       │
Committee decision stored; parent notified; relief applied
```
- Committee minutes: stored in system; accessible to auditors
- Appeal rejection: reason communicated to parent; right to re-appeal once

---

## 9. Government Welfare & Scholarship Recovery Support

### 9.1 Government Scheme Search for Hardship Cases
- System matches hardship-flagged students against applicable central + state schemes
- Matching criteria: student category (SC/ST/OBC/EWS/Minority), state, income, class/course
- Matching schemes displayed to Finance Head with application links and deadlines
- Schemes covered: NSP, PM-POSHAN, NMMS, Inspire, state-specific (AP, TS, Karnataka, MH etc.)

### 9.2 NGO Referral Database
- EduForge maintains state-wise database of NGOs providing education grants
- Finance Head can refer a SEVERE hardship student to relevant NGO
- Referral: system generates referral letter on institution letterhead with student details (with parent consent)
- NGO feedback: outcome tracked (grant approved / denied / pending)

### 9.3 OBC/SC/ST Reimbursement Recovery
- Student paid full fee; state reimbursement pending (Model A — institution reimburses state)
- Student's account shows dues until reimbursement received; but student is NOT a defaulter
- Flag: `SCHEME_REIMBURSEMENT_PENDING` — all escalation and consequences suppressed
- Reimbursement received → automatically adjusts student ledger in Module 25

### 9.4 Education Loan Suggestion
- For MODERATE hardship cases: system suggests education loan
- Generates fee demand letter for bank (in-app view; student submits to bank)
- Tracks: loan application status (parent updates); approved loan = Module 25 ELOAN payment

---

## 10. Recovery Mechanisms

### 10.1 Instalment Rescheduling
- Finance Head offers new payment schedule to defaulter
- Rescheduling entity: original_demand_id, new_schedule[], rescheduling_fee (if any), interest_rate, approved_by
- New demand dates created in Module 25; original demand archived
- No-interest rescheduling: for hardship cases (MODERATE/SEVERE)
- Interest-bearing rescheduling: for non-hardship defaults; rate configurable (default: 12% per annum simple)
- Compound interest: NOT configurable — Indian courts have held compound interest on educational fees is unfair
- Rescheduling fee: optional; Rs. 200–500 administrative charge (institution configures)

### 10.2 Recovery Plan — Formal Document
- Finance Head prepares recovery plan: instalment amounts, dates, mode, consequences of breach
- Parent signs digitally (in-app e-sign) or at counter (wet signature; scanned)
- Recovery plan stored in system; linked to student defaulter record
- Parent receives copy via WhatsApp

### 10.3 Recovery Plan Breach
- System checks recovery plan instalments daily
- Breach: instalment missed by 3 days → immediate escalation to next risk tier
- WhatsApp to parent: "Recovery plan payment of Rs. X was due on [date]. Immediate payment required."
- Finance Head alerted; escalation timeline reset

### 10.4 Recovery Plan Amendment
- Parent unable to meet recovery plan → requests amendment
- Finance Head approval required; reason documented
- Maximum 2 amendments per academic year (configurable); third amendment → legal escalation trigger

### 10.5 Settlement Offer
- Institution offers one-time reduced settlement (waive late fee + penalty; collect principal fully)
- Settlement offer: Finance Head proposes → Management approves → presented to parent
- Settlement entity: original_amount, late_fee_waived, penalty_waived, settlement_amount, offer_expiry
- Offer expiry: 15 days (configurable)
- Accepted settlement → settlement receipt + "Full and Final Settlement — No Further Claims" statement
- Difference (waived amount) → write-off entry in system

### 10.6 Debt Acknowledgment — Limitation Act Management
- Every part payment constitutes acknowledgment of debt (Limitation Act 1963, Section 18)
- Written acknowledgment letter: parent signs confirming outstanding amount; limitation clock resets
- PDC issued by parent: legally constitutes acknowledgment; limitation clock resets from PDC date
- System tracks: last acknowledgment date, limitation expiry date (3 years from last acknowledgment)
- Limitation alert: system flags dues approaching 3-year mark → prompts Finance Head to:
  (a) obtain fresh acknowledgment, OR (b) file suit, OR (c) initiate write-off

### 10.7 Security / Caution Deposit Adjustment
- Caution deposit / security deposit applied against dues on Finance Head + Principal approval
- Reduces outstanding; receipt generated in Module 25 (ADJUSTMENT type)
- If deposit > outstanding: excess refunded to parent (Module 25 refund workflow)
- Cannot apply deposit without parent's awareness; notification sent

### 10.8 Staff Ward Fee — Salary Deduction
- If staff member's ward's fee is unpaid: institution may deduct from staff salary
- Prerequisites: employment contract must have this clause; written consent from staff
- Deduction capped: maximum 30% of net salary per month (configurable; legal limit varies by state)
- TDS adjustment: deduction reduces salary; TDS (Form 16) recalculated accordingly
- Staff exit clearance: F&F (Full & Final) settlement blocked if ward's dues outstanding

### 10.9 Guarantor Recovery
- Coaching institutes often take guarantor signature at admission (parent + guarantor)
- Guarantor record: name, relationship, Aadhaar (encrypted), phone, address, signed consent form
- Guarantor contacted only after: 2 formal notices to primary parent fail; MEDIUM+ risk tier
- Guarantor communication: formal notice (not WhatsApp) with outstanding amount; request to pay
- Legal action against guarantor: same as against defaulting parent; filed simultaneously if needed

### 10.10 Agricultural Family — Harvest Schedule
- Rural institution config: "harvest schedule" enabled
- No escalation from August to October (Kharif pre-harvest)
- Recovery drive activated November (post-harvest); dedicated collection camp at institution
- System suppresses all automated escalation during configured moratorium months
- Accountant can still manually outreach during moratorium

### 10.11 Cash Flow Forecasting from Recovery
- Recovery commitments (plan instalments + settlement offers + scheme disbursements) → forecasted inflow
- Finance Head sees: expected recovery for next 30 / 60 / 90 days
- Comparison: committed vs actually received (recovery plan adherence rate)
- Useful for institution cash flow planning (payroll, vendor payments)

### 10.12 Bulk Rescheduling
- Finance Head selects a class/batch → reschedules all defaulters in one operation
- Common use: post-disaster, post-pandemic, post-board-exam season
- Individual rescheduling parameters applied uniformly; can be overridden per student

---

## 11. Legal Recovery

### 11.1 Section 138 — Negotiable Instruments Act (Cheque Bounce Criminal)
**Prerequisites (strictly time-bound):**
```
Step 1 — Cheque bounced (bank return memo received)
       │
Step 2 — Demand notice sent to drawer within 30 days of bounce
       │ (registered post + email; notice period = 15 days for drawer to pay)
       │
Step 3 — Drawer does not pay within 15 days of notice
       │
Step 4 — Criminal complaint filed in magistrate court within 30 days of notice expiry
       │ (total window: ~75 days from bounce date)
       │
Step 5 — Case tracking in system
```
- System tracks: bounce date, demand notice sent date, notice expiry date, complaint deadline
- Alert: 5 days before complaint deadline if payment not received
- Missed deadline = Section 138 complaint cannot be filed (jurisdiction lost permanently)

### 11.2 Section 138 Case Register
| Field | Content |
|---|---|
| Case number | Magistrate court case number |
| Court | Court name + location |
| Complainant | Institution name + authorized signatory |
| Accused | Parent/guardian name |
| Cheque details | Number, date, bank, amount |
| Filing date | Date of complaint |
| Next hearing | Auto-reminder 2 days before |
| Advocate | Name + contact |
| Current status | Filed / Summons issued / Contested / Settled / Convicted / Acquitted |
| Outcome | Final disposition |

### 11.3 Pre-Litigation Notice (Civil Money Recovery)
- Before filing civil suit: formal demand notice (optional but recommended)
- Some states require Section 80 CPC notice (2 months before suit against government institutions)
- System generates: notice on institution letterhead; sent via registered post + email
- Notice-to-suit period tracked; suit filed only after notice period expires

### 11.4 Civil Money Suit
- Jurisdiction: Limitation Act — 3 years from date of default (or last acknowledgment)
- Small claims (≤ Rs. 1 lakh): District Consumer Disputes Redressal Commission (DCDRC)
  - Education is a "service"; parent can also file here against institution
  - Faster resolution: 90–180 days typically
  - Lower legal cost
- Large claims (> Rs. 1 lakh): District Court civil suit (money recovery)
  - Longer timeline: 1–3 years
  - Requires lawyer; court fees = percentage of claim amount

### 11.5 Civil Suit Register
| Field | Content |
|---|---|
| Suit number | Court-assigned |
| Court | District Court / Consumer Forum + location |
| Plaintiff | Institution |
| Defendant | Parent/guardian |
| Claim amount | Principal + interest + legal costs |
| Filing date | |
| Next hearing date | Auto-reminder 2 days before |
| Advocate | Name, enrollment number, contact |
| Current status | Filed / Served / Contested / Ex-parte / Decree / Appeal |
| Decree amount | If decree obtained |
| Execution status | Attachment order / recovery status |

### 11.6 Decree Tracking & Execution
- Favorable decree obtained → execution petition filed
- Execution tools (Indian civil law): attachment of bank account, moveable/immoveable property
- System flags: decree_obtained = TRUE → TC hold becomes absolute (no override possible)
- Partial recovery via execution: amount recovered posted to Module 25 ledger; outstanding updated
- Decree satisfaction: full recovery → decree satisfied; all holds lifted; student status restored

### 11.7 Lok Adalat Settlement
- NALSA (National Legal Services Authority) organizes Lok Adalat for pre-litigation or pending matters
- Advantages: free; legally binding; no appeal; fast (one sitting); relationship preserved
- Finance Head prepares settlement offer before Lok Adalat: principal amount + minimum late fee
  (waive penalties); Management pre-approves settlement band (minimum acceptable amount)
- System generates: case summary + settlement offer document for Finance Head to carry
- Settlement reached: amount paid (cheque/NEFT on the day); receipt issued; case closed; award stored
- Lok Adalat award stored in system; treated as decree for TC release purposes

### 11.8 Revenue Recovery Act (Government / Aided Institutions)
- Some states allow government-aided institutions to recover dues via Revenue Recovery Act
- Mechanism: district collector issues certificate; recovery through tehsildar (like revenue arrears)
- Applicable states: Andhra Pradesh, Telangana, Tamil Nadu, Kerala, Maharashtra (partially)
- System generates: Revenue Recovery Certificate in prescribed state format
- Finance Head submits to district education officer → district collector

### 11.9 Arbitration
- Private institutions with arbitration clause in admission form
- Arbitration: faster than court; legally binding award
- System tracks: arbitrator name, arbitration center, filing date, hearing dates, award

### 11.10 Consumer Forum — Dual Sword
- Institution files against parent: for fee recovery (education = service)
- Parent can ALSO file against institution: for harassment, unfair practices during recovery
- System alert: if institution's communication is escalating (e.g., multiple notices in short period),
  Finance Head reminded of consumer forum exposure from parent side

### 11.11 Legal Cost Register
| Cost Type | Tracked |
|---|---|
| Advocate retainer / case fee | Per case |
| Court filing fee | Per case |
| Process server fee | Per notice served |
| Registered post cost | Per notice |
| Lok Adalat filing fee | Nil (free) |
| Execution petition fee | Per petition |
| Total legal cost per case | Calculated |
| Cost per rupee recovered | KPI: total legal cost / total recovered |

### 11.12 Limitation Act — 3-Year Clock Management
- Limitation Act 1963: money recovery suit must be filed within 3 years
- Clock starts: from date of default (first missed due date after grace period)
- Clock resets: on any part payment OR written acknowledgment OR fresh PDC
- System tracks: limitation_start_date, last_reset_date, limitation_expiry_date
- Alert: 6 months before expiry → Finance Head must act (file suit or get acknowledgment or write off)
- Alert: 1 month before expiry → URGENT flag; daily reminder to Finance Head
- Expired limitation: debt is time-barred; suit cannot be filed; move to write-off or voluntary payment only

### 11.13 Hearing Date Management
- All court hearings (Section 138, civil suit, consumer forum, arbitration) in one calendar
- Alert: Finance Head + legal team 2 days before each hearing
- Post-hearing: Accountant / Finance Head updates hearing outcome; next date logged
- Missed hearing (institution side): adjournment recorded; cost implications noted

---

## 12. Special Case Handling

### 12.1 Student Death
- Death certificate submitted to institution
- Automatic actions:
  1. All academic consequences lifted immediately
  2. Debt forgiveness initiated (Finance Head approval)
  3. All recovery communication stopped
  4. Write-off approval workflow started
- Caution/security deposit: refunded to bereaved family with condolence letter
- Outstanding waived: Finance Head + Management approval; write-off entry; reason = "Student death"
- Institution policy can be configured: full waiver vs 50% waiver vs full recovery from estate (default: full waiver)

### 12.2 Parent / Primary Earner Death
- Surviving parent submits death certificate
- Actions: compassionate deferral (minimum 6 months); escalation clock paused; hardship tier → SEVERE
- Recovery plan: offered after 6 months; long-term; no interest; no late fee
- Legal action: suspended indefinitely; Finance Head review every 6 months

### 12.3 Force Majeure (Natural Disaster / Pandemic)
- Bulk force majeure flag: Finance Head selects affected student cohort + applies flag
- Effects: all escalation suspended; late fee accrual stopped; academic consequences lifted
- State government relief: system coordinates tracking of state relief disbursement
- Recovery resumes: when Finance Head removes force majeure flag (after state-declared relief period ends)
- COVID-type scenario: government orders may mandate specific relief; system enforces

### 12.4 Migrant Family (Relocated Mid-Year)
- Family relocated; student may have withdrawn or is attending school elsewhere
- Contact update workflow: Accountant attempts contact via all channels; logs attempts
- If student received TC: TC fee hold = waived if contact genuinely lost
- Outstanding: remains on record; limitation clock runs; write-off after 5 years if irrecoverable

### 12.5 Multi-Year Alumni Defaulter
- Student graduated with outstanding dues; now an alumnus
- Outstanding maintained in system indefinitely (until limitation expiry or write-off)
- Alumni contact: via alumni association / LinkedIn / registered mobile
- Alumni payment portal: graduate can pay old dues via special link (no institutional login required)
- Alumni dues: not counted in current-year defaulter reports; separate "alumni outstanding" report

### 12.6 Institution Closure / Merger
- If institution closes: advance fee deposits must be refunded (regulatory obligation)
- System generates refund list for state regulatory submission
- Outstanding dues: institution's right to collect survives; transferable if institution is acquired
- Merger: student outstanding ledgers migrate to acquiring institution's system

---

## 13. Write-Off & Bad Debt Provisioning

### 13.1 Write-Off Eligibility
- Institution configures eligibility criteria:
  - Dues older than X years (default: 5 years) AND all recovery attempts exhausted, OR
  - Amount below Rs. Y (default: Rs. 500) — not worth pursuing, OR
  - Student death (immediate eligibility), OR
  - Court judgment against institution (ordered to write off), OR
  - Lok Adalat settlement (difference between original and settled amount)

### 13.2 Write-Off Approval Chain
| Amount | Approval Chain |
|---|---|
| ≤ Rs. 5,000 | Finance Head self-approves |
| Rs. 5,001 – Rs. 50,000 | Finance Head → Management |
| Rs. 50,001 – Rs. 5,00,000 | Finance Head → Management → Board of Trustees |
| > Rs. 5,00,000 | Finance Head → Management → Board of Trustees → EduForge escalation flag |

### 13.3 Write-Off Accounting Entry
```
Dr  Bad Debt Expense (P&L)           Rs. X
    Cr  Student Fee Receivable        Rs. X
    (Removes from outstanding; hits income statement as expense)
```
- Tax treatment: bad debt expense is allowable deduction under Income Tax Act (business expense)
- GST note: no GST reversal on write-off (GST was paid on invoice date; write-off does not reverse GST)
- For coaching: if write-off is within same GST year and before GSTR-9, credit note may be issued

### 13.4 Bad Debt Provision (Accounting Standard)
- Institutions should provision for expected bad debts (matching principle)
- Default provisioning rates by aging bucket (institution can modify):

| Aging | Provision Rate |
|---|---|
| 0–30 days | 0% |
| 31–90 days | 5% |
| 91–180 days | 15% |
| 181–365 days | 30% |
| 1–2 years | 60% |
| 2–3 years | 80% |
| 3+ years | 100% |

- Provision entry:
  ```
  Dr  Provision for Bad Debts (P&L)
      Cr  Provision Account (Balance Sheet contra-asset)
  ```
- Provision report: generated quarterly for Finance Head + CA review

### 13.5 Write-Off Register
- Immutable record; append-only
- Fields: student_id, student_name, class, academic_year, amount_written_off, original_due_date,
  write_off_date, reason_code, approved_by, approval_chain, notes
- Reason codes: STUDENT_DEATH / IRRECOVERABLE_5YR / BELOW_THRESHOLD / COURT_ORDER / LOK_ADALAT /
  HARDSHIP_COMPASSIONATE / INSTITUTION_ERROR / FORCE_MAJEURE
- Exportable for CA audit; 7-year retention

### 13.6 Write-Off Reversal (Recovery After Write-Off)
- Student returns and voluntarily pays after write-off (rare but occurs)
- Reversal entry:
  ```
  Dr  Cash / Bank
      Cr  Bad Debt Recovery (P&L — separate income line)
  ```
- Receipt issued in Module 25 with historical academic year reference
- Write-off record NOT deleted — annotated with "Recovered on [date], Receipt No. [XXX]"

### 13.7 Partial Write-Off
- Common in Lok Adalat settlements: institution waives late fee + penalty; collects principal
- Late fee written off: smaller write-off entry
- Principal collected: receipt issued in Module 25
- Full and final settlement receipt: "No further claims by either party"

---

## 14. Compliance & Regulatory

### 14.1 Limitation Act 1963 Summary for Finance Team
- 3-year limitation for money recovery in civil court
- Starts: date of default
- Resets: any part payment OR written acknowledgment OR fresh cheque
- Expires: if no suit filed and no reset within 3 years → debt is time-barred
- Time-barred debt: still owed morally; cannot be enforced by court; move to voluntary collection only
- DO NOT write off immediately on limitation expiry — wait for policy review

### 14.2 Consumer Protection — Dual Risk
- Institution is service provider; parent is consumer under Consumer Protection Act 2019
- Institution can file: for fee recovery (Section 35 — District Commission)
- Parent can file: for any harassment, unfair trade practice, denial of service
- System ensures communication is measured, documented, and never harassing
- "Harassment" risk: more than 2 unsolicited contact attempts per week (WhatsApp/call) may be
  construed as harassment; system limits automated contacts per week

### 14.3 AICTE / UGC Student Grievance Cell
- If parent complains to AICTE / UGC student grievance cell about fee recovery pressure
- Institution receives complaint forwarding within 30 days (regulatory norm)
- System generates response package: communication log, notices sent, hardship assessment,
  recovery plan offered — submitted to regulator
- SLA: institution must respond to regulator within 30 days

### 14.4 State Fee Regulatory Authority (FRA)
- FRA can order institution to revise demands or penalties (states: MH, TN, KA, AP, TS, RJ)
- FRA order stored in system; all affected demands revised accordingly
- Late fee cap: many FRAs cap late fee at 2% per month; system enforces cap per state config

### 14.5 RTI Compliance (Government Institutions)
- RTI applicants can ask for: total number of fee defaulters, total outstanding amount (aggregate)
- Names of defaulters are EXEMPT from RTI disclosure (personal information — Section 8(1)(j))
- System generates RTI response report: aggregate numbers only; no individual names

### 14.6 CBSE Inspection Compliance
- CBSE can ask for fee defaulter handling policy during affiliation inspection
- System generates policy document from institution configuration settings
- Policy covers: grace period, escalation timeline, no-embarrassment policy, write-off criteria

### 14.17 DPDPA 2023 — Defaulter Data
- Outstanding fee data is financial personal data — sensitive category under DPDPA
- Processing for recovery = legitimate interest (contractual obligation)
- Proportionality: only minimum data shared with recovery agents (Section 7.3 rules)
- Retention: financial records = 7 years (statutory); personal data beyond financial purpose deleted after 7 years
- Cross-border: no defaulter data shared with overseas entities without explicit consent (NRI recovery agents)

---

## 15. MIS & Reports

### 15.1 Daily Reports (Auto-Generated)
| Report | Audience | Content |
|---|---|---|
| New Defaulters Today | Accountant | Students who crossed grace threshold today |
| Escalation Due Today | Accountant | Students whose next notice is due |
| Legal Deadline Alert | Finance Head | Cases with upcoming limitation expiry / hearing dates |
| Recovery Plan Breach | Finance Head | Plans where instalment was missed |
| Hearing Calendar | Finance Head + Legal | Court hearings in next 7 days |

### 15.2 Weekly Reports
| Report | Audience | Content |
|---|---|---|
| Defaulter Aging Summary | Finance Head | Outstanding by 0–30 / 31–90 / 91–180 / 180+ days |
| Recovery Rate This Week | Finance Head | Amount recovered / amount outstanding |
| Communication Delivery Status | Accountant | WhatsApp delivered / read; email opened; registered post status |
| Hardship Cases Under Review | Finance Head | Pending assessments |

### 15.3 Monthly Reports
| Report | Audience | Content |
|---|---|---|
| Defaulter Portfolio Report | Finance Head + Management | Risk tier distribution; total outstanding; movement |
| Recovery Performance Report | Management | Recovered vs target; by branch; by class; by head |
| Provision for Bad Debts | Finance Head + CA | Aging-bucket provisioning; movement vs last month |
| Legal Cases Status | Finance Head | Active cases; outcomes; costs |
| Write-Off Register | Finance Head + Auditor | All write-offs this month; cumulative |
| Cash Flow Forecast | Finance Head | Expected recovery inflow next 30/60/90 days |
| Inter-Branch Defaulter Summary | Group Finance Head | Branch-wise outstanding + recovery rate |

### 15.4 Quarterly / Annual Reports
| Report | Audience | Content |
|---|---|---|
| Board of Trustees Report | Management + Trustees | Total outstanding; recovery rate; legal cases; write-offs; provision |
| Vintage Analysis | Finance Head + Auditor | Which academic year does outstanding belong to |
| Collection Efficiency Trend | Finance Head + Platform (Module 53) | % collected by D+0 / D+30 / D+60 / D+90 over past 12 months |
| Legal Cost Efficiency | Finance Head | Cost per rupee recovered via legal route |
| Default Pattern Analysis | Finance Head | Default by class / head / month / payment mode |
| Annual Write-Off Summary | Finance Head + CA | For Income Tax (bad debt deduction) |
| RTE Reimbursement Pending | Finance Head | Outstanding state government reimbursements |

### 15.5 Auditor-Specific Reports
- Read-only auditor access
- Aging analysis (full detail)
- Write-off register (full history)
- Provision account movement
- Recovery plan status
- Legal case register
- No access to individual communication logs or personal data beyond financial figures

---

## 16. Access Control

### 16.1 Role-Wise Permissions
| Action | Cashier | Accountant | Principal | Finance Head | Management | Legal Team | Recovery Agent |
|---|---|---|---|---|---|---|---|
| View defaulter list | ❌ | ✅ (own branch) | ✅ (own branch) | ✅ (all) | ✅ (all) | ✅ (assigned cases) | Limited only |
| Change defaulter status | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ |
| Send formal notice | ❌ | ✅ | ✅ | ✅ | ❌ | ✅ | ❌ |
| Create recovery plan | ❌ | Draft | Approve | ✅ | ✅ | ❌ | ❌ |
| Approve hardship tier | ❌ | ❌ | Approve | Assess + Approve | ✅ | ❌ | ❌ |
| File legal case | ❌ | ❌ | Recommend | Initiate | Approve | Execute | ❌ |
| Update legal case | ❌ | ❌ | ❌ | ✅ | ❌ | ✅ | ❌ |
| Approve write-off | ❌ | ❌ | ❌ | Initiate | Approve (tiered) | ❌ | ❌ |
| Override consequence | ❌ | ❌ | ✅ | ✅ | ✅ | ❌ | ❌ |
| View recovery agent portal | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ (read-only, limited) |
| View board report | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ |
| Export write-off register | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ |

---

## 17. Notifications Triggered by This Module

| Event | Recipient | Channel | Timing |
|---|---|---|---|
| Student enters OVERDUE | Parent | WhatsApp + in-app | D+1 after grace |
| Formal notice issued | Parent | WhatsApp + in-app + email | Per escalation schedule |
| Pre-legal notice issued | Parent | WhatsApp + email + registered post | D+45 |
| Recovery plan created | Parent | WhatsApp + in-app | Immediate |
| Recovery plan instalment due | Parent | WhatsApp | 2 days before |
| Recovery plan breach | Parent + Finance Head | WhatsApp + in-app | Day of breach |
| Hardship tier assigned | Finance Head | In-app | Immediate |
| Settlement offer created | Parent | WhatsApp + in-app | Immediate (with expiry date) |
| Settlement offer expiring | Parent | WhatsApp | 3 days before expiry |
| Academic consequence imposed | Parent | WhatsApp + in-app | Immediate |
| Consequence lifted | Parent | In-app | Immediate |
| Legal case hearing due | Finance Head + Legal | In-app | 2 days before |
| Limitation expiry approaching | Finance Head | In-app | 6 months before; 1 month before (urgent) |
| Write-off approved | Finance Head | In-app | Immediate |
| Write-off recovery received | Finance Head | In-app | On receipt (Module 25 trigger) |
| Student death — debt forgiveness | Finance Head | In-app | Immediate |
| Force majeure flag applied | Finance Head | In-app | Immediate |

---

## 18. Audit Trail & Retention

### 18.1 Immutable Log — Every Action
- Status changes, notices sent, calls logged, plan created, breach detected, legal filed, write-off approved
- Log fields: action_type, actor_user_id, actor_name, actor_role, student_id, amount, old_status,
  new_status, timestamp (IST), IP address, device_id, reason_text
- No log entry can be edited or deleted by any role including Platform Admin

### 18.2 7-Year Retention
- All defaulter records, communication logs, legal case records, write-off register
- Stored on Cloudflare R2 with immutable flag
- Legal hold: active legal cases → records preserved beyond 7 years until final legal resolution

### 18.3 CIBIL / Credit Bureau Clarification
- Educational institution fee default is NOT reported to CIBIL or any credit bureau
- This is unlike bank loans (which are CIBIL-reported)
- System generates parent-facing clarification: "Fee default at our institution does not affect your CIBIL score"
- Prevents panic-driven parent complaints and consumer forum filings

---

## 19. Architect's Strategic Recommendations

### 19.1 Default Prediction Before It Happens (Module 47 AI Feed)
Build a lightweight prediction model trained on historical data:
- Input features: payment day-of-month history, bounce count, NACH failure count, instalment number,
  fee head, amount vs income category, sibling default flag, seasonal pattern
- Output: probability of default in next 14 days (score 0–100)
- Weekly scoring run; top 20% risk students → Accountant action list
- Proactive WhatsApp at D-7 (before due date): "Your fee is due in 7 days. Pay early to avoid late fee: [link]"
- Expected impact: 30–40% reduction in actual defaults; direct reduction in Module 26 workload

### 19.2 Limitation Act Dashboard — Non-Negotiable
Finance teams consistently miss the 3-year limitation deadline — this causes irrecoverable loss.
Build a dedicated "Limitation Tracker" dashboard:
- Red zone: dues expiring in < 30 days → daily alert to Finance Head
- Amber zone: dues expiring in 30–180 days → weekly alert
- Green zone: dues expiring in 180+ days → monthly report
- One-click action: "Send acknowledgment request to parent" — generates WhatsApp + registered post notice asking parent to confirm outstanding amount (constitutes acknowledgment; resets clock)

### 19.3 Lok Adalat Calendar Integration
Lok Adalats are organized by NALSA/SLSA regularly (National Lok Adalat — quarterly; State — monthly).
Finance Head should be automatically reminded of upcoming Lok Adalats relevant to their district.
System should prepare "case pack" for each eligible defaulter (dues > Rs. 10,000, > 90 days):
settlement offer amount (pre-approved by Management), case summary, communication history.
Finance Head walks in prepared. Expected: 40–60% of Lok Adalat matters settled on first hearing.

### 19.4 Recovery as a Revenue Intelligence Signal
Default rate by class / batch / fee head / payment mode is the strongest signal of fee structure
design problems in Module 24. High default on transport fee → route pricing too high or route
quality poor. High default on lab fee → labs not functional, parents don't see value. High default
on hostel fee → hostel quality issues. Recovery data should flow to Module 53 (Platform Analytics)
and surface as actionable insights for institution management — not just a finance problem.

### 19.5 WhatsApp Payment Link in Every Notice
Every recovery notice (soft reminder, formal notice, pre-legal) must embed a one-click payment link
that opens directly to the student's outstanding amount in checkout. No login friction.
Parent receives WhatsApp: notice text → one tap → sees outstanding → pays in 30 seconds.
Conversion rate on payment-link-embedded notices is 3–5x higher than notices without links.
This is the single highest-ROI change to recovery workflows.
