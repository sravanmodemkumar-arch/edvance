# D-11 — Published MCQ Bank

> **Route:** `/content/bank/`
> **Division:** D — Content & Academics
> **Primary Role:** Question Approver (29) — full access + unpublish + re-tag · Content Director (18) — full access
> **Read Access:** SME ×9 (19–27) — own subject MCQs + Notes tab · Reviewer (28) — read only (duplicate check) · Notes Editor (30) — Notes tab only
> **File:** `d-11-published-bank.md`
> **Priority:** P1 — Reference bank needed by all Div D roles, Exam Ops, and QA from first publish
> **Status:** ⬜ Not started
> **Amendments:** G2 (Unpublish → Amendment Review workflow) · G4 (Access Level filter + Approver access level change) · G5 (Expiry status filter + Approver Extend Valid Until)

---

## 1. Page Name & Route

**Page Name:** Published MCQ Bank
**Route:** `/content/bank/`
**Part-load routes:**
- `/content/bank/?part=results&page={n}` — paginated question results
- `/content/bank/?part=drawer&question_id={uuid}` — question preview drawer
- `/content/bank/?part=notes-table&page={n}` — Notes tab results
- `/content/bank/?part=export-progress&task_id={celery_id}` — export generation progress

---

## 2. Purpose (Business Objective)

The Published MCQ Bank is the master reference for everything that has been approved and released for student use. It is the output of the entire content pipeline — every question that survived SME authoring, Reviewer scrutiny, and Approver sign-off ends up here, searchable and available to every authorised role.

Four distinct user groups access D-11 for different purposes:
1. **Content Director and Approver** — search and browse to understand coverage, perform post-publish corrections (re-tag, access change, unpublish), and export for reports
2. **SMEs** — search their own subject's published bank to avoid duplicating already-covered ground, and to see how their published questions look in the final format
3. **Reviewers** — inline duplicate check during review (checking if a question they're reviewing too closely matches something already published)
4. **Div F (Exam Operations)** — reads published questions directly from the shared content schema to build exam papers; D-11 is their visibility into what's available

The Notes tab gives all roles a unified search point for both MCQs and study notes without navigating to a separate page.

**Business goals:**
- Provide fast, full-text search across 2M+ published questions with subject/difficulty/exam type/access level filters
- Enable Approver post-publish corrections (re-tag, access change, extend expiry, unpublish)
- Enforce DPDPA: author names never exported in CSV/PDF
- Block export of questions scheduled for upcoming exams until exam date passes (exam secrecy)
- Show Exam Usage data per question (which papers it appeared in, how many students answered it)

---

## 3. User Roles

| Role | What They Can Do |
|---|---|
| Question Approver (29) | Search + browse · Unpublish (G2) · Difficulty Re-Tag · Access Level Change (G4) · Extend Valid Until (G5) · Export |
| Content Director (18) | Search + browse · Export · Archive (from Expiry Monitor) · Read-only on all questions |
| SME ×9 (19–27) | Search + browse own subject MCQs · Notes tab read · No write actions |
| Question Reviewer (28) | Search + browse (for duplicate check during D-03 review sessions) · No write actions |
| Notes Editor (30) | Notes tab only · No MCQ tab access |

---

## 4. Section-Wise Detailed Breakdown

---

### Section 1 — Page Layout

**Top section:** Search bar (full-width, prominent) + filter panel (collapsible, below search bar)
**Main area:** Two tabs: "MCQs" (default) and "Notes"
**Right side:** No persistent right panel — all detail via drawer

---

### Section 2 — Search

**Full-text search:** PostgreSQL `tsvector` GIN index on `content_question_plain_text` (concatenation of question_body_plain + option_a–d plain text). Search is over question content, not metadata.

**Search field:**
- Placeholder: "Search question text, options, or explanation…"
- Searches: question body + all 4 options + explanation (all plain text fields)
- Results ranked by relevance (PostgreSQL `ts_rank`)
- Min 3 characters before search fires

**Search behaviour:**
- HTMX `hx-trigger="input changed delay:500ms"` — fires 500ms after user stops typing
- Results load via `?part=results&page=1` — no page reload

---

### Section 3 — Filter Panel

All filters are persistent in URL query params so filtered views can be bookmarked and shared.

| Filter | Type | Notes |
|---|---|---|
| Subject | Multi-select dropdown | 9 subjects — SMEs see only own subject |
| Topic | Multi-select (cascading from Subject) | From D-09 taxonomy |
| Subtopic | Multi-select (cascading from Topic) | — |
| Difficulty | Multi-select: Easy / Medium / Hard | — |
| Exam Type | Multi-select: all 8 exam types | — |
| Bloom's Level | Multi-select: Recall / Understand / Apply / Analyse / Evaluate / Create | — |
| Content Type | Evergreen / Current Affairs / Time-Sensitive | — |
| Access Level | Platform-Wide / School Only / College Only / Coaching Only (Amendment G4) | SMEs see only questions their subject + access levels they can view |
| Expiry Status | All / Expiring ≤ 30 days / Expiring ≤ 90 days / Expired-Archived (Amendment G5) | Amber/red for approaching expiry |
| Published Date | Date range picker | — |
| Source | Human / AI / AI-Edited / Bulk Import | — |

**Filter count badge:** "Filters: 3 active" badge when filters are set — "Clear All" link.

---

### Section 4 — Results Table (MCQs Tab)

**50 rows per page.** "Load More" HTMX append (not pagination navigation — seamless infinite scroll feel).

| Column | Description |
|---|---|
| # | Row number (in current result set) |
| Question (truncated) | First 80 chars of question body — rendered (inline MathJax for short equations) |
| Subject | Badge |
| Topic | — |
| Difficulty | Easy/Medium/Hard badge |
| Content Type | Evergreen / Current Affairs / Time-Sensitive |
| Access Level | Platform-Wide / School / College / Coaching icon (Amendment G4) |
| Valid Until | Shown only for Current Affairs / Time-Sensitive — date, colour-coded by proximity to expiry |
| Exam Types | Comma-separated abbreviations |
| Published Date | — |
| Used In | Count of distinct exam papers this question has appeared in |

**Per-row actions (role-dependent):**
- "Preview" — opens question detail drawer (all roles)
- "Unpublish" (Approver only — G2) — opens unpublish sub-form inline
- "Re-Tag" (Approver only) — opens Tags tab of drawer pre-focused on Difficulty field

**Approver quick actions strip (above the table, visible only to Approver):**
Multi-select mode toggle. When ON:
- Checkboxes appear on each row
- "Bulk Re-Tag Difficulty" (select up to 50 rows → difficulty correction applied to all)
- No bulk unpublish here — Emergency Bulk Unpublish is in D-04

---

### Section 5 — Question Preview Drawer

**Trigger:** Row click or "Preview" button. 640px right-side drawer.

**Drawer tabs:**

**Tab 1: Preview (default)**
Full subject-specific rendered view — MathJax, SVG diagrams, code blocks, Telugu script. The correct answer is marked (visible to all Div D roles — this is the internal reference view, not the student-facing view).

Below the question render:
- Passage Set indicator (if applicable — G9): "This question is part of Passage Set {set_id}" with link to view the full passage + all linked questions

**Tab 2: Tags**
All metadata in read-only display for most roles; editable fields for Approver:

| Field | Read-only roles | Approver |
|---|---|---|
| Subject | Read-only | Read-only |
| Topic | Read-only | Read-only |
| Subtopic | Read-only | Read-only |
| Difficulty | Read-only | Editable dropdown — "Difficulty Re-Tag" action |
| Access Level | Read-only | Editable dropdown — "Access Level Change" action (G4) |
| Valid Until | Read-only | Editable date picker — "Extend Valid Until" (G5, Current Affairs/Time-Sensitive only) |
| Exam Types | Read-only | Read-only |
| Content Type | Read-only | Read-only |
| Source Attribution | Read-only | Read-only |

**Approver Tag Edits — each has its own confirm button in the Tags tab:**

"Save Difficulty Re-Tag":
- Shows: Current: Medium → New: Hard
- One-click confirm (no 2FA)
- D-12 audit entry: `action: TagAmendment`
- Memcached aggregate cache invalidated

"Save Access Level Change" (G4):
- Shows: Current: Platform-Wide → New: Coaching Only
- Warning count: "⚠ {N} upcoming exams in School and College tiers currently include this question. They will no longer have access after this change."
- 2FA re-prompt required (commercial implications)
- D-12 audit entry: `action: AccessAmendment`

"Save Extended Valid Until" (G5):
- Date picker — must be after current `valid_until`
- Optional reason field
- No 2FA
- D-12 audit entry: `action: ValidUntilExtended`

**Tab 3: Version History**
Link: "View Full Audit Trail in D-12 →" (opens D-12 for this question ID in a new tab). Plus a compact inline summary of major events: Created · Published · [if amended] Unpublished + Re-published.

**Tab 4: Exam Usage**
Which exam papers have included this question:
- Table: Institution Name · Exam Name · Exam Date · Marks Allotted · Student Count
- "Used in {N} exams across {M} institutions" — summary
- If exam has not yet occurred (upcoming): shown with "Upcoming" badge — these are the records checked for exam secrecy (export blocked for questions with upcoming exams)

**Approver drawer action bar:**

**"Unpublish" (G2):**
- Sub-form slides up in the drawer:
  - Reason text ≥ 20 chars (required)
  - Category: Paper Leak / Factual Error / Copyright / Court Order / Other
  - Type "UNPUBLISH" to confirm
  - 2FA re-prompt
- On confirm: state → `AMENDMENT_REVIEW` · Celery removes from exam pool · D-12 audit · Director notified

**"Difficulty Re-Tag" / "Access Level Change" / "Extend Valid Until":** Available in the Tags tab as described above.

**"Archive Question" (Approver only):**
- Used to retire a published question permanently from the active pool without triggering the Amendment Review workflow — for questions that are obsolete, superseded, or no longer curriculum-relevant.
- Guard check: if the question is assigned to any upcoming exam paper in Div F → block with "Cannot archive — remove from upcoming exam papers first."
- If question has only past exam usage: allow archive with confirmation.
- Confirmation modal: "Archive this question? It will be removed from the active exam pool and from all future question bank searches. Historical exam results referencing this question are unaffected."
- On confirm: state → `ARCHIVED` · D-12 audit entry · Memcached cache invalidated.
- Toast: ⚠️ "Question archived — removed from active pool" (Warning 8s).
- Archived questions: visible in D-11 with "Status: Archived" filter (hidden from default "Active" filter). Cannot be re-published from D-11 — requires engineering restore.

**Bulk Archive (Approver + Director — MCQ Results Table):**
- Checkbox multi-select on results table (same pattern as other Div D tables).
- "Archive Selected" button appears when ≥1 row selected (max 50).
- Same guard check per question — if any selected question is assigned to an upcoming exam, the batch is blocked with a list of conflicting question IDs.
- Confirmation modal shows count: "Archive {N} questions? This removes them from the active pool permanently."
- On confirm: Celery task archives all N questions atomically. Progress toast during execution for batches > 10.

**Tab 5: Video Production (MCQ-to-Video Integration)**

Shows the video production status for this question. Visible to all Div D roles with page access.

**Video Status Row:**

| State | Display |
|---|---|
| No video job | "No explanatory video" · grey camera icon · "Create Video Job →" button (Producer/Director only) |
| Job exists — In Production | "Video in production" · blue camera icon · Stage badge (e.g. "In Animation") · "View in E-05 →" link |
| Job exists — Published (single language) | "Video published ✅" · green camera icon · YouTube thumbnail + title · YouTube URL (external link) · "View in Library →" link to E-01 |
| Job exists — Published (multiple languages) | "Video published ✅ — {N} languages" · green camera icon · Language pills inline: 🇬🇧 EN · 🇮🇳 HI (each a clickable external link to that language's YouTube URL) · "View all in E-01 Library →" |
| Job exists — Published (multi-audio track) | "Video published ✅ — Multi-language" · One YouTube link · small note: "Audio language selectable on YouTube" |
| Job exists — On Hold | "Video on hold ⏸" · amber camera icon · "View in E-05 →" link |

**Multi-language video status table** (shown when ≥1 language variant job exists for this question):

| Language | Status | YouTube Link | Library |
|---|---|---|---|
| 🇬🇧 EN | ✅ Published | [Watch on YouTube ↗] | [View in E-01 →] |
| 🇮🇳 HI | ✅ Published | [Watch on YouTube ↗] | [View in E-01 →] |
| TE | 🔵 In Production | — | — |
| UR | ⬜ No job | — | [Create variant →] (Producer/Director only) |

"[Create variant →]" opens the language variant creation modal in E-05, pre-filled with this question's parent job ID and the selected language.

**If multiple video jobs exist for this question** (e.g. a remake — both with the same question_id): list each job in a small table: Job Title · Language · Status · "View in E-05 →".

**"Create Video Job" button** (Content Producer 82 and Content Director 18 only):

- Opens Create Video Job modal (640px):

| Field | Type | Required | Notes |
|---|---|---|---|
| Job Title | Text input | Yes | Pre-filled: "{Subject} — {Topic} — {Question short_id}" |
| Content Type | Select | Yes | Default: Problem Walkthrough |
| Priority | Select | Yes | Default: Normal |
| Overall SLA (days) | Number | Yes | Default from E-12 config |
| Language | Select | Yes | Default: EN |
| Notes to Scriptwriter | Textarea | No | Max 300 chars |

- On "Create Job":
  - POST to `/content/video/production/jobs/create-from-question/`
  - Creates `video_production_job` with `question_id = content_question.id`, `source = MCQ`
  - Celery task `seed_production_brief_from_question` populates `video_script.seed_text` with question body + correct answer + explanation
  - ✅ "Production job created — script seeded from question" toast 4s
  - Tab refreshes to show "Video in production" state

**MCQ table column — Video Status badge (read-only, for Producer/Director view):**
- Small camera icon appended to the question row in the results table (visible to Content Producer 82 and Content Director 18 only):
  - ⬜ (grey) = No video
  - 🔵 (blue) = In Production
  - ✅ (green) = Published
  - ⏸ (amber) = On Hold

---

### Section 6 — Export

**Purpose:** Filtered selection of published questions as CSV (raw data) or PDF (formatted question paper).

**Export controls (above the results table):**
- "Export Filtered Questions" button — exports the current search result set (as filtered)
- Format: CSV (max 2,000 questions) or PDF (max 500 questions)
- Both exports are async Celery tasks

**CSV export:**
- Columns: Question ID · Question Body (plain text) · Option A–D · Correct Option · Explanation · Subject · Topic · Subtopic · Difficulty · Bloom's Level · Exam Types · Content Type · Access Level · Valid Until · Source Attribution Type
- **DPDPA compliance:** Author name, author email, author IP, reviewer name — none of these fields are included in the CSV. Author identity is PII stored in audit logs only.
- Questions tagged to upcoming future exams: blocked from export. If the filtered set includes such questions, they are excluded from the export with a note: "{N} questions excluded (scheduled for upcoming exams — export blocked until exam date passes)."

**PDF export:**
- Formatted question paper layout: EduForge watermark per page, question numbers, options formatted as A/B/C/D, blank line below each question
- Correct answers in a separate appendix (last 2 pages) — students cannot infer answers from the paper layout
- Institution / Director can specify a header text for the PDF (exam name, date)

**Export generation:**
Celery `portal.tasks.content.generate_export` → download-ready notification (in-app toast + email with download link). Link expires in 24 hours (S3 presigned URL). Export event logged in D-12 per question: `action: Exported · actor · filter used · timestamp`.

---

### Section 7 — Notes Tab

**Purpose:** Published notes library accessible to all Div D roles in a unified search interface.

**Search bar:** Full-text search on Title + Tags + Chapter Reference. Debounced 300ms. Placeholder: "Search notes by title, topic, or keyword…"

**Filters (advanced filter panel — same collapsible pattern as MCQ tab):**

| Filter | Options |
|---|---|
| Subject | Multi-select — scope-locked for SMEs to their assigned subject |
| Topic | Cascading from Subject — multi-select |
| Exam Type | Multi-select |
| Academic Year | Multi-select |
| Difficulty Level | Introductory / Standard / Advanced |
| Language | English / Telugu / Hindi / Urdu / Bilingual |
| Source Institution | Multi-select (Directors only — SMEs cannot filter by institution) |
| Published Date | Date range picker |
| Version | v1 / v2 / v3+ — show notes that have been revised |

Active filter pills shown below search bar. Each dismissible.

**Results table (sortable columns):**

| Column | Sortable | Default Sort | Notes |
|---|---|---|---|
| Title | ✅ | ASC | Truncated to 80 chars |
| Subject | ✅ | — | — |
| Topics | — | — | Comma-separated tags (max 3 shown, "+N more" tooltip) |
| Published Date | ✅ | **DESC** (newest first) — default | — |
| View Count (30d) | ✅ | — | Unique student views |
| Download Count (30d) | ✅ | — | PDF download events |
| Language | — | — | — |
| Version | — | — | v1, v2, v3 badge |
| Actions | — | — | Role-dependent |

**Sort default:** Published Date DESC.
**Pagination:** 25 notes per page, numbered controls.

**Per-row actions:**

| Action | Roles | Notes |
|---|---|---|
| Preview | All roles | Opens PDF in a read-only PDF.js viewer drawer (560px). Full PDF scrollable, page nav, zoom. |
| Edit Metadata | Notes Editor (own notes) · Director (any note) | Opens D-06 structuring drawer with metadata pre-filled. Version does not increment for metadata-only changes. |
| Unpublish + Edit | Notes Editor (own notes) · Director (any note) | Sends note back to D-06 Incoming Queue. Confirmation modal: "Unpublish this note? Students will lose access until it is re-published." |
| View Audit Trail | Notes Editor (own notes) · Director (any note) | Opens D-06 Audit Trail Viewer panel (same as Section 9 in D-06) |
| Archive | Director only | Archives a published note — removes it from the student-facing notes library permanently. Use for obsolete notes (curriculum changed, superseded by a newer note). |

**"Archive Note" action (Director only):**
- Confirmation modal: "Archive '{Title}'? This note will be removed from the student library. Students who have bookmarked or downloaded it retain their copies, but it will no longer be searchable. This action is not reversible without engineering support."
- Reason field (optional, max 200 chars)
- On confirm: `content_notes.state` → `ARCHIVED` (new state, separate from `UNPUBLISHED`). Audit log entry: `action: NoteArchived`.
- Toast: ⚠️ "Note archived — removed from student library" (Warning 8s)
- Archived notes are excluded from all future search results (state filter: `NOT IN (ARCHIVED)`).
- Archived notes remain visible in D-11 Notes tab with an "ARCHIVED" state badge when the Director searches with filter "Status: Archived" (default filter is "Active" — archived are hidden by default).

**Notes Tab — Empty States:**

| State | Heading | Subtext |
|---|---|---|
| No notes match filters | "No notes found" | "Try clearing some filters or searching by a different keyword." |
| No published notes at all | "No published notes yet" | "Notes structured and published in D-06 will appear here." |
| Notes Editor — no notes in assigned subject | "No notes for your subject" | "Notes published for your subject will appear here." |

---

## 5. Data Models

### `content_question` — published bank query
Standard question table filtered by `state = 'PUBLISHED'`. Full-text search via:
```sql
SELECT *, ts_rank(search_vector, query) AS rank
FROM content.content_question
WHERE search_vector @@ plainto_tsquery('english', :search_text)
  AND state = 'PUBLISHED'
ORDER BY rank DESC
```
`search_vector` is a `tsvector` column maintained by a PostgreSQL trigger on `question_body_plain + option_a + option_b + option_c + option_d`.

### `content_question_exam_usage` (populated by Div F)
| Field | Type | Notes |
|---|---|---|
| `question_id` | FK → content_question | — |
| `exam_id` | FK → Div F exam table | — |
| `institution_id` | FK → Institution | — |
| `exam_date` | date | — |
| `marks_allotted` | decimal | — |
| `student_count` | int | How many students took this exam |
| `is_upcoming` | boolean | True if exam_date > today — used for export secrecy check |

### `content_question_export_log`
| Field | Type | Notes |
|---|---|---|
| `question_id` | FK → content_question | One record per question per export |
| `export_batch_id` | UUID | Groups all questions in one export event |
| `actor_id` | FK → auth.User | Who triggered the export |
| `filters_used` | jsonb | Filter snapshot at time of export |
| `format` | varchar | CSV / PDF |
| `exported_at` | timestamptz | — |

---

## 6. Access Control

| Gate | Rule |
|---|---|
| Page access | `PermissionRequiredMixin(permission='content.view_published_bank')` — all Div D roles |
| SME subject scope | ORM filter: `subject_id IN sme_profile.assigned_subjects` applied to all queries for SME roles |
| Notes Editor | Notes tab accessible; MCQ tab returns 403 |
| Approver write actions | `permission='content.publish_question'` checked on every write action (unpublish, re-tag, access change) |
| Export | `permission='content.export_questions'` — Roles 18 + 29. SMEs and Reviewers cannot export. |
| Export exam secrecy | Server-side filter: questions with `content_question_exam_usage.is_upcoming = true` excluded from all exports regardless of role |
| DPDPA | Author PII fields excluded from export query at ORM level — not filtered post-query |

---

## 7. Caching

**Aggregate count cache (Memcached, 5-min TTL):**
- Key: `published_bank_counts_{subject_id}` — total published question count per subject
- Used by D-05 Subject Coverage Matrix and D-01 Coverage Gaps tab
- `cache.delete(f'published_bank_counts_{subject_id}')` called on every publish, unpublish, or archive action

**Full-text search results:** Not cached — PostgreSQL GIN index on `search_vector` handles search performance. GIN index rebuild is DBA-managed (C-11) after bulk import operations.

---

## 8. Edge Cases & Error States

| Scenario | Behaviour |
|---|---|
| Search returns 0 results | "No published questions match your search. Try broader search terms or remove some filters." — not an error state |
| SME searches for questions in another subject | ORM filter silently excludes them — SME sees 0 results for off-subject search, not a 403 |
| Approver starts Access Level Change, then 2FA session expires | 2FA re-prompt appears inline in the drawer. Access Level change form is preserved. After 2FA: change proceeds. |
| Export of 2,000 questions times out in Celery | Celery task has 10-minute timeout for CSV generation. On timeout: failure logged, user notified: "Export failed — file too large. Try with stricter filters (e.g. max 1,000 questions)." |
| Question appears in Notes Exam Usage as "Upcoming" but exam was cancelled | Exam status is Div F's domain. Content Director can manually clear the `is_upcoming` flag via D-12 audit interface (Approver action) — requires explaining the cancellation in the reason field. |
| Reviewer opens D-11 for duplicate check while reviewing a question in D-03 | Reviewer has D-03 open in one browser tab and D-11 in another. Both are functional. The D-03 drawer auto-refresh is suspended on the D-03 tab (drawer is open). D-11 is a separate page session. |

---

## 9. Integration Points

| Integration | Direction | What Flows | Mechanism |
|---|---|---|---|
| D-04 Approval Queue | D-04 publishes → D-11 shows | Approved questions appear in MCQ tab | Same `content_question` table — state filter |
| D-03 Review Queue | D-03 reads D-11 | Inline duplicate check during review | pgvector HNSW query on `content_question_embeddings` |
| D-12 Audit & Version | D-11 → D-12 | Unpublish, re-tag, access change, export events logged | INSERT into `content_question_audit_log` |
| D-06 Notes Management | D-06 publishes → D-11 shows | Published notes appear in Notes tab | Same `content_notes` table — state filter |
| Div F Exam Operations | Div F reads D-11 | Published question pool for exam paper construction | Shared `content_question` table with `state = 'PUBLISHED'` + access level filter |
| Div F Results | Div F → D-11 | Exam usage data (`content_question_exam_usage`) | Div F writes usage records after exam construction |
| D-18 Reports | D-11 → D-18 | Export functionality shared | D-18 uses the same export Celery task with different filter presets |
| **E-05 Production Job Tracker** | D-11 → E-05 | "Create Video Job" action on question drawer creates `video_production_job` with `question_id` FK. Script seeded from question body + answer + explanation. | Django view POST → creates `video_production_job` record; Celery task seeds script. |

---

---

## 9. UI Patterns & Page-Specific Interactions

### Search
- Primary search bar at top of page. Placeholder: "Search published questions…".
- Full-text search on `content_question_plain_text` GIN index: question body + all four options.
- Debounced 300ms. Results update table in place.
- "N questions match '{query}'" shown below search bar when active.
- Search clears on tab switch (MCQs ↔ Notes) — separate search contexts.

### Advanced Filter Panel
- Collapsible, collapsed by default. "Filters" button with active count badge: "Filters (4)".
- Active filter pills below search: `Subject: Math ×` `Difficulty: Hard ×` — each dismissible.
- Filters: Subject (multi-select) · Topic (cascading from Subject) · Subtopic · Difficulty (multi-select checkboxes) · Exam Type (multi-select) · Author (role label multi-select, Director only) · Published Date (date range) · Bloom's Level (multi-select) · Content Type (multi-select) · Access Level (multi-select, G4) · Expiry Status (All / Active / Expiring ≤30 days / Expired-Archived, G5).
- "Apply Filters" + "Reset All" at bottom of filter panel.

### Sortable Columns — MCQ Table
| Column | Default Sort |
|---|---|
| Published Date | **DESC (newest first)** — default |
| Difficulty | Custom: Hard → Medium → Easy |
| Subject | ASC |
| Topic | ASC |
| Access Level | ASC |
| Valid Until | ASC (soonest expiry first) |
| Used in Exams | DESC |

### Pagination
- 50 rows per page, numbered controls + "Showing X–Y of N results". URL reflects `?page=N`.
- Filter changes reset to page 1.

### Row Selection — Bulk Re-Tag (Approver only)
- Checkbox column: visible to Approver on MCQ table.
- Max 50 rows for bulk re-tag.
- Bulk action bar: "{N} selected · Re-Tag Difficulty → [Easy / Medium / Hard] · [Apply]".
- Confirmation modal: "Re-tag {N} questions to {Difficulty}? This will log a Tag Amendment in the audit trail for each question." Confirm / Cancel.

### Empty States
| State | Heading | Subtext |
|---|---|---|
| No search results | "No questions match your search" | "Try different keywords or clear some filters." |
| No published questions | "Published bank is empty" | "Questions approved by the Approver will appear here." |
| Notes tab — no notes | "No published notes" | "Notes published by the Notes Editor will appear here." |
| Filtered — zero results | "No results for these filters" | "Try broadening your search or clearing some filters." |

### Toast Messages
| Action | Toast |
|---|---|
| Unpublish (G2, Approver) | ✅ "Question unpublished — fast-track amendment review created" (Success 4s) |
| Difficulty Re-Tag | ✅ "Difficulty updated" (Success 4s) |
| Bulk Re-Tag | ✅ "{N} questions re-tagged to {Difficulty}" (Success 4s) |
| Access Level Change (G4) | ✅ "Access level updated" (Success 4s) |
| Extend Valid Until (G5) | ✅ "Expiry date extended to {date}" (Success 4s) |
| Export queued | ℹ "Export started — you'll be notified when the file is ready" (Info 6s) |
| Export blocked — upcoming exam | ⚠ "{N} questions blocked from export — tagged to upcoming exams" (Warning persistent) |
| Video job created | ✅ "Production job created — script seeded from question" (Success 4s) |

### Loading States
- MCQ table: 8-row skeleton on initial load, filter apply, page change, search.
- Search input: spinner icon inside search field while debounce fires.
- Drawer open: 5-line skeleton in drawer body. Question preview renders after skeleton.
- Memcached aggregate counts (totals in sub-header): shimmer numbers while loading.
- Export progress (Celery): inline progress bar in drawer ("Generating export: querying → filtering → generating → uploading"). Notification + download link on complete.

### Responsive Behaviour
| Breakpoint | Priority Columns Shown |
|---|---|
| Desktop (≥1280px) | ID, Subject, Topic, Difficulty, Content Type, Access Level, Valid Until, Exam Types, Published Date, Action |
| Tablet (768–1279px) | Subject, Topic, Difficulty, Access Level, Published Date, Action (all others in row expand) |
| Mobile (<768px) | Subject + Difficulty badge + Published Date — tap row to open drawer. Horizontal scroll reveals other columns. |

Filter panel on mobile: bottom sheet (slides up from bottom). Date pickers are native mobile date inputs.

### Role-Based UI
- Approver actions (Unpublish, Re-Tag, Access Level Change, Extend Valid Until): Approver (29) only. Drawer shows read-only tags for Director and SMEs.
- "Export" button: Director (18) and Approver (29). SMEs see read-only (no export button).
- Author filter in Advanced Filter Panel: Director only. SMEs and Reviewers cannot filter by author (DPDPA — prevents SMEs from looking up each other's questions by name).
- Bulk Re-Tag checkbox column: Approver only. Not shown for other roles.
- Video Status camera icon column: Content Producer (82) and Content Director (18) only. Hidden for SMEs, Reviewers, Approvers.
- "Create Video Job" button in Drawer Tab 5: Content Producer (82) and Content Director (18) only. Other roles see Tab 5 as read-only (video status only, no create button).

---

*Page spec complete.*
*Amendments applied: G2 (Unpublish → Amendment Review workflow in drawer) · G4 (Access Level filter + Approver access level change) · G5 (Expiry status filter + Approver Extend Valid Until)*
*Gap amendments: Gap 5 (Archive individual question + Bulk Archive in MCQ drawer + MCQ results table — Approver only) · Gap 14 (Notes tab full spec with search, sortable table, filter parity with MCQ tab, Archive Note action, Audit Trail link)*
*Div E integration: Drawer Tab 5 (Video Production status + Create Video Job action for Content Producer/Director) · E-05 integration link in Section 9.*
*Next file: `d-12-audit-history.md`*
