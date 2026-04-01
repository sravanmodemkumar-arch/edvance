# Component: Data Display — Stat Cards, Badges, Avatars, Charts

---

## Stat Card (KPI Card)

### Layout Variants

**Compact (4-column dashboard row):**
```
┌──────────────────────────┐
│  📊  Total Students      │
│                          │
│  1,24,700                │  ← large number
│  ↑ 12% from last month   │  ← trend
└──────────────────────────┘
```

**Detailed (2-column):**
```
┌────────────────────────────────────────────┐
│  Total Students                  [📊 ▼]   │
│                                            │
│  1,24,700           ↑ 12%                 │
│                      vs last month         │
│                                            │
│  ████████████████░░  78% capacity          │
│                                            │
│  Hostelers: 34,200   Day: 90,500          │
└────────────────────────────────────────────┘
```

### Trend Indicator

| Trend | Icon | Token | Text |
|---|---|---|---|
| Up (positive) | ↑ | `--success` | `+12%` |
| Down (negative) | ↓ | `--error` | `-3%` |
| Down (positive — for bad metrics) | ↓ | `--success` | `-5% absences` |
| No change | → | `--text-muted` | `No change` |
| Not enough data | — | `--text-muted` | `—` |

### Skeleton Loading
- Card shape maintained
- Number replaced by shimmer bar (60% width)
- Label replaced by shimmer bar (40% width)
- Trend replaced by shimmer bar (30% width)

---

## Badge / Status Chip

### Layout
```
[● Active]    [● Suspended]   [● Pending]   [● Inactive]
```

### Status Colors

> All status badges use CSS token-based colors. The system automatically applies the correct shade for dark vs. light themes.

| Status | Text token | Dark hex | Light hex | Use Case |
|---|---|---|---|---|
| Active | `--success` | `#10B981` | `#059669` | User active, subscription active |
| Inactive | `--text-muted` | `#64748B` | `#64748B` | Archived, not enrolled |
| Pending | `--warning` | `#F59E0B` | `#D97706` | Awaiting action (BGV, fee, approval) |
| Suspended | `--error` | `#EF4444` | `#DC2626` | Account suspended |
| Trial | `#A78BFA` | `#A78BFA` | `#7C3AED` | Free trial user |
| Premium | `#FCD34D` | `#FCD34D` | `#D97706` | Paid subscriber |
| Expired | `--error` muted | `#EF4444` | `#DC2626` | Subscription expired |
| Verified | `--primary` | `#6366F1` | `#4F46E5` | BGV verified, email verified |
| Draft | `--text-muted` | `#64748B` | `#64748B` | Content draft, unpublished |
| Published | `--success` | `#10B981` | `#059669` | Content live |

### Size Variants

| Size | Padding | Font | Use Case |
|---|---|---|---|
| `xs` | 2px 6px | 10px | Dense tables |
| `sm` (default) | 3px 8px | 12px | Standard tables, cards |
| `md` | 4px 12px | 13px | Drawer headers, list items |
| `lg` | 6px 16px | 14px | Profile pages, hero sections |

### Role Badge (Access Level)

```
[L0 No Access]  [L1 Read]  [L2 Content]  [L3 Ops]  [L4 Admin]  [L5 Super]
```

Colors: L0 gray → L1 blue-gray → L2 blue → L3 indigo → L4 deep-purple → L5 red-purple

---

## Avatar

### Sizes
| Size | px | Use Case |
|---|---|---|
| `xs` | 24px | Dense list items, table cells |
| `sm` | 32px | Standard table rows, comment threads |
| `md` | 40px | Navigation, notification items |
| `lg` | 64px | Drawer profile headers |
| `xl` | 96px | Full profile page |
| `xxl` | 128px | Profile setup/edit |

### States

```
[Photo]         ← Has photo: circular crop of actual photo
[R K]           ← No photo: initials in colored circle (hashed from name)
[👤]            ← Fallback: generic person icon
[Photo + ✅]   ← With status indicator (bottom-right corner)
```

### Avatar Group (Multiple people)
```
[A] [B] [C] [+12]
```
- Overlapping circles (negative margin)
- Shows first 3 avatars + count for remainder
- Hover on count shows names in tooltip

---

## Progress Bar

### Layout Variants

**Linear:**
```
████████████░░░░░░  67%   Attendance
```

**With label:**
```
Attendance
████████████████░░  82%  ← inline percentage
```

**Segmented (multiple categories):**
```
[████████] [░░░░░] [▓▓▓]
Paid(65%)  Partial(20%) Defaulter(15%)
```

### Color Coding (Progress)

| Range | Color | Semantic |
|---|---|---|
| 0–40% | Red | Critical / Poor |
| 41–60% | Orange | Warning / Below average |
| 61–75% | Yellow | Average |
| 76–90% | Light green | Good |
| 91–100% | Dark green | Excellent |

---

## Chart Components

> All charts use lightweight library (Chart.js or Recharts).
> All charts must have: title, legend, tooltip on hover, export option.

### Line Chart (Performance Trend)
```
Score %
100 |                              ●
 80 |              ●──────────────
 60 |   ●──────────
 40 |
     Jan   Feb   Mar   Apr   May
```
- Smooth curves (bezier)
- Multiple lines (different colors) for comparison
- Hover: vertical tooltip showing all series values at that point

### Bar Chart (Subject-wise, Comparison)
```
Subject Performance
Maths    ████████████ 78%
Physics  ████████░░░░ 62%
Chemistry████████████ 84%
English  ████████████ 91%
```

### Donut / Pie Chart (Distribution)
```
        ╭───╮
       / Fee \
      │ Paid  │
      │  65%  │
       \ 20% /
        ╰───╯
     Partial Defaulter
         15%
```

### Heatmap (Attendance calendar)
```
     Jan
Mo  [░][▓][█][░][▓]
Tu  [█][█][░][▓][█]
...
```
- Color: white = absent, light = low, dark = full attendance

### Chart Common Behaviors

| Feature | Spec |
|---|---|
| Tooltip | Hover over point/bar → show value + label in popup |
| Legend | Click legend item → toggle that series visibility |
| Zoom | Drag to zoom in. Double-click to reset |
| Export | Download as PNG/SVG/CSV via [⋯] menu on chart |
| Responsive | Redraws on container resize |
| Empty | "No data yet" illustration + message |
| Loading | Shimmer overlay matching chart shape |

---

## Data Table Row Extras (Detail cells)

### Progress Cell
```
78%  ████████░░
```

### Trend Cell
```
↑ 12%   (green)
↓ 3%    (red)
```

### Multi-value Cell
```
Maths: 87 | Physics: 76 | Chem: 92
```
(Compact — tooltip shows full breakdown)

### Link Cell
```
[View 3 documents →]
```

### Action Cell
```
[Edit]  [View]  [⋯]
```

---

## Theme Support (Dark + Light)

```css
/* ── Status badge ── */
.badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 3px 8px;
  border-radius: var(--radius-full);
  font-size: var(--text-xs);
  font-weight: 600;
  letter-spacing: 0.03em;
}

/* Dark and light both use token-based colors */
.badge--active      { color: var(--success); background: color-mix(in srgb, var(--success) 12%, transparent); }
.badge--pending     { color: var(--warning); background: color-mix(in srgb, var(--warning) 12%, transparent); }
.badge--suspended   { color: var(--error);   background: color-mix(in srgb, var(--error)   12%, transparent); }
.badge--inactive    { color: var(--text-muted); background: var(--bg-surface-2); }
.badge--verified    { color: var(--primary); background: color-mix(in srgb, var(--primary) 12%, transparent); }
.badge--published   { color: var(--success); background: color-mix(in srgb, var(--success) 12%, transparent); }
.badge--draft       { color: var(--text-muted); background: var(--bg-surface-2); }

/* Light theme — status colors are slightly darker (defined in --success/--error tokens) */
/* No additional overrides needed — tokens handle the contrast shift */

/* ── Progress bar ── */
.progress-bar-track {
  background: var(--bg-surface-2);
  border-radius: var(--radius-full);
  height: 6px;
  overflow: hidden;
}
.progress-bar-fill {
  height: 100%;
  border-radius: var(--radius-full);
  transition: width 400ms ease-out;
}
/* Color coding by value — same tokens in both themes */
.progress-bar-fill[data-range="critical"]  { background: var(--error); }
.progress-bar-fill[data-range="warning"]   { background: var(--warning); }
.progress-bar-fill[data-range="average"]   { background: #FCD34D; }
.progress-bar-fill[data-range="good"]      { background: #34D399; }
.progress-bar-fill[data-range="excellent"] { background: var(--success); }

[data-theme="light"] .progress-bar-track { background: #E2E8F0; }

/* ── Avatar ── */
.avatar {
  border-radius: 50%;
  object-fit: cover;
  flex-shrink: 0;
}
.avatar--initials {
  display: flex; align-items: center; justify-content: center;
  background: color-mix(in srgb, var(--primary) 20%, var(--bg-surface-2));
  color: var(--primary);
  font-weight: 700;
  font-size: 0.4em; /* scales with width/height */
}

/* Status ring on avatar */
.avatar-wrap--online  { outline: 2px solid var(--success); }
.avatar-wrap--offline { outline: 2px solid var(--border-default); }
.avatar-wrap--busy    { outline: 2px solid var(--warning); }

/* ── Stat card (basic — use Component 10 for full spec) ── */
.kpi-card {
  background: var(--bg-surface-1);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  padding: var(--space-5);
}

:root .kpi-card      { background: var(--bg-surface-1); }   /* #0D1526 */
[data-theme="light"] .kpi-card { background: #FFFFFF; box-shadow: 0 1px 3px rgba(0,0,0,0.06); }

.kpi-card__value {
  font-family: var(--font-mono);
  font-size: var(--text-3xl);
  font-weight: 700;
  color: var(--text-primary);
  font-variant-numeric: tabular-nums;
}
.kpi-card__label { font-size: var(--text-xs); color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.08em; }
.kpi-card__trend--up   { color: var(--success); }
.kpi-card__trend--down { color: var(--error); }
```

### Token Quick Reference

| Property | Dark | Light |
|---|---|---|
| Badge bg (active/success) | `success` 12% tint | `success` 12% tint |
| Badge bg (pending/warn) | `warning` 12% tint | `warning` 12% tint |
| Badge bg (error) | `error` 12% tint | `error` 12% tint |
| Progress track | `--bg-surface-2` → `#131F38` | `#E2E8F0` |
| Avatar initials bg | primary 20% tint | primary 20% tint |
| KPI card bg | `--bg-surface-1` → `#0D1526` | `#FFFFFF` |
| KPI value font | `var(--font-mono)` JetBrains Mono | same |
| Trend up | `--success` → `#10B981` | `--success` → `#059669` |
| Trend down | `--error` → `#EF4444` | `--error` → `#DC2626` |

---

## Usage in Page Specs

```markdown
### Dashboard — KPI Row
→ Component: [Stat Card](../../components/07-data-display.md)
  4 cards in row:
  1. Total Students — 1,24,700 — trend vs last month
  2. Attendance Today — 94.2% — progress bar
  3. Fee Collection — ₹47.2L — vs monthly target
  4. Active Exams — 3 — badge count

### Student Row — Status
→ Badge: Active/Suspended (see status colors above)
→ Avatar: 32px with initials fallback
→ Attendance: Progress bar 0–100% with color coding
```
