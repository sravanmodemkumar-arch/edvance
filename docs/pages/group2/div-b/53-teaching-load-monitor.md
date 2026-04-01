# 53 — Teaching Load Monitor

> **URL:** `/group/acad/teacher-load/`
> **File:** `53-teaching-load-monitor.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Roles:** Academic Director G3 · CAO G4 · Stream Coordinators G3 (own stream)

---

## 1. Purpose

The Teaching Load Monitor tracks the number of teaching periods per week assigned to every teacher across all branches, detecting overload and underload situations that affect teaching quality and teacher wellbeing. In a large group where timetables are managed at the branch level, the group's Academic Director has no visibility into whether branches are distributing teaching load equitably or sustainably — some branches may overload a few specialist teachers while others leave capable teachers underutilised.

Overloaded teachers — those teaching more than 32 periods per week — cannot prepare adequate lesson plans, mark student work promptly, or maintain the quality of instruction that drives student results. Underloaded teachers represent wasted salary expenditure and untapped capacity. Branches with more than 20% of their teachers in the overloaded category are automatically flagged in the CAO dashboard, triggering a review conversation with the branch principal.

The load data is read from branch-level timetable data entered in the branch portal. This page aggregates it and presents it in a searchable, filterable table with configurable load thresholds (the default range of 18–28 periods per week is set by the CAO but can be adjusted). The Teaching Load Monitor does not create or edit timetables — it is a monitoring and escalation tool only.

---

## 2. Role Access

| Role | Level | Can View | Can Create/Act | Notes |
|---|---|---|---|---|
| Chief Academic Officer (CAO) | G4 | ✅ Full | ✅ Configure thresholds | Sets acceptable load range |
| Group Academic Director | G3 | ✅ Full | ✅ Full (configure + escalate) | Primary owner |
| Group Curriculum Coordinator | G2 | ❌ | ❌ | No access |
| Group Exam Controller | G3 | ❌ | ❌ | No access |
| Group Results Coordinator | G3 | ❌ | ❌ | No access |
| Stream Coord — MPC | G3 | ✅ MPC teachers | ❌ | View own stream teachers |
| Stream Coord — BiPC | G3 | ✅ BiPC teachers | ❌ | View own stream teachers |
| Stream Coord — MEC/CEC | G3 | ✅ MEC/CEC teachers | ❌ | View own stream teachers |
| Group JEE/NEET Integration Head | G3 | ❌ | ❌ | No access |
| Group IIT Foundation Director | G3 | ❌ | ❌ | No access |
| Group Olympiad & Scholarship Coord | G3 | ❌ | ❌ | No access |
| Group Special Education Coordinator | G3 | ❌ | ❌ | No access |
| Group Academic MIS Officer | G1 | ❌ | ❌ | No access |
| Group Academic Calendar Manager | G3 | ❌ | ❌ | No access |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Academic  ›  Teacher Performance & CPD  ›  Teaching Load Monitor
```

### 3.2 Page Header
```
Teaching Load Monitor                                              [Export ↓]  [Configure Thresholds]
Periods per week — all branches · Acceptable: 18–28 · Overloaded: >32 · Underloaded: <12
```

### 3.3 Summary Stats Bar

| Stat | Value |
|---|---|
| Total Teachers | Count |
| Overloaded (> configured max) | Count — red |
| Normal Load | Count — green |
| Underloaded (< configured min) | Count — amber |
| Branches with > 20% Overloaded | Count — alert red |
| Last Data Sync from Branches | Datetime |

---

## 4. Main Content

### 4.1 Search
- Full-text across: Teacher name, Teacher ID, Branch name
- 300ms debounce

### 4.2 Advanced Filters (slide-in drawer, active chips, Clear All)

| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Subject | Multi-select | |
| Stream | Multi-select | MPC / BiPC / MEC / CEC / Foundation |
| Load Status | Multi-select | Overloaded / Normal / Underloaded |

### 4.3 Columns

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Teacher ID | Text | ✅ | |
| Teacher Name | Text | ✅ | |
| Branch | Text | ✅ | |
| Subject | Text | ✅ | |
| Stream | Badge | ✅ | |
| Periods / Week | Number | ✅ | From branch timetable |
| Students per Class (avg) | Number | ✅ | Average class size |
| Sections Covered | Number | ✅ | Number of sections this teacher teaches |
| Total Students | Number | ✅ | Sum across all sections |
| Load Status | Badge | ✅ | Overloaded (red) / Normal (green) / Underloaded (amber) |
| Actions | — | ❌ | |

**Default sort:** Load Status (Overloaded first), then Periods/Week descending.

**Pagination:** Server-side · Default 25/page · Selector 10/25/50/All · Page jump input.

### 4.4 Row Actions

| Action | Visible To | Drawer | Notes |
|---|---|---|---|
| View Timetable | Academic Dir, CAO, Stream Coords | `teacher-load-detail` drawer 480px | Period-by-period weekly timetable |
| Escalate to Branch | Academic Dir | Inline confirm | Sends alert to branch principal about this teacher's load |

### 4.5 Bulk Actions (Academic Director only)

| Action | Notes |
|---|---|
| Export Selected (XLSX) | Load data for selected teachers |
| Alert Branch Principals (Overloaded branches) | Sends batch alert to branch principals in selected overloaded branches |

---

## 5. Drawers & Modals

### 5.1 Drawer: `teacher-load-detail`
- **Trigger:** View Timetable row action
- **Width:** 480px
- **Header:** `[Teacher Name] — Weekly Timetable — [Branch]`

**Timetable grid:**
| | Mon | Tue | Wed | Thu | Fri | Sat |
|---|---|---|---|---|---|---|
| Period 1 | Phy XI-A | — | Phy XI-B | Phy XI-A | — | Phy XI-C |
| Period 2 | — | Chem XI-A | — | — | Phy X-A | — |
| … | | | | | | |

Colour-coded: Regular class (grey) · Additional load (amber) · Free period (white).

**Summary below grid:**
- Total periods: N/week
- Sections: N
- Total students taught: N
- Load status badge
- Last updated from branch: datetime

### 5.2 Modal: `configure-thresholds`
- **Trigger:** [Configure Thresholds] header button
- **Width:** 420px
- **Visible to:** Academic Dir, CAO

| Field | Type | Required | Notes |
|---|---|---|---|
| Normal range — minimum periods/week | Number | ✅ | Default 18 |
| Normal range — maximum periods/week | Number | ✅ | Default 28 |
| Overloaded threshold (above this = overloaded) | Number | ✅ | Default 32 |
| Underloaded threshold (below this = underloaded) | Number | ✅ | Default 12 |
| Branch alert threshold (% overloaded triggers CAO alert) | Number (%) | ✅ | Default 20% |

- **Buttons:** [Save Thresholds] · [Reset to Default] · [Cancel]

---

## 6. Charts

### 6.1 Load Distribution (Histogram)
- **Type:** Histogram
- **Data:** Count of teachers by periods/week band (0–10, 10–15, 15–18, 18–28, 28–32, 32+)
- **Colour:** Red for overloaded bands, green for normal, amber for underloaded
- **Tooltip:** Band · Count
- **Export:** PNG

### 6.2 Overloaded Teachers by Branch (Bar)
- **Type:** Vertical bar
- **Data:** Count (or %) of overloaded teachers per branch
- **Threshold line:** Horizontal line at CAO-configured % threshold
- **Tooltip:** Branch · Overloaded: N · % of total
- **Export:** PNG

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Thresholds saved | "Load thresholds updated. Table recalculated." | Success | 4s |
| Escalation sent | "Alert sent to [Branch] principal about [Teacher Name]'s load" | Success | 4s |
| Bulk alert sent | "Branch principal alerts sent to [N] branches" | Success | 4s |
| Export started | "Export preparing… download will start shortly" | Info | 4s |
| Data stale warning | "Branch timetable data last synced > 7 days ago — data may be outdated" | Warning | Manual dismiss |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No timetable data | "No timetable data available" | "Teaching load data is pulled from branch timetables. Ensure branches have entered timetables in the branch portal." | — |
| No overloaded teachers | "No overloaded teachers" | "All teachers are within the configured normal load range" | — |
| No results match filters | "No teachers match" | "Clear filters to see all teaching load records" | [Clear Filters] |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: stats bar + table (10 rows) + chart areas |
| Table filter/search/sort/page | Inline skeleton rows |
| Timetable drawer open | Spinner → grid renders |
| Configure modal open | Spinner (minimal) |
| Charts load | Skeleton chart areas |

---

## 10. Role-Based UI Visibility

| Element | Academic Dir G3 | CAO G4 | Stream Coord G3 |
|---|---|---|---|
| Full table | ✅ | ✅ | ✅ (own stream) |
| [Configure Thresholds] | ✅ | ✅ | ❌ |
| Escalate to Branch | ✅ | ❌ | ❌ |
| Bulk alert | ✅ | ❌ | ❌ |
| Export | ✅ | ✅ | ❌ |
| Charts | ✅ | ✅ | ✅ (own stream) |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/acad/teacher-load/` | JWT | List teacher load records |
| GET | `/api/v1/group/{group_id}/acad/teacher-load/stats/` | JWT | Stats bar |
| GET | `/api/v1/group/{group_id}/acad/teacher-load/{teacher_id}/timetable/` | JWT | Weekly timetable detail |
| POST | `/api/v1/group/{group_id}/acad/teacher-load/{teacher_id}/escalate/` | JWT (G3 Acad Dir) | Send escalation to branch |
| POST | `/api/v1/group/{group_id}/acad/teacher-load/bulk-alert/` | JWT (G3 Acad Dir) | Bulk branch alerts |
| GET | `/api/v1/group/{group_id}/acad/teacher-load/thresholds/` | JWT | Current threshold config |
| PUT | `/api/v1/group/{group_id}/acad/teacher-load/thresholds/` | JWT (G3 Acad Dir, G4) | Update thresholds |
| GET | `/api/v1/group/{group_id}/acad/teacher-load/export/?format=xlsx` | JWT (G3/G4) | Export |
| GET | `/api/v1/group/{group_id}/acad/teacher-load/charts/distribution/` | JWT | Histogram data |
| GET | `/api/v1/group/{group_id}/acad/teacher-load/charts/overloaded-by-branch/` | JWT | Bar chart data |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Search | `input delay:300ms` | GET `.../teacher-load/?q=` | `#load-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../teacher-load/?filters=` | `#load-table-section` | `innerHTML` |
| Sort column | `click` | GET `.../teacher-load/?sort=&dir=` | `#load-table-section` | `innerHTML` |
| Pagination | `click` | GET `.../teacher-load/?page=` | `#load-table-section` | `innerHTML` |
| Timetable drawer | `click` | GET `.../teacher-load/{tid}/timetable/` | `#drawer-body` | `innerHTML` |
| Escalate inline | `click` | POST `.../teacher-load/{tid}/escalate/` | `#toast-container` | `beforeend` |
| Threshold save | `submit` | PUT `.../teacher-load/thresholds/` | `#load-table-section` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
