# D-04 — Question Approval & Publish

> **Route:** `/content/approve/queue/`
> **Division:** D — Content & Academics
> **Primary Role:** Question Approver (Role 29) — sole MCQ publish authority
> **Read Access:** Content Director (18) — full read; cannot publish
> **File:** `d-04-approval-queue.md`
> **Priority:** P0 — Quality Gate 2 and the only path to MCQ publication on the entire platform
> **Status:** ⬜ Not started
> **Amendments:** G2 (Amendment Review workflow — unpublish + fast-track re-publish) · G4 (Access Level update post-publish) · G5 (Extend Valid Until for Current Affairs) · G7 (Committee Review — Approver receives only after both reviewer passes) · G8 (Emergency Bulk Unpublish — paper leak response < 60s for 500 questions)

---

## 1. Page Name & Route

**Page Name:** Question Approval & Publish
**Route:** `/content/approve/queue/`
**Part-load routes:**
- `/content/approve/queue/?part=kpi` — KPI strip
- `/content/approve/queue/?part=table&tab={tab_name}` — question table
- `/content/approve/queue/?part=drawer&question_id={uuid}` — approval drawer
- `/content/approve/queue/?part=bulk-progress&task_id={celery_id}` — bulk publish progress bar
- `/content/approve/queue/?part=emergency-status&task_id={celery_id}` — emergency bulk unpublish progress

---

## 2. Purpose (Business Objective)

D-04 is the final, absolute, and inviolable gate between a question and the live exam pool. No MCQ ever becomes accessible to the exam engine without the Question Approver (Role 29) explicitly approving and publishing it. This restriction is enforced at the model layer — not the UI layer, not through a middleware check, not through a permission that can be granted to other roles. The `content.publish_question` permission is assigned only to Role 29. No override exists.

This design is not bureaucratic — it reflects the mathematical reality of the platform's scale. At 74,000 simultaneous exam submissions, a single wrong published question does not fail one student. It fails every student sitting an exam that uses that question, across every institution, simultaneously. A 74K-student rank distortion is not recoverable within an exam session. The Approver is the human backstop that no automated system or upstream reviewer can replace.

Three distinct workload categories define the Approver's day:

1. **Standard approval queue** — questions that have passed review and are waiting for publish. The Approver reads the full question, verifies the review trail, and either approves + publishes or sends back to the Reviewer with a reason.
2. **Amendment approval queue** (G2) — questions that were published, then unpublished due to errors, revised by the SME, re-reviewed, and are now awaiting re-publication. These carry 2FA re-prompt regardless of bulk/single mode. There is no shortcut for amendment approvals.
3. **Published question management** — the Approver can modify difficulty tags or access levels on already-published questions without triggering a re-review (logged as Tag Amendment in D-12), extend Valid Until dates for Current Affairs (G5), and execute bulk unpublish for paper leaks or errors (G8).

The Approver's decisions are audited at a higher level than any other role. Every publish, unpublish, re-tag, and access level change is recorded with actor + IP + timestamp in D-12 and is immutable.

**Business goals:**
- Ensure every published MCQ has passed independent review + Approver scrutiny
- Enable fast bulk approval of batched content (200 per session) without sacrificing oversight
- Enable emergency bulk unpublish of up to 500 questions in < 60 seconds (G8)
- Enforce 2FA on all amendment re-publishes and destructive actions
- Maintain a clean post-publish management workflow (re-tag, access change, extend expiry, unpublish)

---

## 3. User Roles

| Role | Access | What They Can Do |
|---|---|---|
| Question Approver (29) | Full | Approve + Publish · Bulk Approve + Publish · Send Back to Reviewer · Unpublish · Tag Amendment · Access Level Change · Extend Valid Until · Emergency Bulk Unpublish · Amendment Review approval |
| Content Director (18) | Read | View all tabs and drawers · view review trail · view published bank state. Cannot publish, unpublish, or modify tags. |

> **Permission model:** `content.publish_question` is a Django permission assigned exclusively to Role 29 via `group.permissions`. The publish action view checks `request.user.has_perm('content.publish_question')` and returns 403 on failure — not a redirect to a "you don't have access" page, but a hard 403 that logs the attempt to the security audit log.

---

## 4. Section-Wise Detailed Breakdown

---

### Section 1 — Page Header

- H1: "Approval & Publish Queue"
- Approver's name + "Question Approver" role label
- 2FA session indicator: "2FA verified · Session expires in 28 min" — 2FA re-prompt is required for: Amendment approvals (always) · Unpublish actions · Access Level changes · Emergency Bulk Unpublish. Session expires after 30 minutes of inactivity; re-prompt without needing to log out.
- "Emergency Bulk Unpublish" button (red, prominent, top-right) — available at all times regardless of active tab. See Section 8.
- Auto-refresh indicator: "Live · Updated 41s ago" — pauses when drawer open

---

### Section 2 — KPI Strip

| Tile | Metric | Colour Rule |
|---|---|---|
| Pending Approval | COUNT of `PENDING_APPROVAL` questions | Amber if > 50 · Red if > 150 |
| Amendment Reviews Pending | COUNT of `AMENDMENT_REVIEW` questions awaiting re-approval | Red if > 0 — always needs immediate attention |
| Bulk-Approved Today | COUNT of questions published today (bulk + individual combined) | — |
| Published (All-time) | Total lifetime published question count on the platform | — |
| Unpublished (This Month) | COUNT of questions unpublished this month | Amber if > 5 · Red if > 20 |
| Sent Back to Reviewer (This Month) | COUNT of questions Approver sent back to Reviewer | — |

KPI strip refreshes every 60s via `?part=kpi`.

---

### Section 3 — Tab Navigation

| Tab | Badge | Priority |
|---|---|---|
| Pending Approval | COUNT | Default — standard queue |
| Amendment Reviews | COUNT — bold red if > 0 | Highest priority |
| Published Questions | No count — searchable bank | Post-publish management |
| Sent Back History | No count | Audit of Approver's send-back decisions |

---

### Section 4 — Tab: Pending Approval (Default)

**Purpose:** Standard approval queue — questions passed by Reviewer, awaiting Approver's publish decision.

**Table columns:**

| Column | Description |
|---|---|
| ☐ | Checkbox — for bulk select |
| # | Row number |
| Question Preview | First 100 chars of question body (rendered inline) |
| Subject | Subject badge |
| Topic | Topic name |
| Reviewer | "Reviewer {subject}" — role title, not personal name (DPDPA) |
| Reviewed On | Date the Reviewer passed this question |
| Difficulty | Easy / Medium / Hard |
| Content Type | Evergreen / Current Affairs / Time-Sensitive |
| Access Level | Platform-Wide / School / College / Coaching |
| Exam Types | Comma-separated abbreviations |
| Revision # | ×1, ×2 badges — red if ×2+ |
| Committee | "Committee ✓" badge if this question passed both reviewer passes (G7) |
| Source | — = human · "AI" · "AI-Edited" |

**Per-row actions:**
- "Approve + Publish" (green) — individual publish. See Section 6 (Approval Drawer) for the exact action.
- "Send Back to Reviewer" (orange) — note ≥ 15 characters + reason required. Reason options: Incorrect Answer Key · Factual Error Missed by Reviewer · Formatting Issues · Tags Incorrect · Insufficient Explanation · Other. Question state: `PENDING_APPROVAL` → `UNDER_REVIEW` (back to assigned reviewer's queue, tagged as "Approver Send-Back").
- "Open Detail" — opens approval drawer without triggering any action.

**Filters:**
- Subject (multi-select)
- Difficulty (multi-select)
- Content Type
- Exam Type
- Revision # ≥ 2
- Source: Human / AI / AI-Edited
- Committee Review: Yes / No
- Access Level

**Sort:** Default — Amendment Reviews first (pinned), then oldest Reviewed On first (longest waiting for Approver's decision). User can re-sort any column.

**Pagination:** 50 rows per page. "Load More" (HTMX append).

---

### Section 5 — Bulk Approve + Publish

**Purpose:** Approve and publish up to 200 questions in a single session. Used when a batch of SME output arrives for a seasonal content push (before a major exam period).

**Workflow:**

1. Select rows using checkboxes (individual click or "Select All" for current page — max 200 total)
2. "Bulk Approve + Publish ({N} selected)" button appears in sticky bottom action bar
3. Confirmation modal: "You are about to publish {N} questions. This action cannot be undone without using the unpublish workflow."
   - Type "PUBLISH" to confirm (same confirmation pattern as destructive actions elsewhere in the platform)
   - "Confirm and Publish {N} Questions" button
4. On confirm:
   - Celery async task `portal.tasks.content.bulk_publish_questions` is queued
   - Task ID returned immediately
   - HTMX polls `?part=bulk-progress&task_id={id}` every 2s
   - Live progress bar: "Publishing… 47 / 200 complete"
   - Task publishes questions in batches of 25 to avoid DB lock contention
   - On completion: "✅ 200 questions published successfully" toast + table auto-refreshes
5. If any questions fail (e.g. question state changed between selection and task execution): "17 questions could not be published — they may have been modified. Download failure list." — failures listed as a downloadable CSV.

**Bulk action exclusions:**
- Questions in `AMENDMENT_REVIEW` state are **excluded from bulk action** — amendments always require individual Approver review and mandatory 2FA (see Section 5b)
- Questions with `committee_review_required: true` where committee review is not yet complete are excluded — shown with a lock icon in the checkbox cell

---

### Section 5b — Bulk Approve: Amendment Reviews Exception

Amendment questions can be bulk-approved within the Amendment Reviews tab — but each one still requires the Approver to open the drawer and explicitly acknowledge the amendment context before the 2FA prompt. There is no "Select All + PUBLISH" shortcut for amendments.

The workflow: open drawer → read Amendment Context tab → click "Approve + Re-Publish" → 2FA TOTP prompt → confirm. One at a time. This is intentional — amendment approvals carry audit weight that bulk approval cannot adequately document.

---

### Section 6 — Approval Drawer

**Trigger:** Row click or "Open Detail" in any Pending Approval or Amendment Reviews row. 720px right-side drawer.

**Drawer header:**
- Question ID · Subject · Topic · Difficulty · Access Level · Content Type · Valid Until (if applicable)
- Status pill: "Pending Approval" / "Amendment Review" / "Committee-Reviewed ✓ (2 passes)"
- Revision badge: "×2" in red if applicable

**Drawer tabs:**

**Tab 1: Question Preview (default)**
Full subject-specific rendered view. Same rendering as D-03 — LaTeX, diagrams, code blocks, script rendering. This is what will appear to students after publish.

**Tab 2: Review Trail**
Full chain of custody for this question — shown chronologically:
- Created: [date] by SME {role} in D-02
- Saved as Draft: [date]
- Submitted for Review: [date]
- Assigned to Reviewer: [date]
- [If returned previously]: Returned: [date] · Reason: [category] · Comment: [full text] (this is the key transparency point — Approver sees every reviewer comment ever made on this question)
- Passed by Reviewer: [date] · Reviewer {role title}
- [If committee review]: Passed by Second Reviewer: [date] · Reviewer {role title}
- [If amendment]: Unpublished: [date] · Reason: [category] · Comment: [text]

This trail is the Approver's quality audit. If the trail shows the question was returned 3 times for "Factual Error" and each return comment is vague, the Approver should send it back to the Reviewer with guidance to write a more specific return comment.

**Tab 3: Tags (Approver-editable)**
The Approver can correct two fields without triggering a full re-review cycle — changes are logged as "Tag Amendment" in D-12:

- **Difficulty**: dropdown (Easy / Medium / Hard) — if the Approver judges the tagged difficulty is wrong and can correct it confidently without the question needing SME revision
- **Access Level**: dropdown (Platform-Wide / School Only / College Only / Coaching Only) — if the access level was incorrectly tagged

Both changes are logged with before/after values + Approver actor + timestamp in `content_question_audit_log` with action type "TagAmendment".

These are post-approve corrections, not pre-approve corrections — the Approver makes the correction and then approves + publishes in one step.

**Tab 4: Passage Set Context** *(only visible when question has a `passage_set_id`)*

When the question belongs to a comprehension passage set (G9), this tab gives the Approver the full set context before approving:

- **Passage text:** Full rendered passage (same rendering as D-03 Passage Set Context tab).
- **All questions in the set — approval status table:**

| # | Question Preview | Status | Action |
|---|---|---|---|
| Q1 | Truncated | ✅ PENDING_APPROVAL | Open in drawer |
| Q2 | Truncated | ✅ PENDING_APPROVAL | Open in drawer |
| Q3 | ← This question | 🟡 Currently Open | — |
| Q4 | Truncated | ⬜ UNDER_REVIEW | Waiting for Reviewer |

- **"Approve Entire Set"** button (only enabled when ALL questions in the set are `PENDING_APPROVAL`): approves and publishes all questions in the set in a single action. Uses a database transaction — all questions publish atomically. If any question fails validation during publication, none are published and the error is shown per-question.
- **"View Only This Question"** toggle: when ON, the action bar's "Approve + Publish" button applies only to this question (disabled for passage-set questions unless all others are also at `PENDING_APPROVAL` — see standard passage-set publish guard above).

**Passage Set tab also shows:**
- Completion progress: "3 of 4 questions at Pending Approval — 1 question still in review."
- If any question in the set was returned: "Q2 was returned to SME on {date}. The set cannot be published until all questions are approved."

**Tab 5: Exam Usage (for Amendment Reviews only)**
For questions in `AMENDMENT_REVIEW` state (previously published): which active upcoming exams had used this question before it was unpublished. Shows: Institution name · Exam name · Exam date (upcoming) · Was question used in past completed sessions? This context helps the Approver understand the urgency of re-publishing the corrected version.

**Drawer action bar:**

**"Approve + Publish"** (green, primary):
- For standard pending questions: one-click (no 2FA) — publishes immediately
- For amendment reviews: 2FA TOTP re-prompt first, then publish
- On publish: state → `PUBLISHED` · `published_at` timestamp set · question added to exam engine active pool (via shared content schema read)
- D-12 audit entry: `action: PublishApproved` · `actor: Approver` · IP + timestamp
- For passage set questions (G9): "Approve + Publish" on one question checks if all other questions in the set have `PENDING_APPROVAL`. If yes: "Approve and publish this question as part of Set {set_id}? All {N} questions in the passage set will be published together." If any question in the set is not yet `PENDING_APPROVAL`: "This question is part of a passage set. The other {N−1} questions must also reach approval before any can be published." — the button is disabled for individual questions within incomplete sets.

**Post-Approval — "Create Video Job?" inline prompt** (shown to Content Producer (82) and Content Director (18) only, immediately after successful publish):

An inline callout appears at the bottom of the drawer:

> 📹 **Create explanatory video for this question?**
> {Subject} · {Topic} · {Question short_id}
> [Create Video Job] [Skip]

- **"Create Video Job":** Creates `video_production_job` with `question_id = content_question.id`, `source = MCQ`, taxonomy pre-filled from question tags. Celery task seeds `video_script.seed_text` from question body + correct answer + explanation. ✅ "Production job created" toast 4s. Callout replaced with a "Video job created ✅" badge.
- **"Skip":** Dismisses prompt. No job created. No toast.
- **Not shown to:** Question Approver (29), Reviewers, SMEs — server-side conditional on role.
- **After Bulk Approve + Publish (Section 5):** No per-question prompt. A single post-completion toast: "{N} questions published. [Create video jobs for all →]" — link navigates to E-05 Tab 3 (MCQ Import), pre-filtered to the batch of just-published question IDs.

**"Send Back to Reviewer"** (orange):
- Note ≥ 15 chars required + reason category
- State: `PENDING_APPROVAL` → `UNDER_REVIEW` (re-assigned to the original reviewing Reviewer)
- Logged in D-12 as `action: ApproverSendBack`
- For committee reviews: send-back resets both reviewer passes — question re-enters the standard review queue (not the committee pool directly — committee re-escalation happens at Reviewer's discretion)

---

### Section 7 — Amendment Reviews Tab (Amendment G2)

**Purpose:** Questions previously published, unpublished for errors, revised by SME, re-reviewed, and now awaiting re-publication by the Approver. The Approver is the last human check before a corrected question re-enters the live exam pool.

**Visual differentiation:** Bold amber header bar on the tab and on every question row. "AMENDMENT" badge on each row.

**Additional table columns vs standard pending:**
| Column | Description |
|---|---|
| Original Publish Date | When this question was first published |
| Unpublish Reason | Paper Leak / Factual Error / Copyright / Court Order / Other |
| Flagged By | Student Flags (×N) / Approver / Content Director |
| Time Since Unpublish | Days since the question was removed from the pool |

**Amendment-specific SLA:** 1 day from the point the Reviewer passed the revised question. Shown in the table; red at ≥ 24 hours.

**Drawer for Amendment Reviews:**
Same 4-tab structure as standard approval drawer, plus the amendment context already documented in D-03 Section 7. The Review Trail tab includes the full original publish date, unpublish event, and revision history.

**Mandatory 2FA:** Every amendment approval triggers a 2FA TOTP re-prompt, even if the Approver's session is still within the 30-minute window. There is no bypass. The 2FA prompt modal shows: "Amendment re-publication requires explicit 2FA verification. Enter your 6-digit code:" with the question ID and question preview summary visible above the code input.

---

### Section 8 — Published Questions Tab

**Purpose:** Full searchable view of all published questions with Approver-only post-publish management actions.

**Search:** Full-text on question body + all four options (PostgreSQL `tsvector` GIN index on `content_question_plain_text` column).

**Filters:** Subject · Topic · Subtopic · Difficulty · Exam Type · Published Date range · Bloom's Level · Content Type · Access Level · Expiry Status (All / Expiring ≤ 30 days / Expiring ≤ 90 days / Expired-Archived) · Source (Human/AI/Bulk Import)

**Table columns:**
Question Preview (truncated) · Subject · Topic · Difficulty · Content Type · Access Level · Valid Until · Exam Types · Published Date · Used In Exams count (how many distinct exam papers this question has appeared in)

**Question Preview Drawer** (from Published tab):
- Preview tab: full render
- Tags tab: same Approver-editable Difficulty and Access Level fields
- Version History: link to D-12 for full audit trail
- Exam Usage: which exam papers (institution name + exam date + marks allotted)

**Approver-only actions in Published tab drawer:**

**"Unpublish" (Trigger Amendment G2 workflow):**
- Reason text ≥ 20 chars (mandatory) + reason category (Paper Leak / Factual Error / Copyright / Court Order / Other)
- 2FA re-prompt (always)
- Type "UNPUBLISH" to confirm
- On confirm:
  - State: `PUBLISHED` → `AMENDMENT_REVIEW`
  - Celery high-priority task removes question from exam engine active pool and any upcoming exam paper assignments (< 15s for single question)
  - Original SME notified with reason + context
  - D-12 audit entry: `action: Unpublished` with all context
  - D-16 Feedback Queue (if triggered from student flags): auto-resolves the feedback items linked to this question

**"Difficulty Re-Tag":**
- Update difficulty without triggering re-review or unpublish
- Shows current vs selected new difficulty + D-13 realized difficulty data (if available) for context
- One-click confirm (no 2FA — tag correction is low-risk)
- D-12 audit entry: `action: TagAmendment` · `before: Medium` · `after: Hard`

**"Access Level Change" (Amendment G4):**
- Update access level (Platform-Wide / School / College / Coaching Only) without unpublish
- Shows count of upcoming exams that use this question that would lose access if access is restricted: "Warning: 14 upcoming exams in School-tier institutions currently include this question. Restricting to Coaching Only will remove it from those papers."
- 2FA re-prompt (access restriction has commercial implications)
- D-12 audit entry: `action: AccessAmendment`

**"Extend Valid Until" (Amendment G5):**
- Available only for Current Affairs / Time-Sensitive content type questions
- Date picker for new `valid_until` date — must be after current `valid_until` (cannot shorten — only extend)
- Reason field (optional, 0–200 chars): "Finance Minister extended tenure — question valid until new appointment"
- No 2FA (low-risk extension)
- D-12 audit entry: `action: ValidUntilExtended` · `before: 2026-04-30` · `after: 2026-10-31`

**"Archive Question":**
- Retires a published question from the active exam pool without triggering the Amendment Review workflow. Used for questions that have served their purpose (e.g. Evergreen questions made redundant by curriculum changes, or Time-Sensitive questions past their relevance window) and do not need to be corrected — just retired.
- **Guard check:** If the question is currently assigned to any upcoming (not-yet-completed) exam paper in Div F, archiving is blocked: "Cannot archive — this question is assigned to {N} upcoming exam papers. Remove it from those papers in Div F before archiving."
- If the question has appeared in past (completed) exams: allow archive — historical exam data retains the question for result calculation purposes.
- **Confirmation modal:**
  - "Archive '{Question ID}'? The question will be removed from the active question pool and will not appear in future exam generation. This is not reversible from this page — contact engineering to restore an archived question."
  - Reason field (optional, max 200 chars)
  - No 2FA (archiving is lower risk than unpublish — it does not affect past exam integrity, and archived questions do not enter the amendment workflow)
- **On confirm:**
  - State: `PUBLISHED` → `ARCHIVED`
  - Question removed from exam engine active pool
  - D-12 audit entry: `action: Archived` · `reason` · actor + IP + timestamp
  - Toast: ⚠️ "Question archived — removed from active exam pool" (Warning 8s)
- **Bulk Archive:** In the Published Questions tab table, the Approver can select multiple questions (checkbox) and click "Archive Selected" (max 50 at a time). Same guard check applies per question — if any selected question is assigned to an upcoming exam, the whole batch is blocked with a list of conflicting questions.

---

### Section 9 — Emergency Bulk Unpublish (Amendment G8)

**Purpose:** Paper leak or mass factual error response — remove up to 500 questions from the live exam pool in < 60 seconds.

**Trigger:** "Emergency Bulk Unpublish" button (red, always visible in header). Accessible only to Question Approver (Role 29). Content Director cannot trigger this — they are notified of it.

**Workflow:**

**Step 1 — Select Questions:**
Opens a full-screen modal (not a drawer — the severity warrants full attention). A search panel identical to the Published Questions tab filters allows the Approver to find the affected questions quickly (e.g. filter by Exam Type = SSC CGL + Published Date range if a specific leaked exam paper set is known).

Multi-select checkboxes. Maximum 500 questions. Running count shown: "147 / 500 selected."

**Step 2 — Specify Reason:**
Reason category (radio group — required):
- Paper Leak
- Critical Factual Error
- Court Order
- Copyright Infringement

Detail text field (required, ≥ 30 chars): "SSC CGL 2026 March paper leaked on Telegram — question IDs extracted from leaked screenshots."

**Step 3 — Confirm + 2FA:**
Confirmation field: type "EMERGENCY" (case-sensitive) to unlock.
2FA TOTP re-prompt (always — no session bypass).
"Confirm Emergency Unpublish ({N} questions)" button — red, requires both text confirmation AND 2FA before enabling.

**Step 4 — Execution:**
On confirm:
- Celery high-priority queue: `portal.tasks.content.emergency_bulk_unpublish`
- All N questions: state → `AMENDMENT_REVIEW`
- Questions removed from exam engine active pool and upcoming exam paper assignments via batch UPDATE in the content schema
- Target: < 60 seconds for 500 questions (Celery high-priority queue, batch size 50)
- Live HTMX progress: `?part=emergency-status&task_id={id}` polls every 1s
- Progress bar: "Unpublishing… 247 / 500 complete"

**Step 5 — Notifications (automatic, triggered by Celery task on completion):**
- Content Director: in-app notification + email — "Emergency bulk unpublish completed: 500 questions unpublished at [timestamp] by Approver. Reason: Paper Leak."
- Div F Exam Operations Manager: if any affected question was in an **active live exam session** at the time of unpublish — separate urgent notification: "N questions were removed from active exam sessions. Results for these questions may be affected. Review affected exams in Div F."
- Per-question D-12 audit entry for every unpublished question: `action: EmergencyUnpublished` · `task_id` · actor + IP + timestamp + reason

**Post-emergency state:**
All 500 questions are now in `AMENDMENT_REVIEW` state. They appear in the Amendment Reviews tab awaiting correction and re-approval. The Approver (or another Approver if the primary needs to be debriefed) works through the amendment queue at standard amendment pace.

---

### Section 10 — Sent Back History Tab

**Purpose:** Audit log of questions the Approver sent back to the Reviewer (not unpublished — never published; sent back before approval).

**Table columns:** Question Preview · Subject · Topic · Difficulty · Send-Back Date · Reason Category · Approver Comment (full text) · Outcome (Revised + Eventually Published / Still In Review / Revised + Returned by Reviewer Again)

**Read-only.** No actions — this is an accountability record.

---

## 5. Data Models

### `content_question` — approval-relevant fields
| Field | Type | Notes |
|---|---|---|
| `state` | varchar | PENDING_APPROVAL → PUBLISHED on approve; PENDING_APPROVAL → UNDER_REVIEW on send-back |
| `published_at` | timestamptz | Set on first publish; retained if republished after amendment |
| `published_by` | FK → auth.User | Approver who published — immutable after first publish |
| `republished_at` | timestamptz | Set on re-publication after amendment |
| `republished_by` | FK → auth.User | Approver who approved the amendment re-publish |

### `content_question_audit_log` (INSERT-only — append-only)
| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `question_id` | FK → content_question | — |
| `action` | varchar | PublishApproved · ApproverSendBack · Unpublished · TagAmendment · AccessAmendment · ValidUntilExtended · EmergencyUnpublished · AmendmentApproved |
| `actor_id` | FK → auth.User | — |
| `actor_ip` | inet | IPv4/v6 — stored for DPDPA audit |
| `before_state` | jsonb | Snapshot of changed fields before action |
| `after_state` | jsonb | Snapshot after action |
| `reason_category` | varchar | Nullable — for unpublish/send-back actions |
| `reason_text` | text | Nullable |
| `task_id` | varchar | Nullable — Celery task ID for bulk/emergency operations |
| `created_at` | timestamptz | Immutable |

### `content_bulk_publish_batch`
| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `question_ids` | UUID[] | Array of question UUIDs in batch |
| `initiated_by` | FK → auth.User | Approver |
| `celery_task_id` | varchar | — |
| `total_count` | int | — |
| `success_count` | int | — |
| `failure_count` | int | — |
| `status` | varchar | Pending · In Progress · Completed · PartialFailure |
| `created_at` | timestamptz | — |

### `content_emergency_unpublish_batch`
| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `question_ids` | UUID[] | — |
| `initiated_by` | FK → auth.User | Approver |
| `reason_category` | varchar | — |
| `reason_text` | text | — |
| `celery_task_id` | varchar | — |
| `total_count` | int | — |
| `completed_count` | int | — |
| `status` | varchar | — |
| `duration_seconds` | decimal | Computed at completion — must be < 60 for 500 questions |
| `created_at` | timestamptz | — |

---

## 6. Access Control

| Gate | Rule |
|---|---|
| Page access | `PermissionRequiredMixin(permission='content.approve_questions')` — Role 29 + Content Director (18) |
| Publish action | `request.user.has_perm('content.publish_question')` — only Role 29. Checked in view AND in model's save() override. |
| Content Director | All drawer action buttons hidden at template layer (`{% if request.user.has_perm('content.publish_question') %}`). Director sees the full page layout with read-only data. |
| 2FA requirement | Amendment approvals, unpublish, emergency unpublish, access level change: `request.session['2fa_verified_at']` must be < 30 minutes ago. If expired: 2FA modal shown before action proceeds. |
| Emergency Bulk Unpublish | Role 29 only. Text confirmation "EMERGENCY" checked server-side (client-side check is UX only). 2FA re-prompt mandatory. |
| Audit log | `content_question_audit_log` is INSERT-only. No UPDATE or DELETE route exists in the codebase. |
| Actor IP logging | All Approver actions log `request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])` — stored in `content_question_audit_log.actor_ip`. |

---

## 7. Edge Cases & Error States

| Scenario | Behaviour |
|---|---|
| Two Approvers simultaneously bulk-approve overlapping question sets | Celery task processes questions with `SELECT ... FOR UPDATE SKIP LOCKED` per question. Second task skips already-locked rows; publishes only unprocessed rows. Completion notification shows actual success count (may be less than requested). |
| Question state changes between checkbox selection and bulk-publish execution | Celery task validates each question's state before publish. If state ≠ `PENDING_APPROVAL` at execution time: question skipped; listed in failure CSV. |
| Emergency unpublish takes > 60s for 500 questions | Celery high-priority queue has no other jobs ahead (dedicated queue). If 60s exceeded: `duration_seconds` field is populated with actual duration; alert is logged to C-18 as P2 incident (performance regression). The task completes eventually — the > 60s threshold is a quality SLA, not a timeout. |
| Approver's 2FA session expires mid-workflow | 2FA re-prompt modal appears immediately when next action requiring 2FA is triggered. Unsaved drawer state is preserved in form fields (no data loss). |
| Active live exam session is running when emergency unpublish is triggered | Celery task unpublishes from the active pool. Students currently in-session who have already been served the question (on their exam paper) are NOT affected — their exam paper is a snapshot taken at exam start. Students who have not yet started (or whose exam has not loaded the questions): those future paper generations will not include the unpublished questions. Div F is notified to manually review any ongoing sessions. |
| Passage set question: Approver tries to publish one question when others in the set are not yet at PENDING_APPROVAL | Blocked at the publish action: "This question is part of a passage set. {N} other questions in the set are not yet at approval stage." Approver cannot publish incomplete sets. |
| Approver sends a question back to Reviewer after committee review completed | Both reviewer passes are reset. Question re-enters standard review queue (not committee pool). Reviewer must decide again whether to escalate to committee. |
| Content Director opens the Emergency Unpublish modal | "Emergency Bulk Unpublish" button is visible to Director (for awareness) but clicking it shows: "This action requires Question Approver permissions. Contact the Question Approver immediately." — with the on-call Approver's contact card shown (from D-15 contact config). |

---

## 8. Integration Points

| Integration | Direction | What Flows | Mechanism |
|---|---|---|---|
| D-03 Review Queue | D-03 → D-04 | Questions passed by Reviewer | State change: `UNDER_REVIEW` → `PENDING_APPROVAL` |
| Exam engine (Div F) | D-04 → Div F | Published question becomes active in exam pool | Shared `content_question` table — exam engine reads `state = 'PUBLISHED'` with access level filter |
| D-12 Audit & Version | D-04 → D-12 | Every Approver action logged | INSERT into `content_question_audit_log` |
| D-16 Student Feedback | D-16 → D-04 | Auto-escalated flags (≥ 10) → Approver review prompt | D-16 creates escalation record; Approver sees "Triggered by Student Flags" in amendment context |
| D-11 Published Bank | D-04 publishes → D-11 shows | Published questions appear in D-11 | Same `content_question` table with `state = 'PUBLISHED'` filter |
| Div F Exam Operations | D-04 → Div F | Emergency unpublish notification if active exam affected | Celery task sends in-app notification to Div F Exam Ops Manager after unpublish completion |
| D-05 Director Dashboard | D-05 reads D-04 | Approval queue depth, amendment count, KPI data | Same `content_question` table — no API call |
| D-13 Quality Analytics | D-04 → D-13 | Difficulty Re-Tag actions feed difficulty calibration tab | `content_question_audit_log` with `action: TagAmendment` — D-13 query joins this table |
| Content Director notifications | D-04 → D-05 | Emergency unpublish triggers Director in-app notification | Celery task creates `content_director_notification` record polled by D-05 HTMX |
| **E-05 Production Job Tracker** | D-04 → E-05 | After Approve + Publish: optional "Create Video Job?" prompt for Content Producer / Director. Creates `video_production_job` with `question_id` FK and `source=MCQ`. | Post-approval inline prompt (see Section 6 — Approval Drawer, Video Job prompt); Celery task seeds script. |

---

---

## 9. UI Patterns & Page-Specific Interactions

### Search
- Available on Pending Approval, Published Questions, and Sent Back History tabs.
- Placeholder: "Search questions by topic, subject, or keyword…".
- Searches: question body (first 150 chars), topic name, subject name.
- Debounced 300ms. Results update in place.

### Sortable Columns — Pending Approval Table
| Column | Default Sort |
|---|---|
| Review Date | **ASC (oldest reviewed first)** — default |
| Subject | ASC |
| Difficulty | Custom: Hard → Medium → Easy |
| Revision # | DESC |
| Access Level | ASC |

Amendment Reviews always pinned above regular queue (regardless of sort).

### Sortable Columns — Published Questions Table
| Column | Default Sort |
|---|---|
| Published Date | **DESC (newest first)** — default |
| Subject | ASC |
| Difficulty | — |
| Access Level | — |
| Valid Until | ASC (soonest expiry first) |

### Pagination
All tabs: 50 rows, numbered pagination controls. Published Questions tab default shows last 30 days; "Show All Time" link expands to full bank (same as D-11).

### Row Selection — Bulk Approve
- Checkbox column on Pending Approval tab only.
- Max 200 rows selectable for bulk approve.
- Amendment Review rows: selectable for individual review only — checkbox disabled for Amendment rows, tooltip: "Amendment reviews require individual drawer review."
- "Select All on Page" header checkbox.
- Bulk action bar (sticky bottom): "{N} selected · Approve All Selected → [Confirm]".
- Confirm modal: "You are about to publish {N} questions. Type PUBLISH to confirm." Input field + "Publish" button (disabled until "PUBLISH" typed exactly).

### Empty States
| Tab | Heading | Subtext |
|---|---|---|
| Pending Approval | "Nothing awaiting approval" | "Questions passed by the Review team will appear here." |
| Amendment Reviews | "No amendment reviews" | "Questions unpublished for correction will appear here for fast-track review." |
| Published Questions | "No published questions" | "Questions you approve will appear in the published bank." |
| Sent Back History | "No send-back history" | "Questions you sent back to the Reviewer will appear here." |

### Toast Messages
| Action | Toast |
|---|---|
| Approve + Publish (single) | ✅ "Question published" (Success 4s) |
| Bulk Approve + Publish | ✅ "{N} questions published" (Success 4s) |
| Bulk partial failure | ⚠ "{N} of {total} published. {M} failed — download error list." (Warning persistent) |
| Send Back to Reviewer | ✅ "Sent back to Reviewer with your note" (Success 4s) |
| Unpublish (G2) | ✅ "Question unpublished — fast-track amendment review created" (Success 4s) |
| Difficulty Re-Tag | ✅ "Difficulty updated" (Success 4s) |
| Access Level Change (G4) | ✅ "Access level updated" (Success 4s) |
| Extend Valid Until (G5) | ✅ "Expiry date extended" (Success 4s) |
| Emergency Bulk Unpublish (G8) | ✅ "{N} questions unpublished — Celery task complete" (Success 4s) after job completes |
| 2FA fail | ❌ "Verification failed — check your authenticator code" (Error persistent) |

### Loading States
- Queue table: 8-row skeleton on initial load and filter apply.
- KPI strip: tile shimmer rectangles.
- Drawer open: 5-line skeleton in drawer body.
- Bulk publish progress: HTMX progress bar ("Publishing… {N}/{total}") polls every 2s. On complete: bar turns green, "Published {N} questions" + download audit log link.
- Emergency unpublish: Celery high-priority progress bar. Expected < 60s for 500 questions. If > 60s: "Still processing… ({N} complete)" with cancel option.

### Responsive Behaviour
| Breakpoint | Behaviour |
|---|---|
| Desktop | Full table all columns. Drawer 720px right panel. |
| Tablet | Table: Subject, Difficulty, Revision #, Review Date, Action. Drawer 80% width. |
| Mobile | Table: Subject, Difficulty, Action button. Other columns in expandable row. Drawer full screen. Emergency unpublish modal full-width bottom sheet. |

### Role-Based UI
- "Approve + Publish": Approver (29) only. Director (18) sees read-only Approval drawer without action buttons — "View only. Only the Question Approver can publish questions."
- "Emergency Bulk Unpublish" button: Approver only. Always visible in red at top-right (not behind a menu — emergency access must be immediate).
- 2FA prompt: Approver only. Never shown to Director in read-only mode.
- "Difficulty Re-Tag", "Access Level Change" post-publish: Approver only on Published tab.
- "Create Video Job?" inline prompt: Content Producer (82) and Content Director (18) only — shown after successful Approve + Publish. Hidden from Approver (29), Reviewers, SMEs.

---

*Page spec complete.*
*Amendments applied: G2 (Amendment Review + unpublish workflow) · G4 (Access Level post-publish change) · G5 (Extend Valid Until) · G7 (Committee Review — Approver receives only after 2 reviewer passes, 2FA on amendment) · G8 (Emergency Bulk Unpublish < 60s for 500 questions)*
*Gap amendments: Gap 5 (Individual Archive + Bulk Archive action in Published Questions tab — Section 8) · Gap 15 (Passage Set approval context — Drawer Tab 4 with full set status, "Approve Entire Set" button)*
*Div E integration: Post-approval "Create Video Job?" prompt in Drawer action bar (Section 6) for Content Producer/Director · E-05 integration link in Section 8.*
*Next file: `d-05-director-dashboard.md`*
