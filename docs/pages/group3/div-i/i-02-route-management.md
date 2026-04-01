# I-02 — Route Management

> **URL:** `/school/transport/routes/`
> **File:** `i-02-route-management.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Transport In-Charge (S3) — full · Academic Coordinator (S4) — approve changes · Administrative Officer (S3) — update stop timings

---

## 1. Purpose

Manages school bus routes — the sequence of stops, pickup/drop times, and student count at each stop. Route planning is critical for efficiency (fuel cost) and safety (route distance, road conditions).

---

## 2. Page Layout

### 2.1 Header
```
Route Management                                     [+ New Route]  [Optimise Routes]
Academic Year: [2026–27 ▼]

Total Routes: 8  ·  Total Students on Transport: 240/380 (63%)
Routes with issues: 1 (Route 4 — overloaded)
```

### 2.2 Route List
```
Route  Name                          Bus          Students  Seats  Start    Duration  Status
R01    Chaitanyapuri – School        AP29AB1234   44/52     52     6:45 AM  45 min    ✅ Active
R02    LB Nagar – School             AP29CD5678   38/52     52     6:55 AM  40 min    ✅ Active
R03    Dilsukhnagar – School         AP29GH3456   30/40     40     7:00 AM  35 min    🔧 Maint.
R04    Vanasthalipuram – School      AP29IJ7890   55/52     52     6:50 AM  50 min    ⚠️ Overloaded
R05    Nagole – School               AP29KL1234   32/40     40     7:05 AM  30 min    ✅ Active
Special: Staff transport             Van           8/12      12     7:30 AM  —         ✅ Active
```

---

## 3. Route Detail

```
Route R01 — Chaitanyapuri → School

Bus: AP29AB1234 (52 seats)  ·  Driver: Raju Kumar  ·  Escort: Ms. Kavitha
Students: 44  ·  Seats: 52  ·  Load: 85% ✅

Stops (in order — Morning Pickup):
  Stop  Location               Time    Students  Cumulative
  1     Paradise Circle        6:45 AM  8         8
  2     Chaitanyapuri X-Roads  6:50 AM  12        20
  3     Kothapet Bus Stop      6:55 AM  10        30
  4     Dilsukhnagar X-Roads   7:00 AM  8         38
  5     Meerpet Colony         7:05 AM  6         44
  6     School Gate            7:20 AM  [ARRIVE]  44 total

Evening Drop (reverse order):
  School Gate departs: 4:10 PM
  Meerpet Colony: 4:25 PM
  ...
  Paradise Circle: 4:55 PM (last drop)

Students per stop (with names): [View list]  [Print for driver]
```

---

## 4. Add / Edit Route

```
[+ New Route]

Route Name: [Bandlaguda – School            ]
Bus: [AP29MN5678 ▼]  (or assign later)
Driver: [Vijay Kumar ▼]  Escort: [Ms. Priya ▼]

Stops (add in order):
  Stop 1: [Bandlaguda Junction]  Pickup time: [6:55 AM]
  Stop 2: [Karmanghat X-Roads]   Pickup time: [7:02 AM]
  Stop 3: [Saroor Nagar]         Pickup time: [7:10 AM]
  [+ Add Stop]

School arrival time: [7:30 AM] (30 min before school start at 8:00 AM)
Evening departure: [4:10 PM]

Google Maps integration:
  [Auto-calculate route distance and time between stops]
  Estimated total distance: 18 km  ·  Estimated time: 35 minutes
  [View on map]

[Save Route]
```

---

## 5. Route Issue — Overloaded

```
⚠️ Route R04 — Overloaded Alert

Bus: AP29IJ7890 (52 seats)
Students enrolled: 55  ← 3 students over capacity (Supreme Court — no overcrowding)

Required action:
  Option 1: Move 3 students to another route (Route R05 has 8 vacant seats)
  Option 2: Add a second bus for Route R04 (if demand justifies)
  Option 3: Reduce enrollments (waitlist)

Transport In-Charge must resolve overcrowding before next school day.
[Reassign students to R05]  [Add spare bus to R04]

Supreme Court 2012 Order: No school bus shall carry more students than its
seating capacity. Violation → operator/driver prosecution + school liability.
```

---

## 6. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/transport/routes/` | Route list |
| 2 | `POST` | `/api/v1/school/{id}/transport/routes/` | Create route |
| 3 | `GET` | `/api/v1/school/{id}/transport/routes/{route_id}/` | Route detail with stops |
| 4 | `PATCH` | `/api/v1/school/{id}/transport/routes/{route_id}/` | Update route |
| 5 | `GET` | `/api/v1/school/{id}/transport/routes/{route_id}/students/` | Students on route |
| 6 | `GET` | `/api/v1/school/{id}/transport/routes/issues/` | Routes with problems (overload, no driver) |

---

## 7. Business Rules

- No bus may be assigned more students than its seating capacity (per Supreme Court 2012 order); the system hard-blocks enrollment on a full route
- Route changes (new stops, timing changes) require notification to parents 5 days in advance via F-03 WhatsApp + F-01 notice board
- A route with a vehicle in maintenance status is flagged; the Transport In-Charge must arrange an alternative vehicle or notify affected parents about temporary suspension
- Evening drop routes for girls must have a female escort on board until the last girl student is dropped; if the escort needs to leave early, a substitute must be arranged

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division I*
