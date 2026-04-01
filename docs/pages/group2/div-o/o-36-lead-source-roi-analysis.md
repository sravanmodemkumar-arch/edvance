# O-36 — Lead Source ROI Analysis

> **URL:** `/group/marketing/analytics/lead-source-roi/`
> **File:** `o-36-lead-source-roi-analysis.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Role:** Group Admission Data Analyst (Role 132, G1) — primary operator

---

## 1. Purpose

The Lead Source ROI Analysis page provides granular, source-level marketing economics for the group — answering "for every rupee we spend on Eenadu ads, how many admissions do we get compared to every rupee on Google Ads?" While O-35 (Campaign Performance Analytics) analyses campaigns and channels in aggregate, this page drills into individual lead sources: not just "newspaper" as a channel, but "Eenadu Hyderabad City Edition" vs "Sakshi Vijayawada Edition" vs "Deccan Chronicle Sunday Supplement." In the Indian education market, the difference between sources within the same channel is often larger than the difference between channels — a full-page ad in Eenadu's Hyderabad city edition might generate 800 leads at ₹180 CPL, while the same ad in Eenadu's Nalgonda district edition generates 40 leads at ₹3,500 CPL. Without source-level analysis, groups waste lakhs on underperforming editions, keywords, and locations.

The problems this page solves:

1. **Source-level blindness within channels:** A group's "newspaper budget" of ₹1.2 Cr is split across 8 publications, 3 languages (Telugu, English, Hindi), and 15+ editions. The marketing director knows newspapers "work" but cannot tell the CEO which specific publication-edition combination delivers the best ROI. Similarly, "digital" encompasses Google Search (branded keywords vs generic keywords vs competitor keywords), Google Display, Meta (Facebook + Instagram), YouTube pre-roll, and programmatic — each with vastly different CPL profiles. This page provides source-level unit economics.

2. **Regional source effectiveness variation:** In India, source effectiveness varies dramatically by geography. In Hyderabad, digital ads dominate — parents search "best CBSE schools near Kukatpally" on Google. In Warangal, newspaper ads in Eenadu drive 60% of enquiries because parents trust print media. In Vijayawada, WhatsApp forwarding through parent groups is the top source. A group with branches across Telangana and Andhra Pradesh cannot apply a single source strategy; it needs branch-level source analysis — which this page provides.

3. **Diminishing returns detection:** A source that delivered 500 leads at ₹120 CPL in 2023-24 might deliver only 300 leads at ₹280 CPL in 2025-26 — newspaper readership is declining in metros while ad rates keep increasing. Without multi-year source tracking, groups miss the inflection point where a source becomes uneconomical. This page shows year-over-year CPL and CPA trends per source, with automatic alerts when a source's CPL exceeds its historical average by more than 30%.

4. **Source concentration risk (HHI analysis):** Some groups derive 50%+ of their leads from a single source (e.g., Eenadu newspaper). If that source becomes unavailable (newspaper strike, ad rate hike, publication policy change), the group faces an admissions crisis. The Herfindahl-Hirschman Index (HHI) measures source concentration — a healthy group should have HHI < 2,500 (diversified) rather than HHI > 5,000 (concentrated).

5. **Budget reallocation justification:** When the Data Analyst recommends shifting ₹20L from newspaper to digital, the CEO asks "show me the data." This page provides the evidence: source-wise CPL, CPA, ROI trends, conversion rates, and projected impact of budget reallocation — enabling data-driven budget decisions rather than gut-feel or agency recommendations.

**Scale:** 150 groups × 20-80 distinct lead sources per group × 3-5 years of historical data · Source taxonomy: 5 parent channels → 20-80 specific sources per group · Data volume: 2,000-2,00,000 leads per season with source attribution

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Admission Data Analyst | 132 | G1 | Read + Export — view all source analytics, run simulations, export reports | Primary operator |
| Group Admissions Campaign Manager | 119 | G3 | Read — view source performance to inform campaign planning | Uses insights for budget allocation in O-09 |
| Group Topper Relations Manager | 120 | G3 | No access | Source ROI not relevant to topper relations |
| Group Admission Telecaller Executive | 130 | G3 | No access | Source analytics not relevant to telecalling |
| Group Campaign Content Coordinator | 131 | G2 | No access | Content role, no analytics function |
| Group CEO / Chairman | — | G4/G5 | Read + Export — full access, approve budget reallocation recommendations | Strategic budget decisions |
| Branch Principal | — | G3 | Read (own branch) — view source ROI for own branch only | Branch-scoped via row-level security |

> **Access enforcement:** `@require_role(min_level=G1, division='O')`. Export: role 132 or G4+. Budget simulation: role 132 or G4+. Branch Principals filtered by `branch_id`. All data is read-only — no CRUD operations on analytics pages.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  >  Marketing & Campaigns  >  Analytics & Reports  >  Lead Source ROI Analysis
```

### 3.2 Page Header
```
Lead Source ROI Analysis                            [Season: v]  [Branch: v]  [Compare Seasons: v]  [Export v]
Data Analyst — Priya Raghunandan
Sunrise Education Group · Season 2025-26 · 47 sources tracked · Best: Parent Referral (ROI 8.2x) · Worst CPL: Google Display (₹680)
```

---

## 4. KPI Summary Bar (6 cards)

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Total Sources Tracked | Integer | COUNT(DISTINCT source_id) WHERE season = selected AND has_spend = true | Static blue | `#kpi-sources` |
| 2 | Best Performing Source | Text + ROI | Source name with MAX(ROI) — e.g., "Parent Referral (8.2x)" | Static green | `#kpi-best` |
| 3 | Worst CPL Source | Text + ₹ | Source name with MAX(CPL) — e.g., "Google Display (₹680)" | Static red | `#kpi-worst-cpl` |
| 4 | Avg CPL All Sources | ₹ Amount | SUM(all source spend) / SUM(all source leads) — weighted average | Green < ₹200, Amber ₹200-500, Red > ₹500 | `#kpi-avg-cpl` |
| 5 | Source Concentration (HHI) | Integer (0-10,000) | SUM(source_lead_share² × 10,000) — Herfindahl-Hirschman Index | Green < 1,500, Amber 1,500-2,500, Red > 2,500 | `#kpi-hhi` |
| 6 | YoY Improvement % | Percentage | ((Current season avg CPL - Previous season avg CPL) / Previous season avg CPL) × -100 | Green > 0% (improving), Red < 0% (deteriorating) | `#kpi-yoy` |

**HHI interpretation guide (shown as tooltip):**
- < 1,500: Unconcentrated — healthy source diversification
- 1,500-2,500: Moderately concentrated — acceptable but monitor top source
- > 2,500: Highly concentrated — over-reliance on 1-2 sources, diversify urgently
- > 5,000: Dangerous — single source dominance, business risk

**HTMX:** `hx-get="/api/v1/group/{id}/marketing/analytics/lead-source-roi/kpis/"` → `hx-trigger="load"`

---

## 5. Sections

### 5.1 Tab Navigation

Four tabs:
1. **Source-wise ROI** — Master table with per-source unit economics
2. **Multi-Year Trend** — Year-over-year source performance comparison
3. **Source Mix Analysis** — Concentration, diversification, and optimization
4. **Diminishing Returns** — Sources showing declining efficiency

### 5.2 Tab 1: Source-wise ROI

**Filter bar:** Season · Channel (parent channel) · Branch · Min spend threshold (₹) · Sort metric (CPL/CPA/ROI/Leads/Conversion %)

| Column | Type | Sortable | Notes |
|---|---|---|---|
| # | Auto-index | No | Row number |
| Rank | Integer | Yes | Rank by selected metric (default: ROI) |
| Source Name | Text (link) | Yes | Specific source — e.g., "Eenadu - Hyderabad City", "Google Search - Branded Keywords", "Parent Referral", "WhatsApp Broadcast - Feb Campaign" |
| Channel | Badge | Yes | Parent channel: Newspaper / Digital / WhatsApp / Outdoor / Referral / Open Day / Fair / Email / SMS |
| Total Spend (₹) | Amount | Yes | All spend attributed to this source in selected season |
| Spend Share % | Percentage | Yes | Source spend / Total group spend × 100 |
| Total Leads | Integer | Yes | Leads attributed to this source |
| Lead Share % | Percentage | Yes | Source leads / Total leads × 100 |
| Qualified Leads | Integer | Yes | Leads that progressed past initial contact |
| Qualification Rate % | Percentage | Yes | Qualified / Total × 100 |
| Admissions | Integer | Yes | Confirmed enrollments from this source |
| CPL (₹) | Amount | Yes | Spend / Leads; conditional formatting by channel benchmark |
| CPA (₹) | Amount | Yes | Spend / Admissions |
| Conversion % | Percentage | Yes | (Admissions / Leads) × 100 |
| ROI | Ratio | Yes | Revenue from source admissions / Source spend |
| YoY CPL Change | Percentage | Yes | ((Current CPL - Prev CPL) / Prev CPL) × 100; green if negative (improving), red if positive |
| Efficiency Rating | Stars (1-5) | Yes | Composite: 5 = top quintile ROI, 1 = bottom quintile |
| Actions | Buttons | No | [Deep Dive] [Compare] |

**Default sort:** ROI DESC
**Pagination:** Server-side · 25/page
**Summary row:** Group totals for spend, leads, admissions; weighted averages for CPL, CPA, ROI

**Indian source taxonomy (standard categories):**

| Channel | Typical Sources | Notes |
|---|---|---|
| Newspaper | Eenadu (TE), Sakshi (TE), Deccan Chronicle (EN), The Hindu (EN), Times of India (EN), Namaste Telangana (TE), Vaartha (TE), Andhra Jyothy (TE), Dainik Bhaskar (HI), Rajasthan Patrika (HI) | Each tracked by edition (city/district) |
| Digital | Google Search (branded), Google Search (generic), Google Display, Meta - Facebook, Meta - Instagram, YouTube Pre-roll, Programmatic Display | Each tracked by campaign/ad group |
| WhatsApp | Broadcast - Prospect List, Broadcast - Parent Group, Forward via Teachers, Forward via Alumni | Tracked by batch/campaign |
| Outdoor | Hoardings (specific locations), Bus Shelters, Auto Rickshaw, Pamphlet Distribution, Standee at Malls | Tracked by location cluster |
| Referral | Parent Referral, Alumni Referral, Staff Referral, Current Student Referral | Tracked by referrer type |
| Events | Open Day, School Fair/Exhibition, Mall Stall, Society Event, Demo Class | Tracked per event |
| Direct | Walk-in (organic), Phone Enquiry (organic), Website Form (organic) | No spend — pure organic |

### 5.3 Tab 2: Multi-Year Trend

**Season selector:** Checkbox for each available season (up to 5 seasons); at least 2 must be selected.

**Multi-year comparison table (one row per source):**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Source Name | Text | Yes | — |
| Channel | Badge | Yes | — |
| CPL 2021-22 | Amount | Yes | ₹ CPL for season; "—" if not tracked |
| CPL 2022-23 | Amount | Yes | — |
| CPL 2023-24 | Amount | Yes | — |
| CPL 2024-25 | Amount | Yes | — |
| CPL 2025-26 | Amount | Yes | Current season |
| 3-Year CAGR | Percentage | Yes | Compound annual growth rate of CPL; negative = improving, positive = worsening |
| Trend | Sparkline | No | Mini line chart of CPL across selected seasons |
| Leads 2024-25 | Integer | Yes | Last season leads for comparison |
| Leads 2025-26 | Integer | Yes | Current season leads |
| Lead Change % | Percentage | Yes | YoY lead volume change |
| Recommendation | Badge | No | "Increase Budget" (green) / "Maintain" (blue) / "Reduce" (amber) / "Discontinue" (red) |

**Recommendation logic:**
- **Increase Budget:** CPL decreasing YoY AND conversion > channel average AND ROI > 3x
- **Maintain:** CPL stable (±10%) AND ROI 1.5-3x
- **Reduce:** CPL increasing > 20% YoY OR ROI < 1.5x
- **Discontinue:** CPL increasing > 40% YoY AND leads declining > 30% AND ROI < 1x

### 5.4 Tab 3: Source Mix Analysis

**Three sub-sections:**

**A. Source Contribution Breakdown:**

| Source | Spend Share | Lead Share | Admission Share | Over/Under-indexed |
|---|---|---|---|---|
| Eenadu (all editions) | 28% | 22% | 25% | Under-indexed (spend > admission share) |
| Google Search | 12% | 18% | 20% | Over-indexed (admission share > spend share) |
| Parent Referral | 4% | 12% | 18% | Highly over-indexed (best efficiency) |
| WhatsApp Broadcasts | 8% | 15% | 10% | Neutral |
| ... | ... | ... | ... | ... |

**B. Concentration Analysis (HHI):**
- Current HHI score with trend (last 3 seasons)
- Top 3 sources by lead share with individual contribution to HHI
- Diversification recommendation: "Reducing Eenadu lead share from 22% to 15% would lower HHI from 2,100 to 1,600 (unconcentrated zone)"

**C. Source Efficiency Matrix (Quadrant):**
Displayed as an interactive table (chart in Section 7):

| Quadrant | Sources | Action |
|---|---|---|
| High ROI + High Volume ("Stars") | Parent Referral, Google Search Branded | Protect and scale |
| High ROI + Low Volume ("Niche Winners") | Alumni Referral, Demo Class | Scale up — capacity exists |
| Low ROI + High Volume ("Volume Traps") | Eenadu City, WhatsApp Broadcast | Optimise or reallocate |
| Low ROI + Low Volume ("Eliminate") | Google Display, Pamphlet Distribution | Discontinue and redirect budget |

### 5.5 Tab 4: Diminishing Returns

**Purpose:** Flag sources where ROI is declining season-over-season, indicating market saturation or competitive pressure.

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Source Name | Text | Yes | — |
| Channel | Badge | Yes | — |
| CPL 2 Seasons Ago | Amount | Yes | — |
| CPL Last Season | Amount | Yes | — |
| CPL This Season | Amount | Yes | — |
| CPL Growth Rate | Percentage | Yes | CAGR of CPL over 3 seasons; higher = worse |
| Lead Volume Change | Percentage | Yes | Change in leads despite similar/more spend |
| ROI Current | Ratio | Yes | Current season ROI |
| ROI Decline | Percentage | Yes | (Current ROI - Previous ROI) / Previous ROI × 100 |
| Spend at Risk (₹) | Amount | Yes | Current spend on this source — potential savings if discontinued/reduced |
| Severity | Badge | Yes | Warning (CPL up 10-25%) / Serious (25-50%) / Critical (> 50%) |
| Suggested Reallocation | Text | No | "Shift ₹[X]L to [Source Y] — projected CPL improvement: [Z]%" |

**Default sort:** Severity DESC, then CPL Growth Rate DESC
**Filter:** Only sources with ≥ 2 seasons of data and CPL growth > 10%

---

## 6. Drawers & Modals

### 6.1 Drawer: `source-deep-dive` (720px, right-slide)

- **Title:** "[Source Name] — Source Deep Dive"
- **Tabs:** Overview · Branch Breakdown · Lead Quality · Trend · Campaigns
- **Overview tab:**
  - Source card: name, channel, total spend, leads, admissions, CPL, CPA, ROI
  - Year-over-year comparison: current season vs previous season for all metrics
  - Efficiency rating with explanation (what drives the 1-5 star rating)
  - Source-specific notes:
    - Newspaper: publication, edition(s), typical ad sizes used, response code/phone
    - Digital: platform, campaign types (search/display/video), top keywords/audiences
    - WhatsApp: broadcast list sizes, message templates, read rates
    - Referral: referrer demographics, average referrals per referrer
- **Branch Breakdown tab:** Table showing per-branch performance for this source
  - | Branch | Leads | Admissions | CPL | CPA | ROI | Rank |
  - Useful for identifying which branches benefit most from a specific source — e.g., Eenadu works for Warangal branch but not Hyderabad branch
- **Lead Quality tab:**
  - Lead qualification rate from this source
  - Average time-to-conversion (days from lead to admission)
  - Drop-off stage distribution (where do this source's leads fail?)
  - Duplicate/invalid lead percentage (newspaper ads often generate 15-20% invalid phone numbers)
- **Trend tab:**
  - Monthly CPL line chart for current season
  - Season-over-season CPL bar chart
  - Lead volume trend with spend overlay
- **Campaigns tab:** List of all campaigns that used this source, with per-campaign CPL and ROI
- **Footer:** [Export Source Report] [Compare Sources] [View in O-16]
- **Access:** Role 132, 119, or G4+

### 6.2 Modal: `source-comparison` (720px)

- **Title:** "Compare Lead Sources"
- **Selection:** Up to 4 sources (dropdown with search, filter by channel)
- **Comparison table:**
  - Side-by-side metrics: Spend, Leads, Admissions, CPL, CPA, ROI, Conversion %, Lead Quality Score, YoY Change
  - Colour-coded cells: best value in green, worst in red for each metric
- **Comparison chart:** Grouped bar chart showing all selected sources across key metrics
- **Summary:** Auto-generated recommendation — "Source A delivers 2.3x better ROI than Source B at similar spend levels. Consider reallocating ₹[X]L from B to A."
- **Buttons:** Close · Export Comparison
- **Access:** Role 132, 119, or G4+

### 6.3 Modal: `budget-reallocation-simulator` (720px)

- **Title:** "Budget Reallocation Simulator"
- **Current allocation table:**
  - | Source | Current Budget (₹) | Current CPL (₹) | Current Admissions | Projected Admissions |
  - Each row has an editable budget field (slider or input)
  - Total must equal current total budget (auto-adjusts)
- **Simulation engine:**
  - Uses historical CPL elasticity: if budget increases 20%, CPL typically increases 5-15% (diminishing returns)
  - Projected leads = New Budget / (Current CPL × diminishing returns factor)
  - Projected admissions = Projected Leads × Source conversion rate
- **Scenario comparison:**
  - Current scenario: Total admissions with current allocation
  - Proposed scenario: Total admissions with proposed allocation
  - Delta: Additional admissions (or fewer) + net CPL/CPA change
- **Presets:**
  - "Optimise for Maximum Admissions" — auto-allocates to minimise overall CPA
  - "Optimise for Lowest CPL" — shifts budget to cheapest sources
  - "Diversify Sources" — targets HHI < 1,500
  - "Cut Underperformers" — removes budget from sources with ROI < 1x
- **Validation:** Total budget must match group's approved marketing budget from O-09
- **Buttons:** Cancel · Reset to Current · Apply Preset · Save Scenario · Export Scenario
- **Access:** Role 132 or G4+ (simulation is analysis-only, does not change actual budgets)

### 6.4 Modal: `export-source-report` (480px)

- **Title:** "Export Source ROI Report"
- **Fields:**
  - Format: CSV / Excel (XLSX) / PDF
  - Seasons included: Multi-select (current + previous seasons)
  - Data scope: All sources / Selected channel / Selected branch / Top N sources
  - Include charts: Yes/No (PDF only)
  - Include recommendations: Yes/No (includes auto-generated increase/maintain/reduce/discontinue)
- **Buttons:** Cancel · Export
- **Access:** Role 132 or G4+

---

## 7. Charts

### 7.1 Source ROI Bar Chart (Horizontal Bar)

| Property | Value |
|---|---|
| Chart type | Horizontal bar (Chart.js 4.x) — sorted by ROI DESC |
| Title | "Lead Source ROI — Current Season" |
| Data | All sources with ≥ ₹1L spend; bar length = ROI value |
| Colour | Green (ROI > 3x), Amber (1.5-3x), Red (< 1.5x) |
| Labels | Source name on Y-axis |
| Annotation | Vertical line at ROI = 3.0x (target) and ROI = 1.0x (break-even) |
| Tooltip | "[Source]: ROI [X]x · Spend ₹[Y] · Admissions [Z]" |
| API | `GET /api/v1/group/{id}/marketing/analytics/lead-source-roi/charts/roi-bar/` |

### 7.2 CPL vs CPA Scatter by Source (Scatter)

| Property | Value |
|---|---|
| Chart type | Scatter (Chart.js 4.x) |
| Title | "CPL vs CPA by Source" |
| Data | X = CPL (₹), Y = CPA (₹); one point per source; point size = total spend |
| Colour | By channel: Newspaper `#3B82F6`, Digital `#8B5CF6`, WhatsApp `#10B981`, Outdoor `#F59E0B`, Referral `#EC4899`, Events `#14B8A6`, Direct `#6B7280` |
| Labels | Source name on hover |
| Quadrants | Top-left: "Low CPL, High CPA" (high drop-off) · Bottom-left: "Low CPL, Low CPA" (best) · Bottom-right: "High CPL, Low CPA" (expensive but efficient) · Top-right: "High CPL, High CPA" (worst) |
| Tooltip | "[Source]: CPL ₹[X] · CPA ₹[Y] · Conversion [Z]% · Spend ₹[W]" |
| API | `GET /api/v1/group/{id}/marketing/analytics/lead-source-roi/charts/cpl-cpa-scatter/` |

### 7.3 Source Contribution Pie (Doughnut)

| Property | Value |
|---|---|
| Chart type | Doughnut (Chart.js 4.x) |
| Title | "Lead Source Contribution — Admissions" |
| Data | Each source's share of total admissions (top 10 + "Others") |
| Colour | Distinct colour per source from palette |
| Centre text | "Total: [N] admissions" |
| Tooltip | "[Source]: [N] admissions ([X]%)" |
| Toggle | Dropdown to switch between Admissions / Leads / Spend distribution |
| API | `GET /api/v1/group/{id}/marketing/analytics/lead-source-roi/charts/contribution-pie/` |

### 7.4 Year-over-Year Trend Lines (Multi-Line)

| Property | Value |
|---|---|
| Chart type | Multi-line (Chart.js 4.x) |
| Title | "CPL Trend by Source — Last 4 Seasons" |
| Data | X = season (year), Y = CPL; one line per top 8 sources |
| Colour | Distinct colour per source |
| Tooltip | "[Source] — [Season]: CPL ₹[X] ([+/-Y]% vs previous)" |
| Annotation | Horizontal dashed line at group average CPL |
| API | `GET /api/v1/group/{id}/marketing/analytics/lead-source-roi/charts/yoy-trend/` |

### 7.5 Source Efficiency Matrix (Bubble / Quadrant)

| Property | Value |
|---|---|
| Chart type | Scatter/Bubble (Chart.js 4.x) |
| Title | "Source Efficiency Matrix" |
| Data | X = Lead Volume (normalised 0-100), Y = ROI; bubble size = total spend |
| Colour | Green (Stars quadrant), Blue (Niche Winners), Amber (Volume Traps), Red (Eliminate) |
| Quadrant lines | X midpoint = median lead volume, Y midpoint = ROI 3.0x |
| Labels | Source name on each bubble |
| Tooltip | "[Source]: Leads [X] · ROI [Y]x · Spend ₹[Z] · Quadrant: [Name]" |
| API | `GET /api/v1/group/{id}/marketing/analytics/lead-source-roi/charts/efficiency-matrix/` |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Season filter changed | "Source ROI updated for season [Season]" | Info | 3s |
| Branch filter applied | "Showing source data for [Branch Name]" | Info | 3s |
| Export started | "Generating source ROI report — [Format]" | Info | 3s |
| Export complete | "Report downloaded — [Filename]" | Success | 3s |
| Export failed | "Export failed — please reduce date range or try again" | Error | 5s |
| Simulation saved | "Budget scenario '[Name]' saved" | Success | 3s |
| Simulation reset | "Allocation reset to current budget" | Info | 3s |
| Comparison loaded | "Comparing [N] sources" | Info | 3s |
| No data for filter | "No source data for selected filters" | Warning | 4s |
| Preset applied | "Preset '[Name]' applied — review projected changes" | Info | 3s |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| No source data this season | 📊 | "No Source Data Available" | "Lead source ROI analysis requires enquiry source tracking (O-16) and campaign spend data (O-09) to be populated." | View Enquiry Sources (O-16) |
| No data for selected branch | 🏫 | "No Source Data for This Branch" | "No leads with source attribution exist for the selected branch this season." | Clear Branch Filter |
| No multi-year data | 📈 | "Multi-Year Trend Unavailable" | "Source trend analysis requires at least 2 seasons of data. First-season groups will see trends from next year." | View Current Season |
| No diminishing returns detected | 🎯 | "All Sources Performing Well" | "No sources show significant CPL increases over the past 2+ seasons. Continue monitoring." | — |
| Simulator — no budget set | 💰 | "No Budget Data" | "Set the marketing budget in O-09 (Campaign Budget Manager) to use the reallocation simulator." | Go to Budget Manager (O-09) |
| No sources meet min spend filter | 🔍 | "No Sources Above Threshold" | "No sources meet the minimum spend threshold of ₹[X]. Lower the threshold to see more sources." | Reset Threshold |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | 6 KPI shimmer + tab bar + table skeleton (15 rows) |
| Tab switch | Content skeleton matching target tab |
| Source deep-dive drawer | 720px skeleton: overview card + 5 tabs |
| Season/branch filter change | KPI shimmer + table skeleton (data refresh) |
| Source comparison modal | Two-column skeleton with chart placeholder |
| Budget simulator modal | Table skeleton (15 rows) + slider placeholders + projection cards |
| Export generation | Spinner: "Generating report..." |
| Chart load | Grey canvas placeholder per chart |
| Multi-year trend load | Table skeleton with sparkline placeholders |
| Diminishing returns analysis | Table skeleton with severity badges |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/marketing/analytics/lead-source-roi/kpis/` | G1+ | KPI summary (6 cards) |
| GET | `/api/v1/group/{id}/marketing/analytics/lead-source-roi/sources/` | G1+ | Source-wise ROI table (paginated, filterable) |
| GET | `/api/v1/group/{id}/marketing/analytics/lead-source-roi/sources/{source_id}/` | G1+ | Source deep-dive data |
| GET | `/api/v1/group/{id}/marketing/analytics/lead-source-roi/sources/{source_id}/branches/` | G1+ | Branch breakdown for source |
| GET | `/api/v1/group/{id}/marketing/analytics/lead-source-roi/sources/{source_id}/quality/` | G1+ | Lead quality metrics for source |
| GET | `/api/v1/group/{id}/marketing/analytics/lead-source-roi/sources/{source_id}/trend/` | G1+ | Historical trend for source |
| GET | `/api/v1/group/{id}/marketing/analytics/lead-source-roi/sources/{source_id}/campaigns/` | G1+ | Campaigns using this source |
| GET | `/api/v1/group/{id}/marketing/analytics/lead-source-roi/multi-year/` | G1+ | Multi-year trend table |
| GET | `/api/v1/group/{id}/marketing/analytics/lead-source-roi/mix-analysis/` | G1+ | Source mix and HHI data |
| GET | `/api/v1/group/{id}/marketing/analytics/lead-source-roi/diminishing-returns/` | G1+ | Diminishing returns flagged sources |
| GET | `/api/v1/group/{id}/marketing/analytics/lead-source-roi/compare/` | G1+ | Source comparison (source_ids as params) |
| POST | `/api/v1/group/{id}/marketing/analytics/lead-source-roi/simulate/` | G1+ | Budget reallocation simulation |
| GET | `/api/v1/group/{id}/marketing/analytics/lead-source-roi/simulate/presets/` | G1+ | Simulation presets |
| POST | `/api/v1/group/{id}/marketing/analytics/lead-source-roi/export/` | G1+ | Generate export |
| GET | `/api/v1/group/{id}/marketing/analytics/lead-source-roi/charts/roi-bar/` | G1+ | ROI bar chart data |
| GET | `/api/v1/group/{id}/marketing/analytics/lead-source-roi/charts/cpl-cpa-scatter/` | G1+ | CPL vs CPA scatter data |
| GET | `/api/v1/group/{id}/marketing/analytics/lead-source-roi/charts/contribution-pie/` | G1+ | Contribution doughnut data |
| GET | `/api/v1/group/{id}/marketing/analytics/lead-source-roi/charts/yoy-trend/` | G1+ | YoY trend line data |
| GET | `/api/v1/group/{id}/marketing/analytics/lead-source-roi/charts/efficiency-matrix/` | G1+ | Efficiency matrix bubble data |

---

## 12. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load | Page load | `hx-get=".../lead-source-roi/kpis/"` | `#kpi-bar` | `innerHTML` | `hx-trigger="load"` |
| Tab switch | Tab click | `hx-get` with tab param | `#source-content` | `innerHTML` | `hx-trigger="click"` |
| Filter apply | Dropdown change | `hx-get` with filter params | `#tab-table-body` | `innerHTML` | `hx-trigger="change"` with 300ms debounce |
| Season change | Season dropdown | `hx-get` with season param | `#kpi-bar, #source-content` | `innerHTML` | Refreshes both KPIs and content |
| Branch filter | Branch dropdown | `hx-get` with branch_id | `#kpi-bar, #source-content` | `innerHTML` | Branch-scoped refresh |
| Source deep-dive | Row click | `hx-get=".../sources/{id}/"` | `#right-drawer` | `innerHTML` | `hx-trigger="click"` |
| Source compare | Compare form | `hx-get=".../compare/?ids={id1,id2,...}"` | `#compare-content` | `innerHTML` | Up to 4 sources |
| Simulator run | Slider/input change | `hx-post=".../simulate/"` | `#simulation-results` | `innerHTML` | `hx-trigger="change"` with 500ms debounce |
| Simulator preset | Preset button | `hx-get=".../simulate/presets/?type={t}"` | `#simulator-table` | `innerHTML` | Pre-fills allocation |
| Export trigger | Export button | `hx-post=".../export/"` | `#export-result` | `innerHTML` | Returns download link |
| Chart load | Tab/page load | `hx-get=".../charts/..."` | `#chart-{name}` | `innerHTML` | `hx-trigger="intersect once"` |
| Pagination | Page controls | `hx-get` with `?page={n}` | `#tab-table-body` | `innerHTML` | 25/page |
| Sort column | Header click | `hx-get` with `?sort={col}&dir={asc|desc}` | `#tab-table-body` | `innerHTML` | Preserves filters |
| Contribution toggle | Dropdown (Admissions/Leads/Spend) | `hx-get=".../charts/contribution-pie/?metric={m}"` | `#chart-contribution` | `innerHTML` | Switches pie chart metric |

---

*Page spec version: 1.0 · Last updated: 2026-03-26*
