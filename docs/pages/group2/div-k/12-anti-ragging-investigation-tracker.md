# 12 — Anti-Ragging Investigation Tracker

> **URL:** `/group/welfare/anti-ragging/investigations/`
> **File:** `12-anti-ragging-investigation-tracker.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Role:** Group Anti-Ragging Committee Head (Role 91, G3)

---

## 1. Purpose

Dedicated workspace for managing the active investigation process for all anti-ragging complaints that are currently in the Preliminary Inquiry or Full Investigation stages. While the Complaint Register (File 11) provides a full historical view of all complaints including closed cases, this page focuses exclusively on the cases that demand daily action — the open investigation pipeline.

The Anti-Ragging Committee Head uses this page as a daily operations board during active investigations. Core activities managed here include: assigning committee members to specific cases, recording witness interview schedules and outcomes, logging physical and digital evidence with chain-of-custody tracking, scheduling hearings (witness interviews, evidence presentations, final hearings), tracking SLA compliance at each investigation step, and compiling the formal investigation report. Every step entered in this tracker is time-stamped and immutable once saved, ensuring a tamper-proof investigation record that can withstand judicial or regulatory scrutiny.

The anonymisation scheme from the Complaint Register is maintained throughout — complainants and accused are referred to by their codes (`COMP-NNNN`, `ACC-NNNN`). No real names appear in the investigation tracker view (real names are accessible only in the `investigation-workspace` drawer under the full Case Summary tab, visible only to Role 91). Scale: 0–10 active investigations at any one time; investigation quality matters far more than quantity.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Anti-Ragging Committee Head | G3, Role 91 | Full — all actions, all drawers, all evidence, report generation | Primary owner |
| Group CEO | G4 | View only — investigation list; workspace tabs (no witness names or evidence detail) | No edit capability |
| Branch Principal | Branch-level | View — own branch investigations only; cannot see witness details or evidence | Read-only; scoped to own branch |
| Committee Member (assigned) | Branch-level | View — own assigned cases only; can view workspace (own case); cannot edit committee composition | Limited drawer access |
| Group Legal & Compliance Officer | G3 | View — all investigations; full workspace read access | No edit capability |
| All other roles | — | No access | Redirected to own dashboard |

> **Access enforcement:** Django decorator `@require_role(['anti_ragging_head'])` for all write actions. Committee member queryset: `investigations.filter(committee_members__user=request.user)`. Branch Principal queryset: `investigations.filter(branch=request.user.branch)`. Witness names and real complainant/accused identities visible only to Role 91.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Welfare & Safety  ›  Anti-Ragging  ›  Investigation Tracker
```

### 3.2 Page Header
```
Anti-Ragging Investigation Tracker                [Schedule Hearing]  [Add Evidence]  [Export ↓]
Group Anti-Ragging Committee Head — [Officer Name]
[N] Active Investigations  ·  [N] Preliminary Inquiries  ·  [N] Full Investigations  ·  Updated: [timestamp]
```

`[Schedule Hearing]` — opens `schedule-hearing` drawer (defaults to no pre-selected case; case must be selected in drawer).
`[Add Evidence]` — opens `add-evidence` drawer (defaults to no pre-selected case).
`[Export ↓]` — exports investigation tracker table to PDF/XLSX.

### 3.3 Alert Banner (conditional)

| Condition | Banner Text | Severity |
|---|---|---|
| Preliminary Inquiry SLA breached | "[N] Preliminary Inquiry/Inquiries have exceeded the 7-working-day deadline. Immediate escalation required." | Red |
| Full Investigation SLA breached | "[N] Full Investigation(s) have exceeded the 30-day deadline. UGC compliance breach." | Red |
| Hearing scheduled today | "Hearing scheduled today for Investigation [ID] at [HH:MM] — [location/mode]." | Amber |
| No committee member assigned | "Investigation [ID] has no committee member assigned. Assign before proceeding." | Amber |
| Report draft overdue | "Investigation [ID] has reached Finding stage but no report draft exists." | Amber |
| No active investigations | "No active investigations. All complaints are either closed or at filing stage." | Blue (informational) |

---

## 4. KPI Summary Bar

Five metric cards displayed horizontally.

| Card | Metric | Colour Rule |
|---|---|---|
| Active Investigations | Count of investigations where stage ∈ {Preliminary Inquiry, Full Investigation} | Red if > 5; Amber if 1–5; Green if 0 |
| Preliminary Inquiries Overdue | Count exceeding 7 working days without completion | Red if > 0; Green if 0 |
| Full Investigations Overdue | Count exceeding 30 days without completion | Red if > 0; Green if 0 |
| Avg Days to Complete (This AY) | Average calendar days from complaint filing to case closure for completed investigations | Green if ≤ 30; Amber if 31–45; Red if > 45 |
| Reports Generated | Count of formal investigation reports compiled and downloaded this AY | Grey (informational) |

```
┌───────────────────┐ ┌───────────────────┐ ┌───────────────────┐ ┌───────────────────┐ ┌───────────────────┐
│ Active Invest.    │ │ Prelim. Overdue   │ │ Full Inv. Overdue │ │ Avg Days (AY)     │ │ Reports Generated │
│        4          │ │        1          │ │        0          │ │      22 days       │ │        6          │
│   ● Amber         │ │   ● Red           │ │   ● Green         │ │   ● Green          │ │   ● Grey          │
└───────────────────┘ └───────────────────┘ └───────────────────┘ └───────────────────┘ └───────────────────┘
```

---

## 5. Sections

### 5.1 Filters and Search Bar

```
[🔍 Search by Investigation ID / Committee Lead]  [Stage ▾]  [Branch ▾]  [SLA Status ▾]  [Committee Lead ▾]  [Reset Filters]
```

| Filter | Options |
|---|---|
| Stage | All / Preliminary Inquiry / Full Investigation |
| Branch | All Branches / individual branch names |
| SLA Status | All / On Track / At Risk / Breached |
| Committee Lead | All / individual committee members (dropdown from assigned leads) |

### 5.2 Investigation Tracker Table

Columns, sortable where marked (▲▼):

| Column | Source Field | Sortable | Notes |
|---|---|---|---|
| Investigation ID | `complaint_id` (= investigation ID) | ▲▼ | Format: `AR-2526-NNNN`; hyperlink → opens `investigation-workspace` drawer |
| Branch | `branch.short_name` | ▲▼ | — |
| Complainant Code | `complainant_code` | — | Anonymised; `COMP-NNNN` |
| Accused Code | `accused_code` | — | Anonymised; `ACC-NNNN` |
| Stage | `current_stage` | ▲▼ | Pill: Preliminary Inquiry (Yellow) · Full Investigation (Orange) |
| Committee Lead | `committee_lead.name` | ▲▼ | Full name or "Unassigned" (red text) |
| Investigation Start Date | `investigation_start_date` | ▲▼ | DD MMM YYYY |
| Preliminary Due | `preliminary_due_date` | ▲▼ | DD MMM YYYY; Red if overdue |
| Full Investigation Due | `full_investigation_due_date` | ▲▼ | DD MMM YYYY; Red if overdue; "—" if still in Preliminary |
| Days Remaining | Computed | ▲▼ | Days to nearest active SLA deadline; Red if negative |
| Hearings Scheduled | Count | — | Integer; "0" if none |
| Witnesses Interviewed | Count | — | Integer |
| Evidence Items | Count | — | Integer |
| SLA Status | Computed | — | Pill: On Track (Green) · At Risk (Amber) · Breached (Red) |
| Actions | — | — | [Open Workspace] · [Schedule Hearing] · [Add Evidence] · [Generate Report] |

**Default sort:** SLA Status (Breached first, At Risk next, On Track last) then `days_remaining` ascending.

**Pagination:** 10 rows per page (low volume expected). Controls: `« Previous  Page N of N  Next »`.

### 5.3 SLA Status Definitions (same logic as Complaint Register §5.4)

| Status | Condition |
|---|---|
| On Track | Days remaining > 20% of total allowed period |
| At Risk | Days remaining ≤ 20% of allowed period but deadline not yet passed |
| Breached | Deadline has passed; investigation not complete |

---

## 6. Drawers / Modals

### 6.1 `investigation-workspace` Drawer — 800 px, full right panel

**Trigger:** `[Open Workspace]` in table row or click on Investigation ID link.

**Header:**
```
Investigation Workspace — [AR-2526-0003]                           [×]
[Branch Name]  ·  Stage: [stage pill]  ·  SLA: [N] days remaining / BREACHED
Committee Lead: [Name]  ·  Start: DD MMM YYYY
```

**Tab Bar:**
```
[Case Summary]  [Committee]  [Witness Log]  [Evidence]  [Hearings]  [Timeline]  [Report Draft]
```

**Tab 1 — Case Summary**

Full case overview. Includes real complainant and accused names (Role 91 only; all other roles see codes only):

| Field | Value | Visibility |
|---|---|---|
| Complaint ID | AR-2526-0003 | All |
| Branch | [Branch Name] | All |
| Nature | Verbal / Physical / etc. | All |
| Complainant Name | [Full Name] | Role 91 only; others see `COMP-0003` |
| Accused Name | [Full Name] | Role 91 only; others see `ACC-0003` |
| Description | [full text — CONFIDENTIAL] | Role 91 and CEO only |
| Source | Online Form / Helpline / etc. | All |
| Date Received | DD MMM YYYY | All |
| Current Stage | [stage] | All |

**Tab 2 — Committee**

Table of committee members assigned to this investigation:

| Column | Notes |
|---|---|
| Name | Full name |
| Designation | — |
| Branch | Home branch |
| Role in Investigation | Lead · Member · Observer |
| Assigned Date | DD MMM YYYY |
| Actions | `[Remove]` (Role 91 only) |

`[+ Add Committee Member]` button — inline search-select form. Role 91 only. Prevents adding the same person twice.

**Tab 3 — Witness Log**

Table of all witnesses:

| Column | Notes |
|---|---|
| Witness Code | `WIT-NNNN` (anonymised in shared views; real name shown to Role 91) |
| Interview Date | DD MMM YYYY |
| Interview Mode | In-person · Video call · Written statement |
| Interviewed By | Committee member name |
| Statement Summary | `[CONFIDENTIAL]` — Role 91 and CEO; masked for others |
| Actions | `[View Full Statement]` (Role 91 only) |

`[+ Add Witness Interview]` button — inline form (date, mode, interviewed by, statement — encrypted). Each entry is immutable once saved.

**Tab 4 — Evidence**

Table of all evidence items:

| Column | Notes |
|---|---|
| Evidence ID | Auto `EV-NNNN` |
| Type | Document · CCTV Footage · Physical Item · Testimony |
| Description | Brief description |
| Collected By | Officer / committee member |
| Collection Date | DD MMM YYYY |
| Chain of Custody | Link to custody log |
| Actions | `[Download]` (documents/CCTV) · `[View Custody Log]` |

`[+ Add Evidence]` button — opens `add-evidence` drawer pre-filled with this Investigation ID.

**Tab 5 — Hearings**

Table of all scheduled and completed hearings:

| Column | Notes |
|---|---|
| Hearing Date | DD MMM YYYY |
| Hearing Time | HH:MM |
| Type | Witness Interview · Evidence Presentation · Final Hearing |
| Participants | Comma-separated list (codes for non-Role-91) |
| Venue / Mode | Location or "Video call" |
| Status | Scheduled · Completed · Postponed |
| Outcome | Brief outcome notes (Role 91 only) |
| Actions | `[Edit]` (if Scheduled) · `[Mark Complete]` · `[Cancel]` |

`[+ Schedule Hearing]` button — opens `schedule-hearing` drawer pre-filled with this Investigation ID.

**Tab 6 — Timeline**

Chronological, immutable event log (combined view of all actions across all tabs):
```
[DD MMM YYYY · HH:MM]  [Action type badge]  [Description]  [Entered by]
```
Colour-coded by action type: Committee (Blue) · Witness (Purple) · Evidence (Orange) · Hearing (Teal) · Stage Change (Red) · System (Grey).

No editing allowed in Timeline tab — it is a read-only audit stream.

**Tab 7 — Report Draft**

A structured report template pre-populated with data from all other tabs. Sections of the template:

1. **Case Header** (auto-filled): Investigation ID, Branch, Complaint Date, Stage
2. **Summary of Complaint** (editable textarea — Role 91 only)
3. **Committee Composition** (auto-filled from Committee tab)
4. **Proceedings Summary** (auto-filled from Witness Log + Hearings)
5. **Evidence Summary** (auto-filled from Evidence tab)
6. **Findings** (editable textarea — Role 91 only)
7. **Recommendations** (editable textarea — Role 91 only)

`[Save Draft]` — saves editable sections. `[Generate PDF Report]` — opens `generate-report` drawer.

---

### 6.2 `schedule-hearing` Drawer — 520 px, right-slide

**Trigger:** `[Schedule Hearing]` header button, `[+ Schedule Hearing]` in Hearings tab, or table row action.

**Header:**
```
Schedule Hearing
```

**Fields:**

| Field | Type | Required | Validation |
|---|---|---|---|
| Investigation ID | Select (or pre-filled) | Yes | Dropdown of active investigations |
| Hearing Type | Select | Yes | Witness Interview · Evidence Presentation · Final Hearing |
| Date | Date picker | Yes | Cannot be past date |
| Time | Time picker | Yes | HH:MM format; 09:00–18:00 range |
| Duration (minutes) | Number | Yes | Min 30, max 480 |
| Venue / Mode | Text | Yes | Physical location name or "Video call (link below)" |
| Video Call Link | URL | Conditional | Shown only if mode contains "Video call" |
| Participants | Multi-select search | Yes | Search committee members, witnesses (by code); Role 91 sees real names |
| Notification Channel | Checkbox group | No | Email · SMS · Portal notification |
| Notes | Textarea | No | Pre-hearing instructions or agenda |

**Validation:**
- `Date` must be within the active SLA period; if hearing date falls after SLA deadline, inline warning: "This hearing is scheduled after the investigation SLA deadline of [date]."
- At least one participant must be selected.

**Footer:** `[Cancel]`  `[Schedule Hearing & Notify Participants]`

On save: hearing record created; notifications sent to selected participants via chosen channels.

---

### 6.3 `add-evidence` Drawer — 440 px, right-slide

**Trigger:** `[Add Evidence]` header button, `[+ Add Evidence]` in Evidence tab, or table row action.

**Header:**
```
Add Evidence
All evidence entries are permanent and immutable once saved.
```

**Fields:**

| Field | Type | Required | Validation / Notes |
|---|---|---|---|
| Investigation ID | Select (or pre-filled) | Yes | Dropdown of active investigations |
| Evidence Type | Select | Yes | Document · CCTV Footage · Physical Item · Testimony |
| Evidence Description | Textarea | Yes | Min 20 characters |
| Collected By | Select | Yes | Committee member name |
| Collection Date | Date picker | Yes | Cannot be future date |
| Collection Location | Text | Yes | Where evidence was collected/obtained |
| File Upload | File upload | Conditional | Required for Document and CCTV Footage types; PDF/MP4/JPG/MOV; max 100 MB |
| Physical Item Description | Textarea | Conditional | Required for Physical Item type; stored as descriptive record |
| Chain of Custody — Initial Custodian | Select | Yes | Person currently holding/storing the evidence |
| Chain of Custody — Storage Location | Text | Yes | Physical location (locker/room) or digital storage path |
| Notes | Textarea | No | Additional context |

**Chain of Custody Tracking:**
Once evidence is saved, a custody log is automatically created:
```
[Collected by: X · DD MMM YYYY] → [Transferred to: Y (if transferred)]
```
Any subsequent custody transfer is logged by adding a new entry via `[Log Transfer]` in the Evidence tab.

**Validation:**
- File type validation per evidence type: Document accepts PDF/DOCX; CCTV Footage accepts MP4/MOV/AVI; Physical Item has no file (description only); Testimony accepts PDF.
- Evidence entries are immutable once saved. No edit or delete permitted.
- On save: Evidence ID auto-generated; Timeline entry auto-appended.

**Footer:** `[Cancel]`  `[Save Evidence — Permanent Record]`

Pre-save confirmation: "Evidence once saved cannot be edited or deleted. Confirm all details are correct." `[Cancel]` · `[Confirm & Save]`

---

### 6.4 `generate-report` Drawer — 560 px, right-slide

**Trigger:** `[Generate PDF Report]` button in Report Draft tab of `investigation-workspace`. Role 91 only.

**Header:**
```
Generate Investigation Report — [AR-2526-0003]
This report will compile all case data into a formal PDF. Verify all sections before generating.
```

**Pre-generation Checklist (auto-validated — each item shows ✅ or ❌):**
- [ ] Committee composition recorded
- [ ] At least one witness interview logged
- [ ] At least one evidence item logged
- [ ] At least one final hearing conducted and marked Complete
- [ ] Findings section in Report Draft is not empty
- [ ] Recommendations section in Report Draft is not empty

If any item is ❌, a warning is shown but generation is not blocked (Role 91 may override with confirmation).

**Report Options:**

| Field | Type | Notes |
|---|---|---|
| Report Title | Text | Pre-filled: "Anti-Ragging Investigation Report — [AR-ID]" |
| Report Date | Date picker | Defaults to today |
| Prepared By | Text | Auto-filled with Role 91 user's full name and designation |
| Include Witness Names | Toggle | Default: Off (codes only); On = real names included for judicial submission version |
| Include Evidence Files | Toggle | Default: Off (summary only); On = attachments included in PDF |
| Letterhead | Select | Group letterhead / Branch letterhead / Plain |
| Footer Note | Textarea | Optional legal or procedural note to append |

**Footer:** `[Cancel]`  `[Generate & Download PDF]`

On generate: PDF compiled server-side using all saved data from workspace tabs. Report generation logged in Timeline. File downloaded to browser. A copy is stored as a document in the case's Document store. Role 91 may regenerate; each version is numbered.

---

## 7. Toast Messages

| Action | Toast Text | Type |
|---|---|---|
| Hearing scheduled | "Hearing scheduled for Investigation [ID] on [date] at [time]. Participants notified." | Success |
| Evidence saved | "Evidence item [EV-ID] permanently recorded for Investigation [ID]." | Success |
| Committee member added | "[Name] added to Investigation [ID] committee." | Success |
| Witness interview logged | "Witness interview entry recorded for Investigation [ID]. Entry is permanent." | Success |
| Report draft saved | "Report draft saved for Investigation [ID]." | Success |
| PDF report generated | "Investigation Report for [AR-ID] generated. Download will start shortly." | Success |
| Hearing marked complete | "Hearing of DD MMM YYYY marked as complete." | Info |
| SLA breach auto-detected | "Warning: SLA breached for Investigation [ID]. Escalation recommended." | Warning |
| Evidence save blocked — file type invalid | "Invalid file type. CCTV footage must be MP4, MOV, or AVI." | Error |
| Pre-report checklist failures (override) | "[N] checklist item(s) incomplete. Report generated with warnings." | Warning |
| Unauthorised action | "Access denied. Investigation management requires Anti-Ragging Committee Head privileges." | Error |

---

## 8. Empty States

| Context | Illustration | Heading | Sub-text | Action |
|---|---|---|---|---|
| No active investigations | Clipboard with checkmark | "No Active Investigations" | "All complaints are either at the filing stage or have been closed. This tracker shows only open investigations." | Link: `[View All Complaints ↗]` (to File 11) |
| No results match filters | Funnel icon | "No Investigations Match Filters" | "Adjust your stage, branch, or SLA filter to find the investigations you need." | `[Reset Filters]` |
| Committee tab — no members | People icon | "No Committee Members Assigned" | "Assign committee members before proceeding with this investigation." | `[+ Add Committee Member]` (Role 91) |
| Witness log — no entries | Speech bubble icon | "No Witness Interviews Logged" | "Log the first witness interview to build the investigation record." | `[+ Add Witness Interview]` (Role 91) |
| Evidence tab — no items | Archive box icon | "No Evidence Items Recorded" | "Add evidence items collected during this investigation." | `[+ Add Evidence]` (Role 91) |
| Hearings tab — no hearings | Calendar icon | "No Hearings Scheduled" | "Schedule the first hearing to begin the formal inquiry process." | `[+ Schedule Hearing]` (Role 91) |
| Report draft — findings empty | Document icon | "Findings Not Recorded" | "Complete the Findings and Recommendations sections to generate the formal report." | None |

---

## 9. Loader States

| Context | Loader Behaviour |
|---|---|
| Initial page load | KPI bar: 5 shimmer cards. Table: 6 shimmer rows with action column placeholders |
| Filter application | Table replaced by spinner (20 px, indigo) while HTMX fetches |
| Investigation workspace opening | Full 800 px panel slides in; inner content shows large spinner until HTMX loads Case Summary tab |
| Tab switching in workspace | Tab body area shows spinner while HTMX fetches tab-specific data |
| `[Schedule Hearing]` drawer opening | 520 px drawer slides in with spinner |
| `[Add Evidence]` file upload | Progress bar per file: "Uploading [filename]… [N]%" |
| `[Generate & Download PDF]` | Button disabled, text: "Generating Report…"; spinner; may take 5–15 seconds server-side |
| Committee member search-select | Inline search input shows "Searching…" with spinner on each keypress (debounced 300 ms) |
| Timeline tab load | Shimmer event rows appear while HTMX fetches combined audit stream |

---

## 10. Role-Based UI Visibility

| UI Element | Role 91 (AR Head) | Group CEO | Branch Principal | Committee Member | Legal Compliance | All Others |
|---|---|---|---|---|---|---|
| KPI Summary Bar | Full | Full | Own branch KPIs | Assigned case counts only | Full | Hidden |
| Investigation table — all branches | Visible | Visible | Own branch only | Own assigned cases | Visible | Hidden |
| Real complainant / accused names | Visible (in workspace) | Hidden | Hidden | Hidden | Hidden | Hidden |
| `[Open Workspace]` action | Visible | Visible | Visible (own branch) | Visible (own case) | Visible | Hidden |
| `[Schedule Hearing]` action / button | Visible | Hidden | Hidden | Hidden | Hidden | Hidden |
| `[Add Evidence]` action / button | Visible | Hidden | Hidden | Hidden | Hidden | Hidden |
| `[Generate Report]` action | Visible | Hidden | Hidden | Hidden | Hidden | Hidden |
| `[Export ↓]` button | Visible | Visible | Visible (own branch) | Hidden | Visible | Hidden |
| Workspace — Committee tab `[+ Add]` / `[Remove]` | Visible | Hidden | Hidden | Hidden | Hidden | Hidden |
| Workspace — Witness Log `[+ Add]` | Visible | Hidden | Hidden | Hidden | Hidden | Hidden |
| Witness statement full text | Visible | Hidden | Hidden | Hidden | Hidden | Hidden |
| Workspace — Evidence `[+ Add]` | Visible | Hidden | Hidden | Hidden | Hidden | Hidden |
| Workspace — Report Draft (editable sections) | Editable | Read-only | Read-only | Read-only | Read-only | Hidden |
| Alert banner | Full detail | Full detail | Own branch only | Own case only | Full detail | Hidden |

---

## 11. API Endpoints

### 11.1 List Active Investigations
```
GET /api/v1/welfare/anti-ragging/investigations/
```

| Query Parameter | Type | Description |
|---|---|---|
| `stage` | string | `preliminary_inquiry` · `full_investigation` |
| `branch_id` | integer | Filter by branch |
| `sla_status` | string | `on_track` · `at_risk` · `breached` |
| `committee_lead_id` | integer | Filter by assigned committee lead user ID |
| `search` | string | Searches `complaint_id` and `committee_lead.name` |
| `page` | integer | Default: 1 |
| `page_size` | integer | 10 · 25 (default: 10) |
| `ordering` | string | `sla_status` · `days_remaining` · `investigation_start_date` · `stage` |

### 11.2 Retrieve Investigation Workspace Data
```
GET /api/v1/welfare/anti-ragging/investigations/{complaint_id}/
```
Returns full investigation object. Real names in `complainant_name` and `accused_name` fields returned only for Role 91.

### 11.3 Get Committee Members
```
GET /api/v1/welfare/anti-ragging/investigations/{complaint_id}/committee/
```

### 11.4 Add / Remove Committee Member
```
POST   /api/v1/welfare/anti-ragging/investigations/{complaint_id}/committee/
DELETE /api/v1/welfare/anti-ragging/investigations/{complaint_id}/committee/{member_id}/
```

### 11.5 Add Witness Interview Log Entry
```
POST /api/v1/welfare/anti-ragging/investigations/{complaint_id}/witnesses/
```
Body: `interview_date`, `mode`, `interviewed_by`, `statement` (encrypted). Returns 201 Created; entry is immutable.

### 11.6 Get Evidence Items
```
GET /api/v1/welfare/anti-ragging/investigations/{complaint_id}/evidence/
```

### 11.7 Add Evidence
```
POST /api/v1/welfare/anti-ragging/investigations/{complaint_id}/evidence/
```
Body: `multipart/form-data` — `evidence_type`, `description`, `collected_by`, `collection_date`, `collection_location`, `file` (optional), `initial_custodian`, `storage_location`, `notes`.
Response: 201 Created; immutable.

### 11.8 Log Evidence Custody Transfer
```
POST /api/v1/welfare/anti-ragging/investigations/{complaint_id}/evidence/{evidence_id}/custody-transfer/
```
Body: `transferred_to`, `transfer_date`, `reason`.

### 11.9 Schedule Hearing
```
POST /api/v1/welfare/anti-ragging/investigations/{complaint_id}/hearings/
```
Body: `hearing_type`, `date`, `time`, `duration_minutes`, `venue_mode`, `video_call_link` (optional), `participant_ids[]`, `notification_channels[]`, `notes`.

### 11.10 Update Hearing Status
```
PATCH /api/v1/welfare/anti-ragging/investigations/{complaint_id}/hearings/{hearing_id}/
```
Body: `status` (`completed` · `postponed` · `cancelled`), `outcome_notes` (optional, encrypted).

### 11.11 Save / Update Report Draft
```
PUT /api/v1/welfare/anti-ragging/investigations/{complaint_id}/report-draft/
```
Body: `summary_of_complaint`, `findings`, `recommendations`, `report_date`.

### 11.12 Generate PDF Report
```
POST /api/v1/welfare/anti-ragging/investigations/{complaint_id}/generate-report/
```
Body: `report_title`, `report_date`, `include_witness_names` (bool), `include_evidence_files` (bool), `letterhead`, `footer_note`.
Response: PDF file download stream + `{ report_version, generated_at }`.

### 11.13 Get Investigation Timeline
```
GET /api/v1/welfare/anti-ragging/investigations/{complaint_id}/timeline/
```
Returns chronological list of all events across committee, witness, evidence, hearing, and stage-change actions.

### 11.14 KPI Summary
```
GET /api/v1/welfare/anti-ragging/investigations/kpi-summary/
```
Response: `{ active_investigations, preliminary_overdue, full_investigation_overdue, avg_days_to_complete, reports_generated }`.

---

## 12. HTMX Patterns

### 12.1 Table Initialisation
```html
<div id="investigation-table"
     hx-get="/api/v1/welfare/anti-ragging/investigations/?page=1&page_size=10"
     hx-trigger="load"
     hx-swap="innerHTML"
     hx-indicator="#table-spinner">
</div>
```

### 12.2 Filter Application
```html
<select name="sla_status"
        id="filter-sla"
        hx-get="/api/v1/welfare/anti-ragging/investigations/"
        hx-trigger="change"
        hx-target="#investigation-table"
        hx-swap="innerHTML"
        hx-include="#filter-stage, #filter-branch, #filter-committee-lead, #search-input">
</select>
```

### 12.3 Investigation Workspace — Full Panel Open
```html
<a hx-get="/htmx/welfare/anti-ragging/investigations/{{ complaint_id }}/workspace/"
   hx-target="#workspace-panel"
   hx-swap="innerHTML"
   hx-trigger="click"
   class="text-indigo-700 font-semibold hover:underline cursor-pointer">
  {{ complaint_id }}
</a>
```

### 12.4 Workspace Tab Switching
```html
<button hx-get="/htmx/welfare/anti-ragging/investigations/{{ complaint_id }}/tab/witnesses/"
        hx-target="#workspace-tab-content"
        hx-swap="innerHTML"
        hx-trigger="click"
        class="workspace-tab-btn">
  Witness Log
</button>
```

### 12.5 Add Committee Member (Inline Search-Select)
```html
<input name="member_search"
       hx-get="/api/v1/welfare/anti-ragging/investigations/member-search/"
       hx-trigger="input changed delay:300ms"
       hx-target="#member-search-results"
       hx-swap="innerHTML"
       placeholder="Search committee member…">
<div id="member-search-results"></div>
```

### 12.6 Schedule Hearing Form
```html
<form hx-post="/api/v1/welfare/anti-ragging/investigations/{{ complaint_id }}/hearings/"
      hx-target="#hearings-tab-content"
      hx-swap="innerHTML"
      hx-on::after-request="closeDrawer(); showToast(event);">
</form>
```

### 12.7 Add Evidence Form with File Upload
```html
<form hx-post="/api/v1/welfare/anti-ragging/investigations/{{ complaint_id }}/evidence/"
      hx-encoding="multipart/form-data"
      hx-target="#evidence-tab-content"
      hx-swap="innerHTML"
      hx-confirm="Evidence once saved cannot be edited or deleted. Confirm all details are correct."
      hx-on::after-request="closeDrawer(); showToast(event);">
</form>
```

### 12.8 Evidence Type Conditional Fields
```html
<select name="evidence_type"
        hx-get="/htmx/welfare/anti-ragging/investigations/evidence-fields/"
        hx-target="#evidence-conditional-fields"
        hx-swap="innerHTML"
        hx-trigger="change">
</select>
<div id="evidence-conditional-fields"></div>
```
Server returns file upload field for Document/CCTV types, or text description field for Physical Item type.

### 12.9 Generate Report Button
```html
<form hx-post="/api/v1/welfare/anti-ragging/investigations/{{ complaint_id }}/generate-report/"
      hx-target="#report-download-area"
      hx-swap="innerHTML"
      hx-indicator="#report-spinner"
      hx-disabled-elt="button[type='submit']">
  <button type="submit" class="btn-primary">
    Generate &amp; Download PDF
  </button>
</form>
```

### 12.10 KPI Auto-Refresh
```html
<div id="investigation-kpi-bar"
     hx-get="/api/v1/welfare/anti-ragging/investigations/kpi-summary/"
     hx-trigger="load, every 300s"
     hx-swap="innerHTML">
</div>
```

### 12.11 Hearing Mark-Complete Inline Action
```html
<button hx-patch="/api/v1/welfare/anti-ragging/investigations/{{ complaint_id }}/hearings/{{ hearing_id }}/"
        hx-vals='{"status": "completed"}'
        hx-target="#hearings-tab-content"
        hx-swap="innerHTML"
        hx-confirm="Mark this hearing as completed?"
        class="btn-sm btn-success">
  Mark Complete
</button>
```

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
