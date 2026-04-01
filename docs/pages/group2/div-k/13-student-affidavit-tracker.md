# 13 — Student Affidavit Tracker

> **URL:** `/group/welfare/anti-ragging/affidavits/`
> **File:** `13-student-affidavit-tracker.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Role:** Group Anti-Ragging Committee Head (Role 91, G3)

---

## 1. Purpose

Tracks UGC-mandated annual anti-ragging affidavit collection from all students and their parents/guardians. The UGC Anti-Ragging Regulations 2009 require every student to submit a self-declaration affidavit at the time of admission and at the commencement of each subsequent academic year. A corresponding parent/guardian declaration must also be submitted. Non-submission of either affidavit is grounds for blocking hostel allotment, transport assignment, and in some cases, exam registration — enforcement tools that motivate timely compliance.

The Anti-Ragging Committee Head uses this page to monitor collection progress branch-by-branch, send automated reminders for outstanding affidavits, archive all signed declarations for the UGC-required retention period of 5 years, and produce summary compliance reports for inspection. Digital affidavits — e-signed via OTP sent to the parent/student's registered mobile number — are the preferred mode and reduce physical handling. Physical signed affidavits submitted in paper form are accepted as scans (JPG/PDF upload).

Scale: 20,000–1,00,000 affidavits per academic year (student affidavit + parent affidavit = 2 per student, giving 2× the student headcount). Filtering, pagination, and lazy loading are critical at this scale. Bulk operations (CSV upload, bulk reminders) are the primary data-entry and follow-up mechanisms; individual record updates are the exception.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Anti-Ragging Committee Head | G3, Role 91 | Full — view all branches, send reminders, bulk upload, export, generate compliance report | Primary owner |
| Group CEO | G4 | View only — summary KPIs and branch compliance breakdown only | No student-level access |
| Branch Principal | Branch-level | View — own branch students only; can send reminders for own branch | No access to other branches |
| Branch Anti-Ragging Coordinator | Branch-level | View — own branch; can trigger individual reminders | Read-only; own branch scope |
| Group Hostel Manager | G3 | View — hostel-status column only; cannot see affidavit documents | Read for hostel blocking integration |
| All other roles | — | No access | Redirected to own dashboard |

> **Access enforcement:** Django decorator `@require_role(['anti_ragging_head'])` for write and cross-branch access. Branch-level roles filtered via `queryset.filter(student__branch=request.user.branch)`. Group CEO sees only KPI and branch summary endpoints, not student-level rows.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Welfare & Safety  ›  Anti-Ragging  ›  Student Affidavit Tracker
```

### 3.2 Page Header
```
Student Affidavit Tracker                         [Send Reminders]  [Bulk Upload ↑]  [Export ↓]  [Compliance Report ⎙]
Group Anti-Ragging Committee Head — [Officer Name]
AY [academic year]  ·  [N] Branches  ·  [N] Students  ·  [N] Affidavits Expected  ·  Overall: [N]% Collected
```

`[Send Reminders]` — opens `send-reminder` drawer (select pending students → send WhatsApp/SMS).
`[Bulk Upload ↑]` — opens `bulk-upload-affidavits` drawer for CSV-based physical scan record entry.
`[Export ↓]` — exports filtered affidavit table to XLSX/PDF.
`[Compliance Report ⎙]` — generates branch-level affidavit compliance summary PDF for regulatory submission.

### 3.3 Alert Banner (conditional)

| Condition | Banner Text | Severity |
|---|---|---|
| Hostel-blocked students with pending affidavits | "[N] hostel-allocated students have not submitted affidavits. Hostel blocking is active." | Red |
| Any branch below 90% after 30 days of AY | "[N] branch(es) are below 90% collection after 30 days into the academic year." | Red |
| Parent affidavit significantly lower than student | "Parent affidavit collection is [N]% — [N] percentage points below student affidavit. Drive required." | Amber |
| Upcoming reminder cycle due (monthly) | "Monthly reminder cycle is due. [N] students/parents still have pending affidavits." | Amber |
| All branches above 98% | "Affidavit collection is at [N]% across all branches. Excellent compliance." | Green |

---

## 4. KPI Summary Bar

Five metric cards with a branch-level bar chart below.

| Card | Metric | Colour Rule |
|---|---|---|
| Overall Collection % | (Submitted student affidavits + submitted parent affidavits) / (2 × total students) × 100 | Green if ≥ 95%; Amber if 80–94%; Red if < 80% |
| Student Affidavit % | Submitted student affidavits / Total students × 100 | Green if ≥ 95%; Amber if 80–94%; Red if < 80% |
| Parent Affidavit % | Submitted parent affidavits / Total students × 100 | Green if ≥ 95%; Amber if 80–94%; Red if < 80% |
| Hostel-Blocked Students | Count of hostel-assigned students with any pending affidavit | Red if > 0; Green if 0 |
| Branches Below 95% | Count of branches where overall collection < 95% | Red if > 0; Green if 0 |

```
┌──────────────────────┐ ┌──────────────────────┐ ┌──────────────────────┐ ┌──────────────────────┐ ┌──────────────────────┐
│  Overall Collection  │ │  Student Affidavit   │ │  Parent Affidavit    │ │  Hostel-Blocked      │ │  Branches < 95%      │
│        91%           │ │        94%           │ │        88%           │ │         47           │ │          5           │
│   ● Amber            │ │   ● Amber            │ │   ● Amber            │ │   ● Red              │ │   ● Red              │
└──────────────────────┘ └──────────────────────┘ └──────────────────────┘ └──────────────────────┘ └──────────────────────┘
```

**Branch Compliance Bar Chart:**
A grouped horizontal bar chart rendered via Chart.js (CDN), showing each branch as a row with two bars side-by-side:
- Bar 1 (Blue): Student affidavit % for that branch
- Bar 2 (Teal): Parent affidavit % for that branch

Branches sorted by lowest overall % (most critical at top). Target line at 95% drawn as a dashed vertical reference. Chart loads lazily via HTMX on page load.

---

## 5. Sections

### 5.1 View Toggle
```
[👤 Student View]  [🏫 Branch Summary View]
```
Default: Student View (individual rows). Branch Summary View shows one row per branch (aggregate).

### 5.2 Filters and Search Bar (Student View)

```
[🔍 Search by Student Name / Admission No.]  [Branch ▾]  [Class ▾]  [Student Affidavit Status ▾]  [Parent Affidavit Status ▾]  [Submission Mode ▾]  [Hostel Status ▾]  [Reset Filters]
```

| Filter | Options |
|---|---|
| Branch | All Branches / individual branches |
| Class | All / Class/Year dropdown (populated from student data) |
| Student Affidavit Status | All / Submitted / Pending / Overdue |
| Parent Affidavit Status | All / Submitted / Pending / Overdue |
| Submission Mode | All / Digital (OTP e-sign) / Physical Scan |
| Hostel Status | All / Hostel Allocated / Day Scholar |

### 5.3 Student Affidavit Table (Student View)

Columns, sortable where marked (▲▼):

| Column | Source Field | Sortable | Notes |
|---|---|---|---|
| Student Name | `student.full_name` | ▲▼ | Hyperlink → opens `student-affidavit-detail` drawer |
| Admission No. | `student.admission_number` | ▲▼ | — |
| Branch | `student.branch.short_name` | ▲▼ | — |
| Class / Section | `student.class_section` | ▲▼ | — |
| Hostel Status | `student.hostel_status` | — | Badge: Hostel (Purple) · Day Scholar (Grey) |
| Student Affidavit | `student_affidavit_status` | ▲▼ | Pill (see §5.4) |
| Parent Affidavit | `parent_affidavit_status` | ▲▼ | Pill (see §5.4) |
| Submission Date | `latest_submission_date` | ▲▼ | Most recent of student/parent submission; `DD MMM YYYY` |
| Mode | `submission_mode` | — | Digital / Physical / Mixed (if one each) |
| Verification Status | `verification_status` | — | Verified ✅ / Pending Review ⏳ / Rejected ❌ |
| Actions | — | — | [View] · [Send Reminder] |

**Default sort:** Student Affidavit Status (Overdue first, Pending next, Submitted last) then `student.branch`.

**Pagination:** 50 rows per page. Controls: `« Previous  Page N of N  Next »`. Rows-per-page selector: 25 / 50 / 100. For 1,00,000+ records, cursor-based pagination is used internally.

### 5.4 Affidavit Status Colour Coding

| Status | Pill Colour | Condition |
|---|---|---|
| Submitted | Green | Affidavit received and verified |
| Pending | Amber | Not yet submitted; within collection window |
| Overdue | Red | Collection window has passed; not submitted |

### 5.5 Branch Summary View

One row per branch, aggregated:

| Column | Notes |
|---|---|
| Branch | Branch short name |
| Total Students | — |
| Student Affidavit % | — |
| Parent Affidavit % | — |
| Overall % | (Student % + Parent %) / 2 |
| Hostel-Blocked | Count of hostel students with pending affidavit |
| Compliance Status | Compliant (≥ 95%) / At Risk (85–94%) / Non-Compliant (< 85%) |
| Actions | `[View Students]` (switches to Student View filtered to this branch) · `[Send Branch Reminder]` |

---

## 6. Drawers / Modals

### 6.1 `student-affidavit-detail` Drawer — 560 px, right-slide

**Trigger:** Click on student name in main table or `[View]` action button.

**Header:**
```
Affidavit Record — [Student Full Name]
[Branch]  ·  [Class/Section]  ·  Admission: [No.]  ·  Hostel: [Yes/No]
```

**Student Profile Block:**
| Field | Value |
|---|---|
| Student Name | [Full Name] |
| Admission Number | [No.] |
| Branch | [Branch Name] |
| Class / Section | [Class] |
| Hostel Status | Hostel Allocated / Day Scholar |
| Parent / Guardian Name | [Name] |
| Parent Mobile | [masked: +91 XXXXX-X1234] |
| Parent Email | [masked: xxxxx@gmail.com] |

**Student Affidavit Block:**
| Field | Value |
|---|---|
| Status | Submitted ✅ / Pending ⏳ / Overdue ❌ |
| Submission Date | DD MMM YYYY / "Not submitted" |
| Mode | Digital (OTP e-sign) / Physical Scan / — |
| OTP Verified At | DD MMM YYYY HH:MM / — |
| Verification Status | Verified / Pending Review / Rejected |
| Document | `[Download Affidavit ↓]` / "Not uploaded" |

**Parent Affidavit Block:**
Same fields as Student Affidavit Block, but for parent declaration.

**Submission History Table (if multiple submissions — e.g. rejected and re-submitted):**
| Date | Type | Mode | Uploaded By | Status |
|---|---|---|---|---|
| DD MMM YYYY | Student | Digital | Self | Verified |
| DD MMM YYYY | Parent | Physical | Branch Admin | Pending Review |

**Footer:**
`[Send Reminder to Parent]` — opens `send-reminder` drawer pre-filled with this student.
`[Mark as Verified]` — inline action to change `verification_status` to "Verified". Role 91 and Branch Principal only.
`[Reject Submission]` — with mandatory reason field; sets status to Rejected and triggers re-submission notification.

---

### 6.2 `send-reminder` Drawer — 440 px, right-slide

**Trigger:** `[Send Reminders]` header button, `[Send Reminder]` table action, or `[Send Reminder to Parent]` in student detail drawer.

**Header:**
```
Send Affidavit Reminder
Notify parents and students with pending or overdue affidavits.
```

**Content:**

**Recipient Selection (when opened from header button):**
```
[○ All Pending Students in Branch]  [○ Overdue Only]  [● Custom Selection]
```

If "All Pending" or "Overdue Only" selected: Branch dropdown shown (mandatory); count of affected students displayed: "This will send reminders to [N] students / [N] parents."

If "Custom Selection": A filterable multi-select list of students with pending affidavits. Checkboxes. "Select All" toggle. Shows student name, branch, and which affidavit is pending (Student / Parent / Both).

**Channel Selection:**
| Field | Type | Notes |
|---|---|---|
| WhatsApp | Checkbox | Sends via registered parent WhatsApp number |
| SMS | Checkbox | Falls back to SMS if WhatsApp fails |
| Portal Notification | Checkbox | In-portal notification to student account |

At least one channel must be selected.

**Message Preview:**
```
[WhatsApp Message Preview — auto-generated from template]
"Dear [Parent Name], please submit the anti-ragging affidavit for [Student Name] (Class [X], [Branch]) at the earliest. Last date: [date]. Submit online at: [link] or submit physical copy at the branch office. — [Group Name]"
[Edit Message] (Role 91 only — opens inline text editor with character count)
```

**Fields:**

| Field | Type | Required | Notes |
|---|---|---|---|
| Branch (if batch) | Select | Conditional | Required for batch send |
| Recipient scope | Radio | Yes | All Pending / Overdue Only / Custom |
| Students (if custom) | Multi-checkbox | Conditional | Search + checkbox list |
| Channels | Checkbox group | Yes | At least one required |
| Schedule Send | Toggle | No | Default: Send Immediately; if toggled, shows date/time picker |

**Footer:** `[Cancel]`  `[Send [N] Reminders Now]` / `[Schedule Reminders]`

After send: success toast shows count sent and count failed (if any delivery failures).

---

### 6.3 `bulk-upload-affidavits` Drawer — 480 px, right-slide

**Trigger:** `[Bulk Upload ↑]` header button.

**Header:**
```
Bulk Upload — Physical Affidavit Records
For branches submitting scanned physical affidavit records via CSV.
```

**Content:**

CSV template download:
```
[⬇ Download CSV Template]
```
Template columns: `admission_number, student_name, affidavit_type (student/parent/both), submission_date (YYYY-MM-DD), submission_mode (physical_scan), document_reference_number`

**Upload Fields:**

| Field | Type | Required | Notes |
|---|---|---|---|
| Branch | Select | Yes | All rows in CSV must belong to selected branch |
| Academic Year | Select | Yes | Defaults to current AY |
| CSV File | File upload | Yes | `.csv` only; max 5 MB; max 1,000 rows per upload |
| Document Batch Scan ZIP | File upload | No | Optional ZIP of scanned affidavit PDFs; filenames must match `document_reference_number` from CSV |

**Upload Behaviour (same pattern as File 09 bulk upload):**
1. CSV uploaded; server validates columns, date formats, admission number matches.
2. Preview table shows: Valid (Green) / Warning — already submitted (Amber) / Error (Red).
3. User reviews and clicks `[Confirm Upload]` to commit valid rows.
4. Error rows listed in downloadable error report.

**Validation Rules:**
- `admission_number` must match an existing student in the selected branch.
- `submission_date` must be in `YYYY-MM-DD` format and not a future date.
- `affidavit_type` must be `student`, `parent`, or `both`.
- If `both` selected, one row creates records for both student and parent affidavit.
- If a submission already exists for that student + AY + type and status is "Verified", a warning is shown: "Affidavit already verified. Re-upload will replace with Pending Review status."

**Footer:** `[Cancel]`  `[Upload & Preview]`  → `[Confirm Upload]`

---

## 7. Toast Messages

| Action | Toast Text | Type |
|---|---|---|
| Reminders sent (batch) | "[N] reminders sent via [channels]. [M] failed (delivery errors)." | Success |
| Reminder sent (individual) | "Reminder sent to parent of [Student Name] via [channel]." | Success |
| Bulk upload committed | "[N] affidavit records imported. [M] rows skipped (see error report)." | Success |
| Affidavit marked verified | "Affidavit verified for [Student Name] — [type]." | Success |
| Affidavit rejected | "Affidavit rejected for [Student Name]. Reason recorded. Re-submission notification sent." | Info |
| Compliance report generated | "Affidavit Compliance Report generated and downloaded." | Success |
| Export complete | "Affidavit tracker exported to [format]." | Success |
| Validation — admission number not found | "Admission number [No.] not found in branch [Branch]. Row skipped." | Error |
| Reminder send failed — no mobile on record | "No registered mobile number for [N] students. Reminders not sent." | Warning |
| Scheduled reminder confirmed | "[N] reminders scheduled for [date] at [time]." | Info |

---

## 8. Empty States

| Context | Illustration | Heading | Sub-text | Action |
|---|---|---|---|---|
| No student records loaded (first AY setup) | User group icon | "No Students Found" | "Student data must be imported before affidavit tracking can begin. Contact the system administrator." | None |
| No results match filters | Funnel icon | "No Students Match Filters" | "Adjust your filters or clear them to see all students." | `[Reset Filters]` |
| Student detail — no affidavit submitted | Document icon | "No Affidavit Submitted" | "This student has not yet submitted an anti-ragging affidavit for the current academic year." | `[Send Reminder to Parent]` |
| Bulk upload CSV — no valid rows | Document icon | "No Valid Rows in CSV" | "The uploaded CSV contains no valid rows. Download the template and verify your data." | `[⬇ Download CSV Template]` |
| Branch summary — no branches | Building icon | "No Branches Found" | "Branch data will appear once student records are available." | None |
| Chart — no data yet for AY | Chart icon | "No Collection Data Yet" | "Collection statistics will appear once the academic year data is loaded." | None |

---

## 9. Loader States

| Context | Loader Behaviour |
|---|---|
| Initial page load | KPI bar: 5 shimmer cards. Branch chart: grey shimmer rectangle (120 px tall). Table: 15 shimmer rows |
| Filter / search | Table content replaced by spinner (20 px, indigo). Given large data volumes, debounce delay is 600 ms |
| Student affidavit detail drawer | Drawer slides in; content area shows spinner |
| Branch summary view switch | View container replaced by spinner while HTMX fetches aggregated branch data |
| `[Send Reminders Now]` | Button disabled, text: "Sending…"; spinner; count updates in real-time via polling |
| Bulk upload preview | Shimmer rows during validation; replaced by colour-coded preview table |
| Compliance report generation | Button shows spinner, text: "Generating Report…"; may take 10–20 seconds for large groups |
| Export (large data set) | Button disabled, spinner; server-side generation queued; user notified via toast when ready |

---

## 10. Role-Based UI Visibility

| UI Element | Role 91 (AR Head) | Group CEO | Branch Principal | Branch AR Coord. | Group Hostel Mgr | All Others |
|---|---|---|---|---|---|---|
| KPI Summary Bar | Full | Full | Own branch only | Own branch only | Hostel-Blocked card only | Hidden |
| Branch compliance bar chart | Visible (all branches) | Visible (all branches) | Own branch bar only | Own branch bar only | Hidden | Hidden |
| Student table — all branches | Visible | Hidden (summary only) | Own branch only | Own branch only | Hidden | Hidden |
| `[View]` action button | Visible | Hidden | Visible (own branch) | Visible (own branch) | Hidden | Hidden |
| `[Send Reminder]` action | Visible | Hidden | Visible (own branch) | Visible (own branch) | Hidden | Hidden |
| `[Send Reminders]` header button | Visible | Hidden | Visible (own branch only) | Hidden | Hidden | Hidden |
| `[Bulk Upload ↑]` header button | Visible | Hidden | Visible (own branch) | Hidden | Hidden | Hidden |
| `[Export ↓]` button | Visible | Hidden | Visible (own branch) | Hidden | Hidden | Hidden |
| `[Compliance Report ⎙]` button | Visible | Visible | Visible (own branch) | Hidden | Hidden | Hidden |
| `[Mark as Verified]` in drawer | Visible | Hidden | Visible (own branch) | Hidden | Hidden | Hidden |
| `[Reject Submission]` in drawer | Visible | Hidden | Visible (own branch) | Hidden | Hidden | Hidden |
| Parent contact details (masked) | Visible | Hidden | Visible | Visible | Hidden | Hidden |
| Branch Summary View toggle | Visible | Visible | Visible (own branch) | Hidden | Hidden | Hidden |
| Alert banner | Full detail | Full detail | Own branch alerts | Own branch alerts | Hidden | Hidden |

---

## 11. API Endpoints

### 11.1 List & Filter Student Affidavit Records
```
GET /api/v1/welfare/anti-ragging/affidavits/
```

| Query Parameter | Type | Description |
|---|---|---|
| `branch_id` | integer | Filter by branch |
| `class_section` | string | Filter by class/section identifier |
| `student_affidavit_status` | string | `submitted` · `pending` · `overdue` |
| `parent_affidavit_status` | string | `submitted` · `pending` · `overdue` |
| `submission_mode` | string | `digital` · `physical` |
| `hostel_status` | string | `hostel` · `day_scholar` |
| `search` | string | Searches `student.full_name` and `student.admission_number` |
| `page` | integer | Default: 1 |
| `page_size` | integer | 25 · 50 · 100 (default: 50) |
| `cursor` | string | Cursor token for cursor-based pagination (large datasets) |
| `ordering` | string | `student_affidavit_status` · `parent_affidavit_status` · `student.full_name` · `latest_submission_date` |

**Response:** 200 OK — paginated list; parent contact details masked for non-privileged roles.

### 11.2 Retrieve Student Affidavit Detail
```
GET /api/v1/welfare/anti-ragging/affidavits/student/{admission_number}/
```
Returns full affidavit record including submission history. Parent mobile/email returned masked for Branch AR Coord.

### 11.3 Update Verification Status
```
PATCH /api/v1/welfare/anti-ragging/affidavits/student/{admission_number}/verify/
```
Body: `affidavit_type` (`student` · `parent`), `verification_status` (`verified` · `rejected`), `rejection_reason` (required if rejected).

### 11.4 Send Reminders
```
POST /api/v1/welfare/anti-ragging/affidavits/send-reminders/
```
Body: `branch_id` (optional), `scope` (`all_pending` · `overdue_only` · `custom`), `student_admission_numbers[]` (if custom), `channels[]` (`whatsapp` · `sms` · `portal`), `message_override` (optional), `schedule_at` (optional ISO datetime).
Response: 200 OK — `{ queued_count, failed_count, failure_reasons: [...] }`.

### 11.5 Bulk Upload Preview
```
POST /api/v1/welfare/anti-ragging/affidavits/bulk-upload/preview/
```
Body: `multipart/form-data` — `csv_file`, `branch_id`, `academic_year`.
Response: `{ valid_rows: [...], warning_rows: [...], error_rows: [...], session_id }`.

### 11.6 Bulk Upload Confirm
```
POST /api/v1/welfare/anti-ragging/affidavits/bulk-upload/confirm/
```
Body: `session_id`.
Response: `{ committed_count, skipped_count }`.

### 11.7 KPI Summary
```
GET /api/v1/welfare/anti-ragging/affidavits/kpi-summary/
```
Query: `academic_year` (optional), `branch_id` (optional — for branch-scoped roles).
Response: `{ overall_pct, student_affidavit_pct, parent_affidavit_pct, hostel_blocked_count, branches_below_95 }`.

### 11.8 Branch Compliance Breakdown
```
GET /api/v1/welfare/anti-ragging/affidavits/branch-compliance/
```
Query: `academic_year` (optional).
Response: Array of `{ branch_id, branch_name, total_students, student_pct, parent_pct, overall_pct, hostel_blocked, status }`.

### 11.9 Generate Compliance Report
```
POST /api/v1/welfare/anti-ragging/affidavits/compliance-report/
```
Body: `academic_year`, `branch_ids[]` (empty = all branches).
Response: PDF file download.

### 11.10 Export
```
GET /api/v1/welfare/anti-ragging/affidavits/export/
```
Query: all filter params from §11.1 + `format` (`xlsx` · `pdf`).
Response: File download (async for large exports — returns job ID; poll for completion).

---

## 12. HTMX Patterns

### 12.1 Table Initialisation (Cursor-Paginated)
```html
<div id="affidavit-table"
     hx-get="/api/v1/welfare/anti-ragging/affidavits/?page_size=50"
     hx-trigger="load"
     hx-swap="innerHTML"
     hx-indicator="#table-spinner">
</div>
```

### 12.2 Debounced Search (600 ms for large dataset)
```html
<input name="search"
       hx-get="/api/v1/welfare/anti-ragging/affidavits/"
       hx-trigger="input changed delay:600ms"
       hx-target="#affidavit-table"
       hx-swap="innerHTML"
       hx-include="#filter-branch, #filter-class, #filter-student-status, #filter-parent-status, #filter-mode, #filter-hostel"
       placeholder="Search student name or admission number…">
```

### 12.3 Student Detail Drawer
```html
<a hx-get="/htmx/welfare/anti-ragging/affidavits/student/{{ admission_number }}/detail/"
   hx-target="#drawer-container"
   hx-swap="innerHTML"
   class="text-indigo-600 hover:underline cursor-pointer">
  {{ student.full_name }}
</a>
```

### 12.4 View Toggle (Student / Branch Summary)
```html
<button id="toggle-branch-view"
        hx-get="/htmx/welfare/anti-ragging/affidavits/branch-summary/"
        hx-target="#affidavit-view-container"
        hx-swap="innerHTML"
        hx-trigger="click">
  🏫 Branch Summary View
</button>
```

### 12.5 Send Reminders Form
```html
<form hx-post="/api/v1/welfare/anti-ragging/affidavits/send-reminders/"
      hx-target="#reminder-result"
      hx-swap="innerHTML"
      hx-on::after-request="showToast(event);"
      hx-disabled-elt="button[type='submit']">
  <!-- recipient selection, channel checkboxes -->
  <button type="submit" class="btn-primary">
    Send <span id="reminder-count">0</span> Reminders Now
  </button>
</form>
```

Recipient count updates dynamically as user changes scope/branch selection:
```html
<select name="branch_id"
        hx-get="/htmx/welfare/anti-ragging/affidavits/reminder-count/"
        hx-target="#reminder-count"
        hx-swap="innerHTML"
        hx-trigger="change"
        hx-include="#reminder-scope">
</select>
```

### 12.6 Bulk Upload Preview
```html
<form id="bulk-affidavit-upload"
      hx-post="/api/v1/welfare/anti-ragging/affidavits/bulk-upload/preview/"
      hx-encoding="multipart/form-data"
      hx-target="#bulk-preview-area"
      hx-swap="innerHTML"
      hx-indicator="#upload-spinner">
  <input type="file" name="csv_file" accept=".csv">
</form>
```

### 12.7 Bulk Upload Confirm
```html
<button hx-post="/api/v1/welfare/anti-ragging/affidavits/bulk-upload/confirm/"
        hx-vals='{"session_id": "{{ session_id }}"}'
        hx-target="#affidavit-table"
        hx-swap="innerHTML"
        hx-on::after-request="closeDrawer(); showToast(event); refreshKPI();"
        class="btn-primary">
  Confirm Upload
</button>
```

### 12.8 Verification Status Inline Update
```html
<button hx-patch="/api/v1/welfare/anti-ragging/affidavits/student/{{ admission_number }}/verify/"
        hx-vals='{"affidavit_type": "student", "verification_status": "verified"}'
        hx-target="#student-affidavit-block"
        hx-swap="innerHTML"
        hx-confirm="Mark this student affidavit as verified?"
        class="btn-sm btn-success">
  Mark as Verified
</button>
```

### 12.9 KPI + Chart Auto-Refresh
```html
<div id="affidavit-kpi-bar"
     hx-get="/api/v1/welfare/anti-ragging/affidavits/kpi-summary/"
     hx-trigger="load, every 600s"
     hx-swap="innerHTML">
</div>
<div id="branch-compliance-chart"
     hx-get="/api/v1/welfare/anti-ragging/affidavits/branch-compliance/"
     hx-trigger="load"
     hx-swap="innerHTML"
     hx-on::after-settle="renderBranchChart(this);">
</div>
```

### 12.10 Branch Summary — View Students Link
```html
<button hx-get="/api/v1/welfare/anti-ragging/affidavits/?branch_id={{ branch.id }}&page_size=50"
        hx-target="#affidavit-view-container"
        hx-swap="innerHTML"
        hx-on::before-request="switchToStudentView();"
        class="text-indigo-600 hover:underline text-sm">
  View Students
</button>
```

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
