# 06 — Zone Operations Manager Dashboard

> **URL:** `/group/ops/zone-ops/`
> **File:** `06-zone-ops-manager-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Group Zone Operations Manager (G3) — exclusive landing page
> **Applicable:** Large groups only

---

## 1. Purpose

Post-login landing for the Zone Operations Manager. Responsible for day-to-day operational
management within one zone — maintenance requests, transport issues, procurement deliveries
to zone branches, grievances, and coordinator activity within the zone. Works under the Zone
Director and reports to the Group Operations Manager and COO.

> **Scoping rule:** Zone Operations Manager sees ONLY their assigned zone.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Zone Operations Manager | G3 | Full — own zone ops | Exclusive |
| Zone Director | G4 | View zone ops | Has own dashboard |
| COO | G4 | View all zones | |
| Operations Manager | G3 | View all zones | |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Zone Ops Dashboard  ›  Zone [Name]
```

### 3.2 Page Header
```
Zone [Name] — Zone Operations Manager              [Export Zone Report ↓]  [Settings ⚙]
[Name] · Ops coverage for [N] branches · Last login: [date time]
```

---

## 4. KPI Summary Bar (6 cards)

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Open Maintenance | `11 tickets · 1 Critical` | Green = 0 Critical · Red ≥1 | → Page 26 |
| Zone SLA Compliance | `89.1%` | Green ≥95% · Yellow 85–95% · Red <85% | → Page 15 |
| Open Grievances (Zone) | `4 open · 1 overdue` | Green = none overdue · Red ≥1 | → Page 11 |
| Pending Deliveries | `3 deliveries expected` | Informational | → Page 22 |
| Coordinator Visits (Zone) | `8 / 12 planned` | Green ≥75% · Yellow 50–75% · Red <50% | → Page 10 |
| Facility Certs Expiring | `1 in next 30d` | Green = 0 · Yellow 1–2 · Red ≥3 | → Page 30 |

**HTMX:** `every 5m` → `/api/v1/group/{id}/zone/{zone_id}/ops-manager/kpi-cards/` → `#kpi-bar`

---

## 5. Sections

### 5.1 Zone Branch Ops Status Table

**Search:** Branch name. Debounce 300ms.

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| Branch Name | ✅ | Link → ops detail drawer |
| SLA % | ✅ | |
| Open Maintenance | ✅ | Count |
| Open Grievances | ✅ | Count |
| Last Coordinator Visit | ✅ | |
| Compliance Score | ✅ | |
| Actions | ❌ | View · Raise Maintenance · Log Grievance |

---

### 5.2 Maintenance Priority Queue

> Critical and High priority maintenance across zone branches.

**Columns:** Branch · Category · Priority badge · Description · Days Open · Assigned To · [View]

**Max rows:** 10. [View All Maintenance →] → Page 26 filtered to zone.

---

### 5.3 Zone Ops Trend Chart

**Type:** Multi-line — SLA % + Grievances Resolved + Maintenance Closed — 12 months.

**Library:** Chart.js 4.x. Colorblind-safe. PNG export.

---

### 5.4 Quick Access Grid

4 tiles:
| Tile | Label | Link |
|---|---|---|
| 1 | Maintenance Tracker | `/group/ops/facilities/maintenance/?zone={id}` |
| 2 | Grievance Centre | `/group/ops/grievances/?zone={id}` |
| 3 | Visit Scheduler | `/group/ops/visits/?zone={id}` |
| 4 | Facilities Compliance | `/group/ops/facilities/compliance/?zone={id}` |

---

## 6. Drawers & Modals

### 6.1 Drawer: Branch Ops Detail (Zone scope)
- **Width:** 640px
- **Tabs:** Ops · Maintenance · Grievances · Visits
- **Actions:** Raise maintenance ticket · Assign coordinator visit

### 6.2 Drawer: `maintenance-create`
- **Width:** 560px
- **Fields:** Branch (zone branches only) · Category · Priority · Description · Photos (up to 5) · Assign to (vendor/maintenance staff)

---

## 7. Toast Messages

| Action | Toast | Type |
|---|---|---|
| Maintenance ticket created | "Maintenance ticket raised — Facilities team notified" | Success · 4s |
| Grievance assigned | "Grievance assigned" | Success · 4s |

---

## 8. Empty States

| Condition | Heading |
|---|---|
| No zone assigned | "No zone assigned. Contact your COO." |
| No open maintenance | "No open maintenance tickets in zone" |

---

## 9. Loader States

Page load: Skeleton KPI + branch table + maintenance queue + chart.

---

## 10. Role-Based UI Visibility

| Element | Zone Ops Mgr G3 | Zone Director G4 | COO G4 |
|---|---|---|---|
| Own zone | ✅ Full | ✅ Full | ✅ Full |
| Other zones | ❌ | Own zone only | ✅ All |
| [Raise Maintenance] | ✅ | ✅ | ✅ |
| [Assign Grievance] | ✅ | ✅ | ✅ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/zone/{zone_id}/ops-manager/dashboard/` | JWT (G3+) | Full dashboard |
| GET | `/api/v1/group/{id}/zone/{zone_id}/ops-manager/kpi-cards/` | JWT (G3+) | KPI cards |
| GET | `/api/v1/group/{id}/ops/branches/?zone_id={zone_id}` | JWT (G3+) | Zone branches |
| GET | `/api/v1/group/{id}/facilities/maintenance/?zone_id={zone_id}&priority=critical,high` | JWT (G3+) | Priority queue |
| GET | `/api/v1/group/{id}/zone/{zone_id}/ops/trend/` | JWT (G3+) | Trend chart data |
| POST | `/api/v1/group/{id}/facilities/maintenance/` | JWT (G3) | Create maintenance ticket |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-get | hx-target | hx-swap |
|---|---|---|---|---|
| Branch search | `input delay:300ms` | `/api/.../branches/?zone_id={}&q={}` | `#zone-ops-table-body` | `innerHTML` |
| KPI auto-refresh | `every 5m` | `/api/.../zone/{id}/ops-manager/kpi-cards/` | `#kpi-bar` | `innerHTML` |
| Open ops detail | `click` | `/api/.../branches/{id}/detail/` | `#drawer-body` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
