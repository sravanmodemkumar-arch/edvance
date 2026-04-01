# 23 — Procurement Calendar

> **URL:** `/group/ops/procurement/calendar/`
> **File:** `23-procurement-calendar.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Roles:** COO G4 (full) · Operations Manager G3 (view)

---

## 1. Purpose

Annual procurement planning calendar showing when different categories of procurement
should happen. Helps the COO plan ahead for bulk purchases, ensuring items are ordered
with sufficient lead time before the academic year or term begins.

---

## 2. Standard Procurement Schedule

| Category | Planned Period | Lead Time | Notes |
|---|---|---|---|
| Textbooks (new year) | February–March | 45 days | Ordered before April new year |
| Uniforms | March–April | 30 days | Before new admissions |
| Lab Equipment | May–June | 60 days | After budget approval |
| IT Hardware (computers) | May–June | 30 days | Annual refresh cycle |
| Stationery (bulk) | Quarterly | 14 days | April, July, October, January |
| Sports Equipment | June–July | 21 days | Before sports season |
| Furniture | May–August | 45 days | Before new academic year |
| Hostel Supplies | March–April | 21 days | Before hostel reopening |
| Safety Equipment | Monthly | 7 days | Fire extinguishers, first aid |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Procurement  ›  Procurement Calendar
```

### 3.2 View Toggle
```
[Calendar View]  [List View]
```

---

## 4. Calendar View

**Display:** Full-year calendar (12-month grid or month-by-month navigation).

Each planned procurement event shown as a coloured bar spanning the procurement window.

**Colours per category:**
- Books: Blue
- Uniforms: Green
- Lab Equipment: Purple
- IT Hardware: Orange
- Stationery: Teal
- Sports: Red
- Furniture: Brown
- Hostel: Pink
- Safety: Grey

**Click on event bar:** Opens procurement event detail → allows creating procurement request from it.

---

## 5. List View (Upcoming Events)

**Columns:** Category · Planned Start · Planned End · Estimated Amount · Status (Planned/In Progress/Completed) · Linked POs · Actions (View · Create Request · Edit)

---

## 6. Create/Edit Procurement Event Drawer

- **Width:** 520px
- **Fields:** Category · Name · Start Date · End Date · Estimated Budget · Notes · Linked to which branches (all / specific)

---

## 7. Budget vs Planned Chart

**Type:** Horizontal bar — Planned budget per category. With "Spent so far" overlay.

---

## 8. Toast / Empty / Loader

Standard.

---

## 9. Role-Based UI Visibility

| Element | COO G4 | Ops Mgr G3 |
|---|---|---|
| [Create/Edit Event] | ✅ | ❌ |
| [Create Request] from event | ✅ | ✅ |
| View calendar | ✅ | ✅ |

---

## 10. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/procurement/calendar/` | JWT (G3+) | Calendar events |
| POST | `/api/v1/group/{id}/procurement/calendar/` | JWT (G4) | Create event |
| PUT | `/api/v1/group/{id}/procurement/calendar/{event_id}/` | JWT (G4) | Edit event |
| DELETE | `/api/v1/group/{id}/procurement/calendar/{event_id}/` | JWT (G4) | Delete event |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
