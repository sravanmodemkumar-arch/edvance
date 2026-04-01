# 03 — Route Planning Manager Dashboard

> **URL:** `/group/transport/routes/`
> **File:** `03-route-planning-manager-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Role:** Group Route Planning Manager (Role 81, G3) — exclusive post-login landing

---

## 1. Purpose

Primary post-login landing for the Group Route Planning Manager. Complete command centre for all transport route management across branches — route creation, pickup/drop point management, student-to-route allocation, route optimization, and bus-driver assignment verification.

The Route Planning Manager owns the spatial design of the transport network. A poorly planned route means students miss buses, parents complain, and drivers work excessive hours. Routes must be approved by the Group Transport Director before going live — this dashboard surfaces the approval pipeline, utilization gaps, and unallocated students.

Scale: 300–800 active routes · 2,000–5,000 pickup/drop stops · 3,000–15,000 students on transport.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Route Planning Manager | G3 | Full — all routes, all branches | Exclusive dashboard |
| Group Transport Director | G3 | Approve routes | Via own dashboard route approval queue |
| Group Fleet Manager | G3 | ❌ No access — own dashboard at /fleet/ | Redirect to Page 02 |
| Group Transport Fee Manager | G3 | Read — route list for fee assignment | View only |
| Group Driver/Conductor HR | G0 | ❌ No EduForge login | See Page 05 |
| Group Transport Safety Officer | G3 | Read — route details for safety review | View only |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Transport Management  ›  Route Planning Dashboard
```

### 3.2 Page Header
```
Welcome back, [Manager Name]               [+ New Route]  [Export Route List ↓]  [Settings ⚙]
Group Route Planning Manager · [N] Active Routes · AY [current academic year]
Branches: [N]  ·  Stops: [N]  ·  Students on Transport: [N]  ·  Unallocated Students: [N]
```

### 3.3 Alert Banner

| Condition | Banner Text | Severity |
|---|---|---|
| Unallocated students > 0 | "[N] students are not assigned to any transport route." | Amber |
| Route without bus assignment | "[N] routes have no vehicle assigned." | Red |
| Route without driver assignment | "[N] routes have no driver assigned." | Red |
| Route pending Director approval > 48h | "[N] routes awaiting Director approval for > 48 hours." | Amber |
| Route with overcapacity (students > bus capacity) | "[N] routes are overloaded. Student count exceeds bus capacity." | Red |

---

## 4. KPI Summary Bar (7 cards)

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Total Active Routes | Across all branches | Blue always | → Page 11 |
| Routes Fully Staffed | Bus + Driver assigned | Green = 100% · Yellow < 100% · Red < 90% | → Page 11 |
| Total Stops | Pickup + drop points | Blue always | → Page 12 |
| Students on Transport | Allocated to a route | Blue always | → Page 14 |
| Unallocated Students | Day scholars with no route | Red > 0 · Green = 0 | → Page 14 |
| Routes Pending Approval | Awaiting Director sign-off | Yellow > 0 | → Page 11 (pending filter) |
| Overloaded Routes | Capacity exceeded | Red > 0 · Green = 0 | → Page 11 (overload filter) |

---

## 5. Sections

### 5.1 Route Summary Table (Branch-wise)

> Per-branch route overview — Manager's primary working view.

**Search:** Branch name, city. 300ms debounce.

**Filters:**
| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Route Status | Radio | All / Active / Pending Approval / Suspended |
| Assignment | Radio | All / Fully Assigned / Missing Bus / Missing Driver |
| Capacity | Radio | All / Normal / Overloaded |

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| Branch | ✅ | Link → branch route detail drawer |
| Routes | ✅ | Total active |
| Stops | ✅ | Total stop count |
| Students | ✅ | Allocated students |
| Fully Assigned | ✅ | Routes with bus + driver |
| Overloaded | ✅ | Red if > 0 |
| Pending Approval | ✅ | Yellow if > 0 |
| Actions | ❌ | View Routes · Add Route · Optimize |

**Pagination:** Server-side · 25/page.

---

### 5.2 Route Map Overview

> Spatial view of all routes across a selected branch.

- Branch selector dropdown
- Embedded map (Leaflet.js) showing route lines colour-coded by status
- Green = Active + assigned · Yellow = Pending · Red = Unassigned / Overloaded
- Click any route → route detail side panel
- "View full route manager →" → Page 11

---

### 5.3 Unallocated Students List

> Students who are enrolled as day scholars but have no route assignment.

**Columns:** Student Name · Branch · Class · Address / Area · Nearest Route (suggested) · [Assign →]

"View student transport allocation →" → Page 14.

---

### 5.4 Route Optimization Suggestions

> System-generated suggestions for route improvements.

**Columns:** Suggestion Type · Affected Branch · Route · Rationale · Students Impacted · [Review →]

Types: Merge (two underutilised routes) · Split (overloaded route) · Add Stop · Remove Redundant Stop.

"View full optimization tool →" → Page 13.

---

## 6. Drawers

### 6.1 Drawer: `new-route`
- **Trigger:** + New Route
- **Width:** 640px
- **Fields:** Branch · Route Name / Code · Direction (Morning / Afternoon / Both) · Starting Point · End Point · Stops (multi-row: stop name, area, sequence order) · Estimated Distance (km) · Estimated Duration (min) · Vehicle Assignment (optional) · Driver Assignment (optional)
- **Validation:** At least 2 stops required · Route name unique per branch
- **On save:** Status = "Pending Approval" — notifies Transport Director

### 6.2 Drawer: `branch-route-detail`
- **Width:** 640px
- **Tabs:** Routes · Stops · Students · Assignments
- All routes at this branch with status, assignments, capacity
- Stops list with student count per stop
- Students allocated to this branch's routes
- Bus/driver assignments per route

> **Audit trail:** All write actions (create route, update route, allocate students) are logged to [Transport Audit Log → Page 33].

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Route created | "Route [Name] created at [Branch]. Awaiting Director approval." | Success | 4s |
| Route create failed | "Failed to create route. Check for duplicate route code." | Error | 5s |
| Route approved | "Route [Name] approved and activated." | Success | 4s |
| Route approval failed | "Route approval failed. Please try again." | Error | 5s |
| Route updated | "Route [Name] updated." | Info | 4s |
| Route update failed | "Route update failed. Please retry." | Error | 5s |
| Student allocated | "[N] students allocated to Route [Name]." | Success | 4s |
| Allocation failed | "Student allocation failed. Check route capacity." | Error | 5s |
| Overload detected | "Warning: Route [Name] is over capacity by [N] students." | Warning | 6s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No routes | "No Routes Configured" | "Create routes for each branch before allocating students." | [+ New Route] |
| No unallocated students | "All Students Allocated" | "All day scholars have been assigned to transport routes." | — |
| No optimization suggestions | "Routes Are Optimal" | "No route optimization suggestions at this time." | — |
| Route table — no filter results | "No Branches Match Filters" | "Adjust status, assignment, or capacity filters." | [Clear Filters] |
| Route table — no search results | "No Branches Found for '[term]'" | "Check the branch name." | [Clear Search] |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page load | Skeleton: 7 KPI cards + route table + map placeholder + optimization list |
| Table filter | Inline skeleton rows |
| Map branch change | Map loading overlay |
| New route drawer | 640px drawer skeleton |

---

## 10. Role-Based UI Visibility

| Element | Route Planning Mgr G3 | Transport Director G3 | Safety Officer G3 | Fee Manager G3 |
|---|---|---|---|---|
| Create Route | ✅ | ✅ | ❌ | ❌ |
| Approve Route | ❌ | ✅ | ❌ | ❌ |
| Edit Route | ✅ | ❌ | ❌ | ❌ |
| Assign Students | ✅ | ❌ | ❌ | ❌ |
| View Route Map | ✅ | ✅ | ✅ | ✅ |
| Export | ✅ | ✅ | ✅ | ✅ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/transport/routes/dashboard/` | JWT (G3+) | Dashboard data |
| GET | `/api/v1/group/{group_id}/transport/routes/kpi-cards/` | JWT (G3+) | KPI refresh |
| GET | `/api/v1/group/{group_id}/transport/routes/branch-summary/` | JWT (G3+) | Branch-wise route table |
| GET | `/api/v1/group/{group_id}/transport/routes/map-data/` | JWT (G3+) | Route geodata for map |
| GET | `/api/v1/group/{group_id}/transport/routes/unallocated-students/` | JWT (G3+) | Unallocated students |
| GET | `/api/v1/group/{group_id}/transport/routes/optimization-suggestions/` | JWT (G3+) | Optimization suggestions |
| POST | `/api/v1/group/{group_id}/transport/routes/` | JWT (G3+) | Create route |
| GET | `/api/v1/group/{group_id}/transport/routes/branches/{id}/detail/` | JWT (G3+) | Branch route drawer |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-get/post | hx-target | hx-swap |
|---|---|---|---|---|
| KPI auto-refresh | `every 10m` | GET `.../routes/kpi-cards/` | `#kpi-bar` | `innerHTML` |
| Route table search | `input delay:300ms` | GET `.../routes/branch-summary/?q={val}` | `#route-table-body` | `innerHTML` |
| Route table sort | `click` on header | GET `.../routes/branch-summary/?sort={col}&dir={asc/desc}` | `#route-table-section` | `innerHTML` |
| Route table pagination | `click` | GET `.../routes/branch-summary/?page={n}` | `#route-table-section` | `innerHTML` |
| Route table filter | `click` | GET `.../routes/branch-summary/?{filters}` | `#route-table-section` | `innerHTML` |
| Map branch select | `change` | GET `.../routes/map-data/?branch={id}` | `#route-map-container` | `innerHTML` |
| Open branch drawer | `click` | GET `.../routes/branches/{id}/detail/` | `#drawer-body` | `innerHTML` |
| Submit new route | `click` | POST `.../routes/` | `#route-table-section` | `innerHTML` |
| Export route list | `click` | GET `.../routes/branch-summary/export/` | `#export-btn` | `outerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
