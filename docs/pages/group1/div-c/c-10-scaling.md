# C-10 — Auto-scaling & Capacity Planner

> **Route:** `/engineering/scaling/`
> **Division:** C — Engineering
> **Primary Role:** Platform Admin (Role 10) · DevOps/SRE (Role 14)
> **Read Access:** DBA (Role 15)
> **File:** `c-10-scaling.md`
> **Priority:** P1
> **Status:** ⬜ Amendment pending — G11 (Exam Day Mode tab)

---

## 1. Page Name & Route

**Page Name:** Auto-scaling & Capacity Planner
**Route:** `/engineering/scaling/`
**Part-load routes:**
- `/engineering/scaling/?part=kpi` — scaling health KPI
- `/engineering/scaling/?part=lambda-config` — Lambda concurrency config table
- `/engineering/scaling/?part=ecs-config` — ECS task scaling config
- `/engineering/scaling/?part=rds-config` — RDS replica scaling config
- `/engineering/scaling/?part=memcached-config` — ElastiCache scaling config
- `/engineering/scaling/?part=exam-calendar` — upcoming exam events + capacity forecast
- `/engineering/scaling/?part=simulation` — capacity simulation tool

---

## 2. Purpose (Business Objective)

The Auto-scaling & Capacity Planner is the forward-looking complement to the Infrastructure Monitor (C-08). Where C-08 tells you what is happening right now, C-10 tells you whether the infrastructure is configured to handle what is coming.

The platform's most predictable stress events are exam days — dozens of institutions often schedule exams on the same date, creating known peaks. This page integrates with the exam schedule calendar to forecast how many concurrent users to expect, then helps DevOps configure Lambda provisioned concurrency, ECS task counts, and RDS replicas to handle that load with headroom.

The capacity simulation tool is the most powerful feature: "If 80,000 students submit simultaneously, which service throttles first?" — this question must be answerable in under 60 seconds, before the exam starts, not during it.

**Business goals:**
- Pre-warm Lambda functions 30 minutes before every scheduled exam
- Configure and verify auto-scaling rules for all ECS services
- Plan RDS replica additions before capacity-constraining exam days
- Run capacity simulations against upcoming event forecasts
- Eliminate exam-day surprises through proactive capacity management

---

## 3. User Roles

| Role | Access Level | Permissions |
|---|---|---|
| Platform Admin (10) | Level 5 | Full view + all write: change concurrency · scale ECS · add/remove RDS replicas · add/remove Memcached nodes |
| DevOps / SRE (14) | Level 4 | Full view + all write actions |
| DBA (15) | Level 4 — Read | View RDS scaling config + exam calendar; cannot modify |

---

## 4. Section-Wise Detailed Breakdown

---

### Section 1 — Page Header & Capacity Status

**Purpose:** Instantly show whether the platform is configured for upcoming load.

**Capacity Status Banner:**

| State | Colour | Condition |
|---|---|---|
| ✅ Capacity adequate | Green | All upcoming events within configured headroom |
| ⚠ Capacity review recommended | Amber | 1+ events exceed 80% of current configuration |
| 🚨 Capacity action required | Red | 1+ events projected to exceed current configuration |

**Header elements:**
- H1 "Auto-scaling & Capacity Planner"
- Capacity status banner (large, colour-coded)
- "Run Capacity Simulation" primary CTA button
- Next scheduled exam: "Next exam: Tomorrow 09:00 — 12,400 expected students (8 institutions)"
- "View Exam Calendar" quick-link to calendar section

---

### Section 2 — KPI Strip

**KPI Cards:**

| Card | Metric | Alert |
|---|---|---|
| Lambda Reserved (total) | Total reserved concurrency allocated | > 90% of account limit = amber |
| Provisioned Concurrency (exam-critical) | Sum of warm instances for exam functions | < minimum for next event = amber |
| ECS Min Tasks (celery) | Minimum configured task count | < recommended for next event = amber |
| RDS Replicas | Current count | < 2 = amber (single replica = risk) |
| Memcached Nodes | Current cluster node count (3 nodes) | < 3 = amber |
| Days to Next Exam Peak | Days until next high-load event | — (informational) |

---

### Section 3 — Lambda Concurrency Configuration Table

**Purpose:** Configure reserved and provisioned concurrency for all Lambda functions.

**Table Columns:**

| Column | Description | Editable |
|---|---|---|
| Function | Lambda function name | — |
| Service | Service group | — |
| SLA Group | Exam-critical / Standard / Internal | — |
| Reserved Concurrency | Currently configured reserved limit | ✅ Admin/DevOps |
| Provisioned (Warm Instances) | Pre-warmed instances | ✅ Admin/DevOps |
| Current Usage (5m avg) | Live from C-08 (read-only here) | — |
| Peak Usage (24h) | Highest concurrency in last 24h | — |
| Throttle Events (24h) | Count of 429 throttle events | — |
| Pre-Warm Schedule | Auto pre-warm rule (time + count) | ✅ Admin/DevOps |
| Status | ✅ Adequate · ⚠ Review · 🚨 Action Needed | — |

**Status determination logic:**
- Adequate: Reserved ≥ (peak 24h × 1.5) AND Provisioned ≥ min pre-warm for next event
- Review: Reserved 1.0–1.5× peak OR Provisioned < recommended
- Action needed: Reserved ≤ peak (risk of throttling at current load pattern)

**Inline edit:** Click reserved/provisioned cell → number input → Enter saves immediately (no 2FA required for standard changes; 2FA required for reducing exam-critical function concurrency)

**Pre-warm schedule:**
- Format: "30 min before exam start · warm to {n} instances"
- Sources exam schedule from `platform_exam_schedule` (derived from Div B page 11 exam calendar)
- Celery beat executes pre-warm: calls Lambda PutProvisionedConcurrencyConfig at scheduled time
- Pre-warm status: "Next pre-warm: Tomorrow 08:30 — exam-submit → 500 instances"

**Batch actions (Admin/DevOps):**
- "Apply recommended settings" — computes recommendations from next 7 days of exam calendar; applies to all functions in one action (requires 2FA)
- "Reset to defaults" — clears all custom settings and returns to default concurrency (requires 2FA + confirmation)

---

### Section 4 — ECS Task Scaling Configuration

**Purpose:** Configure minimum, maximum, and step-scale rules for all ECS services.

**Services Table:**

| Service | Current Desired | Current Running | Min Tasks | Max Tasks | Scale-Up Trigger | Scale-Down Trigger | Pre-Exam Rule | Status |
|---|---|---|---|---|---|---|---|---|
| celery-worker | 8 | 8 | 4 | 20 | CPU > 70% for 3 min | CPU < 30% for 10 min | +4 tasks at exam start | ✅ |
| celery-beat | 1 | 1 | 1 | 1 | — (fixed) | — | — | ✅ |
| notification-worker | 4 | 4 | 2 | 12 | Queue depth > 1,000 | Queue depth < 100 | +2 tasks at exam end | ✅ |
| ai-pipeline-worker | 2 | 1 | 1 | 8 | CPU > 80% for 5 min | CPU < 20% for 15 min | — | ⚠ (1 pending task) |

**Edit per service:**
- Click row → inline edit form for min/max/trigger values
- Pre-exam rule: "Add {n} tasks {x} minutes before exam start"
- Pre-exam rule source: same exam calendar integration as Lambda pre-warm

**Scale-up trigger types:**
- CPU % threshold (average across tasks)
- Memory % threshold
- SQS queue depth (for workers)
- Custom CloudWatch metric

**Manual scale (override):**
- "Set desired count" button → number input → immediate ECS UpdateService call
- Confirmation: "Setting desired count to 12 will add 4 new tasks. At ₹{n}/hr per task. Confirm?"

**Edge Cases:**
- Celery beat: always fixed at 1 — "min tasks" and "max tasks" locked to 1; no scale rules (only one beat instance allowed)
- Scale below minimum: blocked; minimum enforced as hard floor
- Scale up during exam (emergency): DevOps can override beyond max with reason field

---

### Section 5 — RDS Replica Scaling

**Purpose:** Plan and execute read replica add/remove for anticipated read load increases.

**Current Replica Configuration:**

| Instance | Role | Instance Class | vCPU | RAM | IOPS | Region/AZ | Status |
|---|---|---|---|---|---|---|---|
| rds-primary | Primary (write) | db.r6g.2xlarge | 8 vCPU | 64 GB | 12,000 | ap-south-1a | ✅ |
| rds-replica-1 | Read | db.r6g.2xlarge | 8 vCPU | 64 GB | 12,000 | ap-south-1b | ✅ |
| rds-replica-2 | Read | db.r6g.2xlarge | 8 vCPU | 64 GB | 12,000 | ap-south-1c | ✅ |

**Connection budget display:**
- Max connections (primary): 5,000 (set by db.r6g.2xlarge RAM ÷ max_connections formula)
- PgBouncer server connections (primary): 300 (pooled)
- PgBouncer client connections (primary): 2,050 max (1 per tenant pool)
- Connection utilisation: {n}% (live from C-08)

**Add Replica:**
- "Add Read Replica" button → modal:
  - Instance class: select (default: same as existing replicas)
  - AZ: select (must differ from existing replicas for redundancy)
  - Estimated cost: ₹{n}/month shown
  - Estimated provision time: 15–30 min
  - Confirmation required (no 2FA for add; 2FA for remove)
- Celery job created; progress shown in notification bell
- New replica visible in table with "Provisioning" status

**Remove Replica:**
- "Remove replica" → modal with confirmation: "Removing this replica reduces read capacity by ~33% and eliminates redundancy. Confirm?" + 2FA
- Blocked if: only 1 replica remaining; or replica has active connections > 0

**Scaling recommendation:**
- System computes: at next peak exam ({n} students), projected read IOPS = {n}. Current capacity: {n} IOPS across {n} replicas. At {n} replicas, utilisation = {n}%.
- If projected > 80%: "Consider adding 1 more replica before {exam date}."

---

### Section 6 — ElastiCache Memcached Scaling

**Purpose:** Configure Memcached cluster node scaling.

**Current Configuration:**

| Dimension | Value |
|---|---|
| Cluster nodes | 3 |
| Node type | cache.r6g.large |
| Memory per node | 6.38 GB |
| Total cluster memory | 19.1 GB |
| Current memory used | 14.3 GB (75% of capacity) |
| Hit rate (cluster) | 96.4% |

**Scaling options:**
- "Add node" → adds a 4th node; ElastiCache rebalances cache distribution automatically
  - Estimated time: 5–10 min
  - Cost: +₹2,800/month per node
- "Scale up node type" → upgrade from cache.r6g.large to cache.r6g.xlarge (2× memory per node)
  - Requires cluster replacement (brief cache-cold period)

**Scaling recommendation (auto-computed):**
- If current memory > 75% of capacity: amber recommendation: "At current memory growth rate, capacity limit will be reached in ~8 months. Consider adding a node."
- If exam day memory estimate (simulate: +15% memory usage during peak): "Peak memory = {n}%. Headroom: {n}%."

**Memory usage projections:**
- Chart: current memory usage + projected growth (3-month linear extrapolation)
- Peak day simulation: adds expected exam-day cache load to projection

---

### Section 7 — Exam Calendar Integration

**Purpose:** The most important input for capacity planning — knowing exactly when exams will run and how large they are.

**Calendar View:**
- Month view (default) · Week view toggle
- Each exam event displayed as colour-coded chip:
  - Green: < 5,000 expected students (low load)
  - Amber: 5,000–20,000 students
  - Red: > 20,000 students
  - Black: > 50,000 students (peak exam day)

**Calendar Data Sources:**
- Exam schedule from `platform_exam_schedule` table (populated by Div B page 11 — Test Series Manager)
- Student enrolment count per exam from tenant schemas (approximated for planning purposes)

**Day Detail (click on exam day):**

| Exam | Institution | Scheduled Students | Domain | Start Time | Duration |
|---|---|---|---|---|---|
| JEE Mock Test 1 | Vibrant Academy | 8,200 | Engineering | 09:00 | 3h |
| NEET Prep Series 4 | Alpha Coaching | 4,800 | Medical | 10:00 | 2.5h |
| Class 10 Board Mock | 14 institutions | 42,000 | School | 09:00 | 3h |

**Total for day:** 55,000 expected concurrent students (at 09:00 peak overlap)

**Capacity assessment for selected day:**
- Lambda exam-submit: 55,000 students / average 30 submissions/student = 1,650,000 requests over 3h = ~9,200 req/min = ~153 concurrent Lambda instances needed
- Current configured: 1,000 reserved + 500 provisioned → "⚠ Provisioned concurrency may be insufficient. Recommend increasing to 800 warm instances."

**Auto-recommendation actions:**
- "Apply recommended scaling for this day" → pre-fills scaling config changes for Lambda + ECS
- "Schedule pre-warm for {date} {time - 30 min}" → creates Celery beat task

---

### Section 8 — Capacity Simulation Tool

**Purpose:** Answer "what if" questions before an exam, not during it.

**Purpose statement on page:** "Simulate any load scenario against current configuration to identify bottlenecks before they occur."

**Simulation Input Form:**

| Parameter | Input | Description |
|---|---|---|
| Concurrent Students | Number (e.g., 80,000) | Simultaneous active exam takers |
| Submission Rate | Number (e.g., 1 submission / 5s per student) | Frequency of answer-save calls |
| Exam Duration | Minutes | How long the load lasts |
| Login Burst | Number (e.g., 5,000 logins in first 2 min) | Auth endpoint spike at exam start |

**"Run Simulation" button:**
- Processing: 2–5s (calculation is server-side; no actual AWS API calls)

**Simulation Results:**

For each service, shows: **estimated load → current config → headroom → status**

| Service | Estimated Peak Load | Current Capacity | Headroom | Status |
|---|---|---|---|---|
| Lambda exam-submit | 800 concurrent | 1,000 reserved, 500 provisioned | 25% headroom | ✅ OK |
| Lambda auth-token | 500 concurrent | 400 reserved | -25% (THROTTLE RISK) | 🚨 Bottleneck |
| RDS connections | 3,200 connections | 5,000 max (PgBouncer) | 36% headroom | ✅ OK |
| Memcached memory | +15% usage during peak | 19.1 GB (75% used → 87% at peak) | 13% headroom | ⚠ Review |
| ECS celery-worker | 18 tasks needed | 8 desired, max 20 | auto-scales to 18 | ✅ OK |

**Bottleneck detail:**
- For each 🚨 service: "auth-service Lambda at 80K students would need 500 concurrent executions but only 400 reserved. 100 requests/min would be throttled (HTTP 429). Exam token refresh failures = students logged out mid-exam."

**Recommended actions panel (auto-generated from simulation results):**
- "Increase auth-service reserved concurrency: 400 → 600 (50% headroom)"
- "Increase auth-service provisioned: 50 → 200 (warm instances)"
- "Monitor Memcached cluster memory on exam day — at 87% expected usage. Consider adding a node."

**"Apply all recommendations" button:**
- Opens pre-filled confirmation showing all proposed changes
- 2FA required
- Applies all changes in one Celery job

**Simulation history:**
- Last 5 simulations saved: date · input parameters · bottlenecks found
- "Re-run last simulation" quick button

---

### Section 9 — Scheduled Scaling Rules

**Purpose:** Manage time-based scaling rules that fire automatically (not just on load — proactive pre-scaling).

**Scheduled Rules Table:**

| Rule Name | Service | Action | Schedule | Next Run | Status |
|---|---|---|---|---|---|
| Pre-warm exam-submit | Lambda | Set provisioned: 500 → 30 min before all exams | Celery beat: dynamic | Tomorrow 08:30 | ✅ Active |
| Exam-end scale-down | Lambda | Set provisioned: 500 → 50 (post-exam, 30 min after last exam ends) | Dynamic | Tomorrow 13:30 | ✅ Active |
| Night scale-down | ECS celery-worker | Desired: 8 → 4 (between 01:00–05:00 IST) | Daily 01:00 | Tonight 01:00 | ✅ Active |
| Night scale-up | ECS celery-worker | Desired: 4 → 8 | Daily 05:00 | Tomorrow 05:00 | ✅ Active |
| Weekend full scale-down | ECS ai-worker | Desired: 2 → 1 (Sat/Sun 00:00–06:00) | Weekend | Saturday 00:00 | ✅ Active |

**Add/Edit rule (Admin · DevOps):**
- Rule name
- Service: Lambda function / ECS service / RDS replica / Memcached node
- Action: specific config change (typed value, not percentage)
- Schedule: cron expression OR "N minutes before exam" (exam-calendar-linked)
- Enabled/disabled toggle
- "Next run" calculated and shown

**Exam-calendar linked rules:**
- Rules with "N min before exam" trigger fire for every exam automatically
- No need to create per-exam rules — one rule applies to all future exams

---

## 5. User Flow

### Flow A — Pre-Exam Capacity Planning

1. DevOps opens `/engineering/scaling/` — 3 days before major exam
2. Exam Calendar: tomorrow 09:00 — 55,000 expected students (red chip)
3. Capacity Status Banner: "⚠ Capacity review recommended"
4. Clicks "Run Capacity Simulation" → enters 55,000 students
5. Simulation result: Lambda auth-service bottleneck detected
6. Reviews recommendation: "Increase auth-service reserved: 400 → 600"
7. Clicks "Apply all recommendations"
8. 2FA confirmation → Celery applies all changes
9. Capacity banner turns green: "✅ Capacity adequate for all upcoming events"
10. Pre-warm scheduled rule fires at 08:30 on exam day

### Flow B — Post-Exam Scale-Down

1. Exam completes at 12:00
2. Scheduled rule fires at 12:30: Lambda provisioned concurrency drops from 500 → 50
3. Lambda cost decreases (provisioned concurrency billed per GB-second)
4. ECS celery worker scale-down at 01:00: 8 → 4 tasks (night mode)
5. DevOps verifies in C-08: concurrency at baseline level

### Flow C — Adding RDS Replica Before Peak Season

1. DBA opens scaling page → RDS section
2. Simulation: at 74K students peak, read IOPS = 9,800/replica (above 8,000 IOPS SLA for this instance class)
3. Recommendation: "Add 1 more read replica before next peak exam"
4. DBA reviews and escalates to DevOps
5. DevOps clicks "Add Read Replica" → selects instance class + AZ
6. Celery job: RDS CreateDBInstanceReadReplica API → 25 min provisioning
7. New replica visible in C-08 Infrastructure Monitor

---

## 6. Component Structure (Logical)

```
AutoscalingCapacityPlannerPage
├── PageHeader
│   ├── CapacityStatusBanner
│   ├── PageTitle
│   ├── RunSimulationButton (primary CTA)
│   └── NextExamSummary
├── KPIStrip × 6
├── LambdaConcurrencyConfigTable
│   ├── FunctionRow × 68 (inline edit)
│   └── BatchActionBar
├── ECSTaskScalingTable
│   └── ServiceRow × 5 (inline edit)
├── RDSReplicaScalingSection
│   ├── InstanceTable
│   ├── ConnectionBudgetDisplay
│   └── AddReplicaModal
├── MemcachedScalingSection
│   ├── ClusterConfigTable
│   └── ScaleActionModals
├── ExamCalendarSection
│   ├── CalendarView (month/week toggle)
│   ├── DayDetailPanel
│   └── CapacityAssessmentForDay
├── CapacitySimulationTool
│   ├── SimulationInputForm
│   ├── SimulationResults (per-service table)
│   ├── BottleneckDetails
│   ├── RecommendationsPanel
│   └── SimulationHistory
└── ScheduledScalingRulesTable
    └── AddEditRuleModal
```

---

## 7. Data Model (High-Level)

### platform_scaling_config

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| service_type | ENUM | lambda/ecs/rds/elasticache |
| resource_name | VARCHAR(100) | function name / service name / instance ID |
| config_key | VARCHAR(100) | e.g., `reserved_concurrency`, `min_tasks`, `max_tasks` |
| config_value | INTEGER | |
| updated_at | TIMESTAMPTZ | |
| updated_by | UUID FK → platform_staff | |

### platform_scheduled_scaling_rules

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| rule_name | VARCHAR(100) | |
| service_type | ENUM | lambda/ecs/rds/elasticache |
| resource_name | VARCHAR(100) | |
| config_key | VARCHAR(100) | |
| target_value | INTEGER | |
| schedule_type | ENUM | cron/pre_exam/post_exam |
| cron_expression | VARCHAR(100) | nullable (for cron type) |
| minutes_offset | INTEGER | nullable (for pre/post exam: e.g., -30 = 30 min before) |
| is_enabled | BOOLEAN | |
| last_run_at | TIMESTAMPTZ | nullable |
| next_run_at | TIMESTAMPTZ | computed by Celery beat |
| created_by | UUID FK → platform_staff | |

### platform_capacity_simulations

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| concurrent_students | INTEGER | |
| submission_rate | DECIMAL | submissions/student/second |
| exam_duration_minutes | INTEGER | |
| login_burst | INTEGER | |
| results | JSONB | per-service {load, capacity, headroom, status} |
| bottlenecks | JSONB | list of bottleneck services |
| recommendations | JSONB | list of recommended changes |
| run_by | UUID FK → platform_staff | |
| run_at | TIMESTAMPTZ | |

---

## 8. Validation Rules

| Rule | Detail |
|---|---|
| Reserved concurrency change | Exam-critical function: cannot reduce below current peak usage × 0.8 without 2FA + warning |
| Minimum ECS tasks | celery-beat: always 1, locked; celery-worker: min 2 (cannot go below); notification-worker: min 1 |
| RDS replica minimum | Cannot remove last remaining read replica (minimum: 1 replica at all times) |
| Memcached scaling | Add node: ElastiCache Memcached supports up to 40 nodes per cluster; scale-out adds distributed capacity with automatic key rebalancing |
| Simulation student count | Min 100 · Max 500,000 (beyond this, simulation results are unreliable) |
| Pre-warm schedule | Offset must be between -240 min and -5 min (relative to exam start); positive offset not allowed (cannot pre-warm after exam start) |
| Batch apply recommendations | 2FA required; must confirm each bottleneck fix individually if more than 5 changes |

---

## 9. Security Considerations

| Control | Detail |
|---|---|
| AWS API calls (all server-side) | Lambda PutProvisionedConcurrencyConfig · ECS UpdateService · RDS CreateDBInstanceReadReplica — all via IAM role; never browser-initiated |
| Reducing exam-critical concurrency | 2FA required to prevent accidental reduction during exam periods |
| Simulation (read-only) | Simulation runs purely on server-side calculations; no actual AWS API calls triggered; cannot affect live infrastructure |
| Scheduled rule approval | Rules that affect exam-critical services require Admin role; DevOps can manage standard service rules |
| Audit log | All scaling configuration changes logged to `platform_infra_events` (same as C-08 write actions) |

---

## 10. Edge Cases (System-Level)

| Scenario | Handling |
|---|---|
| Exam calendar empty (no exams scheduled) | Capacity simulation still available; calendar shows "No exams scheduled in next 30 days" |
| Lambda PutProvisionedConcurrency API fails | Error shown in Celery job result; admin alerted; scheduled pre-warm retry attempted 10 min before exam start |
| Simulation result: all services adequate | Green results table + "No bottlenecks detected at this load level. Platform can handle {n} concurrent students." |
| Manual scale override exceeds Max Tasks | Warning: "Setting desired to {n} exceeds configured maximum of {max}. Update max first." |
| Two DevOps engineers change same Lambda concurrency simultaneously | Optimistic lock on `platform_scaling_config` row; second save returns "Config was modified by another engineer 2s ago. Refresh and retry." |
| RDS replica promotion changes topology | After failover (from C-08), replica-1 becomes primary; scaling config updated automatically to reflect new topology |
| Pre-warm fires but Lambda is being deployed (C-05) | Pre-warm waits for deployment to complete (checks Lambda alias status); times out after 10 min with alert if deployment not finished |

---

## 11. Performance & Scaling Strategy

| Concern | Strategy |
|---|---|
| 68 functions config table | Static config from DB (< 100ms); live metrics column (concurrency) from C-08 Memcached cache — no new CloudWatch call |
| Simulation calculation | Pure arithmetic; server-side Python calculation < 200ms; no external API calls |
| Exam calendar load | `platform_exam_schedule` joined with student count estimates; month view = at most 31 days × 50 exams = 1,550 rows; < 50ms query |
| Pre-warm scheduling | Celery beat evaluates exam schedule every hour; pre-warm tasks queued as Celery countdown tasks (`apply_async(countdown=N)`) |
| Scheduled rule evaluation | Celery beat evaluates all scheduled scaling rules every 5 min; rules with `schedule_type = cron` use `celery-redbeat` for reliable execution |
| Capacity recommendations | Computed server-side in < 500ms; no LLM or ML involved — purely arithmetic comparison of estimated load vs configured capacity |

---

## Amendment — G11: Exam Day Mode Tab

**Gap addressed:** DevOps could not manually activate a coordinated "exam day mode" — simultaneously pre-warming all exam-critical Lambda provisioned concurrency, scaling ECS tasks to configured max, switching CloudFront to no-cache for API responses, and locking production CI/CD deployments — from a single action.

### New Tab on Auto-scaling & Capacity Planner — Exam Day Mode

**Access:** `/engineering/scaling/?tab=exam-day-mode` — top-level tab on the page.

**Tab Layout:**

**Current State Banner:**
- If inactive: Green "Exam Day Mode: OFF" with "Activate" button
- If active: Red pulsing "EXAM DAY MODE ACTIVE — activated {time ago} by {name}" with cost estimate running counter and "Deactivate" button

**Pre-flight Checklist (shown before activation):**

Opens `exam-day-activation-drawer` (600px) when "Activate" is clicked:

**Pre-flight checks (auto-run, 3–5s):**

| Check | Pass | Fail |
|---|---|---|
| No active CI/CD deployments in progress | ✅ | ❌ "Deployment running on portal repo — wait or cancel" |
| No pending Lambda updates | ✅ | ⚠ "Lambda function `exam-submit` has pending config update" |
| Exam calendar: exam(s) scheduled today | ✅ | ⚠ "No exams in calendar today — unusual activation" |
| Current concurrency headroom | ✅ 35% | ❌ < 10% headroom — scaling needed first |
| Last capacity simulation run | ✅ 2 days ago | ⚠ > 7 days — recommend re-running simulation |

**Cost impact estimate:**
- Current monthly Lambda spend (provisioned concurrency): ₹X
- Exam Day Mode additional cost (during activation): ₹Y/hour
- Estimated duration: {configured hours}
- Total estimated cost: ₹Z

**Activation confirmation:**
- 2FA required (Platform Admin or DevOps)
- Confirmation button: "Activate Exam Day Mode — ₹{Z} estimated cost"

**What Exam Day Mode does (on activation — all steps in one Celery job):**
1. Set all exam-endpoint Lambda provisioned concurrency to configured max values (from `platform_scaling_config` exam-day overrides)
2. Scale all ECS services to configured exam-day task counts
3. Switch CloudFront API distribution to no-cache headers (TTL = 0s for `/api/*` paths)
4. Lock CI/CD production deployments in C-09 (sets `platform:exam_day_mode_active` Memcached key → C-09 production deploy button reads this key)
5. Set Memcached `platform:exam_day_mode_active = true` key (picked up by C-08, C-09, C-04 poll intervals halving)
6. Send activation confirmation: Slack (webhook) + email to all DevOps team + Platform Admin

**During Exam Day Mode (active state):**
- All monitoring pages (C-04, C-08) switch to 15s poll interval
- CI/CD production deploy button in C-09 shows "🔒 Locked — Exam Day Mode active"
- Cost estimate counter ticks up in real-time
- "Deactivate" button always visible (no 2FA needed for deactivation — recovery speed matters)

**Deactivation:**
- Reverses all 6 activation steps
- Sends deactivation summary email: activation timestamp · deactivation timestamp · duration · peak metrics during mode (peak Lambda concurrency · peak RDS connections · peak Memcached memory)

**Activation History Table (last 10 activations):**

| Column | Description |
|---|---|
| Activated At | Timestamp |
| Activated By | Staff name |
| Duration | Hours:minutes |
| Deactivated By | Staff name |
| Peak Lambda Concurrency | Highest reached during mode |
| Peak RDS Connections | Highest reached |
| Cost | ₹ total cost of activation |
| Exam Summary | Exams run during this period (from calendar) |

**Data Model Addition — platform_exam_day_activations:**

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| activated_by | UUID FK → platform_staff | |
| activated_at | TIMESTAMPTZ | |
| deactivated_by | UUID FK → platform_staff | nullable |
| deactivated_at | TIMESTAMPTZ | nullable |
| cost_estimate_inr | DECIMAL | computed at activation |
| actual_cost_inr | DECIMAL | nullable — filled on deactivation |
| peak_lambda_concurrency | INTEGER | nullable |
| peak_rds_connections | INTEGER | nullable |
| celery_task_id | VARCHAR(255) | activation job ID |
