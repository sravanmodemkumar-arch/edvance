# 16 — Teacher Performance Analytics

> **URL:** `/group/analytics/teachers/`
> **File:** `16-teacher-performance-analytics.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Academic Data Analyst (Role 104, G1) · Analytics Director (Role 102, G1) · MIS Officer (Role 103, G1) · Exam Analytics Officer (Role 105, G1)

---

## 1. Purpose

Objective, data-driven analysis of teacher performance across all branches using student outcome data — not subjective appraisals. The system derives a Composite Teacher Performance Score from five measurable dimensions: (1) Student Outcomes (avg exam scores in teacher's classes vs branch/group avg), (2) Attendance Proxy (avg student attendance in teacher's periods — low attendance = poor engagement), (3) Syllabus Completion Rate (% of curriculum completed on schedule per Division B data), (4) CPD Participation (professional development trainings attended), and (5) Lesson Plan Compliance (% submitted on time). This page surfaces high performers for recognition and alerts on underperformers for coaching intervention. SENSITIVE: data is for Group-level analysis only — individual performance scores are NOT shared with teachers or branch principals via this page. Access is strictly G1 Analytics roles.

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Academic Data Analyst | 104 | G1 | Full — view all, export, add notes | Primary owner |
| Group Analytics Director | 102 | G1 | View + Export — no notes | Oversight |
| Group MIS Officer | 103 | G1 | View + Export — no notes | For reporting |
| Group Exam Analytics Officer | 105 | G1 | View — student outcomes dimension only | Limited columns |
| All other roles | — | — | No access | Redirected; sensitive data |

> **Access enforcement:** `@require_role(['academic_data_analyst', 'analytics_director', 'mis_officer', 'exam_analytics_officer'])`. Role 105 receives only columns: Teacher Name, Branch, Subject, Student Outcomes Score. Sensitive data notice logged for every access.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Analytics & MIS  ›  Teacher Performance Analytics
```

### 3.2 Page Header
```
Teacher Performance Analytics          [Sensitive: G1 Analytics Access Only 🔒]    [Export ↓]
[Group Name]  ·  AY [academic year]  ·  [N] Teachers Analysed  ·  Last Updated: [date]
```

`[Export ↓]` — Roles 102, 103, 104. Export includes a watermark/header: "CONFIDENTIAL — For Analytics Use Only."

### 3.3 Alert Banners (conditional)

| Condition | Banner Text | Severity |
|---|---|---|
| Teachers with composite score < 40 for 2+ months | "[N] teacher(s) have had a composite performance score below 40 for 2 or more consecutive months." | Red |
| Branches with > 30% teachers below threshold | "[N] branch(es) have more than 30% of their teachers with a performance score below the threshold." | Amber |
| Teachers with no CPD participation in 12+ months | "[N] teacher(s) have not attended any CPD training in the past 12 months." | Amber |
| Teacher data not updated for > 14 days | "Teacher performance data has not been refreshed in [N] days." | Amber |

---

## 4. KPI Summary Bar

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Total Teachers Analysed | Teachers with at least one performance record | `TeacherScore.objects.filter(ay=current_ay).values('teacher').distinct().count()` | Indigo (neutral) | `#kpi-total-teachers` |
| 2 | High Performers (≥ 80) | Teachers with composite score ≥ 80 | — | Green always | `#kpi-high-performers` |
| 3 | Performance Alerts (< 50) | Teachers with composite score < 50 | — | Red > 20 · Amber 5–20 · Green < 5 | `#kpi-alerts` |
| 4 | Group Avg Composite Score | Mean composite score across all teachers | — | Green ≥ 70 · Amber 60–69 · Red < 60 | `#kpi-avg-score` |
| 5 | Branches with Staff Gaps | Branches where > 30% teachers are below threshold | — | Red > 0 · Green = 0 | `#kpi-branches-gaps` |
| 6 | CPD Participation Rate | % of teachers who attended ≥ 1 CPD session this AY | — | Green ≥ 80% · Amber 60–79% · Red < 60% | `#kpi-cpd-rate` |

**HTMX:** `<div id="teacher-kpi-bar" hx-get="/api/v1/group/{id}/analytics/teachers/kpi/" hx-trigger="load, every 300s" hx-swap="innerHTML">`.

---

## 5. Sections

### 5.1 Teacher Performance Table

**Search bar:** Teacher name, subject, branch. Debounced 300ms.

**Filter chips:** `[Branch ▾]` `[Subject ▾]` `[Score Band ▾]` `[Stream ▾]` `[CPD Status ▾]`

| Column | Source Field | Sortable | Notes |
|---|---|---|---|
| Teacher Name | `teacher_name` | ▲▼ | Clickable → `teacher-performance-detail` drawer |
| Branch | `branch_name` | ▲▼ | — |
| Subject | `subject_name` | ▲▼ | Primary subject taught |
| Class/Section | `class_section` | ▲▼ | e.g. "Class 11 MPC" |
| Composite Score | `composite_score` | ▲▼ | 0–100 badge; colour: ≥ 80 green · 60–79 blue · 50–59 amber · 40–49 orange · < 40 red |
| Student Outcomes | `outcomes_score` | ▲▼ | Sub-score; avg student exam score in teacher's classes |
| Attendance Proxy | `attendance_proxy_score` | ▲▼ | Sub-score |
| Syllabus Completion | `syllabus_score` | ▲▼ | Sub-score; "—" if not tracked |
| CPD Sessions | `cpd_sessions_ay` | ▲▼ | Count of CPD sessions attended this AY |
| Lesson Plan Compliance | `lesson_plan_pct` | ▲▼ | % on time |
| Experience (Years) | `experience_years` | ▲▼ | Total teaching experience |
| vs Branch Avg | `vs_branch_avg` | ▲▼ | ±delta from branch average teacher score |
| Actions | — | — | `[View]` · `[Add Note]` (Role 104) |

**Default sort:** Composite Score ascending (underperformers first).
**Pagination:** 25 rows per page.

### 5.2 High Performer Spotlight

Top 10 teachers by composite score. Displayed as a condensed card row above the main table. Collapsed by default; `[▸ Show Top Performers]` expands.

Each card: Teacher name, subject, branch, composite score badge.

### 5.3 Branch-wise Performance Summary

Compact table showing aggregate performance per branch.

| Column | Notes |
|---|---|
| Branch | — |
| Teacher Count | — |
| Avg Composite Score | Colour coded |
| High Performers | Count (≥ 80) |
| Performance Alerts | Count (< 50) |
| CPD Participation Rate | % |
| Trend vs Last AY | ↑/↓/→ |

---

## 6. Drawers & Modals

### 6.1 `teacher-performance-detail` Drawer — 560px, right-slide

**Trigger:** Clicking teacher name or `[View]` in table.

**Header:**
```
[Teacher Name]                                             [×]
[Branch]  ·  [Subject]  ·  [Class/Section]
Composite Score: [N] [badge]  ·  Experience: [N] years
[CONFIDENTIAL label]
```

**Tab 1 — Overview**

Composite score breakdown — progress bars per dimension:

```
Student Outcomes (30%)   ████████████████░░░░ 76/100
Attendance Proxy (25%)   █████████████████░░░ 80/100
Syllabus Completion (20%) ████████████████████ 95/100
CPD Participation (15%)  ████████░░░░░░░░░░░░ 45/100
Lesson Plan Compliance (10%) ██████████████████ 88/100
─────────────────────────────────────────────────
Composite Score:                                78.4/100
```

**Tab 2 — Student Outcomes**

Line chart — avg exam score of teacher's classes over last 5 exams, with branch class average as a second line.
Table: Exam Name | Date | Classes Taught | Class Avg | Branch Class Avg | Delta.

**Tab 3 — Attendance & Syllabus**

Attendance proxy: Bar chart — avg student attendance % per subject period per month (last 6 months).
Syllabus completion: Month-by-month progress bar (% completed vs expected).
Lesson plan compliance: Table — Month | Plans Expected | Submitted | Compliance %.

**Tab 4 — CPD & Development**

List of CPD sessions attended this AY: Date | Session Name | Duration | Provider.
Certification status if any.
AY-over-AY CPD comparison (last 3 AYs): bar chart.

**Tab 5 — History**

YoY composite score table — last 3 AYs. All 5 sub-scores per AY.

**Actions (Role 104 only):**
`[Add Internal Note]` button at drawer footer.
Note textarea (min 20 chars) + `[Save Note]` button.
Notes history list below form.

### 6.2 Export Modal — 480px, centred

| Field | Type | Required | Notes |
|---|---|---|---|
| Report Type | Select | Yes | Full Performance Report / High Performers / Performance Alerts / CPD Status Report / Branch Summary |
| Academic Year | Select | Yes | Current + prev 2 |
| Branches | Multi-select | No | Default: all |
| Subject | Multi-select | No | Default: all |
| Score Band | Multi-select | No | Default: all |
| Format | Radio | Yes | PDF · XLSX |

Confidentiality notice: "Exported data is confidential. Do not share outside Analytics team."

**Footer:** `[Cancel]`  `[Generate Export]`

---

## 7. Charts

### 7.1 Teacher Score Distribution — Histogram

| Property | Value |
|---|---|
| Chart type | Vertical bar (Chart.js 4.x) |
| Title | "Teacher Performance Score Distribution — [Current AY]" |
| Data | Count of teachers in score bands: 0–39 / 40–49 / 50–59 / 60–69 / 70–79 / 80–89 / 90–100 |
| X-axis | Score bands |
| Y-axis | Teacher count |
| Bar colour | 0–49: red · 50–59: amber · 60–79: blue · 80–100: green |
| Tooltip | "[Band]: [N] teachers ([N]%)" |
| Interactive | Click on bar → applies score band filter to table |
| Empty state | "No teacher performance data available." |
| Export | PNG button |
| API endpoint | `GET /api/v1/group/{id}/analytics/teachers/distribution/` |
| HTMX | `hx-trigger="load"` |

### 7.2 Subject-wise Average Performance — Bar Chart

| Property | Value |
|---|---|
| Chart type | Horizontal bar (Chart.js 4.x) |
| Title | "Average Teacher Performance by Subject — [Current AY]" |
| Data | Mean composite score per subject across all teachers |
| Y-axis | Subject names |
| X-axis | Avg composite score |
| Bar colour | Colour coded per score range |
| Tooltip | "[Subject]: [N] avg composite score · [N] teachers" |
| Empty state | "No data available." |
| Export | PNG button |
| API endpoint | `GET /api/v1/group/{id}/analytics/teachers/by-subject/` |
| HTMX | `hx-trigger="load"` |

---

## 8. Toast Messages

| Action | Toast Text | Type |
|---|---|---|
| Note saved | "Note saved for [Teacher Name]." | Success |
| Note error | "Could not save note. Please try again." | Error |
| Export generated | "Teacher performance report exported. This file is confidential." | Success |
| Export failed | "Could not generate export. Please try again." | Error |
| Drawer load error | "Could not load teacher data. Please try again." | Error |
| KPI refresh error | "Failed to refresh KPI data." | Error |

---

## 9. Empty States

| Context | Icon | Heading | Sub-text | Action |
|---|---|---|---|---|
| No teachers analysed | `users` | "No Teacher Data" | "No teacher performance records have been loaded for this academic year." | — |
| No high performers | `star` | "No High Performers Yet" | "No teachers have a composite score of 80 or above yet." | — |
| No performance alerts | `check-circle` | "No Performance Alerts" | "All teachers are above the alert threshold." | — |
| No results after filter | `funnel` | "No Teachers Match Filters" | — | `[Clear Filters]` |
| Teacher detail — no CPD data | `academic-cap` | "No CPD Records" | "No CPD session attendance has been recorded for this teacher." | — |
| Teacher detail — no syllabus data | `book-open` | "No Syllabus Data" | "Syllabus completion data is not tracked for this branch." | — |
| Charts — no data | `chart-bar` | "No data available" | — | — |

---

## 10. Loader States

| Context | Loader Behaviour |
|---|---|
| Initial page load | KPI bar: 6 shimmer cards. Charts: 2 shimmer rectangles. Main table: 8 shimmer rows. |
| Search/filter change | Table shimmer |
| Teacher detail drawer open | Shimmer tabs + progress bar skeleton |
| Tab switch in drawer | Shimmer content |
| Export generate | Button disabled + spinner + confidentiality notice shown |
| KPI auto-refresh | Cards pulse |
| Pagination | Table body shimmer |
| Chart — score band click | Table shimmer while applying filter |

---

## 11. Role-Based UI Visibility

| UI Element | Role 104 | Role 102 | Role 103 | Role 105 |
|---|---|---|---|---|
| Page | ✅ | ✅ | ✅ | ✅ |
| Sensitive data notice banner | ✅ All | ✅ All | ✅ All | ✅ All |
| KPI Bar | Full | Full | Full | KPI 1 + 2 only |
| Main table — all columns | ✅ | ✅ | ✅ | Name, Branch, Subject, Outcomes Score only |
| High performer spotlight | ✅ | ✅ | ✅ | ❌ |
| Branch summary section | ✅ | ✅ | ✅ | ❌ |
| `[Add Note]` in table row | ✅ | ❌ | ❌ | ❌ |
| Teacher detail drawer — all tabs | ✅ | ✅ | ✅ | Tab 2 (outcomes) only |
| `[Add Internal Note]` in drawer | ✅ | ❌ | ❌ | ❌ |
| `[Export ↓]` button | ✅ | ✅ | ✅ | ❌ |
| Alert banners | ✅ All | ✅ All | ✅ All | ✅ First 2 only |

---

## 12. API Endpoints

### 12.1 KPI Summary
```
GET /api/v1/group/{group_id}/analytics/teachers/kpi/
```
Query: `academic_year`.
Response: `{ "total_teachers": N, "high_performers": N, "performance_alerts": N, "avg_composite": N, "branches_with_gaps": N, "cpd_participation_pct": N }`.

### 12.2 Teacher Performance Table
```
GET /api/v1/group/{group_id}/analytics/teachers/
```

| Query Parameter | Type | Description |
|---|---|---|
| `academic_year` | string | Default current |
| `branch` | int | Branch ID |
| `subject` | string | Subject slug |
| `score_band` | string | `high` (≥80) · `medium` (50–79) · `alert` (<50) |
| `stream` | string | `mpc` · `bipc` · `mec` |
| `cpd_status` | string | `attended` · `not_attended` |
| `search` | string | Teacher name, subject, branch |
| `page` | integer | Default 1 |
| `page_size` | integer | 25 · 50 · 100 |
| `ordering` | string | `composite_score` (ASC default) · `teacher_name` · `branch_name` · `outcomes_score` |

### 12.3 Teacher Detail
```
GET /api/v1/group/{group_id}/analytics/teachers/{teacher_id}/
```
Response: Full detail — all sub-scores, student outcome data, attendance proxy, syllabus, CPD, lesson plan, historical data (last 3 AYs), notes.

### 12.4 Add Teacher Note
```
POST /api/v1/group/{group_id}/analytics/teachers/{teacher_id}/notes/
```
Body: `{ "note": "string" }`. Role 104 only.
Response: 201 Created.

### 12.5 Score Distribution
```
GET /api/v1/group/{group_id}/analytics/teachers/distribution/
```
Response: `{ "0_39": N, "40_49": N, "50_59": N, "60_69": N, "70_79": N, "80_89": N, "90_100": N }`.

### 12.6 By Subject
```
GET /api/v1/group/{group_id}/analytics/teachers/by-subject/
```
Response: `[{ subject, avg_score, teacher_count }]` sorted by avg_score ASC.

### 12.7 Export
```
GET /api/v1/group/{group_id}/analytics/teachers/export/
```
Query: `report_type`, `academic_year`, `branches`, `subject`, `score_band`, `format`.
Response: File download (with confidential watermark in PDF).

---

## 13. HTMX Patterns

| Pattern | Trigger Element | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI bar load + auto-refresh | `<div id="teacher-kpi-bar">` | GET `.../teachers/kpi/` | `#teacher-kpi-bar` | `innerHTML` | `hx-trigger="load, every 300s"` |
| Chart 7.1 load | `<div id="chart-distribution">` | GET `.../teachers/distribution/` | `#chart-distribution` | `innerHTML` | `hx-trigger="load"` |
| Chart 7.2 load | `<div id="chart-by-subject">` | GET `.../teachers/by-subject/` | `#chart-by-subject` | `innerHTML` | `hx-trigger="load"` |
| Table search | `<input id="teacher-search">` | GET `.../teachers/?search=` | `#teacher-table` | `innerHTML` | `hx-trigger="keyup changed delay:300ms"` |
| Table filter | Filter chip selects | GET `.../teachers/?filters=` | `#teacher-table` | `innerHTML` | `hx-trigger="change"` |
| Table pagination | Pagination buttons | GET `.../teachers/?page={n}` | `#teacher-table` | `innerHTML` | `hx-trigger="click"` |
| Score band chart click | Distribution bar | GET `.../teachers/?score_band={band}` | `#teacher-table` | `innerHTML` | JS `chartClick` → HTMX `hx-get` |
| Open teacher detail drawer | Teacher name / `[View]` | GET `/htmx/analytics/teachers/{id}/detail/` | `#drawer-container` | `innerHTML` | `hx-trigger="click"` |
| Drawer tab switch | Tab buttons | GET `/htmx/analytics/teachers/{id}/tab/{slug}/` | `#teacher-drawer-tab-content` | `innerHTML` | `hx-trigger="click"` |
| Add note (table row) | `[Add Note]` button | GET `/htmx/analytics/teachers/note-modal/?teacher={id}` | `#modal-container` | `innerHTML` | Role 104; `hx-trigger="click"` |
| Save note | Note form | POST `.../teachers/{id}/notes/` | `#teacher-notes-{id}` | `innerHTML` | `hx-on::after-request="showToast(event);"` |

---

*Page spec version: 1.0 · Last updated: 2026-03-22*
