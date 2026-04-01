# 11 — Route Manager

> **URL:** `/group/transport/routes/list/`
> **File:** `11-route-manager.md`
> **Template:** `portal_base.html`
> **Priority:** P0
> **Role:** Group Route Planning Manager (primary) · Transport Director · Transport Safety Officer · Transport Fee Manager

---

## 1. Purpose

Master list of all transport routes across every branch. Each route record defines the service (branch, direction, start–end points, stops, vehicle assignment, driver assignment, student count, status, and fee plan). Routes must be approved by the Group Transport Director before going Active.

This page is the operational hub for all route management — creating new routes, editing existing ones, suspending routes, and drilling into stop-level detail. It cross-links to the student allocation page (Page 14), GPS tracking (Page 18), and fee structures (Page 20).

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Route Planning Manager | G3 | Full — create, edit, propose suspension | Primary owner |
| Group Transport Director | G3 | Approve / Reject / Suspend routes | Approval authority |
| Group Transport Safety Officer | G3 | Read — safety review | View only |
| Group Transport Fee Manager | G3 | Read — fee plan link | View only |
| Branch Transport In-Charge | Branch G3 | View own branch routes | Cannot edit |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Transport Management  ›  Route Manager
```

### 3.2 Page Header
- **Title:** `Route Manager`
- **Subtitle:** `[N] Active Routes · [N] Pending Approval · [N] Suspended · AY [current]`
- **Right controls:** `+ New Route` · `Advanced Filters` · `Export`

### 3.3 Alert Banner

| Condition | Banner Text | Severity |
|---|---|---|
| Routes with no vehicle | "[N] active routes have no vehicle assigned." | Red |
| Routes with no driver | "[N] active routes have no driver assigned." | Red |
| Overloaded routes | "[N] routes have student count exceeding vehicle capacity." | Red |
| Routes pending approval > 48h | "[N] routes have been pending Director approval for > 48 hours." | Amber |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule |
|---|---|---|
| Total Active Routes | Across all branches | Blue |
| Routes — Fully Assigned | Bus + Driver assigned | Green = 100% · Red < 100% |
| Overloaded Routes | Students > capacity | Red > 0 · Green = 0 |
| Pending Approval | Awaiting Director | Yellow > 0 |
| Total Stops (All Routes) | Pickup + drop | Blue |
| Students on Transport | Allocated to any route | Blue |

---

## 5. Main Table — Route List

**Search:** Route name/code, branch, start point, end point. 300ms debounce.

**Advanced Filters:**
| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Status | Checkbox | Active / Pending Approval / Suspended / Retired |
| Direction | Checkbox | Morning / Afternoon / Both |
| Assignment | Radio | All / Fully Assigned / Missing Bus / Missing Driver |
| Capacity | Radio | All / Normal / Overloaded |

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| Route Code | ✅ | Internal code |
| Route Name | ✅ | Link → route detail drawer |
| Branch | ✅ | |
| Direction | ✅ | Morning / Afternoon / Both |
| Stops | ✅ | Count |
| Students | ✅ | Allocated count |
| Capacity | ✅ | Bus seat count · coloured if students > capacity |
| Bus Assigned | ✅ | Bus No · or ❌ |
| Driver Assigned | ✅ | Driver name · or ❌ |
| Distance (km) | ✅ | Route total |
| Avg Duration (min) | ✅ | |
| Fee Plan | ✅ | ✅ Set · ❌ Missing |
| Status | ✅ | Badge |
| Actions | ❌ | View · Edit · Approve · Suspend · Retire |

**Pagination:** Server-side · 25/page.

---

## 6. Drawers

### 6.1 Drawer: `route-detail` — View Route
- **Trigger:** Route Name link or Actions → View
- **Width:** 680px
- **Tabs:** Overview · Stops · Students · Driver · GPS History · Approvals
- **Overview:** All route fields, status history
- **Stops:** Ordered list of pickup/drop stops with student counts per stop
- **Students:** Paginated list of all students on this route
- **Driver:** Current driver assignment, duty history
- **GPS History:** Last 30 days on-time performance, delay events
- **Approvals:** Approval history (created, modified, approved/rejected, suspended)

### 6.2 Drawer: `route-create`
- **Trigger:** + New Route
- **Width:** 680px
- **Fields:** Branch · Route Name · Route Code · Direction (Morning / Afternoon / Both) · Starting Point · End Point · Estimated Distance (km) · Estimated Duration (min) · Stops (multi-row: sequence, stop name, area, landmark, approx arrival time) · Notes
- **On save:** Status = "Pending Approval"; Director notified via in-app + email

### 6.3 Drawer: `route-edit`
- **Trigger:** Actions → Edit
- **Width:** 680px (same as create, pre-populated)
- **If route is Active:** Editing requires Director re-approval for structural changes (stop additions/removals, direction change)

> **Audit trail:** All write actions (create, edit, approve, suspend, retire route) are logged to [Transport Audit Log → Page 33] with user, timestamp, and IP.

### 6.4 Modal: `route-approve`
- **Trigger:** Actions → Approve (Transport Director only)
- **Width:** 480px
- **Content:** Route summary — name, stops, students, vehicle check, driver check
- **Fields:** Approval Note (optional)
- **On confirm:** Status → Active; Route Planning Manager notified

### 6.5 Modal: `route-suspend`
- **Trigger:** Actions → Suspend
- **Width:** 480px
- **Fields:** Reason · Effective Date · Expected Resume Date · Notify Affected Students/Parents (checkbox)
- **On confirm:** Status → Suspended; affected students notified; fee billing paused

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Route created | "Route [Name] created. Awaiting Director approval." | Success | 4s |
| Route create failed | "Failed to create route. Check for duplicate route code." | Error | 5s |
| Route approved | "Route [Name] approved and activated." | Success | 4s |
| Route approval failed | "Route approval failed. Please retry." | Error | 5s |
| Route updated | "Route [Name] updated. Re-approval required for structural changes." | Info | 4s |
| Route update failed | "Failed to update route. Please retry." | Error | 5s |
| Route suspended | "Route [Name] suspended. [N] students notified." | Warning | 6s |
| Suspension failed | "Failed to suspend route. Please retry." | Error | 5s |
| Route rejected | "Route [Name] rejected by Director. Reason: [note]." | Warning | 5s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No routes | "No Routes Configured" | "Create the first transport route for this group." | [+ New Route] |
| No filter results | "No Routes Match Filters" | "Adjust status, direction, assignment, or capacity filters." | [Clear Filters] |
| No search results | "No Routes Found for '[term]'" | "Check the route name, code, or branch." | [Clear Search] |
| No pending approvals | "No Routes Pending Approval" | "All submitted routes have been reviewed." | — |
| No overloaded routes | "No Overloaded Routes" | "All route capacities are within limits." | — |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page load | Skeleton: 6 KPI cards + route table |
| Filter/search | Table body skeleton |
| Route detail drawer | 680px skeleton; tabs load lazily |
| Approve/suspend modal | Spinner on Confirm |

---

## 10. Role-Based UI Visibility

| Element | Route Planning Mgr G3 | Transport Director G3 | Safety Officer G3 | Fee Manager G3 |
|---|---|---|---|---|
| Create Route | ✅ | ✅ | ❌ | ❌ |
| Edit Route | ✅ | ❌ | ❌ | ❌ |
| Approve Route | ❌ | ✅ | ❌ | ❌ |
| Suspend Route | ✅ (propose) | ✅ (execute) | ❌ | ❌ |
| View All Routes | ✅ | ✅ | ✅ | ✅ |
| Export | ✅ | ✅ | ✅ | ✅ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/transport/routes/` | JWT (G3+) | Paginated, filtered route list |
| GET | `/api/v1/group/{group_id}/transport/routes/{id}/` | JWT (G3+) | Route detail |
| POST | `/api/v1/group/{group_id}/transport/routes/` | JWT (G3+) | Create route |
| PATCH | `/api/v1/group/{group_id}/transport/routes/{id}/` | JWT (G3+) | Update route |
| POST | `/api/v1/group/{group_id}/transport/routes/{id}/approve/` | JWT (G3+ Director) | Approve route |
| POST | `/api/v1/group/{group_id}/transport/routes/{id}/suspend/` | JWT (G3+) | Suspend route |
| GET | `/api/v1/group/{group_id}/transport/routes/kpis/` | JWT (G3+) | KPI cards |
| GET | `/api/v1/group/{group_id}/transport/routes/export/` | JWT (G3+) | Export |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-get/post | hx-target | hx-swap |
|---|---|---|---|---|
| Search | `input delay:300ms` | GET `.../routes/?q={val}` | `#route-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../routes/?{filters}` | `#route-table-section` | `innerHTML` |
| Open route drawer | `click` on Route Name | GET `.../routes/{id}/` | `#drawer-body` | `innerHTML` |
| Create submit | `click` | POST `.../routes/` | `#route-table-section` | `innerHTML` |
| Sort | `click` on header | GET `.../routes/?sort={col}&dir={asc/desc}` | `#route-table-section` | `innerHTML` |
| Pagination | `click` | GET `.../routes/?page={n}` | `#route-table-section` | `innerHTML` |
| Approve confirm | `click` | POST `.../routes/{id}/approve/` | `#route-row-{id}` | `outerHTML` |
| Suspend confirm | `click` | POST `.../routes/{id}/suspend/` | `#route-row-{id}` | `outerHTML` |
| Export | `click` | GET `.../routes/export/` | `#export-btn` | `outerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
