# Page 21: Scholarship Exam Analysis

**URL:** `/group/adm/scholarship-exam/analysis/`
**Template:** `portal_base.html` (light theme)
**Division:** C — Group Admissions · Scholarship Section

---

## 1. Purpose

The Scholarship Exam Analysis page provides comprehensive post-exam analytics for every completed scholarship examination across the group. Its primary purpose is two-fold: first, to evaluate exam quality so that future exams are better designed; and second, to surface the strongest scholarship candidates from across all branches so the Scholarship Manager can make defensible, data-driven award decisions. This page is available after results have been published.

On the exam quality side, the page answers critical questions: Were questions too easy or too hard for the cohort? Which topics are most candidates struggling with — indicating syllabus coverage gaps in branches? Are there questions with near-zero accuracy that might indicate poor phrasing or printing errors? The Difficulty vs Accuracy Scatter plot is particularly valuable here — questions that were intended to be hard but had high accuracy (poorly calibrated) or questions intended to be easy but had low accuracy (potential printing issue or curricular gap) are immediately visible as outliers.

On the talent identification side, the score distribution, branch-wise rank tables, and topper analysis sections provide the Scholarship Manager with everything needed to identify the right candidates for merit-based awards. The Subject-wise Performance Heatmap gives a cross-branch view of relative academic strength by subject, helping distinguish branches that genuinely prepare students well from those where a high ranker might have been a large fish in a small pond. All charts are rendered using Chart.js 4.x and load their data from FastAPI endpoints.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Scholarship Exam Manager (26) | G3 | Full access to all sections | Primary user for exam quality analysis |
| Group Admissions Director (23) | G3 | Full view access | No edit actions |
| Group Scholarship Manager (27) | G3 | Topper Analysis section only (Section 5.6) | Restricted to talent identification |
| Chief Academic Officer | G2 | Full view access | Cross-division read |
| MIS Officer | G2 | Full view access | Reporting purposes |
| Group Admission Coordinator (24) | G3 | No access | Excluded |
| Group Admission Counsellor (25) | G3 | No access | Excluded |

**Enforcement:** Page access validated server-side via `@role_required(['scholarship_exam_manager', 'admissions_director', 'scholarship_manager', 'cao', 'mis_officer'])`. The Scholarship Manager's Django template context scopes visible sections to `section_5_6_only = True`. All chart data API endpoints check role scope before returning data.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Admissions → Scholarship Exams → Analysis
```

### 3.2 Page Header
- **Title:** Scholarship Exam Analysis
- **Subtitle:** Post-exam performance insights — published results only
- **Exam Selector:** Prominent dropdown at top — "Select Exam to Analyse" — lists all exams with status = published. On selection, all sections update.
- **Action Buttons:** `[Export Analysis Report PDF]` · `[Export Data CSV]`

### 3.3 Alert Banner
Triggers:
- **Amber — No Published Results Yet:** "No scholarship exam results have been published yet. Analysis will be available after publication."
- **Blue — Analysis Ready:** "Analysis loaded for: {Exam Name} — {date conducted} · {n} candidates · {b} branches."
- **Amber — Low Participation Branch:** "3 branches had fewer than 10 candidates appear for this exam. Branch-level analysis may be statistically unreliable for these branches."
- **Red — Outlier Questions Detected:** "{n} questions have accuracy below 10%. Review these questions for potential printing or content errors."

---

## 4. KPI Summary Bar

*Note: These KPIs are exam-contextual — all values are for the selected exam.*

| Card | Metric | Source | Colour Rule | Drill-down |
|---|---|---|---|---|
| Exam Selector (context chip) | Selected exam name + date | Page-level state | Blue always | None — informational |
| Avg Score (Group) | Mean score across all candidates in selected exam | `exam_result_candidate` aggregation | Blue always | → Score distribution chart |
| Pass Rate % | (Candidates ≥ passing threshold / total candidates) × 100 | `exam_result_candidate` | Green ≥ 70% · Amber 40–69% · Red < 40% | → result details |
| Toppers (Score > 90%) | COUNT where percentage > 90 | `exam_result_candidate` | Blue always | → Section 5.6 |
| Score Range | Min score – Max score (e.g., 12 – 98) | `exam_result_candidate` | Blue always | → distribution chart |
| Lowest Avg Subject | Subject name with lowest mean accuracy % | `exam_question_response` aggregation | Red always (indicates weakness) | → Section 5.3 topic accuracy |

**HTMX Refresh:** Every 5 minutes via `hx-trigger="every 5m"` targeting `#kpi-bar`. Exam selector change also refreshes immediately.

---

## 5. Sections

### 5.1 Score Distribution Chart

**Display:** Histogram (Chart.js 4.x bar chart) — candidates grouped by score band.

**Score Bands:** 0–20 · 21–40 · 41–60 · 61–80 · 81–100

**Datasets:** Group-wide bar (blue) plus per-branch line overlay (multi-colour toggle). Branch overlay toggled via checkboxes — up to 5 branches overlaid at once to avoid clutter.

**Tooltip:** On hover: band label, count of candidates in that band (group-wide), count per selected branch.

**Interaction:** Clicking a bar opens question-accuracy-detail drawer for that score band.

**Chart Controls:** Toggle branches (checkbox list) · Reset to group-only view.

**HTMX Load:** `hx-trigger="load, examSelected from:body"` → `GET /api/v1/group/{group_id}/adm/scholarship-exam/analysis/{exam_id}/score-distribution/` targeting `#score-distribution-chart-data`.

---

### 5.2 Subject-wise Performance Heatmap

**Display:** Matrix table — branches as rows, subjects as columns, cell value = avg score % for that branch × subject combination. Cell background colour: gradient from red (0%) → yellow (50%) → green (100%).

**Row header:** Branch name + total candidates from that branch.
**Column header:** Subject name + group avg (shown in column footer).

**Interaction:** Click a cell → opens branch-analysis-detail drawer for that branch × subject pair.

**Legend:** Colour scale bar below the matrix (0% → 100%).

**HTMX Load:** `hx-trigger="load, examSelected from:body"` → `GET /api/v1/group/{group_id}/adm/scholarship-exam/analysis/{exam_id}/subject-heatmap/`.

**Empty State:** "Select an exam to view the heatmap."

---

### 5.3 Topic-wise Accuracy

**Display:** Table — one row per topic in the exam.

**Columns:**

| Column | Notes |
|---|---|
| Topic | Topic name |
| Subject | Parent subject |
| Total Questions | Count of questions from this topic in the exam |
| Avg Accuracy % | Mean (correct / total) across all candidates for this topic |
| Branches Below 50% Accuracy | Count of branches where avg accuracy for this topic < 50% |
| Difficulty Rating | Easy / Medium / Hard (from question bank) |
| Status | On-target / Weak Area (amber — avg < 50%) / Critical (red — avg < 30%) |

**Sort:** Avg Accuracy % ASC by default (weakest topics first).

**Interaction:** Click a topic row → opens question-accuracy-detail drawer for that topic.

**HTMX Load:** `hx-trigger="load, examSelected from:body"` → `GET /api/v1/group/{group_id}/adm/scholarship-exam/analysis/{exam_id}/topic-accuracy/`.

**Empty State:** "Select an exam to view topic-wise accuracy."

---

### 5.4 Branch-wise Rank Distribution

**Display:** Stacked horizontal bar chart (Chart.js 4.x) — one bar per branch.

**Segments (rank bands):** Top 10 (dark blue) · Top 11–25 (medium blue) · Top 26–50 (light blue) · Rank 51+ (grey)

**Y-axis:** Branch names. **X-axis:** Count of candidates.

**Tooltip:** On hover: branch name, count in each rank band, total candidates from branch.

**Interaction:** Click a branch bar → opens branch-analysis-detail drawer.

**HTMX Load:** `hx-trigger="load, examSelected from:body"` → `GET /api/v1/group/{group_id}/adm/scholarship-exam/analysis/{exam_id}/rank-distribution/`.

---

### 5.5 Difficulty vs Accuracy Scatter

**Display:** Scatter chart (Chart.js 4.x) — one data point per question in the exam.

**Axes:**
- X-axis: Intended difficulty (mapped numerically: Easy = 1, Medium = 2, Hard = 3)
- Y-axis: Actual accuracy % (0–100)

**Data Point Labels:** Hover tooltip shows question number, topic, intended difficulty, actual accuracy %.

**Quadrant Annotations (Chart.js plugin or canvas overlay):**
- Top-left: "Too Easy for Difficulty Rating" (amber zone)
- Bottom-right: "Harder than Intended" (amber zone)
- Bottom-left: "Potential Issue — Low Accuracy on Easy Q" (red zone)
- Top-right: "Intended and Achieved" (green zone)

**Outlier Highlight:** Points with accuracy < 10% shown in red — clicking opens question-accuracy-detail drawer.

**HTMX Load:** `hx-trigger="load, examSelected from:body"` → `GET /api/v1/group/{group_id}/adm/scholarship-exam/analysis/{exam_id}/difficulty-accuracy-scatter/`.

---

### 5.6 Topper Analysis Table

**Display:** Table — top 50 candidates by rank for selected exam. Server-side paginated (25/page).

**Columns:**

| Column | Notes |
|---|---|
| Rank | Group-wide rank |
| Candidate Name | Full name |
| Branch | Branch name |
| Stream | MPC / BIPC / MEC / CEC / Commerce / Arts etc. |
| Total Score | Numeric |
| Subject-wise Scores | Per-subject columns (dynamic) |
| Scholarship Recommendation | Auto-recommended (green chip) / Not recommended (grey) / Manually added (blue chip) |
| Actions | `[View Full Scorecard →]` |

**Filters:** Branch, Stream, Scholarship Recommendation status

**Note for Scholarship Manager:** Banner at top of this section: "This table is visible to the Scholarship Manager for candidate identification."

**HTMX Load:** `hx-trigger="load, examSelected from:body"` → `GET /api/v1/group/{group_id}/adm/scholarship-exam/analysis/{exam_id}/toppers/`.

**Empty State:** No exam selected or no results published.

---

## 6. Drawers & Modals

### 6.1 Question Accuracy Detail Drawer
- **Width:** 640px
- **Trigger:** Click on question point in scatter chart, or click on topic in Section 5.3
- **HTMX Endpoint:** `GET /api/v1/group/{group_id}/adm/scholarship-exam/analysis/{exam_id}/questions/{question_id}/accuracy-detail/`
- **Content:** Full question text + options, correct answer, per-option response distribution (bar chart — how many chose A/B/C/D), overall accuracy %, per-branch accuracy breakdown table, difficulty rating vs actual performance note.
- **For Exam Manager:** Flag for review link if outlier.

### 6.2 Branch Analysis Detail Drawer
- **Width:** 560px
- **Trigger:** Click on branch bar in Section 5.4, or click a heatmap cell
- **HTMX Endpoint:** `GET /api/v1/group/{group_id}/adm/scholarship-exam/analysis/{exam_id}/branches/{branch_id}/detail/`
- **Content:** Branch summary — total candidates, score distribution (mini histogram Chart.js), subject-wise avg scores table, rank count by band, top 3 candidates from branch, comparison vs group average (delta per subject).

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Exam selected | "Analysis loaded for: {Exam Name}." | Info | 2 s |
| Export PDF queued | "Analysis report PDF is being prepared. Download will start shortly." | Info | 4 s |
| Export CSV queued | "Data export CSV is being prepared." | Info | 4 s |
| No published results available | "No published results found. Analysis requires published exam results." | Warning | 5 s |
| Chart data load error | "Chart data could not be loaded. Try refreshing the page." | Error | 5 s |

---

## 8. Empty States

| Condition | Illustration | Heading | Description | CTA |
|---|---|---|---|---|
| No exam selected | Bar-chart icon | "Select an Exam to Begin" | "Choose a published scholarship exam from the dropdown to load analysis." | None (points to selector) |
| No published exams exist | Clock icon | "No Published Results Yet" | "Analysis is available after exam results are published." | `[Go to Results →]` |
| No candidates in selected exam | Users-x icon | "No Candidate Data" | "This exam has no candidate records. Results may not have been uploaded." | `[Go to Results →]` |
| Topic accuracy table empty | Table icon | "No Topic Data Available" | "Topic-wise accuracy data is not available for this exam." | None |
| Toppers table empty (< 1 candidate) | Award icon | "No Toppers Data" | "Rank data has not been computed for this exam yet." | `[Go to Results →]` |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | KPI shimmer (6 cards) + chart canvas placeholders (grey boxes with spinner) |
| Exam selector change | All section content masked with overlay spinner while charts reload |
| Score distribution chart load | Canvas shimmer with "Loading chart…" text |
| Subject heatmap load | Table skeleton shimmer (rows × columns pattern) |
| Topic accuracy table load | Table skeleton (8 row shimmer) |
| Rank distribution chart load | Horizontal bar skeleton shimmer |
| Scatter chart load | Canvas shimmer |
| Topper table load | Table skeleton (10 row shimmer) |
| Question accuracy drawer open | 640px drawer skeleton with mini chart placeholder |
| Branch analysis drawer open | 560px drawer skeleton with histogram placeholder |
| PDF/CSV export | Button spinner + "Preparing…" text |

---

## 10. Role-Based UI Visibility

| Element | Exam Manager (26) | Director (23) | Scholarship Manager (27) | CAO / MIS | Coordinator (24) |
|---|---|---|---|---|---|
| Section 5.1 Score Distribution | Visible | Visible | Hidden | Visible | No access |
| Section 5.2 Heatmap | Visible | Visible | Hidden | Visible | No access |
| Section 5.3 Topic Accuracy | Visible | Visible | Hidden | Visible | No access |
| Section 5.4 Rank Distribution | Visible | Visible | Hidden | Visible | No access |
| Section 5.5 Difficulty Scatter | Visible | Visible | Hidden | Visible | No access |
| Section 5.6 Topper Analysis | Visible | Visible | Visible | Visible | No access |
| Scholarship Manager section banner | Visible | Visible | Visible | Hidden | No access |
| `[Export Analysis Report PDF]` | Visible | Visible | Visible (toppers only) | Visible | No access |
| `[Export Data CSV]` | Visible | Visible | Hidden | Visible | No access |
| Question accuracy drawer | Visible | Visible | Hidden | Visible | No access |
| Branch analysis drawer | Visible | Visible | Hidden | Visible | No access |
| KPI bar (all 6 cards) | Visible | Visible | Visible (2 cards — toppers, avg) | Visible | No access |

*All UI visibility decisions made server-side in Django template. No client-side JS role checks.*

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/adm/scholarship-exam/analysis/kpis/` | JWT G3 | KPI bar data (exam_id param) |
| GET | `/api/v1/group/{group_id}/adm/scholarship-exam/analysis/exams/published/` | JWT G3 | List of published exams for selector |
| GET | `/api/v1/group/{group_id}/adm/scholarship-exam/analysis/{exam_id}/score-distribution/` | JWT G3 | Score distribution histogram data |
| GET | `/api/v1/group/{group_id}/adm/scholarship-exam/analysis/{exam_id}/subject-heatmap/` | JWT G3 | Subject-wise heatmap matrix data |
| GET | `/api/v1/group/{group_id}/adm/scholarship-exam/analysis/{exam_id}/topic-accuracy/` | JWT G3 | Topic-wise accuracy table |
| GET | `/api/v1/group/{group_id}/adm/scholarship-exam/analysis/{exam_id}/rank-distribution/` | JWT G3 | Branch rank distribution chart data |
| GET | `/api/v1/group/{group_id}/adm/scholarship-exam/analysis/{exam_id}/difficulty-accuracy-scatter/` | JWT G3 | Scatter chart data |
| GET | `/api/v1/group/{group_id}/adm/scholarship-exam/analysis/{exam_id}/toppers/` | JWT G3 | Top 50 candidates table |
| GET | `/api/v1/group/{group_id}/adm/scholarship-exam/analysis/{exam_id}/questions/{question_id}/accuracy-detail/` | JWT G3 | Question accuracy detail drawer |
| GET | `/api/v1/group/{group_id}/adm/scholarship-exam/analysis/{exam_id}/branches/{branch_id}/detail/` | JWT G3 | Branch deep-dive drawer |
| GET | `/api/v1/group/{group_id}/adm/scholarship-exam/analysis/{exam_id}/export/pdf/` | JWT G3 | Export analysis report PDF |
| GET | `/api/v1/group/{group_id}/adm/scholarship-exam/analysis/{exam_id}/export/csv/` | JWT G3 | Export data CSV |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| KPI bar auto-refresh | `every 5m` | GET `.../analysis/kpis/?exam_id={id}` | `#kpi-bar` | `innerHTML` |
| Exam selector change — load KPIs | `change` on exam dropdown | GET `.../analysis/kpis/?exam_id={id}` | `#kpi-bar` | `innerHTML` |
| Exam selector change — fire event | `change` on exam dropdown | (dispatches `examSelected` custom event to body) | N/A | N/A |
| Load score distribution chart data | `load, examSelected from:body` | GET `.../analysis/{exam_id}/score-distribution/` | `#score-distribution-data` | `innerHTML` |
| Load subject heatmap data | `load, examSelected from:body` | GET `.../analysis/{exam_id}/subject-heatmap/` | `#subject-heatmap-container` | `innerHTML` |
| Load topic accuracy table | `load, examSelected from:body` | GET `.../analysis/{exam_id}/topic-accuracy/` | `#topic-accuracy-table` | `innerHTML` |
| Load rank distribution data | `load, examSelected from:body` | GET `.../analysis/{exam_id}/rank-distribution/` | `#rank-distribution-data` | `innerHTML` |
| Load scatter chart data | `load, examSelected from:body` | GET `.../analysis/{exam_id}/difficulty-accuracy-scatter/` | `#scatter-chart-data` | `innerHTML` |
| Load topper table | `load, examSelected from:body` | GET `.../analysis/{exam_id}/toppers/` | `#topper-table-body` | `innerHTML` |
| Open question accuracy drawer | `click` on outlier point / topic row | GET `.../analysis/{exam_id}/questions/{q_id}/accuracy-detail/` | `#drawer-container` | `innerHTML` |
| Open branch analysis drawer | `click` on branch bar / heatmap cell | GET `.../analysis/{exam_id}/branches/{b_id}/detail/` | `#drawer-container` | `innerHTML` |
| Filter topper table | `change` on filter inputs | GET `.../analysis/{exam_id}/toppers/?{filters}` | `#topper-table-body` | `innerHTML` |
| Paginate topper table | `click` on page link | GET `.../analysis/{exam_id}/toppers/?page={n}` | `#topper-table-container` | `innerHTML` |
| Export PDF | `click` on export button | GET `.../analysis/{exam_id}/export/pdf/` | (file download) | none |
| Export CSV | `click` on export button | GET `.../analysis/{exam_id}/export/csv/` | (file download) | none |
| Sort topic accuracy table | `click` on column header | GET `.../analysis/{exam_id}/topic-accuracy/?sort={col}&dir={asc\|desc}` | `#topic-accuracy-table` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
