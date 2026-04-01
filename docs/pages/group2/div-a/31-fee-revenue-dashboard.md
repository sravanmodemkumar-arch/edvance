# 31 — Fee Revenue Dashboard

> **URL:** `/group/gov/fee-dashboard/`
> **File:** `31-fee-revenue-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Chairman G5 · MD G5 · CEO G4 (full) · VP G4 (read) · Trustee G1 (read — aggregated only)

---

## 1. Purpose

Group-wide fee revenue monitoring dashboard. Provides the Chairman, MD, and CEO with a real-time
and historical view of fee collection across all branches — total collected, outstanding,
defaulters, advance payments, category-wise breakdown, and branch-level drill-down.

Replaces the fee widgets on CEO/Chairman dashboards which show only top-line numbers. This page
is the full fee intelligence layer for the group at the governance level.

---

## 2. Role Access

| Role | Access | Scope |
|---|---|---|
| Chairman | Full — all data, all branches | All |
| MD | Full | All |
| CEO | Full — read + export | All |
| VP | Read-only — aggregated + branch summary | All branches |
| Trustee | Read-only — current year totals only | Aggregated |
| Others | ❌ | — |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Fee Revenue Dashboard
```

### 3.2 Page Header
```
Fee Revenue Dashboard                                  [Export Report ↓]  [↻ Refresh]
Academic Year: Apr 2025 – Mar 2026  ·  Data as of: [date time]
```

### 3.3 Period Selector
```
[This Month]  [This Quarter]  [This Academic Year]  [Custom Range]
```

---

## 4. KPI Summary Cards (top row)

**Display:** 6 cards — icon · label · value · trend vs previous period.

| Card | Label | Value Example | Trend |
|---|---|---|---|
| 1 | Total Fee Collected | ₹12,47,83,200 | ↑ 8% vs last year |
| 2 | Outstanding Amount | ₹3,18,45,600 | ↓ 3% vs last month |
| 3 | Collection Rate | 79.6% | ↑ 2.1 pp |
| 4 | Active Defaulters | 1,248 students | ↑ 43 vs last month |
| 5 | Advance Payments | ₹48,32,000 | — |
| 6 | Concessions / Waivers | ₹22,15,000 | — |

**Auto-refresh:** Every 5 minutes (HTMX polling on KPI bar).

---

## 5. Fee Category Breakdown (tab below KPI cards)

### 5.1 Tabs
```
By Category  |  By Branch  |  By Month  |  Defaulters
```

---

### Tab 1: By Category

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Fee Category | Text | ✅ | Day Scholar Tuition · Hostel · Transport · Coaching · Lab · Sports · Others |
| Expected | Currency | ✅ | Total billed amount for selected period |
| Collected | Currency | ✅ | |
| Outstanding | Currency | ✅ | |
| Collection % | Progress bar + % | ✅ | Colour: Green ≥90% · Yellow 70–89% · Red <70% |
| Students Billed | Number | ✅ | |
| Defaulters | Number | ✅ | |
| Actions | — | ❌ | Drill Down |

**Default sort:** Outstanding descending (highest gap first).

**[Drill Down]:** Opens `fee-category-drill` drawer.

---

### Tab 2: By Branch

**Search:** Branch name. Debounce 300ms.

**Filters:** Zone · State · Collection % range · Defaulters >N.

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Branch | Text | ✅ | Branch name + city |
| Zone | Badge | ✅ | |
| Expected | Currency | ✅ | |
| Collected | Currency | ✅ | |
| Outstanding | Currency | ✅ | |
| Collection % | Progress bar + % | ✅ | Colour coded |
| Defaulters | Number | ✅ | |
| Last Collection Date | Date | ✅ | Date of most recent payment recorded |
| Actions | — | ❌ | [Drill Down] [Send Reminder] |

**Default sort:** Collection % ascending (worst branches first).

**Pagination:** 25/page.

**[Drill Down]:** Opens `fee-branch-drill` drawer (branch fee detail).

**[Send Reminder]:** Opens `fee-reminder-modal` for that branch.

---

### Tab 3: By Month

**Display:** Month-by-month breakdown for current academic year.

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Month | Text | ✅ | Apr 2025, May 2025, … |
| Expected | Currency | ✅ | |
| Collected | Currency | ✅ | |
| Outstanding | Currency | ✅ | |
| Collection % | Number + colour bar | ✅ | |
| New Defaulters | Number | ✅ | Students who fell into default this month |
| Cleared Defaulters | Number | ✅ | Defaulters who paid up this month |

**Default sort:** Month chronological.

---

### Tab 4: Defaulters

**Search:** Student name, branch name. Debounce 300ms.

**Filters:** Branch · Zone · Fee Category · Outstanding > ₹ (numeric filter) · Months Overdue.

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Student Name | Text | ✅ | Visible to Chairman/MD/CEO only (PII) |
| Student ID | Text | ✅ | |
| Branch | Text | ✅ | |
| Class | Text | ✅ | |
| Fee Category | Badge | ✅ | |
| Total Outstanding | Currency | ✅ | |
| Months Overdue | Number | ✅ | Red if ≥3 months |
| Last Payment Date | Date | ✅ | |
| Concession Applied | Badge | ✅ | Yes / No |
| Actions | — | ❌ | [View Details] [Send Reminder] |

**Default sort:** Total Outstanding descending.

**Pagination:** 25/page.

**Bulk actions (Chairman/MD/CEO):** Select rows → [Send Reminder to Selected] · [Export Selected].

---

## 6. Drawers & Modals

### 6.1 Drawer: `fee-category-drill`
- **Trigger:** By Category tab → [Drill Down]
- **Width:** 640px
- **Tabs:** Summary · By Branch · By Month

#### Tab: Summary
- Category name + total expected/collected/outstanding/collection%
- Student count breakdown: Billed · Paid in Full · Partially Paid · Not Paid
- Average outstanding per student

#### Tab: By Branch
- Branch-level breakdown for this category
- Same columns as main By Branch tab (scoped to this category)

#### Tab: By Month
- Monthly trend for this category with line chart (collected vs outstanding)

---

### 6.2 Drawer: `fee-branch-drill`
- **Trigger:** By Branch tab → [Drill Down]
- **Width:** 640px
- **Tabs:** Summary · By Category · Defaulters · History

#### Tab: Summary
- Branch metadata (name, city, principal)
- This branch: Expected · Collected · Outstanding · Collection%
- Trend vs last 3 months (mini sparkline)
- Last 5 payments received (date + amount)

#### Tab: By Category
- Category breakdown for this branch only

#### Tab: Defaulters
- Defaulter list for this branch — student-level (same columns as main Defaulters tab)
- [Send Bulk Reminder] for this branch's defaulters

#### Tab: History
- Monthly fee collection history for this branch — 12 months
- Line chart: collected (blue) + outstanding (red) per month

---

### 6.3 Modal: `fee-reminder-modal`
- **Width:** 480px
- **Purpose:** Send fee reminder to branch principal or directly to defaulting students/parents
- **Fields:**
  | Field | Type | Required |
  |---|---|---|
  | Send To | Radio | ✅ | Branch Principal · All Defaulters (via WhatsApp/SMS) · Both |
  | Channel | Multi-select | ✅ | WhatsApp · SMS · Email |
  | Message Template | Select | ✅ | Standard Reminder · Final Notice · Friendly Reminder |
  | Custom Note | Textarea | ❌ | Appended to template |
- **Preview:** Shows final message text before sending
- **Buttons:** [Send Reminder] + [Cancel]

---

## 7. Charts

### 7.1 Collection Rate Trend (12 months)
- **Type:** Line chart (area fill)
- **Data:** Monthly collection % (this year vs last year)
- **Threshold:** 90% target line (dashed)
- **Export:** PNG

### 7.2 Fee Category Distribution — Collected vs Outstanding
- **Type:** Grouped horizontal bar chart
- **Data:** One row per category — bar for collected (green) + outstanding (red)
- **Export:** PNG

### 7.3 Branch Collection Heatmap
- **Type:** Treemap (area proportional to expected fee, colour = collection %)
- **Data:** One rectangle per branch, size = expected, colour = collection%
- **Colour scale:** Green (100%) → Yellow (70%) → Red (<70%)
- **Export:** PNG

### 7.4 Defaulter Trend (last 6 months)
- **Type:** Bar chart
- **Data:** New defaulters (red) and cleared defaulters (green) per month
- **Export:** PNG

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Data refreshed | "Fee data refreshed" | Info | 3s |
| Reminder sent (branch) | "Fee reminder sent to [Branch] principal" | Success | 4s |
| Reminder sent (bulk students) | "Reminder sent to [N] defaulter families" | Success | 4s |
| Export started | "Fee report generating…" | Info | Manual |
| Export ready | "Fee report ready — click to download" | Success | Manual |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No data for period | "No fee data for selected period" | "Try a different date range" | [Change Period] |
| No defaulters | "No defaulters" | "All students are current on fees" | — |
| No branch data | "No branches match" | "Try different filters" | [Clear Filters] |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: KPI bar (6 cards) + tab content (table 8 rows) |
| Period selector change | KPI bar skeleton + tab content skeleton |
| Tab switch | Inline table skeleton |
| Filter apply | Inline skeleton rows |
| Drill-down drawer | Spinner in drawer |
| Chart initial load | Chart skeleton (grey rectangle placeholder) |
| Refresh button | Spinner in Refresh button + KPI skeleton |
| Export | Spinner in export button |

---

## 11. Role-Based UI Visibility

| Element | Chairman/MD | CEO | VP | Trustee |
|---|---|---|---|---|
| All KPI cards | ✅ | ✅ | ✅ | Aggregated only |
| By Category tab | ✅ | ✅ | ✅ | ❌ |
| By Branch tab | ✅ | ✅ | ✅ | ❌ |
| By Month tab | ✅ | ✅ | ✅ | ❌ |
| Defaulters tab | ✅ | ✅ | ❌ | ❌ |
| Student names (PII) | Chairman/MD | ✅ | ❌ | ❌ |
| [Send Reminder] | ✅ | ✅ | ❌ | ❌ |
| [Export Report] | ✅ | ✅ | ❌ | ❌ |
| All charts | ✅ | ✅ | ✅ | ❌ |
| Drill-down drawers | ✅ | ✅ | Branch summary only | ❌ |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/fee-dashboard/summary/` | JWT (G4/G5) | KPI summary cards |
| GET | `/api/v1/group/{id}/fee-dashboard/by-category/` | JWT (G4/G5) | Category breakdown |
| GET | `/api/v1/group/{id}/fee-dashboard/by-branch/` | JWT (G4/G5) | Branch breakdown |
| GET | `/api/v1/group/{id}/fee-dashboard/by-month/` | JWT (G4/G5) | Monthly breakdown |
| GET | `/api/v1/group/{id}/fee-dashboard/defaulters/` | JWT (G4/G5) | Defaulters list |
| GET | `/api/v1/group/{id}/fee-dashboard/branch/{bid}/drill/` | JWT (G4/G5) | Branch drill-down |
| GET | `/api/v1/group/{id}/fee-dashboard/category/{cat}/drill/` | JWT (G4/G5) | Category drill-down |
| POST | `/api/v1/group/{id}/fee-dashboard/send-reminder/` | JWT (G4/G5) | Send fee reminder |
| GET | `/api/v1/group/{id}/fee-dashboard/charts/collection-trend/` | JWT (G4/G5) | Collection trend chart |
| GET | `/api/v1/group/{id}/fee-dashboard/charts/by-category/` | JWT (G4/G5) | Category bar chart |
| GET | `/api/v1/group/{id}/fee-dashboard/charts/heatmap/` | JWT (G4/G5) | Branch heatmap |
| GET | `/api/v1/group/{id}/fee-dashboard/charts/defaulter-trend/` | JWT (G4/G5) | Defaulter trend chart |
| GET | `/api/v1/group/{id}/fee-dashboard/export/` | JWT (G4/G5) | Export fee report |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Period selector | `click` | GET `.../fee-dashboard/summary/?period=` | `#kpi-bar` | `innerHTML` |
| Tab switch | `click` | GET `.../fee-dashboard/{tab}/?period=` | `#fee-tab-content` | `innerHTML` |
| Search (branch/defaulter) | `input delay:300ms` | GET `.../fee-dashboard/{tab}/?q=` | `#table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../fee-dashboard/{tab}/?filters=` | `#table-section` | `innerHTML` |
| Drill-down drawer | `click` | GET `.../fee-dashboard/{tab}/drill/` | `#drawer-body` | `innerHTML` |
| KPI auto-refresh | `every 5m` | GET `.../fee-dashboard/summary/` | `#kpi-bar` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
