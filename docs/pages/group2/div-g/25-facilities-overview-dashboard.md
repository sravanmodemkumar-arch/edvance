# 25 — Facilities Overview Dashboard

> **URL:** `/group/ops/facilities/`
> **File:** `25-facilities-overview-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** COO G4 (full) · Operations Manager G3 (view + manage maintenance) · Zone Dir G4 (zone) · Zone Ops Mgr G3 (zone)

> **Note:** Group Facilities Manager (G0) uses external CMMS tools. Their work is visible
> here by COO/Ops Manager who log outcomes and status into EduForge.

---

## 1. Purpose

Executive overview of all campus facilities across the group — maintenance ticket status,
building asset health, CAPEX project status, utilities costs, and safety compliance. The
COO uses this to identify campuses with failing infrastructure before it becomes a safety
or operational risk.

---

## 2. Page Layout

### 2.1 Breadcrumb
```
Group HQ  ›  Operations  ›  Facilities Overview
```

### 2.2 Page Header
```
Facilities Overview                    [Export Facilities Report ↓]
[N] campuses · [N] buildings · Updated: [timestamp]
```

---

## 3. KPI Summary Bar (6 cards)

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Open Maintenance | `23 tickets · 3 Critical` | Green = 0 Critical · Red ≥1 | → Page 26 |
| Avg Resolution Time | `2.4 days` | Green ≤1d · Yellow 1–3d · Red >3d | → Page 26 |
| Buildings Registered | `186 across 50 branches` | Informational | → Page 27 |
| Active CAPEX Projects | `4 ongoing` | Informational | → Page 28 |
| Safety Certs Expiring | `3 in next 30d` | Green =0 · Yellow 1–3 · Red ≥4 | → Page 30 |
| Utilities Anomalies | `2 branches with spike` | Green =0 · Red ≥1 | → Page 29 |

**HTMX:** `every 5m` → `/api/v1/group/{id}/facilities/kpi-cards/` → `#kpi-bar`

---

## 4. Sections

### 4.1 Branch Facilities Health Table

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| Branch | ✅ | Link → branch facility detail drawer |
| Zone | ✅ | |
| Buildings | ✅ | Count |
| Open Maintenance | ✅ | Count · red if any Critical |
| CAPEX Active | ✅ | Count |
| Safety Certs OK | ✅ | ✅/⚠/❌ |
| Utilities Alert | ✅ | ✅ Normal · ⚠ Spike |
| Facility Score | ✅ | 0–100 composite |
| Actions | — | View · Raise Ticket |

**Default sort:** Facility Score ascending.

**Pagination:** 25/page.

### 4.2 Maintenance Priority Queue

Top 10 Critical/High tickets across all branches.

**Columns:** Branch · Category · Priority · Description · Days Open · [View →]

[View All Maintenance →] → Page 26.

### 4.3 CAPEX Projects Summary

Active projects table: Project · Branch · Budget · Spent % · Expected Completion · Status.

[View All CAPEX →] → Page 28.

### 4.4 Facilities Trend Chart

**Type:** Multi-line — Maintenance tickets raised vs resolved per month (12 months).

**Library:** Chart.js 4.x. PNG export.

### 4.5 Quick Navigation Grid

| Tile | Label | Link |
|---|---|---|
| 1 | Maintenance Tracker | `/group/ops/facilities/maintenance/` |
| 2 | Building Register | `/group/ops/facilities/buildings/` |
| 3 | CAPEX Projects | `/group/ops/facilities/capex/` |
| 4 | Utilities Monitor | `/group/ops/facilities/utilities/` |
| 5 | Compliance Register | `/group/ops/facilities/compliance/` |

---

## 5. Branch Facility Detail Drawer

- **Width:** 640px
- **Tabs:** Overview · Maintenance · Buildings · CAPEX · Compliance

**Overview:** Building count, total floor area, ownership breakdown (own/leased).

**Maintenance:** Open tickets by priority + last 5 resolved.

**Buildings:** List of buildings with condition ratings.

**CAPEX:** Active and planned projects.

**Compliance:** Safety certificates with expiry status.

---

## 6. Toast / Empty / Loader

Standard. Skeleton: KPI + table + maintenance queue + chart.

---

## 7. Role-Based UI Visibility

| Element | COO G4 | Ops Mgr G3 | Zone Dir G4 | Zone Ops G3 |
|---|---|---|---|---|
| All branches | ✅ | ✅ | Zone only | Zone only |
| [Raise Ticket] | ✅ | ✅ | ✅ | ✅ |
| Export | ✅ | ❌ | ❌ | ❌ |
| CAPEX sections | ✅ | ✅ view | ✅ view | ❌ |

---

## 8. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/facilities/` | JWT (G3+) | Branch facilities table |
| GET | `/api/v1/group/{id}/facilities/kpi-cards/` | JWT (G3+) | KPI auto-refresh |
| GET | `/api/v1/group/{id}/facilities/maintenance/?priority=critical,high&limit=10` | JWT (G3+) | Priority queue |
| GET | `/api/v1/group/{id}/facilities/capex/?status=active` | JWT (G3+) | CAPEX summary |
| GET | `/api/v1/group/{id}/facilities/trend/` | JWT (G3+) | 12-month trend |
| GET | `/api/v1/group/{id}/facilities/branches/{bid}/` | JWT (G3+) | Branch facility detail |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
