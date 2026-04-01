# B-06 — Master Timetable

> **URL:** `/school/academic/timetable/`
> **File:** `b-06-master-timetable.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Timetable Coordinator (S3) — full · All teaching staff — read own schedule · HOD (S4) — read dept view · Principal (S6) — full · VP Academic (S5) — full

---

## 1. Purpose

The published master timetable — the definitive schedule showing which teacher teaches which subject to which class in which period on which day. This is the central operational document every teacher and student works from daily. The master timetable is generated via B-07 (Timetable Builder) and published here. Once published, it is read-only except for substitution entries (B-08) or when a new version is built. In an Indian school, the timetable is physically displayed in every classroom and teacher's common room — EduForge makes the digital timetable available on all devices and generates printable formats.

---

## 2. Page Layout

### 2.1 Header
```
Master Timetable                                  [Download PDF]  [Print]  [Edit (Build New)]
Academic Year: 2025–26  ·  Version: V3 (effective 10 Feb 2026)
Status: 🟢 Published  ·  Last modified: 10 Feb 2026  ·  Approved by: Principal Rajan T
View: [Class ▼]  [Teacher ▼]  [Room ▼]  Week: [Current ▼]
```

**Version banner:** If a newer draft exists in B-07 (not yet published), a banner shows: "⚠️ Draft V4 in progress in Timetable Builder. Current V3 remains active until published."

---

## 3. View Modes

### View Mode 1 — Class Timetable (default for teachers/students)

Dropdown selects class (e.g., "Class XI-A"):

```
Class XI-A — Timetable (Week of 24 Mar 2026)
───────────────────────────────────────────────────────────────────────────────
         Monday          Tuesday         Wednesday       Thursday        Friday
P1  Physics            Chemistry        Assembly        Mathematics     Physics
    Ms. Lakshmi        Mr. Ravi         —               Mr. Arjun       Ms. Lakshmi
    Room 301           Room 302                         Room 301        Room 301

P2  Mathematics        Physics          Physics         Chemistry       Biology
    Mr. Arjun          Ms. Lakshmi      Ms. Lakshmi     Mr. Ravi        Ms. Anjali
    Room 301           Room 301         Room 301        Room 302        Room 301

─── SHORT BREAK 10:15–10:30 ─────────────────────────────────────────────────

P3  Biology            English          Chemistry       Biology         English
    Ms. Anjali         Ms. Suma         Mr. Ravi        Ms. Anjali      Ms. Suma
    Room 301           Room 204         Room 302        Room 301        Room 204

P4  English            Biology          Mathematics     English         Chemistry
    Ms. Suma           Ms. Anjali       Mr. Arjun       Ms. Suma        Mr. Ravi
    Room 204           Room 301         Room 301        Room 204        Room 302

─── LUNCH 12:00–12:40 ────────────────────────────────────────────────────────

P5  Computer Science   PT/Games         Physics Lab     Computer Sci    PT/Games
    Mr. Dinesh         Mr. Suresh(PT)   Ms. Lakshmi     Mr. Dinesh      Mr. Suresh(PT)
    Comp Lab 1         Ground           Physics Lab     Comp Lab 1      Ground

P6  Physics Lab        Maths            English         Physics Lab     Biology Lab
    Ms. Lakshmi        Mr. Arjun        Ms. Suma        Ms. Lakshmi     Ms. Anjali
    Physics Lab        Room 301         Room 204        Physics Lab     Bio Lab

P7  Hindi              Hindi            Biology         Hindi           Chemistry Lab
    Mr. Ramesh         Mr. Ramesh       Ms. Anjali      Mr. Ramesh      Mr. Ravi
    Room 301           Room 301         Room 301        Room 301        Chem Lab

P8  Free Period        Free Period      —               Maths           —
    —                  —               —               Mr. Arjun       —
    —                  —               —               Room 301        —
───────────────────────────────────────────────────────────────────────────────
```

Colour coding by subject group:
- Sciences: Blue (Physics), Green (Chemistry), Teal (Biology)
- Mathematics: Orange
- Languages: Purple (English), Maroon (Hindi)
- PT/Games: Yellow
- Computer Science: Cyan
- Labs: Darker shade of subject colour

Today's current period highlighted with a pulsing border (real-time clock comparison).

---

### View Mode 2 — Teacher Timetable

Dropdown selects teacher → shows all their assigned periods across all classes:

```
Ms. Lakshmi Devi — Physics Teacher — Weekly Schedule
─────────────────────────────────────────────────────────────────────────────
         Monday     Tuesday    Wednesday  Thursday   Friday
P1  XI-A Physics   XII-A Phys  XI-A Phys XII-A Phys XI-A Phys
P2  Free           XI-B Phys   XII-B Phys Free       XII-B Phys
P3  XII-A Lab      Free        Free       XII-B Lab  Free
P4  Free           XII-B Phys  XI-B Phys  Free       XII-A Phys
P5  XI-A Phys Lab  Free        XII-A Lab  XI-B Phys  Free
P6  XII-A Phys Lab XII-B Lab   Free       XII-A Lab  XI-A Phys
P7  Free           Free        Free       Free       Free
P8  Free           Free        —          Free       —
─────────────────────────────────────────────────────────────────────────────
Weekly Load: 32 periods / 40 available  ·  Free periods: 8
Classes assigned: XI-A, XI-B, XII-A, XII-B
```

**Free period report:** Shows when each teacher is free — used by Timetable Coordinator for substitution assignments, by HOD for scheduling remedial classes, by VP for scheduling parent meetings.

---

### View Mode 3 — Room Timetable

Dropdown selects room → shows occupancy across the week. Same grid as B-29 (Room & Lab Allotment) but shown here in published timetable context.

---

### View Mode 4 — Department View (for HOD)

Shows all periods across all teachers and classes in the HOD's department. Useful for HOD to see the complete picture of their department's teaching load.

---

## 4. Today's Timetable Summary (Quick Strip)

Shown at the top for Timetable Coordinator's daily dashboard:

```
Today: Monday 24 March 2026  ·  Schedule: Standard (8 periods)
Total periods scheduled: 312  ·  Substitutions active: 3  ·  Cancelled: 0
Absent teachers today: 2 (Ms. Anjali, Mr. Dinesh) — substitutes assigned ✅
```

---

## 5. Version History

| Version | Effective From | Built By | Approved By | Changes |
|---|---|---|---|---|
| V3 (current) | 10 Feb 2026 | Mr. Bala (TT Coord) | Principal Rajan | Term 2 changes — 3 teacher reassignments |
| V2 | 1 Jan 2026 | Mr. Bala | Principal Rajan | Post-exam revision — added Maths extra period for XII |
| V1 | 2 Jun 2025 | Mr. Bala | Principal Rajan | Academic year start |

[View V2] → shows V2 timetable in read-only historical view.

---

## 6. Download & Print Formats

[Download PDF] → options:
- **All Classes (Booklet):** One page per class, printable in A4 — goes to class rooms
- **Teacher Schedule:** One page per teacher — given to each teacher at start of year
- **Coordinator Summary:** All teachers on one condensed sheet — Timetable Coordinator's reference
- **Room Schedule:** One page per room — posted on room doors

All PDFs include the school header/logo, effective date, and version number.

---

## 7. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/timetable/published/` | Current published timetable (full) |
| 2 | `GET` | `/api/v1/school/{id}/timetable/published/class/{class_id}/` | Class timetable |
| 3 | `GET` | `/api/v1/school/{id}/timetable/published/teacher/{teacher_id}/` | Teacher timetable |
| 4 | `GET` | `/api/v1/school/{id}/timetable/published/room/{room_id}/` | Room timetable |
| 5 | `GET` | `/api/v1/school/{id}/timetable/published/today/` | Today's timetable summary |
| 6 | `GET` | `/api/v1/school/{id}/timetable/versions/` | Version history |
| 7 | `GET` | `/api/v1/school/{id}/timetable/versions/{version_id}/` | Historical version detail |
| 8 | `GET` | `/api/v1/school/{id}/timetable/published/export/?format={pdf|excel}` | Download/export |
| 9 | `GET` | `/api/v1/school/{id}/timetable/published/teacher/{teacher_id}/free-periods/` | Teacher free period list |

---

## 8. Business Rules

- Only one timetable version can be "Published" at a time; publishing V4 automatically archives V3 to "Historical"
- The published timetable cannot be directly edited; all changes go through B-07 (Timetable Builder) to create a new version
- Substitution assignments (B-08) overlay the published timetable on specific dates without creating a new version
- Teachers can only see their own timetable by default; they can see the full class timetable for classes they are assigned to
- The "current period" highlight refreshes every minute via HTMX polling
- When a class has no teacher assigned for a period (free/gap period) it shows as "Free" — this is normal for some class combinations in senior secondary

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division B*
