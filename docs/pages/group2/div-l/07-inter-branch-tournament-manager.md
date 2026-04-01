# 07 — Inter-Branch Tournament Manager

> **URL:** `/group/sports/tournaments/`
> **File:** `07-inter-branch-tournament-manager.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Sports Director G3 (Role 97, full approve/manage) · Sports Coordinator G3 (Role 98, coordinate/logistics/results)

---

## 1. Purpose

Central management page for all inter-branch sports tournaments across the group for the current academic year. The Sports Coordinator submits tournament proposals and manages all operational logistics — team registration, fixture scheduling, result entry, and award records — while the Sports Director holds sole authority to approve proposals, open registration to branches, publish standings, and formally complete a tournament. The full lifecycle is enforced: Proposed → Approved → Registration Open → Ongoing → Completed (with Cancelled as an exit state at any pre-Completed stage). A typical large group runs 5–15 tournaments per year spanning cricket, football, athletics, badminton, kabaddi, volleyball, and chess, with 10–50 branches competing per event at scales of 20,000–1,00,000 students group-wide.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Sports Director | G3, Role 97 | Full — approve, create, edit, cancel, delete, publish standings | All lifecycle transitions including Approve and Open Registration |
| Sports Coordinator | G3, Role 98 | Coordinate — create proposals, manage logistics, enter results, manage teams and fixtures | Cannot approve, open registration, publish standings, or cancel tournaments |
| Group Cultural Activities Head | G3, Role 99 | View only — read all records, no edit actions | Cannot create, edit, or transition any tournament |
| All other roles | — | No access | 403 on direct URL access |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Sports & Extra-Curricular  ›  Inter-Branch Tournament Manager
```

### 3.2 Page Header
```
Inter-Branch Tournament Manager               [+ Create Tournament]  [Export ↓]
AY [academic year]  ·  [N] Tournaments  ·  [N] Pending Approval  ·  [N] Ongoing
```

`[+ Create Tournament]` — opens `tournament-create` drawer (Roles 97, 98).
`[Export ↓]` — exports full tournament list to XLSX/PDF; includes all columns visible to the user's role.

**Subtitle bar:** Displays active AY selector (dropdown, defaults to current AY April 1 – March 31). Changing AY reloads the full page via HTMX.

### 3.3 Alert Banners

Displayed stacked above the KPI bar, each dismissible for the session.

| Condition | Banner Text | Severity |
|---|---|---|
| Pending approval > 48 hours | "[N] tournament proposal(s) have been awaiting approval for more than 48 hours." | Amber |
| Tournament start date < 7 days with status = Approved (not yet Ongoing) | "[N] approved tournament(s) start within 7 days but registration has not been opened." | Red |
| Tournament Ongoing with zero results entered | "[N] ongoing tournament(s) have no match results entered yet." | Amber |
| Branch with zero participation this AY | "[N] branch(es) have not participated in any tournament this academic year." | Amber |
| No tournaments created this AY | "No tournaments have been created for AY [year]. Create the first tournament to begin." | Blue |

---

## 4. KPI Summary Bar

Five cards displayed horizontally below the alert banners. Refreshed every 5 minutes via HTMX polling (`hx-trigger="every 5m"`).

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Total Tournaments This AY | Count of all tournament records in current AY | Blue (neutral) | Filters table to all statuses |
| Active (Ongoing + Registration Open) | Count where status = Ongoing or Registration Open | Green if > 0; Grey if 0 | Filters table to Ongoing + Registration Open |
| Pending Approval | Count where status = Proposed | Red if > 2; Amber if 1–2; Green if 0 | Filters table to Proposed |
| Completed This AY | Count where status = Completed | Blue (neutral) | Filters table to Completed |
| Branches with Zero Participation | Count of branches with no confirmed team in any tournament this AY | Red if > 0; Green if 0 | Opens branch-participation report modal |

---

## 5. Sections

### 5.1 Tournament List

**Display note:** Main table occupying the full page body below KPI bar. All tournaments for the selected AY. Each row is selectable for bulk export.

**Search:** Tournament name, sport name, branch name. Debounce 300 ms. Clears with × icon.

**Filters:**

| Filter | Type | Options |
|---|---|---|
| Sport | Multi-select | All group sports (dynamic from sport master) |
| Status | Multi-select | Proposed · Approved · Registration Open · Ongoing · Completed · Cancelled |
| Format | Multi-select | Knockout · League · Round Robin · Combined |
| Academic Year | Select | Current AY (default) · Previous AYs (up to 3) |
| Branch | Multi-select | As host or as participant — all branches in group |

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Tournament Name | Text + link | Yes | Opens `tournament-detail` drawer |
| Sport | Badge (colour-coded per sport) | Yes | |
| Format | Badge (grey) | Yes | Knockout · League · Round Robin · Combined |
| Status | Badge (colour-coded) | Yes | Proposed = yellow · Approved = blue · Registration Open = cyan · Ongoing = green · Completed = teal · Cancelled = red |
| Proposed Dates | Date range (DD MMM – DD MMM YYYY) | Yes | Sorted ascending by default |
| Host Branch | Text | Yes | Branch name; "TBD" if not set |
| Teams Registered / Total Invited | Text fraction (e.g. 12 / 18) | Yes | Red if 0 registered after Registration Open |
| Coordinator Assigned | Text | Yes | Staff name; "Unassigned" in amber if blank |
| Actions | Button group | No | View · Edit · Cancel (context-sensitive per status and role) |

**Action notes:**
- View — always visible; opens `tournament-detail` drawer
- Edit — shown when status ≠ Completed and ≠ Cancelled; Role 97 always; Role 98 for own proposals
- Cancel — shown when status ≠ Completed and ≠ Cancelled; Role 97 only; opens `cancel-tournament` modal
- Approve — shown in Actions only for Role 97 when status = Proposed

**Default sort:** Proposed start date ascending (upcoming tournaments first).

**Pagination:** Server-side · 25 rows per page · page selector shown at bottom.

---

### 5.2 Upcoming Tournaments (Next 30 Days)

**Display note:** Compact card strip pinned above Section 5.1 table. Shows a maximum of 5 cards for tournaments whose start date falls within the next 30 days and whose status is Approved, Registration Open, or Ongoing. Cards are horizontally scrollable on narrow screens.

Each card displays: Tournament Name · Sport badge · Format badge · Status badge · Start Date · Host Branch · Teams Registered / Invited.

Clicking a card opens the `tournament-detail` drawer for that tournament.

If no tournaments fall in the next 30 days, the strip shows the empty state: "No upcoming tournaments in the next 30 days."

---

## 6. Drawers & Modals

### Drawer: `tournament-create`
- **Trigger:** `[+ Create Tournament]` header button
- **Width:** 680 px
- **Tabs:** Details · Teams · Schedule · Venue

#### Tab: Details
| Field | Type | Required | Validation |
|---|---|---|---|
| Tournament Name | Text | Yes | Min 3, max 150 characters |
| Sport | Select | Yes | From group sport master list |
| Format | Select | Yes | Knockout · League · Round Robin · Combined |
| Start Date | Date | Yes | Must be a future date |
| End Date | Date | Yes | Must be ≥ Start Date |
| Description | Textarea | No | Max 500 characters |
| Status | Select (disabled for Role 98) | Yes | Proposed (default, forced for Role 98; Role 97 may set Approved) |

#### Tab: Teams
| Field | Type | Required | Validation |
|---|---|---|---|
| Invite Scope | Radio | Yes | Invite All Branches · Select Specific Branches |
| Branch Selection | Multi-select (shown when Invite Scope = Select) | Conditional | Min 2 branches required |
| Minimum Teams Required | Number | No | Integer ≥ 2 |
| Max Teams Per Branch | Number | No | Integer ≥ 1; default 1 |

#### Tab: Schedule
| Field | Type | Required | Validation |
|---|---|---|---|
| Fixture Generation Method | Radio | Yes | Auto-generate · Manual upload |
| Coordinator Assigned | Search + select | No | From staff list filtered to Role 98 users in group |
| Manual Schedule Notes | Textarea | Conditional (if Manual) | Max 1,000 characters — free-text fixture description |

Note: Auto-generate calculates rounds based on team count and format after teams are confirmed.

#### Tab: Venue
| Field | Type | Required | Validation |
|---|---|---|---|
| Venue Name | Text | No | Max 150 characters |
| Venue Type | Select | No | Branch Ground · Neutral Venue · External Stadium |
| Host Branch | Select | No | From group branch list |
| Address | Textarea | No | Max 300 characters |
| Facilities | Checkboxes | No | Changing Rooms · Medical Room · Floodlights · Scoreboard |

---

### Drawer: `tournament-detail`
- **Trigger:** Tournament Name link in table row, or [View] action button
- **Width:** 680 px
- **Tabs:** Overview · Teams · Fixtures · Results · Awards

#### Tab: Overview
All tournament metadata displayed read-only: Name, Sport, Format, Status badge, Dates, Host Branch, Venue, Description, Coordinator Assigned, Created By, Created On.

[Edit] button — shown to Role 97 always; to Role 98 when status ≠ Completed/Cancelled.
[Approve] button — shown to Role 97 only when status = Proposed. Opens `approve-tournament` modal.
[Open Registration] button — shown to Role 97 only when status = Approved.
[Cancel Tournament] button — shown to Role 97 only when status ≠ Completed/Cancelled.

#### Tab: Teams
Table of registered teams per branch.

| Column | Type | Notes |
|---|---|---|
| Branch | Text | |
| Team Name | Text | |
| Players Count | Number | |
| Registration Status | Badge | Confirmed · Pending · Withdrawn |
| Confirmed On | Date | Blank if not yet confirmed |
| Actions | Buttons | [View Roster] — opens 420 px modal with player list |

[+ Register Team] button — available to Role 97 and 98 when status = Registration Open.

#### Tab: Fixtures
Generated or manually entered fixture list.

| Column | Type | Notes |
|---|---|---|
| Match # | Text | e.g. QF-1, SF-1, Final |
| Date | Date | |
| Team A | Text | Branch – Team Name |
| Team B | Text | Branch – Team Name |
| Venue | Text | |
| Status | Badge | Scheduled · In Progress · Completed · Postponed |
| Score | Text | "3 – 1" or "–" if not yet played |
| Actions | Buttons | [Enter Result] — opens `result-entry` modal |

[Generate Fixtures] button (Roles 97, 98) — auto-generates based on format and team count. Disabled once fixtures exist unless Role 97 regenerates.

#### Tab: Results
Match-by-match results table with winner badge on each row. Includes filter by round/team. Final standings summary card shown at top when all matches complete.

#### Tab: Awards
Entry form for final positions and individual awards.

| Field | Type | Notes |
|---|---|---|
| Gold (1st Place) | Branch + Team select | |
| Silver (2nd Place) | Branch + Team select | |
| Bronze (3rd Place) | Branch + Team select | |
| Best Player | Student search + select | Free-text if student not in system |
| Additional Trophy Nominees | Repeating field | Trophy name + recipient |

[Publish Awards] button — Role 97 only. Generates PDF certificates.
[Download All Certificates (ZIP)] — available after awards published.

> **Auto-populate Achievement Register (triggered automatically on [Publish Awards]):** When [Publish Awards] is clicked, the platform automatically creates achievement records in the Student Achievement Register (page 19) for all award positions:
> - Gold (1st Place) team players → Category: Sports · Level: District (default) · Position: 1st Place · Event: [Tournament Name]
> - Silver (2nd Place) team players → Category: Sports · Level: District (default) · Position: 2nd Place
> - Bronze (3rd Place) team players → Category: Sports · Level: District (default) · Position: 3rd Place
> - Best Player → Category: Sports · Level: District · Position: Best in Category
>
> Level defaults to District for group-internal tournaments. The Sports Coordinator can open the auto-created record in Achievement Register (page 19) and update Level to State/National/International if the tournament was a qualifying event. All auto-created records are set to Pending Verification and tagged "Auto-imported from Tournament: [Name]".

**[Flag Topper for Marketing]** button (Role 97 only) — appears in the Awards tab after award entry is complete. Marks the Gold winner as a candidate for brand ambassador / topper showcase and triggers an in-platform notification to Group Marketing Director and Topper Relations Manager (Division O, Roles 114 and 120).

---

### Modal: `approve-tournament`
- **Width:** 420 px
- **Content:** Displays Tournament Name, Sport, Dates, Host Branch, Branches Invited count (read-only summary)
- **Fields:** Approval Note (textarea, optional, max 300 characters)
- **Buttons:** [Approve Tournament] (green primary) · [Cancel] (ghost)

### Modal: `reject-tournament`
- **Width:** 420 px
- **Fields:** Rejection Reason (textarea, required, min 20 characters, max 500)
- **Buttons:** [Reject] (red danger) · [Cancel] (ghost)

### Modal: `cancel-tournament`
- **Width:** 420 px
- **Fields:** Cancellation Reason (textarea, required, min 30 characters, max 500) · Notify all registered branches (checkbox, default checked)
- **Buttons:** [Cancel Tournament] (red danger) · [Back] (ghost)

### Modal: `result-entry`
- **Width:** 560 px
- **Fields:**

| Field | Type | Required | Validation |
|---|---|---|---|
| Match | Display (pre-filled from row) | — | Read-only |
| Team A Score | Number | Yes | Integer ≥ 0 |
| Team B Score | Number | Yes | Integer ≥ 0 |
| Winner | Auto-calculated | — | Shows "Team A wins", "Team B wins", or "Draw" — for knockout formats, draw requires specifying winner via tiebreak |
| Tiebreak Method (knockout only) | Select (shown on draw) | Conditional | Penalty Shootout · Super Over · Toss |
| Walkover | Checkbox | No | If checked, select which team wins by walkover; scores locked to 0–0 |
| Match Notes | Textarea | No | Max 300 characters |

- **Buttons:** [Save Result] (primary) · [Cancel] (ghost)

---

## 7. Charts

All charts use Chart.js 4.x. Rendered below the main table. Export as PNG via context menu button on each chart card.

### 7.1 Tournament Count by Sport (Current AY)
- **Type:** Horizontal bar chart
- **Data:** Count of tournaments per sport for the current AY
- **X-axis:** Tournament count (integer)
- **Y-axis:** Sport names (sorted descending by count)
- **Tooltip:** "[Sport]: [N] tournament(s)"
- **Export:** PNG

### 7.2 Branch Tournament Participation Rate
- **Type:** Donut chart
- **Data:** Two segments — branches with ≥ 1 tournament participation vs. branches with zero participation
- **Centre text:** "[N] / [Total] branches participating"
- **Tooltip:** Segment label + count + percentage
- **Export:** PNG

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Tournament created | "Tournament [Name] created successfully." | Success | 4 s |
| Tournament updated | "Tournament [Name] updated." | Success | 4 s |
| Tournament approved | "Tournament approved. Registration invite sent to [N] branches." | Success | 4 s |
| Tournament rejected | "Tournament rejected. Coordinator notified with reason." | Info | 4 s |
| Registration opened | "Registration opened for [Name]. Branches have been notified." | Success | 4 s |
| Fixtures generated | "[N] fixtures generated for [Name]." | Success | 4 s |
| Result saved | "Match result saved — [Team A] [Score A]–[Score B] [Team B]." | Info | 3 s |
| Awards published | "Awards published for [Name]. Certificates are ready." | Success | 4 s |
| Tournament cancelled | "Tournament [Name] has been cancelled." | Warning | 6 s |
| Validation error | "Please correct the highlighted fields before saving." | Error | 5 s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No tournaments this AY | "No tournaments created yet" | "Create the first inter-branch tournament for this academic year." | [+ Create Tournament] |
| No tournaments match filters | "No tournaments found" | "Try adjusting the sport, status, or branch filters." | [Clear Filters] |
| No teams registered (Teams tab) | "No teams registered" | "Open registration and invite branches to register their teams." | [Open Registration] (Role 97 only) |
| No fixtures (Fixtures tab) | "No fixtures generated" | "Generate fixtures once team registration is confirmed." | [Generate Fixtures] |
| No results entered (Results tab) | "No results entered yet" | "Enter match results as fixtures are played." | [Enter Result] |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: KPI bar (5 cards) + alert banners + upcoming strip + table (8 rows) + charts |
| Table filter or search change | Inline skeleton rows replacing table body |
| KPI auto-refresh (every 5 min) | Spinner icon on each KPI card; cards not replaced during refresh |
| Drawer open (any) | Spinner centred in drawer body; tab skeleton after load |
| Fixture generation | Full-page overlay with spinner: "Generating fixtures for [Name]…" |
| Certificate generation | Full-page overlay with spinner: "Generating [N] certificates…" |
| Result save | Spinner inside [Save Result] button; button disabled during submit |

---

## 11. Role-Based UI Visibility

| Element | Sports Director G3 (97) | Sports Coordinator G3 (98) | Cultural Activities Head G3 (99) |
|---|---|---|---|
| [+ Create Tournament] | Visible | Visible (creates as Proposed) | Hidden |
| [Export ↓] | Visible | Visible | Visible |
| [Approve] / [Reject] buttons | Visible | Hidden | Hidden |
| [Open Registration] button | Visible | Hidden | Hidden |
| [Cancel Tournament] | Visible | Hidden | Hidden |
| [Edit] on row/drawer | Visible | Visible (own proposals) | Hidden |
| [Enter Result] | Visible | Visible | Hidden |
| [Generate Fixtures] | Visible | Visible | Hidden |
| [Publish Standings] | Visible | Hidden | Hidden |
| [Publish Awards] | Visible | Hidden | Hidden |
| [Generate Certificates] | Visible | Visible | Hidden |
| KPI drill-down links | Visible | Visible | Visible (read-only) |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{gid}/sports/tournaments/` | JWT (Role 97, 98, 99) | Paginated tournament list with filters |
| POST | `/api/v1/group/{gid}/sports/tournaments/` | JWT (Role 97, 98) | Create new tournament |
| GET | `/api/v1/group/{gid}/sports/tournaments/{tid}/` | JWT (Role 97, 98, 99) | Tournament detail |
| PUT | `/api/v1/group/{gid}/sports/tournaments/{tid}/` | JWT (Role 97, 98) | Update tournament metadata |
| DELETE | `/api/v1/group/{gid}/sports/tournaments/{tid}/` | JWT (Role 97) | Delete tournament (Proposed only) |
| POST | `/api/v1/group/{gid}/sports/tournaments/{tid}/approve/` | JWT (Role 97) | Approve tournament proposal |
| POST | `/api/v1/group/{gid}/sports/tournaments/{tid}/reject/` | JWT (Role 97) | Reject with reason |
| POST | `/api/v1/group/{gid}/sports/tournaments/{tid}/open-registration/` | JWT (Role 97) | Transition to Registration Open |
| POST | `/api/v1/group/{gid}/sports/tournaments/{tid}/cancel/` | JWT (Role 97) | Cancel tournament |
| GET | `/api/v1/group/{gid}/sports/tournaments/{tid}/teams/` | JWT (Role 97, 98, 99) | Registered teams list |
| POST | `/api/v1/group/{gid}/sports/tournaments/{tid}/teams/` | JWT (Role 97, 98) | Register a team |
| GET | `/api/v1/group/{gid}/sports/tournaments/{tid}/fixtures/` | JWT (Role 97, 98, 99) | Fixtures list |
| POST | `/api/v1/group/{gid}/sports/tournaments/{tid}/fixtures/generate/` | JWT (Role 97, 98) | Auto-generate fixtures |
| POST | `/api/v1/group/{gid}/sports/tournaments/{tid}/fixtures/{fid}/result/` | JWT (Role 97, 98) | Enter match result |
| GET | `/api/v1/group/{gid}/sports/tournaments/{tid}/standings/` | JWT (Role 97, 98, 99) | League standings |
| POST | `/api/v1/group/{gid}/sports/tournaments/{tid}/standings/publish/` | JWT (Role 97) | Publish standings to branches |
| POST | `/api/v1/group/{gid}/sports/tournaments/{tid}/awards/publish/` | JWT (Role 97) | Publish awards and trigger certificates |
| GET | `/api/v1/group/{gid}/sports/tournaments/kpi/` | JWT (Role 97, 98, 99) | KPI card values |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Tournament name search | `input delay:300ms` | GET `/group/{gid}/sports/tournaments/?q={val}` | `#tournament-table-body` | `innerHTML` |
| Filter apply | `change` | GET `/group/{gid}/sports/tournaments/?filters={encoded}` | `#tournament-table-section` | `innerHTML` |
| AY selector change | `change` | GET `/group/{gid}/sports/tournaments/?ay={val}` | `#page-main-content` | `innerHTML` |
| Open tournament drawer | `click` | GET `/group/{gid}/sports/tournaments/{tid}/drawer/` | `#drawer-body` | `innerHTML` |
| Drawer tab switch | `click` | GET `/group/{gid}/sports/tournaments/{tid}/{tab}/` | `#drawer-tab-content` | `innerHTML` |
| KPI auto-refresh | `every 5m` | GET `/group/{gid}/sports/tournaments/kpi/` | `#kpi-bar` | `innerHTML` |
| Approve inline action | `click` | POST `/group/{gid}/sports/tournaments/{tid}/approve/` | `#tournament-row-{tid}` | `outerHTML` |
| Enter result submit | `submit` | POST `/group/{gid}/sports/tournaments/{tid}/fixtures/{fid}/result/` | `#fixture-row-{fid}` | `outerHTML` |
| Pagination page change | `click` | GET `/group/{gid}/sports/tournaments/?page={n}` | `#tournament-table-section` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
