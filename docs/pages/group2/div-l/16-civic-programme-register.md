# 16 — Civic Programme Register

> **URL:** `/group/nss/civic/`
> **File:** `16-civic-programme-register.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Roles:** Group NSS/NCC Coordinator (Role 100, G3) — full; Group Cultural Activities Head (Role 99, G3) — view

---

## 1. Purpose

Register of civic engagement programmes conducted across all branches in the group — community service drives, voter awareness (SVEEP), environmental programmes (tree plantation, cleanliness drives), health camps, literacy outreach, disaster preparedness drills, anti-drug awareness, road safety, digital literacy, blood donation drives, and Swachh Bharat activities. These programmes may be run under the NSS banner, the NCC banner, or independently by a branch as a school/college initiative or as part of a government drive.

The Group NSS/NCC Coordinator uses this page to: log all civic programmes across branches in a single register; track student participation and volunteer hours (civic hours credited toward the NSS 240-hour target where applicable); record evidence (photographs, documents, media coverage); flag programmes that have been formally reported to district/state authorities; and generate summary reports for district/state submission. The Cultural Activities Head has view-only access to monitor upcoming civic events that may overlap with cultural calendar activities.

Civic programmes are distinct from the NSS Programme Tracker (page 14): that page tracks activities internal to a branch's NSS unit with enrolled volunteers accumulating their 240 hours; this register covers the broader universe of outward-facing civic activities that may involve non-NSS students, external beneficiaries, government or NGO partners, and cross-branch participation. Scale: 50–200 civic programmes per academic year across all branches.

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group NSS/NCC Coordinator | 100 | G3 | Full — create, edit, archive, view all branches, export, manage reporting | Primary owner |
| Group Cultural Activities Head | 99 | G3 | View only — programme register, KPI cards, hours summary; no write actions | Calendar overlap use case |
| Group Sports Director | 97 | G3 | No access | Redirected to own dashboard |
| Group Library Head | 101 | G2 | No access | Redirected to own dashboard |
| All other roles | — | — | No access | Redirected to own dashboard |

> **Access enforcement:** Django decorator `@require_role(['nss_ncc_coordinator', 'cultural_head'])` gates page load. All POST/PATCH/DELETE endpoints further restricted to `nss_ncc_coordinator` via `@require_role(['nss_ncc_coordinator'])`. Cultural Head sees all data but all action buttons are suppressed at the Django template layer (not via CSS hide — rendered conditionally based on `request.user.role`).

---

## 3. Page Layout

### 3.1 Breadcrumb

```
Group HQ  ›  Sports & Extra-Curricular  ›  NSS/NCC  ›  Civic Programme Register
```

### 3.2 Page Header

```
Civic Programme Register                       [+ Log Programme]  [Export ↓]  [District Report ⎙]
Group NSS/NCC Coordinator — [Officer Name]
AY [YYYY-YY]  ·  [N] Branches  ·  [N] Programmes This AY  ·  [N] Students Participated  ·  [N] Hours Generated
```

`[+ Log Programme]` — opens `civic-programme-create` drawer (Coordinator only; hidden for Cultural Head).
`[Export ↓]` — exports filtered programme register to XLSX or PDF.
`[District Report ⎙]` — generates a formatted summary PDF of all reported programmes for submission to district/state authority (Coordinator only; hidden for Cultural Head).

### 3.3 Alert Banners (conditional)

| Condition | Banner Text | Severity |
|---|---|---|
| Programmes with evidence status = Missing (> 5 programmes) | "[N] civic programme(s) have no evidence uploaded. Upload photos or documents to complete these records." | Yellow |
| Programmes not reported to authority (> 15 and AY > 50% elapsed) | "[N] programmes have not been reported to district authorities. Generate reports before the submission deadline." | Orange |
| No programmes logged in any branch for > 45 days | "No civic programmes have been logged in the last 45 days." | Yellow |
| AY nearing end (last 30 days) + unreported count > 0 | "Academic year ends in [N] days. [N] programme(s) are still unreported." | Red |

---

## 4. KPI Summary Bar

Four KPI cards in a horizontal scrollable bar. All values scoped to the selected academic year.

| Card | Metric | Calculation | HTMX Target | Empty State |
|---|---|---|---|---|
| Total Civic Programmes This AY | Count of all logged programmes (any status except Archived) | `CivicProgramme.objects.filter(ay=current_ay).exclude(status='archived').count()` | `#kpi-total-programmes` | "0" with grey badge |
| Participating Students (Unique) | Distinct student count across all programmes this AY | Summed from `CivicProgramme.student_count` (approximate) or distinct cadet/volunteer join if exact records available | `#kpi-participants` | "0" |
| NSS Hours Generated (Total) | Sum of `(student_count × volunteer_hours_per_student)` for all programmes where `programme_type = NSS Activity` | Computed aggregate | `#kpi-nss-hours` | "0 hrs" |
| Programmes Reported to Authority | Count of programmes with `reported_to_authority = True` | `CivicProgramme.objects.filter(ay=current_ay, reported_to_authority=True).count()` | `#kpi-reported` | "0 / [N total]" |

**HTMX pattern:** Each card uses `hx-get` to its dedicated sub-endpoint with `hx-trigger="load"`. Each card shows a skeleton rectangle while loading. AY selector change triggers refresh of all 4 cards and both section tables via `hx-swap-oob="true"`.

---

## 5. Sections

### 5.1 Civic Programme Register

Main table of all civic programmes logged for the selected academic year. Default sort: Date DESC. Server-side paginated at 25 rows/page.

**Table Columns:**

| Column | Field | Notes |
|---|---|---|
| Programme Name | `CivicProgramme.name` | Sortable; clickable — opens `programme-detail` drawer |
| Category | `CivicProgramme.category` | Colour-coded badge (see category list below) |
| Branch | `programme.branch.name` | Text; sortable |
| Date | `CivicProgramme.date` | DD MMM YYYY; sortable |
| Duration | `CivicProgramme.duration` | Text (e.g. "1 Day", "4 Hours") |
| Student Participants | `CivicProgramme.student_count` | Integer; sortable |
| Staff Coordinators | `CivicProgramme.staff_count` | Integer; "—" if 0 |
| Hours Generated | `student_count × volunteer_hours_per_student` | Integer (total student-hours); sortable |
| Reported to Authority? | `CivicProgramme.reported_to_authority` | Toggle badge: Reported (green) / Not Reported (grey); Coordinator can toggle directly in table |
| Evidence | `CivicProgramme.evidence_status` | Badge: Uploaded (green) / Missing (red) |
| Actions | Inline | "View" / "Edit" / "Archive" |

**Category Badge Colours:**

| Category | Badge Colour |
|---|---|
| Community Service | Blue |
| Environmental (Plantation/Cleanliness) | Green |
| Health & Hygiene Awareness | Teal |
| Literacy & Education Outreach | Purple |
| Voter Awareness (SVEEP) | Indigo |
| Disaster Preparedness | Orange |
| Anti-Drug/Tobacco Awareness | Red |
| Road Safety | Amber |
| Digital Literacy | Cyan |
| Blood Donation Drive | Rose |
| Swachh Bharat Activities | Yellow-green |

**Inline Actions:**
- `View` — opens `programme-detail` drawer, Overview tab. Available to both roles.
- `Edit` — opens `civic-programme-create` drawer pre-filled with existing data (Coordinator only; hidden for Cultural Head).
- `Archive` — confirms archival with a small inline confirmation prompt: "Archive this programme? It will no longer appear in active reports." (Coordinator only).

**Reported to Authority toggle (in table):** Clicking the toggle badge for a row fires `hx-post` to `/api/civic/programmes/{id}/toggle-reported/`. On success, the badge swaps via `hx-swap="outerHTML"` on the badge element. The KPI card "Programmes Reported to Authority" is also refreshed via `hx-swap-oob`. Visible to Coordinator only; Cultural Head sees the badge as read-only text.

**Filter Drawer (hx-get `/api/civic/programmes/` with params):**

| Filter | Type | Options |
|---|---|---|
| Category | Multi-select checkbox | All 11 categories |
| Branch | Multi-select checkbox | All branches in group |
| Reported Status | Radio | All / Reported / Not Reported |
| Evidence Status | Radio | All / Uploaded / Missing |
| Date Range | Date range picker | From – To |
| Academic Year | Select | Current AY + 2 prior |

Active filters rendered as dismissible chips. "Clear All" resets table.

**Search:** Free-text on Programme name, Category, Branch name. `hx-trigger="keyup changed delay:400ms"`.

**Pagination:** `hx-get` with `page` param; `hx-target="#civic-programme-table-body"`.

---

### 5.2 Hours Contribution Summary (Per Branch)

Compact table showing civic programme hours contribution broken down by branch. Not paginated (branch-level, ≤ 50 rows). Default sort: Civic Hours DESC.

**Table Columns:**

| Column | Field | Notes |
|---|---|---|
| Branch | `branch.name` | Sortable |
| Civic Hours This AY | Total student-hours from all civic programmes for this branch | Integer; sortable |
| NSS Hours Credit | Subset of civic hours from programmes with `programme_type = NSS Activity` | Integer; contributes to 240-hour target |
| Non-NSS Hours | `Civic Hours − NSS Hours Credit` | Integer |
| % Towards NSS Targets | `NSS Hours Credit / (enrolled_volunteers × 240) × 100` | Percentage; colour: green > 70% / yellow 40–70% / red < 40%; "—" if no volunteers enrolled |

This table is informational — no inline actions. Sortable on all numeric columns. `[Export]` button above the table exports it to XLSX.

---

## 6. Drawers & Modals

### 6.1 Drawer: `civic-programme-create` (480px, slides from right)

**Trigger:** `[+ Log Programme]` button or "Edit" inline action. Coordinator only.

**4 Tabs:**

#### Tab 1 — Programme

| Field | Type | Validation | Notes |
|---|---|---|---|
| Programme Name | Text input | Required; min 3, max 150 chars | Placeholder: "e.g. Blood Donation Drive — St. Xavier's Branch" |
| Category | Select | Required | 11 categories from list above |
| Date | Date picker | Required; must not be in future | Start date of programme |
| End Date | Date picker | Optional; ≥ Date field | For multi-day programmes |
| Duration | Text input | Required; max 50 chars | Placeholder: "e.g. 1 Day, Half Day, 3 Hours" |
| Branch | Select | Required | All branches in group |
| Venue / Location | Text input | Optional; max 200 chars | |
| Description | Textarea | Required; min 30, max 500 chars | Character counter displayed |
| Programme Type | Select | Required | Options: NSS Activity / NCC Activity / School Initiative / Government Drive |

#### Tab 2 — Participants

| Field | Type | Validation | Notes |
|---|---|---|---|
| Students Count | Number input | Required; min 1; integer | Total student participants |
| Staff Coordinators | Number input | Optional; min 0; integer | |
| Volunteer Hours Per Student | Number input | Required; min 1 | Hours each student earns |
| External Participants | Number input | Optional; min 0 | Non-students (community members, etc.) |
| Beneficiary Count | Number input | Optional; min 0 | e.g. households surveyed, patients screened |
| Upload Attendance | File upload | Optional; PDF or Excel; max 5 MB | Stored in `/media/civic/attendance/` |

Helper text below Volunteer Hours Per Student: "Total hours generated = Students Count × Volunteer Hours Per Student = [computed value shown live]".

#### Tab 3 — Impact

| Field | Type | Validation | Notes |
|---|---|---|---|
| Impact Summary | Textarea | Required; min 30, max 500 chars | Narrative of what was achieved |
| Key Outcomes | Textarea | Optional; max 500 chars | Bullet-friendly text |
| Government / NGO Partner | Text input | Optional; max 200 chars | Partner organisation name if any |
| Media Coverage? | Toggle | Default Off | If On: reveals "Media URL" text input (optional; max 500 chars, URL validated) |
| Photos Upload | Multi-file upload | Optional; max 5 files; JPG/PNG only; max 2 MB each | Previews shown below upload field |

#### Tab 4 — Reporting

| Field | Type | Validation | Notes |
|---|---|---|---|
| Reported to Authority? | Toggle | Default Off | |
| Authority Name | Text input | Conditional — required if Reported = On; max 200 chars | e.g. "District Collector Office, Pune" |
| Report Date | Date picker | Conditional — required if Reported = On | Date report was submitted |
| Reference Number | Text input | Optional; max 100 chars | Authority's acknowledgement number |
| Government Certificate Received? | Toggle | Default Off; shown only if Reported = On | |
| Certificate Upload | File upload | Conditional — shown if Certificate Received = On; PDF only; max 5 MB | |

**Footer Buttons:** `[Save Programme]`; `[Save & Mark Reported]` (saves and sets `reported_to_authority = True`); `[Cancel]`.

---

### 6.2 Drawer: `programme-detail` (480px, slides from right)

**Trigger:** "View" inline action in Section 5.1 or programme name click.

**Header:** Programme Name, Category badge, Programme Type badge, Date, Branch.

**3 Tabs:**

#### Tab 1 — Overview

All programme fields displayed in a two-column read-only layout. Fields match those in `civic-programme-create` Tabs 1 and 2:
- Programme Name, Category, Programme Type, Date, End Date, Duration
- Branch, Venue / Location, Description
- Students Count, Staff Coordinators, Volunteer Hours Per Student
- Total Hours Generated (computed: displayed prominently)
- External Participants, Beneficiary Count
- Impact Summary, Key Outcomes, Government / NGO Partner, Media Coverage URL (if set)

**Buttons (Coordinator only):** `[Edit Programme]` — reopens `civic-programme-create` in edit mode. `[Archive]` — inline confirm before archiving.

#### Tab 2 — Evidence

- **Photos:** Gallery grid (2 columns) of uploaded photos. Each photo is clickable to open a lightbox. "No photos uploaded" placeholder if empty.
- **Video / Media Link:** Displayed as a clickable hyperlink if Media Coverage URL was provided.
- **Attendance Document:** "Download Attendance Sheet" button if file was uploaded.
- **Government Certificate:** "View Certificate" / "Download Certificate" button if certificate was uploaded.
- **Upload Additional Evidence:** `[Upload Photos]` and `[Upload Document]` buttons (Coordinator only) — trigger file upload inline without reopening the full create drawer. `hx-post` to `/api/civic/programmes/{id}/evidence/`.

#### Tab 3 — Reporting

Read-only display of all reporting fields:
- Reported to Authority? (Yes / No)
- Authority Name
- Report Date
- Reference Number
- Government Certificate Received? (Yes / No)
- Certificate: View / Download link

**Buttons (Coordinator only):** `[Mark as Reported]` — opens a small inline form with Authority Name, Report Date, Reference Number fields; `hx-post` to `/api/civic/programmes/{id}/mark-reported/`. `[Un-report]` — removes reported status (requires confirmation). Both buttons hidden if already reported / not reported respectively.

---

## 7. Charts

### 7.1 Civic Programmes by Category (Donut Chart)

- **Type:** Donut chart
- **Segments:** One segment per category, ordered by count DESC
- **Centre label:** "Total Programmes: [N]"
- **Legend:** Below chart — category label + count + percentage
- **Colours:** Matches category badge colours from Section 5.1
- **Data endpoint:** `GET /api/civic/charts/by-category/?ay={ay}`
- **HTMX:** `hx-get` on page load; `hx-trigger="load"`. Rendered into `#chart-by-category`.
- **Tooltip:** "[Category]: [N] programmes ([N]%)"
- **Empty state:** Grey empty donut with "No civic programmes logged for this academic year."

### 7.2 Student Hours Generated Per Month (Bar Chart — Last 6 Months)

- **Type:** Vertical bar chart
- **X-axis:** Last 6 calendar months
- **Y-axis:** Total student-hours (sum of `student_count × hours_per_student` across all programmes in that month)
- **Series:** Single bar per month (teal colour). Optional second series "NSS Hours" overlay (dashed border bar) toggled via a "Show NSS breakdown" checkbox above the chart.
- **Data endpoint:** `GET /api/civic/charts/monthly-hours/?ay={ay}&months=6`
- **HTMX:** `hx-get` on page load; `hx-trigger="load"`. Rendered into `#chart-monthly-hours`.
- **Tooltip:** "[Month]: [N] total student-hours ([N] NSS, [N] non-NSS)"
- **Empty state:** "No hours data available for the last 6 months."

---

## 8. Toast Messages

| Trigger | Toast Text | Type |
|---|---|---|
| Programme logged | "Civic programme '[Name]' has been logged for [Branch]." | Success |
| Programme updated | "Civic programme '[Name]' has been updated." | Success |
| Programme archived | "Civic programme '[Name]' has been archived." | Info |
| Reported to authority toggled on | "Programme '[Name]' marked as reported to authority." | Success |
| Reported to authority toggled off | "Reported status removed for '[Name]'." | Info |
| Evidence uploaded | "Evidence uploaded for '[Name]'." | Success |
| Certificate uploaded | "Government certificate uploaded for '[Name]'." | Success |
| File too large | "File too large. Maximum allowed size is [X] MB." | Error |
| Invalid file type (photo) | "Invalid file type. Please upload JPG or PNG images only." | Error |
| Invalid file type (document) | "Invalid file type. Please upload PDF or Excel only." | Error |
| Too many photos (> 5) | "Maximum 5 photos allowed per programme." | Error |
| Required field missing on save | "Please complete all required fields before saving." | Error |
| Export triggered | "Preparing export… You will be notified when ready." | Info |
| District report generation triggered | "Generating district report… You will be notified when ready." | Info |
| API error | "Something went wrong. Please try again or contact support." | Error |

---

## 9. Empty States

| Section / Component | Condition | Icon | Heading | Body Text | CTA |
|---|---|---|---|---|---|
| Section 5.1 — Civic Programme Register | No programmes this AY | clipboard-list | "No Civic Programmes Logged" | "No civic programmes have been recorded for this academic year." | [+ Log Programme] (Coordinator only) |
| Section 5.1 — filtered result empty | Active filters return no rows | filter | "No Matching Programmes" | "Adjust your filters or search term." | [Clear Filters] |
| Section 5.2 — Hours Contribution Summary | No branches or no hours | bar-chart-2 | "No Hours Data" | "Log civic programmes to begin tracking student hours contribution." | — |
| `programme-detail` — Evidence tab | No photos and no documents uploaded | image | "No Evidence Uploaded" | "Upload photos or documents to complete this programme record." | [Upload Photos] / [Upload Document] (Coordinator only) |
| `programme-detail` — Reporting tab | Not reported to authority | file-text | "Not Yet Reported" | "This programme has not been reported to any district or state authority." | [Mark as Reported] (Coordinator only) |
| Chart 7.1 | No programmes this AY | pie-chart | "No Programme Data" | "Log civic programmes to view category distribution." | — |
| Chart 7.2 | No hours data in last 6 months | bar-chart | "No Hours Data" | "No student hours have been generated in the last 6 months." | — |

---

## 10. Loader States

| Component | Loader Type | Duration Trigger |
|---|---|---|
| KPI cards (all 4) | Skeleton rectangle (48px tall, full card width, animated pulse) | Until `hx-get` response received |
| Section 5.1 table body | Skeleton rows (5 rows × all column widths, animated pulse) | Until table data fetched |
| Section 5.2 table body | Skeleton rows (5 rows) | Until data fetched |
| `programme-detail` drawer body | Skeleton two-column layout (4 rows per column) | Until overview data fetched |
| `programme-detail` — Evidence tab | Spinner centred in tab pane | Until evidence files fetched on tab click |
| `programme-detail` — Reporting tab | Spinner centred in tab pane | Until reporting data fetched on tab click |
| Photo upload in drawer | Inline progress bar per file + thumbnail preview overlay | During upload |
| Document upload in drawer | Inline progress bar below upload field | During upload |
| District report generation | Button spinner + "Generating report…" text | During POST |
| Chart 7.1 | Skeleton circle (160px diameter) | Until Chart.js render |
| Chart 7.2 | Skeleton rectangle (200px tall, full width) | Until Chart.js render |

---

## 11. Role-Based UI Visibility

| UI Element | NSS/NCC Coordinator (100) | Cultural Head (99) | Sports Director (97) | Library Head (101) |
|---|---|---|---|---|
| Page access | Yes — full | Yes — view only | No — redirect | No — redirect |
| `[+ Log Programme]` button | Visible + active | Hidden | — | — |
| `[Export ↓]` button | Visible + active | Visible (no PII fields) | — | — |
| `[District Report ⎙]` button | Visible + active | Hidden | — | — |
| Section 5.1 — "Edit" inline action | Visible | Hidden | — | — |
| Section 5.1 — "Archive" inline action | Visible | Hidden | — | — |
| Section 5.1 — "Reported to Authority" toggle | Active (Coordinator can toggle) | Read-only badge | — | — |
| `programme-detail` — `[Edit Programme]` button | Visible | Hidden | — | — |
| `programme-detail` — `[Archive]` button | Visible | Hidden | — | — |
| `programme-detail` — `[Mark as Reported]` button | Visible | Hidden | — | — |
| `programme-detail` — Evidence `[Upload Photos]` button | Visible | Hidden | — | — |
| `programme-detail` — Evidence `[Upload Document]` button | Visible | Hidden | — | — |
| Section 5.2 — `[Export]` button | Visible | Visible | — | — |
| KPI cards | All 4 visible | All 4 visible | — | — |
| Alert banners | All visible | All visible | — | — |
| Charts | Both visible | Both visible | — | — |

---

## 12. API Endpoints

All endpoints under `/api/civic/`. Authentication: session cookie + CSRF token. Role enforcement at view level.

| Method | Endpoint | Description | Roles | Response |
|---|---|---|---|---|
| GET | `/api/civic/programmes/?ay={ay}&category={cats}&branch={ids}&reported={bool}&evidence={status}&date_from={d}&date_to={d}&search={q}&page={n}` | Paginated civic programme register for Section 5.1 | 99, 100 | `{results: [...], count, next, previous}` |
| POST | `/api/civic/programmes/create/` | Log a new civic programme | 100 | Created programme object |
| GET | `/api/civic/programmes/{id}/` | Single programme detail | 99, 100 | Programme object with related evidence and reporting |
| PATCH | `/api/civic/programmes/{id}/update/` | Update programme metadata | 100 | Updated programme object |
| POST | `/api/civic/programmes/{id}/archive/` | Archive a programme | 100 | `{status: "archived"}` |
| POST | `/api/civic/programmes/{id}/toggle-reported/` | Toggle reported_to_authority flag | 100 | `{reported_to_authority: bool}` |
| POST | `/api/civic/programmes/{id}/mark-reported/` | Set reported status with authority details | 100 | Updated reporting fields |
| POST | `/api/civic/programmes/{id}/evidence/` | Upload additional evidence (photos/documents) | 100 | `{uploaded: [file_ids]}` |
| GET | `/api/civic/hours-summary/?ay={ay}` | Branch-level hours contribution for Section 5.2 | 99, 100 | `[{branch, civic_hours, nss_hours, non_nss_hours, pct_towards_nss}]` |
| GET | `/api/civic/kpi/?ay={ay}` | All 4 KPI card values | 99, 100 | `{total_programmes, participants, nss_hours, reported_count}` |
| GET | `/api/civic/charts/by-category/?ay={ay}` | Data for Chart 7.1 | 99, 100 | `[{category, count, pct}]` |
| GET | `/api/civic/charts/monthly-hours/?ay={ay}&months=6` | Data for Chart 7.2 | 99, 100 | `[{month, total_hours, nss_hours}]` |
| GET | `/api/civic/export/?ay={ay}&format={xlsx\|pdf}&branch={ids}&category={cats}` | Export programme register | 99, 100 | Binary file download |
| GET | `/api/civic/district-report/?ay={ay}&format=pdf` | Generate district submission report | 100 | Binary PDF download |

---

## 13. HTMX Patterns

| Pattern | Trigger Element | `hx-get` / `hx-post` | `hx-target` | `hx-swap` | Notes |
|---|---|---|---|---|---|
| KPI card load | Each card container | `GET /api/civic/kpi/?ay={ay}` | `#kpi-{card-id}` | `innerHTML` | `hx-trigger="load"` |
| AY selector change | `<select name="ay">` | `GET /api/civic/kpi/?ay={ay}` | Multiple via `hx-swap-oob="true"` | `outerHTML` | Refreshes KPI bar + both section tables |
| Programme register table load | `#civic-programme-table-body` | `GET /api/civic/programmes/` | `#civic-programme-table-body` | `innerHTML` | `hx-trigger="load"` |
| Search input | `<input name="search">` | `GET /api/civic/programmes/?search={q}` | `#civic-programme-table-body` | `innerHTML` | `hx-trigger="keyup changed delay:400ms"` |
| Filter drawer apply | `[Apply Filters]` button | `GET /api/civic/programmes/?{params}` | `#civic-programme-table-body` | `innerHTML` | Drawer closes after response |
| Pagination | Page number links | `GET /api/civic/programmes/?page={n}` | `#civic-programme-table-body` | `innerHTML` | |
| Hours summary table load | `#hours-summary-body` | `GET /api/civic/hours-summary/` | `#hours-summary-body` | `innerHTML` | `hx-trigger="load"` |
| Reported toggle in table | Toggle badge per row | `POST /api/civic/programmes/{id}/toggle-reported/` | `#reported-badge-{id}` | `outerHTML` | Refreshes KPI card `#kpi-reported` via `hx-swap-oob` |
| Drawer open — programme detail | "View" / programme name link | `GET /api/civic/programmes/{id}/` | `#drawer-civic-body` | `innerHTML` | Drawer slides open |
| Drawer tab — Evidence | Tab 2 click in `programme-detail` | `GET /api/civic/programmes/{id}/` (evidence sub-section) | `#drawer-tab-evidence-body` | `innerHTML` | `hx-trigger="click"` on tab |
| Drawer tab — Reporting | Tab 3 click | Reporting data from same endpoint | `#drawer-tab-reporting-body` | `innerHTML` | `hx-trigger="click"` |
| Mark as Reported inline form | `[Mark as Reported]` button | `POST /api/civic/programmes/{id}/mark-reported/` | `#drawer-tab-reporting-body` | `innerHTML` | Replaces tab content with updated state |
| Evidence photo upload | `[Upload Photos]` button | `POST /api/civic/programmes/{id}/evidence/` | `#evidence-gallery` | `innerHTML` | Shows progress bar per file; gallery refreshes on complete |
| Evidence document upload | `[Upload Document]` button | `POST /api/civic/programmes/{id}/evidence/` | `#evidence-docs-list` | `innerHTML` | Progress bar shown; list refreshes |
| Chart 7.1 load | `#chart-by-category` | `GET /api/civic/charts/by-category/` | `#chart-by-category` | `innerHTML` | Response contains `<canvas>` + Chart.js init script |
| Chart 7.2 load | `#chart-monthly-hours` | `GET /api/civic/charts/monthly-hours/` | `#chart-monthly-hours` | `innerHTML` | Response contains `<canvas>` + Chart.js init script |
| Chart 7.2 NSS breakdown toggle | "Show NSS breakdown" checkbox | `GET /api/civic/charts/monthly-hours/?nss_breakdown=true` | `#chart-monthly-hours` | `innerHTML` | Re-renders chart with two-series data |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
