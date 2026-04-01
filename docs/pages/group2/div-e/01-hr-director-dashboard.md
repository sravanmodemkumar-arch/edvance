# 01 — Group HR Director Dashboard

- **URL:** `/group/hr/director/`
- **Template:** `portal_base.html`
- **Priority:** P0
- **Role:** Group HR Director (Role 41, G3)

---

## 1. Purpose

The Group HR Director Dashboard is the command centre for the senior-most HR authority in the group. It provides a consolidated, real-time view of all human resource health indicators across every branch — covering staff strength, recruitment velocity, background verification compliance, POCSO training adherence, disciplinary pipeline, and pending approvals. Given that the group operates 5–50 branches with 2,000–100,000 students, the HR Director must be able to spot systemic risk before it becomes a legal or operational crisis.

This dashboard aggregates data that would otherwise require visiting each branch individually. It eliminates blind spots by surfacing the branches with the worst BGV compliance, the highest vacancy rates, and the most unresolved disciplinary cases — all in one screen. The HR Director uses this data to direct the HR team, escalate to the Group CEO, and respond to regulatory inquiries (CBSE, state board, NCPCR) with confidence.

The dashboard also functions as an approval gateway. All inter-branch transfers, disciplinary outcomes, and high-severity welfare cases route through the HR Director's approval queue shown prominently on this page. Pending approvals older than 48 hours are colour-flagged amber, and those older than 72 hours are flagged red with an auto-notification to the Director's registered email.

From a risk management perspective, this page enforces the rule that no staff member with a failed or expired BGV may remain in student-facing roles — any such case triggers a red banner that cannot be dismissed until the underlying record is resolved. Similarly, any active POCSO incident across any branch escalates to this dashboard automatically, ensuring the Director is never unaware of child-safety events.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group HR Director | G3 | Full read + approve/reject | Primary role; sees all branches |
| Group HR Manager | G3 | Full read | Cannot action Director-level approvals |
| Group CEO / Principal | G3 | Read-only summary | Access limited to KPI bar and alerts |
| Group Performance Review Officer | G1 | No access | This dashboard is above G1 scope |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → HR & Staff → Director Dashboard
```

### 3.2 Page Header
- **Title:** `Group HR Director Dashboard`
- **Subtitle:** `Staff Overview — All Branches · [Total Staff Count] employees · AY [current academic year]`
- **Role Badge:** `Group HR Director`
- **Right-side controls:** `Export Report (PDF)` · `Pending Approvals ([count])` · `Notification Bell`

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| Any staff working with students has failed/expired BGV | "⚠ [N] staff member(s) with failed or expired BGV are currently active in student-facing roles. Immediate action required." | Red (non-dismissible) |
| Active POCSO incident reported in any branch | "🔴 Active POCSO incident at [Branch Name]. Escalation required. Click to view." | Red (non-dismissible) |
| Vacancy rate > 10% in any branch | "Vacancy alert: [Branch Name] has [N] critical vacancies exceeding 10% of sanctioned strength." | Amber |
| Pending Director approvals > 72 hours old | "[N] approval(s) have been pending for more than 72 hours. Review now." | Amber |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Total Staff | Count of all active employees across all branches | Blue (informational) | Links to Staff Directory (`/group/hr/staff/`) |
| Open Positions | Count of unfilled sanctioned posts group-wide | Green < 5%, Amber 5–10%, Red > 10% | Links to Recruitment Drives list |
| BGV Pending | Staff with BGV not initiated or in-progress > 30 days | Green = 0, Amber 1–10, Red > 10 | Links to BGV Manager Dashboard |
| POCSO Non-Compliant | Staff who have not completed mandatory POCSO training | Green = 0, Amber 1–20, Red > 20 | Links to POCSO Coordinator Dashboard |
| Transfers Pending Approval | Inter-branch transfer requests awaiting Director sign-off | Green = 0, Amber 1–5, Red > 5 | Opens Transfer Approval drawer |
| Appraisals Pending | Staff whose annual appraisal cycle is incomplete | Green = 0, Amber 1–50, Red > 50 | Links to Performance Review Dashboard |
| Turnover (Last 12 M) | Rolling 12-month attrition rate as a percentage | Green < 10%, Amber 10–20%, Red > 20% | Links to Exit Analysis report |

---

## 5. Main Table — Branch HR Health

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Branch Name | Text (link to branch HR detail) | Yes | Yes (multi-select) |
| Staff Count | Integer | Yes | No |
| Sanctioned Strength | Integer | Yes | No |
| Vacancies | Integer (Sanctioned − Actual) | Yes | Yes (> N) |
| BGV Complete % | Percentage bar | Yes | Yes (< threshold) |
| POCSO Trained % | Percentage bar | Yes | Yes (< threshold) |
| Active Disciplinary Cases | Integer | Yes | Yes (> 0) |
| Last HR Audit Date | Date | Yes | Yes (date range) |
| Health Score | Badge (Green/Amber/Red) | Yes | Yes (status) |
| Actions | Icon buttons | No | No |

### 5.1 Filters

| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select dropdown | All branches in the group |
| Health Score | Checkbox group | Green / Amber / Red |
| BGV Compliance Below | Numeric threshold input | Percentage value (e.g., 80%) |
| Vacancy Rate Above | Numeric threshold input | Percentage value (e.g., 5%) |
| POCSO Compliance Below | Numeric threshold input | Percentage value (e.g., 100%) |

### 5.2 Search
- Full-text: Branch name
- 300ms debounce

### 5.3 Pagination
- Server-side · 20 rows/page

---

## 6. Drawers

### 6.1 Drawer: `director-branch-detail` — Branch HR Detail
- **Trigger:** Click on branch name or Actions → View
- **Width:** 720px
- Shows: Branch name, Principal, HR contact, full staff breakdown by department, BGV status breakdown, POCSO compliance timeline, last 3 disciplinary cases, open vacancies list, last audit date and findings summary

### 6.2 Drawer: `director-approval` — Pending Approval Review
- **Trigger:** Click on Transfers Pending Approval KPI card or action from notification
- **Width:** 560px
- Fields: Transfer request detail (staff, from-branch, to-branch, reason), requesting manager name, date submitted, impact analysis (will this create a critical vacancy?), Director notes (textarea), Approve / Reject / Request More Info buttons

### 6.3 Drawer: `director-exit-detail` — Exit & Turnover Detail
- **Trigger:** Actions → View Exits on any branch row
- **Width:** 560px
- Shows: Exits in last 12 months for that branch, exit reason breakdown, notice period compliance, full-and-final settlement status

### 6.4 Modal: Approve Transfer
- Confirmation: "You are approving the transfer of [Staff Name] from [Branch A] to [Branch B]. This will create a vacancy at [Branch A]. Confirm?"
- Buttons: Confirm Approval · Cancel

---

## 7. Charts

### 7.1 Staff Strength vs. Sanctioned Posts (Bar Chart)
- **X-axis:** Branch names
- **Series 1:** Sanctioned strength (grouped bar, grey)
- **Series 2:** Actual staff count (grouped bar, blue)
- **Annotation:** Branches where actual < 90% of sanctioned are highlighted in red

### 7.2 Turnover Rate — Last 12 Months (Line Chart)
- **X-axis:** Month labels (rolling 12 months)
- **Y-axis:** Attrition rate %
- **Series:** Group average line + individual branch lines (toggled via legend)
- **Benchmark line:** 10% threshold shown as dashed red line

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Transfer approved | "Transfer approved. [Staff Name] moved to [Branch]." | Success | 4s |
| Transfer rejected | "Transfer request rejected. Requesting manager notified." | Info | 4s |
| Export triggered | "Report is being generated. You will be notified when ready." | Info | 5s |
| Approval error | "Failed to process approval. Please try again." | Error | 6s |
| BGV alert acknowledged | "Alert acknowledged. Action logged against your profile." | Warning | 5s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No branches configured | "No Branches Found" | "No branch data is available yet. Set up your group branches to begin HR oversight." | Configure Branches |
| All health scores Green | "All Branches Healthy" | "Every branch meets HR compliance thresholds. No action required at this time." | View Full Directory |
| No pending approvals | "No Pending Approvals" | "You are up to date. All transfer and escalation requests have been actioned." | — |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Initial page load | Full-page skeleton: KPI bar shimmer + table skeleton (8 rows) |
| Branch detail drawer open | Drawer-scoped spinner centred in panel |
| Approval submission | Button spinner + disabled state on both Approve and Reject buttons |
| Chart data fetch | Chart area shimmer overlay with "Loading data…" label |

---

## 11. Role-Based UI Visibility

| Element | HR Director (G3) | HR Manager (G3) | CEO Read-Only (G3) | Performance Officer (G1) |
|---|---|---|---|---|
| KPI Summary Bar | Visible (all 7 cards) | Visible (all 7 cards) | Visible (summary only) | Hidden |
| Branch HR Health Table | Visible + Actions | Visible (no approval action) | Visible (read-only) | Hidden |
| Approval Drawer | Visible + Actionable | Visible (read-only) | Hidden | Hidden |
| Export PDF Button | Visible | Visible | Visible | Hidden |
| Alert Banners | Visible + dismissible after action | Visible (non-dismissible) | Visible (non-dismissible) | Hidden |
| Charts | Visible | Visible | Visible | Hidden |
| Turnover Detail Drawer | Visible | Visible | Hidden | Hidden |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/hr/director/kpis/` | JWT (G3) | Returns all 7 KPI card values |
| GET | `/api/v1/hr/director/branch-health/` | JWT (G3) | Paginated branch HR health table |
| GET | `/api/v1/hr/director/branch-health/{branch_id}/` | JWT (G3) | Single branch HR detail for drawer |
| GET | `/api/v1/hr/director/pending-approvals/` | JWT (G3) | List of pending transfer approvals |
| POST | `/api/v1/hr/transfers/{id}/approve/` | JWT (G3) | Director approves a transfer request |
| POST | `/api/v1/hr/transfers/{id}/reject/` | JWT (G3) | Director rejects a transfer request |
| GET | `/api/v1/hr/director/charts/strength/` | JWT (G3) | Staff vs. sanctioned bar chart data |
| GET | `/api/v1/hr/director/charts/turnover/` | JWT (G3) | Rolling 12-month turnover line data |
| GET | `/api/v1/hr/director/export/` | JWT (G3) | Triggers async PDF export of full report |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Load KPI bar on page ready | `load` | GET `/api/v1/hr/director/kpis/` | `#kpi-bar` | `innerHTML` |
| Load branch health table | `load` | GET `/api/v1/hr/director/branch-health/` | `#branch-table` | `innerHTML` |
| Open branch detail drawer | `click` on branch name | GET `/api/v1/hr/director/branch-health/{id}/` | `#detail-drawer` | `innerHTML` |
| Paginate branch table | `click` on page button | GET `/api/v1/hr/director/branch-health/?page=N` | `#branch-table` | `innerHTML` |
| Submit approval decision | `click` on Approve/Reject | POST `/api/v1/hr/transfers/{id}/approve/` | `#approval-result` | `innerHTML` |
| Filter by health score | `change` on health filter | GET `/api/v1/hr/director/branch-health/?health=red` | `#branch-table` | `innerHTML` |
| Dismiss alert banner after action | `click` on Dismiss (post-action) | POST `/api/v1/hr/director/alerts/{id}/acknowledge/` | `#alert-banner` | `outerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
