# Division I — Customer Support: Pages List & Architecture

> EduForge platform-level support covering 2,050 institutions and 2.4M–7.6M students.
> 6 core roles + 1 added role (90) = **7 roles total**.
> Support pipeline handles L1 → L2 → L3 escalation with hard SLA enforcement.

---

## Scale Context

| Segment | Count | Avg Monthly Tickets (Est.) |
|---|---|---|
| Schools | 1,000 | ~3,000 |
| Colleges | 800 | ~1,600 |
| Coaching Centres | 100 | ~800 |
| Institution Groups | 150 | ~300 |
| **Total institutions** | **2,050** | **~5,700/month normal** |
| **Exam-day peak** | — | **~18,000–25,000 in 48h window** |

Peak load driver: 74,000 simultaneous exam submissions → login failures, OTP timeouts, and session errors flood L1 simultaneously.

---

## Page Inventory

| Page | Route | Primary Role | Purpose |
|---|---|---|---|
| I-01 | `/support/` | Support Manager | Real-time support health dashboard |
| I-02 | `/support/tickets/` | L1/L2/L3/Support Manager | Paginated ticket worklist with SLA timers |
| I-03 | `/support/tickets/{id}/` | L1/L2/L3/Support Manager | Full ticket thread, actions, escalation |
| I-04 | `/support/institutions/{institution_id}/` | All support roles | Institution-scoped support history + contacts |
| I-05 | `/support/onboarding/` | Onboarding Specialist | Institution onboarding pipeline tracker |
| I-06 | `/support/knowledge-base/` | Training Coordinator | KB article authoring + training session scheduler |
| I-07 | `/support/reports/` | Support Manager | SLA compliance + team performance analytics |

---

## Division I Roles

| # | Role | Level | Owns | Cannot Do |
|---|---|---|---|---|
| 47 | Support Manager | 3 | Team management, SLA config, escalation rules, cross-division coordination, full ticket access | Infra config, billing, data writes outside support module |
| 48 | L1 Support Executive | 3 | Login, OTP, basic navigation, student and institution admin queries | Access L2/L3 queues; trigger code-level fixes; DB writes |
| 49 | L2 Support Engineer | 3 | Bug investigation, log analysis, DB read queries via tool access, technical ticket resolution | L3 fixes (code deploy, hotfix); billing changes |
| 50 | L3 Support Engineer | 4 | Code-level fixes, DB writes under Support Manager approval, hotfixes, rollbacks | Approve content; configure AI pipeline |
| 51 | Onboarding Specialist | 3 | New institution onboarding pipeline, portal setup guidance, admin training coordination | Access student ticket data; L2/L3 queues |
| 52 | Training Coordinator | 2 | Create training docs, schedule and conduct training sessions for institution admins | Access ticket queue; no ticket actions |
| 108 | Support Quality Lead | 3 | Random-sample ticket quality audits, CSAT trend monitoring, L1 agent coaching, KB gap identification, weekly quality report to Support Manager | Cannot reassign or escalate tickets; no direct ticket resolution |

---

## Role-to-Page Access Matrix

| Page | 47 Manager | 48 L1 | 49 L2 | 50 L3 | 51 Onboarding | 52 Training | 90 Quality |
|---|---|---|---|---|---|---|---|
| I-01 Dashboard | Full | Own-queue KPIs only | Own-queue KPIs only | Own-queue KPIs only | Onboarding panel only | No access | Quality panel + CSAT |
| I-02 Ticket Queue | All queues | L1 queue | L2 queue | L3 queue | Onboarding category | No access | Read all (no actions) |
| I-03 Ticket Detail | Full actions | L1 tickets | L2 tickets | L3 tickets | Onboarding tickets | No access | Read + quality annotation |
| I-04 Institution Profile | Full | Read | Read | Read | Full | Read | Read |
| I-05 Onboarding Tracker | Full | No access | No access | No access | Full | Read | No access |
| I-06 Knowledge Base | Full + Approve | Read | Read | Read | Read | Full (Create/Edit) | Read + flag gap |
| I-07 SLA Reports | Full | Own stats | Own stats | Own stats | Onboarding stats | No access | Quality metrics only |

---

## Data Model

### `support_ticket`

| Column | Type | Notes |
|---|---|---|
| id | bigserial PK | — |
| ticket_number | varchar(25) UNIQUE | Format: `SUP-YYYYMMDD-NNNNNN`; sequence resets daily |
| institution_id | int FK → institution | Nullable for platform-level tickets |
| subject | varchar(500) NOT NULL | — |
| category | varchar(30) NOT NULL | See enum below |
| priority | varchar(20) NOT NULL | `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`; default `MEDIUM` |
| status | varchar(30) NOT NULL | See state machine below; default `OPEN` |
| tier | varchar(5) NOT NULL | `L1`, `L2`, `L3`; default `L1` |
| source | varchar(30) NOT NULL | `PORTAL`, `EMAIL`, `PHONE`, `INTERNAL`, `DIVISION_H_ALERT`, `DIVISION_F_ESCALATION`; default `PORTAL` |
| assigned_to_id | int FK → user | Nullable; null = unassigned |
| created_by_id | int FK → user | Platform staff who created internal tickets; null for self-service |
| requester_name | varchar(200) | Name of institution admin or student who raised the ticket |
| requester_email | varchar(254) | — |
| requester_role | varchar(50) | `INSTITUTION_ADMIN`, `INSTITUTION_STAFF`, `STUDENT`, `PLATFORM_STAFF` |
| exam_day_incident | boolean DEFAULT false | True = flagged as exam-day critical; bypasses normal queue position |
| linked_exam_id | int FK → exam | Nullable; set for EXAM_ACCESS and EXAM_DAY_INCIDENT categories |
| sla_breach_at | timestamptz NOT NULL | Computed at creation: `created_at + resolution_hours` from `support_sla_config` |
| first_response_at | timestamptz | Set on first non-system reply from an agent |
| sla_pause_started_at | timestamptz | Set when status changes to `PENDING_CUSTOMER` |
| sla_pause_duration_seconds | int DEFAULT 0 | Cumulative seconds of PENDING_CUSTOMER time; subtracted from effective SLA |
| resolved_at | timestamptz | Set when status changes to `RESOLVED` |
| closed_at | timestamptz | Set when status changes to `CLOSED` |
| csat_score | smallint | 1–5; null until customer submits CSAT |
| csat_comment | text | Optional customer text on CSAT submission |
| csat_submitted_at | timestamptz | — |
| quality_audit_score | smallint | 1–5; set by Support Quality Lead (#108) during audit; null = not yet audited |
| quality_audit_note | text | Auditor note on ticket quality |
| quality_audited_at | timestamptz | — |
| first_response_sla_at | timestamptz NOT NULL | Computed at creation: `created_at + first_response_minutes` from `support_sla_config`; used for first-response SLA tracking in I-03 SLA tracker |
| sla_warning_sent | boolean DEFAULT false | Set to true when Task 2 sends the at-risk warning; prevents duplicate notifications within same breach window; reset to false when ticket is re-escalated (tier change recomputes SLA) |
| csat_sent_at | timestamptz | Set when CSAT survey is sent on RESOLVED; used by Task 3 to distinguish initial send from reminder |
| csat_link_expires_at | timestamptz | Set to `csat_sent_at + interval '30 days'`; CSAT submission portal rejects submissions after this timestamp; reset when CSAT is resent via [Resend CSAT] |
| tags | varchar[] DEFAULT '{}' | Free-form tags; editable by assigned agent and Support Manager; not editable by Quality Lead (#108) |
| created_at | timestamptz DEFAULT now() | — |
| updated_at | timestamptz DEFAULT now() | — |

**Category enum (12 values):**
`LOGIN_ISSUE`, `OTP_FAILURE`, `EXAM_ACCESS`, `RESULT_QUERY`, `BILLING_QUERY`, `TECHNICAL_BUG`, `FEATURE_REQUEST`, `ONBOARDING_HELP`, `DATA_CORRECTION`, `EXAM_DAY_INCIDENT`, `BGV_QUERY`, `OTHER`

> `BGV_QUERY` added: any BGV-related institution query. Auto-routes to BGV Manager (#39) via post-save signal (see Integration Points — Division G). BGV Manager is an external role that does NOT access Division I pages; they receive an F-06 notification with a direct link to the ticket in I-03 (read-only view). Division I retains ownership for SLA tracking; BGV Manager resolves by adding a reply in I-03.
>
> `ONBOARDING_HELP` creation: any of L1, L2, L3, Support Manager, or Onboarding Specialist (#51) can create this category. It is not restricted to Onboarding Specialist alone.

**Routing rules at creation:**
- `EXAM_DAY_INCIDENT` → auto-tier = L2, auto-priority = CRITICAL, `exam_day_incident=true`; never appears in L1 queue unless Support Manager explicitly overrides tier (with audit note)
- `DATA_CORRECTION` → auto-tier = L2
- `TECHNICAL_BUG` → auto-tier = L1; Celery Task 2 flags for escalation if first-response SLA is breached and status still = OPEN (agent must escalate manually — no auto-tier change)
- All others → tier = L1
- **Catch-all**: any category not listed above → tier = L1, priority = MEDIUM
- **Internal ticket validation**: tickets with `source=INTERNAL` (created via [+ New Ticket] with "internal ticket" checked) MUST have at least one of: `institution_id` OR `requester_name` OR `requester_email`. A ticket with all three null is rejected at the API level with 400: "Internal tickets must have at least one requester identifier."

**Ticket number sequence**: `ticket_number` uses a PostgreSQL daily sequence (`support_ticket_seq_{YYYYMMDD}`). Sequence created on first ticket of each day; auto-increments without gaps. Max throughput: PostgreSQL sequences are lockless — handles exam-day peak (25,000 tickets/48h = ~520/hour) without collision.

---

### `support_ticket_message`

| Column | Type | Notes |
|---|---|---|
| id | bigserial PK | — |
| ticket_id | bigint FK → support_ticket | — |
| author_id | int FK → user | Nullable for system messages |
| message_type | varchar(20) NOT NULL | `REPLY`, `INTERNAL_NOTE`, `STATUS_CHANGE`, `ESCALATION`, `QUALITY_ANNOTATION`, `SYSTEM` |
| body | text NOT NULL | Markdown for REPLY; plain text for SYSTEM |
| attachments | jsonb DEFAULT '[]' | `[{filename, r2_key, size_bytes, content_type, uploaded_at}]` |
| is_visible_to_requester | boolean DEFAULT true | False for `INTERNAL_NOTE`, `QUALITY_ANNOTATION`, `ESCALATION` type |
| created_at | timestamptz DEFAULT now() | — |

---

### `support_ticket_escalation`

| Column | Type | Notes |
|---|---|---|
| id | bigserial PK | — |
| ticket_id | bigint FK → support_ticket | — |
| from_tier | varchar(5) | L1 or L2; null if escalated from Support Manager directly |
| to_tier | varchar(5) NOT NULL | L2 or L3 |
| escalated_by_id | int FK → user | — |
| reason | text | Required free-text reason; displayed in ticket thread |
| reason_type | varchar(50) NOT NULL | Structured reason code: `NEEDS_DB_INVESTIGATION`, `TECHNICAL_BUG_CONFIRMED`, `REQUIRES_CODE_CHANGE`, `CUSTOMER_REQUESTING_SUPERVISOR`, `SLA_BREACH_IMMINENT`, `TIER_SKIP_EMERGENCY`, `BILLING_ESCALATION`, `OTHER` |
| escalated_at | timestamptz DEFAULT now() | — |

---

### `support_sla_config`

| Column | Type | Notes |
|---|---|---|
| id | serial PK | — |
| tier | varchar(5) NOT NULL | L1, L2, L3 |
| priority | varchar(20) NOT NULL | CRITICAL, HIGH, MEDIUM, LOW |
| first_response_minutes | int NOT NULL | Minutes until first response SLA |
| resolution_minutes | int NOT NULL | Minutes until resolution SLA |
| is_exam_day_override | boolean DEFAULT false | If true, this row is the exam-day override config; matched when `support_ticket.exam_day_incident=true` AND priority=CRITICAL; takes precedence over standard row for same tier+priority |
| is_active | boolean DEFAULT true | — |
| UNIQUE(tier, priority, is_exam_day_override) | — | — |

**Default SLA values:**

| Tier | Priority | First Response | Resolution |
|---|---|---|---|
| L1 | CRITICAL | 30 min | 120 min |
| L1 | HIGH | 60 min | 240 min |
| L1 | MEDIUM | 120 min | 480 min |
| L1 | LOW | 240 min | 1,440 min |
| L2 | CRITICAL | 60 min | 240 min |
| L2 | HIGH | 120 min | 480 min |
| L2 | MEDIUM | 240 min | 960 min |
| L2 | LOW | 480 min | 2,880 min |
| L3 | CRITICAL | 120 min | 480 min |
| L3 | HIGH | 240 min | 960 min |
| L3 | MEDIUM | 480 min | 1,440 min |
| L3 | LOW | 1,440 min | 4,320 min |

> Exam-day override: A dedicated row with `is_exam_day_override=true` exists for L1/CRITICAL: first_response=15min, resolution=60min. Matched at ticket creation when `exam_day_incident=true`. All exam-day incidents auto-tier to L2 (so L2/CRITICAL exam-day row: first_response=30min, resolution=120min).

---

### `onboarding_instance`

| Column | Type | Notes |
|---|---|---|
| id | serial PK | — |
| institution_id | int FK → institution | Not UNIQUE at column level — uniqueness enforced by composite constraint `UNIQUE(institution_id, re_onboarding_sequence)` below; allows multiple records per institution when re-onboarding |
| assigned_specialist_id | int FK → user | Onboarding Specialist (#51) |
| stage | varchar(30) NOT NULL DEFAULT 'INITIATED' | See stage machine below |
| started_at | timestamptz DEFAULT now() | — |
| target_go_live_at | date | Set at initiation; agreed go-live date |
| actual_go_live_at | date | Set when stage transitions to LIVE |
| completed_at | timestamptz | Set when stage = COMPLETED |
| stalled_since | timestamptz | Set by Celery Task 4 when `last_activity_at < now() - interval '7 days'` |
| last_activity_at | timestamptz DEFAULT now() | Updated whenever: a checklist item is completed, a training session is created or completed, or the stage changes; used by Celery Task 4 for stall detection (NOT `updated_at`, which only updates on direct instance edits) |
| is_re_onboarding | boolean DEFAULT false | True if this is a second+ onboarding for the same institution after a prior COMPLETED instance |
| re_onboarding_sequence | smallint DEFAULT 1 | 1=first onboarding, 2=first re-onboarding, etc. `UNIQUE(institution_id, re_onboarding_sequence)` replaces `UNIQUE(institution_id)`; system auto-sets to `MAX(sequence for institution) + 1` on create; prevents accidental duplicate creation |
| notes | text | Specialist notes |
| updated_at | timestamptz DEFAULT now() | Updated on direct instance edits; do NOT use for stall detection — use `last_activity_at` |

**Stage machine:** `INITIATED → SETUP_CALL_SCHEDULED → PORTAL_CONFIGURED → ADMIN_TRAINED → FIRST_EXAM_CREATED → LIVE → COMPLETED`
Parallel: any stage → `STALLED` (Celery auto-sets after 7 days inactivity); Support Manager can re-activate.

---

### `onboarding_checklist_template`

| Column | Type | Notes |
|---|---|---|
| id | serial PK | — |
| stage | varchar(30) NOT NULL | Which stage this item belongs to |
| title | varchar(200) NOT NULL | — |
| description | text | Tooltip/help text for specialist |
| is_mandatory | boolean DEFAULT true | Mandatory items block stage progression |
| sort_order | int NOT NULL | Display order within stage |

---

### `onboarding_checklist_progress`

| Column | Type | Notes |
|---|---|---|
| id | serial PK | — |
| instance_id | int FK → onboarding_instance | — |
| template_item_id | int FK → onboarding_checklist_template | — |
| is_completed | boolean DEFAULT false | — |
| completed_by_id | int FK → user | — |
| completed_at | timestamptz | — |
| notes | text | Optional per-item note |
| UNIQUE(instance_id, template_item_id) | — | — |

---

### `onboarding_training_session`

| Column | Type | Notes |
|---|---|---|
| id | serial PK | — |
| instance_id | int FK → onboarding_instance | — |
| title | varchar(300) NOT NULL | — |
| session_type | varchar(30) NOT NULL | `PORTAL_WALKTHROUGH`, `EXAM_CREATION`, `STUDENT_MGMT`, `RESULTS_WORKFLOW`, `REFRESHER` |
| scheduled_at | timestamptz NOT NULL | — |
| duration_minutes | int DEFAULT 60 | — |
| meeting_link | varchar(500) | Google Meet / Zoom link |
| conducted_by_id | int FK → user | Onboarding Specialist or Training Coordinator |
| status | varchar(20) DEFAULT 'SCHEDULED' | `SCHEDULED`, `COMPLETED`, `CANCELLED`, `NO_SHOW` |
| attendee_names | text[] DEFAULT '{}' | Names of institution staff who attended |
| recording_url | varchar(500) | Nullable |
| notes | text | Post-session notes |
| created_at | timestamptz DEFAULT now() | — |

> **Standalone sessions** (`instance_id=null`): FK constraint is NULLABLE (no FK violation). Application validates: `title` and `scheduled_at` are always required regardless of `instance_id`. Standalone sessions are created via I-06 Training tab by Training Coordinator (#52) or Support Manager; they represent platform-wide training events not tied to any onboarding instance (e.g., periodic refresher webinars for all institution admins). Onboarding Specialist (#51) can also create standalone sessions from I-06.

---

### `kb_article`

| Column | Type | Notes |
|---|---|---|
| id | serial PK | — |
| title | varchar(500) NOT NULL | — |
| slug | varchar(200) UNIQUE NOT NULL | URL-safe; auto-generated from title |
| category | varchar(50) NOT NULL | `LOGIN`, `EXAM_FLOW`, `BILLING`, `ONBOARDING`, `TECHNICAL`, `ADMIN_PORTAL`, `RESULTS`, `GENERAL` |
| body | text NOT NULL | Markdown content |
| status | varchar(20) DEFAULT 'DRAFT' | `DRAFT`, `PENDING_REVIEW`, `PUBLISHED`, `ARCHIVED` |
| author_id | int FK → user | Training Coordinator or Support Manager |
| reviewed_by_id | int FK → user | Support Manager who approved |
| published_at | timestamptz | — |
| archived_at | timestamptz | — |
| view_count | int DEFAULT 0 | Incremented on each view |
| helpful_votes | int DEFAULT 0 | — |
| not_helpful_votes | int DEFAULT 0 | — |
| linked_ticket_categories | varchar[] DEFAULT '{}' | Which `support_ticket.category` values this article helps resolve; multi-select in editor; updated in-place (array replaced) |
| review_feedback | text | Rejection feedback from Support Manager; shown as yellow banner in editor when status=DRAFT after rejection; cleared on next PENDING_REVIEW submission |
| created_at | timestamptz DEFAULT now() | — |
| updated_at | timestamptz DEFAULT now() | — |

**KB article state machine:** `DRAFT → PENDING_REVIEW → PUBLISHED or DRAFT` (if rejected) → `ARCHIVED`
Training Coordinator (#52) authors; Support Manager (#47) approves. Support Quality Lead (#108) can flag articles for review.

---

### `kb_article_gap_flag`

| Column | Type | Notes |
|---|---|---|
| id | serial PK | — |
| flagged_by_id | int FK → user | Support Quality Lead (#108) or any agent |
| ticket_category | varchar(30) | Category where the KB gap was identified |
| gap_type | varchar(30) NOT NULL DEFAULT 'MISSING_ARTICLE' | `MISSING_ARTICLE` (no article for this category), `INACCURATE` (existing article has wrong info), `OUTDATED` (article correct but stale), `INCOMPLETE` (article exists but missing steps) |
| description | text NOT NULL | Description of the missing or incorrect content |
| status | varchar(20) DEFAULT 'OPEN' | `OPEN`, `ASSIGNED`, `RESOLVED` |
| assigned_to_id | int FK → user | Training Coordinator assigned to fill gap |
| resolved_at | timestamptz | Set when status → RESOLVED |
| created_at | timestamptz DEFAULT now() | — |

---

### `support_quality_audit`

| Column | Type | Notes |
|---|---|---|
| id | serial PK | — |
| audited_by_id | int FK → user | Support Quality Lead (#108) |
| ticket_id | bigint FK → support_ticket | The ticket being audited |
| quality_score | smallint NOT NULL CHECK (1–5) | 1=Poor, 5=Excellent |
| criteria_scores | jsonb | `{tone, accuracy, speed, resolution_quality}` each 1–5 |
| notes | text | Detailed feedback |
| shared_with_agent | boolean DEFAULT false | Whether audit result was shared with ticket agent |
| audited_at | timestamptz DEFAULT now() | — |

---

### `institution_contact`

> Support team's operational contact directory for each institution. Separate from institution admin user accounts — may include IT contacts, finance contacts, principal's office, etc.

| Column | Type | Notes |
|---|---|---|
| id | serial PK | — |
| institution_id | int FK → institution | — |
| name | varchar(200) NOT NULL | — |
| role_title | varchar(100) | e.g., "IT Coordinator", "Finance Admin", "Principal" |
| email | varchar(254) | — |
| phone | varchar(20) | — |
| preferred_contact | varchar(20) DEFAULT 'EMAIL' | `EMAIL`, `PHONE`, `WHATSAPP` |
| last_contacted_at | date | Manually updated by support staff |
| notes | text | Internal notes about this contact |
| created_by_id | int FK → user | Support staff who added this contact |
| created_at | timestamptz DEFAULT now() | — |
| updated_at | timestamptz DEFAULT now() | — |

---

### `institution_support_note`

> Internal notes about an institution maintained by the support team. Not visible to institution.

| Column | Type | Notes |
|---|---|---|
| id | serial PK | — |
| institution_id | int FK → institution | — |
| author_id | int FK → user | Support staff who created the note |
| note_type | varchar(20) NOT NULL DEFAULT 'INFO' | `PINNED` (always shown first), `WARNING` (orange ⚠ — flags special handling), `INFO` (grey — general note) |
| body | text NOT NULL | No length limit |
| is_pinned | boolean DEFAULT false | True for PINNED type; multiple pinned notes allowed; shown reverse-chronologically |
| created_at | timestamptz DEFAULT now() | — |
| updated_at | timestamptz DEFAULT now() | — |

---

### `support_weekly_report`

> Pre-computed weekly performance snapshot generated by Celery Task 5 every Monday 09:00 IST. Read by I-07 for the "Weekly Snapshot" section.

| Column | Type | Notes |
|---|---|---|
| id | serial PK | — |
| week_start | date NOT NULL UNIQUE | Monday of the report week (ISO: first day of week) |
| total_tickets | int | COUNT for the week |
| sla_compliance_l1 | numeric(5,2) | % tickets meeting resolution SLA in L1 |
| sla_compliance_l2 | numeric(5,2) | % tickets meeting resolution SLA in L2 |
| sla_compliance_l3 | numeric(5,2) | % tickets meeting resolution SLA in L3 |
| avg_csat_score | numeric(3,2) | Average CSAT score for the week |
| csat_response_rate | numeric(5,2) | % of resolved tickets that received CSAT |
| avg_resolution_minutes_l1 | int | Average resolution time for L1 tickets |
| avg_resolution_minutes_l2 | int | — |
| avg_resolution_minutes_l3 | int | — |
| tickets_by_category | jsonb | `{LOGIN_ISSUE: 142, OTP_FAILURE: 87, ...}` |
| escalation_rate_l1 | numeric(5,2) | % of L1 tickets escalated to L2 |
| escalation_rate_l2 | numeric(5,2) | % of L2 tickets escalated to L3 |
| agent_stats | jsonb | `[{user_id, name, tier, tickets_handled, avg_resolution_min, csat_avg, sla_compliance_pct}]` |
| generated_at | timestamptz DEFAULT now() | — |

---

### `kb_article_vote`

> Tracks per-user votes on KB articles to enforce one-vote-per-user idempotency.

| Column | Type | Notes |
|---|---|---|
| id | bigserial PK | — |
| article_id | int FK → kb_article | — |
| voted_by_id | int FK → user | The support staff member who voted |
| vote | varchar(10) NOT NULL | `HELPFUL`, `NOT_HELPFUL` |
| created_at | timestamptz DEFAULT now() | — |
| UNIQUE(article_id, voted_by_id) | — | One vote per user per article; re-voting updates the row (UPDATE, not INSERT) |

On INSERT or UPDATE: increments/decrements `kb_article.helpful_votes` or `not_helpful_votes` accordingly.

---

## Ticket Status State Machine

```
OPEN
  │
  ├─ Agent picks up → IN_PROGRESS
  │     │
  │     ├─ Needs customer input → PENDING_CUSTOMER
  │     │     │
  │     │     └─ Customer replies → IN_PROGRESS (SLA timer resumes)
  │     │
  │     ├─ Escalation action → ESCALATED
  │     │     │  (tier updated; new SLA computed; assigned_to_id cleared)
  │     │     └─ New-tier agent picks up → IN_PROGRESS
  │     │        (ESCALATED is transient: it exists from escalation action
  │     │         until the new-tier agent first replies or changes status)
  │     │
  │     └─ Issue fixed → RESOLVED
  │           │
  │           └─ [Auto-close after 7 days no activity] → CLOSED
  │
  └─ (Unassigned; Support Manager assigns OR agent clicks [Assign to me]) → IN_PROGRESS
```

**ESCALATED** is a **distinct status** (not just a badge): it means "escalated, waiting for new-tier agent to pick up." It is NOT the same as IN_PROGRESS at the new tier. Filtering by `status=ESCALATED` in I-02 shows tickets pending pickup at L2/L3. Exiting ESCALATED: any action by the new-tier agent (reply, status change, internal note) transitions to IN_PROGRESS. Support Manager can also re-assign from ESCALATED to IN_PROGRESS manually.

**Re-open CLOSED**: Support Manager only → status = IN_PROGRESS; tier preserved from last tier before closure (not reset to L1/MEDIUM); no new escalation record created; new SLA computed from preserved tier + priority + `support_sla_config`; CSAT not re-sent on re-open (prior CSAT score preserved; `csat_link_expires_at` not reset). An INTERNAL_NOTE with the re-open reason is required and is inserted into the thread.

CSAT survey sent to requester **immediately when status changes to `RESOLVED`** (not on CLOSED). Sets `csat_sent_at` timestamp. Celery Task 3 sends a **reminder** (not a new survey) if `csat_submitted_at IS NULL` AND `csat_link_expires_at > now()` and ticket auto-closes after 7 days.

---

## SLA Pause/Resume Accumulation

When status changes to `PENDING_CUSTOMER`:
- `sla_pause_started_at` = `now()`; `sla_warning_sent` = false (warning resets on new customer activity)

When status changes from `PENDING_CUSTOMER` to any other status (customer replies or agent takes action):
- `sla_pause_duration_seconds += EXTRACT(EPOCH FROM (now() - sla_pause_started_at))`
- `sla_pause_started_at` = null

**Effective SLA breach time** (used in all Celery tasks and I-03 display):
```
effective_breach_at = sla_breach_at + sla_pause_duration_seconds * interval '1 second'
```
For tickets currently in `PENDING_CUSTOMER`, the running pause is also added:
```
effective_breach_at = sla_breach_at
  + sla_pause_duration_seconds * interval '1 second'
  + EXTRACT(EPOCH FROM (now() - sla_pause_started_at)) * interval '1 second'
```

This means a ticket that waited 4h for a customer reply effectively gets 4h added to its deadline. Task 1 uses `effective_breach_at < now()` (not raw `sla_breach_at`) for breach detection, and does NOT exclude `PENDING_CUSTOMER` tickets — it just adjusts for pause time.

**Rapid toggling**: If status is toggled PENDING_CUSTOMER → IN_PROGRESS → PENDING_CUSTOMER within seconds, the `+=` accumulates even sub-second durations (minimum granularity: 1 second via `EXTRACT(EPOCH ...)`). This is correct behaviour — each transition is independently summed. No minimum pause threshold is enforced; extremely short pauses (< 5s) are architectural noise but do not break SLA accuracy at any meaningful scale.

**KB Article Duplicate Detection Threshold**: I-06 uses PostgreSQL `pg_trgm` trigram similarity for duplicate article detection at >0.8 (80%) threshold. This is intentionally high to avoid false positives on related-but-distinct articles. Common false-positive pairs ("Login Issues" / "Login Problems") will trigger the warning — authors should review and proceed if the content is genuinely different. No exemption list is maintained; the warning is advisory only and never blocks saving.

---

## Celery Tasks

| # | Task Name | Schedule | Queue | Action |
|---|---|---|---|---|
| 1 | `check_sla_breaches` | Every 5 min | `support` | Scans ALL open tickets (including PENDING_CUSTOMER) where `effective_breach_at < now()` (see SLA Pause/Resume section for formula); sends breach notification via F-06 to assigned agent + Support Manager; PENDING_CUSTOMER tickets use extended effective deadline; does not breach tickets in RESOLVED or CLOSED |
| 2 | `send_sla_warnings` | Every 15 min | `support` | Checks two thresholds: (a) **Resolution SLA**: tickets where `effective_breach_at BETWEEN now() AND now() + interval '60 min'` and status NOT IN (RESOLVED, CLOSED) and `sla_warning_sent=false`; (b) **First response SLA**: tickets where `first_response_at IS NULL` and `first_response_sla_at BETWEEN now() AND now() + interval '30 min'` and status=OPEN; sends F-06 warning push to assigned agent; sets `sla_warning_sent=true` to prevent duplicate sends |
| 3 | `auto_close_resolved_tickets` | Daily at 00:00 IST | `support` | Closes tickets in `RESOLVED` status where `resolved_at < now() - interval '7 days'` and no new `support_ticket_message` rows since `resolved_at`; if `csat_submitted_at IS NULL` and `csat_sent_at IS NOT NULL`, sends one CSAT **reminder** push via F-06 (not a new survey); sets `closed_at = now()` |
| 4 | `flag_stalled_onboarding` | Daily at 08:00 IST | `support` | Marks onboarding instances as `STALLED` if `last_activity_at < now() - interval '7 days'` and stage NOT IN (`LIVE`, `COMPLETED`); notifies assigned Onboarding Specialist and Support Manager via F-06; does not re-notify if `stalled_since` is already set (idempotent) |
| 5 | `generate_support_weekly_report` | Every Monday 09:00 IST | `support` | Computes all metrics for the prior week (Mon–Sun); upserts into `support_weekly_report` (idempotent on `week_start`); notifies Support Manager via F-06 push with summary stats |
| 6 | `alert_unassigned_queue` | Every 30 min during business hours (08:00–20:00 IST) | `support` | Counts open tickets WHERE `assigned_to_id IS NULL` AND `created_at < now() - interval '30 min'`; if count > 0, sends F-06 push notification to Support Manager listing unassigned ticket count + longest-waiting ticket number; does NOT auto-assign — assignment is always a human decision to ensure correct tier/skill match |
| 7 | `aggregate_feature_requests` | Every 1 hour | `support` | Scans `support_ticket` WHERE `category='FEATURE_REQUEST'`; groups tickets by subject using PostgreSQL trigram similarity (`pg_trgm`); if any cluster has ≥3 tickets with similarity >0.8 and no notification sent in the last 24h for that cluster, sends F-06 push to Product Manager (#5): "{N} feature requests about '{subject_cluster_representative}'. Review in Division B." Rate-limit enforced: 1 notification per cluster per 24h (tracked via Redis counter keyed by cluster hash). |

---

## Caching Strategy (Memcached)

| Page | Part | TTL | Bypass |
|---|---|---|---|
| I-01 Dashboard | KPI strip | No cache | Live SLA timers require fresh data; auto-refreshes every 60s |
| I-01 Dashboard | Volume chart | 2 min | Support Manager: `?nocache=true` |
| I-01 Dashboard | SLA compliance gauges | 2 min | `?nocache=true` |
| I-01 Dashboard | Team workload table | 2 min | `?nocache=true` |
| I-01 Dashboard | Quality panel | 5 min | `?nocache=true` |
| I-01 Dashboard | Escalation feed | 1 min | `?nocache=true` |
| I-01 Dashboard | Onboarding pipeline strip | 5 min | `?nocache=true` |
| I-01 Dashboard | Exam day banner | No cache | Auto-refreshes every 30s; must be live |
| I-02 Ticket Queue | Table rows | No cache | Live SLA timers require fresh data |
| I-03 Ticket Detail | Thread messages | No cache | Must reflect real-time replies |
| I-04 Institution Profile | Subscription badge | 30 min | `?part=subscription&nocache=true` (Support Manager only) |
| I-04 Institution Profile | Ticket history table | 5 min | — |
| I-05 Onboarding Tracker | Stage table | 5 min | — |
| I-06 KB Manager | Article list | 10 min | — |
| I-06 KB Manager | Published articles | 60 min | — |
| I-07 SLA Reports | Charts | 15 min | `?nocache=true` |
| I-07 SLA Reports | Weekly report snapshot | 60 min | `?nocache=true` |
| I-07 SLA Reports | Exam day markers (Division F join) | 60 min | — |

---

## Integration Points

| External System | Direction | What Flows |
|---|---|---|
| Division F — Exam Day Ops | Inbound + Outbound | Incident Manager (#38) creates `EXAM_DAY_INCIDENT` tickets via `POST /api/support/tickets/` with `source=DIVISION_F_ESCALATION`; auto-tier=L2, auto-priority=CRITICAL; F-06 routes all ticket notifications (breach, escalation, resolution). Outbound: I-07 volume chart shows exam-day markers by joining `support_ticket.linked_exam_id` → Division F `exam` table (read-only via service account); Division F `exam.start_date` used as marker date |
| Division H — Analytics | Inbound | H-01 anomaly alert webhook calls `POST /api/support/tickets/` with `source=DIVISION_H_ALERT`, category=`TECHNICAL_BUG`, priority=`HIGH`, subject pre-populated from anomaly description; auto-assigned to Support Manager; appears in I-02 with grey "H-01 Alert" badge; Support Manager triages and re-assigns |
| Division G — BGV | Inbound | BGV_QUERY tickets: on creation (any agent), a post-save signal creates a SYSTEM message: "BGV query detected. Assigning to BGV Manager for resolution." and sets `assigned_to_id` to BGV Manager (#39) user ID; ticket remains in Division I system for SLA tracking. **BGV Manager (#39) has limited I-03 access scoped to `BGV_QUERY` tickets only** (similar to Onboarding Specialist's scoped access to ONBOARDING_HELP tickets) — they do NOT access I-01, I-02, I-05, I-06, or I-07. They receive an F-06 direct link, open the ticket in I-03, resolve by adding a REPLY, and change status to RESOLVED. Division I agent then closes. |
| Division K — Sales | Inbound | When Sales marks a deal as WON in the CRM, a webhook calls `POST /api/support/onboarding/create/` with institution_id and expected_go_live_date; creates `onboarding_instance` with `stage=INITIATED`; notifies all Onboarding Specialists via F-06 for assignment |
| Division B — Product | Outbound | **Celery Task 7** (`aggregate_feature_requests`): every hour, check if any `category=FEATURE_REQUEST` ticket cluster has 3+ tickets with identical/similar subject (PostgreSQL trigram similarity >0.8); if cluster threshold met, creates a notification record for Product Manager (#5) via F-06 push (notification only — no cross-module DB write); rate-limited to one notification per cluster per 24h to avoid spam |
| Division M — Billing | Inbound (read-only) | `institution_subscription` table read for I-04 institution header subscription status; fetched via `subscription` service read-only API; cached for 30 min; graceful fallback: if Division M unavailable, subscription badge shows "Status unavailable" grey without blocking page load |
| AWS SES | Bidirectional | Inbound: SES inbound email handler parses emails to support@eduforge.in → creates ticket with `source=EMAIL`; replies to ticket notification emails are appended as REPLY messages (SES SNS webhook). Outbound: ticket notification emails, CSAT survey emails, training session invites |
| WhatsApp (Meta API) | Outbound | CSAT surveys sent as WhatsApp message to `requester_phone` if `preferred_contact=WHATSAPP` (from `institution_contact` table); template pre-approved by Meta; managed by Notification Manager (#37); retry: 1 attempt only (no loops) |

---

## Cross-Page Workflows

### Workflow 1 — Exam Day Surge Handling
1. Live exam begins (Division F confirms exam started; `exam.status=LIVE` in Division F DB)
2. I-01 shows red exam-day banner; I-02 auto-applies `?exam_day=true&priority=CRITICAL` filter for all agents
3. `EXAM_DAY_INCIDENT` tickets auto-route to L2; SLA = 30-min first response, 120-min resolution (exam-day override row)
4. **Surge overflow handling**: If open `EXAM_DAY_INCIDENT` ticket count exceeds 200 (configurable env var `EXAM_DAY_SURGE_THRESHOLD`), I-02 shows surge mode: "⚠ Surge active: {N} critical tickets. [Activate Triage Mode]"
   - Triage mode (Support Manager activates): collapses ticket detail — reply box shows only 3 canned responses ([Exam is ongoing — issue logged], [Technical team notified], [Rejoin link: {link}]); agents can reply with one click; full detail still accessible via [Full View] link
   - Support Manager can auto-assign unassigned surge tickets in bulk via [Distribute {N} tickets across L2 team] button (round-robin assignment)
5. EXAM_DAY_INCIDENT tickets: L2 can attempt resolution; if needs L3 code change, escalate immediately; L2 cannot close without resolution note
6. After exam ends (Division F updates `exam.status`), banner clears on next 60s HTMX refresh; surge mode deactivates; normal queue resumes
7. Post-exam: Support Manager runs I-07 report filtered to exam day to review surge handling performance

### Workflow 2 — L1 → L2 → L3 Escalation
1. L1 agent in I-03 clicks [Escalate to L2]; required: select reason from dropdown (8 reasons)
2. `support_ticket_escalation` record created; ticket tier updated to L2; old SLA invalidated; new SLA computed from L2 config
3. L2 queue in I-02 shows escalated ticket with red "Escalated from L1" badge
4. L2 can further escalate to L3 (same process); Support Manager can skip tiers in emergency
5. L3 resolves; resolution note visible to all prior tier agents for learning

### Workflow 3 — New Institution Onboarding
1. Sales closes deal → creates `onboarding_instance` (Stage: INITIATED)
2. Onboarding Specialist sees new entry in I-05; picks up and schedules first call
3. I-05 checklist tracks each mandatory item per stage before stage can progress
4. If stalled >7 days: Celery task flags STALLED; Support Manager gets notification
5. On stage = LIVE: `actual_go_live_at` stamped; Training Coordinator schedules follow-up session via I-06

### Workflow 4 — CSAT-Driven Quality Loop
1. Ticket resolved → auto CSAT sent to requester
2. Score < 3 → Support Quality Lead (#108) sees ticket in quality audit queue in I-07
3. Quality Lead audits ticket in I-03 (via quality annotation message type); logs `support_quality_audit` record
4. If agent performance issue: quality audit report shared with Support Manager via I-07
5. Recurring patterns → KB gap flagged via I-06 → Training Coordinator creates/updates article

### Workflow 5 — KB Article Lifecycle
1. Training Coordinator (#52) creates DRAFT article in I-06
2. Submits for review → status = PENDING_REVIEW
3. Support Manager reviews; approves (→ PUBLISHED) or rejects with feedback (→ DRAFT with note)
4. Published articles auto-linked to matching ticket categories
5. L1 agents in I-03 see suggested KB articles when viewing tickets of matching category
6. Support Quality Lead can flag any article for review if identified as inaccurate/outdated

---

## Attachment Security Policy

Applied to all file uploads across Division I (ticket replies, quality annotations):

| Rule | Specification |
|---|---|
| Max file size | 10 MB per file |
| Max files per upload | 3 files per message/reply |
| Max total per ticket | No hard limit per ticket lifetime; application does not restrict cumulative attachment count |
| Allowed MIME types | `image/png`, `image/jpeg`, `image/gif`, `image/webp`, `application/pdf`, `text/plain`, `text/csv`, `application/vnd.ms-excel`, `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`, `application/msword`, `application/vnd.openxmlformats-officedocument.wordprocessingml.document`, `application/zip` (support logs only) |
| Blocked types | All executables: `.exe`, `.bat`, `.sh`, `.cmd`, `.scr`, `.msi`, `.dll`, `.jar`; scripts: `.js`, `.php`, `.py`, `.rb`; enforced by MIME type check AND file extension check (both must pass) |
| MIME spoofing protection | Server validates MIME type using `python-magic` (libmagic) against actual file bytes, not just `Content-Type` header. A `.exe` renamed to `.pdf` will be rejected. |
| Malware scanning | Files scanned via ClamAV (self-hosted, sidecar container) before writing to R2. Infected files: rejected with error "File failed security scan. Please contact your IT team." R2 write happens only after scan passes. |
| R2 key format | `tickets/{ticket_id}/messages/{message_id}/{timestamp}_{original_filename}` |
| Signed URL TTL | 24 hours; [Download] regenerates a fresh signed URL on click |
| Upload error messages | "File too large (max 10 MB)" · "File type not allowed" · "Too many files (max 3)" · "Security scan failed" · "Upload failed — please try again" |

---

## Database Performance & Indexes

Critical indexes required for support queue performance at 25,000+ ticket scale:

```sql
-- I-02 stats bar queries (run every 60s per agent)
CREATE INDEX idx_ticket_sla_status ON support_ticket(sla_breach_at, status)
  WHERE status NOT IN ('RESOLVED', 'CLOSED');

-- I-02 queue by tier + assigned agent
CREATE INDEX idx_ticket_assigned_status_tier ON support_ticket(assigned_to_id, status, tier);

-- Celery Task 1: breach scan every 5 min
CREATE INDEX idx_ticket_breach_open ON support_ticket(sla_breach_at)
  WHERE status NOT IN ('RESOLVED', 'CLOSED');

-- I-02 full-text search on subject
ALTER TABLE support_ticket ADD COLUMN subject_tsv tsvector
  GENERATED ALWAYS AS (to_tsvector('english', subject)) STORED;
CREATE INDEX idx_ticket_subject_fts ON support_ticket USING GIN(subject_tsv);
-- ticket_number prefix search: btree index
CREATE INDEX idx_ticket_number_prefix ON support_ticket(ticket_number varchar_pattern_ops);

-- I-04 institution ticket history
CREATE INDEX idx_ticket_institution_created ON support_ticket(institution_id, created_at DESC);

-- Celery Task 6: unassigned alert
CREATE INDEX idx_ticket_unassigned_created ON support_ticket(created_at)
  WHERE assigned_to_id IS NULL AND status NOT IN ('RESOLVED', 'CLOSED');

-- I-07 agent performance aggregation
CREATE INDEX idx_ticket_assigned_resolved ON support_ticket(assigned_to_id, resolved_at)
  WHERE resolved_at IS NOT NULL;

-- kb_article_vote dedup enforcement
-- UNIQUE(article_id, voted_by_id) already serves as index via PK constraint
```

All queries against `support_ticket` in I-02 stats bar, I-01 KPI strip, and Celery tasks 1, 2, 6 use these indexes. Without them, a 25,000-row scan takes ~200ms per query; with them, <5ms.

---

## Rate Limiting

| Endpoint | Limit | Scope | Response if exceeded |
|---|---|---|---|
| `POST /api/support/tickets/` (PORTAL source) | 10 tickets/hour per institution | Per `institution_id` | HTTP 429 "Too many tickets submitted. Please wait 60 minutes or contact support via email." |
| `POST /api/support/tickets/` (EMAIL inbound) | 20 emails/hour per sender email | Per `requester_email` | Email silently discarded; no bounce (prevents confirmation spam) |
| `POST /api/support/tickets/` (INTERNAL source) | 100 tickets/hour per platform user | Per `created_by_id` | HTTP 429 with retry-after header |
| `POST /api/support/tickets/{id}/reply/` | 30 replies/hour per user | Per `author_id` | HTTP 429 "Reply limit reached. Wait before sending another message." |
| Attachment upload | 20 files/hour per user | Per `author_id` | HTTP 429 "File upload limit reached." |

Rate limiting implemented via Django Rate Limit middleware with Redis counters (1-hour sliding window). Note: Division I is the only module where Redis is used — strictly for rate limit counters only, not for caching (which uses Memcached per project memory rules).

---

## Timezone Handling

All timestamps stored as `timestamptz` (UTC) in PostgreSQL. Display rules:
- **Default display**: IST (UTC+5:30) — the platform's primary operating timezone
- **Per-user preference**: support staff can set preferred timezone in their profile settings (stored in `user.timezone` field); if set, all Division I timestamps display in their timezone
- **SLA countdown timers**: always displayed in agent's local timezone; the deadline is identical regardless of timezone (it's a UTC timestamp)
- **Date filters** (e.g., `?created_after=2024-11-05`): interpreted as midnight IST by default; agents in other timezones should be aware of this when filtering by date
- **CSV exports**: timestamps exported in UTC with ISO 8601 format (`2024-11-05T08:30:00Z`) to avoid ambiguity

---

## SLA Config Management

`support_sla_config` table is managed via **Django Admin** (`/admin/support/slaconfigentry/`) — not via any Division I page. Only Platform Admin (#10) can modify SLA thresholds via Django Admin. Support Manager (#47) can VIEW current SLA config on the I-07 reports page (a static read-only table showing current thresholds) but cannot edit.

**Process for changing SLA thresholds**: Support Manager submits a request to Platform Admin → Platform Admin updates via Django Admin → change takes effect for all new tickets immediately (existing tickets retain their original `sla_breach_at` and `first_response_sla_at` computed at creation).

---

## Audit Log Access

All system-level audit events (PII access, bulk actions, CSAT resends, ticket closures, escalations, re-opens) are recorded as `SYSTEM` type messages in `support_ticket_message`. This provides a per-ticket audit trail accessible in I-03 thread.

**Platform-level audit log**: the Data Privacy Officer (#76) and Platform Admin (#10) have access to a platform-wide audit log (outside Division I scope — managed by Division C Engineering). Division I does NOT have its own dedicated audit log page. Support Manager can view per-ticket audit trails via I-03 thread history only.

---

## DPDPA 2023 Considerations

- Ticket records contain requester PII (name, email, phone) — classified as **personal data** under DPDPA 2023
- Access strictly role-scoped: agents see only tickets in their tier queue; Support Manager sees all; Quality Lead reads all but cannot export without DPO approval
- All PII data access (view, export, download) logged as SYSTEM message in `support_ticket_message` for 7-year audit trail
- **Bulk PII export rules**:
  - Institution admin tickets: exportable by Support Manager with audit log entry (institutional data, DPDPA purpose = legitimate interest)
  - Student tickets (requester_role=STUDENT): `requester_email` masked as `s***@domain.com` in all exports regardless of role; requires DPO (#76) approval for unmasked export
  - Quality Lead (#108): can export ticket metadata (ticket_number, category, score, resolution_time) but NOT requester PII fields
- `institution_contact` table contains operational contact PII — access limited to support roles; not exportable in bulk
- **Retention** enforced by annual archival Celery job (runs 1 Jan each year): archives `support_ticket` records older than 7 years to S3 cold storage; cascades to messages and escalations

---

## Data Retention Policy

| Table | Retention | Method |
|---|---|---|
| `support_ticket` | 7 years | Soft-delete then archive to cold storage |
| `support_ticket_message` | 7 years | Cascades with parent ticket |
| `support_ticket_escalation` | 7 years | Cascades with parent ticket |
| `support_sla_config` | Permanent | Config table; never deleted |
| `onboarding_instance` | 5 years post-completion | Archived after `completed_at + 5 years` |
| `onboarding_checklist_progress` | 5 years | Cascades with instance |
| `onboarding_training_session` | 5 years | Cascades with instance |
| `kb_article` | Permanent (published); 1 year (DRAFT/ARCHIVED) | — |
| `kb_article_gap_flag` | 1 year post-resolution | Soft-delete; `resolved_at + 1 year` |
| `support_quality_audit` | 2 years | Hard delete after 2 years |
| `support_weekly_report` | 3 years | Hard delete after 3 years |
| `institution_contact` | 5 years post institution offboarding | Cascades on institution deletion |
| `institution_support_note` | 5 years post institution offboarding | Cascades on institution deletion |
| `kb_article_vote` | Until article deleted/archived | Cascades on `kb_article` deletion; retained for article lifetime |
| `support_ticket` (attachments in R2) | 7 years | On ticket archival, R2 objects are moved to S3 cold storage under the same key prefix; signed URL generation stops; objects are not hard-deleted until institution offboarding |
