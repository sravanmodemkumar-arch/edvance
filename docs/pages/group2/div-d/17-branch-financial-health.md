# 17 — Branch Financial Health Monitor

- **URL:** `/group/finance/branch-health/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Roles:** Finance Manager G1 (primary) · CFO G1 · Chairman G5

---

## 1. Purpose

The Branch Financial Health Monitor provides a composite health score for each branch across four financial dimensions: Fee Collection Health, Budget Compliance, Audit Compliance, and Reporting Timeliness. Each dimension is scored 0–100 and weighted to produce a single Branch Financial Health Score.

This page enables early identification of financially struggling or non-compliant branches before problems escalate. A branch with a health score below 60 triggers an automatic alert to the CFO and Finance Manager. The Finance Manager uses this page to prioritise intervention — which branch needs a finance team visit, which needs a collection drive, which needs an audit.

---

## 2. Role Access

| Role | Level | Access |
|---|---|---|
| Group Finance Manager | G1 | Full read + add notes |
| Group CFO | G1 | Full read |
| Group Chairman | G5 | Read — health scores + trend |
| Group Internal Auditor | G1 | Read — audit dimension only |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Finance → Branch Financial Health Monitor
```

### 3.2 Page Header
- **Title:** `Branch Financial Health Monitor`
- **Subtitle:** `[N] Branches · Group Avg Health Score: [X]/100 · [Month Year]`
- **Right-side controls:** `[Month ▾]` `[Branch ▾]` `[Export ↓]`

---

## 4. Health Score Definition

| Dimension | Weight | Measured By |
|---|---|---|
| Fee Collection Health | 40% | Collection rate % vs target |
| Budget Compliance | 25% | Actual vs budgeted spend variance |
| Audit Compliance | 20% | Audit completion + open findings |
| Reporting Timeliness | 15% | Monthly report submission on time |

**Score bands:** 80–100 = Healthy (green) · 60–79 = Watch (amber) · < 60 = Critical (red)

---

## 5. Main Table — Branch Health Scores

| Column | Type | Sortable |
|---|---|---|
| Branch | Text | ✅ |
| Overall Health Score | Number + colour bar | ✅ |
| Fee Collection | Score /100 | ✅ |
| Budget Compliance | Score /100 | ✅ |
| Audit Compliance | Score /100 | ✅ |
| Reporting Timeliness | Score /100 | ✅ |
| Trend (3-month) | Sparkline (↑↓→) | — |
| Status | Badge: Healthy · Watch · Critical | ✅ |
| Notes | Count | — |
| Actions | View Detail · Add Note | — |

### 5.1 Filters

| Filter | Type |
|---|---|
| Status | Multi-select: Healthy · Watch · Critical |
| Health Score Range | Slider: 0–100 |
| Branch | Multi-select |

### 5.2 Search
- Branch name

### 5.3 Pagination
- Server-side · 25 rows/page · Default sort: Overall Health Score asc (worst first)

---

## 6. Drawers

### 6.1 Drawer: `branch-health-detail` — Branch Health Detail
- **Trigger:** View Detail
- **Width:** 720px

**Tab: Score Breakdown**
- Radar chart (4 dimensions) with scores
- Detailed sub-metrics for each dimension

**Tab: 6-Month Trend**
- Line chart: Overall health score trend last 6 months

**Tab: Action Items**
- Auto-generated action items based on low dimension scores
- e.g., "Collection rate at 62% — initiate collection drive" / "3 open audit findings — schedule closure meeting"

**Tab: Notes History**
- Notes added by Finance Manager with date + author

**Actions:**
- [Add Note] — text + date recorded
- [Initiate Collection Drive] — links to Page 33
- [Schedule Audit] — links to Page 39

### 6.2 Drawer: `add-note` — Add Finance Note
| Field | Type | Required |
|---|---|---|
| Note | Textarea | ✅ |
| Action Required | Toggle | ❌ |
| Follow-up Date | Date | ❌ |

---

## 7. Charts

### 7.1 Health Score Distribution (Donut)
- **Segments:** Healthy (green) · Watch (amber) · Critical (red)

### 7.2 Branch Health Ranking (Horizontal Bar)
- **Y-axis:** Branches
- **X-axis:** Health score 0–100
- **Colour-coded bars**
- **Export:** PNG

### 7.3 Group Average Health Trend (Line)
- **X-axis:** Last 6 months
- **Y-axis:** Avg health score

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Note added | "Note added for [Branch]." | Success | 3s |
| Export | "Branch health report exported." | Info | 3s |

---

## 9. Empty States

| Condition | Heading | Description |
|---|---|---|
| All branches healthy | "All branches healthy" | "All branches have a health score ≥ 80." |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Page load | Skeleton table + chart skeletons |
| Month switch | Table skeleton |
| Detail drawer | Spinner + skeleton tabs |

---

## 11. Role-Based UI Visibility

| Element | Finance Mgr G1 | CFO G1 | Chairman G5 |
|---|---|---|---|
| Full table with scores | ✅ | ✅ | ✅ |
| [Add Note] | ✅ | ❌ | ❌ |
| [Initiate Collection Drive] | ✅ | ❌ | ❌ |
| [Schedule Audit] | ✅ | ❌ | ❌ |
| Export | ✅ | ✅ | ❌ |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/finance/branch-health/` | JWT (G1+) | Health scores table |
| GET | `/api/v1/group/{id}/finance/branch-health/{bid}/` | JWT (G1+) | Branch detail |
| GET | `/api/v1/group/{id}/finance/branch-health/{bid}/trend/` | JWT (G1+) | 6-month trend |
| POST | `/api/v1/group/{id}/finance/branch-health/{bid}/notes/` | JWT (G1, Finance Mgr) | Add note |
| GET | `/api/v1/group/{id}/finance/branch-health/charts/` | JWT (G1+) | Chart data |
| GET | `/api/v1/group/{id}/finance/branch-health/export/` | JWT (G1+) | Export |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Filter | `change` | GET `.../branch-health/?status=` | `#health-table` | `innerHTML` |
| Sort | `click` | GET `.../branch-health/?sort=` | `#health-table` | `innerHTML` |
| Detail drawer | `click` | GET `.../branch-health/{bid}/` | `#drawer-body` | `innerHTML` |
| Add note | `submit` | POST `.../branch-health/{bid}/notes/` | `#notes-tab-body` | `innerHTML` |
| Month switch | `change` | GET `.../branch-health/?month=` | `#health-section` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
