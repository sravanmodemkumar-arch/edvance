# 16 — Zone Academic Dashboard

> **URL:** `/group/ops/zones/<id>/academic/`
> **File:** `16-zone-academic-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** COO G4 · Ops Manager G3 · Zone Director G4 · Zone Academic Coordinator G3 (own zone)

---

## 1. Purpose

Academic performance view for a single zone — branch-level marks, attendance, exam
compliance, lesson plans, teacher performance, and dropout signals. The Zone Academic
Coordinator's primary working dashboard. Links to Division B pages for detailed academic
management; this page provides the zone-level aggregate view.

---

## 2. Role Access

| Role | Access |
|---|---|
| COO G4 | All zones — zone selector |
| Ops Manager G3 | All zones — view |
| Zone Director G4 | Own zone |
| Zone Academic Coordinator G3 | Own zone only |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Operations  ›  Zones  ›  Zone [Name]  ›  Academic
```

### 3.2 Navigation Tabs
```
[Operations →]  [Academic]  [Branch Health →]
```

---

## 4. KPI Summary Bar (6 cards)

| Card | Metric | Colour Rule |
|---|---|---|
| Zone Avg Marks | `74.2%` | Green ≥75% · Yellow 65–75% · Red <65% |
| Attendance Rate | `89.3%` | Green ≥90% · Yellow 80–90% · Red <80% |
| Exam Compliance | `92%` | Green ≥95% · Yellow 85–95% · Red <85% |
| Lesson Plan Submission | `88%` on time | Green ≥90% · Yellow 75–90% · Red <75% |
| Dropout Signals | `5 flagged` | Green =0 · Yellow 1–5 · Red ≥6 |
| Teacher Performance | `78% avg score` | Green ≥80% · Yellow 70–80% · Red <70% |

---

## 5. Sections

### 5.1 Branch Academic Performance Table

**Columns:** Branch · Avg Marks · Attendance % · Exam Compliance · Lesson Plans % · Teacher Score · Dropout Signals · Actions (View · Flag)

**Default sort:** Avg Marks ascending (worst first).

### 5.2 Zone Academic Performance Chart

**Type:** Grouped bar — branch avg marks this term vs last term. Sorted branch by current score.

### 5.3 Upcoming Zone Exams (30 days)

Table: Branch · Subject/Stream · Exam Date · Status (Ready/Pending Paper/Not Scheduled)

### 5.4 Dropout Signals Panel

List of flagged students: Branch · Class · Reason (Attendance <50%, No Fee, Absent 10+ days) · Days Flagged · [Alert Principal]

---

## 6. Drawers

### 6.1 Branch Academic Detail
- **Width:** 640px
- **Tabs:** Performance · Exams · Lesson Plans · Teachers · Dropout

### 6.2 Dropout Alert
- **Width:** 420px modal
- Alert principal + coordinator · Add note · Severity (At Risk / Dropout Likely)

---

## 7. Toast / Empty / Loader

Standard division G pattern. Skeleton: KPI + branch table + chart + exam table.

---

## 8. Role-Based UI Visibility

| Element | Zone Acad G3 | Zone Dir G4 | COO/Ops |
|---|---|---|---|
| Own zone | ✅ Full | ✅ Full | ✅ All zones |
| [Flag Branch] | ✅ | ✅ | ✅ |
| [Alert Principal] (dropout) | ✅ | ✅ | ✅ |
| Edit lesson plan / exam | ❌ (Division B) | ❌ | ❌ |

---

## 9. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/zone/{zone_id}/academic/` | JWT (G3+) | Full academic dashboard |
| GET | `/api/v1/group/{id}/zone/{zone_id}/academic/kpi-cards/` | JWT (G3+) | KPI cards |
| GET | `/api/v1/group/{id}/zone/{zone_id}/academic/branches/` | JWT (G3+) | Branch performance table |
| GET | `/api/v1/group/{id}/zone/{zone_id}/academic/exam-calendar/` | JWT (G3+) | Zone exam list |
| GET | `/api/v1/group/{id}/zone/{zone_id}/academic/dropout-signals/` | JWT (G3+) | Flagged students |
| POST | `/api/v1/group/{id}/zone/{zone_id}/academic/dropout-signals/{id}/alert/` | JWT (G3+) | Alert principal |

---

## 10. HTMX Patterns

| Interaction | hx-trigger | hx-get | hx-target | hx-swap |
|---|---|---|---|---|
| Zone selector | `change` | `/api/.../zone/{id}/academic/` | `#zone-academic-content` | `innerHTML` |
| KPI refresh | `every 5m` | `/api/.../zone/{id}/academic/kpi-cards/` | `#kpi-bar` | `innerHTML` |
| Branch sort | `click` | `/api/.../zone/{id}/academic/branches/?sort={}` | `#acad-branch-table` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
