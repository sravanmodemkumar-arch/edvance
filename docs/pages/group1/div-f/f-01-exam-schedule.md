# F-01 — Exam Schedule & Configuration

> **Route:** `/ops/exam/schedule/`
> **Division:** F — Exam Day Operations
> **Primary Role:** Exam Configuration Specialist (90) — full control pre-lock; Exam Operations Manager (34) — approve config lock, monitor
> **Supporting Roles:** Results Coordinator (36) read-only · Exam Integrity Officer (91) read-only · Platform Admin (10) full
> **File:** `f-01-exam-schedule.md`
> **Priority:** P0 — Must be configured before any exam can go live

---

## 1. Page Name & Route

**Page Name:** Exam Schedule & Configuration
**Route:** `/ops/exam/schedule/`
**Part-load routes:**
- `/ops/exam/schedule/?part=schedule-table` — main exam schedule list
- `/ops/exam/schedule/?part=kpi` — KPI strip
- `/ops/exam/schedule/?part=schedule-drawer&id={id}` — exam detail/config drawer
- `/ops/exam/schedule/?part=template-list` — exam template tab
- `/ops/exam/schedule/?part=bulk-form` — bulk scheduling tab
- `/ops/exam/schedule/?part=calendar` — calendar view tab
- `/ops/exam/schedule/?part=config-form&id={id}` — config sub-form within drawer

---

## 2. Purpose

F-01 is the pre-exam configuration hub. Before any exam goes live, the Exam Configuration Specialist (90) must:

1. Create exam schedule records — link an exam to an institution with specific timing
2. Assign the question paper (from Div D question bank)
3. Configure exam parameters: duration, negative marking, section rules, grace period, max attempts, registration window
4. Lock the config (T-24h before start) — prevents further changes
5. Handle institution-specific overrides (e.g., a school that needs extra time for accessibility reasons)

At 2,050 institutions, exam scheduling is a bulk operation. A single national SSC CGL Mock has 300 coaching centres running it simultaneously — F-01 provides batch scheduling, template reuse, and per-institution override management to handle this at scale.

**Business goals:**
- Zero configuration errors reaching exam day — lock gate enforces this
- Batch scheduling reduces manual effort for national exam days
- Institution-specific overrides handled in-platform, not via email/phone

---

## 3. Tabs

| Tab | Label | HTMX |
|---|---|---|
| 1 | Upcoming Schedules | `?part=schedule-table` |
| 2 | Exam Templates | `?part=template-list` |
| 3 | Bulk Scheduling | `?part=bulk-form` |
| 4 | Calendar View | `?part=calendar` |
| 5 | Institution Overrides | `?part=overrides-table` |

---

## 4. Section-Wise Detailed Breakdown

---

### KPI Strip (top of page, all tabs)

| # | Metric | Notes |
|---|---|---|
| 1 | Scheduled (Next 7 days) | Count of `exam_schedule` with status IN (`SCHEDULED`, `CONFIG_LOCKED`) and `scheduled_start ≤ now+7d` |
| 2 | Awaiting Config Lock | Count of schedules where start < T+24h and status = `SCHEDULED` (not yet locked) — amber if > 0 |
| 3 | Active Right Now | Count with status = `ACTIVE` |
| 4 | Exams This Month | Count with `scheduled_start` in current calendar month |

**Awaiting Config Lock tile:** if count > 0, pulse amber border. Clicking applies filter `?filter=awaiting_lock` to Tab 1 (status = SCHEDULED + start < now + 24h + config_locked_at IS NULL). Filter persists in URL and survives page reload.

---

### Tab 1 — Upcoming Schedules

#### Search & Filter Bar

**Search:** institution name, exam name, paper code. Debounced 300ms.

**Filters:**

| Filter | Control |
|---|---|
| Status | Multi-select: Draft · Scheduled · Config Locked · Active · Paused · Completed · Cancelled |
| Exam Type | Multi-select: SSC · RRB · NEET · JEE · AP Board · TS Board · IBPS · SBI · Custom |
| Institution Type | Multi-select: School · College · Coaching · Online Domain |
| Date Range | Scheduled start from/to |
| Config Lock Status | All · Locked · Unlocked · Overdue (should be locked but isn't) |
| Paper Assigned | Assigned · Unassigned |

#### Schedule Table (Sortable, Selectable, Responsive)

| Column | Sortable | Notes |
|---|---|---|
| Exam Name | Yes | From `exam_exam.title` |
| Institution | Yes | Institution name |
| Type | No | Institution type badge: `SCHOOL` · `COLLEGE` · `COACHING` |
| Scheduled Start | Yes (default: ASC) | Absolute datetime + relative: "in 3h", "in 2d" |
| Duration | No | Minutes from `exam_schedule.duration_minutes` |
| Paper | No | Paper code badge or "Unassigned" badge (red if start < T+24h) |
| Status | No | Status pill: `DRAFT` grey · `SCHEDULED` blue · `CONFIG_LOCKED` green · `ACTIVE` green pulse · `PAUSED` amber · `COMPLETED` grey · `CANCELLED` red |
| Config Lock | No | 🔒 Locked / ⚠️ Due in {N}h / — (not due yet) |
| Actions | — | [Configure] · [Lock Config] · [···] |

**[Configure]:** opens Schedule Detail Drawer (760px)
**[Lock Config]:** shown only when status = SCHEDULED and all required fields complete. Confirmation modal required. See Section 6.
**[Reschedule]:** shown only when status = SCHEDULED or CONFIG_LOCKED (not ACTIVE or COMPLETED). Opens Reschedule Modal. Creates a new `exam_schedule` record with `rescheduled_from_id` pointing to the original; marks original as RESCHEDULED status. Student registrations are migrated to the new schedule by Celery task.

**Row selection:** Multi-select via checkbox (column 1). Bulk actions: "Lock selected configs" · "Cancel selected".

**Responsive:**
- Desktop: all columns
- Tablet: Exam Name + Institution + Scheduled Start + Status + Actions
- Mobile: card per row — Exam Name · Institution · Start datetime · Status badge · [Configure] button

**Empty state:** "No exams scheduled in this period. Use 'Bulk Scheduling' tab to create schedules in bulk, or add a single exam from an institution's page." + [Go to Bulk Scheduling]

**Pagination:** 25 rows. Sort state in URL.

---

### Schedule Detail Drawer (760px right panel)

Triggered by [Configure] on any row.

**Header:** Exam name · Institution name · Status pill · [×]

**Drawer Tabs:**

#### Drawer Tab 1 — Overview & Timing

**Read-only summary block:**
- Exam: `{exam_exam.title}`
- Exam type: `{exam_type.name}`
- Institution: `{institution.name}` — `{institution_type}`
- Created by: Role label (DPDPA) + timestamp

**Timing Configuration (editable unless CONFIG_LOCKED or ACTIVE):**

| Field | Control | Validation |
|---|---|---|
| Scheduled Start | Datetime picker | Must be in future when saving as SCHEDULED; cannot be < T+1h |
| Duration (minutes) | Number input | Min 10, max 480; overrides template default |
| Grace Period (minutes) | Number input | Default from `exam_operational_config.grace_period_default_minutes`; min 0, max 60 |
| Max Attempts | Number input | Min 1, max 3; default 1 |
| Registration Opens | Datetime picker | Nullable; must be before scheduled start |
| Registration Closes | Datetime picker | Nullable; must be before scheduled start |
| Timezone | Read-only display | Always IST (Asia/Kolkata) — platform standard |

**Status controls:**
- [Save Timing] — saves timing fields. Not available when CONFIG_LOCKED or ACTIVE.
- **[Confirm Schedule]** — moves status from `DRAFT` → `SCHEDULED`. Enabled when:
  - `scheduled_start` is set and > now + 1 hour
  - `duration_minutes` is set
  - Shows confirmation: "Confirm this exam schedule? It will appear in the calendar and be visible to institution admins." [Confirm] · [Keep as Draft]
  - After confirming: status badge updates to SCHEDULED and config-lock deadline appears.
- Config lock indicator: 🔒 "Locked by {Role} at {datetime}" or "⚠️ Config must be locked before {datetime}"

**Computed fields (read-only):**
- Scheduled End: `start + duration + grace_period`
- "Exam closes at: {datetime}"

#### Drawer Tab 2 — Exam Configuration

**Section A — Question Paper**

| Field | Control | Notes |
|---|---|---|
| Assigned Paper | Searchable dropdown | Shows papers published in Div D for this exam type. Displays paper_code + question_count + marks. "Unassigned" if null. |
| Paper Details (read-only after assignment) | — | Paper code · Total questions · Total marks · Section count |

**Section B — Scoring Rules**

| Field | Control | Validation |
|---|---|---|
| Negative Marking Factor | Number input (decimal) | Default from template; 0 = disabled; 0.25 = standard; 0.33 = 1/3; 1 = equal penalty |
| Marks per Correct Answer | Number input (decimal) | Default from paper config; typically 1 or 2 |
| Partial Marking | Toggle | Default OFF |

**Marks consistency validation:** After entering Marks per Correct Answer, compute read-only preview: "Max possible score: {marks_per_correct × total_questions} marks." If this exceeds `exam_question_paper.total_marks`, show red inline: "⚠️ This marks value would allow a maximum of {N} marks, exceeding the paper's total ({M}). Adjust marks or verify paper config."

**Section C — Section-Level Config** (shown only if paper has sections)

For each section in the paper:

| Field | Control |
|---|---|
| Section name (read-only) | — |
| Questions in section (read-only) | — |
| Section time limit (minutes) | Number input (nullable); 0 = no section limit |
| Mandatory section | Toggle |
| Min questions to attempt | Number input (nullable) |

**[Save Exam Config]** — saves all Section A/B/C fields. Validation: paper must be assigned before saving; negative marking factor must be ≥ 0.

#### Drawer Tab 3 — Institution Override

Overrides applied specifically for this institution-exam combination.

| Override | Control | Notes |
|---|---|---|
| Extra time (minutes) | Number input (0 by default) | Added to duration; for accessibility/special cases; logged in `exam_ops_action_log` |
| Override reason | Text area | Required if extra time > 0 |
| Allow late entry (minutes) | Number input (0 by default) | Grace to start after scheduled start |
| VIP priority flag | Toggle | Fast-tracks support tickets from this institution to HIGH |

**[Save Override]** → logs to `exam_ops_action_log` with action type = `INSTITUTION_OVERRIDE_SET`.

#### Drawer Tab 4 — Config Lock

Pre-lock checklist (all must be green before locking):

| Check | Condition |
|---|---|
| ✅ / ❌ Question paper assigned | `paper_id IS NOT NULL` |
| ✅ / ❌ Negative marking configured | `negative_marking_factor IS NOT NULL` |
| ✅ / ❌ Duration set | `duration_minutes IS NOT NULL` |
| ✅ / ❌ Start time in future | `scheduled_start > now()` |
| ✅ / ❌ Paper published (not draft) | `exam_question_paper.status = PUBLISHED` |
| ⚠️ / ✅ Registration window set | Nullable — warning only if not set |

**[Lock Configuration]** button — enabled only when all ❌ checks resolved.
- Opens confirmation modal: "Lock this exam configuration? No further changes will be allowed after locking. Duration, paper, and scoring rules will be frozen."
- On confirm: `exam_schedule.status → CONFIG_LOCKED`, `config_locked_at` set, `config_locked_by_id` set.
- Logs `CONFIG_LOCK` to `exam_ops_action_log`.
- ✅ "Exam configuration locked" toast 4s.

**[Unlock Configuration]** — shown only to Exam Operations Manager (34). Requires reason. Logs `CONFIG_UNLOCK`. Sets status back to SCHEDULED. Used only in emergencies (e.g., wrong paper assigned post-lock).

#### Drawer Tab 5 — Activity Log

Immutable log of all changes to this schedule.

| Column | Notes |
|---|---|
| Timestamp | Absolute datetime |
| Action | Action type in human-readable form |
| By | Role label (DPDPA) |
| Details | Action-specific details |

Read-only. Paginated: 20 rows.

---

### Tab 2 — Exam Templates

Templates allow reuse of common exam configurations. Creating a schedule from a template pre-fills all config fields.

#### Template Table

| Column | Sortable |
|---|---|
| Template Name | Yes |
| Exam Type | No |
| Duration | No |
| Negative Marking | No |
| Sections | No |
| Used In (schedule count) | Yes |
| Actions | — |

Actions: [Use Template] · [Edit] · [Duplicate] · [Archive]

**[Use Template]** → opens Create Schedule Modal (560px) with template fields pre-filled. See Section 6.

**[+ New Template]** → Create Template Modal.

#### Create / Edit Template Modal (560px)

| Field | Required | Notes |
|---|---|---|
| Template Name | Yes | Unique; max 100 chars |
| Exam Type | Yes | Select from exam_type list |
| Duration (minutes) | Yes | Min 10, max 480 |
| Negative Marking Factor | Yes | Default 0.25 |
| Grace Period (minutes) | No | Default from `exam_operational_config` |
| Max Attempts | No | Default 1 |
| Sections Config | No | JSON-editable grid: section name + question_count + time_limit |
| Description | No | Max 300 chars |

**[Save Template]** → ✅ "Template saved" toast 4s.

---

### Tab 3 — Bulk Scheduling

Schedules the same exam for multiple institutions simultaneously. Reduces manual effort on national exam days (SSC CGL mock → 300 coaching centres → one operation).

#### Step 1 — Select Exam

- Searchable dropdown: select `exam_exam`
- Shows: exam name, type, estimated institutions

#### Step 2 — Select Institutions

- Filter by institution type: All · School · College · Coaching · Online Domain
- Searchable multi-select list of institutions
- "Select all Coaching Centres" button
- Preview: "Scheduling for {N} institutions"

#### Step 3 — Common Config

| Field | Notes |
|---|---|
| Scheduled Start | Applied to all selected institutions |
| Duration (minutes) | Default from template; can override |
| Exam Template | Optional: select to pre-fill scoring rules |
| Question Paper | Select paper to assign to all |
| Negative Marking Factor | Applies to all |
| Grace Period | Applies to all |

**Institution-specific overrides (optional):** "Add per-institution override" expando — allows setting different start times or durations for specific institutions within the bulk batch. Shown as a sub-table: Institution | Override Start | Override Duration | Override Reason.

#### Step 4 — Preview & Submit

Summary table:
| Institution | Type | Scheduled Start | Duration | Paper | Override |
|---|---|---|---|---|---|
| SR Coaching | Coaching | 2026-04-10 10:00 IST | 90 min | CGL-2026-SET-A | — |
| VR Academy | Coaching | 2026-04-10 10:00 IST | 90 min | CGL-2026-SET-A | +15 min extra time |
| … | … | … | … | … | — |

Conflict detection: if any institution already has an overlapping exam scheduled, it's highlighted red: "⚠️ SR Academy already has an exam at 09:45 AM — this would overlap."

**[Confirm Bulk Schedule]** → creates `exam_schedule` records for all institutions. Shows progress indicator if batch > 50 institutions. ✅ "{N} exams scheduled" toast.

**Zero-institution validation:** [Confirm Bulk Schedule] is disabled if selected institution count = 0. Inline message: "Select at least 1 institution to proceed." Shown below the institution list in Step 2.

**Conflict detection with per-institution overrides:** After a per-institution override sets a different start time in Step 3, the conflict detection algorithm in Step 4 re-runs using each institution's **effective** start/end time (base schedule ± override). Example: if base start = 10:00 and institution A has +30 min start override, conflict check uses 10:30 as institution A's start.

---

### Tab 4 — Calendar View

A calendar grid of all scheduled exams to spot conflicts and cluster density.

**Header controls:** Month/Week toggle · Jump to date · Filter by exam type

**Month view:**
- Each day cell shows exam count badges by type (e.g., "SSC ×3 · NEET ×1")
- Clicking a day expands to day-detail panel: list of exams that day with institution name, time, status

**Week view:**
- Horizontal timeline (00:00–23:59 IST)
- Each exam shown as a horizontal bar spanning its duration
- Color-coded by status: blue = SCHEDULED, green = CONFIG_LOCKED, amber = needs attention
- Overlap detection: exams of same type at same time shown stacked

**Click on exam bar:** opens Schedule Detail Drawer (same as Tab 1 row click).

---

### Tab 5 — Institution Overrides

A consolidated view of all per-institution overrides applied across all scheduled exams.

#### Overrides Table

| Column | Sortable |
|---|---|
| Exam | Yes |
| Institution | Yes |
| Override Type | No (Extra Time · Late Entry · VIP Flag) |
| Value | No |
| Reason | No |
| Applied By | No (role label) |
| Applied At | Yes |
| Actions | — |

Actions: [View Exam] · [Edit Override] · [Remove Override]

**Removing an override:** requires confirmation. Logs to `exam_ops_action_log`. Not available if CONFIG_LOCKED.

---

## 5. Modals

### Create Schedule Modal (560px)

**Trigger:** [+ New Schedule] button (header), or [Use Template] in Tab 2.

| Field | Required | Notes |
|---|---|---|
| Exam | Yes | Searchable dropdown from `exam_exam` |
| Institution | Yes | Searchable dropdown from institution list |
| Scheduled Start | Yes | Datetime picker; must be ≥ 1 hour in future |
| Template (pre-fill config) | No | Selecting auto-fills duration, negative marking, etc. |
| Duration (minutes) | Yes | Min 10, max 480 |
| Question Paper | No | Can assign now or later in drawer |

**[Create Schedule]** → creates `exam_schedule` with status = `DRAFT`. Opens Schedule Detail Drawer for full configuration. ✅ "Schedule created — configure exam settings before locking" toast.

### Config Lock Confirmation Modal (400px)

**Trigger:** [Lock Configuration] in Drawer Tab 4.

"You are about to lock the exam configuration for **{Exam Name}** at **{Institution}** scheduled for **{datetime}**.

After locking:
- Question paper, duration, and scoring rules **cannot be changed**
- Institution override settings **can still be modified** (extra time, etc.)
- Only an Exam Operations Manager can unlock (emergency only)

Lock configuration now?"

[Confirm Lock] `bg-[#6366F1]` · [Cancel]

### Reschedule Modal (480px)

**Trigger:** [Reschedule] in table row Actions.

"Rescheduling creates a new exam schedule and marks the current one as RESCHEDULED. Student registrations will be migrated to the new schedule."

| Field | Required | Notes |
|---|---|---|
| New Scheduled Start | Yes | Must be ≥ 1 hour in future |
| Reason for Reschedule | Yes | Text area — logged in `exam_ops_action_log` |
| Notify institution? | Toggle | Default ON — creates in-app notification to institution admin |

**[Confirm Reschedule]** → creates new `exam_schedule` with `rescheduled_from_id = original.id`, original status → RESCHEDULED, Celery task migrates student registrations. ✅ "Schedule rescheduled — new schedule created for {datetime}" toast 4s.

### Config Unlock Confirmation Modal (400px)

**Trigger:** [Unlock Configuration] in Drawer Tab 4 — Ops Manager (34) only.

"⚠️ Unlock exam configuration for **{Exam Name}** at **{Institution}**?

This reverses the config lock gate. The exam can be reconfigured until re-locked. **This is an emergency action — exams within 30 minutes of start cannot be unlocked.**

After unlocking:
- Config Specialist (90) can edit paper, duration, and scoring rules
- You must re-lock before the exam starts"

| Field | Required | Notes |
|---|---|---|
| Unlock Reason | Yes | Text area; min 30 chars — logged permanently in `exam_ops_action_log` |
| Notify Config Specialist? | Toggle | Default ON — in-app notification to Config Specialist (90): "Config unlocked for {Exam} — review and re-lock before exam starts." |

[Confirm Unlock] `bg-[#EF4444]` · [Cancel]

**On confirm:** `exam_schedule.status → SCHEDULED`, `config_locked_at` and `config_locked_by_id` cleared, `CONFIG_UNLOCK` logged to `exam_ops_action_log`.
⚠️ "Config unlocked — lock again before exam starts" toast 8s.

**Hard block:** Cannot unlock if `scheduled_start ≤ now() + 30 min`. Show: "Cannot unlock — exam starts in less than 30 minutes. Emergency changes must go through Platform Admin."

---

### Bulk Cancel Modal (400px)

**Trigger:** Bulk selection → "Cancel selected"

"Cancel {N} selected exam schedules? This cannot be undone. Institutions will need to be notified separately via F-06 Notification Hub."

[Confirm Cancel] `bg-[#EF4444]` · [Cancel]

---

## 6. Data Model Reference

### `exam_schedule` — Status State Machine

Valid transitions (enforced server-side):

```
DRAFT ──[Confirm Schedule]──────────────────────────────► SCHEDULED
                                                               │
SCHEDULED ──[Lock Config]──────────────────────────────► CONFIG_LOCKED
                                                               │
                         ──[auto_activate_exam Celery]──► ACTIVE ──[Pause]──► PAUSED
                                                               │                  │
                                                               │ ◄──[Resume]──────┘
                                                               │
CONFIG_LOCKED or SCHEDULED ──[Cancel]──► CANCELLED            │
SCHEDULED or CONFIG_LOCKED ──[Reschedule]──► RESCHEDULED       │
                                                               ▼
                                         ──[auto_complete_exam]──► COMPLETED
```

**Rules:**
- Only Exam Config Specialist (90) can CONFIRM (DRAFT → SCHEDULED) and LOCK (SCHEDULED → CONFIG_LOCKED)
- Only Ops Manager (34) can UNLOCK (CONFIG_LOCKED → SCHEDULED, emergency only)
- `auto_activate_exam` and `auto_complete_exam` are Celery Beat tasks (if enabled in F-09 config)
- CANCELLED and RESCHEDULED are terminal states — no further transitions
- PAUSED is only possible from ACTIVE; RESUME sends back to ACTIVE with `resumed_at` set

**`exam_schedule`** — full definition in `div-f-pages-list.md`

**`exam_question_paper`** (referenced from Div D):
| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `exam_id` | FK → `exam_exam` | — |
| `paper_code` | varchar(50) | Unique identifier e.g. `CGL-2026-SET-A` |
| `total_questions` | int | — |
| `total_marks` | decimal | — |
| `sections_config` | jsonb | `[{"name": "General Intelligence", "question_count": 25, "marks": 50, "time_limit_minutes": null}]` |
| `status` | varchar | Enum: `DRAFT` · `PUBLISHED` · `ARCHIVED` — only PUBLISHED papers available in F-01 dropdown |

**`exam_schedule_template`**:
| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `name` | varchar(100) | Unique |
| `exam_type_id` | FK → `exam_type` | — |
| `duration_minutes` | int | — |
| `negative_marking_factor` | decimal | — |
| `grace_period_minutes` | int | — |
| `max_attempts` | int | Default 1 |
| `sections_config` | jsonb | — |
| `description` | varchar(300) | Nullable |
| `is_archived` | boolean | Default False |
| `created_by_id` | FK → auth.User | — |
| `created_at` | timestamptz | — |
| `use_count` | int | Denormalised for display |

---

## 7. Access Control

| Gate | Rule |
|---|---|
| Page access | Exam Config Specialist (90), Ops Manager (34), Results Coordinator (36), Integrity Officer (91), Platform Admin (10) |
| Create/edit schedule | Exam Config Specialist (90), Platform Admin (10) |
| Lock/unlock config | Config lock: Exam Config Specialist (90). Config **unlock**: Ops Manager (34) only |
| Bulk scheduling | Exam Config Specialist (90) only |
| Create/edit templates | Exam Config Specialist (90) only |
| Institution overrides | Exam Config Specialist (90), Ops Manager (34) |
| Read-only (all tabs) | Results Coordinator (36), Integrity Officer (91) |
| "You have read-only access" banner | Results Coordinator (36), Integrity Officer (91) |

---

## 8. Edge Cases & Error States

| Scenario | Behaviour |
|---|---|
| Config lock attempted with unassigned paper | Block: "Cannot lock — question paper is not assigned. Assign a published paper first." |
| Config lock attempted with start < 30 min away | Block: "Cannot lock — exam starts in less than 30 minutes. Contact Ops Manager for emergency protocol." |
| DRAFT schedule with `scheduled_start` in the past | [Confirm Schedule] is blocked: "Cannot confirm — scheduled start time is in the past. Update start time before confirming." Schedule remains DRAFT. Shown as "Overdue DRAFT" amber row in Tab 1 table. |
| [Confirm Schedule] when start < now + 1h | Block: "Cannot confirm — exam starts too soon (less than 1 hour). Reschedule or contact Ops Manager." |
| Bulk schedule: institution already has overlapping exam | Row highlighted red in Step 4 preview. User must explicitly check "Proceed despite overlap" per institution, or deselect them. Not a hard block — business may intentionally schedule back-to-back. |
| Edit attempted on CONFIG_LOCKED schedule | All form fields disabled. Tooltip: "Config is locked. Contact Exam Operations Manager to unlock if change is required." |
| Bulk schedule creates > 200 schedules | Progress modal with Celery task progress: "Created {N} of {total} schedules…" — polling `?part=bulk-progress&task_id={id}` every 3s. |
| Paper status changes to ARCHIVED after assignment | Warning banner in drawer: "⚠️ Assigned paper {code} has been archived in the question bank. Verify with Content team before exam goes live." — no auto-block. |
| Two specialists edit same schedule simultaneously | Last write wins. Footer shows "Last saved by {role} at {time}". On conflict: "This schedule was updated by another session since you opened it. Reload?" |

---

## 9. UI Patterns

### Forms with Validation
- Required fields: red border + "Required" on blur
- Date conflicts: "This start time overlaps with another exam at this institution"
- Negative marking < 0: "Factor must be 0 or greater"
- All client-side first; server-side re-validates on save

### Toast Messages

| Action | Toast |
|---|---|
| Schedule created | ✅ "Schedule created" (4s) |
| Timing saved | ✅ "Timing updated" (4s) |
| Config saved | ✅ "Exam configuration saved" (4s) |
| Config locked | ✅ "Exam configuration locked" (4s) |
| Config unlocked | ⚠️ "Config unlocked — lock again before exam starts" (8s) |
| Bulk schedule complete | ✅ "{N} schedules created" (4s) |
| Schedule cancelled | ✅ "Schedule cancelled" (4s) |
| Validation error | ❌ Per field — no toast |

### Responsive

| Breakpoint | Behaviour |
|---|---|
| Desktop (≥1280px) | Full table with all columns; drawer 760px |
| Tablet (768–1279px) | Table: Exam + Institution + Start + Status + Actions only; drawer full-width |
| Mobile (<768px) | Card layout; drawer = full screen bottom sheet |

**Drawer Tab 2 — Section C (Section-Level Config) on tablet/mobile:** Section grid becomes scrollable table with sticky Section Name column. Each row = one section; columns: Section · Questions · Time Limit · Mandatory · Min Attempt. Horizontal scroll if > 4 sections.

---

*Page spec complete.*
*F-01 covers: schedule creation → per-exam config (with marks consistency validation) → bulk scheduling (zero-institution guard, override-aware conflict detection) → config lock gate → Config Unlock Modal → institution overrides → calendar view → state machine (DRAFT past-start guard).*
