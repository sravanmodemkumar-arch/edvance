# 14 — Student Transport Allocation

> **URL:** `/group/transport/students/`
> **File:** `14-student-transport-allocation.md`
> **Template:** `portal_base.html`
> **Priority:** P0
> **Role:** Group Route Planning Manager (primary) · Transport Fee Manager · Transport Safety Officer (view)

---

## 1. Purpose

Master register of all day-scholar students enrolled in group transport, their route assignment, pickup/drop stop, bus pass status, and fee plan. This page is the link between the student academic record and the transport system.

Day scholars who use transport must be allocated to a route and stop. Their allocation drives the fee plan (via route → fee structure), the bus pass, GPS boarding notifications, and parent WhatsApp alerts. This page manages all those linkages.

Note: Hostelers are NOT included — they live on campus and do not use transport.

Scale: 3,000–15,000 day scholars on transport across all branches.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Route Planning Manager | G3 | Full — allocate, reassign, remove | Primary owner |
| Group Transport Fee Manager | G3 | Read — fee plan view + bus pass management | View route; manage fee/pass |
| Group Transport Safety Officer | G3 | Read — student safety context | View only |
| Branch Transport In-Charge | Branch G3 | View + allocate own branch students | Branch-scoped |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Transport Management  ›  Student Transport Allocation
```

### 3.2 Page Header
- **Title:** `Student Transport Allocation`
- **Subtitle:** `[N] Students on Transport · [N] Unallocated · [N] Branches · AY [current]`
- **Right controls:** `+ Allocate Student` · `Bulk Allocate ↑` · `Advanced Filters` · `Export`

### 3.3 Alert Banner

| Condition | Banner Text | Severity |
|---|---|---|
| Unallocated day scholars | "[N] day scholars have transport opted-in but no route assigned." | Red |
| Students on overloaded route | "[N] students are on routes that exceed vehicle capacity." | Red |
| Bus passes expiring within 7 days | "[N] student bus passes expire within 7 days." | Amber |
| Fee not linked | "[N] students on transport have no fee plan linked." | Amber |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule |
|---|---|---|
| Total Students on Transport | Allocated to any route | Blue |
| Unallocated Students | Transport opted-in, no route | Red > 0 · Green = 0 |
| Bus Passes Active | Currently valid | Blue |
| Bus Passes Expired | Need renewal | Yellow > 0 |
| Overloaded Route Students | On over-capacity buses | Red > 0 · Green = 0 |
| Fee Plan Linked | % with transport fee assigned | Green = 100% · Red < 100% |

---

## 5. Main Table — Student Transport Register

**Search:** Student name, roll number, route, stop, branch. 300ms debounce.

**Advanced Filters:**
| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Class | Multi-select | 1–12 |
| Route | Multi-select | All routes |
| Bus Pass Status | Radio | All / Active / Expired / Not Issued |
| Fee Status | Radio | All / Linked / Missing |
| Allocation Status | Radio | All / Allocated / Unallocated |

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| Student Name | ✅ | Link → student transport detail drawer |
| Roll No | ✅ | Branch-assigned |
| Class | ✅ | |
| Branch | ✅ | |
| Route | ✅ | Route name · or "Unallocated ❌" |
| Pickup Stop | ✅ | Stop name |
| Drop Stop | ✅ | Stop name (if different) |
| Bus No | ✅ | Assigned vehicle |
| Bus Pass | ✅ | Pass No + Expiry · or "Not Issued" |
| Fee Plan | ✅ | ✅ Linked · ❌ Missing |
| Actions | ❌ | View · Edit Allocation · Remove from Transport |

**Bulk actions:** Bulk assign to route · Bulk issue bus pass · Bulk export.
**Pagination:** Server-side · 25/page.

---

## 6. Drawers

### 6.1 Drawer: `student-transport-detail` — View
- **Width:** 600px
- **Tabs:** Allocation · Fee · Bus Pass · GPS History
- **Allocation:** Route, stop, bus, allocation date, history of route changes
- **Fee:** Transport fee plan, monthly amount, collection status
- **Bus Pass:** Pass number, issue date, expiry, renewal history
- **GPS History:** Last 30 days — boarding/alighting events, missed boarding alerts

### 6.2 Drawer: `allocate-student`
- **Trigger:** + Allocate Student
- **Width:** 540px
- **Fields:** Branch · Student (searchable by name/roll) · Route (searchable — shows capacity status) · Pickup Stop (dropdown, filtered by route) · Drop Stop (optional — if different from pickup) · Effective Date
- **Validation:** Route capacity check (warn if adding student will overload route) · Student must be day scholar (not hosteler)

### 6.3 Drawer: `edit-allocation`
- **Trigger:** Actions → Edit Allocation
- **Width:** 540px (same as allocate, pre-populated)
- Changing route triggers fee plan update prompt

> **Audit trail:** All write actions (allocate, update allocation, remove from transport) are logged to [Transport Audit Log → Page 33] with user, timestamp, and IP.

### 6.4 Modal: `remove-from-transport`
- **Width:** 480px
- **Fields:** Effective Date · Reason (Opted Out / Branch Transfer / Academic Exit / Other) · Cancel Bus Pass (checkbox) · Refund Remaining Term Fee (checkbox)
- **Warning:** "Student will be removed from transport. Bus pass will be cancelled if selected."

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Student allocated | "[Name] allocated to Route [Name] — Stop [Stop Name]." | Success | 4s |
| Allocation failed | "Failed to allocate student. Check route capacity and student eligibility (day scholar only)." | Error | 5s |
| Allocation updated | "[Name]'s transport allocation updated." | Info | 4s |
| Update failed | "Failed to update allocation. Please retry." | Error | 5s |
| Removed from transport | "[Name] removed from transport. Bus pass cancelled." | Info | 5s |
| Removal failed | "Failed to remove student from transport. Please retry." | Error | 5s |
| Overload warning | "Warning: Route [Name] is at [N]% capacity after this allocation." | Warning | 6s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No students on transport | "No Students on Transport" | "Allocate students to routes to start tracking." | [+ Allocate Student] |
| No filter results | "No Students Match Filters" | "Adjust branch, class, route, or pass status filters." | [Clear Filters] |
| No search results | "No Students Found for '[term]'" | "Check the student name, roll number, or route." | [Clear Search] |
| No unallocated students | "All Students Allocated" | "All transport-enrolled students have a route assigned." | — |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page load | Skeleton: 6 KPI cards + table (15 rows × 11 columns) |
| Filter/search | Table body skeleton |
| Student detail drawer | 600px skeleton; tabs load lazily |

---

## 10. Role-Based UI Visibility

| Element | Route Planning Mgr G3 | Fee Manager G3 | Safety Officer G3 |
|---|---|---|---|
| Allocate Student | ✅ | ❌ | ❌ |
| Edit Allocation | ✅ | ❌ | ❌ |
| Remove from Transport | ✅ | ❌ | ❌ |
| Issue / Renew Bus Pass | ❌ | ✅ | ❌ |
| View All Students | ✅ | ✅ | ✅ |
| Export | ✅ | ✅ | ✅ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/transport/students/` | JWT (G3+) | Paginated student list |
| GET | `/api/v1/group/{group_id}/transport/students/{id}/` | JWT (G3+) | Student transport detail |
| POST | `/api/v1/group/{group_id}/transport/students/` | JWT (G3+) | Allocate student |
| PATCH | `/api/v1/group/{group_id}/transport/students/{id}/` | JWT (G3+) | Update allocation |
| POST | `/api/v1/group/{group_id}/transport/students/{id}/remove/` | JWT (G3+) | Remove from transport |
| GET | `/api/v1/group/{group_id}/transport/students/kpis/` | JWT (G3+) | KPI cards |
| GET | `/api/v1/group/{group_id}/transport/students/export/` | JWT (G3+) | Export |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-get/post | hx-target | hx-swap |
|---|---|---|---|---|
| Search | `input delay:300ms` | GET `.../students/?q={val}` | `#student-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../students/?{filters}` | `#student-table-section` | `innerHTML` |
| Open detail drawer | `click` on Name | GET `.../students/{id}/` | `#drawer-body` | `innerHTML` |
| Sort | `click` on header | GET `.../students/?sort={col}&dir={asc/desc}` | `#student-table-section` | `innerHTML` |
| Pagination | `click` | GET `.../students/?page={n}` | `#student-table-section` | `innerHTML` |
| Allocate submit | `click` | POST `.../students/` | `#student-table-section` | `innerHTML` |
| Remove confirm | `click` | POST `.../students/{id}/remove/` | `#student-row-{id}` | `outerHTML` |
| Export | `click` | GET `.../students/export/` | `#export-btn` | `outerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
