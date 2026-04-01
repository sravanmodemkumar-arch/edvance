# J-08 — Customer Success Reports

**Route:** `GET /csm/reports/`
**Method:** Django `TemplateView` + HTMX part-loads
**Primary roles:** CSM (#53), CS Analyst (#93)
**Also sees:** Account Manager (#54) — own portfolio section only; Escalation Manager (#55) — escalation metrics only; Renewal Executive (#56) — renewal metrics only; ISM (#94) — implementation success metrics only

---

## Purpose

Executive-grade CS analytics. Surfaces GRR/NRR retention metrics, churn root-cause analysis, cohort health evolution, CSM performance benchmarks, and playbook effectiveness. The CSM uses this for quarterly business reviews with EduForge leadership and for identifying structural patterns in churn (e.g., coaching centres churning more during coaching season). The CS Analyst uses it as the primary analytical workspace.

---

## Data Sources

| Section | Source | Cache TTL |
|---|---|---|
| Retention KPI strip | `csm_weekly_snapshot` (pre-computed) | 60 min |
| GRR/NRR trend | `csm_renewal` closed by quarter for last 8 quarters | 15 min |
| Churn analysis | `csm_renewal` WHERE stage='CHURNED' for selected period | 15 min |
| Cohort analysis | `institution` JOIN `csm_health_history` grouped by join_quarter — `join_quarter` is derived from `institution.created_at` (the date the institution record was first created in EduForge, i.e., contract start date); formatted as `YYYY-QN` (e.g., Q2 2024) | 15 min |
| CSM performance table | `csm_touchpoint` + `csm_renewal` + `csm_nps_survey` + `csm_institution_health` grouped by csm_id | 15 min |
| Playbook effectiveness | `csm_playbook_instance` + `csm_institution_health` pre/post comparison | 15 min |
| Health score distribution | `csm_institution_health.health_score` histogram | 15 min |
| Implementation success | `csm_account_assignment` + `csm_institution_health` + `csm_playbook_instance` for ISM accounts | 15 min |
| Escalation metrics | `csm_escalation` aggregated | 15 min |

All chart data pre-computed by Celery Task J-5 (weekly snapshot). Live queries used only for selected date range overrides.

`?nocache=true` bypasses cache (CSM + CS Analyst only).

---

## URL Parameters

| Param | Values | Default | Effect |
|---|---|---|---|
| `?period` | `this_quarter`, `last_quarter`, `last_2q`, `last_4q`, `last_8q`, `ytd`, `custom` | `last_4q` | Reporting window for all charts |
| `?from` | `YYYY-MM-DD` | — | Custom period start |
| `?to` | `YYYY-MM-DD` | — | Custom period end |
| `?type` | `school`, `college`, `coaching`, `group` | `all` | Segment filter applied to all sections |
| `?csm_id` | user_id | `all` | Filter CSM performance table to one CSM |
| `?section` | `overview`, `churn`, `cohort`, `csm_performance`, `playbooks`, `escalations`, `implementations` | `overview` | Scroll anchor / active section highlight |
| `?export` | `pdf` | — | Export full report as PDF (CSM + Analyst) |
| `?export` | `csv` | — | Export underlying data as CSV (Analyst only) |
| `?nocache` | `true` | — | Bypass Memcached (CSM + CS Analyst only) |

---

## HTMX Part-Load Routes

| Part | Route | Trigger |
|---|---|---|
| Retention KPI strip | `?part=retention_kpi` | Page load + period change |
| GRR/NRR trend chart | `?part=grr_nrr_trend` | Page load + period change + type filter |
| Churn analysis section | `?part=churn_analysis` | Page load + period change + type filter |
| Cohort analysis | `?part=cohort_analysis` | Page load + period change |
| CSM performance table | `?part=csm_performance` | Page load + period change + csm_id filter |
| Playbook effectiveness | `?part=playbook_effectiveness` | Page load + period change |
| Health distribution | `?part=health_dist` | Page load + type filter |
| Escalation metrics | `?part=escalation_metrics` | Page load + period change |
| Implementation success | `?part=implementation_metrics` | Page load + period change |

---

## Page Layout

```
┌─────────────────────────────────────────────────────────────────────┐
│  CS Reports   Period: [Last 4 Quarters ▼]   Segment: [All ▼]        │
│  [Export PDF]  [Export CSV]  (role-gated)                           │
├─────────────────────────────────────────────────────────────────────┤
│  RETENTION KPI STRIP                                                │
├──────────────────────────┬──────────────────────────────────────────┤
│  GRR / NRR TREND CHART   │  HEALTH SCORE DISTRIBUTION               │
├──────────────────────────┴──────────────────────────────────────────┤
│  CHURN ANALYSIS (by reason, by segment, by ARR band)                │
├─────────────────────────────────────────────────────────────────────┤
│  COHORT ANALYSIS                                                    │
├──────────────────────────┬──────────────────────────────────────────┤
│  CSM PERFORMANCE TABLE   │  PLAYBOOK EFFECTIVENESS TABLE            │
├──────────────────────────┴──────────────────────────────────────────┤
│  ESCALATION METRICS                                                 │
├─────────────────────────────────────────────────────────────────────┤
│  IMPLEMENTATION SUCCESS METRICS (ISM + CSM)                        │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Retention KPI Strip (6 tiles)

```
┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐
│ 91.2%      │ │ 94.8%      │ │ 3.8%       │ │ 2.3%       │ │ +38        │ │ 72         │
│ GRR        │ │ NRR        │ │ Logo Churn │ │ Expansion  │ │ NPS Score  │ │ Avg Health │
│ (Gross     │ │ (Net Rev   │ │ Rate       │ │ Rate (ARR  │ │            │ │ Score      │
│ Rev Ret.)  │ │ Retention) │ │            │ │ growth)    │ │            │ │            │
└────────────┘ └────────────┘ └────────────┘ └────────────┘ └────────────┘ └────────────┘
```

- **GRR:** MIN(ARR_renewed_base, ARR_due) / ARR_due (capped at 100%; excludes expansion delta; covers contract renewals only — does not capture mid-period cancellations). Green if ≥ 90%, amber 80–89%, red < 80%.
- **NRR:** (ARR_renewed_base + expansion_arr) / ARR_due (can exceed 100% when net expansion outpaces churn). Green if ≥ 100%, amber 90–99%, red < 90%.
- **ARR_renewed_base** = `SUM(arr_value_paise WHERE stage='RENEWED' AND expansion_arr_paise IS NULL)` — base renewal ARR, excludes expansion-only contracts.
- **expansion_arr** = `SUM(expansion_arr_paise WHERE stage='EXPANSION')` — net new ARR from expanded seats/plans.
- **ARR_due** = `SUM(arr_value_paise WHERE renewal_date BETWEEN period_start AND period_end)` — total ARR up for renewal in the period.
- **Logo Churn Rate:** Count(institutions where `stage='CHURNED'` AND `lost_at BETWEEN period_start AND period_end`) / Count(institutions with an active subscription at `period_start`) × 100. "Institutions at period start" = institutions with `csm_renewal.stage NOT IN ('CHURNED')` as of `period_start` date — so institutions that joined mid-period are included in the denominator only for the next period. Example: 44 churned institutions in Q1 2026 / 2,040 institutions active at Jan 1 2026 = 2.16% logo churn.
- **Expansion Rate:** Sum(expansion_arr) / ARR_due × 100.
- **NPS Score:** From `csm_weekly_snapshot` most recent.
- **Avg Health Score:** Platform-wide from `csm_weekly_snapshot`.

Delta vs prior period shown below each tile.

---

## GRR / NRR Trend Chart

Dual-line chart — quarterly GRR and NRR over last 8 quarters.

- X-axis: quarter labels (Q1 2024, Q2 2024, ...)
- Y-axis: 0–120% (NRR can exceed 100%)
- Line 1 (blue): GRR %
- Line 2 (teal): NRR %
- Dashed reference lines at 85% (GRR target) and 100% (NRR parity)
- Bar overlay (secondary Y-axis, right): ARR churned per quarter (₹Cr, red bars)

Hover tooltip: GRR % · NRR % · ARR churned · ARR expanded · Quarter.

---

## Health Score Distribution

Histogram (10 buckets: 0–9, 10–19, ..., 90–100):

```
Count
300 │                                    ┌───┐
250 │                          ┌───┐     │   │ ┌───┐
200 │                    ┌───┐ │   │     │   │ │   │
150 │              ┌───┐ │   │ │   │     │   │ │   │ ┌───┐
100 │        ┌───┐ │   │ │   │ │   │ ┌───┤   │ │   │ │   │
 50 │  ┌───┐ │   │ │   │ │   │ │   │ │   │   │ │   │ │   │
  0 └──┴───┴─┴───┴─┴───┴─┴───┴─┴───┴─┴───┴───┴─┴───┴─┴───┴
      0-9  10-19 20-29 30-39 40-49 50-59 60-69 70-79 80-89 90-100
      [■ CHURNED_RISK]  [■ CRITICAL]  [■ AT_RISK]  [■ ENGAGED]  [■ HEALTHY]
```

Shows current distribution snapshot. Bars coloured by tier. Hover: count + % of total.

---

## Churn Analysis

Three sub-charts in a row:

### By Reason (horizontal bar chart)
```
PRICING          ████████████████  34%  (8 institutions · ₹4.2L)
LOW_USAGE        ██████████        22%  (5 · ₹2.1L)
SWITCHED_COMP    ████████          17%  (4 · ₹3.8L)
BUDGET_CUT       ██████            13%  (3 · ₹1.4L)
ADMIN_TURNOVER   ████              9%   (2 · ₹0.8L)
OTHER            ██                5%   (1 · ₹0.2L)
```

Hovering a bar shows: churn_reason · count · total ARR lost · institution types affected.

### By Segment (stacked bar per type)
Shows churn count and ARR by institution type (Schools / Colleges / Coaching / Groups) for selected period.

### By ARR Band (histogram)
```
₹0–50K         ████  8 institutions
₹50K–1L        ████████  16 institutions
₹1L–3L         ██████  12 institutions
₹3L–6L         ███  6 institutions
> ₹6L          █  2 institutions
```

Bands: ₹0–50K · ₹50K–1L · ₹1L–3L · ₹3L–6L · > ₹6L.

### Churned Institution Table
Below charts: scrollable table of all churned institutions in period.

| Column | Description |
|---|---|
| Institution | Name (link → J-03) + type |
| ARR | ₹ value |
| Churn Date | Date |
| Reason | churn_reason badge |
| Health at Churn | Score at time of churn (from last health snapshot before `lost_at`) |
| Last Touchpoint | Relative time before churn date |
| Open Escalations | Count at time of churn |
| NPS (last) | Last NPS score or "—" |

Sorted by churn_date DESC. Exportable by CS Analyst.

---

## Cohort Analysis

**What it shows:** For institutions that joined EduForge in the same quarter (cohort, derived from `institution.created_at`), how has their average health score evolved over time? Each cohort row represents all institutions whose `created_at` falls within that calendar quarter.

Cohort table (rows = join quarter, columns = quarters since joining):

```
Join Quarter   Q0     Q1     Q2     Q3     Q4     Q5     Q6
Q2 2024        72     69     74     77     80     79     81
Q3 2024        70     68     71     75     79     82     —
Q4 2024        68     65     69     73     77     —      —
Q1 2025        65     63     67     72     —      —      —
Q2 2025        63     62     —      —      —      —      —
Q3 2025        61     —      —      —      —      —      —
```

Cell colour: green if ≥ 75, amber if 60–74, red if < 60. "—" = cohort not yet that old.

Q0 = first quarter (onboarding). Typically lower health. Q1+ = post-onboarding trajectory.

**Key insight this reveals:** If Q0 scores are consistently < 65 for recent cohorts, onboarding quality is degrading. If Q1→Q2 score drops, the ISM handoff to AM is losing continuity.

**Filter:** Type selector (All / School / College / Coaching / Group) changes cohort segmentation.

---

## CSM Performance Table

Per-CSM breakdown for the selected period. Sorted by `avg_health_score` ASC (lowest first = needs attention).

| Column | Description |
|---|---|
| CSM | Avatar + name |
| Portfolio | Count of assigned institutions |
| Avg Health Score | Average across portfolio; colour-banded |
| Health Δ | Change vs prior period |
| Renewal Rate | Count(RENEWED) / Count(due) × 100% in period |
| NPS Avg | Average NPS score across surveys sent by this CSM in period |
| Touchpoints (30d) | Count of touchpoints logged |
| Open Escalations | Count of open escalations in their portfolio |
| Active Playbooks | Count in their portfolio |

**Role visibility:** CSM (#53) sees all CSMs. AM and others see own row only (greyed "N/A" for others).

**Warm-handoff context:** When a CSM's portfolio row is expanded (click to expand), a sub-row shows accounts previously managed by a different CSM (sourced from `csm_account_assignment_history`). Displays "Previously managed by [Name] until [date]" — helps identify accounts that may have relationship continuity risk after a CSM reassignment.

**Note below table:** "Touchpoint count reflects activity volume only, not quality. High count with low NPS may indicate reactive rather than proactive engagement."

---

## Playbook Effectiveness Table

Shows per-template health score delta for institutions that completed a playbook in the selected period.

| Column | Description |
|---|---|
| Template | Name + trigger type |
| Instances (completed) | Count completed in period |
| Avg Duration (days) | Actual vs estimated |
| Health Δ (pre → post) | Avg health score 30 days before start vs 30 days after completion |
| GRR Impact | Renewal rate for institutions that completed this playbook vs didn't (in same period) |
| Task Completion Rate | tasks_completed / tasks_total × 100% across completed instances |

**Health Δ** is the key column. Positive = playbook correlates with improvement. Example: "AT_RISK_RECOVERY → +14 avg health delta" means institutions that completed this playbook improved by 14 points on average.

Note: Correlation, not causation. Displayed with asterisk and footnote.

**Empty state:** "Not enough completed playbook data for the selected period. Data appears after at least 5 completed instances per template."

---

## Escalation Metrics

Two-chart row:

**Left: Escalation volume trend** — Bar chart by month for last 12 months. Bars stacked by severity (P1/P2/P3). Trend line for resolved. Y-axis: count. Hover: month + counts + resolution rate.

**Right: Mean Time to Resolve (MTTR) by severity**
```
P1 CRITICAL   ████████████  18h avg  (target: 24h)  ✓
P2 HIGH       ██████████████████████  51h avg  (target: 72h)  ✓
P3 MEDIUM     ████████████████████████████████████  9.2d avg  (target: 7d)  ✗
```

Horizontal bars. Green if within target, red if over. Computed from `resolved_at - opened_at`.

**Below charts:** Summary table:

| Metric | Value |
|---|---|
| Total opened (period) | N |
| Total resolved | N |
| P1 opened / resolved | N / N |
| Avg resolution time P1 | X hours |
| ARR protected (resolved with account_at_risk=true) | ₹X.XCr |
| ARR at risk (open) | ₹X.XCr |

---

## Implementation Success Metrics (ISM section)

Restricted to ISM (#94) own data and CSM (#53) full view.

### KPI strip
```
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│ 18              │ │ 43 days         │ │ 74              │ │ 82%             │
│ Active          │ │ Avg Time-to-    │ │ Avg Health at   │ │ On-time ISM     │
│ Implementations │ │ First Exam      │ │ Day-90 Handoff  │ │ Handoff Rate    │
│                 │ │ (target: 30d)   │ │ (target: ≥65)   │ │ (target: 90%)   │
└─────────────────┘ └─────────────────┘ └─────────────────┘ └─────────────────┘
```

- **Avg Time-to-First Exam:** Days from `ism_handoff_date` to first exam created by the institution. Amber if > 30d, red if > 60d.
- **Avg Health at Day-90 Handoff:** Health score at day 90 for institutions that completed ISM tenure this period. Green if ≥ 65 (handed off as ENGAGED or HEALTHY).
- **On-time Handoff Rate:** % of ISM tenures where health ≥ 65 at day 90 before handoff to AM.

### Implementation cohort table
Shows institutions currently in ISM period (within first 90 days):

| Institution | Type | Day | Health | First Exam | Playbook | Touchpoints | ISM |
|---|---|---|---|---|---|---|---|
| Victory School | SCHOOL | Day 34 | 67 (ENGAGED) | ✓ Day 12 | 4/8 tasks | 7 | Priya K. |
| Sunrise College | COLLEGE | Day 18 | 52 (AT_RISK) | ✗ Pending | 2/10 tasks | 3 | Priya K. |

"Day" = days since `ism_handoff_date`. "First Exam" = whether any exam has been created + day it happened. Health colour-banded.

Row with AT_RISK and Day > 45: highlighted red-50 — ISM needs to escalate or notify CSM.

---

## Export PDF

`?export=pdf` — generates a formatted PDF report for the selected period and segment.

**PDF sections:**
1. Cover: "EduForge CS Report — [Period] — [Segment]" + generated date
2. Executive Summary: Retention KPI strip + GRR/NRR trend chart
3. Portfolio Health: Health distribution + cohort analysis table
4. Churn Analysis: By reason + by segment + churned institution table
5. Team Performance: CSM performance table
6. Voice of Customer: NPS KPI strip + NPS trend chart

**Generated by:** Celery task (async). Notification sent with download link on completion. Download link valid 48h.

**Available to:** CSM (#53) and CS Analyst (#93).

---

## Empty States

| Section | Condition | Message |
|---|---|---|
| GRR/NRR trend | Not enough closed renewals | "Not enough renewal data for the selected period. Trend appears after at least 2 quarters of data." |
| Churn analysis | No churns in period | "No churned institutions in this period. " |
| Cohort analysis | < 3 cohorts | "Not enough cohort data. Cohort analysis requires at least 3 quarters of institution join history." |
| CSM performance | No CSMs in system | "No CSM assignments found. Assign CSMs to institutions in J-02 to track performance." |
| Playbook effectiveness | < 5 instances | "Not enough playbook data. Appears after 5 or more completed instances per template." |
| Implementation success | No active implementations | "No active implementations in the selected period." |

---

## Toast Messages

| Action | Toast |
|---|---|
| PDF export queued | "Report is generating. You'll be notified when it's ready for download." (blue) |
| CSV export downloaded | "CSV downloaded." (green) |
| Cache bypassed | "Cache bypassed — showing live data." (blue) |
| Filter applied with no data | "No data for the selected filters." (amber) |

---

## Role-Based UI Visibility Summary

| Section | 53 CSM | 54 AM | 55 Escalation | 56 Renewal | 93 Analyst | 94 ISM |
|---|---|---|---|---|---|---|
| Retention KPI strip | Full | Own portfolio metrics | Escalation section only | Renewal section only | Full | Implementation section only |
| GRR/NRR trend | Yes | No | No | Renewal chart only | Yes | No |
| Health distribution | Yes | Own portfolio | No | No | Yes | Own implementations |
| Churn analysis | Full | No | No | No | Full | No |
| Cohort analysis | Yes | No | No | No | Yes | No |
| CSM performance table | All CSMs | Own row | No | No | All CSMs | Own row |
| Playbook effectiveness | Yes | No | No | No | Yes | Own templates |
| Escalation metrics | Yes | No | Full | No | Yes | No |
| Implementation success | Full | No | No | No | Full | Own only |
| Export PDF | Yes | No | No | No | Yes | No |
| Export CSV | Yes | No | No | No | Yes | No |
| Period selector | All | Own quarter | All | All | All | All |
| Segment filter | Yes | Own type | Yes | Yes | Yes | Own type |
