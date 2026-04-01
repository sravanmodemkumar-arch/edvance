# 13 — Academic MIS Officer Dashboard

> **URL:** `/group/acad/mis/`
> **File:** `13-mis-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Group Academic MIS Officer (G1 — READ ONLY) — exclusive landing page

---

## 1. Purpose

Primary post-login landing for the Group Academic MIS Officer. This role has read-only access across the academic division. There are no write controls, approval actions, or data entry interfaces on this page. The MIS Officer's function is data aggregation, report generation, and monitoring — providing the academic leadership team with accurate, timely, and downloadable MIS reports.

The dashboard is intentionally data-dense. The MIS Officer is a trained data worker who accesses this dashboard primarily to generate reports, monitor trend data across terms, and schedule auto-report delivery. They do not make decisions — they provide the data that decision-makers act on. Every section on this page is view-only or download-only.

The MIS Officer role exists across both large and small groups. For small groups, the function may be handled part-time by an admin staff member with a G1 access token. The dashboard is designed to be useful at any group scale — even when some subjects or branches have sparse data, the MIS summaries degrade gracefully with "No data" cells rather than breaking.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Academic MIS Officer | G1 | READ ONLY — full dashboard, no write controls anywhere | This is their exclusive dashboard |
| Chief Academic Officer (CAO) | G4 | Full read — can access this page as an additional view | CAO reviews MIS data |
| Group Academic Director | G3 | Full read — can access this page | Academic oversight |
| Group Curriculum Coordinator | G2 | — | Has own dashboard; no access here |
| Group Exam Controller | G3 | — | No access |
| Group Results Coordinator | G3 | — | No access |
| All Stream Coordinators | G3 | — | No access |
| Group JEE/NEET Integration Head | G3 | — | No access |
| Group IIT Foundation Director | G3 | — | No access |
| Group Olympiad & Scholarship Coord | G3 | — | No access |
| Group Special Education Coordinator | G3 | — | No access (MIS accesses special-ed data via aggregate reports only) |
| Group Academic Calendar Manager | G3 | — | No access |

> **Access enforcement:** Django view decorator `@require_role('academic_mis')`. No other role is admitted to this URL except CAO and Academic Director via role-union override. The MIS Officer role has no write permission in any API endpoint — all POST/PATCH/DELETE calls return `HTTP 403 Forbidden` for G1 tokens.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Academic Leadership  ›  Academic MIS  ›  MIS Officer Dashboard
```

### 3.2 Page Header
```
Welcome back, [MIS Officer Name]                          [Download Full MIS Report ↓]  [Settings ⚙]
Group Academic MIS Officer  ·  Last login: [date time]  ·  [Group Logo]
```

**Read-only notice strip (below header, always visible):**
> `ℹ This is a read-only dashboard. Data is for reporting and monitoring purposes. No changes can be made from this page.`
> Background: `bg-grey-50 border-l-4 border-grey-400` · Non-dismissible.

### 3.3 Alert Banner (conditional — informational alerts only)
- Collapsible panel above KPI row
- Background: `bg-yellow-50 border-l-4 border-yellow-400` for Warning — no Critical alerts for G1
- Each alert: icon + message — no [Take Action →] link (read-only role cannot act)
- "Dismiss" per alert (session-stored)
- Maximum 3 alerts shown

**Alert trigger examples (informational only):**
- Auto-report scheduled for today has failed to generate — [Contact system admin]
- Branch MIS data not received for > 7 days from [Branch Name] — data may be stale
- Academic year end approaching — annual MIS archive due in [N] days

---

## 4. KPI Summary Bar

| Card | Metric | Source | Colour Rule | Drill-down |
|---|---|---|---|---|
| Avg Group Attendance | `XX%` across all branches this month | Attendance aggregation | Green ≥ 85% · Yellow 75–85% · Red < 75% | → Section 5.1 Monthly MIS Summary |
| Avg Result (Group) | Group-wide average marks percentage across all streams and branches this term | Results aggregation | Green ≥ 65% · Yellow 50–65% · Red < 50% | → Section 5.2 Subject-wise Performance |
| Dropout Count | Total student dropouts this academic year | Enrollment module | Green = 0 · Yellow 1–10 · Red > 10 | → Section 5.2 (dropout row filter) |
| Teacher Absenteeism | Group avg teacher absence rate this month | HR aggregation | Green < 3% · Yellow 3–8% · Red > 8% | → Section 5.4 Teacher Performance |
| Scheduled Auto-Reports | Count of reports scheduled for auto-generation this week | Report scheduler | Green = on schedule · Yellow = 1 failed · Red ≥ 2 failed | → Section 5.5 Report Scheduler |
| Data Freshness | Branches with MIS data updated in last 48 hrs / total branches | Sync module | Green ≥ 90% fresh · Yellow 70–90% · Red < 70% | → Section 5.1 (stale data flag) |

**HTMX:** Cards auto-refresh every 5 minutes via `hx-trigger="every 5m"` `hx-get="/api/v1/group/{group_id}/acad/mis/kpi-cards/"` `hx-swap="innerHTML"` targeting `#kpi-bar`.

---

## 5. Sections

### 5.1 Monthly MIS Summary

> Key academic performance indicators for the current month — read-only stat cards and trend indicators.

**Display:** Stat card grid (2 rows × 3 columns)

**Stat cards:**
1. Average Attendance % — group-wide this month · Delta from last month (↑/↓) · Trend sparkline (last 6 months)
2. Average Result % — most recent term result · Delta from previous term
3. Dropout Count — this academic year · By stream breakdown (MPC/BiPC/MEC-CEC/Foundation) — click to filter Section 5.2 table
4. Teacher Absenteeism Rate — this month · Top 5 branches with highest absenteeism (tooltip)
5. Lesson Plan Submission Rate — % branches submitted all lesson plans for this month
6. Data Completeness — % of branches with complete MIS data for the current month

**Stale data flag:** Each stat card shows a `[Data last updated: DD-MMM-YYYY HH:MM]` timestamp. If data > 48 hrs old, timestamp text turns amber with a warning icon.

**No write controls anywhere on this card grid.**

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/mis/monthly-summary/"` · `hx-trigger="load"` · `hx-target="#monthly-summary-section"`.

---

### 5.2 Subject-wise Performance Table

> Full sortable table — all subjects × all branches — average marks, pass percentage, and rank.

**Display:** Sortable, filterable table — data-dense, no action columns.

**Columns:**

| Column | Sortable | Notes |
|---|---|---|
| Subject | ✅ | Subject name |
| Stream | ✅ | MPC / BiPC / MEC / CEC / HEC / Foundation |
| Class | ✅ | Standard (e.g., Class XI, XII, 6–10) |
| Branch | ✅ | Branch name |
| Avg Marks % | ✅ | Colour-coded: green ≥ 65% · amber 50–65% · red < 50% |
| Pass % | ✅ | % of students who passed |
| Fail Count | ✅ | Number of students who failed |
| Rank (Group) | ✅ | Rank among all branches for this subject |
| Term | ✅ | Which term these results are from |
| Last Updated | ✅ | Data upload timestamp |

**Filters:** Stream · Subject · Class · Branch · Term · Pass % band (< 50% / 50–65% / ≥ 65%) · Show only failing subjects (toggle)

**Search:** Subject name, branch name — 300ms debounce.

**Pagination:** Server-side · Default 25 rows/page · Selector 10 / 25 / 50 / 100 · "Showing X–Y of Z records" · Page jump input.

**Export (read-only, download only):**
- [Export as XLSX] → downloads current filtered view
- [Export as PDF] → generates formatted table PDF

**Column visibility toggle:** Gear icon top-right of table — show/hide columns.

**No row actions — no edit, no approve, no delete.**

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/mis/subject-performance/"` · search/filter/sort triggers `hx-get` with params · `hx-target="#subject-performance-section"` · pagination triggers fresh `hx-get`.

---

### 5.3 Branch-wise MIS Report Downloads

> Quick-download links for branch-level MIS reports in PDF and XLSX format.

**Display:** Table (one row per branch)

**Columns:**

| Column | Sortable | Notes |
|---|---|---|
| Branch Name | ✅ | |
| City | ✅ | |
| Last Report Generated | ✅ | Timestamp |
| Report Month | ✅ | Which month the report covers |
| Status | ✅ | Ready · Generating · Failed · Scheduled |
| Download PDF | ❌ | [↓ PDF] — opens download (no preview) |
| Download XLSX | ❌ | [↓ XLSX] — opens download |
| Request Fresh Report | ❌ | [Regenerate] — POST to regenerate; G1 CAN trigger report regeneration (this is the only write-like action, but it is a report job, not a data edit) |

**Filters:** Branch · Report month · Status (Ready / Generating / Failed)

**[Download Full Group MIS ↓] button** (matches page header button): Downloads a consolidated group-level MIS report across all branches in XLSX format.

**Note on regenerate:** The [Regenerate] button is the only action available on this page. It submits a report generation job to the background task queue. It does not modify any academic data. The MIS Officer may trigger this when branch data is stale or a report failed.

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/mis/branch-reports/"` · filter triggers `hx-get` · `hx-target="#branch-reports-section"` · [Regenerate] `hx-post="/api/v1/group/{group_id}/acad/mis/branch-reports/{branch_id}/regenerate/"` · `hx-swap="none"` (toast only).

---

### 5.4 Teacher Performance by Branch

> Average teacher rating per branch — group comparison.

**Display:** Bar chart (Chart.js 4.x) + sortable table toggle.

**Bar chart:**
- X-axis: Branches (sorted by avg rating ascending — lowest performers first)
- Y-axis: Average teacher performance rating (1–5)
- Colour: Red < 3.0 · Amber 3.0–3.5 · Green > 3.5
- Reference line: Group average rating (dashed grey)

**Tooltip:** Branch name · Avg teacher rating · Number of teachers rated · % rated below 3.0

**Table toggle (same data):**

| Column | Sortable |
|---|---|
| Branch | ✅ |
| Avg Teacher Rating | ✅ |
| Teachers Rated | ✅ |
| Teachers Below 3.0 | ✅ |
| Last Rating Period | ✅ |

**Filter:** Branch · Rating band · Stream filter (to see teacher ratings within a specific stream)

**Export:** [Export XLSX] for current view.

**No action columns — read-only.**

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/mis/teacher-performance/"` · filter/view-toggle triggers `hx-get` · `hx-target="#teacher-performance-section"`.

---

### 5.5 Trend Chart — Last 6 Terms

> Multi-line chart showing attendance, average marks, and dropout rate across the last 6 academic terms.

**Display:** Multi-line chart (Chart.js 4.x)

**X-axis:** Last 6 terms (Term 1 2023–24 → Term 2 2025–26; current term highlighted)

**Y-axis (left):** Percentage (0–100%) — for attendance and avg marks

**Y-axis (right):** Count (0–[max]) — for dropout count

**Series:**
- Avg Attendance % — Blue solid line
- Avg Result % — Green solid line
- Dropout Count — Red dashed line (right Y-axis)
- Teacher Absenteeism % — Orange dashed line

**Tooltip:** Term · Attendance · Avg marks · Dropout count · Teacher absenteeism

**Legend:** Bottom horizontal. Colorblind-safe palette. Toggle series visibility by clicking legend items.

**Filters within chart card:** Branch filter (group-wide vs individual branch) · Stream filter · Year range selector.

**Export:** "Export PNG" and "Export XLSX (data)" buttons.

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/mis/trend/"` · filter changes trigger `hx-get` with params · `hx-target="#trend-chart-section"` · `hx-swap="innerHTML"`.

---

### 5.6 Report Scheduler

> Upcoming scheduled auto-reports — shows what will be generated automatically and when.

**Display:** Table (upcoming list, sorted by next-run time)

**Columns:**

| Column | Sortable | Notes |
|---|---|---|
| Report Name | ✅ | e.g., "Monthly MIS Summary — All Branches" |
| Frequency | ✅ | Weekly · Monthly · Term-end · Annual |
| Next Run | ✅ | Next scheduled generation date + time |
| Last Run | ✅ | Last successful generation timestamp |
| Delivery | ✅ | Email · Portal download · Both |
| Recipients | ✅ | Role names (not individual names) |
| Status | ✅ | Scheduled · Failed · Paused |
| Actions | ❌ | [Download Last Report ↓] · [Run Now] |

**[Run Now]:** POST to trigger immediate report generation job. Same principle as [Regenerate] — submits a background job, does not modify academic data.

**[Download Last Report ↓]:** Downloads the last successfully generated report file.

**No create/edit/delete controls — the MIS Officer cannot modify report schedules.** Schedule configuration is done by CAO/Academic Director in a separate admin section.

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/mis/report-scheduler/"` · `hx-trigger="load"` · `hx-target="#scheduler-section"` · [Run Now] `hx-post="/api/v1/group/{group_id}/acad/mis/reports/{report_id}/run/"` → toast only.

---

## 6. Drawers & Modals

There are minimal drawers on this page — it is a read-only dashboard. No approval drawers, edit drawers, or action modals exist.

### 6.1 Drawer: `subject-detail-view` (read-only)
- **Trigger:** Click on a subject row in Section 5.2 table
- **Width:** 560px
- **Content:** Subject name · Stream · Class · All branches' data for this subject — avg marks, pass %, fail count, rank, last updated
- **No action buttons — read-only view**
- **HTMX:** `hx-get="/api/v1/group/{group_id}/acad/mis/subject-performance/{subject_id}/?class={class}&stream={stream}"` `hx-target="#drawer-body"` `hx-swap="innerHTML"`

### 6.2 Drawer: `branch-report-preview` (read-only)
- **Trigger:** Not a standard drawer — reports open as file downloads directly. No preview drawer on this page.
- **Note:** PDF/XLSX are downloaded to local filesystem. No in-browser preview to avoid DPDP data display risk.

### 6.3 Modal: `run-report-confirm`
- **Trigger:** [Run Now] in Section 5.6 report scheduler
- **Width:** 400px
- **Content:** "Run '[Report Name]' now? This will generate the report immediately and deliver it to scheduled recipients." + [Confirm] [Cancel]
- **On confirm:** `hx-post="/api/v1/group/{group_id}/acad/mis/reports/{report_id}/run/"` → toast "Report generation started"

### 6.4 Modal: `regenerate-branch-report-confirm`
- **Trigger:** [Regenerate] in Section 5.3 branch reports table
- **Width:** 400px
- **Content:** "Regenerate MIS report for [Branch Name]? The existing report will be replaced." + [Confirm] [Cancel]
- **On confirm:** `hx-post="/api/v1/group/{group_id}/acad/mis/branch-reports/{branch_id}/regenerate/"` → toast "Report generation queued"

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Full group MIS download started | "Group MIS report download started — check your downloads" | Info (blue) | 4s auto-dismiss |
| Branch report download started | "Branch MIS report for [Branch Name] downloading…" | Info | 4s |
| Report regeneration queued | "Report regeneration queued for [Branch Name]. Ready in a few minutes." | Info | 5s |
| Report run (scheduler) started | "[Report Name] generation started. You will receive it via [Email/Portal]." | Info | 5s |
| Report generation failed | "Report generation failed for [Report Name]. Contact system admin." | Error (red) | Manual dismiss |
| KPI load error | "Failed to load KPI data. Retrying…" | Error (red) | Manual dismiss |
| Stale data warning | "Some branch data is older than 48 hours. Reports may not reflect latest data." | Warning (yellow) | 6s |

---

## 8. Empty States

| Condition | Illustration | Heading | Description | CTA |
|---|---|---|---|---|
| No subject performance data | Bar chart outline | "No performance data available" | "No exam results have been uploaded for the selected term and filters" | [Clear Filters] |
| No branches in report list | Building outline | "No branch reports found" | "No branch MIS reports match the selected filters" | [Clear Filters] |
| No scheduled reports | Calendar outline | "No auto-reports scheduled" | "No automatic reports are currently configured. Contact your CAO to set up report schedules." | — |
| No teacher performance data | Person outline | "No teacher ratings recorded" | "No teacher performance ratings have been submitted for the selected period" | — |
| No trend data | Line chart outline | "No trend data available" | "Trend data requires at least 2 terms of results to display" | — |
| KPI stale (all failed) | Refresh icon | "Data unavailable" | "Unable to load dashboard data. Please refresh the page." | [Refresh Page] |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton screens: KPI bar (6 cards) + monthly summary cards (6) + subject table (5 skeleton rows) |
| Subject performance table load | Skeleton rows — 10 rows, same column widths as table |
| Subject table filter/search/sort | Inline skeleton rows — 5 rows |
| Branch report table load | Skeleton rows — 5 rows |
| Teacher performance chart load | Spinner centred in chart area |
| Trend chart load | Spinner centred in chart area |
| Report scheduler table load | Skeleton rows — 5 rows |
| Subject detail drawer open | Skeleton rows inside drawer body |
| KPI auto-refresh | Subtle shimmer over existing card values |
| [Run Now] / [Regenerate] button click | Spinner inside button + button disabled for 2s then re-enabled |

---

## 10. Role-Based UI Visibility

| Element | MIS Officer (G1) | CAO (G4) | Academic Director (G3) | All others |
|---|---|---|---|---|
| Page itself | ✅ Rendered (full read-only) | ✅ Rendered | ✅ Rendered | ❌ Redirected |
| Read-only notice strip | ✅ Shown | ❌ Not shown (they have write access elsewhere) | ❌ Not shown | N/A |
| [Export XLSX] / [Export PDF] | ✅ Shown | ✅ Shown | ✅ Shown | N/A |
| [Download Full MIS Report ↓] header | ✅ Shown | ✅ Shown | ✅ Shown | N/A |
| [Regenerate] branch report | ✅ Shown (report job only) | ✅ Shown | ✅ Shown | N/A |
| [Run Now] report scheduler | ✅ Shown (report job only) | ✅ Shown | ✅ Shown | N/A |
| Any POST that modifies academic data | ❌ Never shown; 403 if attempted | ✅ (via own dashboards) | ✅ (via own dashboards) | N/A |
| Subject detail drawer | ✅ Read-only view | ✅ Read-only view | ✅ Read-only view | N/A |
| Student-level data (special-ed cross-ref) | ❌ Aggregate counts only; no individual identifiers | ✅ Full (via special-ed dashboard) | ✅ Full (via special-ed dashboard) | N/A |

> All UI visibility decisions made server-side in Django template. No client-side JS role checks. The MIS Officer G1 token is JWT-scoped to read-only academic endpoints only — write endpoints return 403 at the API layer regardless of UI visibility.

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/acad/mis/dashboard/` | JWT (G1+) | Full page data |
| GET | `/api/v1/group/{group_id}/acad/mis/kpi-cards/` | JWT (G1+) | KPI card values only (auto-refresh) |
| GET | `/api/v1/group/{group_id}/acad/mis/monthly-summary/` | JWT (G1+) | Monthly MIS stat cards |
| GET | `/api/v1/group/{group_id}/acad/mis/subject-performance/` | JWT (G1+) | Subject × branch performance table with filters/sort/pagination |
| GET | `/api/v1/group/{group_id}/acad/mis/subject-performance/{subject_id}/` | JWT (G1+) | Subject detail for drawer |
| GET | `/api/v1/group/{group_id}/acad/mis/subject-performance/export/` | JWT (G1+) | Export current filtered view as XLSX |
| GET | `/api/v1/group/{group_id}/acad/mis/branch-reports/` | JWT (G1+) | Branch MIS report list |
| GET | `/api/v1/group/{group_id}/acad/mis/branch-reports/{branch_id}/download/?format=pdf` | JWT (G1+) | Download branch PDF report |
| GET | `/api/v1/group/{group_id}/acad/mis/branch-reports/{branch_id}/download/?format=xlsx` | JWT (G1+) | Download branch XLSX report |
| POST | `/api/v1/group/{group_id}/acad/mis/branch-reports/{branch_id}/regenerate/` | JWT (G1+) | Queue report regeneration job (report job only — no data edit) |
| GET | `/api/v1/group/{group_id}/acad/mis/group-report/download/` | JWT (G1+) | Download full group MIS XLSX |
| GET | `/api/v1/group/{group_id}/acad/mis/teacher-performance/` | JWT (G1+) | Teacher performance chart + table data |
| GET | `/api/v1/group/{group_id}/acad/mis/teacher-performance/export/` | JWT (G1+) | Export teacher performance XLSX |
| GET | `/api/v1/group/{group_id}/acad/mis/trend/` | JWT (G1+) | 6-term trend chart data |
| GET | `/api/v1/group/{group_id}/acad/mis/trend/export/` | JWT (G1+) | Export trend data XLSX |
| GET | `/api/v1/group/{group_id}/acad/mis/report-scheduler/` | JWT (G1+) | Scheduled report list |
| POST | `/api/v1/group/{group_id}/acad/mis/reports/{report_id}/run/` | JWT (G1+) | Trigger immediate report generation job |
| GET | `/api/v1/group/{group_id}/acad/mis/reports/{report_id}/download/` | JWT (G1+) | Download last generated report file |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| KPI auto-refresh | `every 5m` | GET `/api/.../mis/kpi-cards/` | `#kpi-bar` | `innerHTML` |
| Monthly summary load | `load` | GET `/api/.../mis/monthly-summary/` | `#monthly-summary-section` | `innerHTML` |
| Subject table search | `input delay:300ms` | GET `/api/.../mis/subject-performance/?q={val}&…` | `#subject-performance-section` | `innerHTML` |
| Subject table filter change | `change` | GET `/api/.../mis/subject-performance/?stream={}&subject={}&branch={}&term={}` | `#subject-performance-section` | `innerHTML` |
| Subject table sort click | `click` | GET `/api/.../mis/subject-performance/?sort={col}&dir={asc|desc}` | `#subject-performance-section` | `innerHTML` |
| Subject table pagination | `click` | GET `/api/.../mis/subject-performance/?page={n}` | `#subject-performance-section` | `innerHTML` |
| Subject row click (drawer) | `click` | GET `/api/.../mis/subject-performance/{id}/` | `#drawer-body` | `innerHTML` |
| Branch reports filter | `change` | GET `/api/.../mis/branch-reports/?branch={}&month={}&status={}` | `#branch-reports-section` | `innerHTML` |
| Regenerate confirm | `click` | POST `/api/.../mis/branch-reports/{id}/regenerate/` | `#toast-container` | `afterbegin` |
| Teacher perf filter / view toggle | `change` / `click` | GET `/api/.../mis/teacher-performance/?branch={}&view={chart|table}` | `#teacher-performance-section` | `innerHTML` |
| Trend chart filter | `change` | GET `/api/.../mis/trend/?branch={}&stream={}&years={}` | `#trend-chart-section` | `innerHTML` |
| Scheduler load | `load` | GET `/api/.../mis/report-scheduler/` | `#scheduler-section` | `innerHTML` |
| Run report now confirm | `click` | POST `/api/.../mis/reports/{id}/run/` | `#toast-container` | `afterbegin` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
