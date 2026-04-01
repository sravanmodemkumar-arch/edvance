# 12 — Pickup / Drop Point Manager

> **URL:** `/group/transport/routes/stops/`
> **File:** `12-pickup-drop-point-manager.md`
> **Template:** `portal_base.html`
> **Priority:** P1
> **Role:** Group Route Planning Manager (primary) · Transport Director · Transport Safety Officer

---

## 1. Purpose

Granular management of every pickup and drop point across all routes in all branches. Each stop represents a physical location where students board or alight. Stop data includes geo-coordinates, area/landmark, expected arrival time, student count, and safety rating (lighting, visibility, road conditions).

Stops are the last-mile touchpoint in student safety. A poorly chosen stop location (on a blind curve, under a poorly lit road, with no waiting area) creates daily risk. The Route Planning Manager manages stop additions/removals; the Safety Officer can flag stops for safety review.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Route Planning Manager | G3 | Full — add, edit, remove stops | Primary owner |
| Group Transport Director | G3 | Approve new stop on approved routes | View + approve |
| Group Transport Safety Officer | G3 | Read + flag safety concern | Safety flag only |
| Branch Transport In-Charge | Branch G3 | Read own branch stops | View only |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Transport Management  ›  Pickup / Drop Point Manager
```

### 3.2 Page Header
- **Title:** `Pickup / Drop Point Manager`
- **Subtitle:** `[N] Total Stops · [N] Routes · [N] Branches · [N] Safety Flags`
- **Right controls:** `+ Add Stop` · `Map View` · `Advanced Filters` · `Export`

### 3.3 Alert Banner

| Condition | Banner Text | Severity |
|---|---|---|
| Safety-flagged stops | "[N] stops have open safety flags. Review required." | Amber |
| Stops with no students | "[N] stops have 0 students assigned." | Amber |
| Stops with missing geo-coordinates | "[N] stops have no geo-location set — GPS tracking gap." | Amber |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule |
|---|---|---|
| Total Stops | All active stops | Blue |
| Pickup-only Stops | Morning boarding points | Blue |
| Drop-only Stops | Afternoon deboarding | Blue |
| Pickup + Drop | Bidirectional stops | Blue |
| Safety Flagged | Open safety concerns | Yellow > 0 · Red > 5 |
| Stops Missing Geo-data | No coordinates | Yellow > 0 |

---

## 5. Main Table — Stop List

**Search:** Stop name, area, landmark, route name. 300ms debounce.

**Filters:**
| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Route | Multi-select | All routes |
| Stop Type | Checkbox | Pickup / Drop / Both |
| Safety Status | Radio | All / Flagged / Clear |
| Geo-data | Checkbox | Show stops missing coordinates |

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| Stop Name | ✅ | Link → stop detail drawer |
| Route | ✅ | Route name |
| Branch | ✅ | |
| Stop Type | ✅ | Pickup / Drop / Both |
| Sequence | ✅ | Order on route |
| Area / Landmark | ✅ | |
| Students | ✅ | Currently boarding here |
| Expected Arrival | ✅ | Time |
| Geo Status | ✅ | ✅ Mapped · ❌ Missing |
| Safety Status | ✅ | ✅ Clear · ⚠ Flagged |
| Actions | ❌ | View · Edit · Flag Safety · Remove |

**Pagination:** Server-side · 25/page.

---

## 6. Map View

> Toggle between table and map view.

- All stops plotted on Leaflet.js map
- Colour coded: Green = clear · Red = safety flagged · Grey = missing geo-data
- Click stop → mini popup: stop name, route, students, type, [Edit] [Flag]
- Cluster markers for zoomed-out views
- "View GPS live map →" → Page 18 (different view — live buses vs static stops)

---

## 7. Drawers

### 7.1 Drawer: `stop-create`
- **Width:** 540px
- **Fields:** Branch · Route (searchable) · Stop Name · Area / Landmark · Stop Type (Pickup / Drop / Both) · Sequence on Route (numeric) · Expected Arrival Time (HH:MM) · Geo-coordinates (lat/lng — map pin picker + manual entry) · Safety Notes (optional)
- **Validation:** Stop name unique per route · Sequence number not duplicate

### 7.2 Drawer: `stop-detail`
- **Width:** 540px
- **Tabs:** Details · Students · Safety
- **Details:** All stop fields, mini map with location pin
- **Students:** List of students boarding/alighting at this stop with class and route
- **Safety:** Safety flags history, status, resolution notes

> **Audit trail:** All write actions (add stop, edit stop, remove stop, flag safety) are logged to [Transport Audit Log → Page 33] with user, timestamp, and IP.

### 7.3 Drawer: `flag-safety`
- **Width:** 480px
- **Fields:** Stop · Concern Type (Poor Lighting / Blind Spot / Traffic Hazard / No Waiting Area / Flooding Risk / Other) · Description · Severity (Low / Medium / High) · Photos (upload)
- **On save:** Safety Officer and Transport Director notified

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Stop added | "Stop [Name] added to Route [Route Name]." | Success | 4s |
| Stop add failed | "Failed to add stop. Check for duplicate stop name or sequence number on this route." | Error | 5s |
| Stop updated | "Stop [Name] updated." | Info | 4s |
| Stop update failed | "Failed to update stop. Please retry." | Error | 5s |
| Safety flag raised | "Safety flag raised for Stop [Name]. Transport Safety Officer notified." | Warning | 5s |
| Safety flag failed | "Failed to raise safety flag. Please retry." | Error | 5s |
| Safety flag resolved | "Safety flag for Stop [Name] resolved." | Success | 4s |
| Stop removed | "Stop [Name] removed from Route [Route Name]. [N] students need reassignment." | Warning | 6s |
| Stop remove failed | "Failed to remove stop. Ensure no students are currently assigned to this stop." | Error | 5s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No stops | "No Stops Configured" | "Add pickup and drop points for each route." | [+ Add Stop] |
| No filter results | "No Stops Match Filters" | "Adjust route, branch, stop type, or safety status filters." | [Clear Filters] |
| No search results | "No Stops Found for '[term]'" | "Check the stop name, area, or route name." | [Clear Search] |
| No safety flags | "No Safety Flags" | "All stops have cleared safety review." | — |
| No stops missing geo-data | "All Stops Mapped" | "All stops have geo-coordinates for GPS tracking." | — |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Page load | Skeleton: 6 KPI cards + stop table |
| Map view toggle | Map loading overlay |
| Stop detail drawer | 540px drawer skeleton |

---

## 11. Role-Based UI Visibility

| Element | Route Planning Mgr G3 | Transport Director G3 | Safety Officer G3 |
|---|---|---|---|
| Add Stop | ✅ | ✅ | ❌ |
| Edit Stop | ✅ | ❌ | ❌ |
| Remove Stop | ✅ | ✅ (approve) | ❌ |
| Flag Safety | ✅ | ✅ | ✅ |
| Resolve Safety Flag | ✅ | ✅ | ✅ |
| View Map | ✅ | ✅ | ✅ |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/transport/stops/` | JWT (G3+) | Paginated stop list |
| GET | `/api/v1/group/{group_id}/transport/stops/{id}/` | JWT (G3+) | Stop detail |
| POST | `/api/v1/group/{group_id}/transport/stops/` | JWT (G3+) | Create stop |
| PATCH | `/api/v1/group/{group_id}/transport/stops/{id}/` | JWT (G3+) | Update stop |
| DELETE | `/api/v1/group/{group_id}/transport/stops/{id}/` | JWT (G3+) | Remove stop |
| POST | `/api/v1/group/{group_id}/transport/stops/{id}/flag-safety/` | JWT (G3+) | Raise safety flag |
| GET | `/api/v1/group/{group_id}/transport/stops/map-data/` | JWT (G3+) | Geo-data for map |

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-get/post | hx-target | hx-swap |
|---|---|---|---|---|
| Search | `input delay:300ms` | GET `.../stops/?q={val}` | `#stop-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../stops/?{filters}` | `#stop-table-section` | `innerHTML` |
| Sort | `click` on header | GET `.../stops/?sort={col}&dir={asc/desc}` | `#stop-table-section` | `innerHTML` |
| Pagination | `click` | GET `.../stops/?page={n}` | `#stop-table-section` | `innerHTML` |
| Toggle map view | `click` | GET `.../stops/map-data/` | `#stop-map-container` | `innerHTML` |
| Open stop detail drawer | `click` on Stop Name | GET `.../stops/{id}/` | `#drawer-body` | `innerHTML` |
| Create stop submit | `click` | POST `.../stops/` | `#stop-table-section` | `innerHTML` |
| Remove stop confirm | `click` | DELETE `.../stops/{id}/` | `#stop-row-{id}` | `outerHTML` |
| Flag safety confirm | `click` | POST `.../stops/{id}/flag-safety/` | `#stop-row-{id}` | `outerHTML` |
| Export | `click` | GET `.../stops/export/` | `#export-btn` | `outerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
