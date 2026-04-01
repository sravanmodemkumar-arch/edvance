# 08 — Sports Team Registry

> **URL:** `/group/sports/teams/`
> **File:** `08-sports-team-registry.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Sports Director G3 (Role 97, full) · Sports Coordinator G3 (Role 98, full CRUD)

---

## 1. Purpose

Group-wide registry of all sports teams across every branch for the current academic year. A team record captures the sport, branch, age group, category (Boys/Girls/Mixed), enrolled players with class and eligibility data, captain, vice-captain, assigned coach, jersey colour, and season performance history. Sports Coordinators create and maintain team rosters; Sports Directors monitor program health and cross-branch parity at a glance. The page is the authoritative source for tournament eligibility checks — a team must be registered and have the minimum required player count for its sport before it can be entered into an inter-branch tournament. Scale: 8–20 teams per branch × up to 50 branches = up to 1,000 teams group-wide. The page must handle this volume through server-side pagination and performant filtering without client-side sluggishness.

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Sports Director | 97 | G3 | Full — create, edit, deactivate all teams group-wide | Can deactivate any team; sees all branches |
| Sports Coordinator | 98 | G3 | Full — create, edit, manage rosters for all branches | Cannot deactivate; sees all branches |
| Group Cultural Activities Head | 99 | G3 | View only — read all records | No create, edit, or roster actions |
| All other roles | — | — | No access | 403 on direct URL |

> **Access enforcement:** `@require_role(['sports_director', 'sports_coordinator', 'cultural_head'])` on read endpoints. `@require_role(['sports_director', 'sports_coordinator'])` on create/edit. `@require_role(['sports_director'])` on deactivate.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Sports & Extra-Curricular  ›  Sports Team Registry
```

### 3.2 Page Header
```
Sports Team Registry                          [+ New Team]  [Export ↓]
AY [academic year]  ·  [N] Teams  ·  [N] Sports  ·  [N] Branches with Teams
```

`[+ New Team]` — opens `team-create` drawer (Roles 97, 98).
`[Export ↓]` — exports current filtered table to XLSX/PDF. Includes all visible columns.

**Subtitle bar:** AY selector (dropdown). Changing AY reloads the page via HTMX.

### 3.3 Alert Banners

Stacked above the KPI bar. Each banner is individually dismissible for the session.

| Condition | Banner Text | Severity |
|---|---|---|
| Teams below minimum player count | "[N] team(s) are below the minimum required player count for their sport and are ineligible for tournaments." | Red |
| Branches with no teams registered | "[N] branch(es) have no sports teams registered for this academic year." | Amber |
| Teams with no coach assigned | "[N] team(s) have no coach assigned. Assign coaches to ensure tournament eligibility." | Amber |
| No teams registered this AY | "No sports teams have been registered for AY [year]. Register the first team to begin." | Blue |

---

## 4. KPI Summary Bar

Five cards displayed horizontally below the alert banners. Refreshed every 5 minutes via HTMX polling (`hx-trigger="every 5m"`).

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Total Teams Registered | All active team records in current AY | `Team.objects.filter(ay=current_ay, status='active').count()` | Blue (neutral) | `#kpi-total-teams` |
| 2 | Branches with Full Coverage | Branches with teams in ≥ 5 distinct sports | `Branch.objects.annotate(sport_count=Count('teams__sport', distinct=True)).filter(sport_count__gte=5).count()` | Green if all branches; Amber if < 80%; Red if < 50% | `#kpi-full-coverage` |
| 3 | Branches with No Teams | Branches with zero team records this AY | `Branch.objects.filter(active=True).exclude(teams__ay=current_ay).count()` | Red if > 0; Green if 0 | `#kpi-no-teams` |
| 4 | Total Athletes Enrolled | Distinct students in at least one team roster | `RosterEntry.objects.filter(team__ay=current_ay).values('student').distinct().count()` | Blue (neutral) | `#kpi-total-athletes` |
| 5 | Teams Without Coach | Teams where coach field is null | `Team.objects.filter(ay=current_ay, status='active', coach__isnull=True).count()` | Red if > 0; Green if 0 | `#kpi-no-coach` |

**HTMX:** Each card loads independently via `hx-get` with `hx-trigger="load"` and shows skeleton while loading. AY change triggers all cards to refresh via `hx-swap-oob="true"`.

Auto-refresh: `hx-trigger="every 5m"` `hx-get="/api/v1/group/{id}/sports/teams/kpi/"` `hx-target="#kpi-bar"` `hx-swap="innerHTML"`.

---

## 5. Sections

### 5.1 Team Registry

**Display note:** Main table occupying the full page body below the KPI bar. Shows all teams for the selected AY. Row selection enabled for bulk export.

**Search:** Team name, branch name, sport. Debounce 300 ms. Cleared with × icon.

**Filters:**

| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches in group |
| Sport | Multi-select | All sports (dynamic from sport master) |
| Category | Multi-select | Boys · Girls · Mixed |
| Age Group | Multi-select | U-12 · U-14 · U-17 · U-19 · Open |
| Status | Multi-select | Active · Inactive · Suspended |
| Coach Assigned | Select | Yes · No (unassigned) |

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Team Name | Text + link | Yes | Opens `team-detail` drawer |
| Branch | Text + link | Yes | Links to branch detail page |
| Sport | Badge (colour-coded) | Yes | |
| Category | Badge | Yes | Boys (blue) · Girls (pink) · Mixed (purple) |
| Age Group | Text | Yes | U-12 · U-14 · U-17 · U-19 · Open |
| Player Count | Number | Yes | Red if below sport minimum; green if at or above |
| Coach Assigned | Text | Yes | Staff name; "Unassigned" in red badge if blank |
| Last Match Date | Date | Yes | Date of most recent match result; "–" if no matches |
| Status | Badge | Yes | Active (green) · Inactive (grey) · Suspended (orange) |
| Actions | Button group | No | View · Edit · Manage Roster · Deactivate |

**Action notes:**
- View — always visible; opens `team-detail` drawer
- Edit — Role 97 and 98; opens `team-create` drawer in edit mode
- Manage Roster — Role 97 and 98; navigates directly to Roster tab of `team-detail` drawer
- Deactivate — Role 97 only; opens `deactivate-team` modal

**Default sort:** Branch name ascending, then Team Name ascending.

**Pagination:** Server-side · 25 rows per page.

---

### 5.2 Teams Without Coach

**Display note:** Collapsible alert section shown just above Section 5.1 table when the "Teams Without Coach Assigned" KPI > 0. Collapsed by default after first page load; user can expand. When expanded, shows a compact table filtered to teams with no coach. Header: "Teams Without Coach Assigned — [N] teams" with a red badge.

| Column | Type | Notes |
|---|---|---|
| Team Name | Text + link | Opens team-detail drawer |
| Branch | Text | |
| Sport | Badge | |
| Age Group | Text | |
| Status | Badge | |
| Actions | Button | [Assign Coach] — opens team-detail Coach tab directly |

---

## 6. Drawers & Modals

### Drawer: `team-create`
- **Trigger:** `[+ New Team]` header button, or [Edit] row action
- **Width:** 560 px
- **Tabs:** Profile · Members · Coach

#### Tab: Profile
| Field | Type | Required | Validation |
|---|---|---|---|
| Team Name | Text | Yes | Min 3, max 100 characters |
| Branch | Select | Yes | From group branch list |
| Sport | Select | Yes | From group sport master |
| Category | Select | Yes | Boys · Girls · Mixed |
| Age Group | Select | Yes | U-12 · U-14 · U-17 · U-19 · Open |
| Stream | Select | No | MPC · BiPC · General (optional academic stream grouping) |
| Jersey Colour | Text | No | Max 50 characters (e.g. "Blue jersey, white shorts") |
| Founded Year | Year select | No | 4-digit year; max = current year |

#### Tab: Members
| Field | Type | Required | Validation |
|---|---|---|---|
| Add Players | Search + multi-select | Yes | Search students from selected branch by name or roll number; minimum player count shown below field based on sport default |
| Role Assignment | Tag picker per player | Yes | Captain (exactly one) · Vice Captain (at most one) · Player |

**Player count indicator:** Live counter shows "X players selected — minimum required: Y" in green when met, red when below minimum.

Warning banner shown if Captain is not assigned before proceeding to Coach tab.

#### Tab: Coach
| Field | Type | Required | Validation |
|---|---|---|---|
| Coach | Search + select | No | From coach registry, filtered to coaches with this sport in their expertise; shows name, qualification, and branch |
| Assistant Coach | Search + select | No | Same source as Coach field |
| Practice Schedule | Textarea | No | Max 300 characters; free-text (e.g. "Mon/Wed 4–6 PM, Main Ground") |

---

### Drawer: `team-detail`
- **Trigger:** Team Name link in table, or [View] / [Manage Roster] row action
- **Width:** 560 px
- **Tabs:** Roster · Performance · History

#### Tab: Roster
Team header (name, branch, sport, category, age group, status badge).

Player table:

| Column | Type | Notes |
|---|---|---|
| Student Name | Text | |
| Class | Text | e.g. "X-B" |
| Roll No. | Text | |
| Role | Badge | Captain (gold) · Vice Captain (silver) · Player |
| Added On | Date | |
| Actions | Button | [Remove] — opens confirm modal; Role 97/98 only |

[Add Player] button (Role 97, 98) — inline search field appears below table; selecting a student adds them immediately via HTMX.
[Edit Team] button (Role 97, 98) — opens `team-create` drawer in edit mode.

#### Tab: Performance
Three summary cards: Matches Played · Won (green) · Lost (red) · Drawn (grey).

Last 5 results list: Date · Opponent · Score · Result badge (W/L/D) · Tournament Name.

Tournament participation history table: Tournament Name · Format · Stage Reached · Finish Position.

#### Tab: History
Season-wise summary table:

| Column | Notes |
|---|---|
| Academic Year | |
| Tournaments Participated | Count |
| Best Tournament Finish | e.g. "Runner-up — District Cricket Cup" |
| Coach | Staff name during that AY |

[View Previous Season] year selector — reloads tab content for selected AY via HTMX.

---

### Modal: `deactivate-team`
- **Width:** 380 px
- **Content:** "Deactivate [Team Name] ([Branch] — [Sport]) for AY [year]?" Warning note if team has active tournament registrations: "This team is registered in [N] upcoming tournament(s). Deactivating will withdraw the team from those events."
- **Fields:** Reason (textarea, optional, max 200 characters)
- **Buttons:** [Deactivate] (orange warning) · [Cancel] (ghost)

---

## 7. Charts

All charts use Chart.js 4.x. Rendered in a two-column grid below the main table. Export as PNG via button on each chart card.

### 7.1 Teams Per Sport Group-Wide (Current AY)
- **Type:** Vertical bar chart
- **Data:** Count of teams per sport, all branches combined
- **X-axis:** Sport names
- **Y-axis:** Team count (integer)
- **Tooltip:** "[Sport]: [N] teams across [B] branches"
- **Export:** PNG

### 7.2 Athletes Per Branch — Top 10
- **Type:** Horizontal bar chart
- **Data:** Count of distinct enrolled athletes per branch; top 10 by athlete count
- **X-axis:** Athlete count
- **Y-axis:** Branch names (top 10 sorted descending)
- **Tooltip:** "[Branch]: [N] athletes enrolled"
- **Export:** PNG

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Team created | "Team [Name] created for [Branch]." | Success | 4 s |
| Team updated | "Team [Name] updated." | Success | 4 s |
| Team deactivated | "Team [Name] deactivated for AY [year]." | Warning | 6 s |
| Player added to roster | "[Student Name] added to [Team Name]." | Info | 3 s |
| Player removed from roster | "[Student Name] removed from [Team Name]." | Info | 3 s |
| Coach assigned | "[Coach Name] assigned as coach for [Team Name]." | Success | 4 s |
| Validation error | "Please correct the highlighted fields before saving." | Error | 5 s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No teams this AY | "No teams registered" | "Register the first sports team for this academic year." | [+ New Team] |
| No teams match filters | "No teams found" | "Try adjusting the sport, branch, age group, or status filters." | [Clear Filters] |
| Team has no players (Roster tab) | "No players in this team" | "Add players from [Branch] to build this team's roster." | [Add Player] |
| No matches played (Performance tab) | "No match history" | "Performance data will appear once match results are entered for this team's tournaments." | — |
| No history (History tab) | "No previous seasons" | "History will appear from the next academic year onwards." | — |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: KPI bar (5 cards) + alert banners + table (10 rows) + charts |
| Table filter or search change | Inline skeleton rows replacing table body |
| KPI auto-refresh (every 5 min) | Spinner icon on each KPI card |
| Drawer open | Spinner centred in drawer body; tab skeleton after load |
| Player search in Members tab | Inline spinner within search field |
| Add player (inline) | Spinner on [Add Player] button; table row appended after response |
| Deactivate confirm | Spinner inside [Deactivate] modal button |

---

## 11. Role-Based UI Visibility

| Element | Sports Director G3 (97) | Sports Coordinator G3 (98) | Cultural Activities Head G3 (99) |
|---|---|---|---|
| [+ New Team] button | Visible | Visible | Hidden |
| [Export ↓] | Visible | Visible | Visible |
| [Edit] row action | Visible | Visible | Hidden |
| [Manage Roster] row action | Visible | Visible | Hidden |
| [Deactivate] row action | Visible | Hidden | Hidden |
| [Add Player] in Roster tab | Visible | Visible | Hidden |
| [Remove] player button | Visible | Visible | Hidden |
| [Edit Team] in drawer | Visible | Visible | Hidden |
| Section 5.2 "Assign Coach" button | Visible | Visible | Hidden |
| KPI drill-down links | Visible | Visible | Visible (read-only) |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{gid}/sports/teams/` | JWT (Role 97, 98, 99) | Paginated team list with filters |
| POST | `/api/v1/group/{gid}/sports/teams/` | JWT (Role 97, 98) | Create new team |
| GET | `/api/v1/group/{gid}/sports/teams/{tid}/` | JWT (Role 97, 98, 99) | Team detail |
| PUT | `/api/v1/group/{gid}/sports/teams/{tid}/` | JWT (Role 97, 98) | Update team metadata |
| POST | `/api/v1/group/{gid}/sports/teams/{tid}/deactivate/` | JWT (Role 97) | Deactivate team |
| GET | `/api/v1/group/{gid}/sports/teams/{tid}/roster/` | JWT (Role 97, 98, 99) | Team roster |
| POST | `/api/v1/group/{gid}/sports/teams/{tid}/roster/` | JWT (Role 97, 98) | Add player to roster |
| DELETE | `/api/v1/group/{gid}/sports/teams/{tid}/roster/{pid}/` | JWT (Role 97, 98) | Remove player from roster |
| GET | `/api/v1/group/{gid}/sports/teams/{tid}/performance/` | JWT (Role 97, 98, 99) | Match performance summary |
| GET | `/api/v1/group/{gid}/sports/teams/{tid}/history/` | JWT (Role 97, 98, 99) | Season-wise history |
| GET | `/api/v1/group/{gid}/sports/teams/kpi/` | JWT (Role 97, 98, 99) | KPI card values |
| GET | `/api/v1/group/{gid}/sports/teams/no-coach/` | JWT (Role 97, 98) | Teams without coach assigned |

---

## 13. HTMX Patterns

| Pattern | Trigger Element | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI bar load | `#kpi-bar` container | GET `/api/v1/group/{gid}/sports/teams/kpi/` | `#kpi-bar` | `innerHTML` | `hx-trigger="load"`; skeleton shimmer per card |
| KPI auto-refresh | `#kpi-bar` container | GET `/api/v1/group/{gid}/sports/teams/kpi/` | `#kpi-bar` | `innerHTML` | `hx-trigger="every 5m"` |
| Team search | Search input | GET `/api/v1/group/{gid}/sports/teams/?q={val}` | `#team-table-body` | `innerHTML` | `hx-trigger="input delay:300ms"` |
| Filter apply | Filter controls | GET `/api/v1/group/{gid}/sports/teams/?filters={encoded}` | `#team-table-section` | `innerHTML` | `hx-trigger="change"` |
| AY selector change | AY dropdown | GET `/api/v1/group/{gid}/sports/teams/?ay={val}` | `#page-main-content` | `innerHTML` | `hx-trigger="change"`; reloads full page content |
| Pagination | Pagination controls | GET `/api/v1/group/{gid}/sports/teams/?page={n}` | `#team-table-section` | `innerHTML` | `hx-trigger="click"` |
| Open team drawer | Team name link / [View] | GET `/api/v1/group/{gid}/sports/teams/{tid}/drawer/` | `#drawer-body` | `innerHTML` | `hx-trigger="click"` |
| Drawer tab switch | Tab buttons | GET `/api/v1/group/{gid}/sports/teams/{tid}/{tab}/` | `#drawer-tab-content` | `innerHTML` | `hx-trigger="click"`; lazy-loads tab content |
| Add player (inline) | Search result click | POST `/api/v1/group/{gid}/sports/teams/{tid}/roster/` | `#roster-table-body` | `beforeend` | `hx-trigger="click"`; appends new row |
| Remove player confirm | [Remove] per row | DELETE `/api/v1/group/{gid}/sports/teams/{tid}/roster/{pid}/` | `#roster-row-{pid}` | `outerHTML` | `hx-trigger="click"`; removes row with fade |
| Chart 7.1 load | Chart container | GET `/api/v1/group/{gid}/sports/analytics/teams-by-sport/` | `#chart-teams-by-sport` | `innerHTML` | `hx-trigger="load"` |
| Chart 7.2 load | Chart container | GET `/api/v1/group/{gid}/sports/analytics/roster-health/` | `#chart-roster-health` | `innerHTML` | `hx-trigger="load"` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
