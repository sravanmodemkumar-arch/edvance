# I-06 — GPS Live Tracking

> **URL:** `/school/transport/gps/`
> **File:** `i-06-gps-live-tracking.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Transport In-Charge (S3) — full dashboard · Administrative Officer (S3) — view · Principal (S6) — view · Parent (via Parent Portal N-09) — own child's bus only

---

## 1. Purpose

Real-time GPS tracking of all school buses. Two audiences with different needs:
- **School dashboard (this page):** Transport In-Charge sees all buses simultaneously on a map; monitors delays, route deviations, SOS alerts
- **Parent view (N-09):** Parent sees only their child's bus — "Bus is 3 km away, estimated 8 minutes" — no access to other buses or student lists

Indian regulatory basis:
- **CBSE Circular 2015:** GPS tracking device mandatory on all school buses
- **Motor Vehicles Act 1988 (amended 2019):** Vehicle Location Tracking (VLT) system mandatory
- **State RTO requirements:** Most states (TG, TS, AP, MH, KA, TN) require AIS-140 compliant GPS devices on school vehicles

---

## 2. School Dashboard — Transport In-Charge View

### 2.1 Map Panel

```
GPS Live Tracking                                    [All Routes]  [Live]  [Alerts: 1]
27 March 2026 — 7:14 AM  ·  Morning pickup in progress

┌─────────────────────────────────────────────────────────────────────────────────┐
│                        [Google Maps / OpenStreetMap embed]                      │
│                                                                                 │
│  🚌 R01 ●  ──── route line (blue) ────── School                                │
│      Chaitanyapuri — ETA 7:22 AM  ·  On time  ·  42 students on board          │
│                                                                                 │
│  🚌 R02 ●  ──── route line (green) ──── School                                 │
│      LB Nagar — ETA 7:28 AM  ·  ⚠️ 6 min delay  ·  35 students                │
│                                                                                 │
│  🚌 R04 ●  ──── route line (orange) ─── School                                 │
│      Vanasthalipuram — ETA 7:35 AM  ·  On time  ·  51 students                 │
│                                                                                 │
│  🔧 R03 ─ In maintenance (no GPS data expected)                                 │
│  ✅ R05 ─ Reached school 7:08 AM  ✅                                            │
│                                                                                 │
│  [Satellite]  [Road]  [Zoom in/out]  [Fit all buses]                            │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Fleet Status Panel (right sidebar)

```
Fleet Status — 7:14 AM

Route  Bus           Driver         Last Ping    Speed   Status
R01    AP29AB1234    Raju Kumar     7:13:52 AM   28 km/h  ✅ On route
R02    AP29CD5678    Suresh M.      7:13:47 AM   0 km/h   ⚠️ Stopped (traffic signal?)
R04    AP29IJ7890    Kishore R.     7:14:01 AM   35 km/h  ✅ On route
R05    AP29KL1234    Prakash D.     7:08:14 AM   0 km/h   ✅ At school
R03    AP29GH3456    —              N/A          N/A      🔧 Maintenance

⚠️ Alert: R02 has been stopped for 8 minutes (may be traffic/breakdown)
  [Mark as Traffic]  [Call Driver]  [Send Substitute Bus]
```

### 2.3 Active Alerts Panel

```
Active Alerts — 27 Mar 2026

⚠️ 7:06 AM — Route R02 — Bus stopped for 8+ min at LB Nagar bypass
   Driver: Suresh M. — [Call +91 9876-XXXXX]
   Action taken: [Log as traffic delay]  [Dispatch assistance]

──────────────────────────────────────────────────────
Resolved today:
  ✅ 6:52 AM — R01 — 2-min wait for student Arjun S. at stop — logged
```

---

## 3. Bus Detail View (click on bus icon)

```
Route R01 — AP29AB1234 — Live Detail
7:14 AM — Approaching Kothapet Bus Stop

Current position: 500m south of Kothapet Bus Stop
Speed: 28 km/h  ·  Heading: North-East
Driver: Raju Kumar  ·  Escort: Ms. Kavitha

Route progress:
  ✅ Stop 1 — Paradise Circle (6:45 AM)         8 students boarded
  ✅ Stop 2 — Chaitanyapuri X-Roads (6:50 AM)  12 students boarded
  ▶ Stop 3 — Kothapet Bus Stop                 (approaching — ETA 7:15 AM)
  ○ Stop 4 — Dilsukhnagar X-Roads              7:20 AM (projected)
  ○ Stop 5 — Meerpet Colony                    7:25 AM (projected)
  ○ School Gate                                7:35 AM (projected) — 13 min late

Students on board: 20 confirmed (via I-05 attendance)

Speed history (last 30 min):
  6:45–7:05: 25–32 km/h ✅ (within 40 km/h limit)
  7:05–7:08: 0 km/h (stopped at signal — 3 min)
  7:08–now:  28–35 km/h ✅

⚠️ Route deviation check: ✅ On authorised route (no deviation detected)

[Call Driver]  [Call Escort]  [Alert Principal]  [View Route on Map]
```

---

## 4. Speed Violation Alert

```
⚠️ SPEED ALERT — 15 March 2026 (historical example)

Route R04 — AP29IJ7890 — Driver: Kishore R.
Time: 3:45 PM (Evening drop)
Location: NH163 — Vanasthalipuram bypass
Speed recorded: 52 km/h
Limit: 40 km/h (CBSE/RTO school bus maximum)
Duration: 2 min 14 sec (sustained over-speeding)

Automatic actions taken:
  ✅ Alert sent to Transport In-Charge (7:45 PM)
  ✅ Alert sent to Principal (7:45 PM)
  ✅ Logged in driver's incident history (I-04)
  ✅ Parent notification suppressed (this is an internal compliance matter)

Required action:
  Transport In-Charge: [Issue written warning to driver]
  Principal: [Review and sign off]
  HR record: [Add to I-04 driver profile]

3rd speeding violation in 12 months → mandatory disciplinary committee review
```

---

## 5. SOS Alert (Emergency Button on Bus)

```
🚨 SOS ALERT — EMERGENCY

Route R01 — AP29AB1234
Time: 7:18 AM — 27 March 2026
Location: Kothapet flyover (GPS: 17.3789°N, 78.5678°E)
Driver: Raju Kumar (pressed SOS button on GPS device)

Type (auto-classified as unknown until confirmed):
  ○ Accident  ● Unknown emergency  ○ Medical emergency  ○ Breakdown

Automatic escalation (within 30 seconds of SOS):
  ✅ Transport In-Charge notified (push + call)
  ✅ Principal notified (push + SMS)
  ✅ Administrative Officer notified

Required immediate actions:
  1. [Call Driver — +91 9876-XXXXX]   (try every 30 sec if no answer)
  2. [Call Escort — +91 8765-XXXXX]
  3. [Dispatch nearest school vehicle to location]
  4. [Alert parents of students on R01]  ← requires Principal approval before send
  5. [Call Police 100]  ← one tap
  6. [Call Ambulance 108]  ← one tap

Do NOT mark as resolved until:
  □ All students accounted for
  □ Written incident report filed (I-08)
  □ Principal has reviewed

[Mark as Resolved + Open I-08 Incident Report]
```

---

## 6. Parent View (N-09 integration — read-only child's bus)

```
[Parent portal view — different from school dashboard]

My child's bus — Arjun Sharma (XI-A)
Route R01 — Chaitanyapuri → School

[Mini map showing only R01 route and current bus position]

🚌 Bus is currently near: Kothapet Bus Stop
Estimated arrival at school: 7:35 AM
On-time status: ⚠️ 13 minutes late today (traffic near Kothapet flyover)

Your child's stop (Pick-up): Kothapet Bus Stop
Bus will reach your stop at approximately: 7:15 AM

Driver contact: [Call Bus — connects via school switchboard]
                (parent does not receive driver's personal number)

Last updated: 7:14 AM  ·  [Refresh]

Note: Location data is updated every 30 seconds. Minor delays (±2 min) are normal.
```

---

## 7. GPS Device Health Dashboard

```
GPS Device Health — Transport In-Charge View

Device        Bus           Last Ping      Battery  Signal  Status
GPS-BUS-001   AP29AB1234    7:14:01 AM     N/A      Good    ✅ Active
GPS-BUS-002   AP29CD5678    7:13:47 AM     N/A      Good    ✅ Active
GPS-BUS-004   AP29IJ7890    7:14:01 AM     N/A      Fair    ✅ Active
GPS-BUS-005   AP29KL1234    7:08:14 AM     N/A      Good    ✅ Active
GPS-BUS-003   AP29GH3456    N/A            N/A      None    🔧 Offline (maintenance)

AIS-140 compliance: 4/5 active devices reporting ✅
VLTD portal sync (MoRTH): Last sync 6:00 AM today ✅

⚠️ If a GPS device goes offline during a running route:
  → Transport In-Charge is immediately alerted
  → Driver is called to confirm position
  → Parents are sent a message: "Live tracking temporarily unavailable for Route R02.
     We are in contact with the driver. Bus is running on schedule."
```

---

## 8. Historical Tracking (Playback)

```
Route Playback — Route R01 — 26 March 2026 — Morning

[Timeline slider: 6:40 AM ────────────────── 7:25 AM]
[Play] [Pause] [▶▶ 2x speed]

Playback shows:
  6:44 AM — Bus departed Paradise Circle (2 min early)
  6:51 AM — Stop 2 Chaitanyapuri X-Roads (1 min late)
  7:02 AM — Bus stopped for 3 min 41 sec (signal/traffic at Kothapet junction)
  7:22 AM — Arrived school gate

Total route time: 38 min  ·  Expected: 45 min  ·  5 min early arrival

Speed analysis:
  Average speed: 24 km/h
  Maximum speed: 38 km/h (within limit)
  Over-speed incidents: 0

[Export playback as PDF report]  [Save as evidence for I-08]
```

---

## 9. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/transport/gps/live/` | All buses live positions |
| 2 | `GET` | `/api/v1/school/{id}/transport/gps/live/{route_id}/` | Single route live position |
| 3 | `GET` | `/api/v1/school/{id}/transport/gps/parent/{student_id}/` | Parent view — own child's bus |
| 4 | `POST` | `/api/v1/school/{id}/transport/gps/alert/` | Inbound alert from GPS device (SOS, speeding) |
| 5 | `GET` | `/api/v1/school/{id}/transport/gps/history/?route={id}&date={date}` | Route playback data |
| 6 | `GET` | `/api/v1/school/{id}/transport/gps/speed-violations/?month={m}` | Speed violation log |
| 7 | `GET` | `/api/v1/school/{id}/transport/gps/device-health/` | GPS device status |
| 8 | `POST` | `/api/v1/school/{id}/transport/gps/sos-resolve/{alert_id}/` | Mark SOS resolved + open I-08 |

---

## 10. Business Rules

- GPS data is received from AIS-140 compliant VLT devices; EduForge accepts raw NMEA/API push from major Indian GPS vendors (Rosmerta, Intellicar, Uffizio, TrackoBit); school configures their vendor's API credentials in admin
- Parent view shows bus location only — no student list, no other routes, no driver personal contact (DPDPA: minimum disclosure principle)
- SOS alert escalates automatically without any human approval step — speed is critical; Principal is informed simultaneously with Transport In-Charge
- Speed violations above 40 km/h are logged automatically; driver is not notified in real time (to prevent distraction); the written notice is given after the route ends
- GPS data is retained for 90 days for routine operations; accident/incident data is retained indefinitely once linked to an I-08 record
- A GPS device offline during a route does not stop the bus operation but triggers an alert chain; the school must have a manual check-in protocol (escort calls school every 15 min) as backup
- Route deviation detection: if bus position is >500m from authorised route for >2 minutes, an alert is triggered; legitimate deviations (road block, emergency hospital) must be logged post-route
- Privacy: live GPS feed is accessible only to authorised school staff and the parent of a student on that bus; GPS feed is never public or shareable

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division I*
