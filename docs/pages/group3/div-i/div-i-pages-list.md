# Division I — Transport Management — Pages List

> **Group:** 3 — School Portal
> **Division:** I — Transport Management
> **Total Pages:** 12
> **Directory:** `docs/pages/group3/div-i/`

---

## Purpose

Manages the school transport fleet — buses, vans, routes, and student transport enrollment. Indian school transport context:
- **Safety regulation:** Motor Vehicles Act + CBSE Transport Policy (2021) + state school transport rules mandate bus safety standards (yellow colour, school name, speed governors, GPS)
- **Supreme Court order (2012 — Ashok Kumar v. State):** Comprehensive school bus safety guidelines; CCTV mandatory; no overcrowding; first aid kit; lady escort for girls' schools
- **GPS tracking:** CBSE mandates GPS trackers on all school buses (post-2015 circular); parents must be able to track bus in real-time
- **Driver background verification:** CBSE requires police verification of drivers; drivers must hold commercial vehicle license (LMV badge for buses < 8 passengers, HMV for larger)
- **Transport fee:** Separate fee from tuition; collected termly; subject to FRA in some states (no arbitrary increase)
- **Contract vs own buses:** Many schools operate a mix — owned buses + hired from operators; hired operators must comply with same standards
- **Women's safety (girl students):** Female escort mandatory on all routes carrying girl students (CBSE circular + Supreme Court order)

---

## Roles (new to this division)

| Role | Code | Level | Description |
|---|---|---|---|
| Transport In-Charge | S3 | S3 | Manages fleet, routes, and transport staff |
| Driver | S2 | S2 | View-only: own route, student list, daily checklist |
| Female Escort | S2 | S2 | Attendance on bus; safety monitoring |
| Administrative Officer | S3 | S3 | Transport fee management |
| Academic Coordinator | S4 | S4 | Approve route changes |
| Principal | S6 | S6 | Policy approval; serious incident decisions |

---

## Pages

| Page ID | Title | URL Slug | Priority | Key Function |
|---|---|---|---|---|
| I-01 | Fleet Management | `transport/fleet/` | P1 | Vehicles, PUC, insurance, fitness certificates |
| I-02 | Route Management | `transport/routes/` | P1 | Routes, stops, timing, student allocation |
| I-03 | Student Transport Enrollment | `transport/enrollment/` | P1 | Student route assignment, pickup/drop points |
| I-04 | Driver & Escort Management | `transport/staff/` | P1 | Driver profiles, BGV, license, escort records |
| I-05 | Bus Attendance | `transport/attendance/` | P1 | Daily bus roll call; GPS cross-check |
| I-06 | GPS Live Tracking | `transport/gps/` | P1 | Real-time bus tracking; parent app integration |
| I-07 | Transport Fee | `transport/fees/` | P1 | Route-based fee billing; integrated with D-04 |
| I-08 | Incident & Accident Register | `transport/incidents/` | P0 | Accidents, breakdowns, student injuries on bus |
| I-09 | Safety Checklist | `transport/safety/` | P1 | Daily pre-trip inspection; CCTV check; first aid |
| I-10 | Parent Notifications | `transport/notifications/` | P1 | Late bus alerts, route changes, pickup confirmations |
| I-11 | Contract Transport | `transport/contracts/` | P2 | Hired buses/vans management and compliance |
| I-12 | Transport Reports | `transport/reports/` | P2 | Fleet utilisation, route efficiency, safety compliance |

---

## Key Integrations

- **C-05 Student Enrollment:** Transport flag; pickup/drop point
- **D-04 / D-07 Fee Collection:** Transport fee billing
- **E-01 Daily Attendance:** If student is absent and has transport — bus attendance cross-check
- **C-13 TC Generator:** Transport clearance required for TC (no outstanding transport dues)
- **F-10 Emergency Alert System:** Bus accident/incident triggers mass parent notification
- **L-01 Staff HR:** Driver and escort records (employment, BGV, leave)

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division I*
