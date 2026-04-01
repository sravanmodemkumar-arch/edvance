# 32 — Hostel Analytics

> **URL:** `/group/hostel/reports/analytics/`
> **File:** `32-hostel-analytics.md`
> **Template:** `portal_base.html`
> **Priority:** P1
> **Role:** Group Hostel Director (primary) · Boys/Girls Coordinators · Welfare Officer · Mess Manager · Fee Manager

---

## 1. Purpose

Interactive analytics dashboard covering long-term trends across all hostel sub-systems — occupancy trends, welfare incident patterns, fee collection trends, mess hygiene improvement (or deterioration), security incident frequency, and medical room utilization. Unlike the MIS Report (Page 31) which is a monthly snapshot, this page is an always-on exploratory analytics surface with configurable date ranges, branch filters, and chart types.

The analytics here help the Hostel Director identify systemic problems: branches that consistently underperform on welfare SLA, months where discipline cases spike, hostel types that have disproportionate welfare incidents, or fee collection rates that drop in specific quarters.

---

## 2. Page Layout

### 2.1 Breadcrumb
```
Group HQ  ›  Hostel Management  ›  Reports  ›  Hostel Analytics
```

### 2.2 Page Header
- **Title:** `Hostel Analytics`
- **Global Filters (persistent, apply to all charts):** Date Range · Branch(es) · Gender · Hostel Type (AC/Non-AC)
- **Right controls:** `Export All Charts (PNG)` · `Export Data (CSV)`
- **PNG export format:** 300 DPI · minimum 1200px wide · group branding footer (group name, page title, export date) appended automatically. Per-chart export available via ⬇ icon on each chart card; "Export All Charts (PNG)" bundles all charts into a ZIP.

---

## 3. Analytics Sections

### 3.1 Occupancy Analytics

**Chart 1A — Occupancy Trend (12 months)**
- Multi-line: Total / Boys / Girls / AC / Non-AC occupancy %
- Target line at 85%.

**Chart 1B — Occupancy by Branch (Current Month)**
- Horizontal bar: All branches sorted by occupancy %
- Color: Green ≥ 85% / Yellow 70–85% / Red < 70%

**Chart 1C — Occupancy Seasonality**
- Line chart: Average occupancy by month across 3 academic years (to detect seasonal patterns — e.g., drop after summer exams)

---

### 3.2 Welfare Analytics

**Chart 2A — Incidents by Severity Over Time (12 months)**
- Stacked bar: S1/S2/S3/S4 per month

**Chart 2B — Incidents by Branch (Heatmap)**
- Bar chart: Incidents per branch, grouped by severity

**Chart 2C — Boys vs Girls Welfare Comparison**
- Grouped bar: Boys incidents vs Girls incidents per month
- Ratio card: "Boys incident rate: [N] per 100 hostelers · Girls: [N] per 100"

**Chart 2D — SLA Compliance Trend**
- Line: SLA compliance % per month (S1 and S2 separate lines)
- Target line at 95%.

**Chart 2E — Incident Type Distribution**
- Pie chart: All incident types with %

---

### 3.3 Fee Collection Analytics

**Chart 3A — Collection Rate Trend (12 months)**
- Line: Overall collection % per month
- Area: Outstanding ₹ per month (secondary Y-axis)

**Chart 3B — Defaulter Trend**
- Bar: Count of 30d+ defaulters per month

**Chart 3C — Revenue by Fee Type (Stacked Bar)**
- Stacked: Accommodation / Mess / Extras per month

---

### 3.4 Mess Hygiene Analytics

**Chart 4A — Average Hygiene Score by Branch**
- Bar chart: All branches sorted by avg score (last 6 months)
- Fail threshold line at 60%.

**Chart 4B — Hygiene Score Trend**
- Multi-line: Top 5 most improved branches + bottom 5 (12 months)

**Chart 4C — Audit Frequency**
- Bar: Audits conducted per branch per quarter (compliance check — minimum 1/month required)

---

### 3.5 Security Analytics

**Chart 5A — Security Incidents by Type (6 months)**
- Stacked bar: All incident types per month

**Chart 5B — Boys vs Girls Security Incidents**
- Grouped bar per month

**Chart 5C — CCTV Uptime**
- Line: Average CCTV uptime % per month
- Girls hostel CCTV shown separately (higher importance)

---

### 3.6 Medical Analytics

**Chart 6A — Medical Visits per 100 Hostelers**
- Line per month (normalized rate — accounts for occupancy differences between branches)

**Chart 6B — Condition Distribution**
- Pie: Most common complaints/conditions from medical visits

---

### 3.7 Discipline Analytics

**Chart 7A — Cases by Type (AY to date)**
- Horizontal bar: Case count per type

**Chart 7B — Monthly Cases and Outcomes**
- Stacked bar: Warning / Suspension / Expulsion / Dismissed per month

---

## 4. Cross-Metric Correlation View

> Advanced section — relates two metrics to identify correlations.

**Pre-configured quick-select combinations (shown as chips above the chart):**
- Welfare incidents vs Fee defaulters (same branch, same month) → do financial stress and welfare incidents correlate?
- Mess hygiene score vs food complaints → validates audit system accuracy
- Security incidents vs roll call discrepancies → identifies branches with system-wide control issues
- Occupancy rate vs welfare incident rate → do crowded hostels generate more welfare events?
- Discipline cases vs welfare incidents → are high-discipline branches also high-welfare-burden?
- Medical visits per 100 hostelers vs mess hygiene score → does poor hygiene drive medical room usage?
- CCTV uptime % vs unauthorized visitor entries → does camera coverage deter violations?
- Fee collection rate vs hostel type (AC vs Non-AC) → do AC hostel families pay more reliably?
- Welfare SLA compliance % vs branch hosteler count → do larger branches miss SLAs more often?
- Calling hour violations vs welfare incident count (girls hostels only) → do communication restrictions correlate with mental health incidents?

**Display:** Scatter plot with branch names as data points. Axes configurable from metric dropdowns (override any pre-configured pair).

---

## 5. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Export triggered | "Analytics data export started." | Info | 4s |
| Chart PNG exported | "Chart exported as PNG." | Success | 3s |
| Filter applied | — | Silent | — |

---

## 6. Loader States

| Trigger | Loader Type |
|---|---|
| Page load | Skeleton placeholders for all chart areas |
| Filter change (global) | All charts show shimmer simultaneously |
| Individual chart filter | That chart's shimmer only |
| Export | Spinner on Export button |

---

## 7. Role-Based UI Visibility

| Section | Hostel Director | Boys Coord | Girls Coord | Welfare Officer | Mess Manager | Fee Manager |
|---|---|---|---|---|---|---|
| All sections | ✅ | Boys-scoped | Girls-scoped | Welfare + Security | Mess only | Fee only |
| Cross-metric view | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Export full data | ✅ | ✅ scoped | ✅ scoped | ✅ scoped | ✅ scoped | ✅ scoped |

---

## 8. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/hostel/analytics/occupancy/` | JWT (G3+) | Occupancy chart data |
| GET | `/api/v1/group/{group_id}/hostel/analytics/welfare/` | JWT (G3+) | Welfare chart data |
| GET | `/api/v1/group/{group_id}/hostel/analytics/fees/` | JWT (G3+) | Fee chart data |
| GET | `/api/v1/group/{group_id}/hostel/analytics/mess/` | JWT (G3+) | Mess hygiene chart data |
| GET | `/api/v1/group/{group_id}/hostel/analytics/security/` | JWT (G3+) | Security chart data |
| GET | `/api/v1/group/{group_id}/hostel/analytics/medical/` | JWT (G3+) | Medical chart data |
| GET | `/api/v1/group/{group_id}/hostel/analytics/discipline/` | JWT (G3+) | Discipline chart data |
| GET | `/api/v1/group/{group_id}/hostel/analytics/correlation/` | JWT (G3+) | Cross-metric correlation |
| GET | `/api/v1/group/{group_id}/hostel/analytics/export/` | JWT (G3+) | Export CSV |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
