# Component: Charts & Graphs

> This file defines every chart and data visualization type used across the EduForge admin
> portal. Charts are built on a single charting library (Recharts or Victory — team decision)
> and wrapped in EduForge-specific components that apply the design tokens, handle loading
> states, support real-time WebSocket data, and expose consistent export controls.
> No page spec re-documents chart internals — they reference this file instead.

---

## Design Principles for Charts

> Charts in the admin portal serve one purpose: helping executives make decisions faster.
> They are never decorative. Every chart must answer a specific question for a specific role.
> If removing a chart would not change any decision, it should not exist.

| Principle | What it means in practice |
|---|---|
| Data density | Show as much meaningful data as fits without crowding |
| Context always | Every metric needs a comparator: vs target, vs last period, vs threshold |
| Actionable | Every chart has a related action (export, drill down, or filter change) |
| Role-scoped | Chart data is filtered by the logged-in user's access level and scope |
| Real-time capable | Any chart can accept WebSocket data stream for live updates |
| Accessible | Color is never the only signal — patterns, labels, and tooltips reinforce |
| Theme-aware | All charts use CSS tokens — they switch between dark/light automatically |

---

## Chart Color Palette

> Charts use a sequential, diverging, or categorical palette depending on the data type.
> All palettes are tested for color-blind accessibility (WCAG AA contrast on both themes).

### Categorical Palette (for multiple series, segments, divisions)

| Index | Dark Theme | Light Theme | Use |
|---|---|---|---|
| 1 | `#6366F1` Indigo | `#4F46E5` Indigo | Primary series, first category |
| 2 | `#10B981` Emerald | `#059669` Emerald | Second series, success metric |
| 3 | `#F59E0B` Amber | `#D97706` Amber | Third series, warning metric |
| 4 | `#3B82F6` Blue | `#2563EB` Blue | Fourth series, info metric |
| 5 | `#EC4899` Pink | `#DB2777` Pink | Fifth series |
| 6 | `#8B5CF6` Violet | `#7C3AED` Violet | Sixth series |
| 7 | `#14B8A6` Teal | `#0D9488` Teal | Seventh series |
| 8 | `#F97316` Orange | `#EA580C` Orange | Eighth series |

### Status Palette (for health/status charts)

| Status | Color | Use |
|---|---|---|
| Good / Healthy / Pass | `--status-success` | Passing thresholds, healthy metrics |
| Warning / At Risk | `--status-warning` | Near-threshold metrics |
| Critical / Fail | `--status-error` | Breached thresholds, failing checks |
| Neutral / Inactive | `--status-neutral` | Dormant, no data |

### Sequential Palette (for heatmaps, choropleth maps)

> Low → High intensity scale using the portal's primary color.

| Step | Dark Theme | Light Theme |
|---|---|---|
| 0 (empty/zero) | `#1C2A42` | `#F1F5F9` |
| 1 (low) | `rgba(99,102,241,0.15)` | `rgba(99,102,241,0.10)` |
| 2 | `rgba(99,102,241,0.30)` | `rgba(99,102,241,0.25)` |
| 3 | `rgba(99,102,241,0.50)` | `rgba(99,102,241,0.40)` |
| 4 | `rgba(99,102,241,0.70)` | `rgba(99,102,241,0.60)` |
| 5 (high) | `#6366F1` | `#4F46E5` |

---

## Chart Wrapper — Standard Shell

> Every chart is wrapped in a standard container that provides the title, subtitle,
> time range selector, export button, and loading/error states. Charts never appear
> as naked visuals — they always have context around them.

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  CHART HEADER                                                                 │
│  ┌──────────────────────────────────────────┐  ┌──────────────────────────┐  │
│  │ Chart Title (16px/600)                   │  │ [7d ▼] [Export ↓]        │  │
│  │ Subtitle / data source note (12px/muted) │  │ [Expand ⤢]               │  │
│  └──────────────────────────────────────────┘  └──────────────────────────┘  │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  CHART AREA                                                                   │
│  (variable height — defined per usage. Min 160px, default 240px, max 480px)  │
│                                                                               │
├──────────────────────────────────────────────────────────────────────────────┤
│  CHART FOOTER                                                                 │
│  Legend (if multiple series)  ·  Last updated: 8s ago  ·  [● LIVE]           │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Time Range Selector

> Appears in the top-right of every chart header. Changing the range triggers a new API call.
> The active range is highlighted. Charts remember the last-used range per user session.

```
[1h] [24h] [7d ▼] [30d] [90d] [12mo] [Custom]
       ↑ active: filled primary background
```

| Range | API param | Use case |
|---|---|---|
| `1h` | `period=1h` | Live exam monitoring, real-time ops |
| `24h` | `period=24h` | Daily operational view |
| `7d` | `period=7d` | Weekly health checks |
| `30d` | `period=30d` | Monthly business review |
| `90d` | `period=90d` | Quarterly analysis |
| `12mo` | `period=12mo` | Annual trends, board reports |
| `custom` | `from=&to=` | Date range picker overlay |

### Export Options

```
[Export ↓]  →  dropdown:
  ┌──────────────────────┐
  │ [🖼 Export as PNG]   │
  │ [📊 Export as CSV]   │
  │ [📋 Copy to Clipboard│
  └──────────────────────┘
```

---

## Chart Type 1 — Line Chart

> **Purpose:** Show trends over time for a single or multiple continuous metrics.
> Used for: API latency, student growth, revenue trend, error rates, NPS scores.
> The most-used chart type in the admin portal — almost every trend is a line chart.

### Anatomy

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  API Latency (p50 / p95 / p99)                          [7d ▼] [Export ↓]   │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  300ms ── ─ ── ─ ── ─ ── ─ ── ─ ── ─ ── threshold ── ─ ── ─ ──             │
│                                                          ╭─────────╮         │
│  200ms                      ╭─────────────────────────╯ p99       │         │
│                    ╭────────╯                                      │         │
│  100ms ─────────────────────────────────────────── p95 ────────── │         │
│  50ms  ─────────────────────────────────────────── p50 ────────── │         │
│       Mon     Tue     Wed     Thu     Fri     Sat     Sun          │         │
│                                                    [tooltip popup] │         │
└──────────────────────────────────────────────────────────────────────────────┘
│  ── p50 (94ms avg)   ── p95 (187ms avg)   ── p99 (342ms avg)   [SLA: 300ms] │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Specifications

| Property | Value |
|---|---|
| Line style | Smooth curve (monotone interpolation) |
| Line weight | 2px primary series, 1.5px secondary |
| Data points | Shown as 4px dots on hover, always shown on last data point |
| Threshold line | Dashed `--status-warning` or `--status-error` horizontal line |
| Area fill | Optional — fill below line at 15% opacity of line color |
| Grid lines | Horizontal only, `--border-subtle`, 1px |
| Axis labels | 11px, `--text-muted`, every N-th tick to avoid crowding |
| Tooltip | Vertical crosshair + floating card showing all series values at that point |
| Zoom | Click-drag to zoom in on a time range. Double-click to reset |
| Pan | Hold Shift + drag to pan |
| Legend | Below chart — click to toggle series on/off |

### Tooltip Design

```
┌────────────────────────────────┐
│  Thu, Mar 14  14:23 IST        │
│  ─────────────────────────     │
│  ─── p50    94ms               │
│  ─── p95    187ms              │
│  ─── p99    342ms  ⚠ near SLA │
│  ─────────────────────────     │
│  SLA threshold: 300ms          │
└────────────────────────────────┘
```

---

## Chart Type 2 — Area Chart

> **Purpose:** Show volume over time where the filled area communicates quantity/magnitude.
> Used for: Lambda concurrency, submission rates, API throughput, active students over time.
> The visual weight of the filled area makes large numbers feel viscerally large.

### Anatomy

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  Lambda Warm Instances (24h)                            [24h ▼] [Export ↓]  │
├──────────────────────────────────────────────────────────────────────────────┤
│  1200 ── Max capacity ─────────────────────────────────────────────────────  │
│                                                                               │
│   847 ─────────────────────────────────────────────────────── current        │
│                          ████████████████████████████████                    │
│         ████████████████████████████████████████████████████                 │
│  ─────────████████████████████████████████████████████████████               │
│       00:00  04:00  08:00  12:00  14:23  16:00  20:00  24:00                 │
│                             ↑ now                                            │
└──────────────────────────────────────────────────────────────────────────────┘
│  ■ Warm instances   Max: 1,200   Current: 847   Exam-day threshold: 1,100    │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Specifications

| Property | Value |
|---|---|
| Fill | Gradient fill: solid at bottom → 30% opacity at top (creates depth) |
| Fill colors | Single series: `--primary` at 20%. Multi-series: categorical palette at 15% each |
| Stacked option | `stacked=true` — series stack on top of each other (for composition) |
| Reference line | Horizontal dashed lines for thresholds/targets |
| Now indicator | Vertical dashed line at current time for 24h/1h charts |
| Smooth | Uses monotone interpolation to avoid spiky visual artifacts |

---

## Chart Type 3 — Bar Chart

> **Purpose:** Compare discrete categories or show distribution across buckets.
> Used for: Revenue by segment, incidents by priority, institution count by type,
> monthly exam volume, support ticket distribution by division.

### Vertical Bar (Column Chart)

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  Revenue by Segment (MTD)                               [MTD ▼] [Export ↓]  │
├──────────────────────────────────────────────────────────────────────────────┤
│  ₹1.2Cr │                                                                    │
│         │          ████                                                      │
│  ₹0.8Cr │          ████                                                      │
│         │   ████   ████   ████                                               │
│  ₹0.4Cr │   ████   ████   ████   ████                                        │
│         │   ████   ████   ████   ████   ████                                  │
│  0      └────────────────────────────────────                                │
│            Schools  Colleges Coaching Online  Groups                         │
└──────────────────────────────────────────────────────────────────────────────┘
│  ₹2.47 Cr total MTD  ·  ↑ 17.6% vs target  ·  ₹2.1 Cr target line         │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Horizontal Bar

> Used when: category labels are long, or when ranking is the primary message.

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  Division Workload (Open Tasks)                                               │
│  ─────────────────────────────────────────────────────────────────────────── │
│  Customer Support   ██████████████████████████████████  34                   │
│  Exam Operations    ████████████████████████  22                             │
│  Content & Academics████████████████  16                                     │
│  BGV Division       ████████  8                                              │
│  Engineering        ████  4                                                  │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Grouped Bar

> Used when comparing multiple series across the same categories (e.g., this month vs last month).

### Stacked Bar

> Used when showing composition within each category total (e.g., subscription tier mix per segment).

### Bar Chart Specifications

| Property | Value |
|---|---|
| Bar gap | 20% of bar width between grouped bars |
| Corner radius | `--radius-xs` (4px) on top corners only |
| Value labels | Optional — shown above bars for datasets with <8 categories |
| Grid lines | Horizontal only |
| Target line | Dashed horizontal line with label "Target: ₹X" |
| Hover | Opacity 80% on non-hovered bars. Tooltip on hovered bar. |

---

## Chart Type 4 — Pie / Donut Chart

> **Purpose:** Show composition/proportion of a whole.
> Used for: Revenue by segment, incidents by category, institutions by type, compliance coverage.
> Always use donut (center hole) over solid pie — the center displays the total or key metric.

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  Revenue Breakdown (MTD)                                [MTD ▼] [Export ↓]  │
├──────────────────────────────────────────────────────────────────────────────┤
│                          ╭──────────────────────╮                            │
│  ■ Schools    ₹1.18Cr   │     ╭────────────╮    │   ■ Schools      47.8%   │
│    47.8%      ──────────│──  │  ₹2.47 Cr  │    │   ■ Colleges     26.7%   │
│                         │    │   Total     │    │   ■ Coaching     18.2%   │
│  ■ Colleges   ₹0.66Cr  │    │    MTD      │    │   ■ Online        4.9%   │
│  ■ Coaching   ₹0.45Cr  │     ╰────────────╯    │   ■ Groups        2.4%   │
│  ■ Online     ₹0.12Cr   ╰──────────────────────╯                            │
│  ■ Groups     ₹0.06Cr                                                        │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Specifications

| Property | Value |
|---|---|
| Inner radius | 60% of outer (donut style) |
| Center text | Primary metric (total, or selected segment detail) |
| Hover | Segment explodes outward 8px on hover. Tooltip shows value + percentage. |
| Legend | Right side or below. Click legend item to isolate/hide segment. |
| Max segments | 8. Beyond 8 → group remainder into "Other" |
| Small pie warning | If any segment < 2%, label shown outside with leader line |

---

## Chart Type 5 — Sparkline

> **Purpose:** Compact inline trend indicator embedded within table cells or stat cards.
> Conveys trend direction and volatility at a glance without consuming page space.
> No axes, no labels, no tooltips — pure visual trend signal.

```
Table row example:
┌──────────────────────────────────────────────────────────────────┐
│  Platform Uptime (30d) │  99.94%  │  ╭─────────────────╮        │
│                        │   ↑0.02% │  ╰─╯               ╰────    │
│                        │          │  [sparkline, 80×24px]       │
└──────────────────────────────────────────────────────────────────┘
```

### Specifications

| Property | Value |
|---|---|
| Dimensions | 80×24px (default). 120×32px (wide variant in stat cards) |
| Line weight | 1.5px |
| Color | `--status-success` if trending up, `--status-error` if trending down, `--primary` if neutral |
| Fill | Area fill at 20% opacity below the line |
| Data points | Last 7d or last 30d of daily values |
| Hover | None — sparklines are display-only. For interaction, click navigates to full chart. |

---

## Chart Type 6 — Heatmap / Calendar Heatmap

> **Purpose:** Show intensity/density of a metric across two dimensions (typically time × category
> or date × value). Used for: exam schedule density, division workload heatmap, weekly error
> pattern, student activity calendar.

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  Division Workload Heatmap (last 30 days)                [30d ▼] [Export ↓] │
├──────────────────────────────────────────────────────────────────────────────┤
│              Mar 1  Mar 8  Mar 14  Mar 21  Mar 28                            │
│  Support     ██▓▓░░░██▓░░░░░░░░██▓░░░░░██▓▓░░░                             │
│  Exam Ops    ░░░░████████░░░░░░████████░░░░░░░                              │
│  BGV         ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                           │
│  Engineering ░░████░░░░░░░░████░░░░░░░░████░░░                              │
│  Finance     ░░░░░░░░░░░░░░░░░░░░░░░░░░░░████                               │
│  ─────────────────────────────────────────────────────────────────────────── │
│  ░ Low (0–3)  ▓ Medium (4–8)  █ High (9–15)  ██ Critical (>15)             │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## Chart Type 7 — Funnel Chart

> **Purpose:** Show conversion or drop-off through a sequential multi-stage process.
> Used for: Institution onboarding funnel (Lead → Demo → Signed → Onboarding → Active),
> student registration funnel, content approval pipeline.

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  Institution Onboarding Funnel (Q1 2026)                         [Export ↓] │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  ████████████████████████████████████████  Lead Identified     247  100%    │
│   ████████████████████████████████████    Demo Completed       189   77%    │
│      ████████████████████████████         Agreement Signed      94   38%    │
│         ████████████████████              Onboarding Started    62   25%    │
│               ████████████               Fully Active           47   19%    │
│                                                                               │
└──────────────────────────────────────────────────────────────────────────────┘
│  Biggest drop: Demo → Signed (39% conversion). [View details]                │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## Chart Type 8 — Gauge / Radial Chart

> **Purpose:** Show a single metric against a scale with clear zones (good/warning/critical).
> Used for: Security score, platform health score, SLA compliance percentage, storage usage.

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  Platform Security Score                                                      │
│                                                                               │
│                   🟢  87 / 100                                               │
│               ╭─────────────╮                                                │
│           ╭───┤    87/100   ├───╮                                            │
│      ╭────┤   │  ↑+3 this  │   ├────╮                                       │
│      │    │   │    week     │   │    │                                       │
│      │ 🔴 │   ╰─────────────╯   │ 🟢 │                                       │
│      │ 0  ╰───────────────────╯100  │                                        │
│      ╰──────── 50 (threshold) ──────╯                                        │
│                                                                               │
│  🔴 Critical  🟡 Warning  🟢 Good                                            │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## Chart Type 9 — Cohort / Retention Table

> **Purpose:** Show how different cohorts (groups starting in the same month) retain over time.
> Used for: Institution retention by acquisition month, student engagement cohorts.

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  Institution Retention Cohorts (2025)                            [Export ↓]  │
├───────────────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┬────────────┤
│  Cohort       │  Mo0 │  Mo1 │  Mo2 │  Mo3 │  Mo4 │  Mo5 │  Mo6 │ Current   │
├───────────────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┼────────────┤
│  Jan'25 (47)  │ 100% │  96% │  94% │  91% │  89% │  87% │  85% │  83%      │
│  Feb'25 (38)  │ 100% │  97% │  95% │  92% │  90% │  88% │  —   │  88%      │
│  Mar'25 (62)  │ 100% │  98% │  96% │  93% │  91% │  —   │  —   │  91%      │
│  Apr'25 (29)  │ 100% │  97% │  94% │  92% │  —   │  —   │  —   │  92%      │
└───────────────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┴────────────┘
```

> Cells are color-coded: ≥95% `--status-success`, 85–95% `--status-warning`, <85% `--status-error`.

---

## Real-Time Chart Behavior (WebSocket)

> Some charts receive live data via WebSocket and update without any user action.
> These charts have special behavior to prevent disorienting visual jumps.

| Behavior | Implementation |
|---|---|
| New data point added | Chart smoothly scrolls left as newest point is appended to the right |
| Y-axis rescale | When new data exceeds current Y range, axis smoothly rescales over 300ms |
| Live indicator | `● LIVE` badge shown in chart header with pulsing dot animation |
| Reconnect | On WebSocket disconnect: chart shows "⚠ Live data paused" overlay, data freezes |
| Buffer | Chart buffers 5 data points before rendering to smooth out bursts |
| Historical join | On reconnect: seamless join between frozen data and new live stream |

### Live Chart Header

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  Lambda Concurrency  ● LIVE  (last update: 1s ago)       [1h ▼] [Pause ⏸]  │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## Chart Loading, Empty, and Error States

### Loading State

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  API Latency (p50 / p95 / p99)                          [7d ▼] [Export ↓]   │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  ← shimmer skeleton  │
│  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░                                     │
│  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░                                                │
│                                                                               │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Empty State (no data for selected range)

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  API Latency (p50 / p95 / p99)                          [7d ▼] [Export ↓]   │
│  ─────────────────────────────────────────────────────────────────────────── │
│                                                                               │
│                    [icon: empty chart]                                        │
│                    No data for this period                                    │
│                    Try selecting a different time range                       │
│                    [Change range]                                             │
│                                                                               │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Error State

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  API Latency (p50 / p95 / p99)                                                │
│  ─────────────────────────────────────────────────────────────────────────── │
│                    ⚠  Failed to load chart data                               │
│                    [Retry]                                                    │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## Chart Grid Layouts

> Charts are grouped in responsive grids. The grid collapses on smaller screens.

### 2-Column Grid (default analytics layout)

```
┌──────────────────────────────┬──────────────────────────────┐
│  Chart A                     │  Chart B                     │
│  (240px height)              │  (240px height)              │
└──────────────────────────────┴──────────────────────────────┘
┌──────────────────────────────┬──────────────────────────────┐
│  Chart C                     │  Chart D                     │
└──────────────────────────────┴──────────────────────────────┘
```

On tablet (768–1023px): 2 columns → 1 column (full width)
On mobile (<768px): 1 column only

### 3-Column Grid (dashboard overview)

```
┌────────────────┬────────────────┬────────────────┐
│  Chart A       │  Chart B       │  Chart C       │
│  (160px)       │  (160px)       │  (160px)       │
└────────────────┴────────────────┴────────────────┘
```

On tablet: 3 → 2 columns
On mobile: 3 → 1 column

### Full-Width Chart (primary focus)

```
┌──────────────────────────────────────────────────────────────┐
│  Primary Chart (e.g., MAU trend — most important metric)     │
│  (320px height)                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## Usage in Page Specs

```markdown
### Revenue Trend Chart
→ Component: [Line Chart](../../components/09-charts-graphs.md#chart-type-1--line-chart)
  Title: "Monthly Recurring Revenue"
  Series:
    - MRR (primary, --primary color)
    - Target (dashed, --status-warning)
  Time ranges: [30d] [90d] [12mo]  Default: 12mo
  Y-axis: ₹ (Indian Rupee, formatted as ₹X.XXCr)
  Threshold: Target line at current month target value
  Data source: GET /api/v1/finance/mrr?period=12mo

### Submission Rate (live)
→ Component: [Area Chart](../../components/09-charts-graphs.md#chart-type-2--area-chart)
  Title: "Submission Rate (per minute)"
  Mode: Real-time WebSocket
  Source: WS /ws/exam/{id}/submissions
  Time range: Fixed to exam duration (no selector)
  Reference lines: Peak capacity (1,200/min)
  Annotations: Error spikes (red vertical lines)
```
