# D-02 — Question Authoring & Editor

> **Route:** `/content/sme/question/new/` · `/content/sme/question/<uuid>/edit/`
> **Division:** D — Content & Academics
> **Primary Roles:** SME — Mathematics (19) · SME — Physics (20) · SME — Chemistry (21) · SME — Biology (22) · SME — English (23) · SME — General Knowledge (24) · SME — Reasoning (25) · SME — Computer Science (26) · SME — Regional Language (27)
> **Secondary Access:** Content Director (18) — read-only preview of any question via separate route `/content/sme/question/<uuid>/preview/`
> **File:** `d-02-question-editor.md`
> **Priority:** P0 — No content enters the platform without this page
> **Status:** ⬜ Not started
> **Amendments:** G1 (Duplicate Detection — pgvector cosine similarity) · G4 (Access Level field — Platform-Wide / School / College / Coaching) · G5 (Content Type + Valid Until — question expiry) · G7 (High Stakes flag — committee review trigger) · G9 (Passage / Linked Question Set mode — comprehension questions)

---

## 1. Page Name & Route

**Page Name:** Question Authoring & Editor
**Routes:**
- `/content/sme/question/new/` — Create new standalone MCQ
- `/content/sme/question/new/?mode=passage-set` — Create new comprehension passage set (G9)
- `/content/sme/question/<uuid>/edit/` — Edit existing draft MCQ
- `/content/sme/question/<uuid>/edit/?mode=revision` — Edit returned question in split-view revision mode
- `/content/sme/question/<uuid>/preview/` — Read-only preview (Content Director)

**Part-load routes:**
- `/content/sme/question/new/?part=duplicate-check` — Async duplicate check results banner
- `/content/sme/question/<uuid>/edit/?part=revision-panel` — Prior version content for split-view left panel
- `/content/sme/question/new/?part=taxonomy-cascade&subject={id}&topic={id}` — Subtopic cascade on topic change
- `/content/sme/question/new/?part=freeze-check&exam_types={csv}` — Validate exam types against content freeze dates

---

## 2. Purpose (Business Objective)

The Question Authoring & Editor is where all MCQ content originates. Every question in the 2M+ bank was created here — by one of the 9 SME roles, with subject-specific tooling, structured metadata, and a quality pipeline entry point. Nothing enters review without passing through D-02.

The page has three distinct operational modes that serve very different needs:

**Create mode** — a blank editor where an SME authors a new question from scratch. The subject-specific toolbar adapts to the SME's assigned subject: a Mathematics SME gets LaTeX with MathJax live preview; a Chemistry SME gets a molecular formula builder and SMILES renderer; a Regional Language SME gets Telugu/Devanagari/Urdu IME with script validation. These are not cosmetic differences — they are the functional tools without which these SMEs cannot do their job.

**Revision mode** — triggered when an SME opens a returned question. A split-screen layout shows the prior submitted version (read-only, with the reviewer's comment highlighted in context) on the left and the editable current version on the right. The SME sees exactly what the reviewer saw, alongside the correction they are making. Without this split-view, SMEs routinely make the wrong correction because they cannot precisely recall what the submitted version looked like.

**Passage Set mode (G9)** — a fundamentally different workflow for comprehension-type questions required by SSC CGL, UPSC Prelims, CHSL, and State Board English exams. A passage (50–2,000 words of source text) is created first, then 2–8 MCQs are linked to it. All linked questions move through the review pipeline as a unit — the Reviewer sees the full passage with all questions; the Approver approves them as a set.

At 15,000–20,000 new questions per month across 9 SMEs, the editor must be fast to load, autosave on every keystroke, and give immediate inline feedback on tagging errors, duplicate matches, and freeze violations — without interrupting the authoring flow.

**Business goals:**
- Enable 9 SMEs with different subject domains to author questions without worrying about formatting — the toolbar handles domain-specific rendering
- Catch potential duplicate questions before they enter the review queue, saving Reviewer time
- Enforce all required metadata at submission time (not review time) — incomplete tags cannot enter the pipeline
- Support comprehension passage questions for 3 of the 8 supported exam types (G9)
- Make revision a precise, confident act — the SME knows exactly what changed

---

## 3. User Roles

| Role | What They Can Do in D-02 | Subject Scope |
|---|---|---|
| SME — Mathematics (19) | Create, edit, revise own draft questions · Submit for review | Mathematics only — LaTeX toolbar enabled |
| SME — Physics (20) | Create, edit, revise own draft questions · Submit for review | Physics only — LaTeX + circuit/ray diagram toolbar |
| SME — Chemistry (21) | Create, edit, revise own draft questions · Submit for review | Chemistry only — formula builder + SMILES renderer |
| SME — Biology (22) | Create, edit, revise own draft questions · Submit for review | Biology only — annotated diagram upload tool |
| SME — English (23) | Create, edit, revise own draft questions · Submit for review · Create Passage Sets | English only — rich text; Passage Set mode available by default |
| SME — General Knowledge (24) | Create, edit, revise own draft questions · Submit for review · Create Passage Sets | GK only — rich text + image; Passage Set mode available by default; `valid_until` always required |
| SME — Reasoning (25) | Create, edit, revise own draft questions · Submit for review | Reasoning only — pattern/matrix image upload |
| SME — Computer Science (26) | Create, edit, revise own draft questions · Submit for review | CS only — code block with syntax highlighting |
| SME — Regional Language (27) | Create, edit, revise own draft questions · Submit for review | Regional Language — Telugu/Hindi/Urdu IME with script validation |
| Content Director (18) | Read-only preview only — via `/content/sme/question/<uuid>/preview/` | All subjects |

> **Critical constraint:** Subject scope is enforced at view initialization. The Subject field in the tagging panel is locked to the SME's `sme_profile.assigned_subjects` values. Even if a POST request is forged with a different `subject_id`, the view rejects it with 403 and logs the attempt.

---

## 4. Section-Wise Detailed Breakdown

---

### Section 1 — Page Header & Mode Indicator

**New question header:**
- H1: "New Question"
- Mode toggle (if English or GK SME): "Standalone MCQ" | "Passage Set" — tab-style toggle. Default: Standalone MCQ. Switching mode clears the form after a confirmation modal ("Switching mode will clear the current form. Continue?")
- Autosave indicator: "Saving…" (spinner) → "Saved as Draft" (timestamp) → "Save failed — reconnecting…" (red, retries every 10s)
- "Back to Dashboard" link (top-left) — if unsaved changes exist, prompts: "You have unsaved changes. Leave anyway?"

**Edit / Revision header:**
- H1: "Edit Question" (standard edit) or "Revise Returned Question" (revision mode — amber background header to visually differentiate)
- Question UUID displayed: "Question ID: `3f8a...c21d`" — for support references
- Status pill: "Draft" / "Returned (Revision ×2)" — shows return count
- "Back to Dashboard" link — if unsaved changes, same prompt as above

---

### Section 2 — Standalone MCQ Editor Layout

**Two-column layout:**
- **Left column (65%):** Question body editor + Answer options + Explanation
- **Right column (35%):** Tagging panel (always visible, scrolls independently)

The right tagging panel uses `position: sticky` so it stays visible as the SME scrolls through a long question body.

---

### Section 3 — Question Body Editor

**Purpose:** Compose the question stem — the text, images, equations, diagrams, or code that forms the question.

**Universal features (all 9 subjects):**
- Rich text editor based on ProseMirror — bold, italic, underline, ordered list, unordered list, superscript, subscript
- Inline image upload: drag-and-drop or click to upload (PNG/SVG/JPG ≤ 2MB) → uploaded immediately to S3 `content-media/{sme_id}/{uuid}/` → CloudFront URL auto-embedded in question body → thumbnail preview shown inline in editor. Upload progress spinner inline.
- Character count (not word count — some exam authorities impose character limits)
- Paste sanitisation: strips Microsoft Word formatting, preserves only plain text + image references

**Subject-specific toolbar extensions (loaded from `sme_profile.assigned_subjects`):**

**Mathematics (Role 19) — LaTeX Equation Builder:**
Toolbar button "∑ Insert Equation" opens an equation editor modal:
- LaTeX input field with syntax highlighting
- MathJax live preview panel (renders as the SME types — no submit needed)
- Shortcut buttons: fractions (½), integrals (∫), summation (Σ), square roots (√), matrices (2×2, 3×3 presets), limits, derivatives, vectors
- "Insert" button embeds the LaTeX as `\[...\]` in the question body and stores it; the rendered preview shows in the editor using client-side MathJax
- Error indicator: if LaTeX is syntactically invalid, preview shows "Invalid LaTeX" in red — Insert button disabled until fixed
- Equations are stored as LaTeX in the DB; MathJax renders client-side on display

**Physics (Role 20) — LaTeX (same as Math) + Circuit Diagram Tool + Ray Diagram Tool:**
- LaTeX equation builder (same as Math)
- "Draw Circuit" toolbar button → opens SVG circuit diagram editor: component palette (resistors, capacitors, inductors, voltage sources, current sources, ground, wire, node labels) + canvas with snap-to-grid. Export as SVG → auto-uploaded to S3, embedded as inline SVG in question body. Preview renders directly in editor.
- "Draw Ray Diagram" toolbar button → simplified optics diagram tool: concave/convex lens/mirror, principal axis, focus point, object/image arrows. Same SVG export + S3 upload flow.

**Chemistry (Role 21) — Chemical Formula Builder + SMILES Renderer:**
- Chemical formula toolbar: subscript/superscript shortcuts specifically for chemical notation (H₂SO₄, [CuSO₄]²⁻, CO₂, etc.) — typed in standard keyboard shorthand, rendered correctly
- Ionic charge notation: auto-formats `2+` as ²⁺
- "Draw Molecule" button → SMILES (Simplified Molecular Input Line Entry System) input field with RDKit.js client-side 2D structure renderer. SME enters SMILES string → molecular structure diagram renders in preview panel → "Embed Diagram" → uploaded as PNG to S3 and embedded in question body. Common molecule presets (Benzene, Glucose, H₂O, NaCl, etc.).
- Reaction equation editor: arrow notation (→, ⇌, ↔) with correct rendering

**Biology (Role 22) — Annotated Diagram Upload:**
- "Upload Diagram" button: upload a base image (anatomy diagram, cell structure, plant/animal tissue image) — PNG/JPG ≤ 5MB
- After upload, an annotation overlay editor: add text labels positioned over specific areas of the image (with arrow connector lines). Labels are stored as JSON overlay on the base image, rendered client-side as SVG overlay.
- "Export Annotated Diagram" → composite image (base + labels) saved to S3, embedded in question body
- Without annotation: plain image upload also works (Biology diagrams sometimes used without labels, with the question asking students to identify structures)

**English (Role 23) — Rich Text + Passage Integration:**
- Standard rich text toolbar (bold, italic, underline, lists)
- No special equation or diagram tools
- When in Passage Set mode: the question body editor shows a simplified version ("Question text — refers to the passage above" hint) — the passage is shown in a read-only panel above the MCQ editor

**General Knowledge (Role 24) — Rich Text + Image:**
- Standard rich text toolbar
- Image upload (for charts, graphs, maps, newspaper clippings used in GK questions)
- `valid_until` date is always visible and always required (GK questions are almost always time-sensitive)

**Reasoning (Role 25) — Pattern/Matrix Image Upload:**
- "Upload Pattern" button: upload the pattern or matrix image (PNG/JPG ≤ 3MB) that forms the question stem
- Image preview renders in the editor body with a caption field below it
- Sequence/series builder (optional): structured tool to define a numerical or alphabetical series without needing to upload an image

**Computer Science (Role 26) — Code Block with Syntax Highlighting:**
- "Insert Code" toolbar button → code block editor with language selector (Python · C · C++ · Java · SQL · JavaScript · HTML)
- Monaco editor (VS Code engine) embedded in a modal with syntax highlighting, line numbers, bracket matching
- "Insert" embeds the code as a styled `<pre><code class="language-{x}">` block — rendered with Prism.js on display
- Output field (optional): "Expected Output" for code evaluation questions

**Regional Language (Role 27) — Unicode IME + Script Validation:**
- Telugu IME: integrated Aksharamukhi transliteration keyboard (type in Roman → renders in Telugu Unicode block U+0C00–U+0C7F)
- Devanagari IME: similar transliteration for Hindi (U+0900–U+097F)
- Urdu IME: right-to-left input with Nastaliq rendering (U+0600–U+06FF)
- **Script Validation**: on save-draft, a backend validator checks that the question body contains at least one character in the declared language's Unicode block. If a Telugu question contains only ASCII or Devanagari: validation error "Question body does not appear to contain Telugu script. Please verify." — non-blocking warning (SME can override by clicking "Proceed Anyway" which logs a flag).
- Multiple script support: a single question can mix Telugu and English (common in State Board papers) — validation checks that the primary target script is present, not that it's exclusive.

---

### Section 4 — Answer Options

**Layout:** Four options (A, B, C, D) in a vertical list below the question body.

Each option:
- Label: "Option A" / "Option B" / "Option C" / "Option D"
- Rich editor (same subject-specific toolbar as question body — SME can use LaTeX in options for Math, formula builder for Chemistry, etc.)
- Radio button: "✓ Mark as Correct Answer" — exactly one option must be marked correct. If SME tries to submit with no correct answer marked: validation error.
- Inline character count

**Option count:** Minimum 4 options always. Maximum 6 options (for exam types that use more than 4 options — rare but supported). "Add Option" button appears if < 6 options exist.

**Option randomisation note:** SME labels options A/B/C/D but the exam engine randomises option order per student at exam-delivery time. The question body should never say "In option B, the value is..." — a lint warning appears if the question body contains "option A/B/C/D" text: "⚠ Your question text mentions specific option labels. The exam engine randomises option order — students may not see options in the same order. Consider rephrasing."

---

### Section 5 — Explanation

**Purpose:** Mandatory explanation for every question — shown to students after exam submission as the "solution walkthrough."

**Field:** Rich editor (same subject-specific toolbar), mandatory, minimum 30 characters.
- Character count with 30-char minimum indicator
- If SME tries to submit with explanation < 30 chars: validation error "Explanation must be at least 30 characters. A good explanation helps students understand why the correct answer is right."
- For Math/Physics/Chemistry: explanation typically shows the full working. The same LaTeX/formula tools are available here.
- For comprehension questions: explanation cites the passage paragraph that supports the answer.

---

### Section 6 — Tagging Panel (Right Rail)

**Purpose:** All metadata that determines how this question is categorised, routed, displayed, and used in exams. Always visible. Required fields validated on Submit — not on individual change (to avoid constant errors while SME is mid-tagging).

**Fields in order:**

**1. Subject (locked)**
Displays the SME's assigned subject — not editable. "Mathematics" (Role 19). If the SME has multiple assigned subjects (rare — Regional Language Role 27 covers Telugu/Hindi/Urdu): a dropdown scoped to those subjects only.

**2. Topic (required, cascading)**
Dropdown populated from D-09 taxonomy for the selected subject. On change: fires `?part=taxonomy-cascade&subject={id}&topic={id}` to load subtopics. Includes only Active topics (Archived topics hidden).

**3. Subtopic (optional, cascading)**
Populated after Topic selection. Nullable — not all topics have subtopics. Dropdown from D-09.

**4. Difficulty (required)**
Radio group: Easy · Medium · Hard
- Tooltip on each: calibration rubric from D-09 Style Guide for this subject (e.g. Math: "Easy = direct formula application, one step · Medium = 2-3 step derivation · Hard = multi-concept, derivation + interpretation")
- Rubric opens in a small popover on hover — SME can reference without leaving the tagging panel

**5. Bloom's Taxonomy Level (required)**
Dropdown: Recall · Understand · Apply · Analyse · Evaluate · Create
- Tooltip: brief definition of each level
- Default: none selected — SME must choose

**6. Exam Types (required, multi-select)**
Checkbox group: SSC CGL · SSC CHSL · RRB NTPC · RRB Group D · AP State Board · TS State Board · UPSC Prelims · Online
- At least one must be selected
- On change: fires `?part=freeze-check&exam_types={csv}` — async check against content freeze dates (D-10). If any selected exam type is in freeze period: amber inline warning "SSC CGL is in content freeze until 15 April 2026 — submissions for this exam type will be blocked." The warning is inline in the tagging panel, not a modal interrupt.

**7. Content Type (required — Amendment G5)**
Radio group: Evergreen · Current Affairs · Time-Sensitive

| Type | Meaning | `valid_until` Required? |
|---|---|---|
| Evergreen | Factual content unlikely to change (Math, Science laws, Grammar rules) | No |
| Current Affairs | GK questions about recent events (Finance Minister, Latest census data, Recent summits) | Yes — mandatory |
| Time-Sensitive | Content that will become outdated (Union Budget 2025–26 specifics, Recent court verdict) | Yes — mandatory |

**8. Valid Until (conditionally required — Amendment G5)**
Date picker: shown and required only when Content Type = Current Affairs or Time-Sensitive.
- Minimum date: tomorrow (cannot expire immediately)
- For GK SME (24): a suggested expiry helper appears: "Current Affairs: typically 6–12 months. Time-Sensitive: match the event's relevance window (e.g. budget specifics: 1 year)."
- Hidden (not required) when Content Type = Evergreen

**9. Access Level (required — Amendment G4)**
Dropdown: Platform-Wide · School Only · College Only · Coaching Only

| Level | Meaning |
|---|---|
| Platform-Wide | Available to all 2,050 tenants in all exam configurations |
| School Only | Restricted to school-tier tenant exam pools — Board exam content for school students |
| College Only | Restricted to college/intermediate-tier tenants |
| Coaching Only | Exclusive to coaching centre tenants — premium content for competitive exam preparation |

- Default: Platform-Wide
- Tooltip: "Access level is enforced at the exam engine level — not just a UI filter. A Coaching Only question will not appear in school or college exams even if the SME selects it for those exam types."

**10. High Stakes Flag (checkbox — Amendment G7)**
"Mark as High Stakes — requires 2 independent reviewers before approval"
- Checkbox, default unchecked
- On check: amber tooltip — "High Stakes questions require 2 sequential Reviewer passes (Committee Review). Only use for UPSC, State Board, or other high-impact questions where a single reviewer error could affect many students. Can also be flagged by the Reviewer in D-03."
- When checked: question goes into the committee review queue in D-03 (both Reviewer passes must be completed before the question reaches D-04 Approval Queue)

**11. Source Attribution (required)**
Radio group: Original · Adapted from Textbook · Past Exam Paper

If "Adapted from Textbook": text input for "Book Title + Author + Edition" (free text, required)
If "Past Exam Paper": two inputs: "Exam Name" (free text) + "Year" (4-digit number)

Rationale: Copyright compliance — questions sourced from textbooks or past papers must be tracked. "Original" means the SME authored it themselves. The exam engine will never publish an "Adapted" question without attribution recorded. DPDPA compliance: attribution tracks IP provenance, not SME identity.

**12. SME Notes (optional)**
Free text, max 500 chars. Private note visible only to Reviewer and Approver in their drawer views — not shown to students. Used for: "Reference: NCERT Chemistry Ch.5 p.127" or "This is a tricky wording — reviewers may want to verify option B's calculation independently."

---

### Section 7 — Duplicate Detection (Amendment G1)

**Trigger:** Fires automatically on every **Save as Draft** action (not on every keystroke). The check is async — the question is saved immediately, and the duplicate check result arrives separately via `?part=duplicate-check`.

**Mechanism:**
1. Save-draft API call returns immediately with `question_id` and `state: DRAFT`
2. Celery task `portal.tasks.content.check_question_duplicates` is queued — computes embedding of the new question body via the active embedding model (configured in C-15), then queries `content_question_embeddings` via pgvector:
   ```sql
   SELECT question_id, 1 - (embedding <=> $1::vector) AS similarity
   FROM content.content_question_embeddings
   ORDER BY embedding <=> $1::vector
   LIMIT 10
   ```
3. Results with similarity ≥ 0.80 are stored in `content_duplicate_check_results` with the source question ID
4. HTMX polls `?part=duplicate-check&question_id={uuid}` every 3s until result appears — typical completion: < 30 seconds
5. If matches found: non-blocking orange banner below the question body editor: "⚠ Possible Duplicates Found — {N} similar questions already in the bank" with a "View Matches" button

**Duplicate Results Panel (triggered by "View Matches"):**
Inline panel below the question body (not a modal — SME keeps editing while reviewing matches):
- Top 5 matches, each showing: similarity score (e.g. "87% similar") · truncated question text · topic · difficulty · state (Published / In Review / etc.) · "View Full" link (opens the matched question in a read-only overlay)
- Below the matches: "Acknowledge and Continue" button — SME confirms they have reviewed the duplicates and chooses to proceed (logged as `duplicate_acknowledged: true` on the question record)
- No hard block: the duplicate check is informational. If the SME is intentionally creating a variant of an existing question (different difficulty, different context), they can proceed after acknowledgement.

**If no matches found:** Small green indicator "No duplicates found" appears briefly near the Save button, then fades — no banner needed.

**If Celery task fails:** After 60s without a result, `?part=duplicate-check` returns a soft warning: "Duplicate check unavailable — proceed with caution. The review team will perform a manual duplicate check." — not a blocker.

---

### Section 8 — Revision Mode (Split-View)

**Triggered by:** `/content/sme/question/<uuid>/edit/?mode=revision` — opened from "Revise Now" button in D-01 Returned tab or from the D-01 My Questions table.

**Layout:** Full-width split screen (two equal columns, each ~48%):

**Left panel (read-only — "Previous Submitted Version"):**
- Amber header bar: "Version Submitted for Review — Reviewer Comment Below"
- Full rendered question body (LaTeX/diagrams/code blocks rendered — exactly what the Reviewer saw)
- All 4 options with correct answer marked
- Explanation
- All tags (topic, difficulty, exam types, access level, etc.)
- **Reviewer comment highlighted in amber at the top of the left panel** — the most important piece of information for the SME
- Return reason category badge (e.g. "Factual Error")
- Return date and time

**Right panel (editable — "Your Revision"):**
- Identical to the standard editor but pre-populated with the current question state (which may already have some edits if this is a partial revision)
- Subject-specific toolbar active
- Tagging panel on the right side of this column (not sticky — nested within the panel)
- Autosave active

**Bottom action bar (spanning full width):**
- "Save Draft" — saves current right-panel state as draft, stays in split-view
- "Submit Revised Question" — validates all required fields, submits. Question state changes to `UNDER_REVIEW` with `revision_count` incremented. Revision #2+ is flagged in D-03 Reviewer queue as "Revision ×2" — indicates a persistent issue needing careful attention.
- "Discard Changes" — reverts right panel to the submitted version state (loses unsaved changes in right panel — confirmation modal required)

**Revision tracking:** On submit, a `content_question_versions` record is created storing the full snapshot of the prior submitted version. This is what the Reviewer sees in D-03 "Return History" and what D-12 Audit & Version History shows. The diff between the submitted version and the newly revised version is computed and stored field-by-field.

---

### Section 9 — Passage Set Mode (Amendment G9)

**Triggered by:** Mode toggle (English and GK SMEs by default; other subjects can switch via toggle). Or by URL: `/content/sme/question/new/?mode=passage-set`.

**Use case:** Reading Comprehension questions, Map/Passage-based GK questions (UPSC Prelims "Read the following passage and answer questions 1–4:"), Matching questions based on a shared data table.

**Step 1 — Create the Passage:**

Full-width passage editor above the question list:
- Label: "Passage / Stimulus"
- Rich text editor (bold, italic, underline, ordered lists, blockquote for source attribution)
- Image upload (for maps, graphs, charts that serve as the passage stimulus)
- Word count: 50 word minimum · 2,000 word maximum (hard limit enforced at save — prevents uploading entire textbooks)
- Passage subject tags (same Subject/Topic/Subtopic selectors — applies to all linked questions as the base context)
- Exam Types multi-select (applies to all linked questions)
- Passage Source Attribution (Original / Adapted from Published Source [title + year])
- "Save Passage" button — passage is saved to `content_question_set` with state `DRAFT`

**Step 2 — Add Linked Questions:**

After passage is saved, a "Questions in this Set" panel appears below the passage editor:
- "Add Question" button — opens a compact inline MCQ editor (same rich editor + all 4 options + explanation + tagging panel, but Subject and Exam Types are pre-filled from the passage and locked — individual questions cannot override the passage's subject or exam types)
- Question list: shows all linked questions in order (Q1, Q2, Q3, … up to Q8 maximum)
- Drag to reorder questions (question order is saved — Reviewer sees them in this order)
- Remove question from set (confirmation modal — "Remove Q3 from this set? The question will be deleted.")
- Minimum 2 questions required before set can be submitted

**Step 3 — Submit the Set:**

"Submit Set for Review" button (appears when ≥ 2 questions are complete):
- Validates: passage has ≥ 50 words · each question has ≥ 4 options · exactly 1 correct answer per question · explanation ≥ 30 chars per question
- On submit: all questions in the set transition to `UNDER_REVIEW` simultaneously — a single `content_question_set` record with `state: SUBMITTED`, all `content_question_set_items` with their individual question UUIDs
- In D-03 Review Queue: the set appears as a single row with a "Set: {N} Questions" indicator — the Reviewer opens the set review drawer which shows the full passage + all N questions in sequence

**Passage Set constraints:**
- A question can belong to at most one set at a time
- Questions within a set cannot be individually submitted for review outside the set
- If the Reviewer returns a specific question within the set (not the whole set): that question's state goes to `RETURNED`, the others remain `UNDER_REVIEW`. The set as a whole is marked `PARTIALLY_RETURNED`. SME revises only the returned question; the others stay in review.
- If the Reviewer determines the passage itself is flawed: flags the set as "Passage Return" — all questions return to `RETURNED` simultaneously with the passage feedback displayed prominently.
- Approver constraint: cannot publish any question in the set until all questions in the set reach `PENDING_APPROVAL`. Once all are pending, Approver can approve individually or use "Approve Set" batch action.

---

### Section 10 — Save, Submit & Validation

**Autosave:**
Every 30 seconds while the SME is actively editing, an autosave fires: `POST /content/sme/question/<uuid>/autosave/` with the current editor state as JSON. Response updates the "Saved as Draft" timestamp. If the network connection is lost: autosave queue holds up to 5 pending saves and retries every 10s on reconnect. The SME sees "Save failed — reconnecting…" in the status bar.

**Optimistic Locking — Concurrent Edit Conflict Detection:**

A question in `DRAFT` or `RETURNED` state can theoretically be opened in two browser tabs simultaneously (or by the same SME on two devices). Without conflict detection, the last autosave wins silently — overwriting the other session's work.

**Mechanism:**
- On page load, the server embeds a `version_token` (the `updated_at` timestamp as a Unix millisecond integer) into the editor page as a hidden field: `<input type="hidden" id="version_token" value="{ts}">`.
- Every autosave request includes the `version_token` in the POST body.
- Server-side: before writing the autosave, the view queries `SELECT updated_at FROM content_question WHERE id = {uuid}` and compares it to the submitted `version_token`.
  - **Match** (no other session has written since this tab loaded): write proceeds normally. Response includes the new `version_token` (updated `updated_at`). The client replaces its stored token.
  - **Mismatch** (another session wrote after this tab loaded): server returns HTTP 409 Conflict with a JSON body: `{"conflict": true, "server_content": "<truncated 200 chars of server-side question body>", "server_updated_at": "<ISO timestamp>"}`.

**Conflict UI (on 409 response):**
The editor status bar changes from "Saved as Draft" to a persistent amber banner:

> ⚠ **Edit Conflict Detected**
> This question was saved from another session {N} minutes ago. Your local changes have not been saved.
> **[Keep My Version]** &nbsp;&nbsp; **[Load Server Version]** &nbsp;&nbsp; **[Show Differences]**

- **"Keep My Version"**: forces an overwrite save with a special `force=true` parameter. Server accepts unconditionally and writes the client content. Old version is snapshotted to `content_question_draft_history` before overwrite (so the server version is not lost permanently).
- **"Load Server Version"**: discards local edits and reloads the editor with the server's current content. Confirmation: "This will discard your unsaved local changes. Continue?" Local content is lost (not saved to history — it was never committed).
- **"Show Differences"**: opens a side-by-side diff view in a modal: left = server version · right = local version. Differences highlighted. SME can manually reconcile by copying text between panels. After reviewing: shows both "Keep My Version" and "Load Server Version" buttons.

**Conflict prevention (primary measure):** A warning banner appears when the editor detects that the same question UUID is open in another tab of the same browser session (via `BroadcastChannel` API): "This question is open in another tab. Editing in both tabs simultaneously may cause conflicts. Close the other tab to continue." — non-blocking, advisory only.

**`content_question_draft_history` (new model for conflict overwrite snapshots):**
| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `question_id` | FK → content_question | — |
| `body_snapshot` | text | Full question body JSON at time of snapshot |
| `snapshotted_at` | timestamptz | — |
| `snapshot_reason` | varchar | `conflict_overwrite` · `pre_submit` |

Retained for 30 days, then purged. Accessible to the SME via a "Draft History" link at the bottom of the editor (shows last 5 snapshots with timestamp — SME can restore any snapshot by clicking "Restore This Version" which loads the snapshot into the editor as the current content).

**Manual "Save as Draft":**
- Available at all times via button in bottom action bar
- Also triggers duplicate check (G1)
- Does NOT validate required fields — SME can save incomplete work

**"Submit for Review":**
Full validation runs:
1. Question body: not empty, > 10 characters
2. All 4 options filled
3. Exactly 1 correct answer marked
4. Explanation: ≥ 30 characters
5. Topic: selected
6. Difficulty: selected
7. Bloom's Level: selected
8. Exam Types: at least 1 selected
9. Content Type: selected
10. Valid Until: present if Content Type ≠ Evergreen
11. Access Level: selected
12. Source Attribution: selected (and required text fields filled if not Original)
13. **Content Freeze check**: if any selected exam type is in freeze period (from D-10 `content_exam_freeze` table) — hard block: "SSC CGL content submissions are frozen from 10 March to 30 March 2026. Remove SSC CGL from exam types, or wait until the freeze lifts, to submit." Submit button remains disabled. The SME can still save as Draft.
14. **Script validation (Regional Language only)**: if assigned subject is Regional Language — check Unicode block presence in question body and options

All validation errors shown as inline field-level messages — not a single modal. The SME can see exactly which fields need fixing without losing their place.

On successful submit:
- Question state transitions from `DRAFT` to `UNDER_REVIEW`
- `revision_count` incremented (if this is a resubmission)
- Celery task auto-assigns to the primary Question Reviewer for this subject (from D-15 `content_reviewer_assignment` — primary reviewer for subject, or backup if primary queue > threshold)
- SME sees success toast: "Question submitted for review. It has been assigned to the review queue." with a "View in Dashboard" link back to D-01
- Page clears for new question creation (or redirects back to D-01 if this was a revision)

---

## 5. Data Models

### `content_question`
| Field | Type | Notes |
|---|---|---|
| `id` | UUID | Primary key |
| `author_id` | FK → auth.User | The SME — immutable after creation |
| `subject_id` | FK → content_taxonomy_subject | — |
| `topic_id` | FK → content_taxonomy_topic | — |
| `subtopic_id` | FK → content_taxonomy_subtopic | Nullable |
| `question_body` | text | HTML — includes inline CloudFront image URLs + rendered LaTeX references |
| `question_body_plain` | text | Plain text version — used for pgvector embedding and full-text search |
| `option_a` | text | HTML |
| `option_b` | text | HTML |
| `option_c` | text | HTML |
| `option_d` | text | HTML |
| `option_e` | text | Nullable — for 5-option questions |
| `option_f` | text | Nullable — for 6-option questions |
| `correct_option` | varchar | "a" / "b" / "c" / "d" / "e" / "f" |
| `explanation` | text | HTML |
| `difficulty` | varchar | Easy / Medium / Hard |
| `blooms_level` | varchar | Recall / Understand / Apply / Analyse / Evaluate / Create |
| `exam_types` | varchar[] | Array of exam type codes |
| `content_type` | varchar | Evergreen / CurrentAffairs / TimeSensitive |
| `valid_until` | date | Nullable — required if not Evergreen |
| `access_level` | varchar | PlatformWide / SchoolOnly / CollegeOnly / CoachingOnly |
| `high_stakes` | boolean | Default false — triggers committee review in D-03 |
| `source_attribution_type` | varchar | Original / AdaptedFromTextbook / PastExamPaper |
| `source_attribution_detail` | text | Nullable — book/exam details if not Original |
| `sme_notes` | text | Nullable — visible to Reviewer/Approver in drawer |
| `state` | varchar | DRAFT · UNDER_REVIEW · RETURNED · PENDING_APPROVAL · PUBLISHED · ARCHIVED · AMENDMENT_REVIEW |
| `revision_count` | int | Default 0 — incremented on each resubmit after return |
| `duplicate_acknowledged` | boolean | Default false — set true when SME clicks "Acknowledge and Continue" after duplicate check |
| `question_set_id` | FK → content_question_set | Nullable — links to passage set (G9) |
| `created_at` | timestamptz | — |
| `updated_at` | timestamptz | — |
| `state_changed_at` | timestamptz | — |

### `content_question_versions` (snapshot on each submit)
| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `question_id` | FK → content_question | — |
| `version_number` | int | 1, 2, 3… increments on each submit |
| `snapshot` | jsonb | Full serialised question state at time of submit |
| `reviewer_comment` | text | Nullable — populated when Reviewer returns this version |
| `reviewer_return_reason` | varchar | Nullable — reason category |
| `created_at` | timestamptz | Submit timestamp |

### `content_question_embeddings` (pgvector — shared content schema)
| Field | Type | Notes |
|---|---|---|
| `question_id` | FK → content_question | — |
| `embedding` | vector(1536) | pgvector — populated by Celery embedding task within 30s of save-draft |
| `model_version` | varchar | Embedding model ID (from C-15 Embedding Model Manager) |
| `created_at` | timestamptz | — |

HNSW index: `CREATE INDEX ON content_question_embeddings USING hnsw (embedding vector_cosine_ops) WITH (m=16, ef_construction=400)`

### `content_duplicate_check_results`
| Field | Type | Notes |
|---|---|---|
| `source_question_id` | FK → content_question | Question being authored |
| `matched_question_id` | FK → content_question | Matched question |
| `similarity_score` | decimal | 0.00–1.00 cosine similarity |
| `checked_at` | timestamptz | — |

### `content_question_set` (Amendment G9)
| Field | Type | Notes |
|---|---|---|
| `id` | UUID | Primary key |
| `passage_body` | text | HTML — the comprehension passage text |
| `passage_body_plain` | text | Plain text |
| `subject_id` | FK → content_taxonomy_subject | — |
| `topic_id` | FK → content_taxonomy_topic | — |
| `exam_types` | varchar[] | Shared across all linked questions |
| `source_attribution_type` | varchar | — |
| `source_attribution_detail` | text | Nullable |
| `author_id` | FK → auth.User | SME who created the set |
| `state` | varchar | DRAFT · SUBMITTED · PARTIALLY_RETURNED · PASSAGE_RETURNED · PUBLISHED · ARCHIVED |
| `created_at` | timestamptz | — |

### `content_question_set_items` (Amendment G9)
| Field | Type | Notes |
|---|---|---|
| `set_id` | FK → content_question_set | — |
| `question_id` | FK → content_question | — |
| `question_order` | int | 1-based display order within the set |

---

## 6. Access Control

| Gate | Rule |
|---|---|
| Page access — Create | `PermissionRequiredMixin(permission='content.add_question')` — Roles 19–27 only |
| Page access — Edit | `PermissionRequiredMixin(permission='content.change_question')` + `question.author == request.user` — SME can only edit their own questions |
| Page access — Revision | Same as Edit, additionally `question.state == 'RETURNED'` — if state is not RETURNED, redirect to standard edit with a notice |
| Page access — Preview | Content Director only — separate route, read-only Django view with `PermissionRequiredMixin(permission='content.view_all_questions')` |
| Subject scope on save | View validates `question.subject_id in request.user.sme_profile.assigned_subjects` before save — returns 403 with audit log entry if violated |
| Correct option | Backend validates exactly 1 correct option on submit — client-side JS also enforces but is not trusted |
| Content freeze | Checked server-side on Submit (not just client-side) — if freeze active for any selected exam type, HTTP 400 with specific error |
| Script validation | Backend regex check for Unicode block presence — client-side feedback is UX only |

---

## 7. Edge Cases & Error States

| Scenario | Behaviour |
|---|---|
| Network drops mid-edit | Autosave queue holds last 5 unsaved changes, retries every 10s on reconnect. "Save failed — reconnecting…" status indicator. If question was never saved: local storage backup of editor content (clears after successful save or page close). |
| Duplicate check Celery task never completes | After 60s, poll stops and shows: "Duplicate check unavailable — proceed with caution." SME can still submit. Reviewer will manually check against D-11 published bank. |
| SME uploads an image > 2MB | S3 presigned URL policy rejects it immediately — client shows "File too large. Maximum 2MB per image." before upload even begins. |
| CloudFront URL embedded in question body becomes unreachable | S3 lifecycle rule protects content-media from deletion while any question references the URL. A nightly integrity check identifies dangling URLs and flags them to Content Director as orphan media issues. |
| SME tries to edit a question in UNDER_REVIEW state | Route returns 403 with message: "This question is currently with a Reviewer and cannot be edited. Wait for the review decision." |
| SME in Regional Language (27) submits a question with only English text | Script validation warning: "No Telugu/Hindi/Urdu characters detected. Are you sure this is a Regional Language question?" — non-blocking with "Override and Submit" option. Logged with `script_validation_overridden: true`. |
| Exam type freeze activates while SME is mid-edit | On Submit click, freeze check fires server-side — if newly frozen since the SME began editing, error displayed: "SSC CGL entered content freeze while you were editing. Please deselect SSC CGL to submit." Autosaved draft is preserved. |
| Passage Set mode: Reviewer returns 1 of 4 questions | Only the returned question shows "Returned" state in D-01. Set state becomes `PARTIALLY_RETURNED`. SME revises only the returned question via the same split-view but within the passage set context (passage is shown read-only above the revision). The other 3 questions remain `UNDER_REVIEW`. |
| SME deletes their D-01 "My Media" image that is still referenced in a saved draft | D-01 prevents deletion if "Used In > 0". But if a race condition allows deletion: on next autosave, the question body references a dead CloudFront URL. The integrity checker flags this within 24 hours. |
| SME tries to add more than 8 questions to a passage set | "Add Question" button is disabled after 8 questions with tooltip "Maximum 8 questions per passage set." |

---

## 8. Integration Points

| Integration | Direction | What Flows | Mechanism |
|---|---|---|---|
| D-09 Taxonomy Manager | D-02 reads | Subject/Topic/Subtopic dropdown data | ORM with Memcached 10-min cache on taxonomy tree per subject |
| D-10 Content Freeze Config | D-02 reads | Freeze dates per exam type (freeze-check part-route) | `content_exam_freeze` table — direct ORM read, no cache (freeze status must be current) |
| D-15 Reviewer Assignments | D-02 triggers read | On submit: which reviewer to auto-assign (primary for subject, or backup if queue > threshold) | `content_reviewer_assignment` table read by post-submit signal |
| C-15 Embedding Model Manager | D-02 → Celery → pgvector | Question embedding for duplicate check | Celery task calls the active embedding model API (configured in C-15), stores vector in `content_question_embeddings` |
| D-03 Review Queue | D-02 → D-03 | Submitted question enters review queue | State change to `UNDER_REVIEW` + Celery notification to assigned reviewer |
| D-01 SME Dashboard | D-01 → D-02 | Navigation: Edit, Revise Now, New Question | URL parameters pass `?next=` for return navigation; revision mode passed as `?mode=revision` |
| S3 (ap-south-1) | D-02 → S3 | Image uploads | Presigned URL generated by view, client uploads directly to S3 `content-media/` — no binary through Django |
| CloudFront | S3 → CloudFront | CDN delivery of uploaded images | CloudFront distribution pointed at `content-media/` — URL embedded in question HTML |

---

---

## 9. UI Patterns & Page-Specific Interactions

### Layout & Responsive Behaviour
- **Desktop (≥1280px):** Two-column — editor area (65% left) + tagging rail (35% right, sticky).
- **Tablet (768–1279px):** Same two-column but tagging rail collapses to a "Tags" bottom drawer toggle. Tap "View Tags" to open the tagging rail as a bottom sheet.
- **Mobile (<768px):** Single column. Question body editor full width. Tagging rail accessible via "Tags" floating action button → full-screen bottom sheet. Submit button sticky at bottom.

### Form Validation
All validation fires on blur (field loses focus) AND on Submit attempt:

| Field | Validation rule | Error message |
|---|---|---|
| Question body | Required, ≥ 20 chars | "Question body is required (min 20 characters)" |
| Options A–D | All 4 required, each ≥ 5 chars | "All four options are required" |
| Correct answer | One option must be selected | "Select the correct answer" |
| Explanation | Required, ≥ 30 chars | "Explanation required (min 30 characters)" |
| Topic | Required (from taxonomy cascade) | "Select a topic for this question" |
| Difficulty | Required | "Select a difficulty level" |
| Exam Type(s) | At least 1 required | "Select at least one exam type" |
| Valid Until | Required if Content Type ≠ Evergreen | "Set an expiry date for non-Evergreen content" |
| Passage body (G9) | Required, 50–2,000 words | "Passage must be 50–2,000 words" |

Submit button is disabled (greyed, tooltip "Complete all required fields") until all required fields pass client-side validation.

### Toast Messages
| Action | Toast |
|---|---|
| Save as Draft | ✅ "Draft saved" (Success 4s) |
| Submit for Review | ✅ "Submitted for review" (Success 4s) |
| Submit blocked — content freeze | ⚠ "Submission blocked: {Exam Type} is in content freeze until {date}" (Warning, persistent) |
| Duplicate detected (≥ 0.80 similarity) | ⚠ "Possible duplicate detected — review before submitting" (Warning, 8s) |
| Auto-save fail (network) | ❌ "Auto-save failed — check your connection" (Error, persistent) |
| Edit conflict detected (409) | ⚠ Amber banner (not toast — persists until resolved): "Edit Conflict Detected — another session saved this question. Choose how to resolve." |
| Conflict resolved — Keep My Version | ✅ "Your version saved. The server version was archived." (Success 4s) |
| Conflict resolved — Load Server Version | ✅ "Server version loaded. Your local changes were discarded." (Success 4s) |
| Draft History snapshot restored | ✅ "Draft restored from {timestamp}. Review before saving." (Success 4s) |
| Passage Set submitted | ✅ "Passage set submitted — {N} linked questions sent for review" (Success 4s) |

### Loading States
- **Taxonomy cascade (Topic dropdown):** Spinner inside dropdown while subtopics load from Memcached/ORM. Dropdown disabled during load.
- **Duplicate check panel:** "Checking for duplicates…" skeleton with progress dots (polls `?part=duplicate-check` every 3s). Timeout at 30s: "Duplicate check is taking longer than expected. [Skip and proceed]".
- **LaTeX/SMILES preview:** Inline spinner next to rendered preview while MathJax/RDKit.js renders. If render fails: "Preview unavailable — check your formula syntax."
- **Passage word count:** Live counter updates on every keystroke. No loading state needed.

### Mobile-specific Drawer Behaviour (Revision Mode)
- On mobile, the split-view (previous version left / editable right) collapses to a tab interface: "Previous Version" tab (read-only) · "Edit" tab (editable). Reviewer comment pinned at top as a yellow banner.

### Role-Based UI
- **Subject selector:** Locked to SME's assigned subject (read-only display, not dropdown). Director has no access to D-02.
- **High Stakes flag (G7):** Visible to all SME roles. Shown as a checkbox: "Flag as High Stakes (requires committee review)".
- **Access Level field (G4):** All SME roles see this. Platform-Wide selected by default.
- **Passage Set toggle (G9):** Shown by default for English (23) and GK (24). Shown but not default for all other subjects.

---

*Page spec complete.*
*Amendments applied: G1 (Duplicate Detection) · G4 (Access Level) · G5 (Content Type + Valid Until) · G7 (High Stakes Flag) · G9 (Passage Set Mode)*
*Gap amendments: Gap 11 (Auto-save conflict detection with optimistic locking — Section 10 autosave block + `content_question_draft_history` model)*
*Next file: `d-03-review-queue.md`*
