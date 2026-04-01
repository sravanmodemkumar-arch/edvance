# E-03 — YouTube Channel Dashboard

> **Route:** `/content/video/channel/`
> **Division:** E — Video & Learning
> **Primary Role:** YouTube Channel Manager (33)
> **Supporting Roles:** Video Curator (31) — read + map channel uploads; Content Director (18) — read-only analytics; Playlist Manager (32) — read-only
> **File:** `e-03-channel-dashboard.md`
> **Priority:** P2
> **Status:** ⬜ Not started

---

## 1. Page Name & Route

**Page Name:** YouTube Channel Dashboard
**Route:** `/content/video/channel/`
**Part-load routes:**
- `/content/video/channel/?part=kpi-strip` — 5 KPI tiles (polled every 120s)
- `/content/video/channel/?part=analytics-charts` — analytics charts section
- `/content/video/channel/?part=upload-queue` — upload queue tab content
- `/content/video/channel/?part=new-uploads` — unsynced new uploads tab
- `/content/video/channel/?part=comments-list` — comments moderation tab

---

## 2. Purpose

The Channel Dashboard is the command centre for EduForge's official YouTube channel. The YouTube Channel Manager (33) monitors analytics, manages the upload queue (videos ready to go live), syncs new channel uploads into the E-01 library, and moderates comments.

**Business goals:**
- Know which videos are performing well so curation and production priorities are informed
- Ensure every new channel upload is tagged into the E-01 library (prevents orphaned uploads)
- Manage the public-facing comment section to maintain brand reputation
- Monitor channel health metrics (subscriber growth, watch time, quota usage)

---

## 3. YouTube API Quota Indicator

Displayed in page header (visible to all roles on this page):
> `YouTube API: 1,240 / 10,000 units used today`
> Colour: Green ≤6,000 · Amber 6,001–9,000 · Red >9,000

At >9,000 units: amber banner — "YouTube API quota nearly exhausted. Sync and comment moderation operations may be impacted. Resets at midnight PST (1:30 PM IST)." At >9,500 units: quota-intensive operations (bulk sync, channel search) are **disabled** with tooltip "Quota limit reached — available after midnight PST." Hard block at 10,000 (quota exhausted — all API-dependent actions disabled). This threshold policy is standardised with E-01 health check enforcement.

---

## 4. KPI Strip

Five tiles, `hx-trigger="every 120s"` (data from YouTube Analytics API — separate quota):

| Tile | Value | Notes |
|---|---|---|
| Channel Subscribers | Total subscriber count | ▲/▼ change vs last 7 days |
| Total Views (30 days) | Rolling 30-day view count | — |
| Watch Time (30 days) | Hours watched | — |
| Uploaded Videos | Total channel video count | — |
| Unsynced Uploads | Videos on channel not yet in E-01 library | Turns amber if > 0 |

Skeleton: 5 rectangle shimmers.

---

## 5. Tabs

| Tab | Label | Default |
|---|---|---|
| 1 | Analytics | ✅ Active |
| 2 | Upload Queue | — |
| 3 | New Uploads | — |
| 4 | Comments | — |

---

## 6. Section-Wise Detailed Breakdown

---

### Tab 1 — Analytics

#### Charts Section

All charts use Recharts with `ResponsiveContainer`. No-data state: grey placeholder + "No data yet" text.

**Chart 1 — Views & Watch Time (Line Chart)**
- X-axis: last 30 days (daily)
- Y-axis: Views (left) and Watch Time hours (right, secondary axis)
- Two lines: Views (blue) · Watch Time (green)
- Toggle: 7 days / 30 days / 90 days (HTMX reload on change)
- Data source: YouTube Analytics API v2

**Chart 2 — Top 10 Videos by Views (Bar Chart)**
- Horizontal bar chart
- Y-axis: video titles (truncated to 30 chars)
- X-axis: view count
- Click a bar → opens E-01 detail drawer for that video
- Toggle: 7 days / 30 days / all time

**Chart 3 — Subscriber Growth (Line Chart)**
- X-axis: last 90 days (weekly)
- Y-axis: net subscriber change per week
- Bars for gained subscribers (green) and lost (red) — stacked bar variant

**Chart 4 — Traffic Sources (Pie Chart)**
- Slices: Search · Browse features · Suggested · External · Playlist · Other
- Legend on right. Click slice → tooltip with count + %

#### Top Video Performance Table

Below charts. Sortable. Server-side pagination: 25 rows per page.

| Column | Sortable | Notes |
|---|---|---|
| Thumbnail | No | 80×45px |
| Title | Yes | Click → E-01 drawer |
| Views (30d) | Yes | — |
| Watch Time (30d) | Yes | Hours |
| Avg View % | Yes | Average percentage of video watched |
| Likes | Yes | — |
| Comments | Yes | — |
| Published | Yes | — |

**Search:** title search. Debounced 300ms.
**Filters:** Date range, minimum views threshold.

**Role-based visibility:** All roles see this tab read-only. No write actions.

#### Data Freshness

Analytics chart data (Charts 1–4 and Top Video Performance Table) is loaded on page load and does **not** auto-refresh on a timer — this prevents costly YouTube Analytics API calls on every refresh. Charts reload when the time period toggle (7 days / 30 days / 90 days) is changed or when the page is reloaded manually. Data is cached in Memcached for 30 minutes per time period per chart. The cache timestamp is shown in a tooltip on each chart: "Data as of {N} min ago." The KPI strip (Section 4) is polled separately every 120s and reflects live data regardless of chart cache.

---

### Tab 2 — Upload Queue

**Purpose:** Manage videos ready to be published to the YouTube channel — scheduled or immediate.

#### Search & Filter Bar

- Search: title. Debounced 300ms.
- Advanced Filters (collapsible):

| Filter | Control |
|---|---|
| Status | Multi-select: Scheduled · Ready · Publishing · Published · Failed |
| Subject | Multi-select |
| Content Type | Multi-select |
| Scheduled Date | Date range |

Active filter pills below search. "Reset All" clears to page 1.

#### Upload Queue Table (Sortable, Selectable, Responsive)

| Column | Sortable | Notes |
|---|---|---|
| Title | Yes | — |
| Subject · Topic | No | — |
| Content Type | No | Pill |
| Production Source | No | "Production Job #{id}" or "External" |
| Status | No | Scheduled / Ready / Publishing / Published / Failed — colour pills |
| Scheduled For | Yes | Datetime or "Immediate" |
| Actions | No | [View] [Edit Schedule] [Publish Now] [Remove] |

**Pagination:** 25 rows per page. "Showing X–Y of N".
**Row select:** checkbox column. Bulk action: "Publish Selected" (for Ready-status items only).

**Responsive:**
- Desktop (≥1280px): full column set as above
- Tablet (768–1279px): Title · Status · Scheduled For · Actions
- Mobile (<768px): card — title + status badge + [View]

#### Create Upload Queue Entry — Modal (640px)

Triggered by "Queue Video" button (top-right). Role: YouTube Channel Manager (33) only.

**Form Fields:**

| Field | Type | Required | Validation |
|---|---|---|---|
| Video Source | Radio | Yes | Options: From Production Job · External YouTube URL |
| Production Job | Searchable dropdown (if source = Production Job) | Conditional | Only shows PUBLISH_QUEUE status jobs from E-11 |
| YouTube URL | Text input (if source = External) | Conditional | Must be valid YouTube URL |
| Title Override | Text input | No | If blank: uses production job title or YouTube title |
| Scheduled For | Datetime picker | No | If blank: publishes immediately on "Publish Now" |
| Visibility | Select | Yes | Public · Unlisted · Private |
| Add to Playlist(s) | Multi-select (from E-02) | No | Published playlists only |
| Tags | Tag input | No | Max 10 tags, each max 30 chars |
| Description | Textarea | No | Max 5,000 chars |

**Form validation:**
- If source = External URL: validates YouTube URL format before submission
- If Scheduled For is in the past: inline error "Scheduled time must be in the future"
- If no production job selected when source = Production Job: required error

**Actions:**
- "Save to Queue" → creates `content_channel_upload_queue` record in SCHEDULED or READY state
- "Cancel" → closes modal, no changes

#### Upload Queue Detail / Edit — Drawer (640px)

Opens on [View] or [Edit Schedule].

**View tab:**
- All metadata fields (read-only)
- Current status badge
- Timeline: Queued at · Scheduled for · Published at (if published)
- YouTube URL (if published) with external link

**Edit tab** (Channel Manager only, only for SCHEDULED / READY status):
- Editable: Scheduled For · Visibility · Playlist assignment · Tags · Description
- "Save Changes" button

**Delete action** (Channel Manager only):
- "Remove from Queue" — only available for SCHEDULED / READY status
- Confirm modal: "Remove '{title}' from the upload queue?" [Confirm] [Cancel]
- Published entries cannot be deleted (link to YouTube remains)

**Loading state:** Drawer skeleton — header shimmer + 4 field shimmers.

---

### Tab 3 — New Uploads

**Purpose:** Show videos recently uploaded to the EduForge YouTube channel that have NOT yet been mapped into E-01 (unsynced uploads).

#### Channel Sync

- "Sync Channel" button (top-right): calls Celery task `sync_youtube_channel` — fetches latest `PlaylistItems.list` (1 unit per 50 videos) for the channel's uploads playlist
- Last sync timestamp always shown: "Last synced: {relative time}"
- `hx-trigger="every 300s"` auto-sync every 5 minutes (passive, no user action needed)

#### Unsynced Uploads Table (Sortable, Selectable, Responsive)

| Column | Sortable | Notes |
|---|---|---|
| Thumbnail | No | From YouTube |
| YouTube Title | Yes | — |
| Channel | No | EduForge channel name |
| Uploaded At | Yes | Date uploaded to YouTube |
| Duration | No | — |
| Map Status | No | Not Mapped / Mapped (with link) |
| Actions | No | [Map to Library] |

**Pagination:** 25 rows per page.
**Select all:** checkbox. Bulk action: "Bulk Map to Library" — opens bulk mapping modal.

**Responsive:**
- Desktop (≥1280px): full column set as above
- Tablet (768–1279px): YouTube Title · Uploaded At · Map Status · Actions
- Mobile (<768px): card — video title + upload date + [Map to Library]

#### Map to Library — Modal (640px)

Triggered by [Map to Library] on a single row, or bulk modal for multiple.

**Form (per video):**

| Field | Type | Required | Validation |
|---|---|---|---|
| Subject | Searchable dropdown | Yes | From D-09 taxonomy |
| Topic | Cascading dropdown | Yes | — |
| Subtopic | Cascading dropdown | No | — |
| Exam Type(s) | Multi-select | Yes | At least 1 |
| Content Type | Select | Yes | — |
| Language | Select | Yes | Default: EN |
| Custom Title | Text input | No | — |

**Multi-language video handling:** If the YouTube video contains multiple audio tracks (a multi-audio track video published via E-11), select the **primary language** of the video (typically EN). Map it as a single `content_video` record. If the video has separate language variants published as individual YouTube videos, each variant should be mapped individually — one [Map to Library] action per language video, each with its own language selection. If unsure whether a channel video is multi-audio or multi-upload, check with the production team via E-05 before mapping.

**Bulk mapping:** form repeated per video (accordion) or "Apply same taxonomy to all" shortcut.

**Validation:** Subject + Topic + Exam Type required before save.

"Map Video" → creates `content_video` record in E-01. Success: row disappears from unsynced table. ✅ "Video mapped to library" toast 4s.

**Loading state:** Table skeleton — 8 rows of shimmer (thumbnail + 3 text lines).
**Empty state:** "All channel uploads are mapped to the library. ✅" — no further action needed.

---

### Tab 4 — Comments

**Purpose:** Moderate comments on EduForge's YouTube channel videos to maintain brand reputation and flag policy violations.

> Note: YouTube comment moderation via API requires YouTube Data API v3 `CommentThreads.list` (1 unit per 50 comments). Heavy moderation consumes quota.

#### Search & Filter Bar

- Search: comment text, video title. Debounced 300ms.
- Advanced Filters (collapsible):

| Filter | Control |
|---|---|
| Status | Multi-select: Pending · Approved · Rejected · Spam |
| Video | Search by video title |
| Date Range | — |
| Flagged | Toggle — show only flagged/reported comments |

#### Comments Table (Sortable, Selectable, Responsive)

| Column | Sortable | Notes |
|---|---|---|
| Video | No | Thumbnail + title |
| Comment | No | Truncated to 120 chars. Click → expand |
| Author | No | YouTube display name (external, not DPDPA-covered) |
| Posted At | Yes | — |
| Likes | Yes | — |
| Status | No | Pending · Approved · Rejected · Spam |
| Actions | No | [Approve] [Reject] [Mark Spam] [Hide] |

**Pagination:** 25 rows per page.
**Bulk actions:** Bulk Reject · Bulk Mark Spam (with confirmation modal).

**Responsive:**
- Desktop (≥1280px): full column set as above
- Tablet (768–1279px): Video · Comment (truncated) · Status · Actions
- Mobile (<768px): card — video title + comment preview + [View]

#### Comment Detail Drawer (640px)

Opens on comment row click or [View] action.

**Content:**
- Video thumbnail + title + YouTube link
- Full comment text (not truncated)
- Comment thread (replies, if any) — collapsible
- Author YouTube name + URL
- Comment metrics: likes, reply count, posted timestamp

**Actions (Channel Manager only):**
- Approve — marks comment as APPROVED in `content_channel_comment`
- Reject — hides comment from YouTube channel via API. Requires confirm: "Hide this comment from YouTube? This calls the YouTube API."
- Mark as Spam — marks SPAM status; queues Celery task to report to YouTube
- Add Note — internal note for audit (not sent to YouTube)

**Loading state:** Drawer skeleton — 2 shimmer blocks.

**Role-based visibility:** Only YouTube Channel Manager (33) sees Approve/Reject/Mark Spam actions. Other roles see comment text and status read-only.

---

## 7. Data Models

### `content_channel_upload_queue`
| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `production_job_id` | FK → video_production_job | Nullable — populated if from E-11 |
| `youtube_video_id` | varchar(20) | Nullable — populated after publish |
| `title` | varchar(200) | — |
| `description` | text | Nullable |
| `tags` | varchar[] | Max 10 |
| `visibility` | varchar | Enum: `PUBLIC` · `UNLISTED` · `PRIVATE` |
| `playlist_ids` | M2M → content_playlist | — |
| `status` | varchar | Enum: `SCHEDULED` · `READY` · `PUBLISHING` · `PUBLISHED` · `FAILED` |
| `scheduled_for` | timestamptz | Nullable |
| `published_at` | timestamptz | Nullable |
| `failure_reason` | text | Nullable |
| `queued_by_id` | FK → auth.User | — |
| `created_at` | timestamptz | — |

### `content_channel_comment`
| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `youtube_comment_id` | varchar(50) | YouTube's comment ID — unique |
| `youtube_video_id` | varchar(20) | — |
| `author_name` | varchar(200) | External YouTube display name |
| `body` | text | Comment text |
| `like_count` | int | — |
| `status` | varchar | Enum: `PENDING` · `APPROVED` · `REJECTED` · `SPAM` |
| `internal_note` | text | Nullable — Channel Manager note |
| `posted_at` | timestamptz | From YouTube |
| `synced_at` | timestamptz | When EduForge synced this comment |
| `moderated_by_id` | FK → auth.User | Nullable |
| `moderated_at` | timestamptz | Nullable |

---

## 8. Access Control

| Gate | Rule |
|---|---|
| Page access | YouTube Channel Manager (33), Video Curator (31), Playlist Manager (32), Content Director (18) |
| Analytics tab | All roles — read-only |
| Upload Queue — create/edit/delete | YouTube Channel Manager (33) only |
| New Uploads — map to library | YouTube Channel Manager (33) and Video Curator (31) |
| Comments — moderation actions | YouTube Channel Manager (33) only |
| Comments — read | All roles |
| "You have read-only access" banner | Shown to Playlist Manager (32) and Content Director (18) |

---

## 9. Edge Cases & Error States

| Scenario | Behaviour |
|---|---|
| YouTube Analytics API quota exceeded | Charts show "Analytics unavailable — quota exhausted" grey state. KPI tiles show last cached values with "Cached {N}h ago" label. |
| Channel sync returns no new videos | "All uploads are synced. No new videos found." info toast 6s. |
| Comment hide API call fails | Error toast persistent: "Could not hide comment — YouTube API error. Try again." Comment stays PENDING in DB. |
| Upload queue publish fails (YouTube API) | Status set to FAILED. Failure reason stored. Channel Manager notified: "Upload failed for '{title}'. Check queue for details." |
| Video in upload queue already published manually to YouTube | Duplicate detection: if `youtube_video_id` already exists in `content_video`, show warning: "This video is already in the library." |
| Comment table empty (no comments synced yet) | "No comments synced yet. Run a channel sync to load comments." with sync button CTA. |

---

## 10. UI Patterns

### Empty States

| Context | Heading | Subtext | CTA |
|---|---|---|---|
| Upload queue empty | "Upload queue is empty" | "Queue videos from the production pipeline or external URLs." | "Queue Video →" |
| No unsynced uploads | "All uploads are mapped" | "Every channel video is in the library. ✅" | — |
| Comments pending | "No comments to review" | "Comments will appear after the next channel sync." | "Sync Channel" |
| Analytics no data | "No analytics yet" | "Analytics data will appear after the channel has published videos." | — |

### Toast Messages

| Action | Toast |
|---|---|
| Queued for upload | ✅ "Video added to upload queue" (4s) |
| Schedule updated | ✅ "Schedule updated" (4s) |
| Removed from queue | ✅ "Removed from upload queue" (4s) |
| Video mapped to library | ✅ "Video mapped to library" (4s) |
| Comment hidden | ✅ "Comment hidden from channel" (4s) |
| Comment marked spam | ✅ "Marked as spam — reported to YouTube" (4s) |
| Channel sync started | ℹ️ "Channel sync started" (6s) |
| Publish failed | ❌ "Upload failed — see queue for details" (persistent) |

### Loading States

- KPI strip: 5 rectangle shimmers
- Analytics charts: grey rectangle placeholder matching chart area dimensions
- Tables: 8-row shimmer per table
- Drawers: header shimmer + 4 field line shimmers

### Responsive Behaviour

| Breakpoint | Behaviour |
|---|---|
| Desktop (≥1280px) | Full table, side drawers, filter panel collapsible |
| Tablet (768–1279px) | Filter panel behind "Filters" button; table reduces to: thumbnail + title + status + actions |
| Mobile (<768px) | Card layout (thumbnail + title + status badge); drawer = full screen bottom sheet |

---

*Page spec complete.*
*E-03 covers: channel analytics → upload queue → map new uploads → comment moderation.*
