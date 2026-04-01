# I-03 — Student Grievance Redressal

> **URL:** `/college/welfare/grievance/`
> **File:** `i-03-grievance.md`
> **Priority:** P1
> **Roles:** Student (S1) · Welfare Officer (S4) · Grievance Committee (S5) · Principal/Director (S6)

---

## 1. Grievance Categories

```
STUDENT GRIEVANCE REDRESSAL — GCEH
(UGC Grievance Redressal Regulations 2012 + AICTE Redressal Guidelines)

GRIEVANCE CATEGORIES:
  Category A — Academic:
    Marks / results disputes (CIE marks, result errors)
    Attendance discrepancy
    Subject teacher conduct (unfair treatment, favoritism)
    Exam irregularities
    Curriculum / timetable issues

  Category B — Administrative / Fee:
    Fee overcharging (above AFRC approved)
    Scholarship/concession not applied
    TC/document delays
    Admission discrepancy

  Category C — Welfare / Safety:
    Hostel issues (not ragging — those go to ARC)
    Mess quality
    Infrastructure (broken facilities)
    Transport issues

  Category D — Harassment / Discrimination:
    Caste-based discrimination → routes to SC/ST Cell
    Gender harassment → routes to ICC (POSH)
    Disability discrimination → routes to Welfare Officer + Principal
    Regional discrimination → Grievance Committee

ESCALATION MATRIX:
  Level 1: Concerned department (faculty/HOD) — 7-day SLA
  Level 2: Welfare Officer — 14-day SLA (if unresolved at Level 1)
  Level 3: Grievance Committee (Principal chaired) — 30-day SLA
  Level 4: Ombudsman (UGC-mandated for affiliating university) — 60 days
  External: UGC grievance portal (ugc.ac.in), AICTE student portal, Consumer Court
```

---

## 2. Grievance Register

```
GRIEVANCE REGISTER 2026–27

GRV ID  | Student          | Category | Issue                              | Status    | Days
───────────────────────────────────────────────────────────────────────────────────────────────────
GRV-001 | Arjun V.         | A        | CIE marks error (CS201 Mid-I)      | ✅ Resolved | 3
GRV-002 | Priya R.         | B        | TS ePASS not applied despite docs   | ✅ Resolved | 12
GRV-003 | Suresh T.        | C        | Hostel RO not working (Block A)    | ✅ Resolved | 2
GRV-004 | Deepa S.         | A        | Attendance marked wrong (3 days)   | ✅ Resolved | 5
GRV-005 | Anonymous        | D        | "Caste remarks by lab instructor"  | 🔄 Active   | 18
GRV-006 | Kiran M.         | B        | Exam fee charged twice             | ✅ Resolved | 1
GRV-007 | Rahul N.         | A        | Backlog result not updated JNTU    | 🔄 Active   | 8
GRV-008 | Priya K.         | C        | Girls' hostel hot water not working| ✅ Resolved | 1
...

SUMMARY 2026–27:
  Total grievances: 28
  Resolved within SLA: 24 (85.7%)
  Beyond SLA: 4 (2 complex cases, 2 JNTU-dependent)
  Pending: 2 (GRV-005 under investigation, GRV-007 awaiting JNTU portal response)

GRV-005 DETAIL (Anonymous caste remark complaint):
  Nature: Student claims lab instructor made derogatory caste remark during lab session
  Route: Anonymous → Welfare Officer (Day 1) → SC/ST Cell Coordinator (Day 2)
  Investigation: Witness statements collected (3 students present) — 2 corroborate
  Action: Warning issued to instructor; sensitisation workshop scheduled
  Status: Closed with action taken (Day 18) ✅

NAAC EVIDENCE (Criterion 5.1.3):
  Grievance mechanism documented ✅
  Register maintained ✅
  Resolution rate: 85.7% within SLA ✅ (NAAC expects ≥90% — target for improvement)
```

---

## 3. Grievance Process

```
GRIEVANCE FILING — Student Flow

STEP 1: FILING (EduForge → Welfare → Grievance → New)
  Student enters:
    Category (A/B/C/D)
    Description (max 500 characters)
    Date of incident
    Preferred resolution
    Supporting document (optional upload)
    Anonymity: [Anonymous / Named]

  Auto-routing:
    Category A → HOD of relevant department
    Category B → Welfare Officer + Finance Manager (if fee-related)
    Category C → Welfare Officer
    Category D → SC/ST Cell / ICC / Principal depending on sub-type

STEP 2: ACKNOWLEDGEMENT (automatic, within 24 hours)
  SMS + EduForge notification: "Your grievance GRV-XXX has been received.
  Expected resolution: [7/14/30] days. Track status in EduForge."

STEP 3: RESOLUTION
  Department/Welfare reviews and acts
  Status updates in EduForge: Received → Under Review → Resolved
  Resolution details: Uploaded by officer (brief description of action taken)
  Student notified: SMS + app notification

STEP 4: CLOSURE CONFIRMATION
  Student asked: "Is your grievance resolved to your satisfaction? [Yes/No]"
  If No + beyond SLA: Auto-escalated to next level
  If No + within SLA: Flagged to Welfare Officer (student can elaborate)

RIGHT TO RE-OPEN:
  Student can re-open within 15 days of "Resolved" if resolution was inadequate
  After 15 days: Treated as new grievance

ANNUAL REVIEW (IQAC):
  Grievance patterns analysed annually (anonymised)
  Top categories → systemic action at department level
  Example: 8 marks-related grievances in CSE → HOD review of CIE process
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `POST` | `/api/v1/college/{id}/welfare/grievance/` | File grievance |
| 2 | `GET` | `/api/v1/college/{id}/welfare/grievance/my/` | Student's own grievances |
| 3 | `GET` | `/api/v1/college/{id}/welfare/grievance/` | All grievances (welfare officer) |
| 4 | `POST` | `/api/v1/college/{id}/welfare/grievance/{id}/resolve/` | Mark resolved with details |
| 5 | `GET` | `/api/v1/college/{id}/welfare/grievance/analytics/` | Resolution rate analytics |

---

## 5. Business Rules

- UGC Grievance Redressal Regulations 2012 require every college to have a documented grievance mechanism; NAAC Criterion 5.1.3 evaluates this; a college that has no grievance register or cannot show resolution records scores zero on this metric; the grievance mechanism must be publicised (student handbook, website, orientation) — not just exist
- Anonymous grievances must be investigated; the anonymity protection does not prevent the institution from investigating facts independently (through witnesses, CCTV, records); a college that dismisses anonymous grievances as "unverifiable" is misusing the confidentiality framework as a shield against accountability; GRV-005 (anonymous caste remark) was resolved through independent witness statements — demonstrating the correct approach
- SLA compliance must be measured and reported; the 85.7% within-SLA rate is below the 90% NAAC target; the bottleneck is typically grievances that depend on external bodies (JNTU for results corrections, government for scholarship delays) which are outside the college's control; separating "internal SLA" from "external-dependent SLA" in reporting gives a more accurate picture to the NAAC
- Grievance patterns are institutional health indicators; 8 marks disputes in one department could mean the CIE process is flawed (marks calculation errors, biased evaluation) — this is more valuable than resolving each individual case; the IQAC's annual pattern analysis is the correct vehicle to convert grievance data into systemic improvement
- Retaliation against a student for filing a grievance is a serious institutional failure; faculty who reduce a student's attendance records or marks after the student filed a grievance have committed an act of victimisation; EduForge's grievance module timestamps the filing date — any negative academic event shortly after filing is automatically flagged for review; this prevents silent retaliation

---

*Last updated: 2026-03-27 · Group 4 — College Portal · Division I*
