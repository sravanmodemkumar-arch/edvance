# L-12 — Timetable & Teaching Workload

> **URL:** `/school/hr/timetable/`
> **File:** `l-12-timetable-workload.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Academic Coordinator (S4) — build and maintain timetable · Vice Principal (S5) — approve timetable, resolve conflicts · HR Officer (S4) — workload compliance and payroll integration · Principal (S6) — override authority · Staff (S3–S5) — view own timetable

---

## 1. Purpose

The timetable is the operational heartbeat of the school — every period allocation is a contractual teaching commitment for a staff member and a curriculum delivery commitment to students. This module manages:
- Annual master timetable construction (classes × periods × subjects × teachers)
- Teacher workload validation against CBSE norms and individual contracts
- Period-level teacher assignment (class, subject, room)
- Free-period and remedial allocation
- Workload integration with payroll (for guest lecturers paid per period)
- Substitute management integration (L-13) when a teacher is absent

CBSE requirement: Every school must demonstrate that teaching is distributed as per affiliation norms — the timetable is inspected during CBSE visits.

---

## 2. School Timetable — Master View

```
MASTER TIMETABLE — GREENFIELDS SCHOOL, 2026–27
Academic Year: June 2026 – March 2027
Last revised: 1 June 2026
Approved by: Ms. Meena Rao (Principal)

SCHOOL TIMING:
  7:45 AM  – 8:00 AM   Assembly (all classes)
  8:00 AM  – 8:45 AM   Period 1
  8:45 AM  – 9:30 AM   Period 2
  9:30 AM  – 10:15 AM  Period 3
  10:15 AM – 10:30 AM  Break
  10:30 AM – 11:15 AM  Period 4
  11:15 AM – 12:00 PM  Period 5
  12:00 PM – 12:45 PM  Period 6
  12:45 PM – 1:30 PM   Lunch
  1:30 PM  – 2:15 PM   Period 7
  2:15 PM  – 3:00 PM   Period 8
  3:00 PM  – 3:30 PM   Activity / Remedial / Games (alternate days)

DAYS: Monday–Friday (5 full days) + alternate Saturdays (4 periods, 8:00–12:00)
TOTAL PERIODS/WEEK: 8×5 + 4×0.5 = 42 periods/week (36 teaching + 6 activity/games)
```

---

## 3. Teacher Timetable — Individual View

```
TEACHER TIMETABLE — Ms. Geeta Sharma (TCH-031)
Subject: Social Science  |  Classes: IX, X (4 sections each)
Role: Subject Teacher (SS) + Class Teacher (IX-A)
Academic Year: 2026–27

            Monday      Tuesday     Wednesday   Thursday    Friday      Sat(alt)
Period 1    IX-A SS     X-A SS      IX-B SS     X-B SS      IX-C SS     IX-D SS
Period 2    IX-B SS     IX-C SS     X-A SS      IX-A SS     X-C SS      X-D SS
Period 3    X-B SS      X-C SS      IX-D SS     X-D SS      IX-A SS     —
Period 4    IX-D SS     IX-A CT*    X-B SS      IX-C SS     X-A SS      —
Period 5    X-A SS      X-B SS      IX-A CT*    X-C SS      IX-B SS     —
Period 6    X-C SS      IX-D SS     IX-C SS     IX-B SS     X-D SS      —
Period 7    FREE        X-D SS      FREE        FREE        FREE        —
Period 8    IX-C SS     FREE        X-D SS**    X-A SS      FREE        —

* CT = Class Teacher period (administrative: attendance review, student interaction,
  pastoral care — not subject teaching)
** Double period for project work (SS alternate weeks)

PERIOD SUMMARY:
  Teaching periods/week (SS):   22
  Class Teacher admin periods:   2
  Free periods (planning/correction): 6 (Mon P7, Wed P7, Thu P7, Thu P8 = wait, recounting)
  Total periods allocated:       30 (incl. 2 CT + 2 free)

CBSE NORM:
  Maximum teaching periods: 24–26/week for a full-time teacher (CBSE Affiliation Bye-Laws)
  Ms. Geeta: 22 teaching periods ✅ (within norm)
  Free periods: Minimum 4 free periods/week recommended (for correction, lesson prep)
  Free periods available: 6 ✅

WORKLOAD COMPLIANCE:
  Total Social Science periods school needs/week (9 sections × SS × 6 periods/week): 54
  Allocated to Ms. Geeta: 22
  Remaining allocated to Mr. Arjun (TCH-032): 20 + 12 (Class X extra) = 32 ✅
  Coverage: 54/54 ✅
```

---

## 4. Timetable Construction — Constraints

```
Timetable Constraints — Greenfields 2026–27

Hard constraints (cannot be violated):
  ✅ No teacher in two rooms simultaneously (clash detection)
  ✅ No classroom with two different classes simultaneously
  ✅ All subjects get minimum periods/week as per CBSE syllabus:
       English: 6/week  |  Mathematics: 6/week  |  Science: 6/week
       Social Science: 6/week  |  Second Language (Hindi/Telugu): 4/week
       Art/Craft: 2/week  |  Physical Education: 2/week  |  Computer: 2/week
  ✅ No teacher exceeds 26 teaching periods/week
  ✅ No class has more than 4 consecutive teaching periods without a break
  ✅ Double periods (labs, projects) only in slots 3+4, 5+6, or 7+8 (not across break/lunch)
  ✅ PT/Games period only in morning (Periods 1–3) — temperature compliance
  ✅ Science lab periods: Periods 1–5 only (lab cleaning time required before close)

Soft constraints (system flags; coordinator may override with reason):
  ⚠ Same subject not in consecutive periods for a class (engagement variety)
  ⚠ A teacher should not have teaching in all 8 periods on any single day
  ⚠ Science/Maths teachers preferred in morning slots (cognitive load)
  ⚠ All free periods should not cluster on a single day
  ⚠ Class Teacher period ideally in Period 1 (morning — to handle attendance/pastoral before day starts)

Clash detection result (2026–27):
  Room clashes: 0 ✅
  Teacher clashes: 0 ✅
  Period coverage gaps: 0 ✅
  Soft constraint violations: 3 (flagged below for review)
    1. Mr. Ravi K. (Physics) has 6 consecutive periods on Wednesday — ⚠ flagged
    2. Class XII-B has Maths in Period 8 (3 times/week) — late slot ⚠
    3. Ms. Anita Rao (History) has all free periods on Saturday — imbalanced ⚠
```

---

## 5. Workload Register

```
TEACHING WORKLOAD REGISTER — 2026–27
(As required for CBSE Inspection — Affiliation Bye-Laws Schedule V)

Teacher           Designation   Subject        Periods/wk  Max(CBSE)  Status
Ms. Geeta Sharma  Sr. Teacher   Social Sci     22          26         ✅
Mr. Arjun R.      Teacher       Social Sci     24          26         ✅
Ms. Anita Rao     Teacher       History        22          26         ✅ (new joiner)
Mr. Ravi Kumar    Sr. Teacher   Physics        26          26         ⚠ AT LIMIT
Ms. Sunita P.     Teacher       Chemistry      24          26         ✅
Mr. Suresh T.     Teacher       Physics        22          26         ✅
Ms. Kavitha N.    HOD-Maths     Mathematics    18          26         ✅ (HOD reduction: -4)
Ms. Priya M.      Sr. Teacher   Mathematics    26          26         ⚠ AT LIMIT
Mr. Deepak C.     Teacher       Mathematics    25          26         ✅
Ms. Rekha B.      Teacher       English        24          26         ✅
Ms. Jyothi P.     HOD-English   English        16          26         ✅ (HOD reduction: -8)
...
[87 teaching staff total]

CBSE PTR Compliance:
  Total students: 1,240
  Total full-time teaching staff: 52
  PTR: 1,240 ÷ 52 = 23.8 : 1
  CBSE requirement: ≤30:1  ✅
  State (TS) RTE requirement: ≤30:1 (Class VI–VIII: ≤35:1)  ✅

HOD Workload Allowance:
  HOD with 1–3 sections of their department: teaching load reduced by 4 periods/week
  HOD with 4+ sections: teaching load reduced by 6–8 periods/week
  (Standard school practice; reflects administrative responsibilities)
```

---

## 6. Room Allocation

```
ROOM ALLOCATION — MASTER

Room        Type          Capacity   Assigned Classes
Room 1      Classroom     40         VI-A (Class Teacher: Mr. ...)
Room 2      Classroom     40         VI-B
...
Room 16     Classroom     40         XII-B
Physics Lab  Lab           30         —  (period-wise booking: see below)
Chemistry Lab Lab          30         —
Biology Lab  Lab           30         —
Computer Lab Computer     36         —
Library      Library      25         —  (structured reading: Tuesday P4 Classes VI–VIII)
Art Room     Art          30         —
Music Room   Music        25         —
Seminar Hall Multi-use    80         —

PHYSICS LAB — Period-Wise Booking:
  Monday P3+P4: XII-A (Physics practicals — Ms. Sunita)
  Monday P5+P6: XII-B (Physics practicals — Mr. Suresh T.)
  Tuesday P1+P2: XI-A (Physics practicals)
  Tuesday P3+P4: XI-B (Physics practicals)
  [etc. — double periods for lab sessions]

Room Conflict: None ✅
Unbooked periods (Physics Lab): 12/week → available for remedial/extra practicals
```

---

## 7. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/hr/timetable/master/` | Full master timetable |
| 2 | `GET` | `/api/v1/school/{id}/hr/timetable/teacher/{staff_id}/` | Individual teacher timetable |
| 3 | `GET` | `/api/v1/school/{id}/hr/timetable/class/{class_id}/` | Class timetable |
| 4 | `POST` | `/api/v1/school/{id}/hr/timetable/` | Create/update master timetable |
| 5 | `GET` | `/api/v1/school/{id}/hr/timetable/workload/` | Workload register (all teachers) |
| 6 | `GET` | `/api/v1/school/{id}/hr/timetable/conflicts/` | Clash detection report |
| 7 | `GET` | `/api/v1/school/{id}/hr/timetable/rooms/` | Room allocation schedule |
| 8 | `GET` | `/api/v1/school/{id}/hr/timetable/cbse-ptr/` | PTR compliance report |
| 9 | `POST` | `/api/v1/school/{id}/hr/timetable/period-swap/` | Swap two periods (with audit) |

---

## 8. Business Rules

- CBSE Affiliation Bye-Laws Schedule V requires the school to maintain a teachers' workload register; inspectors verify that no teacher exceeds the maximum period limit (typically 26 teaching periods/week); schools where teachers are overloaded face adverse compliance reports
- PTR (Pupil-Teacher Ratio) must be ≤30:1; for RTE-covered schools this is mandatory; PTR is calculated using only full-time qualified teachers (part-time, substitute, and visiting staff are not counted); a school approaching 30:1 must initiate recruitment before it crosses the threshold
- HODs are given a teaching load reduction (4–8 periods/week) to account for departmental administration; this is a long-standing school HR practice though not a statutory requirement; the EduForge timetable module enforces this reduction when the HOD role is assigned
- Double periods (for labs, projects, activities) must not straddle lunch or the main break; they must be contiguous within a session; this is standard pedagogy — a 45-minute gap in the middle of an experiment is pedagogically counterproductive
- The timetable is approved by the Principal at the start of the year and changes during the year require VP authorisation with an audit log entry; this is required for CBSE inspection (inspectors ask whether the timetable was changed mid-year and why)
- Room allocation is locked per semester; a room reassignment requires Academic Coordinator approval; rooms are not arbitrarily changed to avoid confusion for students (especially hostel boarders who memorise their day's schedule)
- Timetable data integrates directly with L-13 (Substitute Management) — when a teacher is absent, the system uses this table to identify which periods need coverage and which teacher is free at that time; this makes substitute assignment automatic and prevents gaps in class coverage

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division L*
