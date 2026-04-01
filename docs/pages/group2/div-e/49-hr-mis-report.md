# 49 — HR MIS Report

- **URL:** `/group/hr/reports/mis/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Role:** Group HR Director (Role 41, G3)

---

## 1. Purpose

The HR MIS (Management Information System) Report page is the formal monthly reporting interface for the HR function. Every month, the HR Director compiles, reviews, and publishes a structured HR report to the Chairman, Board, and CEO of the group. This report is the primary instrument through which the Board monitors human capital health across the institution — it translates operational HR data into executive-level summaries that inform governance decisions.

The HR MIS report covers the following data sections: Total Staff Strength (current headcount broken down by branch, by role category, and by employment type — permanent vs. contract vs. visiting), Joinings and Exits This Month (new joiners with role and branch; exits with reason — resignation / termination / retirement / contract end), Vacancies (unfilled posts by branch and category, with days vacant), BGV Compliance Rate (% of current staff with verified background checks), POCSO Training Rate (% of staff with valid POCSO certification), Disciplinary Cases Summary (new cases opened, cases closed, cases in progress, outcomes given), Grievances Filed and Resolved (volume, SLA adherence, escalation count), Training Hours Delivered (total CPD hours, branch-wise distribution), and Group Turnover Rate (rolling 12-month figure).

The report builder interface on this page allows the HR Director to select the reporting month and year, choose which data sections to include in the report (all sections included by default), preview the compiled report with live data, edit the narrative commentary sections, and publish to the G5/G4 stakeholder group. Publication triggers an in-app notification to all G4+ users and a system-generated PDF attached to the notification. Once published, the report is locked — changes require the HR Director to create a revised version, which is tracked separately.

This page is also the archive for all past MIS reports. The HR Director can access any previously published report, compare figures month-over-month, and download historical PDFs. A reminder alert fires on the 1st of each month if the previous month's MIS has not yet been generated, and an escalating amber alert fires on the 5th if still unpublished — ensuring the reporting cadence is maintained.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group HR Director | G3 | Full access — Build + Edit + Publish + Archive | Primary operator |
| Group HR Manager | G3 | Read-only — can view generated reports, no build or publish | Reference access |
| Chairman / CEO (G5) | G5 | Read-only — published reports only | Primary report consumers |
| Group Admin (G4) | G4 | Read-only — published reports only | Secondary consumers |
| All other roles | — | No access | Page not rendered |

---

## 3. Page Layout

### 3.1 Breadcrumb

```
Group Portal › HR & Staff › Reports › HR MIS Report
```

### 3.2 Page Header

- **Title:** HR MIS Report
- **Subtitle:** Monthly HR Management Information System — Board and Executive Report
- **Tab Navigation:**
  - **Report Builder** (default — for HR Director only)
  - **Published Reports** (archive view — all roles with access)
- **Primary CTA (Report Builder tab):** `Generate Report` (builds report for selected month)
- **Primary CTA (Published Reports tab):** None (view-only)
- **Secondary CTA:** `Export PDF` (downloads current preview or selected published report)

### 3.3 Alert Banner (conditional)

- **Amber (1st of month):** `MIS Report for [prior month] has not been generated yet. Generate by the 5th.` Action: `Generate Now`
- **Red (after 5th):** `MIS Report for [prior month] is overdue. Board reporting SLA breached.` Action: `Generate Now`
- **Blue:** `MIS Report for [current period] is in draft. Review and publish to distribute to Board.` Action: `Preview`
- **Green:** `MIS Report for [last month] published on [date]. Next report due: [date].`

---

## 4. KPI Summary Bar

(These KPIs describe the MIS report process itself, not HR metrics)

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Report Generated | Status badge for current month: Yes / No | Green if Yes, red if No (past 5th of month) | Switch to Report Builder |
| Last Published Date | Date of most recently published report | Green if within 35 days, amber if 35–45, red if > 45 days ago | Open report in Published tab |
| Pending Approval | Count of generated-but-not-published drafts | Amber if > 0, else grey | Switch to Report Builder |
| Reports Published This Year | Count of published MIS reports in current academic year | Blue always | Switch to Published Reports tab filtered to current AY |
| Current Draft Sections | Count of sections included in current draft | Blue always | No drill-down |
| Avg Report Completion Day | Average day-of-month on which MIS is generated (rolling 6 months) | Green if ≤ 5, amber 6–8, red > 8 | No drill-down |

---

## 5. Main Section — Report Builder (Tab: Report Builder)

The Report Builder is the primary interface on this tab. It replaces the standard table layout.

### 5.1 Report Configuration Panel (top of Builder)

- **Reporting Month:** Month / Year dropdown (defaults to last completed month)
- **Sections to Include:** Checklist with all sections pre-ticked:
  - Staff Strength Summary
  - Joinings & Exits
  - Vacancy Status
  - BGV Compliance
  - POCSO Training Compliance
  - Disciplinary Cases Summary
  - Grievances Summary
  - Training Hours Delivered
  - Turnover Rate
  - HR Director Commentary (free text section)
- **Generate Report** button: Pulls live data for all ticked sections for the selected month

### 5.2 Report Preview Panel (below configuration)

After generation, renders a formatted preview of the full report. Each section renders as a card with:
- Section title
- Key figures in a summary table (pulled from respective operational data)
- Optional narrative commentary box (editable by HR Director — plain textarea, max 500 characters per section)
- Data source note (e.g., "Source: Disciplinary Case Tracker — as of [date]")

Preview matches the final PDF layout closely (WYSIWYG-aligned).

### 5.3 Action Bar (below preview)

- `Save Draft` — saves current report with commentary, status = Draft
- `Preview PDF` — opens PDF preview in new tab
- `Publish to Board` — changes status to Published, triggers notifications, locks report
- `Discard` — deletes draft (confirmation dialog required)

### 5.4 Published Reports Archive (Tab: Published Reports)

Table listing all historical published MIS reports:

| Column | Type |
|---|---|
| Report Period | Text (e.g., "February 2026") |
| Generated Date | Date |
| Published Date | Date |
| Published By | Text (HR Director name) |
| Sections Included | Count |
| Status | Badge (Published / Archived) |
| Actions | Download PDF / View Online |

---

## 6. Drawers

No separate drawers on this page. All interactions occur within the Report Builder panel and archive table directly.

---

## 7. Charts

No standalone charts on this page. Chart data is embedded within the Report Preview as part of the generated report content (e.g., a mini bar chart for staff strength by branch, a turnover trend line). These are rendered server-side into the report preview using a chart-generation library and embedded as images in the PDF export.

---

## 8. Toast Messages

| Trigger | Type | Message |
|---|---|---|
| Report generated | Success | "HR MIS Report for [Month Year] generated. Review and publish when ready." |
| Draft saved | Success | "Draft saved. You can continue editing before publishing." |
| Report published | Success | "MIS Report for [Month Year] published. Board and executive team notified." |
| Report already published | Warning | "A report for [Month Year] is already published. Create a revised version if changes are needed." |
| PDF export ready | Success | "HR MIS Report PDF downloaded." |
| Discard confirmed | Info | "Draft discarded. Report data is still available for re-generation." |
| Data source warning | Warning | "Some data sections have not been updated in the last 7 days. Review before publishing." |
| Server error | Error | "Failed to generate report. Please retry or contact support." |

---

## 9. Empty States

**No published reports in archive (new setup):**
> Icon: document stack
> "No MIS reports have been published yet."
> "Generate the first monthly HR MIS report using the Report Builder tab."
> CTA: `Go to Report Builder`

**Report Builder — no data for selected month:**
> "No HR data found for [Month Year]. Ensure operational data has been entered before generating the report."

---

## 10. Loader States

- Report generation: Full-width loading bar with "Compiling report data from [N] sources..." message and estimated time (typically 5–15 seconds for large groups)
- Preview render: Section cards render progressively (each section appears as data fetches complete)
- PDF preview: Loading spinner in new tab while PDF generates
- Published reports table: Skeleton rows while archive loads
- KPI bar: Individual card shimmer on page load

---

## 11. Role-Based UI Visibility

| UI Element | HR Director | HR Manager | G5 / G4 (Board) |
|---|---|---|---|
| Report Builder tab | Visible and editable | Hidden | Hidden |
| Published Reports tab | Visible | Visible | Visible |
| `Generate Report` button | Visible | Hidden | Hidden |
| `Publish to Board` button | Visible | Hidden | Hidden |
| Commentary fields (edit) | Editable | Read-only (in preview) | Hidden |
| Export PDF button | Visible | Visible (published only) | Visible (published only) |
| Discard Draft button | Visible | Hidden | Hidden |
| Section selector checklist | Visible | Hidden | Hidden |

---

## 12. API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/hr/reports/mis/` | List of published MIS reports (paginated) |
| POST | `/api/hr/reports/mis/generate/` | Generate new MIS report for specified month |
| GET | `/api/hr/reports/mis/{id}/` | Fetch specific report (draft or published) |
| PATCH | `/api/hr/reports/mis/{id}/` | Update draft (save commentary edits) |
| POST | `/api/hr/reports/mis/{id}/publish/` | Publish report to Board |
| DELETE | `/api/hr/reports/mis/{id}/` | Discard draft (soft delete) |
| GET | `/api/hr/reports/mis/{id}/pdf/` | Generate PDF for download |
| GET | `/api/hr/reports/mis/kpis/` | KPI bar data (report process metrics) |

---

## 13. HTMX Patterns

| Interaction | HTMX Attribute | Behaviour |
|---|---|---|
| Tab switch | `hx-get` on tab buttons + `hx-target="#tab-content"` | Loads Report Builder or Archive tab content |
| Generate report | `hx-post` on Generate button + `hx-target="#report-preview"` | Posts month selection, renders report preview HTML |
| Progressive section rendering | `hx-trigger="load"` on each section card | Each section fetches its data independently |
| Save draft | `hx-patch` with commentary data + `hx-target="#save-status"` | Patches draft, shows saved confirmation inline |
| Publish | `hx-post` + `hx-confirm` dialog + `hx-target="#publish-status"` | Confirmation dialog before publish; updates status |
| Published reports table load | `hx-get` on tab activation | Fetches archive list |
| KPI bar refresh | `hx-get` on `#kpi-bar` on page load | Loads report process KPIs |
| Toast | `hx-swap-oob` on `#toast-container` | Out-of-band toast on generate/publish/save |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
