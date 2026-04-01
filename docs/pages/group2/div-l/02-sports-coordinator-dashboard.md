# 02 — Sports Coordinator Dashboard

> **URL:** `/group/sports/coordinator/`
> **File:** `02-sports-coordinator-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Role:** Group Sports Coordinator (Role 98, G3) — exclusive post-login landing

---

## 1. Purpose

Primary post-login landing for the Group Sports Coordinator. The Coordinator is the operational backbone of the group's sports program — managing coaches, tracking equipment inventory across branches, maintaining the sports calendar, and ensuring upcoming events are fully resourced. Where the Sports Director sets policy and approves tournaments, the Coordinator executes day-to-day operations.

Core responsibilities surfaced here:
- Coach assignment gaps (branches needing a coach for a specific sport)
- Equipment requests pending procurement approval
- Sports calendar — upcoming events requiring logistics action
- Team roster health (teams without minimum player count)

Scale: 20–50 branches · 3–8 coaches per branch · 200–500 equipment requests per year.

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Sports Coordinator | 98 | G3 | Full — all sections, all actions | Exclusive dashboard |
| Group Sports Director | 97 | G3 | — | Has own dashboard `/group/sports/director/` |
| Group Cultural Activities Head | 99 | G3 | — | Separate domain |
| Group NSS/NCC Coordinator | 100 | G3 | — | Separate domain |
| Group Library Head | 101 | G2 | — | Separate domain |
| All others | — | — | — | Redirected |

> **Access enforcement:** `@require_role('sports_coordinator')` on all views and API endpoints.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Sports & Extra-Curricular  ›  Sports Coordinator Dashboard
```

### 3.2 Page Header
```
Welcome back, [Coordinator Name]                 [+ Add Coach]  [+ Log Equipment Request]
[Group Name] — Sports Coordinator · Last login: [date time]
AY [current academic year]  ·  [N] Coaches Active  ·  [N] Equipment Requests Pending
```

### 3.3 Alert Banner (conditional)

| Condition | Banner Text | Severity |
|---|---|---|
| Branch with no coach in any sport | "[N] branch(es) have no assigned coach: [list]." | Red |
| Equipment request overdue > 14 days | "[N] equipment requests have been pending for over 14 days." | Amber |
| Team with < minimum player count | "[N] team(s) are below minimum player requirement and cannot participate in upcoming tournament." | Amber |
| Upcoming tournament < 7 days, logistics incomplete | "[Tournament Name] starts in [N] days — venue confirmation and fixture sheet not finalized." | Amber |

---

## 4. KPI Summary Bar (6 cards)

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Coaches Active | Active coaches group-wide | `Coach.objects.filter(ay=current_ay, status='active').count()` | Blue always | `#kpi-coaches-active` |
| 2 | Coach Vacancy Rate | Branches with at least one coaching gap / total | `CoachVacancy.objects.filter(ay=current_ay, filled=False).values('branch').distinct().count() / Branch.objects.filter(active=True).count()` | Green = 0% · Yellow > 0% · Red > 10% | `#kpi-coach-vacancy-rate` |
| 3 | Equipment Requests Pending | Open requests not yet procured | `EquipmentRequest.objects.filter(ay=current_ay, status='pending').count()` | Green = 0 · Yellow 1–5 · Red > 5 | `#kpi-equipment-pending` |
| 4 | Events This Month | Sports events in current calendar month | `SportsEvent.objects.filter(date__month=current_month, date__year=current_year).count()` | Blue always | `#kpi-events-month` |
| 5 | Teams Below Min Roster | Teams with fewer than required player count | `Team.objects.filter(ay=current_ay, player_count__lt=F('sport__min_players')).count()` | Green = 0 · Red > 0 | `#kpi-teams-below-roster` |
| 6 | Tournament This Week | Tournaments actively running or starting within 7 days | `Tournament.objects.filter(start_date__lte=today+7d, end_date__gte=today).count()` | Blue (info) — pulsing if > 0 | `#kpi-tournament-this-week` |

**HTMX:** Each card loads independently via `hx-get` with `hx-trigger="load"` and shows skeleton while loading. AY change triggers all 6 cards to refresh via `hx-swap-oob="true"`.

Auto-refresh: `hx-trigger="every 5m"` `hx-get="/api/v1/group/{id}/sports/coordinator/kpi/"` `hx-target="#kpi-bar"` `hx-swap="innerHTML"`.

---

## 5. Sections

### 5.1 Coach Coverage Gap Table

> Branches and sports where no coach is currently assigned.

**Display:** Table — all gaps across group.

**Search:** Branch name, sport. Debounce 300ms.

**Filters:** Branch, Sport, Gap duration (>7d / >14d / >30d).

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Branch | Text + link | ✅ | |
| Sport | Badge | ✅ | Football · Cricket · etc. |
| Gap Since | Date | ✅ | When last coach left or role was created |
| Days Vacant | Number | ✅ | Red if > 30 |
| Teams Affected | Number | ✅ | Teams with no coach |
| Actions | — | ❌ | [Assign Coach] [View Coaches] |

**[Assign Coach]:** Opens `coach-detail` drawer pre-filtered to available coaches for that sport → can assign directly.

**Default sort:** Days Vacant descending.

**Pagination:** 25/page.

---

### 5.2 Equipment Request Queue

> Pending equipment requests from branch sports staff.

**Display:** Table — max 10 rows, "View All →" to page 10.

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Request ID | Text | ✅ | e.g. EQ-2026-042 |
| Branch | Text | ✅ | |
| Sport | Badge | ✅ | |
| Item Requested | Text | ✅ | e.g. "Cricket Batting Gloves" |
| Quantity | Number | ✅ | |
| Est. Cost ₹ | Currency | ✅ | |
| Requested By | Text | ❌ | Branch sports teacher name |
| Days Pending | Number | ✅ | Red if > 14 |
| Status | Badge | ✅ | Pending · Approved · Ordered · Delivered |
| Actions | — | ❌ | [Approve] [Reject] [View] |

**[Approve]:** Confirm modal (420px) — cost shown prominently.
**[Reject]:** Reason modal (420px) — min 20 chars.

**Default sort:** Days Pending descending.

---

### 5.3 Sports Calendar — This Week + Next Week

**Display:** 2-week horizontal calendar grid (Mon–Sun × 2 rows).

**Events shown:** Matches · Practice fixtures · Tournament days · Sports Day · External competitions.

**Event colours:** Tournament (blue) · Practice (grey) · Sports Day (green) · External (orange).

**Click event:** Opens event detail.

**[+ Add Event] button:** Opens `sports-event-create` form (within sports calendar page 06).

**"View Full Calendar →"** link to page 06.

---

### 5.4 Upcoming Tournament — Logistics Checklist

> For the next upcoming tournament — coordinator's pre-tournament checklist.

**Display:** Single card (if tournament exists in next 14 days) with inline checklist.

**Card header:** Tournament name · Sport · Date · Venue · Registered teams count.

**Checklist items:**
- [ ] Venue booking confirmed
- [ ] Fixture schedule published
- [ ] Referees / umpires assigned
- [ ] First aid arrangement confirmed
- [ ] Transport for visiting teams arranged
- [ ] Trophies / medals ordered
- [ ] Branch principals notified

**Each item:** Toggle (Coordinator can check off) · Updated at timestamp.

**"View Tournament Details →"** link to page 07.

---

## 6. Drawers & Modals

### 6.1 Modal: `equipment-approve`
- **Width:** 420px
- **Content:** "Approve request for [item] × [quantity] from [Branch]? Estimated cost: ₹[amount]"
- **Optional note:** Textarea
- **Buttons:** [Approve] (primary) + [Cancel]

### 6.2 Modal: `equipment-reject`
- **Width:** 420px
- **Fields:** Reason (required, min 20 chars)
- **Buttons:** [Reject] (danger) + [Cancel]

### 6.3 Drawer: `coach-assign` (from gap table)
- **Width:** 560px
- **Context:** Branch + Sport pre-filled
- **Content:** List of available coaches — name, qualifications, current assignments, sport specializations
- **[Assign] button:** Per row — opens confirm modal (380px) → on confirm: coach assigned, branch notified

---

## 7. Charts

All charts use Chart.js 4.x, are fully responsive, use a colorblind-safe palette, and each has a PNG export button (top-right corner of the chart card).

### 7.1 Equipment Request Volume (last 6 months)

| Property | Value |
|---|---|
| Chart type | Bar chart |
| Title | "Equipment Request Volume — Last 6 Months" |
| Data | Monthly equipment requests received vs resolved |
| X-axis | Last 6 months |
| Y-axis | Request count |
| Colours | Blue (received) · Green (resolved) |
| Tooltip | "[Month] · Received: [N] · Resolved: [N] · Pending: [N]" |
| API endpoint | `GET /api/v1/group/{id}/sports/analytics/equipment-trend/` |
| HTMX | `hx-get` on load → `hx-target="#chart-equipment-trend"` → `hx-swap="innerHTML"` |
| Export | PNG |

### 7.2 Coach Coverage by Branch

| Property | Value |
|---|---|
| Chart type | Horizontal bar chart |
| Title | "Coach Coverage by Branch" |
| Data | Coach count per branch (sorted ascending) |
| X-axis | Coach count |
| Y-axis | Branch names |
| Benchmark line | Minimum required coaches (configurable, default 3) |
| Colour | Red if below minimum, green otherwise |
| Tooltip | "[Branch]: [N] coaches ([status: below/meets minimum])" |
| API endpoint | `GET /api/v1/group/{id}/sports/analytics/coach-coverage/` |
| HTMX | `hx-get` on load → `hx-target="#chart-coach-coverage"` → `hx-swap="innerHTML"` |
| Export | PNG |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Equipment approved | "Equipment request [ID] approved. Branch notified." | Success | 4s |
| Equipment rejected | "Equipment request rejected. Branch notified with reason." | Success | 4s |
| Coach assigned | "[Coach Name] assigned to [Branch] — [Sport]." | Success | 4s |
| Checklist item saved | "Checklist updated" | Info | 3s |
| API error | "Failed to load data. Refresh the page." | Error | Manual |
| Validation error | "Please correct the highlighted fields before saving." | Error | 5s |
| API / network error | "Something went wrong. Please try again." | Error | Manual dismiss |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| No coach gaps | `users` | "All coaching positions filled" | "Every branch has a coach for all active sports" | — |
| No pending equipment requests | `calendar` | "No equipment requests pending" | "Equipment requests from branches will appear here" | — |
| No events this week | `calendar` | "No sports events this week" | "Add events to the sports calendar" | [Go to Calendar] |
| No upcoming tournament | `alert-circle` | "No tournament in next 14 days" | "Next tournament logistics checklist will appear here when one is scheduled" | — |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: 6 KPI cards + gap table (5 rows) + equipment table (5 rows) + calendar grid |
| Table filter/search | Inline skeleton rows |
| Equipment approve / reject | Spinner in button + disabled |
| Coach assign confirm | Spinner in confirm button |
| KPI auto-refresh | Shimmer on card values |

---

## 11. Role-Based UI Visibility

| Element | Sports Coordinator G3 | Others |
|---|---|---|
| Page | ✅ | ❌ Redirected |
| [Approve] / [Reject] equipment | ✅ | N/A |
| [Assign Coach] in gap table | ✅ | N/A |
| [+ Add Coach] header button | ✅ | N/A |
| Tournament checklist toggle | ✅ | N/A |
| [+ Log Equipment Request] | ✅ | N/A |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/sports/coordinator/dashboard/` | JWT (G3 Coord) | Full dashboard data |
| GET | `/api/v1/group/{id}/sports/coordinator/kpi/` | JWT (G3) | KPI auto-refresh |
| GET | `/api/v1/group/{id}/sports/coaches/gaps/` | JWT (G3) | Coach coverage gaps |
| POST | `/api/v1/group/{id}/sports/coaches/{cid}/assign/` | JWT (G3) | Assign coach to branch+sport |
| GET | `/api/v1/group/{id}/sports/equipment/?status=pending` | JWT (G3) | Equipment requests queue |
| POST | `/api/v1/group/{id}/sports/equipment/{eid}/approve/` | JWT (G3) | Approve equipment request |
| POST | `/api/v1/group/{id}/sports/equipment/{eid}/reject/` | JWT (G3) | Reject with reason |
| GET | `/api/v1/group/{id}/sports/calendar/?range=2weeks` | JWT (G3) | 2-week calendar events |
| PATCH | `/api/v1/group/{id}/sports/tournaments/{tid}/logistics/{item}/` | JWT (G3) | Toggle logistics checklist item |
| GET | `/api/v1/group/{id}/sports/analytics/equipment-trend/` | JWT (G3) | Equipment request volume chart |
| GET | `/api/v1/group/{id}/sports/analytics/coach-coverage/` | JWT (G3) | Coach coverage by branch chart |

### Query Parameters for List Endpoints

**Equipment requests list** (`/sports/equipment/`):

| Parameter | Type | Description |
|---|---|---|
| `status` | str | Filter by status: `pending`, `approved`, `ordered`, `delivered` |
| `sport` | str | Filter by sport slug |
| `branch` | int | Filter by branch ID |
| `q` | str | Search by item name or request ID |
| `page` | int | Page number (default 1) |

**Coach coverage gaps** (`/sports/coaches/gaps/`):

| Parameter | Type | Description |
|---|---|---|
| `sport` | str | Filter by sport slug |
| `branch` | int | Filter by branch ID |
| `gap_days` | int | Minimum days vacant (e.g., `7`, `14`, `30`) |
| `q` | str | Search by branch name or sport |
| `page` | int | Page number (default 1) |

---

## 13. HTMX Patterns

| Pattern | Trigger Element | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI bar load | Page container on load | GET `.../coordinator/kpi/` | `#kpi-bar` | `innerHTML` | Fires on `hx-trigger="load"`; shows skeleton cards until resolved |
| Chart 7.1 load | Chart container on load | GET `.../analytics/equipment-trend/` | `#chart-equipment-trend` | `innerHTML` | Fires on `hx-trigger="load"`; shows spinner in chart area |
| Chart 7.2 load | Chart container on load | GET `.../analytics/coach-coverage/` | `#chart-coach-coverage` | `innerHTML` | Fires on `hx-trigger="load"`; shows spinner in chart area |
| Coach gap table search | Search input | GET `.../coaches/gaps/?q=` | `#gap-table-body` | `innerHTML` | `hx-trigger="input delay:300ms"` |
| Coach gap table pagination | Pagination controls | GET `.../coaches/gaps/?page=` | `#gap-table-body` | `innerHTML` | `hx-trigger="click"` |
| Equipment queue filter | Filter controls | GET `.../equipment/?status=pending&filters=` | `#equipment-table-section` | `innerHTML` | `hx-trigger="click"` |
| Approve equipment | [Approve] button per row | POST `.../equipment/{id}/approve/` | `#eq-row-{id}` | `outerHTML` | Spinner in button while pending |
| Logistics checklist toggle | Checklist checkbox | PATCH `.../tournaments/{tid}/logistics/{item}/` | `#checklist-item-{item}` | `outerHTML` | `hx-trigger="change"` |
| KPI auto-refresh | KPI bar element | GET `.../coordinator/kpi/` | `#kpi-bar` | `innerHTML` | `hx-trigger="every 5m"` |
| Open coach assign drawer | [Assign Coach] button | GET `.../coaches/?sport={s}&available=true` | `#drawer-body` | `innerHTML` | `hx-trigger="click"` |

---

*Page spec version: 1.1 · Last updated: 2026-03-21*
