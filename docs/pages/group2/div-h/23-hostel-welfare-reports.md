# 23 — Hostel Welfare Reports

> **URL:** `/group/hostel/welfare/reports/`
> **File:** `23-hostel-welfare-reports.md`
> **Template:** `portal_base.html`
> **Priority:** P1
> **Role:** Group Hostel Welfare Officer · Hostel Director · Boys/Girls Coordinators

---

## 1. Purpose

Trend analysis and reporting for welfare incidents across all hostel campuses. While Page 22 is the operational incident tracker, this page provides aggregate welfare intelligence — which branches have the most incidents, which severities are trending up, which hostel types (AC/Non-AC, Boys/Girls) have different welfare profiles, and whether welfare events are resolved within SLA targets.

Reports here are used by the Hostel Director for monthly board presentations and by the Group Mental Health Coordinator for counselling resource allocation.

---

## 2. Page Layout

### 2.1 Breadcrumb
```
Group HQ  ›  Hostel Management  ›  Welfare  ›  Welfare Reports
```

### 2.2 Page Header
- **Title:** `Hostel Welfare Reports`
- **Filters:** AY · Month Range · Branch · Gender
- **Right controls:** `Export Report ↓` · `Schedule Auto-Report`
- **PNG export format:** Individual charts exported at 300 DPI · minimum 1200px wide · group branding footer (group name, report title, export date) appended. Per-chart ⬇ PNG icon available on each chart; Export Report ↓ includes full PDF report + chart PNGs as a ZIP.

---

## 3. Report Sections

### 3.1 Executive Summary Cards

| Metric | Value | vs Last Month |
|---|---|---|
| Total Incidents (Period) | [N] | +/-% trend arrow |
| Severity 1+2 Share | [N]% | |
| Avg Resolution Time | [N] hours | |
| SLA Compliance Rate | [N]% | |
| Branches with 0 Incidents | [N] | |
| POCSO-linked Incidents | [N] | |

---

### 3.2 Chart 1 — Incidents by Severity Over Time

- Stacked area chart: S1 (red) · S2 (orange) · S3 (yellow) · S4 (blue)
- X: Monthly. Y: Count.
- Filter: Branch / Gender / All.

---

### 3.3 Chart 2 — Incident Heatmap by Branch

- Horizontal bar chart: Branches on Y-axis · Incident count on X-axis
- Color intensity = severity distribution
- Sorted: Most incidents at top

---

### 3.4 Chart 3 — Boys vs Girls Welfare Profile

- Grouped bar: Boys total incidents vs Girls total incidents per month
- Sub-grouped by severity

---

### 3.5 Chart 4 — Resolution Time Distribution

- Histogram: < 2h / 2–8h / 8–24h / 24–72h / > 72h
- Target line: "SLA requires S1 within 2h, S2 within 8h"

---

### 3.6 Chart 5 — Incident Type Distribution

- Pie chart: All incident types with %
- Filter: Boys / Girls / Severity / Branch

---

### 3.7 SLA Compliance Table by Branch

**Columns:** Branch | Total Incidents | S1 Within SLA | S2 Within SLA | Overall SLA % | Avg Resolution (hours)

Sortable. Red rows for branches with SLA < 80%.

---

### 3.8 Top Welfare Issues (Current Period)

- Word cloud or ranked list: Most common incident descriptions
- Useful for identifying systemic issues (e.g., food complaints, bullying in specific branches)

---

## 4. Auto-Report Scheduling

> Schedule automatic welfare reports to be emailed to the Hostel Director and Group Chairman.

**Settings drawer:** Frequency (Weekly / Monthly / Quarterly) · Recipients (multi-select from role list) · Report sections to include · Day of delivery.

---

## 5. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Export triggered | "Welfare report export started." | Info | 4s |
| Auto-report saved | "Monthly welfare report scheduled. Recipients notified." | Success | 4s |

---

## 6. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/hostel/welfare/reports/summary/` | JWT (G3+) | Executive summary cards |
| GET | `/api/v1/group/{group_id}/hostel/welfare/reports/trends/` | JWT (G3+) | All chart data |
| GET | `/api/v1/group/{group_id}/hostel/welfare/reports/sla-by-branch/` | JWT (G3+) | SLA table |
| GET | `/api/v1/group/{group_id}/hostel/welfare/reports/export/` | JWT (G3+) | Export full report |
| POST | `/api/v1/group/{group_id}/hostel/welfare/reports/schedule/` | JWT (G3+) | Schedule auto-report |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
