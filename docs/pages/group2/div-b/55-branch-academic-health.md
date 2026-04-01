# 55 — Branch Academic Health Dashboard

> **URL:** `/group/acad/branch-health/`
> **File:** `55-branch-academic-health.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** CAO G4 · Academic Director G3 · Stream Coordinators G3 (own stream view) · Academic MIS Officer G1

---

## 1. Purpose

The Branch Academic Health Dashboard is the group-level early warning system for academic performance at the branch level. Rather than forcing the CAO or Academic Director to examine ten separate reports to assess a branch's academic state, this page computes a single composite health score (0–100) per branch from five weighted components: student attendance, exam result averages, curriculum completion, teacher performance, and dropout rate. Branches are then ranked and flagged in three zones: Healthy (> 70), Warning (50–70), and Critical (< 50).

The health score is not a final judgment — it is an attention-directing tool. A branch with a score of 48 today (Critical) may have dropped from 72 (Healthy) three months ago because of a recent exam result dip or a wave of teacher transfers. The historical trend chart inside the branch health detail drawer tells this story, and the component drill-down explains exactly which of the five dimensions is dragging the score down. This allows the Academic Director to have a specific, evidence-based conversation with the branch principal rather than a vague concern about "performance."

In a large group managing 50 branches simultaneously, the CAO cannot monitor every branch daily. The health score system operates as a triage layer: it surfaces only the branches that need attention, auto-escalates Critical-zone branches to the CAO dashboard (page 01), and allows the Academic Director to drill into any branch for a component-level breakdown in seconds. The weight of each component in the formula is configurable by the CAO to reflect the group's current strategic priorities.

---

## 2. Role Access

| Role | Level | Can View | Can Create/Act | Notes |
|---|---|---|---|---|
| Chief Academic Officer (CAO) | G4 | ✅ Full | ✅ Configure health score formula | Formula configuration |
| Group Academic Director | G3 | ✅ Full | ✅ Add recommended actions | Primary operational owner |
| Group Curriculum Coordinator | G2 | ❌ | ❌ | No access |
| Group Exam Controller | G3 | ❌ | ❌ | No access |
| Group Results Coordinator | G3 | ❌ | ❌ | No access |
| Stream Coord — MPC | G3 | ✅ MPC-stream view only | ❌ | Sees branches filtered to MPC performance data |
| Stream Coord — BiPC | G3 | ✅ BiPC-stream view | ❌ | |
| Stream Coord — MEC/CEC | G3 | ✅ MEC/CEC-stream view | ❌ | |
| Group JEE/NEET Integration Head | G3 | ❌ | ❌ | No access |
| Group IIT Foundation Director | G3 | ❌ | ❌ | No access |
| Group Olympiad & Scholarship Coord | G3 | ❌ | ❌ | No access |
| Group Special Education Coordinator | G3 | ❌ | ❌ | No access |
| Group Academic MIS Officer | G1 | ✅ Full | ❌ No write | Read all data; cannot configure or add actions |
| Group Academic Calendar Manager | G3 | ❌ | ❌ | No access |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Academic  ›  Academic MIS & Analytics  ›  Branch Academic Health
```

### 3.2 Page Header
```
Branch Academic Health Dashboard                             [Configure Formula]  [Export ↓]
Composite health scoring — all branches                                 (CAO, Academic Dir)
```

### 3.3 Summary Stats Bar

| Stat | Value |
|---|---|
| Total Branches | Count |
| Healthy (> 70) | Count — green |
| Warning (50–70) | Count — amber |
| Critical (< 50) | Count — red |
| Group Avg Health Score | Score / 100 |
| Score Formula Last Updated | Date |

---

## 4. Main Content

### 4.1 Search
- Full-text across: Branch name, Branch code
- 300ms debounce · Highlights match in Branch column

### 4.2 Advanced Filters (slide-in drawer, active chips, Clear All)

| Filter | Type | Options |
|---|---|---|
| Zone | Multi-select | All group zones |
| Health Score Band | Select | Critical (< 50) / Warning (50–70) / Healthy (> 70) |
| Trend | Select | Improving / Stable / Declining |
| Attendance below threshold | Checkbox | Attendance < configured warning threshold |
| Result below threshold | Checkbox | Exam avg < configured warning threshold |
| Date range (score computed for) | Date range picker | |

### 4.3 Columns

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Branch | Text + link | ✅ | |
| Health Score | Number + colour badge | ✅ | Colour: green ≥ 70, amber 50–69, red < 50 |
| Attendance % | Progress bar | ✅ | Component 1 |
| Result Avg % | Progress bar | ✅ | Component 2 |
| Curriculum Completion % | Progress bar | ✅ | Component 3 |
| Teacher Rating (avg) | Stars | ✅ | Component 4 |
| Dropout Rate % | Number | ✅ | Component 5 — lower is better |
| Trend | Arrow icon | ✅ | ↑ Improving (green) · → Stable (grey) · ↓ Declining (red) |
| Actions | — | ❌ | |

**Default sort:** Health Score ascending (Critical branches at top).

**Pagination:** Server-side · Default 25/page · Selector 10/25/50/All · Page jump input.

### 4.4 Row Actions

| Action | Visible To | Drawer | Notes |
|---|---|---|---|
| View Detail | All roles | `branch-health-detail` drawer 560px | Score breakdown + trends |
| Add Action Plan | Academic Dir, CAO | Inline within drawer | Recommended corrective actions |
| Export Branch Report | Academic Dir, CAO, MIS | PDF download | Single-branch health report |

---

## 5. Drawers & Modals

### 5.1 Drawer: `branch-health-detail`
- **Trigger:** View Detail row action
- **Width:** 560px
- **Tabs:** Score Breakdown · Historical Trend · Component Drill-downs · Recommended Actions

**Tab: Score Breakdown**
| Component | Weight | Raw Value | Weighted Contribution |
|---|---|---|---|
| Student Attendance | 25% | 82% | 20.5 pts |
| Exam Result Avg | 30% | 68% | 20.4 pts |
| Curriculum Completion | 20% | 91% | 18.2 pts |
| Teacher Rating | 15% | 3.8/5 → 76% | 11.4 pts |
| Dropout Rate (inverted) | 10% | 4% dropout → 96% | 9.6 pts |
| **Total Health Score** | 100% | — | **80.1** |

Note: Formula weights shown as configured by CAO. Actual values from live data.

**Tab: Historical Trend**
Line chart: Health score per month for last 12 months. Horizontal reference lines at 50 (Critical) and 70 (Healthy). Annotations: any significant events added by Academic Dir.

**Tab: Component Drill-downs**
Four sub-sections, expandable:
- Attendance: Trend line (12 months) + comparison to group avg
- Exam Results: Last 3 exam cycle averages by stream
- Curriculum Completion: By stream and class (heat-indicator)
- Teacher Performance: Avg composite score distribution; count on PIP

**Tab: Recommended Actions**
| Column | Notes |
|---|---|
| Action | Recommended corrective action description |
| Owner | Branch principal / CAO / Academic Dir |
| Due Date | |
| Status | Open / In Progress / Done |
| Added By | |

[+ Add Action] button within this tab (Academic Dir, CAO only).

### 5.2 Modal: `configure-formula`
- **Trigger:** [Configure Formula] header button (CAO only)
- **Width:** 420px

| Component | Weight | Min | Max |
|---|---|---|---|
| Student Attendance | Number % | 0 | 100 |
| Exam Result Avg | Number % | 0 | 100 |
| Curriculum Completion | Number % | 0 | 100 |
| Teacher Rating | Number % | 0 | 100 |
| Dropout Rate | Number % | 0 | 100 |

**Validation:** Total of all weights must equal 100% (live counter shown). [Save Formula] · [Reset to Default] · [Cancel]

---

## 6. Charts

### 6.1 Health Score Distribution (All Branches) — Scatter / Bar
- **Type:** Vertical bar chart
- **Data:** Health score per branch — sorted ascending
- **Colour:** Green / Amber / Red by zone
- **Reference lines:** At 50 and 70
- **Tooltip:** Branch · Health Score: X · Zone
- **Export:** PNG

### 6.2 Component Radar (Group Average)
- **Type:** Radar chart
- **Data:** Group average score on each of 5 health components
- **Identifies:** Which component is the group-level weak link
- **Tooltip:** Component · Group Avg: X%
- **Export:** PNG

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Formula saved | "Health score formula updated. Scores recomputed." | Success | 4s |
| Action plan added | "Action plan item added for [Branch]" | Success | 4s |
| Action status updated | "Action status updated" | Success | 4s |
| Export started | "Export preparing… download will start shortly" | Info | 4s |
| Critical branch auto-escalation | "Branch [Name] health score dropped to Critical. CAO notified." | Warning | — (system) |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No branches | "No branches configured" | "Set up branches to begin tracking academic health" | — |
| No Critical branches | "No branches in Critical zone" | "All branches are above the critical threshold. Monitor Warning-zone branches." | — |
| No results match filters | "No branches match" | "Clear filters to see all branches" | [Clear Filters] |
| Actions tab empty | "No actions logged" | "Add corrective action recommendations for this branch" | [+ Add Action] |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: stats bar + table (10 rows) + chart areas |
| Table filter/search/sort/page | Inline skeleton rows |
| Detail drawer open | Spinner → tabs load |
| Historical trend chart | Skeleton line chart |
| Formula modal open | Spinner (brief) |
| Export trigger | Spinner in button |

---

## 10. Role-Based UI Visibility

| Element | CAO G4 | Academic Dir G3 | Stream Coord G3 | MIS G1 |
|---|---|---|---|---|
| Full table | ✅ | ✅ | ✅ (own stream) | ✅ |
| [Configure Formula] | ✅ | ❌ | ❌ | ❌ |
| Add Action Plan | ✅ | ✅ | ❌ | ❌ |
| Export | ✅ | ✅ | ❌ | ✅ |
| Charts | ✅ | ✅ | ✅ | ✅ |
| Historical trend tab | ✅ | ✅ | ✅ | ✅ |
| Component drill-downs | ✅ | ✅ | ✅ (own stream) | ✅ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/acad/branch-health/` | JWT | Branch health list |
| GET | `/api/v1/group/{group_id}/acad/branch-health/stats/` | JWT | Stats bar |
| GET | `/api/v1/group/{group_id}/acad/branch-health/{branch_id}/` | JWT | Branch health detail |
| GET | `/api/v1/group/{group_id}/acad/branch-health/{branch_id}/trend/` | JWT | Historical trend data |
| GET | `/api/v1/group/{group_id}/acad/branch-health/{branch_id}/actions/` | JWT | Action plan list |
| POST | `/api/v1/group/{group_id}/acad/branch-health/{branch_id}/actions/` | JWT (G3 Dir, G4) | Add action |
| PATCH | `/api/v1/group/{group_id}/acad/branch-health/{branch_id}/actions/{id}/` | JWT (G3 Dir, G4) | Update action status |
| GET | `/api/v1/group/{group_id}/acad/branch-health/formula/` | JWT | Current formula weights |
| PUT | `/api/v1/group/{group_id}/acad/branch-health/formula/` | JWT (G4 CAO) | Update formula |
| GET | `/api/v1/group/{group_id}/acad/branch-health/export/?format=pdf` | JWT | Single or all branch report |
| GET | `/api/v1/group/{group_id}/acad/branch-health/charts/score-distribution/` | JWT | Bar chart data |
| GET | `/api/v1/group/{group_id}/acad/branch-health/charts/component-radar/` | JWT | Radar chart data |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Search | `input delay:300ms` | GET `.../branch-health/?q=` | `#health-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../branch-health/?filters=` | `#health-table-section` | `innerHTML` |
| Sort column | `click` | GET `.../branch-health/?sort=&dir=` | `#health-table-section` | `innerHTML` |
| Pagination | `click` | GET `.../branch-health/?page=` | `#health-table-section` | `innerHTML` |
| Detail drawer | `click` | GET `.../branch-health/{bid}/` | `#drawer-body` | `innerHTML` |
| Historical trend tab | `click` | GET `.../branch-health/{bid}/trend/` | `#trend-chart-container` | `innerHTML` |
| Action add submit | `submit` | POST `.../branch-health/{bid}/actions/` | `#actions-list` | `beforeend` |
| Formula save | `submit` | PUT `.../branch-health/formula/` | `#stats-bar` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
