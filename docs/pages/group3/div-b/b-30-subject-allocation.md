# B-30 — Subject Allocation Manager

> **URL:** `/school/academic/dept/<dept>/allocation/`
> **File:** `b-30-subject-allocation.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** HOD (S4) — full own dept · VP Academic (S5) — read all · Timetable Coordinator (S3) — read · Principal (S6) — full

---

## 1. Purpose

The HOD assigns which teacher in their department teaches which subject to which class and section for the academic year. This allocation is the critical input that the Timetable Builder (B-07) needs — it cannot assign periods without knowing who teaches what. Subject allocation also determines who can enter marks in B-16, who needs to submit lesson plans in B-23, and whose performance is tracked under which subject in B-05. Done once at the start of the year, reviewed mid-year if a teacher joins, leaves, or needs reassignment. In an Indian school, this is the HOD's annual planning responsibility before the academic year begins.

---

## 2. Page Layout

### 2.1 Header
```
Subject Allocation — Science Department           [Save Allocation]  [Export Plan]  [Submit to Timetable]
HOD: Dr. Priya Venkataraman  ·  Academic Year: 2025–26
Department Teachers: 8  ·  Subjects: 6  ·  Class Sections: 24  ·  Periods Needed: 186/week
Allocation Status: ⚠️ Draft (not yet submitted to Timetable Coordinator)
```

---

## 3. Teacher Load Summary

Quick overview of each teacher's allocated load:

| Teacher | Designation | Total Periods/Week | Classes Assigned | Status |
|---|---|---|---|---|
| Ms. Lakshmi Devi | PGT Physics | 32 | XI-A, XI-B, XII-A, XII-B | ✅ Within norm |
| Mr. Ravi Kumar | PGT Chemistry | 30 | XI-A, XI-B, XII-A, XII-B | ✅ Within norm |
| Ms. Anjali Singh | PGT Biology | 28 | IX-A, IX-B, X-A, XI-A, XI-B | ✅ Within norm |
| Dr. Suresh P | PGT Physics | 30 | IX-A, IX-B, X-A, X-B | ✅ Within norm |
| Ms. Leela K | TGT Science | 24 | VI-A, VI-B, VII-A, VII-B | ✅ Within norm |
| Mr. Dinesh S | TGT Science | 22 | VIII-A, VIII-B | 🟡 Underloaded |
| Ms. Pooja R | TGT Science | 18 | VI-C, VII-C | 🔴 Underloaded (< 20) |
| Ms. Kavitha M | TGT Science | 26 | VIII-C, VIII-D | ✅ Within norm |

**Teacher norms (CBSE/NCERT guidelines):**
- TGT (Trained Graduate Teacher): 24–30 periods/week
- PGT (Post Graduate Teacher): 24–36 periods/week
- Part-time: 12–18 periods/week

---

## 4. Main Allocation Grid

Class sections (rows) × Subjects (columns) = assigned teacher

### Science Department — Subject Allocation

| Class | Section | Physics | Chemistry | Biology | Env Science | Gen Science |
|---|---|---|---|---|---|---|
| VI | A | — | — | — | — | Ms. Leela K |
| VI | B | — | — | — | — | Ms. Leela K |
| VI | C | — | — | — | — | Ms. Pooja R |
| VII | A | — | — | — | — | Ms. Leela K |
| VII | B | — | — | — | — | Ms. Leela K |
| VIII | A | — | — | — | — | Mr. Dinesh S |
| VIII | B | — | — | — | — | Mr. Dinesh S |
| VIII | C | — | — | — | — | Ms. Kavitha M |
| IX | A | Dr. Suresh P | Mr. Ravi K | Ms. Anjali S | — | — |
| IX | B | Dr. Suresh P | Mr. Ravi K | Ms. Anjali S | — | — |
| X | A | Dr. Suresh P | Mr. Ravi K | Ms. Anjali S | — | — |
| X | B | Dr. Suresh P | [Unassigned] | Ms. Anjali S | — | — |
| XI | A | Ms. Lakshmi D | Mr. Ravi K | Ms. Anjali S | — | — |
| XI | B | Ms. Lakshmi D | Mr. Ravi K | Ms. Anjali S | — | — |
| XII | A | Ms. Lakshmi D | Mr. Ravi K | — | — | — |
| XII | B | Ms. Lakshmi D | Mr. Ravi K | — | — | — |

🔴 Red cells = unassigned (X-B Chemistry above).

---

## 5. Assign / Change Teacher

Click any cell → assignment dropdown:

```
Assign Chemistry Teacher — Class X-B

Available Chemistry Teachers:
  Mr. Ravi Kumar       (Currently: 30/36 periods → adding 6 = 36, at limit)
  Ms. Leela K          (Chemistry-qualified? ❌ — not in dept competency)
  [+ Request External Teacher from other dept]

[Assign Mr. Ravi Kumar]
[Leave Unassigned — Flag for Principal]
[Assign Visiting Teacher]
```

If no teacher is available and load limits are all full → HOD can flag for VP Academic to hire or request resource sharing from another school campus.

---

## 6. Periods-per-Week Configuration

For each class-subject assignment, the HOD sets the expected periods per week:

| Class | Subject | Periods/Week | Lab Periods (double) | Notes |
|---|---|---|---|---|
| XI-A | Physics | 6 | 2 (×2 = 4 periods counted) | Physics Lab on Mon P5+P6 |
| XI-A | Chemistry | 6 | 1 (×2 = 2 periods) | Chemistry Lab on Thu P5+P6 |
| XI-A | Biology | 5 | 1 (×2 = 2 periods) | Bio Lab on Fri P5+P6 |
| IX-A | Physics | 3 | 0 | Integrated in Science paper |
| IX-A | Gen Science Lab | 1 double period | 1 | Combined sci lab |

This feeds as requirements into the Timetable Builder (B-07) — the builder must find slots for exactly these many periods.

---

## 7. Validation & Conflicts

| Check | Status |
|---|---|
| All class-subject cells assigned | ⚠️ X-B Chemistry unassigned |
| Teacher loads within norms | ⚠️ Ms. Pooja underloaded (18 periods) |
| No teacher assigned to more than 2 consecutive double-periods | ✅ OK |
| Lab periods covered (qualified lab teacher) | ✅ All labs have science PGTs |
| Total periods match curriculum requirement | ✅ 186 of 186 periods planned |

---

## 8. Submit to Timetable Coordinator

[Submit to Timetable] → converts the allocation to timetable builder input.

Once submitted:
- Timetable Coordinator can see this department's allocation in B-07
- HOD can still make changes (will require re-submission)
- Principal is notified that Science dept allocation is ready

**All departments must submit allocation before B-07 (Timetable Builder) can begin.**

---

## 9. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/dept/{dept_id}/allocation/?year={year}` | Department allocation grid |
| 2 | `PATCH` | `/api/v1/school/{id}/dept/{dept_id}/allocation/cell/` | Assign teacher to class-subject |
| 3 | `GET` | `/api/v1/school/{id}/dept/{dept_id}/allocation/teacher-load/` | Teacher load summary |
| 4 | `GET` | `/api/v1/school/{id}/dept/{dept_id}/allocation/conflicts/` | Validation conflicts |
| 5 | `POST` | `/api/v1/school/{id}/dept/{dept_id}/allocation/submit/` | Submit to Timetable Coordinator |
| 6 | `GET` | `/api/v1/school/{id}/allocation/all-depts/` | Cross-dept view (VP Academic/Principal) |
| 7 | `GET` | `/api/v1/school/{id}/dept/{dept_id}/allocation/export/` | Export allocation plan PDF |

---

## 10. Business Rules

- HOD can only allocate teachers within their own department; if a teacher from another department teaches a cross-listed subject (e.g., a Commerce teacher teaching Maths), VP Academic manages that centrally
- A teacher cannot be assigned to a subject they are not qualified to teach (qualifications verified from A-16 staff profile; if no qualification, a warning is shown but not a hard block — HOD acknowledges)
- Allocation for the new year can be done from April/May; it does not affect the previous year's records
- If a teacher leaves mid-year, the HOD must update allocation and re-submit; the timetable coordinator then triggers a timetable rebuild
- Teacher load norms are CBSE guidelines — they are soft warnings, not hard blocks; a school can exceed them if required but the overload is flagged for Principal awareness

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division B*
