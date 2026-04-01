# E-02 — Campus Drive Management

> **URL:** `/college/placement/drives/`
> **File:** `e-02-campus-drive.md`
> **Priority:** P1
> **Roles:** Placement Officer (S3) · Training & Placement Coordinator (S4) · Faculty Advisor — Placement (S3)

---

## 1. Drive Calendar

```
CAMPUS DRIVE CALENDAR — 2026–27
(Final year placement season)

SEASON STATUS: Active (Aug 2026 – Apr 2027)

COMPLETED DRIVES:
  Aug 2026: TCS (placed 28), Wipro (placed 12), Accenture (placed 8)
  Sep 2026: Cognizant (placed 6), Mphasis (placed 4), HCL (placed 9)
  Oct 2026: Infosys (placed 14), Deloitte (placed 5), Goldman Sachs (placed 2)
  Nov 2026: Amazon (Online — placed 1), Microsoft (placed 1 — intern-to-PPO)
  Dec 2026: Persistent Systems (placed 7)
  Jan 2027: BHEL (PSU — placed 3 via GATE score)
  Feb 2027: Various (placed 22 aggregate — smaller companies)
  Mar 2027: ONGC (scheduled 30 Mar), Startup batch (4 companies — scheduled Apr)

UPCOMING:
  30 March 2027: ONGC PSU drive (GATE-based — only ECE/EEE/Mech eligible)
  2 April 2027:  RetailTech Solutions (E-commerce analytics, Tier 2)
  5 April 2027:  Startup Block (4 companies in single day — rotating interview slots)

SEASON TOTALS TO DATE:
  Companies visited: 23
  Students appeared: 894 (multiple students appear in multiple drives)
  Students placed: 224 / 332 (67.5% placement rate — as of 27 March 2027)
  Students with multiple offers: 38 (11.4% — must release other pipeline slots)
```

---

## 2. Drive Detail

```
DRIVE DETAIL — Infosys Campus Drive
Drive ID: DR-2027-018
Date: 15 October 2026
Venue: GCEH Seminar Hall + Computer Lab 3
Coordinator: Ms. Priya Reddy (Placement Officer)

SCHEDULE:
  8:00 AM:  Company PPT (Infosys overview, role details)
  9:00 AM:  Online aptitude test (InfyTQ platform — college systems)
  11:30 AM: Result announcement (shortlisted for technical interview)
  12:00 PM: Lunch break
  1:00 PM:  Technical interviews (Panel 1: Java/DSA; Panel 2: Analytics track)
  4:00 PM:  HR interviews (shortlisted after technical)
  5:30 PM:  Provisional offer list

STUDENT APPLICATIONS: 198 students applied (registered)
ELIGIBILITY VERIFIED: 194 eligible (4 ineligible — CGPA/backlog)
APPEARED FOR TEST: 189 (5 absent — notified with reason)

APTITUDE TEST:
  Platform: InfyTQ (Infosys-managed online platform)
  Duration: 90 minutes
  Sections: Verbal (20Q), Quantitative (20Q), Logical (20Q), Coding (2 problems)
  Cutoff (Infosys decided): 60% aggregate (not disclosed to college before test)

RESULTS:
  Shortlisted for Technical: 42 students (22.2% of appeared)
  Cleared Technical: 28 students
  Cleared HR: 24 students (4 rejected in HR — attitude/communication)
  Offers extended: 24
  Offers accepted: 22 (2 declined — preferred other company)

FINAL PLACED: 22 students
  Role: Systems Engineer (18) + Digital Specialist Engineer (4)
  CTC: ₹3.6L – ₹4.5L
  Joining: July 2027 (after final semester exams)
```

---

## 3. Student Placement Tracker

```
STUDENT PLACEMENT STATUS — Individual View
(Placement Officer view — all final year students)

Roll No.    | Student         | Status          | Company          | CTC     | Round
────────────────────────────────────────────────────────────────────────────────────────
226J1A0101  | Aditya K.       | ✅ Placed       | Amazon           | ₹18.5L  | —
226J1A0102  | Bhavana M.      | ✅ Placed       | TCS             | ₹3.36L  | —
226J1A0103  | Charan R.       | 🔄 In pipeline  | Goldman Sachs    | —       | Final round
226J1A0104  | Deepa S.        | ✅ Placed       | Infosys         | ₹3.6L   | —
226J1A0105  | Eshwar T.       | ❌ Not placed   | —               | —       | —
...
226J1A0332  | Zoya F.         | ✅ Placed       | Deloitte        | ₹7.0L   | —

SUMMARY:
  ✅ Placed: 224 (67.5%)
  🔄 In pipeline (active process): 38 (11.4%)
  ❌ Not placed (not appeared / not clearing): 70 (21.1%)
    - Not interested (higher studies): 28
    - Appeared but not cleared yet: 32
    - GATE/civil service aspirant: 10

STUDENTS WITH MULTIPLE OFFERS:
  Policy: Student can hold maximum 2 offers simultaneously while final round pending
          Once 3rd offer in hand, must release earlier 2 (to free up slots for others)
  EduForge alert: Triggers when student logs 3rd offer → "Release previous offers?"
  Ethics: Accepting an offer and not joining after company relied on headcount
          is not illegal, but repeated no-shows get college blacklisted by company

HIGHER STUDIES (not entering job market):
  GATE qualified (waiting for IIT/NIT admission): 18 students
  GRE/GMAT (US/Europe MS): 6 students
  UPSC/State PSC preparation: 4 students
  Entrepreneurship: 2 students
  Total higher studies declared: 30 students (9.0% of batch)
```

---

## 4. Placement Rules

```
PLACEMENT RULES — GCEH (agreed by students at registration)

RULE 1: One job rule (ethics-based, not mandatory)
  Students are strongly encouraged to withdraw from further drives once placed
  Reason: Fairness to unplaced students; maintaining company relationships
  Exception: Student may appear in dream company drive (CTC ≥2× current offer)
             Must intimate placement cell before appearing
  Enforcement: EduForge status update required; opt-out from subsequent drives auto-offered

RULE 2: Attendance at drives
  If registered and shortlisted: Attendance mandatory
  No-show without 24-hour notice to placement officer: 1 missed drive counted
  2 no-shows: Placement cell support temporarily suspended (student self-managed)
  Reason: No-shows disrupt drive scheduling; companies reduce intake when students absent

RULE 3: Offer acceptance
  Acceptance must be confirmed within 7 days of offer letter
  Non-response = automatic decline (company notified)
  Withdrawal after acceptance: Allowed before joining date, but company notified
                               and student flagged (may affect future batches)

RULE 4: Communication with companies
  All formal communication via placement cell email/coordinator
  Students must not contact company SPOC directly during process (unless told to)
  Reason: Coordinated approach maintains college credibility; uncoordinated student
          contacts can create confusion in company's recruitment pipeline
```

---

## 5. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/college/{id}/placement/drives/` | All drives (current season) |
| 2 | `POST` | `/api/v1/college/{id}/placement/drives/` | Schedule new drive |
| 3 | `GET` | `/api/v1/college/{id}/placement/drives/{id}/` | Drive detail |
| 4 | `POST` | `/api/v1/college/{id}/placement/drives/{id}/apply/` | Student applies for drive |
| 5 | `POST` | `/api/v1/college/{id}/placement/drives/{id}/results/` | Upload drive results |
| 6 | `GET` | `/api/v1/college/{id}/placement/students/status/` | All students placement status |

---

## 6. Business Rules

- CGPA eligibility cut-off for drives is set by the company, not by the college; the placement cell must apply the company's exact eligibility criteria; adding stricter internal filters without company consent (e.g., restricting to top 50% of eligible students without company knowledge) deprives eligible students of opportunity and is ethically and legally questionable
- Drive scheduling must account for exam timetable; scheduling a campus drive during mid-semester exams forces students to choose between academic assessment and placement — the placement cell must coordinate with the academic calendar; JNTU exam dates in particular are non-negotiable and drive dates must be adjusted around them
- No-show by shortlisted students directly damages the college's reputation with the company; if a company shortlists 40 students for interview and 15 are absent, the company reduces future intake from the college; enforcing the no-show penalty in EduForge is both fair to other students and protects the institution's placement track record
- PwD students must not be excluded from drive registration; if a company's physical test/process creates barriers for PwD students, the placement cell must request reasonable accommodation from the company (separate room, extra time, accessible venue); the RPwD Act 2016 prohibits discrimination in employment, and campus recruitment is an employment process
- DPDPA 2023 — company SPOCs receive student data as data processors; the college must have a data processing agreement (DPA) with each company before sharing student profiles; EduForge generates a standard DPA template that companies must acknowledge before receiving profile exports

---

*Last updated: 2026-03-27 · Group 4 — College Portal · Division E*
