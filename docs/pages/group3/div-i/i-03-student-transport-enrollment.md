# I-03 — Student Transport Enrollment

> **URL:** `/school/transport/enrollment/`
> **File:** `i-03-student-transport-enrollment.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Transport In-Charge (S3) — manage enrollments · Administrative Officer (S3) — assign routes · Academic Coordinator (S4) — approve route changes

---

## 1. Purpose

Links students to transport routes — manages which students use the school bus, which stop they board/alight at, and the associated transport fee billing. Enrollment changes when:
- A new student joins and opts for transport
- A student moves (new address, new stop)
- A student discontinues transport mid-year
- Annual reallocation at start of academic year

---

## 2. Page Layout

### 2.1 Header
```
Student Transport Enrollment                         [+ Enroll Student]  [Bulk Assign by Area]
Academic Year: [2026–27 ▼]

Total transport students: 240/380 (63%)
Day scholars (no transport): 140 (37%)
Pending transport application: 3 (waiting for route capacity)
```

### 2.2 Enrollment List
```
Filter: Route [All ▼]  Class [All ▼]

Student         Class  Route   Pickup Stop          Drop Stop  Fee/Term   Status
Arjun Sharma    XI-A   R01     Kothapet Bus Stop    Same       ₹4,500     ✅ Active
Priya Venkat    XI-A   R01     Chaitanyapuri XRds   Same       ₹4,500     ✅ Active
Vijay S.        X-B    R04     Vanasthalipuram      Same       ₹5,000     ✅ Active
Meena D.       XII-A   R02     LB Nagar             Same       ₹4,200     ✅ Active
Chandana Rao   XI-A    None    —                    —          ₹0         🏠 Day scholar
```

---

## 3. Enroll Student for Transport

```
[+ Enroll Student]

Student: [Chandana Rao — XI-A]
Academic Year: 2026–27
Transport option: ● School bus  ○ Hired vehicle (for staff children)

Address: Auto-filled from C-05: Flat 4, Srinagar Colony, Dilsukhnagar

Route suggestion (based on address):
  Nearest routes:
  ● Route R03 (Dilsukhnagar) — Dilsukhnagar X-Roads stop (500 m from address)
  ○ Route R01 (Chaitanyapuri) — Kothapet Bus Stop (2.1 km from address)

Selected route: R03 — Dilsukhnagar
Pickup stop: Dilsukhnagar X-Roads  ·  Pickup time: 7:00 AM

Availability check:
  Route R03 — Capacity: 40  ·  Current: 30  ·  After enrollment: 31/40 ✅

Drop arrangement: ● Same as pickup (two-way)  ○ Pick-up only  ○ Drop only

Transport fee: ₹4,800/term (Route R03 rate)
  → Added to D-07 fee ledger effective April 2026

Parent informed: ✅ WhatsApp: "Chandana is enrolled on Route R03 (Dilsukhnagar – School).
  Pickup: Dilsukhnagar X-Roads, 7:00 AM. Driver: Mr. Dinesh (+91 7654-XXXXX)"

[Confirm Enrollment]
```

---

## 4. Transport Discontinuation

```
Stop Transport — Vijay S. (X-B)

Reason: ● Family moving to nearby area  ○ Discontinuing own preference  ○ Other
Effective: [1 April 2026]

Transport fee refund (if applicable):
  Paid for Term 2 (Jan–Mar 2026): ₹5,000 paid
  Used: 27 Mar 2026 (3 days remaining in term)
  Refund: ₹500 (proportional for 3 unused days — configurable policy)
  → D-14 Security Deposit adjustment OR direct refund

[Confirm Discontinuation]

Driver/Escort notified: ✅ "Vijay S. will no longer use Route R04 from 1 Apr 2026."
Parent: ✅ Confirmed
Route R04 capacity: 55 → 54/52 (still overloaded — reassignment still needed)
```

---

## 5. Temporary Transport Change

```
Temporary Change — Parent Request

Student: Arjun Sharma (XI-A) — Regular: Route R01 (Kothapet Bus Stop)
Request: Tomorrow (28 Mar) — will be at uncle's house (Dilsukhnagar)
          Please allow boarding at Dilsukhnagar X-Roads (R03 stop)

Transport In-Charge review:
  Route R03 seats available: 9/40 ✅
  [Approve temporary stop for 28 Mar only]

Driver/Escort notified: "Arjun Sharma to board at Dilsukhnagar X-Roads tomorrow only."
Parent confirmed: ✅

Note: This is a one-time change; does not affect regular enrollment.
```

---

## 6. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/transport/enrollment/?route={route_id}` | Enrolled students by route |
| 2 | `POST` | `/api/v1/school/{id}/transport/enrollment/` | Enroll student |
| 3 | `PATCH` | `/api/v1/school/{id}/transport/enrollment/{enr_id}/route/` | Change route |
| 4 | `DELETE` | `/api/v1/school/{id}/transport/enrollment/{enr_id}/` | Discontinue transport |
| 5 | `POST` | `/api/v1/school/{id}/transport/enrollment/{enr_id}/temp-change/` | One-day stop change |
| 6 | `GET` | `/api/v1/school/{id}/transport/enrollment/student/{student_id}/` | Student transport details |

---

## 7. Business Rules

- Transport enrollment triggers fee billing in D-07; the fee is based on route (I-07) and effective from the enrollment date (prorated for mid-term enrollment)
- A student cannot be enrolled on a route that is at full capacity — hard block; they are placed on a waitlist with parent notification
- Parents can request temporary stop changes with 24-hour notice; the Transport In-Charge approves based on route capacity; more than 5 temp changes per term requires a formal route change
- TC clearance (C-13) checks for outstanding transport dues — if fees are unpaid, TC is blocked
- DPDPA: Student address (used for route assignment) is shared with the driver and escort as "student stop" only (no home address) — the driver receives a stop list with student names, not home addresses

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division I*
