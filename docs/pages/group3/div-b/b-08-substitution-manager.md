# B-08 — Substitution Manager

> **URL:** `/school/academic/timetable/substitutions/`
> **File:** `b-08-substitution-manager.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Timetable Coordinator (S3) — full · Principal (S6) — full · VP Academic (S5) — full

---

## 1. Purpose

Manages teacher substitution when a teacher is absent. Every morning, when the attendance system (A-17) marks a teacher absent, the Timetable Coordinator sees the affected periods and assigns substitute teachers from the pool of staff who are free during those periods. Without substitution management, classes are left unattended — a serious issue in Indian schools both for discipline and for parents who complain about "wasted periods." The substitution register is also checked by CBSE inspection teams as evidence that the school ensures continuous teaching coverage.

**Indian school context:** Substitute assignment follows an unwritten fairness rule — the same teacher shouldn't be repeatedly pulled out of their free periods for substitution. EduForge tracks substitution frequency to help the Timetable Coordinator maintain fairness. The physical substitution register is a statutory record in many state boards.

---

## 2. Page Layout

### 2.1 Header
```
Substitution Manager                              [+ Manual Entry]  [Export Register]
Today: Monday, 24 March 2026
Absent Today: 2 teachers  ·  Affected Periods: 12  ·  Arranged: 10  ✅  ·  Pending: 2  ⚠️
```

---

## 3. Today's Substitution Board

### 3.1 Absent Teachers & Affected Periods

| Teacher | Absent Type | Leave Type | Periods Affected Today | Arranged | Pending |
|---|---|---|---|---|---|
| Ms. Anjali Singh | Full Day | CL | P1 (IX-A Bio), P3 (XI-A Bio), P6 (X-A Bio), P7 (IX-B Bio) | 3 | 1 |
| Mr. Dinesh Kumar | Half Day (PM) | Medical | P6 (XI-A CS), P7 (XI-B CS), P8 (XII-A CS) | 2 | 1 |

### 3.2 Period-wise Substitution Table

| Period | Class | Subject | Original Teacher | Substitute Assigned | Room | Status | Action |
|---|---|---|---|---|---|---|---|
| P1 | IX-A | Biology | Ms. Anjali | Ms. Kavitha (CL Teacher IX-A) | 301 | ✅ Done | [Change] |
| P3 | XI-A | Biology | Ms. Anjali | Dr. Suresh P (Physics — free P3) | 305 | ✅ Done | [Change] |
| P6 | X-A | Biology | Ms. Anjali | Ms. Pooja (Hindi — free P6) | 302 | ✅ Done | [Change] |
| P7 | IX-B | Biology | Ms. Anjali | — | 303 | ⚠️ Pending | [Arrange] |
| P6 | XI-A | Comp Sci | Mr. Dinesh | Mr. Rajan (Maths — free P6) | 309 | ✅ Done | [Change] |
| P7 | XI-B | Comp Sci | Mr. Dinesh | — | 310 | ⚠️ Pending | [Arrange] |
| P8 | XII-A | Comp Sci | Mr. Dinesh | Ms. Suma (English — free P8) | 308 | ✅ Done | [Change] |

---

## 4. Substitute Assignment Drawer (`substitute-assign`, 480px)

Triggered by [Arrange] or [Change] on any pending period:

```
Arrange Substitute
Original: Ms. Anjali Singh · Biology · Class IX-B · Period 7 · Room 303

Free Teachers During P7 (Monday):
──────────────────────────────────────────────────────────
  Teacher               Dept        Sub Count  Last Subst
  Mr. Ramesh (Hindi)    Languages   4          22 Mar
  Ms. Leela (Chem)      Science     2          20 Mar ← recommended (fewer substitutions)
  Mr. Bala (Physics)    Science     6          24 Mar (today - already substituted once)
  Ms. Priya (Maths)     Maths       1          15 Mar ← recommended
──────────────────────────────────────────────────────────
  [Assign Ms. Leela]  [Assign Ms. Priya]  [Assign manually]  [Mark Free Period]
```

**Recommendation logic:** Prefer teacher with fewest recent substitutions (fairness); prefer same department (Biology substitute from Science dept is better than from Languages); avoid teachers who already substituted today.

**[Mark Free Period]** — option when no suitable substitute is available; class is marked as supervised free period (students remain in class, senior student or nearby teacher monitors).

---

## 5. Substitution Register (History)

Full register of all substitutions:

| Date | Absent Teacher | Class | Subject | Period | Substitute | Reason | Confirmed |
|---|---|---|---|---|---|---|---|
| 24 Mar | Ms. Anjali Singh | IX-A | Biology | P1 | Ms. Kavitha | CL | ✅ |
| 24 Mar | Ms. Anjali Singh | XI-A | Biology | P3 | Dr. Suresh P | CL | ✅ |
| 22 Mar | Mr. Ravi Kumar | XII-A | Chemistry | P2 | Ms. Leela | Medical | ✅ |
| 20 Mar | Mr. Arjun | IX-B | Maths | P4 | Ms. Priya | Personal | ✅ |

Filter by: Date range · Absent teacher · Substitute teacher · Subject · Class

**Export Register** → generates PDF/Excel in the format of the physical substitution register (used for CBSE inspections: columns for Date, Period, Class, Subject, Absent Teacher, Substitute, HOD Signature).

---

## 6. Teacher Substitution Load Analysis

| Teacher | Total Sub Count (This Month) | Total Sub Count (This Year) | Last Substitution |
|---|---|---|---|
| Mr. Ramesh (Hindi) | 4 | 18 | Today |
| Ms. Pooja (Hindi) | 3 | 14 | Today |
| Dr. Suresh P (Physics) | 2 | 9 | Today |
| Ms. Kavitha (Class Teacher VI-A) | 2 | 11 | Today |
| Ms. Leela (Chemistry) | 2 | 7 | 22 Mar |
| Ms. Priya (Mathematics) | 1 | 4 | 20 Mar |

Sorted by total count desc. Teachers with high substitution load flagged in amber (> 20 in a term).

---

## 7. Advance Substitution (Planned Leave)

When a teacher applies for leave in advance (B-18 Leave Management), the Timetable Coordinator is notified and can pre-arrange substitutions:

**Upcoming Leave Requiring Substitution:**

| Teacher | Leave Dates | Periods Affected/Day | Status |
|---|---|---|---|
| Mr. Ravi Kumar | 1–5 Apr (5 days) | 7 periods/day (35 total) | ⬜ Not yet arranged |
| Ms. Anjali Singh | 10 Apr (1 day) | 4 periods | ⬜ Not yet arranged |

[Pre-arrange] → opens the substitution planning view for those dates.

---

## 8. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/substitutions/today/` | Today's absent teachers + affected periods |
| 2 | `GET` | `/api/v1/school/{id}/substitutions/available/?date={date}&period={p}&class_id={c}` | Free teachers for a period |
| 3 | `POST` | `/api/v1/school/{id}/substitutions/` | Assign substitute |
| 4 | `PATCH` | `/api/v1/school/{id}/substitutions/{sub_id}/` | Change/update substitute |
| 5 | `GET` | `/api/v1/school/{id}/substitutions/register/?from={date}&to={date}` | Substitution register |
| 6 | `GET` | `/api/v1/school/{id}/substitutions/load-report/?month={month}` | Teacher load analysis |
| 7 | `GET` | `/api/v1/school/{id}/substitutions/upcoming/` | Advance substitution planning queue |
| 8 | `GET` | `/api/v1/school/{id}/substitutions/export/?from={date}&to={date}` | Export register PDF |

---

## 9. Business Rules

- Substitution data is sourced from A-17 (Staff Attendance Overview) — when a teacher is marked absent, their periods auto-appear in the substitution board for today
- A period can be marked as "Free Period" (supervised but no teaching) as a last resort; this logs a reason and is visible in the HOD's dashboard
- Substitute teachers are not required to teach the subject being substituted; they are monitors/supervisors; however, same-subject substitutes are preferred (recommendation logic)
- Substitution register entries are locked after 48 hours — corrections require VP Admin approval (audit trail)
- The "substitution count" per teacher resets at the start of each academic term
- HOD of the absent teacher's department is auto-notified when a substitution is arranged for a teacher in their department

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division B*
