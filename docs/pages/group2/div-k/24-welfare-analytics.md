# 24 — Welfare Analytics

> **URL:** `/group/welfare/events/analytics/`
> **File:** `24-welfare-analytics.md`
> **Template:** `portal_base.html`
> **Priority:** P2
> **Role:** Group Welfare Events Coordinator (Role 95, G3) — primary; Group Chairman/CEO (G5/G4) — read-only

---

## 1. Purpose

Analytics and intelligence dashboard for the welfare events system. This page provides cross-branch, cross-severity, and trend-based analysis to help the Group Welfare Events Coordinator identify systemic patterns, high-risk branches, recurring welfare gaps, and seasonal or cyclical patterns in student wellbeing incidents.

This page is the **analytical layer** of the welfare system — distinct from the operational register (page 23), which is for logging and managing individual events. The analytics page provides the intelligence needed to act strategically: understanding whether bullying is increasing, whether a particular branch consistently shows elevated welfare incidents, whether resolution times are improving year-on-year, and whether the group's SLA compliance is trending in the right direction.

**Primary use cases:**
- Monthly welfare digest for the Group Chairman (generated directly from this page as a branded PDF)
- Branch welfare load identification for resource allocation
- Early detection of under-reporting branches (branches with suspiciously low event rates relative to student population)
- Year-on-year welfare trend comparison for board reporting
- Seasonal pattern identification (e.g., examination periods, hostel admission weeks)

This page has **no create, edit, or status-change functionality**. All interactions are read and export operations. Report generation is a POST that triggers an async task.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Welfare Events Coordinator | G3 | Full read + export + generate monthly digest | Primary owner; all charts, tables, and export |
| Group Chairman / CEO | G5 | Read-only — all charts visible; no export; PDF digest delivered via notification | Cannot change filters; sees pre-set current academic year view |
| Group COO | G4 | Full read + export | Same access as Coordinator |
| All other roles | — | No access | — |

> **Access enforcement:** `@require_role('welfare_coordinator', 'chairman', 'coo')`. Chairman role receives a read-only serialiser with no filter controls rendered in the UI; filter parameters are stripped server-side even if injected via URL.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Welfare & Safety  ›  Events  ›  Welfare Analytics
```

### 3.2 Page Header
- **Title:** `Welfare Analytics`
- **Subtitle:** `Intelligence dashboard · [Selected Academic Year] · [Selected Branch(es)]`
- **Right controls:** `Generate Monthly Digest` (PDF) · `Export Data` (CSV — Coordinator + COO only) · `Academic Year` selector · `Branch` multi-select filter · `Date Range` picker

### 3.3 Alert Banner

| Condition | Banner Text | Severity |
|---|---|---|
| Under-reporting branch detected | "[N] branches are flagged for potential under-reporting based on event rate vs student population." | Amber |
| Year-on-year S3–S4 increase > 20% | "Severity 3–4 events have increased [X]% compared to the same period last year." | Red |
| Monthly digest overdue | "The monthly welfare digest for [Month] has not been generated yet. It is [N] days overdue." | Amber |

---

## 4. KPI Summary Bar

Six cards reflecting the period and branch filters currently selected. Default: current academic year, all branches.

| # | Card | Metric | Colour Rule |
|---|---|---|---|
| 1 | Total Events | Count of all welfare events in selected period | Blue always |
| 2 | Severity 3–4 Count | Count of Severity 3 + Severity 4 events | Red > 10 · Yellow 1–10 · Green = 0 |
| 3 | SLA Compliance % | (Events resolved within SLA / Total resolved) × 100 | Green ≥ 90% · Yellow 70–89% · Red < 70% |
| 4 | Most Common Event Type | Name of most frequent event type + count in brackets | Blue always |
| 5 | Branch with Highest Load | Branch name + event count for highest-event branch | Blue always |
| 6 | Avg Resolution Days | Mean days from log date to Close date (all closed events) | Green ≤ 1.5 · Yellow 1.5–3 · Red > 3 |

---

## 5. Analytics Sections

### 5.1 Severity Trend Chart

**Type:** Line chart
**Description:** Monthly count of welfare events by severity (4 lines: Severity 1, 2, 3, 4) for the past 24 months, or for the selected date range if shorter.

| Element | Detail |
|---|---|
| X-axis | Month labels (MMM YYYY) |
| Y-axis | Event count |
| Lines | S1 (grey) · S2 (amber) · S3 (orange) · S4 (red) |
| Tooltip | On hover: month, each severity count |
| Annotations | Vertical dashed lines at start of each academic year; exam period bands (shaded) |
| Legend | Clickable — toggle individual severity lines on/off |

**Underlying data table** (collapsible below chart):

| Column | Notes |
|---|---|
| Month | MMM YYYY |
| Severity 1 Count | |
| Severity 2 Count | |
| Severity 3 Count | |
| Severity 4 Count | |
| Total | |
| SLA Compliance % | For that month |

Pagination on the data table: 24 rows per page (one row per month).

---

### 5.2 Branch Welfare Load Heatmap

**Type:** Matrix table (branches as rows × months as columns), with colour-coded cells.

| Colour | Meaning |
|---|---|
| White / very light | 0–2 events |
| Light amber | 3–5 events |
| Medium amber | 6–10 events |
| Orange | 11–20 events |
| Red | > 20 events |

- Rows: all branches (alphabetical or sortable by total)
- Columns: last 12 months (MMM YYYY)
- Cell value: event count for that branch × month
- Cell tooltip: branch name, month, count, severity breakdown
- Row footer: branch total (sum of all months in view)
- Column footer: group total per month

**Sort controls:** Sort rows by total (descending / ascending) · alphabetical · branch region.

**Export:** This table can be exported independently as CSV via a small export icon at the section header.

---

### 5.3 Event Type Distribution

**Type:** Donut chart + data table side by side.

- Donut: top 8 event types by count for the selected period; remaining types collapsed into "Other"
- Each segment is labelled with event type + count + percentage
- Clicking a segment filters section 5.4 and 5.5 to that event type

**Underlying data table:**

| Column | Notes |
|---|---|
| Event Type | |
| Count | |
| % of Total | |
| Avg Resolution Days | For this event type |
| S3–S4 Count | High-severity count for this event type |
| YoY Change | vs same period prior year (+ / − with colour) |

Sorted by Count descending. All event types shown (not just top 8).

---

### 5.4 Resolution Time Benchmarks

**Type:** Grouped bar chart (or box plot if sufficient data) showing resolution time distribution.

**X-axis:** Severity (1, 2, 3, 4)
**Y-axis:** Days to resolution
**Bar groups:** Mean / Median / 90th Percentile — three bars per severity

**SLA reference lines:**
- Severity 1: horizontal dashed line at 1 day
- Severity 2: line at 2 days
- Severity 3: line at 7 days
- Severity 4: line at 1 day (immediate)

**Underlying data table:**

| Column | Notes |
|---|---|
| Branch | |
| Severity | |
| Avg Days to Resolve | |
| Median Days | |
| 90th Percentile Days | |
| SLA Met % | Percentage of events at this severity meeting SLA |
| Events Count | |

Sorted by Avg Days descending (slowest branch first) within each severity group. Paginated 25 rows.

---

### 5.5 Under-Reporting Analysis

**Type:** Data table

Identifies branches where the welfare event rate (events per 100 students per year) is significantly below the group average — a signal that events may be occurring but not being logged.

| Column | Notes |
|---|---|
| Branch | |
| Student Population | Total enrolled students |
| Events Logged (period) | |
| Event Rate (per 100 students) | |
| Group Avg Rate | For context |
| Deviation from Avg | % below group average; red if > 50% below |
| Last Event Logged | Date of most recently logged event |
| Days Since Last Event | Red if > 30 |
| Flag | Under-Reporting Risk (amber) · Significant Under-Reporting (red) · Normal (green) |

**Tooltip:** On hover over Flag column: *"Expected events for this branch size: [N]. Actual logged: [M]. This branch may require a site welfare audit."*

**Export:** Section-level CSV export icon.

---

### 5.6 Year-on-Year Comparison

**Type:** Grouped bar chart

- X-axis: Severity categories (S1, S2, S3, S4)
- Y-axis: Event count
- Bar groups: Current academic year (dark blue) · Previous year (medium blue) · Year before that (light blue) — up to 3 years
- Tooltip: Year, severity, count, % change vs prior year

**Underlying data table:**

| Column | Notes |
|---|---|
| Academic Year | |
| Severity 1 | |
| Severity 2 | |
| Severity 3 | |
| Severity 4 | |
| Total | |
| SLA Compliance % | |
| Avg Resolution Days | |

3 rows (one per year shown). No pagination needed.

---

## 6. Drawers / Modals

### 6.1 Modal — `generate-monthly-digest` (560px, centred)

Triggered by **Generate Monthly Digest** button.

| Field | Type | Validation |
|---|---|---|
| Report Month | Month picker (MMM YYYY) | Required; not future |
| Branches to Include | Multi-select (default: all) | Required |
| Sections to Include | Checklist: Severity Trend · Branch Heatmap · Event Type Distribution · Resolution Benchmarks · Under-Reporting Analysis · YoY Comparison | Required; at least one |
| Executive Summary | Textarea — Coordinator's narrative commentary (max 2,000 chars) | Optional but recommended |
| Report Title | Text input (default: "Group Welfare Monthly Digest — [Month Year]") | Required; max 100 chars |
| Prepared By | Read-only (logged-in user) | Auto |
| Date | Read-only (today) | Auto |

**Footer:** `Cancel` · `Generate PDF Digest`

**Behaviour:** On submit, POST to async report generation endpoint. Modal body shows progress indicator with section-by-section compilation status. On completion, shows download link + share options (notify Chairman via internal message). Generated PDF is branded with group logo, date, and "Prepared by [name]" footer.

**No edits are possible from this modal** — data is pulled live from the analytics API.

---

## 7. Toast Messages

| Action | Toast Text | Type |
|---|---|---|
| Digest generation started | "Monthly welfare digest is being compiled. You will be notified when ready." | Info |
| Digest ready | "Welfare Digest for [Month Year] is ready. Click to download." | Success |
| CSV export triggered | "Data export is being prepared." | Info |
| CSV export ready | "Export file is ready for download." | Success |
| Filter applied (no data) | "No data found for the selected period and filters." | Warning |
| Digest generation failed | "Report generation failed. Please try again or contact support." | Error |

---

## 8. Empty States

| Context | Heading | Sub-text | Action |
|---|---|---|---|
| No events for selected period | "No welfare event data for the selected period." | "Adjust the date range or branch filters to find data." | `Clear Filters` button |
| Severity Trend — no data | "No event data available for the selected 24-month window." | "Events will appear once they are logged in the Welfare Event Register." | — |
| Branch Heatmap — single branch | "Heatmap requires at least 2 branches." | "Select additional branches in the filter to view the heatmap." | — |
| Under-Reporting table — no flags | "No under-reporting flags detected." | "All branches have event rates within expected range for their student population." | — |
| YoY — only one year of data | "Year-on-year comparison requires at least 2 years of data." | "This comparison will populate as the second academic year's data is available." | — |

---

## 9. Loader States

| Context | Loader Behaviour |
|---|---|
| Initial page load | Full-page skeleton: 6 KPI cards + 6 chart/table placeholders (grey gradient rectangles) |
| Filter change | All 6 sections show individual spinner overlays simultaneously; resolve independently as each API call returns |
| Severity Trend chart load | Chart area shows animated pulse skeleton (line-chart shape outline) |
| Branch Heatmap load | Matrix skeleton with alternating grey/white cells |
| Event Type donut load | Donut placeholder (grey ring) + table skeleton (5 rows) |
| Resolution Benchmarks load | Bar chart skeleton (4 groups × 3 grey bars) |
| Under-Reporting table load | Table skeleton (10 rows × 8 columns) |
| YoY chart load | Grouped bar skeleton (4 groups × 3 grey bars) |
| Monthly digest generation | Modal body: step-by-step progress list — each section marked with spinner → green check as it compiles |

---

## 10. Role-Based UI Visibility

| UI Element | Welfare Coordinator | COO | Chairman |
|---|---|---|---|
| All 6 analytics sections | ✅ | ✅ | ✅ (read-only; no filter controls) |
| Filter controls (year / branch / date) | ✅ | ✅ | ❌ (pre-set to current year, all branches) |
| Generate Monthly Digest button | ✅ | ✅ | ❌ (receives PDF via notification) |
| Export Data (CSV) button | ✅ | ✅ | ❌ |
| Section-level CSV exports | ✅ | ✅ | ❌ |
| Under-Reporting flags | ✅ | ✅ | ✅ (read-only) |
| KPI bar — full detail | ✅ | ✅ | ✅ (read-only) |
| Alert banners | ✅ | ✅ | S3–S4 increase banner only |

---

## 11. API Endpoints

All endpoints are GET (read-only) except the report generation POST. No create, edit, or delete operations on this page.

### Base URL: `/api/v1/group/{group_id}/welfare/analytics/`

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/welfare/analytics/kpi/` | KPI summary bar for selected period | JWT + role check |
| GET | `/api/v1/group/{group_id}/welfare/analytics/severity-trend/` | Monthly severity counts for trend chart | JWT + role check |
| GET | `/api/v1/group/{group_id}/welfare/analytics/heatmap/` | Branch × month event count matrix | JWT + role check |
| GET | `/api/v1/group/{group_id}/welfare/analytics/event-type-distribution/` | Event type counts + donut data | JWT + role check |
| GET | `/api/v1/group/{group_id}/welfare/analytics/resolution-benchmarks/` | Resolution time stats by branch and severity | JWT + role check |
| GET | `/api/v1/group/{group_id}/welfare/analytics/under-reporting/` | Under-reporting analysis table | JWT + role check |
| GET | `/api/v1/group/{group_id}/welfare/analytics/yoy-comparison/` | Year-on-year event counts by severity | JWT + role check |
| GET | `/api/v1/group/{group_id}/welfare/analytics/alerts/` | Active alert conditions | JWT + role check |
| POST | `/api/v1/group/{group_id}/welfare/analytics/digest/generate/` | Async monthly digest PDF generation | Welfare Coordinator / COO |
| GET | `/api/v1/group/{group_id}/welfare/analytics/digest/{task_id}/status/` | Poll digest generation progress | Welfare Coordinator / COO |
| GET | `/api/v1/group/{group_id}/welfare/analytics/digest/{task_id}/download/` | Download completed digest PDF | Welfare Coordinator / COO |
| GET | `/api/v1/group/{group_id}/welfare/analytics/export/` | Export full analytics dataset as CSV | Welfare Coordinator / COO |

**Query parameters (shared across analytics endpoints):**

| Parameter | Type | Description |
|---|---|---|
| `academic_year` | str | e.g., `2025-26` |
| `branch` | int[] | Filter by branch ID(s) |
| `severity` | int[] | 1, 2, 3, 4 |
| `event_type` | str[] | Event type slugs |
| `date_from` | date | Override for specific date range |
| `date_to` | date | Override for specific date range |
| `months` | int | Number of months for trend chart (default 24) |
| `compare_years` | int | Number of years for YoY (default 3; max 5) |

**Chairman role enforcement:** Server-side middleware strips `branch`, `date_from`, `date_to`, `academic_year` parameters for Chairman role — fixed to current academic year, all branches.

---

## 12. HTMX Patterns

| Interaction | HTMX Attributes | Behaviour |
|---|---|---|
| Academic year filter change | `hx-get="/api/.../analytics/kpi/"` `hx-trigger="change"` `hx-target="#kpi-bar"` `hx-include="#global-filter-form"` | KPI bar refreshed; custom event `analyticsFilterChanged` dispatched to trigger all sections |
| Branch multi-select change | Same trigger pattern as above via `analyticsFilterChanged` event | All 6 sections refreshed in parallel |
| Severity trend chart load | `hx-get="/api/.../analytics/severity-trend/"` `hx-trigger="load, analyticsFilterChanged from:body"` `hx-target="#severity-trend-section"` `hx-include="#global-filter-form"` | Chart + data table partial replaced |
| Branch heatmap load | `hx-get="/api/.../analytics/heatmap/"` `hx-trigger="load, analyticsFilterChanged from:body"` `hx-target="#heatmap-section"` `hx-include="#global-filter-form"` | Heatmap matrix partial replaced |
| Event type donut load | `hx-get="/api/.../analytics/event-type-distribution/"` `hx-trigger="load, analyticsFilterChanged from:body"` `hx-target="#event-type-section"` `hx-include="#global-filter-form"` | Donut + table partial replaced |
| Resolution benchmarks load | `hx-get="/api/.../analytics/resolution-benchmarks/"` `hx-trigger="load, analyticsFilterChanged from:body"` `hx-target="#resolution-section"` `hx-include="#global-filter-form"` | Chart + table partial replaced |
| Under-reporting table load | `hx-get="/api/.../analytics/under-reporting/"` `hx-trigger="load, analyticsFilterChanged from:body"` `hx-target="#under-reporting-section"` `hx-include="#global-filter-form"` | Table partial replaced |
| YoY comparison load | `hx-get="/api/.../analytics/yoy-comparison/"` `hx-trigger="load, analyticsFilterChanged from:body"` `hx-target="#yoy-section"` `hx-include="#global-filter-form"` | Chart + table partial replaced |
| Digest generation submit | `hx-post="/api/.../analytics/digest/generate/"` `hx-target="#digest-modal-body"` `hx-swap="innerHTML"` | Modal body replaced with progress tracker |
| Digest status polling | `hx-get="/api/.../analytics/digest/{task_id}/status/"` `hx-trigger="every 3s"` `hx-target="#digest-progress-list"` | Step list updated every 3 s; stops when `status=complete` |
| Alert banner load | `hx-get="/api/.../analytics/alerts/"` `hx-trigger="load"` `hx-target="#alert-banner"` | Conditional banner display |
| Section-level CSV export | `hx-get="/api/.../analytics/export/?section={slug}"` `hx-trigger="click"` `hx-target="#export-status-{slug}"` | Export initiated; toast fires |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
