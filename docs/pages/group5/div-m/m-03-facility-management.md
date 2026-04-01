# M-03 — Facility & Asset Management

> **URL:** `/coaching/operations/facility/`
> **File:** `m-03-facility-management.md`
> **Priority:** P2
> **Roles:** Branch Manager (K6) · Operations Coordinator (K4) · Maintenance Staff

---

## 1. Facility Overview

```
FACILITY REGISTER — Toppers Coaching Centre, Hyderabad Main
Ground + 3 floors | Total area: 14,800 sq ft (owned building)

  FLOOR MAP:
    Ground Floor:  Reception, Counselling rooms (×3), Admin office,
                   Accounts office, Server room, Housekeeping store
    1st Floor:     Classrooms Room 1–3, Faculty room, Staff restrooms
    2nd Floor:     Classrooms Room 4–5, Hall A (200-seat), IT lab
    3rd Floor:     Hostel Block A (male — 30 rooms), Common room

  ADJACENT BUILDING (leased):
    Block B:       Hostel (female — 24 rooms), Warden quarters
    Block C:       Under construction (12 new hostel rooms — ready Jul 2026)

  AMENITIES:
    Drinking water: RO plant (serviced monthly) ✅
    Generator:      15 KVA (covers classrooms + server) ✅
    Fire safety:    10 extinguishers + 2 fire panels (inspected Jan 2026) ✅
    CCTV:           24 cameras (indoor + outdoor, 30-day recording) ✅
    Internet:       100 Mbps leased line (primary) + 40 Mbps backup ✅
    Elevator:       Not available (3-floor building — ramp for differently abled)
```

---

## 2. Maintenance Tracker

```
MAINTENANCE REQUESTS — Open
As of 31 March 2026

  ID     │ Location    │ Issue                      │ Priority │ Raised   │ Days Open │ Assigned To
  ───────┼─────────────┼────────────────────────────┼──────────┼──────────┼───────────┼────────────
  MNT-42 │ Room 4      │ AC unit not cooling        │ HIGH ⚠️  │ 23 Mar   │   8 days  │ AC vendor
  MNT-43 │ Hostel B-12 │ Hot water geyser fault     │ MEDIUM   │ 25 Mar   │   6 days  │ Electrician
  MNT-44 │ Reception   │ Printer paper jam (frequent)│ LOW      │ 26 Mar   │   5 days  │ Mohan D.
  MNT-45 │ Room 2      │ Projector screen cable worn │ MEDIUM   │ 27 Mar   │   4 days  │ IT team
  MNT-46 │ Hall A      │ 2 chairs broken            │ LOW      │ 28 Mar   │   3 days  │ Carpenter
  MNT-47 │ Hostel A-08 │ Window latch broken        │ LOW      │ 29 Mar   │   2 days  │ Mohan D.
  MNT-48 │ Block C     │ Construction dust in R.4   │ MEDIUM   │ 30 Mar   │   1 day   │ Housekeeping
  ───────┴─────────────┴────────────────────────────┴──────────┴───────────┴──────────┴────────────

  SLA:  HIGH = 24 hrs  │  MEDIUM = 3 days  │  LOW = 7 days
  BREACHED: MNT-42 (8 days, HIGH — AC vendor delayed ⚠️)

  RESOLVED THIS MONTH (March 2026): 24 requests ✅
```

---

## 3. Asset Register

```
ASSET REGISTER — Major Assets
TCC Hyderabad Main | Net Book Value as of Mar 2026

  Category          │ Count │ Gross Value  │ Depreciation │ Net Book Value │ Next Service
  ──────────────────┼───────┼──────────────┼──────────────┼────────────────┼─────────────
  Projectors        │   8   │  ₹4.0 L      │  ₹1.8 L      │  ₹2.2 L       │ Jun 2026
  AC units          │  12   │  ₹9.6 L      │  ₹3.2 L      │  ₹6.4 L       │ Apr 2026 *
  Computers (lab)   │  20   │  ₹6.0 L      │  ₹2.4 L      │  ₹3.6 L       │ May 2026
  Server + UPS      │   2   │  ₹4.8 L      │  ₹1.6 L      │  ₹3.2 L       │ Jun 2026
  CCTV system       │   1   │  ₹1.8 L      │  ₹0.6 L      │  ₹1.2 L       │ Jan 2027
  Biometric devices │   6   │  ₹0.6 L      │  ₹0.2 L      │  ₹0.4 L       │ Dec 2026
  Furniture (total) │  —    │  ₹8.4 L      │  ₹2.8 L      │  ₹5.6 L       │ Ongoing
  RO Plant          │   2   │  ₹0.8 L      │  ₹0.3 L      │  ₹0.5 L       │ Apr 2026 *
  Generator         │   1   │  ₹2.4 L      │  ₹0.8 L      │  ₹1.6 L       │ May 2026
  ──────────────────┴───────┴──────────────┴──────────────┴────────────────┴─────────────
  TOTAL             │  —    │ ₹38.4 L      │ ₹13.7 L      │ ₹24.7 L       │
  * Service overdue or due this month
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/operations/facility/` | Facility overview |
| 2 | `GET` | `/api/v1/coaching/{id}/operations/maintenance/` | Open maintenance requests |
| 3 | `POST` | `/api/v1/coaching/{id}/operations/maintenance/` | Raise new maintenance request |
| 4 | `PATCH` | `/api/v1/coaching/{id}/operations/maintenance/{mid}/resolve/` | Mark resolved |
| 5 | `GET` | `/api/v1/coaching/{id}/operations/assets/` | Asset register |
| 6 | `GET` | `/api/v1/coaching/{id}/operations/maintenance/analytics/?month=2026-03` | Maintenance analytics |

---

## 5. Business Rules

- Maintenance SLA timers start the moment a request is raised in the system; a HIGH priority request (AC fault affecting classroom use) that is not resolved in 24 hours triggers an automatic escalation email to the Branch Manager; after 72 hours, the Director is copied; TCC cannot control vendor responsiveness (the AC vendor's 8-day delay), but TCC must document the vendor failure and have a contingency plan (portable AC, temporary room shift); accepting a student-impact issue passively because "the vendor hasn't come yet" is not acceptable — the Branch Manager must apply pressure and have alternatives ready
- The asset register is updated when new assets are purchased, existing assets are written off, or assets are relocated between branches; depreciation is computed annually using the Written Down Value (WDV) method as required by the Income Tax Act; the Schedule II of Companies Act 2013 prescribes asset lives (computers: 3 years, AC: 5 years, furniture: 10 years); TCC's accountant files the depreciation claim in the annual ITR; assets below ₹5,000 individual cost are expensed immediately rather than capitalised; the asset register is audited annually by TCC's statutory auditor
- Fire safety compliance is non-negotiable; TCC must maintain valid fire NOC (No Objection Certificate) from the local fire department; the NOC is renewed annually and requires inspection of fire extinguishers, exit routes, fire panels, and staff fire drill records; an institution without a valid fire NOC is operating illegally and faces closure orders; the annual fire safety inspection is scheduled in January each year (completed Jan 2026); the extinguisher service records are kept in the facility register and must be available during inspection; any new construction (Block C) must have a separate fire clearance before students occupy the space
- CCTV footage (30-day rolling retention) is stored on the server room's NVR; access to footage is restricted to the Branch Manager and Director; footage is reviewed only when there is a specific incident (theft, safety event, conduct complaint requiring corroboration); routine browsing of student footage without a specific purpose is a privacy violation under DPDPA 2023; students and staff are informed of CCTV coverage at enrollment/joining; cameras in bathrooms, counselling rooms, and bedrooms are prohibited (installed only in common areas, corridors, entry/exit points)
- Block C construction creates a temporary dust and noise disruption; the Branch Manager must notify affected students and staff before construction begins; scheduled construction hours must avoid class time (before 8:30 AM and after 6:30 PM on weekdays); the contractor is contractually required to contain dust and maintain safety barriers between the construction zone and the student-occupied building; non-compliance by the contractor is grounds for penalty deduction from the construction contract; student complaints about construction disruption (MNT-48) are addressed immediately with housekeeping, not dismissed

---

*Last updated: 2026-03-31 · Group 5 — Coaching Portal · Division M*
