# I-01 — Hostel Dashboard

> **URL:** `/coaching/hostel/dashboard/`
> **File:** `i-01-hostel-dashboard.md`
> **Priority:** P1
> **Roles:** Hostel Warden (K3) · Branch Manager (K6)

---

## 1. Hostel Overview

```
HOSTEL DASHBOARD — Toppers Coaching Centre, Hyderabad Main
As of 30 March 2026  |  Warden: Ms. Sunitha Verma

  ┌──────────────────────────────────────────────────────────────────────────────┐
  │  CAPACITY: 120  │  OCCUPIED: 108  │  VACANT: 12  │  OCCUPANCY: 90.0%       │
  └──────────────────────────────────────────────────────────────────────────────┘

  BLOCK SUMMARY:
    Block       │ Rooms │ Capacity │ Occupied │ Occupancy │ Status
    ────────────┼───────┼──────────┼──────────┼───────────┼──────────────────
    Block A (M) │  20   │    60    │    54    │   90.0%   │ ✅ Near full
    Block B (F) │  20   │    60    │    54    │   90.0%   │ ✅ Near full
    ────────────┴───────┴──────────┴──────────┴───────────┴──────────────────
    TOTAL       │  40   │   120    │   108    │   90.0%   │

  GENDER SPLIT:
    Male:   54 (Block A — 3 per room, 20 rooms, 2 rooms triple-vacancy remaining)
    Female: 54 (Block B — 3 per room, 20 rooms, 2 rooms triple-vacancy remaining)
    Mixed: Not applicable (strict gender segregation — mandatory)

  TODAY'S ALERTS:
    🟡 Room A-12: Light not working (reported 29 Mar) — maintenance pending
    🟡 Room B-08: Request for room change (student Divya S.) — pending decision
    ✅ Morning headcount: 108/108 accounted for (6:30 AM)
    ✅ Mess breakfast served: 7:00 AM (106 attended — 2 in class early)
```

---

## 2. Today's Operations

```
TODAY — 30 March 2026

  HEADCOUNTS:
    6:30 AM — Morning headcount: 108/108 ✅
    Curfew last night (10:30 PM): 106/108 in (2 had late-pass until 11 PM) ✅

  CLASS SCHEDULE (hostel students):
    5:45 AM: Study room opens
    6:00 AM: Morning batch (CGL, Banking) depart to campus
    9:15 AM: Breakfast return
    12:00 PM: Lunch (mess)
    3:00 PM: Evening batch departs
    7:00 PM: Evening batch returns
    7:30 PM: Dinner (mess)
    9:00 PM: Study time (mandatory — supervised)
    10:30 PM: Lights out (curfew)

  DEPARTURES (with gate pass / late pass):
    Ravi Singh (Room A-04):  Out from 2 PM — medical appointment (slip ✅)
    Priya Reddy (Room B-11): Out from 4 PM — personal errand (gate pass ✅)
```

---

## 3. Quick Actions

```
QUICK ACTIONS

  [+ Allot New Room]              → Opens I-02 Room Allotment
  [📋 Occupancy Report]           → Opens I-03 Occupancy Report
  [💰 Collect Hostel Fee]         → Opens I-04 Hostel Fee
  [🍽️ Today's Menu]               → Opens I-05 Mess Management
  [👤 Log Visitor]                → Opens I-06 Visitor Register
  [🔧 New Maintenance Request]    → Opens I-07 Maintenance

  PENDING ACTIONS (warden to-do):
    🔴 Room B-08 change request — Divya S. — awaiting decision
    🟡 A-12 light repair — follow up with maintenance
    🟡 3 students with hostel fee due Apr 1 — send reminders
    ✅ Monthly inspection report (March) — submitted to Branch Manager
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/hostel/dashboard/` | Hostel dashboard data |
| 2 | `GET` | `/api/v1/coaching/{id}/hostel/blocks/` | Block-level occupancy summary |
| 3 | `GET` | `/api/v1/coaching/{id}/hostel/headcount/?date=2026-03-30` | Headcount log for a day |
| 4 | `POST` | `/api/v1/coaching/{id}/hostel/headcount/` | Log headcount |
| 5 | `GET` | `/api/v1/coaching/{id}/hostel/alerts/` | Active alerts and pending warden tasks |

---

## 5. Business Rules

- Twice-daily headcounts (morning at 6:30 AM and curfew at 10:30 PM) are mandatory; if any student is unaccounted for after 15 minutes of the curfew check, the warden initiates a search protocol: call the student's mobile, then the emergency contact; if the student is a minor, the parent is called immediately; if unreachable after 30 minutes, the Branch Manager is notified; unreported absences from a hostel are a POCSO-relevant safety concern for minor residents and a duty-of-care obligation for all residents
- Strict gender segregation between Block A (male) and Block B (female) is enforced by the building design (separate entrances, separate stairwells, separate common areas); cross-block visits are prohibited at all times; this policy is stated in the hostel rules signed by the student and guardian at admission; a violation results in an immediate disciplinary hearing and mandatory guardian notification; the warden may involve the Branch Manager and if a minor is involved, the designated POCSO contact
- The hostel curfew time (10:30 PM) is calibrated to morning batch classes that start at 6 AM; students need at least 7 hours of sleep for effective preparation; exceptions for medical appointments, family emergencies, or cultural events require a late-pass (signed by warden) with return time specified; a student who stays out past their late-pass time is logged as a curfew violation; repeated violations (3+) are reported to the guardian and reviewed for hostel continuation
- Gate passes for daytime exits are recorded in the visitor/departure register (I-06) with destination, expected return time, and contact number; the warden does not need to approve casual daytime exits (students are adults or have parental consent) but does record them for duty-of-care; if a student doesn't return by expected time, the warden calls; if no response in 30 minutes, escalates to Branch Manager; this record-keeping is a practical safety measure, not surveillance
- The hostel is a revenue-generating service (₹3.15 Lakh/month in March 2026 — G-07); it must be managed both as a welfare facility (student safety) and a business (fee collection, cost control); the warden reports to the Branch Manager on both dimensions; the hostel P&L (rent, mess cost, utilities, staff) is reviewed monthly; the target is to run the hostel at break-even or a small margin; heavily subsidised hostels are a financial drain; TCC's hostel fees are priced at ₹6,000–8,000/month depending on room type

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division I*
