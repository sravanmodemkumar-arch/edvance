# 38 — Support Operations

---

## 1. Page Metadata

| Field | Value |
|---|---|
| Page title | Support Operations |
| Route | `/exec/support-ops/` |
| Django view | `SupportOpsView` |
| Template | `exec/support_ops.html` |
| Priority | **P1** |
| Nav group | Operations |
| Required roles | `coo` · `support_manager` · `ceo` · `superadmin` |
| L1/L2/L3 Support | Denied (they use their own support dashboard) |
| CTO / CFO | Denied |
| HTMX poll — summary strip | Every 60s |
| HTMX poll — ticket table | Every 120s |
| Cache | Summary: Redis TTL 55s · Ticket data: Redis TTL 115s |
| Theme tokens | bg-base `#040810` · surface-1 `#08101E` · accent `#6366F1` · danger `#EF4444` · warn `#F59E0B` · success `#22C55E` |

---

## 2. Purpose & Business Logic

**The COO's support visibility problem:**

EduForge's support team handles tickets from 2,050 institutions across L1 (login/OTP/navigation), L2 (bug investigation), and L3 (code-level fixes). The COO currently has no single view showing:
- How many tickets are open right now, and are they within SLA?
- Which institutions are generating the most tickets? (high volume = unhappy customer, churn risk signal)
- Which agents are overloaded? (uneven distribution → slower resolution)
- What are the top issue categories this week? (recurring issues → product/engineering fix needed)

**SLA commitments by tier:**

| Tier | L1 Response | L2 Response | L3 Response |
|---|---|---|---|
| Standard (Schools) | < 4 hours | < 24 hours | < 72 hours |
| Professional (Colleges) | < 2 hours | < 12 hours | < 48 hours |
| Enterprise (Coaching) | < 1 hour | < 8 hours | < 24 hours |

A single Enterprise coaching centre SLA breach = Rs.X credit obligation + churn risk.

---

## 3. User Roles & Access

| Role | Can View | Can Act |
|---|---|---|
| CEO | All sections | Read-only |
| COO | All sections | Reassign ticket, change priority, close ticket, export |
| Support Manager | All sections | All ticket management actions |
| CFO | No access | Redirect |
| CTO | No access | Redirect |
| L1/L2/L3 Support | No access | They have own support dashboard (not Division A) |

---

## 4. Section-wise UI Breakdown

---

### Section 1 — Summary Strip

**Purpose:** Instant operational pulse — how many tickets, what's breaching SLA, which tier is worst.

**UI elements — 6 cards:**

```
╔══════════════╦══════════════╦══════════════╦══════════════╦══════════════╦══════════════╗
║ OPEN TICKETS ║ SLA BREACH   ║ AVG RESPONSE ║ RESOLVED 24h ║ ESCALATION   ║ BACKLOG      ║
║              ║              ║ TIME         ║              ║ RATE         ║ TREND        ║
║     284      ║  12 🔴       ║  1h 42m      ║    148       ║    4.2%      ║  ▲ +18 WoW   ║
║  L1:192 L2:72║  Enterprise:8 ║  SLA: < 2h   ║              ║              ║  3 wk streak ║
╚══════════════╩══════════════╩══════════════╩══════════════╩══════════════╩══════════════╝
```

| Card | Alert |
|---|---|
| Open Tickets | > 300: amber · > 500: red |
| SLA Breach | Any > 0: amber · > 10: red |
| Avg Response Time | > SLA tier average: amber |
| Resolved 24h | < 50% of opened yesterday: amber |
| Escalation Rate | > 10%: amber |
| Backlog Trend | Growing > 3 weeks: red |

**HTMX:** `id="support-summary"` `hx-trigger="load, every 60s"` — Redis cache.

---

### Section 2 — Ticket Volume Chart

**Purpose:** 30-day trend of tickets opened vs resolved. Rising "opened" line = growing problem. Converging lines = team catching up.

**UI elements:**
- Chart.js Line, full width, 180px tall
- Series 1: Opened (daily) — `#EF4444` line
- Series 2: Resolved (daily) — `#22C55E` line
- Area fill between lines: red fill when opened > resolved (backlog growing), green fill when resolved > opened
- X-axis: last 30 days, tick every 3 days
- Tooltip: "Mar 15: Opened 28 · Resolved 34 · Net: -6 (improving)"

**HTMX:** `id="ticket-trend-chart"` `hx-trigger="load"` `hx-swap="innerHTML"` (no poll — daily data).

---

### Section 3 — SLA Breach Tracker

**Purpose:** Every breached SLA is a potential credit obligation and churn risk. COO must see all open breaches with time elapsed.

**UI elements:**
```
SLA BREACHES (OPEN)                                    [Export Breaches]
──────────────────────────────────────────────────────────────────────────────
Ticket ID   │Institution        │Tier       │Level│Opened      │Elapsed │Agent
────────────┼───────────────────┼───────────┼─────┼────────────┼────────┼──────
TKT-2026-884│ABC Coaching       │Enterprise │ L2  │2h ago      │+1h SLA │Rahul G.
TKT-2026-871│XYZ Coaching       │Enterprise │ L1  │4h ago      │+3h SLA │Unassigned
TKT-2026-856│DEF School Group   │Professional│L2  │6h ago      │+2h SLA │Priya M.
```

- "Elapsed" = time beyond SLA. Red. Pulsing if > 2× SLA time.
- "Unassigned" agent = red badge
- Click row → opens Ticket Detail Drawer (460px)
- [Export Breaches] → CSV with institution name, contact, ticket details — for SLA credit calculation

**HTMX:** `id="sla-breach-table"` `hx-trigger="load, every 60s"` — query `SupportTicket.objects.filter(sla_breached=True, status__in=['open','in_progress'])`.

---

### Section 4 — Agent Performance Table

**Purpose:** COO identifies overloaded agents and rebalances ticket distribution.

**UI elements:**
```
AGENT PERFORMANCE                                     [Period: This Week ▾]
──────────────────────────────────────────────────────────────────────────────
Agent        │Level│Open │Resolved│Avg Resolution│SLA Met%│Satisfaction
─────────────┼─────┼─────┼────────┼──────────────┼────────┼────────────
Rahul G.     │ L2  │  18 │   42   │   6h 20m     │ 88.1%  │  4.2/5 ⭐
Priya M.     │ L2  │  24 │   38   │   7h 12m     │ 82.4%  │  4.0/5 ⭐
Kiran S.     │ L1  │  42 │   61   │   1h 08m     │ 94.2%  │  4.5/5 ⭐
Unassigned   │  —  │  12 │   —    │   —          │  —     │  —
```

- "Open" column: red if > 20 for L2, red if > 30 for L1
- "Unassigned" row at bottom: COO can click → bulk-assigns to selected agent
- Click agent name → drill-down drawer with their individual ticket list

**Period filter:** This Week / Last Week / This Month. Changes all agent stats.

---

### Section 5 — Top Issue Categories

**Purpose:** Identify recurring issues that need product/engineering fix (not individual ticket resolution).

**UI elements:**
```
TOP ISSUE CATEGORIES — Last 30 Days                   [View All →]
─────────────────────────────────────────────────────────────────────
Category                  Count    % of Total   Trend vs last month
OTP / Login issues          84      29.6%        ▼ -12% (improving)
Exam submission errors      48      16.9%        ▲ +38% (worsening) ⚠
Report download failures    32      11.3%        ▲ +15%
Password reset issues       28       9.9%        → same
Slow page load / timeout    24       8.5%        ▲ +22% ⚠
Other                       68      24.0%        —
```

- Worsening categories (MoM increase > 20%): amber text + ⚠ badge
- "Exam submission errors up 38%" → COO flags to Engineering (link to create incident or Slack mention)
- Horizontal bar chart variant below table: same data visually

**HTMX:** `id="issue-categories"` `hx-trigger="load"` (no poll — batch data).

---

### Section 6 — Institutions with Most Open Tickets

**Purpose:** Cross-reference with Customer Health (page 35). High ticket volume = unhappy institution = churn risk.

**UI elements:**
```
INSTITUTIONS — MOST OPEN TICKETS
──────────────────────────────────────────────────────────────────────────────
Institution       │Type    │Open│SLA Breach│Health Score│CSM
──────────────────┼────────┼────┼──────────┼────────────┼────────────
XYZ Coaching      │Coaching│ 12 │    3     │   38 🔴    │Unassigned
ABC School Group  │Group   │  8 │    1     │   52 🟠    │Ravi K.
DEF College       │College │  6 │    0     │   71 🟡    │Priya M.
```

- Health Score column links to Customer Health page drill-down (Drawer-I)
- "Unassigned CSM" on high-ticket institution: red badge — COO can click to assign directly from here

Top 10 institutions only. "View all in Customer Health →" link.

---

## 5. Full Page Wireframe

```
╔══════════════════════════════════════════════════════════════════════════════╗
║  Support Operations                                   [↺ Refresh]           ║
╠══════════╦══════════╦══════════╦══════════╦══════════╦══════════════════════╣
║ OPEN     ║ SLA BREACH║ AVG RESP ║ RESOLVED ║ ESC RATE ║ BACKLOG TREND        ║
║   284    ║  12 🔴   ║ 1h 42m   ║   148    ║  4.2%    ║ ▲ +18 WoW            ║
╠══════════╩══════════╩══════════╩══════════╩══════════╩══════════════════════╣
║  TICKET VOLUME — Last 30 Days                                                ║
║  [Chart: Opened(red) vs Resolved(green)]                                     ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  SLA BREACHES (OPEN)                               [Export Breaches]        ║
║  TKT-884 │ ABC Coaching │ Enterprise │ L2 │ +1h over SLA │ Rahul G.         ║
║  TKT-871 │ XYZ Coaching │ Enterprise │ L1 │ +3h over SLA │ ⚠ Unassigned     ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  AGENT PERFORMANCE  [This Week ▾]     TOP ISSUE CATEGORIES (30d)            ║
║  Rahul G.  L2  18 open  88.1% SLA    OTP/Login        84  ▼ improving       ║
║  Priya M.  L2  24 open  82.4% SLA    Exam submit err  48  ▲ +38% ⚠          ║
║  Kiran S.  L1  42 open  94.2% SLA    Report download  32  ▲ +15%            ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  INSTITUTIONS — MOST OPEN TICKETS                                           ║
║  XYZ Coaching  │ 12 open │ 3 SLA breach │ Health: 38 🔴 │ Unassigned CSM    ║
║  ABC School Gr │  8 open │ 1 SLA breach │ Health: 52 🟠 │ Ravi K.           ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 6. Ticket Detail Drawer (460px)

```
┌──────────────────────────────────────────────────────┐
│  TKT-2026-884                  🔴 SLA Breach +1h [✕] │
│  ABC Coaching · Enterprise · L2                       │
│  ─────────────────────────────────────────────────── │
│  Issue: Exam submission errors on Safari              │
│  Opened: 2h ago by admin@abc-coaching.com             │
│  Agent: Rahul G.                                      │
│  ─────────────────────────────────────────────────── │
│  TIMELINE                                             │
│  14:22  Ticket opened (institution portal)            │
│  14:45  Assigned to L2 — Rahul G.                     │
│  15:10  Rahul: "Investigating Safari WebKit issue"    │
│  [Add internal note...]                               │
│  ─────────────────────────────────────────────────── │
│  [Reassign]  [Escalate to L3]  [Close Ticket]        │
└──────────────────────────────────────────────────────┘
```

---

## 7. Component Architecture

| Component | File | Props |
|---|---|---|
| `SupportSummaryCard` | `components/support/summary_card.html` | `label, value, subline, alert_level` |
| `SLABreachRow` | `components/support/breach_row.html` | `ticket, institution, tier, level, elapsed_over_sla, agent` |
| `AgentPerformanceRow` | `components/support/agent_row.html` | `agent, level, open_count, resolved_count, avg_resolution, sla_pct, satisfaction` |
| `IssueCategoryRow` | `components/support/issue_row.html` | `category, count, pct, trend_pct, trend_direction` |
| `HighTicketInstitutionRow` | `components/support/institution_ticket_row.html` | `institution, open_count, breach_count, health_score, csm` |
| `TicketDrawer` | `components/support/ticket_drawer.html` | `ticket_id` |

---

## 8. HTMX Architecture

| `?part=` | Target | Poll | Trigger |
|---|---|---|---|
| `summary` | `#support-summary` | 60s | load |
| `trend` | `#ticket-trend-chart` | None | load |
| `sla-breaches` | `#sla-breach-table` | 60s | load |
| `agents` | `#agent-performance` | 120s | load + period change |
| `categories` | `#issue-categories` | None | load |
| `top-institutions` | `#top-institutions` | 120s | load |
| `ticket-drawer` | `#drawer-container` | None | row click |

---

## 9. Backend View & API

```python
class SupportOpsView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "portal.view_support_ops"

    def get(self, request):
        allowed = {"coo","support_manager","ceo","superadmin"}
        if request.user.role not in allowed:
            return redirect("exec:dashboard")

        if _is_htmx(request):
            part = request.GET.get("part","")
            ctx  = self._build_context(request, part)
            dispatch = {
                "summary":          "exec/support/partials/summary.html",
                "trend":            "exec/support/partials/trend.html",
                "sla-breaches":     "exec/support/partials/sla_breaches.html",
                "agents":           "exec/support/partials/agents.html",
                "categories":       "exec/support/partials/categories.html",
                "top-institutions": "exec/support/partials/top_institutions.html",
                "ticket-drawer":    "exec/support/partials/ticket_drawer.html",
            }
            if part in dispatch:
                return render(request, dispatch[part], ctx)
        return render(request, "exec/support_ops.html", {})
```

**Action endpoints:**

| Method | URL | Permission | Action |
|---|---|---|---|
| POST | `/exec/support-ops/actions/reassign/` | `portal.manage_support` | Update `SupportTicket.assigned_to`, log to timeline |
| POST | `/exec/support-ops/actions/escalate/` | `portal.manage_support` | Escalate ticket tier (L1→L2 or L2→L3) |
| POST | `/exec/support-ops/actions/close/` | `portal.manage_support` | Close ticket with resolution note |
| GET | `/exec/support-ops/?part=export&type=breaches` | `portal.export_support_data` | CSV of SLA breaches |

---

## 10. Database Schema

```python
class SupportTicket(models.Model):
    ticket_ref    = models.CharField(max_length=20, unique=True)  # TKT-2026-884
    institution   = models.ForeignKey("Institution", on_delete=models.PROTECT, db_index=True)
    tier          = models.CharField(max_length=15)  # standard/professional/enterprise
    level         = models.CharField(max_length=3,
                        choices=[("L1","L1"),("L2","L2"),("L3","L3")])
    category      = models.CharField(max_length=100, db_index=True)
    title         = models.CharField(max_length=200)
    description   = models.TextField()
    status        = models.CharField(max_length=20,
                        choices=[("open","Open"),("in_progress","In Progress"),
                                 ("resolved","Resolved"),("closed","Closed")],
                        db_index=True)
    assigned_to   = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,
                                       on_delete=models.SET_NULL, db_index=True)
    sla_deadline  = models.DateTimeField()
    sla_breached  = models.BooleanField(default=False, db_index=True)
    opened_at     = models.DateTimeField(auto_now_add=True, db_index=True)
    resolved_at   = models.DateTimeField(null=True)
    satisfaction_score = models.FloatField(null=True)  # 1–5, from post-resolution survey

    class Meta:
        indexes = [
            models.Index(fields=["status","sla_breached","opened_at"]),
            models.Index(fields=["institution","status"]),
        ]


class TicketTimelineEntry(models.Model):
    ticket     = models.ForeignKey(SupportTicket, on_delete=models.CASCADE,
                                    related_name="timeline")
    actor      = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,
                                    on_delete=models.SET_NULL)
    entry_type = models.CharField(max_length=30)  # comment / assignment / escalation / status_change
    body       = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_internal= models.BooleanField(default=False)  # internal notes not visible to institution
```

---

## 11. Validation Rules

| Action | Validation |
|---|---|
| Reassign ticket | New agent must exist and have appropriate level role. Ticket must be open/in-progress. |
| Escalate ticket | Can only escalate up (L1→L2, L2→L3). Reason required (min 20 chars). L3 escalation requires COO/Support Manager. |
| Close ticket | Resolution note required (min 10 chars). Actor must have `portal.manage_support`. |
| Export SLA breaches | Rate-limited: 10/hour. COO / Support Manager / CEO only. |

---

## 12. Security Considerations

| Concern | Implementation |
|---|---|
| Ticket content privacy | Ticket descriptions may contain student data. Access restricted to Support Manager + COO + CEO + assigned agent. |
| Institution data in tickets | Institutions cannot see each other's tickets. This page (exec-only) shows cross-institution view — access controlled by role. |
| Audit trail | Every ticket status change, reassignment, and escalation logged in `TicketTimelineEntry` + `AuditLog`. Immutable. |
| SLA breach export | Export contains institution contact data — restricted to COO/Support Manager/CEO. Logged in `AuditLog`. |

---

## 13. Edge Cases

| State | Behaviour |
|---|---|
| All agents offline / unassigned queue growing | Banner: "⚠ 12 tickets unassigned for > 2h — [Assign All to On-call Agent →]" |
| Enterprise SLA breach > 2x over limit | Auto-creates P2 incident (enterprise client SLA breach = operational incident). Notifies COO + account manager. |
| No open SLA breaches | SLA Breach section shows "✅ All tickets within SLA" green state |
| Ticket count = 0 | Summary shows all zeros with green "No open tickets ✅" |
| Support ticket from institution in critical health zone | Row in top-institutions table shows red health badge — visual cross-signal between support + health data |

---

## 14. Performance & Scaling

| Endpoint | Target |
|---|---|
| Summary strip | < 100ms (Redis) |
| SLA breach table | < 200ms |
| Agent performance | < 300ms |
| Ticket trend chart | < 400ms |
| Top institutions | < 200ms |

- SLA breach check runs as Celery beat task every 5 min: `SupportTicket.objects.filter(status__in=['open','in_progress'], sla_deadline__lt=now()).update(sla_breached=True)`
- All summary aggregations cached in Redis at 55s TTL
- Agent performance query: indexed on `assigned_to` + `opened_at` — fast even at 10,000 tickets/month history

---

*Last updated: 2026-03-20*
