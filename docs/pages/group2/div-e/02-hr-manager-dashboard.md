# 02 — Group HR Manager Dashboard

- **URL:** `/group/hr/manager/`
- **Template:** `portal_base.html`
- **Priority:** P0
- **Role:** Group HR Manager (Role 42, G3)

---

## 1. Purpose

The Group HR Manager Dashboard is the operational hub from which the HR Manager coordinates all hiring, onboarding, and exit activity across every branch in the group. While the HR Director operates at a strategic and approval level, the HR Manager is responsible for executing the day-to-day mechanics: posting job requirements, tracking candidate pipelines, issuing offer letters, ensuring new joiners complete their onboarding checklists, and managing exit formalities for departing staff.

This dashboard condenses what would otherwise be a scattered series of spreadsheets and email threads into a single actionable view. The HR Manager sees at a glance how many positions are open, how many candidates are currently in different pipeline stages, which branches are receiving new joiners this month, and which staff members are exiting. Any gap in this picture — a role that has been open for over 60 days, a new joiner whose document submission is overdue — is surfaced immediately via alerts and colour-coded indicators.

The active recruitment drives table is the core of this page. It allows the HR Manager to monitor every open drive by branch, understand the funnel conversion at each stage, and quickly identify stalled drives that need intervention. Sorting by "Days Open" instantly surfaces the longest-running, most urgent openings. Actions from this table link directly to candidate lists and allow the HR Manager to move a candidate to the next stage or escalate to the HR Director.

Probation management is another critical function. The HR Manager must ensure that staff on probation receive formal confirmation or extension letters before the probation end date. This dashboard surfaces all staff whose probation expires within 30 days as a dedicated KPI, allowing proactive management rather than reactive fire-fighting.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group HR Manager | G3 | Full read + write | Primary role; manages all branches |
| Group HR Director | G3 | Full read + approve | Can view and take approval actions |
| Group Recruiter — Teaching | G0 | No platform access | Operates via external ATS only |
| Group Recruiter — Non-Teaching | G0 | No platform access | Operates via external ATS only |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → HR & Staff → HR Manager Dashboard
```

### 3.2 Page Header
- **Title:** `Group HR Manager Dashboard`
- **Subtitle:** `Recruitment & Onboarding Operations · All Branches · AY [current academic year]`
- **Role Badge:** `Group HR Manager`
- **Right-side controls:** `+ New Job Drive` · `Export Pipeline Report` · `Notification Bell`

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| Any recruitment drive open > 60 days | "Critical: [N] role(s) have been open for more than 60 days. Immediate sourcing action required." | Red |
| Onboarding tasks overdue > 7 days | "[N] new joiner(s) have incomplete onboarding tasks overdue by more than 7 days." | Amber |
| Probation confirmation letter not issued < 7 days to expiry | "[N] probation period(s) expire within 7 days. Issue confirmation or extension letters." | Amber |
| Staff exiting without full-and-final clearance | "[N] exit(s) are past relieving date with pending clearance items." | Red |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Active Job Openings | Total open positions across all drives and branches | Blue (informational) | Opens recruitment drives table |
| Candidates in Pipeline | All candidates at any active stage group-wide | Blue | Links to full candidate list |
| Joining This Month | Staff confirmed and scheduled to join in current calendar month | Green | Opens joining tracker |
| Exiting This Month | Staff on notice period relieving this month | Amber | Opens exit tracker |
| Probation Due (30 Days) | Staff whose probation end date falls within 30 days | Amber if > 0 | Opens probation list drawer |
| Onboarding Overdue | New joiners with incomplete mandatory onboarding tasks past deadline | Red if > 0, Green if 0 | Opens overdue onboarding list |

---

## 5. Main Table — Active Recruitment Drives

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Branch | Text | Yes | Yes (multi-select) |
| Role Title | Text (link to drive detail) | Yes | Yes (text search) |
| Type | Badge (Teaching / Non-Teaching) | Yes | Yes (checkbox) |
| Openings | Integer | Yes | Yes (> N) |
| Applied | Integer | Yes | No |
| Interviewed | Integer | Yes | No |
| Offered | Integer | Yes | No |
| Joined | Integer | Yes | No |
| Status | Badge (Active / Paused / Closed / Filled) | Yes | Yes (status filter) |
| Days Open | Integer (coloured: Green <30, Amber 30–60, Red >60) | Yes | Yes (> N) |
| Actions | Icon buttons (View / Pause / Close) | No | No |

### 5.1 Filters

| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select dropdown | All configured branches |
| Role Type | Checkbox | Teaching / Non-Teaching / Admin |
| Status | Checkbox | Active / Paused / Closed / Filled |
| Days Open | Range slider | 0–180 days |
| Openings Remaining | Numeric | > 0 (default) |

### 5.2 Search
- Full-text: Role title, branch name
- 300ms debounce

### 5.3 Pagination
- Server-side · 20 rows/page

---

## 6. Drawers

### 6.1 Drawer: `drive-create` — Create New Job Drive
- **Trigger:** `+ New Job Drive` button
- **Width:** 560px
- **Fields:**
  - Branch (required, dropdown)
  - Role Title (required, text, max 100 chars)
  - Role Type (required, radio: Teaching / Non-Teaching / Admin)
  - Department (required, dropdown based on branch config)
  - Number of Openings (required, integer, min 1)
  - Job Description (required, rich textarea, max 2000 chars)
  - Minimum Qualification (required, dropdown: Graduate / Post-Graduate / B.Ed / M.Ed / PhD / Other)
  - Experience Required (required, integer in years)
  - Salary Band — Min (₹, required)
  - Salary Band — Max (₹, required; must be ≥ min)
  - Target Joining Date (date picker, required)
  - Assigned Recruiter (dropdown: Group Recruiter Teaching / Non-Teaching)
  - Notes (optional textarea)
- **Validation:** Salary max ≥ salary min; target date must be in future

### 6.2 Drawer: `drive-view` — View Drive Detail
- **Trigger:** Click on role title in table
- **Width:** 720px
- Shows: Full job description, all candidate stages with names and status, timeline since creation, assigned recruiter, interview schedule summary, offer letters issued, joins vs. openings progress bar

### 6.3 Drawer: `drive-edit` — Edit Drive
- **Trigger:** Actions → Edit
- **Width:** 560px
- Same fields as create, pre-populated; Role Type and Branch are locked after first candidate enters pipeline

### 6.4 Modal: Pause / Close Drive
- Confirmation: "You are [pausing / closing] the drive for [Role] at [Branch]. This will [pause sourcing / mark all remaining candidates as Not Proceeding]. Confirm?"
- Buttons: Confirm · Cancel

---

## 7. Charts

### 7.1 Joining & Exiting Trend (Bar Chart)
- **X-axis:** Last 6 calendar months
- **Series 1:** Joinings per month (blue bars)
- **Series 2:** Exits per month (red bars)
- Shows net headcount change pattern across the group

### 7.2 Recruitment Funnel (Funnel Chart)
- Stages: Applied → Screened → Interviewed → Offered → Joined
- Current active drives aggregated into a group-level funnel
- Highlights drop-off stage with the highest attrition

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Job drive created | "New job drive created for [Role] at [Branch]." | Success | 4s |
| Drive updated | "Job drive updated successfully." | Success | 3s |
| Drive paused | "Drive paused. Assigned recruiter has been notified." | Info | 4s |
| Drive closed | "Drive closed. All open candidates marked Not Proceeding." | Warning | 5s |
| Export triggered | "Pipeline report is being prepared. You will be notified when ready." | Info | 5s |
| Validation error | "Please complete all required fields before submitting." | Error | 5s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No active drives | "No Active Recruitment Drives" | "All positions are currently filled. Create a new drive when a vacancy arises." | + New Job Drive |
| No candidates in pipeline | "Pipeline Is Empty" | "No candidates have been added to any active drive. Begin sourcing." | View Drives |
| No joinings this month | "No Joinings This Month" | "No new staff are scheduled to join in the current month." | — |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Initial page load | Full-page skeleton: KPI bar shimmer + table skeleton (10 rows) |
| Drive detail drawer open | Drawer spinner centred; candidate list loads progressively |
| Drive create/edit form submit | Button spinner on Submit; form fields disabled |
| Chart data load | Chart shimmer overlay with "Loading pipeline data…" label |

---

## 11. Role-Based UI Visibility

| Element | HR Manager (G3) | HR Director (G3) | Recruiter Teaching (G0) | Recruiter Non-Teaching (G0) |
|---|---|---|---|---|
| KPI Summary Bar | Visible (all 6 cards) | Visible (all 6 cards) | No access | No access |
| Recruitment Drives Table | Visible + Create/Edit/Pause/Close | Visible (read + approve) | No access | No access |
| + New Job Drive Button | Visible | Hidden | No access | No access |
| Salary Band in Drive Detail | Visible | Visible | No access | No access |
| Export Button | Visible | Visible | No access | No access |
| Charts | Visible | Visible | No access | No access |
| Probation Due KPI Drill-down | Visible + actionable | Visible (read-only) | No access | No access |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/hr/manager/kpis/` | JWT (G3) | Returns all 6 KPI values |
| GET | `/api/v1/hr/recruitment/drives/` | JWT (G3) | Paginated list of all recruitment drives |
| POST | `/api/v1/hr/recruitment/drives/` | JWT (G3) | Create a new recruitment drive |
| GET | `/api/v1/hr/recruitment/drives/{id}/` | JWT (G3) | Drive detail for view/edit drawer |
| PATCH | `/api/v1/hr/recruitment/drives/{id}/` | JWT (G3) | Update drive fields |
| POST | `/api/v1/hr/recruitment/drives/{id}/pause/` | JWT (G3) | Pause a drive |
| POST | `/api/v1/hr/recruitment/drives/{id}/close/` | JWT (G3) | Close a drive |
| GET | `/api/v1/hr/manager/charts/joining-exiting/` | JWT (G3) | Monthly joining/exiting trend data |
| GET | `/api/v1/hr/manager/charts/funnel/` | JWT (G3) | Group-level recruitment funnel data |
| GET | `/api/v1/hr/manager/export/pipeline/` | JWT (G3) | Triggers async pipeline report export |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Load KPI bar on page ready | `load` | GET `/api/v1/hr/manager/kpis/` | `#kpi-bar` | `innerHTML` |
| Load drives table | `load` | GET `/api/v1/hr/recruitment/drives/` | `#drives-table` | `innerHTML` |
| Open drive detail drawer | `click` on role title | GET `/api/v1/hr/recruitment/drives/{id}/` | `#drive-drawer` | `innerHTML` |
| Paginate drives table | `click` on page control | GET `/api/v1/hr/recruitment/drives/?page=N` | `#drives-table` | `innerHTML` |
| Filter by status or type | `change` on filter controls | GET `/api/v1/hr/recruitment/drives/?status=active` | `#drives-table` | `innerHTML` |
| Submit new drive form | `click` on Submit | POST `/api/v1/hr/recruitment/drives/` | `#drives-table` | `innerHTML` |
| Search drives | `input` with 300ms debounce | GET `/api/v1/hr/recruitment/drives/?q=...` | `#drives-table` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
