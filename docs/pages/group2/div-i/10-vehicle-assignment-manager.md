# 10 — Vehicle Assignment Manager

> **URL:** `/group/transport/vehicles/assignments/`
> **File:** `10-vehicle-assignment-manager.md`
> **Template:** `portal_base.html`
> **Priority:** P1
> **Role:** Group Fleet Manager (primary) · Route Planning Manager · Transport Director

---

## 1. Purpose

Manages the assignment of vehicles to routes and branches across the group. Each route must have exactly one vehicle assigned. This page gives the Fleet Manager visibility into which buses are assigned where, which are unassigned (spare pool), and how to reassign when a vehicle goes into maintenance or breaks down.

Key use cases:
- Assign a spare bus to a route when the primary breaks down (emergency swap)
- Reassign vehicles when a route is restructured
- Track spare vehicle pool per branch
- Ensure no route operates without a vehicle

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Fleet Manager | G3 | Full — assign, reassign, release | Primary owner |
| Group Route Planning Manager | G3 | Read + request assignment | Cannot directly assign |
| Group Transport Director | G3 | View + approve emergency reassignment | Oversight |
| Group Transport Safety Officer | G3 | Read — verify compliant vehicle assigned | View only |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Transport Management  ›  Vehicle Assignment Manager
```

### 3.2 Page Header
- **Title:** `Vehicle Assignment Manager`
- **Subtitle:** `[N] Routes · [N] Assigned · [N] Unassigned Routes · [N] Spare Vehicles`
- **Right controls:** `+ Assign Vehicle` · `Emergency Swap` · `Export`

### 3.3 Alert Banner

| Condition | Banner Text | Severity |
|---|---|---|
| Routes with no vehicle | "[N] active routes have no vehicle assigned. Students cannot be transported." | Red |
| Non-compliant vehicle assigned | "[N] routes have a non-compliant vehicle assigned (expired fitness/insurance)." | Red |
| Route assignment gaps for tomorrow | "[N] routes have vehicle going into maintenance tomorrow — reassignment needed." | Amber |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule |
|---|---|---|
| Total Routes | All active routes | Blue |
| Routes with Vehicle | Assigned | Green if = total · Red if < total |
| Unassigned Routes | Need vehicle | Red > 0 · Green = 0 |
| Spare Vehicles | Unassigned, operational | Blue |
| Non-Compliant Assignments | Route with expired-doc vehicle | Red > 0 |

---

## 5. Main Table — Route-Vehicle Assignment

**Search:** Route name, bus number, branch. 300ms debounce.

**Filters:**
| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Assignment Status | Radio | All / Assigned / Unassigned |
| Vehicle Compliance | Radio | All / Compliant / Non-Compliant |

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| Branch | ✅ | |
| Route Name | ✅ | Link → route detail (Page 11) |
| Route Direction | ✅ | Morning / Afternoon / Both |
| Student Count | ✅ | Students on this route |
| Assigned Vehicle | ✅ | Bus No + type · or "Unassigned ❌" |
| Vehicle Compliance | ✅ | ✅ Compliant · 🔴 Non-Compliant |
| Assigned Since | ✅ | Date of assignment |
| Backup Vehicle | ✅ | If configured |
| Actions | ❌ | Assign · Swap · Release |

**Default sort:** Unassigned routes first.
**Pagination:** Server-side · 25/page.

---

## 6. Drawers

### 6.1 Drawer: `assign-vehicle`
- **Trigger:** + Assign Vehicle · Actions → Assign
- **Width:** 540px
- **Fields:** Branch · Route (searchable) · Vehicle (searchable — shows only active, compliant vehicles at this branch) · Assignment Type (Primary / Backup) · Effective Date · Notes
- **Vehicle selector shows:** Bus No, type, capacity, compliance status (fitness/permit/insurance), current assignment (if any)
- **Validation:** Cannot assign non-compliant vehicle to active route (warning shown, Director must approve override)

> **Audit trail:** All write actions (assign, swap, release vehicle) are logged to [Transport Audit Log → Page 33] with user, timestamp, and IP.

### 6.2 Drawer: `emergency-swap`
- **Trigger:** Emergency Swap button · Vehicle breakdown scenario
- **Width:** 540px
- **Fields:** Route requiring swap · Reason (Breakdown / Maintenance / Other) · Replacement Vehicle (spare pool for this branch) · Effective From (time) · Expected Duration · Notify Driver (checkbox) · Notify Branch Transport In-Charge (checkbox)
- **On save:** Original vehicle released · Spare assigned · Notifications sent

---

## 7. Spare Vehicle Pool (Section)

> All unassigned, operational vehicles per branch — the spare pool.

**Columns:** Bus No · Branch · Type · Capacity · Compliance Status · Last Used · [Assign to Route →]

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Vehicle assigned | "[Bus No] assigned to Route [Name]." | Success | 4s |
| Assignment failed | "Failed to assign vehicle. Check compliance status or route conflicts." | Error | 5s |
| Emergency swap done | "Emergency swap: [Bus No] now serving Route [Name]. Driver notified." | Warning | 6s |
| Emergency swap failed | "Emergency swap failed. No spare vehicles available at this branch." | Error | 5s |
| Vehicle released | "[Bus No] released from Route [Name]. Added to spare pool." | Info | 4s |
| Release failed | "Failed to release vehicle. Please retry." | Error | 5s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No unassigned routes | "All Routes Assigned" | "Every active route has a vehicle assigned." | — |
| No spare vehicles | "No Spare Vehicles" | "All operational vehicles are assigned to routes." | — |
| No filter results | "No Assignments Match Filters" | "Adjust branch, assignment status, or compliance filters." | [Clear Filters] |
| No search results | "No Routes Found for '[term]'" | "Check the route name, bus number, or branch." | [Clear Search] |

---

## 10. Role-Based UI Visibility

| Element | Fleet Manager G3 | Transport Director G3 | Route Planning Mgr G3 | Safety Officer G3 |
|---|---|---|---|---|
| Assign Vehicle | ✅ | ✅ (approve non-compliant) | ❌ | ❌ |
| Emergency Swap | ✅ | ✅ | ❌ | ❌ |
| Release Vehicle | ✅ | ❌ | ❌ | ❌ |
| View All Assignments | ✅ | ✅ | ✅ | ✅ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/transport/assignments/` | JWT (G3+) | Route-vehicle assignment list |
| POST | `/api/v1/group/{group_id}/transport/assignments/` | JWT (G3+) | Create assignment |
| POST | `/api/v1/group/{group_id}/transport/assignments/emergency-swap/` | JWT (G3+) | Emergency swap |
| DELETE | `/api/v1/group/{group_id}/transport/assignments/{id}/` | JWT (G3+) | Release vehicle |
| GET | `/api/v1/group/{group_id}/transport/vehicles/spare-pool/` | JWT (G3+) | Spare vehicles list |
| GET | `/api/v1/group/{group_id}/transport/assignments/kpis/` | JWT (G3+) | KPI cards |
| GET | `/api/v1/group/{group_id}/transport/assignments/export/` | JWT (G3+) | Async CSV/XLSX export |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-get/post | hx-target | hx-swap |
|---|---|---|---|---|
| Search | `input delay:300ms` | GET `.../assignments/?q={val}` | `#assignment-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../assignments/?{filters}` | `#assignment-table-section` | `innerHTML` |
| Sort | `click` on header | GET `.../assignments/?sort={col}&dir={asc/desc}` | `#assignment-table-section` | `innerHTML` |
| Pagination | `click` | GET `.../assignments/?page={n}` | `#assignment-table-section` | `innerHTML` |
| Assign submit | `click` | POST `.../assignments/` | `#assignment-table-section` | `innerHTML` |
| Emergency swap confirm | `click` | POST `.../assignments/emergency-swap/` | `#assignment-table-section` | `innerHTML` |
| Export | `click` | GET `.../assignments/export/` | `#export-btn` | `outerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
