# 75 — Chapter / Unit Progress Tracker

> **URL:** `/group/acad/chapter-progress/`
> **File:** `75-chapter-progress-tracker.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Academic Director G3 (full) · CAO G4 (view) · Curriculum Coordinator G2 (view) · Stream Coordinators G3 (own stream) · MIS Officer G1 (read)

---

## 1. Purpose

Real-time tracking of actual chapter/unit completion per branch, per class, per subject, vs. the planned
pacing schedule defined in the Syllabus Manager (Page 15).

The Syllabus Manager defines what chapters exist and in what sequence. This page answers the live
operational question: **"Which chapter is each branch actually on right now — and are they behind?"**

**Key distinction from Syllabus Manager:** Syllabus Manager = the plan. This page = actual execution
tracking with date-stamped completion logs.

**Data input:** Branch portal subject teachers log chapter completions. This page aggregates and compares
against planned pacing.

---

## 2. Role Access

| Role | Level | Can View | Can Set Pacing | Can Override | Notes |
|---|---|---|---|---|---|
| Academic Director | G3 | ✅ All branches | ❌ | ✅ (mark chapter completed on behalf) | |
| CAO | G4 | ✅ All | ❌ | ❌ | |
| Curriculum Coordinator | G2 | ✅ All | ✅ (set planned dates) | ❌ | Sets target pacing |
| Stream Coord MPC | G3 | ✅ MPC branches | ❌ | ❌ | |
| Stream Coord BiPC | G3 | ✅ BiPC | ❌ | ❌ | |
| Stream Coord MEC/CEC | G3 | ✅ MEC/CEC | ❌ | ❌ | |
| Stream Coord HEC | G3 | ✅ HEC | ❌ | ❌ | |
| MIS Officer | G1 | ✅ Read (agg only) | ❌ | ❌ | |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Academic Leadership  ›  Chapter Progress Tracker
```

### 3.2 Page Header
```
Chapter / Unit Progress Tracker                          [Set Pacing Schedule]  [Export ↓]
AY 2025–26 · Term 2 · Today: [Date]
```

### 3.3 Summary Stats Bar

| Stat | Value | Color |
|---|---|---|
| Branches Tracked | 46 / 50 | — |
| Branches On Track | 31 | Green |
| Branches Behind (1 chapter) | 11 | Amber |
| Branches Critical (2+ chapters behind) | 4 | Red |
| Subjects with Most Delays | Physics (8 branches) | Red badge |
| Avg Completion vs. Plan | 94% | — |

---

## 4. Main View — Branch × Subject Progress

### 4.1 View Toggle
- **Grid View (default):** Colour-coded grid of Branch × Subject pacing status
- **Table View:** Detailed sortable table with all metrics

### 4.2 Grid View

- **Rows:** Branches
- **Columns:** Subjects (filtered by selected stream/class)
- **Cell colour:**
  - Green: On track (actual chapter ≥ expected chapter for today)
  - Amber: 1 chapter behind
  - Red: 2+ chapters behind
  - Grey: No data logged (branch hasn't started tracking)
- **Cell content:** Actual chapter number / Total chapters
- **Cell click:** Opens branch-subject detail drawer

### 4.3 Table View Columns

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Branch | Text + link | ✅ | |
| Stream | Badge | ✅ | |
| Class | Badge | ✅ | |
| Subject | Badge | ✅ | |
| Total Chapters | Number | ✅ | From Syllabus Manager |
| Expected Chapter Today | Number | ✅ | Based on planned pacing |
| Actual Chapter | Number | ✅ | Last logged by teacher |
| Gap | Number | ✅ | Expected − Actual (negative = ahead) |
| Last Logged | Date | ✅ | Date teacher logged last completion |
| Status | Badge | ✅ | On Track · Behind · Critical · No Data |
| Completion % | Progress bar | ✅ | Actual / Total chapters |

### 4.4 Filters

| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | Branch names |
| Stream | Multi-select | MPC / BiPC / MEC / CEC / HEC / Foundation |
| Class | Multi-select | 6–12 |
| Subject | Multi-select | Subject names |
| Status | Multi-select | On Track · Behind · Critical · No Data |

### 4.5 Search
- Full-text: branch name, subject name
- 300ms debounce

---

## 5. Pacing Schedule

**Pacing** = expected chapter completion date for each chapter in a syllabus.

Set by Curriculum Coordinator based on the academic calendar and term duration.

### 5.1 Pacing Setup Drawer: `pacing-setup`
- **Trigger:** [Set Pacing Schedule] header button
- **Width:** 640px

| Field | Type | Required |
|---|---|---|
| Stream | Select | ✅ |
| Class | Select | ✅ |
| Subject | Select | ✅ |
| Academic Term | Select | ✅ |
| Pacing table | Per-chapter: Chapter Name → Expected Completion Date | ✅ |

- **Auto-distribute:** Button to evenly distribute chapters across working days of the term
- **Import:** Upload CSV (Chapter, Expected Date)
- **Save:** Pacing saved and immediately used for pacing calculations

---

## 6. Drawers

### 6.1 Drawer: `branch-subject-detail`
- **Trigger:** Grid cell click or table row view
- **Width:** 560px

**Tab: Chapter Log**

| Column | Type |
|---|---|
| Chapter # | Number |
| Chapter Name | Text |
| Planned Date | Date |
| Actual Completed Date | Date |
| Logged By | Text (teacher name, masked) |
| Status | Badge (Completed / Not Yet / Skipped) |

**Tab: Subject Overview**
- Branch · Stream · Class · Subject
- Pacing chart: planned vs actual completion % over time (line chart)

**Actions:**
- [Mark Chapter Complete] → Academic Director can log on behalf of branch (audited)
- [Send Pacing Alert] → Notifies branch teacher/Principal to update their log

---

## 7. Alert Logic

| Condition | Alert | Recipient |
|---|---|---|
| Branch 1 chapter behind | In-app badge (amber) | Stream Coordinator |
| Branch 2+ chapters behind | In-app alert (red) | Academic Director |
| Branch 2+ chapters critical for > 7 days | Escalation alert | CAO |
| Branch hasn't logged any chapter in 14 days | "Stale data" flag | Stream Coordinator |

---

## 8. Charts

### 8.1 Pacing Trend by Branch (Line)
- **Data:** Planned % completion vs actual % completion over weeks
- **Each line:** One branch
- **Export:** PNG

### 8.2 Behind by Subject (Bar)
- **Data:** Number of branches behind per subject
- **Color:** Red if > 10 branches behind
- **Export:** PNG

---

## 9. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Pacing saved | "Pacing schedule saved for [Subject] Class [N]." | Success | 4s |
| Chapter marked complete | "Chapter [N] marked complete for [Branch] — [Subject]." | Success | 3s |
| Alert sent | "Pacing alert sent to [Branch] Principal." | Info | 4s |
| Export started | "Export preparing…" | Info | 4s |

---

## 10. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No pacing set | "No pacing schedule defined" | "Set pacing for subjects to start tracking." | [Set Pacing Schedule] |
| No data logged | "No chapter completions logged" | "Branches need to log chapter completions from their portal." | [Send Reminder] |
| All on track | "All branches on track" | "No branches are behind on their chapter pacing." | — |

---

## 11. Loader States

| Trigger | Loader |
|---|---|
| Page load | Skeleton: stats bar + grid/table placeholder |
| Grid/table filter | Inline skeleton |
| Branch-subject drawer | Spinner + skeleton tabs |
| Chart render | Spinner in chart area |

---

## 12. Role-Based UI Visibility

| Element | Academic Dir G3 | CAO G4 | Curr Coord G2 | Stream Coords G3 | MIS G1 |
|---|---|---|---|---|---|
| Grid + table | ✅ All | ✅ All | ✅ All | ✅ Own stream | ✅ Agg only |
| [Set Pacing] | ❌ | ❌ | ✅ | ❌ | ❌ |
| [Mark Chapter Complete] | ✅ | ❌ | ❌ | ❌ | ❌ |
| [Send Pacing Alert] | ✅ | ❌ | ❌ | ❌ | ❌ |
| Charts | ✅ | ✅ | ✅ | ✅ | ✅ |
| Export | ✅ | ✅ | ✅ | ✅ | ✅ |

---

## 13. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/acad/chapter-progress/` | JWT (G1+) | Progress grid/table data |
| GET | `/api/v1/group/{id}/acad/chapter-progress/stats/` | JWT (G1+) | Summary stats |
| GET | `/api/v1/group/{id}/acad/chapter-progress/{branch}/{subject}/` | JWT (G2+) | Branch-subject detail |
| POST | `/api/v1/group/{id}/acad/chapter-progress/{branch}/{subject}/complete/` | JWT (G3, AcadDir) | Mark chapter complete |
| POST | `/api/v1/group/{id}/acad/chapter-progress/{branch}/{subject}/alert/` | JWT (G3) | Send pacing alert |
| GET | `/api/v1/group/{id}/acad/chapter-progress/pacing/` | JWT (G2+) | Get pacing schedules |
| POST | `/api/v1/group/{id}/acad/chapter-progress/pacing/` | JWT (G2) | Create/update pacing |
| GET | `/api/v1/group/{id}/acad/chapter-progress/charts/trend/` | JWT (G1+) | Pacing trend chart |
| GET | `/api/v1/group/{id}/acad/chapter-progress/charts/by-subject/` | JWT (G1+) | Behind-by-subject chart |
| GET | `/api/v1/group/{id}/acad/chapter-progress/export/?format=csv` | JWT (G1+) | Export progress |

---

## 14. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Grid/table search | `input delay:300ms` | GET `.../chapter-progress/?q=` | `#progress-body` | `innerHTML` |
| Filter | `click` | GET `.../chapter-progress/?filters=` | `#progress-section` | `innerHTML` |
| View toggle (grid/table) | `click` | GET `.../chapter-progress/?view=grid` | `#progress-body` | `innerHTML` |
| Grid cell click | `click` | GET `.../chapter-progress/{branch}/{subj}/` | `#drawer-body` | `innerHTML` |
| Mark complete | `click` | POST `.../complete/` | `#chapter-row-{n}` | `outerHTML` |
| Send alert | `click` | POST `.../alert/` | `#alert-btn` | `outerHTML` |
| Pacing setup submit | `submit` | POST `.../pacing/` | `#drawer-body` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
