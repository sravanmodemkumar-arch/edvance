# E-01 — Video Library & Mapping

> **Route:** `/content/video/library/`
> **Division:** E — Video & Learning
> **Primary Role:** Video Curator (31)
> **Supporting Roles:** YouTube Channel Manager (33) — read + map channel uploads; Playlist Manager (32) — read-only; Content Director (18) — read-only
> **File:** `e-01-video-library.md`
> **Priority:** P0 — Foundation for all video content delivery across 7.6M students
> **Status:** ⬜ Not started

---

## 1. Page Name & Route

**Page Name:** Video Library & Mapping
**Route:** `/content/video/library/`
**Part-load routes:**
- `/content/video/library/?part=kpi-strip` — 4 KPI tiles (polled every 120s)
- `/content/video/library/?part=video-table` — main table with filters
- `/content/video/library/?part=video-detail&id={video_id}` — detail drawer content
- `/content/video/library/?part=health-check-status&id={video_id}` — live health check result
- `/content/video/library/?part=requests-list` — Video Requests tab
- `/content/video/library/?part=feedback-queue` — Feedback Queue tab
- `/content/video/library/?part=feedback-detail&id={feedback_id}` — feedback detail drawer
- `/content/video/library/?part=production-gap-finder` — Production Gap Finder table (Tab 5b)
- `/content/video/library/?part=gap-request-modal&subject_id={id}&topic_id={id}` — production gap request modal

---

## 2. Purpose

The Video Library is the master catalogue of every YouTube video mapped into the EduForge platform. Every video that reaches students passes through this page: Curators map it, verify it, tag it to the taxonomy, and track its health.

**Business goals:**
- Single source of truth for all mapped videos (5,000+ target at scale)
- Prevent incorrectly tagged videos from reaching students (a Physics video under Chemistry is a P0 incident)
- Detect broken/unavailable YouTube links before students encounter them (automated daily health check)
- Provide the taxonomy-tagged library that Playlist Manager (E-02) and Syllabus Coverage (D-14) read from
- Surface video production status for MCQ-linked videos (cross-division integration with Div D)

---

## 3. KPI Strip

Four tiles auto-refreshed every 120s (`hx-trigger="every 120s"`):

| Tile | Value | Click Action |
|---|---|---|
| Total Videos | Count of all active mapped videos | Clears filters |
| Unmapped Requests | Count of videos in REQUESTED state | Switches to Requests tab |
| Health Failures | Count of videos flagged UNAVAILABLE or EMBEDDABLE_FALSE | Applies Health=Failed filter |
| Videos This Month | Count mapped in current calendar month | Applies Date filter |

Skeleton: 4 rectangle shimmers. Colour: Health Failures tile turns red when count > 0.

---

## 4. Tabs

| Tab | Label | Default |
|---|---|---|
| 1 | All Videos | ✅ Active |
| 2 | Map New Video | — |
| 3 | Bulk Import | — |
| 4 | Health Check | — |
| 5 | Video Requests | — |
| 6 | Feedback Queue | — |

---

## 5. Section-Wise Detailed Breakdown

---

### Tab 1 — All Videos

**Purpose:** Browse, filter, and manage all mapped videos.

#### Search & Filter Bar

- Search: debounced 300ms. Searches: `title`, `custom_title`, `youtube_video_id`, `channel_name`. While debounce is in-flight: inline "Searching…" spinner replaces the magnifier icon (HTMX `hx-indicator` on search input).
- Advanced Filter Panel (collapsible, "Filters ▼"):

| Filter | Control | Options |
|---|---|---|
| Subject | Multi-select dropdown | All subjects (from D-09 taxonomy) |
| Exam Type | Multi-select dropdown | All exam types |
| Topic | Cascading dropdown (loads after subject selected) | — |
| Content Type | Multi-select | Concept Explainer · Problem Walkthrough · Revision Quick · Shorts |
| Health Status | Multi-select | OK · Failed · Unchecked · Region Blocked — see display-to-DB mapping below |
| Video Source | Multi-select | External (curator mapped) · Channel Upload · Bulk Import |
| Duration | Range | Min–Max minutes |
| Mapped Date | Date range picker | — |
| Production Linked | Toggle | Show only videos with a linked production job |

Active filters: pills below search bar, each dismissible with ×. "Reset All" clears to page 1.

**Health Status filter — display value to DB enum mapping:**

| Filter Display Value | DB `health_status` Values Matched |
|---|---|
| OK | `OK` |
| Failed | `UNAVAILABLE` · `EMBEDDABLE_FALSE` · `PRIVATE` · `DELETED` |
| Unchecked | `UNCHECKED` |
| Region Blocked | `REGION_BLOCKED` |

> The "Failed" filter aggregates all non-OK, non-UNCHECKED, non-REGION_BLOCKED failure states for simplicity. Tab 4 (Health Check) shows the detailed `failure_reason` per video row.

#### Video Table

**Columns:**

| Column | Sortable | Notes |
|---|---|---|
| Thumbnail | No | 80×45px YouTube thumbnail (cached CDN). Fallback: grey rectangle |
| Title | Yes | Custom title if set; otherwise YouTube title. Click → opens detail drawer |
| Subject · Topic | No | "Subject / Topic / Subtopic" breadcrumb |
| Exam Type | No | Pill badge |
| Duration | Yes | HH:MM:SS |
| Content Type | No | Pill badge |
| Health | No | ✅ OK · ❌ Failed · ⚠️ Unchecked · 🌍 Region Blocked |
| Production | No | Camera icon if MCQ-linked job exists. Status: In Production / Published |
| Mapped At | Yes | Relative time + absolute on hover |
| Actions | No | [View] [Edit] [Health Check] [Archive] |

**Pagination:** 25 rows per page. "Showing X–Y of N". URL-bookmarkable `?page=N&sort=X&dir=asc`.

**Bulk Actions** (checkbox select rows):
- Bulk Health Check — queues Celery health check for selected videos (counts YouTube API units: 1 unit per 50 videos)
- Bulk Archive — requires confirmation modal: "Archive {N} videos? They will be removed from all playlists."
- Bulk Retag — opens **Retag Modal (640px)** with an accordion listing each selected video. For each video: current subject/topic/exam type shown read-only + editable dropdowns for new values. **"Apply to All" toggle (top of modal):** when ON, sets the same subject + topic + exam type to all selected videos at once (overrides per-video selections). When OFF, each video can be individually retagged. Confirm button saves all changes in a single batch. ✅ "Retagged {N} videos" toast 4s.

#### Video Detail Drawer (640px right panel)

Opens on row click or [View]/[Edit]. Tabs within drawer:

**Drawer Tab 1 — Details**
- YouTube embed preview (lazy-load via `hx-trigger="revealed"`)
- Custom title (editable for Curator; read-only for others)
- YouTube Video ID + link to YouTube
- Channel name + channel ID
- Duration, Published date (from YouTube)
- Health status badge + last health check timestamp
- "Run Health Check" button (1 unit from quota)

**Drawer Tab 2 — Taxonomy Mapping**
- Subject (searchable dropdown, from D-09 taxonomy)
- Topic (cascading, loads on subject select)
- Subtopic (cascading, loads on topic select)
- Exam Type(s) (multi-select — a single video can apply to multiple exam types)
- Content Type (select: Concept Explainer / Problem Walkthrough / Revision Quick / Shorts)
- Language (select: EN / HI / TE / UR)
- "Save Mapping" button

**Drawer Tab 3 — Production Status**
- Shows if any `video_production_job` has `youtube_video_id` matching this video
- Job title, status badge, assigned producer, SLA due date
- Link → E-05 Production Job Tracker filtered to this video
- If no production job: "No production job linked. This video was mapped from an external source."

**Drawer Tab 4 — History**
- Audit log: mapping changes, custom title edits, health check results, archive/restore actions
- Each row: timestamp · actor role · action · before/after value
- Newest first. 25 per page inside drawer.

**Role-based drawer behaviour:**
- Video Curator (31): all tabs, all edits
- YouTube Channel Manager (33): Tab 1 read + Tab 2 edit (for their channel uploads only)
- Playlist Manager (32), Content Director (18): all tabs read-only

---

### Tab 2 — Map New Video

**Purpose:** Add a single YouTube video to the library.

**Form:**

| Field | Type | Required | Notes |
|---|---|---|---|
| YouTube URL or Video ID | Text input | Yes | Accepts full URL or bare video ID (e.g. `dQw4w9WgXcQ`). Auto-strips URL parameters. |
| Custom Title | Text input | No | Defaults to YouTube title on fetch |
| Subject | Searchable dropdown | Yes | From D-09 taxonomy |
| Topic | Cascading dropdown | Yes | Loads after subject selected |
| Subtopic | Cascading dropdown | No | Loads after topic selected |
| Exam Type(s) | Multi-select | Yes | At least one required |
| Content Type | Select | Yes | Concept Explainer · Problem Walkthrough · Revision Quick · Shorts |
| Language | Select | Yes | EN · HI · TE · UR |

**On Paste URL → "Fetch" button:**
- Calls `videos.list` (1 unit) to validate: video exists, embeddable=true, not region-blocked for IN
- Populates: thumbnail preview, YouTube title, duration, channel name
- If `embeddable=false`: ⚠️ warning toast 8s — "This video cannot be embedded. Students will be redirected to YouTube. Consider an alternative."
- If video not found: ❌ error toast persistent — "Video ID not found on YouTube. Verify the URL and try again."
- If region-blocked: ⚠️ warning toast 8s — "This video is region-blocked in India. Students in all institutions will see an unavailable video."

**Duplicate detection:** After fetch, server checks if `youtube_video_id` already exists in library. If yes: ❌ "This video is already mapped. [View existing mapping →]"

**"Map Video" button:**
- Creates `content_video` record
- Runs async health check (Celery, 1 unit)
- ✅ Success toast 4s — "Video mapped successfully"
- Returns form to blank state for next mapping

**YouTube Search (fallback — expensive):**
- "Can't find the URL? Search YouTube ▼" toggle (collapsed by default)
- Text input + "Search" button
- Calls `search.list` (100 units — labelled in tooltip: "⚡ 100 API units")
- Daily budget: 20 searches. If exhausted: search button disabled, "YouTube search quota exhausted for today. Use direct URL."
- Results: 10-item list (thumbnail + title + channel). Click to fill URL field.

---

### Tab 3 — Bulk Import

**Purpose:** Map multiple videos at once via CSV.

**Step 1 — Upload CSV**
- Drag-and-drop zone + "Browse" button
- Accepts `.csv` only. Max 500 rows per import.
- Required columns: `youtube_url`, `subject`, `topic`, `exam_type`, `content_type`
- Optional columns: `custom_title`, `subtopic`, `language`
- "Download CSV Template" link (always available)

**Step 2 — Validation Preview**
- Table shows all rows with validation status per row:
  - ✅ Valid — ready to import
  - ⚠️ Warning — embeddable=false or region block (can still import)
  - ❌ Error — invalid URL, unknown subject/topic, duplicate
- Summary bar: "N valid · M warnings · K errors"
- Errors are highlighted in red. User can download "Error Report CSV".
- "Fix & Re-upload" or "Import Valid Rows ({N})" button

**Step 3 — Processing**
- Celery task batch-processes valid rows
- Progress bar: HTMX polling every 5s — "Processing: {N}/{Total}"
- On complete: ✅ "Bulk import complete: {N} videos mapped, {K} skipped" (Info 6s)
- Import record saved in `content_video_import_batch` for audit

**YouTube API cost:** 1 unit per 50 videos for metadata fetch. 500 videos = 10 units.

---

### Tab 4 — Health Check

**Purpose:** Detect broken, region-blocked, or unavailable YouTube links before students encounter them.

#### KPI Summary (read from last health check run)

| Metric | Value |
|---|---|
| Last Check | Timestamp of most recent batch health check |
| Total Checked | Count |
| Healthy | Count (green) |
| Failed | Count (red) |
| Unchecked | Count (amber — never health-checked) |

#### Health Check Table

- Same table as All Videos but pre-filtered to: Health Status = Failed OR Unchecked
- Columns: Thumbnail · Title · Subject/Topic · Health Status · Failure Reason · Last Checked · Actions
- Failure reason values: `UNAVAILABLE` · `EMBEDDABLE_FALSE` · `REGION_BLOCKED` · `PRIVATE` · `DELETED`
- Actions per row: [Run Check] (1 unit) · [Archive Video] · [Find Replacement]

#### Bulk Health Check

- "Run Full Health Check" button (prominent, top-right of tab)
- Calls Celery task `run_video_health_check`: processes all active videos in batches of 50 (1 unit per batch)
- Total API units = ceil(total_videos / 50)
- Quota warning: if running full check would push quota above 9,500 units (standardised warning threshold), show confirm: "Full health check will consume {N} units. Current usage: {M}/10,000. Proceed?" Operations are hard-blocked at 10,000 (quota exhausted).
- Progress: HTMX polling every 10s — "Health check in progress: {N}/{Total} checked"
- Scheduled: Celery Beat runs nightly at 2:00 AM IST automatically using the latest `health_status` SLA thresholds from `video_production_config`. **Note:** Changing SLA targets in E-12 does NOT retroactively change the health status of videos that were already checked. Updated thresholds are applied starting from the next nightly health check run (2:00 AM IST following the config change).

---

### Tab 5 — Video Requests

**Purpose:** View requests from Playlist Managers or Channel Managers to add a video covering a specific topic.

**Who submits requests:** Playlist Manager (32), YouTube Channel Manager (33) — from their respective pages.
**Who fulfils:** Video Curator (31).

**Request Table:**

| Column | Notes |
|---|---|
| Subject · Topic · Subtopic | Requested taxonomy node |
| Exam Type | — |
| Requested By | Role label (not name — DPDPA) |
| Requested On | Date |
| Priority | Low · Normal · High |
| Status | Open · In Progress · Fulfilled · Declined |
| Actions | [View] [Mark In Progress] [Fulfil] [Decline] |

**Request status transitions:**
- **Open** → [Mark In Progress] → **In Progress** (Curator has started looking for a match)
- **In Progress** → [Fulfil] (with YouTube URL mapping) → **Fulfilled** (notifies requester)
- **Open** or **In Progress** → [Decline] (with reason) → **Declined** (notifies requester; cannot be reopened)
- "In Progress" indicates the Curator is actively working on it, but no mapping has been confirmed yet. It does not auto-transition — the Curator manually moves it. Declined requests are permanently closed.

**"Fulfil" action:**
- Opens a mini-form: YouTube URL + confirm mapping
- Maps the video and marks request as FULFILLED
- Notifies requester (Div E internal notification, not Div D notification system)

**"Decline" action:**
- Requires reason (text, max 200 chars)
- Marks request DECLINED, notifies requester

**Empty state:** "No open video requests. Playlist Managers and Channel Managers can submit requests from their pages."

---

### Tab 5b — Production Gap Finder (Video Curator 31 only, sub-section within Tab 5)

**Purpose:** Allow the Curator to identify taxonomy nodes (subject/topic/exam type combinations) that have zero mapped videos, and directly request a production job for them — bridging the gap between E-01 library management and E-05 production pipeline.

> This is distinct from "Video Requests" (Tab 5): Requests ask for an external YouTube video to be mapped. Production Gap Finder identifies topics needing a *produced* video and creates a production job in E-05.

**Gap Detection Table:**

| Column | Notes |
|---|---|
| Subject · Topic · Subtopic | Taxonomy node |
| Exam Type | — |
| Mapped Videos | Count from `content_video` |
| In Production | Count of active `video_production_job` for this topic (any status except PUBLISHED/CANCELLED) |
| Published Videos | Count of PUBLISHED production jobs |
| Gap? | ✅ Covered · ⚠️ In Production · ❌ No video — No map, no active job |
| Actions | [Request Production Job] (shown only for ❌ rows) |

**Filters:**
- Subject · Exam Type · Show only gaps (toggle: default ON)
- **Pagination:** 25 rows per page. Default sort: most-accessed topic (from Div H analytics) DESC.

**[Request Production Job] button:**

Opens a lightweight modal (480px):

| Field | Type | Required | Notes |
|---|---|---|---|
| Topic | Read-only | — | Pre-filled from row |
| Content Type | Select | Yes | Concept Explainer · Problem Walkthrough · Revision Quick · Shorts |
| Priority | Select | Yes | Default: Normal |
| Notes to Producer | Textarea | No | Max 300 chars. E.g. "Students frequently search this topic — high demand." |

On submit:
- POST to `/content/video/production/jobs/request-from-library/`
- Creates `video_production_job_request` record (not a full job — a request for the Producer to review and convert)
- Content Producer (82) notified: "Video Curator has flagged a production gap: {Subject} — {Topic} ({Exam Type}). Review and create a job in E-05."
- ✅ "Production gap reported — Producer notified" toast 4s
- Row updates to show ⚠️ "Request sent" badge

> **Note:** This does NOT directly create a `video_production_job` — the Producer reviews and decides. The Curator does not have production pipeline write access. This is a request/suggestion flow only.

---

### Tab 6 — Feedback Queue

**Purpose:** Collect and act on video quality feedback submitted by teachers and institution admins (not students directly — feedback is routed via the institution admin portal). This surfaces reports of incorrect, low-quality, or mistagged videos before the nightly health check catches them.

#### Who Submits Feedback

- Institution admins and teachers submit feedback from the student-facing video player page (outside this admin panel — a "Report Video" button)
- Feedback is routed through `content_video_feedback` and surfaces here for the Curator

#### Feedback Table (Sortable, Selectable, Responsive)

| Column | Sortable | Notes |
|---|---|---|
| Video Title | Yes | Click → opens detail drawer Tab 1 |
| Subject · Topic | No | — |
| Feedback Type | No | Colour pill: Wrong Taxonomy · Audio/Video Issue · Incorrect Content · Broken Link · Other |
| Submitted By | No | "Teacher — {Institution Name}" or "Institution Admin — {Institution Name}" (no personal names — DPDPA) |
| Submitted At | Yes | Relative time |
| Status | No | Pill: Open · Under Review · Resolved · Dismissed |
| Actions | No | [View] [Mark Under Review] [Resolve] [Dismiss] |

**Pagination:** 25 rows per page. Default sort: Submitted At DESC (newest first).
**Filters:** Feedback Type · Status · Subject · Date range.
**Select:** Checkbox. Bulk action: Bulk Dismiss (Curator only, requires confirmation).

#### Feedback Detail Drawer (640px)

Opens on [View] or row click.

**Content:**
- Video thumbnail + title + YouTube link
- Feedback type badge
- Feedback text (full, submitted by reporter)
- Submitted by: role + institution (no name — DPDPA)
- Submitted at: datetime

**Action Panel (Curator only):**

| Action | Behaviour |
|---|---|
| Mark Under Review | Status → UNDER_REVIEW. No notification sent. |
| Resolve — Taxonomy Fixed | Opens mini-form to confirm taxonomy change made. Status → RESOLVED. |
| Resolve — Video Replaced | Links to Map New Video tab to re-map. Status → RESOLVED after new video confirmed. |
| Resolve — No Action | Requires reason (max 200 chars). Status → RESOLVED. |
| Dismiss | Requires reason. Status → DISMISSED. |

✅ "Feedback resolved" toast 4s on any resolve action.
⚠️ "Feedback dismissed" toast 4s on dismiss.

**Empty state (Tab 6):** "No feedback submitted" | "Video feedback from teachers and institution admins will appear here."

> **Health status transition on feedback resolve:** When the Curator resolves a "Broken Link" or "Audio/Video Issue" feedback by archiving or replacing the video, the old video row in Tab 1 animates to a grey "Archived" state (CSS transition 300ms fade + strikethrough on title) and a ✅ toast appears: "Video archived — feedback resolved." The health status badge in the table transitions with a brief green pulse before settling on its new value (CSS `@keyframes pulse-green`, 600ms).

---

## 6. Data Models

### `content_video`
| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `youtube_video_id` | varchar(20) | Unique — YouTube's video ID |
| `custom_title` | varchar(200) | Nullable — overrides YouTube title in UI |
| `youtube_title` | varchar(200) | As returned by YouTube API |
| `youtube_channel_id` | varchar(50) | — |
| `youtube_channel_name` | varchar(200) | — |
| `duration_seconds` | int | — |
| `thumbnail_url` | varchar | CDN-cached thumbnail URL |
| `subject_id` | FK → content_subject | — |
| `topic_id` | FK → content_topic | — |
| `subtopic_id` | FK → content_subtopic | Nullable |
| `exam_type_ids` | M2M → content_exam_type | Via `content_video_exam_type` |
| `content_type` | varchar | Enum: `CONCEPT_EXPLAINER` · `PROBLEM_WALKTHROUGH` · `REVISION_QUICK` · `SHORTS` |
| `language` | varchar | Enum: `EN` · `HI` · `TE` · `UR` |
| `source` | varchar | Enum: `CURATOR_MAPPED` · `CHANNEL_UPLOAD` · `BULK_IMPORT` |
| `health_status` | varchar | Enum: `OK` · `UNAVAILABLE` · `EMBEDDABLE_FALSE` · `REGION_BLOCKED` · `PRIVATE` · `DELETED` · `UNCHECKED` |
| `health_checked_at` | timestamptz | Nullable |
| `is_active` | boolean | Default True — False = archived |
| `mapped_by_id` | FK → auth.User | — |
| `mapped_at` | timestamptz | — |

### `content_video_request`
| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `subject_id` | FK → content_subject | — |
| `topic_id` | FK → content_topic | — |
| `subtopic_id` | FK → content_subtopic | Nullable |
| `exam_type_id` | FK → content_exam_type | — |
| `priority` | varchar | Enum: `LOW` · `NORMAL` · `HIGH` |
| `status` | varchar | Enum: `OPEN` · `IN_PROGRESS` · `FULFILLED` · `DECLINED` |
| `requested_by_id` | FK → auth.User | — |
| `fulfilled_video_id` | FK → content_video | Nullable |
| `decline_reason` | text | Nullable |
| `created_at` | timestamptz | — |

### `content_video_feedback`
| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `video_id` | FK → content_video | — |
| `feedback_type` | varchar | Enum: `WRONG_TAXONOMY` · `AV_ISSUE` · `INCORRECT_CONTENT` · `BROKEN_LINK` · `OTHER` |
| `feedback_text` | text | Submitted by reporter |
| `submitted_by_id` | FK → auth.User | Institution admin or teacher (role stored, not name displayed) |
| `institution_id` | FK → institution | — |
| `status` | varchar | Enum: `OPEN` · `UNDER_REVIEW` · `RESOLVED` · `DISMISSED` |
| `resolution_notes` | text | Nullable — Curator's resolution reason |
| `resolved_by_id` | FK → auth.User | Nullable |
| `created_at` | timestamptz | — |
| `resolved_at` | timestamptz | Nullable |

### `content_video_import_batch`
| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `status` | varchar | Enum: `UPLOADED` · `VALIDATING` · `READY` · `PROCESSING` · `COMPLETE` · `FAILED` |
| `total_rows` | int | — |
| `valid_rows` | int | — |
| `imported_count` | int | — |
| `error_count` | int | — |
| `file_key` | varchar | S3 key of uploaded CSV |
| `error_file_key` | varchar | Nullable — S3 key of error report CSV |
| `uploaded_by_id` | FK → auth.User | — |
| `created_at` | timestamptz | — |
| `completed_at` | timestamptz | Nullable |

---

## 7. Access Control

| Gate | Rule |
|---|---|
| Page access | Video Curator (31), YouTube Channel Manager (33), Playlist Manager (32), Content Director (18) |
| Map New / Edit / Archive | Video Curator (31) only; Channel Manager (33) for their own channel's videos |
| Bulk Import | Video Curator (31) only |
| Health Check (run) | Video Curator (31), Content Director (18) |
| Video Requests (fulfil/decline) | Video Curator (31) only |
| Feedback Queue (view + resolve) | Video Curator (31) only |
| Read-only | Playlist Manager (32), Content Director (18) — cannot edit taxonomy or archive |

---

## 8. Edge Cases & Error States

| Scenario | Behaviour |
|---|---|
| YouTube API quota exhausted (>9,800 units) | Single health check and Map buttons disabled. "API quota exhausted for today" banner. Nightly batch reschedules to next 2:00 AM IST. |
| Video deleted from YouTube between health checks | Nightly health check sets `health_status=DELETED`. Card shows ❌ DELETED badge. Curator prompted to archive. |
| Same video ID mapped twice | Server-side duplicate check prevents creation. Curator sees "Already mapped" with link to existing record. |
| CSV import with 0 valid rows | "No valid rows to import. Download Error Report to see issues." Import button disabled. |
| Archive video still in active playlists | Confirm modal: "This video is in {N} playlist(s). Archiving will remove it from: [playlist names]. Proceed?" Requires explicit confirmation. |
| Health check for region-blocked video | Still marks REGION_BLOCKED. YouTube API returns `regionRestriction.blocked` containing `IN`. |
| Network timeout during single-video fetch | Error toast persistent: "Could not reach YouTube API. Check your connection and try again." No record created. |

---

## 9. Integration Points

| Integration | Direction | What Flows |
|---|---|---|
| D-09 Taxonomy | E-01 reads | Subject / Topic / Subtopic / Exam Type tree for dropdown population |
| D-14 Syllabus Coverage | D-14 reads E-01 | `content_video` count per `topic_id` for coverage calculation |
| E-02 Playlist Manager | E-02 reads E-01 | Video library is the source for adding videos to playlists |
| E-03 Channel Dashboard | E-03 → E-01 | Channel uploads auto-create `content_video` records via Celery sync |
| E-05 Production Job Tracker | E-05 reads E-01 | Production jobs link `youtube_video_id` back to library on publish |
| YouTube Data API v3 | E-01 → YouTube | `videos.list` for metadata fetch + health checks |

---

## 10. UI Patterns & Page-Specific Interactions

### Empty States

| Context | Heading | Subtext | CTA |
|---|---|---|---|
| Library empty | "No videos mapped yet" | "Start by mapping your first video from the YouTube tab." | "Map First Video →" |
| Filter zero | "No videos match these filters" | "Try widening your subject or topic filter." | "Reset Filters" |
| Health tab empty | "All videos are healthy" | "No failed or unchecked videos found." | — |
| Requests empty | "No open requests" | "When Playlist Managers request a video, it appears here." | — |

### Toast Messages

| Action | Toast |
|---|---|
| Video mapped | ✅ "Video mapped successfully" (4s) |
| Mapping updated | ✅ "Mapping saved" (4s) |
| Health check complete (single) | ✅ "Health check complete — {status}" (4s) |
| Full health check queued | ℹ️ "Health check started for {N} videos" (6s) |
| Bulk import complete | ✅ "Bulk import complete: {N} mapped, {K} skipped" (4s) |
| Embeddable=false on map | ⚠️ "Video is not embeddable — students will be redirected to YouTube" (8s) |
| Archive with playlists | ❌ Blocked by confirm modal before archiving |
| Duplicate detected | ❌ "This video is already mapped" (persistent) |
| Feedback resolved | ✅ "Feedback resolved" (4s) |
| Feedback dismissed | ⚠️ "Feedback dismissed" (4s) |
| Video archived via feedback | ✅ "Video archived — feedback resolved" (4s) + row fade-to-grey animation |

---

*Page spec complete.*
*E-01 covers: map → verify → bulk-import → health check → requests.*
