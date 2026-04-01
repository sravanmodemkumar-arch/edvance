# B-20 — Result Analytics

> **URL:** `/school/academic/results/<exam_id>/analytics/`
> **File:** `b-20-result-analytics.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Exam Cell Head (S4) — full · HOD (S4) — own dept · Academic Coordinator (S4) — full · VP Academic (S5) — full · Principal (S6) — full · Class Teacher (S3) — read own class

---

## 1. Purpose

Post-result analytical dashboard for a specific exam — gives the Exam Cell Head, HODs, and Principal a complete picture of how the school performed. While B-05 (Department Analytics) focuses on one department, B-20 is school-wide and exam-specific. Identifies toppers, at-risk students, subject-wise failure trends, and class-level performance to guide remedial planning, teacher accountability conversations, and CBSE annual performance report submissions.

---

## 2. Page Layout

### 2.1 Header
```
Result Analytics — Annual Exam 2025–26            [Export Report]  [Print]
Exam: Annual Exam 2025–26  ·  Published: 28 Mar 2026
Filter: Class [All ▼]  Subject [All ▼]
```

---

## 3. School-wide Summary (KPI Strip)

| Metric | Value | vs Last Exam | vs Last Year |
|---|---|---|---|
| Total Appeared | 2,182 | — | ↑ 68 |
| Pass % | 96.4% | ↑ 0.8% | ↑ 1.2% |
| Avg Score | 74.8% | ↑ 1.4% | ↑ 2.0% |
| A1 Grade (91–100%) | 244 (11.2%) | ↑ 1.1% | ↑ 2.4% |
| Distinction (75%+) | 842 (38.6%) | ↑ 2.2% | ↑ 3.1% |
| Fail (< 33%) | 78 (3.6%) | ↓ 0.4% | ↓ 0.8% |
| Compartment (1–2 subj fail) | 24 (1.1%) | ↓ 0.2% | → same |
| Remedial needed (< 35% any subj) | 142 (6.5%) | ↓ 0.6% | ↓ 1.2% |

---

## 4. Class-wise Performance Table

| Class | Section | Appeared | Pass % | Avg % | A1+ | Fail | Compartment | Rank 1 Student |
|---|---|---|---|---|---|---|---|---|
| XII | MPC | 38 | 100% | 81.4% | 12 | 0 | 0 | Priya Sharma 94.2% |
| XII | BiPC | 22 | 100% | 78.2% | 6 | 0 | 0 | Deepa Kumar 91.8% |
| XI | A | 40 | 95.0% | 74.2% | 8 | 1 | 1 | Rohit K 88.6% |
| X | A | 42 | 97.6% | 72.8% | 7 | 1 | 0 | Anjali D 90.4% |
| IX | A | 42 | 95.2% | 70.4% | 4 | 2 | 0 | Arjun S 87.2% |
| IX | B | 40 | 92.5% | 67.8% | 2 | 3 | 0 | Ravi K 85.4% |
| … | … | … | … | … | … | … | … | … |

Click any row → student-level breakdown for that class.

---

## 5. Subject-wise Performance Heatmap

Grid: Class levels (rows) × Subjects (columns) = avg score %

Colour: <50% red · 50–65% amber · 65–80% yellow · >80% green

| | English | Hindi | Maths | Physics | Chemistry | Biology | History | Econ |
|---|---|---|---|---|---|---|---|---|
| **IX** | 74.2% | 68.4% | 72.1% | 68.8% | 64.2% | 61.4% | 70.6% | — |
| **X** | 76.4% | 70.2% | 74.8% | 71.2% | 68.4% | 64.8% | 72.4% | — |
| **XI MPC** | 71.8% | — | 77.4% | 74.2% | 72.8% | — | — | — |
| **XI BiPC** | 70.4% | — | — | — | 70.2% | 68.4% | — | — |
| **XII** | 74.6% | — | 78.2% | 78.8% | 76.4% | 72.2% | — | — |

Click any cell → top 5 and bottom 5 students in that class-subject.

---

## 6. Topper List (School-wide)

| Rank | Student | Class | % | Grade | Subjects |
|---|---|---|---|---|---|
| 1 | Priya Sharma | XII-MPC | 94.2% | A1 | Physics, Chemistry, Maths, English, CS |
| 2 | Deepa Kumar | XII-BiPC | 91.8% | A1 | Biology, Chemistry, Maths, English, Hindi |
| 3 | Anjali Das | X-A | 90.4% | A1 | All 5 subjects |
| 4 | Arjun Sharma | IX-A | 87.2% | A2 | All 6 subjects |

[Generate Merit Certificate] per topper → PDF certificate with student name, rank, percentage, school seal.

[Export Topper List] → for felicitation event announcement, school magazine.

---

## 7. Students Needing Attention (< 35% in any subject)

| Student | Class | Subjects at Risk | Scores | Class Teacher | Action |
|---|---|---|---|---|---|
| Deepak M | XI-A | Chemistry | 28/80 (35%) | Ms. Kavitha | [Remedial Plan] |
| Ravi P | IX-C | Mathematics (28%), Hindi (31%) | Low | Mr. Suresh | [Remedial Plan] |
| Anand T | VII-B | Science | 22/80 (27.5%) | Ms. Priya | [Remedial Plan] |

[Remedial Plan] → adds student to B-34 (Remedial Teaching Register) with pre-filled subject details.

---

## 8. Grade Distribution Chart

Doughnut chart per class showing grade distribution:
- A1 (91–100%) — Gold
- A2 (81–90%) — Green
- B1 (71–80%) — Teal
- B2 (61–70%) — Blue
- C1 (51–60%) — Yellow
- C2 (41–50%) — Orange
- D (33–40%) — Light Red
- E (< 33%, Fail) — Red

---

## 9. Score Distribution Histogram

Per subject-class, histogram showing number of students in mark bands:
- Helps spot bimodal distributions
- Compared against previous exam to spot regression

---

## 10. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/exams/{exam_id}/analytics/summary/` | School-wide KPI summary |
| 2 | `GET` | `/api/v1/school/{id}/exams/{exam_id}/analytics/class-wise/` | Class performance table |
| 3 | `GET` | `/api/v1/school/{id}/exams/{exam_id}/analytics/heatmap/` | Subject heatmap |
| 4 | `GET` | `/api/v1/school/{id}/exams/{exam_id}/analytics/toppers/?limit=20` | Topper list |
| 5 | `GET` | `/api/v1/school/{id}/exams/{exam_id}/analytics/at-risk/` | At-risk students |
| 6 | `GET` | `/api/v1/school/{id}/exams/{exam_id}/analytics/distribution/?class_id={id}&subject_id={id}` | Grade/score distribution |
| 7 | `GET` | `/api/v1/school/{id}/exams/{exam_id}/analytics/toppers/{student_id}/certificate/` | Merit certificate PDF |
| 8 | `GET` | `/api/v1/school/{id}/exams/{exam_id}/analytics/export/` | Full analytics report PDF |

---

## 11. Business Rules

- Analytics are available only after results are published (B-18)
- At-risk student list (< 35%) auto-triggers remedial notification to class teacher and counsellor; this is logged in the Audit Log
- Class teacher can see analytics for their own class only; HOD for their department; Exam Cell Head for all
- Merit certificates use the school's letterhead template and are signed by Principal (digital signature applied)
- Export report generates an A4 booklet suitable for Principal presentation or CBSE annual report submission

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division B*
