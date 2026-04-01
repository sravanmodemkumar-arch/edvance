# I-05 — Onboarding Tracker

**Route:** `GET /support/onboarding/`
**Method:** Django CBV (`ListView`) + HTMX part-loads
**Primary roles:** Onboarding Specialist (#51), Support Manager (#47)
**Also sees (read):** Training Coordinator (#52)
**No access:** L1 (#48), L2 (#49), L3 (#50), Support Quality Lead (#108)

---

## Purpose

Institution onboarding pipeline management. Tracks every institution from contract signing to active platform usage. The Onboarding Specialist manages stage progression, checklist completion, and training session scheduling. At scale: up to 2,050 institutions could have onboarding records (though most will be COMPLETED or LIVE).

---

## Data Sources

| Section | Source |
|---|---|
| Stage counts | `onboarding_instance` grouped by stage; 5-min Memcached TTL |
| Onboarding table | `onboarding_instance` JOINed with `institution`; server-side paginated |
| Checklist items | `onboarding_checklist_template` + `onboarding_checklist_progress` |
| Training sessions | `onboarding_training_session` WHERE `instance_id=` |

---

## URL Parameters

| Param | Values | Effect |
|---|---|---|
| `?stage` | Any stage value | Pre-filters table to that stage |
| `?specialist` | user_id | Filter by assigned specialist |
| `?institution_type` | `SCHOOL`, `COLLEGE`, `COACHING`, `GROUP` | Filter by institution type |
| `?status` | `ACTIVE`, `STALLED`, `COMPLETED` | Filter by operational status — **derived state** (not a DB column): `ACTIVE` = `stalled_since IS NULL AND stage NOT IN ('COMPLETED')`; `STALLED` = `stalled_since IS NOT NULL`; `COMPLETED` = `stage='COMPLETED'` |
| `?institution_id` | integer | Jump directly to specific institution's onboarding |
| `?view` | `table`, `kanban` | Toggle display mode; default `table` |

---

## HTMX Part-Load Routes

| Part | Route | Trigger |
|---|---|---|
| Stage pipeline strip | `?part=pipeline_strip` | Page load; 5-min auto-refresh |
| Table / kanban rows | `?part=list&view={table|kanban}` | Page load, filter change, pagination |
| Checklist drawer | `?part=checklist&instance_id={id}` | Open checklist action |
| Training sessions panel | `?part=sessions&instance_id={id}` | Open training panel |

---

## Page Layout

```
┌──────────────────────────────────────────────────────────────────┐
│  Onboarding Tracker   [Table | Kanban]   [+ New Onboarding]      │
├──────────────────────────────────────────────────────────────────┤
│  PIPELINE STRIP (stage counts + stalled indicator)               │
├──────────────────────────────────────────────────────────────────┤
│  FILTER ROW                                                      │
├──────────────────────────────────────────────────────────────────┤
│  TABLE VIEW  (or KANBAN VIEW if toggled)                         │
├──────────────────────────────────────────────────────────────────┤
│  PAGINATION (table view only)                                    │
└──────────────────────────────────────────────────────────────────┘
```

---

## Components

### Pipeline Strip

Horizontal stage-count bar showing institution counts per stage.

```
INITIATED    SETUP CALL   PORTAL CFG   ADMIN TRAINED   FIRST EXAM   LIVE   COMPLETED
    3  →          5  →        8    →        4     →        2   →    12 →    2,016
                                                          ⚠ 2 STALLED
```

Each stage count is a clickable filter: clicking filters the table to that stage.

STALLED count (red text with ⚠): clicking filters to `?status=stalled`.

---

### Filter Row

| Filter | Type |
|---|---|
| Stage | Multi-checkbox dropdown |
| Institution type | Radio |
| Assigned specialist | Dropdown (list of Onboarding Specialists) |
| Status | Radio: All / Active / Stalled / Completed |
| Target go-live | Date range picker (show overdue in red) |
| Search | Text search on institution name |

[Apply] [Clear All] — active filters as dismissible pills.

---

### Table View

Columns: Institution | Type | Stage | Specialist | Checklist Progress | Target Go-Live | Days in Stage | Status | Actions

**Stage badge** colour: grey (INITIATED), blue (SETUP_CALL/PORTAL_CONFIGURED), yellow (ADMIN_TRAINED/FIRST_EXAM), green (LIVE), dark green (COMPLETED), red (STALLED).

**Checklist Progress**: `{completed_mandatory}/{total_mandatory}` with mini progress bar.
- All mandatory complete: green bar
- Incomplete: amber bar
- No progress started: grey bar

**Target Go-Live**: Date; coloured:
- Future >14 days: grey
- Future 1–14 days: amber ("due soon")
- Future 0 days: red ("due today")
- Past and not LIVE/COMPLETED: red bold + "OVERDUE"

**Days in Stage**: How many days since last stage transition. Amber if 5–7 days (approaching stall threshold); red if >7 days (Celery should have already flagged as STALLED — if showing red but not STALLED, check that Celery Task 4 ran). The 7-day threshold matches the Celery stall detection threshold exactly.

**Status badge**: ACTIVE (green), STALLED (red, **not** pulsing — pulsing reserved for SLA breaches in I-02; stalled uses steady red badge + ⚠ icon), COMPLETED (grey).

Row click: opens the institution's onboarding drawer (see below).

**Row actions** (Onboarding Specialist; Support Manager):
- [Checklist] — opens checklist drawer
- [Schedule Session] — opens training session modal
- [View Institution →] — links to I-04

**Support Manager additional row actions:**
- [Override Stage ▼] — dropdown: shows all stages with a required reason text field. Allows moving forward multiple stages at once (skipping) or moving backward.
  - **Moving forward by skip**: marks all mandatory checklist items in skipped stages as completed by Support Manager with note "Auto-completed via stage skip"; `last_activity_at` updated.
  - **Moving backward**: inserts SYSTEM note "Stage moved back from {from} to {to} by {manager} — Reason: {text}"; **resets all checklist items for the destination stage and every stage between destination and current stage back to incomplete** — sets `onboarding_checklist_progress.is_completed = false`, `completed_at = NULL`, `completed_by_id = NULL` (notes preserved so specialist retains prior context); `last_activity_at` updated; `stalled_since` cleared. The intent is that the specialist must genuinely redo those steps. Items in stages *before* the destination stage (already fully completed earlier) are not touched. Moving backward does not auto-clear `is_re_onboarding` or `re_onboarding_sequence`.

**Onboarding Specialist backward movement request**: Specialist cannot drag backward in kanban, but can click [Request Stage Rewind] in the onboarding drawer. This creates an `INTERNAL_NOTE` message on the institution's onboarding record (not a ticket) and sends an F-06 push to Support Manager: "Onboarding Specialist {name} requested stage rewind for {institution} — from {current} to {target}." Support Manager reviews and uses [Override Stage] to action it. This prevents unauthorized stage regression while still enabling self-service recovery requests.

---

### Kanban View

Six swimlane columns (COMPLETED collapsed):

```
INITIATED | SETUP CALL | PORTAL CFG | ADMIN TRAINED | FIRST EXAM | LIVE
──────────┼────────────┼────────────┼───────────────┼────────────┼──────
 [Card]   |  [Card]    |  [Card]    |   [Card]      |  [Card]    |[Card]
          |            |            |               |            |
```

Each card:
```
┌─────────────────────────────┐
│  Sunrise Public School      │
│  School · Hyderabad          │
│  Specialist: Arun Nair      │
│  Go-live: 20 Nov (15 days)  │
│  Checklist: 3/4 ██████░     │
│  [Checklist] [Session]      │
└─────────────────────────────┘
```

STALLED cards: red left border (4px) + steady red "⚠ Stalled 12d" label (matches table view — no pulsing).
OVERDUE cards (past go-live, not LIVE): amber left border + "Overdue" label.

**Kanban card [Checklist] and [Session] buttons**: clicking either button opens the same right-side Onboarding Drawer as a table row click, but with the respective tab pre-selected. [Checklist] opens the Checklist tab; [Session] opens the Training Sessions tab. The drawer is loaded via `?part=checklist&instance_id={id}` and `?part=sessions&instance_id={id}` respectively.

Drag-and-drop to move cards between stages (Onboarding Specialist; Support Manager). On drag-drop:
- Validates: all mandatory checklist items for current stage must be completed before moving to next stage
- If mandatory items incomplete: drop rejected; toast "Cannot progress to {next_stage}. Complete mandatory checklist items first: {list}"
- If mandatory items complete: confirmation "Move Sunrise Public School to {PORTAL_CONFIGURED}?" → confirm → POST `/support/onboarding/{id}/stage/`; card moves; system note added to institution record

Can only move forward one stage at a time in kanban. Support Manager can skip stages via table view [Override Stage] button.

COMPLETED column collapsed by default with "(2,016 completed)" label; [Expand] to show.

---

### Onboarding Drawer

Opens on row click (table) or card click (kanban). Right-side drawer (600px wide).

**Header:**
```
Sunrise Public School · School · Hyderabad
Stage: ADMIN_TRAINED  →  [Progress to FIRST_EXAM_CREATED ▶]
Specialist: Arun Nair
Target go-live: 20 Nov 2024 (15 days)
```

[Progress to FIRST_EXAM_CREATED ▶] button:
- Enabled only when all mandatory items for current stage are complete
- Disabled with tooltip "Complete mandatory checklist items first" if incomplete
- Click → confirmation modal → POST stage progression → drawer refreshes

**Tabs inside drawer:**

**Checklist tab (default):**
Stage-grouped checklist. Current stage items shown expanded; prior stages collapsed with ✓ all-complete indicator.

```
▼ ADMIN_TRAINED (current)
  ☑ Portal walkthrough completed  [note: "Done via Zoom 10 Nov" · 10 Nov by Arun]
  ☑ Exam creation demo done       [completed 10 Nov]
  ☐ Student management explained  [mandatory]  [Mark Complete] [Add Note]
  ☐ Results workflow explained    [mandatory]  [Mark Complete] [Add Note]

▶ PORTAL_CONFIGURED (completed)  ✓ All 4/4 complete
▶ SETUP_CALL_SCHEDULED (completed) ✓ All 3/3 complete
▶ INITIATED (completed)           ✓ All 3/3 complete
```

[Mark Complete] → POST `/support/onboarding/{id}/checklist/{item_id}/complete/`; checkbox becomes ☑; checklist progress bar in table updates via HTMX.

[Add Note] → inline text field; note saved to `onboarding_checklist_progress.notes`.

**Training Sessions tab:**
```
Upcoming
· 15 Nov 2024, 11:00 AM · "Results Workflow Walkthrough" (60 min)
  Conducted by: Arun Nair · meet.google.com/xyz-abc
  [Mark Completed] [Cancel Session]

Past
· 10 Nov 2024 · "Portal Walkthrough" · COMPLETED · Attendees: 2
· 3 Nov 2024  · "Exam Creation Demo" · COMPLETED · Attendees: 3
```

[+ Schedule New Session] button → opens session modal (see below).

**Notes tab:**
Chronological notes about this onboarding (separate from ticket notes). Add note form at bottom.

---

### Schedule Training Session Modal

```
Schedule Training Session

Institution: Sunrise Public School (pre-filled, locked)
Session type: [▼ PORTAL_WALKTHROUGH / EXAM_CREATION / STUDENT_MGMT / RESULTS_WORKFLOW / REFRESHER]
Title: [____________________________________]
Date & time: [Date picker]  [Time picker]  IST
Duration: [60] minutes
Meeting link: [________________________________]
Conducted by: [▼ Arun Nair (me)]
Attendees (optional):
  Name 1: [__________]  Role: [__________]  Email: [______________]
  [+ Add Attendee]

[Cancel]  [Schedule Session]
```

POST `/support/onboarding/sessions/create/`; creates `onboarding_training_session` record; confirmation email sent to entered attendee emails via AWS SES.

---

### [+ New Onboarding] Button

Support Manager and Onboarding Specialist only.

Opens a New Onboarding modal:
1. Institution search (autocomplete; filters to institutions with **no currently active onboarding instance** — excludes institutions where `onboarding_instance.stage NOT IN ('COMPLETED')` AND `is_re_onboarding=false` for initial onboardings; institutions with a COMPLETED instance ARE shown and get `is_re_onboarding=true` on the new instance)
2. Assign specialist (dropdown)
3. Target go-live date (date picker)
4. Notes (optional)
[Create] → POST `/support/onboarding/create/`; creates `onboarding_instance` with `stage=INITIATED`; auto-creates mandatory checklist progress rows from `onboarding_checklist_template`; specialist gets notification.

---

## Edge Cases

1. **All mandatory items complete but specialist doesn't progress stage**: Checklist shows all items green; [Progress to Next Stage] button enabled; stage progression is always explicit — system never auto-advances stages.
2. **Specialist tries to bypass checklist (mandatory items incomplete)**: Drag-drop and [Progress] button both blocked. Support Manager can use [Override Stage] in table view with a reason field (creates audit note).
3. **Institution already COMPLETED but issues arise post-onboarding**: Support Manager can create a new onboarding instance for the same institution (override unique constraint via admin); appears with badge "(Re-onboarding)".
4. **STALLED institution**: Red banner in drawer "⚠ Stalled 12 days. No checklist activity since 3 Nov." [Mark as Active] button resets `stalled_since` to null; adds system note.
5. **Target go-live in the past and not yet LIVE**: Drawer shows "OVERDUE" banner in red. Celery `flag_stalled_onboarding` handles notification but does not auto-close — specialist must take action.
6. **Training Coordinator (#52) access**: Can view all onboarding records and training sessions in read-only mode. Cannot modify checklist, progress stages, or schedule sessions directly (sessions go through Onboarding Specialist). Can view recordings from past sessions.
7. **Kanban with >50 cards per column**: Column shows first **50** cards + "Load more" button (load next 50 on click). The ">50" threshold aligns with what is shown before truncation. Kanban not suitable for viewing COMPLETED column (2,000+ records) — that column collapses by default with a pagination link to table view filtered by COMPLETED.
8. **Backward stage movement in kanban**: Drag-drop to a prior stage is allowed only for Support Manager (with mandatory reason field); blocked for Onboarding Specialist. Backward move: creates a system note "Stage moved back from {current} to {previous} by {manager} — Reason: {text}"; `last_activity_at` updated; `stalled_since` cleared. Use case: institution portal config broke after ADMIN_TRAINED; specialist needs to redo PORTAL_CONFIGURED items.
9. **Stall detection reliability**: `last_activity_at` is updated by application code (not a trigger) whenever: a checklist item is marked complete, a training session is created or completed, or the stage changes. If `last_activity_at` is accidentally stale (e.g., bug), Support Manager can [Manually Reset Stall] from the drawer (sets `stalled_since=null`, `last_activity_at=now()`); creates audit note.
8. **Specialist reassignment**: [Reassign Specialist] button in drawer (Support Manager only); reassignment notifies both old and new specialist via F-06.

---

## Notifications (via F-06)

- New onboarding instance created → push to assigned Onboarding Specialist
- Stage progression completed → push to Support Manager: "Sunrise School progressed to ADMIN_TRAINED"
- STALLED flagged by Celery → push to assigned specialist + Support Manager
- Target go-live overdue (Celery checks daily) → push to specialist + Support Manager
- Training session scheduled → confirmation email to attendees (via AWS SES, not F-06)
- Training session status = COMPLETED or CANCELLED → F-06 push to Support Manager
