# 11 — Health Screening Manager

> **URL:** `/group/health/screening/`
> **File:** `11-health-screening-manager.md`
> **Template:** `portal_base.html`
> **Priority:** P1
> **Role:** Group Medical Coordinator (primary) · Group School Medical Officer

---

## 1. Purpose

Manage annual health screening programs across all branches in the group. Screening programs are structured, scheduled health checks conducted for entire classes or student cohorts — they are distinct from individual medical room consultations.

Screening types covered: general physical examination, eye test, dental check, BMI recording, hearing test, blood group identification (for new students), and haemoglobin test (for girls — anaemia screening). Each type may be run as a standalone program or combined into a comprehensive annual health screening week.

This page enables the Medical Coordinator to plan and assign screening programs to branches at the start of each academic year, track branch-level completion status, monitor screened vs pending student counts, capture aggregate result summaries, flag students with abnormal findings for follow-up action, and enforce accountability where branches have not yet conducted their scheduled screenings.

Scale: 1–3 screening events per branch per academic year × 20–50 branches = 20–150 screening events per year at group level. During a large annual screening week, 500–2,000 students may be screened across branches on the same day.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Medical Coordinator | G3 | Full — create programs, assign branches, view all results, manage flagged actions | Primary owner |
| Group School Medical Officer | G3 | Update progress for own branch, upload result reports, flag abnormal counts | Cannot create new programs |
| Group Mental Health Coordinator | G3 | View — mental health / psychological stress screening programs only | Read-only; filter enforced server-side |
| Branch Principal | Branch G3 | View own branch screening schedule and completion status | Read-only |
| All other roles | — | — | No access |

> **Access enforcement:** `@require_role('medical_coordinator', 'school_medical_officer', 'mental_health_coordinator')` with branch-scoped queryset for School Medical Officer and category-filter for Mental Health Coordinator.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Health & Medical  ›  Health Screening Manager
```

### 3.2 Page Header
- **Title:** `Health Screening Manager`
- **Subtitle:** `[N] Programs This AY · [N] Complete · [N] In Progress · [N] Planned`
- **Right controls:** `+ Create Screening Program` (Medical Coordinator only) · `Advanced Filters` · `Export`

### 3.3 Alert Banner

| Condition | Banner Text | Severity |
|---|---|---|
| Branch with no screening planned this AY | "[N] branches have no screening program planned for this academic year." | Red |
| Screening overdue > 60 days vs schedule | "[N] screenings are more than 60 days overdue against their scheduled date." | Red |
| High rate of abnormal findings (> 10% at a branch) | "High abnormal finding rate detected at [Branch]: [N]% of screened students flagged." | Amber |
| Flagged student with no action taken | "[N] students have been flagged with abnormal findings but no follow-up action has been assigned." | Amber |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule |
|---|---|---|
| Screening Events This AY | Total programs in current academic year (all statuses) | Blue always |
| Branches with All Screenings Complete | Branches where all assigned programs are in Complete status | Green = 100% · Yellow < 90% · Red < 70% |
| Students Screened This AY | Cumulative unique students screened across all completed programs this AY | Blue always |
| Students Pending Screening | Students targeted but not yet screened in In-Progress or Planned programs | Yellow if > 0 · Green if 0 |
| Abnormal Findings Flagged | Total students flagged with abnormal findings requiring follow-up across all programs this AY | Green = 0 · Yellow 1–20 · Red > 20 |
| Follow-up Actions Pending | Flagged students where follow-up action not yet completed | Green = 0 · Yellow 1–10 · Red > 10 |

---

## 5. Main Tables

### 5.1 Program Master Table

**Search:** Program name. 300ms debounce.

**Advanced Filters:**

| Filter | Type | Options |
|---|---|---|
| Screening Type | Checkbox | Eye / Dental / BMI / Blood Group / Haemoglobin / Hearing / Full Physical / Mental Health |
| Academic Year | Single-select | Current AY + last 3 AYs |
| Status | Checkbox | Planned / In-Progress / Complete / Cancelled |
| Branch | Multi-select | All branches |

**Columns:**

| Column | Sortable | Notes |
|---|---|---|
| Program Name | ✅ | Link → `screening-program-detail` drawer |
| Type | ✅ | Colour-coded badge: Eye (blue) / Dental (teal) / BMI (grey) / Blood Group (red) / Haemoglobin (orange) / Hearing (purple) / Full Physical (green) / Mental Health (indigo) |
| Target Class | ✅ | e.g., "All classes" or "Class 6–8" |
| Academic Year | ✅ | |
| Branches Assigned | ✅ | Count of branches assigned; tooltip shows list |
| Start Date | ✅ | Date |
| End Date | ✅ | Date; red if past end date and not Complete |
| Status | ✅ | Planned (grey) / In-Progress (blue) / Complete (green) / Cancelled (red) |
| Completion % | ✅ | Progress bar: % of assigned branches in Complete status |
| Actions | ❌ | View · Edit (Coordinator) · Send Reminder |

**Default sort:** Status (In-Progress first, then Planned, then Complete), then Start Date ascending.
**Pagination:** Server-side · 25/page.

---

### 5.2 Branch Completion Sub-table

Displayed as an expandable row beneath each program in the Program Master Table. Triggered by clicking the expand chevron on a program row.

**Columns:**

| Column | Sortable | Notes |
|---|---|---|
| Branch | ✅ | Branch name |
| Scheduled Date | ✅ | Planned date for this branch |
| Doctor / Nurse | ✅ | Assigned healthcare professional |
| Students Targeted | ✅ | Target count for this screening |
| Students Screened | ✅ | Actual count completed |
| Pending | ✅ | Targeted minus Screened; red if > 0 |
| Abnormal Findings | ✅ | Count of flagged students; amber if > 0 |
| Status | ✅ | Not Started / In-Progress / Complete / Skipped |
| Actions | ❌ | View Results · Update Progress · Upload Report |

Sub-table loads via HTMX on row expand. Pagination within sub-table: 10/page.

---

## 6. Drawers / Modals

### 6.1 Drawer — `screening-program-detail` (700px, right side)

Triggered by program name link or **View** action.

**Tabs:**

#### Tab 1 — Program Details
| Field | Notes |
|---|---|
| Program Name | |
| Screening Type | Badge |
| Description | Full text description of what the screening covers |
| Target Classes | e.g., "Class 1 to 5" or "All Classes" |
| Academic Year | |
| Responsible Doctor | Name + qualification |
| Screening Criteria | What counts as normal vs abnormal for each finding type |
| Expected Findings to Flag | Checklist: e.g., visual acuity < 6/12, BMI > 30, Hb < 12 g/dL |

#### Tab 2 — Branch Progress
Per-branch status table identical to Section 5.2 sub-table, but shown inside drawer with ability to drill down into individual branch results.

| Column | Notes |
|---|---|
| Branch | |
| Scheduled Date | |
| Doctor / Nurse | |
| Students Targeted | |
| Students Screened | |
| Abnormal Findings | |
| Status | |
| Report Uploaded | Yes / No |
| Actions | Update Progress · View Report |

#### Tab 3 — Results Summary
Aggregate findings across all branches for this program.

| Metric | Value |
|---|---|
| Total Branches Assigned | |
| Branches Completed | |
| Total Students Targeted | |
| Total Students Screened | |
| Screening Coverage % | |
| Abnormal Findings (total) | |
| Abnormal Finding Rate % | |

**Findings breakdown table:**

| Finding Type | Total Checked | Abnormal | Abnormal % | Action Required |
|---|---|---|---|---|
| Visual Acuity | | | | |
| BMI | | | | |
| Haemoglobin | | | | |
| Dental Caries | | | | |
| Hearing | | | | |
| Blood Pressure | | | | |

#### Tab 4 — Actions Required
Students flagged with abnormal findings requiring follow-up.

| Column | Notes |
|---|---|
| Student Name | Identifiable — Medical Coordinator only |
| Branch | |
| Class | |
| Finding | e.g., "Visual acuity < 6/12" |
| Recommended Action | e.g., "Refer to ophthalmologist" |
| Assigned To | Counsellor / Doctor / Parent |
| Status | Pending / In-Progress / Completed |
| Actions | Update · Flag Student · Mark Complete |

Filtering within tab: Branch (multi-select), Finding Type (multi-select), Status (radio).

---

### 6.2 Drawer — `screening-program-create` (640px, right side)

Triggered by **+ Create Screening Program** (Medical Coordinator only).

| Field | Type | Validation |
|---|---|---|
| Program Name | Text input (max 150 chars) | Required |
| Screening Type | Single-select: Eye / Dental / BMI / Blood Group / Haemoglobin / Hearing / Full Physical / Mental Health | Required |
| Description | Textarea (max 1,000 chars) | Optional |
| Target Classes | Multi-select (KG / Class 1–12 / All) | Required |
| Academic Year | Single-select | Required |
| Assign Branches | Multi-select (with Select All option) | Required |
| Start Date | Date picker | Required |
| End Date | Date picker | Required; must be after start date |
| Responsible Doctor | Single-select (from doctor/staff registry) | Required |
| Doctor / Nurse per Branch | Repeating table: Branch → Assigned person | Auto-populated from branch assignment; editable |
| Standard Findings Checklist | Checkbox list: define what findings to record per screening type | Required |
| Abnormal Threshold Definitions | Repeating: Finding · Threshold value · Unit | Optional; used for auto-flagging |

**Footer:** `Cancel` · `Save as Draft` · `Create Program`

---

### 6.3 Drawer — `branch-screening-update` (580px, right side)

Triggered by **Update Progress** action in branch sub-table or Actions Required tab. School Medical Officer (own branch) or Medical Coordinator.

| Field | Type | Validation |
|---|---|---|
| Branch | Read-only | |
| Program | Read-only | |
| Scheduled Date | Read-only | |
| Actual Date Conducted | Date picker | Required |
| Students Targeted | Read-only | |
| Students Screened | Number input | Required; must be ≤ targeted |
| Pending Count | Auto-calculated | Read-only |
| Abnormal Findings Count | Number input | Required |
| Findings Details | Textarea (max 500 chars) | Optional — summary of findings |
| Status Update | Radio — In-Progress / Complete / Skipped | Required |
| Upload Result Report | File upload (PDF, max 20 MB) | Required before marking Complete |
| Notes | Textarea (max 500 chars) | Optional |

**Footer:** `Cancel` · `Save Update`

---

### 6.4 Modal — `flag-student-action` (460px, centred)

Triggered by **Flag Student** in the Actions Required tab. Medical Coordinator or School Medical Officer.

| Field | Type | Validation |
|---|---|---|
| Student Name | Read-only | |
| Student ID | Read-only | |
| Branch / Class | Read-only | |
| Screening Finding | Read-only | |
| Recommended Action | Textarea (max 300 chars) | Required |
| Notify | Multi-select: Parent / School Counsellor / School Doctor / Principal | At least one required |
| Urgency | Radio — Routine / Urgent | Required |
| Assign To | Single-select (staff member for follow-up) | Required |
| Target Resolution Date | Date picker | Required |

**Footer:** `Cancel` · `Flag & Notify`

---

## 7. Toast Messages

| Action | Toast Text | Type |
|---|---|---|
| Program created | "Screening program created successfully." | Success |
| Program updated | "Screening program updated." | Success |
| Branch progress updated | "Branch screening progress updated." | Success |
| Report uploaded | "Result report uploaded successfully." | Success |
| Reminder sent | "Reminder sent to [Branch] for pending screening." | Success |
| Student flagged | "Student flagged — notification sent to assigned contacts." | Success |
| Flag action completed | "Follow-up action marked as complete." | Success |
| Program cancelled | "Screening program cancelled." | Info |
| Save failed | "Please complete all required fields before saving." | Error |

---

## 8. Empty States

| Context | Heading | Sub-text | Action |
|---|---|---|---|
| No programs this AY | "No screening programs for this academic year." | "Create the first screening program to get started." | `+ Create Screening Program` button |
| No results for filters | "No programs match your current filters." | "Try adjusting filters." | `Clear Filters` |
| No branches complete | "No branches have completed this screening yet." | "Branch progress will appear here as updates are submitted." | — |
| No abnormal findings | "No abnormal findings flagged for this program." | "All screened students are within normal parameters." | — |
| No actions required | "No follow-up actions pending." | "All flagged student actions have been completed." | — |

---

## 9. Loader States

| Context | Loader Behaviour |
|---|---|
| Initial page load | Full-page skeleton: KPI bar (6 grey cards) + program table (6 grey rows × 9 columns) |
| Filter apply | Table body spinner overlay; KPI bar refreshes after |
| Branch sub-table expand | Expand animation with row skeleton (5 grey rows × 9 columns) while loading |
| Screening detail drawer open | Drawer skeleton: tab headers + 3 grey content blocks per tab |
| Branch progress update save | Submit button spinner; form disabled |
| Send reminder | Button spinner + "Sending…" label; re-enabled on completion |
| Results summary tab | Metrics skeleton (6 grey number blocks) + findings table skeleton |

---

## 10. Role-Based UI Visibility

| UI Element | Medical Coordinator | School Medical Officer | Mental Health Coordinator | Branch Principal |
|---|---|---|---|---|
| + Create Screening Program | ✅ | ❌ | ❌ | ❌ |
| Edit Program | ✅ | ❌ | ❌ | ❌ |
| View all programs | ✅ | ✅ (all types — own branch) | ✅ (Mental Health programs only) | ✅ (own branch) |
| Branch sub-table — all branches | ✅ | Own branch only | Own branch — Mental Health programs | Own branch only |
| Update Progress action | ✅ | ✅ (own branch) | ❌ | ❌ |
| Upload Result Report | ✅ | ✅ (own branch) | ❌ | ❌ |
| Actions Required tab | ✅ (student names visible) | ✅ (student names visible — own branch) | ❌ | ❌ |
| Flag Student action | ✅ | ✅ (own branch) | ❌ | ❌ |
| Send Reminder | ✅ | ❌ | ❌ | ❌ |
| Export button | ✅ | ❌ | ❌ | ❌ |
| KPI bar | ✅ Full | ✅ Full (own branch) | Filtered counts only | Own branch status only |
| Alert banners | ✅ | ✅ (own branch) | ❌ | ❌ |

---

## 11. API Endpoints

### Base URL: `/api/v1/group/{group_id}/health/screening/`

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/health/screening/` | List all screening programs (paginated, filtered) | JWT + role check |
| POST | `/api/v1/group/{group_id}/health/screening/` | Create new screening program | Medical Coordinator |
| GET | `/api/v1/group/{group_id}/health/screening/{program_id}/` | Retrieve screening program detail | JWT + role check |
| PATCH | `/api/v1/group/{group_id}/health/screening/{program_id}/` | Update screening program | Medical Coordinator |
| DELETE | `/api/v1/group/{group_id}/health/screening/{program_id}/` | Cancel screening program (soft delete) | Medical Coordinator |
| GET | `/api/v1/group/{group_id}/health/screening/kpi/` | KPI summary bar data | JWT + role check |
| GET | `/api/v1/group/{group_id}/health/screening/{program_id}/branches/` | Branch completion sub-table for a program | JWT + role check |
| PATCH | `/api/v1/group/{group_id}/health/screening/{program_id}/branches/{branch_id}/` | Update branch screening progress | School Medical Officer / Medical Coordinator |
| POST | `/api/v1/group/{group_id}/health/screening/{program_id}/branches/{branch_id}/upload/` | Upload result report PDF for a branch | School Medical Officer / Medical Coordinator |
| GET | `/api/v1/group/{group_id}/health/screening/{program_id}/results/` | Aggregate results summary | Medical Coordinator |
| GET | `/api/v1/group/{group_id}/health/screening/{program_id}/actions/` | Actions required — flagged students | JWT + role check |
| POST | `/api/v1/group/{group_id}/health/screening/{program_id}/actions/` | Flag a student for follow-up | School Medical Officer / Medical Coordinator |
| PATCH | `/api/v1/group/{group_id}/health/screening/{program_id}/actions/{action_id}/` | Update flagged action status | JWT + role check |
| POST | `/api/v1/group/{group_id}/health/screening/{program_id}/remind/{branch_id}/` | Send reminder to branch | Medical Coordinator |
| GET | `/api/v1/group/{group_id}/health/screening/alerts/` | Fetch active alert conditions | JWT + role check |
| GET | `/api/v1/group/{group_id}/health/screening/export/` | Export screening report CSV | Medical Coordinator |

**Query parameters for list endpoint:**

| Parameter | Type | Description |
|---|---|---|
| `type` | str[] | Screening type filter |
| `academic_year` | str | Academic year filter |
| `status` | str[] | Status filter |
| `branch` | int[] | Branch filter |
| `page` | int | Page number |
| `page_size` | int | 25 default |
| `search` | str | Program name search |

---

## 12. HTMX Patterns

| Interaction | HTMX Attributes | Behaviour |
|---|---|---|
| Filter form apply | `hx-get="/api/.../screening/"` `hx-trigger="change"` `hx-target="#program-table-body"` `hx-include="#filter-form"` | Table refreshed; KPI bar updated via separate trigger |
| Pagination | `hx-get="/api/.../screening/?page={n}"` `hx-target="#program-table-body"` `hx-push-url="true"` | Page swap |
| Branch sub-table expand | `hx-get="/api/.../screening/{program_id}/branches/"` `hx-trigger="click"` `hx-target="#branch-sub-{program_id}"` `hx-swap="innerHTML"` | Sub-table rows loaded inline; chevron rotated |
| Branch sub-table collapse | `hx-trigger="click"` `hx-swap="innerHTML"` with empty response | Sub-table rows cleared |
| Program detail drawer open | `hx-get="/api/.../screening/{program_id}/"` `hx-target="#drawer-container"` `hx-trigger="click"` | Drawer slides in; Tab 1 loaded |
| Drawer tab switch | `hx-get="/api/.../screening/{program_id}/?tab={tab_slug}"` `hx-target="#drawer-tab-content"` | Tab content replaced |
| Status update inline (sub-table) | `hx-patch="/api/.../screening/{program_id}/branches/{branch_id}/"` `hx-target="#branch-row-{branch_id}"` `hx-swap="outerHTML"` | Row updated with new status badge |
| Branch progress update drawer save | `hx-patch="/api/.../screening/{program_id}/branches/{branch_id}/"` `hx-target="#branch-row-{branch_id}"` | Row refreshed; drawer closed; toast fired |
| Upload result report | `hx-post="/api/.../screening/{program_id}/branches/{branch_id}/upload/"` `hx-encoding="multipart/form-data"` `hx-target="#upload-status-{branch_id}"` | Upload status indicator updated |
| Flag student modal submit | `hx-post="/api/.../screening/{program_id}/actions/"` `hx-target="#actions-table"` | Actions table refreshed; modal closed; toast fired |
| Send reminder | `hx-post="/api/.../screening/{program_id}/remind/{branch_id}/"` `hx-target="#remind-btn-{branch_id}"` | Button replaced with "Reminder Sent" badge |
| KPI bar refresh | `hx-get="/api/.../screening/kpi/"` `hx-trigger="load, filterApplied from:body"` `hx-target="#kpi-bar"` | On load and post-filter |
| Alert banner load | `hx-get="/api/.../screening/alerts/"` `hx-trigger="load"` `hx-target="#alert-banner"` | Conditional display |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
