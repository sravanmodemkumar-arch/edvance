# Page 38 — Admission MIS Report

**URL:** `/group/adm/reports/mis/`
**Template:** `portal_base.html`
**App:** `group_admissions`
**Django View:** `AdmissionMISReportView`

---

## 1. Purpose

The Admission MIS (Management Information System) Report is the formal monthly governance document for the Group Admissions function. It is signed off by the Group Admissions Director and submitted to the Chairman, Board members, and CEO as part of the regular management reporting cycle. The report consolidates all key admission activities for the month: enrollment counts by branch and stream, fee collection from new admissions, scholarship approvals and disbursements, demo program performance, admission funnel metrics, counsellor productivity, and upcoming cycle milestones. It is not an operational dashboard — it is an auditable, archivable record of admission performance for each reporting period.

The Coordinator is responsible for compiling the underlying data each month before the Director reviews, annotates, and finalises the report. The page provides a structured data completeness checker that flags any gaps before report generation, preventing the embarrassment of issuing an MIS with missing or placeholder data. Once the Director confirms data completeness, a single action triggers generation of the formatted report. The report is produced in a consistent, branded format suitable for board-level distribution. Once finalised, the report is locked against further changes and stored in the Generated Reports Archive for future reference and audit.

The Distribution List Manager on this page controls who automatically receives each type of MIS report and in what format (PDF email attachment vs secure portal link). The Action Item Tracker ensures that accountability items raised in prior MIS reports — for example, "Director to investigate why Branch X conversion dropped 15%" — are formally tracked to resolution, creating a closed-loop governance mechanism that prevents action items from being forgotten between reporting cycles.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Admissions Director (Role 23) | G3 | Full — generate, review, finalise, distribute, manage distribution list, manage action items | Sign-off authority |
| Group Admission Coordinator (Role 24) | G3 | Compile data, view draft reports, manage action items assigned to them | Cannot finalise or distribute |
| Group CEO | G3 | View finalised reports only | Receives via distribution list |
| Chairman / Board Members | — | View distributed reports only (via emailed secure link) | Not portal users; external recipients |
| Group Analytics Director | G3 | View finalised reports | Read access |
| Group CAO | G3 | View finalised reports | Academic context |
| Group Scholarship Manager (Role 27) | G3 | View scholarship section of finalized reports only | Scoped to scholarship data |

**Enforcement:** `AdmissionMISReportView` uses `@role_required(['admissions_director', 'admission_coordinator', 'ceo', 'analytics_director', 'cao'])`. Report finalisation and distribution actions are additionally gated with `@permission_required('admission.finalise_mis_report')`. Distribution list management requires the `manage_distribution_list` permission. No client-side role checks.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal > Admissions > Reports & Analytics > Admission MIS Report
```

### 3.2 Page Header

| Element | Detail |
|---|---|
| Page title | Admission MIS Report |
| Subtitle | Monthly governance report for Chairman, CEO & Board |
| Header actions | [Generate This Month's Report] [View Archive] [Manage Distribution List] |
| Reporting month selector | Month/year picker — defaults to current month |
| Status badge | Draft / Data Incomplete / Ready to Finalise / Finalised / Distributed |

### 3.3 Alert Banner

| Trigger | Message | Severity |
|---|---|---|
| Current month report not yet generated and today is after 5th of month | "The [Month] MIS report has not been generated yet. Data compilation is overdue." | Warning (amber) |
| Data completeness check has one or more failures | "One or more data sources are incomplete. Resolve all items before generating the MIS." | Critical (red) |
| Report finalized but not yet distributed | "[Month] MIS report is finalized. Distribute to recipients or schedule distribution." | Info (blue) |
| Previous MIS action items overdue | "[N] action items from the previous MIS report are overdue." | Warning (amber) |
| Distribution scheduled for today | "The [Month] MIS report is scheduled for distribution today at [time]." | Info (blue) |

---

## 4. KPI Summary Bar

Refreshes automatically via HTMX every 5 minutes (`hx-trigger="load, every 5m"`).

| Card | Metric | Source | Colour Rule | Drill-down |
|---|---|---|---|---|
| Report Generation Date | Date of latest generated report for selected month (or "Not yet generated") | `MISReport` table | Green if generated · Red if not generated | Opens 5.2 Generated Reports Archive |
| Reporting Month / Year | Selected reporting period | UI context | Neutral | — |
| New Enrollments This Month | Count of enrollments confirmed in reporting month | `Enrollment` table | Green vs prior month trend | Opens 5.1 MIS Generator with enrollment section |
| Scholarship Approvals This Month | Count of scholarship approvals in reporting month | `ScholarshipAward` table | Neutral | Opens scholarship section in report preview |
| Fee Collected (₹) | Sum of fees collected from new admissions in reporting month | `FeeCollection` table | Green if ≥ monthly target · Red if below | Opens fee section in report preview |
| Open Action Items | Count of unresolved action items from all prior MIS reports | `MISActionItem` table | Green 0 · Yellow 1–3 · Red >3 | Opens 5.6 Action Item Tracker |

---

## 5. Sections

### 5.1 MIS Report Generator

Step-by-step form rendered as a wizard (steps indicated via numbered progress bar):

**Step 1 — Select Period**
- Month selector (month/year picker)
- Branch scope: All branches / Select specific branches (multi-select with [Select All] / [Deselect All])

**Step 2 — Choose Sections**
Checklist of report sections to include in this month's report:

| Section | Default | Description |
|---|---|---|
| Enrollment Summary | ✓ | Enrollment by branch, stream, and category |
| Scholarship Summary | ✓ | Approvals, disbursements, pending cases |
| Demo Program Performance | ✓ | Demo attendance, demo-to-enrollment rate |
| Funnel Metrics | ✓ | Stage-wise conversion for the month |
| Counsellor Performance | ✓ | Per-counsellor productivity summary |
| Fee Collection from New Admissions | ✓ | Fee amounts, waivers, scholarships |
| Upcoming Milestones | ✓ | Next 30-day admission calendar events |
| Action Items | ✓ | Previous MIS action items + new ones |
| Executive Summary | ✓ | Auto-generated narrative paragraph |

**Step 3 — Data Completeness Check** (auto-runs; see §5.4)

**Step 4 — Preview**
- [Preview Report] button loads the report in §5.3 preview panel
- Shows estimated page count

**Step 5 — Generate / Finalise**
- [Save as Draft] saves current configuration without finalising
- [Generate & Finalise] generates the PDF, locks the report, and enables distribution
- Director must confirm via modal: "This action will lock the report. Are you sure?"

### 5.2 Generated Reports Archive

Table showing all past MIS reports.

| Column | Description |
|---|---|
| Month | Reporting month/year (e.g., February 2026) |
| Generated By | Staff name who triggered generation |
| Generated On | Date and time of generation |
| Sections Covered | Comma-separated list of sections included |
| Status | Badge: Draft · Finalised · Distributed |
| Actions | [View PDF] [Download] [Redistribute] (Redistribute only for Director) |

Sorting: Most recent first. Pagination: 12 rows per page (one year visible by default).
Click on month opens the report-preview-full drawer with the full rendered report.

### 5.3 Report Preview Panel

Inline HTML preview of the current month's draft or finalised report. The preview panel renders inside the page below the generator, in a bordered frame matching PDF proportions.

Rendered sections (matching selected sections from §5.1):
1. Header: Group logo, report title, reporting month, generation date, Director name
2. Enrollment Summary — table with branch × stream enrollment counts
3. Scholarship Summary — approvals, disbursements, pending, budget consumed
4. Demo Program Performance — demo count, attendance, conversions per branch
5. Funnel Metrics — simplified funnel table for the month
6. Counsellor Performance — top 5 / bottom 5 counsellor summary
7. Fee Collection — fee table per branch with totals
8. Upcoming Milestones — next 30 days from campaign calendar
9. Action Items — table of previous action items (status) + new action items raised
10. Executive Summary — auto-generated paragraph (editable by Director before finalising)

**Director can:** Edit the Executive Summary inline, add annotations/comments to any section (shown as highlighted boxes in the preview), and mark sections as reviewed.

**Status footer** in preview: "Draft — not yet finalised" or "Finalised by [Name] on [Date]".

### 5.4 Data Completeness Checker

Displayed automatically in Step 3 of the generator (§5.1) and also accessible as a standalone panel on the page for the Coordinator to check at any time.

| Data Source | Status | Last Updated | Action |
|---|---|---|---|
| Enrollment records — all branches | ✓ Complete / ✗ Missing | [timestamp] | [Resolve →] |
| Application data — all branches | ✓ Complete / ✗ Missing | [timestamp] | [Resolve →] |
| Attendance / demo records | ✓ Complete / ✗ Partial | [timestamp] | [Resolve →] |
| Fee collection data | ✓ Complete / ✗ Missing | [timestamp] | [Resolve →] |
| Scholarship approvals | ✓ Complete / ✗ Partial | [timestamp] | [Resolve →] |
| Counsellor session logs | ✓ Complete / ✗ Missing | [timestamp] | [Resolve →] |

Status icons: green tick (complete), red cross (missing), amber warning (partial / stale data older than 48h).

[Resolve →] links navigate to the relevant operational page (e.g., Application Pipeline for application data). If all items are green, a banner reads: "All data sources are complete. You may proceed to generate the MIS report."

The [Generate & Finalise] button in §5.1 Step 5 is disabled (greyed out) until all checklist items are green.

### 5.5 Distribution List Manager

Manage who receives each auto-distributed MIS report.

Table of current recipients:

| Column | Description |
|---|---|
| Recipient Name | Full name |
| Role / Title | Role or board position |
| Email | Email address for distribution |
| Format Preference | PDF Email Attachment / Secure Portal Link |
| Report Types | Which report types they receive (Admission MIS / Scholarship MIS / etc.) |
| Active | Toggle (active = included in next distribution) |
| Actions | [Edit] [Remove] |

[Add Recipient] button opens inline form: Name, Title, Email, Format preference, Report type selection.

**Distribution History** sub-section below table: log of past distribution actions — Date, Report Month, Recipients count, Delivery method, Status (Sent / Failed).

### 5.6 Action Item Tracker

Table of action items raised in MIS reports, both historical and current.

| Column | Description |
|---|---|
| Item | Description of the action item |
| Raised In Report | Month/year of the MIS report where the item was raised |
| Assigned To | Staff name |
| Due Date | Target resolution date |
| Status | Badge: Pending · In Progress · Completed · Overdue |
| Actions | [Update Status] [View Detail] |

Filtering: Status filter (All / Pending / Overdue / Completed). Default view: Pending + Overdue items only.

[Add Action Item] button available to Director and Coordinator — allows adding a new action item directly to the current draft report.

Overdue items (past due date, not Completed) shown with red row background.

---

## 6. Drawers & Modals

| ID | Width | Tabs | HTMX Endpoint |
|---|---|---|---|
| `report-preview-full` | 640px | Full Report · Sections · Annotations · History | `GET /api/v1/group/{group_id}/adm/reports/mis/{report_id}/` |
| `distribution-config` | 480px | Recipients · Format Settings · History | `GET /api/v1/group/{group_id}/adm/reports/mis/distribution/` |
| `action-item-detail` | 400px | Details · Comments · Status History | `GET /api/v1/group/{group_id}/adm/reports/mis/action-items/{item_id}/` |
| `finalise-confirm-modal` | 440px (modal) | — (single confirmation panel) | `POST /api/v1/group/{group_id}/adm/reports/mis/{report_id}/finalise/` |
| `distribute-confirm-modal` | 440px (modal) | — (single confirmation panel) | `POST /api/v1/group/{group_id}/adm/reports/mis/{report_id}/distribute/` |

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Report saved as draft | "MIS report saved as draft for [Month Year]." | Success | 3s |
| Report finalised | "[Month Year] MIS report finalised and locked." | Success | 4s |
| Report distribution triggered | "MIS report distributed to [N] recipients." | Success | 4s |
| Distribution failed for some recipients | "Report distributed but failed for [N] recipients. Check distribution log." | Warning | 6s |
| Data completeness check failed | "Data completeness check failed. Resolve missing sources before generating." | Error | 6s |
| PDF download started | "Downloading MIS report PDF…" | Info | 3s |
| Action item status updated | "Action item updated to [status]." | Success | 3s |
| Recipient added to distribution list | "[Name] added to distribution list." | Success | 3s |
| Recipient removed | "[Name] removed from distribution list." | Info | 3s |
| Executive summary saved | "Executive summary saved." | Success | 2s |

---

## 8. Empty States

| Condition | Illustration | Heading | Description | CTA |
|---|---|---|---|---|
| No reports in archive | Document stack icon (empty) | "No Reports Generated Yet" | "No MIS reports have been generated for this group." | [Generate This Month's Report] |
| Action item tracker empty (all resolved) | Checkmark circle icon | "All Action Items Resolved" | "There are no pending action items from previous MIS reports. Well done." | — |
| Distribution list empty | Envelope icon with plus | "No Recipients Configured" | "No distribution recipients have been set up. Add recipients to enable auto-distribution." | [Add Recipient] |
| Data completeness: all items missing | Warning triangle | "No Data Available" | "No admission data has been synced for the selected month. Check data pipeline." | [Contact MIS Team] |
| Report preview: draft not yet generated | Document outline icon | "No Preview Available" | "Select report parameters and complete the data check to preview the report." | — |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | Full-page skeleton: KPI shimmer + generator form skeleton + archive table skeletons |
| KPI bar auto-refresh (every 5m) | Per-card inline spinner; retained last values |
| Data completeness check runs | Each checklist row shows spinner while checking; resolves to tick or cross |
| Report preview loads | Framed preview area shows full-height shimmer animation |
| Archive table pagination | Table body skeleton rows (4 rows) |
| Drawer open | Drawer content full-height skeleton + tab bar shimmer |
| PDF generation | Button text changes to "Generating…" with spinner; button disabled |
| Distribution trigger | Button changes to "Distributing…" with spinner |

---

## 10. Role-Based UI Visibility

> All UI visibility decisions made server-side in Django template. No client-side JS role checks.

| UI Element | Director (23) | Coordinator (24) | CEO | Analytics Director | Scholarship Manager (27) |
|---|---|---|---|---|---|
| MIS Generator — full wizard | Visible | Visible (Steps 1–4 only; Step 5 shows [Save as Draft] only) | Hidden | Hidden | Hidden |
| [Generate & Finalise] button | Visible | Hidden | Hidden | Hidden | Hidden |
| [Redistribute] in archive | Visible | Hidden | Hidden | Hidden | Hidden |
| Report preview — Edit Executive Summary | Visible | Hidden | Hidden | Hidden | Hidden |
| Distribution List Manager | Visible | Hidden | Hidden | Hidden | Hidden |
| Action Item Tracker — [Add Action Item] | Visible | Visible | Hidden | Hidden | Hidden |
| Action Item Tracker — [Update Status] | Visible | Visible (own items) | Hidden | Hidden | Hidden |
| Generated Reports Archive — view all | Visible | Visible | Finalised only | Finalised only | Scholarship section only |
| Data Completeness Checker | Visible | Visible | Hidden | Hidden | Hidden |
| Finalise Confirm Modal trigger | Visible | Hidden | Hidden | Hidden | Hidden |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/adm/reports/mis/` | JWT | List all MIS reports |
| GET | `/api/v1/group/{group_id}/adm/reports/mis/kpi/` | JWT | KPI summary bar data |
| POST | `/api/v1/group/{group_id}/adm/reports/mis/` | JWT | Create a new MIS report draft |
| GET | `/api/v1/group/{group_id}/adm/reports/mis/{report_id}/` | JWT | Fetch full report data (preview) |
| PATCH | `/api/v1/group/{group_id}/adm/reports/mis/{report_id}/` | JWT | Update draft (executive summary, annotations) |
| POST | `/api/v1/group/{group_id}/adm/reports/mis/{report_id}/finalise/` | JWT | Finalise and lock report (Director only) |
| POST | `/api/v1/group/{group_id}/adm/reports/mis/{report_id}/distribute/` | JWT | Trigger distribution to recipients (Director only) |
| GET | `/api/v1/group/{group_id}/adm/reports/mis/{report_id}/export/pdf/` | JWT | Download report PDF |
| GET | `/api/v1/group/{group_id}/adm/reports/mis/completeness/` | JWT | Run data completeness check for selected month/branches |
| GET | `/api/v1/group/{group_id}/adm/reports/mis/distribution/` | JWT | Get distribution list |
| POST | `/api/v1/group/{group_id}/adm/reports/mis/distribution/` | JWT | Add distribution recipient |
| PATCH | `/api/v1/group/{group_id}/adm/reports/mis/distribution/{recipient_id}/` | JWT | Update recipient (format, active status) |
| DELETE | `/api/v1/group/{group_id}/adm/reports/mis/distribution/{recipient_id}/` | JWT | Remove recipient |
| GET | `/api/v1/group/{group_id}/adm/reports/mis/action-items/` | JWT | List all action items |
| POST | `/api/v1/group/{group_id}/adm/reports/mis/action-items/` | JWT | Create new action item |
| PATCH | `/api/v1/group/{group_id}/adm/reports/mis/action-items/{item_id}/` | JWT | Update action item status |
| GET | `/api/v1/group/{group_id}/adm/reports/mis/action-items/{item_id}/` | JWT | Action item detail for drawer |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| KPI bar auto-refresh | `load, every 5m` | `GET /api/v1/group/{group_id}/adm/reports/mis/kpi/` | `#mis-kpi-bar` | `innerHTML` |
| Generator — advance step | `click` on [Next Step] | `GET /group/adm/reports/mis/generator/?step=N&…` | `#generator-step-panel` | `innerHTML` |
| Data completeness check run | `click` on [Run Check] or auto on Step 3 load | `GET /api/v1/group/{group_id}/adm/reports/mis/completeness/?month=…` | `#completeness-checklist` | `innerHTML` |
| Load report preview | `click` on [Preview Report] | `GET /api/v1/group/{group_id}/adm/reports/mis/{report_id}/` | `#report-preview-panel` | `innerHTML` |
| Archive table pagination | `click` on page control | `GET /api/v1/group/{group_id}/adm/reports/mis/?page=N` | `#archive-table-body` | `innerHTML` |
| Open report-preview-full drawer | `click` on report month row | `GET /api/v1/group/{group_id}/adm/reports/mis/{report_id}/` | `#drawer-content` | `innerHTML` |
| Open distribution-config drawer | `click` on [Manage Distribution List] | `GET /api/v1/group/{group_id}/adm/reports/mis/distribution/` | `#drawer-content` | `innerHTML` |
| Open action-item-detail drawer | `click` on [View Detail] | `GET /api/v1/group/{group_id}/adm/reports/mis/action-items/{item_id}/` | `#drawer-content` | `innerHTML` |
| Drawer tab switch | `click` on drawer tab | `GET /group/adm/reports/mis/drawer-tab/?tab=…&id=…` | `#drawer-tab-content` | `innerHTML` |
| Action item status update | `change` on status dropdown | `PATCH /api/v1/group/{group_id}/adm/reports/mis/action-items/{item_id}/` | `#action-item-row-{item_id}` | `outerHTML` |
| Finalise confirm modal submit | `click` on [Confirm Finalise] | `POST /api/v1/group/{group_id}/adm/reports/mis/{report_id}/finalise/` | `#mis-status-badge` | `outerHTML` |
| Save executive summary | `blur` on executive summary textarea (or explicit Save button) | `PATCH /api/v1/group/{group_id}/adm/reports/mis/{report_id}/` | `#exec-summary-status` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
