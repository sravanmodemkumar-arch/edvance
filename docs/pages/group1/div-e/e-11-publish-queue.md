# E-11 — Publish Queue

> **Route:** `/content/video/production/publish/`
> **Division:** E — Video & Learning
> **Primary Role:** Content Producer — Video (82)
> **Supporting Roles:** YouTube Channel Manager (33) — approve channel publish, manage scheduling; Content Director (18) — read-only; Video Curator (31) — read (for library linkage after publish)
> **File:** `e-11-publish-queue.md`
> **Priority:** P1 — Handoff from production pipeline to YouTube channel
> **Status:** ⬜ Not started

---

## 1. Page Name & Route

**Page Name:** Publish Queue
**Route:** `/content/video/production/publish/`
**Part-load routes:**
- `/content/video/production/publish/?part=queue-table` — publish queue table
- `/content/video/production/publish/?part=kpi-strip` — KPI tiles
- `/content/video/production/publish/?part=publish-detail&id={job_id}` — detail drawer
- `/content/video/production/publish/?part=published-history` — published history tab

---

## 2. Purpose

The Publish Queue is the final handoff stage. Videos that pass QA (E-08) enter PUBLISH_QUEUE status and land here. The Content Producer (82) reviews the final package, schedules the upload, and the YouTube Channel Manager (33) approves the channel publish. Once published to YouTube, the video links back to the E-01 library, completing the MCQ-to-video loop.

**Business goals:**
- Provide a controlled handoff from internal production to the public YouTube channel
- Ensure Channel Manager approves before any video goes live
- After publish: automatically create/update the `content_video` record in E-01 to link the produced video back to the library
- For MCQ-linked videos: update `video_production_job.youtube_video_id` so D-11 can show "Video Published" on the question drawer

---

## 3. KPI Strip

Four tiles, `hx-trigger="every 60s"`:

| Tile | Value | Colour Rule |
|---|---|---|
| Ready to Publish | Jobs in PUBLISH_QUEUE, awaiting Channel Manager approval | Amber > 5 |
| Scheduled | Jobs approved + scheduled for future publish | — |
| Published Today | Jobs that went PUBLISHED today | — |
| Failed Publishes | Jobs where YouTube upload failed | Red if > 0 |

Skeleton: 4 rectangle shimmers.

---

## 4. Tabs

| Tab | Label | Default |
|---|---|---|
| 1 | Publish Queue | ✅ Active |
| 2 | Published History | — |

---

## 5. Section-Wise Detailed Breakdown

---

### Tab 1 — Publish Queue

#### Search & Filter Bar

- Search: job title, question ID. Debounced 300ms. "×" clear.
- Advanced Filters (collapsible):

| Filter | Control |
|---|---|
| Status | Multi-select: Awaiting Approval · Approved · Scheduled · Publishing · Failed |
| Subject | Multi-select |
| Exam Type | Multi-select |
| Content Type | Multi-select |
| Language | Multi-select: EN · HI · TE · UR |
| Variant Type | Select: All · Primary only · Language variants only |
| Approved by Channel Manager | Toggle: Yes / No |
| SLA Status | Multi-select: On Time · Overdue |

Active pills + "Reset All".

#### Publish Queue Table (Sortable, Selectable, Responsive)

| Column | Sortable | Notes |
|---|---|---|
| Job Title | Yes | Click → publish detail drawer |
| Source | No | 🔗 MCQ (linked) · ✍️ Manual |
| Subject · Topic | No | — |
| Content Type | No | Pill |
| QA Passed At | Yes | When it entered publish queue |
| Channel Approval | No | ⬜ Pending · ✅ Approved · ❌ Rejected |
| Scheduled For | Yes | Datetime / "Immediate" / "—" |
| Status | No | Awaiting Approval · Approved · Scheduled · Publishing · Published · Failed |
| Actions | No | [View] [Schedule] [Publish Now] [Reject] |

**Row select:** Checkbox. Bulk actions (Producer only):
- Bulk Schedule — set a publish date for multiple jobs at once
- Bulk Approve (Producer can approve on behalf of Channel Manager if Channel Manager is unavailable — requires justification in modal)

**Pagination:** 25 rows per page.

**Responsive:**
- Desktop: full columns
- Tablet: Job Title · Approval · Scheduled · Status · Actions
- Mobile: card — title + approval status + [View]

---

### Publish Detail Drawer (760px)

Opens on row click or [View].

**Drawer Header:**
- Job title
- Status badge (large)
- Language badge: "🇬🇧 EN Primary" (for parent jobs) or "🇮🇳 HI Variant" etc (for child jobs)
- Source badge: "MCQ-Linked: #{question_short_id}" or "Manual"

**Language Variants Summary** (shown on parent jobs only, collapsed by default):

> "This video has {N} language variant(s). Publish each language independently."

| Language | Status | Channel Approval | Actions |
|---|---|---|---|
| HI (Hindi) | PUBLISH_QUEUE | ⬜ Pending | [View HI Publish Package] |
| TE (Telugu) | In Production | — | — |

Clicking "[View {LANG} Publish Package]" switches the drawer to show that variant's publish package (same drawer, changes context). Breadcrumb: "EN Primary → HI Variant".

**Drawer Tab 1 — Publish Package**

**Video Preview:**
- HTML5 `<video>` player (FINAL_EDIT asset from S3, presigned URL, lazy-load)
- Speed controls. Full-screen toggle.
- "This is the final video that will be published to YouTube."

**MCQ Context Panel** (if MCQ-linked):
- Question body (first 100 chars) + "View in D-11 →" link
- Correct answer
- "Publishing an explanatory video for this question"

**Subtitle Coverage:**
- Language rows: EN · HI · TE · UR — ✅ Complete / 🔄 In Progress / ⬜ Pending / ❌ Failed
- **Mandatory subtitle enforcement:** Which languages are mandatory is configured in E-12 Tab 3. EN is always mandatory (locked). HI/TE/UR are mandatory only if toggled ON in E-12. If a mandatory language's subtitle is Missing, In Progress, or Failed → a red ❌ block appears: "Required subtitle missing: {language}. Upload and mark complete in E-09 before publishing." The "Approve for Publish" button for the Channel Manager is disabled until all mandatory subtitles are COMPLETE. Optional languages (not toggled as mandatory) show as informational only — their absence does not block publish.

**YouTube Metadata Form** (editable by Producer, finalised before approval):

| Field | Type | Required | Validation |
|---|---|---|---|
| YouTube Title | Text input | Yes | Max 100 chars (YouTube limit). **Real-time char counter: "45 / 100"** — turns amber at 85+, red at 100. |
| YouTube Description | Textarea | Yes | Max 5,000 chars. Real-time char counter. |
| Tags | Tag input | No | Max 500 chars total (YouTube limit); max 30 chars per tag |
| Category | Select | Yes | YouTube category IDs: Education (27) default |
| Visibility | Select | Yes | Public · Unlisted · Private |
| Scheduled Publish Date | Datetime picker | No | If blank → publish immediately on approval. Max advance: 90 days from today. Dates beyond 90 days show a ⚠️ warning: "Scheduling far in advance may cause stale metadata. Consider scheduling closer to publish time." (Not a block — Producer can proceed.) |
| Add to Playlist(s) | Multi-select | No | Published playlists from E-02 |

**Thumbnail Selection** (below the metadata form):

> **YouTube Thumbnail**
> YouTube requires a 1280×720 PNG/JPG thumbnail. Select from accepted Graphics assets or use the auto-generated frame.

- Grid of accepted GRAPHICS assets for this job that are flagged as "YouTube Thumbnail" in E-07.
  - Each shows: image preview (160×90px) · file name · "Set as Thumbnail" radio button
  - Currently selected: outlined in blue with ✅ "Active"
- "Use Auto-generated Frame" option: YouTube picks a frame from the video. Selected by default if no thumbnail asset exists.
- If no flagged thumbnail assets: ⚠️ "No thumbnail assets uploaded. The Graphics Designer should upload a 1280×720 thumbnail in E-07. YouTube will use an auto-generated frame."
- Thumbnail selection is part of `content_channel_upload_queue.thumbnail_asset_id` (FK → `video_production_asset`).

**Multi-Language Publish Mode** (shown only for parent jobs that have ≥1 language variant also in PUBLISH_QUEUE):

> How do you want to publish the multiple language versions of this video?

Radio selector:

| Option | Description | YouTube API behaviour |
|---|---|---|
| **Separate videos per language** (default) | Each language variant is uploaded as its own YouTube video with its own URL, title, and description. Best for playlists targeting specific language audiences. | One `videos.insert` call per language variant. Each gets its own `youtube_video_id`. |
| **Single video with multi-audio tracks** | All language VOICE_OVER tracks are merged into one YouTube video. Students can switch audio language in the YouTube player. One URL, one video. | One `videos.insert` for the EN video. Each additional language VOICE_OVER is added as an audio track via `videos.update` with `localizations` + `audioTracks` (requires YouTube Partner access or Content Manager API). |

> ⚠️ **Multi-audio track requirement:** YouTube multi-audio track upload requires either YouTube Content ID (available to eligible partners) or YouTube Studio manual import. If the EduForge channel is not a YouTube Partner: ⚠️ "Multi-audio track upload is not available for this channel. Contact your YouTube Partner Manager or use Separate Videos mode." The radio option is greyed out with this tooltip if the channel lacks the required entitlement (`video_production_config.youtube_multi_audio_enabled` toggle in E-12 — default OFF).

**If "Separate videos per language" selected:**
- Each language variant in PUBLISH_QUEUE is listed with its own metadata form and approval status below
- Channel Manager must approve each language independently
- Producer can schedule each language variant at different times (e.g., EN publishes first, HI one week later)

**If "Single video with multi-audio tracks" selected:**
- Only the parent job (EN) metadata is used as the primary video metadata
- "Audio Tracks" section appears below metadata form listing each ready variant: EN · HI · TE (each showing VOICE_OVER file name and size)
- Language labels are set per track (YouTube audio track language codes: `en`, `hi`, `te`, `ur`)
- One Channel Manager approval covers all audio tracks
- On publish: Celery task `publish_video_multi_audio_to_youtube`:
  1. Uploads EN FINAL_EDIT as primary video
  2. For each additional language variant: uploads their VOICE_OVER `.mp3`/`.wav` as a supplementary audio track via YouTube Content Manager API
  3. Sets audio track labels (language names visible to students in player)
- On success: all variant `video_production_job.youtube_video_id` set to the **same** parent YouTube video ID. D-11 question drawer shows one YouTube link labelled "Multi-language (EN · HI · TE)".

**Partial variant publish (MULTI_AUDIO mode):** If not all language variants are in PUBLISH_QUEUE at publish time (e.g., EN + HI + TE are ready but UR is still in production), only the variants currently in PUBLISH_QUEUE are included in the multi-audio upload. UR is excluded at this point and publishes separately later.

When UR eventually reaches PUBLISH_QUEUE and Channel Manager approves:
- A **"Add Audio Track"** action appears in the UR variant's Publish Detail Drawer Tab 1 (in place of the normal Publish Package flow).
- This triggers Celery task `publish_video_multi_audio_to_youtube` in "add track" mode — appends the UR VOICE_OVER as a new audio track to the **existing** YouTube video via YouTube Content Manager API `videos.update` with the existing `youtube_video_id`.
- On success: `video_production_job.youtube_video_id` for the UR variant is set to the same parent YouTube video ID. Producer and Channel Manager notified: "UR audio track added to '{title}' YouTube video."
- Note: Adding tracks to an existing YouTube video carries the same YouTube Partner access requirement as the initial multi-audio upload.

**`content_channel_upload_queue` additions for multi-audio mode:**

| Field | Added value |
|---|---|
| `publish_mode` | Enum: `SEPARATE` (default) · `MULTI_AUDIO` |
| `audio_track_asset_ids` | jsonb array of `video_production_asset.id` for each language VOICE_OVER (used in MULTI_AUDIO mode) |

**Multi-audio metadata rule:** When "Single video with multi-audio tracks" is selected, the **parent EN job's metadata** (YouTube title, description, tags, category, visibility) is used as the primary YouTube video metadata. Language variant metadata is not used — their individual scripts, titles, or descriptions do not appear in the YouTube upload. If multilingual titles or descriptions are needed, the Channel Manager must manually edit the YouTube video in YouTube Studio after publish. The audio track labels (e.g., "Hindi", "Telugu") are set automatically from the variant job's `language` field and are visible to viewers in the YouTube player's audio track selector.

**Publish mode persistence:** The publish mode radio selection ("Separate videos" vs "Single video with multi-audio tracks") is saved to `content_channel_upload_queue.publish_mode` when "Save Metadata" is clicked. Re-opening the drawer shows the previously saved mode. To change mode, select a different radio option and click "Save Metadata" again. Changing mode after Channel Manager approval resets the approval — Producer must re-submit for approval.

"Save Metadata" button — saves without publishing. ✅ "Metadata saved" toast 4s.

**Drawer Tab 2 — Approval**

**For Channel Manager (33):**

- "Approve for Publish" button:
  - Confirm modal: "Approve '{title}' for publishing to EduForge YouTube channel? Visibility: {Public/Unlisted/Private}. Scheduled: {datetime or 'Immediately'}."
  - On approve: `channel_approval = APPROVED`. If no schedule: status → SCHEDULED (immediate). Producer notified.
  - ✅ "Video approved for publish" toast 4s.

- "Reject" button:
  - Reject modal:
    | Field | Required |
    |---|---|
    | Reason Category | Yes: Wrong metadata · Quality concerns · Wrong content · Hold for revision |
    | Specific Feedback | Yes, max 300 chars |
  - On reject: `channel_approval = REJECTED`. Job status and next steps depend on the reason category (see table below). Producer notified.
  - ⚠️ "Publish rejected — Producer notified" warning 8s.

**Rejection consequences by reason category:**

| Reason Category | Job Status After Rejection | Consequence |
|---|---|---|
| Wrong metadata | Stays in `PUBLISH_QUEUE` (`channel_approval = REJECTED`) | Producer corrects title / description / tags / visibility in the metadata form and resubmits for Channel Manager approval. No QA re-review needed. |
| Quality concerns | Reverts to `QA_REVIEW` | QA Reviewer (89) is notified: "'{title}' was rejected from the Publish Queue — Quality concerns: {reason}. Re-review required." Job re-enters QA queue with 🔴 "Returned from Publish" badge (E-08). |
| Wrong content | Set to `ON_HOLD` | Major content issue requiring Producer/Director decision. Producer notified: "'{title}' rejected from Publish Queue — Wrong content: {reason}. Job is on hold — investigate via E-05." Producer must decide whether to revise or cancel the job. |
| Hold for revision | Stays in `PUBLISH_QUEUE` (`channel_approval = REJECTED`) | Channel Manager will re-approve after minor adjustments (metadata, thumbnail, etc.) are made. Producer makes adjustments and requests re-approval — Channel Manager reviews from Drawer Tab 2. |

**For Producer (82):**
- If approved: shows "Approved by Channel Manager at {datetime}"
- If pending: "Awaiting Channel Manager approval"
- "Publish Now" button (Producer) — bypasses schedule, triggers immediate YouTube upload (only if Channel Manager has approved)

**"Publish Now" enforcement rules:**
- Button is **disabled** if Channel Manager approval is PENDING (not yet approved). Tooltip: "Channel Manager approval required before publishing." Enforced server-side: the Celery task `publish_video_to_youtube` checks `channel_approval = APPROVED` before starting upload; if check fails, task aborts.
- **Expected latency:** "Publish Now" enqueues the Celery task immediately. YouTube upload should begin within 30 seconds. If upload has not started within 2 minutes, the Publish Status tab shows: ⚠️ "Upload queued but not yet started — worker may be under load."
- **Celery worker unavailable:** If Celery is unreachable at submit time (Django `celery.app.control.ping()` timeout): ❌ "Cannot publish now — background task worker is unavailable. Try again in a few minutes." toast persistent. Status remains SCHEDULED; no retry is auto-queued — Producer must retry manually.

**Drawer Tab 3 — Publish Status**

Real-time status of the YouTube upload (HTMX polling every 5s while PUBLISHING):

```
[Uploading to YouTube…] ████████░░░░ 68%
```

Or post-publish:

| Field | Value |
|---|---|
| YouTube Video ID | `dQw4w9WgXcQ` (clickable external link) |
| Published At | Datetime |
| Visibility | Public |
| YouTube URL | Full URL (external link) |
| Added to Playlists | List of playlist names |
| Library Status | "Added to E-01 library" ✅ or "Pending library sync" |

**Drawer Tab 4 — Activity Log**

All events for this job in the publish phase: QA passed · Metadata saved · Approved · Scheduled · Publishing started · Published · Failed.

Newest first, 25 per page.

---

### content_channel_upload_queue — Creation Lifecycle

The `content_channel_upload_queue` record is the bridge between E-11 (production pipeline) and E-03 (Channel Manager's YouTube upload view). Here is exactly when and how it is created and updated:

| Step | Event | Who Creates/Updates |
|---|---|---|
| Job enters PUBLISH_QUEUE | QA passes → `video_production_job.status` → PUBLISH_QUEUE | Celery task `create_publish_queue_entry` creates `content_channel_upload_queue` record with `status=AWAITING_APPROVAL`, `production_job_id` FK set, `channel_approval=PENDING` |
| Producer saves metadata | "Save Metadata" button in E-11 drawer | Django view updates `title`, `description`, `tags`, `category`, `visibility`, `scheduled_for`, `thumbnail_asset_id` on the existing queue record |
| Channel Manager approves | "Approve for Publish" in E-11 Drawer Tab 2 | `channel_approval=APPROVED`. If no schedule: `status=SCHEDULED` (immediate) |
| Scheduled time reached / "Publish Now" | Celery Beat checks scheduled jobs every minute; "Publish Now" triggers immediately | Celery task `publish_video_to_youtube` picks up records with `status=SCHEDULED` + `channel_approval=APPROVED` |
| E-03 Channel Dashboard | Tab 2 "Upload Queue" reads `content_channel_upload_queue` records | E-03 shows the same queue — Channel Manager sees all pending uploads in one place whether they came from E-11 or from manual uploads in E-03 |

> **E-03 vs E-11 split:** `content_channel_upload_queue.production_job_id` distinguishes the source. If `production_job_id` is set → originated from production pipeline (E-11). If null → manually created by Channel Manager directly in E-03. E-03 Upload Queue shows ALL records; E-11 Publish Queue only shows records where `production_job_id` is set. There is no double-tracking — it is the same queue table, filtered differently per page.

### Publish Execution

When a job reaches APPROVED + scheduled time (or "Publish Now"):

1. Celery task `publish_video_to_youtube`:
   - Uses YouTube Data API v3 `videos.insert` (upload video) — **not covered by read quota; uses upload quota separately**
   - Uploads FINAL_EDIT asset from S3 to YouTube
   - Sets title, description, tags, category, visibility, scheduled publish time
   - Adds to specified playlists via `PlaylistItems.insert` (1 unit per playlist)
   - `content_channel_upload_queue.status` → PUBLISHING during upload
2. On success:
   - `content_channel_upload_queue.status` → PUBLISHED; `youtube_video_id` set on queue record
   - `video_production_job.status` → PUBLISHED; `youtube_video_id` set
   - Creates/updates `content_video` record in E-01 library (source=`CHANNEL_UPLOAD`, health_status=`OK`)
   - If MCQ-linked: Celery task `sync_d11_video_status` fires **automatically** immediately after successful YouTube upload (triggered by `post_save` signal on `video_production_job` when `status → PUBLISHED`). It updates the D-11 question drawer's "Video Status" row to show "Published" with YouTube link. **SLA: this sync must complete within 2 minutes.** Celery task retries up to 5× at 30s intervals. If D-11 sync fails after all retries: `video_production_job.d11_sync_status` → `FAILED`; Producer sees ⚠️ "D-11 link not updated — manual sync required" in Published History row with **"Sync to D-11" button** (inline in the D-11 Sync column of the Published History table — manually triggers `sync_d11_video_status` Celery task).
   - Channel Manager + Producer notified: "'{title}' is live on YouTube"
3. On failure:
   - `content_channel_upload_queue.status` → FAILED; `failure_reason` stored
   - Producer + Channel Manager notified: "Upload failed for '{title}' — check queue for details"
   - KPI "Failed Publishes" tile turns red

---

### Tab 2 — Published History

**Purpose:** Track all successfully published videos from this pipeline.

#### Search & Filter Bar

- Search: job title, YouTube video ID. Debounced 300ms.
- Filters:

| Filter | Control |
|---|---|
| Subject | Multi-select |
| Exam Type | Multi-select |
| Content Type | Multi-select |
| Visibility | Multi-select: Public · Unlisted · Private |
| Published Date | Date range |
| Source | MCQ-Linked · Manual |

#### Published History Table (Sortable, Selectable, Responsive)

| Column | Sortable | Notes |
|---|---|---|
| Job Title | Yes | — |
| Subject · Topic | No | — |
| Source | No | MCQ icon or Manual |
| YouTube ID | No | Clickable external link to YouTube |
| Published At | Yes | — |
| Visibility | No | Public · Unlisted · Private |
| Library Status | No | ✅ In Library / ❌ Not Synced |
| D-11 Sync | No | ✅ Synced (`d11_sync_status=OK`) / ❌ Failed + **[Sync to D-11]** button (Producer only, shown if `d11_sync_status=FAILED`) / — (shown for standalone/non-MCQ-linked jobs where sync is not applicable). Column is always shown for all rows — non-MCQ rows display "—". |
| Actions | No | [View] [Open in Library →] |

**Pagination:** 25 rows per page.

**"Open in Library →"** — navigates to E-01 with that video's detail drawer open.

---

## 6. Access Control

| Gate | Rule |
|---|---|
| Page access | Content Producer (82), YouTube Channel Manager (33), Content Director (18), Video Curator (31) |
| View publish queue + detail drawer | Producer (82), Channel Manager (33), Director (18) |
| Edit YouTube metadata | Producer (82) only |
| Approve / Reject | YouTube Channel Manager (33) only |
| Publish Now (after approval) | Content Producer (82) only |
| Bulk Schedule | Producer (82) only |
| Published History | All roles with page access |
| "You have read-only access" banner | Video Curator (31), Content Director (18) |

---

## 7. Edge Cases & Error States

| Scenario | Behaviour |
|---|---|
| EN subtitle missing (mandatory per E-12 config) | "Publish" button disabled. Inline error: "EN subtitle is required before publishing. Go to E-09 to upload." |
| YouTube upload quota exceeded | Celery task fails. "YouTube upload quota exceeded — try again after midnight PST." Status → FAILED. Automatic retry next day at 6:00 AM IST. |
| YouTube title > 100 chars | Form validation: "Title must be 100 characters or less (YouTube limit)." Inline error. |
| Channel Manager rejects for quality | Job reverts to QA_REVIEW. **QA Reviewer (89) receives notification: "Publish rejected for '{title}' — Channel Manager feedback: {reason}. Video returned to QA."** QA Reviewer can see the rejection reason in the E-08 queue. |
| Video published but library sync fails | S3 trigger misfires. Celery retry up to 3× for library sync. If all retries fail: "Library Status: Not Synced" in Published History. Manual sync button for Producer. |
| Scheduled publish time arrives but Channel Manager hasn't approved | Job does NOT auto-publish. Scheduled time passes, status stays SCHEDULED. Producer notified: "Scheduled publish time passed for '{title}' — awaiting Channel Manager approval." |
| Duplicate YouTube title for same channel | Allowed (YouTube allows duplicate titles). No block, but Producer sees a warning: "A video with this title already exists on the channel." |
| Language variant ready to publish but parent EN not yet published | Allowed — variants are independent. Warning: "The EN primary version has not been published yet. Consider publishing EN first for a consistent viewer experience." Not a block. |
| All language variants published — link to same MCQ question | All variant `youtube_video_id` values are stored on their respective `video_production_job` records. D-11 question drawer shows all published language versions: "Video Published: 🇬🇧 EN · 🇮🇳 HI · TE" with separate YouTube links per language. |
| Language variant FINAL_EDIT uses wrong language audio | QA checklist item B2 (Audio clear) and C1 (Subtitle sync) will catch mismatched audio. QA Reviewer notes: "Audio language does not match subtitle language." REVISION_REQUESTED. |

---

## 8. UI Patterns

### Empty States

| Context | Heading | Subtext |
|---|---|---|
| Queue empty | "Publish queue is clear" | "Videos will appear here after passing QA review." |
| Filter returns zero | "No videos match" | "Try different subject or status filters." |
| Published history empty | "No videos published yet" | "Published videos will appear here once the first production job completes." |

### Toast Messages

| Action | Toast |
|---|---|
| Metadata saved | ✅ "Metadata saved" (4s) |
| Video approved | ✅ "Video approved for publish" (4s) |
| Publish rejected | ⚠️ "Publish rejected — Producer notified" (8s) |
| Video published | ✅ "'{title}' is live on YouTube" (4s) |
| Publish failed | ❌ "Upload failed — check queue for details" (persistent) |
| Scheduled | ✅ "Publish scheduled for {datetime}" (4s) |

### Loading States

- Queue table: 8-row shimmer
- KPI strip: 4 tile shimmers
- Drawer — video player: 16:9 grey rectangle shimmer
- Publish status (during upload): real progress bar with %, not a shimmer

### Responsive Behaviour

| Breakpoint | Behaviour |
|---|---|
| Desktop (≥1280px) | Full table (all columns) + 760px drawer |
| Tablet (768–1279px) | Publish Queue table: Title · Language · Approval · Scheduled · Status · Actions. Published History table: Title · Language · Published At · D-11 Sync · Actions. Drawer: full-width. |
| Mobile (<768px) | Card layout (title + approval badge + language pill + [View]). Published History: card (title + published date + D-11 sync status). Drawer: full-screen. Video player full-width at top. Metadata form scrolls below. |

---

*Page spec complete.*
*E-11 covers: QA-passed jobs → YouTube metadata → Channel Manager approval → scheduled/immediate publish → YouTube upload → E-01 library auto-link → MCQ question "Video Published" status update → history.*
