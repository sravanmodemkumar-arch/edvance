# B-03 — CIE — Continuous Internal Evaluation

> **URL:** `/college/academic/cie/`
> **File:** `b-03-cie-internals.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Faculty (S3) — enter marks for own courses · HOD (S4) · Examination Controller (S4) · Dean Academics (S5) · Student (S1) — view own CIE marks

---

## 1. Purpose

CIE (Continuous Internal Evaluation) — also called "sessional marks", "mid-term marks", or "internal marks" — is the college-administered component of student assessment. Under JNTU (and most Indian universities), the total marks split is:
- Internal (CIE): 30 marks (or 40 in some universities)
- External (University exam): 70 marks (or 60)
- Total: 100 marks per subject

CIE marks are set by the college and submitted to the university before the semester exam. The university does not control CIE — the college has full responsibility.

---

## 2. CIE Structure (JNTU R26)

```
CIE STRUCTURE — JNTU R26 Regulation
Per theory subject (out of 30 internal marks):

Component         Marks   Conducted by
Mid-I Exam         15     College (after Unit I + II)
Mid-II Exam        15     College (after Unit III + IV)
───────────────────────────────────────────────────────
CIE Total          30

NOTE: JNTU R26 uses "better of two mids" for theory: each mid is out of 30;
  the better score × 0.5 = 15 marks contribution.
  (Some regulations use average; R26 uses "better of" — system parameterised)

Per lab subject (out of 30 internal marks):
Component         Marks   Conducted by
Day-to-day record  10     Faculty (throughout semester)
Internal lab exam  20     College (lab viva + exam)
───────────────────────────────────────────────────────
Lab CIE Total      30

CIE SUBMISSION TO JNTU:
  Deadline: 15 days before university exam
  Format: JNTU portal upload (Excel) or direct API (if available)
```

---

## 3. Mid-I Marks Entry — Faculty View

```
MARKS ENTRY — CS201: Data Structures & Algorithms
Faculty: Dr. Anita K.
Exam: Mid-I (15 February 2027)
Maximum Marks: 30  |  Duration: 2 hours
Class: CSE-A (38 students) + CSE-B (40 students)

  Roll No.         Name                 Marks /30   Absent?
  226J1A0501       Abhinav R.           22          No
  226J1A0502       Aisha M.             27          No
  226J1A0503       Arjun T.             --          Absent (unexcused)
  226J1A0504       Deepika N.           25          No
  ...
  226J1A0541       Aakash Sharma        24          No
  ...
  [78 entries]

MARKS ENTRY RULES:
  ✅ Only marks 0–30 accepted
  ✅ Absent students marked with code AB (get 0 for "better of" calculation)
  ✅ Faculty cannot enter marks for a student not enrolled in their section
  ✅ Once submitted (by faculty), marks go for HOD review
  ✅ HOD can return for correction but cannot edit directly (audit trail)

[Save as draft]  [Submit for HOD review]

SUMMARY STATISTICS (after entry):
  Class average: 21.4 / 30 (71.3%)
  Highest: 29 / 30  |  Lowest: 8 / 30
  Below passing (16/30 = 53%): 12 students ← flag for remedial
```

---

## 4. CIE Computation — Student View

```
CIE MARKS — Aakash Sharma (226J1A0541)
Semester II 2026–27

Course  Mid-I  Mid-II  Better/30  Lab-CIE  Total CIE
CS201     24     26      13+13=26     N/A      26/30  ✅
CS203     28     25      14+14=28     N/A      28/30  ✅
CS205     20     23      11.5+11.5=23 N/A      23/30
EE201     18     22      11+11=22     N/A      22/30
HS201     26     —       (mid-I: 26×0.5=13; mid-II pending)
CS207     N/A    N/A     N/A         28/30    28/30  ✅ (lab)
CS209     N/A    N/A     N/A         24/30    24/30  ✅ (lab)
MA201     22     28      14+14=28     N/A      28/30  ✅

NOTE: "Better of mid-I and mid-II" for JNTU R26:
  Each mid is out of 30; better of the two = full 30-mark weight
  CIE = better mid × 1.0 (simple — both mids are used to find the better)
  Wait: re-check R26 rule: 30 marks = each mid out of 30; best = CIE
  So if Mid-I = 24 and Mid-II = 26: CIE = 26 (better of the two)

  [JNTU R26 exact rule: CIE = best of (Mid-I, Mid-II) for theory]
  CS201: max(24, 26) = 26 ✅

  Updated computation:
  Course  Mid-I  Mid-II  CIE (Best)  Lab CIE  CIE Total
  CS201     24     26      26/30        N/A       26/30
  MA201     22     28      28/30        N/A       28/30
```

---

## 5. CIE Submission to University

```
CIE SUBMISSION — JNTU Hyderabad
Semester II 2026–27 | Due: 30 April 2027

STATUS:
  Faculty marks entry: ✅ Complete (all 9 courses)
  HOD review: ✅ Complete
  Examination Controller audit: ✅ Complete (no anomalies)
  Submission to JNTU portal: ⬜ Pending (due date: 30 April 2027)

PRE-SUBMISSION CHECK:
  Marks range check (all marks 0–30): ✅ No out-of-range
  Absent students coded correctly: ✅
  Malpractice cases (if any): 0 cases this semester ✅
  CIE marks freeze (no changes after submission): Pending

  [Generate JNTU upload file (Excel format)]
  [Submit to JNTU portal]
  [Download submission acknowledgement]

NOTE: Once submitted to JNTU, CIE marks are final.
  Correction requires a JNTU-approved process (Principal's letter + supporting docs).
  Routine "oh we made a mistake" corrections are not accepted.
```

---

## 6. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `POST` | `/api/v1/college/{id}/cie/marks/` | Enter CIE marks for a section |
| 2 | `PATCH` | `/api/v1/college/{id}/cie/marks/{id}/hod-review/` | HOD review and approve |
| 3 | `GET` | `/api/v1/college/{id}/students/{student_id}/cie/semester/{sem}/` | Student's CIE marks |
| 4 | `GET` | `/api/v1/college/{id}/cie/analytics/?course={code}` | Course CIE analytics |
| 5 | `POST` | `/api/v1/college/{id}/cie/submit-to-university/` | Generate and submit to JNTU |
| 6 | `GET` | `/api/v1/college/{id}/cie/status/` | Submission status across all courses |

---

## 7. Business Rules

- CIE marks are the college's responsibility and liability; if marks are found to be inflated (all students getting near-maximum CIE marks while failing university exams), universities investigate; a college that consistently shows this pattern is suspected of CIE inflation and faces audit; EduForge's analytics (CIE vs university exam correlation) flags this pattern proactively
- Faculty cannot enter marks for students they don't teach; the system restricts mark entry to enrolled students in the faculty's assigned sections; this prevents phantom marks or unauthorized modifications
- Once the HOD approves marks, the faculty can request corrections but cannot directly edit; corrections go back through the HOD approval cycle; once the Examination Controller freezes marks for JNTU submission, no changes are possible except through the formal JNTU correction process (rare, documented, slow)
- Absent students in Mid exams: JNTU R26 allows colleges to conduct a re-test for genuinely absent students (medical emergency, etc.); this is the college's discretion; a re-test must be conducted within 7 days of the original exam; re-test marks replace the original 0; this must be documented (medical proof)

---

*Last updated: 2026-03-27 · Group 4 — College Portal · Division B*
