# 15 — Fee Collection Analytics

> **URL:** `/group/analytics/fees/`
> **File:** `15-fee-collection-analytics.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Analytics Director (Role 102, G1) · MIS Officer (Role 103, G1) · Strategic Planning Officer (Role 107, G1) · Hostel Analytics Officer (Role 106, G1) — hosteler fees only

---

## 1. Purpose

Group-wide fee collection analytics across all fee types: Tuition (Day Scholar), Tuition (Hosteler), Hostel Rent (AC and Non-AC), Mess Charges, Transport Fee, Integrated Coaching Fee, Exam Fee, and Miscellaneous. Tracks collection rates by branch, fee type, student category, and month. Identifies chronic under-collection branches, high-value defaulters, seasonal dips in collection, and the impact of scholarship waivers on net revenue. This page does not manage fee records (that is Division D's domain) — it reads and analyses them. Data feeds directly into monthly MIS reports for the Chairman and CFO.

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Analytics Director | 102 | G1 | Full — all fee types, export | Primary user |
| Group MIS Officer | 103 | G1 | Full — all fee types, export | For board/MIS reports |
| Group Strategic Planning Officer | 107 | G1 | Full — for financial feasibility analysis | — |
| Group Hostel Analytics Officer | 106 | G1 | View — hosteler fees only (Hostel Rent, Mess) | Filtered to hostel fee types |
| Group Academic Data Analyst | 104 | G1 | No access | Financial data not in scope |
| All other roles | — | — | No access | Redirected |

> **Access enforcement:** `@require_role(['analytics_director', 'mis_officer', 'strategic_planning_officer', 'hostel_analytics_officer'])`. Role 106 receives queryset filtered to `fee_type__in = ['hostel_rent_ac', 'hostel_rent_nonac', 'mess']`.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Analytics & MIS  ›  Fee Collection Analytics
```

### 3.2 Page Header
```
Fee Collection Analytics                        [Export ↓]
[Group Name]  ·  AY [academic year]  ·  Data as of: [date time]
Total Demanded: ₹[N] Cr  ·  Total Collected: ₹[N] Cr  ·  Collection Rate: [N]%  ·  Outstanding: ₹[N] Cr
```

`[Export ↓]` — dropdown: Export to PDF / Export to XLSX. All roles with access.

### 3.3 Alert Banners (conditional)

| Condition | Banner Text | Severity |
|---|---|---|
| Branches with collection rate < 80% | "[N] branch(es) have fee collection below 80%: [list]." | Red |
| Any branch with outstanding > ₹10 lakh | "[N] branch(es) have outstanding fees exceeding ₹10 lakh: [list]." | Red |
| Fee data stale (> 7 days) | "Fee collection data has not been refreshed in 7 days. Some figures may be outdated." | Amber |
| Month-over-month collection rate drop > 5% | "Group fee collection rate dropped by [N]% compared to last month." | Amber |
| Scholarship waiver exceeding budget | "Total scholarship waivers (₹[N]) exceed the configured annual budget (₹[N])." | Amber |

---

## 4. KPI Summary Bar

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Total Fee Demanded (AY) | Sum of all fee demands for current AY | `FeeRecord.objects.filter(ay=current_ay).aggregate(Sum('amount_demanded'))` | Indigo (neutral) | `#kpi-total-demanded` |
| 2 | Total Collected (AY) | Sum of all fees collected for current AY | `Sum('amount_collected')` | Indigo (neutral) | `#kpi-total-collected` |
| 3 | Overall Collection Rate (%) | (Collected / Demanded) × 100 | — | Green ≥ 92% · Amber 85–91% · Red < 85% | `#kpi-collection-rate` |
| 4 | Total Outstanding (₹) | Demanded − Collected | — | Red > ₹50L · Amber ₹10L–₹50L · Green < ₹10L | `#kpi-outstanding` |
| 5 | Branches < 85% Rate | Count of branches with collection rate < 85% | — | Red > 3 · Amber 1–3 · Green = 0 | `#kpi-branches-below` |
| 6 | Total Defaulters | Count of students with any outstanding fee | — | Red > 500 · Amber 100–500 · Green < 100 | `#kpi-defaulters` |
| 7 | Scholarship Waiver Total (₹) | Total fee waived via scholarships this AY | — | Indigo (neutral; informational) | `#kpi-waiver` |

**HTMX:** `<div id="fee-kpi-bar" hx-get="/api/v1/group/{id}/analytics/fees/kpi/" hx-trigger="load, every 300s" hx-swap="innerHTML">`.

---

## 5. Sections

### 5.1 Fee Collection Summary Table

**Search bar:** Branch name, city. Debounced 300ms.

**Filter chips:** `[Zone ▾]` `[State ▾]` `[Fee Type ▾]` `[Collection Range ▾]` `[Branch Type ▾]`

| Column | Source Field | Sortable | Notes |
|---|---|---|---|
| Branch | `branch_name` | ▲▼ | Clickable → `fee-branch-detail` drawer |
| Zone | `zone_name` | ▲▼ | — |
| Total Demanded (₹) | `total_demanded` | ▲▼ | Formatted: ₹X,XX,XXX |
| Total Collected (₹) | `total_collected` | ▲▼ | — |
| Outstanding (₹) | `outstanding` | ▲▼ | Red badge if > ₹5L |
| Collection Rate (%) | `collection_rate_pct` | ▲▼ | Colour: ≥ 92% green · 85–91% amber · < 85% red |
| Tuition Rate (%) | `tuition_rate_pct` | ▲▼ | Day Scholar + Hosteler tuition |
| Hostel Fee Rate (%) | `hostel_fee_rate_pct` | ▲▼ | "—" for day-only branches |
| Transport Rate (%) | `transport_rate_pct` | ▲▼ | "—" if no transport |
| Defaulters | `defaulter_count` | ▲▼ | Count of students with any outstanding |
| Scholarship Waiver (₹) | `scholarship_waiver` | ▲▼ | — |
| Last Updated | `data_last_updated` | ▲▼ | Amber if > 7 days |
| Actions | — | — | `[View]` |

**Default sort:** Collection Rate ascending (worst first).
**Pagination:** 25 rows per page.

### 5.2 Top 10 Defaulter Branches

Compact table. Top 10 branches by outstanding amount (₹), sorted descending.

| Column | Notes |
|---|---|
| # | Rank |
| Branch | Clickable → detail drawer |
| Outstanding (₹) | Bold red |
| Defaulter Count | — |
| Collection Rate (%) | — |
| Last Updated | — |

### 5.3 Fee Category Breakdown

Summary cards for each fee type showing group-wide collection rate:

| Fee Type | Total Demanded | Collected | Rate | Trend |
|---|---|---|---|---|
| Tuition (Day Scholar) | ₹X Cr | ₹X Cr | N% | ↑/↓ |
| Tuition (Hosteler) | — | — | — | — |
| Hostel Rent (AC) | — | — | — | — |
| Hostel Rent (Non-AC) | — | — | — | — |
| Mess Charges | — | — | — | — |
| Transport Fee | — | — | — | — |
| Integrated Coaching | — | — | — | — |

Displayed as a table with horizontal mini-bar per row showing collection rate visually.

### 5.4 Scholarship Waiver Impact

Shows: Total waivers granted, net collection (demanded − waiver − outstanding), effective collection rate (if waivers counted as collected), and waiver distribution by branch.

---

## 6. Drawers & Modals

### 6.1 `fee-branch-detail` Drawer — 680px, right-slide

**Trigger:** Clicking branch name in §5.1 or `[View]` action.

**Header:**
```
[Branch Name] — Fee Collection Analytics                    [×]
[Zone]  ·  [City], [State]
Collection Rate: [N]%  ·  Outstanding: ₹[N]  ·  Defaulters: [N]
```

**Tab 1 — Collection Summary**

Cards: Total Demanded, Total Collected, Outstanding, Collection Rate (gauge), Defaulters, Scholarship Waiver.
Month-by-month bar chart (last 6 months): Demanded vs Collected.

**Tab 2 — By Fee Type**

Table: Fee Type | Demanded | Collected | Outstanding | Rate % | Defaulters.
Each row colour coded by rate.

**Tab 3 — Top Defaulters**

Table of top 20 students with highest outstanding fees at this branch (read-only):
Student Name | Class | Fee Type | Outstanding (₹) | Last Payment Date.

Note: "Student fee data is read-only. Contact Branch Accounts Officer to update records."

**Tab 4 — Monthly Trend**

Line chart — monthly collection rate for this branch, last 12 months.
Table: Month | Demanded | Collected | Rate % | vs Group Avg.

**Tab 5 — Scholarship Detail**

Table: Scholarship Type | Students | Total Waiver (₹) | vs Demand.
Running total of waivers vs scholarship budget (if configured).

### 6.2 Export Modal — 480px, centred

| Field | Type | Required | Notes |
|---|---|---|---|
| Report Type | Select | Yes | Full Collection Summary / Defaulter Report / Fee Category Breakdown / Scholarship Impact Report |
| Academic Year | Select | Yes | Current + prev 2 |
| Branches | Multi-select | No | Default: all |
| Fee Type | Multi-select | No | Default: all |
| Format | Radio | Yes | PDF · XLSX |

**Footer:** `[Cancel]`  `[Generate Export]`

---

## 7. Charts

### 7.1 Collection Rate by Branch — Horizontal Bar

| Property | Value |
|---|---|
| Chart type | Horizontal bar (Chart.js 4.x) |
| Title | "Fee Collection Rate by Branch — [AY]" |
| Data | Overall collection rate per branch for current AY |
| Y-axis | Branch names (sorted by rate ASC) |
| X-axis | Rate % (0–100%) |
| Bar colour | ≥ 92% green · 85–91% amber · < 85% red |
| Reference lines | Vertical dotted at 85% (minimum) and 92% (target) |
| Tooltip | "[Branch]: [N]% · Collected ₹[N] of ₹[N] demanded" |
| Empty state | "No fee data available." |
| Export | PNG button |
| API endpoint | `GET /api/v1/group/{id}/analytics/fees/by-branch/` |
| HTMX | `hx-trigger="load"` |

### 7.2 Fee Collection Trend — Stacked Area Chart

| Property | Value |
|---|---|
| Chart type | Stacked area (Chart.js 4.x) |
| Title | "Fee Collection by Type — Last 6 Months" |
| Data | Monthly collected amount stacked by fee type (Tuition/Hostel/Transport/Coaching) |
| X-axis | Month names (last 6 months) |
| Y-axis | Amount collected (₹ in lakhs) |
| Area colours | Colorblind-safe palette per fee type |
| Tooltip | "[Month] · Tuition: ₹[N]L · Hostel: ₹[N]L · Transport: ₹[N]L · Total: ₹[N]L" |
| Legend | Bottom |
| Empty state | "No fee trend data available." |
| Export | PNG button |
| API endpoint | `GET /api/v1/group/{id}/analytics/fees/trend/?months=6` |
| HTMX | `hx-trigger="load"` |

---

## 8. Toast Messages

| Action | Toast Text | Type |
|---|---|---|
| Export generated | "Fee collection report exported to [format]." | Success |
| Export failed | "Could not generate export. Please try again." | Error |
| Branch detail drawer load error | "Could not load fee data for this branch." | Error |
| KPI refresh error | "Failed to refresh KPI data." | Error |

---

## 9. Empty States

| Context | Icon | Heading | Sub-text | Action |
|---|---|---|---|---|
| No fee data for current AY | `currency-rupee` | "No Fee Data" | "Fee collection records are not available for this academic year." | — |
| No results after filter | `funnel` | "No Branches Match Filters" | — | `[Clear Filters]` |
| No defaulters in system | `check-circle` | "No Defaulters" | "All students are up to date on their fee payments." | — |
| Branch detail — no tab data | `currency-rupee` | "No Data Available" | "Fee data is not available for this branch." | — |
| Charts — no data | `chart-bar` | "No data available" | — | — |

---

## 10. Loader States

| Context | Loader Behaviour |
|---|---|
| Initial page load | KPI bar: 7 shimmer cards. Charts: 2 shimmer rectangles. Main table: 8 shimmer rows. Top defaulters: 5 shimmer rows. Fee category: shimmer table rows. |
| Search/filter change | Table rows shimmer |
| Branch detail drawer open | Drawer slides in; shimmer cards + shimmer chart |
| Tab switch in drawer | Shimmer content |
| Export generate | Button disabled + spinner |
| KPI auto-refresh | Cards pulse |
| Pagination | Table body shimmer |

---

## 11. Role-Based UI Visibility

| UI Element | Role 102 | Role 103 | Role 107 | Role 106 |
|---|---|---|---|---|
| Page | ✅ | ✅ | ✅ | ✅ |
| KPI Bar — all 7 cards | ✅ | ✅ | ✅ | Hostel fee cards only |
| Main table — all fee columns | ✅ | ✅ | ✅ | Hostel/Mess cols only |
| Fee category breakdown (all types) | ✅ | ✅ | ✅ | Hostel/Mess rows only |
| Scholarship section | ✅ | ✅ | ✅ | ❌ |
| Top defaulters section | ✅ | ✅ | ✅ | Hosteler defaulters only |
| Branch detail — all tabs | ✅ | ✅ | ✅ | Tabs 1, 2 (hostel types), 3 (hosteler defaulters) only |
| `[Export ↓]` button | ✅ | ✅ | ✅ | ✅ |
| Alert banners | ✅ All | ✅ All | ✅ All | Hostel-relevant only |

---

## 12. API Endpoints

### 12.1 KPI Summary
```
GET /api/v1/group/{group_id}/analytics/fees/kpi/
```
Query: `academic_year`.
Response: `{ "total_demanded": N, "total_collected": N, "collection_rate_pct": N, "outstanding": N, "branches_below_85": N, "total_defaulters": N, "scholarship_waiver_total": N }`.

### 12.2 Branch Collection Summary
```
GET /api/v1/group/{group_id}/analytics/fees/branches/
```

| Query Parameter | Type | Description |
|---|---|---|
| `academic_year` | string | Default current |
| `zone` | string | Zone ID |
| `state` | string | State name |
| `fee_type` | string | Filter by fee type slug |
| `collection_range` | string | `above_92` · `85_91` · `below_85` |
| `branch_type` | string | `day` · `hostel` · `both` |
| `search` | string | Branch name |
| `page` | integer | Default 1 |
| `page_size` | integer | 25 · 50 · All |
| `ordering` | string | `collection_rate_pct` (ASC default) · `outstanding` · `branch_name` |

### 12.3 Branch Detail
```
GET /api/v1/group/{group_id}/analytics/fees/branches/{branch_id}/
```
Query: `academic_year`.
Response: Full detail — collection summary, by-fee-type, top defaulters, monthly trend (12 months), scholarship detail.

### 12.4 Fee Category Breakdown
```
GET /api/v1/group/{group_id}/analytics/fees/by-category/
```
Query: `academic_year`.
Response: `[{ fee_type, demanded, collected, rate_pct, trend }]`.

### 12.5 Branch Chart
```
GET /api/v1/group/{group_id}/analytics/fees/by-branch/
```
Query: `academic_year`.
Response: `{ labels: [...], data: [...rates], colours: [...] }`.

### 12.6 Trend Chart
```
GET /api/v1/group/{group_id}/analytics/fees/trend/
```
Query: `months` (default 6).
Response: `{ labels: [...months], datasets: [{ fee_type, data: [...amounts] }] }`.

### 12.7 Export
```
GET /api/v1/group/{group_id}/analytics/fees/export/
```
Query: `report_type`, `academic_year`, `branches`, `fee_type`, `format`.
Response: File download.

---

## 13. HTMX Patterns

| Pattern | Trigger Element | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI bar load + auto-refresh | `<div id="fee-kpi-bar">` | GET `.../fees/kpi/` | `#fee-kpi-bar` | `innerHTML` | `hx-trigger="load, every 300s"` |
| Chart 7.1 load | `<div id="chart-by-branch">` | GET `.../fees/by-branch/` | `#chart-by-branch` | `innerHTML` | `hx-trigger="load"` |
| Chart 7.2 load | `<div id="chart-trend">` | GET `.../fees/trend/` | `#chart-trend` | `innerHTML` | `hx-trigger="load"` |
| Table search | `<input id="fee-search">` | GET `.../fees/branches/?search=` | `#fee-table` | `innerHTML` | `hx-trigger="keyup changed delay:300ms"` |
| Table filter | Filter chip selects | GET `.../fees/branches/?filters=` | `#fee-table` | `innerHTML` | `hx-trigger="change"` |
| Table pagination | Pagination buttons | GET `.../fees/branches/?page={n}` | `#fee-table` | `innerHTML` | `hx-trigger="click"` |
| Open branch detail drawer | Branch name / `[View]` | GET `/htmx/analytics/fees/branches/{id}/detail/` | `#drawer-container` | `innerHTML` | `hx-trigger="click"` |
| Drawer tab switch | Tab buttons | GET `/htmx/analytics/fees/branches/{id}/tab/{slug}/` | `#fee-drawer-tab-content` | `innerHTML` | `hx-trigger="click"` |
| Export modal generate | Export form | GET `.../fees/export/?params=` | — | — | File download |

---

*Page spec version: 1.0 · Last updated: 2026-03-22*
