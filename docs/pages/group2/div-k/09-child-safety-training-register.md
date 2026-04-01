# 09 — Child Safety Training Register

> **URL:** `/group/welfare/pocso/training/`
> **File:** `09-child-safety-training-register.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Role:** Group Child Protection Officer (Role 90, G3)

---

## 1. Purpose

Tracks POCSO awareness and child safety training completion for all staff across all branches of the group. The POCSO Act 2012, read with the POCSO Rules 2020, mandates that every person employed in a child-care institution — including teaching staff, non-teaching staff, support staff, security personnel, and administrative staff — must receive POCSO awareness training annually. Non-compliance exposes the institution to regulatory penalties and licence cancellations during NCPCR or DPCR inspections.

The register captures: staff identity, branch, designation, training date, training mode, training provider, certificate number, certificate validity period, and renewal due date. The Child Protection Officer uses this page daily to identify branches with training gaps, schedule group-level training drives, and generate the Annual Training Compliance Certificate required by regulatory authorities. Automated alerts flag staff whose certificates are expiring within 30 days and branches that have fallen below 80% compliance — the threshold below which a regulatory risk is flagged.

Scale: 3,000–10,000 staff across 20–50 branches. Annual renewal cycle means a near-constant stream of training events, certificate uploads, and compliance monitoring throughout the academic year.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Child Protection Officer | G3, Role 90 | Full — view, add records, bulk upload, export, generate certificate | Primary owner |
| Group POCSO Coordinator (Div E) | G3, Role 50 | View only — all columns; no edit or upload | Read-only access for coordination |
| Group HR Director | G3 | View only — own staff domain data | Cannot edit training records |
| Branch Principal | Branch-level | View — own branch staff only | Cannot see other branches; no edit |
| All other roles | — | No access | Redirected to own dashboard |

> **Access enforcement:** Django decorator `@require_role(['child_protection_officer'])` for write actions. `@require_role(['child_protection_officer', 'pocso_coordinator', 'hr_director', 'branch_principal'])` for read. Branch Principal queryset filtered by `staff__branch = request.user.branch`.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Welfare & Safety  ›  POCSO  ›  Child Safety Training Register
```

### 3.2 Page Header
```
Child Safety Training Register                   [+ Record Training]  [Bulk Upload ↑]  [Export ↓]  [Generate Compliance Certificate ⎙]
Group Child Protection Officer — [Officer Name]
AY [academic year]  ·  [N] Branches  ·  [N] Staff Total  ·  [N] Trained This Year
```

`[+ Record Training]` — opens `record-training` drawer (individual or batch entry).
`[Bulk Upload ↑]` — opens `bulk-upload` drawer for CSV import.
`[Export ↓]` — exports filtered table to XLSX/PDF.
`[Generate Compliance Certificate ⎙]` — generates the official Annual Training Compliance Certificate as a formatted PDF, signed by Role 90 user. Requires at least one academic year of data.

### 3.3 Alert Banner (conditional)

| Condition | Banner Text | Severity |
|---|---|---|
| Any branch below 80% compliance | "[N] branch(es) have POCSO training compliance below 80%. Regulatory risk flagged." | Red |
| Certificates expiring in ≤ 7 days | "[N] staff certificates expire within 7 days. Renewal required immediately." | Red |
| Never-trained staff count > 0 | "[N] staff members have never received POCSO training. Compliance gap." | Amber |
| Certificates expiring in 8–30 days | "[N] staff certificates expire within 30 days. Schedule renewals." | Amber |
| All branches ≥ 95% compliance | "All branches are above 95% compliance. Excellent standing." | Green |

---

## 4. KPI Summary Bar

Five metric cards displayed horizontally. Each card is non-clickable but accompanied by a small sparkline showing trend over last 6 months.

| Card | Metric | Colour Rule |
|---|---|---|
| % Trained This Year | Trained staff / Total staff × 100 | Green if ≥ 95%; Amber if 80–94%; Red if < 80% |
| Expired Certificates | Count of staff with `status = Expired` | Red if > 0; Green if 0 |
| Never Trained | Count of staff with no training record | Red if > 0; Green if 0 |
| Branches Below 80% | Count of branches with compliance < 80% | Red if > 0; Green if 0 |
| Upcoming Renewals (30 days) | Count of staff with cert expiry within 30 days | Amber if > 0; Green if 0 |

```
┌────────────────────┐ ┌────────────────────┐ ┌────────────────────┐ ┌────────────────────┐ ┌────────────────────┐
│  % Trained (AY)    │ │ Expired Certs      │ │  Never Trained     │ │ Branches < 80%     │ │ Renewals (30d)     │
│      87%           │ │       43           │ │       112          │ │        3           │ │       267          │
│   ● Amber          │ │   ● Red            │ │   ● Red            │ │   ● Red            │ │   ● Amber          │
└────────────────────┘ └────────────────────┘ └────────────────────┘ └────────────────────┘ └────────────────────┘
```

**Branch Compliance Mini-Chart:** Below KPI bar, a horizontal bar chart shows each branch's compliance % (sorted ascending). Branches below 80% shown in red bars; 80–94% in amber; ≥ 95% in green. Chart rendered via Chart.js loaded via CDN.

---

## 5. Sections

### 5.1 Filters and Search Bar

```
[🔍 Search by Staff Name / Employee ID / Certificate No.]  [Branch ▾]  [Staff Type ▾]  [Status ▾]  [Training Mode ▾]  [Validity Date Range 📅]  [Reset Filters]
```

| Filter | Options |
|---|---|
| Branch | All Branches / individual branch names |
| Staff Type | All / Teaching / Non-Teaching / Support / Security / Administrative |
| Status | All / Valid / Expiring Soon (≤ 30 days) / Expired / Never Trained |
| Training Mode | All / In-Person / Online / Blended |
| Validity Date Range | Custom date range picker on `valid_until` |

### 5.2 Training Register Table

Columns, sortable where marked (▲▼):

| Column | Source Field | Sortable | Notes |
|---|---|---|---|
| Staff Name | `staff.full_name` | ▲▼ | Hyperlink — opens `staff-training-detail` drawer |
| Employee ID | `staff.employee_id` | ▲▼ | — |
| Branch | `staff.branch.short_name` | ▲▼ | — |
| Designation | `staff.designation` | — | — |
| Type | `staff.staff_type` | — | Badge: Teaching (Blue) · Non-Teaching (Purple) · Support (Grey) · Security (Orange) · Administrative (Teal) |
| Last Training Date | `last_training_date` | ▲▼ | `DD MMM YYYY`; "Never" if no record |
| Training Mode | `training_mode` | — | In-Person / Online / Blended |
| Certificate Number | `certificate_number` | — | "—" if never trained |
| Valid Until | `valid_until` | ▲▼ | `DD MMM YYYY`; "—" if never trained |
| Status | Computed | — | Pill (see §5.3) |
| Actions | — | — | [View] · [Update] |

**Default sort:** `status` (Expired first, then Expiring Soon, then Never Trained, then Valid) then `staff.branch`.

**Pagination:** 25 rows per page (given large staff counts). Controls: `« Previous  Page N of N  Next »`. Rows-per-page selector: 25 / 50 / 100.

### 5.3 Status Colour Coding

| Status | Pill Colour | Condition |
|---|---|---|
| Valid | Green | Certificate exists and `valid_until` > today + 30 days |
| Expiring Soon | Amber | `valid_until` between today and today + 30 days |
| Expired | Red | `valid_until` < today |
| Never Trained | Dark Red / Crimson | No training record exists |

### 5.4 Branch Compliance Summary Sub-Table

Collapsible section below the main table (collapsed by default). Displays one row per branch:

| Column | Notes |
|---|---|
| Branch | Branch short name |
| Total Staff | Count of all staff in branch |
| Trained This Year | Count with `last_training_date` in current AY |
| Compliance % | Trained / Total × 100 |
| Expired | Count with Expired status |
| Never Trained | Count with Never Trained status |
| Status | Branch-level pill: Compliant (≥ 95%) / At Risk (80–94%) / Non-Compliant (< 80%) |

`[▶ Expand Branch Breakdown]` toggle link above sub-table. HTMX-powered lazy load.

---

## 6. Drawers / Modals

### 6.1 `staff-training-detail` Drawer — 560 px, right-slide

**Trigger:** Click on staff name link in main table.

**Header:**
```
Training History — [Staff Full Name]
[Branch]  ·  [Designation]  ·  [Staff Type]  ·  Employee ID: [ID]
Status: [status pill]
```

**Content:**

**Current Certificate Block:**
| Field | Value |
|---|---|
| Certificate Number | [number] or "None" |
| Training Provider | [provider name] |
| Training Date | DD MMM YYYY |
| Mode | In-Person / Online / Blended |
| Valid From | DD MMM YYYY |
| Valid Until | DD MMM YYYY |
| Days Until Expiry | [N] days / EXPIRED |

**Training History Table (all historical records for this staff member):**

| Training Date | Provider | Mode | Certificate No. | Valid Until | Uploaded By | Document |
|---|---|---|---|---|---|---|
| DD MMM YYYY | [name] | In-Person | [cert no.] | DD MMM YYYY | [user] | [Download ↓] |

Sorted by training date descending.

**Footer:** `[Send Renewal Reminder]` (SMS/email to staff) · `[Update Training Record]` (opens `record-training` drawer pre-filled for this staff member)

---

### 6.2 `record-training` Drawer — 560 px, right-slide

**Trigger:** `[+ Record Training]` header button or `[Update Training Record]` from detail drawer.

**Sub-mode toggle at top of form:**
```
[○ Individual Entry]  [● Batch Entry by Branch]
```

**Individual Entry Fields:**

| Field | Type | Required | Validation |
|---|---|---|---|
| Branch | Select | Yes | Locked if pre-filled from detail drawer |
| Staff Member | Search-select (autocomplete) | Yes | Searches by name or employee ID |
| Training Date | Date picker | Yes | Cannot be future date |
| Training Mode | Radio | Yes | In-Person · Online · Blended |
| Training Provider | Text | Yes | Name of organisation or facilitator |
| Training Duration (hours) | Number | Yes | Min 1, max 40 |
| Certificate Number | Text | Yes | Alphanumeric; must be unique per staff member + training date |
| Valid From | Date picker | Yes | Must equal or follow Training Date |
| Valid Until | Date picker | Yes | Must be after Valid From; typically +1 year |
| Certificate Document | File upload | Yes | PDF/JPG; max 10 MB per file |
| Notes | Textarea | No | Internal notes |

**Batch Entry by Branch Fields:**

| Field | Type | Required | Notes |
|---|---|---|---|
| Branch | Select | Yes | All staff in branch will be displayed |
| Training Date | Date picker | Yes | Applied to all staff in batch |
| Training Mode | Radio | Yes | Applied to all |
| Training Provider | Text | Yes | Applied to all |
| Training Duration (hours) | Number | Yes | Applied to all |
| Staff Selection | Multi-checkbox list | Yes | Pre-loaded list of all staff in selected branch; "Select All" toggle |
| Certificates | Note | — | "Individual certificates uploaded in Bulk Upload tool or via staff detail" |

**Validation:**
- Certificate Number must be unique per `(staff_id, training_date)`.
- `Valid Until` must be after `Valid From`.
- File type enforcement: PDF or JPG only.
- On batch entry, if > 50 staff selected, system shows confirmation: "You are recording training for [N] staff. This cannot be undone. Proceed?"

**Footer:** `[Cancel]`  `[Save Training Record(s)]`

---

### 6.3 `bulk-upload` Drawer — 440 px, right-slide

**Trigger:** `[Bulk Upload ↑]` header button.

**Header:**
```
Bulk Upload — Training Records
Upload a CSV file to record training for multiple staff members at once.
```

**Content:**

CSV template download:
```
[⬇ Download CSV Template]
```
Template columns: `employee_id, staff_name, branch_code, training_date (YYYY-MM-DD), training_mode, provider_name, duration_hours, certificate_number, valid_from (YYYY-MM-DD), valid_until (YYYY-MM-DD)`

**Upload Fields:**

| Field | Type | Required | Notes |
|---|---|---|---|
| Branch | Select | Yes | Validation checks that all rows in CSV match selected branch |
| CSV File | File upload | Yes | `.csv` only; max 5 MB; max 500 rows per upload |
| Training Date (override) | Date picker | No | If provided, overrides `training_date` column in CSV for all rows |

**Upload Behaviour:**
1. File uploaded to server via HTMX.
2. Server-side validation runs: column check, date format check, duplicate certificate check.
3. Preview table shown with colour-coded rows: Valid (Green) / Warning — duplicate (Amber) / Error — missing field (Red).
4. User reviews preview and clicks `[Confirm Upload]` to commit valid rows.
5. Error rows are skipped and listed in a downloadable error report.

**Validation Rules:**
- `employee_id` must match an existing staff record in the branch.
- `certificate_number` must be unique per staff member.
- Dates must be in `YYYY-MM-DD` format.
- `valid_until` must be after `valid_from`.

**Footer:** `[Cancel]`  `[Upload & Preview]`  → after preview: `[Confirm Upload]`

---

## 7. Toast Messages

| Action | Toast Text | Type |
|---|---|---|
| Individual training record saved | "Training record saved for [Staff Name]. Certificate [No.] valid until [date]." | Success |
| Batch training records saved | "Training records saved for [N] staff members." | Success |
| Bulk upload — valid rows committed | "[N] training records imported. [M] rows skipped (see error report)." | Success |
| Bulk upload — all rows valid | "All [N] rows imported successfully." | Success |
| Renewal reminder sent | "Renewal reminder sent to [Staff Name] via SMS/email." | Info |
| Compliance certificate generated | "Annual Training Compliance Certificate generated and downloaded." | Success |
| Export complete | "Training register exported to [format]." | Success |
| Validation error — duplicate cert no. | "Certificate number [No.] already exists for this staff member." | Error |
| Validation error — date format | "Invalid date format in row [N]. Use YYYY-MM-DD." | Error |
| Unauthorised action | "You do not have permission to perform this action." | Error |

---

## 8. Empty States

| Context | Illustration | Heading | Sub-text | Action |
|---|---|---|---|---|
| No training records at all | Graduation cap icon | "No Training Records Found" | "Start by recording training for staff or bulk uploading a CSV." | `[+ Record Training]` · `[Bulk Upload ↑]` |
| No records match filters | Funnel icon | "No Results Match Filters" | "Try adjusting your filters or clearing the search." | `[Reset Filters]` |
| Staff detail — no training history | Calendar icon | "No Training History" | "This staff member has not completed POCSO training. Schedule training immediately." | `[Record Training for This Staff Member]` |
| Bulk upload — CSV empty or invalid | Document icon | "No Valid Rows Found" | "The uploaded CSV has no valid rows. Download the template and try again." | `[⬇ Download CSV Template]` |
| Branch compliance sub-table — no branches | Building icon | "No Branch Data" | "Branch data will appear once at least one training record is saved." | None |

---

## 9. Loader States

| Context | Loader Behaviour |
|---|---|
| Initial page load | KPI bar: 5 shimmer cards. Table: 10 shimmer rows. Branch mini-chart: grey shimmer rectangle |
| Filter / search application | Table content area replaced with spinner (20 px, indigo) while HTMX fetches filtered rows |
| Staff training detail drawer opening | Drawer slides in; inner content shows spinner until HTMX response arrives |
| Bulk upload CSV processing | Spinner replaces `[Upload & Preview]` button; progress text: "Validating [N] rows…" |
| Bulk upload preview table | Shimmer rows appear while server validates CSV; replaced by actual preview rows |
| Generate Compliance Certificate | Button shows spinner, disabled; text: "Generating Certificate…" |
| Export | Button disabled, spinner; text: "Exporting…" |
| Branch compliance sub-table expand | Shimmer rows appear in sub-table while HTMX loads branch breakdown |

---

## 10. Role-Based UI Visibility

| UI Element | Role 90 (CPO) | Role 50 (POCSO Coord.) | HR Director | Branch Principal | All Others |
|---|---|---|---|---|---|
| KPI Summary Bar | Full | Full (view only) | Partial (own-domain only) | Own branch KPIs only | Hidden |
| Branch mini-chart (all branches) | Visible | Visible | Hidden | Own branch only | Hidden |
| Main table — all branches | Visible | Visible | Visible (staff filter applied) | Own branch only | Hidden |
| `[View]` action button | Visible | Visible | Visible | Visible (own branch only) | Hidden |
| `[Update]` action button | Visible | Hidden | Hidden | Hidden | Hidden |
| `[+ Record Training]` button | Visible | Hidden | Hidden | Hidden | Hidden |
| `[Bulk Upload ↑]` button | Visible | Hidden | Hidden | Hidden | Hidden |
| `[Export ↓]` button | Visible | Visible | Visible | Visible (own branch) | Hidden |
| `[Generate Compliance Certificate]` button | Visible | Hidden | Hidden | Hidden | Hidden |
| `[Send Renewal Reminder]` in detail drawer | Visible | Hidden | Hidden | Hidden | Hidden |
| Alert banner | Full detail | Full detail | Partial | Own branch only | Hidden |
| Branch compliance sub-table | Visible (all branches) | Visible (all branches) | Hidden | Own branch only | Hidden |

---

## 11. API Endpoints

### 11.1 List & Filter Training Records
```
GET /api/v1/welfare/pocso/training/
```

| Query Parameter | Type | Description |
|---|---|---|
| `branch_id` | integer | Filter by branch |
| `staff_type` | string | `teaching` · `non_teaching` · `support` · `security` · `administrative` |
| `status` | string | `valid` · `expiring_soon` · `expired` · `never_trained` |
| `training_mode` | string | `in_person` · `online` · `blended` |
| `valid_from` | date (YYYY-MM-DD) | Filter `valid_until` from |
| `valid_to` | date (YYYY-MM-DD) | Filter `valid_until` to |
| `search` | string | Searches `staff.full_name`, `staff.employee_id`, `certificate_number` |
| `page` | integer | Default: 1 |
| `page_size` | integer | 25 · 50 · 100 (default: 25) |
| `ordering` | string | `status` · `last_training_date` · `-last_training_date` · `staff.full_name` · `valid_until` |

**Response:** 200 OK — paginated training record list with computed `status` field.

### 11.2 Retrieve Staff Training History
```
GET /api/v1/welfare/pocso/training/staff/{employee_id}/
```
Returns full training history list for a specific staff member (all records, all years).

### 11.3 Create / Update Training Record (Individual)
```
POST /api/v1/welfare/pocso/training/
PUT  /api/v1/welfare/pocso/training/{record_id}/
```
Body: `employee_id`, `branch_id`, `training_date`, `training_mode`, `provider_name`, `duration_hours`, `certificate_number`, `valid_from`, `valid_until`, `certificate_document` (file), `notes`.
Response: 201 Created / 200 OK.

### 11.4 Bulk Upload
```
POST /api/v1/welfare/pocso/training/bulk-upload/
```
Body: `multipart/form-data` — `csv_file`, `branch_id`, `training_date_override` (optional).
Response: 200 OK — `{ valid_count, error_count, preview_rows: [...], error_rows: [...] }`.

### 11.5 Bulk Upload Confirm
```
POST /api/v1/welfare/pocso/training/bulk-upload/confirm/
```
Body: `upload_session_id` (returned from preview step).
Response: 200 OK — `{ committed_count, skipped_count }`.

### 11.6 KPI Summary
```
GET /api/v1/welfare/pocso/training/kpi-summary/
```
Query: `academic_year` (optional).
Response: `{ pct_trained_this_year, expired_count, never_trained_count, branches_below_80, upcoming_renewals_30d }`.

### 11.7 Branch Compliance Breakdown
```
GET /api/v1/welfare/pocso/training/branch-compliance/
```
Query: `academic_year` (optional).
Response: Array of `{ branch_id, branch_name, total_staff, trained_this_year, compliance_pct, expired_count, never_trained_count, status }`.

### 11.8 Send Renewal Reminder
```
POST /api/v1/welfare/pocso/training/send-reminder/
```
Body: `employee_ids: [...]`, `channel` (`sms` · `email` · `both`).
Response: 200 OK — `{ sent_count, failed_count }`.

### 11.9 Generate Compliance Certificate
```
POST /api/v1/welfare/pocso/training/generate-certificate/
```
Body: `academic_year`, `signed_by` (Role 90 user ID auto-populated).
Response: 200 OK — PDF file download stream.

---

## 12. HTMX Patterns

### 12.1 Table Initialisation with Filter State
```html
<div id="training-table"
     hx-get="/api/v1/welfare/pocso/training/?page=1&page_size=25"
     hx-trigger="load"
     hx-swap="innerHTML"
     hx-indicator="#table-spinner">
</div>
```

### 12.2 Debounced Search
```html
<input name="search"
       hx-get="/api/v1/welfare/pocso/training/"
       hx-trigger="input changed delay:400ms"
       hx-target="#training-table"
       hx-swap="innerHTML"
       hx-include="#filter-branch, #filter-staff-type, #filter-status, #filter-mode, #filter-valid-from, #filter-valid-to"
       placeholder="Search staff name, ID or certificate…">
```

### 12.3 Staff Training Detail Drawer
```html
<a hx-get="/htmx/welfare/pocso/training/staff/{{ employee_id }}/detail/"
   hx-target="#drawer-container"
   hx-swap="innerHTML"
   hx-trigger="click"
   class="text-indigo-600 hover:underline cursor-pointer">
  {{ staff.full_name }}
</a>
```

### 12.4 Individual Training Form Submission
```html
<form hx-post="/api/v1/welfare/pocso/training/"
      hx-encoding="multipart/form-data"
      hx-target="#training-table"
      hx-swap="innerHTML"
      hx-on::after-request="closeDrawer(); showToast(event); refreshKPI();">
  <!-- form fields -->
</form>
```

### 12.5 Bulk Upload — Preview Step
```html
<form id="bulk-upload-form"
      hx-post="/api/v1/welfare/pocso/training/bulk-upload/"
      hx-encoding="multipart/form-data"
      hx-target="#bulk-preview-area"
      hx-swap="innerHTML"
      hx-indicator="#upload-spinner">
  <input type="file" name="csv_file" accept=".csv">
</form>
```

### 12.6 Bulk Upload — Confirm Step
```html
<button hx-post="/api/v1/welfare/pocso/training/bulk-upload/confirm/"
        hx-vals='{"upload_session_id": "{{ session_id }}"}'
        hx-target="#training-table"
        hx-swap="innerHTML"
        hx-on::after-request="closeDrawer(); showToast(event); refreshKPI();"
        hx-disabled-elt="this"
        class="btn-primary">
  Confirm Upload
</button>
```

### 12.7 Branch Compliance Sub-Table Lazy Load
```html
<div id="branch-compliance-table"
     hx-get="/api/v1/welfare/pocso/training/branch-compliance/"
     hx-trigger="revealed"
     hx-swap="innerHTML"
     hx-indicator="#branch-compliance-spinner">
  <!-- Collapsed by default; HTMX loads on expand -->
</div>
```

### 12.8 KPI Bar Auto-Refresh
```html
<div id="training-kpi-bar"
     hx-get="/api/v1/welfare/pocso/training/kpi-summary/"
     hx-trigger="load, every 300s"
     hx-swap="innerHTML">
</div>
```

### 12.9 Send Renewal Reminder (from detail drawer)
```html
<button hx-post="/api/v1/welfare/pocso/training/send-reminder/"
        hx-vals='{"employee_ids": ["{{ employee_id }}"], "channel": "both"}'
        hx-target="#reminder-status"
        hx-swap="innerHTML"
        hx-confirm="Send renewal reminder to {{ staff.full_name }} via SMS and email?"
        class="btn-outline btn-sm">
  Send Renewal Reminder
</button>
```

### 12.10 Mode Toggle (Individual / Batch)
```html
<div>
  <label>
    <input type="radio" name="entry_mode" value="individual"
           hx-get="/htmx/welfare/pocso/training/record-form/?mode=individual"
           hx-target="#training-form-body"
           hx-swap="innerHTML">
    Individual Entry
  </label>
  <label>
    <input type="radio" name="entry_mode" value="batch"
           hx-get="/htmx/welfare/pocso/training/record-form/?mode=batch"
           hx-target="#training-form-body"
           hx-swap="innerHTML">
    Batch Entry by Branch
  </label>
</div>
```

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
