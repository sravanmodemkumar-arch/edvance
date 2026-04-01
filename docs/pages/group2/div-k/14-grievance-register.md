# 14 — Grievance Register

> **URL:** `/group/welfare/grievances/`
> **File:** `14-grievance-register.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Role:** Group Grievance Redressal Officer (Role 92, G3)

---

## 1. Purpose

Master register of all student and parent grievances that have been escalated from branch level to the group for resolution. A grievance reaches this register via one of four escalation triggers: (a) branch-level resolution not completed within the mandated 15-day window, (b) complainant is unsatisfied with the branch resolution and requests escalation, (c) the grievance involves a branch-level official who cannot self-investigate their own case, or (d) the issue spans multiple branches and requires group-level coordination.

The Group Grievance Redressal Officer is the accountable officer for all escalated grievances. Upon receipt, the officer logs the escalation, assigns it to the relevant group-level department or specialist officer (academic, hostel, transport, finance, HR, welfare), sets priority, tracks SLA compliance, ensures formal written acknowledgment to the complainant within 7 days, and issues a formal written resolution. The officer also maintains upward escalation rights: any grievance that cannot be resolved at group level within the SLA may be escalated to the Group COO.

Categories: Academic / Fees & Finance / Hostel & Accommodation / Transport / Staff Conduct / Infrastructure / Harassment / Exam & Results / Other.

Scale: 100–500 escalated grievances per academic year. At this volume, filtering, priority management, and SLA monitoring are the core daily activities.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Grievance Redressal Officer | G3, Role 92 | Full — create, view all, assign, resolve, escalate, export | Primary owner |
| Group COO | G3 | View all + can reassign; receives escalation notifications | Cannot create grievances directly |
| Group CEO | G4 | View — summary KPIs and high/urgent priority open cases | No edit capability |
| Department Heads (assigned to grievance) | G3 | View — own assigned grievances only; can add resolution notes | Cannot change category, priority, or assignment |
| Branch Principal | Branch-level | View — own branch grievances only | Read-only; cannot see group assignments |
| Group Legal & Compliance Officer | G3 | View all — for legal audit | No edit capability |
| All other roles | — | No access | Redirected to own dashboard |

> **Access enforcement:** Django decorator `@require_role(['grievance_redressal_officer'])` for all write and create actions. Department Head queryset filtered to `grievances.filter(assigned_to=request.user)`. Branch Principal queryset filtered to `grievances.filter(branch=request.user.branch)`.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Welfare & Safety  ›  Grievances  ›  Grievance Register
```

### 3.2 Page Header
```
Grievance Register                               [+ New Grievance]  [Export ↓]  [SLA Dashboard ↗]
Group Grievance Redressal Officer — [Officer Name]
AY [academic year]  ·  [N] Total  ·  [N] Open  ·  [N] Resolved This Month  ·  Avg Resolution: [N] days
```

`[+ New Grievance]` — opens `new-grievance` drawer for logging a newly escalated grievance.
`[Export ↓]` — exports filtered register to PDF/XLSX.
`[SLA Dashboard ↗]` — opens a dedicated SLA overview view (same page, different filter combination pre-applied) showing all active grievances ordered by SLA urgency.

### 3.3 Alert Banner (conditional)

| Condition | Banner Text | Severity |
|---|---|---|
| Urgent/High priority grievance unacknowledged > 24 h | "[N] Urgent or High-priority grievance(s) not acknowledged within 24 hours." | Red |
| SLA breached (any grievance) | "[N] grievance(s) have exceeded their resolution SLA. Immediate action required." | Red |
| COO escalation pending response | "[N] grievance(s) escalated to COO are awaiting response." | Amber |
| Acknowledgment SLA (7 days) approaching | "[N] grievance(s) must be formally acknowledged within 2 days." | Amber |
| > 10 Open High/Urgent priority | "There are currently [N] High or Urgent priority grievances open. Review workload." | Amber |
| All grievances within SLA | "All active grievances are within SLA. Current compliance: [N]%." | Green |

---

## 4. KPI Summary Bar

Six metric cards displayed horizontally (scroll on smaller screens).

| Card | Metric | Colour Rule |
|---|---|---|
| Total Open | Count of all non-resolved, non-closed grievances | Red if > 100; Amber if 50–100; Green if < 50 |
| High / Urgent Open | Count where `priority ∈ {High, Urgent}` and `status ≠ Resolved, Closed` | Red if > 5; Amber if 1–5; Green if 0 |
| SLA Breach % | (Breached / Total active) × 100 | Red if > 10%; Amber if 1–10%; Green if 0% |
| Resolved This Month | Count closed in current calendar month | Grey (trend indicator with sparkline) |
| Avg Resolution Days (This AY) | Average days from `escalated_date` to `resolved_date` | Green if ≤ 15; Amber if 16–30; Red if > 30 |
| Unassigned | Count with `assigned_to = null` | Red if > 0; Green if 0 |

```
┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│  Total Open  │ │  High/Urgent │ │  SLA Breach% │ │ Resolved/Mo  │ │  Avg Days    │ │  Unassigned  │
│     214      │ │      8       │ │    4.2%      │ │      37      │ │   19 days    │ │      3       │
│   ● Amber    │ │   ● Red      │ │   ● Amber    │ │   ● Grey     │ │   ● Amber    │ │   ● Red      │
└──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘
```

**Category Distribution Mini-Chart:** A horizontal stacked bar or small donut chart (Chart.js CDN) showing open grievances by category. Loads lazily via HTMX.

---

## 5. Sections

### 5.1 Filters and Search Bar

```
[🔍 Search by Grievance ID / Complainant Name / Branch]  [Branch ▾]  [Category ▾]  [Priority ▾]  [Status ▾]  [Assigned To ▾]  [SLA Status ▾]  [Date Range 📅]  [Reset Filters]
```

| Filter | Options |
|---|---|
| Branch | All Branches / individual branches |
| Category | All / Academic / Fees & Finance / Hostel & Accommodation / Transport / Staff Conduct / Infrastructure / Harassment / Exam & Results / Other |
| Priority | All / Low / Medium / High / Urgent |
| Status | All / Open / In Progress / Pending Complainant / Resolved / Closed |
| Assigned To | All / Unassigned / individual officer names |
| SLA Status | All / On Track / At Risk / Breached |
| Date Range | Custom date picker on `escalated_date` |

### 5.2 Grievance Table

Columns, sortable where marked (▲▼):

| Column | Source Field | Sortable | Notes |
|---|---|---|---|
| Grievance ID | `grievance_id` (auto) | ▲▼ | Format: `GRV-AY-NNNN` e.g. `GRV-2526-0214` |
| Branch | `branch.short_name` | ▲▼ | — |
| Category | `category` | ▲▼ | Badge-styled (see §5.3) |
| Complainant Type | `complainant_type` | — | Badge: Student (Blue) · Parent (Teal) · Both (Purple) |
| Escalated Date | `escalated_date` | ▲▼ | `DD MMM YYYY` |
| Assigned To | `assigned_to.name` | ▲▼ | Officer / department name; "Unassigned" in red if null |
| Priority | `priority` | ▲▼ | Pill: Low (Grey) · Medium (Blue) · High (Orange) · Urgent (Red) |
| Days Open | Computed | ▲▼ | Integer; count from `escalated_date` |
| Acknowledgment | `ack_status` | — | ✅ Within 7 days · ⏳ Pending · ❌ Overdue |
| Resolution Status | `status` | ▲▼ | Pill (see §5.4) |
| SLA | Computed | — | Pill: On Track (Green) · At Risk (Amber) · Breached (Red) |
| Actions | — | — | [View] · [Assign] · [Resolve] · [Escalate to COO] |

**Default sort:** Priority (Urgent first) then SLA Status (Breached first) then `days_open` descending.

**Pagination:** 25 rows per page. Controls: `« Previous  Page N of N  Next »`. Rows-per-page: 25 / 50 / 100.

### 5.3 Category Badge Colours

| Category | Badge Colour |
|---|---|
| Academic | Blue |
| Fees & Finance | Green |
| Hostel & Accommodation | Purple |
| Transport | Orange |
| Staff Conduct | Red |
| Infrastructure | Grey |
| Harassment | Dark Red |
| Exam & Results | Indigo |
| Other | Light Grey |

### 5.4 Status Colour Coding

| Status | Pill Colour |
|---|---|
| Open | Blue |
| In Progress | Yellow |
| Pending Complainant | Orange (awaiting complainant response) |
| Resolved | Green |
| Closed | Dark Green |

### 5.5 SLA Logic

SLA deadline is computed based on priority:
| Priority | Resolution SLA |
|---|---|
| Urgent | 7 calendar days from `escalated_date` |
| High | 15 calendar days |
| Medium | 21 calendar days |
| Low | 30 calendar days |

- **On Track:** Days open ≤ 70% of SLA period
- **At Risk:** Days open 70–100% of SLA period
- **Breached:** Days open > SLA period and status ≠ Resolved / Closed

---

## 6. Drawers / Modals

### 6.1 `grievance-detail` Drawer — 700 px, right-slide

**Trigger:** `[View]` button in table row.

**Header:**
```
Grievance [GRV-2526-0214]                                           [×]
[Branch]  ·  [Category badge]  ·  Priority: [pill]  ·  Status: [pill]
SLA: [N] days remaining / BREACHED  ·  Assigned: [Officer Name]
```

**Tab Bar:**
```
[Grievance]  [Assignment]  [Timeline]  [Communications]  [Resolution]  [Documents]
```

**Tab 1 — Grievance**

| Field | Value |
|---|---|
| Grievance ID | GRV-2526-0214 |
| Branch | [Branch Name] |
| Category | [Category] |
| Sub-category | [if applicable] |
| Complainant Type | Student / Parent / Both |
| Complainant Name | [Name] |
| Complainant Contact | [mobile / email] |
| Student Concerned | [Name, Admission No., Class] |
| Escalated Date | DD MMM YYYY |
| Original Branch Complaint Date | DD MMM YYYY |
| Escalation Reason | Branch SLA expired / Complainant unsatisfied / Official involved / Multi-branch |
| Description | [Full text of grievance — scrollable] |
| Priority | Low / Medium / High / Urgent |

**Tab 2 — Assignment**

| Field | Value |
|---|---|
| Assigned To | [Officer / Department] |
| Assigned By | [Role 92 officer] |
| Assigned Date | DD MMM YYYY |
| Expected Resolution Date | DD MMM YYYY |
| Assignment Notes | [notes] |

`[Reassign]` button — Role 92 only; triggers `assign-grievance` drawer pre-filled with current assignment.

**Tab 3 — Timeline**

Chronological, immutable audit stream:
```
[DD MMM YYYY · HH:MM]  [Action type badge]  [Description]  [Entered by]
```
Entries auto-created on: complaint creation, assignment, status change, acknowledgment sent, resolution recorded, escalation to COO.

Manual entry also possible for Role 92: `[+ Add Note to Timeline]` — opens inline textarea. Min 10 characters. Entry immutable once saved.

**Tab 4 — Communications**

Log of all formal communications with the complainant (acknowledgment letter, status update letters, resolution letter):

| Date | Communication Type | Channel | Sent By | Preview |
|---|---|---|---|---|
| DD MMM YYYY | Acknowledgment Letter | Email | [officer] | `[View ↗]` |
| DD MMM YYYY | Resolution Letter | Email + Post | [officer] | `[View ↗]` |

`[Send Communication]` button — opens a modal to compose and send an email/SMS to the complainant. Sends via portal messaging service. Communication is logged automatically.

**Tab 5 — Resolution**

| Field | Value |
|---|---|
| Resolution Summary | [full resolution text] |
| Resolved By | [Officer Name, Role] |
| Resolved Date | DD MMM YYYY |
| Compensation / Remedy | [if any] |
| Complainant Satisfaction | Satisfied / Partially Satisfied / Unsatisfied / Not Recorded |
| Lessons Learned | [notes for institutional improvement] |
| Closure Date | DD MMM YYYY |

`[Record Resolution]` — opens `resolve-grievance` drawer. Available only if status is "In Progress" and Role 92.

**Tab 6 — Documents**

Document list with columns: Document Name, Type (Initial Complaint / Branch Investigation / Evidence / Resolution Letter / Other), Uploaded By, Date, `[Download ↓]`.

`[Upload Document]` — file-upload mini-form. PDF/DOCX/JPG; max 20 MB. Role 92 and assigned department head.

---

### 6.2 `new-grievance` Drawer — 640 px, right-slide

**Trigger:** `[+ New Grievance]` header button.

**Header:**
```
Log New Escalated Grievance
```

**Fields:**

| Field | Type | Required | Validation |
|---|---|---|---|
| Branch | Select | Yes | Dropdown of all branches |
| Escalated Date | Date picker | Yes | Cannot be future date |
| Original Branch Complaint Date | Date picker | Yes | Must be before `escalated_date` |
| Escalation Reason | Select | Yes | Branch SLA Expired · Complainant Unsatisfied · Official Involved · Multi-Branch Issue · Other |
| Category | Select | Yes | All 9 categories |
| Sub-category | Text | No | Optional free text |
| Complainant Type | Radio | Yes | Student · Parent · Both |
| Complainant Name | Text | Yes | Full name |
| Complainant Mobile | Phone | Yes | +91 format; 10-digit validation |
| Complainant Email | Email | No | Validated format |
| Student Name | Text | Conditional | Required if Complainant Type ∈ {Student, Both} |
| Student Admission No. | Text | Conditional | Required if student name provided |
| Class / Section | Text | Conditional | Required if student provided |
| Description | Textarea | Yes | Min 100 characters |
| Priority | Select | Yes | Low · Medium · High · Urgent |
| Supporting Documents | File upload (multi) | No | PDF/DOCX/JPG; max 20 MB; up to 5 files |

**Validation:**
- `Original Branch Complaint Date` must be before `Escalated Date`.
- `Description` minimum 100 characters.
- On save: Grievance ID auto-generated; status set to "Open"; 7-day acknowledgment SLA timer starts; unassigned flag set.

**Footer:** `[Cancel]`  `[Save & Register Grievance ▶]`

---

### 6.3 `assign-grievance` Drawer — 440 px, right-slide

**Trigger:** `[Assign]` table action or `[Reassign]` in Assignment tab. Role 92 only.

**Header:**
```
Assign Grievance — [GRV-2526-0214]
```

**Fields:**

| Field | Type | Required | Validation |
|---|---|---|---|
| Assign To | Search-select | Yes | Searches group-level officers and department heads |
| Department | Select | Yes | Academic · Finance · Hostel · Transport · HR · Welfare · Legal · Other |
| Priority | Select | Yes | May be changed at assignment time; Low · Medium · High · Urgent |
| Expected Resolution Date | Date picker | Yes | System suggests date based on priority SLA; officer may adjust |
| Assignment Notes | Textarea | No | Internal notes for assignee |
| Notify Assignee | Checkbox | Yes (default checked) | Email + portal notification sent on save |

**Footer:** `[Cancel]`  `[Assign Grievance]`

On save: status updated to "In Progress"; Timeline entry auto-created; assignee notified.

---

### 6.4 `resolve-grievance` Drawer — 520 px, right-slide

**Trigger:** `[Resolve]` table action or `[Record Resolution]` in Resolution tab. Role 92 and assigned department head.

**Header:**
```
Record Resolution — [GRV-2526-0214]
[Category]  ·  [Branch]  ·  Days Open: [N]
```

**Fields:**

| Field | Type | Required | Validation |
|---|---|---|---|
| Resolution Summary | Textarea | Yes | Min 100 characters; formal resolution text as it will appear in the resolution letter |
| Resolved By | Text | Yes | Auto-filled with current user; editable if resolution officer differs |
| Resolved Date | Date picker | Yes | Defaults to today; cannot be future |
| Compensation / Remedy | Textarea | No | e.g. fee refund, re-examination, room change |
| Compensation Amount (if financial) | Number | Conditional | In INR; required if remedy involves financial compensation |
| Complainant Satisfaction | Select | No | Satisfied · Partially Satisfied · Unsatisfied · Not Recorded |
| Lessons Learned | Textarea | No | Institutional improvement note; shared with relevant department head |
| Close Case After Resolution | Toggle | Yes | Default: On — sets status to "Resolved" and auto-schedules "Closed" after 15-day appeal window |
| Send Resolution Letter | Toggle | Yes | Default: On — auto-generates and sends formal resolution letter to complainant |
| Supporting Documents | File upload | No | Resolution order, supporting evidence |

**Footer:** `[Cancel]`  `[Record Resolution & Notify Complainant]`

On save: status updated to "Resolved"; resolution letter generated and sent (if toggle on); Timeline entry created; if SLA was breached, breach is flagged in resolution record.

---

### 6.5 `escalate-to-coo` Modal — 400 px, centred modal

**Trigger:** `[Escalate to COO]` table action. Role 92 only. Available only for High/Urgent priority grievances that are at-risk or breached.

**Header:**
```
⚠ Escalate to Group COO
This action notifies the COO and transfers accountability.
```

**Fields:**

| Field | Type | Required | Validation |
|---|---|---|---|
| Grievance ID | Text | — | Pre-filled; read-only |
| Escalation Reason | Textarea | Yes | Min 50 characters |
| Urgency Level | Select | Yes | Cannot Resolve Without COO Direction · SLA Critical · Complaint Involves Senior Official · Legal Threat |
| Recommended Action | Textarea | No | Officer's recommendation to COO |

Auto-notification: On save, email + portal notification auto-sent to Group COO with grievance summary, days open, SLA status, and escalation reason. Notification cannot be cancelled.

**Footer:** `[Cancel]`  `[Confirm Escalation — Notify COO]`

---

## 7. Toast Messages

| Action | Toast Text | Type |
|---|---|---|
| Grievance registered | "Grievance [GRV-ID] registered. 7-day acknowledgment SLA has started." | Success |
| Grievance assigned | "Grievance [GRV-ID] assigned to [Officer/Department]. Assignee notified." | Success |
| Resolution recorded | "Resolution recorded for [GRV-ID]. Resolution letter sent to complainant." | Success |
| Grievance closed | "Grievance [GRV-ID] closed. Case archived." | Success |
| Escalated to COO | "Grievance [GRV-ID] escalated to COO. Notification sent." | Info |
| Timeline note added | "Note added to timeline for [GRV-ID]." | Success |
| Communication sent | "Communication sent to [Complainant Name] via [channel]." | Success |
| Document uploaded | "Document '[name]' uploaded to [GRV-ID]." | Success |
| Export complete | "Grievance register exported to [format]." | Success |
| Validation — description too short | "Description must be at least 100 characters." | Error |
| Unassigned warning on save | "Grievance saved as unassigned. Assign to an officer to begin tracking." | Warning |
| SLA breach auto-flagged | "SLA breached for Grievance [GRV-ID]. Escalation recommended." | Warning |
| Unauthorised action | "Access denied. This action requires Grievance Redressal Officer privileges." | Error |

---

## 8. Empty States

| Context | Illustration | Heading | Sub-text | Action |
|---|---|---|---|---|
| No grievances in register | Inbox icon | "No Grievances Registered" | "No escalated grievances have been logged for this academic year." | `[+ New Grievance]` |
| No results match filters | Funnel icon | "No Grievances Match Filters" | "Try adjusting your filters or resetting them." | `[Reset Filters]` |
| Documents tab — no documents | Folder icon | "No Documents Attached" | "Upload supporting documents, branch investigation reports, or the resolution order." | `[Upload Document]` |
| Communications tab — no communications | Chat icon | "No Communications Logged" | "Formal communications with the complainant will appear here." | `[Send Communication]` |
| Resolution tab — not resolved | Hourglass icon | "Resolution Not Yet Recorded" | "Record the resolution once the grievance has been addressed and verified." | `[Record Resolution]` (Role 92 / Dept Head) |
| Category chart — no data | Chart icon | "No Category Data" | "Category distribution will appear once grievances are logged." | None |

---

## 9. Loader States

| Context | Loader Behaviour |
|---|---|
| Initial page load | KPI bar: 6 shimmer cards. Category mini-chart: grey shimmer. Table: 10 shimmer rows |
| Filter / search | Table content replaced by spinner (20 px, indigo) while HTMX fetches; debounce 400 ms on search input |
| Grievance detail drawer opening | Drawer slides in; content area shows spinner |
| Tab switching in detail drawer | Tab body shows spinner while HTMX fetches tab-specific data |
| `[Save & Register Grievance]` | Button disabled, text: "Saving…", spinner |
| `[Assign Grievance]` | Button disabled, text: "Assigning…" |
| `[Record Resolution & Notify]` | Button disabled, text: "Recording…"; notification sending shown as secondary progress indicator |
| `[Confirm Escalation — Notify COO]` | Button disabled, text: "Escalating…"; toast appears when COO notification confirmed sent |
| Export | Button disabled, spinner; text: "Generating…" |

---

## 10. Role-Based UI Visibility

| UI Element | Role 92 (GRO) | Group COO | Group CEO | Dept Head (assigned) | Branch Principal | Legal Compliance | All Others |
|---|---|---|---|---|---|---|---|
| KPI Summary Bar | Full | Full | Partial (Total Open + High/Urgent) | Own assigned count | Own branch counts | Full | Hidden |
| Category mini-chart | Visible | Visible | Hidden | Hidden | Hidden | Visible | Hidden |
| Grievance table — all branches | Visible | Visible | Hidden | Own assigned | Own branch | Visible | Hidden |
| `[View]` action | Visible | Visible | Hidden | Visible (own) | Visible (own branch) | Visible | Hidden |
| `[Assign]` action | Visible | Visible (reassign) | Hidden | Hidden | Hidden | Hidden | Hidden |
| `[Resolve]` action | Visible | Hidden | Hidden | Visible (own) | Hidden | Hidden | Hidden |
| `[Escalate to COO]` action | Visible | Hidden | Hidden | Hidden | Hidden | Hidden | Hidden |
| `[+ New Grievance]` button | Visible | Hidden | Hidden | Hidden | Hidden | Hidden | Hidden |
| `[Export ↓]` button | Visible | Visible | Hidden | Hidden | Hidden | Visible | Hidden |
| `[SLA Dashboard ↗]` link | Visible | Visible | Hidden | Hidden | Hidden | Hidden | Hidden |
| Assignment tab `[Reassign]` | Visible | Visible | Hidden | Hidden | Hidden | Hidden | Hidden |
| Resolution tab `[Record Resolution]` | Visible | Hidden | Hidden | Visible (own) | Hidden | Hidden | Hidden |
| Communications tab `[Send Communication]` | Visible | Hidden | Hidden | Hidden | Hidden | Hidden | Hidden |
| `escalate-to-coo` modal | Visible | Hidden | Hidden | Hidden | Hidden | Hidden | Hidden |
| Alert banner | Full detail | Full detail | Partial | Own assigned cases | Own branch cases | Full detail | Hidden |
| Complainant contact details | Visible | Visible | Hidden | Visible | Visible (own branch) | Visible | Hidden |

---

## 11. API Endpoints

### 11.1 List & Filter Grievances
```
GET /api/v1/welfare/grievances/
```

| Query Parameter | Type | Description |
|---|---|---|
| `branch_id` | integer | Filter by branch |
| `category` | string | `academic` · `fees_finance` · `hostel` · `transport` · `staff_conduct` · `infrastructure` · `harassment` · `exam_results` · `other` |
| `priority` | string | `low` · `medium` · `high` · `urgent` |
| `status` | string | `open` · `in_progress` · `pending_complainant` · `resolved` · `closed` |
| `assigned_to_id` | integer | Filter by assigned officer user ID; use `unassigned` for null |
| `sla_status` | string | `on_track` · `at_risk` · `breached` |
| `date_from` | date (YYYY-MM-DD) | Filter `escalated_date` from |
| `date_to` | date (YYYY-MM-DD) | Filter `escalated_date` to |
| `search` | string | Searches `grievance_id`, `complainant_name`, `branch.short_name` |
| `page` | integer | Default: 1 |
| `page_size` | integer | 25 · 50 · 100 (default: 25) |
| `ordering` | string | `priority` · `sla_status` · `days_open` · `-days_open` · `escalated_date` · `-escalated_date` |

### 11.2 Retrieve Grievance Detail
```
GET /api/v1/welfare/grievances/{grievance_id}/
```
Returns full grievance object with all tabs' data embedded.

### 11.3 Get Timeline
```
GET /api/v1/welfare/grievances/{grievance_id}/timeline/
```

### 11.4 Get Communications Log
```
GET /api/v1/welfare/grievances/{grievance_id}/communications/
```

### 11.5 Create Grievance
```
POST /api/v1/welfare/grievances/
```
Body: `branch_id`, `escalated_date`, `original_complaint_date`, `escalation_reason`, `category`, `sub_category`, `complainant_type`, `complainant_name`, `complainant_mobile`, `complainant_email`, `student_name`, `student_admission_no`, `class_section`, `description`, `priority`, `documents[]` (files).
Response: 201 Created — returns `grievance_id`, `ack_sla_deadline`.

### 11.6 Assign Grievance
```
PATCH /api/v1/welfare/grievances/{grievance_id}/assign/
```
Body: `assigned_to_id`, `department`, `priority`, `expected_resolution_date`, `assignment_notes`, `notify_assignee` (bool).

### 11.7 Add Timeline Note
```
POST /api/v1/welfare/grievances/{grievance_id}/timeline/
```
Body: `note` (min 10 characters). Returns 201 Created; immutable.

### 11.8 Send Communication to Complainant
```
POST /api/v1/welfare/grievances/{grievance_id}/communications/
```
Body: `communication_type`, `channel` (`email` · `sms` · `both`), `subject`, `body`, `attachments[]` (files).

### 11.9 Record Resolution
```
POST /api/v1/welfare/grievances/{grievance_id}/resolution/
```
Body: `resolution_summary`, `resolved_by`, `resolved_date`, `remedy`, `compensation_amount` (optional), `complainant_satisfaction`, `lessons_learned`, `close_after_resolution` (bool), `send_resolution_letter` (bool), `documents[]` (files).

### 11.10 Escalate to COO
```
POST /api/v1/welfare/grievances/{grievance_id}/escalate-coo/
```
Body: `escalation_reason`, `urgency_level`, `recommended_action` (optional).
Response: 200 OK — COO notification sent; `coo_notified_at` timestamp returned.

### 11.11 Upload Document
```
POST /api/v1/welfare/grievances/{grievance_id}/documents/
```
Body: `multipart/form-data` — `file`, `document_type`, `description`.

### 11.12 KPI Summary
```
GET /api/v1/welfare/grievances/kpi-summary/
```
Query: `academic_year` (optional), `branch_id` (optional for scoped roles).
Response: `{ total_open, high_urgent_open, sla_breach_pct, resolved_this_month, avg_resolution_days, unassigned_count }`.

### 11.13 Category Distribution
```
GET /api/v1/welfare/grievances/category-distribution/
```
Query: `status` (optional filter on open grievances).
Response: Array of `{ category, count }`.

### 11.14 Export
```
GET /api/v1/welfare/grievances/export/
```
Query: all filter params from §11.1 + `format` (`xlsx` · `pdf`).

---

## 12. HTMX Patterns

### 12.1 Table Initialisation
```html
<div id="grievance-table"
     hx-get="/api/v1/welfare/grievances/?page=1&page_size=25&ordering=priority"
     hx-trigger="load"
     hx-swap="innerHTML"
     hx-indicator="#table-spinner">
</div>
```

### 12.2 Multi-Filter Application
```html
<select name="priority"
        id="filter-priority"
        hx-get="/api/v1/welfare/grievances/"
        hx-trigger="change"
        hx-target="#grievance-table"
        hx-swap="innerHTML"
        hx-include="#filter-branch, #filter-category, #filter-status, #filter-assigned, #filter-sla, #filter-date-from, #filter-date-to, #search-input">
</select>
```

### 12.3 Debounced Search
```html
<input id="search-input"
       name="search"
       hx-get="/api/v1/welfare/grievances/"
       hx-trigger="input changed delay:400ms, search"
       hx-target="#grievance-table"
       hx-swap="innerHTML"
       hx-include="#filter-branch, #filter-category, #filter-priority, #filter-status, #filter-assigned, #filter-sla"
       placeholder="Search Grievance ID, complainant or branch…">
```

### 12.4 Grievance Detail Drawer
```html
<button hx-get="/htmx/welfare/grievances/{{ grievance_id }}/detail/"
        hx-target="#drawer-container"
        hx-swap="innerHTML"
        hx-trigger="click"
        class="text-indigo-600 hover:underline text-sm font-medium">
  View
</button>
```

### 12.5 Drawer Tab Switching
```html
<button hx-get="/htmx/welfare/grievances/{{ grievance_id }}/tab/timeline/"
        hx-target="#drawer-tab-content"
        hx-swap="innerHTML"
        hx-trigger="click"
        class="drawer-tab-btn">
  Timeline
</button>
```

### 12.6 New Grievance Form
```html
<form hx-post="/api/v1/welfare/grievances/"
      hx-encoding="multipart/form-data"
      hx-target="#grievance-table"
      hx-swap="innerHTML"
      hx-on::after-request="closeDrawer(); showToast(event); refreshKPI();">
  <button type="submit"
          hx-disabled-elt="this"
          class="btn-primary">
    Save &amp; Register Grievance ▶
  </button>
</form>
```

### 12.7 Assign Grievance Form
```html
<form hx-patch="/api/v1/welfare/grievances/{{ grievance_id }}/assign/"
      hx-target="#drawer-tab-content"
      hx-swap="innerHTML"
      hx-on::after-request="refreshTableRow('{{ grievance_id }}'); showToast(event);">
</form>
```

### 12.8 Resolve Grievance Form
```html
<form hx-post="/api/v1/welfare/grievances/{{ grievance_id }}/resolution/"
      hx-encoding="multipart/form-data"
      hx-target="#drawer-tab-content"
      hx-swap="innerHTML"
      hx-on::after-request="refreshTableRow('{{ grievance_id }}'); showToast(event); refreshKPI();">
</form>
```

### 12.9 Escalate to COO Modal
```html
<div id="escalate-coo-modal"
     class="hidden fixed inset-0 bg-black/40 flex items-center justify-center z-50"
     hx-on:htmx:after-request="this.classList.add('hidden')">
  <div class="bg-white rounded-xl shadow-xl p-6 w-[400px]">
    <form hx-post="/api/v1/welfare/grievances/{{ grievance_id }}/escalate-coo/"
          hx-target="body"
          hx-swap="none"
          hx-on::after-request="closeModal('escalate-coo-modal'); showToast(event);">
    </form>
  </div>
</div>
```

### 12.10 KPI Auto-Refresh
```html
<div id="grievance-kpi-bar"
     hx-get="/api/v1/welfare/grievances/kpi-summary/"
     hx-trigger="load, every 300s"
     hx-swap="innerHTML">
</div>
```

### 12.11 Category Distribution Chart Load
```html
<div id="category-chart-data"
     hx-get="/api/v1/welfare/grievances/category-distribution/?status=open"
     hx-trigger="load"
     hx-swap="innerHTML"
     hx-on::after-settle="renderCategoryChart(this);">
</div>
```

### 12.12 Complainant Type Conditional Fields
```html
<div>
  <label><input type="radio" name="complainant_type" value="student"
                hx-get="/htmx/welfare/grievances/complainant-fields/?type=student"
                hx-target="#complainant-conditional-fields"
                hx-swap="innerHTML"
                hx-trigger="change"> Student</label>
  <label><input type="radio" name="complainant_type" value="parent"
                hx-get="/htmx/welfare/grievances/complainant-fields/?type=parent"
                hx-target="#complainant-conditional-fields"
                hx-swap="innerHTML"
                hx-trigger="change"> Parent</label>
  <label><input type="radio" name="complainant_type" value="both"
                hx-get="/htmx/welfare/grievances/complainant-fields/?type=both"
                hx-target="#complainant-conditional-fields"
                hx-swap="innerHTML"
                hx-trigger="change"> Both</label>
</div>
<div id="complainant-conditional-fields"></div>
```

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
