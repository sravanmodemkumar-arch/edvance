# 16 — Lesson Plan Standards

> **URL:** `/group/acad/lesson-plans/`
> **File:** `16-lesson-plan-standards.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** CAO G4 · Academic Director G3 · Curriculum Coordinator G2 · Stream Coords G3 · Academic MIS Officer G1 · Academic Quality Officer (Div-P G1, view only)

---

## 1. Purpose

Lesson Plan Standards defines the group-wide templates and compliance framework for how every teacher across every branch must prepare and submit lesson plans. The CAO and Academic Director set the format — which sections are mandatory, what the assessment checklist must contain, and how plans must be structured before a class is taught. Branches then submit their lesson plans through the branch portal, and this page tracks compliance.

For a group with 2,000–5,000 teachers across 50 branches, uncontrolled lesson plan quality leads directly to inconsistent outcomes for students. This page exists to eliminate that inconsistency. Each template defines required sections (Learning Objective, Prior Knowledge Check, Pedagogy, Activity, Assessment, Homework), and the compliance engine scores every branch submission against the template automatically.

The Compliance % column gives Academic Directors an at-a-glance view of which branches are submitting complete, on-time lesson plans and which are not. Non-compliant branches can be sent automated WhatsApp or email reminders directly from this page. The Academic Quality Officer from Division P (Group Quality & Standards) also has read-only view access to monitor standards alignment across the group.

---

## 2. Role Access

| Role | Level | Can View | Can Create | Can Edit | Can Delete | Notes |
|---|---|---|---|---|---|---|
| Chief Academic Officer (CAO) | G4 | ✅ All | ✅ | ✅ | ✅ (Archive only) | Full authority over templates |
| Group Academic Director | G3 | ✅ All | ✅ | ✅ | ✅ (Archive only) | Operational ownership |
| Group Curriculum Coordinator | G2 | ✅ All | ✅ | ✅ Templates | ❌ | Create and edit templates; cannot archive |
| Group Exam Controller | G3 | ❌ | ❌ | ❌ | ❌ | No access |
| Group Results Coordinator | G3 | ❌ | ❌ | ❌ | ❌ | No access |
| Stream Coord — MPC | G3 | ✅ MPC only | ❌ | ❌ | ❌ | View own stream compliance only |
| Stream Coord — BiPC | G3 | ✅ BiPC only | ❌ | ❌ | ❌ | View own stream compliance only |
| Stream Coord — MEC/CEC | G3 | ✅ MEC/CEC only | ❌ | ❌ | ❌ | View own stream compliance only |
| JEE/NEET Integration Head | G3 | ✅ MPC+BiPC | ❌ | ❌ | ❌ | View relevant stream compliance |
| IIT Foundation Director | G3 | ✅ Foundation only | ❌ | ❌ | ❌ | View Foundation compliance |
| Olympiad & Scholarship Coord | G3 | ❌ | ❌ | ❌ | ❌ | No access |
| Special Education Coordinator | G3 | ✅ All streams | ❌ | ❌ | ❌ | View to check IEP-linked lesson accommodations |
| Academic MIS Officer | G1 | ✅ All | ❌ | ❌ | ❌ | Read-only |
| Academic Calendar Manager | G3 | ❌ | ❌ | ❌ | ❌ | No access |
| Academic Quality Officer (Div-P) | G1 | ✅ All | ❌ | ❌ | ❌ | Cross-division view — standards monitoring only |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Academic  ›  Lesson Plan Standards
```

### 3.2 Page Header (with action buttons — role-gated)
```
Lesson Plan Standards                     [+ New Template]  [Send Reminders]  [Export XLSX ↓]
[Group Name] · Compliance tracking across all branches     (CAO / Academic Dir only)
```

Action button visibility:
- `[+ New Template]` — CAO, Academic Director, Curriculum Coordinator
- `[Send Reminders]` — CAO, Academic Director only (bulk reminder to non-compliant branches)
- `[Export XLSX ↓]` — All roles with view access

### 3.3 Summary Stats Bar
| Stat | Value |
|---|---|
| Total Templates | Active lesson plan templates |
| Branches ≥ 90% Compliant | Count |
| Branches 70–90% | Count |
| Branches < 70% | Count (highlighted red) |
| Group Avg Compliance | % this term |
| Plans Submitted This Week | Count |

Stats bar refreshes on page load.

---

## 4. Main Lesson Plan Standards Table

### 4.1 Search
- Full-text across: Topic Name, Subject Name
- 300ms debounce · Highlights match in Topic column
- Scope: Current academic term by default

### 4.2 Advanced Filters (slide-in filter drawer)

| Filter | Type | Options |
|---|---|---|
| Stream | Multi-select | MPC · BiPC · MEC · CEC · HEC · IIT Foundation · Integrated JEE · Integrated NEET |
| Subject | Multi-select | Populated based on Stream selection |
| Class | Multi-select | Class 6–12 |
| Compliance Band | Select | Below 70% · 70–90% · 90% and above |
| Template Status | Multi-select | Active · Draft · Archived |
| Date Updated | Date range | From / To |

Active filter chips: dismissible, "Clear All" link, count badge on filter button.

### 4.3 Columns

| Column | Type | Sortable | Visible By | Notes |
|---|---|---|---|---|
| ☐ | Checkbox | — | All | Row select for bulk actions |
| Subject | Text + link | ✅ | All | Opens plan-template-create/edit drawer |
| Topic | Text | ✅ | All | Topic covered by this template |
| Class | Text | ✅ | All | e.g. Class 11 |
| Stream | Badge | ✅ | All | MPC / BiPC / MEC / CEC etc. |
| Template Type | Badge | ✅ | All | Standard · Foundation · IEP-Adapted |
| Branch Submissions | Number + link | ✅ | All | Count of branch submissions for this topic |
| Compliance % | Progress bar + % | ✅ | All | Red < 70%, Amber < 90%, Green ≥ 90% |
| Last Updated | Date | ✅ | All | When template was last edited |
| Status | Badge | ✅ | All | Active · Draft · Archived |
| Actions | — | ❌ | Role-based | See Row Actions |

**Column visibility toggle:** Gear icon top-right — saves preference per user.

**Default sort:** Compliance % ascending (most non-compliant first).

**Pagination:** Server-side · Default 25/page · Selector 10/25/50/All · "Showing X–Y of Z templates" · Page jump input.

### 4.4 Row Actions

| Action | Icon | Visible To | Drawer/Modal | Notes |
|---|---|---|---|---|
| View Submissions | Eye | All | `branch-submission-view` drawer 560px | See branch submission status |
| Edit Template | Pencil | CAO, Academic Dir, Curriculum Coord | `plan-template-create` drawer 640px (edit mode) | Pre-filled form |
| Archive | Archive box | CAO, Academic Dir | Confirm modal 420px | Soft archive — reason required |
| Send Reminder | Bell | CAO, Academic Dir | Inline confirm toast | Sends WhatsApp/email to non-compliant branches for this topic |

### 4.5 Bulk Actions

| Action | Visible To | Notes |
|---|---|---|
| Send Reminder to Non-Compliant Branches | CAO, Academic Dir | Generates WhatsApp/email to branch principals where compliance < threshold |
| Export Selected (XLSX) | All with view access | Exports selected template rows with compliance data |
| Archive Selected | CAO, Academic Dir | Batch archive — requires shared reason |

---

## 5. Drawers & Modals

### 5.1 Drawer: `plan-template-create` — New / Edit Template
- **Trigger:** [+ New Template] button or Edit row action
- **Width:** 640px
- **Tabs:** Template Structure · Required Sections · Assessment Checklist · Publish

#### Tab: Template Structure
| Field | Type | Required | Validation |
|---|---|---|---|
| Template Name | Text | ✅ | Min 3 chars, max 100 |
| Subject | Select | ✅ | From Subject-Topic Master |
| Topic | Select | ✅ | Filtered by Subject selection |
| Class | Select | ✅ | Class 6–12 |
| Stream | Multi-select | ✅ | At least 1 stream |
| Template Type | Select | ✅ | Standard · Foundation · IEP-Adapted |
| Duration (periods) | Number | ✅ | 1–10 periods |
| Teaching Method | Multi-select | ❌ | Lecture · Discussion · Activity · Demo · Lab · Group Work |

#### Tab: Required Sections
Dynamic section builder. Drag to reorder. Add/remove sections.

| Field | Type | Required | Validation |
|---|---|---|---|
| Section Name | Text | ✅ | e.g. "Learning Objective", "Prior Knowledge Check", "Assessment" |
| Description / Instruction | Textarea | ❌ | Guidance for teachers filling this section |
| Mandatory | Toggle | ✅ | Mandatory sections block submission if empty |
| Character Limit | Number | ❌ | Min characters teachers must write |

Pre-built defaults: Learning Objective · Prior Knowledge Check · Pedagogy & Delivery · Student Activity · Assessment · Homework / Follow-up.

#### Tab: Assessment Checklist
| Field | Type | Required | Notes |
|---|---|---|---|
| Checklist Item | Text | ✅ per row | e.g. "Formative assessment question included?" |
| Type | Select | ✅ | Self-check (teacher) · Auto-check (system validates content exists) |
| Add Checklist Item | Button | — | Adds a new row |

#### Tab: Publish
| Field | Type | Required | Notes |
|---|---|---|---|
| Status | Select | ✅ | Draft · Active |
| Effective From | Date | ✅ | Within current or upcoming academic term |
| Notify Branch Principals | Checkbox | — | Default on when publishing Active |
| Compliance Threshold % | Number | ✅ | Minimum compliance % — default 90% |
| Reminder Frequency | Select | ❌ | Weekly · Bi-weekly · Monthly (auto-reminders to non-compliant) |

**Submit:** "Save Template" — disabled until all required sections are filled.

### 5.2 Drawer: `branch-submission-view` — Branch Submissions
- **Trigger:** View Submissions row action or Branch Submissions column link
- **Width:** 560px
- **Tabs:** Submitted Plans · Missing Submissions · Feedback Sent

#### Tab: Submitted Plans
Table: Branch Name · Teacher Name · Submitted At · Compliance Score · Status (Pass/Fail checklist).
Expandable rows: click to view full submitted plan text.

#### Tab: Missing Submissions
Table: Branch Name · Teacher Name · Topic · Deadline · Days Overdue.
[Send Reminder] button per row (CAO/Academic Dir only). [Send All Reminders] bulk button.

#### Tab: Feedback Sent
Table: Branch Name · Teacher · Feedback Content · Sent By · Sent At · Channel (WhatsApp/Email).

### 5.3 Modal: Archive Template Confirm
- **Width:** 420px
- **Content:** "Archive lesson plan template for [Topic] — [Subject]? Existing branch submissions will be retained."
- **Fields:** Reason (required, min 20 chars) · Notify branch principals? (checkbox)
- **Buttons:** [Confirm Archive] (danger) + [Cancel]

### 5.4 Modal: Send Bulk Reminder Confirm
- **Width:** 420px
- **Content:** "Send reminder to [N] branches with compliance below [threshold]%?"
- **Fields:** Message preview (editable) · Channel (WhatsApp / Email / Both)
- **Buttons:** [Send Reminders] (primary) + [Cancel]
- On confirm: bulk notification dispatched · toast confirmation · reminder log entry created

---

## 6. Charts

### 6.1 Compliance by Branch (Bar Chart)
- **Type:** Horizontal bar chart
- **Data:** Compliance % per branch for selected stream/subject
- **X-axis:** Compliance % (0–100%)
- **Y-axis:** Branch names
- **Colour:** Red < 70%, Amber < 90%, Green ≥ 90%
- **Tooltip:** Branch · Subject · Compliance: X% · Submitted: N · Missing: M
- **Export:** PNG

### 6.2 Submission Trend (Line Chart)
- **Type:** Line chart — weekly data points
- **Data:** % plans submitted vs expected per week, last 8 weeks
- **X-axis:** Week
- **Y-axis:** Submission %
- **Tooltip:** Week · Submitted: N · Expected: M · %
- **Export:** PNG

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Template created | "Lesson plan template for [Topic] created." | Success | 4s |
| Template published | "Template published. Branch principals notified." | Success | 4s |
| Template updated | "[Topic] template updated." | Success | 4s |
| Template archived | "[Topic] template archived." | Warning | 6s |
| Reminder sent (single) | "Reminder sent to [N] non-compliant branches for [Topic]." | Info | 4s |
| Reminder sent (bulk) | "Reminders sent to [N] branches." | Info | 4s |
| Export started | "Export preparing… download will start shortly." | Info | 4s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No templates created | "No lesson plan templates yet" | "Create the first template to define standards for your branches." | [+ New Template] |
| No results for search | "No templates match" | "Try a different topic or subject name." | [Clear Search] |
| Filter returns empty | "No templates match your filters" | "Try removing some filters." | [Clear All Filters] |
| No submissions for topic | "No submissions yet" | "No branch has submitted a lesson plan for this topic yet." | — |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: stats bar + table (10 skeleton rows) |
| Table filter/search/sort/page | Inline skeleton rows (10) |
| plan-template-create drawer open | Spinner in drawer body |
| branch-submission-view drawer open | Spinner + skeleton tabs |
| Template save submit | Spinner in submit button |
| Reminder send action | Spinner in Send Reminder button |
| Charts load | Skeleton chart placeholders |
| Export trigger | Spinner in export button (momentary) |

---

## 10. Role-Based UI Visibility

| Element | CAO G4 | Academic Dir G3 | Curriculum Coord G2 | Stream Coords G3 | MIS Officer G1 | Acad Quality Officer (Div-P) G1 |
|---|---|---|---|---|---|---|
| [+ New Template] button | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| [Send Reminders] button | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| [Export XLSX] button | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Edit row action | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| Archive row action | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Send Reminder (row) | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Missing Submissions tab | ✅ | ✅ | ✅ | ✅ (own stream) | ✅ | ✅ |
| Compliance % column | ✅ | ✅ | ✅ | ✅ (own stream) | ✅ | ✅ |
| Stream filter (all streams) | ✅ | ✅ | ✅ | ❌ (own only) | ✅ | ✅ |
| Bulk archive | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Charts section | ✅ | ✅ | ✅ | ✅ (own stream) | ✅ | ✅ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/acad/lesson-plans/` | JWT | List templates (filtered/sorted/paginated) |
| POST | `/api/v1/group/{group_id}/acad/lesson-plans/` | JWT (CAO/Dir/Coord) | Create new template |
| GET | `/api/v1/group/{group_id}/acad/lesson-plans/{tpl_id}/` | JWT | Template detail |
| PUT | `/api/v1/group/{group_id}/acad/lesson-plans/{tpl_id}/` | JWT (CAO/Dir/Coord) | Update template |
| DELETE | `/api/v1/group/{group_id}/acad/lesson-plans/{tpl_id}/` | JWT (CAO/Dir) | Archive template (soft) |
| GET | `/api/v1/group/{group_id}/acad/lesson-plans/{tpl_id}/submissions/` | JWT | Branch submission list |
| POST | `/api/v1/group/{group_id}/acad/lesson-plans/{tpl_id}/remind/` | JWT (CAO/Dir) | Send reminder to non-compliant branches |
| POST | `/api/v1/group/{group_id}/acad/lesson-plans/remind-all/` | JWT (CAO/Dir) | Bulk reminder — all non-compliant |
| GET | `/api/v1/group/{group_id}/acad/lesson-plans/stats/` | JWT | Summary stats bar |
| GET | `/api/v1/group/{group_id}/acad/lesson-plans/export/` | JWT | XLSX export |
| GET | `/api/v1/group/{group_id}/acad/lesson-plans/charts/compliance-by-branch/` | JWT | Bar chart data |
| GET | `/api/v1/group/{group_id}/acad/lesson-plans/charts/submission-trend/` | JWT | Line chart data |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Topic search | `input delay:300ms` | GET `.../lesson-plans/?q=` | `#lp-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../lesson-plans/?filters=` | `#lp-table-section` | `innerHTML` |
| Sort column | `click` | GET `.../lesson-plans/?sort=&dir=` | `#lp-table-section` | `innerHTML` |
| Pagination | `click` | GET `.../lesson-plans/?page=` | `#lp-table-section` | `innerHTML` |
| View submissions drawer | `click` | GET `.../lesson-plans/{id}/submissions/` | `#drawer-body` | `innerHTML` |
| Create drawer open | `click` | GET `.../lesson-plans/create-form/` | `#drawer-body` | `innerHTML` |
| Create submit | `submit` | POST `.../lesson-plans/` | `#drawer-body` | `innerHTML` |
| Send single reminder | `click` | POST `.../lesson-plans/{id}/remind/` | `#toast-container` | `beforeend` |
| Stats bar refresh | `load` | GET `.../lesson-plans/stats/` | `#stats-bar` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
