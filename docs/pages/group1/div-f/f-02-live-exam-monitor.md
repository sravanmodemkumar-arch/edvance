# F-02 — Live Exam Monitor

> **Route:** `/ops/exam/monitor/`
> **Division:** F — Exam Day Operations
> **Primary Role:** Exam Operations Manager (34) — full control including pause/extend
> **Supporting Roles:** Exam Support Executive (35) — create incidents, read monitor; Incident Manager (38) — infra escalation; DevOps/SRE (14) — read-only; Platform Admin (10) — full
> **File:** `f-02-live-exam-monitor.md`
> **Priority:** P0 — Active during all exam windows; the operational command surface for 74K concurrent

---

## 1. Page Name & Route

**Page Name:** Live Exam Monitor
**Route:** `/ops/exam/monitor/`
**Part-load routes:**
- `/ops/exam/monitor/?part=monitor-kpi` — KPI strip (polls every 30s)
- `/ops/exam/monitor/?part=monitor-grid` — exam cards grid (polls every 30s)
- `/ops/exam/monitor/?part=exam-detail&schedule_id={id}` — single exam detail panel
- `/ops/exam/monitor/?part=incident-list` — incidents tab content
- `/ops/exam/monitor/?part=action-log` — actions log tab content
- `/ops/exam/monitor/?part=snapshot-refresh&schedule_id={id}` — manual snapshot refresh for single exam

---

## 2. Purpose

F-02 is the operational command surface during live exams. It gives the Exam Operations Manager real-time visibility into all running exams across 2,050 institutions and the ability to take critical operational actions.

**Distinction from War Room (Div A / 32-war-room.md):**

| Aspect | F-02 Live Exam Monitor | A-32 War Room |
|---|---|---|
| Primary audience | Exam Ops Manager (34), Support Exec (35) | CTO, COO, CEO |
| Focus | Per-exam, per-institution operational triage | Platform-wide infrastructure health |
| Actions | Pause exam, extend time, override sessions | Emergency Lambda scale, Pause All Exams platform-wide |
| Data source | `exam_ops_snapshot` (Celery Beat, 30s) | Redis pub/sub (5s real-time) |
| Infrastructure gauges | Not shown — refer to War Room | Lambda CPU, RDS connections, CDN |
| Navigation | Standard EduForge nav | Full-screen war room mode |

F-02 does NOT duplicate War Room infrastructure data. F-02 is for operational decisions about individual exams; War Room is for infrastructure decisions affecting the platform.

**Why 30s polling instead of 5s:**
At 74K concurrent, each snapshot cycle hits all active tenant schemas. 30s is the minimum acceptable cycle that doesn't overwhelm PostgreSQL. The War Room's 5s uses Redis pub/sub — a different mechanism. F-02 is designed for operational awareness, not millisecond monitoring.

---

## 3. Tabs

| Tab | Label | HTMX |
|---|---|---|
| 1 | Active Exams | `?part=monitor-grid` (auto-polls 30s) |
| 2 | Incidents | `?part=incident-list` |
| 3 | Actions Log | `?part=action-log` |

---

## 4. Section-Wise Detailed Breakdown

---

### KPI Strip (polls every 30s — `hx-trigger="every 30s"`)

| # | KPI | Reads from | Alert threshold |
|---|---|---|---|
| 1 | Active Exams | `COUNT(exam_schedule WHERE status=ACTIVE)` | — |
| 2 | Active Sessions | `SUM(exam_ops_snapshot.total_active_sessions)` | — |
| 3 | Total Submissions (today) | `SUM(exam_ops_snapshot.total_submitted)` | — |
| 4 | Submission Rate | `SUM(last_submit_rate_per_min)` / min | Red if 0 and Active > 0 (no submissions while exam running = critical) |
| 5 | Open Incidents | `COUNT(exam_session_incident WHERE status IN (OPEN, IN_PROGRESS))` | Amber if > 0; Red if any CRITICAL |
| 6 | Snapshot Age | `MAX(now() - last_snapshot_at)` across active snapshots | Amber > 45s; Red > 90s (Celery lag) |

**Snapshot Age alert:** If `MAX(snapshot_age) > 90s`: red banner below KPI strip: "⚠️ Snapshot data is {N}s old — Celery task may be delayed. Data may not reflect current exam state. [Refresh All]"

**[Refresh All]** (manual button, top-right): triggers `?part=monitor-kpi` + `?part=monitor-grid` immediately. Does NOT trigger Celery snapshot update — just re-reads current snapshot data from DB. For a true manual snapshot, use [Force Snapshot] per exam card.

---

### Tab 1 — Active Exams

#### Toolbar

- Search: institution name or exam name. Debounced 300ms.
- Filter by:
  - Exam type: SSC · RRB · NEET · JEE · AP Board · TS Board · All
  - Institution type: School · College · Coaching · All
  - Status: Active · Paused · Scheduled (starting soon) · All
  - Issues only: toggle — shows only exams with `open_incident_count > 0` or `submit_error_count > 0`
- View: [Grid] [Table] toggle — default Grid

#### Exam Monitor Grid (Card Layout — default)

Each card = one active exam schedule.

**Card layout (2-column grid on desktop, 1-column on tablet/mobile):**

```
┌─────────────────────────────────────────────────────────────┐
│ [Status pill] ACTIVE · [Exam Type badge] SSC CGL Mock       │
│ Institution Name — Coaching Centre                          │
│ ─────────────────────────────────────────────────────────── │
│ Start: 10:00 AM IST  Duration: 90 min  Ends: 11:30 AM IST  │
│ Time remaining: [████████░░] 63 min left                    │
│ ─────────────────────────────────────────────────────────── │
│ Registered: 1,240     Active: 987     Submitted: 218        │
│ Timed Out: 3          Errors: 0       Rate: 24/min          │
│ ─────────────────────────────────────────────────────────── │
│ ⚠️ 2 open incidents                                         │
│ [View Details] [Pause Exam] [Extend Time] [···]             │
└─────────────────────────────────────────────────────────────┘
```

**Card colour states:**
- Normal: `bg-[#0D1526] border border-[#1E2D4A]`
- Has incidents: `border-[#F59E0B]` (amber border)
- CRITICAL incident: `border-[#EF4444]` pulsing (red border)
- PAUSED: `bg-[#1A1200] border-[#F59E0B]` (amber background)

**Progress bar (time remaining):**
- > 50% remaining: green
- 20–50%: amber
- < 20%: red
- After scheduled end (grace period): "Grace period — {N} min remaining" in amber

**Rate display:**
- `last_submit_rate_per_min` from snapshot
- If rate = 0 and exam ACTIVE: red text "0/min — check session logs"

**Card actions:**
- **[View Details]:** expands right panel (Exam Detail Panel) or opens full-page drill-down `/ops/exam/monitor/{schedule_id}/`
- **[Pause Exam]:** red button — shown only to Ops Manager (34). See Section 5 Modals.
- **[Extend Time]:** shown only to Ops Manager (34). See Section 5 Modals.
- **[···]:** Force Close · Override Session · Refresh Snapshot · View in War Room

**[···] — Force Close:**
- Closes exam immediately (sets `exam_schedule.status = COMPLETED`)
- All `IN_PROGRESS` sessions in tenant schema set to `TIMED_OUT` (scores computed on current state — partial answers count)
- Requires reason. Confirmation modal shows exact active session count: "Force-close exam? **{N} students are still active.** Their current answers will be scored as-is. This cannot be undone."
- Sessions mid-submit (status = `SUBMITTING`) are given a 30-second grace window before force-close finalises them. F-02 shows a countdown: "Waiting {N}s for in-flight submissions to complete…"

**[···] — Override Session:**
- Opens Override Session Modal (480px)
- Allows Ops Manager to manually set a specific session's status in the tenant schema
- Use case: a student's session is stuck in `IN_PROGRESS` and they cannot submit; Support Exec has already tried [Unlock Session] in F-03 and it failed
- Fields: Session Ref (anonymised hash) · Override Action: Unlock (reset to IN_PROGRESS) / Force Submit (score current state) / Mark Timed Out
- Requires reason. All overrides logged to `exam_ops_action_log` with action type `SESSION_OVERRIDE`.
- DPDPA: session_ref is anonymised — Ops Manager never sees student names

**Override Session outcomes:**
- **Unlock (reset to IN_PROGRESS):** session status reset; student's timer resumes from where it was. No scoring triggered.
- **Force Submit (score current state):** `POST /ops/exam/support/force-submit/{session_ref}/` called synchronously. Button disables, spinner shown "Scoring submission…" (max 10s). On success: session marked SUBMITTED with score; toast ✅ "Session force-submitted — score recorded." On failure: ❌ "Force submit failed — {error}. Session unchanged." Button re-enables.
- **Mark Timed Out:** session status → TIMED_OUT; score computed from current state by Celery (`compute_exam_result_for_session` task).

**[···] — Refresh Snapshot:**
- Triggers `?part=snapshot-refresh&schedule_id={id}`
- Forces Celery to run a snapshot update for just this exam immediately (outside the Beat schedule)
- Shows spinner on card during refresh

#### Starting Soon Panel (shown above the grid when ≥ 1 exam starts within 2 hours)

Collapsible strip — `bg-[#0D1526] border border-[#1E2D4A] rounded-xl p-3 mb-4`

"🕐 **{N} exams starting soon** — next: {Exam Name} at {Institution} in **{time}**"

Expands to show a compact list:

| Exam | Institution | Starts In | Config Status | Paper Assigned |
|---|---|---|---|---|
| SSC CGL Mock 5 | SR Coaching | 1h 42m | 🔒 Locked | ✅ SET-A |
| NEET Mock 3 | VR Academy | 0h 58m | ⚠️ Not Locked | ✅ NEET-2026-A |

**Purpose:** Ops Manager sees what's coming. ⚠️ "Not Locked" in this panel is an urgent flag — clicking it opens the F-01 Schedule Detail Drawer directly.

**[Go to F-01 Schedule]** link per row. Panel auto-dismisses when exam becomes ACTIVE.

**Panel overflow on high exam count:** If ≥ 20 exams are starting soon, show first 10 rows + "[View all {N} upcoming exams →]" button which expands to a full-screen modal. On mobile, limit visible rows to 5 + [View all]. Config Lock Status column computed using `exam_schedule.config_locked_at` compared against `exam_operational_config.config_lock_required_before_hours` — updates automatically on next HTMX poll when F-09 config changes.

#### Exam Monitor Table (alternate view)

Accessible via [Table] toggle.

| Column | Notes |
|---|---|
| Exam | Exam name + exam type badge |
| Institution | Name + type |
| Status | Status pill |
| Start / End | Times with time-remaining countdown |
| Registered | From snapshot |
| Active | From snapshot |
| Submitted | From snapshot |
| Rate | submit_rate/min from snapshot |
| Errors | submit_error_count |
| Incidents | Open incident count badge (amber if > 0) |
| Actions | [Details] · [Pause] · [Extend] · [···] |

Sortable: Start, Submitted, Rate, Incidents.
Pagination: not paginated during live exam — shows all active exams (typically < 100 at any time). Horizontal scroll on tablet.

#### Exam Detail Panel (right panel, 760px)

Triggered by [View Details].

**Header:** Exam name · Institution · Status pill · [Pause Exam] · [Extend Time] · [×]

**Section A — Session Breakdown**

Submission funnel visualization:
```
Registered: 1,240
  └── Started: 987 (79.6%)
       ├── Submitted: 218 (22.1% of started)
       ├── Active: 769 (still working)
       └── Timed Out: 0
```

Session state breakdown `PieChart` (Recharts):
- Active (green) · Submitted (blue) · Timed Out (grey) · Error (red)

**Session state definition — "Active":**
`total_active_sessions = COUNT(*) WHERE status IN (IN_PROGRESS, PAUSED)` in the tenant schema. Sessions with status = ERROR or ABANDONED are **not** counted as Active — they are counted separately in the "Errors" counter on the card. This ensures the Active count reflects students still able to continue their exam.

**Section B — Submission Rate Chart**

`LineChart` — rolling 10-minute submission rate (submissions/min on Y axis, time on X axis).
Data from: `exam_ops_snapshot.last_submit_rate_per_min` — snapshot history stored in `exam_ops_snapshot_history` (each snapshot writes a row).
X-axis: last 30 minutes in 30s increments. Auto-updates with KPI poll.

**Section C — Incidents for This Exam**

List of `exam_session_incident` for this `exam_schedule_id`, most recent first.

| Column | Notes |
|---|---|
| Type | Incident type label |
| Severity | Severity badge |
| Affected | Estimated count |
| Status | Status pill |
| Actions | [View] · [Resolve] · [Escalate] |

**[+ Report Incident]** — opens Incident Create Modal (640px).

**Section D — Operational Actions**

Quick action buttons available to Ops Manager (34):

| Action | When Available | Notes |
|---|---|---|
| Pause Exam | Status = ACTIVE | Opens Pause Exam Modal |
| Extend Duration | Status = ACTIVE or PAUSED | Opens Extend Duration Modal |
| Resume Exam | Status = PAUSED | No modal — confirm via button confirmation |
| Force Close | Status = ACTIVE, PAUSED | Opens Force Close Modal |
| Add Incident | Always during exam | Opens Incident Create Modal |

---

### Tab 2 — Incidents

All operational incidents across all exams, not just active.

#### Toolbar & Filters

| Filter | Control |
|---|---|
| Status | Multi-select: Open · In Progress · Escalated to DevOps · Resolved · Closed |
| Severity | Multi-select: Low · Medium · High · Critical |
| Exam | Searchable select |
| Date Range | Created from/to |
| Assigned to | Me / All |

#### Incidents Table

| Column | Sortable |
|---|---|
| Ticket ref | No — auto ID |
| Exam | Yes |
| Institution | Yes |
| Type | No |
| Severity | Yes (default: DESC) |
| Affected students | Yes |
| Status | No |
| Created | Yes |
| Assigned To | No (role label) |
| Actions | — |

Actions: [View/Edit] · [Resolve] · [Escalate to DevOps] · [Close]

**[+ New Incident]** (header button)

**[Escalate to DevOps]:** opens Escalation Modal. Sets status = `ESCALATED_TO_DEVOPS`. Sends in-app notification to Incident Manager (38) and DevOps on-call. Requires DevOps ticket reference after escalation.

#### Incident Drawer (640px)

**Header:** Exam + Institution + Severity pill + Status pill + [×]

| Field | Notes |
|---|---|
| Incident Type | Select (editable if OPEN) |
| Severity | Select (editable if not RESOLVED) |
| Description | Text area |
| Affected Student Count | Number (estimate) |
| Assigned To | Role-based assignee selector (Support Exec 35 or Ops Manager 34) |
| Status | Workflow: OPEN → IN_PROGRESS → ESCALATED / RESOLVED → CLOSED |
| Resolution | Text area (required for RESOLVED transition) |
| DevOps Ticket Ref | Text (appears when status = ESCALATED_TO_DEVOPS) |

**Activity log (within drawer):** Status changes with timestamp + actor role.

---

### Tab 3 — Actions Log

Immutable log of all operational actions taken on exam schedules (from `exam_ops_action_log`).

#### Filters

| Filter | Control |
|---|---|
| Action Type | Multi-select: Pause · Resume · Extend · Config Lock · Force Close · Result Withhold · Cancel |
| Exam | Searchable select |
| Date Range | — |
| Actor | Role label filter |

#### Actions Log Table

| Column | Sortable |
|---|---|
| Timestamp | Yes (default: DESC) |
| Action Type | No |
| Exam | Yes |
| Institution | Yes |
| By (role) | No (role label — DPDPA) |
| Details | No (action_details rendered) |

Read-only. Pagination: 25 rows.

**Export:** [Download Actions Log CSV] — filtered by current filter state.

---

## 5. Modals

### Pause Exam Modal (480px)

**Trigger:** [Pause Exam] button (card or detail panel)

Header: "Pause Exam — {Exam Name} at {Institution}"

Warning: `bg-[#451A03] border-[#F59E0B]` — "Pausing an exam freezes all active session timers. Students will see a 'Exam paused by administrator' message. Resume the exam to continue — timers will resume from where they were paused."

| Field | Required | Notes |
|---|---|---|
| Pause Reason | Yes | Text area; max 500 chars; logged in `exam_ops_action_log` |
| Notify institutions? | Toggle | Default ON — sends in-app notification to institution admins |

**Pause + in-flight submissions:** Pausing freezes session timers and prevents new submissions. Submissions already in-flight (session `status = SUBMITTING`) will be completed before pause takes effect. F-02 shows: "Waiting up to 30 seconds for in-flight submissions to complete before pausing…" Students see "Exam paused by administrator" immediately; their timer freezes.

**[Pause Exam]** `bg-[#F59E0B] text-black` · [Cancel]

On confirm:
- `exam_schedule.status → PAUSED`
- `paused_at`, `pause_reason`, `paused_by_id` set
- `PAUSE` logged to `exam_ops_action_log`
- ⚠️ "Exam paused — {N} active sessions frozen" toast 8s

### Extend Duration Modal (480px)

**Trigger:** [Extend Time]

Header: "Extend Duration — {Exam Name} at {Institution}"

| Field | Required | Notes |
|---|---|---|
| Extension (minutes) | Yes | Number input; min 1, max 60; cumulative extensions tracked (`extended_by_minutes`) |
| Reason | Yes | Text area |
| Apply to | Radio | This institution only · All institutions with this exam (multi-select if others active) |

**[Extend Time]** `bg-[#6366F1]` · [Cancel]

On confirm:
- `exam_schedule.scheduled_end += extension`
- `extended_by_minutes += extension`
- `EXTEND_DURATION` logged
- ✅ "Exam extended by {N} minutes — new end time: {datetime}" toast 4s

### Resume Exam Modal (400px)

"Resume exam for {N} paused students? Timers will resume from where they were paused."

[Resume Exam] `bg-[#6366F1]` · [Cancel]

### Create Incident Modal (640px)

| Field | Required | Notes |
|---|---|---|
| Exam Schedule | Yes | Pre-filled if opened from exam card |
| Incident Type | Yes | Select |
| Severity | Yes | Select |
| Description | Yes | Text area |
| Affected Student Count | No | Estimate — number input |
| Assign To | Yes | Select from Support Exec (35) / Ops Manager (34) roster |

**[Create Incident]** → `exam_session_incident` created. ✅ "Incident created" toast 4s. Assignee notified via in-app notification.

### Escalate to DevOps Modal (400px)

"Escalate this incident to DevOps / Incident Manager?"

Description of what will happen:
- Status set to ESCALATED_TO_DEVOPS
- Incident Manager (38) notified in-app
- DevOps on-call notified via alert

[DevOps Ticket Reference (optional)] text input

[Escalate] `bg-[#EF4444]` · [Cancel]

---

## 6. Data Model Reference

Full models in `div-f-pages-list.md`:
- `exam_schedule` — status, timing, extension tracking
- `exam_ops_snapshot` — live session aggregations
- `exam_session_incident` — operational incidents
- `exam_ops_action_log` — immutable action history

**`exam_ops_snapshot_history`** (F-02 only — for submission rate chart):
| Field | Type | Notes |
|---|---|---|
| `id` | bigint | Auto-increment |
| `exam_schedule_id` | FK → `exam_schedule` | — |
| `snapshot_at` | timestamptz | — |
| `total_active_sessions` | int | — |
| `total_submitted` | int | — |
| `submit_rate_per_min` | int | — |

Retention: 7 days (Celery Beat purge after exam + 7 days). Not exposed to F-08 analytics — F-08 uses `exam_result_computation` data.

---

## 7. Access Control

| Gate | Rule |
|---|---|
| Page access | All Div F roles + DevOps/SRE (14) |
| Pause/Resume/Extend/Force Close | Exam Ops Manager (34), Platform Admin (10) only |
| Create incidents | Exam Ops Manager (34), Support Exec (35) |
| Escalate to DevOps | Exam Ops Manager (34), Incident Manager (38) |
| Assign incidents | Exam Ops Manager (34) |
| Read-only (all tabs) | DevOps/SRE (14), Results Coordinator (36), Integrity Officer (91) |
| Pause/Extend action buttons | Hidden (not just disabled) for read-only roles |
| Actions Log detail visibility | Full `action_details` JSON shown to: Ops Manager (34), Incident Manager (38), Platform Admin (10). Support Exec (35) sees action type + timestamp only. Integrity Officer (91) sees non-operational details only (no session-level data). |

---

## 8. Edge Cases & Error States

| Scenario | Behaviour |
|---|---|
| Snapshot > 90s old | Red banner above grid: "⚠️ Snapshot data is {N}s old. Celery task may be delayed. [Force Refresh All]". Cards show "Data {N}s old" badge. |
| Celery Beat task down (no snapshot updates) | After 3 missed cycles (90s), red alert banner. Refresh button triggers manual Celery task via `celery.app.control.apply_async`. If Celery unreachable: "⚠️ Cannot refresh — Celery worker unresponsive. Contact DevOps." |
| Pause attempted but exam already completed | "This exam has already ended — pausing is no longer available." |
| Extend attempted for exam with `CONFIG_LOCKED` | Extension is still allowed — it's an operational override, not a config change. Extension is logged separately. |
| 0 active sessions despite exam ACTIVE | Red indicator on card: "No active sessions detected. Verify Celery snapshot or check with institution." Does not auto-pause — Ops Manager decides. |
| Force Close with active sessions | Confirmation modal shows exact active session count: "You are about to force-close an exam with {N} students still active. Their work will be submitted at current state." |
| Two Ops Managers simultaneously pause same exam | Idempotent — second pause request returns "Exam is already paused" toast. No duplicate log entry. |
| Grid has 0 active exams | Empty state: "No exams are running right now." + "Next scheduled exam: {Exam Name} at {Institution} in {time}" |

---

## 9. UI Patterns

### Polling Architecture

```
Browser (HTMX every 30s)
  → GET /ops/exam/monitor/?part=monitor-kpi
  → GET /ops/exam/monitor/?part=monitor-grid
     → Django view → reads exam_ops_snapshot (Memcached 25s TTL)
                   → on cache miss: reads PostgreSQL exam_ops_snapshot

Celery Beat (every 30s during active window)
  → update_exam_ops_snapshots task
     → for each ACTIVE exam_schedule:
        → queries each institution's tenant schema for session counts
        → writes exam_ops_snapshot row
        → appends exam_ops_snapshot_history row
```

**Memcached cache key:** `exam_ops_snapshot_grid_{filter_hash}` · TTL 25s (just under 30s poll)

**[Refresh All] cache bypass:** [Refresh All] triggers `?part=monitor-kpi&nocache=true` + `?part=monitor-grid&nocache=true`. Django view: if `nocache=true`, skips Memcached read, queries PostgreSQL `exam_ops_snapshot` directly, writes fresh result to Memcached with TTL reset. This prevents multiple users all clicking [Refresh All] from cascading direct DB queries — first request updates the cache; subsequent requests within the next 25s get the fresh cached result.

**Celery health check:** F-02 calls `GET /ops/exam/monitor/health/` on page load and every 60s (HTMX). This endpoint pings `celery.app.control.inspect().ping()` with a 3-second timeout. If Celery workers respond: green dot in bottom-right corner "Celery: OK". If no response within 3s: red dot "Celery: Unreachable — contact DevOps." On unreachable: snapshot-age alert escalates from amber to red immediately regardless of actual snapshot age.

### Toast Messages

| Action | Toast |
|---|---|
| Exam paused | ⚠️ "Exam paused — {N} active sessions frozen" (8s) |
| Exam resumed | ✅ "Exam resumed — timers active" (4s) |
| Duration extended | ✅ "Exam extended by {N} min — ends at {time}" (4s) |
| Exam force-closed | ⚠️ "Exam force-closed. {N} sessions submitted." (8s) |
| Incident created | ✅ "Incident created and assigned to {role}" (4s) |
| Incident escalated | ⚠️ "Escalated to DevOps — Incident Manager notified" (8s) |
| Incident resolved | ✅ "Incident resolved" (4s) |
| Snapshot refresh triggered | ℹ️ "Refreshing snapshot…" (6s) |

### Loading States

- **Grid:** 6-card shimmer skeleton (matching card dimensions)
- **KPI strip:** 6 rectangle shimmers
- **Submission rate chart:** flat line placeholder
- **Incident table:** 8-row shimmer

### Responsive

| Breakpoint | Behaviour |
|---|---|
| Desktop (≥1280px) | 3-column card grid; KPI strip 6 tiles |
| Tablet (768–1279px) | 2-column card grid; KPI strip 3+3 tiles |
| Mobile (<768px) | 1-column card stack; KPI tiles scroll horizontal; detail panel = full screen |

---

*Page spec complete.*
*F-02 covers: live exam session monitoring (30s snapshot) → Celery health check → operational triage → pause (in-flight submission handling) → extend/force-close → Override Session (sync Force Submit) → Starting Soon panel (overflow handling) → incident management → actions log (role-based detail visibility). Operationally distinct from Div A War Room.*
