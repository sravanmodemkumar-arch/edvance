# 103 — MIS Officer Dashboard

> **URL:** `/group/mis/officer/`
> **File:** `02-mis-officer-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Role:** MIS Officer (Role 103, G1) — exclusive post-login landing

---

## 1. Purpose

The MIS Officer Dashboard is the operational command centre for the Group MIS Officer (Role 103), responsible for ensuring the Chairman, Board, CEO, and CFO receive complete and timely monthly MIS reports covering attendance, fee collection, and exam results across all branches. This dashboard tracks every report in the generation pipeline — from scheduled upcoming reports to overdue items — and confirms distribution success so nothing falls through the cracks. At group scale (5–50 branches, 8–20 MIS reports per month), the Officer must have instant visibility into what has been sent, what is pending, which branches have not submitted source data, and which distribution attempts failed. This page is the single accountability surface for Group MIS operations.

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| MIS Officer | 103 | G1 | Full Read + Manage own MIS outputs | Exclusive landing; can create/edit/delete MIS reports |
| Analytics Director | 102 | G1 | Read-only view via Div-M navigation | Not their landing page |
| All other roles | Any | Any | No access | HTTP 403 |

Access enforcement: `@role_required(103)` Django decorator. Analytics Director (102) may access this URL with read-only rendering — write controls hidden server-side.

---

## 3. Page Layout

### 3.1 Breadcrumb

```
Group Home > Analytics & MIS > MIS Officer Dashboard
```

### 3.2 Page Header

**Title:** `MIS Officer Dashboard`
**Sub-title:** `[Group Name] · [Current Month, Year] · AY: [current AY]`

Action buttons (right-aligned):

| Button | Icon | Behaviour | Visible To |
|---|---|---|---|
| Generate New Report | plus-circle | Opens Generate Report modal | Role 103 |
| Schedule Report | calendar | Opens Schedule Report modal | Role 103 |
| Export Log | download | Exports distribution log as XLSX | Role 103 |
| Refresh | refresh | HTMX re-poll KPIs + queue table | Role 103, 102 |

Month/AY selectors: Two linked selects — Month (Jan–Dec) and AY (last 5 AYs). Changing either triggers `hx-get` to reload all sections.

### 3.3 Alert Banners

Individually dismissible per session via `sessionStorage`. Close (×) on each banner.

| Condition | Banner Text | Severity |
|---|---|---|
| Any report overdue (due date passed, status != 'generated') | "⚠ [N] report(s) are overdue for [Month]. Generate and distribute immediately." | Error (red) |
| Distribution failure on any report (any recipient not delivered) | "[N] distribution failure(s) detected. Confirm recipients received their reports." | Error (red) |
| Branches with missing source data for current month | "[N] branch(es) have not submitted data required for this month's MIS reports." | Warning (amber) |
| Scheduled report due in < 48 h | "[N] report(s) are due within 48 hours." | Warning (amber) |
| Board report not yet generated for current month | "Board MIS report for [Month] has not been generated. Due date: [date]." | Warning (amber) |
| All reports generated and distributed | "All MIS reports for [Month] have been generated and distributed successfully." | Success (green, auto-dismiss 6s) |

---

## 4. KPI Summary Bar

HTMX auto-refresh every 90 seconds via `hx-trigger="every 90s"` on KPI container.

| Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|
| Reports Generated This Month | Count of MIS reports with status = 'generated' in current month | COUNT(mis_reports WHERE month = current AND ay = current AND status = 'generated') | Neutral (blue) | `#kpi-generated` |
| Reports Pending This Month | Count of scheduled reports not yet generated, current month | COUNT(mis_report_schedule WHERE month = current AND ay = current AND status != 'generated') | Green = 0; Amber 1–3; Red ≥ 4 | `#kpi-pending` |
| Distribution Success Rate | % of generated reports where all recipients confirmed delivery | (Distributions delivered / total distributions attempted) × 100, current month | Green ≥ 95%; Amber 85–94%; Red < 85% | `#kpi-distribution-rate` |
| Branches with Missing Data | Branches that haven't submitted current-month required data | COUNT(branches WHERE monthly_submission_status = 'missing' AND month = current) | Green = 0; Amber 1–3; Red ≥ 4 | `#kpi-missing-branches` |
| Scheduled Reports Next 7 Days | Reports in schedule with due_date within next 7 calendar days | COUNT(mis_report_schedule WHERE due_date BETWEEN TODAY AND TODAY+7 AND status != 'generated') | Green = 0; Amber 1–2; Red ≥ 3 | `#kpi-upcoming` |
| Board Reports Generated This AY | Count of Board-level MIS reports generated in current AY | COUNT(mis_reports WHERE report_type = 'board' AND ay = current AND status = 'generated') | Neutral (blue) | `#kpi-board-reports` |

---

## 5. Sections

### 5.1 Report Generation Queue

**Purpose:** Shows all MIS reports that are due or overdue, ordered by urgency. The MIS Officer uses this to action pending reports one by one.

**Search bar:** Search by report title, report type, branch. Debounced 300 ms. Placeholder: "Search report title or type…".

**Inline filter chips:**
- Status: All | Scheduled | Overdue | In Progress | Generated
- Report Type: All | Monthly MIS | Board Report | Fee Summary | Attendance Summary | Exam Results | Custom
- Due Date: All | Overdue | Due Today | Due This Week | Due This Month

**Table columns:**

| Column | Source Field | Sortable | Notes |
|---|---|---|---|
| # | Row index | No | |
| Report Title | `mis_report_schedule.title` | Yes | Click → Report Detail drawer |
| Report Type | `mis_report_schedule.report_type` | Yes | Colour-coded badge |
| Scope | `mis_report_schedule.scope` | Yes | All Branches / Specific Branch(es) |
| Due Date | `mis_report_schedule.due_date` | Yes | Red if past due; amber if ≤ 48 h away |
| Days Until/Since Due | Calculated | Yes | Positive = days remaining; negative = days overdue (red) |
| Data Ready | `mis_report_schedule.data_ready` | Yes | Yes (green check) / Partial (amber) / No (red X) |
| Status | `mis_report_schedule.status` | Yes | Scheduled / Overdue / In Progress / Generated badge |
| Assigned Recipients | `mis_report_schedule.recipient_count` | Yes | Count; hover shows role list |
| Actions | — | No | "Generate Now" button (enabled only if Data Ready ≠ No) / "Edit Schedule" / "Cancel" |

**Default sort:** Due Date ascending (most urgent first). Overdue items always pinned to top.

**Pagination:** Server-side, 25/page.

**"Generate Now" button behaviour:** Opens Generate Report modal pre-filled with schedule data. On success: row updates status to 'In Progress', then 'Generated' via HTMX polling.

---

### 5.2 Recent Reports Generated

**Purpose:** Audit trail of the last 30 reports generated, with download links and distribution status.

**Search bar:** Search by title, report type, generated-by. Debounced 300 ms.

**Inline filter chips:**
- Report Type: All | Monthly MIS | Board Report | Fee Summary | Attendance Summary | Exam Results | Custom
- Distribution Status: All | Distributed | Partially Distributed | Not Distributed | Failed
- Date Range: Today | This Week | This Month | This AY | Custom

**Table columns:**

| Column | Source Field | Sortable | Notes |
|---|---|---|---|
| # | Row index | No | |
| Report Title | `mis_reports.title` | Yes | Click → Report Detail drawer |
| Report Type | `mis_reports.report_type` | Yes | Badge |
| Scope | `mis_reports.scope` | Yes | All Branches / specific |
| Generated By | `mis_reports.generated_by_name` | Yes | Name; tooltip shows role |
| Generated At | `mis_reports.generated_at` | Yes | Datetime, relative |
| File Size | `mis_reports.file_size_kb` | Yes | KB/MB formatted |
| Distribution Status | `mis_reports.distribution_status` | Yes | Badge: Distributed (green) / Partial (amber) / Not Distributed (grey) / Failed (red) |
| Recipients Reached | `mis_reports.recipients_reached` / `total` | Yes | "X/Y" format |
| Actions | — | No | Download (PDF/XLSX) / Redistribute / View Detail |

**Default sort:** Generated At descending.

**Pagination:** Server-side, 25/page.

**"Redistribute" button:** Shown for status = 'Failed' or 'Partially Distributed'. Opens Redistribute modal.

---

### 5.3 Distribution Log

**Purpose:** Granular record of every report distribution attempt — who received what report, by which channel, and whether delivery was confirmed. Used for accountability to Chairman/Board.

**Search bar:** Search by recipient name, report title, channel. Debounced 300 ms.

**Inline filter chips:**
- Delivery Channel: All | Email | Portal Notification | WhatsApp | SMS
- Status: All | Delivered | Pending | Failed | Bounced
- Recipient Role: All | Chairman | Board Member | CEO | CAO | CFO | Custom
- Date Range: Today | This Week | This Month | Custom

**Table columns:**

| Column | Source Field | Sortable | Notes |
|---|---|---|---|
| # | Row index | No | |
| Report Title | `distribution_log.report_title` | Yes | Link to Report Detail drawer |
| Recipient Name | `distribution_log.recipient_name` | Yes | Full name |
| Recipient Role | `distribution_log.recipient_role` | Yes | Chairman / Board / CEO etc. badge |
| Channel | `distribution_log.channel` | Yes | Email / Portal / WhatsApp / SMS icon + label |
| Sent At | `distribution_log.sent_at` | Yes | Datetime, relative |
| Delivered At | `distribution_log.delivered_at` | Yes | Datetime or "Pending" |
| Status | `distribution_log.status` | Yes | Delivered (green) / Pending (amber) / Failed (red) / Bounced (orange) |
| Failure Reason | `distribution_log.failure_reason` | No | Shown only for Failed/Bounced; truncated 60 chars |
| Actions | — | No | Resend (for Failed/Bounced); View Detail |

**Default sort:** Sent At descending.

**Pagination:** Server-side, 25/page.

---

### 5.4 Branch Data Submission Status

**Purpose:** Shows which branches have submitted their source data for the current month (required for MIS report generation). MIS Officer can identify laggards and follow up.

**Search bar:** Search by branch name or code. Debounced 300 ms.

**Inline filter chips:**
- Submission Status: All | Complete | Partial | Missing
- Region/Zone: dynamic from branch data
- Branch Type: All | Day | Residential | Semi-Residential

**Table columns:**

| Column | Source Field | Sortable | Notes |
|---|---|---|---|
| # | Row index | No | |
| Branch Name | `branch.name` | Yes | |
| Branch Code | `branch.code` | Yes | Monospace |
| Region/Zone | `branch.zone` | Yes | |
| Attendance Data | `branch_submission.attendance_status` | Yes | Complete / Partial / Missing badge |
| Fee Data | `branch_submission.fee_status` | Yes | Complete / Partial / Missing badge |
| Exam Results Data | `branch_submission.exam_status` | Yes | Complete / Partial / Missing badge |
| Overall Status | `branch_submission.overall_status` | Yes | Complete (green) / Partial (amber) / Missing (red) |
| Last Submitted At | `branch_submission.last_submitted_at` | Yes | Datetime, relative; red if > 7 days |
| Submitted By | `branch_submission.submitted_by_name` | Yes | Name + role |
| Actions | — | No | "Send Reminder" (email to branch coordinator) |

**Default sort:** Overall Status (Missing first), then Last Submitted At ascending.

**Pagination:** Server-side, 25/page.

**"Send Reminder" button:** POST to send notification to branch data coordinator. Toast on success/error.

---

## 6. Drawers & Modals

### 6.1 Report Detail Drawer

Triggered by: Clicking report title in 5.1 or 5.2.
Width: 600px. Slide from right. ESC / backdrop click closes with unsaved-changes guard.

**Tabs:**

**Tab 1 — Report Info**

| Field | Value |
|---|---|
| Report Title | Editable text (Role 103 only, max 150 chars) |
| Report Type | Badge |
| Academic Year | Text |
| Month/Period | Text |
| Scope | Branches covered (list) |
| Generated By | Name + role |
| Generated At | Full datetime |
| File | Download PDF / XLSX buttons |
| Status | Badge |
| Notes | Editable textarea (Role 103 only, max 500 chars, character counter) |

**Tab 2 — Distribution Status**

Table: Recipient Name | Role | Channel | Sent At | Status | Action (Resend)
Summary line: "X of Y recipients confirmed delivery."

**Tab 3 — Source Data**

Table: Branch | Attendance Data | Fee Data | Exam Data | Completeness %.
Shows which branches contributed data to this report.

**Footer:** "Save Changes" / "Redistribute All" / "Delete Report" (with confirm modal) / "Close"

---

### 6.2 Generate Report Modal

Triggered by: "Generate New Report" button or "Generate Now" in queue.
Size: 480px centred overlay.

**Fields:**

| Field | Type | Required | Validation |
|---|---|---|---|
| Report Title | Text input | Yes | Max 150 chars; auto-suggest based on type + month |
| Report Type | Select | Yes | Monthly MIS / Board Report / Fee Summary / Attendance Summary / Exam Results / Custom |
| Academic Year | Select | Yes | Current and last 3 AYs |
| Month / Period | Select | Yes | Jan–Dec for monthly; or "Full AY" |
| Branch Scope | Checkbox group | Yes | All branches (default checked) or select specific |
| Output Format | Radio: PDF / XLSX / Both | Yes | Default: Both |
| Recipients | Multi-select tag input | Yes | Roles: Chairman, Board, CEO, CAO, CFO, Custom. At least 1. |
| Distribution Channel | Checkbox group | Yes | Email / Portal Notification / WhatsApp / SMS. At least 1. |
| Distribute Immediately | Toggle | No | Default ON |
| Notes | Textarea | No | Max 500 chars; character counter |

**Footer:** "Generate" (primary, disabled until valid) / "Cancel"

---

### 6.3 Schedule Report Modal

Triggered by: "Schedule Report" button.
Size: 480px centred.

**Fields:**

| Field | Type | Required | Validation |
|---|---|---|---|
| Report Title Template | Text input | Yes | Max 150 chars; `{month}` and `{ay}` variables allowed |
| Report Type | Select | Yes | Same options as Generate modal |
| Recurrence | Select | Yes | Monthly / Quarterly / Annual / One-time |
| Day of Month | Number input | Yes (if Monthly) | 1–28; tooltip "We recommend day 5–10 to allow branches to submit data" |
| Due Date | Date picker | Yes | Must be ≥ today |
| Branch Scope | Checkbox group | Yes | All / Specific |
| Recipients | Multi-select | Yes | Same as Generate modal |
| Distribution Channel | Checkbox group | Yes | |
| Active | Toggle | Yes | Default ON |

**Footer:** "Save Schedule" / "Cancel"

---

### 6.4 Redistribute Modal

Triggered by: "Redistribute" button in 5.2.
Size: 480px centred.

**Fields:**

| Field | Type | Required | Validation |
|---|---|---|---|
| Recipients | Multi-select (pre-filled with failed recipients) | Yes | At least 1 |
| Channel | Checkbox group (pre-filled) | Yes | |
| Note to Recipient | Textarea | No | Max 300 chars |
| Send Now | Toggle | Yes | Default ON |

**Footer:** "Redistribute" / "Cancel"

---

## 7. Charts

### 7.1 Reports Generated per Month — Bar Chart

| Property | Value |
|---|---|
| Type | Chart.js Bar |
| Title | "MIS Reports Generated per Month — [Current AY]" |
| Data | Count of generated reports per calendar month in the current AY, split by report type (series per type) |
| X-Axis | Month labels: "Apr", "May", "Jun", …, "Mar" |
| Y-Axis | "Number of Reports Generated"; integer ticks |
| Colours | Monthly MIS `#4F46E5`, Board Report `#7C3AED`, Fee Summary `#0EA5E9`, Attendance `#10B981`, Exam Results `#F59E0B`, Custom `#6B7280` |
| Tooltip | "[Month]: [Type] — [N] reports generated" |
| API Endpoint | `GET /api/v1/mis/reports/monthly-count/?ay=2025-26` |
| HTMX Pattern | `hx-get` on AY selector change, target `#chart-reports-generated`, swap `innerHTML` |
| Export | PNG export top-right of chart card |
| Colorblind-safe | Yes — colour + pattern fill |
| Empty State | "No reports generated for the selected academic year." |

---

### 7.2 Distribution Coverage per Report — Horizontal Bar Chart

| Property | Value |
|---|---|
| Type | Chart.js Bar (horizontal) |
| Title | "Distribution Coverage — Reports This Month" |
| Data | For each generated report this month: % of recipients who received it. One bar per report. |
| X-Axis | Percentage 0–100%; threshold line at 100% |
| Y-Axis | Report title labels (truncated to 40 chars) |
| Colours | ≥ 100% `#22C55E` (green), 75–99% `#EAB308` (amber), < 75% `#EF4444` (red) |
| Tooltip | "[Report Title]: [X]% recipients reached ([N] of [Y])" |
| API Endpoint | `GET /api/v1/mis/distribution/coverage/?month=3&ay=2025-26` |
| HTMX Pattern | `hx-get` on Month/AY selector change, target `#chart-distribution-coverage`, swap `innerHTML` |
| Export | PNG export top-right |
| Colorblind-safe | Yes |
| Empty State | "No reports distributed in the selected month." |

---

## 8. Toast Messages

| Action | Toast Text | Type |
|---|---|---|
| Page load success | "MIS Officer Dashboard loaded." | Success |
| Page load error | "Failed to load dashboard. Please refresh." | Error |
| KPI refresh success | "KPIs refreshed." | Success |
| KPI refresh error | "Could not refresh KPIs." | Error |
| Report generation started | "Generating report '[Title]'. This may take a few minutes." | Info |
| Report generation success | "Report '[Title]' generated successfully." | Success |
| Report generation error | "Failed to generate report '[Title]'. Check source data completeness." | Error |
| Report scheduled | "Report schedule saved." | Success |
| Report schedule error | "Failed to save schedule. Please try again." | Error |
| Distribution started | "Distributing '[Title]' to [N] recipient(s)." | Info |
| Distribution success | "Report distributed to all [N] recipient(s) successfully." | Success |
| Distribution partial | "[N] of [Y] recipients reached. [M] failed — check distribution log." | Warning |
| Distribution error | "Distribution failed. Please retry or contact support." | Error |
| Reminder sent | "Reminder sent to branch coordinator at [Branch]." | Success |
| Reminder send error | "Failed to send reminder to [Branch]. Please try again." | Error |
| Report deleted | "Report '[Title]' deleted." | Success |
| Report delete error | "Failed to delete report. Please try again." | Error |
| Schedule changes saved | "Schedule updated successfully." | Success |
| Schedule changes error | "Failed to save schedule changes." | Error |
| Export log started | "Export log download started." | Info |
| Filter cleared | "All filters cleared." | Info |

---

## 9. Empty States

| Context | Icon | Heading | Sub-text | Action |
|---|---|---|---|---|
| 5.1 Queue — no pending reports | check-circle (green) | "No Reports Pending" | "All scheduled reports for this month have been generated. Great work!" | None |
| 5.1 Queue — search/filter no match | magnify | "No Matching Reports" | "Adjust your search or filters." | "Clear Filters" |
| 5.2 Recent Reports — no reports yet | document (grey) | "No Reports Generated Yet" | "Generated reports for [Month] will appear here." | "Generate New Report" button |
| 5.2 Recent Reports — search/filter no match | magnify | "No Matching Reports" | "Adjust search or date range filters." | "Clear Filters" |
| 5.3 Distribution Log — no distributions | mail (grey) | "No Distributions Recorded" | "Distribution records will appear here once reports are sent to recipients." | None |
| 5.3 Distribution Log — search/filter no match | magnify | "No Matching Records" | "Try different search terms or filters." | "Clear Filters" |
| 5.4 Branch Data Status — no branches | building (grey) | "No Branch Data" | "Branch submission statuses will appear once branches are configured in the system." | None |
| 5.4 Branch Data Status — search/filter no match | magnify | "No Matching Branches" | "Adjust search or filters." | "Clear Filters" |
| 7.1 Chart — no data | chart-bar (grey) | "No Report Data" | "Report generation data will appear here once reports are generated for the selected AY." | None |
| 7.2 Chart — no data | chart-bar (grey) | "No Distribution Data" | "Distribution coverage data will appear once reports are distributed this month." | None |

---

## 10. Loader States

| Context | Loader Behaviour |
|---|---|
| Initial page load | Skeleton: 6 KPI cards pulsing grey; each table section shows 5 skeleton rows; charts show grey rectangles |
| KPI auto-refresh (90s) | Spinner in each KPI card header; values fade to 60% opacity |
| Month/AY selector change | All 4 table sections + 2 charts show skeleton simultaneously |
| Report generation in progress | "Generate Now" / "Generate" button shows spinner + "Generating…"; button disabled; queue row shows 'In Progress' badge with pulsing animation |
| Report scheduled save | "Save Schedule" button shows spinner + "Saving…" |
| Distribution in progress | "Redistribute" / distribution button shows spinner; row dims 50% |
| Reminder send | "Send Reminder" row button shows spinner |
| Table search/filter | Table body shows 5 skeleton rows during HTMX fetch; search input shows spinner at right end |
| Chart loading | Grey pulsing rectangle until Chart.js renders |
| Drawer opening | Drawer slides in with skeleton fields |
| Export log download | "Export Log" button shows spinner + "Exporting…" |

---

## 11. Role-Based UI Visibility

| UI Element | Role 103 (MIS Officer) | Role 102 (Analytics Director) | All Others |
|---|---|---|---|
| Full page | Visible | Read-only | Hidden (403) |
| "Generate New Report" button | Visible, enabled | Hidden | N/A |
| "Schedule Report" button | Visible, enabled | Hidden | N/A |
| "Export Log" button | Visible, enabled | Visible, enabled | N/A |
| "Refresh" button | Visible | Visible | N/A |
| KPI bar | Visible | Visible | N/A |
| Alert banners | Visible, dismissible | Visible, dismissible | N/A |
| Queue table — "Generate Now" | Visible, enabled | Hidden | N/A |
| Queue table — "Edit Schedule" | Visible, enabled | Hidden | N/A |
| Queue table — "Cancel" | Visible, enabled | Hidden | N/A |
| Recent reports — "Redistribute" | Visible, enabled | Hidden | N/A |
| Recent reports — "Delete Report" | Visible, enabled | Hidden | N/A |
| Distribution log — "Resend" | Visible, enabled | Hidden | N/A |
| Branch status — "Send Reminder" | Visible, enabled | Hidden | N/A |
| Report Detail drawer — save/edit | Visible, enabled | Read-only (no save) | N/A |
| Charts | Visible | Visible | N/A |

All write controls rendered server-side: `{% if request.user.role_id == 103 %}`.

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description | Query Parameters |
|---|---|---|---|---|
| GET | `/api/v1/mis/kpis/` | JWT · Role 103, 102 | All 6 KPI values | `month` (1–12), `ay` |
| GET | `/api/v1/mis/report-queue/` | JWT · Role 103, 102 | Paginated pending report queue | `page`, `page_size`, `search`, `status`, `report_type`, `due_filter`, `sort_by`, `sort_dir` |
| GET | `/api/v1/mis/reports/` | JWT · Role 103, 102 | Paginated generated reports | `page`, `page_size`, `search`, `report_type`, `distribution_status`, `date_from`, `date_to`, `sort_by`, `sort_dir` |
| GET | `/api/v1/mis/reports/{report_id}/` | JWT · Role 103, 102 | Single report detail | — |
| POST | `/api/v1/mis/reports/generate/` | JWT · Role 103 | Generate a new report | — (body: report config JSON) |
| POST | `/api/v1/mis/reports/schedule/` | JWT · Role 103 | Create/update report schedule | — (body: schedule config JSON) |
| PATCH | `/api/v1/mis/reports/{report_id}/` | JWT · Role 103 | Update report title/notes | — (body: partial update) |
| DELETE | `/api/v1/mis/reports/{report_id}/` | JWT · Role 103 | Delete a report | — |
| POST | `/api/v1/mis/reports/{report_id}/distribute/` | JWT · Role 103 | Trigger distribution (or redistribution) | — (body: `{recipients[], channels[]}`) |
| GET | `/api/v1/mis/distribution-log/` | JWT · Role 103, 102 | Paginated distribution log | `page`, `page_size`, `search`, `channel`, `status`, `recipient_role`, `date_from`, `date_to` |
| GET | `/api/v1/mis/branch-submission-status/` | JWT · Role 103, 102 | Branch data submission status for month | `month`, `ay`, `page`, `page_size`, `search`, `status`, `zone`, `branch_type` |
| POST | `/api/v1/mis/branch-submission-status/{branch_id}/remind/` | JWT · Role 103 | Send reminder to branch coordinator | — |
| GET | `/api/v1/mis/reports/monthly-count/` | JWT · Role 103, 102 | Chart data: reports per month | `ay` |
| GET | `/api/v1/mis/distribution/coverage/` | JWT · Role 103, 102 | Chart data: distribution coverage per report | `month` (1–12), `ay` |
| GET | `/api/v1/mis/reports/{report_id}/download/` | JWT · Role 103, 102 | Download report file | `format` (pdf/xlsx) |

---

## 13. HTMX Patterns

| Pattern | Trigger Element | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI auto-refresh | `<div id="kpi-bar">` | `hx-get="/htmx/mis/kpis/"` | `#kpi-bar` | `outerHTML` | `hx-trigger="every 90s"` |
| Month/AY change — reload all | `<select id="month-selector">, <select id="ay-selector">` | `hx-get="/htmx/mis/officer/?month={m}&ay={ay}"` | `#dashboard-content` | `innerHTML` | `hx-trigger="change"` |
| Report queue search | `<input id="queue-search">` | `hx-get="/htmx/mis/report-queue/"` | `#queue-table-body` | `innerHTML` | `hx-trigger="keyup changed delay:300ms"` |
| Report queue filter chips | Filter chip `<button>` elements | `hx-get="/htmx/mis/report-queue/"` | `#queue-table-body` | `innerHTML` | Serialises chip state |
| Report queue sort | Column `<th>` | `hx-get="/htmx/mis/report-queue/"` | `#queue-table-body` | `innerHTML` | `sort_by`, `sort_dir` params |
| Report queue pagination | Pagination `<a>` | `hx-get="/htmx/mis/report-queue/"` | `#queue-table-body` | `innerHTML` | `page` param |
| Recent reports search/filter | Search + filter inputs | `hx-get="/htmx/mis/reports/"` | `#reports-table-body` | `innerHTML` | 300ms debounce on search |
| Distribution log search/filter | Search + filter inputs | `hx-get="/htmx/mis/distribution-log/"` | `#dist-log-table-body` | `innerHTML` | 300ms debounce |
| Branch submission search/filter | Search + filter inputs | `hx-get="/htmx/mis/branch-submission/"` | `#branch-sub-table-body` | `innerHTML` | 300ms debounce |
| Report detail drawer open | Report title `<a>` | `hx-get="/htmx/mis/reports/{id}/detail/"` | `#detail-drawer-content` | `innerHTML` | Triggers drawer slide-in |
| Send branch reminder | "Send Reminder" `<button>` | `hx-post="/htmx/mis/branch/{id}/remind/"` | `#remind-row-{id}` | `outerHTML` | Row updates button to "Sent ✓" on success |
| Report generation status poll | `<div id="gen-status-{id}">` | `hx-get="/htmx/mis/reports/{id}/gen-status/"` | `#gen-status-{id}` | `outerHTML` | `hx-trigger="every 5s"` while status = 'in_progress'; stops via `HX-Trigger` header |
| Distribution status poll | `<div id="dist-status-{id}">` | `hx-get="/htmx/mis/distribution/{id}/status/"` | `#dist-status-{id}` | `outerHTML` | `hx-trigger="every 5s"` while status = 'pending' |
| Chart refresh on AY change | `<select id="ay-selector">` | `hx-get="/htmx/mis/chart/monthly-count/"` | `#chart-reports-generated` | `innerHTML` | Parallel with distribution chart |
| Distribution chart refresh | `<select id="month-selector">` | `hx-get="/htmx/mis/chart/distribution-coverage/"` | `#chart-distribution-coverage` | `innerHTML` | |
| Alert banner dismiss | Close `<button>` on banner | `hx-post="/htmx/alerts/dismiss/{id}/"` | `#alert-banner-{id}` | `outerHTML` | + `sessionStorage` write |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
