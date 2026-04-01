# 24 — Exam Paper Builder

> **URL:** `/group/acad/exam-papers/`
> **File:** `24-exam-paper-builder.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** CAO G4 · Exam Controller G3 · Stream Coords G3

---

## 1. Purpose

The Exam Paper Builder is where all formal examination papers for the group are constructed, reviewed, version-controlled, and approved. It operates in two modes: the papers list view (the default landing), and the full-page builder interface that opens when constructing or editing a specific paper. The builder is the most feature-rich interface in Division B — it functions like a document editor purpose-built for exam papers.

In builder mode, the screen splits into two panels: the left panel is a live-query browser of the Question Bank, with all filtering capabilities (stream, subject, topic, difficulty, Bloom level, type); the right panel is the paper structure editor, where the Exam Controller assembles questions into sections (Section A, B, C), sets marks per question, enables or disables shuffling, and monitors the paper's difficulty balance in real time through the auto-updating donut chart. Every save creates a new version, and any two versions can be diffed to see exactly which questions changed between saves.

Papers undergo a formal approval flow: Draft → Submitted for Approval → Approved → Published. The Exam Controller builds and submits; the CAO approves. Once approved, a paper can be published to branches along with its exam schedule entry. The builder also links to the Answer Keys page — once a paper is published, the Exam Controller can upload the answer key from the same paper record.

---

## 2. Role Access

| Role | Level | Can View List | Can Create | Can Build/Edit | Can Submit | Can Approve | Can Publish | Notes |
|---|---|---|---|---|---|---|---|---|
| Chief Academic Officer (CAO) | G4 | ✅ All | ✅ | ✅ | ✅ | ✅ | ✅ | Approve + override |
| Group Academic Director | G3 | ✅ All | ❌ | ❌ | ❌ | ❌ | ❌ | View-only |
| Group Curriculum Coordinator | G2 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | No access |
| Group Exam Controller | G3 | ✅ All | ✅ | ✅ | ✅ | ❌ | ✅ | Build + submit; cannot self-approve |
| Group Results Coordinator | G3 | ✅ All | ❌ | ❌ | ❌ | ❌ | ❌ | View approved papers only |
| Stream Coord — MPC | G3 | ✅ MPC | ✅ (MPC) | ✅ Draft (MPC) | ✅ (to Exam Ctrl) | ❌ | ❌ | Create draft for own stream; submit to Exam Controller |
| Stream Coord — BiPC | G3 | ✅ BiPC | ✅ (BiPC) | ✅ Draft (BiPC) | ✅ (to Exam Ctrl) | ❌ | ❌ | Same as MPC Coord |
| Stream Coord — MEC/CEC | G3 | ✅ MEC/CEC | ✅ (MEC/CEC) | ✅ Draft (MEC/CEC) | ✅ (to Exam Ctrl) | ❌ | ❌ | Same as MPC Coord |
| JEE/NEET Integration Head | G3 | ✅ JEE/NEET | ✅ | ✅ Draft | ✅ | ❌ | ❌ | JEE/NEET coaching papers |
| IIT Foundation Director | G3 | ✅ Foundation | ✅ | ✅ Draft | ✅ | ❌ | ❌ | Foundation papers |
| Olympiad & Scholarship Coord | G3 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | No access |
| Special Education Coordinator | G3 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | No access |
| Academic MIS Officer | G1 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | No access |
| Academic Calendar Manager | G3 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | No access |

---

## 3. Page Layout — Papers List View (Default Landing)

### 3.1 Breadcrumb
```
Group HQ  ›  Academic  ›  Exam Paper Builder
```

### 3.2 Page Header (with action buttons — role-gated)
```
Exam Paper Builder                        [+ New Paper]  [Export XLSX ↓]
[Group Name] · Version-controlled exam papers             (CAO / Exam Controller / Stream Coords)
```

Action button visibility:
- `[+ New Paper]` — CAO, Exam Controller, Stream Coords (own stream), JEE/NEET Head, Foundation Dir
- `[Export XLSX ↓]` — CAO, Exam Controller, Academic Director

### 3.3 Summary Stats Bar
| Stat | Value |
|---|---|
| Total Papers | Count across all statuses |
| Draft | Papers in progress |
| Pending Approval | Submitted, awaiting CAO review |
| Approved | Ready to use in exams |
| Published | Distributed to branches |
| Archived | Retired papers |

Stats bar refreshes on page load.

---

## 4. Main Papers List Table

### 4.1 Search
- Full-text across: Paper Name, Exam Name, Subject
- 300ms debounce · Highlights match in Paper ID / Name column

### 4.2 Advanced Filters (slide-in filter drawer)

| Filter | Type | Options |
|---|---|---|
| Exam Name | Search input | Link to Group Exam Calendar |
| Stream | Multi-select | MPC · BiPC · MEC · CEC · HEC · Foundation · Integrated JEE · NEET |
| Class | Multi-select | Class 6–12 |
| Status | Multi-select | Draft · Pending Approval · Approved · Published · Archived |
| Date Created | Date range | From / To |
| Created By | Search input | Filter by creator name |

Active filter chips: dismissible, "Clear All" link, count badge on filter button.

### 4.3 Columns

| Column | Type | Sortable | Visible By | Notes |
|---|---|---|---|---|
| ☐ | Checkbox | — | CAO, Exam Controller | Row select for bulk export |
| Paper ID | Text | ✅ | All | Auto-generated e.g. PAP-2025-0142 |
| Exam Name | Text + link | ✅ | All | Linked exam from calendar |
| Stream | Badge | ✅ | All | Stream |
| Class | Text | ✅ | All | e.g. Class 12 |
| Subject | Text | ✅ | All | Subject(s) covered |
| Total Q | Number | ✅ | All | Total questions in paper |
| Total Marks | Number | ✅ | All | Total marks |
| Duration | Text | ✅ | All | Exam duration e.g. 3h 00m |
| Status | Badge | ✅ | All | Draft · Pending · Approved · Published · Archived |
| Created By | Text | ✅ | CAO, Exam Controller | Creator name + role |
| Created At | Date | ✅ | All | Creation timestamp |
| Version | Number | ❌ | CAO, Exam Controller | Current version number |
| Actions | — | ❌ | Role-based | See Row Actions |

**Default sort:** Status (Draft and Pending first), then Created At descending.

**Pagination:** Server-side · Default 25/page · Selector 10/25/50/All.

### 4.4 Row Actions (Papers List)

| Action | Icon | Visible To | Target | Notes |
|---|---|---|---|---|
| Open Builder | Edit | CAO, Exam Controller, Creator | Full-page builder | Opens full-page builder for this paper |
| View Preview | Eye | All with access | `paper-view` drawer 640px | Read-only paper preview |
| Submit for Approval | Checkmark | Exam Controller, Stream Coords | `submit-for-approval` modal | Sends to CAO approval queue |
| Approve | Thumb up | CAO | Inline confirm | Approves paper |
| Publish Answer Key | Key | CAO, Exam Controller | Navigates to Answer Keys (page 28) | |
| Archive | Archive box | CAO, Exam Controller | Confirm modal 420px | Soft archive |
| Clone | Copy | CAO, Exam Controller, Creator | `new-paper` form with data pre-filled | Clone for another exam/year |

### 4.5 Bulk Actions

| Action | Visible To | Notes |
|---|---|---|
| Export Selected (XLSX) | CAO, Exam Controller | Paper metadata export |

---

## 5. Full-Page Builder Interface

Accessed by clicking "Open Builder" from the papers list. Replaces the standard page layout with a dedicated two-panel builder. The breadcrumb persists at top for navigation back.

### 5.1 Builder Header
```
[← Back to Paper List]  [Paper Name — editable inline]  [Exam: {Exam Name}]  [Version: v{N}]
                         [Save Draft]  [Preview]  [Submit for Approval]  [Auto-save indicator]
```

Auto-save: saves every 60 seconds if changes detected. Auto-save indicator: "Saved 30s ago" · "Saving…" · "Unsaved changes".

### 5.2 Left Panel — Question Bank Browser (380px width, fixed)

**Header:** "Question Bank" + [Collapse ←] toggle

**Filters (within left panel):**
- Stream selector (pre-filled from paper stream)
- Class selector (pre-filled)
- Subject selector
- Topic selector (dependent on subject)
- Type: All / MCQ / Short / Long / Numerical / Assertion-Reason
- Difficulty: All / 1–5 slider
- Bloom Level: multi-select chips
- Search: question text partial match (300ms debounce)

**Question list:** Compact cards — Q#, truncated question text (50 chars), type badge, difficulty stars, marks.

Each card:
- [+] button (adds question to active section in right panel)
- Hover: tooltip with full question text + correct answer preview

**Bottom of left panel:** "Showing [N] questions matching your filters" · pagination (10/page within left panel)

### 5.3 Right Panel — Paper Structure Editor

**Sections management:**
- Default sections: Section A (MCQ), Section B (Short Answer), Section C (Long Answer)
- [+ Add Section] button — custom section name, description, marks per question default
- Drag to reorder sections
- [Delete Section] per section (moves questions to unassigned)

**Per section:**
```
Section A — Multiple Choice Questions
[Instructions for this section — editable text field]
Marks per question: [4 ▼]  |  Negative marks: [1 ▼]  |  Shuffle questions: [ON/OFF]

Questions in this section:
┌─────────────────────────────────────────────────────────────┐
│ ≡  Q#142  Physics — Thermodynamics   [MCQ] [Diff: ●●●○○]  [×]│
│    "A gas undergoes an isothermal process..." (truncated)    │
│    Marks: 4  |  Negative: 1                                  │
├─────────────────────────────────────────────────────────────┤
│ ≡  Q#301  Chemistry — Equilibrium    [MCQ] [Diff: ●●○○○]  [×]│
│    "At equilibrium, the rate of forward..."                  │
│    Marks: 4  |  Negative: 1                                  │
└─────────────────────────────────────────────────────────────┘
[Drag questions here from the left panel or use + buttons]
```

- Drag handle (≡) to reorder questions within section
- [×] to remove question from paper (returns to bank — not deleted)
- Marks per question editable per row (override section default)
- Question count badge per section

**Paper summary footer (sticky at bottom of right panel):**
```
Total Questions: 90  |  Total Marks: 360  |  Duration: 3h 00m
Section A: 60Q × 4M = 240  |  Section B: 20Q × 4M = 80  |  Section C: 10Q × 4M = 40
```

**Real-time difficulty donut:** Live donut chart beside summary showing distribution of Easy/Medium/Hard questions as they are added. Target balance indicator (configurable per exam type).

**Real-time Bloom radar:** Radar chart showing coverage across 6 Bloom levels. Updates as questions are added.

### 5.4 Paper Configuration Panel (right side bar, toggleable)
Accessible via [⚙] gear icon. Slides in at 300px width over right panel.

| Field | Type | Required | Notes |
|---|---|---|---|
| Paper Title | Text | ✅ | Editable inline in header too |
| Total Duration | Number (minutes) | ✅ | Default from linked exam schedule |
| Total Marks | Computed (read-only) | — | Auto-calculated from question marks |
| Instructions (general) | Rich text | ❌ | Printed at top of paper |
| Paper Code | Text | ❌ | e.g. "SET A" for multiple sets |
| Is Bilingual | Toggle | ❌ | English + Telugu parallel text |
| Shuffle All Questions | Toggle | ❌ | Paper-level shuffle for multiple sets |
| Watermark | Text | ❌ | e.g. "CONFIDENTIAL — DO NOT CIRCULATE" |

### 5.5 Version History (accessible from builder header)
- Sidebar panel: list of versions — v1, v2, v3… with timestamp, editor, and change summary
- [Compare] button between any two versions: diff view shows questions added/removed/reordered in highlighted colour
- [Restore] button on any version: restores that version as a new version (non-destructive)

---

## 6. Drawers & Modals (Papers List View)

### 6.1 Drawer: `paper-view` — View Paper Preview
- **Trigger:** View Preview row action
- **Width:** 640px
- **Tabs:** Paper Preview (Student View) · Structure Summary · Approval History

#### Tab: Paper Preview (Student View)
Renders the paper exactly as it will be printed and distributed — all questions formatted, KaTeX rendered, options listed, marks shown, instructions displayed. Scroll-through read-only document view.

#### Tab: Structure Summary
Table: Section · Questions · Marks · Difficulty Breakdown · Bloom Coverage.

#### Tab: Approval History
Table: Version · Action · Actor · Timestamp · Notes. Shows full create → submit → approve → publish trail.

### 6.2 Modal: `submit-for-approval`
- **Trigger:** Submit for Approval row action
- **Width:** 420px
- **Content:** "Submit '[Paper Name]' for CAO approval?"
- **Checklist (auto-checked):**
  - [ ] Answer key attached?
  - [ ] Total marks match exam schedule?
  - [ ] Duration set?
  - [ ] All sections have at least 1 question?
- Items not passing checklist: shown as amber warnings with [Fix] link
- **Fields:** Notes to reviewer (optional textarea)
- **Buttons:** [Submit for Approval] (primary — enabled even with amber warnings but not if checklist errors exist) + [Cancel]

### 6.3 Modal: `publish-confirm`
- **Trigger:** Publish action (only available after Approved status)
- **Width:** 420px
- **Content:** "Publish '[Paper Name]' to [N] branches? Branches will receive this paper immediately."
- **Warning:** "Ensure the exam date has not passed. Published papers cannot be edited."
- **Buttons:** [Publish to Branches] (primary green) + [Cancel]
- **On confirm:** Paper status → Published · All branch exam coordinators notified · Audit entry created

### 6.4 Modal: Archive Confirm
- **Width:** 420px
- **Content:** "Archive '[Paper Name]'? This paper will not be available for future exams but version history is retained."
- **Fields:** Reason (required, min 10 chars)
- **Buttons:** [Confirm Archive] (danger) + [Cancel]

---

## 7. Charts (Embedded in Builder — Right Panel)

### 7.1 Difficulty Distribution Donut (Real-time)
- Updates live as questions are added/removed
- Segments: Easy (1–2) · Medium (3) · Hard (4–5)
- Target bands shown as arc overlay (configurable: e.g. 30% Easy / 50% Medium / 20% Hard)
- **Tooltip:** Segment · Count · % · Target %

### 7.2 Bloom Level Coverage Radar (Real-time)
- 6-axis radar: Remember · Understand · Apply · Analyse · Evaluate · Create
- Area fills as questions at each level are added
- Target minimum coverage overlay (e.g. all levels ≥ 10%)
- **Tooltip:** Level · Count · %

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Paper created | "'[Paper Name]' created. Open builder to add questions." | Success | 4s |
| Auto-saved | "Draft auto-saved." | Info | 2s |
| Paper submitted | "'[Paper Name]' submitted for CAO approval." | Success | 4s |
| Paper approved | "'[Paper Name]' approved." | Success | 4s |
| Paper published | "'[Paper Name]' published to [N] branches." | Success | 4s |
| Paper cloned | "'[Paper Name]' cloned. Review and save the new paper." | Info | 4s |
| Paper archived | "'[Paper Name]' archived." | Warning | 6s |
| Question added | "Q#[N] added to [Section]." | Info | 2s |
| Question removed | "Q#[N] removed from paper." | Info | 2s |
| Version restored | "Paper restored to v[N]. Saved as v[M]." | Info | 4s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No papers created | "No exam papers yet" | "Create the first paper to start building exam content." | [+ New Paper] |
| Filter returns empty | "No papers match your filters" | "Try removing some filters." | [Clear All Filters] |
| Left panel — no questions | "No questions match your filters" | "Adjust the stream, subject, or topic filters to find questions." | [Clear Filters] |
| Right panel — no questions | "Add questions from the left panel" | "Use the + button on any question card to add it to this section." | — |
| No versions in history | "No version history yet" | "Version history starts after the first save." | — |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Papers list initial load | Skeleton: stats bar + table (10 skeleton rows) |
| Table filter/search/sort/page | Inline skeleton rows (10) |
| Builder open (full-page) | Full page transition spinner → builder renders |
| Left panel question filter | Inline spinner in left panel question list |
| Paper save (auto or manual) | Spinner in Save button · auto-save shows text indicator |
| paper-view drawer open | Spinner + skeleton tabs |
| Submit for approval confirm | Spinner in submit button |
| Publish confirm | Spinner in publish button |
| Charts (donut + radar in builder) | Skeleton circles while first batch loads; then live update |
| Export trigger | Spinner in export button (momentary) |

---

## 11. Role-Based UI Visibility

| Element | CAO G4 | Exam Controller G3 | Stream Coords G3 | Academic Dir G3 | Results Coord G3 |
|---|---|---|---|---|---|
| [+ New Paper] button | ✅ | ✅ | ✅ (own stream) | ❌ | ❌ |
| Open Builder action | ✅ | ✅ | ✅ (own draft only) | ❌ | ❌ |
| Submit for Approval | ✅ | ✅ | ✅ | ❌ | ❌ |
| Approve action | ✅ | ❌ | ❌ | ❌ | ❌ |
| Publish action | ✅ | ✅ (after approval) | ❌ | ❌ | ❌ |
| Publish Answer Key action | ✅ | ✅ | ❌ | ❌ | ❌ |
| Clone action | ✅ | ✅ | ✅ (own) | ❌ | ❌ |
| Archive action | ✅ | ✅ | ❌ | ❌ | ❌ |
| Version history view | ✅ | ✅ | ✅ (own) | ✅ | ❌ |
| Version restore | ✅ | ✅ | ❌ | ❌ | ❌ |
| Created By column | ✅ | ✅ | ❌ | ✅ | ❌ |
| Version column | ✅ | ✅ | ❌ | ❌ | ❌ |
| Approval History tab | ✅ | ✅ | ✅ | ✅ | ❌ |
| Stream filter (all streams) | ✅ | ✅ | ❌ (own only) | ✅ | ✅ |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/acad/exam-papers/` | JWT | List papers (filtered/sorted/paginated) |
| POST | `/api/v1/group/{group_id}/acad/exam-papers/` | JWT (create roles) | Create new paper |
| GET | `/api/v1/group/{group_id}/acad/exam-papers/{paper_id}/` | JWT | Paper detail |
| PUT | `/api/v1/group/{group_id}/acad/exam-papers/{paper_id}/` | JWT (edit roles) | Update paper (save draft) |
| POST | `/api/v1/group/{group_id}/acad/exam-papers/{paper_id}/submit/` | JWT (Exam Ctrl/Stream Coords) | Submit for approval |
| POST | `/api/v1/group/{group_id}/acad/exam-papers/{paper_id}/approve/` | JWT (CAO) | Approve paper |
| POST | `/api/v1/group/{group_id}/acad/exam-papers/{paper_id}/publish/` | JWT (CAO/Exam Ctrl) | Publish to branches |
| POST | `/api/v1/group/{group_id}/acad/exam-papers/{paper_id}/archive/` | JWT (CAO/Exam Ctrl) | Archive paper |
| POST | `/api/v1/group/{group_id}/acad/exam-papers/{paper_id}/clone/` | JWT (create roles) | Clone paper |
| GET | `/api/v1/group/{group_id}/acad/exam-papers/{paper_id}/versions/` | JWT (CAO/Exam Ctrl) | Version history list |
| POST | `/api/v1/group/{group_id}/acad/exam-papers/{paper_id}/restore/{version}/` | JWT (CAO/Exam Ctrl) | Restore version |
| GET | `/api/v1/group/{group_id}/acad/exam-papers/{paper_id}/preview/` | JWT | Rendered paper preview |
| GET | `/api/v1/group/{group_id}/acad/exam-papers/stats/` | JWT | Summary stats bar data |
| GET | `/api/v1/group/{group_id}/acad/exam-papers/export/` | JWT | XLSX export |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Paper search (list) | `input delay:300ms` | GET `.../exam-papers/?q=` | `#papers-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../exam-papers/?filters=` | `#papers-table-section` | `innerHTML` |
| Sort column | `click` | GET `.../exam-papers/?sort=&dir=` | `#papers-table-section` | `innerHTML` |
| Pagination | `click` | GET `.../exam-papers/?page=` | `#papers-table-section` | `innerHTML` |
| View preview drawer | `click` | GET `.../exam-papers/{id}/preview/` | `#drawer-body` | `innerHTML` |
| Left panel question filter | `change / input delay:300ms` | GET `.../question-bank/?stream=&subject=&q=` | `#qb-left-panel-list` | `innerHTML` |
| Add question to section | `click` | POST `.../exam-papers/{id}/questions/` | `#section-{s_id}-questions` | `beforeend` |
| Remove question | `click` | DELETE `.../exam-papers/{id}/questions/{q_id}/` | `#paper-q-row-{q_id}` | `outerHTML` |
| Reorder (drag drop) | `htmx:afterRequest` (custom event) | PUT `.../exam-papers/{id}/reorder/` | `#paper-summary` | `innerHTML` |
| Auto-save | `every 60s` | PUT `.../exam-papers/{id}/` | `#autosave-indicator` | `innerHTML` |
| Stats bar refresh | `load` | GET `.../exam-papers/stats/` | `#stats-bar` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
