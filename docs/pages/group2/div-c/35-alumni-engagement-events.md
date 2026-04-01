# Page 35: Alumni Engagement Events

**URL:** `/group/adm/alumni/events/`
**Template:** `portal_base.html` (light theme)
**Division:** C — Group Admissions
**Module:** Alumni

---

## 1. Purpose

Alumni engagement events are the cornerstone of a living alumni relationship program — they transform a database of former students into an active community of advocates, mentors, and referral sources. This page manages the full lifecycle of every alumni-facing event organized by the group, from intimate career talks conducted at a single branch to flagship annual meets that draw hundreds of alumni from across the country. The Alumni Relations Manager uses this page to plan events, build invitation lists, collect RSVPs, manage event-day logistics, and track post-event follow-up actions that sustain the relationship momentum.

Events serve a dual strategic purpose that the Admissions Director must appreciate: alumni engagement is not purely a relationship exercise, it is an admissions funnel multiplier. A well-attended alumni felicitation ceremony for JEE rankers creates social media content, generates word-of-mouth in the community, and motivates current alumni to refer prospects who aspire to similar achievements. A career talk by a successful alumnus in front of current students and their parents is a live testimonial worth more than any paid advertisement. The Alumni Relations Manager therefore plans events with both community-building and admissions amplification in mind, and this page surfaces both dimensions through its engagement metrics and referral-generation tracking.

The budget tracking function within this page reflects a reality of institutional administration: alumni events cost money, and that cost must be justified. The event budget tracker captures estimated versus actual spend per event, allowing the group to calculate a return on investment for the events program. When an annual alumni meet generates 50 new referrals that convert at 40%, the cost-per-enrollment from that event can be compared to the cost-per-enrollment from paid advertising — and the alumni program almost always wins. This page provides the data to make that argument.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Alumni Relations Manager (28) | G3 | Full CRUD — create, edit, cancel, manage RSVPs, mark attendance, process budget | Primary owner |
| Group Admissions Director (23) | G3 | View all + approve events where estimated budget exceeds configured threshold | Strategic oversight and budget approval |
| Group Marketing Director | G3 | View all + promote events (social sharing, push notifications) | Marketing collaboration role |
| Group Admission Coordinator (24) | G3 | View-only | Awareness of upcoming events |

Access enforcement: All views protected with `@login_required` and `@role_required(['alumni_manager', 'admissions_director', 'marketing_director', 'admission_coordinator'])`. Budget approval gate enforced in view: `if event.estimated_budget > group.alumni_event_approval_threshold and not request.user.has_perm('approve_event_budget'): raise PermissionDenied` before saving an event with high budget.

---

## 3. Page Layout

### 3.1 Breadcrumb
`Group Portal → Admissions → Alumni → Engagement Events`

### 3.2 Page Header
**Title:** Alumni Engagement Events
**Subtitle:** Plan, manage, and track alumni events across all branches
**Actions (right-aligned):**
- `[+ Create Event]` — primary button, opens event-create-edit drawer
- `[Clone Previous Event]` — secondary button (opens event selector to pick a past event to clone as template)
- `[Export Events Report]` — secondary button

### 3.3 Alert Banner

| Condition | Banner Type | Message |
|---|---|---|
| Event in next 7 days with < 20% RSVP rate | Warning (amber) | "Event [Name] on [Date] has only N RSVPs. Consider sending a reminder." |
| Event pending budget approval | Warning (amber) | "Event [Name] is awaiting budget approval from the Admissions Director." |
| Post-event follow-up overdue (> 3 days after event) | Warning (amber) | "N completed events are awaiting post-event follow-up actions." |
| Event created successfully | Success (green) | "Event [Name] created successfully." |

---

## 4. KPI Summary Bar

| Card | Metric | Source | Colour Rule | Drill-down |
|---|---|---|---|---|
| Upcoming Events (Next 60 Days) | COUNT events WHERE date BETWEEN today AND today+60 AND status IN (Planned, Registration Open) | `alumni_events` | Blue always | Filters table to upcoming |
| Total RSVPs (Upcoming Events) | SUM rsvp_yes_count for upcoming events | `event_rsvps` | Blue always | No drill-down |
| Alumni Engaged via Events (This Year) | COUNT DISTINCT alumni_id who attended any event this year | `event_attendance` | Green if ≥ target; blue otherwise | No drill-down |
| Last Event Attendance Rate % | attended / invited × 100 for most recently completed event | `event_attendance` | Green if ≥ 60%; amber if 40–59%; red if < 40% | Filters to last completed event |
| Events This Year vs Last Year | Current year count / previous year count (ratio + arrow) | `alumni_events` | Green if ratio > 1; amber if = 1; red if < 1 | No drill-down |
| Open Invitations Not Responded | COUNT rsvps WHERE status = Pending across upcoming events | `event_rsvps` | Amber if > 50 | No drill-down |

**HTMX auto-refresh pattern (every 5 minutes):**
```html
<div id="kpi-bar"
     hx-get="/group/adm/alumni/events/kpis/"
     hx-trigger="load, every 300s"
     hx-target="#kpi-bar"
     hx-swap="outerHTML">
  <!-- KPI cards rendered here -->
</div>
```

---

## 5. Sections

### 5.1 Events Table

**Display:** Full-width sortable, server-side paginated table (20 rows/page). Default sort: event date ascending (upcoming first).

**Columns:**

| Column | Notes |
|---|---|
| Event ID | Auto-generated, e.g. AEV-0034 |
| Event Name | Full event name |
| Type | Annual Meet / Felicitation / Career Talk / Webinar / School Visit (colour-coded badge) |
| Date | Event date |
| Branch / Location | Branch name or venue city for multi-branch events |
| Mode | In-person / Online / Hybrid (badge) |
| Target Audience | e.g. "All Alumni", "JEE/NEET Rankers", "Batch 2020–2023" |
| Invited | Count of alumni invited |
| RSVP Yes | Count confirmed |
| Attended | Count who attended (0 for future events) |
| Status | Planned / Registration Open / Registration Closed / Completed / Cancelled (badge) |
| Action | `[Manage →]` — opens event-create-edit drawer in edit/manage mode |

**Filters:**
- Type (multi-select)
- Status (multi-select)
- Date range (from / to date pickers)
- Mode (In-person / Online / Hybrid / All)

**Header actions:**
- `[+ Create Event]` (also in page header)
- `[Clone Previous Event]` (also in page header)

**HTMX:** Filter changes → `hx-get="/group/adm/alumni/events/table/"` with `hx-trigger="change"`, `hx-target="#events-table"`. Pagination: `hx-get` with `?page=N`.

**Empty state:** "No events match the selected filters. Create the first event using [+ Create Event]."

---

### 5.2 Event Calendar

**Display:** Month-view calendar grid. Each day cell shows event chips with event name and type badge. Up to 2 chips per cell; overflow "+N more" linked to list.

**Click on event chip** → opens inline quick-view panel below calendar showing: event name, type, date, venue, RSVP count, status, `[Manage →]` link.

**Month navigation:** Prev/next arrow buttons reload calendar via HTMX.

**HTMX:** Month navigation → `hx-get="/group/adm/alumni/events/calendar/?month=YYYY-MM"`, `hx-target="#event-calendar-grid"`, `hx-swap="outerHTML"`. Event chip click → `hx-get="/group/adm/alumni/events/calendar/event/{id}/"`, `hx-target="#calendar-quick-view"`, `hx-swap="innerHTML"`.

---

### 5.3 RSVP Management

**Display:** Triggered by selecting an event from a dropdown at the top of this section ("Manage RSVPs for:"). Loads the RSVP table for that event.

**RSVP Table columns:**

| Column | Notes |
|---|---|
| Alumni Name | Full name |
| Batch Year | Year of passing |
| Branch | Home branch |
| RSVP Status | Attending / Not Attending / Pending / No Response |
| Dietary / Special Notes | Free text (entered by alumni during registration) |
| Last Reminder Sent | Date of last reminder message |
| Action | `[Send Reminder →]` — sends individual WhatsApp/email reminder |

**Section-level actions:**
- `[Send Reminder to All Pending]` — bulk reminder to all alumni with RSVP = Pending
- `[Export RSVP List]` — CSV of this event's RSVP data
- `[Download Attendee Badge Sheet]` — generates printable name badge template

**HTMX:** Event selection → `hx-get="/group/adm/alumni/events/rsvp/{event_id}/"`, `hx-target="#rsvp-table-area"`. Send reminder (individual): `hx-post="/group/adm/alumni/events/rsvp/{event_id}/remind/{alumni_id}/"`, `hx-target="#reminder-status-{alumni_id}"`.

**Empty state:** "Select an event above to view its RSVP list."

---

### 5.4 Event Engagement Metrics

**Display:** Two Chart.js 4.x charts side by side.

**Chart A — Events per month (last 12 months):** Line chart with X = months, Y = event count. Shows event frequency trend.

**Chart B — RSVP vs Attendance comparison (last 12 months):** Grouped bar chart per month — RSVP count (blue bar) vs actual attendance count (green bar). Shows how well RSVP intent converts to actual attendance.

**Below charts:** Four stat tiles:
- Best attended event (this year): name + attendance count
- Worst attended event (this year): name + attendance rate %
- Average RSVP-to-attendance conversion rate (all events this year)
- Total unique alumni engaged this year (across all events)

**HTMX:** `hx-get="/group/adm/alumni/events/metrics/"` lazy-loaded on `intersect once`, `hx-target="#event-metrics"`.

---

### 5.5 Post-event Follow-up Queue

**Display:** List of completed events that have not yet had post-event follow-up actions completed. An event is considered "pending follow-up" if its status = Completed and the post_event_actions_completed flag = False.

**Each entry shows:**
Event name | Date completed | Branch/location | Attendance count | Action checklist: [Send thank-you WhatsApp ✗] [Collect feedback ✗] [Record referrals generated ✗] | `[Complete Follow-up Actions →]` button

**Clicking `[Complete Follow-up Actions →]`** opens post-event-actions drawer.

**HTMX:** `hx-get="/group/adm/alumni/events/post-event-queue/"` on load.

**Empty state:** "All completed events have had follow-up actions completed."

---

### 5.6 Event Budget Tracker

**Display:** Table listing all events with budget data for the current financial year.

**Columns:**

| Column | Notes |
|---|---|
| Event Name | Name |
| Date | Event date |
| Status | Completed / Planned / etc. |
| Estimated Cost (₹) | Budget entered at creation |
| Vendor Bookings (₹) | Committed spend (venue, catering, transport) |
| Actual Spend (₹) | Post-event actual spend (editable for completed events) |
| Variance (₹) | Actual − Estimated (red if over; green if under) |
| Action | `[Edit Budget →]` — opens inline edit for cost fields |

**HTMX:** Budget table loaded via `hx-get="/group/adm/alumni/events/budget/"`. Edit budget inline: `hx-patch="/group/adm/alumni/events/budget/{event_id}/"` triggered on `[Edit Budget →]` opens editable row.

**Empty state:** "No budget data entered. Add budget information when creating events."

---

## 6. Drawers & Modals

### 6.1 `event-create-edit` Drawer
**Width:** 640px
**Trigger:** `[+ Create Event]`, `[Manage →]` in table, or `[Clone Previous Event]`
**HTMX endpoint:** `hx-get="/group/adm/alumni/events/create/"` (create) or `hx-get="/group/adm/alumni/events/edit/{id}/"` (edit) — lazy-loaded
**Tabs:**
1. **Basic Info** — Event name, type (dropdown), description, target audience (text + alumni segment filter)
2. **Schedule & Venue** — Date, start time, end time, mode (In-person / Online / Hybrid), venue name and address (for in-person), platform URL (for online), branch (dropdown — "All Branches" option for group-wide events)
3. **Invitation List** — Add alumni by: all alumni / batch year filter / branch filter / manual selection (autocomplete). Shows count of invited alumni.
4. **RSVP Settings** — RSVP deadline, allow post-deadline RSVP toggle, collect dietary/special requirements toggle, RSVP confirmation message text
5. **Budget** — Estimated cost (₹), vendor items (line items: venue / catering / gift / transport / other), approval required toggle (auto-set if above threshold)
6. **Notifications** — Event announcement message (WhatsApp/email template), RSVP reminder schedule (3 days before / 1 day before toggle), post-event thank-you message template

---

### 6.2 `event-attendance-sheet` Drawer
**Width:** 560px
**Trigger:** `[Manage →]` on event day (when status = Registration Open or In Progress)
**HTMX endpoint:** `hx-get="/group/adm/alumni/events/attendance/{event_id}/"` lazy-loaded
**Content:**
- List of RSVP-confirmed alumni with attendance toggles (Attended / Not Attended)
- Walk-in entry: quick-add form (name, batch year, branch, phone)
- `[Submit Attendance]` — marks event as Completed, triggers post-event queue entry

---

### 6.3 `post-event-actions` Drawer
**Width:** 400px
**Trigger:** `[Complete Follow-up Actions →]` in post-event queue
**HTMX endpoint:** `hx-get="/group/adm/alumni/events/post-event/{event_id}/"` lazy-loaded
**Content:**
- Checklist of three actions with completion toggles:
  1. Send thank-you WhatsApp to all attendees — `[Send Now]` button triggers bulk message
  2. Collect feedback — `[Generate Feedback Link]` button (creates shareable Google Form or internal form URL)
  3. Record referrals generated at event — number input (how many referral prospects were collected at the event)
- Notes field for event debrief
- `[Mark All Actions Complete]` — sets `post_event_actions_completed = True`, removes from queue

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Event created | "Event [Name] created successfully." | Success | 4s |
| Event updated | "Event details updated." | Success | 3s |
| Event cancelled | "Event [Name] has been cancelled. Invited alumni will be notified." | Warning | 5s |
| Reminder sent (individual) | "Reminder sent to [Alumni Name]." | Success | 3s |
| Bulk reminder sent | "Reminder messages queued for N alumni." | Success | 4s |
| Attendance submitted | "Event attendance submitted. [Name] marked as Completed." | Success | 4s |
| Post-event actions completed | "Post-event follow-up marked complete for [Event Name]." | Success | 4s |
| Budget updated | "Event budget updated." | Success | 3s |
| Event cloned | "Event cloned from [Original Name]. Review and save." | Info | 4s |
| Budget approval required | "This event requires Director approval due to budget. Approval request sent." | Warning | 5s |

---

## 8. Empty States

| Condition | Illustration | Heading | Description | CTA |
|---|---|---|---|---|
| No events yet | Calendar with star | "No alumni events planned" | "Create the first alumni engagement event to start building your program." | `[+ Create Event →]` |
| No events matching filters | Filter icon | "No events match your filters" | "Try adjusting the type, status, or date range." | `[Clear Filters]` |
| Calendar — empty month | Empty calendar grid | "No events this month" | "No alumni events scheduled for this month." | `[+ Create Event]` |
| RSVP section — no event selected | Dropdown placeholder | "Select an event to view RSVPs" | "Choose an event from the dropdown above to manage its RSVP list." | None |
| Post-event queue empty | Checkmark circle | "All follow-ups complete" | "No completed events are awaiting post-event follow-up." | None |
| Budget tracker empty | Wallet icon | "No budget data yet" | "Budget information will appear as events are created." | None |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load (KPI bar) | Skeleton cards (6 cards, grey shimmer) |
| Events table loading | Skeleton rows (5 rows, column placeholders) |
| Calendar loading / month change | Calendar grid skeleton (grey cell shimmer) |
| RSVP table loading (event selected) | Skeleton rows (5 rows) |
| Engagement metrics loading | Skeleton chart areas (2 charts) |
| Post-event queue loading | Skeleton list rows (3 rows) |
| Budget tracker loading | Skeleton rows (4 rows) |
| Drawer opening | Spinner centred in drawer body |
| Bulk reminder in progress | Button spinner + "Sending…" label |
| KPI auto-refresh | Subtle pulse on KPI cards |

---

## 10. Role-Based UI Visibility

All UI visibility decisions made server-side in Django template. No client-side JS role checks.

| UI Element | Alumni Manager (28) | Admissions Director (23) | Marketing Director | Admission Coordinator (24) |
|---|---|---|---|---|
| `[+ Create Event]` button | Visible | Hidden | Hidden | Hidden |
| `[Clone Previous Event]` | Visible | Hidden | Hidden | Hidden |
| `[Manage →]` (edit mode) | Visible | View-only mode | View + promote mode | Hidden |
| `[Cancel]` event action | Visible | Hidden | Hidden | Hidden |
| RSVP management section | Visible | Visible | Visible | Visible |
| `[Send Reminder]` buttons | Visible | Hidden | Hidden | Hidden |
| Event attendance sheet drawer | Visible | Hidden | Hidden | Hidden |
| Post-event follow-up queue | Visible | Visible | Visible | Hidden |
| `[Complete Follow-up Actions →]` | Visible | Hidden | Hidden | Hidden |
| Budget tracker section | Visible | Visible | Hidden | Hidden |
| `[Edit Budget →]` action | Visible | Visible (approval level) | Hidden | Hidden |
| `[Export Events Report]` | Visible | Visible | Visible | Visible |
| Budget approval action | N/A | Visible (approves) | N/A | N/A |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/adm/alumni/events/kpis/` | JWT G3+ | KPI bar metrics |
| GET | `/api/v1/group/{group_id}/adm/alumni/events/` | JWT G3+ | List all alumni events with filters |
| POST | `/api/v1/group/{group_id}/adm/alumni/events/` | JWT G3 write | Create new event |
| GET | `/api/v1/group/{group_id}/adm/alumni/events/{id}/` | JWT G3+ | Get event detail |
| PATCH | `/api/v1/group/{group_id}/adm/alumni/events/{id}/` | JWT G3 write | Update event |
| DELETE | `/api/v1/group/{group_id}/adm/alumni/events/{id}/` | JWT G3 write | Cancel event |
| GET | `/api/v1/group/{group_id}/adm/alumni/events/calendar/` | JWT G3+ | Events for calendar month |
| GET | `/api/v1/group/{group_id}/adm/alumni/events/{id}/rsvps/` | JWT G3+ | RSVP list for an event |
| POST | `/api/v1/group/{group_id}/adm/alumni/events/{id}/rsvps/remind/` | JWT G3 write | Send bulk RSVP reminders |
| POST | `/api/v1/group/{group_id}/adm/alumni/events/{id}/rsvps/{alumni_id}/remind/` | JWT G3 write | Send individual RSVP reminder |
| GET | `/api/v1/group/{group_id}/adm/alumni/events/metrics/` | JWT G3+ | Engagement metrics for charts |
| GET | `/api/v1/group/{group_id}/adm/alumni/events/post-event-queue/` | JWT G3+ | Events pending post-event follow-up |
| PATCH | `/api/v1/group/{group_id}/adm/alumni/events/{id}/post-event-complete/` | JWT G3 write | Mark post-event actions complete |
| GET | `/api/v1/group/{group_id}/adm/alumni/events/budget/` | JWT G3+ | Budget summary for all events |
| PATCH | `/api/v1/group/{group_id}/adm/alumni/events/{id}/budget/` | JWT G3 write | Update event budget |
| POST | `/api/v1/group/{group_id}/adm/alumni/events/{id}/attendance/` | JWT G3 write | Submit event attendance |
| POST | `/api/v1/group/{group_id}/adm/alumni/events/{id}/clone/` | JWT G3 write | Clone event as template |
| GET | `/api/v1/group/{group_id}/adm/alumni/events/export/` | JWT G3+ | Export events report |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| KPI bar auto-refresh | `load, every 300s` | GET `/group/adm/alumni/events/kpis/` | `#kpi-bar` | `outerHTML` |
| Events table filter change | `change` on filter inputs | GET `/group/adm/alumni/events/table/` | `#events-table` | `innerHTML` |
| Events table pagination | `click` on page link | GET `/group/adm/alumni/events/table/?page=N` | `#events-table` | `innerHTML` |
| Calendar month navigation | `click` on prev/next arrow | GET `/group/adm/alumni/events/calendar/?month=YYYY-MM` | `#event-calendar-grid` | `outerHTML` |
| Calendar event chip click | `click` | GET `/group/adm/alumni/events/calendar/event/{id}/` | `#calendar-quick-view` | `innerHTML` |
| RSVP event selector change | `change` on event dropdown | GET `/group/adm/alumni/events/rsvp/{event_id}/` | `#rsvp-table-area` | `innerHTML` |
| Send individual RSVP reminder | `click` on `[Send Reminder →]` | POST `/group/adm/alumni/events/{event_id}/rsvps/{alumni_id}/remind/` | `#reminder-status-{alumni_id}` | `innerHTML` |
| Send bulk RSVP reminders | `click` on bulk remind button | POST `/group/adm/alumni/events/{id}/rsvps/remind/` | `#bulk-remind-status` | `innerHTML` |
| Engagement metrics lazy load | `intersect once` | GET `/group/adm/alumni/events/metrics/` | `#event-metrics` | `innerHTML` |
| Post-event queue load | `load` | GET `/group/adm/alumni/events/post-event-queue/` | `#post-event-queue` | `innerHTML` |
| Open post-event actions drawer | `click` on `[Complete Follow-up Actions →]` | GET `/group/adm/alumni/events/post-event/{id}/` | `#drawer-container` | `innerHTML` |
| Mark post-event complete | `click` on `[Mark All Actions Complete]` | PATCH `/group/adm/alumni/events/{id}/post-event-complete/` | `#post-event-row-{id}` | `outerHTML` |
| Open create/edit drawer | `click` on `[+ Create Event]` or `[Manage →]` | GET `/group/adm/alumni/events/create/` or `/edit/{id}/` | `#drawer-container` | `innerHTML` |
| Submit event create/edit | `submit` | POST/PATCH `/group/adm/alumni/events/` or `/{id}/` | `#events-table` | `innerHTML` |
| Budget table load | `load` | GET `/group/adm/alumni/events/budget/` | `#budget-tracker-table` | `innerHTML` |
| Edit budget inline | `click` on `[Edit Budget →]` | GET `/group/adm/alumni/events/budget/{id}/edit/` | `#budget-row-{id}` | `outerHTML` |
| Save budget edit | `submit` on inline form | PATCH `/group/adm/alumni/events/{id}/budget/` | `#budget-row-{id}` | `outerHTML` |
| Open attendance sheet drawer | `click` on `[Mark Attendance]` | GET `/group/adm/alumni/events/attendance/{id}/` | `#drawer-container` | `innerHTML` |
| Submit event attendance | `submit` in attendance drawer | POST `/group/adm/alumni/events/{id}/attendance/` | `#events-table` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
