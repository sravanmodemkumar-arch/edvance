# [01] — Legal & Compliance Dashboard

> **URL:** `/group/legal/dashboard/`
> **File:** `n-01-legal-compliance-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Role:** Group Compliance Manager (Role 109, G1) — primary landing page for entire Legal & Compliance division

---

## 1. Purpose

The Legal & Compliance Dashboard is the central command centre for the Group Compliance Manager and other legal/compliance roles within an Institution Group. It aggregates compliance health data from all branches into a single unified view, enabling group-level oversight without navigating to individual branch portals. Every critical compliance signal — overdue RTI requests, POCSO incidents pending resolution, upcoming affiliation renewals, data breach alerts, and insurance expiries — surfaces here in real time.

This dashboard serves two audiences simultaneously. For the Group Compliance Manager (Role 109, G1), it provides a comprehensive daily briefing on the compliance posture of all 5–50 branches in the group. For the Chairman/CEO (G4/G5), it provides an executive summary with a single group-wide compliance score and the count of critical unresolved items requiring escalation.

The page is the mandatory landing page when any Division N user logs in. Data is refreshed every 5 minutes automatically. All metric cards, alert banners, and charts are driven by HTMX polling or on-load lazy fetch. No write operations are available from this page — it is a read-only synthesis layer; actual actions are performed on the respective sub-module pages.

Scale: 5–50 branches · 20–500 compliance items per branch · 100–25,000 compliance items group-wide

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Legal Officer | 108 | G0 | No Platform Access | Works in external tools; no login |
| Group Compliance Manager | 109 | G1 | Read — Full Dashboard | Primary user; all widgets visible |
| Group RTI Officer | 110 | G1 | Read — Dashboard (RTI widget highlighted) | RTI summary card is primary focus |
| Group Regulatory Affairs Officer | 111 | G0 | No Platform Access | External filings only |
| Group POCSO Reporting Officer | 112 | G1 | Read — Dashboard (POCSO widget only) | Sees only POCSO KPI card + alert |
| Group Data Privacy Officer | 113 | G1 | Read — Dashboard (DPO widget highlighted) | DPDP breach card is primary focus |
| Group Contract Administrator | 127 | G3 | Read — Dashboard (Contracts widget) | Sees contract expiry KPI card |
| Group Legal Dispute Coordinator | 128 | G1 | Read — Dashboard (Litigation widget) | Litigation count card visible |
| Group Insurance Coordinator | 129 | G1 | Read — Dashboard (Insurance widget) | Insurance expiry card visible |

> **Access enforcement:** `@require_role(min_level=G1, division='N')` on all views and API endpoints.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Legal & Compliance  ›  Dashboard
```

### 3.2 Page Header
```
Legal & Compliance Dashboard                    [Export PDF]  [Settings ⚙]
Group Compliance Manager — Priya Krishnamurthy
Sunrise Education Group · 28 branches · Last refreshed: 2 min ago
```

### 3.3 Alert Banner (conditional)

| Condition | Banner Text | Severity |
|---|---|---|
| Any POCSO incident open > 24 hours without NCPCR report | "URGENT: [N] POCSO incident(s) require NCPCR reporting within 24 hours — POCSO Act 2012" | Critical (red) |
| Any data breach not notified within 72 hours | "CRITICAL: Data breach at [Branch] reported [X] hours ago — CERT-In notification overdue — DPDP Act 2023" | Critical (red) |
| Any RTI request overdue beyond 30 days | "[N] RTI request(s) are overdue. Mandatory response deadline passed — RTI Act 2005" | High (amber) |
| Any affiliation expiring within 30 days | "[N] branch affiliation(s) expire within 30 days. Immediate renewal action required." | High (amber) |
| Any insurance policy expiring within 30 days | "[N] insurance policy(ies) expire within 30 days — potential coverage gap for students and property." | Medium (yellow) |
| Overall compliance score drops below 70% | "Group compliance score is [X]% — below threshold. Review Cross-Branch Status." | Medium (yellow) |

---

## 4. KPI Summary Bar (8 cards)

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Branches Compliant | N / Total branches | COUNT branches where compliance_score ≥ 90 / total_branches | Green ≥ 80%, Amber 60–79%, Red < 60% | `#kpi-branches-compliant` |
| 2 | Deadlines This Month | Count | COUNT items where due_date within current calendar month | Red if > 10, Amber 5–10, Green < 5 | `#kpi-deadlines-month` |
| 3 | Overdue Items | Count | COUNT items where due_date < TODAY and status ≠ 'completed' | Red if > 0, Green = 0 | `#kpi-overdue` |
| 4 | Pending RTI Requests | Count | COUNT rti_requests where status IN ('received','in_progress') | Red if any overdue, Amber if > 5, Green ≤ 5 | `#kpi-rti-pending` |
| 5 | POCSO Incidents Open | Count | COUNT pocso_incidents where status ≠ 'closed' | Red if > 0, Green = 0 | `#kpi-pocso-open` |
| 6 | Data Breaches Reported | Count (this FY) | COUNT dpdp_breaches where created_date within current FY | Red if cert_in_notified = False, Amber if < 72hr, Green all notified | `#kpi-breaches` |
| 7 | Contracts Expiring (60d) | Count | COUNT staff_contracts where expiry_date within 60 days | Amber if > 5, Green ≤ 5 | `#kpi-contracts-expiring` |
| 8 | Group Compliance Score | Percentage | Weighted average of all compliance dimensions across all branches | Green ≥ 80%, Amber 60–79%, Red < 60% | `#kpi-group-score` |

**HTMX:** All 8 cards use `hx-get="/api/v1/group/{id}/legal/dashboard/kpis/"` with `hx-trigger="load, every 60s"` → `hx-swap="innerHTML"`. 60-second refresh ensures critical alerts (POCSO, breach, RTI overdue) surface without delay. Individual targets allow partial refresh without full page reload.

---

## 5. Sections

### 5.1 Overdue & Urgent Items Table

Displays all compliance items across all branches where `due_date < TODAY` or flagged as urgent (POCSO, breach). Sorted by severity descending, then by days overdue descending.

Search: Full-text search across item name, branch, category. Debounced 350ms. HTMX: `hx-get` → `hx-target="#overdue-table-body"`.

Filter chips: `All` · `POCSO` · `RTI` · `Affiliation` · `Insurance` · `Filings` · `Contracts`

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| # | Auto-index | No | Row number |
| Item | Text | Yes | Compliance item name with category badge |
| Branch | Text | Yes | Branch name + city |
| Category | Badge | Yes | Colour-coded: POCSO=red, RTI=orange, Affiliation=blue, etc. |
| Due Date | Date | Yes | Original deadline |
| Days Overdue | Integer | Yes | TODAY − due_date; red badge if positive |
| Status | Badge | Yes | Overdue / Pending / Critical |
| Assigned To | Text | No | Role name responsible |
| Action | Button | No | "View →" — navigates to relevant sub-module page |

**Default sort:** Days Overdue DESC
**Pagination:** Server-side · Default 25/page

### 5.2 Upcoming Deadlines (Next 30 Days)

Timeline-style list of all compliance deadlines falling within the next 30 days. Each item shows days remaining as a countdown badge.

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Deadline | Date | Yes | Due date |
| Days Left | Badge | Yes | Green > 14d, Amber 7–14d, Red ≤ 7d |
| Item | Text | Yes | Compliance item description |
| Branch | Text | Yes | Branch name |
| Category | Badge | Yes | Filing type |
| Responsible Role | Text | No | Role handling this item |
| Quick Link | Icon | No | → opens sub-module directly |

**Default sort:** Deadline ASC (soonest first)
**Pagination:** Server-side · Default 20/page

### 5.3 Branch Compliance Snapshot

Mini-table showing every branch with its overall compliance score and a traffic-light indicator. Provides quick navigation to the full Cross-Branch Compliance Status page (N-19).

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Branch | Text | Yes | Branch name + city |
| Score | Progress bar + % | Yes | 0–100; green ≥ 90, amber 60–89, red < 60 |
| Critical Issues | Integer | Yes | Count of red-flag items |
| Last Updated | Datetime | Yes | When compliance data was last synced |
| Action | Button | No | "Details →" → opens N-19 filtered to this branch |

**Default sort:** Score ASC (worst first)
**Pagination:** Server-side · Default 15/page (shows all branches if ≤ 50)

---

## 6. Drawers & Modals

### 6.1 Drawer: `compliance-item-detail` (640px, right-slide)
Opens when clicking any row in the Overdue Items table.
- **Tabs:** Overview · Timeline · Documents · Notes
- **Overview tab:** Item name, category, description, branch, due date, responsible role, current status, regulatory reference (e.g., "RTI Act 2005 — s.7(1)"), escalation path
- **Timeline tab:** Chronological log of all status changes with timestamps and user
- **Documents tab:** List of documents attached to this compliance item; download links
- **Notes tab:** Internal notes field (read-only for G1; editable for G3+)
- **Footer:** "Go to [Module] →" button navigates to relevant sub-module page

### 6.2 Modal: `export-dashboard`
- **Width:** 480px
- **Title:** "Export Compliance Dashboard Report"
- **Fields:** Date range (from/to), Include sections (checkboxes: KPIs, Overdue Items, Upcoming Deadlines, Branch Scores), Format (PDF / XLSX), Recipient email (optional)
- **Buttons:** Cancel · Generate Report
- **Behaviour:** POST to `/api/v1/group/{id}/legal/dashboard/export/` → triggers async task → toast on completion

### 6.3 Modal: `settings-panel`
- **Width:** 560px
- **Title:** "Dashboard Settings"
- **Fields:** Auto-refresh interval (1 min / 5 min / 15 min / Off), KPI threshold configuration (e.g., compliance score alert threshold), Email alerts (toggle per alert type), Notification recipients
- **Access:** G4/G5 only
- **Buttons:** Cancel · Save Settings

---

## 7. Charts

### 7.1 Group Compliance Score Trend (Line Chart)

| Property | Value |
|---|---|
| Chart type | Line (Chart.js 4.x) |
| Title | "Group Compliance Score — Last 12 Months" |
| Data | Monthly compliance score (0–100) for the group as a whole |
| X-axis | Month (Jan–Dec) |
| Y-axis | Score (0–100) |
| Colour | Line: `#3B82F6` (blue); reference line at 80% threshold: `#EF4444` dashed |
| Tooltip | "Score: [value]% in [Month Year]" |
| API endpoint | `GET /api/v1/group/{id}/legal/dashboard/compliance-trend/` |
| HTMX | `hx-get` on load → `hx-target="#chart-compliance-trend"` → `hx-swap="innerHTML"` |
| Export | PNG |

### 7.2 Compliance by Category (Donut Chart)

| Property | Value |
|---|---|
| Chart type | Donut (Chart.js 4.x) |
| Title | "Open Issues by Compliance Category" |
| Data | Count of open/overdue items per category: Affiliation, RTI, POCSO, DPDP, Insurance, Contracts, Filings |
| X-axis | N/A (donut) |
| Y-axis | N/A (donut) |
| Colour | Each segment: distinct palette — red (POCSO), orange (RTI), blue (Affiliation), purple (DPDP), green (Insurance), teal (Contracts), yellow (Filings) |
| Tooltip | "[Category]: [N] open items ([X]% of total)" |
| API endpoint | `GET /api/v1/group/{id}/legal/dashboard/issues-by-category/` |
| HTMX | `hx-get` on load → `hx-target="#chart-issues-donut"` → `hx-swap="innerHTML"` |
| Export | PNG |

### 7.3 Branch Compliance Score Bar Chart

| Property | Value |
|---|---|
| Chart type | Horizontal bar (Chart.js 4.x) |
| Title | "Branch-wise Compliance Scores" |
| Data | Compliance score per branch (all branches in group) |
| X-axis | Score (0–100) |
| Y-axis | Branch name |
| Colour | Green ≥ 90, Amber 60–89, Red < 60 (dynamic per bar) |
| Tooltip | "[Branch]: [Score]% — [N] open issues" |
| API endpoint | `GET /api/v1/group/{id}/legal/dashboard/branch-scores/` |
| HTMX | `hx-get` on load → `hx-target="#chart-branch-scores"` → `hx-swap="innerHTML"` |
| Export | PNG |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Dashboard data refreshed | "Dashboard refreshed successfully" | Success | 2s |
| POCSO alert triggered | "CRITICAL: POCSO incident requires immediate NCPCR reporting" | Error | 10s (sticky) |
| Data breach alert triggered | "CRITICAL: Data breach notification overdue — CERT-In deadline missed" | Error | 10s (sticky) |
| Export report triggered | "Generating compliance report — you'll receive it via email shortly" | Info | 4s |
| Export report ready | "Compliance Dashboard Report is ready. Click to download." | Success | 8s |
| Settings saved | "Dashboard settings updated" | Success | 3s |
| Filter applied | "Showing [N] items matching filter: [filter name]" | Info | 2s |
| API error on refresh | "Dashboard refresh failed. Retrying in 30 seconds." | Warning | 5s |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| No overdue items | ✅ checklist | "All Items On Track" | "No overdue compliance items across all branches. Great work!" | View Upcoming Deadlines |
| No upcoming deadlines in 30 days | 📅 calendar | "Clear Calendar Ahead" | "No compliance deadlines in the next 30 days." | View Full Compliance Calendar |
| No branches configured | 🏫 building | "No Branches Added Yet" | "Add branch locations to begin compliance tracking." | Configure Branches |
| Dashboard data unavailable | ⚠️ warning | "Data Temporarily Unavailable" | "Unable to load compliance data. Please try refreshing." | Refresh Dashboard |
| New group — no history | 📊 chart | "Compliance Tracking Starting" | "Compliance history will appear after the first data sync." | — |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | Full-page skeleton with grey shimmer cards for all 8 KPI slots |
| KPI card refresh | Inline spinner inside each card container (24px) |
| Table data load | Table skeleton: 5 grey shimmer rows matching column widths |
| Chart data fetch | Chart placeholder with grey canvas + "Loading chart data..." label |
| Drawer open | Right-slide skeleton with 3 tab-shaped placeholders |
| Export generation | Modal: progress bar with "Generating report… [X]%" |
| Branch snapshot load | 5-row skeleton with progress-bar placeholder in Score column |

---

## 11. Role-Based UI Visibility

| Element | Compliance Manager (109, G1) | Data Privacy Officer (113, G1) | POCSO Officer (112, G1) | Contract Admin (127, G3) | CEO/Chairman (G4/G5) |
|---|---|---|---|---|---|
| All 8 KPI Cards | Visible | Visible (DPDP card highlighted) | POCSO card highlighted only | Contracts card highlighted | All visible |
| Overdue Items Table | Full table | Filtered to DPDP/Consent rows | Filtered to POCSO rows | Filtered to Contracts rows | Full table |
| Upcoming Deadlines | All items | DPDP items only | POCSO items only | Contract items only | All items |
| Branch Snapshot | All branches | All branches | All branches | All branches | All branches |
| All 3 Charts | Visible | DPDP chart only | POCSO chart only | Contracts view | All visible |
| Export PDF Button | Visible | Visible (scoped export) | Not visible | Not visible | Visible (full export) |
| Settings Button | Not visible | Not visible | Not visible | Not visible | G4/G5 only |
| Alert Banners | All banners | DPDP breach banner only | POCSO banner only | Contract expiry banner | All banners |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/legal/dashboard/kpis/` | G1+ | Returns all 8 KPI values |
| GET | `/api/v1/group/{id}/legal/dashboard/overdue-items/` | G1+ | Paginated list of overdue compliance items |
| GET | `/api/v1/group/{id}/legal/dashboard/upcoming-deadlines/` | G1+ | Items due in next 30 days |
| GET | `/api/v1/group/{id}/legal/dashboard/branch-snapshot/` | G1+ | Per-branch compliance score summary |
| GET | `/api/v1/group/{id}/legal/dashboard/compliance-trend/` | G1+ | Monthly score trend — last 12 months |
| GET | `/api/v1/group/{id}/legal/dashboard/issues-by-category/` | G1+ | Count per compliance category |
| GET | `/api/v1/group/{id}/legal/dashboard/branch-scores/` | G1+ | Bar chart data: score per branch |
| POST | `/api/v1/group/{id}/legal/dashboard/export/` | G1+ | Trigger async PDF/XLSX report generation |
| GET | `/api/v1/group/{id}/legal/dashboard/export/{task_id}/status/` | G1+ | Poll export task status |
| PATCH | `/api/v1/group/{id}/legal/dashboard/settings/` | G4+ | Update dashboard configuration |

### Query Parameters for Overdue Items

| Parameter | Type | Description |
|---|---|---|
| `category` | string | Filter by compliance category (pocso, rti, affiliation, insurance, contracts, filings, dpdp) |
| `branch_id` | integer | Filter to specific branch |
| `severity` | string | critical / high / medium |
| `page` | integer | Page number (default: 1) |
| `page_size` | integer | Items per page (default: 25, max: 100) |

### Query Parameters for Upcoming Deadlines

| Parameter | Type | Description |
|---|---|---|
| `days_ahead` | integer | Lookahead window in days (default: 30, max: 90) |
| `category` | string | Filter by compliance category |
| `branch_id` | integer | Filter to specific branch |
| `page` | integer | Page number |

---

## 13. HTMX Patterns

| Pattern | Trigger Element | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| Auto-refresh KPIs | `<div id="kpi-bar">` | `hx-get="/api/v1/group/{id}/legal/dashboard/kpis/"` | `#kpi-bar` | `innerHTML` | `hx-trigger="load, every 60s"` |
| Overdue table filter | Filter chip buttons | `hx-get="/api/v1/group/{id}/legal/dashboard/overdue-items/?category={cat}"` | `#overdue-table-body` | `innerHTML` | `hx-trigger="click"` |
| Upcoming deadlines load | `<div id="upcoming-deadlines">` | `hx-get="/api/v1/group/{id}/legal/dashboard/upcoming-deadlines/"` | `#upcoming-deadlines` | `innerHTML` | `hx-trigger="load"` |
| Branch snapshot load | `<div id="branch-snapshot">` | `hx-get="/api/v1/group/{id}/legal/dashboard/branch-snapshot/"` | `#branch-snapshot` | `innerHTML` | `hx-trigger="load"` |
| Open compliance item drawer | Row click in overdue table | `hx-get="/api/v1/group/{id}/legal/compliance-items/{item_id}/"` | `#right-drawer` | `innerHTML` | `hx-trigger="click"` + `hx-push-url="false"` |
| Overdue table search | Search input | `hx-get="/api/v1/group/{id}/legal/dashboard/overdue-items/?q={query}"` | `#overdue-table-body` | `innerHTML` | `hx-trigger="keyup changed delay:350ms"` |
| Export trigger | Export PDF button | `hx-post="/api/v1/group/{id}/legal/dashboard/export/"` | `#export-status` | `innerHTML` | Shows progress modal on response |
| Pagination — overdue | Pagination controls | `hx-get` with `?page={n}` | `#overdue-table-body` | `innerHTML` | Replaces table body only |

---

*Page spec version: 1.1 · Last updated: 2026-03-22*
