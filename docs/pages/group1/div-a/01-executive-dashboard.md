# div-a-01 — Executive Dashboard

## 1. Platform Scale Reference

| Dimension | Value |
|---|---|
| Schools | 1,000 · avg 1,000 students · max 5,000 |
| Colleges (Intermediate) | 800 · avg 500 · max 2,000 |
| Coaching centres | 100 · avg 10,000 members · max 15,000 |
| Institution Groups | 150 · own 5–50 child institutions each |
| **Total institutions** | **2,050** |
| **Total students (floor)** | **2,400,000** |
| **Total students (ceiling)** | **7,600,000** |
| Peak concurrent exam users | 500,000 |
| Platform ARR | ₹60 Cr+ |
| Daily exam submissions | ~4 M |

**Architect's note:** At 500K concurrent, no dashboard query may touch raw tables during peak hours. Every metric must come from a Redis-cached materialised view refreshed every 60 s by Celery beat. One live SQL COUNT(*) during a peak coaching exam is a P1 incident.

---

## 2. Institution Taxonomy

| Type | Students | Revenue model | Dashboard signal |
|---|---|---|---|
| School | 200–5,000 | Annual flat | Volume; low per-unit revenue |
| College | 150–2,000 | Annual flat | Mid-tier; board-exam seasonal spikes |
| Coaching centre | 5,000–15,000 | Monthly postpaid + overage | Highest ARR; highest concurrent density |
| Group | Aggregate | Annual umbrella | Roll-up across 5–50 children |

---

## 3. Page Metadata

| Field | Value |
|---|---|
| Route | `/exec/dashboard/` |
| **Single page API** | **All partials from `/exec/dashboard/?part={name}`** |
| View | `ExecDashboardView` |
| Template | `exec/dashboard.html` |
| Priority | P0 |
| Roles | `exec`, `superadmin` |
| Theme tokens | bg-base `#070C18` · surface-1 `#0D1526` · surface-2 `#131F38` · primary `#6366F1` |

---

## 4. Full Page Wireframe

```
╔══════════════════════════════════════════════════════════════════════════════╗
║ [≡] Srav                                   [🔔 3]  [Exec ▾]  [⚙]          ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ Executive Dashboard              [⚙ Prefs]  [↺ Refresh]  [📅 Today ▾]     ║
╠══════════════╦═════════════╦══════════════╦══════════════╦════════╦═════════╣
║  ARR         ║ Institutions║ Active Stud. ║ Exams Today  ║ Uptime ║At-Risk  ║
║  ₹59.8Cr    ║   2,050     ║   818K       ║   14,280     ║ 99.94% ║  48     ║
║  ▲ 2.1%     ║   ▲ 12      ║   ▲ 3.2%    ║   ▲ 8%       ║ ✅     ║  ▼ 2   ║
╠═══════════════════════════════╦════════════════════════════════════════════╣
║  PLATFORM HEALTH              ║  EXAM OPS                                  ║
║  [24h] [7d] [30d]             ║  Live:14  Sched:142  Issues:2              ║
║  ● ● ●  Exam  Auth  Storage   ║  ┌─────────┬──────────┬──────────┬──────┐ ║
║  ● ● ●  API   Email Proctor   ║  │ABC Coach│JEE Mock42│ 4,200    │Live  │ ║
║  "99.94% · 3m 21s downtime"   ║  │XYZ Sch. │Math Test │   280    │Live  │ ║
║  [View Full Platform Health →] ║  │...      │...       │...       │...   │ ║
║                                ║  [View All Exams →]                       ║
╠═══════════════════════════════╩════════════════════════════════════════════╣
║  BUSINESS OVERVIEW                                                          ║
║  [Growth ●] [Revenue] [Institutions]                                       ║
║  ┌──────────────────────────────────────────────────────────────────────┐  ║
║  │ Line chart: Institution count by type, last 12 months                │  ║
║  └──────────────────────────────────────────────────────────────────────┘  ║
╠══════════════════════════════╦═════════════════════════════════════════════╣
║  REVENUE & BILLING           ║  ACTIVITY FEED                              ║
║  [MTD ●] [QTD] [YTD]         ║  [All ●] [Exam] [Billing] [Incident]       ║
║  MRR: ₹4.98 Cr ▲ 1.2%       ║  ● 2m ago  Exam completed · ABC Coaching   ║
║  Net New: +₹24.6 L           ║  ● 5m ago  Invoice paid · XYZ School       ║
║  ⚠ ₹92.4L overdue (62 insts) ║  ● 8m ago  New institution onboarded       ║
║  [View Financial Overview →]  ║  [Load 20 more...]                         ║
╚══════════════════════════════╩═════════════════════════════════════════════╝
```

---

## 5. Sections — Deep Specification

### 5.1 Page Header

```
[Executive Dashboard]                    [⚙ Prefs]  [↺ Refresh]  [📅 Today ▾]
```

**[⚙ Prefs] button**
- Opens Preferences Drawer (§6.1)
- Icon: 20×20 gear SVG, `text-[#8892A4]`, hover `text-white`
- Tooltip: "Customise dashboard"

**[↺ Refresh] button**
- Fetches all partials simultaneously
- HTMX: `hx-get="/exec/dashboard/?part=all" hx-target="#dash-body" hx-swap="innerHTML"`
- Icon spins 360° during fetch: `animate-spin`
- Keyboard: `R`

**[📅 Today ▾] date picker**
- Dropdown menu (not a calendar): Today · Yesterday · This Week · This Month · Last 30 Days · Last Quarter · Custom
- Applies to KPI bar and Business Overview only
- URL param: `?range=today`
- Triggers: `hx-get="/exec/dashboard/?part=kpi&range={value}"`
- Custom: opens a dual-input date range (from/to)
- Active selection shown in button label

---

### 5.2 KPI Bar — Section A

**HTMX target:** `id="kpi-bar"` `hx-get="/exec/dashboard/?part=kpi&range={{ range }}"` `hx-trigger="load"` `hx-swap="innerHTML"`

**Grid:** `grid grid-cols-6 gap-4` desktop · `grid-cols-3` tablet (<1280px) · `grid-cols-2` mobile (<768px)

**Card anatomy:**
```
┌──────────────────────────────┐
│ ANNUAL RECURRING REVENUE     │  ← 11px, uppercase, tracking-widest, #8892A4
│                              │
│ ₹59.8 Cr                     │  ← 28px, font-bold, text-white
│                              │
│ ▲ 2.1% vs last year          │  ← 12px, text-green-400 / text-red-400 / text-gray-500
└──────────────────────────────┘
bg-[#0D1526], border border-[#1E2D4A], rounded-xl, p-5
Hover: border-[#6366F1], transition-colors duration-150
```

**Loading state (before data arrives):**
`<div class="animate-pulse bg-[#1E2D4A] rounded-xl h-[88px]"></div>` per card

**Count-up animation:** On first load only (not poll), numbers animate from 0 → final value over 600ms using `requestAnimationFrame`. Data attribute `data-count-up="59.8"` drives JS.

**Cards:**

| # | Label | Formula | Delta basis | Good dir. | Alert | Click |
|---|---|---|---|---|---|---|
| 1 | Annual Recurring Revenue | Pre-computed billing aggregate · Decimal only | vs same month prior year | ▲ | None | Opens Revenue mini-drawer |
| 2 | Total Institutions | COUNT(status='active') | vs 30 days ago | ▲ | None | → `/exec/institutions/` |
| 3 | Active Students Today | DAU from session events | vs yesterday | ▲ | <500K on school day = amber | → `/exec/student-analytics/` |
| 4 | Exams Today | Count with status ∈ {scheduled, live, completed} | vs yesterday | ▲ | 0 on weekday = amber | → `/exec/exam-catalog/` |
| 5 | Platform Uptime | Weighted avg by SLA tier, MTD | vs last month | ▲ | <99.5% = red; <99.7% = amber | → `/exec/platform-health/` |
| 6 | At-Risk Institutions | churn_risk_score > 60 | vs 7 days ago | ▼ (less is good) | >100 = red | Opens At-Risk drawer |

**Card 6 reverse logic:** Delta is green when number goes DOWN (fewer at-risk), red when it goes UP. This is set via `data-reverse-delta="true"` attribute.

---

### 5.3 Platform Health Mini — Section B

**HTMX:** `id="health-mini"` `hx-get="/exec/dashboard/?part=health&range=24h"` `hx-trigger="load, every 30s[!document.querySelector('.drawer-open,.modal-open')]"` `hx-swap="innerHTML"`

**Poll pause logic:** The boolean expression `!document.querySelector('.drawer-open,.modal-open')` prevents reloading the section — and thereby destroying open drawers — while any overlay is visible.

**Range toggle buttons:**
```
[24h] [7d] [30d]
```
- Active: `bg-[#131F38] text-white border border-[#6366F1] rounded-md px-3 py-1 text-sm`
- Inactive: `text-[#8892A4] hover:text-white px-3 py-1 text-sm`
- Click: `hx-get="/exec/dashboard/?part=health&range=7d" hx-target="#health-mini" hx-swap="innerHTML"`

**Service grid (3 × 2, or 6 × 1 on mobile):**

Each service circle:
- Diameter: 44px, `rounded-full`
- Operational: `bg-green-500`  Degraded: `bg-yellow-500`  Down: `bg-red-600`  Unknown: `bg-gray-600`
- Pulsing ring when Down: `ring-2 ring-red-500 ring-offset-2 ring-offset-[#0D1526] animate-pulse`
- Hover → tooltip (absolute positioned, z-50): "Exam Engine · P99: 142ms · 99.97% uptime"
- Click → opens Service Detail Drawer (§6.2) — NOT navigation

Service name (below circle): 10px, `text-[#8892A4]`

**Services:**
1. Exam Engine
2. Auth Service
3. File Storage
4. API Gateway
5. Email / SMS
6. Proctoring

**Sparklines:** 60px wide × 24px tall per service. Last 20 data points. Rendered as inline SVG `<polyline>`. Red stroke if any point > 2× P50 baseline. Tooltip on hover: last value.

**Summary line:** `"99.94% overall uptime · 3 min 21 s downtime this month"` — 12px, `text-[#8892A4]`

**[View Full Platform Health →]:** text link, `text-[#6366F1] hover:underline`, navigates to `/exec/platform-health/`

---

### 5.4 Exam Ops Mini — Section C

**HTMX:** `id="exams-mini"` `hx-get="/exec/dashboard/?part=exams"` `hx-trigger="load, every 30s[!document.querySelector('.drawer-open,.modal-open')]"` `hx-swap="innerHTML"`

**Stats strip (4 small cards):**

| Card | Description | Colour if > 0 |
|---|---|---|
| Live Now | Exams currently active | `text-green-400` |
| Scheduled Today | Start time is today, status = scheduled | `text-blue-400` |
| Submissions Today | Exams completed today | `text-green-400` |
| Issues | Exams with submission failures or paused | `text-red-400` if > 0 |

Each card: `bg-[#131F38] rounded-lg px-3 py-2`, 14px number, 11px label.

**Live exams mini-table:**
- 5 rows maximum (top 5 by urgency: live first sorted by student count desc, then nearest start time)
- No pagination, no filters (this is a snapshot)
- Columns: Institution (truncated 18 chars) · Exam name (truncated 20 chars) · Students · Status dot

Status dot: 8px circle, pulsing green for Live (`animate-pulse bg-green-500`), blue for Scheduled.

**Row interaction:**
- Hover: `bg-[#131F38]` row highlight
- Click: `hx-get="/exec/dashboard/?part=exam-detail&id={{ exam.id }}"` `hx-target="#drawer-container"` → loads Exam Detail Drawer (§6.3) without page navigation

**Empty state:** "No live exams right now" · grey illustration · 60px height

**[View All Exams →]:** text link to `/exec/exam-catalog/`

---

### 5.5 Business Overview — Section D

**HTMX:** `id="business-overview"` `hx-get="/exec/dashboard/?part=business&tab=growth"` `hx-trigger="load"` `hx-swap="innerHTML"`

**Tab bar (within the partial — tabs + chart together):**
```
[Growth ●] [Revenue] [Institutions]
```
- Container: `flex gap-2 mb-4`
- Active pill: `bg-[#6366F1] text-white rounded-full px-4 py-1 text-sm font-medium`
- Inactive: `text-[#8892A4] hover:text-white px-4 py-1 text-sm cursor-pointer`
- Click: `hx-get="/exec/dashboard/?part=business&tab=revenue" hx-target="#business-overview" hx-swap="innerHTML"` — replaces the entire section including tabs

**Tab: Growth**
- Chart.js Line (v4.4.2)
- `id="chart-growth"` — uses `window._charts` registry to destroy before re-create on HTMX swap
- X-axis: 12 months (Jan–Dec labels, abbreviated)
- Y-axis: Institution count (left, integer)
- Right Y-axis (secondary): New institutions per month (bars, grey `rgba(255,255,255,0.1)`)
- Series: Schools `#3B82F6` · Colleges `#6366F1` · Coaching `#F59E0B` · Groups `#14B8A6`
- Legend: below chart, horizontal, 12px
- Tooltip: "March 2026 | Schools: 982 | Colleges: 798 | Coaching: 98 | Groups: 148 | Total: 2,026 | New this month: +12"
- Grid lines: `color: 'rgba(255,255,255,0.05)'`
- Chart height: 220px

**Tab: Revenue**
- Chart.js Bar (stacked)
- Same X-axis
- Y-axis: ARR in ₹ Cr
- Stacks: Standard `#60A5FA` · Professional `#818CF8` · Enterprise `#A78BFA`
- Tooltip: "March 2026 | Standard: ₹19.8 Cr | Professional: ₹24.6 Cr | Enterprise: ₹15.4 Cr | Total: ₹59.8 Cr"
- Below chart: MoM growth badge `▲ 1.2% MoM`

**Tab: Institutions**
- Chart.js Doughnut
- Segments: School 48.8% `#3B82F6` · College 39.0% `#6366F1` · Coaching 4.9% `#F59E0B` · Group 7.3% `#14B8A6`
- Centre label: "2,050\nTotal" (custom plugin)
- Right of chart: breakdown table (4 rows — type, count, ARR)
- Chart height: 200px

**Chart destroy-and-recreate pattern:**
```html
<script>
  if (window._charts && window._charts['chart-growth']) {
    window._charts['chart-growth'].destroy();
  }
  window._charts = window._charts || {};
  window._charts['chart-growth'] = new Chart(
    document.getElementById('chart-growth'), { /* config */ }
  );
</script>
```

---

### 5.6 Revenue & Billing Mini — Section E

**HTMX:** `id="revenue-mini"` `hx-get="/exec/dashboard/?part=revenue&tab=mtd"` `hx-trigger="load"` `hx-swap="innerHTML"`

**Tab selector:**
```
[MTD ●] [QTD] [YTD]
```
Click: `hx-get="/exec/dashboard/?part=revenue&tab=qtd" hx-target="#revenue-mini" hx-swap="innerHTML"`

**Mini line chart:**
- Chart.js Line, height 180px
- X-axis: last 6 months
- Series: MRR `#6366F1` (fill below, `rgba(99,102,241,0.1)`)
- No legend (space-constrained); chart title hidden
- Tooltip: "March 2026 | MRR: ₹4.98 Cr"

**Quick stats row (below chart):**
```
MRR: ₹4.98 Cr   |   New MRR: ₹24.6 L   |   Churn: −₹8.2 L   |   Net New: ▲₹16.4 L
```
Each stat: 13px value `text-white`, 11px label `text-[#8892A4]`, separated by `|` dividers.

**Overdue alert (conditional):**
```
⚠ ₹92.4 L overdue · 62 institutions
```
Only shown if overdue total > ₹0. Style: `bg-amber-900/30 border-l-4 border-amber-500 text-amber-300 text-sm px-3 py-2 rounded-r mt-3`
Click → navigates to `/exec/billing/?tab=overdue`

**[View Financial Overview →]:** text link to `/exec/financial-overview/`

---

### 5.7 Activity Feed — Section F

**HTMX:** `id="activity-feed"` `hx-get="/exec/dashboard/?part=activity&cat=all"` `hx-trigger="load"` `hx-swap="innerHTML"`

**Filter chips:**
```
[All ●] [Exam] [Billing] [Institution] [System] [Incident]
```
- Container: `flex flex-wrap gap-2 mb-3`
- Active: `bg-[#6366F1] text-white rounded-full px-3 py-1 text-xs font-medium`
- Inactive: `bg-[#131F38] text-[#8892A4] rounded-full px-3 py-1 text-xs hover:text-white`
- Click: `hx-get="/exec/dashboard/?part=activity&cat=exam" hx-target="#activity-feed" hx-swap="innerHTML"` — replaces entire section including chips

**Feed list:** `id="activity-list"` — `<ul>` with `divide-y divide-[#1E2D4A]`

**Each feed item anatomy:**
```
● [icon]  2 min ago                  [Exam] badge
  Exam submitted: JEE Mock Test #42
  ABC Coaching Centre
```
- Left dot: 8px `rounded-full`, colour by category (green=exam, amber=billing, indigo=institution, grey=system, red=incident)
- Icon: 16×16 SVG emoji-style
- Relative time: `text-[#8892A4] text-xs`; absolute timestamp on hover (tooltip)
- Description: `text-white text-sm`
- Institution: `text-[#8892A4] text-xs`
- Category badge: `bg-[#131F38] text-[#8892A4] text-xs px-2 py-0.5 rounded`
- Hover: `bg-[#131F38]` row
- Row height: 52px approx

**Load more:**
```html
<button
  hx-get="/exec/dashboard/?part=activity&cat={{ cat }}&offset={{ offset + 20 }}"
  hx-target="#activity-list"
  hx-swap="beforeend"
  class="text-[#6366F1] text-sm w-full py-2 hover:underline">
  Load 20 more
</button>
```
Uses `hx-swap="beforeend"` — appends to list; does not replace. Offset increments by 20.

**Empty state:** "No activity in this category." — centred, grey, 40px height.

**No more items:** "All caught up — no more events." replacing Load more button.

---

## 6. Drawers

All drawers: right slide-in, `transform translate-x-full → translate-x-0` transition 200ms ease-out. Backdrop: `fixed inset-0 bg-black/40 z-40`. Drawer: `fixed right-0 top-0 h-full z-50 bg-[#0D1526] overflow-y-auto shadow-2xl`. Class `drawer-open` added to `<body>` on open — this pauses all polls.

### 6.1 Preferences Drawer (400 px)

**Open trigger:** [⚙ Prefs] button · Keyboard: `P`
**Close:** [✕] button (top-right of drawer) · `Esc` key · clicking backdrop

**Header:** "Dashboard Preferences" 16px bold · divider `border-b border-[#1E2D4A]`

**Form fields (each field: label 12px `text-[#8892A4]` + control + 4px margin-bottom):**

| # | Label | Control type | Options | Default |
|---|---|---|---|---|
| 1 | Default date range | `<select>` | Today · Yesterday · This Week · This Month · Last 30 Days · Last Quarter | Today |
| 2 | Health refresh interval | `<select>` | 15s · 30s · 60s · Manual | 30s |
| 3 | Exam ops refresh interval | `<select>` | 15s · 30s · 60s · Manual | 30s |
| 4 | Show activity feed | Toggle switch | On / Off | On |
| 5 | Default activity category | Multi-select checkboxes | All · Exam · Billing · Institution · System · Incident | All |
| 6 | KPI card order | Drag-to-reorder `<ul>` (drag handle ⠿) | 6 labelled items | Default order |
| 7 | Compact mode | Toggle switch | Dense rows, reduced padding | Off |

**Unsaved changes indicator:** "● Unsaved changes" in amber, 12px, shown in header when any field is dirty.

**Footer (sticky bottom of drawer):**
```
[Reset to Defaults]    [Save Preferences]
```
- Reset: `bg-transparent border border-[#1E2D4A] text-[#8892A4]` → confirms then re-renders defaults
- Save: `bg-[#6366F1] text-white` → POST `/exec/dashboard/preferences/` → success toast → closes drawer

**Close with unsaved:** Clicking ✕ or backdrop with dirty form → inline confirm strip: "Discard changes? [Yes, discard] [Keep editing]"

---

### 6.2 Service Detail Drawer (480 px)

**Open trigger:** Click any service circle in Platform Health.

**HTMX load:** `hx-get="/exec/dashboard/?part=service-detail&service={{ slug }}"` `hx-target="#drawer-container"` `hx-swap="innerHTML"`

**Header:** "{Service Name}" · status badge (Operational `bg-green-500` / Degraded `bg-yellow-500` / Down `bg-red-600`) · [✕]

**Tab bar (within drawer):**
```
[Overview ●] [Latency] [Incidents] [Dependencies]
```
Tab click: `hx-get="/exec/dashboard/?part=service-tab&service={{ slug }}&tab=latency"` `hx-target="#drawer-tab-content"` `hx-swap="innerHTML"` — only the content area swaps, tabs stay

**Tab: Overview**
- 2×2 metric grid:

| Current Latency | P99 Latency (1h) |
|---|---|
| Error Rate (1h) | Requests / min |

Each metric: 20px number `text-white` + 10px sparkline (60 data points) + 11px label `text-[#8892A4]`

- Uptime toggles: [24h] [7d] [30d] — swaps just the uptime % value via separate `hx-get`
- Last incident: date + severity badge + short title + link to `/exec/incidents/{id}/`

**Tab: Latency**
- Chart.js Line, full drawer width × 200px
- X-axis: time (last 24h, hourly ticks)
- Y-axis: ms (left)
- Series: P50 `#22C55E` · P95 `#F59E0B` · P99 `#EF4444`
- Alert threshold line: `#EF4444` dashed (e.g., 2000ms = SLA breach)
- Tooltip: "14:00 | P50: 142ms | P95: 380ms | P99: 812ms"

**Tab: Incidents**
- Last 5 incidents for this service
- Each: INC# · Date · Duration · Severity badge · Link to `/exec/incidents/{id}/`
- Empty state: "No incidents for this service in the last 90 days. ✅"

**Tab: Dependencies**
- 2-column: "Depends on" (upstream) and "Used by" (downstream)
- Each dependency: service name + status circle
- If any upstream is degraded → amber alert: "Upstream degradation may be the root cause."

**Footer:** [View Full Platform Health →] · [Create Incident] (opens Create Incident modal §7.2)

---

### 6.3 Exam Detail Drawer (640 px)

**Open trigger:** Click exam row in Exam Ops section.

**HTMX load:** `hx-get="/exec/dashboard/?part=exam-detail&id={{ id }}"` `hx-target="#drawer-container"`

**Header:** Exam name (truncated 50 chars, tooltip for full) · Status badge · Institution name small below · [✕]

**Metric pills (horizontal row):**
```
[Enrolled: 4,200]  [Submitted: 620 ▲]  [In Progress: 3,580]  [Issues: 3 🔴]
```
- Pill style: `bg-[#131F38] rounded-full px-3 py-1 text-sm`
- Issues: red if > 0

**Status timeline (horizontal stepper):**
```
Created → Published → [Started ●] → Live → Submission Open → Evaluating → Completed
```
Current step: filled `bg-[#6366F1]` circle · Past steps: `bg-green-500` · Future: `bg-[#1E2D4A]`

**Live section (visible when status = Live, polls every 10s):**
```html
<div hx-get="/exec/dashboard/?part=exam-live&id={{ id }}"
     hx-trigger="every 10s[document.querySelector('.drawer-open')]"
     hx-swap="innerHTML">
```
Contents: submission progress bar + counters (auto-refresh only while drawer is open)

Progress bar: `[████████░░░░░░░░░] 620 / 4,200 (14.8%) submitted`
`<div class="bg-[#6366F1] h-2 rounded" style="width: 14.8%"></div>` within `bg-[#1E2D4A] h-2 rounded`

**Configuration summary (read-only grid):**

| Duration | Total Marks | Sections | Neg. Marking | Shuffle |
|---|---|---|---|---|
| 3h | 300 | 3 | −1/4 | Yes |

**Footer actions (sticky):**
- [+ Extend ▾] → dropdown: +10 min · +15 min · +30 min · Custom → POST `/exec/exams/{id}/extend/` → success toast
- [⏸ Pause] → confirmation modal with reason input → POST `/exec/exams/{id}/pause/`
- [⏹ End Exam] → type "END" to confirm → POST `/exec/exams/{id}/end/`
- [Open Full Detail →] → navigates to `/exec/exams/{id}/`

---

### 6.4 Incident Detail Drawer (600 px)

**Open trigger:** Click incident in activity feed or Platform Health.

**HTMX load:** `hx-get="/exec/dashboard/?part=incident-detail&id={{ id }}"` `hx-target="#drawer-container"`

**Header:** INC-{year}-{num} · Severity badge · Title · [✕]

**Tabs:**
```
[Summary ●] [Timeline] [Impact]
```
Tab content swaps via `hx-get="/exec/dashboard/?part=incident-tab&id={{ id }}&tab=timeline"` `hx-target="#incident-tab-content"` `hx-swap="innerHTML"`

**Tab: Summary**
- Status · Assigned to (avatar + name) · Started (absolute + relative) · Duration live counter
- Services: tag chips
- SLA risk: "Enterprise tier — 14 min to breach" (amber) or "No breach risk" (green)

**Tab: Timeline**
- Last 10 entries. Each: timestamp (HH:MM) · actor · message. Scroll for more.
- [Post Update] inline form (no modal): textarea 100px + [Submit] button → POST `/exec/incidents/{id}/update/`

**Tab: Impact**
- Affected institutions: up to 20 rows (scrollable). Each: name · type badge · students at-time-of-incident
- Summary: "{n} institutions, est. {students} students affected"

**Footer:** [View Full Incident →] → `/exec/incidents/{id}/`

---

## 7. Modals

### 7.1 Keyboard Shortcut Help Modal (560 px, centred)

**Trigger:** `?` key
**Backdrop:** `bg-black/60` · `z-50`
**Close:** Esc · click backdrop · [✕]

Two-column table of shortcuts grouped by section (Navigation / KPI / Sections / Feed / Drawers).

### 7.2 Create Incident Modal (640 px)

**Trigger:** [Create Incident] in Service Detail Drawer footer.

**Fields:**

| Field | Type | Validation |
|---|---|---|
| Title | Text input, 100 chars max | Required |
| Severity | Select: P0 / P1 / P2 / P3 / P4 | Required |
| Services | Multi-select chips (all 6 services listed) | Required ≥ 1 |
| Description | Textarea, 1,000 chars max, monospace | Required |
| Assigned to | Searchable select (ops team) | Defaults to current user |
| Notify institutions | Toggle (default: on for P0/P1, off for P3/P4) | — |

**Footer:** [Cancel] · [Create Incident]
On save: POST `/exec/incidents/` → success toast "INC-{id} created" → closes modal → updates activity feed

---

## 8. States & Edge Cases

| State | Behaviour |
|---|---|
| P0 active | Full-width pulsing red banner below page header: "🔴 P0 ACTIVE — {title} · {time ago} · [View]". Cannot be dismissed. |
| P1 active | Amber banner, same position, less prominent |
| Poll network error | After 3 consecutive failures: inline grey chip "Connection issue — retrying…" replaces poll indicator |
| Session expired | HTMX catches 401 response → JS: `window.location='/login/?next=/exec/dashboard/'` |
| Zero live exams | Exam mini-table shows empty state illustration (not a blank gap) |
| All services green | Platform Health shows "✅ All services operational" row instead of grid |
| Drawer open during poll | `drawer-open` class on `<body>` blocks poll trigger; poll resumes on drawer close |
| Mobile (< 768 px) | Drawers become full-screen (`w-full`); all sections stack vertically; KPI = 2-col |
| Cold load | All section containers show pulse skeletons for 200–800ms until partials resolve |
| JavaScript disabled | Server renders complete page (no HTMX polling) with static snapshot data |
| Compact mode | Table row height 36px; card padding `p-3`; chart heights reduced 20% |
| Overdue > ₹2 Cr | Revenue section amber banner; KPI delta badge on ARR card turns amber |

---

## 9. HTMX Architecture — One URL Per Page

**Page URL:** `/exec/dashboard/`
**All partials served from:** `/exec/dashboard/?part={name}`
**Zero sub-URLs** for this page.

```python
class ExecDashboardView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "portal.view_exec_dashboard"

    def get(self, request):
        ctx = self._build_context(request)
        if _is_htmx(request):
            part = request.GET.get("part", "")
            templates = {
                "kpi":            "exec/partials/dash_kpi.html",
                "health":         "exec/partials/platform_health.html",
                "exams":          "exec/partials/exam_ops.html",
                "business":       "exec/partials/business_overview.html",
                "revenue":        "exec/partials/revenue_billing.html",
                "activity":       "exec/partials/activity_feed.html",
                "service-detail": "exec/partials/dash_service_drawer.html",
                "service-tab":    "exec/partials/dash_service_tab.html",
                "exam-detail":    "exec/partials/dash_exam_drawer.html",
                "exam-live":      "exec/partials/dash_exam_live.html",
                "incident-detail":"exec/partials/dash_incident_drawer.html",
                "incident-tab":   "exec/partials/dash_incident_tab.html",
            }
            if part == "all":
                return render(request, "exec/partials/dash_all.html", ctx)
            if part in templates:
                return render(request, templates[part], ctx)
            return HttpResponseBadRequest("Unknown part")
        return render(request, "exec/dashboard.html", ctx)
```

| `?part=` | Trigger | Poll |
|---|---|---|
| `kpi` | Page load + date range change | No |
| `health` | Page load | Every 30s (pauses on drawer/modal) |
| `exams` | Page load | Every 30s (pauses on drawer/modal) |
| `business` | Page load + tab click | No |
| `revenue` | Page load + tab click | No |
| `activity` | Page load + filter click + "load more" | No |
| `all` | Refresh button | No |
| `service-detail` | Service circle click | No (opens drawer) |
| `exam-detail` | Exam row click | No (opens drawer) |
| `exam-live` | Drawer open (every 10s while open) | Yes, while drawer open |
| `incident-detail` | Feed item click | No (opens drawer) |

---

## 10. API Endpoints

| Method | URL | Key params | Response |
|---|---|---|---|
| GET | `/exec/dashboard/` | `part`, `range`, `tab`, `cat`, `offset`, `service`, `id` | HTML partial or full page |
| POST | `/exec/dashboard/preferences/` | JSON preferences body | `{saved: true}` |
| POST | `/exec/exams/{id}/extend/` | `{minutes: 30}` | `{status: "extended"}` |
| POST | `/exec/exams/{id}/pause/` | `{reason: "..."}` | `{status: "paused"}` |
| POST | `/exec/exams/{id}/end/` | `{confirm: "END"}` | `{status: "ended"}` |
| POST | `/exec/incidents/` | New incident JSON | `{id: "INC-2026-0048"}` |
| POST | `/exec/incidents/{id}/update/` | `{message: "..."}` | Timeline entry HTML |

---

## 11. Performance Requirements

| Metric | Target | Critical |
|---|---|---|
| Full page shell | < 200 ms | > 1 s |
| `?part=kpi` | < 400 ms | > 1 s |
| `?part=health` | < 300 ms | > 800 ms |
| `?part=exams` | < 300 ms | > 800 ms |
| `?part=business` | < 600 ms | > 2 s |
| `?part=revenue` | < 500 ms | > 1.5 s |
| `?part=activity` | < 400 ms | > 1 s |
| Poll response (health/exams) | < 300 ms | > 800 ms (30s poll; must not lag) |
| Service drawer load | < 500 ms | > 1.5 s |
| Exam drawer load | < 400 ms | > 1 s |
| Chart render (browser) | < 200 ms | > 500 ms |

**All aggregates must be Redis-cached (TTL 60s). Background Celery beat refreshes every 60s. No live SQL during peak (6 AM–10 PM IST).**

---

## 12. Keyboard Shortcuts

| Key | Action |
|---|---|
| `R` | Refresh all sections |
| `P` | Open Preferences drawer |
| `Esc` | Close open drawer/modal; removes `drawer-open` class → resumes polls |
| `1` | Business tab → Growth |
| `2` | Business tab → Revenue |
| `3` | Business tab → Institutions |
| `M` | Revenue tab → MTD |
| `Q` | Revenue tab → QTD |
| `Y` | Revenue tab → YTD |
| `↑` / `↓` | Navigate activity feed items |
| `Enter` (feed) | Open relevant drawer for focused feed item |
| `?` | Open keyboard shortcut help modal |

---

## 13. HTMX Template Files

| File | Purpose |
|---|---|
| `exec/dashboard.html` | Page shell: nav, header, section `<div>` containers with `hx-*` attrs |
| `exec/partials/dash_kpi.html` | 6 KPI cards + count-up `<script>` |
| `exec/partials/platform_health.html` | Range toggles + 6 service circles + sparklines + summary |
| `exec/partials/exam_ops.html` | Stats strip + 5-row mini table |
| `exec/partials/business_overview.html` | Tab bar + Chart.js chart + destroy-recreate script |
| `exec/partials/revenue_billing.html` | Tab bar + mini chart + quick stats + overdue alert |
| `exec/partials/activity_feed.html` | Category chips + feed `<ul>` + load-more button |
| `exec/partials/dash_all.html` | Wraps all above for full-refresh swap |
| `exec/partials/dash_service_drawer.html` | Service Detail Drawer HTML |
| `exec/partials/dash_service_tab.html` | Inner tab content for service drawer |
| `exec/partials/dash_exam_drawer.html` | Exam Detail Drawer HTML |
| `exec/partials/dash_exam_live.html` | Live counter sub-partial (polled while drawer open) |
| `exec/partials/dash_incident_drawer.html` | Incident Detail Drawer HTML |
| `exec/partials/dash_incident_tab.html` | Inner tab content for incident drawer |

---

## 14. Component References

| Component | Reusable partial | Used in |
|---|---|---|
| `KpiCard` | `components/kpi_card.html` | §5.2 |
| `ServiceCircle` | `components/service_circle.html` | §5.3 |
| `SparkLine` | `components/sparkline.html` | §5.3, §6.2 |
| `TabBar` | `components/tab_bar.html` | §5.5, §5.6, §6.2, §6.3, §6.4 |
| `ChartLine` | `components/chart_line.html` | §5.5 Growth, §5.6 Revenue |
| `ChartBar` | `components/chart_bar.html` | §5.5 Revenue tab |
| `ChartDoughnut` | `components/chart_donut.html` | §5.5 Institutions tab |
| `ActivityFeedItem` | `components/feed_item.html` | §5.7 |
| `DrawerPanel` | `components/drawer.html` | §6.1–6.4 |
| `ModalDialog` | `components/modal.html` | §7.1, §7.2 |
| `ProgressBar` | `components/progress_bar.html` | §6.3 submission bar |
| `StatusBadge` | `components/status_badge.html` | Drawers, feed items |
| `LoadingSkeleton` | `components/skeleton.html` | All sections on cold load |
| `AlertBanner` | `components/alert_banner.html` | P0/P1 incident banner |
| `StepperTimeline` | `components/stepper.html` | §6.3 exam status timeline |
