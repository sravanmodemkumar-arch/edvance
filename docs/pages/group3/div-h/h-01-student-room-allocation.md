# H-01 — Student Room Allocation

> **URL:** `/school/hostel/rooms/`
> **File:** `h-01-student-room-allocation.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Chief Warden (S4) — full allocation authority · Warden (S3) — view own block · Administrative Officer (S3) — data entry · Principal (S6) — approve block-level changes

---

## 1. Purpose

Manages the physical allocation of hostel rooms and beds to students. Essential for:
- **Safety:** Fire evacuation requires knowing exactly which student is in which room/bed
- **Discipline:** Room allocation is strategic — mixing year groups, managing friendships/conflicts
- **Billing:** Room category (AC/Non-AC, single/double/dormitory) determines the hostel fee tier
- **Annual reallocation:** Each academic year, rooms are reallocated; Class XII students often get better rooms as seniors

---

## 2. Hostel Structure

```
Hostel Structure — Greenfields School

Boys' Hostel (Block A):
  Capacity: 180 boys (across 45 rooms)
  Room types:
    Single (1 bed): 5 rooms — Class XII seniors only
    Double (2 beds): 20 rooms — Class X and XII
    Triple (3 beds): 10 rooms — Class IX and XI
    Dormitory (6 beds): 10 rooms — Class VI–VIII
  Occupied: 168/180  ·  Vacant: 12 beds

Girls' Hostel (Block B):
  Capacity: 120 girls (separate block, female warden only)
  Room types: Similar structure
  Occupied: 112/120  ·  Vacant: 8 beds
```

---

## 3. Page Layout

### 3.1 Floor Plan View (Interactive)
```
Boys' Hostel — Ground Floor                          [+ Allocate Room]  [Bulk Reallocate]

Room  Type       Occupants                    Capacity  Status
101   Double     Arjun Sharma (XI-A)          2/2       🟢 Full
                 Ravi Kumar (XI-A)
102   Double     Suresh K. (IX-A)             1/2       🟡 Partial
                 [Vacant bed]
103   Triple     Vijay S. (X-B)               2/3       🟡 Partial
                 Dinesh P. (XI-B)
                 [Vacant bed]
104   Dormitory  Class VIII students (6)      6/6       🟢 Full
...

Legend: 🟢 Full  🟡 Partial  🔴 Vacant  🔵 Reserved
```

### 3.2 Student View
```
Room Search: [Student name]

Arjun Sharma (STU-0001187 — XI-A)
  Hostel: Boys' Hostel Block A
  Room: 101  ·  Bed: 1A
  Room type: Double  ·  Roommate: Ravi Kumar (XI-A)
  Allocated: 15 Jun 2025 (start of academic year)
  Block: A  ·  Floor: Ground
  Floor Warden: Mr. Suresh Kumar
```

---

## 4. Allocate / Reallocate

```
[+ Allocate Room]

Student: [New student or existing student]
Student: Chandana Rao (STU-0001190 — XI-A)  (new hostel admission from H-02)

Available beds (matching student class and gender):
  Block B, Room 201 (Double) — Bed 2B [Currently: 1/2 occupied — roommate Priya V.]
  Block B, Room 205 (Triple) — Bed 3C [Currently: 2/3 occupied]
  Block B, Room 212 (Single) — [Full — Class XII only]

Selected: Block B, Room 201, Bed 2B

Roommate compatibility check:
  Chandana Rao (XI-A) + Priya Venkat (XI-A) — same class ✅
  No known disciplinary conflicts ✅

Allocation effective: 28 March 2026
[Confirm Allocation]

Post-allocation:
  → Room allocation record created
  → Hostel fee tier updated (Double room → ₹12,000/term)
  → Parent notified: "Your ward Chandana has been allocated Room 201B
    in the Girls' Hostel. Block B. Warden: Ms. Radha (+91 9876-XXXXX)."
  → Warden notified of new arrival
```

---

## 5. Annual Reallocation

```
Annual Reallocation — Academic Year 2027–28

Step 1: Class promotions locked (after C-10 promotion)
Step 2: Generate reallocation plan:
  ● Class XII (new seniors) → Single rooms (5 available)
  ● Class XI → Better double rooms
  ● Class X → Triple rooms
  ● Classes VI–VIII → Dormitory

Bulk changes:
  Class XII promotion from Class XI:
    14 students currently in Triple → Move to Double/Single
    8 beds freed in Triple for incoming Class XI

  [Generate Optimised Reallocation Suggestion]
  [Review and Edit Suggestions]
  [Apply All Changes — Effective 15 June 2027]
```

---

## 6. Emergency Room Register

```
Emergency Evacuation Register — Boys' Hostel Block A

(Printed and posted in each room + warden office)

Room  Bed  Student           Class  Parent Phone
101   1A   Arjun Sharma      XI-A   +91 9876-XXXXX
101   1B   Ravi Kumar        XI-A   +91 8765-XXXXX
102   2A   Suresh K.         IX-A   +91 7654-XXXXX
102   2B   [Vacant]
...

Total in block: 168 students
Emergency assembly point: Cricket Ground (east side)
Block A Warden: Mr. Suresh Kumar (+91 9999-XXXXX)

[Print Emergency Register]  ← A4 laminated, updated each term
```

---

## 7. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/hostel/rooms/?block={block}&floor={floor}` | Room occupancy view |
| 2 | `POST` | `/api/v1/school/{id}/hostel/rooms/allocate/` | Allocate student to room |
| 3 | `PATCH` | `/api/v1/school/{id}/hostel/rooms/reallocate/` | Reallocate (move student) |
| 4 | `GET` | `/api/v1/school/{id}/hostel/rooms/student/{student_id}/` | Student's current room |
| 5 | `GET` | `/api/v1/school/{id}/hostel/rooms/occupancy-summary/` | Block-level occupancy |
| 6 | `GET` | `/api/v1/school/{id}/hostel/rooms/emergency-register/?block={block}` | Emergency register PDF |
| 7 | `POST` | `/api/v1/school/{id}/hostel/rooms/bulk-reallocation/` | Annual bulk reallocation |

---

## 8. Business Rules

- Room allocation for girls' hostel is managed exclusively by female wardens; male staff (including Admin Officers) cannot view or edit girls' hostel room assignments (privacy requirement; MHA hostel safety guidelines)
- Single rooms are reserved for Class XII students (seniority privilege); allocation requires Chief Warden approval
- Dormitory students (primary classes VI–VIII) are allocated by class group where possible — familiar classmates reduce homesickness
- Emergency room register must be printed and posted in each room and at the warden office at the start of each term; it is reviewed after every room change
- TC clearance (C-13) checks that the student has vacated their room and returned all hostel property — linked via H-09 hostel clearance gate
- Room transfer requests (student wants to change room) require Chief Warden approval and must document the reason; frivolous requests are denied

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division H*
