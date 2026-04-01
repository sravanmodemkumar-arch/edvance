# E-11 — Exam Attendance Eligibility

> **URL:** `/school/attendance/exam-eligibility/`
> **File:** `e-11-exam-eligibility.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Academic Coordinator (S4) — full (condonation workflow) · Exam Cell Head (S4) — full · Principal (S6) — final approval (condonation sign-off) · Class Teacher (S3) — view own class

---

## 1. Purpose

Determines which students are eligible to appear for school exams based on their attendance percentage. This is P0 because:
- **CBSE rule:** 75% attendance in each subject required for annual exam. 65–75% = eligible for condonation (Principal recommendation to CBSE). Below 65% = not eligible regardless.
- **School internal exams (PT, Half-yearly):** School may set its own minimum (typically 75–85%); students below minimum are listed for teacher/coordinator action
- **Board exam LOC (B-33):** CBSE requires the school to certify that each student in the LOC has ≥ 75% attendance; ineligible students cannot be in the LOC

The condonation process (for 65–75% students) involves: Principal's written recommendation to CBSE → CBSE reviews → condonation granted or denied → student may or may not appear.

---

## 2. Page Layout

### 2.1 Header
```
Exam Attendance Eligibility                  [Generate Eligibility Report]  [Start Condonation]  [Export]
Exam: [Annual Exam 2026–27 ▼]
Cutoff Date: 31 March 2026 (attendance computed up to this date)

Overall Status:
  ✅ Eligible (≥ 75%):         369 students
  🟡 Condonation zone (65–74%): 8 students
  ❌ Not eligible (< 65%):      3 students
```

### 2.2 Eligibility Table

```
Filter: [Show all ▼ / Condonation zone / Not eligible]  Class: [All ▼]

── ❌ NOT ELIGIBLE (< 65%) ─────────────────────────────────────────────────

Roll  Name          Class  Attendance %   Max Possible  Condonation  Action
08    Vijay S.       X-B     59.6%        74.0%          N/A (< 65%)  [Block from Exam]
15    Meena D.      XII-A    58.1%        73.1%          N/A (< 65%)  [Block from Exam]
22    Arun M.        IX-A    60.0%        74.5%          N/A (< 65%)  [Block from Exam]

── 🟡 CONDONATION ZONE (65–74%) ────────────────────────────────────────────

11    Suresh K.      IX-A    71.7%   [Prepare Condonation Application]  [Block from Exam]
04    Chandana Rao   XI-A    67.2%   [Prepare Condonation Application]  [Block from Exam]
...

── ✅ ELIGIBLE (≥ 75%) — All others ────────────────────────────────────────

01    Anjali Das     XI-A    94.4%   ✅ Eligible
02    Arjun Sharma   XI-A    87.8%   ✅ Eligible
...
```

---

## 3. Condonation Application (CBSE)

For students in 65–74% zone, the school must send a condonation request to CBSE:

[Prepare Condonation Application] → per student:

```
CONDONATION APPLICATION — CBSE

School: [School Name]  ·  Affiliation: AP2000123
Academic Year: 2026–27  ·  Exam: Class X Annual / Board 2027

Student: Suresh Kumar Naidu
DOB: 15 March 2011
Class X Roll No.: 12342580
Attendance: 71.7% (142/198 working days)

Reason for shortage (Principal statement):
  ________________________________
  ________________________________

Supporting circumstances:
  ● Medical illness (with doctor certificate) — 18 days
  ○ Participation in national-level competition
  ○ Natural calamity
  ○ Other extraordinary circumstances

Supporting documents attached: [Medical certificates — 3 PDFs]

Recommendation:
  I, [Principal Name], Principal of [School Name], do hereby certify that the
  attendance shortage is genuine and recommend condonation for the above student
  to appear in the annual/board examination.

  Signature of Principal: _______________  Date: ______________
  School Seal: [SEAL]

[Generate PDF Condonation Application]  [Send to Academic Coordinator for Review]
```

---

## 4. Subject-wise Eligibility

CBSE requirement is per subject, not just overall:

```
Subject-wise Eligibility — Arjun Sharma (XI-A)

Subject      Periods  Present  %      Eligible  Status
Physics        86       72    83.7%   ✅ Yes
Chemistry      84       70    83.3%   ✅ Yes
Mathematics    88       78    88.6%   ✅ Yes
English Core   80       74    92.5%   ✅ Yes
Phy. Edu.      42       40    95.2%   ✅ Yes

Overall: All subjects eligible ✅
```

For a student with overall 76% but Physics only 68%:
```
⚠️ Priya Venkat — XI-A
Overall attendance: 78% ✅
Physics attendance: 68% ❌ — Below 75% in Physics specifically
→ Student eligible for all exams EXCEPT Physics exam
→ Condonation required for Physics only
```

---

## 5. Exam Block Enforcement

When [Block from Exam] is triggered:
```
Block from Exam — Vijay S. (X-B)

Blocked From:
  ☑ Half-yearly examination
  ☑ Annual examination
  ☑ Board examination (CBSE X — 2026)

Effect:
  Student will not appear in CBSE LOC submission (B-33)
  Hall ticket will NOT be generated (B-12)
  Marks entry (B-16) will be locked for this student

Notification:
  Parent will receive: "This is to inform you that [Name], Class X, has been
  debarred from the annual/board examination due to insufficient attendance
  (59.6%). Please meet the Principal immediately."

Principal Approval Required: ✅ (block is a serious action)
[Generate Debar Notice]  [Confirm Block — Principal]
```

---

## 6. Eligibility Report (for B-33 LOC)

[Generate Eligibility Report] → used when preparing CBSE board exam LOC:

```
ATTENDANCE ELIGIBILITY CERTIFICATION
[School Name] | Affiliation: AP2000123

For CBSE Board Examination — March 2027 (Class X)

This is to certify that the following students have the required attendance
(≥ 75%) and are eligible to appear in the CBSE Board Examination:

[List of 34 students with attendance %]

Students with condonation:
[List of 2 students with condonation applications enclosed]

Students debarred:
[List with reasons]

Certified by: [Principal Name], Principal
Date: [Date]
School Seal: [SEAL]
```

---

## 7. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/attendance/exam-eligibility/?exam_id={id}&date={date}` | Eligibility list for exam |
| 2 | `GET` | `/api/v1/school/{id}/attendance/exam-eligibility/{student_id}/?exam_id={id}` | Student-wise + subject-wise eligibility |
| 3 | `POST` | `/api/v1/school/{id}/attendance/exam-eligibility/{student_id}/condone/` | Prepare condonation application |
| 4 | `POST` | `/api/v1/school/{id}/attendance/exam-eligibility/{student_id}/block/` | Block from exam (Principal) |
| 5 | `GET` | `/api/v1/school/{id}/attendance/exam-eligibility/report/?exam_id={id}` | Certification report PDF |
| 6 | `GET` | `/api/v1/school/{id}/attendance/exam-eligibility/condonation-applications/?exam_id={id}` | All condonation applications PDF/ZIP |

---

## 8. Business Rules

- 75% threshold is a CBSE hard rule — the system does not allow the school to set it lower for board exams; for school internal exams, the threshold is school-configurable (but must be ≥ 75%)
- The condonation zone (65–75%) is for CBSE board exams only; for school internal exams, schools typically enforce their own policy (many don't condone anything)
- A student blocked from board exam (< 65%) is never in the CBSE LOC — attempting to include them in B-33 LOC gives a hard error
- Condonation applications are submitted to CBSE via the Regional Office — EduForge generates the application in CBSE's prescribed format; the school physically submits it
- The eligibility computation runs at the time of E-11 page load (on-demand) — it is not stored as a separate field to avoid stale data; always recomputed from raw attendance records

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division E*
