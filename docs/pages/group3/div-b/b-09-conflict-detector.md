# B-09 — Timetable Conflict Detector

> **URL:** `/school/academic/timetable/conflicts/`
> **File:** `b-09-conflict-detector.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Timetable Coordinator (S3) — full · Principal (S6) — view

---

## 1. Purpose

Dedicated conflict analysis and resolution workspace for the timetable. While B-07 (Timetable Builder) runs inline validation, this page provides a comprehensive view of all conflicts in any timetable version (draft or published), with drill-down to the exact conflicting cells and direct links to resolve. Used during initial timetable building and also when mid-year teacher changes create new conflicts in the published timetable. A conflict-free timetable is a prerequisite for Principal approval.

---

## 2. Page Layout

### 2.1 Header
```
Timetable Conflict Detector                       [Run Full Scan]  [Export Report]
Timetable: [V4 Draft ▼]
Last scan: Today 14:32  ·  Hard Conflicts: 2  ·  Soft Warnings: 7  ·  Status: ⚠️ Needs attention
```

---

## 3. Conflict Summary Cards

```
┌─────────────────┬─────────────────┬─────────────────┬─────────────────┐
│ Teacher Double  │ Room Double     │ Under-allocated │ Load Violations │
│ Bookings        │ Bookings        │ Subjects        │ (teacher/norms) │
│      1          │      1          │      3          │      3          │
│   🔴 Hard       │   🔴 Hard       │   🟡 Warning    │   🟡 Warning    │
└─────────────────┴─────────────────┴─────────────────┴─────────────────┘
```

---

## 4. Conflict List — Hard Conflicts

| # | Type | Description | Classes/Teachers Affected | Day/Period | Action |
|---|---|---|---|---|---|
| C-01 | Teacher double-booking | Ms. Lakshmi assigned to XI-A (Physics) AND XII-B (Physics) simultaneously | XI-A, XII-B · Ms. Lakshmi | Thursday P3 | [Resolve] |
| C-02 | Room double-booking | Chemistry Lab assigned to XI-B (Chemistry) AND XII-A (Chemistry) | XI-B, XII-A · Chem Lab | Tuesday P4 | [Resolve] |

**[Resolve]** → opens the conflict in a resolution drawer showing both conflicting cells side by side, allowing the Timetable Coordinator to drag one to a different slot or swap.

---

## 5. Conflict List — Soft Warnings

| # | Type | Description | Severity | Action |
|---|---|---|---|---|
| W-01 | Under-allocated | Hindi for XI-A: 3 periods assigned, requirement 4 | 🟡 Medium | [Fix in Builder] |
| W-02 | Under-allocated | Mathematics for XI-B: 4 periods assigned, requirement 6 | 🟡 Medium | [Fix in Builder] |
| W-03 | Under-allocated | Biology Lab for IX-A: 0 double-periods assigned, requirement 1 | 🟡 Medium | [Fix in Builder] |
| W-04 | Teacher load exceeded | Mr. Arjun: 38 periods/week (norm max: 36) | 🟡 Low | [View Teacher] |
| W-05 | Teacher load exceeded | Ms. Suma: 37 periods/week (norm max: 36) | 🟡 Low | [View Teacher] |
| W-06 | Consecutive same subject | Physics XI-A appears in P5 and P6 on Thursday | 🟢 Info | [Ignore] |
| W-07 | PT not distributed | Both PT periods for VI-A are on Monday and Tuesday (same week start) | 🟢 Info | [Ignore] |

---

## 6. Conflict Resolution Drawer

Click [Resolve] on any hard conflict:

```
Conflict C-01 — Teacher Double-Booking
Ms. Lakshmi Devi assigned simultaneously to two classes:

  CONFLICT SLOT: Thursday · Period 3

  ┌──────────────────────┐     ┌──────────────────────┐
  │  CLASS XI-A          │     │  CLASS XII-B          │
  │  Subject: Physics    │     │  Subject: Physics     │
  │  Teacher: Ms.Lakshmi │ VS  │  Teacher: Ms.Lakshmi  │
  │  Room: 301           │     │  Room: 305            │
  └──────────────────────┘     └──────────────────────┘

Resolution Options:

Option A — Move XI-A Physics to another slot:
  Available free slots for Ms. Lakshmi + Room 301:
  → Thursday P1 (free), Thursday P8 (free), Friday P4 (free)
  [Move XI-A Thursday P3 → Thursday P1]

Option B — Move XII-B Physics to another slot:
  Available free slots for Ms. Lakshmi + Room 305:
  → Thursday P8 (free), Friday P6 (free)
  [Move XII-B Thursday P3 → Thursday P8]

Option C — Assign a different teacher to one slot:
  Teachers who can teach Physics + free Thursday P3:
  → Mr. Bala Kumar (Physics dept, free) ← available
  [Assign Mr. Bala to XII-B Thursday P3]

[Cancel]
```

One-click resolution — choosing any option updates the draft timetable immediately.

---

## 7. Constraint Check Rules (Full List)

Conflicts are checked against these rules:

**Hard (must fix):**
1. Teacher double-booked — same teacher in two classes same period same day
2. Room double-booked — same room assigned to two classes same period
3. Subject over-allocated — more periods assigned than required

**Soft (warning):**
4. Subject under-allocated — fewer periods than required
5. Teacher load > max — teacher assigned more periods/week than configured max
6. Double period not consecutive — lab double period assigned to non-adjacent slots
7. Lab period without lab room — subject requiring a lab room assigned to a regular classroom
8. PT period placed last — physical education as the final period of the day (not recommended)
9. No morning period for a subject — a subject has all its periods in the afternoon only
10. Same teacher same class consecutive days — same subject for same class on all 5 days (no weekend gap)
11. Single teacher all periods — a class has all periods assigned to only 1 teacher (coverage risk)
12. Unconfirmed room — a room used in the timetable doesn't exist in B-29 registry

---

## 8. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/timetable/conflicts/?draft_id={id}` | Full conflict list for a draft |
| 2 | `POST` | `/api/v1/school/{id}/timetable/conflicts/scan/` | Trigger fresh conflict scan |
| 3 | `GET` | `/api/v1/school/{id}/timetable/conflicts/{conflict_id}/resolution-options/` | Resolution options for a conflict |
| 4 | `POST` | `/api/v1/school/{id}/timetable/conflicts/{conflict_id}/resolve/` | Apply a resolution |
| 5 | `GET` | `/api/v1/school/{id}/timetable/conflicts/export/?draft_id={id}` | Export conflict report |

---

## 9. Business Rules

- Full scan runs automatically when any cell is modified in B-07; this page shows the same data but with more drill-down
- Hard conflicts block the [Submit for Approval] action in B-07 — they must all be resolved first
- Soft warnings can be acknowledged (Timetable Coordinator clicks [Ignore] with a reason) to allow approval to proceed
- Conflict history is preserved — if a conflict was introduced by a mid-year teacher change and then resolved, the resolution is logged with timestamp and resolver
- The conflict detector also runs a nightly background check against the published timetable to catch any data inconsistencies (e.g., a teacher deactivated in A-16 still appearing in published timetable)

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division B*
