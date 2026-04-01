# D-02 — Room & Bed Management

> **URL:** `/college/hostel/rooms/`
> **File:** `d-02-room-management.md`
> **Priority:** P1
> **Roles:** Warden (S3) · Hostel Admin (S3) · Chief Warden (S4)

---

## 1. Room Register

```
ROOM REGISTER — Boys' Hostel Block B
(Warden view — all rooms with current occupants)

BLOCK B OVERVIEW:
  Total rooms: 30  |  Total beds: 60  |  Occupied beds: 57  |  Vacant beds: 3

  Room   | Type   | Bed 1          | Bed 2          | Remarks
  ────────────────────────────────────────────────────────────────────
  B-101  | 2-bed  | Kiran S. (312) | Suresh V. (318)| ✅ Normal
  B-102  | 2-bed  | Ramesh T. (401)| VACANT         | Waiting list
  B-103  | 2-bed  | Ajay P. (511)  | Deepak R. (522)| ✅ Normal
  B-104  | 2-bed  | VACANT         | VACANT         | Under maintenance
  ...    | ...    | ...            | ...            | ...
  B-301  | 2-bed  | Vishal K. (621)| Prakash N.(632)| ✅ Normal (final yr)

MAINTENANCE ROOMS (under repair — not allocatable):
  B-104: Bathroom seepage — plumber scheduled 29 Mar 2027
  B-219: AC unit faulty — electrician scheduled 1 Apr 2027

GROUND FLOOR ACCESSIBLE (PwD):
  B-G01: Arjun V. (226J1A0315 — PwD certificate: locomotor disability)
  B-G02: VACANT (reserved for PwD applications only)
```

---

## 2. Room Amenities Register

```
ROOM AMENITIES — Block B Standard (2-bed)
(NBC 2016 / AICTE hostel guidelines compliance)

MANDATORY AMENITIES (per AICTE):
  Beds: 2 × single beds with mattress ✅
  Study furniture: 2 × study table + chair ✅
  Storage: 2 × personal wardrobe (lockable) ✅
  Lighting: 1 tube light + 1 bedside lamp ✅
  Ventilation: 1 window (min 1/10th floor area — NBC) ✅
  Electrical: 2 power points per bed + 1 dedicated laptop point ✅
  Network: 1 LAN port + WiFi coverage (EduNet AP per floor) ✅
  Housekeeping: Daily cleaning 6:00–8:00 AM (room must be vacated) ✅

ADDITIONAL AMENITIES (GCEH above minimum):
  Ceiling fan (1 per room) ✅
  Air cooler (Block B only — Block A ceiling fan only)
  Study lamp (1 per student) ✅
  Notice board (room + floor corridor) ✅

COMMON FACILITIES PER FLOOR:
  Common bathroom: 1 toilet + 1 shower per 6 students (NBC: 1:8 minimum)
  Drinking water: RO dispenser (floor-level) ✅
  Common room: 1 per block (TV, newspaper, indoor games)
  Laundry: 2 washing machines per block (shared) ✅
  WiFi router: 1 per floor (100 Mbps shared) ✅

BLOCK A vs BLOCK B vs BLOCK C:
  Block A (3-bed): Older building (2010); no AC/cooler; common bathrooms
  Block B (2-bed): Renovated 2022; attached bathroom (4 rooms share); coolers
  Block C (Girls): 2-bed; attached bathroom (2 rooms share); air cooler + geyser ✅
```

---

## 3. Maintenance Tracking

```
MAINTENANCE TICKETS — Active (Hostel)

Ticket   | Room   | Issue                    | Status          | ETA
─────────────────────────────────────────────────────────────────────────
M-2240   | B-204  | Window hinge loose        | In Progress     | 28 Mar
M-2241   | B-104  | Bathroom seepage          | Plumber assigned| 29 Mar
M-2242   | B-219  | AC unit not cooling       | Parts ordered   | 1 Apr
M-2243   | C-312  | Geyser thermostat faulty  | Replaced ✅     | 26 Mar
M-2244   | A-118  | Bed frame broken          | Carpenter visit | 28 Mar
M-2245   | B-Floor2| RO filter replacement   | Scheduled       | 30 Mar

STUDENTS CAN RAISE TICKETS:
  Via EduForge app: Hostel → Maintenance Request
  Category: Electrical / Plumbing / Furniture / Housekeeping / Other
  Response SLA: 48 hours for non-urgent; 4 hours for safety issues (water/electrical)
  Escalation: If unresolved in SLA → auto-escalates to Chief Warden

COMPLETED THIS MONTH: 18 tickets (avg resolution 1.8 days)
```

---

## 4. Room Transfer / Swap

```
ROOM TRANSFER REQUEST

Student: Rahul N. (226J1A0445)
Current: Block A, Room A-312, Bed-03
Request: Transfer to Block B (medical reason — attached bathroom needed)
Reason: Post-surgery, cannot walk to common bathroom
Supporting doc: Doctor certificate ✅

STATUS: Chief Warden approved ✅
New room: B-207 (Bed-01) — vacated by transferred student
Transfer date: 28 March 2027
Room condition check (A-312 vacated bed): ✅ No damage

SWAP REQUEST (student-initiated):
  Student A: Kiran S. (B-204) requests swap with Student B: Arun M. (A-118)
  Reason: Friends want to share room
  Warden review: No objection (both same year, no disciplinary issues)
  Chief Warden: Approved (subject to room condition check both rooms)
  Status: Swap completed 25 March 2027
```

---

## 5. Check-Out Process

```
CHECK-OUT — Outgoing Student
Student: Vinod K. (226J1A0512) — TC to NIT Warangal

CHECK-OUT CHECKLIST:
  ✅ No outstanding hostel dues (₹0 pending as of check-out)
  ✅ Room vacated — condition check done with warden
  ✅ Keys returned (Room B-117, common room key)
  ✅ Mess outstanding: ₹450 (extra items from mess counter) — paid
  ✅ Library clearance (hostel library books returned)
  ✅ Gate access deactivated (biometric removed from hostel gate)
  ✅ Caution deposit (₹5,000): Refund initiated → NEFT within 5 days

ROOM CONDITION CHECK (vacating B-117):
  Furniture: ✅ Good
  Electrical: ✅ Good
  Walls: Minor scuff marks (normal wear) — No deduction
  Windows: ✅ Good
  Special: Arjun left a small hole in wall (picture hanging) — ₹200 deduction from deposit
  Net deposit refund: ₹4,800

CHECK-OUT COMPLETION: 26 March 2027, 11:30 AM
Room B-117 status: Available (waiting list #1 notified)
```

---

## 6. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/college/{id}/hostel/rooms/` | All rooms with occupancy status |
| 2 | `GET` | `/api/v1/college/{id}/hostel/rooms/{room_id}/` | Room detail with occupants |
| 3 | `POST` | `/api/v1/college/{id}/hostel/maintenance/` | Raise maintenance ticket |
| 4 | `GET` | `/api/v1/college/{id}/hostel/maintenance/` | All maintenance tickets |
| 5 | `POST` | `/api/v1/college/{id}/hostel/transfer/` | Room transfer/swap request |
| 6 | `POST` | `/api/v1/college/{id}/hostel/checkout/{student_id}/` | Process check-out |

---

## 7. Business Rules

- Room condition report at check-out must mirror the check-in report; deductions from the caution deposit can only be made for damage beyond normal wear and tear; normal scuffs, small nail holes for pictures, and similar minor wear are not chargeable — courts have consistently disallowed "cleaning charges" as blanket deductions from student deposits
- Maintenance SLA of 4 hours for electrical/water issues is non-negotiable; a student who is denied basic utilities (no water, no electricity) in a hostel room they are paying for has a valid consumer complaint; Chief Warden escalation after SLA breach ensures accountability
- PwD accessible rooms (Ground floor) must never be allocated to non-PwD students regardless of overall occupancy pressure; if a PwD student requests ground floor and it is occupied by a non-PwD student, the non-PwD student must be transferred — RPwD Act 2016 Section 16 mandates reasonable accommodation
- Room swaps between students must be warden-approved to maintain accurate records; informal swaps (students swapping without recording) make the hostel register inaccurate and create issues during fire evacuation headcounts or police verification
- Caution deposit refund must be processed within 5 working days of check-out; withholding deposits for extended periods without documented valid reasons is actionable under consumer protection law

---

*Last updated: 2026-03-27 · Group 4 — College Portal · Division D*
