# 15 — Syllabus Manager

> **URL:** `/group/acad/syllabus/`
> **File:** `15-syllabus-manager.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** CAO G4 · Academic Director G3 · Curriculum Coordinator G2 · Exam Controller G3 · Stream Coords G3 · Academic MIS Officer G1

---

## 1. Purpose

The Syllabus Manager is the authoritative group-wide syllabus master. Every stream, class, subject, and topic that exists in the institution group is defined here. Branches inherit the group syllabus automatically — they can view their assigned syllabi but cannot create, edit, or override anything at the group level.

For a large group operating 50 branches across 5 states with streams ranging from MPC and BiPC to IIT Foundation (Classes 6–10) and Integrated JEE/NEET, this page is the single point of truth. Any change made here cascades to all 50 branches simultaneously, making consistency across locations guaranteed by design rather than by process.

The page enables the Curriculum Coordinator and Academic Director to design syllabi against CBSE or State Board norms, map topics to estimated teaching hours, set difficulty levels, and track how closely each branch adheres to the prescribed curriculum week by week. The Coverage % column shows live adherence data pulled from branch lesson logs, giving CAO-level visibility into which branches are behind schedule before a mid-term review.

---

## 2. Role Access

| Role | Level | Can View | Can Create | Can Edit | Can Delete | Notes |
|---|---|---|---|---|---|---|
| Chief Academic Officer (CAO) | G4 | ✅ All streams | ✅ | ✅ | ✅ (Archive only) | Full authority — approve and publish syllabi |
| Group Academic Director | G3 | ✅ All streams | ✅ | ✅ | ✅ (Archive only) | Operational ownership of syllabus design |
| Group Curriculum Coordinator | G2 | ✅ All streams | ✅ | ✅ Topics & subtopics | ❌ | Upload and edit topics; cannot archive streams |
| Group Exam Controller | G3 | ✅ All streams | ❌ | ❌ | ❌ | View-only — cross-reference with question bank |
| Group Results Coordinator | G3 | ✅ All streams | ❌ | ❌ | ❌ | View-only |
| Stream Coord — MPC | G3 | ✅ MPC only | ❌ | ❌ | ❌ | Filtered to MPC stream only |
| Stream Coord — BiPC | G3 | ✅ BiPC only | ❌ | ❌ | ❌ | Filtered to BiPC stream only |
| Stream Coord — MEC/CEC | G3 | ✅ MEC/CEC only | ❌ | ❌ | ❌ | Filtered to MEC/CEC stream only |
| JEE/NEET Integration Head | G3 | ✅ MPC+BiPC | ❌ | ❌ | ❌ | Views JEE/NEET-relevant streams |
| IIT Foundation Director | G3 | ✅ Foundation only | ❌ | ❌ | ❌ | Filtered to Foundation Classes 6–10 |
| Olympiad & Scholarship Coord | G3 | ✅ All streams | ❌ | ❌ | ❌ | View-only for curriculum cross-reference |
| Special Education Coordinator | G3 | ✅ All streams | ❌ | ❌ | ❌ | View-only for IEP curriculum mapping |
| Academic MIS Officer | G1 | ✅ All streams | ❌ | ❌ | ❌ | Read-only data access |
| Academic Calendar Manager | G3 | ✅ All streams | ❌ | ❌ | ❌ | View to align calendar events with syllabus milestones |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Academic  ›  Syllabus Manager
```

### 3.2 Page Header (with action buttons — role-gated)
```
Syllabus Manager                          [+ New Syllabus]  [Import CSV ↑]  [Export XLSX ↓]
[Group Name] · Group-wide curriculum master               (CAO / Academic Dir only)
```

Action button visibility:
- `[+ New Syllabus]` — CAO, Academic Director only
- `[Import CSV ↑]` — CAO, Academic Director, Curriculum Coordinator
- `[Export XLSX ↓]` — All roles with view access

### 3.3 Summary Stats Bar
| Stat | Value |
|---|---|
| Total Syllabi | Count across all streams |
| Active | Published syllabi in use |
| Draft | Syllabi in creation, not yet published |
| Archived | Retired syllabi |
| Avg Curriculum Coverage | Group-wide coverage % this term |
| Branches Below 70% | Count of branches with coverage < 70% |

Stats bar refreshes on page load. Coverage % is pulled live from branch lesson completion logs.

---

## 4. Main Syllabus Table

### 4.1 Search
- Full-text across: Subject Name, Topic Keyword, Stream Name
- 300ms debounce · Highlights match in Subject column
- Scope: Current academic year by default

### 4.2 Advanced Filters (slide-in filter drawer)

| Filter | Type | Options |
|---|---|---|
| Stream | Multi-select | MPC · BiPC · MEC · CEC · HEC · IIT Foundation · Integrated JEE · Integrated NEET |
| Class | Multi-select | Class 6 · 7 · 8 · 9 · 10 · 11 · 12 |
| Subject | Multi-select | Populated based on Stream + Class selection |
| Board | Multi-select | CBSE · BSEAP · BSETS · ICSE · State Board |
| Status | Multi-select | Active · Draft · Archived |
| Coverage Band | Select | Below 70% · 70–85% · Above 85% |
| Last Updated | Date range | From / To date picker |

Active filter chips: dismissible, "Clear All" link, count badge on filter button.

### 4.3 Columns

| Column | Type | Sortable | Visible By | Notes |
|---|---|---|---|---|
| ☐ | Checkbox | — | All | Row select for bulk actions |
| Stream | Badge | ✅ | All | MPC / BiPC / MEC / CEC / HEC / Foundation |
| Class | Text | ✅ | All | e.g. Class 11, Class 12 |
| Subject | Text + link | ✅ | All | Opens syllabus-view drawer |
| Total Topics | Number | ✅ | All | Total topics defined in this syllabus |
| Covered % | Progress bar + % | ✅ | All | Live: branch avg coverage this term. Red < 70%, Amber < 85%, Green ≥ 85% |
| Last Updated | Date | ✅ | All | When syllabus was last edited |
| Board | Badge | ✅ | All | CBSE / BSEAP / BSETS / State Board |
| Status | Badge | ✅ | All | Active · Draft · Archived |
| Actions | — | ❌ | Role-based | See Row Actions |

**Column visibility toggle:** Gear icon top-right — saves preference per user.

**Default sort:** Stream ascending, then Subject ascending.

**Pagination:** Server-side · Default 25/page · Selector 10/25/50/All · "Showing X–Y of Z syllabi" · Page jump input.

### 4.4 Row Actions

| Action | Icon | Visible To | Drawer/Modal | Notes |
|---|---|---|---|---|
| View Topics | Eye | All | `syllabus-view` drawer 560px | Expands full topic list |
| Edit | Pencil | CAO, Academic Dir, Curriculum Coord | `syllabus-edit` drawer 640px | Edit metadata and topics |
| Archive | Archive box | CAO, Academic Dir | Confirm modal 420px | Soft archive — reason required |
| Clone for Another Stream | Copy | CAO, Academic Dir | `syllabus-clone` drawer 480px | Clone structure, then edit for target stream |

### 4.5 Bulk Actions

| Action | Visible To | Notes |
|---|---|---|
| Export Selected (XLSX) | All with export access | Exports full topic hierarchy for selected syllabi |
| Archive Selected | CAO, Academic Dir | Batch archive — requires reason |
| Change Status to Active | CAO, Academic Dir | Publish draft syllabi in batch |

---

## 5. Drawers & Modals

### 5.1 Drawer: `syllabus-create` — New Syllabus
- **Trigger:** [+ New Syllabus] header button
- **Width:** 640px
- **Tabs:** Stream & Class · Subjects · Topic List · Board Mapping · Publish

#### Tab: Stream & Class
| Field | Type | Required | Validation |
|---|---|---|---|
| Stream | Select | ✅ | MPC / BiPC / MEC / CEC / HEC / IIT Foundation / Integrated JEE / Integrated NEET |
| Class | Select | ✅ | Class 6–12 (options filtered by stream) |
| Academic Year | Select | ✅ | Current and next academic year (April–March) |
| Description | Textarea | ❌ | Max 500 chars |

#### Tab: Subjects
| Field | Type | Required | Validation |
|---|---|---|---|
| Subject Name | Text | ✅ | Min 2 chars, max 100 — must match Subject-Topic Master |
| Add Subject | Button | — | Adds a row for each subject in this stream/class combination |
| Subject Code | Text | ✅ | Alphanumeric, unique within stream+class |
| Total Teaching Hours | Number | ✅ | Min 10 |
| Pass Marks | Number | ✅ | 0–100 |
| Board Affiliation | Multi-select | ✅ | CBSE · BSEAP · BSETS |

#### Tab: Topic List
| Field | Type | Required | Validation |
|---|---|---|---|
| Chapter Name | Text | ✅ per row | Chapters under each subject |
| Topic Name | Text | ✅ per row | Topics under each chapter |
| Subtopics | Tag input | ❌ | Comma-separated |
| Sequence No. | Number | ✅ | Teaching order |
| Difficulty | Select | ✅ | 1 (Easy) · 2 · 3 · 4 · 5 (Hard) |
| Estimated Hours | Number | ✅ | Hours required to teach this topic |
| Linked Resources | Button | ❌ | Opens content library selector |
| NCERT Reference | Text | ❌ | Chapter reference e.g. "Physics Part 1, Ch. 4" |

Add/remove rows dynamically. Drag to reorder sequence.

#### Tab: Board Mapping
| Field | Type | Required | Validation |
|---|---|---|---|
| Board | Select | ✅ | CBSE · BSEAP · BSETS · ICSE |
| Prescribed Textbook | Text | ❌ | Links to Textbook & Resource Mapping |
| Board Topic Reference | Text | ❌ | Official board topic code or chapter number |
| Exam Weightage % | Number | ❌ | % of board exam from this topic |

#### Tab: Publish
| Field | Type | Required | Notes |
|---|---|---|---|
| Status | Select | ✅ | Draft · Active |
| Notify Branch Principals | Checkbox | — | Default on when publishing Active |
| Effective From | Date | ✅ | Must be within current or upcoming academic year |

**Submit:** "Create Syllabus" — disabled until Stream & Class and Topic List tabs are valid (tab icons show red dot if incomplete). On success: row appears in table, branches notified if Active.

### 5.2 Drawer: `syllabus-view` — View Syllabus
- **Trigger:** View Topics action or Subject column link
- **Width:** 560px
- **Tabs:** Overview · Topics · Branch Adherence · History

#### Tab: Overview
Displays: Stream, Class, Board, Subject count, Total topics, Effective date, Last updated, Status badge, Created by.

#### Tab: Topics
Collapsible chapter → topic → subtopic tree. Each topic shows: Sequence, Estimated hours, Difficulty badge, Linked resource count. Read-only.

#### Tab: Branch Adherence
Table: Branch Name · Topics Covered · Topics Remaining · Coverage % · Last Lesson Log Date.
Red rows where Coverage % < 70%. "Send Reminder" button per row (CAO/Academic Dir only).

#### Tab: History
Audit trail: timestamp · actor · action (created / edited / archived / published) · change summary.

### 5.3 Drawer: `syllabus-edit` — Edit Syllabus
- **Width:** 640px
- Same tabs as `syllabus-create`, pre-filled with existing data
- Cannot change Stream or Class after any branch has logged lessons against this syllabus — field is locked with tooltip explaining why
- Topic additions are non-destructive; existing topic sequence numbers are preserved

### 5.4 Drawer: `topic-edit` — Edit Single Topic
- **Trigger:** Inline topic edit within Topic List tab
- **Width:** 480px
- **Fields:** Topic name · Subtopics (tag input, add/remove) · Sequence no. · Difficulty (1–5 star select) · Estimated hours to teach · Linked resources (multi-select from content library) · NCERT reference (text)

### 5.5 Drawer: `syllabus-clone`
- **Trigger:** Clone for Another Stream row action
- **Width:** 480px
- **Fields:** Source stream (pre-filled, read-only) · Target stream (select) · Target class · New subject names (editable list pre-filled from source) · Which topics to include (All / Select manually)
- On confirm: New draft syllabus created in target stream with all topics cloned — opens `syllabus-edit` drawer for the clone.

### 5.6 Modal: Archive Confirm
- **Width:** 420px
- **Content:** "Archive syllabus for [Subject] — [Stream] Class [X]? Branches will no longer see this syllabus."
- **Fields:** Reason (required, min 20 chars) · Notify branch principals? (checkbox, default on)
- **Buttons:** [Confirm Archive] (danger) + [Cancel]

---

## 6. Charts

### 6.1 Curriculum Completion by Branch (Bar Chart)
- **Type:** Horizontal bar chart
- **Data:** Coverage % per branch for the selected stream/subject
- **X-axis:** Coverage % (0–100%)
- **Y-axis:** Branch names
- **Colour:** Red < 70%, Amber < 85%, Green ≥ 85%
- **Tooltip:** Branch · Subject · Coverage: X% · Topics done: N of M
- **Filter:** Stream selector, Subject selector, Class selector
- **Export:** PNG

### 6.2 Topic Coverage Heatmap by Subject
- **Type:** Heatmap grid
- **X-axis:** Subjects (within selected stream)
- **Y-axis:** Branches
- **Cell colour:** % topics covered — Red/Amber/Green scale
- **Tooltip:** Branch · Subject · % covered · Last updated
- **Export:** PNG · XLSX raw data

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Syllabus created | "Syllabus for [Subject] — [Stream] created successfully." | Success | 4s |
| Syllabus published (Active) | "Syllabus published. Branch principals notified." | Success | 4s |
| Syllabus updated | "[Subject] syllabus updated." | Success | 4s |
| Syllabus archived | "[Subject] syllabus archived." | Warning | 6s |
| Syllabus cloned | "Syllabus cloned to [Target Stream]. Review before publishing." | Info | 4s |
| CSV import success | "Import complete. [N] topics added, [M] updated." | Success | 4s |
| CSV import errors | "Import has [N] errors. Review the error report." | Error | Manual |
| Export started | "Export preparing… download will start shortly." | Info | 4s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No syllabi defined | "No syllabus defined yet" | "Start by creating a syllabus for a stream and class." | [+ New Syllabus] |
| No results for search | "No syllabus matches" | "Try different subject or topic keywords." | [Clear Search] |
| Filter returns empty | "No syllabi match your filters" | "Try removing some filters to see more results." | [Clear All Filters] |
| Stream selected — no syllabus | "No syllabus defined for [Stream]" | "Create the first syllabus for this stream." | [+ New Syllabus] |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: stats bar + table (10 skeleton rows) |
| Table filter/search/sort/page | Inline skeleton rows (10) |
| syllabus-create drawer open | Spinner in drawer body |
| syllabus-view drawer open | Spinner + skeleton tabs |
| syllabus-create submit | Spinner in submit button · success toast on resolve |
| Archive confirm submit | Spinner in confirm button |
| CSV import upload | Progress bar in import modal |
| Export trigger | Spinner in export button (momentary) |
| Charts load | Skeleton chart placeholders |

---

## 10. Role-Based UI Visibility

| Element | CAO G4 | Academic Dir G3 | Curriculum Coord G2 | Exam Controller G3 | Stream Coords G3 | MIS Officer G1 |
|---|---|---|---|---|---|---|
| [+ New Syllabus] button | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| [Import CSV] button | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| [Export XLSX] button | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Edit row action | ✅ | ✅ | ✅ (topics only) | ❌ | ❌ | ❌ |
| Archive row action | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Clone row action | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Branch Adherence tab | ✅ | ✅ | ✅ | ✅ | ✅ (own stream) | ✅ |
| Send Reminder (adherence) | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Covered % column | ✅ | ✅ | ✅ | ✅ | ✅ (own stream) | ✅ |
| Stream filter (all streams) | ✅ | ✅ | ✅ | ✅ | ❌ (own only) | ✅ |
| Charts section | ✅ | ✅ | ✅ | ✅ | ✅ (own stream) | ✅ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/acad/syllabus/` | JWT | List syllabi (filtered/sorted/paginated) |
| POST | `/api/v1/group/{group_id}/acad/syllabus/` | JWT (CAO/Dir) | Create new syllabus |
| GET | `/api/v1/group/{group_id}/acad/syllabus/{syl_id}/` | JWT | Syllabus detail |
| PUT | `/api/v1/group/{group_id}/acad/syllabus/{syl_id}/` | JWT (CAO/Dir/Coord) | Update syllabus |
| DELETE | `/api/v1/group/{group_id}/acad/syllabus/{syl_id}/` | JWT (CAO/Dir) | Archive syllabus (soft) |
| GET | `/api/v1/group/{group_id}/acad/syllabus/{syl_id}/topics/` | JWT | Topic list for syllabus |
| POST | `/api/v1/group/{group_id}/acad/syllabus/{syl_id}/topics/` | JWT (CAO/Dir/Coord) | Add topic |
| PUT | `/api/v1/group/{group_id}/acad/syllabus/{syl_id}/topics/{topic_id}/` | JWT (CAO/Dir/Coord) | Edit topic |
| GET | `/api/v1/group/{group_id}/acad/syllabus/{syl_id}/adherence/` | JWT | Branch adherence data |
| POST | `/api/v1/group/{group_id}/acad/syllabus/import/` | JWT (CAO/Dir/Coord) | CSV bulk import |
| GET | `/api/v1/group/{group_id}/acad/syllabus/export/` | JWT | XLSX export |
| GET | `/api/v1/group/{group_id}/acad/syllabus/stats/` | JWT | Summary stats bar data |
| GET | `/api/v1/group/{group_id}/acad/syllabus/charts/coverage-by-branch/` | JWT | Bar chart data |
| GET | `/api/v1/group/{group_id}/acad/syllabus/charts/topic-heatmap/` | JWT | Heatmap data |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Syllabus search | `input delay:300ms` | GET `.../syllabus/?q=` | `#syllabus-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../syllabus/?filters=` | `#syllabus-table-section` | `innerHTML` |
| Sort column | `click` | GET `.../syllabus/?sort=&dir=` | `#syllabus-table-section` | `innerHTML` |
| Pagination | `click` | GET `.../syllabus/?page=` | `#syllabus-table-section` | `innerHTML` |
| View topics drawer | `click` | GET `.../syllabus/{id}/` | `#drawer-body` | `innerHTML` |
| Create drawer open | `click` | GET `.../syllabus/create-form/` | `#drawer-body` | `innerHTML` |
| Create submit | `submit` | POST `.../syllabus/` | `#drawer-body` | `innerHTML` |
| Archive confirm | `click` | DELETE `.../syllabus/{id}/` | `#syllabus-row-{id}` | `outerHTML` |
| Stats bar refresh | `load` | GET `.../syllabus/stats/` | `#stats-bar` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
