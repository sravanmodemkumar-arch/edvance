# 09 — Branch Coordinator Hub

> **URL:** `/group/ops/coordinators/`
> **File:** `09-branch-coordinator-hub.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** COO G4 (full) · Operations Manager G3 (full) · Branch Coordinator G3 (view own profile only)

---

## 1. Purpose

Central hub for managing Group Branch Coordinators — their assignments, performance, task
load, and communication activity. Ops Manager and COO use this to:
- Assign coordinators to branches
- Monitor coordinator workload and visit completion
- Identify coordinators with overdue tasks or coverage gaps
- Review coordinator field reports

---

## 2. Role Access

| Role | Access |
|---|---|
| COO G4 | Full — all coordinators, assign/unassign |
| Operations Manager G3 | Full — all coordinators |
| Branch Coordinator G3 | View own profile + performance only (no others) |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Operations  ›  Branch Coordinator Hub
```

### 3.2 Page Header
```
Branch Coordinator Hub                 [+ Add Coordinator]  [Export Performance ↓]
[N] coordinators · [N] branches covered · [N] unassigned branches
```

### 3.3 Summary Strip
| Card | Value |
|---|---|
| Total Coordinators | `18` |
| Branches Covered | `50 / 50` (red if < 100%) |
| Avg Branches per Coordinator | `2.8` |
| Visits Completed This Month | `82 / 120 planned (68%)` |
| Overdue Visits | `14` (red if >0) |

---

## 4. Coordinator Table

**Search:** Coordinator name, email. 300ms debounce.

**Advanced Filters:**
| Filter | Options |
|---|---|
| Zone | Multi-select |
| Workload | Under-assigned (<2 branches) · Normal (2–4) · Overloaded (>4) |
| Visit Compliance | On Track · Overdue |
| Status | Active · On Leave · Inactive |

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| ☐ | Checkbox | Row select |
| Coordinator Name | ✅ | Opens `coordinator-detail` drawer |
| Employee ID | ✅ | |
| Zone | ✅ | Assigned zone (large groups) |
| Branches Assigned | ✅ | Count · click → branch list |
| Visits Planned | ✅ | This month |
| Visits Completed | ✅ | This month + % |
| Issues Raised | ✅ | Total open issues from this coordinator |
| Last Field Visit | ✅ | Date · red if >30d |
| Status | ✅ | Active · On Leave · Inactive |
| Actions | — | View · Edit Assignment · View Schedule · View Reports |

**Pagination:** Server-side · 25/page · 10/25/50/All.

**Bulk actions (COO/Ops Mgr):** Reassign branches · Export performance CSV.

---

## 5. Branch Coverage Map

> Shows which branches have coordinators assigned and which don't.

**Display:** Two-column section:
- Left: Covered Branches (table — Branch Name · Coordinator · Last Visit · Next Visit)
- Right: Unassigned Branches (table — Branch Name · Zone · Days Without Coordinator · [Assign Now →])

**Alert:** Red banner if any branch has been unassigned for >7 days.

---

## 6. Performance Metrics Section

> Month-to-date performance comparison across all coordinators.

**Display:** Sortable table.

| Column | Notes |
|---|---|
| Coordinator | Name |
| Visit Completion % | Completed / Planned |
| Issues Raised | Count |
| Issues Resolved | Count |
| Messages Sent | To principals |
| Compliance Improved | Branches where compliance improved after visit |
| Performance Score | Composite (0–100) |

**Chart:** Bar chart — Visit Completion % per coordinator, sorted descending.

---

## 7. Coordinator Detail Drawer

- **Width:** 640px
- **Tabs:** Profile · Assignments · Visit Schedule · Performance · Reports

**Profile tab:** Name · Employee ID · Contact · Zone · Manager · Join date · Status

**Assignments tab:**
- Branches assigned (table: Branch Name · Type · City · Last Visit · Compliance Score)
- [Reassign Branch] button (COO/Ops Mgr)
- [Add Branch] button (COO/Ops Mgr)
- [Remove Branch] button (COO/Ops Mgr)

**Visit Schedule tab:**
- Upcoming visits (calendar mini-view + list)
- Past visits with completion status
- Overdue visits highlighted red

**Performance tab:**
- Monthly visit completion rate (last 6 months bar chart)
- Issues raised vs resolved trend
- Avg compliance improvement post-visit

**Reports tab:**
- All submitted visit reports (sortable by date, branch, rating)
- [View Report] → opens report detail within drawer

---

## 8. Coordinator Assignment Drawer

- **Width:** 480px
- **Trigger:** Row → Edit Assignment or Unassigned Branch → [Assign Now]
- **Fields:**
  - Coordinator: searchable select (shows name, current branch count, zone)
  - Branches: multi-select (filtered to same zone or "unassigned" branches)
  - Effective Date: date picker
  - Notes: optional
- **Validation:** Cannot assign coordinator from Zone A to a branch in Zone B (large groups)

---

## 9. Toast Messages

| Action | Toast | Type |
|---|---|---|
| Assignment saved | "Coordinator assigned to [Branch Name]" | Success · 4s |
| Assignment removed | "[Coordinator] unassigned from [Branch]" | Warning · 6s |
| Bulk reassign done | "Branches reassigned successfully" | Success · 4s |
| Export triggered | "Performance export started" | Info · 4s |

---

## 10. Empty States

| Condition | Heading | CTA |
|---|---|---|
| No coordinators | "No coordinators added yet" | [+ Add Coordinator] |
| No unassigned branches | "All branches have coordinators" | — |
| No visits this month | "No visits scheduled this month" | [Schedule Visits] |

---

## 11. Loader States

| Trigger | Loader |
|---|---|
| Page load | Skeleton summary strip + coordinator table (5 rows) + coverage section |
| Table filter | Inline skeleton rows |
| Drawer open | Spinner in drawer |
| Performance chart | Chart area spinner |

---

## 12. Role-Based UI Visibility

| Element | COO G4 | Ops Mgr G3 | Coordinator G3 |
|---|---|---|---|
| All coordinators table | ✅ | ✅ | ❌ (own profile via dashboard) |
| [+ Add Coordinator] | ✅ | ✅ | ❌ |
| [Reassign Branch] | ✅ | ✅ | ❌ |
| [Remove Branch] | ✅ | ✅ | ❌ |
| Export Performance | ✅ | ✅ | ❌ |
| Performance table | ✅ | ✅ | Own row only |

---

## 13. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/ops/coordinators/` | JWT (G3+) | Coordinator list |
| GET | `/api/v1/group/{id}/ops/coordinators/{coord_id}/` | JWT (G3+) | Coordinator detail |
| POST | `/api/v1/group/{id}/ops/coordinators/{coord_id}/assign/` | JWT (G3+) | Assign branch |
| DELETE | `/api/v1/group/{id}/ops/coordinators/{coord_id}/assign/{branch_id}/` | JWT (G3+) | Remove branch |
| GET | `/api/v1/group/{id}/ops/coordinators/coverage/` | JWT (G3+) | Covered/unassigned branches |
| GET | `/api/v1/group/{id}/ops/coordinators/performance/` | JWT (G3+) | Performance table |
| GET | `/api/v1/group/{id}/ops/coordinators/export/?format=csv` | JWT (G3+) | Export performance |

---

## 14. HTMX Patterns

| Interaction | hx-trigger | hx-get/post | hx-target | hx-swap |
|---|---|---|---|---|
| Search | `input delay:300ms` | `/api/.../coordinators/?q={}` | `#coordinator-table-body` | `innerHTML` |
| Filter apply | `click` | `/api/.../coordinators/?filters={}` | `#coordinator-table-section` | `innerHTML` |
| Sort | `click` | `/api/.../coordinators/?sort={}` | `#coordinator-table-section` | `innerHTML` |
| Open detail | `click` | `/api/.../coordinators/{id}/` | `#drawer-body` | `innerHTML` |
| Assign submit | `click` | POST `/api/.../coordinators/{id}/assign/` | `#coordinator-row-{id}` | `outerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
