# 36 — BGV Status Tracker — Compliance View

- **URL:** `/group/hr/bgv/status/`
- **Template:** `portal_base.html`
- **Priority:** P0
- **Role:** Group BGV Manager (Role 48, G3)

---

## 1. Purpose

The BGV Status Tracker is the compliance dashboard that gives the BGV Manager and HR Director a branch-by-branch view of background verification coverage across the entire group. Where the BGV Registry (page 34) provides a staff-level register and the Processing Workflow (page 35) shows operative task queues, this page answers the governance question: which branches are fully compliant, which have BGV gaps, and which are in a critical state where students are being taught by staff whose background has not been verified?

The most serious compliance scenario this page monitors is new joiners who have begun student contact while their BGV is still pending. Under EduForge's policy (derived from POCSO-aligned safeguarding standards), no new staff member should enter a classroom without at minimum a Police Verification or a formal Pending BGV declaration acknowledged by the HR Director. This page highlights such cases with a Critical flag and the staff member's name. The POCSO Coordinator also has read access to this specific view.

The second critical monitoring function is BGV renewal tracking. BGV is not a one-time check — it expires after three years, and the institution must proactively renew it before expiry to maintain continuous coverage. The tracker shows, for each branch, how many staff have BGV expiring within the next six months so the BGV Manager can schedule renewals into the processing workflow before they lapse. A BGV that has lapsed (expired without renewal) is treated the same as a new joiner with no BGV — it creates a compliance gap.

The page is built around a branch-level summary table with a click-through drill-down to the staff-level BGV list for each branch. This two-level view allows the BGV Manager to quickly scan the group picture at the top level and then dive into any branch that needs attention without navigating back to the main registry. The compliance percentage for each branch — (Clear BGV count / Total staff count) × 100 — is the single most important metric on this page and drives the chart visualisation.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group BGV Manager | G3 | Full view + drill-down | Primary owner of compliance view |
| Group BGV Executive | G3 | Read Only | Can view compliance picture |
| Group HR Director | G3 | Full read + flag acknowledgement | Receives critical alerts |
| Group POCSO Coordinator | G3 | Read (new joiners unverified view) | POCSO overlap oversight |
| Group HR Manager | G3 | Read Only | General HR oversight |
| Group Performance Review Officer | G1 | No Access | Not applicable |

---

## 3. Page Layout

### 3.1 Breadcrumb
`Group Portal > HR & Staff > Background Verification > BGV Status Tracker`

### 3.2 Page Header
- **Title:** BGV Status Tracker — Compliance View
- **Subtitle:** Branch-level BGV coverage and compliance monitoring
- **Actions (top-right):**
  - `Export Compliance Report` (CSV/XLSX)
  - `Acknowledge Critical Flags` (button — visible to HR Director only, clears acknowledged items)
  - View Toggle: `Branch Summary` / `Staff List` (switches between the two table views)

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| New joiners in student contact with BGV pending | "CRITICAL: [N] new joiner(s) are in student contact without a verified BGV. HR Director notified." | Red — non-dismissible |
| Any branch below 80% compliance | "WARNING: [N] branch(es) are below 80% BGV compliance. Review staff list for gap details." | Amber — dismissible |
| Renewals due within 30 days | "URGENT: [N] staff BGV renewals are due within 30 days across [N] branches." | Amber — dismissible |
| Group compliance 100% | "All branches are at 100% BGV compliance. No action required." | Green — auto-dismiss 10s |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Group BGV Compliance Rate % | (Group-wide Clear BGV / Total Staff) × 100 | Green ≥ 95%, Amber 85–94%, Red < 85% | No drill-down |
| Branches at 100% BGV | Count of branches with compliance = 100% | Green if = all branches | Filters to fully compliant branches |
| Branches with Gaps | Count of branches with compliance < 100% | Amber if > 0 | Filters to branches with gaps |
| New Joiners Unverified (Critical) | Count of new joiners with no Clear BGV in student contact | Red if > 0, Green if 0 | Filters staff list to critical cases |
| Renewals Due in 3 Months | Count of BGVs expiring within 90 days | Amber if > 0 | Filters to expiry view |
| Flagged Staff Active | Count of staff with Flagged BGV still in system | Red if > 0, Green if 0 | Filters to Flagged |

---

## 5. Main Table — Branch BGV Compliance Summary

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Branch | Text + link to drill-down | Yes | Yes — dropdown |
| Total Staff | Integer | Yes | No |
| BGV Complete | Integer | Yes | No |
| BGV Pending | Integer | Yes | Yes (> 0 filter) |
| BGV Expired | Integer | Yes | Yes (> 0 filter) |
| Flagged | Integer (red if > 0) | Yes | Yes (> 0 filter) |
| Compliance % | Progress bar + number | Yes | Yes — range |
| Status | Badge (Compliant / At Risk / Critical) | No | Yes — multi-select |
| Actions | Drill-down icon | No | No |

### 5.1 Filters
- **Status:** Compliant / At Risk / Critical
- **Compliance % Range:** slider (0–100%)
- **Has Flagged Staff:** Yes / No
- **Has Expired BGV:** Yes / No
- **Has Renewals Due:** Within 30 days / 90 days / 6 months

### 5.2 Search
Free-text search on Branch Name. Debounced `hx-get` on keyup (400 ms).

### 5.3 Pagination
Server-side, 20 rows per page (branch count is typically lower than staff count; 20 is sufficient for most groups). Shows `Showing X–Y of Z branches`.

---

## 6. Drawers

### 6.1 Create
Not applicable — this is a compliance view page. BGV records are created via the BGV Registry (page 34).

### 6.2 Drill-Down: Branch Staff BGV List
**Trigger:** Click branch row or drill-down icon
**Opens as:** Full-page overlay or side panel (not a narrow drawer — this is a secondary data-rich table)
**Displays:** All staff in the selected branch with: Staff Name, Role, BGV Status, BGV Type, Initiated Date, Expiry Date, Agency, Actions (link to full record in BGV Registry). Filterable by status within the drill-down. Back button returns to branch summary.

### 6.3 Acknowledgement Modal (HR Director only)
**Trigger:** `Acknowledge Critical Flags` button
**Displays:** List of all critical flags (new joiners unverified, flagged staff active). HR Director checks each acknowledgement box with a note (e.g., "BGV in progress — police visit scheduled 24 March 2026"). Submit → logs acknowledgement with timestamp. Clears the critical-flag banner for 48 hours (re-triggers if not resolved).

### 6.4 Initiate Renewal (from drill-down)
**Trigger:** Renew icon on expiring-soon staff rows in the drill-down view
**Action:** Opens the BGV Registry's Initiate BGV drawer in Renewal mode, pre-populated with the staff member's details. Saves a round-trip to the Registry page.

---

## 7. Charts

**BGV Compliance Rate by Branch (Horizontal Bar Chart)**
- One bar per branch, showing compliance % (0–100%)
- Red benchmark line at 100%
- Bars coloured: Green (100%), Amber (80–99%), Red (< 80%)
- Sorted by compliance % ascending (worst-performing branches at top)
- Tooltip: hover shows exact counts (Clear / Pending / Expired / Flagged)

**Group BGV Status Over Time (Line Chart)**
- X-axis: Month (last 12 months)
- Y-axis: Group-wide compliance %
- Shows trend: is compliance improving or declining?
- Useful for presenting to HR Director / Board

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Critical flag acknowledged | "Critical flag for [Staff Name] acknowledged by HR Director. Review in 48 hours." | Info | 5s |
| Export triggered | "BGV compliance report export started." | Info | 4s |
| Renewal initiated from drill-down | "BGV renewal initiated for [Staff Name]. Assigned to BGV Executive queue." | Success | 4s |
| Filter applied | "Showing [N] branches matching selected filters." | Info | 3s |
| No critical flags | "No critical flags currently active." | Success | 3s |

---

## 9. Empty States

- **No branches loaded:** "No branch data available. Contact system administrator."
- **All branches compliant:** "All branches are at 100% BGV compliance. No gaps detected."
- **No results match filters:** "No branches match the selected compliance filters. Try adjusting the criteria."
- **Drill-down: no staff:** "No staff records found for this branch. The branch may have no active staff."

---

## 10. Loader States

- Branch summary table skeleton: 8 rows with shimmer.
- KPI cards: shimmer on initial load.
- Drill-down: spinner while staff-level BGV data for selected branch loads.
- Chart area: placeholder with "Loading chart…" text.

---

## 11. Role-Based UI Visibility

| Element | BGV Manager (G3) | HR Director (G3) | POCSO Coordinator (G3) |
|---|---|---|---|
| Branch summary table | Full view | Full view | New Joiners Unverified section only |
| Drill-down to staff list | Full view | Full view | Critical/unverified staff only |
| Acknowledge Critical Flags button | Hidden | Visible + enabled | Hidden |
| Initiate Renewal from drill-down | Visible + enabled | Hidden | Hidden |
| Export Compliance Report | Visible | Visible | Hidden |
| Group Compliance Over Time chart | Visible | Visible | Hidden |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/hr/bgv/status/` | JWT G3 | Branch-level BGV compliance summary |
| GET | `/api/v1/hr/bgv/status/{branch_id}/staff/` | JWT G3 | Staff-level BGV list for one branch |
| POST | `/api/v1/hr/bgv/status/acknowledge/` | JWT G3 HR Director | Acknowledge critical flags |
| GET | `/api/v1/hr/bgv/status/kpis/` | JWT G3 | Group-level KPI data |
| GET | `/api/v1/hr/bgv/status/charts/compliance/` | JWT G3 | Compliance rate by branch chart data |
| GET | `/api/v1/hr/bgv/status/charts/trend/` | JWT G3 | Compliance trend over time chart data |
| GET | `/api/v1/hr/bgv/status/export/` | JWT G3 | Export compliance report |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Search branch name | keyup changed delay:400ms | GET `/api/v1/hr/bgv/status/?q={val}` | `#bgv-status-table-body` | innerHTML |
| Filter change | change | GET `/api/v1/hr/bgv/status/?{params}` | `#bgv-status-table-body` | innerHTML |
| Pagination click | click | GET `/api/v1/hr/bgv/status/?page={n}` | `#bgv-status-table-body` | innerHTML |
| Drill-down: click branch row | click | GET `/api/v1/hr/bgv/status/{branch_id}/staff/` | `#drill-down-panel` | innerHTML |
| Acknowledge flags form submit | submit | POST `/api/v1/hr/bgv/status/acknowledge/` | `#alert-banner-container` | innerHTML |
| Load compliance chart | load | GET `/api/v1/hr/bgv/status/charts/compliance/` | `#chart-compliance` | innerHTML |
| Load trend chart | load | GET `/api/v1/hr/bgv/status/charts/trend/` | `#chart-trend` | innerHTML |
| Refresh KPIs after action | htmx:afterRequest | GET `/api/v1/hr/bgv/status/kpis/` | `#kpi-bar` | innerHTML |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
