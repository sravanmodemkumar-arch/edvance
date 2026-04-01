# Module 31 — Admission & Enquiry CRM

## 1. Purpose

Module 31 owns the complete admission lifecycle within EduForge institutions — from first enquiry capture through lead nurturing, application processing, entrance test management, selection, offer letters, document verification, and final enrolment handover to Module 07 (Student Profile). It serves schools, colleges, coaching centres, and universities managing admission cycles across multiple courses, campuses, and quota categories.

The module aligns with RTE 25% reservation requirements, CBSE/ICSE age eligibility norms, AICTE/UGC approved intake limits, MCI/NMC seat matrix rules, state reservation rosters, and TRAI DND compliance for outbound communications. It integrates deeply with Module 07 (Student Profile), Module 03 (RBAC), Module 05 (Academic Calendar), Module 09 (Parent Portal), Module 10 (Timetable), Module 17 (Question Bank), Module 24–26 (Fees), Module 28–30 (Hostel/Transport/Library), Module 36 (WhatsApp), Module 37 (Email), and Module 42 (Audit Log).

---

## 2. Lead Capture & Enquiry Management

### 2.1 Enquiry Sources

Every lead record carries a source attribute. Sources supported:

| Source | Capture Method |
|--------|---------------|
| Walk-in | Front desk manual entry; counsellor notified immediately |
| Website form | API intake; UTM parameters auto-extracted |
| WhatsApp enquiry | Module 36 integration; message → lead auto-created |
| Inbound phone call | Counsellor logs call; missed call → lead from CLI |
| School fair / exhibition | Event tag; bulk import post-fair |
| Social media | Facebook / Instagram lead forms via webhook |
| Google Ads | UTM source=google; campaign + ad group stored |
| Referral (student/alumni) | Referring person's name + ID stored |
| Newspaper / print ad | Source tag on enquiry form |
| Third-party aggregator | CollegeDekho, Shiksha, Careers360 — bulk CSV import |

UTM parameters (source, medium, campaign, content, term) stored per lead for campaign attribution.

### 2.2 Lead Record

| Field | Detail |
|-------|--------|
| Name | Full name |
| Mobile | Primary; TRAI DND check before bulk SMS |
| Email | For brochure and offer letter |
| Parent name + mobile | Separate; critical comms sent to both |
| Course interested in | One or more; separate interest record per course |
| Class / standard | Applicable for school admissions |
| Current institution | Last school/college attended |
| City / district | For geographic analytics |
| Source | From source list above |
| UTM parameters | If web/ad source |
| Enquiry date | Date first recorded |
| Academic year | e.g., AY 2025–26 |
| Language preference | Hindi / Telugu / Tamil / English |
| Counsellor assigned | Auto-assigned on creation |
| Lead score | Auto-computed (see §2.4) |
| Status | Pipeline stage (see §2.3) |
| Competitor institutions | "Considering other options" — free text |
| Referral by | Referring student/alumni ID (if referral source) |

### 2.3 Lead Pipeline Stages

```
New → Contacted → Interested → Application Sent → Applied →
Docs Submitted → Interview Scheduled → Selected →
Fee Paid → Enrolled
                 ↓
            Cold / Lost (at any stage)
```

Stage transitions:
- Auto-advance: "Applied" when application submitted; "Fee Paid" on fee receipt; "Enrolled" on Module 07 creation
- Manual advance: counsellor moves lead through earlier stages
- Cold: no contact for 15+ days
- Lost: lead explicitly declined or opted for competitor; reason code stored

### 2.4 Lead Scoring

Composite score (0–100) computed on creation and updated on each interaction:

| Factor | Weight | Signal |
|--------|--------|--------|
| Source quality | 20% | Referral/walk-in = high; aggregator = medium |
| Engagement (calls, visits, messages) | 25% | More touchpoints = higher |
| Response rate | 20% | Picks up calls, replies to messages |
| Course fit | 15% | Eligibility met, entrance score if available |
| Geographic proximity | 10% | Within institution's primary catchment area |
| Recency of last interaction | 10% | Recent contact = higher |

Score bands: 80–100 = Hot; 50–79 = Warm; < 50 = Cold. Visible on counsellor dashboard with colour coding.

### 2.5 Duplicate Detection

On every new lead creation:
- System checks existing leads for same mobile number or same email
- If duplicate found: alert to counsellor — "Existing lead found: [Name], [Date]"
- Options: merge (combine communication history), link (keep separate but flag as same person), ignore
- Prevents multiple counsellors chasing same prospect; avoids double-counting in funnel

### 2.6 Missed Call & Walk-in Capture

**Missed call:** institution's enquiry line logs missed call with CLI → lead created with phone number + timestamp + "Missed call" tag → callback task auto-assigned to next available counsellor.

**Walk-in:** front desk registers visitor in-app (name, mobile, course interest, date/time) → counsellor notified immediately with walk-in flag → high-priority treatment (walk-in converts at 3× the rate of web leads).

### 2.7 Bulk Lead Import

Third-party aggregators provide lead files in CSV:
- Upload template: name, mobile, email, course, city, source, date
- Deduplication run before import; duplicates listed for review
- All imported leads tagged with aggregator name + import batch ID
- Cost per lead tracked against campaign spend for ROI calculation

---

## 3. Communication & Follow-up

### 3.1 Counsellor Dashboard

Counsellor's daily view:
- Today's tasks (follow-ups due, interviews, visits)
- Hot leads with no contact in 3 days (urgent)
- Applications awaiting review
- Overdue follow-ups (past due date)
- Today's walk-ins assigned
- Lead pipeline summary: count per stage

### 3.2 Call Logging

Every call (inbound or outbound) logged per lead:

| Field | Detail |
|-------|--------|
| Direction | Inbound / Outbound |
| Date + time | Auto-stamped |
| Duration | Seconds (manual entry or VOIP integration) |
| Counsellor | Who made/received the call |
| Outcome | Answered-Interested / Answered-Not interested / No answer / Callback requested / Wrong number / Disconnected |
| Notes | Free text; what was discussed |
| Next action | Task created automatically based on outcome |

Auto-task creation rules:
- No answer → follow-up task in 24 hours
- Callback requested → task at requested time
- Answered-Interested → send brochure; task in 3 days

### 3.3 Multi-Channel Communication

| Channel | Usage | Compliance |
|---------|-------|-----------|
| SMS | Short alerts, reminders | TRAI DND check before each send |
| WhatsApp | Brochures, rich messages, bot flow | HSM templates pre-approved; Module 36 |
| Email | Brochure, prospectus, offer letter | Module 37 (AWS SES); open/click tracked |
| In-app notification | For existing students' parents (Module 35) | — |

All communications template-based (reduces errors, ensures compliance). Templates localised per language preference.

### 3.4 Follow-up Cadence (Drip Sequence)

Default drip sequence (configurable per course):

| Day | Action |
|----|--------|
| Day 0 | Welcome SMS + WhatsApp message with brochure link |
| Day 2 | Email: course details + fee structure |
| Day 5 | Outbound call attempt |
| Day 8 | SMS: "Application deadline approaching" |
| Day 12 | WhatsApp: virtual tour link |
| Day 15 | Call + offer of campus visit |
| Day 20 | Scholarship eligibility message (if no action) |

Drip pauses automatically when lead advances to "Applied" stage. Customised cadences per campaign.

### 3.5 Best Time to Call

Analytics engine computes per counsellor, per lead segment:
- Call answer rate by hour of day (8 AM–8 PM)
- Call answer rate by day of week
- Best window shown as suggestion: "Leads from this area answer best at 6–7 PM on weekdays"
- Based on aggregated historical call log data

### 3.6 DND Compliance

- TRAI DND registry scrub before any bulk SMS campaign
- Individual DND flag on lead record (set manually by counsellor if lead requests no contact)
- DND leads: only transactional SMS (application status, fee receipt) allowed; marketing SMS blocked
- WhatsApp: consent required; stored as opt-in timestamp per lead

### 3.7 Communication Timeline

Each lead has a unified timeline (newest first):
- All calls (with duration, outcome, notes)
- All SMS sent (template name, status)
- All WhatsApp messages (template, delivery status)
- All emails sent (subject, open/click status)
- All campus visits
- All application events
- All counsellor notes
- All status changes

Visible to: assigned counsellor + admission manager + Principal. Audit-logged for access.

### 3.8 Overdue Follow-up Escalation

- If no contact attempt on a Hot/Warm lead for 5 days → counsellor dashboard alert
- If Hot lead uncontacted for 7 days → supervisor (admission manager) notified
- Supervisor can re-assign or prompt counsellor

---

## 4. Application Management

### 4.1 Application Form Configuration

Each course has its own application form configured by admission manager:

| Section | Contents |
|---------|----------|
| Personal details | Name, DOB, gender, Aadhaar number, photo, address |
| Contact details | Mobile, email, parent contact |
| Academic history | Last 3 years' marks (percentage/grade + board/university) |
| Entrance exam scores | JEE/NEET/CUET/state CET/in-house; rank + score |
| Category declaration | General / SC / ST / OBC / EWS / PWD / NRI / Sports / Management |
| Document upload | Per checklist (generated from course + category) |
| Preferences | Campus preference, course preference (if multi-course application) |
| Declaration | Undertaking of correctness; digital timestamp |
| Payment | Application fee (if applicable) |

### 4.2 Application Fee

- Configurable: ₹0 (free) to ₹2,000 (competitive entrance programmes)
- Payment via Module 25 (online); application not submitted until fee paid (configurable)
- Fee non-refundable by default; exception: if application rejected for technical reasons, librarian can refund
- GST on application fee: 18% if institution is GST-registered (service)

### 4.3 Application Number

Auto-generated on submission:
- Format: `[InstitutionCode]-[AY]-[CourseCode]-[Sequence]` e.g., `GRDC-2526-CSE-00347`
- Unique per academic year per institution
- Used for all subsequent communication with applicant

### 4.4 Age Eligibility Checks

| Admission Level | Age Rule |
|----------------|----------|
| Class 1 (CBSE/ICSE) | Minimum 5 years 6 months as of 1 April of admission year |
| Class 11 (Science) | Minimum Class 10 passed; age 15–17 typical |
| Undergraduate | As per AICTE/UGC norms; no maximum age for most programmes |
| Medical (MBBS) | NEET qualified; minimum 17 years; maximum 25 (GC) / 30 (OBC/SC/ST) |
| Lateral entry | Diploma holder; minimum 3-year diploma from approved institution |

Age validation at application submission: warning shown + blocked if below minimum.

### 4.5 Application Status Flow

```
Draft (form saved, not submitted)
  → Submitted (form + fee)
    → Under Review (admission committee)
      → Shortlisted (called for test/interview)
        → Selected (offer letter generated)
          → Waitlisted (reserve list)
        → Rejected (with reason code; notified)
          → Enrolled (all conditions met; Module 07 created)
```

Applicant sees their status in real-time via app. Status change triggers notification via Module 35.

### 4.6 Quota & Seat Matrix

| Quota | Description |
|-------|-------------|
| General (UR) | Open merit |
| SC | Scheduled Caste (15% central; state varies) |
| ST | Scheduled Tribe (7.5% central; state varies) |
| OBC (NCL) | Other Backward Classes — Non-creamy layer |
| EWS | Economically Weaker Section (10% — 103rd Amendment) |
| PWD / PH | Persons with Disabilities (5% horizontal; RPwD Act 2016) |
| Sports / NCC / NSS | Horizontal quota (1–2% typical) |
| Management quota | Institution-discretionary (AICTE allows up to 15%) |
| NRI / FN | NRI/Foreign National (5–15% depending on programme) |
| Government nominees | State government-directed admissions |

Seat matrix per course per campus: total seats broken by quota. System enforces: cannot admit more than quota allows. Unfilled reserved seats: opened to next eligible category after prescribed date (per state rules).

### 4.7 RTE 25% Lottery (School — Class 1)

For CBSE/state board schools admitting Class 1:
- EWS/disadvantaged group applications collected
- Eligibility verified (income certificate, Aadhaar, address proof within school zone)
- If applications > available seats (25% of Class 1 strength): computerised random draw
- Draw conducted in front of parent representatives; witnessed; result recorded
- Selected + waitlist list published; notifications sent
- Draw audit log: seed used, draw time, witness names — immutable

### 4.8 AICTE/UGC Intake Compliance

- Approved intake per course stored (from AICTE/UGC approval letter)
- System hard-blocks admissions once approved intake is reached
- Additional seats (if any TFW — Tuition Fee Waiver scheme seats) tracked separately
- Annual renewal of approval: alert when AICTE/UGC approval expiry approaches

---

## 5. Entrance Test & Interview

### 5.1 In-house Entrance Test

Integration with Module 17 (Question Bank) and Module 19 (Exam Session):
- Test paper built in Module 18 (Exam Paper Builder)
- Test session created in Module 19
- Admit card: auto-generated (application number, photo, date/time/venue, instructions); downloadable PDF
- Test delivery: online (Module 19) or paper-based (answer sheet scanned and graded)
- Results: auto-graded for MCQ (Module 20); manual entry for descriptive

### 5.2 Merit List Generation

Post-test:
- System generates merit list: applicants ranked by score
- Category-wise merit lists generated simultaneously (SC merit, ST merit, OBC merit, UR merit)
- Tie-breaking rule: configurable (e.g., higher marks in Class 10 Maths; younger age)
- Merit list available to admission committee for review before finalisation
- Merit list publication: visible to applicants (rank and score; not other applicants' details)

### 5.3 Interview Scheduling

For shortlisted candidates:
- Date, time, venue assigned per candidate
- Panel: 2–4 members (faculty + Principal/Director); panel assignment per batch
- Availability check: panel members' calendar from Module 10/timetable
- Confirmation sent to candidate via SMS + email
- Reschedule request: candidate can request (1 time); panel notified

### 5.4 Interview Scorecard

| Criterion | Weight | Score (1–10) |
|-----------|--------|--------------|
| Communication skills | 20% | Each panellist scores |
| Subject knowledge / aptitude | 30% | Each panellist scores |
| Motivation / goal clarity | 20% | Each panellist scores |
| General awareness | 15% | Each panellist scores |
| Overall impression | 15% | Each panellist scores |

Panellists score independently. Average computed. Composite = (Test score × weight) + (Interview score × weight) per programme policy.

### 5.5 Group Discussion (GD)

For management/MBA programmes:
- GD groups of 8–12 candidates; topic assigned by admission committee
- Evaluator(s) score: Initiative, Content quality, Listening, Group dynamics, Communication
- GD score stored per candidate; combined with PI score for final merit

### 5.6 Document Verification at Interview

- Original documents presented at interview centre
- Checker: staff member name + date logged for each document verified
- Discrepancy: if document doesn't match application → admission on hold; Principal informed
- Fake document flag: suspicious documents referred to Principal + legal cell; admission suspended

---

## 6. Selection, Offer & Waitlist

### 6.1 Selection List Generation

After merit computation:
1. System fills seats: UR seats from UR merit; SC seats from SC merit; etc.
2. Horizontal reservation (PWD, Sports) applied across categories
3. Management quota: separate list if applicable
4. Output: provisional selection list per course per campus
5. Admission committee reviews; can override with reason (logged)
6. Principal/Director digital approval; immutable after approval

### 6.2 Offer Letter

Generated on selection approval:
- Candidate name, application number, course, campus, academic year
- Seats allotted under: quota type stated
- Fee payable: admission fee + first instalment (from Module 24)
- Fee due date: acceptance + payment deadline
- Documents required at joining (remaining unverified documents)
- Reporting date and time for orientation
- Anti-ragging declaration requirement noted
- Digitally generated (WeasyPrint PDF); sent via Module 37 email + available in app

### 6.3 Offer Acceptance & Deadline

- Candidate accepts offer in-app (digital confirmation + timestamp)
- Seat status: Reserved (until payment made)
- If not accepted/paid by due date: seat released automatically to waitlist
- Acceptance deadline: configurable per institution (typically 7–15 days from offer)
- Extension: admission manager can extend deadline for individual candidate with reason

### 6.4 Waitlist Management

- Waitlist ranked by same merit criteria as selection list
- Candidate sees their waitlist position in app
- When a seat is released (cancellation or deadline lapse) → first waitlist candidate auto-notified
- Waitlist hold: 48 hours for waitlisted candidate to accept; if not accepted → moves to next
- Waitlist exhausted: if all waitlisted candidates decline → seat goes to management quota (if applicable) or remains vacant
- Waitlist closure: official closure date; remaining waitlisted candidates notified of closure

### 6.5 Seat Cancellation & Refund

Candidate cancels after acceptance:
- Cancellation request in-app; reason recorded
- Refund policy per Module 25:
  - Before classes begin (> 15 days): 90% refund (UGC guideline)
  - Before classes begin (< 15 days): 80% refund
  - After classes begin: no refund (only security deposit)
- Refund processed via Module 25; bank details collected
- Seat released immediately on cancellation confirmation

### 6.6 Management & NRI Quota

Management quota:
- Separate approval chain: management/trustee digital approval required
- Higher fee structure (from Module 24 NRI/management fee component)
- Documented with trustee approval timestamp; auditable

NRI quota:
- Fee in INR equivalent of USD/AED (exchange rate at time of admission stored)
- FEMA compliance note: foreign exchange brought through proper banking channel; bank certificate required
- NRI candidate: foreign passport or OCI card copy stored

---

## 7. Document Collection & Verification

### 7.1 Document Master Per Course

Admission manager configures document checklist per course + category combination:

| Category | Typical Additional Documents |
|---------|------------------------------|
| SC/ST | Caste certificate from competent authority |
| OBC (NCL) | OBC certificate + non-creamy layer declaration (issued within 1 year) |
| EWS | Income certificate (< ₹8L/year from all sources); issued by Tehsildar/SDM |
| PWD | Disability certificate from CMMO/District Hospital; disability % stated |
| Sports | Sports certificate (national / state / district level); sport officer verification |
| NRI | Foreign passport / OCI card; relationship proof if parent is NRI |
| Ex-serviceman | Discharge certificate / NOC from commanding officer |

### 7.2 Document Status Tracking

| Status | Meaning |
|--------|---------|
| Pending | Not yet uploaded |
| Uploaded | Candidate uploaded; awaiting verification |
| Verified | Admission staff verified (original checked); staff name + date logged |
| Rejected | Document invalid/fake/expired; reason stated; candidate notified |
| Waived | Exempted for specific reason (approved by Principal) |

Deficiency notice auto-sent if mandatory document remains "Pending" for > 5 days after application.

### 7.3 Anti-Ragging Affidavit Collection

Per UGC Anti-Ragging Regulations 2009:
- Student affidavit: collected at/before admission; digital signature + timestamp
- Parent affidavit: collected at/before admission; digital signature + timestamp
- Compliance dashboard: % affidavits collected; 100% required before classes begin
- Annual renewal: collected again each academic year

### 7.4 Migration Certificate

For students from a different board/university:
- Migration certificate required before finalising admission
- Provisional admission granted on undertaking; final admission on MC submission within 60 days
- MC collection tracked; non-submission → provisional admission cancelled (with 15-day notice)

### 7.5 EWS Income Certificate Validation

- Issued by: Tehsildar, SDM, BDO, or equivalent (as per state notification)
- Income limit: ₹8 lakh per year from all sources (Central EWS definition)
- Validity: issued within the current financial year
- System checks: issuing authority designation, issue date (must be within 12 months), income amount
- Borderline cases: flagged for Principal review

### 7.6 Fake Document Protocol

If document suspected fake:
1. Admission on hold; document flagged in system
2. Principal + legal cell notified automatically
3. Candidate given 7-day show-cause notice
4. Verification with issuing authority (board, university, Tehsildar) — process tracked
5. Confirmed fake: admission cancelled; amount forfeited (per terms); FIR filed if applicable
6. Immutable log of entire process for legal defence

---

## 8. Enrolment & Handover to Academic Modules

### 8.1 Enrolment Trigger

All conditions must be met before enrolment is confirmed:

```
□ Documents: all mandatory documents verified
□ Fee: admission fee + first instalment paid (Module 25)
□ Offer: accepted by candidate
□ Anti-ragging: both affidavits collected
□ Medical fitness: cleared (where applicable)
□ Seat: within quota limits
```

On all conditions met → admission manager confirms enrolment → Module 07 student record created.

### 8.2 Handover to Module 07

Data passed from Module 31 to Module 07:
- Personal details (name, DOB, gender, photo, Aadhaar, address)
- Academic history (previous marks, board)
- Course assigned, class/section (if allocated), roll number (provisional)
- Category / quota
- Emergency contacts (parent details)
- Language preference
- Documents (linked from R2 storage)

Module 07 becomes the single source of truth for student data henceforth.

### 8.3 Downstream Activations (Auto-triggered on Enrolment)

| Module | Action Triggered |
|--------|----------------|
| Module 03 — RBAC | Student role activated; permissions assigned |
| Module 07 — Student Profile | Full profile created |
| Module 09 — Parent Portal | Parent app invite sent |
| Module 24 — Fee Structure | Student's fee schedule activated |
| Module 25 — Fee Collection | Admission fee receipt finalised; next invoice scheduled |
| Module 28 — Hostel | Hostel preference pre-captured; allotment queued |
| Module 29 — Transport | Transport preference pre-captured; enrolment queued |
| Module 30 — Library | Library member auto-created |
| Module 35 — Notifications | Student + parent added to notification groups |

### 8.4 Admission Register

Official admission register maintained per affiliation board requirements:
- Sequential admission number (never reused, never deleted)
- Fields: S.No., Admission No., Date, Name, DOB, Father's Name, Category, Course, Previous Institution, Remarks
- Exportable in government-mandated format
- Corrections: struck-through with initialled correction (in-app equivalent: edit with reason + audit trail; original preserved)

### 8.5 Welcome Kit (Digital)

Sent to newly enrolled student + parent on confirmation:
- Welcome letter (personalised; WeasyPrint PDF)
- Fee structure summary (from Module 24)
- Academic calendar (from Module 05)
- Orientation date and venue
- Timetable (if available; from Module 10)
- Library card (from Module 30)
- Transport route details (if opted; from Module 29)
- Hostel allotment (if applicable; from Module 28)
- Emergency contact numbers (institution)
- App download link (student + parent app)

---

## 9. Analytics & Funnel Reporting

### 9.1 Admissions Funnel

| Stage | Count | Conversion % |
|-------|-------|-------------|
| Total enquiries | N | 100% |
| Contacted | n1 | n1/N % |
| Applied | n2 | n2/N % |
| Shortlisted | n3 | n3/n2 % |
| Selected | n4 | n4/n3 % |
| Fee paid | n5 | n5/n4 % |
| Enrolled | n6 | n6/n5 % |

Funnel shown per course, per source, per academic year, per campus. Drill-down on any stage.

### 9.2 Source ROI

| Source | Leads | Enrolled | Cost (₹) | Cost per Lead | Cost per Enrolled |
|--------|-------|---------|---------|--------------|------------------|
| Google Ads | … | … | … | … | … |
| Walk-in | … | … | 0 | 0 | 0 |
| Referral | … | … | (bonus paid) | … | … |
| WhatsApp | … | … | … | … | … |

Highest conversion sources identified; budget shifted accordingly.

### 9.3 Counsellor Performance

| Metric | Description |
|--------|-------------|
| Leads assigned | Total leads in their queue |
| Contacted % | Leads attempted contact ÷ assigned |
| Conversion rate | Enrolled ÷ assigned |
| Average response time | Time from lead creation to first contact attempt |
| Average follow-up cadence | Days between contacts |
| Offers issued | Count of offer letters generated |
| Enrolled this month | Confirmed enrolments |

Top/bottom counsellor ranking. Training triggered for bottom performers.

### 9.4 Drop-off Analysis

For each stage transition, system records the last meaningful interaction before drop:
- Stage where lead went Cold/Lost most often
- Most common Lost reason codes
- Course-wise drop-off patterns
- Fee stage: highest absolute drop → scholarship lever flagged

### 9.5 Geographic Heatmap

Enquiries and enrolments plotted by city/district/pin code:
- Identifies primary catchment (where most enrolments come from)
- Identifies underserved zones (high enquiries, low enrolments → possible transport/facility barrier)
- Guides school fair / exhibition location planning

### 9.6 Course-wise Seat Fill Rate

| Course | Approved Intake | Applied | Selected | Enrolled | Fill Rate % |
|--------|----------------|---------|---------|---------|------------|
| B.Tech CSE | 60 | 180 | 72 | 61 | 101%+ (waitlist active) |
| B.Tech Mech | 60 | 40 | 40 | 35 | 58% |

Low fill rate alert (< 60% with 30 days to close): auto-alert to Principal + suggestion to run targeted campaign or open scholarship.

### 9.7 Predictive Enrolment Scoring (Strategic Feature)

ML model scoring each lead's enrolment probability (0–100%):
- Features: source, engagement touchpoints, campus visit done, entrance score, response rate, course fill rate, category, distance from campus
- Score updated daily as new interactions are logged
- Counsellor dashboard shows: High probability (>70%) / Medium (40–70%) / Low (<40%)
- Counsellors prioritise high-probability leads; reduce time on low-probability prospects
- Model retrains monthly on completed admission cycle data

### 9.8 Abandoned Application Recovery

Applicants who started but did not submit:
- 48-hour trigger: if application > 50% complete but not submitted → push notification: "You're almost done! Complete your application before seats fill up."
- 72-hour trigger: WhatsApp message with direct link to incomplete section
- Field-level drop-off: which fields cause most abandonment (marks entry? document upload?) → form simplified
- Abandoned recovery rate tracked: % of nudged abandoners who completed

---

## 10. Regulatory Compliance

### 10.1 Reservation Compliance Report

For every academic year + course:
- Seats allocated per quota vs filled per quota
- Unfilled reserved seats: reason (no eligible applicants) + date opened to general
- EWS 10% compliance: verified with income certificates
- PWD horizontal reservation: 5% applied across all categories
- Roster: OBC roster position per cycle (for institutions following point roster)

Available for regulatory inspection. Immutable once admission cycle closes.

### 10.2 RTE Compliance Report

For schools:
- 25% seats: total Class 1 intake × 25% = RTE seats
- Applications received from EWS/disadvantaged group
- Lottery conducted: Y/N; draw log
- Seats filled vs mandated
- Government reimbursement claim: per-child per-year reimbursement tracked (linked to Module 25)
- Annual RTE report submitted to District Education Officer; exported from Module 31

### 10.3 AICTE/UGC Approved Intake Compliance

- Approval letter details stored: year, programme, approved intake
- Actual admissions vs approved intake: daily dashboard
- Over-intake: hard-blocked; override requires Principal + trustee approval with documented justification
- Annual renewal: alert 90/60/30 days before approval letter expires

### 10.4 Admission Register Audit Trail

- All entries immutable after admission cycle close
- Corrections: before cycle close, correction with reason + approver; audit trail
- Annual submission: admission register summary to affiliating board/university
- Inspection mode: auditor role (Module 03) can view but not edit

### 10.5 Anti-Ragging Collection Compliance

- 100% affidavit collection (student + parent) required before classes begin
- Compliance %: shown on admission manager dashboard
- Students with missing affidavits: blocked from attending classes (configurable enforcement)
- Submitted to Principal's anti-ragging file per UGC regulations

---

## 11. Strategic Features

### 11.1 Scholarship as Conversion Lever

When lead drops off at fee stage:
- System auto-checks scholarship eligibility: income (EWS), merit (top 10% by entrance score), category, sports
- If eligible → counsellor alert: "Lead [Name] dropped at fee stage. Eligible for merit scholarship of ₹20,000. Recommend outreach."
- Counsellor reaches out with scholarship offer
- Scholarship provisionally approved; linked to admission; Module 24 applies waiver
- Converts price-sensitive high-quality leads who would otherwise go to competitors

### 11.2 Alumni Referral Programme

- Enrolled student/alumni refers a new lead
- Referral captured: referring person's ID + name stored in lead record
- On referral lead enrolling: reward triggered — fee waiver (₹1,000–₹5,000) or book/merchandise voucher
- Gamified leaderboard: top referrers visible (with consent) in alumni community
- Referral conversion rate: tracked; programme ROI computed (reward cost vs fee earned from referred student)

### 11.3 WhatsApp Admission Bot (Module 36 Integration)

Structured WhatsApp flow for enquiries:
- Visitor messages institution's WhatsApp
- Bot greets and asks: "What are you looking for? [1] Admissions [2] Fee enquiry [3] Campus visit"
- Selection 1 → "Which course?" → intake form collected via quick-reply buttons
- FAQs auto-answered: eligibility, fee structure, entrance exam dates
- If intent confirmed → bot says: "A counsellor will contact you within 2 hours" → lead created in CRM; counsellor notified
- Bot handles 60–70% of routine enquiries; counsellors focus on warm leads only

### 11.4 Seat Fill Rate Alert & Campaign Trigger

- If course fill rate < 60% and admission deadline > 30 days away → auto-alert to Principal
- Suggested actions shown: Open house event / Targeted WhatsApp campaign / Scholarship announcement / Fee instalment option
- One-click campaign: Principal approves → Module 36 WhatsApp broadcast + Module 37 email to all "Interested but not applied" leads for that course
- Fill rate trend: week-by-week graph so management can see if trajectory is improving

### 11.5 Fee Payment Instalment at Admission

To reduce drop-off at payment stage:
- Option to split admission fee: 50% now + 50% in 30 days (configurable)
- Second instalment: auto-reminder 7 days before due; Module 25 handles
- PDC or auto-debit mandate collected for second instalment
- Students who use instalment option tracked: default rate monitored; policy adjusted if high default

### 11.6 NPS Survey Post-Admission

Two weeks after enrolment confirmation:
- SMS/app survey to student: "How likely are you to recommend [Institution] to a friend? (0–10)"
- Same survey to parent
- NPS = % Promoters − % Detractors
- Tracked year-on-year; benchmark against 40+ (good for EdTech/education)
- Low NPS responders (score 0–6): counsellor follow-up call to understand concern; retention action
- NPS insights: what promoters say = marketing copy; what detractors say = improvement areas

### 11.7 Virtual Campus Tour

- 360° tour video or photo gallery linked per institution from institution settings
- Embedded in: offer letter email, brochure, WhatsApp message (Day 12 drip)
- View tracking: email link click tracked (Module 37); WhatsApp link opened (Module 36)
- Analytics: leads who viewed tour have measurably higher conversion; reported as "Tour ROI"

---

## 12. Integration Map

| Module | Integration |
|--------|------------|
| Module 03 — RBAC | Student role activated on enrolment; counsellor access scoped to assigned leads |
| Module 05 — Academic Calendar | Academic year for lead tagging; orientation dates; admission deadlines |
| Module 07 — Student Profile | Created on enrolment; all admission data handed over |
| Module 09 — Parent Portal | Parent app invite triggered on enrolment |
| Module 10 — Timetable | Class/section assignment post-enrolment |
| Module 17 — Question Bank | In-house entrance test paper sourced |
| Module 18 — Exam Paper Builder | Entrance test paper built |
| Module 19 — Exam Session | Entrance test session created; admit cards generated |
| Module 20 — Auto-Grading | MCQ entrance test auto-graded |
| Module 24 — Fee Structure | Admission fee, course fee activated on enrolment |
| Module 25 — Fee Collection | Application fee, admission fee, instalment collection |
| Module 28 — Hostel | Hostel preference captured; allotment queued |
| Module 29 — Transport | Transport preference captured; enrolment queued |
| Module 30 — Library | Library member auto-created on enrolment |
| Module 36 — WhatsApp | Admission bot, drip messages, broadcast campaigns |
| Module 37 — Email | Brochure, offer letter, welcome kit emails |
| Module 42 — DPDPA & Audit Log | Lead data access, application history, document access audited |

---

## 13. Data Model (Key Tables)

```
crm_leads
  id, tenant_id, name, mobile, email, parent_name, parent_mobile,
  city, source, utm_source, utm_medium, utm_campaign,
  academic_year, language_pref, status, lead_score, score_band,
  assigned_counsellor_id, referring_student_id, competitor_notes,
  created_at, last_activity_at, enrolled_student_id

crm_lead_course_interests
  id, lead_id, course_id, status, created_at

crm_call_logs
  id, lead_id, counsellor_id, direction, call_date, duration_sec,
  outcome, notes, next_action_due, created_at

crm_communications
  id, lead_id, channel, direction, template_id, sent_at,
  delivered_at, opened_at, clicked_at, status, content_preview

crm_tasks
  id, lead_id, assigned_to, task_type, due_date, due_time,
  status, completed_at, notes

crm_applications
  id, lead_id, course_id, campus_id, academic_year,
  application_no, applied_on, status, category_declared,
  application_fee_paid, fee_transaction_id, edit_locked_at

crm_application_academic_history
  id, application_id, year, institution, board_university,
  class_standard, percentage, grade, remarks

crm_application_documents
  id, application_id, doc_type, uploaded_at, r2_key,
  verified_by, verified_at, status, rejection_reason

crm_entrance_tests
  id, application_id, test_session_id, admit_card_generated,
  score, rank, merit_list_position, category_rank

crm_interviews
  id, application_id, interview_date, venue, panel_members,
  status, composite_score, outcome, outcome_reason

crm_interview_scores
  id, interview_id, panellist_id, criterion, score, notes

crm_seat_matrix
  id, course_id, campus_id, academic_year, quota_type,
  total_seats, filled_seats, waitlist_count

crm_selections
  id, application_id, selected_on, quota_type, merit_rank,
  approved_by, approval_timestamp, offer_letter_generated_at

crm_offer_letters
  id, application_id, generated_at, accepted_at, acceptance_deadline,
  fee_due_date, status, pdf_r2_key

crm_waitlist
  id, course_id, campus_id, academic_year, application_id,
  quota_type, waitlist_rank, notified_at, status

crm_enrolments
  id, application_id, enrolled_on, admission_number,
  student_id, confirmed_by, all_docs_verified, fee_paid,
  affidavit_student, affidavit_parent, welcome_kit_sent_at

crm_admission_register
  id, tenant_id, academic_year, serial_no, admission_no,
  student_id, date_of_admission, name, dob, category,
  course_id, previous_institution, remarks

crm_campaigns
  id, tenant_id, name, start_date, end_date, budget,
  channel, academic_year, cost_total, leads_generated,
  enrolled_count, cost_per_lead, cost_per_enrolled

crm_rte_lottery
  id, tenant_id, academic_year, draw_date, total_applicants,
  seats_available, draw_seed, witness_names, result_published_at

crm_nps_surveys
  id, respondent_type, student_id_or_lead_id, sent_at,
  responded_at, score, verbatim, follow_up_done
```

---

## Cross-Module References

- **Module 03**: Student role activated on enrolment; counsellor access scoped to assigned leads only — write
- **Module 05**: Academic year config; orientation dates; admission deadlines synced — read-only
- **Module 07**: Created on enrolment; all personal, academic, document data handed over — write
- **Module 09**: Parent app invite triggered on enrolment — event write
- **Module 17/18/19/20**: Entrance test paper, session, admit card, auto-grading — write/read
- **Module 24**: Fee schedule activated for enrolled student — write
- **Module 25**: Application fee, admission fee, instalment collection — write via Module 25 API
- **Module 28**: Hostel preference pre-captured at admission; allotment queued — event write
- **Module 29**: Transport preference pre-captured; enrolment queued — event write
- **Module 30**: Library member auto-created on enrolment — event write
- **Module 36**: WhatsApp bot, drip messages, broadcast campaigns — write via Module 36 API
- **Module 37**: Brochure, offer letter, welcome kit emails dispatched — write via Module 37 API
- **Module 42**: Lead data access, document access, admission decisions audited — write

---

*Module 31 complete. Next: Module 32 — Counselling & Student Welfare.*
