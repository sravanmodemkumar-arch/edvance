# B-28 — Period & Bell Schedule Configuration

> **URL:** `/school/academic/timetable/periods/`
> **File:** `b-28-period-configuration.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Timetable Coordinator (S3) — full · Principal (S6) — approve · VP Academic (S5) — read

---

## 1. Purpose

Defines the school's daily period structure — what time each period begins and ends, how long breaks are, which periods are fixed (assembly, lunch, PT) and which are teaching periods, and whether different class groups have different bell schedules. This is the foundational data that the Timetable Builder (B-07) depends on: it cannot generate or validate a timetable without knowing the period slots. Must be configured once at the start of the academic year and reconfirmed each year.

**Indian school context:** A typical CBSE school runs 8–9 periods per day for Classes VI–XII, with shorter period counts for primary classes. Many schools have a special period structure on Wednesday (Assembly + Moral Science period replacing a subject period) and shortened days on Saturdays. Some schools run double periods for Labs. The bell schedule is broadcast via the school's PA/bell system — EduForge exports it in a format compatible with automated bell systems.

---

## 2. Page Layout

### 2.1 Header
```
Period & Bell Schedule Configuration              [+ New Schedule]  [Export Bell Schedule]
Active Schedule: Standard (Mon–Fri)  ·  Academic Year: 2025–26
Schedules defined: 3  ·  Last modified: 12 Apr 2025
```

---

## 3. Schedule Overview

A school can have multiple named bell schedules that apply on different days or to different class groups:

| Schedule Name | Applies To | Days | Total Periods | Status | Actions |
|---|---|---|---|---|---|
| Standard | Classes VI–XII | Mon, Tue, Thu, Fri | 8 teaching periods | ✅ Active | [Edit] [Duplicate] |
| Wednesday Assembly | Classes VI–XII | Wednesday only | 7 teaching periods + 1 Assembly | ✅ Active | [Edit] |
| Saturday Half-Day | Classes I–X | Saturday | 5 teaching periods | ✅ Active | [Edit] |
| Primary Standard | Classes I–V | Mon–Fri | 6 teaching periods (shorter) | ✅ Active | [Edit] |

---

## 4. Period Schedule Detail — Standard (Mon–Fri)

Click any schedule row → expands or opens edit view:

### 4.1 Period Slots Table

| Slot # | Label | Type | Start Time | End Time | Duration | Notes |
|---|---|---|---|---|---|---|
| 1 | P1 | Teaching | 08:00 | 08:45 | 45 min | — |
| 2 | P2 | Teaching | 08:45 | 09:30 | 45 min | — |
| 3 | P3 | Teaching | 09:30 | 10:15 | 45 min | — |
| — | Break 1 | Break | 10:15 | 10:30 | 15 min | Short break / snack |
| 4 | P4 | Teaching | 10:30 | 11:15 | 45 min | — |
| 5 | P5 | Teaching | 11:15 | 12:00 | 45 min | — |
| — | Lunch | Break | 12:00 | 12:40 | 40 min | Lunch break |
| 6 | P6 | Teaching | 12:40 | 13:25 | 45 min | — |
| 7 | P7 | Teaching | 13:25 | 14:10 | 45 min | — |
| 8 | P8 | Teaching | 14:10 | 14:55 | 45 min | — |
| — | Dispersal | Admin | 14:55 | 15:00 | 5 min | Bus dismissal |

**Slot Types:**
- **Teaching** — regular academic period; subjects can be assigned
- **Break** — no subject assignment; shown as gap in timetable
- **Assembly** — fixed school assembly; no teacher needed (or VP/Principal takes it)
- **PT/Games** — Physical Education; PT teacher assigned
- **Library** — library period rotation
- **Free** — free period (rare; usually in senior secondary for self-study)

### 4.2 Period Totals (auto-computed)
```
Teaching periods per day: 8
Total teaching minutes per day: 360 min (6 hours)
Break time: 55 min
Total school day: 415 min (6h 55m)
School start: 08:00  ·  School end: 15:00
```

---

## 5. Wednesday Assembly Schedule (Example)

| Slot # | Label | Type | Start Time | End Time | Duration |
|---|---|---|---|---|---|
| — | Assembly | Assembly | 08:00 | 08:30 | 30 min |
| 1 | P1 | Teaching | 08:30 | 09:10 | 40 min |
| 2 | P2 | Teaching | 09:10 | 09:50 | 40 min |
| 3 | P3 | Teaching | 09:50 | 10:30 | 40 min |
| — | Break | Break | 10:30 | 10:45 | 15 min |
| 4 | P4 | Teaching | 10:45 | 11:25 | 40 min |
| 5 | P5 | Teaching | 11:25 | 12:05 | 40 min |
| — | Lunch | Break | 12:05 | 12:45 | 40 min |
| 6 | P6 | Teaching | 12:45 | 13:25 | 40 min |
| 7 | P7 | Teaching | 13:25 | 14:05 | 40 min |
| — | Dispersal | Admin | 14:05 | 14:10 | 5 min |

---

## 6. Double Period Configuration

For lab sessions (90-min chemistry/physics/biology labs, 90-min computer labs), two consecutive periods merge:

```
Double Period Slots:
  P5 + P6 = Lab Block (90 min) — can be used for any class requiring lab
  P7 + P8 = Lab Block (90 min) — alternates with P5+P6 for different classes
```

Double periods must be explicitly defined here so the Timetable Builder (B-07) knows that assigning "Lab" for a class occupies two consecutive slots and requires lab room booking.

---

## 7. Schedule Assignment to Days

Matrix showing which schedule applies on which day for each class group:

| | Mon | Tue | Wed | Thu | Fri | Sat |
|---|---|---|---|---|---|---|
| Classes I–V | Primary Standard | Primary Standard | Wednesday Assembly | Primary Standard | Primary Standard | Saturday Half-Day |
| Classes VI–X | Standard | Standard | Wednesday Assembly | Standard | Standard | Saturday Half-Day |
| Classes XI–XII | Standard | Standard | Wednesday Assembly | Standard | Standard | — (no Sat) |

Saturday applicability: configurable per class group. Many CBSE schools run Saturdays for Classes VI–X but not for XI–XII.

---

## 8. Period Configuration Edit Drawer (`period-slot-edit`, 400px)

| Field | Value |
|---|---|
| Label | P1 / P2 / Assembly / Lunch / Break (free text) |
| Type | Teaching / Break / Assembly / PT / Library / Free |
| Start Time | Time picker (15-min increments) |
| End Time | Auto-computed from start + duration, or manual |
| Duration | Auto-computed; manual override |
| Applies to Class Groups | Checkboxes: Primary (I–V) / Middle (VI–VIII) / Secondary (IX–X) / Sr Secondary (XI–XII) |
| Notes | Optional label shown in timetable display |

---

## 9. Bell Schedule Export

[Export Bell Schedule] → generates:
- **PDF format:** Printable bell schedule (one per schedule variant) for notice boards
- **Excel format:** All schedules in one sheet (for office use)
- **JSON format:** For automated bell system integration (bell rings at exact period start times)

Some schools use automated PA systems / electric bell controllers. EduForge exports a JSON file with all bell ring times that can be uploaded to compatible systems (e.g., CronTech, SchoolBell automated systems).

---

## 10. Validation Rules (enforced on save)

| Rule | Error Message |
|---|---|
| Overlapping slots | "P3 (09:30–10:15) overlaps with Break (10:15–10:30) — check end times" |
| Total teaching periods < 6 | Warning: "CBSE minimum 6 teaching periods per day recommended" |
| Period duration < 30 min | Warning: "Period P5 is only 25 min — unusually short" |
| School day > 8 hours | Warning: "Total school day exceeds 8 hours — check if this is correct" |
| No break between any 3 consecutive teaching periods | Warning: "CBSE guidelines recommend a break every 3 periods for junior classes" |

---

## 11. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/timetable/period-schedules/` | All defined schedules |
| 2 | `POST` | `/api/v1/school/{id}/timetable/period-schedules/` | Create new schedule |
| 3 | `GET` | `/api/v1/school/{id}/timetable/period-schedules/{schedule_id}/` | Schedule detail with slots |
| 4 | `PATCH` | `/api/v1/school/{id}/timetable/period-schedules/{schedule_id}/` | Update schedule |
| 5 | `POST` | `/api/v1/school/{id}/timetable/period-schedules/{schedule_id}/slots/` | Add slot to schedule |
| 6 | `PATCH` | `/api/v1/school/{id}/timetable/period-schedules/{schedule_id}/slots/{slot_id}/` | Edit slot |
| 7 | `DELETE` | `/api/v1/school/{id}/timetable/period-schedules/{schedule_id}/slots/{slot_id}/` | Remove slot |
| 8 | `GET` | `/api/v1/school/{id}/timetable/period-schedules/export/` | Export bell schedule |
| 9 | `GET` | `/api/v1/school/{id}/timetable/effective-schedule/?class_group={g}&day={day}` | Effective schedule for a class/day |

---

## 12. Business Rules

- At least one schedule must be marked Active before B-07 (Timetable Builder) can be used
- Modifying a period schedule after the timetable has been published triggers a warning: "Timetable built on this schedule will need to be re-validated"
- Period schedules are year-specific; they are copied to the next academic year during the Year Transition in A-08 and the Timetable Coordinator reviews and adjusts before publishing
- Principal must confirm (click [Approve Schedule]) before the period configuration is locked — this prevents Timetable Coordinator from quietly changing school hours
- Changing a schedule on a given day only affects future timetable planning; it does not retroactively alter historical timetable records

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division B*
