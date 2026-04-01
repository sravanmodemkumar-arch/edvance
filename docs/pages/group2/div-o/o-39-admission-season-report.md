# O-39 — Admission Season Report

> **URL:** `/group/marketing/analytics/season-report/`
> **File:** `o-39-admission-season-report.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Role:** Group Admission Data Analyst (Role 132, G1) — primary author and compiler

---

## 1. Purpose

The Admission Season Report is the single most consequential document the marketing team produces each year — a comprehensive, board-presentation-quality consolidated analysis of the entire admission season (September to August) covering targets versus actuals, channel effectiveness, financial ROI, branch performance rankings, offer/discount impact, referral outcomes, key wins, critical losses, and actionable recommendations for the next season. This is THE report that the CEO presents at the annual trust meeting or board of directors meeting, and its findings directly determine next year's marketing budget (typically ₹2–10 Cr for a large group), staffing decisions (hire 5 more telecallers or reduce to 3?), branch expansion plans (open Kompally branch or consolidate Mehdipatnam?), and strategic pivots (shift from newspaper to digital, or double down on WhatsApp?).

The problems this page solves:

1. **Data scattered across 15+ pages:** Season data lives in O-08 (Campaign Builder), O-09 (Budget Manager), O-15 (Lead Pipeline), O-20 (Conversion Tracker), O-22 (Enrollment Drive), O-35 (Campaign Performance), O-36 (Lead Source ROI), and O-37 (Branch Comparison). Without a consolidation engine, the Data Analyst spends 3 weeks in August manually pulling data from each page, reconciling numbers, and building PowerPoint slides. The Season Report auto-aggregates from all source pages into a single unified document.

2. **Inconsistent narratives:** The branch principal says "We exceeded target by 5%." The marketing team says "Branch filled only 88% of seats." The finance team says "Revenue fell short by ₹40L." These contradictions arise because each stakeholder uses different baselines, different date cutoffs, and different definitions of "target." The Season Report establishes a single source of truth with locked definitions: target = Board-approved seat count as of September, actual = confirmed enrollment as of July 31, fill rate = actual/target × 100.

3. **Year-over-Year amnesia:** Every September, the new marketing plan is built from scratch because nobody remembers what worked last year. Did newspaper ads in Eenadu generate better ROI than Deccan Chronicle? Did the early-bird discount actually accelerate enrollments or just shift them forward? The Season Report's YoY comparison section preserves institutional memory, and the recommendation engine surfaces patterns spanning 3–5 seasons.

4. **Board presentation panic:** Two days before the annual trust meeting, the CEO asks for "the marketing report." The Data Analyst scrambles to format Excel data into presentable slides. The Season Report solves this by maintaining a continuously updated draft that can be exported as a polished PDF at any time — board-ready with charts, tables, commentary, and branding.

5. **Accountability gaps:** Without a structured season review, underperforming branches escape scrutiny ("We had a tough catchment") while overperforming branches get no recognition. The report's branch-wise ranking, exception reporting (branches below 80% fill), and comparative analysis create transparency that drives accountability.

**Scale:** 1 report per season · covers 5–50 branches · 5,000–50,000 enrollment records · 12 months of campaign data · ₹10L–₹10Cr marketing spend · exportable as 15–30 page PDF · YoY comparison across 3–5 seasons

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Admission Data Analyst | 132 | G1 | Full CRUD — compile, annotate, configure sections, generate report, export | Primary author |
| Group Admissions Campaign Manager | 119 | G3 | Read + Annotate — view report, add commentary on campaign sections | Contributes campaign narrative |
| Group Topper Relations Manager | 120 | G3 | Read — view topper-impact sections of the report | Reference for topper-related outcomes |
| Group Admission Telecaller Executive | 130 | G3 | Read (own metrics) — view telecalling performance section | Self-assessment reference |
| Group Campaign Content Coordinator | 131 | G2 | Read — view creative performance section | Content effectiveness reference |
| Group CEO / Chairman | — | G4/G5 | Read + Approve + Export — final review, approve for Board presentation, PDF export | Ultimate consumer; presents to Board/Trust |

> **Access enforcement:** `@require_role(min_level=G1, division='O')`. Report compilation/editing: role 132 or G4+. Annotation: roles 119, 132, G4+. Approval for Board distribution: G4/G5 only. PDF export: G1+ (draft), G4+ (final approved version).

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  >  Marketing & Campaigns  >  Analytics & Reports  >  Admission Season Report
```

### 3.2 Page Header
```
Admission Season Report                               [Season: 2025-26 ▼]  [Generate Report]  [Annotations]  [Export PDF]
Data Analyst — Priya Venkatesh
Sunrise Education Group · Season 2025-26 · Report Status: Draft · Last compiled: 25 Mar 2026 · 28 branches
```

---

## 4. KPI Summary Bar (6 cards)

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Season Fill Rate % | Percentage | (Total enrolled / Total target seats) × 100 across all branches | Green ≥ 90%, Amber 75–89%, Red < 75% | `#kpi-fill-rate` |
| 2 | Total Enrollment | Integer | SUM(confirmed_enrollment) WHERE season = selected | Static blue | `#kpi-enrollment` |
| 3 | Total Marketing Spend | ₹ Amount | SUM(actual_spend) across all campaigns for the season | Static blue | `#kpi-spend` |
| 4 | Season ROI | Ratio | (Total tuition revenue from new admissions − Total marketing spend) / Total marketing spend | Green ≥ 5x, Amber 2–5x, Red < 2x | `#kpi-roi` |
| 5 | Seats Unfilled | Integer | Total target seats − Total enrolled | Red > 500, Amber 100–500, Green < 100 | `#kpi-unfilled` |
| 6 | Revenue at Risk | ₹ Amount | Seats unfilled × Average annual fee per seat | Red > ₹1Cr, Amber ₹25L–₹1Cr, Green < ₹25L | `#kpi-revenue-risk` |

**HTMX:** `hx-get="/api/v1/group/{id}/marketing/analytics/season-report/kpis/?season={season_id}"` → `hx-trigger="load"`

---

## 5. Sections

### 5.1 Tab Navigation

Six tabs:
1. **Executive Summary** — Top-level season overview for CEO/Board
2. **Branch Performance** — Branch-wise targets, actuals, rankings
3. **Channel Analysis** — Source/channel effectiveness and ROI
4. **Financial Summary** — Spend breakdown, ROI, CPL, CPA
5. **Key Outcomes** — Wins, losses, offer impact, referral impact
6. **Recommendations** — Next-season action items and strategy suggestions

### 5.2 Tab 1: Executive Summary

Auto-generated narrative panel + KPI cards + headline charts. Designed to be the first 2 pages of the exported PDF.

**Sections within:**

#### 5.2.1 Season Headline
```
SEASON 2025-26 — ADMISSION REPORT
Sunrise Education Group

Overall Fill Rate: 91.4% (Target: 18,500 seats · Enrolled: 16,909)
Total Marketing Spend: ₹3,42,00,000
Season ROI: 6.2x
Best Branch: Kukatpally (98.2% fill)
Weakest Branch: Mehdipatnam (71.3% fill)
YoY Improvement: +3.2% fill rate vs 2024-25
```

#### 5.2.2 Season Summary Table

| Metric | Target | Actual | Variance | YoY (Previous Season) | YoY Change |
|---|---|---|---|---|---|
| Total Seats | 18,500 | — | — | 17,200 | +7.6% |
| Enrolled | — | 16,909 | −1,591 | 15,180 | +11.4% |
| Fill Rate | 95% | 91.4% | −3.6% | 88.3% | +3.1% |
| Total Leads | — | 52,340 | — | 44,200 | +18.4% |
| Lead-to-Enrollment | — | 32.3% | — | 34.3% | −2.0% |
| Marketing Spend (₹) | 3,50,00,000 | 3,42,00,000 | −8,00,000 | 2,95,00,000 | +15.9% |
| CPL (₹) | — | 653 | — | 667 | −2.1% |
| CPA (₹) | — | 2,023 | — | 1,943 | +4.1% |
| Revenue from New Admissions (₹) | — | 21,46,00,000 | — | 18,22,00,000 | +17.8% |
| ROI | — | 6.2x | — | 6.1x | +0.1 |

#### 5.2.3 Monthly Enrollment Progress

Inline area chart showing cumulative enrollment over 12 months (Sep–Aug) with target line overlay.

### 5.3 Tab 2: Branch Performance

**Filter bar:** Zone · City · Fill rate range · Performance band (Exceeded Target / Met Target / Below Target / Critical)

| Column | Type | Sortable | Notes |
|---|---|---|---|
| # | Auto-index | No | — |
| Branch | Text (link) | Yes | Click → branch detail sub-panel |
| City | Text | Yes | — |
| Zone | Badge | Yes | North / South / East / West / Central (if zoned) |
| Target Seats | Integer | Yes | Board-approved seat count |
| Enrolled | Integer | Yes | Confirmed enrollment as of season end |
| Fill Rate % | Progress bar | Yes | Enrolled / Target × 100 |
| Performance Band | Badge | Yes | Exceeded (green, ≥ 100%) / Met (blue, 90–99%) / Below (amber, 75–89%) / Critical (red, < 75%) |
| Marketing Spend (₹) | Amount | Yes | Branch-allocated spend |
| CPL (₹) | Amount | Yes | Cost per lead for this branch |
| CPA (₹) | Amount | Yes | Cost per admission |
| Branch ROI | Ratio | Yes | Revenue from new admissions / Marketing spend |
| Top Source | Text | No | Best-performing lead source for this branch |
| YoY Change | Percentage | Yes | Fill rate change vs previous season |
| Rank | Integer | Yes | Rank among all branches (by fill rate) |

**Default sort:** Rank ASC (best performing first)
**Pagination:** None — show all branches (max 50)

**Summary row:** Group totals / averages for each numeric column

**Branch detail sub-panel** (expands below row): Monthly enrollment trend, source breakdown, key observations, principal's commentary (if annotated).

### 5.4 Tab 3: Channel Analysis

**Source effectiveness summary table:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Source / Channel | Text | Yes | Newspaper / Digital Ads / WhatsApp / Walk-in / Referral / Open Day / Fair / Telecalling / Social Media / Website / Other |
| Leads Generated | Integer | Yes | Total leads from this source |
| Lead Share % | Percentage | Yes | This source's leads / Total leads |
| Conversions | Integer | Yes | Leads that converted to enrollment |
| Conversion Rate % | Percentage | Yes | Conversions / Leads |
| Spend (₹) | Amount | Yes | Amount spent on this channel |
| CPL (₹) | Amount | Yes | Spend / Leads |
| CPA (₹) | Amount | Yes | Spend / Conversions |
| Revenue (₹) | Amount | Yes | Estimated first-year revenue from these admissions |
| ROI | Ratio | Yes | Revenue / Spend |
| YoY Leads Change | Percentage | Yes | vs previous season |
| YoY ROI Change | Percentage | Yes | vs previous season |
| Verdict | Badge | Yes | Scale Up (green) / Maintain (blue) / Optimise (amber) / Reduce (red) |

**Below table:** Channel effectiveness radar chart (Section 7.2) + Channel trend lines

### 5.5 Tab 4: Financial Summary

#### 5.5.1 Spend Breakdown

| Budget Category | Budgeted (₹) | Actual (₹) | Variance (₹) | Variance % | YoY Actual (₹) | YoY Change |
|---|---|---|---|---|---|---|
| Newspaper & Print Ads | 1,20,00,000 | 1,15,00,000 | −5,00,000 | −4.2% | 1,05,00,000 | +9.5% |
| Digital Advertising | 80,00,000 | 85,00,000 | +5,00,000 | +6.3% | 60,00,000 | +41.7% |
| WhatsApp / SMS | 15,00,000 | 14,50,000 | −50,000 | −3.3% | 12,00,000 | +20.8% |
| Outdoor / BTL | 45,00,000 | 42,00,000 | −3,00,000 | −6.7% | 40,00,000 | +5.0% |
| Events & Open Days | 30,00,000 | 32,00,000 | +2,00,000 | +6.7% | 25,00,000 | +28.0% |
| Topper Felicitation | 25,00,000 | 22,50,000 | −2,50,000 | −10.0% | 20,00,000 | +12.5% |
| Branding & Materials | 20,00,000 | 18,00,000 | −2,00,000 | −10.0% | 18,00,000 | 0% |
| Telecalling Operations | 15,00,000 | 13,00,000 | −2,00,000 | −13.3% | 15,00,000 | −13.3% |
| **TOTAL** | **3,50,00,000** | **3,42,00,000** | **−8,00,000** | **−2.3%** | **2,95,00,000** | **+15.9%** |

#### 5.5.2 Key Financial Metrics

| Metric | Value | Benchmark | Assessment |
|---|---|---|---|
| Cost Per Lead (CPL) | ₹653 | Industry avg ₹800–1,200 | Below average — efficient |
| Cost Per Admission (CPA) | ₹2,023 | Industry avg ₹3,000–5,000 | Below average — efficient |
| Revenue per Marketing Rupee | ₹6.27 | Target ≥ ₹5.00 | Above target |
| Marketing Spend as % of Revenue | 1.59% | Industry norm 3–5% | Well below norm |
| First-Year Revenue from New Admissions | ₹21.46 Cr | Target ₹22 Cr | 97.5% of target |

### 5.6 Tab 5: Key Outcomes

#### 5.6.1 Key Wins
Editable list (textarea per item — analyst adds narrative):
- "Kukatpally branch exceeded target by 32 seats — driven by WhatsApp campaign targeting IT corridor parents"
- "Digital ad ROI improved 41.7% YoY — shift from broad-match to pin-code-targeted Google Ads"
- "Referral programme generated 1,240 admissions (7.3% of total) at ₹0 acquisition cost"

#### 5.6.2 Key Losses
- "Mehdipatnam branch filled only 71.3% — new Narayana branch opened 1.5 km away in October"
- "Newspaper ad ROI declined 8% — readership shifting to digital, but parent generation still reads print"
- "Lead-to-enrollment conversion dropped 2% despite 18% more leads — quality issue from broad digital targeting"

#### 5.6.3 Offer & Discount Impact

| Offer Type | Applications | Conversions | Revenue Forgone (₹) | Estimated Revenue Gained (₹) | Net Impact |
|---|---|---|---|---|---|
| Early-bird (10% off before Dec 31) | 3,200 | 2,800 | 28,00,000 | 2,24,00,000 | +₹1,96,00,000 |
| Sibling discount (5% second child) | 840 | 780 | 3,90,000 | 62,40,000 | +₹58,50,000 |
| Scholarship (merit-based fee waiver) | 1,200 | 950 | 47,50,000 | 76,00,000 | +₹28,50,000 |
| Staff referral bonus (₹2,000/admission) | 620 | 620 | 12,40,000 | 49,60,000 | +₹37,20,000 |

#### 5.6.4 Referral Impact Summary

| Referral Source | Referrals | Conversions | Conversion Rate | Value |
|---|---|---|---|---|
| Parent referral | 2,400 | 1,240 | 51.7% | ₹9.92 Cr |
| Alumni referral | 380 | 180 | 47.4% | ₹1.44 Cr |
| Staff referral | 820 | 620 | 75.6% | ₹4.96 Cr |
| **Total** | **3,600** | **2,040** | **56.7%** | **₹16.32 Cr** |

### 5.7 Tab 6: Recommendations

Structured recommendation entries — analyst drafts, G4/G5 approves/prioritises for next season:

| # | Category | Recommendation | Priority | Estimated Impact | Status |
|---|---|---|---|---|---|
| 1 | Budget | Increase digital ad budget by 30% (₹85L → ₹1.1Cr) — best ROI channel | High | +800 leads, +250 admissions | Pending Approval |
| 2 | Branch | Deploy dedicated telecaller for Mehdipatnam — branch needs 2x lead flow to counter Narayana | High | +15% fill rate | Pending Approval |
| 3 | Channel | Reduce newspaper frequency in Hyderabad by 20% — shift to hyperlocal WhatsApp targeting | Medium | Save ₹23L, maintain lead volume | Draft |
| 4 | Process | Implement automated lead scoring in O-15 — 35% of telecaller time wasted on unqualified leads | Medium | +12% telecaller productivity | Draft |
| 5 | Content | Create video testimonials for top 50 parents — WhatsApp video shares convert 3x better than text | Low | +500 video-influenced leads | Draft |

**Fields per recommendation:**
- Category (dropdown): Budget / Branch / Channel / Process / Content / Staffing / Technology / Expansion
- Recommendation (textarea)
- Supporting data (text — reference specific metrics)
- Priority (dropdown): High / Medium / Low
- Estimated impact (text)
- Status (dropdown): Draft / Pending Approval / Approved / Rejected / Deferred
- CEO comments (textarea — G4/G5 only)

---

## 6. Drawers & Modals

### 6.1 Modal: `season-selector` (480px)

- **Title:** "Select Season for Report"
- **Fields:**
  - Season (dropdown, required): 2025-26 / 2024-25 / 2023-24 / 2022-23 / 2021-22
  - Comparison season (dropdown, optional — for YoY): defaults to previous season
  - Date range override (toggle — advanced): custom start/end date instead of standard Sep–Aug
- **Info:** Shows data availability indicator per season: "2025-26: 92% data available (Branch Mehdipatnam pending final enrollment confirmation)"
- **Buttons:** Cancel · Load Season
- **Access:** G1+

### 6.2 Modal: `report-builder` (640px)

- **Title:** "Configure Season Report Sections"
- **Purpose:** Select which sections to include in the report and in what order. Some sections may be excluded for specific audiences (e.g., exclude financial details for Branch Principals meeting).
- **Sections (checkboxes, drag-reorderable):**
  - ☑ Executive Summary (always included, non-removable)
  - ☑ Season Summary Table
  - ☑ Monthly Enrollment Trend Chart
  - ☑ Branch Performance Ranking
  - ☑ Branch Detail Cards (one page per branch)
  - ☑ Channel Effectiveness Summary
  - ☑ Channel ROI Comparison
  - ☑ Financial Summary & Budget Variance
  - ☑ Key Financial Metrics
  - ☑ Key Wins & Losses
  - ☑ Offer & Discount Impact
  - ☑ Referral Impact
  - ☑ YoY Comparison Charts
  - ☑ Recommendations
  - ☐ Appendix: Raw Data Tables
  - ☐ Appendix: Branch-wise Monthly Data
- **Report title** (text, editable — defaults to "Admission Season Report 2025-26")
- **Cover page:** Toggle — include branded cover page with group logo
- **Audience** (dropdown): Board of Directors / CEO Review / Branch Principals / Marketing Team / Full (all sections)
- **Buttons:** Cancel · Save Configuration · Preview · Generate PDF
- **Access:** Role 132 or G4+

### 6.3 Modal: `export-configuration` (560px)

- **Title:** "Export Season Report"
- **Pre-condition:** Report must be compiled (at least one section with data)
- **Format options:**
  - PDF (board-presentation quality — branded header/footer, chart images, professional typography)
  - Excel (raw data tables with pivot-ready formatting — for detailed analysis)
  - PowerPoint (slide-per-section format — for presentation)
- **PDF options:**
  - Page size (dropdown): A4 / Letter
  - Orientation (dropdown): Portrait (default) / Landscape
  - Include watermark (toggle): "DRAFT" watermark if report status is not Approved
  - Include page numbers (toggle, default on)
  - Include table of contents (toggle, default on)
  - Include charts (toggle, default on)
  - Branding level (dropdown): Full (group logo, colours) / Minimal (EduForge header only)
- **Approval status:**
  - If status = Draft: PDF has "DRAFT — NOT FOR DISTRIBUTION" watermark
  - If status = Approved (G4/G5): Clean PDF, no watermark
- **Email distribution:**
  - Send to (multi-email, optional): auto-suggest CEO, CFO, Branch Principals
  - Email subject (auto-generated, editable)
  - Email body (auto-generated summary, editable)
- **Buttons:** Cancel · Download · Email & Download
- **Access:** G1+ for draft download; G4+ for approved version distribution

### 6.4 Drawer: `annotation-notes` (560px, right-slide)

- **Title:** "Report Annotations & Commentary"
- **Purpose:** Allow analyst and campaign manager to add contextual narrative that accompanies the data in the exported report.
- **Sections (one annotation block per report section):**
  - Section name (auto-listed from included sections)
  - Annotation text (rich text — bold, italic, bullet points)
  - Author (auto-filled)
  - Timestamp (auto-filled)
  - Visibility (dropdown): Internal Only (not in exported PDF) / Include in Report
- **Thread-style:** Multiple annotations per section, chronological, with author attribution
- **Buttons:** Add Annotation · Save All · Close
- **Access:** Role 132, 119, G4+

### 6.5 Modal: `branch-detail-popup` (640px)

- **Title:** "Branch Season Detail — [Branch Name]"
- **Sections:**
  - **Performance summary:** Target, enrolled, fill %, rank, performance band
  - **Monthly trend:** Mini line chart — enrollments per month (Sep–Aug)
  - **Top sources:** Top 3 lead sources for this branch
  - **Spend:** Branch marketing budget vs actual
  - **Key observations** (textarea — analyst notes)
  - **Principal's input** (textarea — optional, from branch principal annotation)
  - **Comparison with previous season:** Side-by-side metrics
- **Footer:** [Export Branch Report] [Add Annotation]
- **Access:** G1+

### 6.6 Modal: `recommendation-entry` (560px)

- **Title:** "Add Season Recommendation"
- **Fields:**
  - Category (dropdown): Budget / Branch / Channel / Process / Content / Staffing / Technology / Expansion
  - Recommendation (textarea, required)
  - Supporting data (textarea — reference specific report metrics)
  - Priority (dropdown): High / Medium / Low
  - Estimated impact (text)
  - Affected branches (multi-select, optional)
  - Timeline (dropdown): Immediate / Next Season / Long-term (2+ seasons)
- **Buttons:** Cancel · Save as Draft · Submit for Approval
- **Access:** Role 132 or G4+
- **Approval flow:** Draft → Submitted → Approved (G4/G5) / Rejected / Deferred

---

## 7. Charts

### 7.1 Target vs Actual Grouped Bar (Branch-wise)

| Property | Value |
|---|---|
| Chart type | Grouped bar (Chart.js 4.x) |
| Title | "Target vs Actual Enrollment — Branch-wise" |
| Data | X-axis = branch name (sorted by fill rate DESC); Bar 1 = target seats; Bar 2 = actual enrolled |
| Colour | Target = `#94A3B8` grey, Actual = `#10B981` green (red if < 75% of target) |
| Tooltip | "[Branch]: Target [X], Enrolled [Y] ([Z]% fill)" |
| Annotation | Horizontal dashed line at 90% fill rate threshold |
| API | `GET /api/v1/group/{id}/marketing/analytics/season-report/charts/target-vs-actual/` |

### 7.2 Channel Effectiveness Radar

| Property | Value |
|---|---|
| Chart type | Radar (Chart.js 4.x) |
| Title | "Channel Effectiveness — Multi-Dimensional Comparison" |
| Data | 5 axes per channel: Lead Volume / Conversion Rate / ROI / Cost Efficiency / YoY Growth |
| Colour | One line per channel (top 5 channels by lead volume): Newspaper `#3B82F6`, Digital `#10B981`, WhatsApp `#F59E0B`, Walk-in `#EF4444`, Referral `#8B5CF6` |
| Scale | Normalised 0–100 (percentile within own group's channels) |
| Tooltip | "[Channel]: [Axis] = [Value] (rank #[N] of [Total])" |
| API | `GET /api/v1/group/{id}/marketing/analytics/season-report/charts/channel-radar/` |

### 7.3 Monthly Enrollment Trend (Area)

| Property | Value |
|---|---|
| Chart type | Area / Line (Chart.js 4.x) |
| Title | "Monthly Cumulative Enrollment — Season 2025-26" |
| Data | X-axis = month (Sep–Aug); Y = cumulative enrollment; two lines: current season + previous season |
| Colour | Current = `#6366F1` (filled area, 20% opacity), Previous = `#94A3B8` (dashed line, no fill) |
| Overlay | Target line (dashed red) — cumulative target by month |
| Tooltip | "[Month]: [N] enrolled (cumulative [Total]) — Target: [T]" |
| API | `GET /api/v1/group/{id}/marketing/analytics/season-report/charts/monthly-trend/` |

### 7.4 YoY Comparison Line

| Property | Value |
|---|---|
| Chart type | Line (Chart.js 4.x) |
| Title | "Year-over-Year Fill Rate — Last 5 Seasons" |
| Data | X-axis = season (2021-22 to 2025-26); Y = fill rate % |
| Colour | `#6366F1` (solid line with data point markers) |
| Annotation | Horizontal dashed line at 90% (healthy threshold), 75% (critical threshold) |
| Tooltip | "Season [X]: [Y]% fill rate ([N] enrolled / [M] target)" |
| API | `GET /api/v1/group/{id}/marketing/analytics/season-report/charts/yoy-comparison/` |

### 7.5 Top / Bottom Branches Bar

| Property | Value |
|---|---|
| Chart type | Horizontal bar (Chart.js 4.x) |
| Title | "Branch Performance — Top 5 & Bottom 5" |
| Data | Fill rate % for top 5 (descending) and bottom 5 (ascending) branches |
| Colour | Top 5 = `#10B981` green, Bottom 5 = `#EF4444` red |
| Layout | Split: top 5 on left, bottom 5 on right (or stacked vertically) |
| Tooltip | "[Branch]: [X]% fill — [Y] enrolled / [Z] target" |
| API | `GET /api/v1/group/{id}/marketing/analytics/season-report/charts/top-bottom-branches/` |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Report compiled | "Season report compiled — [N] sections with data" | Success | 4s |
| Report updated | "Season report data refreshed as of [Timestamp]" | Success | 3s |
| Annotation added | "Annotation added to [Section] section" | Success | 3s |
| Recommendation added | "Recommendation added — pending G4 approval" | Success | 3s |
| Recommendation approved | "Recommendation #[N] approved by [Name]" | Success | 4s |
| Recommendation rejected | "Recommendation #[N] rejected — [Reason]" | Warning | 5s |
| PDF exported | "Season report exported as PDF — [N] pages" | Success | 4s |
| Excel exported | "Raw data exported to Excel — [Filename]" | Success | 3s |
| Report approved | "Season report approved by [CEO/Chairman] — ready for Board distribution" | Success | 5s |
| Email sent | "Season report emailed to [N] recipients" | Success | 4s |
| Data incomplete | "Warning: [Branch] enrollment data not finalised — report marked as Draft" | Warning | 6s |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| No report for season | 📊 | "No Season Report" | "Generate the admission season report to consolidate targets, enrollments, spend, and outcomes." | Generate Report |
| Season data incomplete | ⏳ | "Season Data Incomplete" | "[N] branches have not confirmed final enrollment numbers. Report will show partial data." | View Pending Branches |
| No recommendations | 💡 | "No Recommendations Yet" | "Add strategic recommendations for the next admission season based on this year's outcomes." | Add Recommendation |
| No annotations | 📝 | "No Annotations" | "Add commentary and context to report sections for Board presentation." | Add Annotation |
| Previous seasons unavailable | 📅 | "No Historical Data" | "YoY comparison requires at least 2 seasons of data. Previous season data not available." | — |
| No report for filter | 🔍 | "No Matching Data" | "Adjust season or date range to view report data." | Change Season |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | 6 KPI shimmer + executive summary skeleton |
| Season switch | Full content skeleton with KPI shimmer |
| Tab switch | Content skeleton |
| Report compilation | Progress bar: "Compiling report... Aggregating branch data (3/28)..." with step indicators |
| Branch performance table | Table skeleton (30 rows) |
| Channel analysis table | Table skeleton (12 rows) |
| Financial summary | Table skeleton with summary row |
| PDF generation | Spinner: "Generating PDF... Page [N] of [M]" with progress bar |
| Excel export | Spinner: "Exporting data..." |
| Chart load | Grey canvas placeholder |
| Branch detail popup | Modal skeleton with mini chart placeholder |
| Annotation drawer | List skeleton (5 items) |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/marketing/analytics/season-report/` | G1+ | Get season report (compiled data) |
| POST | `/api/v1/group/{id}/marketing/analytics/season-report/compile/` | G1+ | Trigger report compilation (aggregates from all source pages) |
| GET | `/api/v1/group/{id}/marketing/analytics/season-report/executive-summary/` | G1+ | Executive summary section data |
| GET | `/api/v1/group/{id}/marketing/analytics/season-report/branches/` | G1+ | Branch performance data (all branches) |
| GET | `/api/v1/group/{id}/marketing/analytics/season-report/branches/{branch_id}/` | G1+ | Single branch detail |
| GET | `/api/v1/group/{id}/marketing/analytics/season-report/channels/` | G1+ | Channel effectiveness data |
| GET | `/api/v1/group/{id}/marketing/analytics/season-report/financials/` | G1+ | Financial summary data |
| GET | `/api/v1/group/{id}/marketing/analytics/season-report/outcomes/` | G1+ | Wins, losses, offers, referrals |
| GET | `/api/v1/group/{id}/marketing/analytics/season-report/recommendations/` | G1+ | List recommendations |
| POST | `/api/v1/group/{id}/marketing/analytics/season-report/recommendations/` | G1+ | Add recommendation |
| PUT | `/api/v1/group/{id}/marketing/analytics/season-report/recommendations/{rec_id}/` | G1+ | Update recommendation |
| PATCH | `/api/v1/group/{id}/marketing/analytics/season-report/recommendations/{rec_id}/approve/` | G4+ | Approve/reject recommendation |
| GET | `/api/v1/group/{id}/marketing/analytics/season-report/annotations/` | G1+ | List annotations |
| POST | `/api/v1/group/{id}/marketing/analytics/season-report/annotations/` | G1+ | Add annotation |
| PUT | `/api/v1/group/{id}/marketing/analytics/season-report/annotations/{ann_id}/` | G1+ | Update annotation |
| DELETE | `/api/v1/group/{id}/marketing/analytics/season-report/annotations/{ann_id}/` | G3+ | Delete annotation |
| PATCH | `/api/v1/group/{id}/marketing/analytics/season-report/approve/` | G4+ | Approve report for Board distribution |
| POST | `/api/v1/group/{id}/marketing/analytics/season-report/export/pdf/` | G1+ | Export as PDF |
| POST | `/api/v1/group/{id}/marketing/analytics/season-report/export/excel/` | G1+ | Export as Excel |
| POST | `/api/v1/group/{id}/marketing/analytics/season-report/export/pptx/` | G1+ | Export as PowerPoint |
| POST | `/api/v1/group/{id}/marketing/analytics/season-report/email/` | G4+ | Email report to stakeholders |
| GET | `/api/v1/group/{id}/marketing/analytics/season-report/seasons/` | G1+ | List available seasons |
| GET | `/api/v1/group/{id}/marketing/analytics/season-report/kpis/` | G1+ | KPI values |
| GET | `/api/v1/group/{id}/marketing/analytics/season-report/charts/target-vs-actual/` | G1+ | Target vs actual chart data |
| GET | `/api/v1/group/{id}/marketing/analytics/season-report/charts/channel-radar/` | G1+ | Channel effectiveness radar data |
| GET | `/api/v1/group/{id}/marketing/analytics/season-report/charts/monthly-trend/` | G1+ | Monthly enrollment trend data |
| GET | `/api/v1/group/{id}/marketing/analytics/season-report/charts/yoy-comparison/` | G1+ | YoY comparison data |
| GET | `/api/v1/group/{id}/marketing/analytics/season-report/charts/top-bottom-branches/` | G1+ | Top/bottom branches data |

---

## 12. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load | Page load | `hx-get=".../season-report/kpis/"` | `#kpi-bar` | `innerHTML` | `hx-trigger="load"` |
| Season switch | Season dropdown | `hx-get=".../season-report/?season={id}"` | `#report-content` | `innerHTML` | Full page content reload |
| Tab switch | Tab click | `hx-get` with tab param | `#report-tab-content` | `innerHTML` | `hx-trigger="click"` |
| Report compile | Generate button | `hx-post=".../season-report/compile/"` | `#compile-progress` | `innerHTML` | Progress bar updates via polling |
| Branch detail popup | Branch row click | `hx-get=".../season-report/branches/{id}/"` | `#branch-detail-modal` | `innerHTML` | `hx-trigger="click"` |
| Add recommendation | Form submit | `hx-post=".../season-report/recommendations/"` | `#recommendations-list` | `beforeend` | Appends to list |
| Approve recommendation | Approve button | `hx-patch=".../season-report/recommendations/{id}/approve/"` | `#rec-status-{id}` | `innerHTML` | Inline badge update |
| Add annotation | Annotation form | `hx-post=".../season-report/annotations/"` | `#annotation-list` | `beforeend` | Appends to thread |
| Export PDF | Export form | `hx-post=".../season-report/export/pdf/"` | `#export-result` | `innerHTML` | Download trigger after generation |
| Approve report | Approve button | `hx-patch=".../season-report/approve/"` | `#report-status` | `innerHTML` | Status badge update |
| Chart load | Tab/section visible | `hx-get=".../season-report/charts/..."` | `#chart-{name}` | `innerHTML` | `hx-trigger="intersect once"` |
| Email distribution | Email form | `hx-post=".../season-report/email/"` | `#email-result` | `innerHTML` | Toast confirmation |
| Annotation drawer open | Annotations button | `hx-get=".../season-report/annotations/"` | `#right-drawer` | `innerHTML` | `hx-trigger="click"` |

---

*Page spec version: 1.0 · Last updated: 2026-03-26*
