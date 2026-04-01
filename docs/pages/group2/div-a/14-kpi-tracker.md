# 14 — KPI vs Targets Tracker

> **URL:** `/group/gov/kpi-tracker/`
> **File:** `14-kpi-tracker.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Chairman G5 · MD G5 · CEO G4 · President G4 (Academic) · VP G4 (Ops) · Trustee G1 · Advisor G1

---

## 1. Purpose

Real-time cross-branch KPI vs target monitoring. Provides a single view of every group-level
KPI with current values, annual targets, variance, and trend. Both the Strategic Advisor and the
Chairman use this page heavily — the Advisor for 3-year trend analysis, the Chairman for
decision-making on underperforming branches.

KPI categories: Enrollment · Finance · Academic · Staff · Compliance · Operations.

---

## 2. Role Access

| Role | Access | Notes |
|---|---|---|
| Chairman | Full — all KPIs, drill-down, export | |
| MD | Full | |
| CEO | Full | |
| President | Academic KPIs only | Academic category visible |
| VP | Ops + Finance KPIs only | Ops/Finance categories |
| Trustee | Read-only — all KPIs | No drill-down |
| Advisor | Full read + drill-down | Primary research tool |
| Exec Secretary | ❌ | |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  KPI vs Targets Tracker
```

### 3.2 Page Header
```
KPI vs Targets Tracker                                 [Set Thresholds ⚙]  [Export PDF ↓]
FY 2026–27 · as of [date]                              (MD/CEO only for thresholds)
```

### 3.3 View Toggle
- **Card view** (default) — KPI cards arranged in category rows
- **Table view** — all KPIs as rows in a searchable, sortable table

### 3.4 Period Selector
- Dropdown: This Month · This Quarter · This Year (FY) · Last Year · Custom range
- Auto-loads data for selected period

### 3.5 Branch Filter
- Multi-select dropdown: Filter KPIs for selected branches only (or All — default)

---

## 4. KPI Card View (default)

### Category Section: Enrollment

| KPI | Value | Target | % Achieved | Trend | Drill-down |
|---|---|---|---|---|---|
| Total Enrollment | 82,340 | 95,000 | 86.7% | ↑2.3% | `kpi-drill` drawer |
| Day Scholar Enrollment | 52,600 | 60,000 | 87.7% | ↑1.8% | Drawer |
| Hosteler Enrollment | 29,740 | 35,000 | 85.0% | ↑3.1% | Drawer |
| New Admissions | 12,100 | 14,000 | 86.4% | ↓0.5% | Drawer |
| Retention Rate | 94.2% | 96% | 98.1% | ↑0.4pt | Drawer |

### Category Section: Finance

| KPI | Value | Target | % Achieved | Trend |
|---|---|---|---|---|
| Annual Revenue | ₹71.2 Cr | ₹98 Cr | 72.7% | ↑11.4% |
| Monthly Collection Rate | 94.2% | 97% | 97.1% | ↓0.8% |
| Outstanding Fees | ₹1.2 Cr | <₹0.5 Cr | ❌ | ↑0.3 Cr |
| Scholarship Disbursed | ₹38L | ₹50L | 76.0% | ↑5L |

### Category Section: Academic

| KPI | Value | Target | % Achieved | Trend |
|---|---|---|---|---|
| Exam Pass Rate | 94.8% | 96% | 98.8% | ↑0.4pt |
| Average Score % | 72.3% | 75% | 96.4% | ↑1.1pt |
| Toppers (90%+) | 1,240 | 1,500 | 82.7% | ↑80 |
| Curriculum On-Track | 68% branches | 90% | 75.6% | ↓2% |

### Category Section: Staff

| KPI | Value | Target | % Achieved | Trend |
|---|---|---|---|---|
| BGV Compliance | 87% | 100% | 87.0% | ↑3pt |
| POCSO Training | 92% | 100% | 92.0% | ↑5pt |
| Vacancy Rate | 8.2% | <5% | ❌ | ↑0.5pt |
| Staff Retention | 91% | 95% | 95.8% | ↓0.3pt |

### Category Section: Compliance

| KPI | Value | Target | % Achieved | Trend |
|---|---|---|---|---|
| Branches CBSE Compliant | 48/50 | 50/50 | 96.0% | — |
| Compliance Score (avg) | 87/100 | 95/100 | 91.6% | ↑2pt |
| Incidents Resolved <SLA | 91.2% | 95% | 96.0% | ↑2.1% |

### Category Section: Operations

| KPI | Value | Target | % Achieved | Trend |
|---|---|---|---|---|
| Branch SLA Compliance | 91.2% | 95% | 96.0% | ↑1.2pt |
| Open Escalations | 7 | 0 | — (count) | ↓3 |
| Grievances Closed <7d | 82% | 90% | 91.1% | ↑4% |
| Transport Incidents (30d) | 2 | 0 | — (count) | ↓1 |

### KPI Card Design

Each KPI card shows:
- Metric name (small text top-left)
- Current value (large, bold)
- Target value (small, grey)
- Achievement gauge: coloured progress arc (green ≥95% · yellow 75–95% · red <75%)
- Trend arrow + % change vs previous period
- Sparkline (7-day trend mini chart)
- [Drill-down ▶] button (G1 Trustee: no drill-down)

---

## 5. KPI Table View (alternative)

Full table of all KPIs — searchable, sortable.

**Search:** KPI name. Debounce 300ms.

**Filters:** Category · Achievement Status (On Track / Warning / Critical) · Trend (Improving / Declining).

**Columns:**

| Column | Type | Sortable |
|---|---|---|
| KPI Name | Text | ✅ |
| Category | Badge | ✅ |
| Current Value | Text | ✅ |
| Target | Text | ✅ |
| % Achieved | Number + bar | ✅ |
| Status | Badge | ✅ |
| Trend | Arrow + Δ | ✅ |
| Last Updated | Date | ✅ |
| Actions | — | ❌ |

Row action: [Drill-down] → `kpi-drill` drawer.

---

## 6. Drawers

### 6.1 Drawer: `kpi-drill`
- **Trigger:** KPI card [Drill-down] or table row
- **Width:** 480px
- **Tabs:** Trend · By Branch · Variance

#### Tab: Trend
- **Chart:** Line chart — selected KPI value over time (monthly, last 12 months)
- **Benchmark line:** Annual target (dashed)
- **Tooltip:** Month · Value · Target · Variance
- **Period selector:** This year / Last year / 3 years

#### Tab: By Branch
- **Table:** Branch · KPI Value · Target · % Achieved · Status
- **Sortable:** Value column, Achievement %
- **Colour-coded rows:** Red if <75% achieved
- **Export:** CSV

#### Tab: Variance
- **Chart:** Bar chart — KPI value variance from target per branch
- **Positive bars:** Green (above target)
- **Negative bars:** Red (below target)
- **Shows** which branches are dragging the group average down

---

## 7. Alert Rules (G4/G5 only — set thresholds)

**[Set Thresholds ⚙] button:** Opens 480px modal — per KPI, set warning and critical thresholds.

**When threshold breached:** KPI card turns yellow/red · group-level alert sent to role via WhatsApp.

**Example rules:**
- Fee collection rate < 85% → Critical alert → Chairman + CEO
- BGV compliance < 90% → Warning → MD + CEO
- Exam pass rate < 80% → Warning → President

---

## 8. Charts

### 8.1 KPI Achievement Overview (Radar)
- **Type:** Radar chart
- **Data:** One axis per category (Enrollment, Finance, Academic, Staff, Compliance, Ops)
- **Value:** % achievement per category (avg of KPIs in that category)
- **Overlay:** Target (100%) as outer ring
- **Export:** PNG

### 8.2 Category Performance Over Time
- **Type:** Multi-line chart
- **Data:** Avg achievement % per category, monthly (last 12 months)
- **X-axis:** Months
- **Y-axis:** Achievement %
- **Export:** PNG

---

## 9. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Period changed | "KPI data updated for [period]" | Info | 3s |
| Branch filter applied | "KPIs filtered to [N] branches" | Info | 3s |
| Threshold saved | "Alert thresholds saved" | Success | 4s |
| Export started | "KPI report generating…" | Info | 4s |
| Data load error | "Failed to load KPI data. Refresh to try again." | Error | Manual |

---

## 10. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No data for period | "No data for selected period" | "Select a different time period or branch filter" | [Clear Filters] |
| No branches selected | "No branches selected" | "Select at least one branch to view KPIs" | [Select Branches] |
| No annual plan set | "Annual targets not configured" | "Set annual targets in the Strategic Plan to see achievement %" | [Go to Strategic Plan] |

---

## 11. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: view toggle + KPI card grid (12 skeleton cards) |
| Period / branch filter change | KPI card grid shimmer (cards keep shape, values shimmer) |
| Drill-down drawer open | Spinner + chart placeholder in drawer |
| Table view switch | Table skeleton rows |

---

## 12. Role-Based UI Visibility

| Element | Chairman/MD/CEO | President | VP | Trustee | Advisor |
|---|---|---|---|---|---|
| All KPI categories | ✅ | Academic only | Ops + Finance | ✅ read | ✅ read |
| [Drill-down] button | ✅ | ✅ (Academic) | ✅ (Ops/Finance) | ❌ | ✅ |
| [Set Thresholds] | ✅ (MD/CEO) | ❌ | ❌ | ❌ | ❌ |
| Branch filter | ✅ | ✅ | ✅ | ❌ | ✅ |
| [Export PDF] | ✅ | ✅ | ✅ | ❌ | ✅ |
| By Branch tab in drill-down | ✅ | ✅ | ✅ | ❌ | ✅ |

---

## 13. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/kpis/?period=fy&category=all` | JWT | All KPI values |
| GET | `/api/v1/group/{id}/kpis/?category=academic` | JWT (G4 President) | Academic KPIs |
| GET | `/api/v1/group/{id}/kpis/{kpi_id}/trend/` | JWT | KPI trend data |
| GET | `/api/v1/group/{id}/kpis/{kpi_id}/by-branch/` | JWT | Per-branch KPI values |
| GET | `/api/v1/group/{id}/kpis/radar-chart/` | JWT | Radar chart data |
| GET | `/api/v1/group/{id}/kpis/export/?format=pdf` | JWT | Export PDF |
| PUT | `/api/v1/group/{id}/kpis/thresholds/` | JWT (G4/G5) | Save alert thresholds |

---

## HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Card / Table view toggle | `click` | GET `.../kpi-tracker/?view=cards\|table` | `#kpi-content-area` | `innerHTML` |
| Category filter | `click` | GET `.../kpi-tracker/?category=` | `#kpi-content-area` | `innerHTML` |
| Branch filter | `change` | GET `.../kpi-tracker/?branch=` | `#kpi-content-area` | `innerHTML` |
| Period selector | `click` | GET `.../kpi-tracker/?period=` | `#kpi-content-area` | `innerHTML` |
| Open KPI drill drawer | `click` | GET `.../kpi-tracker/{kpi_slug}/drill/` | `#drawer-body` | `innerHTML` |
| Drill tab switch (Trend · By Branch · Variance) | `click` | GET `.../kpi-tracker/{kpi_slug}/drill/?tab=` | `#drill-tab-content` | `innerHTML` |
| Save alert threshold | `submit` | PUT `.../kpi-tracker/{kpi_slug}/threshold/` | `#threshold-result-{kpi_slug}` | `innerHTML` |
| KPI cards auto-refresh | `every 5m` | GET `.../kpi-tracker/?view=cards` | `#kpi-content-area` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
