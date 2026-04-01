# F-07 — Exam Integrity Dashboard

> **Route:** `/ops/exam/integrity/`
> **Division:** F — Exam Day Operations
> **Primary Role:** Exam Integrity Officer (91) — full control
> **Supporting Roles:** Results Coordinator (36) — read + result withhold coordination; Exam Operations Manager (34) — read; Platform Admin (10) — full
> **File:** `f-07-exam-integrity.md`
> **Priority:** P1 — Post-exam and ongoing; high-stakes legal consequences if cases mishandled

---

## 1. Page Name & Route

**Page Name:** Exam Integrity Dashboard
**Route:** `/ops/exam/integrity/`
**Part-load routes:**
- `/ops/exam/integrity/?part=kpi` — KPI strip
- `/ops/exam/integrity/?part=flags-table` — integrity flags tab
- `/ops/exam/integrity/?part=cases-table` — malpractice cases tab
- `/ops/exam/integrity/?part=statistical-analysis` — statistical analysis tab
- `/ops/exam/integrity/?part=institution-report` — institution report tab
- `/ops/exam/integrity/?part=flag-drawer&id={id}` — flag review drawer
- `/ops/exam/integrity/?part=case-drawer&id={id}` — case management drawer

---

## 2. Purpose

F-07 gives the Exam Integrity Officer (91) a systematic view of potential malpractice across all exams. It combines:

1. **Proctoring flags** — auto-detected anomalies (tab switches, copy-paste, IP sharing) collected during exam sessions
2. **Statistical analysis** — post-exam mathematical detection of answer-sharing patterns, unusual score jumps, and IP-based clustering
3. **Case management** — formal malpractice cases that may involve result withholding, institution notification, and legal referral
4. **Institution integrity reports** — per-institution history of flags and cases

**DPDPA critical:** This page deals with data about student behaviour. No student names are ever stored or displayed — only anonymised session references. Case descriptions reference cohort-level patterns, not individuals.

**Legal context:**
- Confirmed malpractice cases → institution warned + result withheld
- CRITICAL cases (paper leak, mass copying) → legal team (Div N) referral
- All case actions are permanently logged for audit

---

## 3. Tabs

| Tab | Label |
|---|---|
| 1 | Integrity Flags |
| 2 | Malpractice Cases |
| 3 | Statistical Analysis |
| 4 | Institution Reports |

---

## 4. Section-Wise Detailed Breakdown

---

### KPI Strip

| # | KPI | Alert |
|---|---|---|
| 1 | New Flags (unreviewed) | Amber if > 0; Red if any HIGH severity |
| 2 | Open Cases | Count of OPEN + UNDER_INVESTIGATION; amber if > 0 |
| 3 | Critical Cases | CRITICAL severity open cases; red pulsing if > 0 |
| 4 | Legal Escalated | COUNT where `status = LEGAL_ESCALATED`; for tracking |
| 5 | Institutions with Active Cases | Distinct institution count |
| 6 | Results on Hold (Integrity) | COUNT where `exam_schedule.integrity_hold = True`; red if > 0 |

---

### Tab 1 — Integrity Flags

All proctoring flags across all exams. Volume can be high — a single 74K exam may generate thousands of LOW-severity flags (tab switches are common and mostly benign).

#### Filter Bar (critical for triage)

| Filter | Control |
|---|---|
| Severity | Multi-select: High · Medium · Low |
| Flag Type | Multi-select: Tab Switch · Copy Paste · Multiple Face · Screen Capture · IP Sharing · Answer Pattern Anomaly · Submit Time Anomaly · Unusual Accuracy Jump · Proctor Manual Flag |
| Status | Multi-select: New · Under Review · Escalated to Case · Dismissed · Confirmed |
| Exam | Searchable select |
| Institution | Searchable select |
| Auto-detected | Toggle: Auto · Manual · Both |
| Date Range | Flag created at |
| Min Flag Count | Number (filter out low count flags) — default shows flag_count ≥ 3 |

**Default view:** Severity = HIGH + MEDIUM; Status = NEW; Min Flag Count = 3. This filters out noise and surfaces actionable flags.

#### Flags Table

| Column | Sortable | Notes |
|---|---|---|
| Exam | Yes | — |
| Institution | Yes | — |
| Flag Type | No | — |
| Severity | Yes (default: DESC) | CRITICAL > HIGH > MEDIUM > LOW |
| Flag Count | Yes | How many times this flag occurred for this session |
| Session Ref | No | Anonymised hash — NOT a student name |
| Auto-detected | No | System or Manual badge |
| Status | No | Status pill |
| Created At | Yes | — |
| Actions | — | [Review] · [Dismiss] · [Escalate to Case] |

**[Review]:** opens Flag Review Drawer (640px).

**[Dismiss]:** one-click with required reason. Sets status = DISMISSED. ✅ "Flag dismissed" toast.

**[Escalate to Case]:** opens Create Malpractice Case Modal (links flag to a case).

**Bulk actions:** Select multiple flags → [Bulk Dismiss] · [Bulk Escalate to Case]

**Auto-escalation indicator:** Flags auto-escalated by Celery (flag_count ≥ threshold) show `[Auto-escalated]` badge. Integrity Officer reviews the resulting case in Tab 2.

**Auto-escalation deduplication:** Before creating a new auto-escalated case, the `analyze_exam_integrity` Celery task checks for an existing OPEN or UNDER_INVESTIGATION case with the **exact same** `(exam_schedule_id, institution_id, case_type)` — string-matched precisely. A MASS_COPYING case and a PAPER_LEAK case for the same exam/institution are **separate** (different case_type). If one matching open case exists: flags appended, log entry added "Additional flags auto-linked by system." Only if no exact match found is a new `FMC-` case created. If Integrity Officer believes two different-type cases are related, they can manually link flags between cases using [Link More Flags].

---

### Flag Review Drawer (640px)

**Header:** Flag type + Session ref + Severity pill + Status pill + [×]

#### Section A — Flag Details

| Field | Notes |
|---|---|
| Exam | Exam name + institution |
| Session Reference | Anonymised hash |
| Flag Type | Human-readable label |
| Flag Count | How many times detected |
| Severity | AUTO-computed based on type + count |
| Auto-detected | Yes / No |
| First Detected | Datetime |
| Last Detected | Datetime |

#### Section B — Flag Type Context

For each flag type, a fixed explanation of what this flag means and its typical false-positive rate:

| Flag Type | What It Means | Typical FP Rate |
|---|---|---|
| TAB_SWITCH | Student navigated away from exam tab | High (50–70%) — often accidental or notification |
| COPY_PASTE | Ctrl+C or Ctrl+V detected in exam | Medium (30%) — may be answer pasting |
| MULTIPLE_FACE_DETECTED | AI webcam detected > 1 face in frame | Medium (25%) — may be family members nearby |
| IP_SHARING | Same IP as another session in same exam | Low (5%) — strong malpractice signal |
| ANSWER_PATTERN_ANOMALY | Statistical deviation from expected answer distribution | Low (10%) — most reliable auto-flag |
| SUBMIT_TIME_ANOMALY | Submitted within {N} seconds of exam start | Low (8%) — may indicate pre-prepared answers |

**Note:** "Typical FP rate" is shown to guide review — a high FP rate means Dismiss is appropriate for single occurrences; escalate only when other flags corroborate.

#### Section C — Review Decision

| Field | Required | Notes |
|---|---|---|
| Decision | Yes | Radio: DISMISS · CONFIRM · ESCALATE TO CASE |
| Review Notes | Yes | Min 20 chars |

**[Submit Review]** → sets status accordingly. If ESCALATE TO CASE: opens Create Malpractice Case Modal.

---

### Tab 2 — Malpractice Cases

Formal cases opened and tracked to closure.

#### Filter Bar

| Filter | Control |
|---|---|
| Status | Multi-select: Open · Under Investigation · Legal Escalated · Institution Notified · Closed Confirmed · Closed Dismissed |
| Case Type | Multi-select |
| Severity | Multi-select |
| Institution | Searchable select |
| Date Range | Created at |
| Assigned To | Me / All |

#### Cases Table

| Column | Sortable | Notes |
|---|---|---|
| Case ID | No | Format: `FMC-{YYYYMMDD}-{seq}` — e.g. `FMC-20260315-0001`; seq is 4-digit daily counter |
| Case Type | No | — |
| Exam | Yes | — |
| Institution | Yes | — |
| Severity | Yes (default: DESC) | — |
| Affected Students (est.) | No | DPDPA: count only |
| Anomaly Score | No | Statistical score if available |
| Result Hold | No | 🔒 if hold active |
| Status | No | Status pill |
| Assigned To | No | Role label |
| Created At | Yes | — |
| Actions | — | [Open Case] · [Notify Institution] · [Legal Escalate] · [Close] |

**[+ New Case]** (header button): opens Create Case Modal.

---

### Malpractice Case Drawer (760px)

**Header:** Case ID + Severity pill + Status pill + [×]

#### Drawer Tab 1 — Case Details

| Field | Read/Edit | Notes |
|---|---|---|
| Case Type | Editable | — |
| Severity | Editable | Can be upgraded |
| Exam | Read-only | — |
| Institution | Read-only | — |
| Description | Editable | Full case description |
| Evidence Summary | Editable | Summary of evidence |
| Statistical Anomaly Score | Read-only | Computed score; nullable |
| Affected Student Count (est.) | Editable | Number estimate — no names |
| Result Hold | Read-only | Shows 🔒 if `exam_schedule.integrity_hold = True` |

**[Place Result Hold]:** visible when `integrity_hold = False`. Opens Place Hold Modal. Dual approval required: Integrity Officer (91) + Ops Manager (34). See Section 5.

**[Lift Result Hold]:** visible when `integrity_hold = True`. Opens Lift Hold Modal. Same dual approval.

#### Drawer Tab 2 — Linked Flags

List of `exam_integrity_flag` records escalated to this case.

| Column | Notes |
|---|---|
| Session Ref | Anonymised |
| Flag Type | — |
| Flag Count | — |
| Severity | — |
| Reviewed At | — |

**[Link More Flags]:** searchable flag list (from same exam/institution). Adds flags to this case.

#### Drawer Tab 3 — Status Workflow

Visual status progression:

```
OPEN → UNDER_INVESTIGATION → INSTITUTION_NOTIFIED / LEGAL_ESCALATED → CLOSED_CONFIRMED / CLOSED_DISMISSED
```

**Status transition controls:**

| Transition | Button | Requirements |
|---|---|---|
| → UNDER_INVESTIGATION | [Begin Investigation] | Case has description + at least 1 linked flag |
| → INSTITUTION_NOTIFIED | [Notify Institution] | Sends notification; logs `institution_notified_at` |
| → LEGAL_ESCALATED | [Escalate to Legal] | Opens Legal Escalation Modal |
| → CLOSED_CONFIRMED | [Close — Confirmed] | Requires closure notes |
| → CLOSED_DISMISSED | [Close — Dismissed] | Requires dismissal notes |

**[Notify Institution]:** opens confirmation modal before sending: "Notify institution of malpractice case #{case_id} for exam {exam}? This sends an in-app notification to institution admin (and optional WhatsApp broadcast). **Once sent, notification cannot be unsent.** Confirm?" [Notify] `bg-[#EF4444]` · [Cancel]. On confirm: sets `case.status → INSTITUTION_NOTIFIED`, `institution_notified_at = now()`, sends in-app + optional F-06 broadcast. DPDPA: notification text uses role labels and case type only — no student names.

#### Drawer Tab 4 — Activity Log

Timeline of all case status changes, notes, and actions. Read-only.

**[+ Add Investigation Note]:** appends note to log. Internal only. Max 1000 chars.

---

### Tab 3 — Statistical Analysis

The primary tool for post-exam malpractice detection. Integrity Officer runs analysis after result computation.

#### Analysis Selector

**Select Exam:** Searchable dropdown (only exams with completed result computation available).

**[Run Analysis]** → triggers `analyze_exam_integrity` Celery task. Shows progress.

#### Analysis Results (displayed after task completes)

**Section A — IP Address Clustering**

| Metric | Value |
|---|---|
| Unique IPs detected | {N} |
| Shared IPs (>1 session per IP) | {N} IPs shared |
| Max sessions per IP | {N} (highest concentration) |

Table: IP group → session count → percentage answered identically. Sessions sharing an IP AND having >80% identical answers = high anomaly score.

**DPDPA:** IP addresses are hashed for display using SHA-256, shown as first 6 hex chars: `IP-HASH-{6chars}`. Collision probability at 74K concurrent sessions is negligible. Full unhashed IPs visible only to Platform Admin (10) via raw data export. All other roles see hashed display only.

**CRITICAL flag min count override:** Default filter `Min Flag Count = 3` is overridden for CRITICAL severity — all CRITICAL flags are shown regardless of flag count, even single occurrences. This prevents a single high-impact anomaly (e.g., exam submitted in 5 seconds) from being filtered out by the noise-reduction default.

**Section B — Answer Similarity Analysis**

For each question, percentage of sessions that selected each option:

`BarChart` — expected: answer options should follow a distribution. A single option chosen by >90% of students = question is too easy OR systematic answer sharing.

**Anomalous question list:** Questions where >85% chose same answer AND the D-09 tagged difficulty is MEDIUM or HARD (legitimately EASY questions tagged as such in D-09 are suppressed — high agreement on an easy question is expected and not anomalous). If D-09 metadata is unavailable, threshold is applied without the difficulty filter. Coordinator can adjust the anomaly detection threshold (default 85%) in F-09 Integrity Defaults.

**Section C — Submit Time Distribution**

`HistogramChart` — distribution of submission times (time from exam start to submission).

Normal distribution expected. Anomalous peaks:
- Very early submissions (<10% of exam duration): pre-prepared answers
- Clustered submissions at identical timestamps: possible answer-sharing coordination

**Section D — Score Correlation by Institution**

Scatter plot: institution average score vs. institution flag count. Expected: no correlation. If high score + high flags: integrity concern.

**[Generate Report PDF]:** Generates a structured integrity report PDF for this exam. Used for legal escalation documentation. Contains all statistical analysis + flag summary. No student names — session refs only.

---

### Tab 4 — Institution Reports

Per-institution integrity track record across all exams.

#### Institution Selector

Searchable dropdown. Shows all institutions that have any flag history.

#### Institution Integrity Summary

| Metric | Value |
|---|---|
| Total exams taken | {N} |
| Exams with flags | {N} ({X}%) |
| Total flags generated | {N} |
| Flags per exam (avg) | {X} |
| Cases opened | {N} |
| Cases confirmed | {N} |
| Legal escalations | {N} |
| Current result holds | {N} |

**Trend chart:** flags per exam over time (last 24 months). Identifies escalating or improving institutions.

**Cases list:** All cases for this institution with status + outcome.

**[Export Institution Report PDF]:** Used for institution-facing communication or legal documentation.

---

## 5. Modals

### Create Malpractice Case Modal (560px)

| Field | Required | Notes |
|---|---|---|
| Exam Schedule | Yes | Searchable select |
| Case Type | Yes | Select |
| Severity | Yes | Select |
| Description | Yes | Text area; min 50 chars |
| Affected Student Count (estimate) | No | Number — no names |
| Link Flags | No | Multi-select from flags on this exam |
| Anomaly Score | No | Number 0–100 (from statistical analysis) |

**[Create Case]** → `exam_malpractice_case` created with ID format `FMC-{YYYYMMDD}-{seq}` (e.g. `FMC-20260315-0001`). ✅ "Malpractice case opened — FMC-{ref}" toast 4s. Assigned to Integrity Officer (91).

**Deduplication check on manual create:** Before opening, system checks for an existing OPEN or UNDER_INVESTIGATION case with the same `(exam_schedule_id, institution_id, case_type)`. If found, a warning is shown: "An open case already exists for this exam, institution, and type: FMC-{ref}. Link flags to the existing case instead?" — with buttons [Open Existing Case] · [Create New Case Anyway].

### Place Result Hold Modal (480px) — Dual Approval Required

**Step 1 (Integrity Officer 91):**

"Place an integrity hold on results for **{Exam}** at **{Institution}**?

- Results will NOT be publishable until hold is cleared
- Institution will NOT be notified automatically (you choose when to notify)
- This action requires confirmation from the Exam Operations Manager"

| Field | Required |
|---|---|
| Hold Reason | Yes |
| Case Reference | Yes (links to malpractice case) |

**[Submit Hold Request]** → sets `integrity_hold_requested = True`. Sends in-app notification to Exam Ops Manager (34) for approval.

**Step 2 (Ops Manager 34 — separate session or confirmation request):**

"Integrity Officer has requested a result hold for **{Exam}** at **{Institution}**.
Reason: {reason}"

[Approve Hold] `bg-[#EF4444]` · [Reject Hold Request] → with rejection reason

**On dual approval:** `exam_schedule.integrity_hold = True`. Both actors logged. ⚠️ "Result hold placed" toast 8s.

**Hold rejection loop prevention:** If Ops Manager rejects a hold request: Integrity Officer notified in-app with rejection reason. Can resubmit immediately with a modified reason, or after 1 hour with the same reason. If resubmitting within 1 hour with an identical reason: Ops Manager sees "Re-submitted after earlier rejection — reason unchanged." After 3 rejections of the same case within 24 hours, further hold requests for that case require Platform Admin (10) approval rather than Ops Manager.

### Legal Escalation Modal (560px)

| Field | Required | Notes |
|---|---|---|
| Legal Escalation Type | Yes | Select: Formal Complaint · FIR Guidance · Civil Recovery · Police Referral |
| Escalation Summary | Yes | Text area |
| Evidence Attached | No | Upload S3 document |
| Legal Officer Contact | Pre-filled | Division N Legal Officer (75) in-app notification |

**[Escalate to Legal]** → sets `status = LEGAL_ESCALATED`, `legal_referred_at` = now. Sends in-app notification to Legal Officer (Div N, Role 75). ⚠️ "Case escalated to Legal team" toast 8s.

---

## 6. Data Model Reference

Full models in `div-f-pages-list.md`:
- `exam_integrity_flag` — per-session proctoring flags
- `exam_malpractice_case` — case records

**`exam_integrity_analysis`** (F-07 Tab 3 — analysis results):
| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `exam_schedule_id` | FK → `exam_schedule` | — |
| `analysis_type` | varchar | Enum: `IP_CLUSTERING` · `ANSWER_SIMILARITY` · `SUBMIT_TIME` · `SCORE_CORRELATION` |
| `results_data` | jsonb | Analysis output — structured per type |
| `overall_anomaly_score` | decimal | 0–100; combined score |
| `run_at` | timestamptz | — |
| `celery_task_id` | varchar(50) | — |
| `status` | varchar | Enum: `RUNNING` · `COMPLETED` · `FAILED` |

---

## 7. Access Control

| Gate | Rule |
|---|---|
| Page access | Integrity Officer (91), Results Coordinator (36), Ops Manager (34), Platform Admin (10) |
| Review flags | Integrity Officer (91), Platform Admin (10) |
| Create/manage cases | Integrity Officer (91), Platform Admin (10) |
| Place result hold (Step 1) | Integrity Officer (91) |
| Approve result hold (Step 2) | Ops Manager (34), Platform Admin (10) |
| Run statistical analysis | Integrity Officer (91), Platform Admin (10) |
| Legal escalation | Integrity Officer (91) only |
| Read-only | Results Coordinator (36), Ops Manager (34) |
| Full IP hash visibility | Platform Admin (10) only — all others see hashed IPs |

---

## 8. Edge Cases & Error States

| Scenario | Behaviour |
|---|---|
| Statistical analysis run on exam with < 10 submissions | Warning: "Insufficient data for reliable analysis ({N} submissions). Results may not be statistically meaningful." — analysis still runs. |
| Auto-escalated case (Celery) with no active Integrity Officer session | Case created in OPEN state. In-app notification sent to Integrity Officer (91). Celery task logged. |
| Dual approval: Ops Manager rejects hold request | Hold NOT placed. Integrity Officer notified. Case status unchanged. Rejection reason logged. |
| Legal escalation: Legal Officer (75) unreachable | In-app notification sent (not email). Case status = LEGAL_ESCALATED regardless. Legal team responsible for picking up in-app notifications. |
| Flag bulk-dismissed (e.g., 5,000 LOW flags after exam) | Bulk dismiss allowed in batches of 200. Each batch requires reason. Celery background task processes bulk dismiss asynchronously. |
| Case opened for exam with published results | Can still open case. Result withhold can be placed AFTER publish — `exam_result_publication.status → WITHHELD`. Institution will see results disappear. Warning in modal: "Results are already published to {N} students. Withholding will hide them immediately." |

---

## 9. UI Patterns

### Toasts

| Action | Toast |
|---|---|
| Flag dismissed | ✅ "Flag dismissed" (4s) |
| Flag escalated to case | ✅ "Flag escalated — case #{ref} created" (4s) |
| Case created | ✅ "Malpractice case opened — #{ref}" (4s) |
| Institution notified | ✅ "Institution notified in-app" (4s) |
| Result hold placed | ⚠️ "Result hold placed — results blocked from publication" (8s) |
| Hold lifted | ✅ "Result hold lifted — publication unblocked" (4s) |
| Case legally escalated | ⚠️ "Case escalated to Legal team (Div N)" (8s) |
| Analysis complete | ✅ "Statistical analysis complete — anomaly score: {N}/100" (4s) |

### Responsive

| Breakpoint | Behaviour |
|---|---|
| Desktop (≥1280px) | Full table; case drawer 760px; analysis charts full-width |
| Tablet | Reduced table; drawer full-width; charts stacked |
| Mobile | Card layout; drawer full-screen; simplified analysis (key metrics only, no charts) |

---

*Page spec complete.*
*F-07 covers: proctoring flag triage → malpractice case management → statistical analysis (IP clustering, answer similarity, submit time) → institution integrity reports → result hold (dual approval) → legal escalation.*
