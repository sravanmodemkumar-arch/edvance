# H-01 — Analytics Dashboard

> **Route:** `/analytics/`
> **Division:** H — Data & Analytics
> **Primary Role:** Analytics Manager (42) — platform MIS command centre; Data Analyst (44) — daily monitoring
> **Supporting Roles:** Data Engineer (43) — pipeline health awareness; AI Gen Manager (45) — AI pipeline KPI; Report Designer (46) — delivery status; Platform Admin (10) — full
> **File:** `h-01-analytics-dashboard.md`
> **Priority:** P0 — the first page all Division H roles open every morning

---

## 1. Page Name & Route

**Page Name:** Analytics Dashboard
**Route:** `/analytics/`
**Part-load routes:**
- `/analytics/?part=kpi-bar` — KPI summary bar
- `/analytics/?part=trend-chart` — 30-day platform trend chart
- `/analytics/?part=anomaly-panel` — anomaly alerts
- `/analytics/?part=domain-table` — cross-domain performance table
- `/analytics/?part=pipeline-status` — Celery pipeline health strip
- `/analytics/?part=activity-feed` — recent analytics activity feed

---

## 2. Purpose

H-01 is the platform-wide MIS command centre for Division H. It answers the one question every data person checks first thing every morning: **"Is the platform growing, healthy, and is the data pipeline fresh?"**

Unlike the Division A Executive Dashboard (which is business-level for the CEO), H-01 is oriented toward the data team:
- Are all aggregation pipelines current?
- Are there any statistical anomalies in today's data?
- What is the AI generation pipeline producing?
- Is question bank quality improving or degrading?
- How many institutions are in critical churn risk?

**Who needs this page:**
- Analytics Manager (42) — daily health check, anomaly investigation, stakeholder brief prep
- Data Analyst (44) — morning check before diving into specific analytics pages
- Data Engineer (43) — pipeline status at a glance before investigating H-06
- AI Generation Manager (45) — AI pipeline KPIs
- Report Designer (46) — report delivery success rates

---

## 3. Layout

```
┌─────────────────────────────────────────────────────────────────────┐
│  Page header: "Analytics Dashboard"    [Export Daily Brief PDF]     │
│  ⚠ Data as of: 01:47 IST today · Next refresh: 01:00 IST tomorrow  │
├─────────────────────────────────────────────────────────────────────┤
│  Pipeline Health Strip (top — always visible if any pipeline issue) │
├──────────┬──────────┬──────────┬──────────┬──────────┬─────────────┤
│  Active  │ Exam     │ New      │ Avg      │ AI MCQs  │ Critical    │
│  Inst.   │ Attempts │ Students │ Score    │ in       │ Churn Risk  │
│  (MTD)   │  (MTD)   │  (MTD)   │  (MTD)   │ Pipeline │ Institutions│
├──────────┴──────────┴──────────┴──────────┴──────────┴─────────────┤
│  30-Day Platform Trend Chart (multi-series, Chart.js)              │
├────────────────────────────────┬────────────────────────────────────┤
│  Cross-Domain Performance      │  Anomaly Alerts Panel              │
│  Table (6 domains)             │  (auto-detected outliers)          │
├────────────────────────────────┴────────────────────────────────────┤
│  Analytics Activity Feed                                            │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 4. Section-Wise Detailed Breakdown

---

### Section A — Pipeline Health Strip

**Displayed only when any pipeline is stale, failed, or running.**

| State | Display |
|---|---|
| All pipelines current | Strip hidden (clean state — no noise) |
| Any pipeline stale (> 26h since last success) | `⚠ {N} pipeline(s) are stale — data may be outdated. [View in H-06 →]` (amber bar) |
| Any pipeline FAILED | `❌ {pipeline_name} failed at {time}. [View Details →]` (red bar) |
| Pipeline currently RUNNING | `⏳ {pipeline_name} is running — data will update shortly.` (blue bar) |

Multiple issues: stacked strips, most severe on top. Maximum 3 strips shown; "and {N} more issues" link to H-06.

**Links directly to H-06 Data Pipeline Monitor** for investigation.

**Data freshness indicator (always visible below page header):**
- "Data as of: 01:47 IST today" — shows `max(completed_at)` from successful `analytics_pipeline_run` records
- If any metric is based on a different (older) run: tooltip on that specific tile shows "This metric: data as of {older_time}"

---

### Section B — KPI Summary Bar

Six tiles. All values from `analytics_daily_snapshot` for yesterday (or last available day). Clicking a tile navigates to the relevant deep-dive page.

| Tile | Metric Key | Value Format | Colour Rule | Links To |
|---|---|---|---|---|
| Active Institutions (MTD) | `active_institutions_mtd` (dedicated metric key). **Aggregation note:** `analytics_daily_snapshot` stores the daily distinct-institution count per day (`metric_key='active_institutions'`), but simply summing these double-counts institutions active on multiple days. Instead, `aggregate_daily_platform_metrics` (Task 1) also computes and writes `metric_key='active_institutions_mtd'` each night — this is the running cumulative distinct institution count from the 1st of the current month to yesterday, re-computed each night. The H-01 tile reads the latest `active_institutions_mtd` row (most recent `snapshot_date` in current month). Cached in Memcached 60 min. | Integer · `{N} of 2,050` | Green if MTD ≥ last MTD same period last month; Red if < 80% | H-03 |
| Exam Attempts (MTD) | `exam_attempts_total` | Integer with K/M suffix | Green ≥ last MTD; Amber -10%; Red -20% | H-05 |
| New Students (MTD) | `new_students` | Integer | Green ≥ last MTD | H-02 |
| Avg Score (MTD) | `avg_score_pct` | `{N}%` | Green ≥ target (configurable, default 55%); Amber 45–55%; Red < 45% | H-02 |
| AI MCQs in Pipeline | Count of individual MCQs pending review: `COUNT(*) FROM analytics_ai_generated_mcq WHERE review_status = 'PENDING' AND (skipped_until IS NULL OR skipped_until < NOW())`. This is a direct DB query on analytics schema (cached 5 min) — not a batch-level count. | `{N} MCQs pending review · {M} active batches` | Green if 0 pending; Amber > 200 pending; Red > 500 (critical backlog — risk to Division D pipeline) | H-07 |
| Critical Churn Risk | Latest `analytics_institution_engagement` count where `churn_risk = CRITICAL` | `{N} institutions` | Green = 0; Amber 1–5; Red > 5 | H-03 at `/analytics/institutions/?churn_risk=CRITICAL` — H-03 reads `churn_risk` URL param on load and pre-selects that filter |

**MoM comparison badge** on each tile: `▲ 12%` (green) or `▼ 8%` (red) vs. previous month same period.

**HTMX refresh:** KPI bar refreshes on page load only (data is nightly — no point polling). Manual `[Refresh]` button forces HTMX swap.

---

### Section C — 30-Day Platform Trend Chart

**Purpose:** Single chart showing multiple platform health series over the last 30 days. Each role can toggle which series they care about.

**Implementation:** Chart.js Line chart. Multiple datasets. Shared x-axis (date). Dual y-axis (left: counts, right: percentages).

```
    ┌──────────────────────────────────────────────────────────────────┐
    │  PLATFORM TREND — LAST 30 DAYS                          ● LIVE  │
    │                                                                  │
 45K│                               /\/\/\___/\/\/\/\/\/\/\/\/\       │
    │                           /\/\/                                  │
 30K│         /\/\/\/\/\/\/\/\/\/                                      │
    │        /                                                         │
 15K│       /                        ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─     │
    │──────────────────────────────────────────────────────────────────│
  0 │  Day 1                  Day 15                  Day 30          │
    └──────────────────────────────────────────────────────────────────┘
  Toggle: [✅ Exam Attempts] [✅ Active Institutions] [☐ New Students] [☐ Avg Score %]
```

**Default series shown:** Exam Attempts (left axis, line), Active Institutions (left axis, area). Other series togglable per user preference (persisted in session).

**Available series:**
| Series | Axis | Chart Type | Colour |
|---|---|---|---|
| Exam Attempts | Left | Line | `#6366F1` (indigo) |
| Active Institutions | Left | Area (filled) | `#10B981` (green, 20% opacity) |
| New Students | Left | Line | `#F59E0B` (amber) |
| Avg Score % | Right | Line (dashed) | `#3B82F6` (blue) |
| AI MCQs Approved | Left | Bar | `#8B5CF6` (purple) |
| Questions Published | Left | Bar | `#14B8A6` (teal) |

**Hover tooltip:** Shows all visible series values for that date, plus the day name.
**Click on a date point:** Opens a date-scoped view with data breakdown for that specific day.

**Period selector:** [30D] [90D] [6M] [1Y] — switches the x-axis range. Fetches from `analytics_daily_snapshot` with appropriate date filter.

**HTMX:** `id="trend-chart"` part-loaded on page init. Chart.js instance preserved — data updates via JSON response and `chart.data.datasets[N].data = newData`.

---

### Section D — Cross-Domain Performance Table

Six-row table (one per exam domain). Sortable by any column.

| Column | Notes |
|---|---|
| Domain | SSC · RRB · NEET · JEE · AP Board · TS Board — with icon/badge |
| Active Institutions | Institutions using this domain this month |
| Exam Attempts (MTD) | From `analytics_daily_snapshot` dimension_type=exam_domain |
| Avg Score % | — |
| Pass Rate | `% scoring above domain pass threshold`. Pass threshold is configured per domain in the platform admin settings (Division B Product Manager scope — not a Division H table). Division H reads it from the shared `exam_domain_config` table (read-only). |
| Question Bank Size | Pre-computed nightly: `analytics_daily_snapshot` metric_key=`question_bank_size`, dimension_type=`exam_domain`. Populated by `aggregate_daily_platform_metrics` Celery task. Cached in Memcached 60 min. (No live cross-schema query at page render time.) |
| Trend | Mini 7-day sparkline for exam attempts — Chart.js inline sparkline |

**Row click** → navigates to H-05 Exam & Domain Analytics pre-filtered to that domain.

**[Export Table CSV]** — downloads the current view as CSV.

---

### Section E — Anomaly Alerts Panel

**Purpose:** Auto-detected statistical outliers from the latest nightly pipeline run. Surfaces problems the team hasn't noticed yet.

**Anomaly detection rules (evaluated by `aggregate_daily_platform_metrics` Celery task):**

| Anomaly Type | Trigger Condition | Severity |
|---|---|---|
| Exam attempt spike | Today's attempts > 2× rolling 30-day avg for that domain | WARN |
| Exam attempt drop | Today's attempts < 50% of rolling 30-day avg | CRITICAL |
| Score drop | Avg score drops > 8 percentage points vs. rolling 7-day avg | WARN |
| New student spike | New students > 3× rolling 30-day avg (possible bot / bulk import) | INFO |
| Score ceiling effect | Avg score > 90% for 3+ consecutive days on a specific exam | WARN (too easy?) |
| Question bank shrink | Questions published today < 0 (net deletion — unusual) | WARN |
| AI batch cost spike | Any AI batch cost > 2× avg cost per MCQ | INFO |

**Panel display:**
```
ANOMALY ALERTS                                              [Dismiss All]
─────────────────────────────────────────────────────────────────────
🔴 CRITICAL  Exam attempt drop: RRB domain down 62% vs 30-day avg
             Yesterday: 12,400 · Avg: 32,800 · [View H-05 →]
─────────────────────────────────────────────────────────────────────
⚠  WARN      Score drop: AP Board — 61% → 52% (yesterday)
             May indicate new exam with higher difficulty or data error.
             [View H-02 →]
─────────────────────────────────────────────────────────────────────
ℹ  INFO      New student spike: SSC domain +340% vs avg
             Large coaching centre batch import? [View H-02 →]
─────────────────────────────────────────────────────────────────────
✅ No anomalies in: NEET · JEE · TS Board
```

**[Dismiss]** on each alert — hides for 24h (re-appears if anomaly persists tomorrow). Dismissals logged for audit.

**Zero anomalies state:** "✅ No anomalies detected in today's data." — calm green panel.

**HTMX:** Loads on page init. No auto-refresh (anomalies are computed once per nightly pipeline).

---

### Section F — Analytics Activity Feed

Recent actions across Division H, shown to all H roles. Sourced from `analytics_audit_log` (ordered by `created_at DESC`, last 20 records). Each entry shows: action label, actor name, object reference, and relative timestamp ("1 hour ago").

| Event | Who | When |
|---|---|---|
| Pipeline `aggregate_daily_platform_metrics` completed | System (Celery) | e.g., "1 hour ago" |
| AI batch AIB-202409-0042 approved (42/50 MCQs, 3 auto-rejected duplicates) | AI Gen Manager name | — |
| Institution report template "Monthly Summary" published | Analytics Manager name | — |
| Report delivery: 98 coaching institutions delivered | System | — |
| Question bulk archive: 1,240 NEVER_USED questions flagged | Data Analyst name | — |
| Export request "question_stats_ssc_sept" ready for download | — | — |
| Anomaly dismissed: RRB attempt drop | Analytics Manager name | — |

Pagination: last 20 events. [Load More] loads previous 20.

**Anomaly dismissals** are logged to `analytics_audit_log` (action=`ANOMALY_DISMISSED`, detail includes anomaly_type and value). This ensures dismissed anomalies are auditable — the team can review whether anomalies that were dismissed were actually real issues that got ignored.

---

### Section G — Export Daily Brief

**[Export Daily Brief PDF]** — top-right of page header.

Generates a 1–2 page PDF summary of the current dashboard state:
- KPI tiles with MoM comparison
- Key anomalies
- Domain performance table
- Pipeline status

Generated asynchronously via Celery `process_export_request`. User notified when ready (within 30–60 seconds for this lightweight report).

Useful for: Analytics Manager sharing daily brief in leadership standups.

---

## 5. Access Control

| Gate | Rule |
|---|---|
| Page access | Analytics Manager (42), Data Analyst (44), Data Engineer (43), AI Gen Manager (45), Report Designer (46), Platform Admin (10) |
| KPI tiles | All roles see all tiles |
| Export Daily Brief | Analytics Manager (42), Platform Admin (10) |
| Dismiss anomalies | Analytics Manager (42), Data Analyst (44) |
| Pipeline health strip links | Visible to all; H-06 access required to take action |
| Activity feed | All roles see all events relevant to Division H |

---

## 6. Edge Cases & Error States

| Scenario | Behaviour |
|---|---|
| No nightly pipeline has ever run (fresh install) | KPI bar shows "No data yet — pipeline has not run." with [Trigger First Run →] linking to H-06 for Data Engineer |
| Nightly pipeline failed last night | Orange staleness banner: "⚠ Last successful data: {DD Mon} at {HH:MM AM/PM} IST — {N} hours ago. Pipeline failed. [View Details →] (H-06)". Timestamp format: "30 Nov at 01:04 AM IST" to avoid "yesterday" ambiguity during early morning hours (01:00–03:00 IST when pipelines run). |
| KPI tile has no data for a dimension | Shows "—" (em-dash) with tooltip "No data for this period." Never shows 0 if 0 means "not computed" vs "genuinely zero" |
| All 6 domains show 0 exam attempts | Anomaly alert raised; also possible the pipeline failed before domain aggregation finished |
| Analytics Manager opens dashboard during pipeline run | Blue strip: "⏳ Metrics pipeline running — data will refresh when complete." KPI tiles show previous values clearly labelled as "previous" |
| Trend chart has a gap in the 30-day window | Renders Chart.js `null` point (breaks line rather than connecting over the gap — visually shows missing data honestly) |
| Critical churn risk institutions drop to 0 | KPI tile shows "0" in green; anomaly alert suppressed (it's good news) |

---

## 7. UI Patterns

### Loading States
- Pipeline health strip: none (always rendered server-side)
- KPI bar: 6-tile shimmer (same height as tiles)
- Trend chart: grey placeholder with "Loading chart data..." centred
- Domain table: 6-row shimmer
- Anomaly panel: 3-line shimmer
- Activity feed: 5-item shimmer

### Toasts
| Action | Toast |
|---|---|
| Export Daily Brief queued | ✅ "Daily brief is being generated — you'll be notified when ready" (4s) |
| Brief ready | ✅ "Daily brief ready — [Download PDF]" (persistent until dismissed) |
| Anomaly dismissed | ✅ "Alert dismissed for 24h" (3s) |

### Responsive
| Breakpoint | Behaviour |
|---|---|
| Desktop (≥1280px) | Full layout as designed |
| Tablet | KPI bar: 3×2 grid. Domain table: 4 visible columns. Anomaly panel + Activity feed: stacked below chart. |
| Mobile | KPI bar: 2×3 grid. Chart: 120px height, single series. Tables: horizontal scroll. |

---

*Page spec complete.*
*H-01 covers: pipeline health strip (stale/failed/running states) → 6 KPI tiles with MoM trends → 30-day multi-series trend chart (toggleable series) → cross-domain performance table with sparklines → auto-detected anomaly alerts with dismissal → analytics activity feed → async daily brief export.*
