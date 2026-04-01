# 42 — Scholarship Exam Paper Builder

> **URL:** `/group/adm/scholarship-exam/paper-builder/`
> **File:** `42-scholarship-exam-paper-builder.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Group Scholarship Exam Manager (Role 26) — primary

---

## 1. Purpose

The Scholarship Exam Paper Builder is the dedicated workspace where a scholarship or entrance exam paper is assembled from individual questions stored in the Question Bank (Page 18 — Scholarship Exam Question Bank). Building a high-quality exam paper is not merely a matter of selecting any set of questions — it demands careful balancing across subjects, difficulty levels, section structure, total marks, and time allocation. An unbalanced paper that is heavily skewed toward hard questions, or one where the total achievable marks do not tally with the declared marks ceiling, damages the credibility of the scholarship program and can trigger candidate objections that are difficult to resolve post-exam. The Paper Builder enforces structural quality rules throughout the assembly process and blocks submission of any paper that does not pass the automated quality checks.

The workflow is linear and enforced: the Exam Manager selects a scheduled exam from the Paper Status Table (Section 5.1), enters the Paper Builder Workspace (Section 5.2), defines the exam header, builds sections, adds questions either manually or via the Auto-Select engine, previews the assembled paper, reviews the auto-generated answer key, and then submits the paper to the Director's approval queue (Section 5.3). The Director either approves or returns the paper with feedback. Only after approval does the Dispatch Manager (Section 5.4) become active, allowing the Exam Manager to securely distribute the finalised paper to branches. The system maintains a full version history (Section 5.5) so that any post-exam objection about a question can be traced back to the exact paper version that was dispatched.

Confidentiality controls are paramount in this workflow. Once a paper reaches the Approved status, access to individual question content is restricted — only the Exam Manager and Director can view the full paper. All read accesses to an approved or dispatched paper are written to an audit log. Dispatched papers use secure one-time download links or encrypted email attachments — never plain-text embeds. This ensures that exam confidentiality is maintained from the paper-building stage through to the exam day.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Scholarship Exam Manager (Role 26) | G3 | Full access — build, edit, auto-select, submit for approval, dispatch | Primary operator |
| Group Admissions Director (Role 23) | G3 | View + approve papers + return with feedback + dispatch | Cannot build or edit papers |
| Group Scholarship Manager (Role 27) | G3 | View only — paper status table (no question content access) | Operational oversight |
| Group Admission Coordinator (Role 24) | G3 | No access | Not in scope |
| Group Admission Counsellor (Role 25) | G3 | No access | Not in scope |
| Group Alumni Relations Manager (Role 28) | G3 | No access | Not in scope |
| Group Demo Class Coordinator (Role 29) | G3 | No access | Not in scope |

> **Enforcement:** `@role_required(['scholarship_exam_manager', 'admissions_director', 'scholarship_manager'])` at the Django view level. Paper build/edit endpoints require `request.user.role == 'scholarship_exam_manager'`. Approve and return-with-feedback endpoints require `request.user.role == 'admissions_director'`. Scholarship Manager receives a read-only template (`paper_readonly=True` in context) with no question-level content displayed. All accesses to papers with status Approved or Dispatched are written to `PaperAccessLog`.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal › Admissions › Scholarship Exams › Paper Builder
```

### 3.2 Page Header
- **Title:** Scholarship Exam Paper Builder
- **Subtitle:** Build, review, and dispatch exam papers — `{current_cycle_name}`
- **Right-side controls:**
  - `[+ New Paper]` (Exam Manager only — only active when an exam with no paper exists)
  - `[Dispatch to All Branches →]` (Exam Manager + Director — only active when approved papers exist)
  - `[Refresh ↺]`

### 3.3 Alert Banner

Collapsible panel above the KPI row. `bg-red-50 border-l-4 border-red-500` for Critical; `bg-yellow-50 border-l-4 border-yellow-400` for Warning; `bg-blue-50 border-l-4 border-blue-400` for Info.

| Trigger | Severity | Message |
|---|---|---|
| Exam < 7 days away with no finalised paper | Critical | "URGENT: {Exam Name} is {N} days away and has no approved paper. [Build Now →]" |
| Exam < 14 days away with paper still in draft | Warning | "{Exam Name} is {N} days away — paper is still in Draft. Submit for review. [Review Draft →]" |
| Paper returned by Director | Warning | "'{Exam Name}' paper returned with feedback. [View Feedback →]" |
| Paper approved by Director | Info | "'{Exam Name}' paper approved. Ready for dispatch. [Dispatch Now →]" |
| Quality check failed on paper submission attempt | Critical | "Paper for '{Exam Name}' failed quality check. {N} critical errors must be fixed before submission." |
| Dispatch completed | Info | "'{Exam Name}' paper dispatched to {N} branches successfully." |

---

## 4. KPI Summary Bar

Auto-refreshes every 5 minutes via HTMX:

```html
<div id="paper-builder-kpi-bar"
     hx-get="/api/v1/group/{group_id}/adm/scholarship-exam/paper-builder/kpis/"
     hx-trigger="load, every 5m"
     hx-target="#paper-builder-kpi-bar"
     hx-swap="innerHTML">
  <!-- KPI cards rendered here -->
</div>
```

| Card | Metric | Source | Colour Rule | Drill-down |
|---|---|---|---|---|
| Exams Needing Papers | COUNT of scheduled exams with no paper record at all | `scholarship_exam` JOIN `exam_paper` | Red if > 0; green if 0 | Filters 5.1 to "No Paper" status |
| Papers in Draft | COUNT of papers with status = 'draft' | `exam_paper` | Amber if > 0; grey if 0 | Filters 5.1 to Draft |
| Pending Director Approval | COUNT of papers with status = 'under_review' | `exam_paper` | Amber if > 0; grey if 0 | Scrolls to Approval Queue (5.3) |
| Papers Finalised / Approved | COUNT of papers with status = 'approved' | `exam_paper` | Green | Filters 5.1 to Approved |
| Papers Dispatched | COUNT of papers with status = 'dispatched' | `exam_paper` | Blue | Filters 5.1 to Dispatched |
| Exams < 7 Days — No Final Paper | COUNT of exams within 7 days where paper status != 'approved' and != 'dispatched' | Computed | Red if > 0; green if 0 | Filters 5.1 to urgent exams |

---

## 5. Sections

### 5.1 Paper Status Table

**Display:** Sortable, server-side paginated at 20 rows per page. Default sort: exam date ASC (soonest first). Status badges: No Paper (red), Draft (grey), Under Review (amber), Approved (green), Dispatched (blue).

**Columns:**

| Column | Notes |
|---|---|
| Exam Name | Exam name — click opens Paper Builder Workspace inline (5.2) |
| Type | Merit / Need-based / Special Category / Open — badge |
| Exam Date | `DD MMM YYYY` — red if within 7 days and paper not finalised |
| Paper Status | No Paper / Draft / Under Review / Approved / Dispatched — colour badge |
| Sections | Count of sections in the paper (0 if no paper yet) |
| Total Questions | Sum of questions across all sections |
| Total Marks | Sum of marks across all sections |
| Duration (mins) | Exam duration in minutes as configured in scheduler |
| Built By | Staff name who last edited/built the paper |
| Last Modified | `DD MMM YYYY HH:MM` |
| Actions | `[Build →]` (No Paper) · `[Edit →]` (Draft) · `[Preview]` · `[Approve →]` (Director only) · `[Dispatch →]` (Approved) |

**Filters:** Status (multi-select), Exam date range (from/to date picker)

**HTMX Pattern:**
```html
<div id="paper-status-table-wrapper"
     hx-get="/api/v1/group/{group_id}/adm/scholarship-exam/paper-builder/papers/"
     hx-trigger="load"
     hx-target="#paper-status-table-wrapper"
     hx-swap="innerHTML">
</div>
```
Filter change: `hx-trigger="change"` → `hx-target="#paper-status-table-body"` `hx-swap="innerHTML"`. Pagination: `hx-target="#paper-status-table-wrapper"` `hx-swap="innerHTML"`.

**Empty State:** Document stack graphic. Heading: "No Exams Scheduled." Description: "Scholarship exams will appear here once they are scheduled in the Exam Scheduler." CTA: `[Go to Exam Scheduler →]`

---

### 5.2 Paper Builder Workspace

**Display:** Full-width inline section that expands below Section 5.1 when `[Build →]` or `[Edit →]` is clicked. Not a drawer — it renders within the page body. Collapses/hides 5.1 table while open to give maximum screen real estate. A sticky top bar within the workspace shows: Exam Name (read-only) | Status badge | `[Save Draft]` `[Run Quality Check]` `[Submit for Review →]` `[Close Workspace ✕]`.

**5.2a — Exam Header**

Panel at the top of the workspace:

| Field | Type | Notes |
|---|---|---|
| Exam Name | Read-only display | From scheduler |
| Exam Type | Read-only display | From scheduler |
| Duration (mins) | Editable number field | Pre-populated from scheduler; override allowed |
| Instructions | Rich text editor | Exam instructions printed on paper; supports bold/italic/lists |
| Negative Marking Default | Toggle + number fields | Global default: Yes/No; if Yes: marks deducted per wrong answer (e.g. −0.25) |
| Section-level Override | Note text | "Individual sections can override the global negative marking setting below." |

**5.2b — Section Manager**

Add/remove/reorder paper sections. Each section card:

| Field | Notes |
|---|---|
| Section Name | Text input (e.g. "Physics", "Section A — Maths") |
| Question Count Target | Number — how many questions this section should contain |
| Marks per Question | Number — marks awarded for a correct answer |
| Negative Marks | Number — deduction per wrong answer (overrides global default if set) |
| Section total (computed) | Displayed: `{question_count} × {marks} = {total} marks` |
| `[Remove Section]` | Removes section and all its questions (confirmation prompt) |

`[+ Add Section]` button adds a new blank section card. Sections are drag-reorderable.

**5.2c — Question Selection per Section**

Each section has a question selection panel with two tabs:

*Tab 1: Manual Selection*
- Search bar: filter question bank by Subject, Topic, Difficulty (Easy/Medium/Hard), Class (9/10/11/12), Question Type (MCQ/True-False/Fill-in)
- Results table: Question ID | Subject | Topic | Difficulty | Marks | `[Add →]`
- `[Add →]` moves question into the section's selected list
- Selected questions list: drag-reorderable; `[Remove]` per question
- Section question count badge: "12 / 15 questions selected" (amber if under target; green if met; red if over)

*Tab 2: Auto-Select*
- Subject dropdown (matches section subject)
- Topic distribution: multi-select topics with % weight sliders (must sum to 100%)
- Difficulty ratio: Easy / Medium / Hard — three number inputs (must sum to 100%)
- Class filter: optional
- `[Preview Auto-selection]` — shows which questions will be selected (HTMX GET, renders preview list)
- `[Accept Auto-selection]` — populates the section with auto-selected questions
- `[Re-roll]` — generates a new random selection within the same criteria

**5.2d — Paper Preview**

Tab within the workspace (not a drawer). Renders a full read-through preview of the assembled paper as it will appear when printed. Shows:
- Exam header with instructions
- Section headings
- Numbered questions with A/B/C/D options
- Marks per question (right-aligned)
- Section subtotals and grand total

`[Print Preview]` opens a browser print dialog. `[Download Approved Paper PDF (available after Director approval)]` available for Approved papers only.

**5.2e — Answer Key Panel**

Auto-generated from question data in the Question Bank. Displays: Question Number | Correct Answer | Marks | Section. Editable (for manual corrections if a question has a known error). `[Regenerate from Question Bank]` button resets to auto-generated state.

**5.2f — Quality Checker and Submission**

`[Run Quality Check]` button triggers the automated quality check:

Warnings (non-blocking):
- "Section {N} has fewer than 2 Easy questions — consider adding easier questions."
- "Exam duration seems short for {total_questions} questions ({mins_per_question} min/question)."

Errors (blocking — must be resolved before submission):
- "Total achievable marks ({X}) does not match declared total ({Y})."
- "Section {N} question count ({X}) is below the target ({Y})."
- "Duplicate question IDs detected: {Q001, Q045}."
- "Answer key is incomplete — {N} questions have no correct answer assigned."

Results rendered in a quality-check panel: green if all clear; amber if warnings only; red if errors exist.

`[Submit to Director →]` — disabled if any blocking errors exist. On click: confirmation dialog "Submit '{Exam Name}' paper for Director approval? Once submitted, questions will be locked." → `[Confirm Submit]` → HTMX POST → paper status changes to Under Review.

**HTMX Patterns within Workspace:**
```html
<!-- Load workspace when [Build →] or [Edit →] clicked -->
<div id="paper-builder-workspace"
     hx-get="/api/v1/group/{group_id}/adm/scholarship-exam/paper-builder/papers/{paper_id}/workspace/"
     hx-trigger="click"
     hx-target="#paper-builder-workspace"
     hx-swap="innerHTML">
</div>
```
Auto-select preview: `hx-post="/api/v1/group/{group_id}/adm/scholarship-exam/paper-builder/papers/{paper_id}/sections/{section_id}/auto-select/preview/"` `hx-target="#auto-select-preview-list"` `hx-swap="innerHTML"`. Save draft: `hx-post` to save endpoint → `hx-target="#workspace-status-badge"` `hx-swap="innerHTML"`. Quality check: `hx-post` to quality-check endpoint → `hx-target="#quality-check-panel"` `hx-swap="innerHTML"`. Submit: `hx-post` to submit endpoint → `hx-target="#paper-status-table-wrapper"` `hx-swap="innerHTML"`.

**Empty State (workspace — no sections yet):** "No sections added. Click `[+ Add Section]` to start building the paper."

---

### 5.3 Paper Approval Queue

**Display:** Shown to the Director only (hidden from Exam Manager view via server-side template). Lists all papers with status = Under Review. Sorted by submission date ASC (oldest submitted first).

| Column | Notes |
|---|---|
| Exam Name | Exam name |
| Submitted By | Staff name + submission date/time |
| Exam Date | `DD MMM YYYY` |
| Sections | Count |
| Total Questions | Sum |
| Total Marks | Sum |
| Actions | `[Preview Paper]` · `[Approve →]` · `[Return with Feedback]` |

`[Preview Paper]` opens the paper-preview-drawer (6.1). `[Approve →]` requires confirmation: "Approve this paper? Questions will be locked and paper will be dispatched by Exam Manager." → HTMX POST → status changes to Approved. `[Return with Feedback]` opens approval-return-modal (6.3).

**HTMX Pattern:**
```html
<div id="approval-queue-table"
     hx-get="/api/v1/group/{group_id}/adm/scholarship-exam/paper-builder/approval-queue/"
     hx-trigger="load, every 5m"
     hx-target="#approval-queue-table"
     hx-swap="innerHTML">
</div>
```

**Empty State:** Inbox-zero graphic. "No papers pending approval." (Director only)

---

### 5.4 Dispatch Manager

**Display:** Active only for papers with status = Approved. Lists approved papers and their dispatch status per branch. One row per branch per approved paper.

| Column | Notes |
|---|---|
| Branch | Branch name |
| Exam | Exam name |
| Email Sent | Yes (green) / No (red) / N/A |
| Download Link Generated | Yes (green) / No (grey) |
| Acknowledged by Branch | Yes / No — branch must confirm receipt |
| Dispatch Date | `DD MMM YYYY HH:MM` or "Not dispatched" |
| Actions | `[Dispatch →]` (single branch) · `[Resend]` (if already dispatched) |

**Bulk:** `[Dispatch to All Branches →]` header action — opens dispatch-confirm-modal (6.2).

**HTMX Pattern:**
```html
<div id="dispatch-manager-table"
     hx-get="/api/v1/group/{group_id}/adm/scholarship-exam/paper-builder/dispatch/"
     hx-trigger="load"
     hx-target="#dispatch-manager-table"
     hx-swap="innerHTML">
</div>
```
Single dispatch: `hx-post="/api/v1/group/{group_id}/adm/scholarship-exam/paper-builder/dispatch/{paper_id}/branch/{branch_id}/"` `hx-target="#dispatch-row-{branch_id}"` `hx-swap="outerHTML"`. Bulk dispatch: via dispatch-confirm-modal.

**Empty State:** "No approved papers available for dispatch."

---

### 5.5 Paper Version History

**Display:** Collapsible section (closed by default). Lists all versions of all papers, grouped by exam. Clicking an exam name expands the version list for that exam.

| Column | Notes |
|---|---|
| Version | v1, v2, v3 — incremented on each save-and-submit |
| Created By | Staff name |
| Created Date | `DD MMM YYYY HH:MM` |
| Status | Draft / Submitted / Approved / Returned / Dispatched — badge |
| Changes from Previous | Summary note (e.g. "3 questions replaced in Section B; negative marking adjusted") |
| Actions | `[View →]` (opens paper-preview-drawer for that version) · `[Compare →]` (opens version-compare-drawer if v2 or later) |

**HTMX Pattern:**
```html
<div id="version-history-section"
     hx-get="/api/v1/group/{group_id}/adm/scholarship-exam/paper-builder/version-history/"
     hx-trigger="revealed"
     hx-target="#version-history-section"
     hx-swap="innerHTML">
</div>
```
Version view: `hx-get` to preview endpoint targeting `#paper-preview-drawer`. Compare: `hx-get` to compare endpoint targeting `#version-compare-drawer`.

**Empty State:** "No version history available yet."

---

### 5.6 Paper Quality Checker (Summary Panel)

**Display:** Always-visible summary panel in the right sidebar of the workspace. Updates live as questions are added or removed. Provides a running quality score and surfacing of issues before the Exam Manager manually triggers the full quality check.

| Check | Status | Detail |
|---|---|---|
| Marks tally | ✓ Pass / ✗ Fail | "Total achievable: {X} / Declared: {Y}" |
| Difficulty balance (per section) | ✓ / ⚠ Warning / ✗ Fail | "Section A: 40% Easy, 40% Medium, 20% Hard" |
| Question count targets met | ✓ / ✗ | "Section B: 12/15 questions added" |
| Duplicate question IDs | ✓ / ✗ | Lists any duplicate IDs if found |
| Answer key completeness | ✓ / ✗ | "{N} questions without answer assigned" |
| Time per question | ✓ / ⚠ | "{X} mins per question — [recommended: ≥1.5 mins]" |

Panel background: green if all checks pass; amber if warnings; red if any failures.

**HTMX Pattern:**
```html
<div id="quality-checker-panel"
     hx-get="/api/v1/group/{group_id}/adm/scholarship-exam/paper-builder/papers/{paper_id}/quality-check/"
     hx-trigger="load"
     hx-target="#quality-checker-panel"
     hx-swap="innerHTML">
</div>
```
Re-triggers on question add/remove via `hx-trigger="click from:.question-add-btn, click from:.question-remove-btn"`.

---

## 6. Drawers & Modals

### 6.1 Paper Preview Drawer
- **Width:** 640px (right-side slide-in)
- **Trigger:** `[Preview Paper]` in Approval Queue or `[View →]` in Version History
- **HTMX Endpoint:** `GET /api/v1/group/{group_id}/adm/scholarship-exam/paper-builder/papers/{paper_id}/preview/`
- **Content:** Full rendered paper — exam header and instructions, all sections, numbered questions with options, marks per question, answer key (separate tab, visible to authorised users only), paper metadata (version, built by, approved by). Actions: `[Print]` · `[Download PDF]` (Approved/Dispatched status only) · `[Close]`

---

### 6.2 Dispatch Confirm Modal
- **Width:** 480px (centred modal)
- **Trigger:** `[Dispatch to All Branches →]` or `[Dispatch →]` single branch
- **HTMX Endpoint:** `GET /api/v1/group/{group_id}/adm/scholarship-exam/paper-builder/dispatch/{paper_id}/confirm-form/`
- **Fields:** Exam name (read-only display), Dispatch method (Email PDF / Secure Download Link / Both — radio), Recipient per branch (auto-populated from branch coordinator contact; editable), Confidentiality notice (displayed as a prominent block: "This paper is CONFIDENTIAL. Recipients must not forward or share beyond the invigilator team."), `[Confirm Dispatch]` · `[Cancel]`

---

### 6.3 Approval Return Modal
- **Width:** 400px (centred modal)
- **Trigger:** `[Return with Feedback]` in Approval Queue (Director only)
- **HTMX Endpoint:** `GET /api/v1/group/{group_id}/adm/scholarship-exam/paper-builder/papers/{paper_id}/return-form/`
- **Fields:** Exam name (read-only), Feedback / Reason (required text area — minimum 20 characters), Specific sections to revise (optional multi-select of section names), `[Return Paper]` · `[Cancel]`
- **Action:** POST sets paper status back to Draft with feedback attached; Exam Manager is notified.

---

### 6.4 Version Compare Drawer
- **Width:** 560px (right-side slide-in)
- **Trigger:** `[Compare →]` in Version History
- **HTMX Endpoint:** `GET /api/v1/group/{group_id}/adm/scholarship-exam/paper-builder/papers/{paper_id}/compare/?v1={v}&v2={v}`
- **Content:** Side-by-side diff view of two selected versions. Left panel: older version; Right panel: newer version. Differences highlighted: added questions (green), removed questions (red), changed marks (amber), changed instructions (amber). Version selector dropdowns at the top to switch comparison pair.

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Draft saved | "Draft saved for '{Exam Name}'." | Success | 3s |
| Question added to section | "Question {Q-ID} added to {Section Name}." | Success | 3s |
| Question removed from section | "Question {Q-ID} removed from {Section Name}." | Info | 3s |
| Auto-select accepted | "{N} questions auto-selected for {Section Name}." | Success | 4s |
| Quality check passed | "Quality check passed — paper is ready for submission." | Success | 5s |
| Quality check failed | "Quality check failed: {N} error(s) found. Fix before submitting." | Error | 6s |
| Paper submitted for review | "'{Exam Name}' paper submitted to Director for approval." | Success | 5s |
| Paper approved | "'{Exam Name}' paper approved. Ready for dispatch." | Success | 5s |
| Paper returned with feedback | "Paper returned with feedback by Director. [View Feedback →]" | Warning | 6s |
| Dispatch sent (single branch) | "Paper dispatched to {Branch Name} successfully." | Success | 4s |
| Bulk dispatch completed | "'{Exam Name}' paper dispatched to {N} branches." | Success | 5s |
| Dispatch failed (partial) | "Dispatch failed for {N} branch(es). Check recipient email addresses." | Error | 6s |

---

## 8. Empty States

| Condition | Illustration | Heading | Description | CTA |
|---|---|---|---|---|
| No scheduled exams | Calendar graphic | "No Exams Scheduled" | "Scholarship exams will appear here once scheduled in the Exam Scheduler." | `[Go to Exam Scheduler →]` |
| Paper has no sections yet | Blank paper graphic | "No Sections Yet" | "Add sections to start building the exam paper." | `[+ Add Section]` |
| Section has no questions | Empty box graphic | "No Questions Added" | "Use Manual Selection or Auto-Select to add questions to this section." | (tabs visible) |
| No papers pending approval | Inbox-zero graphic | "No Papers Pending Approval" | "Papers submitted by the Exam Manager will appear here for your review." | — |
| No approved papers to dispatch | Lock graphic | "No Approved Papers" | "Papers must be approved by the Director before they can be dispatched." | — |
| No version history | Clock graphic | "No Version History" | "Version history is created when a paper is first submitted for review." | — |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Full-page skeleton: KPI bar shimmer + table skeleton (6 rows) |
| KPI bar auto-refresh | Inline spinner on each KPI card |
| Paper status table load | Table body skeleton (6-row shimmer) |
| Filter change | Table body skeleton |
| Paper Builder Workspace open | Full-section skeleton: header fields shimmer + section cards shimmer |
| Question bank search in Manual tab | Table body spinner (search results) |
| Auto-select preview generation | Inline spinner within preview list container |
| Quality check run | Full quality-check panel spinner "Running checks…" |
| Paper submit POST | Button spinner + workspace status badge update |
| Paper preview drawer open | Drawer skeleton: paper content shimmer |
| Approval queue auto-refresh | Table body skeleton |
| Dispatch manager table load | Table skeleton |
| Single dispatch POST | Row-level button spinner |
| Bulk dispatch POST | Modal progress indicator "Dispatching to branches…" |
| Version history section reveal | Section skeleton |
| Version compare drawer open | Drawer skeleton: two-column shimmer |

---

## 10. Role-Based UI Visibility

> All UI visibility decisions are made server-side in the Django template. No client-side JS role checks.

| UI Element | Exam Manager (26) | Director (23) | Scholarship Manager (27) |
|---|---|---|---|
| `[+ New Paper]` header button | Visible | Hidden | Hidden |
| `[Dispatch to All Branches →]` header button | Visible | Visible | Hidden |
| Paper Status Table | Visible (full) | Visible (full) | Visible (status only — no question counts) |
| `[Build →]` action | Visible | Hidden | Hidden |
| `[Edit →]` action | Visible | Hidden | Hidden |
| `[Preview]` action | Visible | Visible | Visible |
| `[Approve →]` action | Hidden | Visible | Hidden |
| `[Dispatch →]` action | Visible | Visible | Hidden |
| Paper Builder Workspace | Full access | Hidden | Hidden |
| Paper Approval Queue section | Hidden | Visible | Hidden |
| `[Approve →]` in approval queue | Hidden | Visible | Hidden |
| `[Return with Feedback]` in approval queue | Hidden | Visible | Hidden |
| Dispatch Manager section | Visible | Visible | Hidden |
| `[Resend]` dispatch | Visible | Visible | Hidden |
| Paper Version History section | Visible | Visible | Hidden |
| `[Compare →]` in version history | Visible | Visible | Hidden |
| Answer key tab in paper preview drawer | Visible | Visible | Hidden |
| Quality Checker panel in workspace | Visible | Hidden | Hidden |
| `[Submit for Review →]` in workspace | Visible | Hidden | Hidden |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/adm/scholarship-exam/paper-builder/kpis/` | JWT G3+ | KPI bar data |
| GET | `/api/v1/group/{group_id}/adm/scholarship-exam/paper-builder/papers/` | JWT G3+ | Paginated paper status table with filters |
| GET | `/api/v1/group/{group_id}/adm/scholarship-exam/paper-builder/papers/{paper_id}/workspace/` | JWT G3 | Paper Builder Workspace HTML fragment |
| POST | `/api/v1/group/{group_id}/adm/scholarship-exam/paper-builder/papers/` | JWT G3 | Create new paper record for an exam |
| PATCH | `/api/v1/group/{group_id}/adm/scholarship-exam/paper-builder/papers/{paper_id}/` | JWT G3 | Save paper header and settings |
| POST | `/api/v1/group/{group_id}/adm/scholarship-exam/paper-builder/papers/{paper_id}/sections/` | JWT G3 | Add section to paper |
| PATCH | `/api/v1/group/{group_id}/adm/scholarship-exam/paper-builder/papers/{paper_id}/sections/{section_id}/` | JWT G3 | Update section settings |
| DELETE | `/api/v1/group/{group_id}/adm/scholarship-exam/paper-builder/papers/{paper_id}/sections/{section_id}/` | JWT G3 | Remove section from paper |
| POST | `/api/v1/group/{group_id}/adm/scholarship-exam/paper-builder/papers/{paper_id}/sections/{section_id}/questions/` | JWT G3 | Add question to section (manual) |
| DELETE | `/api/v1/group/{group_id}/adm/scholarship-exam/paper-builder/papers/{paper_id}/sections/{section_id}/questions/{q_id}/` | JWT G3 | Remove question from section |
| POST | `/api/v1/group/{group_id}/adm/scholarship-exam/paper-builder/papers/{paper_id}/sections/{section_id}/auto-select/preview/` | JWT G3 | Preview auto-selected question set |
| POST | `/api/v1/group/{group_id}/adm/scholarship-exam/paper-builder/papers/{paper_id}/sections/{section_id}/auto-select/accept/` | JWT G3 | Accept auto-selected questions into section |
| GET | `/api/v1/group/{group_id}/adm/scholarship-exam/paper-builder/papers/{paper_id}/quality-check/` | JWT G3 | Run quality check and return results |
| POST | `/api/v1/group/{group_id}/adm/scholarship-exam/paper-builder/papers/{paper_id}/submit/` | JWT G3 | Submit paper for Director approval |
| GET | `/api/v1/group/{group_id}/adm/scholarship-exam/paper-builder/approval-queue/` | JWT G3 (Director) | List papers under review |
| POST | `/api/v1/group/{group_id}/adm/scholarship-exam/paper-builder/papers/{paper_id}/approve/` | JWT G3 (Director) | Approve paper |
| GET | `/api/v1/group/{group_id}/adm/scholarship-exam/paper-builder/papers/{paper_id}/return-form/` | JWT G3 (Director) | Return-with-feedback form fragment |
| POST | `/api/v1/group/{group_id}/adm/scholarship-exam/paper-builder/papers/{paper_id}/return/` | JWT G3 (Director) | Return paper with feedback |
| GET | `/api/v1/group/{group_id}/adm/scholarship-exam/paper-builder/papers/{paper_id}/preview/` | JWT G3+ | Full paper preview HTML fragment |
| GET | `/api/v1/group/{group_id}/adm/scholarship-exam/paper-builder/dispatch/` | JWT G3+ | Dispatch manager table data |
| GET | `/api/v1/group/{group_id}/adm/scholarship-exam/paper-builder/dispatch/{paper_id}/confirm-form/` | JWT G3 | Dispatch confirm modal fragment |
| POST | `/api/v1/group/{group_id}/adm/scholarship-exam/paper-builder/dispatch/{paper_id}/branch/{branch_id}/` | JWT G3 | Dispatch paper to single branch |
| POST | `/api/v1/group/{group_id}/adm/scholarship-exam/paper-builder/dispatch/{paper_id}/all-branches/` | JWT G3 | Bulk dispatch paper to all branches |
| GET | `/api/v1/group/{group_id}/adm/scholarship-exam/paper-builder/version-history/` | JWT G3+ | Paper version history list |
| GET | `/api/v1/group/{group_id}/adm/scholarship-exam/paper-builder/papers/{paper_id}/compare/` | JWT G3+ | Version comparison diff data |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| KPI bar initial load and auto-refresh | `load, every 5m` | GET `.../paper-builder/kpis/` | `#paper-builder-kpi-bar` | `innerHTML` |
| Paper status table load | `load` | GET `.../paper-builder/papers/` | `#paper-status-table-wrapper` | `innerHTML` |
| Paper status filter change | `change` | GET `.../paper-builder/papers/?{filters}` | `#paper-status-table-body` | `innerHTML` |
| Table pagination click | `click` | GET `.../paper-builder/papers/?page={n}&{filters}` | `#paper-status-table-wrapper` | `innerHTML` |
| `[Build →]` or `[Edit →]` click | `click` | GET `.../paper-builder/papers/{paper_id}/workspace/` | `#paper-builder-workspace` | `innerHTML` |
| Save draft in workspace | `click` | PATCH `.../paper-builder/papers/{paper_id}/` | `#workspace-status-badge` | `innerHTML` |
| Add section | `click` | POST `.../paper-builder/papers/{paper_id}/sections/` | `#section-list` | `beforeend` |
| Remove section | `click` | DELETE `.../paper-builder/papers/{paper_id}/sections/{section_id}/` | `#section-card-{section_id}` | `outerHTML` |
| Add question (manual) | `click` | POST `.../sections/{section_id}/questions/` | `#selected-questions-{section_id}` | `innerHTML` |
| Remove question | `click` | DELETE `.../sections/{section_id}/questions/{q_id}/` | `#selected-questions-{section_id}` | `innerHTML` |
| Auto-select preview | `click` | POST `.../sections/{section_id}/auto-select/preview/` | `#auto-select-preview-list` | `innerHTML` |
| Auto-select accept | `click` | POST `.../sections/{section_id}/auto-select/accept/` | `#selected-questions-{section_id}` | `innerHTML` |
| Quality check run | `click` | GET `.../papers/{paper_id}/quality-check/` | `#quality-checker-panel` | `innerHTML` |
| Quality check live refresh (on question change) | `click from:.question-add-btn, click from:.question-remove-btn` | GET `.../papers/{paper_id}/quality-check/` | `#quality-checker-panel` | `innerHTML` |
| Submit for review | `click` | POST `.../papers/{paper_id}/submit/` | `#paper-status-table-wrapper` | `innerHTML` |
| Approval queue auto-refresh | `load, every 5m` | GET `.../paper-builder/approval-queue/` | `#approval-queue-table` | `innerHTML` |
| `[Approve →]` in queue | `click` | POST `.../papers/{paper_id}/approve/` | `#approval-queue-table` | `innerHTML` |
| `[Return with Feedback]` click | `click` | GET `.../papers/{paper_id}/return-form/` | `#approval-return-modal` | `innerHTML` |
| Return modal `[Return Paper]` submit | `click` | POST `.../papers/{paper_id}/return/` | `#approval-queue-table` | `innerHTML` |
| `[Preview Paper]` click | `click` | GET `.../papers/{paper_id}/preview/` | `#paper-preview-drawer` | `innerHTML` |
| Dispatch manager table load | `load` | GET `.../paper-builder/dispatch/` | `#dispatch-manager-table` | `innerHTML` |
| Single `[Dispatch →]` click | `click` | POST `.../dispatch/{paper_id}/branch/{branch_id}/` | `#dispatch-row-{branch_id}` | `outerHTML` |
| Version history reveal | `revealed` | GET `.../paper-builder/version-history/` | `#version-history-section` | `innerHTML` |
| `[Compare →]` click | `click` | GET `.../papers/{paper_id}/compare/?v1={v}&v2={v}` | `#version-compare-drawer` | `innerHTML` |
| Re-roll auto-selection | `click from:#btn-reroll-autoselect` | POST `.../scholarship-exam/paper-builder/{paper_id}/auto-select/` | `#auto-select-preview` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
