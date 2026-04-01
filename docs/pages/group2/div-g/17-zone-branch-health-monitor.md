# 17 — Zone Branch Health Monitor

> **URL:** `/group/ops/zones/<id>/branches/`
> **File:** `17-zone-branch-health-monitor.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Roles:** COO G4 · Ops Manager G3 · Zone Director G4 (own zone) · Zone Academic G3 · Zone Ops G3

---

## 1. Purpose

Combined ops + academic health view for all branches within a specific zone. Provides the
Zone Director with a unified health score per branch combining operational and academic
metrics. Used for zone-level performance reviews and identifying branches needing
additional support.

---

## 2. Role Access

Zone Director, Zone Academic, Zone Ops see own zone only. COO/Ops Mgr see all zones
via selector.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Operations  ›  Zones  ›  Zone [Name]  ›  Branch Health
```

### 3.2 Navigation Tabs
```
[Operations →]  [Academic →]  [Branch Health]
```

---

## 4. Summary Strip (Zone Level)

| Card | Value |
|---|---|
| Zone Health Score | Composite `81/100` |
| Best Performing Branch | [Name] (`94/100`) |
| Most At-Risk Branch | [Name] (`52/100`) |
| Branches Below 70 | Count |

---

## 5. Branch Health Scorecard Table

> Health score = weighted average of ops (60%) + academic (40%) metrics.

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| Branch Name | ✅ | Link → branch health detail drawer |
| Health Score | ✅ | 0–100 · colour: Green ≥80 · Yellow 60–79 · Red <60 |
| Ops Score | ✅ | SLA + compliance + maintenance |
| Academic Score | ✅ | Marks + attendance + exam compliance |
| Open Issues | ✅ | Combined escalations + grievances |
| Trend | ❌ | ↑ / → / ↓ vs last month |
| Actions | — | View · Flag for Review |

**Default sort:** Health Score ascending.

### 5.1 Health Score Breakdown (per branch in drawer)

- **Width:** 640px
- **Tabs:** Health Summary · Ops Details · Academic Details · Issues

**Ops Details:** SLA %, maintenance tickets, grievances, coordinator visit status
**Academic Details:** Avg marks, attendance %, exam compliance, teacher score
**Issues:** Open escalations + grievances in one list

---

## 6. Zone Branch Comparison Chart

**Type:** Radar/spider chart — Branches as data points, Axes = key metrics (SLA, Academic, Maintenance, Compliance, Visits).

**Library:** Chart.js 4.x radar chart. One polygon per branch (up to 15 branches). PNG export.

---

## 7. Rank Table (Within Zone)

Zone-internal leaderboard: Branch rank 1–N by health score. With month-over-month rank change (↑3, ↓2, →).

---

## 8. Toast / Empty / Loader

Standard division G. Skeleton: summary strip + table + radar chart.

---

## 9. Role-Based UI Visibility

| Element | Zone roles | COO/Ops |
|---|---|---|
| Zone data | Own zone | All zones |
| [Flag for Review] | ✅ | ✅ |
| Export | ✅ Zone Dir only | ✅ |

---

## 10. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/zone/{zone_id}/health/` | JWT (G3+) | Branch health table |
| GET | `/api/v1/group/{id}/zone/{zone_id}/health/summary/` | JWT (G3+) | Summary strip |
| GET | `/api/v1/group/{id}/zone/{zone_id}/health/chart/` | JWT (G3+) | Radar chart data |
| GET | `/api/v1/group/{id}/zone/{zone_id}/health/branches/{bid}/` | JWT (G3+) | Branch health detail |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
