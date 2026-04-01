# 11 — Cultural Events Calendar

> **URL:** `/group/cultural/calendar/`
> **File:** `11-cultural-events-calendar.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Group Cultural Activities Head (Role 99, G3) · Group Sports Director (Role 97, G3) · Group NSS/NCC Coordinator (Role 100, G3)

---

## 1. Purpose

Provides the group-wide visual calendar of all cultural events planned, confirmed, ongoing, and completed across all branches for the current academic year (April 1 – March 31). Events covered include Annual Day ceremonies, inter-branch competitions, debates, quizzes, talent shows, cultural fests/melas, external competitions, workshops/seminars, and NSS/NCC cross-listed events.

The calendar serves two primary functions:

1. **Cultural Head (Role 99)** uses it as the master scheduling and management console — creating events, assigning coordination, managing venue and branch participation, and tracking completion status across the group's 5–50 branches. Expected volume: 15–40 cultural events per academic year.

2. **Sports Director (Role 97)** and **NSS/NCC Coordinator (Role 100)** have view-only access specifically to prevent scheduling conflicts. The calendar can render a cross-calendar overlay showing sports events (from Page 06 — Sports Events Calendar) alongside cultural events so the Cultural Head can detect date clashes before confirming new events.

Three view modes are available: Month (default), Week, and List. All three share the same underlying event dataset and filters; the view preference is persisted in the user's browser session. Scale: 15–40 cultural events per AY; across up to 50 branches; events span 1–5 days each.

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Cultural Activities Head | 99 | G3 | Full — view, create, edit, cancel, export | Primary owner of this calendar |
| Sports Director | 97 | G3 | View only — all event types visible | Read access to detect scheduling conflicts with sports calendar |
| NSS/NCC Coordinator | 100 | G3 | View only — all events; NSS/NCC events highlighted | No edit capability; read for coordination awareness |
| Sports Coordinator | 98 | G3 | No access | Redirected to own dashboard |
| Library Head | 101 | G2 | No access | No cultural calendar access |
| Branch Cultural Teacher | Branch staff | Branch | No access to this group page | Creates events via branch portal only |
| All other roles | — | — | No access | Redirected to own dashboard |

> **Access enforcement:** Django decorator `@require_role(['cultural_head'])` on all write endpoints. `@require_role(['cultural_head', 'sports_director', 'nss_ncc_coordinator'])` on all read endpoints. Roles 97 and 100 receive server-rendered pages with all action controls omitted. The `[+ New Event]`, `[Edit]`, and `[Cancel Event]` elements are conditionally rendered via Django template context variable `can_write`.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Sports & Extra-Curricular  ›  Cultural Events Calendar
```

### 3.2 Page Header
```
Cultural Events Calendar                     [+ New Event]  [Export ↓]  [⚙ View Options]
Group Cultural Activities Head — [Officer Name]
AY [academic year]  ·  [N] Total Events  ·  [N] Confirmed  ·  [N] Upcoming  ·  [N] Completed
```

`[+ New Event]` — opens `cultural-event-create` drawer. Role 99 only; hidden for Roles 97 and 100.
`[Export ↓]` — dropdown: Export to PDF / Export to XLSX. Available to all permitted roles.
`[⚙ View Options]` — panel: toggles cross-calendar sports overlay (fetch from Page 06 API); toggles NSS/NCC event highlight ring.

View mode switcher (inline pill-style, below header): `[Month]  [Week]  [List]` — controls calendar render mode; active mode underlined/filled; HTMX-driven swap.

### 3.3 Alert Banners (conditional)

Stacked above the KPI bar. Each banner is individually dismissible for the session.

| Condition | Banner Text | Severity |
|---|---|---|
| Event with registration deadline in < 3 days | "[N] inter-branch competition(s) have registration deadlines within 3 days. Act now." | Red |
| Events with no venue confirmed in next 7 days | "[N] confirmed event(s) in the next 7 days have no venue assigned. Confirm venues immediately." | Red |
| Branches with no cultural event this term > 0 | "[N] branch(es) have no cultural event scheduled this term. Consider planning coverage." | Amber |
| Inter-branch competition registration deadline within 7 days | "[N] competition(s) have registration deadlines within 7 days. Review pending registrations." | Amber |
| Proposed or newly saved event date clashes with a group sports event | "Date conflict detected with sports event '[Name]' on [date]. Review before confirming." | Red |
| Events cancelled this month > 3 | "[N] events cancelled this month. Review operational notes." | Amber |
| No events scheduled in next 30 days | "No cultural events are scheduled in the next 30 days." | Blue (Info) |
| All KPIs healthy — no actionable alerts | No banner shown | — |

---

## 4. KPI Summary Bar

Five metric cards displayed horizontally, refreshed on page load and every 5 minutes via HTMX polling.

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Events Scheduled This AY | Total event records for current AY where `status != Cancelled` | `COUNT(*) WHERE academic_year = current AND status != 'cancelled'` | Indigo (neutral) | `#kpi-events-ay` |
| 2 | Events This Month | Count where `start_date` falls in current calendar month | `COUNT(*) WHERE MONTH(start_date) = current_month AND YEAR(start_date) = current_year` | Indigo (neutral) | `#kpi-events-month` |
| 3 | Branches with No Cultural Event This Term | Count of branches with zero confirmed/completed events in current academic term | `COUNT(branches) WHERE event_count_this_term = 0` | Red if > 20% of total branches; Amber if 1–20%; Green if 0 | `#kpi-no-event-branches` |
| 4 | Competitions Pending Registration Deadline | Count of Inter-Branch Competition events where `registration_deadline` within 14 days and `status` in Planned/Confirmed | `COUNT(*) WHERE event_type='inter_branch_competition' AND registration_deadline BETWEEN today AND today+14 AND status IN ('planned','confirmed')` | Red if > 0; Green if 0 | `#kpi-reg-deadline` |
| 5 | Upcoming Events (Next 30 Days) | Count of events with `start_date` in next 30 days and `status` in Planned/Confirmed | `COUNT(*) WHERE start_date BETWEEN today AND today+30 AND status IN ('planned','confirmed')` | Amber if 0; Indigo if > 0 | `#kpi-upcoming` |

```
┌──────────────────────┐ ┌──────────────────────┐ ┌──────────────────────┐ ┌──────────────────────┐ ┌──────────────────────┐
│  Events This AY      │ │  Events This Month   │ │  No Event Branches   │ │  Reg. Deadline Soon  │ │  Upcoming (30 Days)  │
│         28           │ │          4           │ │          3           │ │          2           │ │          6           │
│     ● Indigo         │ │      ● Indigo        │ │       ● Amber        │ │       ● Red          │ │       ● Indigo       │
└──────────────────────┘ └──────────────────────┘ └──────────────────────┘ └──────────────────────┘ └──────────────────────┘
```

**KPI bar HTMX:** `<div id="cultural-kpi-bar" hx-get="/api/v1/cultural/calendar/kpi-summary/" hx-trigger="load, every 300s" hx-swap="innerHTML" hx-indicator="#kpi-spinner">`. Each card is rendered as a shimmer skeleton on first load until the API response arrives.

---

## 5. Sections

### 5.1 View: Month (Default)

Full-month grid calendar. Each day cell shows event chips for events starting or spanning that day.

| Element | Behaviour |
|---|---|
| Day cells | 7-column grid; current day highlighted with indigo ring border |
| Event chip | Coloured pill showing event name (truncated at 22 chars) using event type colour (see §5.4). Click opens `cultural-event-detail` drawer |
| Overflow indicator | If > 3 chips on a day: first 2 shown + `+N more` link; clicking expands a popover listing all events for that day with type badges and times |
| Cross-calendar overlay | When enabled via `[⚙ View Options]`, sports events from Page 06 render as grey-outlined ghost chips behind cultural chips |
| Month navigation | `[‹ Previous]` and `[Next ›]` buttons; `[Today]` shortcut. HTMX swaps the calendar grid fragment only; header stat line updates in place |
| Empty day click (Role 99 only) | Clicking an empty day cell triggers `cultural-event-create` drawer with the clicked date pre-filled as Start Date |

### 5.2 View: Week

7-day hourly time grid. Events are positioned as blocks based on `start_time` and duration.

| Element | Behaviour |
|---|---|
| Time axis | 06:00–22:00, 30-minute slots on the left |
| All-day events | Top stripe above the hourly grid; colour-coded by type |
| Timed event blocks | Width proportional to duration; colour-coded by type; click opens detail drawer |
| Multi-day events | Shown as a spanning banner across the top stripe for each day in range |
| Week navigation | `[‹ Prev Week]` `[This Week]` `[Next Week ›]`; HTMX swap of grid fragment only |
| Events with no time set | Rendered as all-day blocks in the top stripe |

### 5.3 View: List

Tabular view of all events matching current filters. Server-side pagination: 25 rows per page.

| Column | Source Field | Sortable | Notes |
|---|---|---|---|
| Date | `start_date` (+ `end_date` if multi-day: "DD MMM – DD MMM YYYY") | ▲▼ | Red text if `start_date` has passed and `status = Planned` (overdue to confirm) |
| Event Name | `event_name` | ▲▼ | Clickable text — opens `cultural-event-detail` drawer |
| Type | `event_type` | ▲▼ | Colour-coded badge (see §5.4) |
| Activity Category | `activity_category` | ▲▼ | Pill: Arts / Music / Literary / Sports-Cultural / General |
| Branches Involved | `branch_count` or "All" | ▲▼ | Count link; hover tooltip lists branch names |
| Venue | `venue_name` | — | Truncated at 30 chars; full value in tooltip; "TBD" if not set |
| Status | `status` | ▲▼ | Colour-coded pill (see §5.5) |
| Actions | — | — | `[View]` · `[Edit]` (Role 99 only) · `[Cancel]` (Role 99 only; not shown if Completed or Cancelled) |

**Pagination controls:** `« Previous  Page N of N  Next »` · Rows-per-page selector: 25 / 50 / 100.

**Default sort:** `start_date` ascending (nearest upcoming first).

### 5.4 Event Type Colour Map

| Event Type | Calendar Chip Colour | Badge Classes (Tailwind) |
|---|---|---|
| Annual Day | Gold | `bg-amber-100 text-amber-800 border-amber-300` |
| Inter-Branch Competition | Blue | `bg-blue-100 text-blue-800 border-blue-300` |
| Debate / Quiz | Teal | `bg-teal-100 text-teal-800 border-teal-300` |
| Cultural Fest / Mela | Purple | `bg-violet-100 text-violet-800 border-violet-300` |
| External Competition | Orange | `bg-orange-100 text-orange-800 border-orange-300` |
| Workshop / Seminar | Grey | `bg-gray-100 text-gray-700 border-gray-300` |
| NSS/NCC Event | Green | `bg-green-100 text-green-800 border-green-300` |

NSS/NCC events also render with a small green circle indicator in the top-right corner of their chip when the NSS/NCC highlight is active via `[⚙ View Options]`.

### 5.5 Event Status Colour Coding

| Status | Pill Colour | Description |
|---|---|---|
| Planned | `bg-amber-100 text-amber-700` | Event created; details may be incomplete; not yet confirmed |
| Confirmed | `bg-blue-100 text-blue-700` | Confirmed; venue and branches assigned; preparation underway |
| Ongoing | `bg-indigo-100 text-indigo-700` | Currently in progress (`start_date` ≤ today ≤ `end_date`) |
| Completed | `bg-green-100 text-green-700` | Event concluded; results and report may be added |
| Cancelled | `bg-red-100 text-red-700` | Cancelled; `cancel_reason` stored; branches notified |

### 5.6 Filter Drawer (Slide-In, 360 px)

Trigger: `[Filters ▾]` button in list view toolbar. In month/week views, a filter icon (funnel) opens the same drawer.

| Filter | Control | Options |
|---|---|---|
| Branch | Multi-select checkbox list | All branches in group; searchable |
| Event Type | Multi-select checkbox list | All 7 types from §5.4 |
| Activity Category | Multi-select checkbox list | Arts / Music / Literary / Sports-Cultural / General |
| Status | Multi-select checkbox list | Planned / Confirmed / Ongoing / Completed / Cancelled |
| Date Range | Dual date picker | `start_from` and `start_to` applied to `start_date` |

Active filters display as removable chips below the toolbar. `[Reset All Filters]` clears all chips and refreshes the view.

---

## 6. Drawers & Modals

### 6.1 `cultural-event-create` Drawer — 680 px, right-slide

**Trigger:** `[+ New Event]` header button, or clicking an empty day cell in any calendar view. Role 99 only.

**Header:**
```
New Cultural Event
Save as Draft at any time. Confirm the event when all details are finalised.
```

**Tab 1 — Details**

| Field | Type | Required | Validation / Notes |
|---|---|---|---|
| Event Name | Text input | Yes | Min 3, max 150 characters |
| Event Type | Select | Yes | Annual Day / Inter-Branch Competition / Debate+Quiz / Cultural Fest+Mela / External Competition / Workshop+Seminar / NSS+NCC Event |
| Activity Category | Select | Yes | Arts / Music / Literary / Sports-Cultural / General |
| Start Date | Date picker | Yes | Cannot be before today for new events |
| End Date | Date picker | Yes | Must be ≥ Start Date; defaults to same as Start Date |
| Start Time | Time picker | No | Optional; if omitted event renders as all-day |
| End Time | Time picker | No | If Start Time set, End Time must be after Start Time on End Date |
| Description | Textarea | No | Max 500 characters; character counter shown |
| Status | Select | Yes | Default: Planned; options: Planned / Confirmed |
| Registration Deadline | Date picker | Conditional | Shown only when Event Type = Inter-Branch Competition; must be ≤ Start Date |

On change of Start Date or End Date: HTMX call to `/api/v1/cultural/calendar/conflict-check/?start_date=X&end_date=Y` returning any overlapping sports events as an inline warning banner inside the drawer (see §13.8).

**Tab 2 — Branches**

| Field | Type | Required | Validation / Notes |
|---|---|---|---|
| Applies To | Radio buttons | Yes | All Branches / Selected Branches |
| Select Branches | Multi-select checkbox list | Conditional | Required if "Selected Branches" chosen; lists all active branches in group; searchable |
| Host Branch | Select | No | Single select from group branches; "No specific host" default option |

**Tab 3 — Venue**

| Field | Type | Required | Validation / Notes |
|---|---|---|---|
| Venue Name | Text input | No | Max 150 characters |
| Venue Type | Select | No | Branch Auditorium / External Hall / Open Ground / Online / Other |
| Address | Textarea | No | Max 300 characters; hidden when Venue Type = Online |
| Capacity | Number | No | Positive integer |
| Venue Confirmed | Toggle | No | Default off; when on, a "Venue Confirmed" badge appears on the calendar chip |

**Tab 4 — Coordination**

| Field | Type | Required | Validation / Notes |
|---|---|---|---|
| Coordinator Assigned | Search + select | No | Searches staff records across all group branches |
| Budget Allocated (₹) | Currency input | No | Positive decimal, 2 dp |
| Sponsor | Text input | No | Max 100 characters |
| Live Stream? | Toggle | No | Default off; when on, a streaming icon renders on the calendar chip |
| Notes | Textarea | No | Max 500 characters; internal only; not visible to branch roles |

**Footer:** `[Cancel]`  `[Save as Draft]`  `[Save & Confirm Event]`

`[Save as Draft]` → saves with `status = Planned`. `[Save & Confirm Event]` → saves with `status = Confirmed`. Both POST to create endpoint. Both buttons show spinner and become disabled during submission.

---

### 6.2 `cultural-event-detail` Drawer — 680 px, right-slide

**Trigger:** Clicking an event chip in any calendar view, or `[View]` button in list view.

**Header:**
```
[Event Name]                                          [Edit ✎]  [Cancel Event]  [×]
[Event Type badge]  ·  [Activity Category pill]  ·  Status: [status pill]
[Start Date] – [End Date]  ·  [Venue Name] or "Venue TBD"
```

`[Edit ✎]` — opens event fields inline within drawer for editing (same fields as create drawer, pre-populated). Role 99 only.
`[Cancel Event]` — opens `cancel-event` modal. Role 99 only; hidden if status = Cancelled or Completed.

**Tab 1 — Overview**

Two-column metadata layout:

| Field | Notes |
|---|---|
| Event Name | — |
| Event Type | Colour badge |
| Activity Category | Pill |
| Start / End Date | Date range |
| Start / End Time | Shown if set; "All Day" otherwise |
| Status | Colour pill |
| Description | Full text; scrollable if long |
| Applies To | "All Branches" or list of branch names |
| Host Branch | Branch name or "None" |
| Venue Name / Type / Address / Capacity | Full venue block |
| Venue Confirmed | Badge or "Not Confirmed" |
| Coordinator Assigned | Name + role |
| Budget Allocated | ₹ amount |
| Sponsor | Sponsor name if set |
| Live Stream | "Yes" / "No" |
| Registration Deadline | Date (Inter-Branch Competition only) |
| Notes | Full text; scrollable |
| Created By / Created At | Audit fields |
| Last Updated By / At | Audit fields |

**Tab 2 — Branches**

Table of branch participation for this event:

| Column | Notes |
|---|---|
| Branch Name | Link to branch profile page |
| Contact Person | Name + title at branch |
| Registered Teams / Participants | Count; "N/A" for non-competitive events |
| Registration Status | Badge: Registered / Not Registered / Declined |
| Actions | `[View Details]` — expands an inline row to show team/participant names and contact details |

"Applies To: All Branches" message shown above table when event is group-wide. Role 99 sees all rows; Roles 97 and 100 see read-only table.

**Tab 3 — Results**

Shown for all statuses but editable only when `status = Completed`.

| Column | Notes |
|---|---|
| Category / Sub-Contest | Name of the competition category |
| Position | 1st / 2nd / 3rd — rendered as Gold / Silver / Bronze badge |
| Branch | Winning branch name |
| Student / Team Name | Participant name(s) |
| Award / Trophy | Award name if applicable |

`[+ Add Result Entry]` button — Role 99 only; `status` must be Completed. Opens inline form within the tab.

**Tab 4 — Media**

Gallery-style display:
- Photo URLs (Cloudflare R2 hosted) shown as 100×100 thumbnail grid; click opens full-size in new tab
- Video URLs (YouTube / Vimeo) shown as cards with thumbnail preview (via YouTube oEmbed)
- `[+ Add Media Link]` — URL text input + type selector (Photo URL / Video URL) + optional caption; saved via POST; Role 99 only; max 20 links per event

**Tab 5 — Report**

| Field | Type | Notes |
|---|---|---|
| Attendance Count | Number input | Role 99; editable post-event |
| Highlights | Textarea | Max 1000 chars |
| Outcomes | Textarea | Max 1000 chars |
| Report Status | Badge | "Not Generated" / "Generated" |
| Generate PDF Report | Button | Role 99; event must be Completed; triggers async job; download link replaces button when ready |

---

### 6.3 `cancel-event` Modal — 420 px, centred

**Trigger:** `[Cancel Event]` button in event detail drawer header. Role 99 only.

**Header:**
```
Cancel Cultural Event
This action cannot be undone. Provide a reason before proceeding.
```

| Field | Type | Required | Validation |
|---|---|---|---|
| Cancellation Reason | Textarea | Yes | Min 20 characters |
| Notify Branches | Checkbox | — | Default checked; sends in-app notification to all participating branch contacts |

**Footer:** `[Go Back]`  `[Confirm Cancellation]`

On confirm: event `status` → Cancelled; `cancel_reason` and `cancelled_by` recorded; notification dispatched if Notify Branches is checked. [Confirm Cancellation] shows spinner and becomes disabled during submit.

---

## 7. Charts

Charts are placed below the KPI bar and above the calendar, in a two-column row. A `[▸ Hide Charts]` / `[▾ Show Charts]` toggle collapses this row. Preference is stored in the user's browser session.

### 7.1 Cultural Events by Type — Donut Chart

| Property | Value |
|---|---|
| Chart type | Donut (Chart.js 4.x) |
| Title | "Cultural Events by Type — [Current AY]" |
| Data | Count of non-Cancelled events per `event_type` for current AY |
| Segment colours | Match event type colours from §5.4 |
| Legend | Right-side legend with event type name and count |
| Tooltip | "[Event Type]: [N] events ([N]%)" on hover |
| Centre label | Total active event count |
| Empty state | "No events recorded for the current academic year." |
| Export | PNG export button in top-right corner of chart card |
| API endpoint | `GET /api/v1/cultural/calendar/charts/by-type/` |
| HTMX | `<div id="chart-by-type" hx-get="/api/v1/cultural/calendar/charts/by-type/" hx-trigger="load" hx-swap="innerHTML" hx-indicator="#chart-type-spinner">` |

### 7.2 Monthly Event Distribution — Stacked Bar Chart

| Property | Value |
|---|---|
| Chart type | Vertical stacked bar (Chart.js 4.x) |
| Title | "Monthly Event Distribution — [Current AY]" |
| X-axis | 12 months of current AY (Apr – Mar), abbreviated |
| Y-axis | Event count |
| Stacked series | One series per event type, using §5.4 colours |
| Tooltip | Shows breakdown per type for that month on hover |
| Annotation | Current month highlighted with a light indigo background band |
| Empty state | "No events recorded for the current academic year." |
| Export | PNG export button in top-right corner of chart card |
| API endpoint | `GET /api/v1/cultural/calendar/charts/monthly-distribution/` |
| HTMX | `<div id="chart-monthly-dist" hx-get="/api/v1/cultural/calendar/charts/monthly-distribution/" hx-trigger="load" hx-swap="innerHTML" hx-indicator="#chart-monthly-spinner">` |

---

## 8. Toast Messages

| Action | Toast Text | Type |
|---|---|---|
| Event created — Planned | "Cultural event '[Name]' saved as Planned." | Success |
| Event created — Confirmed | "Cultural event '[Name]' confirmed and added to calendar." | Success |
| Event updated | "Changes to '[Name]' saved." | Success |
| Event cancelled | "Event '[Name]' cancelled. [N] branch(es) notified." | Success |
| Scheduling conflict detected | "Date conflict with sports event '[Sports Event Name]'. Review before confirming." | Warning |
| Media link added | "Media link added to '[Name]'." | Success |
| Export complete | "Calendar exported to [format]." | Success |
| PDF report generation started | "Generating PDF report for '[Name]'. Download link will appear shortly." | Info |
| PDF report ready | "PDF report for '[Name]' is ready." (with download link) | Success |
| Required field missing on save | "Please complete all required fields before saving." | Error |
| Network / server error | "Could not save event. Please try again." | Error |
| Branch notification dispatch failed | "Event cancelled, but branch notifications could not be sent. Retry from event detail." | Warning |

---

## 9. Empty States

| Context | Icon | Heading | Sub-text | Action |
|---|---|---|---|---|
| No events in current AY | `calendar` | "No Cultural Events Scheduled" | "No cultural events have been created for this academic year. Start planning now." | `[+ New Event]` (Role 99 only) |
| No events match filters | `funnel` | "No Events Match Filters" | "Try adjusting your filters or reset to see all events." | `[Reset Filters]` |
| Month view — empty month | `calendar-days` | "Nothing Scheduled This Month" | "No cultural events are scheduled for [Month YYYY]." | `[+ New Event]` (Role 99 only) |
| Week view — empty week | `calendar` | "No Events This Week" | "No cultural events scheduled for this week." | `[+ New Event]` (Role 99 only) |
| Results tab — no entries | `trophy` | "No Results Recorded" | "Results can be added once the event is marked Completed." | `[+ Add Result Entry]` (Role 99, Completed status only) |
| Media tab — no links | `photo` | "No Media Added" | "Add photo or video links to document this event." | `[+ Add Media Link]` (Role 99 only) |
| Branches tab — none assigned | `building-office` | "No Branches Assigned" | "This event has not been assigned to any branches yet." | `[Edit]` (Role 99 only) |
| Charts — no data | `chart-bar` | "No data available" | "No event data is available for the selected period." | — |

---

## 10. Loader States

| Context | Loader Behaviour |
|---|---|
| Initial page load | KPI bar: 5 shimmer cards. Charts row: 2 shimmer rectangles (donut placeholder + bar placeholder). Calendar / table area: shimmer skeleton matching selected view mode |
| Month view navigation | Calendar grid replaced by full shimmer grid; HTMX swaps real content on response |
| Week view navigation | Hourly grid replaced by shimmer rows; HTMX swap on response |
| List view filter or search change | Table rows replaced by 6 shimmer rows with a 20 px indigo spinner centred below toolbar |
| Event detail drawer opening | Drawer slides in with shimmer tab bar and shimmer content blocks per tab; real content replaces on API response |
| Conflict check on date change in create drawer | 16 px inline spinner beside the date field; conflict alert area shimmers until response returns |
| [Save as Draft] / [Save & Confirm Event] form submit | Button disabled + spinner inside button label |
| [Confirm Cancellation] submit | Button disabled + "Cancelling…" + spinner; modal closes on success |
| PDF report generation | Button transitions to disabled + "Generating…" + spinner; re-enables and shows download link when job complete |
| Export | `[Export ↓]` transitions to disabled + "Preparing…" + spinner; re-enables on file ready |
| KPI auto-refresh (every 300s) | Cards show a subtle pulse animation; values update in place without full shimmer |
| Chart initial load | Per-chart shimmer rectangle with centred spinner |

---

## 11. Role-Based UI Visibility

| UI Element | Role 99 (Cultural Head) | Role 97 (Sports Director) | Role 100 (NSS/NCC Coord) | All Others |
|---|---|---|---|---|
| KPI Summary Bar | Full | Full | Full | Hidden |
| Charts row | Visible | Visible | Visible | Hidden |
| Month / Week / List views | All three | All three | All three | Hidden |
| `[+ New Event]` button | Visible | Hidden | Hidden | Hidden |
| `[Export ↓]` button | Visible | Visible | Visible | Hidden |
| `[⚙ View Options]` | Visible | Visible | Visible | Hidden |
| Filter drawer | Full access | Full access | Full access | Hidden |
| Event chip click → detail drawer | Visible | Visible | Visible | Hidden |
| `[Edit ✎]` in detail drawer | Visible | Hidden | Hidden | Hidden |
| `[Cancel Event]` in detail drawer | Visible | Hidden | Hidden | Hidden |
| Branches tab — Actions column | Visible | Hidden | Hidden | Hidden |
| Results tab — `[+ Add Result Entry]` | Visible (Completed only) | Hidden | Hidden | Hidden |
| Media tab — `[+ Add Media Link]` | Visible | Hidden | Hidden | Hidden |
| Report tab — `[Generate PDF Report]` | Visible | Hidden | Hidden | Hidden |
| Alert banners | Full | Full | Full | Hidden |
| Cross-calendar sports overlay toggle | Visible | Visible | Hidden | Hidden |

---

## 12. API Endpoints

### 12.1 List Events (Calendar and List Views)
```
GET /api/v1/cultural/calendar/events/
```

| Query Parameter | Type | Description |
|---|---|---|
| `view` | string | `month` · `week` · `list` — affects response structure |
| `year` | integer | Calendar year (e.g. 2025) |
| `month` | integer | 1–12; used when `view=month` |
| `week_start` | date (YYYY-MM-DD) | Monday of target week; used when `view=week` |
| `branch` | string (multi) | Filter by branch ID(s); comma-separated |
| `event_type` | string (multi) | Filter by event type slug(s) |
| `activity_category` | string (multi) | `arts` · `music` · `literary` · `sports_cultural` · `general` |
| `status` | string (multi) | `planned` · `confirmed` · `ongoing` · `completed` · `cancelled` |
| `start_from` | date | List view range start (applied to `start_date`) |
| `start_to` | date | List view range end |
| `search` | string | Searches `event_name` |
| `page` | integer | Default 1; list view only |
| `page_size` | integer | 25 · 50 · 100; default 25; list view only |
| `ordering` | string | `start_date` · `-start_date` · `event_name` · `status` |
| `include_sports_overlay` | boolean | When `true`, response includes `sports_events` array from Page 06 data for cross-calendar overlay |

**Response (list view):** `{ count, next, previous, results: [...] }`.
**Response (month/week view):** `{ events: [...] }` — no pagination; all events in the requested period.

### 12.2 Create Event
```
POST /api/v1/cultural/calendar/events/
```
Body: JSON — all fields from create drawer §6.1. Role 99 only.
Response: 201 Created — full event object.

### 12.3 Retrieve Event Detail
```
GET /api/v1/cultural/calendar/events/{event_id}/
```
Response: 200 OK — full event object including branches, results, media links, report fields, audit trail.

### 12.4 Update Event
```
PATCH /api/v1/cultural/calendar/events/{event_id}/
```
Body: JSON partial update. Role 99 only. Events with `status = cancelled` return HTTP 403.
Response: 200 OK — updated event object.

### 12.5 Cancel Event
```
POST /api/v1/cultural/calendar/events/{event_id}/cancel/
```
Body: `{ "cancel_reason": "string", "notify_branches": true }`. Role 99 only.
Response: 200 OK — updated event with `status = cancelled`.

### 12.6 Add Media Link
```
POST /api/v1/cultural/calendar/events/{event_id}/media/
```
Body: `{ "media_type": "photo|video", "url": "https://...", "caption": "optional" }`. Role 99 only.
Response: 201 Created — media link object.

### 12.7 Add Result Entry
```
POST /api/v1/cultural/calendar/events/{event_id}/results/
```
Body: `{ "category": "string", "position": 1, "branch_id": "string", "participant_name": "string", "award": "optional" }`. Role 99 only; event must have `status = completed`.
Response: 201 Created — result entry object.

### 12.8 Scheduling Conflict Check
```
GET /api/v1/cultural/calendar/conflict-check/
```

| Query Parameter | Type | Description |
|---|---|---|
| `start_date` | date (YYYY-MM-DD) | Proposed event start |
| `end_date` | date (YYYY-MM-DD) | Proposed event end |
| `exclude_event_id` | string | Optional; omit current event when editing to avoid self-conflict |

Response: `{ "has_conflict": bool, "conflicting_sports_events": [ { "id", "name", "start_date", "end_date" } ] }`.

### 12.9 KPI Summary
```
GET /api/v1/cultural/calendar/kpi-summary/
```
Query: `academic_year` (optional; defaults to current AY, e.g. `2025-26`).
Response: `{ "events_this_ay": N, "events_this_month": N, "no_event_branches": N, "reg_deadline_soon": N, "upcoming_30_days": N }`.

### 12.10 Chart Data
```
GET /api/v1/cultural/calendar/charts/by-type/
GET /api/v1/cultural/calendar/charts/monthly-distribution/
```
Both accept optional `academic_year` query parameter.
`by-type` response: `{ "labels": [...], "data": [...] }`.
`monthly-distribution` response: `{ "months": [...], "series": [ { "type": "...", "data": [...] } ] }`.

### 12.11 Export
```
GET /api/v1/cultural/calendar/events/export/
```
Query: all filter params from §12.1 + `format` (`pdf` · `xlsx`).
Response: File download (`Content-Disposition: attachment`).

### 12.12 Generate Event PDF Report
```
POST /api/v1/cultural/calendar/events/{event_id}/report/generate/
```
Role 99 only; event must be Completed. Response: 202 Accepted — `{ "job_id": "string" }`.
Poll status: `GET /api/v1/cultural/calendar/events/{event_id}/report/status/` → `{ "status": "pending|processing|ready|failed", "download_url": "..." }`.

---

## 13. HTMX Patterns

| Pattern | Trigger Element | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI bar load + auto-refresh | `<div id="cultural-kpi-bar">` | GET `/api/v1/cultural/calendar/kpi-summary/` | `#cultural-kpi-bar` | `innerHTML` | `hx-trigger="load, every 300s"`; shimmer on first load |
| Chart 7.1 (by type) load | `<div id="chart-by-type">` | GET `/api/v1/cultural/calendar/charts/by-type/` | `#chart-by-type` | `innerHTML` | `hx-trigger="load"`; shimmer until response |
| Chart 7.2 (monthly dist) load | `<div id="chart-monthly-dist">` | GET `/api/v1/cultural/calendar/charts/monthly-distribution/` | `#chart-monthly-dist` | `innerHTML` | `hx-trigger="load"`; shimmer until response |
| Month view calendar load | `<div id="cultural-month-calendar">` | GET `/api/v1/cultural/calendar/events/?view=month&year={y}&month={m}` | `#cultural-month-calendar` | `innerHTML` | `hx-trigger="load"` |
| Month navigation — previous | `<button>‹ Previous</button>` | GET `/api/v1/cultural/calendar/events/?view=month&year={prev_y}&month={prev_m}` | `#cultural-month-calendar` | `innerHTML` | `hx-trigger="click"` |
| Month navigation — next | `<button>Next ›</button>` | GET `/api/v1/cultural/calendar/events/?view=month&year={next_y}&month={next_m}` | `#cultural-month-calendar` | `innerHTML` | `hx-trigger="click"` |
| List view search (debounced) | `<input id="search-input">` | GET `/api/v1/cultural/calendar/events/?view=list` | `#cultural-event-table` | `innerHTML` | `hx-trigger="keyup changed delay:400ms"`; includes active filters |
| List view filter application | Filter selects | GET `/api/v1/cultural/calendar/events/?view=list` | `#cultural-event-table` | `innerHTML` | `hx-trigger="change"`; includes search input and other filters |
| Pagination (list view) | Pagination buttons | GET `/api/v1/cultural/calendar/events/?view=list&page={n}` | `#cultural-event-table` | `innerHTML` | `hx-trigger="click"` |
| Event detail drawer open | Event chip / [View] button | GET `/htmx/cultural/calendar/events/{event_id}/detail/` | `#drawer-container` | `innerHTML` | `hx-trigger="click"` |
| Detail drawer tab switch (lazy load) | Tab buttons | GET `/htmx/cultural/calendar/events/{event_id}/tab/{tab_slug}/` | `#drawer-tab-content` | `innerHTML` | `hx-trigger="click"`; Overview pre-fetched on open |
| Create event form submit | `<form id="cultural-event-create-form">` | POST `/api/v1/cultural/calendar/events/` | `#cultural-event-table` | `innerHTML` | `hx-encoding="application/json"`; `hx-on::after-request="closeDrawer(); showToast(event); refreshKPI(); refreshCalendar();"` |
| Scheduling conflict check on date change | `<input name="start_date">` | GET `/api/v1/cultural/calendar/conflict-check/` | `#conflict-alert-area` | `innerHTML` | `hx-trigger="change"`; `hx-include="[name='end_date']"`; returns empty fragment if no conflict |
| Cancel event modal submit | `<form>` in cancel-event modal | POST `/api/v1/cultural/calendar/events/{event_id}/cancel/` | `#cultural-event-table` | `innerHTML` | `hx-encoding="application/json"`; `hx-on::after-request="closeModal(); showToast(event); refreshKPI(); refreshCalendar();"` |

---

*Page spec version: 1.1 · Last updated: 2026-03-21*
