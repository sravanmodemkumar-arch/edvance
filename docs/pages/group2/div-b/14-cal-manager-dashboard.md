# 14 — Academic Calendar Manager Dashboard

> **URL:** `/group/acad/cal-manager/`
> **File:** `14-cal-manager-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Group Academic Calendar Manager (G3) — exclusive landing page

---

## 1. Purpose

Primary post-login landing for the Group Academic Calendar Manager. This role is the central authority for the group's academic calendar — responsible for setting working days, declaring group-level holidays, scheduling Parent-Teacher Meetings (PTMs), coordinating academic events across all branches, and approving branch-submitted holiday and event requests.

The calendar manager's primary daily concerns are: which branches have not yet synced or confirmed the group calendar for the current term; which holiday approval requests from branches are pending; whether any events across branches conflict with each other or with group-level exam dates; and how far through the academic year the group currently is. The dashboard surfaces all four of these concerns on the landing page.

The group academic calendar is the authoritative source. Branches inherit the group calendar and may submit requests to add local holidays or events, but cannot override group-mandated dates. The calendar manager approves or rejects branch requests and publishes calendar updates to all branches simultaneously. Coordination with the Group Exam Controller is essential — the calendar manager ensures no exam dates conflict with declared holidays, and surfaces conflicts when they arise.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Academic Calendar Manager | G3 | Full — all sections, all actions | This is their exclusive dashboard |
| Chief Academic Officer (CAO) | G4 | Full read + override actions | Full oversight |
| Group Academic Director | G3 | Read — all sections | Academic coordination visibility |
| Group Exam Controller | G3 | Read — upcoming events timeline and conflict alerts | Exam-calendar coordination |
| Group Results Coordinator | G3 | Read — upcoming events timeline only | Result-publication timing |
| All Stream Coordinators | G3 | Read — upcoming events timeline only | Stream exam scheduling reference |
| Group JEE/NEET Integration Head | G3 | Read — upcoming events (coaching schedule context) | Coaching calendar alignment |
| Group IIT Foundation Director | G3 | Read — upcoming events only | Foundation test scheduling |
| Group Olympiad & Scholarship Coord | G3 | Read — upcoming events (olympiad deadlines context) | Olympiad calendar alignment |
| Group Special Education Coordinator | G3 | Read — PTM schedule only | PTM special needs accommodation coordination |
| Group Academic MIS Officer | G1 | Read-only — all sections | No write controls visible |
| Group Curriculum Coordinator | G2 | Read — upcoming events and working days only | Content scheduling reference |

> **Access enforcement:** Django view decorator `@require_role('academic_cal_manager')`. CAO and MIS Officer admitted via role-union check. All other roles are redirected to their own dashboard unless explicitly listed above.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Academic Leadership  ›  Academic Calendar  ›  Calendar Manager Dashboard
```

### 3.2 Page Header
```
Welcome back, [Manager Name]                    [Publish Calendar Update ↑]  [+ Add Event]  [Settings ⚙]
Group Academic Calendar Manager  ·  Last login: [date time]  ·  [Group Logo]
```

### 3.3 Alert Banner (conditional — shown only when alerts exist)
- Collapsible panel above KPI row
- Background: `bg-red-50 border-l-4 border-red-500` for Critical · `bg-yellow-50 border-l-4 border-yellow-400` for Warning
- Each alert: icon + message + branch name + [Take Action →] link
- "Dismiss" per alert (stored in session, reappears next login if unresolved)
- Maximum 5 alerts shown; "View all →" link

**Alert trigger examples:**
- Calendar conflict: a branch exam date falls on a group-declared holiday
- Branch has not confirmed the current term calendar > 14 days after publication
- Holiday approval request pending > 7 days without decision
- PTM scheduled for a branch with no parent notification sent (< 5 days to PTM)
- Working days count for a branch falls below minimum statutory requirement for the term

---

## 4. KPI Summary Bar

| Card | Metric | Source | Colour Rule | Drill-down |
|---|---|---|---|---|
| Working Days Set | Working days configured for current academic year · Branches confirmed / total branches | Calendar module | Green = all confirmed · Yellow some unconfirmed · Red ≥ 20% unconfirmed | → Section 5.1 Calendar Coverage |
| PTM Dates Set | PTMs scheduled for current term · Parent notifications sent Y/N count | PTM module | Green = all sent · Yellow notifications pending · Red any PTM < 5 days with no notification | → Section 5.5 PTM Schedule |
| Holidays Declared | Group-level holidays declared this academic year (total) | Calendar module | Informational — no colour rule | → Section 5.1 Calendar Coverage |
| Events Pending Approval | Branch-submitted holiday/event requests awaiting group approval (pulsing if > 0) | Approval queue | Green = 0 · Yellow 1–5 · Red > 5 | → Section 5.4 Holiday Approval Queue |
| Calendar Conflicts | Branches with at least one calendar conflict (exam on holiday, events overlapping) | Conflict monitor | Green = 0 · Yellow 1–3 · Red > 3 (pulsing badge) | → Section 5.6 Conflict Alerts |
| Academic Year Progress | Day X of Y working days elapsed · XX% of academic year complete | Calendar module | Progress bar — green < 80% · Amber 80–90% · Red > 90% (year-end pressure) | → Section 5.7 Year Progress |

**HTMX:** Cards auto-refresh every 5 minutes via `hx-trigger="every 5m"` `hx-get="/api/v1/group/{group_id}/acad/cal-manager/kpi-cards/"` `hx-swap="innerHTML"` targeting `#kpi-bar`.

---

## 5. Sections

### 5.1 Calendar Coverage — Working Days & Holidays

> Summary of the academic calendar configuration for the current year — working days set, holidays declared, and which branches have confirmed their calendar.

**Display:** Stat cards row + branch confirmation table.

**Stat cards:**
- Total working days in academic year: [N] (Apr–Mar)
- Holidays declared (group-level): [N] — click to expand list
- Branch-specific holidays approved: [N]
- Branches with confirmed calendar: [M] of [Total]

**Holiday list (collapsible, triggered by "Holidays declared" card):**
- Table: Holiday name · Date · Type (National / State / Group-declared) · Applicable branches (All / Specific)
- Export: [Download Holiday List PDF]

**Branch confirmation table:**

| Column | Sortable | Notes |
|---|---|---|
| Branch Name | ✅ | Link to branch detail |
| City | ✅ | |
| Calendar Version | ✅ | Which version of the group calendar this branch has |
| Confirmed | ✅ | Yes (green) / No (red) / Outdated (amber — branch confirmed an older version) |
| Confirmed By | ✅ | Branch Principal name · Date confirmed |
| Working Days Count | ✅ | Days configured for this branch — red if below minimum |
| Actions | ❌ | [Send Reminder] (G3 only) · [Force Sync] (G3 only) |

**[Send Reminder] (G3):** POST to send notification to branch to confirm calendar.

**[Force Sync] (G3):** POST to push current group calendar to branch, overriding branch version. Confirmation modal required.

**[Publish Calendar Update ↑] header button:** Opens publish workflow drawer — sends updated group calendar to all branches.

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/cal-manager/coverage/"` · `hx-trigger="load"` · `hx-target="#coverage-section"`.

---

### 5.2 Branch Calendar Sync Status

> Detailed per-branch status: confirmed / pending / outdated / conflict.

**Display:** Table (sortable, filterable)

**Columns:**

| Column | Sortable | Notes |
|---|---|---|
| Branch Name | ✅ | |
| City | ✅ | |
| Sync Status | ✅ | Confirmed (green) · Pending (amber) · Conflict (red) · Outdated (orange) |
| Last Sync Date | ✅ | When branch last pulled/confirmed the group calendar |
| Open Conflicts | ✅ | Count of calendar conflicts — red if > 0 |
| Pending Requests | ✅ | Branch holiday/event requests awaiting approval |
| Actions | ❌ | [View Branch Calendar →] [Resolve Conflicts →] [Send Reminder] — last two G3 only |

**Filters:** Sync status · City · Conflicts (only show branches with open conflicts)

**Default sort:** Sync status — Conflict first, then Pending, then Outdated, then Confirmed.

**[View Branch Calendar →]:** Opens read-only view of that branch's effective calendar (group calendar + approved branch additions).

**[Resolve Conflicts →]:** Opens conflict resolution drawer for that branch.

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/cal-manager/sync-status/"` · filter changes trigger `hx-get` · `hx-target="#sync-status-section"`.

---

### 5.3 Upcoming Events — Next 14 Days

> All group-level academic events across all branches in the next 14 days.

**Display:** Timeline (vertical, day-by-day) — 14-day look-ahead.

**Timeline item fields:** Date badge · Event name · Event type badge · Branches scope (All / Specific — count) · Organiser role · Status (Confirmed / Draft / Pending approval) · [View →]

**Event type colour coding:**
- PTM: Blue
- Exam (group): Orange
- Holiday: Red
- Academic event (science fair, quiz, etc.): Green
- Sports / co-curricular: Purple
- Staff training / CPD: Teal
- Olympiad registration deadline: Brown

**Alert:** Any event in the next 48 hours with status "Draft" or "Pending approval" → red alert strip above timeline.

**Filter within section:** Event type multi-select · Branch filter · Status filter.

**[+ Add Event] header button:** Opens event creation drawer.

**Drawer: `event-create-edit`**
- Width: 640px
- Tabs: Event Details · Branch Scope · Notifications · Publish
- Event Details: Name · Type · Date + time · Duration · Description
- Branch Scope: All branches / Specific branch selection / Zone-based selection
- Notifications: Which roles to notify · Notification channels (email / WhatsApp / portal)
- Publish: [Save as Draft] [Publish to Branches]

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/cal-manager/upcoming-events/"` · `hx-trigger="load"` · filter changes trigger `hx-get` · `hx-target="#upcoming-events-section"`.

---

### 5.4 Holiday Approval Queue

> Branch-submitted holiday and event requests awaiting group-level approval or rejection.

**Display:** Counter (active requests) + action list (card per request)

**Card fields:** Request # · Branch name · City · Holiday/Event name · Requested date · Type (Local holiday / Cultural event / Sports event / Branch-specific exam day off) · Submitted by · Submitted date · Days pending (red if > 7) · Reason / rationale (expandable) · [Approve ✓] [Reject ✗] [View Details →]

**[Approve ✓]:** POST with optional approval note → card removed from queue → branch notified → calendar updated.

**[Reject ✗]:** Opens mini rejection modal — required rejection reason (min 20 chars) → POST → branch notified.

**[View Details →]:** Expands card or opens detail drawer with full request context, prior year history for same date, and impact on branch working days count.

**Drawer: `holiday-request-detail`**
- Width: 520px
- Tabs: Request Details · Calendar Impact · History
- Calendar Impact: Shows how approving this request affects branch working days count for the term · Flags if approval causes branch to fall below minimum statutory days
- History: All prior holiday requests from this branch — approved / rejected / year

**Bulk action (G3):** [Approve All Selected] with optional group note.

**Empty state:** "No holiday or event requests pending approval." — checkmark circle.

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/cal-manager/approval-queue/"` · `hx-trigger="load"` · Approve: `hx-post="/api/v1/group/{group_id}/acad/cal-manager/requests/{request_id}/approve/"` · Reject: opens modal then POST with reason.

---

### 5.5 PTM Schedule

> Parent-Teacher Meeting schedule for the current term — branch-wise, with notification sent status.

**Display:** Table (sortable, filterable)

**Columns:**

| Column | Sortable | Notes |
|---|---|---|
| Branch Name | ✅ | |
| PTM Date | ✅ | Date — red if < 5 days and notification not sent |
| PTM Type | ✅ | Full-day / Half-day / Online / Hybrid |
| Venue | ✅ | Branch campus / Online platform |
| Parent Notification Sent | ✅ | Yes (green) / No (red) / Scheduled (amber) |
| Notification Date | ✅ | When notification was sent or scheduled |
| Status | ✅ | Scheduled · Completed · Cancelled · Rescheduled |
| Actions | ❌ | [Send Notification Now] [Edit PTM] [Cancel PTM] — G3 only |

**Filters:** PTM status · Notification sent (Y / N) · Branch · Date range.

**[Send Notification Now] (G3):** POST to trigger immediate parent notification (email + WhatsApp) for this PTM → toast success.

**[Edit PTM] (G3):** Opens edit drawer — date/time/type/venue changes. On save: branch notified of change.

**[Cancel PTM] (G3):** Opens cancellation modal — reason required. On confirm: cancellation notification sent to branch and parents.

**[+ Add PTM] button** (top-right of section, G3 only): Opens PTM creation drawer.

**Drawer: `ptm-create-edit`**
- Width: 560px
- Fields: Branch(es) · Date · Time · Duration · Type (Full / Half / Online / Hybrid) · Venue · Notes
- Action: [Save] [Save & Send Notification]

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/cal-manager/ptm-schedule/"` · filter changes trigger `hx-get` · `hx-target="#ptm-section"` · Send notification: `hx-post="/api/v1/group/{group_id}/acad/cal-manager/ptm/{ptm_id}/notify/"`.

---

### 5.6 Calendar Conflict Alerts

> Branches where calendar conflicts exist — exam date on a holiday, overlapping events, or PTM clashing with major exam.

**Display:** Alert list (card-style, sorted by severity)

**Card fields:** Branch name · City · Conflict description · Conflicting items (e.g., "Unit Test — Physics (Class XI)" conflicts with "Diwali Holiday") · Conflict type · Severity (Hard / Soft) · Discovered date · Days unresolved · [Resolve →]

**Conflict types:**
- Hard conflict: Group exam date falls on a group-declared holiday
- Hard conflict: PTM and major exam same day, same branch
- Soft conflict: Two events in same branch within 24 hrs of each other
- Soft conflict: Branch-approved local holiday falls adjacent to a long weekend (creating > 5-day gap)

**[Resolve →]:** Opens conflict resolution drawer.

**Drawer: `conflict-resolve`**
- Width: 560px
- Tabs: Conflict Details · Resolution Options · Resolution History
- Resolution Options: System suggests 3 alternatives (reschedule the event / reschedule the exam / request exam controller to move exam / override and mark conflict as acceptable)
- [Apply Resolution]: POST resolution choice → notifies relevant roles (Exam Controller / Branch Principal / Stream Coordinator) → audit log

**Empty state:** "No calendar conflicts detected." — green checkmark.

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/cal-manager/conflicts/"` · `hx-trigger="load"` · `hx-target="#conflicts-section"` · Resolve: `hx-get` opens drawer, `hx-post` applies resolution.

---

### 5.7 Academic Year Progress

> Visual progress indicator for the current academic year — working days elapsed vs total.

**Display:** Progress bar (prominent, full-width card) + supporting stats.

**Progress bar:**
- Colour: Green < 70% · Amber 70–85% · Red > 85% (year-end stretch)
- Label: "Day [X] of [Y] working days · [XX%] of academic year complete · [Z] days remaining"
- Term marker: Vertical tick marks on bar showing Term 1, Term 2, Term 3 boundaries

**Supporting stats (below bar):**
- Current term: Term [N] — started [date] · ends [date]
- Working days this term: [X] elapsed of [Y] total
- Next major event: [Event name] on [date] ([N] days away)
- Academic year started: [date] · ends: [date]
- Holidays taken (group-level): [N] days
- Holidays remaining (approved): [N] days

**Term-end actions (shown when < 10 working days to term end):**
- [Prepare Term-end Calendar Summary] → generates a downloadable calendar PDF for the term

**Branch-level mini table (below main progress bar):**

| Column | Description |
|---|---|
| Branch | Branch name |
| Working Days Elapsed | This branch's actual working days (may differ due to branch holidays) |
| Working Days Remaining | Projected |
| Status | On track / Deficit (< statutory minimum pace) |

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/cal-manager/year-progress/"` · `hx-trigger="load"` · `hx-target="#year-progress-section"`.

---

## 6. Drawers & Modals

### 6.1 Drawer: `publish-calendar-update`
- **Trigger:** [Publish Calendar Update ↑] in page header
- **Width:** 640px
- **Tabs:** Changes Summary · Branch Scope · Notifications · Confirm
- **Changes Summary:** Diff of what changed in the calendar vs the previously published version
- **Branch Scope:** All branches / Selected branches
- **Notifications:** Roles to notify · Channels · Message (pre-filled, editable)
- **Confirm:** [Publish Update] → POST → all selected branches receive the update → audit log
- **HTMX:** `hx-post="/api/v1/group/{group_id}/acad/cal-manager/publish/"` on confirm

### 6.2 Drawer: `event-create-edit`
- **Trigger:** [+ Add Event] header button or [View →] in timeline
- **Width:** 640px
- **Tabs:** Event Details · Branch Scope · Notifications · Publish
- **HTMX:** `hx-post="/api/v1/group/{group_id}/acad/cal-manager/events/"` for new · `hx-patch="/api/v1/group/{group_id}/acad/cal-manager/events/{event_id}/"` for edit

### 6.3 Drawer: `holiday-request-detail`
- **Trigger:** [View Details →] in Section 5.4 approval queue card
- **Width:** 520px
- **Tabs:** Request Details · Calendar Impact · History
- **HTMX:** `hx-get="/api/v1/group/{group_id}/acad/cal-manager/requests/{request_id}/"` `hx-target="#drawer-body"`

### 6.4 Drawer: `ptm-create-edit`
- **Trigger:** [+ Add PTM] or [Edit PTM] in Section 5.5
- **Width:** 560px
- **Fields:** Branch(es) · Date · Time · Duration · Type · Venue · Notes
- **HTMX:** `hx-post="/api/v1/group/{group_id}/acad/cal-manager/ptm/"` for new · `hx-patch` for edit

### 6.5 Drawer: `conflict-resolve`
- **Trigger:** [Resolve →] in Section 5.6 conflict card
- **Width:** 560px
- **Tabs:** Conflict Details · Resolution Options · Resolution History
- **HTMX:** `hx-get="/api/v1/group/{group_id}/acad/cal-manager/conflicts/{conflict_id}/"` `hx-target="#drawer-body"` · Apply resolution: `hx-post="/api/v1/group/{group_id}/acad/cal-manager/conflicts/{conflict_id}/resolve/"`

### 6.6 Modal: `reject-holiday-request`
- **Trigger:** [Reject ✗] in Section 5.4 approval queue card
- **Width:** 420px
- **Content:** Request summary (read-only) · Rejection reason (required, min 20 chars) · [Confirm Rejection] [Cancel]
- **On confirm:** `hx-post="/api/v1/group/{group_id}/acad/cal-manager/requests/{request_id}/reject/"` → toast + card removed + branch notified

### 6.7 Modal: `cancel-ptm-confirm`
- **Trigger:** [Cancel PTM] in Section 5.5 PTM table
- **Width:** 420px
- **Content:** PTM details (read-only) · Cancellation reason (required) · [Confirm Cancellation] [Cancel]
- **On confirm:** `hx-post="/api/v1/group/{group_id}/acad/cal-manager/ptm/{ptm_id}/cancel/"` → toast + notification sent to branch + parents

### 6.8 Modal: `force-sync-confirm`
- **Trigger:** [Force Sync] in Section 5.1 branch confirmation table
- **Width:** 420px
- **Content:** "Push current group calendar to [Branch Name]? This will override any local calendar changes the branch has made." · [Confirm Force Sync] [Cancel]
- **On confirm:** `hx-post="/api/v1/group/{group_id}/acad/cal-manager/branches/{branch_id}/force-sync/"` → toast + audit log

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Calendar update published | "Calendar update published to [N] branches — notifications sent" | Success (green) | 5s auto-dismiss |
| Holiday request approved | "Holiday request approved for [Branch Name] — [Event Name] on [date]" | Success | 4s |
| Holiday request rejected | "Rejection sent to [Branch Name] with reason" | Info (blue) | 4s |
| Calendar reminder sent | "Calendar confirmation reminder sent to [Branch Name]" | Info | 4s |
| Force sync completed | "Group calendar pushed to [Branch Name]" | Info | 4s |
| PTM notification sent | "Parent notification sent for PTM on [date] — [Branch Name]" | Success | 5s |
| PTM cancelled | "PTM cancelled — [Branch Name] and parents notified" | Warning (yellow) | 6s |
| Conflict resolved | "Calendar conflict resolved — [Branch Name] and relevant roles notified" | Success | 5s |
| Event published | "Event '[Name]' published to [N] branches" | Success | 4s |
| KPI load error | "Failed to load KPI data. Retrying…" | Error (red) | Manual dismiss |
| Approve all bulk | "[N] holiday requests approved — branches notified" | Success | 5s |

---

## 8. Empty States

| Condition | Illustration | Heading | Description | CTA |
|---|---|---|---|---|
| No calendar published yet | Calendar outline | "No group calendar published" | "Publish the group academic calendar to get started" | [Publish Calendar Update ↑] |
| All branches confirmed | Checkmark circle | "All branches calendar-confirmed" | "Every branch has confirmed the current group academic calendar" | — |
| No holiday requests pending | Checkmark circle | "No pending requests" | "No branch holiday or event requests are waiting for approval" | — |
| No conflicts | Checkmark circle | "No calendar conflicts" | "No conflicts detected in the group academic calendar" | — |
| No upcoming events (14 days) | Calendar outline | "No events in the next 14 days" | "No academic events are scheduled across any branch for the next two weeks" | [+ Add Event] |
| No PTMs scheduled | Calendar outline | "No PTMs scheduled this term" | "No Parent-Teacher Meetings have been scheduled for the current term" | [+ Add PTM] |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton screens: KPI bar (6 cards) + branch coverage table (5 skeleton rows) + upcoming events timeline (3 placeholder events) |
| Coverage / sync-status table load | Skeleton rows — 5 rows |
| Upcoming events timeline load | Vertical skeleton event placeholders — 3 items |
| Holiday approval queue load | Skeleton alert cards — 3 cards |
| PTM table load | Skeleton rows — 5 rows |
| Conflict list load | Skeleton alert cards — 3 cards |
| Year progress section load | Progress bar skeleton + stat row skeletons |
| Drawer open | Skeleton rows inside drawer body |
| Approve / reject button click | Spinner inside button + button disabled |
| Publish calendar modal confirm | Full-page overlay spinner with "Publishing calendar to [N] branches…" |
| KPI auto-refresh | Subtle shimmer over existing card values |
| Force sync confirm | Spinner inside [Confirm Force Sync] button + button disabled |

---

## 10. Role-Based UI Visibility

| Element | Cal Manager (G3) | CAO (G4) | Exam Controller (G3) | MIS Officer (G1) | All others (read access) |
|---|---|---|---|---|---|
| Page itself | ✅ Rendered (full) | ✅ Rendered (full) | ✅ Events + conflict sections | ✅ Read-only all | ✅ Events timeline only |
| Alert Banner | ✅ Shown | ✅ Shown | ✅ Shown | ✅ Shown | ✅ Shown |
| [Publish Calendar Update ↑] | ✅ Shown | ✅ Shown | ❌ Hidden | ❌ Hidden | ❌ Hidden |
| [+ Add Event] | ✅ Shown | ✅ Shown | ❌ Hidden | ❌ Hidden | ❌ Hidden |
| [Approve ✓] holiday request | ✅ Enabled | ✅ Enabled | ❌ Hidden | ❌ Hidden | ❌ Hidden |
| [Reject ✗] holiday request | ✅ Enabled | ✅ Enabled | ❌ Hidden | ❌ Hidden | ❌ Hidden |
| [Send Reminder] branch cal | ✅ Shown | ✅ Shown | ❌ Hidden | ❌ Hidden | ❌ Hidden |
| [Force Sync] | ✅ Shown | ✅ Shown | ❌ Hidden | ❌ Hidden | ❌ Hidden |
| [Send Notification Now] PTM | ✅ Shown | ✅ Shown | ❌ Hidden | ❌ Hidden | ❌ Hidden |
| [Cancel PTM] | ✅ Shown | ✅ Shown | ❌ Hidden | ❌ Hidden | ❌ Hidden |
| [Resolve →] conflict | ✅ Shown | ✅ Shown | ✅ Shown (read only — cannot apply resolution) | ❌ Hidden | ❌ Hidden |
| Conflict resolution — Apply | ✅ Enabled | ✅ Enabled | ❌ Read-only view | ❌ Hidden | ❌ Hidden |
| [+ Add PTM] | ✅ Shown | ✅ Shown | ❌ Hidden | ❌ Hidden | ❌ Hidden |
| Holiday request queue (section) | ✅ Full access | ✅ Full access | ❌ Hidden | ✅ Read (counts only) | ❌ Hidden |

> All UI visibility decisions made server-side in Django template. No client-side JS role checks.

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/acad/cal-manager/dashboard/` | JWT (G3+) | Full page data |
| GET | `/api/v1/group/{group_id}/acad/cal-manager/kpi-cards/` | JWT (G3+) | KPI card values (auto-refresh) |
| GET | `/api/v1/group/{group_id}/acad/cal-manager/coverage/` | JWT (G3+) | Calendar coverage — working days, holidays, branch confirmation |
| POST | `/api/v1/group/{group_id}/acad/cal-manager/publish/` | JWT (G3) | Publish calendar update to branches |
| POST | `/api/v1/group/{group_id}/acad/cal-manager/branches/{branch_id}/remind/` | JWT (G3) | Send confirmation reminder to branch |
| POST | `/api/v1/group/{group_id}/acad/cal-manager/branches/{branch_id}/force-sync/` | JWT (G3) | Force push group calendar to branch |
| GET | `/api/v1/group/{group_id}/acad/cal-manager/sync-status/` | JWT (G3+) | Branch calendar sync status table |
| GET | `/api/v1/group/{group_id}/acad/cal-manager/upcoming-events/` | JWT (G2+) | Upcoming events next 14 days |
| POST | `/api/v1/group/{group_id}/acad/cal-manager/events/` | JWT (G3) | Create new academic event |
| PATCH | `/api/v1/group/{group_id}/acad/cal-manager/events/{event_id}/` | JWT (G3) | Edit event |
| DELETE | `/api/v1/group/{group_id}/acad/cal-manager/events/{event_id}/` | JWT (G3) | Cancel/delete event |
| GET | `/api/v1/group/{group_id}/acad/cal-manager/approval-queue/` | JWT (G3+) | Holiday/event approval queue |
| GET | `/api/v1/group/{group_id}/acad/cal-manager/requests/{request_id}/` | JWT (G3+) | Holiday request detail + calendar impact |
| POST | `/api/v1/group/{group_id}/acad/cal-manager/requests/{request_id}/approve/` | JWT (G3) | Approve holiday request |
| POST | `/api/v1/group/{group_id}/acad/cal-manager/requests/{request_id}/reject/` | JWT (G3) | Reject holiday request with reason |
| POST | `/api/v1/group/{group_id}/acad/cal-manager/requests/bulk-approve/` | JWT (G3) | Bulk approve selected requests |
| GET | `/api/v1/group/{group_id}/acad/cal-manager/ptm-schedule/` | JWT (G3+) | PTM schedule table |
| POST | `/api/v1/group/{group_id}/acad/cal-manager/ptm/` | JWT (G3) | Create PTM |
| PATCH | `/api/v1/group/{group_id}/acad/cal-manager/ptm/{ptm_id}/` | JWT (G3) | Edit PTM |
| POST | `/api/v1/group/{group_id}/acad/cal-manager/ptm/{ptm_id}/notify/` | JWT (G3) | Send parent notification for PTM |
| POST | `/api/v1/group/{group_id}/acad/cal-manager/ptm/{ptm_id}/cancel/` | JWT (G3) | Cancel PTM |
| GET | `/api/v1/group/{group_id}/acad/cal-manager/conflicts/` | JWT (G3+) | Calendar conflicts list |
| GET | `/api/v1/group/{group_id}/acad/cal-manager/conflicts/{conflict_id}/` | JWT (G3+) | Conflict detail + resolution options |
| POST | `/api/v1/group/{group_id}/acad/cal-manager/conflicts/{conflict_id}/resolve/` | JWT (G3) | Apply conflict resolution |
| GET | `/api/v1/group/{group_id}/acad/cal-manager/year-progress/` | JWT (G2+) | Academic year progress data |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| KPI auto-refresh | `every 5m` | GET `/api/.../cal-manager/kpi-cards/` | `#kpi-bar` | `innerHTML` |
| Coverage section load | `load` | GET `/api/.../cal-manager/coverage/` | `#coverage-section` | `innerHTML` |
| Send calendar reminder | `click` | POST `/api/.../cal-manager/branches/{id}/remind/` | `#toast-container` | `afterbegin` |
| Force sync confirm | `click` | POST `/api/.../cal-manager/branches/{id}/force-sync/` | `#sync-status-section` | `innerHTML` |
| Sync status filter change | `change` | GET `/api/.../cal-manager/sync-status/?status={}&city={}` | `#sync-status-section` | `innerHTML` |
| Upcoming events filter | `change` | GET `/api/.../cal-manager/upcoming-events/?type={}&branch={}&status={}` | `#upcoming-events-section` | `innerHTML` |
| Open event drawer | `click` | GET `/api/.../cal-manager/events/{id}/` | `#drawer-body` | `innerHTML` |
| Publish event | `click` | POST `/api/.../cal-manager/events/` | `#upcoming-events-section` | `innerHTML` |
| Approval queue load | `load` | GET `/api/.../cal-manager/approval-queue/` | `#approval-queue-section` | `innerHTML` |
| Approve holiday request | `click` | POST `/api/.../cal-manager/requests/{id}/approve/` | `#approval-queue-section` | `innerHTML` |
| Open reject modal | `click` | — (modal trigger, no HTMX) | `#reject-modal` | `innerHTML` |
| Reject holiday request confirm | `click` | POST `/api/.../cal-manager/requests/{id}/reject/` | `#approval-queue-section` | `innerHTML` |
| Open request detail drawer | `click` | GET `/api/.../cal-manager/requests/{id}/` | `#drawer-body` | `innerHTML` |
| PTM filter change | `change` | GET `/api/.../cal-manager/ptm-schedule/?status={}&branch={}&notified={}` | `#ptm-section` | `innerHTML` |
| Send PTM notification | `click` | POST `/api/.../cal-manager/ptm/{id}/notify/` | `#toast-container` | `afterbegin` |
| Cancel PTM confirm | `click` | POST `/api/.../cal-manager/ptm/{id}/cancel/` | `#ptm-section` | `innerHTML` |
| Conflicts load | `load` | GET `/api/.../cal-manager/conflicts/` | `#conflicts-section` | `innerHTML` |
| Open conflict resolve drawer | `click` | GET `/api/.../cal-manager/conflicts/{id}/` | `#drawer-body` | `innerHTML` |
| Apply conflict resolution | `click` | POST `/api/.../cal-manager/conflicts/{id}/resolve/` | `#conflicts-section` | `innerHTML` |
| Year progress load | `load` | GET `/api/.../cal-manager/year-progress/` | `#year-progress-section` | `innerHTML` |
| Publish calendar update confirm | `click` | POST `/api/.../cal-manager/publish/` | `#coverage-section` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
