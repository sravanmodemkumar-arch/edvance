# Module 41 — POCSO Compliance

## 1. Purpose

The Protection of Children from Sexual Offences Act 2012 (POCSO) is not optional, and neither is compliance with it. Every institution in India with children under 18 — from a 50-student rural primary school to a 10,000-student residential university — carries identical mandatory reporting obligations, committee formation duties, and staff vetting requirements under POCSO and its 2019/2020 amendments. Section 21 makes failure to report a criminal offence punishable with imprisonment. Yet most institutions manage POCSO compliance through paper registers, untrained secretarial staff, and annual policy printouts that nobody reads.

EduForge Module 41 is the institution's POCSO compliance nerve centre. It covers child safety committee management, the 24-hour mandatory reporting timer, incident register (encrypted, access-restricted, legally retained), in-app multilingual staff training and certification, visitor management integration, awareness programme scheduling, code of conduct acknowledgement tracking, and a one-click annual compliance report for DCPU / CBSE inspection. This module does not attempt to investigate offences — that is the exclusive domain of SJPU and courts. It ensures the institution fulfils its legal obligations and creates a documented, auditable child-safe environment.

---

## 2. Legal Framework

### 2.1 Statutes & Circulars

| Instrument | Key Obligation |
|---|---|
| POCSO Act 2012, S.19 | Every person must report suspected offence to SJPU / Police |
| POCSO Act 2012, S.21 | Failure to report → 6 months to 1 year imprisonment + fine |
| POCSO Amendment 2019, S.19A | Institution head must report within 24 hours to SJPU / DCPU |
| POCSO Rules 2020 | Mandatory child protection policy, designated personnel, awareness programmes |
| POCSO Act S.45 | Applies to residential institutions (hostels, boarding schools) |
| CBSE Circular CP/2020 | Written Child Protection Policy, Internal Child Safety Committee, annual compliance report for CBSE-affiliated schools |
| UGC Anti-Ragging Regulations 2009 | Separate Anti-Ragging Committee mandatory for colleges/universities |
| POSH Act 2013 | ICC mandatory for institutions with female employees (separate from CSC) |
| State-specific guidelines | Maharashtra, Kerala, Karnataka, Tamil Nadu have additional state child protection rules — system supports state-level configuration |

### 2.2 Key Authorities

| Authority | Role | Contact Managed In System |
|---|---|---|
| SJPU (Special Juvenile Police Unit) | Investigates POCSO offences | District-level phone pre-loaded |
| DCPU (District Child Protection Unit) | Coordinates child welfare; alternate report destination | District-level phone pre-loaded |
| CWC (Child Welfare Committee) | Orders medical examination, counselling, child placement | District-level contact pre-loaded |
| CHILDLINE 1098 | 24×7 emergency for children in danger | Pre-loaded |
| NCPCR | National oversight; complaints about institution non-compliance | Website URL stored |

### 2.3 Mandatory Reporters

Under POCSO S.19, mandatory reporters include ALL institution personnel:
- Teaching staff (full-time, part-time, visiting)
- Non-teaching staff (admin, peons, security)
- Hostel wardens and attendants
- Bus drivers and attendants
- Canteen / housekeeping vendor staff on campus
- Third-party contractual staff with campus access

Ignorance of law is not a defence. Every person above is trained and holds a signed acknowledgement of their reporting obligation.

---

## 3. Child Safety Committee (CSC)

### 3.1 Composition & Roles

```
┌─────────────────────────────────────────────────────────┐
│  Child Safety Committee (CSC)                           │
├──────────────────────────┬──────────────────────────────┤
│  Role                    │  Person                      │
├──────────────────────────┼──────────────────────────────┤
│  Chairperson             │  Principal / Vice Principal  │
│  Secretary               │  School Counsellor (trained) │
│  Member — Teaching       │  Senior Teacher (woman)      │
│  Member — Teaching       │  Senior Teacher (any gender) │
│  Member — Parent         │  PTA representative          │
│  Member — External Expert│  Child rights NGO / expert   │
└──────────────────────────┴──────────────────────────────┘
```

External expert must be a person not employed by the institution. Their presence in CSC meetings is mandatory (quorum includes external member).

### 3.2 CSC Meeting Management

- Minimum 4 meetings per academic year (quarterly)
- Meeting agenda template — pre-populated by system:
  1. Awareness programme status (sessions completed / pending)
  2. Staff training compliance (% trained)
  3. Incident review (anonymised counts — no names)
  4. Visitor management and CCTV health check
  5. Policy review (any updates needed)
  6. Action items from previous meeting
- Minutes recorded in system: date, attendees (attendance logged), decisions, action items, next meeting date
- System alerts CSC Chairperson if a quarter passes without a meeting being logged

### 3.3 CSC Compliance Dashboard

```
┌─────────────────────────────────────────────────────────┐
│  CSC Status — Academic Year 2025-26                     │
├──────────────────────────────────────┬──────────────────┤
│  Metric                              │  Status          │
├──────────────────────────────────────┼──────────────────┤
│  Meetings held (required: 4)         │  3 / 4           │
│  Next meeting due                    │  Mar 31 ⚠️       │
│  External expert attended all        │  ✅              │
│  Minutes filed                       │  3 / 4           │
│  Annual report submitted to DCPU     │  Pending         │
└──────────────────────────────────────┴──────────────────┘
```

---

## 4. Child Protection Policy

### 4.1 Policy Lifecycle

```
DRAFT (admin drafts in system)
    ↓
REVIEW (CSC Chairperson + Principal review)
    ↓
APPROVED (management committee / trust approval logged)
    ↓
PUBLISHED (PDF generated; published to website URL; emailed to parents)
    ↓
ACKNOWLEDGED (all staff sign digitally; tracked)
    ↓ (after 12 months)
REVIEW DUE (system alerts; annual revision cycle begins)
```

### 4.2 Mandatory Policy Sections

System validates that the policy document covers all mandatory sections before marking it APPROVED:

1. Scope and applicability (who is a child; who is covered)
2. Prohibited staff behaviours (enumerated list)
3. Child-safe physical environment standards
4. Reporting mechanism (internal + external)
5. Investigation protocol (what institution does after report)
6. Visitor management
7. Social media and digital safety
8. Anti-grooming provisions
9. Sanctions for policy violation
10. Annual review commitment

### 4.3 Policy Acknowledgement Tracking

Every staff member — on joining and every subsequent August — signs the Child Protection Policy digitally:

```
"I have read and understood the Child Protection Policy of [Institution Name]
 (Version [X], dated [Date]). I understand my obligations as a mandatory reporter
 under POCSO Act 2012 and commit to comply with this policy."
[Sign digitally] [Date]
```

Status tracked per staff:
- Not Signed (new staff: must sign within 7 days)
- Signed (with timestamp and version)
- Overdue (not signed 15 days after due date — alert to Principal)

---

## 5. Mandatory Reporting System

### 5.1 Incident Intake

The incident intake form is accessible to every staff member from the "Report a Concern" button in the app (visible in the navigation to all roles):

```
Report a Child Safety Concern
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Your identity (optional — anonymous reports are equally valid)
● Identified (your name will be shared with CSC only)
○ Anonymous

Nature of concern:
○ Physical/sexual offence (POCSO)
○ Harassment / bullying
○ Grooming or suspicious adult behaviour
○ Online/cybersexual concern
○ Other

Location of incident: [classroom / hostel / bus / online / other]
Approximate date/time: [date picker]
Brief description: [text field — 500 char max]
Persons involved (describe, do not name in writing):
  Accused (role): [staff / student / visitor / unknown]
  Child (class / age group): [dropdown — no name]
Any witnesses: [Yes / No — do not record names here]

[Submit — I understand this triggers a mandatory review]
```

### 5.2 24-Hour Mandatory Reporting Timer

```
Incident created at: 10:30 AM, 26 Mar 2026
Mandatory police report by: 10:30 AM, 27 Mar 2026

[===========50%==========] ← real-time progress bar

⏰ Alert sent to Principal and CSC Chairperson at: 6:30 AM (20-hour mark)
🚨 Alert sent to Super Admin at: 9:30 AM (23-hour mark)
```

Timer stops when admin logs:
- SJPU report reference number, OR
- DCPU acknowledgement reference, OR
- CHILDLINE 1098 reference (Level 3 immediate danger)

If timer expires without log entry: Super Admin receives critical alert; incident marked OVERDUE_REPORT with full audit trail preserved.

### 5.3 Report-to-Authority Logging

```
Police Report Filed
━━━━━━━━━━━━━━━━━━
Authority:          SJPU, [District]
Officer name:       (optional)
Station:            [police station name]
FIR / Acknowledgement reference: [text]
Date and time filed: [datetime]
Filing method:      ○ In person  ○ Online portal  ○ Phone (written follow-up pending)
Attachment:         [Upload FIR copy or acknowledgement — Module 40 storage]
[Save]
```

### 5.4 Evidence Preservation Alert

On incident creation, the system automatically:
1. Sends push notification to IT Admin: "CCTV footage preservation required — [location], [date], [time window]"
2. Logs the alert as a task in IT Admin's queue with 2-hour deadline
3. IT Admin confirms footage preserved (checked and logged)
4. Footage retention extended to 90 days (vs. standard 30 days)

This does not technically preserve the footage — it alerts the human responsible. Institutions using Module 29 / third-party DVR integration can trigger footage lock via API in Phase 2.

---

## 6. Staff Training System

### 6.1 Course Structure

| Module | Topic | Duration |
|---|---|---|
| 1 | POCSO Act — Key Sections & Penalties | 15 min |
| 2 | Recognising Abuse — Behavioural Indicators, Disclosure Handling | 15 min |
| 3 | Mandatory Reporting — Who, When, How (SJPU / DCPU process) | 10 min |
| 4 | Code of Conduct — Prohibited Behaviours, Child-Safe Standards | 10 min |
| 5 | Cybersafety & Digital Grooming — Online Offences, Platform Safety | 10 min |
| Assessment | 20 MCQ — 80% passing score | 15 min |

Total: ~75 minutes for initial training.

Annual refresher: Modules 3 + 4 + updated content (30 min) + 10-question assessment.

### 6.2 Languages Available

Hindi, Marathi, Telugu, Tamil, Kannada, Bengali, Odia, English — staff selects at first login; can change any time.

### 6.3 Assessment & Certification

- 20 MCQ; 80% (16/20) to pass
- Immediate score display; remedial content shown for wrong answers (which module to re-read)
- Failed: mandatory re-attempt; no limit on attempts; all attempts logged
- Passed: certificate PDF auto-generated with: staff name, institution, date, training version, score
- Certificate stored in Module 40 under staff documents
- Training version — when course is updated (legislative amendment), staff must re-take the updated modules and assessment

### 6.4 Compliance Tracking

```
Staff POCSO Training Compliance — 2025-26

Teaching Staff: 98/102 trained ██████████████████░░ 96%
  Overdue (joined > 7 days ago, not trained):
    → Venkat Rao (joined 20 Mar)
    → Sujatha K (joined 22 Mar)

Non-Teaching Staff: 43/45 trained █████████████████░░ 96%
Vendor Staff: 12/14 trained ████████████████░░░ 86%

Target: 100% by 31 August 2026
```

---

## 7. Code of Conduct — Staff

### 7.1 Conduct Rules

All staff acknowledge the following code at joining and annually:

| Prohibited Behaviour | Rationale |
|---|---|
| One-on-one meeting with a child in a closed room | Eliminates opportunity for unwitnessed offence |
| Physical contact beyond age-appropriate (shoulder, handshake) | Prevents normalisation of unsafe touch |
| Sharing personal phone / email / social media with students | Removes private communication channel |
| Private messaging with students on personal platforms | Only school-managed channels allowed |
| Transporting students in personal vehicle | Unmonitored environment |
| Photographing / recording students without stated educational purpose and parent consent | Privacy and exploitation risk |
| Sharing student photos on personal social media | Uncontrolled distribution |
| Asking students about family income, parental relationship, personal matters beyond welfare | Grooming pattern |

### 7.2 Conduct Violation Reporting

Staff can report a colleague's conduct violation:
- Via "Report a Concern" form (same form as incident report; nature → "Suspicious adult behaviour")
- Reports go to CSC Chairperson inbox
- CSC investigates without disclosing reporter identity (reporter protected under POCSO S.19 — no retaliation permitted)

Students and parents can also report conduct violations via the anonymous form (Section 5).

---

## 8. Visitor Management

### 8.1 Visitor Log

```sql
CREATE TABLE visitor_log (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id       UUID NOT NULL REFERENCES tenants(id),
  campus_id       UUID REFERENCES campuses(id),
  visitor_name    TEXT NOT NULL,
  id_type         TEXT NOT NULL,    -- Aadhaar, PAN, DL, Passport
  id_number       TEXT NOT NULL,    -- stored hashed (DPDPA)
  purpose         TEXT NOT NULL,
  accompanied_by  UUID REFERENCES staff(id),    -- escort staff
  entry_time      TIMESTAMPTZ NOT NULL,
  exit_time       TIMESTAMPTZ,
  badge_number    TEXT,
  areas_permitted TEXT[],           -- ['admin_block', 'main_hall']
  flag            BOOLEAN DEFAULT FALSE,    -- flagged by security staff
  flag_reason     TEXT,
  logged_by_id    UUID NOT NULL REFERENCES users(id)
);
```

### 8.2 Authorised Pickup Verification

When a parent/guardian arrives to pick up a student:

1. Security checks name against student's authorised adult list (sourced from Module 09)
2. Photo ID checked against the photo stored in Module 09
3. For new / unregistered adults: parent must call / WhatsApp confirmation to admin first
4. Emergency pickup by unregistered adult: verbal password (configured by parent at admission) + parent phone confirmation
5. Every pickup logged with pickup adult name, time, staff who verified

### 8.3 CCTV Coverage Policy

| Location | CCTV Required | CCTV Prohibited |
|---|---|---|
| All entry / exit points | ✅ | — |
| Corridors and common areas | ✅ | — |
| Classrooms | Optional (institution choice) | — |
| Canteen and library | ✅ | — |
| Parking area | ✅ | — |
| Washrooms and changing rooms | ❌ | Yes — strictly prohibited |
| Medical / counselling room | ❌ | Yes — strictly prohibited |
| Hostel individual rooms | ❌ | Yes — strictly prohibited |
| Hostel corridors and common room | ✅ | — |

CCTV camera locations documented in the system; annual review by CSC ensures no camera is installed in prohibited areas.

---

## 9. Awareness Programme Management

### 9.1 Age-Band Programme Library

| Age Band | Key Topics | Duration |
|---|---|---|
| 4–6 years | Good touch / bad touch; safe body rules; trusted adults | 30 min (interactive) |
| 7–11 years | Body autonomy; safe secrets vs. unsafe secrets; how to report | 45 min |
| 12–14 years | Consent; online safety; recognising grooming; peer pressure | 60 min |
| 15–18 years | Digital privacy; healthy relationships; legal rights; POCSO S.19 (students as reporters too) | 60 min |

### 9.2 Programme Scheduling

- Admin schedules sessions per class / age group at year start (June/July)
- System sends calendar reminder to facilitator (counsellor or external NGO resource person) 7 days before
- Session attendance logged per student (PRESENT / ABSENT)
- Students who missed session (absent on that day) are tracked; rescheduled session offered

### 9.3 Parent Awareness

At each annual PTM (Module 33):
- CSC Secretary or counsellor delivers a 15-minute POCSO parent awareness talk
- Topics: how to talk to your child about body safety; how to approach school if child discloses; school's reporting obligation
- PTM attendance logged (Module 33) — automatically contributes to compliance report

### 9.4 Trust Teacher System

- Each class has one designated Trust Teacher
- Trust Teacher name displayed in classroom (printed card) and in student's app home screen
- Trust Teacher receives additional 4-hour training: trauma-informed listening, non-leading response techniques, referral protocol
- On child disclosure: Trust Teacher listens without interrogating; does not promise confidentiality; immediately informs counsellor; fills Level 0 incident form
- Rotation: annually in April; overlap period — outgoing TT informs incoming TT about any ongoing concerns (sanitised)

---

## 10. Hostel-Specific POCSO Provisions

### 10.1 Warden Requirements

| Hostel Type | Minimum Staff Requirement |
|---|---|
| Girls' hostel | Female warden (24×7); no male staff in girls' sections after 10 PM except emergency |
| Boys' hostel | Any-gender warden; at least one female staff accessible on floor during waking hours |
| Co-ed hostel | Separate floors / wings; separate wardens for each section |

### 10.2 Room Visit Protocol

- Routine welfare checks — same-gender staff only; door remains open during check
- Emergency visit by opposite-gender staff — only with another staff escort; event logged immediately
- Maintenance / repair in student rooms — only during daytime; at least one warden present; entry logged

### 10.3 Visitor Policy in Hostel

- Visitors (including parents) — common room only, during visiting hours (configurable; default 4 PM–6 PM on weekdays)
- Opposite-gender visitors — common room only; never in student rooms
- All hostel visitors logged in visitor log (Section 8.1)

### 10.4 SOS Integration

When a student triggers the hostel SOS button (Module 28):
- Duty warden alert includes a POCSO protocol card:
  - "If child reports sexual harm: Do NOT touch / examine child. Call CHILDLINE 1098. Inform Principal."
  - SJPU phone, DCPU phone, CHILDLINE 1098 displayed prominently

---

## 11. Digital Safety & Cybersexual Offences

### 11.1 POCSO Coverage of Online Offences

POCSO S.11(iv): showing pornographic content to a child, grooming via electronic means, and cybersexual offences are POCSO offences, not merely IT Act offences. Penalty: rigorous imprisonment up to 3 years (S.12).

### 11.2 Platform-Level Safeguards

On EduForge-managed communication channels:

- Private messages between a staff account and a student account are flagged if volume exceeds a configurable threshold (e.g., > 20 private messages in a day to the same student)
- Flag generates a CSC Chairperson alert: "Unusual messaging pattern: [staff role] → [student class] — 28 messages on [date]"
- Flag is informational only; CSC reviews
- All staff-to-student private messages are stored for 90 days for investigation access (staff are informed of this in the code of conduct)

### 11.3 Cybersafety Curriculum

2 sessions per year per class — coordinated with awareness programme calendar:

| Session | Topics |
|---|---|
| Session 1 (July) | Online safety basics; what is grooming; how to report online harm |
| Session 2 (January) | Social media risks; privacy settings; cyberbullying; sexting awareness (age 13+) |

Sessions conducted by school counsellor or certified cyber-safety facilitator; attendance logged.

---

## 12. Incident Register (Secure)

### 12.1 Access Control

Incident register has its own access control layer, independent of the general RBAC:

| Role | Access |
|---|---|
| Principal | Full read + approve reports |
| CSC Chairperson | Full read + write |
| Super Admin | Full read (for compliance audit) |
| All other roles | NO ACCESS — not even metadata |

Even the HR Manager and Vice Principal cannot see incident records without explicit Super Admin grant (logged).

### 12.2 Schema

```sql
CREATE TABLE pocso_incidents (
  id                    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id             UUID NOT NULL REFERENCES tenants(id),
  incident_ref          TEXT NOT NULL UNIQUE,      -- INC-2026-0001
  knowledge_timestamp   TIMESTAMPTZ NOT NULL,       -- when institution learned
  incident_type         TEXT NOT NULL,              -- sexual_offence / harassment / voyeurism / grooming / cybersexual / other
  accused_type          TEXT NOT NULL,              -- staff / student / visitor / unknown
  victim_anon_id        TEXT NOT NULL,              -- one-way hash; only principal can reverse via separate lookup
  location_type         TEXT,                       -- classroom / hostel / bus / online / offcampus
  description           TEXT NOT NULL,              -- encrypted AES-256
  csc_action            TEXT,                       -- Level 0/1/2/3 response taken
  police_reported       BOOLEAN DEFAULT FALSE,
  police_report_ref     TEXT,                       -- FIR / acknowledgement number
  police_reported_at    TIMESTAMPTZ,
  dcpu_reported         BOOLEAN DEFAULT FALSE,
  dcpu_report_ref       TEXT,
  medical_referral      BOOLEAN DEFAULT FALSE,
  counselling_provided  BOOLEAN DEFAULT FALSE,
  accused_suspended     BOOLEAN DEFAULT FALSE,
  case_status           TEXT DEFAULT 'UNDER_INVESTIGATION',
  -- UNDER_INVESTIGATION / CLOSED_ACQUITTED / CLOSED_CONVICTED / CLOSED_NO_BASIS / PENDING_COURT
  closed_at             TIMESTAMPTZ,
  closure_notes         TEXT,                       -- encrypted
  retention_until       DATE,                       -- closed_at + 7 years
  legal_hold            BOOLEAN DEFAULT TRUE,       -- always true; cannot be false
  created_by_id         UUID NOT NULL REFERENCES users(id),
  created_at            TIMESTAMPTZ DEFAULT now(),
  updated_at            TIMESTAMPTZ DEFAULT now()
);

-- Separate victim lookup table — even more restricted
CREATE TABLE pocso_victim_lookup (
  anon_id               TEXT PRIMARY KEY,
  tenant_id             UUID NOT NULL,
  student_id            UUID NOT NULL REFERENCES students(id),
  can_decode_roles      TEXT[] DEFAULT ARRAY['principal', 'csc_chairperson']
);

-- Incident access audit (every view / edit)
CREATE TABLE pocso_incident_access_log (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  incident_id     UUID NOT NULL REFERENCES pocso_incidents(id),
  accessed_by_id  UUID NOT NULL REFERENCES users(id),
  access_type     TEXT NOT NULL,    -- VIEW / EDIT / EXPORT
  purpose         TEXT,
  accessed_at     TIMESTAMPTZ DEFAULT now(),
  ip_address      INET
);
```

### 12.3 Anonymised Reporting Statistics

For annual compliance report (Section 14), incident data is aggregated:
- Total concerns logged (count)
- Level 1/2/3 incidents (count)
- Police reports filed (count)
- Cases closed (count and disposition)
- NO individual identifiers in any aggregated output

---

## 13. Physical Display Requirements

### 13.1 Mandatory Notices

| Notice | Minimum Size | Locations | Language |
|---|---|---|---|
| Child Safety Committee members + contact numbers | A3 | Every building entrance; canteen; library | English + Regional |
| CHILDLINE 1098 | A2 | Every classroom; 5+ common locations | English + Regional |
| Anonymous complaint procedure | A4 | Near complaint boxes | English + Regional |
| POCSO awareness poster (key provisions) | A2 | Entrance; staffroom | English + Regional |
| Safe School Declaration | A3 | Main entrance | English |

### 13.2 Digital Notice Board Integration

Module 34 (Announcements) auto-rotates POCSO awareness slides on digital display boards:
- "Know your rights" slide for students — shown every 3rd rotation
- CSC contact card — shown every 5th rotation
- CHILDLINE 1098 — permanent footer on all digital boards

Annual circular: Module 34 system generates the mandatory annual POCSO / anti-ragging circular (for colleges) as a system-triggered event at year start.

---

## 14. Annual Compliance Report

### 14.1 Report Contents

System auto-populates the annual POCSO compliance report:

```
EduForge — POCSO Annual Compliance Report
Institution: [Name]   Academic Year: 2025-26   Date: [date]

1. Child Safety Committee
   - Members listed (names, roles)
   - Meetings held: 4 / 4 (required) ✅
   - External expert attendance: 4 / 4 ✅

2. Child Protection Policy
   - Version: [X]   Approved: [date]   Published: [date]
   - Staff acknowledgement: 98 / 100 (98%) ⚠️ 2 pending

3. Staff Training
   - Teaching staff trained: 102 / 102 (100%) ✅
   - Non-teaching staff trained: 45 / 45 (100%) ✅
   - Vendor staff trained: 13 / 14 (93%) ⚠️

4. Awareness Programmes
   - Student sessions held: 24 (8 per age group × 3 age groups)
   - Student coverage: 98%
   - Parent sessions held: 2 (at PTMs)

5. Police Verification
   - Staff with valid police verification: 145 / 148 (98%)
   - Expiring in next 90 days: 3

6. Incident Register (Aggregated)
   - Concerns logged: [N]
   - Level 1/2/3 incidents: [N]
   - Police reports filed: [N]
   - Cases closed: [N]

7. Declaration
   Principal signature: ___________
   Date: ___________
```

### 14.2 Report Submission Tracking

- Report generated as PDF; reviewed and signed by Principal digitally
- Submitted to: DCPU (where mandated) and/or kept on record for CBSE inspection
- Submission date, submitted-to, acknowledgement reference stored
- Stored in Module 40 (institutional documents, POCSO category)

---

## 15. Notices Display & Print Manager

Admin can print all mandatory notices directly from the system:

```
Print Centre — POCSO Notices
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Print] CSC Member Notice (A3, English + Telugu)
[Print] CHILDLINE 1098 Poster (A2, English + Telugu)
[Print] Anonymous Complaint Procedure (A4, English)
[Print] POCSO Awareness Poster (A2, English + Telugu)
[Print] Safe School Declaration (A3, English)
[Print] All notices — combined PDF (5 pages)
```

Notices auto-populate with current CSC member names and contact numbers from the system.

---

## 16. RBAC Matrix

| Action | Any Staff | CSC Secretary | CSC Chairperson | Principal | Super Admin |
|---|---|---|---|---|---|
| Report a concern | ✅ | ✅ | ✅ | ✅ | ✅ |
| View incident register | ❌ | ✅ (created by or assigned) | ✅ | ✅ | ✅ |
| Create incident record | ✅ (concern only) | ✅ | ✅ | ✅ | ✅ |
| Log police report reference | ❌ | ✅ | ✅ | ✅ | ✅ |
| Suspend accused staff (RBAC) | ❌ | ❌ | Recommend | ✅ | ✅ |
| View victim identity (reverse anon) | ❌ | ❌ | ✅ | ✅ | ✅ |
| Generate compliance report | ❌ | ✅ | ✅ | ✅ | ✅ |
| Manage CSC members | ❌ | ❌ | Recommend | ✅ | ✅ |
| View training compliance | ❌ | ✅ | ✅ | ✅ | ✅ |
| Print notices | ❌ | ✅ | ✅ | ✅ | ✅ |
| Place legal hold on incident | ❌ | ❌ | ❌ | ❌ | ✅ |

---

## 17. API Reference

```
# Incident management (restricted)
POST   /api/v1/pocso/incidents/               # Report concern
GET    /api/v1/pocso/incidents/{id}/          # View incident (access-controlled)
PATCH  /api/v1/pocso/incidents/{id}/          # Update incident
PATCH  /api/v1/pocso/incidents/{id}/log-police-report/   # Log FIR reference
PATCH  /api/v1/pocso/incidents/{id}/close/    # Close case

# CSC management
GET    /api/v1/pocso/csc-members/             # Current CSC roster
PUT    /api/v1/pocso/csc-members/             # Update CSC roster
POST   /api/v1/pocso/csc-meetings/            # Log CSC meeting
GET    /api/v1/pocso/csc-meetings/            # Meeting history

# Training
GET    /api/v1/pocso/training/status/         # Own training status
POST   /api/v1/pocso/training/start/          # Begin course
POST   /api/v1/pocso/training/submit-assessment/  # Submit MCQ answers
GET    /api/v1/pocso/training/compliance/     # Admin — all staff status

# Awareness programmes
POST   /api/v1/pocso/awareness-sessions/      # Schedule session
PATCH  /api/v1/pocso/awareness-sessions/{id}/attendance/  # Log attendance

# Compliance
GET    /api/v1/pocso/compliance-dashboard/    # Full compliance overview
POST   /api/v1/pocso/annual-report/generate/  # Generate annual report PDF
GET    /api/v1/pocso/annual-report/{id}/download-url/    # Download report

# Anonymous complaint (no auth)
POST   /api/v1/public/pocso/anonymous-complaint/         # Submit anonymous concern
GET    /api/v1/public/pocso/anonymous-complaint/{tracking_id}/  # Check status
```

---

## 18. DPDPA 2023 Compliance

### 18.1 Incident Record Classification

POCSO incident records are classified at the highest sensitivity level — above all other data categories:

- Encrypted at rest: AES-256, separate encryption key per tenant, keys in AWS KMS
- Encrypted in transit: TLS 1.3 minimum
- Field-level encryption for incident description and victim anon_id
- Stored in a physically separate schema partition (`pocso_secure`) with row-level security in PostgreSQL

### 18.2 Retention & Legal Hold

- Retention: 7 years from case closure (legal mandate under evidence preservation principles)
- Legal hold: auto-applied to ALL incident records; cannot be removed by any role without Board of Management resolution + Super Admin manual override (both logged)
- Right to erasure under DPDPA: does NOT apply to POCSO incident records; legal obligation to retain for court / investigation supersedes DPDPA erasure right (DPDPA S.17 — exemption for law enforcement purposes)

### 18.3 Access Logging

Every access to any POCSO incident record is logged with: user ID, timestamp, access type (VIEW/EDIT/EXPORT), IP address, purpose. Logs retained for the life of the incident record. Logs themselves cannot be deleted.

### 18.4 Data Minimisation

The anonymous complaint form collects minimum data — nature, location, time window, description of persons (roles, not names). Identity of complainant is truly anonymous — no session cookie, no IP logging (Cloudflare terminates at CDN level; backend receives only anonymised origin).

---

## 19. Analytics

### 19.1 Compliance Score (Institution-Level)

```
POCSO Compliance Score — 2025-26

Staff Training                   [████████████████████] 100%
Policy Acknowledgement           [████████████████████]  98%
CSC Meetings (Quarterly)         [███████████████░░░░░]  75%  ← 3/4 held
Awareness Programmes (Students)  [████████████████████]  98%
Police Verification (Current)    [███████████████████░]  97%
Parent Awareness Sessions        [████████████████████] 100%

Overall Compliance Score         [███████████████████░]  95%
```

Overall score drives NAAC Criterion 5.3 (Student Support) and CBSE inspection readiness.

### 19.2 Training Analytics

- Completion rate by department / role group
- Average time to complete course (from joining to certification)
- Assessment failure rate by module (identifies which POCSO topic is least understood → refresh content)
- Language distribution (which regional language most used)

### 19.3 Response Time Analytics

- Average time from incident knowledge to SJPU report (target: < 24 hours; track trends)
- Average time from concern (Level 0) to formal incident classification (target: < 2 hours)
- Cases where 24-hour deadline was breached (should be zero)

---

## 20. Cross-Module Integration Map

| Module | Integration |
|---|---|
| Module 03 — RBAC | Accused staff account suspended immediately on Level 2+ incident; suspension logged with incident reference |
| Module 07 — Student Enrolment | Student POCSO case flag (internal; non-PII in profile); feeds Module 32 EWS |
| Module 08 — Staff BGV | Police verification status and expiry tracked here; BGV completion gate at joining |
| Module 09 — Parent/Guardian | Authorised pickup list for visitor management; parent contact for incident notification |
| Module 28 — Hostel | Female warden requirement enforced; SOS integration; hostel visitor log; CCTV policy |
| Module 29 — Transport | Female attendant tracking for primary buses; no-stranger alert |
| Module 32 — Student Welfare | Counsellor response for Level 1/2 incidents; postvention support for affected students; Level 3 crisis protocol |
| Module 33 — PTM | Parent POCSO awareness session recorded in PTM attendance |
| Module 34 — Announcements | Digital notice board rotation; mandatory annual circulars |
| Module 40 — Document Management | POCSO committee constitution; training certificates; policy versions; incident export (watermarked) |
| Module 42 — DPDPA & Audit Log | Every incident record access event; every training record change; all access logs |

---

*Module 41 — POCSO Compliance — EduForge Platform Specification*
*Version 1.0 | 2026-03-26*
