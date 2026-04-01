# B-09 — NPTEL/SWAYAM Course Management

> **URL:** `/college/academic/online/`
> **File:** `b-09-online-courses.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Roles:** NPTEL Coordinator (S3) · Academic Coordinator (S4) · Faculty (S3) — track own students · Student (S1) — register and track

---

## 1. Purpose

NPTEL (National Programme on Technology Enhanced Learning) and SWAYAM (MOOCs platform) courses allow students to earn credits through online national courses delivered by IIT/NIT faculty. Under NEP 2020 and AICTE guidelines:
- Students can earn up to 40% of their credits through online courses (SWAYAM)
- NPTEL certification is valid for credit transfer at the home institution (if approved by academic council)
- NAAC looks for evidence of NPTEL participation (criterion 2.3)
- Faculty can also do NPTEL FDP (Faculty Development Programme) courses

---

## 2. Student NPTEL Registration

```
NPTEL COURSE REGISTRATION — Semester II 2026–27
NPTEL Coordinator: Mr. Arjun V. (CSE department)

APPROVED NPTEL COURSES (Academic Council approved — mapped to curriculum):
  NPTEL Course              Credits  Maps to               Condition
  Programming in Python     4 cr     CS elective OEC-205   Score ≥60%, NPTEL cert
  Data Science Basics       4 cr     CS elective OEC-207   Score ≥60%, NPTEL cert
  Machine Learning          4 cr     CS elective OEC-209   Score ≥60% + III yr only
  Digital Marketing         2 cr     Management elective   Score ≥60%, NPTEL cert
  Constitution of India     2 cr     Mandatory MC          NPTEL replaces internal

STUDENT REGISTRATIONS (this semester):
  Student ID         Course                       Status      Score
  226J1A0502         Programming in Python        Registered  In progress (Week 8/12)
  226J1A0518         Data Science Basics          Registered  In progress
  226J1A0541 Aakash  (Not registered this sem)    —           —
  [24 total students registered in at least 1 NPTEL course]

AAKASH'S NOTE: Not registered for NPTEL this semester — OEC203 already taken
  in-class. Eligible from Semester III for ML course.

COMPLETION STATUS (previous semester):
  Registered: 28 students  |  Completed with ≥60%: 18 (64.3%)
  Credits granted (uploaded to ABC): 18 × 4 credits = 72 credits
```

---

## 3. Faculty NPTEL FDP Tracking

```
FACULTY NPTEL FDP (Faculty Development Programme)

AICTE requirement: Faculty must complete FDP; NPTEL courses count toward FDP
NAAC criterion 3.4: Faculty development activities

Faculty FDP Status (this year):
  Faculty         NPTEL Course               Status     Credits
  Dr. Anita K.    Deep Learning (IIT-M)     ✅ Completed  8 credits
  Mr. Suresh V.   VLSI Design (IIT-B)       ✅ Completed  4 credits
  Dr. Ramesh M.   Cloud Computing (IIT-KGP) ⏳ Week 6/8   In progress
  Mr. Pradeep T.  (No FDP this year) ← ⚠ Flagged for appraisal
  [Full list 18 faculty]

NOTE: NAAC assessors look for faculty development hours; NPTEL certificates
  are valid NAAC evidence; faculty who don't do any FDP are a NAAC gap.
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/college/{id}/nptel/approved-courses/` | Approved NPTEL courses list |
| 2 | `POST` | `/api/v1/college/{id}/nptel/register/` | Register student for NPTEL course |
| 3 | `GET` | `/api/v1/college/{id}/nptel/status/` | Registration + completion status |
| 4 | `POST` | `/api/v1/college/{id}/nptel/credit-grant/` | Grant credits on completion (HOD + Registrar) |
| 5 | `GET` | `/api/v1/college/{id}/nptel/faculty-fdp/` | Faculty FDP tracking |

---

## 5. Business Rules

- NPTEL credit recognition requires academic council approval for each course (mapping to curriculum); a student who completes an unapproved NPTEL course gets a certificate but no curriculum credit; the mapping list must be published at the beginning of the academic year so students can plan
- NPTEL certificate (with proctored examination score) is the evidence for credit transfer; non-proctored NPTEL completion (self-paced, no exam) is not credit-eligible; the coordinator must verify the certificate type before granting credits
- SWAYAM courses are broadly similar to NPTEL; the same credit recognition policy applies; SWAYAM has a wider range of subjects beyond engineering (useful for open electives, value-added courses, management subjects)

---

*Last updated: 2026-03-27 · Group 4 — College Portal · Division B*
