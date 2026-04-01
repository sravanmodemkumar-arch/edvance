# 14 — Room Allocation Manager

> **URL:** `/group/hostel/rooms/`
> **File:** `14-room-allocation-manager.md`
> **Template:** `portal_base.html`
> **Priority:** P1
> **Role:** Group Hostel Director · Boys/Girls Coordinators · Group Hostel Admission Coordinator

---

## 1. Purpose

The Room Allocation Manager is the operational tool for assigning, reassigning, and swapping hostel rooms for individual hostelers across all branches. While the Hosteler Registry (Page 12) shows what room a hosteler is in, this page lets coordinators manage the room assignment process — view all rooms (with bed-level detail), allocate empty beds to new or existing hostelers, swap beds between hostelers, and mark rooms as under maintenance.

This page is used primarily at the start of academic year (bulk room assignment for new hostelers) and whenever a hosteler needs to be transferred due to disciplinary, medical, or welfare reasons.

---

## 2. Role Access

| Role | Level | Access |
|---|---|---|
| Group Hostel Director | G3 | Full — all branches, all genders |
| Group Boys Hostel Coordinator | G3 | Boys rooms only |
| Group Girls Hostel Coordinator | G3 | Girls rooms only |
| Group Hostel Admission Coordinator | G3 | Allocate (during admission process) |
| Group Hostel Welfare Officer | G3 | View only (for incident context) |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Hostel Management  ›  Room Allocation Manager
```

### 3.2 Page Header
- **Title:** `Room Allocation Manager`
- **Subtitle:** `[N] Total Rooms · [N] Fully Occupied · [N] Partially Occupied · [N] Empty · [N] Under Maintenance`
- **Right controls:** `Branch selector (dropdown)` · `Hostel Type (Boys/Girls)` · `Room Type (AC/Non-AC)` · `Floor filter`

---

## 4. Branch / Hostel Selector

> Persistent top-bar selector — Room Manager is always branch-specific.

`Branch: [dropdown] · Hostel: [Boys/Girls radio] · Type: [AC/Non-AC radio]`

Changing any selector instantly loads the room grid for that combination via HTMX.

> **Selector change safeguard:** If a drawer (`room-allocate` or `room-swap`) is currently open, all selector inputs are disabled and made read-only. A tooltip appears on hover: "Close the open drawer before switching branch or hostel." This prevents partial allocation data from being submitted to the wrong hostel campus.

---

## 5. Room Grid View

> Visual representation of all rooms on each floor for the selected hostel.

**Display:** Floor-by-floor accordion. Each floor shows a grid of room cards.

**Room Card:**
```
┌────────────────┐
│ Room B-204     │
│ AC · Floor 2   │
├────────────────┤
│ Bed A: [Name] ✅│
│ Bed B: [Name] ✅│
│ Bed C: EMPTY  🔵│
└────────────────┘
```

Card background colors:
- Green: All beds occupied
- Blue: At least one empty bed
- Yellow: Partially occupied (≥ 50%)
- Gray: Under maintenance
- Red: Quarantine / medical isolation

Click on a room card → opens `room-detail` drawer.

---

## 6. Room List Table View

> Toggle between grid and table view using "Grid / Table" toggle button.

**Columns:**
| Column | Sortable |
|---|---|
| Room # | ✅ |
| Floor | ✅ |
| Type | ✅ (AC/Non-AC) |
| Capacity (beds) | ✅ |
| Occupied | ✅ |
| Available | ✅ |
| Hostelers (Names) | ❌ (truncated) |
| Status | ✅ (Active/Maintenance/Quarantine) |
| Actions | ❌ (View · Allocate · Swap · Mark Maintenance) |

---

## 7. Drawers

### 7.1 Drawer: `room-detail`
- **Trigger:** Room card click or table → View
- **Width:** 560px
- **Content:**
  - Room header: Number, floor, type, AC/Non-AC, status
  - Bed grid: Each bed (A/B/C/D) with hosteler name + photo + class + link to their registry profile
  - Empty beds show: [Allocate →] button
  - Occupied beds show: Hosteler details + [Swap Bed →] + [Move Out →]
  - Room history: Last 12 room assignment changes

### 7.2 Drawer: `room-allocate` — Assign Hosteler to Bed
- **Trigger:** Empty bed → [Allocate →]
- **Width:** 560px
- **Fields:**
  - Hosteler (search autocomplete — only shows unassigned or pending-room hostelers matching gender)
  - Bed (pre-filled from clicked bed)
  - Effective Date
  - Reason (Admission / Transfer / Return from Leave)
  - Notify Parent (checkbox)
- **Validation:** Gender must match hostel; hosteler must not have another active room assignment

### 7.3 Drawer: `room-swap` — Swap Two Hostelers' Beds
- **Trigger:** Bed → [Swap Bed →]
- **Width:** 480px
- **Fields:**
  - Hosteler A: pre-filled (current bed occupant)
  - Hosteler B: search autocomplete (same hostel only)
  - Swap Date
  - Reason (required: Welfare / Medical / Disciplinary / Requested by hosteler / Administrative)
  - Notify both parents (checkbox)
- **Validation:** Both hostelers must be same gender, same hostel campus

### 7.4 Modal: Mark Room as Under Maintenance
- **Trigger:** Room card → Mark Maintenance
- **Type:** Centred modal (480px)
- **Fields:** Expected return date · Reason · Affected beds (checkboxes A/B/C/D)
- **Note:** "Hostelers in marked beds must be moved before maintenance is active."

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Bed allocated | "Bed [room#/bed] allocated to [Hosteler Name]." | Success | 4s |
| Swap completed | "Beds swapped between [Name A] and [Name B]." | Success | 4s |
| Room marked maintenance | "Room [#] marked as under maintenance." | Info | 4s |
| Parent notified | "Parent notified via WhatsApp." | Info | 3s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No rooms configured | "No Rooms Configured" | "No rooms have been added for this hostel." | [Contact IT Admin] |
| All beds occupied | "All Beds Fully Occupied" | "No empty beds in this hostel campus." | [View Other Branches] |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Branch/hostel selector change | Full room grid skeleton |
| Allocate drawer submit | Spinner; room card refreshes with new occupant |
| Swap drawer submit | Spinner; both bed cells refresh |

---

## 11. Role-Based UI Visibility

| Element | Hostel Director | Boys Coord | Girls Coord | Admission Coord | Welfare Officer |
|---|---|---|---|---|---|
| Boys room grid | ✅ | ✅ | ❌ | ✅ | ✅ read-only |
| Girls room grid | ✅ | ❌ | ✅ | ✅ | ✅ read-only |
| Allocate bed | ✅ | ✅ Boys | ✅ Girls | ✅ | ❌ |
| Swap beds | ✅ | ✅ Boys | ✅ Girls | ❌ | ❌ |
| Mark maintenance | ✅ | ✅ | ✅ | ❌ | ❌ |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/hostel/rooms/?branch={id}&gender={m/f}&type={ac/nonac}` | JWT (G3+) | Room list with bed status |
| GET | `/api/v1/group/{group_id}/hostel/rooms/{room_id}/` | JWT (G3+) | Room detail |
| POST | `/api/v1/group/{group_id}/hostel/rooms/{room_id}/beds/{bed}/allocate/` | JWT (G3+) | Allocate hosteler to bed |
| POST | `/api/v1/group/{group_id}/hostel/rooms/swap/` | JWT (G3+) | Swap two hostelers' beds |
| PATCH | `/api/v1/group/{group_id}/hostel/rooms/{room_id}/` | JWT (G3+) | Update room status (maintenance) |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-get/post | hx-target | hx-swap |
|---|---|---|---|---|
| Branch selector change | `change` | GET `.../rooms/?branch={id}&gender={m/f}&type={t}` | `#room-grid` | `innerHTML` |
| Room card click | `click` | GET `.../rooms/{room_id}/` | `#drawer-body` | `innerHTML` |
| Allocate submit | `click` | POST `.../beds/{bed}/allocate/` | `#room-card-{room_id}` | `outerHTML` |
| Swap submit | `click` | POST `.../rooms/swap/` | `#room-grid` | `innerHTML` |
| Mark maintenance confirm | `click` | PATCH `.../rooms/{room_id}/` | `#room-card-{room_id}` | `outerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
