# 72 — Remedial Programme Manager

> **URL:** `/group/acad/remedial/`
> **File:** `72-remedial-programme-manager.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Academic Director G3 (full) · Stream Coordinators G3 (own stream) · CAO G4 (view)

---

## 1. Purpose

Group-level coordination and monitoring of remedial academic programmes across all branches.
Remedial classes target students performing below threshold in specific subjects. This page provides:
- A trigger mechanism (auto-flag when a branch has >15% students below 40% in a subject)
- A structured programme creation and session tracking workflow
- Pre/post assessment comparison to measure effectiveness

Without this page, remedial is ad-hoc — some branches run it, most don't. No group visibility into
who runs remedials, for which subjects, or whether they work.

---

## 2. Role Access

| Role | Level | Can View | Can Create | Can Track | Notes |
|---|---|---|---|---|---|
| Academic Director | G3 | ✅ All branches | ✅ | ✅ | Primary owner |
| Stream Coord MPC | G3 | ✅ MPC branches | ✅ MPC | ✅ MPC | Own stream only |
| Stream Coord BiPC | G3 | ✅ BiPC branches | ✅ BiPC | ✅ BiPC | |
| Stream Coord MEC/CEC | G3 | ✅ MEC/CEC | ✅ MEC/CEC | ✅ | |
| Stream Coord HEC | G3 | ✅ HEC | ✅ HEC | ✅ | |
| CAO | G4 | ✅ All | ❌ | ❌ | View only |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Academic Leadership  ›  Remedial Programme Manager
```

### 3.2 Page Header
```
Remedial Programme Manager                        [+ New Programme]  [Export Report ↓]
AY 2025–26 · [N] Active Programmes · [M] Branches with Auto-Flag
```

### 3.3 Summary Stats Bar

| Stat | Value |
|---|---|
| Active Programmes | 34 |
| Branches with Auto-Flag (>15% below 40%) | 12 |
| Programmes Completed This Term | 18 |
| Avg Student Improvement | +14.3% |
| Sessions Conducted (this month) | 247 |

---

## 4. Auto-Flag Logic

When branch data shows > 15% of students in a subject scored below 40% in the most recent internal exam:
1. Orange flag appears on the branch row
2. Notification sent to the relevant Stream Coordinator
3. If no remedial programme exists for that branch+subject → [Create Programme] CTA shown prominently
4. If programme exists but is "Not Started" → [Activate Programme] CTA

---

## 5. Main Table

### 5.1 Columns

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Branch | Text + link | ✅ | |
| Stream | Badge | ✅ | |
| Subject | Badge | ✅ | |
| Target Group | Text | ❌ | e.g. "Students < 40% in Chemistry" |
| Students Enrolled | Number | ✅ | |
| Sessions Scheduled | Number | ✅ | |
| Sessions Completed | Number | ✅ | |
| Session Attendance % | Progress bar | ✅ | |
| Pre-Assessment Avg | Number | ✅ | % |
| Post-Assessment Avg | Number | ✅ | % |
| Improvement | Badge | ✅ | +N% (green) or No Change (amber) |
| Status | Badge | ✅ | Active · Completed · Not Started · Paused |
| Auto-Flag | Badge | ✅ | ⚠ Flagged · ✓ Normal |
| Actions | — | ❌ | View · Edit · Complete |

### 5.2 Filters

| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | Branch names |
| Stream | Multi-select | MPC / BiPC / MEC / CEC / HEC |
| Subject | Multi-select | Subject names |
| Status | Multi-select | Active · Completed · Not Started · Paused |
| Auto-Flag | Checkbox | Show flagged branches only |

### 5.3 Search
- Full-text: branch name, subject
- 300ms debounce

---

## 6. Drawers

### 6.1 Drawer: `remedial-create` — New Programme
- **Trigger:** [+ New Programme] header button
- **Width:** 640px

| Field | Type | Required | Validation |
|---|---|---|---|
| Branch | Select | ✅ | |
| Stream | Select | ✅ | |
| Subject | Select | ✅ | |
| Target criteria | Text | ✅ | e.g. "Students scoring < 40% in last exam" |
| Enrolled Students | Multi-select | ✅ | Select from branch student list |
| Schedule — Days | Multi-select | ✅ | Mon / Tue / ... / Sat |
| Schedule — Period | Text | ✅ | e.g. "7th period (after school)" |
| Assigned Teacher | Search + select | ✅ | From branch teacher pool |
| Duration (weeks) | Number | ✅ | |
| Pre-Assessment Date | Date | ✅ | |
| Post-Assessment Date | Date | ✅ | Must be after programme end |
| Group Template | Select | ❌ | Clone from Academic Director's template |

### 6.2 Drawer: `remedial-detail` — Programme Detail
- **Trigger:** View row action
- **Width:** 640px

**Tab: Overview**
- Programme details · Target criteria · Schedule · Teacher assigned

**Tab: Sessions**

| Column | Type |
|---|---|
| Session Date | Date |
| Topic Covered | Text |
| Students Present | Number |
| Attendance % | % |
| Notes | Text |

- **[Log Session]** button — Exam Controller or branch teacher logs completed session

**Tab: Assessment**
- Pre-assessment: Date · Avg score · Distribution chart
- Post-assessment: Date · Avg score · Distribution chart
- Improvement: +N% delta, per-student breakdown (anonymised)

**Tab: Students**
- List of enrolled students (masked names + roll numbers)
- Per student: Pre score · Post score · Improvement · Attendance %

---

## 7. Group Templates

Academic Director can publish a "Group Remedial Session Template":
- Standard session plan format (objectives, activities, time allocation)
- Branches clone template and customise for their context
- Template library: [+ New Template] · list of existing templates

---

## 8. Charts

### 8.1 Programme Coverage by Branch (Bar)
- **Data:** Number of active remedial programmes per branch
- **Color:** Green ≥ 3 programmes · Amber 1–2 · Red 0 (but has auto-flag)
- **Export:** PNG

### 8.2 Pre vs Post Assessment Improvement (Grouped Bar)
- **Data:** Pre avg % and Post avg % per programme
- **Export:** PNG

### 8.3 Auto-Flag Heat Map (Branch × Subject Grid)
- **Data:** Flagged (red) / Clear (green) per branch × subject
- **Click:** Opens programme creation for that cell if no programme exists

---

## 9. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Programme created | "Remedial programme created for [Branch] — [Subject]." | Success | 4s |
| Session logged | "Session on [Date] logged." | Success | 3s |
| Post-assessment recorded | "Post-assessment recorded. Improvement: +[N]%." | Success | 4s |
| Programme completed | "Programme marked complete." | Success | 4s |
| Auto-flag triggered | "[N] branches flagged for remedial. Review recommended." | Warning | 6s |

---

## 10. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No programmes | "No remedial programmes" | "No branches have active remedial programmes." | [+ New Programme] |
| No flags | "No branches flagged" | "All branches have < 15% students below 40%." | — |

---

## 11. Loader States

| Trigger | Loader |
|---|---|
| Page load | Skeleton: stats bar + 8 table rows |
| Filter/search | Inline skeleton rows |
| Detail drawer | Spinner + skeleton tabs |
| Chart load | Spinner in chart area |

---

## 12. Role-Based UI Visibility

| Element | Academic Dir G3 | Stream Coords G3 | CAO G4 |
|---|---|---|---|
| [+ New Programme] | ✅ | ✅ (own stream) | ❌ |
| All branches | ✅ | ❌ Own stream | ✅ Read |
| [Log Session] (in drawer) | ✅ | ✅ | ❌ |
| Auto-flag heatmap | ✅ | ✅ (own stream) | ✅ |
| Group Templates | ✅ Full | ✅ Use/clone | ❌ |
| Charts | ✅ | ✅ (own stream) | ✅ |

---

## 13. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/acad/remedial/` | JWT (G3+) | Programme list |
| GET | `/api/v1/group/{id}/acad/remedial/stats/` | JWT (G3+) | Summary stats |
| POST | `/api/v1/group/{id}/acad/remedial/` | JWT (G3) | Create programme |
| GET | `/api/v1/group/{id}/acad/remedial/{pid}/` | JWT (G3+) | Programme detail |
| PUT | `/api/v1/group/{id}/acad/remedial/{pid}/` | JWT (G3) | Update programme |
| POST | `/api/v1/group/{id}/acad/remedial/{pid}/sessions/` | JWT (G3) | Log session |
| POST | `/api/v1/group/{id}/acad/remedial/{pid}/assessment/` | JWT (G3) | Record assessment |
| POST | `/api/v1/group/{id}/acad/remedial/{pid}/complete/` | JWT (G3) | Mark complete |
| GET | `/api/v1/group/{id}/acad/remedial/auto-flags/` | JWT (G3+) | Auto-flagged branches |
| GET | `/api/v1/group/{id}/acad/remedial/templates/` | JWT (G3) | Group templates |
| POST | `/api/v1/group/{id}/acad/remedial/templates/` | JWT (G3, AcadDir) | Create template |
| GET | `/api/v1/group/{id}/acad/remedial/export/?format=csv` | JWT (G3+) | Export |

---

## 14. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Search | `input delay:300ms` | GET `.../remedial/?q=` | `#remedial-table-body` | `innerHTML` |
| Filter | `click` | GET `.../remedial/?filters=` | `#remedial-section` | `innerHTML` |
| Pagination | `click` | GET `.../remedial/?page=` | `#remedial-section` | `innerHTML` |
| Open detail drawer | `click` | GET `.../remedial/{id}/` | `#drawer-body` | `innerHTML` |
| Create submit | `submit` | POST `.../remedial/` | `#drawer-body` | `innerHTML` |
| Log session | `submit` | POST `.../sessions/` | `#sessions-tab-body` | `innerHTML` |
| Mark complete | `click` | POST `.../complete/` | `#remedial-row-{id}` | `outerHTML` |
| Heatmap cell click | `click` | GET `.../remedial/auto-flags/{branch}/{subject}/` | `#drawer-body` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
