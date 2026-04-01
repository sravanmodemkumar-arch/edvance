# Division E — Video & Learning: Pages List

> **Division:** E — Video & Learning
> **Roles:** Video Curator (31) · Playlist Manager (32) · YouTube Channel Manager (33) · Content Producer — Video (82) · Video Scriptwriter (83) · Script Reviewer (84) · Motion Graphics/Animation Artist (85) · Graphics Designer — Video (86) · Video Editor (87) · Subtitle & Localisation Editor (88) · Video Quality Reviewer (89)
> **Cross-access:** Content Director (18) read-only across all pages
> **Total pages:** 12
> **Scale:** 2.4M–7.6M students across 1,900+ institutions; 74,000 peak concurrent
> **Critical external dependency:** YouTube Data API v3 (10,000 units/day quota shared across all Div E operations)

**YouTube API Quota Policy (platform-wide standard, applied in E-01 and E-03):**

| Threshold | Colour | Behaviour |
|---|---|---|
| ≤ 6,000 units | 🟢 Green | Normal operations |
| 6,001–9,000 units | 🟡 Amber | Visual warning banner. All operations still available. |
| 9,001–9,500 units | 🔴 Red | Quota-intensive operations disabled: bulk health check, bulk channel sync, YouTube search. One-off operations (single health check, single video fetch) still allowed. |
| > 9,500 units | 🔴 Red | **Hard block — all API-dependent actions disabled.** Tooltip: "API quota exhausted for today — available again after midnight PST (1:30 PM IST)." |
| 10,000 units | 🔴 Red | YouTube returns 403 — all API calls fail until quota resets. |

This three-tier policy is applied consistently in E-01 (health checks) and E-03 (channel sync, analytics). Quota resets at midnight PST (1:30 PM IST) daily.

---

## Scale Context

| Segment | Institutions | Students (avg) | Students (max) |
|---|---|---|---|
| Schools | 1,000 | 1,000 | 5,000,000 |
| Colleges | 800 | 500 | 1,600,000 |
| Coaching Centres | 100 | 10,000 | 1,000,000 |
| **Total** | **1,900+** | — | **~7,600,000** |

A single incorrectly tagged video — a Physics video mapped under Chemistry — reaches every student in every institution simultaneously. A broken YouTube link in a crash-course playlist 3 days before an exam is a platform-level incident.

Every MCQ in the question bank (Div D) can have one or more corresponding explanatory videos produced by the Division E production pipeline. This cross-division linkage is the primary driver of the production workflow: a published question triggers a video production job so the Animator (Role 85) can create an explanatory video. Division E is not a support function: it is the study-material quality gate for millions of exam aspirants.

---

## Roles

| # | Role | Phase | Primary Scope |
|---|---|---|---|
| 31 | Video Curator | Phase 1 | Map YouTube videos → subject/topic/exam type taxonomy |
| 32 | Playlist Manager | Phase 1 | Create structured learning paths per syllabus/exam |
| 33 | YouTube Channel Manager | Phase 1 | EduForge official channel — uploads, playlists, metadata |
| 82 | Content Producer — Video | Phase 2 | Manage production pipeline end-to-end; commission briefs; SLA ownership |
| 83 | Video Scriptwriter | Phase 2 | Author scripts from MCQ briefs; collaborate with SMEs |
| 84 | Script Reviewer | Phase 2 | Review scripts for accuracy, pedagogical quality, language |
| 85 | Motion Graphics/Animation Artist | Phase 2 | Create animated explainer videos from approved scripts |
| 86 | Graphics Designer — Video | Phase 2 | Thumbnails, lower-thirds, intro/outro motion assets |
| 87 | Video Editor | Phase 2 | Assemble final video: audio-sync, colour grade, export |
| 88 | Subtitle & Localisation Editor | Phase 2 | Add subtitles (English + regional languages), verify sync |
| 89 | Video Quality Reviewer | Phase 2 | Final QA gate before publish — accuracy, A/V quality, subtitle check |

---

## Pages

| Page | Name | Route | File | Priority | Status |
|---|---|---|---|---|---|
| E-01 | Video Library & Mapping | `/content/video/library/` | `e-01-video-library.md` | P0 | ⬜ Not started |
| E-02 | Playlist Manager | `/content/video/playlists/` | `e-02-playlist-manager.md` | P1 | ⬜ Not started |
| E-03 | YouTube Channel Dashboard | `/content/video/channel/` | `e-03-channel-dashboard.md` | P2 | ⬜ Not started |
| E-04 | Production Dashboard | `/content/video/production/` | `e-04-production-dashboard.md` | P1 | ⬜ Not started |
| E-05 | Production Job Tracker | `/content/video/production/jobs/` | `e-05-production-job-tracker.md` | P0 | ⬜ Not started |
| E-06 | Brief & Script Workspace | `/content/video/production/scripts/` | `e-06-brief-script-workspace.md` | P0 | ⬜ Not started |
| E-07 | Asset Upload & Staging | `/content/video/production/assets/` | `e-07-asset-upload.md` | P1 | ⬜ Not started |
| E-08 | QA Review Queue | `/content/video/production/qa/` | `e-08-qa-review-queue.md` | P1 | ⬜ Not started |
| E-09 | Subtitle Tracking | `/content/video/production/subtitles/` | `e-09-subtitle-tracking.md` | P2 | ⬜ Not started |
| E-10 | Production Analytics | `/content/video/analytics/` | `e-10-production-analytics.md` | P2 | ⬜ Not started |
| E-11 | Publish Queue | `/content/video/production/publish/` | `e-11-publish-queue.md` | P1 | ⬜ Not started |
| E-12 | Production Config | `/content/video/production/config/` | `e-12-production-config.md` | P2 | ⬜ Not started |

---

## Role-to-Page Access Matrix

| Role | E-01 Video Library | E-02 Playlist | E-03 Channel | E-04 Production Dashboard | E-05 Job Tracker | E-06 Brief/Script | E-07 Asset Upload | E-08 QA Queue | E-09 Subtitles | E-10 Analytics | E-11 Publish Queue | E-12 Config |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Video Curator (31) | **Full** | Read + add | Read | Read | Read (own jobs) | Read | — | — | — | Read | — | — |
| Playlist Manager (32) | Read | **Full** | Read | — | — | — | — | — | — | Read | — | — |
| YT Channel Mgr (33) | Read + map channel | Read | **Full** | Read | Read | — | — | — | — | Read | Read + approve | — |
| Content Producer (82) | Read | Read | Read | **Full** | **Full** | Read + commission | Read | Read | Read | **Full** | **Full** | **Full** |
| Scriptwriter (83) | Read | — | — | Read | Own jobs only | **Full** (own scripts) | Upload VO | — | — | — | — | — |
| Script Reviewer (84) | Read | — | — | Read | Own stage | **Full** (review tab) | — | — | — | Read | — | — |
| Animator (85) | Read | — | — | Read | Own jobs only | Read (brief/script) | **Full** (animation) | — | — | — | — | — |
| Graphics Designer (86) | Read | — | — | Read | Own jobs only | Read (brief) | **Full** (graphics) | — | — | — | — | — |
| Video Editor (87) | Read | — | — | Read | Own jobs only | Read (script) | **Full** (edit assets) | — | — | — | — | — |
| Subtitle Editor (88) | Read | — | — | Read | Own jobs only | Read (script) | Read | — | **Full** | — | — | — |
| QA Reviewer (89) | Read | — | — | Read | Own stage | Read | Read | **Full** | Read | — | — | — |
| Content Director (18) | Read | Read | Read | Read | Read | Read | Read | Read | Read | Read | Read | Read |

---

## MCQ-to-Video Integration

Every published MCQ question in Div D (content_question) can have one or more corresponding video production jobs. This is the core cross-division workflow:

### Trigger Points

| Action | Where | Who | Result |
|---|---|---|---|
| "Create Video Job" per question | D-11 Published Bank — question drawer | Content Producer (82), Content Director (18) | Creates `video_production_job` with `question_id` FK, `source=MCQ` |
| "Create Video Job" after approval | D-04 Approval Queue — after approve action | Question Approver (29) triggers; Producer (82) confirms | Draft job created in BRIEF_PENDING state |
| Bulk "Generate Video Jobs" | E-05 Job Tracker — import from D-11 | Content Producer (82) | Multi-select published questions → batch-create jobs |

### Brief Auto-Seeding

When a job is created from an MCQ, Celery auto-populates the brief:
- **Title seed:** Question subject + topic + subtopic
- **Script seed:** Question body + correct answer + explanation text (if present)
- **Taxonomy tags:** Pre-filled from question's exam_type + subject + topic chain
- Scriptwriter sees the seed in E-06 with a yellow banner: *"Script seeded from MCQ #{short_id} — review for accuracy before authoring"*

### Data Model Link

```
content_question (Div D)
    └── video_production_job.question_id FK (nullable — manual jobs have no MCQ link)
            ├── video_script.job_id FK
            ├── video_production_stage_assignment.job_id FK
            ├── video_production_asset.job_id FK
            ├── video_qa_review.job_id FK
            ├── video_subtitle_coverage.job_id FK
            └── video_production_job.parent_job_id FK (self-ref — language variant child jobs)
                    ├── video_production_job (HI variant)
                    ├── video_production_job (TE variant)
                    └── video_production_job (UR variant)
```

### Video Status on Question Cards

- D-11 Published Bank question drawer: "Video Status" row showing `No video` / `In production ({stage})` / `Published ({youtube_url})`
- D-01 SME Dashboard (read-only badge on question row): small camera icon if video job exists

---

## Global UI Standards — Division E

These patterns apply to all 12 Div E pages and are defined once here.

### Toast Notifications
| Variant | Duration | Use |
|---|---|---|
| ✅ Success | 4s | Video mapped, playlist saved, upload queued, job created, script approved |
| ❌ Error | Persistent | YouTube API failure, invalid URL, validation block, file upload error |
| ⚠️ Warning | 8s | API quota low, embeddable=false, region block detected, SLA overdue, asset rejected |
| ℹ️ Info | 6s | Health check started, channel sync started, import in progress, Celery job queued |

### Skeleton Loaders
- **Video table rows:** 8-row shimmer (thumbnail placeholder + 3 text lines per row)
- **KPI tiles:** Rectangle shimmer matching tile dimensions
- **YouTube embed preview:** Grey rectangle 16:9 ratio with play button shimmer
- **Playlist item list:** Drag-handle + thumbnail + title per row skeleton
- **Production job rows:** Stage badge placeholder + 2 text lines + status pill

### Server-Side Pagination
- Default: **25 rows** per page for video library (thumbnails are heavy)
- Playlist items: **50 per page** (text-only)
- Production job lists: **25 per page**
- URL-bookmarkable: `?page=N&sort=X&dir=asc`
- "Showing X–Y of N" always visible

### Search Bar
- Debounced 300ms. Searches: title, custom_title, YouTube video ID, channel name, question ID (for MCQ-linked jobs).
- "×" clear button. Clears to page 1.

### Advanced Filter Panel
- Collapsible (collapsed by default). "Filters ▼" toggle.
- Active filter pills below search bar (each dismissible with ×).
- "Reset All" clears all filters and returns to page 1.

### Empty States
- Three-part structure: Heading + Subtext + CTA (where applicable).
- Match context: empty library vs filtered zero vs no requests.

### Sortable Columns
- ↑ ASC / ↓ DESC indicators in column headers.
- Sort state in URL: `?sort=mapped_at&dir=desc`.
- Only one active sort at a time.

### Drawers
- Video detail/edit drawer: **640px** right panel
- Playlist builder: **860px** right panel (needs space for video search + ordered list)
- Production job drawer: **760px** right panel (stage timeline + brief + assets)
- Script workspace: **full-page** view (not a drawer — navigates to dedicated route)
- Mobile: full-screen bottom sheet for all drawers

### Role-Based UI Visibility
- Write actions hidden (not just disabled) for read-only roles — not rendered server-side.
- "You have read-only access" banner for roles accessing pages outside their write scope.

### Responsive Breakpoints
| Breakpoint | Behaviour |
|---|---|
| Desktop (≥1280px) | Full table, side drawers, filter panel collapsible |
| Tablet (768–1279px) | Filter panel hidden behind "Filters" button; table reduces to key columns |
| Mobile (<768px) | Card layout (thumbnail + title + status); drawer = full screen |

### Charts
- Library: Recharts `BarChart` for subject-wise video counts, `PieChart` for content type distribution
- Playlists: Recharts `ProgressBar` for topic coverage per subject
- Channel: Line charts (views/watch time over time), `BarChart` for top video performance
- Production: `BarChart` for jobs by stage, `LineChart` for weekly throughput, `BarChart` SLA compliance
- All charts: `ResponsiveContainer` wrapper. No-data state: grey placeholder with "No data yet" text.

### YouTube API Quota Awareness
- Quota usage indicator in the page header of E-01, E-02, E-03, E-11 (pages that call YouTube API):
  > `YouTube API: 1,240 / 10,000 units used today`
  > Colour: Green ≤6,000 · Amber 6,001–9,000 · Red >9,000
- Operations that consume quota are labelled with their unit cost in tooltips.
- At >9,000 units used: a persistent amber banner appears: "YouTube API quota is nearly exhausted for today. Search and health check operations are restricted. Quota resets at midnight PST (1:30 PM IST)."
- Production pages (E-04 through E-12) do **not** show the quota indicator — they do not call YouTube API.

### HTMX Loading Patterns
- All table loads: `hx-indicator` spinner on table container.
- KPI strip: `hx-trigger="every 120s"` for E-01/E-03 (YouTube API calls are expensive); `hx-trigger="every 60s"` for production pages.
- YouTube embed preview: lazy-load via `hx-trigger="revealed"` — only load when user scrolls to it.
- Production stage status: `hx-trigger="every 30s"` on active job rows only.

---

## YouTube API Quota Budget

| Operation | Units per call | Max calls/day (budget) | Notes |
|---|---|---|---|
| Video metadata fetch (up to 50 IDs) | 1 | 100 | Health check: 5,000 videos = 100 calls |
| YouTube search.list | 100 | 20 | **Expensive** — use direct URL input whenever possible |
| Channel.list (channel info) | 1 | 10 | One-time per session |
| PlaylistItems.list | 1 | 50 | Channel video sync |
| Videos.list (single ID) | 1 | 500 | Single video map validation |
| YouTube Analytics (separate API) | 1–10 | Budget separately | Analytics has its own quota |

**Rule:** YouTube Search (`search.list`) is restricted to 20 calls/day. Curators should paste YouTube URLs directly. The search box is a fallback, not the primary workflow.

---

## Data Models — Division E (Shared Reference)

### `video_production_job`
| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `title` | varchar(200) | Job title (e.g. "Physics — Optics — Reflection Explained") |
| `question_id` | FK → content_question | **Nullable** — populated when job is MCQ-linked; null for standalone jobs |
| `source` | varchar | Enum: `MCQ` · `MANUAL` · `CHANNEL_REQUEST` |
| `subject_id` | FK → content_subject | — |
| `topic_id` | FK → content_topic | — |
| `exam_type_id` | FK → content_exam_type | — |
| `content_type` | varchar | Enum: `CONCEPT_EXPLAINER` · `PROBLEM_WALKTHROUGH` · `REVISION_QUICK` · `SHORTS` |
| `language` | varchar | Enum: `EN` · `HI` · `TE` · `UR`. Language of this job's video (audio track + on-screen text). EN is the default/primary language. |
| `parent_job_id` | FK → video_production_job | **Self-referential, nullable.** Null = this is a primary (parent) job. Non-null = this job is a language variant of the parent job. All language variant jobs share the same question_id (if MCQ-linked), subject/topic, and content_type as the parent. |
| `status` | varchar | Enum: `BRIEF_PENDING` · `SCRIPT_DRAFT` · `SCRIPT_REVIEW` · `SCRIPT_APPROVED` · `ANIMATION_IN_PROGRESS` · `GRAPHICS_IN_PROGRESS` · `VOICE_OVER_IN_PROGRESS` · `EDIT_IN_PROGRESS` · `AWAITING_SUBTITLE` · `SUBTITLE_IN_PROGRESS` · `QA_REVIEW` · `PUBLISH_QUEUE` · `PUBLISHED` · `ON_HOLD` · `CANCELLED` |
| `priority` | varchar | Enum: `LOW` · `NORMAL` · `HIGH` · `URGENT` |
| `assigned_producer_id` | FK → auth.User | Content Producer (82) managing the job |
| `youtube_video_id` | varchar | Nullable — populated after publish; links back to E-01 video library |
| `d11_sync_status` | varchar | Nullable — Enum: `OK` · `FAILED`. Tracks whether the D-11 question drawer was updated after publish. |
| `qa_revision_count` | int | Default 0 — increments each time QA Reviewer submits REVISION_REQUESTED. When count ≥ `video_production_config.max_qa_revisions`, job auto-transitions to ON_HOLD. |
| `sla_due_date` | date | Overall job deadline |
| `created_at` | timestamptz | — |
| `updated_at` | timestamptz | — |

**Multi-language job relationship:**

```
video_production_job (parent — EN primary)
    ├── video_production_job (child — HI variant, parent_job_id = parent.id)
    ├── video_production_job (child — TE variant, parent_job_id = parent.id)
    └── video_production_job (child — UR variant, parent_job_id = parent.id)
```

Each language variant has its own independent pipeline: own Scriptwriter (localized script or translation), own VOICE_OVER audio track, own subtitle file, own QA review, and own YouTube publish. The ANIMATION stage is **shared** from the parent job — child variant jobs skip ANIMATION and reference the parent's accepted ANIMATION asset. Graphics are also shared from the parent. Only the VOICE_OVER, SCRIPT (if translation required), SUBTITLE, and EDIT stages are separate per language variant.

**Language variant pipeline:**
```
Parent EN job:
  [BRIEF] → [SCRIPT] → [VOICE_OVER] ──┐
                      → [ANIMATION]  ──┼── [EDIT] → [SUBTITLE] → [QA] → [PUBLISH]
                      → [GRAPHICS]   ──┘
                            ↓ (assets shared downward)
Child HI/TE/UR variant job:
  [SCRIPT (translation)] → [VOICE_OVER] → [EDIT (uses parent ANIMATION + GRAPHICS)] → [SUBTITLE] → [QA] → [PUBLISH]
```

### `video_production_stage_assignment`
| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `job_id` | FK → video_production_job | — |
| `stage` | varchar | Enum: `SCRIPT` · `VOICE_OVER` · `ANIMATION` · `GRAPHICS` · `EDIT` · `SUBTITLE` · `QA` |
| `assigned_to_id` | FK → auth.User | Role-specific assignee. Default by stage: SCRIPT→Scriptwriter(83), VOICE_OVER→Scriptwriter(83) [or Producer(82) if external VO], ANIMATION→Animator(85), GRAPHICS→Graphics Designer(86), EDIT→Video Editor(87), SUBTITLE→Subtitle Editor(88), QA→QA Reviewer(89). All assignable/reassignable by Producer(82) in E-05 Tab 2. |
| `status` | varchar | Enum: `PENDING` · `IN_PROGRESS` · `SUBMITTED` · `REVISION_REQUESTED` · `APPROVED` · `PAUSED` · `CANCELLED` |
| `stage_due_date` | date | Stage-level SLA |
| `started_at` | timestamptz | Nullable |
| `submitted_at` | timestamptz | Nullable |
| `approved_at` | timestamptz | Nullable |

### `video_script`
| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `job_id` | FK → video_production_job | OneToOne |
| `seed_text` | text | Auto-populated from MCQ question_body + answer + explanation |
| `body` | text | Full script authored by Scriptwriter |
| `version` | int | Increments on each save |
| `status` | varchar | Enum: `DRAFT` · `SUBMITTED` · `REVISION_REQUESTED` · `APPROVED` |
| `revision_count` | int | Default 0 — increments each time status transitions from APPROVED/SUBMITTED → REVISION_REQUESTED |
| `submitted_at` | timestamptz | — |
| `approved_at` | timestamptz | — |
| `override_approved_by_id` | FK → auth.User | Nullable — set when Producer directly approves (bypasses Script Reviewer) |
| `override_justification` | text | Nullable |
| `locked_by_id` | FK → auth.User | Nullable — set when a user opens the script in edit mode; prevents concurrent edits |
| `locked_at` | timestamptz | Nullable — lock timestamp; lock auto-expires after 30 minutes of inactivity |

### `video_script_review`
| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `script_id` | FK → video_script | — |
| `reviewer_id` | FK → auth.User | Script Reviewer (84) |
| `decision` | varchar | Enum: `APPROVED` · `REVISION_REQUESTED` |
| `feedback` | text | — |
| `reviewed_at` | timestamptz | — |

### `video_production_asset`
| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `job_id` | FK → video_production_job | — |
| `stage` | varchar | Enum: `VOICE_OVER` · `ANIMATION` · `GRAPHICS` · `FINAL_EDIT` |
| `is_thumbnail` | boolean | Default False — for GRAPHICS assets only; marks a 1280×720 PNG/JPG as the YouTube thumbnail for E-11 picker |
| `language` | varchar | Nullable — for VOICE_OVER and FINAL_EDIT stages on language variant jobs: `EN` · `HI` · `TE` · `UR` |
| `file_key` | varchar | S3 object key (CDN-served via presigned URL, 15-min expiry) |
| `file_name` | varchar | Original filename |
| `file_size_mb` | decimal | — |
| `version` | int | 1-based, increments on re-upload |
| `status` | varchar | Enum: `UPLOADED` · `ACCEPTED` · `REJECTED` |
| `rejection_reason` | text | Nullable |
| `uploaded_by_id` | FK → auth.User | — |
| `uploaded_at` | timestamptz | — |

### Pipeline Stage Sequencing (Parallel Execution)

After `SCRIPT_APPROVED`, three stages unlock **simultaneously and independently**:

```
[BRIEF] → [SCRIPT] ──────┬── [VOICE_OVER] ─────────────────────┐
                         ├── [ANIMATION]  ─────────────────────┼── [EDIT] → [AWAITING_SUBTITLE / SUBTITLE_IN_PROGRESS]
                         └── [GRAPHICS]   ─────────────────────┘              │
                                                                               ▼
                                                                          [QA_REVIEW] → [PUBLISH_QUEUE] → [PUBLISHED]
                                                                          (SUBTITLE runs parallel with QA — subtitle must be
                                                                           COMPLETE before QA_REVIEW gate opens)
```

**Stage unlock rules:**
- `VOICE_OVER`, `ANIMATION`, `GRAPHICS` all unlock when `video_script.status = APPROVED`
- `EDIT` stage unlocks only when **all three** (`VOICE_OVER` + `ANIMATION` + `GRAPHICS`) assets are ACCEPTED by Producer
- After EDIT: job enters `AWAITING_SUBTITLE` if mandatory subtitles not yet COMPLETE; transitions to `SUBTITLE_IN_PROGRESS` when subtitle upload begins; transitions to `QA_REVIEW` when all mandatory language subtitles reach `COMPLETE`
- `QA_REVIEW` → `PUBLISH_QUEUE` → `PUBLISHED` is sequential

**Language variant stage differences:**
- Child (HI/TE/UR) jobs skip ANIMATION and GRAPHICS (shared from parent)
- Child jobs: `SCRIPT (translation)` → `VOICE_OVER` → `EDIT (reuse parent ANIMATION + GRAPHICS assets)` → `SUBTITLE` → `QA` → `PUBLISH`

---

### `video_qa_review`
| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `job_id` | FK → video_production_job | — |
| `reviewer_id` | FK → auth.User | Video Quality Reviewer (89) |
| `accuracy_score` | int | 1–5 |
| `av_quality_score` | int | 1–5 |
| `subtitle_score` | int | 1–5 |
| `overall_decision` | varchar | Enum: `PASS` · `REVISION_REQUESTED` · `FAIL` |
| `feedback_notes` | text | — |
| `reviewed_at` | timestamptz | — |

### `video_subtitle_coverage`
| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `job_id` | FK → video_production_job | — |
| `language` | varchar | Enum: `EN` · `HI` · `TE` · `UR` |
| `status` | varchar | Enum: `PENDING` · `IN_PROGRESS` · `COMPLETE` · `QA_FAILED` |
| `subtitle_file_key` | varchar | S3 key for current (active) .srt/.vtt file |
| `current_version` | int | Default 1 — increments on each [Replace] upload |
| `uploaded_by_id` | FK → auth.User | User who uploaded the current version |
| `uploaded_at` | timestamptz | When current version was uploaded |
| `sync_verified` | boolean | Default False — QA Reviewer confirms in E-08 |
| `completed_at` | timestamptz | Nullable — when status set to COMPLETE |

### `video_subtitle_version`
| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `coverage_id` | FK → video_subtitle_coverage | — |
| `version_number` | int | 1-based |
| `file_key` | varchar | S3 key for this version's .srt/.vtt file |
| `file_name` | varchar | Original filename |
| `uploaded_by_id` | FK → auth.User | — |
| `uploaded_at` | timestamptz | — |
| `notes` | varchar(200) | Nullable — e.g. "Fixed sync at 02:30 — QA feedback from v1" |
| `qa_result` | varchar | Nullable — Enum: `PASS` · `FAIL` · `PENDING`. Set after E-08 QA review of this version. |

### `video_production_job_request`
| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `subject_id` | FK → content_subject | — |
| `topic_id` | FK → content_topic | — |
| `subtopic_id` | FK → content_subtopic | Nullable |
| `exam_type_id` | FK → content_exam_type | — |
| `content_type` | varchar | Suggested content type from Curator |
| `priority` | varchar | Suggested priority |
| `notes` | text | Nullable — Curator's notes to Producer |
| `requested_by_id` | FK → auth.User | Video Curator (31) |
| `status` | varchar | Enum: `PENDING` · `ACCEPTED` (Producer created a job) · `DECLINED` |
| `resulting_job_id` | FK → video_production_job | Nullable — set when Producer converts request to a job |
| `created_at` | timestamptz | — |

### `content_video_feedback`
| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `video_id` | FK → content_video | — |
| `feedback_type` | varchar | Enum: `WRONG_TAXONOMY` · `AV_ISSUE` · `INCORRECT_CONTENT` · `BROKEN_LINK` · `OTHER` |
| `feedback_text` | text | Submitted by reporter |
| `submitted_by_id` | FK → auth.User | Institution admin or teacher (role label displayed, not name — DPDPA) |
| `institution_id` | FK → institution | — |
| `status` | varchar | Enum: `OPEN` · `UNDER_REVIEW` · `RESOLVED` · `DISMISSED` |
| `resolution_notes` | text | Nullable — Curator's resolution reason |
| `resolved_by_id` | FK → auth.User | Nullable |
| `created_at` | timestamptz | — |
| `resolved_at` | timestamptz | Nullable |

### `content_channel_upload_queue`

Bridge table used by E-11 (pipeline publish) and E-03 (manual Channel Manager uploads). `production_job_id IS NOT NULL` → pipeline job; `production_job_id IS NULL` → manual upload.

| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `channel_id` | FK → content_channel | YouTube channel to publish to |
| `production_job_id` | FK → video_production_job | Nullable — set for pipeline jobs; NULL for manual uploads (E-03) |
| `title` | varchar(200) | YouTube video title |
| `description` | text | YouTube description (with hashtags) |
| `tags` | varchar[] | YouTube tags array |
| `category_id` | varchar(10) | YouTube category ID (e.g. "27" = Education) |
| `visibility` | varchar | Enum: `PUBLIC` · `UNLISTED` · `PRIVATE` — defaults from E-12 |
| `playlist_id` | FK → content_youtube_playlist | Nullable — auto-add if E-12 default playlist set |
| `thumbnail_asset_id` | FK → video_production_asset | Nullable — GRAPHICS asset with `is_thumbnail=True` |
| `publish_mode` | varchar | Enum: `SEPARATE` · `MULTI_AUDIO` — `SEPARATE` = one YouTube upload per language; `MULTI_AUDIO` = single upload with multiple audio tracks (requires YouTube Partner API) |
| `audio_track_asset_ids` | jsonb | Nullable — `[{"language": "HI", "asset_id": "<uuid>"}, ...]` — used when `publish_mode = MULTI_AUDIO` |
| `youtube_video_id` | varchar(20) | Populated after successful upload |
| `youtube_url` | varchar(200) | Populated after successful upload |
| `status` | varchar | Enum: `PENDING` · `UPLOADING` · `UPLOADED` · `FAILED` · `REJECTED` |
| `celery_task_id` | varchar(50) | Nullable — Celery task tracking upload progress |
| `failure_reason` | text | Nullable — set on FAILED status |
| `rejection_reason` | text | Nullable — set by Channel Manager on REJECTED |
| `created_at` | timestamptz | Set when job status → PUBLISH_QUEUE (Celery `create_publish_queue_entry`) |
| `uploaded_at` | timestamptz | Nullable — set on UPLOADED |
| `created_by_id` | FK → auth.User | Producer for pipeline jobs; Channel Manager for manual |

---

### `video_production_config`
| Field | Type | Notes |
|---|---|---|
| `id` | int | Singleton — always 1 |
| `default_job_sla_days` | int | Default: 14 |
| `script_stage_sla_days` | int | Default: 3 |
| `voice_over_stage_sla_days` | int | Default: 2 |
| `animation_stage_sla_days` | int | Default: 5 |
| `graphics_stage_sla_days` | int | Default: 2 |
| `edit_stage_sla_days` | int | Default: 2 |
| `subtitle_stage_sla_days` | int | Default: 1 |
| `qa_stage_sla_days` | int | Default: 1 |
| `mandatory_subtitle_languages` | varchar[] | Default: ['EN'] |
| `max_asset_size_mb` | int | Default: 2048 (2 GB for video; 500 MB for VOICE_OVER) |
| `voice_over_max_size_mb` | int | Default: 500 |
| `voice_over_accepted_formats` | varchar | Default: 'mp3,wav,aac' |
| `max_script_revisions` | int | Default: 3 — After this many revision cycles in E-06, Scriptwriter submit is blocked |
| `asset_acceptance_sla_hours` | int | Default: 8 — Amber KPI alert on E-07 Tab 3 if UPLOADED assets not accepted within this window |
| `weekly_publish_target` | int | Default: 10 — Reference line in E-04 and E-10 throughput charts |
| `block_publish_if_mandatory_subtitle_missing` | boolean | Default: True — EN required before publish (E-11 enforces) |
| `youtube_multi_audio_enabled` | boolean | Default: False — enables multi-audio track publish option in E-11 (requires YouTube Partner API) |
| `cancelled_job_retention_days` | int | Default: 30 — days to keep S3 assets for cancelled jobs before Celery purge |
| `rejected_asset_retention_days` | int | Default: 90 — days to keep rejected (non-accepted) asset versions |
| `subtitle_version_retention_days` | int | Default: 90 — days to keep superseded subtitle versions |
| `keep_published_assets_indefinitely` | boolean | Default: True — never purge S3 assets for published jobs |
| `max_storage_quota_gb` | int | Default: 5120 — alert threshold (80% amber, 95% red) |
| `updated_by_id` | FK → auth.User | — |
| `updated_at` | timestamptz | — |

---

## `video_production_activity_log`

Write model for the E-10 Activity Log. Entries are created automatically by Django signals and Celery tasks — never written directly by UI actions.

| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `job_id` | FK → video_production_job | — |
| `event_type` | varchar | Enum: `JOB_CREATED` · `STAGE_COMPLETED` · `REVISION_REQUESTED` · `JOB_PUBLISHED` · `JOB_CANCELLED` · `SLA_BREACHED` · `QA_PASS` · `QA_FAIL` |
| `description` | text | Human-readable event message |
| `actor_role` | varchar | Role label of the actor (DPDPA — never personal name) |
| `stage` | varchar | Nullable — pipeline stage where event occurred |
| `triggered_at` | timestamptz | — |

**Event creation rules:**

| Event | Created by | Trigger |
|---|---|---|
| `JOB_CREATED` | Celery / Django view | `video_production_job.status` → `BRIEF_PENDING` |
| `STAGE_COMPLETED` | Django post_save signal | `video_production_stage_assignment.status` → `APPROVED` |
| `REVISION_REQUESTED` | Django post_save signal | `video_production_stage_assignment.status` → `REVISION_REQUESTED` |
| `JOB_PUBLISHED` | Celery `publish_video_to_youtube` | `video_production_job.status` → `PUBLISHED` |
| `JOB_CANCELLED` | Django view (Producer action) | `video_production_job.status` → `CANCELLED` |
| `SLA_BREACHED` | Celery Beat `check_video_production_sla` | Job past `sla_due_date` detected |
| `QA_PASS` | Django view (QA Reviewer action) | `video_qa_review.overall_decision` = `PASS` |
| `QA_FAIL` | Django view (QA Reviewer action) | `video_qa_review.overall_decision` = `FAIL` |

---

## Notification Policy — Division E

All Division E notifications are **in-app only** (Div E internal notification system). No email notifications are sent for any Div E pipeline events. Notifications are delivered to the user's in-app notification bell and their E-04 Production Dashboard notification feed. DPDPA compliance: all notification text uses role labels only (e.g., "Scriptwriter", "QA Reviewer") — never personal names.

---

## Celery Task Registry — Division E

Central reference for all Celery tasks used in the Division E pipeline:

| Task Name | Trigger | Description | Retry Policy |
|---|---|---|---|
| `seed_production_brief_from_question` | Job created from MCQ import | Populates `video_script.seed_text` from question body + answer + explanation | 3× at 60s |
| `check_video_production_sla` | Celery Beat — hourly | Sets `is_overdue=True` on jobs past SLA; notifies Producer | No retry |
| `check_script_review_sla` | Celery Beat — every hour | Notifies Producer if SUBMITTED scripts exceed review SLA | No retry |
| `create_publish_queue_entry` | Job status → PUBLISH_QUEUE | Creates `content_channel_upload_queue` record with status=AWAITING_APPROVAL | 3× at 30s |
| `publish_video_to_youtube` | Celery Beat (scheduled) or "Publish Now" | Uploads FINAL_EDIT asset to YouTube via `videos.insert` | 5× at 5min |
| `publish_video_multi_audio_to_youtube` | "Publish Now" when `publish_mode=MULTI_AUDIO` | Uploads EN video + adds language VOICE_OVER tracks via YouTube Content Manager API | 3× at 5min |
| `sync_d11_video_status` | `post_save` on `video_production_job` when `status→PUBLISHED` | Updates D-11 question drawer with YouTube link | 5× at 30s |
| `run_video_health_check` | Celery Beat — nightly at 2:00 AM IST; or manual | Checks `videos.list` on YouTube for each active `content_video` | 3× at 10min |
| `purge_expired_assets` | Celery Beat — nightly at 2:30 AM IST | Deletes S3 assets beyond retention period (cancelled jobs, rejected versions, old subtitle versions) | No retry |
| `purge_cancelled_job_assets` | Scheduled after job CANCELLED | Schedules S3 asset deletion after `cancelled_job_retention_days` | No retry |

---

## Integration Points — Division E

| Integration | Direction | What Flows |
|---|---|---|
| **Div D — D-09 Taxonomy** | E-01 reads | Subject/Topic/Subtopic tree for video taxonomy mapping |
| **Div D — D-11 Published Bank** | D-11 → E-05 | "Create Video Job" action creates `video_production_job` with `question_id` FK |
| **Div D — D-04 Approval Queue** | D-04 → E-05 | Approver can trigger video job creation on approval |
| **Div D — D-14 Syllabus Coverage** | D-14 reads E-01 | Video coverage count per topic (same taxonomy nodes) |
| **Div H — Analytics** | E pages → H | Video view events, watch duration, completion rate from student portal (EventBridge) |
| **Div C — Engineering** | C maintains | YouTube API key rotation, Celery tasks for health checks + channel sync + SLA monitoring, CDN caching of thumbnails |
| **YouTube Data API v3** | E-01, E-03, E-11 → YouTube | Video metadata fetch, channel video sync, health checks, publish |
| **YouTube Analytics API v2** | E-03 → YouTube | Channel views, watch time, subscriber change |
| **Div L — Marketing** | E-03 ↔ L | Channel Manager (33) coordinates with Social Media Manager (66) for upload strategy |
| **S3 / R2** | E-07, E-08 → S3 | Production assets stored with presigned URL access (15-min expiry) |
| **E-01 — Production Gap Finder** | E-01 → E-05 | Curator requests production job for uncovered topic; creates `video_production_job_request` for Producer review; Producer converts to full `video_production_job` from E-05 Tab 3b |

---

*Division E pages list complete. 12 pages covering the full video lifecycle: map → structure → publish → produce → animate → edit → QA → publish.*
