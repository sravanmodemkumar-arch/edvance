# E-02 — Playlist Manager

> **Route:** `/content/video/playlists/`
> **Division:** E — Video & Learning
> **Primary Role:** Playlist Manager (32)
> **Supporting Roles:** Video Curator (31) — read + add videos; Content Director (18) — read-only; YouTube Channel Manager (33) — read-only
> **File:** `e-02-playlist-manager.md`
> **Priority:** P1 — Required before structured learning paths can be delivered
> **Status:** ⬜ Not started

---

## 1. Page Name & Route

**Page Name:** Playlist Manager
**Route:** `/content/video/playlists/`
**Part-load routes:**
- `/content/video/playlists/?part=kpi-strip` — KPI tiles (polled every 120s)
- `/content/video/playlists/?part=playlist-table` — main playlist list
- `/content/video/playlists/?part=playlist-detail&id={playlist_id}` — detail drawer
- `/content/video/playlists/?part=builder&id={playlist_id}` — full-page playlist builder
- `/content/video/playlists/?part=coverage-map` — coverage map tab

---

## 2. Purpose

Playlist Manager organises mapped videos (from E-01) into curated learning sequences — topic-by-topic learning paths, exam crash courses, chapter-wise revision sets. These playlists are what students actually consume on the student portal.

**Business goals:**
- Structure the video library into learnable sequences — not just a catalogue
- Ensure every major exam has at least one complete crash-course playlist (syllabus alignment check)
- Version playlists so that pre-exam content can be locked while a new version is being edited
- Prevent empty or incomplete playlists from going live (publish guard: min 3 videos)
- Track coverage: which topics have a playlist and which do not

---

## 3. KPI Strip

Four tiles, `hx-trigger="every 120s"`:

| Tile | Value | Click Action |
|---|---|---|
| Total Playlists | Count of all active playlists | Clears filters |
| Published | Count with status=PUBLISHED | Applies Status=Published filter |
| Draft | Count with status=DRAFT | Applies Status=Draft filter |
| Topics Without Playlist | Count of taxonomy topics with no associated playlist | Switches to Coverage Map tab |

---

## 4. Tabs

| Tab | Label | Default |
|---|---|---|
| 1 | All Playlists | ✅ Active |
| 2 | Playlist Builder | Opens on create/edit |
| 3 | Coverage Map | — |
| 4 | Syllabus Alignment | — |

---

## 5. Section-Wise Detailed Breakdown

---

### Tab 1 — All Playlists

#### Search & Filter Bar

- Search: title, description, exam type. Debounced 300ms.
- Advanced Filters (collapsible):

| Filter | Control |
|---|---|
| Subject | Multi-select |
| Exam Type | Multi-select |
| Status | Multi-select: Draft · Published · Archived |
| Created By | My Playlists / All |
| Published Date | Date range |
| Coverage | Complete · Incomplete (< 80% topics covered) |

#### Playlist Table

| Column | Sortable | Notes |
|---|---|---|
| Title | Yes | — |
| Subject · Exam Type | No | — |
| Videos | No | Count of videos in playlist |
| Status | No | Draft · Published · Archived — colour-coded pills |
| Version | No | e.g. "v3" |
| Coverage % | Yes | Topic coverage (see Coverage Map) |
| Published At | Yes | Nullable |
| Actions | No | [View] [Edit] [Publish] [Archive] [Duplicate] |

**Pagination:** 25 rows per page.

**Bulk Actions:**
- Bulk Archive (with confirmation modal)
- Bulk Publish — **"Bulk Publish" button is only enabled if ALL selected playlists have ≥ 3 videos.** If any selected playlist fails the guard, the button is disabled with tooltip: "Some selected playlists have fewer than 3 videos — deselect them or add more videos before publishing." This check is performed client-side on selection change so the button state updates immediately.

#### Playlist Detail Drawer (640px)

**Drawer Tab 1 — Info**
- Title, description, subject, exam type, status, version
- Video count, total duration (sum of all video durations)
- Coverage % (% of syllabus topics covered by at least 1 video)
- "Open in Builder →" button

**Drawer Tab 2 — Videos List**
- Ordered list of all videos (drag-order visible but not editable from drawer)
- Each row: position number · thumbnail · title · duration · topic
- "Open in Builder to reorder" message

**Drawer Tab 3 — Version History**
- Table: Version · Published At · Published By (role label) · Video Count · Notes
- "Restore to this version" button (creates a new draft based on that version)

---

### Tab 2 — Playlist Builder (Full-Page, 860px wide panel)

**Route:** `/content/video/playlists/builder/{playlist_id}/`
**New playlist:** `/content/video/playlists/builder/new/`

The builder is a two-column layout:
- **Left column (400px):** Video search from E-01 library
- **Right column (460px):** Ordered playlist (drag-to-reorder)

#### Left Column — Video Search

- Subject filter (required to load results)
- Topic filter (cascading)
- Search by title / YouTube ID
- Results list: thumbnail · title · duration · topic · content type · [+ Add] button
- Already-added videos show a ✅ checkmark instead of [+ Add]
- YouTube API quota NOT consumed here — searches the local `content_video` table only

#### Right Column — Playlist Sequence

- Drag handle (⠿) per row for reorder
- Row: position number · thumbnail · title · duration · topic · [↑] [↓] arrows · [Remove ×]
- **Section dividers:** Playlist Manager can insert a text-only section header (e.g. "Chapter 1: Mechanics") between videos — drag-reorderable, not a video
- Running total duration at bottom

**Playlist Metadata Panel** (above the sequence):
- Title (required)
- Description (optional, max 500 chars)
- Subject + Exam Type (required)
- Target Audience (multi-select: School · College · Coaching · All)
- Release Date (optional — schedule a future publish date)

#### Builder Actions

| Action | Behaviour |
|---|---|
| Save Draft | Saves current state; increments version counter; ✅ "Draft saved" toast |
| Publish | Publish guard: ≥ 3 videos required. Confirms publish: "Publish this playlist to {N} institutions?" Publishes and sends ℹ️ notification to Channel Manager (33). **Note:** Publishing a playlist in E-02 makes it available within the EduForge platform (institution-facing). It does NOT automatically create a YouTube playlist on the channel. If Channel Manager (33) wants to replicate this playlist on YouTube, they do so manually via E-03 or E-11 post-publish video assignment. E-02 playlists and YouTube channel playlists are separate systems. |
| Save & Exit | Saves draft and returns to Tab 1 |
| Preview | Opens a read-only preview showing the playlist as students will see it (iframe simulation) |
| Discard Changes | Reverts to last saved state (confirm modal) |

**Auto-save:** HTMX POST every 60s while builder is open. Shows "Last saved: 2 min ago" indicator.

---

### Tab 3 — Coverage Map

**Purpose:** Show which topics in the taxonomy have playlist coverage and which are gaps.

#### Layout

- Subject selector (top): changes the coverage view
- Topic tree (left panel): hierarchical tree of topics and subtopics for the selected subject
- Coverage indicator per topic:
  - 🟢 Covered — at least one published playlist includes a video tagged to this topic
  - 🟡 Draft — a draft playlist covers this topic but nothing published
  - 🔴 Gap — no playlist of any status covers this topic
- Click on a topic node → right panel shows:
  - "Playlists covering this topic: {N}" (list of playlist names, status, link)
  - "Videos in library for this topic: {N}" (link to E-01 filtered)
  - "Create Playlist for this topic" button (pre-fills subject + topic in builder)

#### Coverage Summary Bar

- "Topics covered: {N} / {Total} ({%})"
- Recharts `ProgressBar` per subject

#### Responsive Behaviour

| Breakpoint | Behaviour |
|---|---|
| Desktop (≥1280px) | Topic tree (400px left panel) + details panel (remaining width) side-by-side |
| Tablet (768–1279px) | Topic tree collapses to a scrollable list at top; details panel stacked below |
| Mobile (<768px) | Topic tree rendered as an accordion (expand/collapse per topic); tapping a topic shows details in a full-screen bottom sheet modal |

---

### Tab 4 — Syllabus Alignment

**Purpose:** Check that each exam type's syllabus has playlist coverage across all mandatory topics.

**Data source:** Reads the syllabus structure from D-14 (Syllabus Coverage page) and maps playlist coverage against it.

#### Layout

- Exam Type selector (top)
- Table:

| Column | Notes |
|---|---|
| Topic | From D-14 syllabus for the selected exam type |
| Syllabus Weight | Topic importance % from D-14 |
| Playlist Coverage | Green ✅ / Amber ⚠️ (draft only) / Red ❌ (gap) |
| Video Count | Number of videos across all playlists covering this topic |
| Gap Action | "Create Playlist" button (for ❌ topics) / "View Playlists" (for ✅) |

**Coverage Score:** "Syllabus coverage: {N}/{Total} mandatory topics covered ({%})"

**Export:** "Download Coverage Report (CSV)" — columns: topic, weight, coverage status, playlist count, video count

---

## 6. Data Models

### `content_playlist`
| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `title` | varchar(200) | — |
| `description` | text | Nullable |
| `subject_id` | FK → content_subject | — |
| `exam_type_id` | FK → content_exam_type | — |
| `target_audience` | varchar[] | Enum values: `SCHOOL` · `COLLEGE` · `COACHING` · `ALL` |
| `status` | varchar | Enum: `DRAFT` · `PUBLISHED` · `ARCHIVED` |
| `version` | int | 1-based; increments on each save |
| `release_date` | date | Nullable — for scheduled publish |
| `created_by_id` | FK → auth.User | — |
| `published_at` | timestamptz | Nullable |
| `published_by_id` | FK → auth.User | Nullable |
| `created_at` | timestamptz | — |
| `updated_at` | timestamptz | — |
| `video_count` | int (computed) | Count of `content_playlist_item` where `item_type = VIDEO` for this playlist — ORM annotation on queryset; not a stored column |
| `total_duration_seconds` | int (computed) | Sum of `content_video.duration_seconds` across all VIDEO items — ORM annotation; not stored |
| `coverage_percentage` | decimal (computed) | % of the playlist's subject's taxonomy topics covered by ≥1 VIDEO item in this playlist — computed on-the-fly against D-09 topic count; not stored |

### `content_playlist_item`
| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `playlist_id` | FK → content_playlist | — |
| `item_type` | varchar | Enum: `VIDEO` · `SECTION_HEADER` |
| `video_id` | FK → content_video | Nullable (null for SECTION_HEADER) |
| `section_title` | varchar(100) | Nullable (only for SECTION_HEADER) |
| `position` | int | Ordering within playlist |

### `content_playlist_version`
| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `playlist_id` | FK → content_playlist | — |
| `version_number` | int | — |
| `snapshot` | jsonb | Full playlist state at publish (item list, titles, positions) |
| `published_at` | timestamptz | — |
| `published_by_id` | FK → auth.User | — |
| `notes` | varchar(300) | Nullable |

---

## 7. Access Control

| Gate | Rule |
|---|---|
| Page access | Playlist Manager (32), Video Curator (31), Content Director (18), YouTube Channel Manager (33) |
| Create / Edit / Publish / Archive | Playlist Manager (32) only |
| Add to playlist from builder | Video Curator (31) — read E-01 library only; cannot publish |
| Read-only | Content Director (18), YouTube Channel Manager (33) |
| Publish guard | Enforced server-side: playlist must have ≥ 3 videos to publish |

---

## 8. Edge Cases & Error States

| Scenario | Behaviour |
|---|---|
| Video archived while in a published playlist | Playlist continues to show the video slot; video shows ❌ UNAVAILABLE badge. Playlist Manager notified via in-app notification: "A video in '{playlist title}' is no longer available." |
| Publish guard: fewer than 3 videos | Publish button disabled. Tooltip: "A playlist needs at least 3 videos to publish." |
| Duplicate playlist for same subject+exam type | No hard block. Warning on save: "A published playlist already exists for {Subject} + {Exam Type}. Consider archiving the existing one." |
| Scheduled release date in the past | Warning: "Release date is in the past — playlist will publish immediately on save." |
| Restore old version | Creates a new DRAFT from the version snapshot. Does not overwrite published version. |
| Coverage map for subject with no taxonomy | Shows "No topics defined for this subject in taxonomy (D-09)." |

---

## 9. Integration Points

| Integration | Direction | What Flows |
|---|---|---|
| E-01 Video Library | E-02 reads | Video library is the only source of videos for playlists |
| D-09 Taxonomy | E-02 reads | Subject/Topic tree for coverage map and syllabus alignment |
| D-14 Syllabus Coverage | E-02 reads D-14 | Mandatory topics per exam type for alignment tab |
| E-03 Channel Dashboard | E-02 → E-03 | Published playlists available for channel playlist sync |

---

## 10. UI Patterns & Page-Specific Interactions

### Empty States

| Context | Heading | Subtext | CTA |
|---|---|---|---|
| No playlists | "No playlists yet" | "Build your first structured learning path." | "Create Playlist →" |
| Filter zero | "No playlists match" | "Try a different subject or status." | "Reset Filters" |
| Coverage map — all covered | "Full coverage for {Subject}" | "All topics have at least one published playlist." | — |
| Builder — no videos added | "Add videos to build your playlist" | "Search the library and click + Add." | — |

### Toast Messages

| Action | Toast |
|---|---|
| Draft saved | ✅ "Draft saved" (4s) |
| Playlist published | ✅ "Playlist published to {N} institutions" (4s) |
| Publish guard blocked | ❌ "Need at least 3 videos to publish" (persistent inline) |
| Archived | ✅ "Playlist archived" (4s) |
| Version restored | ✅ "Version {N} restored as new draft" (4s) |

---

*Page spec complete.*
*E-02 covers: browse → create → build → publish → version → coverage check → syllabus alignment.*
