# 02 — Academic Director Dashboard

> **URL:** `/group/acad/director/`
> **File:** `02-academic-director-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Group Academic Director (G3) — exclusive landing page

---

## 1. Purpose

Primary post-login landing for the Group Academic Director (G3). This role sits directly under the CAO and is responsible for syllabus design and maintenance, teacher performance monitoring, academic MIS operations, and the Continuing Professional Development (CPD) programme across all branches. The Academic Director does not sit above stream coordinators in terms of exam operations — their domain is curriculum design, teacher quality, and academic data.

This dashboard gives the Academic Director a daily operational view: which branches are falling behind on syllabus delivery, which teachers are underperforming and need support, whether lesson plans have been submitted on time, and whether CPD programmes are on track. The page is operationally dense — the Academic Director spends most of their time here or in the Syllabus Manager and Lesson Plan Standards pages that this dashboard links into.

All data is scoped to the Academic Director's group only. For a large group running 50 branches with 2,000–5,000 teachers, the aggregations are server-side and returned as chart-ready JSON from FastAPI endpoints, rendered via Chart.js in the Django template.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Academic Director | G3 | Full — all sections, all actions | This is their exclusive dashboard |
| Chief Academic Officer (CAO) | G4 | View only — cannot edit | CAO may view but not act on this role's exclusive dashboard |
| Group Curriculum Coordinator | G2 | — | Has own dashboard `/group/acad/curriculum-coord/` |
| Group Exam Controller | G3 | — | Has own dashboard `/group/acad/exam-controller/` |
| Group Results Coordinator | G3 | — | Has own dashboard `/group/acad/results-coord/` |
| Group Stream Coord — MPC | G3 | — | Has own dashboard `/group/acad/stream/mpc/` |
| Group Stream Coord — BiPC | G3 | — | Has own dashboard `/group/acad/stream/bipc/` |
| Group Stream Coord — MEC/CEC | G3 | — | Has own dashboard `/group/acad/stream/mec-cec/` |
| Group JEE/NEET Integration Head | G3 | — | Has own dashboard `/group/acad/jee-neet/` |
| Group IIT Foundation Director | G3 | — | Has own dashboard `/group/acad/iit-foundation/` |
| Group Olympiad & Scholarship Coord | G3 | — | Has own dashboard `/group/acad/olympiad/` |
| Group Special Education Coordinator | G3 | — | Has own dashboard `/group/acad/special-ed/` |
| Group Academic MIS Officer | G1 | — | Has own dashboard `/group/acad/mis/` |
| Group Academic Calendar Manager | G3 | — | Has own dashboard `/group/acad/cal-manager/` |

> **Access enforcement:** Django view decorator `@require_role('academic_director')`. Any other role hitting this URL is redirected to their own dashboard. CAO landing here sees a read-only banner: "Viewing as CAO — write actions are disabled on this page."

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Academic Division  ›  Academic Director Dashboard
```

### 3.2 Page Header
```
Welcome back, [Director Name]                    [Download Academic MIS Report ↓]  [Settings ⚙]
[Group Name] — Group Academic Director · Last login: [date time] · [Group Logo]
```

### 3.3 Alert Banner (conditional — shown only when alerts exist)
- Collapsible panel at top of page, above KPI row
- Background: `bg-red-50 border-l-4 border-red-500` for Critical · `bg-yellow-50 border-l-4 border-yellow-400` for Warning
- Each alert: icon + message + branch name + [Take Action →] link
- "Dismiss" per alert (stored in session, reappears next login if unresolved)
- Maximum 5 alerts shown; "View all X alerts →" link to relevant detail page

**Alert trigger examples:**
- Branch lesson plan submission rate <50% with deadline in <5 days (red — Critical)
- Teacher observation logged 0 times this month in ≥5 branches (red — Critical)
- CPD deadline within 7 days and completion rate <40% (red — Critical)
- Low-performing subject (avg marks <35%) in any branch for 2+ consecutive exams (yellow — Warning)
- Teacher absenteeism >15% in any branch for the current month (yellow — Warning)
- Syllabus completion <60% with 4 weeks left in term in ≥3 branches (yellow — Warning)

---

## 4. KPI Summary Bar

| Card | Metric | Source | Colour Rule | Drill-down |
|---|---|---|---|---|
| Avg Attendance | `87.3%` group-wide monthly average across all branches | Attendance aggregation | Green ≥90% · Yellow 80–89% · Red <80% | → Academic MIS Summary (section 5.4) |
| Avg Result % | `71.4%` current term group average across all streams | Result aggregation | Green ≥75% · Yellow 60–74% · Red <60% | → Low-performing Subjects (section 5.7) |
| Lesson Plan Submission | `76%` branches with ≥90% submission rate | Lesson plan data | Green ≥90% branches · Yellow 70–89% · Red <70% | → Lesson Plan Standards `/group/acad/lesson-plans/` |
| Teacher Observations Due | `23` observations scheduled but not yet logged this month | Teacher observation tracker | Green = 0 · Yellow 1–10 · Red >10 | → Section 5.5 |
| CPD Completion Rate | `68%` teaching staff completed mandatory CPD this year | CPD tracker | Green ≥90% · Yellow 70–89% · Red <70% | → Section 5.6 |
| Dropout Rate | `1.8%` students withdrawn from group this academic year | Student data | Green <1% · Yellow 1–2% · Red >2% | → Academic MIS Summary |

**HTMX:** Cards auto-refresh every 5 minutes via `hx-trigger="every 5m"` `hx-get="/api/v1/group/{group_id}/acad/director/kpi-cards/"` `hx-swap="innerHTML"` targeting `#kpi-bar`.

---

## 5. Sections

### 5.1 Syllabus Completion Rate — Multi-Line Chart

> Term-to-date syllabus completion percentage per branch and stream — the Academic Director's primary operational signal.

**Display:** Multi-line chart (Chart.js 4.x). Each line = one branch. X-axis = weeks of current term. Y-axis = % syllabus completed.

**Reference line:** Expected completion % at this point in the term (dashed grey line).

**Lines below reference line:** Highlighted in red.

**Tooltip:** Branch name · Stream · Current week · Actual % · Expected % · Gap.

**Filters (within card):**
- Stream selector (All / MPC / BiPC / MEC-CEC / Foundation / Integrated) — multi-select
- Branch selector — multi-select (default: All)
- Term selector (Current / Previous)

**Legend:** Bottom — branch names with colour swatches. Clicking legend item toggles that branch's line.

**Click on any branch line data point:** Opens branch syllabus detail drawer (560px) — topic-level completion, teacher assignments, missing topics.

**Export:** "Export PNG" and "Export CSV (raw data)" buttons.

**Empty state:** "No syllabus data for the selected stream/term. Ensure syllabus is configured in the Syllabus Manager."

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/director/syllabus-completion/"` on stream/branch/term filter `change` `hx-target="#syllabus-chart"` `hx-swap="innerHTML"`.

---

### 5.2 Teacher Performance Distribution — Histogram

> Rating distribution across all teaching staff across all branches — shows overall teaching quality profile of the group.

**Display:** Histogram / bar chart (Chart.js 4.x). X-axis: Rating bands (1.0–1.9, 2.0–2.9, 3.0–3.9, 4.0–4.9, 5.0). Y-axis: Number of teachers.

**Bar colours:** 1.0–2.9 → Red (underperforming) · 3.0–3.9 → Amber · 4.0–5.0 → Green.

**Summary stats (below chart):** Avg rating across group · % teachers rated <3.0 (red highlighted) · Total teachers evaluated · Total teachers not yet evaluated (grey).

**Filters (within card):**
- Stream (affects which teachers shown — MPC teachers only, etc.)
- Branch multi-select

**Click on bar:** Opens teacher list drawer (560px) — all teachers in that rating band: Name, Branch, Subject, Rating, Last Observation Date, [View Profile →].

**Export:** "Export PNG" button.

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/director/teacher-distribution/"` on filter change `hx-target="#teacher-histogram"` `hx-swap="innerHTML"`.

---

### 5.3 Lesson Plan Submission Rate — Branch Table

> All branches with their lesson plan submission rates — branches below 90% flagged amber or red.

**Display:** Sortable table.

**Search:** Full-text on branch name. Debounce 300ms.

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Branch Name | Text + link | ✅ | Opens lesson plan detail drawer |
| State | Badge | ✅ | Indian state |
| Stream(s) | Tags | ❌ | MPC, BiPC etc. |
| Teachers (Total) | Number | ✅ | |
| Plans Submitted | Number | ✅ | Count of submitted lesson plans this term |
| Plans Required | Number | ✅ | Total expected lesson plans this term |
| Submission Rate | Progress bar + % | ✅ | Green ≥90% · Amber 70–89% · Red <70% |
| Last Submission | Date | ✅ | Red if >7 days ago |
| Actions | — | ❌ | Send Reminder · View Plans |

**Default sort:** Submission Rate ascending (worst first).

**Row action — Send Reminder:** `hx-post="/api/v1/group/{group_id}/acad/director/lesson-plans/remind/{branch_id}/"` — sends WhatsApp/system notification to branch academic head. Toast: "Reminder sent to [Branch] academic coordinator."

**Row action — View Plans:** Opens lesson plan detail drawer (560px) — per-subject, per-teacher submission status.

**Pagination:** Server-side · Default 25/page · Selector 10/25/50 · "Showing X–Y of Z branches".

**Checkbox row select:** Yes — bulk action: "Send Reminder to Selected Branches".

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/director/lesson-plan-table/"` on search/sort/page `hx-target="#lesson-plan-table-section"` `hx-swap="innerHTML"`.

---

### 5.4 Academic MIS Summary — KPI Strip

> Key academic MIS metrics in a horizontal strip — attendance, average marks, dropout, teacher absenteeism.

**Display:** 4 horizontal stat cards within a bordered strip.

| Card | Value example | Source |
|---|---|---|
| Avg Attendance | `87.3%` this month | Attendance module |
| Group Avg Marks | `71.4%` current term | Result module |
| Dropout Rate | `1.8%` this academic year | Student status data |
| Teacher Absenteeism | `4.2%` this month | HR/attendance |

**Each card:** Current value (large) · Previous period value (small, greyed) · Trend arrow · Colour status.

**Click on any card:** Opens MIS detail drawer (560px) — branch-wise breakdown for that metric, sortable table.

**"View Full MIS Report →"** links to `/group/acad/mis/`.

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/director/mis-summary/"` `hx-trigger="every 5m"` `hx-target="#mis-strip"` `hx-swap="innerHTML"`.

---

### 5.5 Teacher Observations Due — Alert Counter

> Observations scheduled but not logged this month — Academic Director needs to follow up with branches.

**Display:** Alert card — large count number + "teacher observations not yet logged this month." Background: red if >10, amber if 1–10, green if 0.

**Below counter:** Table showing up to 10 overdue observations:

| Column | Notes |
|---|---|
| Teacher Name | Masked initials if >G3 privacy setting |
| Branch | Branch name |
| Subject | Subject taught |
| Scheduled Date | Date observation was supposed to happen |
| Days Overdue | Red if >7 |
| Observed By | Who was supposed to observe |
| Action | [Mark Complete] [Reschedule] |

**[Mark Complete]:** Opens modal (380px) — Observed on (date picker, required) · Observer name · Rating (1.0–5.0, required) · Notes. POST to log the observation.

**[Reschedule]:** Opens modal (380px) — New date picker · Reason. PUT to update schedule.

**"View All Observations →"** links to teacher performance module.

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/director/observation-alerts/"` `hx-trigger="every 5m"` `hx-target="#observation-alert-card"` `hx-swap="innerHTML"`.

---

### 5.6 CPD Completion Rate — Donut Chart

> Teaching staff who completed mandatory CPD (Continuing Professional Development) this academic year.

**Display:** Donut chart (Chart.js 4.x). Segments: Completed (green) · In Progress (amber) · Not Started (red).

**Centre label:** Overall % completed (large), e.g. `68%`.

**Legend (right of chart):** Completed: N teachers · In Progress: N teachers · Not Started: N teachers.

**Below chart:** Branch-breakdown table (compact, 5 rows visible + "Show all" expander):

| Column | Notes |
|---|---|
| Branch | Branch name |
| Completed | Count |
| In Progress | Count |
| Not Started | Count + red badge if >0 |
| Completion % | Progress bar |
| Deadline | Date |

**Filters (within card):** CPD programme selector (if multiple programmes running) · Branch multi-select.

**[Send Reminder to Non-Starters]:** Bulk action — POST to send WhatsApp/system notification to all teachers who have not started CPD.

**Export:** "Export PNG" button.

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/director/cpd-completion/"` on filter change `hx-target="#cpd-chart"` `hx-swap="innerHTML"`.

---

### 5.7 Low-Performing Subjects — Table

> Subject × Branch pairs where average marks are below the pass threshold — the Academic Director investigates and coordinates remediation.

**Display:** Sortable table.

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Subject | Text | ✅ | |
| Branch | Text + link | ✅ | Opens branch-subject detail drawer |
| Stream | Badge | ✅ | |
| Class | Text | ✅ | e.g. Class XI, Class XII |
| Avg Marks | Number + % | ✅ | Red if below pass threshold |
| Pass % | Progress bar + % | ✅ | Red if <50% |
| Pass Threshold | Number | ❌ | Configured in Stream Config |
| Consecutive Low Exams | Number | ✅ | Red badge if ≥2 |
| Last Exam | Date | ✅ | |
| Actions | — | ❌ | View · Flag for Review |

**Default sort:** Consecutive Low Exams descending, then Avg Marks ascending.

**Filters:** Stream · Class · Branch (multi-select) · Consecutive Low Exams (≥1, ≥2, ≥3).

**Search:** Subject name, branch name. 300ms debounce.

**[Flag for Review]:** Marks this subject-branch pair for follow-up — adds to Academic Director's task list and notifies branch academic coordinator.

**Pagination:** Server-side · 25/page.

**Empty state:** "No subjects below pass threshold this term. All subjects performing within expected bands." — Green illustration.

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/director/low-performing-subjects/"` on filter/search/sort `hx-target="#low-subjects-table"` `hx-swap="innerHTML"`.

---

### 5.8 Upcoming Lesson Plan Deadlines — Calendar Strip

> Deadlines for lesson plan uploads in the next 7 days — the Academic Director tracks compliance proactively.

**Display:** Horizontal calendar strip — 7 columns, one per day. Each day shows: date + weekday label + count of deadlines due + colour (red if any deadline is for a branch already below 70% submission, amber otherwise, green if all branches for that deadline are ≥90%).

**Click on any day column:** Expands below to show a list of branches with deadlines on that day — Branch, Stream, Subject, Current submission rate, Status badge.

**"View Lesson Plan Standards →"** links to `/group/acad/lesson-plans/`.

---

## 6. Drawers & Modals

### 6.1 Drawer: `branch-syllabus-detail` (from Syllabus Completion chart click)
- **Width:** 560px
- **Tabs:** Topics · Teachers · History
- **Topics tab:** Table of all topics — Topic, Chapter, Subject, Status (Covered/In Progress/Not Started), Expected completion date
- **Teachers tab:** Each teacher, subject, topics covered, lesson plans submitted, last observation date
- **History tab:** Term-over-term completion rates for this branch
- **HTMX:** `hx-get="/api/v1/group/{group_id}/acad/branches/{branch_id}/syllabus-detail/?stream={stream_id}"` `hx-target="#drawer-body"` `hx-swap="innerHTML"`

### 6.2 Drawer: `teacher-band-list` (from histogram bar click)
- **Width:** 560px
- **Content:** Sortable table — Teacher Name, Branch, Subject, Stream, Rating (current), Last Observation Date, CPD Status
- **Search within drawer:** Teacher name, subject
- **HTMX:** `hx-get="/api/v1/group/{group_id}/acad/director/teacher-distribution/{band}/"` `hx-target="#drawer-body"` `hx-swap="innerHTML"`

### 6.3 Drawer: `lesson-plan-branch-detail` (from lesson plan table row)
- **Width:** 560px
- **Tabs:** By Subject · By Teacher · Missing Plans
- **By Subject tab:** Table — Subject, Total Plans Required, Submitted, Rate, Status
- **By Teacher tab:** Table — Teacher Name, Subject, Plans Due, Submitted, Last Upload Date
- **Missing Plans tab:** List of specific topic lesson plans not yet uploaded — Topic, Subject, Teacher responsible, Deadline
- **Action:** [Send Reminder] per teacher row
- **HTMX:** `hx-get="/api/v1/group/{group_id}/acad/director/lesson-plans/{branch_id}/"` `hx-target="#drawer-body"` `hx-swap="innerHTML"`

### 6.4 Drawer: `mis-detail` (from MIS strip card click)
- **Width:** 560px
- **Content:** Branch-wise breakdown table for the tapped metric — all branches, sortable, with values and trend arrows
- **Export button:** Download XLSX for this metric
- **HTMX:** `hx-get="/api/v1/group/{group_id}/acad/director/mis-detail/?metric={metric_key}"` `hx-target="#drawer-body"` `hx-swap="innerHTML"`

### 6.5 Modal: `observation-mark-complete`
- **Width:** 380px
- **Fields:** Observed on (date picker, required, not future) · Observer Name (text, auto-filled, editable) · Rating (number input 1.0–5.0, required) · Observation Notes (textarea, min 20 chars)
- **Buttons:** [Save Observation] (primary) + [Cancel]
- **On confirm:** `hx-post="/api/v1/group/{group_id}/acad/director/observations/{obs_id}/complete/"` — toast + removes row from list

### 6.6 Modal: `observation-reschedule`
- **Width:** 380px
- **Fields:** New Observation Date (date picker, required, must be future) · Reason for Rescheduling (textarea, required)
- **Buttons:** [Reschedule] (primary) + [Cancel]
- **On confirm:** `hx-put="/api/v1/group/{group_id}/acad/director/observations/{obs_id}/reschedule/"` — toast + updates row

### 6.7 Modal: `low-subject-flag`
- **Width:** 380px
- **Content:** "Flag [Subject] at [Branch] for review?" — auto-populates task description with current metrics
- **Fields:** Priority (Low / Medium / High, required) · Additional Notes (textarea, optional) · Assign to (director's own queue or notify branch academic coordinator)
- **Buttons:** [Flag for Review] (primary) + [Cancel]

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Reminder sent to branch | "Lesson plan reminder sent to [Branch] academic coordinator." | Success (green) | 4s auto-dismiss |
| Observation marked complete | "Observation logged for [Teacher initials] at [Branch]." | Success | 4s |
| Observation rescheduled | "Observation rescheduled to [New Date] for [Teacher initials]." | Info | 4s |
| Subject flagged for review | "[Subject] at [Branch] flagged for review. Branch coordinator notified." | Success | 4s |
| KPI load error | "Failed to load academic data. Retrying…" | Error (red) | Manual dismiss |
| CPD reminder sent | "CPD reminder sent to [N] teachers who have not yet started." | Success | 4s |
| Export triggered | "MIS report export started — download will begin shortly." | Info | 4s |
| Bulk reminder sent | "Lesson plan reminders sent to [N] selected branches." | Success | 4s |

---

## 8. Empty States

| Condition | Illustration | Heading | Description | CTA |
|---|---|---|---|---|
| No observations due | Calendar check | "All observations are logged" | "No scheduled teacher observations are overdue this month." | — |
| No low-performing subjects | Trophy icon | "All subjects within range" | "No subject-branch pairs are below the pass threshold this term." | — |
| No lesson plan deadlines (7 days) | Calendar outline | "No deadlines in the next 7 days" | "There are no lesson plan submission deadlines in the next 7 days." | — |
| No teacher data | People outline | "No teacher performance data" | "Teacher ratings have not been collected yet for this period. Ensure observations are being logged." | [Go to Lesson Plan Standards] |
| No syllabus data | Chart outline | "Syllabus data unavailable" | "No syllabus completion data exists for this filter selection." | [Go to Syllabus Manager] |
| No CPD programmes | Book outline | "No CPD programmes active" | "No mandatory CPD programmes are currently running for this group." | — |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton screens: KPI bar (6 cards) + chart placeholders for syllabus + histogram + lesson plan table (8 rows) |
| KPI auto-refresh | Subtle shimmer over existing card values |
| Syllabus chart filter change | Chart area shimmer + centred spinner |
| Teacher histogram filter change | Chart area shimmer + centred spinner |
| Lesson plan table search/sort/page | Inline skeleton rows — 8 rows, matching column widths |
| Drawer open (any) | Spinner in drawer body with tab skeletons |
| Observation mark-complete submit | Spinner inside [Save Observation] button + button disabled |
| CPD reminder send | Spinner inside reminder button |
| MIS strip auto-refresh | Subtle shimmer over each card value |

---

## 10. Role-Based UI Visibility

| Element | Academic Director G3 | CAO G4 (view-only) | All other Div-B roles |
|---|---|---|---|
| Page itself | ✅ Rendered | ✅ Read-only banner | ❌ Redirected to own dashboard |
| Alert Banner | ✅ Shown | ✅ Shown (read-only) | N/A |
| Send Reminder buttons (lesson plan table) | ✅ Enabled | ❌ Hidden | N/A |
| [Mark Complete] / [Reschedule] in observations | ✅ Enabled | ❌ Hidden | N/A |
| [Flag for Review] in low subjects table | ✅ Enabled | ❌ Hidden | N/A |
| [Send CPD Reminder to Non-Starters] | ✅ Enabled | ❌ Hidden | N/A |
| Bulk reminder action | ✅ Enabled | ❌ Hidden | N/A |
| [Download MIS Report] header button | ✅ Shown | ✅ Shown | N/A |
| Export buttons on charts | ✅ Shown | ✅ Shown | N/A |

> All UI visibility decisions made server-side in Django template. No client-side JS role checks.

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/acad/director/dashboard/` | JWT (G3) | Full page data |
| GET | `/api/v1/group/{group_id}/acad/director/kpi-cards/` | JWT (G3) | KPI card values only (auto-refresh) |
| GET | `/api/v1/group/{group_id}/acad/director/syllabus-completion/` | JWT (G3) | Syllabus chart data — stream, branch, term filters |
| GET | `/api/v1/group/{group_id}/acad/director/teacher-distribution/` | JWT (G3) | Histogram data — stream, branch filters |
| GET | `/api/v1/group/{group_id}/acad/director/teacher-distribution/{band}/` | JWT (G3) | Teachers in a specific rating band (drawer) |
| GET | `/api/v1/group/{group_id}/acad/director/lesson-plan-table/` | JWT (G3) | Lesson plan submission table — sort/search/page |
| POST | `/api/v1/group/{group_id}/acad/director/lesson-plans/remind/{branch_id}/` | JWT (G3) | Send lesson plan reminder to branch |
| POST | `/api/v1/group/{group_id}/acad/director/lesson-plans/remind/bulk/` | JWT (G3) | Bulk remind selected branches |
| GET | `/api/v1/group/{group_id}/acad/director/lesson-plans/{branch_id}/` | JWT (G3) | Branch lesson plan detail (drawer) |
| GET | `/api/v1/group/{group_id}/acad/director/mis-summary/` | JWT (G3) | MIS strip — 4 KPI values |
| GET | `/api/v1/group/{group_id}/acad/director/mis-detail/` | JWT (G3) | Branch breakdown for a metric (drawer) |
| GET | `/api/v1/group/{group_id}/acad/director/observation-alerts/` | JWT (G3) | Overdue teacher observations |
| POST | `/api/v1/group/{group_id}/acad/director/observations/{obs_id}/complete/` | JWT (G3) | Mark observation as complete |
| PUT | `/api/v1/group/{group_id}/acad/director/observations/{obs_id}/reschedule/` | JWT (G3) | Reschedule observation |
| GET | `/api/v1/group/{group_id}/acad/director/cpd-completion/` | JWT (G3) | CPD donut chart + branch table data |
| POST | `/api/v1/group/{group_id}/acad/director/cpd/remind-non-starters/` | JWT (G3) | Bulk CPD reminder to non-starters |
| GET | `/api/v1/group/{group_id}/acad/director/low-performing-subjects/` | JWT (G3) | Low subject table — filter/sort/search/page |
| POST | `/api/v1/group/{group_id}/acad/director/low-performing-subjects/{subject_branch_id}/flag/` | JWT (G3) | Flag subject-branch for review |
| GET | `/api/v1/group/{group_id}/acad/branches/{branch_id}/syllabus-detail/` | JWT (G3) | Branch syllabus detail (drawer) |
| GET | `/api/v1/group/{group_id}/acad/director/report/?format=pdf` | JWT (G3) | Download academic MIS report |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| KPI auto-refresh | `every 5m` | GET `.../director/kpi-cards/` | `#kpi-bar` | `innerHTML` |
| Syllabus chart filter change | `change` | GET `.../director/syllabus-completion/?stream={}&term={}` | `#syllabus-chart` | `innerHTML` |
| Histogram filter change | `change` | GET `.../director/teacher-distribution/?stream={}&branch={}` | `#teacher-histogram` | `innerHTML` |
| Histogram bar click | `click` | GET `.../director/teacher-distribution/{band}/` | `#drawer-body` | `innerHTML` |
| Lesson plan table search | `input delay:300ms` | GET `.../director/lesson-plan-table/?q={}` | `#lesson-plan-table-section` | `innerHTML` |
| Lesson plan table sort | `click` | GET `.../director/lesson-plan-table/?sort={}&dir={}` | `#lesson-plan-table-section` | `innerHTML` |
| Lesson plan pagination | `click` | GET `.../director/lesson-plan-table/?page={}` | `#lesson-plan-table-section` | `innerHTML` |
| Send reminder (row) | `click` | POST `.../lesson-plans/remind/{branch_id}/` | `#lesson-plan-table-section` | `innerHTML` |
| MIS strip auto-refresh | `every 5m` | GET `.../director/mis-summary/` | `#mis-strip` | `innerHTML` |
| MIS card click (drawer) | `click` | GET `.../director/mis-detail/?metric={}` | `#drawer-body` | `innerHTML` |
| Observation alert refresh | `every 5m` | GET `.../director/observation-alerts/` | `#observation-alert-card` | `innerHTML` |
| Mark observation complete | `click` | (opens modal — modal submit is POST) | — | — |
| CPD chart filter change | `change` | GET `.../director/cpd-completion/?programme={}&branch={}` | `#cpd-chart` | `innerHTML` |
| Low subjects table filter | `change` | GET `.../director/low-performing-subjects/?stream={}&class={}` | `#low-subjects-table` | `innerHTML` |
| Low subjects search | `input delay:300ms` | GET `.../director/low-performing-subjects/?q={}` | `#low-subjects-table` | `innerHTML` |
| Lesson plan deadline day click | `click` | GET `.../director/lesson-plan-deadlines/?date={}` | `#deadline-day-detail` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
