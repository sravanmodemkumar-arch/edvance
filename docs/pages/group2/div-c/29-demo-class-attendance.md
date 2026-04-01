# Page 29: Demo Class Attendance

**URL:** `/group/adm/demo/attendance/`
**Template:** `portal_base.html` (light theme)
**Division:** C — Group Admissions
**Module:** Demo Classes

---

## 1. Purpose

Demo Class Attendance tracks the full attendance record for every demo and trial class session run across the group's branches. Recording attendance is a critical operational step: it transforms a scheduling entry into evidence of actual engagement. For the Demo Coordinator, knowing who showed up — and who did not — is the data that drives the next 24 hours of admissions follow-up activity. A no-show from a pre-registered prospect is not a lost cause; it is an opening for a targeted callback. A walk-in who arrived without registration is a high-intent prospect who needs immediate capturing before the trail goes cold.

This page serves as the live attendance console during and immediately after each demo session. The coordinator or branch organizer selects the session, pulls up the pre-registered attendee list, and marks attendance in real time using toggle controls. Walk-in students who arrive without pre-registration are captured through the quick walk-in entry form and merged into the session's attendee record. At session close, the coordinator submits the attendance record, triggering automatic downstream actions: no-shows are added to the follow-up queue, walk-ins receive a welcome message, and the session's conversion funnel entry is updated.

The page also provides a cross-session view for tracking repeat attendance — a prospect who has attended three demos without applying is a signal for a different counselling intervention than one attending their first. The Multi-session Attendance View gives the coordinator visibility into these behavioural patterns across branches and sessions. All attendance data is consumed by the conversion funnel tracker (Page 31) and the demo feedback collector (Page 30), making accurate attendance submission a data-quality requirement for the entire admissions analytics chain.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Demo Class Coordinator (29) | G3 | Full — view all sessions, mark/edit attendance, bulk actions, manage follow-up queue | Primary owner of this page |
| Branch Demo Organizer | Branch | View and mark attendance for own branch demos only | Cannot see other branches |
| Group Admission Coordinator (24) | G3 | View all sessions and attendance; no edit post-submission | Read access for oversight |
| Group Admissions Director (23) | G3 | View-only across all branches | Strategic oversight |

Access enforcement: All views protected with `@login_required` and `@role_required(['demo_coordinator', 'branch_demo_organizer', 'admission_coordinator', 'admissions_director'])`. Branch Demo Organizer scope enforced via `request.user.branch_id` filter on all session and attendance querysets in the Django view layer.

---

## 3. Page Layout

### 3.1 Breadcrumb
`Group Portal → Admissions → Demo Classes → Attendance`

### 3.2 Page Header
**Title:** Demo Class Attendance
**Subtitle:** Mark, review, and manage attendance for demo sessions
**Actions (right-aligned):**
- `[Export Attendance CSV]` — secondary button (exports filtered/current session data)

### 3.3 Alert Banner

| Condition | Banner Type | Message |
|---|---|---|
| Demos today with attendance not yet marked | Warning (amber) | "N demo sessions today have not had attendance marked. [View Sessions →]" |
| Active demo session in progress right now | Info (blue) | "Demo DM-0492 at Ameerpet is currently in progress. [Mark Attendance →]" |
| No-show follow-up queue > 20 pending | Warning (amber) | "22 no-shows from the past 3 days are awaiting follow-up action." |
| Attendance submitted successfully | Success (green) | "Attendance for DM-0482 submitted. No-shows added to follow-up queue." |

---

## 4. KPI Summary Bar

| Card | Metric | Source | Colour Rule | Drill-down |
|---|---|---|---|---|
| Today's Demo Sessions | COUNT sessions scheduled for today group-wide | `demo_sessions` WHERE date = today | Blue always | Filters session selector to today |
| Attendance Marked Today % | Sessions with submitted attendance / total today sessions × 100 | `demo_attendance` | Green if 100%; amber if 50–99%; red if < 50% | Filters to unmarked sessions |
| Avg Attendance Rate (This Month) | AVG (attended / registered) per session this month | `demo_attendance` | Green if ≥ 70%; amber if 50–69%; red if < 50% | No drill-down |
| No-shows Today | COUNT no-shows from today's sessions | `demo_attendance` WHERE attended=False AND date=today | Red if > 0 | Scrolls to Section 5.5 |
| Walk-in Attendees | COUNT walk-in entries added today | `demo_attendance` WHERE source=walk_in AND date=today | Blue always | Filters table to walk-ins |
| Attendance Not Marked | COUNT sessions past start time with no attendance submission | `demo_sessions` WHERE start_time < now AND attendance_submitted = False | Red if > 0 | Filters to unsubmitted sessions |

**HTMX auto-refresh pattern (every 5 minutes):**
```html
<div id="kpi-bar"
     hx-get="/group/adm/demo/attendance/kpis/"
     hx-trigger="load, every 300s"
     hx-target="#kpi-bar"
     hx-swap="outerHTML">
  <!-- KPI cards rendered here -->
</div>
```

---

## 5. Sections

### 5.1 Demo Session Selector

**Display:** Prominent selector bar at the top of the content area. Two cascading dropdowns:
1. **Date picker** — defaults to today; selecting a date reloads the session dropdown
2. **Session dropdown** — lists all demo sessions for the selected date (format: `DM-ID | Branch | Subject | Time | Status`)

On session selection, the attendance sheet (Section 5.2) loads via HTMX. If attendance has already been submitted for the selected session, the sheet renders in read-only mode with an `[Edit Attendance]` button (opens edit drawer).

**Branch filter** (visible to G3 roles only): "All branches" or specific branch dropdown — narrows the session list.

**HTMX:** Date change → `hx-get="/group/adm/demo/attendance/sessions/?date=YYYY-MM-DD"` targeting `#session-dropdown` with `hx-swap="outerHTML"`. Session change → `hx-get="/group/adm/demo/attendance/sheet/{session_id}/"` targeting `#attendance-sheet-area` with `hx-swap="innerHTML"`.

---

### 5.2 Attendance Sheet

**Display:** Loaded after session selection. Sortable table of pre-registered attendees for the selected session. Mark mode (pre-submission) vs. read mode (post-submission).

**Columns:**

| Column | Notes |
|---|---|
| # | Row number |
| Student Name | Full name |
| Parent Name | Primary contact parent |
| Phone | Mobile number (partially masked in read mode) |
| Source | Pre-registered / Walk-in (badge) |
| Class | e.g. "Class 10", "Intermediate 1st Year" |
| Stream Interest | MPC / BiPC / MEC / CEC / Undecided |
| Attended | Toggle (Yes / No) — clickable in mark mode |
| Parent Attended | Toggle (Yes / No) |
| Time In | Time stamp input (optional, auto-filled on toggle) |
| Notes | Short notes text field per student |
| Save | `[Save Row]` per-row save button (for individual updates) |

**Bulk actions (top of table):**
- `[Mark All Present]` — sets all toggles to Yes
- `[Mark All Absent]` — sets all toggles to No
- `[Submit Attendance]` — primary button; triggers confirmation modal then posts full sheet

**HTMX per-row save:** Each row's `[Save Row]` triggers `hx-post="/group/adm/demo/attendance/{session_id}/row/{reg_id}/"` with row data, targeting `#row-status-{reg_id}` with `hx-swap="innerHTML"` (updates a small save-indicator badge).

**Empty state:** "No registrations found for this session. You can add walk-ins using the form below."

---

### 5.3 Walk-in Entry Form

**Display:** Collapsible panel below the attendance sheet. "Add Walk-in Attendee" heading with a `[+]` expand toggle. When expanded, shows a quick-capture form.

**Form fields:**
- Student Name (required)
- Class / Year (dropdown)
- Parent Name
- Parent Phone (required)
- Stream Interest (dropdown)
- How did they hear about the demo? (dropdown: Social media / Referred by alumni / Passed by branch / Other)
- Notes

**Submit:** `[Add to Attendance]` — `hx-post="/group/adm/demo/attendance/{session_id}/walk-in/"` — on success, appends new row to the attendance sheet table and shows success toast. No page reload.

**HTMX swap:** On success response, `hx-swap="beforeend"` on `#attendance-table-body` appends the new row HTML fragment.

---

### 5.4 Attendance Summary

**Display:** Rendered automatically after attendance is submitted. Shows a summary card panel.

**Charts (Chart.js 4.x):**
- **Registered vs Attended vs No-show** — horizontal bar chart, three bars side by side
- **Breakdown by Source** — donut chart: Pre-registered attended / Walk-in / No-show
- **Breakdown by Stream Interest** — horizontal bar: distribution of attended students by declared stream interest

**Stat tiles below charts:**
- Total registered | Attended | No-show | Walk-ins | Parent attendance rate

**HTMX:** Summary section lazy-loaded via `hx-get="/group/adm/demo/attendance/{session_id}/summary/"` with `hx-trigger="load"` when `#summary-section` enters the DOM after submission redirect.

---

### 5.5 No-show Follow-up Queue

**Display:** Paginated list panel (20/page). Shows no-shows from today and the past 3 days that have not yet been followed up.

**Each entry shows:**
- Student name | Branch | Demo date | Demo subject | Phone | Days since demo | Follow-up count

**Actions per row:**
- `[Log Call]` — opens follow-up-action drawer
- `[Schedule New Demo]` — opens demo-create-form pre-filled with branch and student phone
- `[Mark as Lost]` — inline confirm → removes from queue, marks prospect as Lost in system

**Filters:** Branch, Demo date range, Days since demo (0 / 1 / 2–3 / All)

**HTMX:** `hx-get="/group/adm/demo/attendance/no-show-queue/"` loaded on page load, `hx-target="#no-show-queue"`, reloads after each action.

**Empty state:** "No pending no-show follow-ups. All recent no-shows have been contacted."

---

### 5.6 Multi-session Attendance View

**Display:** Cross-session table — shows prospects who have attended more than one demo session. Used to identify repeat interest and pattern behaviour.

**Columns:**

| Column | Notes |
|---|---|
| Student Name | Linked to prospect profile |
| Phone | Partially masked |
| Sessions Attended | Count of demos attended |
| Branches | List of branches where attended |
| First Demo Date | Date of first demo attended |
| Last Demo Date | Most recent demo |
| Applied? | Yes / No badge |
| Action | `[View Journey →]` — links to conversion page prospect detail |

**Filter:** Sessions attended >= N (dropdown: 2 / 3 / 4+), Branch, Applied status

**HTMX:** `hx-get="/group/adm/demo/attendance/multi-session/"` on tab or section load, `hx-target="#multi-session-table"`.

**Empty state:** "No prospects have attended multiple demo sessions yet."

---

## 6. Drawers & Modals

### 6.1 `attendance-edit-drawer` Drawer
**Width:** 480px
**Trigger:** `[Edit Attendance]` button when session is already submitted
**HTMX endpoint:** `hx-get="/group/adm/demo/attendance/{session_id}/edit/"` lazy-loaded
**Content:**
- Reason for edit (dropdown: Data entry error / Late update / Walk-in missed / Other) — required
- Editable attendance toggles for each attendee
- `[Save Changes]` — `hx-post="/group/adm/demo/attendance/{session_id}/edit/"` with reason included

---

### 6.2 `follow-up-action` Drawer
**Width:** 400px
**Trigger:** `[Log Call]` button in no-show follow-up queue
**HTMX endpoint:** `hx-get="/group/adm/demo/attendance/follow-up/{prospect_id}/"` lazy-loaded
**Tabs:**
1. **Log Call** — call outcome (Answered/No answer/Wrong number), notes, next action (Schedule demo / Send info / Mark lost / Call again tomorrow)
2. **Schedule Next Step** — date for follow-up reminder, assign to counsellor (dropdown)

---

### 6.3 `walk-in-capture` Drawer
**Width:** 400px
**Trigger:** Can also be opened from `[Add Walk-in]` button in page header (alternative to inline form)
**HTMX endpoint:** `hx-get="/group/adm/demo/attendance/walk-in-capture/"` lazy-loaded
**Content:** Same fields as Section 5.3 inline form but in drawer format with session selector (date + session dropdown) — for capturing walk-ins when not currently viewing a specific session.

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Row saved (per-row toggle) | "Attendance saved for [Student Name]." | Success | 2s |
| All marked present | "All N attendees marked as present." | Success | 3s |
| All marked absent | "All N attendees marked as absent." | Warning | 3s |
| Attendance submitted | "Attendance for DM-XXXX submitted. N no-shows added to follow-up queue." | Success | 5s |
| Walk-in added | "[Name] added as walk-in attendee." | Success | 3s |
| Attendance edit saved | "Attendance record updated. Change reason logged." | Success | 4s |
| Follow-up logged | "Call logged for [Name]. Next action scheduled." | Success | 3s |
| Mark as Lost confirmed | "[Name] marked as Lost and removed from queue." | Info | 4s |
| Session not yet selected | "Please select a demo session to mark attendance." | Warning | 4s |

---

## 8. Empty States

| Condition | Illustration | Heading | Description | CTA |
|---|---|---|---|---|
| No sessions today (all branches) | Calendar with checkmark | "No demos scheduled today" | "There are no demo sessions scheduled for today." | `[View Full Schedule →]` |
| Session selected — no registrations | Empty list icon | "No registrations for this session" | "No students pre-registered. You can add walk-in attendees below." | `[Add Walk-in]` |
| No-show queue empty | Checkmark circle | "No pending follow-ups" | "All no-shows from the past 3 days have been contacted." | None |
| Multi-session table — no repeats | Single person icon | "No repeat attendees yet" | "Prospects who attend more than one demo will appear here." | None |
| Attendance summary — session not submitted | Chart placeholder | "Submit attendance to see summary" | "Mark and submit this session's attendance to view the summary chart." | `[Submit Attendance]` |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load (KPI bar) | Skeleton cards (6 cards, grey shimmer) |
| Session dropdown loading after date change | Inline spinner inside dropdown |
| Attendance sheet loading after session selection | Skeleton rows (8 rows, column-width placeholders) |
| Summary section loading after submission | Skeleton chart placeholders (2 charts) |
| No-show queue loading | Skeleton list rows (5 rows) |
| Multi-session table loading | Skeleton rows (5 rows) |
| Per-row attendance save | Spinner in `[Save Row]` button, button disabled |
| Walk-in form submission | Button spinner + disabled state |
| Drawer opening | Spinner centred in drawer body |

---

## 10. Role-Based UI Visibility

All UI visibility decisions made server-side in Django template. No client-side JS role checks.

| UI Element | Demo Coordinator (29) | Branch Demo Organizer | Admission Coordinator (24) | Admissions Director (23) |
|---|---|---|---|---|
| Session selector — all branches | Visible | Own branch only | Visible | Visible |
| Attendance toggles (mark mode) | Visible | Visible (own branch) | Hidden (read-only) | Hidden (read-only) |
| `[Mark All Present/Absent]` | Visible | Visible | Hidden | Hidden |
| `[Submit Attendance]` | Visible | Visible | Hidden | Hidden |
| Walk-in entry form | Visible | Visible | Hidden | Hidden |
| `[Edit Attendance]` button | Visible | Visible (own branch) | Hidden | Hidden |
| No-show follow-up queue | Visible | Visible (own branch) | Visible | Visible |
| `[Log Call]` action | Visible | Visible | Hidden | Hidden |
| `[Mark as Lost]` action | Visible | Hidden | Hidden | Hidden |
| Multi-session attendance view | Visible | Hidden | Visible | Visible |
| `[Export Attendance CSV]` | Visible | Visible (own branch) | Visible | Visible |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/adm/demo/attendance/kpis/` | JWT G3+ | KPI bar metrics for attendance page |
| GET | `/api/v1/group/{group_id}/adm/demo/sessions/` | JWT G3+ | List sessions by date and branch |
| GET | `/api/v1/group/{group_id}/adm/demo/attendance/{session_id}/` | JWT G3+ | Get attendance sheet for a session |
| POST | `/api/v1/group/{group_id}/adm/demo/attendance/{session_id}/row/{reg_id}/` | JWT G3 write | Save individual attendance row |
| POST | `/api/v1/group/{group_id}/adm/demo/attendance/{session_id}/submit/` | JWT G3 write | Submit full attendance record |
| POST | `/api/v1/group/{group_id}/adm/demo/attendance/{session_id}/walk-in/` | JWT G3 write | Add walk-in attendee to session |
| PATCH | `/api/v1/group/{group_id}/adm/demo/attendance/{session_id}/edit/` | JWT G3 write | Edit submitted attendance with reason |
| GET | `/api/v1/group/{group_id}/adm/demo/attendance/{session_id}/summary/` | JWT G3+ | Post-submission summary stats |
| GET | `/api/v1/group/{group_id}/adm/demo/no-show-queue/` | JWT G3+ | No-show follow-up queue |
| POST | `/api/v1/group/{group_id}/adm/demo/no-show-queue/{prospect_id}/log-call/` | JWT G3 write | Log follow-up call outcome |
| POST | `/api/v1/group/{group_id}/adm/demo/no-show-queue/{prospect_id}/mark-lost/` | JWT G3 write | Mark no-show prospect as lost |
| GET | `/api/v1/group/{group_id}/adm/demo/attendance/multi-session/` | JWT G3+ | Cross-session repeat attendance data |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| KPI bar auto-refresh | `load, every 300s` | GET `/group/adm/demo/attendance/kpis/` | `#kpi-bar` | `outerHTML` |
| Date change → reload session dropdown | `change` on date picker | GET `/group/adm/demo/attendance/sessions/?date=YYYY-MM-DD` | `#session-dropdown` | `outerHTML` |
| Session selection → load attendance sheet | `change` on session dropdown | GET `/group/adm/demo/attendance/sheet/{session_id}/` | `#attendance-sheet-area` | `innerHTML` |
| Per-row save toggle | `click` on `[Save Row]` | POST `/group/adm/demo/attendance/{session_id}/row/{reg_id}/` | `#row-status-{reg_id}` | `innerHTML` |
| Mark all present | `click` | POST `/group/adm/demo/attendance/{session_id}/mark-all/?present=true` | `#attendance-table-body` | `innerHTML` |
| Mark all absent | `click` | POST `/group/adm/demo/attendance/{session_id}/mark-all/?present=false` | `#attendance-table-body` | `innerHTML` |
| Submit attendance | `click` on `[Submit Attendance]` (after confirm) | POST `/group/adm/demo/attendance/{session_id}/submit/` | `#attendance-sheet-area` | `innerHTML` |
| Walk-in form submit (inline) | `submit` | POST `/group/adm/demo/attendance/{session_id}/walk-in/` | `#attendance-table-body` | `beforeend` |
| Load summary after submission | `load` (on #summary-section mounting) | GET `/group/adm/demo/attendance/{session_id}/summary/` | `#summary-section` | `innerHTML` |
| Open follow-up drawer | `click` on `[Log Call]` | GET `/group/adm/demo/attendance/follow-up/{prospect_id}/` | `#drawer-container` | `innerHTML` |
| Submit follow-up log | `submit` in drawer | POST `/group/adm/demo/no-show-queue/{prospect_id}/log-call/` | `#no-show-queue` | `innerHTML` |
| Mark as Lost | `click` (confirm) | POST `/group/adm/demo/no-show-queue/{prospect_id}/mark-lost/` | `#no-show-row-{prospect_id}` | `outerHTML` |
| No-show queue page filter change | `change` | GET `/group/adm/demo/attendance/no-show-queue/` | `#no-show-queue` | `innerHTML` |
| Multi-session table filter change | `change` | GET `/group/adm/demo/attendance/multi-session/` | `#multi-session-table` | `innerHTML` |
| Open walk-in capture drawer (header) | `click` on `[Add Walk-in]` | GET `/group/adm/demo/attendance/walk-in-capture/` | `#drawer-container` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
