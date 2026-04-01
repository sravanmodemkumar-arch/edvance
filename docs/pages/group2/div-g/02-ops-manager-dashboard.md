# 02 — Operations Manager Dashboard

> **URL:** `/group/ops/manager/`
> **File:** `02-ops-manager-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Group Operations Manager (G3) — exclusive landing page

---

## 1. Purpose

Primary post-login landing for the Group Operations Manager. Operational command centre
focused on SLA enforcement, grievance resolution, coordinator performance, escalation
management, and branch compliance. The Operations Manager is the day-to-day executor of
all operational decisions across branches.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Operations Manager | G3 | Full — all sections | Exclusive dashboard |
| Group COO | G4 | View only | Has own dashboard at `/group/ops/coo/` |
| All others | — | — | Redirected |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Operations Manager Dashboard
```

### 3.2 Page Header
```
Welcome back, [Manager Name]                       [Generate MIS ↓]  [Settings ⚙]
[Group Name] — Group Operations Manager · Last login: [date time]
```

### 3.3 Alert Banner
- Shown when: SLA breach unresolved >12h · Grievance P1 unresolved >4h · Coordinator unassigned branch >7 days
- Collapsible, max 5 alerts

---

## 4. KPI Summary Bar (6 cards)

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Open Escalations | `12 total · 2 P1` | Green =0 P1 · Yellow 1 · Red ≥2 | → Page 12 |
| SLA Compliance | `92.4%` this month | Green ≥95% · Yellow 85–95% · Red <85% | → Page 08 |
| Open Grievances | `8 open · 2 overdue` | Green = none overdue · Yellow 1–2 · Red ≥3 | → Page 11 |
| Visits This Month | `14 / 22 planned` | Green ≥90% plan · Yellow 70–90% · Red <70% | → Page 10 |
| Coordinator Coverage | `50 / 50 branches` | Green = 100% · Red < 100% | → Page 09 |
| Compliance Score | `87% avg group-wide` | Green ≥90% · Yellow 80–90% · Red <80% | → Page 13 |

**HTMX:** `every 5m` → `hx-get="/api/v1/group/{id}/ops-manager/kpi-cards/"` → `#kpi-bar`

---

## 5. Sections

### 5.1 Today's Priority Queue

> Grievances and escalations requiring action today.

**Display:** Card list, max 5, sorted by severity then age. "View all →" → Pages 11/12.

**Card fields:** Type (Grievance / Escalation) · Severity badge · Branch · Subject · Raised by · Age · [Assign] [Resolve] [View]

---

### 5.2 Coordinator Performance Snapshot

> How are branch coordinators performing this month?

**Display:** Table (not full table — top/bottom performers by visit completion rate).

| Column | Notes |
|---|---|
| Coordinator Name | Link → coordinator profile in Page 09 |
| Branches Assigned | Count |
| Visits Planned | Count |
| Visits Completed | Count + % |
| Issues Raised | Count |
| Overdue Tasks | Count, red if >0 |

**Actions:** [View All Coordinators →] → Page 09.

---

### 5.3 SLA Summary by Branch

> Top 10 worst-performing branches by SLA compliance.

**Columns:** Branch · Zone · SLA % · Breaches This Month · Last Breach Date · [View SLA Details]

**Link:** [View Full SLA Tracker →] → Page 08.

---

### 5.4 Grievance Aging Chart

**Type:** Horizontal bar chart — grievances grouped by days open (0–3d, 4–7d, 8–14d, >14d).

**Colour:** Green · Yellow · Orange · Red.

**Tooltip:** Count + % of total open grievances.

---

### 5.5 Escalation Volume Chart

**Type:** Bar chart — escalations raised vs resolved per month (12 months).

**Colour:** Red (raised) + Green (resolved). Legend. PNG export.

---

### 5.6 Quick Access Grid

6 tiles:
| Tile | Label | Link |
|---|---|---|
| 1 | Grievance Centre | `/group/ops/grievances/` |
| 2 | Escalation Tracker | `/group/ops/escalations/` |
| 3 | Branch SLA Tracker | `/group/ops/branches/sla/` |
| 4 | Visit Scheduler | `/group/ops/visits/` |
| 5 | Coordinator Hub | `/group/ops/coordinators/` |
| 6 | Compliance Checklists | `/group/ops/compliance/` |

---

## 6. Drawers & Modals

### 6.1 Drawer: `grievance-detail` (opened from Priority Queue)
- **Width:** 640px
- **Tabs:** Overview · Timeline · Actions · Escalation History
- **Actions tab:** [Assign to self] [Assign to coordinator] [Escalate to COO] [Mark Resolved]

### 6.2 Modal: Resolve confirmation
- **Width:** 420px
- **Content:** Resolution type (Resolved / No Action Needed / Withdrawn by Complainant) + resolution notes (required, min 30 chars)

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Grievance assigned | "Grievance assigned to [Name]" | Success | 4s |
| Grievance resolved | "Grievance resolved and archived" | Success | 4s |
| Escalation updated | "Escalation status updated" | Success | 4s |
| MIS export triggered | "MIS generation started" | Info | 4s |

---

## 8. Empty States

| Condition | Heading | CTA |
|---|---|---|
| No priority queue items | "All clear — nothing urgent" | — |
| No open grievances | "No open grievances" | — |
| No SLA breaches | "All branches meeting SLA targets" | — |

---

## 9. Loader States

| Trigger | Loader |
|---|---|
| Page load | Skeleton KPI bar + 2 tables + 2 charts |
| KPI auto-refresh | Shimmer over values |
| Coordinator table sort | Inline skeleton rows |
| Drawer open | Centred spinner in drawer |

---

## 10. Role-Based UI Visibility

| Element | Ops Mgr G3 | COO G4 (view mode) |
|---|---|---|
| Page | ✅ Full | ✅ View (no actions) |
| [Assign] / [Resolve] buttons | ✅ | ❌ Hidden |
| [Generate MIS] button | ✅ | ✅ |
| Coordinator performance table | ✅ Full | ✅ Read-only |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/ops-manager/dashboard/` | JWT (G3+) | Full page data |
| GET | `/api/v1/group/{id}/ops-manager/kpi-cards/` | JWT (G3+) | KPI cards (auto-refresh) |
| GET | `/api/v1/group/{id}/ops/priority-queue/` | JWT (G3+) | Today's priority items |
| GET | `/api/v1/group/{id}/ops/coordinators/performance/` | JWT (G3+) | Coordinator performance table |
| GET | `/api/v1/group/{id}/ops/sla-summary/?limit=10&sort=sla_asc` | JWT (G3+) | Worst SLA branches |
| GET | `/api/v1/group/{id}/ops/grievance-aging/` | JWT (G3+) | Grievance aging data |
| GET | `/api/v1/group/{id}/ops/escalation-trend/` | JWT (G3+) | 12-month escalation chart |
| POST | `/api/v1/group/{id}/grievances/{gid}/assign/` | JWT (G3) | Assign grievance |
| POST | `/api/v1/group/{id}/grievances/{gid}/resolve/` | JWT (G3) | Resolve grievance |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-get/post | hx-target | hx-swap |
|---|---|---|---|---|
| KPI auto-refresh | `every 5m` | `/api/.../ops-manager/kpi-cards/` | `#kpi-bar` | `innerHTML` |
| Open grievance detail | `click` | `/api/.../grievances/{id}/` | `#drawer-body` | `innerHTML` |
| Assign grievance submit | `click` | POST `/api/.../grievances/{id}/assign/` | `#priority-queue` | `innerHTML` |
| Coordinator table sort | `click` | `/api/.../coordinators/performance/?sort={col}` | `#coordinator-table` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
