# 10 — NCPCR Reporting Manager

> **URL:** `/group/welfare/pocso/ncpcr-reports/`
> **File:** `10-ncpcr-reporting-manager.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Role:** Group Child Protection Officer (Role 90, G3)

---

## 1. Purpose

Manages all mandatory reporting obligations to external child welfare authorities arising from the group's POCSO compliance programme. Reporting obligations exist across three categories:

1. **Complaint-triggered reports:** Every POCSO complaint registered under File 08 triggers a mandatory report to NCPCR (National Commission for Protection of Child Rights) and, in assault cases, to the local police. The law prescribes specific deadlines — failure to report is itself a criminal offence.

2. **Periodic compliance reports:** Annual POCSO Compliance Reports, ICC Constitution Reports (whenever the ICC is reconstituted), and POCSO Training Compliance Certificates must be filed with NCPCR and state-level bodies at prescribed intervals.

3. **Follow-up correspondence:** Authorities may raise queries on submitted reports. These must be acknowledged and responded to within set timeframes.

This page serves as the compliance calendar and submission log for all such obligations. The Child Protection Officer uses it to track due dates, upload submission evidence (acknowledgment receipts, reference numbers), and respond to authority queries. Reports are immutable once submitted — the system allows only new entries and annotations. The audit trail is complete and tamper-proof. Scale: typically 5–25 reporting obligations per academic year across all branches and annual cycles.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Child Protection Officer | G3, Role 90 | Full — view, create, submit, record follow-up, export | Primary owner of all reports |
| Group CEO | G4 | View only — all reports visible | Cannot create or submit |
| Group POCSO Coordinator (Div E) | G3, Role 50 | View only — non-confidential fields | Submission details and reference numbers visible; report body masked |
| Group Legal & Compliance Officer | G3 | View only — all fields | No edit capability; read for legal audit purposes |
| All other roles | — | No access | Redirected to own dashboard |

> **Access enforcement:** Django decorator `@require_role(['child_protection_officer'])` for all write actions. `@require_role(['child_protection_officer', 'group_ceo', 'pocso_coordinator', 'legal_compliance'])` for read. Submitted reports are flagged `is_immutable=True` in the model; any PATCH/PUT to such a record returns HTTP 403 regardless of role.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Welfare & Safety  ›  POCSO  ›  NCPCR Reporting Manager
```

### 3.2 Page Header
```
NCPCR & Mandatory Reporting Manager                   [+ Submit New Report]  [Export Log ↓]
Group Child Protection Officer — [Officer Name]
AY [academic year]  ·  [N] Total Reports  ·  [N] Submitted  ·  [N] Pending  ·  [N] Overdue
```

`[+ Submit New Report]` — opens `submit-report` drawer. Role 90 only.
`[Export Log ↓]` — exports filtered report log to PDF/XLSX.

### 3.3 Alert Banner (conditional)

| Condition | Banner Text | Severity |
|---|---|---|
| Overdue reports exist | "[N] mandatory report(s) are overdue. Submission required immediately to avoid regulatory penalty." | Red |
| Follow-up queries pending without response | "[N] authority follow-up queries are unanswered. Response due within [N] days." | Red |
| Report due within 48 hours | "Mandatory report [Type] for [authority] is due in [N] hours." | Amber |
| Reports due within 7 days | "[N] report(s) are due within 7 days. Review submission queue." | Amber |
| All reports submitted and no pending follow-ups | "All mandatory reports are submitted and acknowledged. Compliance status: Clear." | Green |

---

## 4. KPI Summary Bar

Four metric cards displayed horizontally.

| Card | Metric | Colour Rule |
|---|---|---|
| Reports Due This Quarter | Count of reports with `due_date` in current quarter and `status != Submitted` | Red if > 0 overdue; Amber if approaching; Green if 0 |
| Reports Submitted On Time % | Count submitted on or before `due_date` / Total submitted × 100 | Green if 100%; Amber if 80–99%; Red if < 80% |
| Overdue Reports | Count where `due_date` < today and `status != Submitted` | Red if > 0; Green if 0 |
| Follow-up Queries Pending | Count with `status = Follow-up Required` and no response recorded | Red if > 0; Green if 0 |

```
┌─────────────────────┐ ┌─────────────────────┐ ┌─────────────────────┐ ┌─────────────────────┐
│  Due This Quarter   │ │  On Time Sub. %     │ │  Overdue Reports    │ │ Follow-up Pending   │
│        6            │ │      94%            │ │        1            │ │        2            │
│   ● Amber           │ │   ● Amber           │ │   ● Red             │ │   ● Red             │
└─────────────────────┘ └─────────────────────┘ └─────────────────────┘ └─────────────────────┘
```

---

## 5. Sections

### 5.1 Filters and Search Bar

```
[🔍 Search by Report ID / Reference No. / Complaint ID]  [Report Type ▾]  [Authority ▾]  [Status ▾]  [Due Date Range 📅]  [Complaint Linked ▾]  [Reset Filters]
```

| Filter | Options |
|---|---|
| Report Type | All / POCSO Complaint Report / Annual Compliance Report / ICC Constitution Report / Training Certificate / Follow-up Response / Other |
| Authority | All / NCPCR / State CWC / Police / DPCR (District Protection of Child Rights) / Other |
| Status | All / Pending / Submitted / Acknowledged / Follow-up Required |
| Due Date Range | Custom date range on `due_date` |
| Complaint Linked | Yes (linked to a POCSO complaint) / No (periodic/administrative report) |

### 5.2 Mandatory Reporting Table

Columns, sortable where marked (▲▼):

| Column | Source Field | Sortable | Notes |
|---|---|---|---|
| Report ID | `report_id` (auto) | ▲▼ | Format: `NR-AY-NNNN` e.g. `NR-2526-0001` |
| Report Type | `report_type` | — | Badge-styled label |
| Related Complaint | `related_complaint_id` | — | Hyperlink to complaint register if linked; "—" if periodic |
| Reporting Authority | `authority` | ▲▼ | NCPCR / State CWC / Police / DPCR |
| Due Date | `due_date` | ▲▼ | `DD MMM YYYY`; highlighted Red if overdue |
| Submitted On | `submitted_on` | ▲▼ | `DD MMM YYYY` or "Pending" |
| Reference / Ack. Number | `reference_number` | — | Portal acknowledgment number from authority |
| Status | `status` | ▲▼ | Pill (see §5.3) |
| Actions | — | — | [View] · [Record Follow-up] (if Follow-up Required) |

**Default sort:** `status` (Overdue first, then Follow-up Required, then Pending, then Submitted/Acknowledged) then `due_date` ascending.

**Pagination:** 15 rows per page. Controls: `« Previous  Page N of N  Next »`. Rows-per-page: 15 / 25 / 50.

### 5.3 Status Colour Coding

| Status | Pill Colour | Description |
|---|---|---|
| Pending | Amber | Report not yet submitted; due date in future |
| Overdue | Red | Due date passed; not submitted |
| Submitted | Blue | Submitted; awaiting authority acknowledgment |
| Acknowledged | Green | Authority has acknowledged receipt; no queries |
| Follow-up Required | Orange | Authority has raised a query requiring response |

### 5.4 Compliance Calendar Strip (above table)

A 12-month horizontal timeline strip (current AY, left-to-right) showing due dates of all reports as coloured markers:

- Red dot: Overdue
- Amber dot: Due within 30 days (pending)
- Blue dot: Submitted
- Green dot: Acknowledged

Hovering over a dot shows a tooltip: `[Report Type] — [Authority] — Due: [date] — Status: [status]`.

Rendered via a lightweight vanilla-JS component; no external library required.

---

## 6. Drawers / Modals

### 6.1 `report-detail` Drawer — 600 px, right-slide

**Trigger:** `[View]` button in table row.

**Header:**
```
Report [NR-2526-0001]                                               [×]
[Report Type]  ·  Authority: [authority]  ·  Status: [status pill]
```

**Content Sections:**

**Report Information Block:**
| Field | Value |
|---|---|
| Report ID | `NR-2526-0001` |
| Report Type | Annual Compliance Report |
| Related Complaint ID | `POCSO-2526-0002` / "Not linked (periodic)" |
| Reporting Authority | NCPCR |
| Due Date | DD MMM YYYY |
| Submitted On | DD MMM YYYY |
| Submitted By | [Officer Name, Role] |
| Reference / Ack. Number | [number] |
| Submission Channel | Email / Online Portal / Physical |

**Report Summary (read-only):**
Full text of the submitted report — shown in a scrollable read-only textarea. This field is immutable post-submission.

**Attachments:**
| Document Name | Type | Uploaded By | Date | Download |
|---|---|---|---|---|
| POCSO_Complaint_Report_2526-0001.pdf | Complaint Report | [user] | DD MMM YYYY | [↓] |
| NCPCR_Ack_Receipt.pdf | Acknowledgment | [user] | DD MMM YYYY | [↓] |

**Authority Correspondence:**
All follow-up queries and responses in chronological order:
```
[DD MMM YYYY · From: NCPCR] — Query: [query text]
[DD MMM YYYY · Our Response] — [response text]  ·  Attachment: [file ↓]
```

**Footer:** `[Record Follow-up]` — only if `status = Follow-up Required` and Role 90. Button opens `record-follow-up` drawer. Immutable note: "Submitted reports cannot be edited."

---

### 6.2 `submit-report` Drawer — 580 px, right-slide

**Trigger:** `[+ Submit New Report]` header button.

**Header:**
```
Submit Mandatory Report
All submitted reports are immutable. Verify all details before saving.
```

**Fields:**

| Field | Type | Required | Validation / Notes |
|---|---|---|---|
| Report Type | Select | Yes | POCSO Complaint Report · Annual Compliance Report · ICC Constitution Report · Training Certificate · Follow-up Response · Other |
| Reporting Authority | Select | Yes | NCPCR · State CWC · Police · DPCR · Other |
| Authority Name (if Other) | Text | Conditional | Shown only if "Other" selected |
| Related Complaint ID | Search-select | Conditional | Required if Report Type = "POCSO Complaint Report"; populates from active complaints |
| Due Date | Date picker | Yes | — |
| Submitted On | Date picker | Yes | Cannot be future; defaults to today |
| Submission Channel | Select | Yes | Email · Online Portal · Physical Courier · In Person |
| Reference / Ack. Number | Text | Yes | Alphanumeric; unique per submission |
| Report Summary | Textarea | Yes | Full text of submitted content; min 100 characters; stored immutably |
| Supporting Documents | File upload (multi) | Yes | PDF/DOCX only; max 20 MB per file; up to 5 files |
| Internal Notes | Textarea | No | Not included in exported report; for internal audit only |

**Validation:**
- If `Report Type = POCSO Complaint Report` and complaint has no related complaint ID, show inline warning: "POCSO complaint reports must be linked to a registered complaint."
- `Submitted On` must not be after today.
- `Reference / Ack. Number` must be unique across all submitted reports for the same authority.
- Once saved, `is_immutable` is set to `True`; the system auto-generates an internal Report ID.
- System checks: if a POCSO complaint has been in "Filed" stage for more than 24 hours without a corresponding report being submitted, a system-generated draft obligation appears in the Pending queue.

**Footer:** `[Cancel]`  `[Submit Report — Permanently Record]`

Confirmation modal before final save: "This report will be permanently recorded and cannot be edited. Are you sure?" `[Cancel]` · `[Confirm & Save]`

---

### 6.3 `record-follow-up` Drawer — 440 px, right-slide

**Trigger:** `[Record Follow-up]` button in report detail drawer footer, or `[Record Follow-up]` action in table row.

**Header:**
```
Record Follow-up — Report [NR-2526-0001]
Authority: [authority]
```

**Fields:**

| Field | Type | Required | Notes |
|---|---|---|---|
| Follow-up Type | Radio | Yes | Authority Query (incoming) · Our Response (outgoing) |
| Date | Date picker | Yes | Defaults to today; cannot be future |
| Query / Response Text | Textarea | Yes | Min 50 characters |
| Attachment | File upload | No | PDF/DOCX/JPG; max 10 MB |
| Update Status To | Select | Yes | Keep as Follow-up Required · Mark as Acknowledged (if responding to final query) |

**Validation:**
- If `Follow-up Type = Our Response` and `Update Status To = Mark as Acknowledged`, system prompts: "Marking as Acknowledged closes the follow-up cycle. This action will update report status to Acknowledged."
- Each follow-up entry is immutable once saved (appended to record; cannot be edited or deleted).

**Footer:** `[Cancel]`  `[Save Follow-up Entry]`

On save: entry appended to report's correspondence log, status updated if applicable, audit log entry created.

---

## 7. Toast Messages

| Action | Toast Text | Type |
|---|---|---|
| Report submitted | "Report [NR-ID] permanently recorded. Reference number [ref] saved." | Success |
| Follow-up entry saved | "Follow-up entry recorded for Report [NR-ID]. Status updated to [status]." | Success |
| Export complete | "Reporting log exported to [format]." | Success |
| Attempt to edit submitted report | "Submitted reports are immutable and cannot be edited." | Error |
| Validation — missing reference number | "Reference / Acknowledgment Number is required for submitted reports." | Error |
| Validation — missing complaint link | "POCSO Complaint Reports must be linked to a registered complaint." | Error |
| Overdue report auto-flagged on load | "Report [NR-ID] is overdue. Submission required immediately." | Warning |
| Compliance certificate generated | "Reporting log compliance certificate generated and ready for download." | Info |

---

## 8. Empty States

| Context | Illustration | Heading | Sub-text | Action |
|---|---|---|---|---|
| No reports in log | Clipboard icon | "No Reports Recorded" | "No mandatory reports have been submitted yet. Submit the first report to start the compliance log." | `[+ Submit New Report]` |
| No reports match filters | Funnel icon | "No Results Match Filters" | "Adjust your filters or reset to view all reports." | `[Reset Filters]` |
| No attachments in report detail | Document icon | "No Attachments" | "Upload acknowledgment receipts or report copies to maintain the compliance trail." | `[Upload Attachment]` (Role 90 only) |
| No follow-up correspondence | Chat icon | "No Follow-up Correspondence" | "Authority queries and responses will appear here." | None |
| Compliance calendar — no due dates | Calendar icon | "No Upcoming Due Dates" | "All reporting obligations have been submitted for this quarter." | None |

---

## 9. Loader States

| Context | Loader Behaviour |
|---|---|
| Initial page load | KPI bar: 4 shimmer cards. Compliance calendar strip: grey shimmer bar. Table: 8 shimmer rows |
| Filter / search | Table content replaced by spinner (20 px, indigo) while HTMX fetches |
| Report detail drawer opening | Drawer slides in; inner content shows spinner |
| Compliance calendar hover tooltip | Instant (no loader; data pre-loaded in DOM) |
| Submit report form — file upload | Progress bar shown per file: "Uploading [filename]… [N]%" |
| `[Submit Report]` button clicked | Button disabled, text: "Submitting…", spinner; confirmation modal appears after API response |
| `[Export Log ↓]` clicked | Button disabled, spinner; text: "Generating export…" |

---

## 10. Role-Based UI Visibility

| UI Element | Role 90 (CPO) | Group CEO | Role 50 (POCSO Coord.) | Legal Compliance | All Others |
|---|---|---|---|---|---|
| KPI Summary Bar | Full | Full | Full | Full | Hidden |
| Compliance calendar strip | Visible | Visible | Visible | Visible | Hidden |
| Report table — all rows | Visible | Visible | Visible | Visible | Hidden |
| Report summary text (detail drawer) | Visible | Visible | Masked (first 200 chars) | Visible | Hidden |
| `[+ Submit New Report]` button | Visible | Hidden | Hidden | Hidden | Hidden |
| `[Record Follow-up]` button | Visible | Hidden | Hidden | Hidden | Hidden |
| `[Export Log ↓]` button | Visible | Visible | Visible | Visible | Hidden |
| Internal notes (detail drawer) | Visible | Visible | Hidden | Visible | Hidden |
| Confirm modal (submit) | Visible | N/A | N/A | N/A | N/A |
| Attachment upload (in submit drawer) | Visible | Hidden | Hidden | Hidden | Hidden |
| Alert banner | Full detail | Full detail | Full detail | Full detail | Hidden |

---

## 11. API Endpoints

### 11.1 List & Filter Reports
```
GET /api/v1/welfare/pocso/ncpcr-reports/
```

| Query Parameter | Type | Description |
|---|---|---|
| `report_type` | string | `complaint_report` · `annual_compliance` · `icc_constitution` · `training_cert` · `follow_up_response` · `other` |
| `authority` | string | `ncpcr` · `state_cwc` · `police` · `dpcr` · `other` |
| `status` | string | `pending` · `overdue` · `submitted` · `acknowledged` · `follow_up_required` |
| `complaint_linked` | boolean | `true` · `false` |
| `due_from` | date (YYYY-MM-DD) | Filter `due_date` from |
| `due_to` | date (YYYY-MM-DD) | Filter `due_date` to |
| `search` | string | Searches `report_id`, `reference_number`, `related_complaint_id` |
| `page` | integer | Default: 1 |
| `page_size` | integer | 15 · 25 · 50 (default: 15) |
| `ordering` | string | `due_date` · `-due_date` · `status` · `submitted_on` |

**Response:** 200 OK — paginated list; `report_summary` field truncated to 200 chars for non-CPO roles.

### 11.2 Retrieve Report Detail
```
GET /api/v1/welfare/pocso/ncpcr-reports/{report_id}/
```
Returns full report object including correspondence log and attachments. `report_summary` full text returned only for Role 90 and legal compliance role.

### 11.3 Submit Report (Create)
```
POST /api/v1/welfare/pocso/ncpcr-reports/
```
Body: `multipart/form-data` — `report_type`, `authority`, `related_complaint_id` (optional), `due_date`, `submitted_on`, `submission_channel`, `reference_number`, `report_summary`, `internal_notes`, `documents[]`.
On success: `is_immutable` set to `True`. Response: 201 Created.

### 11.4 Record Follow-up Entry
```
POST /api/v1/welfare/pocso/ncpcr-reports/{report_id}/follow-up/
```
Body: `follow_up_type` (`authority_query` · `our_response`), `date`, `text`, `attachment` (optional file), `update_status` (optional: `acknowledged`).
Response: 201 Created — updated report status returned.

### 11.5 KPI Summary
```
GET /api/v1/welfare/pocso/ncpcr-reports/kpi-summary/
```
Query: `academic_year` (optional).
Response: `{ due_this_quarter, on_time_pct, overdue_count, follow_up_pending }`.

### 11.6 Compliance Calendar Data
```
GET /api/v1/welfare/pocso/ncpcr-reports/calendar/
```
Query: `academic_year` (optional).
Response: Array of `{ report_id, report_type, authority, due_date, status }` — used to render compliance calendar strip.

### 11.7 Export Log
```
GET /api/v1/welfare/pocso/ncpcr-reports/export/
```
Query: all filter params from §11.1 + `format` (`pdf` · `xlsx`).
Response: File download.

---

## 12. HTMX Patterns

### 12.1 Table Initialisation
```html
<div id="ncpcr-report-table"
     hx-get="/api/v1/welfare/pocso/ncpcr-reports/?page=1&page_size=15"
     hx-trigger="load"
     hx-swap="innerHTML"
     hx-indicator="#table-spinner">
</div>
```

### 12.2 Filter Application
```html
<select name="status"
        id="filter-status"
        hx-get="/api/v1/welfare/pocso/ncpcr-reports/"
        hx-trigger="change"
        hx-target="#ncpcr-report-table"
        hx-swap="innerHTML"
        hx-include="#filter-report-type, #filter-authority, #filter-due-from, #filter-due-to, #search-input">
  <option value="">All Statuses</option>
  <option value="pending">Pending</option>
  <option value="overdue">Overdue</option>
  <option value="submitted">Submitted</option>
  <option value="acknowledged">Acknowledged</option>
  <option value="follow_up_required">Follow-up Required</option>
</select>
```

### 12.3 Report Detail Drawer
```html
<button hx-get="/htmx/welfare/pocso/ncpcr-reports/{{ report_id }}/detail/"
        hx-target="#drawer-container"
        hx-swap="innerHTML"
        hx-trigger="click"
        class="text-indigo-600 hover:underline text-sm">
  View
</button>
```

### 12.4 Submit Report Form with Immutability Confirmation
```html
<form id="submit-report-form"
      hx-post="/api/v1/welfare/pocso/ncpcr-reports/"
      hx-encoding="multipart/form-data"
      hx-target="#ncpcr-report-table"
      hx-swap="innerHTML"
      hx-confirm="This report will be permanently recorded and cannot be edited. Are you sure?"
      hx-on::after-request="closeDrawer(); showToast(event); refreshKPI();">
</form>
```

### 12.5 Record Follow-up Submission
```html
<form hx-post="/api/v1/welfare/pocso/ncpcr-reports/{{ report_id }}/follow-up/"
      hx-encoding="multipart/form-data"
      hx-target="#follow-up-correspondence"
      hx-swap="beforeend"
      hx-on::after-request="showToast(event);">
</form>
```

### 12.6 Compliance Calendar Strip Initialisation
```html
<div id="compliance-calendar"
     hx-get="/api/v1/welfare/pocso/ncpcr-reports/calendar/"
     hx-trigger="load"
     hx-swap="innerHTML"
     hx-indicator="#calendar-spinner">
</div>
```

### 12.7 KPI Bar Auto-Refresh
```html
<div id="ncpcr-kpi-bar"
     hx-get="/api/v1/welfare/pocso/ncpcr-reports/kpi-summary/"
     hx-trigger="load, every 300s"
     hx-swap="innerHTML">
</div>
```

### 12.8 Report Type Conditional Fields
```html
<select name="report_type"
        hx-get="/htmx/welfare/pocso/ncpcr-reports/conditional-fields/"
        hx-target="#conditional-fields-area"
        hx-swap="innerHTML"
        hx-trigger="change">
  <!-- options -->
</select>
```
Server returns the `related_complaint_id` field block only when `report_type = complaint_report`, otherwise returns empty fragment.

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
