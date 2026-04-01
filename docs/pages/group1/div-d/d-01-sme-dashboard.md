# D-01 — SME Personal Dashboard

> **Route:** `/content/sme/dashboard/`
> **Division:** D — Content & Academics
> **Primary Roles:** SME — Mathematics (19) · SME — Physics (20) · SME — Chemistry (21) · SME — Biology (22) · SME — English (23) · SME — General Knowledge (24) · SME — Reasoning (25) · SME — Computer Science (26) · SME — Regional Language (27)
> **Read Access (own data only):** All 9 SME roles see only questions within their assigned subjects
> **File:** `d-01-sme-dashboard.md`
> **Priority:** P0 — Must be operational before any SME begins authoring
> **Status:** ⬜ Not started
> **Amendments:** G6 (Performance Data tab — Div F exam results) · G11 (Announcements tab + KPI badge — Director broadcasts)

---

## 1. Page Name & Route

**Page Name:** SME Personal Dashboard
**Route:** `/content/sme/dashboard/`
**Part-load routes:**
- `/content/sme/dashboard/?part=kpi` — KPI strip refresh
- `/content/sme/dashboard/?part=my-questions` — My Questions tab table
- `/content/sme/dashboard/?part=returned` — Returned Questions tab
- `/content/sme/dashboard/?part=coverage-gaps` — Coverage Gaps tab
- `/content/sme/dashboard/?part=performance` — Performance Data tab
- `/content/sme/dashboard/?part=announcements` — Announcements tab
- `/content/sme/dashboard/?part=media` — My Media tab
- `/content/sme/dashboard/?part=drawer&question_id={uuid}` — Question detail mini-drawer

---

## 2. Purpose (Business Objective)

Every SME arrives at their dashboard at the start of every working session. This page is the single source of truth for what they have authored, what is stuck, what has been returned and why, where the coverage gaps are, and how their published questions are performing in actual student exams.

The dashboard replaces mental bookkeeping. An SME producing 85–110 questions per working day across multiple exam types and difficulty levels cannot track their pipeline state, reviewer comments, coverage obligations, and performance feedback without a unified workspace. Without this page, productivity collapses — SMEs either over-produce in already-covered topics or miss the coverage gaps that make exams unbalanced.

At platform scale — 2.4M to 7.6M students, 74,000 simultaneous exam submissions — the quality of what an SME authors today directly affects exam integrity weeks from now. The Performance Data tab (G6) closes the feedback loop that makes quality improvement possible: an SME who discovers their "Medium" question was answered correctly by only 28% of students knows immediately that their difficulty calibration is wrong, and can correct it before authoring another 200 questions at the same miscalibrated level.

**Business goals:**
- Give every SME real-time visibility into their authoring pipeline from first draft to published
- Surface returned questions prominently so revision debt never accumulates unnoticed
- Show coverage gaps per topic so SME effort goes where it is most needed
- Close the quality feedback loop: every SME sees post-publish performance data for their own questions
- Deliver Content Director announcements (G11) to the right subject SMEs with acknowledgement tracking

---

## 3. User Roles

| Role | Subject Scope | What They See | Cannot Do |
|---|---|---|---|
| SME — Mathematics (19) | Mathematics only — ORM-enforced via `sme_profile.assigned_subjects` | All own questions + own media + own coverage gaps for Mathematics topics | See other subjects' questions · see other SMEs' question counts · publish · review |
| SME — Physics (20) | Physics only | Same, Physics scope | Same |
| SME — Chemistry (21) | Chemistry only | Same, Chemistry scope | Same |
| SME — Biology (22) | Biology only | Same, Biology scope | Same |
| SME — English (23) | English only | Same, English scope | Same |
| SME — General Knowledge (24) | GK only | Same, GK scope — includes Current Affairs freshness indicators | Same |
| SME — Reasoning (25) | Reasoning only | Same, Reasoning scope | Same |
| SME — Computer Science (26) | CS only | Same, CS scope | Same |
| SME — Regional Language (27) | Telugu / Hindi / Urdu — all three regional language scopes | Same, Regional Language scope | Same |

> **ORM enforcement:** All dashboard queries are filtered by `content_question.subject_id IN sme_profile.assigned_subjects` for the logged-in user. No URL parameter allows subject override. Django `get_queryset()` applies the filter unconditionally — CSS visibility hides nothing that the ORM hasn't already excluded.

---

## 4. Section-Wise Detailed Breakdown

---

### Section 1 — Page Header

**Purpose:** Identify which SME's workspace this is and display session context.

**Header elements:**
- H1: "My Dashboard" — no subject label in the heading (subject is visible in the KPI strip)
- SME name + subject badge (e.g. "Chemistry SME") — pulled from `sme_profile`
- Current quota period label: "March 2026 · 18 working days remaining"
- "New Question" primary action button (green) → navigates to `/content/sme/question/new/`
- "Bulk Import" secondary button → navigates to `/content/import/` (D-07)
- Auto-refresh indicator: "Live · Updated 43s ago" — dims to "Paused" when a drawer is open

---

### Section 2 — KPI Strip

**Purpose:** At-a-glance production health for the current quota month.

**Layout:** Horizontal row of 7 metric tiles, responsive — wraps to 2 rows on smaller screens.

| Tile | Metric | Calculation | Colour Rule |
|---|---|---|---|
| Authored This Month | COUNT of questions created by this SME in current calendar month (all states) | — | Neutral |
| In Review | COUNT in `UNDER_REVIEW` state assigned to Reviewer, authored by this SME | — | Amber if > 0 AND oldest > 3 days |
| Returned | COUNT in `RETURNED` state, authored by this SME | — | Red if > 0; none if 0 |
| Pending Approval | COUNT in `PENDING_APPROVAL` state, authored by this SME | — | Neutral |
| Published (Lifetime) | COUNT of all `PUBLISHED` questions ever authored by this SME | — | Green |
| Quota Achieved | (Published this month / Quota target for month) × 100% | From `content_sme_quota` for current SME + month | Green ≥ 100% · Amber 50–99% · Red < 50% |
| Announcements | COUNT of unread active director announcements targeted at this SME's subject (G11) | `content_director_announcements` where audience includes SME's subject AND read timestamp NULL for this user | Red badge if any "Action Required"; amber badge if any "Warning"; blue if "Info" only |

**KPI refresh:** HTMX `hx-trigger="every 60s"` on `?part=kpi` only. The rest of the page does not auto-refresh unless explicitly on the My Questions tab (which has its own 60s poll).

---

### Section 3 — Tab Navigation

Six tabs rendered as a horizontal tab bar below the KPI strip:

| Tab | Badge | Default |
|---|---|---|
| My Questions | Count of all non-archived questions by this SME | ✅ Default active |
| Returned | COUNT of RETURNED state questions — bold red if > 0 | — |
| Coverage Gaps | Count of topics with < 10 published questions in this SME's subject | — |
| Performance Data | Count of questions with realized vs tagged difficulty divergence > 20% | — |
| Announcements | COUNT of unread announcements (G11) | — |
| My Media | Count of images/diagrams uploaded | — |

Tab state persists in URL fragment (`#returned`, `#coverage-gaps`, etc.) so browser back-button works correctly and shared links open the right tab.

---

### Section 4 — Tab: My Questions (Default)

**Purpose:** Complete view of every question this SME has ever created — current state, pipeline age, actions.

**Table columns:**

| Column | Description |
|---|---|
| # | Sequential display number (not the question UUID) |
| Question (truncated) | First 80 characters of question body — click to open detail drawer |
| Subject / Topic | Topic name from D-09 taxonomy (not raw ID) |
| Difficulty | Easy / Medium / Hard badge |
| Exam Types | Comma-separated list of assigned exam type abbreviations (e.g. SSC CGL · UPSC) |
| Content Type | Evergreen / Current Affairs / Time-Sensitive badge |
| Access Level | Platform-Wide / School / College / Coaching — icon |
| Status | Colour-coded status pill (see Status Definitions below) |
| Days in Pipeline | Days since last status transition. Amber if > 2; red if > 5 — not shown for Published or Draft just created |
| Revision # | How many times this question has been returned and resubmitted. "×1" amber, "×2+" red |
| Actions | Contextual — depends on Status (see Action Rules below) |

**Status Definitions and Colour Coding:**

| Status | Pill Colour | Meaning |
|---|---|---|
| Draft | Grey | Created but not submitted — editable |
| Under Review | Blue | With a Question Reviewer; SME cannot edit |
| Returned | Yellow/Orange | Reviewer sent back with comment — SME must revise |
| Pending Approval | Purple | Reviewer passed to Approver; SME cannot edit |
| Published | Green | Live in question bank |
| Archived | Dim grey | Past `valid_until` date, removed from active pool by nightly Celery task |
| Amendment Review | Amber striped | Previously published, now unpublished for correction; fast-tracked through review |

**Action Rules per Status:**

| Status | Available Actions |
|---|---|
| Draft | Edit (→ D-02) · Delete (confirmation modal — "Delete this draft? This cannot be undone.") |
| Returned | **Revise** (→ D-02 in split-view revision mode — prominent yellow button) · View Comment (inline expand) |
| Under Review | View Only (→ D-02 read-only preview) |
| Pending Approval | View Only |
| Published | View Only · View Performance (→ Performance Data tab filtered to this question) |
| Archived | View Only · "Request Renewal" (opens a pre-filled request to Content Director — not a direct re-publish action) |
| Amendment Review | Revise (→ D-02 in split-view, amendment mode) |

**Filters (persistent — stored in session, not URL):**
- Status: All / Draft / Returned / Under Review / Pending Approval / Published / Archived / Amendment Review
- Exam Type: multi-select
- Difficulty: Easy / Medium / Hard
- Content Type: Evergreen / Current Affairs / Time-Sensitive
- Topic: dropdown from D-09 taxonomy (scoped to SME's subject)
- Revision #: ≥ 1 / ≥ 2 (flag repeated returners)
- Date Range: Authored Between [from] and [to]

**Sort:** Default — Status (Returned first, then Under Review, then Draft, then others) then Days in Pipeline descending. User can re-sort any column.

**Pagination:** 50 rows per page. "Load more" button (HTMX append, not page reload).

**HTMX auto-refresh:** `hx-trigger="every 60s"` on `?part=my-questions` — only when My Questions tab is active. Auto-refresh paused when a drawer is open (checked via JS flag set on drawer open/close).

**Resume Import Banner (My Questions tab — above the question table):**

When the SME has any `content_import_batch` record with `status NOT IN ('SUBMITTED', 'FAILED', 'ABANDONED')`, a persistent yellow banner renders above the question table:

> ⏭ **In-progress import detected** — You have an incomplete import batch from {date} ({N} rows, Step {current_step} of 4). [Resume Import →]

- "Resume Import →" links to `/content/import/?resume={batch_id}` — D-07 wizard reopens at the last completed step with all row data and decisions restored.
- Only the most recent in-progress batch is shown (one banner max).
- Dismissed automatically when batch reaches `SUBMITTED` or `ABANDONED` (next HTMX 60s refresh removes it).
- If no in-progress batch: banner absent entirely.

**SME Out-of-Office Status Banner (My Questions tab — above Resume Import banner if both apply):**

When the SME has an active `content_sme_oof` record (`oof_from ≤ today ≤ oof_until`), a blue informational banner shows:

> 🔵 **You are currently marked as Out of Office** (until {oof_until date}). Your Director has been notified. Your pending questions remain in your queue.
> [Update OOO →] (link to D-19 SME OOO section) · [Clear OOO] (sets `oof_until = yesterday`, removes active flag)

- This banner is visible only to the SME themselves — Directors do not see this banner (they see OOO status in D-05 and D-10).

---

### Section 5 — Tab: Returned Questions

**Purpose:** Dedicated high-attention workspace for the most urgent SME task — addressing reviewer feedback before revision debt accumulates.

**Entry:** If Returned tab count > 0 at page load, a full-width amber banner shows: "You have {N} questions awaiting revision. Addressing returned questions takes priority over new authoring to keep the pipeline healthy."

**OOO note (shown per returned question row when SME is on active OOO):**
When the SME has an active `content_sme_oof` record, each returned question row in this tab shows a small blue note below the reviewer comment: "You are OOO — this question is awaiting your return. Your Director has been notified." This note is informational — the SME can still open and revise returned questions during OOO if they choose.

**Table structure:** Same columns as My Questions tab, filtered to `RETURNED` state only, with additional columns:

| Extra Column | Description |
|---|---|
| Reviewer Comment (inline) | Full reviewer comment text shown directly in the table row (not in a drawer) — avoids the click-to-read friction when the SME needs to process multiple returns quickly |
| Return Reason Category | Badge: Factual Error · Calculation Error · Language/Grammar · Formatting · Incomplete Explanation · Duplicate · Off-Syllabus · Image Quality · Script Error |
| Return Count | How many times this specific question has been returned total. 2nd return: amber. 3rd+ return: red with tooltip "Repeated returner — review carefully before resubmitting" |
| Last Reviewer | Reviewer's first name (not full name — DPDPA) + role — "Priya R." |
| Returned On | Date + time the question was returned |

**Sort:** Default — Return Count descending (most-returned questions first — these represent the biggest quality debt), then Returned On ascending (oldest returns first).

**Batch action (if multiple returned questions share the same return reason category):**
- Multi-select checkboxes — "View Selected (N) together" — opens a side-by-side comparison mode showing up to 4 returned questions simultaneously so SME can identify a systemic error (e.g. all returned for "Incomplete Explanation" in the same topic — SME revises all at once with the same correction pattern).

**Quick Edit button:** Each row has a "Revise Now" button that opens D-02 in split-view revision mode directly, without navigating away from the dashboard. The split-view drawer renders within the current page (full-width overlay), showing the previous submitted version on the left and the editable version on the right, with the reviewer comment prominently displayed at the top.

---

### Section 6 — Tab: Coverage Gaps

**Purpose:** Show the SME where their subject's question bank is thin, so effort goes to underserved topics rather than over-producing in already-covered areas.

**Data source:** `content_taxonomy_topic` and `content_taxonomy_subtopic` joined with COUNT of published questions, filtered to this SME's assigned subject. Read-only — this is the SME's window into D-14 data for their own subject.

**View: Topic Coverage Tree**

Collapsible 3-level tree matching D-09 taxonomy structure — Subject → Topics → Subtopics.

Per topic/subtopic node:
- Published question count badge
- Coverage status indicator:
  - 🔴 Critical: < 3 published questions
  - 🟠 Low: 3–9 published questions
  - 🟡 Developing: 10–29 published questions
  - 🟢 Adequate: ≥ 30 published questions (target varies by exam type — general guideline)
- In-Pipeline count (questions in UNDER_REVIEW or PENDING_APPROVAL for this topic, shown in parentheses as "+4 in pipeline" — so SME knows coverage is improving even before publish)
- "Create Question for This Topic" quick action button — navigates to D-02 with Subject + Topic + Subtopic pre-populated in the tagging panel

**Sort / Filter:**
- "Show critical only" toggle — hides Adequate and Developing nodes; shows only Critical + Low in a flat list ranked by gap severity
- Exam Type filter: shows coverage gaps relative to a selected exam type's syllabus (from D-09 Exam Type Mapping tab data)

**Exam Type Adequacy Bar (top of tab):**
If an exam type filter is selected, shows a summary bar: "SSC CGL Mathematics: 47 of 63 required topics have ≥ 10 questions (74% adequate)" — gives the SME a quick sense of the scope before drilling into the tree.

**GK SME (24) — Additional indicator:**
For Current Affairs topics, the coverage indicator also shows the "Freshness" dimension: count of published questions with `valid_until` > 30 days remaining. A topic may have 50 published GK questions but 40 expiring within 30 days — the Freshness count shows net-fresh coverage.

---

### Section 7 — Tab: Performance Data (Amendment G6)

**Purpose:** Close the quality feedback loop. Every SME who has published questions sees how those questions performed in actual student exams — % correct, answer distribution, realized difficulty vs tagged difficulty, discrimination index.

**Data source:** Div F exam results module. Celery task `portal.tasks.content.sync_question_performance` runs after each exam result publication and populates `content_question_performance` table (question_id, exam_id, correct_%, option_a_%, option_b_%, option_c_%, option_d_%, discrimination_index, student_count, synced_at). Only this SME's published questions are shown.

**Performance Table:**

| Column | Description |
|---|---|
| Question (truncated) | First 60 chars + topic |
| Difficulty Tagged | Easy / Medium / Hard — what SME assigned in D-02 |
| Difficulty Realized | Derived from % correct: ≥ 70% = Easy · 40–69% = Medium · < 40% = Hard |
| % Correct | Percentage of students who answered correctly — bar fill (green if close to expected for tagged difficulty) |
| Answer Distribution | Micro bar chart: A% / B% / C% / D% — a "correct answer concentration" means distractor options are weak |
| Student Count | How many students answered this question across all exams |
| Discrimination Index | Correlation between answering this question correctly and overall exam score. < 0.2 = poor discriminator (question is either too easy for everyone or not testing the right skill) |
| Divergence | Difference between tagged and realized difficulty. Highlighted amber if > 10% gap; red if > 20% gap |
| Last Updated | Date the performance data was last synced from Div F |

**Divergence Alert Banner (top of tab):**
If any of this SME's questions have realized-vs-tagged divergence > 20%: "⚠ {N} of your published questions have difficulty ratings that diverge significantly from how students actually performed. Review these questions to improve tagging accuracy — accurate difficulty tags help the exam engine build balanced papers."

**Per-question action:** "Update Difficulty Tag" — SME can request a difficulty re-tag (sends a pre-filled message to Question Approver via D-13 Difficulty Calibration tab, which has the Approver-side re-tag action). SME cannot re-tag themselves — Approver holds that permission.

**Discrimination Index guidance (tooltip):**
- 0.40+: Excellent discriminator — question reliably separates high-scorers from low-scorers
- 0.20–0.39: Acceptable
- < 0.20: Poor discriminator — consider revising the question or its distractor options

**Filter:** Minimum student count (only show questions answered by ≥ 50 students — small samples produce noisy statistics). Default: 50.

**No Div F data yet state:** If this SME has no questions with exam performance data (brand-new SME, or their questions haven't been used in a graded exam yet): "No performance data yet. This tab will populate after your published questions are used in student exams and results are published." — not an error.

---

### Section 8 — Tab: Announcements (Amendment G11)

**Purpose:** Content Director communications to this SME — syllabus change notifications, quality policy updates, production reminders, urgent content guidance.

**Entry indicator:** If unread Action Required announcements exist, a persistent amber banner at the very top of the page (not just this tab) reads: "📢 You have {N} action-required announcements from Content Director. [View Announcements]" — dismissible per announcement only after the SME clicks "Acknowledged".

**Announcements list (newest first):**

Per announcement card:
- Title (bold)
- Urgency badge: 🔴 Action Required · 🟡 Warning · 🔵 Info
- Body text (full, not truncated — announcements are formal communications)
- Posted by: "Content Director" (role title, not personal name — DPDPA)
- Posted On date · Expires On date (or "No expiry")
- Status: Unread (bold border) / Read / Acknowledged

**Per-card actions:**
- "Acknowledged" button (for Action Required announcements) — records `content_announcement_reads` entry with timestamp. Once acknowledged, amber banner disappears for this announcement. Cannot un-acknowledge.
- "Mark as Read" (for Info/Warning announcements) — records read timestamp. No acknowledgement required.

**Expired announcements:** Shown in a collapsed "Past Announcements" section (default collapsed) — announcements past their expiry date. Kept for reference, not actionable.

**Empty state:** "No active announcements from Content Director. This tab will show syllabus changes, quality guidance, and production updates when posted." — not an error.

---

### Section 9 — Tab: My Media

**Purpose:** Central view of all images and diagrams this SME has uploaded — enables reuse of previously uploaded assets without re-uploading and managing orphaned assets.

**Grid view:** Thumbnail grid, 6 columns. Each thumbnail:
- Image preview (PNG/SVG/JPG)
- File name (truncated)
- Dimensions + file size
- "Used In" count: how many questions reference this image URL
- Upload date

**Per-image actions:**
- "Copy CloudFront URL" — copies the CDN URL to clipboard for embedding in D-02 question body. Button shows "Copied!" for 2s then reverts.
- "Delete" — only available if "Used In = 0" (image not referenced by any question). If "Used In > 0": Delete button is greyed out with tooltip "Referenced by {N} questions — remove from those questions first". Prevents orphaned CloudFront URLs in published question bodies.

**Batch upload:** Drag-and-drop zone for bulk image upload without navigating to D-02. Useful for pre-uploading a batch of diagrams before authoring a set of questions. Files go directly to S3 `content-media/{sme_id}/` with CloudFront invalidation. Max 20 files per batch, 2MB per file.

**Filter:** All / Used / Unused (Unused = Used In count is 0 — helps identify assets safe to delete for storage hygiene).

---

## 5. HTMX Part-Load Routes Detail

| Route | Trigger | Refresh Interval | Notes |
|---|---|---|---|
| `?part=kpi` | Auto + tab switch | 60s | Always active regardless of which tab is open |
| `?part=my-questions` | My Questions tab active | 60s auto | Paused when drawer open |
| `?part=returned` | Returned tab active | No auto-refresh — user-triggered only | Returned questions list changes only when Reviewer acts, not on its own |
| `?part=coverage-gaps` | Coverage Gaps tab active | No auto-refresh | Data changes only when new questions publish or taxonomy changes |
| `?part=performance` | Performance Data tab active | No auto-refresh | Synced only after exam result events |
| `?part=announcements` | Announcements tab active | 5 min | Director may post new announcements during the day |
| `?part=media` | My Media tab active | No auto-refresh | User-triggered only |
| `?part=drawer&question_id={uuid}` | Row click in any question table | No auto-refresh | Loads question metadata for the mini-drawer |

---

## 6. Data Models

### `sme_profile`
| Field | Type | Notes |
|---|---|---|
| `user_id` | FK → auth.User | One-to-one |
| `assigned_subjects` | int[] | Array of subject IDs from `content_taxonomy_subject` |
| `monthly_quota` | int | Overridden per-month by `content_sme_quota` table |

### `content_question` (core question model — relevant fields for dashboard)
| Field | Type | Notes |
|---|---|---|
| `id` | UUID | Primary key |
| `author_id` | FK → auth.User | The SME who created this question |
| `subject_id` | FK → content_taxonomy_subject | Subject scope |
| `topic_id` | FK → content_taxonomy_topic | — |
| `subtopic_id` | FK → content_taxonomy_subtopic | Nullable |
| `difficulty` | varchar | Easy / Medium / Hard |
| `state` | varchar | DRAFT · UNDER_REVIEW · RETURNED · PENDING_APPROVAL · PUBLISHED · ARCHIVED · AMENDMENT_REVIEW |
| `state_changed_at` | timestamptz | Used for Days-in-Pipeline calculation |
| `revision_count` | int | Incremented each time question is returned and resubmitted |
| `content_type` | varchar | Evergreen / CurrentAffairs / TimeSensitive |
| `access_level` | varchar | PlatformWide / SchoolOnly / CollegeOnly / CoachingOnly |
| `valid_until` | date | Nullable — required if not Evergreen |
| `question_set_id` | FK → content_question_set | Nullable — links to passage set (G9) |
| `created_at` | timestamptz | — |

### `content_sme_quota`
| Field | Type | Notes |
|---|---|---|
| `sme_user_id` | FK → auth.User | — |
| `month` | date | First day of month |
| `target_count` | int | Set by Content Director in D-10 |

### `content_question_performance` (populated by Celery after each exam result — Amendment G6)
| Field | Type | Notes |
|---|---|---|
| `question_id` | FK → content_question | — |
| `correct_pct` | decimal | 0.00–100.00 |
| `option_a_pct` | decimal | — |
| `option_b_pct` | decimal | — |
| `option_c_pct` | decimal | — |
| `option_d_pct` | decimal | — |
| `discrimination_index` | decimal | -1.00–1.00 |
| `student_count` | int | Total students who answered this question |
| `synced_at` | timestamptz | Last sync from Div F |

### `content_director_announcements` (Amendment G11)
| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `title` | varchar(200) | — |
| `body` | text | Rich text, stored as HTML |
| `urgency` | varchar | Info / Warning / ActionRequired |
| `target_subjects` | int[] | Null = all Div D; array of subject IDs = subject-specific |
| `created_by` | FK → auth.User | Content Director |
| `created_at` | timestamptz | — |
| `expires_at` | timestamptz | Nullable — if set, announcement auto-hides after this datetime |

### `content_announcement_reads` (Amendment G11)
| Field | Type | Notes |
|---|---|---|
| `announcement_id` | FK → content_director_announcements | — |
| `user_id` | FK → auth.User | — |
| `read_at` | timestamptz | Set on first view |
| `acknowledged_at` | timestamptz | Nullable — set only for ActionRequired announcements |

---

## 7. Access Control

| Gate | Rule |
|---|---|
| Page access | `LoginRequiredMixin` + `PermissionRequiredMixin(permission='content.view_sme_dashboard')` — granted to Roles 19–27 only |
| Subject scope | All ORM queries add `filter(subject_id__in=request.user.sme_profile.assigned_subjects)` via a custom `SubjectScopedQuerySet` mixin — applied at view layer, not template layer |
| Other SME's data | No query returns questions, media, or performance data for other SMEs. No `?sme_id=` parameter exists — the dashboard is always for the authenticated user |
| Content Director read (D-05) | Director's "SME Productivity" view reads from the same `content_question` table with no subject filter — separate view, separate URL, separate permission |
| Performance data | Read-only from `content_question_performance`. SME cannot write to this table — it is populated exclusively by the Celery `sync_question_performance` task running with a separate service account |
| Announcements | SME sees announcements where `target_subjects IS NULL OR request.user.sme_profile.assigned_subjects && target_subjects` (PostgreSQL array overlap operator) |

---

## 8. Edge Cases & Error States

| Scenario | Behaviour |
|---|---|
| SME has no questions yet | My Questions tab shows empty state: "You haven't created any questions yet. Click 'New Question' to begin." — no error |
| SME's quota not set for current month | Quota tile shows "No quota set" in grey — not red — with tooltip "Content Director has not set a quota for this month yet" |
| Returned question's reviewer comment is empty | Should never occur (D-03 enforces ≥ 20 chars or template), but if NULL: shows "No comment provided" in grey italic |
| Question performance data from Div F not yet synced | Performance Data tab shows the published question but all performance columns show "—" with tooltip "Awaiting exam result sync" |
| SME's subject has no taxonomy topics (new subject added) | Coverage Gaps tab shows: "No taxonomy topics found for your subject. Contact Content Director to configure the taxonomy in D-09." |
| Announcement expires while SME is on the page | On next `?part=announcements` poll (5 min), expired announcements disappear without a page reload |
| SME tries to delete an image that has become referenced since the page loaded | Server returns 409 Conflict with message: "This image is now used by {N} questions and cannot be deleted." — page refreshes My Media tab |
| HTMX auto-refresh fires while SME is mid-typing in a filter field | JS event listener on filter inputs pauses `?part=my-questions` auto-refresh if any filter field has focus — resumes on blur |
| `sme_profile` missing (user has Role 19–27 but no profile created) | Django view raises `ObjectDoesNotExist` → handled by custom 500 page with message: "Your SME profile is not configured. Contact Platform Admin." — logged as P2 in C-18 |

---

## 9. Integration Points

| Integration | Direction | What Flows | Mechanism |
|---|---|---|---|
| D-02 Question Editor | D-01 → D-02 | Edit / Revise / New Question navigation | URL navigation with `?next=/content/sme/dashboard/` so D-02 redirects back to dashboard on save |
| D-02 (split-view revision mode) | D-01 → D-02 | "Revise Now" from Returned tab opens D-02 with `?mode=revision&question_id={uuid}` | URL parameter — D-02 reads prior version from `content_question_versions` table |
| D-07 Bulk Import | D-01 → D-07 | "Bulk Import" button navigation | URL navigation |
| D-09 Taxonomy | D-01 reads | Topic/Subtopic names for display | ORM query with Memcached 10-min cache on full taxonomy tree |
| D-10 Calendar & Quota | D-01 reads | Monthly quota target for KPI strip | `content_sme_quota` table — direct ORM read |
| D-14 Syllabus Coverage | D-01 reads | Coverage gap data per topic for this subject | Shared ORM query — D-14 and D-01 both read from `content_taxonomy_topic` published counts |
| Div F Exam Results | Div F → D-01 | Question performance data (% correct, distribution, discrimination index) | Celery `sync_question_performance` task writes to `content_question_performance` after each exam result event |
| D-13 Quality Analytics | D-01 → D-13 | "Update Difficulty Tag" request routes to D-13 Difficulty Calibration tab for Approver | URL navigation: `?pre_filter=question_id:{uuid}` on D-13 |
| D-05 Director Dashboard | D-05 reads D-01 data | Director sees SME-level production metrics drawn from same `content_question` + `content_sme_quota` tables | Same DB tables, different views — no API call |
| Content Director announcements (G11) | D-05 → D-01 | Director posts announcements; SME receives them | `content_director_announcements` + `content_announcement_reads` tables — HTMX polls every 5 min on Announcements part |

---

## 10. Non-Functional Requirements

| Requirement | Target | Notes |
|---|---|---|
| Page initial load | < 800ms P95 | KPI strip + My Questions first 50 rows (status-sorted) + tab structure rendered server-side |
| HTMX partial refresh | < 300ms P95 | `?part=kpi` and `?part=my-questions` are annotated ORM queries — no joins beyond what's indexed |
| Coverage Gaps tab load | < 1.5s P95 | Taxonomy tree with counts requires a multi-level join — Memcached 10-min cache on the annotated taxonomy tree per subject |
| Performance Data tab load | < 600ms P95 | Direct read from `content_question_performance` — indexed on `author_id` and `question_id` |
| Announcements tab | < 200ms P95 | Small table, indexed on `target_subjects` and `expires_at` |
| Concurrent SME sessions | Up to 27 simultaneous SME dashboard sessions (9 roles, some multi-user) | Stateless Django views — no per-session server state |

---

---

## 9. UI Patterns & Page-Specific Interactions

### Search
- **My Questions tab:** Placeholder "Search your questions…". Searches: question body (first 200 chars), topic name, subtopic name. Debounced 300ms.
- **Returned Questions tab:** Placeholder "Search returned questions…". Searches: question body, reviewer comment text.
- **Announcements tab:** Placeholder "Search announcements…". Searches: title and body text.
- **My Media tab:** Placeholder "Search files…". Searches: filename.

### Sortable Columns — My Questions Table
| Column | Default Sort |
|---|---|
| Days in Pipeline | **DESC (oldest first)** — default |
| Submitted Date | DESC |
| Status | Custom order: Returned > Under Review > Pending Approval > Draft > Published |
| Difficulty | ASC |
| Topic | ASC (alphabetical) |
| Revision # | DESC |

### Sortable Columns — Returned Questions Table
Default sort: **Days Returned DESC** (longest-waiting first).

### Pagination
- My Questions: Load More (HTMX append, 50 per load). "Load 50 more (N remaining)".
- Returned Questions: 25 rows, numbered pagination controls.
- Performance Data: 50 rows, numbered pagination controls.
- Announcements: 20 rows, numbered pagination controls.

### Empty States
| Tab | Heading | Subtext | CTA |
|---|---|---|---|
| My Questions | "No questions yet" | "Save your first draft to see it here." | "Create Question" → D-02 |
| Returned Questions | "No returned questions" | "All submitted questions are progressing through review." | — |
| Coverage Gaps | "Full coverage!" | "All topics in your subject meet the minimum question threshold." | — |
| Performance Data | "No performance data yet" | "Data appears after your published questions are used in graded exams." | — |
| Announcements | "No announcements" | "The Content Director hasn't posted any announcements for your subject." | — |
| My Media | "No media uploaded" | "Images you upload in the Question Editor will appear here." | — |

### Toast Messages
| Action | Toast |
|---|---|
| Submit for review | ✅ "Submitted for review" (Success 4s) |
| Save draft | ✅ "Draft saved" (Success 4s) |
| Delete draft | ✅ "Draft deleted" (Success 4s) |
| Acknowledge announcement | ✅ "Acknowledged" (Success 4s) |

### Loading States
- My Questions table: 8-row skeleton on initial load and filter apply.
- KPI strip: individual tile shimmer rectangles.
- Coverage Gaps tree: indented tree skeleton (3 levels).
- Performance Data: 6-row table skeleton.
- Announcements: 3 card-shaped skeletons.

### Responsive Behaviour
| Breakpoint | Table columns shown |
|---|---|
| Desktop (≥1280px) | All columns |
| Tablet (768–1279px) | Question preview, Status, Days in Pipeline, Action — others in row expand |
| Mobile (<768px) | Question preview (truncated), Status, Action button only — tap row to expand detail |

### Charts
- **Coverage Gaps tab:** Horizontal progress bars per topic — Published count (filled green) vs Target (outline). Sorted by gap (most undercovered first).
- **Performance Data tab:** Per-question stacked bar — A/B/C/D option distribution (%), correct option bar highlighted green.

### Role-Based UI
- "Create Question" button: SME roles (19–27) only. Hidden for Content Director (read-only access).
- "Acknowledged" button: SMEs only. Director never sees acknowledgement prompts.
- Performance Data tab: all SME roles. ORM-scoped to own questions only.

---

*Page spec complete.*
*Amendments applied: G6 (Performance Data tab) · G11 (Announcements tab + KPI badge)*
*Gap amendments: Resume Import banner in My Questions tab (cross-reference from D-07 wizard session persistence) · SME OOO self-status banner in My Questions tab · OOO note per returned question row when SME is on active OOO*
*Next file: `d-02-question-editor.md`*
