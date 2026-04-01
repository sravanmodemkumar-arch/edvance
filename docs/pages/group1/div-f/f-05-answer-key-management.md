# F-05 — Answer Key & Objections Management

> **Route:** `/ops/exam/answer-key/`
> **Division:** F — Exam Day Operations
> **Primary Role:** Results Coordinator (36) — full control over publication and objection decisions
> **Supporting Roles:** Exam Config Specialist (90) — read (for paper reference); Exam Integrity Officer (91) — read (review integrity-flagged objections); Exam Ops Manager (34) — read + approve
> **File:** `f-05-answer-key-management.md`
> **Priority:** P1 — Post-exam workflow; critical for result accuracy after objection review

---

## 1. Page Name & Route

**Page Name:** Answer Key & Objections Management
**Route:** `/ops/exam/answer-key/`
**Part-load routes:**
- `/ops/exam/answer-key/?part=kpi` — KPI strip
- `/ops/exam/answer-key/?part=pending-keys` — pending publication tab
- `/ops/exam/answer-key/?part=published-keys` — published answer keys
- `/ops/exam/answer-key/?part=objections` — objections queue tab
- `/ops/exam/answer-key/?part=closed-objections` — closed objections
- `/ops/exam/answer-key/?part=key-drawer&id={id}` — answer key detail drawer
- `/ops/exam/answer-key/?part=objection-drawer&id={id}` — objection review drawer

---

## 2. Purpose

After an exam ends, the Results Coordinator publishes the answer key so institutions and students can verify which answers were marked correct. Institutions (and sometimes students via institution admins) can then file objections against specific questions — claiming the marked answer is wrong, multiple answers are valid, or a question has an error.

F-05 manages:
1. Answer key entry and publication (PROVISIONAL first, then FINAL)
2. Objection window management (default 72 hours from `exam_operational_config`)
3. Per-objection review workflow (Accept/Reject with reasoning)
4. When a CRITICAL objection is ACCEPTED: the system re-scores the affected exam → F-04 gets a recompute trigger

**Why PROVISIONAL → FINAL matters:**
Publishing PROVISIONAL first signals "students can check, but we're still reviewing objections." Publishing FINAL means scoring is locked and results are now authoritative. If an objection is accepted after FINAL, a revised answer key is published (REVISED status) and results are recomputed.

---

## 3. Tabs

| Tab | Label |
|---|---|
| 1 | Pending Answer Keys |
| 2 | Published Answer Keys |
| 3 | Open Objections |
| 4 | Closed Objections |

---

## 4. Section-Wise Detailed Breakdown

---

### KPI Strip

| # | KPI | Alert |
|---|---|---|
| 1 | Awaiting Answer Key | Exams completed but no answer key published; amber if > 0 |
| 2 | Objection Window Open | Active publications still accepting objections |
| 3 | Open Objections | Count unresolved; amber if > 0 |
| 4 | Accepted Objections (this month) | Count for awareness |
| 5 | Objection Window Closing Soon | Publications with window closing in < 6h; amber |
| 6 | Pending Rescoring | Count where accepted objection triggered rescoring but not yet done |

---

### Tab 1 — Pending Answer Keys

Exams completed (or ACTIVE with answer key ready for pre-staging) that do not have an PROVISIONAL or FINAL answer key published.

#### Pending Table

| Column | Sortable | Notes |
|---|---|---|
| Exam | Yes | Exam name |
| Institution | Yes | — |
| Exam Type | No | — |
| Paper Code | No | `exam_question_paper.paper_code` |
| Completed At | Yes (default: ASC) | — |
| Questions | No | Total question count from paper |
| Key Status | No | `DRAFT` · `PENDING_REVIEW` · No key yet |
| Actions | — | [Create/Edit Key] · [Publish Provisional] |

**[Create/Edit Key]:** opens Answer Key Editor Drawer (760px).

**[Publish Provisional]:** only shown when key status = `PENDING_REVIEW` and all questions have answers entered. Opens Publish Confirmation Modal.

---

### Answer Key Editor Drawer (760px)

**Header:** Exam name + Paper code + Status pill + [×]

#### Section A — Answer Key Grid

One row per question in the paper. **If the paper has sections, questions are grouped by section** (collapsible section headers, matching the paper's `sections_config`):

```
▼ Section 1 — General Intelligence (25 questions · 50 marks)
  Q1 · Q2 · Q3 … Q25

▼ Section 2 — General Awareness (25 questions · 50 marks)
  Q26 · Q27 … Q50
```

Each section header shows: section name · question count · total marks · section-level average (read-only, post-computation).

| Column | Notes |
|---|---|
| Q# | Question number (continuous across sections, e.g. Q1–Q200) |
| Correct Option | Select: A · B · C · D · E (or custom options) — editable |
| Marks Awarded | Number (default from paper config; editable per question) |
| Marks for Wrong | Number (negative marking — default from exam schedule config) |
| Marks if No Attempt | Number (default 0) |
| Status | `DRAFT` · `CONFIRMED` |
| Objection Count | Count of filed objections for this question (shown after key published; amber badge if > 0) |
| Actions | [Mark Confirmed] · [Flag for Review] |

**Bulk actions:** Select all → [Set All Marks to {X}] · [Set All Negative to {Y}]

**Bulk marks validation:** If coordinator sets all marks to 0: confirmation dialog: "Setting all marks to 0 means no student can earn any points. Confirm?" If any individual question has `marks_awarded = 0` at publish time: warning shown: "Q{#} has 0 marks — students answering correctly receive no points. Review before publishing."

**Import Answer Key (CSV):** [Import CSV] button. Format: `question_number,correct_option,marks_awarded,marks_for_wrong`. Validates on upload; preview before import.

**[Save Draft]** → saves without publishing. ✅ "Answer key saved as draft" toast 4s.

#### Section B — Key Summary

- Total questions: {N}
- Answered (confirmed): {N} of {N}
- Unanswered: {N} — highlighted red if any exist before publish

#### Section C — Publish Controls

**Pre-publish validation:**
- All questions must have correct_option set
- All marks_awarded must be ≥ 0
- Total marks must equal `exam_question_paper.total_marks`

**Answer key editing after PROVISIONAL publish:** Once `status = PROVISIONAL`, the grid is read-only. [Save Draft] disabled with tooltip: "Published answer key cannot be edited. Use [Edit Key] to create a new draft, then publish it as a revised key." Published key remains visible to institutions during objection window; draft can be prepared alongside it.

**[Publish Provisional Answer Key]:** enables when all validation passes. Opens confirmation modal.

**Provisional banner message** (shown to institutions after publish): "This is a provisional answer key. Objections can be filed until {objection_window_close_at}. Final answer key will be published after objection review."

**[Mark as Final]:** available when `status = PROVISIONAL` and objection window closed. Opens confirmation modal. After marking FINAL, no new objections accepted.

**[Publish Revised Key]:** available when `status = FINAL` and a new draft was prepared (due to accepted objection). Reopens objection window for {N} hours (configurable). Triggers rescoring task.

**[View Key Diff]** — available when status = REVISED or when a draft exists alongside a published key. Opens a 560px modal showing a diff table:

| Q# | Previous Answer | New Answer | Change Reason |
|---|---|---|---|
| Q15 | B | C | Objection accepted — option B incorrect as per NCERT reference |
| Q32 | A | CANCELLED | Question had printing error — full marks to all |

Green = new (added/changed); red = previous. Useful for audit and institution communication.

---

### Tab 2 — Published Answer Keys

All published answer keys (PROVISIONAL, FINAL, REVISED).

#### Published Keys Table

| Column | Sortable | Notes |
|---|---|---|
| Exam | Yes | — |
| Institution | Yes | — |
| Status | No | PROVISIONAL · FINAL · REVISED |
| Published At | Yes (default: DESC) | — |
| Objection Window | No | Open / Closed + datetime |
| Total Objections | No | Count |
| Accepted | No | Count |
| Rejected | No | Count |
| Actions | — | [View Key] · [View Objections] · [Extend Window] · [Mark Final] |

**[Extend Window]:** extends `objection_window_close_at` by N hours (input). Requires reason. Logs action.

---

### Tab 3 — Open Objections

All unresolved objections across all published answer keys.

#### Filter Bar

| Filter | Control |
|---|---|
| Exam | Searchable select |
| Institution | Searchable select |
| Objection Type | Multi-select |
| Priority | Auto-sorted by: WRONG_ANSWER (highest) → MULTIPLE_CORRECT → QUESTION_ERROR → OTHER |
| Date Filed | Date range |

#### Objections Table

| Column | Sortable | Notes |
|---|---|---|
| ID | No | Auto-ref |
| Exam | Yes | — |
| Institution | Yes | — |
| Q# | No | Question number |
| Objection Type | No | — |
| Description (excerpt) | No | First 80 chars |
| Supporting Doc | No | 📎 if attached |
| Filed At | Yes | — |
| Window Closes | Yes | Countdown if < 12h |
| Status | No | OPEN · UNDER_REVIEW |
| Actions | — | [Review] · [Quick Accept] · [Quick Reject] |

**[Quick Accept] / [Quick Reject]:** one-click with mandatory reason input inline. No drawer needed for simple cases.

**[Review]:** opens Objection Review Drawer (640px).

---

### Objection Review Drawer (640px)

**Header:** Exam + Q# + Objection Type + Status pill + [×]

#### Section A — Objection Details

| Field | Notes |
|---|---|
| Institution | — |
| Question Number | With link to question in paper (read-only view) |
| Objection Type | — |
| Description | Full text |
| Supporting Document | Download link (presigned S3 URL, 15 min expiry) — if attached |
| Filed At | — |

#### Section B — Current Answer Key Entry

| Field | Value |
|---|---|
| Correct Option (current) | A / B / C / D |
| Marks Awarded | {X} |
| Marks for Wrong | {Y} |
| Published Status | PROVISIONAL / FINAL |

#### Section C — Review Decision

| Field | Required | Notes |
|---|---|---|
| Decision | Yes | Radio: ACCEPT · REJECT |
| Corrected Option (if ACCEPT) | Conditional | Required if ACCEPT + objection type = WRONG_ANSWER / MULTIPLE_CORRECT |
| Review Notes | Yes | Min 20 chars — rationale required |

**When ACCEPT selected:**
- If `objection_type = WRONG_ANSWER`: shows "New correct answer" field (select corrected option)
- If `objection_type = MULTIPLE_CORRECT`: shows "Award marks to:" radio with three options: "Option A only (reject partial claim)" / "Option A AND B — both correct (award marks to students who chose either)" / "Cancel question — full marks to all". On selecting "Option A AND B": records `exam_answer_key_entry.multiple_correct_options = ['A', 'B']`. Rescoring awards marks to students who chose A OR B.
- If `objection_type = QUESTION_ERROR`: shows "Mark as cancelled?" toggle — cancelled questions award full marks to all students

**Question cancellation retroactive scoring:** When a question is marked `is_cancelled = True` (via accepted objection or manual action), the rescoring Celery task automatically: (1) sets `exam_answer_key_entry.is_cancelled = True`, (2) recomputes all scores — awards `marks_awarded` to every student for that question regardless of their response, (3) recomputes ranks. Previous scores are fully replaced; no partial or additive patching.

**Duplicate objection on same question:** Before accepting an objection, the system checks for another ACCEPTED objection for the same question in the same exam. If found: "Q{#} already has an accepted objection (decision: {answer_change}). Accept this objection too? The most recent accepted decision will take effect." Both objections link to a single rescoring run (deduplication via `rescoring_pending_additional_changes` flag).

**[Quick Accept] / [Quick Reject]:** Row expands inline below the table — a textarea (min 20 chars, max 500 chars) + [Confirm Accept/Reject] button appears. Clicking outside collapses without saving. On confirm: sets status = ACCEPTED/REJECTED, logs reason, refreshes table row.

**[Submit Decision]** → sets `exam_answer_key_objection.status = ACCEPTED / REJECTED`. Triggers rescoring workflow if ACCEPTED. ✅ "Objection {accepted/rejected}" toast 4s.

**Rescoring workflow on ACCEPT:**
1. Updates `exam_answer_key_entry` for the affected question (correct_option or is_cancelled set)
2. Celery task `compute_exam_results` queued via `apply_async(countdown=10)` for this exam schedule
3. **De-duplication:** If a rescoring task for this `exam_schedule_id` is already PENDING or RUNNING in `exam_result_computation`, the new ACCEPT does not queue a duplicate — instead it sets a `rescoring_pending_additional_changes = True` flag on the running computation. After that computation completes, a follow-up task automatically re-runs to pick up any additional accepted objections. This ensures all accepted objections in a batch are captured in one final recomputed result.
4. `exam_result_publication.status → DRAFT` (forces re-review in F-04 before republishing)
5. In-app notification sent to Results Coordinator (36): "Answer key updated for {Exam} — rescoring triggered. Review and re-approve results in F-04 before republishing to students."

---

### Tab 4 — Closed Objections

Read-only archive of all resolved objections with decision and reasoning.

**Closed objections definition:** Tab 4 shows all objections with `status IN (ACCEPTED, REJECTED)` (both count as closed). Filters: Date resolved · Decision (Accepted/Rejected) · Exam · Objection Type. No separate "Status" column needed — all records here are closed by definition.

**Export:** [Download Objections Report CSV] — useful for SME team (Div D) to review question quality.

---

## 5. Modals

### Publish Answer Key Confirmation Modal (480px)

"Publish provisional answer key for **{Exam Name}** at **{Institution}**?

- {N} questions with answers
- Objection window: {N} hours ({N} days) — closes at {datetime} IST
- Institutions will be notified and can see the answer key immediately"

[Confirm Publish] `bg-[#6366F1]` · [Cancel]

**On confirm:** creates `exam_answer_key_publication` with status = PROVISIONAL. Sends in-app notification to institution admins. Celery task `close_answer_key_objection_window` scheduled for `objection_window_close_at`.

### Mark Final Confirmation Modal (400px)

"Mark answer key as FINAL for **{Exam Name}**?

- Objection window: **Closed** ({N} objections filed, {N} accepted, {N} rejected)
- After marking FINAL, no new objections will be accepted
- Results using this answer key are now authoritative"

[Confirm Mark Final] `bg-[#6366F1]` · [Cancel]

---

## 6. Data Model Reference

Full models in `div-f-pages-list.md`:
- `exam_answer_key_publication` — publication state
- `exam_answer_key_objection` — objection lifecycle

**`exam_answer_key_entry`** (per question):
| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `publication_id` | FK → `exam_answer_key_publication` | — |
| `question_number` | int | — |
| `correct_option` | varchar(10) | `A` · `B` · `C` · `D` · `CANCELLED` |
| `marks_awarded` | decimal | — |
| `marks_for_wrong` | decimal | Default: from exam_schedule.negative_marking_factor × marks_awarded |
| `marks_if_no_attempt` | decimal | Default 0 |
| `is_cancelled` | boolean | Default False — when question cancelled, all students get marks_awarded |
| `status` | varchar | Enum: `DRAFT` · `CONFIRMED` |
| `objection_accepted` | boolean | Default False — set when an objection modifies this entry |
| `revision_note` | text | Nullable — if revised due to accepted objection |

---

## 7. Access Control

| Gate | Rule |
|---|---|
| Page access | Results Coordinator (36), Config Specialist (90), Integrity Officer (91), Ops Manager (34), Platform Admin (10) |
| Create / edit answer key | Results Coordinator (36), Platform Admin (10) |
| Publish (provisional or final) | Results Coordinator (36), Platform Admin (10) |
| Review objections | Results Coordinator (36) |
| Accept/Reject objections | Results Coordinator (36), Platform Admin (10) |
| Extend objection window | Results Coordinator (36), Ops Manager (34) |
| Read-only | Config Specialist (90), Integrity Officer (91), Ops Manager (34) |

---

## 8. Edge Cases & Error States

| Scenario | Behaviour |
|---|---|
| Objection filed after window closed | Institution portal blocks submission. F-05 confirms: "Objection window is closed — this objection was not filed." |
| Max objections per institution reached | New objection submission blocked in institution portal. F-05 shows: "Institution X has reached the objection limit ({N}). No further objections accepted." |
| Accepted objection triggers rescore but computation fails | ❌ "Rescoring failed: {error}. Results remain at previous published state. Retry from F-04." Notification sent to Results Coordinator. |
| Two coordinators review same objection | Optimistic concurrency: first to submit wins. Second sees: "This objection was already resolved by another session." |
| Answer key published for exam with integrity hold | Publication is allowed (students need to see the key). Result publication (F-04) remains blocked by integrity hold separately. |
| Revised key published after FINAL marked | `exam_answer_key_publication.status → REVISED`. Previous FINAL key retained in history. Objection window reopened. Results Coordinator notified that rescoring is needed. |

---

## 9. UI Patterns

### Toasts

| Action | Toast |
|---|---|
| Key saved as draft | ✅ "Answer key saved as draft" (4s) |
| Provisional key published | ✅ "Provisional answer key published — objection window open until {time}" (4s) |
| Final key marked | ✅ "Answer key marked as FINAL" (4s) |
| Objection accepted | ✅ "Objection accepted — rescoring triggered" (4s) |
| Objection rejected | ✅ "Objection rejected" (4s) |
| Window extended | ✅ "Objection window extended to {time}" (4s) |

### Responsive

| Breakpoint | Behaviour |
|---|---|
| Desktop (≥1280px) | Full table; drawer 760px; answer key grid scrollable |
| Tablet | Reduced table columns; drawer full-width |
| Mobile | Card layout; answer key grid → scrollable table with sticky Q# column |

---

*Page spec complete.*
*F-05 covers: answer key creation (grid edit + CSV import) → provisional publish → objection window management → per-objection review → accept/reject → rescoring trigger → final publication.*
