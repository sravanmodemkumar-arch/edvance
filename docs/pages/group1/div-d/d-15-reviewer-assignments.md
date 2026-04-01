# D-15 — Reviewer Assignment Manager

> **Route:** `/content/director/reviewer-assignments/`
> **Division:** D — Content & Academics
> **Primary Role:** Content Director (18) — full access
> **Read Access:** Question Reviewer (28) — own assignment view only (`?reviewer_view=1`)
> **File:** `d-15-reviewer-assignments.md`
> **Priority:** P2 — Needed once ≥ 2 reviewers are active simultaneously
> **Status:** ⬜ Not started
> **Amendments:** G7 (Committee Review Config per subject — sequential 2-reviewer process toggle)

---

## 1. Page Name & Route

**Page Name:** Reviewer Assignment Manager
**Route:** `/content/director/reviewer-assignments/`
**Part-load routes:**
- `/content/director/reviewer-assignments/?part=assignment-matrix` — reviewer × subject assignment grid
- `/content/director/reviewer-assignments/?part=queue-depth` — live queue depth per reviewer
- `/content/director/reviewer-assignments/?part=rebalance-preview&from={user_id}&to={user_id}&count={n}` — rebalance preview
- `/content/director/reviewer-assignments/?part=sla-config` — SLA configuration panel
- `/content/director/reviewer-assignments/?part=oof-status` — out-of-office status panel
- `/content/director/reviewer-assignments/?part=committee-config` — committee review config (G7)
- `/content/director/reviewer-assignments/?part=reviewer-view&reviewer_id={user_id}` — reviewer's own assignment view

---

## 2. Purpose (Business Objective)

The two-gate quality pipeline (Reviewer → Approver) breaks down when reviewers are unassigned, overloaded, unavailable, or assigned to subjects outside their competence. D-15 is where the Content Director configures and actively manages this pipeline.

The core problems D-15 solves:

**Competency-gated assignment:** A Math SME's questions should not be reviewed by the GK Reviewer. The Assignment Matrix ensures each reviewer is only routed questions from their authorised subjects. A reviewer marked as "Primary" gets new questions auto-routed from D-03's queue logic; a reviewer marked as "Backup" only receives questions when the Primary is unavailable or overloaded.

**Live load balancing:** The Director can see how many questions each reviewer currently has in their queue — and rebalance instantly by moving N oldest questions from an overloaded reviewer to one with capacity. This prevents bottlenecks when one reviewer calls in sick or a subject has an unexpected production surge.

**SLA configuration:** Different subjects and exam types have different content velocity and exam timelines. SSC CGL questions during a freeze run-up need faster review than UPSC Optional questions. D-15 is where these SLAs are set — D-13 monitors compliance.

**Out-of-Office management:** A reviewer who goes on leave without an OOO toggle leaves questions stuck in their queue. The OOO toggle auto-routes new assignments to the designated backup for the OOO period.

**Committee Review configuration (G7):** The amendment introduced sequential 2-reviewer review for High Stakes questions. D-15 is where the Director configures which subjects and/or exam types require committee review, and designates the eligible reviewer pool for committee assignments.

**Business goals:**
- Ensure every question has a competency-matched reviewer assigned within SLA
- Surface reviewer overload or underload before questions breach SLA
- Enable instant rebalancing without disrupting in-progress reviews
- Manage reviewer availability (OOO) proactively rather than reactively
- Configure committee review scope per subject (G7)

---

## 3. User Roles

| Role | Access |
|---|---|
| Content Director (18) | Full — assignment matrix edit, SLA config, OOF management, rebalance actions, committee review config |
| Question Reviewer (28) | Restricted read — own assignment view (`?reviewer_view=1`): which subjects they are assigned to, current queue depth, their SLA targets, and their own OOO toggle. Cannot see other reviewers' data. |

---

## 4. Section-Wise Detailed Breakdown

---

### Section 1 — Page Header

- H1: "Reviewer Assignment Manager"
- Live summary strip (auto-refreshed every 60s via HTMX):
  - Total questions in review queue: **{N}**
  - Questions past SLA: **{N}** — red if > 0
  - Reviewers currently active: **{N} / {total}** (OOO-adjusted)
  - Avg queue depth per active reviewer: **{N}**

---

### Section 2 — Assignment Matrix

**Purpose:** The authoritative record of which reviewer covers which Subject + Exam Type combination — primary and backup assignments.

**Layout:** Two-axis table.
- Rows: Subject + Exam Type pairs (e.g. "Mathematics — SSC CGL", "Mathematics — SSC CHSL", "GK — All Exam Types")
- Columns: Each active reviewer (role label: "Reviewer 1", "Reviewer 2", etc. — not personal names per DPDPA)

**Each cell contains a tri-state dropdown:**

| State | Meaning |
|---|---|
| Primary | Reviewer receives new questions for this subject/exam type by default |
| Backup | Reviewer receives questions only when Primary is OOO or queue > threshold |
| — (None) | Reviewer not assigned to this subject/exam type |

**Assignment rules enforced:**
- Every Subject + Exam Type combination must have at least 1 Primary assigned — row highlighted amber if no Primary exists
- A reviewer can be Primary for multiple subjects — but the Director sees a workload estimate (avg daily volume × SLA days) next to each assignment
- Committee Review-eligible reviewers (G7) are designated separately in the Committee Config section — being in the assignment matrix alone does not automatically include a reviewer in committee review

**"Edit Assignments" mode:**
- Toggle button switches cells from read-only badges to dropdown selectors
- Unsaved changes highlighted amber
- "Save All" → single POST updating `content_reviewer_assignment` table
- On save: D-03 routing logic reads from this table immediately — new questions submitted after save are routed to updated assignments; in-progress assignments (already in a reviewer's queue) are not affected

**Workload Estimate column (rightmost):**
Per reviewer: "Estimated daily inflow (next 30 days): ~{N} questions · Avg SLA: {N} days · Estimated max queue depth: {N}"

Derived from: `content_question` (DRAFT state authored in last 30 days, subject-filtered) ÷ active days + current in-queue count. This is a planning estimate, not a live metric.

---

### Section 3 — Live Queue Depth Panel

**Purpose:** Real-time view of each reviewer's current load — how many questions are currently assigned to them.

**Auto-refresh:** 60s HTMX poll (`?part=queue-depth`), paused when a rebalance action is in progress.

**Table columns:**

| Column | Description |
|---|---|
| Reviewer | Role label |
| Assigned (Total) | Current questions in `UNDER_REVIEW` state assigned to this reviewer |
| Past SLA | COUNT where `(today - assigned_at) > sla_days` for subject — red badge |
| Oldest Item Age | Days since oldest currently assigned question was assigned — red if > SLA |
| Status | 🟢 Active · 🟡 High Load (> threshold) · 🔴 OOO (auto-routed to backup) |
| Last Action | Timestamp of reviewer's most recent Pass/Return decision in D-03 |
| Subject Breakdown | Expandable: per-subject counts (e.g. Math: 14 · GK: 31 · English: 8) |

**High Load threshold:** Configurable per reviewer in the SLA Config panel (default: 50 questions). When a reviewer exceeds this threshold, new questions for their subjects are automatically routed to the Backup reviewer. The Director sees a 🟡 warning.

**"Rebalance" action (per reviewer row):**
Available when a reviewer's queue is ≥ 20 questions more than the platform average. Opens the Rebalance Preview panel (see Section 4).

---

### Section 4 — Rebalance Action

**Purpose:** Move N oldest questions from an overloaded reviewer to one with available capacity — without disrupting questions already being reviewed.

**Trigger:** Director clicks "Rebalance" on a reviewer row, or clicks the "Rebalance Queue" button in the D-05 Director Dashboard.

**Rebalance Preview panel** (HTMX part-load into a 640px right drawer):

**Step 1 — Configure:**
- From Reviewer: pre-selected (the overloaded reviewer)
- To Reviewer: dropdown — shows only reviewers who:
  - Are currently active (not OOO)
  - Are assigned (Primary or Backup) to the same subjects as the questions being moved
  - Have queue depth below High Load threshold
- Question Count: slider (1 to max available for rebalance) — default: half the excess over average
- Subject Filter: "Move questions from subject: [All / specific subject dropdown]" — useful when only one subject is overloaded

**Step 2 — Preview** (`?part=rebalance-preview&from={user_id}&to={user_id}&count={n}`):
- Shows the N oldest questions that would be moved: short UUID · subject · days in queue
- Excludes questions that are actively being reviewed (i.e. the reviewer's D-03 drawer is open — detected via a `content_question_review_lock` record with `locked_at > now() - 5 minutes`)
- "Confirm Rebalance" button

**On confirm:**
- `content_question.assigned_reviewer_id` updated for the N selected questions
- `content_question_audit_log` entry: `action: ReviewerReassigned · from: Reviewer A · to: Reviewer B · reason: Director rebalance`
- Reviewer A: in-progress question (if any open in D-03) is not moved — only queued questions move
- Reviewer B: questions appear in their D-03 "Assigned to Me" tab immediately (HTMX next poll)
- Director sees confirmation: "Moved {N} questions from Reviewer A to Reviewer B."

---

### Section 5 — SLA Configuration Panel

**Purpose:** Per-subject, per-exam-type review SLA settings — how many days a reviewer has to act on each question type.

**Table:**

| Column | Description |
|---|---|
| Subject | e.g. Mathematics |
| Exam Type | SSC CGL · All Types · etc. |
| Review SLA (days) | Default: 3 days. Editable integer. |
| Approval SLA (days) | SLA for D-04 Approver after Reviewer passes. Default: 2 days. |
| Amendment SLA (hours) | SLA for amendment reviews (G2). Default: same-day (8 hours). |
| High Load Threshold | Max questions in queue before auto-routing to backup. Default: 50. |
| Notes | Optional free text — e.g. "SSC CGL pre-exam: reduce to 1 day" |

**Save:** Updates `content_sla_config` table. D-13 Quality Analytics uses this table to calculate SLA breach metrics. D-03 Review Queue uses this table to show the "Oldest Current Item Age" colour thresholds.

**SLA Override for Surge Periods:**
"Add Temporary Override" → select Subject + Exam Type + new SLA value + date range (override active from/to). Celery task auto-restores the original SLA on the override end date. Overrides shown in the table as a sub-row in amber with the override end date.

---

### Section 6 — Out-of-Office Management

**Purpose:** Manage reviewer availability and ensure continuous question flow when a reviewer is unavailable.

**Active OOO table:**

| Column | Description |
|---|---|
| Reviewer | Role label |
| OOO From | Start date |
| OOO Until | End date (inclusive) |
| Backup Reviewer | Who receives new assignments during OOO |
| Questions Moved | COUNT moved to backup at OOO activation |
| Status | 🔴 Active · 🟡 Upcoming · ✅ Past |

**"Set OOO" action (Director):**
- Reviewer selector
- From/Until date pickers
- Backup Reviewer dropdown (must be assigned to the same subjects — validated)
- "Move existing queue to backup" toggle (default ON): if ON, all currently assigned questions (not in active review) are moved to the backup reviewer immediately

On save:
- `content_reviewer_oof` record created
- If "Move existing queue" ON: Celery task reassigns questions (same mechanism as Rebalance) + audit log entries
- D-03 auto-routing: during OOO period, new submissions for OOO reviewer's subjects go directly to backup
- Director sees the OOO reviewer's status as 🔴 OOO in the Live Queue Depth panel

**Reviewer self-OOO toggle (`?reviewer_view=1`):**
Reviewers can set their own OOO via the Reviewer View (see Section 8). This notifies the Director via a D-05 dashboard alert. The Director must then confirm the backup assignment — self-OOO without a Director-confirmed backup does not auto-route (safety: Director is aware of all queue routing changes).

**Auto-expiry:** Celery nightly task checks `content_reviewer_oof` — marks past records as ended. New questions resume routing to the primary reviewer the day after OOO ends. In-flight backlog (questions still in backup's queue) stays with the backup — not automatically moved back.

---

### Section 7 — Committee Review Configuration (Amendment G7)

**Purpose:** Configure which subjects and exam types require the sequential 2-reviewer committee process for High Stakes questions.

**What committee review means (recap from D-03):**
- A "High Stakes" question (flagged by Reviewer 1 or auto-flagged by criteria below) goes through sequential review: Reviewer 1 passes → Reviewer 2 passes → only then reaches D-04 Approver.
- Reviewer 2 cannot be the same person as Reviewer 1 (enforced at assignment time).

**Committee Review Config table:**

| Column | Description |
|---|---|
| Subject | e.g. Mathematics |
| Exam Type | SSC CGL · All Types |
| Committee Review Required | Toggle: ON / OFF |
| Trigger Criteria | "All questions" / "Difficulty: Hard only" / "Exam Type: High Stakes exams" / "Manual flag by Reviewer" |
| Eligible Reviewer Pool | Multi-select: which reviewers are eligible for Committee Review Reviewer 2 role for this subject |
| Reviewer 2 Assignment | Auto (round-robin from eligible pool) / Manual (Director assigns per-question from D-03) |

**Trigger criteria options:**
- **All questions:** Every question in this subject goes through committee review (use only for very high-stakes subjects)
- **Hard difficulty only:** Only questions tagged Hard go through committee review
- **Specific exam types:** Select which exam type codes trigger committee review (e.g. only UPSC Prelims questions)
- **Manual flag:** Committee review only when Reviewer 1 explicitly flags it via the D-03 "Flag for Committee Review" action — the most common setting

**Eligible Reviewer Pool:**
The Director selects from all active reviewers who are assigned (Primary or Backup) to this subject. The pool must have ≥ 2 reviewers — a warning is shown if only 1 reviewer is in the pool (committee review would always deadlock because Reviewer 2 cannot be Reviewer 1).

**Save:** Updates `content_committee_review_config` table. D-03's assignment logic reads from this table immediately.

**Committee Review Status panel (below config table):**
Live counts:
- Questions currently in Committee Review (both reviewer slots needed): {N}
- Questions awaiting Reviewer 2 assignment: {N}
- Questions where Reviewer 1 passed > {SLA} days ago without Reviewer 2: {N} — red alert

---

### Section 8 — Reviewer Performance Targets (Reference Panel)

**Purpose:** Surface the performance targets configured in D-20 Tab 4 directly in D-15, so the Director can review assignment decisions and SLA configurations in the same context as the targets that define expected performance. Without this, the Director must switch between D-15 and D-20 to compare current SLA config against the targets.

**Layout:** Collapsible panel at the bottom of the D-15 page (collapsed by default — Director can expand). Heading: "Reviewer Performance Targets (from D-20 Configuration)"

**Panel content (read-only — sourced from `content_reviewer_performance_target`):**

```
Global Performance Targets
──────────────────────────
Throughput:         Min 30 / Target 50 / Max 100 reviews per month
Quality:            Target accuracy 90% · Min 75% · Agreement target 80%
Escalation Ceiling: 10% — flag if reviewer escalates > 10% of questions

SLA Targets:
  Standard Review:    48 hours
  Priority Review:    24 hours
  Amendment Review:   12 hours
  Committee Review:   72 hours
```

**Per-Reviewer Override Indicator:**
For each reviewer shown in the Assignment Matrix and Live Queue panel, an override badge appears if they have a per-reviewer override in D-20: "⚙ Custom targets" with a tooltip showing the override values.

**"Edit Targets →"** link (Director only): navigates to D-20 Tab 4 — Reviewer Performance Targets. In-context discovery so the Director does not need to know D-20 exists.

**Context note below panel:**
"These targets are used as benchmarks in D-13 Quality Analytics charts. SLA configurations above (Section 5) should be aligned with the SLA targets here to avoid inconsistencies."

**Committee Deadlock Fallback (Director override — added here for discovery):**

When a committee review deadlock occurs (all eligible Reviewer 2 candidates are OOO — see D-03 edge cases), the Director needs an emergency resolution path. D-15 Section 7 now includes:

**"Emergency Reviewer Override" action (per committee-deadlocked question):**
- Accessible from the Committee Review Status panel (Section 7 "Questions awaiting Reviewer 2 assignment" row — when any of these are in deadlock state).
- Action: "Designate Emergency Reviewer 2" — Director selects any reviewer outside the normal eligible pool (not just the configured eligible set). Director must provide a documented reason.
- On confirm: selected reviewer is added to the eligible pool for this question only (not a permanent pool change). The deadlock is cleared. The reviewer is notified via D-19. Audit log entry: `action: EmergencyReviewer2Override` · `reason` · Director actor.
- Alternative action: "Override Committee Requirement" — Director can waive the committee review for this specific question with a documented reason. Question moves to `PENDING_APPROVAL` directly after Reviewer 1's pass. Audit log records the waiver.

---

### Section 9 — Reviewer View (Restricted Access)

**Trigger:** Reviewer accesses `/content/director/reviewer-assignments/?reviewer_view=1`

**What the Reviewer sees:**
- "Your Assignments" section:
  - Subjects assigned (Primary): [list of subject + exam type pairs]
  - Subjects assigned (Backup): [list] — with note "You receive questions for these subjects only when the Primary reviewer is unavailable."
- "Your SLA Targets":
  - Per-subject: Review SLA (e.g. Math: 3 days · GK: 1 day) — so reviewers know how quickly they need to act
- "Your Current Queue":
  - Total questions assigned: {N}
  - Past SLA: {N} (red badge if > 0)
  - Oldest item: {N} days
- "Out-of-Office":
  - Current OOO status (if active) or "Not on OOO"
  - "Set Out-of-Office" form:
    - From/Until date pickers
    - Backup preference (optional — Director confirms the actual backup)
    - Note to Director (optional)
    - "Submit OOO Request" → Director receives a D-05 dashboard notification; OOO is NOT active until Director confirms backup
- "Committee Review Eligibility":
  - Whether the reviewer is in the eligible pool for committee review for any subjects (read-only)

---

## 5. Data Models

### `content_reviewer_assignment`
| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `reviewer_user_id` | FK → auth.User | — |
| `subject_id` | FK → content_taxonomy_subject | Nullable — if null: applies to all subjects |
| `exam_type_code` | varchar | Nullable — if null: applies to all exam types for this subject |
| `assignment_type` | varchar | Primary · Backup |
| `assigned_by` | FK → auth.User | Director |
| `assigned_at` | timestamptz | — |
| `deactivated_at` | timestamptz | Nullable — soft deactivation |

### `content_reviewer_oof`
| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `reviewer_user_id` | FK → auth.User | — |
| `oof_from` | date | — |
| `oof_until` | date | Inclusive |
| `backup_reviewer_id` | FK → auth.User | Confirmed by Director |
| `self_requested` | boolean | True if reviewer set their own OOO via reviewer view |
| `director_confirmed_by` | FK → auth.User | Nullable — null if self-OOO not yet confirmed |
| `questions_moved_count` | int | COUNT of questions moved to backup at activation |
| `created_at` | timestamptz | — |

### `content_sla_config`
| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `subject_id` | FK → content_taxonomy_subject | Nullable — null means global default |
| `exam_type_code` | varchar | Nullable — null means all exam types |
| `review_sla_days` | int | Default: 3 |
| `approval_sla_days` | int | Default: 2 |
| `amendment_sla_hours` | int | Default: 8 |
| `high_load_threshold` | int | Default: 50 |
| `override_until` | date | Nullable — for temporary surge overrides |
| `original_review_sla_days` | int | Nullable — stored original value for override restoration |
| `updated_by` | FK → auth.User | Director |
| `updated_at` | timestamptz | — |

### `content_committee_review_config`
| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `subject_id` | FK → content_taxonomy_subject | — |
| `exam_type_code` | varchar | Nullable — null means all exam types for this subject |
| `committee_review_enabled` | boolean | Default: False |
| `trigger_criteria` | varchar | AllQuestions · HardDifficultyOnly · SpecificExamTypes · ManualFlag |
| `reviewer_2_assignment_mode` | varchar | Auto · Manual |
| `updated_by` | FK → auth.User | Director |
| `updated_at` | timestamptz | — |

### `content_committee_review_eligible_reviewer`
| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `committee_config_id` | FK → content_committee_review_config | — |
| `reviewer_user_id` | FK → auth.User | — |
| `added_by` | FK → auth.User | Director |
| `added_at` | timestamptz | — |

---

## 6. Access Control

| Gate | Rule |
|---|---|
| Full page access | `PermissionRequiredMixin(permission='content.manage_reviewer_assignments')` — Role 18 |
| Reviewer view | `permission='content.view_own_assignments'` — Role 28. `?reviewer_view=1` triggers reviewer-scoped render; server validates role before rendering |
| Rebalance action | Role 18 only |
| OOO set (Director) | Role 18 only |
| OOO self-request (Reviewer) | Role 28 — creates a pending OOO request; Director must confirm before it activates |
| Committee Review Config | Role 18 only |
| SLA Config edit | Role 18 only |

---

## 7. Edge Cases & Error States

| Scenario | Behaviour |
|---|---|
| All reviewers for a subject are OOO simultaneously | Live Queue Depth panel shows red alert: "No active reviewers for [Subject]. Questions are accumulating unassigned." Director must manually assign or temporarily broaden another reviewer's subject scope. |
| Reviewer 1 in committee review is then set OOO | Their questions in the "awaiting Reviewer 2" state are not auto-moved — committee review is subject-specific and Reviewer 2 assignment is managed separately. Director receives a D-05 alert: "Reviewer A has been set OOO and has {N} committee review questions pending Reviewer 2." Director manually resolves. |
| Director rebalances to a reviewer who then goes OOO before reviewing the moved questions | The OOO activation logic checks the backup reviewer's queue for questions that came from a rebalance — if "Move existing queue" toggle is ON, these are moved again to the backup's backup (or the original primary if recovered). If no backup exists, Director alert fires. |
| Rebalance preview excludes questions a reviewer is actively reviewing | Detected via `content_question_review_lock` records — any question with a lock created within the last 5 minutes is excluded from the moveable set. The lock record is written when the reviewer opens the D-03 drawer and expires after 5 minutes of inactivity (no re-open). |
| Director tries to save an Assignment Matrix where a subject has no Primary reviewer | Server-side validation blocks save: "Mathematics — SSC CGL has no Primary reviewer assigned. Assign at least one Primary before saving." Client-side also highlights the row in red before the save attempt. |
| Committee Review config has only 1 eligible reviewer | Warning on save (not blocked): "Only 1 reviewer eligible for committee review for [Subject]. Reviewer 2 cannot be Reviewer 1 — committee review will be impossible. Add at least one additional eligible reviewer." |

---

## 8. Integration Points

| Integration | Direction | What Flows | Mechanism |
|---|---|---|---|
| D-03 Review Queue | D-15 → D-03 | Assignment rules + OOO status determine which questions appear in each reviewer's queue | D-03 `get_queryset()` reads `content_reviewer_assignment` and `content_reviewer_oof` on each request |
| D-05 Director Dashboard | D-15 → D-05 | Reviewer load alerts, OOO requests, SLA breach counts surface in D-05 Reviewer Load strip | D-05 reads `content_reviewer_oof` + `content_sla_config` + live queue depth from `content_question` |
| D-13 Quality Analytics | D-15 → D-13 | SLA targets from `content_sla_config` used to calculate SLA breach metrics in D-13 Reviewer Performance tab | D-13 reads `content_sla_config` for threshold values |
| D-04 Approval Queue | D-15 → D-04 | Committee review config determines when a question needs 2 reviewer passes before reaching D-04 | D-04's queue excludes questions still in committee review (< 2 passes) |
| D-10 Calendar | D-10 → D-15 | Upcoming exam dates inform when the Director should consider SLA overrides for high-volume exam types | D-15 SLA Override panel displays upcoming exam dates from `content_exam_freeze` as planning context |

---

---

## 9. UI Patterns & Page-Specific Interactions

### Search
- **Assignment Matrix:** Search bar above the matrix rows. Placeholder "Filter subjects…". Instant filter of subject rows (typically < 50 rows).
- **Live Queue Depth panel:** Placeholder "Filter by reviewer role…". Instant filter of reviewer rows (typically < 10 reviewers).
- **SLA Config table:** Placeholder "Filter by subject…". Instant filter.
- **Active OOO table:** Placeholder "Filter by reviewer…". Instant filter.
- **Committee Config table:** Placeholder "Filter by subject…". Instant filter.

### Sortable Columns — Live Queue Depth Table
| Column | Default Sort |
|---|---|
| Assigned (Total) | **DESC (most loaded first)** — default |
| Past SLA | DESC |
| Oldest Item Age | DESC |
| Last Action | ASC (least recently active first) |

### Sortable Columns — SLA Config Table
Default sort: **Subject ASC** (alphabetical).

### Sortable Columns — OOO Table
Default sort: **OOO From ASC** (upcoming OOO first).

### Pagination
- Assignment Matrix: typically < 80 subject+exam-type rows. Show all (no pagination) — matrix must be scannable as a whole.
- Live Queue Depth: typically < 15 reviewers. Show all.
- SLA Config: typically < 50 rows. Show all.
- OOO table: 25 rows, numbered controls.
- Committee Config: typically < 30 rows. Show all.

### Empty States
| Section | Heading | Subtext |
|---|---|---|
| Assignment Matrix — no reviewers | "No reviewers assigned" | "Add reviewer accounts to the platform before configuring assignments." |
| Live Queue Depth — no active reviewers | "No active reviewers" | "All reviewers are currently OOO or no reviewer accounts are configured." |
| Active OOO — none | "No active OOO periods" | "No reviewers are currently marked as out of office." |
| Committee Config — empty | "No committee review configured" | "Enable committee review for a subject using the toggle above." |
| Reviewer View — no assignments | "No subjects assigned to you" | "The Content Director hasn't configured your subject assignments yet." |

### Toast Messages
| Action | Toast |
|---|---|
| Assignment Matrix saved | ✅ "Assignment configuration saved" (Success 4s) |
| Assignment save validation fail | ❌ "{Subject} has no Primary reviewer — assign at least one Primary before saving" (Error persistent) |
| Rebalance complete | ✅ "Moved {N} questions from {Reviewer A} to {Reviewer B}" (Success 4s) |
| OOO set (Director) | ✅ "OOO period configured — questions routing to backup" (Success 4s) |
| OOO with queue move | ✅ "{N} questions moved to backup reviewer" (Success 4s) |
| Self-OOO request submitted (Reviewer) | ℹ "OOO request submitted — awaiting Director confirmation before taking effect" (Info 6s) |
| SLA override saved | ✅ "SLA override saved — expires {date}" (Success 4s) |
| Committee config saved | ✅ "Committee review configuration saved" (Success 4s) |
| Committee config warning (1 reviewer in pool) | ⚠ "Only 1 reviewer eligible — committee review requires ≥ 2. Add another reviewer to the pool." (Warning persistent) |

### Loading States
- Live Queue Depth table: 5-row skeleton on page load. 60s auto-refresh: table body fades to 60% opacity during refresh.
- Rebalance Preview drawer: 5-item skeleton while loading the moveable questions list.
- Assignment Matrix: matrix cell skeleton (grey shimmer in each cell) on initial load.
- Committee Config table: 5-row skeleton.

### Responsive Behaviour
| Breakpoint | Behaviour |
|---|---|
| Desktop | Assignment Matrix: full grid with all reviewer columns. Live Queue: full table. Rebalance drawer 640px. |
| Tablet | Assignment Matrix: horizontal scroll (reviewer columns fixed-width, left-scroll reveals more). Live Queue: Queue Size, SLA Status, Rebalance action. Drawer 80%. |
| Mobile | Assignment Matrix: per-subject accordion — tap subject to expand and see reviewer assignments. Checkboxes for Primary/Backup per reviewer. Live Queue: reviewer name, queue depth badge, status icon. Rebalance drawer: full screen. |

### Assignment Matrix — Interaction Detail
- Cell tri-state: click cycles through None → Primary → Backup → None.
- OR: cell dropdown — click opens dropdown with three options (Primary / Backup / None).
- Unsaved cells: amber background.
- "Save All" button: sticky at bottom of matrix, always visible. Disabled when no changes made. Active (primary blue) when changes exist.
- "Unsaved changes" warning bar appears above Save button when navigating away: "You have unsaved assignment changes. Save or discard before leaving."

### Form Validation
- OOO Set form: OOO From must be ≤ OOO Until. Backup Reviewer required (cannot save without selecting a backup).
- SLA override: "Override Until" date must be > today. New SLA days must be ≥ 1.
- Committee eligible reviewer pool: must have ≥ 2 reviewers to enable committee review (blocking validation).

### Role-Based UI
- Full page + edit access: Director (18).
- Reviewer View (`?reviewer_view=1`): Reviewer (28) sees only own assignments, own queue depth, own OOO toggle, and committee eligibility. No other reviewers' data visible.
- Self-OOO submit: Reviewer only. Does not activate until Director confirms.
- Rebalance action: Director only.
- SLA Config edit: Director only.
- Committee Config: Director only. Reviewers see "You are eligible for committee review in: {subjects}" — read-only.

---

*Page spec complete.*
*Amendments applied: G7 (Committee Review Config per subject — eligible reviewer pool, trigger criteria, sequential 2-reviewer process configuration)*
*Gap amendments: Gap 13 (Reviewer Performance Targets panel — Section 8, read-only display of D-20 targets, per-reviewer override badges, "Edit Targets →" link) · Gap 16 (Committee deadlock fallback — Emergency Reviewer Override + Override Committee Requirement actions in Section 7 status panel, audit trail)*
*Next file: `d-16-feedback-queue.md`*
