# D-05 — Content Director Command Center

> **Route:** `/content/director/`
> **Division:** D — Content & Academics
> **Primary Role:** Content Director (Role 18)
> **Secondary Access:** Question Reviewer (28) — read of own queue metrics only via a restricted view
> **File:** `d-05-director-dashboard.md`
> **Priority:** P0 — Pipeline visibility before content volume grows
> **Status:** ⬜ Not started
> **Amendments:** G3 (Notes Director Review toggle + Notes Review tab) · G5 (Expiry Monitor tab — Current Affairs question expiry) · G11 (Announcements tab — Director broadcasts to Div D staff)

---

## 1. Page Name & Route

**Page Name:** Content Director Command Center
**Route:** `/content/director/`
**Part-load routes:**
- `/content/director/?part=kpi` — KPI strip
- `/content/director/?part=pipeline-funnel` — pipeline funnel widget
- `/content/director/?part=coverage-matrix` — subject × exam type coverage matrix
- `/content/director/?part=sme-table` — SME production table
- `/content/director/?part=stale-alerts` — stale alerts panel
- `/content/director/?part=reviewer-load` — reviewer load strip
- `/content/director/?part=notes-review&tab=pending` — notes review tab
- `/content/director/?part=expiry-monitor` — expiry monitor tab
- `/content/director/?part=ai-summary` — AI pipeline summary widget
- `/content/director/?part=announcements` — announcements tab
- `/content/director/?part=sme-drawer&sme_id={user_id}` — SME stats drawer

---

## 2. Purpose (Business Objective)

The Content Director's Command Center is a bird's-eye view of the entire content production operation — 9 SMEs, multiple Reviewers, 1 Approver, 1 Notes Editor, 8 exam types, 9 subjects, 18 pages of operational work. Without this page, the Director operates blind: unable to see which subjects are understaffed, which reviewers are bottlenecked, which questions are going stale in the pipeline, and which exam type's content pool is approaching exhaustion.

At 2.4M–7.6M students relying on a balanced, fresh question bank, the Director's primary job is pipeline health. Not individual question quality (that is the Reviewer and Approver's domain) but systemic throughput: Are SMEs hitting their quotas? Is the review bottleneck in Physics or GK? Are Current Affairs questions expiring faster than they are being replaced? Is the AI pipeline acceptance rate collapsing, flooding the review queue with bad questions?

All of these signals are on this page. The Director acts not by editing questions themselves, but by resetting quotas, reassigning reviewers, escalating stale questions, approving notes, and broadcasting guidance to the content team (G11).

**Business goals:**
- Give the Content Director a complete real-time picture of the entire content pipeline in one view
- Surface actionable alerts (stale questions, reviewer overload, expiry risk) before they become failures
- Enable Director-level interventions: quota adjustment, reviewer escalation, notes approval, announcement broadcast
- Monitor AI pipeline quality and triage acceptance rates
- Provide notes oversight gate when Director Review Toggle is enabled (G3)
- Track Current Affairs question freshness and expiry risk (G5)

---

## 3. User Roles

| Role | Access |
|---|---|
| Content Director (18) | Full — all tabs, all write actions, announcements, notes approval |
| Question Reviewer (28) | Read — own queue metrics only (a restricted "My Performance" sub-view of D-05, not the full page; Reviewer sees D-05's Overview tab only with data filtered to their own queue metrics) |

> **Reviewer access:** The Question Reviewer does NOT see the SME Production Table, Subject Coverage Matrix, or Reviewer Load strip for other reviewers. They can access `/content/director/?reviewer_view=1` which returns only their own queue depth, oldest item age, 7-day throughput, and return rate. This is explicitly listed in D-03's KPI strip as read-only data from D-05.

---

## 4. Section-Wise Detailed Breakdown

---

### Section 1 — Page Header

- H1: "Content Director Command Center"
- Content Director name + role label
- Date + time with timezone (IST — content team is all India-based)
- "Emergency Actions" dropdown (top-right): quick links to D-04 Emergency Bulk Unpublish and D-15 Reviewer Reassignment — for incidents where the Director needs to reach those functions without navigating away

---

### Section 2 — KPI Strip

| Tile | Metric | Colour Rule |
|---|---|---|
| Published Questions | Total `PUBLISHED` in content schema | — |
| Published This Week | COUNT published in last 7 days | Amber if < weekly target (from D-10) |
| In Review Now | Total `UNDER_REVIEW` | Amber if > 500 · Red if > 1,000 (pipeline accumulation) |
| Awaiting Approval | Total `PENDING_APPROVAL` | Amber if > 100 · Red if > 300 |
| Stuck (> 3 days returned) | Questions in `RETURNED` state for > 3 days without SME resubmission | Amber if > 0 · Red if > 10 |
| Notes Pending Director Review | COUNT of notes in `PENDING_DIRECTOR_REVIEW` | Red if > 0 (Director-gated notes are waiting) |
| AI Triage Queue | COUNT in D-08 triage queue | Amber if > 200 (backlog building) |

KPI refreshes every 60s.

---

### Section 3 — Pipeline Funnel Widget

**Purpose:** Live count at each stage of the MCQ pipeline — shows where questions are accumulating.

**Visual:** Horizontal funnel diagram (or stacked bar chart) with 5 stages:

| Stage | Count | Δ vs Yesterday |
|---|---|---|
| Draft | All `DRAFT` questions | ±N |
| Under Review | All `UNDER_REVIEW` | ±N |
| Pending Approval | All `PENDING_APPROVAL` | ±N |
| Published | All `PUBLISHED` | ±N (new publishes minus new unpublishes) |
| Amendment Review | All `AMENDMENT_REVIEW` | ±N |

Each stage is clickable — links to the relevant page (D-01 filter for Draft, D-03 for Under Review, D-04 for Pending Approval, D-11 for Published, D-04 Amendment Reviews tab for Amendment Review).

**Bottleneck indicator:** The stage with the highest positive Δ vs yesterday (fastest accumulation) is highlighted amber — that is where throughput is breaking down.

---

### Section 4 — Subject Coverage Matrix

**Purpose:** At-a-glance content health across all 9 subjects × 8 exam types — the Director's daily quality map.

**Layout:** 9-row × 8-column grid. Row = Subject (Math, Physics, Chemistry, Biology, English, GK, Reasoning, CS, Regional Language). Column = Exam Type (SSC CGL, SSC CHSL, RRB NTPC, RRB Group D, AP Board, TS Board, UPSC Prelims, Online).

**Each cell:** Published question count + coverage % (question count / target count for that subject+exam combination — targets set in D-10 or D-14).

**Cell colour coding:**
- 🟢 Green: ≥ 100% of target
- 🟡 Amber: 50–99% of target
- 🔴 Red: < 50% of target
- Grey (—): subject not included in this exam type (per D-09 Exam Type Mapping)

**Cell click:** Drills to D-14 Syllabus Coverage page filtered to that subject + exam type combination — shows topic-level breakdown.

**Row summary (rightmost column):** Per subject — total published count across all exam types + overall coverage rating (green/amber/red based on worst-performing exam type for that subject).

---

### Section 5 — SME Production Table

**Purpose:** Per-SME production tracking — who is hitting quota, who is falling behind, where intervention is needed.

**Columns:**

| Column | Description |
|---|---|
| SME | Subject label ("GK SME") — not personal name. Click → SME Stats Drawer |
| Subject | — |
| Quota (This Month) | Target set in D-10 `content_sme_quota` |
| Authored (This Month) | COUNT of questions created this month (all states) |
| In Pipeline | COUNT in `UNDER_REVIEW` or `PENDING_APPROVAL` (not yet published) |
| Return Rate (30d) | (returned / submitted) × 100% in last 30 days |
| Published (This Month) | COUNT of questions by this SME that reached `PUBLISHED` state this month |
| Published (Lifetime) | Total lifetime published count |
| Quota % | (Published this month / Quota) × 100% — colour-coded |

**Quota % colour coding:**
- ≥ 100%: Green
- 50–99%: Amber
- < 50%: Red (if > 10 working days into month — not red on day 1)

**Inline action per row:**
- "Set Quota" — opens a small inline form: integer input for new quota target. On save: updates `content_sme_quota` table + sends in-app notification to the SME (D-01 KPI strip updates on next poll). "Set" button triggers confirmation: "Update {SME subject}'s quota to {N} questions for March 2026?"

**Sort:** Default — Quota % ascending (most behind first). User can re-sort any column.

**SME Stats Drawer (560px)** — triggered by row click or SME label:
- Tabs: Pipeline (full breakdown of question states) · Quality Metrics (return rate trend, error type breakdown, avg review cycles) · Quota Progress (monthly bar chart: authored vs quota per month, 6-month rolling) · Coverage Gaps (Director's view of what topics this SME still needs to fill, from D-14 data for their subject)
- "Set Quota" action repeated in drawer for convenience

---

### Section 6 — Stale Alerts Panel

**Purpose:** Proactive escalation of pipeline items that have exceeded their SLA without Director intervention.

**Alert categories (shown in priority order):**

**1. Questions in Review > SLA:**
- SLA thresholds from D-15 config (GK Current Affairs: 1 day · All others: 3 days)
- Per question row: Question ID (truncated) · Subject · Topic · Days Waiting · Reviewer (role label) · Escalation Status · "Escalate" button

**Escalation tracking (per question row):**
Each alert row shows an **Escalation Status** badge alongside the action button. This prevents the Director from escalating the same question repeatedly without knowing what happened to the previous escalation.

| Escalation Status | Badge | Meaning |
|---|---|---|
| Not Escalated | — (grey) | No escalation sent yet |
| Escalated | 🟡 "Escalated {N} min ago" | Notification sent; waiting for Reviewer response |
| Acknowledged | 🟢 "Acknowledged {N} min ago" | Reviewer opened the notification (D-19 `is_read = True`) |
| In Progress | 🔵 "In Progress" | Reviewer has opened the question drawer (D-03 review drawer opened, `assigned_reviewer_id` confirmed) |
| Resolved | ✅ "Resolved" | Question left the SLA-breached state (Reviewer passed / returned it) |

**"Escalate" button behavior:**
- First escalation: sends in-app notification to the assigned Reviewer + their backup. Creates a `content_escalation_log` record. Button changes to "Re-Escalate".
- Re-Escalate (if status is still "Escalated" after 4 hours): re-sends the notification, increments `escalation_count`. Tooltip on button: "Last escalated {N} hours ago."
- If Reviewer is OOO: escalation is automatically routed to the backup reviewer (from D-15 OOO config). If backup is also OOO: escalation notification is sent to the Director's own inbox with a message: "Both primary and backup reviewer are OOO — manual reassignment may be needed."
- Toast: ✅ "Escalation sent to {Reviewer role}" (Success 4s)

**`content_escalation_log` (new model — tracks escalation state per stale item):**
| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `question_id` | FK → content_question | Nullable (escalations can target Approver items too) |
| `escalation_type` | varchar | ReviewSLA · ApprovalSLA · AmendmentSLA · SMEReturn |
| `escalated_by` | FK → auth.User | Director |
| `escalated_to` | FK → auth.User | Reviewer or Approver role |
| `escalation_count` | integer | How many times escalated (starts at 1) |
| `status` | varchar | Pending · Acknowledged · InProgress · Resolved |
| `acknowledged_at` | timestamptz | Nullable — when Reviewer opened D-19 notification |
| `resolved_at` | timestamptz | Nullable — when question left the breached state |
| `created_at` | timestamptz | First escalation time |
| `updated_at` | timestamptz | Last status change |

**2. Questions in Approval > 2 days:**
- Questions in `PENDING_APPROVAL` for > 2 days
- Per row: Question ID · Subject · Days Waiting · Escalation Status · "Escalate to Approver" button
- Same escalation tracking logic as above — status transitions from Escalated → Acknowledged → In Progress → Resolved

**3. Amendment Reviews > 1 day:**
- `AMENDMENT_REVIEW` questions with Reviewer pass > 1 day ago but not yet re-approved by Approver
- Per row: Question ID · Subject · Days Since Reviewer Passed · Escalation Status · "Escalate to Approver" button — red badge (amendment reviews have hardest SLA)

**4. SME has not resubmitted Returned question > 3 days:**
- Questions in `RETURNED` state where return date > 3 days ago
- Per row: Question ID · Subject · Return Date · Days Since Return · Escalation Status · "Notify SME" button — sends in-app reminder to the SME

**5. SME OOO — Actions Needed:**

When an SME sets their Out-of-Office in D-19, this sub-panel appears in the Stale Alerts Panel automatically. It is not a SLA breach — it is a proactive workload management alert.

**Panel header:** "SME Out-of-Office Actions Needed" (only visible if at least one SME has an active OOO period)

**Per-SME OOO section:**
> "SME {Subject} · OOO: {From Date} → {Until Date}"
>
> Note to Director: "{Optional SME note from D-19 OOO form}"

**Question list below (for the OOO SME):**

| Column | Description |
|---|---|
| Question ID | Truncated |
| Topic | — |
| Status | DRAFT · RETURNED |
| Days Since Last Activity | — |
| Action | "Reassign to Another SME" · "Keep in Queue" |

**"Reassign to Another SME"** action (per question):
- Opens a small modal: "Reassign to which SME?" — dropdown of other active SMEs for the same subject (same subject required — content expertise constraint).
- On confirm:
  - `content_sme_question_reassignment` record created (from OOO SME → selected SME).
  - Question's `sme_user_id` updated on `content_question`.
  - Target SME receives D-19 notification: "A question has been reassigned to you — {Subject} · {Topic}."
  - D-12 audit log entry: `action: QuestionReassigned` · `from: OOO SME role` · `to: New SME role` · `by: Director`.
  - Toast: ✅ "Question reassigned to {SME role}" (Success 4s).

**"Keep in Queue"** action:
- Records the Director's explicit choice to leave the question with the original SME. No notification sent. Adds a "Kept — awaiting SME return" label to the row. Director can change this decision by clicking "Reassign" later.

**"Reassign All Pending"** button (per OOO SME section):
- Batch action: reassigns all DRAFT and RETURNED questions for this SME to a single selected replacement SME. Same modal — one destination SME for all questions. Confirmation: "Reassign {N} questions from {Subject} SME to another {Subject} SME?"

**6. Pool Adequacy Red Alerts (Amendment G12):**
- Topics where the Pool Adequacy indicator (D-14) has gone red (pool insufficient for concurrent exam demand)
- Per row: Subject · Topic · Adequacy % · Concurrent Demand · Pool Size · "Assign SME" button (navigates to D-10 to set a special quota for this topic)

---

### Section 7 — Reviewer Load Strip

**Purpose:** Current workload distribution across all active Question Reviewers — helps Director identify overload and trigger rebalancing.

**Per-reviewer row (condensed strip format — one row per reviewer):**

| Column | Description |
|---|---|
| Reviewer | "Reviewer {N}" — role title, not personal name |
| Current Queue | COUNT of questions assigned to this reviewer now |
| Oldest Item | Age of the oldest question in their queue — red if > SLA |
| 7-day Avg Throughput | Questions reviewed per day over last 7 days |
| Return Rate (7d) | % returned in last 7 days |

**Action: "Reassign N Questions"**
Per-reviewer row has a "Reassign" button. Opens a modal:
- Select how many questions to reassign: slider 1–50
- Select destination reviewer (from dropdown of active reviewers)
- "Reassign {N} Questions from Reviewer A to Reviewer B" — confirmation
- Backend: atomically reassigns N oldest assigned-to-A questions to Reviewer B
- Used when a Reviewer goes on leave mid-queue or is overwhelmed before a peak exam period

---

### Section 8 — Notes Review Tab (Amendment G3)

**Purpose:** Director reviews and approves or returns notes submitted by the Notes Editor (D-06) — only when the Director Review Toggle is enabled for a subject in this tab.

**Director Review Toggle (per subject):**
A settings panel at the top of this tab showing all 9 subjects with an ON/OFF toggle each: "Require Director Approval for [Subject] Notes?" Default: OFF for all subjects. Toggling ON for a subject means all future notes submissions for that subject will create `PENDING_DIRECTOR_REVIEW` records in this tab.

**Notes Pending Review table:**

| Column | Description |
|---|---|
| Title | Note title |
| Subject | — |
| Topic(s) | Tags from D-06 structuring |
| Institution Source | Which institution's faculty uploaded this |
| Notes Editor | "Notes Editor" role label |
| Submitted Date | When Notes Editor published it (triggering Director review) |
| File Size | PDF file size |
| "Preview" | Opens PDF preview in a 860px drawer |

**Per-note actions:**
- "Approve" — note state: `PENDING_DIRECTOR_REVIEW` → `PUBLISHED`. PDF moves from S3 `notes-raw/` to `notes-published/`. Notes Editor gets in-app notification: "Your note '{title}' was approved by Content Director."
- "Return with Comment" — text field (≥ 20 chars) + reason category (Factual Error / Outdated Content / Poor Formatting / Inappropriate Content / Scope Mismatch). Note state stays `PENDING_DIRECTOR_REVIEW`; Notes Editor receives return comment in D-06 incoming queue.

**PDF Preview Drawer (860px):** Renders the PDF inline. Director reads the full document before approving. Drawer shows: Title · Subject · Topics · Class/Standard · Exam Types · Source Institution · Submission date.

---

### Section 9 — Expiry Monitor Tab (Amendment G5)

**Purpose:** Track published Current Affairs and Time-Sensitive questions approaching their `valid_until` date — prevent stale GK questions from staying in active exam pools.

**Expiry Overview (top of tab):**
Three count tiles:
- Expiring in ≤ 7 days: red
- Expiring in 8–30 days: amber
- Expiring in 31–90 days: yellow

**Expiry Table:**

| Column | Description |
|---|---|
| Question Preview | First 60 chars |
| Subject | — (mostly GK, some Time-Sensitive in other subjects) |
| Topic | — |
| Content Type | Current Affairs / Time-Sensitive |
| Valid Until | Specific date — colour: red ≤ 7 days · amber ≤ 30 |
| Used in Upcoming Exams | Boolean flag — if this question is scheduled in an upcoming exam paper (from Div F calendar), shown as "⚠ In upcoming exams" — highest priority for extend/replace |
| Published Date | — |

**Per-row actions:**
- "Extend Valid Until" — redirects to D-04 Published tab for this question → Approver's "Extend Valid Until" action (Director cannot extend directly — Approver holds this permission). Opens D-04 with the question pre-selected.
- "Archive Now" — Director can request early archiving before the automatic nightly Celery task. Confirmation modal: "Archive this question now? It will be removed from active exam pools immediately." State: `PUBLISHED` → `ARCHIVED`. Logged in D-12. This is a Director action, not Approver — archiving is considered lower-risk than publishing/unpublishing.

**Bulk Archive button (at bottom of tab):**
"Archive All Expired" — archives all questions past their `valid_until` date that the nightly Celery task has not yet processed. Used at month-end cleanup. Confirmation modal with count. State transitions for all selected: `PUBLISHED` → `ARCHIVED`. Logged as a batch archive event in D-12.

---

### Section 10 — AI Pipeline Summary Widget

**Purpose:** Snapshot of AI MCQ generation pipeline health — embedded in the Overview tab, always visible.

**Data source:** Reads from Div C C-15 AI job table and D-08 triage records.

**Widget content:**
- Today's AI batch status: "Batch #47 running · 1,200 questions generated · 180 auto-rejected (15%) · 1,020 in human triage (D-08)"
- Acceptance rate (last 7 days): % of AI questions that cleared human triage in D-08 and entered D-03
- Avg AI confidence score (last batch)
- Questions currently in D-08 triage queue: COUNT
- Link: "View Triage Queue → D-08"

**Alert: If AI acceptance rate drops below 60% (from the default ~85%):** Red indicator — "AI pipeline quality degraded — acceptance rate is {N}%. Check D-08 triage and C-15 pipeline config." — signals either a prompt quality issue (C-15) or a subject domain issue (hallucinations increasing in a specific subject).

---

### Section 11 — Announcements Tab (Amendment G11)

**Purpose:** Director creates and manages announcements to Div D staff (SMEs, Reviewers, Approver, Notes Editor) — syllabus change notifications, quality policy updates, production reminders, urgent content alerts.

**"New Announcement" form (top of tab):**

| Field | Description |
|---|---|
| Title | Required, max 200 chars |
| Body | Rich text editor — bold, italic, lists, blockquote. This is a formal communication. Max 3,000 chars. |
| Target Audience | Radio group: "All Div D Staff" (all Roles 18–30) · "All SMEs" (Roles 19–27) · "Specific Subjects" (multi-select checkboxes for each subject — Math, Physics, Chemistry, Biology, English, GK, Reasoning, CS, Regional Language) · "Reviewers Only" (Role 28) · "Approver Only" (Role 29) · "Notes Editors Only" (Role 30) |
| Urgency | Radio group: Info · Warning · Action Required |
| Expiry Date | Date picker — optional. If set, announcement auto-hides after this date. If not set: announcement stays active indefinitely until Director retracts it. |

**"Post Announcement" button** — confirmation modal: "Post this announcement to {audience description}? {N} staff will see it immediately."

**Active Announcements list (below form):**
All currently active announcements, newest first.

| Column | Description |
|---|---|
| Title | — |
| Audience | "All SMEs" or "GK SME, English SME" |
| Urgency | Badge |
| Posted | Date + time |
| Expires | Date or "No expiry" |
| Total Recipients | COUNT of users this announcement was sent to |
| Read | COUNT of recipients who have seen it |
| Acknowledged | COUNT for Action Required — COUNT of recipients who clicked "Acknowledged" in D-01 |
| Actions | Edit · Retract |

**Edit:** Director can update the body or expiry of a live announcement. Update is logged in `content_director_announcements` with `updated_at` timestamp. Recipients who already read it see the "Updated" badge on next load.

**Retract:** Removes the announcement from all recipients' D-01 Announcements tabs immediately. Confirmation: "Retract this announcement? All recipients will stop seeing it immediately." Retracted announcements move to "Past Announcements" section (collapsed, for Director's reference).

**Past Announcements** (collapsed section at bottom): All retracted and expired announcements — title, dates, audience, read count at time of retraction. Read-only.

---

### Section 12 — Tab Navigation Summary

| Tab | Content | HTMX Refresh |
|---|---|---|
| Overview | KPI + Pipeline Funnel + Coverage Matrix + SME Table + Stale Alerts + Reviewer Load + AI Summary | 60s on active widgets |
| Pipeline Detail | Expanded pipeline funnel with per-subject × per-state breakdown | 60s |
| SME Productivity | Full SME table with charts (authored vs quota per month, 6-month rolling per SME) | 5 min |
| Reviewer Load | Full reviewer load table with per-reviewer 30-day trend charts | 5 min |
| Stale Alerts | Full stale alert panel — all categories | 5 min |
| Notes Review | Notes pending Director approval (G3) | 5 min |
| Expiry Monitor | Current Affairs expiry tracking (G5) | 1 hour |
| Announcements | Announcement management (G11) | On demand |

---

## 5. Data Models

All data read from existing tables in the content schema — no new tables needed for the main dashboard except:

### `content_director_announcements` (Amendment G11)
*(Defined in D-01 spec — shared table)*

### `content_announcement_reads` (Amendment G11)
*(Defined in D-01 spec — shared table)*

### D-05 reads from:
- `content_question` (state, subject, author, created_at, state_changed_at)
- `content_sme_quota` (monthly quota per SME)
- `content_taxonomy_topic` (published counts for coverage matrix)
- `content_reviewer_assignment` (reviewer subjects + backup config from D-15)
- `content_notes` (state = PENDING_DIRECTOR_REVIEW)
- `content_sla_config` (SLA thresholds per subject from D-15)
- Div C C-15 AI job table (AI pipeline summary — shared DB read)
- `content_ai_question_queue` (D-08 triage queue depth)
- `content_question_audit_log` (pool adequacy data from D-14 amendment G12 context)

---

## 6. Access Control

| Gate | Rule |
|---|---|
| Page access | `PermissionRequiredMixin(permission='content.view_director_dashboard')` — Role 18 |
| Reviewer view | `/content/director/?reviewer_view=1` returns only own-metrics data · `PermissionRequiredMixin(permission='content.view_own_review_metrics')` — Role 28 |
| SME Stats Drawer | Accessible to Director only — Role 18 permission check in the drawer view |
| Director Review Toggle | Only Role 18 can toggle per-subject notes review requirement |
| Archive action (Expiry Monitor) | Role 18 — Director can archive expired questions |
| Announcement Post | Role 18 only |
| Reviewer Load "Reassign" action | Role 18 only |
| Notes "Approve" / "Return" actions | Role 18 only |

---

## 7. Edge Cases & Error States

| Scenario | Behaviour |
|---|---|
| Coverage matrix data takes > 2s to load | Coverage matrix defers rendering until taxonomy query resolves — shows a loading skeleton grid while waiting |
| A Reviewer has 0 questions assigned (new reviewer or all reviewed) | "Reviewer Load" strip shows 0 queue with green indicator. "Reassign" button is disabled (no questions to reassign to them) |
| Director enables Notes Review Toggle for a subject | Toggle change takes effect immediately — all future notes submissions for that subject will route to `PENDING_DIRECTOR_REVIEW`. Notes already in `PUBLISHED` state are not retroactively put back into pending review. |
| Director tries to Archive a question that is scheduled in an upcoming exam | Archive action blocked: "This question is scheduled in {N} upcoming exams. Remove it from those exams in Div F before archiving." — or shows a warning and requires Director to type "ARCHIVE" to override (for cases where the exam needs to be rebuilt without this question) |
| Stale alert "Escalate" button clicked when reviewer is out of office | D-15 OOO config routes the escalation to the backup reviewer. If backup is also OOO: escalation goes to Content Director's own inbox (Director self-receives the escalation as a reminder to manually reassign). |
| Director posts announcement with "Action Required" urgency | Recipients who are currently active on the platform (D-01 open) see the amber banner immediately on next HTMX poll (every 5 min from D-01 Announcements part-route). Recipients not currently active see it on next login. |
| AI pipeline summary: C-15 AI job table unavailable | Widget shows "AI pipeline data unavailable — C-15 may be experiencing issues" with a link to C-15 |

---

## 8. Integration Points

| Integration | Direction | What Flows | Mechanism |
|---|---|---|---|
| D-03 Review Queue | D-05 reads | Queue depth per reviewer, oldest item age, throughput | `content_question` + `content_question_review_log` ORM queries |
| D-04 Approval Queue | D-05 reads | Pending approval count, amendment count | `content_question` state counts |
| D-08 AI Triage | D-05 reads | Triage queue depth, acceptance rate | `content_ai_question_queue` + `content_ai_triage_log` |
| D-09 Taxonomy | D-05 reads | Topic-level published counts for coverage matrix | `content_taxonomy_topic` with published question count annotation |
| D-10 Calendar & Quota | D-10 config → D-05 | Monthly quota targets per SME | `content_sme_quota` table |
| D-14 Syllabus Coverage | D-05 links | Coverage matrix cell click navigates to D-14 | URL navigation |
| D-15 Reviewer Assignments | D-15 config → D-05 | Reviewer-subject assignments, SLA thresholds, OOO config | `content_reviewer_assignment` + `content_sla_config` + `content_reviewer_oof` |
| D-01 SME Dashboard | D-05 → D-01 | Announcements posted by Director appear in D-01 (G11) | `content_director_announcements` table — D-01 polls |
| D-06 Notes Management | D-06 → D-05 | Notes in PENDING_DIRECTOR_REVIEW appear in Notes Review tab | `content_notes` state filter |
| C-15 AI Pipeline | C-15 → D-05 | AI job status and metrics for AI Pipeline Summary widget | Shared DB read from C-15 AI job tables |
| Div F Exam Operations | Div F → D-05 | Upcoming exam flag on expiring questions | Shared DB read — Div F's exam-question assignment table |

---

---

## 9. UI Patterns & Page-Specific Interactions

### Search
- **SME Production Table (SME Productivity tab):** Search by role label (e.g. "GK SME"). Placeholder: "Filter SMEs…". Instant filter (no debounce needed — typically < 15 rows).
- **Stale Alerts panel:** Placeholder "Filter alerts by subject or reviewer…". Searches: subject name, reviewer role label.
- **Notes Review tab:** Placeholder "Search notes by title or subject…". Searches: note title, subject name.
- **Expiry Monitor tab:** Placeholder "Search expiring questions by topic…". Searches: topic name, subject.
- **Announcements tab:** Placeholder "Search announcements…". Searches: title and body text.

### Sortable Columns — SME Production Table
| Column | Default Sort |
|---|---|
| Quota Achieved % | **ASC (most behind first)** — default |
| Published this month | DESC |
| Return Rate | DESC |
| Days in Pipeline (avg) | DESC |

### Sortable Columns — Reviewer Load Strip
| Column | Default Sort |
|---|---|
| Queue Depth | **DESC (most loaded first)** — default |
| Oldest Item Age | DESC |
| 7-day Avg Throughput | ASC |

### Sortable Columns — Expiry Monitor Table
Default sort: **Valid Until ASC** (soonest expiring first).

### Pagination
- SME Production Table: typically < 15 rows (one per SME). No pagination needed; show all.
- Notes Review tab: 25 rows, numbered controls.
- Expiry Monitor tab: 50 rows, numbered controls.
- Announcements list: 20 rows, numbered controls.
- Stale Alerts: 50 rows, numbered controls.

### Empty States
| Section | Heading | Subtext |
|---|---|---|
| Stale Alerts | "No stale items" | "All questions are within their review SLA. The pipeline is healthy." |
| Notes Review | "No notes awaiting review" | "Notes submitted by editors for director review will appear here." |
| Expiry Monitor | "No expiring content" | "No published questions are approaching their expiry date." |
| Announcements list | "No announcements posted" | "Create your first announcement to communicate with your content team." |
| SME Production Table | "No SMEs configured" | "Assign SMEs to subjects in the Reviewer Assignments page." |

### Toast Messages
| Action | Toast |
|---|---|
| Quota saved | ✅ "Quota updated — SME notified" (Success 4s) |
| Note approved (G3) | ✅ "Note approved and published" (Success 4s) |
| Note returned (G3) | ✅ "Note returned with your comment" (Success 4s) |
| Announcement posted | ✅ "Announcement posted to {N} recipients" (Success 4s) |
| Announcement retracted | ✅ "Announcement retracted" (Success 4s) |
| Bulk archive (expiry) | ✅ "{N} questions archived" (Success 4s) |
| Director Review Toggle changed | ✅ "Director review {enabled/disabled} for {Subject}" (Success 4s) |
| Stale alert escalation sent | ✅ "Escalation notification sent to {Reviewer role}" (Success 4s) |

### Loading States
- Overview tab: KPI strip — tile shimmer on load. Pipeline Funnel — chart-shaped shimmer rectangle. Coverage Matrix — grid-shaped shimmer.
- SME Production Table: 10-row skeleton.
- Reviewer Load strip: 5-row skeleton.
- Stale Alerts: 5-row skeleton.
- Notes Review tab: 5-row skeleton.
- Charts (Pipeline Funnel, Coverage Matrix, Trend): chart-area shimmer.
- SME Stats Drawer: drawer body 6-line skeleton.
- HTMX 60s poll refresh: table body fades to 60% opacity while refreshing.

### Responsive Behaviour
| Breakpoint | Behaviour |
|---|---|
| Desktop | All tabs visible. Coverage Matrix full grid. Drawers 560px. |
| Tablet | Tab nav: horizontal scroll. Coverage Matrix: horizontal scroll. SME Production Table hides quota breakdown columns. |
| Mobile | Tab nav: horizontal scroll. Coverage Matrix: per-subject list view (not grid). Charts stack vertically. Drawers: full screen. |

### Charts
- **Pipeline Funnel (Overview tab):** Horizontal funnel chart — Draft count, Under Review, Pending Approval, Published today. Click any stage → navigates to that queue (D-03, D-04 etc.). No-data: "Pipeline data loading…".
- **Subject Coverage Matrix:** Heat-map grid (9 subjects × 8 exam types). Green/amber/red cells. Click cell → D-14 for that subject+exam. Mobile: listed vertically as subject cards with exam type chips.
- **Actual vs Target chart (SME Productivity tab):** Grouped bar chart per SME per month (6 months). Published (green), In Pipeline (amber), Quota outline (grey). Legend clickable. Export as PNG / CSV.
- **Trend Charts (if shown inline):** 12-month line chart with anomaly markers.

### Role-Based UI
- Director (18): all tabs, all actions. Quota edit, announcement create, Director Review toggle, bulk archive.
- Reviewer (28) at `?reviewer_view=1`: sees only own queue metrics and own KPI strip. All tabs hidden. No action buttons except own OOO (routed to D-15 reviewer view).
- Notes Review tab Director Review toggle: Director only. Reviewer cannot access this tab.

---

*Page spec complete.*
*Amendments applied: G3 (Notes Review tab + Director Review Toggle per subject) · G5 (Expiry Monitor tab — Current Affairs + bulk archive) · G11 (Announcements tab — post, manage, retract, audience targeting)*
*Gap amendments: Gap 8 (Escalation tracking with state — `content_escalation_log`, Escalation Status badge on all stale alert rows, Re-Escalate logic) · Gap 2 (SME OOO reassignment panel — "SME OOO Actions Needed" sub-panel in Section 6, Reassign/Keep-in-Queue per question, batch reassign)*
*Next file: `d-06-notes-management.md`*
