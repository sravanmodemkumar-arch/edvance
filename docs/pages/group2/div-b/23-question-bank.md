# 23 — Question Bank

> **URL:** `/group/acad/question-bank/`
> **File:** `23-question-bank.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** CAO G4 · Exam Controller G3 · Stream Coords G3 · Curriculum Coordinator G2

---

## 1. Purpose

The Question Bank is the group's centrally managed repository of all examination questions — spanning MCQs, short-answer, long-answer, and numerical types — covering every stream, class, subject, and topic in the group. At scale, this bank holds 10,000–50,000 questions across streams like MPC, BiPC, MEC/CEC, IIT Foundation, and Integrated JEE/NEET. It is the source from which every exam paper in the group is constructed.

Questions involving mathematics, physics, or chemistry formulae are rendered using KaTeX — the fast, lightweight LaTeX rendering library. When a question is written using LaTeX syntax (e.g. `$\frac{d^2y}{dx^2} + k^2y = 0$`), the system renders it beautifully both in the bank interface and in the exam paper builder, ensuring that physics and maths questions display exactly as students will see them in print. The Preview drawer renders KaTeX identically to the final paper output.

The bank is designed for high-frequency querying by the Exam Paper Builder — when a paper is being constructed, the Builder's left panel queries this bank in real time, filtering by subject, topic, difficulty, Bloom level, and question type. The question status lifecycle (Active → Review → Retired) ensures that flagged or outdated questions are not accidentally included in new papers, while the Retired status preserves historical question data for analysis.

---

## 2. Role Access

| Role | Level | Can View | Can Create | Can Edit | Can Retire | Notes |
|---|---|---|---|---|---|---|
| Chief Academic Officer (CAO) | G4 | ✅ All | ✅ | ✅ | ✅ | Full authority |
| Group Academic Director | G3 | ✅ All | ❌ | ❌ | ❌ | View-only |
| Group Curriculum Coordinator | G2 | ✅ All | ✅ | ✅ Own | ❌ | Create and edit own questions; cannot retire others |
| Group Exam Controller | G3 | ✅ All | ✅ | ✅ | ✅ | Operational ownership of question bank |
| Group Results Coordinator | G3 | ✅ All | ❌ | ❌ | ❌ | View-only |
| Stream Coord — MPC | G3 | ✅ MPC | ✅ (MPC) | ✅ Own (MPC) | ❌ | Create/edit for own stream only |
| Stream Coord — BiPC | G3 | ✅ BiPC | ✅ (BiPC) | ✅ Own (BiPC) | ❌ | Create/edit for own stream only |
| Stream Coord — MEC/CEC | G3 | ✅ MEC/CEC | ✅ (MEC/CEC) | ✅ Own (MEC/CEC) | ❌ | Create/edit for own stream only |
| JEE/NEET Integration Head | G3 | ✅ MPC+BiPC | ✅ (JEE/NEET) | ✅ Own | ❌ | Create coaching-specific questions |
| IIT Foundation Director | G3 | ✅ Foundation | ✅ (Foundation) | ✅ Own | ❌ | Create Foundation questions |
| Olympiad & Scholarship Coord | G3 | ✅ All | ✅ | ✅ Own | ❌ | Create olympiad prep questions |
| Special Education Coordinator | G3 | ❌ | ❌ | ❌ | ❌ | No access |
| Academic MIS Officer | G1 | ❌ | ❌ | ❌ | ❌ | No access |
| Academic Calendar Manager | G3 | ❌ | ❌ | ❌ | ❌ | No access |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Academic  ›  Question Bank
```

### 3.2 Page Header (with action buttons — role-gated)
```
Question Bank                             [+ New Question]  [Import XLSX ↑]  [Export XLSX ↓]
[Group Name] · [Total count] questions across all streams   (CAO / Exam Controller / Stream Coords for create)
```

Action button visibility:
- `[+ New Question]` — CAO, Exam Controller, Curriculum Coordinator, Stream Coords (own stream), JEE/NEET Head, Foundation Dir, Olympiad Coord
- `[Import XLSX ↑]` — CAO, Exam Controller, Curriculum Coordinator
- `[Export XLSX ↓]` — CAO, Exam Controller, Academic Director

### 3.3 Summary Stats Bar
| Stat | Value |
|---|---|
| Total Questions | Count of Active + Review questions |
| MCQ | Count |
| Short Answer | Count |
| Long Answer | Count |
| Numerical | Count |
| Added This Month | Count |
| Flagged for Review | Count (links to filtered view) |

Stats bar refreshes on page load.

---

## 4. Main Question Bank Table

### 4.1 Search
- Full-text across: Question text (partial match), Topic name, Subject name
- 300ms debounce · Highlights match in question preview column
- KaTeX expressions are searched by their LaTeX source text, not rendered form
- Scope: Active + Review status by default

### 4.2 Advanced Filters (slide-in filter drawer)

| Filter | Type | Options |
|---|---|---|
| Subject | Multi-select | All subjects from Subject-Topic Master |
| Topic | Multi-select | Populated based on Subject selection |
| Subtopic | Multi-select | Populated based on Topic selection |
| Stream | Multi-select | MPC · BiPC · MEC · CEC · HEC · Foundation · Integrated JEE · Integrated NEET |
| Class | Multi-select | Class 6–12 |
| Question Type | Multi-select | MCQ · Short Answer · Long Answer · Numerical · Assertion-Reason |
| Difficulty | Multi-select | 1 (Easy) · 2 · 3 · 4 · 5 (Hard) |
| Bloom Level | Multi-select | Remember · Understand · Apply · Analyse · Evaluate · Create |
| Status | Multi-select | Active · Review · Retired |
| Last Used | Date range | Last used in a paper — From / To |
| Has LaTeX | Toggle | Questions containing LaTeX/KaTeX expressions only |
| Never Used | Checkbox | Questions not yet included in any paper |

Active filter chips: dismissible, "Clear All" link, count badge on filter button.

### 4.3 Columns

| Column | Type | Sortable | Visible By | Notes |
|---|---|---|---|---|
| ☐ | Checkbox | — | Edit roles | Row select for bulk actions |
| Q# | Number | ✅ | All | Auto-assigned sequential ID |
| Question Preview | Text (truncated) | ❌ | All | First 100 chars — KaTeX rendered inline. Full text on hover tooltip |
| Subject | Text | ✅ | All | Subject name |
| Topic | Text | ✅ | All | Topic name |
| Subtopic | Text | ❌ | All | Subtopic if applicable |
| Type | Badge | ✅ | All | MCQ · Short · Long · Numerical · A-R |
| Difficulty | Stars | ✅ | All | 1–5 |
| Bloom Level | Badge | ✅ | All | Remember / Understand / Apply etc. |
| Last Used | Date | ✅ | CAO, Exam Controller | Last paper this question appeared in |
| Status | Badge | ✅ | All | Active (green) · Review (amber) · Retired (grey) |
| Actions | — | ❌ | Role-based | See Row Actions |

**Column visibility toggle:** Gear icon top-right — saves preference per user.

**Default sort:** Status (Active first), then Q# ascending.

**Pagination:** Server-side · Default 25/page · Selector 10/25/50/All · "Showing X–Y of Z questions" · Page jump input.

### 4.4 Row Actions

| Action | Icon | Visible To | Drawer/Modal | Notes |
|---|---|---|---|---|
| Preview | Eye | All | `question-preview` drawer 480px | Full rendered question — KaTeX active |
| Edit | Pencil | CAO, Exam Controller, Curriculum Coord, Stream Coords (own) | `question-edit` drawer 680px | |
| Clone | Copy | CAO, Exam Controller, Stream Coords | `question-create` drawer 680px (pre-filled) | Creates a copy for modification |
| Retire | Archive | CAO, Exam Controller | Confirm modal 420px | Sets status to Retired; audited |
| Add to Paper | Plus | CAO, Exam Controller | Paper selector popover | Select open paper to add this question |

### 4.5 Bulk Actions

| Action | Visible To | Notes |
|---|---|---|
| Retire Selected | CAO, Exam Controller | Batch retire — requires reason |
| Move to Subject | CAO, Exam Controller | Reassign selected questions to a different subject |
| Tag Selected | CAO, Exam Controller, Curriculum Coord | Add tags to selected questions |
| Export Selected (XLSX) | CAO, Exam Controller | Exports question text, options, answer, metadata |

---

## 5. Drawers & Modals

### 5.1 Drawer: `question-create` — New Question
- **Trigger:** [+ New Question] header button
- **Width:** 680px
- **Tabs:** Question Text · Options · Explanation · Classification · Tags

#### Tab: Question Text
| Field | Type | Required | Validation |
|---|---|---|---|
| Question Type | Select | ✅ | MCQ · Short Answer · Long Answer · Numerical · Assertion-Reason |
| Question Text | Rich text editor + LaTeX | ✅ | Min 10 chars |
| — LaTeX support | KaTeX toggle | — | Toggle "Math Mode" to switch to LaTeX input. Preview renders KaTeX in real time beside input. Inline LaTeX: `$formula$`. Display LaTeX: `$$formula$$` |
| Image Attachment | File upload | ❌ | PNG/JPG, max 2 MB. Renders inline in question |
| Marks | Number | ✅ | 0.5–20 |
| Negative Marks | Number | ❌ | 0–5. Used in MCQ for competitive exam scoring |

**KaTeX rendering preview:** Live preview panel to the right of the editor updates as user types. Renders full KaTeX including fractions, integrals, chemical formulae, Greek letters, matrices, and bracket notation. No server round-trip — all client-side.

#### Tab: Options (MCQ / Assertion-Reason only)
| Field | Type | Required | Notes |
|---|---|---|---|
| Option A | Rich text + LaTeX | ✅ | KaTeX supported |
| Option B | Rich text + LaTeX | ✅ | KaTeX supported |
| Option C | Rich text + LaTeX | ✅ | KaTeX supported |
| Option D | Rich text + LaTeX | ✅ | KaTeX supported |
| Correct Answer | Radio select | ✅ | Select A / B / C / D (MCQ) or select assertion/reason status (A-R) |
| Option Image | File upload | ❌ per option | For diagram-based options |

For Numerical type: Correct Answer field is a number input with tolerance range (±value).
For Short/Long Answer: Tab is hidden; no options required.

#### Tab: Explanation
| Field | Type | Required | Notes |
|---|---|---|---|
| Solution / Explanation | Rich text + LaTeX | ❌ | Full worked solution. KaTeX supported. Shown to students after exam result release. |
| Difficulty Rationale | Textarea | ❌ | Why this question is rated at chosen difficulty level |
| Common Mistakes | Textarea | ❌ | Typical wrong approaches — used for branch teacher guidance |

#### Tab: Classification
| Field | Type | Required | Validation |
|---|---|---|---|
| Stream | Multi-select | ✅ | At least 1 stream |
| Class | Select | ✅ | Class 6–12 |
| Subject | Select | ✅ | From Subject-Topic Master |
| Topic | Select | ✅ | Filtered by Subject |
| Subtopic | Select | ❌ | Filtered by Topic |
| Difficulty | Select | ✅ | 1 (Easy) · 2 · 3 · 4 · 5 (Hard) |
| Bloom Level | Select | ✅ | Remember · Understand · Apply · Analyse · Evaluate · Create |
| Board | Multi-select | ❌ | CBSE · BSEAP · BSETS — for board-specific papers |

#### Tab: Tags
| Field | Type | Required | Notes |
|---|---|---|---|
| Tags | Tag input | ❌ | Freeform comma-separated keywords e.g. "thermodynamics, conceptual, JEE-level" |
| Source | Text | ❌ | e.g. "NCERT Exemplar", "Previous Year JEE 2023", "Internal" |

**Submit:** "Save Question" — validates all required fields. Question assigned next sequential Q# and set to Active status.

### 5.2 Drawer: `question-edit` — Edit Question
- **Width:** 680px — same tabs as `question-create`, pre-filled
- Edit history logged automatically — each save creates a version entry
- Warning shown if question is currently included in a Draft or Approved paper: "This question is in [N] active papers. Changes will not update already-printed papers."

### 5.3 Drawer: `question-preview` — Preview Question
- **Trigger:** Preview row action or Q# column link
- **Width:** 480px
- **Content:** Renders full question exactly as it will appear to students — KaTeX active, images displayed, options formatted
- **Tabs:** Question View · Classification · Usage History

#### Tab: Question View
Full rendered question + options (if MCQ). Answer shown with correct option highlighted. Explanation displayed below.

#### Tab: Classification
Read-only: Subject, Topic, Subtopic, Stream, Class, Difficulty stars, Bloom Level, Board, Tags, Source.

#### Tab: Usage History
Table: Paper Name · Exam Name · Date Used · Stream · Class. Shows every paper this question has been included in.

### 5.4 Modal: XLSX Import
- **Trigger:** [Import XLSX ↑] header button
- **Width:** 560px
- **Step 1:** Download XLSX template (columns: Question, Option_A, Option_B, Option_C, Option_D, Correct_Answer, Type, Difficulty, Bloom, Subject, Topic, Stream, Class, Marks, Tags, Source)
- **Step 2:** File upload — .xlsx only, max 10 MB
- **Step 3:** Validation report — row-level error table (Row # · Column · Error · Value)
- **Note for LaTeX:** LaTeX in imported cells must use `$formula$` syntax. The import validator checks for mismatched LaTeX delimiters.
- **Step 4:** [Confirm Import] — imports valid rows, skips error rows
- **Step 5:** "[N] questions added" toast. Error rows downloadable as XLSX.

### 5.5 Modal: Retire Confirm
- **Width:** 420px
- **Content:** "Retire Q#[N] — [Subject] — [Topic]? This question will be excluded from all new papers."
- **Warning:** "This question appears in [N] active papers." (if applicable)
- **Fields:** Reason (required, min 10 chars)
- **Buttons:** [Confirm Retire] (danger) + [Cancel]

---

## 6. Charts

### 6.1 Questions per Subject (Bar Chart)
- **Type:** Vertical bar chart
- **Data:** Active question count per subject
- **X-axis:** Subject names
- **Y-axis:** Question count
- **Colour:** Stacked by question type (MCQ/Short/Long/Numerical)
- **Tooltip:** Subject · Total: N · MCQ: M · Short: P etc.
- **Filter:** Stream selector, Class selector
- **Export:** PNG

### 6.2 Difficulty Distribution (Donut Chart)
- **Type:** Donut chart
- **Data:** Count per difficulty level (1–5) for current filtered view
- **Segments:** Five segments labelled 1 (Easy) through 5 (Hard)
- **Tooltip:** Difficulty · Count · %
- **Export:** PNG

### 6.3 Questions Added per Month (Line Chart)
- **Type:** Line chart — last 12 months
- **Data:** New questions added per month
- **X-axis:** Month (Apr–Mar)
- **Y-axis:** Count
- **Tooltip:** Month · Added: N
- **Export:** PNG

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Question created | "Q#[N] added to question bank." | Success | 4s |
| Question updated | "Q#[N] updated." | Success | 4s |
| Question cloned | "Q#[N] cloned as Q#[M]. Review before saving." | Info | 4s |
| Question retired | "Q#[N] retired." | Warning | 6s |
| Added to paper | "Q#[N] added to [Paper Name]." | Success | 4s |
| Import success | "[N] questions imported. [M] rows had errors — see error report." | Success | 4s |
| Import errors | "Import failed validation — [N] row errors. Download error report." | Error | Manual |
| Export started | "Export preparing… download will start shortly." | Info | 4s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No questions in bank | "Question bank is empty" | "Add the first question to start building your exam repository." | [+ New Question] |
| Per-stream empty | "No questions for [Subject]" | "Add your first question for [Subject]." | [+ New Question] |
| No results for search | "No questions match" | "Try different subject, topic, or question text keywords." | [Clear Search] |
| Filter returns empty | "No questions match your filters" | "Try removing some filters." | [Clear All Filters] |
| Retired-only view | "All matching questions are retired" | "Retired questions cannot be added to new papers." | [Show Active Questions] |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: stats bar + table (10 skeleton rows) |
| Table filter/search/sort/page | Inline skeleton rows (10) |
| question-create drawer open | Spinner in drawer body |
| question-preview drawer open | Spinner → KaTeX render (client-side, near-instant) |
| LaTeX preview render | Debounced 200ms — renders in preview panel, no loader needed |
| Question save submit | Spinner in submit button |
| XLSX import validation | Progress bar in import modal |
| Retire confirm | Spinner in confirm button |
| Charts load | Skeleton chart placeholders |
| Export trigger | Spinner in export button (momentary) |

---

## 10. Role-Based UI Visibility

| Element | CAO G4 | Exam Controller G3 | Curriculum Coord G2 | Stream Coords G3 | Academic Dir G3 |
|---|---|---|---|---|---|
| [+ New Question] button | ✅ | ✅ | ✅ | ✅ (own stream) | ❌ |
| [Import XLSX] button | ✅ | ✅ | ✅ | ❌ | ❌ |
| [Export XLSX] button | ✅ | ✅ | ❌ | ❌ | ✅ |
| Edit row action | ✅ | ✅ | ✅ (own) | ✅ (own stream) | ❌ |
| Clone row action | ✅ | ✅ | ❌ | ✅ (own stream) | ❌ |
| Retire row action | ✅ | ✅ | ❌ | ❌ | ❌ |
| Add to Paper action | ✅ | ✅ | ❌ | ❌ | ❌ |
| Bulk retire | ✅ | ✅ | ❌ | ❌ | ❌ |
| Last Used column | ✅ | ✅ | ❌ | ❌ | ❌ |
| Usage History tab (preview) | ✅ | ✅ | ❌ | ❌ | ❌ |
| Stream filter (all streams) | ✅ | ✅ | ✅ | ❌ (own only) | ✅ |
| Charts section | ✅ | ✅ | ✅ | ✅ (own stream) | ✅ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/acad/question-bank/` | JWT | List questions (filtered/sorted/paginated) |
| POST | `/api/v1/group/{group_id}/acad/question-bank/` | JWT (create roles) | Create question |
| GET | `/api/v1/group/{group_id}/acad/question-bank/{q_id}/` | JWT | Question detail + preview data |
| PUT | `/api/v1/group/{group_id}/acad/question-bank/{q_id}/` | JWT (edit roles) | Update question |
| POST | `/api/v1/group/{group_id}/acad/question-bank/{q_id}/retire/` | JWT (CAO/Exam Ctrl) | Retire question |
| POST | `/api/v1/group/{group_id}/acad/question-bank/{q_id}/clone/` | JWT (create roles) | Clone question |
| GET | `/api/v1/group/{group_id}/acad/question-bank/{q_id}/usage/` | JWT (CAO/Exam Ctrl) | Usage history |
| POST | `/api/v1/group/{group_id}/acad/question-bank/import/` | JWT (CAO/Exam Ctrl/Coord) | XLSX bulk import |
| GET | `/api/v1/group/{group_id}/acad/question-bank/export/` | JWT (CAO/Exam Ctrl/Dir) | XLSX export |
| GET | `/api/v1/group/{group_id}/acad/question-bank/stats/` | JWT | Summary stats bar data |
| GET | `/api/v1/group/{group_id}/acad/question-bank/charts/by-subject/` | JWT | Bar chart data |
| GET | `/api/v1/group/{group_id}/acad/question-bank/charts/difficulty/` | JWT | Donut chart data |
| GET | `/api/v1/group/{group_id}/acad/question-bank/charts/additions-trend/` | JWT | Line chart data |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Question search | `input delay:300ms` | GET `.../question-bank/?q=` | `#qb-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../question-bank/?filters=` | `#qb-table-section` | `innerHTML` |
| Sort column | `click` | GET `.../question-bank/?sort=&dir=` | `#qb-table-section` | `innerHTML` |
| Pagination | `click` | GET `.../question-bank/?page=` | `#qb-table-section` | `innerHTML` |
| Preview drawer open | `click` | GET `.../question-bank/{id}/` | `#drawer-body` | `innerHTML` |
| Create drawer open | `click` | GET `.../question-bank/create-form/` | `#drawer-body` | `innerHTML` |
| Create submit | `submit` | POST `.../question-bank/` | `#drawer-body` | `innerHTML` |
| Retire confirm | `click` | POST `.../question-bank/{id}/retire/` | `#q-row-{id}` | `outerHTML` |
| Stats bar refresh | `load` | GET `.../question-bank/stats/` | `#stats-bar` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
