# 48 — Staff Attendance Overview (Group-Level)

- **URL:** `/group/hr/attendance/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Role:** Group HR Director (Role 41, G3)

---

## 1. Purpose

The Staff Attendance Overview provides the Group HR Director with a read-only, consolidated view of staff attendance across all branches. This is an aggregated monitoring page — actual attendance marking occurs at the branch level through biometric devices, manual registers, or branch-level ERP systems. Data from those branch systems is synchronised nightly into EduForge, where it is aggregated and surfaced here for group-level HR decision-making.

The primary operational value of this page lies in its ability to identify patterns that branch managers may not escalate: chronic absenteeism (defined as staff whose monthly attendance rate falls below 85% for two or more consecutive months), staff currently on long leave (medical, maternity, paternity, unpaid — each with distinct payroll treatment), and unauthorised absences (days marked absent without approved leave on record). Chronic absenteeism at a specific branch, especially if clustered among a particular department, can indicate a management culture problem, excessive workload, or unresolved grievances.

This attendance data has downstream dependencies in three other process areas: Salary Processing (attendance-linked salary deductions are calculated based on unauthorised absence days — this page feeds the payroll team their required inputs), Performance Appraisal (attendance is a scored KPI in all staff appraisals — staff below 85% annual attendance face a mandatory performance note), and Disciplinary Action (the Disciplinary Committee Head uses chronic absenteeism data from this page as the trigger for issuing Show-Cause Notices to habitual absentees).

The page does not allow HR to mark, edit, or correct attendance records — those operations belong to branch-level administration and branch principals. The HR Director can, however, drill down into a branch's attendance summary and view individual staff records for that branch, and flag staff for follow-up. The flagging creates a notification to the relevant Branch Principal, prompting them to investigate and resolve the discrepancy at source before the payroll processing deadline.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group HR Director | G3 | Read-only + Drill-down + Flag | Primary operator |
| Group HR Manager | G3 | Read-only + Drill-down | Operational support |
| Group Performance Review Officer | G1 | Read-only (attendance % column only) | Used for appraisal scoring |
| Group Disciplinary Committee Head | G3 | Read-only (chronic absentee list only) | Disciplinary trigger data |
| Branch Principal | G3 | Read-only (own branch only) | Aggregated view for own branch |
| All other roles | — | No access | Page not rendered |

---

## 3. Page Layout

### 3.1 Breadcrumb

```
Group Portal › HR & Staff › Staff Attendance Overview
```

### 3.2 Page Header

- **Title:** Staff Attendance Overview (Group-Level)
- **Subtitle:** Consolidated read-only attendance data — updated nightly from branch systems
- **Month Selector:** Month / Year picker at top-right (defaults to current month)
- **Secondary CTA:** `Export` (CSV/PDF — branch summary report)
- **Data freshness badge:** "Last synced: [timestamp]" shown in amber if sync > 24 hours old

### 3.3 Alert Banner (conditional)

- **Red:** `[N] branches are below 90% attendance rate for [Month]. Investigate.` Action: `View Branches`
- **Red:** `[N] staff members are chronic absentees (below 85% for 2+ consecutive months).` Action: `View List`
- **Amber:** `[N] staff have unauthorised absences this month not yet resolved for payroll.` Action: `View`
- **Blue:** `Attendance data sync last completed [timestamp]. Next sync at midnight.`
- **Green:** All branches above 90% and no chronic absentees — shown only when no active alerts

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Group Average Attendance Rate % | Average of all branch attendance rates for selected month | Green if ≥ 95%, amber 90–94%, red < 90% | No drill-down |
| Branches Below 90% | Count of branches with attendance_rate < 90% in selected month | Red if > 0, else green | Filter table to these branches |
| Chronic Absentees | Count of staff with attendance < 85% for 2+ consecutive months | Red if > 0, amber if 1–2, grey if 0 | Open chronic absentee list |
| Staff on Long Leave | Count with active leave record of type: Medical / Maternity / Paternity / Unpaid | Blue always | Filter to long leave view |
| Unauthorized Absences This Month | Count of distinct staff with ≥ 1 unauthorised absence day in selected month | Amber if > 0, else grey | Filter to UA view |
| Absent Today (Group-Wide) | Real-time count of staff marked absent today (best available — may be partial if not all branches synced) | Blue always | No drill-down |

---

## 5. Main Table — Branch Attendance Summary

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Branch | Text (link — click to drill down to branch individual staff attendance) | Yes (A–Z) | Yes — text search |
| Total Staff | Numeric | Yes | No |
| Present Rate % | Numeric with colour chip (green ≥ 95%, amber 90–94%, red < 90%) | Yes | Yes — range dropdown |
| Chronic Absentees | Numeric (count of chronic absentee staff in this branch) | Yes | Yes — has chronic toggle |
| On Long Leave | Numeric (count of staff on active long leave) | Yes | No |
| Unauthorized Absences | Numeric (staff count with ≥ 1 UA day this month) | Yes | Yes — has UA toggle |
| Status | Badge (On Track / Concern / Alert) | No | Yes — status dropdown |
| Actions | Icon buttons: View Details / Flag for Follow-up | No | No |

### 5.1 Filters

- **Status:** On Track / Concern / Alert / All
- **Present Rate Range:** Dropdown — ≥ 95% / 90–94% / < 90% / All
- **Has Chronic Absentees:** Toggle — Yes / All
- **Has Unauthorised Absences:** Toggle — Yes / All
- **Has Long Leave Staff:** Toggle — Yes / All
- **Reset Filters** button

### 5.2 Search

Text search on Branch name. Min 2 characters, 400 ms debounce.

### 5.3 Pagination

Server-side. Default 20 rows per page. Options: 10 / 20 / 50. "Showing X–Y of Z branches."

---

## 6. Drawers

### 6.1 Branch Drill-Down (View Details)

Triggered by clicking branch name or "View Details" action. Opens a wide drawer or navigates to a branch-scoped sub-page (implementation choice: drawer preferred for UX continuity).

**Displays:**
- Branch name and summary header
- Month selector (inherits from parent; adjustable within drawer)
- Individual staff attendance table:
  - Staff Name / Role / Department / Working Days / Days Present / Days Absent / Days on Leave / Attendance % / Leave Status
  - Sortable by Attendance %
  - Chronic absentees highlighted in red row
- Summary statistics for branch
- Link to branch-level attendance system (if external link available)

**Read-only.** No editing.

### 6.2 Chronic Absentee List (Overlay Panel)

Triggered from Chronic Absentees KPI card or Red alert banner.

**Displays:**
- Full-page overlay (or large drawer)
- Table: Staff Name / Branch / Role / Month 1 Attendance % / Month 2 Attendance % / Current Month Attendance % / Escalation Status
- Colour: Rows with 3+ consecutive months below 85% shown in red
- Action per row: "Initiate Show-Cause Notice" button (links to Disciplinary page 40 with pre-filled context)
- Action per row: "Flag to Branch Principal" (sends notification)

**Read-only list with action links.**

### 6.3 Flag for Follow-up

Short drawer. Triggered by "Flag for Follow-up" action in Actions column.

**Fields:**
- Branch (locked)
- Issue Type (dropdown: Chronic Absenteeism / Unauthorised Absences / Attendance Data Not Synced / Other)
- Note (textarea, min 50 characters)
- Notify Branch Principal: checkbox (default checked)
- Deadline for Response (date picker, defaults to 5 working days)

**Submit:** `Send Flag` → POST `/api/hr/attendance/flags/`

---

## 7. Charts

Two charts displayed below the main table.

### Chart A — Attendance Rate by Branch (Bar Chart with 90% Benchmark Line)

- **Type:** Vertical bar chart
- **X-axis:** Branch names
- **Y-axis:** Attendance rate %
- **Reference line:** 90% benchmark in dashed red
- **Bar colour:** Green ≥ 95%, amber 90–94%, red < 90%
- **Tooltip:** Branch, attendance %, present days, total working days
- **Month controlled by:** Parent page month selector
- **Export:** PNG

### Chart B — Group Average Attendance Monthly Trend (Line Chart)

- **Type:** Single line chart
- **X-axis:** Last 12 months
- **Y-axis:** Group average attendance rate %
- **Reference line:** 90% threshold in dashed red
- **Area fill:** Light green above 90%, light red below 90%
- **Tooltip:** Month, group average %
- **Export:** PNG

---

## 8. Toast Messages

| Trigger | Type | Message |
|---|---|---|
| Flag sent to branch principal | Success | "Follow-up flag sent to Branch Principal of [Branch]." |
| Export initiated | Info | "Generating attendance summary report. Downloading shortly." |
| Export ready | Success | "Attendance report downloaded." |
| Data sync warning | Warning | "Attendance data not synced in the last 24 hours. Figures may be outdated." |
| Server error | Error | "Failed to load attendance data. Please try again." |

---

## 9. Empty States

**No branches in table:**
> Icon: attendance register outline
> "No branch attendance data available yet."
> "Attendance data is synced nightly from branch systems. Check sync status or contact system admin."

**Branch drill-down — no staff data:**
> "No individual attendance records found for [Branch] for [Month]."
> "This may indicate that branch-level data has not been synced yet."

**Filtered results return nothing:**
> Icon: magnifying glass
> "No branches match your current filters."
> CTA: `Reset Filters`

---

## 10. Loader States

- Page load: Skeleton KPI bar + skeleton table rows (all branches)
- Month change: Full table skeleton while re-fetching for new month
- Branch drill-down drawer: Spinner while individual staff data loads
- Charts: Pulsing grey placeholder in chart area; independent load from table
- Export: Button spinner + "Generating..." while report builds

---

## 11. Role-Based UI Visibility

| UI Element | HR Director | HR Manager | Perf. Review Officer | Disc. Committee Head | Branch Principal |
|---|---|---|---|---|---|
| All KPI cards | Visible | Visible | Attendance % only | Chronic only | Own branch summary |
| Full branch table | Visible | Visible | Read-only | Read-only (chronic) | Own branch row only |
| Branch drill-down | Visible | Visible | Hidden | Read-only | Own branch only |
| Chronic Absentee list | Visible | Visible | Hidden | Visible | Hidden |
| Flag for Follow-up action | Visible | Visible | Hidden | Hidden | Hidden |
| Initiate SCN link | Visible | Hidden | Hidden | Visible | Hidden |
| Export button | Visible | Visible | Hidden | Hidden | Hidden |

---

## 12. API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/hr/attendance/summary/` | Branch-level attendance summary (paginated, filterable) |
| GET | `/api/hr/attendance/summary/{branch_id}/` | Individual staff attendance for a branch |
| GET | `/api/hr/attendance/chronic-absentees/` | List of chronic absentees across group |
| GET | `/api/hr/attendance/kpis/` | KPI summary bar data |
| POST | `/api/hr/attendance/flags/` | Create follow-up flag for branch |
| GET | `/api/hr/attendance/charts/by-branch/` | Bar chart data for attendance rate by branch |
| GET | `/api/hr/attendance/charts/trend/` | Monthly trend line data |
| GET | `/api/hr/attendance/export/` | Generate branch summary report (CSV/PDF) |

All endpoints accept `month` (YYYY-MM) and `branch` filter params.

---

## 13. HTMX Patterns

| Interaction | HTMX Attribute | Behaviour |
|---|---|---|
| Page load | `hx-get` on `#table-body` on render | Fetches current month's branch summary |
| Month selector change | `hx-get` + `hx-trigger="change"` on month picker | Re-fetches table, KPIs, and charts for selected month |
| Filter change | `hx-get` + `hx-include` on filter form | Re-fetches filtered table |
| Pagination | `hx-get` on page buttons | Fetches specified page of branches |
| Branch drill-down | `hx-get` + `hx-target="#drawer"` | Loads per-branch individual attendance in drawer |
| Flag form submit | `hx-post` + `hx-target="#flag-status"` | Submits flag, shows inline confirmation |
| Chart load | `hx-get` on `#chart-{n}` independently | Asynchronous chart data fetch |
| Month change — charts | `hx-trigger="custom-event"` on chart panels | Re-fetches charts when month changes via dispatched JS event |
| Toast | `hx-swap-oob` on `#toast-container` | Out-of-band toast on flag sent or export ready |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
