# E-05 — Production Job Tracker

> **Route:** `/content/video/production/jobs/`
> **Division:** E — Video & Learning
> **Primary Role:** Content Producer — Video (82)
> **Supporting Roles:** All production roles (83–89) — filtered view of own assigned jobs; Video Curator (31) — read; Content Director (18) — read
> **File:** `e-05-production-job-tracker.md`
> **Priority:** P0 — Core production management page; MCQ-to-video integration hub
> **Status:** ⬜ Not started

---

## 1. Page Name & Route

**Page Name:** Production Job Tracker
**Route:** `/content/video/production/jobs/`
**Part-load routes:**
- `/content/video/production/jobs/?part=job-table` — main table with filters
- `/content/video/production/jobs/?part=job-detail&id={job_id}` — detail drawer
- `/content/video/production/jobs/?part=stage-timeline&id={job_id}` — stage timeline within drawer
- `/content/video/production/jobs/?part=mcq-import` — import from MCQ bank modal content

---

## 2. Purpose

The Production Job Tracker is the master list of every video production job — from commission through animation, editing, QA, and publish. Every MCQ question in the Div D question bank can have one or more video production jobs linked to it; this page is where those jobs are created, tracked, and managed.

**Business goals:**
- Single source of truth for the status of every video being produced
- Enforce SLA discipline: overdue jobs surfaced with clear visual signals
- Enable bulk creation of video jobs from published MCQ questions (MCQ bank → production pipeline)
- Provide each production role (Scriptwriter, Animator, Editor, etc.) a filtered view of their own work
- Close the loop: when a job publishes to YouTube, it links back to the E-01 video library

---

## 3. Tabs

| Tab | Label | Default |
|---|---|---|
| 1 | All Jobs | ✅ Active (Producer/Director view) |
| 2 | My Jobs | ✅ Active (non-Producer roles; or secondary tab for Producer) |
| 3 | MCQ Import | — |

---

## 4. Section-Wise Detailed Breakdown

---

### Tab 1 — All Jobs (Content Producer / Content Director view)

#### Search & Filter Bar

- Search: job title, question ID (for MCQ-linked), YouTube video ID (for published). Debounced 300ms. "×" clear. **During debounce: "Searching…" spinner shown inside search field. On result: "{N} jobs found" shown below search bar. If 0: "No jobs match — try clearing some filters."**
- Advanced Filters (collapsible "Filters ▼"):

| Filter | Control | Options |
|---|---|---|
| Status | Multi-select | Brief Pending · Script Draft · Script Review · Script Approved · Voice Over · Animation · Graphics · Edit · Awaiting Subtitle · Subtitle · QA Review · Publish Queue · Published · On Hold · Cancelled |
| Subject | Multi-select | From D-09 taxonomy |
| Exam Type | Multi-select | — |
| Content Type | Multi-select | Concept Explainer · Problem Walkthrough · Revision Quick · Shorts |
| Priority | Multi-select | Low · Normal · High · Urgent |
| Language | Multi-select | EN · HI · TE · UR |
| Variant Type | Select | All · Primary only · Language variants only |
| Source | Multi-select | MCQ-Linked · Manual · Channel Request |
| Assigned Producer | Select | My jobs / All / Unassigned |
| SLA Status | Multi-select | On Time · Overdue · Critical (>2× SLA) |
| Date Range | Date range picker | Created at |

Active filter pills below search, each ×-dismissible. "Reset All" button.

#### Job Table (Sortable, Selectable, Responsive)

| Column | Sortable | Notes |
|---|---|---|
| Title | Yes | Truncated to 60 chars. Hover for full. Click → opens detail drawer. Parent jobs with language variants show a **▶ expand chevron** — click to reveal child variant rows indented beneath. |
| Language | No | Flag pill: 🇬🇧 EN · 🇮🇳 HI · TE · UR. Parent jobs also show a count badge: "+2 variants" if child language jobs exist. |
| Source | No | 🔗 MCQ icon (linked) · ✍️ Manual · 📺 Channel |
| Subject · Topic | No | "Subject / Topic" breadcrumb |
| Content Type | No | Pill badge |
| Status | No | Colour-coded pill: each status has a distinct colour |
| Priority | No | 🔴 Urgent · 🟠 High · 🔵 Normal · ⚪ Low |
| Stage SLA | No | Progress of current stage: "Day 2 of 5" · ⚠️ overdue in red |
| Overall SLA | Yes | Due date, colour: green (≥3d remaining) · amber (1–2d) · red (overdue) |
| Assigned To | No | Role label(s) of current stage assignee(s) |
| Actions | No | [View] [Edit] [Hold] [Cancel] |

**Row selection:** Checkbox column. Bulk actions appear in action bar above table.

**Bulk Actions:**
- **Bulk Assign (Current Stage)** — assign selected jobs' **currently active stage** to a specific role member. This is cross-job, single-stage reassignment. Distinct from per-job "Bulk Assign All Stages" in the Stage Timeline drawer.
  - **Bulk Assign Modal (560px):** Lists selected jobs in a scrollable table. For each job: job title (read-only) + new assignee dropdown (filtered to the correct role for the current active stage) + optional note field (max 200 chars). "Apply to All" toggle sets the same assignee + note for all jobs at once. "Confirm Assignments" button — creates/updates all stage assignments in batch. All new assignees notified. ✅ "{N} jobs reassigned" toast 4s.
- **Bulk Set Priority** — change priority for selected jobs (single priority dropdown applies to all)
- **Bulk Hold** — pause selected jobs (reason modal required — max 300 chars; applies to all selected)
- **Bulk Cancel** — cancel selected jobs (confirmation modal; reason required; shows count "You are about to cancel {N} jobs")

**Default sort:** Overall SLA ASC (soonest deadline first). Language variant child rows inherit their parent's sort position — they appear indented under their parent when the parent row is expanded and do not have an independent sort position.

**Variant filter behaviour:** When "Variant Type = Language variants only" is applied, child variant jobs are shown as flat rows (no parent grouping). Each row shows "Variant of: {parent title}" in smaller text below the job title. Clicking a child variant row opens the child job's drawer directly. If searching for a specific child variant job by title, the parent row is not auto-expanded in Tab 1 — the child appears as a flat result.

**Pagination:** 25 rows per page. "Showing X–Y of N". URL-bookmarkable `?page=N&sort=X&dir=asc&status=X`.

**Responsive:**
- Desktop: full column set
- Tablet: Title · Status · SLA · Actions
- Mobile: card layout — title + status pill + SLA badge + [View]

---

### Tab 2 — My Jobs (All Production Roles)

Identical table layout to Tab 1 but pre-filtered to:
- Jobs where `video_production_stage_assignment.assigned_to_id = request.user.id`
- AND stage status is not APPROVED/CANCELLED

**Extra column:** "My Stage" — shows specifically the stage the user owns (e.g. SCRIPT for Scriptwriter, ANIMATION for Animator).

**Sort default:** SLA due date ASC (soonest first).

**Non-Producer roles see only this tab by default.** Tab 1 "All Jobs" is hidden for roles 83–89.

---

### Tab 3 — MCQ Import

**Purpose:** Bulk-create production jobs from published MCQ questions in the D-11 Published Bank.

**Flow:**

#### Step 1 — Filter & Select Questions

- Search by question ID, subject, topic, exam type.
- Filter: Subject · Topic · Exam Type · Content type (MCQ) · "Has existing video job" toggle (shows questions that already have a job — to avoid duplicates).
- Table of matching published questions:

| Column | Notes |
|---|---|
| Short ID | Question short identifier |
| Question Preview | First 80 chars of question body |
| Subject · Topic | — |
| Exam Type | — |
| Video Job | "None" · "In Production" · "Published" (with link) |

- Checkbox select. "Select All on Page" checkbox.
- "Select {N} questions" counter.

#### Step 2 — Job Configuration

After selecting questions, "Configure Jobs →" button opens a form panel:

| Field | Type | Required | Notes |
|---|---|---|---|
| Content Type | Select | Yes | Applied to all selected jobs |
| Priority | Select | Yes | Default: Normal |
| Overall SLA (days from today) | Number | Yes | **Auto-populated** based on selected Content Type: reads `video_content_type.sla_override_days` first; falls back to `video_production_config.default_job_sla_days`. Helper text: "Based on {content_type} SLA: {N} days (E-12 config)." Editable. |
| Assign Scriptwriter | Searchable dropdown (Role 83) | No | Optional pre-assignment |
| Language | Select | Yes | Default: EN |
| Notes to Scriptwriter | Textarea | No | Seed note visible in E-06 |

#### Step 3 — Preview & Create

- Preview table: each question → proposed job title (auto-generated: "{Subject} — {Topic} — {Question short ID}")
- "Edit title" inline for any row before creation
- "Skipped" badge on rows where video job already exists (source=MCQ, same question_id)
- **"Allow duplicates" checkbox** (shown only when one or more rows carry a "Skipped" badge): checking this includes skipped rows in the creation batch, creating a new job even when an existing active video job exists for the same question. Use only when a replacement or secondary video is intentionally needed for the same question. Default: unchecked (skipped rows excluded).
- "Create {N} Jobs" button

**On creation:**
- Celery task `seed_production_brief_from_question` runs per job:
  - Populates `video_script.seed_text` with: question body + correct answer + explanation
  - Tags taxonomy from question's subject/topic/exam_type
- ✅ "Created {N} production jobs from MCQ bank" toast 4s
- Navigates to Tab 1 with "Source=MCQ-Linked" filter pre-applied

---

### Tab 3b — Production Gap Requests (sub-section, Producer 82 only)

**Purpose:** Review and act on video production gap requests submitted by the Video Curator (31) from E-01 Tab 5b (Production Gap Finder). The Curator flags topics with no mapped video and no active production job; the Producer decides whether to create a job.

**Access:** Content Producer (82) only. Tab 3 shows MCQ Import for Producers, and this sub-section appears below the import flow as a separate panel with its own amber badge count: "Requests ({N})" when there are pending items.

**Gap Requests Table:**

| Column | Sortable | Notes |
|---|---|---|
| Subject · Topic · Subtopic | No | Taxonomy node flagged by Curator |
| Exam Type | No | — |
| Suggested Content Type | No | Curator's recommendation |
| Suggested Priority | No | — |
| Notes from Curator | No | Truncated to 60 chars; click [View] to expand |
| Requested At | Yes | Relative time |
| Status | No | ⬜ Pending · ✅ Accepted · ❌ Declined |
| Actions | No | [Create Job] [Decline] |

**[Create Job]:**
- Opens Create Job modal pre-filled with: subject, topic, subtopic, exam type, content type, priority from the request
- Curator's notes pre-filled into the "Notes" field
- On create: `video_production_job_request.status` → ACCEPTED; `resulting_job_id` set to the new job's ID
- Curator notified: "Your production gap request for '{Subject} — {Topic}' has been accepted. Job created by Producer."
- ✅ "Job created — Curator notified" toast 4s

**[Decline]:**
- Decline modal: Reason text (required, max 200 chars)
- `video_production_job_request.status` → DECLINED
- Curator notified: "Your production gap request for '{Subject} — {Topic}' was declined. Reason: {reason}."
- ⚠️ "Request declined — Curator notified" toast 4s

**Pagination:** 25 rows per page. Default sort: Requested At DESC (oldest pending requests first so nothing is missed). Sort options: Status · Requested At · Subject. No automatic SLA or priority is attached to gap requests — Producer decides when to act based on current pipeline capacity.
**Empty state:** "No pending production gap requests from the Video Curator."

---

## 5. Job Detail Drawer (760px)

Opens on row click or [View]. Contains multiple tabs.

### Drawer Header

- Job title (editable inline for Producer)
- Status badge (large, colour-coded)
- Priority badge
- Language badge: "🇬🇧 EN" (or HI/TE/UR for variant jobs). Variant jobs also show "Variant of: {parent title}" in smaller text below the job title.
- Source badge: "MCQ-Linked: #{question_short_id}" (clickable → D-11 question drawer) or "Manual" or "Channel Request"
- "Edit Job" / "Put On Hold" / "Cancel Job" buttons (Producer only)
- **"+ Add Language Variant" button** (Producer only, visible on parent jobs only — not on child variant jobs):
  - Opens modal (640px):

| Field | Type | Required | Notes |
|---|---|---|---|
| Language | Select | Yes | EN · HI · TE · UR — only shows languages not already having a variant job |
| Scriptwriter | Searchable dropdown | No | Optional pre-assignment for translation/localisation |
| Overall SLA (days from today) | Number | Yes | Defaults to E-12 config |
| Notes | Textarea | No | E.g. "Translate to Hindi — keep technical terms in English" |

  - On create: new `video_production_job` record with `parent_job_id = this job's ID`, `language = selected`, pipeline starts at `BRIEF_PENDING`. Animation and Graphics stage assignments are NOT created (variant uses parent's accepted ANIMATION + GRAPHICS assets). Scriptwriter notified (if assigned). ✅ "Language variant created — {language} version added" toast 4s.

### Drawer Tab 1 — Overview

**Job Info:**
- Subject · Topic · Subtopic · Exam Type · Content Type · Language
- Overall SLA due date (with calendar indicator: N days remaining or N days overdue)
- Assigned Producer
- Created at · Created by (role label)

**MCQ Link Panel** (shown only if `question_id` is set):
- Question preview: first 100 chars of question body
- Correct answer label (A/B/C/D)
- Explanation preview (if present, first 100 chars)
- "View Full Question →" link → D-11 Published Bank, filtered to this question
- "Video will explain this question" contextual label

**YouTube Video** (shown only if job is PUBLISHED):
- YouTube thumbnail + title
- YouTube URL (external link)
- "View in Library →" link → E-01 detail drawer

**Language Variants Panel** (shown on parent jobs only — hidden on child variant jobs):

> Appears below YouTube Video section even before publish.

| Language | Status | YouTube Published | Actions |
|---|---|---|---|
| 🇬🇧 EN | (this job's status badge) | (youtube_video_id link or "—") | [View Job] |
| 🇮🇳 HI | In Production — SCRIPT_DRAFT | — | [View Job] |
| TE | Not started | — | [+ Add Variant] |
| UR | Not started | — | [+ Add Variant] |

- "[+ Add Variant]" opens the same language variant creation modal as the Drawer Header button, pre-filled with that language.
- "[View Job]" opens the child variant job's drawer (pushes a new drawer layer, breadcrumb: "Parent: {title} → HI Variant").

### Drawer Tab 2 — Stage Timeline

Visual horizontal stage pipeline. **ANIMATION, VOICE_OVER, and GRAPHICS run in parallel** after SCRIPT is approved. EDIT only unlocks when ALL three parallel stages are ACCEPTED. SUBTITLE runs in parallel with QA.

```
[BRIEF] → [SCRIPT] ──┬── [VOICE_OVER] ──┐
                     ├── [ANIMATION]  ──┼── [EDIT] → [SUBTITLE] ──┬── [QA] → [PUBLISH]
                     └── [GRAPHICS]   ──┘                         └── (parallel with QA)
```

**Stage sequencing rules (server-side enforced):**
- SCRIPT stage: sequential — BRIEF must complete first
- VOICE_OVER, ANIMATION, GRAPHICS: parallel — all three unlock simultaneously when SCRIPT is APPROVED
- EDIT: sequential — unlocks only when ALL of VOICE_OVER + ANIMATION + GRAPHICS are ACCEPTED
- SUBTITLE: parallel with QA — both unlock when EDIT is ACCEPTED
- PUBLISH_QUEUE: only when both QA (PASS) and SUBTITLE (all mandatory languages COMPLETE) are done

Each stage node shows:
- Stage name
- Status: ⬜ Pending · 🔵 In Progress · ✅ Approved · 🔄 Revision Requested · ❌ Skipped
- Assignee role label
- Stage SLA: "Due {date}" (green/amber/red based on remaining days)
- Started at / Completed at (if applicable)

Click a stage node → expands inline detail:
- Assignee name (role label only, DPDPA)
- Submission notes (if submitted)
- Review feedback (if revision requested)
- Assets attached (count)

**Stage Assignment Panel** (Producer only — shown below the pipeline diagram):

> This is how the Producer assigns roles to each pipeline stage. Assignment is required before a stage can start. Unassigned stages show as "⚠️ Unassigned" and block pipeline progression.

**"Assign / Reassign" per-stage button** (Producer only): shown inside each expanded stage node.

Opens **Stage Assignment Modal (480px)**:

| Field | Type | Required | Notes |
|---|---|---|---|
| Stage | Read-only label | — | Pre-filled from clicked stage |
| Assign To | Searchable dropdown | Yes | Lists only users with the correct role for this stage (SCRIPT → all Scriptwriters, ANIMATION → all Animators, etc.) |
| Stage SLA Due Date | Date picker | Yes | Pre-filled from E-12 config (today + stage SLA days). Editable. |
| Assignment Note | Textarea | No | Max 200 chars. Visible to assignee in their E-04 My Stage Panel and E-06/E-07 workspace. |

On assign:
- Creates/updates `video_production_stage_assignment` record
- Assignee receives Div E internal notification: "You have been assigned to the {stage} stage for '{title}' — due {date}."
- Stage node updates to show assignee role label
- ✅ "{Stage} assigned" toast 4s

**"Bulk Assign All Stages" button** (Producer only, shown at top of assignment panel):

Opens **Bulk Stage Assignment Modal (640px)** — one row per unassigned stage:

| Stage | Assignee (dropdown) | SLA Due Date | Note |
|---|---|---|---|
| SCRIPT | Searchable dropdown (Scriptwriters) | Date input | — |
| VOICE_OVER | Searchable dropdown (Scriptwriters / Producer) | Date input | Toggle: "In-house (Scriptwriter)" · "External (Producer uploads)" |
| ANIMATION | Searchable dropdown (Animators) | Date input | — |
| GRAPHICS | Searchable dropdown (Graphics Designers) | Date input | — |
| EDIT | Searchable dropdown (Video Editors) | Date input | — |
| SUBTITLE | Searchable dropdown (Subtitle Editors) | Date input | — |
| QA | Searchable dropdown (QA Reviewers) | Date input | — |

"Assign All" button — creates all stage assignments in a single batch. All assignees notified simultaneously via Celery. ✅ "All stages assigned — {N} team members notified" toast 4s.

**Validation:** If a stage's assignee is left blank in Bulk Assign, that stage is saved as PENDING/Unassigned. A ⚠️ badge persists on the Stage Timeline tab until all stages have assignees.

> **Job creation trigger:** When a new job is created (via Create Job modal or MCQ Import), the Pipeline tab immediately shows "⚠️ No stages assigned — assign team members to begin production." The "Bulk Assign All Stages" button is highlighted with an amber outline to draw attention.

### Drawer Tab 3 — Assets

List of all uploaded production assets for this job:

| Column | Notes |
|---|---|
| Stage | VOICE_OVER · ANIMATION · GRAPHICS · FINAL_EDIT |
| File Name | GRAPHICS assets with `is_thumbnail=True` show a ⭐ "YouTube Thumbnail" badge next to the file name |
| Version | v1, v2, … |
| Size | MB |
| Status | Uploaded · Accepted · Rejected |
| Uploaded By | Role label |
| Uploaded At | — |
| Actions | [Download] (presigned S3 URL, 15-min expiry) · [View] (for video/image) |

**Language variant jobs:** ANIMATION and GRAPHICS assets are **inherited from the parent job** and displayed as read-only references labelled "Shared from parent job". Only VOICE_OVER, FINAL_EDIT, and SUBTITLE assets are separate per variant job and appear as editable rows. Parent assets cannot be uploaded or replaced from a child variant's drawer — those actions must be performed from the parent job.

"Upload Asset" button → opens E-07 upload modal (if user has upload rights for this job's current stage).

### Drawer Tab 4 — Script

Inline read-only view of the current script:
- Seed text (from MCQ auto-population, shown in yellow-tinted box if present)
- Script body (latest version)
- Script status badge
- Latest review feedback (if revision requested)
- "Open in Script Workspace →" link → E-06 (full workspace)

**Producer Actions (Content Producer 82 only — shown below script status):**

| Button | Condition | Behaviour |
|---|---|---|
| "Force unlock edit" | `video_script.locked_by_id` is set (script is locked by an active or abandoned edit session) | Immediately clears the lock (`locked_by_id = null`, `locked_at = null`). The displaced user receives a Div E notification: "Your script edit session for '{title}' was ended by the Producer." Use when a Scriptwriter has closed their browser without releasing the lock and the 30-minute auto-expiry has not yet elapsed. |
| "Override: Approve Script" | `video_script.revision_count >= max_script_revisions` (from E-12 config) | Opens Override Approval Modal — see E-06 Section 8b for full spec. |
| "Reassign Scriptwriter" | Available at Producer's discretion (any script status) | Opens Reassign Modal — see E-06 Section 8b for full spec. |

### Drawer Tab 5 — Activity Log

All events for this job, newest first:
- Timestamp · Event · Actor (role label)
- Examples: "Job created · Scriptwriter assigned · Script submitted · Revision requested · Script approved · Animation started · …"

25 per page inside drawer.

### Drawer Tab 6 — Comments

**Purpose:** Internal team communication thread for this job. Allows Scriptwriter, Animator, Editor, QA Reviewer, and Producer to discuss the job without leaving the tracker.

**Layout:** Chronological message thread, newest at bottom.

**Comment card:**
```
[Role label]           [Relative time]
[Comment text — plain text, max 500 chars]
                        [Reply] [Resolve ✓] (Producer only)
```

**Compose box (bottom of thread):**
- Textarea: max 500 chars. Counter: "450 / 500"
- "Post Comment" button
- "@ mention" support: typing `@` shows a dropdown of **all roles assigned to this job's stage assignments** (not all users in the system). Tagged roles receive a Div E notification: "You were mentioned in a job comment for '{title}'". The notification goes to all users holding that role who are assigned to this specific job — not all role holders platform-wide. If a role is not assigned to this job, it does not appear in the @ dropdown.

**Resolve thread:** Producer (82) can mark the entire thread as "Resolved ✓" — collapses thread with "Resolved by Producer on {date}". Thread still readable but greyed out. Producer can "Reopen" if needed.

**Access:** All production roles assigned to this job can read and post. Read-only for Content Director (18). Comments are internal — never shown to Div D roles or students.

**Empty state:** "No comments yet. Post a question or note for the production team."

**Notification trigger:** Any new comment in a job's thread sends a Div E internal notification to all roles assigned to that job's stage assignments.

---

## 6. Create Production Job — Modal (640px)

Triggered by "+ New Job" button (Producer only).

**Form:**

| Field | Type | Required | Validation |
|---|---|---|---|
| Title | Text input | Yes | Max 200 chars |
| Source | Radio | Yes | Manual · Channel Request |
| Content Type | Select | Yes | — |
| Subject | Searchable dropdown | Yes | From D-09 taxonomy |
| Topic | Cascading dropdown | Yes | — |
| Subtopic | Cascading dropdown | No | — |
| Exam Type(s) | Multi-select | Yes | At least 1 |
| Language | Select | Yes | Default: EN |
| Priority | Select | Yes | Default: Normal |
| Overall SLA (days) | Number | Yes | Min 1. Default from E-12 config. |
| Assign Scriptwriter | Searchable dropdown | No | Role 83 members |
| Notes | Textarea | No | Max 500 chars |

**Validation rules:**
- Title required
- Subject + Topic + Exam Type required
- SLA days must be positive integer
- Content Type required

"Create Job" → creates `video_production_job` record in BRIEF_PENDING state + creates stage assignment records for each configured stage (PENDING status). ✅ "Production job created" toast 4s.

---

## 7. Edit Job — Modal (same 640px layout as Create)

Editable fields: Title · Priority · Overall SLA due date · Subject/Topic/Exam Type · Content Type · Notes.
Status, Source, and question_id are not editable after creation.
"Save Changes" → ✅ "Job updated" toast 4s.

---

## 8. Hold / Cancel — Modals

**Hold Modal:**
- Reason (required textarea, max 300 chars)
- Sets status to `ON_HOLD`. All active stage assignments set to PAUSED (new status on `video_production_stage_assignment.status`).
- All assignees notified: "'{title}' has been put on hold. Your {stage} stage is paused. Reason: {reason}."
- Holds do NOT delete stage assignments or assets.
- **Language variant cascade:** If the job has child language variant jobs (HI/TE/UR), the Hold modal shows: ⚠️ "This job has {N} language variant(s). Hold parent only, or hold all variants too?" → Radio: "Hold parent only" · "Hold parent + all variants". Default: "Hold parent only" (variants continue independently unless Producer selects cascade). If "all variants": each active child job is also set to ON_HOLD, assignees notified.

**Resume Job — full recovery flow:**

"Resume Job" button appears in the job detail drawer header whenever `status = ON_HOLD`. Visible and clickable for Producer (82) only.

**Resume Modal (480px):**

| Field | Type | Required | Notes |
|---|---|---|---|
| Resume from stage | Select | Yes | Pre-filled to the stage that was active when hold was applied. Options: all stages from SCRIPT through QA. Producer can resume from an earlier stage if needed (e.g., QA FAIL → hold → resume from EDIT to re-upload). |
| Resume note | Textarea | No | Max 300 chars. Shown to all assignees. |

**On confirm:**
- `video_production_job.status` → restored to the appropriate active status for the selected resume stage (e.g., resume from EDIT → `EDIT_IN_PROGRESS`; resume from SCRIPT → `SCRIPT_DRAFT`)
- Stage assignment for the resume stage: status → `IN_PROGRESS` (re-activates)
- All subsequent stages: status → `PENDING` (reset, not PAUSED)
- All assignees for resume stage and later notified: "'{title}' has resumed. {stage} stage is now active."
- ✅ "Job resumed from {stage} stage" toast 4s
- `video_production_config_log` entry created: "Job resumed from {stage} — reason: {note}" (audit trail)

**Edge:** If the job was on hold due to QA FAIL (E-08), and Producer resumes from EDIT stage, the Video Editor (87) is notified to re-upload a corrected FINAL_EDIT asset. The QA workspace will show "Revision v{N} — previous QA feedback: {text}" when the job re-enters QA.

**Language variant cascade on resume:** Resume is job-specific. If a parent job is resumed, child variant jobs (HI/TE/UR) are NOT automatically resumed — each variant must be resumed independently from its own job detail drawer. This allows the Producer to resume only the variants that are ready, rather than all at once.

**Cancel Modal:**
- Warning: "Cancelling a job cannot be undone. Any uploaded assets will be retained for 30 days, then permanently deleted from S3."
- Reason (required, max 300 chars)
- Sets status to `CANCELLED`. Stage assignments set to CANCELLED.
- All currently active assignees notified: "'{title}' has been cancelled. Reason: {reason}."
- If job has language variant children: ⚠️ confirmation: "This job has {N} language variant(s) (HI/TE/UR). Cancel parent only, or cancel all variants too?" → Radio: "Cancel parent only" · "Cancel parent + all variants". If "all variants": each child job is cancelled and its assignees notified.
- Celery schedules S3 asset deletion after 30 days (`purge_cancelled_job_assets` task).

---

## 9. Access Control

| Gate | Rule |
|---|---|
| Page access | All Div E production roles (82–89), Content Director (18), Video Curator (31) |
| Tab 1 (All Jobs) | Content Producer (82), Content Director (18) only |
| Tab 2 (My Jobs) | All roles — filtered to own assignments |
| Tab 3 (MCQ Import) | Content Producer (82) only |
| Create / Edit / Hold / Cancel Job | Content Producer (82) only |
| Bulk actions | Content Producer (82) only |
| Reassign Stage | Content Producer (82) only |
| Download Assets | All production roles for their own stage's assets; Producer sees all |
| MCQ link "View Full Question →" | All roles can view D-11 (read-only from there) |

---

## 10. Edge Cases & Error States

| Scenario | Behaviour |
|---|---|
| MCQ Import: question already has an active video job | Row shows "In Production" badge. Skipped automatically in bulk create. User can still force-create (checkbox "Allow duplicates"). |
| Job SLA passes with status still in production | Celery Beat task `check_video_production_sla` runs hourly. Marks `is_overdue=True`. Producer notified. Dashboard SLA tile turns red. |
| Stage assignee is unavailable (no such role member) | Stage shown as "Unassigned". Producer receives warning: "Scriptwriter stage unassigned for {N} jobs." |
| Cancel a job in QA_REVIEW | Confirm modal adds: "This job is in QA — the QA Reviewer will lose their work-in-progress. Confirm?" |
| Bulk cancel > 20 jobs | Confirm modal shows: "You are about to cancel {N} jobs. This cannot be undone." Requires typing "CANCEL {N}" to confirm. |
| MCQ question deleted after job creation | question_id FK retained. "View Full Question" link shows "Question no longer available (archived)." Job continues unaffected. |
| MCQ question answer corrected (D-04 Amendment Review) after script already seeded | Celery signal `post_save` on `content_question` detects change in correct_answer or explanation. If a linked `video_production_job` is in SCRIPT_DRAFT or SCRIPT_REVIEW: a yellow banner appears in E-06 script editor: "⚠️ The linked MCQ answer/explanation was updated. Review seed content before submitting." `video_script.seed_text` is also auto-updated. Scriptwriter must re-review their script against the new correct answer. |
| Script Reviewer unavailable (> 24h with scripts in SUBMITTED) | Celery Beat task `check_script_review_sla` runs every hour. If any script in SUBMITTED state has been waiting > review SLA (default from E-12): Producer receives notification: "{N} scripts awaiting review for > {SLA}h. Consider reassigning Script Reviewer." Producer can reassign from E-05 Drawer Tab 2 → Stage Timeline → "Reassign Stage". |
| Revision loop (script returned > max revisions from E-12 config) | System adds an auto-comment in Drawer Tab 6: "⚠️ Script has been revised {N} times — exceeds the {max} revision limit. Producer intervention required." Status stays REVISION_REQUESTED. Producer must decide: reassign Scriptwriter, escalate to Director, or override and approve. |

---

## 11. UI Patterns

### Empty States

| Context | Heading | Subtext | CTA |
|---|---|---|---|
| No jobs at all | "No production jobs yet" | "Create your first video job or import from the MCQ bank." | "Create Job" / "Import from MCQ Bank" |
| Filter returns zero | "No jobs match these filters" | "Try clearing the status or subject filter." | "Reset Filters" |
| My Jobs empty | "No jobs assigned to you" | "Your stage assignments will appear here once the Producer assigns work." | — |
| MCQ Import — no questions match | "No published questions match" | "Adjust the subject or exam type filter." | "Reset Filters" |

### Toast Messages

| Action | Toast |
|---|---|
| Job created | ✅ "Production job created" (4s) |
| Job updated | ✅ "Job updated" (4s) |
| Job put on hold | ⚠️ "Job paused — all stage assignments suspended" (8s) |
| Job resumed | ✅ "Job resumed" (4s) |
| Job cancelled | ✅ "Job cancelled" (4s) |
| MCQ bulk import created | ✅ "Created {N} production jobs from MCQ bank" (4s) |
| Stage reassigned | ✅ "Stage reassigned" (4s) |

### Loading States

- Job table: 8-row shimmer (icon + title + 4 pill placeholders per row)
- Drawer: header shimmer + 3 tab shimmers + timeline skeleton
- Stage timeline: horizontal pipeline of 8 circle nodes with connecting lines, all shimmered

### Responsive Behaviour

| Breakpoint | Behaviour |
|---|---|
| Desktop (≥1280px) | Full table + 760px drawer |
| Tablet (768–1279px) | Table: Title · Status · SLA · Actions. Drawer: full width 100% |
| Mobile (<768px) | Card list: title + status + SLA badge + [View]. Drawer: full-screen bottom sheet |

---

*Page spec complete.*
*E-05 covers: all jobs → my jobs → MCQ bulk import → create → edit → parallel stage timeline (VOICE_OVER/ANIMATION/GRAPHICS in parallel) → assets → script preview → activity log → job comments thread.*
