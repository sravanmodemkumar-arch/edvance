# Division J — Customer Success: Pages List & Architecture

> EduForge platform-level Customer Success covering 2,050 institutions and 2.4M–7.6M students.
> 4 original roles + 2 added roles (93, 94) = **6 roles total**.
> CS owns retention, expansion, escalation resolution, NPS programme, and institution health scoring.

---

## Scale Context

| Segment | Count | Avg ARR/Institution (Est.) | Renewal Risk Profile |
|---|---|---|---|
| Schools | 1,000 | ₹60K–₹2.4L | High churn if exam utility low; admin turnover |
| Colleges | 800 | ₹1.2L–₹6L | Stable; driven by placement/entrance exam board decisions |
| Coaching Centres | 100 | ₹3L–₹18L | High ARR; high-touch; usage intensity is primary churn signal |
| Institution Groups | 150 | ₹6L–₹60L | Complex; multi-level contacts; board-level relationships |
| **Total** | **2,050** | — | **~₹18Cr–₹90Cr ARR portfolio (estimate)** |

Health score recomputed nightly for all 2,050 institutions from 5 weighted components.

---

## Page Inventory

| Page | Route | Primary Role | Purpose |
|---|---|---|---|
| J-01 | `/csm/` | CSM (#53) | Real-time portfolio health dashboard — heatmap, at-risk feed, renewals, NPS |
| J-02 | `/csm/accounts/` | CSM + AM (#53, #54) | Paginated institution portfolio — sortable, filterable, bulk actions |
| J-03 | `/csm/accounts/{id}/` | All CS roles | Full account profile — health, touchpoints, playbooks, renewals, escalations |
| J-04 | `/csm/renewals/` | AM + Renewal Exec (#54, #56) | Renewal pipeline — Kanban + list; ARR tracking; stage management |
| J-05 | `/csm/escalations/` | Escalation Manager (#55) | Active CS escalations — severity, cross-division coordination, ARR at risk |
| J-06 | `/csm/playbooks/` | CSM + ISM (#53, #94) | Playbook template library + active instance tracker |
| J-07 | `/csm/feedback/` | CSM + CS Analyst (#53, #93) | NPS/CSAT survey management, verbatim feedback, promoter/detractor analysis |
| J-08 | `/csm/reports/` | CSM + CS Analyst (#53, #93) | GRR/NRR, churn analysis, cohort analysis, CSM performance, playbook ROI |

---

## Division J Roles

| # | Role | Level | Owns | Cannot Do |
|---|---|---|---|---|
| 53 | Customer Success Manager | 3 | Portfolio strategy, playbook governance, NPS programme, health score oversight, renewal pipeline co-ownership, escalation visibility | Billing config, infra config |
| 54 | Account Manager | 3 | Institution relationship management, upsell, expansion seats, renewal execution | Bulk survey dispatch; playbook template approval |
| 55 | Escalation Manager | 3 | Critical institution complaints, SLA breach coordination, cross-division war-room for account-threatening incidents | Content approval; billing modification |
| 56 | Renewal Executive | 1 | Subscription expiry tracking, renewal reminders, stage updates to COMMITTED | Cannot confirm won/lost renewal (AM or CSM only); no data writes outside renewal module |
| 93 | Customer Success Analyst | 1 | Health score model maintenance, churn signal analysis, cohort analytics, NPS/CSAT data analysis, weekly CS data pack | No customer-facing comms; no playbook execution; no billing access |
| 94 | Implementation Success Manager | 3 | First-90-day post-onboarding success, time-to-value tracking, go-live readiness, first EBR facilitation; handoff from Div-I Onboarding Specialist (#51) | Billing config; renewal ownership hands off to AM at day 90; no L2/L3 support queue |

---

## Role-to-Page Access Matrix

| Page | 53 CSM | 54 AM | 55 Escalation | 56 Renewal | 93 Analyst | 94 ISM |
|---|---|---|---|---|---|---|
| J-01 Dashboard | Full | My-portfolio + renewal strip | Escalations + at-risk | Renewal strip + at-risk | Read-only full + anomaly panel | First-90-day portfolio |
| J-02 Portfolio | Full | Own assigned accounts | Read all | Read all | Read all + export | Own implementations |
| J-03 Account Profile | Full all tabs | Full (except NPS send on non-assigned) | Escalations tab full; others read | Renewals tab full; others read | Read all tabs; no actions | Full for first-90-day accounts; read-only after day 90 |
| J-04 Renewals | Full + can win/lose | Full + can win/lose | Read only | Full except win/lose | Read + export | Own implementations renewal strip only |
| J-05 Escalations | Full read + assign | Read | Full all actions | Read | Read | Read |
| J-06 Playbooks | Full (create/edit templates + start instances) | Start instances; read templates | Read | No access | Read | Start instances for own accounts; read templates |
| J-07 NPS Feedback | Full (send + review) | Send for own accounts | Read | Read | Full read + export | Send for own accounts |
| J-08 Reports | Full | Own accounts section | Escalation metrics only | Renewal metrics only | Full + export | Implementation success metrics only |

---

## Data Model

### `csm_institution_health`

| Column | Type | Notes |
|---|---|---|
| id | bigserial PK | — |
| institution_id | int FK → institution UNIQUE | One row per institution; upserted by Celery Task J-1 nightly |
| health_score | smallint NOT NULL | 0–100; composite of 5 components |
| prev_health_score | smallint | Last computed score; used to compute delta |
| score_delta | smallint | Signed: positive = improving; negative = degrading |
| engagement_tier | varchar(20) NOT NULL | `HEALTHY` (85–100) · `ENGAGED` (65–84) · `AT_RISK` (45–64) · `CRITICAL` (25–44) · `CHURNED_RISK` (0–24) |
| institution_type | varchar(20) NOT NULL | `SCHOOL` · `COLLEGE` · `COACHING` · `GROUP`; denormalised from `institution` for fast filter/aggregation without join |
| product_adoption_score | smallint NOT NULL | 0–25: exams created 30d (10 pts) + active_user_ratio (10 pts) + features_activated_pct (5 pts) |
| engagement_score | smallint NOT NULL | 0–25: DAU/MAU ratio (15 pts) + session_frequency_weekly (10 pts) |
| support_burden_score | smallint NOT NULL | 0–20: inverted critical/high tickets 30d (10 pts) + csat_avg 30d (10 pts) |
| payment_health_score | smallint NOT NULL | 0–20: days_past_due inverted (15 pts) + payment_history_12m (5 pts) |
| relationship_score | smallint NOT NULL | 0–10: touchpoint_recency_days inverted (5 pts) + ebr_completed_90d (3 pts) + nps_contribution (2 pts) |
| churn_probability_pct | decimal(5,2) NOT NULL | 0.00–100.00; computed by logistic regression on historical churn cohort; null for new institutions (<30 days) |
| is_new_institution | boolean NOT NULL DEFAULT false | True if institution age < 30 days; score computation deferred, health_score defaults to 65 (ENGAGED) |
| days_to_renewal | int | Nullable; null if no active renewal record |
| active_users_30d | int NOT NULL DEFAULT 0 | Distinct users who logged in in last 30 days |
| total_enrolled | int NOT NULL DEFAULT 0 | Total enrolled users in tenant |
| dau_7d_avg | decimal(8,2) NOT NULL DEFAULT 0 | Average daily active users over last 7 days |
| exams_created_30d | int NOT NULL DEFAULT 0 | Exams created (or activated) in last 30 days |
| features_activated_pct | decimal(5,2) NOT NULL DEFAULT 0 | % of institution-type-applicable modules enabled; denominator varies by institution type |
| content_consumed_hrs_30d | decimal(10,2) NOT NULL DEFAULT 0 | Total video watch hours in last 30 days |
| sessions_30d | int NOT NULL DEFAULT 0 | Portal login sessions in last 30 days |
| last_login_at | timestamptz | Most recent login across any institution user |
| last_exam_at | timestamptz | Most recent exam created or activated |
| last_portal_access_at | timestamptz | Most recent portal session |
| computed_at | timestamptz NOT NULL | When this row was last recomputed by Task J-1 |
| created_at | timestamptz DEFAULT now() | — |

**Indexes:**
- `CREATE INDEX csm_health_engagement_tier_idx ON csm_institution_health (engagement_tier)` — for tier-filter queries on J-02
- `CREATE INDEX csm_health_score_idx ON csm_institution_health (health_score ASC)` — for at-risk feed sorting
- `CREATE INDEX csm_health_institution_type_idx ON csm_institution_health (institution_type)` — for segment filter

**Tier thresholds (configurable via `csm_config` key-value table):**
```
HEALTHY:       85 ≤ score ≤ 100
ENGAGED:       65 ≤ score ≤ 84
AT_RISK:       45 ≤ score ≤ 64
CRITICAL:      25 ≤ score ≤ 44
CHURNED_RISK:  0  ≤ score ≤ 24
```

---

### `csm_touchpoint`

| Column | Type | Notes |
|---|---|---|
| id | bigserial PK | — |
| institution_id | int FK → institution NOT NULL | — |
| performed_by_id | int FK → user NOT NULL | The CS team member who performed or logged it |
| touchpoint_type | varchar(30) NOT NULL | `CALL` · `EMAIL` · `EBR` · `QBR` · `TRAINING` · `ESCALATION_UPDATE` · `ONBOARDING_CHECKIN` · `RENEWAL_DISCUSSION` · `PRODUCT_WALKTHROUGH` · `INTERNAL_NOTE` |
| direction | varchar(20) NOT NULL | `OUTBOUND` (CS initiated) · `INBOUND` (institution initiated) · `INTERNAL` (internal note, no contact) |
| subject | varchar(500) NOT NULL | — |
| notes | text | Free-form notes; markdown supported |
| outcome | varchar(200) | Short outcome summary |
| next_action | text | What happens next |
| next_action_date | date | When next action is due; surfaced in J-03 as reminder |
| nps_ad_hoc_score | smallint | 0–10; set if NPS verbally collected during call (ad-hoc, not via survey) |
| is_deleted | boolean NOT NULL DEFAULT false | Soft-delete flag; deleted touchpoints hidden from all UI views but retained for audit trail |
| deleted_at | timestamptz | Set when `is_deleted` → true; null for active records |
| deleted_by_id | int FK → user | Who soft-deleted this record |
| created_at | timestamptz DEFAULT now() | — |
| updated_at | timestamptz DEFAULT now() | — |

```sql
CREATE INDEX csm_touchpoint_institution_active ON csm_touchpoint (institution_id, created_at DESC) WHERE is_deleted = false;
```

---

### `csm_renewal`

| Column | Type | Notes |
|---|---|---|
| id | bigserial PK | — |
| institution_id | int FK → institution NOT NULL | — |
| renewal_date | date NOT NULL | Contract renewal/expiry date; sourced from `billing_subscription.expires_at` |
| arr_value_paise | bigint NOT NULL CHECK (arr_value_paise > 0) | Annual recurring revenue in paise (₹1 = 100 paise); avoids decimal precision issues |
| plan_name | varchar(100) NOT NULL | Current subscription plan name |
| seats | int NOT NULL CHECK (seats > 0) | Contracted seat count |
| stage | varchar(20) NOT NULL | `IDENTIFIED` · `OUTREACH_SENT` · `QUOTE_SENT` · `NEGOTIATING` · `COMMITTED` · `RENEWED` · `CHURNED` · `EXPANSION`; default `IDENTIFIED` |
| probability_pct | smallint NOT NULL DEFAULT 50 CHECK (probability_pct BETWEEN 0 AND 100) | 0–100; manually set by AM or Renewal Exec |
| assigned_csm_id | int FK → user | Customer Success Manager owner |
| assigned_am_id | int FK → user | Account Manager owner |
| renewal_executive_id | int FK → user | Renewal Executive tracking this renewal |
| churn_reason | varchar(50) | Populated when stage = `CHURNED`; see enum below |
| expansion_arr_paise | bigint CHECK (expansion_arr_paise > 0) | Populated when stage = `EXPANSION`; delta ARR added; must be positive |
| won_at | timestamptz | Set when stage transitions to `RENEWED` or `EXPANSION` |
| lost_at | timestamptz | Set when stage transitions to `CHURNED` |
| notes | text | Free-form renewal notes; visible to AM, CSM, Renewal Exec |
| previous_renewal_id | int FK self → csm_renewal | Chain: links current renewal to last closed renewal for history |
| created_at | timestamptz DEFAULT now() | — |
| updated_at | timestamptz DEFAULT now() | — |

**Active renewal uniqueness constraint:**
```sql
CREATE UNIQUE INDEX csm_renewal_one_active_per_institution
  ON csm_renewal (institution_id)
  WHERE stage NOT IN ('RENEWED', 'CHURNED');
```
Only one in-flight renewal per institution at any time. New renewal cycle begins only after previous is closed (RENEWED or CHURNED). Application must check before creating a new record; DB partial unique index is the final guard.

**Stage transition rules:**
- Only AM (#54), CSM (#53) can transition to `RENEWED` or `CHURNED` (won/lost gate)
- Renewal Executive (#56) can update all stages up to `COMMITTED`
- `EXPANSION` stage: requires AM + CSM agreement; triggers new billing record creation in Division M
- Auto-created by Celery Task J-1 if no renewal record exists for an institution with an active subscription; auto-creates with `stage=IDENTIFIED`, `renewal_date` from `billing_subscription.expires_at`, `arr_value_paise` from subscription ARR

**Churn reason enum (9 values):**
`PRICING`, `BUDGET_CUT`, `SWITCHED_COMPETITOR`, `PRODUCT_FIT`, `LOW_USAGE`, `ADMIN_TURNOVER`, `INSTITUTION_CLOSURE`, `DELAYED_DECISION`, `UNKNOWN`

---

### `csm_escalation`

| Column | Type | Notes |
|---|---|---|
| id | bigserial PK | — |
| institution_id | int FK → institution NOT NULL | — |
| title | varchar(500) NOT NULL | — |
| severity | varchar(20) NOT NULL | `P1_CRITICAL` · `P2_HIGH` · `P3_MEDIUM` |
| status | varchar(30) NOT NULL | `OPEN` · `IN_PROGRESS` · `PENDING_INSTITUTION` · `PENDING_DIVISION` · `RESOLVED` · `CLOSED`; default `OPEN` |
| opened_by_id | int FK → user NOT NULL | — |
| assigned_to_id | int FK → user | Escalation Manager (#55) or CSM (#53) |
| description | text NOT NULL | Full description of the issue |
| root_cause | text | Populated after investigation |
| resolution | text | Populated when resolving |
| commit_date | date | Manually set by Escalation Manager; preferred ≤ `commit_sla_at` |
| commit_sla_at | timestamptz NOT NULL | Auto-computed at creation: P1 = `opened_at + 4h`; P2 = `opened_at + 24h`; P3 = `opened_at + 72h` |
| resolve_sla_at | timestamptz NOT NULL | Auto-computed at creation: P1 = `opened_at + 24h`; P2 = `opened_at + 72h`; P3 = `opened_at + 7d` |
| commit_sla_breached | boolean NOT NULL DEFAULT false | Set true if `commit_date IS NULL` and `now() > commit_sla_at`; evaluated nightly by Task J-1 |
| resolve_sla_breached | boolean NOT NULL DEFAULT false | Set true if `resolved_at IS NULL` and `now() > resolve_sla_at`; evaluated nightly by Task J-1 |
| support_ticket_ids | int[] DEFAULT '{}' | Linked Division I ticket IDs |
| cross_division_notes | jsonb DEFAULT '[]' | Array of `{division, contact_name, status, note, logged_at, logged_by_id}`; `logged_by_id` is FK to user for audit |
| account_at_risk | boolean NOT NULL DEFAULT false | True = institution has threatened to churn; surfaces in J-01 red flag |
| arr_at_risk_paise | bigint | Populated when `account_at_risk=true`; copied from active renewal ARR |
| last_notify_csm_at | timestamptz | Set when Escalation Manager triggers [Escalate to CSM]; enforces 60-min cooldown per escalation — endpoint checks `now() - last_notify_csm_at < 60 min` and returns 429 if within cooldown |
| opened_at | timestamptz NOT NULL DEFAULT now() | — |
| resolved_at | timestamptz | Set when status → RESOLVED |
| closed_at | timestamptz | Set when status → CLOSED (after institution confirms) |
| created_at | timestamptz DEFAULT now() | — |
| updated_at | timestamptz DEFAULT now() | — |

**SLA definitions (hard targets, breaches tracked in J-08):**
- P1_CRITICAL: commit_sla = 4h from open; resolve_sla = 24h from open
- P2_HIGH: commit_sla = 24h from open; resolve_sla = 72h from open
- P3_MEDIUM: commit_sla = 72h from open; resolve_sla = 7d from open

Both `commit_sla_at` and `resolve_sla_at` are shown as countdown timers in the J-05 Escalation Detail Drawer. Breached timers display in red.

**Status transition rules (application-level; enforced in Django model `clean()` method):**
Valid forward transitions only: `OPEN → IN_PROGRESS → PENDING_INSTITUTION | PENDING_DIVISION → RESOLVED → CLOSED`. Backward transitions (e.g., RESOLVED → OPEN) are rejected — escalations must be re-opened by creating a new escalation if a resolved issue resurfaces. Exception: admin staff can force-set status in Django admin for data corrections. A DB CHECK constraint is intentionally NOT used to preserve admin override capability.

**FK ON DELETE behaviour:**
- `institution_id → institution` : ON DELETE RESTRICT (preserve historical escalations for churn analysis; institution cannot be deleted with open escalations)
- `assigned_to_id → user` : ON DELETE SET NULL (escalation un-assigns if manager account deleted; Task J-2 picks up unassigned escalations)
- `opened_by_id → user` : ON DELETE SET NULL (preserve audit record)

---

### `csm_playbook_template`

| Column | Type | Notes |
|---|---|---|
| id | bigserial PK | — |
| name | varchar(200) NOT NULL | — |
| description | text | — |
| trigger_type | varchar(30) NOT NULL | `ONBOARDING_SUCCESS` · `AT_RISK_RECOVERY` · `RENEWAL_PREP` · `EXPANSION` · `EBR` · `CHURN_SAVE` · `CUSTOM` |
| target_segment | varchar(20) NOT NULL DEFAULT 'ALL' | `ALL` · `SCHOOL` · `COLLEGE` · `COACHING` · `GROUP` |
| tasks | jsonb NOT NULL | Array of `{step: int, title: str, description: str, owner_role: str, touchpoint_type: str, due_days_offset: int, required: bool}` — `touchpoint_type` mirrors `csm_touchpoint.touchpoint_type` enum (CALL, EMAIL, EBR, etc.); used as a hint for what action the task represents; nullable for INTERNAL_NOTE tasks |
| estimated_duration_days | int NOT NULL | Total duration in days |
| is_active | boolean NOT NULL DEFAULT true | Inactive templates cannot be started; existing instances continue |
| created_by_id | int FK → user NOT NULL | CSM (#53) only can create/edit templates |
| created_at | timestamptz DEFAULT now() | — |
| updated_at | timestamptz DEFAULT now() | — |

---

### `csm_playbook_instance`

| Column | Type | Notes |
|---|---|---|
| id | bigserial PK | — |
| template_id | int FK → csm_playbook_template NOT NULL | — |
| institution_id | int FK → institution NOT NULL | — |
| assigned_to_id | int FK → user NOT NULL | CSM (#53) or ISM (#94) |
| status | varchar(20) NOT NULL | `ACTIVE` · `COMPLETED` · `ABANDONED`; default `ACTIVE` |
| task_states | jsonb NOT NULL | Mirrors template tasks with `{step, completed: bool, completed_at, completed_by_id, note}` per task |
| tasks_total | int NOT NULL | Snapshot of template task count at instance creation |
| tasks_completed | int NOT NULL DEFAULT 0 | Incremented on task completion |
| notes | text | Instance-level notes |
| started_at | timestamptz NOT NULL DEFAULT now() | — |
| completed_at | timestamptz | Set when tasks_completed = tasks_total |
| abandoned_at | timestamptz | Set when status → ABANDONED |
| created_at | timestamptz DEFAULT now() | — |
| updated_at | timestamptz DEFAULT now() | — |

---

### `csm_nps_survey`

| Column | Type | Notes |
|---|---|---|
| id | bigserial PK | — |
| institution_id | int FK → institution NOT NULL | — |
| survey_type | varchar(30) NOT NULL | `QUARTERLY_NPS` · `POST_ONBOARDING_NPS` · `RENEWAL_CSAT` · `EBR_FEEDBACK` · `AD_HOC` |
| sent_to_email | varchar(254) NOT NULL | — |
| sent_to_name | varchar(200) NOT NULL | — |
| sent_by_id | int FK → user NOT NULL | — |
| sent_at | timestamptz NOT NULL | — |
| responded_at | timestamptz | Null until response received |
| nps_score | smallint | 0–10; null for CSAT surveys |
| csat_score | smallint | 1–5; null for NPS surveys |
| promoter_category | varchar(20) | `PROMOTER` (9–10) · `PASSIVE` (7–8) · `DETRACTOR` (0–6); computed from nps_score; null for CSAT |
| verbatim_feedback | text | Optional open text from respondent |
| follow_up_required | boolean NOT NULL DEFAULT false | Flagged by CSM after reviewing response |
| follow_up_notes | text | CSM notes on follow-up action |
| survey_link_token | varchar(100) UNIQUE NOT NULL | Unique token for public survey URL; generated using `secrets.token_urlsafe(48)`; never exposes internal IDs |
| link_expires_at | timestamptz NOT NULL | `sent_at + interval '14 days'`; submission rejected after expiry |
| reminder_sent_at | timestamptz | Set when Celery Task J-3 sends 7-day reminder; prevents duplicate reminders |
| superseded_by_id | int FK → csm_nps_survey | Set when a Resend creates a new row to replace this one; old row is inactive; null = current active survey |
| dispatch_channel | varchar(20) NOT NULL DEFAULT 'EMAIL' | Channel used to send this survey: `EMAIL` · `WHATSAPP`; COACHING institutions receive QUARTERLY_NPS via WhatsApp (F-06); all others receive via email |
| created_at | timestamptz DEFAULT now() | — |
| updated_at | timestamptz DEFAULT now() | — |

**Supersession rule:** When a survey is resent via [Resend], a new `csm_nps_survey` row is created. The old row gets `superseded_by_id = new_row.id`. The public survey endpoint rejects submissions to tokens where `superseded_by_id IS NOT NULL`.

**NPS response threshold rules:**
- Portfolio-wide KPI tiles and `csm_weekly_snapshot.nps_score`: require **≥ 10 responses** in the period (statistical minimum for credibility).
- Per-month trend chart data points (in J-07 NPS Trend Chart and J-01 NPS Trend Chart): require **≥ 5 responses** per month — monthly samples are smaller by nature; fewer responses are acceptable for trend visualisation (displayed with a "low sample" indicator icon). These thresholds are intentionally different.

---

### `csm_account_assignment`

| Column | Type | Notes |
|---|---|---|
| id | bigserial PK | — |
| institution_id | int FK → institution UNIQUE NOT NULL | One assignment record per institution |
| csm_id | int FK → user | Customer Success Manager (#53); nullable if unassigned |
| account_manager_id | int FK → user | Account Manager (#54); nullable |
| ism_id | int FK → user | Implementation Success Manager (#94); nullable; auto-set on onboarding complete from Div-I |
| ism_handoff_date | date | Date ISM received handoff from Div-I Onboarding Specialist; used to compute 90-day ISM tenure |
| ism_tenure_end_date | date | `ism_handoff_date + 90 days`; after this date ISM read-only, AM takes ownership |
| notes | text | — |
| assigned_by_id | int FK → user NOT NULL | Who made the assignment |
| created_at | timestamptz DEFAULT now() | — |
| updated_at | timestamptz DEFAULT now() | — |

---

### `csm_weekly_snapshot` (pre-computed)

| Column | Type | Notes |
|---|---|---|
| id | bigserial PK | — |
| snapshot_date | date UNIQUE NOT NULL | Monday of the week |
| total_institutions | int NOT NULL | — |
| healthy_count | int NOT NULL | tier = HEALTHY |
| engaged_count | int NOT NULL | tier = ENGAGED |
| at_risk_count | int NOT NULL | tier = AT_RISK |
| critical_count | int NOT NULL | tier = CRITICAL |
| churned_risk_count | int NOT NULL | tier = CHURNED_RISK |
| avg_health_score | decimal(5,2) NOT NULL | — |
| median_health_score | decimal(5,2) NOT NULL | — |
| renewals_due_30d | int NOT NULL | Renewals within 30 days at snapshot time |
| arr_due_30d_paise | bigint NOT NULL | ARR value of those renewals |
| arr_committed_quarter_paise | bigint NOT NULL | ARR in COMMITTED + RENEWED stage this quarter |
| nps_score | decimal(5,2) | Calculated NPS = (Promoters% - Detractors%) × 100; null if < 10 responses |
| csat_avg | decimal(4,2) | Average CSAT score (1–5 scale); null if no responses |
| promoter_pct | decimal(5,2) | — |
| detractor_pct | decimal(5,2) | — |
| grr_pct | decimal(5,2) | Gross Revenue Retention: MIN(ARR_renewed_base, ARR_due) / ARR_due; capped at 100%; excludes expansion delta; computed by Task J-5 |
| nrr_pct | decimal(5,2) | Net Revenue Retention: (ARR_renewed_base + expansion_arr) / ARR_due; can exceed 100% when expansion outpaces churn; computed by Task J-5 |
| open_escalations | int NOT NULL | — |
| p1_escalations | int NOT NULL | P1_CRITICAL open |
| active_playbooks | int NOT NULL | Instances with status = ACTIVE |
| completed_playbooks_7d | int NOT NULL | Instances completed in last 7 days |
| created_at | timestamptz DEFAULT now() | — |

---

### `csm_health_history` (daily snapshot, retained 90 days)

> Required for the 90-day health trend chart in J-03 Account Profile.
> `csm_institution_health` holds only the latest row per institution (upserted nightly).
> History rows are inserted — never updated — by Task J-1.

| Column | Type | Notes |
|---|---|---|
| id | bigserial PK | — |
| institution_id | int FK → institution NOT NULL | — |
| health_score | smallint NOT NULL | Score at time of computation |
| engagement_tier | varchar(20) NOT NULL | Tier at time of computation |
| score_delta | smallint | Delta vs previous day's history row for this institution |
| computed_date | date NOT NULL | Date the score was computed (Task J-1 run date) |
| created_at | timestamptz DEFAULT now() | — |

```sql
UNIQUE (institution_id, computed_date);
CREATE INDEX csm_health_history_lookup ON csm_health_history (institution_id, computed_date DESC);
```

**Retention policy:** Rows older than 90 days are deleted nightly by Task J-1 after inserting today's rows.
`DELETE FROM csm_health_history WHERE computed_date < CURRENT_DATE - INTERVAL '90 days';`

---

### `csm_account_assignment_history` (audit log)

> Required to track CSM/AM reassignments for audit and warm-handoff purposes.
> One row inserted every time `csm_account_assignment` is updated (via post-save signal).

| Column | Type | Notes |
|---|---|---|
| id | bigserial PK | — |
| institution_id | int FK → institution NOT NULL | — |
| previous_csm_id | int FK → user | Old CSM (null if none was assigned) |
| new_csm_id | int FK → user | New CSM (null if being unassigned) |
| previous_am_id | int FK → user | Old AM |
| new_am_id | int FK → user | New AM |
| previous_ism_id | int FK → user | Old ISM |
| new_ism_id | int FK → user | New ISM |
| changed_by_id | int FK → user NOT NULL | Who made the assignment change |
| change_reason | text | Optional reason note (required when reassigning > 10 accounts in bulk) |
| changed_at | timestamptz DEFAULT now() | — |

```sql
CREATE INDEX csm_assignment_history_inst ON csm_account_assignment_history (institution_id, changed_at DESC);
```

**Use cases:** Post-CSM-departure bulk reassignment audit; warm handoff context in J-03 ("Previously managed by Ananya K.").

---

### `csm_config` (key-value configuration store)

| Column | Type | Notes |
|---|---|---|
| key | varchar(100) PK | e.g., `health_threshold_healthy`, `renewal_alert_days`, `nps_quarterly_enabled`, `new_institution_grace_days`, `at_risk_default_playbook_template_id`, `churn_risk_default_playbook_template_id` |
| value | text NOT NULL | Stored as string; cast in application |
| description | text | Human-readable description |
| updated_by_id | int FK → user | — |
| updated_at | timestamptz DEFAULT now() | — |

**Initial seed values (applied in data migration on first deploy):**

| Key | Default | Description |
|---|---|---|
| `health_threshold_healthy` | `85` | Minimum score for HEALTHY tier |
| `health_threshold_engaged` | `65` | Minimum score for ENGAGED tier |
| `health_threshold_at_risk` | `45` | Minimum score for AT_RISK tier |
| `health_threshold_critical` | `25` | Minimum score for CRITICAL tier |
| `new_institution_grace_days` | `30` | Days since creation before health scoring begins |
| `renewal_alert_days` | `30` | Days before renewal date to trigger alerts |
| `nps_quarterly_enabled` | `true` | Enable/disable quarterly NPS dispatch (Task J-3) |
| `nps_min_kpi_responses` | `10` | Min responses needed to display portfolio-wide NPS KPI |
| `nps_min_chart_responses` | `5` | Min responses needed per month to render trend chart point |
| `at_risk_default_playbook_template_id` | `null` | Set post-seed once AT_RISK_RECOVERY template is created |
| `churn_risk_default_playbook_template_id` | `null` | Set post-seed once CHURN_SAVE template is created |
| `last_health_compute_at` | `null` | Updated by Task J-1 on each successful completion; read by Task J-4 |
| `nps_survey_expiry_days` | `14` | Days after sending before a survey link expires; used by `csm_nps_survey.link_expires_at = sent_at + interval '14 days'` |

**Who can edit csm_config keys:** Admin staff via Django admin interface (superuser or staff with `csm.change_csm_config` permission). CSM (#53) can read config values in the UI (visible in Settings panel) but cannot edit them directly — config changes require a platform admin to prevent misconfiguration at scale. Changes to config keys are logged via Django admin's built-in `LogEntry` mechanism (`updated_by_id` field).

---

## Health Score Computation (Celery Task J-1)

```
─── GRACE PERIOD GUARD ─────────────────────────────────────────────
If institution age < csm_config['new_institution_grace_days'] (default: 30):
  health_score = 65  (defaults to ENGAGED tier)
  is_new_institution = true
  All component scores = 0 (no data to measure yet)
  churn_probability_pct = null
  DO NOT run the formula below; skip to upsert.
─────────────────────────────────────────────────────────────────────

health_score = SUM(component_scores)

product_adoption_score (0–25):
  exams_created_30d:
    ≥ 10 exams → 10 pts
    5–9 exams  → 7 pts
    1–4 exams  → 4 pts
    0 exams    → 0 pts
  active_user_ratio (active_users_30d / total_enrolled):
    Guard: if total_enrolled = 0 → 0 pts (avoids div-by-zero)
    ≥ 0.60 → 10 pts
    0.40–0.59 → 7 pts
    0.20–0.39 → 4 pts
    < 0.20 → 0 pts
  features_activated_pct (stored in csm_institution_health.features_activated_pct):
    Denominator = count of modules applicable to institution_type
      SCHOOL: MCQ Bank, Exam Engine, Notes, Video Library, Results, Notifications = 6 modules
      COLLEGE: same as SCHOOL = 6 modules
      COACHING: MCQ Bank, Exam Engine, Notes, Video Library, Results, Notifications, Live Classes = 7 modules
      GROUP: all modules of child institutions = max applicable
    ≥ 80% → 5 pts
    50–79% → 3 pts
    < 50% → 0 pts

engagement_score (0–25):
  dau_mau_ratio (dau_7d_avg / active_users_30d):
    Guard: if active_users_30d = 0 → dau_mau_ratio = 0 → 0 pts (avoids div-by-zero)
    ≥ 0.30 → 15 pts
    0.15–0.29 → 10 pts
    0.05–0.14 → 5 pts
    < 0.05 → 0 pts
  session_frequency (sessions_30d / active_users_30d):
    Guard: if active_users_30d = 0 → 0 pts
    ≥ 8 sessions/user/month → 10 pts
    4–7 → 7 pts
    1–3 → 3 pts
    0 → 0 pts

support_burden_score (0–20):
  critical_high_tickets_30d (inverted):
    0 tickets → 10 pts
    1–2 → 7 pts
    3–5 → 3 pts
    > 5 → 0 pts
  csat_avg_30d (from support_ticket.csat_score; null = neutral 5 pts):
    4.5–5.0 → 10 pts
    3.5–4.4 → 7 pts
    2.5–3.4 → 4 pts
    < 2.5 → 0 pts

payment_health_score (0–20):
  days_past_due (inverted):
    0 days (current) → 15 pts
    1–7 days → 10 pts
    8–30 days → 5 pts
    > 30 days → 0 pts
  payment_history_12m (% of invoices paid on time):
    Guard: if no billing history → 5 pts (neutral, assume good faith)
    ≥ 90% → 5 pts
    70–89% → 3 pts
    < 70% → 0 pts

relationship_score (0–10):
  touchpoint_recency_days (inverted):
    ≤ 14 days → 5 pts
    15–30 days → 3 pts
    31–60 days → 1 pt
    > 60 days → 0 pts
  ebr_completed_90d (EBR or QBR touchpoint in last 90 days):
    Yes → 3 pts · No → 0 pts
  nps_contribution (most recent NPS response in last 12 months):
    PROMOTER → 2 pts · PASSIVE → 1 pt · DETRACTOR → 0 pts · No response → 1 pt (neutral)

─── POST-COMPUTE: PLAYBOOK AUTO-TRIGGER ────────────────────────────
After computing new health_score, check for tier transitions:

If new tier = AT_RISK (score 45–64) AND previous tier was ENGAGED or HEALTHY:
  → Task J-4 will fire at 08:00 IST (uses yesterday vs today comparison)
  → Auto-creates AT_RISK_RECOVERY playbook if none active
    Template ID from csm_config['at_risk_default_playbook_template_id']

If new tier = CHURNED_RISK (score 0–24) AND previous tier was not CHURNED_RISK:
  → Task J-4 will fire at 08:00 IST
  → Auto-creates CHURN_SAVE playbook if none active (overrides AT_RISK_RECOVERY suggestion)
    Template ID from csm_config['churn_risk_default_playbook_template_id']
  → Additionally sends P2 escalation suggestion notification to CSM + Escalation Manager
─────────────────────────────────────────────────────────────────────
```

---

## Celery Tasks

| Task ID | Name | Schedule | Description |
|---|---|---|---|
| J-1 | `csm_health_recompute` | Nightly 01:00 IST | (1) Applies grace period guard for institutions < 30 days old. (2) Recomputes health scores for all 2,050 institutions. (3) Upserts `csm_institution_health`. (4) Inserts today's row into `csm_health_history`; deletes history rows > 90 days old. (5) Auto-creates `csm_renewal` records for active subscriptions with no open renewal. (6) Updates `csm_escalation.commit_sla_breached` and `resolve_sla_breached` flags. (7) Sets `csm_config['last_health_compute_at']` on completion (used by Task J-4 to verify data freshness). Duration ~12–18 min. |
| J-2 | `csm_renewal_alert` | Daily 09:00 IST | Checks renewals due in ≤30 days with no touchpoint in last 14 days and stage not in (COMMITTED, RENEWED, CHURNED). Sends in-app notification to assigned AM + Renewal Exec. For ≤7 days remaining: escalates to WhatsApp via F-06 **for all active stages** (IDENTIFIED, OUTREACH_SENT, QUOTE_SENT, NEGOTIATING) — not limited to IDENTIFIED only; urgency applies regardless of pipeline progress. Also sends ISM tenure-end warning: if `ism_tenure_end_date` is 10 days away, sends in-app + email to ISM (#94) and AM (#54). Also sends daily digest to platform CSM (#53) listing count of institutions with no CSM or AM assigned. |
| J-3 | `csm_nps_dispatch` | 1st of each quarter at 10:00 IST | Sends `QUARTERLY_NPS` surveys to primary contacts of HEALTHY + ENGAGED institutions. Uses `@app.task(rate_limit='50/h')` Celery rate limiting; surveys spread via individual subtasks with ETA scheduling — no blocking sleep. Skips institutions surveyed in last 60 days. Queues 7-day reminder subtasks for non-respondents (sets `reminder_sent_at` on send). For COACHING-type institutions: dispatches via WhatsApp (F-06) instead of email, as coaching centres have higher WhatsApp engagement than email. |
| J-4 | `csm_at_risk_alert` | Daily 08:00 IST | Checks `csm_config['last_health_compute_at']` first — if Task J-1 did not complete today, runs on yesterday's data and adds note to notification: "based on last available data [timestamp]". Scans for tier crossings: (a) health_score dropped below 65 → sends CSM notification + auto-creates AT_RISK_RECOVERY playbook (template from `csm_config['at_risk_default_playbook_template_id']`). (b) health_score dropped below 25 (CHURNED_RISK crossing) → sends CSM + Escalation Manager notification + auto-creates CHURN_SAVE playbook (`csm_config['churn_risk_default_playbook_template_id']`). **Duplicate playbook logic:** Does not create duplicate playbooks if same-type instance is already ACTIVE. Exception: if account transitions directly to CHURNED_RISK (previously AT_RISK or ENGAGED), and an AT_RISK_RECOVERY playbook is currently ACTIVE, Task J-4 does NOT auto-abandon it — the assigned CSM receives a notification "Account now in CHURNED_RISK — review active AT_RISK_RECOVERY playbook and consider switching to CHURN_SAVE." CSM manually abandons the AT_RISK_RECOVERY instance if needed; Task J-4 creates CHURN_SAVE alongside it if none exists. **Template null guard:** if the config key is null or the referenced template ID does not exist or `is_active = false`, skip playbook auto-creation and send an additional in-app notification to the platform CSM (#53): "Auto-playbook skipped for [Institution] — default template not configured. Update `at_risk_default_playbook_template_id` in CS config." |
| J-5 | `csm_weekly_snapshot` | Monday 02:00 IST | Aggregates portfolio-wide metrics into `csm_weekly_snapshot`. Computes GRR = MIN(ARR_renewed_base, ARR_due) / ARR_due (capped at 100%; excludes expansion delta). Computes NRR = (ARR_renewed_base + expansion_arr) / ARR_due. **ARR_renewed_base** = `SUM(arr_value_paise WHERE stage='RENEWED' AND expansion_arr_paise IS NULL)` — base renewal ARR for institutions that renewed without expansion; **expansion_arr** = `SUM(expansion_arr_paise WHERE stage='EXPANSION')`; **ARR_due** = `SUM(arr_value_paise WHERE renewal_date in period)`. Uses rolling 13-week window for quarterly GRR/NRR. Also cleans up `csm_health_history` rows as a safety net (duplicate cleanup for rare retry-caused duplicates on the UNIQUE index). |
| J-6 | `csm_ism_tenure_handoff` | Daily 07:00 IST | Scans `csm_account_assignment` where `ism_tenure_end_date = today`. For each: (1) Sends in-app + email to ISM and AM: "ISM tenure complete for [Institution]. AM takes ownership from today." (2) Checks if any `csm_playbook_instance` with `assigned_to_id = ism_id` and `status = ACTIVE` exists — if so, reassigns instance to `account_manager_id` and sends AM a notification: "Playbook '[name]' for [Institution] transferred to you." **AM null guard:** if `account_manager_id` is null, do NOT reassign; instead notify the assigned CSM (#53): "[Institution] ISM tenure ended but no AM is assigned — active playbooks remain with ISM until an AM is assigned." Log a WARNING to application logs for monitoring. (3) Does NOT nullify `ism_id` — keeps as reference; AM is now primary. |

---

## Integration Points

### Division I — Customer Support
- `support_ticket` `critical_high_ticket_count_30d` per institution feeds into `support_burden_score` in health calculation (read-only join).
- When L3 Support Engineer (#50) closes a ticket with `account_at_risk=true` flag (added to `support_ticket` table in Div-I): Celery task fires a `csm_escalation` auto-creation with severity = P1_CRITICAL and pre-linked `support_ticket_ids`. Escalation Manager (#55) receives an in-app notification.
- Div-I Onboarding Specialist (#51) marks onboarding complete → `csm_account_assignment.ism_id` is set, ISM (#94) receives a handoff notification, and a `ONBOARDING_SUCCESS` playbook instance is auto-created for the institution.
- Mutual read: support ticket summary panel in J-03 Account Profile reads from `support_ticket` table. `/support/institutions/{id}/` in Div-I shows a CS health score strip read from `csm_institution_health`.

### Division M — Finance & Billing
- `billing_subscription.expires_at` is the source of truth for `csm_renewal.renewal_date`. Celery Task J-1 syncs renewal dates nightly.
- When renewal stage → `RENEWED` in `csm_renewal`, a signal fires to update `billing_subscription.auto_renew=true` and notify Billing Admin (#70) for invoice generation.
- Payment health data (`billing_payment.paid_at`, `billing_payment.due_date`) feeds into `payment_health_score`. Read-only join; Celery Task J-1 queries `billing_payment` directly.

### Division H — Data & Analytics
- CS Analyst (#93) reads `analytics_institution_engagement` table (pre-computed nightly by Div-H Task 1) for `active_users_30d`, `dau_7d_avg`, `sessions_30d`, `content_consumed_hrs_30d`. No live cross-tenant scans.
- Analytics Manager (#42) can read CSM health score distribution from `csm_institution_health` for anomaly detection (read-only cross-division read).

### Division F — Exam Day Operations
- Exam frequency data (`exam.created_by_institution_id`, `exam_submission.count`) aggregated nightly by Task J-1 to compute `exams_created_30d` and `product_adoption_score`.
- `EXAM_DAY_INCIDENT` tickets in Division I that are institution-level and unresolved after 24h trigger an escalation review suggestion in the Escalation Console (J-05).

### Division K — Sales
- When Sales converts a new institution (lead → active subscription), a `csm_account_assignment` record is created with `csm_id` and `account_manager_id` assigned by the B2B Sales Manager.
- Renewal stage changes (CHURNED) are visible to B2B Sales Manager (#57) in a read-only win-back dashboard within Division K (out of scope for Div-J).

---

## URL Namespace

All Division J routes under `/csm/` prefix. Django app name: `csm`.

**Shell pages (GET):**

| URL Pattern | View Function | Name |
|---|---|---|
| `GET /csm/` | `dashboard` | `csm:dashboard` |
| `GET /csm/accounts/` | `institution_portfolio` | `csm:portfolio` |
| `GET /csm/accounts/<int:pk>/` | `account_profile` | `csm:account` |
| `GET /csm/accounts/export/` | `portfolio_export` | `csm:portfolio_export` |
| `GET /csm/renewals/` | `renewal_pipeline` | `csm:renewals` |
| `GET /csm/escalations/` | `escalation_console` | `csm:escalations` |
| `GET /csm/escalations/<int:pk>/` | `escalation_detail` | `csm:escalation_detail` |
| `GET /csm/playbooks/` | `playbook_hub` | `csm:playbooks` |
| `GET /csm/feedback/` | `nps_feedback` | `csm:feedback` |
| `GET /csm/reports/` | `cs_reports` | `csm:reports` |
| `GET /csm/reports/export/` | `reports_export` | `csm:reports_export` |

**Write endpoints (POST / PATCH / DELETE):**

| URL Pattern | Method | View Function | Name |
|---|---|---|---|
| `/csm/accounts/<int:pk>/touchpoints/` | POST | `touchpoint_create` | `csm:touchpoint_create` |
| `/csm/accounts/<int:pk>/touchpoints/<int:tp_pk>/` | PATCH | `touchpoint_update` | `csm:touchpoint_update` |
| `/csm/accounts/<int:pk>/touchpoints/<int:tp_pk>/` | DELETE | `touchpoint_delete` | `csm:touchpoint_delete` |
| `/csm/accounts/<int:pk>/contacts/<int:user_pk>/set_primary/` | POST | `contact_set_primary` | `csm:contact_set_primary` |
| `/csm/accounts/<int:pk>/playbooks/start/` | POST | `playbook_instance_start` | `csm:playbook_start` |
| `/csm/accounts/<int:pk>/assign/` | POST | `account_assign` | `csm:account_assign` |
| `/csm/renewals/` | POST | `renewal_create` | `csm:renewal_create` |
| `/csm/renewals/<int:pk>/` | PATCH | `renewal_update` | `csm:renewal_update` |
| `/csm/renewals/<int:pk>/stage/` | POST | `renewal_stage_update` | `csm:renewal_stage` |
| `/csm/escalations/` | POST | `escalation_create` | `csm:escalation_create` |
| `/csm/escalations/<int:pk>/` | PATCH | `escalation_update` | `csm:escalation_update` |
| `/csm/escalations/<int:pk>/status/` | POST | `escalation_status_update` | `csm:escalation_status` |
| `/csm/escalations/<int:pk>/resolve/` | POST | `escalation_resolve` | `csm:escalation_resolve` |
| `/csm/escalations/<int:pk>/close/` | POST | `escalation_close` | `csm:escalation_close` |
| `/csm/escalations/<int:pk>/link_tickets/` | PATCH | `escalation_link_tickets` | `csm:escalation_link_tickets` |
| `/csm/escalations/<int:pk>/coordination/` | PATCH | `escalation_coordination` | `csm:escalation_coordination` |
| `/csm/playbooks/templates/` | POST | `playbook_template_create` | `csm:template_create` |
| `/csm/playbooks/templates/<int:pk>/` | PATCH | `playbook_template_update` | `csm:template_update` |
| `/csm/playbooks/instances/<int:pk>/tasks/<int:step>/complete/` | POST | `playbook_task_complete` | `csm:task_complete` |
| `/csm/playbooks/instances/<int:pk>/abandon/` | POST | `playbook_instance_abandon` | `csm:instance_abandon` |
| `/csm/feedback/surveys/send/` | POST | `survey_send` | `csm:survey_send` |
| `/csm/feedback/surveys/<int:pk>/followup/` | PATCH | `survey_followup` | `csm:survey_followup` |
| `/csm/feedback/surveys/<int:pk>/resend/` | POST | `survey_resend` | `csm:survey_resend` |
| `/csm/feedback/dispatch/skip/` | POST | `dispatch_skip` | `csm:dispatch_skip` |
| `/csm/accounts/bulk_assign/` | POST | `bulk_account_assign` | `csm:bulk_assign` |
| `/csm/accounts/bulk_playbook_start/` | POST | `bulk_playbook_start` | `csm:bulk_playbook_start` |
| `/csm/playbooks/instances/<int:pk>/` | PATCH | `playbook_instance_update` | `csm:instance_update` |
| `/csm/renewals/export/` | GET | `renewal_export` | `csm:renewal_export` |
| `/csm/escalations/<int:pk>/notify_csm/` | POST | `escalation_notify_csm` | `csm:escalation_notify_csm` |

---

## HTMX Conventions (Division J Standard Patterns)

### Auto-refresh polling
All "auto-refresh every X min/s" entries in Part-Load tables use HTMX's built-in polling trigger — no custom JavaScript interval needed:
```html
<div hx-get="/csm/?part=at_risk_feed"
     hx-trigger="load, every 180s"
     hx-target="#at_risk_feed"
     hx-swap="innerHTML">
```
The `every Xs` trigger is `hx-trigger` polling (HTMX native). If the poll request fails (network error, 5xx), HTMX stops polling automatically — no retry backoff needed at the JS layer; Celery tasks regenerate cache on next run.

### Tab / section navigation
Tab changes that update the URL use `hx-push-url="true"` on the HTMX request (not a form GET). The response is the **partial content only** (just the tab body), not a full page reload. Browser back/forward restores the ?section= param, which the shell page reads to re-render the correct active tab.

### hx-swap-oob (out-of-band swaps)
Write endpoints (POST/PATCH) that change header counters or badges return two fragments in one response:
1. Main swap: the updated record row or form result
2. OOB fragment: `<div id="target-id" hx-swap-oob="true">…updated content…</div>`

Both fragments are returned together in the same HTTP response body; HTMX processes them simultaneously — there is no sequential ordering or partial failure risk.

### Modal / drawer pattern
Drawers (Escalation Detail, Survey Detail, Account Assign, etc.) are opened via an HTMX `hx-get` on the trigger element with `hx-target="#drawer-container"` and `hx-swap="innerHTML"`. The `#drawer-container` is a persistent empty `<div>` in the base template that receives the drawer HTML. Closing via `[×]` dispatches a custom JS event that empties `#drawer-container` and removes the `is-open` CSS class from the overlay. Focus management: drawer open sets `focus()` to the first interactive element; close restores focus to the element that triggered the open.

### Memcached key naming convention
All Division J cache keys follow the pattern: `csm:{page}:{filter_hash}` where `{filter_hash}` is a deterministic hex digest of the sorted URL params dict. Example: `csm:portfolio:a3f4b2` for a specific filter combination on J-02. Keys are namespaced under `csm:` to allow bulk invalidation. TTL set per section as documented in each page's Data Sources table.

---

## Notification Events (Division J → F-06 Notification Manager)

| Event | Recipient | Channel | Trigger |
|---|---|---|---|
| AT_RISK threshold crossed (score drops below 65) | Assigned CSM | In-app + Email | Task J-4 |
| CHURNED_RISK threshold crossed (score drops below 25) | Assigned CSM + Escalation Manager | In-app + Email | Task J-4 |
| Renewal due ≤30d, no touchpoint in 14d | Assigned AM + Renewal Exec | In-app + WhatsApp | Task J-2 |
| Renewal due ≤7d, all active stages (IDENTIFIED, OUTREACH_SENT, QUOTE_SENT, NEGOTIATING) | Assigned AM + CSM | In-app + WhatsApp | Task J-2 |
| Renewal stage → COMMITTED | Assigned CSM + AM | In-app | Post-save signal on csm_renewal |
| P1 Escalation auto-created (from Div-I L3 flag) | Escalation Manager + CSM | In-app | Post-save signal on csm_escalation |
| Escalation commit SLA breached | Assigned Escalation Manager + CSM | In-app | Task J-1 (nightly SLA flag check) |
| Escalation resolve SLA breached | Assigned Escalation Manager + CSM | In-app + Email | Task J-1 (nightly SLA flag check) |
| Escalation RESOLVED (account_at_risk=true) | Assigned CSM + AM | In-app + Email | Post-save signal on status change |
| Playbook task overdue | Assigned playbook owner | In-app | Task J-1 (checked nightly) |
| Playbook instance COMPLETED | Assigned CSM (if ISM completed it) | In-app | Post-save signal when tasks_completed = tasks_total |
| NPS survey response received | Assigned CSM | In-app | Survey response webhook |
| DETRACTOR response received | Assigned CSM + CS Analyst (#93) | In-app + Email | Survey response webhook |
| NPS survey 7-day reminder sent | — (no notification; auto-sent to respondent) | Email to institution contact | Task J-3 subtask |
| ISM handoff received | ISM (#94) | In-app + Email | Post-save on csm_account_assignment.ism_id |
| ISM tenure ending in 10 days | ISM (#94) + AM (#54) | In-app + Email | Task J-2 (daily check on ism_tenure_end_date) |
| ISM tenure ended — playbook(s) transferred | AM (#54) | In-app | Task J-6 (daily tenure handoff task) |
| New account assigned (first time csm_id or am_id set) | Assigned CSM or AM | In-app + Email | Post-save signal on csm_account_assignment |
| Unassigned account detected (no CSM or AM) | Division J CSM (#53) — platform CSM | In-app (daily digest) | Task J-2 (includes count of unassigned accounts) |
| Escalation Manager flags escalation for CSM attention | Assigned CSM (#53) | In-app | POST to `/csm/escalations/{id}/notify_csm/` (rate-limited: max once per 60 min per escalation) |
