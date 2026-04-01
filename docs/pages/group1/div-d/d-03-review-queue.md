# D-03 — Question Review Workspace

> **Route:** `/content/review/queue/`
> **Division:** D — Content & Academics
> **Primary Role:** Question Reviewer (Role 28)
> **Read Access:** Content Director (18) — full read of queue state; AI/ML Engineer (17) — read-only via D-08 triage handoff
> **File:** `d-03-review-queue.md`
> **Priority:** P0 — Quality Gate 1. No question reaches the Approver without passing through here.
> **Status:** ⬜ Not started
> **Amendments:** G7 (Committee Review — sequential 2-reviewer process for High Stakes questions)

---

## 1. Page Name & Route

**Page Name:** Question Review Workspace
**Route:** `/content/review/queue/`
**Part-load routes:**
- `/content/review/queue/?part=kpi` — KPI strip refresh
- `/content/review/queue/?part=table&tab={tab_name}` — question table for active tab
- `/content/review/queue/?part=drawer&question_id={uuid}` — review drawer content
- `/content/review/queue/?part=duplicate-panel&question_id={uuid}` — inline duplicate results panel

---

## 2. Purpose (Business Objective)

The Question Review Workspace is Quality Gate 1 in the two-gate publishing pipeline. No MCQ enters the Approver's queue without a Reviewer's explicit pass decision. At the scale of 15,000–20,000 new questions per month (across 9 SMEs, plus AI triage output from D-08), the Reviewer's queue is the highest-throughput quality checkpoint in the platform.

The Reviewer's job is not merely to find errors — it is to precisely characterise errors by category so that the SME understands exactly what to fix. A vague return comment generates another revision cycle. A specific return comment with the correct reason category enables a targeted fix in one revision. The design of D-03 is built around making precise, well-documented review decisions fast.

Three workload categories are kept rigorously separated in this workspace:
1. **Standard review** — new questions from SMEs entering the pipeline for the first time
2. **Amendment reviews** — questions previously published and then unpublished due to errors; these are fast-tracked and displayed with explicit priority above the standard queue
3. **Committee reviews** — High Stakes questions (G7) requiring 2 sequential reviewer passes; reviewer cannot see the second reviewer's question until the first has passed it

At 74,000 concurrent exam submissions, a wrong question that gets through a careless review session can reach every student in every institution simultaneously. The SLA framework (3 days standard · 1 day GK Current Affairs · same-day for Amendment Reviews) is enforced visually in the queue — overdue questions turn red before the Reviewer needs to be told.

**Business goals:**
- Enable fast, well-documented review decisions with minimal drawer friction
- Surface amendment reviews above standard queue (post-publish errors are highest priority)
- Enforce review SLAs via visual indicators — no manual tracking needed
- Prevent double-assignment of questions to multiple reviewers simultaneously
- Support committee review (G7) for High Stakes questions
- Provide inline duplicate checking against the published bank during review

---

## 3. User Roles

| Role | Access | What They Can Do |
|---|---|---|
| Question Reviewer (28) | Full | Self-assign questions · open review drawer · Pass to Approver · Return to SME · Flag for Committee Review · Search published bank for duplicates |
| Content Director (18) | Read | View full queue state across all subjects · see queue depth per reviewer · see stale alerts. Cannot make review decisions. |

> **Reviewer subject scope:** Question Reviewer (Role 28) reviews all subjects — no subject restriction. The reviewer assignment in D-15 routes specific subjects to specific reviewers as the primary/backup assignment, but any Reviewer can pull from the unassigned pool regardless of subject if needed. The reviewer reads the question regardless of subject — they are cross-subject experts in quality, accuracy, and language.

---

## 4. Section-Wise Detailed Breakdown

---

### Section 1 — Page Header & Status Strip

**Header:**
- H1: "Review Queue"
- Reviewer's name + "Question Reviewer" role label
- "Batch Self-Assign" button (primary) — described in Section 5
- Auto-refresh indicator: "Live · Updated 18s ago" — auto-refreshes every 30s when no drawer is open

---

### Section 2 — KPI Strip

**Purpose:** Reviewer's daily operational health at a glance.

| Tile | Metric | Colour Rule |
|---|---|---|
| Total Pending | All `UNDER_REVIEW` questions in the pool (assigned + unassigned) | — |
| Assigned to Me | Questions currently assigned to this reviewer (in `UNDER_REVIEW` with `assigned_reviewer_id = me`) | Amber if > 20 · Red if > 40 |
| Reviewed Today | Questions this reviewer passed or returned today | — |
| Avg Days in Queue | Average age of all `UNDER_REVIEW` questions currently | Amber if > 2 days · Red if > SLA for subject |
| My Return Rate (30d) | (Questions returned by me / Questions I reviewed in last 30 days) × 100% | Amber if > 40% (high return rates may indicate a systemic SME quality issue) |
| Amendment Reviews | COUNT of `AMENDMENT_REVIEW` questions in queue | Red if > 0 — always needs immediate attention |
| Committee Queue | COUNT of High Stakes questions flagged for committee review awaiting this reviewer (G7) | Amber if > 0 |

KPI strip refreshes every 30s via `?part=kpi`.

---

### Section 3 — Tab Navigation

| Tab | Badge | Description |
|---|---|---|
| Pending Review | COUNT of unassigned + assigned-to-me UNDER_REVIEW questions | Default active — standard queue |
| Amendment Reviews | COUNT — bold red if > 0 | Highest priority — fast-track queue |
| Assigned to Me | COUNT of questions assigned to this reviewer | — |
| Committee Queue | COUNT of High Stakes questions awaiting this reviewer's sequential pass (G7) | — |
| My Review History | No count badge | All decisions made by this reviewer — searchable |

---

### Section 4 — Tab: Pending Review (Default)

**Purpose:** The main working queue. All questions in `UNDER_REVIEW` state from all SMEs (across all subjects assigned to this reviewer per D-15 assignment matrix, plus unassigned questions from other subjects if pool runs low).

**Sub-tabs within Pending Review:**
- **Unassigned Pool**: questions not yet assigned to any reviewer — available for batch self-assign
- **Assigned to Me**: questions already assigned to this reviewer — their personal in-progress queue

**Unassigned Pool table columns:**

| Column | Description |
|---|---|
| # | Row number |
| Question Preview | First 100 chars of question body (LaTeX rendered inline as small inline text, not full MathJax — prevents slow rendering for 50+ rows) |
| Subject | Subject badge |
| Topic | Topic name |
| Difficulty | Easy / Medium / Hard |
| Exam Types | Comma-separated abbreviations |
| Content Type | Evergreen / Current Affairs / Time-Sensitive badge |
| SME | "SME {subject}" — role title only, not personal name (DPDPA: reviewer knows the subject, not the individual) |
| Days Waiting | Days since SME submitted. Colour: ≤ SLA = neutral · 1 day before SLA = amber · at/past SLA = red pulsing |
| SLA | Subject-specific SLA: GK Current Affairs = 1 day · All others = 3 days (configured in D-15) |
| Revision # | "×1", "×2" badges — amber at ×1, red at ×2+ |
| Source | — = human-authored · "AI" badge (blue) = came via D-08 AI Triage · "AI-Edited" = AI draft edited by SME in D-08 before accepting |
| Passage Set | — = standalone · "Set: 4Q" = part of a passage set with 4 linked questions |

**Per-row actions:**
- "Assign to Me" — atomically assigns this question to the logged-in reviewer. Uses `SELECT ... FOR UPDATE SKIP LOCKED` to prevent race condition where two reviewers simultaneously claim the same question. On success: question moves to "Assigned to Me" sub-tab. On race condition loss: "Question was just assigned to another reviewer" toast, row disappears.
- "Open" — opens review drawer without self-assigning (browse mode — Reviewer can read but cannot submit a decision without assigning first)

**Filters:**
- Subject (multi-select)
- Difficulty (multi-select)
- Content Type
- Exam Type
- Days Waiting ≥ N (show only overdue)
- Revision # ≥ 2 (show persistent problem questions)
- Source: Human / AI / AI-Edited
- SLA Status: All / Overdue / Due Today / On Track

**Sort:** Default — Amendment Reviews first (pinned), then SLA Status (Overdue first), then Days Waiting descending. User can re-sort any column.

**Pagination:** 50 rows per page with "Load More" (HTMX append).

---

### Section 5 — Batch Self-Assign

**Purpose:** Reviewer pulls a batch of questions from the unassigned pool into their personal queue in one action, rather than clicking "Assign to Me" 50 times.

**"Batch Self-Assign" button** (header):
Opens a modal:
- "How many questions to assign?" — number input, 1–50, default 20
- Filter options for the batch: Subject (default: all subjects assigned to this reviewer in D-15), Exam Type, Difficulty
- "Assign {N} Questions" button

**Assignment logic:** Backend assigns the N oldest unassigned questions (Days Waiting descending) matching the filter, using `SELECT ... FOR UPDATE SKIP LOCKED` in a single transaction — atomic assignment, no race conditions. Returns the count actually assigned (may be less than requested if pool is smaller).

**Result:** Toast notification: "20 questions assigned to your queue" + immediate HTMX refresh of the "Assigned to Me" sub-tab.

---

### Section 6 — Review Drawer

**Trigger:** Click on any question row in any tab (other than My Review History). Opens as a 720px right-side drawer with dark overlay. Auto-refresh suspended while drawer is open.

**Drawer header:**
- Question ID (UUID, truncated to last 8 chars: "…c21d")
- Status pill: "Under Review" / "Amendment Review" / "High Stakes — Committee Review Required"
- Subject + Topic + Subtopic
- Difficulty · Bloom's Level · Content Type · Access Level
- SME note (if present): shown in a light blue box — "SME Note: Reference NCERT Chemistry Ch.5 p.127"
- Revision badge: "Revision ×2" in red if applicable — with tooltip "This question has been returned 2 times. Review for systemic issues."
- AI Source badge (if applicable): "AI-Generated" or "AI-Edited by {SME role}" — distinguishes AI-origin content

**Drawer tabs:**

**Tab 1: Question Preview (default)**

Full subject-specific rendered view — exactly what students will see. No raw markdown, no LaTeX strings — fully rendered:
- Question body: MathJax for LaTeX · SVG circuit/ray diagrams rendered inline · SMILES molecular structures as images · annotated Biology diagrams · code blocks with syntax highlighting · Telugu/Hindi/Urdu text in correct script and direction
- All 4 (or more) options — fully rendered, with the correct answer marked (Reviewer must see this to verify the key is correct)
- Explanation — fully rendered

Below the rendered question:
- Tags summary: Topic · Subtopic · Difficulty · Bloom's Level · Exam Types · Content Type · Valid Until (if applicable) · Access Level · High Stakes (if flagged) · Source Attribution
- **"Check Duplicates" button** — triggers inline duplicate check panel (see Section 13)

**Tab 2: Reviewer Notes + Quick Templates**

**Free-text notes field:**
Large textarea for the reviewer to draft their return comment. Min 20 characters required if returning. Return comment is shown to the SME in D-01 and D-02 revision mode — it must be specific and actionable.

**Quick Templates (below notes field):**
Reviewer's personal library of saved return-reason templates. Each template is a pre-written comment for a common error pattern. Examples:
- "Calculation Error — Option [X] is incorrect. Working: [calculation]. Correct answer should be [Y]."
- "Off-Syllabus — This topic is not included in the SSC CGL 2024 syllabus. Reference: Notification §3.2.X."
- "Incomplete Explanation — The explanation should show the full working, not just the final answer."

Templates are personal to each reviewer (scoped to `reviewer_id`). Template selection auto-fills the notes field (reviewer then edits as needed before returning).

**In-drawer template actions:**
- **"Save as Template"** — saves the current notes field content as a new template. Opens a mini-form inline: Template Name (required, max 80 chars) + "Save". Duplicate name within the same reviewer → inline error: "You already have a template named '{name}'.".
- **"Manage Templates"** link → opens the Quick Template Manager (see Section 12).

**Tab 3 (inserted): Passage Set Context** *(only visible when question belongs to a passage set)*

When a question has a `passage_set_id`, this tab appears with full passage context:

- **Passage text:** Full rendered passage (with MathJax, tables, images) — exactly as the SME authored it.
- **All questions in the set:** Numbered list of every question in this passage set, with their current review states:
  - This question: highlighted with "← You are reviewing this"
  - Other questions: truncated preview + status badge (`UNDER_REVIEW` / `PENDING_APPROVAL` / `RETURNED` / already reviewed by this reviewer → "Passed" / "Returned" badge in green/orange)
- **"Review Together" toggle (Director config):** If enabled in D-15 per subject, the Reviewer can see all passage questions simultaneously and pass/return them as a group. When toggled ON, the action bar shows "Pass All {N}" and "Return Selected" options (see Passage Set actions below).

**Passage Set action bar additions** (when Passage Set Context tab is active):
- **"Pass All {N} Questions"**: passes every question in the set that has not already been reviewed. One confirmation: "Pass all {N} questions in this passage set?" Each question transitions individually — audit log records each pass separately.
- **"Return Selected"**: checkbox list of all passage set questions appears inline; reviewer checks which to return and fills a single return comment that applies to all selected. Each returned question gets its own `content_question_review_log` entry with the shared comment.
- **Mixed result:** Reviewer can pass some and return others — there is no requirement for the whole passage set to move together. See Edge Cases (Passage Set partial return) for downstream state handling.

**Tab 4: Return History**

Full history of all prior review cycles for this question:
- Version 1 → submitted → returned by [Reviewer name] on [date] — "Return reason: Factual Error. Comment: [full comment]"
- Version 2 → submitted → passed by [Reviewer name] on [date]
- etc.

Shows all versions in reverse chronological order. Helps the current reviewer understand the pattern: if a question was returned twice for "Calculation Error," the Reviewer knows to check arithmetic very carefully.

**Drawer action bar (bottom, always visible):**

Three actions, clearly separated:

**1. Pass to Approver** (green, primary):
One-click. No additional input required — the Reviewer's pass decision is their signature of quality. On click:
- Confirmation: inline toast "Question passed to Approver. You reviewed 7 questions today." (no modal — fast workflow)
- Question state: `UNDER_REVIEW` → `PENDING_APPROVAL`
- Assigned reviewer ID + pass timestamp logged in `content_question_audit_log`
- For committee review (G7): if this is the first reviewer pass, question goes back to unassigned committee pool (not directly to Approver). If this is the second reviewer pass: question moves to `PENDING_APPROVAL`. See Section 9.
- Drawer closes, next question in queue auto-opens if "Auto-advance" toggle is ON (Reviewer can enable: "Automatically open next question after each decision")

**2. Return to SME** (orange):
Opens an inline sub-form below the action bar (drawer stays open):
- Return reason category (required — radio group):
  - Factual Error
  - Calculation Error
  - Language / Grammar
  - Formatting
  - Incomplete Explanation
  - Duplicate
  - Off-Syllabus
  - Image Quality
  - Script Error (for Regional Language questions with Unicode issues)
- Comment field (required, ≥ 20 characters — pre-filled from Quick Template if one was active)
- "Confirm Return" button

On confirm:
- Question state: `UNDER_REVIEW` → `RETURNED`
- `return_reason_category` and `reviewer_comment` stored
- `revision_count` incremented on the question record
- In-app notification sent to the SME (D-01 Returned tab badge updates on next poll)
- Drawer closes, next question auto-opens if auto-advance is ON

**3. Flag for Committee Review** (purple — Amendment G7):
Available for any question — Reviewer can escalate any question they feel requires a second opinion from a peer reviewer, particularly for complex High Stakes content.
- Confirmation modal: "Flag for Committee Review? This question will be removed from the standard queue and placed in the committee review pool, where a second reviewer must also pass it independently before it reaches the Approver."
- On confirm: question tagged `committee_review_required: true` (if not already set via SME High Stakes flag in D-02) · removed from this reviewer's assigned queue · placed in committee review pool (Reviewer 1 has passed it; Reviewer 2 must now review it)
- If question was NOT previously flagged as High Stakes: the committee flag is logged as a "Reviewer escalation" — does not change the original SME tagging
- Full documentation in Section 9 (Committee Review — G7)

---

### Section 7 — Amendment Reviews Tab

**Purpose:** Questions previously published, then unpublished due to errors — now in `AMENDMENT_REVIEW` state. These are the highest-priority items in the entire queue. A published question error affects every student who used that question in an exam; restoring a corrected version as fast as possible is critical.

**Visual differentiation:** Tab badge is bold red when count > 0. The tab itself has an amber background. Amendment questions are shown with an amber "AMENDMENT" label in the question row — never mixed with standard pending queue.

**Additional columns vs standard queue:**

| Extra Column | Description |
|---|---|
| Previous Publish Date | When this question was originally published |
| Unpublish Reason | Category: Paper Leak / Factual Error / Copyright / Court Order / Other — from D-04 unpublish action |
| Flagged By | "Student Flags (×15)" or "Approver" or "Content Director" — the trigger for unpublishing |
| Amendment SLA | Hard 1-day SLA regardless of subject or content type. Red immediately when ≥ 24 hours in queue. |

**Review drawer for Amendment Reviews:**
Same as standard drawer but with an additional tab: **"Amendment Context"** — shows the full D-12 audit trail for this question: original publish date · who unpublished · unpublish reason · any student feedback flags that triggered unpublishing · what the SME changed in revision (diff view: old vs new question body, old vs new tags, old vs new explanation — changes highlighted green/red).

The Reviewer must understand what changed before passing an amendment review. The diff view makes this explicit.

**Pass to Approver for Amendment Reviews:** Same as standard pass, but after passing, question goes to D-04 "Amendment Reviews" tab (not the standard Pending Approval queue). Approver's mandatory 2FA re-prompt applies regardless of bulk/single (enforced at D-04 layer).

---

### Section 8 — Assigned to Me Tab

**Purpose:** The reviewer's personal in-progress queue — questions already self-assigned.

Same table structure as Pending Review, with one additional column: "Assigned On" (timestamp when self-assigned). Questions assigned > 3 days ago show a self-reminder amber indicator: "This question has been in your queue for 3 days — it may be approaching SLA."

**Release action:** Per-row "Release" button — returns the question to the unassigned pool if the Reviewer cannot complete it (e.g., subject expertise needed). Confirmation modal: "Release this question? It will return to the unassigned pool for other reviewers." No penalty — releasing is better than letting it stall.

---

### Section 9 — Committee Queue Tab (Amendment G7)

**Purpose:** Questions flagged as High Stakes — requiring 2 independent sequential reviewer passes before reaching the Approver. Handles UPSC Prelims, State Board, and any question where the SME or a prior Reviewer determined that a single reviewer pass carries too much risk.

**How Committee Review works:**

1. A question is flagged High Stakes (by SME in D-02, or by Reviewer in standard review drawer)
2. On first Reviewer's "Pass to Approver" action: question is placed in the committee pool, not directly in the Approver's queue
3. Second reviewer picks up the question from the committee pool — sees the full question but NOT the first reviewer's pass decision (they review blindly, just as in a genuine double-blind review)
4. If Second Reviewer also passes: question moves to `PENDING_APPROVAL` → enters D-04 normally
5. If Second Reviewer returns it: question goes back to `RETURNED` state with both the standard return flow. First reviewer's pass is discarded — the question must go through the full cycle again after the SME revises.

**Committee Queue table:**

| Column | Description |
|---|---|
| Question Preview | Truncated |
| Subject · Topic | — |
| High Stakes flag | "SME-Flagged" or "Reviewer-Escalated" — shows who triggered committee review |
| Committee Pass Status | "Reviewer 1: Passed" (visible to all) · "Reviewer 2: Pending" |
| First Pass Date | When Reviewer 1 passed it |
| Days Since First Pass | Time waiting for Reviewer 2 |

**Reviewer 2 assignment:** Second reviewer self-assigns from the committee pool — same atomic assignment logic as standard queue. System prevents the same reviewer from being both Reviewer 1 and Reviewer 2 on the same question (checked on assignment: if `first_reviewer_id == request.user.id` → block with message "You reviewed this question in the first pass. A different reviewer must complete the second pass.").

**Reviewer 2 drawer:** Identical to standard review drawer — full question preview, notes, quick templates, return history. The only difference: there is no "Flag for Committee Review" action (question is already in committee review). The "Pass to Approver" action completes the committee review and sends the question to D-04.

**Committee Review config:** Enabled/disabled per subject by Content Director in D-15. When disabled for a subject: High Stakes flag still works as a tag on the question, but the committee queue workflow is not triggered — question goes through single-reviewer pass as normal.

---

### Section 10 — My Review History Tab

**Purpose:** Searchable personal log of all review decisions this reviewer has made.

**Table columns:** Question ID · Subject · Topic · Difficulty · Decision (Passed / Returned / Committee-Flagged) · Return Reason (if returned) · Review Date · Revision # at time of review

**Filters:** Decision type · Subject · Date range · Return Reason Category

**"Review Statistics" summary row (top of tab):**
- 30-day: questions reviewed · pass rate · return rate · top return reason (e.g. "Factual Error × 23")
- Useful for the reviewer to see their own patterns — if they're returning 60% for "Language/Grammar", they may need to communicate a pattern to the Content Director for SME training

**No edit capability:** Review history is immutable — INSERT-only in `content_question_review_log`. Reviewers cannot change a past decision.

---

### Section 11 — Passage Set Review Context

When a question is part of a passage set (identified by `passage_set_id` on `content_question`), the queue table shows a "Set: {N}Q" badge in the Passage Set column. The review drawer opens for the individual question but exposes the Passage Set Context tab (Tab 3 above).

**Passage Set grouping logic in queue table:**
- Questions in the same passage set are grouped with an expandable row: "▶ Passage Set ({N} questions)" — clicking expands to show all N questions inline without navigating away.
- The oldest question in the set (Days Waiting DESC) is shown as the group row.
- "Assign All in Set to Me" group action: atomically assigns all unassigned questions in the set in one click. Prevents the set from being split across multiple reviewers (unless pool contention forces it — then the system assigns as many as available).

**Passage Set partial return — edge case state definition:**
If the reviewer passes some questions in a passage set and returns others:
- Passed questions: `UNDER_REVIEW` → `PENDING_APPROVAL` normally.
- Returned questions: `UNDER_REVIEW` → `RETURNED` normally — SME revises and resubmits only the returned question(s).
- D-04 Approver sees only the passed questions; the returned questions are not visible until the SME resubmits.
- When the SME resubmits the returned questions, they re-enter the review queue as individual questions, still tagged with the same `passage_set_id`. The Approver is responsible for checking passage coherence when approving the final batch (D-04 Passage Set tab shows full set completion status).
- No "passage set lock" — the set is not held together in the pipeline. This avoids blocking published questions due to one problematic question in the set.

---

### Section 12 — Quick Template Manager

**Route:** Accessible via "Manage Templates" link in the review drawer Tab 2, and via a "Templates" link in the page header (top-right, visible to Reviewers only).

**Purpose:** Full CRUD interface for the reviewer's personal return comment templates. The in-drawer experience (Tab 2) only allows Save + Delete; Template Manager adds editing and reordering.

**Layout:** Right-side panel (640px) that slides in over the queue table — not a full-page navigation. Reviewer's queue remains visible in the background.

**Template List:**

| Column | Notes |
|---|---|
| Drag handle | For reordering (drag-and-drop; order persists to `content_reviewer_quick_template.sort_order`) |
| Template Name | Editable inline on click |
| Body Preview | First 80 chars of template body |
| Return Reason | Which return reason category this template is typically used for (optional tag — for filtering) |
| Actions | Edit · Duplicate · Delete |

**Default sort:** User-defined order (sort_order ASC). Can also sort by Name ASC, Most Recently Used.

**"+ New Template" button:**
Opens an inline form at the top of the list:
- Template Name (required, max 80 chars)
- Return Reason Tag (optional — select from the standard return reason categories)
- Template Body (required, textarea, no character minimum — this is a template, not a final comment)
- "Save Template" · "Cancel"

On save: new `content_reviewer_quick_template` record created. Template immediately available in the drawer.

**Edit Template:**
Clicking "Edit" row action expands the row into an inline edit form (same fields as create). "Save" updates the record. "Cancel" discards changes.

**Duplicate Template:**
Creates a copy named "{Original Name} (copy)" — opens inline edit form for the user to rename before saving.

**Delete Template:**
Confirmation: "Delete '{Name}'? This cannot be undone." On confirm: record soft-deleted (hidden from list; retained in DB for 30 days in case of accidental deletion — not exposed in UI).

**"Import from Return History" button (top of panel):**
Scans the reviewer's past return comments (`content_question_review_log.reviewer_comment` for this reviewer) and surfaces the 10 most frequently used phrases. Reviewer can select any → pre-fills the New Template form with that text. Reduces friction to build a template library from past work.

**Validation:**
- Template Name unique per reviewer (case-insensitive) — inline error on save if duplicate.
- Max 50 templates per reviewer — if limit reached, "New Template" button is disabled with tooltip: "Template limit reached (50). Delete unused templates to create new ones."

---

### Section 13 — Inline Duplicate Check Panel

**Trigger:** "Check Duplicates" button in the review drawer's Question Preview tab.

**Purpose:** During review, the Reviewer can verify the question is not already in the published bank before passing it. The SME's autosave triggers an async duplicate check (G1 in D-02), but the Reviewer performs a fresh check at review time against the current published bank — the bank grows daily, and a question that passed duplicate check at authoring time may now have a near-duplicate that was published since.

**Panel placement:** Inline below the full question preview in the drawer (pushes down the action bar — not a modal). 480px wide, same drawer context.

**Trigger:** "Check Duplicates" → Celery task fires immediately (real-time check — not pre-cached like the D-02 autosave check). Spinner while waiting (< 5s typical for HNSW ANN search on 2M+ vectors). Results appear in the panel:

**Results format:**
- If matches ≥ 0.80 similarity found: "Top {N} matches found:" — each match shows:
  - Similarity score (e.g. "91% similar")
  - Question ID + truncated question text
  - State: Published / In Review / Draft
  - Topic + Difficulty
  - "View Full" link — opens the matched question in a read-only overlay inside the drawer
- If no matches ≥ 0.80: "No duplicates found (checked against {N} published questions)"

**Reviewer action after duplicate check:**
- If a near-duplicate is found and the Reviewer agrees it's a duplicate: use "Return to SME" with reason "Duplicate" — the reviewer's return comment should include the matched question ID so the SME can compare directly.
- If the match is found but the Reviewer judges it's a legitimate variant (different difficulty, different exam type): proceed with Pass — the "Duplicate" concern is noted in SME Notes only.

---

## 5. Data Models

### `content_question_review_log` (INSERT-only — append-only audit)
| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `question_id` | FK → content_question | — |
| `question_version` | int | The `revision_count` at time of review |
| `reviewer_id` | FK → auth.User | The reviewer |
| `decision` | varchar | Passed / Returned / CommitteeFlagged |
| `return_reason_category` | varchar | Nullable — only if Returned |
| `reviewer_comment` | text | Nullable — only if Returned |
| `committee_pass_number` | int | Nullable — 1 or 2 for committee review questions |
| `created_at` | timestamptz | Immutable — no update ever |

### `content_reviewer_quick_template`
| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `reviewer_id` | FK → auth.User | — |
| `template_name` | varchar(80) | Unique per reviewer (case-insensitive) |
| `template_body` | text | Pre-written comment |
| `return_reason_tag` | varchar | Nullable — maps to standard return reason categories |
| `sort_order` | integer | User-defined display order |
| `is_deleted` | boolean | Soft-delete — Default False |
| `last_used_at` | timestamptz | Nullable — updated each time template is applied in drawer |
| `created_at` | timestamptz | — |
| `updated_at` | timestamptz | — |
| Unique: `(reviewer_id, LOWER(template_name)) WHERE NOT is_deleted` | — | Partial unique index |

### `content_question` — additional fields relevant to review
| Field | Type | Notes |
|---|---|---|
| `assigned_reviewer_id` | FK → auth.User | Nullable — set atomically on self-assign |
| `assigned_at` | timestamptz | Nullable |
| `committee_review_required` | boolean | Default false |
| `committee_reviewer_1_id` | FK → auth.User | Nullable — first reviewer who passed it |
| `committee_reviewer_1_passed_at` | timestamptz | Nullable |
| `committee_reviewer_2_id` | FK → auth.User | Nullable |
| `return_reason_category` | varchar | Nullable — last return reason |
| `reviewer_comment` | text | Nullable — last reviewer comment |

---

## 6. Access Control

| Gate | Rule |
|---|---|
| Page access | `PermissionRequiredMixin(permission='content.review_questions')` — Role 28 + Content Director (18) |
| Content Director access | Read-only — `has_write_permission` flag False for Director. All drawer action buttons hidden via Django template `{% if can_review %}` block, not CSS alone. |
| Pass to Approver | `question.assigned_reviewer_id == request.user.id` — only the assigned reviewer can pass. Prevents passing a question they never assigned to themselves. |
| Committee — Reviewer 2 | `question.committee_reviewer_1_id != request.user.id` — enforced at assignment time and at Pass action time. |
| Return to SME | Same as Pass — only assigned reviewer. |
| Return comment length | Server-side: minimum 20 characters enforced in view. Client-side validation is UX only. |
| Audit log | `content_question_review_log` is INSERT-only at application layer — no UPDATE or DELETE route exists for this table in the codebase. |

---

## 7. Edge Cases & Error States

| Scenario | Behaviour |
|---|---|
| Two reviewers self-assign same question simultaneously | `SELECT ... FOR UPDATE SKIP LOCKED` — second reviewer sees a toast: "This question was just assigned to another reviewer." Row disappears from their view on next HTMX refresh. |
| Reviewer tries to pass a question not assigned to them | Server returns 403: "You must self-assign this question before making a review decision." |
| HTMX auto-refresh fires while reviewer is composing a return comment | Auto-refresh is suspended when any drawer is open (JS flag). Comment is never lost. |
| Question is withdrawn by Content Director while reviewer has the drawer open | Drawer shows a soft banner: "This question has been unpublished by the Content Director while you were reviewing it. It has moved to Amendment Review state." Action buttons are replaced with "Close Drawer." |
| SME edits question while it is UNDER_REVIEW | This is blocked at D-02 layer (403 if `state != DRAFT or RETURNED`). But if state changes due to a race condition: D-03 reviewer sees the content that was submitted; any post-assignment edit by the SME is impossible. |
| Reviewer 2 tries to self-assign a committee question they reviewed as Reviewer 1 | Blocked at assignment time: "You reviewed this question in the first pass. A different reviewer must complete the second pass." |
| All committee-capable reviewers have already been Reviewer 1 on this question | Edge case at low reviewer headcount. System shows: "No eligible second reviewer available — all reviewers have completed the first pass. Contact Content Director to resolve." Content Director can reassign via D-15. |
| All eligible Reviewer 2 candidates are on OOO (D-19/D-15 OOO flag set) | Committee deadlock due to OOO. System detects this at the point where Reviewer 1 passes and no eligible Reviewer 2 is available. Action: (a) Question is held in committee pool with a "COMMITTEE_DEADLOCK" sub-status. (b) Content Director receives a D-19 notification: "Committee review deadlock — no eligible Reviewer 2 is available for question {ID}. All eligible reviewers are currently OOO." (c) D-05 Director Dashboard shows a "Committee Deadlock" alert tile. (d) Director options via D-15: extend a reviewer's return date · designate an emergency backup outside the usual eligible pool (Director can manually override eligible reviewer list for this question only) · or override the committee requirement entirely for this question with a documented reason (logged to `content_question_audit_log`). |
| Passage set split across reviewers | If two reviewers each self-assign different questions from the same passage set (race condition), both can review their assigned questions independently. The Passage Set Context tab in each drawer shows the other reviewer's decisions as they complete them (live via HTMX). No hard block — independent review of passage-set questions is valid. Approver sees the full set state in D-04. |
| Amendment review SLA (1 day) breaches | Question row turns red. Content Director in D-05 Stale Alerts panel sees this and can click "Escalate" which sends an in-app notification to the assigned reviewer and their backup. |
| Reviewer submits Pass for a question where the correct answer is demonstrably wrong | This is a human judgement error — the platform cannot catch it. It is why the Approver gate (D-04) exists as the second independent check. Post-publish, D-16 student flags and D-13 quality analytics catch realized-vs-expected divergence. |

---

## 8. Integration Points

| Integration | Direction | What Flows | Mechanism |
|---|---|---|---|
| D-02 Question Editor | D-02 → D-03 | New questions on submit; revised questions on resubmit | State change to `UNDER_REVIEW`; Celery assigns reviewer |
| D-08 AI Triage | D-08 → D-03 | AI-accepted questions enter `UNDER_REVIEW` with AI source flag | Same `UNDER_REVIEW` state; `ai_source` field set |
| D-04 Approval Queue | D-03 → D-04 | Passed questions transition to `PENDING_APPROVAL` | State change; `assigned_reviewer_id` + pass timestamp logged |
| D-11 Published Bank | D-03 reads | Inline duplicate check against published questions | Celery task calls pgvector HNSW query on `content_question_embeddings` |
| D-15 Reviewer Assignments | D-15 config → D-03 | Subject-to-reviewer routing for auto-assign; SLA thresholds per subject | `content_reviewer_assignment` table read on submit (D-02) and on stale check |
| D-05 Director Dashboard | D-05 reads D-03 | Queue depth per reviewer; stale alerts; amendment review count | Same `content_question` table with state filters — no API call |
| D-12 Audit History | D-03 → D-12 | Every review decision (Pass / Return / Flag) logged immutably | INSERT into `content_question_review_log` + `content_question_audit_log` |
| D-16 Feedback Queue (G2) | D-16 → D-03 | Unpublished questions re-enter as AMENDMENT_REVIEW | State set to `AMENDMENT_REVIEW` by D-04/D-16 unpublish action |

---

---

## 9. UI Patterns & Page-Specific Interactions

### Search
- Available on all queue tabs. Placeholder: "Search questions by topic, subject, or keyword…".
- Searches: topic name, subtopic name, question body first 150 chars, SME role label.
- Debounced 300ms. Results update table in place.

### Sortable Columns — Pending Review Table
| Column | Default Sort |
|---|---|
| Days Waiting | **DESC (oldest first)** — default |
| Submitted Date | DESC |
| Subject | ASC (alphabetical) |
| Difficulty | Custom: Hard → Medium → Easy |
| Revision # | DESC |
| SLA Status | Custom: Overdue → At Risk → OK |

Default sort order: Amendment Reviews pinned at top → then by Days Waiting DESC.

### Pagination
- All tabs: 50 rows per page, numbered pagination controls.
- "Showing X–Y of N" always visible.
- "Amendment Reviews" tab: always shows full count regardless of filter (no inadvertent hiding of high-priority items).

### Empty States
| Tab | Heading | Subtext | CTA |
|---|---|---|---|
| Pending Review | "Queue is empty" | "All available questions have been assigned or are awaiting SME resubmission." | — |
| Amendment Reviews | "No amendment reviews" | "No questions are currently in fast-track amendment review." | — |
| Assigned to Me | "Nothing assigned yet" | "Assign questions from the Pending Review tab to start reviewing." | "Go to Pending Review" |
| Committee Queue | "No committee questions" | "No questions currently require 2-reviewer consensus." | — |
| My Review History | "No review history yet" | "Your Pass and Return decisions will appear here." | — |

### Row Selection for Bulk Actions
- Checkbox column (shown on hover or when ≥1 selected).
- Bulk action: "Assign Selected to Me" (max 50). Confirmation modal shows count: "Assign {N} questions to yourself?" with "Confirm" + "Cancel".
- "Select All on Page" header checkbox.
- "Select All N Results" banner if all 50 on current page selected.

### Toast Messages
| Action | Toast |
|---|---|
| Batch self-assign | ✅ "Assigned {N} questions to your queue" (Success 4s) |
| Pass to Approver | ✅ "Passed to Approver" (Success 4s) |
| Return to SME | ✅ "Returned to SME with your feedback" (Success 4s) |
| Flag for Committee Review | ✅ "Flagged for committee review — question reassigned to committee pool" (Success 4s) |
| Race condition (question already assigned) | ⚠ "This question was just assigned to another reviewer" (Warning 8s) |
| Batch assign — some failed | ⚠ "{N} of {total} questions assigned. {M} were already taken." (Warning 8s) |

### Loading States
- Queue table: 8-row skeleton on initial load, tab switch, and filter apply.
- KPI strip: tile shimmer rectangles.
- Drawer open: drawer body 5-line skeleton while question data loads.
- Duplicate check panel: "Checking for duplicates…" with animated dots. Results replace inline. Timeout 15s → "Check timed out. [Retry]".
- Auto-refresh (30s): table body fades to 60% opacity with spinner overlay. No skeleton — data already present, just refreshing.

### Responsive Behaviour
| Breakpoint | Behaviour |
|---|---|
| Desktop | Full table all columns. Drawer at 720px right panel. |
| Tablet | Table: Days Waiting, Subject, Topic, SLA Status, Action. Other columns hidden (row expand). Drawer: 80% viewport width. |
| Mobile | Table: Subject, Days Waiting (badge), Assign button. Drawer: full screen. Batch assign modal: full screen bottom sheet. |

### Charts
- **KPI strip:** No charts — metric tiles with colour thresholds.
- **My Review History tab:** Horizontal bar chart — return reasons breakdown (Factual/Language/Formatting/etc.) for the reviewer's last 30 days. Helps reviewer see their own pattern. No data state: "Complete more reviews to see your return reason breakdown."

### Role-Based UI
- "Flag for Committee Review" button: visible only to Question Reviewer (28). Content Director sees read-only drawer without action buttons.
- "Batch Self-Assign": Reviewer only. Director read-only.
- Committee Queue tab: visible to Reviewer and Director. Only Reviewer can take action.
- My Review History tab: Reviewer only. Director uses D-13 for all reviewers' history.

---

*Page spec complete.*
*Amendments applied: G7 (Committee Review — sequential 2-reviewer process, committee pool, Reviewer 2 blind pass)*
*Gap amendments: Gap 3 (Quick Template CRUD — Section 12 Quick Template Manager) · Gap 15 (Passage Set review drawer context — Tab 3 Passage Set Context + Section 11) · Gap 16 (Committee deadlock when all Reviewer 2 candidates OOO — Edge Case added) · Gap 17 (Passage Set partial return state definition — Section 11 and Edge Case added)*
*Next file: `d-04-approval-queue.md`*
