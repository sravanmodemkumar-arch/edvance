# O-21 — Follow-up Scheduler & Reminders

> **URL:** `/group/marketing/leads/follow-ups/`
> **File:** `o-21-follow-up-scheduler.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Role:** Group Admission Telecaller Executive (Role 130, G3) — primary user; Campaign Manager (119) — oversight

---

## 1. Purpose

The Follow-up Scheduler & Reminders is the task management layer for the lead pipeline — ensuring no lead goes unfollowed and no promise to a parent ("I'll call you back on Thursday") is forgotten. In Indian education admissions, persistence is everything. The industry wisdom is: it takes 5–7 touchpoints to convert a lead. A parent who said "I'll think about it" on Day 1 often enrolls on Day 15 — but only if someone calls on Day 3, sends a WhatsApp on Day 7, invites for a demo class on Day 10, and offers an early-bird discount on Day 14.

The problems this page solves:

1. **Follow-up discipline:** Telecallers manage 50–80 leads each. Without a system, they forget who to call today, double-call some parents while ignoring others, and miss promised callback dates. The scheduler gives each telecaller a clear daily task list.

2. **Escalation on overdue:** If a follow-up is scheduled for Wednesday and the telecaller hasn't completed it by Thursday, the system auto-escalates to the Campaign Manager. If not addressed by Friday, it escalates to G4.

3. **Multi-channel follow-up:** Not every follow-up is a phone call. Some leads prefer WhatsApp ("Please don't call during office hours, send me WhatsApp"). The scheduler supports: Call / WhatsApp / SMS / Email / Branch Visit Invite as follow-up types.

4. **Auto-scheduled sequences:** When a lead enters a certain stage, the system auto-creates a follow-up sequence. Example: "Interested but not booked walk-in" → auto-schedule: Day 1 call, Day 3 WhatsApp with prospectus, Day 7 call, Day 14 SMS with offer.

**Scale:** 5–50 telecallers · 1,000–10,000 active follow-ups at any time · 200–2,000 follow-ups due daily across group · 3–5 follow-up sequences per stage

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Admission Telecaller Executive | 130 | G3 | Full operations (own follow-ups) — view, complete, reschedule, add notes | Primary user |
| Group Admissions Campaign Manager | 119 | G3 | Full CRUD (all follow-ups) — view all, reassign, override, configure sequences | Supervisor + sequence configuration |
| Group Admission Data Analyst | 132 | G1 | Read only — follow-up compliance reports | Analytics |
| Branch Principal | — | G3 | Read (own branch) — view follow-up status for branch leads | Branch oversight |
| Group CEO / Chairman | — | G4/G5 | Read — escalation recipient for critical overdue | Escalation endpoint |

> **Access enforcement:** `@require_role(min_level=G1, division='O')`. Telecallers (130) see only `assigned_to = user.id`. Campaign Manager sees all.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Marketing & Campaigns  ›  Lead Management  ›  Follow-up Scheduler & Reminders
```

### 3.2 Page Header (Telecaller View)
```
Follow-up Scheduler                                  [+ Schedule Follow-up]  [My Today]  [My Overdue]
Telecaller — Priya Reddy
Kukatpally Branch · Due Today: 24 · Overdue: 3 · Completed Today: 18 · Upcoming (7 days): 86
```

### 3.3 Page Header (Supervisor View)
```
Follow-up Scheduler — All Team                       [Configure Sequences]  [Bulk Reschedule]  [Export]
Campaign Manager — Rajesh Kumar
All Branches · Due Today: 342 · Overdue: 48 · Completed Today: 264 · Compliance Rate: 84.6%
```

---

## 4. KPI Summary Bar (6 cards)

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Due Today | Integer | COUNT WHERE due_date = today AND status = 'pending' | Static blue | `#kpi-due-today` |
| 2 | Overdue | Integer | COUNT WHERE due_date < today AND status = 'pending' | Red > 20, Amber 5–20, Green < 5 | `#kpi-overdue` |
| 3 | Completed Today | Integer | COUNT WHERE completed_date = today | Static green | `#kpi-completed` |
| 4 | Compliance Rate | Percentage | Completed on-time / Total due × 100 (last 7 days) | Green ≥ 85%, Amber 70–85%, Red < 70% | `#kpi-compliance` |
| 5 | Upcoming (7 days) | Integer | COUNT WHERE due_date in next 7 days | Static blue | `#kpi-upcoming` |
| 6 | Auto-Sequences Active | Integer | COUNT active follow-up sequences | Static grey | `#kpi-sequences` |

**HTMX:** `hx-get="/api/v1/group/{id}/marketing/leads/follow-ups/kpis/"` → `hx-trigger="load, every 60s"`

---

## 5. Sections

### 5.1 Tab Navigation

Four tabs:
1. **Today's Tasks** — Follow-ups due today (actionable task list)
2. **Calendar** — Follow-up schedule across dates
3. **Overdue** — All overdue follow-ups with escalation status
4. **Sequences** — Auto-follow-up sequence configuration (Supervisor only)

### 5.2 Tab 1: Today's Tasks

**Priority-ordered task list.** Each task = one follow-up action.

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Priority | Badge | No | 🔴 Overdue / 🟡 Due Now / 🟢 Later Today |
| Time | Time | Yes | Scheduled time (if set) or "Any time today" |
| Lead | Text (link) | Yes | Student name → opens lead in O-15 |
| Parent | Text | Yes | Parent name |
| Phone | Text (click-to-call) | No | — |
| Branch | Text | Yes | — |
| Stage | Badge | Yes | Current pipeline stage |
| Follow-up Type | Badge | Yes | 📞 Call / 💬 WhatsApp / 📱 SMS / 📧 Email / 🏫 Visit Invite |
| Reason | Text | No | Why this follow-up: "Callback requested" / "Walk-in reminder" / "Auto-sequence Day 7" |
| Previous Attempts | Integer | No | How many prior follow-ups for this lead |
| Last Contact | Date | No | When lead was last contacted |
| Actions | Buttons | No | [Do It] [Reschedule] [Skip] [Mark Done] |

**"Do It" action per type:**
- Call → initiates click-to-call + opens O-18 disposition form
- WhatsApp → opens WhatsApp send modal with template pre-selected
- SMS → opens SMS send modal
- Email → opens email compose
- Visit Invite → opens walk-in booking form

**Completion:** After action, telecaller marks follow-up as "Done" with brief note.

### 5.3 Tab 2: Calendar

Monthly calendar view showing follow-up density.

**Calendar cell content:**
```
┌──────────────┐
│  18  Tue     │
│  Due: 28     │
│  Done: 22    │
│  Pending: 6  │
│  ██████░░    │
└──────────────┘
```

- Click on a date → shows all follow-ups for that date in a list below the calendar
- Colour: Green (all done), Amber (some pending), Red (many overdue)
- Drag-and-drop: reschedule by dragging a follow-up to a new date

### 5.4 Tab 3: Overdue

All overdue follow-ups with escalation status.

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Lead | Text | Yes | Student name |
| Phone | Text | No | — |
| Due Date | Date | Yes | When it was due |
| Days Overdue | Integer | Yes | Red ≥ 7, Amber 3–7, less = yellow |
| Follow-up Type | Badge | Yes | — |
| Assigned To | Text | Yes | Telecaller name |
| Reason | Text | No | — |
| Escalation | Badge | Yes | None / Level 1 (Campaign Mgr) / Level 2 (CEO) |
| Actions | Buttons | No | [Do Now] [Reschedule] [Reassign] [Close (with reason)] |

**Escalation rules:**
- Overdue 1 day → notification to telecaller (in-app + WhatsApp)
- Overdue 2 days → escalate to Campaign Manager (119)
- Overdue 5 days → escalate to G4 (CEO)
- Overdue 7 days → auto-mark lead as "At Risk" in pipeline

### 5.5 Tab 4: Sequences (Supervisor only)

Auto-follow-up sequence configuration. A sequence is a series of follow-up actions triggered when a lead enters a specific pipeline stage.

**Sequence table:**

| Column | Type | Notes |
|---|---|---|
| Sequence Name | Text | E.g., "Interested — Not Booked Walk-in" |
| Trigger | Badge | Pipeline stage entry: "Interested" / "Walk-in Booked" / "Offered" / etc. |
| Steps | Integer | Number of follow-up steps |
| Active Leads | Integer | How many leads currently in this sequence |
| Completion Rate | Percentage | % of leads that completed all steps |
| Status | Toggle | Active / Paused |
| Actions | Buttons | [Edit] [Pause] [Clone] [Delete] |

**Sequence builder (on edit):**

Each sequence has ordered steps:

| Step # | Day Offset | Type | Template/Script | Condition |
|---|---|---|---|---|
| 1 | Day 0 | 📞 Call | "Introduce branch, ask about visit" | Always |
| 2 | Day 3 | 💬 WhatsApp | Template: "prospectus_share" | If Step 1 = contacted |
| 3 | Day 7 | 📞 Call | "Follow up on prospectus, invite for walk-in" | If not yet booked walk-in |
| 4 | Day 10 | 💬 WhatsApp | Template: "demo_class_invite" | If still interested |
| 5 | Day 14 | 📞 Call | "Early bird offer closing soon" | If not yet applied |
| 6 | Day 21 | 📱 SMS | "Last chance — seats filling fast" | If still in pipeline |

**Sequence exit conditions:**
- Lead advances to next stage → exit sequence
- Lead marked as Lost → exit sequence
- All steps completed → exit sequence
- Manual override → telecaller can pause/exit a lead from sequence

---

## 6. Drawers & Modals

### 6.1 Modal: `schedule-follow-up` (480px)

- **Title:** "Schedule Follow-up"
- **Fields:**
  - Lead (search by name or phone, or pre-selected from pipeline)
  - Follow-up type (dropdown): Call / WhatsApp / SMS / Email / Branch Visit Invite
  - Due date (date, required)
  - Due time (time, optional — specific time or "Any time")
  - Assigned to (dropdown — defaults to lead's current assignee)
  - Reason / Note (textarea — what to say/discuss)
  - Priority (dropdown): Normal / Urgent
  - Repeat (optional): None / Daily for N days / Weekly for N weeks
- **Buttons:** Cancel · Schedule
- **Access:** Role 130 (own leads), 119 (any lead), G4+

### 6.2 Modal: `reschedule-follow-up` (400px)

- **Title:** "Reschedule Follow-up"
- **Pre-filled:** Current due date, lead name
- **Fields:**
  - New date (date, required)
  - New time (time, optional)
  - Reason for reschedule (dropdown): Parent Not Available / Telecaller Absent / Weather/Holiday / Parent Requested / Other
- **Buttons:** Cancel · Reschedule
- **Access:** Role 130 (own), 119 (any), G4+

### 6.3 Modal: `complete-follow-up` (480px)

- **Title:** "Complete Follow-up — [Lead Name]"
- **Fields:**
  - Outcome (dropdown): Completed Successfully / Parent Not Reachable / Rescheduled / Lead Not Interested
  - If call: call duration (auto from telephony or manual)
  - If WhatsApp: message sent confirmation
  - Notes (textarea — conversation summary)
  - Next follow-up needed? (toggle → if yes, schedule next inline)
  - Advance lead stage? (toggle → if yes, opens stage advance form)
- **Buttons:** Cancel · Complete
- **Access:** Role 130 (own), 119 (any), G4+

### 6.4 Modal: `create-sequence` (640px, Supervisor)

- **Title:** "Create Follow-up Sequence"
- **Fields:**
  - Sequence name (text, required)
  - Trigger stage (dropdown — pipeline stage that activates this sequence)
  - Additional trigger conditions (optional): Source = X / Priority = Hot / Branch = Y
  - Steps (dynamic list — add/remove/reorder):
    - Per step: Day offset / Type / Template or script / Condition (skip if lead has advanced)
  - Exit conditions: Lead advances / Lead lost / All steps done / Manual exit
  - Max leads in sequence (optional — cap to prevent overload)
- **Buttons:** Cancel · Save · Save & Activate
- **Access:** Role 119 or G4+

### 6.5 Drawer: `follow-up-detail` (560px, right-slide)

- **Content:**
  - Follow-up details: lead, type, due date, assigned to, reason
  - Lead context: current stage, lead score, last 3 interactions
  - Sequence info (if auto-generated): which sequence, which step, remaining steps
  - Previous follow-ups for this lead (timeline)
- **Footer:** [Do It Now] [Reschedule] [Reassign] [Mark Done] [Cancel Follow-up]

---

## 7. Charts

### 7.1 Follow-up Compliance Rate (Line)

| Property | Value |
|---|---|
| Chart type | Line (Chart.js 4.x) |
| Title | "Follow-up Compliance Rate — Last 30 Days" |
| Data | Daily: completed on-time / total due |
| Colour | `#10B981` green |
| Benchmark | 85% target (dashed line) |
| API | `GET /api/v1/group/{id}/marketing/leads/follow-ups/analytics/compliance-trend/` |

### 7.2 Overdue Trend (Area)

| Property | Value |
|---|---|
| Chart type | Area (Chart.js 4.x) |
| Title | "Overdue Follow-ups — Daily Count" |
| Data | Daily count of overdue follow-ups |
| Colour | `#EF4444` red area |
| Purpose | Track if overdue backlog is growing or shrinking |
| API | `GET /api/v1/group/{id}/marketing/leads/follow-ups/analytics/overdue-trend/` |

### 7.3 Telecaller Compliance Comparison (Bar)

| Property | Value |
|---|---|
| Chart type | Horizontal bar (Chart.js 4.x) |
| Title | "Follow-up Compliance by Telecaller" |
| Data | Per telecaller: compliance rate (%) |
| Colour | Green ≥ 85%, Amber 70–85%, Red < 70% |
| API | `GET /api/v1/group/{id}/marketing/leads/follow-ups/analytics/telecaller-compliance/` |

### 7.4 Follow-up Type Distribution (Donut)

| Property | Value |
|---|---|
| Chart type | Donut |
| Title | "Follow-up Types — This Month" |
| Data | COUNT per follow-up type (Call / WhatsApp / SMS / Email / Visit) |
| Colour | Call: blue / WhatsApp: green / SMS: teal / Email: indigo / Visit: amber |
| API | `GET /api/v1/group/{id}/marketing/leads/follow-ups/analytics/type-distribution/` |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Follow-up scheduled | "Follow-up for [Name] scheduled on [Date]" | Success | 3s |
| Follow-up completed | "Follow-up completed — [Outcome]" | Success | 2s |
| Follow-up rescheduled | "Follow-up rescheduled to [New Date]" | Info | 3s |
| Overdue alert | "You have [N] overdue follow-ups — complete them now!" | Warning | 5s |
| Escalation triggered | "Follow-up for [Name] escalated to [Role]" | Warning | 5s |
| Sequence created | "Sequence '[Name]' created with [N] steps" | Success | 3s |
| Sequence activated | "Sequence '[Name]' activated — will apply to new leads at [Stage]" | Success | 4s |
| Bulk rescheduled | "[N] follow-ups rescheduled to [Date]" | Success | 3s |
| Lead advanced from follow-up | "Lead [Name] advanced to [Stage] after follow-up" | Success | 3s |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| No follow-ups today | ✅ | "All Clear Today!" | "You have no follow-ups scheduled for today. Great work!" | — |
| No overdue follow-ups | ✅ | "No Overdue Items" | "All follow-ups are on track." | — |
| No sequences configured | 🔄 | "No Auto-Sequences" | "Create follow-up sequences to automate lead nurturing." | Create Sequence |
| No follow-ups for lead | 📋 | "No Follow-ups Scheduled" | "Schedule a follow-up to keep this lead engaged." | Schedule Follow-up |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | 6 KPI shimmer + task list skeleton (12 rows) |
| Tab switch | Content skeleton |
| Calendar load | 7×5 grid shimmer |
| Overdue list | Table skeleton (15 rows) |
| Sequence builder | Step list placeholder |
| Chart load | Grey canvas placeholder |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/marketing/leads/follow-ups/` | G1+ | List follow-ups (filterable) |
| GET | `/api/v1/group/{id}/marketing/leads/follow-ups/today/` | G3+ | Today's task list (own or all) |
| GET | `/api/v1/group/{id}/marketing/leads/follow-ups/overdue/` | G1+ | Overdue follow-ups |
| GET | `/api/v1/group/{id}/marketing/leads/follow-ups/{fu_id}/` | G1+ | Follow-up detail |
| POST | `/api/v1/group/{id}/marketing/leads/follow-ups/` | G3+ | Schedule follow-up |
| PATCH | `/api/v1/group/{id}/marketing/leads/follow-ups/{fu_id}/complete/` | G3+ | Complete follow-up |
| PATCH | `/api/v1/group/{id}/marketing/leads/follow-ups/{fu_id}/reschedule/` | G3+ | Reschedule |
| PATCH | `/api/v1/group/{id}/marketing/leads/follow-ups/{fu_id}/reassign/` | G3+ (119) | Reassign |
| DELETE | `/api/v1/group/{id}/marketing/leads/follow-ups/{fu_id}/` | G3+ | Cancel follow-up |
| POST | `/api/v1/group/{id}/marketing/leads/follow-ups/bulk-reschedule/` | G3+ (119) | Bulk reschedule |
| GET | `/api/v1/group/{id}/marketing/leads/follow-ups/sequences/` | G1+ | List sequences |
| POST | `/api/v1/group/{id}/marketing/leads/follow-ups/sequences/` | G3+ (119) | Create sequence |
| PUT | `/api/v1/group/{id}/marketing/leads/follow-ups/sequences/{seq_id}/` | G3+ (119) | Update sequence |
| PATCH | `/api/v1/group/{id}/marketing/leads/follow-ups/sequences/{seq_id}/toggle/` | G3+ (119) | Activate/pause |
| DELETE | `/api/v1/group/{id}/marketing/leads/follow-ups/sequences/{seq_id}/` | G4+ | Delete sequence |
| GET | `/api/v1/group/{id}/marketing/leads/follow-ups/calendar/` | G1+ | Calendar view data |
| GET | `/api/v1/group/{id}/marketing/leads/follow-ups/kpis/` | G1+ | KPI values |
| GET | `/api/v1/group/{id}/marketing/leads/follow-ups/analytics/compliance-trend/` | G1+ | Compliance chart |
| GET | `/api/v1/group/{id}/marketing/leads/follow-ups/analytics/overdue-trend/` | G1+ | Overdue trend |
| GET | `/api/v1/group/{id}/marketing/leads/follow-ups/analytics/telecaller-compliance/` | G1+ | Telecaller compliance |
| GET | `/api/v1/group/{id}/marketing/leads/follow-ups/analytics/type-distribution/` | G1+ | Type donut |

---

## 12. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load | `<div id="kpi-bar">` | `hx-get=".../follow-ups/kpis/"` | `#kpi-bar` | `innerHTML` | `hx-trigger="load, every 60s"` |
| Today's tasks | Default tab | `hx-get=".../follow-ups/today/"` | `#task-list` | `innerHTML` | `hx-trigger="load"` |
| Tab switch | Tab click | `hx-get` with tab param | `#followup-content` | `innerHTML` | `hx-trigger="click"` |
| Complete follow-up | Done button | `hx-patch=".../follow-ups/{id}/complete/"` | `#task-row-{id}` | `outerHTML` | Row removed or greyed |
| Reschedule | Reschedule form | `hx-patch=".../follow-ups/{id}/reschedule/"` | `#task-row-{id}` | `outerHTML` | Row updated |
| Schedule new | Schedule form | `hx-post=".../follow-ups/"` | `#schedule-result` | `innerHTML` | Toast + list refresh |
| Calendar load | Calendar tab | `hx-get=".../follow-ups/calendar/?month={YYYY-MM}"` | `#calendar-view` | `innerHTML` | `hx-trigger="click"` |
| Calendar nav | Prev/next | `hx-get=".../follow-ups/calendar/?month={adj}"` | `#calendar-view` | `innerHTML` | Month navigation |
| Overdue list | Overdue tab | `hx-get=".../follow-ups/overdue/"` | `#overdue-list` | `innerHTML` | `hx-trigger="load"` |
| Sequence list | Sequences tab | `hx-get=".../follow-ups/sequences/"` | `#sequence-list` | `innerHTML` | Supervisor only |
| Sequence toggle | Toggle switch | `hx-patch=".../follow-ups/sequences/{id}/toggle/"` | `#seq-status-{id}` | `innerHTML` | Inline badge |

---

*Page spec version: 1.0 · Last updated: 2026-03-26*
