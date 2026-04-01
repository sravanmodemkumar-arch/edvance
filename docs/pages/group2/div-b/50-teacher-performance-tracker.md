# 50 — Teacher Performance Tracker

> **URL:** `/group/acad/teacher-performance/`
> **File:** `50-teacher-performance-tracker.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Academic Director G3 · CAO G4 · Stream Coordinators G3 (own stream) · Academic MIS Officer G1 (anonymised)

---

## 1. Purpose

The Teacher Performance Tracker is the group-wide appraisal system for teaching staff across all branches. For an institution group with 2,000–5,000 teachers spread across 50 branches, subjective or informal performance assessments are inadequate — they create inconsistency, fairness disputes, and missed intervention opportunities. This page provides a composite, data-driven performance score for every teacher, computed from four objective components: the average academic results of their classes, their own attendance record, their lesson plan submission compliance, and their observed classroom rating.

The composite score is not just an internal management tool. It feeds directly into Division-E (HR) for annual appraisal and promotion decisions. When the Academic Director recommends that a teacher be placed on a Performance Improvement Plan (PIP), transferred, or promoted, that recommendation is made here and synchronised to the Div-E Group Performance Review Officer — creating a single audit trail from observation to action.

In the Indian education context, managing teacher performance fairly and legally requires documented evidence. This page provides that evidence: every data point, every score, every recommendation is timestamped and attributed. The appraisal drawer captures the scoring methodology transparently so teachers (and branch principals) can understand how scores are computed. Stream Coordinators can view and assess the performance of teachers in their own stream, enabling subject-level intervention without requiring the Academic Director to manage every case.

---

## 2. Role Access

| Role | Level | Can View | Can Create/Act | Notes |
|---|---|---|---|---|
| Chief Academic Officer (CAO) | G4 | ✅ Full | ✅ Override recommendation | Final authority on all appraisal recommendations |
| Group Academic Director | G3 | ✅ Full | ✅ Full — create appraisals, set recommendations | Primary owner |
| Group Curriculum Coordinator | G2 | ❌ | ❌ | No access |
| Group Exam Controller | G3 | ❌ | ❌ | No access |
| Group Results Coordinator | G3 | ❌ | ❌ | No access |
| Stream Coord — MPC | G3 | ✅ MPC teachers only | ❌ No create | View own stream teachers |
| Stream Coord — BiPC | G3 | ✅ BiPC teachers only | ❌ No create | View own stream teachers |
| Stream Coord — MEC/CEC | G3 | ✅ MEC/CEC teachers only | ❌ No create | View own stream teachers |
| Group JEE/NEET Integration Head | G3 | ❌ | ❌ | No access |
| Group IIT Foundation Director | G3 | ❌ | ❌ | No access |
| Group Olympiad & Scholarship Coord | G3 | ❌ | ❌ | No access |
| Group Special Education Coordinator | G3 | ❌ | ❌ | No access |
| Group Academic MIS Officer | G1 | ✅ Anonymised summary | ❌ | Aggregated stats only, no teacher names |
| Group Academic Calendar Manager | G3 | ❌ | ❌ | No access |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Academic  ›  Teacher Performance & CPD  ›  Teacher Performance Tracker
```

### 3.2 Page Header
```
Teacher Performance Tracker                              [+ Create Appraisal]  [Export ↓]
Group-wide teacher appraisal — feeds into Div-E HR                   (Academic Dir only)
```

### 3.3 Summary Stats Bar

| Stat | Value |
|---|---|
| Total Teachers Tracked | Count |
| Avg Composite Score (Group) | Score out of 100 |
| Teachers on PIP | Count — red |
| Appraisals Pending This Term | Count — amber |
| High Performers (Score ≥ 80) | Count — green |
| Recommendations Synced to Div-E | Count (this academic year) |

---

## 4. Main Content

### 4.1 Search
- Full-text across: Teacher name, Teacher ID, Branch name
- MIS Officer: search disabled (no teacher names)
- 300ms debounce · Highlights match in Teacher Name column

### 4.2 Advanced Filters (slide-in drawer, active chips, Clear All)

| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Subject | Multi-select | All subjects |
| Stream | Multi-select | MPC / BiPC / MEC / CEC / HEC / Foundation |
| Score Band | Select | High (≥ 80) / Medium (60–79) / Low (< 60) |
| Status | Multi-select | Active / On Leave / Transferred / Exited |
| Recommendation | Multi-select | Promote / Hold / PIP / Transfer / Not Yet Appraised |
| Academic Year | Select | Current + last 3 years |

Stream Coords see only their own stream (enforced server-side).

Active filter chips dismissible. "Clear All". Filter badge count.

### 4.3 Columns

| Column | Type | Sortable | Visible To | Notes |
|---|---|---|---|---|
| ☐ | Checkbox | — | Academic Dir | Bulk select |
| Teacher ID | Text | ✅ | All | |
| Teacher Name | Text | ✅ | Academic Dir, CAO, Stream Coords | Hidden from MIS |
| Branch | Text | ✅ | All | |
| Subject | Text | ✅ | All | |
| Stream | Badge | ✅ | All | |
| Student Result Avg | Number + bar | ✅ | All | Average % in their class(es) this term |
| Attendance % | Progress bar | ✅ | All | Teacher's own attendance |
| Lesson Plan Compliance % | Progress bar | ✅ | All | |
| Observation Rating | Stars (1–5) | ✅ | All | Avg from Observation Log (page 51) |
| Composite Score | Number (0–100) | ✅ | All | Weighted average of 4 components |
| Recommendation | Badge | ✅ | Academic Dir, CAO | Promote / Hold / PIP / Transfer / Pending |
| Status | Badge | ✅ | All | Active / On Leave etc. |
| Actions | — | ❌ | Role-based | |

**Composite score formula (configurable by CAO):**
- Student Result Avg: 35%
- Teacher Attendance: 25%
- Lesson Plan Compliance: 20%
- Observation Rating (normalised to 100): 20%

**Default sort:** Composite Score ascending (lowest performers first — intervention focus).

**Pagination:** Server-side · Default 25/page · Selector 10/25/50/All · Page jump input.

### 4.4 Row Actions

| Action | Icon | Visible To | Drawer | Notes |
|---|---|---|---|---|
| View Profile | Eye | Academic Dir, CAO, Stream Coords | `teacher-profile` drawer 560px | Full performance history |
| Create Appraisal | Clipboard | Academic Dir | `appraisal-create` drawer 640px | New appraisal for this teacher |
| Sync to Div-E | Arrow | Academic Dir, CAO | Inline confirm | Sends recommendation to Div-E HR system |
| Override Recommendation | Edit | CAO | Inline modal | CAO overrides Academic Dir recommendation |

### 4.5 Bulk Actions (Academic Director only)

| Action | Notes |
|---|---|
| Export Selected (XLSX) | Performance data for selected teachers |
| Sync Selected to Div-E | Bulk sync recommendations — confirm modal |

---

## 5. Drawers & Modals

### 5.1 Drawer: `teacher-profile`
- **Trigger:** View Profile row action
- **Width:** 560px
- **Tabs:** Personal · Performance History · Observations · CPD · Appraisal

**Tab: Personal**
Teacher ID · Name · Branch · Subject · Stream · Hire date · Status · Current class assignments

**Tab: Performance History**
Table: Academic Year · Term · Student Result Avg · Attendance % · Lesson Plan % · Observation Rating · Composite Score · Recommendation
Mini line chart: Composite Score trend across last 6 terms.

**Tab: Observations**
List of all observations from Observation Log (page 51): Date · Observer · Rating · Strengths summary. [View Full Observation →] link per row.

**Tab: CPD**
CPD summary from CPD Tracker (page 52): Hours completed · Hours required · % · Last training date · Status.

**Tab: Appraisal**
Current term appraisal status (if created). All historical appraisals — date, composite score, recommendation, signed by.

### 5.2 Drawer: `appraisal-create`
- **Trigger:** [+ Create Appraisal] header button or row action
- **Width:** 640px
- **Tabs:** Results Score · Attendance Score · Lesson Plan Score · Peer Review · Composite + Recommendation

#### Tab: Results Score
| Field | Type | Required | Notes |
|---|---|---|---|
| Teacher | Search + select | ✅ | From branch staff |
| Academic Year + Term | Select | ✅ | |
| Classes taught this term | Repeater | ✅ | Class + Section + Subject + Exam avg% |
| Computed result avg | Auto | — | Mean of all class averages above |
| Override result avg | Number | ❌ | With mandatory reason if overriding |

#### Tab: Attendance Score
| Field | Type | Required | Notes |
|---|---|---|---|
| Teacher attendance % (this term) | Number | ✅ | Auto-pulled from branch HR data if integrated |
| Override attendance % | Number | ❌ | With reason |

#### Tab: Lesson Plan Score
| Field | Type | Required | Notes |
|---|---|---|---|
| Lesson plans required (this term) | Number | ✅ | Based on periods × subjects |
| Lesson plans submitted | Number | ✅ | |
| Compliance % | Auto | — | Submitted / Required × 100 |
| Override compliance % | Number | ❌ | With reason |

#### Tab: Peer Review
| Field | Type | Required | Notes |
|---|---|---|---|
| Peer reviewer name | Text | ❌ | |
| Peer rating (1–5) | Stars | ❌ | |
| Peer review notes | Textarea | ❌ | Max 500 chars |

#### Tab: Composite + Recommendation
| Field | Type | Required | Notes |
|---|---|---|---|
| Composite score (auto) | Number display | — | Computed from 4 components with configured weights |
| Component weight display | Read-only table | — | Shows weights: Results 35% / Attendance 25% / Lesson Plan 20% / Observation 20% |
| Observation rating (auto-pulled) | Number | — | From Observation Log page 51 avg |
| Recommendation | Select | ✅ | Promote / Hold / PIP / Transfer |
| Recommendation rationale | Textarea | ✅ | Min 50 chars |
| Notify teacher's branch principal | Toggle | ✅ | Default on |
| Send to Div-E immediately | Toggle | ❌ | Default off — Academic Dir may queue first |

- **Submit:** "Save Appraisal"
- **On success:** Appraisal saved · Recommendation badge updated in table · If Div-E toggle on: sync initiated

### 5.3 Modal: `sync-to-dive-confirm`
- **Width:** 420px
- **Content:** "Sync [N] teacher recommendation(s) to Div-E HR? Once synced, the Div-E Performance Review Officer will be notified."
- **Buttons:** [Confirm Sync] · [Cancel]
- **On confirm:** Div-E notification triggered · Sync status logged

### 5.4 Modal: `override-recommendation`
- **Width:** 420px (CAO only)
- **Content:** "Override recommendation for [Teacher Name]?"
- **Fields:** Override to (Select: Promote/Hold/PIP/Transfer) · Override reason (Textarea, required, min 30 chars)
- **Buttons:** [Confirm Override] · [Cancel]

---

## 6. Charts

### 6.1 Score Distribution by Branch (Box Plot)
- **Type:** Box plot (horizontal)
- **Data:** Composite score distribution per branch — min, Q1, median, Q3, max, outliers
- **Y-axis:** Branch names
- **X-axis:** Score 0–100
- **Tooltip:** Branch · Median: X · Q1: X · Q3: X
- **Export:** PNG

### 6.2 Subject-wise Average Composite Score (Bar)
- **Type:** Vertical bar chart
- **Data:** Average composite score per subject across group
- **X-axis:** Subjects
- **Y-axis:** Score 0–100
- **Colour:** Green ≥ 70 · Amber 50–69 · Red < 50
- **Tooltip:** Subject · Avg score: X
- **Export:** PNG

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Appraisal created | "Appraisal created for [Teacher Name]. Composite score: [X]." | Success | 4s |
| Appraisal updated | "Appraisal updated" | Success | 4s |
| Synced to Div-E | "[N] appraisal(s) synced to Div-E HR" | Success | 4s |
| CAO override applied | "Recommendation overridden by CAO. Reason logged." | Warning | 6s |
| Export started | "Export preparing… download will start shortly" | Info | 4s |
| Sync failed | "Div-E sync failed. Please retry or contact system admin." | Error | Manual dismiss |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No teachers tracked | "No teacher performance data" | "Appraisals will populate once branch staff data is available" | — |
| No appraisals this term | "No appraisals created this term" | "Create appraisals to track performance and feed into the Div-E review cycle" | [+ Create Appraisal] |
| No teachers match filters | "No teachers match your filters" | "Clear filters or change your search" | [Clear Filters] |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: stats bar + table (10 rows) + chart areas |
| Table filter/search/sort/page | Inline skeleton rows |
| Profile drawer open | Spinner → tabs load |
| Appraisal drawer open | Spinner → tabs |
| Charts load | Skeleton chart areas |
| Export trigger | Spinner in export button |

---

## 10. Role-Based UI Visibility

| Element | Academic Dir G3 | CAO G4 | Stream Coord G3 | MIS G1 |
|---|---|---|---|---|
| Full teacher table | ✅ | ✅ | ✅ (own stream) | ❌ (aggregate stats bar) |
| Teacher name column | ✅ | ✅ | ✅ | ❌ |
| Recommendation column | ✅ | ✅ | ❌ | ❌ |
| [+ Create Appraisal] | ✅ | ❌ | ❌ | ❌ |
| View Profile action | ✅ | ✅ | ✅ | ❌ |
| Sync to Div-E action | ✅ | ✅ | ❌ | ❌ |
| Override Recommendation | ❌ | ✅ | ❌ | ❌ |
| Bulk actions | ✅ | ❌ | ❌ | ❌ |
| Export | ✅ | ✅ | ❌ | ❌ |
| Charts | ✅ | ✅ | ✅ (own stream) | ❌ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/acad/teacher-performance/` | JWT | List teacher performance records |
| GET | `/api/v1/group/{group_id}/acad/teacher-performance/stats/` | JWT | Stats bar |
| GET | `/api/v1/group/{group_id}/acad/teacher-performance/{teacher_id}/` | JWT (G3 Acad Dir, G4) | Teacher profile detail |
| POST | `/api/v1/group/{group_id}/acad/teacher-performance/appraisals/` | JWT (G3 Acad Dir) | Create appraisal |
| PUT | `/api/v1/group/{group_id}/acad/teacher-performance/appraisals/{id}/` | JWT (G3 Acad Dir) | Update appraisal |
| POST | `/api/v1/group/{group_id}/acad/teacher-performance/appraisals/sync-dive/` | JWT (G3/G4) | Sync to Div-E (bulk) |
| POST | `/api/v1/group/{group_id}/acad/teacher-performance/appraisals/{id}/override/` | JWT (G4 CAO) | CAO recommendation override |
| GET | `/api/v1/group/{group_id}/acad/teacher-performance/export/?format=xlsx` | JWT (G3 Acad Dir, G4) | Export |
| GET | `/api/v1/group/{group_id}/acad/teacher-performance/charts/score-distribution/` | JWT | Box plot data |
| GET | `/api/v1/group/{group_id}/acad/teacher-performance/charts/subject-avg/` | JWT | Bar chart data |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Search | `input delay:300ms` | GET `.../teacher-performance/?q=` | `#teacher-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../teacher-performance/?filters=` | `#teacher-table-section` | `innerHTML` |
| Sort column | `click` | GET `.../teacher-performance/?sort=&dir=` | `#teacher-table-section` | `innerHTML` |
| Pagination | `click` | GET `.../teacher-performance/?page=` | `#teacher-table-section` | `innerHTML` |
| Profile drawer | `click` | GET `.../teacher-performance/{tid}/` | `#drawer-body` | `innerHTML` |
| Appraisal drawer open | `click` | GET `.../teacher-performance/appraisals/create-form/?teacher={tid}` | `#drawer-body` | `innerHTML` |
| Appraisal submit | `submit` | POST `.../teacher-performance/appraisals/` | `#drawer-body` | `innerHTML` |
| Sync confirm | `click` | POST `.../teacher-performance/appraisals/sync-dive/` | `#toast-container` | `beforeend` |
| Override confirm | `click` | POST `.../teacher-performance/appraisals/{id}/override/` | `#teacher-row-{id}` | `outerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
