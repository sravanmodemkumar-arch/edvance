# 32 — Exam Day War Room

---

## 1. Page Metadata

| Field | Value |
|---|---|
| Page title | Exam Day War Room |
| Route | `/exec/war-room/` |
| Django view | `WarRoomView` |
| Template | `exec/war_room.html` |
| Priority | **P0** |
| Nav group | Hidden from main nav — accessed via banner trigger or direct URL |
| Required roles | `exec` · `superadmin` · `ops_manager` · `incident_manager` |
| CFO access | Denied (Level 1 read-only role has no operational purpose here) |
| HTMX poll — command strip | Every 5s (pauses when any modal is open) |
| HTMX poll — institution grid | Every 10s |
| HTMX poll — throughput chart | Every 5s |
| Cache | All metrics: Redis TTL 4s (tighter than all other pages — this is a war room) |
| Theme tokens | bg-base `#040810` · surface-1 `#08101E` · surface-2 `#0D1828` · accent `#6366F1` · danger `#EF4444` · warn `#F59E0B` |
| Auto-activation trigger | When platform-wide concurrent exam users > 10,000, all exec pages show banner: "🔴 PEAK ACTIVE — [Enter War Room]" |

---

## 2. Purpose & Business Logic

The War Room exists for one reason: **74,000 students submit answers simultaneously, and a 3-minute failure at peak = 3,700 students disrupted per minute.**

The existing Platform Health page (02) is designed for post-incident analysis and daily monitoring. It answers "what is the health of our services over the last 24 hours?" The War Room answers a completely different question: **"Are we safe right now, at this exact second, and what do I press if we are not?"**

During a peak exam day, the CTO and COO currently must tab between 4 interfaces simultaneously:
1. Platform Health (service uptime)
2. Exam Operations (student counts)
3. Incident Manager (active incidents)
4. AWS Console (Lambda concurrency, RDS)

This multi-tab context-switching is how cascade failures are caught 8 minutes too late. The War Room collapses all of this into one command-and-control surface with no nav, no sidebar, no distractions, and one-click escalation paths.

**What decisions this page enables:**
- Is Lambda concurrency approaching the ceiling? → Approve emergency scale-out now, not after throttling starts
- Which institution's exam is failing? → Dispatch support team directly from this page
- Is Redis eviction rate rising? → Proactively flip to direct-DB mode before cache stampede
- Is OTP delivery failing? → Pause new exam logins while Exotel ticket is raised
- Is one coaching centre getting 80% of all errors? → Pause that institution's exam only (surgical, not platform-wide)

---

## 3. User Roles & Access

| Role | Can View | Can Act | Specific Restrictions |
|---|---|---|---|
| CEO / Platform Owner | All sections | Emergency pause (any exam), escalate | Cannot modify infra settings |
| CTO | All sections | All actions including "Emergency Lambda Scale" | Full action access |
| COO | All sections | Pause exam, escalate, dispatch support | Cannot trigger Lambda scale (infra-gated) |
| Platform Admin | All sections | All actions | Full access |
| Ops Manager / Incident Manager | All sections except cost gauges | Pause exam, escalate | Cannot approve infra scale |
| CFO | No access | No access | Redirect to `/exec/dashboard/` with toast "War Room access is restricted to Operations roles." |

**Role-based UI differences:**
- CTO only: "Emergency Lambda Scale" button is enabled (green). For all other roles it renders but is disabled with tooltip "CTO access required."
- COO / Ops: "Pause All Exams" button requires a confirm modal with reason field. CTO can skip confirm with Shift+click (power-user shortcut, documented in keyboard help).

---

## 4. Section-wise UI Breakdown

---

### Section 1 — Page Shell (No Nav Mode)

**Purpose:** The War Room must fill the entire viewport. Navigation, sidebar, breadcrumbs, and footer are all hidden. The user must feel like they are in a cockpit, not a dashboard. Every pixel is operational.

**User interaction:** The user arrives via the banner link on any exec page, or navigates directly to `/exec/war-room/`. On arrival, the page is already polling; no manual refresh needed.

**UI elements:**
- `<body>` class: `war-room-mode` — CSS removes sidebar (`#sidebar { display: none }`), removes topbar (`#topbar { display: none }`), sets `body { overflow: hidden }` (prevent accidental scroll away from critical data)
- Full-viewport grid: `grid grid-rows-[auto_1fr_1fr] h-screen w-screen`
- Status bar (top): 32px fixed strip — platform name left, current IST time (live, updated every second via JS), "WAR ROOM ACTIVE" badge right, "Exit War Room" button far right
- Keyboard shortcut `Q` or `Escape` → "Exit War Room?" confirm dialog (not immediate — never accidentally exit the war room mid-peak)

**Data flow:** `WarRoomView.get()` → render `exec/war_room.html` (page shell only, no data in initial render — all data via HTMX partials)

**Role-based behavior:** All permitted roles see identical shell. CFO is redirected before reaching this view.

**Edge cases:**
- If user presses browser back: shell handles `popstate` event and shows "Are you sure you want to leave the War Room?" dialog
- Mobile (<768px): War Room renders a simplified read-only status view with a banner "Full War Room requires desktop. Showing status summary." — no action buttons on mobile

**Performance:** Shell HTML < 8KB. All data partials loaded async via HTMX. Shell must render in < 100ms.

**Accessibility:** "WAR ROOM ACTIVE" badge has `role="alert" aria-live="assertive"` so screen readers announce it on page load. All action buttons have explicit `aria-label` attributes.

---

### Section 2 — Command Strip (Top Row)

**Purpose:** The single most important row on the page. Shows the 6 metrics that determine whether the platform is healthy at this exact moment. If any metric is in the red zone, it is immediately obvious. No charts, no trends — just the number and a colour.

**User interaction:**
- Each metric card is clickable → opens a detail drawer for that metric (except throughput, which scrolls to the chart below)
- Cards auto-update every 5 seconds via HTMX polling (partial swap)
- When any card enters red zone: the card border pulses (`animate-pulse ring-2 ring-red-500`) and an audio ping plays (user-configurable: Settings → War Room → Alert Sound: On/Off)

**UI elements — 6 metric cards in a flex row:**

```
╔═══════════════╦═══════════════╦═══════════════╦═══════════════╦═══════════════╦═══════════════╗
║ LAMBDA CONC.  ║ SUBMISSIONS/s ║ RDS POOL      ║ REDIS HIT %   ║ ERROR RATE    ║ OTP SUCCESS % ║
║               ║               ║               ║               ║               ║               ║
║  3,842/5,000  ║     1,240     ║   412/500     ║    97.4%      ║    0.18%      ║    99.2%      ║
║               ║               ║               ║               ║               ║               ║
║  ████████░░   ║  ▲ from 1,100 ║  ████████░    ║  ● Healthy    ║  ● Healthy    ║  ● Healthy    ║
║  76.8%  WARN  ║               ║  82.4%  WARN  ║               ║               ║               ║
╚═══════════════╩═══════════════╩═══════════════╩═══════════════╩═══════════════╩═══════════════╝
```

**Card anatomy:**
- Label: 10px, uppercase, letter-spacing: widest, `text-[#8892A4]`
- Primary value: 28px bold `text-white`
- Progress bar (where applicable): `h-2 rounded` within `bg-[#1E2D4A]` — fill colour changes with zone
- Zone badge: 11px pill — green=OK / amber=WARN / red=CRIT

**Zone thresholds:**

| Metric | Green | Amber | Red | Action if Red |
|---|---|---|---|---|
| Lambda Concurrency | < 60% of limit | 60–85% | > 85% | CTO: "Emergency Lambda Scale" |
| Submissions/sec | Any positive | < 50% of expected for this exam | 0 for > 30s | Investigate + potential exam pause |
| RDS Connection Pool | < 60% | 60–85% | > 85% | DevOps: read replica promotion |
| Redis Hit % | > 95% | 90–95% | < 90% | Alert: cache stampede risk; check Celery beat |
| Error Rate (all endpoints) | < 0.5% | 0.5–2% | > 2% | Auto-creates P1 incident draft |
| OTP Success % | > 98% | 95–98% | < 95% | Exotel/Kaleyra gateway check |

**Data flow:**
- HTMX: `id="command-strip"` `hx-get="/exec/war-room/?part=command"` `hx-trigger="load, every 5s[!document.querySelector('.modal-open')]"` `hx-swap="innerHTML"`
- Backend: reads from Redis keys (pre-computed by Celery beat every 4s):
  - `war:lambda_concurrency` — pulled from CloudWatch Lambda ConcurrentExecutions metric via boto3
  - `war:submissions_per_sec` — rolling 10s average of exam submission events from EventBridge
  - `war:rds_connections` — RDS DescribeDBInstances via boto3
  - `war:redis_hit_ratio` — ElastiCache INFO stats
  - `war:error_rate` — aggregated from API Gateway error logs
  - `war:otp_success_rate` — Exotel webhook delivery confirmation counts

**Role-based behavior:** All permitted roles see all 6 cards. No role-based hiding here — the command strip is universal truth.

**Edge cases:**
- If Redis key is stale (> 10s old): card shows grey background + "Data stale — retrying" in place of value. Never show a cached stale number as if it were fresh.
- If boto3 CloudWatch call fails: Lambda card shows "AWS API error" with retry timestamp. Does not block other cards.
- If Celery beat job missed its 4s window (high load): data source lag indicator appears below card: "12s old" in amber.

**Performance:** Command strip partial < 4KB. Redis reads only — zero DB queries. Target < 80ms round-trip including network.

**Mobile:** On mobile, command strip becomes a 2×3 grid (2 columns, 3 rows). Cards are smaller (60px height vs 88px). Progress bars hidden. Values and zone badges remain.

**Accessibility:** Each card has `role="status" aria-label="Lambda Concurrency: 76.8%, Warning zone"`. Zone changes trigger `aria-live="polite"` updates.

---

### Section 3 — Submission Throughput Chart

**Purpose:** The one chart that matters during a live exam. It answers: "Is the platform absorbing submissions at the rate students are submitting them, or is something backing up?" A healthy exam shows a submission curve that rises as students finish, then plateaus, then drops. Any sudden drop or flatline = problem.

**User interaction:**
- Chart auto-scrolls (newest data on the right, x-axis is last 10 minutes, sliding window)
- Hover on any data point → tooltip showing exact value + timestamp
- Click any anomaly point (if error rate spike) → opens Incident Draft modal pre-filled with timestamp and current error data

**UI elements:**
- Chart.js Line chart, `id="chart-throughput"`, full width, 180px tall
- X-axis: last 10 minutes, ticks every 1 minute, label format HH:MM
- Y-axis (left): submissions/second (integer)
- Y-axis (right, secondary): error count/second (small bars, `rgba(239,68,68,0.5)` red fill)
- Series 1: Submission throughput — `#6366F1` line, 2px stroke, no fill
- Series 2: Error count — red bar series on secondary axis
- Baseline reference line: expected submissions/sec for the current exams (calculated from enrolled student count ÷ expected exam duration in seconds) — dashed grey line `rgba(255,255,255,0.2)`
- "Zero throughput" alert line: if series 1 = 0 for > 30s, a red dashed horizontal line at y=0 pulses

**HTMX update:** The chart data is NOT swapped via HTMX innerHTML (that would destroy the Chart.js instance). Instead:
```html
<div hx-get="/exec/war-room/?part=throughput-data"
     hx-trigger="every 5s"
     hx-swap="none"
     hx-on::after-request="updateThroughputChart(event.detail.xhr.responseText)">
</div>
```
`updateThroughputChart()` parses the JSON response and calls `chart.data.datasets[0].data.push(newPoint)` + `chart.data.datasets[0].data.shift()` (sliding window, always 120 points = 10 min × 12 ticks/min).

**Data flow:** Backend serves `/exec/war-room/?part=throughput-data` → returns JSON (not HTML): `{"ts": "14:32:05", "submissions_per_sec": 1240, "errors_per_sec": 2}` from Redis time-series key `war:throughput_ts` (sorted set, keyed by epoch, last 600s).

**Role-based behavior:** All permitted roles see chart. No differences.

**Edge cases:**
- Chart renders immediately with last 10 minutes of historical data on page load (not blank on arrival)
- If Redis time-series has gaps (Celery miss): gap rendered as Chart.js `null` point (breaks line — visually shows the gap, not a false zero)
- Chart container shows "Live" badge (green pulsing dot + "LIVE") in top-right corner

**Performance:** 120 data points × 2 series = trivial render. JSON payload < 200 bytes per poll. Chart update via push/shift is O(1), no full re-render.

**Mobile:** Chart height reduces to 100px. Secondary Y-axis (error bars) hidden on mobile.

**Accessibility:** Chart container has `role="img" aria-label="Live submission throughput chart — last 10 minutes"`. Tooltip values are also written to a visually-hidden `<div aria-live="polite">` on hover.

---

### Section 4 — Live Institution Grid

**Purpose:** The granular view. Which of the 2,050 institutions are currently running exams? For each one, are they healthy or failing? This is where the COO identifies surgical problems: "ABC Coaching is failing but XYZ School is fine — this is institution-specific, not platform-wide."

**User interaction:**
- Grid auto-updates every 10s
- Each row is clickable → opens Institution War Room Drawer (drawer-F, 480px) with per-institution metrics
- Rows sorted by: (1) Error state first, (2) Student count descending within each state
- Search input (real-time, client-side filter) — filters the rendered grid without API call
- Filter chips: [All] [Live] [Issues] [Queued] [Ended] — swaps the partial
- "Pause Exam" action button on each row (COO/CTO/Admin only) — opens pause confirmation modal
- Keyboard: Arrow keys navigate rows, Enter opens drawer, P triggers pause for focused row

**UI elements:**
- Table: `id="institution-grid"` — `<table>` with sticky header
- Columns:

| Column | Width | Type | Notes |
|---|---|---|---|
| Status | 60px | Coloured dot + label | Live (green pulse) · Issues (red pulse) · Queued (blue) · Ended (grey) |
| Institution | 200px | Name + type badge (School/College/Coaching/Group) | Truncated at 24 chars, full name in tooltip |
| Exam | 160px | Exam name | Truncated at 20 chars |
| Enrolled | 80px | Integer | Right-aligned |
| Submitted | 80px | Integer + progress bar | "620 (14.8%)" — bar width = submitted/enrolled |
| Errors (5m) | 80px | Integer | Red if > 0, pulsing if > 10 |
| Latency (P95) | 80px | ms | Amber if > 800ms, red if > 2000ms |
| Actions | 100px | Buttons | [👁 View] [⏸ Pause] |

- Rows with status="Issues": `bg-red-900/20 border-l-4 border-red-500`
- Rows with status="Live": normal `bg-[#08101E]` hover `bg-[#0D1828]`
- Max rows rendered: 50 (top 50 by error count + student count). "Showing top 50 active institutions. 12 more ended." at bottom.

**Data flow:**
- HTMX: `id="institution-grid-body"` `hx-get="/exec/war-room/?part=institutions&status=live"` `hx-trigger="load, every 10s[!document.querySelector('.modal-open,.drawer-open')]"` `hx-swap="innerHTML"`
- Backend: reads from `war:institutions` Redis hash (all 2,050 institutions, but filtered to those with `status IN ['live','issues','queued']`). Redis hash updated by Celery beat every 8s.
- Filter chips: `hx-get="/exec/war-room/?part=institutions&status=issues"` → swaps only `#institution-grid-body`

**Role-based behavior:**
- All roles see all columns
- "Pause" button: disabled for CEO (read + escalate only), enabled for CTO/COO/Ops/Admin
- CEO sees "Pause" button rendered but greyed out with tooltip "Pause actions are for Ops team"

**Edge cases:**
- If 0 institutions are live: grid shows empty state — "No exams are currently active. War Room will auto-refresh." with a status indicator.
- If institution data is stale: row shows "⚠ Stale data" in the latency cell
- If an institution transitions from Live → Issues during a poll cycle: the row animate-slides to the top of the table (CSS transition) and the status dot changes from green → red with a pulse

**Performance:**
- Celery beat writes to Redis hash every 8s — never a live DB query during a peak exam
- Backend reads Redis → builds HTML partial → returns in < 100ms target
- Client-side search filters the DOM (no API call) using JS `filterRows()` on the already-rendered table
- 50 rows × 9 columns = manageable DOM; no virtualisation needed

**Mobile:** Table collapses to 4 columns (Status, Institution, Submitted, Errors). Full table accessible via horizontal scroll. Drawer-F opens as full-screen on mobile.

**Accessibility:** Table has `role="grid"`, each row `role="row"`, each cell `role="gridcell"`. Status dot has `aria-label="Status: Issues"`. Sort column header has `aria-sort="descending"`.

---

### Section 5 — Infrastructure Gauges Panel

**Purpose:** The CTO's primary focus area. While the COO watches institution-level data, the CTO watches infra capacity. These gauges are the "fuel gauges" of the platform — they show how much headroom remains before a hard ceiling is hit.

**User interaction:**
- Gauges are read-only (no interaction except hover)
- Hover on any gauge → tooltip explaining what this metric means and what the threshold values represent
- Each gauge has a "History" link → navigates to `/exec/infrastructure/?metric=lambda_concurrency` (page 37)
- "Emergency Lambda Scale" button (CTO only) below Lambda gauge

**UI elements — 4 gauges in a 2×2 grid:**

```
╔══════════════════════════╦══════════════════════════╗
║  LAMBDA CONCURRENCY      ║  RDS CONNECTION POOL     ║
║                          ║                          ║
║      ╭────────╮          ║      ╭────────╮          ║
║    ╭─┤  76.8% ├─╮        ║    ╭─┤  82.4% ├─╮        ║
║    │  ████████  │        ║    │  ████████  │        ║
║    ╰────────────╯        ║    ╰────────────╯        ║
║   3,842 / 5,000          ║    412 / 500              ║
║   [Emergency Scale ▾]    ║   [Notify DevOps]        ║
╠══════════════════════════╬══════════════════════════╣
║  REDIS HIT RATIO         ║  CDN OFFLOAD %            ║
║                          ║                          ║
║      ╭────────╮          ║      ╭────────╮          ║
║    ╭─┤  97.4% ├─╮        ║    ╭─┤  94.2% ├─╮        ║
║    │  ██████░░  │        ║    │  ██████░░  │        ║
║    ╰────────────╯        ║    ╰────────────╯        ║
║   Healthy                ║   Healthy                ║
╚══════════════════════════╩══════════════════════════╝
```

**Gauge implementation:**
- SVG arc gauge (not Chart.js — SVG is lighter, no library needed for a single number)
- Arc: `stroke-dasharray` animated from 0 → current value on load
- Fill colour: green < 60%, amber 60–85%, red > 85%
- Centre label: percentage (24px bold) + absolute numbers (11px grey below)

**"Emergency Lambda Scale" button (CTO only):**
```
[⚡ Emergency Lambda Scale ▾]
```
Dropdown on click:
- "+500 concurrency (safe — within account limit)"
- "+1,000 concurrency (aggressive — requires DevOps confirmation)"
- "Custom..." → number input modal

On select:
1. Confirmation modal: "You are about to increase Lambda concurrency by 500. Estimated AWS cost impact: +₹2,400/hour. This change takes 2–3 minutes to propagate."
2. CTO confirms → POST `/exec/war-room/actions/scale-lambda/` → triggers boto3 `put_function_concurrency()` → audit log entry → success toast "Lambda concurrency limit updated to 5,500 · Propagation ~2 min"
3. Gauge begins polling at 5s and will show the new ceiling once propagation completes

**"Notify DevOps" button (any permitted role):**
- Sends a PagerDuty / Slack alert to the DevOps on-call channel with the current RDS pool %
- Disabled if RDS is in green zone (tooltip: "Alert not needed — pool is healthy")

**Data flow:** HTMX partial `id="infra-gauges"` `hx-get="/exec/war-room/?part=gauges"` `hx-trigger="load, every 5s"` `hx-swap="innerHTML"`. All 4 metrics from Redis (same keys as command strip but rendered as gauges here).

**Role-based behavior:**
- "Emergency Lambda Scale": CTO only — enabled. All other roles — button renders but disabled with "CTO access required" tooltip
- "Notify DevOps": COO/CTO/Ops — enabled. CEO — enabled. CFO — N/A (no access)

**Edge cases:**
- If Lambda concurrency data is unavailable (boto3 failure): gauge shows "AWS API unreachable" — grey arc, no percentage. "Last known: 3,842 (18 min ago)" shown in small text.
- If any gauge hits 100%: full red background on that gauge card, pulsing border, auto-triggers a P0 incident draft

**Performance:** 4 SVG gauges, no library, inline SVG = < 5KB per render. 5s poll.

**Mobile:** 2×2 gauge grid becomes 1×4 stack. Gauge diameter reduces from 80px to 60px.

**Accessibility:** Each gauge has `role="meter" aria-valuenow="76" aria-valuemin="0" aria-valuemax="100" aria-label="Lambda Concurrency: 76.8%"`.

---

### Section 6 — Active Incidents & Escalation Panel

**Purpose:** During a peak exam, incidents may be happening simultaneously. This panel shows the current incident queue and provides the fastest possible path to escalation and action — without leaving the War Room.

**User interaction:**
- Each incident row shows severity, title, duration, and affected institution count
- [Create Incident] button → opens Create Incident modal (identical to div-a-01's §7.2 but pre-fills "Exam Day" tag and current peak metrics)
- [Escalate] on each row → sends PagerDuty alert + Slack message to on-call engineer + updates incident status to "Escalated"
- [Resolve] on each row → marks resolved → row fades and moves to "Resolved (this session)" collapsed section
- Keyboard shortcut `I` → focuses the Create Incident button

**UI elements:**
```
ACTIVE INCIDENTS                                     [+ Create Incident]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔴 P1  Exam Engine latency spike         14 min · 3 institutions  [Escalate] [Resolve]
🟡 P2  OTP delivery delays (Exotel)       7 min · 12 institutions  [Escalate] [Resolve]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
▸ Resolved this session (2)
```

- Incident row: `flex items-center gap-3 py-3 border-b border-[#1E2D4A]`
- Severity dot: 10px circle — `bg-red-500` (P0/P1) · `bg-amber-500` (P2) · `bg-blue-400` (P3)
- Duration: live counter updated every second via JS `setInterval`, `text-[#8892A4]`
- [Escalate] button: `bg-amber-600 hover:bg-amber-500 text-white text-xs px-2 py-1 rounded`
- [Resolve] button: `bg-transparent border border-[#1E2D4A] text-[#8892A4] text-xs px-2 py-1 rounded`

**Data flow:** HTMX: `id="incident-panel"` `hx-get="/exec/war-room/?part=incidents"` `hx-trigger="load, every 10s"` `hx-swap="innerHTML"`. Backend reads from `Incident` model filtered `status__in=['open','escalated']`, ordered by severity ASC then created_at DESC.

**Role-based behavior:**
- [Create Incident]: all permitted roles
- [Escalate]: COO/CTO/Ops/Admin — enabled. CEO — enabled (CEO can always escalate).
- [Resolve]: CTO/Ops/Admin — enabled. COO — enabled with confirm. CEO — disabled (tooltip: "Resolution is for Ops team — use Escalate to notify them")

**Edge cases:**
- 0 active incidents: panel shows "✅ No active incidents" — green text, 40px height, no empty illustration (space is precious in the War Room)
- > 10 active incidents (mass failure scenario): panel shows first 5, "8 more incidents — [View All →]" links to `/exec/incidents/` in new tab

**Performance:** Incidents rarely exceed 10 rows — light query, no pagination needed here.

**Mobile:** Each incident row shows severity + title + [Escalate] only. Duration and institution count hidden. [Resolve] moved into a swipe action (right-swipe on mobile).

**Accessibility:** Incident list has `role="list"`. P0/P1 incidents trigger `aria-live="assertive"` announcement when they appear. P2/P3 use `aria-live="polite"`.

---

### Section 7 — Emergency Actions Bar (Bottom Strip)

**Purpose:** The nuclear options. These are platform-wide actions that should be pressed in a real emergency. They must be highly visible, clearly labelled, and protected by confirmation to prevent accidental activation — but fast enough that a stressed operator can execute them in < 15 seconds.

**User interaction:**
- All buttons require a confirm modal before execution
- P0/P1 severity actions (Pause All, Kill Switch) additionally require the operator to type a confirmation phrase (e.g., "PAUSE ALL EXAMS") to prevent panic-clicking
- Each action logs to audit log with actor, timestamp, and reason
- Keyboard shortcut `Shift+P` → focuses "Pause All Exams" button (shortcut shown on button as tooltip)

**UI elements:**
```
╔══════════════════════════════════════════════════════════════════════════════╗
║  [⏸ Pause All Live Exams]  [🔔 Broadcast Alert]  [⚡ Emergency Lambda Scale] ║
║  [📞 Page On-Call DevOps]  [📋 Create P0 Incident]  [🚪 Exit War Room]       ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

**Button specifications:**

| Button | Colour | Role restriction | Confirm type | Action |
|---|---|---|---|---|
| Pause All Live Exams | `bg-red-600 hover:bg-red-500` | COO/CTO/Admin | Type "PAUSE ALL EXAMS" | POST `/exec/war-room/actions/pause-all/` → sets all `status=live` exams to `status=paused` · broadcasts institution admins via WhatsApp/SMS · creates P0 incident |
| Broadcast Alert | `bg-amber-600 hover:bg-amber-500` | COO/CTO/Admin | Confirm modal + message textarea | POST `/exec/war-room/actions/broadcast/` → sends WhatsApp/SMS to all institution admins of currently-live exams |
| Emergency Lambda Scale | `bg-indigo-600 hover:bg-indigo-500` (CTO only — grey for others) | CTO only | Confirm with cost estimate | boto3 `put_function_concurrency()` |
| Page On-Call DevOps | `bg-[#131F38] border border-[#1E2D4A]` | All | Single confirm | POST `/exec/war-room/actions/page-devops/` → PagerDuty API → Slack #oncall-devops |
| Create P0 Incident | `bg-[#131F38] border border-[#1E2D4A]` | All | Modal with pre-filled P0 form | Same as Create Incident modal but severity locked to P0 |
| Exit War Room | `bg-transparent text-[#8892A4]` | All | "Exit during active peak?" confirm | Navigate to `/exec/dashboard/` |

**Data flow for Pause All:**
```python
# POST /exec/war-room/actions/pause-all/
def pause_all_exams(request):
    reason = request.POST.get("reason", "")
    confirm_phrase = request.POST.get("confirm_phrase", "")
    if confirm_phrase != "PAUSE ALL EXAMS":
        return JsonResponse({"error": "Confirmation phrase mismatch"}, status=400)

    live_exams = Exam.objects.filter(status="live").select_related("institution")
    paused_count = live_exams.update(
        status="paused",
        paused_at=now(),
        paused_by=request.user,
        pause_reason=reason
    )

    # Queue notification task
    notify_institutions_exam_paused.delay(
        exam_ids=list(live_exams.values_list("id", flat=True)),
        reason=reason,
        actor_id=request.user.id
    )

    # Audit log
    AuditLog.objects.create(
        actor=request.user,
        action="PAUSE_ALL_EXAMS",
        detail=f"Paused {paused_count} live exams. Reason: {reason}",
        ip=get_client_ip(request),
    )

    # Create P0 incident
    incident = Incident.objects.create(
        title=f"Emergency: All exams paused — {reason}",
        severity="P0",
        created_by=request.user,
        status="open",
    )

    return JsonResponse({
        "paused_count": paused_count,
        "incident_id": incident.id,
        "message": f"{paused_count} exams paused. Incident INC-{incident.id} created."
    })
```

**Role-based behavior:**
- "Pause All Exams": disabled for CEO with tooltip "Contact COO/CTO to pause exams." CEO may broadcast alerts and page DevOps.
- "Emergency Lambda Scale": disabled for all except CTO.

**Edge cases:**
- If 0 live exams: "Pause All" button disabled with tooltip "No live exams to pause."
- If broadcast fails (Exotel/WhatsApp gateway down): action still executes (exams paused), but shows warning toast: "Exams paused, but institution notification failed — notify manually."
- If Lambda scale API call fails: shows error modal with AWS error detail + manual fallback instructions link

**Performance:** POST actions are not performance-critical (rare execution). All actions complete asynchronously; the UI shows a spinner and receives a webhook-style completion update.

**Mobile:** Emergency Actions Bar stacks vertically. Only 3 buttons visible: "Pause All", "Page DevOps", "Create P0 Incident". Others are behind a "More Actions ▾" button.

**Accessibility:** All action buttons have `aria-label` with full action description. Confirm modals trap focus within the modal container. Destructive actions have `aria-describedby` pointing to a warning text element explaining the consequences.

---

## 5. Full Page Wireframe

```
╔══════════════════════════════════════════════════════════════════════════════╗
║  ⚔ EduForge WAR ROOM                        14:32:07 IST  🔴 PEAK ACTIVE  [✕]║
╠══════════╦═══════════╦══════════╦══════════╦══════════╦═══════════════════════╣
║ LAMBDA   ║ SUBM/sec  ║ RDS POOL ║ REDIS    ║ ERR RATE ║ OTP SUCCESS           ║
║ 3842/5K  ║   1,240   ║  412/500 ║  97.4%   ║  0.18%   ║  99.2%               ║
║ ████░░   ║  ▲ from   ║  █████░  ║  ● OK    ║  ● OK    ║  ● OK                ║
║ 76.8%⚠  ║  1,100    ║  82.4%⚠ ║          ║          ║                       ║
╠══════════╩═══════════╩══════════╩══════════╩══════════╩═══════════════════════╣
║  SUBMISSION THROUGHPUT (last 10 min)                          ● LIVE           ║
║  ┌──────────────────────────────────────────────────────────────────────────┐  ║
║  │       /\/\/\/\____/\/\/\/\/\/\/\______/\/\/\/\/\/\/\/\/\/\              │  ║
║  └──────────────────────────────────────────────────────────────────────────┘  ║
╠══════════════════════════════════════╦═════════════════════════════════════════╣
║  LIVE INSTITUTION GRID               ║  INFRA GAUGES           INCIDENTS       ║
║  [All] [Live●] [Issues] [Queued]     ║                                         ║
║  [Search institutions...          ]  ║  ╭──╮   ╭──╮   🔴 P1 Latency  14m [!] ║
║  ● LIVE  ABC Coaching  JEE Prep      ║  76% 82% ╭──╮   🟡 P2 OTP      7m [!] ║
║          4,200 enr  620 sub  0 err   ║  Lambda RDS╭──╮  ─────────────────────  ║
║  ● LIVE  XYZ School  Math T          ║            97% 94%  ✅ No P0/P1 breach  ║
║          280 enr   142 sub  0 err   ║            Redis CDN                    ║
║  🔴 ISSUE DEF Coaching  SSC          ║                         [+ P0 Incident] ║
║          8,100 enr  200 sub  48 err  ║  [⚡ Emergency Scale]   [Escalate All]  ║
║  ● LIVE  ...                         ║                                         ║
║                                      ║                                         ║
╠══════════════════════════════════════╩═════════════════════════════════════════╣
║ [⏸ PAUSE ALL EXAMS] [🔔 BROADCAST ALERT] [⚡ LAMBDA SCALE] [📞 PAGE DEVOPS]   ║
║ [📋 CREATE P0 INCIDENT]                                    [🚪 EXIT WAR ROOM]  ║
╚══════════════════════════════════════════════════════════════════════════════════╝
```

---

## 6. Component Architecture

| Component | File | Props | Used in |
|---|---|---|---|
| `CommandMetricCard` | `components/war_room/metric_card.html` | `label, value, unit, pct, zone (ok/warn/crit), stale_seconds` | Section 2 |
| `ThroughputChart` | `components/war_room/throughput_chart.html` | `initial_data (120 points)` | Section 3 |
| `InstitutionGridRow` | `components/war_room/institution_row.html` | `institution, exam, enrolled, submitted, error_count, latency_p95, status` | Section 4 |
| `InfraGauge` | `components/war_room/gauge.html` | `label, current, max, zone, history_url` | Section 5 |
| `IncidentRow` | `components/war_room/incident_row.html` | `incident_id, severity, title, duration_seconds, institution_count, can_resolve, can_escalate` | Section 6 |
| `EmergencyActionButton` | `components/war_room/action_button.html` | `label, icon, colour, confirm_type (phrase/modal/single), role_required, disabled, tooltip` | Section 7 |
| `WarRoomDrawer` | `components/war_room/drawer.html` | `institution_id` — loaded via HTMX on row click | Drawer-F |
| `PauseConfirmModal` | `components/war_room/pause_confirm_modal.html` | `action_label, phrase_required, cost_note` | Section 7 |

---

## 7. HTMX Architecture

**One page URL: `/exec/war-room/`**
**All partials: `/exec/war-room/?part={name}`**

| `?part=` | Target | Trigger | Poll | Swap |
|---|---|---|---|---|
| `command` | `#command-strip` | load | Every 5s (pauses on modal) | innerHTML |
| `throughput-data` | None (JS-handled) | Every 5s | JSON, processed by JS | none |
| `institutions` | `#institution-grid-body` | load + filter chip click | Every 10s (pauses on drawer/modal) | innerHTML |
| `gauges` | `#infra-gauges` | load | Every 5s | innerHTML |
| `incidents` | `#incident-panel` | load | Every 10s | innerHTML |
| `institution-drawer` | `#drawer-container` | Row click | No | innerHTML |

**Poll-pause logic** (identical to div-a-01 but tighter):
```javascript
// War Room specific: also pause when confirmation modal is open
const warRoomPollPause = `!document.querySelector(
  '.modal-open,.drawer-open,.confirm-open'
)`;
```

---

## 8. Backend View & API

```python
class WarRoomView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "portal.view_war_room"

    def get(self, request):
        # CFO redirect
        if request.user.has_role("cfO") and not request.user.is_superuser:
            messages.warning(request, "War Room access is restricted to Operations roles.")
            return redirect("exec:dashboard")

        if _is_htmx(request):
            part = request.GET.get("part", "")
            templates = {
                "command":           "exec/war_room/partials/command_strip.html",
                "throughput-data":   None,  # returns JSON
                "institutions":      "exec/war_room/partials/institution_grid.html",
                "gauges":            "exec/war_room/partials/infra_gauges.html",
                "incidents":         "exec/war_room/partials/incident_panel.html",
                "institution-drawer":"exec/war_room/partials/institution_drawer.html",
            }
            ctx = self._build_war_room_context(request, part)

            if part == "throughput-data":
                return JsonResponse(self._get_throughput_point())

            if part in templates:
                return render(request, templates[part], ctx)

            return HttpResponseBadRequest("Unknown part")

        # Full page: render shell + initial data embedded for cold-load speed
        ctx = self._build_war_room_context(request, "all")
        return render(request, "exec/war_room.html", ctx)

    def _build_war_room_context(self, request, part):
        r = get_redis_connection()
        return {
            "lambda_conc":      self._read_metric(r, "war:lambda_concurrency"),
            "lambda_limit":     self._read_metric(r, "war:lambda_limit"),
            "submissions_ps":   self._read_metric(r, "war:submissions_per_sec"),
            "rds_current":      self._read_metric(r, "war:rds_connections_current"),
            "rds_max":          self._read_metric(r, "war:rds_connections_max"),
            "redis_hit_ratio":  self._read_metric(r, "war:redis_hit_ratio"),
            "error_rate":       self._read_metric(r, "war:error_rate"),
            "otp_success_rate": self._read_metric(r, "war:otp_success_rate"),
            "can_scale_lambda": request.user.has_role("cto") or request.user.is_superuser,
            "can_pause_exams":  request.user.has_perm("portal.pause_exam"),
        }

    def _read_metric(self, r, key):
        data = r.hgetall(key)  # {"value": "3842", "ts": "1711015327", "limit": "5000"}
        if not data:
            return {"value": None, "ts": None, "stale": True}
        age_s = time.time() - float(data.get(b"ts", 0))
        return {
            "value": float(data.get(b"value", 0)),
            "ts": data.get(b"ts"),
            "stale": age_s > 10,
            "stale_seconds": int(age_s),
            "limit": float(data.get(b"limit", 0)) if b"limit" in data else None,
        }
```

**Action endpoints:**

| Method | URL | Permission | Action |
|---|---|---|---|
| POST | `/exec/war-room/actions/pause-all/` | `portal.pause_all_exams` | Bulk pause + notify + P0 incident |
| POST | `/exec/war-room/actions/pause-exam/` | `portal.pause_exam` | Pause single exam by `exam_id` |
| POST | `/exec/war-room/actions/broadcast/` | `portal.broadcast_alert` | WhatsApp/SMS to all live-exam institutions |
| POST | `/exec/war-room/actions/scale-lambda/` | `portal.scale_lambda` (CTO only) | boto3 put_function_concurrency |
| POST | `/exec/war-room/actions/page-devops/` | `portal.view_war_room` | PagerDuty API + Slack webhook |
| POST | `/exec/war-room/actions/escalate/` | `portal.manage_incidents` | Escalate incident by `incident_id` |
| POST | `/exec/war-room/actions/resolve/` | `portal.manage_incidents` | Resolve incident by `incident_id` |

---

## 9. Database & Caching

**Celery Beat Tasks (all run during peak — scheduled to start 30 min before first exam of day):**

```python
# celery_tasks/war_room.py

@app.task
def refresh_war_room_metrics():
    """Runs every 4s. Writes all command strip + gauge metrics to Redis."""
    r = get_redis_connection()
    ts = str(time.time())

    # Lambda concurrency — boto3 call (cached 15s to avoid CloudWatch throttle)
    if not r.get("war:lambda_conc_cache_lock"):
        cw = boto3.client("cloudwatch", region_name="ap-south-1")
        resp = cw.get_metric_statistics(...)  # ConcurrentExecutions
        r.hset("war:lambda_concurrency", mapping={
            "value": resp["Datapoints"][-1]["Maximum"],
            "ts": ts,
            "limit": get_lambda_reserved_concurrency(),
        })
        r.setex("war:lambda_conc_cache_lock", 15, "1")

    # Submissions/sec — from Redis sorted set of submission events
    recent = r.zrangebyscore("events:submissions", time.time() - 10, "+inf")
    r.hset("war:submissions_per_sec", mapping={"value": len(recent) / 10, "ts": ts})

    # RDS connections — from cached CloudWatch RDS metric
    # ... similar pattern

    # Redis hit ratio — from INFO stats
    info = r.info("stats")
    hits = info["keyspace_hits"]
    misses = info["keyspace_misses"]
    ratio = (hits / (hits + misses) * 100) if (hits + misses) > 0 else 100
    r.hset("war:redis_hit_ratio", mapping={"value": round(ratio, 2), "ts": ts})

    # Error rate — from aggregated API error counter (incremented by middleware)
    total = int(r.get("metrics:requests_1m") or 1)
    errors = int(r.get("metrics:errors_1m") or 0)
    r.hset("war:error_rate", mapping={"value": round(errors/total*100, 3), "ts": ts})


@app.task
def refresh_war_room_institutions():
    """Runs every 8s. Writes institution-level exam status to Redis hash."""
    live_exams = (
        Exam.objects
        .filter(status__in=["live", "queued"])
        .select_related("institution", "exam_template")
        .annotate(
            submitted_count=Count("attempts", filter=Q(attempts__status="submitted")),
            error_count=Count("attempts", filter=Q(
                attempts__status="error",
                attempts__updated_at__gte=now() - timedelta(minutes=5)
            )),
        )
    )
    r = get_redis_connection()
    r.delete("war:institutions")
    for exam in live_exams:
        r.hset("war:institutions", exam.id, json.dumps({
            "institution_name": exam.institution.name,
            "institution_type": exam.institution.type,
            "exam_name": exam.exam_template.name,
            "enrolled": exam.enrolled_count,
            "submitted": exam.submitted_count,
            "errors_5m": exam.error_count,
            "status": "issues" if exam.error_count > 10 else "live",
            "latency_p95_ms": get_exam_latency_p95(exam.id),  # from Redis metrics
        }))
```

**Key Redis schema:**

| Key | Type | TTL | Written by | Read by |
|---|---|---|---|---|
| `war:lambda_concurrency` | Hash (value, ts, limit) | None (overwritten every 4s) | Celery beat | War Room view |
| `war:submissions_per_sec` | Hash (value, ts) | None | Celery beat | War Room view |
| `war:rds_connections_current` | Hash | None | Celery beat | War Room view |
| `war:redis_hit_ratio` | Hash | None | Celery beat | War Room view |
| `war:error_rate` | Hash | None | Celery beat | War Room view |
| `war:otp_success_rate` | Hash | None | Celery beat | War Room view |
| `war:institutions` | Hash (exam_id → JSON) | None | Celery beat | Institution grid partial |
| `war:throughput_ts` | Sorted set (score=epoch, value=JSON) | 600s entries (auto-expire) | Submission middleware | Throughput chart |
| `events:submissions` | Sorted set | 60s entries | Exam submission handler | Submissions/sec calc |

---

## 10. Validation Rules

| Action | Validation |
|---|---|
| Pause All Exams | `confirm_phrase` must equal "PAUSE ALL EXAMS" (case-sensitive). `reason` field required, min 10 chars. |
| Pause Single Exam | `exam_id` must exist and have `status="live"`. Actor must have `portal.pause_exam` permission. |
| Emergency Lambda Scale | `delta` must be positive integer, max 2,000. Actor must have `portal.scale_lambda`. AWS account concurrent limit check (do not exceed account-level limit). |
| Broadcast Alert | `message` required, max 160 chars (SMS limit). At least one active exam must exist. |
| Create Incident | Severity required. Title required max 100 chars. Services min 1. |
| Resolve Incident | Incident must have `status in ['open','escalated']`. Actor must have `portal.manage_incidents`. |

---

## 11. Security Considerations

| Concern | Implementation |
|---|---|
| Action authentication | All POST actions require `@login_required` + explicit `has_perm()` check per action. No role assumed from session alone. |
| CSRF protection | All HTMX POST requests include `hx-headers='{"X-CSRFToken": "{{ csrf_token }}"}'` on the page shell. |
| CFO redirect | Enforced at view level (`WarRoomView.get()`) — not just UI hiding. HTTP 302 redirect, not 403. |
| Lambda scale audit | Every call to `put_function_concurrency()` creates an `AuditLog` entry with actor, timestamp, old limit, new limit, reason. |
| Pause All audit | Bulk pause creates one `AuditLog` entry per paused exam (not one entry for "all") — so the audit trail shows exactly which exams were paused by whom. |
| Rate limiting | POST actions rate-limited: 10 requests/minute per user for pause/broadcast, 2 requests/minute for Lambda scale. Uses Django rate-limit middleware. |
| War Room access logging | Every War Room page load is logged to `WarRoomAccessLog` table (user, timestamp, IP). Useful for post-incident review: who was watching when the failure happened. |
| No sensitive data exposure | Lambda limit values (Reserved Concurrency = billing-sensitive AWS config) visible to CTO/Admin only. COO/CEO see only the % gauge without the raw number. |

---

## 12. Edge Cases (System-Level)

| State | Behaviour |
|---|---|
| P0 incident auto-detected | Error rate > 2% for > 60s → system auto-creates P0 incident draft, flashes incident panel red, audio alert (if enabled), sends PagerDuty page |
| Lambda at 100% (throttling) | Command strip shows CRIT state; gauge goes full red with pulsing; "Emergency Lambda Scale" button border pulses green to draw attention; auto-creates P1 incident |
| Redis hit ratio < 90% | CRIT state + "Cache Stampede Risk" alert toast; Celery beat self-check link shown in gauge tooltip |
| 0 submissions for > 30s | "⚠ SUBMISSION FLATLINE" red banner appears below throughput chart. Not necessarily failure (all students may have submitted), but requires human confirmation |
| Celery beat worker down | All Redis keys go stale > 10s → command strip cards go grey with stale indicator. War Room banner: "⚠ Metric refresh offline — data may be stale. [Check Celery →]" |
| Network disconnect (client) | HTMX catches failed polls → after 3 failures: red "Connection lost — retrying…" banner at top of page. Retries every 10s. |
| Session expired during peak | HTMX 401 response → JS redirects to `/login/?next=/exec/war-room/` — user logs back in and returns to War Room |
| Multiple users in War Room | Supported — each user sees same data (Redis). Pause actions show "Paused by {name}" in the incident log. No collision issues since all writes are atomic Redis operations. |
| Accidental Exit | If user navigates away (back button, link click), `beforeunload` event shows "You are leaving the War Room during an active exam peak. Are you sure?" |
| No exams scheduled | War Room shows "No active exams" state for all sections. Auto-activation banner on exec pages suppressed. Page accessible manually but shows this state. |

---

## 13. Performance & Scaling

**Response time targets:**

| Endpoint | Target | Critical Threshold |
|---|---|---|
| War Room full page shell | < 150ms | > 500ms |
| `?part=command` | < 80ms | > 200ms |
| `?part=throughput-data` (JSON) | < 50ms | > 150ms |
| `?part=institutions` (50 rows) | < 120ms | > 300ms |
| `?part=gauges` | < 80ms | > 200ms |
| `?part=incidents` | < 100ms | > 250ms |
| POST pause-all (sync portion) | < 500ms (async notify queued) | > 2s |

**All reads are Redis only. Zero database queries during War Room polling.**

The one exception: POST actions (pause exam, create incident) write to the database. These are rare, high-value operations where 200–500ms latency is acceptable.

**Celery beat schedule during peak:**
```python
CELERYBEAT_SCHEDULE = {
    "war-room-metrics": {
        "task": "celery_tasks.war_room.refresh_war_room_metrics",
        "schedule": 4.0,  # every 4 seconds
        "options": {"queue": "war_room_priority"},
    },
    "war-room-institutions": {
        "task": "celery_tasks.war_room.refresh_war_room_institutions",
        "schedule": 8.0,
        "options": {"queue": "war_room_priority"},
    },
}
```

The `war_room_priority` queue is a dedicated Celery queue with higher worker allocation during exam days — so a slow content-processing task cannot delay a War Room metric refresh.

**Database query protection:**
- `refresh_war_room_institutions` task runs the annotated query against the DB (it must — it needs live submission counts). This query is designed to complete in < 500ms even at 74K concurrent:
  - Filtered by `status IN ['live','queued']` (index on `exams.status`)
  - `Count("attempts")` uses a covering index on `exam_attempts(exam_id, status, updated_at)`
  - Django ORM generates a single GROUP BY query — no N+1

**HTMX poll concurrency:**
- If 5 War Room users are polling simultaneously: 5 × 5 requests/second × 5 partials = 125 requests/minute to the War Room view
- All War Room view handlers read from Redis only → each request < 80ms → 125 rpm is trivial (Django handles 1,000s of rpm at this latency)

**Auto-deactivation of Celery beat war-room tasks:**
- Tasks are enabled by a Redis flag: `war:peak_active` (set when concurrent users > 10,000, unset when all exams end)
- When `war:peak_active` is unset, tasks run at 60s interval instead of 4s (saves Redis/CPU between peaks)
