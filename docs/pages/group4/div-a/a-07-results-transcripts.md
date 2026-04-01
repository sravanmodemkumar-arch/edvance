# A-07 — Results, Transcripts & SGPA/CGPA

> **URL:** `/college/students/results/`
> **File:** `a-07-results-transcripts.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Examination Controller (S4) · Registrar (S4) · Faculty (S3) — view results of own students · Student (S1) — own results only

---

## 1. Purpose

After the university publishes results, colleges download and display them to students. This module manages the complete results lifecycle — from marks entry/import through to SGPA/CGPA computation, grade sheets, transcripts, and the ABC (Academic Bank of Credits) upload.

---

## 2. Results Import — JNTU

```
RESULTS IMPORT — JNTU Portal
Semester II — June/July 2027 Results

JNTU result release: 15 July 2027
EduForge fetch: Automated (JNTU API / Excel upload fallback)
Status: ✅ Results imported (15 July 2027, 4:30 PM)
Students: 332  |  Results received: 332  |  Pending: 0 ✅

RESULT SUMMARY (College aggregate):
  Subjects with >90% pass rate: 6/9 ✅
  Subjects 75–90% pass rate: 2/9
  Subjects <75% pass rate: 1/9 (MA201 — Mathematics II: 71.4%) ⚠

  Overall pass % (all subjects, all students): 88.4%
  Students with all clears (no backlog): 278/332 (83.7%)
  Students with ≥1 backlog: 54/332 (16.3%)
```

---

## 3. Individual Results — SGPA Computation

```
RESULTS — Aakash Sharma (GCEH-2026-CSE-0041)
Semester II — May/June 2027

Course     Credits  Grade  Grade Points  Credits × Points
MA201        4       B+        7          28
CS201        4       A         8          32
CS203        3       A+        9          27
CS205        3       B+        7          21
EE201        3       B         6          18
HS201        2       A         8          16
CS207 Lab    1.5     O        10          15
CS209 Lab    1.5     A+        9         13.5
OE203        2       B+        7          14
────────────────────────────────────────────────────────
TOTAL       24      —          —          184.5

SGPA = Total Credits × Points ÷ Total Credits = 184.5 ÷ 24 = 7.69

GRADE SCALE (JNTU 2026 Regulation):
  O (Outstanding): 91–100 → 10 points
  A+ (Excellent):  81–90  → 9 points
  A  (Very Good):  71–80  → 8 points
  B+ (Good):       61–70  → 7 points
  B  (Above Avg):  51–60  → 6 points
  C  (Average):    41–50  → 5 points
  F  (Fail):       <40    → 0 points

CGPA (after Semester II):
  Semester I: SGPA 7.84  |  Credits: 22
  Semester II: SGPA 7.69 |  Credits: 24
  CGPA = (7.84×22 + 7.69×24) ÷ (22+24) = (172.48 + 184.56) ÷ 46 = 357.04 ÷ 46 = 7.76

  [Download Semester II Grade Sheet]  [View cumulative transcript]
```

---

## 4. Official Transcript

```
OFFICIAL TRANSCRIPT
GREENFIELDS COLLEGE OF ENGINEERING
Affiliated to: Jawaharlal Nehru Technological University Hyderabad
AICTE Approved | NAAC Accredited — Grade B+ (2024)

TRANSCRIPT

Name: AAKASH SHARMA
Roll No.: 226J1A0541
Programme: B.Tech Computer Science & Engineering (R26 Regulation)
Admission Year: 2026–27

SEMESTER I (Dec 2026 Exams):
  [Subject list, grades, credits — Sem I]
  SGPA: 7.84  |  Credits Earned: 22

SEMESTER II (May 2027 Exams):
  MA201 English Maths II: B+ (7) — 4 Cr
  CS201 Data Structures: A (8) — 4 Cr
  [...]
  SGPA: 7.69  |  Credits Earned: 24

CUMULATIVE CGPA (after Sem II): 7.76

This transcript is issued by the college for academic purposes.
For official university transcript (required for higher studies/immigration):
  Student must apply to JNTU directly; JNTU issues the official transcript
  with university seal (₹500/copy + courier, JNTU online portal).

[Download college transcript PDF]
[Apply for JNTU official transcript →] (External link to JNTU student portal)

College Registrar Signature + Seal
Certificate No.: GCEH/TRANS/2027/0041
Date of Issue: 20 July 2027
```

---

## 5. ABC Credit Upload

```
ACADEMIC BANK OF CREDITS — Semester II Update

Student: Aakash Sharma | ABC ID: ABC-2026-GCEH-0041
Credits earned in Semester II: 24
Total ABC credits: 22 (Sem I) + 24 (Sem II) = 46 credits

Upload status:
  Submitted to NAD (National Academic Depository): ✅ 20 July 2027
  Credits visible in ABC portal: ✅ (student can verify at abc.edu.in)

All 332 students' credits uploaded in batch ✅ (by 25 July 2027 — deadline)

NOTE: NAAC accreditation criterion 2.6 specifically evaluates ABC implementation.
  Colleges that upload credits late or inconsistently receive a lower score.
```

---

## 6. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `POST` | `/api/v1/college/{id}/results/import/` | Import results from university |
| 2 | `GET` | `/api/v1/college/{id}/results/summary/` | College-wide results analysis |
| 3 | `GET` | `/api/v1/college/{id}/students/{student_id}/results/` | Student results all semesters |
| 4 | `GET` | `/api/v1/college/{id}/students/{student_id}/transcript/pdf/` | Generate transcript PDF |
| 5 | `GET` | `/api/v1/college/{id}/students/{student_id}/sgpa-cgpa/` | SGPA/CGPA history |
| 6 | `POST` | `/api/v1/college/{id}/results/abc-upload/` | Batch upload credits to ABC/NAD |
| 7 | `GET` | `/api/v1/college/{id}/results/backlogs/` | All students with pending backlogs |

---

## 7. Business Rules

- SGPA/CGPA computation must follow the affiliating university's prescribed formula; JNTU uses the credit-weighted average of grade points; different universities use different scales (some use 10-point, some 4-point); the system is parameterised by university formula, not hardcoded — this is critical for multi-university colleges
- The college transcript is NOT the official university transcript; for immigration, higher studies abroad, or competitive applications, students need the official university-issued transcript; the college transcript is for reference and local purposes; EduForge clearly labels this distinction on the document
- ABC upload deadline (typically 30 days after result declaration) is a compliance obligation under NEP 2020; colleges that miss this deadline are penalised in NAAC criteria; EduForge auto-triggers a reminder 7 days before deadline and generates the batch upload file
- Backlog management: A student's CGPA is calculated only on subjects where they have a passing grade; a failed subject is shown as F (0 grade points) in the semester it was failed, but once re-attempted and passed, the passing grade is used in CGPA going forward (JNTU uses "latest attempt" for CGPA, not average of all attempts — varies by university)

---

*Last updated: 2026-03-27 · Group 4 — College Portal · Division A*
