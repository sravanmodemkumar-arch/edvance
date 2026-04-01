# 15 — Zone Operations Dashboard

> **URL:** `/group/ops/zones/<id>/ops/`
> **File:** `15-zone-operations-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** COO G4 (all zones) · Ops Manager G3 (all zones) · Zone Director G4 (own zone) · Zone Ops Manager G3 (own zone)

---

## 1. Purpose

Detailed operational KPI dashboard for a single zone. Shows SLA compliance, maintenance
status, grievance resolution, coordinator activity, transport, and facilities health for all
branches in the selected zone. Enables Zone Director and Zone Ops Manager to identify and
act on operational issues within their zone.

---

## 2. Role Access & Zone Scoping

| Role | Access |
|---|---|
| COO G4 | All zones — zone selector dropdown |
| Ops Manager G3 | All zones — zone selector dropdown |
| Zone Director G4 | Own zone only — no zone selector |
| Zone Ops Manager G3 | Own zone only — no zone selector |

**Zone selector:** Dropdown in page header (COO/Ops Mgr only) to switch between zones.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Operations  ›  Zones  ›  Zone [Name]  ›  Operations
```

### 3.2 Page Header
```
Zone [Name] — Operations Dashboard         [Zone Selector ▼]  [Export ↓]
[Zone Director Name] · [N] branches · [N] students · Academic Year [current]
```

### 3.3 Navigation Tabs (within zone)
```
[Operations]  [Academic →]  [Branch Health →]
```
— Operations tab is active on this page. Links to pages 16 and 17.

---

## 4. KPI Summary Bar (6 cards)

| Card | Metric | Drill-down |
|---|---|---|
| Zone SLA % | `89.1%` | → Page 08 filtered to zone |
| Maintenance Open | `11 tickets · 2 Critical` | → Page 26 filtered |
| Open Grievances | `4 · 1 overdue` | → Page 11 filtered |
| Coordinator Visits | `8 / 12 planned (67%)` | → Page 10 filtered |
| Facilities Compliance | `2 certs expiring` | → Page 30 filtered |
| Transport Issues | `1 route disruption` | Informational |

**HTMX:** `every 5m` → `/api/v1/group/{id}/zone/{zone_id}/ops/kpi-cards/` → `#kpi-bar`

---

## 5. Sections

### 5.1 Zone Branch Ops Table

**Columns:** Branch · SLA % · Maint Open · Grievances · Last Visit · Compliance Score · Actions

**Default sort:** SLA % ascending.

### 5.2 Maintenance Priority Queue (Zone)

Top 10 open maintenance tickets across zone branches, Critical+High first.

**Columns:** Branch · Category · Priority · Days Open · [View]

### 5.3 Zone Ops Trend Chart

Multi-line: SLA % + Grievances Closed + Maintenance Closed — 12 months.

### 5.4 Coordinator Visit Status

Mini-table: Coordinator → Branches Assigned → Visits Completed → Overdue.

---

## 6. Drawers

- `branch-ops-detail` (640px) — zone-scoped
- `maintenance-create` (560px) — raise from zone

---

## 7. Toast / Empty / Loader states

Follow Division G standard (see index). Skeleton: KPI bar + 2 tables + chart.

---

## 8. Role-Based UI Visibility

| Element | COO/Ops Mgr | Zone Dir G4 | Zone Ops G3 |
|---|---|---|---|
| Zone selector | ✅ | ❌ (own zone) | ❌ (own zone) |
| [Raise Maintenance] | ✅ | ✅ | ✅ |
| [Escalate to COO] | N/A | ✅ | ✅ |
| Export | ✅ | ✅ | ❌ |

---

## 9. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/zone/{zone_id}/ops/` | JWT (G3+) | Full ops dashboard |
| GET | `/api/v1/group/{id}/zone/{zone_id}/ops/kpi-cards/` | JWT (G3+) | KPI cards |
| GET | `/api/v1/group/{id}/zone/{zone_id}/ops/branches/` | JWT (G3+) | Zone branch table |
| GET | `/api/v1/group/{id}/zone/{zone_id}/ops/maintenance/` | JWT (G3+) | Priority maintenance |
| GET | `/api/v1/group/{id}/zone/{zone_id}/ops/trend/` | JWT (G3+) | 12-month trend |

---

## 10. HTMX Patterns

| Interaction | hx-trigger | hx-get | hx-target | hx-swap |
|---|---|---|---|---|
| Zone selector change | `change` | `/api/.../zone/{id}/ops/` | `#zone-ops-content` | `innerHTML` |
| KPI auto-refresh | `every 5m` | `/api/.../zone/{id}/ops/kpi-cards/` | `#kpi-bar` | `innerHTML` |
| Branch sort | `click` | `/api/.../zone/{id}/ops/branches/?sort={}` | `#zone-branch-table` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
