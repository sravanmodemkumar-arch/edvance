# 13 — Hostel Occupancy Overview

> **URL:** `/group/hostel/occupancy/`
> **File:** `13-hostel-occupancy-overview.md`
> **Template:** `portal_base.html`
> **Priority:** P0
> **Role:** Group Hostel Director (primary) · All hostel roles (view scoped by gender)

---

## 1. Purpose

Real-time cross-branch occupancy dashboard for all hostel campuses. Shows how many beds are filled, empty, or reserved across every combination of branch × gender × room type (AC/Non-AC). Used daily by the Hostel Director and Admission Coordinator for seat allocation decisions; used by the Fee Manager for billing reconciliation (only occupied beds are billed); used by Boys/Girls Coordinators to monitor their respective campuses.

Occupancy is dynamic — hostelers go on leave, return, transfer rooms, or exit. The occupancy snapshot is pulled fresh from the database on each page load and auto-refreshes every 10 minutes.

---

## 2. Role Access

| Role | Level | Access |
|---|---|---|
| Group Hostel Director | G3 | Full — all branches, all genders |
| Group Boys Hostel Coordinator | G3 | Boys hostel columns only |
| Group Girls Hostel Coordinator | G3 | Girls hostel columns only |
| Group Hostel Admission Coordinator | G3 | Full view + seat availability drill-down |
| Group Hostel Fee Manager | G3 | Full view (for billing reconciliation) |
| Group Hostel Welfare Officer | G3 | Full view (read-only) |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Hostel Management  ›  Hostel Occupancy Overview
```

### 3.2 Page Header
- **Title:** `Group Hostel Occupancy Overview`
- **Subtitle:** `[N] Hostel Campuses · [N] Total Beds · [N] Occupied ([N]%) · [N] Available · Last updated: [time]`
- **Right controls:** `Refresh ↻` · `Export ↓` · `Filter by Branch`

---

## 4. KPI Summary Bar (8 cards)

| Card | Metric | Colour Rule |
|---|---|---|
| Total Beds (All) | All hostel beds across all branches | Blue |
| Occupied | Filled beds | Green ≥ 85% · Yellow 70–85% · Red < 70% |
| Available | Empty beds (not reserved) | Blue |
| Reserved | Beds reserved for incoming hostelers | Blue |
| Boys Occupancy % | Boys beds filled / total boys beds | Colour-coded same as Occupied |
| Girls Occupancy % | Girls beds filled / total girls beds | Colour-coded |
| AC Occupancy % | AC beds filled / total AC beds | Colour-coded |
| Non-AC Occupancy % | Non-AC beds filled / total | Colour-coded |

**HTMX:** `hx-trigger="every 10m"` → `hx-get="/api/v1/group/{id}/hostel/occupancy/kpis/"` → `hx-target="#kpi-bar"` `hx-swap="innerHTML"`

---

## 5. Sections

### 5.1 Occupancy Heat Map

> Visual grid — each cell is one hostel campus. Color = occupancy %.

**Display:** Grid of cards, one per branch-hostel (Branch A Boys / Branch A Girls are separate cards).

**Card content:**
- Branch name + Hostel type (Boys/Girls) + Room type (AC/Non-AC)
- Progress bar: Occupied [N] / Total [N]
- Occupancy % in large font (colour-coded: Green ≥ 85% / Yellow 70–85% / Red < 70%)
- [View Rooms →] button → Page 14 (filtered)

**Group by:** Branch (default) or Room Type or Zone.

> **Zone grouping:** The "Zone" option is visible only when Zone configuration is enabled for the group (applicable to large multi-city groups). For groups without Zone management set up, the Zone option is hidden from the Group by control. No "Zone management not configured" error is shown — the option is simply absent.

---

### 5.2 Branch Occupancy Table

> Detailed tabular view for filtering and export.

**Search:** Branch name. 300ms debounce.

**Filters:**
| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Gender | Radio | All / Boys / Girls |
| Room Type | Checkbox | AC / Non-AC |
| Occupancy Rate | Radio | Any / Fully occupied (≥ 98%) / Available (< 85%) / Empty (< 50%) |
| Zone | Multi-select | All zones (large groups) |

**Columns:**
| Column | Sortable |
|---|---|
| Branch | ✅ |
| Hostel Type | ✅ |
| Room Type | ✅ |
| Total Beds | ✅ |
| Occupied | ✅ |
| Available | ✅ |
| Reserved | ✅ |
| On Leave (counted as occupied) | ✅ |
| Occupancy % | ✅ |
| Actions | ❌ (View Rooms) |

**Pagination:** Server-side · 25/page.

---

### 5.3 Trend Chart — Occupancy Over Time

**Chart 1 — Monthly Occupancy Rate (12 months)**
- Multi-line: Boys Occupancy % · Girls Occupancy % · AC % · Non-AC %
- Target line at 85% (group standard).
- X: Month. Y: %.

**Chart 2 — Capacity vs Occupancy by Branch (Top 10 / All)**
- Grouped bar: Total Beds vs Occupied per branch
- Toggle to show Boys / Girls / Combined.

---

### 5.4 Availability Summary

> Quick view of where seats are available — for admission decisions.

**Display:** Table — Branch | Boys AC Available | Boys Non-AC Available | Girls AC Available | Girls Non-AC Available | Total Available

Rows sorted by total available descending. Red cells when = 0.

[Allocate Seats →] → Page 16.

---

## 6. Drawers

### 6.1 Drawer: `hostel-occupancy-detail`
- **Trigger:** Branch occupancy card → [View Rooms →] or table → row
- **Width:** 640px
- **Tabs:** Overview · AC Rooms · Non-AC Rooms · On Leave · History
- **Overview:** Branch details, total capacity, current occupancy, reserved count
- **AC Rooms tab:** Room-by-room list with occupancy per room (bed A/B/C status)
- **Non-AC Rooms tab:** Same for non-AC
- **On Leave:** Hostelers on approved leave (temporarily vacating beds)
- **History:** Occupancy trend for this campus (12 months)

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Manual refresh | "Occupancy data refreshed." | Info | 3s |
| Export triggered | "Occupancy report export started." | Info | 4s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No hostels configured | "No Hostel Campuses Found" | "No hostel campuses have been configured." | [Contact IT Admin] |
| All beds occupied | "All Hostel Seats Occupied" | "Every configured hostel bed is filled. No seats available." | [View Waitlist] |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page load | Skeleton: 8 KPI cards + heatmap grid (12 placeholder cards) + table |
| KPI auto-refresh | Shimmer on card values + progress bars |
| Filter apply | Table body skeleton |
| Branch detail drawer | Centred spinner; room tabs load lazily |

---

## 10. Role-Based UI Visibility

| Element | Hostel Director G3 | Boys Coord G3 | Girls Coord G3 | Admission Coord G3 | Fee Manager G3 |
|---|---|---|---|---|---|
| Boys hostel data | ✅ | ✅ | ❌ | ✅ | ✅ |
| Girls hostel data | ✅ | ❌ | ✅ | ✅ | ✅ |
| Availability summary | ✅ | ✅ Boys | ✅ Girls | ✅ All | ✅ All |
| Export | ✅ | ✅ Boys | ✅ Girls | ✅ | ✅ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/hostel/occupancy/` | JWT (G3+) | Full occupancy data |
| GET | `/api/v1/group/{group_id}/hostel/occupancy/kpis/` | JWT (G3+) | KPI auto-refresh |
| GET | `/api/v1/group/{group_id}/hostel/occupancy/branches/` | JWT (G3+) | Branch table (filtered) |
| GET | `/api/v1/group/{group_id}/hostel/occupancy/branches/{id}/` | JWT (G3+) | Branch room detail |
| GET | `/api/v1/group/{group_id}/hostel/occupancy/availability/` | JWT (G3+) | Availability summary |
| GET | `/api/v1/group/{group_id}/hostel/occupancy/trends/` | JWT (G3+) | 12-month trend data |
| GET | `/api/v1/group/{group_id}/hostel/occupancy/export/` | JWT (G3+) | Export occupancy report |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-get/post | hx-target | hx-swap |
|---|---|---|---|---|
| KPI auto-refresh | `every 10m` | GET `.../occupancy/kpis/` | `#kpi-bar` | `innerHTML` |
| Heatmap auto-refresh | `every 10m` | GET `.../occupancy/heatmap/` | `#occupancy-heatmap` | `innerHTML` |
| Branch filter | `click` | GET `.../occupancy/branches/?{filters}` | `#occupancy-table-section` | `innerHTML` |
| Open branch detail | `click` | GET `.../occupancy/branches/{id}/` | `#drawer-body` | `innerHTML` |
| Manual refresh | `click` on Refresh ↻ | GET `.../occupancy/kpis/` | `#kpi-bar` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
