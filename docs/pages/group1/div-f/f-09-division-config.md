# F-09 — Division Config

> **Route:** `/ops/exam/config/`
> **Division:** F — Exam Day Operations
> **Primary Role:** Exam Operations Manager (34) — full control over operational settings
> **Supporting Roles:** Exam Config Specialist (90) — read; Platform Admin (10) — full
> **File:** `f-09-division-config.md`
> **Priority:** P2 — Must be configured before first exam goes live; infrequent changes thereafter

---

## 1. Page Name & Route

**Page Name:** Division Config
**Route:** `/ops/exam/config/`
**Part-load routes:**
- `/ops/exam/config/?part=exam-day-settings` — exam day settings tab
- `/ops/exam/config/?part=result-config` — result computation config tab
- `/ops/exam/config/?part=notification-config` — notification defaults tab
- `/ops/exam/config/?part=sla-config` — support SLA targets tab
- `/ops/exam/config/?part=change-log` — config change log tab

---

## 2. Purpose

F-09 is the settings page for the Division F operational pipeline. It controls the singleton `exam_operational_config` record and propagates changes to all Division F pages and Celery tasks.

**Who needs this page:**
- Exam Operations Manager (34) — the primary decision-maker for operational policies
- Platform Admin (10) — for emergency changes

**When is it used:**
- Initial platform setup (before first exam)
- After an incident reveals a policy gap (e.g., grace period too short → adjust default)
- Regulatory change (e.g., objection window extended by TRAI/Education Ministry)
- Scale adjustment (e.g., notification rate raised after Infrastructure upgrade)

**Changes here affect:**
- All new exam schedules (grace period, max objections, SLA timers)
- Celery Beat task frequencies
- F-02 polling intervals
- F-06 send rate limits
- F-03 SLA countdown calculations

---

## 3. Tabs

| Tab | Label |
|---|---|
| 1 | Exam Day Settings |
| 2 | Result & Answer Key Config |
| 3 | Notification Config |
| 4 | Support SLA Targets |
| 5 | Change Log |

---

## 4. Section-Wise Detailed Breakdown

---

### Tab 1 — Exam Day Settings

Configuration for live exam operations (F-01, F-02 behaviour).

#### Section A — Monitoring & Snapshot

| Setting | Control | Default | Notes |
|---|---|---|---|
| Snapshot update frequency (seconds) | Number input | 30 | How often Celery Beat updates `exam_ops_snapshot` during active exams. Min 15, max 120. Lower = more DB load. |
| Start snapshot monitoring (hours before exam) | Number input | 1 | How many hours before `scheduled_start` Celery begins taking snapshots |
| Stop snapshot monitoring (hours after exam) | Number input | 2 | How many hours after exam `actual_end` Celery stops snapshots |

**Warning note:** "Reducing snapshot frequency below 30s increases PostgreSQL query load significantly at 74K concurrent. Engineering (Div C) must confirm DB capacity before reducing."

#### Section B — Exam Defaults

| Setting | Control | Default | Notes |
|---|---|---|---|
| Default grace period (minutes) | Number input | 10 | Applied to all new exam schedules unless overridden in F-01. Min 0, max 60. |
| Max allowed extension per exam (minutes) | Number input | 30 | Maximum cumulative extension an Ops Manager can grant for one exam. Prevents runaway extensions. |
| Config lock required before go-live | Toggle (locked ON) | ON | Platform policy — cannot be disabled. Exams without CONFIG_LOCKED status cannot be made ACTIVE. |
| Config lock deadline (hours before start) | Number input | 24 | How many hours before `scheduled_start` the config must be locked. Shown as deadline in F-01. Min 1, max 72. |
| Auto-transition to ACTIVE on start time | Toggle | ON | If ON: Celery task `auto_activate_exam` fires at `scheduled_start` and sets `exam_schedule.status → ACTIVE`. If OFF: `auto_activate_exam` is not queued for new exams — requires manual activation in F-01. |
| Auto-transition to COMPLETED on end time | Toggle | ON | If ON: Celery task `auto_complete_exam` fires at `scheduled_end + grace_period_minutes` and sets `exam_schedule.status → COMPLETED`. If OFF: requires manual completion in F-01. |

#### Section C — Integrity Defaults

| Setting | Control | Default | Notes |
|---|---|---|---|
| Auto-escalate flags threshold | Number input | 5 | If `flag_count ≥ N` for HIGH severity flags: Celery auto-creates a malpractice case DRAFT. |
| Result withhold requires dual approval | Toggle (locked ON) | ON | Platform policy — Integrity Officer + Ops Manager must both approve. Cannot be disabled. |
| Auto-create integrity case on manual proctor flag | Toggle | OFF | If ON: any manual proctor flag automatically creates a draft case (aggressive setting). |

**[Save Exam Day Settings]** → updates `exam_operational_config` singleton. Logs to change log. ✅ "Exam day settings saved" toast 4s.

#### Section D — Automation Task Health (read-only)

Live status of the critical Celery Beat tasks that power Division F automation. Refreshed on page load and every 60s via HTMX.

| Task | Schedule | Last Run | Last Run Ago | Next Run | Status |
|---|---|---|---|---|---|
| `auto_activate_exam` | Per exam `scheduled_start` | {datetime or `—`} | {e.g. "2h ago"} | {datetime or Disabled} | ✅ OK / ❌ FAILED / — Disabled |
| `auto_complete_exam` | Per exam `scheduled_end + grace` | {datetime or `—`} | {e.g. "45m ago"} | {datetime or Disabled} | ✅ OK / ❌ FAILED / — Disabled |
| `update_exam_ops_snapshots` | Every {snapshot_frequency}s | {datetime} | {e.g. "28s ago"} | {datetime} | ✅ OK / ❌ FAILED |
| `close_answer_key_objection_window` | Per objection window close | {datetime or `—`} | {e.g. "3h ago"} | {datetime or `—`} | ✅ OK / ❌ FAILED |
| `auto_close_support_tickets` | Nightly 02:00 IST | {datetime} | {e.g. "6h ago"} | Next 02:00 IST | ✅ OK / ❌ FAILED |

**Stale detection:** If `update_exam_ops_snapshots` last ran > 4 minutes ago (8× the snapshot frequency at 30s default), or `auto_activate_exam` / `auto_complete_exam` should have run but hasn't (exam `scheduled_start` is in the past and status is still SCHEDULED): row shows ⚠️ amber "Expected to run — may be delayed." Section D refreshes every 30s via HTMX.

**Status rules:**
- `✅ OK` — last run completed successfully (Celery task result = SUCCESS)
- `❌ FAILED` — last run raised an exception; red badge; in-app notification sent to Ops Manager (34) and Platform Admin (10) automatically
- `— Disabled` — shown when the corresponding toggle (Section B) is OFF
- `—` (dash) — task has not run yet (e.g., no exam scheduled today)

**[View Celery Logs]** (Platform Admin only): opens read-only log drawer showing last 20 task executions with task_id, started_at, duration, and result/exception for the selected task row.

**Note:** This section is **read-only** — it reflects the Celery worker's reported state. Task health issues require DevOps/Engineering (Div C) intervention if Celery workers are down. Ops Manager can toggle tasks on/off (Section B) but cannot directly restart Celery workers from F-09.

---

### Tab 2 — Result & Answer Key Config

Configuration affecting F-04 and F-05 behaviour.

#### Section A — Result Computation

| Setting | Control | Default | Notes |
|---|---|---|---|
| Auto-compute on exam complete | Toggle | ON | If ON: Celery queues `compute_exam_results` automatically when `exam_schedule.status → COMPLETED`. Coordinator still must review + approve before publish. |
| Result review window (hours) | Number input | 48 | After computation COMPLETED, how long coordinator has to review before a warning appears in F-04. Min 1, max 168 (7 days). |
| Default computation method | Select: Raw Marks · Percentile · Normalized | Raw Marks | Pre-selected in F-04 computation modal. Can be overridden per exam. |

#### Section B — Answer Key & Objections

| Setting | Control | Default | Notes |
|---|---|---|---|
| Objection window (hours after key publish) | Number input | 72 | How long institutions can file objections after answer key is published. Min 24, max 168. |
| Max objections per institution per exam | Number input | 20 | Hard limit enforced by institution portal. Min 1, max 100. |
| Auto-close objection window | Toggle | ON | Celery auto-closes window at `objection_window_close_at`. If OFF: manual close required in F-05. |
| Require provisional key before final | Toggle (locked ON) | ON | Platform policy — FINAL key cannot be published without first publishing PROVISIONAL. |

#### Section C — Result Publication

| Setting | Control | Default | Notes |
|---|---|---|---|
| Allow provisional result publication | Toggle | ON | If ON: Results Coordinator can publish provisional results (with banner to students). |
| Auto-send result notification on publish | Toggle | OFF | If ON: `result_announcement_en` template broadcast auto-triggered when results published. Requires template to be ACTIVE in F-06. Ops Manager must have reviewed before enabling. |

**[Save Result Config]** ✅ "Result settings saved" toast 4s.

---

### Tab 3 — Notification Config

Configuration affecting F-06 Notification Hub.

#### Section A — Send Rate & Quotas

| Setting | Control | Default | Notes |
|---|---|---|---|
| WhatsApp send rate (messages/min) | Number input | 5,000 | Max WhatsApp messages Celery sends per minute. Controlled by Meta API tier. Contact Engineering before raising. |
| SMS send rate (messages/min) | Number input | 5,000 | — |
| Daily WhatsApp quota | Number input | 150,000 | Platform-level daily limit. Alert at 70% and 90%. |
| Daily SMS quota | Number input | 200,000 | — |
| OTP WhatsApp reservation | Number input | 5,000 | Reserved from daily quota — cannot be used by broadcast sends. Min 1,000. |
| OTP SMS reservation | Number input | 5,000 | — |

**Engineering note (inline):** "WhatsApp rate limit is set by Meta Business API tier. Increasing above current tier capacity causes 429 errors. Contact DevOps/Engineering (Div C) before modifying rate limits."

#### Section B — Broadcast Approval Policy

| Setting | Control | Default | Notes |
|---|---|---|---|
| Require approval for broadcasts > {N} recipients | Number input | 10,000 | Broadcasts above this threshold require Ops Manager (34) approval before send. |
| Large broadcast confirmation threshold | Number input | 50,000 | Broadcasts above this additionally require explicit quota impact confirmation. |
| Auto-cancel stale pending broadcasts (hours) | Number input | 24 | Broadcasts in PENDING_APPROVAL state auto-cancelled after N hours if not approved. 0 = disabled. |

**[Save Notification Config]** ✅ "Notification settings saved" toast 4s.

---

### Tab 4 — Support SLA Targets

Configuration affecting F-03 Support Console SLA timers.

#### SLA Targets Table (Editable inline)

| Priority | SLA Target (minutes) | Current | Notes |
|---|---|---|---|
| CRITICAL | Number input | 5 | Student locked out during active exam — fastest |
| HIGH | Number input | 15 | Session stuck, submission failure |
| MEDIUM | Number input | 30 | Login issues, question not loading |
| LOW | Number input | 60 | Timer mismatch, non-urgent queries |

**Validation:** CRITICAL must be < HIGH < MEDIUM < LOW. Min 1 minute per level.

**Impact note:** "SLA timers apply to all new tickets from the time of saving. Existing open tickets retain their original SLA deadlines."

#### Section B — Auto-Assignment Policy

| Setting | Control | Default | Notes |
|---|---|---|---|
| Auto-assign CRITICAL tickets | Toggle | ON | If ON: unassigned CRITICAL tickets auto-assigned to Support Exec with fewest open CRITICAL tickets after 2 min. |
| Auto-escalate to Incident (unresolved after N min) | Number input | 30 | Unresolved HIGH/CRITICAL tickets auto-escalated to `exam_session_incident` after this many minutes. 0 = disabled. |

**[Save SLA Config]** ✅ "SLA settings saved" toast 4s.

---

### Tab 5 — Change Log

Read-only audit trail of all configuration changes.

#### Filter Bar

| Filter | Control |
|---|---|
| Tab | Multi-select: Exam Day · Result · Notification · SLA |
| Changed By | Role label filter |
| Date Range | — |

#### Change Log Table

| Column | Sortable | Notes |
|---|---|---|
| Timestamp | Yes (default: DESC) | — |
| Tab / Setting | No | e.g. "Exam Day Settings — Grace Period" |
| Change | No | "{Before} → {After}" |
| Changed By | No | Role label (DPDPA) |

Pagination: 25 rows. **Export:** [Download Change Log CSV].

---

## 5. Data Model Reference

**`exam_operational_config`** — full definition in `div-f-pages-list.md`. This page manages all fields of that singleton.

**`exam_operational_config_log`**:
| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `tab` | varchar | Enum: `EXAM_DAY` · `RESULT` · `NOTIFICATION` · `SLA` |
| `setting_key` | varchar | e.g. `grace_period_default_minutes` |
| `old_value` | text | JSON-encoded |
| `new_value` | text | JSON-encoded |
| `changed_by_id` | FK → auth.User | — |
| `changed_at` | timestamptz | — |
| `note` | varchar(300) | Optional reason |

---

## 6. Access Control

| Gate | Rule |
|---|---|
| Page access | Ops Manager (34), Config Specialist (90), Platform Admin (10) |
| Edit all settings | Ops Manager (34), Platform Admin (10) |
| Read-only | Config Specialist (90) |
| "You have read-only access" banner | Config Specialist (90) |
| Locked settings (platform policy) | Visible but non-editable for all roles. Tooltip: "This setting is a platform policy and cannot be changed." |
| View Automation Task Health (Section D) | Ops Manager (34), Config Specialist (90), Platform Admin (10) |
| [View Celery Logs] action in Section D | Platform Admin (10) only |

---

## 7. Edge Cases & Error States

| Scenario | Behaviour |
|---|---|
| Snapshot frequency reduced to < 15s | Validation block: "Snapshot frequency below 15s is not allowed. This would overload PostgreSQL at exam scale. Min: 15s." |
| Auto-compute disabled but exam completes | Coordinator sees exam in F-04 Computation Queue with banner: "Auto-compute is disabled — trigger computation manually." |
| Auto-compute toggle changed mid-exam | Toggle change takes effect for **new exams starting after the change**. Active exams retain the config state from when they were scheduled. Rationale: changing auto-compute mid-exam would create inconsistent behaviour for exams in progress. Recommendation: avoid toggling during exam window. |
| Config lock deadline changed retroactively | New deadline applies only to exam schedules **created after the config change**. Existing DRAFT/SCHEDULED exams retain the deadline computed at their creation time. No bulk retroactive update — manage per-exam in F-01 if needed. |
| SLA CRITICAL > SLA HIGH | Inline validation: "CRITICAL SLA must be less than HIGH SLA. ({N} > {M})" |
| Two Ops Managers edit config simultaneously | Last write wins. "Config was updated by another session since you opened this page. Reload to see latest values before saving." |
| Notification rate raised above API tier capacity | No server-side block — Engineering (Div C) must manage API tier. Warning inline: "Ensure Meta API tier supports this rate. Contact DevOps before raising." |
| Config save during active exam | Settings saved immediately. Changes to snapshot frequency and grace period apply to new exam schedules only. Active exams retain original settings (documented in section save confirmation toast). |
| `auto_activate_exam` task fails at scheduled start | Exam remains SCHEDULED. F-02 "Starting Soon" panel shows ⚠️ "Auto-activation failed — activate manually in F-01." In-app alert sent to Ops Manager (34). `❌ FAILED` shown in Section D. |
| `auto_complete_exam` task fails at scheduled end | Exam remains ACTIVE beyond intended end time. F-02 shows the exam as overrunning. Ops Manager must manually complete in F-01. In-app alert sent. |
| Both auto-transition toggles turned OFF | F-09 shows inline confirmation: "Disabling auto-transitions requires manual activation and completion for every exam. Confirm?" — prevents accidental disablement. |

---

## 8. UI Patterns

### Forms with Validation

- Required fields: red border + "Required" on blur
- Range errors: "Must be between {min} and {max}"
- Interdependency errors (SLA order): inline per field
- Locked fields: `opacity-60 cursor-not-allowed` with lock icon + tooltip

### Toasts

| Action | Toast |
|---|---|
| Exam day settings saved | ✅ "Exam day settings saved — applies to new exams" (4s) |
| Result config saved | ✅ "Result settings saved" (4s) |
| Notification config saved | ✅ "Notification settings saved" (4s) |
| SLA config saved | ✅ "SLA targets updated — applies to new tickets" (4s) |
| Concurrent edit conflict | ⚠️ "Config updated by another session. Reload before saving." (8s) |

### Loading States

- Each tab: form skeleton (label + input shimmer × 6 rows)
- Change log: 8-row shimmer

### Responsive

| Breakpoint | Behaviour |
|---|---|
| Desktop (≥1280px) | Two-column form (label left, input right) |
| Tablet | Single-column form |
| Mobile | Single-column; read-only recommendation banner: "Settings are best edited on desktop" |

---

*Page spec complete.*
*F-09 covers: exam day monitoring thresholds → exam defaults (grace period, config lock deadline) → auto_activate_exam / auto_complete_exam Celery task toggles → Automation Task Health panel → integrity auto-escalation → result computation defaults → objection window → notification rate limits → support SLA targets → change log.*
