# 35 — Customer Health & Churn Map

---

## 1. Page Metadata

| Field | Value |
|---|---|
| Page title | Customer Health & Churn Map |
| Route | `/exec/customer-health/` |
| Django view | `CustomerHealthView` |
| Template | `exec/customer_health.html` |
| Priority | **P1** |
| Nav group | Operations |
| Required roles | `ceo` · `coo` · `csm_manager` · `account_manager` · `superadmin` |
| CFO access | Read-only (revenue-at-risk column only) |
| CTO access | Denied — redirect to `/exec/dashboard/` |
| HTMX poll — health table | Every 300s (5 min) |
| HTMX poll — summary strip | Every 300s |
| Cache | Health scores: Redis TTL 290s · Churn signals: Redis TTL 1800s |
| Theme tokens | bg-base `#040810` · surface-1 `#08101E` · surface-2 `#0D1828` · accent `#6366F1` · success `#22C55E` · danger `#EF4444` · warn `#F59E0B` |

---

## 2. Purpose & Business Logic

**The retention problem at scale:**

EduForge has 2,050 institutions. At Rs.60 Cr ARR, average revenue per institution is ~Rs.2.9 lakh/year. Losing 50 institutions to churn = Rs.1.5 Cr ARR gone. At the coaching centre tier (avg Rs.15 lakh/year each), losing 5 = Rs.75 lakh gone.

The COO and CSM team currently have no single view showing which institutions are healthy, which are at risk, and which have already begun the behavioural patterns that precede cancellation. Customer health signals are scattered across:
- Exam usage data (are students actually taking exams?)
- Login frequency (is the admin even using the portal?)
- Support ticket volume (are they frustrated?)
- Billing status (are they paying on time?)
- BGV compliance (are they completing onboarding requirements?)
- Feature adoption (are they using the platform deeply or just the bare minimum?)

**The composite health score:**

Each institution gets a **0–100 Health Score**, computed nightly by a Celery beat task. Score is weighted across 6 dimensions:

| Dimension | Weight | Green signal | Red signal |
|---|---|---|---|
| Exam Activity | 30% | ≥ 1 exam/week | No exam in 30+ days |
| Login Frequency | 20% | Admin logs in ≥ 3×/week | No login in 14+ days |
| Support Load | 15% | 0 open tickets | 3+ open P1/P2 tickets |
| Payment Health | 20% | All invoices paid on time | Overdue invoice > 30 days |
| Feature Adoption | 10% | Uses ≥ 4 modules | Uses only 1 module |
| BGV Compliance | 5% | 100% staff verified | < 80% verified |

**Score bands:**
- 80–100: Healthy (green)
- 60–79: Needs attention (amber)
- 40–59: At risk (orange)
- 0–39: Critical — churn likely within 60 days (red)

**What decisions this page enables:**
- Which 20 institutions need a CSM call this week? → COO assigns from this page
- Which coaching centre (Rs.15L ARR) just dropped from 72 → 41 in 2 weeks? → Escalation Manager notified immediately
- What is the platform's aggregate health trend — are we getting healthier or sicker over 90 days? → CEO's retention KPI
- Which institution's score drop is driven by exam activity (product problem) vs payment (billing problem) vs support load (ops problem)? → Routes to right team

---

## 3. User Roles & Access

| Role | Can View | Can Act | Specific Capabilities |
|---|---|---|---|
| CEO / Platform Owner | All sections | Read-only | Full view including revenue-at-risk |
| COO | All sections | Assign CSM, trigger intervention, add notes | Cannot see invoice amounts |
| CSM Manager | All sections | Assign CSM, add notes, mark intervention done | Cannot see invoice amounts |
| Account Manager | Institutions assigned to them only | Add notes, request escalation | Filtered view |
| CFO | Summary strip + at-risk table (revenue column only) | Read-only | Sees only institution name + health score + ARR at risk |
| Escalation Manager | All sections | Trigger escalation | Cannot assign CSM |
| CTO | No access | — | Redirect |

**Account Manager filtered view:** When `request.user.role == 'account_manager'`, the table is pre-filtered to `institution.csm_assigned == request.user`. They cannot see other AM's accounts.

---

## 4. Section-wise UI Breakdown

---

### Section 1 — Page Header

**Purpose:** Set context and provide quick filters. The COO arrives here every Monday morning — the default view should immediately show what needs action this week.

**User interaction:**
- Segment filter: [All] [Schools] [Colleges] [Coaching] [Groups]
- Health filter: [All] [Critical] [At Risk] [Needs Attention] [Healthy]
- Sort: by Health Score (default: ascending — worst first), by Score Change (biggest drop first), by ARR
- Search: institution name

**UI elements:**
```
Customer Health & Churn Map    [Segment: All ▾]  [Health: All ▾]  [Sort: Score ▾]  [🔍]
Last score computation: Today 02:14 IST  ·  Next run: Tomorrow 02:00 IST
```
- Secondary line: `text-xs text-[#8892A4]` — shows when scores were last computed (important for trust)
- Filter chips persist in URL params (`?segment=coaching&health=critical`) so COO can bookmark "Critical Coaching Centres"

**Data flow:** Filters passed as GET params → `hx-get="/exec/customer-health/?part=table&segment=coaching&health=critical"` on change.

**Edge cases:** If score computation ran > 36 hours ago: secondary line turns amber "⚠ Scores last computed 38h ago — may be stale."

**Mobile:** Filter dropdowns collapse into a single `[Filters ▾]` button that opens a bottom sheet.

**Accessibility:** All filters have `aria-label`. Active filter state communicated via `aria-pressed` on chips.

---

### Section 2 — Summary Strip

**Purpose:** Platform-level retention health at a glance. COO and CEO's weekly KPI check.

**User interaction:** Read-only. "Critical" count card is clickable — filters table to critical-only.

**UI elements — 5 cards:**

```
╔═══════════════╦═══════════════╦═══════════════╦═══════════════╦═══════════════╗
║ AVG HEALTH    ║ CRITICAL       ║ AT RISK        ║ HEALTHY        ║ ARR AT RISK   ║
║ SCORE         ║ (0–39)         ║ (40–59)        ║ (80–100)       ║               ║
║               ║               ║               ║               ║               ║
║     72.4      ║      14        ║      38        ║    1,820       ║  ₹3.2 Cr      ║
║  ▲ +1.8 MoM   ║  ▼ was 11 last ║  ▲ was 31 last ║               ║  coaching: 62%║
╚═══════════════╩═══════════════╩═══════════════╩═══════════════╩═══════════════╝
```

| Card | Detail | Alert |
|---|---|---|
| Avg Health Score | Platform-wide average. Trend arrow vs last month. | Decrease > 3 pts MoM: amber |
| Critical (0–39) | Count of institutions in red zone. Delta vs last week. | Any increase: amber |
| At Risk (40–59) | Count in orange zone. | If > 10% of total: amber |
| Healthy (80–100) | Count in green zone. | — |
| ARR at Risk | Sum of ARR for Critical + At Risk institutions. Segment breakdown in subline. | > Rs.2 Cr: amber; > Rs.5 Cr: red |

**HTMX:** `id="health-summary"` `hx-get="/exec/customer-health/?part=summary"` `hx-trigger="load, every 300s"` `hx-swap="innerHTML"`

**Data flow:** Pre-aggregated nightly. Cached in Redis `health:summary` TTL 290s.

**Role-based behavior:** "ARR at Risk" card hidden for COO (sees count but not rupee value). CFO sees only this card.

**Edge cases:** If 0 critical institutions: Critical card shows "0 ✅" with green background.

**Performance:** Redis read only. < 80ms.

**Mobile:** 2×3 card grid.

**Accessibility:** Delta arrows have `aria-label="Increased by 3 since last month"`.

---

### Section 3 — Health Score Table (Core of Page)

**Purpose:** The operational list. Every institution, its score, its trend, its assigned CSM, and the one action the COO needs to take.

**User interaction:**
- Click row → opens Institution Health Drawer (Drawer-I, 560px)
- "Assign CSM" button per row (COO / CSM Manager only)
- "Add Note" per row → inline mini-form appears in row expansion
- Sort by any column header
- Pagination: 50 rows per page, server-side

**UI elements:**

```
INSTITUTION HEALTH                                              [Export CSV]
──────────────────────────────────────────────────────────────────────────────────────
Institution        │ Type    │ Score │ Trend   │ Top Decay Signal  │ CSM         │ ⋯
───────────────────┼─────────┼───────┼─────────┼───────────────────┼─────────────┼──
DEF Coaching       │Coaching │  31 🔴│ ▼ -22 ↘ │ No exam 28d       │ Ravi K.     │ ⋯
ABC School Group   │Group    │  38 🔴│ ▼ -8  ↘ │ 4 open tickets    │ Unassigned  │ ⋯
XYZ College        │College  │  44 🟠│ ▼ -5  ↘ │ Invoice overdue   │ Priya M.    │ ⋯
Sunrise Coaching   │Coaching │  68 🟡│ ▲ +3  ↗ │ Low feature use   │ Amit S.     │ ⋯
...
```

**Column details:**

| Column | Width | Detail |
|---|---|---|
| Institution | 200px | Name + type icon. Click → drawer |
| Type | 90px | School / College / Coaching / Group badge |
| Score | 80px | Number (0–100) + coloured dot. `font-bold`. Red < 40, Orange 40–59, Amber 60–79, Green 80+ |
| Trend | 100px | Delta vs 30 days ago (`▼ -22`) + 7-day sparkline (tiny, 40px wide). Red if declining > 10 pts/month |
| Top Decay Signal | 200px | The single most impactful negative dimension. e.g. "No exam 28d", "Invoice overdue 45d", "4 open P1 tickets" |
| CSM | 120px | Assigned CSM name or "Unassigned" (red badge if critical + unassigned) |
| ⋯ | 80px | View Detail · Assign CSM · Add Note · Trigger Escalation |

**Row colour coding:**
- Score 0–39: `border-l-4 border-red-500 bg-red-950/15`
- Score 40–59: `border-l-4 border-orange-500 bg-orange-950/10`
- Score 60–79: `border-l-4 border-amber-500/50`
- Score 80+: default background

**"Assign CSM" modal (400px):**
- Institution name (pre-filled, read-only)
- Current CSM (pre-filled)
- New CSM (searchable select — lists all CSM Manager + Account Manager users)
- Reason (optional, textarea)
- POST `/exec/customer-health/actions/assign-csm/` → updates `Institution.csm_assigned`, creates `InstitutionNote` with "CSM assigned: {name}", audit log

**"Add Note" inline form:**
- Expands below the row on click (not a modal — keeps user in context)
- Textarea (required, max 500 chars)
- Note type: [General] [Intervention] [Escalation] [Positive Signal]
- [Save Note] → POST → collapses row expansion, adds note count badge to row

**HTMX:** `id="health-table"` `hx-get="/exec/customer-health/?part=table&{{ filter_params }}"` `hx-trigger="load, every 300s[!document.querySelector('.drawer-open,.modal-open,.row-expanded')]"` `hx-swap="innerHTML"`

**Data flow:**
- `InstitutionHealthScore.objects.filter(...).select_related('institution', 'csm_assigned').order_by('score')`
- Cached per filter combination: `health:table:all:critical:score:1` TTL 290s
- Top decay signal: stored on `InstitutionHealthScore.top_decay_signal` (string, computed by Celery beat nightly)

**Role-based behavior:**
- Account Manager: query filtered to `csm_assigned == request.user` before any other filter
- "Trigger Escalation" in ⋯ menu: COO / Escalation Manager / CEO only
- "Assign CSM": COO / CSM Manager only

**Edge cases:**
- Critical + Unassigned combination: row's CSM cell shows "⚠ Unassigned" in red. Appears in a dedicated banner above table: "3 critical institutions have no CSM assigned. [Assign Now →]"
- Score = 0: rare edge case (institution completely inactive). Row shows "⚠ Dormant" badge. COO should investigate — possible off-platform migration.
- Score jumps > 20 pts in either direction between polls: `HealthScoreAlert` created (spike/crash alert)

**Performance:**
- 2,050 rows with filters: query uses composite index on `(segment, score, csm_assigned)`
- Sparklines: 7 data points per institution, pre-serialised as JSON in `InstitutionHealthScore.score_history_7d` (avoids N+1)
- 50 rows per page × 7-point sparklines = manageable DOM

**Mobile:** Trend sparkline hidden. Columns: Institution + Score + Top Signal + CSM only. Drawer opens full-screen.

**Accessibility:** Table `role="grid"`. Score dots `aria-label="Score: 31, Critical"`. Sort headers `aria-sort`.

---

### Section 4 — Churn Risk Heatmap

**Purpose:** Shows churn risk distribution visually. COO uses this monthly to understand the shape of the problem: is churn risk concentrated in one segment or one region?

**User interaction:**
- Two views toggled by tab: [By Segment] [By Acquisition Month]
- Hover any cell → tooltip with count + avg score + ARR at risk

**UI elements:**

**Tab: By Segment**
```
CHURN RISK HEATMAP                         [By Segment ●] [By Acq. Month]
         Critical  At Risk  Attention  Healthy
Schools  [  2   ] [  18  ] [  24   ] [  956 ]
Colleges [  4   ] [  12  ] [  8    ] [  776 ]
Coaching [  7   ] [   6  ] [  4    ] [   83 ]
Groups   [  1   ] [   2  ] [  2    ] [  145 ]
```
Each cell: `<div>` with background colour intensity proportional to count (darker = more). White number inside.
- Green cells for Healthy, intensity proportional to count
- Red cells for Critical, intensity proportional to count
- Empty cell (count = 0): `bg-[#0D1828]` dim

**Tab: By Acquisition Month (Cohort)**
```
         Critical  At Risk  Attention  Healthy
Jan 2025 [  0   ] [   1  ] [   2   ] [  48  ]
Feb 2025 [  1   ] [   3  ] [   4   ] [  62  ]
Mar 2025 [  2   ] [   5  ] [   6   ] [  71  ]
```
Reveals if newer institutions are healthier than older ones (or vice versa — onboarding quality signal).

**HTMX:** `id="churn-heatmap"` `hx-get="/exec/customer-health/?part=heatmap&view={{ view }}"` `hx-trigger="load"` `hx-swap="innerHTML"` (no polling — static until filter change)

**Data flow:**
- By Segment: `InstitutionHealthScore.objects.values('institution__type', 'score_band').annotate(count=Count('id'), arr_at_risk=Sum('institution__arr'))`
- By Acq Month: same but `values('institution__onboarded_month', 'score_band')`
- Cache: `health:heatmap:segment` and `health:heatmap:cohort` TTL 1800s

**Mobile:** Heatmap cells reduce to 32px × 32px. Count shown. Tooltip replaced by tap → shows value below cell.

**Accessibility:** Each cell `role="gridcell" aria-label="Coaching, Critical: 7 institutions"`.

---

### Section 5 — Score Trend Chart

**Purpose:** Platform-level health over time. Is the COO's retention efforts working? This chart answers it.

**User interaction:**
- Date range: [30d ●] [60d] [90d] — switches the x-axis window
- Toggle series: show/hide individual bands (Critical / At Risk / Healthy count over time)

**UI elements:**
- Chart.js Stacked Area or Line, `id="health-trend-chart"`, full width, 200px tall
- X-axis: dates (daily for 30d, weekly for 90d)
- Series 1: Critical count — `#EF4444` fill `rgba(239,68,68,0.15)`
- Series 2: At Risk count — `#F97316` fill `rgba(249,115,22,0.12)`
- Series 3: Healthy count — `#22C55E` fill `rgba(34,197,94,0.10)`
- Tooltip: "Mar 15: Critical 18, At Risk 42, Healthy 1,790"

**HTMX:** `id="health-trend"` `hx-get="/exec/customer-health/?part=trend&days={{ days }}"` `hx-trigger="load"` `hx-swap="innerHTML"` (HTMX returns full chart init HTML with embedded data)

**Data flow:** `DailyHealthSnapshot` model (one row per day, storing band counts). Pre-computed by Celery beat nightly after health score computation completes.

**Mobile:** Chart height 120px. Only Critical and Healthy series shown (At Risk hidden for space).

**Accessibility:** `role="img" aria-label="Health score trend: 90-day chart. Critical institutions declining from 22 to 14."`.

---

## 5. Full Page Wireframe

```
╔══════════════════════════════════════════════════════════════════════════════╗
║  Customer Health & Churn Map  [Segment: All ▾] [Health: All ▾] [Sort ▾] [🔍]║
║  Last score computation: Today 02:14 IST · Next: Tomorrow 02:00 IST         ║
╠═════════════╦═════════════╦═════════════╦═════════════╦═════════════════════╣
║ AVG SCORE   ║ CRITICAL    ║ AT RISK     ║ HEALTHY     ║ ARR AT RISK         ║
║    72.4     ║     14      ║     38      ║   1,820     ║  ₹3.2 Cr            ║
║  ▲ +1.8 MoM ║  ▼ was 11  ║  ▲ was 31  ║             ║  coaching: 62%      ║
╠═════════════╩═════════════╩═════════════╩═════════════╩═════════════════════╣
║  ⚠ 3 critical institutions unassigned  [Assign Now →]                       ║
║  INSTITUTION HEALTH                                          [Export CSV]   ║
║  Institution        │Type    │Score │Trend    │Top Signal      │CSM         ║
║  DEF Coaching       │Coaching│ 31🔴 │▼ -22 ↘  │No exam 28d     │Ravi K.    ║
║  ABC School Group   │Group   │ 38🔴 │▼ -8  ↘  │4 open tickets  │⚠Unassigned║
║  XYZ College        │College │ 44🟠 │▼ -5  ↘  │Invoice overdue │Priya M.   ║
║  Sunrise Coaching   │Coaching│ 68🟡 │▲ +3  ↗  │Low feature use │Amit S.    ║
║  [< Prev]  Page 1 of 41  [Next >]                                            ║
╠════════════════════════════════════╦════════════════════════════════════════╣
║  CHURN RISK HEATMAP                ║  SCORE TREND (90d)                     ║
║  [By Segment ●] [By Acq. Month]    ║  [30d] [60d] [90d ●]                   ║
║           Crit  Risk  Attn  Hlthy  ║  ┌──────────────────────────────────┐  ║
║  Schools  [ 2] [ 18] [ 24] [ 956] ║  │  ████ Critical (declining)       │  ║
║  Colleges [ 4] [ 12] [  8] [ 776] ║  │  ░░░░ At Risk                    │  ║
║  Coaching [ 7] [  6] [  4] [  83] ║  │  ▓▓▓▓ Healthy (growing)          │  ║
║  Groups   [ 1] [  2] [  2] [ 145] ║  └──────────────────────────────────┘  ║
╚════════════════════════════════════╩════════════════════════════════════════╝
```

---

## 6. Drawer-I — Institution Health Detail (560px)

**Open trigger:** Click any row in health table.

**HTMX:** `hx-get="/exec/customer-health/?part=health-drawer&id={{ institution_id }}"` `hx-target="#drawer-container"` `hx-swap="innerHTML"`

```
┌────────────────────────────────────────────────────────┐
│  DEF Coaching Pvt Ltd                   Score: 31 🔴 [✕]│
│  ─────────────────────────────────────────────────────  │
│  [Score Breakdown ●]  [Signals]  [Notes]  [History]     │
│  ─────────────────────────────────────────────────────  │
│  (tab content)                                          │
│  ─────────────────────────────────────────────────────  │
│  [Assign CSM]  [Add Note]  [Trigger Escalation]         │
└────────────────────────────────────────────────────────┘
```

**Tab — Score Breakdown:**
Radar/spider chart of 6 dimensions (Chart.js Radar), 280px, showing current score per dimension vs benchmark:

```
Dimension       Score   Weight  Contribution  Signal
Exam Activity     8/30   30%       2.4 pts    ⚠ No exam in 28 days
Login Frequency  12/20   20%       2.4 pts    ⚠ Last login: 19 days ago
Support Load     12/15   15%       1.8 pts    ⚠ 3 open tickets (P2)
Payment Health   18/20   20%       3.6 pts    ✅ All invoices current
Feature Adoption  7/10   10%       0.7 pts    ⚠ Only 2 modules active
BGV Compliance    4/5     5%       0.4 pts    ✅ 94% staff verified
────────────────────────────────────────────
Total Score:  31 / 100
```

Radar chart: current (red fill) overlaid on benchmark (dashed green outline = avg healthy institution).

**Tab — Signals:**
Timeline of all health events for this institution:
```
🔴 28 Mar  No exam taken in 21+ days (threshold crossed)
🟡 22 Mar  Support ticket P2 opened (now 3 open total)
✅ 18 Mar  Invoice paid (renewal confirmed)
🔴 14 Mar  Admin login gap: 12 days since last access
🟡  8 Mar  Feature adoption dropped: stopped using Reports module
```

**Tab — Notes:**
All `InstitutionNote` records for this institution, newest first:
```
[Ravi K.]  31 Mar 2026  [Intervention]
"Called admin. They say exams are planned for next week.
 Will monitor — re-check score in 7 days."

[System]  28 Mar 2026  [Auto]
"Score dropped from 53 → 31. Top signal: exam inactivity."
```
+ inline "Add Note" form at top.

**Tab — History:**
Line chart: institution's health score over last 90 days.
Key events annotated on chart (e.g., "Support ticket opened", "Invoice paid").

**Footer actions:**
- [Assign CSM]: opens Assign CSM modal (same as inline table action)
- [Add Note]: scrolls to Notes tab with form focused
- [Trigger Escalation]: COO / Escalation Manager only → opens Escalation modal (institution pre-filled, severity select, reason textarea, assigns to Escalation Manager) → creates `EscalationRecord`

---

## 7. Component Architecture

| Component | File | Props |
|---|---|---|
| `HealthSummaryCard` | `components/health/summary_card.html` | `label, value, delta, delta_period, alert_level, can_view_arr` |
| `HealthTableRow` | `components/health/table_row.html` | `institution, score, score_band, trend_delta, sparkline_data, top_decay_signal, csm, can_assign, can_escalate` |
| `ScoreBadge` | `components/health/score_badge.html` | `score, band (critical/at-risk/attention/healthy)` |
| `TrendCell` | `components/health/trend_cell.html` | `delta, sparkline_data (7 points)` |
| `HeatmapCell` | `components/health/heatmap_cell.html` | `count, band, segment_or_month, arr_at_risk` |
| `HealthDrawer` | `components/health/drawer.html` | `institution_id` |
| `ScoreBreakdownTable` | `components/health/score_breakdown.html` | `dimensions (list of {name, score, max, weight, signal})` |
| `SignalTimeline` | `components/health/signal_timeline.html` | `events (list of {date, type, message})` |
| `NotesList` | `components/health/notes_list.html` | `notes, institution_id, can_add` |
| `AssignCSMModal` | `components/health/assign_csm_modal.html` | `institution_id, current_csm, csm_options` |
| `EscalationModal` | `components/health/escalation_modal.html` | `institution_id, institution_name` |

---

## 8. HTMX Architecture

**Page URL:** `/exec/customer-health/`
**All partials:** `/exec/customer-health/?part={name}`

| `?part=` | Target | Trigger | Poll | Swap |
|---|---|---|---|---|
| `summary` | `#health-summary` | load | Every 300s | innerHTML |
| `table` | `#health-table` | load + filter/sort/page change | Every 300s (pause on drawer/modal/expanded row) | innerHTML |
| `heatmap` | `#churn-heatmap` | load + view tab change | None | innerHTML |
| `trend` | `#health-trend` | load + range change | None | innerHTML |
| `health-drawer` | `#drawer-container` | Row click | None | innerHTML |

---

## 9. Backend View & API

```python
class CustomerHealthView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "portal.view_customer_health"

    ALLOWED_ROLES = frozenset(["ceo","coo","csm_manager","account_manager",
                                "escalation_manager","superadmin","cfo"])

    def get(self, request):
        if request.user.role not in self.ALLOWED_ROLES:
            messages.warning(request, "Access restricted.")
            return redirect("exec:dashboard")

        segment = request.GET.get("segment", "all")
        health  = request.GET.get("health", "all")
        sort    = request.GET.get("sort", "score")
        page    = int(request.GET.get("page", 1))
        q       = request.GET.get("q", "")

        # Account managers see only their assigned institutions
        am_filter = None
        if request.user.role == "account_manager":
            am_filter = request.user

        can_view_arr = request.user.role in {"ceo", "superadmin"}

        if _is_htmx(request):
            part = request.GET.get("part", "")
            ctx  = self._build_context(request, segment, health, sort, page, q,
                                        am_filter, can_view_arr)
            dispatch = {
                "summary":       "exec/health/partials/summary.html",
                "table":         "exec/health/partials/table.html",
                "heatmap":       "exec/health/partials/heatmap.html",
                "trend":         "exec/health/partials/trend.html",
                "health-drawer": "exec/health/partials/drawer.html",
            }
            if part in dispatch:
                return render(request, dispatch[part], ctx)
            return HttpResponseBadRequest("Unknown part")

        ctx = self._build_context(request, segment, health, sort, page, q,
                                   am_filter, can_view_arr)
        return render(request, "exec/customer_health.html", ctx)

    def _get_health_queryset(self, segment, health, sort, q, am_filter):
        qs = (InstitutionHealthScore.objects
              .select_related("institution", "csm_assigned")
              .filter(computed_date=latest_score_date()))

        if segment != "all":
            qs = qs.filter(institution__type=segment)
        if health == "critical":
            qs = qs.filter(score__lte=39)
        elif health == "at-risk":
            qs = qs.filter(score__range=(40, 59))
        elif health == "attention":
            qs = qs.filter(score__range=(60, 79))
        elif health == "healthy":
            qs = qs.filter(score__gte=80)
        if q:
            qs = qs.filter(institution__name__icontains=q)
        if am_filter:
            qs = qs.filter(csm_assigned=am_filter)

        sort_map = {
            "score": "score",
            "-score": "-score",
            "trend": "trend_delta_30d",
            "arr": "-institution__arr",
        }
        return qs.order_by(sort_map.get(sort, "score"))
```

**Action endpoints:**

| Method | URL | Permission | Action |
|---|---|---|---|
| POST | `/exec/customer-health/actions/assign-csm/` | `portal.assign_csm` | Update `Institution.csm_assigned`, create `InstitutionNote`, audit log |
| POST | `/exec/customer-health/actions/add-note/` | `portal.view_customer_health` | Create `InstitutionNote` |
| POST | `/exec/customer-health/actions/trigger-escalation/` | `portal.manage_escalations` | Create `EscalationRecord`, notify Escalation Manager |
| GET | `/exec/customer-health/?part=export&format=csv` | `portal.export_health_data` | CSV of health table |

---

## 10. Database Schema

```python
class InstitutionHealthScore(models.Model):
    institution     = models.ForeignKey("Institution", on_delete=models.CASCADE, db_index=True)
    computed_date   = models.DateField(db_index=True)

    # Composite score
    score           = models.IntegerField()  # 0–100
    score_band      = models.CharField(max_length=12,
                          choices=[("critical","Critical"),("at_risk","At Risk"),
                                   ("attention","Attention"),("healthy","Healthy")])

    # Dimension scores (0–max weight)
    exam_activity_score   = models.FloatField()   # 0–30
    login_frequency_score = models.FloatField()   # 0–20
    support_load_score    = models.FloatField()   # 0–15
    payment_health_score  = models.FloatField()   # 0–20
    feature_adoption_score= models.FloatField()   # 0–10
    bgv_compliance_score  = models.FloatField()   # 0–5

    # Signals
    top_decay_signal      = models.CharField(max_length=100)  # human-readable top issue
    signal_details        = models.JSONField()  # full list of signal events

    # Trend
    trend_delta_7d  = models.IntegerField(default=0)   # score change vs 7 days ago
    trend_delta_30d = models.IntegerField(default=0)   # score change vs 30 days ago
    score_history_7d= models.JSONField()               # list of 7 daily scores for sparkline

    # Assignment
    csm_assigned    = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,
                                         on_delete=models.SET_NULL, related_name="health_assignments")

    class Meta:
        unique_together = ("institution", "computed_date")
        indexes = [
            models.Index(fields=["computed_date", "score_band", "institution"]),
            models.Index(fields=["computed_date", "score"]),
        ]


class InstitutionNote(models.Model):
    institution  = models.ForeignKey("Institution", on_delete=models.CASCADE, db_index=True)
    author       = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,
                                      on_delete=models.SET_NULL)
    note_type    = models.CharField(max_length=20,
                       choices=[("general","General"),("intervention","Intervention"),
                                ("escalation","Escalation"),("positive","Positive Signal"),
                                ("auto","Auto-generated")])
    body         = models.TextField()
    created_at   = models.DateTimeField(auto_now_add=True, db_index=True)
    is_system    = models.BooleanField(default=False)


class DailyHealthSnapshot(models.Model):
    """Aggregated daily counts for trend chart."""
    snapshot_date    = models.DateField(unique=True)
    critical_count   = models.IntegerField()
    at_risk_count    = models.IntegerField()
    attention_count  = models.IntegerField()
    healthy_count    = models.IntegerField()
    avg_score        = models.FloatField()
    arr_at_risk      = models.DecimalField(max_digits=14, decimal_places=2)


class EscalationRecord(models.Model):
    institution  = models.ForeignKey("Institution", on_delete=models.CASCADE)
    triggered_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
                                      related_name="escalations_triggered")
    assigned_to  = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,
                                      on_delete=models.SET_NULL,
                                      related_name="escalations_assigned")
    severity     = models.CharField(max_length=10)
    reason       = models.TextField()
    status       = models.CharField(max_length=20, default="open")
    created_at   = models.DateTimeField(auto_now_add=True)
    resolved_at  = models.DateTimeField(null=True)
```

**Celery Beat — Nightly Health Score Computation (02:00 IST):**

```python
@app.task
def compute_institution_health_scores():
    """
    Runs nightly at 02:00 IST.
    Computes health score for all 2,050 institutions.
    Runtime estimate: ~3–5 minutes at full scale.
    """
    today = date.today()
    institutions = Institution.objects.filter(status="active").prefetch_related(
        "exams", "support_tickets", "invoices", "staff_bgv_records"
    )

    scores_to_create = []
    for inst in institutions:
        # Compute each dimension
        exam_score    = _score_exam_activity(inst)      # 0–30
        login_score   = _score_login_frequency(inst)    # 0–20
        support_score = _score_support_load(inst)       # 0–15
        payment_score = _score_payment_health(inst)     # 0–20
        feature_score = _score_feature_adoption(inst)   # 0–10
        bgv_score     = _score_bgv_compliance(inst)     # 0–5

        total = sum([exam_score, login_score, support_score,
                     payment_score, feature_score, bgv_score])
        band  = _score_to_band(total)
        top_signal = _top_decay_signal(inst, exam_score, login_score,
                                        support_score, payment_score,
                                        feature_score, bgv_score)

        # 7-day history for sparkline
        prev_7 = InstitutionHealthScore.objects.filter(
            institution=inst,
            computed_date__gte=today - timedelta(days=7)
        ).values_list("score", flat=True).order_by("computed_date")

        scores_to_create.append(InstitutionHealthScore(
            institution=inst,
            computed_date=today,
            score=total,
            score_band=band,
            exam_activity_score=exam_score,
            login_frequency_score=login_score,
            support_load_score=support_score,
            payment_health_score=payment_score,
            feature_adoption_score=feature_score,
            bgv_compliance_score=bgv_score,
            top_decay_signal=top_signal,
            trend_delta_7d=total - (prev_7[0] if len(prev_7) >= 7 else total),
            trend_delta_30d=_score_30d_delta(inst, total),
            score_history_7d=list(prev_7) + [total],
        ))

    # Bulk create (one DB round-trip for all 2,050)
    InstitutionHealthScore.objects.bulk_create(
        scores_to_create, ignore_conflicts=True
    )

    # Update daily snapshot
    _write_daily_snapshot(today)

    # Alert on critical + unassigned combinations
    _fire_critical_unassigned_alerts()

    # Invalidate Redis caches
    r = get_redis_connection()
    r.delete("health:summary")
    for key in r.scan_iter("health:table:*"):
        r.delete(key)
```

---

## 11. Validation Rules

| Action | Validation |
|---|---|
| Assign CSM | `institution_id` must exist and be active. `csm_user_id` must have role `csm_manager` or `account_manager`. Actor must have `portal.assign_csm`. One assignment per institution (overwrites previous, logs both). |
| Add Note | `body` required, 1–500 chars. `note_type` must be a valid choice. Actor must have `portal.view_customer_health`. |
| Trigger Escalation | `institution_id` required. `severity` required. `reason` required, min 20 chars. Only one open escalation per institution allowed (returns error "An escalation is already open for this institution"). |
| CSV Export | Actor must have `portal.export_health_data`. Rate-limited: 5 exports/hour. |

---

## 12. Security Considerations

| Concern | Implementation |
|---|---|
| Account Manager isolation | `am_filter` set server-side from `request.user` — never from GET param. Account Manager cannot see other AM's accounts even by manipulating the URL. |
| ARR visibility restriction | `can_view_arr` boolean set server-side. Template does not render ARR values for COO/CSM roles — absent from DOM. |
| Health score data sensitivity | Health score data (low exam activity, overdue invoices) is commercially sensitive. All access logged in `AuditLog` at page load. |
| Escalation action | Creates `EscalationRecord` (immutable). Sends notification to `assigned_to` user. Both actor and assignee logged. |
| Note immutability | `InstitutionNote` records cannot be edited or deleted once created. Only addition allowed. Preserves audit trail. |
| CSRF | All POST actions use `hx-headers` CSRF token. |

---

## 13. Edge Cases (System-Level)

| State | Behaviour |
|---|---|
| Health score computation not run today | Table shows "⚠ Health scores are from yesterday (2 Mar 2026). Nightly computation may have failed. [Check Celery →]" amber banner |
| Institution churned (subscription cancelled) | Removed from active filter. Appears in a "Recently Churned" section below the main table (last 30 days) with final health score at time of churn. |
| Score spike > 20 pts upward | `HealthScoreAlert` of type `recovery` created. CSM notified: "DEF Coaching score jumped from 31 → 54 — positive signal." |
| Score crash > 20 pts downward | `HealthScoreAlert` of type `crash` created. Escalation Manager and assigned CSM notified immediately (not waiting for next poll). |
| 0 institutions in filtered view | Empty state: "No {segment} institutions in {health} health band. This is a good sign! ✅" (or "Try adjusting your filters.") |
| All 2,050 institutions critical | Extremely unlikely but handled: summary strip shows "2,050 🔴" with a P0 incident auto-created ("Platform-wide engagement crisis detected") |
| Celery score computation fails mid-run | `bulk_create` is atomic per batch of 100. Partial completion recorded. On next run, `ignore_conflicts=True` means already-computed institutions are skipped. |
| New institution (onboarded today) | No score yet — excluded from table. Gets first score after next nightly run. Listed in "New Institutions (no score yet)" section. |

---

## 14. Performance & Scaling

| Endpoint | Target | Critical Threshold |
|---|---|---|
| Page shell | < 500ms | > 1.5s |
| `?part=summary` | < 100ms (Redis) | > 300ms |
| `?part=table` (50 rows) | < 400ms | > 1s |
| `?part=heatmap` | < 200ms (Redis) | > 500ms |
| `?part=trend` | < 200ms | > 500ms |
| Health drawer load | < 400ms | > 1s |
| Nightly score computation (2,050 inst.) | < 5 min | > 15 min = alert to DevOps |

**Scaling notes:**
- Nightly computation: processes 2,050 institutions sequentially (not parallel) to avoid DB connection storms. At avg 150ms/institution = ~5 minutes. Acceptable for a nightly job.
- `bulk_create` in batches of 100: single DB round-trip per 100 institutions = 21 round-trips total.
- Table query with filters: composite index on `(computed_date, score_band, institution__type)` ensures < 50ms query time even at 2,050 rows.
- Redis caching: summary strip cached 290s, table cache keyed by all filter combinations (cleared nightly after computation). Cold cache after nightly computation is re-warmed on first request.
- Sparkline data pre-serialised in `score_history_7d` JSON field — no N+1 query for 50 table rows.

---

*Last updated: 2026-03-20*
