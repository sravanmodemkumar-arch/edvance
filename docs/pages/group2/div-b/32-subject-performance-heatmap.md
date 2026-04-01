# 32 — Subject Performance Heatmap

> **URL:** `/group/acad/subject-performance/`
> **File:** `32-subject-performance-heatmap.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** CAO G4 · Academic Director G3 · Stream Coordinators G3 · Exam Controller G3 · Academic MIS Officer G1

---

## 1. Purpose

The Subject Performance Heatmap translates raw exam data into an instant visual diagnostic across all branches. For each topic within a selected subject, the heatmap shows the average marks percentage achieved by every branch — colour-coded red (below 50%), amber (50–70%), and green (above 70%). A group Academic Director or CAO looking at this page for five minutes can identify which topics are systematically weak across multiple branches, which branches need targeted intervention, and which branches are outperforming peers on specific topics.

For a group with 50 branches and 120 topics per stream, a purely tabular view would require hundreds of rows. The heatmap collapses this into a single scannable grid: X-axis as topics, Y-axis as branches, each cell as a colour-coded average marks percentage. A branch row that is predominantly red signals a systemic curriculum or teaching gap. A topic column that is predominantly red signals a group-wide weakness that requires curriculum review or supplementary material deployment from the Shared Content Library.

The drill-down capability converts the heatmap from a diagnostic view into an action starting point. Clicking any cell opens a drawer showing the specific questions from that topic asked in the exam, the average marks per question, the most commonly chosen wrong option, and the difficulty-vs-result correlation. This gives Stream Coordinators the granular data needed to plan remedial classes or flag question bank quality issues.

---

## 2. Role Access

| Role | Level | Can View | Can Act | Notes |
|---|---|---|---|---|
| Chief Academic Officer (CAO) | G4 | ✅ All streams, all branches | ✅ Export · Drill-down | Full cross-stream view |
| Group Academic Director | G3 | ✅ All streams, all branches | ✅ Export · Drill-down | Full access |
| Group Curriculum Coordinator | G2 | ❌ | ❌ | No access to results section |
| Group Exam Controller | G3 | ✅ All streams, all branches | ✅ Export · Drill-down | For question bank quality review |
| Group Results Coordinator | G3 | ✅ All streams | ✅ Export · Drill-down | Full access |
| Group Stream Coord — MPC | G3 | ✅ MPC subjects only | ✅ Export (own stream) · Drill-down | Cannot see BiPC/MEC subjects |
| Group Stream Coord — BiPC | G3 | ✅ BiPC subjects only | ✅ Export (own stream) · Drill-down | Cannot see MPC/MEC subjects |
| Group Stream Coord — MEC/CEC | G3 | ✅ MEC/CEC subjects only | ✅ Export (own stream) · Drill-down | Cannot see MPC/BiPC subjects |
| Group JEE/NEET Integration Head | G3 | ✅ Physics, Chemistry, Maths, Biology | ✅ Export · Drill-down | JEE/NEET relevant subjects only |
| Group IIT Foundation Director | G3 | ✅ Foundation subjects (Cl.6–10) | ✅ Export · Drill-down | Foundation only |
| Group Olympiad & Scholarship Coord | G3 | ❌ | ❌ | No access |
| Group Special Education Coordinator | G3 | ❌ | ❌ | No access |
| Group Academic MIS Officer | G1 | ✅ All streams, all branches | ✅ Export only | No drill-down action |
| Group Academic Calendar Manager | G3 | ❌ | ❌ | No access |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Academic  ›  Subject Performance Heatmap
```

### 3.2 Page Header
```
Subject Performance Heatmap                         [Export PNG ↓]  [Export XLSX ↓]
[Group Name] — Topic-level performance across all branches
```

### 3.3 Filter Controls (above heatmap — always visible)

| Filter | Type | Required | Options |
|---|---|---|---|
| Exam | Select | ✅ | Completed exams with moderated results |
| Stream | Select | ✅ | MPC · BiPC · MEC · CEC · HEC · Foundation · JEE/NEET |
| Subject | Select | ✅ | Dynamically populated based on stream |
| Class | Select | ✅ (if multi-class stream) | Class 6–12 |
| Branch | Multi-select | ❌ | Default: All branches (50 rows); can narrow to selected |

"Apply Filters" button — heatmap reloads on apply.

---

## 4. Main Content — Heatmap

### 4.1 Heatmap Grid

```
                 [Topic 1]  [Topic 2]  [Topic 3]  [Topic 4]  ...  [Topic N]
Branch A        |  87%  |   42%  |   65%  |   91%  |  ...  |   55%  |
Branch B        |  73%  |   38%  |   71%  |   88%  |  ...  |   49%  |
Branch C        |  91%  |   82%  |   94%  |   78%  |  ...  |   83%  |
...
Branch 50       |  55%  |   47%  |   58%  |   62%  |  ...  |   40%  |
```

**Cell colour coding:**
- Red: < 50% average marks — `bg-red-200 text-red-900`
- Amber: 50%–70% — `bg-amber-100 text-amber-900`
- Green: > 70% — `bg-green-100 text-green-900`

**Cell content:** Average marks percentage, displayed as integer (e.g. "87%").

**Cell tooltip (on hover):** Branch Name · Topic Name · Avg Marks: X / Max Y (Z%) · Students: N · Questions in exam: N

**Cell click:** Opens `topic-branch-drill` drawer 480px.

**Colorblind accessibility:** In addition to colour, cells below 50% show a downward triangle indicator (▼), amber cells show a horizontal dash (—), and green cells show an upward triangle (▲). This ensures readability for users with red-green colour blindness.

### 4.2 Heatmap Axes

**X-axis (columns — Topics):**
- Topics from the Subject-Topic Master for the selected subject
- Ordered by curriculum sequence number (as defined in Subject-Topic Master page 18)
- Column headers truncated at 20 chars with full name in tooltip
- Fixed column: "Branch" label column on left
- Horizontal scroll if topics exceed visible width

**Y-axis (rows — Branches):**
- Branch Name (short code in parentheses if long name)
- Sorted: worst-performing branch first (lowest row average %) by default
- Re-sortable: Alphabetical by branch name / By average (asc/desc) / By state

**Sort control:** Dropdown above heatmap — "Sort branches by: Average Score (Worst first) | Alphabetical | State"

### 4.3 Heatmap Summary Row and Column

**Bottom summary row:** "Group Average" — shows group-wide average % per topic column. Coloured by same Red/Amber/Green rule.

**Right summary column:** "Branch Average" — shows branch's average % across all topics. Coloured by same rule.

**Corner cell:** "Overall Group Avg" — single percentage for the full heatmap.

### 4.4 Highlighting Controls

| Toggle | Effect |
|---|---|
| Highlight worst topic per branch | Adds dark red border to the single worst cell in each row |
| Highlight worst branch per topic | Adds dark red border to the single worst cell in each column |
| Show only red cells | Hides amber and green cells (shows dashes) — focuses attention on critical gaps |

---

## 5. Drawers & Modals

### 5.1 Drawer: `topic-branch-drill`
- **Trigger:** Click on any heatmap cell
- **Width:** 480px
- **Title:** "[Branch Name] — [Topic Name] — [Subject]"
- **Tabs:** Summary · Questions · Difficulty Analysis

#### Tab: Summary
| Metric | Value |
|---|---|
| Branch | Name + code |
| Topic | Name |
| Subject | |
| Exam | |
| Students who attempted | N |
| Questions from this topic | N |
| Avg marks (topic) | X / Y (Z%) |
| Group avg (same topic) | X% — shown for comparison |
| Delta vs group avg | e.g. "+5%" (green) or "−12%" (red) |
| Most common wrong answer | e.g. "Q4: Option B chosen by 67% — correct is D" |

#### Tab: Questions
Table: Q# · Question text (truncated, full on expand) · Max marks · Avg marks · Avg % · Most wrong option · Difficulty (1–5) · Attempts

Questions sorted by avg % ascending (worst-answered first).

Click row: expands inline to show full question text, all 4 options, correct answer, and most-chosen wrong option with percentage.

#### Tab: Difficulty Analysis
- Scatter plot: X-axis = Question Difficulty (1–5) · Y-axis = Avg marks % for that question
- Each point = one question from this topic in this branch
- Expected pattern: higher difficulty = lower marks. Points above the trend line = easier than expected. Points below = harder than expected (possible ambiguous questions).
- Tooltip: Question number · Difficulty · Avg % · Times appeared in previous exams
- Legend: Points coloured by difficulty band — Blue (1–2) · Green (3) · Amber (4) · Red (5)
- Export: PNG

---

## 6. Charts

### 6.1 Pass Rate Trend Per Subject (Line — 6 Terms)
- **Type:** Multi-line chart
- **X-axis:** Last 6 exam terms (labelled by term name + year)
- **Y-axis:** Group-wide average marks % for selected subject
- **Lines:** One per branch (multi-select — default: Top 5 + Bottom 5 branches)
- **Tooltip:** Term · Branch · Avg %
- **Colorblind-safe palette:** 10-colour set — avoiding red-green pairing for same-chart lines
- **Export:** PNG
- **Position:** Below heatmap, in a collapsible card "Subject Trend (6 Terms)"

### 6.2 Topic Coverage Completeness Bar
- **Type:** Horizontal bar chart
- **X-axis:** % of topics with average score > 70% (green zone) across all branches
- **Y-axis:** Subject names (one bar per subject in selected stream)
- **Colour:** Green if > 80% topics are green · Amber if 50–80% · Red if < 50%
- **Tooltip:** Subject · Topics in green zone: N/Total · Avg %
- **Export:** PNG
- **Shown in:** "Subject Overview" card alongside main filter controls

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Filters applied | "Heatmap loaded for [Subject] — [Exam Name] — [N] branches." | Info | 3s |
| Export PNG started | "Heatmap PNG export preparing — download will begin shortly." | Info | 4s |
| Export XLSX started | "XLSX data export preparing — download will begin shortly." | Info | 4s |
| No data for selection | "No result data available for this subject/exam combination." | Warning | Manual |
| Drill-down drawer data error | "Could not load topic detail. Please try again." | Error | Manual |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No exam selected | "Select an Exam" | "Choose a completed exam and a subject to load the heatmap" | [Apply Filters] |
| No topic data for subject | "No topic data available" | "This subject has no topic-level performance data for the selected exam" | — |
| No branches match filter | "No branches match" | "Adjust branch filters to see more data" | [Clear Branch Filter] |
| All cells in same colour band | "All topics at [Red / Amber / Green] level" | "Performance is consistent across topics — drill down for detail" | — |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: filter controls + heatmap placeholder (grey grid skeleton) |
| Filter apply | Full heatmap area spinner overlay while reloading |
| Heatmap sort change | Brief shimmer over heatmap grid |
| Topic-branch drill drawer open | Spinner in drawer body + skeleton tabs |
| Difficulty scatter chart in drawer | Spinner in chart area |
| Trend chart load | Spinner centred in chart card |
| Export triggered | Spinner in export button (momentary) |

---

## 10. Role-Based UI Visibility

| Element | CAO G4 | Academic Dir G3 | Stream Coords G3 | Exam Controller G3 | MIS G1 |
|---|---|---|---|---|---|
| Stream filter options | All streams | All streams | Own stream only | All streams | All streams |
| Export PNG/XLSX | ✅ | ✅ | ✅ (own stream) | ✅ | ✅ |
| Topic-branch drill drawer | ✅ | ✅ | ✅ (own stream) | ✅ | ❌ |
| Difficulty Analysis tab in drawer | ✅ | ✅ | ✅ | ✅ | ❌ |
| Highlight controls | ✅ | ✅ | ✅ | ✅ | ✅ |
| Branch sort controls | ✅ | ✅ | ✅ | ✅ | ✅ |
| 6-Term trend chart | ✅ | ✅ | ✅ (own stream) | ✅ | ✅ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/acad/subject-performance/exams/` | JWT | Exam list for selector |
| GET | `/api/v1/group/{group_id}/acad/subject-performance/heatmap/` | JWT | Heatmap cell data (all branches × topics for selected exam/subject) |
| GET | `/api/v1/group/{group_id}/acad/subject-performance/heatmap/summary/` | JWT | Row and column summary averages |
| GET | `/api/v1/group/{group_id}/acad/subject-performance/drill/` | JWT | Topic-branch drill drawer data |
| GET | `/api/v1/group/{group_id}/acad/subject-performance/drill/questions/` | JWT | Questions tab in drill drawer |
| GET | `/api/v1/group/{group_id}/acad/subject-performance/drill/difficulty/` | JWT | Difficulty analysis chart data for drawer |
| GET | `/api/v1/group/{group_id}/acad/subject-performance/trend/` | JWT | 6-term pass rate trend chart data |
| GET | `/api/v1/group/{group_id}/acad/subject-performance/topic-coverage/` | JWT | Topic coverage bar chart data |
| GET | `/api/v1/group/{group_id}/acad/subject-performance/export/?format=png` | JWT | Export heatmap PNG |
| GET | `/api/v1/group/{group_id}/acad/subject-performance/export/?format=xlsx` | JWT | Export raw heatmap data XLSX |

Query params for heatmap endpoint: `exam_id`, `stream`, `subject`, `class`, `branch_ids` (comma-separated or "all").

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Apply filters (heatmap load) | `click` on Apply button | GET `.../heatmap/?exam_id=&stream=&subject=&class=&branch_ids=` | `#heatmap-container` | `innerHTML` |
| Branch sort change | `change` | GET `.../heatmap/?...&sort=` | `#heatmap-container` | `innerHTML` |
| Highlight toggle | `click` | GET `.../heatmap/?...&highlight=worst_topic` | `#heatmap-container` | `innerHTML` |
| Cell click (drill drawer) | `click` | GET `.../drill/?exam_id=&branch_id=&topic_id=` | `#drawer-body` | `innerHTML` |
| Drill drawer tab switch | `click` | GET `.../drill/questions/?...` or `.../drill/difficulty/?...` | `#drill-tab-content` | `innerHTML` |
| Trend chart filter change | `change` | GET `.../trend/?exam_id=&subject=&branch_ids=` | `#trend-chart-container` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
