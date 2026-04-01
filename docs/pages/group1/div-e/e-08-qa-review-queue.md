# E-08 — QA Review Queue

> **Route:** `/content/video/production/qa/`
> **Division:** E — Video & Learning
> **Primary Role:** Video Quality Reviewer (89)
> **Supporting Roles:** Content Producer (82) — read all reviews, override; Content Director (18) — read-only
> **File:** `e-08-qa-review-queue.md`
> **Priority:** P1 — Final quality gate before publish
> **Status:** ⬜ Not started

---

## 1. Page Name & Route

**Page Name:** QA Review Queue
**Route:** `/content/video/production/qa/`
**Part-load routes:**
- `/content/video/production/qa/?part=queue-table` — main queue
- `/content/video/production/qa/?part=review-workspace&id={job_id}` — QA workspace
- `/content/video/production/qa/?part=kpi-strip` — KPI tiles
- `/content/video/production/qa/?part=review-history` — completed reviews table

---

## 2. Purpose

The QA Review Queue is the final quality gate before a video is sent to the Publish Queue (E-11). The Video Quality Reviewer (89) checks:
1. Factual accuracy — does the video correctly explain the concept/MCQ answer?
2. Audio/Video quality — resolution, audio sync, no artefacts
3. Subtitle sync — if subtitles are attached, do they match the audio?
4. Spec compliance — correct format, aspect ratio, duration range

**Business goals:**
- Prevent factually wrong videos from reaching 7.6M students
- Catch A/V quality issues before they are uploaded to YouTube
- Enforce subtitle completeness for accessibility
- Maintain a review audit trail

---

## 3. KPI Strip

Four tiles, `hx-trigger="every 60s"`:

| Tile | Value | Colour Rule |
|---|---|---|
| Queue Length | Jobs in QA_REVIEW state | Amber if > 10; Red if > 20 |
| Reviewed Today | Count reviewed today by this user | — |
| Pass Rate (30d) | % of reviews resulting in PASS | Red if < 70% |
| Avg Review Time | Average minutes per review (30d) | — |

Skeleton: 4 rectangle shimmers.

---

## 4. Tabs

| Tab | Label | Default |
|---|---|---|
| 1 | Review Queue | ✅ Active |
| 2 | Review History | — |

---

## 5. Section-Wise Detailed Breakdown

---

### Tab 1 — Review Queue

#### Search & Filter Bar

- Search: job title, question ID. Debounced 300ms. "×" clear.
- Advanced Filters (collapsible):

| Filter | Control |
|---|---|
| Subject | Multi-select |
| Exam Type | Multi-select |
| Content Type | Multi-select |
| Language | Multi-select: EN · HI · TE · UR |
| Variant Type | Select: All · Primary only · Language variants only |
| Priority | Multi-select: Low · Normal · High · Urgent |
| SLA Status | Multi-select: On Time · Overdue |
| Subtitle Status | Multi-select: Complete · In Progress · Pending · Failed — aligned with E-09 subtitle status naming (replaces legacy "Present/Missing/Partial" labels) |

Active pills + "Reset All".

#### Review Queue Table (Sortable, Selectable, Responsive)

| Column | Sortable | Notes |
|---|---|---|
| Job Title | Yes | Click → opens QA workspace. Language variant jobs show "HI Variant" / "TE Variant" in smaller text below title. Jobs returned from the Publish Queue show a 🔴 **"Returned from Publish"** badge below the title (set when Channel Manager rejects a job from E-11 and it re-enters QA_REVIEW). |
| Language | No | Flag pill: 🇬🇧 EN · 🇮🇳 HI · TE · UR |
| Source | No | 🔗 MCQ (linked) · ✍️ Manual |
| Subject · Topic | No | — |
| Content Type | No | Pill |
| Priority | No | Colour-coded |
| Subtitles | No | ✅ Complete · 🔄 In Progress · ⬜ Pending · ❌ Failed (uses E-09 status values) |
| QA SLA | No | "Day {N} of {total}" — red if overdue |
| Entered QA | Yes | When job moved to QA_REVIEW |
| Actions | No | [Review] |

**Pagination:** 25 rows. Default sort: QA SLA ASC (most urgent first).
**Select:** Checkbox for bulk — only bulk action is "Bulk Assign" (Producer only).
**No bulk review** — each review requires individual inspection.

**Responsive:**
- Desktop: full columns
- Tablet: Job Title · Priority · Subtitle · SLA · Actions
- Mobile: card — title + priority + SLA + [Review]

---

### QA Review Workspace

**Route:** `/content/video/production/qa/{job_id}/review/`

Full-page view (not a drawer). Layout:

**Left Panel (320px) — Job Context**

**Brief section:**
- Job title, content type, subject, topic, exam type
- Production job link → E-05 drawer

**MCQ Seed section** (if MCQ-linked):
- Question body (full)
- Correct answer
- Explanation text
- "Use this to verify the video content is factually correct"
- "View in D-11 →" link

**Script section:**
- Latest approved script body (read-only, scrollable)
- "Compare video against this script for accuracy"

**Subtitle section:**
- Subtitle status (Present / Missing / Partial)
- Languages covered: EN · HI · TE · UR (checkmarks)
- Link to view subtitle file (if present)

> **Subtitle gate before QA entry:** A job only enters `QA_REVIEW` status when mandatory subtitle languages (defined in E-12) are in `COMPLETE` state in `video_subtitle_coverage`. If mandatory subtitles are still `IN_PROGRESS` when the Editor's FINAL_EDIT asset is accepted, the job enters a new intermediate status `AWAITING_SUBTITLE` (not `QA_REVIEW`). The QA queue will NOT show this job. Once all mandatory subtitles become COMPLETE, Celery transitions the job to `QA_REVIEW` and the QA Reviewer is notified.
>
> If a subtitle is `IN_PROGRESS` but the job is somehow in `QA_REVIEW` (edge case, legacy data), the subtitle track in the player shows "Subtitle loading…" with a note: "Subtitle file is still being uploaded. Reload this page to check again."

**Right Panel (full remaining width) — Video Review**

**Returned from Publish Queue banner (shown when applicable):**

If a job was rejected by the Channel Manager (33) from the Publish Queue (E-11) and returned to QA_REVIEW, an amber banner appears at the top of the QA workspace:

> ⚠️ **Returned from Publish Queue** — Channel Manager feedback: "{rejection_reason}". Previous QA decision: PASS (by {role label} on {date}). Review and resubmit.

The previous checklist results are shown as read-only reference below the banner. The QA Reviewer must complete a fresh checklist and resubmit. The `qa_revision_count` is NOT incremented for Publish Queue returns (this counter tracks QA→EDIT revision cycles only).

---

**Video Player:**
- HTML5 `<video>` player, streamed from presigned S3 URL (FINAL_EDIT asset)
- Playback controls: play/pause, seek bar, volume, speed (0.5×, 1×, 1.25×, 1.5×, 2×)
- Full-screen toggle
- If subtitle file attached: subtitle track loaded in video player (`<track kind="subtitles">`)

**Checklist Panel (below video player):**

The QA Reviewer works through a structured checklist. Each item is a row with: description + Pass / Fail radio.

**Section A — Factual Accuracy:**
| # | Item | Options |
|---|---|---|
| A1 | Video answer matches the correct answer (if MCQ-linked) | Pass / Fail |
| A2 | Explanation is accurate and complete | Pass / Fail |
| A3 | No misleading or incorrect content | Pass / Fail |
| A4 | All figures, formulas, and values are correct | Pass / Fail |

**Section B — Audio/Video Quality:**
| # | Item | Options |
|---|---|---|
| B1 | Video resolution is ≥ 1080p | Pass / Fail |
| B2 | Audio is clear, no distortion or clipping | Pass / Fail |
| B3 | Audio and video are in sync throughout | Pass / Fail |
| B4 | No visual artefacts, glitches, or rendering errors | Pass / Fail |
| B5 | Intro and outro are present and correct | Pass / Fail |

**Section C — Subtitles (if present; section hidden if no subtitle attached):**
| # | Item | Options |
|---|---|---|
| C1 | Subtitles appear in sync with audio | Pass / Fail |
| C2 | Subtitle text matches spoken content | Pass / Fail |
| C3 | No spelling errors in subtitles | Pass / Fail |

**Section D — Overall:**
| # | Item | Options |
|---|---|---|
| D1 | Video is complete (no abrupt cutoff) | Pass / Fail |
| D2 | Video duration is appropriate for content type (see spec below) | Pass / Fail |
| D3 | Appropriate for student audience (no inappropriate content) | Pass / Fail |

**Duration spec reference (shown as tooltip on D2):**
- Concept Explainer: 5–20 min
- Problem Walkthrough: 3–15 min
- Revision Quick: 1–5 min
- Shorts: 15s–3 min

**QA Timestamp Notes:**
- Reviewer can add timestamped notes: "[MM:SS] description of issue"
- "+ Add Timestamp Note" button. Stored in `video_qa_review.timestamp_notes` (jsonb array).
- Notes appear as a list below the checklist.

---

**Review Decision Panel:**

| Field | Type | Required |
|---|---|---|
| Overall Decision | Radio | Yes: **PASS** · **REVISION_REQUESTED** · **FAIL** |
| Summary Feedback | Textarea | Required if REVISION_REQUESTED or FAIL. Max 1,000 chars. |
| Accuracy Score | 1–5 star rating | Required |
| A/V Quality Score | 1–5 star rating | Required |
| Subtitle Score | 1–5 star rating | Required (if subtitles present; else N/A) |

**Decision rules:**
- Any Fail on Section A (factual accuracy) → overall decision must be REVISION_REQUESTED or FAIL
- PASS allowed only if: **all of A1+A2+A3+A4 are Pass AND B1+B2+B3 are Pass**
- B4 (no visual artefacts) and B5 (intro/outro present) can be Fail without blocking PASS — these are noted in feedback but do not trigger a mandatory revision. The reviewer should still include them in the Summary Feedback if failed.
- If reviewer tries to PASS with Section A failures: inline error "Factual accuracy failures must be resolved before marking PASS."

**Section C and Subtitle Score interaction rules:**
- If Section C is hidden (no subtitles attached to the job): `subtitle_score` is N/A and not required. Subtitle score has no effect on the PASS/FAIL determination.
- If Section C is visible and all items Pass: any subtitle score (1–5) is acceptable and does not block PASS.
- If Section C has any Fail item AND subtitle score ≤ 3: an inline warning appears below the scores: "⚠️ Subtitle issues found with a score of {N}. Requesting revision is strongly recommended." This is a **non-blocking soft warning** — the reviewer may still choose PASS. If they proceed with PASS despite the warning, Summary Feedback becomes required (inline error if empty: "Summary feedback is required when subtitle issues are present and you are marking PASS.").
- If Section C has any Fail item but subtitle score ≥ 4: no warning. Reviewer's assessment is that despite the checklist item failing, overall subtitle quality is acceptable.

**"Submit Review" button:**
- Disabled until all mandatory checklist items completed + decision selected
- On PASS:
  - `video_qa_review.overall_decision` → PASS
  - `video_production_job.status` → PUBLISH_QUEUE
  - Stage assignment APPROVED
  - Content Producer (82) + YouTube Channel Manager (33) notified: "{job title} passed QA — ready for publish"
  - ✅ "Video passed QA — added to Publish Queue" toast 4s
  - Returns to queue list
- On REVISION_REQUESTED:
  - Status → QA_REVIEW remains; stage assignment → REVISION_REQUESTED
  - `video_production_job.qa_revision_count` incremented (new field — see data model)
  - Producer notified. Video Editor (87) notified (primary revision target).
  - ⚠️ "Revision requested — Editor and Producer notified" warning toast 8s
  - **Max QA revisions check (runs immediately on submit):** If `qa_revision_count >= max_qa_revisions` (from E-12 config, default 2):
    - Job status → ON_HOLD (auto-escalation)
    - QA workspace banner: 🔴 "Max QA revisions reached — this job has been put on hold. Producer must decide next steps."
    - Producer receives persistent notification: "'{title}' has exceeded the maximum QA revision limit ({N} rounds). Job is on hold — review and resume via E-05."
    - ❌ "Max QA revisions reached — job put on hold" error toast persistent
- On FAIL:
  - Status → ON_HOLD (job requires Producer decision on path forward)
  - Producer notified: "QA FAIL for '{title}' — review feedback and determine next steps."
  - ❌ "Video failed QA — job put on hold" error toast persistent

---

### Tab 2 — Review History

List of all completed QA reviews by this reviewer (and all reviews for Producer view).

#### Search & Filter Bar

- Search: job title. Debounced 300ms.
- Filters:

| Filter | Control |
|---|---|
| Decision | Multi-select: Pass · Revision Requested · Fail |
| Subject | Multi-select |
| Date Reviewed | Date range |

#### Review History Table (Sortable, Selectable, Responsive)

| Column | Sortable | Notes |
|---|---|---|
| Job Title | Yes | Click → opens read-only review detail drawer |
| Subject · Topic | No | — |
| Decision | No | ✅ Pass · ⚠️ Revision · ❌ Fail — colour pills |
| Accuracy | No | ⭐⭐⭐⭐⭐ (1–5) |
| A/V Quality | No | ⭐⭐⭐⭐⭐ |
| Reviewed At | Yes | — |
| Actions | No | [View Review] |

**Pagination:** 25 rows.

**Empty state:** "No reviews completed yet. Start reviewing from the Queue tab."

---

## 6. Review Detail Drawer (640px, read-only)

Opens from Review History [View Review].

**Content:**
- Job overview (title, source, subject/topic)
- MCQ link (if applicable)
- QA scores: Accuracy / A/V Quality / Subtitle (star ratings)
- Decision badge
- Summary feedback text
- Checklist items with Pass/Fail status per item
- Timestamp notes list (if any)
- Reviewed by: role label · reviewed at: datetime

**Producer override panel** (Producer only, shown if decision = REVISION_REQUESTED or FAIL):
- "Override QA Decision" button → modal: "Mark as PASS manually? Provide justification."
- Justification required (min 20 chars, max 500 chars — aligned with E-06 Producer override minimum). Logged in `video_qa_review.override_justification`.
- Override changes job status to PUBLISH_QUEUE.

---

## 7. Data Models

### `video_qa_review` (extended from pages-list)
| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `job_id` | FK → video_production_job | — |
| `reviewer_id` | FK → auth.User | — |
| `checklist_results` | jsonb | Array of {item_code, result: 'PASS'/'FAIL'} |
| `timestamp_notes` | jsonb | Array of {timecode: 'MM:SS', note: text} |
| `accuracy_score` | int | 1–5 |
| `av_quality_score` | int | 1–5 |
| `subtitle_score` | int | Nullable (1–5 or null if no subtitles) |
| `overall_decision` | varchar | Enum: `PASS` · `REVISION_REQUESTED` · `FAIL` |
| `feedback_notes` | text | — |
| `override_by_id` | FK → auth.User | Nullable — if Producer overrides |
| `override_justification` | text | Nullable |
| `reviewed_at` | timestamptz | — |

---

## 8. Access Control

| Gate | Rule |
|---|---|
| Page access | Video Quality Reviewer (89), Content Producer (82), Content Director (18) |
| Review Queue view | QA Reviewer (89): own queue; Producer (82): all jobs in QA_REVIEW |
| QA Review Workspace (submit review) | QA Reviewer (89) only |
| Review History | QA Reviewer (89): own history; Producer (82): all history |
| Override QA decision | Content Producer (82) only |
| Read-only drawer | Content Director (18) |

---

## 9. Edge Cases & Error States

| Scenario | Behaviour |
|---|---|
| No FINAL_EDIT asset uploaded (job in QA with no file) | QA workspace shows error state: "No final video file uploaded. The Video Editor must upload the final edit before QA can begin." Producer notified. |
| Video file expired presigned URL (> 15 min open) | Player shows "Video link expired — Refresh page to reload." Refresh regenerates presigned URL. |
| QA Reviewer submits PASS but skips checklist items | Submit button disabled. "Complete all checklist items before submitting." inline validation. |
| Job sent back from QA for revision, Editor re-uploads | New FINAL_EDIT asset version created. Job re-enters QA_REVIEW. QA Reviewer sees "Revision v2 — previous feedback: {text}" at top of workspace. |
| QA Reviewer has 0 reviews this week | Tab 2 empty state. No impact on queue visibility. |
| FAIL — Producer decides to scrap and recreate | Producer cancels job from E-05. Assets retained 30 days. New job created if needed. |
| Channel Manager rejects video from Publish Queue (E-11) after QA PASS | **QA Reviewer is notified:** Div E internal notification — "'{title}' was rejected from the Publish Queue by Channel Manager. Reason: {reason}. Job returned to QA_REVIEW." The QA queue shows a 🔴 "Returned from Publish" badge on this job's row. QA workspace shows a new amber banner: "This video was returned from the Publish Queue — Channel Manager feedback: {reason}. Review and resubmit." |

---

## 10. UI Patterns

### Empty States

| Context | Heading | Subtext |
|---|---|---|
| Queue empty | "QA queue is clear ✓" | "All jobs have been reviewed. Check back after more productions complete editing." |
| History empty | "No reviews yet" | "Completed reviews will appear here." |
| Filter returns zero | "No reviews match" | "Try different subject or decision filters." |

### Toast Messages

| Action | Toast |
|---|---|
| Video passed QA | ✅ "Video passed QA — added to Publish Queue" (4s) |
| Revision requested | ⚠️ "Revision requested — Editor and Producer notified" (8s) |
| Video failed QA | ❌ "Video failed QA — job put on hold" (persistent) |
| QA decision overridden | ✅ "QA decision overridden — video moved to Publish Queue" (4s) |

### Loading States

- Queue table: 8-row shimmer
- KPI strip: 4 tile shimmers
- QA workspace: left panel 3-block shimmer + video player grey 16:9 rectangle + checklist skeleton

### Responsive Behaviour

| Breakpoint | Behaviour |
|---|---|
| Desktop (≥1280px) | Two-panel workspace (320px context + full-width player + checklist) |
| Tablet (768–1279px) | Context panel collapses to accordion; player full-width; checklist below |
| Mobile (<768px) | Video player full-width at top; checklist below; context in collapsed accordion; submit button sticky at bottom |

---

*Page spec complete.*
*E-08 covers: QA queue → structured checklist review → factual accuracy check (MCQ seed) → A/V quality check → subtitle check → PASS/REVISION/FAIL → Producer override → review history.*
