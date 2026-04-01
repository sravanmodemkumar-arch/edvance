# F-04 — Results Management

> **Route:** `/ops/exam/results/`
> **Division:** F — Exam Day Operations
> **Primary Role:** Results Coordinator (36) — full control including compute trigger and publish
> **Supporting Roles:** Exam Operations Manager (34) — read + approve; Exam Integrity Officer (91) — read + withhold; Platform Admin (10) — full
> **File:** `f-04-results-management.md`
> **Priority:** P0 — Result publication is the highest-stakes irreversible action on the platform

---

## 1. Page Name & Route

**Page Name:** Results Management
**Route:** `/ops/exam/results/`
**Part-load routes:**
- `/ops/exam/results/?part=kpi` — KPI strip
- `/ops/exam/results/?part=computation-queue` — computation queue tab
- `/ops/exam/results/?part=review-queue` — review & approve tab
- `/ops/exam/results/?part=published-list` — published results tab
- `/ops/exam/results/?part=computation-progress&id={id}` — live progress (polls 10s while RUNNING)
- `/ops/exam/results/?part=result-drawer&id={id}` — result publication drawer
- `/ops/exam/results/?part=computation-history` — computation history tab

---

## 2. Purpose

F-04 manages the complete lifecycle of exam results: computation, review, and publication.

At 2,050 institutions, result publishing is not just high-stakes per institution — a wrong rank published to thousands of students simultaneously is a reputation event. The Results Coordinator (36) is the single gated authority who must:
1. Trigger the computation Celery task
2. Review the computed output (sample review, score range check, outlier detection)
3. Approve and publish

**Why results are never auto-published (even with `auto_compute_on_exam_complete = True`):**
- Auto-compute (Celery) is allowed — it prepares the result data
- Auto-publish is NOT allowed — a human must review before students see their scores
- This is a design invariant: `exam_result_publication.status` requires `APPROVED` before `PUBLISHED`

---

## 3. Tabs

| Tab | Label | HTMX |
|---|---|---|
| 1 | Computation Queue | `?part=computation-queue` |
| 2 | Pending Review | `?part=review-queue` |
| 3 | Published Results | `?part=published-list` |
| 4 | Computation History | `?part=computation-history` |

---

## 4. Section-Wise Detailed Breakdown

---

### KPI Strip

| # | KPI | Alert |
|---|---|---|
| 1 | Awaiting Computation | Count of COMPLETED exams without result computation; amber if > 0 |
| 2 | Computation Running | Count of `exam_result_computation.status = RUNNING`; blue pulsing if > 0 |
| 3 | Pending Review | Count with `exam_result_publication.status IN (DRAFT, REVIEWED)`; amber if > 24h old |
| 4 | Published Today | Count published today |
| 5 | Results on Hold | Count with `exam_schedule.integrity_hold = True`; red if > 0 |
| 6 | Overdue Review | Count with `review_window_expires_at < now()`; red if > 0 |

---

### Tab 1 — Computation Queue

Exams that have COMPLETED but do not yet have a result computation started.

#### Filter Bar

| Filter | Control |
|---|---|
| Exam Type | Multi-select |
| Institution Type | Multi-select |
| Date Range | Exam completed at |
| Integrity Hold | Include · Exclude · Only |

#### Computation Queue Table

| Column | Sortable | Notes |
|---|---|---|
| Exam | Yes | Exam name |
| Institution | Yes | Name + type |
| Completed At | Yes (default: ASC — oldest first) | Absolute datetime |
| Duration | No | Exam duration |
| Registered | No | `exam_ops_snapshot.total_registered` |
| Submitted | No | `exam_ops_snapshot.total_submitted` |
| Submission Rate | No | `(submitted / registered) × 100`% — 80%+ is healthy; 50–80% common (grace period); < 50% may indicate technical issues — check F-07 flags and F-03 tickets before computing. |
| Integrity Hold | No | 🔒 hold badge if `integrity_hold = True` |
| Actions | — | [Compute Results] · [View Exam] |

**[Compute Results]:** triggers `compute_exam_results` Celery task. Opens Computation Config Modal.

**Integrity Hold indicator:** Row with `integrity_hold = True` is amber-tinted. [Compute Results] still available (computation can happen; publication is blocked separately). Tooltip: "This exam has an integrity hold. Results will be computed but cannot be published until hold is cleared."

**Bulk action:** Select multiple → [Compute Selected] — triggers computation for all selected exams sequentially. Progress modal shows per-exam status.

**Empty state:** "All completed exams have been processed. No results waiting for computation."

---

### Computation Config Modal (560px)

**Trigger:** [Compute Results]

Header: "Compute Results — {Exam Name} at {Institution}"

| Field | Default | Notes |
|---|---|---|
| Computation Method | RAW_MARKS | Select: **Raw Marks** (score = correct × marks_per_q - wrong × negative_factor) · **Percentile** (ranks within percentile bands) · **Normalized** (mean-shifted normalisation for multi-paper exams — requires normalization notes) |
| Apply Normalization | OFF | Toggle — only valid when exam ran with multiple question papers (SET-A, SET-B). If ON: scores normalised before ranking. |
| Normalization Notes | — | Text area (required if normalization ON) — explains normalisation method used |
| Include Timed-Out Sessions | OFF | Whether to score sessions that expired before submission. If OFF: timed-out sessions get score = 0 and rank = last |
| **Rank Scope** | Per Institution | Select: **Per Institution** (rank within this institution's cohort — default) · **Cross-Institution** (rank across all institutions running this same exam on the same scheduled_start date). |

**Cross-Institution ranking validation:** Cross-Institution ranking is only available when: (1) all `exam_schedule` records with the same `exam_id` and `scheduled_start` date have `result_computation.status = COMPLETED`, AND (2) each such institution has ≥ 50% submission rate. If validation fails, the radio shows amber warning: "Cross-institution ranking unavailable — {N} of {total} institutions have not yet completed results. Available when all institutions finish." Radio option greys out until conditions are met. If user selects it while partially available: ❌ "Cannot compute cross-institution ranks yet. {N} institutions still pending."

**Pre-computation summary (read-only):**
- Total submissions: {N}
- Timed-out sessions: {N}
- Paper: {paper_code}
- Negative marking: {factor}

**[Start Computation]** → `exam_result_computation` created with status = PENDING → Celery task queued. Tab switches to "In-Progress" view for this exam.

---

### Computation In-Progress View

When a computation task is RUNNING, it displays a progress panel (polls every 10s via `?part=computation-progress&id={id}`).

**Two-stage progress:**

```
STAGE 1 — Score Computation
[████████████░░░░░░░░░░░░░░░░] 42%  (218 / 520 submissions scored)
Method: Raw Marks  |  Negative Marking: 0.25
Started: 10:32 AM  |  Elapsed: 1 min 23s
Status: RUNNING

STAGE 2 — Rank Computation
[░░░░░░░░░░░░░░░░░░░░░░░░░░░░] waiting…
Rank Scope: Per Institution  |  Status: PENDING (starts after Stage 1)
```

After Stage 1 COMPLETED → Celery auto-chains `compute_exam_ranks`. Progress panel updates:
```
STAGE 1 — Score Computation  ✅ Done (218 students)
STAGE 2 — Rank Computation
[████████████████████████████] 100% — Ranks assigned  ✅
```

**[Cancel Computation]** — available only when `status IN (PENDING, RUNNING)`. On click: sets `exam_result_computation.status = CANCELLED`. Celery task checks status at the start of each processing batch; if `CANCELLED`, task stops and performs rollback: deletes all `exam_result` records created by this computation job (identified by `computation_id`). If Celery task completes between cancel click and rollback check (race condition): rollback is skipped; UI shows ❌ "Computation already completed — cannot cancel. Use [Recompute] if results are incorrect." Cancel button is not shown for COMPLETED computations.

---

### Tab 2 — Pending Review

Exams with completed computation (`exam_result_computation.status = COMPLETED`) awaiting Results Coordinator review.

#### Review Queue Table

| Column | Sortable | Notes |
|---|---|---|
| Exam | Yes | — |
| Institution | Yes | — |
| Computed At | Yes (default: ASC) | — |
| Students Processed | No | — |
| Review Window Expires | Yes | Amber if < 4h; red if expired. Computed as `exam_result_computation.completed_at + result_review_window_hours (from exam_operational_config)`. Stored in `exam_result_publication.review_window_expires_at`. |
| Publication Status | No | DRAFT · REVIEWED |
| Integrity Hold | No | 🔒 if hold active |
| Actions | — | [Review] · [Quick Publish] |

**[Review]:** opens Result Review Drawer (760px).

**[Quick Publish]:** only shown when publication status = REVIEWED (already reviewed). Skips drawer, opens Publish Confirmation Modal directly.

---

### Result Review Drawer (760px)

**Header:** Exam name + Institution + Status pill + [×]

#### Drawer Tab 1 — Results Summary

**Score Distribution Chart (Recharts `BarChart`):**
- X axis: score ranges (0–10, 10–20, … up to max marks)
- Y axis: student count
- Overlay: pass mark line (if defined)
- Instant outlier detection: bars that are statistically anomalous shown in amber

**Anomaly detection definition:** A score range is flagged amber (anomalous) if: (1) it contains > 40% of all students (heavily left/right-skewed distribution), OR (2) a single score value appears in ≥ 3 standard deviations above/below the mean frequency. If anomaly detected: inline warning: "⚠️ Anomalous score distribution detected — review before approval. Possible causes: answer key error, unusually easy/hard paper, or data issue." [View Details] opens an expanded analysis panel within the drawer.

**Key statistics (computed from result set):**

| Metric | Value |
|---|---|
| Total scored | {N} students |
| Mean score | {X} marks |
| Median score | {X} marks |
| Highest score | {X} marks |
| Lowest score | {X} marks |
| Pass rate | {X}% (if pass mark defined) |
| Standard deviation | {X} |
| P99 score | {X} |
| Timed-out (no score) | {N} |

**Integrity Hold banner** (if `integrity_hold = True`): `bg-[#451A03] border-[#EF4444]` — "⚠️ This exam has an integrity hold placed by {role} on {date}. Results cannot be published until the hold is cleared. Contact Exam Integrity Officer (91) to review case status."

#### Drawer Tab 2 — Sample Records

Random sample of `min(20, total_students)` result records for spot-check. DPDPA: shows `student_ref` (anonymised), score, rank (provisional), and submission timestamp. NOT student names. If total students < 20: note "Showing all {N} results (exam has fewer than 20 submissions)."

| Column | Notes |
|---|---|
| Session Ref (anonymised) | — |
| Score | Raw marks |
| Percentage | — |
| Rank (provisional) | Within institution cohort |
| Submission Time | HH:MM:SS |
| Time Taken | Duration from exam start to submission |

**[Resample]** button: loads a new random 20. Useful for spot-checking different score ranges.

**[Filter sample by score range]:** enter min/max marks to inspect a specific range.

#### Drawer Tab 3 — Validation Checks

Automated pre-publication validation:

| Check | Status | Detail |
|---|---|---|
| Score range valid (all ≥ 0 and ≤ max_marks) | ✅ / ❌ | If ❌: shows count of anomalous records |
| No duplicate ranks within cohort | ✅ / ❌ | — |
| Negative marking applied correctly | ✅ / ❌ | Spot-check via formula verification |
| Submission count matches expected | ✅ / ⚠️ | ⚠️ if submitted < 70% of registered (warning, not block) |
| Computation method matches config | ✅ / ❌ | — |
| No integrity hold | ✅ / 🔒 | 🔒 = blocks publication (not computation review) |

**Integrity hold placed after computation:** [Mark as Reviewed] remains enabled — review is always allowed. [Approve & Publish] disabled with tooltip: "Integrity hold active — results cannot be published. Contact Exam Integrity Officer (91)." Coordinator can still review and sign off; publish becomes available once hold is cleared.

All ✅ or ⚠️ (no ❌): [Approve for Publication] button enabled.
Any ❌: "Fix validation errors before approving" — [Recompute] button shown.

**[Recompute]:** triggers a new `compute_exam_results` task. Previous computation record is retained (status = SUPERSEDED).

#### Drawer Tab 4 — Publish Controls

**Only accessible when all validation checks pass (no ❌).**

| Field | Notes |
|---|---|
| Publication Type | Radio: Full Results · Provisional Results (shows banner to students) |
| Publish to institutions | Toggle (default ON) — institution admins can see results |
| Publish to students | Toggle (default ON) — students can see their own score in portal |
| Release rank? | Toggle — some exams publish score but hold rank initially |
| Coordinator sign-off | Text area — "Review notes" (optional) |

**[Mark as Reviewed]** — sets `exam_result_publication.status = REVIEWED`. Saves review notes.

**[Approve & Publish]** — sets status = APPROVED → triggers `publish_exam_results` Celery task → sets to PUBLISHED.
- Opens Publish Confirmation Modal before executing.
- IMPORTANT: Not available if `integrity_hold = True` — button disabled with tooltip: "Integrity hold active — contact Exam Integrity Officer (91)"
- After `publish_exam_results` COMPLETED: Celery chain triggers `compute_exam_analytics_aggregate` for F-08. No action needed by coordinator.

**Result notification:**
- If `auto_send_result_notification_on_publish = True` (F-09 config): Celery automatically triggers `send_notification_broadcast` using the template with `category = RESULT_RELEASE` and the activated ACTIVE template in F-06. If no ACTIVE result notification template exists, a warning is logged but publish proceeds.
- If `auto_send_result_notification_on_publish = False`: A prompt appears after publish: "Results published. Send result notification to students? [Send Now via F-06] [Skip]"
  - [Send Now via F-06]: opens F-06 Broadcast wizard in a new tab with `exam_schedule_id` pre-filled and `RESULT_RELEASE` template pre-selected.

**[Withhold Results]** — opens Withhold Modal. Sets `exam_result_publication.status = WITHHELD`.

---

### Tab 3 — Published Results

All exams with published results.

#### Published Table

| Column | Sortable | Notes |
|---|---|---|
| Exam | Yes | — |
| Institution | Yes | — |
| Published At | Yes (default: DESC) | — |
| Students | No | Count of students with results |
| Provisional? | No | Badge if `is_provisional = True` |
| Approved By | No | Role label |
| Actions | — | [View] · [Withdraw] · [Mark Final] |

**[Withdraw]:** opens Withdraw Modal. Hides results from institutions/students. Rare action.

**[Mark Final]:** converts provisional → final results (removes provisional banner).

---

### Tab 4 — Computation History

Full audit of all computation jobs.

| Column | Notes |
|---|---|
| Exam | — |
| Institution | — |
| Status | PENDING · RUNNING · COMPLETED · FAILED · CANCELLED · SUPERSEDED |
| Method | RAW_MARKS · PERCENTILE · NORMALIZED |
| Started | Datetime |
| Completed | Datetime |
| Duration | Computed |
| Students Processed | — |
| Triggered By | Role label |

---

## 5. Modals

### Publish Confirmation Modal (480px)

**Trigger:** [Approve & Publish] in drawer

Warning: `bg-[#042313] border-[#34D399]`

"You are about to publish results for **{Exam Name}** at **{Institution}**.

- **{N}** students will be able to see their scores immediately
- This action creates a permanent audit record
- Results can be withdrawn but cannot be unpublished instantly (institutions may already see them)"

[Institution name + scheduled publication timestamp]

**[Confirm & Publish]** `bg-[#6366F1]` · [Cancel]

### Withhold Results Modal (480px)

**Trigger:** [Withhold Results] in drawer or table

| Field | Required | Notes |
|---|---|---|
| Withhold Reason | Yes | Text area |
| Integrity Hold Reference | No | Link to malpractice case if applicable |

**[Withhold]** `bg-[#EF4444]` → sets `exam_result_publication.status = WITHHELD` + `exam_schedule.integrity_hold = True` (if not already set). Notifies Integrity Officer (91) in-app. ⚠️ "Results withheld" toast 8s.

### Withdraw Published Results Modal (480px)

**Trigger:** [Withdraw] on published results row

"Withdrawing published results will immediately hide them from students and institution admins. Students who have already seen results cannot have their memory erased — this action only prevents further viewing."

| Field | Required |
|---|---|
| Withdrawal Reason | Yes |

**[Confirm Withdraw]** `bg-[#EF4444]` · [Cancel]

---

## 6. Data Model Reference

Full models in `div-f-pages-list.md`:
- `exam_result_computation` — computation job with Celery tracking
- `exam_result_publication` — publication state machine

**`exam_result`** (tenant schema — read by computation Celery task):
| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `exam_schedule_id` | FK → `exam_schedule` | — |
| `student_ref` | varchar(50) | Anonymised hash — DPDPA |
| `raw_score` | decimal | — |
| `percentage` | decimal | Computed |
| `rank` | int | Nullable — set after rank computation |
| `percentile` | decimal | Nullable — set if method = PERCENTILE |
| `is_timed_out` | boolean | True if session expired without submission |
| `is_provisional` | boolean | Mirrors `exam_result_publication.is_provisional` |
| `created_at` | timestamptz | — |

**`exam_result_publication`** additions:
| Field | Type | Notes |
|---|---|---|
| `review_window_expires_at` | timestamptz | Computed on DRAFT: `exam_result_computation.completed_at + result_review_window_hours`. Nullable (NULL until computation completes). |

---

## 7. Access Control

| Gate | Rule |
|---|---|
| Page access | Results Coordinator (36), Ops Manager (34), Integrity Officer (91), Platform Admin (10) |
| Trigger computation | Results Coordinator (36), Platform Admin (10) |
| Review and approve | Results Coordinator (36) |
| Publish results | Results Coordinator (36), Platform Admin (10) |
| Withhold results | Results Coordinator (36), Integrity Officer (91), Ops Manager (34) — any can withhold |
| Withdraw published | Results Coordinator (36), Platform Admin (10) |
| Read-only | Ops Manager (34) — can see all, cannot publish |
| Integrity Officer | Can withhold; cannot publish or trigger computation |

---

## 8. Edge Cases & Error States

| Scenario | Behaviour |
|---|---|
| Computation fails (Celery error) | Status → FAILED. Error message stored in `exam_result_computation.error_message`. ❌ "Computation failed: {error}" persistent toast. [Retry Computation] button appears. |
| Publish while Celery down | `celery.app.control.ping()` check before publish. If timeout: ❌ "Cannot publish — Celery workers unreachable. Contact DevOps." |
| Integrity hold placed after computation | Results computed correctly. [Approve & Publish] blocked. Banner: "Integrity hold placed after computation. Results are ready but publication is blocked." |
| Two coordinators review same result simultaneously | Optimistic concurrency: last review sign-off wins. Drawer shows "Last reviewed by {role} at {time}". Warning if another session has the drawer open. |
| Submission count = 0 (all timed out) | Validation check shows ⚠️ "No submitted responses — all sessions timed out. Computation will generate zero-score records." Coordinator must explicitly acknowledge before proceeding. |
| Result withdrawal after institution has exported | Withdrawal hides the portal view. Exported PDFs are on institution's side — withdrawal does NOT recall them. Warning in Withdraw Modal: "Downloaded exports cannot be recalled." |

---

## 9. UI Patterns

### Toasts

| Action | Toast |
|---|---|
| Computation started | ℹ️ "Computation queued — Celery task started" (6s) |
| Computation complete | ✅ "Results computed — {N} students processed" (4s) |
| Marked reviewed | ✅ "Results marked as reviewed" (4s) |
| Results published | ✅ "Results published — {N} students notified" (4s) |
| Results withheld | ⚠️ "Results withheld" (8s) |
| Computation failed | ❌ "Computation failed: {error}" (persistent) |

### Responsive

| Breakpoint | Behaviour |
|---|---|
| Desktop (≥1280px) | Full table; drawer 760px; score chart full-width |
| Tablet | Reduced table columns; drawer full-width |
| Mobile | Card layout; drawer full-screen |

---

*Page spec complete.*
*F-04 covers: computation queue (submission rate guidance) → computation config (cross-institution rank validation) → live progress (cancel idempotency) → review (anomaly detection, sample min(20,N), review_window_expires_at, integrity hold after compute workflow) → approve + publish gate → withhold/withdraw.*
