# E-10 — Production Analytics

> **Route:** `/content/video/analytics/`
> **Division:** E — Video & Learning
> **Primary Role:** Content Producer — Video (82)
> **Supporting Roles:** Content Director (18) — full read; All production roles (83–89) — read own-stage metrics only
> **File:** `e-10-production-analytics.md`
> **Priority:** P2
> **Status:** ⬜ Not started

---

## 1. Page Name & Route

**Page Name:** Production Analytics
**Route:** `/content/video/analytics/`
**Part-load routes:**
- `/content/video/analytics/?part=kpi-strip` — KPI tiles (polled every 120s)
- `/content/video/analytics/?part=throughput-chart` — throughput chart
- `/content/video/analytics/?part=sla-chart` — SLA compliance chart
- `/content/video/analytics/?part=stage-bottleneck` — stage bottleneck chart
- `/content/video/analytics/?part=mcq-coverage-chart` — MCQ video coverage chart
- `/content/video/analytics/?part=qa-score-chart` — QA score trends chart (Chart 7)
- `/content/video/analytics/?part=activity-log` — full activity log table

---

## 2. Purpose

Production Analytics gives the Content Producer and Content Director a data-driven view of the production pipeline: how fast videos are being produced, where the bottlenecks are, SLA compliance per stage, and how much of the MCQ question bank has corresponding videos.

**Business goals:**
- Identify bottlenecks (e.g. Script Review stage takes 4 days average vs 3-day SLA)
- Track MCQ video coverage rate — what % of published questions have an explanatory video
- Measure team throughput week-over-week
- Provide exportable reports for Content Director review

---

## 3. KPI Strip

Six tiles, `hx-trigger="every 120s"`:

| Tile | Value | Notes |
|---|---|---|
| Jobs Published (30d) | Count | ▲/▼ vs prior 30d |
| Avg Pipeline Time | Avg days from job creation to PUBLISHED | — |
| SLA Compliance | % of jobs completed within overall SLA (On Time = within SLA · Overdue = past SLA · Critical = >2× SLA) | Red if < 80% |
| MCQ Video Coverage | % of published questions with a PUBLISHED video job | — |
| Jobs In Progress | Count of non-terminal active jobs | — |
| Overdue Right Now | Count of currently overdue jobs | Red if > 0 |

Skeleton: 6 rectangle shimmers.

---

## 4. Date Range Selector

Global date range picker at top of page (default: last 30 days). Options: 7d · 30d · 90d · Custom range.
All charts and KPIs update on change via HTMX reload.

---

## 5. Charts Section

All charts: Recharts `ResponsiveContainer`. No-data: grey placeholder + "No data yet" text.

**Refresh behaviour:** Charts do NOT auto-refresh on a timer — they load on page load and re-render only when the global date range selector changes. This prevents costly aggregation queries running every 120s. KPI tiles (top strip) are the only auto-refreshed elements (every 120s). Activity Log table is also on-demand only (reloads on filter change).

---

### Chart 1 — Weekly Throughput (Line + Bar combo)

- X-axis: weeks in selected date range
- Bars: jobs completed (entered PUBLISHED state) per week
- Line: cumulative total
- Reference line: "Weekly target" (from E-12 config if set)
- Hover tooltip: "{N} jobs published this week"
- Toggle: All / MCQ-Linked / Standalone

---

### Chart 2 — SLA Compliance by Stage (Grouped Bar Chart)

- X-axis: pipeline stages (Script · Animation · Graphics · Edit · Subtitle · QA)
- Y-axis: % on time
- Bar colour: Green ≥80% · Amber 60–79% · Red <60%
- Each bar: hover shows "{N} on time / {M} total = {%}%"
- Click a bar → filters Activity Log to that stage + SLA breach

---

### Chart 3 — Stage Bottleneck — Avg Days per Stage (Horizontal Bar Chart)

- Y-axis: stages
- X-axis: average days spent in stage
- Each bar shows: avg days (with a reference line at the SLA target for that stage from E-12)
- Bars exceeding SLA target shown in amber/red
- "Bottleneck indicator": stage with highest avg-to-SLA ratio highlighted with a ⚠️ badge

---

### Chart 4 — MCQ Video Coverage by Subject (Stacked Bar Chart)

- X-axis: subjects (Math, Physics, Chemistry, Biology, etc.)
- Y-axis: question count
- Stacked bars:
  - Green: questions with PUBLISHED video
  - Blue: questions with a video job In Production
  - Grey: questions with no video job
- Shows the gap clearly — how much of each subject's question bank needs video work
- Click a bar segment → opens E-05 filtered to that subject + relevant status

---

### Chart 5 — Production Volume by Content Type (Pie Chart)

- Slices: Concept Explainer · Problem Walkthrough · Revision Quick · Shorts
- Shows distribution of what types of videos are being produced
- Legend with counts + %

---

### Chart 6 — Revision Rate by Stage (Bar Chart)

- X-axis: stages
- Y-axis: % of submissions that required revision (revision_requested / total_submitted)
- High revision rate at Script Review → scripts need improvement
- High revision rate at QA → final edit quality is low
- Tooltip: "{N} revisions / {M} total submissions = {%}%"

---

### Chart 7 — QA Score Trends (Line Chart)

**Purpose:** Track whether video quality is improving over time, and surface which subjects or content types consistently score low.

- **Part-load route:** `/content/video/analytics/?part=qa-score-chart`
- Recharts `LineChart` with `ResponsiveContainer`
- X-axis: week (ISO week number + year)
- Y-axis: average score (1.0–5.0)
- Three lines:
  - 🔵 Avg Accuracy Score (`video_qa_review.accuracy_score`)
  - 🟢 Avg A/V Quality Score (`video_qa_review.av_quality_score`)
  - 🟡 Avg Subtitle Score (`video_qa_review.subtitle_score`) — calculated only for reviews where subtitles were present
- Reference line at 4.0 (target quality threshold) — dashed grey
- Tooltip on hover: "Week {N}: Accuracy {X.X} · A/V {X.X} · Subtitles {X.X} · {N} reviews"
- **Filter panel (right of chart):** Group by: All · Subject · Content Type · QA Reviewer
  - When "Subject" selected: each subject gets its own coloured line (max 6 subjects shown; "Others" aggregated)
  - When "QA Reviewer" selected: shows per-reviewer average scores (role labels only, no names — DPDPA)
- **No-data state:** "No QA reviews in selected date range."
- Click a week point → opens Activity Log below pre-filtered to that week's QA events
- **Filter persistence:** The Group By filter selection is NOT URL-bookmarkable (HTMX-driven state). Filters reset when navigating away from the page. To preserve a view, take a screenshot or use the "Download Report" export.
- **Auto-refresh:** Chart 7 does NOT auto-refresh (to minimise data aggregation load). It re-renders when the global date range selector changes. KPI tiles continue to auto-refresh every 120s independently.

**Score distribution breakdown (below chart, data table):**

| Score Range | Accuracy | A/V Quality | Subtitle |
|---|---|---|---|
| 5 (Excellent) | {N} reviews ({%}%) | {N} ({%}%) | {N} ({%}%) |
| 4 (Good) | — | — | — |
| 3 (Average) | — | — | — |
| 2 (Below standard) | — | — | — |
| 1 (Fail) | — | — | — |

---

## 6. Activity Log

Full chronological log of all pipeline events across all jobs. Searchable and filterable.

#### Search & Filter Bar

- Search: job title, event description. Debounced 300ms.
- Filters (collapsible):

| Filter | Control |
|---|---|
| Event Type | Multi-select: Job Created · Stage Completed · Revision Requested · Job Published · Job Cancelled · SLA Breached · QA Pass · QA Fail |
| Subject | Multi-select |
| Date Range | Date range |
| Stage | Multi-select |

Active pills + "Reset All".

#### Activity Log Table (Sortable, Selectable, Responsive)

| Column | Sortable | Notes |
|---|---|---|
| Timestamp | Yes (default: DESC) | Datetime |
| Event | No | Human-readable event description |
| Job Title | Yes | Clickable → E-05 job drawer |
| Stage | No | Stage where event occurred (if applicable) |
| Actor | No | Role label (DPDPA — no personal name) |
| SLA Status | No | "On Time" / "Late {N}d" at time of event |

**Pagination:** 50 rows per page (text-only, no thumbnails).
**Export:** "Download Activity Log (CSV)" — same columns, full date range (not paginated).

---

## 7. Role-Specific Views

**Content Producer (82) / Content Director (18):** All 6 charts + full activity log.

**Production roles (83–89):** Reduced view — only see their own stage metrics:
- My Stage KPIs (4 tiles: My Submissions · My Revisions · My Avg Time · My SLA Rate)
- Chart 2 filtered to their stage only
- Activity log filtered to events involving their own stage assignments

---

## 8. Export

**"Download Report" button (Producer + Director only):**
- Opens export modal:
  - Date range: pre-filled from global selector
  - Include: KPI summary (checkbox, default on) · Charts as PNG (checkbox) · Activity Log CSV (checkbox)
  - Format: **PDF report** or **ZIP (CSV + PNGs)** — see format contents below:

| Format | Contents |
|---|---|
| **PDF** | Single PDF document: KPI summary table (if checked) on page 1 · each selected chart as an inline image on subsequent pages (if "Charts as PNG" checked) · Activity Log as a formatted table on final pages (if checked) — **PDF Activity Log is truncated to 2,000 rows**; use ZIP for full untruncated data |
| **ZIP** | Archive of separate files: `kpi_summary.csv` (if KPI summary checked) · `chart_1_throughput.png` through `chart_7_qa_scores.png` (if "Charts as PNG" checked, one PNG per chart at 1920×1080) · `activity_log.csv` (if checked, full untruncated data) |

> Both PDF and ZIP download links expire after 15 minutes.
- "Generate Report" → Celery task generates report. Toast: ℹ️ "Report generating — download link will appear in {N} seconds" (6s)
- Download link appears when ready (inline on page, not email). Link valid for 15 minutes.

---

## 9. Access Control

| Gate | Rule |
|---|---|
| Page access | All Div E production roles (82–89), Content Director (18) |
| Full analytics (all charts + activity log) | Content Producer (82), Content Director (18) |
| Own-stage analytics | Production roles 83–89 |
| Export | Content Producer (82), Content Director (18) only |

---

## 10. Edge Cases & Error States

| Scenario | Behaviour |
|---|---|
| No jobs published in selected period | Throughput chart shows all-zero bars. KPI tiles show 0 or "—". Empty state below chart: "No jobs published in this period." |
| MCQ coverage at 0% | Coverage chart shows all grey bars. KPI tile shows "0%" in red. CTA: "Import from MCQ Bank →" link to E-05 Tab 3. |
| Data aggregation takes > 2s | Charts show skeleton while loading. `hx-indicator` spinner on each chart container. |
| Export generates a large report | Progress spinner in export modal. If Celery takes > 30s, a retry message appears: "Report is taking longer than usual — try again or reduce the date range." |
| Activity log query is slow (> 5s) | Table shows loading shimmer with "Loading activity log…" message. |

---

## 11. UI Patterns

### Empty States

| Context | Heading | Subtext | CTA |
|---|---|---|---|
| No data (fresh pipeline) | "No production data yet" | "Analytics will populate as jobs move through the pipeline." | "Go to Job Tracker →" |
| No MCQ coverage | "0% MCQ video coverage" | "No published questions have video explanations yet. Import from the MCQ bank to start." | "Import from MCQ Bank →" |
| Activity log empty | "No activity in this period" | "Extend the date range or try different filters." | "Reset Filters" |

### Toast Messages

| Action | Toast |
|---|---|
| Report generating | ℹ️ "Report generating — download will appear shortly" (6s) |
| Report ready | ✅ "Report ready — [Download]" (persistent until downloaded) |
| Export failed | ❌ "Report generation failed — try again" (persistent) |

### Loading States

- KPI strip: 6 rectangle shimmers
- Each chart: grey rectangle placeholder matching chart height
- Activity log: 8-row shimmer (timestamp + text + 3 pill shimmers)

### Responsive Behaviour

| Breakpoint | Behaviour |
|---|---|
| Desktop (≥1280px) | Charts in 2×3 grid; activity log full width below |
| Tablet (768–1279px) | Charts stack vertically in single column |
| Mobile (<768px) | KPI strip scrolls horizontally; charts replaced by "View full analytics on desktop"; activity log shows last 10 events with "View All" link |

---

*Page spec complete.*
*E-10 covers: throughput → SLA compliance → bottleneck detection → MCQ coverage → revision rate → activity log → export.*
