# H-06 — Teaching Workload & Timetable

> **URL:** `/college/hr/workload/`
> **File:** `h-06-workload.md`
> **Priority:** P2
> **Roles:** HOD (S4) · Dean Academics (S5) · HR Officer (S3) · Principal/Director (S6)

---

## 1. Workload Norms

```
TEACHING WORKLOAD NORMS — GCEH
(AICTE 2019 + UGC guidelines for engineering colleges)

WORKLOAD REQUIREMENTS:
  Assistant Professor: 16 hours/week (direct teaching — theory + lab combined)
  Associate Professor: 14 hours/week
  Professor:           14 hours/week (with research allocation)

  Lab hours: 1 lab session (2–3 hours) counts as 1 hour for workload
             → So 4 lab sessions/week + 8 theory = 4×1 + 8 = 12 hours minimum (Assoc. Prof.)
  Tutorial/consultation: Up to 2 hours/week can be included in 14/16 hours

  AICTE definition of "contact hours": Face-to-face with students
  Preparation time, evaluation: Not counted in contact hours but recognized implicitly

MAXIMUM WORKLOAD (to prevent overloading):
  AICTE: No explicit maximum; UGC guidance: ≤20 hours/week for professors
  GCEH policy: Max 20 contact hours/week for any faculty
  HOD: Max 12 hours (admin responsibilities)
  Principal: Max 6 hours (token teaching to maintain academic connect)

STUDENT-FACULTY RATIO (for AICTE compliance):
  B.Tech: 1:15 (AICTE) — GCEH current: 1:12.9 ✅
  M.Tech: 1:12 — GCEH: 1:8 ✅ (small intake)
  MBA/MCA: 1:25 — GCEH: 1:16 ✅
```

---

## 2. Workload Register

```
WORKLOAD REGISTER — Semester II 2026–27 (January–June 2027)
CSE Department

Faculty          | Designation    | Theory hrs | Lab hrs | Tutorial | Total | Norm | Status
──────────────────────────────────────────────────────────────────────────────────────────────────
Dr. Suresh K.    | Assoc. Prof.   | 12         | 2       | 0        | 14    | 14   | ✅ Exact
Dr. Priya M.     | HOD + Assoc.   | 6          | 2       | 0        | 8     | 12   | ✅ (HOD adj.)
Dr. Ramesh D.    | Asst. Prof.    | 12         | 4       | 0        | 16    | 16   | ✅ Exact
Mr. Arun M.      | Asst. Prof.    | 14         | 4       | 2        | 20    | 16   | ⚠️ Over 16
Ms. Deepa R.     | Asst. Prof.    | 12         | 4       | 0        | 16    | 16   | ✅ Exact
Mr. Kiran T.     | Contract       | 16         | 0       | 0        | 16    | 16   | ✅
Mr. Suresh M.    | Contract       | 18         | 0       | 0        | 18    | 16   | ⚠️ Over 16

MR. ARUN M. OVERLOAD:
  Current load: 20 hours (16 norm + 4 extra = 4 hours extra)
  Cause: 3rd faculty member left in December 2026; load redistributed temporarily
  EduForge alert: ⚠️ Overload flagged (auto-notification to HOD + Principal)
  Action: 2 subjects redistributed to Mr. Suresh M. (contract) + visiting faculty
  Revised load from Feb 2027: 17 hours (still slightly over — acceptable interim)
  Resolution: New faculty joins June 2027 → normalised next semester
```

---

## 3. Timetable Integration

```
MASTER TIMETABLE — CSE Sem II 2026–27 (Summary)

WORKLOAD ALLOCATION PROCESS:
  Step 1: Course coordinator assigns subjects to faculty (based on expertise + workload)
  Step 2: HOD reviews allocation (no faculty below minimum; none above maximum)
  Step 3: Timetable master generated (EduForge → B-03 / AICTE norm check)
  Step 4: Timetable published to students + faculty (start of semester)

WORKLOAD COMPLIANCE MONITORING (ongoing):
  EduForge checks weekly: Any faculty missing classes (absences create temporary underload)
  Substitution: Recorded in substitute register; workload recalculated
  Annual workload statement: Signed by each faculty (for service book + appraisal)

EXAM WORKLOAD:
  Invigilation duties: Distributed fairly (per semester schedule)
  Evaluation (paper correction): JNTU external papers → 3 days evaluation duty
  CIE evaluation: Faculty evaluates own section's scripts
  All exam workload: Counted separately from regular teaching hours (not in 14/16-hr cap)
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/college/{id}/hr/workload/?semester=2027-2` | Semester workload register |
| 2 | `GET` | `/api/v1/college/{id}/hr/workload/alerts/` | Overload/underload alerts |
| 3 | `GET` | `/api/v1/college/{id}/hr/workload/{faculty_id}/annual/` | Annual workload statement |

---

## 5. Business Rules

- AICTE's 1:15 student-faculty ratio applies to sanctioned intake, not actual enrolled students; if intake is 180 and actual enrolment is 160, the PTR is computed on 180; a college that maintains faculty count based on actual enrolment and then fills intake to maximum will violate PTR the very next semester; staffing decisions must be based on sanctioned intake
- Overload (beyond maximum contact hours) is an HR and academic risk; a faculty member consistently teaching 20+ hours/week cannot maintain teaching quality, prepare adequately, or pursue research; NAAC Criterion 2 (Teaching-Learning) and faculty burnout data both suffer; the overload alert in EduForge ensures the Principal is aware and takes corrective action rather than letting it continue silently
- The annual workload statement (signed by faculty) serves as evidence that the college has conducted the required teaching hours; in NAAC Criterion 2.3 and AICTE inspection, the question is always "how many teaching hours were actually conducted?"; the statement, cross-referenced with timetable and attendance records, provides an audit-grade answer
- Contract faculty workload is identical to regular faculty workload in terms of minimum contact hours; some colleges try to extract more teaching hours from contract faculty (who lack the security to refuse); this is exploitative and also means research time is zero for contract faculty; GCEH's equal workload norm treats contract and regular faculty identically in teaching hours
- Timetable generated without workload analysis leads to uneven distribution — some faculty overloaded, others underutilized; systematic workload calculation before timetable creation (EduForge's sequence: workload → timetable, not timetable → workload) ensures equitable distribution and AICTE compliance simultaneously

---

*Last updated: 2026-03-27 · Group 4 — College Portal · Division H*
