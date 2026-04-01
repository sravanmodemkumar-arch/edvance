# 05 — Zone Academic Coordinator Dashboard

> **URL:** `/group/ops/zone-academic/`
> **File:** `05-zone-academic-coordinator-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Group Zone Academic Coordinator (G3) — exclusive landing page
> **Applicable:** Large groups only

---

## 1. Purpose

Post-login landing for the Group Zone Academic Coordinator. Responsible for academic
oversight within one zone — ensuring exam schedules are followed, lesson plan submissions
are on time, teacher performance is tracked, and academic compliance is met across all
branches in the zone. Works under the Zone Director and coordinates with group-level
Division B (Academic Leadership).

> **Scoping rule:** Zone Academic Coordinator sees only their assigned zone's branches.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Zone Academic Coordinator | G3 | Full — own zone academic data | Exclusive |
| Zone Director | G4 | View | Has own dashboard |
| COO | G4 | View all | |
| Operations Manager | G3 | View | |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Zone Academic Dashboard  ›  Zone [Name]
```

### 3.2 Page Header
```
Zone [Name] — Zone Academic Coordinator            [Academic Report ↓]  [Settings ⚙]
[Name] · Academic oversight for [N] branches · Last login: [date time]
```

---

## 4. KPI Summary Bar (6 cards)

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Zone Avg Marks | `74.2%` this term | Green ≥75% · Yellow 65–75% · Red <65% | → Page 16 |
| Exam Calendar Compliance | `92%` branches on schedule | Green ≥95% · Yellow 85–95% · Red <85% | → Page 16 |
| Lesson Plans Submitted | `88% on time this month` | Green ≥90% · Yellow 75–90% · Red <75% | → Page 16 |
| Attendance Rate | `89.3% zone average` | Green ≥90% · Yellow 80–90% · Red <80% | → Page 16 |
| Dropout Signals | `5 students flagged` | Green =0 · Yellow 1–5 · Red ≥6 | → Page 16 |
| IEP Pending Actions | `2 special needs IEPs overdue` | Green =0 · Red ≥1 | → Division B |

**HTMX:** `every 5m` → `/api/v1/group/{id}/zone/{zone_id}/academic/kpi-cards/` → `#kpi-bar`

---

## 5. Sections

### 5.1 Branch Academic Health Table

**Search:** Branch name. Debounce 300ms.

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| Branch Name | ✅ | Link → academic detail drawer |
| Stream(s) | ❌ | MPC / BiPC / MEC etc. |
| Zone Avg Marks | ✅ | This term |
| Attendance % | ✅ | This month |
| Exam Compliance | ✅ | % on-schedule exams |
| Lesson Plans % | ✅ | On-time submission rate |
| Teacher Performance | ✅ | Avg score |
| Dropout Signals | ✅ | Count, red if >0 |
| Actions | ❌ | View · Flag for Zone Director |

**Default sort:** Avg Marks ascending (worst first).

---

### 5.2 Upcoming Zone Exam Calendar

> Exams across all zone branches in next 30 days.

**Columns:** Branch · Subject · Stream · Exam Date · Status (Scheduled/Pending Paper/Ready)

**Actions:** [View in Full Calendar →] → Division B pages.

---

### 5.3 Zone Academic Performance Chart

**Type:** Grouped bar — Avg Marks per branch, this term vs last term.

**Colour:** Blue (this term) · Grey (last term). Colorblind-safe. Legend. PNG export.

---

### 5.4 Teacher Performance Summary

> Zone-level view of teacher performance across branches.

**Columns:** Branch · Subject · Teacher Count · Avg Performance Score · Below-threshold Count

**Threshold:** Performance score < 70 highlighted red.

**Link:** [View Full Teacher Performance →] → Division B teacher tracking pages.

---

## 6. Drawers & Modals

### 6.1 Drawer: Branch Academic Detail
- **Width:** 640px
- **Tabs:** Performance · Exam Schedule · Lesson Plans · Teachers · Dropout Signals
- **Zone Academic Coord actions:** Flag branch for Zone Director review · Add observation note

---

## 7. Toast Messages

| Action | Toast | Type |
|---|---|---|
| Branch flagged | "Branch flagged for Zone Director review" | Success · 4s |
| Report exported | "Academic report export started" | Info · 4s |

---

## 8. Empty States

| Condition | Heading | CTA |
|---|---|---|
| No zone assigned | "No zone assigned yet" | Contact Zone Director |
| No academic data this term | "No exam data for this period" | — |

---

## 9. Loader States

Page load: Skeleton KPI bar + branch table + exam calendar + chart.

---

## 10. Role-Based UI Visibility

| Element | Zone Acad Coord G3 | Zone Director G4 | COO G4 |
|---|---|---|---|
| Own zone data | ✅ Full | ✅ Full | ✅ Full |
| Other zones | ❌ Blocked | Own zone only | ✅ All |
| [Flag branch] action | ✅ | ✅ | ✅ |
| Write/edit lesson plan | ❌ (Division B responsibility) | ❌ | ❌ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/zone/{zone_id}/academic/dashboard/` | JWT (G3+) | Full page data |
| GET | `/api/v1/group/{id}/zone/{zone_id}/academic/kpi-cards/` | JWT (G3+) | KPI cards |
| GET | `/api/v1/group/{id}/zone/{zone_id}/academic/branches/` | JWT (G3+) | Branch academic table |
| GET | `/api/v1/group/{id}/zone/{zone_id}/academic/exam-calendar/` | JWT (G3+) | Zone exam schedule |
| GET | `/api/v1/group/{id}/zone/{zone_id}/academic/performance-chart/` | JWT (G3+) | Chart data |
| POST | `/api/v1/group/{id}/ops/branches/{branch_id}/flag/` | JWT (G3) | Flag for Zone Director |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-get | hx-target | hx-swap |
|---|---|---|---|---|
| Branch search | `input delay:300ms` | `/api/.../zone/{id}/academic/branches/?q={}` | `#acad-branch-table-body` | `innerHTML` |
| KPI auto-refresh | `every 5m` | `/api/.../zone/{id}/academic/kpi-cards/` | `#kpi-bar` | `innerHTML` |
| Open branch detail | `click` | `/api/.../branches/{id}/academic-detail/` | `#drawer-body` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
