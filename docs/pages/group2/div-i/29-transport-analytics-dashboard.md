# 29 — Transport Analytics Dashboard

> **URL:** `/group/transport/analytics/`
> **File:** `29-transport-analytics-dashboard.md`
> **Template:** `portal_base.html`
> **Priority:** P1
> **Role:** Group Transport Director (primary) · Fleet Manager · Safety Officer · CFO (view)

---

## 1. Purpose

Data-driven analytics view for transport operations — fleet utilisation, route efficiency, cost per student, on-time performance, safety incident trends, GPS coverage trends, and driver compliance trajectory. Designed for strategic decision-making: which routes need splitting, which buses need replacing, which branches have unsafe transport operations.

This page is read-only — all charts, no edit actions. Drills through to operational pages for corrective action.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Transport Director | G3 | Full — all analytics | Primary consumer |
| Group Fleet Manager | G3 | Fleet + maintenance analytics | Full access |
| Group Transport Safety Officer | G3 | Safety analytics | Full access |
| Group CFO | G1 | Cost analytics only | Financial tabs only |
| Group Chairman / CEO | G5 / G4 | View via governance reports | Not this URL |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Transport Management  ›  Transport Analytics Dashboard
```

### 3.2 Page Header
```
Transport Analytics                         [Date Range ▾]  [Branch ▾]  [Export Report ↓]
AY [current academic year]  ·  [N] Branches  ·  [N] Buses  ·  [N] Routes
```

---

## 4. Analytics Sections

### 4.1 Summary KPI Row

| KPI | Current Value | vs Last Month | vs Last AY |
|---|---|---|---|
| Fleet Utilisation % | % buses in daily operation | ▲/▼ % | ▲/▼ % |
| On-Time Performance | % routes on schedule | ▲/▼ % | ▲/▼ % |
| Safety Incidents (Month) | Count | ▲/▼ | ▲/▼ |
| Collection Rate | % transport fee collected | ▲/▼ % | ▲/▼ % |
| Cost per Student/Month | ₹ | ▲/▼ ₹ | ▲/▼ ₹ |
| Driver Compliance | % valid licence + BGV | ▲/▼ % | — |

---

### 4.2 Fleet Utilisation Chart

**Chart — Fleet Utilisation (12-month line)**
- % buses deployed daily, month-by-month
- Idle fleet (unassigned buses) as stacked bar

---

### 4.3 On-Time Performance Heatmap

**Heatmap — Branch × Month**
- Colour: Green ≥ 90% on-time · Yellow 70–90% · Red < 70%
- Click cell → branch/month drill-down modal

---

### 4.4 Safety Incidents Trend

**Chart — Incident Trend (12-month bar)**
- Bars by severity (1/2/3/4 stacked)
- Line overlay: Incident-free day streak

**Chart — Incident Type Breakdown (Pie)**
- By incident type (Accident / Breakdown / SOS / etc.)

---

### 4.5 Transport Cost Analysis

**Chart — Cost Breakdown (Stacked bar — monthly)**
- Fuel / Maintenance / Driver wages (if available) / Misc
- Line overlay: Cost per student/month

**Chart — Cost vs Revenue (12-month)**
- Transport fee collected vs total transport opex
- Shows if transport is cost-recovering

---

### 4.6 Route Efficiency Matrix

**Table — Routes ranked by efficiency**

| Route | Branch | Students | Bus Capacity | Utilisation % | Avg Delay (min) | Cost per Student |
|---|---|---|---|---|---|---|

Sortable. Colour-code: Utilisation < 50% = yellow (underutilised) · > 100% = red (overloaded).

---

### 4.7 GPS Coverage Trend

**Chart — GPS Online % (30-day daily line)**
- % buses transmitting GPS during school hours each day
- Target line at 95%

---

### 4.8 Driver Compliance Trend

**Chart — Licence + BGV + Training compliance (12-month lines)**
- Three overlapping lines: Licence valid % · BGV cleared % · Training current %

---

## 5. Drawers

### 5.1 Drill-down Modal: `branch-analytics`
- **Width:** 640px
- Selected branch and month: all KPIs scoped to that branch
- Links to relevant operational pages for action

---

## 6. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Export initiated | "Analytics report export is being prepared." | Info | 4s |
| Export ready | "Analytics report export ready. Download below." | Success | 4s |
| Export failed | "Export failed. Please try again." | Error | 5s |

---

## 7. Empty States

| Condition | Heading | Description |
|---|---|---|
| Insufficient data | "Insufficient Data" | "Analytics require at least 30 days of transport data." |
| No routes in selected branch | "No Data for Selected Filter" | "No transport routes configured for this branch." |

---

## 8. Loader States

| Trigger | Loader Type |
|---|---|
| Page load | Full-page chart skeleton (all 6 chart areas) |
| Date/branch filter change | Chart area shimmers while reloading |
| Drill-down modal | 640px skeleton |

---

## 9. Role-Based UI Visibility

| Element | Transport Director G3 | Fleet Manager G3 | Safety Officer G3 | CFO G1 |
|---|---|---|---|---|
| Fleet Utilisation Charts | ✅ | ✅ | ✅ | ❌ |
| Safety Incident Charts | ✅ | ✅ | ✅ | ❌ |
| Cost Analysis Charts | ✅ | ✅ | ❌ | ✅ |
| Route Efficiency Matrix | ✅ | ✅ | ✅ | ❌ |
| Driver Compliance Charts | ✅ | ✅ | ✅ | ❌ |
| Export Report | ✅ | ✅ | ✅ | ✅ |

---

## 10. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/transport/analytics/kpi-summary/` | JWT (G3+) | Summary KPI row |
| GET | `/api/v1/group/{group_id}/transport/analytics/fleet-utilisation/` | JWT (G3+) | Fleet utilisation chart |
| GET | `/api/v1/group/{group_id}/transport/analytics/on-time-heatmap/` | JWT (G3+) | On-time heatmap data |
| GET | `/api/v1/group/{group_id}/transport/analytics/incidents/` | JWT (G3+) | Incident trend charts |
| GET | `/api/v1/group/{group_id}/transport/analytics/costs/` | JWT (G3+) | Cost analysis data |
| GET | `/api/v1/group/{group_id}/transport/analytics/route-efficiency/` | JWT (G3+) | Route efficiency matrix |
| GET | `/api/v1/group/{group_id}/transport/analytics/gps-coverage/` | JWT (G3+) | GPS trend |
| GET | `/api/v1/group/{group_id}/transport/analytics/driver-compliance/` | JWT (G3+) | Compliance trend |
| GET | `/api/v1/group/{group_id}/transport/analytics/export/` | JWT (G3+) | Export full analytics report |

## 11. HTMX Patterns

| Interaction | hx-trigger | hx-get/post | hx-target | hx-swap |
|---|---|---|---|---|
| Date range filter | `change` | GET `.../analytics/kpi-summary/?{filters}` | `#kpi-summary-row` | `innerHTML` |
| Branch filter | `change` | GET `.../analytics/kpi-summary/?{filters}` | `#kpi-summary-row` | `innerHTML` |
| Fleet utilisation chart reload | `change` on filters | GET `.../analytics/fleet-utilisation/?{filters}` | `#fleet-utilisation-chart` | `innerHTML` |
| On-time heatmap reload | `change` on filters | GET `.../analytics/on-time-heatmap/?{filters}` | `#ontime-heatmap` | `innerHTML` |
| Safety chart reload | `change` on filters | GET `.../analytics/incidents/?{filters}` | `#safety-chart` | `innerHTML` |
| Cost chart reload | `change` on filters | GET `.../analytics/costs/?{filters}` | `#cost-chart` | `innerHTML` |
| Route efficiency sort | `click` on header | GET `.../analytics/route-efficiency/?sort={col}&dir={asc/desc}` | `#route-efficiency-table` | `innerHTML` |
| Open branch drill-down | `click` on heatmap cell | GET `.../analytics/branches/{id}/?month={m}` | `#drawer-body` | `innerHTML` |
| Export report | `click` | GET `.../analytics/export/?{filters}` | `#export-btn` | `outerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
