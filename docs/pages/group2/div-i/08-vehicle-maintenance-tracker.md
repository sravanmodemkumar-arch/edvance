# 08 — Vehicle Maintenance Tracker

> **URL:** `/group/transport/vehicles/maintenance/`
> **File:** `08-vehicle-maintenance-tracker.md`
> **Template:** `portal_base.html`
> **Priority:** P0
> **Role:** Group Fleet Manager (primary) · Transport Director (view)

---

## 1. Purpose

End-to-end maintenance lifecycle management for all group vehicles — scheduled servicing, breakdown repairs, tyre replacements, battery replacements (for electric buses), oil changes, and annual overhauls. Each maintenance event is logged against the vehicle record, with cost, workshop, parts, and downtime tracked.

Preventive maintenance is critical for student safety. An unserviced bus is a liability. The Fleet Manager uses this page to schedule upcoming service, track vehicles currently in the workshop, and ensure no vehicle operates beyond its service interval.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Fleet Manager | G3 | Full — schedule, log, close | Primary owner |
| Group Transport Director | G3 | View — maintenance summary | Approve budget overruns |
| Group Transport Safety Officer | G3 | Read — maintenance history for safety audits | View only |
| Branch Transport In-Charge | Branch G3 | View own branch vehicles | Cannot edit |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Transport Management  ›  Vehicle Maintenance Tracker
```

### 3.2 Page Header
- **Title:** `Vehicle Maintenance Tracker`
- **Subtitle:** `[N] Scheduled · [N] In Progress · [N] Overdue · [N] Completed (AY)`
- **Right controls:** `+ Schedule Maintenance` · `Advanced Filters` · `Export`

### 3.3 Alert Banner

| Condition | Banner Text | Severity |
|---|---|---|
| Overdue scheduled maintenance | "[N] vehicles have overdue scheduled maintenance." | Red |
| Vehicle in workshop > 7 days | "[Bus No] has been in workshop for > 7 days. Status update required." | Amber |
| Breakdown count > 5 in last 30 days | "High breakdown rate: [N] breakdowns in last 30 days across [N] branches." | Amber |
| Maintenance budget threshold exceeded | "Maintenance spend at [Branch] exceeded monthly threshold by [N]%." | Amber |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule |
|---|---|---|
| Scheduled This Month | Count | Blue |
| In Workshop Now | Vehicles currently under repair | Yellow > 0 · Red > 10 |
| Overdue | Past scheduled date, not done | Red > 0 · Green = 0 |
| Completed (This Month) | Closed maintenance events | Blue |
| Breakdown Events (This Month) | Unplanned repairs | Yellow > 3 · Red > 10 |
| Avg Workshop Downtime | Days per event | Yellow > 3 · Red > 7 |

---

## 5. Main Table — Maintenance Records

**Search:** Bus number, branch, workshop name. 300ms debounce.

**Advanced Filters:**
| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Status | Checkbox | Scheduled / In Progress / Completed / Overdue / Cancelled |
| Type | Checkbox | Scheduled Service / Breakdown Repair / Tyre / Oil Change / Battery / Annual Overhaul / Other |
| Date Range | Date picker | Service date range |

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| Bus No | ✅ | Link → vehicle detail (Page 07) |
| Branch | ✅ | |
| Maintenance Type | ✅ | |
| Scheduled Date | ✅ | |
| Completion Date | ✅ | Blank if in progress |
| Workshop | ✅ | |
| Mileage at Service | ✅ | km |
| Cost (₹) | ✅ | |
| Downtime (days) | ✅ | Calculated |
| Status | ✅ | Badge colour |
| Actions | ❌ | View · Edit · Close · Cancel |

**Pagination:** Server-side · 25/page.

---

## 6. Drawers

### 6.1 Drawer: `schedule-maintenance`
- **Trigger:** + Schedule Maintenance
- **Width:** 600px
- **Fields:** Bus No (searchable) · Branch (auto-filled) · Maintenance Type · Scheduled Date · Workshop Name · Workshop Location · Estimated Downtime (days) · Estimated Cost (₹) · Notes · Assign to driver (move bus away)
- **Validation:** Scheduled date must be future · Bus must be Active (not already Decommissioned)
- **On save:** Vehicle status changed to "Maintenance Scheduled" · Route Planning Manager notified if bus is route-assigned

> **Audit trail:** All write actions (schedule, update, close maintenance) are logged to [Transport Audit Log → Page 33] with user, timestamp, and IP.

### 6.2 Drawer: `maintenance-detail` — View / Edit
- **Trigger:** View or Edit in Actions
- **Width:** 600px
- **Fields (editable):** Actual Start Date · Completion Date · Actual Cost (₹) · Parts Replaced · Mileage · Workshop Name · Notes · Status update
- **On close (status = Completed):** Vehicle status reverts to Active; next service date auto-calculated based on mileage interval

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Maintenance scheduled | "Maintenance scheduled for [Bus No] on [date]." | Info | 4s |
| Schedule failed | "Failed to schedule maintenance. Check vehicle status and date." | Error | 5s |
| Maintenance completed | "[Bus No] maintenance completed. Vehicle marked Active." | Success | 4s |
| Close failed | "Failed to close maintenance record. Please retry." | Error | 5s |
| Maintenance updated | "Maintenance record updated for [Bus No]." | Info | 4s |
| Update failed | "Failed to update maintenance record. Please retry." | Error | 5s |
| Overdue alert sent | "Overdue maintenance reminder sent for [N] vehicles." | Warning | 5s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No maintenance records | "No Maintenance Records" | "Schedule the first maintenance event to start tracking." | [+ Schedule Maintenance] |
| No filter results | "No Records Match Filters" | "Adjust branch, status, or date range filters." | [Clear Filters] |
| No search results | "No Records Found for '[term]'" | "Check the bus number or workshop name." | [Clear Search] |
| Nothing overdue | "No Overdue Maintenance" | "All scheduled maintenance is on track." | — |
| No vehicles in workshop | "No Vehicles In Workshop" | "No vehicles are currently under maintenance." | — |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page load | Skeleton: 6 KPI cards + table skeleton |
| Filter/search | Table body skeleton |
| Schedule drawer | 600px drawer skeleton |
| Close maintenance confirm | Spinner on Confirm button |

---

## 10. Role-Based UI Visibility

| Element | Fleet Manager G3 | Transport Director G3 | Safety Officer G3 |
|---|---|---|---|
| Schedule Maintenance | ✅ | ✅ | ❌ |
| Edit Record | ✅ | ❌ | ❌ |
| Close Maintenance | ✅ | ❌ | ❌ |
| Approve Budget Overrun | ❌ | ✅ | ❌ |
| Export | ✅ | ✅ | ✅ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/transport/maintenance/` | JWT (G3+) | Paginated, filtered list |
| POST | `/api/v1/group/{group_id}/transport/maintenance/` | JWT (G3+) | Schedule maintenance |
| GET | `/api/v1/group/{group_id}/transport/maintenance/{id}/` | JWT (G3+) | Detail view |
| PATCH | `/api/v1/group/{group_id}/transport/maintenance/{id}/` | JWT (G3+) | Update record |
| POST | `/api/v1/group/{group_id}/transport/maintenance/{id}/close/` | JWT (G3+) | Mark completed |
| GET | `/api/v1/group/{group_id}/transport/maintenance/kpis/` | JWT (G3+) | KPI cards |
| GET | `/api/v1/group/{group_id}/transport/maintenance/export/` | JWT (G3+) | Async CSV/XLSX export |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-get/post | hx-target | hx-swap |
|---|---|---|---|---|
| Search | `input delay:300ms` | GET `.../maintenance/?q={val}` | `#maintenance-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../maintenance/?{filters}` | `#maintenance-table-section` | `innerHTML` |
| Sort | `click` on header | GET `.../maintenance/?sort={col}&dir={asc/desc}` | `#maintenance-table-section` | `innerHTML` |
| Pagination | `click` | GET `.../maintenance/?page={n}` | `#maintenance-table-section` | `innerHTML` |
| Schedule submit | `click` | POST `.../maintenance/` | `#maintenance-table-section` | `innerHTML` |
| Close confirm | `click` | POST `.../maintenance/{id}/close/` | `#row-{id}` | `outerHTML` |
| Export | `click` | GET `.../maintenance/export/` | `#export-btn` | `outerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
