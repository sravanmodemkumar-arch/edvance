# 58 — Academic Trend Analytics

> **URL:** `/group/acad/trends/`
> **File:** `58-academic-trend-analytics.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Roles:** CAO G4 · Academic Director G3 · Academic MIS Officer G1 · Strategic Advisor/Div-A (read-only)

---

## 1. Purpose

The Academic Trend Analytics page provides long-term, multi-term trend analysis of the institution group's key academic performance metrics. While the MIS Report (page 54) captures a snapshot of the current period and the Branch Academic Health Dashboard (page 55) provides a live health score, the Trend Analytics page is specifically designed for strategic analysis — examining how the group has been moving over the past six, twelve, or eighteen terms, and whether improvement initiatives are having a sustained effect.

Six metrics are tracked over time: average exam result percentage, student attendance percentage, dropout rate, CPD completion rate, average teacher rating, and olympiad medal count. For each metric, the page shows a line chart across selected terms with the ability to overlay multiple metrics on the same chart for cross-metric analysis. Year-over-year comparison bar charts enable the CAO to see whether this academic year outperforms last year on every dimension.

A critical feature is the ability to annotate the timeline with contextual events — a new principal appointment in Branch X, a COVID disruption in 2021, a curriculum change, or a major exam format change — so that trend inflections are understood in context rather than treated as unexplained anomalies. The PDF export includes all charts with a narrative placeholder, enabling the MIS Officer to produce a strategic review document for the Chairman or Board without requiring manual chart creation in PowerPoint.

---

## 2. Role Access

| Role | Level | Can View | Can Create/Act | Notes |
|---|---|---|---|---|
| Chief Academic Officer (CAO) | G4 | ✅ Full | ✅ Full — annotate, configure | Full analytical access |
| Group Academic Director | G3 | ✅ Full | ✅ Full — annotate | Full access |
| Group Curriculum Coordinator | G2 | ❌ | ❌ | No access |
| Group Exam Controller | G3 | ❌ | ❌ | No access |
| Group Results Coordinator | G3 | ❌ | ❌ | No access |
| Stream Coordinators (all) | G3 | ❌ | ❌ | No access |
| Group JEE/NEET Integration Head | G3 | ❌ | ❌ | No access |
| Group IIT Foundation Director | G3 | ❌ | ❌ | No access |
| Group Olympiad & Scholarship Coord | G3 | ❌ | ❌ | No access |
| Group Special Education Coordinator | G3 | ❌ | ❌ | No access |
| Group Academic MIS Officer | G1 | ✅ Full | ✅ Full — annotate | Full analytical + annotation access |
| Group Academic Calendar Manager | G3 | ❌ | ❌ | No access |
| Strategic Advisor (Div-A) | Cross-div | ✅ Read-only | ❌ | View charts; cannot annotate or export |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Academic  ›  Academic MIS & Analytics  ›  Academic Trend Analytics
```

### 3.2 Page Header
```
Academic Trend Analytics                                    [Export PDF Report]  [Export XLSX]
Long-term trend analysis — [Group Name]                              (CAO, Academic Dir, MIS)
```

### 3.3 Summary Stats Bar

| Stat | Value |
|---|---|
| Analysis Period | [From Term] to [To Term] — N terms |
| Avg Result % (Latest Term) | X% |
| Avg Result % (Previous Year Same Term) | X% |
| Year-over-Year Delta | ▲/▼ X% |
| Overall Trend Direction | Improving / Stable / Declining (computed from linear regression slope) |

---

## 4. Main Content

### 4.1 Filter and Metric Selection Panel

| Control | Type | Notes |
|---|---|---|
| Scope | Select | Group-wide / Zone / Branch (multi-select) |
| Date range | Term multi-select | Select up to 12 terms (up to 3 academic years) |
| Metrics to display | Multi-checkbox | Avg result % · Attendance % · Dropout rate · CPD completion · Teacher rating · Olympiad medals |
| Normalise axes | Toggle | When on: all metrics scaled to 0–100 for overlay comparison |

[Apply] button · [Reset]

### 4.2 Main Trend Line Chart

- **Type:** Multi-line chart (Chart.js 4.x)
- **X-axis:** Terms (e.g. "2023 Term 1", "2023 Term 2", …)
- **Y-axis:** Left: primary metric scale (%) · Right: secondary scale if metrics are mixed units
- **Each selected metric:** One coloured line, colorblind-safe palette
- **Legend:** Below chart — click legend item to show/hide a line
- **Annotations:** Vertical lines with labels at annotated events
- **Tooltip on hover:** Term · Metric values for all active lines
- **Export:** PNG

### 4.3 Year-over-Year Comparison Chart

- **Type:** Grouped bar chart
- **Data:** For each metric selected, compare: This Year Term N vs Last Year Term N vs Year Before
- **X-axis:** Academic year
- **Y-axis:** Metric value
- **One grouped bar set per metric (shown in tabs or adjacent panels)**
- **Tooltip:** Year · Metric value
- **Export:** PNG

### 4.4 Metric Deep Dive (expandable section per metric)

Each selected metric has an expandable section showing:
- **Trend stats:** Highest term value · Lowest term value · Linear regression slope (improving/declining/flat)
- **Branch comparison mini-table:** Branch · Latest value · vs Group avg · Trend direction

### 4.5 Annotation Manager (sidebar)

Annotations panel on right side of page (collapsible):
- **Table:** Date · Event label · Created by · Edit · Delete (owner only)
- **[+ Add Annotation] button** — opens inline form
- **Annotation form:** Date / Term · Label (max 150 chars) · Type (Academic event / External disruption / Policy change / Leadership change) · Scope (All branches / Zone / Branch)

---

## 5. Drawers & Modals

### 5.1 Modal: `annotation-add`
- **Width:** 400px (also accessible from annotation sidebar)
- **Fields:** Term (Select) · Label (Textarea, max 150 chars) · Type (Select) · Scope (Select + multi-branch)
- **Buttons:** [Add Annotation] · [Cancel]
- **On save:** Vertical marker appears on trend chart at selected term

### 5.2 Modal: `export-config`
- **Trigger:** [Export PDF Report] button
- **Width:** 420px
- **Fields:** Include sections (checkboxes): Trend line chart · YoY comparison · Metric deep dives · Annotations list · Narrative placeholder (editable text area, max 1000 chars)
- **Buttons:** [Generate PDF] · [Cancel]
- PDF: A4, group letterhead, all selected charts embedded, narrative at top.

---

## 6. Charts

### 6.1 Main Trend Line — described in 4.2

### 6.2 Year-over-Year Comparison — described in 4.3

### 6.3 Metric Improvement Heat Calendar (optional, below main chart)
- **Type:** Calendar heatmap
- **Data:** Monthly average of selected metric (e.g. attendance %) — darker green = higher value
- **Shows:** Seasonal patterns (e.g. attendance always dips in December)
- **Export:** PNG

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Filters applied | "Trend data updated — [N] terms in view" | Info | 3s |
| Annotation added | "Event annotation added to timeline" | Success | 4s |
| Annotation deleted | "Annotation removed from timeline" | Info | 4s |
| PDF generating | "Generating PDF report… this may take 10–15 seconds" | Info | 15s |
| PDF ready | "PDF ready — download starting" | Success | 4s |
| XLSX exported | "Data exported to XLSX" | Info | 4s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No terms selected | "Select terms to analyse" | "Use the filter panel to select a date range of at least 2 terms" | — |
| Insufficient data | "Not enough historical data" | "At least 2 terms of data are required to display a trend" | — |
| No metrics selected | "Select at least one metric" | "Choose one or more metrics from the filter panel" | — |
| No annotations yet | "No annotations" | "Add contextual events to make trend inflections meaningful" | [+ Add Annotation] |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: filter panel + chart area + YoY area |
| Filter apply | Spinner in chart area → chart animates in |
| Metric toggle | Smooth chart re-render (no full page reload) |
| YoY chart | Skeleton bar chart |
| PDF generation | Full-page overlay "Generating PDF…" with progress indicator |
| XLSX export | Spinner on export button |

---

## 10. Role-Based UI Visibility

| Element | CAO G4 | Academic Dir G3 | MIS G1 | Div-A Strategic Advisor |
|---|---|---|---|---|
| Trend chart | ✅ | ✅ | ✅ | ✅ |
| YoY comparison | ✅ | ✅ | ✅ | ✅ |
| Metric deep dives | ✅ | ✅ | ✅ | ✅ |
| [+ Add Annotation] | ✅ | ✅ | ✅ | ❌ |
| Edit / delete annotation | ✅ (own + all) | ✅ (own) | ✅ (own) | ❌ |
| [Export PDF] | ✅ | ✅ | ✅ | ❌ |
| [Export XLSX] | ✅ | ✅ | ✅ | ❌ |
| Scope filter — Branch level | ✅ | ✅ | ✅ | ✅ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/acad/trends/` | JWT | Trend data (metric × term matrix) |
| GET | `/api/v1/group/{group_id}/acad/trends/stats/` | JWT | Stats bar data |
| GET | `/api/v1/group/{group_id}/acad/trends/yoy/` | JWT | Year-over-year comparison data |
| GET | `/api/v1/group/{group_id}/acad/trends/calendar-heatmap/` | JWT | Calendar heatmap data |
| GET | `/api/v1/group/{group_id}/acad/trends/annotations/` | JWT | All annotations |
| POST | `/api/v1/group/{group_id}/acad/trends/annotations/` | JWT (G1+, G3+, G4) | Create annotation |
| PUT | `/api/v1/group/{group_id}/acad/trends/annotations/{id}/` | JWT (owner) | Update annotation |
| DELETE | `/api/v1/group/{group_id}/acad/trends/annotations/{id}/` | JWT (owner or G4) | Delete annotation |
| POST | `/api/v1/group/{group_id}/acad/trends/export-pdf/` | JWT (G1, G3, G4) | Generate and return PDF |
| GET | `/api/v1/group/{group_id}/acad/trends/export-xlsx/` | JWT (G1, G3, G4) | XLSX download |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Filter apply | `click` | GET `.../trends/?metrics=&scope=&terms=` | `#trend-charts-container` | `innerHTML` |
| Stats bar update | `click` | GET `.../trends/stats/?filters=` | `#stats-bar` | `innerHTML` |
| Metric toggle (line visibility) | — | Client-side Chart.js only | — | — |
| Annotation add | `submit` | POST `.../trends/annotations/` | `#annotations-list` | `beforeend` |
| Annotation delete | `click` | DELETE `.../trends/annotations/{id}/` | `#annotation-{id}` | `outerHTML` |
| PDF export trigger | `click` | POST `.../trends/export-pdf/` | `#export-result-container` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
