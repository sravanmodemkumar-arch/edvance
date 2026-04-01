# I-07 — SLA & Performance Reports

**Route:** `GET /support/reports/`
**Method:** Django CBV (`TemplateView`) + HTMX part-loads
**Primary role:** Support Manager (#47)
**Also sees (restricted):** L1 (#48) — own stats only; L2 (#49) — own stats only; L3 (#50) — own stats only; Support Quality Lead (#108) — quality metrics section only
**No access:** Onboarding Specialist (#51), Training Coordinator (#52)

---

## Purpose

Operational intelligence for support leadership. Surfaces SLA compliance trends, ticket volume patterns, per-agent performance, CSAT trends, category distribution, and escalation analysis over configurable time windows. Also the central view for the Support Quality Lead's audit metrics.

---

## Data Sources

| Section | Source | Cache TTL |
|---|---|---|
| SLA compliance chart | `support_ticket` aggregated by tier + date + SLA met/breached | 15 min |
| Ticket volume chart | `support_ticket` grouped by `created_at::date` + category | 15 min |
| Category breakdown | `support_ticket` grouped by category | 15 min |
| Agent performance table | `support_ticket` grouped by `assigned_to_id` | 15 min |
| CSAT trend chart | `support_ticket.csat_score` by date | 15 min |
| Escalation analysis | `support_ticket_escalation` grouped by tier + reason | 15 min |
| Quality audit metrics | `support_quality_audit` aggregated | 15 min |
| Weekly report snapshot | `support_weekly_report` (pre-computed by Celery Task 5) | 60 min |

All caches bypass with `?nocache=true` (Support Manager only).

---

## URL Parameters

| Param | Values | Effect |
|---|---|---|
| `?period` | `7d`, `30d`, `90d`, `custom` | Reporting window; default `30d` |
| `?from` | `YYYY-MM-DD` | Start date for custom period |
| `?to` | `YYYY-MM-DD` | End date for custom period |
| `?tier` | `L1`, `L2`, `L3`, `all` | Filter by tier; default `all` |
| `?agent_id` | user_id | Filter to single agent's stats |
| `?category` | Any ticket category | Filter by category |
| `?institution_type` | `SCHOOL`, `COLLEGE`, `COACHING`, `GROUP` | Filter by institution segment |
| `?nocache` | `true` | Bypass Memcached (Support Manager only) |

---

## HTMX Part-Load Routes

| Part | Route | Trigger |
|---|---|---|
| SLA compliance chart | `?part=sla_chart` | Page load + filter change |
| Volume chart | `?part=volume_chart` | Page load + filter change |
| Category pie | `?part=category_pie` | Page load + filter change |
| Agent performance table | `?part=agent_table` | Page load + filter change |
| CSAT trend chart | `?part=csat_chart` | Page load + filter change |
| Escalation chart | `?part=escalation_chart` | Page load + filter change |
| Quality metrics | `?part=quality_metrics` | Page load + filter change |
| Weekly snapshot | `?part=weekly_snapshot` | Page load; 60-min TTL; NOT re-triggered by filter changes (uses fixed prior-week data) |
| SLA config table | `?part=sla_config` | Page load only (static config; only changes when Platform Admin edits Django Admin) |

---

## Page Layout

```
┌──────────────────────────────────────────────────────────────────┐
│  Support Reports   Period: [30d ▼]  Tier: [All ▼]  [Export PDF] │
│  [Apply Filters]                           [?nocache=true link]  │
├──────────────────────────────────────────────────────────────────┤
│  SUMMARY KPI ROW (4 tiles)                                       │
├──────────────────────┬───────────────────────────────────────────┤
│  SLA COMPLIANCE CHART│  CSAT TREND CHART                         │
├──────────────────────┴───────────────────────────────────────────┤
│  TICKET VOLUME CHART (stacked bar)                               │
├──────────────────────┬───────────────────────────────────────────┤
│  CATEGORY BREAKDOWN  │  ESCALATION ANALYSIS                      │
├──────────────────────┴───────────────────────────────────────────┤
│  AGENT PERFORMANCE TABLE                                         │
├──────────────────────────────────────────────────────────────────┤
│  QUALITY AUDIT METRICS (Quality Lead / Support Manager)          │
├──────────────────────────────────────────────────────────────────┤
│  WEEKLY SNAPSHOT (collapsible; prior week pre-computed)          │
├──────────────────────────────────────────────────────────────────┤
│  SLA CONFIGURATION REFERENCE (Support Manager only; static)      │
└──────────────────────────────────────────────────────────────────┘
```

---

## Components

### Period Selector + Filter Bar

```
Period:  [7d]  [30d ●]  [90d]  [Custom]
Tier:    [All ▼]     Category: [All ▼]     Agent: [All ▼]     Institution type: [All ▼]
[Apply]  [Reset]
```

Custom period → date range picker appears inline. Max range: 365 days.

Filters apply to all charts simultaneously via HTMX broadcast (one filter change reloads all `?part=` endpoints in parallel).

---

### Summary KPI Row (4 tiles)

| Tile | Value | Colour logic |
|---|---|---|
| Total Tickets | COUNT for selected period | Grey |
| SLA Compliance | % tickets that met resolution SLA | Red (<85%), Amber (85–94%), Green (≥95%) |
| Avg CSAT | Average CSAT score for period | Red (<3.5), Amber (3.5–4.0), Green (≥4.0) |
| Avg Resolution Time | Mean resolution time for RESOLVED tickets | — |

Tile click: scrolls to relevant chart.

---

### SLA Compliance Chart

**Chart type**: Grouped bar chart (Chart.js). One group per day (or week if period > 30d).

Per group: three bars — L1, L2, L3. Bar height = compliance % (0–100%).
Horizontal reference lines at: L1 target (95%), L2 target (90%), L3 target (85%) — dashed.

Hover tooltip: "L1: 96.2% (124/129 tickets met SLA) · 5 breaches"

Below chart: summary table:

| Tier | Total | Met SLA | Breached | Compliance % | Target | Status |
|---|---|---|---|---|---|---|
| L1 | 847 | 812 | 35 | 95.9% | 95% | ✓ On target |
| L2 | 312 | 289 | 23 | 92.6% | 90% | ✓ On target |
| L3 | 87 | 71 | 16 | 81.6% | 85% | ✗ Below target |

L3 below target: row highlighted red. [View L3 Breached Tickets →] links to I-02 with appropriate filter.

---

### CSAT Trend Chart

**Chart type**: Line chart (Chart.js). X-axis: daily points for ≤30d; weekly points for >30d.

**Dual Y-axis chart**: left Y-axis (1–5) for CSAT score; right Y-axis (0–100%) for response rate. Both axes are labelled. Chart.js `y` and `y1` axes configuration.

Two series:
- Average CSAT score (primary line, blue, left Y-axis 1–5)
- Ticket response rate: `COUNT(csat_submitted_at IS NOT NULL) / COUNT(status IN ('RESOLVED','CLOSED'))` for the period; secondary line, grey dashed, right Y-axis 0–100%

Target line at 4.0 (dashed red horizontal).

Hover tooltip: "5 Nov · CSAT: 3.8 (42 responses, 68% response rate)"

If CSAT drops below 3.5 for 3+ consecutive data points: orange alert banner below chart: "⚠ CSAT dropped below 3.5 for 3 consecutive days. Review recent ticket quality."

[Download CSAT Data CSV] button (Support Manager only).

---

### Ticket Volume Chart

**Chart type**: Stacked bar chart (Chart.js). X-axis: days (or weeks for long periods).

Stacked series by top 5 categories (others collapsed into "Other"):
- LOGIN_ISSUE, EXAM_ACCESS, TECHNICAL_BUG, RESULT_QUERY, BILLING_QUERY, Other

Hover tooltip: breakdown per category for that period.

Below chart: top 5 categories ranked by volume for the selected period with % of total.

**Exam-day markers**: On dates where a live exam occurred, a yellow vertical marker is drawn on the X-axis. Implementation: server-side query `SELECT DISTINCT DATE(start_date) FROM exam WHERE DATE(start_date) BETWEEN {from} AND {to}` via read-only service account (Division F DB read replica); result cached for 60 min. Marker tooltip on hover: exam name + student count. If Division F DB is unavailable, markers are omitted silently; a subtle footnote appears below the chart: "* Exam-day markers unavailable (Division F data unreachable)" — so the Support Manager knows the markers may be missing rather than assuming no exams ran.

---

### Category Breakdown (pie chart)

**Chart type**: Doughnut chart (Chart.js). One segment per category.

Hover: category name + count + % of total.

Click on segment: applies category filter to all charts (HTMX broadcast).

Below pie: table form of same data, sortable by count or % of total.

---

### Escalation Analysis

Two mini charts side-by-side:

**Left — Escalation Rate by Tier:**
Bar chart: L1→L2 escalation rate (% of L1 tickets escalated); L2→L3 escalation rate.
Target: L1 escalation rate < 15%; L2 escalation rate < 30%.

**Right — Escalation Reason Distribution:**
Horizontal bar chart of escalation reasons from `support_ticket_escalation.reason` (grouped by type).

Below both charts:

Top 5 categories with highest escalation rates — table with [View Tickets →] link per category that opens I-02 filtered.

---

### Agent Performance Table

**Support Manager view (full team):**

Columns: Agent | Tier | Tickets Handled | Avg Resolution Time | SLA Met % | CSAT Avg | Escalations Received | Escalations Initiated | Quality Score Avg

Sortable by any column. **Default sort: Tickets Handled DESC** (busiest agents first; most actionable view for workload balancing). Column header shows sort indicator (↓ on Tickets Handled by default).

Rows with SLA compliance below tier target: highlighted amber/red.
Rows with CSAT < 3.5: highlighted red.

[View Agent Queue →] per row: links to I-02 filtered to that agent.
[View Quality Audits →] per row (Quality Lead / Support Manager): links to I-07 quality section filtered to that agent.

**L1/L2/L3 agent view (own stats only):**
Single-row version showing only their own metrics. No other agents visible.

---

### Quality Audit Metrics (Support Manager + Quality Lead)

Summary of quality audit activity for the period.

**KPI row:**
- Tickets Audited: COUNT for period
- Audit Coverage: % of closed tickets that were audited
- Avg Quality Score: mean of `quality_audit_score` 1–5
- Score Distribution: mini horizontal bar (5 segments for 1–5)

**Agent Quality Scores table:**

| Agent | Tier | Audited Tickets | Avg Score | Trend vs Prior Period |
|---|---|---|---|---|
| Priya Sharma | L1 | 12 | 4.2 | ↑ +0.3 |
| Rahul Kumar | L2 | 8 | 3.6 | ↓ -0.4 |

Agents with avg score < 3.0: row highlighted red.

**Open Gap Flags**: Count of unresolved KB gap flags. [View Gaps →] links to I-06 tab=gaps.

**CSAT vs Quality Score correlation** (mini scatter chart): X=agent quality score (from `support_quality_audit`), Y=average CSAT score for that agent's tickets for the period. Each dot = one agent. Minimum 5 audited tickets required to plot an agent's dot; agents with <5 audits shown as greyed-out dots with tooltip "Insufficient audit data (N audits)". Significant outliers (quality score >4 but CSAT <3, or vice versa) shown with a red ring and tooltip "Outlier — investigate". Quality Lead export of this chart includes the underlying data table.

---

### SLA Configuration Reference Table (Support Manager only)

Static read-only table showing current `support_sla_config` values at the bottom of the page. **Not filterable; not part of the chart period selection.** Shows current live thresholds.

```
Current SLA Thresholds (as configured in Django Admin)
────────────────────────────────────────────────────────
Tier  Priority   First Response   Resolution    Exam-Day Override
L1    CRITICAL   30 min           120 min       15 min / 60 min ✓
L1    HIGH        60 min           240 min       —
L1    MEDIUM     120 min          480 min       —
L1    LOW        240 min          1,440 min     —
L2    CRITICAL    60 min           240 min       30 min / 120 min ✓
...
```

Each row shows `is_exam_day_override` rows with a "✓" badge. Label: "To change these thresholds, contact Platform Admin." No edit controls.

---

### Weekly Snapshot

Pre-computed data from `support_weekly_report` (Celery Task 5; 60-min Memcached TTL). Shown as a collapsible section at the bottom of the page, always using the prior complete week (Mon–Sun) regardless of the period selector.

```
┌──────────────────────────────────────────────────────────┐
│  Weekly Snapshot (4 Nov – 10 Nov 2024)  [Collapse ▲]    │
├───────────────────┬──────────────────────────────────────┤
│  Total tickets: 1,247    SLA compliance: L1 96%, L2 91%, L3 84%  │
│  Avg CSAT: 4.1 (68% response rate)                      │
│  Escalation rates: L1→L2 11%, L2→L3 8%                 │
│  Top categories: LOGIN_ISSUE (312) · OTP_FAILURE (187)  │
└──────────────────────────────────────────────────────────┘
```

[Export Weekly CSV] — downloads the `support_weekly_report` row as CSV.

Note: the Weekly Snapshot always reflects the prior full week and is NOT affected by the period selector. For custom period analysis, use the main charts above.

---

### [Export PDF] Button

Generates a PDF snapshot of the current view with all charts (server-side chart rendering via headless Chromium). Filename: `support_report_{period}_{date}.pdf`. This is an **on-demand Celery task** — dispatched to the `exports` queue when the button is clicked (not a scheduled task). The task renders all active `?part=` chart endpoints and compiles them into a PDF. Download link emailed to Support Manager when ready (typically 30–120s depending on queue depth).

[Export CSV] button below each chart: downloads the raw data for that specific chart.

---

### Report Scheduling (Support Manager only)

**[Schedule Report ▼]** button in the header bar (next to [Export PDF]):

```
Schedule Automated Report

Frequency:  ● Weekly (Monday 09:00 IST)   ○ Monthly (1st of month)
Period:     [30d ▼]
Format:     [✓ PDF]  [✓ CSV summary]
Recipients: [support.manager@platform.in    ] [+ Add recipient]
            (email addresses; space-separated)

[Cancel]   [Save Schedule]
```

- Saves a `support_report_schedule` record (not a model exposed in Division I data model — stored as a simple JSON config in Support Manager's user preferences).
- Celery Task 5 (`generate_support_weekly_report`) already runs Mondays 09:00 IST; if a schedule is active, it also emails the PDF/CSV to the configured recipients list.
- **Multiple recipients supported**: space/comma separated; validated as email addresses.
- [Cancel Schedule] button appears in the same dropdown when a schedule is active; cancels by clearing the schedule config.
- If the Support Manager wants a one-off report immediately: use [Export PDF] instead.

---

## Role-Based View Differences

| Section | Support Manager (#47) | L1/L2/L3 agents | Quality Lead (#108) |
|---|---|---|---|
| Period selector + filters | Full | Own stats only; period selector works but data scoped | Full |
| Summary KPI row | All 4 tiles | All 4 tiles (own scope) | All 4 tiles |
| SLA compliance chart | Full team view | **Own tier only, own metrics line only** — e.g. L1 agent sees only L1 bar and their personal resolution time, not other agents | Full (read-only) |
| CSAT trend chart | Full | Own CSAT only | Full (read-only) |
| Volume chart | Full | Hidden | Full (read-only) |
| Category breakdown | Full | Own ticket categories only | Full (read-only) |
| Escalation analysis | Full | Own escalations only | Full (read-only) |
| Agent performance table | Full team | Own row only | Full team (read-only) |
| Quality audit metrics | Full | Hidden | Full |
| Export PDF / CSV | Enabled | Own data CSV only; no PDF | PDF + CSV enabled |

---

## Edge Cases

1. **Selected period has 0 tickets**: All charts show empty state with "No tickets in this period." and the period range displayed. KPI tiles show 0.
2. **CSAT response rate < 10%**: Warning below CSAT chart: "Low CSAT response rate ({N}%). Scores may not be statistically significant." Avg CSAT tile shown with "⚠ Low sample" label.
3. **Custom date range > 365 days**: Validation error: "Reports are available for a maximum of 365 days. Please narrow your date range."
4. **Agent with 0 tickets in period**: Row shown in agent table with all zeros; not filtered out (the Support Manager may be looking for why an agent had no activity).
5. **Quality audit coverage < 5%**: Info note in quality section: "Low audit coverage this period. Consider increasing sample rate." (No auto-action; Support Quality Lead decides sampling rate.)
6. **L3 SLA compliance below 85% for 3+ consecutive weeks**: No auto-escalation in reports page; this is a human-reviewed page. Alert banner shown but action is at Support Manager discretion.
7. **PDF export during high-load period**: If export job queues, page shows "Export queued. You will receive it via email shortly." No blocking loader.
8. **Period spans a major exam day surge**: Volume chart will show a spike; a yellow vertical marker is drawn on the X-axis on dates where a live exam ran (based on Division F exam data join). Hover shows exam name and student count.

---

## Notifications (via F-06)

- SLA compliance drops below target for any tier for 3 consecutive days → weekly Celery report triggers push notification to Support Manager
- PDF export ready → email to Support Manager with download link
- CSAT weekly report available → push notification to Support Manager every Monday 09:00 IST
