# Division F — Exam Day Operations: Pages List

> **Division:** F — Exam Day Operations
> **Roles:** Exam Operations Manager (34) · Exam Support Executive (35) · Results Coordinator (36) · Notification Manager (37) · Incident Manager — Exam Day (38) · Exam Configuration Specialist (90) · Exam Integrity Officer (91) · OMR Processing Specialist (109)
> **Cross-access:** Content Director (18) read on F-08 Analytics · Analytics Manager (42) read on F-08 · Platform Admin (10) full access all pages · Exam Operations Manager (34) full access all F pages · DevOps/SRE (14) read-only on F-02
> **Total pages:** 11
> **Scale:** 2,050 institutions · 2.4M–7.6M students · 74,000 peak concurrent submissions
> **Peak exam load:** Up to 300 simultaneous exam schedules active across all institutions on a single national exam day

**Critical context:**
One misconfigured exam at 74,000 concurrent — negative marking factor wrong, wrong question paper assigned, start time off — affects all students simultaneously. A results coordinator who publishes unchecked ranks affects institution reputations. This division owns the most irreversible actions on the platform.

---

## Scale Context

| Segment | Institutions | Students (avg) | Peak concurrent |
|---|---|---|---|
| Schools | 1,000 | 1,000 | — |
| Colleges | 800 | 500 | — |
| Coaching Centres | 100 | 10,000 | Most of peak load |
| **Total** | **2,050** | — | **74,000 simultaneous submissions** |

**Exam load profile:**
- 6 primary exam domains: SSC · RRB · NEET · JEE · AP Board · TS Board
- Additional domains: IBPS · SBI · State PSC
- ~800+ active test series across all institutions
- 2M+ questions in bank
- Typical national exam day: 40–80 institutions running the same exam simultaneously
- Submission surge window: final 10 minutes before exam close — 60–70% of total submissions arrive in this window

---

## Roles

| # | Role | Level | Division Scope |
|---|---|---|---|
| 34 | Exam Operations Manager | 3 | Owns live exam monitoring, exam-day decisions, pause/extend authority |
| 35 | Exam Support Executive | 3 | First-response support for student/institution issues during live exams |
| 36 | Results Coordinator | 3 | Result computation trigger, review, and publish authority |
| 37 | Notification Manager | 3 | WhatsApp/SMS/Email template management, broadcast sends |
| 38 | Incident Manager — Exam Day | 4 | Infrastructure escalation, war room coordination, emergency scaling |
| 90 | Exam Configuration Specialist | 3 | Pre-exam setup: timing, question papers, scoring rules, institution configs |
| 91 | Exam Integrity Officer | 3 | Malpractice detection, proctor flag review, case management, legal escalation |
| 109 | OMR Processing Specialist | 3 | Design OMR templates · configure scan pipelines · QA ambiguous marks · integrate OMR results with F-04 · train institutions on OMR workflow |

**Note:** Role 109 (OMR Processing Specialist) was added 2026-03-26 to cover the large cohort of Indian schools and coaching centres that conduct OMR-based assessments alongside or instead of digital exams.

---

## Pages

| Page | Name | Route | File | Priority |
|---|---|---|---|---|
| F-01 | Exam Schedule & Configuration | `/ops/exam/schedule/` | `f-01-exam-schedule.md` | P0 |
| F-02 | Live Exam Monitor | `/ops/exam/monitor/` | `f-02-live-exam-monitor.md` | P0 |
| F-03 | Exam Support Console | `/ops/exam/support/` | `f-03-exam-support-console.md` | P0 |
| F-04 | Results Management | `/ops/exam/results/` | `f-04-results-management.md` | P0 |
| F-05 | Answer Key & Objections | `/ops/exam/answer-key/` | `f-05-answer-key-management.md` | P1 |
| F-06 | Notification Hub | `/ops/exam/notifications/` | `f-06-notification-hub.md` | P1 |
| F-07 | Exam Integrity Dashboard | `/ops/exam/integrity/` | `f-07-exam-integrity.md` | P1 |
| F-08 | Exam Analytics | `/ops/exam/analytics/` | `f-08-exam-analytics.md` | P2 |
| F-09 | Division Config | `/ops/exam/config/` | `f-09-division-config.md` | P2 |
| F-10 | OMR Sheet Processing | `/ops/exam/omr/` | `f-10-omr-sheet-processing.md` | P1 |
| F-11 | Offline Exam Manager | `/ops/exam/offline/` | `f-11-offline-exam-manager.md` | P1 |

---

## Role-to-Page Access Matrix

| Role | F-01 Schedule | F-02 Monitor | F-03 Support | F-04 Results | F-05 Answer Key | F-06 Notifications | F-07 Integrity | F-08 Analytics | F-09 Config | F-10 OMR | F-11 Offline |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Exam Ops Manager (34) | Read + approve lock/unlock | **Full** + pause/extend | Read + escalate | Read + approve | Read + approve | Read | Read | Read | **Full** | Read + approve | Read + approve |
| Exam Support Exec (35) | Read | Read + incident create | **Full** | — | — | — | Read | — | — | — | Read |
| Results Coordinator (36) | Read | Read | Read | **Full** | **Full** | Read + send result broadcasts | Read (integrity summary) | Read | — | Read (results integration) | Read (offline results) |
| Notification Manager (37) | Read | Read | — | Read | — | **Full** | — | Read | — | — | — |
| Incident Manager (38) | Read | Read + infra escalation | Read | — | — | — | — | — | — | — | — |
| Exam Config Specialist (90) | **Full** | Read | — | — | Read | — | — | Read | — | Read + configure | **Full** |
| Exam Integrity Officer (91) | Read | Read | Read | Read | Read (for integrity holds) | — | **Full** | Read | — | Read | Read |
| OMR Specialist (109) | Read | — | — | — | — | — | — | Read | — | **Full** | — |
| Platform Admin (10) | Full | Full | Full | Full | Full | Full | Full | Full | Full | Full | Full |
| DevOps/SRE (14) | — | Read-only | — | — | — | — | — | — | — | — | — |
| Content Director (18) | — | — | — | — | — | — | — | Read | — | — | — |
| Analytics Manager (42) | — | — | — | — | — | — | — | Read | — | Read | Read |

---

## Division F — Critical Action Ownership

| Action | Owner | Gate |
|---|---|---|
| Lock exam config (no more changes) | Exam Config Specialist (90) | At T-24h before scheduled start |
| Pause running exam for all tenants | Exam Operations Manager (34) | Requires confirmation modal + reason |
| Extend exam duration per institution | Exam Operations Manager (34) | Per institution; logged |
| Trigger result computation | Results Coordinator (36) | Manual — not automatic |
| Approve result publication | Results Coordinator (36) | After review sign-off |
| Publish answer key | Results Coordinator (36) | After internal review |
| Accept/reject objection | Results Coordinator (36) | Per objection |
| Send bulk 74K notifications | Notification Manager (37) | Broadcast preview + confirm |
| Open malpractice case | Exam Integrity Officer (91) | After flag review |
| Withhold institution result (integrity hold) | Exam Integrity Officer (91) + Exam Ops Manager (34) | Dual approval |
| Emergency Lambda scale-up | Incident Manager (38) | Triggers DevOps alert; logged |

---

## Integration Points — Division F

| Integration | Direction | What Flows |
|---|---|---|
| **Div A — War Room (32)** | F-02 → A-32 | F-02 raises operational incidents; critical incidents escalate to War Room. F-02 does NOT see infra gauges — those are in War Room. War Room can see live exam session counts from shared `exam_ops_snapshot`. |
| **Div B — Exam Domain Config (09)** | B-09 → F-01 | Exam domain definitions, test series structure feed into F-01 scheduling |
| **Div B — Test Series Manager (11)** | B-11 → F-01 | Test series schedules drive batch exam creation in F-01 |
| **Div C — Engineering** | F ops → C | Incident Manager (38) escalates infra incidents to DevOps. C maintains Lambda auto-scaling, RDS, notification delivery infrastructure. |
| **Div D — Published Question Bank** | D-11 → F-01 | Question papers assembled from published MCQs |
| **Div H — Data & Analytics** | F-04, F-08 → H | Result data flows to H for platform-wide analytics, MIS reports |
| **Div I — Customer Support** | F-03 ↔ I | Post-exam support tickets from L1/L2 escalated to F-03 during exam window; after exam ends, tickets hand back to Div I |
| **WhatsApp Business API (Meta)** | F-06 → Meta | Bulk notifications via approved templates; DLT sender ID `EDUFGE` (TRAI registered) |
| **SMS Gateway (DLT)** | F-06 → SMS Gateway | SMS via Vonage/Twilio with TRAI DLT pre-registered templates; sender ID `EDUFGE` |
| **Razorpay (webhook)** | External → F-06 | Payment confirmation triggers exam access notification (handled by F-06 template) |
| **AWS EventBridge** | Tenant sessions → H | Exam session events stream to H for real-time aggregation |

---

## Data Models — Division F (Shared Reference)

All Division F models live in the **shared schema** (`ops` app). Tenant-specific exam sessions (`exam_session`, `exam_submission`) live in tenant schemas and are read by F-02/F-04 via aggregation views.

---

### `exam_schedule`

The central record linking a platform exam to a specific institution with timing and config.

| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `exam_id` | FK → `exam_exam` | Platform-wide exam definition (title, subject, exam_type) |
| `institution_id` | int | Institution reference |
| `institution_type` | varchar | Enum: `SCHOOL` · `COLLEGE` · `COACHING` · `ONLINE_DOMAIN` |
| `paper_id` | FK → `exam_question_paper` | Nullable — assigned by Exam Config Specialist (90) |
| `scheduled_start` | timestamptz | Absolute UTC datetime |
| `scheduled_end` | timestamptz | Derived: start + duration; overrideable by Ops Manager |
| `actual_start` | timestamptz | Nullable — set when first student session created |
| `actual_end` | timestamptz | Nullable — set when exam is closed/completed |
| `duration_minutes` | int | Overrides exam template default if set |
| `grace_period_minutes` | int | Default from `exam_operational_config`; institution-specific override |
| `status` | varchar | Enum: `DRAFT` · `CONFIG_LOCKED` · `SCHEDULED` · `ACTIVE` · `PAUSED` · `COMPLETED` · `CANCELLED` · `RESCHEDULED` |
| `negative_marking_factor` | decimal | Default from template. e.g. `0.25` = lose 0.25 marks per wrong answer. `0` = no negative marking. |
| `max_attempts` | int | Default 1 |
| `registration_open_at` | timestamptz | Nullable — students can register from this time |
| `registration_close_at` | timestamptz | Nullable |
| `config_locked_at` | timestamptz | Nullable — set when Exam Config Specialist locks config |
| `config_locked_by_id` | FK → auth.User | Nullable |
| `pause_reason` | text | Nullable — set when Ops Manager pauses |
| `paused_by_id` | FK → auth.User | Nullable |
| `paused_at` | timestamptz | Nullable |
| `resumed_at` | timestamptz | Nullable — set when status transitions from PAUSED back to ACTIVE |
| `extended_by_minutes` | int | Default 0 — tracks cumulative extensions granted |
| `rescheduled_from_id` | FK → `exam_schedule` (self) | Nullable — set when this schedule is a reschedule of a previous one. Preserves student registration continuity. |
| `result_status` | varchar | Enum: `PENDING` · `COMPUTING` · `COMPUTED` · `REVIEWED` · `PUBLISHED` · `WITHHELD` |
| `integrity_hold` | boolean | Default False — set by Integrity Officer; blocks result publish |
| `created_by_id` | FK → auth.User | Exam Config Specialist or Ops Manager |
| `created_at` | timestamptz | — |
| `updated_at` | timestamptz | — |

---

### `exam_ops_snapshot`

Materialized aggregation of live exam state per schedule, updated by Celery Beat every 30s during active exam windows.

| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `exam_schedule_id` | FK → `exam_schedule` | OneToOne |
| `institution_id` | int | Denormalised for fast filtering |
| `total_registered` | int | Students registered for this exam instance |
| `total_started` | int | Sessions created (student clicked Start) |
| `total_submitted` | int | Final submissions received |
| `total_active_sessions` | int | `started - submitted - expired` |
| `total_timed_out` | int | Sessions that expired without submission |
| `submit_error_count` | int | Submission failures in current window |
| `last_submit_rate_per_min` | int | Rolling 5-min average submissions/min |
| `open_incident_count` | int | Unresolved support tickets for this exam |
| `last_snapshot_at` | timestamptz | When this row was last updated by Celery |
| `snapshot_source` | varchar | Enum: `CELERY_BEAT` · `MANUAL_REFRESH` |

**Snapshot strategy:** Celery Beat task `update_exam_ops_snapshots` runs every 30s. It queries each active exam's tenant schema for session counts and writes to this table. F-02 HTMX polls `?part=monitor-grid` every 30s, reading from this table — never hitting tenant schemas directly from the web request.

---

### `exam_session_incident`

Operational incidents raised during a live exam window.

| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `exam_schedule_id` | FK → `exam_schedule` | — |
| `institution_id` | int | — |
| `incident_type` | varchar | Enum: `STUCK_SESSION` · `SUBMIT_FAILURE` · `AUTH_FAILURE` · `CONNECTIVITY_DROP` · `QUESTION_DISPLAY_ERROR` · `TIMER_MISMATCH` · `OTHER` |
| `severity` | varchar | Enum: `LOW` · `MEDIUM` · `HIGH` · `CRITICAL` |
| `affected_student_count` | int | Estimated count — DPDPA: no individual names |
| `description` | text | — |
| `reported_by_id` | FK → auth.User | Support Exec (35) or Ops Manager (34) |
| `assigned_to_id` | FK → auth.User | Nullable |
| `status` | varchar | Enum: `OPEN` · `IN_PROGRESS` · `ESCALATED_TO_DEVOPS` · `RESOLVED` · `CLOSED` |
| `resolution` | text | Nullable |
| `devops_ticket_ref` | varchar(50) | Nullable — external reference if escalated |
| `created_at` | timestamptz | — |
| `resolved_at` | timestamptz | Nullable |

---

### `exam_ops_action_log`

Immutable log of all operational actions taken on exam schedules (pause, extend, config lock, etc.).

| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `exam_schedule_id` | FK → `exam_schedule` | — |
| `action_type` | varchar | Enum: `PAUSE` · `RESUME` · `EXTEND_DURATION` · `CONFIG_LOCK` · `CONFIG_UNLOCK` · `FORCE_CLOSE` · `RESULT_WITHHOLD` · `RESULT_WITHHOLD_LIFT` · `CANCEL` · `RESCHEDULE` |
| `actor_id` | FK → auth.User | — |
| `actor_role` | varchar | Role label (DPDPA) |
| `details` | jsonb | Action-specific details (e.g. `{"extension_minutes": 15, "reason": "Server latency issue"}`) |
| `performed_at` | timestamptz | — |

---

### `exam_result_computation`

Tracks a result computation job for a completed exam.

| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `exam_schedule_id` | FK → `exam_schedule` | — |
| `status` | varchar | Enum: `PENDING` · `RUNNING` · `COMPLETED` · `FAILED` · `CANCELLED` |
| `triggered_by_id` | FK → auth.User | Results Coordinator (36) |
| `started_at` | timestamptz | Nullable |
| `completed_at` | timestamptz | Nullable |
| `celery_task_id` | varchar(50) | Nullable — for progress tracking |
| `total_students` | int | Total submissions processed |
| `computation_method` | varchar | Enum: `RAW_MARKS` · `PERCENTILE` · `NORMALIZED` |
| `normalization_applied` | boolean | Default False |
| `normalization_notes` | text | Nullable — notes if normalization was applied |
| `error_message` | text | Nullable — set on FAILED |
| `result_count` | int | Nullable — number of result records created on COMPLETED |

---

### `exam_result_publication`

Controls the publication state of a computed result set.

| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `exam_schedule_id` | FK → `exam_schedule` | OneToOne |
| `computation_id` | FK → `exam_result_computation` | Links to the computation used for this publication |
| `status` | varchar | Enum: `DRAFT` · `REVIEWED` · `APPROVED` · `PUBLISHED` · `WITHHELD` · `WITHDRAWN` |
| `reviewed_by_id` | FK → auth.User | Results Coordinator who reviewed |
| `reviewed_at` | timestamptz | Nullable |
| `approved_by_id` | FK → auth.User | Results Coordinator who approved |
| `approved_at` | timestamptz | Nullable |
| `published_at` | timestamptz | Nullable |
| `is_provisional` | boolean | Default False — provisional results shown with banner to institutions |
| `withdrawal_reason` | text | Nullable — reason if WITHDRAWN |
| `withheld_by_id` | FK → auth.User | Nullable — Integrity Officer or Results Coordinator |
| `withheld_reason` | text | Nullable |

---

### `exam_answer_key_publication`

Answer key publish state for an exam.

| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `exam_schedule_id` | FK → `exam_schedule` | — |
| `paper_id` | FK → `exam_question_paper` | — |
| `status` | varchar | Enum: `DRAFT` · `PROVISIONAL` · `FINAL` · `REVISED` |
| `published_at` | timestamptz | Nullable — when first published |
| `finalized_at` | timestamptz | Nullable — when marked FINAL (objection window closed) |
| `objection_window_close_at` | timestamptz | Nullable — after this, no new objections accepted |
| `published_by_id` | FK → auth.User | Results Coordinator (36) |
| `total_objections` | int | Computed field (count of related objections) |
| `accepted_objections` | int | Count of ACCEPTED objections |

---

### `exam_answer_key_objection`

An objection filed against a specific answer key entry (per question).

| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `answer_key_publication_id` | FK → `exam_answer_key_publication` | — |
| `institution_id` | int | Institution filing the objection |
| `question_number` | int | Question being objected to |
| `objection_type` | varchar | Enum: `WRONG_ANSWER` · `MULTIPLE_CORRECT` · `QUESTION_ERROR` · `IMAGE_ISSUE` · `LANGUAGE_ERROR` · `OTHER` |
| `description` | text | Objection reasoning |
| `supporting_doc_key` | varchar | Nullable — S3 key for attached document |
| `status` | varchar | Enum: `OPEN` · `UNDER_REVIEW` · `ACCEPTED` · `REJECTED` |
| `reviewed_by_id` | FK → auth.User | Results Coordinator (36) |
| `review_notes` | text | Nullable |
| `resolved_at` | timestamptz | Nullable |
| `created_at` | timestamptz | — |

---

### `exam_notification_template`

WhatsApp/SMS/Email notification templates (DLT pre-registered for SMS).

| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `template_code` | varchar(50) | Unique. Used in broadcasts. |
| `name` | varchar(100) | Display name |
| `channel` | varchar | Enum: `WHATSAPP` · `SMS` · `EMAIL` |
| `language` | varchar | Enum: `EN` · `HI` · `TE` · `UR` — default EN |
| `category` | varchar | Enum: `RESULT_RELEASE` · `EXAM_REMINDER` · `OTP` · `SCHEDULE_CHANGE` · `ADMIT_CARD` · `GENERAL_ANNOUNCEMENT` · `PAYMENT_CONFIRMATION` |
| `body_text` | text | Template with `{{variable}}` placeholders |
| `variable_list` | jsonb | Array of `{"key": "student_name", "description": "...", "example": "..."}` |
| `character_count` | int | Computed — for SMS 160-char limit planning |
| `dlt_template_id` | varchar(50) | Nullable — DLT registration ID (TRAI requirement for SMS) |
| `dlt_approved_at` | date | Nullable |
| `whatsapp_template_id` | varchar(50) | Nullable — Meta Business API template ID |
| `whatsapp_approved_at` | date | Nullable |
| `status` | varchar | Enum: `DRAFT` · `PENDING_APPROVAL` · `APPROVED` · `ACTIVE` · `ARCHIVED` |
| `approved_by_id` | FK → auth.User | Notification Manager (37) |
| `created_by_id` | FK → auth.User | — |
| `created_at` | timestamptz | — |

---

### `exam_notification_broadcast`

A single bulk notification send event.

| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `template_id` | FK → `exam_notification_template` | — |
| `exam_schedule_id` | FK → `exam_schedule` | Nullable — for exam-specific broadcasts |
| `broadcast_name` | varchar(100) | Human label |
| `target_type` | varchar | Enum: `ALL_INSTITUTIONS` · `BY_INSTITUTION_LIST` · `BY_EXAM_TYPE` · `BY_INSTITUTION_TYPE` |
| `target_filter` | jsonb | Filter criteria: `{"institution_ids": [...]}` or `{"exam_type": "SSC"}` or `{"institution_type": "COACHING"}` |
| `variable_values` | jsonb | `{"student_name": "{{student_name}}"}` — variables resolved per recipient |
| `channel` | varchar | Matches template channel |
| `status` | varchar | Enum: `DRAFT` · `PENDING_APPROVAL` · `APPROVED` · `QUEUED` · `SENDING` · `SENT` · `FAILED` · `PARTIAL` · `CANCELLED` |
| `total_recipients` | int | Nullable — computed before send |
| `sent_count` | int | Default 0 — updated as Celery sends |
| `failed_count` | int | Default 0 |
| `opt_out_skipped` | int | Default 0 — recipients who opted out |
| `created_by_id` | FK → auth.User | Notification Manager (37) |
| `approved_by_id` | FK → auth.User | Notification Manager (37) or Ops Manager (34) |
| `scheduled_at` | timestamptz | Nullable — if scheduled for later |
| `send_started_at` | timestamptz | Nullable |
| `completed_at` | timestamptz | Nullable |
| `celery_task_id` | varchar(50) | Nullable |

---

### `exam_integrity_flag`

Auto-detected or manually raised proctoring flag per student session. DPDPA: no student names stored; session reference is anonymized.

| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `exam_schedule_id` | FK → `exam_schedule` | — |
| `institution_id` | int | — |
| `session_ref` | varchar(50) | Anonymised session identifier (hash, not student name) |
| `flag_type` | varchar | Enum: `TAB_SWITCH` · `COPY_PASTE` · `MULTIPLE_FACE_DETECTED` · `SCREEN_CAPTURE` · `IP_SHARING` · `ANSWER_PATTERN_ANOMALY` · `SUBMIT_TIME_ANOMALY` · `UNUSUAL_ACCURACY_JUMP` · `PROCTOR_MANUAL_FLAG` |
| `flag_count` | int | How many times this flag occurred for this session |
| `severity` | varchar | Enum: `LOW` · `MEDIUM` · `HIGH` |
| `auto_detected` | boolean | True = system-generated; False = manual proctoring flag |
| `reviewed_by_id` | FK → auth.User | Nullable — Integrity Officer (91) |
| `status` | varchar | Enum: `NEW` · `UNDER_REVIEW` · `ESCALATED_TO_CASE` · `DISMISSED` · `CONFIRMED` |
| `review_notes` | text | Nullable |
| `created_at` | timestamptz | — |
| `reviewed_at` | timestamptz | Nullable |

---

### `exam_malpractice_case`

A formal case opened by the Integrity Officer for a pattern of misconduct.

| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `exam_schedule_id` | FK → `exam_schedule` | — |
| `institution_id` | int | — |
| `case_type` | varchar | Enum: `PAPER_LEAK` · `MASS_COPYING` · `IMPERSONATION` · `ANSWER_SHARING` · `SYSTEMATIC_ANOMALY` · `OTHER` |
| `severity` | varchar | Enum: `LOW` · `MEDIUM` · `HIGH` · `CRITICAL` |
| `description` | text | Case details |
| `statistical_anomaly_score` | decimal | Nullable — computed score from statistical analysis |
| `affected_student_count_estimate` | int | Nullable — DPDPA: count only, no names |
| `evidence_summary` | text | Nullable |
| `result_hold_placed` | boolean | Default False — set if Results Coordinator placed hold |
| `assigned_to_id` | FK → auth.User | Integrity Officer (91) |
| `status` | varchar | Enum: `OPEN` · `UNDER_INVESTIGATION` · `LEGAL_ESCALATED` · `INSTITUTION_NOTIFIED` · `CLOSED_CONFIRMED` · `CLOSED_DISMISSED` |
| `institution_notified_at` | timestamptz | Nullable |
| `legal_referred_at` | timestamptz | Nullable |
| `closure_notes` | text | Nullable |
| `created_by_id` | FK → auth.User | — |
| `created_at` | timestamptz | — |
| `updated_at` | timestamptz | — |

---

### `exam_support_ticket`

Support ticket raised during a live exam window. DPDPA: no student names — `student_ref` is anonymized.

| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `ticket_number` | varchar(20) | Auto-generated: `FST-{YYYYMMDD}-{seq}` |
| `exam_schedule_id` | FK → `exam_schedule` | — |
| `institution_id` | int | — |
| `ticket_type` | varchar | Enum: `STUDENT_LOCKED_OUT` · `SESSION_STUCK` · `SUBMIT_FAILED` · `LOGIN_ISSUE` · `TIMER_MISMATCH` · `QUESTION_NOT_LOADING` · `RESULT_NOT_VISIBLE` · `OTHER` |
| `priority` | varchar | Enum: `LOW` · `MEDIUM` · `HIGH` · `CRITICAL` |
| `description` | text | — |
| `student_ref` | varchar(50) | Nullable — anonymised reference (hash) |
| `reported_via` | varchar | Enum: `PHONE` · `WHATSAPP` · `EMAIL` · `IN_APP` |
| `assigned_to_id` | FK → auth.User | Support Exec (35) |
| `status` | varchar | Enum: `OPEN` · `IN_PROGRESS` · `ESCALATED` · `RESOLVED` · `CLOSED` |
| `resolution` | text | Nullable |
| `escalated_to_incident_id` | FK → `exam_session_incident` | Nullable — if ticket escalated to an incident |
| `sla_due` | timestamptz | Set from `exam_operational_config.support_sla_minutes` |
| `created_at` | timestamptz | — |
| `resolved_at` | timestamptz | Nullable |

---

### `exam_operational_config`

Singleton configuration record (always id=1).

| Field | Type | Default | Notes |
|---|---|---|---|
| `live_monitor_snapshot_seconds` | int | 30 | How often Celery updates `exam_ops_snapshot` during active exams |
| `auto_snapshot_hours_before_exam` | int | 1 | How many hours before exam start Celery begins snapshotting |
| `auto_snapshot_hours_after_exam` | int | 2 | How many hours after exam end Celery keeps snapshotting |
| `grace_period_default_minutes` | int | 10 | Default grace period after scheduled exam end before auto-close |
| `result_review_window_hours` | int | 48 | How long Results Coordinator has to review before publication |
| `answer_key_objection_window_hours` | int | 72 | Hours after answer key publish that objections are accepted |
| `max_objections_per_institution` | int | 20 | Hard limit on objections per institution per exam |
| `auto_compute_on_exam_complete` | boolean | True | If True: Celery auto-queues computation when exam status → COMPLETED |
| `notification_send_rate_per_minute` | int | 5000 | Max WhatsApp+SMS messages per minute (rate limiter for Celery broadcast tasks) |
| `whatsapp_daily_limit` | int | 150000 | Platform-level WhatsApp sends per day |
| `sms_daily_limit` | int | 200000 | Platform-level SMS sends per day |
| `support_sla_minutes_low` | int | 60 | SLA for LOW priority tickets |
| `support_sla_minutes_medium` | int | 30 | SLA for MEDIUM priority tickets |
| `support_sla_minutes_high` | int | 15 | SLA for HIGH priority tickets |
| `support_sla_minutes_critical` | int | 5 | SLA for CRITICAL priority tickets |
| `integrity_flag_auto_escalate_threshold` | int | 5 | If `flag_count ≥ N` for HIGH severity: auto-create malpractice case |
| `result_withhold_requires_dual_approval` | boolean | True | Both Integrity Officer (91) AND Ops Manager (34) must approve |
| `updated_by_id` | FK → auth.User | — | — |
| `updated_at` | timestamptz | — | — |

---

## Global UI Standards — Division F

These patterns apply to all 9 Div F pages and are defined once here.

### Toast Notifications

| Variant | Duration | Use |
|---|---|---|
| ✅ Success | 4s | Config saved, exam scheduled, result published, notification sent, objection resolved |
| ❌ Error | Persistent | Config lock failed, computation failed, broadcast rejected, validation error |
| ⚠️ Warning | 8s | Exam approaching (T-1h), result review window expiring, objection window closing, quota at 80% |
| ℹ️ Info | 6s | Snapshot update started, computation queued, broadcast queued, Celery task acknowledged |

### Skeleton Loaders

- **Exam schedule table rows:** 6-row shimmer (status pill + institution name + exam name + dates)
- **Live monitor grid cards:** 4 × 3 grid of card shimmers (institution + progress bar + 3 stat pairs)
- **Support ticket rows:** 8-row shimmer (ticket number + type + priority + status)
- **KPI tiles:** Rectangle shimmer matching tile dimensions
- **Result computation progress:** Inline progress bar shimmer

### Server-Side Pagination

- Default: **25 rows** per page for all list views
- Live monitor: **grid of 50 exam cards** (scroll-based, no pagination — filter instead)
- URL-bookmarkable: `?page=N&sort=X&dir=asc`
- "Showing X–Y of N" always visible

### Search Bar

- Debounced 300ms. Context-sensitive: searches institution name, exam name, ticket number, case ID.
- "×" clear button. Clears to page 1.

### Advanced Filter Panel

- Collapsible (collapsed by default). "Filters ▼" toggle.
- Active filter pills below search bar (each dismissible with ×).
- "Reset All" clears all filters and returns to page 1.

### Empty States

Three-part structure: Heading + Subtext + CTA (where applicable).

### Sortable Columns

↑ ASC / ↓ DESC indicators. Sort state in URL: `?sort=scheduled_start&dir=desc`. Only one active sort at a time.

### Drawers

- Exam schedule detail/config drawer: **760px** right panel
- Support ticket drawer: **640px** right panel
- Result review drawer: **760px** right panel
- Objection review drawer: **640px** right panel
- Malpractice case drawer: **760px** right panel
- Mobile: full-screen bottom sheet for all drawers

### Role-Based UI Visibility

- Write actions hidden (not just disabled) for read-only roles — not rendered server-side.
- "You have read-only access to this page" banner at top for read-only visitors.

### Responsive Breakpoints

| Breakpoint | Behaviour |
|---|---|
| Desktop (≥1280px) | Full table, side drawers, filter panel collapsible |
| Tablet (768–1279px) | Filter panel hidden behind "Filters" button; table reduces to key columns |
| Mobile (<768px) | Card layout; drawer = full screen. Live monitor card stacks vertically. |

### Charts (Division F)

- Live monitor: `BarChart` for submission rate over time (rolling 10min); `PieChart` for session state breakdown
- Results: `HistogramChart` (score distribution); `BarChart` (institution comparison)
- Analytics: `LineChart` (trend over exam series); `ScatterPlot` (item difficulty vs. discrimination)
- All charts: `ResponsiveContainer` wrapper. No-data state: grey placeholder with "No data yet" text.
- All charts read from aggregated/computed tables — never from live tenant schema queries.

### HTMX Polling Strategy

| Page | Polling frequency | What polls |
|---|---|---|
| F-02 Live Monitor | 30s | `?part=monitor-grid` (reads `exam_ops_snapshot`) |
| F-02 Live Monitor KPI | 30s | `?part=monitor-kpi` |
| F-03 Support Console (open tickets) | 60s | `?part=ticket-table` |
| F-04 Results (computation progress) | 10s while RUNNING | `?part=computation-progress&id={id}` |
| All other pages | On-demand only | No auto-poll |

**No Redis:** All real-time data flows through `exam_ops_snapshot` (Celery Beat → PostgreSQL → HTMX poll). Memcached caches snapshot reads for 25s (just under poll interval) to protect the DB during peak load.

---

## Notification Policy — Division F

Division F is the primary notification-sending division. All outbound communications to institutions and students route through F-06 Notification Hub.

- **Student notifications:** WhatsApp/SMS via F-06 broadcast (74K recipients = Celery batch, 5,000/min rate)
- **Institution admin notifications:** Email via F-06 broadcast
- **Internal Ops notifications (in-app):** F-02/F-03 use in-app notifications to Ops team for incidents, SLA breaches
- **DPDPA compliance:** All notification templates use role labels and exam names — never personal student data in logs
- **DLT registration:** All SMS templates must have TRAI DLT pre-registration (`dlt_template_id` populated) before activation. Notification Manager (37) tracks DLT approval status in F-06.

---

## Celery Task Registry — Division F

| Task Name | Trigger | Description | Retry Policy |
|---|---|---|---|
| `update_exam_ops_snapshots` | Celery Beat — every 30s (during active exam windows) | Aggregates session counts from all active tenant schemas → writes `exam_ops_snapshot` | No retry — next beat cycle picks up |
| `auto_start_snapshot_monitoring` | Celery Beat — hourly | Detects exams starting within next 1 hour → begins snapshot monitoring | 3× at 60s |
| `auto_stop_snapshot_monitoring` | Celery Beat — hourly | Detects exams completed >2 hours ago → stops snapshot updates | 3× at 60s |
| `compute_exam_results` | Manual trigger (Results Coordinator) or `auto_compute_on_exam_complete` | Reads submissions from tenant schema, computes marks, creates result records | 3× at 5min |
| `compute_exam_ranks` | After `compute_exam_results` COMPLETED | Assigns ranks/percentile within institution cohort | 3× at 5min |
| `publish_exam_results` | Approval action in F-04 | Sets result records visible in student/institution portals | 5× at 30s |
| `send_notification_broadcast` | Broadcast approved + send action in F-06 | Sends WhatsApp/SMS/Email to all recipients in `exam_notification_broadcast.target_filter` at rate-limited 5K/min | 3× per failed message batch |
| `close_answer_key_objection_window` | Celery Beat — hourly | Checks `objection_window_close_at` → closes expired windows | 3× at 60s |
| `check_support_ticket_sla` | Celery Beat — every 5 min | Flags overdue tickets; notifies Support Exec (35) and Ops Manager (34) | No retry |
| `auto_escalate_integrity_flags` | Celery Beat — every 10 min | Checks flags with `flag_count ≥ integrity_flag_auto_escalate_threshold` → creates malpractice case draft | 3× at 60s |
| `check_notification_quota` | Celery Beat — hourly | Compares daily send count vs quota limits → amber/red alerts in F-06 | No retry |
| `auto_activate_exam` | Celery Beat — every 1 min | Detects `exam_schedule` with `status=SCHEDULED` and `scheduled_start ≤ now()` → sets `status=ACTIVE`; only fires if `auto_transition_to_active=True` in config | 3× at 30s |
| `auto_complete_exam` | Celery Beat — every 1 min | Detects `status=ACTIVE` exams where `scheduled_end + grace_period_minutes ≤ now()` → sets `status=COMPLETED`; triggers `compute_exam_results` if `auto_compute_on_exam_complete=True` | 3× at 30s |
| `auto_close_support_tickets` | Celery Beat — every 30 min | Sets `RESOLVED` tickets older than 24h to `CLOSED` | No retry |
| `compute_exam_analytics_aggregate` | Celery chain after `publish_exam_results` COMPLETED | Aggregates score statistics (mean, median, std dev, distribution) into `exam_analytics_aggregate` — used by F-08 Tab 1 | 3× at 5min |
| `compute_item_analysis` | Celery chain after answer key status → `FINAL` AND `exam_result_computation.status=COMPLETED` | Computes p-value and discrimination index per question into `exam_item_analysis` — used by F-08 Tab 2 | 3× at 5min |
| `analyze_exam_integrity` | Manual trigger from F-07 Tab 3 [Run Analysis] | Runs IP clustering + answer similarity + submit-time distribution analysis; writes to `exam_integrity_analysis`; deduplicates: if analysis already exists for this exam_schedule, overwrites | 3× at 10min |
| `deduplicate_malpractice_cases` | After `auto_escalate_integrity_flags` creates a case | Checks if an OPEN case already exists for the same `exam_schedule_id` and same `institution_id`; if yes, links flags to existing case instead of creating duplicate | 3× at 60s |

**Task chain for post-exam workflow:**
```
exam_schedule.status → COMPLETED
    ├── auto_compute_on_exam_complete=True?
    │       └── compute_exam_results → compute_exam_ranks
    │
    └── (after coordinator approves + publish_exam_results PUBLISHED)
            └── compute_exam_analytics_aggregate

answer_key status → FINAL (F-05) + exam_result_computation.status=COMPLETED
    └── compute_item_analysis  (F-08 Tab 2 now available)
```

---

---

## Cross-Page Critical Workflows

### 1. Objection Accepted → Rescore → Re-publish → Notify (F-05 → F-04 → F-06)

```
F-05: Objection accepted for Q15 (B → C)
    └── exam_answer_key_entry updated (correct_option = C)
    └── compute_exam_results queued (deduplication via rescoring_pending_additional_changes)
    └── exam_result_publication.status → DRAFT
    └── in-app notification to Results Coordinator (36): "Rescoring triggered for {Exam} — review and re-approve results."

F-04: Coordinator opens pending review
    └── Sees updated score distribution
    └── Runs validation checks
    └── [Approve & Publish] → publish_exam_results Celery task
    └── in-app prompt: "Results published. Send result notification? [Send Now via F-06] [Skip]"
    └── auto_send if F-09 config enabled

F-06: Notification Manager or auto-trigger sends result_announcement broadcast
    └── Recipient list re-queried fresh at send time (opt-outs excluded)
    └── Per-recipient variables resolved from tenant schema (score, student_ref)
```

**SLA continuity across F-03 escalation to F-02 incident:** When F-03 ticket status → ESCALATED (ticket linked to `exam_session_incident`), the ticket's own SLA timer **stops** (ticket is no longer directly being resolved). The incident has no independent SLA — Ops Manager manages it operationally. When the incident is resolved, the linked ticket must be closed manually in F-03. SLA breaches are only counted against the original ticket up to the escalation point.

### 2. Integrity Case → Result Withhold → Resolution (F-07 → F-04 → F-07)

```
F-07: Integrity Officer opens malpractice case FMC-{YYYYMMDD}-{seq}
    └── [Place Result Hold]: Step 1 (Integrity Officer submits)
    └── Step 2: Ops Manager approves → exam_schedule.integrity_hold = True
    └── F-04: [Approve & Publish] disabled for this exam until hold lifted

F-07: After investigation → [Close — Confirmed] or [Close — Dismissed]
    └── If Confirmed: institution notified (modal confirmation before send); Legal escalation if needed
    └── [Lift Result Hold]: dual approval again → integrity_hold = False
    └── F-04: [Approve & Publish] now available
```

### 3. Config Lock Flow (F-09 → F-01 → F-02)

Config lock deadline (`config_lock_required_before_hours`) set in F-09 → applies to all new exam schedules in F-01 → F-02 "Starting Soon" panel computes ⚠️ "Not Locked" using the same config value (live HTMX refresh every 30s picks up F-09 config changes).

---

*Division F pages list complete. 9 pages covering the full exam operations lifecycle: configure → monitor live → support → compute results → publish answer key → notify → detect integrity issues → analyse → configure ops settings.*
