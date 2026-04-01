# N-06 — Bus Tracking (Parent View)

> **URL:** `/parent/transport/`
> **File:** `n-06-transport-tracking.md`
> **Template:** `parent_portal.html`
> **Priority:** P1
> **Roles:** Parent/Guardian (S1-P) — only for children enrolled in school transport

---

## 1. Purpose

Parents with children on school buses get a live view of their child's bus — location, estimated time of arrival, and safety notifications. This is a privacy-controlled view derived from I-06 (GPS Live Tracking) — parents see only their own child's bus, not the school's full fleet view.

DPDPA principle: Minimum disclosure — parents see their bus route status and ETA; they cannot see other students' names, boarding points, or personal details on the bus.

---

## 2. Live Bus View — Morning (School-Bound)

```
BUS TRACKING — Rahul Rao (Class X-A)
Route 3 — Dilsukhnagar → Greenfields School
Driver: Mr. Shankar R. (DRV-007)  |  Escort: Ms. Fatima N. (ESC-003)

LIVE STATUS — 27 March 2026, 7:38 AM:
  ┌─────────────────────────────────────────────────────────────┐
  │                                                             │
  │   🚌  Bus is 2.4 km away — ETA: 7:43 AM (5 minutes)       │
  │       [MAP — bus icon moving on route, approaching stop]    │
  │                                                             │
  │   Rahul's stop: Dilsukhnagar Main Road (Stop 4)            │
  │   Scheduled pick-up: 7:42 AM                               │
  │   Current status: ON TIME ✅                               │
  │                                                             │
  └─────────────────────────────────────────────────────────────┘

  [Notify me when bus is 10 min away] ← currently active ✅

BUS STATUS TODAY:
  Departed depot: 6:55 AM ✅
  Stops completed: 1, 2, 3 (of 14 stops on route)
  Students on board: 18 (cannot see names — privacy)
  Next stop: Stop 4 (Rahul's stop)

DRIVER AND ESCORT:
  Driver: Mr. Shankar R. — BGV verified ✅ | Licence: Valid
  Escort: Ms. Fatima N. — BGV verified ✅
  [Contact school for urgent matters: +91-40-XXXX-XXXX]
  Note: Parent cannot directly call driver/escort (school policy — safety protocol)
```

---

## 3. Afternoon Return View

```
AFTERNOON RETURN — 27 March 2026

School dismissal: 3:15 PM
Route 3 departs school: 3:30 PM (after all students board + escort confirms)

  [After 3:30 PM — live view activates]

  4:02 PM:
  ┌─────────────────────────────────────────────────────────────┐
  │   🚌  Bus is 6.1 km from your stop — ETA: 4:18 PM         │
  │                                                             │
  │   Rahul boarded bus at school: ✅ 3:28 PM (escort confirmed)│
  │   [Map — bus moving towards Dilsukhnagar]                   │
  └─────────────────────────────────────────────────────────────┘

  4:19 PM — NOTIFICATION sent:
  "🚌 Rahul's bus approaching Dilsukhnagar Main Road — ETA 4:22 PM."

  4:24 PM — NOTIFICATION sent:
  "✅ Rahul dropped at Dilsukhnagar Main Road stop. Route 3 proceeding."
```

---

## 4. Delay and Safety Alerts

```
BUS ALERTS — Parent Notifications (last 7 days)

  26 Mar  🟡 Bus delayed — Route 3 running 12 min late (traffic — Dilsukhnagar flyover)
             Resolved: 7:54 AM arrival (vs 7:42 AM scheduled)
  22 Mar  ✅ Normal operations
  21 Mar  🟡 Bus delayed 8 minutes (route diversion — road work LB Nagar)
             Resolved: 7:50 AM arrival

SAFETY ALERT (example — not current):
  If SOS is triggered on bus:
  🔴 EMERGENCY ALERT: Route 3 SOS activated at [location].
     School management has been notified. Do NOT contact the driver.
     For updates, contact school: +91-40-XXXX-XXXX
     [This alert cannot be dismissed until school resolves and clears it]
```

---

## 5. Transport Enrolment Details

```
TRANSPORT DETAILS — Rahul Rao

Route:          Route 3 — Dilsukhnagar Loop
Pick-up stop:   Dilsukhnagar Main Road (Stop 4)
Pick-up time:   7:42 AM (approx — varies ±5 min)
Drop-off time:  4:20 PM (approx — varies by traffic)
Bus Number:     TS-09-EA-1234
Bus capacity:   45 seats | Current route load: 38 students

TERM TRANSPORT FEE:
  Term 3: ₹2,400 — PAID ✅ (included in fee payment)

NOTIFY IF NOT BOARDING (parent can report):
  If Rahul will not take the bus today (e.g., parent pick-up):
  [Report child not taking bus today →] ← logs in I-02 attendance; escort aware
```

---

## 6. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/parent/{parent_id}/child/{student_id}/transport/status/` | Live bus position and ETA |
| 2 | `GET` | `/api/v1/parent/{parent_id}/child/{student_id}/transport/details/` | Route and stop details |
| 3 | `GET` | `/api/v1/parent/{parent_id}/child/{student_id}/transport/alerts/` | Recent transport alerts |
| 4 | `POST` | `/api/v1/parent/{parent_id}/child/{student_id}/transport/not-boarding/` | Report child not using bus today |

---

## 7. Business Rules

- Parent can see only their child's bus location and ETA — they cannot see the full fleet, other routes, or other students on the bus (DPDPA minimum disclosure)
- The parent cannot see the driver's or escort's personal phone number; all communication must go through the school office; this protects the driver and escort from direct parent harassment or pressure (common problem in Indian school contexts)
- The "child boarded bus at school" confirmation is sent after the escort manually confirms all students are aboard (not automatic from GPS); this is an important distinction — GPS tells you the bus is at school, but only the escort's explicit confirmation tells you the child is on the bus
- If a parent reports "child not boarding today" before 7:30 AM, the system updates the escort's manifest so they don't wait at the stop; this also ensures the bus doesn't linger unnecessarily
- Transport tracking data (GPS coordinates) is retained for 90 days (K-04 and I-06 rules); parent-visible history is limited to 7 days to avoid the portal becoming a surveillance tool

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division N*
