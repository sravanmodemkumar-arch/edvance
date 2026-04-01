# 16 — Inter-Branch Benchmarking

> **URL:** `/group/gov/benchmarking/`
> **File:** `16-inter-branch-benchmarking.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Chairman G5 · MD G5 · CEO G4 · President G4 · VP G4 · Trustee G1 (read) · Advisor G1 (read)

---

## 1. Purpose

Side-by-side comparison of all branches across every KPI. Enables leadership to identify
top and bottom performers, understand which branches need intervention, and allocate support
resources accordingly. A student in Branch A must compete fairly with Branch B — this page
makes the inequality visible.

Key use cases:
- Spot branches with poor exam scores AND low fee collection (double risk)
- Identify consistently strong branches to use as benchmarks for others
- Export benchmarking report for board meeting or zone director review

---

## 2. Role Access

| Role | Access | Notes |
|---|---|---|
| Chairman | Full — all metrics, export, comparison | |
| MD | Full | |
| CEO | Full | |
| President | Full — academic metrics prominent, but all visible | |
| VP | Full — ops metrics prominent, but all visible | |
| Trustee | Read-only — no filter, no export | |
| Advisor | Read-only + export | Research tool |
| Exec Secretary | ❌ | |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Inter-Branch Benchmarking
```

### 3.2 Page Header
```
Inter-Branch Benchmarking                              [Compare Selected ▼]  [Export PDF ↓]
All 50 branches · FY 2026–27 · Last updated: [date]
```

### 3.3 View Controls

| Control | Options |
|---|---|
| View Mode | Table · Heat Map · Radar Comparison |
| Metric Category | All · Enrollment · Finance · Academic · Staff · Compliance · Ops |
| Period | This Month · This Quarter · This Year |
| Branch Filter | Multi-select (default: all) |
| Zone Filter | Multi-select (large groups) |

---

## 4. Table View (default)

### 4.1 Master Benchmarking Table

Branches as rows. Metrics as columns. Cell colour-coded by performance tier.

**Search:** Branch name, city. Debounce 300ms.

**Filters (advanced, slide-in):**
| Filter | Options |
|---|---|
| State | Multi-select |
| Zone | Multi-select |
| Branch Type | Day · Hostel · Both |
| Performance Tier | Top 25% · Mid · Bottom 25% |
| Stream | Multi-select |

**Row selection:** Checkbox per branch — for Radar Comparison view.

**Column groups:**

| Group | Columns |
|---|---|
| Identity | Branch Name · City · Zone · Type |
| Enrollment | Total · Day Scholar · Hosteler · New Admissions · Retention % |
| Finance | Fee Collection % · Revenue ₹ · Outstanding ₹ · Per-Student Revenue ₹ |
| Academic | Avg Score % · Pass % · Toppers · Curriculum % |
| Staff | Total Staff · Vacancy % · BGV % · POCSO % |
| Compliance | Compliance Score · CBSE Status · Last Audit |
| Operations | SLA Score · Open Escalations · Grievances |

**Column visibility toggle:** Gear icon top-right — default shows key columns only, can expand.

**Cell colour coding (per column):**
- Green: Top 25th percentile within group
- Yellow: Mid 50th percentile
- Red: Bottom 25th percentile
- Each cell: Value + small coloured dot

**Default sort:** Composite Score column descending.

**Row click:** Opens Branch Detail page 10 for that branch.

**Pagination:** 25/page. But for small groups (≤20 branches) "Show All" by default.

**Bulk actions (for selected rows):**
- [Compare in Radar Chart] → opens radar comparison modal
- [Export Selected CSV] → downloads CSV of selected branches

---

## 5. Heat Map View

**Display:** Same data as table but displayed as a colour-graded matrix.

- **Rows:** Branches (sorted by composite score default)
- **Columns:** One per metric
- **Cell:** Colour intensity (dark green = best in group, dark red = worst)
- **Hover tooltip:** Branch Name · Metric · Value · Rank N of 50

**Export:** PNG of entire heat map.

---

## 6. Radar Comparison View

**Trigger:** Select 2–5 branches via row checkboxes → [Compare Selected] button.

**Display:** Radar (spider) chart — one polygon per selected branch, overlaid.

**Axes:** 6 axes = Enrollment % · Fee % · Academic % · Staff BGV % · Compliance % · SLA %.

**Legend:** Branch name + colour per polygon.

**Tooltip:** Axis name · Branch: Value %.

**Export:** PNG.

---

## 7. Drawers

### 7.1 Drawer: `kpi-drill` (reused from page 14)
- **Trigger:** Click any metric cell in table
- **Width:** 480px
- **Tabs:** Trend · By Branch · Variance
- Same spec as page 14 `kpi-drill` drawer

---

## 8. Composite Score Methodology

Displayed as an info card on the page:

| Metric | Weight |
|---|---|
| Academic (Avg Score × Pass Rate) | 30% |
| Finance (Fee Collection Rate) | 25% |
| Enrollment vs Target | 20% |
| Compliance (BGV + POCSO + CBSE) | 15% |
| Operations (SLA Score) | 10% |

Score = weighted average of metric achievement %. Range: 0–100.

**Methodology [?] tooltip on column header** — explains the formula.

---

## 9. Charts

### 9.1 Radar Comparison Chart (comparison mode)
- **Type:** Radar / Spider chart
- **Library:** Chart.js 4.x
- **Axes:** 6 (as above)
- **Max branches compared:** 5 (more creates visual clutter)
- **Colours:** Colorblind-safe palette (6 distinct colours)
- **Export:** PNG

### 9.2 Composite Score Distribution (all branches)
- **Type:** Bar chart (sorted ascending — worst to best)
- **X-axis:** Branch codes
- **Y-axis:** Composite score (0–100)
- **Benchmark line:** Group average
- **Colour:** Red <60 · Yellow 60–80 · Green >80
- **Export:** PNG

### 9.3 Metric Correlation Scatter (two-metric view)
- **Select X-axis metric** and **Y-axis metric** from dropdowns
- **Type:** Scatter — each branch as a dot
- **Quadrant:** auto-calculated based on group median
- **Tooltip:** Branch · X value · Y value
- **Export:** PNG

---

## 10. Export

**[Export PDF ↓] button:**
- Opens 480px modal: Report type selection (Full Benchmarking · Top/Bottom 10 · By Zone · Academic Only · Finance Only)
- Date range
- Include charts? (checkbox)
- [Generate & Download PDF] → triggers async generation, toast "PDF generating… you'll be notified when ready"

**[Export CSV]:**
- Instant — all branches, all visible columns
- Filename: `group_benchmarking_[date].csv`

---

## 11. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Data refreshed | "Benchmarking data updated" | Info | 3s |
| PDF generating | "PDF report generating… download will start shortly" | Info | 4s |
| CSV downloaded | "CSV export downloaded" | Success | 4s |
| Radar comparison opened | "[N] branches selected for comparison" | Info | 3s |
| Too many branches selected | "Select up to 5 branches for radar comparison" | Warning | 4s |

---

## 12. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No branches | "No branches to compare" | "Add branches to your group to see benchmarking data" | [Go to Branch Overview] |
| Filter returns 0 | "No branches match" | "Try different filter settings" | [Clear Filters] |
| Radar: nothing selected | "Select 2–5 branches" | "Check the boxes next to branches you want to compare in the radar chart" | — |

---

## 13. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: controls row + table (10 rows) + chart placeholders |
| View mode switch | Full table/heatmap skeleton |
| Filter/search apply | Inline skeleton rows |
| Radar chart generate | Spinner in chart area |
| PDF generation | Spinner in export button + toast notification |

---

## 14. Role-Based UI Visibility

| Element | Chairman/MD/CEO/Pres/VP | Trustee/Advisor |
|---|---|---|
| All metric categories | ✅ | ✅ read-only |
| [Compare Selected] radar | ✅ | ✅ |
| [Export PDF] | ✅ | ✅ (Advisor) · ❌ (Trustee) |
| [Export CSV] | ✅ | ✅ (Advisor) · ❌ (Trustee) |
| Advanced Filters | ✅ | ❌ (Trustee) |
| Drill-down drawer | ✅ | ❌ (Trustee) |
| Finance columns (full) | Chairman/MD/CEO/VP | Totals only |

---

## 15. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/benchmarking/` | JWT | All branches benchmarking data |
| GET | `/api/v1/group/{id}/benchmarking/?category=academic` | JWT | Filtered by category |
| GET | `/api/v1/group/{id}/benchmarking/radar/?branches=id1,id2,id3` | JWT | Radar chart data for selected branches |
| GET | `/api/v1/group/{id}/benchmarking/heatmap/` | JWT | Heat map data |
| GET | `/api/v1/group/{id}/benchmarking/composite-score-chart/` | JWT | Bar chart data |
| GET | `/api/v1/group/{id}/benchmarking/scatter/?x=fee&y=score` | JWT | Scatter chart data |
| GET | `/api/v1/group/{id}/benchmarking/export/?format=pdf&type=full` | JWT | Export report |
| GET | `/api/v1/group/{id}/benchmarking/export/?format=csv` | JWT | Export CSV |

---

## HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| View switch (Table · Heat Map · Radar) | `click` | GET `.../benchmarking/?view=table\|heatmap\|radar` | `#benchmarking-content` | `innerHTML` |
| Branch filter (for radar comparison) | `change` | GET `.../benchmarking/?branches=&view=radar` | `#benchmarking-content` | `innerHTML` |
| Metric group toggle (column visibility) | `click` | GET `.../benchmarking/?groups=` | `#benchmarking-content` | `innerHTML` |
| Period selector | `click` | GET `.../benchmarking/?period=` | `#benchmarking-content` | `innerHTML` |
| Sort column (table view) | `click` | GET `.../benchmarking/?sort=&dir=` | `#benchmarking-table-section` | `innerHTML` |
| Correlation scatter axis change | `change` | GET `.../benchmarking/scatter/?x=&y=` | `#scatter-chart-area` | `innerHTML` |
| Export trigger | `click` | GET `.../benchmarking/export/?format=pdf\|csv` | `#export-status` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
