# D-13 — Content Quality Analytics

> **Route:** `/content/analytics/quality/`
> **Division:** D — Content & Academics
> **Primary Role:** Content Director (18) — full access
> **Scoped Access:** Question Reviewer (28) — own metrics only (ORM-scoped)
> **File:** `d-13-quality-analytics.md`
> **Priority:** P2 — Once > 500 questions published — patterns become meaningful
> **Status:** ⬜ Not started
> **Amendments:** G6 (Difficulty Calibration tab — realized vs tagged difficulty from Div F exam performance data)

---

## 1. Page Name & Route

**Page Name:** Content Quality Analytics
**Route:** `/content/analytics/quality/`
**Part-load routes:**
- `/content/analytics/quality/?part=sme-table` — SME quality table
- `/content/analytics/quality/?part=reviewer-table` — reviewer performance table
- `/content/analytics/quality/?part=pipeline-age` — pipeline age distribution histogram
- `/content/analytics/quality/?part=post-publish-issues` — post-publish issues table
- `/content/analytics/quality/?part=difficulty-calibration` — difficulty calibration tab (G6)
- `/content/analytics/quality/?part=trend-charts` — 12-month rolling trend charts
- `/content/analytics/quality/?part=ai-quality` — AI vs human quality comparison

---

## 2. Purpose (Business Objective)

Production volume without quality measurement produces noise, not content. D-13 converts pipeline data and exam performance data into actionable quality intelligence for the Content Director.

Three quality dimensions are tracked here:

**Upstream quality (SME):** Return rate, error type breakdown, revision cycles per question, time to publish. A high return rate for a specific SME indicates a calibration problem — not necessarily a bad SME, but possibly a mismatch between what they think "Medium difficulty" means and what the style guide says.

**Pipeline quality (Reviewer):** Throughput, return rate, return reason distribution. A Reviewer who never returns questions (0% return rate) is either reviewing very high-quality content or not reviewing carefully enough. A Reviewer with 80% return rate may be applying non-standard criteria.

**Post-publish quality (from Div F exam results — G6):** Realized difficulty (% students correct) vs tagged difficulty. This is the ultimate quality signal — it comes from actual student performance, not human judgment. A question tagged "Medium" that 88% of students answered correctly was effectively an "Easy" question, and the difficulty tag should be corrected.

**Business goals:**
- Give Content Director data-driven insight into SME quality patterns
- Surface Reviewer performance anomalies before they become systemic issues
- Identify and resolve difficulty calibration errors using real student performance data (G6)
- Track AI-generated question quality vs human-authored quality
- Enable export to CSV for management reporting

---

## 3. User Roles

| Role | Access |
|---|---|
| Content Director (18) | Full — all tabs, all SMEs and Reviewers visible, all filters available |
| Question Reviewer (28) | Own metrics only — sees only the Reviewer Performance Table filtered to their own data. All SME Quality Table data, other reviewers' data, and Director-level views are hidden. |

---

## 4. Section-Wise Detailed Breakdown

---

### Section 1 — Page Header & Filters

- H1: "Content Quality Analytics"
- Global filter bar (applies to all tabs unless overridden per tab):
  - Subject (multi-select)
  - Date range (default: last 90 days)
  - Source: Human / AI / AI-Edited / Bulk Import / All
- "Export Data" button (Director only) — exports currently visible tab data to CSV

---

### Section 2 — Tab Navigation

| Tab | Description |
|---|---|
| SME Quality | Per-SME quality breakdown |
| Reviewer Performance | Per-reviewer throughput and quality |
| Pipeline Age | Distribution histogram — where questions accumulate |
| Post-Publish Issues | Questions unpublished post-publish — reason analysis |
| Difficulty Calibration (G6) | Realized vs tagged difficulty from Div F exam data |
| Trend Charts | 12-month rolling key metrics |
| AI vs Human Quality | Comparative quality for AI-generated questions |

---

### Section 3 — Tab: SME Quality

**Purpose:** Per-SME quality metrics — return rate, error types, review cycles.

**Table columns (Content Director view — all SMEs):**

| Column | Description |
|---|---|
| SME | Role label ("GK SME") — not personal name (DPDPA) |
| Subject | — |
| Questions Authored (period) | COUNT in selected date range (all states) |
| Published (period) | COUNT that reached PUBLISHED state |
| Return Rate | (returned / submitted) × 100% — amber if > 30% · red if > 50% |
| Avg Review Cycles | Average number of times a question was returned before approval (1.0 = never returned · 2.0 = returned once on average) |
| Error Type Breakdown | Expandable sparkline: Factual vs Language vs Formatting vs Duplicate vs Off-Syllabus vs Other — click to expand to full count table |
| Avg Days Draft to Publish | Average total days from first save-draft to PUBLISHED state |
| Published Lifetime | All-time published count |

**"Error Type Breakdown" expanded view:**
Opens a small inline panel below the SME row showing:
- Bar chart: each return reason category with count + % of total returns
- Trend: is Factual Error increasing or decreasing over the last 3 months?
- "Most common error this period": e.g. "Language/Grammar ×47 (38% of all returns)"

This data surfaces patterns like: "GK SME's returns are 70% Factual Error — they may need a refresher on Current Affairs verification process" or "Math SME's returns are 80% Formatting — they may need help with LaTeX standards (see D-09 Style Guide)."

**Question Reviewer view (own metrics only):**
Reviewer accesses this tab but sees only their own data, not a table of all SMEs. Their view shows their personal quality impact: "Questions you reviewed: 234 · Pass rate: 67% · Return rate: 33% · Top return reason: Incomplete Explanation ×31." This is provided for Reviewer self-awareness, not management surveillance.

---

### Section 4 — Tab: Reviewer Performance

**Purpose:** Per-reviewer throughput, consistency, and quality impact.

**Table columns:**

| Column | Description |
|---|---|
| Reviewer | Role label |
| Questions Reviewed / Day (7d avg) | Throughput indicator |
| Avg Time Per Question | Minutes from assign to decision — amber if > 30 min (may indicate low engagement or very complex questions) |
| Pass-to-Approver Rate | (passed / reviewed) × 100% |
| Return-to-SME Rate | (returned / reviewed) × 100% |
| Return Reason Distribution | Same expandable sparkline as SME Quality tab |
| Questions Currently Assigned | Live count from D-03 |
| Oldest Current Item Age | Days — red if > SLA |

**Anomaly indicators:**
- Return rate = 0%: yellow note "This reviewer has returned 0 questions in the last 30 days — verify review quality."
- Return rate > 70%: red note "High return rate — may indicate overly strict criteria or SME quality issue in assigned subject."
- Avg time per question > 60 min: amber "Unusually high review time — may be working on complex committee questions or have a heavy queue."

**Zero-division edge cases — Reviewer Performance Tab:**

All rate and average calculations in this tab must handle the case where a reviewer has reviewed zero questions in the selected period. Division-by-zero produces NaN or infinity — shown in the UI as "—" (em dash) to indicate "no data" rather than 0%.

| Metric | Zero-division scenario | Display |
|---|---|---|
| Pass-to-Approver Rate | reviewer reviewed 0 questions | "—" (not "0%") |
| Return-to-SME Rate | reviewer reviewed 0 questions | "—" (not "0%") |
| Questions Reviewed / Day | period has 0 working days or reviewer has 0 reviews | "—" |
| Avg Time Per Question | reviewer has 0 completed reviews | "—" |
| Inter-Reviewer Agreement Rate | < 2 questions with both reviewers' decisions | "—" (insufficient data) |
| Calibration Score (D-13 health summary) | 0 published questions with performance data | "Insufficient data — calibration score requires at least 30 questions with exam results" |

These "—" values are excluded from averages when computing platform-wide aggregates. A reviewer who reviewed 0 questions does NOT drag down the platform average review rate — they are omitted from the denominator.

**Anomaly: reviewer reviewed 0 questions for ≥ 7 days (while not OOO):**
An additional amber anomaly indicator appears: "No reviews in {N} days — is this reviewer active? Check D-15 for OOO status or queue issues."

---

### Section 5 — Tab: Pipeline Age Distribution

**Purpose:** Histogram showing how old the questions currently in each pipeline stage are — reveals bottlenecks.

**Two histograms:**

**Histogram 1: Days in Review (UNDER_REVIEW questions)**
X-axis: 0–1 days / 1–2 days / 2–3 days / 3–5 days / 5–7 days / >7 days
Y-axis: Question count per bucket
Colour: Green ≤ SLA · Amber approaching SLA · Red past SLA
Subject breakdown: Stacked bar per bucket showing which subjects contribute

**Histogram 2: Days in Approval (PENDING_APPROVAL questions)**
Same structure — X-axis: 0–1 / 1–2 / 2–3 / >3 days
Approver SLA: 2 days standard, same-day for amendments

**Bottleneck interpretation panel (below histograms):**
Auto-generated insight: "The largest accumulation of questions (143) is in the 3–5 day review bucket for Mathematics. Review SLA is 3 days. Consider reviewing D-15 reviewer assignments to add backup capacity for Mathematics."

---

### Section 6 — Tab: Post-Publish Issues

**Purpose:** Questions that were published and then unpublished — why did they get through both review gates?

**Table columns:**

| Column | Description |
|---|---|
| Month | — |
| Questions Unpublished | COUNT |
| Reason Distribution | Paper Leak / Factual Error / Student Flags / Copyright / Other — bar chart |
| SME Distribution | Which SMEs' questions were unpublished (role labels) |
| Reviewer at Time | Which reviewer had passed these questions (role label) — not personal name |
| Avg Time Published to Unpublish | Days between publish and unpublish — a short time suggests systematic error |

**Month-over-month trend:** Line chart of unpublish rate (unpublished / total published that month). Amber if > 1% · Red if > 3%.

**Drill-down:** Click any month row → shows individual unpublished questions with full D-12 links. Director can review each question's audit trail to understand why the error was missed.

---

### Section 7 — Tab: Difficulty Calibration (Amendment G6)

**Purpose:** The definitive answer to "Is our difficulty tagging accurate?" — using actual student performance data from Div F exam results.

**Data source:** `content_question_performance` table (populated by Celery after each exam result publication — same source as D-01 Performance Data tab).

**Difficulty Calibration Table:**

| Column | Description |
|---|---|
| Question ID (short) | UUID first 8 chars — click → D-12 audit trail |
| Subject | — |
| Topic | — |
| Tagged Difficulty | Easy / Medium / Hard — what the SME assigned |
| Realized Difficulty | Derived from % correct: ≥ 70% = Easy · 40–69% = Medium · < 40% = Hard |
| % Correct | Raw percentage — bar fill |
| Divergence | |Tagged - Realized| in % points |
| Discrimination Index | ≥ 0.40 = Excellent · 0.20–0.39 = Acceptable · < 0.20 = Poor |
| Student Count | How many students answered this question |
| Action (Approver only) | "Re-Tag Difficulty" button |

**Filter: Divergence ≥ 20%** (default — shows only the miscalibrated questions). Threshold adjustable.

**"Re-Tag Difficulty" button (Approver only):**
Opens a compact inline form:
- Current tag: Medium
- Realized performance: 89% correct → effectively Easy
- New tag selector: Easy / Medium / Hard (pre-selected to match realized difficulty)
- "Apply Re-Tag" → updates `content_question.difficulty` + D-12 audit entry `action: TagAmendment` + invalidates Memcached aggregate cache

This action can be done directly from D-13 — no navigation to D-11 needed. Designed for bulk calibration sessions where the Approver works through the divergence list and corrects tags systematically.

**Calibration Health Summary (top of tab):**
- Total published questions with performance data: {N}
- Questions with divergence > 20%: {N} ({N}%) — amber if > 10%, red if > 20%
- **Calibration Score:** Average `|tagged_difficulty_numeric - realized_difficulty_numeric|` across all questions with performance data.
  - Numeric mapping: Easy = 1 · Medium = 2 · Hard = 3
  - Formula: `Calibration Score = mean(|tagged - realized|)` across N questions
  - Range: 0.0 (perfect calibration) → 2.0 (maximum miscalibration — every Easy tagged as Hard or vice versa)
  - **Benchmarks (sourced from D-20 Reviewer Performance Targets — used as a proxy for content quality targets):**
    - 0.00–0.15: 🟢 Excellent — tagging is highly accurate
    - 0.16–0.30: 🟡 Acceptable — minor systematic bias; review SME difficulty rubric
    - 0.31–0.50: 🟠 Needs Attention — significant bias; SME training recommended
    - > 0.50: 🔴 Poor — systematic miscalibration; Director review + possible SME quota freeze
  - **Zero-division edge case:** If fewer than 30 questions have performance data, calibration score is suppressed and replaced with: "Insufficient data — requires at least 30 questions with exam results. Currently: {N}."
  - **Calibration Score link:** "What does this mean? →" tooltip explaining the formula and benchmark ranges in plain language.
- "SME with highest avg divergence": [SME role] — [avg divergence %] — Director can then review that SME's difficulty rubric understanding. If all SMEs have 0 questions with performance data: shows "—" instead of an SME label.

**Discrimination Index Alert Panel:**
Questions with discrimination index < 0.20 (poor discriminator):
- These questions do not help separate high-scoring students from low-scoring ones
- Could indicate the question is trivially easy (answered correctly by almost everyone) or poorly written
- Listed separately from divergence — a question can have correct difficulty tag but still be a poor discriminator
- Director can flag these for SME revision (D-01 announcement G11) or Approver can unpublish (D-04) if quality is deemed insufficient

---

### Section 8 — Tab: Trend Charts

**Purpose:** 12-month rolling view of key quality metrics — identify improving or deteriorating trends before they become crises.

**Charts (all 12-month rolling, monthly data points):**

1. **Publication Rate** — questions published per month (total + by subject)
2. **Return Rate** — (returned / submitted) per month — should be declining as SME quality improves
3. **AI Acceptance Rate** — D-08 acceptance rate per month — plateau or decline indicates prompt quality issues
4. **Average Review Cycle Time** — mean days from submit to published, per month
5. **Post-Publish Issue Rate** — unpublished questions as % of published, per month

**Anomaly markers:** Spike events marked with vertical lines and labels (e.g. "New GK SME onboarded" · "AI prompt updated to v1.4.2" · "Major exam period — high volume").

Director can add custom annotations to explain anomalies — "New subject added to bank" or "SME training workshop conducted." Annotations stored in `content_analytics_annotations`.

---

### Section 9 — Tab: AI vs Human Quality

**Purpose:** Comparative quality analysis for AI-generated content vs human-authored content — tracks whether the AI pipeline is improving or degrading content quality.

**Side-by-side comparison table:**

| Metric | Human-Authored | AI-Generated | AI-Edited |
|---|---|---|---|
| Return Rate in Review | % | % | % |
| Avg Review Cycles | N | N | N |
| Post-Publish Issue Rate | % | % | % |
| Avg Realized Difficulty Divergence | % | % | % |
| Avg Discrimination Index | N | N | N |

**Interpretation:** If AI-generated questions have a significantly higher post-publish issue rate or difficulty divergence than human-authored questions, the AI pipeline's rejection thresholds in C-15 should be tightened. If AI-Edited questions perform similarly to human-authored, the Edit+Accept workflow in D-08 is working effectively.

**Trend: AI acceptance rate vs AI post-publish issue rate:**
Line chart — if acceptance rate increases (less strict triage) while post-publish issue rate also increases, the triage is being too permissive. If both decline, the AI pipeline quality is genuinely improving.

---

## 5. Data Models

D-13 is a read-heavy analytics page — it reads from existing tables without creating new ones (except annotations):

**Reads from:**
- `content_question` (state, author, subject, created_at, revision_count)
- `content_question_audit_log` (all state transitions for pipeline age calculations)
- `content_question_review_log` (reviewer decisions, return reasons, review times)
- `content_question_performance` (Div F exam performance data — for G6 difficulty calibration)
- `content_ai_triage_log` (AI acceptance rate data from D-08)

### `content_analytics_annotations`
| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `annotation_date` | date | Which month the annotation applies to |
| `annotation_text` | varchar(300) | Short explanation of anomaly |
| `created_by` | FK → auth.User | Director |
| `created_at` | timestamptz | — |

---

## 6. Access Control

| Gate | Rule |
|---|---|
| Page access | `PermissionRequiredMixin(permission='content.view_quality_analytics')` — Roles 18 + 28 |
| Content Director | Full access to all tabs, all roles' data |
| Question Reviewer | ORM-scoped: all queries filtered to `actor_id = request.user.id` for reviewer-specific data. Reviewer Performance tab shows only own row. SME Quality tab: not shown (403 on the part-route). |
| Difficulty Re-Tag action (G6) | `permission='content.publish_question'` — Role 29 only. Button hidden for other roles. |
| Export | Role 18 only |

---

## 7. Edge Cases & Error States

| Scenario | Behaviour |
|---|---|
| Performance data from Div F not yet available (platform launched < 1 month ago) | Difficulty Calibration tab shows: "No student performance data available yet. This tab will populate after your published questions are used in graded exams and results are published." |
| A question has performance data from < 50 students | Excluded from Difficulty Calibration table by default (filter: min 50 students). Director can lower the threshold in the filter. |
| SME account deactivated — still has historical data | Analytics shows historical data for deactivated SMEs with a "[Former]" prefix on the role label: "[Former] GK SME." Data remains — the analytics period pre-dates the deactivation. |
| AI vs Human Quality tab has no AI questions yet | Tab shows: "No AI-generated questions have been published yet. This tab will populate once D-08 AI triage accepts questions that complete the review pipeline." |
| HTMX part-load for trend charts takes > 3s | Charts show a loading skeleton. If > 5s: "Analytics data is taking longer than expected. Data may be refreshing." with a Retry button. Underlying ORM query is a GROUP BY aggregation on large tables — query plan is DBA-reviewed (C-11 slow query log). |

---

## 8. Integration Points

| Integration | Direction | What Flows | Mechanism |
|---|---|---|---|
| Div F Exam Results | Div F → D-13 | `content_question_performance` table (% correct, discrimination index) | Celery `sync_question_performance` task after each exam result event |
| D-12 Audit History | D-12 → D-13 | TagAmendment events from D-12 feed the difficulty calibration history | `content_question_audit_log` ORM read |
| D-08 AI Triage | D-08 → D-13 | Acceptance rate, rejection reasons per batch | `content_ai_triage_log` ORM read |
| D-11 Published Bank | D-13 → D-11 | Difficulty Re-Tag from calibration tab triggers D-12 audit entry (same as D-11 → D-12 flow) | Direct `content_question.difficulty` update + `content_question_audit_log` INSERT |
| D-01 SME Dashboard | D-13 (G6) → D-01 | Divergent questions surfaced in D-01 Performance Data tab | Same `content_question_performance` table — different view |

---

---

## 9. UI Patterns & Page-Specific Interactions

### Search
- **SME Quality tab:** Placeholder "Filter by SME role or subject…". Instant filter by role label + subject (typically < 15 rows).
- **Reviewer Performance tab:** Placeholder "Filter by reviewer role…". Instant filter by role label.
- **Post-Publish Issues tab:** Placeholder "Filter by month or subject…". Searches: month label, subject name.
- **Difficulty Calibration tab:** Placeholder "Search by topic or question ID…". Searches: topic name, question UUID (short).
- No search bar on Pipeline Age tab (histogram view, not a table).

### Sortable Columns — SME Quality Table
| Column | Default Sort |
|---|---|
| Return Rate | **DESC (highest first)** — default |
| Questions Authored | DESC |
| Avg Review Cycles | DESC |
| Avg Days Draft to Publish | DESC |
| Published Lifetime | DESC |

### Sortable Columns — Reviewer Performance Table
| Column | Default Sort |
|---|---|
| Questions Reviewed/Day | **DESC** — default |
| Return Rate | DESC |
| Avg Time Per Question | DESC |
| Oldest Current Item Age | DESC |

### Sortable Columns — Difficulty Calibration Table
| Column | Default Sort |
|---|---|
| Divergence | **DESC (highest first)** — default |
| % Correct | ASC |
| Student Count | DESC |
| Discrimination Index | ASC |

### Pagination
- SME Quality table: typically < 15 rows — show all, no pagination.
- Reviewer Performance table: typically < 10 rows — show all.
- Post-Publish Issues table: 25 rows, numbered controls (monthly data, typically < 24 months).
- Difficulty Calibration table: 50 rows, numbered controls (can have thousands of divergent questions at 2M+ bank size).

### Empty States
| Tab | Heading | Subtext |
|---|---|---|
| SME Quality — no data | "No SME data yet" | "SME quality metrics appear after questions enter the review pipeline." |
| Reviewer Performance — no data | "No reviewer data yet" | "Reviewer metrics appear after the first review decisions are made." |
| Difficulty Calibration — no data | "No performance data yet" | "This tab populates after published questions are used in graded exams and results are published." |
| Difficulty Calibration — no divergent questions | "Calibration looks good ✓" | "No questions have a divergence ≥ {threshold}% between tagged and realized difficulty." |
| AI vs Human — no AI questions | "No AI-generated questions published yet" | "This tab populates after D-08 AI triage accepts questions that complete the review pipeline." |
| Trend Charts — insufficient data | "Not enough data for trend view" | "Trend charts require at least 2 months of production data." |

### Toast Messages
| Action | Toast |
|---|---|
| Difficulty Re-Tag from Calibration tab | ✅ "Difficulty updated — audit entry created" (Success 4s) |
| Export tab data to CSV | ℹ "Export started — download link will appear when ready" (Info 6s) |
| Annotation saved (Trend Charts) | ✅ "Annotation saved" (Success 4s) |
| Annotation deleted | ✅ "Annotation removed" (Success 4s) |
| Error type breakdown expand | No toast — expands inline |

### Loading States
- All tabs: tab-content skeleton on tab switch (table skeleton for data tabs, chart skeleton for chart tabs).
- SME Quality / Reviewer tables: 6-row skeleton.
- Difficulty Calibration table: 8-row skeleton + Calibration Health Summary shimmer bar at top.
- Trend Charts: chart-area shimmer rectangle (full height). Timeout > 5s: "Analytics data is taking longer than expected. [Retry]".
- Pipeline Age histograms: histogram-shaped shimmer (bars at varying heights).

### Responsive Behaviour
| Breakpoint | Behaviour |
|---|---|
| Desktop | All tabs full-width. Charts at full resolution. Expandable sparklines inline. |
| Tablet | Charts: reduced height (60% of desktop). Tables: priority columns + row expand. Sparkline expands as bottom sheet. |
| Mobile | Tab nav: horizontal scroll. Charts: single-series at a time (legend toggles active series). Tables: 3 columns + tap-to-expand. Difficulty Re-Tag form: full-width bottom sheet. |

### Charts (tab-specific)
- **SME Quality — Error Type Breakdown:** Expandable horizontal bar chart per SME row (Factual/Language/Formatting/Duplicate/Off-Syllabus). Collapse after expand via chevron.
- **Reviewer Performance — Return Reason Distribution:** Same expandable bar chart per reviewer.
- **Pipeline Age:** Dual histograms (Days in Review + Days in Approval). Stacked bars by subject. Colour: green ≤ SLA, amber approaching, red past. Hover tooltip: "{count} questions in {subject} — {N} days in review".
- **Post-Publish Issues:** Line chart of unpublish rate % over months. Red threshold line at 3%.
- **Trend Charts:** Multi-series line chart. 12 months on X-axis. Anomaly markers: vertical dashed lines with hover label. Director can click any point to see annotation (or add one).
- **AI vs Human:** Grouped bar chart (Human / AI-Generated / AI-Edited) per metric row.

### Role-Based UI
- Reviewer (28): sees only their own row in Reviewer Performance table (ORM-scoped). SME Quality tab not rendered (403 on part-route). All other tabs not visible.
- Director (18): full access all tabs.
- "Difficulty Re-Tag" button in Calibration tab: Approver (29) only. Director sees a "View in D-11" link instead.
- Export CSV button: Director only.

---

*Page spec complete.*
*Amendments applied: G6 (Difficulty Calibration tab — realized vs tagged difficulty from Div F exam results + Approver re-tag action from this tab)*
*Gap amendments: Gap 21 (Zero-division edge cases — Reviewer Performance Tab metric table, "—" display instead of 0%, excluded from platform averages, 7-day inactivity anomaly) · Gap 21 (Calibration score benchmark definition — 0.0–2.0 range, 4 benchmark tiers, formula documented, 30-question minimum, link to D-20 targets)*
*Next file: `d-14-syllabus.md`*
