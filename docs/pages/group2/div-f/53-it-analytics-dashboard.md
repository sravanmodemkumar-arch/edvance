# Page 53: IT Analytics Dashboard

**URL:** `/group/it/analytics/`
**Role:** Group IT Director (Role 53, G4)
**Priority:** P1
**Division:** F — Group IT & Technology

---

## 1. Purpose

Strategic IT analytics dashboard for the IT Director. Aggregates data from all IT sub-functions to surface platform adoption trends, capacity planning insights, support performance, integration reliability, security posture, and storage growth. Used for quarterly IT strategy reviews, Board reporting, budget planning, and identifying branches that need targeted IT intervention.

Unlike the operational pages (tickets, incidents, health monitor), this page is designed for strategic decision-making — looking at 12-month trends, cross-function correlations, and executive-level metrics rather than day-to-day operations.

**Use cases:**
- Quarterly IT Board presentation preparation
- Annual IT budget planning (storage growth → capacity costs; ticket rate → staffing needs)
- Identifying low-adoption branches requiring training or change management support
- Demonstrating ROI of security investments (lower phishing click rates, faster incident resolution)
- Integration reliability reporting to vendor/EduForge SLAs

All data sourced from PostgreSQL. All charts have export (PNG) functionality. Page-level filters (branch, date range) cascade to all charts where applicable.

---

## 2. Role Access

| Role | Access Level | Notes |
|------|-------------|-------|
| Group IT Director (Role 53, G4) | Full access | View all charts + export |
| Group EduForge Integration Manager (Role 58, G4) | Limited view | View integration-related charts only (Charts 1, 4) |
| Group IT Admin (Role 54, G4) | Read access | View all; no export of raw data |
| All other roles | No access | Returns 403 |
| Group Data Privacy Officer (Role 55, G1) | No access | Returns 403 |
| Group Cybersecurity Officer (Role 56, G1) | No access | Returns 403 |
| Group IT Support Executive (Role 57, G3) | No access | Returns 403 |

---

## 3. Page Layout

**Breadcrumb:**
`Group Portal > IT & Technology > IT Analytics Dashboard`

**Page Header:**
- Title: `IT Analytics Dashboard`
- Subtitle: `Strategic analytics across all IT functions — quarterly review and budget planning`
- Right side: `Export All Charts (PDF)` button (Role 53 only)

**Page-Level Filters (prominent bar below header):**
- **Date Range:** Last 3 months / Last 6 months / Last 12 months / Custom (default: Last 12 months)
- **Branch:** Multi-select dropdown (All Branches by default)
- `Apply Filters` button → all charts reload with `hx-include`

**Alert Banners:**

1. **Low Platform Adoption** (amber, dismissible):
   - Condition: Platform Adoption Rate < 80%
   - Text: `Platform adoption is [X]% — [X] eligible users have not logged in for 30+ days. Consider targeted outreach.`

2. **Storage Approaching Threshold** (amber, dismissible):
   - Condition: R2 storage > 80% of allocated capacity
   - Text: `Cloudflare R2 storage is at [X]GB ([Y]% capacity). Review storage plan and consider cleanup or upgrade.`

---

## 4. KPI Summary Bar

Six KPI cards in a 6-column responsive grid (3-column on tablet, 2-column on mobile).

| # | Metric | Calculation | Visual |
|---|--------|-------------|--------|
| 1 | Platform Adoption Rate | (users who logged in at least once in last 30 days / total active user accounts) × 100 | % — green ≥ 80%, amber 60–79%, red < 60% |
| 2 | Feature Adoption | Average number of distinct portal features used per branch in last 30 days (out of total available features) | Score e.g. `8.2 / 14 features` |
| 3 | Support Ticket Rate | (total support tickets raised in last 30 days / total active users) × 100 | Tickets per 100 users — lower is better |
| 4 | Integration Reliability % | (successful_api_calls / total_api_calls) × 100 across all active integrations in last 30 days | % — red < 99%, amber 99–99.5%, green > 99.5% |
| 5 | Security Score Trend | Difference between this month's group security score and last month's | `↑ +X` (green) / `↓ -X` (red) / `→ No change` (grey) |
| 6 | Storage Used (Cloudflare R2) | Total GB stored in R2 across all branches | `X.X GB` — with allocated capacity context |

---

## 5. Main Table

No primary data table on this page (analytics/charts-focused). The main content area is the 6-chart grid.

However, below the charts there is a **Branch Performance Summary Table** — a compact read-only table providing per-branch context:

**Table Title:** `Branch IT Performance Summary`

| Branch | Adoption Rate | Feature Adoption | Tickets (30d) | Ticket Rate | Security Score | Integration Errors | Storage (GB) |
|--------|--------------|-----------------|---------------|-------------|----------------|--------------------|-------------|
| ... | ... | ... | ... | ... | ... | ... | ... |

- Colour coding: Each metric column colour-coded (green/amber/red thresholds)
- No actions column (read-only analytics)
- Pagination: Server-side, 15 rows per page
- Sorting: By any column; default: Adoption Rate ascending (lowest first)

**Note:** No action column — this table is read-only. Branch drill-down detail is available by clicking the branch name row.

---

## 6. Drawers

No create/edit drawers on this analytics page. One informational drawer:

### Chart Detail Drawer (640px — expanding a chart to full-screen view)

Triggered by `Expand` icon on each chart card.

- Full-width rendering of the selected chart
- Additional filter options specific to the chart (e.g., select individual branches for the heatmap)
- `Export PNG` button
- `Export Data (CSV)` button (Role 53 only)
- `Close` button

---

## 7. Charts

Six charts in a 2-column responsive grid (1-column on mobile). Each chart card has a header with: Chart Title, filter icon (expand filter options), expand icon, export PNG button.

### Chart 1: Monthly Active Users Trend
- **Type:** Line chart
- **Series:** Total monthly active users (group) as solid line; individual branch series available as toggle
- **X-axis:** Last 12 months
- **Y-axis:** Unique user count (users who logged in ≥ 1 session in the month)
- **Reference line:** Total registered users (dashed — shows gap between registered and active)
- **Purpose:** Track whether platform adoption is growing, stable, or declining
- **Additional filter:** Branch multi-select toggle
- **Data endpoint:** `/api/v1/it/analytics/charts/mau-trend/`

### Chart 2: Feature Adoption by Branch (Heatmap)
- **Type:** Heatmap grid
- **Rows:** Branch names
- **Columns:** Feature names (e.g., Fee Collection, Student Registration, Attendance, Reports, Timetable, Notifications, Parent Portal, etc.)
- **Cell colour:** Heat intensity from white (0% usage) to dark green (100% branch staff using that feature)
- **Cell value:** % of branch staff who used the feature in last 30 days
- **Purpose:** Identify which features are underutilised in specific branches — guides training and onboarding priorities
- **Data endpoint:** `/api/v1/it/analytics/charts/feature-heatmap/`

### Chart 3: Support Ticket Volume Trend with SLA Overlay
- **Type:** Combination chart
- **Primary series (bars):** Monthly ticket volume (grouped by priority — P1/P2/P3 stacked bars)
- **Secondary series (line, secondary Y-axis):** SLA compliance % (0–100%)
- **X-axis:** Last 12 months
- **Purpose:** Identify correlation between ticket volume increases and SLA compliance drops; detect seasonal patterns
- **Data endpoint:** `/api/v1/it/analytics/charts/ticket-trend/`

### Chart 4: Integration Error Rate Trend
- **Type:** Multi-series line chart
- **Series:** One line per active integration (e.g., WhatsApp Business, Payment Gateway, SSO Provider, CBSE APIs)
- **X-axis:** Last 12 months (monthly data points)
- **Y-axis:** Error rate % (0–10%; scale adjusted to show variation)
- **Reference line:** 1% error rate threshold (amber dashed)
- **Purpose:** Identify which integrations are becoming less reliable over time; track against SLA commitments
- **Data endpoint:** `/api/v1/it/analytics/charts/integration-errors/`

### Chart 5: Security Incident Trend by Severity
- **Type:** Stacked bar chart
- **X-axis:** Last 12 months
- **Y-axis:** Incident count
- **Segments:** Severity 1/Critical (red), 2/High (orange), 3/Medium (amber), 4/Low (grey)
- **Overlay line:** Group security score trend (secondary Y-axis, 0–100)
- **Purpose:** Track whether the group is experiencing escalating security incidents; correlate with security score trend
- **Data endpoint:** `/api/v1/it/analytics/charts/security-incidents/`

### Chart 6: Storage Usage Trend (Cloudflare R2)
- **Type:** Area chart
- **Series:** Actual storage usage (filled area, blue), Projected growth (dashed line, extrapolated based on 3-month rolling average growth rate)
- **X-axis:** Last 12 months + next 3 months (projection)
- **Y-axis:** Storage in GB
- **Reference lines:** 80% capacity (amber dashed), 100% capacity (red dashed)
- **Breakdown (tooltip on hover):** Storage by category — Documents, Media/Images, Reports, Other
- **Purpose:** Capacity planning — when will current storage be exhausted at current growth rate?
- **Data endpoint:** `/api/v1/it/analytics/charts/storage-trend/`

---

## 8. Toast Messages

| Action | Toast |
|--------|-------|
| Filters applied | Info: `Dashboard updated for [date range] and [branch selection].` |
| Chart exported (PNG) | Success: `Chart exported as PNG.` |
| All charts PDF export | Info: `Generating full analytics PDF — please wait.` |
| PDF ready | Success: `Analytics report PDF downloaded.` |
| Chart data CSV export | Info: `Exporting chart data.` |
| No data for filter combination | Warning: `No data available for the selected branch and date range. Try a wider selection.` |
| Filter application failed | Error: `Failed to apply filters. Please try again.` | Error | 5s |
| Chart data load failed | Error: `Failed to load chart data. Try refreshing the page.` | Error | 5s |
| PDF export failed | Error: `Failed to generate PDF. Please try again.` | Error | 5s |
| CSV export failed | Error: `Failed to export data. Please try again.` | Error | 5s |

---

## 9. Empty States

| Condition | Message |
|-----------|---------|
| Chart has no data | Chart container: `No data available for the selected period. Adjust the date range or branch filters.` |
| Feature heatmap — features not tracked | `Feature usage tracking not enabled. Contact IT Admin to enable portal usage analytics.` |
| Integration chart — no integrations active | `No active integrations configured. Set up integrations via the Integration Manager page.` |
| Branch performance table empty | `No branch data available. Ensure branches are configured in the system.` |
| Storage chart — no R2 data | `R2 storage data not available. Ensure storage monitoring is configured.` |

---

## 10. Loader States

| Element | Loader Behaviour |
|---------|-----------------|
| KPI bar | 6 skeleton shimmer cards |
| All 6 charts | Each chart card shows spinner independently (parallel load) |
| Branch performance table | 5 skeleton rows |
| Heatmap (Chart 2) | Full skeleton grid while loading |
| Filter application | Charts briefly show shimmer while reloading |
| Chart detail drawer | Spinner then full chart renders |
| PDF export | Progress indicator with estimated time |

---

## 11. Role-Based UI Visibility

| UI Element | Role 53 (G4) | Role 58 (G4) | Role 54 (G4) |
|------------|-------------|-------------|-------------|
| All 6 KPI cards | Visible | Limited (adoption + integration only) | Visible |
| Chart 1 (MAU Trend) | Visible | Visible | Visible |
| Chart 2 (Feature Heatmap) | Visible | Hidden | Visible |
| Chart 3 (Ticket Trend) | Visible | Hidden | Visible |
| Chart 4 (Integration Errors) | Visible | Visible | Visible |
| Chart 5 (Security Incidents) | Visible | Hidden | Visible |
| Chart 6 (Storage Trend) | Visible | Hidden | Visible |
| Branch Performance Table | Visible | Hidden | Visible |
| Export All Charts PDF | Visible | Hidden | Hidden |
| Export PNG per chart | Visible | Visible (own charts) | Visible |
| Export Data CSV (in drawer) | Visible | Hidden | Hidden |
| Page-level branch filter | Visible | Visible | Visible |

---

## 12. API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/v1/it/analytics/kpis/` | Fetch 6 KPI values |
| GET | `/api/v1/it/analytics/branch-summary/` | Branch performance table |
| GET | `/api/v1/it/analytics/charts/mau-trend/` | Monthly active users |
| GET | `/api/v1/it/analytics/charts/feature-heatmap/` | Feature adoption heatmap |
| GET | `/api/v1/it/analytics/charts/ticket-trend/` | Ticket volume + SLA combo |
| GET | `/api/v1/it/analytics/charts/integration-errors/` | Integration error rates |
| GET | `/api/v1/it/analytics/charts/security-incidents/` | Security incident trend |
| GET | `/api/v1/it/analytics/charts/storage-trend/` | R2 storage trend + projection |
| GET | `/api/v1/it/analytics/charts/{chart_id}/export/csv/` | Export chart data as CSV |
| GET | `/api/v1/it/analytics/export/pdf/` | Export all charts as PDF |
| GET | `/api/v1/it/analytics/reload/` | JWT (G4) | Reload all dashboard content with applied filters |

**Common Query Parameters (all chart endpoints):**
- `date_range` (3m/6m/12m) or `date_from` + `date_to`
- `branch_ids` (comma-separated UUIDs; omit for all branches)

---

## 13. HTMX Patterns

```html
<!-- Page-level filter form — applied to all charts -->
<form id="analytics-filter-form">
  <select name="date_range">
    <option value="3m">Last 3 Months</option>
    <option value="6m">Last 6 Months</option>
    <option value="12m" selected>Last 12 Months</option>
    <option value="custom">Custom</option>
  </select>
  <select name="branch_ids" multiple>
    <!-- branch options -->
  </select>
  <button type="button"
          hx-get="/group/it/analytics/reload/"
          hx-target="#analytics-dashboard"
          hx-include="#analytics-filter-form"
          hx-indicator="#dashboard-loader">
    Apply Filters
  </button>
</form>

<!-- KPI bar — responds to filter changes -->
<div id="analytics-kpis"
     hx-get="/group/it/analytics/kpis/"
     hx-trigger="load, analyticsFiltersApplied from:body"
     hx-target="#analytics-kpis"
     hx-include="#analytics-filter-form">
</div>

<!-- Charts — each loads independently -->
<div id="chart-mau"
     hx-get="/group/it/analytics/charts/mau-trend/"
     hx-trigger="load, analyticsFiltersApplied from:body"
     hx-target="#chart-mau"
     hx-include="#analytics-filter-form">
</div>

<div id="chart-heatmap"
     hx-get="/group/it/analytics/charts/feature-heatmap/"
     hx-trigger="load, analyticsFiltersApplied from:body"
     hx-target="#chart-heatmap"
     hx-include="#analytics-filter-form">
</div>

<div id="chart-tickets"
     hx-get="/group/it/analytics/charts/ticket-trend/"
     hx-trigger="load, analyticsFiltersApplied from:body"
     hx-target="#chart-tickets"
     hx-include="#analytics-filter-form">
</div>

<div id="chart-integrations"
     hx-get="/group/it/analytics/charts/integration-errors/"
     hx-trigger="load, analyticsFiltersApplied from:body"
     hx-target="#chart-integrations"
     hx-include="#analytics-filter-form">
</div>

<div id="chart-security"
     hx-get="/group/it/analytics/charts/security-incidents/"
     hx-trigger="load, analyticsFiltersApplied from:body"
     hx-target="#chart-security"
     hx-include="#analytics-filter-form">
</div>

<div id="chart-storage"
     hx-get="/group/it/analytics/charts/storage-trend/"
     hx-trigger="load, analyticsFiltersApplied from:body"
     hx-target="#chart-storage"
     hx-include="#analytics-filter-form">
</div>

<!-- Chart detail drawer (expand) -->
<button class="expand-chart-btn"
        hx-get="/group/it/analytics/charts/{{ chart_id }}/detail/"
        hx-target="#drawer-container"
        hx-swap="innerHTML"
        hx-include="#analytics-filter-form"
        hx-on::after-request="openDrawer()">
  ⤢ Expand
</button>

<!-- Branch performance table -->
<div id="branch-summary-table"
     hx-get="/group/it/analytics/branch-summary/"
     hx-trigger="load, analyticsFiltersApplied from:body"
     hx-target="#branch-summary-table"
     hx-include="#analytics-filter-form">
</div>
```

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
