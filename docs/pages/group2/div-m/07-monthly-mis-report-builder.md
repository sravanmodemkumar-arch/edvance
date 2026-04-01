# 07 — Monthly MIS Report Builder

> **URL:** `/group/mis/builder/`
> **File:** `07-monthly-mis-report-builder.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Role 102 (Group Analytics Director), Role 103 (Group MIS Officer), Role 104 (Group Academic Data Analyst), Role 105 (Group Exam Analytics Officer), Role 106 (Group Hostel Analytics Officer), Role 107 (Group Strategic Planning Officer)

---

## 1. Purpose

The Monthly MIS Report Builder is the primary configuration and generation tool used by the MIS Officer (Role 103) to define, schedule, and dispatch management information system reports to senior stakeholders including the Chairman, Board members, CEO, CAO, and CFO. The Officer configures report templates by selecting which data sections to include (attendance, fee collection, exam results, HR stats, hostel summary, welfare events), specifies distribution recipients and delivery methods, and sets automated generation schedules tied to the academic calendar. Reports are produced as PDF and/or XLSX files and stored in Cloudflare R2 before distribution. The Analytics Director (Role 102) may view all templates and trigger on-demand generation; all other Division M roles have read-only access to the builder to understand report cadence and coverage.

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Analytics Director | 102 | G1 | View all templates, trigger on-demand generation, view logs | Cannot create or edit templates |
| Group MIS Officer | 103 | G1 | Full CRUD — create, edit, delete templates; schedule; generate on-demand; send reports | Primary owner of this page |
| Group Academic Data Analyst | 104 | G1 | View only — templates, queue, log | Cannot generate or edit |
| Group Exam Analytics Officer | 105 | G1 | View only | Cannot generate or edit |
| Group Hostel Analytics Officer | 106 | G1 | View only | Cannot generate or edit |
| Group Strategic Planning Officer | 107 | G1 | View only | Cannot generate or edit |

**Access enforcement note:** All access checks are server-side. Template create/edit/delete buttons are rendered only for Role 103. The "Generate Now" button is rendered for Roles 102 and 103. All other roles receive read-only rendered HTML with no action affordances. HTMX endpoints for mutation are guarded by `@require_role([103])` decorators; generation endpoints by `@require_role([102, 103])`.

---

## 3. Page Layout

### 3.1 Breadcrumb

```
Group Dashboard > Analytics & MIS > MIS Report Builder
```

### 3.2 Page Header

- **Title:** `MIS Report Builder`
- **Subtitle:** `Configure, schedule, and generate monthly MIS reports for Board and senior management`
- **Header actions (Role 103 only):** `[+ New Report Template]` button (primary, opens `report-template-create` drawer)
- **Header actions (Roles 102–103):** `[Generate Report]` dropdown button listing all Active templates for on-demand generation

### 3.3 Alert Banners (conditional, each individually dismissible)

| Condition | Colour | Message |
|---|---|---|
| Current month > 5th and no report generated this month | Red | "MIS report overdue — it is past the 5th and no report has been generated this month. Generate now." with [Generate] CTA |
| Any template has branches with missing data inputs | Amber | "One or more report templates have branches with missing data. Review before generating." with [Review] CTA |
| Any scheduled report is in Paused state | Amber | "You have paused scheduled reports. They will not auto-generate until resumed." with [View Paused] CTA |
| Any Active template has zero recipients configured | Blue | "Some templates have no recipients configured. Reports will generate but will not be sent." with [Configure Recipients] CTA |

---

## 4. KPI Summary Bar

| KPI | Description | Format |
|---|---|---|
| Active Templates | Count of report templates with status = Active | Integer badge |
| Reports Generated This Month | Count of successful generation jobs in current calendar month | Integer |
| Reports Overdue | Templates where expected generation date has passed and no report generated | Integer, red if > 0 |
| Scheduled This Month | Count of auto-generate jobs due in current calendar month | Integer |
| Total Recipients Configured | Distinct recipients across all Active templates | Integer |
| Branches Missing Data | Branches flagged as having incomplete data for any Active template | Integer, amber if > 0 |

KPI bar is a horizontal scrollable card row on mobile. Each card has a label, value, and optional status colour. Data fetched from `/api/v1/mis/builder/kpis/` on page load.

---

## 5. Sections

### 5.1 Report Templates Table

Displays all configured MIS report templates for the group, regardless of status.

**Table columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Checkbox | Checkbox | No | Bulk select; select-all in header |
| Report Name | Text link | Yes | Opens `report-template-edit` drawer on click (Role 103) or read-only detail drawer (others) |
| Type | Badge | Yes | Monthly MIS / Board Report / Custom |
| Sections Included | Compact list | No | Abbreviated section names, e.g. "Enrol, Fees, Attendance +3" |
| Frequency | Text | Yes | One-time / Monthly / Quarterly / Custom |
| Last Generated | Datetime | Yes | Relative time (e.g. "3 days ago") with absolute on hover |
| Next Due | Date | Yes | Highlighted amber if overdue |
| Status | Badge | Yes | Active (green) / Paused (amber) / Draft (grey) |
| Actions | Button group | No | [Generate Now] (Roles 102–103), [Edit] (Role 103), [Delete] (Role 103) |

**Table behaviour:**
- Default sort: Status ASC then Next Due ASC
- Rows per page selector: 10 / 25 / 50 / All (default 25)
- Row hover reveals inline action buttons
- Checkbox bulk actions (Role 103 only): Bulk Pause, Bulk Activate, Bulk Delete
- Responsive: collapses to card layout on viewport < 768px; card shows Report Name, Type badge, Status badge, Next Due, and a "..." action menu

**Search:** Full-text search on Report Name and Type. 300ms debounce. Targets `hx-get="/api/v1/mis/builder/templates/"` with `?q=` param. Clears on Escape key.

**Advanced Filters (slide-in drawer, 360px, opens right):**

| Filter | Type | Options |
|---|---|---|
| Report Type | Multi-select checkbox | Monthly MIS, Board Report, Custom |
| Status | Multi-select checkbox | Active, Paused, Draft |
| Frequency | Multi-select checkbox | One-time, Monthly, Quarterly, Custom |
| Sections Included | Multi-select checkbox | All 9 section options |
| Has Recipients | Toggle | Yes / No |
| Last Generated (range) | Date range picker | From – To |

Active filters display as dismissible chips below the filter button. [Clear All] removes all chips and reloads table.

**Empty state:** Illustration of a blank report page. Heading: "No report templates yet." Description: "Create your first MIS report template to get started." CTA: [+ New Report Template] (Role 103 only).

**Loader state:** 5-row skeleton with alternating grey bars at 60%, 40%, 80%, 30%, 70% width.

---

### 5.2 Scheduled Reports Queue

Shows all auto-generate jobs expected to run in the next 30 days.

**Table columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Report Name | Text | Yes | Link to template |
| Type | Badge | Yes | |
| Scheduled Date | Date | Yes | Highlighted if < 3 days away |
| Frequency | Text | No | |
| Recipients | Count | No | Number of configured recipients |
| Status | Badge | No | Scheduled (blue) / Paused (amber) / Skipped (grey) |
| Actions | Button group | No | [Run Now] (Role 103), [Pause] (Role 103) |

Default sort: Scheduled Date ASC. Max 30 rows (30-day window). No pagination — full list shown.

**Empty state:** Heading: "No scheduled reports in the next 30 days." Description: "Configure a report template with a recurring schedule to see it here."

---

### 5.3 Recent Generations Log

Last 20 report generation jobs (on-demand and auto), most recent first.

**Table columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Report Name | Text | Yes | |
| Type | Badge | No | |
| Generated By | Text | No | User name + "(Auto)" if scheduled |
| Generated At | Datetime | Yes | |
| Duration | Text | No | Time taken to generate (e.g. "42s") |
| Format | Badge | No | PDF / XLSX / Both |
| Status | Badge | No | Completed (green), In Progress (blue spinner), Failed (red) |
| Actions | Button group | No | [Download] (if Completed), [Retry] (if Failed, Role 103), [View Log] |

Default sort: Generated At DESC. Fixed 20-row display, no pagination. Table auto-refreshes every 30 seconds via HTMX polling if any row is In Progress.

**Empty state:** Heading: "No reports generated yet." Description: "Use the Generate Now button on any active template."

---

## 6. Drawers & Modals

### 6.1 Drawer: `report-template-create`

**Width:** 680px. Slides in from right. Overlay backdrop. Tab-based layout.

**Tab 1 — Scope**

| Field | Type | Required | Validation |
|---|---|---|---|
| Report Name | Text input | Yes | Min 3, max 120 chars; unique within group |
| Report Type | Select | Yes | Options: Monthly MIS, Board Report, Custom |
| Academic Year | Select | Yes | Populated from group AY config (e.g. 2025-26) |
| Date Range Mode | Radio | Yes | Options: Month Picker (single month) / Custom Range (From–To dates) |
| Date From | Date picker | Conditional | Required if Custom Range; must be < Date To |
| Date To | Date picker | Conditional | Required if Custom Range; must be > Date From |
| Month | Month picker | Conditional | Required if Month Picker mode; format YYYY-MM |
| Branches | Multi-select | Yes | Options: All Branches (default) / Select Specific; if specific, shows branch multi-select dropdown |
| Sections to Include | Checkbox group | Yes | At least 1 required. Options: Enrollment & Admissions, Fee Collection, Attendance Summary, Exam Results Summary, Staff HR Summary, Hostel Summary, Transport Summary, Welfare Events, Custom Notes |

**Tab 2 — Recipients**

| Field | Type | Required | Validation |
|---|---|---|---|
| Recipients | Multi-select typeahead | Yes (at least 1 recommended — shown as warning if empty) | Search by name or role from group contacts; shows role label next to name |
| Delivery Method | Checkbox group | Yes | Options: Email PDF, Email XLSX, Portal Only (at least 1 required) |
| CC Email List | Textarea | No | One email per line; validates each line as valid email format; max 20 lines; char counter shown |

**Tab 3 — Schedule**

| Field | Type | Required | Validation |
|---|---|---|---|
| Frequency | Select | Yes | Options: One-time, Monthly, Quarterly, Custom |
| Generation Day | Number input | Conditional | Required if Monthly or Quarterly; day of month 1–28 (capped at 28 for safety) |
| Custom Schedule | Cron-like text input | Conditional | Required if Custom; helper text shows plain-English interpretation |
| Auto-Generate | Toggle | No | Default: Off; when On, generation runs at scheduled time automatically |
| Notify MIS Officer on Generate | Toggle | No | Default: On; sends in-platform notification when report is generated |

**Tab 4 — Preview**

- [Preview Report Structure] button — triggers POST to `/api/v1/mis/builder/preview/` with current template config
- Returns a skeleton PDF outline listing the included sections with placeholder data
- Preview rendered in an iframe (800px tall, scrollable) within the drawer
- Shows section headings, placeholder charts, and dummy data so the Officer can verify layout
- Button shows spinner while generating; preview loads inline
- Note beneath: "This is a structural preview using sample data. The final report uses live data."

**Footer actions:** [Save as Draft] (saves without activation) | [Save & Activate] (saves and sets status to Active) | [Cancel]

Inline validation fires on blur for all fields. Tab navigation disabled until required fields on current tab pass validation. Progress indicator shows which tabs are complete (green checkmark) or incomplete (grey dot).

---

### 6.2 Drawer: `report-template-edit`

**Width:** 680px. Identical tab structure and field spec to `report-template-create` but all fields pre-populated from existing template data. Change audit: shows "Last edited by [name] on [date]" in drawer header.

**Footer actions:** [Save Changes] | [Save as Draft] | [Cancel]

---

### 6.3 Modal: `report-delete-confirm`

**Width:** 420px. Centered overlay.

- **Title:** "Delete Report Template"
- **Body:** "You are about to permanently delete **[Report Name]**. All associated generation history will be unlinked. This cannot be undone."
- **Confirmation input:** Text field with label "Type the report name to confirm:" — [Delete] button remains disabled until input matches report name exactly (case-sensitive).
- **Footer:** [Delete] (destructive red) | [Cancel]

---

### 6.4 Modal: `report-generation-progress`

**Width:** 480px. Triggered when "Generate Now" is clicked on any template row or header button.

**States:**

1. **In Progress state:**
   - Title: "Generating Report…"
   - Body: "Generating **[Report Name]** for [Period]… This may take 30–60 seconds."
   - Spinner animation centred
   - Cannot be dismissed; close button disabled
   - Polls `/api/v1/mis/jobs/[job_id]/status/` every 3 seconds via HTMX

2. **Completed state:**
   - Title: "Report Ready"
   - Body: "**[Report Name]** has been generated successfully."
   - File size shown (e.g. "PDF — 2.4 MB")
   - Buttons: [Download PDF] | [Download XLSX] (whichever formats were configured) | [Send to Recipients] (Role 103 only) | [Close]

3. **Failed state:**
   - Title: "Generation Failed"
   - Body: Error message from job log (truncated to 200 chars)
   - Buttons: [Retry] (Role 103 only) | [View Full Log] | [Close]

---

## 7. Charts

### 7.1 Reports Generated per Month (Bar Chart)

- **Library:** Chart.js 4.x
- **Type:** Grouped bar chart
- **X-axis:** Months (Apr–Mar for current AY or last 12 calendar months)
- **Y-axis:** Count of reports generated
- **Series:** One bar per Report Type (Monthly MIS, Board Report, Custom) — colourblind-safe palette (blue #2563EB, teal #0D9488, amber #D97706)
- **Data source:** `/api/v1/mis/builder/charts/monthly-volume/?ay=2025-26`
- **Interactions:** Hover tooltip shows count per type; click bar filters the Recent Generations Log
- **Export:** PNG download button in chart header
- **Empty state:** "No reports generated yet for this academic year." with chart area showing empty axes
- **Loader:** Grey skeleton rectangle (height 200px) while data fetches

### 7.2 Distribution Reach (Line Chart)

- **Library:** Chart.js 4.x
- **Type:** Line chart
- **X-axis:** Months (last 12)
- **Y-axis:** Count of recipients who opened or downloaded each report
- **Series:** One line per Report Type
- **Note:** Displayed only if email tracking is enabled in group settings. If disabled, shows informational message: "Enable delivery tracking in Group Settings to see recipient engagement."
- **Data source:** `/api/v1/mis/builder/charts/distribution-reach/?months=12`
- **Interactions:** Hover tooltip; click opens recipient engagement drill-down modal
- **Export:** PNG download button
- **Empty state:** "No distribution data available. Enable tracking or send reports to recipients."
- **Loader:** Grey skeleton rectangle (height 200px)

---

## 8. Toast Messages

| Action | Success | Error |
|---|---|---|
| Template created (Save & Activate) | "Report template created and activated." (4s) | "Failed to create template. [reason]" (manual dismiss) |
| Template created (Save as Draft) | "Template saved as draft." (4s) | "Failed to save draft. [reason]" (manual dismiss) |
| Template updated | "Template updated successfully." (4s) | "Failed to update template. [reason]" (manual dismiss) |
| Template deleted | "Report template deleted." (4s) | "Failed to delete template. [reason]" (manual dismiss) |
| Template activated | "Template activated. Scheduling is now live." (4s) | "Failed to activate template." (manual dismiss) |
| Template paused | "Template paused. No auto-generation will occur." (4s) | "Failed to pause template." (manual dismiss) |
| Report generation started | "Report generation started. You will be notified when ready." (4s) | "Failed to start generation job. [reason]" (manual dismiss) |
| Report generation completed | "Report generated successfully. Ready to download." (4s) | — |
| Report generation failed | — | "Report generation failed: [reason]. Check the log for details." (manual dismiss) |
| Report sent to recipients | "Report sent to [N] recipients." (4s) | "Failed to send to some recipients. [N] delivery failures." (manual dismiss) |
| Bulk pause | "[N] templates paused." (4s) | "Bulk pause failed for [N] templates." (manual dismiss) |
| Bulk activate | "[N] templates activated." (4s) | "Bulk activate failed." (manual dismiss) |

---

## 9. Empty States

| Section | Illustration | Heading | Description | CTA |
|---|---|---|---|---|
| Templates Table (no templates) | Blank report icon | "No report templates yet." | "Create your first MIS report template to start generating reports for the Board." | [+ New Report Template] (Role 103 only) |
| Scheduled Queue (none in 30 days) | Calendar with no events icon | "No scheduled reports in the next 30 days." | "Templates with Monthly or Quarterly frequency will appear here." | [Configure Schedule] (Role 103 only) |
| Recent Generations Log (empty) | Document generation icon | "No reports generated yet." | "Use the Generate Now button on any active template to create your first report." | — |
| Chart 7.1 (no data) | Empty bar chart icon | "No generation data for this period." | "Reports generated this academic year will appear here." | — |
| Chart 7.2 (tracking disabled) | Envelope icon | "Distribution tracking is disabled." | "Enable delivery tracking in Group Settings to monitor recipient engagement." | [Open Settings] |

---

## 10. Loader States

| Element | Loader Type | Description |
|---|---|---|
| Templates Table | Skeleton | 5 rows, each row has 8 columns of varying-width grey bars |
| Scheduled Queue | Skeleton | 3 rows |
| Recent Generations Log | Skeleton | 5 rows |
| KPI Summary Bar | Skeleton | 6 card-shaped grey rectangles |
| Chart 7.1 | Skeleton | Single grey rectangle, 200px tall |
| Chart 7.2 | Skeleton | Single grey rectangle, 200px tall |
| Generate Now button (in progress) | Spinner | 16px spinner replaces button text; button disabled |
| Report Preview (Tab 4) | Spinner centred | "Generating preview…" text below spinner |
| Save / Save & Activate buttons | Spinner | 16px spinner in button; button disabled during POST |

---

## 11. Role-Based UI Visibility

| UI Element | Role 102 | Role 103 | Roles 104–107 |
|---|---|---|---|
| "+ New Report Template" button | Hidden | Visible | Hidden |
| "Generate Report" header dropdown | Visible | Visible | Hidden |
| Edit button in table row | Hidden | Visible | Hidden |
| Delete button in table row | Hidden | Visible | Hidden |
| Bulk action toolbar | Hidden | Visible | Hidden |
| "Generate Now" per-row button | Visible | Visible | Hidden |
| "Pause / Activate" per-row button | Hidden | Visible | Hidden |
| "Send to Recipients" button in modal | Hidden | Visible | Hidden |
| "Retry" button in generation modal | Hidden | Visible | Hidden |
| Filter advanced drawer | Visible | Visible | Visible |
| Download buttons (completed reports) | Visible | Visible | Visible |
| Score Weights configuration | Hidden | Hidden | Hidden |

---

## 12. API Endpoints

| Method | Path | Auth | Description | Query Params |
|---|---|---|---|---|
| GET | `/api/v1/mis/builder/templates/` | Roles 102–107 | List all report templates with pagination | `page`, `page_size`, `q` (search), `type`, `status`, `frequency`, `has_recipients` |
| POST | `/api/v1/mis/builder/templates/` | Role 103 | Create a new report template | — |
| GET | `/api/v1/mis/builder/templates/{id}/` | Roles 102–107 | Retrieve single template detail | — |
| PUT | `/api/v1/mis/builder/templates/{id}/` | Role 103 | Full update of template | — |
| PATCH | `/api/v1/mis/builder/templates/{id}/` | Role 103 | Partial update (e.g. status change) | — |
| DELETE | `/api/v1/mis/builder/templates/{id}/` | Role 103 | Delete template | — |
| POST | `/api/v1/mis/builder/templates/{id}/generate/` | Roles 102–103 | Trigger on-demand generation job | — |
| POST | `/api/v1/mis/builder/preview/` | Role 103 | Generate structural preview with sample data | — |
| GET | `/api/v1/mis/jobs/{job_id}/status/` | Roles 102–107 | Poll generation job status | — |
| POST | `/api/v1/mis/jobs/{job_id}/send/` | Role 103 | Send completed report to recipients | — |
| GET | `/api/v1/mis/builder/queue/` | Roles 102–107 | List scheduled jobs in next 30 days | — |
| GET | `/api/v1/mis/builder/log/` | Roles 102–107 | Last 20 generation jobs | — |
| GET | `/api/v1/mis/builder/kpis/` | Roles 102–107 | KPI summary bar data | — |
| GET | `/api/v1/mis/builder/charts/monthly-volume/` | Roles 102–107 | Bar chart data | `ay` (academic year) |
| GET | `/api/v1/mis/builder/charts/distribution-reach/` | Roles 102–107 | Line chart data | `months` |
| GET | `/api/v1/group/contacts/` | Roles 102–107 | Group contacts for recipient typeahead | `q` (search), `role` |

---

## 13. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| Template table search | `input` (300ms debounce via `hx-trigger="input delay:300ms"`) | `hx-get="/api/v1/mis/builder/templates/"` | `#templates-table-body` | `innerHTML` | Sends `q` param |
| Template table pagination | `click` on page button | `hx-get="/api/v1/mis/builder/templates/"` | `#templates-table-body` | `innerHTML` | Sends `page` param |
| Apply advanced filters | `click` on [Apply] in filter drawer | `hx-get="/api/v1/mis/builder/templates/"` | `#templates-table-body` | `innerHTML` | Closes drawer, updates chips |
| Open create drawer | `click` on [+ New Report Template] | `hx-get="/group/mis/builder/drawer/create/"` | `#drawer-container` | `innerHTML` | Slides in; focus trapped |
| Open edit drawer | `click` on [Edit] in row | `hx-get="/group/mis/builder/drawer/edit/{id}/"` | `#drawer-container` | `innerHTML` | Pre-populated fields |
| Delete template | `click` on [Delete] in confirm modal | `hx-delete="/api/v1/mis/builder/templates/{id}/"` | `#templates-table-body` | `outerHTML` | Closes modal; shows toast |
| Generate Now | `click` on [Generate Now] | `hx-post="/api/v1/mis/builder/templates/{id}/generate/"` | `#generation-modal` | `innerHTML` | Opens progress modal |
| Poll generation status | `load` + `every 3s` | `hx-get="/api/v1/mis/jobs/{job_id}/status/"` | `#generation-modal-body` | `innerHTML` | Stops polling on Completed/Failed |
| Scheduled queue load | `load` | `hx-get="/api/v1/mis/builder/queue/"` | `#scheduled-queue-body` | `innerHTML` | On section reveal |
| Recent log load + auto-refresh | `load` + `every 30s` | `hx-get="/api/v1/mis/builder/log/"` | `#recent-log-body` | `innerHTML` | Refreshes if any row In Progress |
| Status toggle (pause/activate) | `click` on status toggle | `hx-patch="/api/v1/mis/builder/templates/{id}/"` | `#row-{id}` | `outerHTML` | Sends `{status: "paused"\|"active"}` |
| Dismiss alert banner | `click` on X | `hx-delete="/group/mis/builder/alerts/{alert_id}/dismiss/"` | `#alert-{alert_id}` | `outerHTML` | Server stores dismissal in session |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
