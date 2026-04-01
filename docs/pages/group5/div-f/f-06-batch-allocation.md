# F-06 — Batch Allocation

> **URL:** `/coaching/admissions/batch-allocation/`
> **File:** `f-06-batch-allocation.md`
> **Priority:** P2
> **Roles:** Admissions Counsellor (K3) · Batch Coordinator (K4) · Branch Manager (K6)

---

## 1. Batch Allocation at Enrollment

```
BATCH ALLOCATION — LEAD-1842: Suresh Babu Rao
As of 30 March 2026

  COURSE ENROLLED:  SSC CGL 2026–27 (Full Batch, 10 months)

  AVAILABLE BATCHES:
    Batch Name               │ Start Date │ Timing       │ Mode    │ Seats Left │ Fit Score
    ─────────────────────────┼────────────┼──────────────┼─────────┼────────────┼──────────
    SSC CGL Morning (May 26) │ 4 May 2026 │ 6:00–9:00 AM │ Offline │     40     │ 98% ✅
    SSC CGL Evening (May 26) │ 4 May 2026 │ 4:00–7:00 PM │ Offline │     62     │ 82%
    SSC CGL Online (May 26)  │ 4 May 2026 │ 7:00–9:00 PM │ Online  │    108     │ 65%
    SSC CGL Morning (Aug 26) │ 3 Aug 2026 │ 6:00–9:00 AM │ Offline │    250     │ 70%

  FIT SCORE BASED ON:
    Preferred time: Morning ✅ (SSC CGL Morning = 100% match)
    Mode: Offline ✅ (matches)
    Location: Dilsukhnagar — 4 km from main campus ✅
    Deducted: -2% (40 seats left — batch nearly full, urgency to decide)

  RECOMMENDED:  SSC CGL Morning (May 2026) ← Pre-selected

  [Confirm Allocation: SSC CGL Morning May 2026]   [Change Batch]

  WARNING: Batch Morning (May 26) has only 40 seats.
  This enrollment fills 1 seat. Remaining after allocation: 39.
```

---

## 2. Pending Allocations Queue

```
BATCH ALLOCATION PENDING — (Enrolled but awaiting batch assignment)
As of 30 March 2026

  #  │ Student             │ Enrolled   │ Course       │ Requested Batch     │ Status
  ───┼─────────────────────┼────────────┼──────────────┼─────────────────────┼──────────────────
  1  │ Meena Kapoor (2499) │ 28 Mar     │ SSC CGL      │ Online (eve)        │ ⏳ Seat pending
  2  │ Arun Kumar  (2498)  │ 27 Mar     │ Banking PO   │ Banking Morning     │ ✅ Allocated today
  3  │ Renu Sharma (2497)  │ 27 Mar     │ SSC CGL      │ Morning (May)       │ ✅ Allocated
  4  │ Kiran Naidu (2496)  │ 26 Mar     │ Foundation   │ Foundation Jun      │ ⏳ Seat pending
  5  │ Priya Devi  (2495)  │ 25 Mar     │ RRB NTPC     │ RRB Morning (Jun)   │ ✅ Allocated

  PENDING REASON:
    Meena Kapoor: Online evening batch at 80% capacity — auto-held for mgr review
    Kiran Naidu: Foundation Jun batch not yet confirmed (minimum 50 students needed)

  [Allocate Meena → Online Evening]   [Confirm Foundation Jun batch]
```

---

## 3. Batch Capacity Dashboard

```
BATCH CAPACITY — All Upcoming Batches (May–Jun 2026)

  Batch                    │ Capacity │ Allocated │ Remaining │ Status
  ─────────────────────────┼──────────┼───────────┼───────────┼──────────────────────
  SSC CGL Morning (May)    │   250    │   211     │    39     │ 🔴 Near full
  SSC CGL Evening (May)    │   250    │   188     │    62     │ 🟡 Filling
  SSC CGL Online (May)     │   500    │   392     │   108     │ ✅ Available
  Banking Morning (May)    │   200    │   158     │    42     │ 🟡 Filling
  Banking Evening (May)    │   200    │   124     │    76     │ ✅ Available
  RRB NTPC Morning (Jun)   │   200    │    90     │   110     │ ✅ Available
  Foundation Morning (Jun) │   150    │    62     │    88     │ ⚠️ Below min (need 50)
  ─────────────────────────┴──────────┴───────────┴───────────┴──────────────────────

  ⚠️ Foundation Jun: 62 enrolled — batch minimum is 50 ✅ confirmed
     (Was at risk — confirmed viable now that 62 > 50)
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/batches/upcoming/seats/` | Upcoming batch capacity and seats |
| 2 | `POST` | `/api/v1/coaching/{id}/admissions/enroll/{eid}/batch/` | Allocate student to a batch |
| 3 | `GET` | `/api/v1/coaching/{id}/admissions/batch-allocation/pending/` | Students awaiting batch assignment |
| 4 | `PATCH` | `/api/v1/coaching/{id}/admissions/enroll/{eid}/batch/` | Change batch allocation |
| 5 | `GET` | `/api/v1/coaching/{id}/admissions/batch-allocation/fit/?student={sid}&course={c}` | Fit score for available batches |

---

## 5. Business Rules

- Batch allocation is the final step in enrollment before the student is fully active in the system; an enrolled student without a batch allocation cannot access the student portal's batch-specific content (timetable, batch announcements, attendance records); allocation should happen at enrollment time wherever possible; the "pending allocation" queue exists only for edge cases (batch not yet confirmed, seat on hold, student preference requires waiting for a new batch)
- The batch minimum enrollment rule (Foundation batch requires at least 50 students to run) protects TCC from running financially unviable batches; a batch with 20 students costs the same to run as one with 150 students (hall, faculty, AC, materials) but generates 1/7.5 the revenue; if the minimum is not met 21 days before the batch start date, TCC either combines the batch with another (if a similar batch is running) or reschedules; all enrolled students are notified and offered a choice of alternative batch or full refund
- Batch reallocation (a student requesting to move from Morning to Evening) is permitted up to 14 days before batch start; after batch start, reallocation requires Branch Manager approval and the receiving batch must have a seat; reallocation is not free — a ₹500 administrative fee is charged (plus any applicable GST); this discourages frivolous requests and covers the administrative cost of updating records in the batch coordinator's system
- The "fit score" algorithm recommends the best batch based on: preferred timing (40%), mode (offline/online) preference (30%), proximity to campus (20%), and available seats (10%); the counsellor can override the recommendation but must log the reason; if a student is allocated to a less suitable batch against their stated preference, the counsellor's note is reviewed if the student later complains about the batch assignment — the note serves as evidence of an informed decision
- Batch allocation is immediately communicated to the student (WhatsApp + email) and to the Batch Coordinator; the coordinator adds the student to the batch WhatsApp group and EduForge batch group after BGV is complete; premature addition to the group (before BGV) is a process violation — the coordinator should not add students who have not passed identity verification to the batch's official communication channel

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division F*
