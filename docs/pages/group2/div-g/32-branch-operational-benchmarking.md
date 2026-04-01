# 32 — Branch Operational Benchmarking

> **URL:** `/group/ops/reports/benchmarking/`
> **File:** `32-branch-operational-benchmarking.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** COO G4 · Operations Manager G3 · Zone Director G4 (zone) · Zone Ops/Academic G3 (zone)

---

## 1. Purpose

Side-by-side comparison of branches on operational and academic metrics. Identifies
consistently top-performing and underperforming branches. Enables COO and Operations
Manager to reallocate resources, share best practices from high performers, and provide
targeted support to low performers.

---

## 2. Metric Categories

| Category | Metrics |
|---|---|
| **Operational** | SLA Compliance % · Grievance Resolution Rate · Coordinator Visit Rate · Compliance Score · Maintenance Avg Resolution Days |
| **Academic** | Avg Marks % · Attendance Rate · Exam Compliance · Lesson Plan Submission Rate · Teacher Performance Score |
| **Financial** | Fee Collection Rate · Defaulter % |
| **Safety** | BGV Compliance · POCSO Training % · Facilities Cert Validity |
| **Composite** | Overall Operational Health Score |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Operations  ›  Reports  ›  Benchmarking
```

### 3.2 Page Header
```
Branch Operational Benchmarking        [Export Comparison ↓]
[Metric Category ▼]  [Zone Filter ▼]  [Branch Type ▼]  [Time Period ▼]
```

---

## 4. Benchmarking Table

**Default:** All branches · All metrics · Current month.

**View modes:**
- **Table:** All branches as rows, selected metrics as columns (sortable)
- **Ranked List:** Branches ranked 1–N by selected composite score

**Table columns (customizable via column selector):**

| Column | Sortable | Notes |
|---|---|---|
| Rank | ✅ | By composite score |
| Branch | ✅ | |
| Zone | ✅ | |
| Type | ✅ | |
| SLA % | ✅ | |
| Grievance Res% | ✅ | |
| Visit Rate% | ✅ | |
| Compliance Score | ✅ | |
| Maint Res Days | ✅ | Lower is better |
| Avg Marks % | ✅ | |
| Attendance % | ✅ | |
| Fee Collection% | ✅ | |
| BGV % | ✅ | |
| Health Score | ✅ | Composite |
| vs Last Month | ❌ | ↑ / → / ↓ |

**Colour coding:** Top 25% cells green · Bottom 25% cells red · Middle yellow.

**Column visibility toggle:** Yes — select which metrics to display.

**Pagination:** 25/page.

---

## 5. Comparison Charts

### 5.1 Bar Chart Comparison
**Type:** Horizontal bar chart — selected metric for all branches, sorted by value.
Benchmark line: group average.

### 5.2 Radar Chart (Multi-Metric)
**Type:** Radar/spider chart — Compare up to 5 selected branches across 6 metrics simultaneously.
**Branch selector:** Multi-select dropdown (max 5).

### 5.3 Trend Line (selected branch)
When a branch is clicked in the table → trend line chart added at bottom: selected metric over 12 months for that branch vs group average.

---

## 6. Top & Bottom Performers Panel

**Display:** Two side-by-side lists.

**Top 5 Performers (green border):** Branch name · Score · Highest metric.
**Bottom 5 Performers (red border):** Branch name · Score · Biggest gap.

[Share Best Practice →] for top performers: Opens communication compose to share with other branches.

---

## 7. Time Period Comparison

**Options:** Current Month · Last Month · Last Quarter · Last Academic Year.

**Mode:** Current vs Previous period side-by-side columns in table.

---

## 8. Export

**Export options:** CSV (all data) · PDF (formatted comparison report with charts) · Excel.

---

## 9. Toast / Empty / Loader

Standard. Skeleton: top/bottom performers panels + table + charts.

---

## 10. Role-Based UI Visibility

| Element | COO G4 | Ops Mgr G3 | Zone roles |
|---|---|---|---|
| All branches | ✅ | ✅ | Zone only |
| Radar chart (any 5 branches) | ✅ | ✅ | Zone only |
| Financial metrics | ✅ | ✅ | ❌ |
| [Share Best Practice] | ✅ | ✅ | ❌ |
| Export | ✅ | ✅ | ✅ zone |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/ops/benchmarking/` | JWT (G3+) | Benchmarking table data |
| GET | `/api/v1/group/{id}/ops/benchmarking/chart/?branches={ids}&metrics={list}` | JWT (G3+) | Radar chart data |
| GET | `/api/v1/group/{id}/ops/benchmarking/trend/?branch_id={}&metric={}` | JWT (G3+) | 12-month trend |
| GET | `/api/v1/group/{id}/ops/benchmarking/top-bottom/` | JWT (G3+) | Top/bottom 5 |
| GET | `/api/v1/group/{id}/ops/benchmarking/export/?format=csv` | JWT (G3+) | Export |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-get | hx-target | hx-swap |
|---|---|---|---|---|
| Metric category filter | `change` | `/api/.../benchmarking/?category={}` | `#benchmark-table-section` | `innerHTML` |
| Zone filter | `change` | `/api/.../benchmarking/?zone_id={}` | `#benchmark-table-section` | `innerHTML` |
| Sort click | `click` | `/api/.../benchmarking/?sort={}&dir={}` | `#benchmark-table-section` | `innerHTML` |
| Branch click (trend) | `click` | `/api/.../benchmarking/trend/?branch_id={}&metric={}` | `#trend-chart` | `innerHTML` |
| Radar branch select | `change` | `/api/.../benchmarking/chart/?branches={}` | `#radar-chart` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
