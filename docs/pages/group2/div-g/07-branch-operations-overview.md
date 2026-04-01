# 07 — Branch Operations Overview

> **URL:** `/group/ops/branches/`
> **File:** `07-branch-operations-overview.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** COO G4 · Operations Manager G3 · Branch Coordinator G3 (own branches) · Zone Director G4 (zone branches) · Zone Academic Coord G3 (zone) · Zone Ops Mgr G3 (zone)

---

## 1. Purpose

Cross-branch operational health matrix. Shows every branch's operational status with metrics
the COO and Operations Manager use daily to identify branches needing intervention. The
primary data entry point for operational decision-making. Coordinators and zone roles see
their scoped subset.

---

## 2. Role Access

| Role | Level | Access |
|---|---|---|
| COO | G4 | All branches — full actions |
| Operations Manager | G3 | All branches — assign coordinator, raise escalation |
| Branch Coordinator | G3 | Own branches only — view |
| Zone Director | G4 | Zone branches only |
| Zone Academic Coord | G3 | Zone branches — academic cols only |
| Zone Ops Manager | G3 | Zone branches — ops cols only |

> **API scoping:** `?zone_id=`, `?coordinator_id=` appended server-side per user role. Coordinator sees
> only branches where `coordinator_id == current_user.id`.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Operations  ›  Branch Operations Overview
```

### 3.2 Page Header
```
Branch Operations Overview                [+ Assign Coordinator]  [Export CSV ↓]  [⚙ Columns]
Showing [N] branches · [N] active · [N] inactive
```

### 3.3 Summary Strip (above table)
4 mini-cards:
- Total Branches: `50` (active: `48` · inactive: `2`)
- Avg SLA Compliance: `92.4%`
- Branches with Open P1 Issues: `3`
- Coordinator Coverage: `100%`

---

## 4. Search & Filters

**Search:** Full-text across branch name, city, district, principal name. 300ms debounce. Highlights match.

**Advanced Filter Drawer:**
| Filter | Type | Options |
|---|---|---|
| Zone | Multi-select | All zones |
| State / District | Multi-select | |
| Branch Type | Multi-select | Day Scholar · Hostel · Both |
| Status | Multi-select | Active · Inactive · Onboarding |
| SLA Status | Select | Compliant (≥95%) · At Risk (85–94%) · Breached (<85%) |
| Coordinator | Select | All coordinators |
| Has P1 Issues | Checkbox | Show only branches with P1 escalations |
| Visit Overdue | Checkbox | Last visit >30 days |
| Compliance Score | Range slider | 0–100% |

Active filter chips: dismissible · "Clear All" · filter count badge on button.

---

## 5. Branch Operations Table

**Default sort:** SLA % ascending (worst first).

**Columns:**
| Column | Type | Sortable | Notes |
|---|---|---|---|
| ☐ | Checkbox | — | Row select + select-all |
| Branch Name | Text + link | ✅ | Opens `branch-ops-detail` drawer |
| City / State | Text | ✅ | |
| Zone | Badge | ✅ | Large groups only |
| Coordinator | Text | ✅ | Assigned name · "Unassigned" badge (red) if none |
| Type | Badge | ✅ | Day / Hostel / Both |
| Students | Number | ✅ | |
| SLA % | Progress + % | ✅ | Green/Yellow/Red |
| Open Escalations | Number badge | ✅ | Red if any P1 |
| Open Grievances | Number | ✅ | Orange if overdue |
| Maintenance Tickets | Number | ✅ | Red if any Critical |
| Last Visit | Date | ✅ | Red if >30 days |
| Compliance Score | Progress + % | ✅ | |
| Status | Badge | ✅ | Active · Inactive · Onboarding |
| Actions | — | ❌ | See below |

**Row actions (3-dot menu):**
| Action | Roles | Opens |
|---|---|---|
| View Details | All | `branch-ops-detail` drawer |
| Assign Coordinator | COO/Ops Mgr | `coordinator-assign` drawer |
| Schedule Visit | COO/Ops Mgr/Coordinator | `visit-schedule-create` drawer |
| Raise Escalation | COO/Ops Mgr/Coordinator | `escalation-create` drawer |
| Export Branch Report | COO/Ops Mgr | PDF download |

**Pagination:** Server-side · Default 25 · Selector 10/25/50/All · "Showing X–Y of Z" · Page jump.

**Column visibility toggle:** Gear icon top-right — show/hide any column.

**Bulk actions (COO/Ops Mgr only):**
| Action | Notes |
|---|---|
| Export Selected CSV | |
| Assign Coordinator (bulk) | Opens coordinator-assign drawer with multi-branch |
| Schedule Bulk Visit | Set same date/coordinator for selected branches |

---

## 6. Branch Ops Detail Drawer

> Opened from any row's View action or branch name click.

- **Width:** 640px
- **Tabs:** Ops Metrics · SLA · Coordinator · Escalations · Visit History · Compliance

**Ops Metrics tab:**
- Enrollment (total, day scholar, hosteler), Attendance %, Fee collection %
- Staff count, active staff, BGV %
- Transport (buses, route count if day scholar)

**SLA tab:**
- Per-metric SLA: Exam results published within X days · Grievance resolved within X days
- Breaches this month: count + details
- Trend: SLA % last 6 months (sparkline)

**Coordinator tab:**
- Assigned coordinator name, contact, assignment date
- Last visit date + report summary
- Next scheduled visit
- [Reassign Coordinator] button (COO/Ops Mgr only)

**Escalations tab:**
- All open escalations for this branch, sorted by priority
- [Raise New Escalation] button

**Visit History tab:**
- Last 10 visits: date, coordinator, type, report status (submitted/missing)
- [View Report] for each completed visit

**Compliance tab:**
- Checklist items: ✅/❌ status
- Last updated date
- [View Full Checklist →] → Page 13

---

## 7. Drawers & Modals

| Drawer | Trigger | Width | Description |
|---|---|---|---|
| `branch-ops-detail` | Row name click / View action | 640px | As detailed above |
| `coordinator-assign` | Assign action | 480px | Select coordinator · Start date · Notes |
| `visit-schedule-create` | Schedule Visit | 560px | Branch · Type · Date · Coordinator |
| `escalation-create` | Raise Escalation | 640px | Full escalation form |
| Bulk assign confirm | Bulk assign action | 420px modal | "Assign [N] branches to [Coordinator]?" |

---

## 8. Toast Messages

| Action | Toast | Type |
|---|---|---|
| Coordinator assigned | "Coordinator assigned to [Branch Name]" | Success · 4s |
| Visit scheduled | "Visit scheduled for [Date]" | Success · 4s |
| Escalation raised | "Escalation raised — Operations Manager notified" | Success · 4s |
| Export triggered | "Export started" | Info · 4s |
| Bulk assign done | "Coordinator assigned to [N] branches" | Success · 4s |

---

## 9. Empty States

| Condition | Heading | CTA |
|---|---|---|
| No branches | "No branches set up" | [Add Branch] (COO only) |
| No search results | "No branches match your search" | [Clear Filters] |
| Coordinator unassigned all | "No branches assigned to you" | Contact Ops Manager |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Page load | Skeleton: 4 summary cards + 5 table skeleton rows |
| Filter/search/page change | Inline skeleton rows (same column widths) |
| Row action (assign, schedule) | Spinner in drawer while loading |
| Bulk export | Progress toast notification |

---

## 11. Role-Based UI Visibility

| Element | COO G4 | Ops Mgr G3 | Coordinator G3 | Zone Dir G4 |
|---|---|---|---|---|
| All branches visible | ✅ | ✅ | ❌ own only | ❌ zone only |
| [Assign Coordinator] | ✅ | ✅ | ❌ | ❌ |
| [Raise Escalation] | ✅ | ✅ | ✅ | ✅ |
| [Schedule Visit] | ✅ | ✅ | ✅ | ✅ |
| Bulk actions | ✅ | ✅ | ❌ | ❌ |
| [Export CSV] | ✅ | ✅ | ❌ | ✅ |
| Finance columns (Fee %) | ✅ | ✅ | ❌ Hidden | ✅ |
| Column visibility gear | ✅ | ✅ | ✅ | ✅ |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/ops/branches/` | JWT (G3+) | Branch list — all filters, sort, paginate |
| GET | `/api/v1/group/{id}/ops/branches/{branch_id}/detail/` | JWT (G3+) | Branch ops detail drawer |
| POST | `/api/v1/group/{id}/ops/branches/{branch_id}/assign-coordinator/` | JWT (G3+) | Assign coordinator |
| POST | `/api/v1/group/{id}/ops/branches/bulk-assign-coordinator/` | JWT (G3+) | Bulk coordinator assign |
| GET | `/api/v1/group/{id}/ops/branches/export/?format=csv&filters={}` | JWT (G3+) | CSV export |
| GET | `/api/v1/group/{id}/ops/branches/summary/` | JWT (G3+) | 4 summary cards |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-get/post | hx-target | hx-swap |
|---|---|---|---|---|
| Search input | `input delay:300ms` | `/api/.../ops/branches/?q={}` | `#branch-table-body` | `innerHTML` |
| Filter apply | `click` | `/api/.../ops/branches/?filters={}` | `#branch-table-section` | `innerHTML` |
| Page change | `click` | `/api/.../ops/branches/?page={n}` | `#branch-table-section` | `innerHTML` |
| Sort click | `click` | `/api/.../ops/branches/?sort={col}&dir={asc/desc}` | `#branch-table-section` | `innerHTML` |
| Row name click | `click` | `/api/.../ops/branches/{id}/detail/` | `#drawer-body` | `innerHTML` |
| Coordinator assign submit | `click` | POST `/api/.../branches/{id}/assign-coordinator/` | `#branch-table-row-{id}` | `outerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
