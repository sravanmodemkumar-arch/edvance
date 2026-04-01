# 01 — Product Dashboard

## 1. Platform Scale Reference

| Dimension | Value |
|---|---|
| Total institutions | 2,050 (1,000 schools · 800 colleges · 100 coaching · 150 groups) |
| Total students | 2.4M–7.6M |
| Peak concurrent exam load | 74,000 simultaneous submissions |
| Active feature flags | ~120 in production |
| Releases per quarter | ~6–8 releases |
| Active A/B experiments | ~5–10 at any time |
| Open defects (all severity) | Typically 80–200 |
| Test tenants | ~30–50 sandbox environments |
| Exam domains | 6+ (SSC · RRB · NEET · JEE · AP Board · TS Board) |
| Plan tiers | 4 (Starter · Standard · Professional · Enterprise) |

**Why this page matters:** The Product Dashboard is the single pane of glass for all 5 Division B roles. Every morning, the PM Platform opens this page to check: did last night's release deploy cleanly? Are any flags in a bad state? Is the QA team blocking the next release? Are adoption metrics moving in the right direction? This page replaces 5 separate Slack channels and 3 spreadsheets.

---

## 2. Page Metadata

| Field | Value |
|---|---|
| Page title | Product Dashboard |
| Route | `/product/dashboard/` |
| Django view class | `ProductDashboardView` |
| Template | `product/dashboard.html` |
| Permission required | `portal.view_product_dashboard` |
| Accessible to | PM Platform · PM Exam Domains · PM Institution Portal · UI/UX Designer · QA Engineer |
| 2FA required | No (read-only page; no destructive actions) |
| HTMX poll — KPI strip | Every 60s (paused when drawer/modal open) |
| HTMX poll — Activity feed | Every 30s (paused when drawer/modal open) |
| HTMX poll — QA summary | Every 120s |
| Nav group | Product |
| Nav icon | `grid-2x2` |
| Priority | P0 |

---

## 3. Wireframe

```
┌────────────────────────────────────────────────────────────────────────────────────┐
│ HEADER: Product Dashboard                    [Export PDF]  [Customize ▾]  [⚙ Prefs]│
├────────┬────────┬────────┬────────┬────────┬────────┬────────┬────────────────────┤
│ Active │ Flags  │ Next   │ Open   │ Test   │ A/B    │ Roadmap│ Feature            │
│ Flags  │ In     │ Release│ Defects│ Tenants│ Tests  │ On     │ Adoption           │
│  120   │ Partial│ v2.4.1 │  14    │   38   │   6    │ Track  │ 68%                │
│        │  8     │ in 3d  │ (2 P0) │        │ running│        │ ↑4% MoM            │
├────────┴────────┴────────┴────────┴────────┴────────┴────────┴────────────────────┤
│ TABS: [Overview] [Release Health] [Flag Health] [QA Summary] [Adoption]            │
├─────────────────────────────────────┬──────────────────────────────────────────────┤
│ RELEASE VELOCITY (chart)            │ ACTIVITY FEED                                │
│ Releases per quarter — Bar chart    │ [Filter: All ▾]                              │
│ v2.4 ████████████ 8 items           │ ● Flag "new_exam_ui" enabled for 10%   2m    │
│ v2.3 ██████ 5 items                 │ ● Release v2.4.1 moved to staging      15m   │
│ v2.2 ███████████ 9 items            │ ● Defect #412 P0 opened — exam crash   1h    │
│                                     │ ● A/B test "dashboard_v2" started      2h    │
│                                     │ ● Plan config updated by PM Platform   3h    │
│                                     │ [Load more]                                   │
├─────────────────────────────────────┼──────────────────────────────────────────────┤
│ FLAG HEALTH SUMMARY                 │ QA BLOCKERS                                  │
│ ● Enabled:     89  ████████████     │ P0 Defects:  2  ██ (blocking release)        │
│ ● Partial:      8  ██               │ P1 Defects: 12  ████████                     │
│ ● Disabled:    18  ████             │ Failed runs: 4  ██                           │
│ ● Deprecated:   5  █                │ Test coverage: 74%  ████████████░░           │
│ [View All Flags →]                  │ [View QA Dashboard →]                        │
├─────────────────────────────────────┼──────────────────────────────────────────────┤
│ ROADMAP BURNDOWN                    │ FEATURE ADOPTION (top 5 features)            │
│ Q1 2026: 12/18 items complete ██████│ Exam Timer Controls    ████████████ 91%      │
│ Q2 2026: 2/14 items started   ██░░░ │ Student Leaderboard    ██████████   82%      │
│                                     │ Batch Result Export    ████████     67%      │
│ [View Roadmap →]                    │ WhatsApp Notifications  ████████    63%      │
│                                     │ AI MCQ Generation       ████        44%      │
│                                     │ [View All Adoption →]                        │
└─────────────────────────────────────┴──────────────────────────────────────────────┘
```

---

## 4. Sections — Deep Specification

### 4.1 KPI Strip

**Container:** `flex gap-4 p-4 overflow-x-auto` · 8 cards · `bg-[#0D1526] rounded-xl border border-[#1E2D4A]`
**Poll:** `hx-get="?part=kpi" hx-trigger="every 60s[!document.querySelector('.drawer-open,.modal-open')]" hx-target="#kpi-strip" hx-swap="outerHTML"`
**Height:** 88px per card · `min-w-[140px] flex-shrink-0`

| # | Card | Value Format | Delta | Alert Threshold | Click Action |
|---|---|---|---|---|---|
| 1 | Active Flags | `120` | +3 this week | > 150 = amber | → `/product/feature-flags/` |
| 2 | Flags in Partial Rollout | `8` | — | > 20 = amber | → Feature Flags filtered by partial |
| 3 | Next Release | `v2.4.1 · in 3d` | Stage badge | Overdue = red | → Release detail drawer |
| 4 | Open Defects | `14` with P0 badge | +2 today | Any P0 = red banner | → Defect Tracker |
| 5 | Test Tenants Active | `38` | — | < 5 = amber | → Test Tenant Manager |
| 6 | A/B Tests Running | `6` | — | — | → A/B Test Manager |
| 7 | Roadmap On Track | `On Track ✓` or `At Risk ⚠` | — | Off-track = amber | → Product Roadmap |
| 8 | Feature Adoption | `68%` | `↑4% MoM` green | < 50% = amber | → Adoption tab |

**Count-up animation:** `data-count-up` on numeric value spans · runs once on first load via `requestAnimationFrame` · 600ms · easing `t*(2-t)` · guarded by `data-animated="true"` — does NOT replay on poll refresh.

**Delta chip:** `text-xs px-1.5 py-0.5 rounded-full`
- Green: `bg-[#064E3B] text-[#34D399]`
- Red: `bg-[#450A0A] text-[#F87171]`
- Amber: `bg-[#451A03] text-[#FCD34D]`

**P0 badge on Defects card:** `bg-[#EF4444] text-white text-[10px] px-1.5 py-0.5 rounded-full animate-pulse` — only shown when P0 count > 0

---

### 4.2 Tab Bar

**Container:** `flex border-b border-[#1E2D4A] px-6`
**Tab item:** `px-4 py-3 text-sm font-medium cursor-pointer`
- Inactive: `text-[#94A3B8] hover:text-white`
- Active: `text-white border-b-2 border-[#6366F1]`

**Tabs:**

| Tab | hx-get | Description |
|---|---|---|
| Overview | `?part=overview` | Release velocity + activity feed + flag health + QA blockers |
| Release Health | `?part=release_health` | Release pipeline status, staging checks, changelog preview |
| Flag Health | `?part=flag_health` | All 120 flags status board, stale flag warnings |
| QA Summary | `?part=qa_summary` | Module health grid, defect trends, automation pass rate |
| Adoption | `?part=adoption` | Feature adoption funnel, institution type breakdown |

**HTMX:** `hx-get="?part={tab}" hx-target="#tab-content" hx-swap="innerHTML" hx-push-url="false"`
**Loading skeleton:** `#tab-content` shows 3 skeleton rows `animate-pulse bg-[#1E2D4A] h-8 rounded mb-2` during load

---

### 4.3 Tab: Overview

Two-column layout: `grid grid-cols-2 gap-4 p-4`

#### 4.3.1 Release Velocity Chart (left column)

**Container:** `bg-[#0D1526] rounded-xl border border-[#1E2D4A] p-4`
**Title:** `text-sm font-semibold text-[#F1F5F9]` — "Release Velocity (last 6 releases)"
**Library:** Chart.js 4.4.2 · Canvas id: `release-velocity-chart` · height 220px
**Destroy-before-recreate:** `if (window._charts?.releaseVelocity) { window._charts.releaseVelocity.destroy(); }`

**Dataset:**

| Series | Colour | Type |
|---|---|---|
| Items shipped | `#6366F1` | Bar |
| Bugs fixed | `#10B981` | Bar (stacked) |
| Rollbacks | `#EF4444` | Bar (stacked) |
| Cycle time (days) | `#F59E0B` | Line on right Y-axis |

**X-axis:** Release labels (e.g., `v2.3`, `v2.3.1`, `v2.4`) · `color: '#64748B'`
**Y-axis left:** Item count · `color: '#64748B'` · grid: `#1E2D4A`
**Y-axis right:** Cycle time in days · `color: '#94A3B8'`
**Tooltip:** custom — shows release name, items, bugs fixed, cycle time, deploy date
**Click on bar:** opens Release Detail Drawer for that release

#### 4.3.2 Activity Feed (right column)

**Container:** `bg-[#0D1526] rounded-xl border border-[#1E2D4A] p-4 h-[320px] overflow-y-auto`
**Poll:** `hx-get="?part=feed" hx-trigger="every 30s[!document.querySelector('.drawer-open,.modal-open')]" hx-swap="innerHTML"`
**Title:** "Activity Feed" + Filter dropdown `[All ▾]`

**Filter options:**
- All activity
- Flags only
- Releases only
- Defects only
- QA activity
- Plan changes

**Feed item structure:**
```
● [icon] [actor] [action] [resource]   [relative time]
  └ sub-text detail line
```

**Icon colours by event type:**
- Flag change: `text-[#6366F1]` flag icon
- Release event: `text-[#10B981]` rocket icon
- Defect opened: `text-[#EF4444]` bug icon
- Defect closed: `text-[#34D399]` check icon
- Plan change: `text-[#F59E0B]` credit card icon
- A/B test: `text-[#22D3EE]` flask icon
- QA sign-off: `text-[#10B981]` shield icon

**Feed item click:** opens relevant drawer or links to relevant page
**"Load more" button:** `hx-get="?part=feed&page=2" hx-swap="beforeend" hx-target="#feed-list"`
**Empty state:** "No recent activity" · `text-[#475569] text-sm`

---

#### 4.3.3 Flag Health Summary (left column, below chart)

**Container:** `bg-[#0D1526] rounded-xl border border-[#1E2D4A] p-4`
**Title:** "Flag Health"

**Horizontal stacked progress bar** (full width, height 12px, `rounded-full`):
- Enabled: `bg-[#6366F1]` — proportion of 120
- Partial rollout: `bg-[#F59E0B]`
- Disabled: `bg-[#475569]`
- Deprecated: `bg-[#EF4444]`

**Legend row below bar:** `flex gap-4 text-xs text-[#94A3B8]`

| Status | Colour dot | Count |
|---|---|---|
| Enabled | `#6366F1` | 89 |
| Partial Rollout | `#F59E0B` | 8 |
| Disabled | `#475569` | 18 |
| Deprecated | `#EF4444` | 5 |

**Warnings section:** amber cards for flags needing attention
- Flags with 0% rollout for > 30 days: stale warning
- Flags enabled for > 90 days without deprecation plan: cleanup needed
- Flags with conflicting dependencies: conflict warning

**[View All Flags →]** link: `text-[#6366F1] text-sm hover:underline` → `/product/feature-flags/`

---

#### 4.3.4 QA Blockers (right column, below activity feed)

**Container:** `bg-[#0D1526] rounded-xl border border-[#1E2D4A] p-4`
**Title:** "QA Blockers for Next Release"

**Release name badge:** `bg-[#1E2D4A] text-[#94A3B8] text-xs px-2 py-1 rounded` — e.g., "v2.4.1"

| Metric | Value | Bar | Colour |
|---|---|---|---|
| P0 Defects | 2 | `██` | `#EF4444` |
| P1 Defects | 12 | `████████` | `#F59E0B` |
| Failed test runs | 4 | `██` | `#F59E0B` |
| Test coverage | 74% | `████████████░░░` | `#6366F1` |
| Automation pass rate | 91% | `███████████████░` | `#10B981` |

**Release readiness gauge:** SVG semicircle gauge 0–100
- 0–49: red `#EF4444`
- 50–74: amber `#F59E0B`
- 75–89: green `#10B981`
- 90–100: bright green `#34D399`
- Current score calculated as: `(100 - p0*30 - p1*5 + coverage*0.3 + automation*0.2)`

**QA sign-off status:** `✓ QA Lead signed off` green or `⚠ Awaiting QA sign-off` amber

**[View QA Dashboard →]** link → `/product/qa/`

---

### 4.4 Tab: Release Health

**Container:** `p-4 space-y-4`

#### 4.4.1 Release Pipeline Kanban

**Column layout:** `grid grid-cols-5 gap-3`

Columns (left to right):
1. **Planning** — `bg-[#0D1526] border border-[#1E2D4A]`
2. **Development** — same
3. **Staging** — same
4. **QA Sign-off** — same
5. **Production** — `bg-[#0A1628] border border-[#064E3B]`

Each column header: `text-xs font-semibold text-[#94A3B8] uppercase tracking-wider px-3 py-2`
Each release card in column: `bg-[#131F38] rounded-lg p-3 mb-2 cursor-pointer hover:border-[#6366F1] border border-transparent`

**Release card content:**
- Release version badge: `text-xs font-mono bg-[#1E2D4A] px-2 py-0.5 rounded`
- Release name: `text-sm text-[#F1F5F9]`
- Item count: `text-xs text-[#94A3B8]` e.g., "8 items · 3 bugs"
- Target date: `text-xs text-[#94A3B8]` — red if overdue
- QA status indicator: dot — red/amber/green
- Click: opens Release Detail Drawer (640px)

#### 4.4.2 Staging Environment Checks

**Table:** `id="staging-checks"`

| Column | Detail |
|---|---|
| Check | e.g., "API smoke test", "HTMX partials load", "DB migration dry-run" |
| Status | ✅ Pass · ❌ Fail · ⏳ Running · ⬜ Not run |
| Last run | Relative timestamp |
| Duration | Seconds |
| Actions | [Re-run] [View logs] |

**[Run All Checks]** button: `bg-[#6366F1] text-white px-4 py-2 rounded-lg text-sm`
Trigger: `hx-post="?action=run_checks" hx-target="#staging-checks" hx-swap="outerHTML"`

---

### 4.5 Tab: Flag Health

**Purpose:** Full status board of all 120 flags. Identifies stale, conflicting, or misconfigured flags.

#### 4.5.1 Toolbar

| Control | Type | Options |
|---|---|---|
| Search | Text input (debounce 300ms) | Search by flag key or name |
| Status | Multi-select | Enabled · Partial · Disabled · Deprecated |
| Owner | Dropdown | PM Platform · PM Exam · PM Portal · All |
| Age | Dropdown | < 7d · 7–30d · 30–90d · > 90d |
| [Apply] | Button | `bg-[#6366F1]` |

#### 4.5.2 Flag Status Grid

**Layout:** `grid grid-cols-4 gap-2 p-4` for compact overview
Each flag tile: `bg-[#0D1526] rounded-lg p-3 border border-[#1E2D4A] hover:border-[#6366F1] cursor-pointer`

Tile content:
- Flag key: `text-xs font-mono text-[#94A3B8]` e.g., `new_exam_ui`
- Flag name: `text-sm font-medium text-[#F1F5F9]`
- Status badge: colour-coded
- Rollout %: `text-xs text-[#94A3B8]` (if partial)
- Age: `text-xs text-[#475569]`
- Warning icon if stale or conflicting

**Status badge colours:**
- Enabled: `bg-[#064E3B] text-[#34D399]`
- Partial: `bg-[#451A03] text-[#FCD34D]`
- Disabled: `bg-[#1E2D4A] text-[#94A3B8]`
- Deprecated: `bg-[#450A0A] text-[#F87171]`

**Click on tile:** opens Flag Detail Drawer (560px)

#### 4.5.3 Stale Flag Warnings Panel

`bg-[#1A1000] border border-[#F59E0B] rounded-xl p-4 mb-4`
Lists flags that have been in partial rollout for > 60 days without progressing.
Each row: flag key · days since last change · owner · [Review] button

---

### 4.6 Tab: QA Summary

#### 4.6.1 Module Health Grid

**Layout:** `grid grid-cols-5 gap-3 p-4`

Modules tracked (20 total):
Auth · Dashboard (Exec) · Institution Mgmt · Student Analytics · Financial · Billing · Subscription Plans · Incidents · Alerting · Maintenance · Compliance · Audit Log · Security · Exam Catalog · Exam Detail · Question Bank · Proctoring · Reports · Usage Analytics · SLA

Each module tile: `bg-[#0D1526] rounded-xl border p-3`
- Module name: `text-sm font-medium text-[#F1F5F9]`
- Health score: `text-2xl font-bold` — colour by score
- Open defects count: `text-xs text-[#94A3B8]`
- Test coverage %: small progress bar
- Last test run: relative time

**Health score colour:**
- 90–100: `text-[#34D399] border-[#064E3B]`
- 70–89: `text-[#FCD34D] border-[#451A03]`
- < 70: `text-[#F87171] border-[#450A0A]`

**Click tile:** opens module's defect list filtered by that module in Defect Tracker

#### 4.6.2 Defect Trend Chart

**Canvas id:** `defect-trend-chart` · height 200px
**Series:**
- P0 defects: `#EF4444`
- P1 defects: `#F59E0B`
- P2 defects: `#6366F1`
- Closed: `#10B981` (shown as negative / below axis)

**X-axis:** last 30 days (daily) · `color: '#64748B'`
**Y-axis:** count · grid: `#1E2D4A`
**Tooltip:** date · open by severity · closed that day · net change

#### 4.6.3 Automation Pass Rate Sparklines

**Layout:** `grid grid-cols-3 gap-3`

| Test Suite | Pass Rate | 7-day Sparkline |
|---|---|---|
| Unit Tests | 98.2% | green sparkline |
| Integration Tests | 94.7% | green sparkline |
| E2E Tests | 87.3% | amber sparkline |
| API Contract Tests | 99.1% | green sparkline |
| Performance Tests | 72.4% | red sparkline |
| Accessibility Tests | 81.0% | amber sparkline |

Each row: `flex justify-between items-center bg-[#0D1526] rounded-lg p-3`
Sparkline: 20px height SVG inline path

---

### 4.7 Tab: Adoption

**Purpose:** How widely are features being used across 2,050 institutions?

#### 4.7.1 Adoption Overview Filters

| Control | Type | Options |
|---|---|---|
| Institution Type | Multi-select | All · School · College · Coaching · Group |
| Plan Tier | Multi-select | Starter · Standard · Professional · Enterprise |
| Date Range | Dropdown | Last 30d · 90d · 6M · 12M |
| Feature Category | Dropdown | Exam · Content · Analytics · Communication · Billing · All |

#### 4.7.2 Feature Adoption Funnel

**Canvas id:** `adoption-funnel-chart` · height 280px

Stages (top to bottom, narrowing):
1. Feature available to institution (plan entitlement)
2. Feature enabled in institution settings
3. Feature used at least once
4. Feature used weekly (active adoption)
5. Feature is primary workflow (power user)

Colour: `#6366F1` with 20% opacity decrease per stage
Hover tooltip: count + % at each stage

#### 4.7.3 Top Feature Adoption Table

**Columns:**

| Column | Detail |
|---|---|
| # | Rank |
| Feature | Feature name + category badge |
| Eligible Institutions | Count with plan entitlement |
| Adopted | Count using feature · % of eligible |
| Weekly Active | Count using weekly |
| MoM Change | +/- % with colour |
| Trend | 4-week sparkline |
| Lagging Institution Types | Which types have lowest adoption |

**Sort:** Adopted % desc by default
**Pagination:** 25/page
**Row click:** opens Feature Adoption Drawer (480px) — shows breakdown by institution type, adoption timeline chart, top institutions using feature, bottom institutions not yet adopted

---

## 5. Drawers

### 5.1 Release Detail Drawer (640px)

**Trigger:** Release card click in Release Health tab or KPI card click
**Header:** Release version badge + Release name + Status badge + `[×]` close

**Tab bar (5 tabs):**

**Tab A — Summary:**
- Target date · Actual deploy date · Cycle time · Items count
- Description: `text-sm text-[#94A3B8]`
- Risk level badge: Low / Medium / High / Critical

**Tab B — Changelog:**
- Grouped by type: Features · Bug Fixes · Performance · Security
- Each item: `● [JIRA-ID] Title — [module badge]`
- Breaking changes section with `⚠` banner: `bg-[#1A0A0A] border border-[#EF4444]`

**Tab C — Flags Deployed:**
Table of all feature flags included in this release:
| Flag Key | Status Change | Rollout % | Owner |

**Tab D — QA Sign-off:**
- Checklist of required sign-offs with status: ✓ / ✗ / ⏳
- QA lead name + sign-off timestamp
- Open blockers list
- [Mark as QA Approved] button (QA role only, 2FA)

**Tab E — Rollback:**
- `bg-[#1A0A0A] border border-[#EF4444] rounded-xl p-4`
- Last stable version badge
- Rollback impact summary: "Will affect 120 flags, 3 DB migrations"
- [Initiate Rollback] button — opens Rollback Confirmation Modal (2FA required)

**Footer:** [Edit Release] · [View in Roadmap] · [Close]

---

### 5.2 Flag Detail Drawer (560px)

**Trigger:** Flag tile click in Flag Health tab
**Header:** Flag key `font-mono` + Flag name + Status badge + `[×]`

**Tab bar (4 tabs):**

**Tab A — Config:**
- Flag key (read-only) · Flag name · Description
- Status toggle: Enabled / Disabled (2FA required for kill-switch)
- Rollout %: slider `0–100` with live preview count: "Affects ~X institutions"
- Rollout strategy: All institutions · By type · By plan · Specific list
- Kill-switch button (red): `bg-[#450A0A] border border-[#EF4444] text-[#F87171]`

**Tab B — Overrides:**
Table of per-institution overrides:
| Institution | Type | Override | Set by | Set on |
- [Add Override] button → mini modal (search institution + toggle)
- [Remove] per row

**Tab C — History:**
Timeline of all changes: who · what · when
Each event: `● [actor] changed [field] from [old] to [new] — [timestamp]`

**Tab D — Dependencies:**
- Flags this flag depends on (must be enabled first)
- Flags that depend on this flag
- Dependency graph: small SVG tree diagram
- Conflict warnings: red if circular dependency

**Footer:** [Save Changes] (2FA for publish/kill) · [Deprecate Flag] · [Close]

---

### 5.3 Feature Adoption Drawer (480px)

**Trigger:** Row click in Adoption tab table
**Header:** Feature name + Category badge

**Section A — Adoption Breakdown by Institution Type:**
Horizontal bar chart per type (School / College / Coaching / Group)
Values: eligible count · adopted count · adoption %

**Section B — Adoption Timeline (12 months):**
Line chart: monthly adoption % trend · `#6366F1` line

**Section C — Top 10 Adopters:**
Table: Institution name · type · first used · usage frequency

**Section D — Not Yet Adopted (bottom 10 eligible):**
Table: Institution name · plan · days since eligible · last login
[Send Re-engagement Notice] button per row

**Footer:** [Export CSV] · [Close]

---

## 6. Modals

### 6.1 Customize Dashboard Modal

**Trigger:** [Customize ▾] header button
**Width:** 520px

**Content:**
- Drag-and-drop panel order: `cursor-grab` each panel card
- Toggle visibility per panel (checkboxes)
- Default date range setting
- Poll interval override (30s / 60s / 120s / Off)

**Footer:** [Save Layout] · [Reset to Default] · [Cancel]

---

### 6.2 Rollback Confirmation Modal

**Trigger:** [Initiate Rollback] in Release Detail Drawer Tab E
**Width:** 540px
**Style:** `bg-[#1A0A0A] border border-[#EF4444]`

**Content:**
- ⚠ Warning heading: `text-[#EF4444] text-lg font-bold`
- "Rolling back to v2.3.2 will:"
  - [ ] Revert 8 DB migrations (data loss risk)
  - [ ] Disable 3 feature flags
  - [ ] Affect 2,050 active institutions
- Type rollback reason: `textarea` required
- 2FA verification field: `input type="text" placeholder="Enter 6-digit code"`

**Footer:** [Confirm Rollback] `bg-[#EF4444]` · [Cancel]

---

## 7. Django View

```python
# portal/apps/product/views.py

class ProductDashboardView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "portal.view_product_dashboard"

    def get(self, request):
        ctx = self._build_context(request)
        if _is_htmx(request):
            part = request.GET.get("part", "")
            templates = {
                "kpi":            "product/partials/dashboard_kpi.html",
                "overview":       "product/partials/dashboard_overview.html",
                "release_health": "product/partials/dashboard_release_health.html",
                "flag_health":    "product/partials/dashboard_flag_health.html",
                "qa_summary":     "product/partials/dashboard_qa_summary.html",
                "adoption":       "product/partials/dashboard_adoption.html",
                "feed":           "product/partials/dashboard_feed.html",
                "flag_drawer":    "product/partials/flag_drawer.html",
                "release_drawer": "product/partials/release_drawer.html",
                "adoption_drawer":"product/partials/adoption_drawer.html",
                "staging_checks": "product/partials/staging_checks.html",
            }
            if part in templates:
                return render(request, templates[part], ctx)
        return render(request, "product/dashboard.html", ctx)

    def _build_context(self, request):
        from django.core.cache import cache
        ctx = {}
        # KPI data — Redis-cached 60s
        ctx["kpi"] = cache.get_or_set(
            "product:dashboard:kpi",
            lambda: self._compute_kpi(),
            60
        )
        # Activity feed — Redis-cached 30s
        ctx["feed"] = cache.get_or_set(
            "product:dashboard:feed",
            lambda: self._compute_feed(),
            30
        )
        return ctx

    def _compute_kpi(self):
        from portal.apps.product.models import FeatureFlag, Release, Defect, TestTenant, ABTest
        return {
            "active_flags":    FeatureFlag.objects.filter(status="enabled").count(),
            "partial_flags":   FeatureFlag.objects.filter(status="partial").count(),
            "next_release":    Release.objects.filter(status="staging").order_by("target_date").first(),
            "open_defects":    Defect.objects.filter(status__in=["open","in_progress"]).count(),
            "p0_defects":      Defect.objects.filter(status="open", severity="P0").count(),
            "test_tenants":    TestTenant.objects.filter(active=True).count(),
            "ab_tests":        ABTest.objects.filter(status="running").count(),
            "adoption_rate":   self._compute_adoption_rate(),
        }
```

---

## 8. Empty States

| Section | Empty State Copy | Illustration |
|---|---|---|
| Activity Feed | "No recent activity. Actions taken by your team will appear here." | Empty inbox icon `text-[#475569]` |
| Flag Health | "No flags configured yet. Create your first feature flag." | Toggle off icon |
| QA Blockers | "No blockers for this release. QA looks good! 🎉" | Checkmark shield |
| Release Pipeline | "No releases in pipeline. Create a new release to get started." | Rocket icon |
| Adoption Table | "No adoption data available for selected filters." | Bar chart empty |

---

## 9. Error States

| State | Display |
|---|---|
| Network error on poll | Amber banner: "Unable to refresh data. Retrying in 30s." · `bg-[#451A03] border border-[#F59E0B]` |
| Permission denied | `403` card: "You do not have permission to view this section." |
| Data load failure | Red inline error per section: "Failed to load [section]. [Retry]" |
| Stale data | "Data last updated Xm ago" timestamp in `text-[#475569] text-xs` |

---

---

## G5 Amendment — Critical Alert Bus (Shared Across All Division B Pages)

### Purpose

When a P0 production incident fires — a kill-switch is activated, a performance SLA breach is detected at 74K concurrent users, a P0 defect opens, or a Lambda Lambda cold-start cascade begins — every team member working in any Division B page must be immediately aware. Without this, a PM editing a roadmap card in page 05 has no idea the platform is in crisis.

The Critical Alert Bus is a **server-side SSE (Server-Sent Events) stream** that delivers real-time platform alerts to all Division B pages simultaneously. It is implemented as a shared component included in the base template for all Division B pages.

---

### Alert Banner Behaviour

**Position:** Fixed top of page, above the navigation bar. Full-width. Z-index: 9999.

**Style by severity:**

| Severity | Background | Border | Icon | Example |
|---|---|---|---|---|
| P0 — Critical | `bg-[#450A0A]` | `border-b border-[#EF4444]` | 🔴 | Lambda cold-start cascade · active exam data loss risk |
| P1 — High | `bg-[#451A03]` | `border-b border-[#F59E0B]` | 🟡 | Kill-switch fired · performance SLA breached |
| Info | `bg-[#0C1A2E]` | `border-b border-[#3B82F6]` | 🔵 | Scheduled maintenance in 30 minutes |

**Banner content:**
```
🔴  [P0] Lambda cold-start cascade detected — 74K exam submissions impacted.
    Incident: INC-2026-03-20-001  ·  Open since: 14:32  ·  [View Incident →]  [Dismiss ✕]
```

- **[View Incident →]**: opens Defect Tracker (page 25) filtered to this incident
- **[Dismiss ✕]**: hides the banner for the current user's session only. The alert still exists — other users still see it. Cannot be dismissed for P0 alerts (the × is disabled for P0).

**Multiple alerts:** If 2+ alerts are active, a stacked banner with a counter shows: "2 active alerts" with an expand chevron to show all.

---

### Alert Source — `platform_alerts` Redis Key

A single Redis sorted set: `platform_alerts` holds all active alerts, scored by creation timestamp.

Alerts are written to this key by:
- Defect Tracker (page 25): when a P0 or P1 defect is created or escalated
- Automation Monitor (page 26): when a CI/CD gate fails blocking a release
- Performance Test Dashboard (page 24): when SLA thresholds are breached
- Feature Flags (page 02): when a kill-switch is activated
- External monitoring (PagerDuty/CloudWatch): via webhook into the platform

An alert entry contains: `alert_id · severity · title · body · source_page · incident_url · created_at · auto_expire_at`.

**Auto-expiry:** P1/Info alerts auto-expire after 4 hours. P0 alerts never auto-expire — they must be manually resolved by the creator (with a "Resolve Alert" button available only to the PM Platform and QA Lead roles).

---

### SSE Stream Endpoint

`GET /api/v1/platform-alerts/stream/` — Returns `text/event-stream`.

Each event:
```
event: alert
data: {"alert_id": "ALT-001", "severity": "P0", "title": "...", "body": "...", "source": "defect-tracker"}
```

All authenticated Division B pages subscribe to this stream on page load. If the SSE connection drops, the client falls back to polling `GET /api/v1/platform-alerts/` every **60 seconds**.

**Guard:** Poll/SSE is paused while `document.querySelector('.modal-open,.drawer-open')` is true — the alert banner still shows if already loaded, but no new fetch is triggered during modal interactions.

---

### War Room Integration

The Product Dashboard (this page) has an additional capability: when a P0 alert is active, a **[Open War Room →]** button appears inside the alert banner. This links to the War Room page (`/product/war-room/` — see page 32 of Division A or a future Division B page) where all stakeholders coordinate the incident response.

If a War Room page does not exist yet, the button links to the Incident Manager in Division A (`/dashboard/incidents/`).

---

### Role-Based Alert Visibility

| Role | Sees Alert Banner | Can Dismiss | Can Resolve Alert | Can Create Alert Manually |
|---|---|---|---|---|
| PM Platform | ✅ | P1/Info only | ✅ | ✅ |
| PM Exam Domains | ✅ | P1/Info only | — | — |
| PM Institution Portal | ✅ | P1/Info only | — | — |
| UI/UX Designer | ✅ | P1/Info only | — | — |
| QA Engineer | ✅ | P1/Info only | ✅ | ✅ |

---

### Pages Where This Banner Appears

The Critical Alert Bus banner appears on all Division B pages:
01, 02, 03, 04, 05, 06, 07, 08, 09, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28

It is included in the base Division B layout template — no per-page implementation needed beyond the shared component.

---

## 10. Keyboard Shortcuts

| Shortcut | Action |
|---|---|
| `G D` | Go to Dashboard (this page) |
| `G F` | Go to Feature Flags |
| `G R` | Go to Release Manager |
| `G Q` | Go to QA Dashboard |
| `1–5` | Switch between tabs (Overview/Release/Flags/QA/Adoption) |
| `Esc` | Close open drawer or modal |
| `R` | Refresh current tab data |
| `/` | Focus search / filter input |

---

## 11. Responsive Behaviour

| Viewport | Layout Change |
|---|---|
| ≥ 1440px | Full 2-column layout |
| 1024–1439px | 2-column with narrower columns |
| 768–1023px | Single column; charts full width |
| < 768px | KPI strip scrolls horizontally; tabs scroll horizontally |

---

## 12. Performance Considerations

- **KPI strip:** Redis-cached 60s — never hits DB on poll
- **Activity feed:** Redis stream or DB with index on `created_at DESC` — max 50 rows fetched
- **Flag health:** Materialized count from Redis `HGETALL product:flags:status` — O(1)
- **QA summary:** Module health scores pre-computed by Celery beat every 5 min
- **Adoption metrics:** Nightly Celery aggregate job — never live COUNT on 2.4M student events
- **Chart data:** All chart datasets included in initial page context — no secondary HTMX call on first load
