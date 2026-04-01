# Component 10 — Stat Cards / KPI Cards

> **Stat Cards** (also called KPI Cards, Metric Cards, or Summary Cards) are the primary visual building blocks for surfacing high-signal numbers across the EduForge Admin Portal. Every executive dashboard, operational command center, financial overview, and operational page opens with a row (or grid) of Stat Cards that give the viewer an immediate quantitative snapshot before they engage with any table or chart. They are intentionally compact, scannable, and information-dense — designed to support a decision-maker who needs to assess platform health in under 5 seconds.
>
> These cards live inside the **App Shell Content Area** and are always the first element below the page header. They support real-time WebSocket updates, trend indicators, status coloring, sparkline mini-charts, drill-down click targets, and loading skeleton states.
>
> All colors in this component use CSS custom property tokens from `00-global-layout.md`. Cards automatically adapt between dark and light themes without any logic changes.

---

## 1. Card Anatomy

> Every Stat Card is composed of a fixed set of structural regions. Each region serves a precise informational role. Understanding the anatomy ensures consistent implementation across all 31 Division A pages and beyond.

```
┌─────────────────────────────────────────────────────────┐
│  [ICON]  CARD LABEL                      [TREND BADGE]  │
│                                                         │
│  PRIMARY VALUE                          [SPARKLINE]     │
│  secondary context line                                 │
│                                                         │
│  [STATUS DOT] Status text        [LINK: View Details →] │
└─────────────────────────────────────────────────────────┘
```

| Region | Purpose | Required |
|---|---|---|
| **Card Label** | Short noun phrase identifying the metric (e.g., "Active Students", "System Uptime") | Yes |
| **Icon** | 20×20px icon from the icon system; tinted with `--primary` or status color | Optional |
| **Primary Value** | The main number — large, bold, JetBrains Mono font | Yes |
| **Secondary Context** | Sub-metric, delta, or descriptor below the primary value | Optional |
| **Trend Badge** | Percentage change vs. previous period with directional arrow | Optional |
| **Sparkline** | 28-point mini line chart showing the metric's trajectory | Optional |
| **Status Dot** | Colored dot + text for operational status | Optional |
| **Detail Link** | Inline text link to the full drill-down page | Optional |

---

## 2. Card Variants

> Different operational contexts need different levels of information density. Six card variants serve the range from a quick glance at a single KPI to a rich multi-metric executive card.

### 2.1 Standard Card (Default)

> The workhorse variant used on ~80% of pages. Shows label, primary value, trend badge, and secondary context line. Used in 4-column KPI rows at the top of dashboards.

```
┌───────────────────────────────┐
│ 📊 Total Enrollments     ↑12% │
│                               │
│  2,413,847                    │
│  +142,301 from last month     │
└───────────────────────────────┘
```

**CSS:**
```css
.stat-card {
  background: var(--bg-surface-1);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);       /* 12px */
  padding: var(--space-5);               /* 20px */
  min-width: 200px;
  position: relative;
  transition: border-color 150ms ease, box-shadow 150ms ease;
  cursor: default;
}

.stat-card:hover {
  border-color: var(--border-default);
  box-shadow: var(--shadow-md);
}

.stat-card--clickable {
  cursor: pointer;
}

.stat-card--clickable:hover {
  border-color: var(--primary);
  box-shadow: 0 0 0 1px var(--primary), var(--shadow-md);
}

/* Dark theme (default) */
:root .stat-card {
  background: var(--bg-surface-1);   /* #0D1526 */
}

/* Light theme */
[data-theme="light"] .stat-card {
  background: var(--bg-surface-1);   /* #FFFFFF */
  box-shadow: var(--shadow-sm);
}
```

---

### 2.2 Hero Card

> Used when one metric dominates a page (e.g., the "Total Platform Health Score" on the Executive Dashboard). Spans full width or 2 columns. Larger typography. May include a gauge ring or large sparkline.

```
┌──────────────────────────────────────────────────────────────┐
│  PLATFORM HEALTH SCORE                        ● LIVE         │
│                                                              │
│         98.7%          [============================== ]    │
│                         Target: 99.5%   ↓ 0.3% from SLA    │
│                                                              │
│  Uptime: 99.94%  ·  Avg Latency: 42ms  ·  Error Rate: 0.01%│
└──────────────────────────────────────────────────────────────┘
```

**CSS:**
```css
.stat-card--hero {
  grid-column: span 2;
  padding: var(--space-6);   /* 24px */
  background: linear-gradient(
    135deg,
    var(--bg-surface-1) 0%,
    color-mix(in srgb, var(--primary) 6%, var(--bg-surface-1)) 100%
  );
  border-color: color-mix(in srgb, var(--primary) 30%, transparent);
}

.stat-card--hero .stat-card__value {
  font-size: 3rem;
  line-height: 1;
}
```

---

### 2.3 Status Card

> Used for infrastructure/operational metrics where the state (healthy / degraded / critical) matters as much as the number itself. Background tints and border color communicate severity at a glance.

```
┌───────────────────────────────┐
│ ● Database Cluster     HEALTHY│
│                               │
│  99.94%                       │
│  Uptime — last 30 days        │
│                               │
│  3 replicas · 0 lag           │
└───────────────────────────────┘
```

**Status color mapping:**

| State | Border | Background tint | Dot color |
|---|---|---|---|
| `healthy` | `--success` | `--success` 5% | `--success` |
| `warning` | `--warning` | `--warning` 5% | `--warning` |
| `critical` | `--error` | `--error` 5% | `--error` (pulse) |
| `unknown` | `--border-subtle` | transparent | `--text-muted` |

**CSS:**
```css
.stat-card--status-healthy {
  border-color: var(--success);
  background: color-mix(in srgb, var(--success) 5%, var(--bg-surface-1));
}

.stat-card--status-warning {
  border-color: var(--warning);
  background: color-mix(in srgb, var(--warning) 5%, var(--bg-surface-1));
}

.stat-card--status-critical {
  border-color: var(--error);
  background: color-mix(in srgb, var(--error) 5%, var(--bg-surface-1));
  animation: stat-card-critical-pulse 2s ease-in-out infinite;
}

@keyframes stat-card-critical-pulse {
  0%, 100% { box-shadow: 0 0 0 0 color-mix(in srgb, var(--error) 40%, transparent); }
  50%       { box-shadow: 0 0 0 6px color-mix(in srgb, var(--error) 0%, transparent); }
}
```

---

### 2.4 Sparkline Card

> Adds a 28-point mini line chart to the right side of the card. Used when the trajectory of a metric is as important as its current value — revenue trend, enrollment growth, error rate over 24h.

```
┌────────────────────────────────────────┐
│ Revenue (MTD)                    ↑8.2% │
│                                        │
│  ₹4.82 Cr        /\/\___/\/\/\___/\   │
│  ₹5.2 Cr target        (sparkline)     │
└────────────────────────────────────────┘
```

**CSS:**
```css
.stat-card--sparkline {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: var(--space-3);
  align-items: center;
}

.stat-card__sparkline-wrap {
  width: 80px;
  height: 40px;
  opacity: 0.8;
}

/* sparkline SVG path color inherits from parent */
.stat-card__sparkline-wrap svg path {
  stroke: var(--primary);
  fill: none;
  stroke-width: 1.5;
}

[data-theme="light"] .stat-card__sparkline-wrap svg path {
  stroke: var(--primary);   /* #4F46E5 in light */
}
```

---

### 2.5 Comparison Card

> Shows two periods side-by-side (This Period vs. Last Period / This Year vs. Last Year / vs. Target). Used on Finance and Compliance pages where relative performance context is critical.

```
┌──────────────────────────────────────┐
│ Subscription Revenue          MTD    │
│                                      │
│  ₹4.82 Cr      vs   ₹4.45 Cr        │
│  This Month         Last Month       │
│                                      │
│  ↑ +₹0.37 Cr  (+8.3%)               │
└──────────────────────────────────────┘
```

**CSS:**
```css
.stat-card--comparison .stat-card__compare-grid {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  gap: var(--space-2);
  align-items: start;
}

.stat-card--comparison .stat-card__compare-vs {
  font-size: var(--text-xs);
  color: var(--text-muted);
  padding-top: var(--space-1);
  text-align: center;
}

.stat-card--comparison .stat-card__compare-period {
  font-size: var(--text-xs);
  color: var(--text-muted);
  margin-top: var(--space-1);
}
```

---

### 2.6 Mini Card

> Compact single-line card for secondary metrics. Used when many metrics need to be shown without overwhelming the layout (e.g., 8-metric infrastructure status rows, exam readiness checklists).

```
┌────────────────────────────────┐
│ ● API Gateway     99.9%  ↑0.1% │
└────────────────────────────────┘
```

**CSS:**
```css
.stat-card--mini {
  padding: var(--space-3) var(--space-4);   /* 12px 16px */
  display: flex;
  align-items: center;
  gap: var(--space-3);
  min-height: 48px;
}

.stat-card--mini .stat-card__value {
  font-size: var(--text-lg);   /* 18px */
  line-height: 1;
}
```

---

## 3. Internal Elements

### 3.1 Primary Value Typography

> The primary value is the most important piece of information on the card. It uses JetBrains Mono (monospace) so that numbers align vertically in a grid and don't cause layout shift when values change (monospace digits are equal-width).

```css
.stat-card__value {
  font-family: var(--font-mono);      /* JetBrains Mono */
  font-size: var(--text-3xl);         /* 30px */
  font-weight: 700;
  line-height: 1.1;
  color: var(--text-primary);
  letter-spacing: -0.02em;
  font-variant-numeric: tabular-nums; /* ensures digit alignment */
}

/* Dark theme */
:root .stat-card__value {
  color: var(--text-primary);   /* #F1F5F9 */
}

/* Light theme */
[data-theme="light"] .stat-card__value {
  color: var(--text-primary);   /* #0F172A */
}
```

---

### 3.2 Trend Badge

> Trend badges communicate direction and magnitude at a glance using color + icon. Green = improvement, red = regression. The badge always shows the delta vs. the comparison period (default: previous 30 days).

```
↑ +12.4%   (green — positive)
↓ −3.1%    (red — negative)
→ 0.0%     (neutral — gray)
```

**CSS:**
```css
.stat-card__trend {
  display: inline-flex;
  align-items: center;
  gap: 2px;
  font-size: var(--text-xs);    /* 12px */
  font-weight: 600;
  font-family: var(--font-mono);
  padding: 2px 6px;
  border-radius: var(--radius-full);
}

.stat-card__trend--up {
  color: var(--success);
  background: color-mix(in srgb, var(--success) 12%, transparent);
}

.stat-card__trend--down {
  color: var(--error);
  background: color-mix(in srgb, var(--error) 12%, transparent);
}

.stat-card__trend--neutral {
  color: var(--text-muted);
  background: var(--bg-surface-2);
}

/* Both themes — inherit from token system automatically */
```

---

### 3.3 Card Label

```css
.stat-card__label {
  font-size: var(--text-xs);      /* 12px */
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--text-muted);
  margin-bottom: var(--space-2);
}

/* Dark theme */
:root .stat-card__label {
  color: var(--text-muted);   /* #64748B */
}

/* Light theme */
[data-theme="light"] .stat-card__label {
  color: var(--text-muted);   /* #64748B */
}
```

---

### 3.4 Secondary Context Line

```css
.stat-card__secondary {
  font-size: var(--text-sm);   /* 14px */
  color: var(--text-secondary);
  margin-top: var(--space-1);
  line-height: 1.4;
}

:root .stat-card__secondary {
  color: var(--text-secondary);   /* #94A3B8 */
}

[data-theme="light"] .stat-card__secondary {
  color: var(--text-secondary);   /* #475569 */
}
```

---

### 3.5 Live Indicator

> When a stat card is connected to a WebSocket stream, a pulsing "LIVE" badge appears at the top-right corner. This signals to the operator that the number updates automatically and no manual refresh is needed.

```
● LIVE
```

```css
.stat-card__live-badge {
  position: absolute;
  top: var(--space-3);
  right: var(--space-3);
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.1em;
  color: var(--success);
  background: color-mix(in srgb, var(--success) 10%, transparent);
  border: 1px solid color-mix(in srgb, var(--success) 25%, transparent);
  padding: 2px 6px;
  border-radius: var(--radius-full);
}

.stat-card__live-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--success);
  animation: live-pulse 1.5s ease-in-out infinite;
}

@keyframes live-pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50%       { opacity: 0.4; transform: scale(0.8); }
}
```

---

## 4. Layout Patterns

> Stat cards are never used in isolation — they are always arranged in one of three layout patterns depending on how many metrics need to be shown and the relative importance of each metric.

### 4.1 Symmetric Grid (4-up, 3-up, 6-up)

> The most common layout. Equal-width cards in a CSS Grid row. Gaps collapse gracefully at smaller viewports.

```
[  Card 1  ] [  Card 2  ] [  Card 3  ] [  Card 4  ]
```

```css
.stat-card-grid {
  display: grid;
  gap: var(--space-4);   /* 16px */
}

.stat-card-grid--4up { grid-template-columns: repeat(4, 1fr); }
.stat-card-grid--3up { grid-template-columns: repeat(3, 1fr); }
.stat-card-grid--6up { grid-template-columns: repeat(6, 1fr); }
.stat-card-grid--2up { grid-template-columns: repeat(2, 1fr); }

/* Responsive collapse */
@media (max-width: 1280px) {
  .stat-card-grid--4up { grid-template-columns: repeat(2, 1fr); }
  .stat-card-grid--6up { grid-template-columns: repeat(3, 1fr); }
}

@media (max-width: 768px) {
  .stat-card-grid--4up,
  .stat-card-grid--3up,
  .stat-card-grid--6up { grid-template-columns: 1fr 1fr; }
}
```

---

### 4.2 Featured + Supporting (Hero Layout)

> One large hero card spans 2 columns on the left, flanked by 2–3 supporting cards on the right. Used when one metric is the primary signal (Platform Health Score, Total Revenue, Exam Readiness Score).

```
[                      ] [  Card 2  ]
[  Hero Card (span 2)  ] [  Card 3  ]
[                      ] [  Card 4  ]
```

```css
.stat-card-grid--hero-layout {
  display: grid;
  grid-template-columns: 2fr 1fr;
  grid-template-rows: auto auto auto;
  gap: var(--space-4);
}

.stat-card-grid--hero-layout .stat-card--hero {
  grid-row: span 3;
}
```

---

### 4.3 Inline Mini Strip

> A horizontal strip of mini cards. Used below a section header to show infrastructure service statuses, exam server stats, or compliance check results without consuming vertical space.

```
● Svc A  99.9%  ·  ● Svc B  100%  ·  ● Svc C  98.7%  ·  ● Svc D  99.4%
```

```css
.stat-card-strip {
  display: flex;
  gap: var(--space-2);
  flex-wrap: wrap;
}

.stat-card-strip .stat-card--mini {
  flex: 0 1 auto;
  min-width: 160px;
}
```

---

## 5. Real-Time Update Behavior

> When a stat card is connected to a WebSocket data stream, its value updates in place. The update must be visually noticeable (brief highlight flash) but not jarring. The card must never cause layout shift during updates because the monospace font keeps digit widths stable.

### 5.1 Value Update Animation

```css
@keyframes stat-value-flash {
  0%   { color: var(--text-primary); }
  20%  { color: var(--primary); }
  100% { color: var(--text-primary); }
}

.stat-card__value--updated {
  animation: stat-value-flash 600ms ease-out;
}
```

### 5.2 Value Counter Animation (on page load)

> On initial page load, numeric values animate from 0 to their actual value using a JavaScript counter. Duration: 800ms. Easing: ease-out cubic. Only runs once per page load — not on subsequent WebSocket updates (which would be distracting).

```javascript
// Pseudocode — implemented in component JS layer
function animateCounter(element, targetValue, duration = 800) {
  const startTime = performance.now();
  const startValue = 0;
  const isDecimal = targetValue % 1 !== 0;

  function update(currentTime) {
    const elapsed = currentTime - startTime;
    const progress = Math.min(elapsed / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3); // ease-out cubic
    const current = startValue + (targetValue - startValue) * eased;
    element.textContent = isDecimal
      ? current.toFixed(2)
      : Math.floor(current).toLocaleString('en-IN');
    if (progress < 1) requestAnimationFrame(update);
  }
  requestAnimationFrame(update);
}
```

### 5.3 WebSocket Reconnection State

> If the WebSocket connection is lost, stat cards that relied on live data show a subtle "stale" visual treatment to signal that the displayed values may be outdated.

```css
.stat-card--stale {
  opacity: 0.6;
  border-color: var(--warning);
  position: relative;
}

.stat-card--stale::after {
  content: 'DATA STALE';
  position: absolute;
  bottom: var(--space-2);
  right: var(--space-3);
  font-size: 9px;
  font-weight: 700;
  letter-spacing: 0.1em;
  color: var(--warning);
  opacity: 0.7;
}
```

---

## 6. Loading State (Skeleton)

> Before data arrives from the API, stat cards render as animated skeleton placeholders. This prevents layout shift and communicates loading progress.

```
┌───────────────────────────────┐
│ ░░░░░░░░░░           ░░░░░░░ │
│                               │
│  ░░░░░░░░░░░░                 │
│  ░░░░░░░░░░░░░░░░░            │
└───────────────────────────────┘
```

```css
@keyframes skeleton-shimmer {
  0%   { background-position: -200% center; }
  100% { background-position: 200% center; }
}

.stat-card--loading .stat-card__label,
.stat-card--loading .stat-card__value,
.stat-card--loading .stat-card__secondary,
.stat-card--loading .stat-card__trend {
  border-radius: var(--radius-sm);
  background: linear-gradient(
    90deg,
    var(--bg-surface-2) 25%,
    color-mix(in srgb, var(--text-muted) 15%, var(--bg-surface-2)) 50%,
    var(--bg-surface-2) 75%
  );
  background-size: 200% 100%;
  animation: skeleton-shimmer 1.5s ease-in-out infinite;
  color: transparent;
  pointer-events: none;
  user-select: none;
}

/* Light theme skeleton — slightly different shimmer */
[data-theme="light"] .stat-card--loading .stat-card__value {
  background: linear-gradient(
    90deg,
    #E2E8F0 25%,
    #F1F5F9 50%,
    #E2E8F0 75%
  );
  background-size: 200% 100%;
  animation: skeleton-shimmer 1.5s ease-in-out infinite;
}
```

---

## 7. Empty / Error State

```css
.stat-card--error {
  border-color: var(--error);
  opacity: 0.7;
}

.stat-card--error .stat-card__value::after {
  content: '—';
  font-family: var(--font-mono);
  color: var(--text-muted);
}

.stat-card--error .stat-card__secondary {
  color: var(--error);
  font-size: var(--text-xs);
}
```

**Error display pattern:**
```
┌───────────────────────────────┐
│ Total Enrollments             │
│                               │
│  —                            │
│  Failed to load · Retry ↻     │
└───────────────────────────────┘
```

---

## 8. Accessibility

> Stat cards must be accessible to screen readers and keyboard users. All interactive (clickable) cards receive proper ARIA roles and focus styles.

```html
<!-- Non-interactive stat card -->
<article class="stat-card" aria-label="Total Enrollments: 2,413,847, up 12.4% from last month">
  <span class="stat-card__label">Total Enrollments</span>
  <span class="stat-card__value" aria-live="polite" aria-atomic="true">2,413,847</span>
  <span class="stat-card__trend stat-card__trend--up" aria-label="Up 12.4%">↑ 12.4%</span>
  <span class="stat-card__secondary">+142,301 from last month</span>
</article>

<!-- Clickable stat card (links to drill-down page) -->
<a class="stat-card stat-card--clickable"
   href="/portal/revenue/breakdown"
   aria-label="Revenue MTD: ₹4.82 Crore. Click to view breakdown.">
  ...
</a>
```

**Focus ring for keyboard navigation:**
```css
.stat-card--clickable:focus-visible {
  outline: 2px solid var(--primary);
  outline-offset: 2px;
  border-color: var(--primary);
}
```

---

## 9. Complete Dark + Light Theme Token Reference

> All tokens below are defined in `00-global-layout.md`. This table maps each visual property to its token in both themes, enabling exact reproduction of the component in both modes.

| Property | Dark token / value | Light token / value |
|---|---|---|
| Card background | `--bg-surface-1` → `#0D1526` | `--bg-surface-1` → `#FFFFFF` |
| Card border (default) | `--border-subtle` → `#1E293B` | `--border-subtle` → `#E2E8F0` |
| Card border (hover) | `--border-default` → `#334155` | `--border-default` → `#CBD5E1` |
| Card border (focus) | `--primary` → `#6366F1` | `--primary` → `#4F46E5` |
| Primary value text | `--text-primary` → `#F1F5F9` | `--text-primary` → `#0F172A` |
| Secondary text | `--text-secondary` → `#94A3B8` | `--text-secondary` → `#475569` |
| Label text | `--text-muted` → `#64748B` | `--text-muted` → `#64748B` |
| Trend up | `--success` → `#10B981` | `--success` → `#059669` |
| Trend down | `--error` → `#EF4444` | `--error` → `#DC2626` |
| Trend neutral | `--text-muted` → `#64748B` | `--text-muted` → `#64748B` |
| Status healthy border | `--success` → `#10B981` | `--success` → `#059669` |
| Status warning border | `--warning` → `#F59E0B` | `--warning` → `#D97706` |
| Status critical border | `--error` → `#EF4444` | `--error` → `#DC2626` |
| Live badge | `--success` → `#10B981` | `--success` → `#059669` |
| Skeleton base | `--bg-surface-2` → `#131F38` | `#E2E8F0` |
| Shadow (card) | `--shadow-md` | `--shadow-md` + extra |
| Font (values) | `--font-mono` → JetBrains Mono | `--font-mono` → JetBrains Mono |
| Radius | `--radius-lg` → `12px` | `--radius-lg` → `12px` |

---

## 10. Full CSS Block (Copy-Paste Ready)

```css
/* ============================================================
   STAT CARDS — EduForge Admin Portal
   Supports: dark (default) + light theme via data-theme="light"
   Tokens defined in: 00-global-layout.md
   ============================================================ */

/* ── Base card ── */
.stat-card {
  background: var(--bg-surface-1);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  padding: var(--space-5);
  position: relative;
  transition: border-color 150ms ease, box-shadow 150ms ease;
}

.stat-card--clickable { cursor: pointer; }
.stat-card--clickable:hover {
  border-color: var(--primary);
  box-shadow: 0 0 0 1px var(--primary), var(--shadow-md);
}
.stat-card--clickable:focus-visible {
  outline: 2px solid var(--primary);
  outline-offset: 2px;
}

/* ── Light theme overrides ── */
[data-theme="light"] .stat-card {
  background: var(--bg-surface-1);       /* #FFFFFF */
  border-color: var(--border-subtle);    /* #E2E8F0 */
  box-shadow: 0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04);
}

[data-theme="light"] .stat-card:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

/* ── Label ── */
.stat-card__label {
  display: block;
  font-size: var(--text-xs);
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--text-muted);
  margin-bottom: var(--space-2);
}

/* ── Primary value ── */
.stat-card__value {
  display: block;
  font-family: var(--font-mono);
  font-size: var(--text-3xl);
  font-weight: 700;
  line-height: 1.1;
  letter-spacing: -0.02em;
  font-variant-numeric: tabular-nums;
  color: var(--text-primary);
}

/* ── Secondary line ── */
.stat-card__secondary {
  display: block;
  font-size: var(--text-sm);
  color: var(--text-secondary);
  margin-top: var(--space-1);
  line-height: 1.4;
}

/* ── Trend badge ── */
.stat-card__trend {
  display: inline-flex;
  align-items: center;
  gap: 2px;
  font-size: var(--text-xs);
  font-weight: 600;
  font-family: var(--font-mono);
  padding: 2px 6px;
  border-radius: var(--radius-full);
  position: absolute;
  top: var(--space-4);
  right: var(--space-4);
}
.stat-card__trend--up    { color: var(--success); background: color-mix(in srgb, var(--success) 12%, transparent); }
.stat-card__trend--down  { color: var(--error);   background: color-mix(in srgb, var(--error)   12%, transparent); }
.stat-card__trend--flat  { color: var(--text-muted); background: var(--bg-surface-2); }

/* ── Live badge ── */
.stat-card__live-badge {
  position: absolute; top: var(--space-3); right: var(--space-3);
  display: inline-flex; align-items: center; gap: 4px;
  font-size: 10px; font-weight: 700; letter-spacing: 0.1em;
  color: var(--success);
  background: color-mix(in srgb, var(--success) 10%, transparent);
  border: 1px solid color-mix(in srgb, var(--success) 25%, transparent);
  padding: 2px 6px; border-radius: var(--radius-full);
}
.stat-card__live-dot {
  width: 6px; height: 6px; border-radius: 50%;
  background: var(--success);
  animation: live-pulse 1.5s ease-in-out infinite;
}

/* ── Status variants ── */
.stat-card--status-healthy  { border-color: var(--success); background: color-mix(in srgb, var(--success) 5%, var(--bg-surface-1)); }
.stat-card--status-warning  { border-color: var(--warning); background: color-mix(in srgb, var(--warning) 5%, var(--bg-surface-1)); }
.stat-card--status-critical { border-color: var(--error);   background: color-mix(in srgb, var(--error)   5%, var(--bg-surface-1)); animation: stat-card-critical-pulse 2s ease-in-out infinite; }

/* ── Hero variant ── */
.stat-card--hero {
  grid-column: span 2;
  padding: var(--space-6);
  background: linear-gradient(135deg, var(--bg-surface-1) 0%, color-mix(in srgb, var(--primary) 6%, var(--bg-surface-1)) 100%);
  border-color: color-mix(in srgb, var(--primary) 30%, transparent);
}
.stat-card--hero .stat-card__value { font-size: 3rem; line-height: 1; }

/* ── Mini variant ── */
.stat-card--mini {
  padding: var(--space-3) var(--space-4);
  display: flex; align-items: center; gap: var(--space-3);
  min-height: 48px;
}
.stat-card--mini .stat-card__value { font-size: var(--text-lg); line-height: 1; }

/* ── Loading skeleton ── */
.stat-card--loading .stat-card__label,
.stat-card--loading .stat-card__value,
.stat-card--loading .stat-card__secondary,
.stat-card--loading .stat-card__trend {
  border-radius: var(--radius-sm);
  background: linear-gradient(90deg, var(--bg-surface-2) 25%, color-mix(in srgb, var(--text-muted) 15%, var(--bg-surface-2)) 50%, var(--bg-surface-2) 75%);
  background-size: 200% 100%;
  animation: skeleton-shimmer 1.5s ease-in-out infinite;
  color: transparent;
}

[data-theme="light"] .stat-card--loading .stat-card__value,
[data-theme="light"] .stat-card--loading .stat-card__label,
[data-theme="light"] .stat-card--loading .stat-card__secondary {
  background: linear-gradient(90deg, #E2E8F0 25%, #F1F5F9 50%, #E2E8F0 75%);
  background-size: 200% 100%;
  animation: skeleton-shimmer 1.5s ease-in-out infinite;
}

/* ── Value update flash ── */
@keyframes stat-value-flash {
  0%   { color: var(--text-primary); }
  20%  { color: var(--primary); }
  100% { color: var(--text-primary); }
}
.stat-card__value--updated { animation: stat-value-flash 600ms ease-out; }

/* ── Stale data ── */
.stat-card--stale { opacity: 0.6; border-color: var(--warning); }
.stat-card--stale::after {
  content: 'DATA STALE'; position: absolute;
  bottom: var(--space-2); right: var(--space-3);
  font-size: 9px; font-weight: 700; letter-spacing: 0.1em;
  color: var(--warning); opacity: 0.7;
}

/* ── Grid layouts ── */
.stat-card-grid { display: grid; gap: var(--space-4); }
.stat-card-grid--4up { grid-template-columns: repeat(4, 1fr); }
.stat-card-grid--3up { grid-template-columns: repeat(3, 1fr); }
.stat-card-grid--6up { grid-template-columns: repeat(6, 1fr); }
.stat-card-grid--2up { grid-template-columns: repeat(2, 1fr); }
.stat-card-grid--hero-layout { grid-template-columns: 2fr 1fr; grid-template-rows: auto auto auto; }
.stat-card-grid--hero-layout .stat-card--hero { grid-row: span 3; }

@media (max-width: 1280px) {
  .stat-card-grid--4up { grid-template-columns: repeat(2, 1fr); }
  .stat-card-grid--6up { grid-template-columns: repeat(3, 1fr); }
}
@media (max-width: 768px) {
  .stat-card-grid--4up,
  .stat-card-grid--3up,
  .stat-card-grid--6up { grid-template-columns: 1fr 1fr; }
}

/* ── Animations ── */
@keyframes live-pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50%       { opacity: 0.4; transform: scale(0.8); }
}
@keyframes stat-card-critical-pulse {
  0%, 100% { box-shadow: 0 0 0 0 color-mix(in srgb, var(--error) 40%, transparent); }
  50%       { box-shadow: 0 0 0 6px color-mix(in srgb, var(--error) 0%, transparent); }
}
@keyframes skeleton-shimmer {
  0%   { background-position: -200% center; }
  100% { background-position: 200% center; }
}
```

---

## 11. Usage Examples (for Page Specs)

> When writing page specification files, reference this component using the patterns below. Never re-document color or layout details — just reference the variant and describe the specific metric being shown.

**Example usage in a page spec:**

```markdown
### Section: KPI Bar
> Four stat cards in a `stat-card-grid--4up` layout. Each card uses the **Standard Card** variant
> (Component 10, §2.1) with real-time WebSocket updates. The live badge (§3.5) appears on all four
> cards since values stream from the metrics service every 5 seconds.

| Card | Metric | Trend vs | Sparkline |
|---|---|---|---|
| Total Enrollments | 2,413,847 | Last 30 days | 28-pt area chart |
| Active Exams | 74,000 | Same time yesterday | 28-pt line chart |
| Platform Uptime | 99.94% | Last 90 days | — |
| Revenue MTD | ₹4.82 Cr | Same MTD last year | 28-pt bar chart |
```

---

*Component: `10-stat-cards.md` | Scope: Global — all portals | Theme: Dark (default) + Light | Updated: 2026-03*
