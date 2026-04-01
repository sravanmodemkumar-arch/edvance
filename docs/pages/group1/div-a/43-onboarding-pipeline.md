# 43 — Onboarding Pipeline Tracker

---

## 1. Page Metadata

| Field | Value |
|---|---|
| Page title | Onboarding Pipeline Tracker |
| Route | `/exec/onboarding-pipeline/` |
| Django view | `OnboardingPipelineView` |
| Template | `exec/onboarding_pipeline.html` |
| Priority | **P2** |
| Nav group | Operations |
| Required roles | `coo` · `support_manager` · `onboarding_specialist` · `csm_manager` · `ceo` · `superadmin` |
| CTO / CFO | Denied |
| HTMX poll — pipeline table | Every 120s |
| HTMX poll — summary strip | Every 120s |
| Cache | Summary: Redis TTL 115s · Pipeline data: DB query (no Redis — data changes frequently) |
| Theme tokens | bg-base `#040810` · surface-1 `#08101E` · accent `#6366F1` · danger `#EF4444` · warn `#F59E0B` · success `#22C55E` |

---

## 2. Purpose & Business Logic

**The onboarding problem:**

EduForge onboards 30–50 new institutions per month. Each onboarding has ~12 steps:
1. Contract signed
2. GSTIN + bank details collected
3. Subdomain provisioned (`abc-school.eduforge.in`)
4. DB schema created (tenant isolation)
5. Admin user account created
6. Institution admin trained (video call)
7. Initial data import (student roster, class structure)
8. First exam configured
9. BGV requirement communicated
10. Go-live checklist signed off
11. First invoice generated
12. Health score baseline established

If a step is missed or delayed, the institution cannot use the platform — but they are already billed. A single delayed onboarding at a coaching centre = Rs.15L ARR at risk.

The COO currently tracks this in a spreadsheet. This page replaces that spreadsheet with a real-time tracked pipeline.

---

## 3. User Roles & Access

| Role | Can View | Can Act |
|---|---|---|
| CEO | All | Read-only |
| COO | All | Reassign specialist, mark steps complete, flag blockers |
| Support Manager | All | Same as COO |
| Onboarding Specialist | Their assigned institutions only | Mark steps complete, add notes |
| CSM Manager | All | Read-only + add notes |
| CTO / CFO | No access | Redirect |

---

## 4. Section-wise UI Breakdown

---

### Section 1 — Summary Strip

```
╔══════════════╦══════════════╦══════════════╦══════════════╦══════════════╗
║ ACTIVE       ║ ON TRACK     ║ AT RISK      ║ BLOCKED      ║ GO-LIVES     ║
║ ONBOARDINGS  ║              ║              ║              ║ THIS MONTH   ║
║     38       ║     24       ║     10       ║      4       ║     18       ║
║ 30–50/month  ║  63.2%       ║  26.3%       ║  10.5%       ║ ▲ 3 pending  ║
╚══════════════╩══════════════╩══════════════╩══════════════╩══════════════╝
```

- Blocked: any institution with a step stalled > 3 days → COO immediate attention
- "Go-lives This Month": institutions that completed onboarding this calendar month

---

### Section 2 — Kanban Board View (Primary View)

**Purpose:** Visual pipeline showing how many institutions are at each onboarding stage.

**UI elements:**
```
ONBOARDING PIPELINE                              [View: Kanban ●  Table]
────────────────────────────────────────────────────────────────────────
Contract    DB Setup   Training   Data Import  Go-Live    Live
  Signed    Pending                Pending      Ready
   ┌────┐   ┌────┐     ┌────┐      ┌────┐      ┌────┐    ┌────┐
   │ 8  │   │ 6  │     │ 10 │      │ 7  │      │ 3  │    │ 4  │
   │inst│   │inst│     │inst│      │inst│      │inst│    │inst│
   └────┘   └────┘     └────┘      └────┘      └────┘    └────┘
```

Each column: count of institutions at that stage. Click column → expands to list view of those institutions.

**Table view toggle:** Full sortable table (see below).

---

### Section 3 — Pipeline Table

**Purpose:** Detailed operational list with per-institution step completion and go-live date tracking.

**UI elements:**
```
ACTIVE ONBOARDINGS           [Type: All ▾] [Status: All ▾] [Specialist ▾] [🔍]
────────────────────────────────────────────────────────────────────────────────
Institution      │Type    │Stage          │Steps  │Go-Live     │Specialist   │ ⋯
─────────────────┼────────┼───────────────┼───────┼────────────┼─────────────┼──
ABC Coaching     │Coaching│ 🟡 Training    │ 6/12  │ 1 Apr 2026 │ Anjali S.   │ ⋯
XYZ School       │School  │ 🔴 Blocked     │ 3/12  │ 15 Mar ⚠   │ Rahul K.    │ ⋯
DEF College      │College │ ✅ Go-Live Ready│12/12  │ 25 Mar     │ Priya M.    │ ⋯
GHI Group        │Group   │ 🟢 Live        │12/12  │ 20 Mar ✅   │ Anjali S.   │ ⋯
```

**Column details:**

| Column | Detail |
|---|---|
| Institution | Name + type badge |
| Stage | Current step name + colour: 🟢 On Track · 🟡 Delayed · 🔴 Blocked |
| Steps | "X/12" progress. Mini progress bar. |
| Go-Live | Target date. Red if past due + still not live. |
| Specialist | Assigned onboarding specialist. "Unassigned" = red. |
| ⋯ | View Detail · Reassign Specialist · Add Note · Mark Blocked · Complete Step |

**Click row → Onboarding Detail Drawer (560px):**
- All 12 steps with completion status, date completed, completed by
- Overdue steps highlighted
- Notes history
- "Complete Step" action (Onboarding Specialist / COO)
- Go-live date updater

---

### Section 4 — Bottleneck Analysis

**Purpose:** Which step is taking longest across all active onboardings? This reveals process inefficiencies.

**UI elements:**
```
BOTTLENECK ANALYSIS — Avg days per step (last 90 days)
─────────────────────────────────────────────────────
Step                    Avg Days   P90 Days  Bottleneck?
───────────────────────┼───────────┼──────────┼──────────
Contract Signed         0.5d       1.2d       —
DB Setup                0.3d       0.8d       —
Admin Training          3.2d       7.4d       ⚠ Slow
Data Import             4.8d       11.2d      🔴 Major bottleneck
First Exam Config       2.1d       5.6d       ⚠ Slow
BGV Communication       1.4d       3.2d       —
Go-Live Signoff         2.8d       6.4d       ⚠ Slow
```

- "Data Import" is consistently the longest step — COO can decide to hire another data migration specialist or build a self-service import tool
- Horizontal bar chart variant: bar length = avg days, colour by bottleneck severity

---

### Section 5 — Go-Live Calendar

**Purpose:** Upcoming go-live dates — COO plans capacity (onboarding specialists, support team).

**UI elements:**
```
GO-LIVE CALENDAR — Next 30 Days
───────────────────────────────────────────────────────────────────────────
Date        Institutions Going Live          Specialist Load
────────────┼───────────────────────────────┼──────────────────────────────
25 Mar      DEF College, GHI Group           Anjali: 2, Priya: 1
28 Mar      JKL School                       Rahul: 1
1 Apr       ABC Coaching, MNO School Group   Anjali: 2
```

- Multiple go-lives same day: check specialist capacity
- > 3 go-lives same day: amber (risk — support team may be overwhelmed)

---

## 5. Full Page Wireframe

```
╔══════════════════════════════════════════════════════════════════════════════╗
║  Onboarding Pipeline Tracker                          [↺ Refresh]           ║
╠══════════╦══════════╦══════════╦══════════╦══════════════════════════════════╣
║ ACTIVE   ║ ON TRACK ║ AT RISK  ║ BLOCKED  ║ GO-LIVES THIS MONTH             ║
║    38    ║    24    ║    10    ║    4     ║    18                            ║
╠══════════╩══════════╩══════════╩══════════╩══════════════════════════════════╣
║  PIPELINE   [Kanban ●  Table]                                               ║
║  Contract│DB Setup│Training│Data Import│Go-Live Ready│Live                  ║
║    8     │    6   │   10   │     7     │      3      │  4                   ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  ACTIVE ONBOARDINGS           [Type ▾] [Status ▾] [Specialist ▾]           ║
║  ABC Coaching  Coaching  🟡 Training     6/12  1 Apr  Anjali S.             ║
║  XYZ School    School    🔴 Blocked      3/12  15 Mar ⚠ Rahul K.            ║
║  DEF College   College   ✅ Go-Live Ready 12/12  25 Mar  Priya M.            ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  BOTTLENECK ANALYSIS              GO-LIVE CALENDAR (30d)                   ║
║  Data Import:  4.8d avg 🔴         25 Mar: DEF College, GHI Group           ║
║  Admin Training: 3.2d avg ⚠        1 Apr:  ABC Coaching, MNO Group          ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 6. Component Architecture

| Component | File | Props |
|---|---|---|
| `OnboardingSummaryCard` | `components/onboarding/summary_card.html` | `label, value, subline, alert_level` |
| `KanbanColumn` | `components/onboarding/kanban_col.html` | `stage_name, count, institutions` |
| `OnboardingTableRow` | `components/onboarding/table_row.html` | `institution, stage, steps_done, steps_total, go_live_date, specialist, is_blocked, can_act` |
| `StepProgressBar` | `components/onboarding/progress_bar.html` | `done, total` |
| `BottleneckRow` | `components/onboarding/bottleneck_row.html` | `step_name, avg_days, p90_days, is_bottleneck` |
| `GoLiveCalendarRow` | `components/onboarding/go_live_row.html` | `date, institutions, specialist_load` |
| `OnboardingDrawer` | `components/onboarding/drawer.html` | `institution_id, can_act` |

---

## 7. HTMX Architecture

| `?part=` | Target | Poll | Trigger |
|---|---|---|---|
| `summary` | `#onboarding-summary` | 120s | load |
| `kanban` | `#kanban-board` | 120s | load |
| `table` | `#pipeline-table` | 120s | load + filter |
| `bottleneck` | `#bottleneck-analysis` | None | load |
| `go-live-calendar` | `#go-live-calendar` | None | load |
| `onboarding-drawer` | `#drawer-container` | None | row click |

---

## 8. Backend View & API

```python
class OnboardingPipelineView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "portal.view_onboarding_pipeline"

    def get(self, request):
        allowed = {"coo","support_manager","onboarding_specialist",
                   "csm_manager","ceo","superadmin"}
        if request.user.role not in allowed:
            return redirect("exec:dashboard")

        spec_filter = None
        if request.user.role == "onboarding_specialist":
            spec_filter = request.user  # see only own institutions

        can_act = request.user.role in {"coo","support_manager",
                                         "onboarding_specialist","superadmin"}

        if _is_htmx(request):
            part = request.GET.get("part","")
            ctx = {"can_act": can_act, "spec_filter": spec_filter}
            dispatch = {
                "summary":          "exec/onboarding/partials/summary.html",
                "kanban":           "exec/onboarding/partials/kanban.html",
                "table":            "exec/onboarding/partials/table.html",
                "bottleneck":       "exec/onboarding/partials/bottleneck.html",
                "go-live-calendar": "exec/onboarding/partials/go_live_calendar.html",
                "onboarding-drawer":"exec/onboarding/partials/drawer.html",
            }
            if part in dispatch:
                return render(request, dispatch[part], ctx)
        return render(request, "exec/onboarding_pipeline.html",
                      {"can_act": can_act})
```

**Action endpoints:**

| Method | URL | Permission | Action |
|---|---|---|---|
| POST | `/exec/onboarding-pipeline/actions/complete-step/` | `portal.manage_onboarding` | Mark `OnboardingStep.completed=True`, log timestamp + actor |
| POST | `/exec/onboarding-pipeline/actions/reassign/` | `portal.manage_onboarding` | Update `OnboardingRecord.specialist` |
| POST | `/exec/onboarding-pipeline/actions/flag-blocked/` | `portal.manage_onboarding` | Set `OnboardingRecord.status='blocked'`, require blocker description, notify COO |
| POST | `/exec/onboarding-pipeline/actions/update-go-live/` | `portal.manage_onboarding` | Update target go-live date, log reason |

---

## 9. Database Schema

```python
class OnboardingRecord(models.Model):
    institution  = models.OneToOneField("Institution", on_delete=models.CASCADE)
    status       = models.CharField(max_length=20,
                       choices=[("active","Active"),("blocked","Blocked"),
                                ("completed","Completed"),("cancelled","Cancelled")])
    specialist   = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,
                                      on_delete=models.SET_NULL, related_name="onboardings")
    target_go_live = models.DateField()
    actual_go_live = models.DateField(null=True)
    blocker_description = models.TextField(blank=True)
    started_at   = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True)

    class Meta:
        indexes = [models.Index(fields=["status","target_go_live"])]


class OnboardingStep(models.Model):
    STEPS = [
        ("contract_signed", "Contract Signed"),
        ("gstin_collected", "GSTIN & Bank Details"),
        ("subdomain_provisioned", "Subdomain Provisioned"),
        ("db_schema_created", "DB Schema Created"),
        ("admin_account_created", "Admin Account Created"),
        ("admin_trained", "Admin Training Completed"),
        ("data_imported", "Initial Data Import"),
        ("first_exam_configured", "First Exam Configured"),
        ("bgv_communicated", "BGV Requirements Communicated"),
        ("golive_checklist", "Go-Live Checklist Signed"),
        ("first_invoice", "First Invoice Generated"),
        ("health_baseline", "Health Score Baseline Set"),
    ]

    onboarding   = models.ForeignKey(OnboardingRecord, on_delete=models.CASCADE,
                                      related_name="steps")
    step_key     = models.CharField(max_length=50, choices=STEPS)
    completed    = models.BooleanField(default=False)
    completed_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,
                                      on_delete=models.SET_NULL)
    completed_at = models.DateTimeField(null=True)
    notes        = models.TextField(blank=True)

    class Meta:
        unique_together = ("onboarding", "step_key")
```

---

## 10. Validation Rules

| Action | Validation |
|---|---|
| Complete Step | Steps must be completed in order (cannot complete step 8 before step 7). Specialist can only complete steps for their assigned institution. |
| Flag Blocked | Blocker description required (min 20 chars). Notifies COO automatically. |
| Update Go-Live | New date cannot be in the past. Reason required if moving date backward. |
| Reassign Specialist | New specialist must have `onboarding_specialist` role. |

---

## 11. Security Considerations

- Onboarding specialist isolation: server-side filter to own institutions. Cannot view other specialists' clients.
- Step completion: `completed_by` field always set server-side from `request.user` — never from POST body.
- Go-live date change: logged in `AuditLog` with old date, new date, reason, actor.

---

## 12. Edge Cases

| State | Behaviour |
|---|---|
| Go-live date passed + institution not live | Row turns red. COO auto-notified. "Overdue go-live" badge on institution row. |
| Specialist leaves company (user deactivated) | Their institutions show "Unassigned" in red. COO prompted to reassign. |
| > 5 onboardings blocked simultaneously | COO dashboard KPI card "Blocked" turns red + P2 incident created automatically. |
| Steps completed out of order (via API) | `complete-step` endpoint validates step order. Returns 400 with "Previous step not completed: {step_name}". |
| Institution cancels during onboarding | `status='cancelled'` — removed from active pipeline, archived. Billing Admin alerted for invoice cancellation. |

---

## 13. Performance & Scaling

- Active onboardings: max ~100 concurrent (30–50/month with ~2 month pipeline). No pagination concern.
- Bottleneck analysis: aggregate query over last 90 days of completed steps. Cached 1 hour — acceptable.
- Go-live calendar: simple query for `target_go_live BETWEEN today AND today+30`. Fast.
- Kanban column counts: cached in Redis at 115s TTL — Celery beat aggregates every 2 min.

---

*Last updated: 2026-03-20*
