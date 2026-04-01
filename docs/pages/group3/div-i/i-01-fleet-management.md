# I-01 — Fleet Management

> **URL:** `/school/transport/fleet/`
> **File:** `i-01-fleet-management.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Transport In-Charge (S3) — full management · Administrative Officer (S3) — document tracking · Principal (S6) — approve new vehicle additions

---

## 1. Purpose

Manages all school-owned vehicles — buses, vans, and cars. Tracks statutory documents (PUC, insurance, fitness certificate, road tax, school bus permit), maintenance schedules, and compliance status. Indian regulatory requirements:
- **Yellow school bus colour:** Mandatory (Supreme Court order 1992, reaffirmed 2012)
- **School name on bus:** "SCHOOL BUS" lettering; school name and contact number
- **Speed governor:** Mandatory for school buses (max 40 km/h in CBSE circular)
- **GPS tracking device:** CBSE circular 2015; state RTO mandates
- **CCTV cameras:** Supreme Court 2012 order; mandatory for all school buses
- **Fitness Certificate:** Annual renewal from RTO
- **PUC:** Pollution Under Control certificate — quarterly for diesel, half-yearly for CNG
- **Insurance:** Comprehensive (own damage + third party) mandatory; school buses must have passenger liability cover

---

## 2. Page Layout

### 2.1 Header
```
Fleet Management                                     [+ Add Vehicle]  [Export Fleet Register]
Academic Year: [2026–27 ▼]

Total vehicles: 12  ·  Active: 11  ·  In maintenance: 1
Document expiry alerts: 3 (PUC expiring in < 30 days)
```

### 2.2 Fleet Register
```
Vehicle No.   Type    Capacity  Driver        Route   PUC Expiry  Insurance Exp  Fitness Exp  Status
AP29AB1234   Bus 52  52 seats  Raju K.       Route 1  15 Apr 26   31 Mar 27     30 Jun 26    ✅ Active
AP29CD5678   Bus 52  52 seats  Suresh M.     Route 2  28 Apr 26   31 Mar 27     30 Jun 26    ✅ Active
AP29EF9012   Van 12  12 seats  Dinesh P.     Special  10 Apr 26   31 Mar 27     30 Jun 26    ✅ Active
AP29GH3456   Bus 40  40 seats  —             Route 3  20 Mar 26   31 Mar 27     30 Jun 26    🔧 Maint.
AP29IJ7890   Bus 52  52 seats  Kishore R.    Route 4  5 May 26    31 Mar 27     30 Jun 26    ✅ Active

⚠️ PUC expiry alerts:
  AP29AB1234 — PUC expires 15 Apr 2026 (19 days)
  AP29EF9012 — PUC expires 10 Apr 2026 (14 days)
  AP29GH3456 — PUC expires 20 Mar 2026 (EXPIRED — in maintenance)
```

---

## 3. Vehicle Profile

```
Vehicle: AP29AB1234 — Bus (52 seats)

Type: School Bus  ·  Make: TATA StarBus  ·  Model: LP 913/52  ·  Year: 2021
Colour: ✅ Yellow (school bus specification)
School name marking: ✅ "GREENFIELDS SCHOOL BUS — 040-23456789"

Statutory Documents:
  PUC Certificate:         Valid until 15 Apr 2026  ⚠️ Renew soon  [Upload new]
  Insurance:               Valid until 31 Mar 2027  ✅  [View policy]
  Fitness Certificate:     Valid until 30 Jun 2026  ✅  [View cert]
  Road Tax:                Paid until 31 Mar 2027   ✅
  School Bus Permit:       Valid until 30 Sep 2026  ✅  [View permit]
  Driver License (Raju K.): HMV, valid until 15 Nov 2028  ✅

Safety Equipment:
  Speed Governor:  ✅ Installed (max 40 km/h)  Last calibrated: 15 Jan 2026
  GPS Tracker:     ✅ Active  Device ID: GPS-BUS-001  Last ping: 27 Mar, 9:14 AM
  CCTV (interior): ✅ 2 cameras — last checked 20 Mar 2026
  First Aid Kit:   ✅ Stocked (checked weekly)
  Fire Extinguisher: ✅ Valid until Jun 2026
  Emergency Exit:  ✅ Functional

Assigned:
  Route: Route 1 (Chaitanyapuri – School)
  Driver: Raju Kumar (+91 9876-XXXXX)
  Female Escort: Ms. Kavitha (+91 8765-XXXXX)
  Students enrolled: 44/52 seats

Maintenance log:
  15 Jan 2026: Oil change + tire rotation
  10 Mar 2026: Brake pad replacement (rear) — ₹3,800
  Next service: 15 Apr 2026 (3-month interval)
```

---

## 4. Add Vehicle

```
[+ Add Vehicle]

Registration: [AP29KL1234]
Type: ● Bus  ○ Van/Mini-bus  ○ Car/SUV
Capacity (seats): [52]
Make: [TATA ▼]  Model: [StarBus LP 913/52]
Year of manufacture: [2022]
Ownership: ● Owned by school  ○ Hired (operator contract — see I-11)

Documents (upload):
  PUC Certificate: [Upload PDF] · Expiry: [15 Jul 2026]
  Insurance Policy: [Upload PDF] · Expiry: [31 Mar 2027] · Premium: ₹42,000
  Fitness Certificate: [Upload PDF] · Expiry: [30 Jun 2027]
  Road Tax receipt: [Upload PDF]
  School Bus Permit: [Upload PDF] · Expiry: [30 Sep 2027]

Safety equipment installed: ☑ Speed governor  ☑ GPS  ☑ CCTV (2 cameras)  ☑ Fire extinguisher
GPS device ID: [GPS-BUS-006]  (register with GPS provider)

[Save Vehicle]
```

---

## 5. Document Expiry Alerts

```
Document Expiry Calendar — Next 60 Days

Vehicle         Document         Expiry       Days Left   Action
AP29GH3456      PUC              20 Mar 2026  EXPIRED     [Renew immediately — vehicle grounded]
AP29EF9012      PUC              10 Apr 2026  14 days     [Schedule renewal]
AP29AB1234      PUC              15 Apr 2026  19 days     [Schedule renewal]
AP29AB1234      School Bus Permit 30 Sep 2026 188 days    [Upcoming — no action needed]

Rules:
  Expired PUC → vehicle cannot legally operate → immediately removed from route
  Expired Insurance → vehicle cannot operate → immediate grounding
  Expired Fitness Cert → vehicle cannot operate → grounding + RTO inspection

[Export document calendar]  [Send renewal reminders to Transport In-Charge]
```

---

## 6. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/transport/fleet/` | Fleet list |
| 2 | `POST` | `/api/v1/school/{id}/transport/fleet/` | Add vehicle |
| 3 | `GET` | `/api/v1/school/{id}/transport/fleet/{vehicle_id}/` | Vehicle profile |
| 4 | `PATCH` | `/api/v1/school/{id}/transport/fleet/{vehicle_id}/document/` | Update document (upload new) |
| 5 | `GET` | `/api/v1/school/{id}/transport/fleet/expiry-alerts/?days={30}` | Upcoming expiry alerts |
| 6 | `POST` | `/api/v1/school/{id}/transport/fleet/{vehicle_id}/maintenance-log/` | Log maintenance |
| 7 | `GET` | `/api/v1/school/{id}/transport/fleet/export/` | Fleet register export |

---

## 7. Business Rules

- A vehicle with expired PUC, insurance, or fitness certificate is automatically marked as "Grounded" — it cannot be assigned to a route until the document is renewed and uploaded
- CCTV footage is retained for 30 days (SD card loop in bus); if an incident is reported (I-08), the relevant footage must be downloaded and preserved before it is overwritten
- Speed governors are mandatory (max 40 km/h per CBSE circular); tampering with a speed governor is a serious offence; if a driver is caught over-speeding (GPS alert), immediate disciplinary action
- Insurance must specifically cover school bus (passenger-carrying vehicle) use; a standard commercial vehicle insurance without passenger liability coverage is insufficient
- Hired vehicles (I-11 contract transport) must also meet all these statutory requirements; the contract requires the operator to maintain compliance; the school verifies documents annually

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division I*
