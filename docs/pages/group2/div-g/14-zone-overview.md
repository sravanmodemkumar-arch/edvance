# 14 — Zone Overview

> **URL:** `/group/ops/zones/`
> **File:** `14-zone-overview.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** COO G4 (full CRUD) · Operations Manager G3 (view) · Zone Directors G4 (own zone view)
> **Applicable:** Large groups only (20–50 branches with zone layer)

---

## 1. Purpose

Master view and configuration hub for the Group's zone structure. Large groups divide their
50 branches into 3–5 zones of 10–15 branches each. The COO creates zones, assigns Zone
Directors, and allocates branches. This page is the authority for zone structure management.

> Small groups (<10 branches) do not use zones. This page is hidden for small groups.

---

## 2. Role Access

| Role | Access |
|---|---|
| COO G4 | Full CRUD — create/edit zones, assign directors |
| Operations Manager G3 | View only |
| Zone Director G4 | View own zone, cannot create/edit zones |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Operations  ›  Zone Overview
```

### 3.2 Page Header
```
Zone Overview                          [+ Create Zone]  [Zone Report ↓]
[N] zones · [N] total branches · [N] unassigned branches
```

### 3.3 Summary Strip
| Card | Value |
|---|---|
| Total Zones | `4` |
| Total Branches | `50` |
| Unassigned Branches | Count (orange if >0) |
| Zone Directors Assigned | `4 / 4` (red if any missing) |

---

## 4. Zone Cards Grid

**Display:** Grid of zone cards (2 or 3 columns depending on count).

Each zone card:
```
[Zone Name]                     [Edit ✏] [View Details →]
Branches: [N] · Students: [N]
Zone Director: [Name]
Zone Acad Coord: [Name]
Zone Ops Manager: [Name]
SLA: [%]  Academic Score: [%]  Open Issues: [N]
[Branches List (collapsible)]
```

**Zone card colour border:**
- Green: SLA ≥95% + Academic ≥75%
- Yellow: SLA 85–94% or Academic 65–74%
- Red: SLA <85% or Academic <65%

---

## 5. Zone Details Table

> Tabular view of all zones for comparison.

**Columns:**
| Column | Sortable |
|---|---|
| Zone Name | ✅ |
| Zone Director | ✅ |
| Branches | ✅ |
| Students | ✅ |
| SLA Compliance | ✅ |
| Academic Score | ✅ |
| Open Escalations | ✅ |
| Compliance Score | ✅ |
| Actions | — (View Ops · View Academic · Edit) |

---

## 6. Unassigned Branches Panel

> Branches not yet allocated to any zone.

- Shows only when unassigned branches > 0
- Table: Branch Name · City · Students · [Assign to Zone →]

---

## 7. Zone Create/Edit Drawer

- **Width:** 560px
- **Fields:**
  | Field | Type | Validation |
  |---|---|---|
  | Zone Name | Text | Required · max 50 chars · unique within group |
  | Zone Code | Text | Optional · auto-generated if blank |
  | Zone Director | Searchable select (G4 staff) | Required |
  | Zone Academic Coordinator | Searchable select (G3 staff) | Optional |
  | Zone Operations Manager | Searchable select (G3 staff) | Optional |
  | Branches | Multi-select | Branches not already in another zone |
  | Description | Textarea | Optional |

- **Edit mode:** Shows current assignments, allows changes with audit logging
- **Delete zone:** Requires all branches to be reassigned first (validation error if branches exist in zone)

---

## 8. Zone Comparison Chart

**Type:** Grouped bar — SLA % and Academic Score per zone.

**Library:** Chart.js 4.x. Colorblind-safe. PNG export.

---

## 9. Toast Messages

| Action | Toast | Type |
|---|---|---|
| Zone created | "Zone [Name] created successfully" | Success · 4s |
| Zone updated | "Zone [Name] updated" | Success · 4s |
| Branch assigned | "Branch assigned to Zone [Name]" | Success · 4s |
| Zone deleted | "Zone deleted — [N] branches unassigned" | Warning · 6s |

---

## 10. Empty States

| Condition | Heading | CTA |
|---|---|---|
| No zones created | "No zones configured" | [+ Create Zone] (COO) |
| All branches assigned | "All branches allocated to zones" | — |

---

## 11. Loader States

Page load: Skeleton zone cards grid + summary strip.
Drawer open: Spinner in drawer.

---

## 12. Role-Based UI Visibility

| Element | COO G4 | Ops Mgr G3 | Zone Director G4 |
|---|---|---|---|
| All zones | ✅ | ✅ | Own zone only |
| [+ Create Zone] | ✅ | ❌ | ❌ |
| [Edit] on zone card | ✅ | ❌ | ❌ |
| [Assign Branch] | ✅ | ❌ | ❌ |
| Zone Report export | ✅ | ✅ | ✅ own |
| Comparison chart | ✅ | ✅ | ❌ (own zone only) |

---

## 13. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/zones/` | JWT (G3+) | All zones list |
| GET | `/api/v1/group/{id}/zones/summary/` | JWT (G3+) | Summary strip |
| POST | `/api/v1/group/{id}/zones/` | JWT (G4) | Create zone |
| PUT | `/api/v1/group/{id}/zones/{zone_id}/` | JWT (G4) | Edit zone |
| DELETE | `/api/v1/group/{id}/zones/{zone_id}/` | JWT (G4) | Delete zone |
| GET | `/api/v1/group/{id}/zones/unassigned-branches/` | JWT (G4) | Unassigned branches |
| POST | `/api/v1/group/{id}/zones/{zone_id}/assign-branch/` | JWT (G4) | Assign branch to zone |
| GET | `/api/v1/group/{id}/zones/comparison-chart/` | JWT (G3+) | Comparison chart data |

---

## 14. HTMX Patterns

| Interaction | hx-trigger | hx-get/post | hx-target | hx-swap |
|---|---|---|---|---|
| Open zone detail | `click` | `/api/.../zones/{id}/` | `#drawer-body` | `innerHTML` |
| Zone comparison chart | `load` | `/api/.../zones/comparison-chart/` | `#zone-chart` | `innerHTML` |
| Create zone submit | `click` | POST `/api/.../zones/` | `#zone-cards-grid` | `innerHTML` |
| Assign branch submit | `click` | POST `/api/.../zones/{id}/assign-branch/` | `#unassigned-panel` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
