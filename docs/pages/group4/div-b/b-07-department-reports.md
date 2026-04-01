# B-07 — Department Academic Reports

> **URL:** `/college/academic/dept-reports/`
> **File:** `b-07-department-reports.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** HOD (S4) — own department · Dean Academics (S5) — all departments · Principal/Director (S6)

---

## 1. Purpose

Department-level academic performance reporting — aggregates student results, attendance, CIE performance, course completion, and teaching quality into a semester report for each department. Used for:
- Internal academic review (monthly department meeting)
- NAAC Self-Study Report data (criterion 2 — Teaching-Learning & Evaluation)
- NIRF ranking data (teaching and research indicators)
- Annual report to academic council

---

## 2. Department Report — CSE Semester II 2026–27

```
DEPARTMENT REPORT — CSE (Computer Science & Engineering)
HOD: Dr. Kavitha R.  |  Semester II 2026–27
Report date: 30 May 2027

1. ENROLMENT:
   B.Tech CSE students: 332 (Year I: 120, Year II: 84, Year III: 76, Year IV: 52)
   Lateral entry (Year II): 12

2. ATTENDANCE:
   Department average: 87.4% ✅
   Students detained (at least 1 subject): 28 (8.4%)
   JNTU condonation applications: 14 (processing)

3. CIE PERFORMANCE:
   Department average CIE score: 21.8 / 30 (72.7%) ✅
   Subject with lowest CIE: EE201 (Basic Electrical) — 64.2% ⚠
   Remedial classes arranged for EE201: ✅ 8 extra hours (March)

4. FACULTY & TEACHING:
   Faculty: 18 (17 full-time, 1 visiting)
   Average feedback score: 3.97 / 5.0
   Low-scoring faculty: 1 (Mr. Pradeep T., EE201 — 3.42; under review)
   Syllabus completion (all courses): 94.8% ✅
   Lesson plans submitted: 17/17 ✅; Approved by HOD: 17/17 ✅

5. RESULTS (University exam — Sem I 2026–27, received Jan 2027):
   Overall pass %: 88.1%
   Distinctions (SGPA ≥8.0): 32 students (9.6%)
   Backlogs: 64 students (total subject-wise backlogs: 84)

6. INITIATIVES THIS SEMESTER:
   ● Industry expert guest lectures: 4 (TCS, Wipro, NASSCOM, local startup)
   ● Industry visit: CYIENT Hyderabad (40 students, 14 Mar 2027)
   ● Student paper presentations: 6 (Technical Symposium, 22 Feb)
   ● NPTEL courses enrolled: 24 students; 18 completed ✅

7. RECOMMENDATIONS:
   ① EE201 (Basic Electrical) faculty issue — discuss with Dean Academics
   ② Add one more NPTEL FDP slot for faculty (CSE department)
   ③ Increase industry interactions for Year III (for placement readiness)

[Download department report PDF]  [Submit to Dean Academics]
```

---

## 3. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/college/{id}/academic/dept-report/?dept={dept}&semester={sem}` | Department semester report |
| 2 | `GET` | `/api/v1/college/{id}/academic/dept-report/all/` | All departments summary |
| 3 | `POST` | `/api/v1/college/{id}/academic/dept-report/submit/` | Submit report to Dean Academics |

---

## 4. Business Rules

- Department reports must be produced at the end of each semester (within 30 days of results); this is the HOD's accountability document; a department that cannot produce a coherent semester report has a governance gap
- NAAC criterion 2 data is largely drawn from department reports; a college that has structured department reports across 3+ years has a significantly easier NAAC preparation process than one that scrambles for data
- Cross-department comparisons (Dean's view): The Dean sees all department reports together; persistent underperformance in one department requires dean-level intervention; the EduForge report identifies outlier departments automatically by comparing key metrics (pass rate, attendance, CIE, feedback score) across departments

---

*Last updated: 2026-03-27 · Group 4 — College Portal · Division B*
