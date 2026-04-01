# Page 17: Exam Performance Heatmap

**Division:** M — Analytics & MIS
**URL:** `/group/analytics/exam-heatmap/`
**Primary Role:** 105 — Exam Analytics Officer
**Supporting Roles:** 102 (Analytics Director), 103 (MIS Officer), 104 (Academic Data Analyst)
**Access Level:** G1 (read-only on exam data from Division D; no write on operational records)

---

## 1. Purpose

Renders a colour-coded, interactive heatmap grid that maps **branches × subjects × exams** against a chosen performance metric (avg score, pass %, below-threshold %, or rank band). Enables the Exam Analytics Officer to identify systemic weak spots across the institution, compare exam cycles, and escalate low-performing branch-subject pairs to branch principals.

---

## 2. Roles & Permissions Matrix

| UI Element | Role 102 | Role 103 | Role 104 | Role 105 |
|---|---|---|---|---|
| KPI bar (5 cards) | View | View | View | View |
| Dimension selector (rows/cols/metric) | View + change | View + change | View + change | View + change |
| Heatmap grid | View | View | View | View |
| Drilldown drawer | View | View | View | View |
| Low-performer alert panel | View | View | View | View |
| Escalate to branch (create escalation) | — | — | — | Create |
| Gap insight note (add/edit/delete) | — | — | — | Create/Edit/Delete |
| Export heatmap (CSV / PNG) | Download | Download | Download | Download |
| Exam cycle selector | All cycles | All cycles | All cycles | All cycles |

Server-side: all data returned by `/api/v1/analytics/exam-heatmap/` is pre-filtered to branches within the authenticated user's institution group. No additional row-level filtering needed for this page.

---

## 3. Page Layout

```
┌─────────────────────────────────────────────────────────────────────┐
│ Breadcrumb: Analytics & MIS > Exam Performance Heatmap              │
│ Title: "Exam Performance Heatmap"   [Export ▼]  [Refresh]           │
├─────────────────────────────────────────────────────────────────────┤
│  DIMENSION CONTROL BAR                                               │
│  Rows [Branch ▼]  Cols [Subject ▼]  Metric [Avg Score ▼]            │
│  Exam Cycle [2025-26 Term 2 ▼]  Stream [All ▼]  Class [All ▼]       │
│  Threshold [< 40 %]  [Apply]                                         │
├─────────────────────────────────────────────────────────────────────┤
│  KPI BAR (5 cards)                                                   │
│  Total Exams | Avg Score | Pass % | Below-Threshold Cells | High-   │
│              |           |        | Risk Branch-Subject Pairs| Perf  │
├──────────────────────────────────────┬──────────────────────────────┤
│  HEATMAP GRID (Chart.js matrix)      │  LOW-PERFORMER ALERT PANEL   │
│  Rows = branches                     │  Top 10 at-risk cells        │
│  Cols = subjects                     │  [Branch | Subject | Score]  │
│  Cell = colour band (5-tier)         │  [Escalate] per row          │
│  Click cell → drilldown drawer       │                              │
├──────────────────────────────────────┴──────────────────────────────┤
│  EXAM SCORE TREND CHART (Line — top 5 subjects over last 6 cycles)   │
├─────────────────────────────────────────────────────────────────────┤
│  GAP INSIGHT NOTES TABLE             [+ Add Note]                    │
│  Branch | Subject | Note | Added By | Date | Actions               │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 4. Dimension Control Bar

### 4.1 Controls

| Control | Type | Options | Default |
|---|---|---|---|
| Rows | Select | Branch / Class / Stream | Branch |
| Cols | Select | Subject / Exam Name / Exam Type | Subject |
| Metric | Select | Avg Score / Pass % / Below-Threshold % / Rank Band | Avg Score |
| Exam Cycle | Select | All active cycles for this group | Latest cycle |
| Stream | Select | All / Science / Commerce / Arts / Vocational | All |
| Class | Select | All / 11 / 12 / 9 / 10 | All |
| Threshold | Number input | Numeric % (default 40) | 40 |

### 4.2 Behaviour

- All controls are `hx-get="/group/analytics/exam-heatmap/grid/"` with `hx-trigger="change"` (debounced 400 ms).
- `[Apply]` button triggers an explicit full reload: `hx-get` with all query params, `hx-target="#heatmap-section"`, `hx-swap="outerHTML"`, `hx-indicator="#heatmap-loader"`.
- Changing Rows or Cols fires a separate `hx-get="/group/analytics/exam-heatmap/axis-labels/"` to update the axis label lists before the grid reloads, preventing stale axis labels.
- Active dimension selections are persisted to `localStorage` under key `heatmap_prefs` so they survive page reload.

---

## 5. KPI Bar

Five stat cards in a horizontal row (wraps to 2-3 cols on mobile). Each card uses `hx-trigger="every 300s"` auto-refresh.

| # | Card Label | Value | Sub-label | Trend |
|---|---|---|---|---|
| 1 | Total Exams | Count of distinct exams in filter | "This cycle" | — |
| 2 | Group Avg Score | Mean score across all cells | "vs prev cycle" | ↑ / ↓ delta |
| 3 | Pass % | % students scoring ≥ pass mark | "Target: 85%" | colour-coded |
| 4 | Below-Threshold Cells | Count of heatmap cells below threshold | "of {total} cells" | — |
| 5 | High-Risk Pairs | Distinct branch-subject pairs with < threshold for 2+ consecutive cycles | — | — |

Card 4 and 5 are highlighted with `bg-red-50 border-red-300` when non-zero.

---

## 6. Heatmap Grid

### 6.1 Rendering

- Rendered with **Chart.js 4.x** `matrix` chart type (via `chartjs-chart-matrix` plugin).
- Canvas id: `examHeatmapCanvas`.
- Dimensions: full-width, fixed row height 32px, scrollable horizontally if > 10 columns.
- Colour scale (5 tiers, colorblind-safe using Okabe-Ito palette):

| Tier | Range (Avg Score) | Fill | Label |
|---|---|---|---|
| 1 | ≥ 80 | `#009E73` (green) | Excellent |
| 2 | 65–79 | `#56B4E9` (sky blue) | Good |
| 3 | 50–64 | `#F0E442` (yellow) | Average |
| 4 | 35–49 | `#E69F00` (amber) | Below Avg |
| 5 | < 35 | `#D55E00` (red) | Critical |

- When Metric = "Pass %" or "Below-Threshold %", the scale shifts accordingly (anchored at 85% pass = tier 1).
- Each cell displays the numeric value in white/dark text (auto-contrast).
- Below-threshold cells get a `⚠` icon overlay in the top-right corner of the cell.
- Hovering a cell shows a tooltip: `{row label} × {col label}: {value} ({n} students)`.

### 6.2 Click → Drilldown Drawer

Clicking any cell fires:
```
hx-get="/group/analytics/exam-heatmap/drilldown/?row={row_id}&col={col_id}&metric={metric}&cycle={cycle}"
hx-target="#exam-heatmap-drilldown-drawer"
hx-swap="innerHTML"
```
Then JavaScript opens the drawer: `document.getElementById('exam-heatmap-drilldown-drawer').classList.remove('hidden')`.

### 6.3 Empty / Loading States

- **Loading:** grey shimmer grid (same dimensions) shown while `hx-indicator="#heatmap-loader"` is active.
- **Empty:** centred card — "No exam data found for the selected filters. Adjust the Exam Cycle or Stream." with a "Reset Filters" button.
- **Partial data:** cells with no data show `—` (em dash) with `bg-gray-100` and are not clickable.

---

## 7. Exam Heatmap Drilldown Drawer

**ID:** `exam-heatmap-drilldown-drawer`
**Width:** 640px slide-in from right
**Header:** `{Branch} × {Subject}` — e.g. "Hyderabad Main × Physics"

### Tab 1 — Score Summary

| Field | Display |
|---|---|
| Exam Name | Text |
| Exam Date | Formatted date |
| Class / Stream | Text |
| No. of Students | Integer |
| Avg Score | Large stat with colour band |
| Median Score | Integer |
| Highest Score | Integer |
| Lowest Score | Integer |
| Pass % | Donut mini-chart (pass vs fail) |
| Below Threshold % | Stat + colour badge |
| Standard Deviation | Float (2dp) |

**Score Distribution Mini-Chart:** Horizontal bar chart (10-point buckets: 0-9, 10-19, …, 90-100) showing student count per bucket. Canvas id: `drilldownDistChart`.

### Tab 2 — Student List

Scrollable table of students in this branch-subject cell:

| Column | Type |
|---|---|
| Student Name | Text (truncated) |
| Admission No | Text |
| Class | Text |
| Score | Integer |
| Grade | Badge (A/B/C/D/F, colour-coded) |
| Rank (within branch) | Integer |
| Below Threshold? | Icon (⚠ / —) |

- Sorted by Score ascending by default (lowest first).
- Search box filters by name or admission number (`hx-get` with debounce 300ms).
- Pagination: 15 rows per page, HTMX-driven.
- **Role visibility:** Student names masked to initials (`R. S.`) for Role 102 and 103; full names visible for Roles 104 and 105. Applied server-side.

### Tab 3 — Gap Escalation

**Role 105 only** — other roles see read-only view.

**Existing escalations for this pair:** table listing open and resolved escalations with `[View]` action.

**Create Escalation Form:**

| Field | Type | Validation |
|---|---|---|
| Branch | Read-only (pre-filled) | — |
| Subject | Read-only (pre-filled) | — |
| Exam Cycle | Read-only (pre-filled) | — |
| Severity | Select: Low / Medium / High / Critical | Required |
| Root Cause Category | Select: Teaching Gap / Syllabus Coverage / Question Paper Difficulty / External Factors / Unknown | Required |
| Description | Textarea (max 1000 chars) | Required, min 20 chars |
| Recommended Action | Textarea (max 500 chars) | Required |
| Assign To (Branch Principal) | Select (populated from branch principals in this group) | Required |
| Target Resolution Date | Date picker (min: today + 3 days) | Required |
| Supporting Data | Checkbox: "Attach current heatmap snapshot" | Optional |
| Notify via | Checkbox group: In-app / Email | At least one |

**Submit:** POST `/api/v1/analytics/exam-heatmap/escalations/` → success toast → escalation row appended to table above → form clears.

---

## 8. Low-Performer Alert Panel

Right sidebar panel showing the top 10 below-threshold branch-subject pairs sorted by severity (score ascending, then consecutive-cycles-below-threshold descending).

| Column | Notes |
|---|---|
| # | Rank badge |
| Branch | Text with branch code |
| Subject | Text |
| Avg Score | Coloured badge (tier) |
| Consecutive Cycles | "3 cycles" badge — red if ≥ 2 |
| Action | [Escalate] button (Role 105 only); [View] for others |

- **[Escalate]** opens the `exam-heatmap-drilldown-drawer` directly on Tab 3 (Gap Escalation), pre-filled with the row's branch + subject.
- Panel title shows count badge: "Low-Performer Pairs (8)".
- HTMX auto-refresh every 300 s: `hx-trigger="every 300s"` `hx-get="/group/analytics/exam-heatmap/alerts/"` `hx-target="#low-performer-panel"`.

---

## 9. Exam Score Trend Chart

**Type:** Multi-line chart (Chart.js 4.x Line)
**Canvas ID:** `examTrendChart`
**Height:** 280px

- X-axis: Last 6 exam cycles (oldest → newest).
- Y-axis: Selected metric value (Avg Score / Pass %).
- Lines: Top 5 subjects by student volume (configurable via "Subjects" multi-select pill).
- Tooltip: `{Subject}: {value} ({cycle})`.
- Legend: bottom, horizontal.
- Each subject line uses a distinct colorblind-safe colour from the Okabe-Ito set.
- Clicking a line filters the heatmap grid to show only that subject in the Cols dimension.

---

## 10. Gap Insight Notes Table

A lightweight annotation layer — allows Role 105 to attach free-text insights to any branch-subject pair without creating a formal escalation.

**Table Columns:**

| Column | Type | Sortable |
|---|---|---|
| Branch | Text | Yes |
| Subject | Text | Yes |
| Note | Text (truncated 120 chars) | No |
| Added By | Name + role badge | No |
| Date | Formatted date | Yes |
| Actions | Edit / Delete (Role 105 own notes only) | — |

**Pagination:** 10 rows per page, HTMX-driven.
**Search:** `hx-get` with debounce 300ms on branch + subject + note text.

**Add Note Drawer (Role 105 only):**

Triggered by `[+ Add Note]` button.

| Field | Type | Validation |
|---|---|---|
| Branch | Select (branches in group) | Required |
| Subject | Select (subjects available) | Required |
| Exam Cycle | Select | Required |
| Note Text | Textarea (max 500 chars) | Required, min 10 chars |
| Visibility | Radio: "Division M only" / "Visible to Branch Principal" | Required |

**Edit:** opens same drawer pre-filled. **Delete:** confirm modal → DELETE request → row removed with toast.

---

## 11. Export Modal

Triggered by `[Export ▼]` button → dropdown with options:

| Option | Action |
|---|---|
| Export Heatmap as PNG | Calls `Chart.toBase64Image()` → download |
| Export Grid Data as CSV | GET `/api/v1/analytics/exam-heatmap/export/?format=csv&{filters}` |
| Export Full Report (PDF) | POST `/api/v1/analytics/exam-heatmap/export/` `{format: "pdf"}` → async job → polling |
| Export Escalations CSV | GET `/api/v1/analytics/exam-heatmap/escalations/export/` |

**PDF Export Flow:**
1. POST creates export job → returns `{job_id}`.
2. Modal body switches to progress state: "Generating PDF… this may take a few seconds."
3. HTMX polls `GET /api/v1/analytics/export-jobs/{job_id}/status/` every 5s until `status=complete`.
4. On complete: download link shown + success toast "Heatmap PDF ready."
5. On error: error toast "PDF generation failed. Try again."

All exports include the active filter parameters in the filename, e.g. `exam-heatmap_2025-26-T2_branch_subject_avg-score_2026-03-22.csv`.

---

## 12. Toast Notifications

| Trigger | Type | Message |
|---|---|---|
| Escalation created | Success | "Escalation raised for {Branch} × {Subject}. Assigned to {Principal Name}." |
| Escalation form validation fail | Error | "Please fill in all required fields." |
| Gap insight note saved | Success | "Note saved for {Branch} × {Subject}." |
| Note deleted | Info | "Note removed." |
| Export started | Info | "Preparing {format} export…" |
| Export ready | Success | "Export ready. Click to download." |
| Export failed | Error | "Export failed. Please try again." |
| Heatmap grid error (5xx) | Error | "Failed to load heatmap. Retrying in 30s." |
| Auto-refresh triggered | Info (silent) | No toast — silent reload |

---

## 13. Empty States

| Context | Illustration | Message | CTA |
|---|---|---|---|
| No exams in selected cycle | Bar chart icon (grey) | "No exam data found for this cycle and filter combination." | "Reset Filters" |
| No below-threshold cells | Green checkmark | "All branch-subject pairs are above the threshold. " | — |
| No escalations for this pair | Clipboard icon | "No escalations yet for this pair." | "Create Escalation" (Role 105) |
| No gap insight notes | Pencil icon | "No insight notes added yet." | "+ Add Note" (Role 105) |
| All exams data pending | Hourglass icon | "Exam results for this cycle are still being uploaded by branches." | — |

---

## 14. Loader States

| Element | Loader Type |
|---|---|
| Initial page load | Full-page skeleton: 5 card shimmer + grid shimmer + panel shimmer |
| Heatmap grid reload (filter change) | Grid shimmer overlay (preserves axis labels) |
| KPI bar refresh | Individual card shimmer |
| Drilldown drawer open | Spinner centred in drawer body |
| Student list pagination | Row shimmer (15 rows) |
| Low-performer panel refresh | Panel shimmer |
| Trend chart reload | Canvas grey overlay with spinner |
| Export PDF generation | Progress indicator in modal |

---

## 15. HTMX Patterns

| Pattern | Element | Endpoint | Trigger |
|---|---|---|---|
| Grid reload on filter change | `#heatmap-section` | `/group/analytics/exam-heatmap/grid/` | `change` on any control (debounced) |
| KPI auto-refresh | `#heatmap-kpi-bar` | `/group/analytics/exam-heatmap/kpis/` | `every 300s` |
| Alert panel auto-refresh | `#low-performer-panel` | `/group/analytics/exam-heatmap/alerts/` | `every 300s` |
| Drilldown drawer load | `#exam-heatmap-drilldown-drawer` | `/group/analytics/exam-heatmap/drilldown/` | Cell click |
| Student list search | `#drilldown-student-tbody` | `/group/analytics/exam-heatmap/drilldown/students/` | `keyup changed delay:300ms` |
| Student list pagination | `#drilldown-student-tbody` | `/group/analytics/exam-heatmap/drilldown/students/?page={n}` | Button click |
| Notes search | `#gap-notes-tbody` | `/group/analytics/exam-heatmap/notes/` | `keyup changed delay:300ms` |
| Notes pagination | `#gap-notes-tbody` | `/group/analytics/exam-heatmap/notes/?page={n}` | Button click |
| Escalation POST | `#escalation-form` | `/api/v1/analytics/exam-heatmap/escalations/` | Form submit |
| Note POST/PUT | `#note-form` | `/api/v1/analytics/exam-heatmap/notes/` | Form submit |
| Export job poll | `#export-status` | `/api/v1/analytics/export-jobs/{id}/status/` | `every 5s` (stops on complete) |
| Axis label update | `#heatmap-axis-labels` | `/group/analytics/exam-heatmap/axis-labels/` | Rows/Cols change |

---

## 16. API Endpoints

| Method | Endpoint | Purpose | Auth |
|---|---|---|---|
| GET | `/api/v1/analytics/exam-heatmap/` | Full page data (KPIs + grid + alerts) | G1 |
| GET | `/api/v1/analytics/exam-heatmap/grid/` | Heatmap matrix data | G1 |
| GET | `/api/v1/analytics/exam-heatmap/kpis/` | KPI card values | G1 |
| GET | `/api/v1/analytics/exam-heatmap/alerts/` | Low-performer alert list | G1 |
| GET | `/api/v1/analytics/exam-heatmap/axis-labels/` | Row/col label lists | G1 |
| GET | `/api/v1/analytics/exam-heatmap/drilldown/` | Drilldown drawer data | G1 |
| GET | `/api/v1/analytics/exam-heatmap/drilldown/students/` | Student list (paginated) | G1 |
| GET | `/api/v1/analytics/exam-heatmap/trend/` | Score trend chart data | G1 |
| GET | `/api/v1/analytics/exam-heatmap/escalations/` | Escalation list | G1 |
| POST | `/api/v1/analytics/exam-heatmap/escalations/` | Create escalation | Role 105 |
| GET | `/api/v1/analytics/exam-heatmap/escalations/export/` | Export escalations CSV | G1 |
| GET | `/api/v1/analytics/exam-heatmap/notes/` | Gap insight notes list | G1 |
| POST | `/api/v1/analytics/exam-heatmap/notes/` | Add gap note | Role 105 |
| PUT | `/api/v1/analytics/exam-heatmap/notes/{id}/` | Edit gap note | Role 105 (own) |
| DELETE | `/api/v1/analytics/exam-heatmap/notes/{id}/` | Delete gap note | Role 105 (own) |
| POST | `/api/v1/analytics/exam-heatmap/export/` | Trigger async export job | G1 |
| GET | `/api/v1/analytics/export-jobs/{id}/status/` | Poll export job status | G1 |

---

## 17. Mobile (Flutter + Riverpod)

| Screen | Description |
|---|---|
| `ExamHeatmapScreen` | Summary KPI cards + scrollable condensed heatmap (columns scroll horizontally) |
| `HeatmapCellDetailScreen` | Score summary tab only; student list masked for non-105 roles |
| `LowPerformerListScreen` | Sortable list of below-threshold pairs; no escalation creation (desktop-only) |
| `ExamTrendScreen` | Line chart for selected subject across last 6 cycles |

Mobile state managed by `examHeatmapProvider` (Riverpod). Refresh on pull-to-refresh. No chart plugin required — Chart.js is web only; Flutter uses `fl_chart` for native charts.

---

## 18. Accessibility & Responsiveness

- Heatmap grid scrolls horizontally on screens < 1024px; row labels are sticky on the left.
- Colour bands are **not** the only encoding — each cell also displays the numeric value. Screen readers receive `aria-label="{row label} × {col label}: {value} — {tier label}"` (e.g. `"Hyderabad Main × Physics: 58 — Average"`).
- Heatmap container has `role="grid"` and `aria-label="Exam Performance Heatmap — {metric} by {rows} and {cols}"`. Each row has `role="row"`; each cell has `role="gridcell"` and `tabindex="0"`.
- **Keyboard navigation within grid:** `Tab` enters the grid and focuses the first cell. `Arrow keys` (↑ ↓ ← →) move focus between cells. `Enter` or `Space` opens the drilldown drawer for the focused cell. `Escape` while in the grid returns focus to the first control in the Dimension Control Bar.
- Colour legend rendered as a horizontal key with text labels below each swatch; each swatch also has a `title` attribute with the tier name and score range.
- All interactive controls (Rows/Cols/Metric dropdowns, Apply button) are keyboard-navigable with visible focus rings (`outline: 2px solid #4F46E5`).
- Drilldown drawer: focus is trapped inside the drawer while open; `Escape` closes the drawer and returns focus to the originating grid cell.
- Escalation and note forms: all required fields have `aria-required="true"` and inline error messages tied via `aria-describedby`.
- Below-threshold `⚠` icon overlays have `aria-hidden="true"` (decorative — the cell `aria-label` already conveys the severity).
