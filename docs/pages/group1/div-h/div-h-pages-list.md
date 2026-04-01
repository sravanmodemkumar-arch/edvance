# Group 1 — Division H: Data & Analytics — Pages Reference

> **Division:** H — Data & Analytics
> **Roles:** Analytics Manager (42) · Data Engineer (43) · Data Analyst (44) · AI Generation Manager (45) · Report Designer (46)
> **Base URL prefix:** `/analytics/`
> **Theme:** Dark (`portal_base_dark.html`)
> **Status key:** ✅ Spec done · 🔨 In progress · ⬜ Not started

---

## Scale Context (always keep in mind)

| Dimension | Value |
|---|---|
| Total institutions | **2,050** (1,000 schools + 800 colleges + 100 coaching + 150 groups) |
| Total students | **2.4M–7.6M** depending on active enrollment period |
| Peak concurrent exam load | **74,000 simultaneous submissions** |
| Questions in bank | **2M+** across 6 exam domains |
| Active test series | **800+** |
| Exam domains | SSC · RRB · NEET · JEE · AP Board · TS Board |
| AI-generated MCQs in pipeline | Variable — ~5,000–50,000/month target |
| Analytics schema lag | Nightly batch — data is max 24h old (intra-day for P0 metrics) |
| Celery aggregation schemas | One query spans 2,050 tenant schemas — ALWAYS via pre-aggregated tables, never live cross-tenant scan |

---

## Division H — Role Summary

| # | Role | Level | Owns | Cannot Do |
|---|---|---|---|---|
| 42 | Analytics Manager | 1 | Platform-wide MIS; usage, revenue, exam performance trends; anomaly alerts; stakeholder reporting | No data edits; cannot trigger pipeline runs or AI batches |
| 43 | Data Engineer | 4 | EventBridge pipelines; aggregation Celery jobs; analytics schema DDL; data warehouse management; pipeline monitoring | Cannot approve AI MCQs; no business configuration |
| 44 | Data Analyst | 1 | Institution-level reports; cohort analysis; dropout signals; rank analytics; self-serve data exploration | No data edits; no pipeline management; no AI pipeline |
| 45 | AI Generation Manager | 3 | Commission AI MCQ batch jobs; review AI-generated MCQ quality before Division D queue; prompt/model configuration; cost monitoring | Cannot approve MCQs for publish (Division D Approver only); cannot modify existing question bank |
| 46 | Report Designer | 1 | Design institution-facing MIS report templates; schedule automated delivery; preview with sample data | No data edits; cannot trigger pipeline runs |

---

## Page Inventory

| # | Page Name | URL | File | Priority | Status | Primary Roles |
|---|---|---|---|---|---|---|
| H-01 | Analytics Dashboard | `/analytics/` | `h-01-analytics-dashboard.md` | **P0** | ✅ | 42, 44, 43, 45, 46, 10 |
| H-02 | Student Performance Analytics | `/analytics/students/` | `h-02-student-performance.md` | P1 | ✅ | 42, 44, 10 |
| H-03 | Institution Analytics | `/analytics/institutions/` | `h-03-institution-analytics.md` | P1 | ✅ | 42, 44, 10 |
| H-04 | Question Intelligence | `/analytics/questions/` | `h-04-question-intelligence.md` | P1 | ✅ | 42, 44, 43, 10 |
| H-05 | Exam & Domain Analytics | `/analytics/exams/` | `h-05-exam-analytics.md` | P1 | ✅ | 42, 44, 10 |
| H-06 | Data Pipeline Monitor | `/analytics/pipelines/` | `h-06-pipeline-monitor.md` | **P0** | ✅ | 43, 10 |
| H-07 | AI MCQ Generation | `/analytics/ai-generation/` | `h-07-ai-generation.md` | P1 | ✅ | 45, 43, 10 |
| H-08 | Report Studio | `/analytics/report-studio/` | `h-08-report-studio.md` | P2 | ✅ | 46, 42, 44, 10 |
| H-09 | Export Manager | `/analytics/exports/` | `h-09-export-manager.md` | P2 | ✅ | 42, 43, 44, 45, 46, 10 |

---

## Role-to-Page Access Matrix

| Page | Analytics Manager (42) | Data Engineer (43) | Data Analyst (44) | AI Gen Manager (45) | Report Designer (46) | Platform Admin (10) |
|---|---|---|---|---|---|---|
| H-01 Analytics Dashboard | ✅ Full | ✅ Full | ✅ Full | ✅ Full | ✅ Full | ✅ Full |
| H-02 Student Performance | ✅ Full | Read | ✅ Full | — | Read | ✅ Full |
| H-03 Institution Analytics | ✅ Full | Read | ✅ Full | — | Read | ✅ Full |
| H-04 Question Intelligence | ✅ Full | ✅ Full | ✅ Full | Read | — | ✅ Full |
| H-05 Exam Analytics | ✅ Full | Read | ✅ Full | — | Read | ✅ Full |
| H-06 Pipeline Monitor | Read | ✅ Full | — | Read | — | ✅ Full |
| H-07 AI Generation | — | Read | — | ✅ Full | — | ✅ Full |
| H-08 Report Studio | ✅ Approve | — | Read | — | ✅ Full | ✅ Full |
| H-09 Export Manager | ✅ Full | ✅ Full | ✅ Full | ✅ Full | ✅ Full | ✅ Full |

> **Read** = view data, no create/edit/delete. **—** = no access.

---

## Critical Action Ownership

| Action | Role |
|---|---|
| Trigger manual pipeline re-run | Data Engineer (43), Platform Admin (10) |
| Archive dead questions (bulk) | Data Analyst (44) — flags for review; Data Engineer (43) — executes |
| Create AI generation batch | AI Generation Manager (45) |
| Approve/reject AI-generated MCQs | AI Generation Manager (45) |
| Publish AI MCQs to Division D queue | AI Generation Manager (45) |
| Publish institution report template | Analytics Manager (42) |
| Schedule institution report delivery | Report Designer (46), Analytics Manager (42) |
| Override data freshness warning | Data Engineer (43) — via pipeline re-run |
| Configure AI model / prompt templates | AI Generation Manager (45), Platform Admin (10) |

---

## Analytics Architecture

### Cross-Tenant Aggregation Strategy

The platform has 2,050 tenant PostgreSQL schemas. A naive cross-tenant query (e.g., `SELECT COUNT(*) FROM tenant_*.exam_attempts`) at 2.4M–7.6M students is catastrophically slow — and at 74K peak concurrent, impossible in real-time.

**Solution: Pre-Aggregated Analytics Schema**

A dedicated `analytics` schema (separate from all 2,050 tenant schemas) stores pre-computed aggregate data only. No analytics page ever queries tenant schemas directly in real-time.

```
Tenant schemas (2,050)          Analytics schema (1)
    └── exam_attempts     ─────▶  analytics_daily_snapshot
    └── exam_questions    ─────▶  analytics_question_stats
    └── institutions      ─────▶  analytics_institution_engagement
    └── students          ─────▶  analytics_cohort_snapshot
         (nightly Celery batch — never real-time)
```

**Data freshness guarantees:**
- Most metrics: updated nightly at 01:00–04:00 IST (max 24h lag)
- Institution engagement scores: updated weekly (Sunday 03:00 IST)
- Cohort snapshots: updated monthly (1st of month 04:00 IST)
- All pages show "Data as of: {last_computed_at}" timestamp
- Data Engineer can force a manual re-run of any pipeline job from H-06

**Caching layer:** Memcached. `?nocache=true` param available to Data Engineer for fresh reads.

**Memcached TTL per page:**

| Page | Cache Key Pattern | TTL | Notes |
|---|---|---|---|
| H-01 Analytics Dashboard | `h01:kpi:{role}` | 15 min | KPI tiles + trend chart |
| H-01 anomaly alerts | `h01:anomalies` | 30 min | Anomaly detection is compute-heavy |
| H-02 Student Performance | `h02:summary:{filters_hash}` | 15 min | Score distribution, cohort waterfall |
| H-02 cohort waterfall | `h02:cohort:{dim}:{period}` | 60 min | Monthly cohort data changes rarely |
| H-03 Institution Analytics | `h03:list:{filters_hash}` | 15 min | Engagement table |
| H-03 choropleth map | `h03:map:{metric}:{period}` | 30 min | State-level aggregates |
| H-04 Question Intelligence | `h04:quality:{domain}:{subject}` | 60 min | CTT metrics updated nightly only |
| H-05 Exam Analytics | `h05:domain_kpi:{filters_hash}` | 15 min | Domain KPI bar |
| H-05 timing heatmap | `h05:heatmap:{domain}:{period}` | 30 min | Heatmap is aggregation-heavy |
| H-06 Pipeline Monitor | `h06:health` | 2 min | Pipeline health cards need near-real-time |
| H-07 AI Generation | `h07:kpi` | 5 min | Batch status changes frequently |
| H-08 Report Studio | `h08:delivery_log:{filters_hash}` | 5 min | Delivery log updates as reports generate |
| H-09 Export Manager | `h09:list:{user_id}` | 2 min | Export status changes during processing |

---

## Complete Data Model

### Table: `analytics_daily_snapshot`

Pre-computed daily metric aggregates. The backbone of all time-series charts in Division H.

| Field | Type | Notes |
|---|---|---|
| `id` | bigint PK | — |
| `snapshot_date` | date | The date this metric represents |
| `metric_key` | varchar(100) | e.g., `active_institutions`, `exam_attempts_total`, `avg_score_pct`, `new_students` |
| `dimension_type` | varchar(50) | `exam_domain` · `institution_type` · `subscription_tier` · `region_state` · `none` |
| `dimension_value` | varchar(100) | e.g., `SSC`, `SCHOOL`, `Enterprise`, `Telangana` — or `_all_` for undimensioned |
| `metric_value` | decimal(20,4) | Numeric value |
| `metric_metadata` | jsonb | Optional extra context (e.g., `{"sample_size": 14200}`) |
| `computed_at` | timestamptz | When Celery job wrote this row |

Unique constraint: `(snapshot_date, metric_key, dimension_type, dimension_value)`.

Retention: 3 years of daily snapshots per metric.

---

### Table: `analytics_question_stats`

Classical Test Theory (CTT) metrics per question. Computed nightly from cross-tenant attempt data.

| Field | Type | Notes |
|---|---|---|
| `id` | bigint PK | — |
| `question_id` | bigint | References the global question registry (not tenant-specific) |
| `domain` | varchar(50) | SSC · RRB · NEET · JEE · AP_BOARD · TS_BOARD |
| `subject` | varchar(100) | e.g., Mathematics, Physics |
| `attempt_count` | int | Total attempts across all tenants |
| `correct_count` | int | Correct answer count |
| `difficulty_index` | decimal(5,4) | `p = correct_count / attempt_count`. 0.0–1.0. Easy >0.7, Medium 0.4–0.7, Hard <0.4 |
| `discrimination_index` | decimal(5,4) | Point-biserial correlation between item score and total score. Good >0.3, Poor <0.2 |
| `omission_rate` | decimal(5,4) | Proportion of students who skipped this question |
| `distractor_stats` | jsonb | `{"A": 0.42, "B": 0.22, "C": 0.28, "D": 0.08}` — proportion choosing each option |
| `first_used_at` | date | First exam this question appeared in |
| `last_used_at` | date | Last exam this question appeared in |
| `last_computed_at` | timestamptz | When Celery job last updated this row |
| `quality_flag` | varchar(30) | `OK` · `POOR_DISCRIMINATION` · `ALL_CORRECT` · `ALL_WRONG` · `NEGATIVE_D` · `NEVER_USED` · `STALE` · `INSUFFICIENT_ATTEMPTS` (< 30 attempts — not enough data for reliable CTT; shown in H-04 but excluded from quality health KPIs) · `ARCHIVED` (question archived in question registry — row retained for historical analytics) |

---

### Table: `analytics_institution_engagement`

Weekly engagement health score per institution. Used by H-03 and Division J (Customer Success, cross-reference only).

| Field | Type | Notes |
|---|---|---|
| `id` | bigint PK | — |
| `institution_id` | bigint | Platform institution ID |
| `institution_name` | varchar(300) | Denormalized for analytics queries |
| `institution_type` | varchar(20) | SCHOOL · COLLEGE · COACHING · GROUP |
| `subscription_tier` | varchar(20) | Starter · Standard · Professional · Enterprise |
| `region_state` | varchar(100) | — |
| `engagement_score` | smallint | 0–100 composite score (see formula below) |
| `churn_risk` | varchar(10) | LOW · MEDIUM · HIGH · CRITICAL |
| `exam_frequency_per_month` | decimal(6,2) | Average exams conducted per month (last 90 days) |
| `student_active_rate` | decimal(5,4) | Active students ÷ enrolled students in last 30 days |
| `question_bank_usage_pct` | decimal(5,4) | Unique questions used ÷ total available for this tier |
| `login_days_last_30` | smallint | Days with at least one admin login in last 30 days |
| `support_ticket_count_30d` | smallint | L1/L2/L3 tickets raised in last 30 days |
| `last_exam_at` | date | Date of most recent exam |
| `week_start` | date | Start of the week this snapshot covers |
| `computed_at` | timestamptz | — |

**Engagement score formula:**
- `exam_frequency_per_month`: weight 30%
- `student_active_rate`: weight 30%
- `question_bank_usage_pct`: weight 20%
- `login_days_last_30 / 30`: weight 20%
- **Churn risk thresholds:** CRITICAL <30, HIGH 30–49, MEDIUM 50–69, LOW ≥70

---

### Table: `analytics_cohort_snapshot`

Monthly student cohort retention data. Privacy-safe (no individual student IDs — aggregate by cohort).

| Field | Type | Notes |
|---|---|---|
| `id` | bigint PK | — |
| `cohort_month` | date | First day of month when cohort enrolled (e.g., 2024-09-01) |
| `dimension_type` | varchar(50) | `exam_domain` · `institution_type` · `region_state` · `none` |
| `dimension_value` | varchar(100) | — |
| `cohort_size` | int | Students who first appeared in this month |
| `retained_month_1` | int | Students still active in month+1 |
| `retained_month_2` | int | Students still active in month+2 |
| `retained_month_3` | int | — |
| `retained_month_6` | int | — |
| `retained_month_12` | int | — |
| `computed_at` | timestamptz | — |

---

### Table: `analytics_ai_batch`

AI MCQ generation batch jobs managed by AI Generation Manager (45).

| Field | Type | Notes |
|---|---|---|
| `id` | bigint PK | — |
| `batch_ref` | varchar(20) | Auto-generated: `AIB-{YYYY}{MM}-{seq}` e.g. `AIB-202409-0042` |
| `domain` | varchar(50) | Target exam domain |
| `subject` | varchar(100) | Target subject |
| `topic` | varchar(200) | Specific topic within subject |
| `difficulty_target` | varchar(10) | EASY · MEDIUM · HARD · MIXED |
| `requested_count` | smallint | How many MCQs requested |
| `model_config_id` | FK → analytics_ai_model_config | Which model + prompt template was used |
| `status` | varchar(20) | `QUEUED` · `GENERATING` · `REVIEW_PENDING` · `REVIEW_IN_PROGRESS` · `APPROVED` · `PARTIALLY_APPROVED` · `REJECTED` · `CANCELLED` |
| `generated_count` | smallint | How many MCQs the AI actually returned |
| `approved_count` | smallint | How many the AI Gen Manager approved for Division D queue |
| `rejected_count` | smallint | How many were rejected |
| `api_cost_inr` | decimal(10,2) | Cost of this batch (converted to INR at time of generation) |
| `generation_started_at` | timestamptz | — |
| `generation_completed_at` | timestamptz | — |
| `review_started_at` | timestamptz | When AI Gen Manager started reviewing |
| `review_completed_at` | timestamptz | — |
| `created_by_id` | FK → auth.User | AI Generation Manager |
| `reviewed_by_id` | FK → auth.User | — |
| `notes` | text | Generation notes passed to Division D SMEs |
| `celery_task_id` | varchar(36) | Celery task UUID for status polling |

---

### Table: `analytics_ai_generated_mcq`

Individual MCQs produced by an AI batch. Pending review by AI Gen Manager before queuing for Division D.

| Field | Type | Notes |
|---|---|---|
| `id` | bigint PK | — |
| `batch_id` | FK → analytics_ai_batch | — |
| `sequence_no` | smallint | Order within batch (1-based) |
| `question_text` | text | AI-generated question (not encrypted — not student PII) |
| `option_a` | text | — |
| `option_b` | text | — |
| `option_c` | text | — |
| `option_d` | text | — |
| `correct_option` | char(1) | A / B / C / D |
| `explanation` | text | AI-generated explanation |
| `ai_confidence_score` | decimal(4,3) | Model's self-reported confidence 0.0–1.0 |
| `review_status` | varchar(25) | `PENDING` · `APPROVED` · `REJECTED` · `FLAGGED_FOR_REVISION` · `AUTO_REJECTED` (duplicate detected via `question_text_hash` — not shown in review queue; counted in batch stats as auto-rejected) |
| `review_note` | text | AI Gen Manager's note (required if REJECTED or FLAGGED) |
| `division_d_queue_id` | bigint | Once approved, the Division D content queue ID |
| `rejection_reason_codes` | varchar[] | Structured rejection reason codes (nullable — only set when rejected/flagged). Values: `WRONG_ANSWER` · `FACTUALLY_INCORRECT` · `POOR_DISTRACTORS` · `TOPIC_DRIFT` · `AMBIGUOUS` · `DUPLICATE` · `LANGUAGE_QUALITY` · `OTHER`. Multiple codes allowed. |
| `reviewed_at` | timestamptz | — |
| `reviewed_by_id` | FK → auth.User | — |
| `skipped_until` | timestamptz | Nullable. When set, this MCQ is excluded from the review queue until this datetime (24h skip deferral). Managed server-side, persists across browser sessions. |
| `division_d_reject_reason` | text | Nullable. Populated via Division D callback (via F-06 notification hub) when a Division D SME/Approver rejects an AI-sourced MCQ. Used in H-07 quality metrics "Division D rejection rate" chart. |
| `question_text_hash` | char(64) | SHA-256 hash of `question_text` (lowercase, stripped). Used for duplicate detection at batch-review time. Unique constraint — new MCQs matching an existing hash are AUTO_REJECTED with reason `DUPLICATE_DETECTED`. |

---

### Table: `analytics_ai_model_config`

Stores AI model configurations and prompt templates for MCQ generation.

| Field | Type | Notes |
|---|---|---|
| `id` | bigint PK | — |
| `name` | varchar(100) | e.g., "GPT-4o SSC Standard", "Claude 3.5 NEET" |
| `model_provider` | varchar(50) | `OPENAI` · `ANTHROPIC` · `CUSTOM` |
| `model_id` | varchar(100) | e.g., `gpt-4o`, `claude-sonnet-4-6` |
| `api_key_encrypted` | text | AES-256-GCM encrypted API key. Encryption key stored in AWS KMS (same pattern as `bgv_vendor_config.api_key_encrypted` in Division G). Never logged, never returned in API responses — write-only field in UI. |
| `system_prompt` | text | System-level instructions for MCQ generation |
| `user_prompt_template` | text | Template with `{domain}`, `{subject}`, `{topic}`, `{difficulty}`, `{count}` placeholders |
| `temperature` | decimal(3,2) | 0.0–1.0 |
| `max_tokens` | int | — |
| `is_active` | boolean | Only active configs shown in batch creation |
| `api_key_rotation_required_at` | timestamptz | When key must be rotated (default: `created_at + 90 days`). If `NOW() > rotation_required_at`, batch creation with this config is blocked with message: "API key rotation required. [Rotate Key →]". |
| `api_key_last_rotated_at` | timestamptz | Nullable — null means key has never been explicitly rotated (only set). Audited in `analytics_audit_log` (action=`MODEL_CONFIG_KEY_ROTATED`). |
| `monthly_budget_inr` | decimal(10,2) | Per-config monthly budget cap in INR. If MTD spend for this config reaches 80% of budget: amber cost alert in H-07 cost tracker. If 100%: new batch creation with this config is blocked with message "Monthly AI budget (₹{N}) for config '{name}' is exhausted." Editable by AI Generation Manager (45) and Platform Admin (10). Null = no per-config cap (platform-wide global cap still applies). |
| `created_by_id` | FK → auth.User | — |
| `updated_at` | timestamptz | — |

---

### Table: `analytics_report_template`

Institution-facing MIS report templates created by Report Designer (46).

| Field | Type | Notes |
|---|---|---|
| `id` | bigint PK | — |
| `name` | varchar(200) | e.g., "Monthly Performance Summary — Coaching" |
| `target_audience` | varchar(30) | `INSTITUTION_ADMIN` · `INTERNAL_EXEC` · `DIVISION_H_ONLY` |
| `institution_types` | varchar[] | Which institution types this template applies to (SCHOOL/COLLEGE/COACHING/ALL) |
| `subscription_tiers` | varchar[] | Which tiers receive this report |
| `sections` | jsonb | Ordered list of section config objects. Each object has `"type"` (string, required) plus type-specific config keys. Valid types and their key config fields: `kpi_bar` (`metrics`: string[], `period`: "MTD"\|"last_30d"\|"last_90d"`, `tile_count`: 2–8); `score_distribution` (`period`, `domain_filter`); `subject_heatmap` (`domain`, `top_n`); `cohort_retention` (`cohort_period`, `dimension`); `exam_history_table` (`columns`: string[], `row_count`: 5–20, `period`); `domain_breakdown` (`domains`: string[], `metrics`: string[]); `trend_chart` (`metric`, `period`, `show_platform_avg`: bool); `ranking_table` (`metric`, `peer_group`: "auto"\|"same_region"\|"same_tier"\|"national"\|"custom", `custom_states`: string[]); `text_block` (`content`: markdown string with `{variable}` refs); `page_break` (no extra keys); `bgv_summary` (no extra keys — reads from Division G `bgv_institution_compliance`). Order in the array determines render order. |
| `output_formats` | varchar[] | `PDF` · `CSV` · `XLSX` |
| `schedule_type` | varchar(20) | `MANUAL` · `MONTHLY` · `QUARTERLY` · `ANNUAL` |
| `schedule_day` | smallint | Day of month to deliver (1–28) |
| `status` | varchar(30) | State machine: `DRAFT` → `PENDING_APPROVAL` → (`PUBLISHED` or `DRAFT_WITH_FEEDBACK`) → `ARCHIVED`. Only `PUBLISHED` templates are used for auto-delivery. `DRAFT_WITH_FEEDBACK` means Analytics Manager returned it with comments. |
| `status_updated_at` | timestamptz | When status last changed |
| `published_at` | timestamptz | Set when status transitions to PUBLISHED |
| `published_by_id` | FK → auth.User | Analytics Manager (42) must approve publish |
| `feedback_note` | text | Populated when Analytics Manager clicks [Request Changes]; visible to Report Designer as feedback on their DRAFT_WITH_FEEDBACK template |
| `created_by_id` | FK → auth.User | Report Designer (46) |
| `updated_at` | timestamptz | — |

---

### Table: `analytics_report_delivery`

Log of every report delivery (auto-scheduled or manual).

| Field | Type | Notes |
|---|---|---|
| `id` | bigint PK | — |
| `template_id` | FK → analytics_report_template | — |
| `institution_id` | bigint | Which institution received this report |
| `delivery_type` | varchar(20) | `SCHEDULED` · `MANUAL` · `TEST` |
| `period_start` | date | Report covers data from this date |
| `period_end` | date | — |
| `output_format` | varchar(10) | PDF · CSV · XLSX |
| `file_path` | varchar(500) | R2 path (private, signed URL for download) |
| `status` | varchar(20) | `PENDING` · `GENERATING` · `DELIVERED` · `FAILED` |
| `delivered_at` | timestamptz | — |
| `file_size_bytes` | bigint | Nullable — size of generated file; populated when DELIVERED |
| `download_url_expires_at` | timestamptz | When the R2 signed URL expires (set to `delivered_at + 72h`). Nullable for non-DELIVERED records. Regenerated on demand via [Regenerate Download Link]. |
| `error_message` | text | If FAILED — includes which template section caused failure (e.g., "Failed at section 'Score Distribution': chart data error") |
| `error_type` | varchar(20) | `TRANSIENT` (network/timeout — safe to retry) · `DATA_ERROR` (missing/corrupt data — retry will likely fail again; fix template first) · `QUOTA_EXCEEDED` (R2 storage limit) — null for non-FAILED records |
| `triggered_by_id` | FK → auth.User | Null for scheduled deliveries |

---

### Table: `analytics_pipeline_run`

Execution history of every Celery analytics aggregation job. Monitored in H-06.

| Field | Type | Notes |
|---|---|---|
| `id` | bigint PK | — |
| `job_name` | varchar(100) | e.g., `aggregate_daily_platform_metrics`, `compute_question_analytics` |
| `run_type` | varchar(20) | `SCHEDULED` · `MANUAL` |
| `triggered_by_id` | FK → auth.User | Null for scheduled runs |
| `status` | varchar(20) | `RUNNING` · `SUCCESS` · `FAILED` · `PARTIAL_SUCCESS` · `SKIPPED` |
| `started_at` | timestamptz | — |
| `completed_at` | timestamptz | — |
| `duration_ms` | int | — |
| `rows_processed` | bigint | Total rows read across all tenant schemas |
| `rows_written` | bigint | Rows written to analytics schema |
| `tenants_processed` | smallint | Number of tenant schemas queried |
| `tenants_failed` | smallint | Tenants where query failed (partial success) |
| `error_message` | text | Full traceback if FAILED |
| `celery_task_id` | varchar(36) | — |

---

### Table: `analytics_export_request`

Self-serve data export queue for Data Analysts who need raw aggregated data.

| Field | Type | Notes |
|---|---|---|
| `id` | bigint PK | — |
| `requested_by_id` | FK → auth.User | — |
| `export_type` | varchar(50) | `QUESTION_STATS` · `INSTITUTION_ENGAGEMENT` · `STUDENT_COHORT` · `EXAM_PERFORMANCE` · `AI_BATCH_SUMMARY` |
| `filters` | jsonb | Applied filter state at time of export request |
| `output_format` | varchar(10) | CSV · XLSX |
| `status` | varchar(20) | `QUEUED` · `PROCESSING` · `READY` · `EXPIRED` · `FAILED` |
| `file_path` | varchar(500) | R2 path when READY |
| `row_count` | bigint | Rows in exported file |
| `expires_at` | timestamptz | Download link expires 48h after generation |
| `created_at` | timestamptz | — |
| `completed_at` | timestamptz | — |

---

### Table: `analytics_infrastructure_event`

Read-only materialized copy of Division F infrastructure incidents, synced nightly by `aggregate_daily_platform_metrics` as a cross-schema read. Used by H-05 (SLA-breach correlation) and H-06 (infrastructure overlay on timing heatmap). Division H never writes to this table.

| Field | Type | Notes |
|---|---|---|
| `id` | bigint PK | — |
| `source_incident_id` | bigint | PK from Division F `incident_log` table (source of truth) |
| `started_at` | timestamptz | Incident start time (IST) |
| `resolved_at` | timestamptz | Nullable — null = unresolved at sync time |
| `incident_type` | varchar(50) | e.g., `LATENCY_BREACH`, `LAMBDA_THROTTLE`, `RDS_CONNECTION`, `CDN_DEGRADATION` |
| `severity` | varchar(10) | `P0` · `P1` · `P2` · `P3` |
| `affected_domain` | varchar(50) | Nullable — if incident affected a specific exam domain; `_all_` if platform-wide |
| `sla_breached` | boolean | `true` if latency > 2s during this incident window |
| `synced_at` | timestamptz | When the Celery aggregation task last synced this record |

**Sync mechanism:** During `aggregate_daily_platform_metrics` (Task 1), a read-only join is made to the Division F incident schema. Only incidents from the last 90 days are synced (older incidents pruned). Full upsert on `source_incident_id`.

**Retention:** 90 days (matches H-05 max filter window for SLA correlation).

---

### Table: `analytics_saved_query`

Saved SQL queries for the Warehouse SQL Explorer in H-06. Personal and team-shared queries.

| Field | Type | Notes |
|---|---|---|
| `id` | bigint PK | — |
| `name` | varchar(200) | User-defined name |
| `description` | text | Optional description |
| `sql` | text | The saved SELECT query (analytics schema only) |
| `created_by_id` | FK → auth.User | — |
| `is_shared` | boolean | If true, visible to all Division H roles with SQL Explorer access |
| `last_run_at` | timestamptz | — |
| `created_at` | timestamptz | — |
| `updated_at` | timestamptz | — |

---

### Table: `analytics_query_history`

Per-user SQL query execution history for the H-06 Warehouse SQL Explorer. Ring-buffer: only the last 50 queries per user are retained (auto-deleted FIFO). Not an audit table — for operator convenience only.

| Field | Type | Notes |
|---|---|---|
| `id` | bigint PK | — |
| `user_id` | FK → auth.User | — |
| `sql` | text | The executed SQL query |
| `executed_at` | timestamptz | — |
| `duration_ms` | int | Query execution time |
| `row_count` | int | Rows returned (UI cap: 10,000) |
| `status` | varchar(10) | `OK` · `ERROR` · `TIMEOUT` |
| `error_message` | varchar(500) | Truncated error text; no full SQL echoed in error field |

---

### Table: `analytics_audit_log`

Immutable audit trail for all significant Division H actions. Append-only — no UPDATE or DELETE on this table.

| Field | Type | Notes |
|---|---|---|
| `id` | bigint PK | — |
| `actor_id` | FK → auth.User | Who performed the action |
| `actor_role` | varchar(50) | Role at time of action (denormalized for historical accuracy) |
| `action` | varchar(100) | `PIPELINE_TRIGGERED` · `PIPELINE_FORCE_STOPPED` · `AI_BATCH_CREATED` · `AI_BATCH_CANCELLED` · `MCQ_APPROVED` · `MCQ_REJECTED` · `MCQ_AUTO_REJECTED` · `MCQ_SKIPPED` · `REPORT_PUBLISHED` · `REPORT_SUBMITTED` · `REPORT_FEEDBACK_GIVEN` · `TEMPLATE_ARCHIVED` · `MODEL_CONFIG_CREATED` · `MODEL_CONFIG_UPDATED` · `MODEL_CONFIG_KEY_ROTATED` · `SQL_QUERY_EXECUTED` · `SQL_QUERY_EXECUTED_SHARED` · `EXPORT_REQUESTED` · `EXPORT_DOWNLOADED` · `CSM_NOTIFIED` · `ANOMALY_DISMISSED` · `QUESTION_FLAGGED` · `QUESTION_ARCHIVED` · `DOWNLOAD_LINK_REGENERATED` |
| `object_type` | varchar(100) | e.g., `analytics_ai_batch`, `analytics_report_template`, `analytics_pipeline_run` |
| `object_id` | bigint | PK of the affected object |
| `detail` | jsonb | Action-specific context: e.g., `{"batch_ref": "AIB-202409-0042", "count": 50}` for batch creation |
| `ip_address` | inet | Request IP (for security audit) |
| `created_at` | timestamptz | — |

**Indexed on:** `actor_id`, `action`, `object_type + object_id`, `created_at`.

**Who writes:** All write actions in H-06, H-07, H-08 write an audit log entry automatically via a Django signal or explicit service call. Read-only pages (H-01 through H-05) do not write audit entries except for export requests.

**Retention:** 7 years (DPDPA 2023 audit requirement).

---

## Data Retention Policy

| Table | Retention | Mechanism |
|---|---|---|
| `analytics_daily_snapshot` | 3 years | Nightly cleanup task deletes rows where `snapshot_date < NOW() - INTERVAL '3 years'` |
| `analytics_question_stats` | Indefinite while question exists | Row deleted when question archived in global registry |
| `analytics_institution_engagement` | 2 years of weekly snapshots | Delete rows where `week_start < NOW() - INTERVAL '2 years'` |
| `analytics_cohort_snapshot` | Indefinite (monthly, low volume) | No automated deletion |
| `analytics_ai_batch` | 2 years | Batches older than 2 years archived to cold storage (R2) |
| `analytics_ai_generated_mcq` | 2 years | Deleted with parent batch |
| `analytics_ai_model_config` | Indefinite (configs are few) | Soft-delete only (`is_active = false`) |
| `analytics_report_template` | Indefinite (configs are few) | Soft-delete via ARCHIVED status |
| `analytics_report_delivery` | 1 year | Delete rows where `delivered_at < NOW() - INTERVAL '1 year'` |
| `analytics_pipeline_run` | 90 days | Delete rows where `started_at < NOW() - INTERVAL '90 days'` |
| `analytics_export_request` | 30 days after expiry | Delete rows where `expires_at < NOW() - INTERVAL '30 days'` |
| `analytics_saved_query` | Until manually deleted | User-managed |
| `analytics_query_history` | 50 most recent per user | Auto-deleted FIFO; no time-based retention |
| `analytics_infrastructure_event` | 90 days | Delete rows where `synced_at < NOW() - INTERVAL '90 days'` |
| `analytics_audit_log` | **7 years** | DPDPA 2023 compliance — no automated deletion before 7 years |

---

## Celery Tasks

### 1. `aggregate_daily_platform_metrics`

**Schedule:** Daily at 01:00 IST
**Queue:** `analytics`
**Duration target:** < 15 min

Scans all 2,050 tenant schemas using Django's `connection.set_schema()` pattern. For each metric key, executes a SQL aggregate query per tenant schema, accumulates results, and writes to `analytics_daily_snapshot` for `snapshot_date = yesterday`.

**Metrics computed:**
- `active_institutions` — distinct institutions with ≥1 exam attempt that day
- `active_institutions_mtd` — running cumulative distinct institution count from the 1st of the current month to yesterday (re-computed each nightly run). Used by H-01 "Active Institutions (MTD)" KPI tile to avoid double-counting institutions active on multiple days.
- `exam_attempts_total` — sum of exam attempt records
- `exam_completions_total` — completed (submitted) attempt records
- `new_students` — students whose first attempt was yesterday
- `avg_score_pct` — mean score across all attempts
- `avg_completion_rate` — completions ÷ attempts
- `notification_sent_total` — notifications dispatched
- `content_published_total` — MCQs published to live bank
- `re_attempt_rate` — multi-attempt enrollments ÷ total enrollments (cohort-wide; per domain dimension)
- `cohort_score_stagnation_rate` — % of rolling 30-day enrollment cohorts where the cohort's avg score on 5th+ attempt is ≤ 2pp above avg score on 1st attempt (DPDPA-compliant: aggregate cohort means only, no individual tracking)
- `question_bank_size` — distinct published question count per `exam_domain` dimension (pre-computed nightly; replaces the live DB query in H-01 domain table for question bank size)
- `anomaly_flags` — jsonb per dimension: computed anomaly conditions written into `analytics_daily_snapshot` as `metric_key = 'anomaly_{type}'` rows so H-01 reads them from the analytics schema instead of re-computing at page render time
- `avg_rank_delta` — cohort-level metric: average change in exam rank from first attempt to most recent attempt, per `exam_domain` dimension (DPDPA-compliant: computed as group mean, no individual student IDs). Written to `analytics_daily_snapshot` as `metric_key = 'avg_rank_delta'`, `dimension_type = 'exam_domain'`. Source for H-05 rank trend analysis.

Each metric computed with dimensions: overall + per exam_domain + per institution_type + per subscription_tier + per region_state.

**On failure:** Logs to `analytics_pipeline_run`. Sends in-app notification to Data Engineer (43) and Analytics Manager (42). Does not retry automatically — manual re-run required from H-06.

---

### 2. `compute_question_analytics`

**Schedule:** Starts immediately after Task 1 completes via Celery chain (typically 01:15–02:00 IST, depending on Task 1 duration). Not a fixed clock time — Celery chain ensures Task 2 begins only when Task 1 has finished.
**Queue:** `analytics`
**Duration target:** < 45 min (2M questions × CTT computation)

For each question in the global question registry:
- Queries attempt data from all tenant schemas (only schemas where this question was used — skips schemas with no record)
- Computes: `difficulty_index`, `discrimination_index`, `omission_rate`, `distractor_stats`
- Sets `quality_flag` based on thresholds
- Updates `analytics_question_stats` (upsert on `question_id`)

**Discrimination index computation:** Point-biserial correlation between item score (0/1) and total exam score, computed from attempt data. Requires minimum 30 attempts for a valid D value (questions with fewer attempts marked `quality_flag = INSUFFICIENT_ATTEMPTS`).

**Partial success handling:** If a tenant schema query fails (e.g., schema locked), logs the failure but continues with remaining schemas. Final row reflects data from successful schemas only. `tenants_failed` count written to `analytics_pipeline_run`.

---

### 3. `compute_institution_engagement`

**Schedule:** Weekly, Sunday at 03:00 IST
**Queue:** `analytics`

For each institution:
- Reads last 90 days of activity from that institution's tenant schema
- Computes engagement score (weighted formula documented in data model)
- Sets `churn_risk` classification
- Writes to `analytics_institution_engagement`

On CRITICAL churn risk (score < 30) for Enterprise/Professional tier institutions: triggers in-app notification to Customer Success Manager (53, Division J) with link to H-03 institution detail.

---

### 4. `compute_cohort_snapshots`

**Schedule:** Monthly, 1st of month at 04:00 IST
**Queue:** `analytics`

Reads student first-appearance dates from all tenant schemas. Groups by cohort month. Computes retention rates at 1/2/3/6/12 months. Writes to `analytics_cohort_snapshot`.

Privacy: no individual student IDs stored — only aggregate cohort counts.

---

### 5. `run_ai_generation_batch`

**Schedule:** On-demand (triggered by AI Generation Manager in H-07)
**Queue:** `ai_generation`
**Max concurrency:** 3 simultaneous batch generation tasks (to cap AI API spend and avoid rate-limit errors)

Picks up `analytics_ai_batch` records with `status = QUEUED`. Calls configured AI API with system prompt + user prompt template filled with batch parameters. Decrypts `api_key_encrypted` using AWS KMS at runtime — decrypted key held in memory only, never logged. Parses response into individual `analytics_ai_generated_mcq` records. Computes `question_text_hash` for each MCQ. Auto-rejects any MCQ whose hash matches an existing entry (`review_status = AUTO_REJECTED`, `review_note = 'Duplicate detected — question text matches existing MCQ'`). Updates batch status to `REVIEW_PENDING` on completion. Notifies AI Gen Manager (45) in-app: "Batch {batch_ref} — {N} MCQs ready for review ({D} duplicates auto-rejected)."

**Error handling:** If AI API call fails: exponential backoff (3 attempts, 60s/120s/300s delays). After 3 failures: status = `FAILED`, Data Engineer (43) and AI Gen Manager (45) notified.

---

### 6. `poll_ai_batch_status`

**Schedule:** Every 5 minutes (Celery Beat)
**Queue:** `ai_generation`

For AI providers that use async generation (batch APIs where results are not returned synchronously):
- Queries provider batch status endpoint for any `analytics_ai_batch` record with `status = GENERATING` and `celery_task_id` set
- If provider reports complete: fetches results, parses MCQs, updates batch to `REVIEW_PENDING`, notifies AI Gen Manager
- If provider reports failed: updates batch to `FAILED`, notifies Data Engineer + AI Gen Manager
- If provider reports still running and `generation_started_at` > 4 hours ago: marks as `FAILED` with error "Generation timeout — provider did not respond within 4 hours"

For synchronous providers (OpenAI synchronous calls): this task is a no-op (finds no GENERATING batches).

---

### 7. `generate_scheduled_reports`

**Schedule:** 1st of each month at 06:00 IST; also 1st of each quarter
**Queue:** `reports`
**Workers:** Minimum 5 dedicated `reports` queue workers required. Each institution report generation (PDF render + R2 upload) takes 2–30s. At 2,050 institutions × PDF + optional CSV/XLSX, peak load is ~2,050 tasks concurrently enqueued — 5 workers process these over ~10–40 minutes depending on template complexity.

For each published `analytics_report_template` with `schedule_type IN (MONTHLY, QUARTERLY, ANNUAL)` and `delivery_day` matching today:
- Fetches pre-aggregated data for the reporting period
- Renders report in requested output formats
- Stores in R2 private bucket
- Creates `analytics_report_delivery` records
- Sends in-app + email notification to institution admins with signed download URL (72h expiry). For `INSTITUTION_ADMIN` audience: notification sent to the institution's admin user(s) in-app (via F-06 notification hub) AND email with the signed R2 download URL. For `INTERNAL_EXEC` audience: in-app notification to Division H and Platform Admin only (no external delivery). For `DIVISION_H_ONLY` audience: visible in H-08 delivery log only (no notification sent). Institutions do not have a dedicated report portal — they access the signed URL from the notification email or in-app notification link.

---

### 8. `process_export_request`

**Schedule:** Triggered immediately when `analytics_export_request` is created
**Queue:** `exports`

Reads pre-aggregated analytics data matching the export filters. Generates CSV/XLSX file. Stores in R2. Updates `analytics_export_request` status to `READY`. Sends in-app notification to requester: "Export ready — download within 48h."

---

## Pipeline Dependency Chain

The nightly analytics pipelines must run in a specific order due to data dependencies. This is enforced using a Celery chain:

```python
# Scheduled daily at 01:00 IST via Celery Beat
chain(
    aggregate_daily_platform_metrics.si(),     # Task 1 — must complete first
    compute_question_analytics.si(),            # Task 2 — reads from tenant schemas independently but scheduled after Task 1
).apply_async()

# Weekly (independent chain, Sunday 03:00 IST)
compute_institution_engagement.apply_async()

# Monthly (independent, 1st of month 04:00 IST)
compute_cohort_snapshots.apply_async()

# Monthly (depends on analytics data being fresh, 1st of month 06:00 IST)
generate_scheduled_reports.apply_async()
```

**Dependency rules:**
- `compute_question_analytics` starts immediately when Task 1 completes (Celery chain — not a separate cron schedule). If Task 1 finishes at 01:47 IST, Task 2 starts at 01:47 IST. The "02:00" approximation in prior references is the expected latest start; the chain is the actual dependency mechanism. There is no fixed 02:00 trigger.
- `generate_scheduled_reports` (06:00 IST) depends on fresh analytics data. If nightly pipelines failed overnight, reports will contain stale data — this is flagged in H-06 pipeline monitor and Analytics Manager should delay manual send until re-run completes.
- `run_ai_generation_batch` and `process_export_request` are independent on-demand tasks — they run on separate queues (`ai_generation`, `exports`) and do not interfere with analytics pipelines.
- `poll_ai_batch_status` runs on `ai_generation` queue every 5 minutes — lightweight polling task, minimal interference.

**Queue isolation:**

| Queue | Tasks | Worker Count |
|---|---|---|
| `analytics` | Tasks 1–4 (nightly aggregation) | 2 workers (sequential by chain) |
| `ai_generation` | Tasks 5–6 (AI batch + polling) | 3 workers (max concurrency cap) |
| `reports` | Task 7 (report generation) | 5 workers minimum |
| `exports` | Task 8 (data export) | 2 workers |

---

## Cross-Page Workflows

### Workflow 1: Question Quality Degradation Response

```
H-04 daily view → Data Analyst identifies questions with D < 0.2 (poor discrimination)
  → Flags batch for review → Analytics Manager notified
  → Decision: commission AI replacements OR archive
  → If AI replacements: H-07 AI Gen Manager creates batch for same domain/topic
  → Batch generates → AI Manager reviews → Approved MCQs → Division D queue
  → Division D SME reviews → approved → H-04 shows improved bank quality next cycle
```

### Workflow 2: Institution Churn Risk Intervention

```
H-03 Celery task computes CRITICAL churn risk (engagement score < 30)
  → In-app alert to CSM (Division J, role 53)
  → Data Analyst (H-03) drills into institution detail drawer
  → Generates ad-hoc report via H-08 Report Studio
  → CSM + Analyst discuss intervention with Account Manager (Division J, role 54)
  → H-08 monthly report scheduled for at-risk institution (more frequent delivery)
```

### Workflow 3: AI MCQ Pipeline to Division D

```
AI Gen Manager (H-07) creates batch: domain=SSC, topic=Data Interpretation, count=50
  → Celery `run_ai_generation_batch` triggers
  → 50 MCQs generated; any duplicates immediately AUTO_REJECTED via SHA-256 hash comparison (counted in batch stats as auto-rejected; not shown in review queue — nothing to review for duplicates) → status = REVIEW_PENDING
  → AI Gen Manager reviews each MCQ in H-07 review drawer
  → Approved: 42/50 → status = APPROVED → Celery creates Division D content queue entries
  → Division D SME reviews AI-flagged entries (see entry has `source = AI_GENERATED` tag)
  → SME approves/edits/rejects → publishes to live bank
  → H-01 dashboard shows AI contribution to question bank (KPI tile)
```

### Workflow 4: Data Pipeline Failure Recovery

```
Celery `aggregate_daily_platform_metrics` fails at 01:30 IST
  → analytics_pipeline_run record: status = FAILED, error_message = "<traceback>"
  → In-app notification to Data Engineer (43) and Analytics Manager (42)
  → H-01 dashboard shows "⚠ Data may be stale — last successful run: yesterday 01:04"
  → Data Engineer investigates in H-06 (pipeline monitor)
  → Fixes root cause → triggers manual re-run from H-06
  → Re-run succeeds → staleness indicator clears on H-01
```

### Workflow 5: Scheduled Institution Report Delivery

```
Report Designer (46) builds template in H-08 (monthly summary for coaching centres)
  → Analytics Manager (42) approves and publishes template
  → Schedule: every 1st of month at 06:00 IST
  → Celery `generate_scheduled_reports` runs
  → H-08 delivery log shows: 98/100 coaching centres delivered, 2 failed
  → Report Designer sees failure reason → fixes data mapping → manual re-send
```

---

## Integration Points

| System | How Division H Interacts |
|---|---|
| Division D (Content) | AI-approved MCQs enter Division D's content review queue as `source = AI_GENERATED` entries |
| Division G (BGV) | H-01 shows BGV coverage KPI tile (read from `bgv_institution_compliance`); H-03 shows per-institution BGV status |
| Division J (Customer Success) | H-03 Celery task notifies CSM (53) on CRITICAL churn risk; H-08 reports are used by Account Managers |
| Division F (Exam Ops) | H-05 reads pre-aggregated exam performance data; SLA correlation reads from `analytics_infrastructure_event` (nightly sync from Division F `incident_log` via Task 1); all Division H in-app notifications routed through Division F F-06 notification hub |
| Division B (Product) | H-01 shows feature flag adoption metrics; A/B test results are visualised in H-02 student performance |
| Division A (Exec) | H pages are linked from A-01 executive dashboard for deep-dive access; A-24 executive reports uses H-08 templates |
| Institution Portal (tenant) | H-08 generated reports delivered to institution admin dashboards via signed R2 URLs |
| R2 (Cloudflare) | All exported files and reports stored in private R2 bucket; 72h signed URL for downloads |
| Notification Hub (F-06) | H-07 batch complete / H-06 pipeline failure / H-03 churn risk → in-app notifications via Division F notification system |

---

*Pages-list complete.*
*Division H covers: Analytics Dashboard (platform MIS) → Student Performance (cohort + dropout) → Institution Analytics (engagement scoring + churn risk) → Question Intelligence (CTT metrics for 2M+ questions) → Exam & Domain Analytics (cross-domain performance) → Data Pipeline Monitor (Data Engineer workspace) → AI MCQ Generation (batch management + review) → Report Studio (institution-facing template builder) → Export Manager (self-serve data export).*
