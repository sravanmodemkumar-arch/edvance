# O-37 — Branch Marketing Comparison

> **URL:** `/group/marketing/analytics/branch-comparison/`
> **File:** `o-37-branch-marketing-comparison.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Role:** Group Admission Data Analyst (Role 132, G1) — primary operator

---

## 1. Purpose

The Branch Marketing Comparison page is the CEO's branch-level marketing accountability tool — it answers "which of my 30 branches are wasting marketing money and which branches deserve more?" In the Indian education group model, marketing budgets are typically allocated to branches using one of three flawed methods: equal split (every branch gets ₹15L regardless of size or market), proportional to seat capacity (bigger branch = bigger budget, ignoring local competition), or historical precedent (same as last year ± 10%). None of these methods account for the massive variation in marketing efficiency across branches. A branch in Dilsukhnagar (Hyderabad) with 5 competitor schools within 2 km needs ₹25L and aggressive digital marketing to fill 85% seats, while a branch in Siddipet (semi-urban) fills 95% seats with ₹4L of local newspaper ads and word-of-mouth. This page makes that variation visible, measurable, and actionable.

The problems this page solves:

1. **Hidden marketing inefficiency across branches:** In a 30-branch group, the difference in Cost-Per-Admission between the most efficient and least efficient branch is typically 5x to 10x. The Kukatpally branch spends ₹28L to get 1,200 admissions (CPA ₹2,333), while the Mehdipatnam branch spends ₹22L to get 350 admissions (CPA ₹6,286). Without branch comparison, these numbers are invisible — each branch Principal reports "we did well" and the Campaign Manager reports aggregate numbers that mask branch-level failures. This page ranks every branch by marketing efficiency, exposing underperformers who consume disproportionate budget relative to results.

2. **Metro vs tier-2 vs small-town budget mismatch:** Indian education groups span multiple city tiers within a single state. A Narayana or Sri Chaitanya group has branches in Hyderabad (metro), Warangal (tier-2), Nalgonda (tier-3), and Suryapet (small town). Marketing dynamics are fundamentally different: Hyderabad requires digital ads + newspaper + outdoor + open days costing ₹30-50L per branch; Warangal needs newspaper + WhatsApp costing ₹8-15L; Suryapet needs only word-of-mouth + local posters costing ₹2-5L. Groups that apply uniform budgets either overspend in small towns (zero ROI on unread newspaper ads) or underspend in metros (losing competitive students to rival groups). This page provides tier-adjusted efficiency metrics.

3. **Fill rate vs marketing spend disconnect:** A branch Principal claims "we need more marketing budget" when seat fill rate is 65%. But the data might show this branch already has the second-highest marketing spend in the group — the problem is not budget but poor conversion (leads generated but not converted due to infrastructure, faculty, or location issues). Conversely, a branch with 92% fill rate and ₹3L spend might achieve 97% with ₹5L more investment. The spend-vs-fill scatter analysis reveals whether the solution is "more money" or "better execution."

4. **Peer comparison for branch accountability:** Branch Principals respond to peer pressure more than top-down mandates. When the Kukatpally branch Principal sees that the Kompally branch (similar size, similar catchment) achieves ₹2,100 CPA while their own branch is at ₹3,800, they investigate why. This page enables peer-group comparison — branches grouped by size, tier, board, and catchment characteristics — so that comparisons are fair and actionable.

5. **Budget adequacy assessment:** Some branches are underfunded relative to their potential. A branch in a new residential area (Tellapur, Kollur) has 2,000 seat capacity but only ₹8L marketing budget — resulting in 55% fill rate. The branch needs ₹20L to penetrate the catchment. The budget adequacy model compares: current spend per seat, fill rate, local competition density, and catchment population — recommending whether a branch needs 50% more budget, 20% less, or a completely different channel mix.

**Scale:** 150 groups × 5-50 branches per group · Branch-level data: seat capacity, admissions, fill %, marketing spend, leads, CPL, CPA, ROI · Peer groups: by size (small/medium/large), by tier (metro/tier-2/tier-3/rural), by board (CBSE/ICSE/State)

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Admission Data Analyst | 132 | G1 | Read + Export — view all branch comparisons, run assessments, export | Primary operator |
| Group Admissions Campaign Manager | 119 | G3 | Read — view branch rankings to inform budget allocation decisions | Works with Data Analyst on budget reallocation |
| Group Topper Relations Manager | 120 | G3 | No access | Branch marketing comparison not relevant to topper role |
| Group Admission Telecaller Executive | 130 | G3 | No access | Branch comparison not relevant to telecalling |
| Group Campaign Content Coordinator | 131 | G2 | No access | Content role, no analytics function |
| Group CEO / Chairman | — | G4/G5 | Read + Export — full access, primary consumer of branch rankings | Uses for board meetings and budget approvals |
| Branch Principal | — | G3 | Read (own branch + peer group) — view own branch metrics and anonymous peer comparison | Can see own branch rank but not other branches' raw numbers |

> **Access enforcement:** `@require_role(min_level=G1, division='O')`. Export: role 132 or G4+. Branch Principals: `WHERE branch_id = user.branch_id` for own data; peer comparison shows anonymised "Branch A, Branch B" labels for other branches. Full branch name visibility: role 132, 119, or G4+ only. Budget recommendation visibility: G4+ only (sensitive reallocation data).

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  >  Marketing & Campaigns  >  Analytics & Reports  >  Branch Marketing Comparison
```

### 3.2 Page Header
```
Branch Marketing Comparison                         [Season: v]  [Peer Group: v]  [Export v]  [Print League Table]
Data Analyst — Priya Raghunandan
Sunrise Education Group · Season 2025-26 · 28 branches · ₹4.82 Cr total spend · Avg Efficiency: 72/100 · Most Efficient: Kompally (94) · Least: Mehdipatnam (38)
```

---

## 4. KPI Summary Bar (6 cards)

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Total Branches | Integer | COUNT(branches) WHERE has_marketing_data = true AND season = selected | Static blue | `#kpi-branches` |
| 2 | Avg Marketing Efficiency | Score (0-100) | AVG(efficiency_score) across all branches | Green ≥ 70, Amber 50-69, Red < 50 | `#kpi-avg-eff` |
| 3 | Most Efficient Branch | Text + Score | Branch with MAX(efficiency_score) — e.g., "Kompally (94)" | Static green | `#kpi-best` |
| 4 | Least Efficient Branch | Text + Score | Branch with MIN(efficiency_score) — e.g., "Mehdipatnam (38)" | Static red | `#kpi-worst` |
| 5 | Branches Above Target | Ratio (N/M) | COUNT(branches WHERE fill_rate ≥ target_fill_rate) / total branches | Green ≥ 80%, Amber 60-79%, Red < 60% | `#kpi-above-target` |
| 6 | Budget Utilisation % | Percentage | SUM(actual_spend) / SUM(allocated_budget) × 100 across all branches | Green 85-100%, Amber 70-84% or > 100%, Red < 70% or > 115% | `#kpi-budget-util` |

**Efficiency Score calculation (composite, 0-100):**
- Fill Rate Achievement (30%): (Actual Fill Rate / Target Fill Rate) × 30, capped at 30
- Cost Efficiency (30%): (Median Group CPA / Branch CPA) × 30, capped at 30 — lower CPA = higher score
- Target Achievement (20%): (Actual Admissions / Target Admissions) × 20, capped at 20
- Budget Discipline (10%): 10 if actual spend within ±10% of budget, 5 if ±20%, 0 if > ±20%
- Lead Quality (10%): (Branch Conversion Rate / Group Avg Conversion Rate) × 10, capped at 10

**HTMX:** `hx-get="/api/v1/group/{id}/marketing/analytics/branch-comparison/kpis/"` → `hx-trigger="load"`

---

## 5. Sections

### 5.1 Tab Navigation

Four tabs:
1. **Branch League Table** — Ranked table of all branches by marketing efficiency
2. **Peer Comparison** — Branches grouped by tier/size with intra-group comparison
3. **Budget Adequacy** — Assessment of whether each branch's budget matches its potential
4. **Trend by Branch** — Season-over-season efficiency trend per branch

### 5.2 Tab 1: Branch League Table

**Filter bar:** Zone · Branch tier (Metro/Tier-2/Tier-3/Rural) · Branch size (Small/Medium/Large) · Board (CBSE/ICSE/State) · Performance tier (Star/On Track/Needs Attention/Critical) · Sort by (Efficiency Score/Fill Rate/CPA/ROI)

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Rank | Integer | Yes | Overall rank by efficiency score (1 = best) |
| Movement | Arrow icon | No | Rank change vs previous season: ↑ green (improved), ↓ red (declined), → grey (same) |
| Branch Name | Text (link) | Yes | Click opens branch deep-dive drawer |
| City / Tier | Text + Badge | Yes | "Hyderabad (Metro)" / "Warangal (Tier-2)" / "Siddipet (Tier-3)" |
| Board | Badge | Yes | CBSE / ICSE / State / IB |
| Seat Capacity | Integer | Yes | Total seats available |
| Admissions | Integer | Yes | Confirmed enrollments |
| Fill Rate % | Progress bar | Yes | (Admissions / Capacity) × 100; green ≥ 90%, amber 70-89%, red < 70% |
| Target Achievement % | Percentage | Yes | (Admissions / Target) × 100 |
| Marketing Spend (₹) | Amount | Yes | Total marketing spend for branch |
| Spend per Seat (₹) | Amount | Yes | Marketing spend / Seat capacity |
| Total Leads | Integer | Yes | Leads attributed to this branch |
| CPL (₹) | Amount | Yes | Branch spend / Branch leads |
| CPA (₹) | Amount | Yes | Branch spend / Branch admissions |
| ROI | Ratio | Yes | Branch admission revenue / Branch marketing spend |
| Efficiency Score | Score bar (0-100) | Yes | Composite score with colour fill: green ≥ 80, amber 50-79, red < 50 |
| Performance Tier | Badge | Yes | Star (green) / On Track (blue) / Needs Attention (amber) / Critical (red) |
| Actions | Buttons | No | [Deep Dive] [Peer Compare] |

**Default sort:** Efficiency Score DESC (league table format)
**Pagination:** Server-side · 30/page (typically all branches fit on 1 page)

**Performance tier classification:**
- **Star** (green): Efficiency Score ≥ 80 AND Fill Rate ≥ 90% — branch excels at marketing efficiency
- **On Track** (blue): Efficiency Score 60-79 AND Fill Rate ≥ 75% — performing adequately
- **Needs Attention** (amber): Efficiency Score 40-59 OR Fill Rate 60-74% — investigate and intervene
- **Critical** (red): Efficiency Score < 40 OR Fill Rate < 60% — urgent CEO attention required

**Conditional formatting:**
- CPA cell: Red background if > 2× group median CPA
- Fill Rate: Red pulse animation if < 50% and season > 60% elapsed
- Spend per Seat: Red if > ₹2,000 and fill rate < 70% (spending heavily with poor results)

### 5.3 Tab 2: Peer Comparison

**Purpose:** Compare branches within fair peer groups rather than across the entire group.

**Peer group selector:** Auto-grouped by tier + size OR manual selection (pick 3-8 branches)

**Auto peer groups (example):**
- Metro Large (Kukatpally, Ameerpet, Dilsukhnagar — Hyderabad, 1000+ seats each)
- Metro Medium (Tarnaka, Nacharam, Musheerabad — Hyderabad, 500-999 seats)
- Tier-2 Large (Warangal, Karimnagar, Nizamabad — 800+ seats)
- Tier-3 (Siddipet, Nalgonda, Suryapet — under 500 seats)

**Peer comparison table:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Branch | Text | Yes | — |
| Peer Group | Badge | Yes | Auto-assigned tier + size group |
| Fill Rate % | Percentage | Yes | — |
| CPA (₹) | Amount | Yes | — |
| ROI | Ratio | Yes | — |
| Efficiency Score | Score | Yes | — |
| Peer Avg CPA | Amount | No | Average CPA of peer group (excluding this branch) |
| CPA vs Peer | Badge | Yes | "Below Peer Avg" (green) / "At Peer Avg" (blue) / "Above Peer Avg" (red) |
| Peer Rank | Integer | Yes | Rank within peer group |
| Gap to Best | Amount | No | CPA difference to best-performing peer — "₹1,200 above peer leader" |
| Potential Savings (₹) | Amount | Yes | If branch matched peer avg CPA: (Branch CPA - Peer Avg CPA) × Branch Admissions |

**Summary box per peer group:**

```
Metro Large (4 branches) — Avg CPA: ₹3,200 · Avg Fill: 88% · Best: Kompally · Worst: Dilsukhnagar
Peer spread: CPA ranges from ₹2,100 to ₹5,800 (2.8x variation)
If all matched peer average: ₹12.4L potential savings
```

### 5.4 Tab 3: Budget Adequacy

**Purpose:** Determine whether each branch is over-funded, under-funded, or adequately funded relative to its potential.

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Branch | Text | Yes | — |
| Tier | Badge | Yes | Metro / Tier-2 / Tier-3 / Rural |
| Current Budget (₹) | Amount | Yes | Allocated marketing budget |
| Current Spend (₹) | Amount | Yes | Actual spend to date |
| Seat Capacity | Integer | Yes | — |
| Fill Rate % | Percentage | Yes | Current fill rate |
| Competition Density | Badge | Yes | High (> 5 competitors in 3 km) / Medium (2-5) / Low (0-1) |
| Catchment Population | Integer | Yes | Estimated school-age population in catchment area (from O-27) |
| Market Penetration % | Percentage | Yes | Branch admissions / Catchment school-age population × 100 |
| Budget Adequacy | Badge | Yes | Over-funded (red) / Adequate (green) / Under-funded (amber) / Severely Under-funded (red) |
| Recommended Budget (₹) | Amount | Yes | Model-based recommendation |
| Delta (₹) | Amount | Yes | Recommended - Current; positive = needs more, negative = excess |
| Expected Impact | Text | No | "₹5L more → projected +120 admissions, fill rate 72% → 82%" |

**Budget adequacy model logic:**
- **Over-funded:** Spend per admission > 2× tier average AND fill rate ≥ 90% — branch fills organically, marketing spend is wasted
- **Adequate:** Spend per admission within ±30% of tier average AND fill rate ≥ 80%
- **Under-funded:** Fill rate < 80% AND competition density = High AND spend per seat < tier median
- **Severely Under-funded:** Fill rate < 60% AND catchment potential ≥ 2× current admissions AND current budget < 50% of recommended

**Indian context:**
- Metro branch benchmark: ₹800-₹1,500 spend per seat, target fill ≥ 85%
- Tier-2 branch benchmark: ₹300-₹700 spend per seat, target fill ≥ 90%
- Tier-3/Rural branch benchmark: ₹100-₹300 spend per seat, target fill ≥ 92%
- New branch (< 3 years old): 2x benchmark spend expected until brand established

### 5.5 Tab 4: Trend by Branch

**Branch selector:** Dropdown or multi-select (up to 8 branches for comparison)
**Metric selector:** Fill Rate / CPA / ROI / Efficiency Score / Total Spend / Total Admissions

**Trend table (per branch, across seasons):**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Branch | Text | Yes | — |
| Metric 2022-23 | Amount/% | Yes | — |
| Metric 2023-24 | Amount/% | Yes | — |
| Metric 2024-25 | Amount/% | Yes | — |
| Metric 2025-26 | Amount/% | Yes | Current season |
| 3-Year CAGR | Percentage | Yes | Compound annual growth rate of selected metric |
| Direction | Badge | No | "Improving" (green) / "Stable" (blue) / "Declining" (red) |
| Trend | Sparkline | No | Mini line chart across seasons |

**Direction logic:**
- **Improving:** CAGR favourable (CPL/CPA decreasing or Fill Rate/ROI increasing) by > 5%/year
- **Stable:** CAGR within ±5%/year
- **Declining:** CAGR unfavourable by > 5%/year

---

## 6. Drawers & Modals

### 6.1 Drawer: `branch-deep-dive` (780px, right-slide)

- **Title:** "[Branch Name] — Marketing Deep Dive"
- **Tabs:** Overview · Campaigns · Sources · Funnel · Trend · Recommendations
- **Overview tab:**
  - Branch card: name, city, tier, board, seat capacity, Principal name
  - 8 mini-KPIs: Admissions, Fill Rate, Marketing Spend, CPL, CPA, ROI, Efficiency Score, Rank
  - Comparison bar: branch value vs group average for each KPI (horizontal diverging bars)
  - Performance tier badge with explanation
- **Campaigns tab:** All campaigns targeting this branch with per-campaign spend, leads, admissions, ROI
  - Sorted by ROI DESC; highlights top 3 and bottom 3 campaigns
  - Links to O-35 campaign deep-dive
- **Sources tab:** Lead sources for this branch with per-source CPL, CPA, conversion
  - Identifies which sources work specifically for this branch's catchment
  - Example: "For Warangal branch, Eenadu Telugu daily delivers CPL ₹120 while Google Ads delivers ₹450 — newspaper is 3.75x more efficient in this market"
  - Links to O-36 source deep-dive
- **Funnel tab:** Branch-specific conversion funnel (Lead → Contacted → Interested → Visit → Apply → Enroll)
  - Drop-off analysis compared to group average at each stage
  - Highlights stages where this branch underperforms peers
- **Trend tab:** Season-over-season line charts for: fill rate, CPA, spend, admissions, efficiency score
  - 3-5 season history
  - Overlay group average trend for comparison
- **Recommendations tab (G4+ only):**
  - Budget recommendation: increase/decrease/maintain with specific ₹ amount
  - Channel mix recommendation: "Shift ₹3L from newspaper to digital — projected CPA improvement 15%"
  - Operational recommendations: "Improve walk-in experience — visit-to-application drop-off is 35% vs group average 18%"
  - Competitive context: "3 new CBSE schools opened within 2 km in 2024-25 — increased competition explains CPA rise"
- **Footer:** [Export Branch Report] [Compare with Peer] [View in O-22 Enrollment Drive]
- **Access:** Role 132, 119, or G4+ for full view; Branch Principal sees own branch overview + campaigns + funnel (no recommendations tab)

### 6.2 Modal: `peer-comparison` (720px)

- **Title:** "Peer Comparison — [Branch Name]"
- **Auto-selected peers:** 3-5 branches in same tier + size group
- **Manual override:** Add/remove branches from comparison set
- **Comparison table:** Side-by-side for all selected branches:
  - Metrics: Fill Rate, CPA, CPL, ROI, Spend per Seat, Efficiency Score, Lead Conversion %
  - Colour-coded: best = green, worst = red per metric
  - Delta row: difference from peer group average
- **Radar chart:** One polygon per branch on axes: Fill Rate, Cost Efficiency (1/CPA normalised), Lead Quality (conversion %), Budget Discipline, ROI
- **Summary:** "Branch X is [N]% above/below peer average on CPA. Primary driver: [reason — e.g., low walk-in conversion rate, high spend on underperforming newspaper edition]."
- **Buttons:** Close · Change Peers · Export Comparison
- **Access:** Role 132, 119, or G4+

### 6.3 Modal: `budget-reallocation-recommendation` (640px, G4+ only)

- **Title:** "Budget Reallocation Recommendations"
- **Summary table:**

  | Branch | Current Budget | Recommended | Change | Justification |
  |---|---|---|---|---|
  | Kompally | ₹18L | ₹22L | +₹4L | Under-funded — fill rate 92% with lowest CPA; additional budget projected to add 80 admissions |
  | Mehdipatnam | ₹22L | ₹15L | -₹7L | Over-spending — CPA 3x peer average despite similar catchment; reduce and investigate conversion issues |
  | Tellapur (new) | ₹8L | ₹18L | +₹10L | New branch, high-growth catchment — needs 2x investment to establish brand |
  | Siddipet | ₹12L | ₹6L | -₹6L | Over-funded — 95% fill rate on word-of-mouth; newspaper spend unnecessary |

- **Net impact:** "Reallocation is budget-neutral (₹0 net change). Projected impact: +240 additional admissions group-wide (+1.9% fill rate improvement)"
- **Constraints:** Total budget must remain unchanged; no branch reduced below ₹2L minimum
- **Buttons:** Close · Export Recommendation · Submit to CEO for Approval (G4+ only)
- **Note:** This modal generates a recommendation only — actual budget changes happen in O-09 (Campaign Budget Manager)
- **Access:** G4/G5 only (contains sensitive budget reallocation data)

### 6.4 Modal: `export-branch-report` (480px)

- **Title:** "Export Branch Marketing Comparison"
- **Fields:**
  - Format: CSV / Excel (XLSX) / PDF
  - Scope: All branches / Selected tier / Selected branches
  - Seasons: Current / Multi-season (checkbox)
  - Include: League table / Peer comparison / Budget adequacy / Recommendations (G4+)
  - Include charts: Yes/No (PDF only)
- **Quick exports:**
  - "Board Presentation PDF" — league table + charts + top/bottom 5 branches + recommendations
  - "Full Data CSV" — all metrics, all branches, all seasons
- **Buttons:** Cancel · Export
- **Access:** Role 132 or G4+

---

## 7. Charts

### 7.1 Branch Efficiency Scatter (Scatter / Bubble)

| Property | Value |
|---|---|
| Chart type | Scatter/Bubble (Chart.js 4.x) |
| Title | "Branch Marketing Efficiency — Spend vs Fill Rate" |
| Data | X = Marketing Spend (₹ Lakhs), Y = Fill Rate (%); bubble size = seat capacity |
| Colour | By performance tier: Star = `#10B981`, On Track = `#3B82F6`, Needs Attention = `#F59E0B`, Critical = `#EF4444` |
| Quadrants | Top-left: "Efficient" (low spend, high fill) · Top-right: "Scaling" (high spend, high fill) · Bottom-left: "Organic" (low spend, low fill — may need more budget) · Bottom-right: "Inefficient" (high spend, low fill — investigate) |
| Labels | Branch name on each bubble |
| Tooltip | "[Branch] ([Tier]): Spend ₹[X]L · Fill [Y]% · CPA ₹[Z] · Score [W]/100" |
| Regression line | Dashed trend line showing expected fill rate at each spend level |
| API | `GET /api/v1/group/{id}/marketing/analytics/branch-comparison/charts/efficiency-scatter/` |

### 7.2 Branch Ranking Horizontal Bar (Horizontal Bar)

| Property | Value |
|---|---|
| Chart type | Horizontal bar (Chart.js 4.x) |
| Title | "Branch Marketing Efficiency Ranking" |
| Data | All branches sorted by efficiency score; bar length = score (0-100) |
| Colour | Gradient: green (≥ 80) → amber (50-79) → red (< 50) |
| Labels | Branch name on Y-axis, score value at bar end |
| Annotation | Vertical line at score = 70 (group target) |
| Tooltip | "[Branch]: Score [X]/100 · Rank #[Y] · CPA ₹[Z]" |
| API | `GET /api/v1/group/{id}/marketing/analytics/branch-comparison/charts/ranking-bar/` |

### 7.3 Spend Distribution Treemap (Treemap)

| Property | Value |
|---|---|
| Chart type | Treemap (Chart.js 4.x + chartjs-chart-treemap plugin) |
| Title | "Marketing Spend Distribution Across Branches" |
| Data | Each rectangle = one branch; area proportional to marketing spend |
| Colour | By performance tier (same palette as scatter) |
| Labels | Branch name + spend amount inside each rectangle |
| Tooltip | "[Branch]: ₹[X]L ([Y]% of total) · Fill Rate [Z]% · CPA ₹[W]" |
| Insight | Visual immediately shows if spend is proportional to results — large red rectangles indicate inefficient branches consuming disproportionate budget |
| API | `GET /api/v1/group/{id}/marketing/analytics/branch-comparison/charts/spend-treemap/` |

### 7.4 Fill Rate vs Spend Bubble Chart (Bubble)

| Property | Value |
|---|---|
| Chart type | Bubble (Chart.js 4.x) |
| Title | "Fill Rate vs Marketing Spend per Seat" |
| Data | X = Spend per Seat (₹), Y = Fill Rate (%); bubble size = total admissions |
| Colour | By city tier: Metro = `#6366F1`, Tier-2 = `#3B82F6`, Tier-3 = `#10B981`, Rural = `#F59E0B` |
| Annotation | Horizontal line at target fill rate (90%); vertical lines at tier-wise spend benchmarks |
| Tooltip | "[Branch] ([City]): ₹[X] per seat · Fill [Y]% · [Z] admissions · [W] seats" |
| API | `GET /api/v1/group/{id}/marketing/analytics/branch-comparison/charts/fill-vs-spend/` |

### 7.5 Efficiency Trend per Branch (Multi-Line)

| Property | Value |
|---|---|
| Chart type | Multi-line (Chart.js 4.x) |
| Title | "Branch Efficiency Score Trend — Last 4 Seasons" |
| Data | X = season, Y = efficiency score; one line per selected branch (max 8) |
| Colour | Distinct colour per branch from palette |
| Annotation | Horizontal dashed line at group average efficiency score per season |
| Tooltip | "[Branch] — [Season]: Score [X]/100 (Rank #[Y])" |
| API | `GET /api/v1/group/{id}/marketing/analytics/branch-comparison/charts/efficiency-trend/` |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Season filter changed | "Branch comparison updated for [Season]" | Info | 3s |
| Peer group selected | "Showing peer comparison for [Peer Group Name]" | Info | 3s |
| Export started | "Generating branch comparison report — [Format]" | Info | 3s |
| Export complete | "Report downloaded — [Filename]" | Success | 3s |
| Export failed | "Export failed — please try again" | Error | 5s |
| League table printed | "League table sent to printer" | Success | 3s |
| Recommendation submitted | "Budget reallocation recommendation submitted to CEO" | Success | 4s |
| Branch deep-dive opened | "Loading [Branch Name] marketing data..." | Info | 2s |
| Peer comparison loaded | "Comparing [N] branches in [Peer Group]" | Info | 3s |
| No data for filter | "No branches match selected filters" | Warning | 4s |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| No branch marketing data | 🏫 | "No Branch Data Available" | "Branch marketing comparison requires campaign spend data (O-09) and lead attribution (O-16) to be populated for at least 2 branches." | View Budget Manager (O-09) |
| Single branch (no comparison) | 📊 | "Comparison Requires Multiple Branches" | "Only 1 branch has marketing data. Add campaign data for more branches to enable comparison." | View Campaign Builder (O-08) |
| No peer group matches | 🔍 | "No Branches in This Peer Group" | "No branches match the selected tier and size filters. Adjust peer group criteria." | Reset Peer Group |
| No trend data (first season) | 📈 | "Trend Data Unavailable" | "Season-over-season trends require at least 2 seasons of data. Current season rankings are available in the League Table tab." | View League Table |
| No budget adequacy data | 💰 | "Budget Adequacy Requires Setup" | "Configure branch-level marketing budgets in O-09 and catchment data in O-27 to enable budget adequacy assessment." | Go to Budget Manager |
| Branch Principal — no data | 🔒 | "Your Branch Data Not Yet Available" | "Marketing data for your branch will appear once campaigns are running and leads are tracked." | Contact Campaign Manager |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | 6 KPI shimmer + tab bar + table skeleton (20 rows) |
| Tab switch | Content skeleton matching target tab layout |
| Branch deep-dive drawer | 780px skeleton: overview card + 6 tabs + mini-KPI cards |
| Season/tier filter change | KPI shimmer + table skeleton (data refresh) |
| Peer comparison modal | 720px skeleton: branch selector + table + radar chart placeholder |
| Budget recommendation modal | 640px skeleton: table (10 rows) + summary card |
| Export generation | Spinner: "Generating report..." |
| Chart load | Grey canvas placeholder per chart (load on `intersect once`) |
| Treemap load | Rectangular skeleton with grey blocks |
| Trend sparkline load | Small grey line placeholder per row |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/marketing/analytics/branch-comparison/kpis/` | G1+ | KPI summary (6 cards) |
| GET | `/api/v1/group/{id}/marketing/analytics/branch-comparison/league-table/` | G1+ | Branch league table (paginated, filterable) |
| GET | `/api/v1/group/{id}/marketing/analytics/branch-comparison/branches/{branch_id}/` | G1+ | Branch deep-dive data |
| GET | `/api/v1/group/{id}/marketing/analytics/branch-comparison/branches/{branch_id}/campaigns/` | G1+ | Campaigns for branch |
| GET | `/api/v1/group/{id}/marketing/analytics/branch-comparison/branches/{branch_id}/sources/` | G1+ | Lead sources for branch |
| GET | `/api/v1/group/{id}/marketing/analytics/branch-comparison/branches/{branch_id}/funnel/` | G1+ | Branch conversion funnel |
| GET | `/api/v1/group/{id}/marketing/analytics/branch-comparison/branches/{branch_id}/trend/` | G1+ | Multi-season trend for branch |
| GET | `/api/v1/group/{id}/marketing/analytics/branch-comparison/branches/{branch_id}/recommendations/` | G4+ | Branch-specific recommendations |
| GET | `/api/v1/group/{id}/marketing/analytics/branch-comparison/peer-groups/` | G1+ | List of auto-generated peer groups |
| GET | `/api/v1/group/{id}/marketing/analytics/branch-comparison/peer-compare/` | G1+ | Peer comparison (branch_ids as params) |
| GET | `/api/v1/group/{id}/marketing/analytics/branch-comparison/budget-adequacy/` | G1+ | Budget adequacy assessment table |
| GET | `/api/v1/group/{id}/marketing/analytics/branch-comparison/budget-reallocation/` | G4+ | Budget reallocation recommendations |
| GET | `/api/v1/group/{id}/marketing/analytics/branch-comparison/trend/` | G1+ | Multi-branch trend data (branch_ids + metric params) |
| POST | `/api/v1/group/{id}/marketing/analytics/branch-comparison/export/` | G1+ | Generate export |
| GET | `/api/v1/group/{id}/marketing/analytics/branch-comparison/charts/efficiency-scatter/` | G1+ | Scatter chart data |
| GET | `/api/v1/group/{id}/marketing/analytics/branch-comparison/charts/ranking-bar/` | G1+ | Ranking bar chart data |
| GET | `/api/v1/group/{id}/marketing/analytics/branch-comparison/charts/spend-treemap/` | G1+ | Treemap chart data |
| GET | `/api/v1/group/{id}/marketing/analytics/branch-comparison/charts/fill-vs-spend/` | G1+ | Bubble chart data |
| GET | `/api/v1/group/{id}/marketing/analytics/branch-comparison/charts/efficiency-trend/` | G1+ | Efficiency trend line data |

---

## 12. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load | Page load | `hx-get=".../branch-comparison/kpis/"` | `#kpi-bar` | `innerHTML` | `hx-trigger="load"` |
| Tab switch | Tab click | `hx-get` with tab param | `#branch-content` | `innerHTML` | `hx-trigger="click"` |
| Filter apply | Dropdown change | `hx-get` with filter params | `#tab-table-body` | `innerHTML` | `hx-trigger="change"` with 300ms debounce |
| Season change | Season dropdown | `hx-get` with season param | `#kpi-bar, #branch-content` | `innerHTML` | Refreshes both KPIs and content |
| Branch deep-dive | Row click | `hx-get=".../branches/{id}/"` | `#right-drawer` | `innerHTML` | `hx-trigger="click"` |
| Peer compare | Compare button | `hx-get=".../peer-compare/?ids={...}"` | `#peer-modal-content` | `innerHTML` | — |
| Peer group change | Peer group dropdown | `hx-get=".../peer-compare/?group={g}"` | `#peer-content` | `innerHTML` | `hx-trigger="change"` |
| Budget adequacy load | Budget tab click | `hx-get=".../budget-adequacy/"` | `#budget-content` | `innerHTML` | — |
| Reallocation modal | Recommendation button | `hx-get=".../budget-reallocation/"` | `#realloc-modal-content` | `innerHTML` | G4+ only |
| Trend branch select | Branch multi-select | `hx-get=".../trend/?branches={...}&metric={m}"` | `#trend-content` | `innerHTML` | `hx-trigger="change"` with 500ms debounce |
| Trend metric change | Metric dropdown | `hx-get=".../trend/?metric={m}"` | `#trend-content` | `innerHTML` | `hx-trigger="change"` |
| Export trigger | Export button | `hx-post=".../export/"` | `#export-result` | `innerHTML` | Returns download link |
| Chart load | Tab/page load | `hx-get=".../charts/..."` | `#chart-{name}` | `innerHTML` | `hx-trigger="intersect once"` |
| Pagination | Page controls | `hx-get` with `?page={n}` | `#tab-table-body` | `innerHTML` | 30/page |
| Sort column | Header click | `hx-get` with `?sort={col}&dir={asc|desc}` | `#tab-table-body` | `innerHTML` | Preserves filters |
| Print league table | Print button | `hx-get=".../league-table/?format=print"` | `#print-frame` | `innerHTML` | Opens print-optimised view |

---

*Page spec version: 1.0 · Last updated: 2026-03-26*
