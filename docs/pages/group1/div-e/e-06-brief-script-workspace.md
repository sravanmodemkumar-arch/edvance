# E-06 — Brief & Script Workspace

> **Route:** `/content/video/production/scripts/`
> **Division:** E — Video & Learning
> **Primary Roles:** Video Scriptwriter (83) — author scripts; Script Reviewer (84) — review and approve
> **Supporting Roles:** Content Producer (82) — read all, commission briefs; Content Director (18) — read-only
> **File:** `e-06-brief-script-workspace.md`
> **Priority:** P0 — No animation can start without an approved script
> **Status:** ⬜ Not started

---

## 1. Page Name & Route

**Page Name:** Brief & Script Workspace
**Route:** `/content/video/production/scripts/`
**Part-load routes:**
- `/content/video/production/scripts/?part=script-table` — script list with filters
- `/content/video/production/scripts/{job_id}/` — full-page script editor (dedicated route)
- `/content/video/production/scripts/?part=review-queue` — Script Reviewer's queue
- `/content/video/production/scripts/?part=script-detail&id={job_id}` — read-only script drawer

---

## 2. Purpose

The Brief & Script Workspace is where every video's content is authored and approved before animation begins. The Scriptwriter (83) receives a brief (auto-seeded from the MCQ question if linked), writes the script, and submits it. The Script Reviewer (84) reviews for factual accuracy and approves or returns.

**Business goals:**
- Ensure every video script is factually accurate before it enters expensive animation/editing
- Auto-seed scripts from MCQ question body + answer + explanation (reducing Scriptwriter effort)
- Maintain version history so reviewers can track changes between drafts
- Clear handoff signal: script APPROVED status unlocks the ANIMATION stage in E-05

---

## 3. Script List View (default landing)

#### Search & Filter Bar

- Search: job title, question ID. Debounced 300ms. "×" clear.
- Advanced Filters (collapsible "Filters ▼"):

| Filter | Control | Default |
|---|---|---|
| Status | Multi-select | DRAFT · SUBMITTED · REVISION_REQUESTED · APPROVED |
| Subject | Multi-select | — |
| Exam Type | Multi-select | — |
| Source | Multi-select | MCQ-Linked · Manual |
| Assigned To | Select | My Scripts (Scriptwriter) / Assigned to Me (Reviewer) / All (Producer) |
| SLA Status | Multi-select | On Time · Overdue |

Active pills + "Reset All".

#### Script Table (Sortable, Selectable, Responsive)

| Column | Sortable | Notes |
|---|---|---|
| Job Title | Yes | Click → opens script drawer (read-only) or editor (Scriptwriter) |
| Source | No | 🔗 MCQ (linked) · ✍️ Manual |
| Subject · Topic | No | — |
| Script Status | No | Colour-coded pill: Draft (grey) · Submitted (blue) · Revision Requested (amber) · Approved (green) |
| Version | No | "v{N}" |
| Stage SLA | No | "Day {N} of {total}" — red if overdue |
| Assigned Writer | No | Role label |
| Last Updated | Yes | Relative timestamp |
| Actions | No | [Open] [View Brief] |

**Row select:** Checkbox. Bulk action: Bulk Reassign Scriptwriter (Producer only).

**Pagination:** 25 rows per page. URL-bookmarkable.

**Responsive:**
- Desktop: full columns
- Tablet: Job Title · Status · SLA · Actions
- Mobile: card — title + status + SLA badge + [Open]

---

## 4. Script Brief Drawer (640px)

Opens on [View Brief] or from E-05 drawer Tab 4.

**Content:**

**Brief Panel:**
- Job title
- Content type · Subject · Topic · Subtopic · Exam Type · Language
- Overall SLA due date
- Script stage SLA due date (from stage assignment)
- Notes from Producer (if any)

**MCQ Seed Panel** (shown if source = MCQ):
> Yellow-tinted information box labelled "Script Seeded from MCQ #{short_id}"
- Question body (full text)
- Correct answer (e.g. "B. 2.4 m/s²")
- Explanation text (if present in content_question)
- "View question in D-11 →" link (opens D-11 in a new tab)

*Purpose of seed:* Scriptwriter does not need to research from scratch — the correct answer and explanation are the source of truth for the video's content.

> **Language variant jobs:** For HI/TE/UR variant jobs, the MCQ seed content is always in English (sourced from the parent EN job's question record). The Scriptwriter must translate the script to match the target language while preserving pedagogical accuracy. A note at the top of the seed panel reads: "⚠️ This is a {language} variant job. Seed content is in English — translate accurately to {language} while keeping technical terms, formulas, and values exact." The Scriptwriter may reference the parent EN job's approved script via the "View Parent Script →" link (read-only, opens in a separate panel).

**Current Script Status:** Status badge + latest review feedback (if revision requested).

**"Open Script Editor →" button** (Scriptwriter 83 for own jobs; Producer 82 for any).

---

## 5. Full-Page Script Editor

**Route:** `/content/video/production/scripts/{job_id}/`

This is a **full-page view** (not a drawer) to give maximum writing space.

### Layout

**Left panel (280px) — Brief Sidebar**

- Job title (read-only)
- Content type, subject, topic, exam type
- SLA countdown: "Script due in {N} days" (amber <2 days, red if overdue)
- **MCQ Seed section** (if MCQ-linked):
  - "Seed Content" accordion (expanded by default):
    - Question body
    - Correct answer
    - Explanation
    - Yellow banner: "Script seeded from MCQ #{id} — verify content before authoring"
- **Review Feedback section** (shown if status = REVISION_REQUESTED):
  - Reviewer feedback text (amber-tinted box)
  - Version of script that was reviewed: "Feedback on v{N}"
- **"View Parent Script →" link** (shown only for language variant jobs where `parent_job_id` is set):
  - Positioned below the Review Feedback section (or below Seed Content if no feedback is present)
  - Visible only if the parent job's script `status = APPROVED`. If not yet approved: "Parent script not yet approved — available once EN script is approved."
  - Clicking opens a **400px read-only panel** that slides in from the right of the editor, narrowing the script editor area to accommodate it. Panel title: "Parent Script (EN) — read-only" with a ✕ close button.
  - Panel content: parent script body rendered as non-editable rich text (same formatting as the editor)
  - Purpose: translation reference — the Scriptwriter should use this to verify pedagogical accuracy and structure in the target language, not to copy text verbatim.

**Right panel (full remaining width) — Script Editor**

- Rich text editor (content-editable `div` styled as a script document)
- Supports: Bold · Italic · Heading levels (H1–H3) · Bullet list · Numbered list · Horizontal rule (scene break)
- **No external libraries** — custom HTMX-driven editor (Django form `Textarea` with client-side formatting toolbar)
- Word count indicator (bottom-left of editor)
- Version indicator: "Editing v{current_version}"

### Auto-save

- HTMX POST every 30s to `/content/video/production/scripts/{job_id}/?part=autosave`
- Saves current content as a draft (does NOT increment version — version increments only on Submit)
- "Last saved: {N} sec ago" indicator (top-right of editor area)

**Concurrent edit prevention:** Only one user can edit a script at a time. When a user opens the script editor, a server-side edit lock is set (stored as `video_script.locked_by_id` + `locked_at`; lock expires after 30 minutes of inactivity). If a second user attempts to open the same script in edit mode while the lock is active, they are shown a modal: "This script is currently being edited by {role label} (since {N} min ago). [Open Read-Only] [Cancel]". The active editor's auto-save refreshes the lock every 30s. Lock is released on "Save & Exit" or browser close (via unload event). Producer (82) can break the lock via E-05 Drawer Tab 4 → "Force unlock edit" button — the original editor receives a notification: "Your script edit session for '{title}' was ended by the Producer."

### Script Version History

- "Version History ▼" toggle (collapsed by default) in top bar
- Dropdown list: v1 · v2 · … (newest first)
- Click a version → opens read-only modal showing that version's content
- "Restore this version" button in modal → creates a new draft with that content (does not delete current)

### Editor Validation (before submit)

| Rule | Error |
|---|---|
| Script body empty | "Script cannot be empty." inline under editor |
| Script < 100 words | Warning (not block): "This script is very short ({N} words). Ensure it covers the full concept." |
| Script > 5,000 words | Warning: "Long scripts may exceed animation capacity. Consider splitting." |

### Submit for Review

**"Submit for Review" button** (Scriptwriter 83 only):
- Validation runs (see above)
- Confirm modal: "Submit script v{N} for review? The Script Reviewer will be notified."
- On confirm:
  - `video_script.status` → SUBMITTED
  - `video_script.version` incremented
  - Celery task: creates Div E internal notification for Script Reviewer (84)
  - E-05 stage assignment status → SUBMITTED
  - ✅ "Script submitted for review" toast 4s
  - Redirects back to Script List

### "Save & Exit" button

Saves current auto-save draft. Returns to Script List. No version increment.

---

## 6. Script Review — Reviewer Queue (Script Reviewer 84)

**Route:** `/content/video/production/scripts/?view=review-queue`
(or Tab switch on Script List: "Review Queue" tab visible to Script Reviewer only)

#### Review Queue Table (Sortable, Selectable, Responsive)

| Column | Sortable | Notes |
|---|---|---|
| Job Title | Yes | Click → opens Review Workspace |
| Subject · Topic | No | — |
| Script Version | No | "v{N}" |
| Submitted At | Yes | — |
| SLA (script stage) | No | "Day {N} of {total}" — red if overdue |
| Actions | No | [Review] |

**Pagination:** 25 rows.
**Filter:** Subject · Exam Type · SLA Status. No bulk actions (each review is individual).

**Empty state:** "Review queue is clear ✓" | "All submitted scripts have been reviewed."

#### Script Review Workspace

**Route:** `/content/video/production/scripts/{job_id}/review/`

Same two-panel layout as editor, but:

**Left panel:** Brief + MCQ seed (same as editor left panel). Plus: "Previously reviewed: v{N} on {date}" if this job was returned before.

**Right panel:**
- Script content rendered as read-only rich text
- Version selector: "Reviewing v{N}" (can view previous versions for comparison)
- **Inline comment mode:** Reviewer can highlight a text range and add a comment (similar to Google Docs commenting). Comment appears as a side annotation. Stored as `video_script_review_comment` (text_range_start, text_range_end, comment_body).
- **Comment resolve (Scriptwriter):** When the Scriptwriter opens the editor after a revision request, inline comments from the Reviewer are shown as side annotations with a ✓ "Mark Resolved" button per comment. Clicking it sets `resolved = True`, comment turns green with strikethrough. Resolved comments remain visible (not deleted) — they are greyed out with a checkmark as an audit trail. Resolving comments is optional tracking only and does NOT block or enable script submission. On re-submission, all comments (resolved and unresolved) are retained and visible to the Script Reviewer on the new version for comparison. Comment annotations are NOT cleared between revisions.
- **Revision count badge:** Header of the editor shows "Revision #{N}" in amber. If N exceeds max_revisions (from E-12): badge turns red with label "Max revisions reached — Producer must intervene."

**Review Decision Panel (bottom):**

| Field | Type | Required |
|---|---|---|
| Decision | Radio | Yes: Approve / Request Revision |
| Overall Feedback | Textarea | Required if Revision |
| Factual Accuracy | Checkbox list | Pre-filled issues: "Incorrect answer", "Wrong formula/value", "Missing concept", "Misleading explanation", "Other" |

**"Submit Review" button:**
- If Approve:
  - `video_script.status` → APPROVED
  - `video_script.approved_at` set
  - E-05 stage assignment → APPROVED
  - **ANIMATION, VOICE_OVER, and GRAPHICS stages all unlock simultaneously** — all three stage assignments status → PENDING; all three assignees notified in parallel
  - ✅ "Script approved — Animation, Voice Over, and Graphics stages unlocked" toast 4s
- If Revision Requested:
  - `video_script.status` → REVISION_REQUESTED
  - E-05 stage assignment → REVISION_REQUESTED
  - Scriptwriter (83) notified via Div E internal notification
  - ⚠️ "Revision requested — Scriptwriter notified" warning toast 8s

---

## 7. Data Models

*(Defined in div-e-pages-list.md — `video_script`, `video_script_review`)*

### `video_script_review_comment`
| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `script_id` | FK → video_script | — |
| `reviewer_id` | FK → auth.User | Script Reviewer (84) |
| `text_range_start` | int | Character offset in script body |
| `text_range_end` | int | — |
| `comment_body` | text | — |
| `created_at` | timestamptz | — |
| `resolved` | boolean | Default False — Scriptwriter can mark resolved |

### `video_script_version`
| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `script_id` | FK → video_script | — |
| `version_number` | int | — |
| `body` | text | Full script content at this version |
| `saved_by_id` | FK → auth.User | — |
| `saved_at` | timestamptz | — |

---

## 8. Access Control

| Gate | Rule |
|---|---|
| Page access | Scriptwriter (83), Script Reviewer (84), Content Producer (82), Content Director (18) |
| Script Editor (write) | Scriptwriter (83) for own assigned scripts; Producer (82) for any script |
| Submit for Review | Scriptwriter (83) only (for own assigned scripts) |
| Review Queue + Review Workspace | Script Reviewer (84) only |
| Read-only (Brief Drawer, Script List) | Content Director (18), Video Curator (31) |
| Version History view | All roles with page access |
| Inline comments | Script Reviewer (84) only |
| "View question in D-11 →" link | All roles |

---

## 8b. Producer Override Actions (Content Producer 82 only)

These actions are available when `video_script.revision_count >= max_script_revisions` from E-12 config, OR when the Producer decides to intervene at any point.

**Where visible:**
- E-06 Script List table → Actions column: [Override Approve] [Reassign Writer] (Producer only, replace [Open] when revision limit hit)
- E-05 Job Drawer → Tab 4 (Script) → action buttons below script status

---

### Override: Approve Script

**"Override: Approve Script" button** → **Override Approval Modal (480px):**

| Field | Type | Required | Notes |
|---|---|---|---|
| Justification | Textarea | Yes | Min 20 chars, max 500. Reason for bypassing Script Reviewer. |
| Confirm | Checkbox | Yes | "I have reviewed the script and confirm it is factually accurate." |

**On confirm:**
- `video_script.status` → APPROVED
- `video_script.override_approved_by_id` → Producer's user ID (new field — see data model)
- `video_script.override_justification` → justification text
- E-05 stage assignment → APPROVED
- ANIMATION, VOICE_OVER, GRAPHICS stages unlock (same as normal approval)
- Script Reviewer (84) notified: "Script for '{title}' was approved directly by Producer. Review bypassed."
- ✅ "Script approved by Producer override — Animation stage unlocked" toast 4s

---

### Reassign Scriptwriter

**"Reassign Writer" button** → **Reassign Modal (480px):**

| Field | Type | Required | Notes |
|---|---|---|---|
| New Scriptwriter | Searchable dropdown (Role 83) | Yes | — |
| Reset revision count | Toggle | Yes | Default ON — resets `video_script.revision_count` to 0 so new Scriptwriter starts fresh |
| Note to new writer | Textarea | No | Visible to the new Scriptwriter in E-06 brief sidebar |

**On confirm:**
- E-05 SCRIPT stage assignment reassigned to new Scriptwriter
- If reset count: `video_script.revision_count` → 0
- Script status → DRAFT (unlocks editor for new Scriptwriter)
- Old Scriptwriter notified: "'{title}' has been reassigned to a new Scriptwriter."
- New Scriptwriter notified: "You have been assigned the script for '{title}'. Previous drafts are available in Version History."
- ✅ "Script reassigned — new Scriptwriter notified" toast 4s

---

## 9. Edge Cases & Error States

| Scenario | Behaviour |
|---|---|
| Script submitted but Script Reviewer is unassigned | E-05 shows "Reviewer unassigned" on script stage. Producer must assign before reviewer can access. Script stays in SUBMITTED. |
| Script Reviewer unavailable — scripts pile up in SUBMITTED | Celery Beat `check_script_review_sla` runs every hour. If scripts are in SUBMITTED for longer than the script review SLA (default from E-12): Producer notified: "{N} scripts awaiting review — Script Reviewer (84) SLA exceeded. Reassign via E-05." E-06 Review Queue shows a ⚠️ amber banner: "Review SLA exceeded for {N} scripts — Producer has been notified." |
| Scriptwriter edits script after submission (before review) | Not allowed — editor becomes read-only once script is SUBMITTED. Banner: "Script is under review. Editing is locked." If Producer unlocks (cancel review action), status reverts to DRAFT. |
| Script Reviewer approves a script with no animation assignee | ANIMATION stage unlocked but marked "Unassigned". Producer receives alert: "Animation stage unassigned for {N} jobs." |
| MCQ seed text exceeds 3,000 words | Seed panel shows a truncated preview with "Show full seed ▼" toggle. Full content available in accordion. |
| Max revisions reached (from E-12 config) | Script editor header shows red "Max revisions reached" badge. Scriptwriter cannot submit again — the submit button is disabled with tooltip: "Max revisions reached. Contact the Producer to resolve." Producer sees two actions: **[Override: Approve Script]** and **[Reassign Scriptwriter]** — both appear in E-05 Job Drawer Tab 4 (Script) and in E-06 Script List Actions column for Producer. See Producer Override section below. |
| Scriptwriter needs factual clarification from the original SME | No direct mechanism (SMEs are Div D, not Div E). Scriptwriter should use E-05 Job Drawer Tab 6 (Comments) to post the question. Producer bridges to Div D if needed. The seed text from the MCQ is the primary source of truth — Scriptwriter should not deviate from the correct answer in the seed. |
| Script autosave fails (network error) | "Last save failed — check connection" indicator turns red. Manual "Save Draft" button appears prominently. |
| Revision requested after 2nd or more review | System tracks revision count: "Revision #{N} — consider escalating if recurring." Appears as info note for Producer on E-05 drawer. |

---

## 10. UI Patterns

### Toast Messages

| Action | Toast |
|---|---|
| Script auto-saved | — (silent; indicator updates) |
| Script saved manually | ✅ "Draft saved" (4s) |
| Script submitted | ✅ "Script submitted for review" (4s) |
| Revision requested | ⚠️ "Revision requested — Scriptwriter notified" (8s) |
| Script approved | ✅ "Script approved — Animation, Voice Over, and Graphics stages unlocked" (4s) |
| Version restored | ✅ "Version {N} restored as new draft" (4s) |

### Loading States

- Script list table: 8-row shimmer
- Brief drawer: 3 shimmer blocks (brief + seed + status)
- Script editor: editor area skeleton (grey rectangle matching editor height)
- Review workspace: left panel shimmer + editor area shimmer

### Empty States

| Context | Heading | Subtext |
|---|---|---|
| No scripts assigned (Scriptwriter) | "No scripts assigned" | "The Producer will assign script work when production jobs are ready." |
| Review queue empty | "Review queue is clear ✓" | "All submitted scripts have been reviewed." |
| Filter returns zero | "No scripts match" | "Try a different subject or status filter." |

### Responsive Behaviour

| Breakpoint | Behaviour |
|---|---|
| Desktop (≥1280px) | Two-panel editor (280px brief + full-width editor) |
| Tablet (768–1279px) | Brief panel collapses to accordion at top; editor full width below |
| Mobile (<768px) | Brief accordion + single-column editor. Submit button sticky at bottom. |

---

*Page spec complete.*
*E-06 covers: script list → brief drawer (with MCQ seed) → full-page editor → auto-save → version history → submit → review queue → inline review → approve/revise.*
