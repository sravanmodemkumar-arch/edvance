# 13 — Route Optimization Tool

> **URL:** `/group/transport/routes/optimize/`
> **File:** `13-route-optimization-tool.md`
> **Template:** `portal_base.html`
> **Priority:** P2
> **Role:** Group Route Planning Manager (primary) · Transport Director

---

## 1. Purpose

Intelligence tool to identify and act on route inefficiencies — overloaded routes (student count > bus capacity), underutilised routes (< 50% capacity), redundant stops, unserved student clusters, and excessive route durations. The tool generates actionable suggestions; the Route Planning Manager reviews and implements them.

This is a decision-support page, not an auto-optimization engine. Each suggestion requires human review before action. The goal: reduce average cost-per-student-km, improve on-time performance, and ensure no student is unserved.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Route Planning Manager | G3 | Full — view suggestions, implement | Primary owner |
| Group Transport Director | G3 | View + approve structural changes | Oversight |
| All other transport roles | — | No access | — |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Transport Management  ›  Route Optimization Tool
```

### 3.2 Page Header
- **Title:** `Route Optimization Tool`
- **Subtitle:** `[N] Open Suggestions · [N] Implemented (AY) · Last Analysis: [timestamp]`
- **Right controls:** `Run New Analysis` · `Export Suggestions`

### 3.3 Alert Banner

| Condition | Banner Text | Severity |
|---|---|---|
| Overloaded routes found | "[N] routes are overloaded. Students cannot be safely transported." | Red |
| Unserved student clusters found | "[N] student clusters have no nearby route. Potential new route needed." | Amber |
| Suggestions pending > 14 days | "[N] optimization suggestions have been open for > 14 days without action." | Amber |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule |
|---|---|---|
| Open Suggestions | Total pending action | Yellow > 0 |
| Overloaded Routes | Must-fix | Red > 0 · Green = 0 |
| Underutilised Routes | < 50% capacity | Yellow > 0 |
| Unserved Students | No route nearby | Red > 0 · Green = 0 |
| Estimated Cost Saving | If all suggestions implemented | Green (informational) |
| Avg Route Utilisation | % of capacity used | Green ≥ 75% · Yellow 50–75% · Red < 50% |

---

## 5. Sections

### 5.1 Optimization Suggestions Table

**Filters:**
| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Suggestion Type | Checkbox | Overload Split / Merge / New Route / Stop Addition / Stop Removal / Route Retirement |
| Priority | Radio | All / High / Medium / Low |
| Status | Radio | Open / In Review / Implemented / Dismissed |

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| Suggestion Type | ✅ | Badge |
| Branch | ✅ | |
| Route(s) Affected | ✅ | One or two routes |
| Description | ❌ | Plain-language rationale |
| Students Impacted | ✅ | Count |
| Priority | ✅ | High / Medium / Low badge |
| Estimated Saving | ✅ | ₹/month if applicable |
| Status | ✅ | |
| Created | ✅ | When analysis generated this |
| Actions | ❌ | Review · Implement · Dismiss |

**Pagination:** Server-side · 20/page.

---

### 5.2 Route Utilisation Matrix (Chart)

**Chart — Capacity Utilisation Heatmap (per branch)**
- X-axis: Routes
- Colour intensity: 0–50% light · 50–80% medium · 80–100% green · > 100% red (overloaded)
- Click a cell → route detail drawer (Page 11)

---

### 5.3 Unserved Student Clusters Map

- Students with no route assignment plotted by home area on Leaflet.js map
- Cluster circles sized by student count
- "Nearest active route" line shown for each cluster
- [+ Create Route] button per cluster → opens route-create drawer (Page 11) with branch pre-filled

---

## 6. Drawers

### 6.1 Drawer: `suggestion-review`
- **Trigger:** Actions → Review
- **Width:** 680px
- **Tabs:** Analysis · Impact · Action Plan · History
- **Analysis:** Why this suggestion was generated, data backing it (student counts, capacity, GPS delay history)
- **Impact:** How many students affected, which routes change, cost impact
- **Action Plan:** Steps to implement — what needs to change in Route Manager, Stop Manager, Vehicle Assignment, Student Allocation
- **History:** Who reviewed, notes, status changes

### 6.2 Modal: `dismiss-suggestion`
- **Width:** 480px
- **Fields:** Reason for dismissal (dropdown + free text)
- Dismissed suggestions are archived, not deleted

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Analysis run | "Route analysis complete. [N] new suggestions generated." | Info | 5s |
| Analysis failed | "Route analysis failed. Please retry or check data availability." | Error | 5s |
| Suggestion marked in review | "Suggestion marked as In Review." | Info | 4s |
| Suggestion implemented | "Optimization suggestion implemented. Route Manager updated." | Success | 4s |
| Implement failed | "Failed to implement suggestion. Please retry." | Error | 5s |
| Suggestion dismissed | "Suggestion dismissed and archived." | Info | 4s |
| Dismiss failed | "Failed to dismiss suggestion. Please retry." | Error | 5s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No suggestions | "Routes Are Optimal" | "No optimization suggestions at this time. Run a new analysis after route/student changes." | [Run New Analysis] |
| No filter results | "No Suggestions Match Filters" | "Adjust suggestion type, priority, or status filters." | [Clear Filters] |
| No unserved students | "All Students Served" | "All day scholars have been allocated to a transport route." | — |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page load | Skeleton: 6 KPI cards + suggestion table + chart placeholder + map placeholder |
| Run analysis | Full-page loading overlay with progress indicator (analysis can take 5–30 seconds) |
| Suggestion review drawer | 680px skeleton |

---

## 10. Role-Based UI Visibility

| Element | Route Planning Mgr G3 | Transport Director G3 |
|---|---|---|
| Run Analysis | ✅ | ✅ |
| Implement Suggestion | ✅ | ✅ (structural changes) |
| Dismiss Suggestion | ✅ | ✅ |
| Export | ✅ | ✅ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/transport/optimization/suggestions/` | JWT (G3+) | Suggestions list |
| POST | `/api/v1/group/{group_id}/transport/optimization/run/` | JWT (G3+) | Trigger new analysis |
| GET | `/api/v1/group/{group_id}/transport/optimization/suggestions/{id}/` | JWT (G3+) | Suggestion detail |
| POST | `/api/v1/group/{group_id}/transport/optimization/suggestions/{id}/implement/` | JWT (G3+) | Mark implemented |
| POST | `/api/v1/group/{group_id}/transport/optimization/suggestions/{id}/dismiss/` | JWT (G3+) | Dismiss |
| GET | `/api/v1/group/{group_id}/transport/optimization/utilisation-matrix/` | JWT (G3+) | Chart data |
| GET | `/api/v1/group/{group_id}/transport/optimization/unserved-clusters/` | JWT (G3+) | Map cluster data |

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-get/post | hx-target | hx-swap |
|---|---|---|---|---|
| Filter apply | `click` | GET `.../suggestions/?{filters}` | `#suggestion-table-section` | `innerHTML` |
| Sort | `click` on header | GET `.../suggestions/?sort={col}&dir={asc/desc}` | `#suggestion-table-section` | `innerHTML` |
| Pagination | `click` | GET `.../suggestions/?page={n}` | `#suggestion-table-section` | `innerHTML` |
| Open suggestion drawer | `click` on Review | GET `.../suggestions/{id}/` | `#drawer-body` | `innerHTML` |
| Run analysis | `click` | POST `.../optimization/run/` | `#suggestion-table-section` | `innerHTML` |
| Implement confirm | `click` | POST `.../suggestions/{id}/implement/` | `#suggestion-row-{id}` | `outerHTML` |
| Dismiss confirm | `click` | POST `.../suggestions/{id}/dismiss/` | `#suggestion-row-{id}` | `outerHTML` |
| Export | `click` | GET `.../suggestions/export/` | `#export-btn` | `outerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
