# I-02 — Room Allotment

> **URL:** `/coaching/hostel/rooms/`
> **File:** `i-02-room-allotment.md`
> **Priority:** P1
> **Roles:** Hostel Warden (K3) · Branch Manager (K6)

---

## 1. Room Allotment Map

```
ROOM ALLOTMENT — Block A (Male) | Toppers Coaching Centre
As of 30 March 2026

  BLOCK A — MALE (20 rooms × 3 beds = 60 capacity, 54 occupied)

  Room  │ Capacity │ Occupied │ Residents                        │ Status
  ──────┼──────────┼──────────┼──────────────────────────────────┼──────────────
  A-01  │    3     │    3     │ Akhil K. | Ravi S. | Karthik M.  │ ✅ Full
  A-02  │    3     │    3     │ Suresh P.| Rajesh K.| Arun K.    │ ✅ Full
  A-03  │    3     │    3     │ Mohan R. | Sriram N.| Vikram G.  │ ✅ Full
  A-04  │    3     │    3     │ Deepak R.| Arjun S. | Pavan R.   │ ✅ Full
  A-05  │    3     │    3     │ Kiran N. | Tarun K. | Nikhil V.  │ ✅ Full
  ...
  A-11  │    3     │    3     │ ...                              │ ✅ Full
  A-12  │    3     │    2     │ Mohammed R. | Sreekanth V.       │ 🟡 1 Vacant
  A-13  │    3     │    2     │ Ajay N.  | Rahul K.              │ 🟡 1 Vacant
  A-14  │    3     │    3     │ ...                              │ ✅ Full
  ...   (remaining rooms full)

  BLOCK B — FEMALE (similar layout, 2 vacancies)
    B-08: 2 occupied (room change request pending from Divya S.)
    B-16: 2 occupied (1 vacancy)

  VACANCIES AVAILABLE:
    Block A: 2 single-vacancy rooms (A-12, A-13)
    Block B: 2 single-vacancy rooms (B-08, B-16)
```

---

## 2. Allot New Room

```
NEW ROOM ALLOTMENT

  Student:         [TCC-2026-2501 — Suresh Babu Rao ▼]  ← Newly enrolled
  Gender:          Male → Block A only

  AVAILABLE ROOMS (Block A):
    Room A-12:  2 occupants (Mohammed R., Sreekanth V.) — 1 bed available
    Room A-13:  2 occupants (Ajay N., Rahul K.) — 1 bed available

  RECOMMENDED: Room A-13
    Current occupants: Akhil Kumar (SSC CGL) and Rajesh Kumar (SSC CGL)
    Same batch/course — good study compatibility ✅
    Floor: Ground floor (easy access) ✅

  CONFIRM ALLOTMENT:
    Student: Suresh Babu Rao (TCC-2026-2501)
    Room:    Block A, Room A-13, Bed 3
    From:    4 May 2026 (batch start) to 28 Feb 2027 (batch end)
    Monthly fee: ₹ 7,000 (A/C room, twin-sharing upgrade not available)

  [Confirm Allotment]   [Assign Different Room]   [Cancel]

  ACTIONS TRIGGERED:
    → Student notified via WhatsApp
    → Room A-13 updated to Full (3/3)
    → Hostel fee schedule created in G module (₹7,000/month × 10 months)
```

---

## 3. Room Change Request

```
ROOM CHANGE REQUEST — B-08 | Divya Sharma (TCC-2404)
Raised: 28 March 2026 | Status: Pending Decision

  CURRENT ROOM: B-08 (with Meena K. and Sravya R.)
  REQUESTED: Move to B-14 (with friends from her hometown)

  REASON: "My roommates have different study schedules. B-14 students (Anitha K.
  and Priya R.) have the same morning batch as me. Easier to study together."

  WARDEN'S ASSESSMENT:
    B-08 roommates: No complaints filed against Divya or by Divya
    B-14 availability: 1 vacancy ✅ (3-bed room, 2 occupied)
    Compatibility: Same batch = positive; friendship = subjective
    Risk: Friendships can sometimes reduce study focus (social distraction)

  DECISION:
    (●) Approve — effective Apr 1   ( ) Reject   ( ) Defer (ask for 2-week trial)

  BRANCH MANAGER NOTE: "Approve — same-batch roommates improve morning routine"

  [Approve]   [Reject with reason]
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/hostel/rooms/` | All rooms with occupancy status |
| 2 | `POST` | `/api/v1/coaching/{id}/hostel/rooms/{rid}/allot/` | Allot a student to a room |
| 3 | `GET` | `/api/v1/coaching/{id}/hostel/rooms/vacancies/` | List all vacant beds |
| 4 | `POST` | `/api/v1/coaching/{id}/hostel/rooms/change-request/` | Submit room change request |
| 5 | `PATCH` | `/api/v1/coaching/{id}/hostel/rooms/change-request/{rid}/resolve/` | Approve or reject change request |
| 6 | `DELETE` | `/api/v1/coaching/{id}/hostel/rooms/{rid}/vacate/{sid}/` | Vacate a student from a room |

---

## 5. Business Rules

- Room allotment considers course compatibility (students in the same morning batch have the same sleep/wake schedule — reduced friction) and mutual preference (students can request roommates by name); the warden has the final say on allotment; a student cannot demand a specific room as a right, only request it; compatibility-based allotment reduces complaints and room-change requests, which are administratively burdensome
- Gender segregation in room allotment is absolute and system-enforced; a female student cannot be allotted to Block A and vice versa; the system validates gender from the enrollment record before presenting available rooms; this is not only a policy rule but an infrastructure requirement (separate sanitary facilities per block); any data error in gender on the enrollment record that leads to a mis-allotment must be corrected before the student arrives at the hostel
- Room changes are allowed once per academic year without charge; a second room change requires a ₹500 administrative fee and Branch Manager approval; multiple room changes indicate either poor initial allotment or a student with social adjustment challenges; the warden documents the reason for every room change; a pattern of room changes for the same student is shared with the counsellor for student support assessment
- When a student leaves the hostel (course completion, withdrawal, or mid-year transfer), the room vacate process includes: room inspection by the warden, security deposit refund (if applicable), key return, and update to the room allotment system; the bed must be available for the next student; a vacated room that is not updated in the system shows false occupancy and prevents the next student from being allotted; the warden must update within 24 hours of a student's departure
- Triple-sharing rooms are the standard (3 beds per room at ₹7,000/month each = ₹21,000 per room); if a room has only 2 occupants, TCC still collects full rent from both (not a discount for having a vacant bed); however, the vacancy itself represents ₹7,000/month of lost revenue; the warden monitors vacancies and the Branch Manager tracks occupancy rate; a room vacant for more than 30 days is filled by the waitlist or by re-marketing the hostel facility

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division I*
