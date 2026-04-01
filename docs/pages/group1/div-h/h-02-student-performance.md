# H-02 — Student Performance Analytics

> **Route:** `/analytics/students/`
> **Division:** H — Data & Analytics
> **Primary Role:** Analytics Manager (42) — platform-level trends; Data Analyst (44) — deep investigation
> **Supporting Roles:** Platform Admin (10) — full
> **File:** `h-02-student-performance.md`
> **Priority:** P1 — daily use for tracking platform learning outcomes

---

## 1. Page Name & Route

**Page Name:** Student Performance Analytics
**Route:** `/analytics/students/`
**Part-load routes:**
- `/analytics/students/?part=summary-bar` — top-level stat bar
- `/analytics/students/?part=score-distribution` — score histogram
- `/analytics/students/?part=subject-heatmap` — subject performance heatmap
- `/analytics/students/?part=cohort-chart` — retention cohort chart
- `/analytics/students/?part=domain-breakdown` — domain breakdown table
- `/analytics/students/?part=dropout-signals` — dropout risk panel

---

## 2. Purpose

H-02 gives the data team deep visibility into how **students are performing across the platform** — not at the individual level (DPDPA-compliant, no individual student PII) but at aggregate, cohort, domain, and institution-type levels.

**Key questions this page answers:**
- Are students improving over time within a domain?
- Which subjects consistently have low pass rates?
- What's the 3-month retention rate for students who first took an SSC exam in September?
- Is there a score gap between school students and coaching centre students?
- Which exam types have high abandonment (started but never completed)?
- Are students improving on re-attempts, or showing no learning signal?

**Who needs this page:**
- Analytics Manager (42) — trend reporting, leadership briefs
- Data Analyst (44) — deep investigations, dropout intervention proposals

**Privacy:** All data aggregated — no individual student IDs, names, or personal details. DPDPA compliant. Minimum cohort size = 30 students before a data point is shown (to prevent de-anonymisation of small groups).

---

## 3. Layout

```
┌────────────────────────────────────────────────────────────────────┐
│  Page header: "Student Performance Analytics"  [Export Report]    │
│  Filters: Period | Domain | Institution Type | Region | Tier      │
├────────┬────────┬────────┬────────┬────────┬────────┬─────────────┤
│ Total  │ Unique │ Avg    │ Pass   │ Avg    │ Re-    │ Abandonment │
│ Attempts│Students│ Score │ Rate   │ Attempts│attempt │ Rate        │
│ (period)│(period)│       │        │/Student│ Rate   │             │
├────────┴────────┴────────┴────────┴────────┴────────┴─────────────┤
│  Score Distribution Histogram  │  Subject Performance Heatmap     │
│  (10-percentile buckets)       │  (Subject × Score Band grid)     │
├────────────────────────────────┴────────────────────────────────────┤
│  Cohort Retention Chart (12-month waterfall)                       │
├────────────────────────────────┬────────────────────────────────────┤
│  Domain Breakdown Table        │  Dropout Risk Signals Panel       │
│  (6 rows)                      │                                    │
└────────────────────────────────┴────────────────────────────────────┘
```

---

## 4. Section-Wise Detailed Breakdown

---

### Section A — Filters

All filters persist in URL query params. Changing any filter refreshes all sections via HTMX partial swaps.

| Filter | Control | Notes |
|---|---|---|
| Period | Date range picker: Last 7D / 30D / 90D / 6M / 1Y / Custom | Defaults to Last 30D |
| Exam Domain | Multiselect: All / SSC / RRB / NEET / JEE / AP Board / TS Board | — |
| Institution Type | Multiselect: All / School / College / Coaching | — |
| Region / State | Select: All / State list | Institution's registered state |
| Subscription Tier | Multiselect: All / Starter / Standard / Professional / Enterprise | — |

Active filters shown as dismissible chips below the filter bar. [Reset All Filters] link.

---

### Section B — Summary Stat Bar

Seven tiles. All values computed from `analytics_daily_snapshot` for the selected period and filters.

| Tile | Description | Colour Rule |
|---|---|---|
| Total Attempts | Sum of all exam attempts in period | Neutral |
| Unique Students | Students who attempted ≥1 exam (distinct count) | Neutral |
| Avg Score % | Mean score across all attempts | Green ≥55%; Amber 45–55%; Red <45% |
| Pass Rate | % attempts scoring above domain pass threshold | Green ≥60%; Amber 40–60%; Red <40% |
| Avg Attempts/Student | `total_attempts ÷ unique_students` — measures engagement depth | Green >1.5; Neutral 1.0–1.5; Amber <1.0 |
| Re-attempt Rate | % of exam enrollments where the student had a prior attempt on the same exam type (computed cohort-wide: `multi_attempt_enrollments ÷ total_enrollments`). Source: `analytics_daily_snapshot` metric_key=`re_attempt_rate`, dimension=exam_domain. | Green >40%; Amber 20–40%; Red <20% (low re-engagement) |
| Abandonment Rate | Attempts started but never submitted ÷ total starts | Green <5%; Amber 5–15%; Red >15% |

---

### Section C — Score Distribution Histogram

**Purpose:** Shows how scores are distributed across all attempts in the selected period/filters. A healthy distribution shows a bell curve centred around 55–65%. A left-skewed distribution signals the exam bank may be too hard (or a specific topic is poorly taught). A right-skewed distribution signals too easy.

**Implementation:** Chart.js Bar chart. X-axis: score buckets (0–10%, 10–20%, ..., 90–100%). Y-axis: number of attempts (left) + cumulative % line (right axis).

```
        Score Distribution — Last 30 Days (SSC Domain, All Institution Types)

 15,400 │          ████
 12,000 │        ████████                         ─── cumulative %  100%
  8,000 │      ████████████                                          75%
  4,000 │    ████████████████                                        50%
  1,200 │  ████████████████████                                      25%
        │──────────────────────────────────────────────────────────
         0  10  20  30  40  50  60  70  80  90  100   Score %
```

**Annotation line:** Vertical dashed line at the domain pass threshold. Label: "Pass threshold: {N}%".

**Tooltip on hover:** Shows count + % of total for that bucket + cumulative % up to this bucket.

**Comparison mode:** Toggle [Compare to previous period] adds a grey outline bar series for the previous equivalent period.

---

### Section D — Subject Performance Heatmap

**Purpose:** A grid showing average score by subject (rows) × score band (columns). Quickly reveals which subjects are universally weak or strong.

```
                   0-30%   31-50%   51-70%   71-90%   91-100%
Mathematics         ████     ████     ░░░░     ░░░░      ░
Physics             ██       ████     ████     ░░        ░
Chemistry           █        ████     ████     ░░        ░
Biology             ░░       ████     ████     ░░░░      ░
English             ░░       ███      ████     ████      ░░
General Knowledge   ░░░░     ████     ████     ░░        ░
Reasoning           ░░       ███      ████     ████      ░░
```

**Cell colour:** Red gradient (high % in low score bands) → Green gradient (high % in high score bands). Cell value: percentage of attempts in that score band for that subject.

**Tooltip:** "Mathematics — 31–50% band: 38% of attempts. {N} total attempts."

**Row click:** Opens subject detail panel (slide-down expansion) showing:
- 7-day trend of avg score for this subject
- Top 3 weakest topics within the subject (from question-level data)
- Link to H-04 Question Intelligence filtered to this subject

**Column:** Subjects sourced from global subject taxonomy. Only subjects with ≥ 100 attempts shown (min threshold to avoid noise).

---

### Section E — Cohort Retention Chart

**Purpose:** Shows what percentage of students from each monthly enrollment cohort are still active {N} months later. Critical for understanding platform stickiness.

**Data source:** `analytics_cohort_snapshot` — pre-computed monthly.

```
     Cohort Retention — Students by First Exam Month
     % Active vs. Cohort Size

Month 0  ████████████████████████  100% (baseline)
Month 1  ████████████████████░░░░   82%
Month 2  ████████████████░░░░░░░░   67%
Month 3  ████████████████░░░░░░░░   63%
Month 6  ████████████░░░░░░░░░░░░   51%
Month 12 █████████░░░░░░░░░░░░░░░   38%

Cohort: Sep 2024 (n=14,200 students) ▾
```

**Cohort selector:** Dropdown listing all calendar months in the last 24 months. Months where the pipeline ran and produced data are shown normally. Months where the pipeline missed are shown with "(Data not computed)" label and are selectable — the chart will show "⚠ Cohort data not available for {month}. [Re-run pipeline →] (H-06)". Months where the cohort had < 30 students are shown with "(Insufficient data — < 30 students)" label and display only a "Cohort too small to display (DPDPA)" placeholder when selected.

**Overlay mode:** Select up to 3 cohorts to compare retention curves on the same chart (different line colours).

**Dimension toggle:** Split cohort by [Institution Type] or [Exam Domain] or [Region] — shows separate retention lines per dimension.

**Interpretation guide:** Small info tooltip: "Retention = student took at least one exam in that month, relative to their first exam month." Clarifies this is exam activity retention, not login retention.

---

### Section F — Domain Breakdown Table

Six-row table (one per exam domain). Server-side sorted and filtered based on active domain filter.

| Column | Sortable | Notes |
|---|---|---|
| Domain | No | Domain name + icon badge |
| Attempts (period) | Yes | From `analytics_daily_snapshot` dimension=exam_domain |
| Avg Score % | Yes | — |
| Pass Rate % | Yes | — |
| 30-Day Score Trend | No | Sparkline — 30 daily avg score points |
| Abandonment Rate | Yes | Attempts abandoned ÷ total starts |
| YoY Attempts Change | Yes | % change vs same period last year |
| Actions | — | [View in H-05 →] opens H-05 filtered to this domain |

**Row click:** Opens domain detail expansion (accordion) showing a 7-day breakdown of attempts + avg score per subject within that domain.

---

### Section G — Dropout Risk Signals Panel

**Purpose:** Surfaces early warning patterns that indicate student disengagement before churn fully manifests. These are leading indicators, not lagging.

**Signals computed by `aggregate_daily_platform_metrics` Celery task:**

| Signal | Definition | Threshold | Severity |
|---|---|---|---|
| Single-attempt cohort | Students who took exactly 1 exam and never returned | > 40% of new monthly students | WARN |
| Score stagnation (cohort) | **Aggregate signal — DPDPA compliant.** Computed as: of the cohort of students who made their 1st attempt in a given 30-day window, the cohort-average score on their 5th+ attempt is ≤2pp higher than cohort-average on their 1st attempt. No individual student tracking — all values are group means. Source: `analytics_daily_snapshot` metric_key=`cohort_score_stagnation_rate`. | > 25% of rolling cohorts show stagnation | WARN |
| Post-exam abandonment | Students who completed an exam but didn't return within 14 days | > 35% | INFO |
| Domain-specific drop-off | One domain losing > 20% of its student base vs. prior month | — | CRITICAL |
| Night-only usage drop | Students only attempting exams after 10pm (proxy for de-prioritisation) | Trend | INFO |
| First-exam fail → no retry | Students who scored < 30% on first exam and never re-attempted within 30 days | > 30% of <30% scorers | WARN |

**Panel display:** Each signal shows:
- Signal name + severity badge
- Current value vs threshold
- Period this was computed for
- [See Cohort in H-02] — pre-fills filters and scrolls to the relevant section. URL format: `/analytics/students/?signal={signal_key}&period={period_start}_{period_end}&domain={domain}`. H-02 reads these params on load: if `signal` param present, the Dropout Signals panel is expanded with that signal highlighted, and the domain/period filters are pre-selected.
- [Download Segment CSV] — exports anonymised cohort data (IDs hashed, no names). **30-student minimum enforced at export time**: if the signal's qualifying cohort has fewer than 30 students after applying active filters, export is blocked with message "Cohort too small to export (< 30 students) — broaden filters to meet minimum threshold."

**Zero signals:** "✅ No dropout risk signals above threshold for the selected period."

---

## 5. Access Control

| Gate | Rule |
|---|---|
| Page access | Analytics Manager (42), Data Analyst (44), Platform Admin (10) |
| Data Engineer (43) | Read-only via H-01 links; full access not needed |
| Report Designer (46) | Read-only via H-08 template data preview |
| [Export Report] | Analytics Manager (42), Data Analyst (44) |
| [Download Segment CSV] | Analytics Manager (42), Data Analyst (44) |
| Minimum cohort size enforcement | System-enforced: no cell shown if underlying cohort < 30 students |

---

## 6. Edge Cases & Error States

| Scenario | Behaviour |
|---|---|
| Selected period has no data (pipeline hasn't run yet for that date) | Summary bar tiles show "—". Chart shows empty state: "No data available for {period}. Data pipeline runs nightly at 01:00 IST." |
| Domain filter produces cohort < 30 students | Score distribution shows "Insufficient data for this filter combination (< 30 students). Broaden filters to see results." No data exposed. |
| Cohort snapshot not computed for a given month (pipeline missed) | Cohort chart shows gap at that month with tooltip: "Cohort not computed — pipeline missed for {month}. [Re-run →]" (links to H-06 for Data Engineer only) |
| Subject heatmap has >15 subjects | Shows top 15 by attempt volume with "Show {N} more" expandable section |
| Abandonment rate = 0% (suspicious) | Info tooltip: "0% abandonment may indicate all attempts are from completed exams or data pipeline issue." |
| Period spans pipeline schema migration (older data in different format) | Chart shows break with annotation: "Data format changed at {date}. Pre-change data may not be directly comparable." |

---

## 7. UI Patterns

### Loading States
- Summary bar: 7-tile shimmer
- Score distribution chart: grey placeholder (same dimensions as chart)
- Subject heatmap: grid skeleton with shimmer cells
- Cohort chart: line chart skeleton
- Domain table: 6-row shimmer
- Dropout signals: 3-card shimmer

### Toasts
| Action | Toast |
|---|---|
| Export queued | ✅ "Report is being generated — you'll be notified when ready" (4s) |
| Segment CSV ready | ✅ "Segment export ready — download within 48h" (persistent) |

### Responsive
| Breakpoint | Behaviour |
|---|---|
| Desktop (≥1280px) | Full two-column layout for lower sections |
| Tablet | Single column. Heatmap scrolls horizontally. Cohort and domain table full-width. |
| Mobile | Stat bar 2×4 grid. Charts simplified (single series). Heatmap replaced with subject list. |

---

*Page spec complete.*
*H-02 covers: 7-stat summary bar → score distribution histogram with cumulative overlay → subject performance heatmap with topic drilldown → 12-month cohort retention waterfall → domain breakdown table with sparklines → 6-signal dropout risk panel with segment export.*
