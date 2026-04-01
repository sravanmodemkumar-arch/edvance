# 13 — Rank Trend Analyser

> **URL:** `/group/analytics/rank-trends/`
> **File:** `13-rank-trend-analyser.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Role 102 (Group Analytics Director), Role 103 (Group MIS Officer), Role 104 (Group Academic Data Analyst), Role 105 (Group Exam Analytics Officer), Role 107 (Group Strategic Planning Officer)

---

## 1. Purpose

The Rank Trend Analyser provides a consolidated, multi-dimensional view of how students and branches rank across all group-wide competitive and internal examinations over time. It tracks All India Rank (AIR) equivalents for JEE/NEET mock examinations, group-computed rank positions for internal tests, and subject-topper lists to surface which branches and students are consistently excelling or declining. The tool enables the Academic Data Analyst and Exam Analytics Officer to detect rank mobility patterns — including students who transfer between branches and how their performance shifts — so early interventions can be planned. It also feeds scholarship merit analysis by mapping rank bands to eligibility thresholds, giving the Strategic Planning Officer a forward view for budget projections. Rank trends are computed over the current academic year (AY) and compared against the prior AY at branch, class, and individual student levels.

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Academic Data Analyst | 104 | G1 | Full (View + Export + Drill-down) | Primary owner; all controls enabled |
| Group Exam Analytics Officer | 105 | G1 | Full (View + Export + Drill-down) | Co-owner; all controls enabled |
| Group Analytics Director | 102 | G1 | View + Export | Cannot change config; read-only controls |
| Group MIS Officer | 103 | G1 | View + Export | Export enabled for MIS report generation |
| Group Strategic Planning Officer | 107 | G1 | View only | No export button shown; no drawer action buttons |
| Group Hostel Analytics Officer | 106 | G1 | No Access | This page is not visible to Role 106 |

**Access enforcement:** `@role_required([102, 103, 104, 105, 107])` Django decorator on the view. Role 107 receives a context flag `read_only=True` that disables export buttons and hides drawer action CTAs via template conditionals.

---

## 3. Page Layout

### 3.1 Breadcrumb

```
Group Portal > Analytics & MIS > Rank Trend Analyser
```

### 3.2 Page Header

**Title:** `Rank Trend Analyser`
**Sub-title:** `Branch · Class · Student rank tracking across all exams — AY 2025-26`

| Button | Visible To | Action |
|---|---|---|
| Export CSV | Roles 102, 103, 104, 105 | Downloads current filtered view as CSV |
| Export PDF Report | Roles 103, 104 | Generates formatted PDF via `/api/v1/analytics/ranks/export/pdf/` |
| AY Selector (dropdown) | All | Changes active academic year; triggers hx-get page reload |
| Filters (slide-in panel) | All | Opens filter panel: Branch multi-select, Stream, Exam Type, Class |

### 3.3 Alert Banners

Banners appear below the page header. Each is individually dismissible (session-level flag stored in `sessionStorage` keyed by banner ID). Dismissed banners do not reappear until the next page load in a new session.

| Condition | Banner Text | Severity | Banner ID |
|---|---|---|---|
| Any branch shows rank declining 3+ consecutive exams | "⚠ {N} branch(es) show rank decline in 3 or more consecutive exams. Review the Branch Rank Performance table." | Red (danger) | `rank_consec_decline` |
| Any branch has a sudden rank drop > 20 places in one exam | "⚠ Sudden rank drop detected at {Branch Name} — dropped {N} places in {Exam Name}. Investigate immediately." | Amber (warning) | `rank_sudden_drop` |
| No rank data available for the current month | "ℹ No rank data has been recorded for the current month ({Month}). Ensure exam results are uploaded." | Blue (info) | `rank_no_current_data` |

---

## 4. KPI Summary Bar

KPI cards render in a horizontal scrollable row at the top of the content area. Cards auto-refresh every 300 seconds via HTMX polling on the container div.

| Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|
| Group Average Rank | Mean rank position of all ranked students, current AY | `AVG(rank_position)` across all exams in current AY | Neutral (blue) — lower number = better | `#kpi-group-avg-rank` |
| Branches Improving | Count of branches whose AY avg rank improved vs last AY | `COUNT` where `avg_rank_current < avg_rank_prior_ay` | Green if > 50% of total branches | `#kpi-branches-improving` |
| Branches Declining | Count of branches whose AY avg rank declined vs last AY | `COUNT` where `avg_rank_current > avg_rank_prior_ay` | Red if > 3 branches | `#kpi-branches-declining` |
| Total Toppers (Rank 1–10) | Count of unique students who hold group rank 1–10 across any exam this AY | `COUNT DISTINCT(student_id)` where `group_rank <= 10` | Neutral (indigo) | `#kpi-total-toppers` |
| JEE/NEET Mock AIR Avg | Average All India Rank (mock) across all students who appeared in JEE/NEET mock tests | `AVG(air_rank)` where `exam_type IN ('JEE_MOCK','NEET_MOCK')` | Green if avg AIR < 10000 for JEE, < 5000 for NEET | `#kpi-mock-air-avg` |
| Scholarship Qualifiers | Students meeting merit scholarship threshold (configurable %) for current AY | `COUNT` where `cumulative_percentile >= scholarship_threshold_pct` | Green if count ≥ last AY count | `#kpi-scholarship-qualifiers` |

> **Auto-refresh:** `hx-trigger="every 300s"` on `#kpi-bar` div; `hx-get="/group/analytics/rank-trends/kpis/"` `hx-swap="innerHTML"`.

---

## 5. Sections

### 5.1 Branch Rank Performance Table

**Section header:** "Branch Rank Performance — AY 2025-26"
**Controls:** Search box (branch name), Pagination (25 per page), Export (CSV, same filter state)

| Column | Type | Source | Notes |
|---|---|---|---|
| Branch | Text link | `branch.name` | Click opens `rank-trend-branch-detail` drawer |
| Average Group Rank (Current AY) | Number | `AVG(exam_result.group_rank)` current AY | Lower = better; displayed as integer |
| Avg Rank Last AY | Number | `AVG(exam_result.group_rank)` prior AY | Grey text |
| Change | Delta badge | `avg_rank_current - avg_rank_last_ay` | Negative delta (improved) = green arrow ↑; Positive delta (declined) = red arrow ↓; Neutral = grey dash |
| Top 10% Count | Integer | `COUNT` where student's `percentile_rank >= 90` | Shown with small green badge |
| Bottom 30% Count | Integer | `COUNT` where student's `percentile_rank <= 30` | Shown with small red badge; clicking opens filtered student list |
| Rank Improvement Rate (%) | Percentage | `(students_improved / total_students) × 100` where improved = rank is better than same exam last AY | Green ≥ 60%, Amber 40–59%, Red < 40% |
| Toppers Count (Rank 1–10 group-wide) | Integer | `COUNT DISTINCT` students from this branch with `group_rank <= 10` in any exam | Gold star icon if > 0 |
| Actions | Buttons | — | [View Details] → opens drawer; [Export Branch Report] visible to Roles 103, 104 only |

**Row colour coding:**
- Row highlighted light-green: Branch avg rank improved ≥ 10 places vs last AY
- Row highlighted light-red: Branch avg rank declined ≥ 10 places vs last AY
- Row highlighted amber: Branch has a sudden-drop flag (rank dropped > 20 in any single exam)

**Pagination:** 25 rows per page. HTMX-driven: `hx-get="/group/analytics/rank-trends/branches/?page={n}"` `hx-target="#branch-rank-table"` `hx-swap="innerHTML"`.

**Search:** Debounced 400ms. `hx-get="/group/analytics/rank-trends/branches/?q={term}"` on `#branch-search-input`.

---

### 5.2 Topper Trends

**Section header:** "Group Toppers — AY 2025-26 (Rank 1–10)"
**Description:** Displays the top 10 students by group-wide cumulative rank (best average rank across all exams this AY).

| Column | Type | Notes |
|---|---|---|
| Group Rank | Integer (1–10) | Bold; gold medal icon for Rank 1 |
| Student Name | Text | Masked to first name + last initial for non-owner roles (Role 107); full name for Roles 102–105 |
| Branch | Text | |
| Class | Text | |
| Avg Rank This AY | Number | Primary sort key |
| Avg Rank Last AY | Number | Shown with arrow delta |
| Best Exam Rank | Number | Lowest (best) single-exam rank achieved this AY |
| Trend | Sparkline | 5-point sparkline of rank per last 5 exams (rendered via Chart.js sparkline) |
| Change vs Last AY | Badge | "New Entry", "↑ {N} places", "↓ {N} places", "Unchanged" |

**Empty state:** If fewer than 10 students have appeared in 2+ exams, display "Insufficient data to compute group toppers for the current AY. Ensure exam results for at least 2 exams are uploaded."

---

### 5.3 Rank Distribution Chart

**Section header:** "Rank Distribution — Group-wide, Current AY"

An interactive histogram showing the count of students per rank band (e.g., Rank 1–100, 101–500, 501–1000, 1001–5000, 5000+). Rendered as a bar chart via Chart.js. Filters: Exam Type (All / JEE Mock / NEET Mock / Internal), Stream (All / MPC / BiPC / MEC / HEC). See Section 7.2 for full chart specification.

---

### 5.4 Scholarship Merit Analysis

**Section header:** "Scholarship Merit Analysis — by Branch & AY"

Tracks students who qualify for merit-based scholarships by crossing a configurable percentile threshold (default: top 10% of group rank). The threshold is set in Group Settings (Division A) and read here.

| Column | Type | Notes |
|---|---|---|
| Branch | Text | |
| Total Students | Integer | Students with valid rank in current AY |
| Qualifiers This AY | Integer | Students at or above scholarship percentile threshold |
| Qualifier Rate (%) | Percentage | Green ≥ 15%, Amber 8–14%, Red < 8% |
| Qualifiers Last AY | Integer | For comparison |
| Change | Delta | ↑/↓ with colour |
| Total Scholarship Amount (₹) | Currency | Computed from per-rank-band scholarship slab (read-only from Finance division data) |
| Actions | Button | [View Qualifier List] → opens modal with student list (paginated, 20/page) |

**Filter:** AY selector (current AY preselected), Branch multi-select, Stream filter.

**Note:** Data is read-only. Scholarship amounts are pulled from Division E (Finance) scholarship slab configuration. Division M has no write access to these records.

---

## 6. Drawers & Modals

### Drawer: `rank-trend-branch-detail`

**Width:** 560px
**Trigger:** Clicking "View Details" in Section 5.1 Actions column or clicking Branch name link
**Close:** × button top-right; clicking overlay; Escape key
**HTMX load:** `hx-get="/group/analytics/rank-trends/branch-detail/{branch_id}/"` `hx-target="#drawer-content"` `hx-swap="innerHTML"` `hx-trigger="click"` on the trigger element

**Drawer Header:**
- Branch name (H2)
- Sub-text: "Branch Code · Stream · {Total Students} students · AY 2025-26"
- [Export Branch PDF] button (Roles 103, 104 only)

---

**Tab 1 — Rank Summary**

| Field | Value |
|---|---|
| Average Group Rank | Large KPI card, colour-coded |
| Standard Deviation | How spread out ranks are (low = consistent) |
| Median Rank | 50th percentile rank value |
| P10 Rank | Top 10% students' average rank |
| P90 Rank | Bottom 10% students' average rank |
| Rank Range | Min rank (best) to Max rank (worst) recorded this AY |
| Percentile Distribution Table | Bands: Top 1%, Top 5%, Top 10%, Top 25%, Top 50%, Bottom 25%, Bottom 10% — count and percentage of students in each band |
| Total Exams Contributed To | Integer — how many exams this branch's students appear in rank data |

---

**Tab 2 — Trend**

Line chart showing average group rank per exam over the current AY. X-axis: exam names in chronological order. Y-axis: average rank (inverted — lower = better shown at top). Includes:
- Branch avg rank line (primary, blue)
- Group avg rank line (grey, dashed — benchmark)
- Annotations for exam type (Monthly Test / Unit Test / Half-Yearly / Annual / Mock)
- Tooltip: exam name, date, branch avg, group avg, delta

Data endpoint: `GET /api/v1/analytics/ranks/branch-trend/?branch_id={id}&ay={ay}`

**Empty state in tab:** "No rank trend data available for this branch in AY 2025-26. Upload exam results to populate this chart."

---

**Tab 3 — Toppers**

Table of top 10 students from this specific branch ranked by cumulative avg rank in current AY.

| Column | Notes |
|---|---|
| # | Rank within branch (1–10) |
| Student Name | Full name |
| Class | Class + Section |
| Avg Rank (This AY) | |
| Avg Rank (Last AY) | With delta arrow |
| Best Single Exam Rank | |
| Exams Appeared | Count |
| Trend Sparkline | Last 5 exams |

**Empty state:** "This branch has not contributed any students to the group rank top 10 in the current AY."

---

**Tab 4 — Compare**

Side-by-side comparison:

| Metric | This Branch | Group Average | Benchmark Branch |
|---|---|---|---|
| Avg Group Rank | | | |
| Rank Std Dev | | | |
| Top 10% Count | | | |
| Bottom 30% Count | | | |
| Rank Improvement Rate | | | |
| Toppers Count | | | |

**Benchmark Branch selector:** Dropdown listing all branches in the group. Selecting a branch triggers `hx-get="/group/analytics/rank-trends/compare/?base={branch_id}&bench={branch_id2}"` `hx-target="#compare-table"` `hx-swap="innerHTML"`.

**Default benchmark:** Branch with highest composite rank improvement rate.

---

## 7. Charts

### 7.1 Average Rank Trend per Branch

| Attribute | Value |
|---|---|
| Chart Type | Multi-line (Chart.js `type: 'line'`) |
| Title | "Average Rank Trend — Top 5 & Bottom 5 Branches, Last 5 Exams" |
| X-Axis | Exam names (chronological, last 5 exams) |
| Y-Axis | Average Group Rank (inverted scale — lower rank = better, so axis is reversed using `reverse: true`) |
| Series | Top 5 improving branches (solid lines, green palette) + Bottom 5 declining branches (dashed lines, red palette) + Group Average (grey dashed) |
| Data Source | `GET /api/v1/analytics/ranks/branch-trend-multi/?ay={ay}&exam_type={type}` |
| HTMX Trigger | AY selector change, Exam Type filter change → `hx-get` reloads chart data endpoint, JavaScript re-renders via Chart.js `.update()` |
| Tooltip | Branch name + exam name + avg rank + delta vs prior exam |
| Colours | Top branches: `#22c55e`, `#16a34a`, `#15803d`, `#166534`, `#14532d`; Bottom branches: `#ef4444`, `#dc2626`, `#b91c1c`, `#991b1b`, `#7f1d1d`; Group avg: `#9ca3af` |
| Point Radius | 4px; hover radius 6px |
| Legend | Displayed below chart, scrollable if > 11 items |
| Empty State | "No rank data for the last 5 exams. Upload exam results to generate this chart." |

---

### 7.2 Score Distribution Histogram

| Attribute | Value |
|---|---|
| Chart Type | Bar chart (Chart.js `type: 'bar'`) used as histogram |
| Title | "Student Score Distribution — Group-wide, Current AY" |
| X-Axis | Score ranges: 0–9%, 10–19%, 20–29%, 30–39%, 40–49%, 50–59%, 60–69%, 70–79%, 80–89%, 90–100% |
| Y-Axis | Number of students |
| Bars | Single series (blue gradient); a normal distribution overlay (computed from mean/stddev) shown as a red dashed line using a `mixed` chart with `type: 'line'` on the second dataset |
| Filters | Exam Type, Stream — changing either re-fetches data and re-renders |
| Data Source | `GET /api/v1/analytics/ranks/score-distribution/?ay={ay}&exam_type={type}&stream={stream}` |
| Tooltip | Score range + student count + percentage of total |
| Colours | Bars: `#60a5fa` (blue-400); Normal curve line: `#ef4444` (red-500) dashed |
| Empty State | "No score data available for the selected filters." |

---

## 8. Toast Messages

| Action | Toast Text | Type |
|---|---|---|
| CSV export initiated | "Rank data export started. Your download will begin shortly." | Success (green) |
| PDF export initiated | "PDF report is being generated. It will download automatically." | Success (green) |
| CSV export failed | "Export failed. Please try again or contact support." | Error (red) |
| PDF export failed | "PDF generation failed. Check that data is available for selected filters." | Error (red) |
| Branch detail drawer loaded | (No toast — silent HTMX swap) | — |
| Drawer data load failed | "Unable to load branch details. Please refresh and try again." | Error (red) |
| Compare benchmark changed | "Comparison updated for selected benchmark branch." | Info (blue) |
| Alert banner dismissed | (No toast — silent sessionStorage flag set) | — |

---

## 9. Empty States

| Context | Icon | Heading | Sub-text | Action |
|---|---|---|---|---|
| Branch Rank Performance Table — no data | Chart bar icon | "No Rank Data Available" | "No exam results with rank data found for AY 2025-26. Ask the Exam Division to upload results." | [Go to Exam Division] (link) |
| Topper Trends — fewer than 10 ranked students | Trophy icon | "Insufficient Data for Toppers" | "At least 10 students need rank data from 2+ exams to generate this list." | [Refresh] |
| Scholarship Merit Analysis — no qualifiers | Star icon | "No Scholarship Qualifiers Found" | "No students meet the current scholarship threshold. Check threshold settings in Group Settings." | [Open Settings] |
| Branch drawer — no trend data | Line chart icon | "No Trend Data" | "Rank trend for this branch requires at least 2 exams with results." | [Close Drawer] |
| Branch drawer Tab 3 (Toppers) — no toppers | User icon | "No Toppers from This Branch" | "No student from this branch has appeared in the group top 10 this AY." | — |
| Score Distribution Histogram — no data | Bar chart icon | "No Score Data" | "Score distribution data is unavailable for the current filter combination." | [Reset Filters] |

---

## 10. Loader States

| Context | Loader Behaviour |
|---|---|
| KPI bar initial load | Skeleton cards (grey animated pulse) replace each KPI card; 5 grey rectangles of KPI card size |
| KPI bar auto-refresh | Subtle spinner icon in top-right corner of KPI bar; cards retain last values |
| Branch Rank Performance Table | Full-height skeleton table (5 rows of grey bars) with a spinner overlay |
| Chart 7.1 loading | Grey rectangle placeholder with centred spinner + "Loading chart data…" label |
| Chart 7.2 loading | Same pattern as 7.1 |
| Drawer opening | Right-side drawer slides in with skeleton content (title bar + 3 skeleton lines + chart placeholder) |
| Drawer tab switch | Spinner in tab content area; previous content fades to 50% opacity |
| Compare table reload | Inline spinner replacing table body; cells show "—" during load |
| Export (CSV/PDF) | Button shows spinner + "Generating…" text; disabled state until response arrives |

---

## 11. Role-Based UI Visibility

| UI Element | Role 102 | Role 103 | Role 104 | Role 105 | Role 107 |
|---|---|---|---|---|---|
| Export CSV button | Visible | Visible | Visible | Visible | Hidden |
| Export PDF button | Hidden | Visible | Visible | Hidden | Hidden |
| Branch Report Export (drawer) | Hidden | Visible | Visible | Hidden | Hidden |
| Drawer — View Details button | Visible | Visible | Visible | Visible | Visible |
| Scholarship Qualifier List modal | Visible (read) | Visible (read) | Visible (read) | Visible (read) | Hidden |
| Student full names in Toppers table | Visible | Visible | Visible | Visible | Masked (first + last initial) |
| Alert banners | All visible | All visible | All visible | All visible | All visible |
| Filter panel | Visible | Visible | Visible | Visible | Visible |
| Compare tab — benchmark selector | Visible | Visible | Visible | Visible | Visible (read-only, no changes saved) |
| AY selector | Visible | Visible | Visible | Visible | Visible |

---

## 12. API Endpoints

### 12.1 KPI Bar

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/analytics/ranks/kpis/` | JWT (G1) | Returns all 6 KPI values for the summary bar |

**Query params:**

| Param | Type | Required | Description |
|---|---|---|---|
| `ay` | string | No | Academic year, e.g. `2025-26`. Defaults to current AY. |
| `branch_ids` | string (CSV) | No | Comma-separated branch IDs to filter; defaults to all |

---

### 12.2 Branch Rank Performance List

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/analytics/ranks/branches/` | JWT (G1) | Paginated branch rank performance data |

**Query params:**

| Param | Type | Required | Description |
|---|---|---|---|
| `ay` | string | No | Academic year |
| `q` | string | No | Branch name search term |
| `stream` | string | No | `MPC`, `BiPC`, `MEC`, `HEC`, `ALL` |
| `page` | integer | No | Page number (default 1) |
| `page_size` | integer | No | Rows per page (default 25, max 100) |
| `sort_by` | string | No | Column to sort by; default `avg_rank_current` |
| `sort_dir` | string | No | `asc` or `desc` |

---

### 12.3 Branch Rank Detail (Drawer)

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/analytics/ranks/branch-detail/{branch_id}/` | JWT (G1) | All drawer data for a branch (Tab 1 summary + Tab 3 toppers) |
| GET | `/api/v1/analytics/ranks/branch-trend/{branch_id}/` | JWT (G1) | Exam-by-exam rank trend data for Tab 2 chart |

**Query params for branch-detail:**

| Param | Type | Required | Description |
|---|---|---|---|
| `ay` | string | No | Academic year |

---

### 12.4 Multi-Branch Trend (Chart 7.1)

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/analytics/ranks/branch-trend-multi/` | JWT (G1) | Returns rank trend data for top 5 + bottom 5 branches + group avg |

**Query params:**

| Param | Type | Required | Description |
|---|---|---|---|
| `ay` | string | No | Academic year |
| `exam_type` | string | No | `ALL`, `MONTHLY`, `UNIT`, `HALFYEARLY`, `ANNUAL`, `JEE_MOCK`, `NEET_MOCK` |
| `limit_exams` | integer | No | Last N exams to include (default 5) |

---

### 12.5 Score Distribution (Chart 7.2)

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/analytics/ranks/score-distribution/` | JWT (G1) | Score distribution histogram data with normal curve parameters |

**Query params:**

| Param | Type | Required | Description |
|---|---|---|---|
| `ay` | string | No | Academic year |
| `exam_type` | string | No | Exam type filter |
| `stream` | string | No | Stream filter |
| `branch_ids` | string (CSV) | No | Branch filter |

---

### 12.6 Branch Comparison (Drawer Tab 4)

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/analytics/ranks/compare/` | JWT (G1) | Side-by-side comparison of two branches + group average |

**Query params:**

| Param | Type | Required | Description |
|---|---|---|---|
| `base` | integer | Yes | Base branch ID |
| `bench` | integer | Yes | Benchmark branch ID |
| `ay` | string | No | Academic year |

---

### 12.7 Scholarship Merit Analysis

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/analytics/ranks/scholarship/` | JWT (G1) | Scholarship qualifier counts by branch |

**Query params:**

| Param | Type | Required | Description |
|---|---|---|---|
| `ay` | string | No | Academic year |
| `branch_ids` | string (CSV) | No | Branch filter |
| `stream` | string | No | Stream filter |

---

### 12.8 Export Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/analytics/ranks/export/csv/` | JWT (G1, Roles 102–105) | Streams CSV of current filtered branch rank data |
| GET | `/api/v1/analytics/ranks/export/pdf/` | JWT (G1, Roles 103, 104) | Generates and streams PDF rank analytics report |

---

## 13. HTMX Patterns

| Pattern | Trigger Element | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI bar auto-refresh | `#kpi-bar` div | `hx-get="/group/analytics/rank-trends/kpis/"` | `#kpi-bar` | `innerHTML` | `hx-trigger="every 300s"` |
| Branch table — search | `#branch-search-input` input | `hx-get="/group/analytics/rank-trends/branches/?q={val}"` | `#branch-rank-table` | `innerHTML` | Debounced 400ms via `hx-trigger="keyup changed delay:400ms"` |
| Branch table — pagination | Pagination link buttons | `hx-get="/group/analytics/rank-trends/branches/?page={n}"` | `#branch-rank-table` | `innerHTML` | Preserves existing filter query params via hidden inputs |
| Branch table — AY filter | `#ay-selector` select | `hx-get="/group/analytics/rank-trends/branches/?ay={val}"` | `#branch-rank-table` | `innerHTML` | Also triggers KPI bar reload |
| Open branch detail drawer | [View Details] button | `hx-get="/group/analytics/rank-trends/branch-detail/{id}/"` | `#drawer-content` | `innerHTML` | `hx-trigger="click"`; JS opens drawer panel |
| Drawer tab switch | Tab button elements | `hx-get="/group/analytics/rank-trends/branch-detail/{id}/tab/{n}/"` | `#drawer-tab-content` | `innerHTML` | Adds `hx-indicator="#drawer-spinner"` |
| Compare benchmark select | `#benchmark-branch-select` | `hx-get="/group/analytics/rank-trends/compare/?base={base}&bench={val}"` | `#compare-table` | `innerHTML` | `hx-trigger="change"` |
| Score distribution filter | `#score-dist-exam-type`, `#score-dist-stream` selects | `hx-get="/group/analytics/rank-trends/score-dist/?..."` | `#score-dist-chart-data` | `innerHTML` | JS re-renders Chart.js after swap |
| Chart 7.1 filter | `#chart-exam-type-filter` | `hx-get="/group/analytics/rank-trends/branch-trend-multi/?..."` | `#rank-trend-chart-data` | `innerHTML` | JS calls `chart.update()` after HTMX swap |
| Alert banner dismiss | [×] button on each banner | `hx-post="/group/analytics/dismiss-banner/"` | `#banner-{id}` | `outerHTML` | Sets `sessionStorage` flag; posts banner ID to server for analytics; swaps banner with empty div |
| Scholarship table — pagination | Pagination links | `hx-get="/group/analytics/rank-trends/scholarship/?page={n}"` | `#scholarship-table` | `innerHTML` | — |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
