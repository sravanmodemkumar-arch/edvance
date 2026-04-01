# 18 — GPS Live Tracking

> **URL:** `/group/transport/gps/live/`
> **File:** `18-gps-live-tracking.md`
> **Template:** `portal_base.html` (full-width map layout)
> **Priority:** P0
> **Role:** Group Transport Safety Officer (primary) · Transport Director · Fleet Manager

---

## 1. Purpose

Real-time GPS tracking map showing the live location of every bus in the group's fleet during school operational hours. Safety Officers monitor all buses simultaneously, identify delays, track geo-fence violations, respond to SOS alerts, and verify buses arrived at school and departed on schedule.

This is the highest-urgency page in Division I. Any parent wondering where their child's bus is, any driver who hasn't checked in — this page answers those questions in real time.

Tech stack: GPS devices on buses transmit coordinates every 30 seconds via SIM-based telematics. EduForge receives a webhook or polling feed and renders positions on Leaflet.js. Map data = OpenStreetMap tiles.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Transport Safety Officer | G3 | Full — view all buses, respond to alerts | Primary user |
| Group Transport Director | G3 | View — all buses | Oversight |
| Group Fleet Manager | G3 | View — for fleet health context | Read only |
| Branch Transport In-Charge | Branch G3 | View own branch buses only | Scoped |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Transport Management  ›  GPS Live Tracking
```

### 3.2 Page Header (compact bar above full-width map)
```
GPS Live Tracking  ·  [N] Online  ·  [N] Offline  ·  [N] Alerts  ·  Last refresh: [time]
[Branch Filter ▾]  [Route Filter ▾]  [Status Filter ▾]  [↺ Refresh]
```

### 3.3 Alert Banner

| Condition | Banner Text | Severity |
|---|---|---|
| SOS button pressed on any bus | "🚨 SOS ALERT: Bus [No] on Route [Name]. Driver pressed SOS. Call branch immediately." | Critical Red |
| Bus offline > 20 min during school hours | "[N] buses have lost GPS signal for > 20 minutes." | Red |
| Geo-fence breach | "Bus [No] has exited its approved route corridor." | Red |
| Bus delayed > 15 min | "[N] buses are delayed > 15 minutes at next stop." | Amber |

---

## 4. Status Bar (above map)

| Metric | Display |
|---|---|
| Online Buses | Count (green badge) |
| Offline Buses | Count (red badge) |
| Delayed Buses | Count (yellow badge) |
| Active SOS Alerts | Count (flashing red) |
| On Route / Arrived at School / Returning | Status breakdown |

---

## 5. Main Map

### 5.1 Map Configuration
- **Library:** Leaflet.js
- **Tiles:** OpenStreetMap (free tier)
- **Bounds:** Auto-fit to show all active buses on load; user can zoom/pan
- **Auto-refresh:** Every 30 seconds via HTMX partial update of bus marker positions

### 5.2 Bus Markers

| Colour | Meaning |
|---|---|
| 🟢 Green | On route, on time, GPS live |
| 🟡 Yellow | Delayed > 10 min |
| 🔴 Red | GPS offline or geo-fence breach |
| 🚨 Flashing Red | SOS alert — immediate attention |
| ⚫ Grey | Bus not currently on duty |

Each marker tooltip (hover):
```
Bus [No]  |  Route: [Name]  |  Driver: [Name]
Speed: [N] km/h  |  Last Stop: [Name]  |  Next Stop: [Name]  |  ETA: [HH:MM]
Status: [On Route / Delayed / Offline]
[Track This Bus]  [Contact Driver]  [Report Incident]
```

### 5.3 Right Sidebar (Bus List)

Scrollable list of all buses with status indicator. Clicking a bus in the list pans the map to that bus and shows the detail tooltip.

| Column | Notes |
|---|---|
| Bus No | |
| Route | |
| Driver | |
| Status | Colour badge |
| Last Signal | Time ago |
| ETA Next Stop | |

Search in sidebar: bus number, route, driver name.

---

## 6. Track Single Bus View

> Clicking "Track This Bus" on any bus marker opens a full detail panel.

- **Panel Width:** 380px (right side overlay)
- **Content:**
  - Bus No, Route, Driver, Conductor
  - Live location (coords)
  - Current speed
  - Last 10 stops visited with actual arrival vs scheduled arrival
  - On-time performance for today
  - GPS signal strength
  - [Report Incident →] · [Contact Driver →] · [Escalate →]

---

## 7. Route Playback (Historical)

> Replay any bus's route for a past date.

- Date selector + Bus selector
- Play/Pause/Speed control (1x / 2x / 5x)
- Timeline scrubber
- Stop-by-stop time comparison
- Available for last 90 days of GPS data

---

## 8. Offline/Alert Response Actions

### 8.1 Bus Offline Alert
- Duration offline shown
- "Send Alert to Branch" → POST to branch transport in-charge
- "Mark as Known Offline (Maintenance)" → Suppresses alert

### 8.2 SOS Alert Response
- Immediate full-screen alert modal with bus details, last known location, driver phone
- Log response: Response actions taken (free text), resolution status
- Auto-escalates to Transport Director and COO if not acknowledged within 5 minutes

---

## 9. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| SOS acknowledged | "SOS for Bus [No] acknowledged. Emergency response initiated." | Warning | 10s |
| SOS acknowledgement failed | "Failed to acknowledge SOS alert. Please retry immediately." | Error | 6s |
| Offline alert sent | "Offline alert sent to Branch [Name] for Bus [No]." | Info | 4s |
| Offline alert failed | "Failed to send offline alert. Check branch notification settings." | Error | 5s |
| Geo-fence breach acknowledged | "Geo-fence breach acknowledged. Bus [No] back on route." | Info | 4s |
| Acknowledgement failed | "Failed to acknowledge alert. Please retry." | Error | 5s |

---

## 10. Empty States

| Condition | Heading | Description | Notes |
|---|---|---|---|
| No buses active | "No Buses Currently On Route" | "Transport hours have not started or no buses are assigned today." | Outside operational hours |
| All GPS offline | "GPS Feed Unavailable" | "Unable to receive GPS data. Check GPS device connectivity in Page 19." | System-level GPS issue |

---

## 11. Loader States

| Trigger | Loader Type |
|---|---|
| Page load | Map tile loading + bus marker loading spinner |
| Bus list refresh | Sidebar skeleton |
| Auto-refresh | Marker positions update smoothly; no full reload |

---

## 12. Role-Based UI Visibility

| Element | Safety Officer G3 | Transport Director G3 | Fleet Manager G3 |
|---|---|---|---|
| View All Branches | ✅ | ✅ | ✅ |
| Filter to Own Branch | — | — | ✅ (default to all) |
| SOS Response | ✅ | ✅ | ❌ |
| Report Incident | ✅ | ✅ | ❌ |
| Route Playback | ✅ | ✅ | ✅ |
| Contact Driver | ✅ | ✅ | ✅ |

---

## 13. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/transport/gps/live/` | JWT (G3+) | All bus live positions |
| GET | `/api/v1/group/{group_id}/transport/gps/bus/{bus_id}/live/` | JWT (G3+) | Single bus live detail |
| GET | `/api/v1/group/{group_id}/transport/gps/bus/{bus_id}/history/` | JWT (G3+) | Historical route playback |
| GET | `/api/v1/group/{group_id}/transport/gps/alerts/` | JWT (G3+) | Active GPS alerts |
| POST | `/api/v1/group/{group_id}/transport/gps/alerts/{id}/acknowledge/` | JWT (G3+) | Acknowledge alert |
| POST | `/api/v1/group/{group_id}/transport/gps/alerts/{id}/resolve/` | JWT (G3+) | Resolve alert |

---

## 14. HTMX Patterns

| Interaction | hx-trigger | hx-get/post | hx-target | hx-swap |
|---|---|---|---|---|
| Bus positions auto-refresh | `every 30s` | GET `.../gps/live/` | `#bus-markers-data` | `innerHTML` (triggers JS map update) |
| Alert badge refresh | `every 30s` | GET `.../gps/alerts/?active=true` | `#alert-count-badge` | `innerHTML` |
| Bus sidebar filter | `input delay:300ms` | GET `.../gps/live/?q={val}` | `#bus-sidebar-list` | `innerHTML` |
| Status filter (online/offline/alerts) | `click` | GET `.../gps/live/?status={val}` | `#bus-sidebar-list` | `innerHTML` |
| Acknowledge SOS | `click` | POST `.../gps/alerts/{id}/acknowledge/` | `#sos-modal` | `outerHTML` |
| Resolve alert | `click` | POST `.../gps/alerts/{id}/resolve/` | `#alert-row-{id}` | `outerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
