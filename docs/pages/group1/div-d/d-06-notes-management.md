# D-06 — Notes Management

> **Route:** `/content/notes/`
> **Division:** D — Content & Academics
> **Primary Role:** Notes Editor (Role 30)
> **Read Access:** Content Director (18) — Director review actions in this page + read of published library
> **File:** `d-06-notes-management.md`
> **Priority:** P0 — Notes go live in institution portals from onboarding day 1
> **Status:** ⬜ Not started
> **Amendments:** G3 (Director Review Toggle — per-subject director approval gate before notes publish)

---

## 1. Page Name & Route

**Page Name:** Notes Management
**Route:** `/content/notes/`
**Part-load routes:**
- `/content/notes/?part=kpi` — KPI strip
- `/content/notes/?part=incoming-table` — Incoming Queue tab table
- `/content/notes/?part=structuring-drawer&note_id={uuid}` — note structuring drawer content
- `/content/notes/?part=published-table` — Published Library tab table
- `/content/notes/?part=inprogress-table` — In Progress tab table
- `/content/notes/?part=director-review` — Director Review panel (pending director decisions)
- `/content/notes/?part=conversion-status&note_id={uuid}` — file conversion status polling

---

## 2. Purpose (Business Objective)

Notes are the study resource layer that sits alongside the MCQ question bank. Where questions test knowledge, notes build it. Faculty across 1,000 schools, 800 colleges, and 100 coaching centres upload their teaching materials — lecture slides, chapter summaries, past-year analysis documents — through the institution portal. These materials arrive as raw PPTX, DOCX, or PDF files and must be transformed into structured, tagged, searchable resources before students can access them.

The Notes Editor is the single role responsible for this transformation. They receive every faculty upload, verify format conversion, apply structured metadata (subject, topic, exam type, difficulty level, academic year), and decide whether to publish immediately or hold for Director review.

At scale — 10,000 notes target across all subjects and exam types — the quality and discoverability of the notes library directly affects how useful the platform is to students between exams. Untagged notes are invisible. Incorrectly tagged notes surface in irrelevant searches. The Notes Editor's structured metadata work is what converts raw faculty uploads into educationally useful resources.

**Business goals:**
- Process all faculty-uploaded notes from S3 landing bucket to published state with full metadata
- Handle file format conversion failures gracefully without losing the original file
- Enforce per-subject Director approval when the Director Review Toggle is enabled (G3)
- Maintain version history — notes are living documents that faculty update as syllabi change
- Give the Notes Editor a clear view of their in-progress structuring work

---

## 3. User Roles

| Role | Access |
|---|---|
| Notes Editor (30) | Full — Incoming Queue, Structuring Drawer, Published Library (own notes), In Progress, Director Review panel (read — sees Director's decisions) |
| Content Director (18) | Read of all notes + Director review actions (Approve / Return) in D-05 Notes Review tab; Director also has read access to D-06 Published Library for all notes |

---

## 4. Section-Wise Detailed Breakdown

---

### Section 1 — Page Header

- H1: "Notes Management"
- Notes Editor name + role label
- "Notes target" progress: "Published Notes: {N} / 10,000 target" — progress bar
- Auto-refresh indicator on Incoming Queue: "Incoming queue refreshes every 60s"

---

### Section 2 — KPI Strip

| Tile | Metric | Colour Rule |
|---|---|---|
| Incoming Queue | COUNT of notes in `NOTES_INCOMING` state (received, not yet structured) | Amber if > 20 · Red if > 50 (backlog building) |
| In Progress | COUNT of notes with partial metadata saved but not yet published | — |
| Pending Director Review | COUNT of notes in `PENDING_DIRECTOR_REVIEW` state | Amber if > 0 — Director gate is blocking these |
| Published (All-time) | Total `PUBLISHED` notes count | — |
| Published (This Month) | COUNT published this month | — |
| Conversion Failed | COUNT of notes that failed format conversion (PPTX/DOCX → PDF) | Red if > 0 — needs manual intervention |

KPI refreshes every 60s.

---

### Section 3 — Tab Navigation

| Tab | Badge | Default |
|---|---|---|
| Incoming Queue | COUNT of unprocessed incoming notes | ✅ Default |
| In Progress | COUNT of notes with saved draft metadata | — |
| Published Library | No count badge | — |
| Director Review | COUNT of PENDING_DIRECTOR_REVIEW (visible to Notes Editor as status — no action) | — |

---

### Section 4 — Tab: Incoming Queue (Default)

**Purpose:** All notes that faculty have uploaded via institution portals, landed in S3 `notes-raw/`, and are waiting for Notes Editor processing.

**Data pipeline context:**
1. Faculty uploads file via institution portal (PDF / DOCX / PPTX ≤ 50MB)
2. S3 upload triggers `portal.tasks.notes.convert_format` Celery task immediately — PPTX/DOCX → PDF via LibreOffice headless on an ECS task; PDF files pass through unchanged
3. Converted PDF lands in S3 `notes-converted/`
4. `content_notes` record created with `state: NOTES_INCOMING` — appears in Incoming Queue

**Table columns:**

| Column | Description |
|---|---|
| # | Row number |
| File Name | Original uploaded file name |
| Institution | Institution name (school / college / coaching centre) |
| Subject | If faculty tagged it during upload (sometimes blank) |
| Upload Date | When faculty uploaded |
| File Size | Original file size |
| Format | PDF / DOCX / PPTX (original format) |
| Conversion Status | Processing ⏳ / ✅ Ready / ❌ Failed |
| Actions | Download · Open (structured drawer) · [if Failed] Retry / Manual Replace |

**Conversion Status states:**

| Status | Indicator | Notes Editor Action |
|---|---|---|
| Processing | Animated spinner — HTMX polls `?part=conversion-status&note_id={uuid}` every 5s | Wait — typically < 60s |
| ✅ Ready | Green checkmark | Open the Note Structuring Drawer |
| ❌ Failed | Red × with error type | See below |

**Conversion failure handling:**
LibreOffice conversion can fail for: password-protected files · corrupted DOCX/PPTX · files with unsupported media embedded · very large files exceeding LibreOffice memory limit.

Per-row failure actions:
- "Retry" — re-queues the same Celery conversion task. Useful for transient memory limit failures (retry succeeds ~60% of the time on second attempt).
- "Manual Replace" — Notes Editor uploads a manually converted PDF version of the same content. Opens a file upload modal: "Upload PDF replacement for '{filename}'" — new file goes directly to S3 `notes-converted/` without Celery conversion; `conversion_status` set to `ManuallyReplaced`.
- "Return to Faculty" — sends an in-app notification to the institution's admin with: "The file '{filename}' could not be converted. Please re-upload as a plain PDF." State: `NOTES_INCOMING` → `RETURNED_TO_FACULTY`. Note is removed from the incoming queue.

**Batch tagging:**
Multi-select checkboxes + "Batch Tag" button — apply a common Subject+Topic to multiple selected notes before opening each individually for full structuring. Useful when a batch of uploads from the same institution's Physics department arrives — all can be tagged as Subject: Physics before the Notes Editor opens each for detailed structuring.

---

### Section 5 — Note Structuring Drawer

**Trigger:** "Open" button on an Incoming Queue row (only when conversion status is ✅ Ready). 860px right-side drawer.

**Drawer layout: Two-column**
- Left 55%: PDF preview panel (rendered inline via PDF.js — scrollable, full PDF)
- Right 45%: Structured metadata form

**PDF Preview panel:**
- Full PDF rendered inline — Notes Editor reads the document while filling metadata
- Page navigation: "Page 3 / 12" with prev/next buttons
- Zoom controls
- "Download PDF" link (downloads the `notes-converted/` S3 file)

**Metadata form (right panel):**

| Field | Required | Notes |
|---|---|---|
| Title | Yes | Free text, max 200 chars |
| Subject | Yes | Dropdown from D-09 taxonomy — 9 subjects |
| Topic(s) | Yes | Multi-select from D-09, cascading from Subject. Up to 5 topics per note (notes often span multiple topics) |
| Subtopic(s) | No | Multi-select, cascading from selected Topics |
| Class / Standard | No | Free text: "Class 10 / Intermediate Year 2 / Degree Year 3" |
| Exam Type(s) | No | Multi-select: SSC CGL · SSC CHSL · RRB NTPC · RRB Group D · AP Board · TS Board · UPSC Prelims · Online |
| Chapter Reference | No | Free text: "Chapter 5 — Chemical Bonding" |
| Academic Year | No | Year picker: 2024–25 / 2025–26 / etc. |
| Difficulty Level | Yes | Radio: Introductory / Standard / Advanced |
| Language | Yes | Dropdown: English / Telugu / Hindi / Urdu / Bilingual (English+Telugu) |
| Tags | No | Free text, comma-separated — additional searchability keywords |
| Source Institution | Auto-filled | Read-only — institution that uploaded the file |

**Director Review Toggle notice (Amendment G3):**
If the Director Review Toggle is ON for the selected Subject (config set in D-05 Notes Review tab), an amber notice appears below the metadata form: "⚠ Director Approval Required for {Subject} Notes — After you click Publish, this note will be sent to Content Director for review before going live." Notes Editor cannot change this toggle from D-06 — it is a Director-level setting.

**Drawer action bar (bottom):**

- **"Save Progress"** — saves current metadata as a draft without publishing. Note state remains `NOTES_INCOMING`; appears in "In Progress" tab. Notes Editor can close the drawer and return later.
- **"Publish"** — validates required fields. If all valid:
  - Director Review Toggle OFF for this subject: note state → `PUBLISHED` · PDF file moved from S3 `notes-converted/` to S3 `notes-published/`. CloudFront cache for this subject's notes list is invalidated.
  - Director Review Toggle ON for this subject: note state → `PENDING_DIRECTOR_REVIEW`. Note does not go live. Director sees it in D-05 Notes Review tab. Notes Editor sees it in the Director Review tab (read-only) with a "Awaiting Director Approval" indicator.
- **"Return to Faculty"** — sends in-app notification to institution admin with a custom message (text field ≥ 10 chars required): "The uploaded note requires changes. Please re-upload." State: `RETURNED_TO_FACULTY`.

---

### Section 6 — Tab: In Progress

**Purpose:** Notes that the Notes Editor has started structuring (saved metadata draft) but not yet published.

**Table structure:** Same columns as Incoming Queue + "Last Edited" column (when metadata was last saved).

**Action per row:** "Continue Structuring" → opens the Note Structuring Drawer with saved metadata pre-filled.

**Stale indicator:** Notes in In Progress for > 7 days show an amber "7 days" badge — a reminder to either publish or return to faculty.

---

### Section 7 — Tab: Published Library

**Purpose:** All published notes — searchable reference for the Notes Editor to verify what has been published and manage versions.

**Search:** Full-text on title + tags + chapter reference.

**Filters:** Subject · Topic · Exam Type · Academic Year · Difficulty Level · Language · Source Institution · Published Date range

**Table columns:**
Title · Subject · Topics · Published Date · View Count (30 days) · Download Count (30 days) · Version badge (v1, v2, etc.) · Source Institution

**Per-row actions:**

- **"Edit Metadata"** — opens the structuring drawer with all metadata editable. Only metadata changes; the PDF itself is not re-uploaded. On save: metadata updated, logged in `content_notes_audit_log`. Version number does not increment for metadata-only changes.
- **"Unpublish + Edit"** — for cases where the PDF content itself is wrong (not just metadata). Opens a modal: "Unpublish this note for editing? Students will no longer see it until you re-publish." On confirm: state → `NOTES_INCOMING`. Previous version preserved in S3 with `-v1`, `-v2` suffix. Notes Editor then uploads a replacement PDF, re-structures metadata, and re-publishes — this increments the version number (v1 → v2).
- **"Version History" icon** (per row): opens a compact version history panel — all publish events for this note: Date · Notes Editor label · Version · "Restore to this version" (restores previous PDF from S3 versioned key — new publish event created, version incremented).

---

### Section 8 — Tab: Director Review (Read-only for Notes Editor)

**Purpose:** Notes Editor can see the status of notes pending Director review — whether approved or returned, and what the Director's comment was on a return.

**Table:** Title · Subject · Submitted Date · Director Status (Pending / Approved / Returned) · Director Comment (visible to Notes Editor on return)

**No actions for Notes Editor** — this is informational only. The Notes Editor acts on Director's decisions by seeing the return comment and going back to the Incoming Queue / In Progress tab to revise and re-publish.

---

### Section 9 — Note Audit Trail Viewer

**Purpose:** Every significant state change for a note is recorded in `content_notes_audit_log`. The Audit Trail Viewer exposes this log per note, allowing the Notes Editor (and Content Director) to understand the complete lifecycle of any published or unpublished note.

**Access:** Via a "View Audit Trail" action in the Published Library tab (per-row action, accessible to Notes Editor + Content Director). Opens as a 560px right-side panel (not a full drawer — the library table remains visible).

**Panel header:**
- Note title (truncated to 80 chars)
- Note ID (UUID truncated to last 8 chars)
- Current state badge
- "Close ×"

**Audit trail — chronological event list (oldest first):**

Each event card shows:
```
[Event icon]  [Action label]             [Date + Time]
              [Actor label — role only, not personal name]
              [Before → After state, if state change]
              [Comment, if present]
```

**Event types and their display:**

| Action | Icon | Actor | Notes |
|---|---|---|---|
| NoteCreated | 📄 | "Institution Portal (automated)" | When the note record was created from S3 event |
| ConversionComplete | ✅ | "System (Celery)" | LibreOffice conversion success |
| ConversionFailed | ❌ | "System (Celery)" | Shows conversion error detail |
| StructuringStarted | 🖊 | "Notes Editor" | When Notes Editor first opened the structuring drawer |
| MetadataSaved | 💾 | "Notes Editor" | Draft save during structuring |
| Published | 🟢 | "Notes Editor" | Note went live (v1, v2, etc.) — shows version number |
| PendingDirectorReview | ⏳ | "Notes Editor" | Director Review Toggle was ON at publish |
| DirectorApproved | ✅ | "Content Director" | Director approved from D-05 |
| DirectorReturned | 🔴 | "Content Director" | Director returned — Director comment shown in full |
| ReturnedToFaculty | 📤 | "Notes Editor" | Returned to institution for re-upload |
| MetadataUpdated | ✏️ | "Notes Editor" | Metadata-only edit after publish (no version increment) — shows before/after for changed fields |
| Unpublished | ⛔ | "Notes Editor" | Unpublish+Edit started — shows reason (if provided) |
| VersionRestored | 🔄 | "Notes Editor" | A prior S3 version was restored — shows which version |
| DirectorCommentAdded | 💬 | "Content Director" | Director added a comment outside the approval workflow (from D-05) |

**Version timeline strip (above the event list):**
A horizontal version bar showing all published versions: v1 → v2 → v3 (current). Click any version to jump to the events relevant to that version. Versions are visually separated by a thin divider.

**Filters on audit trail:**
- Actor: All · Notes Editor · Director · System
- Event Type: All · Publishes · Returns · State Changes · Metadata Changes

**"Export Audit Log"** button:
Downloads a CSV of all audit events for this note. Columns: Event ID · Action · Actor Role · Before State · After State · Comment · Timestamp. DPDPA compliant — actor personal name is never included, only role label.

---

### Section 10 — Multi-Subject Toggle Rule Clarification

The Director Review Toggle (configured in D-05 Notes Review tab) is a **per-subject** setting. Notes in D-06 span multiple topics within one subject — but a note has exactly one **primary subject** (`content_notes.subject_id`). The toggle applies based on this primary subject.

**Rule:** If the Director Review Toggle is ON for Subject X, ALL notes where `subject_id = Subject X` require Director approval before going live — regardless of how many topics that note spans.

**Multi-topic notes (same subject):** A note covering Topics A, B, and C within Subject X has `subject_id = X`. If the toggle is ON for Subject X, it goes to Director review. The fact that it spans 3 topics does not change this — the subject is the toggle axis, not the topic.

**Multi-subject notes:** The metadata form's Subject field allows only one subject per note (single-select). A note cannot straddle two subjects. If the Notes Editor has content that genuinely covers two subjects (e.g. Physical Chemistry for both Chemistry and Physics syllabi), they must create two separate note records — one per subject — each going through that subject's Director Review Toggle independently.

**Director Toggle change mid-session:** If the Director changes the toggle for Subject X from OFF to ON while the Notes Editor has notes in the "In Progress" tab (unsaved drafts for Subject X): those in-progress notes are NOT retroactively affected. The toggle takes effect on the next "Publish" action. The Notes Editor is shown an amber banner on the In Progress tab for Subject X notes: "⚠ Director Approval now required for {Subject} notes — your next publish will go to Director review before going live."

---

## 5. Data Models

### `content_notes`
| Field | Type | Notes |
|---|---|---|
| `id` | UUID | Primary key |
| `title` | varchar(200) | — |
| `subject_id` | FK → content_taxonomy_subject | — |
| `topics` | UUID[] | Array of topic IDs from content_taxonomy_topic |
| `subtopics` | UUID[] | Nullable array |
| `exam_types` | varchar[] | Multi-select exam type codes |
| `class_standard` | varchar | Nullable free text |
| `chapter_reference` | varchar | Nullable |
| `academic_year` | varchar | e.g. "2025-26" |
| `difficulty_level` | varchar | Introductory / Standard / Advanced |
| `language` | varchar | English / Telugu / Hindi / Urdu / Bilingual |
| `tags` | varchar[] | Free-text searchability tags |
| `source_institution_id` | FK → Institution | The institution that uploaded |
| `notes_editor_id` | FK → auth.User | Notes Editor who structured it |
| `original_filename` | varchar | Faculty's original upload filename |
| `original_format` | varchar | PDF / DOCX / PPTX |
| `s3_raw_key` | varchar | S3 key in `notes-raw/` |
| `s3_converted_key` | varchar | S3 key in `notes-converted/` (after LibreOffice conversion) |
| `s3_published_key` | varchar | S3 key in `notes-published/` (after publish) |
| `conversion_status` | varchar | Processing / Ready / Failed / ManuallyReplaced |
| `conversion_error` | text | Nullable — LibreOffice error message if failed |
| `state` | varchar | NOTES_INCOMING · IN_PROGRESS · PENDING_DIRECTOR_REVIEW · PUBLISHED · UNPUBLISHED · RETURNED_TO_FACULTY · ARCHIVED |
| `version` | int | 1, 2, 3… — incremented on each Unpublish+Edit + Republish cycle |
| `director_comment` | text | Nullable — populated when Director returns a note |
| `created_at` | timestamptz | When faculty uploaded (S3 event time) |
| `published_at` | timestamptz | Nullable |
| `updated_at` | timestamptz | — |

### `content_notes_versions` (S3 version tracking)
| Field | Type | Notes |
|---|---|---|
| `note_id` | FK → content_notes | — |
| `version_number` | int | — |
| `s3_key` | varchar | S3 key for this version's PDF |
| `published_by` | FK → auth.User | Notes Editor |
| `published_at` | timestamptz | — |
| `notes_editor_comment` | text | Nullable — Notes Editor note about what changed in this version |

### `content_notes_audit_log`
| Field | Type | Notes |
|---|---|---|
| `note_id` | FK → content_notes | — |
| `action` | varchar | Published · MetadataUpdated · Unpublished · DirectorApproved · DirectorReturned · ReturnedToFaculty · VersionRestored |
| `actor_id` | FK → auth.User | — |
| `before_state` | jsonb | Nullable |
| `after_state` | jsonb | Nullable |
| `comment` | text | Nullable |
| `created_at` | timestamptz | Immutable |

---

## 6. Access Control

| Gate | Rule |
|---|---|
| Page access | `PermissionRequiredMixin(permission='content.manage_notes')` — Role 30 |
| Content Director read | Content Director can access `/content/notes/` but all write actions (Publish, Unpublish, Batch Tag) are blocked via `{% if has_notes_edit_permission %}` in templates + server-side 403 on POST |
| Director Review decisions | Director's Approve / Return actions occur in D-05 Notes Review tab — D-06 shows the outcome but not the action |
| S3 access | Django view generates S3 presigned URLs for downloads — no direct S3 URL exposed to browser. Presigned URLs expire in 15 minutes. |
| Faculty uploads | Faculty cannot access D-06 directly — they use the institution portal (separate app). Institution portal writes to `content_notes` table and S3. |

---

## 7. Edge Cases & Error States

| Scenario | Behaviour |
|---|---|
| Faculty uploads a 50MB PPTX that LibreOffice cannot handle | Conversion fails with "File too large for conversion" error. Per-row: Retry (reduces batch size), Manual Replace, or Return to Faculty. |
| Notes Editor publishes a note with Director Review Toggle ON, but Toggle is turned off by Director mid-session | The note is already in `PENDING_DIRECTOR_REVIEW` — it stays pending regardless of Toggle change (the Toggle affects future submissions, not retroactive state changes). Director must explicitly approve or return the pending note. |
| Notes Editor tries to Unpublish+Edit a note that is currently in a student's active study session | Notes are not "checked out" — a student viewing a note at the time of unpublish will lose access on next page load or tab switch. No mid-session lock exists. This is an acceptable trade-off: notes are corrective content, not exam sessions. |
| HTMX auto-refresh fires while Notes Editor is mid-structuring in the drawer | Auto-refresh on Incoming Queue table is suspended while any drawer is open (JS flag). Metadata form is never cleared by a background refresh. |
| Two Notes Editors (if multiple roles are eventually created) try to structure the same note simultaneously | Optimistic locking: `content_notes.updated_at` is checked on save. If the server's `updated_at` differs from the client's version at form load, save is rejected with: "This note was modified by another editor. Please refresh and try again." (Last-write-wins is not acceptable for structured metadata.) |
| Director archives a note that a student is actively viewing | Notes are not session-locked — the student's current view continues until they navigate away or refresh. On next load: note is excluded from results (state = ARCHIVED). Acceptable trade-off — this is a rare Director-initiated action on retired content. |
| Notes Editor tries to Edit Metadata on an ARCHIVED note | Blocked at the view layer: "This note has been archived by the Content Director. Contact the Director to restore it before making changes." Notes Editor cannot edit archived notes. |
| S3 `notes-published/` key already exists (version collision) | Notes Management generates a unique key: `notes-published/{subject}/{note_id}/v{version}.pdf`. Version number is always incremented — collision is impossible by design. |
| Incoming Queue accumulates > 100 unprocessed notes | KPI strip shows red badge. No automated processing — Notes Editor must work through the queue manually. If a prolonged backlog exists, Content Director is notified via D-05 KPI strip. |

---

## 8. Integration Points

| Integration | Direction | What Flows | Mechanism |
|---|---|---|---|
| Institution portal | Portal → D-06 | Faculty uploads → S3 `notes-raw/` → Celery conversion → `content_notes` record created | S3 event trigger → Celery task → DB write |
| S3 (ap-south-1) | D-06 ↔ S3 | File download (presigned URL), published key management | Django view generates presigned URLs; file moves via `boto3.copy_object` + `boto3.delete_object` on publish |
| LibreOffice (ECS task) | D-06 → LibreOffice | PPTX/DOCX → PDF conversion | Celery task runs `libreoffice --headless --convert-to pdf` inside a dedicated ECS container |
| D-05 Director Dashboard | D-06 → D-05 | Notes in PENDING_DIRECTOR_REVIEW appear in D-05 Notes Review tab | `content_notes` state filter — same table |
| D-09 Taxonomy | D-06 reads | Subject/Topic/Subtopic dropdowns in structuring form | ORM with Memcached 10-min cache |
| D-17 Notes Analytics | D-06 publishes → D-17 shows | Published notes appear in analytics | Same `content_notes` table with `state = 'PUBLISHED'` filter |
| D-11 Published Bank | D-11 reads | Notes Library tab in D-11 shows published notes | Same `content_notes` table — D-11 reads with `state = 'PUBLISHED'` filter on Notes tab |
| CloudFront | D-06 → CloudFront | Invalidate notes list cache on publish/unpublish | `boto3.cloudfront.create_invalidation` for `/notes/{subject}/*` paths |

---

---

## 9. UI Patterns & Page-Specific Interactions

### Search
- **Incoming Queue tab:** Placeholder "Search by file name or institution…". Searches: file name, institution source label. Instant filter (queue typically < 200 items at once).
- **Published Library tab:** Placeholder "Search notes by title, topic, or tags…". Full-text search on: title, topic name, tags, chapter reference. Debounced 300ms.
- **In Progress tab:** Placeholder "Search in-progress notes…". Searches: title draft (if saved).

### Sortable Columns — Incoming Queue Table
| Column | Default Sort |
|---|---|
| Upload Date | **ASC (oldest first)** — default; process oldest notes first |
| File Size | DESC |
| Conversion Status | Custom: Failed → Processing → Ready |
| Subject | ASC |

### Sortable Columns — Published Library Table
| Column | Default Sort |
|---|---|
| Published Date | **DESC (newest first)** — default |
| View Count (30d) | DESC |
| Title | ASC |
| Subject | ASC |
| Version | DESC |

### Pagination
- Incoming Queue: 50 rows, numbered controls.
- Published Library: 50 rows, numbered controls.
- In Progress: 25 rows, numbered controls.

### Empty States
| Tab | Heading | Subtext |
|---|---|---|
| Incoming Queue | "No notes awaiting processing" | "Notes uploaded by faculty via institution portals will appear here for structuring." |
| Published Library | "No notes published yet" | "Process and publish notes from the Incoming Queue to build the library." |
| In Progress | "No notes in progress" | "Notes you've started structuring but not yet published will appear here." |
| Director Review | "No notes awaiting director review" | "Notes pending director approval will appear here (when director review is enabled for a subject)." |

### Toast Messages
| Action | Toast |
|---|---|
| Publish note (direct) | ✅ "Note published to library" (Success 4s) |
| Publish note (to director review) | ✅ "Submitted for director review" (Success 4s) |
| Return note to faculty | ✅ "Returned to faculty with your comment" (Success 4s) |
| Manual file replacement upload | ✅ "File replaced — ready to structure" (Success 4s) |
| Batch subject/topic tag applied | ✅ "Tags applied to {N} notes" (Success 4s) |
| Conversion complete (HTMX push) | ℹ "'{filename}' is ready to structure" (Info 6s — appears even if user is on another tab) |
| Conversion failed | ❌ "Conversion failed for '{filename}' — retry or replace file" (Error persistent) |
| Unpublish + edit | ✅ "Note unpublished — moved to Incoming Queue for editing" (Success 4s) |

### Loading States
- Incoming Queue: 8-row skeleton on initial load.
- Published Library: 8-row skeleton.
- Note Structuring Drawer open: left pane (PDF preview) shows skeleton shimmer for 2–5s while PDF.js renders. Right pane (metadata form) renders immediately.
- Conversion status badge: animated spinner while status = Processing. Polling `?part=conversion-status&note_id=X` every 5s.
- Conversion timeout (> 10 min): badge changes from spinner to "Timed Out — [Retry] or [Replace File]".

### Responsive Behaviour
| Breakpoint | Behaviour |
|---|---|
| Desktop | Incoming queue table full columns. Note Structuring Drawer 860px. |
| Tablet | Table: file name, status, subject, action — others hidden. Drawer: 80% viewport, PDF preview collapses to thumbnail mode (tap to expand full preview). |
| Mobile | Table: file name (truncated), status badge, action button. Drawer: full screen. PDF preview tab + Metadata form tab (two separate screens, not side-by-side). |

### Form Validation — Note Structuring Drawer
| Field | Validation |
|---|---|
| Title | Required, ≥ 3 chars. Error: "Title is required" |
| Subject | Required (dropdown). Error: "Select a subject" |
| Topic(s) | At least 1 required. Error: "Select at least one topic" |
| Difficulty Level | Required. Error: "Select a difficulty level" |
| Language | Required. Error: "Select the note language" |

"Publish" button disabled until all required fields valid. Unsaved metadata changes show amber "Unsaved changes" indicator.

### Role-Based UI
- Notes Editor (30): full access to all tabs and all actions.
- Content Director (18): read access to Published Library. Notes Review actions are in D-05, not D-06.
- "Director Review" status badge: shown only when Director Review Toggle is enabled for the note's subject.
- Version History icon: visible to Notes Editor for own notes. Director sees version history in D-12 for audit purposes.

---

*Page spec complete.*
*Amendments applied: G3 (Director Review Toggle — notes pending Director approval before publish; Director-side actions handled in D-05 Notes Review tab)*
*Gap amendments: Gap 4 (Notes audit trail viewer — Section 9, per-note lifecycle events, version timeline, CSV export) · Gap 18 (Multi-subject toggle rule clarification — Section 10, primary-subject toggle axis, multi-subject note prohibition, mid-session toggle change banner)*
*Next file: `d-07-bulk-import.md`*
