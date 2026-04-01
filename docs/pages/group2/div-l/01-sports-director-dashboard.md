# 01 — Sports Director Dashboard

> **URL:** `/group/sports/director/`
> **File:** `01-sports-director-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Role:** Group Sports Director (Role 97, G3) — exclusive post-login landing

---

## 1. Purpose

Primary post-login landing for the Group Sports Director. Command centre for sports program oversight across all branches — active tournaments, branches without any sports program, state team nominations pending, coach vacancies, and policy compliance. The Sports Director sets group-wide sports policy, approves inter-branch tournament proposals, nominates students to state and national teams, and ensures every branch runs at least a minimum sports calendar.

Scale: 20–50 branches · 8–20 teams per branch per sport type · 5–15 inter-branch tournaments per year · 100–500 student athletes nominated for external events.

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Sports Director | 97 | G3 | Full — all sections, all actions | Exclusive dashboard |
| Group Sports Coordinator | 98 | G3 | — | Has own dashboard `/group/sports/coordinator/` |
| Group Cultural Activities Head | 99 | G3 | — | Separate domain |
| Group NSS/NCC Coordinator | 100 | G3 | — | Separate domain |
| Group Library Head | 101 | G2 | — | Separate domain |
| Group Chairman / CEO | — | G5 / G4 | View sports analytics via Governance Reports | Not this URL |
| All other roles | — | — | — | Redirected to own dashboard |

> **Access enforcement:** `@require_role('sports_director')` on all views and API endpoints.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Sports & Extra-Curricular  ›  Sports Director Dashboard
```

### 3.2 Page Header
```
Welcome back, [Director Name]                    [+ New Tournament]  [Export Sports Report ↓]
[Group Name] — Group Sports Director · Last login: [date time]
AY [current academic year]  ·  [N] Branches  ·  [N] Active Tournaments  ·  [N] Teams Registered
```

### 3.3 Alert Banner (conditional)

| Condition | Banner Text | Severity |
|---|---|---|
| Branch with zero sports participation this term | "[N] branch(es) have no registered sports teams this term: [list]. Action required." | Red |
| State nomination deadline approaching | "State sports nomination deadline is [date] — [N] students pending Medical Fitness Certificate." | Amber |
| Tournament without assigned coordinator | "[N] upcoming tournament(s) have no assigned coordinator." | Amber |
| Coach vacancy >30 days | "[N] coaching vacancies open for >30 days at branches: [list]." | Amber |

---

## 4. KPI Summary Bar (7 cards)

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Branches with Active Sports | Branches with ≥1 registered team this term / total | `Branch.objects.filter(ay=current_ay, teams__isnull=False).distinct().count()` | Green = all · Yellow = 1–3 missing · Red = 4+ missing | `#kpi-branches-active` |
| 2 | Active Tournaments | Count of tournaments in Upcoming / Ongoing status | `Tournament.objects.filter(ay=current_ay, status__in=['upcoming','ongoing']).count()` | Blue always | `#kpi-tournaments-active` |
| 3 | Total Registered Athletes | Students enrolled in at least one sport group-wide | `Athlete.objects.filter(ay=current_ay, active=True).values('student').distinct().count()` | Blue always | `#kpi-athletes-total` |
| 4 | Tournaments Pending Approval | Tournament proposals submitted from branches awaiting Director approval | `Tournament.objects.filter(ay=current_ay, status='pending_approval').count()` | Red if > 0 · Green = 0 | `#kpi-tournaments-pending` |
| 5 | State / National Nominations | Students nominated for state/national team this AY | `Nomination.objects.filter(ay=current_ay, level__in=['state','national','international']).count()` | Blue always | `#kpi-nominations` |
| 6 | Coach Vacancies | Branches with unfilled coaching positions | `CoachVacancy.objects.filter(ay=current_ay, filled=False).values('branch').distinct().count()` | Green = 0 · Yellow 1–3 · Red > 3 | `#kpi-coach-vacancies` |
| 7 | Upcoming Events (30d) | Sports events across all branches in next 30 days | `SportsEvent.objects.filter(date__range=[today, today+30d]).count()` | Blue always | `#kpi-events-upcoming` |

**HTMX:** Each card loads independently via `hx-get` with `hx-trigger="load"` and shows skeleton while loading. AY change triggers all 7 cards to refresh via `hx-swap-oob="true"`.

Auto-refresh: `hx-trigger="every 5m"` `hx-get="/api/v1/group/{id}/sports/director/kpi/"` `hx-target="#kpi-bar"` `hx-swap="innerHTML"`.

---

## 5. Sections

### 5.1 Tournament Approval Queue

> Branches submit tournament proposals — Sports Director reviews and approves.

**Display:** Table — up to 8 rows, "View All →" link to page 07.

**Search:** Tournament name, branch, sport. Debounce 300ms.

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Tournament Name | Text | ✅ | e.g. "Inter-Branch Football Cup 2026" |
| Sport | Badge | ✅ | Football · Cricket · Volleyball · etc. |
| Proposed By | Text | ✅ | Branch name |
| Proposed Dates | Date range | ✅ | Start – End |
| Venue | Text | ❌ | Branch or neutral venue |
| Teams Expected | Number | ✅ | Estimated participating branches |
| Submitted On | Date | ✅ | |
| Days Pending | Number | ✅ | Red if > 7 |
| Actions | — | ❌ | [Approve] [Reject] [View Details] |

**[Approve]:** `hx-post` → success toast · row removed · branch notified.
**[Reject]:** 420px modal — required reason (min 20 chars) · communicated to submitting branch.
**[View Details]:** Opens `tournament-detail` drawer in view mode with [Approve] / [Reject] in Action tab.

**Default sort:** Days Pending descending.

---

### 5.2 Branch Sports Program Status

> Quick view of which branches are active vs inactive in sports this term.

**Search:** Branch name, city. Debounce 300ms.

**Filters:** State, Type (Day/Hostel), Status (Active/No Teams/Onboarding).

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Branch | Text + link | ✅ | → Branch Detail |
| City | Text | ✅ | |
| Teams Registered | Number | ✅ | Green ≥ 5 · Yellow 1–4 · Red = 0 |
| Total Athletes | Number | ✅ | Students in at least one team |
| Sports Offered | Tags | ❌ | Cricket, Football, etc. |
| Last Tournament | Date | ✅ | Red if > 180 days ago |
| Coach Coverage | Badge | ✅ | Full · Partial · No Coach |
| Actions | — | ❌ | View Teams · View Calendar |

**Default sort:** Teams Registered ascending (branches with fewest first).

**Pagination:** Server-side · Default 25/page.

---

### 5.3 Upcoming Tournaments (next 60 days — approved)

**Display:** Card list — max 6, grouped by sport, "View Full Calendar →" link.

**Card fields:** Tournament name · Sport badge · Dates · Venue · Registered teams count / total invited · Status (Registration Open / Closed / Ongoing).

---

### 5.4 State / National Nominations Tracker

> Students nominated this academic year for state or national-level representation.

**Display:** Compact table — max 10 rows, "View All in Achievement Register →" link.

**Columns:** Student Name · Branch · Class · Sport · Level (State/National/International) · Nomination Date · Medical Certificate (✅/❌) · Outcome (Pending/Selected/Not Selected).

**Default sort:** Nomination Date descending.

---

### 5.5 Quick Links

| Tile | Link |
|---|---|
| Sports Event Calendar | page 06 |
| Tournament Manager | page 07 |
| Sports Team Registry | page 08 |
| Coach & Staff Registry | page 09 |
| Student Achievement Register | page 19 |
| Extra-Curricular Analytics | page 20 |

---

## 6. Drawers & Modals

### 6.1 Drawer: `tournament-detail` (from approval queue)
- **Width:** 680px
- **Tabs:** Overview · Teams · Schedule · Venue · Action
- **Overview:** Tournament name, sport, proposed dates, format (knockout/league/combined)
- **Teams:** Branches invited, confirmed registrations
- **Schedule:** Proposed fixture schedule (if submitted)
- **Venue:** Address, facilities checklist, seating capacity
- **Action tab (Director only):** [Approve Tournament] (green) · [Reject with Reason] (red) · [Request Modification] (amber) — opens inline reason field

### 6.2 Modal: `tournament-reject`
- **Width:** 420px
- **Fields:** Reason (required, min 20 chars, 400 char limit with counter)
- **Buttons:** [Reject Tournament] (danger) + [Cancel]

---

## 7. Charts

All charts use Chart.js 4.x, are fully responsive, use a colorblind-safe palette, and each has a PNG export button (top-right corner of the chart card).

### 7.1 Sports Participation Trend (last 3 Academic Years)

| Property | Value |
|---|---|
| Chart type | Grouped bar chart |
| Title | "Sports Participation Trend — Last 3 Academic Years" |
| Data | Total registered athletes per AY (Day Scholars vs Hostelers) |
| X-axis | Academic years |
| Y-axis | Student count |
| Tooltip | "AY [year] · Day Scholar athletes: [N] · Hosteler athletes: [N] · Total: [N]" |
| API endpoint | `GET /api/v1/group/{id}/sports/analytics/participation-trend/` |
| HTMX | `hx-get` on load → `hx-target="#chart-participation-trend"` → `hx-swap="innerHTML"` |
| Export | PNG |

### 7.2 Sport-wise Team Distribution (current AY)

| Property | Value |
|---|---|
| Chart type | Horizontal bar chart |
| Title | "Sport-wise Team Distribution — [Current AY]" |
| Data | Number of teams registered per sport across all branches |
| X-axis | Team count |
| Y-axis | Sport names |
| Colour | Single colour, sorted descending |
| Tooltip | "[Sport]: [N] teams across [B] branches" |
| API endpoint | `GET /api/v1/group/{id}/sports/analytics/sport-distribution/` |
| HTMX | `hx-get` on load → `hx-target="#chart-sport-distribution"` → `hx-swap="innerHTML"` |
| Export | PNG |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Tournament approved | "Tournament approved. Branch notified." | Success | 4s |
| Tournament rejected | "Tournament proposal rejected. Reason sent to branch." | Success | 4s |
| Export started | "Sports report generating… download will start shortly" | Info | 4s |
| KPI load error | "Failed to refresh KPI data." | Error | Manual |
| Validation error | "Please correct the highlighted fields before saving." | Error | 5s |
| API / network error | "Something went wrong. Please try again." | Error | Manual dismiss |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| No tournament proposals | `calendar` | "No tournament proposals pending" | "Branches haven't submitted any tournament proposals yet" | — |
| No branches with teams (new group) | `users` | "No sports teams registered" | "Start by adding teams in the Sports Team Registry" | [Go to Team Registry] |
| No nominations this year | `alert-circle` | "No state nominations yet" | "Student nominations for state/national teams will appear here" | — |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: 7 KPI cards + approval table (5 rows) + branch table (5 rows) + charts |
| Approval table filter/search | Inline skeleton rows |
| Approve / Reject action | Spinner in button + disabled |
| Chart data load | Spinner centred in chart area |
| KPI auto-refresh | Shimmer on card values |

---

## 11. Role-Based UI Visibility

| Element | Sports Director G3 | All others |
|---|---|---|
| Page | ✅ | ❌ Redirected |
| [Approve] / [Reject] in approval queue | ✅ | N/A |
| [+ New Tournament] header button | ✅ | N/A |
| [Export Sports Report] | ✅ | N/A |
| State nominations table (write) | ✅ | N/A |

> All write controls rendered server-side. G1/G2 visiting any sports page see read-only views.

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/sports/director/dashboard/` | JWT (G3 Director) | Full dashboard data |
| GET | `/api/v1/group/{id}/sports/director/kpi/` | JWT (G3) | KPI cards (auto-refresh) |
| GET | `/api/v1/group/{id}/sports/tournaments/?status=pending_approval` | JWT (G3) | Tournament approval queue |
| POST | `/api/v1/group/{id}/sports/tournaments/{tid}/approve/` | JWT (G3 Director) | Approve tournament |
| POST | `/api/v1/group/{id}/sports/tournaments/{tid}/reject/` | JWT (G3 Director) | Reject with reason |
| GET | `/api/v1/group/{id}/sports/branches/status/` | JWT (G3) | Branch sports program status |
| GET | `/api/v1/group/{id}/sports/tournaments/?status=upcoming&days=60` | JWT (G3) | Upcoming tournaments |
| GET | `/api/v1/group/{id}/sports/nominations/` | JWT (G3) | State/national nominations |
| GET | `/api/v1/group/{id}/sports/analytics/participation-trend/` | JWT (G3) | Participation trend chart |
| GET | `/api/v1/group/{id}/sports/analytics/sport-distribution/` | JWT (G3) | Sport-wise team distribution |

### Query Parameters for List Endpoints

**Tournaments list** (`/sports/tournaments/`):

| Parameter | Type | Description |
|---|---|---|
| `status` | str | Filter by status: `pending_approval`, `upcoming`, `ongoing`, `completed` |
| `sport` | str | Filter by sport slug (e.g., `football`, `cricket`) |
| `branch` | int | Filter by branch ID |
| `q` | str | Search by tournament name |
| `page` | int | Page number (default 1) |

**Branch sports program status** (`/sports/branches/status/`):

| Parameter | Type | Description |
|---|---|---|
| `state` | str | Filter by state/region |
| `type` | str | Filter by branch type: `day`, `hostel` |
| `q` | str | Search by branch name or city |
| `page` | int | Page number (default 1) |

---

## 13. HTMX Patterns

| Pattern | Trigger Element | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI bar load | Page container on load | GET `.../sports/director/kpi/` | `#kpi-bar` | `innerHTML` | Fires on `hx-trigger="load"`; shows skeleton cards until resolved |
| Chart 7.1 load | Chart container on load | GET `.../analytics/participation-trend/` | `#chart-participation-trend` | `innerHTML` | Fires on `hx-trigger="load"`; shows spinner in chart area |
| Chart 7.2 load | Chart container on load | GET `.../analytics/sport-distribution/` | `#chart-sport-distribution` | `innerHTML` | Fires on `hx-trigger="load"`; shows spinner in chart area |
| Approval queue search | Search input | GET `.../tournaments/?status=pending&q=` | `#approval-table-body` | `innerHTML` | `hx-trigger="input delay:300ms"` |
| Branch table filter | Filter controls | GET `.../sports/branches/status/?filters=` | `#branch-table-section` | `innerHTML` | `hx-trigger="click"` |
| Approve tournament | [Approve] button per row | POST `.../tournaments/{id}/approve/` | `#approval-row-{id}` | `outerHTML` | Spinner in button while pending |
| Reject modal open | [Reject] button per row | GET `.../tournaments/{id}/reject-form/` | `#modal-body` | `innerHTML` | `hx-trigger="click"` opens 420px modal |
| Reject submit | Reject form in modal | POST `.../tournaments/{id}/reject/` | `#approval-row-{id}` | `outerHTML` | `hx-trigger="submit"`; closes modal on success |
| Open tournament detail drawer | [View Details] button | GET `.../tournaments/{id}/` | `#drawer-body` | `innerHTML` | `hx-trigger="click"` |
| KPI auto-refresh | KPI bar element | GET `.../sports/director/kpi/` | `#kpi-bar` | `innerHTML` | `hx-trigger="every 5m"` |
| Branch table pagination | Pagination controls | GET `.../sports/branches/status/?page=` | `#branch-table-section` | `innerHTML` | `hx-trigger="click"` |

---

*Page spec version: 1.1 · Last updated: 2026-03-21*
