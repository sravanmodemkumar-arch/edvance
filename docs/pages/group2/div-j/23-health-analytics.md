# 23 — Health Analytics Dashboard

> **URL:** `/group/health/analytics/`
> **File:** `23-health-analytics.md`
> **Template:** `portal_base.html`
> **Priority:** P1
> **Role:** Group Medical Coordinator (primary) · Group Mental Health Coordinator · Group Emergency Response Officer

---

## 1. Purpose

Cross-branch health intelligence dashboard aggregating data from all Health & Medical modules — patient consultations (Page 09), mental health counselling sessions (Page 13), health screenings (Page 11), emergency incidents (Page 20), and insurance claims (Page 17). The dashboard surfaces trends, patterns, and risk signals that cannot be seen by looking at any single module in isolation.

Primary uses: identifying branches with disproportionately high consultation volumes (possible infrastructure issue), detecting mental health demand spikes correlated with academic stress periods, monitoring drill compliance trends over time, identifying patterns in insurance claim types and rejection rates, and computing a composite branch health score for prioritising group-level health investments and staffing decisions.

This is a read-only analytics page. No data is entered here. All underlying data is maintained in the source modules. Chart data is aggregated server-side and returned via dedicated analytics API endpoints.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Medical Coordinator | G3 | Full view of all 6 analytics sections + export with individual data | Primary user |
| Group Mental Health Coordinator | G3 | Mental health section (5.2) + wellbeing elements of 5.6 only | Cannot see medical/insurance/incident data |
| Group Emergency Response Officer | G3 | Emergency incident section (5.4) + drill compliance chart in 5.4 only | Cannot see medical/mental health/insurance data |
| CEO / Chairman | Group | Full view of all sections | No export that contains individual student data |
| CFO | Group | Insurance & claims section (5.5) only | Financial governance |
| All other roles | — | — | No access |

> **Access enforcement:** `@require_role('medical_coordinator', 'mental_health_coordinator', 'emergency_response_officer', 'ceo', 'chairman', 'cfo')`. Section-level visibility enforced server-side: analytics API endpoints for each section return 403 if role lacks access to that section. HTMX partial updates respect the same enforcement so hidden sections cannot be loaded by manipulating requests.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Health & Medical  ›  Health Analytics
```

### 3.2 Page Header
- **Title:** `Health Analytics`
- **Subtitle:** `Data through [last updated timestamp] · [N] Branches · AY [current year]`
- **Right controls:** `Date Range Selector` · `Export Full Report` (Medical Coordinator only)

### 3.3 Alert Banner

| Condition | Banner Text | Severity |
|---|---|---|
| Export job completed and ready | "Your analytics export is ready. [Download Report]" | Info (dismissable) |
| Data not yet available for current AY (< 30 days of data) | "Analytics data is still accumulating for the current academic year. Some charts may show limited data." | Info |

### 3.4 Date Range Selector

Persistent sticky control at the top of the page (below header). Applies to all charts and sections simultaneously.

| Option | Notes |
|---|---|
| This Month | Current calendar month |
| This Quarter | Current academic quarter |
| This AY | Entire current academic year (default) |
| Last AY | Previous academic year |
| Custom Range | Start date + End date picker; max 3-year span |

On change: all HTMX chart partials triggered simultaneously to reload with new date range.

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule |
|---|---|---|
| Total Consultations (AY to date) | All patient consultations from Page 09 | Blue always |
| Mental Health Sessions (AY to date) | All counselling sessions from Page 13 | Blue always |
| Health Screenings Completed | Total students screened across all screening events (Page 11) | Blue; sub-label shows % of enrolled |
| Emergency Incidents This AY | All incidents from Page 20 | Red > 5 · Yellow 1–5 · Green = 0 |
| Insurance Claims This AY | Total claims from Page 17 | Blue always |
| Branches at Health Risk (composite score) | Branches with composite health score < 60 (see Section 5.6) | Red > 0 · Green = 0 |
| At-Risk Students (active) | Students with active flag in wellbeing tracker (Page 14) | Red > 0 · Amber 1–5 · Green = 0 |
| Branches Fully Health-Compliant | Branches with compliance score ≥ 90% (Page 24) | Blue; sub-label shows % of total branches |

---

## 5. Analytics Sections

All sections are collapsible panels. Default: all expanded. Section order matches role interest priority for Medical Coordinator.

---

### 5.1 Consultation Trends

**Access:** Medical Coordinator, CEO/Chairman only.

**Chart 1 — Weekly Consultation Volume (Line Chart)**
- X-axis: Week number (last 52 weeks from end of selected date range)
- Y-axis: Number of consultations
- Single line: group-wide total
- Hover tooltip: exact count + week date range
- Download as PNG

**Chart 2 — Consultation Volume by Branch (Bar Chart)**
- X-axis: Branch names (sorted descending by volume)
- Y-axis: Consultation count for selected period
- Colour: single colour (primary brand blue)
- Download as PNG or CSV

**Chart 3 — Consultation Type Breakdown (Pie / Donut Chart)**
- Segments: Fever & Infection / Injury & Trauma / Gastrointestinal / Mental Health Related / Dental / Eye / Skin / Other
- Hover: count + percentage
- Legend below chart
- Download as PNG

**Table — Top 10 Complaint Categories**

| Column | Notes |
|---|---|
| Complaint Category | ICD chapter name |
| Count (this period) | |
| Count (previous period) | |
| % Change | Colour-coded: green (decrease) / red (increase > 10%) |

---

### 5.2 Mental Health Trends

**Access:** Medical Coordinator, Mental Health Coordinator, CEO/Chairman.

**Chart 1 — Weekly Counselling Sessions (Line Chart with Series)**
- X-axis: Week (last 52 weeks)
- Y-axis: Session count
- Series lines: Academic Stress / Personal / Hostel / Crisis — each a different colour
- Legend toggleable (click to hide/show series)
- Exam period overlay: shaded vertical bands marking exam periods pulled from academic calendar
- Hover: breakdown by category for that week
- Download as PNG

**Chart 2 — Sessions by Branch (Bar Chart)**
- X-axis: Branch names (descending by volume)
- Y-axis: Session count
- Identifies high-demand branches
- Benchmark line: group average
- Download as PNG or CSV

**Chart 3 — At-Risk Student Count Over Time (Trend Line)**
- X-axis: Month (last 12 months)
- Y-axis: Active at-risk student count at month-end
- Shows trajectory; rising line triggers concern
- Download as PNG

**Exam Overlay Note:** Academic calendar exam periods are automatically overlaid on Charts 1 and 3 as translucent shaded bands. Tooltip on hover of shaded band shows exam name and date range.

---

### 5.3 Health Screening Coverage

**Access:** Medical Coordinator, CEO/Chairman.

**Table — Branch × Screening Type Completion Matrix**

Rows: Branches. Columns: Screening types (Vision / Hearing / Dental / Physical / BMI & Nutrition / Vaccination / Mental Health Screening / Other).
Each cell: Completion % for selected period. Colour: Green ≥ 90% / Yellow 70–90% / Red < 70% / Grey = Not applicable or not scheduled.

**Chart 1 — Students Screened vs Pending by Branch (Stacked Bar Chart)**
- X-axis: Branch names
- Y-axis: Student count
- Stack 1: Screened (green)
- Stack 2: Pending (amber)
- Download as PNG or CSV

**Chart 2 — Types of Abnormal Findings (Pie / Donut Chart)**
- Aggregated across all completed screenings in period
- Segments: Vision deficiency / Hearing impairment / Dental caries / Underweight / Overweight/Obese / Vaccination gap / Other
- Hover: count + percentage
- Download as PNG

---

### 5.4 Emergency & Incident Analytics

**Access:** Medical Coordinator, Emergency Response Officer, CEO/Chairman.

**Chart 1 — Incidents by Type This AY (Bar Chart)**
- X-axis: Incident types (Medical / Fire / Natural Disaster / Transport / Missing / Security / Other)
- Y-axis: Count
- Colour-coded by type (consistent with incident register badges)
- Download as PNG or CSV

**Chart 2 — Incidents Over Last 24 Months (Trend Line)**
- X-axis: Month (last 24 months)
- Y-axis: Incident count
- Single line: total incidents per month
- Optional overlay: severity 3+ incidents as separate line
- Download as PNG

**Table — Top 5 Branches by Incident Count**

| Column | Notes |
|---|---|
| Branch | |
| Incident Count | Selected period |
| Critical Incidents (Sev 4–5) | Count |
| Average Response Time (mins) | |
| Open Post-Incident Reviews | Count |

**Chart 3 — Drill Compliance (Grouped Bar Chart)**
- X-axis: Drill types (Fire × 2 / Medical × 1 / Earthquake × 1 / Missing Student × 1)
- Y-axis: % of branches that have completed the required number of this drill type
- Target line at 100%
- Download as PNG or CSV

---

### 5.5 Insurance & Claims Analytics

**Access:** Medical Coordinator, CFO, CEO/Chairman.

**Chart 1 — Claims Filed vs Settled vs Rejected (Grouped Bar Chart, Monthly)**
- X-axis: Month (last 12 months)
- Y-axis: Count
- Three bar groups per month: Filed (blue) / Settled (green) / Rejected (red)
- Download as PNG or CSV

**Chart 2 — Claim Amounts by Type (Stacked Bar Chart)**
- X-axis: Claim type (Accident / Hospitalisation / Death)
- Y-axis: Total ₹ amount
- Stacks: Claimed (blue) / Approved (green) / Rejected (red)
- Download as PNG or CSV

**Table — Average Settlement Time by Insurer**

| Column | Notes |
|---|---|
| Insurer Name | |
| Claims Filed | Count in selected period |
| Claims Settled | Count |
| Average Settlement Days | Mean days from filed to settled |
| Rejection Rate % | Rejected / Filed × 100 |

**Chart 3 — Claim Rejection Reasons (Pie / Donut Chart)**
- Aggregated from all rejected claims in selected period
- Segments: Non-covered procedure / Incomplete documentation / Late filing / Pre-existing condition exclusion / Duplicate claim / Other
- Hover: count + percentage
- Download as PNG

---

### 5.6 Branch Health Score (Composite)

**Access:** Medical Coordinator, CEO/Chairman.

**Table — Branch Health Score Summary**

| Column | Notes |
|---|---|
| Branch | Branch name; click → compliance detail (Page 24 branch drawer) |
| Medical Room Score | 0–100 sub-score |
| Doctor Visit Compliance | 0–100 sub-score |
| First Responder Coverage | 0–100 sub-score |
| Incident Rate Score | 0–100 sub-score (inverse: higher = fewer incidents) |
| Mental Health Coverage | 0–100 sub-score |
| Overall Score (0–100) | Weighted average of 6 sub-scores |
| Trend | Arrow: ↑ improving / ↓ declining / → stable vs last month; colour-coded |

Default sort: Overall Score ascending (worst-performing first — enables intervention targeting).

**Heatmap — Branch × Health Dimension**
- Rows: all branches (up to 50)
- Columns: 6 health dimensions (Medical Room / Doctor Visit / First Responder / Incident Rate / Mental Health / Overall)
- Cell colour: Green ≥ 80 / Yellow 60–80 / Orange 40–60 / Red < 40
- Cell value: numeric score shown inside cell
- Hover: tooltip with sub-score breakdown
- Click cell: links to relevant compliance item on Page 24
- Download heatmap as PNG

**Filter for heatmap:** Sort by overall score ascending / descending. Filter by zone (if group uses geographical zones for branches).

---

## 6. Drawers / Modals

No drawers or modals on this page. This is a fully read-only analytics dashboard. All drill-down interactions (clicking a branch name in Table 5.6) navigate to the relevant source page (Page 24 — Compliance Report) with filters pre-applied.

Export is the only non-view action. Export triggers an async background job and notifies via toast and notification bell when ready.

---

## 7. Toast Messages

| Action | Toast Text | Type |
|---|---|---|
| Export initiated | "Analytics report export initiated. You will be notified when the download is ready." | Info |
| Export ready | "Your analytics export is ready. [Download Report]" | Success (persistent until dismissed or downloaded) |
| Export failed | "Export failed. Please retry or contact IT support." | Error |
| Chart data loaded | No toast — silent load | — |
| Insufficient data for chart (< 3 data points) | Inline notice within chart area: "Insufficient data to render this chart for the selected period." | Inline info (not toast) |

---

## 8. Empty States

| Context | Heading | Sub-text | Action |
|---|---|---|---|
| No data at all for selected period | "No health data available for the selected date range." | "Adjust the date range or ensure data has been entered in the source modules." | Date range selector |
| Specific chart — insufficient data (< 3 data points) | "Insufficient data for this chart." | "At least 3 data points are needed to render this chart. Try expanding the date range." | — |
| Mental health section — no counselling records | "No counselling sessions recorded yet." | "Mental health trend data will appear once sessions are logged in the Counselling Session Register." | — |
| Screening matrix — no screenings | "No health screenings recorded." | "Screening completion data will appear once screening events are completed." | — |
| Insurance section — no claims | "No insurance claims this period." | "Claims analytics will appear once claims are filed in the Insurance Claim Register." | — |
| Branch health score — no compliance data | "Branch health scores are not yet computed." | "Scores are calculated from compliance data. Ensure compliance data is up to date." | — |

---

## 9. Loader States

| Context | Loader Behaviour |
|---|---|
| Initial page load | Full-page skeleton: 8 KPI cards + 6 section panels each with chart placeholders (grey rounded rectangles) |
| Date range change | All chart partials reload simultaneously; each shows spinner overlay on its chart area |
| Individual chart HTMX partial | Spinner overlay on that chart area while data loads; adjacent charts unaffected |
| KPI bar refresh | KPI bar skeleton (8 grey cards) while refreshing |
| Export job submission | Export button replaced with spinner + "Preparing…" label |
| Section collapse / expand | Instant (no API call needed — data already loaded) |
| Heatmap render | Heatmap placeholder with progress indicator "Computing branch scores…" for first load |
| Table sort (client-side) | Instant re-sort; no API call |

---

## 10. Role-Based UI Visibility

| UI Element | Medical Coordinator | Mental Health Coordinator | Emergency Response Officer | CEO / Chairman | CFO |
|---|---|---|---|---|---|
| Section 5.1 — Consultation Trends | ✅ | ❌ | ❌ | ✅ | ❌ |
| Section 5.2 — Mental Health Trends | ✅ | ✅ | ❌ | ✅ | ❌ |
| Section 5.3 — Health Screening Coverage | ✅ | ❌ | ❌ | ✅ | ❌ |
| Section 5.4 — Emergency & Incident Analytics | ✅ | ❌ | ✅ | ✅ | ❌ |
| Section 5.5 — Insurance & Claims Analytics | ✅ | ❌ | ❌ | ✅ | ✅ |
| Section 5.6 — Branch Health Score | ✅ | ❌ | ❌ | ✅ | ❌ |
| KPI bar — all 8 cards | ✅ | Mental health cards only | Incident + drill cards only | ✅ | Insurance cards only |
| Date Range Selector | ✅ | ✅ | ✅ | ✅ | ✅ |
| Export Full Report (with individual data) | ✅ | ❌ | ❌ | ❌ | ❌ |
| Export (aggregated, no individual data) | ✅ | ✅ (mental health section) | ✅ (incident section) | ✅ | ✅ (insurance section) |
| Chart download (PNG/CSV) | ✅ | Own sections | Own sections | ✅ | Own sections |
| Branch drill-down links | ✅ | ❌ | ❌ | ✅ | ❌ |
| Alert banners | ✅ | ✅ | ✅ | ✅ | ✅ |

---

## 11. API Endpoints

### Base URL: `/api/v1/group/{group_id}/health/analytics/`

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/health/analytics/kpi/` | 8 KPI summary cards (role-filtered) | JWT + role check |
| GET | `/api/v1/group/{group_id}/health/analytics/consultations/trend/` | Weekly consultation trend (52 weeks) | Medical Coordinator / CEO / Chairman |
| GET | `/api/v1/group/{group_id}/health/analytics/consultations/by-branch/` | Consultation volume by branch | Medical Coordinator / CEO / Chairman |
| GET | `/api/v1/group/{group_id}/health/analytics/consultations/by-type/` | Consultation type breakdown | Medical Coordinator / CEO / Chairman |
| GET | `/api/v1/group/{group_id}/health/analytics/consultations/top-complaints/` | Top 10 complaint categories with period-over-period change | Medical Coordinator / CEO / Chairman |
| GET | `/api/v1/group/{group_id}/health/analytics/mental-health/trend/` | Weekly counselling sessions by category (52 weeks) | Medical Coordinator / Mental Health Coordinator / CEO / Chairman |
| GET | `/api/v1/group/{group_id}/health/analytics/mental-health/by-branch/` | Sessions by branch | Medical Coordinator / Mental Health Coordinator / CEO / Chairman |
| GET | `/api/v1/group/{group_id}/health/analytics/mental-health/at-risk-trend/` | At-risk student count over 12 months | Medical Coordinator / Mental Health Coordinator / CEO / Chairman |
| GET | `/api/v1/group/{group_id}/health/analytics/mental-health/exam-overlay/` | Exam period date ranges for chart overlay | Medical Coordinator / Mental Health Coordinator / CEO / Chairman |
| GET | `/api/v1/group/{group_id}/health/analytics/screening/matrix/` | Branch × screening type completion matrix | Medical Coordinator / CEO / Chairman |
| GET | `/api/v1/group/{group_id}/health/analytics/screening/by-branch/` | Screened vs pending by branch | Medical Coordinator / CEO / Chairman |
| GET | `/api/v1/group/{group_id}/health/analytics/screening/findings/` | Abnormal findings breakdown | Medical Coordinator / CEO / Chairman |
| GET | `/api/v1/group/{group_id}/health/analytics/incidents/by-type/` | Incident count by type for selected period | Medical Coordinator / Emergency Response Officer / CEO / Chairman |
| GET | `/api/v1/group/{group_id}/health/analytics/incidents/trend/` | Monthly incident trend (24 months) | Medical Coordinator / Emergency Response Officer / CEO / Chairman |
| GET | `/api/v1/group/{group_id}/health/analytics/incidents/top-branches/` | Top 5 branches by incident count | Medical Coordinator / Emergency Response Officer / CEO / Chairman |
| GET | `/api/v1/group/{group_id}/health/analytics/incidents/drill-compliance/` | Drill completion % by type | Medical Coordinator / Emergency Response Officer / CEO / Chairman |
| GET | `/api/v1/group/{group_id}/health/analytics/claims/monthly/` | Monthly claims filed/settled/rejected (12 months) | Medical Coordinator / CFO / CEO / Chairman |
| GET | `/api/v1/group/{group_id}/health/analytics/claims/by-type/` | Claim amounts stacked by type | Medical Coordinator / CFO / CEO / Chairman |
| GET | `/api/v1/group/{group_id}/health/analytics/claims/insurer-settlement/` | Settlement time by insurer | Medical Coordinator / CFO / CEO / Chairman |
| GET | `/api/v1/group/{group_id}/health/analytics/claims/rejection-reasons/` | Rejection reason breakdown | Medical Coordinator / CFO / CEO / Chairman |
| GET | `/api/v1/group/{group_id}/health/analytics/branch-health-score/` | Branch composite health scores and sub-scores | Medical Coordinator / CEO / Chairman |
| GET | `/api/v1/group/{group_id}/health/analytics/branch-health-score/heatmap/` | Heatmap data (branch × dimension matrix) | Medical Coordinator / CEO / Chairman |
| POST | `/api/v1/group/{group_id}/health/analytics/export/` | Initiate async export job | Medical Coordinator (full) / others (section-specific) |
| GET | `/api/v1/group/{group_id}/health/analytics/export/{job_id}/status/` | Poll export job status | Same as POST access |
| GET | `/api/v1/group/{group_id}/health/analytics/export/{job_id}/download/` | Download completed export | Same as POST access |

**Query parameters for all chart endpoints:**

| Parameter | Type | Description |
|---|---|---|
| `period` | str | `this_month`, `this_quarter`, `this_ay`, `last_ay`, `custom` |
| `date_from` | date | Required if `period=custom` |
| `date_to` | date | Required if `period=custom` |
| `branch` | int[] | Optional branch filter (applies to by-branch charts) |

---

## 12. HTMX Patterns

| Interaction | HTMX Attributes | Behaviour |
|---|---|---|
| Date range selector change | Broadcasts `dateRangeChanged` event; all chart HTMX targets listen to this event | All section partials reload simultaneously |
| KPI bar reload | `hx-get="/api/.../analytics/kpi/"` `hx-trigger="load, dateRangeChanged from:body"` `hx-target="#kpi-bar"` | On load and on date range change |
| Consultation trend chart | `hx-get="/api/.../analytics/consultations/trend/"` `hx-trigger="load, dateRangeChanged from:body"` `hx-target="#chart-consultation-trend"` `hx-indicator="#spinner-consultation-trend"` | Chart partial replaced |
| Consultation by-branch chart | `hx-get="/api/.../analytics/consultations/by-branch/"` `hx-trigger="load, dateRangeChanged from:body"` `hx-target="#chart-consultation-branch"` `hx-indicator="#spinner-consultation-branch"` | Chart partial replaced |
| Consultation type pie chart | `hx-get="/api/.../analytics/consultations/by-type/"` `hx-trigger="load, dateRangeChanged from:body"` `hx-target="#chart-consultation-type"` | Chart partial replaced |
| Top complaints table | `hx-get="/api/.../analytics/consultations/top-complaints/"` `hx-trigger="load, dateRangeChanged from:body"` `hx-target="#table-top-complaints"` | Table replaced |
| Mental health trend chart | `hx-get="/api/.../analytics/mental-health/trend/"` `hx-trigger="load, dateRangeChanged from:body"` `hx-target="#chart-mh-trend"` | Chart partial replaced |
| Mental health by-branch chart | `hx-get="/api/.../analytics/mental-health/by-branch/"` `hx-trigger="load, dateRangeChanged from:body"` `hx-target="#chart-mh-branch"` | Chart partial replaced |
| At-risk trend chart | `hx-get="/api/.../analytics/mental-health/at-risk-trend/"` `hx-trigger="load, dateRangeChanged from:body"` `hx-target="#chart-at-risk"` | Chart partial replaced |
| Screening matrix load | `hx-get="/api/.../analytics/screening/matrix/"` `hx-trigger="load, dateRangeChanged from:body"` `hx-target="#table-screening-matrix"` | Matrix table replaced |
| Screening by-branch chart | `hx-get="/api/.../analytics/screening/by-branch/"` `hx-trigger="load, dateRangeChanged from:body"` `hx-target="#chart-screening-branch"` | Chart partial replaced |
| Incident by-type chart | `hx-get="/api/.../analytics/incidents/by-type/"` `hx-trigger="load, dateRangeChanged from:body"` `hx-target="#chart-incident-type"` | Chart partial replaced |
| Incident trend chart | `hx-get="/api/.../analytics/incidents/trend/"` `hx-trigger="load, dateRangeChanged from:body"` `hx-target="#chart-incident-trend"` | Chart partial replaced |
| Drill compliance chart | `hx-get="/api/.../analytics/incidents/drill-compliance/"` `hx-trigger="load, dateRangeChanged from:body"` `hx-target="#chart-drill-compliance"` | Chart partial replaced |
| Claims monthly chart | `hx-get="/api/.../analytics/claims/monthly/"` `hx-trigger="load, dateRangeChanged from:body"` `hx-target="#chart-claims-monthly"` | Chart partial replaced |
| Claims by-type chart | `hx-get="/api/.../analytics/claims/by-type/"` `hx-trigger="load, dateRangeChanged from:body"` `hx-target="#chart-claims-type"` | Chart partial replaced |
| Insurer settlement table | `hx-get="/api/.../analytics/claims/insurer-settlement/"` `hx-trigger="load, dateRangeChanged from:body"` `hx-target="#table-insurer-settlement"` | Table replaced |
| Branch health score table | `hx-get="/api/.../analytics/branch-health-score/"` `hx-trigger="load, dateRangeChanged from:body"` `hx-target="#table-branch-score"` | Table replaced |
| Heatmap load | `hx-get="/api/.../analytics/branch-health-score/heatmap/"` `hx-trigger="load, dateRangeChanged from:body"` `hx-target="#heatmap-container"` `hx-indicator="#heatmap-spinner"` | Heatmap container replaced; JS chart renders from returned data |
| Export initiate | `hx-post="/api/.../analytics/export/"` `hx-target="#export-status"` `hx-trigger="click"` | Export button replaced with "Preparing…" indicator |
| Export status poll | `hx-get="/api/.../analytics/export/{job_id}/status/"` `hx-trigger="every 5s [exportPending]"` `hx-target="#export-status"` | Polls every 5 seconds until job complete; on complete, replaced by Download link and `exportPending` condition cleared |
| Section collapse toggle | Client-side only (no HTMX) | Section body hidden/shown via CSS class toggle; no API call |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
