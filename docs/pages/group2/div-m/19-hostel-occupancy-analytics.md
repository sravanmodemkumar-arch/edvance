# 19 — Hostel Occupancy Analytics

> **URL:** `/group/analytics/hostel-occupancy/`
> **File:** `19-hostel-occupancy-analytics.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Role 102 (Group Analytics Director), Role 103 (Group MIS Officer), Role 106 (Group Hostel Analytics Officer), Role 107 (Group Strategic Planning Officer)

---

## 1. Purpose

This page provides comprehensive analytics on hostel occupancy rates, bed utilisation, and admission fill rates across all branches of the group. It tracks occupancy by branch and by hostel type — Boys AC, Boys Non-AC, Girls AC, Girls Non-AC, Scholarship, and Special Needs — giving the Hostel Analytics Officer a single command view of all residential assets. The page identifies under-utilised hostels (high vacancy signals revenue leakage) and over-subscribed hostels that require waitlist management or capacity expansion. Hostel fee collection rates specific to boarders are tracked separately from day-scholar fee collection to isolate hosteler payment behaviour. All data on this page feeds directly into MIS reports (Page 07) and informs the branch feasibility and 3-year expansion plan (Pages 21 and 22).

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Hostel Analytics Officer | 106 | G1 | Full — View, Filter, Export, Send Reminders, Edit Hostel Config | Primary owner of this page |
| Group Analytics Director | 102 | G1 | View + Export + Dashboard override | Can view all data; cannot edit hostel config |
| Group MIS Officer | 103 | G1 | View + Export | Can export for inclusion in MIS reports |
| Group Strategic Planning Officer | 107 | G1 | View only | Read-only; uses data to inform feasibility studies |
| All other Division M roles | 104, 105 | G1 | No access | Not relevant to their domain |
| All other divisions | — | G2–G5 | No access | Enforced at Django view level |

**Django access enforcement:** All views decorated with `@role_required([102, 103, 106, 107])`. Role 106 gets `hostel_full_access=True` context flag enabling edit/reminder buttons. Roles 102, 103, 107 get `hostel_full_access=False` — edit/configure buttons are hidden in template with `{% if hostel_full_access %}` guards. Export is available to 102, 103, 106 only; 107 sees data but no export button.

---

## 3. Page Layout

### 3.1 Breadcrumb

```
Home > Group Analytics > Hostel Occupancy Analytics
```

### 3.2 Page Header

**Title:** Hostel Occupancy Analytics
**Subtitle:** Bed utilisation, occupancy rates, and fee collection across all hostel branches — AY 2025-26

**Action Buttons (right-aligned):**
- `[Export Report]` — opens export modal (roles 102, 103, 106 only); triggers CSV/XLSX/PDF export
- `[Refresh Data]` — `hx-post="/api/v1/hostel/occupancy/refresh/"` forces cache-bust recalculation
- `[AY Selector]` — dropdown: 2023-24 / 2024-25 / 2025-26 (default current); `hx-get` reloads all sections
- `[Branch Filter]` — multi-select dropdown: All Branches (default) or specific branches

### 3.3 Alert Banners

All banners are individually dismissible per session (JS sets `sessionStorage` key on dismiss; template checks key on render).

| Condition | Banner Text | Severity |
|---|---|---|
| Any branch occupancy < 60% this month | "Revenue leakage alert: [N] branch(es) have hostel occupancy below 60%. Review under-utilisation and consider targeted admissions drives." | Red (Critical) |
| Any branch waitlist count > 20 | "Capacity pressure: [N] branch(es) have waitlists exceeding 20 students. Capacity expansion may be required." | Amber (Warning) |
| Hostel fee collection < 80% at any branch | "Fee collection below threshold: [N] branch(es) have hosteler fee collection below 80%. Review defaulters." | Amber (Warning) |
| Hostel data not updated for > 7 days at any branch | "Data staleness: [N] branch(es) have not updated hostel occupancy data in over 7 days. Analytics may be unreliable." | Blue (Info) |

---

## 4. KPI Summary Bar

HTMX auto-refresh: the entire KPI bar has `id="hostel-kpi-bar"` and refreshes every 5 minutes via `hx-trigger="load, every 300s"` pointing to `/api/v1/hostel/kpi-summary/`. A subtle spinner appears in the bar's right corner during refresh.

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Total Hostel Capacity | Count of total beds across all branches and hostel types | `SUM(beds)` across all `HostelRoom` records for current AY | Static grey | `#kpi-total-capacity` |
| 2 | Current Total Occupancy | Count of students currently assigned to hostel beds | `SUM(occupied_beds)` from latest occupancy snapshot | Static grey | `#kpi-current-occupancy` |
| 3 | Overall Occupancy Rate (%) | Group-wide average occupancy as percentage | `(occupied / capacity) × 100`, rounded to 1 decimal | ≥ 90% green · 75–89% amber · 60–74% orange · < 60% red | `#kpi-occupancy-rate` |
| 4 | Under-Utilised Branches | Branches where current occupancy rate < 70% | Count of branches with `occupancy_rate < 70` | 0 = green · 1–2 = amber · 3+ = red | `#kpi-underutilised` |
| 5 | Over-Subscribed Branches | Branches with at least 1 student on waitlist | Count of branches with `waitlist_count > 0` | 0 = green · 1–2 = amber · 3+ = red | `#kpi-oversubscribed` |
| 6 | Total Waitlist Count | Group-wide total of students on hostel waitlists | `SUM(waitlist_count)` across all branches | 0 = green · 1–20 = amber · 21+ = red | `#kpi-waitlist-total` |
| 7 | Hosteler Fee Collection Rate (%) | Percentage of hostel fees collected vs demanded, group-wide | `(hostel_fees_collected / hostel_fees_demanded) × 100` for current AY | ≥ 90% green · 80–89% amber · 70–79% orange · < 70% red | `#kpi-fee-collection` |

---

## 5. Sections

### 5.1 Hostel Occupancy Table

Main table showing one row per branch. Default sort: Occupancy Rate ascending (worst first). Paginated: 25 rows per page.

**Search:** Text input with 300ms debounce (`hx-trigger="keyup changed delay:300ms"`), searches Branch Name. Placeholder: "Search branch name…"

**Filter Chips (horizontal row above table):**
- Occupancy Status: All | Critical (<60%) | Low (60–74%) | Good (75–89%) | Excellent (≥90%)
- Hostel Type: All | Boys AC | Boys Non-AC | Girls AC | Girls Non-AC | Scholarship
- Fee Status: All | Below 80% | 80–89% | 90%+
- Has Waitlist: All | Yes | No
- State: dropdown (auto-populated from branch data)

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Branch | Text | Yes | Branch short name + district tooltip |
| Total Hostel Beds | Integer | Yes | Sum across all hostel types for this branch |
| Current Occupancy | Integer | Yes | Count of currently occupied beds |
| Occupancy Rate (%) | Percentage | Yes (default, asc) | Colour-coded: ≥90% = green badge · 75–89% = amber · 60–74% = orange · <60% = red |
| Boys AC (beds/filled) | Text "X/Y" | No | X = capacity, Y = occupied; dash if hostel type not present at branch |
| Boys Non-AC (beds/filled) | Text "X/Y" | No | Same format |
| Girls AC (beds/filled) | Text "X/Y" | No | Same format |
| Girls Non-AC (beds/filled) | Text "X/Y" | No | Same format |
| Scholarship (beds/filled) | Text "X/Y" | No | Same format |
| Waitlist Count | Integer | Yes | Red badge if > 0; green "None" if 0 |
| Fee Collection Rate (%) | Percentage | Yes | Colour-coded same as occupancy rate thresholds |
| Last Updated | Date + relative time | Yes | e.g. "2026-03-18 (3 days ago)"; orange if > 7 days, red if > 14 days |
| Actions | Button group | No | [View Details] opens `hostel-branch-detail` drawer · [Edit Config] (role 106 only) |

**Row-level colour rule:** If Occupancy Rate < 60%, entire row has a light red background (`bg-red-50`). If Last Updated > 7 days, `Last Updated` cell has orange text.

**Pagination:** Django paginator, 25 per page. HTMX `hx-push-url="true"` to maintain URL state on page navigation.

---

### 5.2 Occupancy Trend Analysis

Month-by-month occupancy trend for the group or for a selected branch. Default view: group-wide aggregate.

**Controls:**
- Branch selector (dropdown: All Branches or specific branch) — `hx-get` reloads chart and table
- AY selector (2023-24 / 2024-25 / 2025-26) — `hx-get` reloads
- View toggle: Group Total | By Branch (stacked)

**Trend Table** (below the chart, same data in tabular form):

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Month | Text | No | Apr through Mar |
| Total Beds | Integer | No | Branch capacity for that month (may change if beds added) |
| Occupied Beds | Integer | Yes | Snapshot count at month-end |
| Occupancy Rate (%) | Percentage | Yes | Colour-coded |
| Boys (total) | Integer | No | Boys AC + Boys Non-AC combined |
| Girls (total) | Integer | No | Girls AC + Girls Non-AC combined |
| Scholarship | Integer | No | Scholarship hostel occupied |
| MoM Change | Text (↑N% / ↓N%) | No | Green if positive, red if negative |

---

### 5.3 Hostel Fee Collection

Detailed hosteler fee collection breakdown by branch and hostel type. This section focuses only on hostel-related fees (accommodation, mess, AC surcharge, extras) — not tuition fees.

**Filter Chips:** Fee Type: All | Accommodation | Mess | AC Surcharge | Extras; Branch; Month Range

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Branch | Text | Yes | |
| Hostel Type | Badge | No | Boys AC / Boys Non-AC / Girls AC / Girls Non-AC / Scholarship |
| Total Hostelers | Integer | Yes | Students currently in this hostel type at this branch |
| Fees Demanded (₹) | Currency | Yes | Total fees billed for current AY |
| Fees Collected (₹) | Currency | Yes | Total collected |
| Collection Rate (%) | Percentage | Yes | Colour-coded |
| Defaulters Count | Integer | Yes | Students with any outstanding hostel fee |
| Outstanding Amount (₹) | Currency | Yes | Total uncollected amount |
| Mess Fees | Currency | No | Mess fee component specifically |
| Actions | Button | No | [View Defaulters] opens defaulter list in side panel |

**Pagination:** 25 per page.

---

### 5.4 Waitlist Management

Branches with active hostel waitlists. Only branches with `waitlist_count > 0` appear. If no branches have waitlists, empty state shown.

**Filter Chips:** Hostel Type | Branch | Priority (First-come-first-served / Scholarship-priority)

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Branch | Text | Yes | |
| Hostel Type | Badge | No | Which hostel type has the waitlist |
| Waitlist Count | Integer | Yes (default, desc) | |
| Longest Wait (days) | Integer | Yes | Days since earliest waitlist entry |
| Expected Vacancy (date) | Date | No | Based on known discharge schedule; blank if unknown |
| Priority Students | Integer | No | Students with scholarship/special needs priority |
| Actions | Button | No | [Manage Waitlist] opens management panel (role 106 only); others see [View] |

---

## 6. Drawers & Modals

### Drawer: `hostel-branch-detail`

**Width:** 560px (right-side slide-in)
**Trigger:** [View Details] button in Hostel Occupancy Table
**HTMX:** `hx-get="/api/v1/hostel/branch/{branch_id}/detail/"` `hx-target="#hostel-drawer"` `hx-swap="innerHTML"`
**Close:** × button or click outside; HTMX `hx-on="htmx:afterRequest: closeDrawer()"`

#### Tab 1 — Occupancy

| Field / Element | Type | Notes |
|---|---|---|
| Branch Name | Heading | Large bold |
| Academic Year | Badge | e.g. "AY 2025-26" |
| Occupancy Rate Gauge | Circular gauge (Chart.js Doughnut) | 0–100%, colour per threshold |
| Capacity vs Filled (per type) | Table | Hostel Type · Capacity · Occupied · Vacancy · Rate% |
| Boys AC | Row | |
| Boys Non-AC | Row | |
| Girls AC | Row | |
| Girls Non-AC | Row | |
| Scholarship | Row | |
| Special Needs | Row | Hidden if not applicable |
| **Totals** | Row | Bold |
| Current Waitlist | Integer with badge | Red if > 0 |
| Waitlist Breakdown | Text list | e.g. "Girls AC: 8 students · Boys Non-AC: 3 students" |
| Last Occupancy Update | Date + relative | Orange/red if stale |

#### Tab 2 — Monthly Trend

| Field / Element | Type | Notes |
|---|---|---|
| Bar Chart | Chart.js Bar | Month on x-axis, Occupancy Rate % on y-axis, last 12 months. Reference line at 75% (target). Tooltip shows absolute figures (X/Y beds). |
| Month-wise Table | Table | Month · Capacity · Occupied · Rate% · MoM change |
| AY Selector | Dropdown | Reload chart via `hx-get` |

#### Tab 3 — Fee Collection

| Field / Element | Type | Notes |
|---|---|---|
| Total Fees Demanded (₹) | Currency display | Current AY |
| Total Fees Collected (₹) | Currency display | |
| Collection Rate (%) | Large badge | Colour-coded |
| Defaulters Count | Integer with link | Links to defaulter list |
| Outstanding Amount (₹) | Currency | Red text |
| Fee Breakdown Table | Table | Fee Type (Accommodation / Mess / AC Surcharge / Extras) · Demanded · Collected · Rate% |
| Month-wise Collection | Sparkline chart | 12-month fee collection trend |
| [Export Fee Report] | Button | Role 103 and 106 only; triggers export job |

#### Tab 4 — Admissions

| Field / Element | Type | Notes |
|---|---|---|
| Monthly Admissions Chart | Chart.js Line | Admissions (joins) and Discharges (leaves) per month, last 12 months |
| Admissions Table | Table | Month · New Joins · Discharges · Net Change · End-of-Month Count |
| Net Change Trend | Badge per row | Green if positive, red if negative |
| YTD Admissions | Integer | Total hostel admissions since April 1 |
| YTD Discharges | Integer | Total hostel discharges since April 1 |
| Avg Stay Duration | Text | e.g. "8.3 months" (for discharged students this AY) |

#### Tab 5 — Welfare Link

| Field / Element | Type | Notes |
|---|---|---|
| Total Welfare Incidents This AY | Integer with badge | From this branch's hostel records |
| Severity Breakdown | Mini table | Sev 1 · Sev 2 · Sev 3 · Sev 4 counts |
| Open Cases | Integer | Red badge if > 0 |
| Most Recent Incident | Text | Date + severity + brief category |
| [View Hostel Welfare Analytics] | Button/Link | Navigates to Page 20 (`/group/analytics/hostel-welfare/`) pre-filtered to this branch |
| [View Welfare Cases (Division K)] | External link | Opens Division K welfare case management (read-only for Division M roles) |

---

### Modal: Export Report

**Width:** 480px
**Title:** Export Hostel Occupancy Report
**Trigger:** [Export Report] button in page header

| Field | Type | Required | Validation |
|---|---|---|---|
| Export Format | Radio: PDF / XLSX / CSV | Yes | |
| Academic Year | Dropdown | Yes | Default: current AY |
| Branches | Multi-select | Yes | Default: All |
| Include Charts | Toggle | No | PDF only; hidden for XLSX/CSV |
| Date Range | Date range picker | No | Optional; overrides full-AY default |
| Delivery | Radio: Portal Download / Email / Both | Yes | |
| Email Recipients | Text (comma-separated) | If email/both | Shown only when email delivery selected |

**Footer:** `[Cancel]` · `[Generate Export]` — triggers export job, redirects to Export Centre (Page 24) with job pre-selected.

---

## 7. Charts

### Chart 7.1 — Occupancy Rate by Branch

| Property | Value |
|---|---|
| Chart Type | Horizontal bar chart (Chart.js Bar, indexAxis: 'y') |
| Title | "Occupancy Rate by Branch — AY 2025-26" |
| Data | One bar per branch; value = current occupancy rate (%) |
| Sort Order | Ascending by occupancy rate (lowest at top — worst-first) |
| X-axis | Percentage (0–100%); reference line at 75% (target) and 90% (excellent) |
| Y-axis | Branch names (truncated to 20 chars; full name in tooltip) |
| Colours | Bar fill per occupancy threshold: <60% = red (`#EF4444`) · 60–74% = orange (`#F97316`) · 75–89% = amber (`#F59E0B`) · ≥90% = green (`#10B981`) |
| Tooltip | "Branch: [Name] · Occupancy: X% · Occupied: N/M beds · Waitlist: W" |
| API Endpoint | `GET /api/v1/hostel/charts/occupancy-by-branch/?ay=2025-26` |
| HTMX Pattern | Chart rendered on page load; AY selector change triggers `hx-get` to reload data endpoint, Chart.js `.update()` called in callback |
| Empty State | "No hostel data available for this academic year." |

### Chart 7.2 — Occupancy Trend (Boys vs Girls)

| Property | Value |
|---|---|
| Chart Type | Line chart (Chart.js Line) |
| Title | "Group Hostel Occupancy Trend — Last 12 Months" |
| Data | Two lines: Boys Total Occupancy % and Girls Total Occupancy % per month |
| X-axis | Month labels (Apr-25 through Mar-26) |
| Y-axis | Occupancy Rate (%); range 0–100 |
| Colours | Boys: blue (`#3B82F6`) · Girls: pink (`#EC4899`) · Both lines tension: 0.4 (smooth curve) |
| Fill | Light fill under each line (opacity 0.1) for readability |
| Tooltip | "Month: [Month] · Boys: X% (N beds) · Girls: Y% (M beds)" |
| API Endpoint | `GET /api/v1/hostel/charts/occupancy-trend/?ay=2025-26&split=gender` |
| HTMX Pattern | Loaded on page load; branch selector change POSTs branch filter, reloads data |
| Legend | Displayed below chart; Boys / Girls clickable to toggle visibility |
| Empty State | "Insufficient trend data. Occupancy records for at least 2 months required." |

---

## 8. Toast Messages

| Action | Toast Text | Type | Duration |
|---|---|---|---|
| Page data refreshed | "Hostel occupancy data refreshed successfully." | Success | 3s |
| Refresh failed | "Data refresh failed. Please try again." | Error | Manual dismiss |
| Export job created | "Export '[Name]' queued. Check Export Centre for progress." | Success | 4s |
| Export generation failed | "Export generation failed. Please review filters and retry." | Error | Manual dismiss |
| Hostel config saved (role 106) | "Hostel configuration for [Branch] saved successfully." | Success | 3s |
| Hostel config save failed | "Failed to save hostel configuration. Please try again." | Error | Manual dismiss |
| Waitlist management action saved | "Waitlist updated for [Branch] — [Hostel Type]." | Success | 3s |
| Data reminder sent to branch | "Data update reminder sent to [Branch Principal]." | Success | 4s |
| Reminder send failed | "Failed to send reminder. Check network and retry." | Error | Manual dismiss |
| AY filter applied | "Showing data for AY [year]." | Info | 2s |
| Branch filter applied | "Filtered to [N] selected branch(es)." | Info | 2s |

---

## 9. Empty States

| Context | Icon | Heading | Sub-text | Action |
|---|---|---|---|---|
| No hostel data for selected AY | Building icon | "No Hostel Data Found" | "No hostel occupancy records exist for AY [year]. Data may not have been entered yet." | [Go to Data Quality Dashboard] |
| No branches match current filters | Filter icon | "No Branches Match Filters" | "Try removing one or more filter chips to see results." | [Clear All Filters] |
| Waitlist Management — no active waitlists | Check circle icon | "No Active Waitlists" | "All hostel branches are operating within capacity. No waitlist management required." | — |
| Hostel Occupancy Table — search returns no results | Search icon | "No Branches Found" | "No branches match '[search term]'. Check spelling or broaden search." | [Clear Search] |
| Fee Collection — no fee data | Receipt icon | "No Fee Data Available" | "Hostel fee collection data has not been entered for the selected period." | [View Data Quality Dashboard] |
| Trend data — only 1 month of data | Chart icon | "Insufficient Trend Data" | "At least 2 months of data are required to display occupancy trends." | — |
| Branch detail drawer — no welfare incidents | Shield icon | "No Welfare Incidents" | "No welfare incidents recorded for this hostel branch in AY [year]." | — |

---

## 10. Loader States

| Context | Loader Behaviour |
|---|---|
| Initial page load | Full-page skeleton loader: KPI bar shows 7 grey pill placeholders; table shows 8 skeleton rows with shimmer animation |
| KPI bar auto-refresh | Subtle spinner icon in top-right corner of KPI bar; existing values remain visible until new values arrive |
| Table row loading (after filter change) | Table body replaced with 6 skeleton rows (`hx-indicator` on table container); spinner in filter chip area |
| Hostel branch detail drawer opening | Drawer slides in with spinning loader in centre; content swaps in once API response arrives |
| Chart data loading | Chart area shows grey placeholder box with animated spinner; chart renders once data arrives |
| Export job submission | [Generate Export] button shows inline spinner and disables; text changes to "Queuing…" |
| Refresh Data button | Button shows spinner and disables for duration of refresh; re-enables on response |
| Waitlist panel loading | Panel content area shows skeleton rows |

---

## 11. Role-Based UI Visibility

| UI Element | Role 102 (Dir) | Role 103 (MIS) | Role 106 (Hostel) | Role 107 (Strategic) |
|---|---|---|---|---|
| View Hostel Occupancy Table | Yes | Yes | Yes | Yes |
| View KPI Summary Bar | Yes | Yes | Yes | Yes |
| View Occupancy Trend Section | Yes | Yes | Yes | Yes |
| View Fee Collection Section | Yes | Yes | Yes | Yes |
| View Waitlist Management | Yes | Yes | Yes | Yes |
| [Export Report] button | Yes | Yes | Yes | No |
| [Refresh Data] button | Yes | Yes | Yes | No |
| [Edit Config] button (table row) | No | No | Yes | No |
| [Manage Waitlist] button | No | No | Yes | No |
| [View Defaulters] link | Yes | Yes | Yes | No |
| Send Data Reminder (drawer Tab 3) | No | Yes | Yes | No |
| Branch detail drawer Tab 5 Welfare Link | Yes | Yes | Yes | No |
| [Export Fee Report] in drawer | No | Yes | Yes | No |
| AY Selector | Yes | Yes | Yes | Yes |
| Branch Filter | Yes | Yes | Yes | Yes |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/hostel/occupancy/` | JWT · roles 102,103,106,107 | List hostel occupancy by branch |
| GET | `/api/v1/hostel/kpi-summary/` | JWT · roles 102,103,106,107 | KPI bar data |
| GET | `/api/v1/hostel/branch/{branch_id}/detail/` | JWT · roles 102,103,106,107 | Full branch hostel detail for drawer |
| GET | `/api/v1/hostel/trend/` | JWT · roles 102,103,106,107 | Monthly occupancy trend data |
| GET | `/api/v1/hostel/fee-collection/` | JWT · roles 102,103,106 | Hostel fee collection data |
| GET | `/api/v1/hostel/waitlist/` | JWT · roles 102,103,106,107 | Active waitlist data by branch |
| GET | `/api/v1/hostel/charts/occupancy-by-branch/` | JWT · roles 102,103,106,107 | Data for Chart 7.1 |
| GET | `/api/v1/hostel/charts/occupancy-trend/` | JWT · roles 102,103,106,107 | Data for Chart 7.2 |
| POST | `/api/v1/hostel/occupancy/refresh/` | JWT · roles 103,106 | Force recalculation of occupancy snapshot |
| PATCH | `/api/v1/hostel/branch/{branch_id}/config/` | JWT · role 106 only | Update hostel config (bed counts, type labels) |
| POST | `/api/v1/hostel/export/` | JWT · roles 102,103,106 | Trigger hostel report export job |
| POST | `/api/v1/hostel/reminder/` | JWT · roles 103,106 | Send data update reminder to branch principal |

**Query Parameters — `/api/v1/hostel/occupancy/`:**

| Parameter | Type | Default | Description |
|---|---|---|---|
| `ay` | string | current AY | Academic year e.g. `2025-26` |
| `branch_ids` | comma-separated integers | all | Filter to specific branches |
| `occupancy_status` | string | all | `critical`, `low`, `good`, `excellent` |
| `has_waitlist` | boolean | — | `true` to show only branches with waitlists |
| `fee_status` | string | all | `below80`, `80to89`, `90plus` |
| `state` | string | — | Filter by state name |
| `search` | string | — | Search branch name |
| `page` | integer | 1 | Page number |
| `page_size` | integer | 25 | Results per page |
| `sort_by` | string | `occupancy_rate` | Column to sort |
| `sort_dir` | string | `asc` | `asc` or `desc` |

**Query Parameters — `/api/v1/hostel/trend/`:**

| Parameter | Type | Default | Description |
|---|---|---|---|
| `ay` | string | current AY | Academic year |
| `branch_id` | integer | — | Specific branch; omit for group aggregate |
| `split` | string | `gender` | `gender`, `type`, `none` |
| `months` | integer | 12 | Number of months of history |

---

## 13. HTMX Patterns

| Pattern | Trigger Element | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI bar auto-refresh | KPI bar div (timer) | `hx-get="/api/v1/hostel/kpi-summary/"` `hx-trigger="load, every 300s"` | `#hostel-kpi-bar` | `innerHTML` | Runs on load and every 5 min |
| Branch name search | Search input | `hx-get="/api/v1/hostel/occupancy/"` `hx-trigger="keyup changed delay:300ms"` | `#occupancy-table-body` | `innerHTML` | Includes all active filter values as hx-include |
| Filter chip select | Each filter chip | `hx-get="/api/v1/hostel/occupancy/"` `hx-trigger="click"` | `#occupancy-table-body` | `innerHTML` | Re-sends all filter params |
| Table pagination | Page number links | `hx-get="/api/v1/hostel/occupancy/?page=N"` | `#occupancy-table-wrapper` | `outerHTML` | `hx-push-url="true"` |
| AY selector change | AY dropdown | `hx-get="/api/v1/hostel/occupancy/"` `hx-trigger="change"` | `#occupancy-table-body` | `innerHTML` | Also reloads KPI bar and charts |
| Open branch detail drawer | [View Details] button | `hx-get="/api/v1/hostel/branch/{id}/detail/"` | `#hostel-drawer-content` | `innerHTML` | Also sets drawer visible via JS |
| Drawer tab switch | Tab button | `hx-get="/api/v1/hostel/branch/{id}/detail/?tab=N"` | `#drawer-tab-content` | `innerHTML` | Lazy-loads each tab content |
| Refresh Data button | [Refresh Data] button | `hx-post="/api/v1/hostel/occupancy/refresh/"` `hx-trigger="click"` | `#hostel-page-content` | `outerHTML` | Shows spinner; full content reload |
| Trend branch selector | Branch dropdown (§5.2) | `hx-get="/api/v1/hostel/trend/"` `hx-trigger="change"` | `#trend-chart-wrapper` | `innerHTML` | Passes branch_id param |
| Send reminder | [Send Reminder] button | `hx-post="/api/v1/hostel/reminder/"` | `#reminder-response` | `innerHTML` | Validates form before submit |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
