# B-07 — Timetable Builder

> **URL:** `/school/academic/timetable/build/`
> **File:** `b-07-timetable-builder.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Timetable Coordinator (S3) — full build/edit · Principal (S6) — approve & publish · VP Academic (S5) — review/approve

---

## 1. Purpose

The interactive timetable construction workspace. Starting from a blank schedule, the Timetable Coordinator assigns teacher-subject-class-room combinations to each period slot, ensuring no teacher is double-booked, no room is double-booked, subject period counts match board-prescribed weekly periods, and teacher loads are within norms. The final timetable is submitted to the Principal for approval, then published to B-06 (Master Timetable). Timetable building is the most complex logistical task in school administration — a typical Indian school with 50 sections, 60 teachers, 8 periods/day × 6 days has 24,000+ possible assignments to optimise.

**Prerequisites:** B-28 (Period Configuration) must be set up, B-29 (Room & Lab Allotment) must be populated, and B-30 (Subject Allocation) must be complete before the builder can be used.

---

## 2. Page Layout

### 2.1 Header
```
Timetable Builder                                 [Auto-Generate]  [Save Draft]  [Validate]  [Submit for Approval]
Draft: V4 (in progress)  ·  Started: 20 Mar 2026  ·  Academic Year: 2025–26
Warnings: 3  ·  Conflicts: 0  ·  Completion: 78% (610/784 periods assigned)
```

---

## 3. Builder Interface — 3-Panel Layout

```
┌──────────────────┬──────────────────────────────────────┬──────────────────┐
│ LEFT PANEL       │ CENTRE — Timetable Grid              │ RIGHT PANEL      │
│                  │                                      │                  │
│ Class Selector   │ [Class XI-A ▼]                       │ Unassigned Pool  │
│ ─────────────── │                                      │ ─────────────── │
│ VI-A  ✅ Done    │  Mon  Tue  Wed  Thu  Fri  Sat        │ Physics: 2 left  │
│ VI-B  ✅ Done    │ P1 [Phy][Chem][Asmb][Math][Phy][—]  │ Chemistry: 1 left│
│ VI-C  ✅ Done    │ P2 [Math][Phy][Phy][Chem][Bio][—]   │ Biology: 0 ✅    │
│ VII-A ✅ Done    │ P3 [Bio][Eng][Chem][Bio][Eng][—]    │ English: 0 ✅    │
│ VIII-A✅ Done    │ P4 [Eng][Bio][Math][Eng][Chem][—]   │ Hindi: 1 left    │
│ IX-A  ✅ Done    │ P5[LabP][PT][LabP][CS][PT][—]       │ Comp Sci: 0 ✅   │
│ IX-B  ✅ Done    │ P6[LabP][Math][Eng][LabP][LabB][—]  │ PT: 0 ✅         │
│ X-A   ⚠️ WIP    │ P7[Hindi][Hindi][Bio][Hindi][LabC]  │ Hindi: 1 left    │
│ XI-A  🔄 Active  │ P8 [Free][Free][—][Math][—][—]      │                  │
│ XI-B  ⬜ Pending │                                      │ [+ Add Period    │
│ XII-A ⬜ Pending │                                      │  Requirement]    │
└──────────────────┴──────────────────────────────────────┴──────────────────┘
```

---

## 4. Grid Interactions

### 4.1 Assigning a Period

Click any empty cell in the grid → opens period assignment picker:

```
Assign Period: XI-A · Monday P8

Available Assignments (matching unassigned requirements):
──────────────────────────────────────────────────────────
  Hindi (Mr. Ramesh) — Free this period · Room 301 available ✅
  Mathematics (Mr. Arjun) — Free this period · Room 301 available ✅
  [Manual Entry: choose any teacher + subject + room]
──────────────────────────────────────────────────────────
[Assign Hindi — Mr. Ramesh, Room 301]
[Assign Mathematics — Mr. Arjun, Room 301]
[Leave Free]   [Cancel]
```

System only suggests assignments where:
- Teacher has this subject allocated to this class (from B-30)
- Teacher is free during this period (not assigned to another class)
- Room is available (not occupied, not in maintenance)
- The subject still has remaining periods to allocate (from requirements pool)

### 4.2 Editing an Existing Cell

Click an already-assigned cell → shows:
- Current assignment (teacher, subject, room)
- [Change Teacher] — swap to another free teacher
- [Change Room] — swap to another free room
- [Clear] — remove assignment (adds back to unassigned pool)
- [Swap with...] — pick another period to swap with (whole-period swap)

---

## 5. Subject Period Requirements

Set up from B-30 (Subject Allocation). Shown in the Right Panel as the "pool" to fill:

| Subject | Teacher Assigned | Weekly Periods (Required) | Assigned So Far | Remaining |
|---|---|---|---|---|
| Physics | Ms. Lakshmi Devi | 6 | 6 | ✅ 0 |
| Chemistry | Mr. Ravi Kumar | 6 | 5 | 🔵 1 |
| Biology | Ms. Anjali Singh | 5 | 5 | ✅ 0 |
| Mathematics | Mr. Arjun | 6 | 4 | 🔵 2 |
| English | Ms. Suma | 5 | 5 | ✅ 0 |
| Hindi | Mr. Ramesh | 4 | 3 | 🔵 1 |
| Computer Science | Mr. Dinesh | 2 | 2 | ✅ 0 |
| PT/Games | Mr. Suresh | 2 | 2 | ✅ 0 |
| Physics Lab | Ms. Lakshmi | 2 (double period) | 2 | ✅ 0 |
| Chemistry Lab | Mr. Ravi | 1 (double period) | 1 | ✅ 0 |
| Biology Lab | Ms. Anjali | 1 (double period) | 0 | 🔴 1 |

Period requirements come from CBSE/board norms (loaded from B-09/B-21) and can be customised by Timetable Coordinator.

---

## 6. Auto-Generate Feature

[Auto-Generate] → runs the timetable generation algorithm:

**Algorithm inputs:**
- Period schedule (from B-28): which slots are available on which days
- Room pool (from B-29): capacity and availability
- Subject requirements: periods per week per class per subject
- Teacher assignments (from B-30): which teacher teaches which class+subject
- Teacher constraints: max periods per day, no consecutive lab periods, PT on different days
- Fixed constraints: Assembly on Wednesday P1, lunch break, PT not in last period (fatigue)

**Algorithm type:** Constraint-satisfaction + greedy backtracking (not ML). Deterministic; generates the same output for the same inputs.

**Auto-generate result:**
- Shows completion % and conflict count
- Timetable Coordinator can then manually adjust any cell
- Auto-generate can be re-run at any time; it overwrites the draft (confirmation required)

---

## 7. Validation Panel

[Validate] → runs all conflict checks and shows results:

### Validation Categories

**Hard conflicts (must fix before publish):**
| # | Type | Description |
|---|---|---|
| H1 | Teacher double-booked | Ms. Lakshmi assigned to both XI-A and XII-B at Monday P3 |
| H2 | Room double-booked | Physics Lab assigned to both XI-A and XI-B at Tuesday P5 |
| H3 | Subject over-allocated | Physics for XI-A has 7 periods assigned; requirement is 6 |

**Soft warnings (review but can publish):**
| # | Type | Description |
|---|---|---|
| W1 | Under-allocated | Hindi for XI-A has only 3 periods; requirement is 4 |
| W2 | Teacher load exceeded | Mr. Arjun has 38 periods/week; CBSE norm max is 36 |
| W3 | Same subject consecutive | Physics XI-A appears in P5 and P6 on Thursday — may cause fatigue |
| W4 | PT not spread | Both PT periods are on Monday and Tuesday — should spread across week |
| W5 | No morning Mathematics | VI-B has no Math periods before lunch — cognitive load concern |

---

## 8. Submit for Approval → Principal Review

[Submit for Approval] → sends notification to Principal:

Principal sees a review view with:
- Full timetable preview (all classes)
- Validation report (conflicts/warnings)
- Teacher load summary (periods per teacher)
- [Approve & Publish] or [Return with Notes]

**On Approve & Publish:**
- Current draft becomes the new published version in B-06
- Version number increments
- All teachers notified via in-app + WhatsApp: "New timetable V4 published — effective from [date]"
- Previous version archived

---

## 9. Teacher Constraints (Configuration)

Timetable Coordinator can set per-teacher constraints:

| Teacher | Max Periods/Day | Preferred Free Period | Unavailable Days/Periods | Notes |
|---|---|---|---|---|
| Ms. Lakshmi Devi | 7 | P8 | — | — |
| Mr. Ravi Kumar | 7 | — | Tue P1 (doctor appointment) | Recurring |
| Ms. Anjali Singh | 6 | — | — | Part-time (only Mon–Thu) |
| Mr. Ramesh | 5 | P5/P6 | — | Teaches Hindi only |

---

## 10. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/timetable/drafts/` | All draft timetables |
| 2 | `POST` | `/api/v1/school/{id}/timetable/drafts/` | Create new draft |
| 3 | `GET` | `/api/v1/school/{id}/timetable/drafts/{draft_id}/` | Draft detail |
| 4 | `PATCH` | `/api/v1/school/{id}/timetable/drafts/{draft_id}/cell/` | Update single cell assignment |
| 5 | `POST` | `/api/v1/school/{id}/timetable/drafts/{draft_id}/auto-generate/` | Run auto-generation |
| 6 | `GET` | `/api/v1/school/{id}/timetable/drafts/{draft_id}/validate/` | Validation report |
| 7 | `POST` | `/api/v1/school/{id}/timetable/drafts/{draft_id}/submit/` | Submit for Principal approval |
| 8 | `POST` | `/api/v1/school/{id}/timetable/drafts/{draft_id}/publish/` | Publish (Principal only) |
| 9 | `GET` | `/api/v1/school/{id}/timetable/constraints/` | Teacher constraints list |
| 10 | `PATCH` | `/api/v1/school/{id}/timetable/constraints/{teacher_id}/` | Update teacher constraints |

---

## 11. Business Rules

- Only one active draft at a time; attempting to create a second draft warns "Draft V4 already in progress"
- Auto-generate cannot be undone; it overwrites all manual assignments (confirm dialog required)
- Hard conflicts (teacher double-booking, room double-booking) must all be resolved before Principal can approve; the [Submit for Approval] button is disabled if hard conflicts exist
- Teacher load norm: CBSE recommends 25–30 teaching periods/week for subject teachers; this is a soft warning not a block
- Period requirements are sourced from B-30 (Subject Allocation) as the source of truth; manual overrides in the builder are possible but flagged
- Timetable Coordinator cannot publish directly; only Principal (S6) can press [Approve & Publish]
- Once published, the timetable takes effect from a configurable "effective date" (can be set to a future Monday for planned transitions)

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division B*
