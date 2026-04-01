# F-08 — Exam Analytics

> **Route:** `/ops/exam/analytics/`
> **Division:** F — Exam Day Operations
> **Primary Role:** Results Coordinator (36) — primary consumer; Analytics Manager (42) — read; Content Director (18) — read (for question quality insights)
> **Supporting Roles:** Exam Operations Manager (34) — read; Platform Admin (10) — full
> **File:** `f-08-exam-analytics.md`
> **Priority:** P2 — Post-exam analysis; informs content quality (Div D), question bank improvement, and institution performance trends

---

## 1. Page Name & Route

**Page Name:** Exam Analytics
**Route:** `/ops/exam/analytics/`
**Part-load routes:**
- `/ops/exam/analytics/?part=kpi` — KPI strip
- `/ops/exam/analytics/?part=score-distribution` — score distribution tab
- `/ops/exam/analytics/?part=item-analysis` — item analysis tab
- `/ops/exam/analytics/?part=institution-comparison` — institution comparison tab
- `/ops/exam/analytics/?part=trend-analysis` — trend analysis tab
- `/ops/exam/analytics/?part=export-modal` — export modal

---

## 2. Purpose

F-08 provides post-exam analytics for three distinct audiences:

1. **Results Coordinator (36):** Validate result quality, understand score distribution, identify outlier exams
2. **Content Director (18) + SMEs (Div D):** Item analysis — which questions were too easy/hard, which had poor discrimination — feeds back to question bank quality review
3. **Analytics Manager (42):** Platform-wide exam performance trends for MIS reports and institution health scoring

F-08 reads from computed result data (after F-04 computation) — never from live exam sessions. All data is read-only on this page.

**No Redis, no real-time:** F-08 is purely post-exam. All charts and tables are rendered on-demand (no polling) from aggregated result records. Memcached caches heavy aggregations for 30 minutes.

---

## 3. Tabs

| Tab | Label |
|---|---|
| 1 | Score Distribution |
| 2 | Item Analysis |
| 3 | Institution Comparison |
| 4 | Trend Analysis |

---

## 4. Section-Wise Detailed Breakdown

---

### Page Header — Exam Selector

Before any tab content loads, the user selects an exam:

```
[Exam Selector: Searchable dropdown — shows exams with published results]
[Date Range: optional secondary filter]
[Institution Type filter: All / School / College / Coaching]
```

This selection persists across tab navigation. "Viewing: **SSC CGL Mock 5** — 28 institutions — 14,280 students — Conducted 2026-03-15"

**Provisional results visibility:** Exam Selector shows exams with `exam_result_publication.status = PUBLISHED` regardless of `is_provisional` flag. F-08 renders data for the latest published result set. If result is PROVISIONAL: selector shows "[PROVISIONAL]" badge alongside exam name, and page header shows a persistent amber banner: "⚠️ Viewing provisional results — final results may differ after objection review." Analytics update automatically after results are re-published (post-rescore).

---

### KPI Strip (for selected exam)

| # | KPI | Notes |
|---|---|---|
| 1 | Institutions | Count of institutions with published results for this exam |
| 2 | Students Scored | Total result records (submitted) |
| 3 | Mean Score | Platform-wide mean across all institutions |
| 4 | Pass Rate | If pass mark defined; otherwise N/A |
| 5 | Item Analysis Available | ✅ if answer_key published + result computation complete; ❌ if not |
| 6 | Last Data Refresh | Memcached TTL indicator — "Data from {N} min ago" + [Refresh] |

---

### Tab 1 — Score Distribution

**Primary audience:** Results Coordinator (36) for result quality validation.

#### Section A — Platform-Wide Distribution

**Score Distribution Chart (Recharts `BarChart` — Histogram):**
- X axis: score ranges (0–10, 10–20, … up to max marks)
- Y axis: student count
- Colour: blue bars for normal distribution; amber for anomalous ranges
- Overlay: mean line (dashed blue) + pass mark line (dashed green if defined)

**Stat summary cards:**
- Mean, Median, Mode, Standard Deviation, Min, Max, P10, P25, P75, P90, P99

#### Section B — Institution Breakdown

**Table: Score Summary by Institution**

| Column | Sortable | Notes |
|---|---|---|
| Institution | Yes | Name + type |
| Students | Yes | Count |
| Mean Score | Yes | — |
| Median | Yes | — |
| Std Dev | Yes | — |
| Highest | Yes | — |
| Lowest | Yes | — |
| Pass Rate | Yes | If applicable |
| Anomaly | No | ⚠️ if institution mean is >2 SD from platform mean |

Click row → expands institution-specific score distribution chart below table.

#### Section C — Distribution Comparison

When ≥ 2 institutions selected (checkboxes in Section B table), shows overlaid `LineChart`:
- X: score ranges
- Y: percentage of students (normalized for fair comparison)
- One line per institution (up to 5 institutions at a time)

---

### Tab 2 — Item Analysis

**Primary audience:** Content Director (18) and SMEs for question quality review.

**Available only when:** answer key is FINAL + result computation is COMPLETED.

**D-09 taxonomy enrichment:** When question metadata is available from the question bank (Div D — D-09 Question Bank), F-08 joins it via `exam_item_analysis.question_bank_id`. If `question_bank_id = NULL` (legacy/imported paper, no bank linkage): D-09 columns show `—` with tooltip: "Metadata unavailable — question not linked to question bank." Content Director (18) can request bulk question linking from Div D to enable enrichment for future runs. There is no fuzzy-matching — only exact `question_bank_id` links are used.

#### Section A — Difficulty Index (p-value)

For each question, the proportion of students who answered correctly.

**Chart: Question Difficulty Bar (`BarChart`)**
- X: question number
- Y: p-value (0–1)
- Colour: 0–0.3 = Hard (red) · 0.3–0.7 = Medium (blue) · 0.7–1.0 = Easy (green)
- Reference lines: 0.3 and 0.7 boundaries shown as dashed
- **Mismatch indicators:** Questions where the D-09 tagged difficulty diverges from the computed p-value range are marked with ⚠️ (e.g., tagged "Easy" but p-value = 0.18 → computed "Hard"). These are the most actionable items for the content team.

**Interpretation guide (inline):**
- p < 0.30: Too hard — review question for ambiguity or unfair difficulty
- p > 0.80: Too easy — review for curriculum relevance or give-away wording
- p > 0.95: Possibly leaked or very commonly known fact

#### Item Difficulty Detail Table

Tabular companion to the chart. Each row is one question:

| Column | Notes |
|---|---|
| Q# | Question number |
| p-value | Computed difficulty index (0–1) |
| Computed Difficulty | Easy / Medium / Hard — derived from p-value ranges |
| Tagged Difficulty (D-09) | Easy / Medium / Hard — from question bank taxonomy; `—` if unavailable |
| Difficulty Match | ✅ Match / ⚠️ Mismatch — compares computed vs tagged |
| Topic | From D-09 taxonomy (e.g. "Algebra", "Polity"); `—` if unavailable |
| Subject | From D-09 taxonomy (e.g. "Mathematics", "GK"); `—` if unavailable |
| Correct Option | From answer key |
| Actions | [View Option Distribution] — expands Section C for this Q# |

**Sort by:** p-value (default ASC — hardest first), Mismatch (⚠️ first), Topic.

**Filter:** Show only mismatches toggle — "Show only difficulty-mismatch questions ({N})" — most useful starting point for content review.

#### Section B — Discrimination Index

For each question, does it differentiate between high-performing and low-performing students?

**Discrimination Index (D) formula:**
D = (% correct in top 27% scorers) - (% correct in bottom 27% scorers)

**Top/bottom 27% cohort edge cases:** Cohort size = `ceiling(total_valid_students × 0.27)` where `total_valid_students` excludes sessions with `rank = NULL` (timed out / no submission). If total valid students < 30: show ⚠️ "Insufficient data for reliable discrimination index ({N} valid submissions). Metric shown with caution." Chart still renders but bars are amber (unreliable data). For fractional cohort sizes, ceiling is applied (e.g., 100 students → top 27 students; 50 students → top 14 students).

**Chart: Discrimination Bar (`BarChart`)**
- X: question number
- Y: D value (-1 to +1)
- Colour: D < 0.20 = Poor (red) · D 0.20–0.40 = Fair (amber) · D > 0.40 = Good (green)
- D < 0: Negative discrimination (high scorers answer wrong) = serious question flaw

**Questions requiring review table:**
Auto-filtered list of questions where p < 0.20 OR D < 0.15 OR D < 0 (highest priority review needs).

**[Send to Content Team]** button: Creates a review request in Div D question bank (D-04/D-11) flagging listed questions for SME review. Opens modal to confirm and add notes.

#### Section C — Option Analysis (Distractor Analysis)

For each multiple-choice question, shows how students distributed across options.

Select a question from dropdown → shows:

```
Question 12: "Which of the following is NOT a primary colour?"

Option | Selected by | % of students
A      |     6,240   | 43.7%  ← CORRECT
B      |     4,180   | 29.3%
C      |     2,890   | 20.2%
D      |     980     |  6.8%

Distractor effectiveness: B and C are functioning distractors (≥15% each). D is weak (<10%).
```

**DPDPA:** Only aggregate percentages shown — no individual student data.

#### Section D — Section-Wise Performance

If the exam has sections (Math, Reasoning, General Knowledge, etc.):

| Section | Max Marks | Mean Score | Mean % | Difficulty |
|---|---|---|---|---|
| General Intelligence | 50 | 28.4 | 56.8% | Medium |
| General Awareness | 50 | 31.2 | 62.4% | Medium-Easy |
| Quantitative Aptitude | 50 | 19.8 | 39.6% | Hard |
| English Comprehension | 50 | 33.5 | 67.0% | Easy |

---

### Tab 3 — Institution Comparison

**Primary audience:** Results Coordinator, Analytics Manager (42).

**Purpose:** Cross-institution performance comparison for the same exam.

#### Comparison Chart

**Chart Type:** `BarChart` — mean score per institution (sorted by mean score, highest first). Horizontal chart with institution names on Y axis.

Colour-coded:
- Top quartile (top 25% of institutions): dark green
- Above average: light green
- Below average: amber
- Bottom quartile: red

Platform mean shown as a vertical dashed line.

**Toggle:** [Show as % of max marks] / [Show as raw marks]

#### Detailed Comparison Table

| Column | Sortable | Notes |
|---|---|---|
| Institution | Yes | — |
| Type | No | School / College / Coaching |
| Students | Yes | — |
| Mean Score | Yes | — |
| Mean % | Yes | — |
| Rank within Type | No | e.g. "3 of 28 coaching centres" |
| Platform Rank | Yes | Overall rank by mean score |
| Vs Platform Mean | No | "+5.2 pts above" / "-3.1 pts below" |
| Trend | No | ▲▼ vs same exam last time |

**[Export Comparison CSV]** — anonymised: institution names masked if privacy mode enabled. Platform Admin (10) sees full names; other roles see truncated names per DPDPA.

---

### Tab 4 — Trend Analysis

**Primary audience:** Analytics Manager (42), Results Coordinator (36).

**Purpose:** Track exam performance trends over multiple exam instances (across exam series / test series cycles).

#### Section A — Exam Series Selector

Select an exam type + institution (or "All institutions") → shows trend over multiple exam instances.

**Chart: `LineChart` — Mean Score Trend**
- X: exam instances (chronological)
- Y: mean score
- Multiple lines: one per institution (if "All") or platform mean + institution line
- Annotations: "New question paper set" events (when paper changed)

#### Section B — Participation Trend

`BarChart` — student count per exam instance. Shows if participation is growing or declining.

#### Section C — Pass Rate Trend

`LineChart` — pass rate per exam instance over time (if pass mark defined).

#### Section D — Subject Performance Trend

For exams with sections: stacked line chart showing each section's mean score trend over time. Helps identify if one subject area is consistently weak.

---

## 5. Export Modal

**Trigger:** [Export] button in page header

**Available exports:**

| Export Type | Format | Contents |
|---|---|---|
| Score Summary | CSV | Institution, student count, mean, median, std dev, pass rate |
| Score Distribution | CSV | Score range, student count (aggregated — no individual rows) |
| Item Analysis | CSV | Question number, p-value, D value, correct option, option distribution |
| Full Analytics Report | PDF | All tabs as formatted report: charts as images + tables |

**Note:** No individual student records exported from this page. All exports are aggregated. DPDPA compliance is enforced at data model level — individual result records require separate access through F-04 review (which shows only anonymised refs).

**File expiry:** Exports available for 15 minutes via presigned S3 URL.

---

## 6. Data Model Reference

F-08 reads from:
- `exam_result` (tenant schema) — aggregated via Celery pre-computed views
- `exam_result_computation` — computation metadata
- `exam_answer_key_entry` — for item analysis
- `exam_schedule` — for exam metadata

**`exam_analytics_aggregate`** (pre-computed by Celery after F-04 publish):
| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `exam_schedule_id` | FK → `exam_schedule` | OneToOne per exam |
| `mean_score` | decimal | — |
| `median_score` | decimal | — |
| `std_dev` | decimal | — |
| `min_score` | decimal | — |
| `max_score` | decimal | — |
| `p10` | decimal | 10th percentile |
| `p25` | decimal | — |
| `p75` | decimal | — |
| `p90` | decimal | — |
| `p99` | decimal | — |
| `pass_rate` | decimal | Nullable |
| `score_distribution` | jsonb | `[{"range": "0-10", "count": 120}, ...]` |
| `computed_at` | timestamptz | — |

Celery task `compute_exam_analytics_aggregate` runs after `publish_exam_results`.

**`exam_item_analysis`** (per question, per exam):
| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `exam_schedule_id` | FK → `exam_schedule` | — |
| `question_number` | int | — |
| `p_value` | decimal | Difficulty index 0–1 |
| `discrimination_index` | decimal | D value -1 to +1 |
| `option_distribution` | jsonb | `{"A": 0.44, "B": 0.29, "C": 0.20, "D": 0.07}` |
| `top_27_p_value` | decimal | For D computation |
| `bottom_27_p_value` | decimal | For D computation |
| `question_bank_id` | FK → question_bank (nullable) | Linked question bank entry from D-09; NULL if no bank linkage |
| `tagged_difficulty` | varchar(10) | Nullable — from D-09: `EASY` · `MEDIUM` · `HARD` |
| `topic` | varchar(100) | Nullable — from D-09 taxonomy (e.g. "Number System") |
| `subject` | varchar(100) | Nullable — from D-09 taxonomy (e.g. "Mathematics") |
| `difficulty_mismatch` | boolean | True when `tagged_difficulty` ≠ computed difficulty range from `p_value`; NULL if `tagged_difficulty` is NULL |

Celery task `compute_item_analysis` runs after answer key is FINAL + results computed. When computing, it joins `exam_answer_key_entry → question_bank` (if linked) to populate D-09 metadata fields.

---

## 7. Access Control

| Gate | Rule |
|---|---|
| Page access | Results Coordinator (36), Analytics Manager (42), Content Director (18), Ops Manager (34), Config Specialist (90), Platform Admin (10) |
| All tabs read | All above roles |
| [Send to Content Team] action | Results Coordinator (36), Content Director (18), Platform Admin (10) |
| [Export] | All roles with page access |
| Full institution name in exports | Platform Admin (10) only; others see truncated names |
| No write actions on this page | All roles — F-08 is read-only |

---

## 8. Edge Cases & Error States

| Scenario | Behaviour |
|---|---|
| Item analysis not available (answer key not FINAL) | Tab 2 shows: "Item analysis requires a finalized answer key. Publish and finalize the answer key in F-05, then re-run computation." Tab header shows ⚠️ badge. |
| Exam with only 1 student | Statistical charts render but with warning: "⚠️ Insufficient data ({N} students) for reliable statistical analysis." Charts still shown. |
| Score distribution heavily skewed (>80% at max score) | Amber indicator: "⚠️ Unusual distribution — most students scored maximum marks. Review question difficulty or check for answer key error." Links to F-05. |
| Analytics aggregate not yet computed | Tab 1 shows: "Analytics being computed… (usually available within 5 minutes of result publication)" with spinner. Page polls `?part=kpi` every 30s to detect when ready. |
| Score distribution changes after answer key revision (rescore) | After accepted objection → rescore → re-publish (F-05 → F-04): Celery chain re-triggers `compute_exam_analytics_aggregate`. Memcached entry for this exam is invalidated. F-08 shows [Refresh] button if data is > 5 minutes old. On [Refresh]: clears Memcached, re-renders all tabs from fresh aggregate. |
| Trend analysis exam series matching | Exams grouped by `exam_id` for trend calculation. If `paper_id` changes between instances (e.g., new question set each year): both instances included in trend line with annotation marker: "New paper set at this instance." Allows multi-year comparison while flagging paper difficulty shifts. |
| No exams with published results | Empty state on exam selector: "No published results yet. Publish results in F-04 to view analytics." |
| Item analysis sends to Content Team but question already under review | Create request in D-04 still proceeds; D-04 deduplication handles it (existing review flag + new analytics flag merged). |

---

## 9. UI Patterns

### Caching Strategy

| Data | Cache TTL | Invalidation |
|---|---|---|
| `exam_analytics_aggregate` | Memcached 30 min | On `publish_exam_results` task complete |
| `exam_item_analysis` | Memcached 60 min | On `compute_item_analysis` task complete |
| Score distribution chart data | Memcached 30 min | — |
| Institution comparison table | Memcached 30 min | — |

### Toasts

| Action | Toast |
|---|---|
| [Refresh] clicked | ℹ️ "Refreshing analytics data…" (6s) |
| [Send to Content Team] | ✅ "Review request sent to Content team (Div D)" (4s) |
| Export ready | ✅ "Export ready — download starts in 3s" (auto-download) |
| Cache miss (loading) | ℹ️ "Loading analytics — this may take a moment" (info banner, not toast) |

### Loading States

- Charts: grey placeholder rectangle with "Loading data…" text + spinner
- Tables: 8-row shimmer
- KPI strip: 6 tile shimmers

### Responsive

| Breakpoint | Behaviour |
|---|---|
| Desktop (≥1280px) | Side-by-side stat cards + full chart; institution table full columns |
| Tablet | Stat cards scroll horizontal; chart full-width; table reduced columns |
| Mobile | Stat cards stacked; charts full-width (scroll if long); table = key stats only (mean + pass rate) |

---

*Page spec complete.*
*F-08 covers: score distribution analysis → item analysis (difficulty, discrimination, distractor + D-09 tagged difficulty / topic mismatch detection) → institution comparison → trend over exam series. Read-only. Feeds back to Div D question quality review.*
