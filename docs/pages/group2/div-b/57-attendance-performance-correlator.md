# 57 — Attendance vs Performance Correlator

> **URL:** `/group/acad/attendance-performance/`
> **File:** `57-attendance-performance-correlator.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Roles:** Academic Director G3 · CAO G4 · Academic MIS Officer G1

---

## 1. Purpose

The Attendance vs Performance Correlator is a dedicated analytical tool that quantifies and visualises the relationship between student attendance and academic results across the group. This page answers a question that institution management frequently asks but rarely has the data to answer rigorously: does attending class more actually lead to better marks, and if so, how strong is that relationship in this specific institution group?

The tool produces a scatter plot of attendance percentage (X-axis) against exam score percentage (Y-axis) with one data point per student, colour-coded by branch. Overlaid on the scatter is a regression line with a Pearson correlation coefficient displayed — a value near 1 indicates strong positive correlation, near 0 indicates no relationship. Academic Directors use this to counter the argument from both parents and branch principals that extra coaching hours (which often displace regular attendance) are more valuable than classroom attendance.

The analysis is filterable by branch, stream, class, exam, and date range, so the Academic Director can determine whether the correlation is stronger in certain streams (e.g. MPC vs MEC) or in certain branches, enabling targeted policy recommendations. The same scatter is replicated per branch in a tabbed view, enabling branch-level comparisons.

---

## 2. Role Access

| Role | Level | Can View | Can Create/Act | Notes |
|---|---|---|---|---|
| Chief Academic Officer (CAO) | G4 | ✅ Full | ❌ No write | Analytical view |
| Group Academic Director | G3 | ✅ Full | ✅ Add annotations | Can annotate chart with contextual events |
| Group Curriculum Coordinator | G2 | ❌ | ❌ | No access |
| Group Exam Controller | G3 | ❌ | ❌ | No access |
| Group Results Coordinator | G3 | ❌ | ❌ | No access |
| Stream Coordinators (all) | G3 | ❌ | ❌ | No access |
| Group JEE/NEET Integration Head | G3 | ❌ | ❌ | No access |
| Group IIT Foundation Director | G3 | ❌ | ❌ | No access |
| Group Olympiad & Scholarship Coord | G3 | ❌ | ❌ | No access |
| Group Special Education Coordinator | G3 | ❌ | ❌ | No access |
| Group Academic MIS Officer | G1 | ✅ Full | ❌ | Read-only analytical access |
| Group Academic Calendar Manager | G3 | ❌ | ❌ | No access |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Academic  ›  Academic MIS & Analytics  ›  Attendance vs Performance
```

### 3.2 Page Header
```
Attendance vs Performance Correlator                         [Export PNG]  [Export XLSX]
Scatter analysis — all students · Pearson r displayed              (Academic Dir, CAO, MIS)
```

### 3.3 Summary Stats Bar

| Stat | Value |
|---|---|
| Students in Analysis | Count (based on current filter) |
| Pearson Correlation (r) | Value — e.g. 0.72 (strong positive) |
| Attendance Avg | % |
| Score Avg | % |
| Students Below 75% Attendance AND Below Pass | Count — dual-risk students |

---

## 4. Main Content

### 4.1 Filter Panel (inline — not a slide-in drawer for this analytics page)

| Filter | Type | Options |
|---|---|---|
| Exam | Select | From Group Exam Calendar |
| Stream | Select | MPC / BiPC / MEC / CEC / HEC / Foundation |
| Class | Multi-select | Class 6–12 |
| Branch | Multi-select | All branches |
| Date range (for attendance calculation) | Date range picker | Default: term-to-date |
| Minimum data points | Select | Include students with ≥ 1 / ≥ 2 / ≥ 3 exams |

[Apply Filters] button · [Reset]

### 4.2 Group Scatter Chart (Primary)

**Chart type:** Scatter chart (Chart.js 4.x)
**X-axis:** Attendance % (0–100)
**Y-axis:** Exam score % (0–100)
**Each data point:** One student
**Colour coding:** Each branch gets a unique colorblind-safe colour; legend at right
**Overlaid regression line:** Best-fit linear regression in dark grey
**Quadrant reference lines:** Vertical at 75% attendance (minimum threshold) · Horizontal at pass mark (configurable, default 35%)
**Quadrant labels:**
- Top-right: "High attendance, high marks" (ideal)
- Top-left: "Low attendance, high marks" (coaching-dependent)
- Bottom-right: "High attendance, low marks" (effort without outcome — teaching quality issue)
- Bottom-left: "Low attendance, low marks" (at-risk zone)

**Tooltip on hover:** Student ID · Attendance: X% · Score: X% · Branch: [Name]

**Correlation stats panel (below chart):**
- Pearson r: X.XX
- p-value: < 0.001 (statistically significant) or "Not significant"
- Sample size: N students
- Regression equation: Score = m × Attendance + c

**Export:** PNG of full chart

### 4.3 Per-Branch Tab View

Tabbed section below the group chart: one tab per branch.
Each tab contains the same scatter chart and correlation stats filtered to that branch's students.

- **Tab:** Branch name (with student count badge)
- **Content:** Same chart layout; correlation r displayed prominently

### 4.4 XLSX Export Data

XLSX contains:
- Sheet 1: All students — Student ID (no name) · Branch · Class · Stream · Attendance % · Score % · Exam
- Sheet 2: Correlation summary — Branch · r · p-value · N · Regression equation
- Sheet 3: Quadrant counts — Branch × Quadrant breakdown

---

## 5. Drawers & Modals

### 5.1 (No primary drawers — this is an analytics page)

### 5.2 Modal: `annotation-add` (Academic Director only)
- **Trigger:** Right-click or [+ Add Annotation] on chart
- **Width:** 400px
- **Content:** Mark a point or range on the X-axis (attendance %) with a contextual label
- **Fields:** Annotation text (Textarea, max 200 chars) · Attendance range (X1–X2 %) · Date
- **Use case:** "Strike week — attendance drop across MPC students 2026-02-10 to 2026-02-17"
- **Buttons:** [Add Annotation] · [Cancel]
- **Annotations displayed as vertical shaded regions on chart with label**

---

## 6. Charts

All charts are on this page itself (it is an analytics page):

### 6.1 Group Scatter — described in 4.2 above

### 6.2 Per-Branch Scatter — described in 4.3 above

### 6.3 Correlation by Stream (Bar)
- **Type:** Horizontal bar
- **Data:** Pearson r per stream
- **Tooltip:** Stream · r value
- **Colour:** Green (strong positive r > 0.5) · Amber (moderate 0.3–0.5) · Red (weak < 0.3)
- **Export:** PNG

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Filters applied | "Analysis updated — [N] students in view" | Info | 3s |
| Annotation added | "Chart annotation added" | Success | 4s |
| PNG exported | "Chart exported as PNG" | Info | 3s |
| XLSX exported | "Data export ready" | Info | 4s |
| Insufficient data | "Not enough data points for reliable correlation analysis" | Warning | 6s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No exam selected | "Select an exam to begin analysis" | "Choose an exam from the filter panel to populate the scatter chart" | — |
| Insufficient data | "Not enough data" | "At least 30 student data points are required for meaningful correlation analysis" | — |
| No branches match filter | "No data for selected branches" | "Try including more branches in your filter" | [Reset Filters] |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: filter panel + chart area placeholder + stats bar |
| Filter apply | Spinner in chart area → chart renders with smooth animation |
| Per-branch tab click | Spinner in tab content area |
| Correlation by stream chart | Skeleton bar chart |
| PNG export | Spinner on export button |

---

## 10. Role-Based UI Visibility

| Element | Academic Dir G3 | CAO G4 | MIS G1 |
|---|---|---|---|
| Scatter chart (group) | ✅ | ✅ | ✅ |
| Per-branch tabs | ✅ | ✅ | ✅ |
| Correlation by stream bar | ✅ | ✅ | ✅ |
| Student tooltip (Student ID) | ✅ | ✅ | ✅ (ID only, no name) |
| [+ Add Annotation] | ✅ | ❌ | ❌ |
| [Export PNG] | ✅ | ✅ | ✅ |
| [Export XLSX] | ✅ | ✅ | ✅ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/acad/attendance-performance/scatter/` | JWT | Scatter chart data (with filters) |
| GET | `/api/v1/group/{group_id}/acad/attendance-performance/stats/` | JWT | Stats bar + correlation stats |
| GET | `/api/v1/group/{group_id}/acad/attendance-performance/by-branch/{branch_id}/` | JWT | Per-branch scatter data |
| GET | `/api/v1/group/{group_id}/acad/attendance-performance/stream-correlation/` | JWT | Stream-wise r values bar chart |
| GET | `/api/v1/group/{group_id}/acad/attendance-performance/export-xlsx/` | JWT | XLSX data download |
| POST | `/api/v1/group/{group_id}/acad/attendance-performance/annotations/` | JWT (G3 Dir) | Add chart annotation |
| GET | `/api/v1/group/{group_id}/acad/attendance-performance/annotations/` | JWT | Get all annotations |
| DELETE | `/api/v1/group/{group_id}/acad/attendance-performance/annotations/{id}/` | JWT (G3 Dir) | Remove annotation |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Filter apply | `click` | GET `.../attendance-performance/scatter/?filters=` | `#scatter-chart-container` | `innerHTML` |
| Stats bar update | `click` | GET `.../attendance-performance/stats/?filters=` | `#stats-bar` | `innerHTML` |
| Per-branch tab click | `click` | GET `.../attendance-performance/by-branch/{bid}/?filters=` | `#branch-scatter-container` | `innerHTML` |
| Annotation submit | `submit` | POST `.../attendance-performance/annotations/` | `#chart-annotations` | `beforeend` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
