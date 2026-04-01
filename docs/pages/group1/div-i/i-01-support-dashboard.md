# I-01 — Support Dashboard

**Route:** `GET /support/`
**Method:** Django CBV (`TemplateView`) + HTMX part-loads
**Primary role:** Support Manager (#47)
**Also sees (restricted view):** L1 (#48), L2 (#49), L3 (#50), Support Quality Lead (#108), Onboarding Specialist (#51)

---

## Purpose

Real-time health dashboard for the support operation. Surfaces active SLA risk, ticket volume trends, team workload, and quality metrics in a single view. During live exams, becomes the war-room command centre for the support team.

---

## Data Sources

| Section | Source |
|---|---|
| KPI strip | Live query on `support_ticket` (no cache — SLA timers must be real-time) |
| Ticket volume chart | `support_ticket` grouped by `created_at::date` + category; 2-min Memcached TTL |
| SLA compliance gauges | `support_ticket` aggregated; 2-min Memcached TTL |
| Team workload table | `support_ticket` grouped by `assigned_to_id`; 2-min TTL |
| Quality metrics panel | `support_quality_audit` + `support_ticket.csat_score`; 5-min TTL |
| Escalation feed | `support_ticket_escalation` last 24h; 1-min TTL |
| Onboarding pipeline strip | `onboarding_instance` stage counts; 5-min TTL |

---

## URL Parameters

| Param | Values | Effect |
|---|---|---|
| `?nocache=true` | — | Bypasses Memcached; Support Manager only |
| `?view=exam_day` | — | Expands exam-day panel to full screen; active only if exam is live |

---

## HTMX Part-Load Routes

| Part | Route | Trigger |
|---|---|---|
| KPI strip | `?part=kpi` | Page load + auto-refresh every 60s |
| Volume chart | `?part=volume_chart` | Page load + manual refresh |
| SLA gauges | `?part=sla_gauges` | Page load + auto-refresh every 2 min |
| Workload table | `?part=workload` | Page load + auto-refresh every 2 min |
| Quality panel | `?part=quality` | Page load |
| Escalation feed | `?part=escalations` | Page load + auto-refresh every 60s |
| Onboarding strip | `?part=onboarding` | Page load |
| Exam day banner | `?part=exam_banner` | Page load; auto-refresh every 30s via `hx-trigger="every 30s"`; if exam ends mid-session, banner returns empty HTML on next refresh (HTMX removes element); triggers the banner disappearance without full page reload |
| Exam day live feed | `?part=exam_live_feed` | `?view=exam_day` only; auto-refresh every 15s |

---

## Page Layout

```
┌─────────────────────────────────────────────────────────────┐
│  [EXAM DAY BANNER — shown only when exam is live]           │
├─────────────────────────────────────────────────────────────┤
│  KPI STRIP (5 tiles)                                        │
├──────────────────────────┬──────────────────────────────────┤
│  VOLUME CHART (7-day)    │  SLA COMPLIANCE GAUGES (3)       │
├──────────────────────────┴──────────────────────────────────┤
│  TEAM WORKLOAD TABLE                                        │
├────────────────────────────┬────────────────────────────────┤
│  RECENT ESCALATIONS FEED   │  QUALITY & CSAT PANEL          │
├────────────────────────────┴────────────────────────────────┤
│  ONBOARDING PIPELINE STRIP                                  │
└─────────────────────────────────────────────────────────────┘
```

---

## Components

### Exam Day Banner (conditional)

Shown when any exam in `exam` table has `status=LIVE` (checked at page load).

```
┌─────────────────────────────────────────────────────────────────┐
│  🔴 EXAM LIVE: "SSC CGL Mock 12 — Phase 1"                      │
│  Students active: 41,200 · CRITICAL tickets: 7 · IN_PROGRESS: 4│
│  [View Exam-Day Tickets →]    [Exam Day Mode ↗]                 │
└─────────────────────────────────────────────────────────────────┘
```

- Background: red-50 border-red-400
- CRITICAL ticket count refreshes every 30s via HTMX poll (standalone `?part=exam_banner` route)
- [View Exam-Day Tickets →] links to `/support/tickets/?exam_day=true&priority=CRITICAL`
- [Exam Day Mode ↗] links to `?view=exam_day` — full-page overlay (see below)

**Exam Day Mode overlay** (`?view=exam_day`):

Replaces normal dashboard content entirely. Full-page two-panel layout:

```
┌───────────────────────────────────────────────────────────────────┐
│  🔴 EXAM DAY WAR ROOM · SSC CGL Mock 12 · 41,200 students live   │
│  [← Normal View]   Running: 1h 24m   Ends at: 14:00 IST          │
├──────────────────────────┬────────────────────────────────────────┤
│  LIVE TICKET FEED        │  STATS PANEL                           │
│  (auto-refreshes 15s)    │  Open CRITICAL: 12                     │
│                          │  In Progress: 8                         │
│  SUP-…-000347 CRITICAL   │  Resolved (exam day): 3                │
│  "Exam session expired"  │  Avg first response: 4m                │
│  L2 · Priya · 4m ago     │  SLA at risk: 2                       │
│                          │  SLA breached: 0                       │
│  SUP-…-000341 CRITICAL   │                                        │
│  "OTP not received"      │  TEAM STATUS                           │
│  L1 · Unassigned · 7m    │  L1 on duty: 4 agents                 │
│  [Assign →]              │  L2 on duty: 2 agents                 │
│                          │  L3 on duty: 1 agent                  │
│  SUP-…-000338 HIGH       │                                        │
│  "Result not visible"    │  SURGE STATUS                          │
│  L1 · Rahul · 12m        │  ● Normal (< 200 CRITICAL open)       │
│                          │  [Activate Triage Mode ▼]             │
└──────────────────────────┴────────────────────────────────────────┘
```

- Live ticket feed: scrollable; shows top 20 unresolved exam-day tickets sorted by SLA soonest first; auto-refreshes every 15s via `?part=exam_live_feed`
- Each feed item: ticket number, subject (truncated), tier, assigned agent or "Unassigned" (red), time since creation; clicking opens I-03
- [Assign →] shown only for unassigned tickets; Support Manager assigns from inline mini-form (agent picker dropdown, no modal)
- Stats panel refreshes every 30s; team status shows agent count per tier based on who has actively assigned tickets in the last 30 min
- Surge Status: shows "Normal" (green), "Elevated (>200 open)" (amber), "Surge (>500 open)" (red pulsing); [Activate Triage Mode] button available to Support Manager at any surge level
- Exam day mode only accessible to Support Manager (#47); all other roles are redirected to `/support/tickets/?exam_day=true` instead

---

### KPI Strip (5 tiles)

| Tile | Value | Colour logic |
|---|---|---|
| Open Tickets | COUNT status NOT IN (RESOLVED, CLOSED) | Grey (normal), amber (>200), red (>500) |
| SLA at Risk | COUNT where `sla_breach_at BETWEEN now() AND now() + interval '1 hour'` AND open | Amber (>0), red (>10) |
| Breached SLAs | COUNT open tickets where `sla_breach_at < now()` | Green (0), red (any) |
| CSAT This Week | AVG `csat_score` for tickets closed this week | Red (<3.5), amber (3.5–4.0), green (≥4.0) |
| Unassigned | COUNT open tickets where `assigned_to_id IS NULL` | Green (0), amber (>5), red (>20) |

Each tile is clickable and links to I-02 pre-filtered:
- "Open Tickets" → `/support/tickets/?status=OPEN,IN_PROGRESS`
- "SLA at Risk" → `/support/tickets/?sla_status=AT_RISK`
- "Breached SLAs" → `/support/tickets/?sla_status=BREACHED`
- "Unassigned" → `/support/tickets/?assigned=unassigned`

---

### Volume Chart (7-day Ticket Trend)

Chart type: **Stacked bar chart** (Chart.js). X-axis: last 7 days (today + 6 prior). Y-axis: ticket count.

Stacked series (by tier):
- L1 — blue
- L2 — orange
- L3 — red

Hover tooltip: shows total + breakdown by tier for that day.

Below the chart: category breakdown for selected day (pie chart, shows on bar click).

Filter controls (above chart):
- Date range picker: default last 7 days; options: 7d / 14d / 30d / 90d
- [Refresh] button; [Export CSV] — downloads raw ticket volume data

Support Manager (#47) only: shows team picker to filter by assigned agent.

---

### SLA Compliance Gauges

Three circular gauge charts (Chart.js doughnut), one per tier.

Each gauge shows:
- Percentage of tickets in that tier that met resolution SLA in the rolling 7-day window
- Target thresholds: L1 ≥ 95%, L2 ≥ 90%, L3 ≥ 85%
- Colour: green (≥ target), amber (within 5% below target), red (>5% below target)

Below each gauge: small stat row showing:
- Total tickets this period
- Met SLA count
- Breached count
- Avg resolution time

---

### Team Workload Table

Columns: Agent Name | Tier | Open | In Progress | Pending Customer | Breached | Avg Resolution (7d) | CSAT (7d)

Sorted by: Open tickets desc (default). Click column header to re-sort.

Row actions (Support Manager only):
- [Assign ticket] — opens mini-modal with unassigned ticket list; click to assign to this agent
- [View agent queue →] — links to I-02 pre-filtered to this agent

Agents with 0 open tickets: shown in grey italic.
Agents who have been unresponsive for >2h during business hours: amber highlight.

Role-limited views:
- L1/L2/L3 agents see only their own row (not full team)
- Support Quality Lead (#108) sees full table (read-only, no assign action)

---

### Recent Escalations Feed

Shows last 20 escalations in chronological order (newest first).

Each entry:
```
▲ L1 → L2 · Ticket #SUP-20241105-000342 · "Student can't join exam"
   Escalated by: Priya (L1) · 14 min ago · Reason: Technical investigation needed
   [View Ticket →]
```

Colour-coded badge: L1→L2 = orange, L2→L3 = red.

L3 escalations always shown to Support Manager with priority banner.

---

### Quality & CSAT Panel

Two sub-sections:

**CSAT Trend (mini chart)**
Line chart: daily average CSAT score for last 30 days. Target line at 4.0.
If CSAT drops below 3.5 for 3 consecutive days → red alert banner.

**Audit Queue (Support Quality Lead / Support Manager only)**
Count of tickets pending quality audit (tickets resolved within last 14 days, `quality_audit_score IS NULL`).
Random sample size shown: "12 tickets sampled for audit this week (25% of resolved)"
[Start Auditing →] links to `/support/tickets/?status=RESOLVED,CLOSED&quality_audit_pending=true` — this filter shows tickets resolved within the last 14 days with no quality audit score recorded yet (see I-02 `?quality_audit_pending=true` URL param).

Role visibility:
- Support Manager: sees both sections
- Support Quality Lead (#108): sees both sections
- L1/L2/L3: see only their own CSAT row (not full panel)

---

### Onboarding Pipeline Strip

A horizontal stage-progress summary bar with counts per stage.

```
INITIATED (3) → SETUP CALL (5) → PORTAL CONFIG (8) → ADMIN TRAINED (4) → FIRST EXAM (2) → LIVE (12) → COMPLETED (1,987)
```

STALLED count shown in red below the strip: "⚠ 2 stalled"

[View Full Tracker →] links to I-05.

Visible to: Support Manager, Onboarding Specialist. Hidden for L1/L2/L3/Training Coordinator.

---

## Role-Based View Differences

| Component | Support Manager (#47) | L1 (#48) / L2 (#49) / L3 (#50) | Quality Lead (#108) | Onboarding Spec (#51) |
|---|---|---|---|---|
| Exam Day Banner | Full | Full | Full | Hidden |
| KPI Strip | All 5 tiles | Own-queue tiles only (Open in my tier, My SLA at risk) | All 5 (read-only) | **Hidden** — Onboarding Specialist has no ticket KPIs; they see the Onboarding Pipeline Strip below instead |
| Volume Chart | Full + agent filter | Hidden | Full (read-only) | Hidden |
| SLA Gauges | All 3 tiers | Own tier only | All 3 (read-only) | Hidden |
| Workload Table | Full team | Own row only | Full team (read-only) | Hidden |
| Escalation Feed | Full | Only escalations involving own tickets | Full (read-only) | Hidden |
| Quality Panel | Full | Hidden | Full | Hidden |
| Onboarding Strip | Full | Hidden | Hidden | Full |

---

## Edge Cases

1. **No open tickets** — KPI strip tiles show 0; workload table shows "All queues clear" empty state with green checkmark. Volume chart still shows history.
2. **All L1 agents offline** (0 open assignments) — system alert in workload table: "⚠ No L1 agent has an active ticket. Unassigned queue growing." with [Assign Now →].
3. **CSAT data < 7 days** (new platform deployment) — CSAT gauge shows "Insufficient data (N responses)" rather than 0%.
4. **Exam day banner persistence** — if exam ends mid-page-view, banner disappears on next HTMX refresh (60s). Page does not force reload.
5. **Support Manager `?nocache=true`** — all 8 part-load routes bypass Memcached; page may load 2–3s slower during peak — loader spinner shown per section.
6. **Multiple concurrent live exams** — exam day banner shows the exam with the most CRITICAL tickets; "and 2 more" expandable list below.

---

## Notifications

All notifications via F-06:
- SLA breach (any ticket) → push to assigned agent + Support Manager
- 3+ CRITICAL tickets open simultaneously during exam → push to Support Manager + L2/L3 leads
- CSAT score drops below 3.0 → push to Support Manager
- Zero agents assigned for >30 min during business hours → push to Support Manager
