# Page 46: Support SLA Dashboard

**URL:** `/group/it/support/sla/`
**Roles:** Group IT Support Executive (Role 57, G3); Group IT Director (Role 53, G4)
**Priority:** P1
**Division:** F — Group IT & Technology

---

## 1. Purpose

SLA compliance analytics for the IT support function. This page provides a quantitative view of how well the IT support team is meeting service level agreements across all branches and ticket priorities. It is the primary performance management tool for the IT support function.

Use cases:
- **IT Director (Role 53):** Evaluate support team performance, identify chronic SLA failures, make staffing decisions, report to management
- **IT Support Executive (Role 57):** Understand their own performance metrics, identify which ticket categories take longest, prioritise personal workload
- Track patterns — which branches generate the most tickets, which categories take longest to resolve, and which executives have the highest resolution rates
- Trend analysis — whether SLA compliance is improving or degrading over time

This page complements the Ticket Manager (Page 45) which is the operational day-to-day tool. The SLA Dashboard is analytics and reporting.

All data is aggregated from the tickets table in PostgreSQL — no cached summaries.

---

## 2. Role Access

| Role | Access Level | Notes |
|------|-------------|-------|
| Group IT Director (Role 53, G4) | Full access | View all data for all executives; see individual executive performance |
| Group IT Support Executive (Role 57, G3) | Limited view | View group-level metrics and their own performance; cannot see other executives' individual data |
| Group IT Admin (Role 54, G4) | Full access | Same as IT Director |
| All other roles | No access | Returns 403 |
| Group Data Privacy Officer (Role 55, G1) | No access | Returns 403 |
| Group Cybersecurity Officer (Role 56, G1) | No access | Returns 403 |

---

## 3. Page Layout

**Breadcrumb:**
`Group Portal > IT & Technology > IT Support > SLA Dashboard`

**Page Header:**
- Title: `IT Support SLA Dashboard`
- Subtitle: `Service level compliance and support performance analytics`
- Right side: Date range filter (default: Last 30 days), `Export Report (PDF)` button (Role 53/54)

**Date Range Selector (prominent — above KPIs):**
- Quick options: Last 7 days / Last 30 days / Last 90 days / This Quarter / Custom range
- When changed, all KPIs, table, and charts re-fetch via HTMX

**Alert Banners:**

1. **Overall SLA Below Target** (amber, dismissible):
   - Condition: overall SLA compliance < 90% in selected period
   - Text: `Overall SLA compliance is [X]% for the selected period — below the 90% target. Review breach patterns below.`

2. **P1 SLA Below 95%** (red, dismissible):
   - Condition: P1 SLA compliance < 95%
   - Text: `P1 (Critical) SLA compliance is [X]% — critical tickets are not being resolved within the 4-hour SLA.`

---

## 4. KPI Summary Bar

Five KPI cards in a 5-column responsive grid.

| # | Metric | Calculation | Visual |
|---|--------|-------------|--------|
| 1 | Overall SLA Compliance % | (tickets_resolved_within_sla / total_resolved) × 100 for selected period | % — red < 80%, amber 80–89%, green ≥ 90% |
| 2 | P1 SLA Met % | P1 tickets resolved ≤ 4h / total P1 resolved × 100 | % — red if < 95% |
| 3 | P2 SLA Met % | P2 tickets resolved ≤ 8h / total P2 resolved × 100 | % — amber if < 90% |
| 4 | P3 SLA Met % | P3 tickets resolved ≤ 48h / total P3 resolved × 100 | % |
| 5 | Avg CSAT Score | Average customer satisfaction score from resolved tickets where reporter rated the resolution (1–5 scale) | X.X / 5 — red < 3.5, amber 3.5–4.0, green > 4.0 |

All KPIs re-fetch when date range changes. `hx-trigger="dateRangeChanged from:body"`.

---

## 5. Main Table — SLA Performance by Branch

**Table Title:** `SLA Performance by Branch`
**Description:** One aggregated row per branch showing support performance in the selected date range.

### Columns

| Column | Type | Notes |
|--------|------|-------|
| Branch Name | Text | Branch display name |
| Tickets (Period) | Number | Total tickets raised in selected period |
| P1 SLA % | % | Green ≥ 95%, amber 90–94%, red < 90% |
| P2 SLA % | % | Green ≥ 90%, amber 80–89%, red < 80% |
| Avg First Response (hrs) | Number | Average time to first response for all tickets from this branch |
| Avg Resolution (hrs) | Number | Average total resolution time |
| CSAT Score | Number | Average CSAT (1–5) for this branch's tickets |
| Actions | Button | `View Branch Tickets` — navigates to ticket manager filtered by this branch |

CSAT Score: shows `—` if no satisfaction ratings have been submitted for that branch's tickets.

### Filters

- **Date Range:** Inherited from page-level date range selector
- **Category:** All / Portal Login / Feature Issue / Data Issue / Integration / Performance / Account
- **Priority:** All / P1 / P2 / P3
- **Assigned To (Executive):** Dropdown — visible to Role 53/54 only

### Search

Search on branch name. `hx-trigger="keyup changed delay:400ms"`, targets `#sla-branch-table`.

### Pagination

Server-side, 20 rows per page. `hx-get="/group/it/support/sla/table/?page=N"`, targets `#sla-branch-table`.

### Sorting

Sortable: Tickets (Period), P1 SLA %, Avg First Response, CSAT Score. Default: Tickets descending (most active branches first).

---

## 6. Drawers

**Note:** This is a read-only analytics dashboard. No create, edit, or delete operations are available. The executive detail drawer provides branch drill-down viewing only.

No create/edit drawers on this analytics page. One read-only drawer:

### View Executive Performance Drawer (560px — Role 53/54 only)

Accessible from filter by Assigned To or a separate "Executive Performance" tab.

**Drawer Header:** `[Executive Name] — Support Performance`

**Period:** [Selected date range]

**Metrics:**
- Tickets handled (total)
- P1 SLA met %, P2 SLA met %, P3 SLA met %
- Avg first response time (hrs)
- Avg resolution time (hrs)
- CSAT score (average)
- Tickets by category breakdown (mini bar)
- SLA breach count + breach reason breakdown

**Performance Rating:**
- Auto-generated: Excellent / Good / Needs Improvement / At Risk
- Based on: Overall SLA ≥ 95% = Excellent, 90–94% = Good, 80–89% = Needs Improvement, < 80% = At Risk

**Footer:** `Close`

---

## 7. Charts

Five charts in a responsive 2-column grid (chart 1 full width; charts 2–5 in 2-column pairs).

### Chart 1: SLA Compliance Trend (Full Width)
- **Type:** Line chart (3 series)
- **Series:** Overall SLA % (blue), P1 SLA % (red), P2 SLA % (orange)
- **X-axis:** Last 6 months (monthly data points)
- **Y-axis:** Compliance % (0–100%)
- **Reference lines:** 90% target (blue dashed), 95% P1 target (red dashed)
- **Purpose:** Track whether SLA performance is trending up or down
- **Filter:** Responds to page-level date range (shows proportional window)
- **Data endpoint:** `/api/v1/it/support/sla/charts/trend/`

### Chart 2: Ticket Volume by Category
- **Type:** Vertical bar chart
- **X-axis:** Categories (Portal Login, Feature Issue, Data Issue, etc.)
- **Y-axis:** Ticket count
- **Purpose:** Identify which categories generate the most tickets — guides documentation and training efforts
- **Data endpoint:** `/api/v1/it/support/sla/charts/volume-by-category/`

### Chart 3: Ticket Volume by Branch
- **Type:** Horizontal bar chart
- **Y-axis:** Branch names
- **X-axis:** Ticket count
- **Colour:** Based on SLA compliance — green (≥90%), amber (80–89%), red (<80%)
- **Purpose:** Identify high-volume or high-breach branches
- **Data endpoint:** `/api/v1/it/support/sla/charts/volume-by-branch/`

### Chart 4: Average Resolution Time by Category
- **Type:** Horizontal bar chart
- **Y-axis:** Categories
- **X-axis:** Hours
- **Reference lines:** P1 SLA (4h, red dashed), P2 SLA (8h, orange dashed)
- **Purpose:** Identify which issue types take longest to resolve — drives knowledge base prioritisation
- **Data endpoint:** `/api/v1/it/support/sla/charts/resolution-by-category/`

### Chart 5: First Response Time Distribution
- **Type:** Histogram
- **X-axis:** Response time buckets (<1h, 1–2h, 2–4h, 4–8h, 8–24h, >24h)
- **Y-axis:** Ticket count
- **Colour:** Green (within P1 SLA), amber (within P2 SLA), red (beyond P2 SLA)
- **Purpose:** Understand the distribution of response times — are most tickets responded to quickly or is there a long tail?
- **Data endpoint:** `/api/v1/it/support/sla/charts/response-distribution/`

All charts respond to the page-level date range selector. Charts reload when date range changes via HTMX.

---

## 8. Toast Messages

| Action | Toast |
|--------|-------|
| Export report initiated | Info: `Generating SLA report PDF — please wait.` |
| Export complete | Success: `SLA performance report downloaded.` |
| Date range changed | Info: `Dashboard updated for [selected period].` |
| No data in range | Warning: `No ticket data found for the selected period. Try a wider date range.` |
| Export failed | Error: `Failed to generate SLA report. Please try again.` | Error | 5s |
| Data load failed | Error: `Failed to load dashboard data. Please refresh the page.` | Error | 5s |

---

## 9. Empty States

| Condition | Message |
|-----------|---------|
| No tickets in selected period | Icon + `No tickets found for the selected date range. Try expanding the period.` |
| No tickets in a specific branch row | Branch row shows `0` for tickets and `—` for all metrics |
| Chart has no data | `No data available for this chart in the selected period.` |
| CSAT score not available | Cell shows `—` with tooltip `No satisfaction ratings submitted yet` |
| Executive performance drawer — no data | `No tickets handled by this executive in the selected period.` |

---

## 10. Loader States

| Element | Loader Behaviour |
|---------|-----------------|
| KPI bar | 5 skeleton shimmer cards, reload on date change |
| SLA branch table | 5 skeleton rows |
| Charts | Spinner in each chart container; charts load independently |
| Date range change | Page-wide overlay spinner: `Updating dashboard...` lasting max 1 second before partial re-renders |
| Executive performance drawer | Spinner while data loads |
| Export button | `Generating...` text + disabled |

---

## 11. Role-Based UI Visibility

| UI Element | Role 57 (G3) | Role 54 (G4) | Role 53 (G4) |
|------------|-------------|-------------|-------------|
| All KPI cards | Visible | Visible | Visible |
| SLA branch table | Visible | Visible | Visible |
| Assigned To filter | Hidden (only sees own) | Visible | Visible |
| Executive Performance drawer | Hidden | Visible | Visible |
| Export Report PDF | Hidden | Visible | Visible |
| Chart: Volume by Branch | Visible | Visible | Visible |
| Chart: Resolution by Category | Visible | Visible | Visible |
| Date range selector | Visible | Visible | Visible |
| View Branch Tickets button | Visible (navigates to ticket manager) | Visible | Visible |

> Role 57 can see all group-level aggregated charts but cannot identify individual executive performance data. Their own metrics are shown in their profile/dashboard, not here.

**Note:** Role 55 (DPO) and Role 56 (Cybersecurity Officer) have no access to this page (returns 403).

---

## 12. API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/v1/it/support/sla/kpis/` | Fetch 5 KPI values |
| GET | `/api/v1/it/support/sla/branches/` | Fetch branch-level SLA table (paginated) |
| GET | `/api/v1/it/support/sla/executive/{id}/` | Executive performance (Role 53/54) |
| GET | `/api/v1/it/support/sla/charts/trend/` | SLA compliance trend |
| GET | `/api/v1/it/support/sla/charts/volume-by-category/` | Volume by category |
| GET | `/api/v1/it/support/sla/charts/volume-by-branch/` | Volume by branch |
| GET | `/api/v1/it/support/sla/charts/resolution-by-category/` | Avg resolution by category |
| GET | `/api/v1/it/support/sla/charts/response-distribution/` | First response histogram |
| GET | `/api/v1/it/support/sla/export/pdf/` | Generate PDF report |

**Common Query Parameters:**
- `date_from` (ISO date), `date_to` (ISO date)
- `category` (ticket category filter)
- `priority` (P1/P2/P3)
- `assigned_to` (UUID — Role 53/54 only)
- `page`, `page_size`

---

## 13. HTMX Patterns

```html
<!-- Date range selector — triggers full dashboard reload -->
<form id="date-range-form">
  <select name="preset"
          hx-get="/group/it/support/sla/reload/"
          hx-trigger="change"
          hx-target="#sla-dashboard-content"
          hx-swap="innerHTML"
          hx-indicator="#dashboard-loader">
    <option value="7d">Last 7 Days</option>
    <option value="30d" selected>Last 30 Days</option>
    <option value="90d">Last 90 Days</option>
    <option value="this_quarter">This Quarter</option>
  </select>
  <!-- Custom date inputs -->
  <input type="date" name="date_from" />
  <input type="date" name="date_to"
         hx-get="/group/it/support/sla/reload/"
         hx-trigger="change"
         hx-target="#sla-dashboard-content"
         hx-include="#date-range-form" />
</form>

<!-- KPI bar (inside dashboard content) -->
<div id="sla-kpis"
     hx-get="/group/it/support/sla/kpis/"
     hx-trigger="load"
     hx-target="#sla-kpis"
     hx-include="#date-range-form">
</div>

<!-- SLA branch table -->
<div id="sla-branch-table"
     hx-get="/group/it/support/sla/branches/"
     hx-trigger="load"
     hx-target="#sla-branch-table"
     hx-include="#date-range-form, #sla-filter-form">
</div>

<!-- Search -->
<input type="text" name="search"
       hx-get="/group/it/support/sla/branches/"
       hx-trigger="keyup changed delay:400ms"
       hx-target="#sla-branch-table"
       hx-include="#date-range-form, #sla-filter-form" />

<!-- Charts — independent loads responding to date range -->
<div id="chart-trend"
     hx-get="/group/it/support/sla/charts/trend/"
     hx-trigger="load, dateRangeChanged from:body"
     hx-target="#chart-trend"
     hx-include="#date-range-form">
</div>

<!-- Executive performance drawer (Role 53/54) -->
<button hx-get="/group/it/support/sla/executive/{{ exec.id }}/"
        hx-target="#drawer-container"
        hx-swap="innerHTML"
        hx-include="#date-range-form"
        hx-on::after-request="openDrawer()">
  View Performance
</button>
```

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
