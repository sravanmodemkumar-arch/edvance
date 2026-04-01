# A-13 — Student Strength Dashboard

> **URL:** `/school/admin/students/strength/`
> **File:** `a-13-student-strength-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Principal (S6) — full · Promoter (S7) — view · VP Academic (S5) — view · VP Admin (S5) — full · Admin Officer (S3) — view

---

## 1. Purpose

Single-page view of the school's complete student population — how many students, by class, section, gender, stream, student type (day scholar/hosteler/RTE), and admission status. This is the first page a new Principal checks to understand the school, and the page the Promoter uses to track seat fill against targets.

---

## 2. Page Layout

### 2.1 Header
```
Student Strength — 2025–26                  [Export] [Print]
Academic Year: 2025–26 ▼       As of: 26 Mar 2026    [Filters ▼]
```

### 2.2 KPI Strip (5 cards)

| Card | Metric |
|---|---|
| Total Enrolled | 1,048 students |
| New This Year | 312 admitted in 2025–26 |
| Seat Fill Rate | 87.3% (1,048 / 1,200 capacity) |
| Hostelers | 248 (Boys: 138 · Girls: 110) |
| RTE Students | 84 (8.0% — target: 25%) |

---

## 3. Main Sections

### 3.1 Class-wise Strength Table (default view)

| Class | Sections | Capacity | Enrolled | Boys | Girls | Hostelers | RTE | Vacancy |
|---|---|---|---|---|---|---|---|---|
| LKG | A, B, C | 90 | 78 | 40 | 38 | 0 | 8 | 12 |
| UKG | A, B, C | 90 | 82 | 42 | 40 | 0 | 9 | 8 |
| Class I | A, B, C, D | 120 | 142 | 72 | 70 | 0 | 14 | — (Over) |
| Class II–V | … | … | … | … | … | … | … | … |
| Class IX | A, B, C, D | 120 | 112 | 58 | 54 | 32 | 8 | 8 |
| Class X | A, B, C, D | 120 | 108 | 57 | 51 | 34 | 8 | 12 |
| Class XI | MPC/BiPC/Com/Hum | 120 | 76 | 42 | 34 | 24 | 0 | 44 |
| Class XII | MPC/BiPC/Com/Hum | 120 | 73 | 40 | 33 | 28 | 0 | 47 |
| **TOTAL** | **52** | **1,200** | **1,048** | **540** | **508** | **248** | **84** | **152** |

Over-capacity rows shown in amber (Class I has 22 extra — needs section addition).

### 3.2 Section-wise drill-down

Click any class row → expands to show per-section breakdown:
| Section | Capacity | Enrolled | Boys | Girls | Class Teacher |
|---|---|---|---|---|---|
| Class I A | 30 | 36 | 18 | 18 | Ms. Padmaja |
| Class I B | 30 | 35 | 18 | 17 | Ms. Sunitha |
| … | … | … | … | … | … |

### 3.3 Student Type Summary (tab/toggle)

| Type | Count | % of Total |
|---|---|---|
| Day Scholar — Regular | 714 | 68.1% |
| Day Scholar — Scholarship | 42 | 4.0% |
| Day Scholar — RTE (25% free) | 84 | 8.0% |
| Hosteler — Boys | 138 | 13.2% |
| Hosteler — Girls | 110 | 10.5% |
| Special Needs (inclusive ed.) | 12 | 1.1% |
| NRI / Overseas | 3 | 0.3% |

---

## 4. Charts

### 4.1 Class-wise Fill Rate (bar chart)
- X-axis: Class (LKG–XII)
- Y-axis: Fill rate %
- Colour: Green ≥85% · Amber 70–84% · Red <70%

### 4.2 Gender Distribution by Level (stacked bar)
- Primary / Upper Primary / Secondary / Senior Secondary
- Boys vs Girls stacked

### 4.3 Year-over-Year Enrollment Trend (line chart)
- Lines: Current year vs last 3 years
- X-axis: Class · Y-axis: Students enrolled

---

## 5. Quick Actions

- [Export Student List] → CSV with all fields (class, section, roll no, name, gender, type, admission no)
- [View Admission Pipeline →] A-14
- [RTE Compliance →] A-15
- [Add New Sections for Over-capacity Classes] (alert button if any class > capacity)

---

## 6. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/students/strength/` | Strength summary data |
| 2 | `GET` | `/api/v1/school/{id}/students/strength/class-wise/` | Per-class table |
| 3 | `GET` | `/api/v1/school/{id}/students/strength/section-wise/{class_id}/` | Per-section for a class |
| 4 | `GET` | `/api/v1/school/{id}/students/strength/type-summary/` | By student type |
| 5 | `GET` | `/api/v1/school/{id}/students/strength/trend/?years=4` | Enrolment trend data |
| 6 | `GET` | `/api/v1/school/{id}/students/export/` | Full student list CSV |

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division A*
