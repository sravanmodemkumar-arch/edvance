# E-09 — Subtitle Tracking

> **Route:** `/content/video/production/subtitles/`
> **Division:** E — Video & Learning
> **Primary Role:** Subtitle & Localisation Editor (88)
> **Supporting Roles:** Content Producer (82) — read all, accept/reject; QA Reviewer (89) — read (subtitle files loaded in E-08 player); Content Director (18) — read-only
> **File:** `e-09-subtitle-tracking.md`
> **Priority:** P2
> **Status:** ⬜ Not started

---

## 1. Page Name & Route

**Page Name:** Subtitle Tracking
**Route:** `/content/video/production/subtitles/`
**Part-load routes:**
- `/content/video/production/subtitles/?part=subtitle-table` — main table
- `/content/video/production/subtitles/?part=kpi-strip` — KPI tiles
- `/content/video/production/subtitles/?part=upload-modal&job_id={id}` — subtitle upload form
- `/content/video/production/subtitles/?part=subtitle-detail&id={coverage_id}` — detail drawer

---

## 2. Purpose

Subtitle Tracking manages subtitle creation and QA coverage across all production videos. Subtitles are required for accessibility and regional language delivery. This page tracks which jobs have subtitles, which languages are covered, and which are outstanding.

**Business goals:**
- Ensure every published video has at least English subtitles (mandatory per E-12 config)
- Track regional language subtitle progress (HI, TE, UR) across the video library
- Give the Subtitle Editor a clear work queue sorted by priority and SLA
- Feed subtitle files to E-08 QA workspace for sync verification

---

## 3. KPI Strip

Four tiles, `hx-trigger="every 60s"`:

| Tile | Value | Colour Rule |
|---|---|---|
| Jobs Awaiting Subtitles | Jobs in AWAITING_SUBTITLE + SUBTITLE_IN_PROGRESS + PENDING | Amber > 10 |
| EN Coverage | % of published videos with EN subtitles | Red < 90% |
| Multilingual Coverage | % of published videos with ≥ 2 language subtitles | — |
| Completed Today | Subtitle files marked COMPLETE by this user today | — |

Skeleton: 4 rectangle shimmers.

---

## 4. Tabs

| Tab | Label | Default |
|---|---|---|
| 1 | Subtitle Queue | ✅ Active |
| 2 | Coverage Overview | — |

---

## 5. Section-Wise Detailed Breakdown

---

### Tab 1 — Subtitle Queue

#### Search & Filter Bar

- Search: job title, question ID. Debounced 300ms. "×" clear.
- Advanced Filters (collapsible):

| Filter | Control |
|---|---|
| Language | Multi-select: EN · HI · TE · UR |
| Status | Multi-select: Pending · In Progress · Complete · QA Failed (these are the canonical subtitle status values — used consistently in E-08 queue filter) |
| Subject | Multi-select |
| Exam Type | Multi-select |
| Priority | Multi-select: Low · Normal · High · Urgent |
| SLA Status | Multi-select: On Time · Overdue |

Active pills + "Reset All".

#### Subtitle Queue Table (Sortable, Selectable, Responsive)

Each row represents one job × one language combination (a job needing EN + HI shows as 2 rows, or the table groups by job with one row per job showing language status columns).

**Layout choice:** One row per job with language status columns (grouped view):

| Column | Sortable | Notes |
|---|---|---|
| Job Title | Yes | Click → opens subtitle detail drawer |
| Subject · Topic | No | — |
| Priority | No | Colour-coded |
| EN | No | ⬜ Pending · 🔵 In Progress · ✅ Complete · ❌ QA Failed |
| HI | No | Same icons |
| TE | No | Same icons |
| UR | No | Same icons |
| Subtitle SLA | No | "Day {N} of {total}" — red if overdue |
| Actions | No | [Upload] [View] |

**Pagination:** 25 rows per page.
**Select:** Checkbox. Bulk action: Bulk Assign (Producer only).

**Responsive:**
- Desktop: full columns with all 4 language status columns
- Tablet: Job Title · EN · HI · SLA · Actions
- Mobile: card — title + language pills (colour-coded) + SLA + [Upload]

---

### Upload Subtitle — Modal (640px)

Triggered by [Upload] button on a row, or "+ Upload Subtitle" button (top-right).

**Form:**

| Field | Type | Required | Validation |
|---|---|---|---|
| Job | Searchable dropdown | Yes | Read-only if launched from a row |
| Language | Select | Yes | EN · HI · TE · UR. Pre-filled if launched from language column. |
| Subtitle File | File input | Yes | Accepts: `.srt`, `.vtt`. Max 5 MB. |
| Notes | Text input | No | Max 200 chars (e.g. "Regional dialect — Hyderabad Telugu") |

**File validation (client + server):**
- Format check: must be `.srt` or `.vtt`
- Size check: must be < 5 MB
- Parse check: server parses file structure. If malformed (bad timestamps, missing cues): ❌ "Subtitle file could not be parsed. Check formatting and re-upload."
- Duplicate check: if a COMPLETE subtitle for same job + language already exists: ⚠️ "A complete {language} subtitle already exists. Uploading will replace it — continue?"

**On upload:**
- Creates/updates `video_subtitle_coverage` record
- Status set to `IN_PROGRESS`
- File stored in S3
- ✅ "Subtitle file uploaded" toast 4s
- Producer notified if this was the last outstanding language for the job: "All subtitles complete for '{title}' — ready for QA."

**AWAITING_SUBTITLE notification:** When a job enters `AWAITING_SUBTITLE` status (final edit asset accepted, but mandatory subtitles are not yet COMPLETE), the Subtitle Editor (88) assigned to this job receives a Div E internal notification: "Final video ready for '{title}' — complete mandatory subtitles ({languages}) to release the job to QA. SLA: {subtitle_stage_due_date}." If no Subtitle Editor is assigned yet, the notification goes to the Producer instead: "'{title}' is awaiting subtitle assignment — assign a Subtitle Editor to continue."

**Subtitle Editor assignment and notification sequence:**

| Stage | Trigger | Recipient | Notification text |
|---|---|---|---|
| FINAL_EDIT accepted → AWAITING_SUBTITLE | Editor's FINAL_EDIT asset accepted in E-07 | Subtitle Editor (88) — if pre-assigned in E-05 Stage Timeline | "Final video ready for '{title}' — complete mandatory subtitles ({languages}) to release the job to QA. SLA: {subtitle_stage_due_date}." |
| AWAITING_SUBTITLE with no Subtitle Editor assigned | Same trigger as above | Producer (82) — fallback | "'{title}' is awaiting subtitle assignment — assign a Subtitle Editor to continue (E-05 → Stage Timeline → SUBTITLE stage)." |
| Producer assigns Subtitle Editor after job is already AWAITING_SUBTITLE | Stage assignment created from E-05 | Subtitle Editor (88) — newly assigned | Same as row 1 above (sent at assignment time, not at AWAITING_SUBTITLE entry). |
| Subtitle Editor reassigned mid-work (subtitle IN_PROGRESS) | Producer reassigns SUBTITLE stage from E-05 | New Subtitle Editor (88) | "You have been assigned the subtitle work for '{title}'. Existing IN_PROGRESS files are available — continue or replace as needed. SLA: {subtitle_stage_due_date}." |
| Subtitle Editor reassigned mid-work | Same | Old Subtitle Editor (88) | "'{title}' subtitle assignment has been transferred to another editor. Your uploads are retained." |

**Cancel:** closes modal, no changes.

---

### Subtitle Detail Drawer (640px)

Opens on row click or [View].

**Drawer Tab 1 — Status Overview**

- Job title + link → E-05
- Content type, subject, topic
- Subtitle SLA due date

**Language Coverage Table:**

| Language | Status | File | Uploaded At | Uploaded By | Actions |
|---|---|---|---|---|---|
| EN | ✅ Complete | subtitle_en_v2.srt | 2 days ago | Subtitle Editor | [Download] [Replace] |
| HI | 🔵 In Progress | subtitle_hi_v1.srt | 5 hours ago | Subtitle Editor | [Download] [Replace] |
| TE | ⬜ Pending | — | — | — | [Upload] |
| UR | ⬜ Pending | — | — | — | [Upload] |

**[Download]:** Generates presigned S3 URL (15-min expiry).
**[Replace]:** Opens upload modal (same form, pre-fills job + language).
**[Upload]:** Opens upload modal for that language.

**"Mark Complete" button** (per language, Subtitle Editor only):
- Changes status from IN_PROGRESS → COMPLETE
- Triggers sync_verified check in E-08 (QA Reviewer will verify sync in video player)

**Prerequisites for "Mark Complete":**
- The job's FINAL_EDIT asset must be in ACCEPTED status in E-07. If not yet accepted, the button is **disabled** with tooltip: "Cannot mark complete until the final video edit is accepted (E-07)."
- If the subtitle file was uploaded early (before FINAL_EDIT was accepted), the button remains disabled until FINAL_EDIT is accepted and the job enters AWAITING_SUBTITLE. Once that condition is met, the button becomes enabled.
- When the **last mandatory subtitle language** is marked COMPLETE: Celery transitions `video_production_job.status` from `AWAITING_SUBTITLE` → `QA_REVIEW`. **QA Reviewer (89) is notified** via Div E internal notification: "'{title}' has all mandatory subtitles complete — the video is now in your QA queue. SLA: {qa_stage_due_date}."

**Re-upload after COMPLETE:** If the Subtitle Editor uploads a new file for a language that is already COMPLETE (via the [Replace] button), the language status reverts to `IN_PROGRESS`. If this language was mandatory, the job status reverts to `AWAITING_SUBTITLE` (job is removed from QA queue). QA Reviewer (89) receives notification: "Subtitle re-uploaded for '{title}' ({language}) after COMPLETE mark — job returned to AWAITING_SUBTITLE. Re-verify sync once marked complete again." The Subtitle Editor must mark the new version COMPLETE before the job re-enters QA_REVIEW.

**Drawer Tab 2 — Version History**

Table of all subtitle versions uploaded for each language in this job:

| Column | Notes |
|---|---|
| Language | EN · HI · TE · UR |
| Version | v1, v2, … |
| File Name | Original .srt/.vtt filename |
| Uploaded By | Role label (DPDPA — no personal names) |
| Uploaded At | Relative time |
| Notes | Version note if provided |
| QA Result | ✅ Pass · ❌ Fail · ⬜ Pending |
| Actions | [Download] |

Newest version per language at the top. Older versions are retained in S3 for 90 days then purged.

**Version rollback:** There is no one-click restore. To use a previous version, download it from the [Download] button in this table, then use the [Replace] button in Drawer Tab 1 to re-upload it as a new version. The system treats this as a new upload (new version number). The previous COMPLETE status is cleared and the language returns to IN_PROGRESS until the re-uploaded file is marked COMPLETE.

**Drawer Tab 3 — Subtitle Preview**

- Language selector (tabs: EN · HI · TE · UR)
- Selected subtitle file rendered as scrollable text list:
  - Cue index · Timestamp · Text
  - E.g. "42 | 00:04:23,500 → 00:04:26,000 | Newton's second law states F = ma"
- "Download .srt" button

**Drawer Tab 4 — QA Sync Results**

Shows results from E-08 QA review for this job's subtitle check:

| Check | Result | Notes |
|---|---|---|
| C1 — Subtitle sync | Pass / Fail | Subtitles appear in sync with audio |
| C2 — Text match | Pass / Fail | Subtitle text matches spoken content |
| C3 — Spelling | Pass / Fail | No spelling errors in subtitles |

- QA feedback text (if any — entered by QA Reviewer in E-08 checklist)
- Reviewed at: datetime
- Status: `sync_verified` boolean — set by QA Reviewer (89) in E-08

**If QA flagged failures (any check = Fail):**

Amber-tinted failure box:
> ⚠️ **Subtitle QA issues found** — {language} subtitles failed QA on {date}.
> QA feedback: "{feedback text}"
>
> **[Re-upload Corrected File]** button — opens the upload modal with job + language pre-filled and locked. Previous rejection reason displayed in amber box. On upload: status → IN_PROGRESS; QA Reviewer (89) notified via Div E internal notification: "Subtitle re-uploaded for '{title}' ({language}) — re-verify sync in E-08."

> **Race condition note:** If a subtitle file is `IN_PROGRESS` (uploaded but not yet marked COMPLETE by the Subtitle Editor) when the QA Reviewer opens E-08, the player shows "Subtitle loading… — subtitle file is still being uploaded. Reload this page to check again." QA checklist Section C is locked (greyed out) with tooltip: "Subtitles are not yet marked complete. Check again after the Subtitle Editor marks this language complete." The job is in `AWAITING_SUBTITLE` status and does NOT appear in the QA queue until all mandatory subtitle languages reach COMPLETE.

---

### Tab 2 — Coverage Overview

**Purpose:** Dashboard view of subtitle coverage across the entire published video library.

#### Summary Cards (top)

| Card | Value |
|---|---|
| Published videos | Total count |
| EN subtitles | {N} / {Total} ({%}) — colour: green ≥90%, amber 70–89%, red <70% |
| HI subtitles | Same |
| TE subtitles | Same |
| UR subtitles | Same |

#### Coverage by Subject (Bar Chart)

- Recharts `BarChart` — grouped bars per subject
- Bars: EN · HI · TE · UR (4 colour-coded bars per subject cluster)
- Y-axis: count of videos with complete subtitles
- X-axis: subject names
- Toggle: All / Published only
- Click bar → filters table below

#### Coverage Table (Sortable, Responsive)

| Column | Sortable | Notes |
|---|---|---|
| Subject | Yes | — |
| Total Videos | Yes | — |
| EN % | Yes | Progress bar within cell |
| HI % | Yes | — |
| TE % | Yes | — |
| UR % | Yes | — |
| Gap Count | Yes | Videos with no subtitle in any language |
| Actions | No | "View Gaps →" — opens Subtitle Queue filtered to that subject, status=Pending |

**Pagination:** 25 rows per page.

**Export:** "Download Coverage CSV" — subject-level breakdown of subtitle completeness.

---

## 6. Data Models

*(Defined in div-e-pages-list.md — `video_subtitle_coverage`)*

No additional models needed.

---

## 7. Access Control

| Gate | Rule |
|---|---|
| Page access | Subtitle Editor (88), Content Producer (82), QA Reviewer (89), Content Director (18) |
| Upload subtitle files | Subtitle Editor (88) and Content Producer (82) only |
| Mark Complete | Subtitle Editor (88) for own uploads; Producer (82) for any |
| Download subtitle files | All roles with page access |
| Coverage Overview | All roles with page access (read-only) |
| "You have read-only access" banner | QA Reviewer (89), Content Director (18) |

---

## 8. Edge Cases & Error States

| Scenario | Behaviour |
|---|---|
| Malformed .srt file (bad timestamps) | Server-side parse fails. ❌ "Subtitle file could not be parsed — line {N}: {error}. Fix formatting and re-upload." File not saved to S3. |
| Subtitle uploaded but video not yet in FINAL_EDIT stage | Allowed — subtitle can be uploaded early. Warning: "The final video is not yet ready. Subtitle sync cannot be verified until the final edit is uploaded." |
| QA marks subtitle sync as failed | `sync_verified = False`. Status in `video_subtitle_coverage` → QA_FAILED. Subtitle Editor notified. Row in Subtitle Queue shows ❌ QA Failed in language column. |
| EN subtitle marked mandatory but not uploaded before QA | E-08 QA workspace shows warning: "EN subtitle is missing. QA Reviewer should flag C1 as Fail." |
| Replace subtitle for a language that is already COMPLETE | Confirm: "Replacing a completed subtitle will require QA to re-verify sync. Continue?" |
| Two Subtitle Editors try to upload for the same job+language simultaneously | Last write wins. Server-side: check if `IN_PROGRESS` record exists; show warning: "Another upload is in progress for {language}. You may be overwriting work." |

---

## 9. UI Patterns

### Empty States

| Context | Heading | Subtext | CTA |
|---|---|---|---|
| Queue empty | "No subtitles pending" | "All subtitle work is complete or no jobs have reached the subtitle stage." | — |
| Filter returns zero | "No jobs match" | "Try a different language or subject filter." | "Reset Filters" |
| Coverage tab — no published videos | "No published videos yet" | "Coverage data will appear after the first video is published." | — |

### Toast Messages

| Action | Toast |
|---|---|
| Subtitle uploaded | ✅ "Subtitle file uploaded" (4s) |
| All subtitles complete for job | ✅ "All subtitles complete for '{title}' — ready for QA" (4s) |
| Marked complete | ✅ "Subtitle marked complete" (4s) |
| QA sync failed | ❌ "Subtitle sync failed QA — re-upload corrected file" (persistent) |
| Parse error | ❌ "Subtitle file could not be parsed" (persistent) |
| Download link generated | ℹ️ "Download link generated — expires in 15 minutes" (6s) |

### Loading States

- Queue table: 8-row shimmer
- KPI strip: 4 tile shimmers
- Drawer: header + 4 language-row shimmers
- Coverage chart: grey rectangle placeholder matching chart dimensions

### Responsive Behaviour

| Breakpoint | Behaviour |
|---|---|
| Desktop (≥1280px) | Full table with 4 language columns; coverage chart full width |
| Tablet (768–1279px) | Table: Job Title · EN · HI · SLA · Actions; chart stacks vertically |
| Mobile (<768px) | Card with language pill badges; chart replaced by summary cards only |

---

*Page spec complete.*
*E-09 covers: subtitle upload → language coverage tracking → QA sync results → coverage overview by subject → export.*
