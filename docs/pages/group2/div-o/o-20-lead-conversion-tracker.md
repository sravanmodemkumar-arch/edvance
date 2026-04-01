# O-20 — Lead Conversion Tracker

> **URL:** `/group/marketing/leads/conversion/`
> **File:** `o-20-lead-conversion-tracker.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Role:** Group Admissions Campaign Manager (Role 119, G3) — primary analyst

---

## 1. Purpose

The Lead Conversion Tracker is the analytical lens on the lead pipeline — showing where leads convert, where they drop off, how long each stage takes, and what factors predict enrollment. While O-15 (Pipeline) is the operational view for managing individual leads, this page is the strategic view for optimising the entire funnel. A 2% improvement in conversion rate for a group receiving 50,000 leads means 1,000 additional enrollments — potentially ₹5–15 crore in additional revenue.

The problems this page solves:

1. **Stage-wise drop-off identification:** If 80% of leads reach "Contacted" but only 46% reach "Interested," the problem is the telecalling pitch. If 60% of walk-ins get counselled but only 40% submit applications, the problem is the counselling process. This page pinpoints exactly where the funnel leaks.

2. **Time-to-convert analysis:** A lead that converts in 7 days vs 45 days costs dramatically different amounts in telecaller effort. The tracker shows average days per stage and identifies leads stuck too long — a lead in "Offered Seat" for 20 days without fee payment likely needs a push or discount.

3. **Cohort analysis:** Leads from January behave differently from leads arriving in April (desperation buyers). The tracker lets you compare conversion rates, speed, and source effectiveness across time cohorts.

4. **Predictive indicators:** Based on historical data, the tracker identifies which lead attributes correlate with enrollment: source, class/stream, branch, lead score, number of calls, walk-in vs no walk-in, referral vs newspaper. These insights feed back into O-19 (assignment rules) and O-09 (budget allocation).

5. **Lost lead analysis:** Understanding why leads are lost is as valuable as understanding why they convert. Competitor analysis (which groups are winning your lost leads), price sensitivity, geographic drop-off patterns.

**Scale:** 2,000–2,00,000 leads/season · 10 pipeline stages · 7 admission phases · multi-dimensional analysis (source × branch × class × time)

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Admissions Campaign Manager | 119 | G3 | Full read + configure — all conversion data, set benchmarks, configure alerts | Primary analyst |
| Group Admission Data Analyst | 132 | G1 | Read + Export — full analytics access, download reports | Deep analytics |
| Group Admission Telecaller Executive | 130 | G3 | Read (own leads only) — view own conversion metrics | Self-assessment |
| Group Topper Relations Manager | 120 | G3 | Read — topper/scholarship lead conversion data | Cross-reference |
| Group CEO / Chairman | — | G4/G5 | Read — full conversion dashboard | Strategic decisions |
| Branch Principal | — | G3 | Read (own branch) — branch conversion performance | Branch accountability |

> **Access enforcement:** `@require_role(min_level=G1, division='O')`. Telecallers see only own leads. Branch staff see only own branch. Full cross-branch analytics: 119, 132, G4+.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Marketing & Campaigns  ›  Lead Management  ›  Lead Conversion Tracker
```

### 3.2 Page Header
```
Lead Conversion Tracker                              [Set Benchmarks]  [Alerts Config]  [Export Report]
Campaign Manager — Rajesh Kumar
Sunrise Education Group · Season 2026-27 · Overall Conversion: 17.9% · Avg Days to Enroll: 34 · Lost Rate: 42%
```

---

## 4. KPI Summary Bar (8 cards)

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Overall Conversion | Percentage | Enrolled / Total leads × 100 | Green ≥ 25%, Amber 15–25%, Red < 15% | `#kpi-conversion` |
| 2 | Enquiry → Contact | Percentage | Contacted / New × 100 | Green ≥ 85%, Amber 70–85%, Red < 70% | `#kpi-e2c` |
| 3 | Contact → Walk-in | Percentage | Walk-in Done / Contacted × 100 | Green ≥ 40%, Amber 25–40%, Red < 25% | `#kpi-c2w` |
| 4 | Walk-in → Enrolled | Percentage | Enrolled / Walk-in Done × 100 | Green ≥ 55%, Amber 40–55%, Red < 40% | `#kpi-w2e` |
| 5 | Avg Days to Enroll | Decimal | AVG(enrolled_date − created_date) | Green ≤ 30, Amber 30–60, Red > 60 | `#kpi-days` |
| 6 | This Month Enrolled | Integer | COUNT enrolled this month | Static green | `#kpi-month-enrolled` |
| 7 | Active Pipeline Value | ₹ Amount | SUM(expected_fee) for leads in stages Interested–Offered | Static blue | `#kpi-pipeline-value` |
| 8 | Lost This Month | Integer + % | COUNT + % of total lost this month | Red > 50%, Amber 30–50%, Green < 30% | `#kpi-lost` |

---

## 5. Sections

### 5.1 Tab Navigation

Five tabs:
1. **Conversion Funnel** — Stage-wise conversion with drop-off analysis
2. **Stage Analytics** — Time-in-stage, bottleneck identification
3. **Source Conversion** — Conversion rates per lead source
4. **Lost Lead Analysis** — Why leads don't convert
5. **Cohort & Trends** — Time-based conversion patterns

### 5.2 Tab 1: Conversion Funnel

**Interactive funnel visualisation** (see §7.1) showing leads at each stage with:
- Count at each stage
- Drop-off % between stages
- Click on any stage → drill-down to see leads at that stage

**Funnel filters:** Season · Branch · Source · Class/Stream · Date Range · Telecaller

**Stage-wise conversion table below funnel:**

| Stage | Leads | % of Total | Stage Conversion | Drop-off | Avg Days in Stage | SLA Target | Status |
|---|---|---|---|---|---|---|---|
| New Enquiry | 48,200 | 100% | — | — | 0.3 | 0.2 | ✅ |
| Contacted | 38,560 | 80.0% | 80.0% | 20.0% | 1.2 | 1.0 | ⚠️ |
| Interested | 22,414 | 46.5% | 58.1% | 41.9% | 3.4 | 3.0 | ⚠️ |
| Walk-in Done | 14,460 | 30.0% | 64.5% | 35.5% | 5.2 | 7.0 | ✅ |
| Counselled | 11,568 | 24.0% | 80.0% | 20.0% | 2.1 | 3.0 | ✅ |
| Applied | 10,411 | 21.6% | 90.0% | 10.0% | 1.8 | 3.0 | ✅ |
| Offered | 9,640 | 20.0% | 92.6% | 7.4% | 4.5 | 7.0 | ✅ |
| Enrolled | 8,640 | 17.9% | 89.6% | 10.4% | 2.3 | 14.0 | ✅ |

**Colour coding:** Green (above benchmark), Amber (near benchmark), Red (below benchmark).

### 5.3 Tab 2: Stage Analytics

#### 5.3.1 Time-in-Stage Distribution

Per stage, show distribution of how long leads spend in that stage:
- Histogram: X = days in stage (0, 1, 2, 3, …, 30+), Y = count of leads
- Median, P75, P90 markers
- Leads above P90 are "stuck" — potential bottleneck

#### 5.3.2 Bottleneck Identification

| Bottleneck | Metric | Current | Target | Gap | Impact |
|---|---|---|---|---|---|
| Highest drop-off stage | Contacted → Interested | 58.1% | 70% | −11.9% | +5,700 more interested leads |
| Slowest stage | Walk-in booking | 5.2 days avg | 3 days | +2.2 days | Faster conversion = more seats filled |
| Lowest stage conversion | Interested → Walk-in | 64.5% | 75% | −10.5% | +2,350 more walk-ins |

#### 5.3.3 Stuck Leads Alert

Table of leads stuck in a stage beyond SLA:

| Lead | Stage | Days in Stage | SLA | Overdue By | Assigned To | Last Action | Quick Action |
|---|---|---|---|---|---|---|---|
| L-2026-01234 | Interested | 14 days | 7 days | 7 days | Priya R. | Call on Jan 20 | [Call] [Reassign] |

### 5.4 Tab 3: Source Conversion

Conversion funnel broken down by source (see §7.3).

| Source | Leads | Contact % | Walk-in % | Enroll % | CPL (₹) | CPA (₹) | ROI | Rank |
|---|---|---|---|---|---|---|---|---|
| Referral | 4,820 | 92% | 68% | 38% | ₹120 | ₹315 | 18.2× | #1 |
| Walk-in (direct) | 3,860 | 100% | 100% | 55% | ₹0 | ₹0 | ∞ | #2 |
| Newspaper | 14,460 | 78% | 28% | 12% | ₹340 | ₹2,840 | 2.1× | #3 |
| WhatsApp | 8,680 | 82% | 22% | 10% | ₹45 | ₹450 | 12.8× | #4 |
| Digital Ads | 7,230 | 72% | 18% | 8% | ₹520 | ₹6,500 | 0.9× | #5 |

### 5.5 Tab 4: Lost Lead Analysis

#### 5.5.1 Loss Reasons (Donut + Table)

| Reason | Count | % of Lost | Trend |
|---|---|---|---|
| Fee Too High | 4,820 | 24% | ↑ (+3% vs last season) |
| Joined Competitor | 3,640 | 18% | ↓ (−2%) |
| No Response (unreachable) | 5,240 | 26% | — |
| Location/Distance | 2,410 | 12% | — |
| Academic Mismatch | 1,200 | 6% | — |
| Changed City | 800 | 4% | — |
| Other / Not Specified | 2,090 | 10% | — |

#### 5.5.2 Competitor Analysis

| Competitor | Leads Lost To | % of Competitor Losses | Common Reason |
|---|---|---|---|
| Narayana Group | 1,420 | 39% | Lower fee / More branches |
| Sri Chaitanya | 980 | 27% | Better results reputation |
| Local single-branch | 640 | 18% | Proximity |
| Other | 600 | 16% | — |

#### 5.5.3 Stage-of-Loss Analysis

Where in the funnel do leads exit?

| Exit Stage | Count | % | Insight |
|---|---|---|---|
| After Contact (Not Interested) | 8,200 | 41% | Telecalling pitch needs improvement |
| After Walk-in (Didn't Apply) | 2,890 | 14% | Counselling or facilities gap |
| After Offer (Didn't Pay) | 1,000 | 5% | Fee objection — offer discount push |
| Never Contacted | 4,800 | 24% | Assignment or capacity issue |
| Duplicate / Invalid | 3,310 | 16% | Data quality |

### 5.6 Tab 5: Cohort & Trends

#### 5.6.1 Monthly Cohort Analysis

| Cohort (Month) | Total Leads | Enrolled | Conversion % | Avg Days | Still Active |
|---|---|---|---|---|---|
| October 2025 | 2,400 | 840 | 35% | 42 | 120 |
| November 2025 | 4,800 | 1,560 | 32.5% | 38 | 340 |
| December 2025 | 6,200 | 1,860 | 30% | 32 | 620 |
| January 2026 | 12,400 | 2,480 | 20% | 28 | 2,800 |
| February 2026 | 14,200 | 1,600 | 11.3% | — | 8,400 |

**Insight:** Early-season leads (Oct–Nov) convert at 2–3× the rate of peak-season leads (Jan–Feb), validating early-bird campaign investment.

#### 5.6.2 Conversion Rate Trend (Weekly)

Line chart showing weekly conversion rate over the season. Overlaid with campaign launch markers.

---

## 6. Drawers & Modals

### 6.1 Modal: `set-benchmarks` (560px)

- **Title:** "Set Conversion Benchmarks"
- **Fields:** Per stage: target conversion %, target days in stage
- **Pre-fill:** Last season's actuals as starting point
- **Use:** Benchmarks colour-code the conversion table (green/amber/red)
- **Buttons:** Cancel · Save Benchmarks
- **Access:** Role 119 or G4+

### 6.2 Modal: `configure-alerts` (480px)

- **Title:** "Conversion Alert Configuration"
- **Alert types:**
  - Stage conversion drops below [X]% for [N] consecutive days
  - Stuck leads exceed [N] at any stage
  - Lost rate exceeds [X]% in [period]
  - Competitor loss spike: > [N] leads lost to same competitor in [period]
- **Notification:** Email / WhatsApp / In-app notification / All
- **Recipients:** Campaign Manager / Data Analyst / CEO
- **Buttons:** Cancel · Save Alerts
- **Access:** Role 119 or G4+

### 6.3 Drawer: `stage-drill-down` (720px, right-slide)

- **Title:** "[Stage Name] — Detailed Analysis"
- **Content:**
  - Total leads at this stage
  - Avg days in stage, distribution histogram
  - Source breakdown for leads at this stage
  - Branch breakdown
  - Telecaller breakdown (who has the most leads stuck here)
  - List of leads with "stuck" badge (beyond SLA)
  - Quick actions: [Bulk Reassign Stuck Leads] [Send Reminder Notification]

### 6.4 Drawer: `lost-lead-drill-down` (640px, right-slide)

- **Title:** "Lost Leads — [Reason]"
- **Content:**
  - List of all leads lost with this reason
  - Common attributes (source, branch, class, telecaller)
  - Stage where lost
  - Recovery opportunity: leads lost < 30 days ago might be recoverable
  - [Recover — Re-enter Pipeline] action for selected leads

---

## 7. Charts

### 7.1 Conversion Funnel (Interactive Funnel)

| Property | Value |
|---|---|
| Chart type | Interactive funnel (custom CSS/D3.js) |
| Title | "Lead-to-Enrollment Funnel — Season [Year]" |
| Data | Count per stage with progressive narrowing |
| Colour | Grey → Blue → Purple → Amber → Green → Emerald (progressive) |
| Interactivity | Click stage → drill-down drawer; Hover → tooltip with %, count, avg days |
| API | `GET /api/v1/group/{id}/marketing/leads/conversion/analytics/funnel/` |

### 7.2 Stage Conversion Over Time (Multi-Line)

| Property | Value |
|---|---|
| Chart type | Multi-line (Chart.js 4.x) |
| Title | "Stage Conversion Rates — Weekly Trend" |
| Data | Per stage: weekly conversion rate |
| Lines | One line per key transition: E→C, C→I, I→W, W→E |
| X-axis | Week |
| Y-axis | Percentage |
| API | `GET /api/v1/group/{id}/marketing/leads/conversion/analytics/stage-trend/` |

### 7.3 Source Conversion Comparison (Grouped Bar)

| Property | Value |
|---|---|
| Chart type | Grouped horizontal bar |
| Title | "Conversion Rate by Source" |
| Data | Per source: enquiry-to-contact %, contact-to-walkin %, walkin-to-enroll % |
| Colour | Three shades per source |
| API | `GET /api/v1/group/{id}/marketing/leads/conversion/analytics/source-conversion/` |

### 7.4 Loss Waterfall (Waterfall Chart)

| Property | Value |
|---|---|
| Chart type | Waterfall (Chart.js plugin or custom) |
| Title | "Where Leads Are Lost — Waterfall" |
| Data | Starting at total → subtract losses at each stage → ending at enrolled |
| Colour | Starting/ending: blue; Losses: red; Remaining: green |
| API | `GET /api/v1/group/{id}/marketing/leads/conversion/analytics/loss-waterfall/` |

### 7.5 Cohort Heatmap (Matrix)

| Property | Value |
|---|---|
| Chart type | Heatmap (CSS grid) |
| Title | "Cohort Conversion Heatmap" |
| Data | Rows = monthly cohorts; Columns = weeks since creation; Cell = conversion % at that point |
| Colour | White (0%) → Green (max %) |
| Purpose | See how fast each cohort converts over time |
| API | `GET /api/v1/group/{id}/marketing/leads/conversion/analytics/cohort-heatmap/` |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Benchmarks saved | "Conversion benchmarks updated for Season [Year]" | Success | 3s |
| Alerts configured | "Conversion alerts configured — [N] rules active" | Success | 3s |
| Alert triggered | "⚠️ Conversion alert: [Stage] conversion dropped below [X]%" | Warning | 6s |
| Stuck leads alert | "[N] leads stuck beyond SLA at [Stage]" | Warning | 5s |
| Competitor spike | "⚠️ [N] leads lost to [Competitor] this week — review pricing" | Warning | 6s |
| Report exported | "Conversion report exported" | Success | 2s |
| Lead recovered | "Lead [Name] re-entered pipeline from lost stage" | Success | 3s |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| No leads in pipeline | 📊 | "No Conversion Data" | "Conversion analytics require leads in the pipeline." | Go to Lead Pipeline |
| Not enough data for trends | 📈 | "Insufficient Data" | "Trend charts require at least 4 weeks of data." | — |
| No benchmarks set | 🎯 | "Benchmarks Not Configured" | "Set conversion benchmarks to enable performance colour coding." | Set Benchmarks |
| No lost leads | ✅ | "No Leads Lost" | "Excellent! No leads have been marked as lost." | — |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | 8 KPI shimmer + funnel placeholder + table skeleton |
| Tab switch | Content area skeleton |
| Funnel render | Animated funnel build (stages appear top-down) |
| Drill-down drawer | 720px skeleton: metrics + list |
| Cohort matrix | Grid placeholder |
| Chart load | Grey canvas placeholder |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/marketing/leads/conversion/` | G1+ | Conversion summary data |
| GET | `/api/v1/group/{id}/marketing/leads/conversion/funnel/` | G1+ | Funnel stage data |
| GET | `/api/v1/group/{id}/marketing/leads/conversion/stage/{stage}/` | G1+ | Stage drill-down |
| GET | `/api/v1/group/{id}/marketing/leads/conversion/stage/{stage}/stuck/` | G1+ | Stuck leads at stage |
| GET | `/api/v1/group/{id}/marketing/leads/conversion/sources/` | G1+ | Source conversion table |
| GET | `/api/v1/group/{id}/marketing/leads/conversion/lost/` | G1+ | Lost lead analysis |
| GET | `/api/v1/group/{id}/marketing/leads/conversion/lost/competitors/` | G1+ | Competitor loss data |
| GET | `/api/v1/group/{id}/marketing/leads/conversion/cohorts/` | G1+ | Cohort analysis |
| POST | `/api/v1/group/{id}/marketing/leads/conversion/benchmarks/` | G3+ | Set benchmarks |
| GET | `/api/v1/group/{id}/marketing/leads/conversion/benchmarks/` | G1+ | Get current benchmarks |
| POST | `/api/v1/group/{id}/marketing/leads/conversion/alerts/` | G3+ | Configure alerts |
| PATCH | `/api/v1/group/{id}/marketing/leads/pipeline/{lead_id}/recover/` | G3+ | Recover lost lead |
| GET | `/api/v1/group/{id}/marketing/leads/conversion/kpis/` | G1+ | KPI values |
| GET | `/api/v1/group/{id}/marketing/leads/conversion/analytics/funnel/` | G1+ | Funnel chart |
| GET | `/api/v1/group/{id}/marketing/leads/conversion/analytics/stage-trend/` | G1+ | Stage trend lines |
| GET | `/api/v1/group/{id}/marketing/leads/conversion/analytics/source-conversion/` | G1+ | Source bars |
| GET | `/api/v1/group/{id}/marketing/leads/conversion/analytics/loss-waterfall/` | G1+ | Loss waterfall |
| GET | `/api/v1/group/{id}/marketing/leads/conversion/analytics/cohort-heatmap/` | G1+ | Cohort heatmap |
| GET | `/api/v1/group/{id}/marketing/leads/conversion/export/` | G1+ | Export report |

---

## 12. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load | `<div id="kpi-bar">` | `hx-get=".../conversion/kpis/"` | `#kpi-bar` | `innerHTML` | `hx-trigger="load"` |
| Tab switch | Tab click | `hx-get` with tab param | `#conversion-content` | `innerHTML` | `hx-trigger="click"` |
| Funnel render | Funnel tab | `hx-get=".../conversion/funnel/"` | `#funnel-container` | `innerHTML` | `hx-trigger="load"` |
| Filter apply | Dropdowns | `hx-get` with params | `#conversion-content` | `innerHTML` | `hx-trigger="change"` |
| Stage drill-down | Funnel click | `hx-get=".../conversion/stage/{stage}/"` | `#right-drawer` | `innerHTML` | `hx-trigger="click"` |
| Lost drill-down | Reason row click | `hx-get=".../conversion/lost/?reason={r}"` | `#right-drawer` | `innerHTML` | `hx-trigger="click"` |
| Benchmark save | Form submit | `hx-post=".../conversion/benchmarks/"` | `#bench-result` | `innerHTML` | Toast + table recolour |
| Recover lead | Recover button | `hx-patch=".../pipeline/{id}/recover/"` | `#recover-result` | `innerHTML` | Toast |
| Chart load | Per chart | `hx-get=".../conversion/analytics/..."` | `#chart-{name}` | `innerHTML` | Lazy-load |

---

*Page spec version: 1.0 · Last updated: 2026-03-26*
