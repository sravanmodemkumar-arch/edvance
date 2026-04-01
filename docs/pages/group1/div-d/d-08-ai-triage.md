# D-08 — AI-Generated MCQ Triage

> **Route:** `/content/ai-triage/`
> **Division:** D — Content & Academics
> **Primary Roles:** Content Director (18) — full access including batch reject · Question Reviewer (28) — screen only, no batch-reject-all
> **File:** `d-08-ai-triage.md`
> **Priority:** P1 — Required before Div C C-15 AI pipeline goes live
> **Status:** ⬜ Not started

---

## 1. Page Name & Route

**Page Name:** AI-Generated MCQ Triage
**Route:** `/content/ai-triage/`
**Part-load routes:**
- `/content/ai-triage/?part=kpi` — KPI strip
- `/content/ai-triage/?part=batch-selector` — batch dropdown refresh
- `/content/ai-triage/?part=triage-table&batch_id={uuid}` — triage question table for selected batch
- `/content/ai-triage/?part=drawer&question_id={uuid}` — AI question triage drawer

---

## 2. Purpose (Business Objective)

The AI pipeline (Div C C-15) generates 500–2,000 MCQs per batch using LLM models (Claude Sonnet 4.6, GPT-4o, Gemini 1.5 Pro) targeting Indian competitive exam content. These AI-generated questions are raw material — not finished products. The hallucination rate on Indian exam content is approximately 15%, meaning roughly 1 in 7 AI-generated questions contains a factual error, incorrect answer key, fabricated statistic, or off-syllabus content.

D-08 is the mandatory human screening gate between AI generation and the review queue. No AI question enters D-03 without a human triager (Content Director or Reviewer) explicitly accepting it. The AI pipeline's purpose is to accelerate content production — not to bypass quality — and D-08 is the architectural enforcement of that principle.

The acceptance rate signal from D-08 feeds back to Div C C-16 (AI Cost Monitor) as a quality signal per batch. If a batch has 40% acceptance (vs the expected 85%), that signals a prompt quality issue in C-15 — reducing the cost-per-approved-question dramatically by fixing the upstream problem.

**Business goals:**
- Mandatory human gate: no AI question enters review queue without explicit human accept/edit/reject decision
- Surface AI flags prominently (Hallucination Risk, Possible Duplicate, Off-Syllabus, Copyright Risk) to guide human decisions
- Enable Director-level batch operations (Accept All Clean, Reject All Flagged) for throughput
- Feed acceptance rate back to C-16 as quality signal
- Track rejection reasons to inform C-15 prompt and threshold improvements

---

## 3. User Roles

| Role | Access |
|---|---|
| Content Director (18) | Full — all per-row actions + batch actions (Accept All Clean, Reject All Flagged) |
| Question Reviewer (28) | Screen only — per-row Accept, Edit+Accept, Reject. No batch-reject-all. |

---

## 4. Section-Wise Detailed Breakdown

---

### Section 1 — Page Header

- H1: "AI-Generated MCQ Triage"
- Role label
- "Integration: Div C C-15 AI Pipeline → D-08 → D-03 Review Queue" — a subtle breadcrumb showing where this data comes from and where it goes
- Link: "View AI Pipeline Dashboard →" (links to C-15 in Div C — Engineering). Read-only for non-engineering roles; shown for context.

**Active Threshold Panel (collapsible, shown by default for Content Director — collapsed by default for other roles):**

A read-only summary of the current AI triage thresholds that govern auto-rejection and duplicate flagging. This gives the Director immediate context when triage results seem off (high auto-rejection rate or suspicious duplicate flags).

```
Current AI Triage Thresholds (configured in D-20 Content Configuration)
───────────────────────────────────────────────────────────────────────
Auto-Rejection:
  Language Quality     Auto-reject if score < 15%    [threshold: 85%]
  Factual Accuracy     Auto-reject if score < 10%    [threshold: 90%]
  Formatting           Auto-reject if score < 5%     [threshold: 95%]
  Bloom's Mismatch     Auto-reject if score < 20%    [threshold: 80%]

Duplicate Detection:
  Flag Threshold       ≥ 0.85 cosine similarity       [flagged in triage]
  Confirmed Duplicate  ≥ 0.95 cosine similarity       [auto-rejected]

Last Updated: 15 March 2026 by Content Director
```

**"Edit Thresholds →"** link (Content Director only): navigates to D-20 Tab 3 — AI Triage Thresholds. The panel includes this link so the Director does not need to know that D-20 is where thresholds are managed — discovery is in-context.

---

### Section 2 — KPI Strip

| Tile | Metric | Notes |
|---|---|---|
| Total in Triage | COUNT of all questions in `content_ai_question_queue` with `state: AWAITING_HUMAN` | — |
| Accepted Today | COUNT of Accept + Edit+Accept decisions today | — |
| Rejected Today | COUNT of Reject decisions today | — |
| Acceptance Rate (This Batch) | (Accept + Edit+Accept) / Total screened in selected batch × 100% | Amber if < 70% · Red if < 50% — signals prompt quality issue |
| Avg AI Confidence Score | Average confidence score across all questions in selected batch | Low confidence = more likely to contain errors |
| Auto-Rejected (Pipeline) | COUNT of questions rejected by C-15's automatic pipeline before reaching human triage (hallucination score, duplicate, formatting rules) | Shows the pipeline's pre-filter effectiveness |

---

### Section 3 — Batch Selector

**Purpose:** AI batches are discrete generation jobs — each with a specific model, prompt version, exam domain, and generation date. The triager selects which batch they are working through.

**Batch dropdown:**
Dropdown lists all AI generation batches with pending or recently completed triage — newest first.

Per dropdown option:
- Batch ID (short UUID)
- Model: Claude Sonnet 4.6 / GPT-4o / Gemini 1.5 Pro
- Prompt version: e.g. "v1.4.2"
- Exam domain / Subject: e.g. "SSC CGL Mathematics"
- Generation date
- Total questions: N
- Auto-rejected (pre-human): N (by pipeline thresholds)
- Awaiting human: N
- Accepted: N
- Rejected: N
- Acceptance rate: N%

Selecting a batch updates the triage table via `?part=triage-table&batch_id={uuid}`.

---

### Section 4 — Triage Table

**Purpose:** Row-by-row review of all questions in the selected batch that reached human triage.

**Table columns:**

| Column | Description |
|---|---|
| # | Row number within batch |
| Question (truncated) | First 100 chars — click to open triage drawer |
| Subject | — |
| Topic | AI-assigned topic (from C-15 prompt) |
| Difficulty | AI-assigned difficulty |
| AI Confidence Score | 0–100. Visual: green ≥ 75 · amber 50–74 · red < 50 |
| AI Flags | Comma-separated flag badges (see below) |
| Days in Triage | Days since batch arrived in D-08 |
| Status | Awaiting Review / Accepted / Edited+Accepted / Rejected |

**AI Flag types:**
- 🔴 Hallucination Risk — AI confidence score below threshold or specific hallucination detector triggered
- 🟠 Possible Duplicate — cosine similarity ≥ 0.75 with existing question (less strict than the 0.80 threshold in D-02/D-07 — used as an early warning flag here)
- 🟡 Formatting Issue — LaTeX syntax invalid, option count wrong, explanation too short
- 🟡 Off-Syllabus — AI prompt domain mismatch detected (e.g. AI generated a Calculus question for an SSC CGL batch that doesn't include Calculus)
- 🟠 Copyright Risk — AI reproduced text that matches a known copyright-protected source

**Sort:** Default — Flagged rows at bottom (clean questions shown first for fast Accept All Clean batch action), then by AI Confidence Score descending within each group.

**Filters:**
- AI Flags: All / Clean (No Flags) / Flagged (Any Flag) / specific flag type
- Status: Awaiting / Accepted / Rejected
- Confidence Score: ≥ N (slider)
- Subject

**Per-row actions:**
- **"Accept"** — question accepted as-is. State → `ACCEPTED`. Creates a `content_question` record in `UNDER_REVIEW` state with `ai_source: true`, attributed to the triager as reviewer-proxy (not as author — the AI is not a user). Enters D-03 Review Queue with "AI" source badge.
- **"Edit + Accept"** — opens the triage drawer's Edit mode (identical to D-02 edit view — full subject-specific toolbar). SME makes corrections to the AI content (fixes the wrong answer, corrects the explanation, updates the topic tag). On save: creates `content_question` record in `UNDER_REVIEW` with `ai_source: true, ai_edited: true`. Enters D-03 with "AI-Edited" badge.
- **"Reject"** — opens a rejection reason selector (inline sub-form):
  - Reason: Factual Error · Hallucination · Duplicate · Off-Syllabus · Poor Quality · Copyright Risk
  - Optional comment (max 300 chars) — logged for prompt feedback
  - "Confirm Reject" → state → `REJECTED` · rejection reason + comment logged in `content_ai_triage_log` · this data flows back to C-16 as quality signal and C-15 for prompt analysis

---

### Section 5 — Triage Drawer

**Trigger:** Row click. 720px right-side drawer.

**Drawer header:**
- AI Confidence Score (large, colour-coded)
- AI Flags (all badges displayed prominently)
- Model: "Claude Sonnet 4.6 · Prompt v1.4.2"
- Subject · Topic (AI-assigned)

**Drawer tabs:**

**Tab 1: AI Question Preview (default)**
Full subject-specific rendering — LaTeX rendered, code blocks highlighted, etc. This is what the human triager evaluates. Below the question:
- AI Confidence breakdown (if available from C-15): per-dimension confidence scores (Factual Accuracy / Answer Correctness / Language Quality / Exam Alignment)

**Tab 2: AI Flags + Confidence**
Detailed explanation of each AI flag triggered for this question:
- Per flag: flag type · triggering condition · what the human should check
- "Hallucination Risk: Confidence score 42/100. The AI model flagged uncertainty in the answer key. Verify: is Option C definitely correct? Check primary source."
- "Possible Duplicate: 78% cosine similarity with Question ID `abc...`. Compare with the matched question below."
- Matched question preview (for Possible Duplicate flag) — full question text of the matched question for comparison

**Tab 3: Drawer Actions**
Three action buttons (same as per-row actions but in the drawer for more deliberate decision-making):
- "Accept" (green) — with a checkbox: "Correct topic tag" if the AI's topic assignment is wrong — Corrected Topic dropdown appears; correction is applied before accepting.
- "Edit + Accept" — triggers full D-02-style editor within the drawer (same implementation as D-02 standalone question editor, loaded in the drawer's right panel with the AI question pre-filled). SME corrects and saves. On save: accepted with `ai_edited: true`.
- "Reject" — rejection reason selector (same as per-row).

---

### Section 6 — Batch Actions (Content Director Only)

**Purpose:** Director-level throughput tools for managing large batches when individual screening would be too slow.

**"Accept All Clean" button (Director only):**
- Selects all rows with NO AI flags in the current batch (up to 200 at once)
- Confirmation modal: "Accept {N} clean questions from this batch? They will enter the D-03 Review Queue."
- On confirm: Celery async task creates `content_question` records for all clean rows in `UNDER_REVIEW` state with `ai_source: true`
- Live progress bar: "Accepting… 89 / 200 complete"
- Use case: a high-quality batch (prompt v1.4.2, Claude Sonnet 4.6) where clean questions have been historically reliable — Director bulk-accepts the clean subset and manually reviews flagged rows

**"Reject All Flagged" button (Director only):**
- Selects all rows with any AI flag in the current batch
- Reason category required (applies to all rejected rows)
- Confirmation: type "REJECT" + count displayed: "Reject {N} flagged questions from this batch?"
- On confirm: Celery task marks all flagged rows as `REJECTED` with the specified reason
- Use case: a bad batch with high hallucination rate (e.g. 40% flagged) — Director rejects all flagged rows in bulk and feeds back to C-15 for prompt investigation

**Batch-level acceptance rate warning:**
If after completing triage, the batch acceptance rate < 60%, a banner appears: "This batch has a {N}% acceptance rate. Consider reviewing C-15 prompt configuration for this exam domain." with a link to C-15.

---

## 5. Data Models

### `content_ai_question_queue` (populated by Div C C-15 AI pipeline)
| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `batch_id` | FK → content_ai_batch | — |
| `question_body` | text | Raw AI-generated question body |
| `option_a` · `option_b` · `option_c` · `option_d` | text | AI-generated options |
| `correct_option` | varchar | AI-predicted answer key |
| `explanation` | text | AI-generated explanation |
| `subject_id` | FK → content_taxonomy_subject | AI-assigned |
| `topic_id` | FK → content_taxonomy_topic | AI-assigned |
| `difficulty` | varchar | AI-assigned |
| `exam_types` | varchar[] | From batch prompt config |
| `ai_confidence_score` | int | 0–100 |
| `ai_flags` | varchar[] | List of flag codes |
| `state` | varchar | AWAITING_HUMAN · ACCEPTED · EDITED_ACCEPTED · REJECTED |
| `triaged_by` | FK → auth.User | Nullable — triager |
| `triaged_at` | timestamptz | Nullable |
| `created_question_id` | FK → content_question | Nullable — populated on Accept/Edit+Accept |

### `content_ai_batch` (created by Div C C-15)
| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `model_id` | varchar | claude-sonnet-4-6 / gpt-4o / gemini-1.5-pro |
| `prompt_version` | varchar | e.g. "v1.4.2" |
| `exam_domain` | varchar | SSC CGL · UPSC Prelims · etc. |
| `subject_id` | FK → content_taxonomy_subject | — |
| `total_generated` | int | — |
| `auto_rejected` | int | Rejected before human triage by pipeline thresholds |
| `awaiting_human` | int | Reached D-08 queue |
| `created_at` | timestamptz | When batch generation completed |

### `content_ai_triage_log`
| Field | Type | Notes |
|---|---|---|
| `queue_item_id` | FK → content_ai_question_queue | — |
| `batch_id` | FK → content_ai_batch | — |
| `decision` | varchar | Accepted · EditedAccepted · Rejected |
| `rejection_reason` | varchar | Nullable |
| `rejection_comment` | text | Nullable |
| `triager_id` | FK → auth.User | — |
| `is_batch_action` | boolean | Whether triggered by Accept All Clean / Reject All Flagged |
| `created_at` | timestamptz | — |

---

## 6. Access Control

| Gate | Rule |
|---|---|
| Page access | `PermissionRequiredMixin(permission='content.triage_ai_questions')` — Roles 18 + 28 |
| Batch actions | `request.user.has_perm('content.batch_reject_ai_questions')` — Role 18 only. Checked server-side; "Accept All Clean" and "Reject All Flagged" buttons hidden for Reviewer. |
| Reject confirmation | "REJECT" text confirmation checked server-side for batch reject |

---

## 7. Edge Cases & Error States

| Scenario | Behaviour |
|---|---|
| Two triagers simultaneously accept the same AI question row | First accept creates the `content_question` record successfully. Second accept finds `state != AWAITING_HUMAN` — server returns 409: "This question was just accepted by another reviewer. It will now appear in the Review Queue." |
| Batch acceptance rate is 0% (entire batch rejected) | C-16 receives 0% acceptance rate for this batch. Alert triggers in C-16 API Rate Limits / Cost Monitor — high wasted spend event logged. C-15 pipeline config team is notified. |
| C-15 sends a batch with questions in a subject not covered by any current SME | Questions enter triage. Director triages — if accepted, they enter D-03. D-03 routing assigns to whichever Reviewer is available (D-15 assignment has a catch-all configuration for subjects with no primary reviewer). |
| AI question has LaTeX in the question body that MathJax cannot render | Preview tab shows "LaTeX rendering error" below the question. Triager can either Edit+Accept to fix the LaTeX, or Reject with "Formatting Issue" reason. |
| Batch has 2,000 questions — triager works through 200 today | Batch remains in "In Progress" state. Remaining 1,800 stay `AWAITING_HUMAN`. Next triager session continues from where they left off. Batch is shown in the dropdown with current counters. |

---

## 8. Integration Points

| Integration | Direction | What Flows | Mechanism |
|---|---|---|---|
| Div C C-15 AI Pipeline | C-15 → D-08 | AI-generated question batches | C-15 Celery task writes to `content_ai_question_queue` after generation + auto-rejection |
| Div C C-16 AI Cost Monitor | D-08 → C-16 | Acceptance rate per batch (quality signal) | `content_ai_triage_log` table read by C-16 for wasted spend + quality analysis |
| D-03 Review Queue | D-08 → D-03 | Accepted AI questions enter review queue | Accept action creates `content_question` in `UNDER_REVIEW` with `ai_source: true` |
| D-05 Director Dashboard | D-05 reads D-08 | AI Pipeline Summary widget reads D-08 queue depth + acceptance rate | `content_ai_question_queue` + `content_ai_batch` ORM queries |

---

---

## 9. UI Patterns & Page-Specific Interactions

### Search
- Placeholder: "Search questions by keyword or topic…".
- Searches: question body (first 150 chars), AI-assigned topic, exam domain.
- Debounced 300ms. Results update triage table in place.

### Sortable Columns — Triage Table
| Column | Default Sort |
|---|---|
| AI Confidence Score | **DESC (high confidence first)** — default (clean questions first) |
| Days in Triage | DESC |
| Subject | ASC |
| AI Flags | Custom: Flagged → Clean |
| Difficulty (AI-assigned) | Custom: Hard → Medium → Easy |

### Pagination
- Triage table: 50 rows per page, numbered controls.
- Batch selector dropdown: batches shown newest first. If > 20 batches, dropdown has a search filter inside it.

### Empty States
| State | Heading | Subtext |
|---|---|---|
| No batch selected | "Select a batch to begin triage" | "Choose an AI generation batch from the dropdown to see questions awaiting human review." |
| Batch is empty | "No questions awaiting triage" | "All questions in this batch have been accepted, rejected, or are auto-rejected." |
| No batches exist | "No AI batches received yet" | "AI-generated question batches from the Div C pipeline will appear here." |
| All questions in batch resolved | "Batch complete ✓" | "All questions in this batch have been triaged. Review the batch statistics below." |

### Toast Messages
| Action | Toast |
|---|---|
| Accept question | ✅ "Accepted — sent to Review Queue" (Success 4s) |
| Edit + Accept | ✅ "Edited and accepted — sent to Review Queue" (Success 4s) |
| Reject question | ✅ "Rejected — reason logged" (Success 4s) |
| Accept All Clean (Director) | ✅ "Accepted {N} clean questions — sent to Review Queue" (Success 4s) |
| Reject All Flagged (Director) | ✅ "Rejected {N} flagged questions" (Success 4s) |
| Acceptance rate < 60% alert | ⚠ "Acceptance rate is {N}% — below threshold. Review AI prompt config." (Warning persistent) |
| Batch actions require "type REJECT" | ❌ "Type REJECT in the confirmation field to proceed" (Error inline in modal) |

### Loading States
- Triage table: 8-row skeleton on batch select and filter apply.
- KPI strip: tile shimmer rectangles.
- Edit+Accept drawer: 5-line skeleton while D-02-style editor loads. MathJax renders after form load.
- Batch selector: spinner in dropdown while batch list loads.
- "Accept All Clean" Celery task: progress bar "Accepting {N} of {total} questions…" polled every 2s.

### Responsive Behaviour
| Breakpoint | Behaviour |
|---|---|
| Desktop | Triage table full columns. Batch selector wide dropdown. Drawer 720px. |
| Tablet | Table: Question preview (truncated), Subject, Confidence Score, Flags, Action — others hidden. Drawer 80% width. |
| Mobile | Table: Question preview (2 lines), Flags badge, Action buttons (Accept/Reject icons). Drawer full screen. Edit+Accept editor stacks vertically. |

### Charts
- **Batch Statistics panel (below triage table):** Donut chart — Accepted / Rejected / Auto-Rejected / Pending percentages for selected batch. Click any segment to filter table to that subset.
- **Acceptance Rate Trend:** Line chart (last 10 batches) — acceptance rate % per batch. Helps Director see whether AI quality is improving or degrading. No-data: "Review 2+ batches to see trend."

### Role-Based UI
- "Accept All Clean" and "Reject All Flagged" batch action buttons: **Content Director only**. Question Reviewer sees these buttons greyed with tooltip "Only the Content Director can perform batch triage actions."
- Individual Accept / Edit+Accept / Reject: both Director and Reviewer.
- Rejection reason logging: both roles. Director can add optional batch-level note on "Reject All Flagged".

---

*Page spec complete.*
*Gap amendments: Gap 12 (AI threshold visibility — Active Threshold Panel in Section 1 page header, read-only display of current D-20 thresholds, "Edit Thresholds →" link to D-20 Tab 3)*
*Next file: `d-09-taxonomy.md`*
