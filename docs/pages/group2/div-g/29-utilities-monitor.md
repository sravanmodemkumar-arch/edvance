# 29 — Utilities Monitor

> **URL:** `/group/ops/facilities/utilities/`
> **File:** `29-utilities-monitor.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Roles:** COO G4 · Operations Manager G3 · Zone Dir G4 (zone) · Zone Ops Mgr G3 (zone)

---

## 1. Purpose

Monitors electricity, water, internet, and generator fuel costs across all branch campuses.
Detects cost anomalies (spikes vs baseline) and helps COO identify energy inefficiency or
billing issues. Cost per student benchmarks help compare branches fairly.

---

## 2. Utility Types

| Utility | Unit | Billing Cycle |
|---|---|---|
| Electricity | kWh / ₹ | Monthly |
| Water | Litres / ₹ | Monthly |
| Internet / Leased Line | Mbps / ₹ | Monthly |
| Generator Fuel | Litres / ₹ | Monthly |
| LPG / Gas (Hostel Mess) | Cylinders / ₹ | Monthly |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Facilities  ›  Utilities Monitor
```

### 3.2 Month Selector
```
< April 2025  [Month ▼] [Year ▼]  March 2026 >
```

### 3.3 Summary Strip
| Card | Value |
|---|---|
| Total Utility Spend | ₹ this month |
| vs Last Month | ↑ or ↓ % |
| Anomaly Alerts | Count (red if >0) |
| Highest Spend Branch | [Name] ₹X.XL |

---

## 4. Branch Utility Table

**Columns (for selected month):**
| Column | Sortable | Notes |
|---|---|---|
| Branch | ✅ | Link → branch utility detail drawer |
| Zone | ✅ | |
| Students | ✅ | For per-student cost calc |
| Electricity (₹) | ✅ | |
| Water (₹) | ✅ | |
| Internet (₹) | ✅ | |
| Generator (₹) | ✅ | |
| Total (₹) | ✅ | |
| Cost/Student | ✅ | Red if >group average + 30% |
| vs Last Month | ✅ | % change · red if spike >20% |
| Alert | ❌ | ⚠ if anomaly detected |
| Actions | — | View Trend · Log Reading · Raise Alert |

**Anomaly detection:** Any branch with >20% month-over-month increase on any utility → automatic alert flag.

---

## 5. Branch Utility Detail Drawer

- **Width:** 560px
- **Tabs:** This Month · 12-Month Trend · Readings

**12-Month Trend:** Line chart per utility type (12 months).

**Readings tab:** Manual meter readings log: Date · Reader · kWh/Litres reading · Bill amount.

---

## 6. Log Reading Drawer

- **Width:** 480px
- **Fields:** Branch · Utility type · Reading date · Meter reading · Invoice amount · Invoice PDF upload

---

## 7. Utility Benchmark Chart

**Type:** Bar chart — Cost per student per utility type, all branches sorted by total.

Highlights: Group average line overlay. Branches significantly above average marked red.

---

## 8. Toast / Empty / Loader

Standard. Skeleton: summary + table.

---

## 9. Role-Based UI Visibility

| Element | COO G4 | Ops Mgr G3 | Zone roles |
|---|---|---|---|
| All branches | ✅ | ✅ | Zone only |
| [Log Reading] | ✅ | ✅ | ✅ |
| [Raise Alert] | ✅ | ✅ | ✅ |
| Export | ✅ | ✅ | ❌ |

---

## 10. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/facilities/utilities/?month={yyyy-mm}` | JWT (G3+) | Monthly utility table |
| GET | `/api/v1/group/{id}/facilities/utilities/branches/{bid}/` | JWT (G3+) | Branch detail + trend |
| POST | `/api/v1/group/{id}/facilities/utilities/readings/` | JWT (G3+) | Log meter reading |
| GET | `/api/v1/group/{id}/facilities/utilities/benchmark/` | JWT (G3+) | Benchmark chart data |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
