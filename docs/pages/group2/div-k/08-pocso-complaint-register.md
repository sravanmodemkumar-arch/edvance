# 08 — POCSO Complaint Register

> **URL:** `/group/welfare/pocso/complaints/`
> **File:** `08-pocso-complaint-register.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Role:** Group Child Protection Officer (Role 90, G3)

---

## 1. Purpose

Complete register of all POCSO (Protection of Children from Sexual Offences) complaints received across all branches of the group. Every complaint progresses through a legally mandated lifecycle under the POCSO Act 2012: Filed → Acknowledged (within 24 hours) → ICC Preliminary Inquiry (within 7 days) → Full Investigation (within 60 days) → Finding → Closure or Appeal. Mandatory reporting to NCPCR and the local police is also tracked against each complaint.

This page is the nerve-centre for child protection compliance across the entire group. The Group Child Protection Officer owns the entire process end-to-end. The Branch Principal may initiate a complaint record (trigger only) but cannot view full case details — confidentiality is absolute. All free-text fields (description, witness statements, finding notes) are encrypted at rest using AES-256 and are decrypted only for Role 90 and Group CEO on-screen. Every access to a complaint record is audit-logged with timestamp, role, and user ID.

Given the extreme sensitivity and legal gravity of POCSO matters, the system enforces strict role gates, immutable audit trails, and SLA countdown timers. Each breach of an SLA deadline is flagged as a compliance risk. Scale: typically 0–5 complaints per year across all branches — each one is high-stakes, legally consequential, and demands flawless case management.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Child Protection Officer | G3, Role 90 | Full — create, view all fields, update stage, mark reporting | Only role that sees decrypted `[CONFIDENTIAL]` fields |
| Group CEO | G4 | View — all fields including confidential | Read-only; no edit capability |
| Group POCSO Coordinator (Div E) | G3, Role 50 | View only — non-confidential fields visible | Description, witness names, and finding notes are masked |
| Branch Principal | Branch-level | Trigger new complaint only via `new-complaint` drawer | Cannot view complaint detail after submission |
| ICC Member (assigned) | Branch-level | View — own assigned case summary only | No edit; receives system notifications |
| All other roles | — | No access | Redirected to own dashboard; 403 on direct URL |

> **Access enforcement:** Django view decorator `@require_role(['child_protection_officer', 'group_ceo'])` for full access; separate read-only decorator `@require_role_read(['pocso_coordinator'])` for view-only fields. Confidential field decryption gated at `ConfidentialFieldMixin` which checks `request.user.role_id in [90, 'ceo']`.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Welfare & Safety  ›  POCSO  ›  Complaint Register
```

### 3.2 Page Header
```
POCSO Complaint Register                          [+ New Complaint]  [Export ↓]  [Print Register ⎙]
Group Child Protection Officer — [Officer Name]
AY [academic year]  ·  [N] Total Complaints  ·  [N] Active  ·  [N] Closed
```

`[+ New Complaint]` — opens `new-complaint` drawer. Available to Role 90 and Branch Principal (limited form).
`[Export ↓]` — exports complaint list (non-confidential fields only) to PDF/XLSX. Requires Role 90.
`[Print Register]` — formatted A4 register view for regulatory inspection.

### 3.3 Alert Banner (conditional — shown above KPI bar)

| Condition | Banner Text | Severity |
|---|---|---|
| Acknowledgment overdue (> 24 h since filing) | "[N] complaint(s) not yet acknowledged within the mandated 24-hour window. Immediate action required." | Red |
| Preliminary Inquiry SLA breached (> 7 days) | "[N] complaint(s) have exceeded the 7-day Preliminary Inquiry deadline." | Red |
| Full Investigation SLA breached (> 60 days) | "[N] complaint(s) have exceeded the 60-day Full Investigation deadline." | Red |
| Mandatory NCPCR report not filed | "Mandatory NCPCR report has not been submitted for Complaint [ID]. Due: [date]." | Red |
| Police FIR not recorded within 24 h of assault complaint | "Complaint [ID] involves assault — police FIR must be recorded. Status: Pending." | Red |
| No complaints on record (first load) | "No complaints registered. Register is active and secure." | Blue (informational) |

---

## 4. KPI Summary Bar

Five cards displayed horizontally below the page header. Cards are non-clickable data indicators.

| Card | Metric | Colour Rule |
|---|---|---|
| Total Complaints (This AY) | Count of all complaints in current academic year | Grey (neutral) |
| Active Cases | Count where stage ≠ Closed and stage ≠ Appealed | Red if > 2; Amber if 1–2; Green if 0 |
| Acknowledgment Compliance | % complaints acknowledged within 24 hours | Green if 100%; Amber if 80–99%; Red if < 80% |
| Mandatory Reporting Complete | % complaints with NCPCR + Police reporting marked | Green if 100%; Amber if 80–99%; Red if < 80% |
| SLA Breach Count | Count of any active SLA breached (24 h / 7 day / 60 day) | Red if > 0; Green if 0 |

```
┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│ Total (This AY)  │ │  Active Cases    │ │ Ack. Compliance  │ │ Mand. Reporting  │ │  SLA Breaches    │
│       4          │ │       2          │ │     100%         │ │      75%         │ │       1          │
│    (All AYs: 9)  │ │ ● Red            │ │   ● Green        │ │   ● Amber        │ │   ● Red          │
└──────────────────┘ └──────────────────┘ └──────────────────┘ └──────────────────┘ └──────────────────┘
```

---

## 5. Sections

### 5.1 View Toggle
```
[≡ Table View]  [⬜ Stage Pipeline View]
```
Default: Table View. Stage Pipeline View renders a Kanban-style column board (see §5.3).

### 5.2 Filters and Search Bar (Table View)

```
[🔍 Search by Complaint ID / Branch]  [Branch ▾]  [Stage ▾]  [SLA Status ▾]  [Complainant Type ▾]  [Victim Category ▾]  [Date Range 📅]  [Reset Filters]
```

| Filter | Options |
|---|---|
| Branch | All Branches / individual branch names (dropdown populated from DB) |
| Stage | Filed / Acknowledged / Preliminary Inquiry / Full Investigation / Finding / Closed / Appeal |
| SLA Status | All / On Track / At Risk (within 20% of deadline) / Breached |
| Complainant Type | Student / Staff / Parent / Anonymous |
| Victim Category | Student / Staff |
| Date Range | Custom date picker — filters on `date_received` |

### 5.3 Complaint Table (Table View)

Columns, sortable where marked (▲▼):

| Column | Source Field | Sortable | Notes |
|---|---|---|---|
| Complaint ID | `complaint_id` (auto) | ▲▼ | Format: `POCSO-AY-NNNN` e.g. `POCSO-2526-0001` |
| Branch | `branch.short_name` | ▲▼ | — |
| Date Received | `date_received` | ▲▼ | `DD MMM YYYY` format |
| Complainant Type | `complainant_type` | — | Badge: Student (Blue) · Staff (Purple) · Parent (Teal) · Anonymous (Grey) |
| Victim Category | `victim_category` | — | Badge: Student / Staff |
| Complaint Nature | `complaint_nature` | — | `[CONFIDENTIAL]` shown to non-Role-90 as `████████` |
| Current Stage | `current_stage` | ▲▼ | Colour-coded pill (see §5.4) |
| Days Since Filing | Computed | ▲▼ | Integer days |
| SLA Status | Computed from stage + days | — | Pill: On Track (Green) · At Risk (Amber) · Breached (Red) |
| NCPCR Reported | `ncpcr_reported` | — | ✅ / ❌ |
| Police Reported | `police_reported` | — | ✅ / ❌ |
| Actions | — | — | [View] visible to Role 90 and CEO only |

**Default sort:** `date_received` descending (most recent first).

**Pagination:** 10 rows per page. Controls: `« Previous  Page N of N  Next »`. Rows-per-page selector: 10 / 25 / 50.

### 5.4 Stage Colour Coding

| Stage | Pill Colour |
|---|---|
| Filed | Blue |
| Acknowledged | Indigo |
| ICC Preliminary Inquiry | Yellow |
| Full Investigation | Orange |
| Finding | Purple |
| Closed | Green |
| Appeal | Red |

### 5.5 Stage Pipeline View (Kanban)

Seven columns, one per stage. Each card shows:
- Complaint ID
- Branch name
- Days in current stage
- SLA badge (On Track / At Risk / Breached)
- `[View]` action button

Cards with SLA status "Breached" display a pulsing red border. Cards with "At Risk" display an amber border.

Maximum 5 cards visible per column before vertical scroll activates within the column.

---

## 6. Drawers / Modals

### 6.1 `complaint-detail` Drawer — 720 px, right-slide

**Trigger:** `[View]` button in table row or Kanban card. HTMX `hx-get` loads drawer content.

**Header:**
```
Complaint [POCSO-2526-0001]                                          [×]
[Branch Name]  ·  Filed: DD MMM YYYY  ·  Stage: [current stage pill]
⚠ SLA: [N] days remaining / BREACHED
```

**Tab Bar:**
```
[Overview]  [ICC Proceedings]  [Investigation Log]  [Mandatory Reporting]  [Documents]
```

**Tab 1 — Overview**

| Field | Value | Confidentiality |
|---|---|---|
| Complaint ID | `POCSO-2526-0001` | Public (to authorised roles) |
| Branch | [Branch Name] | Public |
| Date Received | DD MMM YYYY | Public |
| Complainant Type | Student / Staff / Parent / Anonymous | Public |
| Victim Category | Student / Staff | Public |
| Complaint Nature | [nature] | `[CONFIDENTIAL]` — masked for non-Role-90 |
| Respondent Type | Student / Staff / External | Public |
| Description | [full text] | `[CONFIDENTIAL]` — AES-256 encrypted at rest; decrypted on-screen only for Role 90 / CEO |
| Assigned ICC Member | [Name, Designation] | Public |
| ICC Case Number | [number] | Public |

Footer: `[Update Stage]` → opens `update-stage` drawer.

**Tab 2 — ICC Proceedings**

Timeline of ICC actions in reverse chronological order:

```
[Date · Time]  [User · Role]  [Action: e.g. "Preliminary Inquiry Opened"]  [Notes — CONFIDENTIAL]
```

Read-only for all roles except Role 90 who can append new entries via inline `[+ Add Entry]` button.

**Tab 3 — Investigation Log**

Full investigation step log. Same format as ICC Proceedings. Each entry shows: timestamp, investigator name, step description, outcome notes (`[CONFIDENTIAL]`). Immutable once saved.

**Tab 4 — Mandatory Reporting**

| Report Type | Required | Submitted | Date | Reference No. | Notes |
|---|---|---|---|---|---|
| NCPCR Report | Yes | ✅ / ❌ | DD MMM YYYY | [ref] | — |
| State CWC Report | Yes (if applicable) | ✅ / ❌ | — | — | — |
| Police FIR | Yes (assault cases) | ✅ / ❌ | — | [FIR No.] | — |

`[Mark as Reported]` button per row — opens a small inline form to enter reference number and date. Only Role 90.

**Tab 5 — Documents**

Document list with columns: Document Name, Type (ICC Notice / Witness Statement / Evidence / Finding Report / Compliance Certificate), Uploaded By, Date, `[Download]`.

`[Upload Document]` button — triggers a file-upload mini-form (accepts PDF, DOCX, JPG; max 20 MB).

---

### 6.2 `new-complaint` Drawer — 640 px, right-slide

**Trigger:** `[+ New Complaint]` header button.

**Header:**
```
Register New POCSO Complaint
⚠ This information is strictly confidential and access-controlled.
```

**Fields:**

| Field | Type | Required | Validation / Notes |
|---|---|---|---|
| Branch | Select | Yes | Dropdown of all branches |
| Date Received | Date picker | Yes | Cannot be future date |
| Complainant Type | Radio | Yes | Student · Staff · Parent · Anonymous |
| Victim Category | Radio | Yes | Student · Staff |
| Complaint Nature | Select | Yes | Sexual Harassment / Assault / Inappropriate Behaviour / Exposure / Other |
| Description | Textarea (encrypted) | Yes | Min 50 characters; marked `[CONFIDENTIAL]`; stored AES-256 encrypted |
| Respondent Type | Radio | Yes | Student · Staff · External |
| Assigned ICC Member | Select | No | Dropdown from ICC member register |
| ICC Case Number | Text | No | Alphanumeric; assigned by ICC admin |
| Supporting Document | File upload | No | PDF/DOCX/JPG, max 20 MB |
| Internal Notes | Textarea | No | `[CONFIDENTIAL]` — Role 90 only |

**Validation:**
- `Date Received` must not be in the future.
- `Description` minimum 50 characters enforced client-side and server-side.
- On save, system auto-generates `Complaint ID` in format `POCSO-[AY]-[NNNN]` and sets stage to "Filed".
- 24-hour SLA acknowledgment timer starts immediately upon save.
- Audit log entry created: `Complaint created by [User] at [timestamp]`.

**Footer:** `[Cancel]`  `[Save & Register Complaint ▶]`

> **Role gate for Branch Principal:** When triggered by Branch Principal, form shows only: Branch (locked to own branch), Date Received, Complainant Type, Victim Category, Complaint Nature, Description (encrypted). Respondent Type and all ICC fields hidden. After save, Branch Principal sees only the generated Complaint ID — no further access to the record.

---

### 6.3 `update-stage` Drawer — 440 px, right-slide

**Trigger:** `[Update Stage]` button in `complaint-detail` drawer footer. Only Role 90.

**Header:**
```
Update Stage — Complaint [POCSO-2526-0001]
Current Stage: [current stage pill]
```

**Fields:**

| Field | Type | Required | Validation |
|---|---|---|---|
| New Stage | Select | Yes | Only forward progression allowed (no reverting to earlier stage unless Appealed); options filtered to valid next stages |
| Stage Change Date | Date picker | Yes | Defaults to today; cannot be before current stage start date |
| Notes | Textarea | Yes | Min 20 characters; stored `[CONFIDENTIAL]` |
| Escalation Required | Checkbox | No | If checked, notification sent to Group CEO |
| Notify ICC Member | Checkbox | No | System sends email/SMS notification to assigned ICC member |

**Stage Transition Rules:**
- Filed → Acknowledged (acknowledgment must be within 24 hours of `date_received`)
- Acknowledged → ICC Preliminary Inquiry
- ICC Preliminary Inquiry → Full Investigation (preliminary inquiry finding must be attached)
- Full Investigation → Finding
- Finding → Closed or Appeal
- Appeal → Closed (only after appeal authority ruling)

Attempting to skip a stage shows inline validation error: "Stage cannot be skipped. Please complete [intermediate stage] first."

**Footer:** `[Cancel]`  `[Save Stage Update]`

On save: stage updated, audit log entry appended, SLA timer recalculated for new stage.

---

## 7. Toast Messages

| Action | Toast Text | Type |
|---|---|---|
| Complaint registered | "Complaint POCSO-[ID] registered. 24-hour acknowledgment SLA has started." | Success |
| Stage updated | "Stage updated to [Stage]. Audit log entry saved." | Success |
| Mandatory report marked | "NCPCR/Police report marked as submitted. Reference saved." | Success |
| Document uploaded | "Document '[name]' uploaded and attached to complaint [ID]." | Success |
| Escalation triggered | "Escalation notification sent to Group CEO." | Info |
| Validation error — description too short | "Description must be at least 50 characters." | Error |
| Unauthorised access attempt | "Access denied. This action requires Child Protection Officer privileges." | Error |
| SLA breach auto-detected on load | "Warning: SLA deadline breached for complaint [ID]. Immediate action required." | Warning |

---

## 8. Empty States

| Context | Illustration | Heading | Sub-text | Action |
|---|---|---|---|---|
| No complaints registered (Table View) | Shield with checkmark icon | "No POCSO Complaints Registered" | "No complaints have been recorded for this academic year. The register is active and secure." | `[Register First Complaint]` — Role 90 only |
| No complaints in a Kanban column | Empty inbox icon | "No cases at this stage" | — | None |
| No documents in complaint detail | Document icon | "No Documents Attached" | "Upload ICC notices, findings, or compliance certificates here." | `[Upload Document]` |
| No ICC proceedings logged | Timeline icon | "No Proceedings Logged" | "Add the first ICC proceeding entry to begin the audit trail." | `[+ Add Entry]` |
| Filtered results return nothing | Funnel icon | "No Complaints Match Filters" | "Adjust your filters or reset to see all complaints." | `[Reset Filters]` |

---

## 9. Loader States

| Context | Loader Behaviour |
|---|---|
| Initial page load | Full-page skeleton: KPI bar shows 5 grey shimmer cards; table shows 5 shimmer rows |
| Drawer opening (any) | Drawer slides in with inner content area showing spinner (24 px, indigo) while HTMX fetches content |
| Tab switch in `complaint-detail` | Tab content area shows spinner while HTMX fetches tab-specific data |
| `[Save & Register Complaint]` clicked | Button disabled, text changes to "Saving…", spinner replaces icon |
| `[Save Stage Update]` clicked | Button disabled, text changes to "Updating…" |
| Export / Print | Button shows spinner, disabled until file is generated server-side |
| Kanban view load | Each column loads independently with shimmer card placeholders (3 per column) |

---

## 10. Role-Based UI Visibility

| UI Element | Role 90 (CPO) | Group CEO | Role 50 (POCSO Coord.) | Branch Principal | All Others |
|---|---|---|---|---|---|
| KPI Summary Bar | Full | Full | Partial (counts only, no breach details) | Hidden | Hidden |
| Complaint table — all rows | Visible | Visible | Visible (masked confidential fields) | Not accessible | Not accessible |
| Complaint ID column | Visible | Visible | Visible | Own-triggered only | Hidden |
| `[CONFIDENTIAL]` fields | Decrypted, visible | Decrypted, visible | `████████` masking | Not visible | Not visible |
| `[View]` action button | Visible | Visible | Visible | Not visible | Not visible |
| `[+ New Complaint]` button | Visible | Hidden | Hidden | Visible (limited form) | Hidden |
| `[Export ↓]` button | Visible | Visible | Hidden | Hidden | Hidden |
| `[Update Stage]` button | Visible | Hidden | Hidden | Hidden | Hidden |
| `[Mark as Reported]` (Mand. Reporting tab) | Visible | Hidden | Hidden | Hidden | Hidden |
| `[Upload Document]` (Documents tab) | Visible | Hidden | Hidden | Hidden | Hidden |
| ICC Proceedings — `[+ Add Entry]` | Visible | Hidden | Hidden | Hidden | Hidden |
| Alert banner | Full detail | Full detail | Counts only | Not shown | Not shown |
| Kanban view toggle | Visible | Visible | Visible | Hidden | Hidden |
| `[Escalation Required]` checkbox | Visible | Hidden | Hidden | Hidden | Hidden |

---

## 11. API Endpoints

### 11.1 List & Filter Complaints
```
GET /api/v1/group/{group_id}/welfare/pocso/complaints/
```

| Query Parameter | Type | Description |
|---|---|---|
| `branch_id` | integer | Filter by branch |
| `stage` | string | `filed` · `acknowledged` · `preliminary_inquiry` · `full_investigation` · `finding` · `closed` · `appeal` |
| `sla_status` | string | `on_track` · `at_risk` · `breached` |
| `complainant_type` | string | `student` · `staff` · `parent` · `anonymous` |
| `victim_category` | string | `student` · `staff` |
| `date_from` | date (YYYY-MM-DD) | Filter `date_received` from |
| `date_to` | date (YYYY-MM-DD) | Filter `date_received` to |
| `search` | string | Searches `complaint_id` and `branch.short_name` |
| `page` | integer | Pagination page number (default: 1) |
| `page_size` | integer | Rows per page; 10 · 25 · 50 (default: 10) |
| `ordering` | string | `date_received` · `-date_received` · `days_since_filing` · `complaint_id` |

**Response:** 200 OK — paginated list; confidential fields omitted or encrypted based on role.

### 11.2 Retrieve Complaint Detail
```
GET /api/v1/group/{group_id}/welfare/pocso/complaints/{complaint_id}/
```
Returns full complaint object. Confidential fields (`description`, `complaint_nature`, `witness_notes`, `finding_text`) are decrypted only if `request.user.role_id in [90, 'ceo']`; otherwise returned as `null`.

### 11.3 Create Complaint
```
POST /api/v1/group/{group_id}/welfare/pocso/complaints/
```
Body: `branch`, `date_received`, `complainant_type`, `victim_category`, `complaint_nature`, `description` (plaintext — server encrypts before storage), `respondent_type`, `assigned_icc_member` (optional), `icc_case_number` (optional).
Response: 201 Created — returns `complaint_id`, `stage: "filed"`, `sla_ack_deadline`.

### 11.4 Update Stage
```
PATCH /api/v1/group/{group_id}/welfare/pocso/complaints/{complaint_id}/stage/
```
Body: `new_stage`, `stage_change_date`, `notes` (encrypted before storage), `escalate` (bool), `notify_icc` (bool).
Response: 200 OK — updated complaint object.

### 11.5 Log Proceeding / Investigation Entry
```
POST /api/v1/group/{group_id}/welfare/pocso/complaints/{complaint_id}/proceedings/
POST /api/v1/group/{group_id}/welfare/pocso/complaints/{complaint_id}/investigation-log/
```
Body: `entry_date`, `entered_by`, `action`, `notes` (encrypted).
Response: 201 Created.

### 11.6 Mark Mandatory Report
```
PATCH /api/v1/group/{group_id}/welfare/pocso/complaints/{complaint_id}/mandatory-reporting/
```
Body: `report_type` (`ncpcr` · `state_cwc` · `police`), `submitted_on`, `reference_number`, `fir_number` (police only).
Response: 200 OK.

### 11.7 Document Upload
```
POST /api/v1/group/{group_id}/welfare/pocso/complaints/{complaint_id}/documents/
```
Body: `multipart/form-data` — `file`, `document_type`, `description`.
Response: 201 Created — returns `document_id`, `file_url`.

### 11.8 KPI Summary
```
GET /api/v1/group/{group_id}/welfare/pocso/complaints/kpi-summary/
```
Query params: `academic_year` (optional, defaults to current).
Response: `{ total_this_ay, active_cases, ack_compliance_pct, mandatory_reporting_pct, sla_breach_count }`.

### 11.9 Kanban Data
```
GET /api/v1/group/{group_id}/welfare/pocso/complaints/kanban/
```
Returns complaints grouped by stage. Confidential field masking same as list endpoint.

---

## 12. HTMX Patterns

### 12.1 Table Initialisation
```html
<div id="pocso-complaint-table"
     hx-get="/api/v1/group/{{ group_id }}/welfare/pocso/complaints/?page=1&page_size=10"
     hx-trigger="load"
     hx-swap="innerHTML"
     hx-indicator="#table-spinner">
  <!-- skeleton rows rendered server-side until HTMX fires -->
</div>
```

### 12.2 Filter Application (debounced search + filter dropdowns)
```html
<input id="complaint-search"
       name="search"
       hx-get="/api/v1/group/{{ group_id }}/welfare/pocso/complaints/"
       hx-trigger="input changed delay:500ms, search"
       hx-target="#pocso-complaint-table"
       hx-swap="innerHTML"
       hx-include="#filter-branch, #filter-stage, #filter-sla, #filter-complainant-type, #filter-date-from, #filter-date-to"
       placeholder="Search Complaint ID or Branch…">
```

### 12.3 Complaint Detail Drawer
```html
<button hx-get="/htmx/welfare/pocso/complaints/{{ complaint_id }}/detail/"
        hx-target="#drawer-container"
        hx-swap="innerHTML"
        hx-trigger="click"
        class="text-indigo-600 hover:underline text-sm font-medium">
  View
</button>
```

### 12.4 Drawer Tab Switching
```html
<button hx-get="/htmx/welfare/pocso/complaints/{{ complaint_id }}/tab/icc-proceedings/"
        hx-target="#drawer-tab-content"
        hx-swap="innerHTML"
        hx-trigger="click"
        class="drawer-tab-btn">
  ICC Proceedings
</button>
```

### 12.5 New Complaint Form Submission
```html
<form hx-post="/api/v1/group/{{ group_id }}/welfare/pocso/complaints/"
      hx-target="#pocso-complaint-table"
      hx-swap="innerHTML"
      hx-on::after-request="closeDrawer(); showToast(event)">
  <!-- form fields -->
  <button type="submit"
          hx-disabled-elt="this"
          class="btn-primary">
    Save &amp; Register Complaint ▶
  </button>
</form>
```

### 12.6 Stage Update Form Submission
```html
<form hx-patch="/api/v1/group/{{ group_id }}/welfare/pocso/complaints/{{ complaint_id }}/stage/"
      hx-target="#drawer-tab-content"
      hx-swap="innerHTML"
      hx-on::after-request="refreshTable(); showToast(event)">
```

### 12.7 KPI Summary Auto-Refresh (every 5 minutes)
```html
<div id="kpi-bar"
     hx-get="/api/v1/group/{{ group_id }}/welfare/pocso/complaints/kpi-summary/"
     hx-trigger="load, every 300s"
     hx-swap="innerHTML">
</div>
```

### 12.8 Kanban View Toggle
```html
<button id="toggle-kanban"
        hx-get="/htmx/welfare/pocso/complaints/kanban/"
        hx-target="#view-container"
        hx-swap="innerHTML"
        hx-trigger="click">
  ⬜ Stage Pipeline View
</button>
```

### 12.9 Mandatory Report Inline Mark
```html
<button hx-patch="/api/v1/welfare/pocso/complaints/{{ complaint_id }}/mandatory-reporting/"
        hx-vals='{"report_type": "ncpcr"}'
        hx-target="#mandatory-reporting-tab"
        hx-swap="innerHTML"
        hx-confirm="Mark NCPCR report as submitted? This action is permanent."
        class="btn-sm btn-success">
  Mark as Reported
</button>
```

### 12.10 Document Upload Progress
```html
<form hx-post="/api/v1/welfare/pocso/complaints/{{ complaint_id }}/documents/"
      hx-encoding="multipart/form-data"
      hx-target="#documents-list"
      hx-swap="beforeend"
      hx-indicator="#upload-spinner">
  <input type="file" name="file" accept=".pdf,.docx,.jpg">
  <button type="submit" class="btn-outline">Upload</button>
</form>
```

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
