# 22 — College & Career Guidance Tracker

> **URL:** `/group/welfare/counselling/guidance/`
> **File:** `22-college-career-guidance-tracker.md`
> **Template:** `portal_base.html`
> **Priority:** P1
> **Role:** Group Counselling Head (Role 94, G3) — primary owner

---

## 1. Purpose

Tracks the college and career guidance programme for all Class 11 and Class 12 students (and equivalent coaching-stream students preparing for competitive entrance exams) across all branches in the group. The programme runs throughout the academic year across six structured phases:

1. **Interest Profiling** — subject preferences, career interests, parental expectations (Class 11, Q1)
2. **Aptitude Testing** — standardised aptitude battery administered by the branch counsellor (Class 11, Q2)
3. **Stream / College Shortlisting** — counsellor-facilitated shortlisting of target streams and 5–10 colleges (Class 11–12, Q2–Q3)
4. **Entrance Exam Guidance** — JEE / NEET / CLAT / IPM / CUET / State PG exam preparation counselling, including study plans and test-series tracking (Class 12, Q3–Q4)
5. **College Application Tracking** — application submissions, portal verifications, document checklists (Class 12, Q4)
6. **Offer & Admission Outcomes** — offer letters received, final admission, institution name, stream, admission category (Open / OBC / SC / ST / Management / NRI)

The Group Counselling Head uses this tracker to:
- Ensure every eligible student receives at least 2 individual guidance sessions per academic year
- Track application success rates and offer conversion rates branch by branch
- Compile the group-wide college placement report for the Group Chairman at the end of each academic year
- Benchmark branches against each other on guidance coverage and placement quality
- Identify counsellors with high placement rates for recognition and best-practice sharing
- Flag branches with low guidance coverage for corrective intervention

Scale: 5,000–30,000 eligible students across 20–50 branches. Data is branch-logged; the Counselling Head has a consolidated cross-branch view.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Counselling Head | G3 | Full read + export + generate placement report | Primary owner; all branches, all students |
| Branch Counsellor | Branch | Create + edit own branch's student guidance records | Cannot view other branches' student data |
| Branch Principal | Branch | Read own branch — aggregate and per-student view | No edit; no cross-branch |
| Group Academic Director | G3 | Read all — aggregate and per-student | No edit |
| Group Chairman / CEO | G5/G4 | Read — aggregate summary + placement report PDF | No individual student records; report only |
| All other roles | — | No access | — |

> **Access enforcement:** `@require_role('counselling_head', 'branch_counsellor', 'branch_principal', 'academic_director', 'chairman')` with branch-scoped querysets for Branch Counsellor and Branch Principal. Chairman sees only aggregate widgets and can download the generated PDF — no row-level data.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Welfare & Safety  ›  Career Guidance  ›  College & Career Guidance Tracker
```

### 3.2 Page Header
- **Title:** `College & Career Guidance Tracker`
- **Subtitle:** `[Academic Year] · [N] Eligible Students · [N] Branches · Last synced [timestamp]`
- **Right controls:** `+ Add Student Record` (Branch Counsellor + Counselling Head) · `Batch Record Session` · `Generate Placement Report` (Counselling Head only) · `Advanced Filters` · `Export CSV` (Counselling Head + Academic Director)

### 3.3 Alert Banner

| Condition | Banner Text | Severity |
|---|---|---|
| Student has 0 sessions with < 60 days to board exam | "[N] Class 12 students have had zero guidance sessions and have fewer than 60 days to their target exam." | Red |
| Branch guidance coverage below 50% | "[N] branches have fewer than 50% of eligible students profiled. Immediate follow-up required." | Red |
| Application deadlines approaching (≤ 7 days) | "[N] students have college application deadlines in the next 7 days. Verify submission status." | Amber |
| Counsellor workload imbalance | "Counsellor [Name] at [Branch] has [N] unassigned students. Reassignment may be needed." | Amber |
| Placement report due in 7 days | "The Annual College Placement Report is due to the Chairman in 7 days. [N] student outcomes are still pending." | Amber |

---

## 4. KPI Summary Bar

Eight cards displayed in a responsive 4×2 grid. All metrics are filtered by the currently selected Academic Year and Branch filters.

| # | Card | Metric | Colour Rule |
|---|---|---|---|
| 1 | Students Profiled % | (Students with profile completed / Total eligible students) × 100 | Green ≥ 80% · Yellow 50–79% · Red < 50% |
| 2 | Avg Sessions Per Student | Total individual guidance sessions / Total eligible students | Green ≥ 2.0 · Yellow 1.0–1.9 · Red < 1.0 |
| 3 | Applications Submitted | Total college applications submitted by all students | Blue always |
| 4 | Offers Received Rate | (Students with ≥ 1 offer / Students who applied) × 100 | Green ≥ 70% · Yellow 40–69% · Red < 40% |
| 5 | Admissions Confirmed | Count of students with final admission confirmed | Blue always |
| 6 | Top Destination (count) | Name and count of most-appearing college in Final Admission column | Blue always; mini list of top 3 on hover |
| 7 | High-Placement Counsellors | Count of counsellors whose assigned students have ≥ 70% offer rate | Green always |
| 8 | Branches with Lowest Coverage | Count of branches with guidance coverage below group average | Red if > 3 · Yellow 1–3 · Green = 0 |

---

## 5. Main Table — Student Guidance Records

### 5.1 Search
Full-text search on: Student Code, Student Name (Counselling Head only), Branch Name, Counsellor Name. Debounce 300 ms, minimum 2 characters. Results replace table body via HTMX.

### 5.2 Advanced Filters

| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Class | Checkbox | Class 11 · Class 12 |
| Stream | Checkbox | MPC · BiPC · MEC · CEC · Integrated Coaching |
| Target Exam | Checkbox | JEE · NEET · CLAT · CUET · IPM · State PG · None / Other |
| Profile Completed | Radio | All · Yes · No |
| Aptitude Test Done | Radio | All · Yes · No |
| Application Status | Checkbox | Not Started · In Progress · Submitted · Deadline Passed |
| Admission Status | Checkbox | Pending · Offer Received · Confirmed · Not Admitted |
| Sessions Count | Range | Min – Max (integer) |
| Academic Year | Single-select | Current + 3 prior years |

### 5.3 Table Columns

| Column | Sortable | Notes |
|---|---|---|
| Student Code | ✅ | System ID; name shown to Counselling Head + assigned counsellor only |
| Branch | ✅ | Branch name |
| Class / Stream | ✅ | "Class 12 / MPC", "Class 11 / BiPC", etc. |
| Counsellor Assigned | ✅ | Name; "(Unassigned)" in amber if blank |
| Profile Completed | ✅ | Green tick / Red cross badge |
| Aptitude Test Done | ✅ | Green tick / Red cross badge |
| Sessions Count | ✅ | Integer; red if 0 and Class 12 |
| Target Colleges | ✅ | Count of shortlisted colleges |
| Applications Submitted | ✅ | Integer |
| Offers Received | ✅ | Integer |
| Final Admission | ✅ | "College Name — Stream" or "Pending" (grey) |
| Admission Category | ✅ | Open / OBC / SC / ST / Management / NRI badge; blank if pending |
| Status | ✅ | Profiling · Counselling · Applying · Offer Received · Admitted · Withdrawn badge |
| Actions | ❌ | View Profile · Log Session · Edit |

**Default sort:** Status (Applying → Counselling → Profiling), then Sessions Count ascending (fewest-attended first).
**Pagination:** Server-side · 25 rows/page · page indicator shows "Showing [X]–[Y] of [N]".

### 5.4 Funnel Visualisation (above table, collapsible)

Horizontal funnel showing group-wide progression for currently selected filters:

```
Profiled [N] → Counselled (≥2 sessions) [N] → Applied [N] → Offer Received [N] → Admitted [N]
```

Each stage is a clickable segment that pre-filters the table to students at that stage.

### 5.5 Charts Panel (right sidebar, collapsible)

- **Bar chart:** Branch-wise placement rate (Admitted / Eligible × 100%) — sorted descending
- **Pie chart:** Stream distribution of confirmed admissions (MPC / BiPC / MEC / CEC / Other)

---

## 6. Drawers / Modals

### 6.1 Drawer — `student-guidance-profile` (680px, right side)

Triggered by **View Profile** in Actions column.

**Header:** Student Code · Branch · Class/Stream · Status badge

**Tabs:**

#### Tab 1 — Profile
| Field | Notes |
|---|---|
| Student Code | Read-only |
| Student Name | Visible to Counselling Head + assigned counsellor only |
| Class | Read-only |
| Stream | Read-only |
| Branch | Read-only |
| Hostel / Day Scholar | Read-only |
| Career Interest Areas | Multi-tag — e.g., Engineering, Medicine, Law, Management, Civil Services |
| Parental Expectation | Free text (max 500 chars) |
| Preferred Geography | Single-select: Home State · Any Indian State · International |
| Profile Completed | Toggle |
| Profiling Date | Date |
| Notes | Textarea (max 1,000 chars) |

#### Tab 2 — Sessions
Chronological list of all guidance sessions for this student.

| Column | Notes |
|---|---|
| Session # | Sequential count |
| Date | DD-MMM-YYYY |
| Counsellor | Name |
| Session Type | Individual / Group |
| Topics Covered | Tags: Stream Selection / Exam Strategy / Application Help / Motivation / Other |
| Duration (mins) | |
| Outcome | Free text summary |
| Next Steps | |

**Footer actions:** `+ Log Session` button opens the `batch-session-record` drawer pre-filled for this student only.

#### Tab 3 — Colleges
| Column | Notes |
|---|---|
| # | Row counter |
| College Name | |
| Stream / Programme | |
| City / State | |
| Entrance Exam Required | Yes / No |
| Priority | High / Medium / Low (colour badge) |
| Added Date | |
| Actions | Remove |

**Footer:** `+ Add Target College` inline row form.

#### Tab 4 — Applications
| Column | Notes |
|---|---|
| College Name | |
| Programme | |
| Application Portal | Link (optional) |
| Submission Deadline | Date; red if past and not submitted |
| Submitted On | Date or "Pending" |
| Application Status | Not Started / In Progress / Submitted / Deadline Passed badge |
| Documents Verified | Checkbox |
| Notes | |

**Footer:** `+ Add Application`

#### Tab 5 — Offers
| Column | Notes |
|---|---|
| College | |
| Programme | |
| Offer Date | |
| Offer Type | Merit / Management / Scholarship / Waitlist |
| Offer Letter | Upload link (PDF) |
| Status | Pending Decision / Accepted / Declined |

**Footer:** `+ Record Offer`

#### Tab 6 — Outcome
| Field | Type | Validation |
|---|---|---|
| Final Admission — College | Text input | Required if admitted |
| Final Admission — Programme / Stream | Text input | Required if admitted |
| Admission Category | Single-select: Open / OBC / SC / ST / Management / NRI | Required if admitted |
| Admission Date | Date picker | Required if admitted |
| Fee Scholarship Received | Toggle + amount (optional) | Optional |
| Outcome Status | Radio: Admitted · Not Admitted · Deferred · Withdrawn | Required |
| Counsellor Remarks | Textarea (max 1,000 chars) | Optional |

**Footer:** `Cancel` · `Save Outcome`

**Validation rules:**
- Profile tab: Career Interest Areas required before Tab is saved; max 5 tags
- Sessions tab: Date required; must not be in future; Topics Covered at least one tag
- Colleges tab: College Name required; max 10 target colleges per student
- Applications tab: Submission Deadline required; if status = Submitted, Submitted On required
- Outcome tab: if Outcome Status = Admitted, Final Admission fields are required

---

### 6.2 Drawer — `batch-session-record` (560px, right side)

Triggered by **Batch Record Session** button in page header. Allows a counsellor to record a single group guidance session for multiple students simultaneously.

| Field | Type | Validation |
|---|---|---|
| Branch | Single-select (auto-set for branch counsellor) | Required |
| Session Date | Date picker (defaults to today) | Required; not future |
| Session Type | Radio — Group Guidance | Fixed; this drawer is for group sessions only |
| Counsellor | Single-select (auto-set for branch counsellor) | Required |
| Topics Covered | Multi-select: Stream Selection / Exam Strategy / Application Help / Motivation / Interview Prep / Other | Required; at least one |
| Duration (mins) | Number input | Required; min 15, max 480 |
| Students in Session | Multi-select student search (autocomplete; branch-scoped; shows Student Code + Class/Stream) | Required; min 2 students |
| Session Summary | Textarea (max 2,000 chars) | Required |
| Next Steps for Group | Textarea (max 1,000 chars) | Optional |
| Follow-up Session Needed | Toggle | Optional |
| Follow-up Date | Date picker | Required if follow-up = Yes |

**Behaviour:** On save, one session record is created for each selected student; Sessions Count increments on each student row in the main table.

**Footer:** `Cancel` · `Record Session for [N] Students`

**Validation:** Students list must have at least 2 entries; if session date is more than 7 days in the past, a confirmation prompt is shown: *"You are recording a session that occurred [N] days ago. Confirm?"*

---

### 6.3 Modal — `placement-report-generator` (480px, centred)

Triggered by **Generate Placement Report** button. Counselling Head only.

| Field | Type | Validation |
|---|---|---|
| Academic Year | Single-select (current + 3 prior) | Required |
| Branches to Include | Multi-select (default: all branches) | Required; at least one |
| Include Student-Level Detail | Toggle (default: Off — aggregate only) | Optional |
| Include Benchmark Comparison | Toggle — compare against prior year | Optional |
| Report Format | Radio — PDF · Excel | Required |
| Report Title (editable) | Text input (default: "Group College Placement Report — [Year]") | Required; max 100 chars |
| Prepared By | Read-only (logged-in user name) | Auto |
| Date | Read-only (today) | Auto |

**Footer:** `Cancel` · `Generate Report`

**Behaviour:** On submit, a POST is made to the async report generation endpoint. A progress indicator replaces the modal body while the report compiles. On completion, a download link appears. Report includes: executive summary (KPI snapshot), branch-wise placement table, funnel chart, stream distribution pie, top destination colleges list, counsellor performance table, and (if enabled) student-level outcome appendix.

**Toast on generation start:** *"Placement report is being generated. You will be notified when it is ready."* (Info)
**Toast on completion:** *"Placement Report for [Year] is ready. Click to download."* (Success)

---

## 7. Toast Messages

| Action | Toast Text | Type |
|---|---|---|
| Student record created | "Guidance record created for [Student Code]." | Success |
| Student record updated | "Guidance record updated." | Success |
| Session logged (single) | "Guidance session logged for [Student Code]." | Success |
| Batch session recorded | "Group session recorded for [N] students." | Success |
| Outcome saved | "Admission outcome recorded for [Student Code]." | Success |
| College added to shortlist | "College added to target list." | Success |
| Application status updated | "Application status updated." | Success |
| Offer recorded | "Offer recorded successfully." | Success |
| Report generation started | "Placement report is being generated. You will be notified when ready." | Info |
| Report ready | "Placement Report for [Year] is ready. Click to download." | Success |
| CSV export triggered | "Export is being prepared." | Info |
| Validation error | "Please complete all required fields before saving." | Error |
| Duplicate session warning | "A session was already recorded for this student on [Date]. Confirm to add another." | Warning |

---

## 8. Empty States

| Context | Heading | Sub-text | Action |
|---|---|---|---|
| No students for selected filters | "No student records match the current filters." | "Try adjusting or clearing your filters." | `Clear Filters` button |
| No eligible students in branch | "No eligible students found for this branch and year." | "Eligible students (Class 11–12) will appear here once enrolled." | — |
| Colleges tab — no colleges added | "No target colleges added." | "Add colleges the student is targeting to begin tracking applications." | `+ Add Target College` |
| Applications tab — no applications | "No applications recorded." | "Record application submissions here once students begin applying." | `+ Add Application` |
| Offers tab — no offers | "No offers received yet." | "Offer letters will be recorded here as results are announced." | `+ Record Offer` |
| Sessions tab — no sessions | "No guidance sessions recorded." | "Log the first session to begin tracking this student's progress." | `+ Log Session` |
| Report generator — no data for selected year | "No student outcome data for the selected year." | "Ensure outcomes have been recorded before generating the report." | — |

---

## 9. Loader States

| Context | Loader Behaviour |
|---|---|
| Initial page load | Full-page skeleton: 8 KPI cards (grey rectangles) + funnel bar (grey gradient) + chart panel placeholders + table (10 grey rows × 13 columns) |
| Filter / search apply | Table body spinner overlay; KPI cards and funnel update after table resolves |
| Drawer open | Drawer skeleton: tab headers + 6 grey field blocks |
| Tab switch inside drawer | Tab content area shows spinner for 400 ms then resolves |
| Batch session student search | Dropdown spinner below autocomplete field |
| Report generation | Modal body replaced with progress bar + "Compiling report…" label; cancel button disabled during generation |
| Chart panel load | Bar chart: horizontal skeleton bars; Pie chart: grey donut placeholder |
| CSV export | Button replaced with spinner + "Preparing export…" label |

---

## 10. Role-Based UI Visibility

| UI Element | Counselling Head | Branch Counsellor | Branch Principal | Academic Director | Chairman |
|---|---|---|---|---|---|
| Full cross-branch student list | ✅ | Own branch only | Own branch only | ✅ (read) | ❌ |
| Student name visible | ✅ | Own students only | ❌ (code only) | ❌ (code only) | ❌ |
| Profile / Sessions / Colleges tabs | ✅ | ✅ (own) | ✅ (read, own branch) | ✅ (read) | ❌ |
| Outcome tab edit | ✅ | ✅ (own branch) | ❌ | ❌ | ❌ |
| + Add Student Record button | ✅ | ✅ | ❌ | ❌ | ❌ |
| Batch Record Session button | ✅ | ✅ | ❌ | ❌ | ❌ |
| Generate Placement Report button | ✅ | ❌ | ❌ | ❌ | ❌ |
| Export CSV button | ✅ | ❌ | ❌ | ✅ | ❌ |
| KPI bar — full detail | ✅ | Own branch | Own branch | ✅ | Aggregate widget only |
| Chart panel | ✅ | Own branch | Own branch | ✅ | ❌ |
| Alert banners | ✅ | Own branch | Own branch | ✅ | ❌ |
| Placement report download | ✅ | ❌ | ❌ | ✅ | ✅ (PDF link via notification) |

---

## 11. API Endpoints

### Base URL: `/api/v1/group/{group_id}/welfare/guidance/`

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/welfare/guidance/` | List student guidance records (paginated, filtered, role-masked) | JWT + role check |
| POST | `/api/v1/group/{group_id}/welfare/guidance/` | Create new student guidance record | Counselling Head / Branch Counsellor |
| GET | `/api/v1/group/{group_id}/welfare/guidance/{record_id}/` | Retrieve full guidance profile (role-masked fields) | JWT + role check |
| PATCH | `/api/v1/group/{group_id}/welfare/guidance/{record_id}/` | Update guidance record | Counselling Head / Branch Counsellor |
| GET | `/api/v1/group/{group_id}/welfare/guidance/kpi/` | KPI summary bar data for selected filters | JWT + role check |
| GET | `/api/v1/group/{group_id}/welfare/guidance/funnel/` | Funnel stage counts for selected filters | JWT + role check |
| GET | `/api/v1/group/{group_id}/welfare/guidance/charts/` | Bar and pie chart data | JWT + role check |
| POST | `/api/v1/group/{group_id}/welfare/guidance/sessions/` | Log guidance session (single or batch) | Counselling Head / Branch Counsellor |
| POST | `/api/v1/group/{group_id}/welfare/guidance/{record_id}/colleges/` | Add target college to student record | Counselling Head / Branch Counsellor |
| DELETE | `/api/v1/group/{group_id}/welfare/guidance/{record_id}/colleges/{college_id}/` | Remove target college | Counselling Head / Branch Counsellor |
| POST | `/api/v1/group/{group_id}/welfare/guidance/{record_id}/applications/` | Add application record | Counselling Head / Branch Counsellor |
| PATCH | `/api/v1/group/{group_id}/welfare/guidance/{record_id}/applications/{app_id}/` | Update application status | Counselling Head / Branch Counsellor |
| POST | `/api/v1/group/{group_id}/welfare/guidance/{record_id}/offers/` | Record an offer | Counselling Head / Branch Counsellor |
| PATCH | `/api/v1/group/{group_id}/welfare/guidance/{record_id}/outcome/` | Record final admission outcome | Counselling Head / Branch Counsellor |
| POST | `/api/v1/group/{group_id}/welfare/guidance/report/generate/` | Async placement report generation | Counselling Head |
| GET | `/api/v1/group/{group_id}/welfare/guidance/report/{task_id}/status/` | Poll report generation status | Counselling Head |
| GET | `/api/v1/group/{group_id}/welfare/guidance/report/{task_id}/download/` | Download generated report | Counselling Head / Academic Director |
| GET | `/api/v1/group/{group_id}/welfare/guidance/export/` | Export CSV (role-gated fields) | Counselling Head / Academic Director |
| GET | `/api/v1/group/{group_id}/welfare/guidance/alerts/` | Fetch active alert conditions | JWT + role check |
| GET | `/api/v1/group/{group_id}/welfare/guidance/student-search/` | Student autocomplete (branch-scoped) | JWT + role check |

**Query parameters for list endpoint:**

| Parameter | Type | Description |
|---|---|---|
| `branch` | int[] | Filter by branch ID(s) |
| `class_level` | str[] | `class_11`, `class_12` |
| `stream` | str[] | `mpc`, `bipc`, `mec`, `cec`, `coaching` |
| `target_exam` | str[] | `jee`, `neet`, `clat`, `cuet`, `ipm`, `state`, `other` |
| `profile_completed` | bool | Filter by profile completion |
| `aptitude_done` | bool | Filter by aptitude test completion |
| `application_status` | str[] | `not_started`, `in_progress`, `submitted`, `deadline_passed` |
| `admission_status` | str[] | `pending`, `offer_received`, `confirmed`, `not_admitted` |
| `sessions_min` | int | Minimum session count |
| `sessions_max` | int | Maximum session count |
| `academic_year` | str | e.g., `2025-26` |
| `page` | int | Page number |
| `page_size` | int | Default 25, max 100 |
| `search` | str | Student code, branch, or counsellor name |
| `sort_by` | str | Column name; prefix `-` for descending |

---

## 12. HTMX Patterns

| Interaction | HTMX Attributes | Behaviour |
|---|---|---|
| Search input | `hx-get="/api/.../guidance/"` `hx-trigger="keyup changed delay:300ms"` `hx-target="#guidance-table-body"` `hx-include="#filter-form"` | Table body replaced on search |
| Advanced filter apply | `hx-get="/api/.../guidance/"` `hx-trigger="change"` `hx-target="#guidance-table-body"` `hx-include="#filter-form"` | Table + KPI + funnel refreshed |
| Pagination | `hx-get="/api/.../guidance/?page={n}"` `hx-target="#guidance-table-body"` `hx-push-url="true"` | Page swap; URL updated |
| Student profile drawer open | `hx-get="/api/.../guidance/{record_id}/"` `hx-target="#drawer-container"` `hx-trigger="click"` | Drawer slides in from right |
| Drawer tab switch | `hx-get="/api/.../guidance/{record_id}/?tab={tab_slug}"` `hx-target="#drawer-tab-content"` | Tab content swapped without full drawer reload |
| Add target college inline form | `hx-post="/api/.../guidance/{record_id}/colleges/"` `hx-target="#colleges-list"` `hx-swap="beforeend"` | New college row appended; form cleared |
| Application status update | `hx-patch="/api/.../guidance/{record_id}/applications/{app_id}/"` `hx-target="#application-row-{app_id}"` `hx-swap="outerHTML"` | Row updated in place |
| Batch session student search | `hx-get="/api/.../guidance/student-search/?q={value}&branch={id}"` `hx-trigger="keyup changed delay:300ms"` `hx-target="#student-search-dropdown"` | Student dropdown populated |
| Batch session submit | `hx-post="/api/.../guidance/sessions/"` `hx-target="#guidance-table-body"` `hx-on::after-request="closeDrawer(); fireToast();"` | Sessions logged; table refreshed; drawer closed |
| Outcome save | `hx-patch="/api/.../guidance/{record_id}/outcome/"` `hx-target="#student-row-{record_id}"` `hx-swap="outerHTML"` | Table row Status badge updated; drawer closes |
| Report generation submit | `hx-post="/api/.../guidance/report/generate/"` `hx-target="#report-modal-body"` `hx-swap="innerHTML"` | Modal body replaced with progress indicator |
| Report status polling | `hx-get="/api/.../guidance/report/{task_id}/status/"` `hx-trigger="every 3s"` `hx-target="#report-status-area"` | Polls every 3 s; stops on completion; shows download link |
| KPI bar refresh | `hx-get="/api/.../guidance/kpi/"` `hx-trigger="load, filterApplied from:body"` `hx-target="#kpi-bar"` | Refreshes on load and after filters |
| Funnel update | `hx-get="/api/.../guidance/funnel/"` `hx-trigger="load, filterApplied from:body"` `hx-target="#funnel-bar"` | Funnel segment counts updated |
| Alert banner load | `hx-get="/api/.../guidance/alerts/"` `hx-trigger="load"` `hx-target="#alert-banner"` | Conditional banner display |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
