# K-01 — Sales Dashboard

**Route:** `GET /group1/k/dashboard/`
**Method:** Django `TemplateView` + HTMX part-loads
**Primary role:** B2B Sales Manager (#57)
**Also sees (restricted view):** Sales Execs #58/#59/#60 (own segment only), Inside Sales #97 (own inbound leads only), Sales Ops #95 (read-only all data), Partnership Manager #61 (pipeline read + partnership strip), Channel Partner Manager #63 (channel metrics strip only), Demo Manager #62 (upcoming demos strip + demo KPIs)

---

## Purpose

Central command view for the Sales & Business Development division. The B2B Sales Manager uses this as the morning briefing screen — complete funnel health, quota attainment per exec, team leaderboard, stale lead alerts, and upcoming demo calendar. Sales Execs see only their own segment metrics. Sales Ops Analyst reads everything in full without any write actions. Demo Manager sees the demo strip and demo KPIs only. The dashboard consolidates data from six data sources into a single viewport to avoid context-switching during daily standups and pipeline review sessions.

---

## Data Sources

| Section | Source | Cache TTL |
|---|---|---|
| KPI strip — pipeline value | `sales_lead` WHERE stage NOT IN ('CLOSED_WON','CLOSED_LOST') — SUM arr_estimate_paise | 5 min |
| KPI strip — closed MTD | `sales_lead` WHERE stage='CLOSED_WON' AND won_at in selected period — COUNT + SUM | 5 min |
| KPI strip — quota attainment | `sales_quota` + CLOSED_WON arr in period (from `analytics_quota_attainment`) | 15 min |
| KPI strip — avg deal size | `sales_lead` WHERE stage='CLOSED_WON' AND won_at in period — AVG arr_estimate_paise | 5 min |
| KPI strip — demo-to-close rate | CLOSED_WON count / (DEMO_DONE + PROPOSAL_SENT + NEGOTIATION + CLOSED_WON + CLOSED_LOST count) × 100 | 10 min |
| Pipeline funnel chart | `analytics_sales_funnel` (written by Task K-1 every 6 hours) | 60 min |
| Team leaderboard | `sales_lead` GROUP BY owner_id WHERE won_at in period; joined to auth_user | 10 min |
| Stale leads widget | `sales_lead` LEFT JOIN `sales_activity` MAX occurred_at; WHERE last activity > 14 days OR no activity since creation > 7 days | 30 min |
| Upcoming demos | `sales_activity` WHERE activity_type='DEMO' AND occurred_at BETWEEN now() AND now()+7d; joined to `sales_demo_tenant` | 5 min |
| Recent activities feed | `sales_activity` ORDER BY occurred_at DESC LIMIT 20 | 2 min |

All caches keyed on `(user_id, period, segment, territory)`. Manager (#57) and Ops (#95) caches are org-wide; exec caches are scoped to owner_id. `?nocache=true` bypasses Memcached for Manager (#57) only.

---

## URL Parameters

| Param | Values | Default | Effect |
|---|---|---|---|
| `?period` | `month`, `quarter`, `ytd` | `month` | Sets the reporting window for all period-dependent KPIs and the leaderboard |
| `?segment` | `all`, `school`, `college`, `coaching` | `all` | Filters the funnel chart, stale leads, leaderboard, and demos to one institution type |
| `?owner` | user_id or `me` | `me` (exec) / `all` (manager) | Scopes the pipeline value, stale leads, and activities to one exec; Manager/Ops only for non-`me` values |
| `?territory` | territory enum value | — | Filters all sections to one territory; Manager and Ops only |

---

## HTMX Part-Load Routes

| Route | Component | Trigger | Auto-Refresh | Target ID |
|---|---|---|---|---|
| `htmx/k/kpi-strip/` | KPI Strip | Page load + period/segment change | 10 min | `#k-kpi-strip` |
| `htmx/k/funnel-chart/` | Pipeline Funnel | Page load + filter change | 30 min | `#k-funnel-chart` |
| `htmx/k/leaderboard/` | Team Leaderboard | Page load + period change | 10 min | `#k-leaderboard` |
| `htmx/k/stale-leads/` | Stale Leads Widget | Page load | 30 min | `#k-stale-leads` |
| `htmx/k/upcoming-demos/` | Upcoming Demos Strip | Page load | 5 min | `#k-upcoming-demos` |
| `htmx/k/recent-activities/` | Recent Activities Feed | Page load | 2 min | `#k-recent-activities` |

Each part responds with an HTML fragment only; no full page reload required. Filter changes use `hx-push-url="true"` to keep the URL in sync with the current filter state for bookmarking and sharing.

---

## Page Layout

```
┌─────────────────────────────────────────────────────────────────────┐
│  SALES DASHBOARD      [Period: Month▼]  [Segment: All▼]  [Refresh] │
├──────────────┬─────────────┬─────────────┬────────────┬────────────┤
│  Pipeline    │  Closed MTD │  Quota      │  Avg Deal  │  Demo-to-  │
│  Value       │  12 deals   │  Attain %   │  Size      │  Close %   │
│  ₹4.2Cr      │  ₹38.4L ARR │  68%  ↑+5  │  ₹3.5L     │  42%       │
├──────────────┴─────────────┴─────────────┴────────────┴────────────┤
│  Pipeline Funnel (Chart.js horizontal bars)  │  Team Leaderboard   │
│                                              │  (Manager/Ops only) │
│  PROSPECT    ████████████████  28 · ₹9.8L   │  # │ Exec │Deals│ARR│
│  CONTACTED   █████████████    31 · ₹10.9L   │  1 │Rahul │  5  │75L│
│  DEMO SCHED  ████████         18 · ₹6.3L    │  2 │Priya │  4  │60L│
│  DEMO DONE   ████████         22 · ₹7.7L    │  3 │Arjun │  3  │45L│
│  PROPOSAL    ███████          19 · ₹6.7L    │  ── colour-coded ── │
│  NEGOTIATION █████            11 · ₹3.9L    │  green/amber/red    │
│  WON  ██  8  │  LOST  █  5   │             │  (click → K-02)     │
│  (click bar → K-02 filtered to stage)       │                     │
├─────────────────────────────────────────────┤                     │
│  Stale Leads (no activity 14d+)             ├─────────────────────┤
│  Institution    │Stage    │Owner│Age │Close │  Upcoming Demos (7d)│
│  KIMS School    │PROPOSAL │Rahul│18d │5d    │  Inst │Date │Owner  │
│  SR College     │DEMO_DONE│Priya│22d │-3d ▲ │  ─────────────────  │
│  [View All →]   (K-02?stale=true)           │  (→K-03 on click)  │
├─────────────────────────────────────────────┴─────────────────────┤
│  Recent Activity Feed                                              │
│  [icon] [Who] logged a [type] with [Institution] · [time ago]     │
│  [stage badge]   [outcome badge]                                  │
└────────────────────────────────────────────────────────────────────┘
```

---

## Components

### KPI Strip (5 tiles)

```
┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ ₹4.2Cr       │ │ 12 deals     │ │ 68%          │ │ ₹3.5L        │ │ 42%          │
│ Pipeline     │ │ Closed MTD   │ │ Quota        │ │ Avg Deal     │ │ Demo-to-     │
│ Value        │ │ ₹38.4L ARR   │ │ Attainment   │ │ Size (won)   │ │ Close Rate   │
│ (open stages)│ │ ↑+3 vs L.Mo. │ │ ↑+5 pts      │ │ ↓ ₹0.3L      │ │ ↑+4 pts      │
└──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘
```

**Tile 1 — Pipeline Value:** SUM of `arr_estimate_paise` for all leads WHERE stage NOT IN ('CLOSED_WON', 'CLOSED_LOST'), filtered by period's expected_close_date window if `?period` set. Formatted as ₹X.XCr or ₹X.XL. Sub-label: "N active leads". For execs: own leads only. For Manager/Ops: org-wide with territory filter option.

**Tile 2 — Closed MTD/QTD/YTD:** COUNT and SUM arr_estimate_paise WHERE stage='CLOSED_WON' AND won_at falls within the selected period window. Shows `↑+N vs last period` or `↓-N`. Red badge if count < 50% of target_deals for the period. For execs: own only.

**Tile 3 — Quota Attainment %:** Reads from `analytics_quota_attainment` (Task K-2 output). Formula: actual_arr_paise / target_arr_paise × 100, rounded to 1 decimal. Colour: green ≥ 100%, amber 70–99%, red < 70%. Shows delta vs previous period. Manager sees org-wide average; tooltip shows per-exec breakdown.

**Tile 4 — Avg Deal Size:** AVG(arr_estimate_paise) WHERE stage='CLOSED_WON' AND won_at in period. Formatted as ₹X.XL. Shows delta vs last period. Guard: if 0 closed deals in period, shows "— (no wins yet)" in grey. Useful for detecting ARR dilution from heavy discounting.

**Tile 5 — Demo-to-Close Rate:** **Demo-to-Close Rate:** COUNT(CLOSED_WON leads WHERE a sales_activity of type='DEMO' with outcome in ('POSITIVE','NEUTRAL') exists on the lead) ÷ COUNT(all leads where any sales_activity of type='DEMO' exists) × 100. Note: Activity-based definition (not stage-history-based) — counts any lead with a logged DEMO activity as having "reached demo stage", regardless of current lead stage. This avoids the need for a stage history table. Guard: if fewer than 5 demos in period, shows "Low data" in amber. Tracked as a conversion health metric for the Demo Manager's calibration.

Edge cases: If denominator (leads that reached DEMO_DONE or later) < 5 in the period, tile shows "Low data" in amber with tooltip "Less than 5 demos completed this period — rate may not be representative." If denominator = 0, shows "—" (em-dash, not 0%).

**Loading state:** While HTMX partial loads or auto-refreshes, tiles show a shimmer skeleton (grey animated block at tile height). Auto-refresh happens in-place — tiles update without full page reload. If refresh fails (network error), tiles retain stale values with a subtle grey border and "↻ Retry" icon.

**Role-based tile behaviour:**
- Sales Execs #58–60: All tiles visible but scoped to own leads. No delta vs last period on Tile 3 (quota set by manager; detail in K-07).
- Inside Sales #97: Tiles 1 and 2 visible scoped to own leads. Tiles 3–5 hidden (quota tracking not applicable to #97 in the same way).
- Demo Manager #62: Only Tile 5 (Demo-to-Close) visible; others hidden. Demo-specific KPIs shown in the Upcoming Demos section instead.
- Sales Ops #95: All tiles visible org-wide with additional "last computed" timestamp tooltip on Tile 3.

---

### Pipeline Funnel Chart

Horizontal bar chart rendered with Chart.js. One bar per pipeline stage in order: PROSPECT → CONTACTED → DEMO_SCHEDULED → DEMO_DONE → PROPOSAL_SENT → NEGOTIATION → CLOSED_WON → CLOSED_LOST. CLOSED_LOST rendered as a separate grey bar below the main funnel.

Each bar shows:
- Count of leads in stage (left label)
- Total ARR estimate for those leads (right label)
- Conversion rate from previous stage shown as a small percentage label on the bar: e.g., "DEMO_SCHEDULED → DEMO_DONE: 81%"

**Colour scheme:** PROSPECT=grey-400 → CONTACTED=blue-400 → DEMO_SCHEDULED=indigo-400 → DEMO_DONE=purple-400 → PROPOSAL_SENT=amber-400 → NEGOTIATION=orange-400 → CLOSED_WON=green-500 → CLOSED_LOST=red-300.

**Interaction:** Clicking a bar navigates to K-02 with `?stage=<stage>` pre-set (and any active segment/territory filters carried over via `hx-push-url`).

**Manager view:** Legend toggle allows switching between "All Execs" and individual exec view. Selecting an exec overlays their personal funnel as a lighter outline bar on each stage bar, making it easy to spot which exec has a bottleneck at a specific stage.

**Exec view:** Shows own funnel only. No exec legend toggle.

**Zero-lead stages:** A stage with 0 leads shows a minimal 2px bar in grey with "0" label. The conversion % from the previous stage shows "0%" in red. Clicking a zero-count stage bar still navigates to K-02 with that stage filter applied (will show empty state).

**Data source:** `analytics_sales_funnel` (Task K-1 output, 6-hour cache). Live data available via `?nocache=true` for Manager.

---

### Team Leaderboard

Visible only to B2B Sales Manager (#57) and Sales Ops Analyst (#95). Hidden for all other roles.

| Column | Description |
|---|---|
| Rank | Integer rank by ARR generated in period, descending |
| Exec Name | Full name (link → K-02?owner=<user_id>) |
| Segment | Primary segment badge (SCHOOL/COLLEGE/COACHING) |
| Deals Closed | COUNT CLOSED_WON in period |
| ARR Generated | SUM arr_estimate_paise CLOSED_WON in period, formatted |
| Quota Attainment % | From `analytics_quota_attainment`; colour-coded |

**Colour coding (entire row):**
- Green background: attainment ≥ 100%
- Amber background: attainment 70–99%
- Red background: attainment < 70%

**Sorting:** Default by ARR Generated descending. Clicking column headers re-sorts client-side (data pre-loaded in the partial).

**Row click:** Navigates to K-02 filtered to that exec's leads (`?owner=<user_id>`).

**Period toggle:** Respects `?period` URL param — leaderboard updates when period filter is changed at the top.

---

### Stale Leads Widget

Leads with no `sales_activity` record in the last 14 days (or leads created >7 days ago with zero activities). Maximum 10 rows shown; "View All" link to `K-02?stale=true`.

| Column | Description |
|---|---|
| Institution Name | Truncated to 28 chars (full name on hover); link → K-03 |
| Stage | Stage badge |
| Owner | Exec name (Manager sees all; Exec sees only own) |
| Days Since Last Activity | Integer; ≥ 14d shown in amber; ≥ 30d shown in red |
| Expected Close Date | Date; if in the past, shown with red "Overdue" badge |

**Red urgency badge:** A red badge overlays any row where the lead is stale AND its `expected_close_date` is within 7 days OR already past.

**[View All →]:** Links to K-02?stale=true. For execs, the link carries `?owner=me` implicitly.

**Exec visibility:** Execs see only their own stale leads. Manager sees all. Sales Ops sees all read-only.

**Empty state:** "No stale leads — great pipeline hygiene!" with a green checkmark icon.

---

### Upcoming Demos Strip

Horizontally scrollable card row showing demos scheduled in the next 7 days. Source: `sales_activity` WHERE activity_type='DEMO' AND occurred_at BETWEEN now() AND now()+7d, joined to `sales_demo_tenant` for tenant status.

```
┌──────────────────────────┐  ┌──────────────────────────┐  ┌──────────────────────────┐
│ KIMS School              │  │ Delhi Coaching Hub        │  │ Sunrise College Group    │
│ STANDARD demo            │  │ ENTERPRISE_POC            │  │ CUSTOM demo              │
│ Mon 23 Mar · 11:00       │  │ Wed 25 Mar · 14:30        │  │ Fri 27 Mar · 10:00       │
│ Owner: Rahul S.          │  │ Owner: Arjun M.           │  │ Owner: Priya K.          │
│ Tenant: ✓ Active         │  │ Tenant: ⚠ Not setup       │  │ Tenant: ✓ Active         │
│ [View Account →]         │  │ [Setup Demo Tenant →]     │  │ [View Account →]         │
└──────────────────────────┘  └──────────────────────────┘  └──────────────────────────┘
```

**Card border colour:** Green if tenant is active and ready; amber if demo is within 48 hours but no tenant is set up; red if demo is today and no tenant.

**[Setup Demo Tenant →]:** Visible to Demo Manager (#62) only. Links to K-04 pre-filled with the lead_id.

**[View Account →]:** Links to K-03 for the corresponding lead.

**For Demo Manager (#62):** This strip is the primary widget they see on the dashboard — all other sections (except the funnel chart in read-only mode) are hidden.

**Empty state:** "No demos scheduled in the next 7 days." with a calendar icon.

---

### Recent Activities Feed

Last 20 `sales_activity` records ordered by `occurred_at DESC`. For execs: own activities only (`logged_by = current_user`). For Manager/Ops: org-wide.

| Column | Description |
|---|---|
| Icon | Activity type icon: CALL, EMAIL, MEETING, DEMO, WHATSAPP, SITE_VISIT, PROPOSAL, RFP_RESPONSE |
| Who | Exec name who logged the activity |
| Activity Type | Formatted label |
| Institution | Institution name (link → K-03 for that lead) |
| Outcome | Badge: POSITIVE=green · NEUTRAL=grey · NEGATIVE=red · NO_SHOW=amber · RESCHEDULED=indigo |
| Time Ago | Relative time: "2h ago" / "Yesterday" / "3d ago" |
| Stage Badge | Current lead stage as a compact badge |

**"Log Activity" prompt:** If the current exec has any open lead with no activity in 48+ hours, a subtle amber prompt bar appears at the top of the feed: "You have N leads with no activity in 48h — [Log Activity →]" (links to K-02?stale=true).

**Row click:** Links to K-03 for the corresponding lead.

---

## Empty States

| Section | Condition | Message |
|---|---|---|
| KPI Strip — Closed MTD | No CLOSED_WON leads in the selected period | "No deals closed this period yet." with a target icon |
| Pipeline Funnel | No leads in the system for this exec/segment | "No pipeline data — start by creating your first lead." with [+ Create Lead] button |
| Team Leaderboard | Period just started, no closed deals by anyone | "Leaderboard will populate as deals close. First one wins!" |
| Stale Leads Widget | All leads have recent activity | "No stale leads — great pipeline hygiene!" with a green shield icon |
| Upcoming Demos | No demos scheduled in the next 7 days | "No demos scheduled in the next 7 days." with calendar icon |
| Recent Activities | No activities logged at all | "No recent activities. Start logging your calls and meetings." |
| Pre-Sales Engineer (#96) accessing dashboard | Role check | 403 redirect to K-03 (they are assigned to specific accounts, not the dashboard) |

---

## Toast Messages

| Action | Toast | Type |
|---|---|---|
| Period filter changed | "Dashboard updated to show [Month/Quarter/YTD] data." | Blue (info) |
| Segment filter changed | "Showing [segment] leads only." | Blue (info) |
| CLOSED_WON notification received (real-time via Django Channels) | "[Institution Name] — deal marked CLOSED_WON by [Exec]. ₹[ARR] ARR." | Green (success) |
| Stale lead alert — exec has a lead past its close date | "[Institution Name] expected close date has passed. Log an activity or update the close date." | Amber (warning) |
| `?nocache=true` used | "Cache bypassed — showing live pipeline data." | Blue (info) |
| Territory filter applied | "Showing [Territory] leads only." | Blue (info) |

---

---

## Authorization

**Route guard:** `@division_k_required(allowed_roles=[57, 58, 59, 60, 95, 97])` applied to `SalesDashboardView`.

| Scenario | Behaviour |
|---|---|
| Unauthenticated | Redirect to `/login/?next=/group1/k/dashboard/` |
| Wrong role (e.g., #62 Demo Manager navigates here) | 403 redirect to `/403/` |
| Sales Exec (#58–60) | Queryset filtered to `owner_id = request.user.id`; all KPI tiles show own data only |
| Sales Ops (#95) | Full read-only; no period/segment controls are blocked but all data is pre-aggregated (no raw query access) |

**HTMX partial security:** All partial-load routes (`htmx/k/kpi-strip/`, etc.) enforce the same role checks. Direct calls without a valid session return 403.

---

## Role-Based UI Visibility Summary

| Component | 57 Manager | 58/59/60 Execs | 95 Ops Analyst | #97 Inside Sales Exec | 61 Partnership | 62 Demo Manager (#62) |
|---|---|---|---|---|---|---|
| KPI Strip | All 5 tiles, org-wide | All 5 tiles, own segment | All 5 tiles, org-wide (read-only) | Tiles 1–2 own only | Pipeline value tile only | Tile 5 (Demo-to-Close) only |
| Pipeline Funnel Chart | Full, all execs, with exec toggle | Own segment only, no exec toggle | Full org-wide, no interactions | Own inbound leads | Read-only all | Read-only all |
| Team Leaderboard | Full — all execs, sortable | Hidden | Full — read-only | Hidden | Hidden | Hidden |
| Stale Leads Widget | All execs' stale leads | Own stale leads only | All stale leads read-only | Own inbound stale leads | Hidden | Hidden |
| Upcoming Demos Strip | Full — all execs' demos + tenant status | Own demos only | Full read-only | Hidden | Hidden | Full + [Setup Demo Tenant] links |
| Recent Activities Feed | Org-wide last 20 | Own activities last 20 | Org-wide read-only | Own activities only | Hidden | Own demo activities only |
| [?nocache=true] | Yes | No | No | No | No | No |
