# 39 — IIT Foundation Program Manager

> **URL:** `/group/acad/iit-foundation/program/`
> **File:** `39-foundation-program-manager.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** IIT Foundation Director G3 · CAO G4 · Curriculum Coordinator G2

---

## 1. Purpose

The IIT Foundation Program Manager oversees the curriculum, batches, faculty assignments, and content structure for the group's Class 6–10 IIT Foundation programme. IIT Foundation is a long-horizon academic investment: students who join in Class 6 are being prepared not for an exam that is 6 years away, but for a sustained problem-solving culture and mathematical maturity that distinguishes top JEE performers from average ones. Managing this programme at group scale — across potentially 50 branches with thousands of Class 6–10 students — requires a structured hub.

The page is organised around five class tabs (Class 6 through Class 10), because the curriculum, difficulty progression, and faculty qualifications required at each level are distinct. A teacher suitable for Class 6 Foundation (introducing basic algebra and Olympiad-style puzzles) may not have the depth required for Class 9–10 (where calculus prerequisites and advanced physics concepts begin). The IIT Foundation Director uses this page to ensure each class level has appropriate subject coverage, study material, faculty, and test scheduling across all branches.

Batch management is a key operational function: the Foundation Director must know how many batches exist per class per branch, who the faculty are, and whether batch sizes are within acceptable limits. A branch that has 120 Class 8 Foundation students but only one batch of 120 is creating an environment where individual attention — essential for Foundation pedagogy — is impossible. This page surfaces that imbalance through the batch management table so the Director can mandate batch splitting.

---

## 2. Role Access

| Role | Level | Can View | Can Act | Notes |
|---|---|---|---|---|
| Chief Academic Officer (CAO) | G4 | ✅ All classes, all branches | ✅ View · Approve configs | Approval authority |
| Group Academic Director | G3 | ✅ All classes | ❌ | Read-only |
| Group Curriculum Coordinator | G2 | ✅ All classes | ✅ Upload content · Edit study material | Content management |
| Group Exam Controller | G3 | ❌ | ❌ | No access |
| Group Results Coordinator | G3 | ❌ | ❌ | No access |
| Group Stream Coord — MPC | G3 | ✅ Class 9–10 only (transition to MPC preparation) | ❌ | Read-only |
| Group Stream Coord — BiPC | G3 | ❌ | ❌ | No access |
| Group Stream Coord — MEC/CEC | G3 | ❌ | ❌ | No access |
| Group JEE/NEET Integration Head | G3 | ✅ Class 9–10 only (pipeline awareness) | ❌ | Read-only |
| Group IIT Foundation Director | G3 | ✅ All classes, all branches | ✅ Full — create · edit · configure · manage batches | Primary operator |
| Group Olympiad & Scholarship Coord | G3 | ✅ All classes (for scholarship tracking) | ❌ | Read-only |
| Group Special Education Coordinator | G3 | ❌ | ❌ | No access |
| Group Academic MIS Officer | G1 | ✅ Summary stats only | ❌ | Read-only |
| Group Academic Calendar Manager | G3 | ✅ Schedule dates only | ❌ | Read-only — calendar coordination |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Academic  ›  IIT Foundation  ›  Program Manager
```

### 3.2 Page Header
```
IIT Foundation Program Manager                      [+ Create Class Config]  [Export Program Report ↓]
[Group Name] · Academic Year [YYYY–YY]              IIT Foundation Director only — actions
```

### 3.3 Class Tabs

Five primary tabs: **Class 6** · **Class 7** · **Class 8** · **Class 9** · **Class 10**

Each tab shows the complete programme configuration and data for that class level. Tab switching reloads the content area via HTMX.

### 3.4 Summary Stats Bar (per class tab)

| Stat | Value (example: Class 8) |
|---|---|
| Total Enrolled (Class 8) | 3,240 |
| Branches Running Class 8 Foundation | 38 of 50 |
| Subjects Offered | 3 (Maths · Physics · Chemistry) |
| Total Batches | 72 |
| Avg Batch Size | 45 |
| Test Count (This Term) | 6 |
| Study Material Items | 84 |

---

## 4. Main Content

### 4.1 Content Table (per class tab)

Shows the subject-level programme configuration for the selected class.

**Search:** Subject name — 300ms debounce.

**Filters:**

| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Subject | Multi-select | Mathematics · Physics · Chemistry · Biology (Class 9–10) |
| Status | Select | Active · Draft · Inactive |

### 4.2 Columns — Content/Programme Table

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Subject | Badge | ✅ | Mathematics · Physics · Chemistry |
| Topics Covered | Fraction | ✅ | e.g. 18/24 topics in curriculum |
| Curriculum Coverage % | Progress bar | ✅ | Colour: Red < 60% · Amber 60–80% · Green > 80% |
| Study Material Count | Number | ✅ | Resources in Content Library for this class+subject |
| Test Count | Number | ✅ | Foundation tests conducted this term |
| Enrolled Students | Number | ✅ | Across all branches for this class |
| Status | Badge | ✅ | Active · Draft · Inactive |
| Last Updated | Date | ✅ | |
| Actions | — | ❌ | See row actions |

**Default sort:** Subject name.

**Pagination:** Server-side · Default 25/page.

### 4.3 Row Actions — Content Table

| Action | Visible To | Opens | Notes |
|---|---|---|---|
| View Subject Detail | All with access | `subject-detail` drawer 560px | Curriculum, material, test history |
| Edit Class Config | Foundation Dir · CAO | `class-config` drawer 560px | Hours/week, syllabus, faculty requirements |
| Upload Study Material | Foundation Dir · Curriculum Coord | Links to Content Library (page 17) with class/subject pre-filled | |
| View Tests | Foundation Dir · CAO | Links to Foundation Test Series (page 40) filtered by class+subject | |

---

### 4.4 Batch Management Table (below content table)

A separate section per class tab: "Batch Management — Class [N] Foundation"

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Batch ID | Text | ✅ | Auto-generated: e.g. HYD04-CL8-B01 |
| Branch | Text | ✅ | Branch name + code |
| Class | Text | ❌ | Same as current tab |
| Students Enrolled | Number | ✅ | |
| Faculty (Primary) | Text | ❌ | Faculty name |
| Faculty (Secondary) | Text | ❌ | Optional co-teacher |
| Schedule | Text | ❌ | Days/periods as text |
| Status | Badge | ✅ | Active · Inactive · Draft |
| Actions | — | ❌ | See batch row actions |

**Batch size alert:** Rows where Students Enrolled > 60 shown with amber row highlight + tooltip "Batch size exceeds recommended maximum of 60. Consider splitting."

**Default sort:** Branch name, then Batch ID.

**Pagination:** Server-side · Default 25/page.

### 4.5 Batch Row Actions

| Action | Visible To | Opens | Notes |
|---|---|---|---|
| View Batch | All with access | `batch-detail` drawer 480px | Students list, schedule, faculty |
| Edit Batch | Foundation Dir · CAO | `batch-edit` drawer 480px | Edit faculty, schedule, students |
| Deactivate Batch | Foundation Dir · CAO | Confirm modal 380px | With reason |

### 4.6 Bulk Actions (batch table)

| Action | Visible To | Notes |
|---|---|---|
| Send Faculty Reminder | Foundation Dir | Reminds selected batch faculty of upcoming test/deadline |
| Export Batch Report (XLSX) | Foundation Dir · CAO · MIS | Batch data export |

---

## 5. Drawers & Modals

### 5.1 Drawer: `class-config`
- **Trigger:** [+ Create Class Config] header button or "Edit Class Config" row action
- **Width:** 560px
- **Title:** "Class [N] Foundation — Configuration"
- **Tabs:** Subjects · Hours & Schedule · Faculty Requirements · Branch Scope

#### Tab: Subjects
For each subject:
| Field | Type |
|---|---|
| Subject Name | Pre-defined (Maths / Physics / Chemistry) |
| Include in Class [N] | Toggle |
| Curriculum Reference | Select — CBSE / NCERT / Foundation proprietary |
| Topics Required | Number — expected topic count |
| Passing Marks (%) | Number |
| Textbook | Text — title and edition |

#### Tab: Hours & Schedule
| Field | Type | Required |
|---|---|---|
| Coaching Hours per Week | Number (per subject) | ✅ |
| Class Days | Multi-select (Mon–Sat) | ✅ |
| Preferred Period Slots | Multi-select | ✅ |
| Annual Lecture Hours Target | Number | ❌ |

#### Tab: Faculty Requirements
| Field | Type | Required |
|---|---|---|
| Min Qualification (Maths) | Select — B.Sc/B.Tech/M.Sc/IIT Alumni preferred | ✅ |
| Min Qualification (Physics) | Select | ✅ |
| Min Qualification (Chemistry) | Select | ✅ |
| IIT/NIT background preferred | Toggle | ❌ |
| Note to branches | Textarea — sent to branch when class setup is pushed | ❌ |

#### Tab: Branch Scope
- Radio: Apply to All Branches · Apply to Selected Branches
- Multi-select (if selected): Branches running Foundation at this class level

**Submit:** [Save Configuration] — pushes config to selected branches.

---

### 5.2 Drawer: `subject-detail`
- **Width:** 560px
- **Tabs:** Curriculum · Study Material · Test History · Branch Adherence

#### Tab: Curriculum
Topic list for this class+subject from Subject-Topic Master — Name · Difficulty · Sequence No · Covered (Y/N) — progress bar at top.

#### Tab: Study Material
List of resources in Content Library tagged to this class+subject: Title · Type · Uploaded By · Date · Downloads · Status

[Upload New Resource →] links to Content Library with pre-fill.

#### Tab: Test History
Table of foundation tests for this class+subject: Test # · Date · Branches · Results Published (Y/N) · Group Avg % — links to page 40.

#### Tab: Branch Adherence
Table: Branch · Topics Covered % · Material Available (Y/N) · Test Count · Status — colour-coded by coverage %.

---

### 5.3 Drawer: `batch-detail` / `batch-edit`
- **Width:** 480px
- **Batch Detail tabs:** Overview · Students · Schedule · Faculty

**Overview:** Batch ID · Branch · Class · Enrolled count · Status · Created date.

**Students tab:** Student name · Roll Number · Class section · Admission date — sortable table.

**Schedule tab:** Day-by-day timetable for this batch's Foundation periods.

**Faculty tab:** Primary faculty details + Secondary faculty (if any) — name, qualification, IIT background (Y/N), contact.

**Edit mode (batch-edit):** All fields editable except Batch ID and Branch.

---

### 5.4 Modal: `deactivate-batch-confirm`
- **Width:** 380px
- **Title:** "Deactivate Batch — [Batch ID] — [Branch]"
- **Content:** "Students in this batch will need to be reassigned to another batch or enrolled individually."
- **Fields:** Reason (required, min 20 chars)
- **Buttons:** [Confirm Deactivation] (danger) + [Cancel]

---

## 6. Charts

### 6.1 Enrollment by Class — Across Branches (Grouped Bar)
- **Type:** Vertical grouped bar chart
- **X-axis:** Class levels (Class 6 · 7 · 8 · 9 · 10)
- **Y-axis:** Student count
- **Bars:** One colour per selected branch subset — or total group bar if no branch filter
- **Tooltip:** Class · Total Students · Branches running
- **Shown:** In "Enrollment Overview" collapsible card at top of page (above tabs)
- **Export:** PNG

### 6.2 Curriculum Coverage by Class (Horizontal Stacked Bar)
- **Type:** Horizontal stacked bar
- **Y-axis:** Class levels (Class 6–10)
- **X-axis:** Topic count
- **Stacks:** Covered (green) · Not Covered (red)
- **Tooltip:** Class · Covered: N · Not Covered: N · Coverage %
- **Export:** PNG

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Class config saved | "Class [N] Foundation configuration saved and pushed to [N] branches." | Success | 5s |
| Batch created | "Batch [ID] created for [Branch] — Class [N] Foundation." | Success | 4s |
| Batch edited | "Batch [ID] updated." | Success | 4s |
| Batch deactivated | "Batch [ID] deactivated. [N] students need reassignment." | Warning | 6s |
| Faculty reminder sent | "Reminder sent to [N] faculty members." | Success | 4s |
| Programme report export | "Programme report preparing — download will begin shortly." | Info | 4s |
| Batch size warning | "Batch [ID] at [Branch] exceeds recommended size of 60. Consider splitting." | Warning | 6s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| Class not configured | "Class [N] Not Configured" | "Foundation programme for Class [N] has not been set up yet. Create the class configuration to begin." | [+ Create Class Config] |
| No batches for class | "No Batches Created" | "No Foundation batches exist for Class [N] yet. Branch coordinators must create batches after class is configured." | — |
| No branches running this class | "No Branches Offering Class [N]" | "No branches have activated Class [N] Foundation yet" | — |
| No study material | "No Study Material" | "No resources have been uploaded for this class and subject yet" | [Upload Resource →] |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: stats bar + content table (5 rows) + batch table (5 rows) |
| Class tab switch | Full tab content area skeleton reload |
| Content/batch table filter | Inline skeleton rows |
| Class-config drawer open | Spinner in drawer body |
| Subject-detail drawer open | Spinner + skeleton tabs |
| Batch-detail/edit drawer | Spinner in drawer body |
| Charts load | Spinner centred in chart card |
| Export trigger | Spinner in export button (momentary) |

---

## 10. Role-Based UI Visibility

| Element | Foundation Dir G3 | CAO G4 | Curriculum Coord G2 | MIS G1 |
|---|---|---|---|---|
| [+ Create Class Config] | ✅ | ❌ (can approve) | ❌ | ❌ |
| Edit Class Config row action | ✅ | ✅ | ❌ | ❌ |
| Upload Study Material | ✅ | ❌ | ✅ | ❌ |
| Batch Edit | ✅ | ✅ | ❌ | ❌ |
| Batch Deactivate | ✅ | ✅ | ❌ | ❌ |
| Faculty Reminder bulk action | ✅ | ❌ | ❌ | ❌ |
| Export Programme Report | ✅ | ✅ | ❌ | ✅ |
| Branch Adherence tab in drawer | ✅ | ✅ | ❌ | ✅ |
| Enrollment charts | ✅ | ✅ | ❌ | ✅ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/acad/iit-foundation/program/` | JWT | Programme overview — class tabs summary |
| GET | `/api/v1/group/{group_id}/acad/iit-foundation/program/stats/` | JWT | Stats bar for selected class |
| GET | `/api/v1/group/{group_id}/acad/iit-foundation/program/class/{class_level}/` | JWT | Content table for class tab |
| GET | `/api/v1/group/{group_id}/acad/iit-foundation/program/class/{class_level}/config/` | JWT | Class config for drawer |
| POST | `/api/v1/group/{group_id}/acad/iit-foundation/program/class/{class_level}/config/` | JWT (Foundation Dir) | Create class config |
| PUT | `/api/v1/group/{group_id}/acad/iit-foundation/program/class/{class_level}/config/` | JWT (Foundation Dir / CAO) | Update class config |
| GET | `/api/v1/group/{group_id}/acad/iit-foundation/program/class/{class_level}/subjects/{subject_id}/` | JWT | Subject detail drawer data |
| GET | `/api/v1/group/{group_id}/acad/iit-foundation/program/batches/` | JWT | Batch list (filterable by class/branch) |
| POST | `/api/v1/group/{group_id}/acad/iit-foundation/program/batches/` | JWT (Foundation Dir) | Create batch |
| GET | `/api/v1/group/{group_id}/acad/iit-foundation/program/batches/{batch_id}/` | JWT | Batch detail |
| PUT | `/api/v1/group/{group_id}/acad/iit-foundation/program/batches/{batch_id}/` | JWT (Foundation Dir / CAO) | Update batch |
| POST | `/api/v1/group/{group_id}/acad/iit-foundation/program/batches/{batch_id}/deactivate/` | JWT (Foundation Dir / CAO) | Deactivate batch |
| POST | `/api/v1/group/{group_id}/acad/iit-foundation/program/batches/notify-faculty/` | JWT (Foundation Dir) | Send faculty reminder |
| GET | `/api/v1/group/{group_id}/acad/iit-foundation/program/export/report/?format=xlsx` | JWT | Programme report export |
| GET | `/api/v1/group/{group_id}/acad/iit-foundation/program/charts/enrollment/` | JWT | Enrollment by class chart |
| GET | `/api/v1/group/{group_id}/acad/iit-foundation/program/charts/curriculum-coverage/` | JWT | Curriculum coverage chart |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Class tab switch | `click` | GET `.../program/class/{level}/` | `#foundation-class-tab-content` | `innerHTML` |
| Content table filter | `click` | GET `.../program/class/{level}/?filters=` | `#content-table-section` | `innerHTML` |
| Batch table filter | `click` | GET `.../program/batches/?class={level}&filters=` | `#batch-table-section` | `innerHTML` |
| Class-config drawer open | `click` | GET `.../program/class/{level}/config/` | `#drawer-body` | `innerHTML` |
| Subject-detail drawer open | `click` | GET `.../program/class/{level}/subjects/{id}/` | `#drawer-body` | `innerHTML` |
| Batch-detail drawer open | `click` | GET `.../program/batches/{id}/` | `#drawer-body` | `innerHTML` |
| Save class config | `submit` | POST/PUT `.../program/class/{level}/config/` | `#drawer-body` | `innerHTML` |
| Deactivate batch | `click` | POST `.../program/batches/{id}/deactivate/` | `#batch-row-{id}` | `outerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
