# 14 — Attendance Analytics

> **URL:** `/group/analytics/attendance/`
> **File:** `14-attendance-analytics.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Roles:** Academic Data Analyst (Role 104, G1) · MIS Officer (Role 103, G1) · Analytics Director (Role 102, G1) · Strategic Planning Officer (Role 107, G1)

---

## 1. Purpose

Group-wide attendance analytics covering both day scholars and hostelers separately. Tracks attendance rates by branch, class, subject, and time period. Identifies critical patterns: Monday/Friday dips, post-exam attendance slumps, branches with chronic under-attendance, and the gap between day scholar and hosteler attendance (hosteler should be higher as they live on campus — a significant gap suggests a problem). Also cross-references attendance with exam performance to identify the correlation (low attendance → low scores). Hostelers have two attendance records daily: morning class attendance and night roll call — both tracked. Data feeds into monthly MIS reports and dropout signal scoring.

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Academic Data Analyst | 104 | G1 | Full — all data, export, add notes | Primary owner |
| Group MIS Officer | 103 | G1 | Full — all data, export | For MIS reports |
| Group Analytics Director | 102 | G1 | View + Export | Oversight |
| Group Strategic Planning Officer | 107 | G1 | View + Export | Planning reference |
| Group Hostel Analytics Officer | 106 | G1 | View — hosteler attendance only | Hostel focus |
| All other roles | — | — | No access | Redirected |

> **Access enforcement:** `@require_role(['academic_data_analyst', 'mis_officer', 'analytics_director', 'strategic_planning_officer', 'hostel_analytics_officer'])`. Role 106 gets a queryset filtered to `student_type = hosteler`.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Analytics & MIS  ›  Attendance Analytics
```

### 3.2 Page Header
```
Attendance Analytics                            [Export ↓]
[Group Name]  ·  Data as of: [date]
AY [current academic year]  ·  Month: [current month selector] ·  [N] Branches Reporting
```

`[Export ↓]` — dropdown: Export to PDF / Export to XLSX. Roles 102, 103, 104, 107.
Month selector — changes the reporting period for all sections. Default: current month.

### 3.3 Alert Banners (conditional)

| Condition | Banner Text | Severity |
|---|---|---|
| Branches below 75% attendance this month | "[N] branch(es) have group-wide attendance below 75% this month: [list]." | Red |
| Month-over-month attendance drop > 5% | "Group average attendance dropped by [N]% compared to last month." | Amber |
| Day scholar attendance significantly below hosteler in same branch | "[N] branch(es) show day scholar attendance more than 15% lower than hosteler attendance. Possible transport issue." | Amber |
| Students with < 50% attendance not flagged in dropout monitor | "[N] students have attendance below 50% but are not yet in the dropout signal monitor." | Amber |
| Attendance data not updated for current month | "Attendance data has not been submitted for the current month at [N] branch(es)." | Amber |

---

## 4. KPI Summary Bar

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Group Average Attendance | Avg attendance % across all students, selected month | `AttendanceRecord.objects.filter(month=selected_month).aggregate(Avg('att_pct'))` | Green ≥ 90% · Amber 80–89% · Red < 80% | `#kpi-group-avg` |
| 2 | Day Scholar Avg Attendance | Avg for day scholars only | — | Same colour rules | `#kpi-day-scholar` |
| 3 | Hosteler Avg Attendance | Avg for hostelers only | — | Same colour rules | `#kpi-hosteler` |
| 4 | Students < 75% Attendance | Students below the critical threshold (minimum attendance for exams) | `DropoutScore.objects.filter(att_30d_pct__lt=75).count()` | Red > 500 · Amber 100–499 · Green < 100 | `#kpi-below-75` |
| 5 | Students < 50% Attendance | Students at critical attendance (usually barred from exams) | `AttendanceRecord.objects.filter(att_cumulative_pct__lt=50).count()` | Red if > 0 | `#kpi-below-50` |
| 6 | Branches Below 80% | Branches where avg attendance < 80% this month | `BranchAttendance.objects.filter(month=selected_month, avg_pct__lt=80).count()` | Red > 3 · Amber 1–3 · Green = 0 | `#kpi-branches-below-80` |
| 7 | Highest Absentee Day | Day of week with most absences group-wide | Computed from daily data | Indigo (neutral) | `#kpi-absent-day` |

**HTMX:** `<div id="att-kpi-bar" hx-get="/api/v1/group/{id}/analytics/attendance/kpi/?month={month}" hx-trigger="load, every 300s" hx-swap="innerHTML">`. KPI bar reloads when month changes.

---

## 5. Sections

### 5.1 Branch Attendance Summary Table

**Search bar:** Branch name, city. Debounced 300ms.

**Filter chips:** `[Zone ▾]` `[State ▾]` `[Branch Type ▾]` `[Attendance Range ▾]` `[Student Type ▾]`

| Column | Source Field | Sortable | Notes |
|---|---|---|---|
| Branch | `branch_name` | ▲▼ | Clickable → `attendance-branch-detail` drawer |
| Zone | `zone_name` | ▲▼ | — |
| Total Students | `total_students` | ▲▼ | — |
| Day Scholar Avg (%) | `day_scholar_att_pct` | ▲▼ | Colour: ≥ 90% green · 80–89% amber · 75–79% orange · < 75% red |
| Hosteler Avg (%) | `hosteler_att_pct` | ▲▼ | Same colour rules; "—" if no hostel |
| Combined Avg (%) | `combined_att_pct` | ▲▼ | Overall branch avg |
| Students < 75% | `students_below_75` | ▲▼ | Red badge if > 10 |
| Students < 50% | `students_below_50` | ▲▼ | Red badge if > 0 |
| vs Last Month | `delta_mom_pct` | ▲▼ | "+2.1%" green · "-3.5%" red |
| Night Roll Call Compliance | `night_roll_pct` | ▲▼ | Hosteler branches only; "—" otherwise |
| Last Updated | `data_last_updated` | ▲▼ | Amber if > 7 days |
| Actions | — | — | `[View]` |

**Default sort:** Combined Avg ascending (lowest first).
**Pagination:** 25 rows · `« Previous  Page N of N  Next »`.

### 5.2 Attendance Pattern Heatmap

**Heading:** "Day-of-Week Attendance Pattern — [Selected Month]"

A 6-column mini heatmap (Mon–Sat) × branches (rows), showing avg attendance % per day.

Colour scale: < 70% = dark red → 70–79% = amber → 80–89% = yellow → 90–94% = light green → 95–100% = dark green.

Below heatmap: Bar chart showing group-wide avg attendance by day of week (Mon/Tue/Wed/Thu/Fri/Sat).

### 5.3 Critical Attendance Alerts

Students with < 50% cumulative attendance (group-wide). Compact table — top 50 by attendance %, lowest first.

| Column | Notes |
|---|---|
| Student Name | — |
| Branch | — |
| Class | — |
| Cumulative Attendance % | Red badge |
| Days Present | out of total working days |
| Exam Eligibility | Auto-derived: typically < 75% = ineligible; shown as badge |

`[View All in Dropout Monitor →]` link to Page 12 with `<75%` filter pre-applied.

---

## 6. Drawers & Modals

### 6.1 `attendance-branch-detail` Drawer — 680px, right-slide

**Trigger:** Clicking branch name or `[View]` in §5.1.

**Header:**
```
[Branch Name] — Attendance Analytics                        [×]
[Zone]  ·  [City], [State]
Combined Avg: [N]%  ·  Day Scholar: [N]%  ·  Hosteler: [N]%  ·  Month: [selected month]
```

**Tab 1 — Monthly Overview**

Cards: Day Scholar Avg, Hosteler Avg, Combined Avg, Students < 75%, Students < 50%, Working Days This Month.

Bar chart: Monthly attendance (last 6 months) — grouped bars: Day Scholar + Hosteler.

**Tab 2 — By Class**

Table: Class | Total Students | Day Scholar Avg | Hosteler Avg | Below 75% Count.
Sorted by combined avg ascending.

**Tab 3 — By Subject**

Table: Subject | Teacher | Avg Attendance | vs Branch Avg | Gap?.
If subject attendance is significantly below branch avg → flag with amber badge.
Note: subject-level data shown only if branch submits subject-wise data; otherwise shows "Subject-level data not available."

**Tab 4 — Critical Students**

Table of students in this branch with attendance < 75%:
Student Name | Class | Att % | Days Absent | Fee Status | Dropout Risk Score | In Monitor?

`[View in Dropout Monitor →]` link per student (Role 104 only).

**Tab 5 — Day-of-Week Pattern**

Bar chart: avg attendance per day of week (Mon–Sat) for this branch.
Shows which days have lowest attendance.

### 6.2 Export Modal — 480px, centred

**Trigger:** `[Export ↓]` header button.

| Field | Type | Required | Notes |
|---|---|---|---|
| Report Type | Select | Yes | Branch Summary / Critical Students / Day-of-Week Analysis / Full Report |
| Period | Select | Yes | Current Month / Last Month / Custom Date Range / Full AY |
| Branches | Multi-select | No | Default: all |
| Student Type | Radio | No | All / Day Scholar / Hosteler |
| Format | Radio | Yes | PDF · XLSX |

**Footer:** `[Cancel]`  `[Generate Export]`

---

## 7. Charts

### 7.1 Attendance Trend Line — Multi-Line Chart

| Property | Value |
|---|---|
| Chart type | Multi-line (Chart.js 4.x) |
| Title | "Group Attendance Trend — Last 12 Months" |
| Data | Monthly group avg attendance %: Day Scholar, Hosteler, Combined (3 lines) |
| X-axis | Month names (last 12 months) |
| Y-axis | Attendance % (50–100% range for clarity) |
| Line colours | Day Scholar: blue · Hosteler: teal · Combined: indigo |
| Reference lines | Horizontal dotted lines at 75% (critical) and 90% (target) |
| Tooltip | "[Month] · Day Scholar: [N]% · Hosteler: [N]% · Combined: [N]%" |
| Legend | Bottom |
| Empty state | "Insufficient attendance data for trend." |
| Export | PNG button |
| API endpoint | `GET /api/v1/group/{id}/analytics/attendance/trend/?months=12` |
| HTMX | `hx-trigger="load"`; reloads on month selector change |

### 7.2 Branch Attendance Comparison — Horizontal Bar

| Property | Value |
|---|---|
| Chart type | Horizontal bar (Chart.js 4.x) |
| Title | "Branch Attendance — [Selected Month]" |
| Data | Combined avg attendance % per branch, selected month |
| Y-axis | Branch names (sorted by attendance ASC) |
| X-axis | Attendance % (0–100%) |
| Bar colour | Green ≥ 90% · Amber 80–89% · Orange 75–79% · Red < 75% per bar |
| Reference line | Vertical dotted at 75% and 90% |
| Tooltip | "[Branch]: [N]% · Day Scholar: [N]% · Hosteler: [N]%" |
| Empty state | "No attendance data for the selected period." |
| Export | PNG button |
| API endpoint | `GET /api/v1/group/{id}/analytics/attendance/by-branch/?month={month}` |
| HTMX | Reloads when month selector changes |

---

## 8. Toast Messages

| Action | Toast Text | Type |
|---|---|---|
| Export generated | "Attendance report exported to [format]." | Success |
| Export failed | "Could not generate export. Please try again." | Error |
| Branch detail drawer load error | "Could not load attendance data for this branch." | Error |
| KPI refresh error | "Failed to refresh KPI data." | Error |

---

## 9. Empty States

| Context | Icon | Heading | Sub-text | Action |
|---|---|---|---|---|
| No attendance data for selected month | `calendar` | "No Attendance Data" | "Attendance records have not been submitted for the selected month." | — |
| No branches reporting | `building-office` | "No Branches Reporting" | "No branches have submitted attendance data for this period." | — |
| No results after filter | `funnel` | "No Branches Match Filters" | "Try adjusting or clearing your filters." | `[Clear Filters]` |
| No students < 50% | `check-circle` | "No Critical Attendance" | "No students have attendance below 50% for this period." | — |
| Branch detail — subject data not available | `book-open` | "No Subject Data" | "Subject-wise attendance records are not available for this branch." | — |
| Charts — no data | `chart-bar` | "No data available" | — | — |

---

## 10. Loader States

| Context | Loader Behaviour |
|---|---|
| Initial page load | KPI bar: 7 shimmer cards. Charts: 2 shimmer rectangles. Table: 8 shimmer rows. |
| Month selector change | KPI bar shimmer + table shimmer + charts shimmer (all reload together) |
| Search/filter change | Table rows shimmer |
| `attendance-branch-detail` drawer open | Drawer slides in; shimmer tabs + content |
| Tab switch in drawer | Shimmer in tab content area |
| Export generate | Button disabled + "Generating…" + spinner |
| KPI auto-refresh | Cards pulse; values update in place |
| Pagination | Table body shimmer |

---

## 11. Role-Based UI Visibility

| UI Element | Role 104 | Role 103 | Role 102 | Role 107 | Role 106 |
|---|---|---|---|---|---|
| Page | ✅ | ✅ | ✅ | ✅ | ✅ |
| KPI Bar — all 7 cards | ✅ | ✅ | ✅ | ✅ | Hosteler cards only |
| Charts | ✅ Both | ✅ Both | ✅ Both | ✅ Both | ✅ Both (hosteler filter) |
| Branch table — all columns | ✅ | ✅ | ✅ | ✅ | Hosteler cols only |
| Branch detail drawer — all tabs | ✅ | ✅ | ✅ | ✅ | Tabs 1 + 4 (hosteler) |
| Branch detail — Tab 4 `[View in Dropout Monitor]` link | ✅ | ✅ | ✅ | ❌ | ❌ |
| Critical attendance alerts section | ✅ | ✅ | ✅ | ✅ | Hosteler only |
| `[Export ↓]` button | ✅ | ✅ | ✅ | ✅ | ❌ |
| Alert banners | ✅ All | ✅ All | ✅ All | ✅ All | Hosteler-relevant only |

---

## 12. API Endpoints

### 12.1 KPI Summary
```
GET /api/v1/group/{group_id}/analytics/attendance/kpi/
```
Query: `month` (YYYY-MM), `academic_year`.
Response: `{ "group_avg": N, "day_scholar_avg": N, "hosteler_avg": N, "below_75": N, "below_50": N, "branches_below_80": N, "highest_absentee_day": "Monday" }`.

### 12.2 Branch Attendance Summary
```
GET /api/v1/group/{group_id}/analytics/attendance/branches/
```

| Query Parameter | Type | Description |
|---|---|---|
| `month` | string (YYYY-MM) | Default current month |
| `academic_year` | string | Default current |
| `zone` | string | Zone ID |
| `state` | string | State name |
| `branch_type` | string | `day` · `hostel` · `both` |
| `att_range` | string | `above_90` · `80_89` · `75_79` · `below_75` |
| `student_type` | string | `day_scholar` · `hosteler` · `all` |
| `search` | string | Branch name |
| `page` | integer | Default 1 |
| `page_size` | integer | 25 · 50 · All |
| `ordering` | string | `combined_att_pct` (ASC default) · `branch_name` · `students_below_75` |

### 12.3 Branch Detail
```
GET /api/v1/group/{group_id}/analytics/attendance/branches/{branch_id}/
```
Query: `month`.
Response: Full detail — monthly overview, class breakdown, subject breakdown (if available), critical students, day-of-week pattern.

### 12.4 Trend Chart
```
GET /api/v1/group/{group_id}/analytics/attendance/trend/
```
Query: `months` (default 12).
Response: `{ labels: [...months], day_scholar: [...], hosteler: [...], combined: [...] }`.

### 12.5 Branch Chart
```
GET /api/v1/group/{group_id}/analytics/attendance/by-branch/
```
Query: `month`.
Response: `{ labels: [...branch_names], data: [...pcts], colours: [...hex] }`.

### 12.6 Export
```
GET /api/v1/group/{group_id}/analytics/attendance/export/
```
Query: `report_type`, `period`, `branches` (comma-separated), `student_type`, `format` (pdf/xlsx).
Response: File download.

---

## 13. HTMX Patterns

| Pattern | Trigger Element | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI bar load + month change | `<div id="att-kpi-bar">` + `<select id="month-selector">` | GET `.../attendance/kpi/?month={month}` | `#att-kpi-bar` | `innerHTML` | `hx-trigger="load"` on div; `hx-trigger="change"` on selector |
| Chart 7.1 load | `<div id="chart-trend">` | GET `.../attendance/trend/` | `#chart-trend` | `innerHTML` | `hx-trigger="load"` |
| Chart 7.2 load + month change | `<div id="chart-by-branch">` | GET `.../attendance/by-branch/?month={month}` | `#chart-by-branch` | `innerHTML` | `hx-trigger="load"`, reloads on month change |
| Table search | `<input id="att-search">` | GET `.../attendance/branches/?search=` | `#attendance-table` | `innerHTML` | `hx-trigger="keyup changed delay:300ms"` |
| Table filter | Filter chip selects | GET `.../attendance/branches/?filters=` | `#attendance-table` | `innerHTML` | `hx-trigger="change"` |
| Table pagination | Pagination buttons | GET `.../attendance/branches/?page={n}` | `#attendance-table` | `innerHTML` | `hx-trigger="click"` |
| Month selector change — reload all | `<select id="month-selector">` | Multiple: kpi + table + chart 7.2 | `#att-kpi-bar`, `#attendance-table`, `#chart-by-branch` | `innerHTML` | `hx-trigger="change"` on selector with `hx-swap-oob="true"` targets |
| Open branch detail drawer | Branch name / `[View]` | GET `/htmx/analytics/attendance/branches/{id}/detail/?month={month}` | `#drawer-container` | `innerHTML` | `hx-trigger="click"` |
| Drawer tab switch | Tab buttons | GET `/htmx/analytics/attendance/branches/{id}/tab/{slug}/` | `#att-drawer-tab-content` | `innerHTML` | `hx-trigger="click"` |
| Export modal — generate | Export form | GET `.../attendance/export/?params=` | — | — | Triggers file download |
| KPI auto-refresh | `#att-kpi-bar` | GET `.../attendance/kpi/?month={current_month}` | `#att-kpi-bar` | `innerHTML` | `hx-trigger="every 300s"` |

---

*Page spec version: 1.0 · Last updated: 2026-03-22*
