# Module 28 — Hostel Management

## 1. Purpose

Module 28 owns the complete lifecycle of residential accommodation within EduForge institutions — from hostel block configuration and room allotment through daily mess operations, attendance, health monitoring, disciplinary tracking, and eventual checkout. It serves boarding schools, engineering colleges, medical colleges, coaching residential campuses, and polytechnics across India, each with different regulatory overlays (CBSE boarding norms, UGC/AICTE residential guidelines, Anti-Ragging Regulations 2009, POCSO 2012, FSSAI licensing, and state hostel welfare board rules).

The module integrates tightly with Module 07 (Student Profile), Module 24 (Fee Structure), Module 25 (Fee Collection), Module 11 (Attendance), Module 35 (Notifications), and Module 41 (POCSO Compliance) while maintaining strict data ownership boundaries.

---

## 2. Hostel Configuration & Typology

### 2.1 Hostel Setup Parameters

Each institution may operate multiple hostels. Every hostel is configured as an independent entity with its own room inventory, staff, mess, and accounts:

| Parameter | Options |
|-----------|---------|
| Hostel type | Boys / Girls / Mixed (UG only with separate floors) / Staff / PG / Research Scholar |
| Affiliation level | Institutional / University-mandated / Government-subsidised |
| Residential model | Full boarder / Day boarder / Weekend boarder / Home-stay registered |
| Capacity | 10 to 5,000 beds |
| Mess model | Centralised / Block-wise / Tuck-shop + centralised hybrid |
| Warden structure | Chief Warden → Block Warden → Floor Warden → Resident Student Advisor |

### 2.2 Institution Type Mapping

| Institution Type | Hostel Applicability |
|-----------------|---------------------|
| Residential School (CBSE/ICSE) | Mandatory; gender-separate blocks; POCSO wall separation |
| Engineering College (AICTE) | Optional but common; Anti-Ragging Committee per hostel |
| Medical College (MCI/NMC) | Mandatory for 85%+ students; 24×7 duty doctor room |
| Coaching (Residential) | All students boarders; mess critical for retention |
| Polytechnic | Government-run hostels; fee subsidised; SC/ST reservation 60% |
| University Campus | Research scholars + PG + UG; multiple hostel categories |
| Deemed University | UGC 2016 norms apply; warden qualifications defined |

### 2.3 Regulatory Framework Index

| Regulation | Key Obligation |
|-----------|----------------|
| UGC (Prevention, Prohibition and Redressal of Sexual Harassment) 2015 | ICC formation; complaint register |
| Anti-Ragging Regulations 2009 | Affidavit per student; complaint cell; CCTV mandate |
| POCSO 2012 (for under-18) | No male staff in girls' hostel after 8 PM; mandatory CRC |
| FSSAI Food Safety and Standards Act 2006 | Mess licence; hygiene audit; pest control certificate |
| UGC Hostel Development Fund Guidelines 2022 | Norms for room area, common room, grievance board |
| State Fire Safety Act | NOC; fire drill twice per year; extinguisher log |
| State Hostel Welfare Board (SC/ST/OBC) | Scholarship-linked hostel fee waiver processing |
| National Building Code 2016 | Emergency exit, ramp, lift norms for new hostels |

---

## 3. Room & Bed Inventory Management

### 3.1 Room Hierarchy

```
Hostel Block
  └── Floor
        └── Room
              └── Bed / Bunk / Cot
```

### 3.2 Room Master Configuration

Each room record carries:

| Field | Detail |
|-------|--------|
| Room number | Alphanumeric; block-prefixed (e.g., A-203) |
| Room type | Single / Double / Triple / Dormitory (4–8) / Suite |
| Bed count | 1 to 12 |
| Room area (sq ft) | UGC norm: 9.5 sq m per person |
| Attached toilet | Yes / No / Shared on floor |
| AC status | AC / Non-AC / AC-optional (unit owned by student) |
| Fee tier | Links to Module 24 hostel fee component |
| Amenities checklist | Bed, mattress, pillow, study table, chair, wardrobe, reading lamp |
| Accessibility | Wheelchair accessible flag; ground-floor preference |
| Special designation | Warden room / Medical isolation / Anti-ragging patrol area |

### 3.3 Occupancy Status Engine

Every bed carries a real-time status:

- **Vacant** — available for allotment
- **Allotted** — student assigned, not yet checked in
- **Occupied** — student present
- **Reserved** — held for late joiner or transfer
- **Under maintenance** — bed/room not usable
- **Quarantine** — medical isolation flag
- **Blocked** — permanently out of service

Occupancy dashboard auto-refreshes; colour-coded grid view (green/yellow/red) for warden.

### 3.4 Room Allotment Logic

**Priority rules (configurable per institution):**

1. Reserved category (SC/ST/OBC/EWS) — mandatory block allocation where government hostel norms require
2. Distance from hometown > 200 km priority
3. Academic rank (merit-based in coaching hostels)
4. Special needs / medical requirement
5. Sibling preference (same block, same floor)
6. First-come-first-served among equal-priority applicants

**Allotment engine:**

- Auto-suggest optimal room based on gender, batch, priority, preferences
- Manual override by warden with reason logging (audit trail)
- Bulk allotment via CSV upload for new academic year
- Waitlist queue — auto-allot when vacancy opens
- Room-mate compatibility: same course year, same gender, compatible sleep-schedule tags

### 3.5 Room Change Requests

Student initiates room change request → warden reviews → approved/rejected with reason. Change history logged (max 2 changes per term, configurable). Reason codes: medical, academic, conflict, special need, family request.

---

## 4. Admission & Documentation

### 4.1 Hostel Admission Workflow

```
Student applies for hostel (in-app form)
  → Eligibility check (enrolled student, fee not defaulted, no disciplinary bar)
  → Room preference captured (room type, floor, roommate request)
  → Priority score calculated
  → Room allotted
  → Admission letter generated (in-app; PDF-downloadable)
  → Documents collected
  → Physical check-in recorded
  → Parent notification sent
```

### 4.2 Document Checklist

| Document | Mandatory | Notes |
|----------|-----------|-------|
| Anti-ragging affidavit (student) | Yes | UGC 2009; re-signed each year |
| Anti-ragging affidavit (parent) | Yes | UGC 2009 |
| Medical fitness certificate | Yes | Renewed annually |
| Undertaking — hostel rules | Yes | Signed in-app with timestamp |
| Bonafide certificate | For govt-scholarship students | Auto-generated from Module 07 |
| Aadhaar (for scholarship hostel) | Yes | State welfare board requirement |
| Emergency contact form | Yes | Min 2 contacts with relationship |
| Blood group declaration | Yes | Stored in health profile |
| Insurance nominee form | For MCI colleges | Stored in staff/student profile |

Document status dashboard: pending / uploaded / verified. Warden cannot confirm check-in until all mandatory documents are in status = verified.

### 4.3 Local Guardian Registration

Students (especially minors) must register a local guardian:
- Name, relationship, phone, address
- Aadhaar or ID proof linkage
- Authorised for emergency pickup (POCSO-compliant)
- Outpass issuance limited to registered guardians

### 4.4 Student Undertaking System

Digital undertaking covers: hostel rules, mess timings, curfew, visitor policy, no-smoking/drinking, anti-ragging pledge, property damage liability, CCTV acknowledgement. Timestamped, IP-logged, stored immutably.

---

## 5. Mess & Dining Management

### 5.1 Mess Structure Options

| Model | Description |
|-------|-------------|
| Fully managed | Institution-run; contractor cooks; monthly audit |
| Mess contractor | Private caterer; FSSAI licensed; contract renewed annually |
| Student mess committee | Self-managed; committee elected; accounts audited quarterly |
| Hybrid | Breakfast/dinner institutional; lunch outsourced |
| Tuck-shop + centralised | Light meals from canteen; main meals centralised |

### 5.2 FSSAI Compliance Tracking

- FSSAI licence number stored; renewal alert 90/60/30 days before expiry
- Hygiene audit log: monthly inspection by FSSAIs designated officer
- Pest control certificate: quarterly; uploaded in-app
- Water quality test: monthly; TDS + bacterial count logged
- Food safety officer visit log with findings and action-taken
- Menu must be displayed 7 days in advance (FSSAI Food Safety in School Guidelines)

### 5.3 Menu Planning Engine

Weekly rotating menu (configurable cycle: 7, 14, 21, 28 days):

| Meal | Timing (default) | Components |
|------|-----------------|-----------|
| Breakfast | 07:00–09:00 | Main item + accompaniment + beverage |
| Lunch | 12:30–14:30 | Dal/Curry + Rice/Chapati + Salad + Dessert (Sunday) |
| Evening snack | 17:00–18:30 | Light snack + tea/coffee |
| Dinner | 19:30–21:00 | Main item + Rice/Chapati + Salad + Curd |

- Regional menu support: North Indian / South Indian / Bengali / Gujarati bases
- Special meal flags: vegetarian-only campus, Jain option, diabetic meal, allergy-tagged meals
- Festival special meals logged with extra cost approval
- Calorie count per meal (optional; enabled for medical colleges)

### 5.4 Meal Pre-booking System (Strategic Feature)

Students mark expected absence 24 hours before meal → mess produces exact quantity → food wastage reduced 25–40%:

- App-based meal toggle per slot (Breakfast / Lunch / Snack / Dinner)
- Default = booked; student opts out
- Mess manager sees real-time headcount per meal slot
- Biometric/QR-based meal entry validation (prevents proxy)
- Monthly meal count per student reported to accounts for per-meal billing (where applicable)
- Skip statistics: auto-flag students skipping >5 consecutive meals for welfare check

### 5.5 Mess Fee Models

| Model | How it works |
|-------|-------------|
| Flat monthly mess charge | Fixed per month; no per-meal tracking |
| Per-meal deduction | Student pre-booked meals billed; skipped = not billed |
| Mess deposit + drawdown | Advance collected; consumed from balance |
| Mess committee subscription | Committee collects; institution has no direct billing role |

Mess fee integrates with Module 24 (fee component) and Module 25 (collection).

### 5.6 Mess Feedback System

Post-meal feedback (in-app, 1 tap): rating (1–5 stars) per meal + optional comment. Weekly aggregated report to mess manager + warden. Persistent low-rated items flagged for menu change. Monthly mess committee meeting minutes recorded.

### 5.7 Special Dietary Requirements

- Allergy profile per student (peanut, gluten, lactose, egg, shellfish)
- Medical diet flag (diabetic, hypertension, post-surgery)
- Religious dietary requirement (vegetarian, no beef, halal, Jain)
- Allergy alert visible to mess manager; colour-coded tray sticker option
- Severe allergy → auto-flag to hostel health room

---

## 6. Attendance & Movement Control

### 6.1 Hostel Attendance (Roll Call)

Distinct from academic attendance (Module 11). Hostel attendance is residential presence:

| Roll Call | Time | Method |
|-----------|------|--------|
| Morning roll call | 06:30–07:00 | Floor warden marks in-app |
| Night roll call | 10:00–10:30 PM | Floor warden marks; auto-absent after curfew |
| Gate exit scan | On exit | QR / RFID tap at gate |
| Gate entry scan | On return | QR / RFID tap; timestamp |

### 6.2 Outpass & Leave Management

**Outpass types:**

| Type | Duration | Approval Chain | Parent Notification |
|------|----------|---------------|---------------------|
| Day pass | Same day, return before 9 PM | Floor warden | SMS/app alert |
| Night pass (weekend) | Fri–Sun | Block warden → Chief warden | SMS/app + confirmation |
| Emergency pass | Immediate; any day | Chief warden override | Immediate alert |
| Medical leave | As per doctor | Health room + Chief warden | Alert + updates |
| Semester break | Academic calendar-linked | Auto-generated | Auto-notification |
| Temporary suspension leave | Disciplinary | Principal + Chief warden | Formal letter via app |

**Outpass workflow:**
Student raises request in app → selects type → guardian contact auto-verified → warden approves → gate QR generated → student scans at exit → return scan closes outpass → overstay alert if not returned within window.

### 6.3 Curfew & Overstay Management

- Curfew time configurable per hostel type (girls: 7:30 PM school / 9 PM college; boys: 10 PM typical)
- Auto-alert to warden + parent when student not returned by curfew − 30 minutes
- Overstay escalation: Warden → Chief Warden → Parents → Security
- Repeated overstay (3+ times) → disciplinary flag → Module 41 / student conduct record
- Emergency override: warden can suspend curfew alert for authorised late return

### 6.4 Visitor Management

- All visitors must be registered at gate with ID proof
- Visitor types: Parent / Registered guardian / Friend (restricted hours only) / Official visitor
- Female visitors in boys' hostel: common room only; time-limited (10 AM–5 PM)
- Male visitors in girls' hostel: strictly prohibited inside residential area (POCSO-compliant)
- Visitor log: name, ID type, ID number, visited student, entry/exit time, purpose
- Blacklist flag: warden can bar a visitor; alert on attempted re-entry
- Minor visitor rule: accompanied by registered parent/guardian only

### 6.5 CCTV Integration Metadata

Module 28 does not store video (separate security system). It does store:
- CCTV camera location register (entry gate, corridors, common areas, mess hall)
- Incident timestamp (when flagged) → security team notified to pull footage
- Footage pull request log (who requested, for which incident, time range)
- CCTV maintenance log: last tested, next test due

---

## 7. Student Well-being & Health

### 7.1 Health Room Configuration

Each hostel (or cluster of hostels) maintains a health room:

| Setup | Details |
|-------|---------|
| Nurse on duty | 24×7 for medical colleges; 7 AM–10 PM for others |
| Doctor availability | Panel doctor visits: 3× per week (min); 24×7 for medical college |
| First aid kit | Checklist; monthly audit of contents |
| Emergency medicines | Institution pharmacist approval; controlled drug register |
| Sick bay beds | Min 2% of hostel strength |
| Ambulance tie-up | Empanelled hospital + ambulance number displayed at gate |

### 7.2 Health Visit & Sick Leave Recording

- Student walks into health room → nurse records visit in-app
- Symptoms noted; treatment given; medicines dispensed
- Sick bay admission: room allotted; academic attendance auto-excused (integration with Module 11)
- Medical leave issued → outpass auto-generated → parent notified
- Referral to empanelled hospital: referral letter generated in-app
- Hospital admission → warden + parent + guardian notified immediately

### 7.3 Well-being Score (Strategic Feature)

A composite well-being index per student computed weekly:
- Attendance regularity (20%)
- Meal skip rate (15%)
- Sleep pattern (reported lights-out compliance) (10%)
- Health room visits (15%)
- Outpass frequency anomaly (10%)
- Academic performance trend (15%) (from Module 21)
- Disciplinary incidents (15%)

Score: 0–100. < 60 triggers pastoral care intervention. Counsellor (Module 32) assigned. Parent briefed. Trend chart visible to Chief Warden only.

### 7.4 Mental Health & Counselling

- Counsellor name and schedule visible to all hostel students in-app
- Anonymous grievance submission option (for mental health concerns)
- Peer support group session log (group name, date, facilitator, attendance)
- Stress event calendar: exam period, result day → proactive check-in by counsellor
- Critical incident flag (suicide ideation, self-harm report) → immediate principal + counsellor + parent escalation; Module 41 logged

### 7.5 Epidemic / Outbreak Management

- Cluster illness detection: 5+ students with same symptoms in 48 hours → epidemic alert
- Isolation room assignment: quarantine flag on selected rooms
- CMO / District Health Officer notification log
- Contact tracing: list of students who share mess batch / room / common area
- Return-to-hostel clearance: medical certificate required

---

## 8. Fee Structure & Finance

### 8.1 Hostel Fee Components (Links to Module 24)

| Component | Billing Frequency |
|-----------|------------------|
| Room rent | Monthly / Quarterly / Annual |
| Mess charges | Monthly (or per-meal where applicable) |
| Electricity charges | Monthly (metered or flat) |
| Maintenance deposit | One-time at admission; refundable at checkout |
| Hostel admission fee | One-time per enrolment |
| Laundry charges | Monthly (if institutional service) |
| Wi-Fi charges | Monthly (separate add-on) |
| Security deposit | One-time refundable |

### 8.2 Government Scholarship-Linked Fee Adjustment

- SC/ST/OBC/EWS hostel scholarship: fee waived or subsidised per state scheme
- Module 28 records scholarship type + sanctioned amount per student
- Net payable = gross fee − scholarship amount
- Scholarship disbursement delay → institution bears and adjusts when received
- Hostel welfare board reconciliation report: sanctioned vs received vs adjusted

### 8.3 Fee Defaulter Link to Module 26

- Outstanding hostel fee > 30 days → automatic flag in Module 26 (Fee Defaulters)
- Outpass restriction: configurable — restrict overnight passes for defaulters
- Mess access: never restricted (student welfare minimum — food always provided)
- Checkout clearance: Module 26 dues must be settled before final NOC issued

### 8.4 Refund on Early Exit

Refund policy (configured per institution):
- Mess charges: prorated to date of exit
- Room rent: prorated or full month (configurable)
- Admission fee: non-refundable
- Security deposit: refunded after room inspection clearance within 30 days
- Government scholarship: portion refunded back to welfare board if applicable

---

## 9. Discipline & Conduct

### 9.1 Incident Recording Framework

All disciplinary incidents recorded with:
- Date/time, reporter (warden/student/staff/CCTV flag)
- Incident type (see below)
- Students involved (accused + witness)
- Location (room number / common area / mess / gate)
- Description (free text, min 100 chars)
- Immediate action taken
- Evidence reference (CCTV timestamp if applicable)
- Hearing scheduled: date, panel members
- Outcome: warning / fine / suspension / expulsion / police complaint

### 9.2 Incident Type Taxonomy

| Category | Sub-types |
|----------|-----------|
| Anti-ragging | Physical ragging, verbal ragging, online ragging, forcing to perform acts |
| Substance abuse | Alcohol in room, smoking in campus, narcotics possession |
| Property damage | Room damage, common area damage, theft |
| Misconduct | Violation of curfew, unauthorised absence, bringing contraband |
| Sexual harassment | Unwanted advances, obscene material, molestation (POCSO/ICC) |
| Violence | Physical altercation, bullying, threatening behaviour |
| Food-related | Mess boycott, food waste, bringing outside alcohol |
| Safety violation | Tampering fire equipment, electrical hazard creation |
| Academic misconduct | Cheating in hostel-based study (rare; linked to Module 19) |

### 9.3 Anti-Ragging Compliance (UGC 2009)

- Anti-Ragging Committee: constituted per hostel; names + contact stored
- Anti-Ragging Squad: patrol schedule (daily patrol log)
- Helpline number (1800-180-5522) displayed in-app and on hostel notice board
- Incident report to UGC within 24 hours of confirmed ragging — log of submission with reference number
- Accused student: suspended from hostel pending enquiry; room blocked
- FIR filing: Chief Warden initiates; police contact logged
- Annual anti-ragging self-declaration by institution: due date alert

### 9.4 Disciplinary Hearing & Outcome

| Stage | Timeline | Action |
|-------|----------|--------|
| Complaint registered | Day 0 | Auto-alert to warden + student |
| Prima facie review | Day 1–2 | Chief Warden reviews; hearing called or dismissed |
| Show-cause notice | Day 3 | Student given written notice (in-app) |
| Hearing | Day 5–7 | Panel: Chief Warden + faculty + student rep |
| Order passed | Day 8–10 | Written order; penalty enforced; appeal rights stated |
| Appeal | Day 10–20 | Principal / Grievance cell hearing |
| Final order | Day 21 | Stored in student conduct record |

### 9.5 Fine & Penalty Collection

- Fine amount configured per incident type
- Fine amount added to student fee account → Module 25 collection flow
- Fine receipt issued; linked to disciplinary order
- Repeated offender (3+ incidents in semester) → mandatory counselling referral

---

## 10. Maintenance & Housekeeping

### 10.1 Asset Register per Hostel

Every room and common area has an asset list:

| Area | Assets Tracked |
|------|---------------|
| Student room | Bed frame, mattress, wardrobe, study table, chair, fan, AC unit, geyser |
| Bathroom | Water heater, exhaust fan, flush mechanism |
| Common room | TV, furniture, inverter, gym equipment |
| Corridor | Lighting, CCTV, notice board |
| Mess | Tables, chairs, serving counters, utensils |
| Kitchen | Cooking equipment, refrigerators, exhaust hoods |

Each asset: asset ID, purchase date, warranty expiry, last service date, condition (Good / Needs repair / Condemned).

### 10.2 Maintenance Request Workflow

Student or warden raises maintenance request in-app:
- Category: Electrical / Plumbing / Civil / Furniture / AC / Pest control / IT (Wi-Fi)
- Description + optional photo (camera capture)
- Priority: Low / Medium / High / Emergency
- Assigned to: maintenance staff or external vendor
- SLA: Emergency = 4 hours; High = 24 hours; Medium = 48 hours; Low = 7 days
- Status: Open → Assigned → In Progress → Resolved → Closed
- Student feedback on resolution quality (1–5 stars)
- Unresolved SLA breach → auto-escalate to Chief Warden

### 10.3 Housekeeping Schedule

- Daily cleaning schedule: room common areas (corridors, bathrooms, mess)
- Housekeeping staff attendance tracked via in-app check-in
- Deep cleaning schedule: monthly; room fumigation quarterly
- Linen change schedule: weekly (institutional beds) — log maintained
- Pest control: quarterly professional pest control; certificate stored

### 10.4 Predictive Maintenance Tracker (Strategic Feature)

- Age-based service alerts: AC serviced every 6 months; geyser checked annually
- Failure pattern detection: if 3+ similar repairs (e.g., geyser failures) in same block within 30 days → root cause alert → bulk replacement budget triggered
- Annual maintenance calendar auto-generated from asset ages and service histories

---

## 11. Check-out & Exit Management

### 11.1 Checkout Trigger Events

| Event | Action |
|-------|--------|
| End of academic year | Bulk checkout; semester-end date |
| Mid-year withdrawal | Student-initiated; warden approval |
| Transfer to another branch | NOC from hostel; re-allotment at receiving branch |
| Disciplinary expulsion | Immediate checkout; security escort logged |
| Medical emergency extended absence | Temporary checkout; room held or released |
| Graduate / pass-out | Auto-triggered after result publication |

### 11.2 Checkout Clearance Checklist

```
□ Room inspection: no damage / damage documented + fine raised
□ Asset return: all issued items returned (keys, library books, etc.)
□ Fee clearance: Module 26 — no outstanding dues
□ Mess dues: settled
□ Fine/penalty dues: settled
□ Library clearance: Module 30 — no pending books
□ ID card return
□ Anti-ragging departure declaration signed
□ Security deposit refund initiation: Module 25
□ NOC issued: digital, in-app
```

### 11.3 Room Inspection at Checkout

Warden conducts physical inspection:
- Checklist: walls (marks/damage), furniture condition, plumbing, electrical fittings
- Any damage: photographed (camera capture), assessed at replacement cost
- Damage charge raised → student fee account → Module 25 collection
- Deposit release: after all clearances, initiated within 30 days
- Pre vs post condition comparison if pre-check-in photos were taken

### 11.4 NOC & Departure Certificate

On full clearance:
- Hostel NOC generated (in-app, downloadable PDF)
- Content: student name, roll number, room allotted, period of stay, clearance confirmation
- Used for: college TC, scholarship closure, bank account KYC updates
- NOC revocable within 7 days if post-checkout damage found

---

## 12. Parent Communication & Transparency

### 12.1 Parent App Dashboard

Parents of hostellers see (read-only):
- Current room assignment (block, floor, room number)
- Last gate scan timestamp (entry/exit)
- Meal booking status for current day
- Outstanding hostel fee + payment link
- Recent disciplinary incidents (summary only; no peer names)
- Health room visits (date + reason category)
- Well-being score trend (last 30 days)
- Upcoming outpass requests awaiting approval

### 12.2 Notification Events to Parents

| Event | Channel | Timing |
|-------|---------|--------|
| Student exits hostel | SMS + app | On gate scan |
| Student returns | App notification | On return scan |
| Curfew breach | SMS + app | At curfew − 15 minutes if not returned |
| Sick bay admission | SMS | Immediate |
| Hospital referral | SMS + call attempt | Immediate |
| Outpass approved | App | On warden approval |
| Disciplinary incident | In-app formal letter | Within 24 hours |
| Fee due reminder | SMS + app | 7 days before due |
| Mess skip alert (5 consecutive) | App | Auto-trigger |
| Counsellor referral | App (confidential) | On referral |

### 12.3 Parent Visit Scheduling

- Parent books visit slot in-app (date + time preference)
- Warden confirms (or suggests alternative slot)
- Visitor pass auto-generated with QR code
- Gate scan on parent arrival logs the visit
- Visiting hours: institution-defined (typically 10 AM–5 PM on Sundays)
- Special cases (illness, emergency) — anytime with warden approval

---

## 13. Staff & Warden Management

### 13.1 Hostel Staff Roles

| Role | Responsibilities |
|------|----------------|
| Chief Warden | Policy, escalation, external compliance, budget |
| Block Warden | Block-level discipline, room allotment oversight |
| Floor Warden (Resident Faculty) | Daily roll call, immediate student issues |
| Resident Student Advisor (RSA) | Senior student peer mentor; anti-ragging squad |
| Mess Manager | Menu planning, contractor supervision, FSSAI compliance |
| Nurse | Health room, first aid, sick bay |
| Security Guard | Gate management, visitor log, CCTV monitoring |
| Housekeeping Supervisor | Cleaning schedule, pest control, linen |
| Maintenance Supervisor | Repair requests, asset register, contractor coordination |

### 13.2 Warden Duty Roster

- Weekly duty roster published in-app (visible to all wardens)
- Night duty warden: mandatory for all nights (rotating among block wardens)
- Night duty log: sign-in, rounds completed, incidents noted
- Warden absence: substitute assigned; no hostel left without duty warden
- Warden leave: must notify Chief Warden; auto-alert to replacement

### 13.3 Staff Training & Compliance

- POCSO mandatory training log: all hostel staff trained; certificate stored
- Anti-ragging sensitisation: annual; attendance logged
- Fire drill participation: twice per year; names logged
- First aid training: nurse + 2 wardens per hostel certified; certificate expiry tracked
- BGV (Background Verification) for all hostel staff: linked to Module 08

---

## 14. Regulatory Compliance Automation

### 14.1 Anti-Ragging Compliance Calendar

| Task | Frequency | Owner |
|------|-----------|-------|
| Affidavit collection | Each academic year | Warden |
| Committee constitution notification to UGC | Annual | Principal |
| Squad patrol log | Daily | RSA |
| Incident report to UGC | Within 24 hr of incident | Chief Warden |
| Annual self-declaration to UGC | June 30 each year | Principal |
| CCTV operational check | Monthly | Security |

All calendar items with due dates, responsible person, and completion flag. Overdue items escalate.

### 14.2 POCSO Compliance (Residential Context)

- Male staff restriction in girls' hostel: policy setting configurable; alert if male staff access logged after hours
- Child Reporting Certificate (CRC) training for all staff with minor students
- Mandatory reporting log: any POCSO-relevant incident must be logged within 24 hours; sent to DCPO
- Suspicious behaviour report: any student/staff can file anonymous report; routed to Principal + ICC
- POCSO register: maintained in-app; accessible to authorised DCPO only

### 14.3 FSSAI Compliance Tracker

- Licence number + expiry date; renewal alerts at 90/60/30/7 days
- Monthly hygiene inspection checklist (inspector name, date, findings, action-taken, resolved-by)
- Pest control schedule: due date alerts; certificate upload (camera capture)
- Water quality test log: monthly results (TDS, pH, bacterial count)
- Food complaint register: student-filed food quality complaints; resolution timeline
- FSSAI audit history: last 3 audit reports stored

### 14.4 Fire Safety Compliance

- Fire NOC: stored; renewal alert
- Fire extinguisher register: each unit (location, type, last refill, next service due)
- Fire drill log: date, duration, issues found, corrective actions
- Emergency exit map: per floor; last reviewed date
- Fire warden designation: per floor; training certificate date

### 14.5 UGC Hostel Norms Self-Assessment

Annual self-assessment checklist per UGC Hostel Development Fund Guidelines 2022:
- Room area compliance (9.5 sq m per person)
- Common room availability
- Sports facility availability
- Grievance board displayed and functional
- Warden qualifications met
- Annual hostel report submitted to university

---

## 15. SOS & Emergency Response

### 15.1 SOS Button (Strategic Feature)

In-app SOS button (always visible on hostel student's home screen):
- Single tap → sends GPS-stamped alert to: Chief Warden + nearest security guard on duty + parent
- Message: student name, room/last-known location, timestamp
- Warden app shows alert with response buttons: Responding / Need Police / Need Ambulance
- Auto-escalates to Principal if no warden response in 5 minutes
- SOS test drill mode (monthly drill; alerts suppressed but flow tested)
- False SOS log (3 false alarms → student counselling; 5 → disciplinary)

### 15.2 Emergency Response Protocol

| Emergency Type | First Contact | Escalation |
|---------------|---------------|------------|
| Medical | Nurse → Ambulance | Parent + Principal |
| Fire | Security → Fire department | All wardens + Principal + parents |
| Ragging | Chief Warden → Police | UGC complaint + Principal |
| Missing student | Chief Warden → Police (after 1 hr) | Parents + University registrar |
| Natural disaster | Security → Civil authorities | Evacuation protocol; parent alert |
| Bomb threat | Security → Police | Immediate evacuation; log |

Emergency contact board: stored in-app (police, fire brigade, ambulance, district hospital, DCPO, POCSO helpline, anti-ragging helpline).

---

## 16. Room Allocation Optimisation (Smart Allocation)

### 16.1 Allocation Dashboard

Chief Warden sees:
- Total rooms vs occupied vs vacant vs maintenance
- Occupancy % by block / floor / room type
- Gender-wise occupancy
- Course/batch-wise distribution
- Average beds per room type
- Waitlist count

### 16.2 Smart Allocation Engine (Strategic Feature)

At start of each academic year:
- Algorithm ingests: room inventory, student list, priorities (see §3.4), preferences
- Produces optimal allocation minimising: waitlist length, room-type over/under-use, cross-gender errors
- Output: draft allotment list → Chief Warden reviews → approves → bulk confirmation sent
- Warden can swap any pair before confirmation
- Re-run allocation after each approval batch (for rolling admissions)

### 16.3 Vacancy Bulletin

- Configurable: show available rooms + types to prospective students (during admission season)
- Room preference expressed before admission (preference stored; allotment post-admission)

---

## 17. Hostel Analytics & Reporting

### 17.1 Operational Reports

| Report | Frequency | Audience |
|--------|-----------|---------|
| Daily occupancy report | Daily | Chief Warden |
| Meal headcount vs served | Daily | Mess Manager |
| Outpass summary | Weekly | Chief Warden |
| Maintenance SLA compliance | Weekly | Maintenance Supervisor |
| Disciplinary incident log | Monthly | Principal |
| Health room visit summary | Monthly | Medical Officer |
| Well-being score distribution | Monthly | Chief Warden + Counsellor |
| Fee outstanding (hostel only) | Monthly | Accounts + Warden |
| FSSAI compliance status | Monthly | Chief Warden |
| Annual hostel performance report | Annually | Management + UGC |

### 17.2 Hostel Cost Per Student KPI (Strategic Feature)

Monthly cost breakdown per student:
- Mess cost per meal × meals served
- Staff salary allocation (warden, nurse, housekeeping, security) per bed
- Maintenance spend per student
- Utility cost per student (electricity, water)
- Total hostel operating cost per student per month

Benchmarked against: previous month, previous year same period, industry benchmark (₹4,000–₹12,000/student/month range for residential colleges).

Low-cost flag: if cost drops unusually → quality check triggered. High-cost flag: if cost spikes → budget review triggered.

### 17.3 Compliance Dashboard

Single-page view for Principal:
- Anti-ragging: affidavits collected % / incidents this year / UGC reports filed
- FSSAI: licence valid Y/N / last inspection date / open findings
- Fire safety: NOC valid Y/N / last drill date / extinguisher service status
- POCSO: staff trained % / incidents this year / CRC held by all staff Y/N
- Hostel self-assessment: UGC norms met % / last submission date

---

## 18. Integration Map

| Module | Integration |
|--------|------------|
| Module 07 — Student Profile | Student photo, blood group, emergency contact, course/batch |
| Module 08 — Staff Management | Warden profile, BGV status, staff attendance |
| Module 11 — Attendance | Sick bay absence auto-excused in academic attendance |
| Module 24 — Fee Structure | Hostel fee components defined here |
| Module 25 — Fee Collection | Hostel fee invoices, mess fee, fines collected through Module 25 |
| Module 26 — Fee Defaulters | Hostel outstanding fees flagged here |
| Module 30 — Library | Library clearance at checkout |
| Module 32 — Counselling | Well-being referral, mental health sessions |
| Module 35 — Notifications | All parent/student alerts routed through Module 35 |
| Module 41 — POCSO Compliance | Incidents logged; mandatory reporting flow |
| Module 42 — DPDPA & Audit Log | All PII access and incident logs audited |

---

## 19. Data Model (Key Tables)

```
hostels
  id, tenant_id, name, type, gender_type, block_count, total_beds,
  mess_model, fssai_licence_no, fssai_expiry, chief_warden_id,
  created_at, is_active

hostel_rooms
  id, hostel_id, block, floor, room_number, room_type, bed_count,
  area_sqft, attached_toilet, ac_status, fee_tier_id, status,
  accessibility_flag, created_at

hostel_beds
  id, room_id, bed_label, status, current_allotment_id

hostel_allotments
  id, student_id, bed_id, allotted_on, checked_in_at, checked_out_at,
  check_in_by, check_out_by, status, waitlist_rank, allocation_priority,
  room_change_count

hostel_outpass
  id, student_id, outpass_type, applied_at, departure_expected,
  return_expected, departure_actual, return_actual, approved_by,
  gate_exit_scan, gate_return_scan, status, guardian_contact_id,
  parent_notified_at

hostel_roll_call
  id, hostel_id, roll_call_type, roll_call_date, conducted_by,
  total_students, present, absent, on_leave, recorded_at

hostel_meal_bookings
  id, student_id, meal_date, meal_slot, status, scanned_at

hostel_mess_menu
  id, hostel_id, menu_date, meal_slot, menu_items, cycle_week,
  posted_by, posted_at

hostel_mess_feedback
  id, student_id, meal_date, meal_slot, rating, comment, submitted_at

hostel_incidents
  id, hostel_id, incident_date, incident_type, category, reporter_id,
  accused_student_ids, witness_ids, location, description, evidence_ref,
  hearing_date, outcome_type, fine_amount, order_date, appeal_filed,
  final_order_date, created_at

hostel_health_visits
  id, student_id, visit_date, nurse_id, symptoms, treatment,
  medicines_dispensed, sickbay_admission, referred_hospital,
  parent_notified, leave_issued_days, cleared_on

hostel_wellbeing_scores
  id, student_id, week_start, attendance_score, meal_skip_score,
  health_visit_score, outpass_anomaly_score, academic_score,
  discipline_score, composite_score, intervention_triggered,
  computed_at

hostel_maintenance_requests
  id, hostel_id, room_id, raised_by, raise_date, category, description,
  priority, assigned_to, sla_due, resolved_at, status, student_rating

hostel_checkout_clearances
  id, allotment_id, room_inspection_done, asset_returned, fee_cleared,
  mess_cleared, library_cleared, id_returned, deposit_refund_initiated,
  noc_issued_at, issued_by

hostel_documents
  id, hostel_id, document_type, reference_number, issue_date,
  expiry_date, alert_sent_30, alert_sent_60, alert_sent_90, status

hostel_fssai_audits
  id, hostel_id, audit_date, inspector_name, findings, action_taken,
  resolved_by, resolved_date, next_audit_due

hostel_visitor_log
  id, hostel_id, visitor_name, id_type, id_number, visited_student_id,
  entry_time, exit_time, purpose, approved_by, blacklisted

hostel_asset_register
  id, hostel_id, room_id, area_type, asset_name, asset_code,
  purchase_date, warranty_expiry, last_service_date, condition,
  next_service_due

hostel_sos_events
  id, student_id, triggered_at, location_lat, location_lng,
  alert_sent_to, warden_responded_at, resolution_type,
  is_test_drill, is_false_alarm
```

---

## Cross-Module References

- **Module 07**: Student profile (blood group, allergies, emergency contacts, course/batch) — read-only reference
- **Module 08**: Warden and hostel staff profiles, BGV status — read-only reference
- **Module 11**: Academic attendance excused when sick bay flag set — event-based integration
- **Module 24**: Hostel fee component definitions — read-only reference
- **Module 25**: Fee invoices, fine collection, deposit refund — write via Module 25 APIs
- **Module 26**: Hostel fee default flag passed to Module 26 — event-based
- **Module 30**: Library clearance status checked at checkout — read-only
- **Module 32**: Counselling referral created from well-being alert — write via Module 32 API
- **Module 35**: All parent/student notifications dispatched through Module 35 — write
- **Module 41**: POCSO incidents logged; mandatory reporting workflow — write
- **Module 42**: All PII access, incident creation, checkout events audited — write

---

*Module 28 complete. Next: Module 29 — Transport & GPS Tracking.*
