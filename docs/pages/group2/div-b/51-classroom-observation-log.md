# 51 — Classroom Observation Log

> **URL:** `/group/acad/teacher-observations/`
> **File:** `51-classroom-observation-log.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Academic Director G3 · CAO G4 · Stream Coordinators G3 (own stream) · Group Inspection Officer/Div-P (create)

---

## 1. Purpose

The Classroom Observation Log is the structured record of all formal classroom observations conducted by group-level academic staff and inspection officers across all branches. Classroom observation is the highest-quality input into teacher performance assessment — it captures what a composite score cannot: whether the teacher actually understands their subject, whether students are engaged, whether the lesson has a clear structure, and whether the teacher manages the classroom professionally.

In the Indian education ecosystem, classroom observation as a formal practice is inconsistently applied. Many institutions conduct observations once a year as a formality. This page is designed to change that by making observation records visible at the group level, searchable by branch and subject, and directly linked to the teacher performance appraisal. When the Academic Director creates a new appraisal (page 50), the observation rating is auto-pulled from this log — it is not a self-reported number.

The observation rubric has ten criteria, each rated 1–5, giving a maximum raw score of 50 which is normalised to a 5-point scale for the performance tracker. The criteria cover the full spectrum of effective teaching: subject knowledge, lesson structure, student engagement, questioning technique, formative assessment, classroom management, differentiation for mixed-ability groups, use of materials and technology, time management, and professional conduct. Observers are trained to use this rubric consistently, and the log captures both the scores and free-text observations so the evidence behind ratings is always accessible.

---

## 2. Role Access

| Role | Level | Can View | Can Create/Act | Notes |
|---|---|---|---|---|
| Chief Academic Officer (CAO) | G4 | ✅ Full | ❌ No create | Supervisory view of all observations |
| Group Academic Director | G3 | ✅ Full | ✅ Full CRUD | Primary owner; conducts group-level observations |
| Group Curriculum Coordinator | G2 | ❌ | ❌ | No access |
| Group Exam Controller | G3 | ❌ | ❌ | No access |
| Group Results Coordinator | G3 | ❌ | ❌ | No access |
| Stream Coord — MPC | G3 | ✅ MPC teachers only | ❌ | View own stream |
| Stream Coord — BiPC | G3 | ✅ BiPC teachers only | ❌ | View own stream |
| Stream Coord — MEC/CEC | G3 | ✅ MEC/CEC teachers only | ❌ | View own stream |
| Group JEE/NEET Integration Head | G3 | ❌ | ❌ | No access |
| Group IIT Foundation Director | G3 | ❌ | ❌ | No access |
| Group Olympiad & Scholarship Coord | G3 | ❌ | ❌ | No access |
| Group Special Education Coordinator | G3 | ❌ | ❌ | No access |
| Group Academic MIS Officer | G1 | ❌ | ❌ | No access |
| Group Academic Calendar Manager | G3 | ❌ | ❌ | No access |
| Group Inspection Officer (Div-P) | Cross-div | ✅ Full | ✅ Create observations | Creates observations during academic audits |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Academic  ›  Teacher Performance & CPD  ›  Classroom Observation Log
```

### 3.2 Page Header
```
Classroom Observation Log                                [+ New Observation]  [Export ↓]
Structured observations — all branches                           (Academic Dir, Div-P)
```

### 3.3 Summary Stats Bar

| Stat | Value |
|---|---|
| Total Observations (This Term) | Count |
| Branches Observed | Count (of total branches) |
| Avg Rating (Group) | X.X / 5 |
| Observations With Follow-up Due | Count — amber |
| Teachers Not Observed This Term | Count — red |

---

## 4. Main Content

### 4.1 Search
- Full-text across: Teacher name, Teacher ID, Observer name, Branch name
- 300ms debounce · Highlights match in Teacher Name column

### 4.2 Advanced Filters (slide-in drawer, active chips, Clear All)

| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Subject | Multi-select | All subjects |
| Stream | Multi-select | MPC / BiPC / MEC / CEC / Foundation |
| Rating Band | Select | Excellent (4.5–5.0) / Good (3.5–4.4) / Average (2.5–3.4) / Needs Improvement (< 2.5) |
| Observer Type | Select | Group (Academic Dir / Div-P) / Branch |
| Follow-up Due | Select | Yes / No / Overdue |
| Date range | Date range picker | |
| Teacher acknowledgement | Select | Acknowledged / Pending |

Stream Coords see only their own stream (server-side enforced).

### 4.3 Columns

| Column | Type | Sortable | Notes |
|---|---|---|---|
| ☐ | Checkbox | — | Academic Dir bulk select |
| Observation ID | Text | ✅ | System-generated |
| Teacher | Text | ✅ | Name + ID |
| Branch | Text | ✅ | |
| Subject | Text | ✅ | |
| Class | Badge | ✅ | |
| Observer | Text | ✅ | Name + role |
| Date | Date | ✅ | |
| Rating | Stars (1–5) | ✅ | Visual star display + numeric |
| Strengths | Text (truncated) | ❌ | First 60 chars; full in drawer |
| Areas for Improvement | Text (truncated) | ❌ | First 60 chars |
| Follow-up Due | Date | ✅ | Amber/red if overdue |
| Acknowledgement | Badge | ✅ | Acknowledged / Pending |
| Actions | — | ❌ | Role-based |

**Default sort:** Date descending.

**Pagination:** Server-side · Default 25/page · Selector 10/25/50/All · Page jump input.

### 4.4 Row Actions

| Action | Icon | Visible To | Drawer | Notes |
|---|---|---|---|---|
| View | Eye | All roles with access | `observation-view` drawer 560px | Full rubric scores + comments |
| Edit | Pencil | Academic Dir, Div-P (own observations) | `observation-create` drawer 640px (pre-filled) | Cannot edit after teacher acknowledgement |
| Delete | Trash | Academic Dir | Confirm modal | Soft delete; requires reason |

### 4.5 Bulk Actions (Academic Director only)

| Action | Notes |
|---|---|
| Export Selected (XLSX) | Observation records for selected rows |

---

## 5. Drawers & Modals

### 5.1 Drawer: `observation-create` — New Observation
- **Trigger:** [+ New Observation] header button or Edit action
- **Width:** 640px
- **Sections (single scrollable form, no tabs):**

**Section 1 — Observation Details**
| Field | Type | Required | Validation |
|---|---|---|---|
| Teacher | Search + select | ✅ | Search from branch rosters |
| Branch | Auto-populated | — | From teacher record |
| Subject | Select | ✅ | Subject the teacher was teaching |
| Class & Section | Select | ✅ | Class observed |
| Date of observation | Date | ✅ | Cannot be future |
| Time slot | Text | ✅ | e.g. "Period 3 — 10:00–10:45" |
| Observer name | Auto-populated | — | Current logged-in user |
| Observer role | Auto-populated | — | Group Academic Director / Div-P Inspector |

**Section 2 — 10-Criterion Rubric**

Each criterion is rated 1–5 with a mandatory comments field (min 15 chars each):

| # | Criterion | Rating (1–5) | Comments |
|---|---|---|---|
| 1 | Subject knowledge | ★☆☆☆☆ to ★★★★★ | Required |
| 2 | Lesson structure | ★☆☆☆☆ to ★★★★★ | Required |
| 3 | Student engagement | ★☆☆☆☆ to ★★★★★ | Required |
| 4 | Questioning technique | ★☆☆☆☆ to ★★★★★ | Required |
| 5 | Assessment for learning | ★☆☆☆☆ to ★★★★★ | Required |
| 6 | Classroom management | ★☆☆☆☆ to ★★★★★ | Required |
| 7 | Differentiation | ★☆☆☆☆ to ★★★★★ | Required |
| 8 | Use of materials | ★☆☆☆☆ to ★★★★★ | Required |
| 9 | Time management | ★☆☆☆☆ to ★★★★★ | Required |
| 10 | Professional conduct | ★☆☆☆☆ to ★★★★★ | Required |

**Auto-display:** Overall rating = sum of all criteria / 10, shown live as ratings are entered.

**Rating scale descriptors (shown as tooltip on each criterion):**
- 1 = Unsatisfactory — significant improvement needed
- 2 = Developing — some key elements present but inconsistent
- 3 = Competent — meets expectations consistently
- 4 = Proficient — exceeds expectations in most areas
- 5 = Exemplary — outstanding practice, model for peers

**Section 3 — Narrative Feedback**
| Field | Type | Required | Notes |
|---|---|---|---|
| Key strengths observed | Textarea | ✅ | Min 50 chars |
| Key areas for improvement | Textarea | ✅ | Min 50 chars |
| Follow-up plan | Textarea | ❌ | Specific actions or support offered |
| Follow-up due date | Date | Conditional | Required if Follow-up plan is filled |
| Share this observation with teacher | Toggle | ✅ | Default on — teacher receives notification |
| Share with branch principal | Toggle | ✅ | Default on |

- **Submit:** "Save Observation"
- **On success:** Record created · Teacher notified (if toggle on) · Rating auto-updated in Teacher Performance Tracker (page 50)

### 5.2 Drawer: `observation-view`
- **Width:** 560px
- **Content:**

**Header:** Observation ID · Teacher · Branch · Subject · Class · Date · Observer

**Rubric Score Table:**
| Criterion | Rating | Comments |
|---|---|---|
| Subject knowledge | 4/5 | [Comment text] |
| … | … | … |
| **Overall** | **4.2/5** | — |

**Narrative section:** Strengths · Areas for Improvement · Follow-up plan · Follow-up due date

**Acknowledgement section:**
- Status badge: Acknowledged on [Date] / Pending
- [Acknowledge] button — visible only when logged in as the observed teacher (branch portal view, not this group page)

### 5.3 Modal: `delete-confirm`
- **Width:** 420px
- **Content:** "Delete observation [ID] for [Teacher Name]? This cannot be undone."
- **Fields:** Reason (Textarea, required, min 20 chars)
- **Buttons:** [Confirm Delete] (danger) · [Cancel]

---

## 6. Charts

### 6.1 Average Rating by Branch (Horizontal Bar)
- **Type:** Horizontal bar
- **Data:** Average observation rating per branch (all teachers in branch)
- **Colour:** Green ≥ 3.5 · Amber 2.5–3.4 · Red < 2.5
- **Tooltip:** Branch · Avg Rating: X.X
- **Export:** PNG

### 6.2 Criterion-wise Group Average (Radar)
- **Type:** Radar chart
- **Data:** 10 criteria on 10 axes; value = group average per criterion
- **Identifies:** Which criteria are systemic weaknesses across the group
- **Tooltip:** Criterion · Group Avg: X.X
- **Export:** PNG

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Observation saved | "Observation recorded for [Teacher Name]. Rating: [X.X]/5." | Success | 4s |
| Observation updated | "Observation updated" | Success | 4s |
| Observation deleted | "Observation deleted. Reason logged." | Warning | 6s |
| Teacher notified | "Teacher and branch principal notified of observation" | Info | 4s |
| Follow-up overdue alert | "Follow-up due for observation [ID] is overdue" | Warning | — (system alert) |
| Export started | "Export preparing… download will start shortly" | Info | 4s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No observations yet | "No observations recorded" | "Record the first classroom observation to start building performance data" | [+ New Observation] |
| No observations this term | "No observations this term" | "Schedule and conduct observations to keep performance data current" | [+ New Observation] |
| No observations match filters | "No observations match" | "Clear filters or adjust your search" | [Clear Filters] |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: stats bar + table (10 rows) + chart areas |
| Table filter/search/sort/page | Inline skeleton rows |
| Observation create drawer open | Spinner → form loads |
| Observation view drawer open | Spinner → rubric table + narrative |
| Charts load | Skeleton chart placeholders |

---

## 10. Role-Based UI Visibility

| Element | Academic Dir G3 | CAO G4 | Stream Coord G3 | Div-P Inspector |
|---|---|---|---|---|
| [+ New Observation] | ✅ | ❌ | ❌ | ✅ |
| Edit own observations | ✅ | ❌ | ❌ | ✅ (own only) |
| Delete | ✅ | ❌ | ❌ | ❌ |
| View all | ✅ | ✅ | ✅ (own stream) | ✅ |
| Bulk actions | ✅ | ❌ | ❌ | ❌ |
| Export | ✅ | ✅ | ❌ | ❌ |
| Charts | ✅ | ✅ | ✅ (own stream) | ✅ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/acad/teacher-observations/` | JWT | List observations |
| GET | `/api/v1/group/{group_id}/acad/teacher-observations/stats/` | JWT | Stats bar |
| POST | `/api/v1/group/{group_id}/acad/teacher-observations/` | JWT (G3 Acad Dir, Div-P) | Create observation |
| GET | `/api/v1/group/{group_id}/acad/teacher-observations/{id}/` | JWT | Observation detail |
| PUT | `/api/v1/group/{group_id}/acad/teacher-observations/{id}/` | JWT (G3 owner) | Update (before acknowledgement) |
| DELETE | `/api/v1/group/{group_id}/acad/teacher-observations/{id}/` | JWT (G3 Acad Dir) | Soft delete |
| GET | `/api/v1/group/{group_id}/acad/teacher-observations/export/?format=xlsx` | JWT (G3/G4) | Export |
| GET | `/api/v1/group/{group_id}/acad/teacher-observations/charts/branch-avg/` | JWT | Bar chart data |
| GET | `/api/v1/group/{group_id}/acad/teacher-observations/charts/criterion-radar/` | JWT | Radar chart data |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Search | `input delay:300ms` | GET `.../teacher-observations/?q=` | `#obs-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../teacher-observations/?filters=` | `#obs-table-section` | `innerHTML` |
| Sort column | `click` | GET `.../teacher-observations/?sort=&dir=` | `#obs-table-section` | `innerHTML` |
| Pagination | `click` | GET `.../teacher-observations/?page=` | `#obs-table-section` | `innerHTML` |
| Create drawer open | `click` | GET `.../teacher-observations/create-form/` | `#drawer-body` | `innerHTML` |
| Create submit | `submit` | POST `.../teacher-observations/` | `#drawer-body` | `innerHTML` |
| View drawer open | `click` | GET `.../teacher-observations/{id}/` | `#drawer-body` | `innerHTML` |
| Live rating total update | `change` | — | `#overall-rating-display` | `innerHTML` (client-side JS) |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
