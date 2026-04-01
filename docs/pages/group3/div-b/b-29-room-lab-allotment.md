# B-29 — Room & Lab Allotment

> **URL:** `/school/academic/timetable/rooms/`
> **File:** `b-29-room-lab-allotment.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Timetable Coordinator (S3) — full · HOD (S4) — read · Exam Cell Head (S4) — read (exam mode) · All teaching staff — read own schedule · Principal (S6) — full

---

## 1. Purpose

Manages the school's physical infrastructure as a schedulable resource. Every classroom, laboratory, library, computer lab, and auditorium is registered here with its capacity and purpose. When the Timetable Builder (B-07) assigns a class-subject-teacher combination to a period, it must also verify that the required room type is available — a Chemistry lab period can't be scheduled if the only chemistry lab is already occupied by another class at that time. Room allotment also prevents exam hall conflicts during examination periods. Critically, in Indian schools with one physics lab, one chemistry lab, and one biology lab, competing demand from Classes VI through XII makes resource conflict a daily operational challenge.

---

## 2. Page Layout

### 2.1 Header
```
Room & Lab Allotment                              [+ Add Room]  [Export Schedule]
Campus: [Main Building ▼]  Type: [All ▼]  Day: [Monday ▼]
Rooms registered: 48  ·  Labs: 7  ·  Halls/Special Rooms: 4
```

---

## 3. Room Registry

All rooms registered in the school:

| Room ID | Room Name | Type | Block/Floor | Capacity | Features | Status |
|---|---|---|---|---|---|---|
| R-101 | Room 101 | Classroom | Block A / Floor 1 | 45 | Projector, Whiteboard | ✅ Available |
| R-203 | Room 203 | Classroom | Block A / Floor 2 | 48 | Smart Board | ✅ Available |
| L-SCI-P | Physics Lab | Science Lab | Block B / Floor 1 | 30 | 15 lab benches, projector, weighing balance | ✅ Available |
| L-SCI-C | Chemistry Lab | Science Lab | Block B / Floor 1 | 30 | 15 lab benches, fume hood, reagent storage | ✅ Available |
| L-SCI-B | Biology Lab | Science Lab | Block B / Floor 2 | 30 | Microscopes (15), charts, specimens | ✅ Available |
| L-COMP-1 | Computer Lab 1 | Computer Lab | Block C / Floor 1 | 40 | 40 computers, A/C, projector | ✅ Available |
| L-COMP-2 | Computer Lab 2 | Computer Lab | Block C / Floor 1 | 40 | 40 computers | ✅ Available |
| R-MATH | Maths Lab | Maths Lab | Block A / Floor 3 | 35 | Geoboards, abacus, geometry set | ✅ Available |
| R-LIB | Library | Library | Block D / Floor 1 | 60 | — | ✅ Available |
| R-AUD | Auditorium | Assembly Hall | Main Building | 800 | Stage, PA system, AC | Booked (Sat) |
| R-ACT | Activity Room | Multi-purpose | Block E / Floor 1 | 80 | Foldable chairs | ✅ Available |

**Room Types:**
- Classroom (general purpose)
- Science Lab (Physics / Chemistry / Biology)
- Computer Lab
- Maths Lab
- Language Lab
- Library
- Assembly Hall / Auditorium
- Activity / Multi-purpose Room
- Sports Complex
- Music Room
- Art Room

---

## 4. Room Weekly Grid View

Main operational view: shows room utilisation across the week.

Toggle between two views:

### View A — Room Timeline (default)

Select a room → see its week-at-a-glance:

```
Physics Lab — Weekly Schedule (Week 12, 24–28 Mar)
─────────────────────────────────────────────────────────────────────
         Mon         Tue         Wed         Thu         Fri
P1   [ IX-A Sci ]  [  Free   ] [ VIII-B ] [  Free  ]  [ XI-A Phy ]
P2   [ Free     ]  [ X-B Sci ] [ Free   ] [ IX-B Sci] [ Free     ]
P3   [ XI-A Phy ]  [ Free    ] [ Free   ] [ X-A Sci ] [ Free     ]
P4   [ Free     ]  [ XI-B Phy] [ Free   ] [ Free   ]  [ IX-A Sci ]
P5   [ XII-A Phy]  [ Free    ] [ XII-B  ] [ Free   ]  [ Free     ]
P6   [ Free     ]  [ XII-A Phy [Free    ] [ XI-A   ]  [ Free     ]
P7   [ Free     ]  [ Free    ] [ Free   ] [ Free   ]  [ X-B Sci  ]
P8   [ Free     ]  [ Free    ] [ Free   ] [ Free   ]  [ Free     ]
─────────────────────────────────────────────────────────────────────
Utilisation: 14/40 slots = 35%
```

Colour coding: occupied (blue) · free (light grey) · exam day (amber) · maintenance (red)

### View B — Day Overview

All rooms for a single day, all periods — used to spot room conflicts or under-utilisation at a glance.

```
Monday — All Rooms
Room         P1       P2       P3       P4       P5       P6       P7       P8
R-101       VI-A     VI-A     FREE    VII-B    VII-B    FREE     IX-A    IX-A
R-102       FREE    VII-A    VII-A    FREE     VIII-A   VIII-A   FREE     X-A
L-SCI-P     IX-A    FREE     XI-A    FREE     XII-A    FREE     FREE    FREE
L-SCI-C     FREE    XII-A    FREE    XI-B     FREE     XII-B    FREE    FREE
L-COMP-1    FREE    VIII-B   FREE    X-B      FREE     XI-CS    FREE    XII-CS
```

---

## 5. Room Booking (Manual Override)

For special events, exams, or one-off use, a room can be booked outside the regular timetable:

[+ Book Room] → booking form:

| Field | Value |
|---|---|
| Room | Dropdown |
| Date / Day | Date picker or recurring day |
| Periods | Multi-select (P1–P8) |
| Purpose | Regular class / Exam hall / Event / Maintenance / Remedial class / Counselling / External use |
| Booked By | Auto-filled (logged-in user) |
| Notes | Free text |

Booking conflicts are shown in real-time: "Physics Lab is already occupied by XI-A Physics during P3 on Monday."

---

## 6. Room Allotment for Exam Season

During exam periods (B-10 Exam Schedule), the Exam Cell Head needs to convert classrooms into exam halls:

**[Exam Hall Mode]** toggle — switches the room grid to show exam assignments:

| Room | Capacity | Exam Date | Exam Hall for | Invigilator Assigned |
|---|---|---|---|---|
| R-101 | 45 | 1 Apr | Hall A (Seats 1–45) | Ms. Priya, Mr. Rajan |
| R-102 | 45 | 1 Apr | Hall B (Seats 46–90) | Mr. Suresh, Ms. Kavitha |
| R-203 | 48 | 1 Apr | Hall C (Seats 91–138) | Dr. Anand, Ms. Leela |

This feeds into B-13 (Seating Arrangement) — exam hall allocation is done here; seating plan within the hall is generated in B-13.

---

## 7. Room Booking Conflict Detector

When a new timetable is being built in B-07 (Timetable Builder), room assignments from this page are checked in real-time:

- If Chemistry lab is assigned to two classes at the same period → conflict flag in B-09
- If Computer Lab 1 is under maintenance on Thursday → timetable builder shows it as unavailable

Conflict report (read-only view for HODs):
```
⚠️ Room Conflicts This Week:
  Chemistry Lab — Tuesday P4: XI-B (Chemistry) AND XII-A (Chemistry) both assigned
  Computer Lab 1 — Under maintenance Thursday P5–P8 (reported by IT staff)
```

---

## 8. Room Add / Edit Drawer (`room-booking-view`, 520px)

| Field | Type | Notes |
|---|---|---|
| Room ID | Text | Unique; used in timetable export |
| Room Name | Text | Display name (e.g., "Physics Lab", "Room 203") |
| Type | Dropdown | See room types in Section 3 |
| Block | Text | Building block / wing |
| Floor | Number | Floor number |
| Capacity | Number | Seating capacity (important for exam hall calculation) |
| Features | Multi-select tag | Projector, Smart Board, AC, Lab Benches, Computers, etc. |
| Available from | Date | If a new room is under construction and not yet ready |
| Status | Active / Maintenance / Inactive | |

---

## 9. Lab Inventory Link

Each lab room has a [View Inventory] link that shows high-level equipment availability (read-only from this page; full inventory managed in a separate system or sub-page):

```
Chemistry Lab — Equipment Summary
  Fume hoods: 3 (2 operational, 1 under repair)
  Lab burners: 30 (all operational)
  Weighing balances: 5 (all operational)
  Reagent stock: 87% adequate (last checked 20 Mar)
```

Flagged equipment issues feed the Safety Audit (A-31).

---

## 10. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/rooms/` | All rooms list |
| 2 | `POST` | `/api/v1/school/{id}/rooms/` | Add room |
| 3 | `PATCH` | `/api/v1/school/{id}/rooms/{room_id}/` | Edit room details |
| 4 | `GET` | `/api/v1/school/{id}/rooms/{room_id}/schedule/?week={date}` | Room weekly schedule |
| 5 | `GET` | `/api/v1/school/{id}/rooms/day-overview/?date={date}` | All rooms all periods for one day |
| 6 | `POST` | `/api/v1/school/{id}/rooms/{room_id}/bookings/` | Create manual booking |
| 7 | `GET` | `/api/v1/school/{id}/rooms/conflicts/?week={date}` | Conflict report |
| 8 | `GET` | `/api/v1/school/{id}/rooms/exam-halls/?exam_id={id}` | Exam hall assignments |
| 9 | `PATCH` | `/api/v1/school/{id}/rooms/exam-halls/` | Assign rooms to exam halls |
| 10 | `GET` | `/api/v1/school/{id}/rooms/utilisation/?month={month}` | Monthly utilisation stats |

---

## 11. Business Rules

- A room with status "Maintenance" or "Inactive" is excluded from timetable builder's room pool automatically
- Lab rooms can have a "max simultaneous classes" setting (default 1); some large schools have labs partitioned into two independent sections
- Room capacity is used in exam seating — if capacity is set to 45, the seating plan for that room will not exceed 45 students
- Rooms can be shared between school sections (e.g., lab shared between two school buildings on alternate days) — managed via booking slots
- Historical bookings are retained for 2 years (room utilisation reports for infrastructure planning)
- Timetable Coordinator can add/edit rooms; Principal must approve deactivating a room (to prevent accidentally removing an active room from the pool)

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division B*
