# 20 — Extra-Curricular Analytics

> **URL:** `/group/sports/analytics/`
> **File:** `20-extracurricular-analytics.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Roles:** Group Sports Director (Role 97, G3) · Group Sports Coordinator (Role 98, G3) · Group Cultural Activities Head (Role 99, G3) · Group NSS/NCC Coordinator (Role 100, G3) · Group Library Head (Role 101, G2) · Group Chairman / CEO (G5/G4 — view only)

---

## 1. Purpose

Comprehensive read-only analytics dashboard for all extra-curricular activity across Division L — sports participation trends, cultural event frequency, NSS/NCC programme health, library resource usage, and cross-division student achievement analytics. No write actions exist on this page; it is a pure analytics view.

**Primary audience:** Sports Director and Cultural Head for programme oversight and cross-branch benchmarking.
**Secondary audience:** Group Chairman / CEO for executive-level programme health visibility.

All sections are role-filtered — each role sees sections relevant to their domain plus cross-division views. The AY selector at page top applies globally to all sections, charts, and KPI cards simultaneously.

**Data source:** All metrics are derived from activity records entered across Division L pages (Sports Registration, Cultural Events Calendar, NSS/NCC Programme Register, Library Resource Catalogue, Student Achievement Register).

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Sports Director | 97 | G3 | Full view — all sections and all charts | Sees sports + cross-division data in full; can export all sections |
| Group Sports Coordinator | 98 | G3 | View — Sports section + Achievements section + cross-division KPI cards only | Cannot see Cultural / NSS/NCC / Library section details; no heatmap |
| Group Cultural Activities Head | 99 | G3 | Full view — all sections and all charts | Sees cultural + cross-division data in full; can export all sections |
| Group NSS/NCC Coordinator | 100 | G3 | Full view — all sections and all charts | Sees NSS/NCC + cross-division data in full; can export all sections |
| Group Library Head | 101 | G2 | View — Library section (charts 7.9–7.10) + KPI cards 6–7 + Achievements charts only | Cannot see Sports / Cultural / NSS/NCC detail sections or heatmap |
| Group Chairman / CEO | G4/G5 | G4/G5 | View only — all sections; no export | Executive read-only; all KPI cards and all charts visible; no export button |
| Group Analytics Director (Div M) | 102 | G1 | View only — all sections and all charts; full cross-division visibility | Cannot export; primary data consumer for cross-division intelligence reports submitted to Chairman/Board |
| Group MIS Officer (Div M) | 103 | G1 | View only — KPI cards + Overview table + Achievement charts (7.11–7.12) only | Monthly MIS report data consumer; domain-detail sections (sports/cultural/NSS/library) not shown |
| All other roles | — | — | No access | — |

> **Access enforcement:** `@require_role('sports_director', 'sports_coordinator', 'cultural_head', 'nss_ncc_coordinator', 'library_head', 'chairman', 'ceo', 'analytics_director', 'mis_officer')` with section-level visibility gating per role.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Sports & Extra-Curricular  ›  Analytics  ›  Extra-Curricular Analytics
```

### 3.2 Page Header

```
Extra-Curricular Analytics                     [Export All ↓]
Group HQ Dashboard  ·  AY [YYYY-YY selector]
```

- **Title:** `Extra-Curricular Analytics`
- **Subtitle row:** `Group HQ Dashboard` · AY selector dropdown (see below)
- **No `+ New` buttons** — pure analytics page
- **Right controls:**
  - `Export All ↓` — generates server-side PDF/Excel of all visible sections and charts based on role and AY; hidden for Chairman/CEO
  - AY selector dropdown in the subtitle row

**AY Selector:** Single-select dropdown listing all academic years for which any activity data exists, plus the current AY (default). Options formatted as `YYYY-YY` (e.g., `2025-26`). Changing the AY triggers `hx-get` on the entire analytics container with `hx-swap-oob="true"` for each section, refreshing all KPI cards, tables, heatmap, and charts simultaneously without a full page reload. The selected AY value is persisted in the URL as `?ay=2025-26` to support bookmarking and sharing.

---

### 3.3 Alert Banners

| # | Condition | Banner Text | Severity | Dismissible |
|---|---|---|---|---|
| 1 | No activity data loaded for any section in the selected AY | "Analytics data for this AY is loading. Charts will appear as data becomes available." | Info | No — auto-clears when data resolves |
| 2 | One or more domains have zero activity records for the selected AY | "[N] domains have no activity data for this AY. Incomplete data may affect trend comparisons." | Amber | Yes |
| 3 | Export job in progress | "Your analytics export is being prepared. It will download automatically when ready." | Info | No — auto-clears when download begins |

Banners are rendered server-side at page load and can also be injected via HTMX `hx-swap-oob` when conditions change during the user's session (e.g., export triggered, AY changed).

---

## 4. KPI Summary Bar

Eight KPI cards in a responsive 4×2 grid (collapses to 2×4 on tablet, 1×8 on mobile). All metrics reflect the selected AY. Cards load independently via HTMX `hx-trigger="load"` and refresh on AY selector change.

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Total Athletes | Students enrolled in at least one sport this AY | COUNT(DISTINCT student_id) WHERE sport_enrolment.ay = selected_ay | Blue always | `#kpi-card-1` |
| 2 | Active Sports Teams | Teams registered and active in the selected AY | COUNT(teams) WHERE status='active' AND ay=selected_ay | Blue always | `#kpi-card-2` |
| 3 | Cultural Events This AY | Total cultural events conducted across all branches | COUNT(events) WHERE category='cultural' AND ay=selected_ay | Purple always | `#kpi-card-3` |
| 4 | NSS Volunteers (240 h+) | Students who have logged ≥ 240 volunteer hours this AY | COUNT(students) WHERE nss_hours >= 240 AND ay=selected_ay | Green if > 0; red if 0 | `#kpi-card-4` |
| 5 | NCC Cadets | Total NCC cadets enrolled this AY | COUNT(DISTINCT student_id) WHERE ncc_enrolment.ay=selected_ay | Blue always | `#kpi-card-5` |
| 6 | Library Resources (Active) | Count of active resources in the catalogue | COUNT(resources) WHERE status='active' | Teal always | `#kpi-card-6` |
| 7 | Student Achievements This AY | Total achievement records in the selected AY | COUNT(achievements) WHERE ay=selected_ay | Indigo always | `#kpi-card-7` |
| 8 | Branches — Full Extra-Curr Programme | Branches with all 4 domains (Sports + Cultural + NSS/NCC + Library) active this AY | COUNT(branches) WHERE sports_active AND cultural_active AND nss_active AND library_active | Green if equals total branches; amber if < total; red if 0 | `#kpi-card-8` |

**Role visibility for KPI cards:**

| Card | Sports Dir (97) | Sports Coord (98) | Cultural Head (99) | NSS/NCC Coord (100) | Library Head (101) | Chairman (G4/G5) |
|---|---|---|---|---|---|---|
| 1 Total Athletes | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ |
| 2 Active Sports Teams | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ |
| 3 Cultural Events | ✅ | ❌ | ✅ | ✅ | ❌ | ✅ |
| 4 NSS Volunteers | ✅ | ❌ | ✅ | ✅ | ❌ | ✅ |
| 5 NCC Cadets | ✅ | ❌ | ✅ | ✅ | ❌ | ✅ |
| 6 Library Resources | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ |
| 7 Student Achievements | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 8 Full Programme Branches | ✅ | ❌ | ✅ | ✅ | ❌ | ✅ |

**HTMX — KPI bar load:**
Each card div carries `hx-get="/api/v1/group/{group_id}/analytics/extracurricular/kpi/?ay={ay}&card={n}"` `hx-trigger="load"` `hx-target="#kpi-card-{n}"` `hx-swap="outerHTML"`. On AY selector change, an `ayChanged` event is dispatched from the AY dropdown; all 8 card divs listen via `hx-trigger="ayChanged from:body"` and refresh independently.

---

## 5. Sections

### 5.1 Cross-Division Engagement Overview

*Visible to: Sports Director (97), Cultural Head (99), NSS/NCC Coordinator (100), Chairman/CEO (G4/G5). Not shown to Sports Coordinator (98) or Library Head (101).*

High-level summary table showing all branches' participation across all four extra-curricular domains for the selected AY.

#### Filters (above table)

| Filter | Type | Options | Default |
|---|---|---|---|
| State | Multi-select dropdown | All states where branches exist | All |
| Branch Type | Radio buttons | All / Day School Only / Residential Only | All |

Filter controls carry `hx-get` targeting `#overview-table-body`; `hx-include="#overview-filter-form,#ay-selector"` ensures AY is always included.

#### Table Columns

| Column | Sortable | Notes |
|---|---|---|
| Branch | ✅ | Branch name; clicking the name opens the `branch-division-drilldown` drawer (section 6.1) |
| Sports Participation % | ✅ | (students enrolled in ≥ 1 sport ÷ total enrolled students) × 100; displayed as `NN%` |
| Cultural Participation % | ✅ | (students in ≥ 1 cultural event ÷ total enrolled students) × 100 |
| NSS Enrolment % | ✅ | (NSS-enrolled students ÷ eligible students) × 100 |
| NCC Enrolment % | ✅ | (NCC-enrolled cadets ÷ eligible students) × 100 |
| Library Access | ✅ | `Yes` (green badge) / `No` (red badge) — branch has ≥ 1 active resource assignment in selected AY |
| Overall Extra-Curr Score | ✅ | Composite score: (Sports% × 0.3) + (Cultural% × 0.25) + (NSS% × 0.2) + (NCC% × 0.1) + (Library: 1 if Yes × 15); result on 0–100 scale |
| Trend vs Last AY | ✅ | ↑ green / ↓ red / — grey; compares Overall Extra-Curr Score for this AY vs same date in prior AY |

**Default sort:** Overall Extra-Curr Score ASC (lowest-scoring branches first).
**Pagination:** Server-side, 25 rows/page.
**Row highlight:** Score < 30 → red left border (3px solid `#ef4444`); 30–59 → amber left border (`#f59e0b`); 60+ → green left border (`#22c55e`).

**Empty state:**
- Icon: chart-bar (outlined, grey)
- Heading: "No cross-division data for this academic year."
- Body: "Activity records will appear here once branches log data across all domains."
- CTA: None

---

### 5.2 Branch Extra-Curricular Health Heatmap

*Visible to: Sports Director (97), Cultural Head (99), NSS/NCC Coordinator (100), Chairman/CEO (G4/G5). Not shown to Sports Coordinator (98) or Library Head (101).*

A colour-coded grid giving a rapid visual overview of all branches' activity status across each extra-curricular domain for the selected AY.

**Layout:**
- Rows: All active branches (alphabetical A–Z)
- Columns: Sports · Cultural · NSS · NCC · Library
- Each cell: Status badge + activity count (e.g., "12 events")

**Cell colour coding — intensity scale:**

| Value | Cell Colour | Meaning |
|---|---|---|
| 0 activity | White / `#ffffff` | No activity recorded in this domain this AY |
| 1–2 activities | Very light tint (10% domain colour) | Minimal activity |
| 3–9 activities | Light tint (40% domain colour) | Some activity, below threshold |
| 10–24 activities | Medium tint (70% domain colour) | Moderate activity |
| 25+ activities | Full domain colour (100%) | High activity |

Domain colours: Sports = blue (`#3b82f6`); Cultural = purple (`#8b5cf6`); NSS = olive (`#65a30d`); NCC = teal (`#0d9488`); Library = amber (`#d97706`).

**What counts as "activity" per domain:**

| Domain | Activity Unit |
|---|---|
| Sports | Count of sport enrolments (athletes registered) in the branch for the AY |
| Cultural | Count of cultural events the branch participated in or hosted this AY |
| NSS | Count of NSS activities or camps the branch conducted this AY |
| NCC | Count of NCC training sessions or parades conducted this AY |
| Library | Count of unique resource downloads or views attributed to the branch this AY |

**Cell click:** Clicking a cell filters the view to that branch + domain combination — it opens the `branch-division-drilldown` drawer (section 6.1) pre-loaded with that branch's data for the selected domain. The clicked cell gains a 2px dark outline to indicate selection.

**Legend:** Displayed below the heatmap. Shows the colour gradient from white (0) to full domain colour (max), with midpoint labels. One legend row per domain.

**API endpoint:** `GET /api/v1/group/{group_id}/analytics/extracurricular/heatmap/?ay={ay}`

**Empty state:**
- Icon: grid (outlined, grey)
- Heading: "No branches found for this academic year."
- Body: "Branches will appear once they are active and have data in the selected AY."
- CTA: None

---

## 6. Drawers & Modals

### 6.1 Drawer — `branch-division-drilldown` (480px, right side)

Triggered by clicking any cell in the Branch Extra-Curricular Health Heatmap (section 5.2) or clicking a branch name in the overview table (section 5.1).

**Header:** `[Branch Name] — [Division Name] Activity · AY [YYYY-YY]`

**Tabs:** Summary · Details

**HTMX load:** `hx-get="/api/v1/group/{group_id}/analytics/extracurricular/drilldown/{branch_id}/{domain}/?ay={ay}"` `hx-target="#drawer-container"` `hx-trigger="click"` on heatmap cells.

---

#### Tab 1 — Summary

| Field | Notes |
|---|---|
| Branch name | Full branch name; read-only |
| State | State where the branch is located; read-only |
| Domain | Badge: Sports (blue) / Cultural (purple) / NSS (olive) / NCC (teal) / Library (amber) |
| Status | Active (green badge) / Partial (amber badge) / Inactive (red badge); thresholds same as heatmap colour scale |
| Key metric | Sports: total athletes enrolled; Cultural: total events participated; NSS: % of students with 240 h+; NCC: cadets enrolled; Library: total resource accesses |
| Total activity count this AY | Count of activity units (as defined in section 5.2 heatmap table) for this branch + domain |
| Trend vs last AY | ↑ green / ↓ red / — grey; compares current AY total vs prior AY total |
| Next scheduled activity | If available: next event, camp, or session date for this branch in this domain; shown as `DD-MMM-YYYY — [Event Name]`; "None scheduled" if absent |
| Domain coordinator at branch | Name + role of the relevant coordinator at branch level; "Not assigned" if absent |

---

#### Tab 2 — Details

Table listing the last 5 activities, events, or entries for this branch in the selected domain and AY:

| Column | Notes |
|---|---|
| Activity / Event | Full event or activity name |
| Date | DD-MMM-YYYY |
| Status | Completed (green) / Upcoming (blue) / Cancelled (red) — badge |
| Participants / Resources | Count of students involved (Sports/NSS/NCC/Cultural) or resource access count (Library) |
| Notes | Brief description; truncated at 80 characters; full text on hover |

If no activity found: "No [Domain] activity recorded for [Branch] in AY [YYYY-YY]."

**Empty state per tab:**
- Icon: calendar-x (outlined, grey)
- Heading: "No [Domain] activity for [Branch Name]."
- Body: "Activity will appear here once data is logged for this branch and domain."
- CTA: None

**Footer:** `Close` · `View Full [Domain] Data →` (links to the relevant divisional management page filtered to this branch)

---

## 7. Charts

All charts use Chart.js 4.x, are fully responsive, use a colorblind-safe palette (Wong 2011 8-colour set), include a legend and tooltip with exact numbers, and each has a PNG export button in the top-right corner of the chart card (icon: download). All charts respect the global AY selector. Charts load independently on page load via `hx-trigger="load"` and refresh on AY change via `hx-trigger="ayChanged from:body"`.

Charts are organised into six domain sections rendered as visually separated cards with domain-colour header bars.

---

### Section A — Sports Charts

*Visible to: Sports Director (97), Sports Coordinator (98), Cultural Head (99, view only), NSS/NCC Coordinator (100, view only), Chairman/CEO (G4/G5).*
*Not shown to Library Head (101).*

#### Chart 7.1 — Sports Participation Trend (Line Chart)

| Property | Value |
|---|---|
| Chart type | Line |
| Title | "Sports Participation Trend — Last 3 Academic Years" |
| X-axis | Academic years: last 3 AYs (e.g., 2023-24 / 2024-25 / 2025-26); label rotated 0° |
| Y-axis | Total athletes (student-sport enrolments); label: "Students Enrolled" |
| Lines | Three lines: "Total Athletes" (blue, `#3b82f6`) · "Day Scholars" (teal, `#0d9488`) · "Hostelers" (orange, `#f97316`) |
| Data points | Circular markers (r=4) on each AY data point |
| Tooltip | "[AY]: Total [N] · Day Scholars [N] · Hostelers [N]" |
| Empty state | Icon: line-chart (grey); Heading: "No sports participation data available."; Body: "Data will appear once sports teams and athletes are registered." |
| Export PNG | Top-right download icon; filename: `sports-participation-trend-{ay}.png` |
| API endpoint | `GET /api/v1/group/{group_id}/analytics/extracurricular/sports/participation-trend/?ay={ay}` |
| HTMX trigger | `hx-trigger="load"` on page load; `hx-trigger="ayChanged from:body"` on AY change |
| HTMX target | `#chart-sports-participation-trend` |

---

#### Chart 7.2 — Sport-wise Team Count (Horizontal Bar Chart)

| Property | Value |
|---|---|
| Chart type | Horizontal bar |
| Title | "Teams Registered by Sport — AY [YYYY-YY]" |
| Y-axis | Sport names; top 10 by team count, sorted DESC; label: "Sport" |
| X-axis | Number of active teams; label: "Teams Registered"; integer ticks |
| Bar colour | Blue gradient from `#93c5fd` (lowest) to `#1d4ed8` (highest) |
| Tooltip | "[Sport]: [N] teams active this AY" |
| Empty state | Icon: bar-chart (grey); Heading: "No sports teams registered for this AY."; Body: "Teams will appear once registered via the Sports Management page." |
| Export PNG | Top-right download icon; filename: `sport-teams-{ay}.png` |
| API endpoint | `GET /api/v1/group/{group_id}/analytics/extracurricular/sports/team-count/?ay={ay}` |
| HTMX trigger | `hx-trigger="load"` on page load; `hx-trigger="ayChanged from:body"` on AY change |
| HTMX target | `#chart-sport-teams` |

---

#### Chart 7.3 — Tournament Count per Sport (Vertical Bar Chart)

| Property | Value |
|---|---|
| Chart type | Vertical bar |
| Title | "Tournaments Conducted by Sport — AY [YYYY-YY]" |
| X-axis | Sport names (all sports with ≥ 1 tournament in selected AY); label rotated 30° if > 6 sports |
| Y-axis | Tournament count; label: "Tournaments Conducted"; integer ticks |
| Bar colour | Indigo (`#6366f1`); all bars same colour |
| Tooltip | "[Sport]: [N] tournaments in AY [YYYY-YY]" |
| Empty state | Icon: trophy (grey); Heading: "No tournaments recorded for this AY."; Body: "Tournament data will appear once events are logged in the Sports Management page." |
| Export PNG | Top-right download icon; filename: `tournament-count-{ay}.png` |
| API endpoint | `GET /api/v1/group/{group_id}/analytics/extracurricular/sports/tournament-count/?ay={ay}` |
| HTMX trigger | `hx-trigger="load"` on page load; `hx-trigger="ayChanged from:body"` on AY change |
| HTMX target | `#chart-tournament-count` |

---

### Section B — Cultural Charts

*Visible to: Cultural Head (99), Sports Director (97), NSS/NCC Coordinator (100, view only), Chairman/CEO (G4/G5).*
*Not shown to Sports Coordinator (98) or Library Head (101).*

#### Chart 7.4 — Cultural Events per Month (Vertical Bar Chart)

| Property | Value |
|---|---|
| Chart type | Vertical bar |
| Title | "Cultural Events per Month — Last 12 Months" |
| X-axis | Month labels (MMM YYYY); last 12 calendar months relative to current date; label rotated 30° |
| Y-axis | Count of cultural events conducted; label: "Events Conducted"; integer ticks |
| Bar colour | Purple (`#8b5cf6`); all bars same colour |
| Tooltip | "[MMM YYYY]: [N] cultural events" |
| Empty state | Icon: calendar (grey); Heading: "No cultural events recorded in this period."; Body: "Events will appear once recorded on the Cultural Events Calendar." |
| Export PNG | Top-right download icon; filename: `cultural-events-monthly.png` |
| API endpoint | `GET /api/v1/group/{group_id}/analytics/extracurricular/cultural/events-monthly/?ay={ay}` |
| HTMX trigger | `hx-trigger="load"` on page load; `hx-trigger="ayChanged from:body"` on AY change |
| HTMX target | `#chart-cultural-events-monthly` |

---

#### Chart 7.5 — Cultural Participation by Branch — Top 10 (Horizontal Bar Chart)

| Property | Value |
|---|---|
| Chart type | Horizontal bar |
| Title | "Top 10 Branches — Cultural Events Participated · AY [YYYY-YY]" |
| Y-axis | Branch names; top 10 by total events participated, sorted DESC |
| X-axis | Count of events; label: "Events Participated"; integer ticks |
| Bar colour | Purple gradient from `#ddd6fe` (lowest) to `#5b21b6` (highest) |
| Tooltip | "[Branch]: [N] cultural events participated in AY [YYYY-YY]" |
| Empty state | Icon: users (grey); Heading: "No cultural participation data for this AY."; Body: "Branch participation data will appear once cultural events are logged." |
| Export PNG | Top-right download icon; filename: `cultural-participation-branches-{ay}.png` |
| API endpoint | `GET /api/v1/group/{group_id}/analytics/extracurricular/cultural/branch-participation/?ay={ay}` |
| HTMX trigger | `hx-trigger="load"` on page load; `hx-trigger="ayChanged from:body"` on AY change |
| HTMX target | `#chart-cultural-branch-participation` |

---

### Section C — NSS / NCC Charts

*Visible to: NSS/NCC Coordinator (100), Sports Director (97), Cultural Head (99, view only), Chairman/CEO (G4/G5).*
*Not shown to Sports Coordinator (98) or Library Head (101).*

#### Chart 7.6 — NSS Volunteer Hours Distribution (Donut Chart)

| Property | Value |
|---|---|
| Chart type | Doughnut |
| Title | "NSS Volunteer Hours Distribution — AY [YYYY-YY]" |
| Data | Four segments: `< 100 h` / `100–199 h` / `200–239 h` / `240 h+` |
| Segment colours | `< 100 h` = red (`#ef4444`) · `100–199 h` = orange (`#f97316`) · `200–239 h` = yellow (`#eab308`) · `240 h+` = green (`#22c55e`) |
| Legend | Right side; label + count of students in each band |
| Centre label | "Total NSS Enrolled: [N]" |
| Tooltip | "[Band]: [N] students ([X]% of enrolled)" |
| Empty state | Icon: clock (grey); Heading: "No NSS data available for this AY."; Body: "Volunteer hours and activity data will appear once NSS units log data." |
| Export PNG | Top-right download icon; filename: `nss-hours-distribution-{ay}.png` |
| API endpoint | `GET /api/v1/group/{group_id}/analytics/extracurricular/nss/hours-distribution/?ay={ay}` |
| HTMX trigger | `hx-trigger="load"` on page load; `hx-trigger="ayChanged from:body"` on AY change |
| HTMX target | `#chart-nss-hours-distribution` |

---

#### Chart 7.7 — NSS Activity Count per Month (Line Chart)

| Property | Value |
|---|---|
| Chart type | Line with filled area |
| Title | "NSS Activities Conducted per Month — Last 6 Months" |
| X-axis | Month labels (MMM YYYY); last 6 calendar months |
| Y-axis | Count of NSS activities conducted; label: "Activities Conducted"; integer ticks |
| Line colour | Olive green (`#65a30d`); area fill with 20% opacity |
| Data points | Circular markers (r=4) on each month |
| Tooltip | "[MMM YYYY]: [N] NSS activities" |
| Empty state | Icon: leaf (grey); Heading: "No NSS activities recorded in this period."; Body: "Activity counts will appear once NSS units log data in the NSS/NCC Programme Register." |
| Export PNG | Top-right download icon; filename: `nss-activities-monthly.png` |
| API endpoint | `GET /api/v1/group/{group_id}/analytics/extracurricular/nss/activities-monthly/?ay={ay}` |
| HTMX trigger | `hx-trigger="load"` on page load; `hx-trigger="ayChanged from:body"` on AY change |
| HTMX target | `#chart-nss-activities-monthly` |

---

#### Chart 7.8 — NCC Cadets by Wing (Donut Chart)

| Property | Value |
|---|---|
| Chart type | Doughnut |
| Title | "NCC Cadets by Wing — AY [YYYY-YY]" |
| Data | Four segments: Army Wing / Naval Wing / Air Wing / Girls Wing |
| Segment colours | Army Wing = khaki (`#a16207`) · Naval Wing = navy (`#1e3a5f`) · Air Wing = sky blue (`#0ea5e9`) · Girls Wing = rose (`#f43f5e`) |
| Legend | Right side; wing name + cadet count |
| Centre label | "Total NCC Cadets: [N]" |
| Tooltip | "[Wing]: [N] cadets ([X]% of total)" |
| Empty state | Icon: shield (grey); Heading: "No NCC data available for this AY."; Body: "Cadet enrolment and wing data will appear once NCC units are registered." |
| Export PNG | Top-right download icon; filename: `ncc-cadets-by-wing-{ay}.png` |
| API endpoint | `GET /api/v1/group/{group_id}/analytics/extracurricular/ncc/cadets-by-wing/?ay={ay}` |
| HTMX trigger | `hx-trigger="load"` on page load; `hx-trigger="ayChanged from:body"` on AY change |
| HTMX target | `#chart-ncc-cadets-by-wing` |

---

### Section D — Library Charts

*Visible to: Library Head (101), Sports Director (97), Cultural Head (99, view only), NSS/NCC Coordinator (100, view only), Chairman/CEO (G4/G5).*
*Not shown to Sports Coordinator (98).*

#### Chart 7.9 — Library Resource Access per Month (Line Chart)

| Property | Value |
|---|---|
| Chart type | Line with filled area |
| Title | "Library Resource Accesses per Month — Last 6 Months" |
| X-axis | Month labels (MMM YYYY); last 6 calendar months |
| Y-axis | Total downloads + views combined; label: "Resource Accesses"; integer ticks |
| Line colour | Teal (`#0d9488`); area fill with 20% opacity |
| Data points | Circular markers (r=4) on each month |
| Tooltip | "[MMM YYYY]: [N] accesses ([D] downloads + [V] views)" |
| Empty state | Icon: book-open (grey); Heading: "No library access data for this period."; Body: "Data will appear once branches access distributed resources." |
| Export PNG | Top-right download icon; filename: `library-access-monthly.png` |
| API endpoint | `GET /api/v1/group/{group_id}/analytics/extracurricular/library/access-monthly/?ay={ay}` |
| HTMX trigger | `hx-trigger="load"` on page load; `hx-trigger="ayChanged from:body"` on AY change |
| HTMX target | `#chart-library-access-monthly` |

---

#### Chart 7.10 — Resource Type Usage (Vertical Bar Chart)

| Property | Value |
|---|---|
| Chart type | Vertical bar |
| Title | "Downloads by Resource Type — AY [YYYY-YY]" |
| X-axis | Resource type labels (all 10 types from Library Resource Catalogue); rotated 30° |
| Y-axis | Download count for the selected AY; label: "Downloads"; integer ticks |
| Bar colours | Matching resource-type badge colours as defined in Library Resource Catalogue (page 18) |
| Tooltip | "[Type]: [N] downloads in AY [YYYY-YY]" |
| Empty state | Icon: file-text (grey); Heading: "No resource download data for this AY."; Body: "Download counts will appear once library resources are accessed by branches." |
| Export PNG | Top-right download icon; filename: `library-usage-by-type-{ay}.png` |
| API endpoint | `GET /api/v1/group/{group_id}/analytics/extracurricular/library/usage-by-type/?ay={ay}` |
| HTMX trigger | `hx-trigger="load"` on page load; `hx-trigger="ayChanged from:body"` on AY change |
| HTMX target | `#chart-library-usage-by-type` |

---

### Section E — Achievements Charts

*Visible to: All roles with page access.*

#### Chart 7.11 — Student Achievements by Level — Last 3 AYs (Stacked Bar Chart)

| Property | Value |
|---|---|
| Chart type | Stacked vertical bar |
| Title | "Student Achievements by Level — Last 3 Academic Years" |
| X-axis | Academic years: last 3 AYs (e.g., 2023-24 / 2024-25 / 2025-26) |
| Y-axis | Count of achievement records; label: "Achievements Recorded"; integer ticks |
| Stacks (bottom to top) | School/Branch (grey `#9ca3af`) · District (blue `#3b82f6`) · State (indigo `#6366f1`) · National (red `#ef4444`) · International (gold `#eab308`) |
| Legend | Below chart; level label + colour swatch |
| Tooltip | "[AY] — [Level]: [N] achievements; Total across all levels: [N]" |
| Empty state | Icon: award (grey); Heading: "No achievement records for the last 3 academic years."; Body: "Records will appear once achievements are added to the register." |
| Export PNG | Top-right download icon; filename: `achievements-by-level-trend.png` |
| API endpoint | `GET /api/v1/group/{group_id}/analytics/extracurricular/achievements/by-level-trend/?ay={ay}` |
| HTMX trigger | `hx-trigger="load"` on page load; `hx-trigger="ayChanged from:body"` on AY change |
| HTMX target | `#chart-achievements-level-trend` |

---

#### Chart 7.12 — Achievements by Category (Donut Chart)

| Property | Value |
|---|---|
| Chart type | Doughnut |
| Title | "Achievements by Category — AY [YYYY-YY]" |
| Data | One segment per category; count of records in selected AY |
| Segment colours | 10-colour colorblind-safe palette matching category badge colours (Sports=blue, Cultural=purple, NSS/NCC=olive, Literary=teal, Science=orange, External=yellow, State Rep=indigo, National Rep=red, International=gold, Other=grey) |
| Legend | Right side; category label + count |
| Centre label | "Total: [N] Achievements" |
| Tooltip | "[Category]: [N] achievements ([X]% of total)" |
| Empty state | Icon: pie-chart (grey); Heading: "No achievement records for this AY."; Body: "Records will appear once achievements are added to the register." |
| Export PNG | Top-right download icon; filename: `achievements-by-category-{ay}.png` |
| API endpoint | `GET /api/v1/group/{group_id}/analytics/extracurricular/achievements/by-category/?ay={ay}` |
| HTMX trigger | `hx-trigger="load"` on page load; `hx-trigger="ayChanged from:body"` on AY change |
| HTMX target | `#chart-achievements-by-category` |

---

## 8. Toast Messages

| Action | Toast Text | Type | Duration |
|---|---|---|---|
| AY selector changed | "Analytics updated for AY [YYYY-YY]." | Success | 3 s |
| Export triggered | "Your analytics export is being prepared. It will download automatically when ready." | Info | Persists until export completes or fails |
| Export complete / download ready | "Your analytics export is ready. [Download ↓]" | Success | Persists until dismissed |
| Export failed | "Export generation failed. Please try again." | Error | 8 s |
| Section load error (any section) | "Could not load [Section Name] data. Please refresh the page or try again." | Warning | 6 s |
| Chart load error — Chart 7.1 | "Sports Participation Trend could not load. Refresh to retry." | Warning | 6 s |
| Chart load error — Chart 7.2 | "Sport-wise Team Count could not load. Refresh to retry." | Warning | 6 s |
| Chart load error — Chart 7.3 | "Tournament Count chart could not load. Refresh to retry." | Warning | 6 s |
| Chart load error — Chart 7.4 | "Cultural Events Monthly chart could not load. Refresh to retry." | Warning | 6 s |
| Chart load error — Chart 7.5 | "Cultural Participation by Branch could not load. Refresh to retry." | Warning | 6 s |
| Chart load error — Chart 7.6 | "NSS Hours Distribution could not load. Refresh to retry." | Warning | 6 s |
| Chart load error — Chart 7.7 | "NSS Activities Monthly could not load. Refresh to retry." | Warning | 6 s |
| Chart load error — Chart 7.8 | "NCC Cadets by Wing could not load. Refresh to retry." | Warning | 6 s |
| Chart load error — Chart 7.9 | "Library Access Monthly could not load. Refresh to retry." | Warning | 6 s |
| Chart load error — Chart 7.10 | "Resource Type Usage could not load. Refresh to retry." | Warning | 6 s |
| Chart load error — Chart 7.11 | "Achievements by Level Trend could not load. Refresh to retry." | Warning | 6 s |
| Chart load error — Chart 7.12 | "Achievements by Category could not load. Refresh to retry." | Warning | 6 s |
| Drilldown drawer load error | "Could not load branch data. Please try again." | Error | 6 s |
| PNG export triggered (per chart) | "Chart image downloading…" | Info | 2 s |

All chart load errors are handled gracefully: the chart container displays the chart-specific empty state (icon + heading + body) rather than an error page. The toast runs in parallel with the graceful empty state — the user sees both the inline empty state and the brief warning toast.

---

## 9. Empty States

### Per Section

| Section | Icon | Heading | Body | CTA |
|---|---|---|---|---|
| Cross-Division Overview (5.1) — no data | chart-bar (grey) | "No cross-division data for this academic year." | "Activity records will appear here once branches log data across all domains." | None |
| Cross-Division Overview (5.1) — no results for filters | filter (grey) | "No branches match the current filters." | "Try adjusting or clearing the State and Branch Type filters." | `Clear Filters` button |
| Heatmap (5.2) — no branches | grid (grey) | "No branches found for this academic year." | "Branches will appear once they are active and have data in the selected AY." | None |
| Drilldown drawer (6.1) — no activity in domain | calendar-x (grey) | "No [Domain] activity for [Branch Name]." | "Activity will appear here once data is logged for this branch and domain in AY [YYYY-YY]." | None |

### Per Chart

| Chart | Icon | Heading | Body |
|---|---|---|---|
| 7.1 Sports Participation Trend | line-chart (grey) | "No sports participation data available." | "Data will appear once sports teams and athletes are registered." |
| 7.2 Sport-wise Team Count | bar-chart (grey) | "No sports teams registered for this AY." | "Teams will appear once registered via the Sports Management page." |
| 7.3 Tournament Count per Sport | trophy (grey) | "No tournaments recorded for this AY." | "Tournament data will appear once events are logged in the Sports Management page." |
| 7.4 Cultural Events per Month | calendar (grey) | "No cultural events recorded in this period." | "Events will appear once recorded on the Cultural Events Calendar." |
| 7.5 Cultural Participation by Branch | users (grey) | "No cultural participation data for this AY." | "Branch participation data will appear once cultural events are logged." |
| 7.6 NSS Hours Distribution | clock (grey) | "No NSS data available for this AY." | "Volunteer hours data will appear once NSS units log data." |
| 7.7 NSS Activity Count per Month | leaf (grey) | "No NSS activities recorded in this period." | "Activity counts will appear once NSS units log data." |
| 7.8 NCC Cadets by Wing | shield (grey) | "No NCC data available for this AY." | "Cadet enrolment data will appear once NCC units are registered." |
| 7.9 Library Access per Month | book-open (grey) | "No library access data for this period." | "Data will appear once branches access distributed resources." |
| 7.10 Resource Type Usage | file-text (grey) | "No resource download data for this AY." | "Download counts will appear once library resources are accessed by branches." |
| 7.11 Achievements by Level Trend | award (grey) | "No achievement records for the last 3 academic years." | "Records will appear once achievements are added to the register." |
| 7.12 Achievements by Category | pie-chart (grey) | "No achievement records for this AY." | "Records will appear once achievements are added to the register." |

---

## 10. Loader States

| Context | Loader Behaviour |
|---|---|
| Initial page load — full skeleton | 8 KPI card shimmer placeholders (4×2 grid) + overview table skeleton (8 grey rows × 8 columns) + heatmap skeleton (grey grid, all cells uniform grey) + 12 chart skeletons (grey rounded rectangles, animated shimmer, 300×200 px each) |
| AY selector change | Semi-transparent overlay (opacity 60%, background `#f9fafb`) covers the entire analytics content area below the page header; centred spinner with label "Loading AY [YYYY-YY]…"; resolves section by section as HTMX responses arrive (OOB swap) |
| Per-section tab switch (if tabs exist) | The section body shows a grey shimmer block matching the previous content height; resolves to loaded content |
| KPI bar — individual card load or refresh | Each KPI card shows an individual shimmer pulse (width: full card, height: 80px); resolves independently as each card's HTMX request completes |
| Chart load (individual, on page load) | Per-chart: grey rounded rectangle with a centred grey spinner; height matches the final chart height (250px standard); animated shimmer border |
| Chart refresh (on AY change) | Per-chart: existing chart fades to 30% opacity; spinner overlaid on centre; resolves when new data arrives |
| Drilldown drawer open | Drawer slides in from right (300ms ease); drawer body shows skeleton: 2 tab header shimmer blocks + 5 grey field rows (label + value) per tab; resolves when API response arrives |
| Export generation | `Export All ↓` button shows inline spinner + label changes to "Generating…"; button disabled (pointer-events none, opacity 70%); info toast displayed (see Section 8); button restores on completion or failure |
| Overview table filter apply | Table body shows spinner overlay centred on the tbody; tbody opacity 40%; resolves to filtered results |
| Overview table pagination | Same as filter apply: tbody spinner; resolves to new page |

---

## 11. Role-Based UI Visibility

| UI Element | Sports Dir (97) | Sports Coord (98) | Cultural Head (99) | NSS/NCC Coord (100) | Library Head (101) | Chairman (G4/G5) |
|---|---|---|---|---|---|---|
| AY Selector | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Export All button | ✅ (all sections) | ✅ (sports + achievements only) | ✅ (all sections) | ✅ (all sections) | ✅ (library + achievements only) | ❌ Hidden |
| KPI cards 1–2 (Sports) | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ |
| KPI cards 3 (Cultural) | ✅ | ❌ | ✅ | ✅ | ❌ | ✅ |
| KPI cards 4–5 (NSS/NCC) | ✅ | ❌ | ✅ | ✅ | ❌ | ✅ |
| KPI card 6 (Library) | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ |
| KPI card 7 (Achievements) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| KPI card 8 (Full Programme) | ✅ | ❌ | ✅ | ✅ | ❌ | ✅ |
| 5.1 Cross-Division Overview table | ✅ Full | ❌ Hidden | ✅ Full | ✅ Full | ❌ Hidden | ✅ View only |
| 5.2 Branch Health Heatmap | ✅ Full | ❌ Hidden | ✅ Full | ✅ Full | ❌ Hidden | ✅ View only |
| 6.1 Drilldown drawer | ✅ | ❌ | ✅ | ✅ | ❌ | ✅ View only |
| Charts 7.1–7.3 (Sports section) | ✅ Full | ✅ Full | ✅ View only | ✅ View only | ❌ Hidden | ✅ View only |
| Charts 7.4–7.5 (Cultural section) | ✅ Full | ❌ Hidden | ✅ Full | ✅ View only | ❌ Hidden | ✅ View only |
| Charts 7.6–7.8 (NSS/NCC section) | ✅ Full | ❌ Hidden | ✅ View only | ✅ Full | ❌ Hidden | ✅ View only |
| Charts 7.9–7.10 (Library section) | ✅ View only | ❌ Hidden | ✅ View only | ✅ View only | ✅ Full | ✅ View only |
| Charts 7.11–7.12 (Achievements section) | ✅ Full | ✅ Full | ✅ Full | ✅ Full | ✅ Full | ✅ View only |
| Per-chart PNG export | ✅ | ✅ (visible charts) | ✅ | ✅ | ✅ (visible charts) | ❌ Hidden |
| Alert banners | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

"View only" means the section is visible and interactive (tooltips, PNG export) but the role cannot trigger write actions. Since this page has no write actions, "view only" and "full" are functionally equivalent here; the distinction is preserved for consistency with the Role Access table in Section 2.

---

## 12. API Endpoints

### Base URL: `/api/v1/group/{group_id}/analytics/extracurricular/`

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/analytics/extracurricular/kpi/` | KPI summary bar — all 8 cards, role-filtered; returns only cards the requesting role may see | JWT + role check |
| GET | `/api/v1/group/{group_id}/analytics/extracurricular/overview/` | Cross-division engagement table data (section 5.1) | JWT + role check |
| GET | `/api/v1/group/{group_id}/analytics/extracurricular/heatmap/` | Branch health heatmap grid data (section 5.2) | JWT + role check |
| GET | `/api/v1/group/{group_id}/analytics/extracurricular/drilldown/{branch_id}/{domain}/` | Branch + domain drilldown drawer data (section 6.1); `domain` = `sports` / `cultural` / `nss` / `ncc` / `library` | JWT + role check |
| GET | `/api/v1/group/{group_id}/analytics/extracurricular/sports/participation-trend/` | Chart 7.1 data — last 3 AYs, total + day scholars + hostelers | JWT + role check |
| GET | `/api/v1/group/{group_id}/analytics/extracurricular/sports/team-count/` | Chart 7.2 data — top 10 sports by team count | JWT + role check |
| GET | `/api/v1/group/{group_id}/analytics/extracurricular/sports/tournament-count/` | Chart 7.3 data — tournament count per sport | JWT + role check |
| GET | `/api/v1/group/{group_id}/analytics/extracurricular/cultural/events-monthly/` | Chart 7.4 data — events per month, last 12 months | JWT + role check |
| GET | `/api/v1/group/{group_id}/analytics/extracurricular/cultural/branch-participation/` | Chart 7.5 data — top 10 branches by cultural events | JWT + role check |
| GET | `/api/v1/group/{group_id}/analytics/extracurricular/nss/hours-distribution/` | Chart 7.6 data — NSS volunteer hours distribution | JWT + role check |
| GET | `/api/v1/group/{group_id}/analytics/extracurricular/nss/activities-monthly/` | Chart 7.7 data — NSS activities per month, last 6 months | JWT + role check |
| GET | `/api/v1/group/{group_id}/analytics/extracurricular/ncc/cadets-by-wing/` | Chart 7.8 data — NCC cadets by wing | JWT + role check |
| GET | `/api/v1/group/{group_id}/analytics/extracurricular/library/access-monthly/` | Chart 7.9 data — library accesses per month, last 6 months | JWT + role check |
| GET | `/api/v1/group/{group_id}/analytics/extracurricular/library/usage-by-type/` | Chart 7.10 data — downloads by resource type | JWT + role check |
| GET | `/api/v1/group/{group_id}/analytics/extracurricular/achievements/by-level-trend/` | Chart 7.11 data — achievements by level, last 3 AYs | JWT + role check |
| GET | `/api/v1/group/{group_id}/analytics/extracurricular/achievements/by-category/` | Chart 7.12 data — achievements by category | JWT + role check |
| POST | `/api/v1/group/{group_id}/analytics/extracurricular/export/` | Trigger server-side full analytics export generation; returns `{job_id}` | JWT + role check (Chairman/CEO excluded) |
| GET | `/api/v1/group/{group_id}/analytics/extracurricular/export/{job_id}/status/` | Poll export job status; returns `{status: "pending"/"generating"/"complete"/"failed", download_url}` | JWT + role check |
| GET | `/api/v1/group/{group_id}/analytics/extracurricular/export/{job_id}/download/` | Download completed export file | JWT + role check |

**Common query parameters (applicable to all GET endpoints above):**

| Parameter | Type | Description | Required |
|---|---|---|---|
| `ay` | str | Academic year slug, e.g., `2025-26` (default: current AY) | No |
| `branch` | int[] | Filter to specific branch IDs; used in overview and drilldown endpoints | No |
| `state` | str[] | Filter branches by state code; used in overview endpoint | No |
| `branch_type` | str | `day` / `residential` / `all` (default: `all`); used in overview endpoint | No |
| `format` | str | Export format: `pdf` / `xlsx` (default: `pdf`); used in export endpoint only | No |

---

## 13. HTMX Patterns

| Pattern | Trigger Element | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| Page load — KPI cards (all 8) | Each `#kpi-card-{n}` div | `hx-get="/api/.../extracurricular/kpi/?card={n}&ay={ay}"` | `#kpi-card-{n}` | `outerHTML` | `hx-trigger="load"` on each card; 8 independent requests; role-filtered server-side |
| AY selector change — refresh all sections | `#ay-selector` dropdown | `hx-get="/api/.../extracurricular/kpi/?ay={selected}"` | `#kpi-bar` | `outerHTML` with `hx-swap-oob="true"` on each section target | `hx-trigger="change"`; JS dispatches `ayChanged` custom event from `document.body`; all chart and table containers listen for `ayChanged from:body` and fire their own requests |
| AY selector change — refresh KPI bar | `document.body` (listener) | `hx-get="/api/.../extracurricular/kpi/?ay={ay}"` | `#kpi-bar` | `innerHTML` | `hx-trigger="ayChanged from:body"` `hx-include="#ay-selector"` |
| AY selector change — refresh overview table | `document.body` (listener) | `hx-get="/api/.../extracurricular/overview/?ay={ay}"` | `#overview-table-body` | `innerHTML` | `hx-trigger="ayChanged from:body"` `hx-include="#ay-selector,#overview-filter-form"` |
| AY selector change — refresh heatmap | `document.body` (listener) | `hx-get="/api/.../extracurricular/heatmap/?ay={ay}"` | `#heatmap-container` | `innerHTML` | `hx-trigger="ayChanged from:body"` `hx-include="#ay-selector"` |
| AY selector change — refresh each chart (×12) | `document.body` (listener) per chart container | `hx-get="/api/.../extracurricular/{domain}/{chart-slug}/?ay={ay}"` | `#chart-{chart-slug}` | `innerHTML` | `hx-trigger="ayChanged from:body"` `hx-include="#ay-selector"`; one listener per chart container; 12 independent requests |
| Section A (Sports) KPI bar load | `#kpi-sports-section` | `hx-get="/api/.../extracurricular/kpi/?section=sports&ay={ay}"` | `#kpi-sports-section` | `outerHTML` | `hx-trigger="load"` |
| Section B (Cultural) KPI bar load | `#kpi-cultural-section` | `hx-get="/api/.../extracurricular/kpi/?section=cultural&ay={ay}"` | `#kpi-cultural-section` | `outerHTML` | `hx-trigger="load"` |
| Section C (NSS/NCC) KPI bar load | `#kpi-nss-section` | `hx-get="/api/.../extracurricular/kpi/?section=nss&ay={ay}"` | `#kpi-nss-section` | `outerHTML` | `hx-trigger="load"` |
| Section D (Library) KPI bar load | `#kpi-library-section` | `hx-get="/api/.../extracurricular/kpi/?section=library&ay={ay}"` | `#kpi-library-section` | `outerHTML` | `hx-trigger="load"` |
| Chart 7.1 load | `#chart-sports-participation-trend` | `hx-get="/api/.../extracurricular/sports/participation-trend/?ay={ay}"` | `#chart-sports-participation-trend` | `innerHTML` | `hx-trigger="load"` |
| Chart 7.2 load | `#chart-sport-teams` | `hx-get="/api/.../extracurricular/sports/team-count/?ay={ay}"` | `#chart-sport-teams` | `innerHTML` | `hx-trigger="load"` |
| Chart 7.3 load | `#chart-tournament-count` | `hx-get="/api/.../extracurricular/sports/tournament-count/?ay={ay}"` | `#chart-tournament-count` | `innerHTML` | `hx-trigger="load"` |
| Chart 7.4 load | `#chart-cultural-events-monthly` | `hx-get="/api/.../extracurricular/cultural/events-monthly/?ay={ay}"` | `#chart-cultural-events-monthly` | `innerHTML` | `hx-trigger="load"` |
| Chart 7.5 load | `#chart-cultural-branch-participation` | `hx-get="/api/.../extracurricular/cultural/branch-participation/?ay={ay}"` | `#chart-cultural-branch-participation` | `innerHTML` | `hx-trigger="load"` |
| Chart 7.6 load | `#chart-nss-hours-distribution` | `hx-get="/api/.../extracurricular/nss/hours-distribution/?ay={ay}"` | `#chart-nss-hours-distribution` | `innerHTML` | `hx-trigger="load"` |
| Chart 7.7 load | `#chart-nss-activities-monthly` | `hx-get="/api/.../extracurricular/nss/activities-monthly/?ay={ay}"` | `#chart-nss-activities-monthly` | `innerHTML` | `hx-trigger="load"` |
| Chart 7.8 load | `#chart-ncc-cadets-by-wing` | `hx-get="/api/.../extracurricular/ncc/cadets-by-wing/?ay={ay}"` | `#chart-ncc-cadets-by-wing` | `innerHTML` | `hx-trigger="load"` |
| Chart 7.9 load | `#chart-library-access-monthly` | `hx-get="/api/.../extracurricular/library/access-monthly/?ay={ay}"` | `#chart-library-access-monthly` | `innerHTML` | `hx-trigger="load"` |
| Chart 7.10 load | `#chart-library-usage-by-type` | `hx-get="/api/.../extracurricular/library/usage-by-type/?ay={ay}"` | `#chart-library-usage-by-type` | `innerHTML` | `hx-trigger="load"` |
| Chart 7.11 load | `#chart-achievements-level-trend` | `hx-get="/api/.../extracurricular/achievements/by-level-trend/?ay={ay}"` | `#chart-achievements-level-trend` | `innerHTML` | `hx-trigger="load"` |
| Chart 7.12 load | `#chart-achievements-by-category` | `hx-get="/api/.../extracurricular/achievements/by-category/?ay={ay}"` | `#chart-achievements-by-category` | `innerHTML` | `hx-trigger="load"` |
| Overview table load | `#overview-table-body` | `hx-get="/api/.../extracurricular/overview/?ay={ay}"` | `#overview-table-body` | `innerHTML` | `hx-trigger="load"` `hx-include="#ay-selector,#overview-filter-form"` |
| Overview table filter apply | `#overview-filter-form` inputs | `hx-get="/api/.../extracurricular/overview/"` | `#overview-table-body` | `innerHTML` | `hx-trigger="change"` on each filter input; `hx-include="#overview-filter-form,#ay-selector"` |
| Overview table pagination | Pagination `<a>` links | `hx-get="/api/.../extracurricular/overview/?page={n}&ay={ay}"` | `#overview-table-body` | `innerHTML` | `hx-push-url="true"` to update `?page=` in URL |
| Heatmap load | `#heatmap-container` | `hx-get="/api/.../extracurricular/heatmap/?ay={ay}"` | `#heatmap-container` | `innerHTML` | `hx-trigger="load"` `hx-include="#ay-selector"` |
| Heatmap cell click — drilldown drawer | Each heatmap `<td>` cell | `hx-get="/api/.../extracurricular/drilldown/{branch_id}/{domain}/?ay={ay}"` | `#drawer-container` | `innerHTML` | `hx-trigger="click"`; drawer slides in; URL updated via `hx-push-url="true"` |
| Drilldown drawer tab switch | Tab nav buttons inside drawer | `hx-get="/api/.../extracurricular/drilldown/{branch_id}/{domain}/?ay={ay}&tab={tab_slug}"` | `#drawer-tab-content` | `innerHTML` | `hx-trigger="click"` on each tab button |
| Export trigger | `#export-all-btn` button | `hx-post="/api/.../extracurricular/export/"` | `#export-status` | `innerHTML` | `hx-trigger="click"` `hx-include="#ay-selector"`; body also carries `format` param (default `pdf`); button disabled after click |
| Export status polling | `#export-status` div | `hx-get="/api/.../extracurricular/export/{job_id}/status/"` | `#export-status` | `outerHTML` | `hx-trigger="every 5s"` injected into `#export-status` by server response; polling stops when server returns `status=complete` or `status=failed` (server renders final state without the polling trigger) |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
