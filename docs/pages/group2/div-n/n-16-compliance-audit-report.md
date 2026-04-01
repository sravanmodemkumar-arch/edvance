# [16] — Compliance Audit Report

> **URL:** `/group/legal/audit-report/`
> **File:** `n-16-compliance-audit-report.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Role:** Group Compliance Manager (Role 109, G1) — annual/quarterly audit scores, dimension breakdown, trend analysis, action plans

---

## 1. Purpose

The Compliance Audit Report provides a structured, periodic audit view of the Institution Group's compliance posture across all dimensions and all branches. It synthesises data from all other Division N pages into a single executive-level report: which branches are fully compliant, which have gaps, what the trend has been over the last 4 audit cycles, and what action plans are in place for non-compliant items.

The audit dimensions covered are: Affiliation Compliance, RTI Compliance, POCSO Compliance, Data Privacy (DPDP), Staff Contracts, Regulatory Filings, Insurance Coverage, Statutory Returns, Inspection Records, and Policy Acknowledgements. Each dimension is scored 0–100 based on objective data (e.g., percentage of filings submitted on time, percentage of staff with valid contracts, percentage of consent records active). The overall branch compliance score is a weighted average.

The Compliance Manager generates this report at the end of each quarter for internal governance and annually for board presentation. The Chairman/CEO uses this report to hold branch principals accountable for compliance gaps. External auditors and CBSE inspectors may request this report as evidence of systematic compliance management.

Scale: 5–50 branches · 10 audit dimensions · Quarterly and annual audit cycles · Score history over 4 cycles

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Legal Officer | 108 | G0 | No Platform Access | Reviews audit findings externally |
| Group Compliance Manager | 109 | G1 | Full Read — All Data + Generate Report | Primary user |
| Group RTI Officer | 110 | G1 | Read — RTI dimension only | |
| Group Regulatory Affairs Officer | 111 | G0 | No Platform Access | Not relevant |
| Group POCSO Reporting Officer | 112 | G1 | Read — POCSO dimension only | |
| Group Data Privacy Officer | 113 | G1 | Read — DPDP dimension only | |
| Group Contract Administrator | 127 | G3 | Read — Contracts dimension only | |
| Group Legal Dispute Coordinator | 128 | G1 | No Access | Not relevant to audit scoring |
| Group Insurance Coordinator | 129 | G1 | Read — Insurance dimension only | |

> **Access enforcement:** `@require_role(roles=[109,110,112,113,127,129], min_level=G1)` with dimension-scoping. G4/G5 full access.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Legal & Compliance  ›  Compliance Audit Report
```

### 3.2 Page Header
```
Compliance Audit Report                         [Generate Quarterly Report]  [Export PDF]
Group Compliance Manager — [Name]
[Group Name] · Audit Cycle: [Q1/Q2/Q3/Q4 FY year] · Overall Score: [X]%
```

### 3.3 Alert Banner (conditional)

| Condition | Banner Text | Severity |
|---|---|---|
| Any branch scores < 60% overall | "[N] branch(es) scored below 60% — critical compliance risk. Immediate corrective action required." | Critical (red) |
| Score declined more than 10% from last cycle | "Overall compliance score dropped [X]% from last audit cycle. Review deteriorating dimensions." | High (amber) |
| Action plans overdue (no update in 30 days) | "[N] action plan item(s) have not been updated in 30 days." | Medium (yellow) |

---

## 4. KPI Summary Bar (6 cards)

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Group Score (This Cycle) | % | Weighted avg of all dimensions all branches | Green ≥ 80%, Amber 60–79%, Red < 60% | `#kpi-group-score` |
| 2 | Score Change from Last Cycle | ±% | This cycle score − last cycle score | Green if ≥ 0, Red if < 0 | `#kpi-score-change` |
| 3 | Branches Score ≥ 80% | Count | COUNT WHERE score ≥ 80 | Green if = total | `#kpi-above-80` |
| 4 | Branches Score < 60% | Count | COUNT WHERE score < 60 | Red > 0, Green = 0 | `#kpi-below-60` |
| 5 | Open Action Plans | Count | COUNT action_plan_items WHERE status != 'closed' | Amber > 10, Green ≤ 10 | `#kpi-action-plans` |
| 6 | Dimensions Fully Compliant | Count (of 10) | COUNT dimensions WHERE group_avg ≥ 90% | Green if = 10, Amber 7–9, Red < 7 | `#kpi-dims-compliant` |

**HTMX:** `hx-get="/api/v1/group/{id}/legal/audit/kpis/"` with `hx-trigger="load"`.

---

## 5. Sections

### 5.1 Branch Compliance Scores Table

**Search:** Branch name. Debounced 350ms.

**Filters:**
- Score Range: `All` · `≥ 80% (Good)` · `60–79% (Needs Attention)` · `< 60% (Critical)`
- Audit Cycle: dropdown of last 4 cycles
- Dimension Filter: selects which dimension to sort/highlight

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Branch | Text | Yes | |
| Affiliation | Score (0–100) | Yes | Colour-coded |
| RTI | Score | Yes | |
| POCSO | Score | Yes | |
| Data Privacy | Score | Yes | |
| Staff Contracts | Score | Yes | |
| Regulatory Filings | Score | Yes | |
| Insurance | Score | Yes | |
| Statutory Returns | Score | Yes | |
| Inspections | Score | Yes | |
| Policy Ack | Score | Yes | |
| Overall Score | Score + bar | Yes | Weighted average |
| vs Last Cycle | ±% | Yes | Change indicator |
| Actions | Button | No | [View Detail] |

**Default sort:** Overall Score ASC (worst first)
**Pagination:** Server-side · Default 25/page

---

### 5.2 Dimension-wise Summary

Summary row showing group-average score per dimension — highlights weakest dimensions.

| Dimension | Group Average | Min (Worst Branch) | Max (Best Branch) | Trend (vs last cycle) |
|---|---|---|---|---|
| Affiliation Compliance | [X]% | [X]% | [X]% | ↑/↓/→ |
| RTI Compliance | | | | |
| ... (all 10 dimensions) | | | | |

---

## 6. Drawers & Modals

### 6.1 Drawer: `branch-audit-detail` (760px)
- **Tabs:** Score Breakdown · Action Plans · History · Notes
- **Score Breakdown tab:** Bar chart of all 10 dimension scores for this branch + comparison to group average. For each dimension: score, max possible, key issues (auto-populated from N-01 to N-19 data).
- **Action Plans tab:** All open action items for this branch — dimension, issue description, assigned to, deadline, status (Open/In Progress/Closed). [+ Add Action Item] (Role 109 only).
- **History tab:** Score for each dimension across last 4 audit cycles — table + sparkline.
- **Notes tab:** Internal compliance notes for this branch.

### 6.2 Modal: `generate-audit-report` (560px)
| Field | Type | Required |
|---|---|---|
| Audit Period | Select (Q1/Q2/Q3/Q4 + FY) | Yes |
| Branches to Include | Multi-select | Yes (default all) |
| Dimensions to Include | Multi-checkbox | Yes (default all 10) |
| Report Format | Select (PDF / Excel) | Yes |
| Include Action Plans | Toggle | No |
| Include Charts | Toggle | No |

**Footer:** Cancel · Generate Report (async; toast when ready)

### 6.3 Modal: `add-action-item` (560px)
| Field | Type | Required |
|---|---|---|
| Branch | Display | — |
| Dimension | Select | Yes |
| Issue Description | Textarea | Yes |
| Corrective Action | Textarea | Yes |
| Assigned To | Text | Yes |
| Deadline | Date | Yes |

---

## 7. Charts

### 7.1 Group Score Trend (Line Chart)

| Property | Value |
|---|---|
| Chart type | Line (Chart.js 4.x) |
| Title | "Group Compliance Score — Last 4 Audit Cycles" |
| Data | Overall group score per cycle (per dimension as separate lines) |
| X-axis | Audit cycle (Q1 FY24 → current) |
| Y-axis | Score (0–100) |
| Colour | Each dimension a distinct colour; bold line for Overall |
| Tooltip | "[Cycle]: Overall [X]%, [Dimension] [X]%" |
| API endpoint | `GET /api/v1/group/{id}/legal/audit/score-trend/` |
| HTMX | `hx-get` on load → `hx-target="#chart-score-trend"` → `hx-swap="innerHTML"` |
| Export | PNG |

### 7.2 Dimension Performance — Radar Chart

| Property | Value |
|---|---|
| Chart type | Radar (Chart.js 4.x) |
| Title | "Group Compliance by Dimension — Current Cycle" |
| Data | Group average score per dimension (10 dimensions = 10 axes) |
| Colour | Fill: `rgba(59,130,246,0.3)`, Border: `#3B82F6` |
| Tooltip | "[Dimension]: [X]% this cycle" |
| API endpoint | `GET /api/v1/group/{id}/legal/audit/dimension-radar/` |
| HTMX | `hx-get` on load → `hx-target="#chart-dimension-radar"` → `hx-swap="innerHTML"` |
| Export | PNG |

### 7.3 Branch Score Distribution (Histogram)

| Property | Value |
|---|---|
| Chart type | Vertical bar / histogram (Chart.js 4.x) |
| Title | "Branch Score Distribution — Current Cycle" |
| Data | Count of branches per score band: 0–59, 60–69, 70–79, 80–89, 90–100 |
| X-axis | Score band |
| Y-axis | Number of branches |
| Colour | Red (0–59), Amber (60–79), Green (80–100) |
| Tooltip | "[Band]: [N] branches" |
| API endpoint | `GET /api/v1/group/{id}/legal/audit/score-distribution/` |
| HTMX | `hx-get` on load → `hx-target="#chart-score-dist"` → `hx-swap="innerHTML"` |
| Export | PNG |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Report generation started | "Generating compliance audit report for [period]…" | Info | 3s |
| Report ready | "Audit report ready. Click to download." | Success | 6s |
| Action item added | "Action item added for [Branch] — [Dimension]." | Success | 3s |
| Action item closed | "Action plan item marked as Closed." | Success | 3s |
| Score deterioration alert | "Compliance score for [Branch] dropped [X]% this cycle." | Warning | 6s |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| No audit data | `bar-chart` | "No Audit Data Yet" | "Compliance audit scores will appear after the first data cycle." | — |
| No action plans | `check-circle` | "No Open Action Plans" | "All action plan items are closed or none have been created." | — |
| Filter returns no results | `search` | "No Matching Branches" | | Clear Filters |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | Skeleton: 6 KPI + table + 3 chart placeholders |
| Report generation | Progress modal |
| Charts | Grey canvas + spinner |
| Drawer open | Right-slide skeleton |
| Branch action plans tab | Shimmer list |

---

## 11. Role-Based UI Visibility

| Element | Compliance Mgr (109) | DPO (113) | POCSO Officer (112) | CEO/Chairman |
|---|---|---|---|---|
| Full branch score table | Visible | DPDP column only | POCSO column only | Full |
| Dimension summary | Full | Own dimension | Own dimension | Full |
| [Generate Report] | Visible | Not visible | Not visible | Visible |
| [Add Action Item] | Visible | Not visible | Not visible | Visible |
| All 3 charts | Visible | DPDP-scoped | POCSO-scoped | Visible |
| Export | Visible | Not visible | Not visible | Visible |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/legal/audit/scores/` | G1+ (scoped) | Branch compliance scores |
| GET | `/api/v1/group/{id}/legal/audit/kpis/` | G1+ | KPI values |
| GET | `/api/v1/group/{id}/legal/audit/score-trend/` | G1+ | Trend line chart data |
| GET | `/api/v1/group/{id}/legal/audit/dimension-radar/` | G1+ | Radar chart data |
| GET | `/api/v1/group/{id}/legal/audit/score-distribution/` | G1+ | Histogram data |
| GET | `/api/v1/group/{id}/legal/audit/{branch_id}/action-plans/` | Role 109, G4+ | Branch action plans |
| POST | `/api/v1/group/{id}/legal/audit/{branch_id}/action-plans/` | Role 109, G4+ | Add action item |
| PATCH | `/api/v1/group/{id}/legal/audit/{branch_id}/action-plans/{item_id}/` | Role 109, G4+ | Update action item |
| POST | `/api/v1/group/{id}/legal/audit/generate/` | Role 109, G4+ | Generate report (async) |

---

## 13. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load | KPI container | GET `.../audit/kpis/` | `#kpi-bar` | `innerHTML` | `hx-trigger="load"` |
| Scores table load | Table body | GET `.../audit/scores/` | `#audit-table-body` | `innerHTML` | `hx-trigger="load"` |
| Filter | Filter chips | GET with `?score_range=` | `#audit-table-body` | `innerHTML` | `hx-trigger="click"` |
| Open branch drawer | [View Detail] | GET `.../audit/{branch_id}/` | `#right-drawer` | `innerHTML` | |
| Generate report modal | [Generate] button | GET `/htmx/legal/audit/generate-form/` | `#modal-container` | `innerHTML` | |
| All 3 charts | Chart containers | GET chart endpoints | `#{chart-id}` | `innerHTML` | `hx-trigger="load"` |

---

*Page spec version: 1.0 · Last updated: 2026-03-22*
