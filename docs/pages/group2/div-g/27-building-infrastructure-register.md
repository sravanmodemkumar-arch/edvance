# 27 — Building Infrastructure Register

> **URL:** `/group/ops/facilities/buildings/`
> **File:** `27-building-infrastructure-register.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Roles:** COO G4 (full CRUD) · Operations Manager G3 (view + update condition) · Zone Dir G4 (zone view)

---

## 1. Purpose

Master register of all buildings and major infrastructure assets across all group campuses.
Documents ownership, dimensions, condition ratings, renovation history, and open maintenance
issues per building. Forms the basis for CAPEX planning and safety compliance.

---

## 2. Page Layout

### 2.1 Breadcrumb
```
Group HQ  ›  Facilities  ›  Building Register
```

### 2.2 Summary Strip
| Card | Value |
|---|---|
| Total Buildings | `186` across 50 branches |
| Owned | `142 (76%)` |
| Leased | `44 (24%)` |
| Poor Condition | Count (red if >0) |
| Leases Expiring 90d | Count |

---

## 3. Filters & Search

**Search:** Building name, branch, city. 300ms debounce.
**Filters:** Branch · Zone · Building Type · Ownership · Condition · Lease expiring.

---

## 4. Building Table

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| Building Name | ✅ | Link → `building-detail` drawer |
| Branch | ✅ | |
| Type | ✅ | Classroom Block · Admin · Hostel · Lab · Sports · Library · Multipurpose |
| Ownership | ✅ | Own / Leased / Government |
| Floor Area (sq ft) | ✅ | |
| Floors | ✅ | |
| Year Built | ✅ | |
| Last Renovation | ✅ | |
| Condition | ✅ | Good (green) / Fair (yellow) / Poor (red) |
| Open Issues | ✅ | Count maintenance tickets |
| Lease Expiry | ✅ | Red if <90d (leased only) |
| Actions | — | View · Edit · Upload Document |

**Pagination:** 25/page.

---

## 5. Building Create/Edit Drawer

- **Width:** 600px
- **Tabs:** Details · Ownership · Documents · Condition

**Details:** Building name · Branch · Building type · Year built · Floor area · Number of floors · Number of classrooms/rooms.

**Ownership:** Own / Leased / Government. If leased: Lessor name, lease start, lease end, monthly rent, contact.

**Documents:** Property deed / Lease agreement / Building plan / Occupancy certificate.

**Condition:** Condition rating (Good/Fair/Poor) · Last inspection date · Notes.

---

## 6. Building Detail Drawer

- **Width:** 640px
- **Tabs:** Overview · Maintenance · Documents · Renovation History

**Overview:** All building details. Condition rating with history.

**Maintenance:** Open and recent tickets for this building.

**Documents:** All uploaded documents with view/download.

**Renovation History:** Past renovation projects with dates, costs, descriptions.

---

## 7. Condition Update Modal

- **Width:** 420px
- Trigger: Building row → [Update Condition]
- Fields: New Condition rating · Inspection Date · Notes · Inspector Name

---

## 8. Toast / Empty / Loader

Standard. Skeleton: summary + table.

---

## 9. Role-Based UI Visibility

| Element | COO G4 | Ops Mgr G3 | Zone Dir G4 |
|---|---|---|---|
| [+ Add Building] | ✅ | ❌ | ❌ |
| [Edit] | ✅ | ❌ | ❌ |
| [Update Condition] | ✅ | ✅ | ❌ |
| [Upload Document] | ✅ | ✅ | ❌ |
| Lease/ownership details | ✅ | ✅ | ❌ |

---

## 10. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/facilities/buildings/` | JWT (G3+) | Building list |
| POST | `/api/v1/group/{id}/facilities/buildings/` | JWT (G4) | Create |
| PUT | `/api/v1/group/{id}/facilities/buildings/{bid}/` | JWT (G4) | Edit |
| GET | `/api/v1/group/{id}/facilities/buildings/{bid}/` | JWT (G3+) | Detail |
| POST | `/api/v1/group/{id}/facilities/buildings/{bid}/condition/` | JWT (G3+) | Update condition |
| POST | `/api/v1/group/{id}/facilities/buildings/{bid}/documents/` | JWT (G3+) | Upload document |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
