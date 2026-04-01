# H-05 — Exam & Domain Analytics

> **Route:** `/analytics/exams/`
> **Division:** H — Data & Analytics
> **Primary Role:** Analytics Manager (42) · Data Analyst (44)
> **Supporting Roles:** Platform Admin (10) — full
> **File:** `h-05-exam-analytics.md`
> **Priority:** P1 — exam performance drives product roadmap and content decisions

---

## 1. Page Name & Route

**Page Name:** Exam & Domain Analytics
**Route:** `/analytics/exams/`
**Part-load routes:**
- `/analytics/exams/?part=domain-kpi` — domain KPI bar
- `/analytics/exams/?part=domain-comparison` — side-by-side domain chart
- `/analytics/exams/?part=exam-table` — exam performance table
- `/analytics/exams/?part=timing-analysis` — timing heatmap
- `/analytics/exams/{exam_ref}/?part=exam-drawer` — exam detail drawer

---

## 2. Purpose

H-05 drills into **how exams are performing across domains, test series, and time periods**. While Division F (Exam Day Operations) monitors live exam health in real-time, H-05 provides the retrospective analytical view:

- Which domains are growing vs stagnating?
- Are completion rates acceptable? Where are students abandoning?
- How does exam difficulty correlate with student time-on-paper?
- Is a new test series attracting or losing students vs prior series?
- Which institutions are the heaviest users of each domain?
- Is there a "difficulty spike" in a specific month's question set?

**Who needs this page:**
- Analytics Manager (42) — domain performance reporting, leadership decks
- Data Analyst (44) — detailed exam investigations, series comparison

---

## 3. Layout

```
┌────────────────────────────────────────────────────────────────────┐
│  Page header: "Exam & Domain Analytics"  [Export Domain Report]   │
│  Filters: Period | Domain | Exam Type | Institution Type | Tier   │
├──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────────────────┤
│Total │Total │Avg   │Compl.│Avg   │Avg   │Abnd. │ SLA-breach        │
│Exams │Attmps│Score │Rate  │Time  │Rank  │Rate  │ Correlation %     │
│      │      │      │      │/Min  │Delta │      │                   │
├──────┴──────┴──────┴──────┴──────┴──────┴──────┴──────────────────┤
│  Domain Comparison Bar Chart (6 domains, multiple metrics)        │
├────────────────────────────────┬───────────────────────────────────┤
│  Exam Performance Table        │  Timing Heatmap                   │
│  (server-side paginated)       │  (time-of-day × day-of-week)      │
└────────────────────────────────┴───────────────────────────────────┘
```

---

## 4. Section-Wise Detailed Breakdown

---

### Section A — Filters

| Filter | Control | Notes |
|---|---|---|
| Period | Date range picker: 7D / 30D / 90D / 6M / 1Y / Custom | Default: 30D |
| Exam Domain | Multiselect: All / SSC / RRB / NEET / JEE / AP Board / TS Board | — |
| Exam Type | Multiselect: Mock Test / Practice Set / Chapter Test / Full Syllabus | — |
| Institution Type | Multiselect: School / College / Coaching / All | — |
| Subscription Tier | Multiselect: All / Starter–Enterprise | — |
| Min Exam Size | Number input | Only exams with ≥ N enrolled students (default: 10) |

---

### Section B — Domain KPI Bar

Eight tiles. Source: `analytics_daily_snapshot` for the selected period.

| Tile | Description | Colour Rule |
|---|---|---|
| Total Exams | Distinct exam instances conducted | Neutral |
| Total Attempts | Sum of all student attempts | Neutral |
| Avg Score % | Mean score across all attempts | Green ≥55%; Amber 45–55%; Red <45% |
| Completion Rate | Submitted ÷ started | Green ≥90%; Amber 80–90%; Red <80% |
| Avg Time on Paper (min) | Mean time from exam start to submission | Green if within ±20% of time limit; Amber if < 60% (students finishing too fast) |
| Avg Rank Delta | **DPDPA-compliant cohort metric:** For the cohort of students who attempted the same exam type more than once within the period, the group-average change in percentile rank from first attempt to most recent attempt. No individual rank tracking — computed as `avg(latest_attempt_percentile_band) - avg(first_attempt_percentile_band)` across the cohort. Cohort must have ≥ 30 students; otherwise shows "—". Source: `analytics_daily_snapshot` metric_key=`avg_rank_delta`, dimension=exam_domain. | Green > 0 (improving); Amber = 0; Red < 0 |
| Abandonment Rate | Started but not submitted (timed out or closed) | Green <5%; Red >15% |
| SLA-breach Correlation | % of exams where infrastructure SLA was breached during the exam window | Red if > 0% (any SLA breach correlating with exams) |

**SLA-breach correlation** — links Division F SLA data with exam outcomes. Computed by joining exam time windows with infrastructure incident records from `analytics_infrastructure_event` table (synced nightly from Division F's `incident_log` via the `aggregate_daily_platform_metrics` Celery task — a read-only cross-schema join at aggregation time, not at page render time). High value indicates students are being impacted by platform issues.

---

### Section C — Domain Comparison Bar Chart

**Purpose:** Side-by-side comparison of all 6 exam domains on multiple metrics. Immediately shows which domain is under or over-performing.

**Implementation:** Chart.js Grouped Bar chart. X-axis: 6 domains. Toggle between metrics via button group.

**Metric toggle options:**
- [Exam Attempts] — total attempt volume
- [Avg Score %] — difficulty proxy
- [Completion Rate] — engagement proxy
- [Abandonment Rate] — friction proxy
- [MoM Growth %] — momentum indicator

Hover tooltip: "{Domain} — {metric}: {value} · Period: {start}–{end}"

**Trend lines toggle:** [Show 3-month trend] adds a line chart overlay per domain for the selected metric over time (3 data points: M-2, M-1, current month).

---

### Section D — Exam Performance Table

Server-side paginated, 25 rows per page. One row = one distinct exam instance. Source: `analytics_daily_snapshot` + exam registry. **Exam name denormalization:** `exam_name` and `institution_name` are denormalized into `analytics_daily_snapshot` at aggregation time by the `aggregate_daily_platform_metrics` Celery task. If an exam is renamed after aggregation, the analytics record retains the name at time of aggregation — updated on the next nightly run.

| Column | Sortable | Notes |
|---|---|---|
| Exam Name | Yes | Truncated. Full in tooltip. |
| Domain | Yes | Badge |
| Institution | No | Institution name (or "Multi-institution" if group exam) |
| Date | Yes | Exam date |
| Type | No | Mock / Practice / Chapter / Full Syllabus badge |
| Enrolled | Yes | Students enrolled |
| Attempts | Yes | Students who started |
| Completion Rate | Yes | Completed ÷ started |
| Avg Score % | Yes | — |
| Avg Time (min) | Yes | — |
| Abandonment | Yes | Started but not submitted count |
| Actions | — | [View →] opens exam detail drawer |

**Default sort:** Date DESC (most recent exams first).

**Bulk actions:**
- [Export Selected CSV] — exam performance data for selected rows
- [Compare Selected] — opens comparison modal (max 5 exams) showing side-by-side metrics

**Compare modal:** Table with selected exams as columns, metrics as rows. Useful for comparing "same test series, different months" to identify performance drift. **Domain mismatch warning:** if selected exams span more than 2 different domains, a banner appears: "⚠ Selected exams span {N} domains ({list}). Cross-domain score comparison may be misleading due to different passing thresholds. Continue?"

---

### Section E — Timing Heatmap

**Purpose:** Shows when students are taking exams (time of day × day of week). Critical for:
- Scheduling infrastructure maintenance windows (avoid exam-heavy hours)
- Identifying peak times for capacity planning
- Understanding if exam schedules cluster (coaching centres run Sunday morning mock tests → peak load)

```
            Mon   Tue   Wed   Thu   Fri   Sat   Sun
  6–9am     ░░░   ░░░   ░░░   ░░░   ░░░   ████  ████
  9–12pm    ████  ██    ██    ██    ██    ████  ████
  12–3pm    ████  ██    ██    ██    ██    ████  ████
  3–6pm     ████  █     █     █     █     ██    ██
  6–9pm     ████  ████  ████  ████  ████  ████  ████
  9pm–12am  ████  ████  ████  ████  ████  ██    ██
```

**Cell colour:** Dark indigo = highest attempt volume. Light grey = lowest. 8 colour bands.

**Cell tooltip:** "{day} {time_band} — {N} attempts · {M} exams scheduled"

**Overlays:**
- [Infrastructure incidents] toggle — overlays red borders on cells where SLA was breached during that time window in the period
- [Peak load periods] toggle — highlights cells that exceed 70% of the max cell value

**Data:** Computed from `analytics_daily_snapshot` with time-of-day dimension during the `aggregate_daily_platform_metrics` aggregation job. The Celery task reads `exam_start_time` from tenant schemas, extracts `day_of_week` (0=Monday–6=Sunday) and `hour_of_day` (0–23), buckets into 3-hour bands (0–2, 3–5, ..., 21–23), and writes to `analytics_daily_snapshot` with `dimension_type = 'time_band'` and `dimension_value = '{day_of_week}_{band}'` (e.g., `'0_6'` = Monday 6–9am band). All times stored in IST.

---

### Section F — Exam Detail Drawer

460px right drawer. Tabs: **Performance | Score Distribution | Timing | Infrastructure**

#### Performance Tab

**Exam header:** Exam name · Domain · Institution · Date · Duration · Enrolled count

**Performance summary:**
| Metric | Value | vs Platform Avg |
|---|---|---|
| Enrolled | — | — |
| Attempts | — | — |
| Completion Rate | — | ▲ or ▼ vs platform avg |
| Avg Score % | — | ▲ or ▼ |
| Pass Rate | — | — |
| Avg Time on Paper | — | ▲ or ▼ |
| Abandonment Count | — | — |

**Score percentile table:**
| Percentile | Score |
|---|---|
| 90th | e.g., 82% |
| 75th | 71% |
| 50th (median) | 58% |
| 25th | 44% |
| 10th | 31% |

**Re-attempt context:** If this exam type has been run before (same template): "Previous run: {date} — Avg score was {N}% ({+/-} {delta}pp change)."

#### Score Distribution Tab

Histogram (10-bucket) of scores for this specific exam. Same format as H-02 Section C but scoped to one exam.

**Annotation:** Pass threshold line + median line + platform average line (three dashed verticals).

**Normal distribution overlay:** Optional toggle. Fits a normal curve to the distribution — if the actual distribution deviates significantly, it may indicate question set issues.

#### Timing Tab

**Time-on-paper distribution:** Histogram showing how long students spent before submitting (0–10min, 10–20min, ..., up to exam duration). Reveals:
- Students submitting very quickly (< 30% of time limit) = possible cheating or very easy exam
- Large spike at exact time limit = students running out of time = exam too long

**Question-level timing (top 10 slowest and fastest):** Table of the 10 questions where students spent the most time (high difficulty) and the 10 where they spent the least time (possibly skipped or trivially easy).

#### Infrastructure Tab

**Purpose:** Did infrastructure issues affect this exam's outcome?

Shows timeline of the exam window (e.g., 10:00–13:00) overlaid with any infrastructure events:
- SLA breaches (latency > 2s)
- Incident records open during this window
- Lambda concurrency alerts during this window

**If no incidents:** "✅ No infrastructure issues recorded during this exam window."
**If incidents existed:** "⚠ {N} infrastructure incident(s) open during this exam. [View Incident →]" with timeline overlay showing incident duration vs exam duration.

This tab answers: "Was the low completion rate due to infrastructure or student behaviour?"

---

## 5. Access Control

| Gate | Rule |
|---|---|
| Page access | Analytics Manager (42), Data Analyst (44), Platform Admin (10) |
| [Export Domain Report] | Analytics Manager (42), Platform Admin (10) |
| [Export Selected CSV] bulk | Analytics Manager (42), Data Analyst (44) |
| [Compare Selected] modal | Analytics Manager (42), Data Analyst (44) |
| Infrastructure tab in drawer | Analytics Manager (42), Data Analyst (44) — read-only |

---

## 6. Edge Cases & Error States

| Scenario | Behaviour |
|---|---|
| Domain has 0 exams in the selected period | Domain row shows "No exams" with em-dash across all metrics. Remains visible (not hidden) so the gap is obvious. |
| Exam with < 10 students | Filtered out by default (Min Exam Size = 10). If user sets Min Exam Size = 1, low-sample exams show with "Low sample — statistics may be unreliable" tooltip. |
| SLA-breach correlation = 100% | Critical alert: "All exams in this period occurred during SLA-breach windows. Data reliability for score analytics may be compromised. Contact Division F." Shown as a prominent banner. |
| Timing heatmap has only 1 day of data | Shows a 1-column heatmap labelled clearly. No inference about weekly patterns. |
| Exam with 0 completions (all abandoned) | Completion Rate = 0%. Marked with ABANDONED badge. Likely infrastructure issue or exam configuration error. Shows link to Division F incident log for that day. |
| Period selected is longer than available pipeline data | Chart shows data only for available dates. Annotation: "Historical data available from {earliest_date}." |

---

## 7. UI Patterns

### Loading States
- KPI bar: 8-tile shimmer
- Domain comparison chart: bar chart skeleton
- Table: 10-row shimmer
- Timing heatmap: grid of shimmer cells
- Exam drawer: header + 4 tab shimmers + content skeleton

### Toasts
| Action | Toast |
|---|---|
| Export queued | ✅ "Domain report queued — notified when ready" (4s) |
| Comparison modal opened | No toast — modal opens |

### Responsive
| Breakpoint | Behaviour |
|---|---|
| Desktop (≥1280px) | Full side-by-side layout for table + heatmap |
| Tablet | Table + heatmap stacked. Table: 6 columns. |
| Mobile | Heatmap collapsed to 3-hour bands only (simplified). Table card view. |

---

*Page spec complete.*
*H-05 covers: 8 domain KPIs with SLA correlation → domain comparison grouped bar chart → exam performance table with comparison mode → timing heatmap (time-of-day × day-of-week with incident overlay) → exam detail drawer (performance / score distribution / timing analysis / infrastructure correlation).*
