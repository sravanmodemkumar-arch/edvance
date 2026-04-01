# A-10 — Graduation & Convocation

> **URL:** `/college/students/graduation/`
> **File:** `a-10-graduation.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Examination Controller (S4) · Registrar (S4) · Principal/Director (S6) · Student (S1) — view own graduation status

---

## 1. Purpose

Manages the final steps of a student's academic journey — confirming graduation eligibility, applying for the university degree, convocation registration, and degree certificate issuance.

---

## 2. Graduation Eligibility Check

```
GRADUATION ELIGIBILITY — Batch 2026–30 (Final Year — B.Tech)
Programme: B.Tech CSE | University: JNTU Hyderabad

ELIGIBILITY CRITERIA (JNTU R26 Regulation):
  ✅ All 8 semesters completed
  ✅ All subjects passed (no pending backlog)
  ✅ Total credits: ≥160 (for Honours with Research) OR ≥120 (standard B.Tech)
  ✅ Minimum CGPA: 5.0 (to be awarded B.Tech degree)
  ✅ No disciplinary disqualification
  ✅ All dues to college and university cleared
  ✅ Project/Thesis submitted and evaluated (Semester VIII)

GRADUATION ELIGIBILITY REGISTER (May 2030):
  Eligible for degree (all requirements met): 298 / 332 students ✅
  Backlog pending (not eligible yet):          28 students ⚠ (must clear backlogs)
  CGPA below 5.0 (minimum):                    4 students ⚠ (not eligible)
  Eligible with Honours (CGPA ≥8.0):          42 students

[Generate eligibility list for JNTU]
```

---

## 3. Degree Application to University

```
DEGREE APPLICATION — JNTU Process

For students who are eligible:
  Step 1: College submits degree application batch to JNTU
    File: Excel — Roll No., Name, CGPA, Programme, Distinction/First/Second Class
    Application fee: ₹1,500/student (JNTU — collected by college, remitted)
    Submission deadline: 15 June 2030

  Step 2: JNTU verifies and approves
    JNTU cross-checks: Exam records, marks, attendance, fee clearance
    Approval: July 2030

  Step 3: Degree certificate printing (JNTU central printing)
    JNTU prints degree certificates with university seal and VC signature
    Distribution: At convocation or by post (student's choice)

DEGREE CLASS:
  CGPA 7.5 and above: First Class with Distinction
  CGPA 6.0–7.49: First Class
  CGPA 5.0–5.99: Second Class
  CGPA <5.0: Not eligible for degree (must improve)

AAKASH SHARMA (projected):
  Expected CGPA (after all 8 semesters): ~8.2 (projecting from current 7.76)
  Expected class: First Class with Distinction ✅ (if CGPA ≥7.5)
```

---

## 4. Convocation Registration

```
CONVOCATION — JNTU Annual Convocation (Oct/Nov 2030)

Greenfields College — Convocation 2030:
  Total eligible graduates: 298 students + previous year backlogs (22)
  Registering for convocation: 265 students
  Not attending (opting for degree by post): 33 students

CONVOCATION REGISTRATION:
  Student registers: [Yes / No — attend or receive by post]
  Convocation fee: ₹1,200 (gown + certificate handling + lunch)
  Guest tickets: 2 per student (parent/family)
  Venue: JNTU Hyderabad Main Campus (or college campus for affiliated convocation)

AAKASH SHARMA — CONVOCATION:
  Registered: ✅
  Fee paid: ₹1,200 ✅
  Guest tickets: 2 (parents attending) ✅

[Download convocation admit card]
[Download degree certificate (after JNTU releases)] ← Available post-convocation
```

---

## 5. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/college/{id}/graduation/eligibility/` | Graduation eligibility register |
| 2 | `POST` | `/api/v1/college/{id}/graduation/apply/` | Submit degree application to university |
| 3 | `POST` | `/api/v1/college/{id}/graduation/convocation/register/` | Student convocation registration |
| 4 | `GET` | `/api/v1/college/{id}/students/{student_id}/degree/certificate/` | Download degree certificate |
| 5 | `GET` | `/api/v1/college/{id}/graduation/summary/` | Batch graduation summary |

---

## 6. Business Rules

- Degree application to the university is the college's responsibility (not the student's individual responsibility); the college submits a batch application for all eligible students; a student who is accidentally omitted from the batch may have their degree delayed by a full year (JNTU processes degrees once a year)
- Students with pending backlogs at the time of batch graduation will receive their degree only after clearing all backlogs; they are not eligible for the current year's convocation; EduForge tracks these "trailing backlog" students separately and notifies them when they become eligible
- Degree certificates from JNTU are physical documents with the Vice Chancellor's signature; JNTU has introduced digital degrees (Digilocker) for some recent batches; EduForge integrates with Digilocker to allow students to download their JNTU degree from the portal when available
- The CGPA used for the degree class (Distinction/First/Second) is the final CGPA including all semester results; if a student's backlog pass in a supplementary exam improves their CGPA across the class boundary (e.g., from 7.48 to 7.52), they are entitled to First Class with Distinction; this re-classification must be applied correctly

---

*Last updated: 2026-03-27 · Group 4 — College Portal · Division A*
