# B-05 — Department Performance Analytics

> **URL:** `/school/academic/dept/<dept>/analytics/`
> **File:** `b-05-dept-analytics.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** HOD (S4) — full own dept · Exam Cell Head (S4) — read all depts · Academic Coordinator (S4) — full all depts · Principal (S6) — full · VP Academic (S5) — full

---

## 1. Purpose

Deep analytical view of the department's academic performance — exam results, teacher effectiveness, syllabus delivery, student progression, and year-on-year trends. While B-01 (Department Dashboard) gives a daily operational snapshot, B-05 provides the analytical depth the HOD needs for annual reviews, teacher appraisals, Principal presentations, and CBSE performance submissions. This is where patterns emerge: which topics students consistently fail, which teacher's classes outperform, whether the department's result trend is improving.

---

## 2. Page Layout

### 2.1 Header
```
Department Performance Analytics — Science      [Export Report]  [Print]
Exam: [All Exams 2025–26 ▼]  Subject: [All ▼]  Class: [All ▼]  Compare Year: [2024–25 ▼]
```

---

## 3. Section 1 — Department Summary (Current Year)

| Metric | Value | vs Last Exam | vs Last Year |
|---|---|---|---|
| Total Students Appeared | 612 | — | ↑ 28 |
| Department Pass % | 96.4% | ↑ 0.8% | ↑ 1.4% |
| Avg Score (all subjects) | 74.8% | ↑ 2.1% | ↑ 2.6% |
| A+ (> 90%) | 88 (14.4%) | ↑ 1.6% | ↑ 2.2% |
| Below 35% (at-risk) | 22 (3.6%) | ↓ 0.4% | ↓ 1.0% |
| Best Subject (avg) | Chemistry XII-A: 81.2% | — | — |
| Weakest Subject (avg) | Biology XI-A: 58.4% | — | ↓ 1.2% |

---

## 4. Section 2 — Subject-wise Performance (Current Year)

Sortable table of every subject × class combination:

| Subject | Class | Appeared | Pass % | Avg % | A+ | Below 35 | Highest | Lowest |
|---|---|---|---|---|---|---|---|---|
| Physics | XII-A | 38 | 100% | 81.2% | 11 | 0 | 96.4% | 52.2% |
| Physics | XII-B | 36 | 97.2% | 76.8% | 7 | 1 | 92.6% | 29.4% |
| Chemistry | XII-A | 38 | 100% | 78.4% | 8 | 0 | 94.2% | 51.8% |
| Biology | XI-A | 40 | 90.0% | 58.4% | 2 | 4 | 84.6% | 22.2% |
| Physics | XI-A | 40 | 92.5% | 68.2% | 3 | 2 | 88.4% | 31.2% |

Click any row → shows student-level marks distribution for that subject-class.

---

## 5. Section 3 — Teacher Performance Analysis

Aggregated from all their subject-class assignments:

| Teacher | Classes | Avg Pass % | Avg Score | A+ Count | Below 35 | Lesson Plan Score | Syllabus % |
|---|---|---|---|---|---|---|---|
| Ms. Lakshmi Devi | Physics XII-A, XI-B | 98.6% | 79.0% | 18 | 1 | 4.3/5 | 78.4% |
| Mr. Ravi Kumar | Chemistry XII-A, XI-A | 97.2% | 74.6% | 12 | 2 | 4.5/5 | 74.1% |
| Ms. Anjali Singh | Biology XI-A, X-A, IX-B | 91.4% | 62.8% | 5 | 8 | 3.8/5 | 62.3% |
| Dr. Suresh P | Physics XI-A, X-A | 94.0% | 70.4% | 6 | 3 | 4.7/5 | 77.2% |

**Composite Score** = weighted average of: Avg Pass % (40%) + Avg Score (30%) + LP Score (20%) + Syllabus % (10%)

This section is visible to HOD and above only — not to teachers themselves.

---

## 6. Section 4 — Topic-level Failure Analysis

Which topics are students consistently failing across exams? Computed from marks entry data + HOD-tagged topics:

| Topic | Subject | Class | Avg Score on Topic | Fail Rate | Trend |
|---|---|---|---|---|---|
| Meiosis — Stages | Biology | XI | 42.3% | 38% | ↓ worse |
| Nernst Equation | Chemistry | XII | 48.6% | 24% | → stable |
| Wave Optics — Interference | Physics | XII | 51.2% | 18% | ↑ improving |
| Heredity — Pedigree Charts | Biology | X | 44.1% | 31% | ↓ worse |

**Action buttons:**
- [Flag for Remedial] → adds to B-34 (Remedial Teaching) as a suggested topic
- [Add to LP Template] → adds a note to lesson plan template for this topic: "Emphasise diagrams"
- [HOD Observation] → schedules an observation class for the teacher teaching this topic

---

## 7. Section 5 — Year-on-Year Trend (4 Years)

Line chart with:
- X-axis: Academic years (2022–23, 2023–24, 2024–25, 2025–26)
- Y-axis: Pass % and Avg Score
- One line per subject-class combination (filterable)
- Benchmark line: CBSE national average (loaded from board data if available, else manual entry)

Insight callouts generated automatically:
- "Physics XII-A has improved pass % by 8.2% over 4 years — consistent growth"
- "Biology XI-A has fallen 4.1% below last year — second consecutive year of decline"

---

## 8. Section 6 — Score Distribution (Current Year)

Histogram per subject showing student score distribution in bands:
- 0–35% (fail), 35–50%, 50–65%, 65–80%, 80–90%, 90–100%

Visualised as stacked bar chart per class for each subject. Helps spot bimodal distributions (where there are two clusters: high scorers and low scorers with nothing in between — typical when a class has students who attend coaching and those who don't).

---

## 9. Section 7 — Exam-wise Trend (Within Year)

Tracks a single subject's performance across all exams in the year:

| Exam | Physics XI-A — Avg Score | Pass % |
|---|---|---|
| Periodic Test 1 | 58.4% | 85.0% |
| Periodic Test 2 | 62.1% | 87.5% |
| Half-Yearly | 66.8% | 90.0% |
| Periodic Test 3 | 70.2% | 92.5% |

Trend line with annotation if score drops significantly between exams (regression flag).

---

## 10. Export Report

[Export Report] → generates a department annual performance report PDF:
- Cover page: Department, HOD name, Academic Year
- Summary section (Section 1 metrics)
- Subject-wise tables
- Year-on-year trend charts
- Teacher performance table
- HOD's narrative (free text input before export)
- Signature line for HOD and Principal

Used for CBSE annual report submissions and internal Principal review.

---

## 11. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/dept/{dept_id}/analytics/summary/?year={year}` | Dept summary |
| 2 | `GET` | `/api/v1/school/{id}/dept/{dept_id}/analytics/subject-wise/?exam_id={id}` | Subject × class table |
| 3 | `GET` | `/api/v1/school/{id}/dept/{dept_id}/analytics/teacher-performance/?year={year}` | Teacher performance |
| 4 | `GET` | `/api/v1/school/{id}/dept/{dept_id}/analytics/topic-failures/?exam_id={id}` | Topic failure analysis |
| 5 | `GET` | `/api/v1/school/{id}/dept/{dept_id}/analytics/trend/?years=4` | Year-on-year trend |
| 6 | `GET` | `/api/v1/school/{id}/dept/{dept_id}/analytics/distribution/?exam_id={id}&subject_id={id}` | Score distribution |
| 7 | `GET` | `/api/v1/school/{id}/dept/{dept_id}/analytics/exam-trend/?subject_id={id}&class_id={id}` | Within-year exam trend |
| 8 | `GET` | `/api/v1/school/{id}/dept/{dept_id}/analytics/export/?year={year}` | Report PDF (async) |

---

## 12. Business Rules

- Teacher performance data (Section 5) is visible only to HOD (own dept), VP Academic, and Principal — not to the teacher or other staff
- Year-on-year comparison requires result data from prior years to be present; missing years shown as "Data not available"
- Topic-level failure analysis requires that exam marks are entered at topic/question level (not just subject total); only available when B-16 uses detailed marks entry mode
- CBSE national average benchmark data is manually updated by Academic Coordinator once CBSE releases national performance data (typically August)
- Export report PDF generation is an async task for large departments; download link sent to HOD's in-app notification

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division B*
