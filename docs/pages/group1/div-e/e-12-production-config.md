# E-12 — Production Config

> **Route:** `/content/video/production/config/`
> **Division:** E — Video & Learning
> **Primary Role:** Content Producer — Video (82) — full control
> **Supporting Roles:** Content Director (18) — read-only; All other Div E roles — no access
> **File:** `e-12-production-config.md`
> **Priority:** P2 — Must be configured before production pipeline starts
> **Status:** ⬜ Not started

---

## 1. Page Name & Route

**Page Name:** Production Config
**Route:** `/content/video/production/config/`
**Part-load routes:**
- `/content/video/production/config/?part=sla-config` — SLA configuration tab
- `/content/video/production/config/?part=content-types` — content type settings tab
- `/content/video/production/config/?part=subtitle-config` — subtitle requirements tab
- `/content/video/production/config/?part=publish-config` — publish settings tab
- `/content/video/production/config/?part=audit-log` — config change log

---

## 2. Purpose

Production Config is the settings page for the Division E video production pipeline. It controls SLA targets per stage, file spec requirements, mandatory subtitle languages, publish settings, and weekly throughput targets. Changes here propagate immediately to all active jobs' SLA calculations and to all E-04/E-10 reference lines in charts.

**Business goals:**
- Give the Content Producer one place to tune the pipeline without engineering involvement
- Ensure SLA targets are realistic and reflected consistently across all pipeline pages
- Enforce subtitle requirements as policy, not as individual judgement

---

## 3. Tabs

| Tab | Label |
|---|---|
| 1 | SLA Targets |
| 2 | Content Type Settings |
| 3 | Subtitle Requirements |
| 4 | Publish Settings |
| 5 | Storage & Retention |
| 6 | Change Log |

---

## 4. Section-Wise Detailed Breakdown

---

### Tab 1 — SLA Targets

#### Overall Job SLA

| Field | Type | Current | Validation |
|---|---|---|---|
| Default job SLA (calendar days) | Number input | 14 | Min 1, max 90 |
| Warning threshold (days before due) | Number input | 2 | Min 1 |
| Critical threshold (days before due) | Number input | 1 | Min 1 |

*Warning threshold:* SLA indicator turns amber when this many days remain.
*Critical threshold:* SLA indicator turns red.

#### Stage SLA Targets Table (Editable inline)

| Stage | Default SLA (days) | Editable | Notes |
|---|---|---|---|
| Script Draft | 3 | Yes | Time for Scriptwriter to draft |
| Script Review | 2 | Yes | Time for Script Reviewer to review |
| Animation | 5 | Yes | Time for Animator to produce animation |
| Graphics | 2 | Yes | Time for Graphics Designer |
| Final Edit | 2 | Yes | Time for Video Editor |
| Subtitle | 1 | Yes | Time for Subtitle Editor |
| QA Review | 1 | Yes | Time for QA Reviewer |

Each row: Stage name · Current SLA (number input, inline editable) · "Revert to default" button per row.

**Validation:** Each stage SLA must be ≥ 1 day. Sum of all stage SLAs must be ≤ default overall job SLA. If not: inline warning "Stage SLA total ({N}d) exceeds overall job SLA ({M}d). Either increase the overall SLA or reduce stage SLAs."

**"Save SLA Config" button:**
- Saves `video_production_config` singleton
- Adds entry to `video_production_config_log`
- ✅ "SLA targets updated. Changes apply to new jobs immediately; existing jobs retain their original SLAs." toast 4s

> **Health check SLA note:** SLA target changes affect stage SLA calculations for new jobs only. They do NOT retroactively update existing jobs' SLA due dates or change the health status of existing videos in E-01. The E-01 nightly health check (Celery Beat, 2:00 AM IST) will apply the updated thresholds starting from the next run after the config change.

#### Quality & Review Config

| Field | Type | Default | Notes |
|---|---|---|---|
| Max script revisions | Number input | 3 | After this many revision cycles in E-06, submit button is disabled and Producer must intervene. Min 1, max 10. |
| Max QA revisions | Number input | 2 | After this many REVISION_REQUESTED cycles in E-08, job is auto-escalated: status → ON_HOLD, Producer notified, QA workspace shows red "Max QA revisions reached — Producer intervention required" banner. Min 1, max 10. |
| Producer asset acceptance SLA (hours) | Number input | 8 | If a UPLOADED asset is not accepted/rejected within this many hours: amber KPI alert in E-07 Tab 3. Red at 2× this value. Min 1, max 72. |

**Save** included in the main "Save SLA Config" button — all SLA tab fields saved together.

#### Weekly Throughput Target

| Field | Type | Notes |
|---|---|---|
| Weekly publish target | Number input | Used as reference line in E-04 and E-10 throughput charts |
| Show target line in charts | Toggle | Default: On |

---

### Tab 2 — Content Type Settings

Manage the content type definitions and their expected duration ranges (used for QA D2 checklist item).

#### Content Type Table (Editable, Selectable)

| Column | Notes |
|---|---|
| Content Type | Concept Explainer · Problem Walkthrough · Revision Quick · Shorts |
| Min Duration (min) | Editable number input |
| Max Duration (min) | Editable number input |
| Default SLA Override | Optional: number of days (overrides Tab 1 SLA for this type) |
| Active | Toggle — disable content types not in use |

**Validation:**
- Min duration must be < Max duration
- Duration values must be positive numbers

> **SLA override propagation:** When a job is created, `video_production_job.sla_due_date` is calculated as: `today + video_content_type.sla_override_days` (if set) OR `today + video_production_config.default_job_sla_days` (fallback). The content type SLA override applies to the **overall job SLA** only. Stage-level SLAs (script, animation, etc.) remain from Tab 1 config regardless of content type. This calculation is applied at job creation time and stored on `sla_due_date` — it does not recalculate if the content type SLA override is later changed in E-12 (existing jobs are unaffected; only new jobs use the updated value). All SLA indicators in E-05, E-08, and E-09 read `sla_due_date` from the job record — no live lookup needed.

**"Add Content Type" — Modal (640px):**

| Field | Type | Required | Validation |
|---|---|---|---|
| Name | Text input | Yes | Max 50 chars; must be unique |
| Description | Text input | No | Max 200 chars |
| Min Duration (min) | Number | Yes | ≥ 0 |
| Max Duration (min) | Number | Yes | > Min Duration |
| SLA Override (days) | Number | No | — |

"Add" → creates new content type option available in all Div E dropdowns.

**"Edit" — Modal:** same form, pre-filled.

**"Deactivate" (not delete):** sets `is_active = False`. Existing jobs with this type are unaffected; type no longer appears in new job forms. Confirm: "Deactivating this content type will hide it from new job creation. Existing jobs are unaffected."

**"Reactivate":** restore `is_active = True`.

**"Save Content Type Changes" button:** Saves all inline edits in batch. ✅ "Content type settings saved" toast 4s.

> **Retroactive application:** Changes to content type SLA override values (`sla_override_days`) apply to **new jobs only**. Existing jobs' `sla_due_date` is calculated at job creation time and stored on the job record — it does NOT recalculate if the content type SLA override is later changed here. Only jobs created after saving this change will use the updated SLA value.

---

### Tab 3 — Subtitle Requirements

Configure which subtitle languages are mandatory before a video can be published.

#### Mandatory Language Toggles

| Language | Toggle | Current |
|---|---|---|
| English (EN) | Toggle (locked ON by default) | Required |
| Hindi (HI) | Toggle | Optional |
| Telugu (TE) | Toggle | Optional |
| Urdu (UR) | Toggle | Optional |

**Note:** EN is locked ON — English subtitles are always required. Platform policy. UI shows "(Required — cannot disable)" in grey next to EN toggle.

**"Block publish if mandatory language missing" toggle:** Default ON. If turned OFF, publish queue will allow publishing without mandatory subtitles (warning only, not block).

**"Save Subtitle Config" button:** Saves. ✅ "Subtitle requirements updated" toast 4s.

---

### Tab 4 — Publish Settings

Configure defaults for the E-11 Publish Queue.

| Setting | Control | Default | Notes |
|---|---|---|---|
| Default YouTube visibility | Select: Public · Unlisted · Private | Unlisted | New jobs default to this visibility; Channel Manager can override |
| Default YouTube category | Select: Education · Science & Technology · How-to & Style | Education | YouTube category ID |
| Require Channel Manager approval | Toggle | ON (locked) | Cannot be disabled. Platform policy: Channel Manager must approve all publishes. |
| Enable multi-audio track publish | Toggle | OFF | Requires YouTube Partner / Content Manager API access. When ON: E-11 shows "Single video with multi-audio tracks" option for multi-language jobs. When OFF: that option is greyed out. |
| Auto-add to default playlist | Searchable dropdown (from E-02) | None | If set, all published videos are automatically added to this playlist |
| Max asset size (MB) | Number | 2048 | Controls E-07 upload validation |
| Asset formats — Voice Over | Tag input | mp3, wav, aac | Accepted file extensions for VOICE_OVER stage |
| Asset formats — Animation | Tag input | mp4, mov | Accepted file extensions for ANIMATION stage |
| Asset formats — Graphics | Tag input | zip, png, ai, psd | — |
| Asset formats — Final Edit | Tag input | mp4 | — |
| Max Voice Over size (MB) | Number | 500 | Controls E-07 upload validation for VOICE_OVER stage |

**"Save Publish Settings" button:** ✅ "Publish settings updated" toast 4s.

---

### Tab 5 — Storage & Retention

**Purpose:** Monitor S3 storage usage by the production pipeline and configure asset retention policies. Prevents runaway storage costs as the pipeline scales to thousands of jobs.

#### Storage Usage Summary (read-only, polled every 10 min)

| Metric | Value |
|---|---|
| Total assets stored | {N} files · {X} GB |
| FINAL_EDIT assets | {N} files · {X} GB (largest category) |
| ANIMATION assets | {N} files · {X} GB |
| GRAPHICS assets | {N} files · {X} GB |
| VOICE_OVER assets | {N} files · {X} GB |
| Subtitle files | {N} files · {X} MB |
| Cancelled job assets (awaiting purge) | {N} files · {X} GB · "Oldest: {N} days" |

Colour: Total storage turns amber at 80% of configured quota, red at 95%.

#### Retention Policy Settings

| Setting | Control | Default | Notes |
|---|---|---|---|
| Cancelled job asset retention (days) | Number input | 30 | After a job is CANCELLED, how long S3 assets are kept before Celery purges them. Min 7, max 365. |
| Rejected asset retention (days) | Number input | 90 | How long REJECTED (non-accepted) asset versions are kept. Min 7, max 365. |
| Superseded subtitle version retention (days) | Number input | 90 | How long old subtitle versions (video_subtitle_version) are kept after being replaced. Min 7, max 180. |
| Keep PUBLISHED job assets indefinitely | Toggle | ON | If OFF: PUBLISHED jobs' S3 assets are eligible for purge after {N} days (configurable). Platform policy default: ON — never delete published assets. |
| Max S3 quota (GB) | Number input | 5120 | Alert threshold only — does not enforce a hard limit. Alerts at 80% and 95%. |

**Storage quota enforcement model:** `max_storage_quota_gb` is a monitoring threshold only — EduForge does not enforce a hard S3 block. If usage exceeds the quota:
- At 80%: amber notification to Producer on E-07 Pending Review tab, E-04 KPI strip, and this page.
- At 95%: red notification; a persistent banner on E-07 Tab 3 and this tab: "S3 storage at {N}% of quota. Free space or increase quota."
- Above 100%: red critical banner everywhere — "Storage quota exceeded. Uploads may fail. Contact Engineering (Div C)."

**Manual cleanup actions available from this tab:**
- ⚠️ "Purge Rejected Assets Now" button — deletes all REJECTED asset versions past their retention date immediately (does not wait for nightly Celery). Confirm modal: "Purge {N} rejected asset files ({X} GB)?"
- ⚠️ "Purge Cancelled Job Assets Now" button — same for cancelled-job assets past retention. Confirm modal.
- Producer cannot delete PUBLISHED or ACCEPTED assets from this UI — those require Div C (Engineering) manual S3 intervention.

**"Save Retention Settings" button:** ✅ "Storage settings saved" toast 4s.

#### Scheduled Purge Log (read-only)

Last 10 purge runs:

| Run At | Files Purged | Space Freed | Trigger |
|---|---|---|---|
| 2026-03-15 02:00 IST | 234 files | 48 GB | Celery Beat nightly |
| … | … | … | … |

Celery Beat task `purge_expired_assets` runs nightly at 2:30 AM IST.

---

### Tab 6 — Change Log

Read-only audit trail of all configuration changes.

#### Search & Filter Bar

- Search: description. Debounced 300ms.
- Filters:

| Filter | Control |
|---|---|
| Tab | Multi-select: SLA · Content Types · Subtitles · Publish · Storage |
| Changed By | My changes / All |
| Date Range | — |

#### Change Log Table (Sortable, Selectable, Responsive)

| Column | Sortable | Notes |
|---|---|---|
| Timestamp | Yes (default: DESC) | — |
| Tab / Setting | No | E.g. "SLA Targets — Animation stage" |
| Change | No | "{Before} → {After}" |
| Changed By | No | Role label (DPDPA) |

**Pagination:** 25 rows per page.
**Export:** "Download Config Log CSV"

---

## 5. Data Models

### `video_production_config` (singleton, extended from pages-list)
*(Full model in div-e-pages-list.md — all fields editable via this page)*

Key fields managed by this page (additions beyond pages-list definition):

| Field | Type | Default | Managed In |
|---|---|---|---|
| `max_script_revisions` | int | 3 | Tab 1 — Quality & Review Config |
| `asset_acceptance_sla_hours` | int | 8 | Tab 1 — Quality & Review Config |
| `voice_over_max_size_mb` | int | 500 | Tab 4 — Publish Settings |
| `voice_over_accepted_formats` | varchar | mp3,wav,aac | Tab 4 — Publish Settings |

### `video_production_config_log`
| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `tab` | varchar | Enum: `SLA` · `CONTENT_TYPES` · `SUBTITLES` · `PUBLISH` · `STORAGE` |
| `setting_key` | varchar | E.g. `animation_stage_sla_days` |
| `old_value` | text | JSON-encoded previous value |
| `new_value` | text | JSON-encoded new value |
| `changed_by_id` | FK → auth.User | — |
| `changed_at` | timestamptz | — |
| `note` | varchar(300) | Optional reason for change |

### `video_content_type`
| Field | Type | Notes |
|---|---|---|
| `id` | int | — |
| `name` | varchar(50) | Unique |
| `description` | varchar(200) | Nullable |
| `min_duration_min` | decimal | — |
| `max_duration_min` | decimal | — |
| `sla_override_days` | int | Nullable |
| `is_active` | boolean | Default True |

---

## 6. Access Control

| Gate | Rule |
|---|---|
| Page access | Content Producer (82), Content Director (18) |
| Edit all settings | Content Producer (82) only |
| Read-only | Content Director (18) |
| Change Log | Both roles |
| "You have read-only access" banner | Content Director (18) |

---

## 7. Edge Cases & Error States

| Scenario | Behaviour |
|---|---|
| Stage SLA sum > overall job SLA | Inline warning (not block): "Total stage SLAs ({N}d) exceed the overall job SLA ({M}d). Jobs will technically be overdue by design." |
| Deactivate content type that's in active use | Block: "Cannot deactivate — {N} active jobs use this content type. Resolve those jobs first." |
| Asset format list cleared (empty tags) | Validation block: "At least one accepted format must be defined per stage." |
| Max asset size set to 0 | Validation: "Max asset size must be at least 1 MB." |
| Config saved during active QA review | QA checklist spec (duration ranges for D2) updates immediately. In-progress review sessions reload config on next submit. |
| Two producers edit config simultaneously | Last write wins. Server-side: config save shows "Last saved by {role label} at {time}" on each tab. If another save happened while editing: ⚠️ "Config was updated by another Producer since you opened this page. Review and re-save." |

---

## 8. UI Patterns

### Forms with Validation

All forms follow inline validation:
- Required fields: red border + "Required" message on blur
- Range errors: "Must be between {min} and {max}"
- Duplicate names: "A content type with this name already exists"
- All validation client-side first; server-side re-validates on save

### Toast Messages

| Action | Toast |
|---|---|
| SLA targets saved | ✅ "SLA targets updated" (4s) |
| Content types saved | ✅ "Content type settings saved" (4s) |
| Content type added | ✅ "Content type added" (4s) |
| Content type deactivated | ✅ "Content type deactivated" (4s) |
| Subtitle config saved | ✅ "Subtitle requirements updated" (4s) |
| Publish settings saved | ✅ "Publish settings updated" (4s) |
| Validation error | ❌ Inline per field — no toast |

### Loading States

- Each tab content: skeleton matching form layout (label + input field shimmers)
- Change log table: 8-row shimmer

### Empty States

| Context | Heading | Subtext |
|---|---|---|
| Change log empty | "No configuration changes yet" | "Changes to production settings will appear here." |
| Filter returns zero | "No changes match" | "Try different tab or date filters." |

### Responsive Behaviour

| Breakpoint | Behaviour |
|---|---|
| Desktop (≥1280px) | Two-column form layout where applicable (label left, input right) |
| Tablet (768–1279px) | Single-column form layout |
| Mobile (<768px) | Single-column; config is read-only recommendation on mobile — "Edit on desktop for best experience" info banner |

---

*Page spec complete.*
*E-12 covers: SLA targets per stage → content type management → subtitle requirements → publish defaults → asset file spec → change log.*
