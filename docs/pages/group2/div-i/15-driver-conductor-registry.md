# 15 — Driver & Conductor Registry

> **URL:** `/group/transport/staff/`
> **File:** `15-driver-conductor-registry.md`
> **Template:** `portal_base.html`
> **Priority:** P0
> **Role:** Group Fleet Manager (primary) · Transport Safety Officer · Transport Director

---

## 1. Purpose

Master searchable registry of all drivers and conductors across every branch. Each record links to their licence details, BGV status, training records, route assignment, duty status, and incident history. Drivers and conductors are synced from the external HRMS (see Page 05) and managed on the EduForge side for compliance, assignment, and safety monitoring.

Drivers carry the most critical responsibility in the transport chain — they are directly responsible for student safety. Every driver must have a valid commercial/PSV licence, passed BGV, and be current on road safety training before they are permitted to operate a school bus.

Scale: 500–1,000 drivers + 300–600 conductors across 20–50 branches.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Fleet Manager | G3 | Full — edit assignment, update compliance | Primary owner |
| Group Transport Director | G3 | Full view + approve suspensions | Oversight |
| Group Transport Safety Officer | G3 | Read + flag safety concern | Safety flag only |
| Branch Transport In-Charge | Branch G3 | View own branch staff | Cannot edit |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Transport Management  ›  Driver & Conductor Registry
```

### 3.2 Page Header
- **Title:** `Driver & Conductor Registry`
- **Subtitle:** `[N] Drivers · [N] Conductors · [N] Active Routes · AY [current]`
- **Right controls:** `Advanced Filters` · `Export` · `Trigger Sync ↻` (syncs from HRMS)

### 3.3 Alert Banner

| Condition | Banner Text | Severity |
|---|---|---|
| Drivers with expired licence | "[N] drivers have expired driving licences. Cannot operate." | Red |
| Drivers on duty with expired licence | "[N] drivers are currently on duty with an expired licence." | Red |
| BGV not completed | "[N] drivers/conductors have incomplete BGV." | Amber |
| Training overdue > 1 year | "[N] drivers have not completed annual road safety training." | Amber |
| Route assignments gap | "[N] active routes have no driver assigned for tomorrow." | Amber |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule |
|---|---|---|
| Total Drivers | Active drivers | Blue |
| Total Conductors | Active conductors | Blue |
| Licence Non-Compliant | Expired/missing | Red > 0 · Green = 0 |
| BGV Incomplete | Not completed | Yellow > 0 |
| Training Overdue | Annual road safety overdue | Yellow > 0 |
| On Duty Today | Drivers active right now | Blue |

---

## 5. Main Table — Staff Registry

**Tabs:** All · Drivers · Conductors

**Search:** Name, employee ID, licence number, branch. 300ms debounce.

**Advanced Filters:**
| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Role | Radio | All / Driver / Conductor |
| Status | Checkbox | Active / On Leave / Suspended / Resigned |
| Licence Status | Radio | All / Valid / Expiring (≤30d) / Expired |
| BGV Status | Radio | All / Cleared / Pending / Failed |
| Training | Radio | All / Current / Overdue |
| Route Assignment | Checkbox | Assigned / Unassigned |

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| Photo | ❌ | Thumbnail or avatar |
| Name | ✅ | Link → staff detail drawer |
| Employee ID | ✅ | |
| Role | ✅ | Driver / Conductor badge |
| Branch | ✅ | |
| Route Assigned | ✅ | Route name · or — |
| Licence No | ✅ | |
| Licence Type | ✅ | LMV / HMV / PSV |
| Licence Expiry | ✅ | Colour-coded |
| BGV Status | ✅ | ✅ Cleared · ⏳ Pending · ❌ Failed |
| Training Status | ✅ | ✅ Current · ⚠ Due Soon · 🔴 Overdue |
| Status | ✅ | Active / On Leave / Suspended |
| Actions | ❌ | View · Edit · Suspend · Assign Route |

**Bulk actions:** Export selected · Bulk send training reminder.
**Pagination:** Server-side · 25/page.

---

## 6. Drawers

### 6.1 Drawer: `staff-detail` — View
- **Width:** 640px
- **Tabs:** Profile · Licence · BGV · Training · Route · Incidents · History
- **Profile:** Photo, name, ID, role, branch, joining date, contact, emergency contact
- **Licence:** Licence number, type, issue date, expiry, issuing authority, scan document
- **BGV:** BGV vendor, submission date, clearance date, status, notes
- **Training:** All training records — road safety, first aid, defensive driving (Page 17)
- **Route:** Current route assignment, duty history (last 30 days)
- **Incidents:** All incidents where this driver was involved (Page 23)
- **History:** Status changes, branch transfers, suspensions

### 6.2 Drawer: `edit-staff`
- **Width:** 640px (same tabs as view, pre-populated)
- **Editable:** Branch · Route Assignment · Status · Emergency Contact
- **Read-only (comes from HRMS sync):** Name · Employee ID · Licence Number

### 6.3 Drawer: `assign-route`
- **Trigger:** Actions → Assign Route
- **Width:** 480px
- **Fields:** Driver/Conductor Name · Branch · Route (searchable — shows current driver assignment) · Effective Date · Duty Type (Morning / Afternoon / Both) · Notes
- **Validation:** Cannot assign driver with expired licence · Cannot assign to route in different branch without Director approval

> **Audit trail:** All write actions (route assignment, suspension, status changes) are logged to [Transport Audit Log → Page 33] with user, timestamp, and IP.

### 6.4 Modal: `suspend-staff`
- **Trigger:** Actions → Suspend
- **Width:** 480px
- **Fields:** Reason (Expired Licence / Incident Involvement / Misconduct / Medical Reason / Other) · Effective Date · Expected Reinstatement Date (optional) · Notify Branch (checkbox) · Notes
- **Warning:** "Driver's route will have no driver assigned. Please arrange replacement."

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Record synced | "Driver/conductor data synced from HRMS. [N] records updated." | Info | 4s |
| Sync failed | "HRMS sync failed. Check integration configuration and retry." | Error | 5s |
| Route assigned | "[Name] assigned to Route [Name]." | Success | 4s |
| Route assignment failed | "Failed to assign route. Check driver licence compliance or route availability." | Error | 5s |
| Staff suspended | "[Name] suspended. Branch transport in-charge notified." | Warning | 6s |
| Suspension failed | "Failed to suspend staff record. Please retry." | Error | 5s |
| Training reminder sent | "Road safety training reminder sent to [N] staff." | Info | 4s |
| Reminder failed | "Failed to send training reminders. Please retry." | Error | 5s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No staff records | "No Driver/Conductor Records" | "Sync from HRMS to populate the registry." | [Trigger Sync ↻] |
| No compliance issues | "All Staff Compliant" | "All drivers have valid licences, cleared BGV, and current training." | — |
| No filter results | "No Staff Match Filters" | "Adjust branch, role, or status filters." | [Clear Filters] |
| No search results | "No Staff Found for '[term]'" | "Check the name, employee ID, or licence number." | [Clear Search] |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page load | Skeleton: 6 KPI cards + table (15 rows × 13 columns) |
| Filter/search | Table body skeleton |
| Staff detail drawer | 640px skeleton; tabs load lazily |
| HRMS sync trigger | Spinner + "Syncing…" overlay for 3–10 seconds |

---

## 10. Role-Based UI Visibility

| Element | Fleet Manager G3 | Transport Director G3 | Safety Officer G3 |
|---|---|---|---|
| Edit Staff Record | ✅ | ❌ | ❌ |
| Assign Route | ✅ | ✅ | ❌ |
| Suspend Staff | ✅ (propose) | ✅ (execute) | ❌ |
| Trigger HRMS Sync | ✅ | ✅ | ❌ |
| Flag Safety Concern | ✅ | ✅ | ✅ |
| Export | ✅ | ✅ | ✅ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/transport/staff/` | JWT (G3+) | Paginated staff list |
| GET | `/api/v1/group/{group_id}/transport/staff/{id}/` | JWT (G3+) | Staff full profile |
| PATCH | `/api/v1/group/{group_id}/transport/staff/{id}/` | JWT (G3+) | Update editable fields |
| POST | `/api/v1/group/{group_id}/transport/staff/{id}/assign-route/` | JWT (G3+) | Assign route |
| POST | `/api/v1/group/{group_id}/transport/staff/{id}/suspend/` | JWT (G3+) | Suspend |
| POST | `/api/v1/group/{group_id}/transport/drivers/sync/` | JWT (G3+) | Trigger HRMS sync |
| GET | `/api/v1/group/{group_id}/transport/staff/kpis/` | JWT (G3+) | KPI cards |
| GET | `/api/v1/group/{group_id}/transport/staff/export/` | JWT (G3+) | Export |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-get/post | hx-target | hx-swap |
|---|---|---|---|---|
| Search | `input delay:300ms` | GET `.../staff/?q={val}` | `#staff-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../staff/?{filters}` | `#staff-table-section` | `innerHTML` |
| Tab switch (Drivers/Conductors) | `click` | GET `.../staff/?role={type}` | `#staff-table-section` | `innerHTML` |
| Open detail drawer | `click` on Name | GET `.../staff/{id}/` | `#drawer-body` | `innerHTML` |
| Sort | `click` on header | GET `.../staff/?sort={col}&dir={asc/desc}` | `#staff-table-section` | `innerHTML` |
| Pagination | `click` | GET `.../staff/?page={n}` | `#staff-table-section` | `innerHTML` |
| Assign route submit | `click` | POST `.../staff/{id}/assign-route/` | `#staff-row-{id}` | `outerHTML` |
| Suspend confirm | `click` | POST `.../staff/{id}/suspend/` | `#staff-row-{id}` | `outerHTML` |
| Export | `click` | GET `.../staff/export/` | `#export-btn` | `outerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
