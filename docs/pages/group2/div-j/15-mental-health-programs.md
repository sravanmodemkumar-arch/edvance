# 15 — Mental Health Programs

> **URL:** `/group/health/mh-programs/`
> **File:** `15-mental-health-programs.md`
> **Template:** `portal_base.html`
> **Priority:** P1
> **Role:** Group Mental Health Coordinator (primary) · Group Medical Coordinator (view)

---

## 1. Purpose

Create, schedule, and track mental health awareness programs, workshops, campaigns, and group wellbeing activities across all branches in the group. This page manages the proactive, population-level dimension of the mental health programme — distinct from individual counselling (which is managed in the Session Register and Wellbeing Tracker).

Program types covered: exam stress management workshops, peer support circles, teacher mental health awareness training, parent orientation on adolescent wellbeing, anti-bullying campaigns, suicide prevention awareness sessions, resilience-building activities, and digital wellbeing sessions.

The Mental Health Coordinator uses this page to plan the group's annual mental health calendar, assign programs to branches, track attendance and completion, collect feedback from participants, and measure whether programs are translating into better wellbeing outcomes (e.g., reduction in high-risk cases post-program at a branch). Branch Principals confirm attendance data for their branch.

Scale: 3–10 programs per branch per academic year × 20–50 branches = 60–500 program events per year at group level.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Mental Health Coordinator | G3 | Full CRUD — create, edit, assign, mark complete, cancel, view all results | Primary owner |
| Group Medical Coordinator | G3 | View only — program list and results | No create or edit |
| Academic Director | Group | View only | For academic calendar coordination |
| Branch Principal | Branch | Own branch programs — view schedule + confirm attendance count | Cannot create; attendance update only |
| All other roles | — | — | No access |

> **Access enforcement:** `@require_role('mental_health_coordinator', 'medical_coordinator', 'academic_director', 'branch_principal')` with branch-scoped queryset for Branch Principal.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Health & Medical  ›  Mental Health Programs
```

### 3.2 Page Header
- **Title:** `Mental Health Programs`
- **Subtitle:** `[N] Programs This AY · [N] Completed · [N] Scheduled · [N] Draft`
- **Right controls:** `+ Create Program` (Mental Health Coordinator only) · `Advanced Filters` · `Export`

### 3.3 Alert Banner

| Condition | Banner Text | Severity |
|---|---|---|
| Branch with no program this term | "[N] branches have no mental health program planned for the current term." | Amber |
| Program planned but no facilitator assigned | "[N] programs have no facilitator assigned. Assign a facilitator before the scheduled date." | Amber |
| Low participation reported (< 30% of target) | "[N] programs reported participation below 30% of the target audience." | Amber |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule |
|---|---|---|
| Programs This AY | All programs in current academic year (all statuses) | Blue always |
| Programs This Month | Programs with scheduled date in current calendar month | Blue always |
| Branches with Program This Month | Branches where at least one program is Scheduled or Completed in current month | Green = 100% · Yellow < 80% · Red < 60% |
| Student Participants (Cumulative This AY) | Sum of actual participant counts across all completed student-facing programs this AY | Blue always |
| Teacher Programs Completed | Count of completed programs with target audience = Teachers or All | Blue always |
| Programs Pending Launch | Programs in Scheduled status with date ≤ 7 days from today | Yellow if > 0 · Red if facilitator not assigned |

---

## 5. Main Table — Program Master Table

**Search:** Program name. 300ms debounce.

**Advanced Filters:**

| Filter | Type | Options |
|---|---|---|
| Program Type | Checkbox | Workshop / Campaign / Group Session / Teacher Training / Parent Orientation / Awareness |
| Target Audience | Checkbox | Students / Teachers / Parents / All |
| Status | Checkbox | Draft / Scheduled / Completed / Cancelled |
| Branch | Multi-select | All branches |
| Date Range | Date picker | From – To |

**Columns:**

| Column | Sortable | Notes |
|---|---|---|
| Program Name | ✅ | Link → `program-detail` drawer |
| Type | ✅ | Colour badge: Workshop (blue) / Campaign (teal) / Group Session (green) / Teacher Training (purple) / Parent Orientation (orange) / Awareness (grey) |
| Target Audience | ✅ | Students / Teachers / Parents / All badge |
| Branch(es) | ✅ | Count with tooltip listing branch names |
| Facilitator | ✅ | Name; amber badge "Not Assigned" if missing |
| Scheduled Date | ✅ | Date; red if past date and not Completed |
| Participants Expected | ✅ | Target count |
| Participants Actual | ✅ | Actual count (populated after completion) |
| Status | ✅ | Draft (grey) / Scheduled (blue) / Completed (green) / Cancelled (red) badge |
| Actions | ❌ | View · Edit · Mark Complete · Cancel |

**Default sort:** Scheduled Date ascending for Scheduled/Draft; Completed date descending for Completed.
**Pagination:** Server-side · 25/page.
**Bulk actions:** Export selected (Mental Health Coordinator only).

---

## 6. Drawers / Modals

### 6.1 Drawer — `program-detail` (700px, right side)

Triggered by program name link or **View** action.

**Tabs:**

#### Tab 1 — Details
| Field | Notes |
|---|---|
| Program Name | |
| Type | Badge |
| Objectives | Numbered list — what the program aims to achieve |
| Description | Full program description and content outline |
| Target Audience | Students / Teachers / Parents / All |
| Target Classes / Groups | e.g., "Class 9–12" or "All teachers" |
| Facilitator(s) | Name(s) — internal counsellor or external speaker |
| Facilitator Type | Internal (branch counsellor) / External (speaker / NGO / expert) |
| Duration | Planned duration in minutes / hours |
| Materials / Resources | Uploaded PDFs — viewable/downloadable |
| Registration Required | Yes / No |
| Feedback Form | Generated QR code + link for participant feedback |

#### Tab 2 — Schedule
Per-branch schedule table.

| Column | Notes |
|---|---|
| Branch | |
| Date | Scheduled date |
| Time | Start – End |
| Venue | Room / hall name at branch |
| Facilitator | May differ per branch |
| Reminder Sent | Yes / No; Send Reminder button if No and date is within 7 days |
| Status | Planned / Completed / Cancelled |

#### Tab 3 — Participants
| Metric | Notes |
|---|---|
| Total Expected | Sum across all branches |
| Total Actual | Sum of confirmed attendances |
| Participation Rate % | Actual / Expected × 100 |
| Attendance Sheet | Uploaded file link per branch |
| Feedback Completion Rate | (Feedback forms completed / Actual participants) × 100 |

Per-branch attendance table:

| Branch | Expected | Actual | Rate | Attendance Sheet | Feedback Completion |
|---|---|---|---|---|---|

#### Tab 4 — Feedback
Aggregate feedback from participant responses to the standard feedback form.

**Standard feedback questions (1–5 scale):**

| Question | Avg Score | Response Count |
|---|---|---|
| How relevant was this program to your needs? | | |
| How would you rate the quality of the content? | | |
| How would you rate the facilitator? | | |
| Would you recommend this program to others? | | |

Overall NPS-style score (% who rated ≥ 4 on "would recommend").

**Comment highlights:** top 3 positive comments and top 3 constructive suggestions (selected by coordinator).

#### Tab 5 — Outcomes
Post-program follow-up data.

| Metric | Notes |
|---|---|
| New Counselling Cases Opened Post-Program | Count of wellbeing cases opened within 30 days, at branches where this program ran |
| Teacher Referrals Generated | Teachers who referred students to counselling after attending teacher training |
| Parent Follow-up Contacts | Parents who contacted school after parent orientation |
| Notable Outcomes | Free text — coordinator notes on observed impact |
| Follow-up Action Items | Repeating list: Action · Assigned To · Due Date · Status |

---

### 6.2 Drawer — `program-create` (660px, right side)

Triggered by **+ Create Program** (Mental Health Coordinator only).

| Field | Type | Validation |
|---|---|---|
| Program Name | Text input (max 150 chars) | Required |
| Type | Single-select: Workshop / Campaign / Group Session / Teacher Training / Parent Orientation / Awareness | Required |
| Objectives | Textarea (max 1,000 chars) | Required |
| Description | Textarea (max 2,000 chars) | Optional |
| Target Audience | Multi-select: Students / Teachers / Parents | Required; at least one |
| Target Classes / Groups | Multi-select (conditional if Students selected) | Required if Students |
| Assign Branches | Multi-select (with Select All option) | Required |
| Facilitator Type | Radio — Internal / External | Required |
| Facilitator Name | Text input or single-select from counsellor registry (if internal) | Required |
| Facilitator Contact | Email + phone (if external) | Required if External |
| Scheduled Date | Date picker | Required |
| Start Time | Time picker | Required |
| Duration (mins) | Number input | Required |
| Venue (per branch) | Text input per assigned branch | Optional |
| Expected Participants | Number input | Required |
| Registration Required | Toggle — Yes / No | Required |
| Materials Upload | File upload (PDF, max 10 MB, multiple allowed) | Optional |
| Feedback Form | Auto-generated on create; toggle to enable/disable | Default enabled |
| Notes | Textarea (max 500 chars) | Optional |

**Footer:** `Cancel` · `Save as Draft` · `Schedule Program`

---

### 6.3 Drawer — `program-edit` (660px, right side)

Pre-populated with existing data. Same layout as create. Status = Completed or Cancelled: all fields read-only.

---

### 6.4 Drawer — `attendance-update` (540px, right side)

Triggered by **Update Attendance** in the Schedule tab or from Branch Principal's view.

| Field | Type | Validation |
|---|---|---|
| Branch | Read-only | |
| Program Name | Read-only | |
| Scheduled Date | Read-only | |
| Actual Date Conducted | Date picker | Required |
| Expected Participants | Read-only | |
| Actual Participants | Number input | Required |
| Facilitator Present | Toggle — Yes / No | Required |
| Upload Attendance Sheet | File upload (PDF/JPG/XLS, max 10 MB) | Optional |
| Program Completed as Planned | Toggle — Yes / No | Required |
| Notes / Deviations | Textarea (max 300 chars) | Required if not completed as planned |

**Footer:** `Cancel` · `Save Attendance`

---

### 6.5 Modal — `cancel-program` (420px, centred)

Triggered by **Cancel** action.

| Field | Type | Validation |
|---|---|---|
| Program Name | Read-only | |
| Reason for Cancellation | Textarea (max 300 chars) | Required |
| Reschedule? | Radio — Yes / No | Required |
| New Scheduled Date | Date picker | Required if Reschedule = Yes |
| Notify Registered Participants | Toggle — Yes / No | Required |

**Footer:** `Cancel` · `Confirm Cancellation`

---

## 7. Toast Messages

| Action | Toast Text | Type |
|---|---|---|
| Program created | "Program created and scheduled successfully." | Success |
| Draft saved | "Program saved as draft." | Info |
| Program updated | "Program details updated." | Success |
| Attendance submitted | "Attendance updated for [Branch] — [N] participants recorded." | Success |
| Program marked complete | "Program marked as complete." | Success |
| Program cancelled | "Program cancelled. [Notify message if participants notified]" | Info |
| Reminder sent | "Reminder sent to facilitator and branch principal for [Branch]." | Success |
| Feedback form link copied | "Feedback form link copied to clipboard." | Info |
| Export triggered | "Export is being prepared. Download will start shortly." | Info |
| Save failed | "Please complete all required fields before saving." | Error |

---

## 8. Empty States

| Context | Heading | Sub-text | Action |
|---|---|---|---|
| No programs this AY | "No mental health programs for this academic year." | "Create the first program to get started." | `+ Create Program` button |
| No results for filters | "No programs match your current filters." | "Try adjusting your filters." | `Clear Filters` |
| Schedule tab — no branches assigned | "No branch schedule configured." | "Assign branches to this program to set up the schedule." | — |
| Feedback tab — no responses yet | "No feedback collected yet." | "Share the feedback QR code or link with participants after the program." | — |
| Outcomes tab — no data yet | "No outcome data recorded." | "Outcome data will populate here 30 days after program completion." | — |

---

## 9. Loader States

| Context | Loader Behaviour |
|---|---|
| Initial page load | Full-page skeleton: KPI bar (6 grey cards) + program table (8 grey rows × 9 columns) |
| Filter apply | Table body spinner; KPI bar updates after |
| Program detail drawer open | Drawer skeleton: tab headers + content block skeleton |
| Feedback tab load | Metrics skeleton (4 grey score blocks) + comment skeleton |
| Outcomes tab load | Metrics skeleton (4 grey blocks) + action list skeleton |
| Attendance update save | Submit button spinner; inputs disabled |
| Send reminder | Button spinner + "Sending…" |

---

## 10. Role-Based UI Visibility

| UI Element | Mental Health Coordinator | Medical Coordinator | Academic Director | Branch Principal |
|---|---|---|---|---|
| Full program list | ✅ | ✅ (view only) | ✅ (view only) | Own branch programs only |
| + Create Program button | ✅ | ❌ | ❌ | ❌ |
| Edit action | ✅ | ❌ | ❌ | ❌ |
| Mark Complete action | ✅ | ❌ | ❌ | ❌ |
| Cancel action | ✅ | ❌ | ❌ | ❌ |
| Attendance Update | ✅ | ❌ | ❌ | ✅ (own branch) |
| Facilitator field | ✅ | ✅ | ✅ | ✅ |
| Feedback tab | ✅ | ✅ | ✅ | Own branch only |
| Outcomes tab | ✅ | ✅ | ❌ | ❌ |
| Materials upload | ✅ | ❌ | ❌ | ❌ |
| Send Reminder | ✅ | ❌ | ❌ | ❌ |
| Export button | ✅ | ❌ | ❌ | ❌ |
| KPI bar | ✅ Full | ✅ Full (view) | ✅ Full (view) | Own branch only |
| Alert banners | ✅ | ❌ | ❌ | Own branch only |

---

## 11. API Endpoints

### Base URL: `/api/v1/group/{group_id}/health/mh-programs/`

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/health/mh-programs/` | List all programs (paginated, filtered) | JWT + role check |
| POST | `/api/v1/group/{group_id}/health/mh-programs/` | Create new program | Mental Health Coordinator |
| GET | `/api/v1/group/{group_id}/health/mh-programs/{program_id}/` | Retrieve program detail | JWT + role check |
| PATCH | `/api/v1/group/{group_id}/health/mh-programs/{program_id}/` | Update program | Mental Health Coordinator |
| DELETE | `/api/v1/group/{group_id}/health/mh-programs/{program_id}/` | Cancel program (soft delete) | Mental Health Coordinator |
| GET | `/api/v1/group/{group_id}/health/mh-programs/kpi/` | KPI summary bar data | JWT + role check |
| GET | `/api/v1/group/{group_id}/health/mh-programs/{program_id}/schedule/` | Branch schedule table | JWT + role check |
| PATCH | `/api/v1/group/{group_id}/health/mh-programs/{program_id}/schedule/{branch_id}/` | Update attendance for a branch | Mental Health Coordinator / Branch Principal |
| POST | `/api/v1/group/{group_id}/health/mh-programs/{program_id}/schedule/{branch_id}/upload/` | Upload attendance sheet | Mental Health Coordinator / Branch Principal |
| POST | `/api/v1/group/{group_id}/health/mh-programs/{program_id}/complete/` | Mark program as complete | Mental Health Coordinator |
| POST | `/api/v1/group/{group_id}/health/mh-programs/{program_id}/remind/{branch_id}/` | Send reminder to facilitator and principal | Mental Health Coordinator |
| GET | `/api/v1/group/{group_id}/health/mh-programs/{program_id}/feedback/` | Aggregate feedback results | JWT + role check |
| GET | `/api/v1/group/{group_id}/health/mh-programs/{program_id}/outcomes/` | Outcome data for this program | JWT + role check |
| POST | `/api/v1/group/{group_id}/health/mh-programs/{program_id}/materials/` | Upload program materials | Mental Health Coordinator |
| GET | `/api/v1/group/{group_id}/health/mh-programs/export/` | Export programs CSV | Mental Health Coordinator |
| GET | `/api/v1/group/{group_id}/health/mh-programs/alerts/` | Fetch active alert conditions | JWT + role check |
| GET | `/api/v1/group/{group_id}/health/mh-programs/{program_id}/feedback-link/` | Get feedback form URL and QR code for program | JWT + role check |

**Query parameters for list endpoint:**

| Parameter | Type | Description |
|---|---|---|
| `type` | str[] | Program type filter |
| `target_audience` | str[] | Audience filter |
| `status` | str[] | Status filter |
| `branch` | int[] | Branch filter |
| `date_from` | date | Start of date range |
| `date_to` | date | End of date range |
| `page` | int | Page number |
| `page_size` | int | 25 default |
| `search` | str | Program name |

---

## 12. HTMX Patterns

| Interaction | HTMX Attributes | Behaviour |
|---|---|---|
| Filter form apply | `hx-get="/api/.../mh-programs/"` `hx-trigger="change"` `hx-target="#programs-table-body"` `hx-include="#filter-form"` | Table and KPI bar refreshed |
| Pagination | `hx-get="/api/.../mh-programs/?page={n}"` `hx-target="#programs-table-body"` `hx-push-url="true"` | Page swap |
| Program detail drawer open | `hx-get="/api/.../mh-programs/{program_id}/"` `hx-target="#drawer-container"` `hx-trigger="click"` | Drawer slides in; Details tab default |
| Drawer tab switch | `hx-get="/api/.../mh-programs/{program_id}/?tab={tab_slug}"` `hx-target="#drawer-tab-content"` | Tab content replaced |
| Feedback tab load | `hx-get="/api/.../mh-programs/{program_id}/feedback/"` `hx-target="#feedback-content"` `hx-trigger="click[tab='feedback']"` | Feedback data loaded on tab click |
| Outcomes tab load | `hx-get="/api/.../mh-programs/{program_id}/outcomes/"` `hx-target="#outcomes-content"` `hx-trigger="click[tab='outcomes']"` | Outcomes loaded on tab click |
| Attendance update drawer save | `hx-patch="/api/.../mh-programs/{program_id}/schedule/{branch_id}/"` `hx-target="#schedule-row-{branch_id}"` `hx-swap="outerHTML"` | Schedule row updated; toast fired |
| Attendance sheet upload | `hx-post="/api/.../mh-programs/{program_id}/schedule/{branch_id}/upload/"` `hx-encoding="multipart/form-data"` `hx-target="#upload-status-{branch_id}"` | Upload indicator updated |
| Mark complete button | `hx-post="/api/.../mh-programs/{program_id}/complete/"` `hx-target="#program-row-{program_id}"` `hx-swap="outerHTML"` | Row status badge updated; toast fired |
| Cancel program modal submit | `hx-delete="/api/.../mh-programs/{program_id}/"` `hx-target="#program-row-{program_id}"` `hx-swap="outerHTML"` | Row updated to Cancelled status |
| Send reminder | `hx-post="/api/.../mh-programs/{program_id}/remind/{branch_id}/"` `hx-target="#remind-btn-{branch_id}"` | Button replaced with "Reminder Sent" badge |
| Feedback link copy | `hx-get="/api/.../mh-programs/{program_id}/feedback-link/"` `hx-target="#feedback-link-display"` | QR code and link shown in drawer |
| Program create form submit | `hx-post="/api/.../mh-programs/"` `hx-target="#programs-table-body"` `hx-on::after-request="closeDrawer(); fireToast();"` | New row prepended; drawer closed |
| KPI bar refresh | `hx-get="/api/.../mh-programs/kpi/"` `hx-trigger="load, filterApplied from:body"` `hx-target="#kpi-bar"` | On load and post-filter |
| Alert banner load | `hx-get="/api/.../mh-programs/alerts/"` `hx-trigger="load"` `hx-target="#alert-banner"` | Conditional display |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
