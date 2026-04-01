# A-02 — Admission Process & Seat Allotment

> **URL:** `/college/students/admission/`
> **File:** `a-02-admission-process.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Admissions Officer (S3) · Registrar (S4) · Principal/Director (S6) — management quota approval

---

## 1. Purpose

After applications are received and verified, the admission process allocates seats through merit lists and counselling. In Indian engineering/professional colleges, this operates in two parallel tracks:
1. **Convener quota (70%):** State government's centralised counselling (TGCHE for TS engineering; NEET-UG/PG counselling for medical; state counselling for degree colleges)
2. **Management quota (30%):** College-initiated process within AICTE/UGC fee and seat norms

---

## 2. Convener Quota Process (State Counselling Integration)

```
CONVENER QUOTA — TGCHE EAPCET 2026 (Telangana)
B.Tech Admissions — Greenfields College of Engineering

TGCHE (Telangana State Council of Higher Education) conducts EAPCET
(Engineering, Agriculture & Pharmacy Common Entrance Test).

COLLEGE-SIDE TASKS:
  Phase 1 — Seat Matrix upload to TGCHE portal (by 1 July 2026):
    Programme  Category  Seats
    CSE        UR        30
    CSE        OBC       33
    CSE        SC        18
    CSE        ST         7
    CSE        EWS       12
    CSE        PwD (H)    5 (horizontal across categories)
    ... [full matrix for all programmes]
    [Upload to TGCHE] ✅

  Phase 2 — Receiving allotted students (TGCHE releases allotment):
    Round 1 allotment: 15 July 2026
    Reporting deadline: 20 July 2026 (student must report to college)
    Students allotted (Round 1): 218 students across all programmes

  Phase 3 — Reporting and verification:
    Student reports with originals → Admissions Office verifies documents
    If documents pass → Admit student → Generate College ID → Fee collection
    If documents fail → Cancel and report vacancy to TGCHE

    Admitted (Round 1): 198 / 218 allotted (20 did not report — vacancy)
    Vacancies reported to TGCHE for Round 2: 20 seats

  Phase 4 — Mop-up rounds (TGCHE):
    Round 2 allotment: 1 August 2026 → 12 more seats filled
    Spot admissions (if any remaining): August 15–20
    Final convener intake: 247/252 convener seats filled

COLLEGE CANNOT:
  ✗ Accept a convener-quota student who was NOT allotted by TGCHE
  ✗ Charge above AICTE-approved tuition fee for convener seats
  ✗ Refuse a validly allotted student without legal grounds
```

---

## 3. Management Quota Process

```
MANAGEMENT QUOTA — B.Tech 2026–27
Greenfields College of Engineering

Management quota seats: 108 (30% of 360)
  CSE: 36  |  ECE: 18  |  ME: 18  |  Civil: 18  |  EEE: 18

ELIGIBILITY: Same as convener (PCM 45% + valid JEE/EAPCET score)
FEE: AICTE/TS AFRC (Admissions and Fee Regulatory Committee) approved
  Management quota fee cap (TS): ₹1,40,000/year for CSE (2026–27 AFRC approval)
  Cannot exceed AFRC cap under any circumstance

MANAGEMENT QUOTA PROCESS:
  Step 1: Merit list from verified applications (non-TGCHE applicants or TGCHE
           applicants who prefer management quota's admission timing)

  Step 2: Counselling session (college-level):
    Date: 5 July 2026
    Students called: Top 3× seats (108 × 3 = 324 called)
    Documents verified in original during counselling

  Step 3: Seat allotment (merit within management quota, category-wise)
  Step 4: Fee payment (AFRC-approved amount) within 3 days
  Step 5: Student enrolled

MANAGEMENT QUOTA FILL STATUS (2026–27):
  CSE: 36/36 ✅  |  ECE: 17/18  |  ME: 15/18  |  Civil: 12/18  |  EEE: 14/18
  Total filled: 94/108 (87% fill rate)

UNFILLED SEATS:
  14 management seats unfilled → reported to AICTE as per norms
  Mop-up: College can admit in remaining 14 seats through spot process (AFRC guidelines)

TRANSPARENCY REQUIREMENT:
  TS AFRC mandates display of merit list and fee structure on college notice board and website
  EduForge posts these automatically on the college's public portal
```

---

## 4. Reservation Matrix Enforcement

```
RESERVATION COMPLIANCE — B.Tech 2026–27 (FINAL INTAKE)

After all rounds (convener + management):

Category      Seats  Admitted  Fill%   Compliance
UR (Open)       90       88    97.8%   ✅
OBC-NCL         97       93    95.9%   ✅
SC              54       50    92.6%   ✅
ST              23       21    91.3%   ✅
EWS             36       32    88.9%   ⚠ (below 100% — 4 seats unfilled)
PwD (Horiz.)    18       14    77.8%   ⚠ PwD seats unfilled (common challenge)
Management     108       94    87.0%   ✅ (AFRC norms allow some vacancy)
NRI             12        8    66.7%   ✅ (low NRI interest — normal)
─────────────────────────────────────────────────────────────────────────────
TOTAL          360      332    92.2%   ✅

NOTE: Unfilled SC/ST/EWS/PwD convener seats are NOT to be filled with
  general category students; they are carried forward as vacancies and
  reported to AICTE/TGCHE as unfilled reserved seats.
  (Conversion of reserved seats to general is not permitted under law)

[Generate admission report for AICTE/TGCHE submission]
```

---

## 5. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/college/{id}/admissions/seat-matrix/` | Seat matrix by programme and category |
| 2 | `POST` | `/api/v1/college/{id}/admissions/enrol/` | Enrol admitted student |
| 3 | `GET` | `/api/v1/college/{id}/admissions/fill-status/` | Real-time seat fill status |
| 4 | `POST` | `/api/v1/college/{id}/admissions/convener/upload/` | Upload TGCHE allotment list |
| 5 | `GET` | `/api/v1/college/{id}/admissions/reservation-compliance/` | Reservation category fill analysis |
| 6 | `GET` | `/api/v1/college/{id}/admissions/unfilled/` | Unfilled seats (for spot process) |

---

## 6. Business Rules

- Conversion of unfilled reserved category seats (SC/ST/OBC/EWS/PwD) to general category is prohibited under central and state reservation laws; a college that "converts" unfilled reserved seats (even with AICTE's knowledge) is violating constitutional provisions; EduForge prevents this at the system level — reserved seats cannot be re-labelled
- AFRC (Admissions and Fee Regulatory Committee) fee cap is a hard ceiling — the college cannot charge management quota students more than the AFRC-approved fee; capitation fee (one-time illegal payment above approved fee) is a criminal offence; EduForge fee module (C-series) enforces the AFRC fee cap
- Every admission — convener or management — must have a unique college enrollment number; the enrollment number format is prescribed by the affiliating university (JNTU format for engineering); EduForge generates this in the correct university-specified format
- Spot admission (after regular rounds) must follow the same merit-cum-reservation principles; it is not a free-for-all for management to fill seats with non-merit candidates; AICTE conducts inspections post-admission to verify spot admission records

---

*Last updated: 2026-03-27 · Group 4 — College Portal · Division A*
