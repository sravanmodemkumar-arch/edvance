# O-35 — Campaign Performance Analytics

> **URL:** `/group/marketing/analytics/campaign-performance/`
> **File:** `o-35-campaign-performance-analytics.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Role:** Group Admission Data Analyst (Role 132, G1) — primary operator

---

## 1. Purpose

The Campaign Performance Analytics page is the single most important analytics page in Division O — it answers the question every Group CEO asks at every board meeting: "We spent ₹4.8 crore on marketing this season — what did we get for it?" In the Indian education market, institution groups with 20-50 branches routinely spend ₹2-10 crore per admission season across newspaper ads, digital campaigns, WhatsApp blasts, outdoor hoardings, open days, referral incentives, and topper felicitation events. Yet most groups cannot connect a single rupee of marketing spend to a confirmed admission. The newspaper ad manager knows the ad cost ₹3.5 lakh. The telecaller knows 40 parents called mentioning the ad. But nobody knows how many of those 40 actually enrolled, paid fees, and sat in a classroom. This page closes that attribution gap.

The problems this page solves:

1. **No spend-to-enrollment attribution:** In a typical Indian education group, the marketing team tracks ad placements (O-10), the telecalling team tracks enquiries (O-18), the admissions team tracks applications (Division C), and the finance team tracks fee payments (Division D). These are four separate data silos. A parent sees a newspaper ad in Eenadu, calls the helpline, visits the Kukatpally branch, applies, and pays fees at the Secunderabad branch. Without campaign-level attribution, the newspaper ad gets zero credit. This page connects campaign spend (O-09) to leads generated (O-16) to applications submitted (Division C) to fees paid (Division D) — producing true cost-per-lead (CPL), cost-per-admission (CPA), and return-on-investment (ROI) for every campaign.

2. **Channel comparison blindness:** A group running newspaper ads (₹1.2 Cr), Google Ads (₹40L), WhatsApp blasts (₹8L), outdoor hoardings (₹60L), and referral programmes (₹20L) needs to know which channel delivers the cheapest admissions. In tier-2/3 cities, newspaper ads often outperform digital by 3x on CPA. In metros, digital outperforms newspaper by 2x. Without comparative analytics, groups over-invest in channels that "feel" effective but deliver poor ROI.

3. **Branch-level spend inefficiency:** In a 30-branch group, marketing budgets are often allocated evenly or by branch size, not by branch marketing efficiency. A Hyderabad branch with ₹50L budget might fill 95% seats (CPA = ₹2,800), while a Warangal branch with ₹30L budget fills only 60% seats (CPA = ₹8,500). CEOs need branch-level marketing efficiency data to reallocate budgets — but manually compiling this across 30 branches and 100+ campaigns is impossible without a system.

4. **Funnel drop-off invisibility:** A campaign generates 5,000 leads but only 200 admissions — a 4% conversion rate. Where did 4,800 leads drop off? Were they uncontactable (bad phone numbers from newspaper ads)? Did they visit but choose a competitor? Did they apply but not pay fees? The funnel visualization reveals exactly where each campaign leaks, enabling targeted intervention — more telecaller follow-ups at the contacted stage, better open-day experience at the visited stage, or fee instalment options at the payment stage.

5. **Year-over-year regression:** Without historical comparison, groups cannot detect that their newspaper ad CPL has risen from ₹180 to ₹340 over three years while WhatsApp CPL has dropped from ₹120 to ₹45. Trend analysis enables proactive budget reallocation before ROI deteriorates.

**Scale:** 150 groups × 50-300 campaigns per season × 5-8 channels × 5-50 branches per group · Season data: 5,000-2,00,000 leads per group · ₹2-10 Cr annual marketing spend · 7-year data retention for trend analysis

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Admission Data Analyst | 132 | G1 | Read + Export — view all analytics, download reports, schedule exports | Primary operator — builds and shares reports |
| Group Admissions Campaign Manager | 119 | G3 | Read — view campaign performance, drill into own campaigns | Uses data to optimise ongoing campaigns |
| Group Topper Relations Manager | 120 | G3 | Read — view topper campaign ROI only | Limited to topper-related campaign analytics |
| Group Admission Telecaller Executive | 130 | G3 | No access | Analytics not relevant to telecalling operations |
| Group Campaign Content Coordinator | 131 | G2 | No access | Content role, no analytics function |
| Group CEO / Chairman | — | G4/G5 | Read + Export — full access to all analytics, approve budget reallocation | Board-level decision maker; receives scheduled MIS |
| Branch Principal | — | G3 | Read (own branch) — view own branch's campaign performance only | Branch-scoped data via row-level security |

> **Access enforcement:** `@require_role(min_level=G1, division='O')`. Export permission: role 132 or G4+. Branch-scoped access: Branch Principals see only `WHERE branch_id = user.branch_id`. All data read-only — no CRUD operations on analytics pages. Scheduled report creation: role 132 or G4+.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  >  Marketing & Campaigns  >  Analytics & Reports  >  Campaign Performance Analytics
```

### 3.2 Page Header
```
Campaign Performance Analytics                    [Date Range: v]  [Season: v]  [Export v]  [Schedule Report]
Data Analyst — Priya Raghunandan
Sunrise Education Group · Season 2025-26 · 142 campaigns · ₹4.82 Cr spent · 68,420 leads · 12,860 admissions · Blended ROI: 3.2x
```

**Date range selector:** Pre-sets: This Month / This Quarter / This Season / Last Season / Custom Range. Default = Current Season.

---

## 4. KPI Summary Bar (6 cards)

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Total Marketing Spend | ₹ Amount (Cr/L) | SUM(campaign.actual_spend) WHERE season = selected AND group_id = current | Static blue | `#kpi-spend` |
| 2 | Total Leads Generated | Integer | COUNT(leads) WHERE source_campaign IS NOT NULL AND season = selected | Static blue | `#kpi-leads` |
| 3 | Total Admissions | Integer | COUNT(admissions) WHERE attributed_campaign IS NOT NULL AND season = selected | Static green | `#kpi-admissions` |
| 4 | Overall CPL | ₹ Amount | Total Marketing Spend / Total Leads | Green < ₹200, Amber ₹200-500, Red > ₹500 | `#kpi-cpl` |
| 5 | Overall CPA | ₹ Amount | Total Marketing Spend / Total Admissions | Green < ₹4,000, Amber ₹4,000-8,000, Red > ₹8,000 | `#kpi-cpa` |
| 6 | Blended ROI | Ratio (X.Xx) | (Total Admission Revenue Attributed / Total Marketing Spend) | Green > 3.0x, Amber 1.5-3.0x, Red < 1.5x | `#kpi-roi` |

**Threshold context (Indian education market):**
- CPL thresholds: Newspaper ₹150-400, Digital ₹80-250, WhatsApp ₹20-80, Referral ₹50-200, Walk-in ₹0 (organic)
- CPA thresholds: Budget school ₹1,500-3,000, Mid-range ₹3,000-6,000, Premium ₹5,000-12,000, Coaching ₹8,000-20,000
- ROI > 3x = healthy, 1.5-3x = acceptable, < 1.5x = marketing overspend

**HTMX:** `hx-get="/api/v1/group/{id}/marketing/analytics/campaign-performance/kpis/"` → `hx-trigger="load"`

---

## 5. Sections

### 5.1 Tab Navigation

Five tabs:
1. **Campaign-wise Performance** — All campaigns with spend, leads, enrollments, CPL, CPA, ROI
2. **Channel Comparison** — Aggregate performance by channel (newspaper, digital, WhatsApp, outdoor, referral, etc.)
3. **Branch-wise Efficiency** — Per-branch marketing spend vs fill rate and admissions
4. **Funnel Analysis** — Lead-to-admission funnel with drop-off at each stage
5. **Trend Analysis** — Time-series performance (monthly, quarterly, year-over-year)

### 5.2 Tab 1: Campaign-wise Performance

**Filter bar:** Season · Channel (Newspaper/Digital/WhatsApp/Outdoor/Referral/Open Day/Fair/Email/SMS/Other) · Branch (All/Specific) · Status (Active/Completed/Paused) · Date range · Budget range (₹)

| Column | Type | Sortable | Notes |
|---|---|---|---|
| # | Auto-index | No | — |
| Campaign Name | Text (link) | Yes | Click opens campaign deep-dive drawer |
| Channel | Badge | Yes | Newspaper / Digital / WhatsApp / Outdoor / Referral / Open Day / Fair / Email / SMS / Mixed |
| Branch(es) | Text | Yes | "All" or comma-separated branch names; tooltip shows full list |
| Duration | Date range | Yes | Start date – End date |
| Status | Badge | Yes | Active (green) / Completed (blue) / Paused (amber) |
| Budget (₹) | Amount | Yes | Allocated budget |
| Actual Spend (₹) | Amount | Yes | Actual spend; red if > 110% of budget |
| Leads | Integer | Yes | Total leads attributed to this campaign |
| Qualified Leads | Integer | Yes | Leads that progressed past initial contact |
| Admissions | Integer | Yes | Confirmed enrollments with fee payment |
| CPL (₹) | Amount | Yes | Actual Spend / Leads; colour-coded by threshold |
| CPA (₹) | Amount | Yes | Actual Spend / Admissions; colour-coded by threshold |
| Conversion % | Percentage | Yes | (Admissions / Leads) × 100 |
| ROI | Ratio | Yes | (Revenue from admitted students / Actual Spend); green > 3x, amber 1.5-3x, red < 1.5x |
| Actions | Buttons | No | [Deep Dive] [Compare] |

**Default sort:** ROI DESC (best-performing campaigns first)
**Pagination:** Server-side · 25/page
**Summary row:** Totals for spend, leads, admissions; weighted averages for CPL, CPA, ROI

**Indian context notes:**
- Newspaper campaigns: Track by publication (Eenadu, Sakshi, Deccan Chronicle), edition (city/state), and ad size (full-page/half-page/quarter). Different editions have vastly different CPLs — Hyderabad city edition of Eenadu generates 5x more leads than Nalgonda district edition at similar cost.
- Digital campaigns: Aggregated from O-11; Google Ads + Meta Ads + YouTube pre-roll counted separately. Attribution uses UTM parameters + landing page form submissions.
- WhatsApp campaigns: Tracked from O-12; leads = replies + link clicks. WhatsApp has the lowest CPL (₹20-80) but also the lowest conversion rate (1-3%) due to broadcast fatigue.
- Referral campaigns: Tracked from O-24; highest conversion rate (15-25%) because referrals come with built-in trust.

### 5.3 Tab 2: Channel Comparison

**Aggregate view — one row per channel:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Channel | Text (badge) | Yes | Newspaper / Digital / WhatsApp / Outdoor / Referral / Open Day / Fair / Email / SMS |
| # Campaigns | Integer | Yes | Count of campaigns in this channel |
| Total Spend (₹) | Amount | Yes | SUM(actual_spend) for channel |
| Spend Share % | Percentage | Yes | Channel spend / Total spend × 100 |
| Total Leads | Integer | Yes | SUM(leads) for channel |
| Lead Share % | Percentage | Yes | Channel leads / Total leads × 100 |
| Total Admissions | Integer | Yes | SUM(admissions) for channel |
| Admission Share % | Percentage | Yes | Channel admissions / Total admissions × 100 |
| Avg CPL (₹) | Amount | Yes | Channel total spend / Channel total leads |
| Avg CPA (₹) | Amount | Yes | Channel total spend / Channel total admissions |
| Conversion % | Percentage | Yes | Channel total admissions / Channel total leads × 100 |
| ROI | Ratio | Yes | Channel revenue / Channel spend |
| Efficiency Index | Score (0-100) | Yes | Composite: normalised(1/CPL) × 0.3 + normalised(conversion%) × 0.3 + normalised(ROI) × 0.4 |
| Trend | Sparkline | No | Mini line chart showing monthly CPL trend for this channel |

**Default sort:** Efficiency Index DESC
**No pagination** — typically 8-12 channels

**Key insight row:** Below the table, a highlighted recommendation box:
```
Recommendation: Newspaper CPL (₹285) is 3.6x higher than WhatsApp CPL (₹78), but Newspaper
conversion rate (8.2%) is 4.1x higher than WhatsApp (2.0%). Net CPA: Newspaper ₹3,475 vs
WhatsApp ₹3,900. Consider maintaining newspaper spend in tier-2 cities where it outperforms digital.
```
(Auto-generated from data — compares top 2 channels by spend, highlights CPL vs conversion tradeoff.)

### 5.4 Tab 3: Branch-wise Efficiency

**Filter bar:** Zone · Branch size (Small < 500, Medium 500-2000, Large > 2000 students) · Fill rate range

| Column | Type | Sortable | Notes |
|---|---|---|---|
| # | Auto-index | No | — |
| Branch | Text (link) | Yes | Click opens branch deep-dive |
| Zone | Text | Yes | If group uses zones (from Division A) |
| Seat Capacity | Integer | Yes | Total seats available for admission |
| Target Admissions | Integer | Yes | Admission target set by group |
| Actual Admissions | Integer | Yes | Confirmed enrollments |
| Fill Rate % | Progress bar | Yes | (Actual / Capacity) × 100; green ≥ 90%, amber 70-89%, red < 70% |
| Target Achievement % | Percentage | Yes | (Actual / Target) × 100 |
| Marketing Spend (₹) | Amount | Yes | Total spend on campaigns targeting this branch |
| CPL (₹) | Amount | Yes | Branch spend / Branch leads |
| CPA (₹) | Amount | Yes | Branch spend / Branch admissions |
| Marketing Efficiency Score | Score (0-100) | Yes | Composite: normalised(fill_rate) × 0.4 + normalised(1/CPA) × 0.3 + normalised(target_achievement) × 0.3 |
| Spend per Seat (₹) | Amount | Yes | Marketing Spend / Seat Capacity — marketing cost per seat regardless of fill |
| ROI | Ratio | Yes | Branch admission revenue / Branch marketing spend |
| Rank | Integer | Yes | Rank by Marketing Efficiency Score (1 = best) |
| Alert | Icon | No | Red flag if: CPA > 2× group average OR fill rate < 60% OR spend > 120% budget |

**Default sort:** Marketing Efficiency Score DESC (best branches first)
**Pagination:** Server-side · 30/page (most groups have < 50 branches)

**Branch performance tiers (auto-classified):**
- **Star Performers** (green badge): Efficiency Score ≥ 80, Fill Rate ≥ 90%
- **On Track** (blue badge): Efficiency Score 60-79, Fill Rate 75-89%
- **Needs Attention** (amber badge): Efficiency Score 40-59, Fill Rate 60-74%
- **Critical** (red badge): Efficiency Score < 40 OR Fill Rate < 60%

### 5.5 Tab 4: Funnel Analysis

**Filter bar:** Campaign (specific or all) · Channel · Branch · Date range

**Funnel table:**

| Stage | Count | Drop-off | Drop-off % | Cumulative Conversion | Notes |
|---|---|---|---|---|---|
| Leads Generated | 68,420 | — | — | 100% | Total leads from all campaigns |
| Contacted | 52,340 | 16,080 | 23.5% | 76.5% | Successfully reached by phone/WhatsApp |
| Interested | 31,200 | 21,140 | 40.4% | 45.6% | Expressed interest in admission |
| Walk-in / Open Day Visit | 18,750 | 12,450 | 39.9% | 27.4% | Visited branch physically |
| Application Submitted | 15,400 | 3,350 | 17.9% | 22.5% | Completed application form |
| Seat Offered | 14,200 | 1,200 | 7.8% | 20.8% | Offered admission in branch/stream |
| Fee Paid (Enrolled) | 12,860 | 1,340 | 9.4% | 18.8% | Confirmed enrollment with payment |

**Visual funnel:** Horizontal funnel bar chart showing progressive narrowing at each stage.

**Drop-off analysis per stage (expandable):**
- **Leads → Contacted (23.5% drop-off):** Reasons: Invalid phone (8%), Unreachable after 3 attempts (10%), Duplicate entry (5.5%)
- **Contacted → Interested (40.4% drop-off):** Reasons: Already admitted elsewhere (15%), Fee too high (12%), Location not convenient (8%), Wrong board/medium (5.4%)
- **Interested → Visit (39.9% drop-off):** Reasons: No follow-up within 48h (18%), Competitor visit scheduled first (12%), Distance concern (9.9%)
- **Visit → Application (17.9% drop-off):** Reasons: Infrastructure disappointed (6%), Chose competitor after comparison (8%), Delayed decision (3.9%)
- **Offer → Fee Paid (9.4% drop-off):** Reasons: Fee higher than expected (4%), Seat in preferred branch not available (3%), Financial difficulty (2.4%)

### 5.6 Tab 5: Trend Analysis

**Sub-tabs:** Monthly Trend · Quarterly Trend · YoY Comparison

**Monthly Trend table:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Month | Text | Yes | "Apr 2025", "May 2025", etc. |
| Spend (₹) | Amount | Yes | Total marketing spend in month |
| Leads | Integer | Yes | New leads generated |
| Admissions | Integer | Yes | Confirmed enrollments |
| CPL (₹) | Amount | Yes | Month spend / Month leads |
| CPA (₹) | Amount | Yes | Month spend / Month admissions |
| ROI | Ratio | Yes | Month revenue / Month spend |
| Top Channel | Text | No | Highest-ROI channel for the month |

**YoY Comparison table (seasons side-by-side):**

| Metric | 2023-24 | 2024-25 | 2025-26 | YoY Change | Trend |
|---|---|---|---|---|---|
| Total Spend | ₹3.6 Cr | ₹4.2 Cr | ₹4.8 Cr | +14.3% | Sparkline |
| Total Leads | 48,000 | 58,000 | 68,420 | +18.0% | Sparkline |
| Total Admissions | 9,200 | 11,100 | 12,860 | +15.9% | Sparkline |
| CPL | ₹750 | ₹724 | ₹705 | -2.6% | Sparkline |
| CPA | ₹39,130 | ₹37,838 | ₹37,481 | -0.9% | Sparkline |
| Blended ROI | 2.6x | 2.9x | 3.2x | +10.3% | Sparkline |

---

## 6. Drawers & Modals

### 6.1 Drawer: `campaign-deep-dive` (780px, right-slide)

- **Title:** "[Campaign Name] — Performance Deep Dive"
- **Tabs:** Overview · Leads · Funnel · Branch Split · Timeline · Attribution
- **Overview tab:**
  - Campaign card: name, channel, duration, status, budget vs actual spend
  - 6 mini-KPIs: Leads, Qualified Leads, Admissions, CPL, CPA, ROI
  - Channel-specific metrics:
    - Newspaper: publication, edition, ad size, insertion dates, response phone/code
    - Digital: platform (Google/Meta/YouTube), impressions, clicks, CTR, landing page URL
    - WhatsApp: messages sent, delivered, read, replied, link clicks
    - Outdoor: location count, estimated impressions, duration
    - Referral: referrers count, referral-to-admission rate
- **Leads tab:** List of all leads attributed to this campaign with current stage, branch, contact, and last action date
- **Funnel tab:** Campaign-specific funnel (same structure as Tab 4) — show where THIS campaign's leads drop off
- **Branch Split tab:** If campaign targets multiple branches, show per-branch breakdown: leads, admissions, CPL, CPA
- **Timeline tab:** Day-by-day or week-by-week lead generation trend; identifies peak response days (useful for newspaper ads — response spikes 1-2 days after insertion)
- **Attribution tab:** Attribution model applied (first-touch, last-touch, multi-touch); leads with multi-campaign touchpoints; co-attributed campaigns
- **Footer:** [Export Campaign Report] [Compare with Another Campaign] [View in O-08]
- **Access:** Role 132, 119, or G4+

### 6.2 Drawer: `channel-attribution` (640px, right-slide)

- **Title:** "Channel Attribution Analysis"
- **Sections:**
  - **Attribution model selector:** First-touch (default) / Last-touch / Linear (multi-touch) / Time-decay
    - First-touch: 100% credit to first campaign that generated the lead
    - Last-touch: 100% credit to last campaign before enrollment
    - Linear: Equal credit split across all touchpoints
    - Time-decay: More credit to recent touchpoints (half-life = 7 days)
  - **Model comparison table:** Shows how CPA changes under each attribution model for top 5 channels
  - **Multi-touch path analysis:** Most common conversion paths:
    - Newspaper Ad → Telecall → Open Day → Enrolled (28% of admissions)
    - WhatsApp Blast → Walk-in → Enrolled (18% of admissions)
    - Referral → Walk-in → Enrolled (15% of admissions)
    - Digital Ad → WhatsApp Follow-up → Open Day → Enrolled (12% of admissions)
  - **Assisted conversions:** Campaigns that appear in conversion paths but are not the primary source — "WhatsApp assisted 4,200 conversions even when not the primary source"
- **Footer:** [Apply Model] [Export Attribution Report]
- **Access:** Role 132 or G4+

### 6.3 Modal: `custom-date-range` (480px)

- **Title:** "Custom Date Range"
- **Fields:**
  - Start date (date picker, required)
  - End date (date picker, required)
  - Compare with (toggle): Previous period / Same period last year / Custom comparison range
  - Comparison start date (date picker, conditional)
  - Comparison end date (date picker, conditional)
- **Quick presets:** Last 7 days / Last 30 days / Last 90 days / This admission season / Last admission season / Full financial year
- **Validation:** End date > Start date; maximum range 3 years; comparison range must be same duration
- **Buttons:** Cancel · Apply
- **Access:** All roles with page access

### 6.4 Modal: `export-schedule-report` (560px)

- **Title:** "Export / Schedule Report"
- **Sections:**
  - **Export now:**
    - Format: CSV / Excel (XLSX) / PDF
    - Data scope: Current tab data / All tabs / Custom selection
    - Include charts: Yes/No (PDF only)
    - Date range applied: [shows current filter]
  - **Schedule recurring:**
    - Frequency: Daily / Weekly (select day) / Monthly (select date) / Quarterly
    - Recipients: Email addresses (multi-input — auto-suggest from group users)
    - Format: Excel / PDF
    - Report sections: Checkboxes for each tab/section to include
    - Active: Toggle on/off
  - **Existing schedules:** Table showing active scheduled reports with frequency, recipients, next run date, [Edit] [Delete] buttons
- **Buttons:** Cancel · Export Now · Save Schedule
- **Access:** Role 132 or G4+

### 6.5 Modal: `campaign-compare` (720px)

- **Title:** "Compare Campaigns"
- **Selection:** Two campaign dropdowns (search by name, filter by channel/season)
- **Comparison table:**
  - Side-by-side metrics: Spend, Leads, Admissions, CPL, CPA, ROI, Conversion %, Duration, Channel
  - Delta column showing difference (absolute and percentage)
  - Winner indicator (green highlight on better metric)
- **Comparison chart:** Grouped bar chart — both campaigns' metrics side by side
- **Buttons:** Close · Swap Campaigns · Export Comparison
- **Access:** Role 132, 119, or G4+

---

## 7. Charts

### 7.1 Campaign ROI Waterfall (Bar)

| Property | Value |
|---|---|
| Chart type | Horizontal bar (Chart.js 4.x) — sorted by ROI DESC |
| Title | "Campaign ROI — Top 20 Campaigns" |
| Data | Top 20 campaigns by ROI; bar length = ROI value; bar label = campaign name |
| Colour | Green (ROI > 3x), Amber (1.5-3x), Red (< 1.5x) |
| Tooltip | "[Campaign]: ROI [X]x · Spend ₹[Y] · Admissions [Z] · CPA ₹[W]" |
| Annotation | Vertical line at ROI = 3.0x (target threshold) |
| API | `GET /api/v1/group/{id}/marketing/analytics/campaign-performance/charts/roi-waterfall/` |

### 7.2 Channel Comparison Radar (Radar)

| Property | Value |
|---|---|
| Chart type | Radar / spider chart (Chart.js 4.x) |
| Title | "Channel Performance Comparison" |
| Data | One polygon per channel; axes: Lead Volume (normalised), Conversion %, 1/CPL (cost efficiency), ROI, Lead Quality Score |
| Colour | Newspaper `#3B82F6`, Digital `#8B5CF6`, WhatsApp `#10B981`, Outdoor `#F59E0B`, Referral `#EC4899`, Open Day `#14B8A6` |
| Tooltip | "[Channel] — [Axis]: [Value]" |
| API | `GET /api/v1/group/{id}/marketing/analytics/campaign-performance/charts/channel-radar/` |

### 7.3 CPL Trend Line (Line)

| Property | Value |
|---|---|
| Chart type | Multi-line (Chart.js 4.x) |
| Title | "Cost Per Lead — Monthly Trend by Channel" |
| Data | X = month (Apr–Mar), Y = CPL (₹); one line per channel |
| Colour | Same channel palette as radar chart |
| Annotation | Horizontal dashed line at group average CPL |
| Tooltip | "[Month] — [Channel]: CPL ₹[X] ([+/-Y]% vs prev month)" |
| API | `GET /api/v1/group/{id}/marketing/analytics/campaign-performance/charts/cpl-trend/` |

### 7.4 Branch Efficiency Scatter (Scatter)

| Property | Value |
|---|---|
| Chart type | Scatter / bubble (Chart.js 4.x) |
| Title | "Branch Marketing Efficiency — Spend vs Fill Rate" |
| Data | X = Marketing Spend (₹L), Y = Fill Rate (%); bubble size = total admissions |
| Colour | Green (Efficiency Score ≥ 80), Amber (60-79), Red (< 60) |
| Quadrants | Top-left: "Low spend, high fill" (ideal) · Top-right: "High spend, high fill" (good) · Bottom-left: "Low spend, low fill" (needs more budget) · Bottom-right: "High spend, low fill" (inefficient) |
| Labels | Branch names on each point |
| Tooltip | "[Branch]: Spend ₹[X]L · Fill [Y]% · CPA ₹[Z] · Admissions [W]" |
| API | `GET /api/v1/group/{id}/marketing/analytics/campaign-performance/charts/branch-scatter/` |

### 7.5 Conversion Funnel (Funnel / Horizontal Stacked Bar)

| Property | Value |
|---|---|
| Chart type | Horizontal stacked bar rendered as funnel (Chart.js 4.x + custom plugin) |
| Title | "Lead-to-Admission Funnel" |
| Data | Stages: Lead → Contacted → Interested → Visited → Applied → Offered → Enrolled; width proportional to count |
| Colour | Progressive gradient: light blue (Lead) → dark green (Enrolled); drop-off shown in grey |
| Labels | Stage name + count + percentage of total |
| Tooltip | "[Stage]: [N] ([X]% of leads) · Drop-off: [Y] ([Z]%)" |
| API | `GET /api/v1/group/{id}/marketing/analytics/campaign-performance/charts/funnel/` |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Date range applied | "Analytics updated for [Start] to [End]" | Info | 3s |
| Export started | "Exporting campaign performance report — [Format]" | Info | 3s |
| Export complete | "Report downloaded — [Filename]" | Success | 3s |
| Export failed | "Export failed — try again or reduce date range" | Error | 5s |
| Schedule created | "Report scheduled — [Frequency] to [N] recipients" | Success | 4s |
| Schedule updated | "Report schedule updated" | Success | 3s |
| Schedule deleted | "Report schedule '[Name]' removed" | Warning | 3s |
| Attribution model changed | "Attribution recalculated using [Model] model" | Info | 3s |
| Campaign compare loaded | "Comparing '[Campaign A]' vs '[Campaign B]'" | Info | 3s |
| No data for filter | "No campaign data found for selected filters" | Warning | 4s |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| No campaigns this season | 📊 | "No Campaign Data Yet" | "Campaign performance analytics will appear here once campaigns are created in O-08 and leads start flowing through the pipeline." | View Campaign Builder (O-08) |
| No data for selected filters | 🔍 | "No Matching Data" | "No campaigns match the selected channel, branch, or date range. Adjust filters to see results." | Clear Filters |
| No admissions attributed | 📉 | "No Attributed Admissions" | "Leads exist but no admissions have been attributed to campaigns yet. Ensure the admissions pipeline (Division C) is connected and fee payments are recorded." | Check Pipeline (O-15) |
| No trend data (first season) | 📈 | "Trend Data Unavailable" | "Year-over-year trends require at least 2 seasons of data. Current season data will appear in monthly view." | View Monthly Trend |
| No scheduled reports | 📅 | "No Scheduled Reports" | "Schedule automated reports to receive campaign performance updates by email." | Create Schedule |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | 6 KPI shimmer + tab bar + table skeleton (15 rows) |
| Tab switch | Content skeleton matching target tab layout |
| Campaign deep-dive drawer | 780px skeleton: KPI cards + 6 tabs + table placeholder |
| Channel attribution drawer | 640px skeleton: model selector + table + path diagram |
| Date range change | KPI shimmer + table skeleton (data refresh) |
| Export generation | Spinner: "Generating [Format] report..." with progress indicator |
| Chart load | Grey canvas placeholder per chart (load on `intersect once`) |
| Funnel visualization | Horizontal bar skeleton (7 rows) |
| YoY comparison load | Table skeleton with sparkline placeholders |
| Campaign compare modal | Two-column skeleton with chart placeholder |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/marketing/analytics/campaign-performance/kpis/` | G1+ | KPI summary (6 cards) |
| GET | `/api/v1/group/{id}/marketing/analytics/campaign-performance/campaigns/` | G1+ | Campaign-wise performance table (paginated, filterable) |
| GET | `/api/v1/group/{id}/marketing/analytics/campaign-performance/campaigns/{campaign_id}/` | G1+ | Single campaign deep-dive data |
| GET | `/api/v1/group/{id}/marketing/analytics/campaign-performance/campaigns/{campaign_id}/leads/` | G1+ | Leads attributed to campaign |
| GET | `/api/v1/group/{id}/marketing/analytics/campaign-performance/campaigns/{campaign_id}/funnel/` | G1+ | Campaign-specific funnel |
| GET | `/api/v1/group/{id}/marketing/analytics/campaign-performance/campaigns/{campaign_id}/branch-split/` | G1+ | Branch breakdown for campaign |
| GET | `/api/v1/group/{id}/marketing/analytics/campaign-performance/campaigns/{campaign_id}/timeline/` | G1+ | Day/week-wise lead trend for campaign |
| GET | `/api/v1/group/{id}/marketing/analytics/campaign-performance/channels/` | G1+ | Channel comparison aggregate |
| GET | `/api/v1/group/{id}/marketing/analytics/campaign-performance/branches/` | G1+ | Branch-wise efficiency table |
| GET | `/api/v1/group/{id}/marketing/analytics/campaign-performance/funnel/` | G1+ | Overall funnel (all campaigns) |
| GET | `/api/v1/group/{id}/marketing/analytics/campaign-performance/trend/monthly/` | G1+ | Monthly trend data |
| GET | `/api/v1/group/{id}/marketing/analytics/campaign-performance/trend/yoy/` | G1+ | Year-over-year comparison |
| GET | `/api/v1/group/{id}/marketing/analytics/campaign-performance/attribution/` | G1+ | Attribution analysis (model param) |
| GET | `/api/v1/group/{id}/marketing/analytics/campaign-performance/compare/` | G1+ | Campaign comparison (two campaign_ids as params) |
| POST | `/api/v1/group/{id}/marketing/analytics/campaign-performance/export/` | G1+ | Generate export (format, scope params) |
| GET | `/api/v1/group/{id}/marketing/analytics/campaign-performance/schedules/` | G1+ | List scheduled reports |
| POST | `/api/v1/group/{id}/marketing/analytics/campaign-performance/schedules/` | G1+ | Create scheduled report |
| PUT | `/api/v1/group/{id}/marketing/analytics/campaign-performance/schedules/{schedule_id}/` | G1+ | Update schedule |
| DELETE | `/api/v1/group/{id}/marketing/analytics/campaign-performance/schedules/{schedule_id}/` | G1+ | Delete schedule |
| GET | `/api/v1/group/{id}/marketing/analytics/campaign-performance/charts/roi-waterfall/` | G1+ | ROI waterfall chart data |
| GET | `/api/v1/group/{id}/marketing/analytics/campaign-performance/charts/channel-radar/` | G1+ | Channel radar chart data |
| GET | `/api/v1/group/{id}/marketing/analytics/campaign-performance/charts/cpl-trend/` | G1+ | CPL trend line data |
| GET | `/api/v1/group/{id}/marketing/analytics/campaign-performance/charts/branch-scatter/` | G1+ | Branch scatter chart data |
| GET | `/api/v1/group/{id}/marketing/analytics/campaign-performance/charts/funnel/` | G1+ | Funnel visualization data |

---

## 12. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load | Page load | `hx-get=".../campaign-performance/kpis/"` | `#kpi-bar` | `innerHTML` | `hx-trigger="load"` |
| Tab switch | Tab click | `hx-get` with tab param | `#analytics-content` | `innerHTML` | `hx-trigger="click"` |
| Filter apply | Dropdown change | `hx-get` with filter params | `#tab-table-body` | `innerHTML` | `hx-trigger="change"` with 300ms debounce |
| Date range apply | Modal submit | `hx-get` with date params | `#kpi-bar, #analytics-content` | `innerHTML` | Refreshes both KPIs and current tab |
| Campaign deep-dive | Row click | `hx-get=".../campaigns/{id}/"` | `#right-drawer` | `innerHTML` | `hx-trigger="click"` |
| Channel attribution | Button click | `hx-get=".../attribution/"` | `#right-drawer` | `innerHTML` | Includes model param |
| Attribution model change | Model dropdown | `hx-get=".../attribution/?model={m}"` | `#attribution-content` | `innerHTML` | `hx-trigger="change"` |
| Campaign compare | Compare form | `hx-get=".../compare/?a={id1}&b={id2}"` | `#compare-content` | `innerHTML` | — |
| Export trigger | Export button | `hx-post=".../export/"` | `#export-result` | `innerHTML` | Returns download link |
| Schedule save | Schedule form | `hx-post=".../schedules/"` | `#schedule-list` | `innerHTML` | Toast on success |
| Chart load | Tab/page load | `hx-get=".../charts/..."` | `#chart-{name}` | `innerHTML` | `hx-trigger="intersect once"` |
| Pagination | Page controls | `hx-get` with `?page={n}` | `#tab-table-body` | `innerHTML` | 25/page |
| Sort column | Header click | `hx-get` with `?sort={col}&dir={asc|desc}` | `#tab-table-body` | `innerHTML` | Preserves filters |
| Funnel drill-down | Stage click | `hx-get=".../funnel/?stage={s}"` | `#funnel-detail` | `innerHTML` | Expands drop-off reasons |

---

*Page spec version: 1.0 · Last updated: 2026-03-26*
