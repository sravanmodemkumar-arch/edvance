# 07 — Vehicle Register

> **URL:** `/group/transport/vehicles/`
> **File:** `07-vehicle-register.md`
> **Template:** `portal_base.html`
> **Priority:** P0
> **Role:** Group Fleet Manager (primary) · Transport Director · Transport Safety Officer (view)

---

## 1. Purpose

Master vehicle register for all buses and transport vehicles across every branch. Each row represents a single vehicle — its identity (RC, chassis, engine), assignment (branch, route), compliance status (fitness cert, permit, insurance), operational status, GPS device, and maintenance history linkage.

This is the authoritative source of truth for all vehicles in the group. Every compliance check, maintenance record, and safety inspection is linked back to a vehicle record here. Scale: 200–500 vehicles across 20–50 branches.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Fleet Manager | G3 | Full — create, edit, decommission | Primary owner |
| Group Transport Director | G3 | Full — approve decommission, view all | Can create in emergency |
| Group Transport Safety Officer | G3 | Read + flag safety concern | Cannot edit profile |
| Group Route Planning Manager | G3 | Read — for route assignment | Cannot edit |
| Branch Transport In-Charge | Branch G3 | Read own branch | Cannot edit group data |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Transport Management  ›  Vehicle Register
```

### 3.2 Page Header
- **Title:** `Group Vehicle Register`
- **Subtitle:** `[N] Active Vehicles · [N] Under Maintenance · [N] Decommissioned · AY [current]`
- **Right controls:** `+ Add Vehicle` · `Bulk Import ↑` · `Advanced Filters` · `Export`

### 3.3 Alert Banner

| Condition | Banner Text | Severity |
|---|---|---|
| Vehicles with expired fitness cert | "[N] vehicles have expired fitness certificates." | Red |
| Vehicles with expired insurance | "[N] vehicles have expired insurance." | Red |
| Vehicles without GPS device | "[N] vehicles have no GPS device assigned." | Amber |
| Vehicles > 15 years old | "[N] vehicles are older than 15 years — statutory decommission review required." | Amber |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule |
|---|---|---|
| Total Vehicles | All registered | Blue |
| Active / Operational | Available for deployment | Blue |
| Under Maintenance | In workshop today | Yellow > 0 |
| Fitness Non-Compliant | Expired or missing | Red > 0 · Green = 0 |
| Insurance Non-Compliant | Expired or missing | Red > 0 · Green = 0 |
| Avg Age (years) | Fleet average | Green < 8 · Yellow 8–12 · Red > 12 |

---

## 5. Main Table — Vehicle Register

**Search:** Bus number, RC number, chassis number, branch. 300ms debounce.

**Advanced Filters:**
| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Status | Checkbox | Active / Under Maintenance / Breakdown / Decommissioned |
| Vehicle Type | Checkbox | Full Bus / Mini Bus / Van / Electric Bus |
| Fuel Type | Checkbox | Diesel / CNG / Electric |
| Compliance | Radio | All / Fully Compliant / Fitness Issue / Insurance Issue / Permit Issue |
| GPS Status | Radio | All / GPS Fitted / GPS Missing |
| Age | Radio | All / < 5yr / 5–10yr / > 10yr |
| Route Assignment | Checkbox | Assigned / Unassigned |

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| Bus No | ✅ | Link → vehicle detail drawer |
| Branch | ✅ | |
| Type | ✅ | Bus / Mini Bus / Van |
| Capacity | ✅ | Seats |
| Year | ✅ | Manufacturing year |
| RC Number | ✅ | Registration certificate |
| Fitness Cert | ✅ | ✅ Valid · ⚠ Expiring · 🔴 Expired — with date |
| Insurance | ✅ | ✅ Valid · ⚠ Expiring · 🔴 Expired — with date |
| Permit | ✅ | ✅ Valid · ⚠ Expiring · 🔴 Expired — with date |
| GPS Device | ✅ | Device ID or ❌ Not fitted |
| Route Assigned | ✅ | Route name or — |
| Status | ✅ | Active / Maintenance / Breakdown / Decommissioned |
| Actions | ❌ | View · Edit · Maintenance · Flag |

**Bulk actions:** Export selected · Bulk update branch assignment · Bulk flag for inspection.
**Pagination:** Server-side · 25/page · 10/25/50/All.

---

## 6. Drawers

### 6.1 Drawer: `vehicle-detail` — View Vehicle
- **Trigger:** Bus No link or Actions → View
- **Width:** 680px
- **Tabs:** Profile · Compliance · Maintenance · GPS · Incidents · History
- **Profile:** Bus No, type, capacity, RC, chassis, engine, fuel type, manufacturer, model, year, purchased/leased, purchase date, branch, current route
- **Compliance:** Fitness cert (date, expiry, renewal history), route permit (authority, number, expiry), insurance (policy no, insurer, expiry, premium), RC book (expiry)
- **Maintenance:** Last 10 service records — date, type (scheduled/breakdown), workshop, cost, mileage
- **GPS:** Device ID, IMEI, install date, last signal, coverage % last 30 days
- **Incidents:** All accidents/incidents linked to this vehicle
- **History:** Status changes, branch transfers, decommission events with timestamps

### 6.2 Drawer: `vehicle-create` — Add Vehicle
- **Trigger:** + Add Vehicle
- **Width:** 640px
- **Tabs:** Identity · Compliance Documents · Assignment
- **Identity:** Bus No · Vehicle Type · Manufacturer · Model · Year · Seating Capacity · Fuel Type · RC Number · Chassis Number · Engine Number · Purchased / Leased · Purchase/Lease Date
- **Compliance:** Fitness Cert (issue date, expiry) · Route Permit (authority, number, expiry) · Insurance (policy no, insurer, start, expiry) · Upload documents (PDF)
- **Assignment:** Branch · GPS Device ID (optional) · Route (optional)
- **Validation:** RC number globally unique · Bus number unique per group

### 6.3 Drawer: `vehicle-edit`
- **Trigger:** Actions → Edit
- **Width:** 640px (same tabs as create, pre-populated)
- **Read-only after save:** RC Number, Chassis Number, Engine Number — change requires Director approval

> **Audit trail:** All write actions (add vehicle, edit vehicle, renew compliance, decommission) are logged to [Transport Audit Log → Page 33] with user, timestamp, and IP.

### 6.4 Modal: `vehicle-decommission`
- **Trigger:** Actions → Flag → Decommission
- **Width:** 480px
- **Fields:** Decommission Date · Reason (Age / Beyond Repair / Regulatory / Sold / Scrapped) · Odometer Reading · Final Status Notes
- **Warning:** "Decommissioned vehicles cannot be assigned to routes. All active route assignments will be removed."
- **Requires Director approval** before status change finalises

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Vehicle added | "[Bus No] added to vehicle register." | Success | 4s |
| Vehicle add failed | "Failed to add vehicle. Check for duplicate RC number or bus number." | Error | 5s |
| Vehicle updated | "[Bus No] details updated." | Success | 4s |
| Vehicle update failed | "Failed to update vehicle. Please retry." | Error | 5s |
| Compliance renewed | "Fitness certificate renewed for [Bus No]. Expiry: [date]." | Success | 4s |
| Compliance renewal failed | "Failed to update compliance record. Please retry." | Error | 5s |
| Vehicle decommissioned | "[Bus No] decommissioned on [date]. Record archived." | Info | 5s |
| Decommission failed | "Decommission failed. Director approval may be required." | Error | 5s |
| Bulk export | "Vehicle register export prepared. You'll be notified when ready." | Info | 4s |
| Export failed | "Export failed. Please try again." | Error | 5s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No vehicles | "No Vehicles Registered" | "Add vehicles to build the fleet register." | [+ Add Vehicle] |
| No filter results | "No Vehicles Match Filters" | "Adjust branch, status, or compliance filters." | [Clear Filters] |
| No search results | "No Vehicles Found for '[term]'" | "Check the bus number, RC number, or branch name." | [Clear Search] |
| No compliance issues | "All Vehicles Compliant" | "All vehicles have valid fitness, insurance, and permits." | — |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page load | Skeleton: 6 KPI cards + table skeleton (15 rows × 13 columns) |
| Filter/search | Table body skeleton |
| Vehicle detail drawer | 680px drawer skeleton; tabs load lazily |
| Document upload | Progress bar on file upload |

---

## 10. Role-Based UI Visibility

| Element | Fleet Manager G3 | Transport Director G3 | Safety Officer G3 | Route Planning Mgr G3 |
|---|---|---|---|---|
| Add Vehicle | ✅ | ✅ | ❌ | ❌ |
| Edit Vehicle | ✅ | ❌ | ❌ | ❌ |
| Decommission | ✅ (propose) | ✅ (approve) | ❌ | ❌ |
| View All Vehicles | ✅ | ✅ | ✅ | ✅ |
| Upload Documents | ✅ | ❌ | ❌ | ❌ |
| Export | ✅ | ✅ | ✅ | ✅ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/transport/vehicles/` | JWT (G3+) | Paginated, filtered vehicle list |
| GET | `/api/v1/group/{group_id}/transport/vehicles/{id}/` | JWT (G3+) | Vehicle full profile |
| POST | `/api/v1/group/{group_id}/transport/vehicles/` | JWT (G3+) | Create vehicle |
| PATCH | `/api/v1/group/{group_id}/transport/vehicles/{id}/` | JWT (G3+) | Update vehicle |
| POST | `/api/v1/group/{group_id}/transport/vehicles/{id}/decommission/` | JWT (G3+ + Director) | Decommission |
| GET | `/api/v1/group/{group_id}/transport/vehicles/kpis/` | JWT (G3+) | KPI card values |
| GET | `/api/v1/group/{group_id}/transport/vehicles/export/` | JWT (G3+) | Async CSV/XLSX export |
| POST | `/api/v1/group/{group_id}/transport/vehicles/bulk-import/` | JWT (G3+) | Bulk import via CSV |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-get/post | hx-target | hx-swap |
|---|---|---|---|---|
| Search | `input delay:300ms` | GET `.../vehicles/?q={val}` | `#vehicle-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../vehicles/?{filters}` | `#vehicle-table-section` | `innerHTML` |
| Pagination | `click` | GET `.../vehicles/?page={n}` | `#vehicle-table-section` | `innerHTML` |
| Sort | `click` on header | GET `.../vehicles/?sort={col}&dir={asc/desc}` | `#vehicle-table-section` | `innerHTML` |
| Open view drawer | `click` on Bus No | GET `.../vehicles/{id}/` | `#drawer-body` | `innerHTML` |
| Sort | `click` on header | GET `.../vehicles/?sort={col}&dir={asc/desc}` | `#vehicle-table-section` | `innerHTML` |
| Pagination | `click` | GET `.../vehicles/?page={n}` | `#vehicle-table-section` | `innerHTML` |
| Submit create | `click` | POST `.../vehicles/` | `#vehicle-table-section` | `innerHTML` |
| Decommission confirm | `click` | POST `.../vehicles/{id}/decommission/` | `#vehicle-row-{id}` | `outerHTML` |
| Export | `click` | GET `.../vehicles/export/` | `#export-btn` | `outerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
