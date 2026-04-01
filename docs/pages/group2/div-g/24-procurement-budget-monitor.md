# 24 — Procurement Budget Monitor

> **URL:** `/group/ops/procurement/budget/`
> **File:** `24-procurement-budget-monitor.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** COO G4 (full — set budgets) · Operations Manager G3 (view)

---

## 1. Purpose

Tracks procurement budget allocation and utilization across categories, branches, and
financial year. Alerts when any category approaches or exceeds budget. COO sets annual
procurement budgets; spend from approved POs is tracked automatically.

---

## 2. Page Layout

### 2.1 Breadcrumb
```
Group HQ  ›  Procurement  ›  Budget Monitor
```

### 2.2 Page Header
```
Procurement Budget Monitor             [Set Annual Budget]  [Export Report ↓]
Financial Year [FY] · Updated: [timestamp]
```

### 2.3 Summary Strip
| Card | Value |
|---|---|
| Total Annual Budget | `₹2.0 Cr` |
| Total Spent YTD | `₹1.4 Cr (70%)` |
| Remaining Budget | `₹60 L` |
| Over-budget Categories | Count (red if >0) |

---

## 3. Budget vs Actual Table

**Rows per procurement category:**

| Column | Notes |
|---|---|
| Category | Books · Uniforms · Lab · IT · Stationery · Sports · Furniture · Hostel · Safety |
| Annual Budget | ₹ |
| Spent YTD | ₹ |
| Utilization % | Progress bar |
| Remaining | ₹ |
| Committed (pending POs) | ₹ (approved but not yet delivered/paid) |
| Available | Budget − Spent − Committed |
| Status | Green ≤80% · Yellow 80–95% · Red >95% |
| Actions | View Spend · Edit Budget |

---

## 4. Budget Utilization Chart

**Type:** Horizontal grouped bar — Budget vs Spent vs Committed per category.

**Library:** Chart.js 4.x. Colorblind-safe. PNG export.

---

## 5. Branch-wise Budget Breakdown

**Toggle view:** Group-level (default) → Branch-level breakdown

**Branch table:** Branch · Category · Branch Budget · Spent · % Utilized

---

## 6. Set Annual Budget Drawer (COO only)

- **Width:** 560px
- **Fields:** Financial Year · Per-category budget allocation (numeric inputs) · Total auto-calculated
- **Validation:** Total cannot exceed group-approved procurement budget from CFO

---

## 7. Alert Thresholds

- 80% utilization → Yellow warning on category row
- 95% utilization → Red alert + COO notification
- 100% utilization → Locked: new POs for this category require COO override

---

## 8. Toast / Empty / Loader

Standard. Skeleton: summary strip + budget table.

---

## 9. Role-Based UI Visibility

| Element | COO G4 | Ops Mgr G3 |
|---|---|---|
| [Set Annual Budget] | ✅ | ❌ |
| [Edit Budget] per category | ✅ | ❌ |
| View all | ✅ | ✅ |
| Export | ✅ | ✅ |

---

## 10. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/procurement/budget/` | JWT (G3+) | Budget table |
| GET | `/api/v1/group/{id}/procurement/budget/chart/` | JWT (G3+) | Chart data |
| GET | `/api/v1/group/{id}/procurement/budget/branches/` | JWT (G3+) | Branch breakdown |
| PUT | `/api/v1/group/{id}/procurement/budget/` | JWT (G4) | Set annual budget |
| PUT | `/api/v1/group/{id}/procurement/budget/{category}/` | JWT (G4) | Edit category budget |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
