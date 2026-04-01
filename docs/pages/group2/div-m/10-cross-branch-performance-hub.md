# 10 — Cross-Branch Performance Hub

> **URL:** `/group/analytics/performance/`
> **File:** `10-cross-branch-performance-hub.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Analytics Director (Role 102, G1) · Academic Data Analyst (Role 104, G1) · MIS Officer (Role 103, G1) · Strategic Planning Officer (Role 107, G1)

---

## 1. Purpose

Central intelligence page for comparing all branches simultaneously across multiple performance dimensions. The Analytics Director uses this as the primary tool to identify branch outliers — best performers, worst performers, most improved, and branches showing consistent decline — and to generate cross-branch comparison reports for the Chairman and Board. Performance is measured across seven dimensions: Academic (exam scores), Financial (fee collection), Attendance, Enrollment, Hostel (if applicable), Staff, and Welfare. Users can configure which dimensions to display and drill into any branch for a detailed breakdown.

Scale: 20–50 branches per group. All branches rendered in a single sortable table with colour-coded performance indicators and trend arrows. Data updated daily from branch submissions.

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Analytics Director | 102 | G1 | Full — all data, outlier analysis, export, notes | Primary user |
| Group Academic Data Analyst | 104 | G1 | Full — same as Analytics Director | Shares page equally |
| Group MIS Officer | 103 | G1 | View + Export — no notes or configuration | For report generation |
| Group Strategic Planning Officer | 107 | G1 | View + Export — no notes or configuration | For expansion analysis |
| Group Exam Analytics Officer | 105 | G1 | View only — academic and exam dimensions | Limited to academic data |
| Group Hostel Analytics Officer | 106 | G1 | View only — hostel dimension only | Limited to hostel data |
| All other roles | — | — | No access | Redirected |

> **Access enforcement:** `@require_role(['analytics_director', 'academic_data_analyst', 'mis_officer', 'strategic_planning_officer', 'exam_analytics_officer', 'hostel_analytics_officer'])`. Dimension visibility is further filtered server-side by role (e.g., Role 106 sees only the Hostel column; Roles 102/104 see all columns).

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Analytics & MIS  ›  Cross-Branch Performance Hub
```

### 3.2 Page Header
```
Cross-Branch Performance Hub                    [Configure Columns ⚙]  [Export ↓]  [+ Add Note]
[Group Name]  ·  [N] Branches  ·  Last Updated: [date time]
AY [current academic year]  ·  Showing [N] of [N] dimensions  ·  Data: [current month/period]
```

`[Configure Columns ⚙]` — opens `column-config` drawer (Role 102 and 104 only); saves configuration per user session.
`[Export ↓]` — dropdown: Export to PDF / Export to XLSX. Roles 102, 103, 104, 107.
`[+ Add Note]` — opens `branch-note-add` modal (Roles 102 and 104 only).

### 3.3 Alert Banners (conditional)

| Condition | Banner Text | Severity |
|---|---|---|
| Branches in bottom quartile for 3+ months | "[N] branch(es) have been in the bottom performance quartile for 3 or more months: [list]." | Red |
| Branches with anomalous data (e.g., 100% attendance) | "[N] branch(es) have data that may be inaccurate (e.g. 100% attendance reported). Review data quality." | Amber |
| Cross-branch data older than 7 days | "Performance data has not been refreshed in 7 days. Some metrics may be stale." | Amber |
| No branch data at all | "No branch performance data is available for this academic year." | Blue |

---

## 4. KPI Summary Bar

Six metric cards at the top of the page.

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Total Branches | Count of active branches in the group | `Branch.objects.filter(active=True).count()` | Indigo (neutral) | `#kpi-branches` |
| 2 | Top Quartile Branches | Branches in top 25% by composite score | Top N/4 by `composite_score` | Green always | `#kpi-top-quartile` |
| 3 | Bottom Quartile Branches | Branches in bottom 25% by composite score | Bottom N/4 by `composite_score` | Red if > 0 | `#kpi-bottom-quartile` |
| 4 | Most Improved (YoY) | Branches with highest composite score improvement vs last AY | Top 3 branches by `yoy_score_change` | Green always | `#kpi-most-improved` |
| 5 | Consistent Decline (3m+) | Branches with declining composite score for 3+ consecutive months | `BranchTrend.objects.filter(direction='declining', months__gte=3).count()` | Red if > 0 · Green = 0 | `#kpi-declining` |
| 6 | Data Quality (Avg) | Average data quality score across all branches (%) | `DataQuality.objects.aggregate(Avg('quality_score'))` | Green ≥ 85% · Amber 70–84% · Red < 70% | `#kpi-data-quality` |

**HTMX:** `<div id="perf-kpi-bar" hx-get="/api/v1/group/{id}/analytics/performance/kpi/" hx-trigger="load, every 300s" hx-swap="innerHTML" hx-indicator="#kpi-spinner">`.

---

## 5. Sections

### 5.1 Cross-Branch Comparison Table

> The core of the page. All active branches in one sortable table. Columns are configurable.

**Search bar:** Branch name, city. Debounced 300ms.

**Filter chips:** `[Zone ▾]` `[State ▾]` `[Branch Type ▾]` `[Performance Band ▾]` `[Stream ▾]`

**Fixed columns (always shown):**

| Column | Source Field | Sortable | Notes |
|---|---|---|---|
| # | `rank` | ▲▼ | Rank by composite score (1 = best) |
| Branch | `branch_name` | ▲▼ | Clickable → `branch-performance-detail` drawer |
| Zone | `zone_name` | ▲▼ | "—" if no zone |
| Students | `enrollment_count` | ▲▼ | Total enrolled, current AY |
| Health Score | `composite_score` | ▲▼ | 0–100 badge; colour: 85–100 green · 70–84 blue · 55–69 amber · 40–54 orange · <40 red |
| Trend | `trend_3m` | ▲▼ | ↑ improving · ↓ declining · → stable (3-month direction) |
| Actions | — | — | `[View]` |

**Configurable columns (any combination of these 7 dimensions):**

| Column | Dimension | Default Visible | Notes |
|---|---|---|---|
| Enrollment Rate (%) | Enrollment | ✅ | Actual enrolled / sanctioned capacity |
| Avg Score (%) | Academic | ✅ | Group-wide avg exam score, current AY |
| Attendance Rate (%) | Attendance | ✅ | Monthly avg, current month |
| Fee Collection Rate (%) | Financial | ✅ | Collected / demanded, current AY |
| Hostel Occupancy (%) | Hostel | ❌ (shown only for hostel branches) | Bed fill rate |
| Staff Strength (%) | Staff | ❌ | Filled positions / sanctioned positions |
| Welfare Events Count | Welfare | ❌ | Count this AY, Sev 3+4 highlighted |

**Row colour rules:**
- Top quartile composite score: `bg-green-50`
- Bottom quartile composite score: `bg-red-50`
- 3-month declining trend: left border `border-l-4 border-red-400`
- Data anomaly flagged: `bg-amber-50`

**Default sort:** Health Score ascending (worst first — immediate visibility of problems).
**Pagination:** 25 rows · Controls: `« Previous  Page N of N  Next »` · Rows per page: 25 / 50 / All.

**Column visibility toggle:** `[Columns ▾]` dropdown above table showing checkboxes for all 7 configurable dimensions. State saved to user session (not database — resets on new session). Role 106 cannot unhide the non-hostel dimensions.

### 5.2 Outlier Panel

> Auto-detected performance outliers. Collapsed by default, expandable.

**Panel header:** "Performance Outliers — [Current AY]" with outlier count badge. `[▸ Expand]` / `[▾ Collapse]` toggle.

When expanded, shows 4 sub-panels in a 2×2 grid:

| Sub-panel | Content |
|---|---|
| 🏆 Top 3 Performers | Branches with highest composite score; cards with score, key metric |
| ⚠️ Bottom 3 Performers | Branches with lowest composite score; cards with score, intervention flag |
| 📈 Most Improved | Branches with highest YoY composite score improvement; cards with delta |
| 📉 Consistent Decline | Branches declining for 3+ months; cards with months count, last score |

Each card has a `[View Details]` link that opens `branch-performance-detail` drawer.

### 5.3 Dimension Comparison (Side-by-Side)

> Compare any 2 selected branches across all dimensions. Optional section.

`[▸ Show Branch Comparison]` expands this section.

**Branch selectors:** Two dropdowns — "Select Branch A" and "Select Branch B" (all active branches). On selection, loads side-by-side comparison of all 7 dimensions via HTMX.

| Dimension | Branch A | Branch B | Better |
|---|---|---|---|
| Composite Score | [N] | [N] | ← or → arrow |
| Enrollment Rate | [N]% | [N]% | — |
| Avg Score | [N]% | [N]% | — |
| Attendance Rate | [N]% | [N]% | — |
| Fee Collection Rate | [N]% | [N]% | — |
| Staff Strength | [N]% | [N]% | — |
| Welfare Events | [N] | [N] | — |

---

## 6. Drawers & Modals

### 6.1 `branch-performance-detail` Drawer — 680px, right-slide

**Trigger:** Clicking branch name in §5.1 or `[View]` action or `[View Details]` in outlier panel.

**Header:**
```
[Branch Name]                                              [×]
[Zone]  ·  [City], [State]  ·  [Branch Type]
Health Score: [N] [colour badge]  ·  Rank: [N] of [N]  ·  Trend: [↑↓→]
```

**Tab 1 — Overview**

Two-column card layout showing all 7 performance dimensions. Each card:
- Dimension name (icon + label)
- Current value (large number, colour coded)
- vs Group Average (±delta, colour coded)
- Trend arrow (last 3 months)

**Tab 2 — Academic**

- Avg exam score trend line (last 5 exams)
- Subject-wise avg score horizontal bar chart
- Rank position in group (current AY)
- Topper count from this branch

**Tab 3 — Financial**

- Fee collection rate (current AY)
- Month-by-month collection bar chart (last 6 months)
- Outstanding amount (₹)
- Defaulter count (read-only)

**Tab 4 — Operations**

- Attendance rate this month + trend line (last 12 months)
- Staff strength % (filled/sanctioned)
- Welfare events this AY by severity
- Hostel occupancy (if hostel branch)

**Tab 5 — History**

YoY comparison table — last 3 AYs × all 7 dimensions. Shows absolute values + YoY change %.

**Footer actions (Roles 102 and 104 only):**
`[Add Internal Note]` button at drawer footer — opens inline note field within the drawer; saves note attached to branch record for current AY. Notes visible only to Division M team.

### 6.2 `column-config` Drawer — 400px, right-slide

**Trigger:** `[Configure Columns ⚙]` header button. Roles 102 and 104 only.

**Header:** "Configure Visible Columns"

Checkboxes for the 7 configurable dimensions:
- [✅] Enrollment Rate
- [✅] Avg Score
- [✅] Attendance Rate
- [✅] Fee Collection Rate
- [❌] Hostel Occupancy (auto-checked and locked for hostel branches)
- [❌] Staff Strength
- [❌] Welfare Events

Note: "Selections are saved for your current session."

**Footer:** `[Reset to Default]`  `[Apply]`

On Apply: HTMX `hx-post` updates table column visibility; drawer closes.

### 6.3 `branch-note-add` Modal — 420px, centred

**Trigger:** `[+ Add Note]` header button or `[Add Internal Note]` in drawer footer. Roles 102 and 104 only.

| Field | Type | Required | Notes |
|---|---|---|---|
| Branch | Select | Yes | All active branches |
| Note | Textarea | Yes | Min 20, max 1000 chars |
| Dimension Flagged | Select | No | Academic / Financial / Attendance / Hostel / Staff / Welfare / General |
| Flag for Follow-up | Toggle | No | Default off; adds to follow-up list |

**Footer:** `[Cancel]`  `[Save Note]`

---

## 7. Charts

### 7.1 Branch Performance Radar Chart — Radar/Spider Chart

| Property | Value |
|---|---|
| Chart type | Radar (Chart.js 4.x) |
| Title | "Branch Performance Profile — [Selected Branch]" |
| Data | Single branch across 6 dimensions (Academic, Financial, Attendance, Enrollment, Staff, Welfare — all normalised 0–100); group average shown as a second line |
| Axes | One axis per dimension |
| Line colours | Branch: indigo-500 (filled area opacity 0.2) · Group Avg: grey-400 (no fill) |
| Tooltip | "[Dimension]: Branch [N] · Group Avg [N]" |
| Branch selector | Dropdown above chart; on change: chart reloads via HTMX |
| Default | First branch in current sort order |
| Empty state | "Select a branch to view its performance profile." |
| Export | PNG export button |
| API endpoint | `GET /api/v1/group/{id}/analytics/performance/radar/{branch_id}/` |
| HTMX | `<div id="chart-radar" hx-get="..." hx-trigger="load" hx-swap="innerHTML">` |

### 7.2 Group Composite Score Trend — Multi-Line Chart

| Property | Value |
|---|---|
| Chart type | Multi-line (Chart.js 4.x) |
| Title | "Composite Score Trend — Last 6 Months" |
| Data | Monthly composite score for: Group Average + Top Branch + Bottom Branch (3 lines) |
| X-axis | Month name (last 6 months) |
| Y-axis | Composite score (0–100) |
| Line colours | Group Avg: indigo · Top Branch: green · Bottom Branch: red |
| Tooltip | "[Month] · Group Avg: [N] · Top: [Branch, N] · Bottom: [Branch, N]" |
| Legend | Bottom; group avg, top, bottom |
| Empty state | "Insufficient trend data available." |
| Export | PNG export button |
| API endpoint | `GET /api/v1/group/{id}/analytics/performance/trend/?months=6` |
| HTMX | `<div id="chart-trend" hx-get="..." hx-trigger="load" hx-swap="innerHTML">` |

---

## 8. Toast Messages

| Action | Toast Text | Type |
|---|---|---|
| Column config applied | "Column configuration updated." | Info |
| Column config reset | "Columns reset to default view." | Info |
| Branch note saved | "Note saved for [Branch Name]." | Success |
| Branch note error | "Could not save note. Please try again." | Error |
| Export generated | "Performance report exported to [format]. Download starting." | Success |
| Export failed | "Could not generate export. Please try again." | Error |
| Branch detail drawer load error | "Could not load branch details. Please try again." | Error |
| Radar chart branch load error | "Could not load performance data for this branch." | Error |
| KPI refresh error | "Failed to refresh KPI data." | Error |
| Comparison — select both branches | "Please select two branches to compare." | Error |

---

## 9. Empty States

| Context | Icon | Heading | Sub-text | Action |
|---|---|---|---|---|
| No branches configured | `building-office` | "No Branches" | "No active branches are configured for this group." | — |
| No performance data for current AY | `chart-bar` | "No Performance Data" | "Branch performance data has not been loaded for this academic year." | — |
| No results matching filters | `funnel` | "No Branches Match Filters" | "Try adjusting or clearing your filters." | `[Clear Filters]` |
| Outlier panel — no declining branches | `check-circle` | "No Consistent Declines" | "No branches have been declining for 3+ consecutive months." | — |
| Branch comparison — no branches selected | `arrows-right-left` | "Select Branches to Compare" | "Choose two branches from the dropdowns above to see a side-by-side comparison." | — |
| Radar chart — no branch selected | `chart-pie` | "Select a Branch" | "Choose a branch from the dropdown to view its performance radar." | — |
| Branch detail — no notes | `pencil` | "No Internal Notes" | "No internal notes have been added for this branch." | `[Add Internal Note]` (Roles 102/104) |
| Charts — no trend data | `chart-bar` | "No Trend Data" | "Insufficient historical data to show a trend." | — |

---

## 10. Loader States

| Context | Loader Behaviour |
|---|---|
| Initial page load | KPI bar: 6 shimmer cards. Charts: 2 shimmer rectangles. Main table: 8 shimmer rows. Outlier panel: shimmer header only (collapsed). |
| Search/filter change | Table rows replaced by shimmer rows + spinner below toolbar |
| Column config applied | Table body shimmer for 1s while re-rendering columns |
| Branch detail drawer open | Drawer slides in; shimmer tab bar + shimmer cards |
| Tab switch in drawer | Tab content shimmer while fetching |
| Radar chart — branch change | Chart area shimmer + spinner until data loads |
| Branch comparison — branch selection | Comparison table shimmer while loading |
| `[Save Note]` modal submit | Button disabled + spinner |
| Export — `[Export ↓]` click | "Preparing…" spinner on button; file triggers download |
| KPI auto-refresh | Cards pulse; values update in place |
| Pagination click | Table body replaced by shimmer rows |

---

## 11. Role-Based UI Visibility

| UI Element | Role 102 (Analytics Dir) | Role 104 (Academic Analyst) | Role 103 (MIS Officer) | Role 107 (Strategic) | Role 105 (Exam) | Role 106 (Hostel) |
|---|---|---|---|---|---|---|
| Page | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| KPI Bar | Full | Full | Full | Full | Full | Full |
| Main table — all 7 dimensions | ✅ All | ✅ All | ✅ All | ✅ All | Academic + Enrollment only | Hostel only |
| Column config drawer | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| `[Export ↓]` button | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| `[+ Add Note]` button | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Outlier panel | ✅ Full | ✅ Full | ✅ View | ✅ View | ✅ View | Hostel outliers only |
| Branch comparison section | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `branch-performance-detail` drawer | ✅ All tabs | ✅ All tabs | ✅ Read-only | ✅ Read-only | Academic tabs only | Hostel tabs only |
| `[Add Internal Note]` in drawer | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Alert banners | ✅ All | ✅ All | ✅ All | ✅ All | ✅ Relevant | ✅ Relevant |

---

## 12. API Endpoints

### 12.1 KPI Summary
```
GET /api/v1/group/{group_id}/analytics/performance/kpi/
```
Query: `academic_year` (optional).
Response: `{ "total_branches": N, "top_quartile": N, "bottom_quartile": N, "most_improved": N, "consistent_decline": N, "avg_data_quality": N }`.

### 12.2 Cross-Branch Comparison Table
```
GET /api/v1/group/{group_id}/analytics/performance/branches/
```

| Query Parameter | Type | Description |
|---|---|---|
| `academic_year` | string | Default current AY |
| `zone` | string | Filter by zone ID |
| `state` | string | Filter by state |
| `branch_type` | string | `day` · `hostel` · `both` |
| `performance_band` | string | `top` · `above_avg` · `below_avg` · `bottom` |
| `stream` | string | `mpc` · `bipc` · `mec` · `all` |
| `search` | string | Branch name, city |
| `dimensions` | string | Comma-separated: `academic,financial,attendance,enrollment,hostel,staff,welfare` |
| `page` | integer | Default 1 |
| `page_size` | integer | 25 · 50 · All |
| `ordering` | string | `composite_score` (ASC default) · `branch_name` · `enrollment_count` · `trend_3m` |

Response: `{ count, next, previous, group_avg: {...}, results: [...] }`.

Server enforces dimension visibility based on role — Role 106 only receives hostel columns regardless of `dimensions` param.

### 12.3 Branch Performance Detail
```
GET /api/v1/group/{group_id}/analytics/performance/branches/{branch_id}/
```
Response: Full detail object — all 7 dimensions + tab data (academic trend, financial trend, operations, history).

### 12.4 Radar Chart Data
```
GET /api/v1/group/{group_id}/analytics/performance/radar/{branch_id}/
```
Response: `{ labels: [dim1, ...], branch_data: [...], group_avg_data: [...] }`.

### 12.5 Composite Score Trend
```
GET /api/v1/group/{group_id}/analytics/performance/trend/
```
Query: `months` (default 6).
Response: `{ labels: [...months], group_avg: [...], top_branch: { name, data: [...] }, bottom_branch: { name, data: [...] } }`.

### 12.6 Outlier Data
```
GET /api/v1/group/{group_id}/analytics/performance/outliers/
```
Response: `{ top_performers: [...3], bottom_performers: [...3], most_improved: [...3], consistent_decline: [...] }`.

### 12.7 Branch Side-by-Side Comparison
```
GET /api/v1/group/{group_id}/analytics/performance/compare/
```
Query: `branch_a` (ID), `branch_b` (ID).
Response: `{ branch_a: { name, dimensions: {...} }, branch_b: { name, dimensions: {...} } }`.

### 12.8 Add Branch Note
```
POST /api/v1/group/{group_id}/analytics/performance/branches/{branch_id}/notes/
```
Body: `{ "note": "string", "dimension_flagged": "...", "flag_for_followup": true }`. Roles 102, 104 only.
Response: 201 Created.

### 12.9 Export
```
GET /api/v1/group/{group_id}/analytics/performance/export/
```
Query: `format` (pdf/xlsx), `academic_year`, `dimensions` (comma-separated), all filter params from §12.2.
Response: File download.

---

## 13. HTMX Patterns

| Pattern | Trigger Element | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI bar load + auto-refresh | `<div id="perf-kpi-bar">` | GET `.../performance/kpi/` | `#perf-kpi-bar` | `innerHTML` | `hx-trigger="load, every 300s"` |
| Chart 7.1 load | `<div id="chart-radar">` | GET `.../performance/radar/{default_branch_id}/` | `#chart-radar` | `innerHTML` | `hx-trigger="load"` |
| Chart 7.2 load | `<div id="chart-trend">` | GET `.../performance/trend/` | `#chart-trend` | `innerHTML` | `hx-trigger="load"` |
| Radar chart — branch change | `<select id="radar-branch-select">` | GET `.../performance/radar/{branch_id}/` | `#chart-radar` | `innerHTML` | `hx-trigger="change"` |
| Main table — search | `<input id="perf-search">` | GET `.../performance/branches/?search=` | `#performance-table` | `innerHTML` | `hx-trigger="keyup changed delay:300ms"` |
| Main table — filter chips | Filter chip selects | GET `.../performance/branches/?filters=` | `#performance-table` | `innerHTML` | `hx-trigger="change"` |
| Main table — pagination | Pagination buttons | GET `.../performance/branches/?page={n}` | `#performance-table` | `innerHTML` | `hx-trigger="click"` |
| Main table — column config apply | `[Apply]` in config drawer | POST `/htmx/analytics/performance/column-config/` | `#performance-table` | `outerHTML` | `hx-on::after-request="closeDrawer();"` |
| Open branch detail drawer | Branch name / `[View]` | GET `/htmx/analytics/performance/branches/{id}/detail/` | `#drawer-container` | `innerHTML` | `hx-trigger="click"` |
| Branch drawer tab switch | Tab buttons | GET `/htmx/analytics/performance/branches/{id}/tab/{slug}/` | `#branch-drawer-tab-content` | `innerHTML` | `hx-trigger="click"` |
| Branch comparison — select A | `<select id="compare-branch-a">` | GET `.../performance/compare/?branch_a={id}&branch_b={b_id}` | `#comparison-section` | `innerHTML` | `hx-trigger="change"` (fires only when both selected) |
| Branch comparison — select B | `<select id="compare-branch-b">` | GET `.../performance/compare/?branch_a={a_id}&branch_b={id}` | `#comparison-section` | `innerHTML` | `hx-trigger="change"` |
| Open note modal | `[+ Add Note]` / `[Add Internal Note]` | GET `/htmx/analytics/performance/note-modal/` | `#modal-container` | `innerHTML` | `hx-trigger="click"` |
| Save branch note | Note form in modal | POST `.../branches/{id}/notes/` | `#modal-container` | `innerHTML` | `hx-on::after-request="closeModal(); showToast(event);"` |
| Outlier panel expand | `[▸ Expand]` toggle | GET `/htmx/analytics/performance/outliers/` | `#outlier-panel-content` | `innerHTML` | `hx-trigger="click"` (lazy load on expand) |

---

*Page spec version: 1.0 · Last updated: 2026-03-22*
