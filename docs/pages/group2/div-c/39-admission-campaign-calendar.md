# Page 39 — Admission Campaign Calendar

**URL:** `/group/adm/campaign-calendar/`
**Template:** `portal_base.html`
**App:** `group_admissions`
**Django View:** `AdmissionCampaignCalendarView`

---

## 1. Purpose

The Admission Campaign Calendar is the group-wide coordination layer for all admission-related activities across the academic year. Admission is a time-critical function: a branch that misses a school fair window, delays its demo class season, or fails to dispatch offer letters before competitors do will lose enrolled students. Across a group of multiple branches operating in competitive markets, the risk of branches working at cross-purposes — overlapping scholarship exam windows, clashing marketing campaigns in the same city, demo seasons that collide with board examination periods — is significant without a single shared calendar enforced from the group level. This page exists to eliminate that risk.

The Director uses this page to define the group-wide admission framework: official admission season start and end dates per cycle, group-level school fair participation windows, scholarship exam scheduling windows (coordinated with the Scholarship Exam Manager), offer letter dispatch dates, joining confirmation deadlines, and RTE lottery dates mandated by the state authority. These group-level events define the non-negotiable skeleton of the admission year. Within that skeleton, individual branches can add branch-specific sub-events — a local school partnership visit, a walk-in drive, a branch-specific demo class — and submit them for Director review before they appear on the shared calendar. This two-tier structure ensures group consistency without stifling branch-level initiative.

The campaign calendar integrates with the campaign execution pages by surfacing event records that trigger workflows: a "Demo Season Start" event in the calendar is the signal for the Demo Class Coordinator to open scheduling on the demo program pages; a "Scholarship Exam Window" event is what the Scholarship Exam Manager sees when scheduling paper dates. The Year View Timeline gives the Director a Gantt-style overview of all campaign phases across all 12 months, making it immediately visible whether the admission season is front-loaded, whether marketing campaigns align with demo seasons, and whether joining dates leave adequate processing time for the admissions team.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Admissions Director (Role 23) | G3 | Full CRUD — group-wide events, admission season config, branch event approval/rejection | Only role that can configure Admission Season settings |
| Group Admission Coordinator (Role 24) | G3 | View all events + add branch-specific events (pending Director approval) | Cannot edit group-wide events; cannot configure seasons |
| Group Demo Class Coordinator (Role 29) | G3 | View all events + manage demo season event dates | Can edit demo-category events they own; cannot edit other categories |
| Group Scholarship Exam Manager (Role 26) | G3 | View all events + manage scholarship exam window events | Can edit scholarship-exam-category events; cannot edit other categories |
| Group Admission Counsellor (Role 25) | G3 | View only — calendar and events table | Read-only; cannot add or edit events |
| Group CEO | G3 | View only | High-level overview |
| Branch Principal | Branch | View — only own branch events + group-wide events | Cannot add or modify events |

**Enforcement:** Django view `AdmissionCampaignCalendarView` checks role and category ownership before permitting write operations. `EventCategoryPermissionMixin` ensures Demo Coordinators can only write demo-category events, Scholarship Exam Managers can only write exam-category events. No client-side role checks.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal > Admissions > Campaign Calendar
```

### 3.2 Page Header

| Element | Detail |
|---|---|
| Page title | Admission Campaign Calendar |
| Subtitle | Group-wide admission activities · AY [current cycle] |
| Header actions | [+ Add Event] [Export ICS] [Print Calendar] [Manage Seasons] |
| View toggle | Calendar View / List View / Year Timeline |
| Cycle selector | Dropdown — current cycle pre-selected |
| Category filter | Multi-select: All / Admission Season / Demo Program / Scholarship Exam / Offer Letters / Joining Dates / RTE Lottery / School Fairs / Marketing Campaigns |
| Branch filter | All / Specific branches |

### 3.3 Alert Banner

| Trigger | Message | Severity |
|---|---|---|
| Critical deadline within 7 days | "[Event name] at [Branch] is due in [N] days. Confirm readiness." | Critical (red) |
| Pending branch event requests awaiting Director approval | "[N] branch event request(s) are awaiting your approval." | Warning (amber) — Director only |
| Admission season end date within 30 days and enrollment below target | "Admission season closes in [N] days. Group enrollment is [X]% of target." | Warning (amber) |
| Event date clash detected | "Calendar conflict detected: [Event A] and [Event B] overlap at [Branch] on [Date]." | Warning (amber) |
| No admission season configured for next cycle | "The admission season for the next cycle has not been configured." | Info (blue) — Director only |

---

## 4. KPI Summary Bar

Refreshes automatically via HTMX every 5 minutes (`hx-trigger="load, every 5m"`).

| Card | Metric | Source | Colour Rule | Drill-down |
|---|---|---|---|---|
| Days to Next Season Start | Days until next admission season start date | `AdmissionSeason` table | Green >30d · Yellow 15–30d · Red ≤14d | Opens 5.5 Admission Season Configuration |
| Events This Month | Count of campaign events in current calendar month | `CampaignEvent` table | Neutral | Opens 5.2 Events Table filtered to current month |
| Events Needing Confirmation | Count of events with Status = "Pending Confirmation" | `CampaignEvent` table | Green 0 · Yellow 1–3 · Red >3 | Opens 5.2 Events Table filtered to Pending Confirmation |
| Branch Events Awaiting Approval | Count of branch-submitted events in Pending status | `CampaignEvent` table | Green 0 · Amber ≥1 | Opens 5.4 Branch Event Requests (Director only; Hidden for other roles) |
| Critical Deadlines — Next 7 Days | Count of events with due date within 7 days | `CampaignEvent` table | Green 0 · Yellow 1–2 · Red ≥3 | Opens 5.3 Critical Deadlines Strip |
| Cycle Progress | (Days elapsed since season start / Total season duration) × 100 | `AdmissionSeason` table | Neutral (progress bar style) | Opens 5.5 Admission Season Configuration |

---

## 5. Sections

### 5.1 Campaign Calendar

Full-year calendar view with month navigation. Displayed using a custom Django-rendered HTML grid (month view by default) enhanced with HTMX for month navigation.

**Event categories and colours:**
| Category | Colour |
|---|---|
| Admission Season | Deep blue |
| Demo Program | Teal |
| Scholarship Exam | Purple |
| Offer Letters | Orange |
| Joining Dates | Green |
| RTE Lottery | Red |
| School Fairs | Yellow |
| Marketing Campaigns | Pink |

Each event appears as a coloured chip on its start date. Multi-day events span their full range. Events are truncated at 3 per day with "+N more" overflow link that expands inline.

Clicking any event chip opens the event-create-edit drawer in view mode (edit mode if user has permission).

**Filter controls** (above calendar):
- Category multi-select filter
- Branch filter (All / specific branch)
- Scope: Group-wide only / Branch-specific only / All

**Navigation:** [← Prev Month] [Today] [Next Month →]. Keyboard arrow keys supported. HTMX loads new month data without full page reload.

### 5.2 Events Table

List view — all campaign events. Toggle from calendar header.

| Column | Description |
|---|---|
| Event Name | Full event name |
| Type / Category | Event category badge with colour |
| Start Date | Event start date |
| End Date | Event end date (or "Single day") |
| Branches | Affected branches (or "All branches" for group-wide) |
| Scope | Badge: Group-wide / Specific Branches |
| Status | Badge: Upcoming / Active / Completed / Cancelled |
| Created By | Staff name + role |
| Actions | [Edit →] [Duplicate →] [Delete] (role-gated) |

**Sorting:** All columns sortable. Default: Start Date ascending.
**Pagination:** 25 rows per page, HTMX-paginated.
**Filters above table:** Type, Status, Branch, Date range (from/to).

**Bulk actions (Director only):** [Export Calendar ICS] exports all visible events as an ICS file. [Print Calendar] opens a print-formatted version.

### 5.3 Critical Deadlines Strip

A fixed, always-visible panel (above the calendar/table, below the KPI bar) showing all events with a start or end date within the next 30 days.

Each deadline item is a compact card row showing:
- Event name
- Event type badge
- Date (absolute) + days remaining ("in 5 days")
- Branch tag(s)
- Colour coding: Red background if ≤7 days · Yellow background if 8–14 days · No highlight if 15–30 days

Items sorted by date ascending (nearest first).

Strip collapses to a compact "N upcoming deadlines" bar if the user hides it; expand state persists in `localStorage`.

### 5.4 Branch Event Requests

Visible to Director only. Table of events submitted by branch coordinators requesting inclusion on the group calendar.

| Column | Description |
|---|---|
| Branch | Submitting branch name |
| Event Name | Proposed event name |
| Type | Category |
| Proposed Date | Start/end date |
| Submitted By | Branch staff name |
| Submitted On | Submission date |
| Actions | [Approve →] [Reject →] [View Detail] |

[Approve] adds the event to the shared calendar with Status = Upcoming and sends confirmation notification to the submitting branch.
[Reject] opens a small inline comment field ("Reason for rejection") before confirming. Rejection sends notification with reason to submitting branch.

If the queue is empty, shows the relevant empty state card.

### 5.5 Admission Season Configuration

Director-only section (hidden for all other roles at template render time). Configures the parameters of each admission cycle.

Per-cycle form fields (one form per cycle, new cycle can be created):

| Field | Type | Description |
|---|---|---|
| Season Name | Text | e.g., "Admission Season AY 2025-26" |
| Start Date | Date picker | Official admission season open date |
| End Date | Date picker | Official admission season close date |
| Target Enrollment | Table: per-branch, per-stream | Fill target enrollment numbers |
| Key Milestone Dates | Repeater: milestone label + date | e.g., "Offer Letter Dispatch: 15 Mar 2026" |
| Notes | Textarea | Any Director notes for this cycle |

[Save Season] persists via HTMX PATCH. [Add New Cycle +] creates a new season record. Completed seasons are read-only.

Changes to season dates propagate to the campaign calendar view automatically.

### 5.6 Year View Timeline

Horizontal Gantt-style timeline chart (Chart.js 4.x — using a horizontal bar chart with time scale). Displays all campaign phases across all 12 months of the academic year on a single view.

X-axis: 12 months (Apr–Mar for Indian academic year, or Jan–Dec if configured differently).
Y-axis: Campaign categories (one row per category: Admission Season · Demo Program · Scholarship Exam · Offer Letters · Joining Dates · RTE Lottery · School Fairs · Marketing).

Each event is a horizontal bar spanning its start-to-end dates, colour-coded by category. Overlapping events within a category stack vertically. Hovering a bar shows a tooltip with event name, branch, and exact dates.

Toggle: [All branches] / [Specific branch] filter updates the chart via HTMX. This allows the Director to view one branch's full campaign timeline in isolation to check for internal clashes.

---

## 6. Drawers & Modals

| ID | Width | Tabs | HTMX Endpoint |
|---|---|---|---|
| `event-create-edit` | 640px | Basic Details · Dates & Duration · Branch Scope · Notifications · Recurrence | `GET /api/v1/group/{group_id}/adm/campaign-calendar/events/{event_id}/` (view/edit) · `POST /api/v1/group/{group_id}/adm/campaign-calendar/events/` (create) |
| `admission-season-config` | 560px | Season Settings · Branch Targets · Milestones · History | `GET /api/v1/group/{group_id}/adm/campaign-calendar/seasons/{season_id}/` · Director only |
| `branch-event-detail` | 400px | Event Details · Branch Context · Approval History | `GET /api/v1/group/{group_id}/adm/campaign-calendar/events/{event_id}/branch-request/` |

**event-create-edit drawer tabs detail:**
- **Basic Details:** Event name, category, description, created-by (auto), status
- **Dates & Duration:** Start date, end date, all-day toggle, time fields (if not all-day)
- **Branch Scope:** Group-wide toggle; if off, branch multi-select; stream filter (optional)
- **Notifications:** Who to notify on event creation / reminder schedule (N days before)
- **Recurrence:** None / Annually / Custom; recurrence end date

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Event created | "Event '[name]' added to the campaign calendar." | Success | 3s |
| Event updated | "Event '[name]' updated." | Success | 3s |
| Event deleted | "Event '[name]' removed from the calendar." | Info | 3s |
| Event duplicated | "Event duplicated. Edit the copy to adjust dates." | Info | 3s |
| Branch event approved | "Branch event '[name]' approved and added to the shared calendar." | Success | 4s |
| Branch event rejected | "Branch event '[name]' rejected. Notification sent to branch." | Info | 4s |
| Admission season saved | "Admission season configuration saved." | Success | 3s |
| ICS export ready | "Calendar exported as ICS file." | Success | 3s |
| Clash detected on save | "Warning: This event overlaps with '[other event]' on [date] at [branch]." | Warning | 6s |
| Event notification sent | "Reminder notifications sent to [N] recipients." | Success | 3s |

---

## 8. Empty States

| Condition | Illustration | Heading | Description | CTA |
|---|---|---|---|---|
| Calendar view: no events in selected month | Calendar grid with empty cells | "No Events This Month" | "No campaign events are scheduled for this month." | [+ Add Event] |
| Events table: no events match filters | Filter icon with empty result | "No Events Found" | "No events match the selected category, branch, or date range." | [Clear Filters] |
| Critical deadlines strip: no upcoming deadlines | Checkmark calendar | "No Upcoming Deadlines" | "No critical deadlines in the next 30 days." | — |
| Branch event requests: empty queue | Inbox icon | "No Pending Requests" | "No branch events are awaiting approval." | — |
| Year timeline: no events in cycle | Empty horizontal bar chart | "No Events in This Cycle" | "No campaign events have been added for the selected cycle." | [+ Add Event] [Configure Season] |
| Admission season not configured | Season outline icon | "No Season Configured" | "The admission season for this cycle has not been set up." | [Configure Season] (Director only) |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | Full-page skeleton: KPI shimmer + calendar grid skeleton (month cells shimmer) |
| KPI bar auto-refresh (every 5m) | Per-card inline spinner; retained last values |
| Month navigation in calendar | Calendar grid fades to 40% opacity; central spinner; new month content replaces |
| Filter applied | Calendar grid or table body overlay spinner |
| Events table pagination | Table body skeleton rows (5 rows) |
| Year timeline load | Chart canvas shimmer placeholder matching Gantt chart height |
| Drawer open (event-create-edit) | Drawer content skeleton with tab bar shimmer |
| Branch event approval action | [Approve] / [Reject] button spinner while processing |
| Season config drawer | Drawer skeleton with form field placeholders |

---

## 10. Role-Based UI Visibility

> All UI visibility decisions made server-side in Django template. No client-side JS role checks.

| UI Element | Director (23) | Coordinator (24) | Demo Coord (29) | Scholarship Exam Mgr (26) | Counsellor (25) | CEO |
|---|---|---|---|---|---|---|
| [+ Add Event] button | Visible | Visible (branch events only) | Visible (demo events only) | Visible (exam events only) | Hidden | Hidden |
| Event [Edit] in table | All events | Own branch events | Demo events only | Scholarship exam events only | Hidden | Hidden |
| Event [Delete] in table | All events | Own branch events | Demo events own | Exam events own | Hidden | Hidden |
| Branch Event Requests section | Visible | Hidden | Hidden | Hidden | Hidden | Hidden |
| Admission Season Configuration | Visible | Hidden | Hidden | Hidden | Hidden | Hidden |
| [Manage Seasons] header button | Visible | Hidden | Hidden | Hidden | Hidden | Hidden |
| Critical Deadlines Strip | Visible | Visible | Visible | Visible | Visible | Visible |
| KPI card: Branch Events Awaiting Approval | Visible | Hidden | Hidden | Hidden | Hidden | Hidden |
| [Export ICS] | Visible | Visible | Visible | Visible | Visible | Visible |
| Year View Timeline | Visible | Visible | Visible | Visible | Visible | Visible |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/adm/campaign-calendar/events/` | JWT | List all campaign events (filterable by month, category, branch) |
| POST | `/api/v1/group/{group_id}/adm/campaign-calendar/events/` | JWT | Create a new campaign event |
| GET | `/api/v1/group/{group_id}/adm/campaign-calendar/events/{event_id}/` | JWT | Get single event detail |
| PATCH | `/api/v1/group/{group_id}/adm/campaign-calendar/events/{event_id}/` | JWT | Update an event |
| DELETE | `/api/v1/group/{group_id}/adm/campaign-calendar/events/{event_id}/` | JWT | Delete an event |
| POST | `/api/v1/group/{group_id}/adm/campaign-calendar/events/{event_id}/duplicate/` | JWT | Duplicate an event |
| GET | `/api/v1/group/{group_id}/adm/campaign-calendar/events/kpi/` | JWT | KPI summary bar data |
| GET | `/api/v1/group/{group_id}/adm/campaign-calendar/events/deadlines/` | JWT | Critical deadlines (next 30 days) |
| GET | `/api/v1/group/{group_id}/adm/campaign-calendar/events/branch-requests/` | JWT | Pending branch event requests (Director only) |
| POST | `/api/v1/group/{group_id}/adm/campaign-calendar/events/{event_id}/approve/` | JWT | Approve a branch event request |
| POST | `/api/v1/group/{group_id}/adm/campaign-calendar/events/{event_id}/reject/` | JWT | Reject a branch event request with reason |
| GET | `/api/v1/group/{group_id}/adm/campaign-calendar/seasons/` | JWT | List admission seasons |
| POST | `/api/v1/group/{group_id}/adm/campaign-calendar/seasons/` | JWT | Create a new admission season (Director only) |
| GET | `/api/v1/group/{group_id}/adm/campaign-calendar/seasons/{season_id}/` | JWT | Get season detail |
| PATCH | `/api/v1/group/{group_id}/adm/campaign-calendar/seasons/{season_id}/` | JWT | Update season configuration (Director only) |
| GET | `/api/v1/group/{group_id}/adm/campaign-calendar/events/export/ics/` | JWT | Export events as ICS file |
| GET | `/api/v1/group/{group_id}/adm/campaign-calendar/events/timeline/` | JWT | Year timeline data for Gantt chart |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| KPI bar auto-refresh | `load, every 5m` | `GET /api/v1/group/{group_id}/adm/campaign-calendar/events/kpi/` | `#calendar-kpi-bar` | `innerHTML` |
| Calendar — navigate to previous month | `click` on [← Prev Month] | `GET /group/adm/campaign-calendar/?month=YYYY-MM&view=calendar` | `#calendar-grid` | `innerHTML` |
| Calendar — navigate to next month | `click` on [Next Month →] | `GET /group/adm/campaign-calendar/?month=YYYY-MM&view=calendar` | `#calendar-grid` | `innerHTML` |
| Calendar — apply category/branch filter | `change` on filter dropdowns | `GET /group/adm/campaign-calendar/?category=…&branch=…&month=…` | `#calendar-grid` | `innerHTML` |
| Switch to list view | `click` on List View toggle | `GET /group/adm/campaign-calendar/?view=list` | `#calendar-main-content` | `innerHTML` |
| Switch to year timeline view | `click` on Year Timeline toggle | `GET /group/adm/campaign-calendar/?view=timeline` | `#calendar-main-content` | `innerHTML` |
| Events table — pagination | `click` on page control | `GET /api/v1/group/{group_id}/adm/campaign-calendar/events/?page=N` | `#events-table-body` | `innerHTML` |
| Open event-create-edit drawer (create) | `click` on [+ Add Event] | `GET /group/adm/campaign-calendar/event-form/new/` | `#drawer-content` | `innerHTML` |
| Open event-create-edit drawer (edit) | `click` on [Edit →] | `GET /api/v1/group/{group_id}/adm/campaign-calendar/events/{event_id}/` | `#drawer-content` | `innerHTML` |
| Drawer tab switch | `click` on drawer tab | `GET /group/adm/campaign-calendar/drawer-tab/?tab=…&id=…` | `#drawer-tab-content` | `innerHTML` |
| Approve branch event request | `click` on [Approve →] | `POST /api/v1/group/{group_id}/adm/campaign-calendar/events/{event_id}/approve/` | `#branch-request-row-{event_id}` | `outerHTML` |
| Reject branch event request | `click` on [Reject →] | `POST /api/v1/group/{group_id}/adm/campaign-calendar/events/{event_id}/reject/` | `#branch-request-row-{event_id}` | `outerHTML` |
| Open admission-season-config drawer | `click` on [Manage Seasons] | `GET /api/v1/group/{group_id}/adm/campaign-calendar/seasons/` | `#drawer-content` | `innerHTML` |
| Year timeline — branch filter | `change` on branch dropdown | `GET /api/v1/group/{group_id}/adm/campaign-calendar/events/timeline/?branch={id}` | `#year-timeline-container` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
