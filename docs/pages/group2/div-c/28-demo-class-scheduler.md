# 28 — Demo Class Scheduler

**URL:** `/group/adm/demo/scheduler/`
**Template:** `portal_base.html` (light theme)
**Division:** C — Group Admissions
**Module:** Demo Classes

---

## 1. Purpose

The Demo Class Scheduler is the central planning hub for all demo and trial classes organized by the group across its branch network. Demo classes represent the single most powerful admissions conversion tool available to a competitive coaching group — a prospective student who attends a well-run, engaging demo session is statistically far more likely to submit an application than one who merely receives a brochure or marketing call. This page enables the Group Demo Coordinator to plan, schedule, and supervise all demo activity across branches during the admission season, ensuring no branch is left without active demo programming at peak inquiry periods.

The scheduler coordinates three distinct dimensions of demo management simultaneously: calendar coverage (ensuring demos are spread across branches and dates to maximize reach), teacher assignment (matching the best available faculty to each session based on subject and availability), and registration tracking (monitoring prospect sign-ups and confirmations per session). The page surfaces branch-level gaps in real time — if a branch in an active admission zone has not had a demo in the past 30 days, the system flags it as a coverage risk and prompts the coordinator to schedule one.

Beyond scheduling logistics, the page feeds data downstream into the conversion funnel. Every session created here becomes a trackable unit whose attendance, feedback, and conversion metrics are measured on related pages. The Admissions Director uses the Branch Demo Coverage panel to evaluate whether branch-level demo investment is yielding enrollment returns, and uses the overall demo volume as a leading indicator of application intake for the coming month. A complete, well-maintained demo schedule is therefore a prerequisite for accurate admissions forecasting at the group level.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Demo Class Coordinator (29) | G3 | Full — create, edit, cancel, reassign teachers, bulk actions | Primary owner of this page |
| Group Admission Coordinator (24) | G3 | View all + create demos; cannot cancel or bulk-override | Operational support role |
| Group Admissions Director (23) | G3 | View all + override cancellations; approve high-capacity demos | Strategic oversight |
| Branch Academic Head | Branch | Read-only scoped to own branch demos | Cannot see other branches |
| Group Scholarship Exam Manager (Role 26) | G3 | Read — Section 5.1 (Demo Schedule) and Section 5.2 (Calendar) only | Relevant for joint demo-scholarship events coordination |

Access enforcement: All views are protected with `@login_required` and `@role_required(['demo_coordinator', 'admission_coordinator', 'admissions_director', 'branch_academic_head', 'scholarship_exam_manager'])` Django view decorators. Branch Academic Head scope is enforced via `request.user.branch_id` queryset filter applied in the view before any data is returned to the template.

---

## 3. Page Layout

### 3.1 Breadcrumb
`Group Portal → Admissions → Demo Classes → Scheduler`

### 3.2 Page Header
**Title:** Demo Class Scheduler
**Subtitle:** Plan and manage demo sessions across all branches
**Actions (right-aligned):**
- `[+ Schedule New Demo]` — primary button, opens `demo-create-form` drawer
- `[Export Schedule CSV]` — secondary button

### 3.3 Alert Banner

Displayed conditionally above KPI bar. Triggers:

| Condition | Banner Type | Message |
|---|---|---|
| 1 or more branches with no demo in 30+ days during active admission season | Warning (amber) | "3 branches have no demo scheduled in the past 30 days. Review Branch Demo Coverage below." |
| Demo session starts in < 2 hours with no teacher confirmed | Error (red) | "Demo ID DM-0482 at Kukatpally begins in 90 minutes — teacher not yet confirmed." |
| 10+ demos in "Registration Open" with 0 registrations | Info (blue) | "10 open demos have zero registrations. Consider sending batch outreach." |
| Bulk action succeeded | Success (green) | "Registration opened for 6 selected demos." |

---

## 4. KPI Summary Bar

| Card | Metric | Source | Colour Rule | Drill-down |
|---|---|---|---|---|
| Demos Planned | COUNT demos this admission month (all statuses except Cancelled) | `demo_sessions` WHERE month = current | Blue always | Filters table to current month |
| Demos Completed | COUNT demos WHERE status = Completed this month | `demo_sessions` | Green if ≥ target; amber if 70–99%; red if < 70% | Filters table to Completed |
| Demos Cancelled | COUNT demos WHERE status = Cancelled this month | `demo_sessions` | Amber if > 5%; red if > 10% of planned | Filters table to Cancelled |
| Branches with No Demo | COUNT distinct branches in admission season with no demo last 30 days | `branches` LEFT JOIN `demo_sessions` | Red if > 0; green if 0 | Scrolls to Section 5.5 |
| Avg Prospects per Demo | AVG registered prospects per completed demo this month | `demo_registrations` GROUP BY session | Green if ≥ 15; amber if 8–14; red if < 8 | No drill-down (aggregate only) |
| Total Unique Prospects | COUNT DISTINCT prospect_id attending demos this month | `demo_attendance` | Blue always | Links to attendance page |

**HTMX auto-refresh pattern (every 5 minutes):**
```html
<div id="kpi-bar"
     hx-get="/group/adm/demo/scheduler/kpis/"
     hx-trigger="load, every 300s"
     hx-target="#kpi-bar"
     hx-swap="outerHTML">
  <!-- KPI cards rendered here -->
</div>
```

---

## 5. Sections

### 5.1 Demo Schedule Table

**Display:** Full-width sortable, selectable, server-side paginated table (20 rows/page). Default sort: Date ascending (upcoming first).

**Columns:**

| Column | Notes |
|---|---|
| Demo ID | Auto-generated, e.g. DM-0482 |
| Date & Time | Date + start time, timezone-aware |
| Branch | Branch name |
| Subject / Stream Demo | e.g. "Physics – JEE" or "Biology – NEET" |
| Mode | In-person / Online / Hybrid |
| Demo Teacher | Assigned teacher name |
| Duration | Minutes |
| Registered | Count of registrations |
| Confirmed | Count of confirmed attendees |
| Status | Planned / Registration Open / In Progress / Completed / Cancelled (colour-coded badge) |
| Actions | `[Edit →]` `[Manage →]` `[Cancel]` — Cancel hidden if status = Completed |

**Filters (filter bar above table):**
- Branch (multi-select dropdown)
- Mode (In-person / Online / Hybrid / All)
- Status (multi-select)
- Date range (from / to date pickers)
- Subject (text search)

**Bulk actions (appear when rows selected):**
- `[Open Registration for Selected]` — sets status to "Registration Open", sends registration link
- `[Send Reminders to All Registered]` — triggers WhatsApp/SMS to all registered prospects for selected demos

**HTMX:** Filter bar uses `hx-get="/group/adm/demo/scheduler/table/"` with `hx-trigger="change"` on each filter input, targeting `#demo-schedule-table` with `hx-swap="innerHTML"`. Pagination uses `hx-get` with `?page=N` param, `hx-target="#demo-schedule-table"`, `hx-push-url="true"`.

**Empty state:** "No demos scheduled for the selected filters. Use [+ Schedule New Demo] to add the first session."

---

### 5.2 Demo Calendar

**Display:** Month-view calendar grid. Each day cell shows demo event chips colour-coded by branch. Up to 3 chips visible per cell; overflow shown as "+N more".

**Branch colour coding:** Each branch assigned a consistent hue (stored in branch settings); legend shown above calendar.

**Interactions:**
- Click event chip → opens inline quick-view panel (HTMX `hx-get="/group/adm/demo/scheduler/calendar/event/{id}/"`, target: `#calendar-quick-view`, swap: `innerHTML`)
- Branch filter dropdown (top right of calendar) — `hx-get` with branch param reloads calendar month
- Month navigation prev/next arrows — `hx-get="/group/adm/demo/scheduler/calendar/?month=YYYY-MM"`, target: `#demo-calendar-grid`, swap: `outerHTML`

**Empty state:** "No demos scheduled this month. [+ Schedule Demo →]"

---

### 5.3 Branch Demo Coverage

**Display:** Table showing all active branches with their demo activity for the current admission month.

**Columns:**

| Column | Notes |
|---|---|
| Branch | Branch name |
| Demos Planned This Month | COUNT planned + registration open + in-progress + completed |
| Demos Completed | COUNT status = Completed |
| Registrations | SUM registrations across all demos |
| Conversions to Application | COUNT prospects who attended demo AND submitted application |
| Action | `[Schedule Demo for Branch →]` CTA button — shown if demos_planned = 0 (opens create drawer pre-filled with that branch) |

**HTMX:** Table loaded on page load. Refresh button reloads via `hx-get="/group/adm/demo/scheduler/branch-coverage/"`.

**Empty state:** Not applicable (all branches always shown).

---

### 5.4 Teacher Assignment Table

**Display:** Table of all demo teacher assignments for the current month.

**Columns:**

| Column | Notes |
|---|---|
| Branch | Branch name |
| Subject | Subject/stream for the demo |
| Demo Date | Scheduled date |
| Teacher Assigned | Name of assigned teacher |
| Availability Confirmed | Yes / No / Pending (badge) |
| Action | `[Reassign →]` — opens teacher-reassign-modal |

**Filters:** Branch, Subject, Availability status (Confirmed / Unconfirmed / All)

**HTMX:** `hx-get="/group/adm/demo/scheduler/teacher-assignments/"` on filter change, target: `#teacher-assignment-table`.

**Empty state:** "No teacher assignments found. Assign teachers when scheduling demos."

---

### 5.5 Branches with No Demo Alert

**Display:** Alert-style list panel with red left border. Lists all branches that are in an active admission season window AND have had no demo scheduled in the past 30 days.

**Each entry shows:** Branch name | City | Last demo date (or "Never") | Admission season status | `[Schedule Demo →]` button (opens create drawer pre-filled with branch)

**HTMX:** Loaded via `hx-get="/group/adm/demo/scheduler/no-demo-alert/"` on page load, target: `#no-demo-alert-panel`.

**Empty state (positive):** Green banner — "All active admission-season branches have demos scheduled. Good coverage."

---

## 6. Drawers & Modals

### 6.1 `demo-create-form` Drawer
**Width:** 640px
**Trigger:** `[+ Schedule New Demo]` button or `[Schedule Demo for Branch →]` CTA. `[Edit →]` table action opens the same `demo-create-form` drawer (6.1) pre-populated with the existing demo's data via `hx-get=".../demo/scheduler/exam-form/{id}/"`.
**HTMX endpoint:** `hx-get="/group/adm/demo/scheduler/create/"` on open; `hx-post="/group/adm/demo/scheduler/create/"` on submit
**Tabs:**
1. **Basic Info** — Demo title, Subject, Stream (MPC/BiPC/MEC/CEC), Demo type (Trial / Full Demo / Webinar)
2. **Schedule** — Date, Start time, Duration (minutes), Recurring? (toggle — weekly for N weeks)
3. **Branch & Venue** — Branch (dropdown), Venue (room/hall/online platform), Capacity (max attendees)
4. **Teacher Assignment** — Teacher search (autocomplete from staff directory), role: Lead / Co-presenter
5. **Registration Settings** — Registration link auto-generate toggle, registration deadline, max registrations, allow walk-ins toggle
6. **Notifications** — WhatsApp reminder schedule (24h before / 2h before), send confirmation on registration toggle

---

### 6.2 `demo-manage-drawer` Drawer
**Width:** 560px
**Trigger:** `[Manage →]` action in table
**HTMX endpoint:** `hx-get="/group/adm/demo/scheduler/manage/{id}/"` lazy-loaded on open
**Content:**
- Attendance count (live) with `[Go to Attendance →]` link
- Conversion count from this demo
- Session notes (editable textarea, auto-save via `hx-post` `hx-trigger="blur"`)
- Status update control (dropdown + `[Update Status]`)
- Registered prospects list (name, phone, confirmation status)

---

### 6.3 `teacher-reassign-modal` Modal
**Width:** 400px
**Trigger:** `[Reassign →]` in Teacher Assignment Table
**HTMX endpoint:** `hx-get="/group/adm/demo/scheduler/teacher-reassign/{assignment_id}/"` lazy-loaded
**Content:**
- Current teacher display
- New teacher search (autocomplete)
- Reason for reassignment (dropdown: Unavailable / Better fit / Teacher request / Other)
- Notify teacher? (Yes/No toggle)
- `[Confirm Reassignment]` button — `hx-post`

---

### 6.4 Modal: `cancel-demo-confirm`
- **Width:** 400px
- **Trigger:** `[Cancel]` action in Section 5.1 table
- **Content:** "Cancel demo '[Demo Name]' at [Branch] on [Date]? All [N] registered attendees will be notified."
- **Fields:**
  - Cancellation reason (select dropdown, required): Venue unavailable / Teacher absent / Low registrations / Rescheduled / Other
  - Notify registered attendees via WhatsApp (checkbox, default checked)
  - Notes (textarea, optional)
- **Buttons:** `[Confirm Cancellation]` (danger red) + `[Keep Demo]`
- **On confirm:** `hx-delete="/api/v1/group/{group_id}/adm/demo/scheduler/exams/{demo_id}/"` → `hx-target="#demo-schedule-table"` `hx-swap="innerHTML"` → toast "Demo cancelled. [N] attendees notified."
- **HTMX:** `hx-get="/api/v1/group/{group_id}/adm/demo/scheduler/exams/{demo_id}/cancel-form/"` `hx-target="#modal-body"` `hx-swap="innerHTML"`

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Demo created successfully | "Demo DM-XXXX scheduled for [Branch] on [Date]." | Success | 4s |
| Demo updated | "Demo details updated." | Success | 3s |
| Demo cancelled | "Demo DM-XXXX cancelled. Registered prospects will be notified." | Warning | 5s |
| Registration opened (bulk) | "Registration opened for N demos." | Success | 4s |
| Reminders sent (bulk) | "Reminder messages queued for N registered prospects." | Success | 4s |
| Teacher reassigned | "Teacher updated for [Demo ID]. Previous teacher notified." | Success | 4s |
| Create failed (validation) | "Please complete all required fields in the Schedule tab." | Error | 6s |
| Teacher availability conflict | "Teacher [Name] has another assignment on this date. Confirm override?" | Warning | 8s (with action button) |

---

## 8. Empty States

| Condition | Illustration | Heading | Description | CTA |
|---|---|---|---|---|
| No demos at all (fresh setup) | Calendar with plus icon | "No demos scheduled yet" | "Start the admission season by scheduling the first demo class for your branches." | `[Schedule First Demo →]` |
| No demos matching active filters | Filtered list icon | "No demos match your filters" | "Try adjusting the branch, status, or date range filters." | `[Clear Filters]` |
| Demo calendar — empty month | Empty calendar grid | "No demos this month" | "Switch months or schedule a new session." | `[+ Schedule Demo]` |
| Teacher assignment — no assignments | Empty clipboard | "No teacher assignments" | "Teachers will appear here once demos are created with assigned faculty." | `[Schedule Demo →]` |
| Branch coverage — no active branches | Branch icon | "No active admission-season branches configured" | "Contact the system admin to configure branch admission windows." | None |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load (KPI bar) | Skeleton cards (6 cards, grey shimmer) |
| Demo schedule table loading | Skeleton rows (5 rows, column-width placeholders) |
| Calendar loading / month change | Full calendar grid skeleton (grey cell shimmer) |
| Branch coverage table loading | Skeleton rows (3 rows) |
| Teacher assignment table loading | Skeleton rows (3 rows) |
| Drawer opening (any) | Spinner centred in drawer body until HTMX response |
| Bulk action in progress | Button disabled + inline spinner + "Processing…" label |
| KPI auto-refresh (every 5m) | Subtle pulse animation on KPI cards (no full skeleton re-render) |
| Filter change (table reload) | Table body replaced with 3 skeleton rows during HTMX fetch |

---

## 10. Role-Based UI Visibility

All UI visibility decisions made server-side in Django template. No client-side JS role checks.

| UI Element | Demo Coordinator (29) | Admission Coordinator (24) | Admissions Director (23) | Branch Academic Head | SchExam Mgr (26) |
|---|---|---|---|---|---|
| `[+ Schedule New Demo]` button | Visible | Visible | Visible | Hidden | Hidden |
| `[Cancel]` action in table | Visible | Hidden | Visible (override) | Hidden | Hidden |
| `[Edit →]` action in table | Visible | Visible | Visible | Hidden | Hidden |
| Bulk action bar | Visible | Hidden | Visible | Hidden | Hidden |
| `[Reassign →]` teacher button | Visible | Hidden | Visible | Hidden | Hidden |
| `[Export Schedule CSV]` | Visible | Visible | Visible | Visible (branch-scoped) | Hidden |
| Branch Demo Coverage — all branches | Visible | Visible | Visible | Own branch only | Hidden |
| Branches with No Demo Alert | Visible | Visible | Visible | Own branch only | Hidden |
| Demo Calendar — all branches | Visible | Visible | Visible | Own branch only | R (read-only) |
| Demo Schedule Table (5.1) | Visible | Visible | Visible | Own branch only | R (read-only, no actions) |
| Teacher Assignment (5.6) | Visible | Visible | Visible | Hidden | Hidden |
| Follow-up Queue (5.7) | Visible | Visible | Visible | Hidden | Hidden |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/adm/demo/sessions/` | JWT G3+ | List all demo sessions with filters |
| POST | `/api/v1/group/{group_id}/adm/demo/sessions/` | JWT G3 write | Create a new demo session |
| GET | `/api/v1/group/{group_id}/adm/demo/sessions/{id}/` | JWT G3+ | Get single demo session detail |
| PATCH | `/api/v1/group/{group_id}/adm/demo/sessions/{id}/` | JWT G3 write | Update demo session fields |
| DELETE | `/api/v1/group/{group_id}/adm/demo/sessions/{id}/` | JWT G3 write | Cancel demo session |
| GET | `/api/v1/group/{group_id}/adm/demo/kpis/` | JWT G3+ | Fetch KPI bar metrics |
| GET | `/api/v1/group/{group_id}/adm/demo/calendar/` | JWT G3+ | Fetch demo events for calendar month |
| GET | `/api/v1/group/{group_id}/adm/demo/branch-coverage/` | JWT G3+ | Branch-level demo coverage summary |
| GET | `/api/v1/group/{group_id}/adm/demo/teacher-assignments/` | JWT G3+ | List all teacher assignments |
| PATCH | `/api/v1/group/{group_id}/adm/demo/teacher-assignments/{id}/` | JWT G3 write | Reassign teacher |
| GET | `/api/v1/group/{group_id}/adm/demo/no-demo-branches/` | JWT G3+ | Branches with no demo in 30 days |
| POST | `/api/v1/group/{group_id}/adm/demo/sessions/bulk-open-registration/` | JWT G3 write | Open registration for multiple sessions |
| POST | `/api/v1/group/{group_id}/adm/demo/sessions/bulk-remind/` | JWT G3 write | Send reminders for selected sessions |
| POST | `/api/v1/group/{group_id}/adm/demo/scheduler/sessions/{id}/notes/` | JWT G3 | Auto-save session notes from manage drawer |
| GET | `/api/v1/group/{group_id}/adm/demo/scheduler/exams/{demo_id}/cancel-form/` | JWT G3 | Load cancel demo confirmation form |
| DELETE | `/api/v1/group/{group_id}/adm/demo/scheduler/exams/{demo_id}/` | JWT G3 | Cancel a scheduled demo and optionally notify attendees |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| KPI bar auto-refresh | `load, every 300s` | GET `/group/adm/demo/scheduler/kpis/` | `#kpi-bar` | `outerHTML` |
| Filter change → reload table | `change` on any filter input | GET `/group/adm/demo/scheduler/table/` | `#demo-schedule-table` | `innerHTML` |
| Table pagination | `click` on page link | GET `/group/adm/demo/scheduler/table/?page=N` | `#demo-schedule-table` | `innerHTML` |
| Calendar month navigation | `click` on prev/next arrow | GET `/group/adm/demo/scheduler/calendar/?month=YYYY-MM` | `#demo-calendar-grid` | `outerHTML` |
| Calendar branch filter change | `change` | GET `/group/adm/demo/scheduler/calendar/` | `#demo-calendar-grid` | `outerHTML` |
| Calendar event chip click | `click` | GET `/group/adm/demo/scheduler/calendar/event/{id}/` | `#calendar-quick-view` | `innerHTML` |
| Open create drawer | `click` on `[+ Schedule New Demo]` | GET `/group/adm/demo/scheduler/create/` | `#drawer-container` | `innerHTML` |
| Submit create form | `submit` | POST `/group/adm/demo/scheduler/create/` | `#demo-schedule-table` | `innerHTML` |
| Open manage drawer | `click` on `[Manage →]` | GET `/group/adm/demo/scheduler/manage/{id}/` | `#drawer-container` | `innerHTML` |
| Open reassign modal | `click` on `[Reassign →]` | GET `/group/adm/demo/scheduler/teacher-reassign/{id}/` | `#modal-container` | `innerHTML` |
| Submit reassign | `click` on `[Confirm Reassignment]` | POST `/group/adm/demo/scheduler/teacher-reassign/{id}/` | `#teacher-assignment-table` | `innerHTML` |
| Session notes auto-save | `blur` on notes textarea | POST `/group/adm/demo/scheduler/manage/{id}/notes/` | `#notes-save-indicator` | `innerHTML` |
| Bulk open registration | `click` on bulk action button | POST `/group/adm/demo/scheduler/bulk-open-registration/` | `#demo-schedule-table` | `innerHTML` |
| Branch coverage refresh | `click` on refresh icon | GET `/group/adm/demo/scheduler/branch-coverage/` | `#branch-coverage-table` | `innerHTML` |
| No-demo alert panel load | `load` | GET `/group/adm/demo/scheduler/no-demo-alert/` | `#no-demo-alert-panel` | `innerHTML` |
| Edit demo (open create form pre-filled) | `click from:.btn-edit-demo` | GET `.../demo/scheduler/exam-form/{id}/` | `#drawer-container` | `innerHTML` |
| Auto-save session notes | `blur from:#session-notes-field` | POST `.../demo/scheduler/sessions/{id}/notes/` | `#notes-status` | `innerHTML` |
| Open cancel demo modal | `click from:.btn-cancel-demo` | GET `.../demo/scheduler/exams/{id}/cancel-form/` | `#modal-body` | `innerHTML` |
| Confirm demo cancellation | `click from:#btn-confirm-cancel` | DELETE `.../demo/scheduler/exams/{id}/` | `#demo-schedule-table` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
