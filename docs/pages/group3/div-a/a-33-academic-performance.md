# A-33 — Academic Performance Overview

> **URL:** `/school/admin/mis/academics/`
> **File:** `a-33-academic-performance.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Principal (S6) — full · VP Academic (S5) — full · Promoter (S7) — view · HOD (S4) — view own department

---

## 1. Purpose

Deep-dive into academic performance metrics — exam results, subject-wise scores, topper analysis, bottom-performer identification, and year-on-year trend comparison. Gives the VP Academic and Principal the data they need to make decisions: which departments need support, which teachers' classes are consistently underperforming, which students need remedial attention. In the Indian school context, this data is also submitted to CBSE/state board as part of annual performance reports.

---

## 2. Page Layout

### 2.1 Header
```
Academic Performance Overview               [Export Report] [Print]
Exam: [Last Half-Yearly ▼]  Class: [All ▼]  Subject: [All ▼]  Year: [2025–26 ▼]
```

---

## 3. Main Sections

### 3.1 School-wide Performance Summary (current selected exam)

| Metric | Value | vs Last Exam | vs Last Year |
|---|---|---|---|
| Total Students Appeared | 1,022 | — | ↑ 42 |
| Pass % | 97.4% | ↑ 0.6% | ↑ 1.2% |
| Avg Score (all subjects) | 74.2% | ↑ 1.4% | ↑ 2.1% |
| A+ Grade (>90%) | 142 (13.9%) | ↑ 1.2% | ↑ 2.4% |
| Below 35% (risk group) | 28 (2.7%) | ↓ 0.3% | ↓ 0.5% |
| Distinction (>75%) | 398 (38.9%) | ↑ 2.1% | ↑ 3.2% |

---

### 3.2 Class-wise Performance Table

| Class | Total | Pass | Pass % | Avg % | A+ | Fail | Highest | Lowest |
|---|---|---|---|---|---|---|---|---|
| XII MPC | 38 | 38 | 100% | 81.2% | 12 | 0 | 96.4% | 52.2% |
| XII BiPC | 22 | 22 | 100% | 78.4% | 6 | 0 | 93.2% | 48.8% |
| X A | 42 | 40 | 95.2% | 72.1% | 8 | 2 | 91.4% | 31.2% |
| IX B | 40 | 38 | 95.0% | 69.8% | 5 | 2 | 88.6% | 28.4% |
| … | … | … | … | … | … | … | … | … |

Click any row → opens class-wise subject breakdown.

---

### 3.3 Subject-wise Performance Heatmap

Grid: Class (row) × Subject (column) = avg score.
Colour: <50% red · 50–65% amber · 65–80% yellow · >80% green.

Click any cell → shows top-5 and bottom-5 students in that class-subject.

---

### 3.4 Topper List (A+ > 90%)

| Rank | Student | Class | % | Subjects |
|---|---|---|---|---|
| 1 | Priya Sharma | XII MPC | 96.4% | All 5 subjects |
| 2 | Rohit K | XII MPC | 95.2% | All 5 subjects |
| … | … | … | … | … |

[Felicitation Certificate] → generates merit certificate PDF per topper.

---

### 3.5 Students Needing Attention (< 35% in any subject)

| Student | Class | Subject(s) at Risk | Score | Class Teacher | Action |
|---|---|---|---|---|---|
| Ajay M | IX A | Maths (28%), Science (32%) | Poor | Ms. Priya | [Remedial Plan] |

[Remedial Plan] → notifies class teacher + subject teacher + counsellor.

---

### 3.6 Year-on-Year Trend

Line chart: Pass % and Avg Score per class level × 4 academic years.

---

## 4. Department-wise Analysis (for HOD view)

When HOD logs in:
- Same data filtered to their department's subjects only
- Their classes + their subject performance highlighted

---

## 5. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/academic-performance/summary/?exam_id={id}` | School-wide summary |
| 2 | `GET` | `/api/v1/school/{id}/academic-performance/class-wise/?exam_id={id}` | Class table |
| 3 | `GET` | `/api/v1/school/{id}/academic-performance/heatmap/?exam_id={id}` | Subject heatmap |
| 4 | `GET` | `/api/v1/school/{id}/academic-performance/toppers/?exam_id={id}&threshold=90` | Topper list |
| 5 | `GET` | `/api/v1/school/{id}/academic-performance/at-risk/?exam_id={id}&threshold=35` | At-risk students |
| 6 | `GET` | `/api/v1/school/{id}/academic-performance/trend/?class_level={level}&years=4` | YoY trend |
| 7 | `GET` | `/api/v1/school/{id}/academic-performance/toppers/{student_id}/certificate/` | Merit certificate PDF |

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division A*
