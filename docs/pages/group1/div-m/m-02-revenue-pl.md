# M-02 — Revenue & P&L

**Route:** `GET /finance/revenue/`
**Method:** Django `TemplateView` + HTMX part-loads
**Primary roles:** Finance Manager (#69), Finance Analyst (#101)
**Also sees:** Pricing Admin (#74) — plan revenue breakdown only (read-only, no P&L rows)

---

## Purpose

Investor-grade revenue analytics workspace. Finance Manager uses this to prepare monthly P&L reports, board decks, and investor updates. Finance Analyst uses it to model ARR movements (new/expansion/contraction/churn), compute Net Revenue Retention (NRR) and Gross Revenue Retention (GRR), and investigate variance between forecast and actuals. Pricing Admin gets a read-only view of plan-tier revenue breakdown to understand which plans are driving growth. No operational actions from this page — it is purely analytical and export-driven.

---

## Data Sources

| Section | Source | Cache TTL |
|---|---|---|
| Revenue KPI strip | `analytics_revenue` latest month (segment='all', plan_tier='all') | 15 min |
| ARR waterfall chart | `analytics_revenue` current month: new_arr + expansion - contraction - churn | 15 min |
| MRR/ARR trend | `analytics_revenue` last 24 months, segment='all', plan_tier='all' | 60 min |
| NRR/GRR chart | Computed from `analytics_revenue` waterfall fields, 12 months | 60 min |
| Revenue by plan tier | `analytics_revenue` latest month grouped by plan_tier | 15 min |
| Revenue by segment | `analytics_revenue` last 12 months grouped by segment | 60 min |
| Cohort revenue table | `analytics_revenue` grouped by institution first-subscription year × current ARR contribution | 60 min |
| P&L summary table | `analytics_revenue` invoiced/collected/overdue/written-off per period | 15 min |
| Forecast vs Actuals | `finance_invoice` actuals vs forecast model stored in `analytics_revenue.forecast_arr_paise` | 15 min |

All caches keyed on `(user_id, period_from, period_to, segment, plan_tier)`. `?nocache=true` for FM (#69) and Analyst (#101).

---

## URL Parameters

| Param | Values | Default | Effect |
|---|---|---|---|
| `?period` | `last_month`, `this_quarter`, `last_quarter`, `last_6m`, `last_12m`, `last_24m`, `ytd`, `custom` | `last_12m` | Reporting window for all charts |
| `?from` | `YYYY-MM` | — | Custom period start (month precision) |
| `?to` | `YYYY-MM` | — | Custom period end (month precision) |
| `?segment` | `all`, `school`, `college`, `coaching`, `group` | `all` | Filter all charts to one segment |
| `?tier` | `all`, `STARTER`, `STANDARD`, `PROFESSIONAL`, `ENTERPRISE` | `all` | Filter all charts to one plan tier |
| `?export` | `pdf`, `csv` | — | Export current view (FM + Analyst only) |
| `?nocache` | `true` | — | Bypass Memcached (FM + Analyst only) |

---

## HTMX Part-Load Routes

| Part | Route | Trigger | Target ID |
|---|---|---|---|
| Revenue KPI strip | `?part=rev_kpi` | Page load + filter change | `#rev-kpi` |
| ARR waterfall | `?part=waterfall` | Page load + period/filter change | `#rev-waterfall` |
| MRR/ARR trend | `?part=mrr_arr_trend` | Page load + period change | `#rev-trend` |
| NRR/GRR chart | `?part=retention_chart` | Page load + period change | `#rev-retention` |
| Plan tier breakdown | `?part=plan_breakdown` | Page load + filter change | `#rev-plan` |
| Revenue by segment | `?part=seg_breakdown` | Page load + filter change | `#rev-segment` |
| Cohort table | `?part=cohort` | Page load | `#rev-cohort` |
| P&L summary | `?part=pl_summary` | Page load + period change | `#rev-pl` |
| Forecast vs Actuals | `?part=forecast` | Page load + period change | `#rev-forecast` |

---

## Page Layout

```
┌─────────────────────────────────────────────────────────────────────────┐
│  Revenue & P&L   Period: [Last 12 Months ▼]  Segment: [All ▼]          │
│  Tier: [All ▼]    [Export PDF]  [Export CSV]                            │
├─────────────────────────────────────────────────────────────────────────┤
│  REVENUE KPI STRIP (6 tiles)                                            │
├──────────────────────────────────┬──────────────────────────────────────┤
│  ARR WATERFALL (current month)   │  NRR / GRR TREND (12 months)        │
├──────────────────────────────────┴──────────────────────────────────────┤
│  MRR / ARR TREND (dual-axis line, 24 months)                            │
├──────────────────────────────────┬──────────────────────────────────────┤
│  REVENUE BY PLAN TIER (pie+table)│  REVENUE BY SEGMENT (stacked area)  │
├──────────────────────────────────┴──────────────────────────────────────┤
│  P&L SUMMARY TABLE                                                      │
├─────────────────────────────────────────────────────────────────────────┤
│  FORECAST VS ACTUALS (line chart)  │  COHORT REVENUE TABLE              │
└────────────────────────────────────┴──────────────────────────────────┘
```

---

## Components

### Revenue KPI Strip (6 tiles)

```
┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│ ₹4.2Cr   │ │ ₹35.1L   │ │ +₹42L    │ │ 108%     │ │ 94%      │ │ 2.3 yrs  │
│ ARR      │ │ MRR      │ │ Net New  │ │ NRR      │ │ GRR      │ │ Avg Sub  │
│          │ │          │ │ ARR (MTD)│ │ (LTM)    │ │ (LTM)    │ │ Duration │
│ ↑+₹18L   │ │ ↑+₹1.2L  │ │ +32 insts│ │ ↑+3 pts  │ │ ↓-1 pt   │ │ ↑+0.2    │
└──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘
```

**Tile 1 — ARR:** Total ARR from `analytics_revenue.arr_paise`. Delta = `new_arr + expansion - contraction - churn` for the period. See M-01 for colour coding.

**Tile 2 — MRR:** `analytics_revenue.mrr_paise` latest month. Sub-label "×12 = ₹X.XCr annual run rate".

**Tile 3 — Net New ARR (MTD):** `new_arr_paise + expansion_arr_paise - contraction_arr_paise - churned_arr_paise` for the current month. Shows count of net-new institutions. Green if positive. This is the most important growth signal.

**Tile 4 — NRR (Last 12 Months):** Net Revenue Retention: `(beginning_ARR + expansion - contraction - churn) / beginning_ARR × 100`. LTM (last twelve months) rolling. Green if ≥ 100%, amber if 80–99%, red if < 80%. NRR > 100% means expansion revenue exceeds churn — the holy grail for SaaS.

**Tile 5 — GRR (Last 12 Months):** Gross Revenue Retention: `(beginning_ARR - churn) / beginning_ARR × 100`. Does not count expansion. Target ≥ 90%. Amber if 80–89%, red if < 80%.

**Tile 6 — Avg Subscription Duration:** Average `(end_date - start_date)` across all active `finance_subscription` records, in years. Delta vs previous quarter. Rising duration = healthy renewal behaviour.

---

### ARR Waterfall Chart

Horizontal waterfall chart (Chart.js custom plugin) showing ARR movement for the selected period.

```
Beginning ARR         ₹4.00Cr  ████████████████████████████████████████
+ New ARR             +₹24L    ████
+ Expansion ARR       +₹18L    ███
− Contraction ARR     −₹6L    ██ (red)
− Churned ARR         −₹12L   ████ (dark red)
─────────────────────────────────────────────────────
Ending ARR            ₹4.24Cr  ████████████████████████████████████████
```

- Green bars: Beginning ARR, New ARR, Expansion ARR
- Red bars: Contraction ARR, Churned ARR (direction shown as negative)
- Grey connector lines between bars show the running total at each step
- Ending ARR bar colour: green if > Beginning ARR, red if <
- Hover tooltip: exact paise amount + count of institutions in that category
- Clicking "New ARR" bar: filters M-04 to `?status=active&created_in=<period>` — shows which new subscriptions drove growth
- Clicking "Churned ARR" bar: cross-links to `csm_renewal` WHERE stage='CHURNED' for the period

**Period note:** Waterfall shows the most recently completed full month within the selected period. If period is 'last_12m', waterfall shows the last calendar month; a "Previous Month" / "Next Month" navigation appears below the chart.

---

### MRR / ARR Trend (Dual-Axis)

Line chart — 24 months of MRR (left Y-axis, ₹L) and ARR (right Y-axis, ₹Cr) overlaid.

- **Solid blue line:** ARR (right Y-axis)
- **Dashed blue line:** MRR × 12 run-rate (left Y-axis, scaled to match)
- **Green shaded area:** between MRR run-rate and ARR (shows how ARR leads/lags MRR changes)
- **Vertical dashed markers:** phase boundaries — "Phase 2 start" at ₹50K students milestone
- **Hover:** ARR · MRR · MoM growth % · QoQ growth %
- **Finance Analyst toggle:** "Show components" — adds stacked area layers for new/expansion/contraction/churn below the main ARR line (useful for understanding composition of growth)

---

### NRR / GRR Trend Chart

Line chart — 12 months of monthly NRR% and GRR%.

- **Solid green line:** NRR%
- **Dashed green line:** GRR%
- **Reference lines:** horizontal at 100% (NRR target) and 90% (GRR target)
- **Hover:** NRR% · GRR% · expansion ARR that month · churn ARR that month
- **Fill:** soft green fill above 100% NRR line (expansion territory)

**Interpretation guide (tooltip on chart title [?]):** "NRR > 100% means existing customers are growing their spend faster than churn. GRR < NRR gap = expansion from existing customers."

---

### Revenue by Plan Tier

**Left: Donut chart** — ARR contribution by plan tier for the latest month.

- Colours: Starter=grey-400, Standard=blue-400, Professional=indigo-500, Enterprise=violet-600
- Centre label: total ARR
- Legend with ₹Cr and % per tier

**Right: Summary table**

| Plan Tier | Institutions | ARR (₹) | % of Total | MoM Change |
|---|---|---|---|---|
| Enterprise | 105 | ₹23.8Cr | 56.7% | ↑+₹1.2Cr |
| Professional | 743 | ₹14.9Cr | 35.5% | ↑+₹0.6Cr |
| Standard | 890 | ₹5.3Cr | 12.6% | ↓-₹0.2Cr |
| Starter | 312 | ₹0.78Cr | 1.9% | ↑+₹0.1Cr |

Clicking any tier row filters the entire dashboard to `?tier=<tier>`.

---

### Revenue by Segment (Stacked Area)

Stacked area chart — 12 months showing ARR contribution per institution segment.

- Segments: School (blue) · College (violet) · Coaching (orange) · Group (teal)
- Stacked so total height = total ARR
- Hover: exact ARR per segment for that month + % of total
- Finance Analyst can overlay a "forecast" line (from forecast model) by clicking a toggle

---

### P&L Summary Table

Tabular month-by-month P&L for the selected period. Server-side paginated (12 months per page).

| Column | Description |
|---|---|
| Month | e.g., "Feb 2026" |
| Invoiced (₹) | `analytics_revenue.invoiced_paise` |
| Collected (₹) | `analytics_revenue.collected_paise` |
| Outstanding (₹) | invoiced - collected |
| Written Off (₹) | Sum of `finance_invoice.total_paise` WHERE status='WRITTEN_OFF' in month |
| Net Revenue (₹) | collected - written_off |
| GST Liability (₹) | Sum of (cgst + sgst + igst) for paid invoices; source: `finance_invoice` |
| Net of GST (₹) | Net Revenue - GST Liability |
| MoM Change | % change vs previous month's Net Revenue; green/red |

- Sortable by all numeric columns
- Row click: expands to show segment breakdown inline (HTMX accordion)
- [Export this table] button: CSV download of the full P&L rows in the selected period
- **Visible to:** FM (#69) and Analyst (#101) only. Pricing Admin (#74) sees only the Invoiced column (hidden: Written Off, Net Revenue, GST, Net of GST).

---

### Forecast vs Actuals Chart

Line chart — actual ARR vs forecast for the next 6 months (backward 6 months actual + forward 6 months forecast).

- **Solid blue line:** actuals (historical months)
- **Dashed blue line:** forecast (from `analytics_revenue.forecast_arr_paise`)
- **Shaded confidence band** around forecast line: ±10% band in blue-100
- **Vertical "today" line:** separates historical from projected
- **Hover on forecast:** "Forecast: ₹X.XCr | Low: ₹X.XCr | High: ₹X.XCr"
- **"Update Forecast" button** (FM #69 only): opens Forecast Update drawer to manually adjust monthly forecast values for the next 6 months (stored in `analytics_revenue.forecast_arr_paise` via a POST to `/finance/revenue/forecast/`)

---

## Forecast Update Drawer (560px — FM #69 only)

```
  Update ARR Forecast
  ──────────────────────────────────────────────────────────
  Set monthly ARR targets for the next 6 months.
  ──────────────────────────────────────────────────────────
  Apr 2026  Forecast ARR (₹Cr) [ 4.20 ]  Confidence (%)  [ 80 ]
  May 2026  Forecast ARR (₹Cr) [ 4.40 ]  Confidence (%)  [ 75 ]
  Jun 2026  Forecast ARR (₹Cr) [ 4.60 ]  Confidence (%)  [ 70 ]
  Jul 2026  Forecast ARR (₹Cr) [ 4.80 ]  Confidence (%)  [ 65 ]
  Aug 2026  Forecast ARR (₹Cr) [ 5.00 ]  Confidence (%)  [ 60 ]
  Sep 2026  Forecast ARR (₹Cr) [ 5.20 ]  Confidence (%)  [ 55 ]
  ──────────────────────────────────────────────────────────
  Notes  [Optional context for this forecast revision...]
  ──────────────────────────────────────────────────────────
  [Cancel]                              [Save Forecast]
```

| Field | Validation |
|---|---|
| Forecast ARR (₹Cr) | Required; ≥ 0; stored as paise (× 10,000,000) |
| Confidence (%) | Integer; 10–100; default 80; displayed as ±band on chart |
| Notes | Optional; max 500 chars; HTML-escaped on display |

**On submit:** POST `/finance/revenue/forecast/` with array of `{period_year, period_month, forecast_arr_paise, confidence_pct, notes}`. Upserts rows in `analytics_revenue`. Writes `finance_audit_log` entry. Chart auto-refreshes to reflect new values.

Toast: "Forecast updated for 6 months."

---

### Cohort Revenue Table

Matrix showing ARR contribution by institution cohort (year of first subscription) × current month.

| Cohort | Subscriptions | Starting ARR | Month 1 | Month 6 | Month 12 | Month 24 | Current ARR | NRR |
|---|---|---|---|---|---|---|---|---|
| 2023 | 180 | ₹0.54Cr | 100% | 98% | 94% | 102% | ₹0.55Cr | 102% |
| 2024 | 650 | ₹1.95Cr | 100% | 97% | 101% | 108% | ₹2.11Cr | 108% |
| 2025 | 1020 | ₹3.06Cr | 100% | 99% | — | — | ₹3.03Cr | 99% |

- Percentages = ARR as % of starting cohort ARR (retention + expansion)
- Green if ≥ 100%, amber if 90–99%, red if < 90%
- "—" for future months not yet reached
- Clicking a cell: links to M-04 filtered to that cohort × period
- **Visible to:** FM (#69) and Analyst (#101) only.

---

## Export

**[Export PDF]:** WeasyPrint server-side render of the current dashboard view (all visible charts + tables) as a multi-page PDF. Suitable for investor decks. Filename: `eduforge_revenue_report_YYYY-MM.pdf`. Includes EduForge letterhead, period label, and "Confidential" watermark. Available to FM (#69) and Analyst (#101).

**[Export CSV]:** CSV of the P&L Summary Table rows for the selected period. Columns: month, invoiced, collected, outstanding, written_off, net_revenue, gst_liability, net_of_gst. Filename: `eduforge_pl_YYYY-MM_to_YYYY-MM.csv`.

**Async threshold:** PDF generation queued as Celery task if period > 12 months. Toast: "PDF generation queued — you'll receive an email with the download link shortly."

---

## Empty States

| Section | Condition | Message |
|---|---|---|
| ARR Waterfall | No analytics_revenue data for the selected period | "Revenue data for this period is not yet computed. Task M-5 runs nightly." |
| Cohort Table | Fewer than 2 active cohort years | "Not enough cohort history yet — data will populate as the platform matures." |
| Forecast vs Actuals | No forecast values entered | "No forecast data. Use [Update Forecast] to set monthly ARR targets." |

---

## Toast Messages

| Action | Toast | Type |
|---|---|---|
| Period filter changed | "Showing revenue data for [period]." | Blue (info) |
| Segment filter changed | "Filtered to [segment] institutions." | Blue (info) |
| Forecast updated | "Forecast updated for [N] months." | Green (success) |
| PDF export queued | "PDF generation queued — email with download link coming shortly." | Amber (info) |
| CSV export downloaded | "P&L exported to CSV." | Green (success) |
| `?nocache=true` | "Cache bypassed — showing live revenue data." | Blue (info) |

---

## Authorization

**Route guard:** `@division_m_required(allowed_roles=[69, 74, 101])` applied to `RevenuePLView`.

| Scenario | Behaviour |
|---|---|
| Unauthenticated | Redirect to login |
| Role #70, #71, #72, #73, #102 | 403 redirect — they access revenue context only via M-01 strips |
| Pricing Admin (#74) | Full page loads; P&L table shows only Invoiced column; all other columns hidden; no export access |
| Finance Analyst (#101) | Full read + export; no Forecast Update action |
| Finance Manager (#69) | Full read + export + Forecast Update |

---

## Role-Based UI Visibility Summary

| Element | 69 FM | 101 Analyst | 74 Pricing |
|---|---|---|---|
| All 6 KPI tiles | Yes | Yes | Tiles 1+2 only |
| ARR Waterfall | Yes | Yes | No |
| MRR/ARR Trend | Yes | Yes + "show components" toggle | No |
| NRR/GRR Trend | Yes | Yes | No |
| Revenue by Plan Tier | Yes | Yes | Yes (read) |
| Revenue by Segment | Yes | Yes + forecast overlay | No |
| P&L Summary Table | Full | Full | Invoiced col only |
| Forecast vs Actuals | Yes + Update Forecast | Yes (read) | No |
| Cohort Revenue Table | Yes | Yes | No |
| Export PDF | Yes | Yes | No |
| Export CSV | Yes | Yes | No |
| [?nocache=true] | Yes | Yes | No |

---

## Performance Requirements

| Metric | Target | Notes |
|---|---|---|
| Initial page load (SSR) | < 2s P95 | KPI strip + chart placeholders served immediately; charts lazy-loaded |
| KPI tiles | < 600ms P95 (cache hit) | 15-min TTL; `analytics_revenue` pre-aggregated by Task M-5 |
| ARR waterfall chart data | < 800ms P95 (cache hit) | 60-min TTL |
| Cohort revenue table | < 1.5s P95 (cache hit) | 60-min TTL; large JOIN across subscriptions + invoices |
| PDF export (≤ 12 months) | < 5s P95 | WeasyPrint synchronous render |
| PDF export (> 12 months) | Async; email within 2 min | Celery task; immediate amber toast feedback |
| CSV export | < 3s for ≤ 5,000 rows | Streaming response |
| `?nocache=true` full rebuild | < 15s | All charts + tables re-computed from `analytics_revenue` + source tables |

---

## Keyboard Shortcuts

| Key | Action |
|---|---|
| `g` `r` | Go to Revenue & P&L (M-02) |
| `e` | Export CSV (FM / Analyst) |
| `p` | Export PDF (FM / Analyst) |
| `←` / `→` | Navigate chart time period (prev / next month range) |
| `Esc` | Close open drawer or modal |
| `?` | Show keyboard shortcut help overlay |

