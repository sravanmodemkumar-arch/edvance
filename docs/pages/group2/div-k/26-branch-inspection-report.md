# 26 — Branch Inspection Report

> **URL:** `/group/welfare/safety-audit/inspections/`
> **File:** `26-branch-inspection-report.md`
> **Template:** `portal_base.html`
> **Priority:** P1
> **Role:** Group Safety Audit Officer (Role 96, G1)

---

## 1. Purpose

Repository of all safety inspection reports for all branches. Every inspection visit produces a structured, evidence-based report that serves as the formal, legally defensible record of the branch's safety condition at the time of inspection.

Each inspection report contains:
- Overall safety score (0–100) — weighted average of per-category scores
- Per-category scores for each of the 8 inspection categories
- Full checklist findings — each checklist item marked as Compliant / Non-Compliant / Partial / Not Applicable, with inspector notes
- Photographs as evidence (linked to specific checklist items)
- Non-compliance items flagged and extracted to the non-compliance tracker (page 27) on report submission
- Corrective actions recommended
- Inspector's formal sign-off (digital signature)

**Immutability rule:** Inspection reports are immutable once signed and submitted. Errors or newly discovered issues require a new supplementary inspection report. The "submitted" state is enforced server-side — PATCH is rejected for submitted reports. This ensures audit integrity.

The Group Safety Audit Officer uses this repository as the evidence base for:
- The annual safety compliance report submitted to the COO and Chairman
- Non-compliance tracking (page 27)
- Branch-to-branch safety benchmarking
- Trend analysis for the 5-year safety score trajectory

Branch principals receive an automatic notification (with a read-only PDF copy of the report) upon submission.

Scale: 20–50 branches × 1 full audit per year = 20–50 inspection reports per year minimum, plus targeted and surprise visit reports (40–200 total per year).

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Safety Audit Officer | G1 | Read all + create report + submit | Primary owner; cannot edit once submitted |
| Group COO | G4 | Read all reports; receive annual compliance summary | No create; no edit |
| Branch Principal | Branch | Read own branch reports (submitted only; not drafts) | Receives PDF on submission; acknowledges report in portal |
| Group Chairman / CEO | G5 | Read — annual compliance report summary | No individual report detail; PDF only |
| All other roles | — | No access | — |

> **Access enforcement:** `@require_role('safety_audit_officer', 'coo', 'branch_principal', 'chairman')`. Branch Principal sees only `status=submitted` reports for their own branch. Draft reports are Safety Audit Officer-only until submitted.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Welfare & Safety  ›  Safety Audit  ›  Branch Inspection Reports
```

### 3.2 Page Header
- **Title:** `Branch Inspection Reports`
- **Subtitle:** `[Academic Year] · [N] Reports Submitted · Avg Safety Score: [X]/100 · [N] Branches Below 70`
- **Right controls:** `+ New Inspection Report` · `Advanced Filters` · `Export CSV` · `Generate Annual Compliance Report` (Safety Audit Officer + COO)

### 3.3 Alert Banner

| Condition | Banner Text | Severity |
|---|---|---|
| Branch report pending acknowledgment > 7 days | "[N] branches have not acknowledged their inspection report in over 7 days." | Amber |
| Branch below safety score 50 | "[N] branches scored below 50/100 on their latest inspection. Immediate corrective action required." | Red |
| Critical non-compliances open > 30 days | "[N] critical non-compliance items from inspection reports are overdue (> 30 days without resolution)." | Red |
| Annual compliance report due | "The Annual Safety Compliance Report is due in [N] days. [N] branch reports are still missing." | Amber |

---

## 4. KPI Summary Bar

Eight cards in a responsive 4×2 grid. Metrics are filtered by the currently selected Academic Year and Branch filters.

| # | Card | Metric | Colour Rule |
|---|---|---|---|
| 1 | Reports Submitted This Year | Count of reports with Status = Submitted or beyond | Blue always |
| 2 | Average Safety Score | Mean overall score across all submitted reports for selected filters | Green ≥ 80 · Yellow 60–79 · Red < 60 |
| 3 | Branches Below 70 Score | Count of branches whose latest submitted report has overall score < 70 | Red > 3 · Yellow 1–3 · Green = 0 |
| 4 | Critical Non-Compliances Open | Count of critical NC items from all reports with status ≠ resolved (sourced from NC tracker) | Red > 0 · Green = 0 |
| 5 | Reports Pending Acknowledgment | Count of submitted reports not yet acknowledged by branch principal | Red > 5 · Yellow 1–5 · Green = 0 |
| 6 | Full Audit Reports | Count of Full Audit reports submitted this year | Blue always |
| 7 | Safety Score by Branch | Mini horizontal bar chart — all branches, score bar (0–100) | Bars coloured: ≥ 80 green · 60–79 yellow · < 60 red |
| 8 | Compliance Trend (5 years) | Mini line chart — group avg safety score per year for last 5 years | Visual only |

---

## 5. Main Table — Inspection Reports

### 5.1 Search
Full-text search on: Report ID, Branch Name, Inspector Name. Debounce 300 ms, minimum 2 characters.

### 5.2 Advanced Filters

| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Inspection Category | Checkbox | Fire · Building · Electrical · Playground · Hostel · Transport · Food · Lab · Full Audit |
| Date Range | Date picker | Inspection date From – To |
| Score Range | Dual-handle range slider | 0–100 |
| Status | Checkbox | Draft · Submitted · Acknowledged by Branch · Corrective Actions Due · Closed |
| Critical Items | Radio | All · Has Critical Items · No Critical Items |
| Inspector | Single-select | All inspectors |
| Academic Year | Single-select | Current + 4 prior years |

### 5.3 Table Columns

| Column | Sortable | Notes |
|---|---|---|
| Report ID | ✅ | System-generated (e.g., RPT-2026-00041) |
| Branch | ✅ | |
| Category | ✅ | Tag(s) |
| Inspection Date | ✅ | DD-MMM-YYYY |
| Inspector | ✅ | Primary inspector name |
| Overall Score | ✅ | "78 / 100" with score bar (colour: ≥ 80 green · 60–79 yellow · < 60 red) |
| Fire Score | ✅ | /100 |
| Building Score | ✅ | /100 |
| Electrical Score | ✅ | /100 |
| Other Scores | ❌ | Collapsed into "More Scores" expandable inline panel to keep table width manageable |
| Non-Compliances | ✅ | Count; link opens NC tracker filtered to this report |
| Critical Items | ✅ | Count; red badge if > 0 |
| Status | ✅ | Draft (grey) · Submitted (blue) · Acknowledged (green) · Corrective Actions Due (amber) · Closed (dark grey) badge |
| Actions | ❌ | View · Edit (Draft only) · Submit · Acknowledge (Branch Principal) |

**Default sort:** Inspection Date descending, then Overall Score ascending (lowest-scoring first within same date).
**Pagination:** Server-side · 25 rows/page.

### 5.4 Charts Panel (collapsible, above table)

- **Bar chart:** Overall safety score per branch, current academic year (sorted ascending by score — worst first). Each bar coloured by score band.
- **Trend line:** Group average safety score per year for past 5 years. Plotted as a single line with data point markers.

---

## 6. Drawers / Modals

### 6.1 Drawer — `inspection-report-detail` (800px, right side)

Triggered by **View** in Actions column. The widest drawer in the system — required to display the full checklist.

**Header:** Report ID · Branch · Category · Score badge · Status badge

**Tabs:**

#### Tab 1 — Summary
| Field | Notes |
|---|---|
| Report ID | Read-only |
| Inspection Date | Read-only |
| Inspector(s) | Names + qualifications |
| Inspection Type | Scheduled / Surprise / Targeted |
| Branch | Name + address |
| Linked Inspection Plan | Link to planner record (page 25) |
| Overall Score | Large score badge (0–100) with colour |
| Per-Category Scores | Score table: Category · Score · Non-Compliances · Critical Items |
| Executive Summary | Inspector's overall narrative (free text) |
| Key Concerns | Bulleted list of top 3–5 most significant findings |
| Recommended Priority Actions | Numbered list |
| Status | Badge + status history compact timeline |

#### Tab 2 — Checklist
Full structured checklist for the inspection category. Loaded from the checklist template assigned at the planning stage.

**Structure:**
- One section per category (Fire Safety, Building Safety, etc.)
- Each section is a collapsible accordion panel
- Each panel contains a table of checklist items

| Column | Notes |
|---|---|
| Item # | Sequential within category |
| Checklist Item Description | e.g., "Fire extinguishers available in each classroom (1 per room)" |
| Compliance Status | Compliant (green) · Non-Compliant (red) · Partial (amber) · N/A (grey) badge |
| Inspector Notes | Free text note for this item |
| Photos | Camera icon (count) — opens photo gallery for this item |
| NC Created | Link to NC record if Non-Compliant or Partial (shown only in submitted reports) |

Section header shows: category name · total items · compliant count · non-compliant count · partial count · category score.

**Checklist template sizes by category:**
- Fire Safety: 25 items
- Building Safety: 20 items
- Electrical Safety: 18 items
- Playground & Sports: 15 items
- Hostel Safety: 20 items
- Transport Yard: 22 items
- Food Safety: 18 items
- Lab Safety: 16 items

#### Tab 3 — Non-Compliances
Extracted list of all Non-Compliant and Partial items, sorted by severity (Critical → High → Medium → Low).

| Column | Notes |
|---|---|
| NC ID | Link to non-compliance tracker record (page 27) |
| Category | |
| Item Description | |
| Severity | Critical (red) · High (orange) · Medium (amber) · Low (grey) badge |
| Corrective Action Required | |
| Responsible Party | |
| Target Resolution Date | |
| Current Status | Badge (from NC tracker — live sync) |

**Footer:** `Open All NCs in Tracker` button — opens page 27 pre-filtered to this report ID.

#### Tab 4 — Photographs
Image gallery organised by checklist category. Each photo:
- Thumbnail in a responsive grid (3 columns)
- Caption: checklist item it is linked to
- Click: opens full-size lightbox
- Each photo shows: filename, upload timestamp, linked item reference

**Upload note:** Photos are uploaded during report creation (Tab 2 item-level) and are associated with specific checklist items. No standalone photo upload is available in this tab — this tab is view-only for submitted reports.

#### Tab 5 — Corrective Actions
Formal corrective action recommendations compiled from the non-compliances.

| Column | Notes |
|---|---|
| Priority | 1 (highest) to N |
| Category | |
| Corrective Action Required | Free text description |
| Recommended By | Inspector name |
| Timeline | Immediate / 30 Days / 60 Days / 90 Days |
| Owner | Branch role responsible |
| Status | Open / In Progress / Resolved (synced from NC tracker) |

#### Tab 6 — Sign-off
| Field | Notes |
|---|---|
| Inspector Name | Read-only |
| Inspector Qualification | Read-only |
| Sign-off Declaration | *"I certify that this inspection was conducted on the date stated, that all findings are accurate to the best of my knowledge, and that the recommendations reflect genuine safety concerns observed during the inspection."* |
| Digital Signature | Inspector's initials + timestamp at submission |
| Report Submitted On | Timestamp |
| Branch Acknowledgment | Name + role + timestamp (when Branch Principal acknowledges) |
| Acknowledgment Note | Branch Principal's free-text response (optional) |

**Immutability notice (shown on submitted reports):** *"This report was submitted on [date]. Submitted reports are immutable. If corrections are required, please create a supplementary inspection report."*

---

### 6.2 Drawer — `create-inspection-report` (720px, right side)

Triggered by **+ New Inspection Report** button. Begins a new inspection report from a completed inspection plan.

**Step 1 — Link to Plan:**
| Field | Type | Validation |
|---|---|---|
| Inspection Plan | Single-select (search by plan ID, branch, date — shows only Confirmed and Completed plans without a submitted report) | Required |

On selecting the plan, the following fields are auto-populated:
- Branch, Category, Inspection Date, Inspector(s), Checklist Version

The Inspection Date field is editable (actual inspection date may differ from planned date by ≤ 7 days).

**Step 2 — Checklist Completion:**

The checklist template for the selected category is loaded. The inspector completes each item:

| Per-item Fields | Type | Validation |
|---|---|---|
| Compliance Status | Radio: Compliant · Non-Compliant · Partial · N/A | Required for each item |
| Inspector Notes | Textarea (max 500 chars) | Required if Non-Compliant or Partial |
| Photo Upload | File input (JPEG/PNG, max 5MB per photo, max 3 photos per item) | Optional for Compliant; required for Non-Compliant |

The checklist is displayed as a full accordion (same structure as the detail drawer's Checklist tab). Items are saved progressively — each item is saved on blur via HTMX to prevent data loss.

**Step 3 — Executive Summary:**
| Field | Type | Validation |
|---|---|---|
| Executive Summary | Textarea (max 3,000 chars) | Required |
| Key Concerns | Textarea — numbered list (max 2,000 chars) | Required |
| Priority Recommended Actions | Textarea — numbered list (max 2,000 chars) | Required |

**Step 4 — Non-Compliance Severity Assignment:**

For each Non-Compliant or Partial item, the inspector assigns:

| Field | Type | Validation |
|---|---|---|
| Severity | Radio: Critical · High · Medium · Low | Required |
| Corrective Action Description | Textarea (max 500 chars) | Required |
| Recommended Timeline | Radio: Immediate · 30 Days · 60 Days · 90 Days | Required |
| Responsible Party | Single-select: Branch Principal / Maintenance Team / IT / Kitchen Staff / Transport Team / Other | Required |

**Score calculation (automatic):** Overall score and per-category scores are calculated server-side on save: (Compliant items + 0.5 × Partial items) / Total applicable items × 100.

**Footer (all steps):** `Save as Draft` · `Previous Step` (Step 2–4) · `Next Step` (Step 1–3) · `Submit Report` (Step 4 only)

**Submit Report action:** Opens the `submit-report` confirmation modal.

**Validation for submission:**
- All checklist items must have a status (no blank items)
- All Non-Compliant and Partial items must have notes and severity assigned
- Executive Summary, Key Concerns, and Priority Actions must be completed
- At least one photo required for each Non-Compliant item (enforced before submit)

---

### 6.3 Modal — `submit-report` (400px, centred)

Triggered by **Submit Report** in the create drawer or **Submit** in Actions column (for Draft reports).

| Field | Notes |
|---|---|
| Report ID | Read-only |
| Branch | Read-only |
| Overall Score | Read-only — score displayed prominently |
| Non-Compliances Summary | Read-only: "X critical · Y high · Z medium · W low" |
| Declaration Checkbox | "I confirm the accuracy of this report and authorise its submission." — required |

**Footer:** `Cancel` · `Submit Report`

**On submit:**
- Report status updated to Submitted; immutable flag set
- Branch Principal notified (push notification + email) with PDF copy attached
- All Non-Compliant and Partial items auto-extracted to non-compliance tracker (page 27) with assigned severity, timeline, and responsible party
- Toast fires: *"Report [ID] submitted. Branch Principal notified. [N] non-compliance records created."*

---

## 7. Toast Messages

| Action | Toast Text | Type |
|---|---|---|
| Report saved as draft | "Inspection report [ID] saved as Draft." | Success |
| Checklist item saved | "Item saved." | Success (brief, 1.5 s) |
| Report submitted | "Report [ID] submitted. Branch Principal notified. [N] non-compliance records created." | Success |
| Branch acknowledgment recorded | "Report [ID] acknowledged by [Branch Principal name] at [Branch]." | Success |
| Photo uploaded | "Photo uploaded and linked to checklist item." | Success |
| Photo upload failed | "Photo upload failed. File must be JPEG or PNG under 5 MB." | Error |
| Submission blocked — incomplete checklist | "Cannot submit: [N] checklist items have no compliance status. Complete the checklist." | Error |
| Submission blocked — NC without photo | "Cannot submit: [N] non-compliant items require at least one photograph." | Error |
| Edit blocked — report submitted | "Submitted reports cannot be edited. Create a supplementary inspection report." | Error |
| Export triggered | "Export is being prepared." | Info |
| Annual compliance report generated | "Annual Safety Compliance Report is ready for download." | Success |

---

## 8. Empty States

| Context | Heading | Sub-text | Action |
|---|---|---|---|
| No reports for current filters | "No inspection reports match the current filters." | "Try adjusting or clearing your filters." | `Clear Filters` button |
| No reports this year | "No inspection reports submitted for this academic year." | "Begin by creating a report from a completed inspection plan." | `+ New Inspection Report` button |
| Checklist tab — plan not linked | "No checklist loaded." | "Link this report to an inspection plan to load the appropriate checklist template." | Link plan field |
| Photos tab — no photos | "No photographs attached to this report." | "Photographs are attached at the checklist item level during report creation." | — |
| NCs tab — no non-compliances | "No non-compliance items." | "This inspection found full compliance across all checklist items." | — |
| Corrective Actions tab — all resolved | "All corrective actions resolved." | "All items from this inspection have been resolved and verified." | — |

---

## 9. Loader States

| Context | Loader Behaviour |
|---|---|
| Initial page load | Full-page skeleton: 8 KPI cards + 2 chart placeholders + table (10 grey rows × 12 columns) |
| Filter / search apply | Table body spinner overlay; KPI + charts refresh after |
| Report detail drawer open | Drawer skeleton: tab bar + summary field blocks (8 grey rows) |
| Checklist tab load | Accordion skeleton: 8 grey category headers with 3-row grey item placeholders per category |
| Checklist item save (per item) | Inline micro-spinner on the item row during save; resolves to saved state in < 500 ms |
| Photo gallery load | Grid skeleton: 6 grey thumbnail rectangles |
| Photo lightbox open | Spinner inside lightbox overlay for 300 ms |
| NC tab load | Table skeleton (5 rows × 7 columns) |
| Submit modal — processing | Modal footer spinner + "Processing submission…" label; button disabled |
| Annual compliance report generation | Progress bar in page header area: "Compiling annual report…" |

---

## 10. Role-Based UI Visibility

| UI Element | Safety Audit Officer | COO | Branch Principal | Chairman |
|---|---|---|---|---|
| Full cross-branch report list | ✅ | ✅ | Own branch, submitted only | ❌ |
| Draft reports visible | ✅ | ❌ | ❌ | ❌ |
| + New Inspection Report button | ✅ | ❌ | ❌ | ❌ |
| Submit button | ✅ | ❌ | ❌ | ❌ |
| Acknowledge button | ❌ | ❌ | ✅ (own branch, submitted reports) | ❌ |
| Checklist tab (full) | ✅ | ✅ | ✅ (read-only) | ❌ |
| Photos tab | ✅ | ✅ | ✅ (read-only) | ❌ |
| NC tab | ✅ | ✅ | ✅ (read-only) | ❌ |
| Sign-off tab | ✅ | ✅ | ✅ (read-only + acknowledge) | ❌ |
| Score data (KPI + columns) | ✅ | ✅ | Own branch | Summary % only |
| Export CSV | ✅ | ✅ | ❌ | ❌ |
| Generate Annual Compliance Report | ✅ | ✅ | ❌ | Receives PDF via notification |
| Alert banners | ✅ | ✅ | Own branch | ❌ |
| Chart panel (bar + trend line) | ✅ | ✅ | Own branch | ❌ |

---

## 11. API Endpoints

### Base URL: `/api/v1/group/{group_id}/welfare/safety/reports/`

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/welfare/safety/reports/` | List inspection reports (paginated, filtered, role-scoped) | JWT + role check |
| POST | `/api/v1/group/{group_id}/welfare/safety/reports/` | Create new inspection report (Draft) | Safety Audit Officer |
| GET | `/api/v1/group/{group_id}/welfare/safety/reports/{report_id}/` | Retrieve report detail | JWT + role check |
| PATCH | `/api/v1/group/{group_id}/welfare/safety/reports/{report_id}/` | Update draft report fields | Safety Audit Officer (Draft only — 422 if submitted) |
| POST | `/api/v1/group/{group_id}/welfare/safety/reports/{report_id}/checklist/{item_id}/` | Save individual checklist item (progressive save) | Safety Audit Officer |
| POST | `/api/v1/group/{group_id}/welfare/safety/reports/{report_id}/photos/` | Upload photo linked to checklist item | Safety Audit Officer |
| DELETE | `/api/v1/group/{group_id}/welfare/safety/reports/{report_id}/photos/{photo_id}/` | Delete photo (Draft only) | Safety Audit Officer |
| POST | `/api/v1/group/{group_id}/welfare/safety/reports/{report_id}/submit/` | Submit report (sets immutable flag, notifies branch) | Safety Audit Officer |
| POST | `/api/v1/group/{group_id}/welfare/safety/reports/{report_id}/acknowledge/` | Branch acknowledgment | Branch Principal |
| GET | `/api/v1/group/{group_id}/welfare/safety/reports/kpi/` | KPI summary bar | JWT + role check |
| GET | `/api/v1/group/{group_id}/welfare/safety/reports/charts/` | Bar + trend line chart data | JWT + role check |
| GET | `/api/v1/group/{group_id}/welfare/safety/reports/alerts/` | Active alert conditions | JWT + role check |
| GET | `/api/v1/group/{group_id}/welfare/safety/reports/export/` | Export CSV | Safety Audit Officer / COO |
| POST | `/api/v1/group/{group_id}/welfare/safety/reports/annual-report/generate/` | Async annual compliance report PDF | Safety Audit Officer / COO |
| GET | `/api/v1/group/{group_id}/welfare/safety/reports/annual-report/{task_id}/status/` | Poll annual report generation status | Safety Audit Officer / COO |
| GET | `/api/v1/group/{group_id}/welfare/safety/reports/annual-report/{task_id}/download/` | Download annual report PDF | Safety Audit Officer / COO |

**Query parameters for list endpoint:**

| Parameter | Type | Description |
|---|---|---|
| `branch` | int[] | Filter by branch ID(s) |
| `category` | str[] | Category slugs |
| `date_from` | date | Inspection date range start |
| `date_to` | date | Inspection date range end |
| `score_min` | int | Minimum overall score (0–100) |
| `score_max` | int | Maximum overall score (0–100) |
| `status` | str[] | `draft`, `submitted`, `acknowledged`, `corrective_due`, `closed` |
| `has_critical_items` | bool | Filter by presence of critical NC items |
| `inspector` | int | Inspector ID |
| `academic_year` | str | e.g., `2025-26` |
| `page` | int | Page number |
| `page_size` | int | Default 25, max 100 |
| `search` | str | Report ID, branch, inspector name |

---

## 12. HTMX Patterns

| Interaction | HTMX Attributes | Behaviour |
|---|---|---|
| Search input | `hx-get="/api/.../reports/"` `hx-trigger="keyup changed delay:300ms"` `hx-target="#reports-table-body"` `hx-include="#filter-form"` | Table body replaced |
| Filter apply | `hx-get="/api/.../reports/"` `hx-trigger="change"` `hx-target="#reports-table-body"` `hx-include="#filter-form"` | Table + KPI + charts refreshed |
| Pagination | `hx-get="/api/.../reports/?page={n}"` `hx-target="#reports-table-body"` `hx-push-url="true"` | Page swap |
| Report detail drawer open | `hx-get="/api/.../reports/{report_id}/"` `hx-target="#drawer-container"` `hx-trigger="click"` | Drawer slides in; Summary tab default |
| Drawer tab switch | `hx-get="/api/.../reports/{report_id}/?tab={tab_slug}"` `hx-target="#drawer-tab-content"` | Tab content swapped |
| Checklist tab load | `hx-get="/api/.../reports/{report_id}/?tab=checklist"` `hx-target="#drawer-tab-content"` `hx-trigger="click[tab='checklist']"` | Accordion checklist loaded |
| Checklist item progressive save | `hx-post="/api/.../reports/{report_id}/checklist/{item_id}/"` `hx-trigger="change"` `hx-target="#checklist-item-status-{item_id}"` `hx-swap="outerHTML"` | Item status saved; micro-feedback icon shown |
| Photo upload | `hx-post="/api/.../reports/{report_id}/photos/"` `hx-encoding="multipart/form-data"` `hx-target="#photo-gallery-{item_id}"` `hx-swap="beforeend"` | Thumbnail appended to gallery |
| NC tab live status sync | `hx-get="/api/.../reports/{report_id}/?tab=non_compliances"` `hx-trigger="load"` `hx-target="#nc-tab-content"` | NC statuses synced live from NC tracker |
| Submit report modal open | `hx-get="/api/.../reports/{report_id}/submit-preview/"` `hx-target="#modal-container"` `hx-trigger="click"` | Modal populated with score + NC summary |
| Submit report confirm | `hx-post="/api/.../reports/{report_id}/submit/"` `hx-target="#report-row-{report_id}"` `hx-swap="outerHTML"` | Row status updated; drawer closes; toast fires |
| Branch acknowledgment | `hx-post="/api/.../reports/{report_id}/acknowledge/"` `hx-target="#report-row-{report_id}"` `hx-swap="outerHTML"` | Row status updated to Acknowledged |
| KPI bar refresh | `hx-get="/api/.../reports/kpi/"` `hx-trigger="load, filterApplied from:body"` `hx-target="#kpi-bar"` | On load and post-filter |
| Chart panel refresh | `hx-get="/api/.../reports/charts/"` `hx-trigger="load, filterApplied from:body"` `hx-target="#chart-panel"` | Charts updated |
| Alert banner load | `hx-get="/api/.../reports/alerts/"` `hx-trigger="load"` `hx-target="#alert-banner"` | Conditional banner |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
