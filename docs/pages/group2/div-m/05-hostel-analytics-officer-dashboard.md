# 05 — Hostel Analytics Officer Dashboard

> **URL:** `/group/analytics/hostel/`
> **File:** `05-hostel-analytics-officer-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Role:** Group Hostel Analytics Officer (Role 106, G1) — exclusive post-login landing

---

## 1. Purpose

Primary post-login workspace for the Group Hostel Analytics Officer. Provides a unified analytics view across all hostel branches — covering occupancy rates, fee collection for hostelers, welfare incident trends, and student welfare monitoring. Hostelers (Boys/Girls × AC/Non-AC × Scholarship) have distinct tracking needs from day scholars: they live on campus, require night roll call, and have welfare events that must be tracked by severity (1–4). This dashboard surfaces the metrics that matter most for hostel management quality across the group.

Scale: Large groups — 200–1,000+ total hostel beds across 10–30 hostel branches. Small groups with hostel: 50–150 beds in 1–3 branches.

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Hostel Analytics Officer | 106 | G1 | Full — all sections, all analytics actions, export | Exclusive dashboard |
| Group Analytics Director | 102 | G1 | — | Has own dashboard `/group/analytics/director/` |
| Group MIS Officer | 103 | G1 | — | Has own dashboard `/group/mis/officer/` |
| Group Academic Data Analyst | 104 | G1 | — | Has own dashboard `/group/analytics/academic/` |
| Group Exam Analytics Officer | 105 | G1 | — | Has own dashboard `/group/analytics/exam/` |
| Group Strategic Planning Officer | 107 | G1 | — | Has own dashboard `/group/analytics/strategy/` |
| All other roles | — | — | — | Redirected to own dashboard |

> **Access enforcement:** `@require_role('hostel_analytics_officer')` on all views and API endpoints. G1 level — read-only on hostel/welfare/fee data from Divisions D and H; full CRUD on own analytics outputs (reports, export jobs, internal notes).

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Analytics & MIS  ›  Hostel Analytics Officer Dashboard
```

### 3.2 Page Header
```
Welcome back, [Officer Name]                    [Export Hostel Report ↓]
[Group Name] — Hostel Analytics Officer · Last login: [date time]
AY [current academic year]  ·  [N] Hostel Branches  ·  [N] Total Beds  ·  [N]% Group Occupancy
```

`[Export Hostel Report ↓]` — dropdown: Export to PDF / Export to XLSX. Role 106 only.

### 3.3 Alert Banners (conditional)

Stacked above KPI bar. Each individually dismissible for the session.

| Condition | Banner Text | Severity |
|---|---|---|
| Any Severity 4 welfare incident open > 3 days | "[N] critical welfare incident(s) (Severity 4) have been open for more than 3 days: [Branch list]." | Red |
| Hostel branch with occupancy < 60% | "[N] hostel branch(es) have occupancy below 60% — significant revenue leakage: [Branch list]." | Red |
| Hosteler fee collection < 80% at any branch | "[N] branch(es) have hosteler fee collection below 80%: [Branch list]." | Amber |
| Branches with open Severity 3 incidents > 7 days | "[N] Severity 3 welfare incident(s) have been open more than 7 days without resolution." | Amber |
| Hostel data not updated > 7 days at any branch | "[N] hostel branch(es) have not updated their data in more than 7 days." | Amber |
| No hostel branches configured | "No hostel branches are configured for this group. This dashboard is not applicable." | Blue |

---

## 4. KPI Summary Bar

Seven metric cards displayed horizontally. Auto-refresh every 5 minutes via HTMX polling.

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Total Hostel Capacity | Sum of all configured hostel beds across all hostel branches | `HostelBranch.objects.filter(active=True).aggregate(Sum('total_beds'))` | Indigo (neutral) | `#kpi-total-capacity` |
| 2 | Current Occupancy | Total filled beds across all hostel branches | `HostelOccupancy.objects.filter(ay=current_ay, month=current_month).aggregate(Sum('filled_beds'))` | Indigo (neutral) | `#kpi-total-occupancy` |
| 3 | Occupancy Rate (%) | (filled / total capacity) × 100 | Computed from above two values | Green ≥ 85% · Amber 70–84% · Orange 60–69% · Red < 60% | `#kpi-occupancy-rate` |
| 4 | Welfare Incidents This Month | Count of all welfare incidents (all severities) in current calendar month | `WelfareIncident.objects.filter(branch__hostel=True, date__month=current_month).count()` | Red > 20 · Amber 10–20 · Green < 10 | `#kpi-welfare-incidents` |
| 5 | Severity 3+4 Open Cases | Open welfare incidents with severity ≥ 3 | `WelfareIncident.objects.filter(severity__gte=3, status='open').count()` | Red if > 0 · Green = 0 | `#kpi-severe-open` |
| 6 | Hosteler Fee Collection Rate (%) | (collected / demanded) × 100 for hosteler fees group-wide | `FeeCollection.objects.filter(fee_type__in=['hostel','mess'], ay=current_ay).aggregate(...)` | Green ≥ 90% · Amber 80–89% · Red < 80% | `#kpi-fee-rate` |
| 7 | Hostel Branches Reporting | Branches with data updated in last 7 days / total hostel branches | `HostelData.objects.filter(last_updated__gte=today-7d).values('branch').distinct().count()` | Green = 100% · Amber < 100% | `#kpi-reporting` |

**HTMX:** `<div id="hostel-kpi-bar" hx-get="/api/v1/group/{id}/analytics/hostel/kpi/" hx-trigger="load, every 300s" hx-swap="innerHTML" hx-indicator="#kpi-spinner">`. Cards shimmer on first load.

---

## 5. Sections

### 5.1 Hostel Occupancy by Branch

> Master occupancy table across all hostel branches.

**Search bar:** Branch name. Debounced 300ms.

**Filter chips:** `[Zone ▾]` `[Occupancy Range ▾]` `[Hostel Type ▾]` `[State ▾]`

| Column | Source Field | Sortable | Notes |
|---|---|---|---|
| Branch | `branch_name` | ▲▼ | Clickable — opens `hostel-branch-detail` drawer |
| Zone | `zone_name` | ▲▼ | "—" if no zone |
| Total Beds | `total_beds` | ▲▼ | Aggregate: Boys AC + Boys Non-AC + Girls AC + Girls Non-AC + Scholarship |
| Filled | `filled_beds` | ▲▼ | Current occupancy count |
| Occupancy Rate | `occupancy_rate_pct` | ▲▼ | Colour badge: ≥ 85% green · 70–84% amber · < 70% red |
| Boys AC | `boys_ac_filled / boys_ac_total` | ▲▼ | "filled/total" format |
| Boys Non-AC | `boys_nonac_filled / boys_nonac_total` | ▲▼ | — |
| Girls AC | `girls_ac_filled / girls_ac_total` | ▲▼ | — |
| Girls Non-AC | `girls_nonac_filled / girls_nonac_total` | ▲▼ | — |
| Scholarship | `scholarship_filled / scholarship_total` | ▲▼ | — |
| Waitlist | `waitlist_count` | ▲▼ | Amber badge if > 0 |
| Fee Collection Rate | `hosteler_fee_rate_pct` | ▲▼ | Colour: ≥ 90% green · 80–89% amber · < 80% red |
| Last Updated | `data_last_updated` | ▲▼ | Amber if > 7 days ago; Red if > 14 days ago |
| Actions | — | — | `[View]` |

**Default sort:** Occupancy Rate ascending (lowest first — problems visible immediately).
**Pagination:** 25 rows · Controls: `« Previous  Page N of N  Next »` · Rows per page: 25 / 50 / All.

### 5.2 Welfare Incidents — Recent Activity

> Latest welfare events across all hostel branches. Severity 3 and 4 incidents shown with red row highlight.

**Search bar:** Branch name, incident description. Debounced 300ms.

**Filter chips:** `[Severity ▾]` `[Branch ▾]` `[Status ▾]` `[Date Range ▾]`

| Column | Source Field | Sortable | Notes |
|---|---|---|---|
| Branch | `branch_name` | ▲▼ | — |
| Incident Date | `incident_date` | ▲▼ | `DD MMM YYYY` |
| Severity | `severity` | ▲▼ | Colour badge: Sev 1 grey · Sev 2 amber · Sev 3 orange · Sev 4 red |
| Category | `incident_category` | ▲▼ | Health / Food / Discipline / Security / Mental Health / Other |
| Hostel Type | `hostel_type` | ▲▼ | Boys Hostel / Girls Hostel |
| Status | `status` | ▲▼ | Open / Resolved — colour coded |
| Days Open | `days_open` | ▲▼ | Red if Sev3 > 7 days, Sev4 > 3 days |
| Actions | — | — | `[View Details]` |

**Default sort:** Severity DESC, then incident_date DESC.
**Pagination:** 25 rows per page.

### 5.3 Hostel Fee Collection Summary

> Condensed fee table. Full analysis in Page 15 (Fee Collection Analytics).

**Shown:** Top 10 branches by outstanding fee amount (hosteler fees only), sorted by outstanding DESC.

| Column | Notes |
|---|---|
| Branch | Clickable → `hostel-branch-detail` drawer → Fee tab |
| Fee Demanded (₹) | Hostel + Mess + AC surcharge |
| Fee Collected (₹) | — |
| Outstanding (₹) | Colour: ≥ ₹1L red · ₹50k–₹1L amber · < ₹50k green |
| Collection Rate | % — colour coded same as KPI bar |
| Defaulter Count | Students with any outstanding amount |

`[View Full Fee Analytics →]` link to Page 15.

### 5.4 Quick Navigation

| Tile | Link |
|---|---|
| Hostel Occupancy Analytics | Page 19 |
| Hostel Welfare Trend Analytics | Page 20 |
| Fee Collection Analytics | Page 15 |
| MIS Report Builder | Page 07 |
| Cross-Branch Performance Hub | Page 10 |
| Analytics Export Centre | Page 24 |

---

## 6. Drawers & Modals

### 6.1 `hostel-branch-detail` Drawer — 680px, right-slide

**Trigger:** Clicking branch name in §5.1 or `[View]` action.

**Header:**
```
[Branch Name] — Hostel Analytics                                    [×]
[Zone]  ·  [City], [State]
Total Capacity: [N] beds  ·  Current Occupancy: [N]% · Data as of: [date]
```

**Tab 1 — Occupancy**

Read-only cards per hostel type: Boys AC, Boys Non-AC, Girls AC, Girls Non-AC, Scholarship.
Per card: capacity / filled / occupancy % / waitlist count.
Overall occupancy gauge chart (donut showing filled vs vacant).

**Tab 2 — Monthly Trend**

Line chart — occupancy % per month (last 12 months), split by Boys Total vs Girls Total.
Table below chart: Month | Total Beds | Filled | Rate (%) | vs Last Month.

**Tab 3 — Fee Collection**

Cards: Total Demanded, Total Collected, Outstanding, Collection Rate, Defaulter Count.
Breakdown table: Fee Type (Hostel AC/Non-AC/Mess/Extras) | Demanded | Collected | Rate.
Month-by-month collection bar chart (last 6 months).

**Tab 4 — Welfare**

Summary: Total incidents this AY | Sev 1 | Sev 2 | Sev 3 | Sev 4 | Open cases.
Recent incidents table (last 5): Date | Severity | Category | Status.
`[View Full Welfare Analytics →]` link to Page 20.

**Tab 5 — Admissions**

Monthly admissions (students joining hostel) and departures (students leaving), last 6 months bar chart.
Current waitlist count per hostel type.

### 6.2 `welfare-incident-detail` Drawer — 560px, right-slide

**Trigger:** `[View Details]` in §5.2 welfare table.

**Header:**
```
Welfare Incident — [Category]  [Severity badge]             [×]
[Branch Name]  ·  [Hostel Type]  ·  [Date]
Status: [Open/Resolved]  ·  Reported by: [Name]
```

**Tab 1 — Incident Details**

Read-only fields: Date, Branch, Hostel Type (Boys/Girls), Category, Severity, Description (full text), Reported By, Reported At.

**Tab 2 — Resolution Log**

Timeline of status changes and notes. Shows resolution date and resolution notes if resolved.

**Tab 3 — Escalation History**

Which roles were notified, at what time, and whether they acknowledged.

> Role 106 is read-only on welfare incidents — they analyse but do not manage incidents (that is Division K's role). No action buttons except `[Add Internal Analyst Note]`.

### 6.3 `hostel-report-export` Modal — 480px, centred

**Trigger:** `[Export Hostel Report ↓]` header button.

| Field | Type | Required | Notes |
|---|---|---|---|
| Report Type | Select | Yes | Occupancy Summary / Welfare Trend / Fee Collection / Full Hostel Report |
| Academic Year | Select | Yes | Current + previous 2 AYs |
| Branches | Multi-select | No | Default: All hostel branches |
| Date Range | Date range picker | No | Optional override; defaults to full AY |
| Format | Radio | Yes | PDF · XLSX |

**Footer:** `[Cancel]`  `[Generate Export]`

---

## 7. Charts

### 7.1 Occupancy Rate by Branch — Horizontal Bar Chart

| Property | Value |
|---|---|
| Chart type | Horizontal bar (Chart.js 4.x) |
| Title | "Hostel Occupancy Rate by Branch — [Current Month, AY]" |
| Data | Occupancy rate (%) per hostel branch, current month |
| Y-axis | Branch names |
| X-axis | Occupancy rate (0–100%) |
| Bar colour | Green ≥ 85% · Amber 70–84% · Orange 60–69% · Red < 60% |
| Reference line | Vertical dotted line at 70% (minimum viable) and 85% (target) |
| Sorted | Ascending by occupancy rate (worst first) |
| Tooltip | "[Branch]: [N]% occupancy · [filled]/[total] beds filled" |
| Footer note | "Showing [N] hostel branches. Data as of [date]." |
| Empty state | "No hostel occupancy data available for the current month." |
| Export | PNG export button top-right of chart card |
| API endpoint | `GET /api/v1/group/{id}/analytics/hostel/occupancy-by-branch/` |
| HTMX | `<div id="chart-occupancy" hx-get="..." hx-trigger="load" hx-swap="innerHTML" hx-indicator="#chart-occ-spinner">` |

### 7.2 Welfare Incident Trend — Stacked Area Chart

| Property | Value |
|---|---|
| Chart type | Stacked area (Chart.js 4.x) |
| Title | "Welfare Incident Trend — Last 12 Months" |
| Data | Count of welfare incidents per month, stacked by severity (1/2/3/4) |
| X-axis | Month name (Jan–Dec or Apr–Mar per AY) |
| Y-axis | Incident count |
| Area colours | Sev 1: grey-200 · Sev 2: amber-200 · Sev 3: orange-300 · Sev 4: red-400 |
| Tooltip | "[Month] · Sev1: [N] · Sev2: [N] · Sev3: [N] · Sev4: [N] · Total: [N]" |
| Legend | Right side; severity labels with colour |
| Empty state | "No welfare incident data available for the last 12 months." |
| Export | PNG export button |
| API endpoint | `GET /api/v1/group/{id}/analytics/hostel/welfare-trend/?months=12` |
| HTMX | `<div id="chart-welfare-trend" hx-get="..." hx-trigger="load" hx-swap="innerHTML">` |

---

## 8. Toast Messages

| Action | Toast Text | Type |
|---|---|---|
| Export generated | "Hostel report exported to [format]. Download starting." | Success |
| Export failed | "Could not generate export. Please try again." | Error |
| Drawer loaded | (silent — no toast on successful drawer open) | — |
| Drawer load error | "Could not load hostel details for this branch. Please try again." | Error |
| Welfare incident detail load error | "Could not load incident details. Please try again." | Error |
| KPI refresh error | "Failed to refresh KPI data." | Error |
| Internal analyst note saved | "Note added to incident record." | Success |
| Note save error | "Could not save note. Please try again." | Error |

---

## 9. Empty States

| Context | Icon | Heading | Sub-text | Action |
|---|---|---|---|---|
| No hostel branches configured | `building-office` | "No Hostel Branches" | "No hostel branches are configured for this group. This dashboard applies only to groups with hostel facilities." | — |
| Occupancy table — no data | `table-cells` | "No Occupancy Data" | "Hostel occupancy records have not been submitted for this academic year." | — |
| Welfare table — no incidents | `check-circle` | "No Welfare Incidents" | "No welfare incidents have been logged for hostel branches in the selected period." | — |
| Fee table — no data | `currency-rupee` | "No Fee Data" | "Hosteler fee collection records are not available for this period." | — |
| Branch detail — occupancy tab — no data | `table-cells` | "No Occupancy Data" | "Occupancy records have not been submitted for this branch." | — |
| Branch detail — welfare tab — no incidents | `check-circle` | "No Welfare Incidents" | "No welfare events recorded for this hostel branch." | — |
| Branch detail — trend tab — no data | `chart-bar` | "No Trend Data" | "Insufficient historical data to show a trend." | — |
| Charts — no data | `chart-bar` | "No data available" | "Hostel data has not been loaded for the current period." | — |

---

## 10. Loader States

| Context | Loader Behaviour |
|---|---|
| Initial page load | KPI bar: 7 shimmer cards. Charts: 2 shimmer rectangles. Occupancy table: 6 shimmer rows. Welfare table: 5 shimmer rows. Fee summary: 3 shimmer rows. |
| Search or filter change | Relevant table rows replaced by shimmer rows + 20px spinner below toolbar |
| `hostel-branch-detail` drawer open | Drawer slides in; shimmer tab bar + shimmer content cards |
| Tab switch in drawer | Tab content replaced by shimmer rows while fetching |
| `welfare-incident-detail` drawer open | Drawer slides in; shimmer metadata lines |
| `[Generate Export]` submit | Button disabled + "Generating…" + spinner; file downloads on ready |
| Add internal note — save | Button disabled + spinner |
| Chart initial load | Shimmer rectangle with centred spinner per chart |
| KPI auto-refresh | Cards pulse; values update in place |
| Pagination click | Table body replaced by shimmer rows |

---

## 11. Role-Based UI Visibility

| UI Element | Role 106 (Hostel Analytics Officer) | All Others |
|---|---|---|
| Page | ✅ Full access | ❌ Redirected to own dashboard |
| KPI Summary Bar (all 7 cards) | ✅ | — |
| Charts (both) | ✅ | — |
| Occupancy table | ✅ Read-only | — |
| Welfare incidents table | ✅ Read-only | — |
| Fee summary table | ✅ Read-only | — |
| `[Export Hostel Report ↓]` button | ✅ | — |
| `hostel-branch-detail` drawer — all tabs | ✅ Read-only | — |
| `welfare-incident-detail` drawer | ✅ Read-only | — |
| `[Add Internal Analyst Note]` in welfare drawer | ✅ | — |
| `hostel-report-export` modal | ✅ | — |
| Alert banners | ✅ All banners | — |
| Quick navigation tiles | ✅ | — |

---

## 12. API Endpoints

### 12.1 KPI Summary
```
GET /api/v1/group/{group_id}/analytics/hostel/kpi/
```
Query: `academic_year` (optional).
Response: `{ "total_capacity": N, "filled_beds": N, "occupancy_rate_pct": N, "welfare_incidents_month": N, "severe_open_cases": N, "fee_rate_pct": N, "branches_reporting": N, "total_hostel_branches": N }`.

### 12.2 Occupancy by Branch
```
GET /api/v1/group/{group_id}/analytics/hostel/occupancy/
```

| Query Parameter | Type | Description |
|---|---|---|
| `zone` | string | Filter by zone ID |
| `occupancy_range` | string | `high` (≥85%) · `medium` (70–84%) · `low` (<70%) |
| `hostel_type` | string | `boys_ac` · `boys_nonac` · `girls_ac` · `girls_nonac` · `scholarship` |
| `state` | string | Filter by state |
| `search` | string | Search by branch name |
| `page` | integer | Default 1 |
| `page_size` | integer | 25 · 50 · All |
| `ordering` | string | `occupancy_rate_pct` (ASC default) · `branch_name` · `total_beds` · `waitlist_count` |

Response: `{ count, next, previous, results: [...] }`.

### 12.3 Welfare Incidents
```
GET /api/v1/group/{group_id}/analytics/hostel/welfare-incidents/
```

| Query Parameter | Type | Description |
|---|---|---|
| `severity` | int (multi) | 1 · 2 · 3 · 4 |
| `branch` | int | Filter by branch ID |
| `status` | string | `open` · `resolved` |
| `category` | string | `health` · `food` · `discipline` · `security` · `mental_health` · `other` |
| `date_from` | date | Filter incident date from |
| `date_to` | date | Filter incident date to |
| `search` | string | Search by branch name, description |
| `page` | integer | Default 1 |
| `page_size` | integer | 25 · 50 · 100 |
| `ordering` | string | `-severity` (default) · `-incident_date` · `days_open` |

Response: paginated list.

### 12.4 Fee Collection Summary (Hosteler)
```
GET /api/v1/group/{group_id}/analytics/hostel/fee-summary/
```
Query: `academic_year`, `top` (integer, default 10 — top N branches by outstanding).
Response: list of branches with fee demanded, collected, outstanding, rate, defaulter_count.

### 12.5 Branch Detail
```
GET /api/v1/group/{group_id}/analytics/hostel/branches/{branch_id}/
```
Response: Full detail object — occupancy_by_type, monthly_trend (12 months), fee_breakdown, welfare_summary, admissions_trend.

### 12.6 Welfare Incident Detail
```
GET /api/v1/group/{group_id}/analytics/hostel/welfare-incidents/{incident_id}/
```
Response: Full incident with resolution log and escalation history.

### 12.7 Add Internal Analyst Note
```
POST /api/v1/group/{group_id}/analytics/hostel/welfare-incidents/{incident_id}/notes/
```
Body: `{ "note": "string" }`. Role 106 only. Note is internal — not visible to Division H or branch.
Response: 201 Created.

### 12.8 Occupancy Chart Data
```
GET /api/v1/group/{group_id}/analytics/hostel/occupancy-by-branch/
```
Query: `month` (YYYY-MM), `academic_year`.
Response: `{ labels: [...branches], data: [...rates], colours: [...hex] }`.

### 12.9 Welfare Trend Chart Data
```
GET /api/v1/group/{group_id}/analytics/hostel/welfare-trend/
```
Query: `months` (default 12).
Response: `{ labels: [...month_names], datasets: [{ severity: 1, data: [...counts] }, ...] }`.

### 12.10 Export
```
GET /api/v1/group/{group_id}/analytics/hostel/export/
```
Query: `report_type`, `academic_year`, `branches` (comma-separated), `date_from`, `date_to`, `format` (pdf/xlsx).
Response: File download.

---

## 13. HTMX Patterns

| Pattern | Trigger Element | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI bar load + auto-refresh | `<div id="hostel-kpi-bar">` | GET `.../hostel/kpi/` | `#hostel-kpi-bar` | `innerHTML` | `hx-trigger="load, every 300s"` |
| Chart 7.1 load | `<div id="chart-occupancy">` | GET `.../hostel/occupancy-by-branch/` | `#chart-occupancy` | `innerHTML` | `hx-trigger="load"` |
| Chart 7.2 load | `<div id="chart-welfare-trend">` | GET `.../hostel/welfare-trend/` | `#chart-welfare-trend` | `innerHTML` | `hx-trigger="load"` |
| Occupancy table — search | `<input id="occ-search">` | GET `.../hostel/occupancy/?search=` | `#occupancy-table` | `innerHTML` | `hx-trigger="keyup changed delay:300ms"` |
| Occupancy table — filter chip | Filter chip selects | GET `.../hostel/occupancy/?filters=` | `#occupancy-table` | `innerHTML` | `hx-trigger="change"` |
| Occupancy table — pagination | Pagination buttons | GET `.../hostel/occupancy/?page={n}` | `#occupancy-table` | `innerHTML` | `hx-trigger="click"` |
| Welfare table — search/filter | Search + filters | GET `.../hostel/welfare-incidents/?filters=` | `#welfare-table` | `innerHTML` | `hx-trigger="keyup changed delay:300ms"` or `change` |
| Welfare table — pagination | Pagination buttons | GET `.../hostel/welfare-incidents/?page={n}` | `#welfare-table` | `innerHTML` | `hx-trigger="click"` |
| Open branch detail drawer | Branch name / [View] | GET `/htmx/analytics/hostel/branches/{branch_id}/detail/` | `#drawer-container` | `innerHTML` | `hx-trigger="click"` |
| Drawer tab switch | Tab buttons | GET `/htmx/analytics/hostel/branches/{branch_id}/tab/{tab_slug}/` | `#hostel-drawer-tab-content` | `innerHTML` | `hx-trigger="click"` |
| Open welfare incident detail | [View Details] button | GET `/htmx/analytics/hostel/welfare-incidents/{id}/detail/` | `#drawer-container` | `innerHTML` | `hx-trigger="click"` |
| Submit analyst note | Note form | POST `.../welfare-incidents/{id}/notes/` | `#incident-notes-section` | `innerHTML` | `hx-encoding="application/json"`; `hx-on::after-request="showToast(event);"` |
| Export modal — [Generate Export] | Export form | GET `.../hostel/export/?params=` | — | — | Triggers file download; spinner on button |
| KPI auto-refresh | `#hostel-kpi-bar` | GET `.../hostel/kpi/` | `#hostel-kpi-bar` | `innerHTML` | `hx-trigger="every 300s"` |

---

*Page spec version: 1.0 · Last updated: 2026-03-22*
