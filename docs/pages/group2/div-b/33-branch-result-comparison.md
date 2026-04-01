# 33 — Branch Result Comparison

> **URL:** `/group/acad/branch-results/`
> **File:** `33-branch-result-comparison.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** CAO G4 · Academic Director G3 · Results Coordinator G3 · Stream Coordinators G3 · Academic MIS Officer G1

---

## 1. Purpose

Branch Result Comparison enables side-by-side academic performance analysis of up to five branches on a single exam. For a group where some branches consistently outperform others, this page surfaces those differences systematically and gives Academic Directors and CAOs the data needed to understand why. Is it the teaching quality? The student intake profile? Curriculum adherence? The comparison page does not answer those questions directly, but it makes the performance gap undeniable and quantifies it precisely.

The kernel density scatter overlay is the most analytically powerful feature on this page. Rather than just comparing averages, it shows the full score distribution shape for each branch — revealing whether a branch's lower average is because its weakest students are performing poorly (left tail problem) or because its high achievers are not reaching their potential (right tail problem). These two scenarios require completely different interventions, and this chart distinguishes them at a glance.

The export function produces a PDF comparison report formatted for presentation to a board of trustees or principals' meeting. It includes the comparison table, all charts, and an auto-generated summary paragraph highlighting the key performance differential between branches. This report format is designed for executive audiences who are not expected to interact with the portal itself.

---

## 2. Role Access

| Role | Level | Can View | Can Act | Notes |
|---|---|---|---|---|
| Chief Academic Officer (CAO) | G4 | ✅ All branches, all streams | ✅ Full — all features + export | Cross-stream comparison |
| Group Academic Director | G3 | ✅ All branches, all streams | ✅ Export · Full comparison | Full access |
| Group Curriculum Coordinator | G2 | ❌ | ❌ | No access |
| Group Exam Controller | G3 | ✅ All branches | ✅ View · Export | Read-only comparison |
| Group Results Coordinator | G3 | ✅ All branches, all streams | ✅ Full — all features + export | Primary user |
| Group Stream Coord — MPC | G3 | ✅ MPC stream, all branches | ✅ Export (MPC) | Filtered to MPC exams |
| Group Stream Coord — BiPC | G3 | ✅ BiPC stream, all branches | ✅ Export (BiPC) | Filtered to BiPC exams |
| Group Stream Coord — MEC/CEC | G3 | ✅ MEC/CEC stream, all branches | ✅ Export (MEC/CEC) | Filtered to MEC/CEC exams |
| Group JEE/NEET Integration Head | G3 | ✅ JEE/NEET exams, all branches | ✅ Export | JEE/NEET filtered |
| Group IIT Foundation Director | G3 | ✅ Foundation exams, all branches | ✅ Export | Foundation filtered |
| Group Olympiad & Scholarship Coord | G3 | ❌ | ❌ | No access |
| Group Special Education Coordinator | G3 | ❌ | ❌ | No access |
| Group Academic MIS Officer | G1 | ✅ All branches, all streams | ✅ Export only | Full read access |
| Group Academic Calendar Manager | G3 | ❌ | ❌ | No access |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Academic  ›  Branch Result Comparison
```

### 3.2 Page Header
```
Branch Result Comparison                            [Export PDF Report ↓]
[Group Name] — Compare up to 5 branches side-by-side
```

### 3.3 Configuration Panel (above comparison — always visible)

```
┌────────────────────────────────────────────────────────────────────────────┐
│  Exam:   [Select Exam ▾]    Stream: [Select ▾]    Class: [Select ▾]       │
│                                                                             │
│  Branches:                                                                  │
│  [Branch 1 ▾]  [Branch 2 ▾]  [Branch 3 ▾]  [+ Add Branch]  [Clear All]   │
│  (up to 5 branches — minimum 2 to enable comparison)                       │
│                                                                             │
│  Subject filter (optional):  [All Subjects ▾]                             │
│                                                                             │
│  [Load Comparison]  ← primary button                                       │
└────────────────────────────────────────────────────────────────────────────┘
```

Branch selector: Multi-tag input — type to search branch name, select up to 5. Each selected branch gets a unique colour chip (used across all charts to maintain colour consistency). Remove branch by clicking × on chip.

"Load Comparison" triggers full data load for all selected branches.

---

## 4. Main Content

### 4.1 Comparison Metric Table

Displayed immediately after configuration panel on load.

| Metric | Branch 1 | Branch 2 | Branch 3 | Branch 4 | Branch 5 |
|---|---|---|---|---|---|
| Branch Name | [Name] | [Name] | [Name] | [Name] | [Name] |
| Students Appeared | N | N | N | N | N |
| Average Score | X% | X% | X% | X% | X% |
| Median Score | X% | X% | X% | X% | X% |
| Highest Score | X / Max | X / Max | X / Max | X / Max | X / Max |
| Lowest Score | X / Max | X / Max | X / Max | X / Max | X / Max |
| Pass % | X% | X% | X% | X% | X% |
| Distinction % (≥ 75%) | X% | X% | X% | X% | X% |
| Top 10% Count | N | N | N | N | N |
| Fail Count | N | N | N | N | N |
| Absent Students | N | N | N | N | N |
| Attendance on Exam Day | X% | X% | X% | X% | X% |
| Standard Deviation | X | X | X | X | X |

**Colour coding in cells:** Each metric's best-performing branch cell highlighted in a light green tint; worst-performing in a light red tint. Visual quick-scan of winner/loser per metric.

**Sortable columns:** Click any metric row label to re-sort branches by that metric (best first).

### 4.2 Per-Subject Comparison Table

Shown below overall metrics. One row per subject covered in the exam.

| Subject | Branch 1 Avg % | Branch 2 Avg % | Branch 3 Avg % | Branch 4 Avg % | Branch 5 Avg % | Group Avg % |
|---|---|---|---|---|---|---|
| Physics | 72% | 65% | 81% | 58% | 74% | 70% |
| Chemistry | 68% | 71% | 75% | 64% | 79% | 71% |
| Mathematics | 61% | 55% | 69% | 52% | 63% | 60% |

Same colour coding: best cell green tint, worst cell red tint, per row.

"Group Avg %" column always pinned at the right — provides reference point for every branch.

### 4.3 Search / Filters / Table Controls

No paginated table — comparison is always a fixed panel view. Filtering changes the configuration panel and triggers "Load Comparison" reload.

### 4.4 Row Actions

Not applicable — this is a comparison panel view, not a row-based table.

### 4.5 Bulk Actions

Not applicable.

---

## 5. Drawers & Modals

### 5.1 Drawer: `branch-comparison-detail`
- **Trigger:** Click on any branch name in the comparison table (header row)
- **Width:** 560px
- **Title:** "[Branch Name] — Exam Detail — [Exam Name]"
- **Tabs:** Overview · Subject Detail · Student Distribution

#### Tab: Overview
Summary of this single branch's performance in the selected exam — same metrics as comparison table rows but formatted as a single-branch profile card.

#### Tab: Subject Detail
Table: Subject · Avg marks · Max marks · Avg % · Pass % · Top scorer (masked name, score) · Questions from branch paper.

#### Tab: Student Distribution
Histogram of student score distribution for this branch:
- X-axis: Score bands (0–10%, 10–20%, ..., 90–100%)
- Y-axis: Student count
- Colour: Red (0–50%) · Amber (50–70%) · Green (70%+)

---

## 6. Charts

### 6.1 Per-Subject Grouped Bar Chart
- **Type:** Vertical grouped bar chart
- **X-axis:** Subjects (Physics · Chemistry · Maths / Biology etc.)
- **Y-axis:** Average marks %
- **Bar groups:** One bar per selected branch per subject (up to 5 bars per group) + one reference bar for Group Average (grey)
- **Branch colours:** Each branch assigned a unique colour from Chart.js colorblind-safe palette — Blue · Orange · Teal · Purple · Dark Green (max 5 branches)
- **Reference bar:** Grey (Group Average) — always shown
- **Tooltip:** Subject · Branch Name · Avg % · vs Group Avg: +N% or −N%
- **Legend:** Bottom, horizontal — branch name + colour swatch
- **Export:** PNG
- **Y-axis:** 0–100%

### 6.2 Score Distribution Kernel Density Overlay (Line)
- **Type:** Line chart (smooth curve — kernel density estimate)
- **X-axis:** Score percentage (0%–100%)
- **Y-axis:** Relative density (normalised to allow fair cross-branch comparison even with different student counts)
- **Lines:** One per selected branch (using same branch colours as bar chart above) + one grey line for Group Average distribution
- **Line style:** Solid lines with low-opacity fill under each curve
- **Tooltip:** Score % · Branch Name · Relative frequency
- **Legend:** Branch names + colours
- **Key insight text:** Auto-generated below chart: "Branch A's distribution is left-skewed — more students scoring below average. Branch C's distribution is right-skewed — strong high-achiever cohort." (Generated from statistical skew values.)
- **Export:** PNG
- **Colorblind accessibility:** Each branch line also has a distinct dash pattern (solid · dashed · dotted · dash-dot · long-dash) in addition to colour differentiation

### 6.3 Radar Chart — Multi-Subject Balance (per branch)
- **Type:** Radar chart
- **Axes:** One axis per subject (up to 6 subjects)
- **Data:** Average % per subject for each selected branch
- **Lines:** One radar polygon per branch, same colour coding
- **Fill:** Low-opacity fill per polygon
- **Tooltip:** Subject · Branch · Avg %
- **Purpose:** Shows which branches are well-balanced across subjects vs those with strong peaks and weak valleys
- **Export:** PNG

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Comparison loaded | "Comparison loaded for [N] branches — [Exam Name]." | Info | 3s |
| PDF export started | "Comparison report PDF preparing — download will begin shortly." | Info | 4s |
| Fewer than 2 branches | "Please select at least 2 branches to compare." | Error | Manual |
| More than 5 branches | "Maximum 5 branches can be compared at once. Remove a branch to add another." | Error | Manual |
| No data for selected combination | "No result data available for this exam/stream/class combination." | Warning | Manual |
| Branch has no results | "[Branch Name] has no uploaded marks for this exam and will be excluded." | Warning | 6s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No configuration set | "Configure Your Comparison" | "Select an exam and at least 2 branches above, then click Load Comparison" | — |
| Only one branch selected | "Select at Least 2 Branches" | "Add another branch to the comparison to see side-by-side data" | [+ Add Branch] |
| No data for selection | "No Data Available" | "No moderated results exist for this exam and class combination" | — |
| All selected branches missing data | "No Branches Have Results" | "None of the selected branches have uploaded marks for this exam" | — |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Filter configuration panel only — no skeleton (comparison loads on demand) |
| "Load Comparison" click | Full comparison area overlay spinner with "Loading comparison data…" |
| Branch comparison detail drawer | Spinner in drawer body + skeleton tabs |
| Chart load (async from comparison data) | Spinner centred in each chart card |
| PDF export | Spinner in export button + "Generating report…" tooltip |

---

## 10. Role-Based UI Visibility

| Element | CAO G4 | Academic Dir G3 | Results Coord G3 | Stream Coords G3 | MIS G1 |
|---|---|---|---|---|---|
| Exam selector options | All exams | All exams | All exams | Own stream exams only | All exams |
| Branch selector | All 50 branches | All 50 branches | All 50 branches | All 50 branches | All 50 branches |
| Export PDF Report | ✅ | ✅ | ✅ | ✅ (own stream) | ✅ |
| Branch detail drawer | ✅ | ✅ | ✅ | ✅ (own stream) | ✅ |
| Score distribution chart | ✅ | ✅ | ✅ | ✅ | ✅ |
| Radar chart | ✅ | ✅ | ✅ | ✅ | ✅ |
| Auto-generated summary text | ✅ | ✅ | ✅ | ✅ | ✅ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/acad/branch-results/exams/` | JWT | Exam list for selector |
| GET | `/api/v1/group/{group_id}/acad/branch-results/compare/` | JWT | Comparison data — query params: exam_id, stream, class, branch_ids (comma-sep, max 5) |
| GET | `/api/v1/group/{group_id}/acad/branch-results/compare/subjects/` | JWT | Per-subject comparison table data |
| GET | `/api/v1/group/{group_id}/acad/branch-results/branch/{branch_id}/detail/` | JWT | Branch comparison detail drawer |
| GET | `/api/v1/group/{group_id}/acad/branch-results/branch/{branch_id}/distribution/` | JWT | Score distribution histogram data for drawer |
| GET | `/api/v1/group/{group_id}/acad/branch-results/charts/grouped-bar/` | JWT | Per-subject grouped bar chart data |
| GET | `/api/v1/group/{group_id}/acad/branch-results/charts/kde/` | JWT | Kernel density overlay line chart data |
| GET | `/api/v1/group/{group_id}/acad/branch-results/charts/radar/` | JWT | Radar chart data |
| GET | `/api/v1/group/{group_id}/acad/branch-results/export/report/?format=pdf` | JWT | Export PDF comparison report |

All endpoints accept common query params: `exam_id`, `stream`, `class_level`, `branch_ids`.

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| "Load Comparison" click | `click` | GET `.../compare/?exam_id=&stream=&class=&branch_ids=` | `#comparison-panel` | `innerHTML` |
| Branch chip remove | `click` | GET `.../compare/?...updated branch_ids` | `#comparison-panel` | `innerHTML` |
| Branch detail drawer open | `click` | GET `.../branch/{id}/detail/?exam_id=` | `#drawer-body` | `innerHTML` |
| Drawer tab switch | `click` | GET `.../branch/{id}/distribution/?...` | `#branch-detail-tab-content` | `innerHTML` |
| Subject filter change in config | `change` | GET `.../compare/subjects/?...&subject=` | `#subject-comparison-table` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
