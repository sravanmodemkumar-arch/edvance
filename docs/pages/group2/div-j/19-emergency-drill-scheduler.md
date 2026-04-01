# 19 — Emergency Drill Scheduler

> **URL:** `/group/health/drills/`
> **File:** `19-emergency-drill-scheduler.md`
> **Template:** `portal_base.html`
> **Priority:** P1
> **Role:** Group Emergency Response Officer (primary)

---

## 1. Purpose

Plan, schedule, track, and record emergency drills across all group branches. Compliance with minimum annual drill requirements is mandatory: Fire Evacuation (minimum 2 per year), Medical Emergency (minimum 1 per year), Earthquake / Natural Disaster (minimum 1 per year), and Missing Student Protocol (minimum 1 per year). Each branch must complete all four drill types per academic year to achieve full emergency preparedness compliance.

The scheduler provides two views: a monthly calendar for scheduling overview and a filterable list view for detailed tracking. A compliance matrix gives a one-glance status of every branch against every drill type. Outcome recording captures actual date and time, participant counts (students, teaching staff, non-teaching staff), evacuation completion time, issues found during the drill, and corrective actions assigned to branch principals. Drill records are used in the Compliance Report (Page 24) and link to the SOP library (Page 18).

Scale: 4 mandatory drill types × minimum 2 per year for fire × 20–50 branches = 300–400 drill events per academic year minimum.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Emergency Response Officer | G3 | Full CRUD — create, edit, record outcomes, cancel, export | Primary owner |
| Group Medical Coordinator | G3 | View all drills; record outcome for medical emergency drills | Co-participant for medical drill type |
| Branch Principal | Branch | View own branch drills + submit drill outcome via branch portal | Cannot create or cancel drills |
| CEO / COO | Group | View compliance matrix and summary statistics | No edit access |
| All other roles | — | — | No access |

> **Access enforcement:** `@require_role('emergency_response_officer', 'medical_coordinator', 'branch_principal', 'ceo', 'coo')`. Drill creation and cancellation restricted to Emergency Response Officer. Branch Principal outcome submission restricted to `drill.branch == request.user.branch`. Medical Coordinator outcome submission restricted to `drill.type == 'medical_emergency'`.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Health & Medical  ›  Emergency Drill Scheduler
```

### 3.2 Page Header
- **Title:** `Emergency Drill Scheduler`
- **Subtitle:** `[N] Drills Scheduled · [N] Completed · [N] Overdue · AY [current year]`
- **Right controls:** `+ Schedule Drill` (Emergency Response Officer) · `Calendar / List` toggle · `Compliance Matrix` toggle · `Advanced Filters` · `Export`

### 3.3 Alert Banner

| Condition | Banner Text | Severity |
|---|---|---|
| Branch has not completed a mandatory drill type this AY | "⚠ [N] branch(es) have not yet completed one or more mandatory drill types for this academic year." | Amber |
| Drill overdue by > 30 days from target date | "OVERDUE: [N] drill(s) are more than 30 days past their target date without completion." | Red |
| Corrective action from a previous drill unresolved | "[N] corrective action(s) from previous drills remain unresolved past their due date." | Amber |
| Fire drill evacuation time > 5 minutes | "⚠ Evacuation time exceeded 5-minute threshold in [N] recent fire drill(s). Review and re-train." | Amber |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule |
|---|---|---|
| Drills Scheduled This AY | Total drills created for current academic year (all branches) | Blue always |
| Drills Completed | Status = Completed (outcome recorded) | Blue; sub-label shows % of scheduled |
| Drills Overdue | Scheduled date passed + no outcome recorded | Green = 0 · Yellow 1–5 · Red > 5 |
| Branches with All 4 Types Completed | Branches with at least 1 completed drill for each of the 4 mandatory types | Blue; sub-label shows % of total branches |
| Average Evacuation Time — Fire Drills | Mean evacuation time (minutes) across all completed fire drills this AY | Green < 3 min · Yellow 3–5 min · Red > 5 min |
| Open Corrective Actions | Corrective actions from all drills with status = Open past due date | Green = 0 · Amber 1–10 · Red > 10 |

---

## 5. Sections

### 5.1 Calendar View (default)

Monthly calendar grid (Mon–Sun columns, 4–5 week rows for the displayed month).

- Navigation: Previous Month / Next Month / Today / Jump to Month (date picker).
- Each drill event appears as a colour-coded pill on its scheduled date:
  - Fire Evacuation: Red pill
  - Medical Emergency: Blue pill
  - Earthquake / Natural Disaster: Orange pill
  - Missing Student Protocol: Purple pill
  - Cancelled: Grey pill with strikethrough
- Pill shows: Branch abbreviation + Drill Type icon. Hover → tooltip with full drill name, branch, lead coordinator, status.
- Click on pill → opens `drill-detail` drawer.
- Click on empty date cell → pre-fills `drill-create` drawer with that date.
- Scroll in month view shows all branches' drills for that month.

---

### 5.2 List View (toggle from Calendar)

**Search:** Branch name or drill type. 300ms debounce.

**Advanced Filters:**

| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Drill Type | Checkbox | Fire Evacuation / Medical Emergency / Earthquake/Natural Disaster / Missing Student Protocol / Other |
| Status | Checkbox | Scheduled / In Progress / Completed / Overdue / Cancelled |
| Outcome | Radio | All / Pass / Fail / Partial / Cancelled |
| Academic Year | Single-select | Current AY + last 2 AYs |
| Month | Single-select | All months in selected AY |

**Columns:**

| Column | Sortable | Notes |
|---|---|---|
| Drill Name | ✅ | Auto-generated: "[Type] Drill — [Branch] — [Target Month]"; click → `drill-detail` drawer |
| Type | ✅ | Colour-coded badge |
| Branch | ✅ | |
| Scheduled Date | ✅ | Target date; red if past and no outcome recorded (overdue) |
| Actual Date | ✅ | Blank until outcome recorded |
| Lead Coordinator | ✅ | Name + role |
| Participants | ✅ | Count (students + staff total); shown after outcome recorded |
| Evacuation Time (mins) | ✅ | Fire drills only; blank for other types; red if > 5 min |
| Outcome | ✅ | — (not yet done) / Pass / Fail / Partial / Cancelled — badge |
| Issues Found | ✅ | Count of issues logged; amber if > 0 |
| Status | ✅ | Scheduled / Completed / Overdue / Cancelled — badge |
| Actions | ❌ | View · Edit · Mark Done · Cancel |

**Default sort:** Status (Overdue first, then Scheduled by date ascending, then Completed, then Cancelled).
**Pagination:** Server-side · 25 records per page.

---

### 5.3 Compliance Matrix (sticky panel toggle)

Displayed above the list/calendar view when toggled. Persists while user scrolls through list.

Grid layout:
- **Rows:** All branches (alphabetical, 20–50 rows)
- **Columns:** Fire Evacuation (2 req'd) · Medical Emergency (1 req'd) · Earthquake/Natural Disaster (1 req'd) · Missing Student Protocol (1 req'd)
- **Cell content:** One of:
  - Completed (green checkmark) — all required drills of this type done for this AY
  - Scheduled (yellow warning) — at least one drill of this type scheduled but not yet done
  - Not Scheduled (grey X) — no drill of this type scheduled
  - Overdue (red circle) — scheduled date passed without completion

**Cell interaction:** Click any cell → filters the list view to that specific branch + drill type combination.
**Export Compliance Matrix:** PNG or PDF snapshot button (Emergency Response Officer + CEO/COO).

---

## 6. Drawers / Modals

### 6.1 Drawer — `drill-detail` (700px, right side)

Triggered by drill name link, calendar pill click, or **View** action.

**Tabs:**

#### Tab 1 — Details

| Field | Notes |
|---|---|
| Drill Name | Auto-generated |
| Drill Type | With SOP reference (linked to SOP library Page 18) |
| Branch | |
| Scheduled Date | |
| Actual Date / Time | Blank until outcome recorded |
| Lead Coordinator | Name + role |
| Pre-Drill Briefing Date | Date of briefing to staff before the drill |
| Weather Conditions | (Relevant for outdoor / fire / earthquake drills) |
| Assembly Point Used | Named assembly area (from campus map reference) |
| Total Campus Population at Time | Students present + all staff at time of drill |
| Expected Participant Count | Planned before drill |
| Notes | Pre-drill notes |

#### Tab 2 — Attendance

| Field | Notes |
|---|---|
| Students Participated | Count |
| Teaching Staff Participated | Count |
| Non-Teaching Staff Participated | Count |
| Bus Drivers / Transport Staff | Count |
| Hostel Wardens | Count (if hostel involved) |
| Total Participants | Auto-calculated |
| Coverage % | Total participants / Total campus population × 100 |
| Evacuation Completion Time | Time from start signal to all-clear at assembly point (minutes and seconds) |

#### Tab 3 — Issues & Actions

Table of all issues identified during the drill:

| Column | Notes |
|---|---|
| Issue # | Sequential |
| Issue Description | e.g., "Emergency exit on 2nd floor blocked by furniture", "Roll call took > 8 minutes" |
| Priority | High / Medium / Low badge |
| Corrective Action | What must be done to address it |
| Assigned To | Branch Principal name |
| Due Date | Deadline for resolution |
| Resolved | Yes / No toggle |
| Resolved Date | Date marked resolved |

Add Issue button (+ row). Emergency Response Officer and Branch Principal (own branch) can mark items resolved.

#### Tab 4 — Report

Auto-generated drill summary in regulatory format. Includes:
- Drill header information (branch, type, date, lead coordinator)
- Participant statistics
- Evacuation time result vs threshold
- Issues summary (count + priority breakdown)
- Corrective actions list
- Sign-off fields: Conducted by, Witnessed by, Principal acknowledgement

Actions: **Download Drill Report (PDF)** · **Send Report to Branch Principal**

---

### 6.2 Drawer — `drill-create` (660px, right side)

Triggered by **+ Schedule Drill** or click on calendar empty date.

| Field | Type | Validation |
|---|---|---|
| Drill Type | Single-select: Fire Evacuation / Medical Emergency / Earthquake/Natural Disaster / Missing Student Protocol / Other | Required |
| Branch(es) | Multi-select (can schedule same type across multiple branches in one operation) | Required; at least 1 |
| Target Date | Date picker | Required; must be future date; auto-filled if triggered from calendar cell |
| Lead Coordinator | Text input with autocomplete from staff registry | Required |
| SOP Reference | Single-select (auto-filters SOPs by type from SOP library) | Required |
| Pre-Drill Briefing Date | Date picker | Required; must be ≤ Target Date |
| Expected Participants | Number input | Required |
| Assembly Point | Text input | Required for Fire / Earthquake types |
| Notes / Special Instructions | Textarea (max 500 chars) | Optional |
| Notify Branch Principal | Checkbox (default checked) | Sends notification via portal + WhatsApp |

**Batch create note:** If multiple branches selected, one drill record is created per branch with all the same field values. Each drill record can then be independently managed.

**Footer:** `Cancel` · `Schedule Drill`

---

### 6.3 Drawer — `drill-outcome` (640px, right side)

Triggered by **Mark Done** action. Also accessible via Branch Principal portal (own branch only).

| Field | Type | Validation |
|---|---|---|
| Drill Reference | Read-only | |
| Actual Date | Date picker | Required; cannot be future date |
| Actual Start Time | Time picker | Required |
| Actual End Time | Time picker | Required; > Start Time |
| Students Participated | Number input | Required |
| Teaching Staff Participated | Number input | Required |
| Non-Teaching Staff Participated | Number input | Required |
| Total Campus Population at Time | Number input | Required |
| Evacuation Completion Time (mins) | Decimal number input | Required for Fire and Earthquake types; optional for others |
| Assembly Point Used | Text input | Required |
| Weather Conditions | Text input | Optional |
| Outcome | Radio: Pass / Fail / Partial | Required |
| Outcome Notes | Textarea (max 500 chars) | Required if Outcome = Fail or Partial |
| Issues Found | Add-row table: Issue Description + Priority + Corrective Action + Assigned To + Due Date | Optional; recommended if Outcome ≠ Pass |
| Attach Drill Report PDF | File upload | Optional |

**Validation:** If evacuation time > 5 minutes for fire drills, warning shown: "Evacuation time exceeds 5-minute threshold. An issue should be logged and a corrective action assigned." If outcome = Pass but issues exist, confirmation prompt shown.

**Footer:** `Cancel` · `Record Outcome`

---

### 6.4 Modal — `cancel-drill` (420px, centred)

Triggered by **Cancel** action in table or drill-detail drawer.

| Field | Type | Validation |
|---|---|---|
| Drill Reference | Read-only | |
| Reason for Cancellation | Textarea (max 300 chars) | Required |
| Reschedule Date | Date picker | Required; must be future date; cannot be the same as original date |
| Notes | Textarea (max 200 chars) | Optional |

**Footer:** `Cancel` · `Confirm Cancellation & Reschedule`

On confirm: original drill marked Cancelled; new drill record auto-created with Reschedule Date as Target Date, same type/branch/coordinator/SOP reference. Toast shown for both actions.

---

## 7. Toast Messages

| Action | Toast Text | Type |
|---|---|---|
| Drill scheduled (single branch) | "Drill scheduled for [Branch] on [Date]. Branch Principal notified." | Success |
| Drill scheduled (multiple branches) | "Drills scheduled for [N] branches. Principals notified." | Success |
| Outcome recorded — pass | "Drill outcome recorded. [Branch] passed [Type] drill on [Date]." | Success |
| Outcome recorded — fail/partial | "Drill outcome recorded with issues. [N] corrective action(s) assigned to [Branch] Principal." | Warning |
| Drill cancelled and rescheduled | "Drill cancelled. New drill scheduled for [Reschedule Date]." | Info |
| Corrective action resolved | "Corrective action marked as resolved." | Success |
| Evacuation time warning | "Evacuation time exceeds threshold. Issue logged automatically." | Warning |
| Export initiated | "Compliance report export initiated. Download will be ready shortly." | Info |
| Drill create failed | "Please complete all required fields before scheduling." | Error |

---

## 8. Empty States

| Context | Heading | Sub-text | Action |
|---|---|---|---|
| No drills scheduled this AY | "No drills scheduled yet." | "Schedule the first emergency drill to begin the compliance calendar." | `+ Schedule Drill` |
| No drills match filters | "No drills match your current filters." | "Try adjusting the branch, type, or status filters." | `Clear Filters` |
| Calendar view — empty month | "No drills scheduled in [Month Year]." | "Click on any date to schedule a drill." | — |
| Issues & Actions tab — no issues | "No issues found during this drill." | "Issues identified during future drills will appear here." | — |
| Compliance matrix — all complete | "All branches have completed all mandatory drill types for this AY." | "Full emergency drill compliance achieved." | — |

---

## 9. Loader States

| Context | Loader Behaviour |
|---|---|
| Initial page load | Full skeleton: 6 KPI cards + compliance matrix + calendar/list area |
| Calendar month switch | Calendar grid overlay spinner; pill events reload |
| List view filter apply | Table body inline spinner |
| Compliance matrix load | Matrix skeleton: grey grid of 50 rows × 4 columns |
| Drill detail drawer open | Drawer skeleton: tab bar + content blocks |
| Attendance tab load | Form-like skeleton (6 grey input rows) |
| Issues & Actions tab load | Table skeleton (3 grey rows) |
| Report tab generate | Spinner + "Generating report…" message |
| Drill create / outcome submit | Submit button spinner; all fields disabled |
| Cancel modal submit | Modal footer spinner |

---

## 10. Role-Based UI Visibility

| UI Element | Emergency Response Officer | Medical Coordinator | Branch Principal | CEO / COO |
|---|---|---|---|---|
| Full drill list (all branches) | ✅ | ✅ | Own branch only | ✅ |
| + Schedule Drill button | ✅ | ❌ | ❌ | ❌ |
| Edit drill | ✅ | ❌ | ❌ | ❌ |
| Cancel drill | ✅ | ❌ | ❌ | ❌ |
| Mark Done / Record Outcome | ✅ | Medical drills only | Own branch (via branch portal) | ❌ |
| Add / resolve issues | ✅ | Medical drills | Own branch issues | ❌ |
| Compliance matrix | ✅ | ✅ | ❌ (own row only) | ✅ |
| Export compliance matrix | ✅ | ❌ | ❌ | ✅ |
| Download drill report PDF | ✅ | ✅ | Own branch | ✅ |
| KPI bar — all 6 cards | ✅ | ✅ | ❌ | ✅ |
| Alert banners | ✅ | ✅ | Own branch alerts | ✅ |
| Calendar view | ✅ | ✅ | Own branch | ✅ |
| SOP reference link | ✅ | ✅ | ✅ (read-only SOP) | ✅ |

---

## 11. API Endpoints

### Base URL: `/api/v1/group/{group_id}/health/drills/`

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/health/drills/` | List all drills (paginated, filtered, branch-scoped by role) | JWT + role check |
| POST | `/api/v1/group/{group_id}/health/drills/` | Schedule new drill(s) | Emergency Response Officer |
| GET | `/api/v1/group/{group_id}/health/drills/{drill_id}/` | Retrieve drill detail | JWT + role check |
| PATCH | `/api/v1/group/{group_id}/health/drills/{drill_id}/` | Update drill details | Emergency Response Officer |
| GET | `/api/v1/group/{group_id}/health/drills/kpi/` | KPI summary bar data | JWT + role check |
| GET | `/api/v1/group/{group_id}/health/drills/alerts/` | Active alert conditions | JWT + role check |
| GET | `/api/v1/group/{group_id}/health/drills/calendar/` | Calendar data (monthly drill events) | JWT + role check |
| GET | `/api/v1/group/{group_id}/health/drills/compliance-matrix/` | Compliance matrix data (branch × type grid) | JWT + role check |
| POST | `/api/v1/group/{group_id}/health/drills/{drill_id}/outcome/` | Record drill outcome | Emergency Response Officer / Medical Coordinator / Branch Principal |
| POST | `/api/v1/group/{group_id}/health/drills/{drill_id}/cancel/` | Cancel drill and create rescheduled drill | Emergency Response Officer |
| GET | `/api/v1/group/{group_id}/health/drills/{drill_id}/issues/` | List issues for a drill | JWT + role check |
| POST | `/api/v1/group/{group_id}/health/drills/{drill_id}/issues/` | Add issue to drill record | Emergency Response Officer / Branch Principal |
| PATCH | `/api/v1/group/{group_id}/health/drills/{drill_id}/issues/{issue_id}/` | Update issue (resolve) | Emergency Response Officer / Branch Principal |
| GET | `/api/v1/group/{group_id}/health/drills/{drill_id}/report/` | Generate drill report (PDF or JSON) | JWT + role check |
| POST | `/api/v1/group/{group_id}/health/drills/{drill_id}/report/send/` | Send report to branch principal | Emergency Response Officer |
| GET | `/api/v1/group/{group_id}/health/drills/export/` | Export drill list and compliance data | Emergency Response Officer / CEO / COO |

**Query parameters for list endpoint:**

| Parameter | Type | Description |
|---|---|---|
| `search` | str | Branch name or drill type |
| `branch` | int[] | Branch filter |
| `type` | str[] | `fire`, `medical`, `earthquake`, `missing_student`, `other` |
| `status` | str[] | `scheduled`, `completed`, `overdue`, `cancelled` |
| `outcome` | str | `pass`, `fail`, `partial`, `cancelled` |
| `ay` | str | Academic year (e.g., `2025-26`) |
| `month` | int | Calendar month (1–12) |
| `page` | int | Page number |
| `page_size` | int | Default 25; max 100 |
| `calendar` | bool | `true` → returns event objects for calendar rendering |

**Query parameters for compliance-matrix endpoint:**

| Parameter | Type | Description |
|---|---|---|
| `ay` | str | Academic year |
| `branch` | int[] | Optional branch filter |

---

## 12. HTMX Patterns

| Interaction | HTMX Attributes | Behaviour |
|---|---|---|
| Calendar / list view toggle | `hx-get="/api/.../drills/?view={calendar|list}"` `hx-target="#drills-view-container"` `hx-trigger="click"` | Entire view container swapped |
| Calendar month navigate | `hx-get="/api/.../drills/calendar/?month={M}&year={Y}"` `hx-target="#calendar-grid"` `hx-trigger="click"` `hx-indicator="#calendar-spinner"` | Calendar grid replaced |
| Compliance matrix toggle | `hx-get="/api/.../drills/compliance-matrix/"` `hx-target="#compliance-matrix-panel"` `hx-trigger="click"` `hx-swap="innerHTML"` | Matrix panel shown/hidden |
| Compliance matrix cell click filter | `hx-get="/api/.../drills/?branch={b_id}&type={type}"` `hx-target="#drills-table-body"` `hx-trigger="click"` `hx-push-url="true"` | List filtered to that branch + type |
| Search debounce | `hx-get="/api/.../drills/"` `hx-trigger="keyup changed delay:300ms"` `hx-target="#drills-table-body"` `hx-include="#filter-form"` | Table rows replaced |
| Filter apply | `hx-get="/api/.../drills/"` `hx-trigger="change"` `hx-target="#drills-table-body"` `hx-include="#filter-form"` | Table rows replaced; KPI bar refreshed |
| KPI bar load | `hx-get="/api/.../drills/kpi/"` `hx-trigger="load"` `hx-target="#kpi-bar"` | On page load |
| Alert banner load | `hx-get="/api/.../drills/alerts/"` `hx-trigger="load"` `hx-target="#alert-banner"` | On page load |
| Pagination | `hx-get="/api/.../drills/?page={n}"` `hx-target="#drills-table-body"` `hx-push-url="true"` | Page swap |
| Drill detail drawer open | `hx-get="/api/.../drills/{drill_id}/"` `hx-target="#drawer-container"` `hx-trigger="click"` | Drawer slides in; Details tab default |
| Drawer tab switch | `hx-get="/api/.../drills/{drill_id}/?tab={tab_slug}"` `hx-target="#drawer-tab-content"` `hx-trigger="click"` | Lazy load on first click |
| Issues tab load | `hx-get="/api/.../drills/{drill_id}/issues/"` `hx-target="#issues-content"` `hx-trigger="click[tab='issues'] once"` | Loaded once |
| Report tab generate | `hx-get="/api/.../drills/{drill_id}/report/"` `hx-target="#report-content"` `hx-trigger="click[tab='report'] once"` `hx-indicator="#report-spinner"` | Generated on first click |
| Drill create submit | `hx-post="/api/.../drills/"` `hx-target="#drills-table-body"` `hx-on::after-request="closeDrawer(); fireToast(); refreshCalendar();"` | New row(s) prepended; calendar refreshed |
| Outcome submit | `hx-post="/api/.../drills/{drill_id}/outcome/"` `hx-target="#drill-row-{drill_id}"` `hx-swap="outerHTML"` `hx-on::after-request="fireToast(); refreshKPI();"` | Row status + outcome badge updated; KPI refreshed |
| Cancel modal submit | `hx-post="/api/.../drills/{drill_id}/cancel/"` `hx-target="#drills-table-body"` `hx-on::after-request="closeModal(); fireToast();"` | Original row updated; new rescheduled row inserted |
| Issue resolve toggle | `hx-patch="/api/.../drills/{drill_id}/issues/{issue_id}/"` `hx-target="#issue-row-{issue_id}"` `hx-swap="outerHTML"` | Issue row resolved status toggled |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
