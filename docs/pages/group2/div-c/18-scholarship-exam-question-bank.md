# Page 18: Scholarship Exam Question Bank

**URL:** `/group/adm/scholarship-exam/question-bank/`
**Template:** `portal_base.html` (light theme)
**Division:** C — Group Admissions · Scholarship Section

---

## 1. Purpose

The Scholarship Exam Question Bank is the secure, centralised repository of all examination questions used in scholarship entrance tests across the group. The Group Scholarship Exam Manager is the primary custodian of this bank — responsible for adding new questions, reviewing submissions from subject-matter contributors, approving questions for use, categorising them by subject, topic, class level, difficulty, and type, and retiring questions that have been over-exposed or are no longer relevant. The bank feeds directly into the Exam Paper Builder (Page 24) when assembling question papers, ensuring that paper creation is systematic, balanced, and traceable.

Questions in this bank are classified under a strict confidentiality regime. Access is restricted exclusively to G3+ roles in the scholarship exam function — no counsellor, coordinator, or alumni-facing role can view question content. This ensures that candidates do not receive advance exposure to exam questions through any internal channel. Every question record carries a usage audit trail: how many times it has been used, in which exams, and when it was last included in a paper.

Quality assurance is built into the workflow. Subject teachers or external contributors may submit questions, but they move through a Draft → Under Review → Approved state machine before becoming eligible for paper inclusion. The Scholarship Exam Manager reviews each pending question, can modify it, request revisions, or approve it directly. The Subject Distribution Chart and Difficulty Distribution Chart in this page help the Manager identify gaps — subjects that are under-represented or difficulty bands that have too few approved questions — so the bank remains healthy enough to support future exam cycles without question repetition.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Scholarship Exam Manager (26) | G3 | Full CRUD — add, edit, approve, retire, bulk import | Primary owner of this page |
| Group Admissions Director (23) | G3 | View all questions + approve | Cannot add or bulk import |
| Group Admission Coordinator (24) | G3 | No access | Excluded entirely |
| Group Admission Counsellor (25) | G3 | No access | Excluded entirely |
| Group Alumni Relations Manager (28) | G3 | No access | Excluded entirely |
| Group Demo Class Coordinator (29) | G3 | No access | Excluded entirely |
| MIS Officer | G2 | No access | Excluded entirely |

**Enforcement:** This page is restricted to Scholarship Exam Manager and Director roles only. Django view decorator `@role_required(['scholarship_exam_manager', 'admissions_director'])` enforces this at the view level. JWT must carry `function == scholarship_exam` for write operations. All other roles receive an HTTP 403 redirect to the portal home page.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Admissions → Scholarship Exams → Question Bank
```

### 3.2 Page Header
- **Title:** Scholarship Exam Question Bank
- **Subtitle:** Secure question repository — G3 restricted access
- **Action Buttons:** `[+ Add Question]` (Exam Manager only) · `[Bulk Import]` (Exam Manager only) · `[Export Approved PDF]` · `[Subject Gap Report]`
- **Bank Health Chip:** Health indicator — "Bank Healthy" (green) if all subjects have ≥ 50 approved questions; "Gaps Detected" (amber) otherwise

### 3.3 Alert Banner
Triggers (dismissible per session):
- **Amber — Subject Gap:** "3 subjects have fewer than 50 approved questions (Biology, History, Economics). [View Gaps →]"
- **Amber — Pending Review Backlog:** "28 questions have been awaiting review for more than 7 days. [Review Now →]"
- **Blue — Import Complete:** "Bulk import completed: 45 questions imported, 3 errors. [View Report →]"
- **Red — Bank Coverage Risk:** "Physics (Class 11) has only 12 approved questions. Insufficient for a full paper. [Add Questions →]"

---

## 4. KPI Summary Bar

| Card | Metric | Source | Colour Rule | Drill-down |
|---|---|---|---|---|
| Total Questions (Bank) | COUNT of all non-deleted question records | `question_bank` table | Blue always | → full table, no filter |
| Added This Month | COUNT where created_at >= first day of current month | `question_bank` aggregation | Blue always | → table filtered by date |
| Pending Review | COUNT where status = 'under_review' | `question_bank` status filter | Red > 10 · Amber 1–10 · Green = 0 | → Section 5.4 |
| Used in Last Exam | COUNT of distinct questions used in the most recently conducted exam | `exam_question_usage` join | Blue always | → usage report |
| Subject Gaps | COUNT of subjects where approved_count < 50 | `question_bank` group by subject | Red > 0 · Green = 0 | → subject distribution chart |
| Difficulty Distribution | Inline mini stat: "Easy {n} / Medium {n} / Hard {n}" (approved only) | `question_bank` group by difficulty | Blue always | → difficulty chart |

**HTMX Refresh:** KPI bar refreshes every 5 minutes via `hx-trigger="every 5m"` targeting `#kpi-bar` with `GET /api/v1/group/{group_id}/adm/scholarship-exam/question-bank/kpis/`.

---

## 5. Sections

### 5.1 Question Bank Table

**Display:** Sortable, selectable (checkbox), server-side paginated (20/page). Default sort: created_at DESC.

**Columns:**

| Column | Notes |
|---|---|
| Checkbox | Bulk select |
| Q ID | System-generated reference, e.g., QB-2026-0341 |
| Subject | Text |
| Topic | Text |
| Class Level | Class 9 / 10 / 11 / 12 etc. |
| Question Text | Truncated to 80 characters with ellipsis — full text in drawer |
| Type | MCQ (blue chip) / Short Answer (grey chip) / Integer (teal chip) |
| Difficulty | Easy (green) / Medium (amber) / Hard (red) badge |
| Status | Draft (grey) / Under Review (amber) / Approved (green) / Retired (red) |
| Added by | Staff name |
| Used Count | Number of times included in a paper |
| Actions | `[View →]` always · `[Edit]` if Draft/Under Review · `[Approve]` if Under Review, Manager/Director only · `[Retire]` if Approved |

**Search:** Full-text search across question_text, subject, topic — `hx-trigger="keyup changed delay:400ms"`.

**Filters:** Subject (multi-select), Topic (dependent on subject selection), Difficulty, Type, Status, Class Level

**Bulk Actions (Manager only):** `[Approve Selected]` · `[Retire Selected]` · `[Export PDF]`

**HTMX Pattern:** Filter/search changes trigger `GET /api/v1/group/{group_id}/adm/scholarship-exam/question-bank/questions/` targeting `#question-table-body` with `hx-swap="innerHTML"`.

**Empty State:** No questions match filters. Icon: book-question. Heading: "No Questions Found". CTA: `[Clear Filters]` or `[+ Add Question]`.

---

### 5.2 Subject Distribution Chart

**Display:** Donut chart (Chart.js 4.x) — one segment per subject. Segment size = total questions. Colour split within segment shown via tooltip: approved (green shade) / under review (amber shade) / draft (grey shade).

**Legend:** Listed below chart with question counts per subject.

**Interaction:** Click a segment → filters Section 5.1 table to that subject.

**Gap Indicator:** Subjects with total approved < 50 shown with a warning asterisk (*) in the legend.

**HTMX Load:** `hx-trigger="load"` → `GET /api/v1/group/{group_id}/adm/scholarship-exam/question-bank/stats/subject-distribution/` returning Chart.js-ready JSON.

---

### 5.3 Difficulty Distribution

**Display:** Stacked horizontal bar chart (Chart.js 4.x) — one bar per subject. Segments: Easy (green) / Medium (amber) / Hard (red) — approved questions only.

**Y-axis:** Subject names. **X-axis:** Count of approved questions.

**Tooltip:** On hover: subject name, Easy count, Medium count, Hard count, total approved.

**Interaction:** Click a bar segment → filters Section 5.1 table to that subject + difficulty.

**HTMX Load:** `hx-trigger="load"` → `GET /api/v1/group/{group_id}/adm/scholarship-exam/question-bank/stats/difficulty-distribution/`.

---

### 5.4 Questions Pending Review

**Display:** Sub-table (collapsible, expanded by default when pending_review KPI > 0). Compact row display.

**Columns:** Q ID · Subject · Topic · Difficulty · Question Text (80 chars) · Submitted by · Submitted date · Days waiting · `[Quick Review]`

**`[Quick Review]`:** Opens the question-detail-view drawer with Approve/Edit/Reject actions.

**Sort:** Days waiting DESC (longest waiting first).

**HTMX Pattern:** `hx-trigger="load"` to populate sub-table. After any approve/retire action, `htmx:afterRequest` refreshes this sub-table and the KPI bar.

**Empty State:** No questions pending review. Icon: check-badge. Heading: "Review Queue Clear". Description: "All submitted questions have been reviewed."

---

### 5.5 Question Upload / Bulk Import

**Display:** Upload card — DOCX or CSV template.

**Card Contents:**
- **Template Download:** `[Download DOCX Template]` · `[Download CSV Template]`
- **Upload Area:** Drag-and-drop zone or file picker — accepts `.docx`, `.csv`
- **Validation Instructions:** Shows field requirements inline
- **Upload Progress:** HTMX-driven progress bar after file selection

**Post-Upload:** Validation report shown inline: Rows processed / Questions imported / Rows with errors (with row-by-row error list) / Warnings. [View Full Report →] opens bulk-import-result drawer.

**HTMX Pattern:** File selection triggers `hx-post="/api/v1/group/{group_id}/adm/scholarship-exam/question-bank/import/"` (multipart/form-data) targeting `#import-result-area` with `hx-swap="innerHTML"`. Shows spinner during processing.

**Empty State (before upload):** Dashed upload border with cloud-upload icon. "Drag & drop your question file here or click to browse."

---

## 6. Drawers & Modals

### 6.1 Question Detail View Drawer
- **Width:** 640px (right slide-in)
- **Trigger:** `[View →]` on table row or `[Quick Review]`
- **HTMX Endpoint:** `GET /api/v1/group/{group_id}/adm/scholarship-exam/question-bank/questions/{question_id}/view/`
- **Content:** Full question text, answer options (A/B/C/D for MCQ), correct answer highlighted, explanation text, subject/topic/class/difficulty/type tags, usage history (which exams), added by + date, current status
- **Actions:** `[Edit]` (if Draft/Under Review) · `[Approve]` (if Under Review, Manager/Director) · `[Mark for Retirement]` (if Approved)
- All actions trigger respective HTMX POST calls and refresh the table row via `hx-swap="outerHTML"` on the row.

### 6.2 Question Edit Form Drawer
- **Width:** 640px
- **Trigger:** `[Edit]` from table row or Detail View drawer
- **HTMX Endpoint:** `GET /api/v1/group/{group_id}/adm/scholarship-exam/question-bank/questions/{question_id}/edit-form/`
- **Tabs:**
  1. **Question** — Question text (rich text), Class level, Subject, Topic, Type
  2. **Options** — For MCQ: Option A, B, C, D text fields
  3. **Answer** — Correct answer selector (A/B/C/D for MCQ, numeric for integer)
  4. **Explanation** — Explanation text (rich text) + solution steps
  5. **Tags** — Difficulty, Bloom's taxonomy level, Chapter reference
  6. **Preview** — Rendered preview of question as it will appear in a paper
- **Submit:** `hx-put` → `/api/v1/group/{group_id}/adm/scholarship-exam/question-bank/questions/{question_id}/` · on success: refresh row in table, show toast

### 6.3 Bulk Import Result Drawer
- **Width:** 560px
- **Trigger:** After import completes, `[View Full Report →]`
- **HTMX Endpoint:** `GET /api/v1/group/{group_id}/adm/scholarship-exam/question-bank/import/{import_id}/report/`
- **Content:** Import summary card (total / imported / errors / warnings) + error detail table (Row number, Field, Error message) + warning list

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Question added | "Question QB-{id} added to bank (status: Draft)." | Success | 4 s |
| Question updated | "Question QB-{id} updated." | Success | 3 s |
| Question approved | "Question QB-{id} approved." | Success | 3 s |
| Bulk approve | "{n} questions approved." | Success | 4 s |
| Question retired | "Question QB-{id} retired." | Info | 3 s |
| Bulk retire | "{n} questions retired." | Info | 4 s |
| Import started | "Processing import file..." | Info | 3 s |
| Import success | "Import complete: {n} questions added, {e} errors." | Success | 5 s |
| Import failed | "Import failed: invalid file format. Download the template and retry." | Error | 6 s |
| Approve action unauthorised | "Only Scholarship Exam Manager or Director can approve questions." | Error | 5 s |
| PDF export queued | "Question export PDF is being prepared." | Info | 3 s |

---

## 8. Empty States

| Condition | Illustration | Heading | Description | CTA |
|---|---|---|---|---|
| Bank is empty (no questions at all) | Book-open icon | "Question Bank is Empty" | "Add questions manually or use bulk import to populate the bank." | `[+ Add Question]` · `[Bulk Import]` |
| Filter returns no results | Search-x icon | "No Questions Match Filters" | "Try adjusting filters or broadening the search." | `[Clear Filters]` |
| Review queue empty | Check-badge icon | "Review Queue Clear" | "All submitted questions have been reviewed." | None |
| No subject gaps | Check-circle icon | "No Subject Gaps" | "All subjects have at least 50 approved questions." | None |
| No import history | Upload-cloud icon | "No Imports Yet" | "Use the template to bulk-import questions from DOCX or CSV." | `[Download Template]` |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | Full-page skeleton: KPI shimmer (6 cards) + table rows shimmer (5 rows) + chart placeholders |
| KPI bar refresh | In-place spinner per KPI card |
| Table filter / search | Table body skeleton (5 row shimmer) |
| Drawer open | 640px drawer skeleton with 6 tab-label shimmers + content shimmer |
| Chart load (subject donut) | Chart.js loading animation in canvas area |
| Chart load (difficulty bars) | Horizontal bar loading animation |
| Bulk import upload | Progress bar + spinner overlay on upload card |
| Bulk approve / retire | Button spinner + "Processing…" text |
| Quick review action (approve/retire) | Inline row spinner while HTMX request in flight |

---

## 10. Role-Based UI Visibility

| Element | Exam Manager (26) | Director (23) | Coordinator (24) | Counsellor (25) | Other Roles |
|---|---|---|---|---|---|
| `[+ Add Question]` button | Visible | Hidden | No access | No access | No access |
| `[Bulk Import]` button | Visible | Hidden | No access | No access | No access |
| `[Edit]` on table/drawer | Visible | Hidden | No access | No access | No access |
| `[Approve]` on table/drawer | Visible | Visible | No access | No access | No access |
| `[Retire]` on table/drawer | Visible | Hidden | No access | No access | No access |
| Bulk action bar | Visible | Hidden | No access | No access | No access |
| Section 5.4 Quick Review | Visible (full actions) | Visible (approve only) | No access | No access | No access |
| Section 5.5 Bulk Import card | Visible | Hidden | No access | No access | No access |
| `[Export Approved PDF]` | Visible | Visible | No access | No access | No access |
| Page itself | Accessible | Accessible | 403 redirect | 403 redirect | 403 redirect |

*All UI visibility decisions made server-side in Django template. No client-side JS role checks.*

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/adm/scholarship-exam/question-bank/kpis/` | JWT G3 (exam_mgr/director) | KPI bar data |
| GET | `/api/v1/group/{group_id}/adm/scholarship-exam/question-bank/questions/` | JWT G3 | Paginated, filtered question list |
| POST | `/api/v1/group/{group_id}/adm/scholarship-exam/question-bank/questions/` | JWT G3 write | Create new question |
| GET | `/api/v1/group/{group_id}/adm/scholarship-exam/question-bank/questions/{question_id}/view/` | JWT G3 | Question detail drawer fragment |
| GET | `/api/v1/group/{group_id}/adm/scholarship-exam/question-bank/questions/{question_id}/edit-form/` | JWT G3 | Question edit form drawer fragment |
| PUT | `/api/v1/group/{group_id}/adm/scholarship-exam/question-bank/questions/{question_id}/` | JWT G3 write | Update question |
| POST | `/api/v1/group/{group_id}/adm/scholarship-exam/question-bank/questions/{question_id}/approve/` | JWT G3 write | Approve question |
| POST | `/api/v1/group/{group_id}/adm/scholarship-exam/question-bank/questions/{question_id}/retire/` | JWT G3 write | Retire question |
| POST | `/api/v1/group/{group_id}/adm/scholarship-exam/question-bank/questions/bulk-approve/` | JWT G3 write | Bulk approve questions |
| POST | `/api/v1/group/{group_id}/adm/scholarship-exam/question-bank/questions/bulk-retire/` | JWT G3 write | Bulk retire questions |
| POST | `/api/v1/group/{group_id}/adm/scholarship-exam/question-bank/import/` | JWT G3 write | Upload bulk import file |
| GET | `/api/v1/group/{group_id}/adm/scholarship-exam/question-bank/import/{import_id}/report/` | JWT G3 | Import result report drawer fragment |
| GET | `/api/v1/group/{group_id}/adm/scholarship-exam/question-bank/stats/subject-distribution/` | JWT G3 | Subject distribution chart data |
| GET | `/api/v1/group/{group_id}/adm/scholarship-exam/question-bank/stats/difficulty-distribution/` | JWT G3 | Difficulty distribution chart data |
| GET | `/api/v1/group/{group_id}/adm/scholarship-exam/question-bank/export/pdf/` | JWT G3 | Export approved questions PDF |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| KPI bar auto-refresh | `every 5m` | GET `.../question-bank/kpis/` | `#kpi-bar` | `innerHTML` |
| Full-text search questions | `keyup changed delay:400ms` on search input | GET `.../question-bank/questions/?search={q}` | `#question-table-body` | `innerHTML` |
| Filter table | `change` on filter inputs | GET `.../question-bank/questions/?{filters}` | `#question-table-body` | `innerHTML` |
| Paginate table | `click` on page link | GET `.../question-bank/questions/?page={n}` | `#question-table-container` | `innerHTML` |
| Sort column | `click` on column header | GET `.../question-bank/questions/?sort={col}&dir={asc\|desc}` | `#question-table-body` | `innerHTML` |
| Open question view drawer | `click` on `[View →]` | GET `.../question-bank/questions/{id}/view/` | `#drawer-container` | `innerHTML` |
| Open question edit drawer | `click` on `[Edit]` | GET `.../question-bank/questions/{id}/edit-form/` | `#drawer-container` | `innerHTML` |
| Open question add drawer | `click` on `[+ Add Question]` | GET `.../question-bank/questions/new-form/` | `#drawer-container` | `innerHTML` |
| Submit question form (create) | `submit` on question form | POST `.../question-bank/questions/` | `#question-table-body` | `innerHTML` |
| Submit question form (edit) | `submit` on edit form | PUT `.../question-bank/questions/{id}/` | `#question-row-{id}` | `outerHTML` |
| Approve single question | `click` on `[Approve]` | POST `.../question-bank/questions/{id}/approve/` | `#question-row-{id}` | `outerHTML` |
| Retire single question | `click` on `[Retire]` | POST `.../question-bank/questions/{id}/retire/` | `#question-row-{id}` | `outerHTML` |
| Bulk approve | `click` on `[Approve Selected]` | POST `.../question-bank/questions/bulk-approve/` | `#question-table-body` | `innerHTML` |
| Load subject distribution chart | `load` on chart container | GET `.../question-bank/stats/subject-distribution/` | `#subject-chart-data` | `innerHTML` |
| Load difficulty distribution chart | `load` on chart container | GET `.../question-bank/stats/difficulty-distribution/` | `#difficulty-chart-data` | `innerHTML` |
| Load pending review sub-table | `load` on section | GET `.../question-bank/questions/?status=under_review` | `#pending-review-table` | `innerHTML` |
| Bulk import file upload | `change` on file input | POST `.../question-bank/import/` (multipart) | `#import-result-area` | `innerHTML` |
| View import report drawer | `click` on `[View Full Report →]` | GET `.../question-bank/import/{id}/report/` | `#drawer-container` | `innerHTML` |
| Refresh pending review after approve | `htmx:afterRequest` from approve call | GET `.../question-bank/questions/?status=under_review` | `#pending-review-table` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
