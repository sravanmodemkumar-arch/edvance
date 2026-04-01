# 47 — HR Analytics Dashboard

- **URL:** `/group/hr/analytics/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Role:** Group HR Director (Role 41, G3)

---

## 1. Purpose

The HR Analytics Dashboard is the data intelligence hub for strategic HR decision-making across the group. Unlike the operational pages that manage individual records, this page synthesises long-term trends and cross-branch comparisons that are invisible in day-to-day operations. The HR Director uses this page to identify systemic HR problems, validate HR interventions, and prepare evidence-based arguments for management decisions.

The dashboard answers key strategic questions: Is staff turnover higher in certain branches — and does that signal a management or culture problem at those branches? Is the recruitment process efficient — what proportion of applicants ultimately join? Which role categories are hardest to fill? Is the investment in training producing measurable outcomes — do branches with higher CPD hours show better student results? Are disciplinary incidents clustered in specific branches, indicating management failure? Are grievances rising over time — an early warning of staff dissatisfaction?

All charts on this page are interactive. Clicking on any chart element drills down into the underlying data — for example, clicking a branch bar in the Turnover Rate chart navigates to a filtered view of that branch's exit records, showing individual exits with reasons. All charts support date range filtering — Last 30 Days, Last 3 Months, This Academic Year (default), and Custom range. Branch filter applies globally to all charts simultaneously. Every chart has an Export PNG button for use in presentations and an Export CSV button for the underlying data.

The page loads chart data asynchronously — the page skeleton renders immediately, and each chart fetches its data independently, so slow-loading charts do not block others. The HR Director sees all branches; Group HR Managers see all branches in read-only mode. Branch-level staff do not have access to this page — it is a group-level strategic tool.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group HR Director | G3 | Full access — all charts, all branches, drill-down | Primary operator |
| Group HR Manager | G3 | Read-only — all charts, no drill-down | Strategic awareness |
| Group Training & Development Manager | G2 | Read-only — Training ROI chart only | Scoped access |
| Group Performance Review Officer | G1 | Read-only — Performance and Disciplinary charts only | Scoped access |
| All other roles | — | No access | Page not rendered |

---

## 3. Page Layout

### 3.1 Breadcrumb

```
Group Portal › HR & Staff › HR Analytics Dashboard
```

### 3.2 Page Header

- **Title:** HR Analytics Dashboard
- **Subtitle:** Strategic HR intelligence — trends, comparisons, and drill-downs
- **Global Filters (applied to all charts simultaneously):**
  - Date Range: Dropdown — Last 30 Days / Last 3 Months / This Academic Year (default) / Custom (date picker pair)
  - Branch: Multi-select dropdown — All Branches (default) or specific selection
- **Secondary CTA:** `Export Full Report` (PDF — all charts + KPI bar compiled into a report)
- **Last refreshed:** Timestamp shown in header ("Data as of 2026-03-21 08:30")

### 3.3 Alert Banner (conditional)

- **Amber:** `[N] charts failed to load. Refresh to retry.` Action: `Retry All`
- **Blue:** `Analytics data is updated nightly. Real-time data is on individual operational pages.`
- No green/red operational alerts — this is an analytics page, not an operational one

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Overall Staff Strength | Total active staff count across all branches | Blue always | Navigate to Staff Strength Report (page 51) |
| Group Turnover Rate (%) | Exits in last 12 months ÷ avg staff strength × 100 | Green if ≤ 10%, amber 10–15%, red > 15% | Navigate to exit records |
| Avg Vacancy Fill Time (days) | Average days from vacancy creation to joining, last 12 months | Green if ≤ 30, amber 31–45, red > 45 | Navigate to Recruitment Analytics (page 53) |
| BGV Compliance % | Staff with BGV status = Verified ÷ total staff × 100 | Red if < 90%, amber 90–95%, green ≥ 95% | Navigate to BGV Dashboard (page 34) |
| POCSO Compliance % | Staff with valid POCSO training certificate ÷ total staff × 100 | Red if < 90%, amber 90–99%, green 100% | Navigate to POCSO Compliance page (page 37) |
| Active Grievance Rate | Open grievances ÷ total staff × 1000 (per 1000 staff) | Green if < 5, amber 5–10, red > 10 | Navigate to Grievance Manager (page 43) |

---

## 5. Main Table — Not Applicable

This page does not have a main data table. It is a charts-first analytics dashboard. The main body is a responsive grid of chart panels.

---

## 6. Drawers

No drawers on this page. Drill-down interactions navigate to relevant operational pages with pre-applied filters, rather than opening in-page drawers.

---

## 7. Charts

All charts occupy responsive full-width or half-width panels in a 2-column grid on desktop (single column on mobile). Each panel has a title, subtitle, date-range badge, and Export PNG / Export CSV buttons.

### Chart 1 — Turnover Rate by Branch (Bar Chart)

- **Type:** Vertical grouped bar chart
- **X-axis:** Branch names
- **Y-axis:** Turnover rate % (exits ÷ avg staff)
- **Reference line:** 10% benchmark line in red (industry threshold)
- **Bar colour:** Green if branch ≤ 10%, amber 10–15%, red > 15%
- **Tooltip:** Branch name, turnover %, exit count, avg staff count
- **Drill-down:** Click branch bar → navigates to Exit Management page filtered to that branch and selected date range
- **Width:** Full width

### Chart 2 — Recruitment Funnel by Role Type (Funnel Chart)

- **Type:** Horizontal funnel (stages from widest to narrowest)
- **Stages:** Applications Received → Shortlisted → Interviewed → Offer Made → Offer Accepted → Joined
- **Segmented by:** Role Type (Teaching / Non-Teaching toggle)
- **Each stage:** Shows count and conversion % from previous stage
- **Tooltip:** Stage name, count, conversion rate
- **Drill-down:** Click stage → navigates to Recruitment Analytics (page 53) filtered to that stage
- **Width:** Half width (left column)

### Chart 3 — Training Completion Trend (12-Month Line Chart)

- **Type:** Multi-line chart
- **X-axis:** Last 12 months (month labels)
- **Y-axis:** % of staff who completed at least one CPD training in the month
- **Lines:** One per branch (colour-coded), plus group average (bold black dashed line)
- **Tooltip:** Month, branch name, completion %
- **Drill-down:** Click data point → navigates to Training Dashboard (page 25) filtered to branch and month
- **Width:** Half width (right column)

### Chart 4 — Disciplinary Incidents Trend (Line Chart)

- **Type:** Single-line chart with area fill
- **X-axis:** Last 12 months
- **Y-axis:** Count of new disciplinary cases initiated per month
- **Area fill:** Light red below the line
- **Annotations:** Markers for any months where mass disciplinary action occurred
- **Tooltip:** Month, case count
- **Drill-down:** Click data point → navigates to Disciplinary Case Tracker (page 40) filtered to that month
- **Width:** Half width

### Chart 5 — Staff Strength vs. Sanctioned Posts (Stacked Bar Chart)

- **Type:** Stacked vertical bar
- **X-axis:** Branch names
- **Y-axis:** Headcount
- **Stack A:** Actual filled posts (blue)
- **Stack B:** Vacant posts (red — extends above actual to show sanctioned total)
- **Reference line:** Sanctioned total as a step line
- **Tooltip:** Branch, sanctioned, actual, vacancies, vacancy %
- **Drill-down:** Click branch → navigates to Staff Strength Report (page 51) filtered to branch
- **Width:** Full width

### Chart 6 — BGV Failure Rate by Verification Type (Horizontal Bar Chart)

- **Type:** Horizontal bar
- **Y-axis:** Verification types (Education / Employment / Criminal / Address / Reference)
- **X-axis:** Failure rate % (count of failed/flagged BGV checks ÷ total checks of that type)
- **Tooltip:** Verification type, failure count, total checks, failure %
- **Drill-down:** Click bar → navigates to BGV Dashboard filtered to that verification type
- **Width:** Half width

---

## 8. Toast Messages

| Trigger | Type | Message |
|---|---|---|
| Chart data load error | Warning | "[Chart Name] failed to load. Retrying..." |
| Export PDF initiated | Info | "Generating full analytics report. This may take a few seconds." |
| Export PDF ready | Success | "Analytics report ready. Downloading now." |
| Export CSV downloaded | Success | "Chart data exported as CSV." |
| Date filter applied | Info | "Charts updated for: [date range label]." |
| Server error | Error | "Analytics data unavailable. Please try again later." |

---

## 9. Empty States

**Chart has no data for selected range/branch:**
> Icon: bar chart with question mark (inline within chart panel)
> "[Chart Name]: No data available for the selected date range and branch filters."
> CTA: `Change Filters`

**All charts empty (new group, no historical data):**
> Full-page empty state
> Icon: chart outline
> "No analytics data yet. HR data across the group will appear here as operations begin."

---

## 10. Loader States

- Page load: KPI card skeletons rendered immediately; chart panels render with grey placeholder boxes and pulsing animation
- Each chart loads independently: spinner centred in chart panel; other charts load normally while one is loading
- Export PDF: Button spinner + "Generating..." label while report compiles server-side
- Global filter change: All charts show loading spinner simultaneously while re-fetching
- Drill-down navigation: Brief loading indicator before target page opens

---

## 11. Role-Based UI Visibility

| UI Element | HR Director | HR Manager | T&D Manager | Perf. Review Officer |
|---|---|---|---|---|
| All 6 charts | Visible | Visible | Training chart only | Disciplinary chart only |
| KPI summary bar | All 6 cards | All 6 cards | Training KPI only | Disciplinary KPI only |
| Drill-down links | Active | Disabled (read-only) | Active (training) | Active (disciplinary) |
| Export Full Report | Visible | Visible | Hidden | Hidden |
| Global date/branch filter | Visible | Visible | Visible | Visible |

---

## 12. API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/hr/analytics/kpis/` | KPI summary bar data |
| GET | `/api/hr/analytics/charts/turnover/` | Turnover rate by branch data |
| GET | `/api/hr/analytics/charts/recruitment-funnel/` | Recruitment funnel stage data |
| GET | `/api/hr/analytics/charts/training-trend/` | Training completion trend data |
| GET | `/api/hr/analytics/charts/disciplinary-trend/` | Disciplinary incident trend data |
| GET | `/api/hr/analytics/charts/staff-strength/` | Staff strength vs. sanctioned data |
| GET | `/api/hr/analytics/charts/bgv-failure-rate/` | BGV failure rate by type data |
| GET | `/api/hr/analytics/export/pdf/` | Generate full analytics PDF report |
| GET | `/api/hr/analytics/charts/{chart_id}/csv/` | Export individual chart data as CSV |

All endpoints accept query params: `date_from`, `date_to`, `branch` (comma-separated IDs).

---

## 13. HTMX Patterns

| Interaction | HTMX Attribute | Behaviour |
|---|---|---|
| KPI bar load | `hx-get` on `#kpi-bar` on page render | Fetches KPI data |
| Each chart load | `hx-get` on each `#chart-panel-{n}` independently | Charts load asynchronously, no blocking |
| Global filter change | `hx-get` on all chart panels via `hx-trigger="custom-event from:body"` | JS dispatches custom event on filter change; all charts re-fetch |
| Branch filter change | `hx-include` carries branch param to all chart endpoints | Included in every chart `hx-get` |
| Chart retry (error state) | `hx-get` on retry button inside chart panel | Re-fetches that chart only |
| Export PDF button | `hx-get` on button + `hx-target="#export-status"` | Triggers PDF generation; status updates in dedicated div |
| KPI refresh | KPIs re-fetched when global filters change | Same custom-event trigger as charts |
| Drill-down | Standard `<a>` navigation (no HTMX) | Navigates to operational page with query params pre-populated |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
