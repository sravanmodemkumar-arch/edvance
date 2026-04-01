# 06 — Sports Event Calendar

> **URL:** `/group/sports/calendar/`
> **File:** `06-sports-event-calendar.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Sports Director (Role 97, G3) · Sports Coordinator (Role 98, G3) · Cultural Head (Role 99, G3) · Chairman/CEO G5/G4 (view via governance)

---

## 1. Purpose

Central calendar of all sports events across all branches — inter-branch tournaments, sports days, practice fixtures, external competitions, and state/national events. Provides a group-wide visual overview to prevent scheduling conflicts, identify overloaded weeks, and allow the Sports Coordinator to manage logistics for upcoming events.

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Sports Director | 97 | G3 | Full — create, edit, delete events | Approve tournaments from here |
| Sports Coordinator | 98 | G3 | Full — create, edit events; manage logistics | Day-to-day operations |
| Cultural Head | 99 | G3 | View — shared calendar to avoid clashes | No sports write access |
| Group CEO / Chairman | — | G4/G5 | View via links from dashboards | Not primary audience |
| Branch Staff | — | Branch G2 | View events for their branch only | Branch-scoped view |

> **Access enforcement:** `@require_role('sports_director', 'sports_coordinator', 'cultural_head', 'chairman', 'ceo')` with server-side action gating. Cultural Head and Chairman/CEO see no create, edit, delete, or cancel controls.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Sports & Extra-Curricular  ›  Sports Event Calendar
```

### 3.2 Page Header
```
Sports Event Calendar                              [+ Add Event]  [Export Calendar ↓]
AY [academic year selector]  ·  [N] Events This Month  ·  [N] Upcoming This Week
```

**Stats Bar (below header, 3 items):**

| Item | Value | Notes |
|---|---|---|
| Events This Month | Count of events in current calendar month | Updates on AY change |
| Upcoming This Week | Count of events in next 7 days | Real-time |
| AY Selector | Dropdown — current AY (default) / previous AYs | Triggers OOB KPI + chart refresh on change |

**HTMX:** AY selector change fires `hx-get="/api/v1/group/{id}/sports/calendar/?ay={ay}"` targeting `#calendar-area` with `hx-swap="innerHTML"`, and dispatches `ayChanged` event to refresh stats bar and charts.

### 3.3 Alert Banners (conditional)

| Condition | Banner Text | Severity |
|---|---|---|
| Events with venue unconfirmed in next 7 days | "[N] event(s) in the next 7 days have an unconfirmed venue. Confirm venues to avoid last-minute issues." | Amber |
| No events scheduled this month | "No events are scheduled for this month. Add sports events to keep branches informed." | Amber |
| Tournament starting in ≤ 3 days with no coordinator assigned | "[N] tournament(s) starting within 3 days have no coordinator assigned. Assign a coordinator immediately." | Red |

### 3.4 View Switcher
- **Month** (default) · **Week** · **List** — tabs at top right of calendar area.
- Active view persisted in URL parameter: `?view=month|week|list`.

---

## 4. Calendar Views

### 4.1 Month View
- Standard month grid (Mon–Sun headers)
- Events shown as coloured tags within date cells (max 3 visible per cell + "+N more" overflow link)
- Overflow click: Opens popover listing all events for that day

**Event colours by type:**
| Event Type | Colour |
|---|---|
| Inter-Branch Tournament | Blue |
| Sports Day | Green |
| External Competition | Orange |
| Practice Fixture | Grey |
| State / National Event | Purple |
| Medical Fitness Camp | Teal |

**Click event tag:** Opens `sports-event-detail` drawer.

**Click empty date:** Opens `sports-event-create` drawer with date pre-filled.

### 4.2 Week View
- 7-column grid (Mon–Sun) × 24-hour time slots
- Events shown as blocks with duration
- Same colour coding as month view

### 4.3 List View
- All events in chronological order — full table

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Date | Date | ✅ | |
| Event Name | Text | ✅ | |
| Type | Badge | ✅ | Colour-coded |
| Sport | Badge | ✅ | |
| Branches Involved | Number | ✅ | "All" if group-wide |
| Venue | Text | ❌ | |
| Status | Badge | ✅ | Planned · Confirmed · Ongoing · Completed · Cancelled |
| Actions | — | ❌ | View · Edit · Cancel |

**Pagination (list view):** Server-side · 25/page. `hx-get="/api/v1/group/{id}/sports/calendar/?view=list&page={n}"` `hx-target="#list-table-body"` `hx-swap="innerHTML"` `hx-push-url="true"`.

---

## 5. Filters (all views)

**Slide-in filter drawer — applies to all views:**

| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Sport | Multi-select | Cricket · Football · Volleyball · Kabaddi · Athletics · Badminton · Chess · Table Tennis · Basketball · All |
| Event Type | Multi-select | Tournament · Sports Day · External · Practice · State/National |
| Status | Multi-select | Planned · Confirmed · Ongoing · Completed · Cancelled |
| Date Range | Date range picker | Custom range — default current month |

Active filters shown as chips above calendar. "Clear All" link triggers `hx-get="/api/v1/group/{id}/sports/calendar/"` (no filter params) targeting `#calendar-area` `hx-swap="innerHTML"`.

---

## 6. Drawers & Modals

### 6.1 Drawer: `sports-event-create`
- **Trigger:** [+ Add Event] header · Empty date click
- **Width:** 640px
- **Tabs:** Details · Branches · Venue · Logistics

#### Tab: Details
| Field | Type | Required | Validation |
|---|---|---|---|
| Event Name | Text | ✅ | Min 3, max 150 |
| Event Type | Select | ✅ | Tournament · Sports Day · External Competition · Practice Fixture · State/National · Medical Fitness Camp |
| Sport | Select | ✅ | From group sports list |
| Start Date | Date | ✅ | |
| End Date | Date | ✅ | ≥ Start Date |
| Start Time | Time | ❌ | |
| Duration Note | Text | ❌ | e.g. "Full day", "Morning session" |
| Description | Textarea | ❌ | Max 500 chars |
| Status | Select | ✅ | Planned (default) · Confirmed |

#### Tab: Branches
| Field | Type | Required | Validation |
|---|---|---|---|
| Applies To | Radio | ✅ | All Branches · Selected Branches |
| Select Branches | Multi-select | Conditional | |
| Host Branch | Select | ❌ | If one branch is hosting |

#### Tab: Venue
| Field | Type | Required | Validation |
|---|---|---|---|
| Venue Name | Text | ❌ | |
| Venue Type | Select | ❌ | Branch Ground · Neutral Venue · External Stadium |
| Address | Textarea | ❌ | |
| Confirmed | Toggle | ❌ | Default Off |

#### Tab: Logistics
| Field | Type | Required | Notes |
|---|---|---|---|
| Coordinator Assigned | Search + select | ❌ | From group staff |
| Equipment Needed | Textarea | ❌ | Free text list |
| Medical Staff On-Site | Toggle | ❌ | |
| Transport Arranged | Toggle | ❌ | |
| Notes | Textarea | ❌ | Internal notes |

---

### 6.2 Drawer: `sports-event-detail`
- **Width:** 640px
- **Tabs:** Overview · Branches · Results · Logistics
- **Overview:** All event metadata read-only + [Edit Event] button (Sports Dir/Coord only)
- **Branches:** Participating branches list + registration status per branch
- **Results:** Results entry table (post-event) — if event type = Tournament, links to tournament manager
- **Logistics:** Checklist items (same as coordinator dashboard logistics section)

---

### 6.3 Modal: `cancel-event-confirm`
- **Width:** 420px
- **Fields:** Cancellation reason (required, min 20 chars) · Notify participants? (checkbox default on)
- **Buttons:** [Cancel Event] (danger) + [Back]

---

## 7. Charts

All charts use Chart.js 4.x, are fully responsive, use a colorblind-safe palette, include legend and tooltip with exact numbers, and each has a PNG export button (top-right corner of each chart card). Charts are displayed in a 1×2 responsive row below the calendar / list view. On mobile they stack to single column.

### 7.1 Events by Type This AY (Donut Chart)

| Property | Value |
|---|---|
| Chart type | Doughnut |
| Title | "Events by Type — [Selected AY]" |
| Segments | Inter-Branch Tournament · Sports Day · External Competition · Practice Fixture · State/National · Medical Fitness Camp |
| Segment colours | Blue · Green · Orange · Grey · Purple · Teal (matching event type colour coding) |
| Centre label | Total events this AY |
| Legend | Right side; label + count |
| Tooltip | "[Event Type]: [N] events ([X]%)" |
| Empty state | "No events recorded for this academic year." |
| API endpoint | `GET /api/v1/group/{id}/sports/calendar/charts/by-type/?ay={ay}` |
| HTMX trigger | `hx-trigger="load"` `hx-get="…/sports/calendar/charts/by-type/"` `hx-target="#chart-events-by-type"` `hx-swap="innerHTML"`; refreshes on `ayChanged from:body` |
| Export | PNG |

### 7.2 Monthly Event Count Trend — Last 6 Months (Line Chart)

| Property | Value |
|---|---|
| Chart type | Line |
| Title | "Monthly Event Count — Last 6 Months" |
| X-axis | Last 6 calendar months (MMM YYYY) |
| Y-axis | Count of events |
| Line colour | Blue with filled area below line |
| Data points | Circular markers on each month |
| Tooltip | "[Month]: [N] events" |
| Empty state | "No event data available for the last 6 months." |
| API endpoint | `GET /api/v1/group/{id}/sports/calendar/charts/monthly-trend/` |
| HTMX trigger | `hx-trigger="load"` `hx-get="…/sports/calendar/charts/monthly-trend/"` `hx-target="#chart-monthly-trend"` `hx-swap="innerHTML"` |
| Export | PNG |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Event created | "Event [Name] added to calendar. Branches notified." | Success | 4s |
| Event updated | "Event [Name] updated." | Success | 4s |
| Event cancelled | "Event [Name] cancelled. Participants notified." | Warning | 6s |
| Export started | "Calendar export generating…" | Info | 4s |
| Validation error — required fields | "Please complete all required fields before saving." | Error | 6s |
| API error | "Something went wrong. Please try again or contact support." | Error | 8s |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| No events this month | `calendar-empty` | "No events scheduled this month" | "Add sports events to the group calendar" | [+ Add Event] |
| No events match filters | `filter-empty` | "No events match your filters" | "Try adjusting the sport, type, or date range" | [Clear Filters] |
| No events in list view | `list-empty` | "No events in this period" | "Adjust the date range or add a new event" | [+ Add Event] |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: stats bar + view switcher + calendar grid placeholder + 2 chart placeholders |
| View switch | Grid/table skeleton matching new view |
| Filter apply | Calendar re-render skeleton (300ms) |
| Event create drawer | Spinner in drawer |
| Month navigation | Shimmer overlay on calendar grid |
| Chart load | Per-chart skeleton (grey rounded rectangle with spinner) |

---

## 11. Role-Based UI Visibility

| Element | Sports Dir (97) | Sports Coord (98) | Cultural Head (99) | Others |
|---|---|---|---|---|
| [+ Add Event] button | ✅ | ✅ | ❌ | ❌ |
| [Edit] / [Cancel] on events | ✅ | ✅ | ❌ | ❌ |
| [Export Calendar] | ✅ | ✅ | ✅ (their events only) | ❌ |
| Logistics tab in drawer | ✅ | ✅ | ❌ (hidden tab) | ❌ |
| Stats bar | ✅ | ✅ | ✅ | ❌ |
| Alert banners | ✅ | ✅ | ✅ (view) | ❌ |
| Charts | ✅ | ✅ | ✅ | ❌ |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/sports/calendar/` | JWT (G3) | Events list (with date range + filters) |
| POST | `/api/v1/group/{id}/sports/events/` | JWT (G3 Dir/Coord) | Create event |
| GET | `/api/v1/group/{id}/sports/events/{eid}/` | JWT (G3) | Event detail |
| PUT | `/api/v1/group/{id}/sports/events/{eid}/` | JWT (G3 Dir/Coord) | Update event |
| POST | `/api/v1/group/{id}/sports/events/{eid}/cancel/` | JWT (G3) | Cancel event |
| GET | `/api/v1/group/{id}/sports/calendar/export/` | JWT (G3) | Export calendar (iCal/CSV) |
| GET | `/api/v1/group/{id}/sports/calendar/charts/by-type/` | JWT (G3) | Chart 7.1 — events by type |
| GET | `/api/v1/group/{id}/sports/calendar/charts/monthly-trend/` | JWT (G3) | Chart 7.2 — monthly event trend |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| Month navigation | `click` | GET `.../sports/calendar/?month={m}&year={y}` | `#calendar-grid` | `innerHTML` | Prev/next month arrows |
| View switch | `click` | GET `.../sports/calendar/?view={v}` | `#calendar-area` | `innerHTML` | Month / Week / List tabs |
| Filter apply | `click` | GET `.../sports/calendar/?filters={…}` | `#calendar-area` | `innerHTML` | Filter drawer confirm |
| Filter clear | `click` | GET `.../sports/calendar/` | `#calendar-area` | `innerHTML` | "Clear All" link; removes all filter params |
| List view pagination | `click` | GET `.../sports/calendar/?view=list&page={n}` | `#list-table-body` | `innerHTML` | Server-side; `hx-push-url="true"` |
| Click event tag | `click` | GET `.../sports/events/{id}/` | `#drawer-body` | `innerHTML` | Opens detail drawer |
| Click empty date | `click` | GET `.../sports/events/create-form/?date={d}` | `#drawer-body` | `innerHTML` | Opens create drawer with date pre-filled |
| Submit event form | `submit` | POST `.../sports/events/` | `#drawer-body` | `innerHTML` | On success: closes drawer, refreshes calendar, fires toast |
| Chart 7.1 load | `load` | GET `.../sports/calendar/charts/by-type/` | `#chart-events-by-type` | `innerHTML` | Independent per-chart load on page load |
| Chart 7.1 AY refresh | `ayChanged from:body` | GET `.../sports/calendar/charts/by-type/?ay={ay}` | `#chart-events-by-type` | `innerHTML` | OOB swap on AY selector change |
| Chart 7.2 load | `load` | GET `.../sports/calendar/charts/monthly-trend/` | `#chart-monthly-trend` | `innerHTML` | Independent per-chart load on page load |

---

*Page spec version: 1.1 · Last updated: 2026-03-21*
