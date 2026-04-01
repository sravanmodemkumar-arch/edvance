# M-01 — Operations Dashboard

> **URL:** `/coaching/operations/`
> **File:** `m-01-operations-dashboard.md`
> **Priority:** P2
> **Roles:** Branch Manager (K6) · Operations Coordinator (K4) · Director (K7)

---

## 1. Operations Overview

```
OPERATIONS DASHBOARD — Toppers Coaching Centre
Hyderabad Main Branch | 31 March 2026

  ┌──────────────────────────────────────────────────────────────────────┐
  │  BRANCH STATUS: ✅ OPERATIONAL                                       │
  ├──────────────┬───────────────┬──────────────┬────────────────────────┤
  │  STAFF        │  FACILITIES   │  IT SYSTEMS  │  COMPLIANCE            │
  │  42/44 present│  All rooms OK │  All online  │  4 items due Apr 2026  │
  │  2 on leave   │  1 AC unit ⚠️ │  Uptime 99.6%│  0 overdue ✅         │
  │  0 absent     │  7 open maint │  Backup ✅   │  Next audit: May 2026  │
  ├──────────────┴───────────────┴──────────────┴────────────────────────┤
  │  TODAY'S SCHEDULE (31 Mar 2026, Tuesday):                            │
  │    Classes running:    12/12  (all on time ✅)                       │
  │    Faculty present:    14/14                                         │
  │    Rooms occupied:     10/12  (2 in afternoon slot)                  │
  │    Hostel students:    84/84  (all checked in ✅)                    │
  │    Online classes:      4 live (356 students connected)              │
  └──────────────────────────────────────────────────────────────────────┘

  OPEN TASKS:
    Maintenance: 7 open requests (oldest: 8 days — AC unit Room 4) ⚠️
    Procurement: 2 pending purchase orders (whiteboard markers, printing paper)
    HR:          1 open position (Admin Coordinator — interviews Apr 5)
    Compliance:  GST return due Apr 20 | TDS deposit due Apr 7
```

---

## 2. Daily Operations Log

```
DAILY OPERATIONS LOG — 31 March 2026

  TIME    │ EVENT                                          │ STATUS     │ Note
  ────────┼────────────────────────────────────────────────┼────────────┼──────────────────
  7:00 AM │ Security handover (night → day shift)          │ ✅ Done    │
  8:00 AM │ Housekeeping round (classrooms + hostel)       │ ✅ Done    │
  8:30 AM │ IT systems check (server, LMS, cameras)        │ ✅ Online  │
  9:00 AM │ Morning batch check-in (Attendance scanned)    │ ✅ 284/296 │ 12 absent
  9:00 AM │ Online classes start (SSC CGL + IBPS)          │ ✅ Live    │
  10:00 AM│ Maintenance team briefing                      │ ✅ Done    │ 7 open requests
  12:30 PM│ Afternoon batch preparation (room setup)        │ ⏳ Pending │
  1:00 PM │ Faculty attendance confirmation (afternoon)     │ ⏳ Pending │
  2:00 PM │ Afternoon batch starts                         │ ⏳ Scheduled│
  6:00 PM │ Evening batch check-in                         │ 📅 Later   │
  8:00 PM │ Hostel curfew check                            │ 📅 Later   │
  10:00 PM│ Security handover (day → night shift)          │ 📅 Later   │
```

---

## 3. Resource Utilisation

```
RESOURCE UTILISATION — March 2026

  CLASSROOM UTILISATION:
    Room    │ Capacity │ Morning  │ Afternoon│ Evening  │ Avg Util%
    ────────┼──────────┼──────────┼──────────┼──────────┼──────────
    Room 1  │   60     │ SSC CGL  │ IBPS PO  │ Free     │  67%
    Room 2  │   60     │ SSC CHSL │ SSC MTS  │ SSC CGL  │  90%
    Room 3  │   40     │ RRB PO   │ Demo cls │ Free     │  60%
    Room 4  │   40     │ Free     │ Free     │ Free     │   0% ⚠️ AC fault
    Room 5  │   80     │ SSC CGL  │ IBPS Clrk│ SSC CGL  │  95%
    Hall A  │  200     │ Mock test│ Free     │ Seminar  │  45%
    ────────┴──────────┴──────────┴──────────┴──────────┴──────────
    Total:             │ 480 seats│          │           │  76.3%

  HOSTEL ROOM UTILISATION:
    Block A (male):    48/60 rooms  (80%)
    Block B (female):  36/48 rooms  (75%)
    TOTAL:             84/108 rooms  (77.8%)

  EQUIPMENT:
    Projectors:         8/8 functional ✅
    Whiteboards:        12/12 ✅
    CCTV cameras:       24/24 online ✅
    Biometric devices:  6/6 ✅  |  Last sync: 7:58 AM today
    AC units:           11/12 ✅  |  1 fault (Room 4) — technician booked Apr 1
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/operations/dashboard/` | Operations dashboard summary |
| 2 | `GET` | `/api/v1/coaching/{id}/operations/log/?date=2026-03-31` | Daily operations log |
| 3 | `GET` | `/api/v1/coaching/{id}/operations/utilisation/?month=2026-03` | Resource utilisation metrics |
| 4 | `POST` | `/api/v1/coaching/{id}/operations/log/entry/` | Add log entry |
| 5 | `GET` | `/api/v1/coaching/{id}/operations/alerts/` | Open operational alerts |

---

## 5. Business Rules

- The operations dashboard is the Branch Manager's morning briefing tool; the first 15 minutes of every working day should be spent reviewing the dashboard: staff present, classes running, IT status, and open maintenance issues; a Branch Manager who is not monitoring daily operations is not managing — they are reacting; proactive daily monitoring prevents small issues (a broken projector, an absent faculty member) from becoming student-experience failures
- Room 4's AC fault illustrates the threshold for escalation: a comfort issue (warm room) in March (mild weather) is a medium-priority maintenance request; the same fault in May (40°C Hyderabad summer) is an emergency that cancels classes if unresolved; the operations calendar should anticipate seasonal criticality — all AC units must be serviced before April every year; a maintenance checklist that overlooks summer HVAC readiness is a planning failure with predictable consequences
- Daily operations logs are timestamped and immutable once entered; they serve as the official record of what happened on any given day; if a student claims "the projector was broken for 3 days and I missed class", the operations log either confirms or refutes this; the log is also the first reference in any insurance claim or incident investigation; operations staff must complete log entries in real time (not at end of shift from memory); retrospective entries are flagged with a note ("added at 4 PM — event occurred at 2 PM")
- Resource utilisation data drives scheduling decisions; Room 4 being at 0% utilisation (due to AC fault) wastes capacity that the over-full Room 5 (95%) needs; the immediate operational response is to repair AC (booked Apr 1) and consider temporarily moving Room 4 classes to Hall A if repair is delayed; the strategic response is to ensure no single HVAC dependency disables an entire room — TCC's infrastructure SOP requires standby portable AC units for emergency room use; this resilience planning prevents a hardware failure from becoming a student experience crisis
- Operations KPIs (room utilisation target 80–90%, hostel occupancy target 80%, IT uptime target 99.5%) are reviewed monthly by the Branch Manager and annually by the Director; a utilisation rate above 95% consistently signals the need for expansion (new rooms, additional batch times); a rate below 70% signals either over-provisioned capacity or under-enrolled batches; the utilisation data from the dashboard directly feeds the hostel expansion decision (Initiative 2 in L-07) — the 78% hostel occupancy is below the 83% target, driving the Block C expansion decision

---

*Last updated: 2026-03-31 · Group 5 — Coaching Portal · Division M*
