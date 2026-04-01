# D-07 — Bulk MCQ Import

> **Route:** `/content/import/`
> **Division:** D — Content & Academics
> **Primary Roles:** All 9 SME roles (19–27) — own subject only · Content Director (18) — all subjects
> **File:** `d-07-bulk-import.md`
> **Priority:** P1 — Required before AI pipeline activates and legacy content migration begins
> **Status:** ⬜ Not started
> **Amendments:** G1 (Duplicate Detection — pgvector cosine similarity on all valid rows before submit)

---

## 1. Page Name & Route

**Page Name:** Bulk MCQ Import
**Route:** `/content/import/`
**Part-load routes:**
- `/content/import/?part=validation-progress&batch_id={uuid}` — live validation progress bar
- `/content/import/?part=validation-results&batch_id={uuid}` — validation report table
- `/content/import/?part=duplicate-check-progress&batch_id={uuid}` — duplicate check progress
- `/content/import/?part=duplicate-results&batch_id={uuid}` — duplicate flagged rows

---

## 2. Purpose (Business Objective)

Institutions bringing their existing question banks to EduForge cannot author 2M+ questions from scratch. The Bulk Import page is the migration gateway: a structured CSV/Excel import that validates, de-duplicates, and batch-creates questions without each one requiring manual entry in D-02.

At the scale of 15,000–20,000 questions per month target, even a single legacy institution migration (a coaching centre with 50,000 past-year questions) represents 3+ months of manual authoring time. Bulk import compresses that to hours.

The import process is intentionally strict: every row must meet the same quality standards as a manually authored question (all required tags, valid taxonomy codes, explanation minimum length). The validation report and inline fix capability mean SMEs do not need to re-upload to fix errors — they fix them in the preview table and submit once.

**Business goals:**
- Enable legacy content migration at institutional scale (up to 500 rows per file)
- Enforce the same quality standards as manual D-02 authoring — no bypassing required metadata
- Catch duplicate questions against the 2M+ bank before they enter the pipeline (G1)
- Give SMEs and Director full visibility into what was imported, what failed, and why
- Support subject-scoped import for SMEs (cannot import another subject's content)

---

## 3. User Roles

| Role | Subject Scope | Max Rows |
|---|---|---|
| SME — any (19–27) | Own assigned subjects only — mismatched subject rows auto-rejected | 500 rows per file |
| Content Director (18) | All subjects | 500 rows per file |

---

## 4. Section-Wise Detailed Breakdown

---

### Section 1 — Step 1: Upload

**Layout:** Stepper UI — 4 steps shown as numbered breadcrumbs at top. User is on Step 1.

**Step 1 header:** "Upload Your Question File"

**Template download:**
Before uploading, SME downloads a per-subject CSV template:
- Dropdown: "Download Template for [Subject]" — subject dropdown (locked to SME's assigned subjects; Director sees all subjects)
- Template is pre-populated with all required column headers and one example row:
  - `question_body` · `option_a` · `option_b` · `option_c` · `option_d` · `correct_option` (a/b/c/d) · `explanation` · `topic_code` · `subtopic_code` · `difficulty` (Easy/Medium/Hard) · `blooms_level` (Recall/Understand/Apply/Analyse/Evaluate/Create) · `exam_types` (semicolon-separated codes: SSC_CGL;RRB_NTPC) · `content_type` (Evergreen/CurrentAffairs/TimeSensitive) · `access_level` (PlatformWide/SchoolOnly/CollegeOnly/CoachingOnly) · `valid_until` (YYYY-MM-DD — required if content_type ≠ Evergreen) · `source_attribution_type` (Original/AdaptedFromTextbook/PastExamPaper) · `source_attribution_detail` (required if not Original) · `high_stakes` (TRUE/FALSE)
- Topic codes and subtopic codes reference the D-09 taxonomy — the template download includes a second sheet "Taxonomy Reference" with all valid codes for the selected subject

**File upload zone:**
- Drag-and-drop zone + "Browse Files" button
- Accepted: CSV, XLSX
- Max file size: 5MB (approximately 500 rows with long question text)
- Max rows: 500 — if file has > 500 rows, upload is rejected with: "This file has {N} rows. Maximum 500 per batch. Split your file into smaller batches."
- "Upload" button → triggers Celery task + navigates to Step 2

---

### Section 2 — Step 2: Validation Report

**Header:** "Step 2: Validation Report"

**Progress bar (while Celery task runs):**
HTMX polls `?part=validation-progress&batch_id={uuid}` every 2s.
"Validating… Row 123 / 500 complete" — validation is row-by-row.

**Validation checks per row:**
1. `question_body`: not empty, > 10 chars
2. Options A–D: all four present and non-empty
3. `correct_option`: must be "a", "b", "c", or "d" exactly
4. `explanation`: ≥ 30 characters
5. `topic_code`: valid code in `content_taxonomy_topic` for the declared subject
6. `subtopic_code`: valid code in `content_taxonomy_subtopic` for the declared topic (if provided)
7. `difficulty`: exactly "Easy", "Medium", or "Hard"
8. `blooms_level`: valid enum value
9. `exam_types`: at least 1 valid exam type code; each code in allowed set
10. `content_type`: exactly "Evergreen", "CurrentAffairs", or "TimeSensitive"
11. `valid_until`: present and a valid future date if `content_type` ≠ Evergreen
12. `access_level`: valid enum value
13. `source_attribution_type`: valid enum value; `source_attribution_detail` present if not "Original"
14. **Subject scope check (SMEs only):** `topic_code`'s parent subject must match SME's assigned subject — mismatched rows are auto-rejected with error "This topic belongs to [Subject] — you can only import your assigned subjects."

**Validation results (after task completes):**

Summary bar:
- ✅ Valid rows: {N}
- ❌ Error rows: {N}

**Validation table (all rows, colour-coded):**

| Column | Description |
|---|---|
| Row # | File row number |
| Status | ✅ Valid / ❌ Error |
| Question (truncated) | First 60 chars |
| Error Details | Inline error messages — one per failing field (e.g. "explanation: must be ≥ 30 characters" · "topic_code: 'PHYS_999' is not a valid code") |

**Inline fix capability:**
Error cells are editable directly in the table — Notes Editor types the corrected value. "Validate this row" per-row button fires a single-row re-validation via HTMX. On success: row turns green. Fixed rows are included in Step 3 without re-uploading the entire file.

SMEs do not need to download the file, fix it offline, and re-upload — the inline fix covers the most common errors (typos in topic codes, missing explanation text).

"Download Errors CSV" button — downloads only the error rows with all error messages as an additional column — for complex fixes that need offline work.

---

### Section 3 — Step 3: Duplicate Check (Amendment G1)

**Header:** "Step 3: Duplicate Check"
"All valid rows are being checked against the 2M+ question bank for similarity."

**Progress bar:**
HTMX polls `?part=duplicate-check-progress&batch_id={uuid}` every 3s.
"Checking duplicates… Row 89 / 423 valid rows complete" — pgvector HNSW cosine similarity check for each valid row's embedding vs `content_question_embeddings`.

This step runs in parallel in the background — embeddings for each valid row are computed via the active embedding model, then cosine similarity searched. Typical completion: 2–5 minutes for 500 rows.

**Duplicate results (after task completes):**

Summary:
- ✅ No duplicates found: {N} rows
- ⚠ Possible duplicates: {N} rows (similarity ≥ 0.80 with existing questions)

**Duplicate-flagged rows table:**

| Column | Description |
|---|---|
| Row # | — |
| Question (truncated) | — |
| Similarity Score | e.g. "91% similar" |
| Matched Question ID | UUID of the matching question |
| Matched Question Preview | First 60 chars of the matching question |
| Matched State | Published / In Review / Draft |
| Action | "Include Anyway" / "Exclude" |

**Per-row action:**
- "Include Anyway" — marks the row as `duplicate_acknowledged: true` · row will be saved as Draft in the next step. Used when the new question is a legitimate variant (different difficulty, different wording, different exam type context).
- "Exclude" — marks the row as excluded from the batch submit. Row shown in Step 4 as excluded.

"Acknowledge All and Include" bulk button — marks all flagged rows as acknowledged. For Directors performing bulk legacy content migration where they accept some duplication risk.

---

### Section 4 — Step 4: Submit

**Header:** "Step 4: Submit {N} Questions"

**Summary panel:**
- ✅ Valid + no duplicate issues: {N} rows → will be saved as DRAFT
- ⚠ Valid + duplicate acknowledged: {N} rows → will be saved as DRAFT (with `duplicate_acknowledged: true`)
- ❌ Excluded (error or SME excluded duplicate): {N} rows → not saved
- Total to submit: {N}

**"Submit {N} Questions" button:**
On click:
- Celery task `portal.tasks.content.bulk_import_submit` creates `content_question` records for all valid rows with `state: DRAFT`, `author_id: request.user.id`
- Batch logged: `content_import_batch` record with all metadata
- On completion: toast "✅ {N} questions saved as Draft. They appear in D-01 My Questions tab and are ready to submit for review."
- "Download Failures CSV" button appears if any rows were excluded — CSV with all excluded rows and their rejection reasons

**"Submit" does NOT move questions to UNDER_REVIEW** — the questions are saved as DRAFT. The SME then reviews them in D-01 and submits for review individually or in batches via D-01 My Questions table. This ensures the SME has a chance to review imported content before it enters the review pipeline.

**Exception: Content Director import** — When the Director imports for a subject not covered by a current active SME (migration scenario), the Director can select "Submit all to Review immediately" — all valid rows bypass the DRAFT state and go directly to `UNDER_REVIEW`. Available only to Role 18.

---

### Wizard Session Persistence

**Problem without persistence:** If an SME completes Step 2 (Validation) or Step 3 (Duplicate Check) and then accidentally closes the browser tab, navigates away, or loses their session, they must re-upload the file and wait through validation and duplicate check again. For large batches (500 rows), duplicate check takes 2–5 minutes — re-running it is costly.

**Session persistence mechanism:**

Each batch creates a `content_import_batch` record immediately on file upload (Step 1), with an initial `status: UPLOADED`. This record acts as the session anchor.

**State per batch:**

| `status` value | Wizard Step | Resume behaviour |
|---|---|---|
| `UPLOADED` | Step 1 complete | Return to Step 2 — validation job may still be running |
| `VALIDATION_IN_PROGRESS` | Step 2 in progress | Return to Step 2 — progress bar reconnects via HTMX poll |
| `VALIDATION_COMPLETE` | Step 2 complete | Return to Step 2 with validation results shown |
| `DUPLICATE_CHECK_IN_PROGRESS` | Step 3 in progress | Return to Step 3 — progress bar reconnects via HTMX poll |
| `DUPLICATE_CHECK_COMPLETE` | Step 3 complete | Return to Step 3 with duplicate results shown |
| `SUBMITTED` | Step 4 complete | Batch is done — redirect to Import History |

**"Resume Import" entry point in D-01:**
When the SME navigates to D-01 (My Questions tab) and has an in-progress import batch (status not `SUBMITTED`), a yellow banner appears at the top of D-01:

> ⏭ **In-progress import detected** — You have an incomplete import batch from {date}. {N} rows uploaded. [Resume Import →]

Clicking "Resume Import →" returns the SME to D-07 at the last completed step (Step 2, 3, or 4) with all data restored.

**"In-Progress Imports" section in D-07 Import History (Section 5):**
A dedicated sub-section above the full import history table showing only batches with status ≠ `SUBMITTED` and ≠ `FAILED`. Per row:

| Column | Notes |
|---|---|
| Batch ID | Truncated |
| Uploaded | Date/time |
| File name | Original filename |
| Rows | Total rows in file |
| Status | Current wizard step |
| "Resume" button | Returns to wizard at current step with data restored |
| "Abandon" button | Confirmation modal: "Abandon this import batch? The uploaded file will be deleted and no questions will be created." Sets status → `ABANDONED`. |

**Celery task reconnection:**
When a validation or duplicate check Celery task was still running when the user navigated away, returning to the wizard step reconnects the HTMX progress bar to the existing task via `?part=validation-progress&batch_id={uuid}`. The Celery task continues running in the background regardless of whether the browser is open — the user can close the tab, return 5 minutes later, and see the completed results.

**Session expiry:** Import batches are retained for 48 hours in `UPLOADED`, `VALIDATION_COMPLETE`, or `DUPLICATE_CHECK_COMPLETE` states without submission. After 48 hours: a Celery beat task marks them `ABANDONED` and deletes the S3 file. SME is notified via D-19 notification: "Your import batch from {date} expired without submission — the uploaded file was deleted. Please re-upload to continue."

**`content_import_batch` additional fields (for persistence):**

| Field | Type | Notes |
|---|---|---|
| `status` | varchar | UPLOADED · VALIDATION_IN_PROGRESS · VALIDATION_COMPLETE · DUPLICATE_CHECK_IN_PROGRESS · DUPLICATE_CHECK_COMPLETE · SUBMITTED · FAILED · ABANDONED |
| `validation_task_id` | varchar | Celery task ID — for HTMX progress reconnection |
| `duplicate_check_task_id` | varchar | Celery task ID |
| `row_decisions` | jsonb | Per-row SME decisions from Step 2 + Step 3 (inline fixes, exclude/include choices) — persisted so resuming shows the SME's prior work |
| `expires_at` | timestamptz | 48 hours from `created_at` — after which batch is abandoned |

---

### Section 5 — Import History

**Bottom section of the page (always visible, below the step UI):**
A collapsible "Import History" panel showing the last 20 batches imported by this user:

| Column | Description |
|---|---|
| Batch ID | UUID (first 8 chars) |
| Date | Import date |
| Subject | Which subject's template was used |
| Total Rows | Rows in the file |
| Valid | Validated successfully |
| Errors | Failed validation |
| Duplicates | Flagged as duplicate |
| Submitted | Actually saved as Draft |
| Status | Completed / Partial / Failed |

Click on any batch row to see the full import report for that batch.

---

## 5. Data Models

### `content_import_batch`
| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `uploader_id` | FK → auth.User | SME or Director |
| `subject_id` | FK → content_taxonomy_subject | Subject declared at template download time |
| `filename` | varchar | Original uploaded filename |
| `total_rows` | int | — |
| `valid_rows` | int | After validation |
| `error_rows` | int | — |
| `duplicate_flagged_rows` | int | — |
| `submitted_rows` | int | Actually saved as DRAFT |
| `celery_task_id` | varchar | For progress polling |
| `status` | varchar | Uploading · Validating · DuplicateCheck · Completed · Failed |
| `created_at` | timestamptz | — |
| `completed_at` | timestamptz | Nullable |

### `content_import_batch_rows`
| Field | Type | Notes |
|---|---|---|
| `batch_id` | FK → content_import_batch | — |
| `row_number` | int | File row number |
| `question_id` | FK → content_question | Nullable — populated after submit |
| `status` | varchar | Valid · Error · DuplicateFlagged · DuplicateAcknowledged · Excluded · Submitted |
| `validation_errors` | jsonb | Per-field error messages |
| `duplicate_similarity` | decimal | Nullable — highest match similarity |
| `duplicate_match_id` | UUID | Nullable — matched question UUID |
| `raw_data` | jsonb | The original row data (for re-validation on inline fix) |

---

## 6. Access Control

| Gate | Rule |
|---|---|
| Page access | `PermissionRequiredMixin(permission='content.bulk_import_questions')` — Roles 19–27 + Role 18 |
| Subject scope | During validation, row's `topic_code` parent subject is checked against `sme_profile.assigned_subjects` for SME users. Mismatched rows auto-rejected. Content Director bypasses this check. |
| Director immediate-review option | `request.user.has_perm('content.submit_all_to_review')` — Role 18 only |
| Import history | SME sees only their own batches. Director sees all batches from all users. |

---

## 7. Edge Cases & Error States

| Scenario | Behaviour |
|---|---|
| SME uploads a file where all 500 rows have the wrong subject | All 500 rows fail subject scope validation — Step 2 shows 0 valid, 500 errors with "Subject mismatch" as the error. No rows proceed to Step 3. |
| Validation Celery task times out (> 5 minutes for 500 rows) | HTMX poll receives timeout response. "Validation is taking longer than expected. The report will be available when complete — you can leave this page and return." Email notification sent to user when complete. |
| User closes browser mid-import | Import batch continues processing on the server (Celery tasks are server-side). User returns to `/content/import/` and sees the Import History panel with the in-progress batch — can navigate back to the batch report. |
| Duplicate check finds a match with a question currently in Amendment Review | The matched question is shown as "Amendment Review" state. The import row is still flagged as a possible duplicate — SME decides whether to include or exclude. |
| Content Director imports 500 rows for a subject that has no active SME | All valid rows created as DRAFT attributed to the Director. Director selects "Submit all to Review immediately" — questions enter D-03 as AI-sourced equivalent (Director-authored flag). No SME notification (no assigned SME for this subject). |

---

## 8. Integration Points

| Integration | Direction | What Flows | Mechanism |
|---|---|---|---|
| D-09 Taxonomy | D-07 reads | Valid topic_code and subtopic_code lookups | ORM — `content_taxonomy_topic.code` field indexed |
| C-15 Embedding Model | D-07 → Celery → pgvector | Question embeddings for duplicate check | Same Celery task as D-02 duplicate check — reuses `portal.tasks.content.compute_embedding` |
| D-03 Review Queue | D-07 → D-03 | Director's "Submit all to Review" option | State change to UNDER_REVIEW for all valid rows in batch |
| D-01 SME Dashboard | D-07 → D-01 | Imported DRAFT questions appear in My Questions tab | Same `content_question` table — no additional integration |

---

---

## 9. UI Patterns & Page-Specific Interactions

### Wizard Step Indicator
- Persistent horizontal step bar at top: Step 1 Upload → Step 2 Validate → Step 3 Duplicates → Step 4 Submit.
- Current step: filled circle. Completed steps: checkmark. Future steps: grey outline.
- Breadcrumb navigation: completed steps are clickable (to go back). Cannot skip forward.
- Mobile: step bar collapses to "Step {N} of 4 — {Step Name}" text with a progress bar below.

### Step 2 — Validation Report: Table
- Validation results table: all 500 rows shown (no pagination — user needs to see all errors to fix them). Horizontal scroll on mobile.
- Sortable columns: Row # · Status (Valid/Error first) · Subject · Topic · Error Type.
- Default sort: **Error rows first**, then by Row # ASC.
- **Inline fix:** Error cells highlighted red. Click any error cell → inline input appears in place. Type correction → HTMX validates single field on blur. Green checkmark on valid, red border on still-invalid.
- "Download Errors CSV": exports only error rows with column + error description per cell.
- Filter toggle: "Show Errors Only" / "Show All Rows" — default "Show Errors Only" after validation.

### Step 3 — Duplicate Check: Table
- Same 500-row capacity. Duplicate-flagged rows sorted first.
- Per flagged row: expandable detail panel shows top 3 similar questions (UUID short, similarity %, subject, topic) with "Include Anyway" / "Exclude" toggle per row.
- "Acknowledge All Flagged as Unique and Include" bulk action (Director only) — requires checkbox confirm: "I confirm these are unique questions."

### Empty States
| State | Heading | Subtext |
|---|---|---|
| Step 1 — no file | "Upload your question file" | "Drag & drop a CSV or XLSX file, or click to browse. Maximum 500 rows, 5MB." |
| Step 2 — all rows valid | "All rows are valid ✓" | "No errors found. Proceed to the duplicate check." |
| Step 3 — no duplicates | "No duplicates detected ✓" | "All valid rows appear unique against the published question bank." |
| Import History — no batches | "No imports yet" | "Your previous import batches will appear here." |

### Toast Messages
| Action | Toast |
|---|---|
| File uploaded | ℹ "File uploaded — validation starting…" (Info 4s) |
| Validation complete — errors found | ⚠ "{N} rows have errors. Review and fix before proceeding." (Warning persistent) |
| Validation complete — all valid | ✅ "All {N} rows are valid" (Success 4s) |
| Duplicate check complete | ℹ "{N} possible duplicates flagged" (Info 6s) |
| Submit batch | ✅ "{N} questions saved as Draft" (Success 4s) |
| Submit + Send to Review | ✅ "{N} questions submitted for review" (Success 4s) |
| File too large (> 5MB) | ❌ "File too large — maximum 5MB" (Error persistent) |
| File exceeds 500 rows | ❌ "File has {N} rows — maximum 500 per import. Split into multiple files." (Error persistent) |

### Loading States
- Step 2 validation: animated progress bar ("Validating row {N} of {total}…"). Updates every 1s via HTMX poll. Validation report renders when complete.
- Step 3 duplicate check: progress bar ("Checking for duplicates: {N} of {valid_count} rows checked…"). pgvector HNSW queries batched in groups of 50 to avoid timeout.
- Step 4 submit: spinner on Submit button. "Saving {N} questions as Draft…" toast replaces spinner on completion.

### Responsive Behaviour
| Breakpoint | Behaviour |
|---|---|
| Desktop | Full stepper visible. Validation table full columns, scrollable. |
| Tablet | Stepper condensed (text labels hidden, icons only). Validation table: Row #, Status, Error column — others in row expand. |
| Mobile | Step indicator: "Step N of 4" text. Tables: Row #, Status, Error summary — horizontal scroll. Inline fix opens as bottom sheet input on mobile. |

### Import History Table (below main wizard)
Collapsible section "Previous Imports". Shows last 20 batches. Columns: Batch ID (short) · Date · Uploader Role · Total Rows · Valid · Errors · Status. Sortable by Date DESC (default). Pagination: 20 per page. Download Report link per batch.

### Role-Based UI
- Subject column validation: SMEs see only their assigned subject rows as valid. Mismatched rows auto-error: "Your account is not assigned to this subject." Director sees all subjects.
- "Submit all to Review immediately" checkbox: Director only (bypasses DRAFT state). SMEs cannot see this option.
- Step 3 "Acknowledge All Flagged" bulk action: Director only. SMEs must acknowledge per-row.

---

*Page spec complete.*
*Amendments applied: G1 (Duplicate Detection on all valid rows via pgvector HNSW similarity, Step 3 of import flow)*
*Gap amendments: Gap 10 (Wizard session persistence + "Resume Import" from D-01 — `content_import_batch.status` state machine, Celery task reconnection, 48-hour expiry, D-01 banner, D-07 In-Progress Imports sub-section)*
*Next file: `d-08-ai-triage.md`*
