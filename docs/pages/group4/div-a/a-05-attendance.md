# A-05 — Attendance (UGC 75% Rule)

> **URL:** `/college/students/attendance/`
> **File:** `a-05-attendance.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Faculty (S3) — mark attendance for own courses · HOD (S4) — department view · Registrar (S4) — full view and detention processing · Student (S1) — own attendance only

---

## 1. Purpose

Attendance management in colleges differs from school in critical ways:
- **Subject-wise attendance:** Each course is tracked independently (a student may have 80% overall but <75% in one subject — that subject is the problem)
- **UGC 75% rule:** Minimum 75% attendance in each subject is mandatory to appear for university exams (JNTU/affiliating university norms); students below 75% are "detained" and cannot appear for exams
- **Condonation:** Students between 65–75% with medical/genuine reasons may apply for condonation (university approval); <65% cannot appear regardless of reason
- **Lectures vs Labs:** Separate tracking for theory periods and lab sessions

---

## 2. Faculty — Mark Attendance

```
MARK ATTENDANCE — Dr. Anita K.
Course: CS201 — Data Structures & Algorithms
Date: 27 March 2026 (Friday)  |  Hour: 9:00–10:00 AM (Period 2)
Class: CSE-A + CSE-B (merged for this lecture — lecture hall)
Total students: 78

ATTENDANCE ENTRY:
  [Auto-populated from timetable and enrolled students]

  226J1A0501  Abhinav R.     ✅ Present
  226J1A0502  Aisha M.       ✅ Present
  226J1A0503  Arjun T.       🔴 Absent
  226J1A0504  Deepika N.     ✅ Present
  ...
  226J1A0541  Aakash Sharma  ✅ Present
  ...
  [78 entries — biometric/manual]

Summary: 71 present / 78 enrolled (91.0%)

[Submit Attendance]  [Save as draft]

PREVIOUS CLASS ATTENDANCE (last 5 sessions):
  24 Mar: 73/78 (93.6%)
  21 Mar: 68/78 (87.2%)  — low ⚠
  19 Mar: 75/78 (96.2%)
  17 Mar: 72/78 (92.3%)
  14 Mar: 76/78 (97.4%)
```

---

## 3. Student Attendance View — Subject-Wise

```
ATTENDANCE — Aakash Sharma (GCEH-2026-CSE-0041)
Semester II — As of 27 March 2026

Course       Faculty          Classes  Present  %      Status
MA201        Dr. R. Patel     42       38       90.5%  ✅
CS201        Dr. Anita K.     48       43       89.6%  ✅
CS203        Mr. Suresh V.    36       31       86.1%  ✅
CS205        Dr. Ramesh M.    40       36       90.0%  ✅
EE201        Mr. Pradeep T.   38       32       84.2%  ✅
HS201        Ms. Neeraja R.   28       21       75.0%  ⚠ AT THRESHOLD
CS207 Lab    Dr. Anita K.     14       12       85.7%  ✅
CS209 Lab    Mr. Suresh V.    14       11       78.6%  ✅
OE203        External         18       16       88.9%  ✅
──────────────────────────────────────────────────────────
OVERALL      (weighted)       278     240       86.3%  ✅

⚠ WARNING: HS201 (English) at exactly 75.0% — ONE MORE ABSENCE = DETAINED
  [Student has been sent a warning notification]

DETENTION RISK:
  HS201: 21/28 classes attended. Remaining classes: ~12
  If misses 1 more: 21/29 = 72.4% → Below threshold → DETAINED in HS201
  Action required: Attend all remaining HS201 classes

UGC MINIMUM: 75% in each subject
University (JNTU): 75% minimum; condonation 65–75% (medical with approval)
```

---

## 4. Detention Processing

```
DETENTION REGISTER — Semester II 2026–27 (End of semester)

DETAINED STUDENTS (below 75% in at least one subject):

Student ID        Name          Subject   Att%   Action
226J1A0503        Arjun T.      CS201      68.2%  Detained — cannot appear
226J1A0503        Arjun T.      CS203      71.4%  Condonation eligible (>65%)
226J1A0517        Priya M.      HS201      64.2%  Detained — <65% in HS201
226J1A0528        Kiran V.      MA201      74.8%  Condonation eligible (border)

CONDONATION PROCESS (for 65–75% students):
  Student submits: Medical certificate / genuine reason
  HOD recommends: Yes/No
  Principal forwards to university (JNTU) with consolidated list
  JNTU grants/rejects: Condonation is JNTU's decision, not college's

  JNTU condonation fee: ₹500/subject (collected by college, remitted to JNTU)

DETAINED STUDENT CONSEQUENCES:
  Cannot appear in university semester exam for detained subject(s)
  Must attend next semester's classes for the detained subject (if recurring)
  OR appear in supplementary exam after completing 75% in next offer

[Generate detention list for JNTU]  [Process condonation applications]
[Send detention notifications to students + parents]
```

---

## 5. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `POST` | `/api/v1/college/{id}/attendance/mark/` | Mark attendance for a session |
| 2 | `GET` | `/api/v1/college/{id}/attendance/student/{student_id}/semester/{sem}/` | Student subject-wise attendance |
| 3 | `GET` | `/api/v1/college/{id}/attendance/below-threshold/?threshold=75` | Students below attendance threshold |
| 4 | `GET` | `/api/v1/college/{id}/attendance/detained/` | Detained student register |
| 5 | `POST` | `/api/v1/college/{id}/attendance/condonation/` | Submit condonation application to university |
| 6 | `GET` | `/api/v1/college/{id}/attendance/course/{course_id}/` | Course-level attendance report |

---

## 6. Business Rules

- UGC and affiliating universities (JNTU, Osmania, etc.) mandate 75% attendance per subject; the college must detain students below this threshold; allowing detained students to appear for exams is a violation of university affiliation norms and can result in results being cancelled
- Subject-wise attendance is maintained separately from overall attendance; a student with 85% overall but 68% in one subject is detained in that subject — the overall percentage does not save them; EduForge calculates and displays subject-wise status prominently
- Faculty must mark attendance within 24 hours of the class (next working day at the latest); the system locks attendance entry after 48 hours (to prevent backdating); if faculty miss marking, they must submit a manual correction request to the HOD
- Attendance alert thresholds: 85% (early warning — green banner), 80% (yellow banner, CT notification), 75% (red banner — student + parent notification), below 75% (critical — detained flag); alerts at 80% give the student time to self-correct before detention
- Condonation is a university prerogative, not a college one; the college can recommend condonation but cannot grant it; a college that allows students to sit exams without university condonation approval risks having those results invalidated by the university

---

*Last updated: 2026-03-27 · Group 4 — College Portal · Division A*
