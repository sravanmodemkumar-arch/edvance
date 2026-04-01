# Module 32 — Counselling & Student Welfare

## 1. Purpose

Module 32 owns the complete student welfare and counselling lifecycle within EduForge institutions — from appointment booking and case management through career guidance, special needs support, crisis intervention, anti-ragging counselling, and proactive well-being monitoring. It serves all 16 institution types with particular depth for residential schools, engineering and medical colleges, coaching centres, and universities.

The module aligns with UGC Guidelines on Counselling 2020, RCI (Rehabilitation Council of India) registration requirements, POCSO 2012 mandatory reporting obligations, UGC Anti-Ragging Regulations 2009, NAAC Criterion 5.2 (Student Support and Progression), RTE Section 26 (inclusive education), WHO counsellor-to-student ratio benchmarks, and DPDPA 2023 for sensitive personal data. It integrates with Module 07 (Student Profile), Module 11 (Attendance), Module 21 (Results), Module 28 (Hostel Well-being), Module 29 (Transport), Module 31 (Admission), Module 35 (Notifications), Module 41 (POCSO), and Module 42 (Audit Log).

---

## 2. Counselling Service Configuration

### 2.1 Counsellor Types & Qualifications

| Counsellor Type | Minimum Qualification | Scope |
|----------------|----------------------|-------|
| Academic counsellor | M.Ed / B.Ed + counselling training | Study skills, attendance, academic distress |
| Personal / mental health counsellor | M.A. Psychology (Clinical/Counselling) / MPhil Clinical Psychology | Personal, emotional, mental health issues |
| Career counsellor | M.A. Psychology + career guidance certification / MBA + HR background | Stream selection, higher education, career planning |
| Special educator (CWSN) | B.Ed Special Education / RCI-registered | IEP, learning disabilities, ADHD, ASD |
| Anti-ragging counsellor | Any counsellor; anti-ragging training mandatory | Ragging victims + accused; ARC support |

Counsellor profile: photo, qualifications, RCI number (if applicable), POCSO training date, caseload capacity, assigned student groups.

### 2.2 Counselling Centre Configuration

| Parameter | Detail |
|-----------|--------|
| Room name / location | Room number, floor, building |
| Session capacity | 1-on-1 / Group (up to 15) |
| Appointment hours | Time slots per day; counsellor-specific |
| Walk-in availability | Flag: yes/no per counsellor |
| Online session option | Video link (WebRTC or external) |
| Confidentiality policy | Stored; shown to students before first session |
| Mandatory reporting policy | POCSO + imminent harm exceptions; disclosed in consent |

### 2.3 Counsellor–Student Assignment

- Default assignment: counsellor allocated to class group / department / hostel block
- Student-initiated change: student can request a different counsellor; no reason required
- Large institutions: head counsellor triages new cases; assigns based on specialty + caseload
- Counsellor-to-student ratio tracked: WHO benchmark 1:250 (school) / 1:500 (college); alert when exceeded

### 2.4 Confidentiality & Consent Framework

- Consent form signed before first session (in-app; timestamped)
- Consent covers: confidentiality scope, mandatory reporting exceptions, session recording policy, data retention (3 years post-graduation per DPDPA guidance)
- Session notes: encrypted at rest; accessible to assigned counsellor + Principal (documented need-to-know only)
- Not visible to: parents (except for minors in routine cases or mandatory reporting), teachers, wardens, or administrative staff
- Under-18 students: parental consent required before counselling begins (except crisis and mandatory reporting situations)
- Anonymous access: student books via token; identity voluntarily disclosed; counsellor sees token only until disclosure

---

## 3. Appointment & Session Management

### 3.1 Booking Methods

| Method | Initiated By | Priority |
|--------|-------------|---------|
| Self-booking (app) | Student | Normal |
| Parent-initiated | Parent | Normal |
| Teacher referral | Class teacher (from their dashboard) | Elevated |
| Warden referral | Hostel warden (low well-being score) | Elevated |
| Academic distress flag | System (auto; attendance/marks drop) | Elevated |
| SOS-linked | Student taps SOS → "Talk to counsellor" | Immediate |
| Crisis walk-in | Student arrives directly | Immediate |
| Anti-ragging referral | ARC member | Elevated |

### 3.2 Appointment Workflow

```
Student selects counsellor → selects date + slot → selects reason category
  → (optional) types brief description (visible to counsellor only)
  → Confirmation sent (app + SMS)
  → Reminder: 1 hour before session
  → Session conducted
  → Counsellor closes session: notes, outcome, follow-up
  → Follow-up appointment auto-suggested
```

### 3.3 Reason Categories

Student selects one or more at booking (general categories; not clinical diagnoses):
- Academic stress / difficulty
- Exam anxiety
- Peer conflict / bullying
- Family issues
- Career confusion / stream selection
- Personal / emotional concerns
- Relationship issues
- Substance use concerns
- Identity / self-esteem
- Grief / loss
- Adjustment (new to institution)
- Other (anonymous submission)

Anonymous option: student selects reason without identifying themselves; counsellor sees reason + anonymous token.

### 3.4 Session Types

| Type | Participants | Duration |
|------|-------------|---------|
| Individual | Student + counsellor | 30–60 min |
| Group | 4–15 students + counsellor | 45–90 min |
| Family | Student + parent + counsellor | 45–60 min |
| Crisis | Student + counsellor (immediate) | As needed |
| Peer mediation | 2 students + trained mediator | 45–60 min |
| Online | Video/phone | Same as in-person |

### 3.5 Session Notes Structure

| Field | Visibility |
|-------|-----------|
| Presenting issue | Counsellor + Principal (need-to-know) |
| Counsellor observations | Counsellor only |
| Intervention used | Counsellor + supervisor |
| Risk assessment score | Counsellor + Principal |
| Safety plan (if created) | Counsellor + Principal; parent if minor or consented |
| Follow-up plan | Counsellor |
| Session outcome | Counsellor; anonymised in reports |

All notes encrypted at rest (AES-256). Access logged in Module 42.

### 3.6 Session Outcome Codes

- Resolved — presenting issue addressed; no further sessions needed
- Ongoing — case active; follow-up scheduled
- Referred (internal) — referred to different counsellor / special educator
- Referred (external) — psychiatrist, psychologist, de-addiction centre
- Escalated — crisis protocol activated
- No-show — student did not attend; follow-up outreach triggered

---

## 4. Case Management

### 4.1 Case File Structure

Case file created on first session; all subsequent sessions appended:

| Section | Contents |
|---------|---------|
| Student context | Name, class/batch, hostel/day-scholar, key background (from Module 07 read-only) |
| Presenting concern | Initial presenting issue; history |
| Case status | Active / Closed / On hold / Referred externally |
| Severity | Low / Medium / High / Critical |
| Sessions log | All sessions with notes, dates, outcomes |
| Risk assessments | Date, tool used, score, action taken |
| Safety plan | If created; version-controlled |
| Referrals | Internal + external referral history |
| IEP | If CWSN; separate sub-section |
| Communications | Parent notifications, teacher flags, warden alerts |
| Closure summary | Goals achieved, ongoing concerns, recommendations |

### 4.2 Case Severity Levels

| Level | Description | Protocol |
|-------|-------------|---------|
| Low | Routine support; one-off concern | Standard appointments |
| Medium | Recurring concern; affecting academics / well-being | Fortnightly sessions; parent informed |
| High | Acute risk; self-harm ideation (passive) | Weekly sessions; safety check; parent notified (minor) |
| Critical | Imminent harm; active crisis | Immediate escalation (see §7) |

Severity change: counsellor upgrades/downgrades with rationale logged; each change auditable.

### 4.3 Risk Assessment

Structured tool administered at every Medium/High/Critical session:
- Adapted Columbia Suicide Severity Rating Scale (C-SSRS): passive ideation / active ideation / plan / means / intent / behaviour
- Score: 0–5; stored per session
- Score ≥ 3 → Level High protocol auto-triggered; counsellor prompted
- Score = 5 → Level Critical protocol; immediate escalation

### 4.4 Safety Plan

Co-created with student at Level High:
- Warning signs (what triggers distress)
- Coping strategies (what helps)
- People to contact (trusted person at institution)
- Professional contacts (counsellor, helpline)
- Environment safety steps (means restriction)
- Stored in case file; shared with parent if minor or if student consents

### 4.5 Behavioural Observation System

- Teacher observes concerning behaviour → submits anonymous flag from teacher dashboard: [Student ID, concern type, date, brief description]
- Student not informed of teacher flag identity
- Counsellor receives flag; uses as context; decides whether to reach out
- 3+ flags from different teachers in 30 days → auto-elevate to counsellor attention

### 4.6 Academic Context Integration

Counsellor dashboard shows (read-only, for context):
- Attendance trend last 30 days (Module 11)
- Exam score trend last 3 assessments (Module 21)
- Hostel well-being score trend (Module 28, if boarder)
- Meal skip rate (Module 28, if boarder)
- Disciplinary incidents (Module 28, anonymised)

Data not stored in case file; used for session context only. Access logged in Module 42.

### 4.7 CWSN Case & IEP

**Identification:**
- Flagged at admission (Module 31) or by teacher/counsellor post-admission
- Formal diagnosis: referral to external RCI-registered psychologist; assessment report stored

**IEP (Individualised Education Plan):**
- Created jointly: counsellor + special educator + class teacher + parent
- Goals: specific, measurable, time-bound (3 per term maximum)
- Accommodations: extra time (25–50%), scribe, large-print paper, oral exam option, preferential seating, assistive technology
- Review: every term; progress against goals documented
- Communicated to: Module 19 (Exam Session) for exam accommodations, Module 10 (Timetable) for classroom accommodations

**UDID tracking:** Unique Disability ID (Divyangjan) stored; used for government scholarship and reservation compliance.

### 4.8 Case Handover

When counsellor leaves institution:
- All active cases assigned to incoming counsellor
- Handover notes written by departing counsellor (summary, current status, risk level, ongoing plan)
- Student notified of counsellor change; new counsellor introduced
- Case file continuity: all history available to incoming counsellor
- Handover audit: date, from/to counsellor, case count — logged

---

## 5. Group Programmes & Workshops

### 5.1 Group Session Management

| Field | Detail |
|-------|--------|
| Group name | Descriptive (e.g., "Exam Stress — Class 12 Batch A") |
| Topic | From topic taxonomy (see §5.2) |
| Counsellor facilitating | Assigned counsellor |
| Dates | Multiple sessions; series or one-off |
| Max participants | 4–15 for therapeutic group; up to 100 for psychoeducation |
| Eligibility | By class, age, gender, referral-only vs open |
| Consent | Collected from each participant before first session |

Group attendance: per-session per-student; completion = attending ≥ 3 of N sessions.

### 5.2 Programme Catalogue

| Programme | Type | Sessions | Target |
|-----------|------|---------|--------|
| Exam stress management | Group therapy | 4 | Class 10, 12, Final year |
| Study skills workshop | Psychoeducation | 2 | All classes |
| Social skills training | Group therapy | 6 | Referred + voluntary |
| Anger management | Group therapy | 8 | Referred (discipline incidents) |
| Grief support group | Group therapy | 6 | Bereavement cases |
| Substance awareness | Psychoeducation | 2 | Class 8 onwards |
| Anti-ragging awareness | Compliance | 1/year | All students; mandatory |
| Career exploration | Workshop | 3 | Class 9–11; First year college |
| POCSO awareness | Age-appropriate | 1/year | All; mandatory |
| Mindfulness (8-week) | Group programme | 8 | Voluntary; stress-prone |
| Life skills (12-session) | Structured | 12 | All; ideally embedded in timetable |
| Digital wellness | Psychoeducation | 2 | Class 6 onwards |
| Parent workshop | Psychoeducation | 2/year | Parents |

### 5.3 Pre/Post Well-being Score

For each group programme:
- Student completes standardised well-being scale (e.g., WHO-5 Well-being Index) at first and last session
- Pre vs post score improvement computed
- Programme effectiveness: if < 20% average improvement → counsellor reviews content for next cycle
- Aggregate results in annual welfare report (anonymised)

### 5.4 Life Skills Programme Structure

12-session structured curriculum (one session/week):

| Session | Topic |
|---------|-------|
| 1–2 | Self-awareness and emotional intelligence |
| 3–4 | Communication and assertiveness |
| 5–6 | Conflict resolution and peer pressure |
| 7–8 | Time management and study organisation |
| 9 | Financial literacy basics |
| 10 | Digital citizenship and online safety |
| 11 | Career readiness mindset |
| 12 | Reflection and goal-setting |

Session log: date, attendance, key learnings noted, student feedback. Progress tracked per student.

---

## 6. Career Counselling

### 6.1 Career Counselling Flow

```
Career interest inventory (RIASEC) administered online
  → Aptitude assessment (logical, verbal, spatial, numerical)
  → Personality profile (advisory)
  → Counsellor debrief session: results discussed
  → Career cluster mapping: 3–5 career paths suggested
  → Stream selection guidance (Class 10 exit)
  → Higher education pathway planning
  → College shortlist + application tracking
  → Entrance exam calendar (Module 49 integration)
  → Mock interview + SOP review
  → Career decision milestone recorded
```

### 6.2 Assessments

| Assessment | Tool Basis | Stored Data |
|-----------|-----------|-------------|
| Career interest inventory | Holland RIASEC codes | 6 dimension scores + primary code |
| Aptitude | Standardised battery | Sub-scores: logical, verbal, spatial, numerical |
| Personality | Big-5 adjacent (advisory) | Broad trait profile; not diagnostic |

Results stored in student profile (career section); visible to student + career counsellor only.

### 6.3 Higher Education Guidance

- Counsellor tracks entrance exam preparation: JEE / NEET / CUET / CAT / CLAT / state CETs
- Target exam dates imported from Module 49 (National Exam Catalog)
- College shortlist per student: dream / match / safety list; maintained in career case file
- Application deadlines tracked per institution; counsellor sends reminders
- Scholarship database: curated list of national + state scholarships; eligibility mapped to student profile
- Counsellor notes: session notes specific to career pathway discussions

### 6.4 Alumni Mentorship

- Counsellor matches student (career goal + field) to alumni mentor
- Alumni mentor profile: name, batch year, current role, company, willing to mentor (opt-in)
- Mentorship session log: date, type (call/in-person/video), notes
- Mentorship outcome: did student apply to similar field? — tracked as long-term data point

### 6.5 Career Decision Milestone

When student finalises career direction:
- Stored as milestone in Module 07 student profile
- Data used for: alumni tracking, programme evaluation, NAAC outcomes reporting
- Longitudinal: how many students are placed in their chosen career field 3–5 years post-graduation (if alumni tracking enabled)

---

## 7. Mental Health Crisis Protocols

### 7.1 Crisis Categories

| Category | Examples |
|---------|---------|
| Suicide ideation | Passive wishing to be dead; active plan |
| Active self-harm | Cutting, burning; disclosed or discovered |
| Harm to others | Threat to harm a specific person |
| Acute psychosis | Hallucinations, delusions, disorganised behaviour |
| Substance overdose | Intentional or accidental |
| Panic attack | Acute anxiety; breathing difficulty |
| Severe dissociation | Derealization; student unresponsive to surroundings |

### 7.2 Four-Level Protocol

**Level 1 — Low Risk (passive ideation, no plan):**
- Counsellor: immediate session; safety check; coping plan developed
- Frequency: weekly check-in sessions
- Parent notification: if minor AND if counsellor judges necessary
- Documentation: session note; risk score recorded

**Level 2 — Moderate Risk (ideation + vague plan, no means access):**
- Counsellor: immediate session + safety plan created
- Principal: notified same day
- Parent: notified same day (guardian if student is minor; student consent if 18+)
- Daily: counsellor check-in (in-person or app message)
- Means restriction: counsellor advises parent/warden to remove access to potential means

**Level 3 — High Risk (specific plan + means accessible):**
- Counsellor: immediate session; do not leave student alone
- Principal: notified immediately; present if possible
- Parent: called immediately; come to institution
- Hospital: counsellor recommends psychiatric consultation; referral letter generated
- Documentation: every action time-stamped

**Level 4 — Imminent/Acute (active attempt or acute psychosis):**
- Ambulance: called immediately (108)
- Parent: called simultaneously
- Principal: informed
- Police: if warranted (threat to others)
- All actions time-stamped in crisis log; immutable

### 7.3 Crisis Log

Every crisis event (Level 2+):
- Trigger event, date/time, who reported
- Risk score at time of crisis
- Each action taken with timestamp and who took it
- Resolution: student stabilised / hospitalised / returned home / referred
- Post-crisis review date
- Immutable log; visible to Principal + counsellor; accessible to authorised external auditor

### 7.4 Post-Crisis Review

Within 48 hours of resolution:
- Counsellor + Principal review: what triggered, early warning signs missed, what interventions worked
- System / protocol gaps identified
- Action plan for prevention of recurrence
- Documented; reviewed in quarterly ARC meeting

### 7.5 Postvention Protocol

After suicide attempt or death by suicide:
- Counsellor leads debrief sessions for affected classmates/batchmates/hostel peers within 48 hours
- Safe messaging guidelines followed (WHO/NIMHANS): no details of method; focus on help-seeking
- Staff debrief: counsellor conducts separate session for teachers and wardens
- Media communication: managed by Principal; counsellor advises
- Memorial: thoughtful; avoids glorification
- Long-term: follow-up sessions for high-impact peers over next 4–8 weeks

### 7.6 External Resource Network

Maintained by counsellor (reference only; not managed within Module 32):
- iCall (TISS): 9152987821
- NIMHANS helpline: 080-46110007
- Vandrevala Foundation: 1860-2662-345 (24×7)
- District mental health programme (DMHP) contact
- Empanelled psychiatrists + psychologists (3+ per institution)
- De-addiction centre (district-level)
- Child Welfare Committee (CWC) for POCSO referrals
- Legal aid cell (for domestic violence disclosures)

---

## 8. Anti-Ragging Cell Support

### 8.1 Anti-Ragging Committee (ARC) — Counsellor Role

Counsellor is a mandatory member of ARC per UGC Anti-Ragging Regulations 2009:
- Provides welfare perspective in enquiry proceedings
- Mandated to counsel both victim and accused
- Reports anonymised welfare trends to ARC quarterly

### 8.2 Victim Counselling

- Minimum 5 sessions; priority case; assigned senior counsellor
- First session within 24 hours of complaint
- Trauma-informed approach; no re-traumatisation through repeated questioning
- Safety assessment: is student at risk in current setting? Hostel / class change may be needed
- Coordination with Module 28 (hostel room change) and Module 41 (POCSO compliance if applicable)
- Progress notes shared with ARC (anonymised; severity and intervention type only)

### 8.3 Accused Counselling

- Counsellor assesses: is this behaviour a pattern? is there a trauma history?
- Minimum 3 sessions regardless of enquiry outcome
- Goal: behaviour change, not re-traumatisation
- Outcome communicated to ARC (behaviour risk level only)
- If accused shows high recidivism risk → flagged to Principal; expulsion recommendation supported by welfare evidence

### 8.4 Quarterly ARC Review

- ARC meets every quarter; counsellor presents: complaint count, type breakdown, victim welfare status, accused counselling completion rate
- Meeting minutes stored; accessible to NAAC / regulatory auditors
- Annual UGC self-declaration: auto-populated from ARC records; submitted by Principal

---

## 9. Proactive Well-being Monitoring

### 9.1 Early Warning System (EWS) Dashboard

Counsellor dashboard shows traffic-light status per student:

| Signal | Source | Weight |
|--------|--------|--------|
| Attendance drop (< 70%) | Module 11 | High |
| Exam score decline (>15% drop) | Module 21 | High |
| Well-being score < 50 | Module 28 | High |
| Meal skip rate > 5 consecutive | Module 28 | Medium |
| Disciplinary incidents (2+ in term) | Module 28 | Medium |
| Teacher behavioural flags (3+) | In-module | Medium |
| Counselling sessions skipped (3+) | In-module | Low |
| No extracurricular participation | In-module | Low |

Composite status:
- Green: all signals normal
- Amber: 2+ medium signals or 1 high signal
- Red: 2+ high signals or any Level 3/4 crisis history

Amber students: counsellor outreach within 3 working days.
Red students: immediate session; Level 2 protocol default.

### 9.2 Proactive Outreach Triggers

| Trigger | Action |
|---------|--------|
| New student (first term) | Orientation session offered within 2 weeks |
| Hostel new joiner (first 3 weeks) | Separation anxiety check-in by warden + counsellor |
| 2 weeks before major exam | Extra drop-in hours; exam stress session offered |
| Result publication day | Counsellor on standby; unexpected fail → immediate referral |
| Death in family | Fast-tracked session; class teacher discreet communication |
| Boarding school first week | Counsellor + warden joint check-in schedule |
| Student applied for withdrawal | Counsellor alerted before withdrawal approved (Module 31) |

### 9.3 Peer Supporter Programme

5% of students (approximately 1 per class) trained as peer supporters:
- Selection: students who volunteer; teacher + counsellor recommended
- Training: 8 hours; active listening, when to refer, self-care, confidentiality
- Role: first-contact listener; NOT therapists; refer to counsellor if in doubt
- Peer supporter identity: known to counsellor; may or may not be public (student's choice)
- Support log: peer supporter can flag a concern to counsellor (anonymously) without breaking confidence
- Annual training refresh; recognition at prize day
- Reduces stigma: peers see other students as helpers; normalises help-seeking

### 9.4 Anonymous In-app Helpline

- In-app text channel: student types concern anonymously
- Counsellor responds within 4 hours (during working hours); within 1 hour for crisis-flagged messages
- Student decides whether to escalate to full session
- If student describes imminent risk: counsellor cannot maintain anonymity; mandatory reporting applies; student warned in helpline terms
- Lowers barrier for adolescents who fear stigma or parental notification

### 9.5 Exam Period Surge Protocol

2 weeks before any major exam (from Module 05 calendar):
- Extended counsellor hours (configurable: +2 hours/day)
- Drop-in sessions: no appointment needed; counsellor available daily
- Stress management push notification to all students: coping tips + helpline
- Peer supporters briefed on common exam stress symptoms
- Post-exam debrief (2 days after): counsellor visits each class for 10 minutes; identifies distressed students early

### 9.6 Substance Abuse Protocol

- Teacher or warden reports suspected substance use → counsellor opened a case
- First response: non-judgmental assessment; build trust before intervention
- Severity: recreational (early stage) vs dependent vs overdose
- Referral: to de-addiction centre for medium/high severity
- Parent communication: counsellor-mediated; timing depends on severity and student's age/consent
- Follow-up: weekly sessions; slip monitoring; 6-month tracking
- Harm reduction approach (evidence-based) for cases where abstinence not immediately achievable

---

## 10. Reporting & Compliance

### 10.1 Counsellor Activity Report

Monthly report visible to Principal:

| Metric | Detail |
|--------|--------|
| Sessions conducted | Individual / group / family / crisis |
| New cases opened | By severity level |
| Active cases | Current caseload |
| Cases closed | With outcome summary |
| External referrals made | Psychiatrist / psychologist / de-addiction |
| Crisis events | Level 3/4 count |
| Programme participants | Group programme enrolment + completion |
| No-show rate | % of scheduled sessions not attended |

Counsellor identity visible in report. Student names not included — anonymised case IDs.

### 10.2 NAAC Criterion 5.2 Auto-Report

Required data auto-computed:
- Number of students counselled per year (unique student count)
- Number of career guidance sessions conducted
- Number of psychoeducation workshops
- Number of anti-ragging sessions
- Number of POCSO awareness sessions
- CWSN students with IEP count

Exported in NAAC format for SSR submission.

### 10.3 Annual Welfare Report

Submitted to management (no student names):
- Total cases by type (academic / personal / career / CWSN / crisis)
- Severity distribution
- Outcome distribution (resolved / referred / ongoing)
- Programme completion rates
- EWS signal analysis: most common triggers
- Counsellor-to-student ratio vs benchmark
- Recommendations for next year

### 10.4 Regulatory Compliance Tracker

| Requirement | Tracking |
|------------|---------|
| POCSO training (all counsellors) | Certificate stored; renewal alert |
| RCI registration (special educators) | Registration number; expiry alert |
| Anti-ragging awareness session | Annual; attendance log |
| POCSO awareness sessions | Annual per grade; attendance log |
| ARC quarterly meeting | Minutes stored; overdue alert |
| UGC annual self-declaration | Submission date; reference number |
| Mental health policy review | Annual; Principal sign-off |

### 10.5 DPDPA Compliance for Session Data

- Session notes: classified as sensitive personal data under DPDPA 2023
- Storage: encrypted at rest (AES-256); access restricted to counsellor + Principal
- Access log: every read/write to case file logged in Module 42
- Retention: 3 years post-graduation (or 3 years post-last-session if student left early)
- Deletion: after retention period, case files anonymised (name, ID removed; aggregate data retained)
- Data principal rights: student can request a summary of what is stored (not full therapeutic notes)

---

## 11. Parent Engagement

### 11.1 Parent Communication Rules Per Case

Counsellor sets parent notification level at case opening:

| Notification Level | When Used | What Parents Receive |
|-------------------|-----------|---------------------|
| Routine (no contact) | Minor/episodic concern | Nothing unless requested |
| Periodic (summary) | Active case, medium severity | Term-end brief summary |
| Regular (ongoing updates) | High severity; minor student | Fortnightly check-in call |
| Immediate (crisis) | Level 3/4; mandatory reporting | Same-day call + follow-up letter |

### 11.2 Family Session

- Student must consent (if 18+); counsellor facilitates
- Parent cannot access individual session notes without student consent (DPDPA + ethical practice)
- Minors: parent may be included at counsellor's discretion for case benefit
- Family session notes: separate from individual session notes; labelled as "Family session"

### 11.3 Parent Workshop

Offered twice per year:
- Topics: exam anxiety management for parents, teenage communication, social media safety, recognising depression in children
- Invitation via Module 35 (notification) + Module 37 (email)
- Attendance logged (parent ID + student link)
- Feedback collected; content updated annually

### 11.4 Parent Concern Intake

Parent submits concern via app:
- About: child's emotional state / academic pressure / peer issues / other
- Routed to assigned counsellor
- Acknowledged within 48 hours
- Counsellor decides action: open case / schedule session / reply to parent with guidance

### 11.5 Parental Consent for Minors

- All counselling of under-18 students requires parental consent before first session
- Exceptions: acute crisis (life-threatening); mandatory reporting situations
- Consent stored with timestamp; revocable by parent; counsellor notified on revocation
- Revocation during active case: counsellor completes crisis safety plan (if applicable) before closing

---

## 12. Strategic Features

### 12.1 Early Warning System — Detailed Logic

EWS score computed weekly per student (see §9.1):
- All signals normalised to 0–100
- Weighted composite score
- If score < 40 for 2 consecutive weeks → amber auto-flag
- If score < 20 any week → red auto-flag
- Counsellor receives daily digest: new amber + red students
- EWS dashboard: searchable by class, hostel block, gender, date range
- EWS trend: is institution-wide score improving or declining? Useful for management

### 12.2 Counsellor Burnout Monitoring

Counsellors face vicarious trauma from crisis caseload:
- Monthly caseload report per counsellor: total active cases + Level 3/4 cases in month
- If Level 3/4 cases > 3 in a month → supervision session auto-triggered
- If active caseload > 150% of recommended capacity → Principal alerted: need additional counsellor
- Annual counsellor self-assessment: provided to Principal; confidential
- External supervisor: institution may engage external clinical supervisor for counsellors; schedule tracked

### 12.3 Programme Effectiveness Evaluation

Each group programme evaluated:
- Pre-programme WHO-5 well-being score + post-programme score
- Attendance completion rate
- Student satisfaction rating (1–5 stars post-programme)
- 30-day follow-up: counsellor checks in; re-administers WHO-5
- Impact report: mean score change, completion %, satisfaction
- Programmes with < 20% mean WHO-5 improvement redesigned for next cycle
- Best-performing programmes scaled (offered to more students)

### 12.4 Counselling Access Equity Tracking

Sessions disaggregated by:
- Gender
- Class / year
- Hostel vs day scholar
- Category (SC/ST/OBC/EWS/General) — anonymised
- Course type (engineering vs arts vs commerce)

Equity report: identifies groups consistently underusing services → targeted outreach designed.

### 12.5 Re-enrolment Risk Flag

When student applies for withdrawal (Module 31 integration):
- If student has active counselling case OR recent Level 2+ crisis → counsellor alerted before withdrawal processed
- Counsellor contacts student: "We'd like to have one conversation before you decide."
- Retention rate of at-risk students who had retention conversation: tracked
- Not a barrier (student's right to withdraw respected); an additional support touchpoint

### 12.6 Crisis Simulation Drill

Annual crisis protocol drill:
- Scenario presented to counsellors, teachers, wardens
- Roles: who calls ambulance, who contacts parent, who logs actions
- Time from trigger to each action measured
- Debrief: gaps identified; protocol updated
- Drill log: date, scenario type, participants, outcomes, improvements made

### 12.7 Mental Health Month Campaign (October 10)

World Mental Health Day annual campaign:
- In-app pledge wall: students share anonymous wellness commitment
- Awareness posts: 5-day content series on app
- De-stigmatisation events: panel discussion, student art competition
- Counsellor availability extended: drop-in sessions all week
- Engagement tracked: pledge count, session bookings that week vs baseline
- Campaign impact report: submitted to NAAC as evidence of student welfare initiatives

---

## 13. Integration Map

| Module | Integration |
|--------|------------|
| Module 07 — Student Profile | Student context (read-only); career milestone written back |
| Module 11 — Attendance | Attendance trend for EWS; sick-day absences flagged to counsellor |
| Module 19 — Exam Session | IEP exam accommodations communicated (extra time, scribe) |
| Module 21 — Results | Score trend for EWS dashboard |
| Module 28 — Hostel | Well-being score input to EWS; warden referrals received; hostel room change recommended |
| Module 29 — Transport | CWSN transport accommodation flagged |
| Module 31 — Admission | Withdrawal risk flag; CWSN identified at admission |
| Module 35 — Notifications | Appointment reminders, workshop invitations, wellness nudges |
| Module 37 — Email | Parent workshop invitations, external referral letters |
| Module 41 — POCSO Compliance | Mandatory reporting; POCSO sessions log |
| Module 42 — DPDPA & Audit Log | All case file access, note creation, export logged |
| Module 49 — National Exam Catalog | Career counselling: entrance exam dates + syllabus reference |

---

## 14. Data Model (Key Tables)

```
counsellors
  id, tenant_id, staff_id, counsellor_type, qualifications,
  rci_number, rci_expiry, pocso_trained_on, caseload_capacity,
  assigned_student_groups, status, created_at

counselling_appointments
  id, student_id, counsellor_id, booking_method, booked_at,
  session_date, slot_start, slot_end, session_type, modality,
  reason_category, anonymous_token, status, reminder_sent,
  cancelled_at, cancellation_reason

counselling_sessions
  id, appointment_id, student_id, counsellor_id, conducted_at,
  duration_min, session_type, presenting_issue, observations,
  intervention, risk_score, safety_plan_updated, outcome_code,
  follow_up_date, notes_encrypted, created_at

counselling_cases
  id, student_id, counsellor_id, opened_on, status, severity,
  case_type, consent_obtained_at, consent_type,
  parent_notification_level, closed_on, closure_reason,
  handover_to, handover_notes

counselling_risk_assessments
  id, case_id, session_id, assessed_on, tool_used,
  score, level_triggered, action_taken, reviewed_by

counselling_safety_plans
  id, case_id, version, created_on, warning_signs,
  coping_strategies, trusted_contacts, professional_contacts,
  means_restriction, shared_with_parent, counsellor_id

counselling_ieps
  id, case_id, student_id, created_on, disability_type,
  udid_number, review_date, goals, accommodations,
  exam_accommodations, classroom_accommodations,
  progress_notes, reviewed_on, next_review_date

counselling_group_programmes
  id, tenant_id, programme_name, topic, counsellor_id,
  session_dates, max_participants, eligibility_criteria,
  status, pre_score_avg, post_score_avg, completion_rate

counselling_group_enrolments
  id, programme_id, student_id, enrolled_on, consent_obtained,
  sessions_attended, pre_score, post_score, completion_status

counselling_behavioural_flags
  id, student_id, flagged_by_role, concern_type, flag_date,
  description, counsellor_notified_at, action_taken

counselling_career_profiles
  id, student_id, riasec_primary, riasec_scores, aptitude_scores,
  personality_summary, assessed_on, career_clusters,
  career_decision, decision_date, updated_at

counselling_ews_scores
  id, student_id, week_start, attendance_signal, marks_signal,
  wellbeing_signal, meal_signal, discipline_signal, flag_signal,
  composite_score, status, counsellor_alerted_at

counselling_crisis_log
  id, case_id, student_id, crisis_date, level, trigger_description,
  actions_json, resolved_at, resolution_type,
  postvention_required, review_conducted_on

counselling_arc_members
  id, tenant_id, staff_id, role, appointed_on, term_end
counselling_arc_meetings
  id, tenant_id, meeting_date, agenda, attendance, minutes,
  action_items, recorded_by

counselling_referrals
  id, case_id, referral_type, referred_to, referral_date,
  referral_letter_r2_key, appointment_confirmed_at,
  follow_up_date, outcome
```

---

## Cross-Module References

- **Module 07**: Student career milestone written; context read for sessions — read + write
- **Module 11**: Attendance trend fed to EWS — read-only
- **Module 19**: IEP exam accommodations written — event write
- **Module 21**: Score trend fed to EWS — read-only
- **Module 28**: Well-being score input; warden referrals; room change recommendation — read + event write
- **Module 29**: CWSN transport accommodation note — event write
- **Module 31**: Withdrawal risk flag received; CWSN identified at admission — event read
- **Module 35**: Appointment reminders, nudges, workshop invitations — write
- **Module 37**: External referral letters, parent workshop invitations — write
- **Module 41**: POCSO mandatory reporting; awareness session logs — write
- **Module 42**: All case file access and note creation audited — write
- **Module 49**: Entrance exam dates for career counselling — read-only

---

*Module 32 complete. Next: Module 33 — PTM (Parent-Teacher Meeting).*
