# 18 — Subject-Topic Master

> **URL:** `/group/acad/subject-topic/`
> **File:** `18-subject-topic-master.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** CAO G4 · Academic Director G3 · Curriculum Coordinator G2 · Exam Controller G3 · Stream Coords G3

---

## 1. Purpose

The Subject-Topic Master is the foundational taxonomy of the entire academic platform. Every other module — Syllabus Manager, Content Library, Question Bank, Exam Paper Builder, Lesson Plan Standards, Result Moderation — references this master list for its subject and topic data. If a subject or topic is not defined here, it cannot exist in any other module.

The hierarchy is: Stream → Class → Subject → Chapter → Topic → Subtopic. For a large group with streams from MPC and BiPC to IIT Foundation (Classes 6–10) and Integrated JEE/NEET, this master can contain 80–120 subject-topic pairs per stream, totalling several thousand entries across all streams and classes. Maintaining this master is therefore a critical and deliberate activity — changes here cascade everywhere.

The page supports both a tree view (expand/collapse hierarchy) and a flat table view (sortable, filterable). Tree view is ideal for navigating the hierarchy visually; table view is better for auditing, searching, and bulk operations. A CSV bulk import workflow allows the Curriculum Coordinator to populate or update the master from a spreadsheet, with a row-level validation error report before anything is committed.

---

## 2. Role Access

| Role | Level | Can View | Can Create | Can Edit | Can Delete | Notes |
|---|---|---|---|---|---|---|
| Chief Academic Officer (CAO) | G4 | ✅ All | ✅ | ✅ | ✅ (Archive only) | Full authority |
| Group Academic Director | G3 | ✅ All | ✅ | ✅ | ✅ (Archive only) | Operational ownership |
| Group Curriculum Coordinator | G2 | ✅ All | ✅ | ✅ | ❌ | Create/edit subjects and topics; cannot archive |
| Group Exam Controller | G3 | ✅ All | ❌ | ❌ | ❌ | View for question bank subject/topic mapping |
| Group Results Coordinator | G3 | ❌ | ❌ | ❌ | ❌ | No access |
| Stream Coord — MPC | G3 | ✅ MPC only | ❌ | ❌ | ❌ | View own stream hierarchy |
| Stream Coord — BiPC | G3 | ✅ BiPC only | ❌ | ❌ | ❌ | View own stream hierarchy |
| Stream Coord — MEC/CEC | G3 | ✅ MEC/CEC only | ❌ | ❌ | ❌ | View own stream hierarchy |
| JEE/NEET Integration Head | G3 | ✅ MPC+BiPC | ❌ | ❌ | ❌ | View for curriculum mapping |
| IIT Foundation Director | G3 | ✅ Foundation only | ❌ | ❌ | ❌ | View Foundation Classes 6–10 |
| Olympiad & Scholarship Coord | G3 | ✅ All | ❌ | ❌ | ❌ | View for olympiad topic alignment |
| Special Education Coordinator | G3 | ❌ | ❌ | ❌ | ❌ | No access |
| Academic MIS Officer | G1 | ❌ | ❌ | ❌ | ❌ | No access |
| Academic Calendar Manager | G3 | ❌ | ❌ | ❌ | ❌ | No access |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Academic  ›  Subject-Topic Master
```

### 3.2 Page Header (with action buttons — role-gated)
```
Subject-Topic Master                      [+ Add Subject]  [Import CSV ↑]  [Export XLSX ↓]  [Tree | Table]
[Group Name] · Canonical subject-topic hierarchy           (CAO / Academic Dir / Curriculum Coord for create/import)
```

Action button visibility:
- `[+ Add Subject]` — CAO, Academic Director, Curriculum Coordinator
- `[Import CSV ↑]` — CAO, Academic Director, Curriculum Coordinator
- `[Export XLSX ↓]` — All roles with view access
- `[Tree | Table]` toggle — All roles (view mode preference, saved per user)

### 3.3 Summary Stats Bar
| Stat | Value |
|---|---|
| Total Subjects | Count across all streams |
| Total Topics | Count across all subjects |
| Total Subtopics | Count |
| Streams Covered | Count of streams with at least 1 subject |
| Topics Without Content | Topics with no linked content library resource |
| Topics Without Questions | Topics with no linked question bank entry |

Stats bar refreshes on page load. "Topics Without Content" and "Topics Without Questions" are actionable gap indicators.

---

## 4. Main Content — Tree View & Table View

### 4.1 Search
- Full-text across: Subject Name, Chapter Name, Topic Name, Subtopic Name
- 300ms debounce · In tree view: expands tree to show matching nodes, dims non-matching · In table view: highlights match in Topic column
- Scope: All active entries by default

### 4.2 Advanced Filters (slide-in filter drawer)

| Filter | Type | Options |
|---|---|---|
| Stream | Multi-select | MPC · BiPC · MEC · CEC · HEC · IIT Foundation · Integrated JEE · Integrated NEET |
| Class | Multi-select | Class 6–12 |
| Subject | Multi-select | Populated based on Stream + Class selection |
| Chapter | Multi-select | Populated based on Subject selection |
| Difficulty | Multi-select | 1 (Easy) · 2 · 3 · 4 · 5 (Hard) |
| Has Content | Toggle | Topics with at least 1 linked content resource |
| Has Questions | Toggle | Topics with at least 1 question bank entry |

Active filter chips: dismissible, "Clear All" link, count badge on filter button.

### 4.3 Tree View

Expand/collapse hierarchy: Stream → Class → Subject → Chapter → Topic → Subtopic.

Each node shows:
- **Stream node:** Icon, stream name, total subjects count
- **Class node:** Class label, subjects count
- **Subject node:** Subject name, chapter count, topic count, [+ Add Topic] button (edit roles only)
- **Chapter node:** Chapter name, topic count, sequence number
- **Topic node:** Topic name, difficulty badge, estimated hours, subtopic count, linked resources icon, linked questions icon, [Edit] icon (edit roles only)
- **Subtopic node:** Subtopic name, indented leaf node

Inline actions (edit roles):
- [+ Add Topic] next to Chapter nodes
- [Edit] pencil icon next to Topic nodes → opens `topic-edit` drawer

### 4.4 Table View (Flat Table)

| Column | Type | Sortable | Visible By | Notes |
|---|---|---|---|---|
| ☐ | Checkbox | — | Edit roles | Row select for bulk actions |
| Stream | Badge | ✅ | All | Stream name |
| Class | Text | ✅ | All | e.g. Class 11 |
| Subject | Text | ✅ | All | Subject name |
| Chapter | Text | ✅ | All | Chapter name |
| Topic | Text + link | ✅ | All | Opens topic-edit drawer (edit roles) or topic-view (view roles) |
| Subtopics | Number | ✅ | All | Count of subtopics |
| Sequence | Number | ✅ | All | Teaching order within chapter |
| Difficulty | Stars / Number | ✅ | All | 1–5 |
| Est. Hours | Number | ✅ | All | Estimated teaching hours |
| NCERT Ref | Text | ❌ | All | e.g. "Physics Part 1, Ch. 4" |
| Resources | Number + icon | ❌ | All | Linked content library items |
| Questions | Number + icon | ❌ | All | Linked question bank entries |
| Actions | — | ❌ | Edit roles | See Row Actions |

**Column visibility toggle:** Gear icon top-right — saves preference per user.

**Default sort:** Stream ascending, then Class ascending, then Sequence ascending.

**Pagination:** Server-side · Default 25/page · Selector 10/25/50/All · "Showing X–Y of Z topics" · Page jump input.

### 4.5 Row Actions (Table View)

| Action | Icon | Visible To | Drawer/Modal | Notes |
|---|---|---|---|---|
| Edit Topic | Pencil | CAO, Academic Dir, Curriculum Coord | `topic-edit` drawer 480px | Full topic edit |
| View | Eye | All | `topic-view` drawer 480px | Read-only topic detail |
| Archive | Archive box | CAO, Academic Dir | Confirm modal 420px | Archives topic — removes from all dropdowns |

### 4.6 Bulk Actions (Table View)

| Action | Visible To | Notes |
|---|---|---|
| Export Selected (XLSX) | All with export access | Full hierarchy for selected topics |
| Archive Selected | CAO, Academic Dir | Batch archive — requires reason |

---

## 5. Drawers & Modals

### 5.1 Drawer: `subject-create` — New Subject
- **Trigger:** [+ Add Subject] header button
- **Width:** 480px

| Field | Type | Required | Validation |
|---|---|---|---|
| Subject Name | Text | ✅ | Min 2 chars, max 100, unique within stream+class |
| Subject Code | Text | ✅ | Alphanumeric, max 10 chars, unique within stream+class |
| Stream | Select | ✅ | From stream list |
| Class | Select | ✅ | Class 6–12 (filtered by stream eligibility) |
| Board Mapping | Multi-select | ✅ | CBSE · BSEAP · BSETS · ICSE |
| Pass Marks (%) | Number | ✅ | 1–100 |
| Total Teaching Hours (term) | Number | ✅ | Min 10 |
| Language Medium | Select | ❌ | English · Telugu · Hindi · Tamil |

**Submit:** "Create Subject" — on success, opens empty topic list for this subject.

### 5.2 Drawer: `topic-create` — New Topic
- **Trigger:** [+ Add Topic] in tree view next to a chapter node, or inline in subject editor
- **Width:** 480px

| Field | Type | Required | Validation |
|---|---|---|---|
| Chapter Name | Text | ✅ | Select existing chapter or type new chapter name |
| Topic Name | Text | ✅ | Min 2 chars, max 150 |
| Subtopics | Tag input | ❌ | Add/remove rows — comma or Enter to add |
| Sequence No. | Number | ✅ | Teaching order within chapter — auto-increments |
| Difficulty | Select | ✅ | 1 (Easy) · 2 · 3 · 4 · 5 (Hard) |
| Estimated Hours to Teach | Number | ✅ | Min 0.5 |
| NCERT Reference | Text | ❌ | e.g. "Chemistry Part 2, Ch. 7, Pg. 142" |
| Linked Resources | Multi-select | ❌ | Content library items — search and select |

**Submit:** "Add Topic" — topic appears in tree/table immediately.

### 5.3 Drawer: `topic-edit` — Edit Topic
- **Trigger:** Edit icon in tree view, pencil row action in table, or Topic column link
- **Width:** 480px
- Same fields as `topic-create`, pre-filled
- Sequence No. change shows warning: "Changing sequence will reorder topics in all linked syllabi. Continue?"

### 5.4 Drawer: `topic-view` — View Topic (Read-only)
- **Trigger:** Topic name link in table view (for view-only roles)
- **Width:** 480px
- Displays: Topic name, chapter, subject, stream, class, difficulty, estimated hours, subtopics list, NCERT reference, linked content count, linked questions count.
- [View Content] button → filters Content Library to this topic.
- [View Questions] button → filters Question Bank to this topic.

### 5.5 Modal: CSV Import
- **Trigger:** [Import CSV ↑] header button
- **Width:** 560px
- **Step 1:** Download CSV template button (shows headers: Stream, Class, Subject, Chapter, Topic, Subtopics, Sequence, Difficulty, Hours, NCERT_Ref)
- **Step 2:** File upload input (.csv or .xlsx) · Max 5 MB
- **Step 3:** Validation report — table of errors per row (Row # · Column · Error · Current value)
- **Step 4:** If no errors: [Confirm Import] button — imports all rows
- **Step 5:** Success: "[N] topics added, [M] updated" toast. Error rows skipped; downloadable error report.

### 5.6 Modal: Archive Confirm
- **Width:** 420px
- **Content:** "Archive '[Topic Name]'? It will be removed from all syllabus dropdowns, content filters, and question bank selectors."
- **Warning:** Topics archived here may break existing content or question bank entries still linked to this topic.
- **Fields:** Reason (required, min 20 chars) · I understand the impact (checkbox, required)
- **Buttons:** [Confirm Archive] (danger) + [Cancel]

---

## 6. Charts

No standalone charts section — data is primarily navigated through tree/table. Gap indicators ("Topics Without Content", "Topics Without Questions") in the stats bar link to filtered table views for action.

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Subject created | "Subject '[Name]' created for [Stream] Class [X]." | Success | 4s |
| Topic added | "Topic '[Name]' added to [Chapter] — [Subject]." | Success | 4s |
| Topic updated | "Topic '[Name]' updated." | Success | 4s |
| Topic archived | "Topic '[Name]' archived." | Warning | 6s |
| CSV import success | "Import complete. [N] topics added, [M] updated." | Success | 4s |
| CSV import errors | "Import has [N] row errors. Review the error report before re-uploading." | Error | Manual |
| Export started | "Export preparing… download will start shortly." | Info | 4s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No subjects defined | "No subjects in master" | "Start by adding the first subject for a stream and class." | [+ Add Subject] |
| No results for search | "No topics match" | "Try different subject, chapter, or topic keywords." | [Clear Search] |
| Filter returns empty | "No topics match your filters" | "Try removing some filters." | [Clear All Filters] |
| Stream selected — no subjects | "No subjects defined for [Stream]" | "Add the first subject for this stream." | [+ Add Subject] |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load (tree view) | Skeleton: stats bar + tree skeleton (collapsed top-level nodes) |
| Page initial load (table view) | Skeleton: stats bar + table (10 skeleton rows) |
| Tree node expand | Spinner in node row |
| Table filter/search/sort/page | Inline skeleton rows (10) |
| subject-create drawer open | Spinner in drawer body |
| topic-create/edit drawer open | Spinner in drawer body |
| CSV import validation | Progress bar in import modal |
| Topic archive confirm | Spinner in confirm button |
| Export trigger | Spinner in export button (momentary) |

---

## 10. Role-Based UI Visibility

| Element | CAO G4 | Academic Dir G3 | Curriculum Coord G2 | Exam Controller G3 | Stream Coords G3 |
|---|---|---|---|---|---|
| [+ Add Subject] button | ✅ | ✅ | ✅ | ❌ | ❌ |
| [Import CSV] button | ✅ | ✅ | ✅ | ❌ | ❌ |
| [Export XLSX] button | ✅ | ✅ | ✅ | ✅ | ✅ |
| [+ Add Topic] (tree) | ✅ | ✅ | ✅ | ❌ | ❌ |
| Edit icon (tree/table) | ✅ | ✅ | ✅ | ❌ | ❌ |
| Archive row action | ✅ | ✅ | ❌ | ❌ | ❌ |
| Bulk archive | ✅ | ✅ | ❌ | ❌ | ❌ |
| Stream filter (all streams) | ✅ | ✅ | ✅ | ✅ | ❌ (own only) |
| Resources column | ✅ | ✅ | ✅ | ✅ | ✅ |
| Questions column | ✅ | ✅ | ✅ | ✅ | ✅ (own stream) |
| Topics Without Content (stats) | ✅ | ✅ | ✅ | ❌ | ❌ |
| Topics Without Questions (stats) | ✅ | ✅ | ❌ | ✅ | ❌ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/acad/subject-topic/` | JWT | Flat list of topics (filtered/sorted/paginated) |
| GET | `/api/v1/group/{group_id}/acad/subject-topic/tree/` | JWT | Full hierarchy tree (stream → subtopic) |
| POST | `/api/v1/group/{group_id}/acad/subject-topic/subjects/` | JWT (CAO/Dir/Coord) | Create subject |
| PUT | `/api/v1/group/{group_id}/acad/subject-topic/subjects/{sub_id}/` | JWT (CAO/Dir/Coord) | Update subject |
| DELETE | `/api/v1/group/{group_id}/acad/subject-topic/subjects/{sub_id}/` | JWT (CAO/Dir) | Archive subject (soft) |
| POST | `/api/v1/group/{group_id}/acad/subject-topic/topics/` | JWT (CAO/Dir/Coord) | Create topic |
| PUT | `/api/v1/group/{group_id}/acad/subject-topic/topics/{topic_id}/` | JWT (CAO/Dir/Coord) | Update topic |
| DELETE | `/api/v1/group/{group_id}/acad/subject-topic/topics/{topic_id}/` | JWT (CAO/Dir) | Archive topic (soft) |
| POST | `/api/v1/group/{group_id}/acad/subject-topic/import/` | JWT (CAO/Dir/Coord) | CSV/XLSX bulk import |
| GET | `/api/v1/group/{group_id}/acad/subject-topic/export/` | JWT | XLSX full hierarchy export |
| GET | `/api/v1/group/{group_id}/acad/subject-topic/stats/` | JWT | Summary stats bar data |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Topic search (table) | `input delay:300ms` | GET `.../subject-topic/?q=` | `#topic-table-body` | `innerHTML` |
| Topic search (tree) | `input delay:300ms` | GET `.../subject-topic/tree/?q=` | `#topic-tree` | `innerHTML` |
| Filter apply | `click` | GET `.../subject-topic/?filters=` | `#topic-table-section` | `innerHTML` |
| Sort column | `click` | GET `.../subject-topic/?sort=&dir=` | `#topic-table-section` | `innerHTML` |
| Pagination | `click` | GET `.../subject-topic/?page=` | `#topic-table-section` | `innerHTML` |
| Tree node expand | `click` | GET `.../subject-topic/tree/{node_id}/children/` | `#tree-node-{node_id}` | `innerHTML` |
| Create subject drawer | `click` | GET `.../subject-topic/subject-form/` | `#drawer-body` | `innerHTML` |
| Create topic drawer | `click` | GET `.../subject-topic/topic-form/?subject={id}` | `#drawer-body` | `innerHTML` |
| Create submit | `submit` | POST `.../subject-topic/topics/` | `#drawer-body` | `innerHTML` |
| Archive confirm | `click` | DELETE `.../subject-topic/topics/{id}/` | `#topic-row-{id}` | `outerHTML` |
| Stats bar refresh | `load` | GET `.../subject-topic/stats/` | `#stats-bar` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
