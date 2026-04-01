# Page 37 — Cross-Branch Admission Comparison

**URL:** `/group/adm/reports/comparison/`
**Template:** `portal_base.html`
**App:** `group_admissions`
**Django View:** `CrossBranchAdmissionComparisonView`

---

## 1. Purpose

The cross-branch admission comparison report provides a side-by-side analytical view of admission performance across every branch in the group. The primary audience is the Group Admissions Director, who uses this report to identify star branches — those with high enquiry-to-enrollment conversion rates and strong absolute enrollment numbers — and underperforming branches, characterised by high enquiry volumes but poor conversion, weak demo attendance, or wide gaps between target and actual enrollment. The comparison is the primary evidence base for resource allocation decisions: which branches require additional counsellors, which need intensified marketing support, which need a structural overhaul of their demo program or admissions process.

The report distils twelve metrics per branch into a single sortable table with intelligent row colouring to enable rapid visual triage. The Director can scan the table and immediately identify which branches are on green (at or above target), which are on yellow (within striking distance), and which are on red (materially below target and requiring intervention). The multi-metric bar chart adds a visual pipeline-shape comparison — it is immediately apparent whether a red-coded branch has a narrow enquiry funnel (marketing problem), a wide enquiry funnel but poor conversion (counselling problem), or strong conversion but low target (planning problem). These visual distinctions drive very different remediation strategies.

The year-over-year comparison section grounds the current cycle in historical context, preventing over-reaction to branches that are down slightly from an exceptional prior year, and flagging branches that appear numerically adequate but are actually in structural decline. The Outlier Analysis section uses algorithmic pattern detection to summarise the top five overachieving branches (what they have in common) and the bottom five underperforming branches (what patterns of failure are shared), distilling actionable intelligence for the Director without requiring manual analysis of the full table.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Admissions Director (Role 23) | G3 | Full — all branches, all metrics, all exports | Primary owner |
| Group CEO | G3 | View only — all branches, all metrics | Accessed via CEO dashboard |
| Group Admission Coordinator (Role 24) | G3 | View — own branch data + group aggregate totals | Cannot see peer branch counsellor-level breakdowns |
| Group Analytics Director | G3 | View only — all data | Cross-function read access |
| Group CAO | G3 | View only — all data | Academic context |
| Group Scholarship Manager (Role 27) | G3 | View only — scholarship enrollment column only | Scoped to scholarship figures |
| Branch Principal | Branch | No access | Use branch-level admission reports |

**Enforcement:** Access scoping is enforced in the Django view via `BranchAccessMixin`. Coordinators receive a queryset pre-filtered to their permitted branches; the group aggregate row is appended separately. No client-side access logic is used.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal > Admissions > Reports & Analytics > Cross-Branch Comparison
```

### 3.2 Page Header

| Element | Detail |
|---|---|
| Page title | Cross-Branch Admission Comparison |
| Subtitle | All branches · [Current cycle label] · [N] branches reporting |
| Header actions | [Filter] [Export Table CSV] [Download PDF] [Print] |
| Cycle selector | Dropdown — current cycle pre-selected |
| Comparison cycle | Optional: select a second cycle for year-over-year view |
| Last refreshed | Timestamp + [Refresh] |

### 3.3 Alert Banner

| Trigger | Message | Severity |
|---|---|---|
| More than 30% of branches below target | "[N] branches are below target enrollment. Immediate review recommended." | Critical (red) |
| Group-level enrollment more than 20% below target at this point in cycle | "Group enrollment is tracking [N]% below target for this cycle at this date. Escalation may be required." | Critical (red) |
| One or more branches have zero enrollments with cycle >50% elapsed | "[Branch names] have zero enrollments and the admission season is more than half over." | Critical (red) |
| Year-over-year comparison shows >15% group decline | "Group enrollment is down [N]% versus the same period last year." | Warning (amber) |
| Comparison data unavailable for selected second cycle | "Year-over-year comparison data is unavailable for the selected prior cycle." | Info (blue) |

---

## 4. KPI Summary Bar

Refreshes automatically via HTMX every 5 minutes (`hx-trigger="load, every 5m"`).

| Card | Metric | Source | Colour Rule | Drill-down |
|---|---|---|---|---|
| Best Performing Branch | Branch name + enrollment count | Derived: max enrolled | Neutral (blue badge) | Opens branch-detail-comparison drawer for that branch |
| Worst Performing Branch | Branch name + enrollment count | Derived: min enrolled (with ≥1 enquiry) | Neutral (red badge) | Opens branch-detail-comparison drawer for that branch |
| Avg Group Enrollment Rate | Mean of Achievement % across all branches | Derived | Green ≥90% · Yellow 70–89% · Red <70% | Opens 5.1 Branch Comparison Table sorted by Achievement % |
| Branches Above Target | Count of branches with Achievement % ≥100% | Derived | Green if >50% of branches | Opens 5.1 filtered to Above-target rows |
| Branches Below Target | Count of branches with Achievement % <75% | Derived | Red if >25% of total branches | Opens 5.1 filtered to Below-target rows |
| Widest Spread | Best branch enrollment % vs worst branch enrollment % | Derived | Red if spread >3× | Opens 5.6 Outlier Analysis |

---

## 5. Sections

### 5.1 Branch Comparison Table

Sortable, paginated table. 25 rows per page, HTMX-paginated.

| Column | Description |
|---|---|
| Branch | Branch name |
| City | City / district |
| Target Enrollment | Annual target set in Admission Season Configuration |
| Actual Enrolled | Confirmed enrollments in selected cycle |
| Achievement % | (Actual Enrolled / Target Enrollment) × 100 |
| Enquiries | Total enquiry count |
| Applications | Count at Application stage |
| Conversion Rate | (Enrolled / Enquiries) × 100 |
| Demo Conversions | Enrollments where demo attendance is recorded as first touchpoint |
| Scholarship Enrolled | Enrollments awarded scholarship |
| RTE Enrolled | Enrollments under Right to Education quota |
| NRI Enrolled | NRI category enrollments |
| Avg Days Pipeline | Mean days from first enquiry to enrollment for enrolled students |
| Action | [View Detail →] — opens branch-detail-comparison drawer |

**Sorting:** All columns sortable. Default: Achievement % descending.

**Row colour coding:**
- Green background: Achievement % ≥ 100%
- Yellow background: Achievement % 75–99%
- Red background: Achievement % < 75%

**Filters above table:**
| Filter | Options |
|---|---|
| City / District | Multi-select from available cities |
| Achievement % | All / Above target / Below target / Far below target (<50%) |
| Stream | All / MPC / BiPC / MEC / CEC / Commerce / Humanities |

**Footer row:** Group Total row pinned at bottom with aggregate values across all columns.

### 5.2 Multi-Metric Bar Chart

Grouped bar chart (Chart.js 4.x). X-axis: Branch names (abbreviated). Three bars per branch:
- Bar 1 (blue): Enquiries
- Bar 2 (orange): Applications
- Bar 3 (green): Enrolled

This chart makes the pipeline shape immediately visible per branch — a branch with a tall blue bar but short green bar has a funnel problem; a branch with all three bars at similar heights has a narrow-top funnel (awareness problem).

Toggle: [By Count] / [By Percentage] — percentage mode normalises each bar to 100% of the branch's enquiry base, making conversion ratios directly comparable regardless of branch size.

Chart is responsive; branches scroll horizontally if >15 branches. Clicking a branch bar group opens the branch-detail-comparison drawer.

### 5.3 Achievement vs Target Bullet Chart

One horizontal bullet chart per branch (Chart.js 4.x). Each chart shows:
- Thin background bar: Target enrollment
- Thick foreground bar: Actual enrolled
- Vertical marker line: 75% of target (warning threshold)

Per-branch bars stack vertically (one row per branch), sorted by Achievement % descending. Colour:
- Green bar: At or above target
- Yellow bar: 75–99% of target
- Red bar: Below 75% of target

Optional stream breakdown: toggle to show each branch bar split by stream segment colouring. This reveals whether a branch is hitting group total through one dominant stream or balanced across all streams.

### 5.4 Stream-wise Branch Heatmap

Matrix table: Rows = Branches · Columns = Streams (MPC · BiPC · MEC · CEC · Commerce · Humanities · Other).
Each cell: Enrollment count for that branch × stream combination.

Colour scale (per column, normalised):
- Dark green: Top quartile enrollment in this stream
- Medium green: Upper-middle quartile
- Light green / white: Lower-middle quartile
- Red: Zero or bottom 10% — indicates no traction in this stream at this branch

Cells with zero enrollment show "—" in red. Clicking a non-zero cell opens the branch-detail-comparison drawer filtered to that stream.

Footer row: Stream totals across all branches. Far-right column: Branch total.

### 5.5 Year-over-Year Comparison

Table with one row per branch.

| Column | Description |
|---|---|
| Branch | Branch name |
| This Year Enrolled | Current cycle enrollment count |
| Last Year Enrolled | Corresponding cycle prior year count |
| Change | Absolute difference (+ or −) |
| Change % | Percentage change with directional arrow |
| Trend | Sparkline (3-year mini line chart per branch) |

Rows sorted by Change % descending (best improvement first). Branches with no prior-year data show "—" in Last Year column with tooltip "No data for prior cycle."

Group aggregate row at bottom. Three-year sparkline uses Chart.js sparkline plugin.

### 5.6 Outlier Analysis

Two cards side by side:

**Card A — Top 5 Overachievers**
Branches ranked by Achievement % above 100%, with a bulleted summary of detected common factors:
- Counsellor: Staff ratio
- Demo-to-enrollment conversion rate
- Time in pipeline (avg days)
- Lead source mix
- Stream offering breadth
Each bullet shows the statistic for top-5 group vs group average, to make the differentiation concrete.

**Card B — Bottom 5 Underperformers**
Branches ranked by Achievement % below target, with bulleted common failure patterns detected:
- Stage bottleneck (which stage is stalling)
- Counsellor assignment gaps (enquiries unassigned)
- Demo attendance rate vs group average
- Lead source over-reliance (single source dependency)
- Year-over-year decline flag

Both cards include [View Full Detail →] link — opens the outlier-analysis-detail drawer which shows the individual branch cards with full metric tables.

---

## 6. Drawers & Modals

| ID | Width | Tabs | HTMX Endpoint |
|---|---|---|---|
| `branch-detail-comparison` | 640px | Overview · Pipeline Stages · Counsellors · Stream Breakdown · Timeline | `GET /api/v1/group/{group_id}/adm/reports/comparison/branch/{branch_id}/` |
| `outlier-analysis-detail` | 480px | Top Performers · Underperformers · Common Patterns | `GET /api/v1/group/{group_id}/adm/reports/comparison/outliers/` |

All drawers slide in from the right. Backdrop overlay dims main content. Tab content loads independently via HTMX on tab click.

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Table CSV exported | "Branch comparison data exported to CSV." | Success | 3s |
| PDF downloaded | "PDF report downloaded." | Success | 3s |
| PDF generation failed | "PDF generation failed. Please try again." | Error | 6s |
| Filter applied | "Comparison table updated with new filters." | Info | 2s |
| Refresh complete | "Branch data refreshed." | Success | 3s |
| Refresh failed (data unavailable) | "Data refresh failed. Displaying last available data." | Warning | 5s |
| No branches match filter | "No branches found matching the selected filters." | Warning | 4s |
| Drawer data load failed | "Could not load branch details. Please try again." | Error | 5s |

---

## 8. Empty States

| Condition | Illustration | Heading | Description | CTA |
|---|---|---|---|---|
| No branches have enrollment data | Building icon with dashed outline | "No Enrollment Data" | "No enrollment records exist for the selected cycle." | [Select a Different Cycle] |
| Filter returns zero branches | Filter icon with X | "No Branches Match" | "No branches match the selected city, stream, or achievement filters." | [Clear Filters] |
| Year-over-year: no prior cycle data | Calendar icon with question mark | "No Prior Cycle Data" | "Prior cycle enrollment data is not available for comparison." | [View Single Cycle] |
| Outlier analysis: fewer than 5 branches | Bar chart with partial fill | "Insufficient Data for Outlier Analysis" | "Outlier analysis requires data from at least 5 branches." | — |
| Stream heatmap: no stream data for a branch | Empty cell indicator | "No stream data" | Shown as "—" in cell with tooltip | — |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | Full-page skeleton: KPI shimmer + table row skeletons (8 rows) + chart placeholders |
| KPI bar auto-refresh (every 5m) | Per-card inline spinner; card values retained |
| Filter applied | Table body skeleton overlay; chart containers fade to 40% |
| Pagination | Table body skeleton (5 rows) while next page loads |
| Multi-metric bar chart load | Chart.js canvas shimmer placeholder |
| Bullet chart load | Row-by-row shimmer animation matching bullet chart height |
| Stream heatmap load | Matrix shimmer with column headers visible |
| Drawer open | Full drawer content skeleton with tab bar shimmer |
| Year-over-year table | Table skeleton with sparkline placeholder per row |

---

## 10. Role-Based UI Visibility

> All UI visibility decisions made server-side in Django template. No client-side JS role checks.

| UI Element | Director (23) | Coordinator (24) | CEO | Analytics Director | Scholarship Manager (27) |
|---|---|---|---|---|---|
| All branches in table | All | Own + aggregate | All | All | All (scholarship column only) |
| Achievement % colour coding | Visible | Visible | Visible | Visible | Hidden |
| Export: CSV | Visible | Visible | Visible | Visible | Hidden |
| Export: PDF | Visible | Hidden | Visible | Visible | Hidden |
| Print | Visible | Visible | Visible | Visible | Hidden |
| Branch-detail-comparison drawer | Visible | Own branch only | Visible | Visible | Hidden |
| Outlier Analysis cards | Visible | Hidden | Visible | Visible | Hidden |
| Year-over-year table | Visible | Visible | Visible | Visible | Hidden |
| Stream heatmap | Visible | Visible | Visible | Visible | Visible |
| Multi-metric bar chart toggle | Visible | Visible | Visible | Visible | Hidden |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/adm/reports/comparison/` | JWT | Full cross-branch comparison dataset |
| GET | `/api/v1/group/{group_id}/adm/reports/comparison/kpi/` | JWT | KPI summary bar data (auto-refresh) |
| GET | `/api/v1/group/{group_id}/adm/reports/comparison/table/` | JWT | Paginated branch comparison table data |
| GET | `/api/v1/group/{group_id}/adm/reports/comparison/chart/multi-metric/` | JWT | Multi-metric bar chart data |
| GET | `/api/v1/group/{group_id}/adm/reports/comparison/chart/bullet/` | JWT | Achievement vs target bullet chart data |
| GET | `/api/v1/group/{group_id}/adm/reports/comparison/heatmap/` | JWT | Stream × branch enrollment heatmap data |
| GET | `/api/v1/group/{group_id}/adm/reports/comparison/yoy/` | JWT | Year-over-year comparison table data |
| GET | `/api/v1/group/{group_id}/adm/reports/comparison/outliers/` | JWT | Outlier analysis data (top 5 + bottom 5) |
| GET | `/api/v1/group/{group_id}/adm/reports/comparison/branch/{branch_id}/` | JWT | Full branch detail for drawer |
| GET | `/api/v1/group/{group_id}/adm/reports/comparison/export/csv/` | JWT | Export table as CSV |
| GET | `/api/v1/group/{group_id}/adm/reports/comparison/export/pdf/` | JWT | Generate and stream PDF report |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| KPI bar auto-refresh | `load, every 5m` | `GET /api/v1/group/{group_id}/adm/reports/comparison/kpi/` | `#comparison-kpi-bar` | `innerHTML` |
| Apply filters | `click` on [Apply] | `GET /group/adm/reports/comparison/?city=…&achievement=…&stream=…` | `#comparison-main-content` | `innerHTML` |
| Table pagination | `click` on page control | `GET /api/v1/group/{group_id}/adm/reports/comparison/table/?page=N` | `#branch-comparison-table-body` | `innerHTML` |
| Sort column | `click` on column header | `GET /api/v1/group/{group_id}/adm/reports/comparison/table/?sort=…&dir=…` | `#branch-comparison-table-body` | `innerHTML` |
| Open branch-detail-comparison | `click` on [View Detail →] | `GET /api/v1/group/{group_id}/adm/reports/comparison/branch/{branch_id}/` | `#drawer-content` | `innerHTML` |
| Open outlier-analysis-detail | `click` on [View Full Detail →] | `GET /api/v1/group/{group_id}/adm/reports/comparison/outliers/` | `#drawer-content` | `innerHTML` |
| Drawer tab switch | `click` on tab | `GET /group/adm/reports/comparison/drawer-tab/?tab=…&id=…` | `#drawer-tab-content` | `innerHTML` |
| Refresh data manually | `click` on [Refresh] | `GET /api/v1/group/{group_id}/adm/reports/comparison/` | `#comparison-main-content` | `innerHTML` |
| Bar chart — toggle count/percentage | `change` on toggle | `GET /api/v1/group/{group_id}/adm/reports/comparison/chart/multi-metric/?mode=count\|pct` | `#multi-metric-chart-container` | `innerHTML` |
| Bullet chart — toggle stream breakdown | `click` on toggle | `GET /api/v1/group/{group_id}/adm/reports/comparison/chart/bullet/?breakdown=stream` | `#bullet-chart-container` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
