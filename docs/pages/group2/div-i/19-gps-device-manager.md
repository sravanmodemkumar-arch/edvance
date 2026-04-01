# 19 — GPS Device Manager

> **URL:** `/group/transport/gps/devices/`
> **File:** `19-gps-device-manager.md`
> **Template:** `portal_base.html`
> **Priority:** P1
> **Role:** Group Fleet Manager (primary) · Transport Safety Officer · Group IT Admin (Division F)

---

## 1. Purpose

Registry and management of all GPS tracking devices fitted to the group's fleet. Each device record stores the hardware details (IMEI, device model, SIM number), installation details (vehicle, install date, installer), connectivity status, and signal health history.

A GPS device that goes offline means a bus is invisible to the safety monitoring system. Fleet Manager tracks device health proactively, coordinates replacements for faulty devices, and ensures every operational vehicle has a functioning GPS unit.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Fleet Manager | G3 | Full — register, update, replace devices | Primary owner |
| Group Transport Safety Officer | G3 | Read + flag connectivity issues | View + flag only |
| Group IT Admin (Div F) | G4 | Integration config — API key, webhook setup | Tech setup |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Transport Management  ›  GPS Device Manager
```

### 3.2 Page Header
- **Title:** `GPS Device Manager`
- **Subtitle:** `[N] Devices Registered · [N] Online · [N] Offline · [N] Vehicles Without GPS`
- **Right controls:** `+ Register Device` · `Advanced Filters` · `Export`

### 3.3 Alert Banner

| Condition | Banner Text | Severity |
|---|---|---|
| Devices offline > 24 hours | "[N] GPS devices have been offline for > 24 hours." | Red |
| Vehicles with no GPS device | "[N] operational vehicles have no GPS device installed." | Amber |
| SIM card expired | "[N] GPS device SIM cards have expired data plans." | Amber |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule |
|---|---|---|
| Total Devices | Registered | Blue |
| Online Now | Active signal | Green |
| Offline > 1hr | Not transmitting | Red > 0 |
| Vehicles Without GPS | Unequipped operational vehicles | Yellow > 5 |
| Device Coverage % | Vehicles with GPS / Total vehicles | Green ≥ 95% · Red < 90% |
| SIM Renewals Due | Within 30 days | Yellow > 0 |

---

## 5. Main Table — GPS Device Registry

**Search:** Device ID, IMEI, bus number, branch. 300ms debounce.

**Filters:**
| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Status | Radio | All / Online / Offline / Uninstalled |
| Signal Quality | Radio | All / Good / Weak / No Signal |

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| Device ID | ✅ | Internal ID |
| Bus No | ✅ | Installed on · or "Unassigned" |
| Branch | ✅ | |
| IMEI | ✅ | Hardware identifier |
| Device Model | ✅ | Manufacturer/model |
| SIM Number | ✅ | |
| SIM Plan Expiry | ✅ | Colour-coded |
| Install Date | ✅ | |
| Last Signal | ✅ | Time ago — colour: Green < 5min · Red > 30min |
| Signal Quality | ✅ | Good / Weak / No Signal |
| Status | ✅ | Online / Offline / Fault |
| Actions | ❌ | View · Edit · Replace · Uninstall |

**Pagination:** Server-side · 25/page.

---

## 6. Drawers

### 6.1 Drawer: `register-device`
- **Width:** 520px
- **Fields:** Device ID · IMEI · Device Model · Manufacturer · SIM Number · Telecom Provider · SIM Plan Expiry · Installed On (Bus No searchable) · Install Date · Installed By (name) · Notes
- **Validation:** IMEI globally unique

### 6.2 Drawer: `device-detail`
- **Width:** 520px
- **Tabs:** Details · Signal History · Alerts
- **Details:** All device fields, last known location map mini
- **Signal History:** 30-day signal strength chart (line chart — uptime % per day)
- **Alerts:** All offline alerts and resolutions for this device

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Device registered | "GPS device [ID] registered and assigned to [Bus No]." | Success | 4s |
| Registration failed | "Failed to register GPS device. Check for duplicate IMEI." | Error | 5s |
| Device replaced | "GPS device replaced on [Bus No]. New device: [ID]." | Info | 4s |
| Replace failed | "Failed to replace GPS device. Please retry." | Error | 5s |
| SIM renewal reminder | "SIM renewal reminders sent for [N] devices." | Info | 4s |
| Reminder failed | "Failed to send SIM renewal reminders. Please retry." | Error | 5s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No devices registered | "No GPS Devices Registered" | "Register GPS devices for fleet tracking." | [+ Register Device] |
| All devices online | "All GPS Devices Online" | "Full GPS coverage across the fleet." | — |
| No filter results | "No Devices Match Filters" | "Adjust branch, status, or signal quality filters." | [Clear Filters] |
| No search results | "No Devices Found for '[term]'" | "Check the device ID, IMEI, or bus number." | [Clear Search] |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page load | Skeleton: 6 KPI cards + device table |
| Filter/search | Table body skeleton |
| Device detail drawer | 520px skeleton; Signal History chart loads on tab click |

---

## 10. Role-Based UI Visibility

| Element | Fleet Manager G3 | Safety Officer G3 | IT Admin G4 |
|---|---|---|---|
| Register Device | ✅ | ❌ | ✅ (API config) |
| Edit Device | ✅ | ❌ | ✅ |
| Replace Device | ✅ | ❌ | ❌ |
| Flag Offline Issue | ✅ | ✅ | ❌ |
| Configure API Integration | ❌ | ❌ | ✅ |
| Export | ✅ | ✅ | ✅ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/transport/gps/devices/` | JWT (G3+) | Device list |
| POST | `/api/v1/group/{group_id}/transport/gps/devices/` | JWT (G3+) | Register device |
| PATCH | `/api/v1/group/{group_id}/transport/gps/devices/{id}/` | JWT (G3+) | Update device |
| POST | `/api/v1/group/{group_id}/transport/gps/devices/{id}/replace/` | JWT (G3+) | Replace device |
| GET | `/api/v1/group/{group_id}/transport/gps/devices/{id}/signal-history/` | JWT (G3+) | 30-day signal history |
| GET | `/api/v1/group/{group_id}/transport/gps/devices/kpis/` | JWT (G3+) | KPI cards |
| GET | `/api/v1/group/{group_id}/transport/gps/devices/export/` | JWT (G3+) | Async CSV/XLSX export |

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-get/post | hx-target | hx-swap |
|---|---|---|---|---|
| Search | `input delay:300ms` | GET `.../devices/?q={val}` | `#device-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../devices/?{filters}` | `#device-table-section` | `innerHTML` |
| Sort | `click` on header | GET `.../devices/?sort={col}&dir={asc/desc}` | `#device-table-section` | `innerHTML` |
| Pagination | `click` | GET `.../devices/?page={n}` | `#device-table-section` | `innerHTML` |
| Open device detail drawer | `click` on Device ID | GET `.../devices/{id}/` | `#drawer-body` | `innerHTML` |
| Register device submit | `click` | POST `.../devices/` | `#device-table-section` | `innerHTML` |
| Replace device confirm | `click` | POST `.../devices/{id}/replace/` | `#device-row-{id}` | `outerHTML` |
| Export | `click` | GET `.../devices/export/` | `#export-btn` | `outerHTML` |

> **Audit trail:** All write actions (register, replace, update device) are logged to [Transport Audit Log → Page 33] with user, timestamp, and IP.

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
