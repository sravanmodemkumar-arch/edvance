# div-a-04 — Institution Growth

## 1. Platform Scale Reference

| Dimension | Value |
|---|---|
| Total institutions | 2,050 |
| Schools | 1,000 · avg 1,000 students · max 5,000 |
| Colleges (Intermediate) | 800 · avg 500 · max 2,000 |
| Institution Groups | 150 · each owns 5–50 child institutions |
| Coaching Centres | 100 · avg 10,000 members · max 15,000 |
| Total students | 2.4M–7.6M |
| Indian states covered | 28 states + 8 UTs |
| New institutions/month (current velocity) | ~30–50 |
| Churn rate (annual) | ~4% (≈ 82 institutions/yr) |
| ARR from coaching centres | ₹15 Cr (highest revenue segment) |

**Why this matters:** Growth is the COO's north star metric. At 2,050 institutions and ₹XX Cr ARR, the board wants to see net new logo velocity, regional penetration maps, cohort retention curves, and pipeline health on one page — not 4 separate reports. This page replaces the quarterly Excel deck.

---

## 2. Page Metadata

| Field | Value |
|---|---|
| Page title | Institution Growth |
| Route | `/exec/institution-growth/` |
| Django view | `InstitutionGrowthView` |
| Template | `exec/institution_growth.html` |
| Priority | P1 |
| Nav group | Analytics |
| Required role | `exec`, `superadmin` |
| 2FA required | No |
| HTMX poll | Stats strip: every 60s; Map: manual refresh only |

---

## 3. Wireframe

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ HEADER: Institution Growth              [Export PDF] [Export CSV] [Share ▾]  │
├──────────┬──────────┬──────────┬──────────┬──────────┬──────────────────────┤
│ Total    │ Net New  │ MoM      │ Churn    │ Pipeline │ Penetration          │
│ Active   │ (30d)    │ Growth % │ (30d)    │ (Qualified)│ Score              │
│ 2,050    │  +38     │ +1.9%    │   -4     │   127    │  62 / 100            │
├──────────┴──────────┴──────────┴──────────┴──────────┴──────────────────────┤
│ TABS: [Growth Trend] [Geographic Map] [Cohort Retention] [Pipeline] [Churn] │
├──────────────────────────────────────────────────────────────────────────────┤
│ TAB: GROWTH TREND                                                            │
│ [Date Range ▾] [Institution Type ▾] [State ▾] [Plan Tier ▾]  [Apply]       │
│                                                                              │
│  Monthly Net New Institutions — Stacked Bar (12 months)                     │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │  ▓▓▒▒░░   School ▓  College ▒  Coaching ░  Group                      │  │
│  │  50 ┤ ██▓▓ ▒▒░ ██▓▓ ▒▒░ ██▓▓ ▒▒░                                      │  │
│  │  25 ┤                                                                   │  │
│  │   0 ┼─────────────────────────────────── months                        │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  Cumulative Growth Line (secondary Y-axis)                                  │
│  YoY comparison toggle [On/Off]                                              │
├──────────────────────────────────────────────────────────────────────────────┤
│ GROWTH TABLE: Top Gaining / Top Churning this month                          │
│ Institution │ Type │ State │ Plan │ Students │ Joined/Churned │ ARR Impact  │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Sections — Deep Specification

### 4.1 KPI Strip

**Container:** `flex gap-4 p-4` · 6 cards · `bg-[#0D1526] rounded-xl border border-[#1E2D4A]`
**Poll:** `hx-trigger="every 60s[!document.querySelector('.drawer-open,.modal-open')]"` on strip wrapper
**Height:** 88px per card · `min-w-[140px]`

| # | Card | Value format | Delta | Alert threshold |
|---|---|---|---|---|
| 1 | Total Active | `2,050` | +38 MoM (green ↑) | — |
| 2 | Net New (30d) | `+38` | vs prev 30d | < 20 = amber |
| 3 | MoM Growth % | `+1.9%` | vs prev month | < 0.5% = amber |
| 4 | Churn (30d) | `4` | vs prev 30d | > 10 = red |
| 5 | Pipeline (Qualified) | `127` | — | — |
| 6 | Penetration Score | `62 / 100` sparkline | — | < 50 = amber |

**Count-up animation:** `data-count-up` attribute on value span · runs once on first load via `requestAnimationFrame` · 600ms duration · easing: `t*(2-t)` · does NOT replay on HTMX poll refreshes (guarded by `data-animated="true"` flag)

**Delta chip:** `text-xs px-1.5 py-0.5 rounded-full` · green: `bg-[#064E3B] text-[#34D399]` · red: `bg-[#450A0A] text-[#F87171]` · amber: `bg-[#451A03] text-[#FCD34D]`

---

### 4.2 Tab Bar

**Container:** `flex border-b border-[#1E2D4A] px-6`
**Tab item:** `px-4 py-3 text-sm font-medium cursor-pointer` · inactive: `text-[#94A3B8]` · active: `text-white border-b-2 border-[#6366F1]`
**Tabs:** Growth Trend · Geographic Map · Cohort Retention · Pipeline · Churn Risk
**HTMX:** `hx-get="?part={tab_id}" hx-target="#tab-content" hx-swap="innerHTML" hx-push-url="false"`
**Loading state:** `#tab-content` shows 3 skeleton rows `animate-pulse bg-[#1E2D4A] h-8 rounded mb-2` while loading

---

### 4.3 Tab: Growth Trend

#### 4.3.1 Toolbar

`flex flex-wrap gap-3 p-4 bg-[#0D1526] rounded-xl border border-[#1E2D4A] mb-4`

| Control | Type | Options | Width |
|---|---|---|---|
| Date Range | Dropdown + custom picker | Last 3M / 6M / 12M / 24M / Custom | 160px |
| Institution Type | Multi-select dropdown | All / School / College / Coaching / Group | 180px |
| State | Searchable multi-select | 28 states + All | 200px |
| Plan Tier | Multi-select | Starter / Standard / Professional / Enterprise | 200px |
| [Apply] | Button | `bg-[#6366F1] text-white px-4 py-2 rounded-lg` | auto |
| [Reset] | Ghost button | `text-[#94A3B8] hover:text-white` | auto |

**Active filter chips:** below toolbar · `flex flex-wrap gap-2` · each chip: `text-xs bg-[#1E2D4A] text-[#94A3B8] px-2 py-1 rounded-full` with `×` remove button · "Clear all" link when ≥ 2 chips

#### 4.3.2 Monthly Net New — Stacked Bar Chart

**Library:** Chart.js 4.4.2
**Canvas id:** `growth-bar-chart` · height 280px
**Destroy-before-recreate:** `if (window._charts?.growthBar) { window._charts.growthBar.destroy(); }`

**Dataset series:**

| Series | Colour | Stack key |
|---|---|---|
| Schools (new) | `#6366F1` | `stack0` |
| Colleges (new) | `#22D3EE` | `stack0` |
| Coaching (new) | `#F59E0B` | `stack0` |
| Groups (new) | `#10B981` | `stack0` |
| Churned (negative) | `#EF4444` (below zero) | `stack1` |

**X-axis:** month labels `MMM 'YY` · `color: '#64748B'`
**Y-axis left:** count · `color: '#64748B'` · grid: `#1E2D4A`
**Y-axis right:** cumulative total · `color: '#94A3B8'` · type: `linear`
**YoY comparison:** toggle switch `YoY [On/Off]` · adds dashed line series `borderDash: [5,5]` `borderColor: '#475569'`
**Tooltip:** custom HTML tooltip showing: month label, breakdown per type, net = new − churned, cumulative total
**Click on bar:** `onClick` handler → sets Institution Type filter to clicked segment → `htmx.trigger('#growth-table', 'filter-change')`

#### 4.3.3 Growth Table

`id="growth-table"` · `hx-get="?part=growth_table"` · `hx-trigger="filter-change"` · `hx-swap="innerHTML"`

**Two sub-tabs:** [Top Gaining] [Top Churning] — toggle with `hx-get="?part=growth_table&mode={gaining|churning}"`

| Column | Detail |
|---|---|
| # | Row number |
| Institution | Name + type icon (16px SVG) |
| Type | Badge pill |
| State | State name |
| Plan | Plan badge |
| Students | Current count |
| Joined / Churned | Date relative |
| ARR Impact | `+₹X.XX L` green or `-₹X.XX L` red |
| Actions ⋯ | View Detail → opens drawer; View in List → links to div-a-05 |

**Pagination:** 10 rows · `?page=N` · "Showing X–Y of Z"

---

### 4.4 Tab: Geographic Map

**Container:** `relative w-full h-[520px] bg-[#0D1526] rounded-xl border border-[#1E2D4A]`
**Map library:** SVG India state map rendered inline (no external dependency) · states coloured by institution count
**Colour scale:** `#1E2D4A` (0) → `#312E81` (low) → `#6366F1` (mid) → `#A5B4FC` (high) using 5-step linear interpolation

**Choropleth metric selector:** top-right of map `select.bg-[#131F38]`:
- Total institutions
- New this quarter
- Penetration score
- Churn rate

**State hover tooltip:** `absolute z-50 bg-[#0D1526] border border-[#1E2D4A] rounded-lg p-3 text-sm shadow-xl`
Content: State name · Total institutions · Breakdown by type · Top district

**State click:** opens State Drill-Down Drawer (480px) — see §6.1

**Legend:** bottom-left · `flex gap-3 text-xs text-[#94A3B8]` · colour squares + labels

**Refresh button:** `[↻ Refresh Map]` top-right · `hx-get="?part=map" hx-swap="outerHTML hx-target="#map-container"` · map does NOT auto-poll (data is expensive; 1-min stale acceptable)

**District-level zoom toggle:** [State view] [District view] · district view shows dot markers (SVG circle `r=4`) sized by institution count

---

### 4.5 Tab: Cohort Retention

**Purpose:** For each cohort (month of onboarding), show % still active at M+1, M+3, M+6, M+12.

#### 4.5.1 Cohort Selector

`flex gap-3 items-center p-4`
- Cohort group by: [Monthly] [Quarterly] [Annual]
- Institution Type: same multi-select as §4.3.1
- Start cohort / End cohort: month picker

#### 4.5.2 Retention Heatmap Table

`id="cohort-heatmap"` · `hx-get="?part=cohort"`

**Rows:** each cohort (e.g., "Jan 2024") = one row
**Columns:** M+0 (100%), M+1, M+3, M+6, M+12
**Cell background:** heatmap — 100% = `bg-[#064E3B]` · 90–99% = `bg-[#065F46]` · 75–89% = `bg-[#047857]` · 50–74% = `bg-[#D97706]` · < 50% = `bg-[#991B1B]`
**Cell text:** `text-sm font-mono text-white`
**Click on cell:** opens Cohort Cell Drawer (see §6.2) showing which institutions in that cohort/month are still active vs churned

#### 4.5.3 Retention Line Chart (below heatmap)

Shows overlay of multiple cohort lines on single chart
**X-axis:** months since onboarding (0–12)
**Y-axis:** retention % (0–100)
**Each line:** one cohort · hover: tooltip with cohort name + % at that month
**Benchmark line:** dashed `#475569` at platform average retention

---

### 4.6 Tab: Pipeline

**Purpose:** Institutions in sales pipeline (CRM data pulled via nightly sync). Visibility into what's coming into the funnel.

#### 4.6.1 Funnel Chart

`id="pipeline-funnel"` · Canvas height 200px
**Stages:** Prospect → Demo Scheduled → Trial → Proposal Sent → Closed Won / Closed Lost
**Colour:** `#6366F1` with decreasing opacity per stage
**Hover:** tooltip with count + conversion rate from prev stage

#### 4.6.2 Pipeline Table

| Column | Detail |
|---|---|
| Institution | Name + type |
| Stage | Stage badge |
| Owner | Sales rep name |
| Expected ARR | `₹X.XX L` |
| Expected close | Date |
| Days in stage | Number + amber if > 14d |
| Actions ⋯ | View CRM, Convert to Active, Archive |

**Filters:** Stage multi-select · Owner dropdown · Expected close date range
**Sort:** Expected ARR desc by default

---

### 4.7 Tab: Churn Risk

**Purpose:** Early warning — institutions likely to churn in next 90 days. Score = composite of: exam frequency decline, login frequency decline, overdue invoices, support tickets, NPS.

#### 4.7.1 Risk Score Distribution

Horizontal bar chart (5 buckets):
- 80–100: Critical (red) · 60–79: High (orange) · 40–59: Medium (amber) · 20–39: Low (green) · 0–19: Safe (grey)
Click bucket → filters churn table

#### 4.7.2 Churn Risk Table

`id="churn-table"` · `hx-get="?part=churn"` · `hx-trigger="load, filter-change"`

| Column | Detail |
|---|---|
| Institution | Name + type icon |
| Risk Score | 0–100 · coloured badge |
| ARR at Risk | `₹X.XX L` |
| Last Exam | Relative date · red if > 30 days |
| Last Login | Relative date |
| Overdue Invoice | `₹X.XX L` or `—` |
| Trend | 7-day sparkline of risk score |
| Actions ⋯ | Open Detail Drawer, Flag for CS, Send Re-engagement |

**Sort:** Risk score desc by default
**Pagination:** 25/page

---

## 5. Drawers

### 5.1 State Drill-Down Drawer (480 px)

`id="state-drawer"` · slides in from right · `transition-transform duration-300`
`body.drawer-open` class added on open · removed on close

**Header:** State name + State code + `[×]` close · `bg-[#0D1526] border-b border-[#1E2D4A] px-6 py-4`

**Section A — Summary:**
- Total institutions · New this quarter · Churn this quarter · Net growth
- Penetration score (vs national average)

**Section B — Breakdown by type:** Horizontal stacked bar · Schools / Colleges / Coaching / Groups

**Section C — Top districts table:**
| District | Institutions | Students | Top institution |
- 10 rows · expandable

**Section D — Growth trend (12 months):** Small area chart 200px height · `#6366F1` fill

**Footer:** [View Institutions in this State] → links to div-a-05 with state filter pre-applied · [Close]

---

### 5.2 Cohort Cell Drawer (480 px)

**Header:** "Cohort {MMM YYYY} — {month} retention"

**Section A — Active institutions (still retained):**
Table: Name · Type · Plan · Students · ARR

**Section B — Churned institutions in this period:**
Table: Name · Type · Churn date · ARR lost · Reason (if recorded)

**Footer:** [Export] [Close]

---

### 5.3 Institution Growth Drawer (560 px)

Opened from growth table row Actions ⋯ → "View Detail"

**Header:** Institution name + type badge + status badge + `[×]`

**Tab bar (3 tabs):**

**Tab A — Growth Profile:**
- Joined date · Plan · State · District
- Student count history: line chart (last 12 months)
- Exam count history: line chart (last 12 months)
- ARR history: line chart (last 12 months)

**Tab B — Churn Risk:**
- Risk score gauge (0–100) · Breakdown by factor:
  | Factor | Score | Weight | Contribution |
  | Exam frequency | 72 | 30% | 21.6 |
  | Login frequency | 85 | 20% | 17.0 |
  | Invoice status | 100 | 25% | 25.0 |
  | Support tickets | 60 | 15% | 9.0 |
  | NPS | 70 | 10% | 7.0 |
  | **Total** | | | **79.6** |
- Risk trend sparkline (30 days)

**Tab C — Pipeline / Expansion:**
- Current plan + recommended upsell
- Usage vs plan limits (progress bars)
- Expansion signals: student count growth, feature adoption, API usage

**Footer:** [View Full Profile →] (links to div-a-06) · [Flag for CS] · [Close]

---

## 6. Modals

### 6.1 Export Modal (480 px)

Trigger: [Export PDF] or [Export CSV] header buttons

**Fields:**
- Format: PDF / CSV / XLSX
- Include sections: checkboxes (Growth Trend / Geographic / Cohort / Pipeline / Churn)
- Date range (pre-filled from current filter)
- Recipient email (optional — for scheduled exports)

**Footer:** [Cancel] [Generate Report]

---

## 7. HTMX Architecture

| Part param | Template | Trigger |
|---|---|---|
| `?part=kpi` | `exec/partials/growth_kpi.html` | Page load · poll every 60s |
| `?part=growth_trend` | `exec/partials/growth_trend.html` | Tab click · filter apply |
| `?part=growth_table` | `exec/partials/growth_table.html` | Filter change · tab load |
| `?part=map` | `exec/partials/growth_map.html` | Tab click · manual refresh |
| `?part=cohort` | `exec/partials/growth_cohort.html` | Tab click · filter change |
| `?part=pipeline` | `exec/partials/growth_pipeline.html` | Tab click |
| `?part=churn` | `exec/partials/growth_churn.html` | Tab click · filter change |
| `?part=state_drawer&state={code}` | `exec/partials/state_drawer.html` | Map state click |
| `?part=cohort_drawer&cohort={id}&month={n}` | `exec/partials/cohort_drawer.html` | Heatmap cell click |

**Django view dispatch:**
```python
class InstitutionGrowthView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "portal.view_exec_analytics"

    def get(self, request):
        ctx = self._build_context(request)
        if _is_htmx(request):
            part = request.GET.get("part", "")
            templates = {
                "kpi": "exec/partials/growth_kpi.html",
                "growth_trend": "exec/partials/growth_trend.html",
                "growth_table": "exec/partials/growth_table.html",
                "map": "exec/partials/growth_map.html",
                "cohort": "exec/partials/growth_cohort.html",
                "pipeline": "exec/partials/growth_pipeline.html",
                "churn": "exec/partials/growth_churn.html",
                "state_drawer": "exec/partials/state_drawer.html",
                "cohort_drawer": "exec/partials/cohort_drawer.html",
            }
            if part in templates:
                return render(request, templates[part], ctx)
        return render(request, "exec/institution_growth.html", ctx)

    def _build_context(self, request):
        # All aggregates from Redis cache (TTL 60s)
        return {
            "kpi": growth_kpi_from_cache(),
            "filters": extract_filters(request.GET),
        }
```

**Poll pause pattern:**
```html
<div id="growth-kpi-strip"
     hx-get="/exec/institution-growth/?part=kpi"
     hx-trigger="every 60s[!document.querySelector('.drawer-open,.modal-open')]"
     hx-swap="innerHTML">
```

---

## 8. Performance Requirements

| Metric | Target | Critical |
|---|---|---|
| KPI strip initial | < 300 ms | > 800 ms |
| Growth trend chart | < 600 ms | > 1.5 s |
| Geographic map render | < 800 ms | > 2 s |
| Cohort heatmap | < 500 ms | > 1.2 s |
| Pipeline tab | < 400 ms | > 1 s |
| Churn risk table | < 400 ms | > 1 s |
| State drawer | < 300 ms | > 800 ms |
| Full page initial load | < 1.2 s | > 3 s |

---

## 9. States & Edge Cases

| State | Behaviour |
|---|---|
| No data for selected filters | Empty state: illustration + "No institutions match your filters" + [Clear filters] |
| Single institution type selected | Other stacks hidden from bar chart; Y-axis rescales |
| State with 0 institutions | State choropleth = `#1E2D4A` (empty colour); tooltip shows "No institutions" |
| Pipeline tab: CRM sync failed | Amber banner "Pipeline data last synced {X} hours ago — may be stale" |
| Churn table: all green (no at-risk) | Green success state: "No institutions at elevated churn risk" |
| Export: large date range (> 12 months) | "Generating report — you'll receive an email when ready" toast |
| Cohort retention < 50% in any cell | Red cell + tooltip "High churn — click for details" |
| Map district view: > 500 districts visible | Cluster dots for districts with < 3 institutions |

---

## 10. Keyboard Shortcuts

| Key | Action |
|---|---|
| `1`–`5` | Switch tabs (Growth / Map / Cohort / Pipeline / Churn) |
| `F` | Focus filter toolbar |
| `R` | Refresh current tab |
| `E` | Open export modal |
| `Esc` | Close drawer/modal |
| `↑` / `↓` | Navigate table rows |
| `Enter` | Open drawer for focused row |
| `?` | Keyboard shortcut help overlay |

---

## 11. Template Files

| File | Purpose |
|---|---|
| `exec/institution_growth.html` | Full page shell |
| `exec/partials/growth_kpi.html` | KPI strip (6 cards) |
| `exec/partials/growth_trend.html` | Stacked bar + YoY line chart |
| `exec/partials/growth_table.html` | Top gaining/churning table |
| `exec/partials/growth_map.html` | SVG choropleth map |
| `exec/partials/growth_cohort.html` | Heatmap + retention lines |
| `exec/partials/growth_pipeline.html` | Funnel + pipeline table |
| `exec/partials/growth_churn.html` | Risk distribution + churn table |
| `exec/partials/state_drawer.html` | State drill-down drawer |
| `exec/partials/cohort_drawer.html` | Cohort cell detail drawer |
| `exec/partials/growth_institution_drawer.html` | Institution growth drawer |

---

## 12. Component References

| Component | Used in |
|---|---|
| `KpiCard` | §4.1 |
| `TabBar` | §4.2 |
| `StackedBarChart` | §4.3.2 |
| `GrowthTable` | §4.3.3 |
| `IndiaChoroMap` | §4.4 |
| `CohortHeatmap` | §4.5.2 |
| `RetentionLineChart` | §4.5.3 |
| `FunnelChart` | §4.6.1 |
| `PipelineTable` | §4.6.2 |
| `RiskGauge` | §4.7.1 + §5.3 Tab B |
| `ChurnRiskTable` | §4.7.2 |
| `DrawerPanel` | §5.1–§5.3 |
| `ModalDialog` | §6.1 |
| `FilterChip` | §4.3.1 |
| `SearchFilterBar` | All toolbars |
| `PaginationStrip` | All tables |
| `SparklineChart` | Churn table trend column |
| `PollableContainer` | KPI strip |
