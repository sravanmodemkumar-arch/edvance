# 102 — Analytics Director Dashboard

> **URL:** `/group/analytics/director/`
> **File:** `01-analytics-director-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Role:** Analytics Director (Role 102, G1) — exclusive post-login landing

---

## 1. Purpose

The Analytics Director Dashboard is the command centre for the Group Analytics Director (Role 102), providing a unified view of cross-branch performance intelligence across all branches in the group. It surfaces data quality alerts, tracks pending analytics outputs (reports due, active feasibility studies), and gives a real-time composite health score for every branch. This dashboard enables the Analytics Director to supervise all six Division M roles, identify anomalies before they escalate, and deliver timely intelligence to the Chairman, Board, CEO, and CFO. At group scale (5–50 branches, 20,000–1,00,000 students), this page is the single source of truth for analytics governance.

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Analytics Director | 102 | G1 | Full Read + Manage Div-M outputs | Exclusive landing page; can create/edit/delete analytics outputs |
| All other Division M roles | 103–107 | G1 | No access to this URL | Redirect to own dashboard |
| All other roles | Any | G1/G2/G3 | No access | 403 Forbidden |

Access enforcement: `@role_required(102)` Django decorator on the view. Session verified on every request. Non-102 roles receive HTTP 403 with redirect to their own landing page.

---

## 3. Page Layout

### 3.1 Breadcrumb

```
Group Home > Analytics & MIS > Analytics Director Dashboard
```

### 3.2 Page Header

**Title:** `Analytics Director Dashboard`
**Sub-title:** `[Group Name] · Academic Year: [current AY selector]`

Action buttons (right-aligned):

| Button | Icon | Behaviour | Visible To |
|---|---|---|---|
| Export Summary | download | Opens export modal (PDF/XLSX) | Role 102 |
| Refresh Data | refresh | HTMX re-poll all KPIs + tables | Role 102 |
| Settings | gear | Opens Div-M settings drawer | Role 102 |

AY Selector: `<select>` dropdown pre-set to current AY (e.g., 2025-26), listing last 5 AYs. On change, triggers full page HTMX reload via `hx-get="/group/analytics/director/?ay=2025-26"`.

### 3.3 Alert Banners

Rendered above KPI bar, individually dismissible per session via `sessionStorage`. Each banner has a close (×) button.

| Condition | Banner Text | Severity |
|---|---|---|
| Any branch has data completeness < 60% | "⚠ Data quality critical: [N] branch(es) have less than 60% data completeness. Reports may be unreliable." | Warning (amber) |
| MIS report overdue by > 3 days | "🔴 [N] MIS report(s) are overdue. Immediate action required by MIS Officer." | Error (red) |
| Export job stuck > 30 min | "Export job [ID] has been running for over 30 minutes. Check export queue." | Warning (amber) |
| No branches reported data in last 48 h | "No branch has submitted data in the last 48 hours. Check data pipeline." | Error (red) |
| Active feasibility studies with deadline today | "[N] feasibility study/studies are due today." | Info (blue) |
| All data complete, no overdue reports | "All systems nominal. Data completeness ≥ 90% across all branches." | Success (green, auto-dismiss 6s) |

---

## 4. KPI Summary Bar

HTMX auto-refresh: every 120 seconds via `hx-trigger="every 120s"` on the KPI container. Spinner shown in KPI card header during refresh.

| Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|
| Total Branches Reporting | Count of branches that submitted data in current month | COUNT(branch_submissions WHERE month = current_month AND ay = current_ay) | Green ≥ 90% of total; Amber 70–89%; Red < 70% | `#kpi-branches-reporting` |
| Data Completeness Score | Avg % of required fields filled across all branches, current month | AVG(branch_data_completeness_pct) | Green ≥ 90%; Amber 75–89%; Red < 75% | `#kpi-data-completeness` |
| Branches Below Benchmark | Branches with composite health score < 60 | COUNT(branches WHERE composite_score < 60) | Green = 0; Amber 1–3; Red ≥ 4 | `#kpi-below-benchmark` |
| MIS Reports Due This Month | Reports scheduled but not yet generated, current calendar month | COUNT(mis_report_schedule WHERE due_month = current AND status != 'generated') | Green = 0; Amber 1–2; Red ≥ 3 | `#kpi-mis-due` |
| Active Feasibility Studies | Open feasibility studies (status = 'in_progress' or 'review') | COUNT(feasibility_studies WHERE status IN ('in_progress','review')) | Neutral (blue always) | `#kpi-feasibility` |
| Cross-Branch Alerts | Data anomalies flagged by system in last 7 days, not dismissed | COUNT(data_alerts WHERE flagged_at ≥ NOW()-7d AND dismissed = false) | Green = 0; Amber 1–4; Red ≥ 5 | `#kpi-alerts` |
| Export Jobs Pending | Export jobs in queue or processing state | COUNT(export_jobs WHERE status IN ('queued','processing')) | Green = 0; Amber 1–2; Red ≥ 3 | `#kpi-export-pending` |

---

## 5. Sections

### 5.1 Cross-Branch Performance Snapshot

**Purpose:** Shows every branch in the group with its key composite metrics for the selected AY, enabling the Analytics Director to spot underperformers at a glance.

**Search bar:** Full-text search on Branch Name and Branch Code. Debounced 300 ms. Input placeholder: "Search branch name or code…". Match highlighted in yellow.

**Inline filter chips (above table):**
- Region/Zone (multi-select)
- Performance Band: All | Excellent (≥ 80) | Good (60–79) | Needs Attention (40–59) | Critical (< 40)
- Data Completeness: All | Complete (≥ 90%) | Partial (60–89%) | Incomplete (< 60%)
- Branch Type: All | Day School | Residential | Semi-Residential

Active filters shown as dismissible chips. "Clear All" button when any filter active. Filter count badge on "Filters" button.

**Table columns:**

| Column | Source Field | Sortable | Notes |
|---|---|---|---|
| # | Row index | No | 1-based |
| Branch Name | `branch.name` | Yes | Clickable — opens Branch Detail drawer |
| Branch Code | `branch.code` | Yes | Monospace font |
| Region/Zone | `branch.zone` | Yes | Text badge |
| Enrollment % | `branch_stats.enrollment_pct` | Yes | Filled seats / sanctioned seats × 100. Colour: ≥ 90% green, 70–89% amber, < 70% red |
| Fee Collection % | `branch_stats.fee_collection_pct` | Yes | Collected / billed × 100. Colour: ≥ 90% green, 70–89% amber, < 70% red |
| Avg Score | `branch_stats.avg_exam_score` | Yes | Mean score across all exams, current AY. Colour: ≥ 70 green, 50–69 amber, < 50 red |
| Attendance % | `branch_stats.avg_attendance_pct` | Yes | Group avg attendance. Colour: ≥ 85% green, 75–84% amber, < 75% red |
| Composite Score | `branch_stats.composite_score` | Yes | Weighted formula: (enrollment 25% + fee 25% + score 25% + attendance 25%). 0–100 scale. Colour bar |
| Data Completeness | `branch_stats.data_completeness_pct` | Yes | % of required data fields submitted. Colour coded |
| Last Submission | `branch_stats.last_submission_at` | Yes | Relative time (e.g., "2 days ago"). Red if > 7 days |
| Actions | — | No | View button → Branch Detail drawer |

**Default sort:** Composite Score ascending (lowest first — worst performers at top).

**Pagination:** Server-side, default 25/page. Selector: 10/25/50/All. "Showing X–Y of Z branches". Page jump input.

**Checkbox row select + select-all:** Bulk action: "Export Selected" (XLSX/PDF).

**Responsive:** Card layout on mobile (< 768px), showing Branch Name, Composite Score, and Data Completeness only; tap to expand.

**Column visibility toggle:** Button top-right of table card.

---

### 5.2 Data Quality Alerts

**Purpose:** Lists branches where data is missing, stale, or inconsistent, enabling targeted follow-up.

**Search bar:** Search by Branch Name, Alert Type. Debounced 300 ms.

**Inline filter chips:**
- Alert Type: All | Missing Data | Stale Data (> 48 h) | Inconsistent Data | Duplicate Entry
- Severity: All | Critical | High | Medium | Low
- Status: All | Open | Acknowledged | Resolved

**Table columns:**

| Column | Source Field | Sortable | Notes |
|---|---|---|---|
| # | Row index | No | |
| Branch Name | `data_alert.branch_name` | Yes | Link to Branch Detail drawer |
| Alert Type | `data_alert.alert_type` | Yes | Colour-coded badge |
| Affected Module | `data_alert.module` | Yes | e.g., Attendance, Fee, Exam Results |
| Description | `data_alert.description` | No | Truncated at 80 chars; expand on hover |
| Severity | `data_alert.severity` | Yes | Critical (red) / High (orange) / Medium (amber) / Low (blue) |
| Flagged At | `data_alert.flagged_at` | Yes | Datetime, relative |
| Status | `data_alert.status` | Yes | Open / Acknowledged / Resolved badge |
| Assigned To | `data_alert.assigned_role_name` | Yes | Div-M role responsible |
| Actions | — | No | Acknowledge / Resolve / View Detail |

**Default sort:** Severity (Critical first), then Flagged At descending.

**Pagination:** Server-side, 25/page.

**Empty state:** No alerts table row → See Section 9.

---

### 5.3 Analytics Team Activity

**Purpose:** Shows recent actions by all Division M team members (Roles 102–107) — reports generated, feasibility studies updated, export jobs completed — giving the Analytics Director oversight of team productivity.

**Search bar:** Search by team member name, action type, output title. Debounced 300 ms.

**Inline filter chips:**
- Role: All | MIS Officer (103) | Academic Analyst (104) | Exam Analytics (105) | Hostel Analytics (106) | Strategy Officer (107)
- Action Type: All | Report Generated | Feasibility Updated | Export Completed | Alert Resolved
- Date Range: Today | This Week | This Month | Custom

**Table columns:**

| Column | Source Field | Sortable | Notes |
|---|---|---|---|
| # | Row index | No | |
| Team Member | `activity_log.user_full_name` | Yes | Name + role badge |
| Role | `activity_log.role_id` | Yes | Badge: 103/104/105/106/107 |
| Action | `activity_log.action_type` | Yes | Colour-coded badge |
| Output / Item | `activity_log.item_title` | Yes | Truncated 60 chars; click → detail |
| Branches Covered | `activity_log.branch_count` | Yes | Count; hover shows list |
| Timestamp | `activity_log.created_at` | Yes | Datetime, relative |
| Status | `activity_log.status` | Yes | Completed / In Progress / Failed badge |

**Default sort:** Timestamp descending.

**Pagination:** Server-side, 25/page.

---

### 5.4 Quick Navigation Tiles

**Purpose:** Provides one-click access to all Division M pages (for the Analytics Director to navigate to any analytics tool).

Layout: 4-column grid (desktop), 2-column (tablet), 1-column (mobile). Each tile is a card with icon, label, and short description.

| Tile Label | URL | Icon |
|---|---|---|
| MIS Officer Dashboard | `/group/mis/officer/` | chart-bar |
| Academic Analyst Dashboard | `/group/analytics/academic/` | academic-cap |
| Exam Analytics Dashboard | `/group/analytics/exam/` | clipboard-check |
| Hostel Analytics Dashboard | `/group/analytics/hostel/` | home |
| Strategic Planning Dashboard | `/group/analytics/strategy/` | map |
| Generate MIS Report | `/group/mis/reports/generate/` | document-add |
| Report Archive | `/group/mis/reports/archive/` | archive |
| Feasibility Studies | `/group/analytics/feasibility/` | light-bulb |
| Export Centre | `/group/analytics/exports/` | download |
| Data Quality Monitor | `/group/analytics/data-quality/` | shield-check |
| Attendance Analytics | `/group/analytics/attendance/` | user-check |
| Fee Analytics | `/group/analytics/fees/` | currency-rupee |
| Exam Results Deep Dive | `/group/analytics/exam/deep-dive/` | magnify |
| Teacher Performance | `/group/analytics/teachers/` | user-group |
| Hostel Welfare | `/group/analytics/hostel/welfare/` | heart |
| Dropout Risk Engine | `/group/analytics/dropout-risk/` | exclamation |
| Branch Benchmarking | `/group/analytics/benchmarking/` | chart-bar |
| Rank Analytics | `/group/analytics/ranks/` | trophy |
| Topic Gap Analysis | `/group/analytics/topic-gaps/` | book-open |
| 3-Year Expansion Plan | `/group/analytics/expansion-plan/` | map-marker |
| Market Opportunity Map | `/group/analytics/market/` | globe |
| Scheduled Reports | `/group/mis/reports/scheduled/` | clock |
| Distribution Log | `/group/mis/distribution/log/` | mail |
| Div-M Settings | `/group/analytics/settings/` | cog |

---

## 6. Drawers & Modals

### 6.1 Branch Detail Drawer

Triggered by: Clicking any branch name in Section 5.1.
Width: 600px. Slide in from right. Backdrop click closes (with unsaved-changes guard). ESC closes.

**Tabs:**

**Tab 1 — Overview**

| Field | Value |
|---|---|
| Branch Name | Full name + code |
| Region/Zone | Text |
| Branch Type | Day / Residential / Semi-Residential |
| Principal Name | Text |
| Total Enrolment | Number |
| Sanctioned Seats | Number |
| Enrollment % | Calculated |
| Last Data Submission | Datetime |
| Data Completeness | % with progress bar |
| Composite Health Score | Gauge 0–100 |

**Tab 2 — Performance Metrics**

Mini table: Metric | This Month | Last Month | Change (↑↓%)
Rows: Enrollment %, Fee Collection %, Avg Exam Score, Avg Attendance %, Dropout Rate

**Tab 3 — Active Alerts**

List of open data quality alerts for this branch. Each row: Alert Type, Severity badge, Flagged At, Status.
"Acknowledge All" button (Role 102 only).

**Tab 4 — Recent Reports**

Last 5 reports generated for/by this branch. Table: Report Title, Generated By, Date, Download link.

**Footer actions:**
- "View Full Branch Report" (opens new tab)
- "Flag for Review" (sets branch status = 'flagged'; toast on success)
- "Close" button

---

### 6.2 Export Modal

Triggered by: "Export Summary" button in page header.
Size: 480px centred overlay.

**Fields:**

| Field | Type | Required | Validation |
|---|---|---|---|
| Export Format | Radio: PDF / XLSX | Yes | Default PDF |
| Include Sections | Checkbox group: KPI Bar, Cross-Branch Snapshot, Data Alerts, Team Activity | Yes | At least 1 |
| Academic Year | Select (pre-filled current AY) | Yes | Valid AY |
| Branch Scope | Radio: All Branches / Selected Branches (from table checkboxes) | Yes | |
| Report Title | Text input | No | Max 100 chars |
| Notes | Textarea | No | Max 500 chars; character counter |

**Footer buttons:** "Generate Export" (primary, disabled until valid) / "Cancel"

Form validation: inline on blur. Required fields marked *. Submit button disabled until all required fields valid.

---

### 6.3 Data Alert Detail Drawer

Triggered by: "View Detail" in Section 5.2.
Width: 480px.

| Field | Value |
|---|---|
| Alert ID | Monospace |
| Branch | Name + Code |
| Affected Module | Text |
| Alert Type | Badge |
| Description | Full text |
| Severity | Badge |
| Flagged At | Full datetime |
| System Detail | JSON snippet (collapsible) |
| Assigned To | Role name |
| Resolution Notes | Textarea (editable by Role 102, max 500 chars) |
| Status | Select: Open / Acknowledged / Resolved |

**Footer:** "Save Changes" / "Close"

---

## 7. Charts

### 7.1 Group Performance Index — Line Chart

| Property | Value |
|---|---|
| Type | Chart.js Line |
| Title | "Group Performance Index — Last 5 Academic Years" |
| Data | Composite group score per AY: weighted avg of (enrollment % + fee collection % + avg score + attendance %) across all branches |
| X-Axis | Academic Year labels: "2021-22", "2022-23", "2023-24", "2024-25", "2025-26" |
| Y-Axis | Score 0–100; label "Composite Score" |
| Colour | Single line — `#4F46E5` (Indigo), fill below with 20% opacity |
| Tooltip | "AY [X]: Score [Y] · Branches: [N] · Top Branch: [name]" |
| Data Points | Circular markers, 5px radius |
| API Endpoint | `GET /api/v1/analytics/group-performance-index/?ay_from=2021-22&ay_to=2025-26` |
| HTMX Pattern | Chart rendered on page load via JS fetch; no HTMX polling on this chart (historical data) |
| Export | PNG export button top-right of chart card |
| Colorblind-safe | Yes — single-line, uses label + shape differentiation |
| Empty State | "No historical data available. Data will appear once 2 or more academic years have been recorded." |

---

### 7.2 Branch Performance Distribution — Bar Chart (Histogram)

| Property | Value |
|---|---|
| Type | Chart.js Bar (histogram bins) |
| Title | "Branch Health Score Distribution — [Current AY]" |
| Data | Count of branches per score band: < 40, 40–49, 50–59, 60–69, 70–79, 80–89, ≥ 90 |
| X-Axis | Score bands as labels |
| Y-Axis | "Number of Branches" |
| Colours | Bins coloured: < 40 `#EF4444` (red), 40–59 `#F97316` (orange), 60–79 `#EAB308` (amber), ≥ 80 `#22C55E` (green) |
| Tooltip | "Score Band [X]: [N] branches. [List of branch names on hover — up to 5, then '+N more']" |
| API Endpoint | `GET /api/v1/analytics/branch-score-distribution/?ay=2025-26` |
| HTMX Pattern | `hx-get` on AY selector change, target `#chart-distribution-container`, swap `innerHTML` |
| Export | PNG export button top-right of chart card |
| Colorblind-safe | Yes — colour + pattern fill |
| Empty State | "No branch score data available for the selected academic year." |

---

## 8. Toast Messages

All toasts appear bottom-right. Max 3 stacked. Success auto-dismiss 4s. Error manual dismiss. Warning 6s. Info 4s.

| Action | Toast Text | Type |
|---|---|---|
| Page load success | "Dashboard loaded successfully." | Success |
| Page load error | "Failed to load dashboard data. Please refresh." | Error |
| KPI refresh success | "KPIs refreshed." | Success |
| KPI refresh error | "Could not refresh KPIs. Check network connection." | Error |
| Branch detail drawer open error | "Could not load branch details. Please try again." | Error |
| Alert acknowledged | "Alert acknowledged successfully." | Success |
| Alert acknowledge error | "Failed to acknowledge alert. Please try again." | Error |
| Alert resolved | "Alert marked as resolved." | Success |
| Alert resolve error | "Failed to resolve alert. Please try again." | Error |
| Export job queued | "Export job queued. You will be notified when it is ready." | Info |
| Export job failed | "Export job failed. Please try again or contact support." | Error |
| Branch flagged for review | "Branch flagged for review successfully." | Success |
| Branch flag error | "Failed to flag branch. Please try again." | Error |
| Alert detail saved | "Alert details saved." | Success |
| Alert detail save error | "Failed to save alert details." | Error |
| Filter cleared | "All filters cleared." | Info |
| AY changed | "Showing data for [AY]." | Info |

---

## 9. Empty States

| Context | Icon | Heading | Sub-text | Action |
|---|---|---|---|---|
| 5.1 Cross-Branch table — no branches reporting | chart-bar (grey) | "No Branch Data Available" | "No branches have submitted data for the selected academic year. Ask branches to complete their data submissions." | "Go to Data Quality Monitor" button |
| 5.1 Cross-Branch table — search/filter returns nothing | magnify (grey) | "No Branches Match" | "Try different search terms or clear the filters." | "Clear Filters" button |
| 5.2 Data Quality Alerts — no alerts | shield-check (green) | "No Data Quality Alerts" | "All branches are reporting clean data. Great work!" | None |
| 5.2 Alerts — search returns nothing | magnify | "No Matching Alerts" | "Adjust your search or filters to find alerts." | "Clear Filters" |
| 5.3 Team Activity — no activity yet | users (grey) | "No Team Activity Recorded" | "Division M team activity will appear here once reports and analyses are generated." | None |
| 5.3 Activity — filter returns nothing | magnify | "No Matching Activity" | "Try a different date range or role filter." | "Clear Filters" |
| 7.1 Group Performance Index chart — no data | chart-line (grey) | "Insufficient Historical Data" | "At least two academic years of data are needed to plot this chart." | None |
| 7.2 Branch Distribution chart — no data | chart-bar (grey) | "No Score Data" | "Branch health scores will appear once branch data is submitted for the selected year." | None |

---

## 10. Loader States

| Context | Loader Behaviour |
|---|---|
| Initial page load | Full-page skeleton: KPI bar shows 7 grey pulsing cards; each table shows 5 skeleton rows (grey bars); charts show grey placeholder rectangles |
| KPI auto-refresh (every 120s) | Spinner icon inside each KPI card header; card value fades to 60% opacity during refresh |
| Branch detail drawer opening | Drawer slides in with skeleton: 3 tab skeletons + 6 field skeletons in first tab |
| Cross-Branch table search/filter | Table body replaced with 5 skeleton rows during fetch; search input shows spinner at right |
| Data Alerts table filter | Same: 5 skeleton rows during fetch |
| Team Activity table filter | Same: 5 skeleton rows during fetch |
| Export job generating | Export button shows spinner + "Generating…" label; button disabled during processing |
| Alert resolve/acknowledge | Row action button shows spinner; row dims to 50% opacity |
| AY selector change | Full KPI bar + all three tables show skeleton simultaneously |
| Chart data loading | Chart canvas shows grey pulsing rectangle until data arrives |

---

## 11. Role-Based UI Visibility

| UI Element | Role 102 (Analytics Director) | Roles 103–107 (Other Div-M) | All Others |
|---|---|---|---|
| Full page | Visible | Hidden (403) | Hidden (403) |
| Export Summary button | Visible, enabled | N/A | N/A |
| Refresh Data button | Visible, enabled | N/A | N/A |
| Settings button | Visible, enabled | N/A | N/A |
| KPI bar (all 7 cards) | Visible | N/A | N/A |
| Alert banners | Visible, dismissible | N/A | N/A |
| Cross-Branch table | Visible, read-only | N/A | N/A |
| Data Quality Alerts — Acknowledge/Resolve | Visible, enabled | N/A | N/A |
| Team Activity table | Visible | N/A | N/A |
| Quick Navigation tiles | Visible (all 24) | N/A | N/A |
| Branch Detail drawer — "Flag for Review" | Visible, enabled | N/A | N/A |
| Alert Detail drawer — "Save Changes" | Visible, enabled | N/A | N/A |
| Export Modal | Visible | N/A | N/A |
| Bulk Export (selected rows) | Visible | N/A | N/A |

All write controls (Flag for Review, Acknowledge, Resolve, Save) are server-side rendered for Role 102 only via Django template tag `{% if request.user.role_id == 102 %}`.

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description | Query Parameters |
|---|---|---|---|---|
| GET | `/api/v1/analytics/director/kpis/` | JWT · Role 102 | Returns all 7 KPI values | `ay` (str, e.g. "2025-26") |
| GET | `/api/v1/analytics/branch-performance/` | JWT · Role 102 | Paginated cross-branch performance table | `ay`, `page`, `page_size`, `search`, `zone`, `band`, `completeness`, `branch_type`, `sort_by`, `sort_dir` |
| GET | `/api/v1/analytics/branch-performance/{branch_id}/` | JWT · Role 102 | Single branch detail (for drawer) | `ay` |
| POST | `/api/v1/analytics/branch-performance/{branch_id}/flag/` | JWT · Role 102 | Flag branch for review | — (body: `{"notes": "..."}`) |
| GET | `/api/v1/analytics/data-alerts/` | JWT · Role 102 | Paginated data quality alerts | `page`, `page_size`, `search`, `alert_type`, `severity`, `status`, `sort_by`, `sort_dir` |
| PATCH | `/api/v1/analytics/data-alerts/{alert_id}/` | JWT · Role 102 | Update alert status/resolution notes | — (body: `{"status": "acknowledged", "resolution_notes": "..."}`) |
| GET | `/api/v1/analytics/team-activity/` | JWT · Role 102 | Div-M team activity log | `page`, `page_size`, `search`, `role_id`, `action_type`, `date_from`, `date_to` |
| GET | `/api/v1/analytics/group-performance-index/` | JWT · Role 102 | Chart data: composite score per AY | `ay_from`, `ay_to` |
| GET | `/api/v1/analytics/branch-score-distribution/` | JWT · Role 102 | Chart data: branch score histogram bins | `ay` |
| POST | `/api/v1/analytics/export-jobs/` | JWT · Role 102 | Queue a new export job | — (body: `{format, sections[], ay, branch_scope, title, notes}`) |
| GET | `/api/v1/analytics/export-jobs/{job_id}/status/` | JWT · Role 102 | Poll export job status | — |
| GET | `/api/v1/analytics/export-jobs/{job_id}/download/` | JWT · Role 102 | Download completed export | — |

---

## 13. HTMX Patterns

| Pattern | Trigger Element | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI auto-refresh | `<div id="kpi-bar">` | `hx-get="/htmx/analytics/director/kpis/"` | `#kpi-bar` | `outerHTML` | `hx-trigger="every 120s"` |
| AY selector change — full reload | `<select id="ay-selector">` | `hx-get="/htmx/analytics/director/?ay={value}"` | `#dashboard-content` | `innerHTML` | `hx-trigger="change"` |
| Cross-branch table search | `<input id="branch-search">` | `hx-get="/htmx/analytics/branch-performance/"` | `#branch-table-body` | `innerHTML` | `hx-trigger="keyup changed delay:300ms"`, includes current filter params |
| Cross-branch table sort | Column header `<th>` | `hx-get="/htmx/analytics/branch-performance/"` | `#branch-table-body` | `innerHTML` | Passes `sort_by` and `sort_dir` |
| Cross-branch pagination | Pagination `<a>` | `hx-get="/htmx/analytics/branch-performance/"` | `#branch-table-body` | `innerHTML` | Passes `page` param |
| Cross-branch filter drawer apply | "Apply Filters" `<button>` | `hx-get="/htmx/analytics/branch-performance/"` | `#branch-table-body` | `innerHTML` | Serialises filter form |
| Data alerts table filter/search | Filter + search inputs | `hx-get="/htmx/analytics/data-alerts/"` | `#alerts-table-body` | `innerHTML` | 300 ms debounce on search |
| Data alert acknowledge | "Acknowledge" `<button>` in row | `hx-post="/htmx/analytics/data-alerts/{id}/acknowledge/"` | `#alert-row-{id}` | `outerHTML` | `hx-confirm` not needed; row updates in place |
| Data alert resolve | "Resolve" `<button>` in row | `hx-post="/htmx/analytics/data-alerts/{id}/resolve/"` | `#alert-row-{id}` | `outerHTML` | Row replaced with resolved state |
| Team activity table filter | Role/Date filter chips | `hx-get="/htmx/analytics/team-activity/"` | `#activity-table-body` | `innerHTML` | Chip toggles trigger re-fetch |
| Branch detail drawer open | Branch name `<a>` | `hx-get="/htmx/analytics/branch-detail/{id}/"` | `#detail-drawer-content` | `innerHTML` | `hx-trigger="click"` |
| Branch distribution chart — AY change | AY selector `<select>` | `hx-get="/htmx/analytics/chart/branch-distribution/"` | `#chart-distribution-container` | `innerHTML` | Re-renders chart JSON data |
| Export job status poll | Export status `<div>` | `hx-get="/htmx/analytics/export-jobs/{id}/status/"` | `#export-status-{id}` | `outerHTML` | `hx-trigger="every 5s"` while status is 'queued' or 'processing'; stops on 'completed' or 'failed' via `HX-Trigger` response header |
| Alert banner dismiss | Close `<button>` on banner | `hx-post="/htmx/alerts/dismiss/{alert_id}/"` | `#alert-banner-{id}` | `outerHTML` | Also writes to `sessionStorage` client-side |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
