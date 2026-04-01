# 06 — Group Performance Review Officer Dashboard

- **URL:** `/group/hr/performance/`
- **Template:** `portal_base.html`
- **Priority:** P0
- **Role:** Group Performance Review Officer (Role 46, G1)

---

## 1. Purpose

The Group Performance Review Officer Dashboard provides a read-only, group-wide overview of the annual staff appraisal cycle. Role 46 carries G1 (Group Read Only) access — this officer does not fill in appraisals or make HR decisions, but functions as an independent monitor who ensures that the appraisal process is proceeding on schedule, that rating distributions across branches are statistically reasonable, and that Performance Improvement Plans (PIPs) and promotion recommendations are being handled appropriately.

Rating integrity is a central concern for this role. In school groups, appraisal inflation — where local branch principals award uniformly high ratings to avoid conflict — is a chronic problem that distorts pay revision decisions and hides genuine underperformance. The Performance Review Officer uses this dashboard to spot branches where the distribution of ratings is unusually skewed (e.g., >80% "Excellent" ratings) and flags these to the Group HR Director for calibration review. The dashboard's rating distribution chart makes this analysis immediate and visual.

The appraisal completion tracking table shows the HR Manager and Director which branches are falling behind the mandated submission deadline. Submissions are tracked at the individual staff level, so the officer can see exactly how many teachers at each branch have not yet had their appraisals submitted by their branch principal. Branches below 50% submission with less than 14 days remaining in the appraisal window receive an amber flag; those below 30% receive a red flag.

PIP tracking is another critical function. Staff placed on Performance Improvement Plans represent both a management priority and a legal sensitivity — the PIP documentation must be complete before any disciplinary or termination action can be taken. This dashboard shows all active PIPs across the group, their target review dates, and their current status. The Performance Review Officer ensures that PIP timelines are being followed and escalates overdue PIPs to the HR Director.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Performance Review Officer | G1 | Full read, no write | Primary role; read-only access |
| Group HR Director | G3 | Full read + action | Can use this view and take action |
| Group HR Manager | G3 | Full read | Operational oversight |
| Branch Principal | Branch-level | No access to this group-level view | Branch principals access their own branch appraisal UI |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → HR & Staff → Performance Review
```

### 3.2 Page Header
- **Title:** `Group Performance Review Dashboard`
- **Subtitle:** `Appraisal Cycle AY [current academic year] · [N] Branches · [N] Staff to Review`
- **Role Badge:** `Group Performance Review Officer`
- **Right-side controls:** `Export Appraisal Report (read-only)` · `Appraisal Calendar`

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| Branch appraisal submission < 30% with ≤ 14 days to deadline | "Critical: [Branch] is at [X]% appraisal submission with [N] days remaining." | Red |
| Rating inflation detected (>80% Excellent in a branch) | "Possible rating inflation at [Branch]: [X]% of ratings are Excellent. Review recommended." | Amber |
| PIP review date overdue | "[N] PIP(s) have passed their review date without a formal update. Escalation required." | Red |
| Appraisal cycle deadline approaching (7 days) | "Appraisal submission deadline is in 7 days. [N] staff reviews are still pending group-wide." | Amber |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Appraisals Submitted | Count of completed appraisal submissions group-wide | Blue | Branch breakdown table |
| Appraisals Pending | Count of staff not yet appraised | Red if > 20% of total, Amber 10–20% | Pending list |
| Appraisal Cycle Completion % | Submitted ÷ Total staff to review | Green ≥ 90%, Amber 60–90%, Red < 60% | Branch breakdown |
| PIPs Active | Staff currently on active Performance Improvement Plans | Red if > 0, with count | PIP detail view |
| Promotions Recommended | Staff recommended for promotion in current appraisal cycle | Blue | Promotion list |
| Rating: Below Average / Poor | Count of staff rated below average or poor | Amber if > 5% of submitted | Rating distribution |

---

## 5. Main Table — Branch Appraisal Status

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Branch Name | Text | Yes | Yes (multi-select) |
| Total Staff to Review | Integer | Yes | No |
| Submitted | Integer | Yes | No |
| Pending | Integer | Yes | Yes (> N) |
| Completion % | Percentage bar (Green ≥ 80%, Amber 50–80%, Red < 50%) | Yes | Yes (< threshold) |
| Avg Rating | Score (1.0–5.0) | Yes | Yes (< / >) |
| % Excellent | Percentage (amber if > 80%) | Yes | Yes (> threshold) |
| PIP Count | Integer | Yes | Yes (> 0) |
| Promotions Recommended | Integer | Yes | No |
| Status | Badge (On Track / At Risk / Overdue) | Yes | Yes |

### 5.1 Filters

| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select dropdown | All configured branches |
| Completion Status | Checkbox | On Track / At Risk / Overdue |
| Completion % Below | Threshold input | Percentage value |
| Has Active PIPs | Toggle | Yes / No |
| Avg Rating Below | Numeric input | Score 1.0–5.0 |

### 5.2 Search
- Full-text: Branch name
- 300ms debounce

### 5.3 Pagination
- Server-side · 20 rows/page

---

## 6. Drawers

### 6.1 Drawer: `appraisal-branch-detail` — Branch Appraisal Detail (Read-Only)
- **Trigger:** Click on branch name in table
- **Width:** 720px
- Shows: Full appraisal submission list for the branch (staff name, role, submission date, rating, PIP status, promotion flag), rating distribution within the branch, appraisal submission timeline, pending staff names

### 6.2 Drawer: `pip-detail` — PIP Detail View (Read-Only)
- **Trigger:** Click on PIP Count > 0 or from PIP Active KPI drill-down
- **Width:** 560px
- Shows: Staff name, branch, current rating, PIP objectives set, start date, review date, review date status (upcoming / overdue), PIP notes, outcome (if resolved)

### 6.3 Drawer: `promotion-list` — Promotion Recommendations (Read-Only)
- **Trigger:** Click on Promotions Recommended KPI card
- **Width:** 560px
- Shows: Staff name, branch, current role, recommended new role, recommending principal, current rating, years in current role, HR Director approval status

### 6.4 Modal: (None — G1 read-only; no write actions available)
- No create, edit, or delete modals on this dashboard
- All action buttons are hidden for G1 role

---

## 7. Charts

### 7.1 Rating Distribution Across Group (Pie / Donut Chart)
- Segments: Excellent / Good / Average / Below Average / Poor
- Shows aggregate rating breakdown across all submitted appraisals group-wide
- Hover tooltip: count and percentage per segment

### 7.2 Appraisal Submission Progress by Branch (Horizontal Progress Bars)
- Each bar represents one branch
- Bar fill = completion %; colour-coded Green/Amber/Red
- Sorted by completion % ascending (lowest at top for quick identification)
- Rendered as an inline chart within the page's right panel

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Export triggered | "Appraisal report is being generated. You will be notified when ready." | Info | 5s |
| Filter applied | — (silent table reload) | — | — |
| Drawer opened | — (silent) | — | — |
| Session expired | "Your session has expired. Please log in again." | Error | 8s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| Appraisal cycle not started | "Appraisal Cycle Not Yet Open" | "The appraisal cycle for this academic year has not been initiated by the HR Manager." | — |
| All appraisals submitted | "Appraisal Cycle Complete" | "All staff appraisals have been submitted. Proceed to review and calibration." | View Summary Report |
| No PIPs active | "No Active PIPs" | "No staff are currently on Performance Improvement Plans." | — |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Initial page load | Full skeleton: 6 KPI shimmer + table skeleton (10 rows) + chart shimmer |
| Branch detail drawer open | Drawer spinner; staff list loads progressively |
| PIP detail drawer open | Drawer spinner centred |
| Chart re-render on filter | Chart overlay shimmer with "Updating…" label |

---

## 11. Role-Based UI Visibility

| Element | Performance Officer (G1) | HR Director (G3) | HR Manager (G3) | Branch Principal |
|---|---|---|---|---|
| KPI Summary Bar | Visible (read-only, all 6) | Visible (all 6, actionable) | Visible (all 6, actionable) | No access |
| Branch Appraisal Table | Visible (read-only) | Visible + action buttons | Visible + action buttons | No access |
| All drawers | Visible (read-only mode) | Visible + editable | Visible + editable | No access |
| Export Button | Visible (read-only export) | Visible | Visible | No access |
| Alert Banners | Visible (informational only) | Visible + dismissible | Visible + dismissible | No access |
| Rating Inflation Flags | Visible | Visible + can trigger review | Visible + can trigger review | No access |
| PIP Detail Drawer | Visible (no edit) | Visible + editable | Visible + editable | No access |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/hr/performance/kpis/` | JWT (G1+) | All 6 KPI values |
| GET | `/api/v1/hr/performance/branch-status/` | JWT (G1+) | Paginated branch appraisal status table |
| GET | `/api/v1/hr/performance/branch-status/{branch_id}/` | JWT (G1+) | Branch appraisal detail for drawer |
| GET | `/api/v1/hr/performance/pips/` | JWT (G1+) | All active PIPs group-wide |
| GET | `/api/v1/hr/performance/pips/{id}/` | JWT (G1+) | Single PIP detail |
| GET | `/api/v1/hr/performance/promotions/` | JWT (G1+) | Promotion recommendations list |
| GET | `/api/v1/hr/performance/charts/rating-distribution/` | JWT (G1+) | Rating distribution pie chart data |
| GET | `/api/v1/hr/performance/charts/submission-progress/` | JWT (G1+) | Branch submission progress bar data |
| GET | `/api/v1/hr/performance/export/` | JWT (G1+) | Async appraisal summary report export |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Load KPI bar | `load` | GET `/api/v1/hr/performance/kpis/` | `#kpi-bar` | `innerHTML` |
| Load branch status table | `load` | GET `/api/v1/hr/performance/branch-status/` | `#branch-table` | `innerHTML` |
| Open branch detail drawer | `click` on branch name | GET `/api/v1/hr/performance/branch-status/{id}/` | `#detail-drawer` | `innerHTML` |
| Open PIP list drawer | `click` on PIP KPI card | GET `/api/v1/hr/performance/pips/` | `#pip-drawer` | `innerHTML` |
| Filter by completion status | `change` on status filter | GET `/api/v1/hr/performance/branch-status/?status=...` | `#branch-table` | `innerHTML` |
| Paginate table | `click` on page controls | GET `/api/v1/hr/performance/branch-status/?page=N` | `#branch-table` | `innerHTML` |
| Load submission progress chart | `load` | GET `/api/v1/hr/performance/charts/submission-progress/` | `#progress-chart` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
