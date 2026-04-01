# E-07 — Asset Upload & Staging

> **Route:** `/content/video/production/assets/`
> **Division:** E — Video & Learning
> **Primary Roles:** Motion Graphics/Animation Artist (85) · Graphics Designer — Video (86) · Video Editor (87)
> **Supporting Roles:** Content Producer (82) — review all assets, accept/reject; Script Reviewer (84) — read script assets; Subtitle Editor (88) — read (uploads via E-09); QA Reviewer (89) — read all; Content Director (18) — read-only
> **File:** `e-07-asset-upload.md`
> **Priority:** P1
> **Status:** ⬜ Not started

---

## 1. Page Name & Route

**Page Name:** Asset Upload & Staging
**Route:** `/content/video/production/assets/`
**Part-load routes:**
- `/content/video/production/assets/?part=asset-table` — asset list
- `/content/video/production/assets/?part=upload-modal&job_id={id}` — upload form
- `/content/video/production/assets/?part=asset-detail&id={asset_id}` — asset detail drawer
- `/content/video/production/assets/?part=my-uploads` — filtered to current user's uploads
- `/content/video/production/assets/job/{job_id}/` — full-page Job Assets view (Tab 4); all production assets for a single job grouped by stage (not a `?part=` partial — full page render)

---

## 2. Purpose

Asset Upload & Staging is where production files are submitted, versioned, and accepted before proceeding to the next pipeline stage. Each production role uploads outputs at their stage: the Animator uploads the animation export, the Graphics Designer uploads thumbnail and graphic packages, the Video Editor uploads the final assembled video.

> **Scope note:** E-07 handles the four production asset stages: VOICE_OVER · ANIMATION · GRAPHICS · FINAL_EDIT. Subtitle files (`.srt`/`.vtt`) are managed exclusively in E-09 (Subtitle Tracking) and do NOT appear anywhere in E-07's upload forms, asset tables, or drawers.

**Business goals:**
- Centralise all production files in one place (S3) with version tracking
- Prevent raw/incomplete assets from reaching QA — the Producer must accept assets before the next stage unlocks
- Maintain a complete audit trail of what was uploaded, when, by whom, and which version was accepted
- Enforce file spec compliance (resolution, format, size limits) at upload time

---

## 3. Tabs

| Tab | Label | Who Sees It | Default |
|---|---|---|---|
| 1 | My Uploads | All production roles (own assets) | ✅ Active for roles 85–87 |
| 2 | All Assets | Producer (82), Director (18) | ✅ Active for Producer |
| 3 | Pending Review | Producer (82) only — assets awaiting accept/reject | — |
| 4 | Job Assets | All production roles assigned to a job — read/download all stages for that job | Active via E-05 "Assets" tab link |

---

## 4. Section-Wise Detailed Breakdown

---

### Tab 1 — My Uploads

#### Search & Filter Bar

- Search: job title, file name. Debounced 300ms. "×" clear.
- Filters (collapsible):

| Filter | Control |
|---|---|
| Stage | My stage only (fixed for non-Producer roles); Animator sees ANIMATION only. **Exceptions:** (1) If a Scriptwriter (83) is assigned as the VOICE_OVER stage uploader (in-house VO flow), their Tab 1 shows VOICE_OVER uploads and the Stage filter includes "VOICE_OVER" as a selectable option. (2) If a Content Producer (82) is assigned as the VOICE_OVER stage uploader (external contractor flow), same applies — Tab 1 shows VOICE_OVER uploads with "VOICE_OVER" in Stage filter. |
| Status | Multi-select: Uploaded · Accepted · Rejected |
| Date Uploaded | Date range |

Active pills + "Reset All".

#### My Uploads Table (Sortable, Selectable, Responsive)

| Column | Sortable | Notes |
|---|---|---|
| Job Title | Yes | Click → opens asset detail drawer |
| Stage | No | ANIMATION · GRAPHICS · FINAL_EDIT |
| File Name | No | — |
| Version | No | v1, v2, … |
| Size | Yes | MB |
| Status | No | Uploaded (grey) · Accepted (green) · Rejected (red) |
| Uploaded At | Yes | Relative time |
| Actions | No | [View] [Download] [Re-upload] (if rejected) |

**Pagination:** 25 rows per page.
**Select:** Checkbox for bulk download (zip).

**Responsive:**
- Desktop: full columns
- Tablet: Job Title · Stage · Status · Actions
- Mobile: card — job title + stage + status badge + [View]

---

### Tab 2 — All Assets (Producer / Director view)

Same table structure as Tab 1 with additional columns:

| Extra Column | Notes |
|---|---|
| Uploaded By | Role label |
| Rejection Reason | Shows if status=Rejected |

**Additional Filters:**

| Filter | Control |
|---|---|
| Stage | Multi-select: VOICE_OVER · ANIMATION · GRAPHICS · FINAL_EDIT |
| Uploaded By Role | Multi-select: Scriptwriter · Animator · Graphics Designer · Video Editor · Producer |
| Job Subject | Multi-select |

**Bulk Actions (Producer only):**
- Bulk Accept — accepts selected UPLOADED assets
- Bulk Reject — opens reason modal, rejects selected

---

### Tab 3 — Pending Review (Producer only)

Pre-filtered: Status = UPLOADED AND not yet reviewed.

Same table layout. Default sort: uploaded_at ASC (oldest first — review oldest first).

**KPI bar at top of tab:**
- "Pending acceptance: {N} assets across {M} jobs"
- "Oldest pending: {N} hours ago" — amber if > acceptance SLA from E-12 (default 8h), red if > 2× SLA
- If any asset is past acceptance SLA: ⚠️ persistent banner on Tab 3: "Assets are overdue for review — production stages are blocked. Review oldest first."

---

## 5. Upload Asset — Modal (640px)

Triggered by "Upload Asset" from:
- E-05 Production Job Tracker → Drawer Tab 3 → "Upload Asset" button
- E-07 Tab 1 → "+ Upload" button (pre-fills job from My Jobs list)
- Production role's own stage card on E-04 dashboard

**Form:**

| Field | Type | Required | Validation |
|---|---|---|---|
| Job | Searchable dropdown | Yes | Only shows jobs where user has an active stage assignment. Read-only if launched from job drawer. |
| Stage | Select | Yes | Pre-filled from user's role (Animator → ANIMATION; Graphics Designer → GRAPHICS; Video Editor → FINAL_EDIT). Read-only for non-Producer. |
| File | File input | Yes | See file spec below |
| Version Note | Text input | No | Max 200 chars. E.g. "Fixed colour grading in chapter 2" |

**File Spec Validation (client-side + server-side):**

| Stage | Accepted Formats | Max Size | Resolution / Spec |
|---|---|---|---|
| VOICE_OVER | `.mp3`, `.wav`, `.aac` | 500 MB | Min 44.1kHz stereo; no background noise guidance |
| ANIMATION | `.mp4`, `.mov` | 2 GB | Min 1080p (1920×1080), 24fps or 30fps |
| GRAPHICS | `.zip` (containing .png/.psd), `.png`, `.ai`, `.psd` | 500 MB | Thumbnail: 1280×720 (**mark one asset as thumbnail — see below**). Lower-thirds: 1920×1080 |
| FINAL_EDIT | `.mp4` | 2 GB | Min 1080p, max 4K (3840×2160), H.264 or H.265 |
| SUBTITLE_FILE | Handled by E-09 (not this page) | — | — |

**GRAPHICS — Zip Upload Flow:**

When a `.zip` file is selected in the upload modal, a server-side extraction preview is triggered after the file is chosen (before the "Upload" button is clicked):

1. **Client-side size check** — must be < 500 MB (blocking, prevents upload)
2. **"Scanning zip…" indicator** — small spinner appears below the file input
3. **Extracted File List** — displayed as a table inside the upload modal below the file input:

| File Name | Detected Type | Dimensions | Size | Flag |
|---|---|---|---|---|
| thumbnail_v2.png | PNG | 1280×720 | 842 KB | ⭐ [Set as Thumbnail] radio |
| lower_third_intro.png | PNG | 1920×1080 | 512 KB | — |
| logo_animation.ai | AI file | — | 2.1 MB | — |
| old_draft.psd | PSD | 3000×1688 | 18 MB | — |
| notes.txt | ❌ Unsupported | — | 4 KB | Will be excluded |

- PNG/JPG files: dimensions detected client-side (FileReader API)
- AI/PSD files: listed but no dimension detection — shown as "—"
- Unsupported files (e.g. `.txt`, `.docx`): shown in red with "Will be excluded" label — they are stripped on server after upload; the upload button is NOT blocked unless ALL files are unsupported. Clicking "Upload" proceeds with only the supported files. A post-upload toast confirms: ✅ "Uploaded {N} files — {Y} unsupported files were automatically excluded." (4s)
- If all files are unsupported: ❌ "Zip contains no valid graphic files. Re-upload with PNG, PSD, or AI files." Upload button disabled.

**GRAPHICS — Thumbnail Flag:**

After the extracted file list renders, the Graphics Designer selects the YouTube thumbnail using the **"Set as Thumbnail" radio button** on the 1280×720 PNG row. If no 1280×720 PNG detected in the zip: ⚠️ "No thumbnail-sized PNG found in zip (required: 1280×720). You can flag a thumbnail later from the Asset Detail Drawer."

Rules:
- Only one asset per job can be the active thumbnail (`is_thumbnail = True`)
- If a thumbnail was already flagged for this job: new selection replaces it (old `is_thumbnail` set to False)
- The selected thumbnail appears in E-11 Publish Package drawer's thumbnail picker
- If no thumbnail is flagged: E-11 shows ⚠️ "No thumbnail selected — YouTube will use auto-generated frame."

**Post-upload: GRAPHICS Asset Detail Drawer**

After upload, the Asset Detail Drawer (Tab 1 — File Info) shows each extracted file in a sub-table:

| File Name | Type | Dimensions | Size | Thumbnail |
|---|---|---|---|---|
| thumbnail_v2.png | PNG | 1280×720 | 842 KB | ⭐ Active thumbnail |
| lower_third_intro.png | PNG | 1920×1080 | 512 KB | [Set as Thumbnail] |

"[Set as Thumbnail]" button per PNG row — allows flagging/changing after upload without re-uploading. Changes `is_thumbnail` on the relevant `video_production_asset` record.

**VOICE_OVER stage — assignee and ownership:**

| Scenario | Stage Assignee | Who Uploads |
|---|---|---|
| In-house VO (Scriptwriter records) | Scriptwriter (83) | Scriptwriter (83) uploads via E-07 |
| External VO contractor | Content Producer (82) | Producer (82) uploads the contractor's file |

The stage assignee is set by the Producer in E-05 Stage Timeline when the SCRIPT stage completes. Default: Scriptwriter (83). Producer can reassign to themselves if using an external contractor.

VOICE_OVER is a **parallel stage with ANIMATION and GRAPHICS** — all three unlock at SCRIPT_APPROVED and are independent of each other. The Video Editor (87) needs VOICE_OVER + ANIMATION + GRAPHICS all ACCEPTED before EDIT stage unlocks.

**Notification:** When VOICE_OVER stage assignee is set and SCRIPT is approved, the assignee receives a Div E internal notification: "Voice Over stage is now open for '{title}' — SLA: {date}." The notified user is the `video_production_stage_assignment.assigned_to_id` for the VOICE_OVER stage — either Scriptwriter (83) for in-house VO or Producer (82) for external contractor VO. If the Producer is the assigned uploader, the notification still goes to the Producer (they are acting as the uploader for that stage).

**Validation errors (inline, per field):**
- File too large: "File exceeds {max} limit for {stage} stage."
- Wrong format: "Only {formats} are accepted for {stage} uploads."
- No active stage assignment for job: "You are not assigned to the {stage} stage for this job."

**Upload progress:**
- Progress bar: "Uploading… {%}" (S3 multipart upload)
- Spinner on "Upload" button while in progress
- On success: ✅ "Asset uploaded — awaiting Producer review" toast 4s
- On failure: ❌ "Upload failed — {error message}. Try again." toast persistent

**"Cancel" button:** Aborts upload and closes modal. Partial uploads are not saved.

---

## 6. Asset Detail Drawer (640px)

Opens on [View] or row click.

### Drawer Header

- File name + stage badge
- Status badge (large): Uploaded / Accepted / Rejected
- Job title (clickable → E-05 job drawer)

### Drawer Tab 1 — File Info

| Field | Value |
|---|---|
| Job | Title + link |
| Stage | ANIMATION / GRAPHICS / FINAL_EDIT |
| File name | — |
| File size | MB |
| Format | File extension |
| Version | v{N} |
| Uploaded by | Role label |
| Uploaded at | Datetime |
| Version note | If provided |
| S3 key | Shown to Producer only |

**Download button:** Generates presigned S3 URL (15-min expiry). Available to: Production roles for their own stage assets + Producer + Director.

**Preview:**
- `.mp4` / `.mov`: HTML5 `<video>` player (streaming from presigned URL, lazy-load)
- `.png` / `.jpg`: `<img>` tag
- `.zip` / `.psd` / `.ai`: No preview — download only. "Preview not available for this file type."
- Subtitle files: text preview

### Drawer Tab 2 — Version History

Table of all versions uploaded for this job's stage:

| Column | Notes |
|---|---|
| Version | v1, v2, … |
| File Name | — |
| Uploaded At | — |
| Uploaded By | Role label |
| Status | Accepted / Rejected / Superseded (older version replaced by newer) |
| Version Note | — |
| Actions | [Download] |

### Drawer Tab 3 — Review (Producer only)

Shown if `asset.status = UPLOADED`.

**Accept:**
- "Accept Asset" button
- Confirm modal: "Accept this asset for {job title} — {stage} stage? The next stage will be unlocked."
- On accept:
  - `video_production_asset.status` → ACCEPTED
  - Stage assignment `status` → APPROVED
  - Next stage assignment `status` → PENDING; assignee notified
  - **Stage-specific unlock notifications:**
    - VOICE_OVER / ANIMATION / GRAPHICS accepted: Celery checks if **all three parallel stages** are now ACCEPTED for this job. **EDIT stage only unlocks when ALL of VOICE_OVER + ANIMATION + GRAPHICS are ACCEPTED** — accepting just one or two of the three does not unlock EDIT. When all three are confirmed: Video Editor (87) notified: "All parallel stages complete for '{title}' — your EDIT stage is now open. SLA: {date}." If accepting one of the three but not all: the uploader sees "✅ {Stage} accepted — waiting for {remaining stages} before EDIT unlocks" toast 4s.
    - FINAL_EDIT accepted: **Subtitle Editor (88) notified** via Div E internal notification: "Final video accepted for '{title}' — your SUBTITLE stage is now open. Use the final video to time your subtitle cues. SLA: {date}." AND QA Reviewer (89) notified: "'{title}' is entering AWAITING_SUBTITLE — QA will open once mandatory subtitles are complete. SLA for QA: {qa_stage_due_date}."
    - ANIMATION accepted (single stage, not triggering EDIT yet): Animator (85) notified of acceptance. No unlock yet — waiting for VOICE_OVER + GRAPHICS.
  - ✅ "Asset accepted — {next stage} unlocked" toast 4s

**Reject:**
- "Reject Asset" button
- Reject modal (640px):

| Field | Type | Required |
|---|---|---|
| Rejection Reason Category | Select | Yes: Quality Below Spec · Wrong Format · Wrong Version · Wrong Content · Incomplete |
| Specific Feedback | Textarea | Yes, max 500 chars |

- On reject:
  - `video_production_asset.status` → REJECTED
  - `video_production_asset.rejection_reason` saved
  - Stage assignment `status` → REVISION_REQUESTED
  - Uploader notified via Div E internal notification: "Asset rejected for {job}: {reason}". The notified role is the `video_production_stage_assignment.assigned_to_id` for the rejected asset's stage, resolved as follows:

| Stage | Notified role |
|---|---|
| VOICE_OVER | Scriptwriter (83) if in-house VO assigned; Producer (82) if Producer uploaded as external VO contractor |
| ANIMATION | Animator (85) |
| GRAPHICS | Graphics Designer (86) |
| FINAL_EDIT | Video Editor (87) |

  - ⚠️ "Asset rejected — {role} notified" warning toast 8s

**If already accepted/rejected:** Tab shows decision history (who, when, reason). No further action available.

---

## 6b. Tab 4 — Job Assets (All Assigned Production Roles)

**Purpose:** Cross-stage asset visibility. Every production role assigned to a job can view and download ALL accepted assets for that job — regardless of stage. This is critical for the Video Editor (87) who needs the ANIMATION file and VOICE_OVER file to assemble the final edit.

**Access:** Any production role (83–89) who has an active or completed stage assignment for the job. Read + download only — no upload, accept/reject from this view.

**Entry points:**
- E-05 Job Tracker → Drawer Tab 3 (Assets) → "View All Job Assets →" link
- E-07 Tab 1 row → [View] → "View All Assets for This Job" button (cross-link)

**URL:** `/content/video/production/assets/job/{job_id}/`

**Layout:** Full-page, grouped by stage.

#### Job Header

- Job title + status badge
- Subject · Topic · Content Type
- "← Back to Job" link → E-05 drawer

#### Assets by Stage (Accordion per stage)

Each stage section (VOICE_OVER · ANIMATION · GRAPHICS · FINAL_EDIT):

**Stage header:** stage name · status badge (PENDING / IN_PROGRESS / ACCEPTED / REJECTED) · "Accepted version: v{N}" if accepted.

**Asset table per stage:**

| Column | Notes |
|---|---|
| File Name | — |
| Version | v1, v2, … (latest first) |
| Status | Accepted (green) · Rejected (red) · Superseded (grey) · Uploaded (amber) |
| Size | MB |
| Uploaded By | Role label |
| Uploaded At | — |
| Actions | [Download] · [Preview] (video/image/audio) |

**[Download]:** Generates presigned S3 URL (15-min expiry). Logged to audit trail.

**For GRAPHICS stage:** Thumbnail-flagged asset shows ⭐ "YouTube Thumbnail" badge.

**"No assets yet" state per stage:** Stage accordion shows "No assets uploaded yet for this stage."

**Script section (read-only):**
Below the asset stages, a collapsed accordion "Script" shows the approved script body. This gives the Animator (85) and Editor (87) the script on the same page as the assets, without navigating to E-06.

#### Role-Specific Visibility Rules

| Role | Can See |
|---|---|
| Animator (85) | VOICE_OVER (needs VO for animation timing) · ANIMATION (own) · GRAPHICS (reference) |
| Graphics Designer (86) | GRAPHICS (own) · ANIMATION (reference for lower-thirds timing) |
| Video Editor (87) | ALL stages — needs Animation + VO + Graphics to assemble |
| Subtitle Editor (88) | FINAL_EDIT (to time subtitle cues) + script |
| QA Reviewer (89) | ALL stages — needs full package for quality check |
| Script Reviewer (84) | ANIMATION + FINAL_EDIT (to verify script was followed) |
| Scriptwriter (83) | ANIMATION + FINAL_EDIT (to learn from feedback) |

**Language variant jobs:** For HI/TE/UR variant jobs, the ANIMATION and GRAPHICS stage accordions show the **parent job's accepted assets** with a "Shared from parent job" label. These are read-only references. Only VOICE_OVER and FINAL_EDIT accordions show the variant job's own uploaded assets. The Video Editor (87) working on a variant job's EDIT stage sees parent ANIMATION + parent GRAPHICS + variant VOICE_OVER all in one view to assemble the variant final edit.

All non-Producer roles: **download only**. Accept/Reject/Upload are not shown.

---

## 7. Re-upload Flow

When an asset is rejected, the uploader sees "Re-upload" button on their Tab 1 row.

"Re-upload" opens the same upload modal but:
- Job and Stage are pre-filled and locked
- Previous rejection reason displayed in amber box: "Rejection reason: {reason text}"
- On upload: creates new `video_production_asset` record at version `N+1`; previous rejected version is retained in history (status = REJECTED)

---

## 8. Access Control

| Gate | Rule |
|---|---|
| Page access | Roles 82–89, Content Director (18) |
| Upload assets | Scriptwriter (83) → VOICE_OVER (in-house VO); Animator (85) → ANIMATION only; Graphics Designer (86) → GRAPHICS only; Video Editor (87) → FINAL_EDIT only; Producer (82) → VOICE_OVER (if assigned as external VO uploader), GRAPHICS (emergency), any stage as override |
| Accept / Reject | Content Producer (82) only |
| Tab 3 (Pending Review) | Content Producer (82) only |
| Download | Roles can download assets for their own stage. Producer + Director can download all. QA Reviewer (89) can download FINAL_EDIT for review. |
| View all assets (Tab 2) | Content Producer (82), Content Director (18) only |
| Tab 4 Job Assets (cross-stage) | All production roles assigned to the specific job (ORM-scoped: `video_production_stage_assignment.job_id + assigned_to_id = request.user.id`) |
| Version history | All roles with page access for their own stage |

---

## 9. Edge Cases & Error States

| Scenario | Behaviour |
|---|---|
| Upload interrupted mid-way (network drop) | Progress bar freezes. "Upload interrupted — check connection and try again." Error persistent. No partial file saved. |
| File format valid but resolution below spec | Server validates after upload to S3. If below spec: auto-reject with reason "Resolution below minimum ({detected} < {required})". File is deleted from S3. |
| Producer accepts v1 then uploader uploads v2 | v2 shows as UPLOADED pending review. v1 marked as SUPERSEDED (was ACCEPTED — producer must review v2 as a revision). |
| All stage assets accepted but no QA assignee | QA stage set to PENDING Unassigned. Producer receives alert in E-04 dashboard. |
| Graphics zip contains unsupported file types | Server extracts and validates zip contents. If unsupported files found: ❌ "Zip contains unsupported file types: {list}. Re-upload with only PNG/PSD/AI files." |
| Asset > 2 GB | Client-side check blocks upload before it starts: "File exceeds the 2 GB limit for this stage." |

---

## 10. UI Patterns

### Empty States

| Context | Heading | Subtext | CTA |
|---|---|---|---|
| My Uploads empty | "No assets uploaded yet" | "Upload your output for active job stages." | "Upload Asset →" |
| Pending Review empty | "No assets pending review" | "All uploaded assets have been reviewed." | — |
| Filter returns zero | "No assets match" | "Try different stage or status filters." | "Reset Filters" |

### Toast Messages

| Action | Toast |
|---|---|
| Asset uploaded | ✅ "Asset uploaded — awaiting Producer review" (4s) |
| Asset accepted | ✅ "Asset accepted — {next stage} unlocked" (4s) |
| Asset rejected | ⚠️ "Asset rejected — {role} notified" (8s) |
| Download initiated | ℹ️ "Download link generated — expires in 15 minutes" (6s) |
| Re-upload complete | ✅ "New version uploaded — awaiting review" (4s) |
| Upload failed | ❌ "Upload failed — {error}" (persistent) |

### Loading States

- Tables: 8-row shimmer (file icon + title + 3 pill placeholders)
- Drawer: header shimmer + 3 field line shimmers + video player skeleton (16:9 grey rectangle)
- Upload progress: progress bar with % indicator (not a shimmer)

### Responsive Behaviour

| Breakpoint | Behaviour |
|---|---|
| Desktop (≥1280px) | Full table, 640px drawer |
| Tablet (768–1279px) | Table: Job Title · Stage · Status · Actions. Drawer: full-width. |
| Mobile (<768px) | Card layout. Drawer: full-screen bottom sheet. Upload modal: full-screen. |

---

*Page spec complete.*
*E-07 covers: upload by stage role → version tracking → Producer accept/reject → re-upload → asset preview → download (presigned S3).*
