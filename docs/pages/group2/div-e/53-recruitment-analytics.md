# 53 — Recruitment Analytics

- **URL:** `/group/hr/recruitment/analytics/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Role:** Group HR Manager (Role 42, G3) + Group HR Director (Role 41, G3)

---

## 1. Purpose

Recruitment Analytics is the strategic intelligence layer for the group's recruitment function. While the operational recruitment pipeline pages (Teaching Recruitment Pipeline, page 18, and Non-Teaching Recruitment Pipeline, page 19) manage individual candidates through the hiring process, this page answers the structural questions that those operational views cannot: Where do the best candidates come from? Which subjects are chronically hard to fill? Which branches are struggling to attract candidates — and is that a location problem or a compensation problem? What is the group's cost per hire? How many recruits pass probation and convert to permanent staff?

This page is primarily consumed by the Group HR Manager for month-to-month operational tuning of the recruitment function, and by the Group HR Director for strategic planning, budget justification, and board reporting. The analytics on this page directly inform: annual recruitment budget allocation (cost per hire trend determines next year's estimate), source channel investment decisions (if employee referrals produce 40% of hires but only 10% of applications, increase referral incentives), and recruitment team performance assessment (fill time by recruiter is visible here, though shown at aggregate level to avoid individual targeting without HR Director review).

Key analytics dimensions: Source Analysis (where are hired candidates coming from — Employee Referral, Job Board, Walk-in, Campus Recruitment Drive, Social Media, Consultancy), Supply Gap Analysis by Subject (which teaching subjects have the lowest application volumes relative to vacancies — structural market supply problem), Offer Acceptance Rate by Branch (branches with low acceptance rates may have compensation, location, or culture issues worth investigating), Time-to-Hire by role type (average days from vacancy creation to candidate joining — separated by Teaching and Non-Teaching), Cost per Hire (recruiters' time + advertising spend + consultancy fees ÷ hires), and Quality of Hire (% of recruits from a given source or period who pass the 90-day probation and convert to permanent employment).

All charts are interactive — clicking any chart element applies a filter and updates supporting charts simultaneously. Date range and branch filters are global and apply to all charts. Export functions produce both PNG (for presentations) and CSV (for further analysis in spreadsheet tools).

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group HR Manager | G3 | Full access — all charts, all branches, export | Primary operator |
| Group HR Director | G3 | Full access — all charts, drill-down, export | Oversight and strategic use |
| Group Recruiter — Teaching | G0 | No EduForge access | Briefed on findings by HR Manager |
| Group Recruiter — Non-Teaching | G0 | No EduForge access | Same as above |
| Group Training & Development Manager | G2 | Read-only — Probation Pass Rate chart only | Training relevance |
| All other roles | — | No access | Page not rendered |

---

## 3. Page Layout

### 3.1 Breadcrumb

```
Group Portal › HR & Staff › Recruitment › Recruitment Analytics
```

### 3.2 Page Header

- **Title:** Recruitment Analytics
- **Subtitle:** Source analysis, time-to-hire, offer conversion, and quality of hire across the group
- **Global Filters (apply to all charts):**
  - Date Range: Dropdown — Last 30 Days / Last 3 Months / This Academic Year (default) / Custom range (date picker pair)
  - Branch: Multi-select dropdown — All Branches (default)
  - Role Type: Toggle — All / Teaching / Non-Teaching
- **Secondary CTA:** `Export Full Analytics Report` (PDF — all charts compiled)
- **Last updated badge:** "Data refreshed daily at midnight"

### 3.3 Alert Banner (conditional)

- **Amber:** `Offer acceptance rate dropped below 60% in [N] branches this month.` Action: `View Branches`
- **Red:** `Average time-to-hire for Teaching roles exceeds 45 days. Recruitment bottleneck detected.`
- **Blue:** Data is refreshed nightly. Real-time candidate data is available on the pipeline pages.
- **Green:** Recruitment metrics within healthy ranges — shown when no active alerts

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Total Hires This AY | Count of candidates with joining_date in current academic year | Blue always | Navigate to pipeline pages |
| Time-to-Hire Teaching (avg days) | Avg(joining_date − vacancy_created_date) for Teaching hires | Green if ≤ 30, amber 31–45, red > 45 | No drill-down |
| Time-to-Hire Non-Teaching (avg days) | Avg(joining_date − vacancy_created_date) for Non-Teaching hires | Green if ≤ 21, amber 22–35, red > 35 | No drill-down |
| Offer Acceptance Rate % | Offers accepted ÷ offers made × 100 | Green if ≥ 80%, amber 70–79%, red < 70% | No drill-down |
| Source-wise Hire Distribution | Text: Top source (e.g., "Job Board — 42%") | Blue always | See Source Distribution chart |
| Probation Pass Rate % | Recruits who passed 90-day probation ÷ total recruits × 100, last 12 months | Green if ≥ 85%, amber 75–84%, red < 75% | No drill-down |

---

## 5. Main Table — Not Applicable

This page is a charts-first analytics dashboard. No main tabular data register exists here. All data is presented through interactive charts. Supporting detail for each chart is accessible via drill-down to the respective operational pipeline page.

---

## 6. Drawers

No drawers on this page. Drill-down interactions navigate to relevant operational pages (Teaching Pipeline page 18 or Non-Teaching Pipeline page 19) with pre-applied filters from the chart selection. These navigations open in the same tab with a back-navigation breadcrumb.

---

## 7. Charts

Charts are arranged in a 2-column grid on desktop (full width on mobile). Each chart panel has a title, description line, date-range badge, and Export PNG / Export CSV buttons in the panel header.

### Chart 1 — Recruitment Funnel by Role Type (Funnel Chart)

- **Type:** Vertical funnel chart (standard conversion funnel)
- **Stages:** Applications Received → Screened (Resume shortlisted) → Interview Scheduled → Interview Completed → Offer Made → Offer Accepted → Joined
- **Toggle:** Teaching / Non-Teaching (switches funnel data set)
- **Each stage:** Shows absolute count and conversion % from previous stage (attrition highlighted where it is highest)
- **Tooltip:** Stage name, count, conversion from previous stage, drop-off count
- **Drill-down:** Click stage → pipeline page filtered to that stage and selected date range
- **Width:** Full width

### Chart 2 — Source-wise Hire Distribution (Pie Chart)

- **Type:** Donut pie chart
- **Segments:** Employee Referral / Job Board (Naukri, LinkedIn, etc.) / Walk-in / Campus Drive / Social Media / Consultancy / Other
- **Each segment:** % of total hires and absolute count
- **Centre label:** Total Hires
- **Tooltip:** Source name, hire count, percentage
- **Drill-down:** Click segment → pipeline page filtered to that source
- **Width:** Half width (left column)

### Chart 3 — Time-to-Hire Trend by Month (Line Chart)

- **Type:** Multi-line chart
- **X-axis:** Last 12 months
- **Y-axis:** Average days to hire
- **Line 1:** Teaching roles (blue)
- **Line 2:** Non-Teaching roles (green)
- **Reference lines:** 30-day benchmark (blue dashed) and 21-day benchmark (green dashed)
- **Tooltip:** Month, teaching avg days, non-teaching avg days
- **Width:** Half width (right column)

### Chart 4 — Offer Decline Reasons (Bar Chart)

- **Type:** Horizontal bar chart (only hires where offer was declined, not accepted)
- **Y-axis:** Decline reasons (Compensation Below Expectation / Location Issues / Accepted Competitor Offer / Role Mismatch / Personal Reasons / No Response)
- **X-axis:** Count of offers declined for that reason
- **Bar colour:** Single colour (red) — this is a problem-surfacing chart
- **Tooltip:** Reason, count, percentage of total declines
- **Width:** Half width (left column)

### Chart 5 — Vacancy Age Distribution (Histogram)

- **Type:** Histogram (grouped bars)
- **X-axis:** Vacancy age buckets: 0–15 days / 16–30 days / 31–45 days / 46–60 days / 60+ days
- **Y-axis:** Count of vacancies in each bucket (currently open vacancies)
- **Bar colour:** Green (0–30), amber (31–45), red (46+)
- **Tooltip:** Age bucket, vacancy count, % of open vacancies
- **Width:** Half width (right column)

### Chart 6 — Probation Pass Rate by Source (Bar Chart)

- **Type:** Grouped vertical bar chart
- **X-axis:** Hire sources (same 7 as pie chart)
- **Y-axis:** Probation pass rate %
- **Reference line:** 85% benchmark (dashed)
- **Bar colour:** Green if ≥ 85%, amber 75–84%, red < 75%
- **Tooltip:** Source, pass count, total recruits from source, pass rate %
- **Annotation:** "Higher pass rate = better quality-of-hire from that source"
- **Width:** Full width

---

## 8. Toast Messages

| Trigger | Type | Message |
|---|---|---|
| Export PDF initiated | Info | "Generating recruitment analytics report. This may take a few seconds." |
| Export PDF ready | Success | "Recruitment analytics report downloaded." |
| Chart data load error | Warning | "[Chart Name] failed to load. Retrying..." |
| Filter applied | Info | "Analytics updated for: [filter description]." |
| No data for selected range | Warning | "No recruitment data available for the selected date range and filters." |
| Server error | Error | "Analytics data unavailable. Please retry later." |

---

## 9. Empty States

**Chart has no data:**
> Icon: bar chart with question mark (inline in chart panel)
> "[Chart Name]: No data for the selected range and filters."
> CTA: `Widen Date Range`

**Page-level empty state (new group, no recruitment data):**
> Icon: magnifying glass with person
> "No recruitment data has been recorded yet."
> "Recruitment analytics will populate as candidates move through the pipeline."
> CTA: `Go to Teaching Pipeline`

---

## 10. Loader States

- Page load: KPI card skeletons + chart panel placeholders (grey boxes with pulse animation)
- Each chart loads independently: spinner centred in chart panel; other charts unaffected
- Filter change: All charts simultaneously show loading spinner; KPI bar also refreshes
- Export PDF: Button shows spinner + "Generating..." while compiling
- Drill-down navigation: Brief loader before navigating to pipeline page

---

## 11. Role-Based UI Visibility

| UI Element | HR Manager | HR Director | T&D Manager |
|---|---|---|---|
| All 6 charts | Visible | Visible | Probation Pass Rate only |
| All KPI cards | Visible | Visible | Probation Pass Rate card only |
| Export Full Report | Visible | Visible | Hidden |
| Chart CSV export | Visible | Visible | Visible (for visible chart only) |
| Drill-down links to pipeline pages | Active | Active | Hidden |
| Global date/branch/role filter | Visible | Visible | Visible |
| Source-wise chart | Visible | Visible | Hidden |
| Offer Decline Reasons chart | Visible | Visible | Hidden |

---

## 12. API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/hr/recruitment/analytics/kpis/` | KPI summary bar data |
| GET | `/api/hr/recruitment/analytics/charts/funnel/` | Recruitment funnel stage data |
| GET | `/api/hr/recruitment/analytics/charts/source-distribution/` | Source-wise hire distribution |
| GET | `/api/hr/recruitment/analytics/charts/time-to-hire/` | Time-to-hire trend by month |
| GET | `/api/hr/recruitment/analytics/charts/offer-decline-reasons/` | Offer decline reason breakdown |
| GET | `/api/hr/recruitment/analytics/charts/vacancy-age/` | Vacancy age distribution data |
| GET | `/api/hr/recruitment/analytics/charts/probation-pass-rate/` | Probation pass rate by source |
| GET | `/api/hr/recruitment/analytics/export/pdf/` | Generate full analytics PDF |
| GET | `/api/hr/recruitment/analytics/charts/{chart_id}/csv/` | Export chart data as CSV |

All endpoints accept: `date_from`, `date_to`, `branch` (comma-separated IDs), `role_type` (teaching/non-teaching/all).

---

## 13. HTMX Patterns

| Interaction | HTMX Attribute | Behaviour |
|---|---|---|
| KPI bar load | `hx-get` on `#kpi-bar` on page render | Fetches KPI data with default filters |
| Each chart load | `hx-get` on each `#chart-panel-{n}` independently | Async load; no chart blocks another |
| Global filter change | JS dispatches `filter-changed` custom event; all chart panels listen | All charts and KPI bar re-fetch simultaneously |
| Role type toggle | Included in custom event payload | Charts re-fetch with role_type param |
| Chart retry | `hx-get` on Retry button inside failed chart panel | Re-fetches that chart only |
| Export PDF | `hx-get` on export button + `hx-target="#export-status"` | Triggers server-side PDF generation |
| Drill-down | Standard `<a>` with pre-built query params (no HTMX) | Navigates to pipeline page with filters |
| Chart CSV export | Standard `<a>` with download attribute | Direct CSV download from API |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
