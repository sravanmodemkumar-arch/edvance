# 11 — Branch Health Scorecard

> **URL:** `/group/analytics/scorecard/`
> **File:** `11-branch-health-scorecard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Analytics Director (Role 102, G1) · Strategic Planning Officer (Role 107, G1) · MIS Officer (Role 103, G1)

---

## 1. Purpose

Composite health scoring system that assigns every branch a single Health Index Score (0–100), calculated from seven weighted sub-scores across: Academic (25%), Financial (20%), Attendance (15%), Staff (15%), Welfare (10%), Data Quality (10%), and Compliance (5%). The scorecard provides a standardised, objective way to rank and compare branches — removing the difficulty of comparing raw metrics like "Branch A has 85% fee collection but 70% attendance" versus "Branch B has 72% fee collection and 91% attendance". The Analytics Director can adjust dimension weights; the Strategic Planning Officer uses the scorecard to inform expansion and intervention decisions.

Score thresholds: 85–100 = Excellent (green), 70–84 = Good (blue), 55–69 = Needs Attention (amber), 40–54 = At Risk (orange), 0–39 = Critical (red).

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Analytics Director | 102 | G1 | Full — view, configure weights, add notes, export | Primary owner |
| Group Strategic Planning Officer | 107 | G1 | Full — view, export, add strategic notes | Co-primary user |
| Group MIS Officer | 103 | G1 | View + Export — no weight configuration | For board reports |
| Group Academic Data Analyst | 104 | G1 | View only | Academic dimension reference |
| Group Hostel Analytics Officer | 106 | G1 | View only — Hostel dimension visible | Limited view |
| All other roles | — | — | No access | Redirected |

> **Access enforcement:** `@require_role(['analytics_director', 'strategic_planning_officer', 'mis_officer', 'academic_data_analyst', 'hostel_analytics_officer'])`. Weight configuration endpoint: `@require_role('analytics_director')` only.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Analytics & MIS  ›  Branch Health Scorecard
```

### 3.2 Page Header
```
Branch Health Scorecard                         [Configure Weights ⚙]  [Export ↓]
[Group Name]  ·  [N] Branches Scored  ·  Group Average Score: [N]/100
AY [current academic year]  ·  Score weights last updated: [date]  ·  Data as of: [date]
```

`[Configure Weights ⚙]` — opens `score-weights-config` drawer. Role 102 only.
`[Export ↓]` — dropdown: Export to PDF / Export to XLSX. Roles 102, 103, 107.

### 3.3 Alert Banners (conditional)

| Condition | Banner Text | Severity |
|---|---|---|
| Branches with score < 40 (Critical) | "[N] branch(es) have a Critical health score (below 40): [list]. Immediate review required." | Red |
| Score weights not configured (all equal default) | "Health score weights are at default values. Configure weights to reflect your group's priorities." | Amber |
| Score weights don't total 100% | "Score weight configuration error — weights do not total 100%. Scores may be inaccurate." | Red |
| Branches with score declining for 3+ months | "[N] branch(es) have had a declining health score for 3 or more consecutive months." | Amber |
| Data quality affecting scores | "[N] branch(es) have low data quality scores which may be dragging their health scores down." | Blue |

---

## 4. KPI Summary Bar

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Group Average Score | Average health score across all branches | `BranchScore.objects.filter(ay=current_ay).aggregate(Avg('composite_score'))` | Green ≥ 75 · Amber 60–74 · Red < 60 | `#kpi-group-avg` |
| 2 | Excellent (85–100) | Count of branches in Excellent band | — | Green always | `#kpi-excellent` |
| 3 | Needs Attention (55–69) | Count in Needs Attention band | — | Amber always | `#kpi-attention` |
| 4 | At Risk / Critical (< 55) | Count in At Risk + Critical bands | — | Red if > 0 · Green = 0 | `#kpi-at-risk` |
| 5 | Most Improved (vs last month) | Branch with largest score improvement month-over-month | Top branch by `score_delta_mom` | Green always | `#kpi-most-improved` |
| 6 | Biggest Decline (vs last month) | Branch with largest score drop month-over-month | Bottom branch by `score_delta_mom` | Red if decline > 5 pts | `#kpi-biggest-decline` |

**HTMX:** `<div id="scorecard-kpi-bar" hx-get="/api/v1/group/{id}/analytics/scorecard/kpi/" hx-trigger="load, every 300s" hx-swap="innerHTML">`.

---

## 5. Sections

### 5.1 Branch Health Scorecard Table

**Search bar:** Branch name, city. Debounced 300ms.

**Filter chips:** `[Score Band ▾]` `[Zone ▾]` `[State ▾]` `[Branch Type ▾]` `[Trend ▾]`

| Column | Source Field | Sortable | Notes |
|---|---|---|---|
| Rank | `score_rank` | ▲▼ | 1 = highest score in group |
| Branch | `branch_name` | ▲▼ | Clickable → `branch-scorecard-detail` drawer |
| Zone | `zone_name` | ▲▼ | "—" if no zone |
| Health Score | `composite_score` | ▲▼ | Large colour badge (see score thresholds in §1) |
| Band | `score_band` | ▲▼ | Excellent / Good / Needs Attention / At Risk / Critical |
| Academic (25%) | `academic_score` | ▲▼ | Sub-score 0–100 · Colour coded independently |
| Financial (20%) | `financial_score` | ▲▼ | Sub-score 0–100 |
| Attendance (15%) | `attendance_score` | ▲▼ | Sub-score 0–100 |
| Staff (15%) | `staff_score` | ▲▼ | Sub-score 0–100 |
| Welfare (10%) | `welfare_score` | ▲▼ | Sub-score 0–100 |
| Data Quality (10%) | `data_quality_score` | ▲▼ | Sub-score 0–100 |
| Compliance (5%) | `compliance_score` | ▲▼ | Sub-score 0–100 |
| vs Last Month | `score_delta_mom` | ▲▼ | "+3.2" green · "-2.1" red · "—" no change |
| Trend (3m) | `trend_3m` | ▲▼ | ↑ / ↓ / → |
| Actions | — | — | `[View]` · `[Add Note]` (Roles 102 and 107) |

**Row colour:**
- Score 85–100: `bg-green-50`
- Score 40–54: `bg-orange-50`
- Score < 40: `bg-red-50`

**Default sort:** Health Score ascending (worst first).
**Pagination:** 25 rows · `« Previous  Page N of N  Next »`.

### 5.2 Score Band Distribution Summary

Visual summary bar showing how many branches fall in each score band:

```
Score Distribution (current AY):
Excellent ████████ 8
Good      ███████████████ 15
Needs Att ██████ 6
At Risk   ███ 3
Critical  ██ 2
          0    5    10    15    20
```

Rendered as a horizontal stacked bar chart (Chart.js). Click on any band → applies filter to §5.1 table.

### 5.3 Benchmark Comparison Panel

Displays three benchmark reference lines:
- **Group Average:** [N] points
- **Top Performer:** [Branch Name] — [N] points
- **Bottom Performer:** [Branch Name] — [N] points
- **National Benchmark:** [N] points (configurable static value — set by Analytics Director in Configure Weights; shown as dotted reference line on score chart)

---

## 6. Drawers & Modals

### 6.1 `branch-scorecard-detail` Drawer — 680px, right-slide

**Trigger:** Clicking branch name or `[View]` in §5.1.

**Header:**
```
[Branch Name] — Health Scorecard                            [×]
[Zone]  ·  [City], [State]
Health Score: [N]/100  [colour badge]  ·  Rank [N] of [N]  ·  Band: [band label]
```

**Tab 1 — Score Breakdown**

Visual breakdown of each sub-score as a horizontal progress bar with label, score, and weight.

```
Academic      ████████████████████░░░░░░░░  78/100  × 25% = 19.5 pts
Financial     ████████████████████████░░░░  91/100  × 20% = 18.2 pts
Attendance    ██████████████████░░░░░░░░░░  72/100  × 15% = 10.8 pts
Staff         ████████████████████████████  95/100  × 15% = 14.25 pts
Welfare       ████████████████████████████  98/100  × 10% = 9.8 pts
Data Quality  █████████████████░░░░░░░░░░░  68/100  × 10% = 6.8 pts
Compliance    ████████████████████████████  100/100 × 5%  = 5.0 pts
─────────────────────────────────────────
Composite Score:                            84.35 / 100
```

**Tab 2 — Trend**

Line chart — composite health score per month over last 12 months.
Below chart: table of monthly scores.

**Tab 3 — Component Analysis**

For each sub-score, shows the raw metric(s) that produced it:

| Sub-score | Raw Metric | Raw Value | Benchmark | Score Contribution |
|---|---|---|---|---|
| Academic | Avg exam score | 73% | Group avg 68% | +5% → score boost |
| Financial | Fee collection rate | 91% | Target 90% | On target |
| Attendance | Attendance rate | 81% | Target 90% | Below target |
| etc. | — | — | — | — |

**Tab 4 — Action Notes**

Internal notes added by Analytics Director / Strategic Planning Officer for this branch.
Notes list (newest first): Date · Author · Note text.
`[+ Add Note]` inline form at bottom (Roles 102, 107 only).

Note form fields: Text area (min 20 chars), Flag for Follow-up toggle.

### 6.2 `score-weights-config` Drawer — 480px, right-slide

**Trigger:** `[Configure Weights ⚙]` header button. Role 102 only.

**Header:**
```
Configure Health Score Weights
Weights must total exactly 100%.
```

| Field | Type | Required | Validation |
|---|---|---|---|
| Academic Weight (%) | Number input | Yes | 0–100, integer |
| Financial Weight (%) | Number input | Yes | 0–100, integer |
| Attendance Weight (%) | Number input | Yes | 0–100, integer |
| Staff Weight (%) | Number input | Yes | 0–100, integer |
| Welfare Weight (%) | Number input | Yes | 0–100, integer |
| Data Quality Weight (%) | Number input | Yes | 0–100, integer |
| Compliance Weight (%) | Number input | Yes | 0–100, integer |
| National Benchmark Score | Number input | No | 0–100; used as reference line on charts |

**Live total indicator:** Inline sum updates as weights are changed. Red if ≠ 100, green if = 100. Save is disabled until total = 100.

**Warning:** "Changing weights will recalculate all branch scores immediately."

**Footer:** `[Reset to Default (25/20/15/15/10/10/5)]`  `[Save Weights]`

On save: all `BranchScore` records for current AY are recalculated asynchronously; toast shown when complete.

### 6.3 `branch-note-add` Modal — 420px, centred

**Trigger:** `[Add Note]` in table row or `[+ Add Note]` inside scorecard detail drawer. Roles 102 and 107.

| Field | Type | Required | Notes |
|---|---|---|---|
| Branch | Read-only | — | Pre-filled |
| Note | Textarea | Yes | Min 20, max 1000 chars |
| Dimension | Select | No | Academic / Financial / Attendance / Staff / Welfare / Data Quality / Compliance / General |
| Flag for Follow-up | Toggle | No | Default off |

**Footer:** `[Cancel]`  `[Save Note]`

---

## 7. Charts

### 7.1 Score Distribution Histogram

| Property | Value |
|---|---|
| Chart type | Horizontal stacked bar (Chart.js 4.x) |
| Title | "Branch Health Score Distribution — [Current AY]" |
| Data | Count of branches in each score band: Excellent / Good / Needs Attention / At Risk / Critical |
| Y-axis | Band labels |
| X-axis | Count of branches |
| Bar colours | Excellent: green · Good: blue · Needs Attention: amber · At Risk: orange · Critical: red |
| Tooltip | "[Band]: [N] branches ([N]%)" |
| Interactive | Click on band → filters table to that band |
| Empty state | "Score distribution data not available." |
| Export | PNG export button |
| API endpoint | `GET /api/v1/group/{id}/analytics/scorecard/distribution/` |
| HTMX | `<div id="chart-distribution" hx-get="..." hx-trigger="load" hx-swap="innerHTML">` |

### 7.2 Sub-Score Dimension Radar — Group Average

| Property | Value |
|---|---|
| Chart type | Radar (Chart.js 4.x) |
| Title | "Group Average Sub-Scores — [Current AY]" |
| Data | Group average of each sub-score (7 dimensions) as a radar |
| Axes | Academic · Financial · Attendance · Staff · Welfare · Data Quality · Compliance |
| Line colour | Indigo-500 with 0.2 opacity fill |
| Tooltip | "[Dimension]: [N] average" |
| Reference line | 70 (target band boundary) |
| Empty state | "Sub-score data not available." |
| Export | PNG export button |
| API endpoint | `GET /api/v1/group/{id}/analytics/scorecard/group-radar/` |
| HTMX | `<div id="chart-group-radar" hx-get="..." hx-trigger="load" hx-swap="innerHTML">` |

---

## 8. Toast Messages

| Action | Toast Text | Type |
|---|---|---|
| Note saved | "Note saved for [Branch]." | Success |
| Note error | "Could not save note. Please try again." | Error |
| Weights saved | "Score weights updated. Branch scores are being recalculated." | Success |
| Weights recalculation complete | "Health scores have been recalculated with the new weights." | Success |
| Weights error — total ≠ 100% | "Weights must total exactly 100%. Current total: [N]%." | Error |
| Weights save error | "Could not save weights. Please try again." | Error |
| Export generated | "Scorecard exported to [format]. Download starting." | Success |
| Export failed | "Could not generate export. Please try again." | Error |
| Drawer load error | "Could not load scorecard details for this branch." | Error |
| KPI refresh error | "Failed to refresh KPI data." | Error |

---

## 9. Empty States

| Context | Icon | Heading | Sub-text | Action |
|---|---|---|---|---|
| No branches scored | `chart-bar` | "No Scores Available" | "Branch health scores have not been calculated for this academic year." | — |
| No results after filter | `funnel` | "No Branches Match Filters" | "Try adjusting or clearing your filters." | `[Clear Filters]` |
| Scorecard detail — trend tab — no data | `chart-bar` | "No Trend Data" | "Insufficient historical score data to show a trend." | — |
| Scorecard detail — action notes — no notes | `pencil` | "No Notes" | "No internal notes have been added for this branch." | `[+ Add Note]` (Roles 102/107) |
| Score weights not configured | `cog` | "Default Weights Active" | "Health scores are using default weights. Configure weights to match your group's priorities." | `[Configure Weights]` (Role 102) |
| Charts — no data | `chart-bar` | "No data available" | "Health score data is not available." | — |

---

## 10. Loader States

| Context | Loader Behaviour |
|---|---|
| Initial page load | KPI bar: 6 shimmer cards. Charts: 2 shimmer rectangles. Table: 8 shimmer rows. Benchmark panel: 3 shimmer lines. |
| Filter/search change | Table rows replaced by shimmer rows |
| `branch-scorecard-detail` drawer open | Drawer slides in; shimmer tabs + progress bars skeleton |
| Tab switch in drawer | Shimmer content in tab area |
| Score weights recalculation | Toast shown while processing; table shimmers and reloads on complete |
| `[Save Weights]` submit | Button disabled + "Saving…" + spinner |
| `[Save Note]` modal submit | Button disabled + spinner |
| Chart initial load | Shimmer rectangle with centred spinner per chart |
| Chart distribution — band filter click | Table rows shimmer while filtered data loads |
| KPI auto-refresh | Cards pulse; values update in place |
| Pagination click | Table body replaced by shimmer rows |

---

## 11. Role-Based UI Visibility

| UI Element | Role 102 (Analytics Dir) | Role 107 (Strategic) | Role 103 (MIS Officer) | Role 104 (Academic) | Role 106 (Hostel) |
|---|---|---|---|---|---|
| Page | ✅ | ✅ | ✅ | ✅ | ✅ |
| KPI Bar | Full | Full | Full | Full | Full |
| Scorecard table — all 7 sub-scores | ✅ | ✅ | ✅ | ✅ | Hostel sub-score only |
| `[Configure Weights ⚙]` button | ✅ | ❌ | ❌ | ❌ | ❌ |
| `[Export ↓]` button | ✅ | ✅ | ✅ | ❌ | ❌ |
| `[Add Note]` in table row | ✅ | ✅ | ❌ | ❌ | ❌ |
| `branch-scorecard-detail` drawer — Tab 1–3 | ✅ All | ✅ All | ✅ Read-only | ✅ Academic only | Hostel dimension only |
| `branch-scorecard-detail` drawer — Tab 4 Notes | ✅ Full | ✅ Full | ✅ View only | ❌ | ❌ |
| `[+ Add Note]` in drawer | ✅ | ✅ | ❌ | ❌ | ❌ |
| `score-weights-config` drawer | ✅ Full | ❌ | ❌ | ❌ | ❌ |
| Charts — distribution and radar | ✅ | ✅ | ✅ | ✅ | ✅ |
| Alert banners | ✅ All | ✅ All | ✅ All | ✅ Relevant | ✅ Relevant |

---

## 12. API Endpoints

### 12.1 KPI Summary
```
GET /api/v1/group/{group_id}/analytics/scorecard/kpi/
```
Query: `academic_year`.
Response: `{ "group_avg": N, "excellent_count": N, "attention_count": N, "at_risk_count": N, "most_improved": { branch, delta }, "biggest_decline": { branch, delta } }`.

### 12.2 Scorecard Table
```
GET /api/v1/group/{group_id}/analytics/scorecard/branches/
```

| Query Parameter | Type | Description |
|---|---|---|
| `academic_year` | string | Default current |
| `score_band` | string | `excellent` · `good` · `needs_attention` · `at_risk` · `critical` |
| `zone` | string | Zone ID |
| `state` | string | State name |
| `branch_type` | string | `day` · `hostel` · `both` |
| `trend` | string | `improving` · `declining` · `stable` |
| `search` | string | Branch name, city |
| `page` | integer | Default 1 |
| `page_size` | integer | 25 · 50 · All |
| `ordering` | string | `composite_score` (ASC default) · `branch_name` · `score_rank` · `score_delta_mom` |

Response: `{ count, next, previous, group_avg: N, results: [...] }`.

### 12.3 Branch Scorecard Detail
```
GET /api/v1/group/{group_id}/analytics/scorecard/branches/{branch_id}/
```
Response: Full detail — sub-scores, raw metric values, benchmarks, trend data (12 months), notes.

### 12.4 Score Distribution Chart Data
```
GET /api/v1/group/{group_id}/analytics/scorecard/distribution/
```
Response: `{ "excellent": N, "good": N, "needs_attention": N, "at_risk": N, "critical": N }`.

### 12.5 Group Radar Chart Data
```
GET /api/v1/group/{group_id}/analytics/scorecard/group-radar/
```
Response: `{ "labels": [dim1,...], "data": [avg1,...], "target": 70 }`.

### 12.6 Get / Update Score Weights
```
GET  /api/v1/group/{group_id}/analytics/scorecard/weights/
PUT  /api/v1/group/{group_id}/analytics/scorecard/weights/
```
GET: Returns current weights + national benchmark.
PUT: Role 102 only. Body: `{ academic: N, financial: N, attendance: N, staff: N, welfare: N, data_quality: N, compliance: N, national_benchmark: N }`. Validates total = 100. Triggers async recalculation.
Response 200 OK.

### 12.7 Add Branch Note
```
POST /api/v1/group/{group_id}/analytics/scorecard/branches/{branch_id}/notes/
```
Body: `{ "note": "string", "dimension": "...", "flag_for_followup": true }`. Roles 102, 107 only.
Response: 201 Created.

### 12.8 Export
```
GET /api/v1/group/{group_id}/analytics/scorecard/export/
```
Query: `format` (pdf/xlsx), `academic_year`, all filter params from §12.2.
Response: File download.

---

## 13. HTMX Patterns

| Pattern | Trigger Element | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI bar load + auto-refresh | `<div id="scorecard-kpi-bar">` | GET `.../scorecard/kpi/` | `#scorecard-kpi-bar` | `innerHTML` | `hx-trigger="load, every 300s"` |
| Chart 7.1 load | `<div id="chart-distribution">` | GET `.../scorecard/distribution/` | `#chart-distribution` | `innerHTML` | `hx-trigger="load"` |
| Chart 7.2 load | `<div id="chart-group-radar">` | GET `.../scorecard/group-radar/` | `#chart-group-radar` | `innerHTML` | `hx-trigger="load"` |
| Distribution chart — band click | Band bar in chart | GET `.../scorecard/branches/?score_band={band}` | `#scorecard-table` | `innerHTML` | `hx-trigger="click"` via JS `chartClick` handler |
| Table — search | `<input id="scorecard-search">` | GET `.../scorecard/branches/?search=` | `#scorecard-table` | `innerHTML` | `hx-trigger="keyup changed delay:300ms"` |
| Table — filter chips | Filter chip selects | GET `.../scorecard/branches/?filters=` | `#scorecard-table` | `innerHTML` | `hx-trigger="change"` |
| Table — pagination | Pagination buttons | GET `.../scorecard/branches/?page={n}` | `#scorecard-table` | `innerHTML` | `hx-trigger="click"` |
| Open branch detail drawer | Branch name / `[View]` | GET `/htmx/analytics/scorecard/branches/{id}/detail/` | `#drawer-container` | `innerHTML` | `hx-trigger="click"` |
| Branch drawer tab switch | Tab buttons | GET `/htmx/analytics/scorecard/branches/{id}/tab/{slug}/` | `#scorecard-drawer-tab-content` | `innerHTML` | `hx-trigger="click"` |
| Open weights config drawer | `[Configure Weights ⚙]` | GET `/htmx/analytics/scorecard/weights-config/` | `#drawer-container` | `innerHTML` | `hx-trigger="click"` |
| Save weights | Weights form | PUT `.../scorecard/weights/` | `#scorecard-table` | `innerHTML` | `hx-encoding="application/json"`; `hx-on::after-request="closeDrawer(); showToast(event);"` |
| Open note modal (table) | `[Add Note]` button in row | GET `/htmx/analytics/scorecard/note-modal/?branch={id}` | `#modal-container` | `innerHTML` | `hx-trigger="click"` |
| Open note form (drawer) | `[+ Add Note]` button | GET `/htmx/analytics/scorecard/note-form/?branch={id}` | `#drawer-note-area` | `innerHTML` | `hx-trigger="click"` |
| Save note (both paths) | Note form | POST `.../scorecard/branches/{id}/notes/` | `#notes-list-{id}` | `innerHTML` | `hx-on::after-request="showToast(event);"` |

---

*Page spec version: 1.0 · Last updated: 2026-03-22*
