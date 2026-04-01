# P-20 — Compliance Trend Analytics

> **URL:** `/group/audit/analytics/compliance-trends/`
> **File:** `p-20-compliance-trend-analytics.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Role:** Group Compliance Data Analyst (Role 127, G1) — primary operator

---

## 1. Purpose

The Compliance Trend Analytics page provides long-term, multi-dimensional visibility into how the Institution Group's compliance health is changing over time — not just what the current score is, but whether it is improving or degrading, which branches are on a recovery trajectory, which are sliding, which dimensions are the weakest across the group, and how audit interventions correlate with score changes.

While the Branch Compliance Scorecard (P-10) shows the current state of each branch, this page shows the story over time. It is the analytical backbone for the quarterly and annual Board-level compliance reports, for resource allocation decisions (which branches need support?), and for evaluating whether the group's audit function is actually producing improvement.

The problems this page solves:

1. **Snapshot vs trajectory confusion:** A branch with a score of 75 could be recovering from a low of 55 (positive trajectory, audit function working) or declining from a high of 90 (negative trajectory, recent governance failure). The snapshot alone is misleading. Trend analytics provide context that makes scores actionable.

2. **Dimension-level trend blindness:** The overall compliance score aggregates six dimensions. A group-wide average of 80% could mask: financial compliance declining (from 85% to 72%) while academic quality improving (from 65% to 82%). Without dimension-level trends, the CEO cannot direct attention to the right intervention.

3. **Audit investment ROI question:** "Is spending on auditors and inspections actually improving compliance?" This is the question every CFO asks. The Audit ROI section shows: how audit intensity (audits per branch per year) correlates with compliance score change. High-audit branches that are not improving signal process failure, not resource failure.

4. **Peer group benchmarking:** A branch that consistently scores below its zone peers on safety, despite similar facilities, may have a leadership problem. Peer group comparison — same institution type, same zone — contextualises scores without the noise of comparing a residential school to a day coaching centre.

5. **Forecast and early warning:** Based on trend data and seasonality, which branches are at risk of dropping below 70 (Band C — At Risk) in the next quarter? Early warning flags allow proactive intervention before a branch enters the formal Improvement Plan process.

**Scale:** 5–50 branches · 6 compliance dimensions · 24 months rolling history · Quarterly compliance score snapshots · Annual audit cycle

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Compliance Data Analyst | 127 | G1 | Full — all analytics, all branches, all dimensions, export | Primary operator |
| Group Internal Audit Head | 121 | G1 | Read all — compliance trends inform audit planning | Strategic oversight |
| Group Process Improvement Coordinator | 128 | G3 | Read — use trends to prioritise CAPA and BIP interventions | Operational |
| Group Affiliation Compliance Officer | 125 | G1 | Read — affiliation dimension trend in their scope | Affiliation |
| Zone Director | — | G4 | Read own zone only | Zone oversight |
| Branch Principal | — | G3 | Read own branch only — own trend visible | Branch |
| Group CEO / Chairman | — | G4/G5 | Read all | Executive |

> **Access enforcement:** `@require_role(min_level=G1, division='P')`. Branches see own trend only. Zones see own zone aggregate + branch breakdown. G1+ see group-wide.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Audit & Quality  ›  Analytics  ›  Compliance Trends
```

### 3.2 Page Header
```
Compliance Trend Analytics                              [Export Report]  [Download Data]
Compliance Data Analyst — P. Sunitha
Sunrise Education Group · 28 branches · 24 months data · Last score update: Mar-2026
```

### 3.3 Filter Bar
```
Branch: [All / Select ▼]    Zone: [All / Zone 1 / Zone 2 / Zone 3 ▼]
Institution Type: [All / School / Coaching / Hostel / College ▼]
Dimension: [All / Financial / Academic / Safety / Affiliation / CAPA Closure / Grievance ▼]
Period: [Last 12 months ▼]  [Last 24 months]  [Custom: From ___ To ___]
Granularity: [Monthly ▼]  [Quarterly]
                                                                        [Apply]
```

### 3.4 KPI Summary Bar

| # | KPI | Value | Colour Logic |
|---|---|---|---|
| 1 | Group Avg Compliance Score (Current) | 78.4% | ≥ 85 green · 70–84 amber · < 70 red |
| 2 | Change vs Prior Quarter | +3.2 pts | > 0 green · 0 neutral · < 0 red |
| 3 | Change vs Prior Year | +8.7 pts | > 5 green · 1–5 amber · < 1 red |
| 4 | Branches Improving (QoQ) | 19 / 28 | ≥ 70% green · 50–69% amber · < 50% red |
| 5 | Branches Declining (QoQ) | 6 / 28 | 0 green · 1–4 amber · ≥ 5 red |
| 6 | Branches in Band C or D (< 70%) | 4 / 28 | 0 green · 1–3 amber · ≥ 4 red |
| 7 | At-Risk Forecast (next quarter) | 2 branches | 0 green · 1–2 amber · ≥ 3 red |
| 8 | Weakest Dimension (Group) | Safety (68.2%) | Shown with colour |

---

## 4. Page Sections

### Section 1 — Group Compliance Score Trend (primary chart)

**Chart type:** Line chart (Chart.js 4.x) — full width at top of page.

**Series:**
- Group average compliance score (solid blue line)
- Group target (dashed green line at 85%)
- Minimum acceptable (dashed red line at 70%)
- Band shading: Green zone ≥ 85%, Amber zone 70–84%, Red zone < 70%

**X-axis:** Months (Apr-2024 to Mar-2026 for 24-month view).
**Y-axis:** Compliance score (0–100%).

**Annotation markers on chart:**
- 🔵 Audit cycle events (group-wide audit month)
- 🟡 Policy changes (e.g., new fire safety policy issued)
- 🟠 BIP activations (branch improvement plan starts)
- ✅ BIP closures

**Hover tooltip:** Month · Group average · Top performing branch · Lowest performing branch · Count of branches in each band.

**Chart controls:**
- Toggle individual branches: checkbox list to overlay specific branches
- Toggle dimensions: switch from overall score to dimension-specific score
- Zoom: select sub-period by dragging on chart

---

### Section 2 — Dimension-Level Trend Analysis

**Six dimension tiles (2 × 3 grid):**

Each tile shows:
- Dimension name and weight
- Current group average for this dimension
- Trend indicator: ↑ +N pts vs prior quarter | ↓ −N pts
- Mini sparkline (12-month trend)
- Weakest branch in this dimension
- Worst-to-best branch spread (min → max)

```
┌──────────────────────────────────┐  ┌──────────────────────────────────┐
│  Financial Compliance  (20%)     │  │  Academic Quality  (25%)         │
│  Group avg: 82.1%  ↑ +2.3 pts   │  │  Group avg: 85.4%  ↑ +4.1 pts   │
│  Sparkline: [▁▂▃▄▄▅▅▆▆▇█]       │  │  Sparkline: [▁▁▂▂▃▄▅▆▆▇▇█]      │
│  Weakest: Sunrise Kukatpally 61% │  │  Weakest: Sunrise Miyapur 72%    │
│  Spread: 61% → 97%               │  │  Spread: 72% → 98%               │
│         [View Dimension Detail]  │  │         [View Dimension Detail]  │
└──────────────────────────────────┘  └──────────────────────────────────┘

┌──────────────────────────────────┐  ┌──────────────────────────────────┐
│  Safety & Infrastructure  (20%)  │  │  Affiliation Compliance  (15%)   │
│  Group avg: 68.2%  ↓ −1.1 pts   │  │  Group avg: 88.3%  ↑ +1.2 pts   │
│  Sparkline: [▇▆▆▅▅▄▅▄▄▄▃▃]       │  │  Sparkline: [▅▆▆▇▇▇▇▇▇▇▇█]      │
│  Weakest: Sunrise Miyapur 48%    │  │  Weakest: Sunrise KPHB 72%       │
│  Spread: 48% → 94%      ⚠️ALERT  │  │  Spread: 72% → 100%              │
│         [View Dimension Detail]  │  │         [View Dimension Detail]  │
└──────────────────────────────────┘  └──────────────────────────────────┘

┌──────────────────────────────────┐  ┌──────────────────────────────────┐
│  CAPA Closure Rate  (10%)        │  │  Grievance Resolution  (10%)     │
│  Group avg: 71.4%  ↑ +5.8 pts   │  │  Group avg: 79.2%  ↑ +2.1 pts   │
│  Sparkline: [▁▂▂▃▃▄▅▅▆▆▇█]       │  │  Sparkline: [▅▅▅▆▆▆▇▇▇▇▇█]      │
│  Weakest: Sunrise Begumpet 51%   │  │  Weakest: Sunrise Uppal 62%      │
│  Spread: 51% → 96%               │  │  Spread: 62% → 95%               │
│         [View Dimension Detail]  │  │         [View Dimension Detail]  │
└──────────────────────────────────┘  └──────────────────────────────────┘
```

**`[View Dimension Detail]`** opens a slide-out panel showing:
- Full 24-month trend chart for this dimension
- All branches ranked by this dimension score
- Dimension-specific CAPA count and open findings
- Top 3 contributing factors to low scores in this dimension (from audit data)

---

### Section 3 — Branch Trajectory Table

One row per branch, sorted by score trajectory (biggest decline first by default).

**Table columns:**

| # | Column | Content |
|---|---|---|
| 1 | Branch | Branch name |
| 2 | Institution Type | School / Coaching / Hostel / College |
| 3 | Zone | Zone name |
| 4 | Score 12 Months Ago | Prior year score |
| 5 | Score 6 Months Ago | Mid-year score |
| 6 | Score 3 Months Ago | Prior quarter |
| 7 | Current Score | Latest score (colour-coded: green ≥ 85, amber 70–84, red < 70) |
| 8 | 12-Month Change | +/− pts — green if positive · red if negative |
| 9 | QoQ Change | +/− pts vs prior quarter |
| 10 | Trend | ↑↑ Strong improving / ↑ Improving / → Stable / ↓ Declining / ↓↓ Sharply declining |
| 11 | Sparkline | 12-month mini chart (right-aligned bars) |
| 12 | Forecast | Projected score next quarter (model-based) |
| 13 | Status | 🟢 Normal / 🟡 Watch / 🔴 At Risk / 🟣 On BIP |
| 14 | Actions | [View Detail] |

**Status logic:**
- Normal: score ≥ 70, QoQ change ≥ 0
- Watch: score 70–79 and declining, or score ≥ 70 but forecast < 70
- At Risk: score < 70 (Band C or D)
- On BIP: active improvement plan in P-17

---

### Section 4 — Peer Group Comparison

Compare a selected branch against peers — same institution type and zone.

**Control:** `Branch: [Select ▼]` → loads peer group comparison.

**Radar chart:** 6 dimensions as axes. Selected branch (blue) vs peer group average (dashed orange).

**Table below radar:**

| Dimension | Selected Branch | Peer Avg | vs Peer | Rank (1 = best) |
|---|---|---|---|---|
| Financial | 72% | 81% | −9 pts 🔴 | 7 of 9 |
| Academic | 85% | 83% | +2 pts 🟢 | 3 of 9 |
| Safety | 55% | 74% | −19 pts 🔴 | 9 of 9 |
| Affiliation | 91% | 88% | +3 pts 🟢 | 2 of 9 |
| CAPA Closure | 62% | 70% | −8 pts 🟠 | 7 of 9 |
| Grievance | 78% | 76% | +2 pts 🟢 | 4 of 9 |

"This branch is weakest in its peer group for Safety (rank 9/9) and Financial (rank 7/9). Safety score has declined 3 months in a row — consider prioritising safety inspection visit."

---

### Section 5 — Audit Intensity vs Score Correlation

**Chart:** Scatter plot.
- X-axis: Audit visits per branch per year (from P-07 data)
- Y-axis: Annual compliance score improvement (pts)
- Each dot: one branch
- Colour: Branch institution type
- Trend line: Linear regression (does more auditing = more improvement?)

**Interpretation panel:**
```
Correlation coefficient: r = 0.61 (moderate positive correlation)
Interpretation: Branches with 4+ audit visits/year improve an average of +8.2 pts vs +2.1 pts
                for branches with < 2 visits/year.

Outliers (high visits, low improvement): Sunrise Miyapur — 6 visits, only +1.4 pts improvement.
  Possible cause: Inspection findings raised but CAPA closure rate low (51%) — audit is finding
  problems but branch is not fixing them. Recommend CAPA enforcement escalation.

Outliers (low visits, high improvement): Sunrise HITEC City — 2 visits, +12.3 pts improvement.
  Possible cause: BIP activated mid-year; intense self-directed improvement driven by new principal.
```

---

### Section 6 — At-Risk Forecast

Branches predicted to drop below 70% in the next quarter based on:
- Current score trajectory (linear trend extrapolation)
- Seasonal adjustment (compliance tends to dip in Dec–Jan during exam season)
- Open CAPA count and age

**Forecast table:**

| Branch | Current Score | Projected Next Quarter | Change | Risk Level | Recommended Action |
|---|---|---|---|---|---|
| Sunrise KPHB | 74% | 67% | −7 pts | 🔴 High Risk | Initiate BIP now |
| Sunrise Uppal | 71% | 68% | −3 pts | 🟠 Medium Risk | Schedule targeted inspection |

**Note displayed:** "Forecast based on 12-month linear trend + seasonal adjustment. Actual outcomes depend on interventions taken. Forecast updates monthly."

---

## 5. Sections Summary

| # | Section | Purpose |
|---|---|---|
| 1 | Group Compliance Score Trend | 24-month group average trend with annotations |
| 2 | Dimension-Level Trend Analysis | 6-tile view of each dimension with sparklines and dimension detail |
| 3 | Branch Trajectory Table | All branches with multi-period scores, trend, and forecast |
| 4 | Peer Group Comparison | Branch vs peer group radar and table |
| 5 | Audit Intensity vs Score | Scatter plot correlating audit frequency to improvement |
| 6 | At-Risk Forecast | Predictive early warning for branches heading toward Band C/D |

---

## 6. Drawers & Modals

### Panel 1 — Dimension Detail Slide-out (right, 820px)

**Trigger:** `[View Dimension Detail]` from dimension tile.

**Content:**
- Full 24-month trend chart for this dimension (group average)
- All branches ranked on this dimension (bar chart)
- Key contributing factors to low dimension scores (from audit findings in P-06 filtered by dimension)
- Open CAPA items in this dimension (count + oldest item age)
- SLA compliance for this dimension (if applicable — affiliation documents, regulatory filings)
- `[Download Dimension Report]`

### Modal 1 — Export Report

**Form:**
```
Report Type:
  ◉ Compliance Trend Summary (all branches)
  ○ Single Branch Deep Dive
  ○ Executive Dashboard (1-page summary)
  ○ Board Presentation Deck (PowerPoint)

Period: [Last 12 months ▼]
Include: ☑ Group trend ☑ Dimension analysis ☑ Branch trajectories ☑ At-risk forecast
         ☐ Peer comparison ☐ Audit intensity correlation

Format: ◉ PDF   ○ Excel   ○ PowerPoint (exec deck only)
Recipients: [optional — send by email]
```

---

## 7. Charts

### Chart 1 — Group Compliance Trend (line)
- **API:** `GET /api/v1/group/{id}/audit/analytics/compliance-trend/`

### Chart 2 — Dimension Sparklines (6 mini charts)
- **API:** `GET /api/v1/group/{id}/audit/analytics/dimension-trends/`

### Chart 3 — Dimension Full Trend (line — in dimension detail panel)
- **API:** `GET /api/v1/group/{id}/audit/analytics/dimension-trends/{dimension}/`

### Chart 4 — Radar — Peer Comparison
- **Type:** Radar (Chart.js 4.x)
- **API:** `GET /api/v1/group/{id}/audit/analytics/peer-comparison/?branch={id}`

### Chart 5 — Scatter — Audit Intensity vs Score
- **Type:** Scatter (Chart.js 4.x)
- **API:** `GET /api/v1/group/{id}/audit/analytics/audit-intensity-correlation/`

### Chart 6 — Branch Trajectory Sparklines (per row in table)
- **Type:** Inline sparkline (Chart.js micro-chart)
- **API:** Included in branch trajectory list response

---

## 8. Toast Messages

| Action | Toast | Type |
|---|---|---|
| Filter applied | "Showing compliance trends for Q3–Q4 FY 2025-26 · 28 branches" | Info (blue) |
| Report exported | "Compliance Trend Report downloaded — 28 branches · 24 months · PDF" | Success (green) |
| At-risk alert | "⚠️ Sunrise KPHB projected to drop below 70% next quarter — recommend BIP initiation" | Warning (amber) |
| Dimension detail loaded | "Safety & Infrastructure trend loaded — 24 months · 28 branches" | Info (blue) |
| Peer comparison loaded | "Peer comparison loaded — Sunrise Miyapur vs 8 peer coaching branches" | Info (blue) |

---

## 9. Empty States

| Scenario | Illustration | Message | CTA |
|---|---|---|---|
| No historical data | Line chart with dotted line | "Compliance score history not available yet. Scores are recorded after each audit cycle." | — |
| Less than 3 data points | Line chart partial | "Only {N} data points available — trend analysis requires at least 3 quarterly scores." | — |
| No peer group | Radar with empty | "No peer branches found for this institution type + zone combination." | — |
| Filter returns no data | Magnifying glass | "No compliance data for the selected filters." | `[Reset Filters]` |

---

## 10. Loader States

| Element | Loader Type | Duration |
|---|---|---|
| Page initial load | Skeleton: KPI bar + chart placeholders | < 1s |
| Group trend chart | Grey line placeholder → Chart.js | < 500ms |
| Dimension tiles | 6 skeleton tiles → populated | < 500ms |
| Branch trajectory table | Skeleton rows → data + sparklines | < 1.5s |
| Peer comparison | Radar placeholder → Chart.js | < 500ms |
| Scatter chart | Scatter placeholder → Chart.js | < 1s |
| At-risk forecast | Skeleton rows → forecast data | < 1s |
| Dimension detail panel | Slide-out skeleton → populated | < 500ms |

---

## 11. API Endpoints

All endpoints prefixed: `/api/v1/group/{group_id}/audit/analytics/`

| # | Method | Endpoint | Purpose | Role |
|---|---|---|---|---|
| 1 | GET | `/compliance-trend/` | Group compliance score time series | G1+ |
| 2 | GET | `/compliance-trend/?branch={id}` | Single branch trend | G1+ |
| 3 | GET | `/dimension-trends/` | All 6 dimensions — current + sparklines | G1+ |
| 4 | GET | `/dimension-trends/{dimension}/` | Full trend for one dimension | G1+ |
| 5 | GET | `/branch-trajectories/` | All branches — multi-period scores + forecast | G1+ |
| 6 | GET | `/peer-comparison/?branch={id}` | Peer group radar data | G1+ |
| 7 | GET | `/audit-intensity-correlation/` | Scatter data — audit visits vs improvement | G1+ |
| 8 | GET | `/at-risk-forecast/` | Branches forecast to drop below 70% | G1+ |
| 9 | GET | `/kpis/` | KPI bar aggregates | G1+ |
| 10 | GET | `/export/` | Export compliance trend report | G1+ |

---

## 12. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load | Page load | `hx-get=".../analytics/kpis/"` | `#kpi-bar` | `innerHTML` | `hx-trigger="load"` |
| Group trend chart | Page load | `hx-get=".../analytics/compliance-trend/"` | `#group-trend-chart` | `innerHTML` | Chart.js init |
| Dimension tiles | Page load | `hx-get=".../analytics/dimension-trends/"` | `#dimension-tiles` | `innerHTML` | 6 tiles with sparklines |
| Branch trajectory table | Page load | `hx-get=".../analytics/branch-trajectories/"` | `#branch-table` | `innerHTML` | Includes sparklines |
| Filter apply | `[Apply]` click | `hx-get` with filters | `#analytics-content` | `innerHTML` | Re-renders all sections |
| Dimension detail panel | `[View Detail]` click | `hx-get=".../analytics/dimension-trends/{dim}/"` | `#dimension-detail-panel` | `innerHTML` | Slide-out |
| Peer comparison load | Branch select change | `hx-get=".../analytics/peer-comparison/?branch={id}"` | `#peer-section` | `innerHTML` | Radar + table |
| Scatter chart | Section scroll | `hx-get=".../analytics/audit-intensity-correlation/"` | `#scatter-chart` | `innerHTML` | Lazy load |
| At-risk forecast | Section scroll | `hx-get=".../analytics/at-risk-forecast/"` | `#at-risk-section` | `innerHTML` | Lazy load |
| Export | Form submit | `hx-post=".../analytics/export/"` | `#export-result` | `innerHTML` | Download trigger |

---

*Page spec version: 1.0 · Last updated: 2026-03-26*
