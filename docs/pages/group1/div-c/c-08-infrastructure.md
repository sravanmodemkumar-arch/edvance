# C-08 — Infrastructure Monitor

> **Route:** `/engineering/infrastructure/`
> **Division:** C — Engineering
> **Primary Role:** Platform Admin (Role 10) · DevOps/SRE (Role 14)
> **Read Access:** Backend Engineer (Role 11) · DBA (Role 15) · Security Engineer (Role 16)
> **File:** `c-08-infrastructure.md`
> **Priority:** P0 — Must be live before first institution goes live
> **Status:** ⬜ Amendment pending — G4 (Celery Queues tab) · G23 (ECS Task Definition Editor drawer)

---

## 1. Page Name & Route

**Page Name:** Infrastructure Monitor
**Route:** `/engineering/infrastructure/`
**Part-load routes:**
- `/engineering/infrastructure/?part=kpi` — global health KPI
- `/engineering/infrastructure/?part=lambda` — Lambda concurrency panel
- `/engineering/infrastructure/?part=ecs` — ECS cluster panel
- `/engineering/infrastructure/?part=rds` — RDS + replicas panel
- `/engineering/infrastructure/?part=elasticache` — Memcached panel
- `/engineering/infrastructure/?part=alb` — ALB panel
- `/engineering/infrastructure/?part=cloudfront` — CloudFront summary
- `/engineering/infrastructure/?part=s3` — S3 buckets panel
- `/engineering/infrastructure/?part=actions-drawer&service={svc}` — write-action drawer

---

## 2. Purpose (Business Objective)

The Infrastructure Monitor is the single pane of glass for all AWS infrastructure during every hour the platform is live. On a normal day, it is a passive monitoring dashboard. During an exam peak at 74K concurrent submissions, it becomes the most critical page in the organisation — DevOps watches Lambda concurrency against reserved limits, RDS connection count against PgBouncer pool capacity, and ElastiCache memory to ensure nothing saturates.

Critically, this page also has **write controls**: DevOps can change Lambda concurrency, restart ECS tasks, promote a read replica to primary, and drain an ALB target group directly from this UI — without navigating to the AWS console. Speed of action during an incident is the core design goal.

**Business goals:**
- Real-time visibility into all infrastructure components with 30s data freshness
- Write controls for the most time-critical recovery actions
- Exam-day mode with elevated alert sensitivity
- CERT-In compliance: infrastructure events logged for potential breach investigations
- Cost visibility across all services

---

## 3. User Roles

| Role | Access Level | Permissions |
|---|---|---|
| Platform Admin (10) | Level 5 | Full view + all write actions |
| DevOps / SRE (14) | Level 4 | Full view + all write actions |
| Backend Engineer (11) | Level 4 — Read | View Lambda + ECS panels only; no write |
| DBA (15) | Level 4 — Read | View RDS panel only (link to C-11 for write actions) |
| Security Engineer (16) | Level 4 — Read | View all panels; no write |

---

## 4. Section-Wise Detailed Breakdown

---

### Section 1 — Page Header & Global Health

**Purpose:** Platform-wide infrastructure health in one colour-coded verdict.

**Global Health Matrix:**

| Service | Status | Colour |
|---|---|---|
| Lambda | ✅ Healthy | Green |
| ECS | ✅ Healthy | Green |
| RDS Primary | ✅ Healthy | Green |
| RDS Replica 1 | ✅ Healthy | Green |
| RDS Replica 2 | ⚠ Lag 4s | Amber |
| ElastiCache Memcached | ✅ Healthy | Green |
| ALB | ✅ Healthy | Green |
| CloudFront | ✅ Healthy | Green |

**Verdict banner:**
- All green → "✅ All infrastructure healthy"
- Any amber → "⚠ Degraded: {service name}"
- Any red → "🚨 Critical: {service name}" (pulsing)

**Exam Day Mode Banner:**
- Triggered when `platform:active_exam_count > 0`
- Amber banner: "🎓 EXAM IN PROGRESS — {n} active exams · Enhanced monitoring active · Poll interval: 15s"
- Poll interval drops from 30s to 15s across all panels

**Header actions:**
- "Open Incident" button → pre-fills C-18
- "View Cost Dashboard" link → C-16 equivalent for infra costs
- Auto-refresh toggle (default: ON)

---

### Section 2 — KPI Strip — Cross-Service Health

**KPI Cards:**

| Card | Metric | Source | Alert |
|---|---|---|---|
| Lambda Throttle Events | Count in last 5 min | CloudWatch | > 10 amber · > 100 red |
| RDS Connections | Active connections (primary) | RDS Metrics | > 80% of max_connections = amber |
| Memcached Memory Usage | % of total cluster memory | ElastiCache | > 85% amber · > 95% red |
| ALB 5xx Rate | 5xx/total (last 5 min) | ALB metrics | > 0.5% amber |
| ECS Task Failures | Failed tasks in last 15 min | ECS metrics | > 0 = amber |
| Estimated Infra Cost (Today) | Sum all services | AWS Cost Explorer | > 80% daily budget = amber |

---

### Section 3 — Lambda Concurrency Panel

**Purpose:** Real-time view of Lambda concurrency usage against reserved and burst limits — critical for exam day.

**Panel Layout:**
- Summary bar: "Total concurrent executions: 1,842 / 3,000 reserved (61%)"
- Progress bar: green → amber at 80% → red at 95%

**Function-Level Table:**

| Function | Concurrency (now) | Reserved | % Used | Throttle Events (5m) | Provisioned | Status |
|---|---|---|---|---|---|---|
| exam-service-submit | 842 | 1,000 | 84% | 0 | 200 (warm) | ⚠ High |
| exam-service-questions | 420 | 600 | 70% | 0 | 100 (warm) | ✅ OK |
| auth-service-token | 210 | 400 | 53% | 0 | 50 (warm) | ✅ OK |
| result-service-fetch | 185 | 300 | 62% | 0 | 50 (warm) | ✅ OK |
| notification-service | 85 | 200 | 43% | 2 | 0 | ✅ OK |

**Colour Rules:**
- < 70%: green
- 70–84%: amber
- ≥ 85%: red
- Throttle events > 0: amber dot on row

**Write Actions (Admin · DevOps — opens action drawer):**
- "Change Reserved Concurrency" — slider (0 to account limit) + confirmation
- "Change Provisioned Concurrency" — number input + confirmation (updates Lambda configuration)
- "Force cold start flush" — sets reserved concurrency to 0 → 1 → back to value (flushes all warm instances) — requires 2FA

**Data Flow:**
- Concurrency: CloudWatch `ConcurrentExecutions` and `ReservedConcurrentExecutions` per function
- Provisioned concurrency: Lambda GetProvisionedConcurrencyConfig API
- 30s HTMX poll (15s in exam day mode)

**Account-level limit display:**
- "Account burst limit: 3,000 concurrent executions (ap-south-1)"
- "Total reserved: 2,850 / 3,000 (95%)" — amber if > 90% reserved (leaves no room for burst)

---

### Section 4 — ECS Cluster Panel

**Purpose:** Monitor ECS services running background workers (Celery, notification workers, AI pipeline workers).

**ECS Services Table:**

| Service | Desired Tasks | Running | Pending | CPU % (avg) | Memory % (avg) | Status |
|---|---|---|---|---|---|---|
| celery-worker | 8 | 8 | 0 | 42% | 68% | ✅ OK |
| celery-beat | 1 | 1 | 0 | 5% | 12% | ✅ OK |
| notification-worker | 4 | 4 | 0 | 28% | 55% | ✅ OK |
| ai-pipeline-worker | 2 | 1 | 1 | 78% | 82% | ⚠ Degraded |
| flower-dashboard | 1 | 1 | 0 | 3% | 18% | ✅ OK |

**Per-service metrics:**
- CPU: average across running tasks
- Memory: average across running tasks
- Pending tasks: tasks that should be running but aren't (failing to start)

**Alert rules:**
- Desired ≠ Running: amber (tasks failing to start or crashing on start)
- CPU > 80%: amber
- Memory > 90%: red (risk of OOM kill)
- Pending > 0 for > 5 min: red

**Write Actions (Admin · DevOps):**
- "Restart all tasks" for a service — stops all running tasks; ECS scheduler starts fresh instances
- "Scale up" — increases desired task count (+1 to +10)
- "Scale down" — decreases desired task count (minimum 1 for critical workers)
- "Force task stop" per individual task (shows task ID + container IP) — for stuck tasks
- "View task logs" per task → CloudWatch log stream for that task

**Data Flow:**
- ECS DescribeServices API for desired/running/pending
- CloudWatch Container Insights for CPU/memory per task
- 60s poll (no faster — ECS metrics have ~60s lag)

**Edge Cases:**
- Celery-beat stopped: critical — all scheduled jobs stop; amber banner: "Celery Beat is not running. Scheduled jobs are paused. Restart immediately."
- All Celery workers down: red banner + auto C-18 incident

---

### Section 5 — RDS Panel (Primary + Replicas)

**Purpose:** PostgreSQL health for the 2,051-schema database — the most critical data layer in the platform.

**Primary + Replica Cards:**

| Instance | Role | CPU % | Connections | Read IOPS | Write IOPS | Free Storage | Replica Lag | Status |
|---|---|---|---|---|---|---|---|---|
| rds-primary-1 | Primary (write) | 34% | 1,840 / 5,000 | 2,400 | 8,200 | 420 GB | — | ✅ OK |
| rds-replica-1 | Read replica | 28% | 920 | 3,100 | 0 | 418 GB | 0.3s | ✅ OK |
| rds-replica-2 | Read replica | 31% | 1,020 | 2,900 | 0 | 416 GB | 4.2s | ⚠ Lag |

**Alert Thresholds:**

| Metric | Amber | Red |
|---|---|---|
| CPU | > 70% | > 90% |
| Connections | > 80% of max | > 95% of max |
| Replica lag | > 2s | > 10s |
| Free storage | < 100 GB | < 50 GB |
| Read IOPS | > 80% provisioned IOPS | > 95% |
| Write IOPS | > 80% provisioned IOPS | > 95% |

**PgBouncer Pool Status:**

| Pool | Mode | Server Connections | Client Connections | Queue Depth | Status |
|---|---|---|---|---|---|
| Primary pool | Transaction | 250/300 | 1,840 | 0 | ✅ OK |
| Replica-1 pool | Transaction | 120/200 | 920 | 0 | ✅ OK |
| Replica-2 pool | Transaction | 128/200 | 1,020 | 12 | ⚠ Queue |

**Connection high-water mark:** Shows maximum connections seen in last 24h (for capacity planning)

**Write Actions (Admin · DevOps):**
- "Promote Replica to Primary" — initiates RDS failover (2FA required · confirmation modal: "This will restart the current primary as a new replica. Failover time: ~60s. During failover, writes are unavailable.")
- "Add Read Replica" — triggers RDS CreateDBInstanceReadReplica (async, 15–30 min) (Admin only)
- "Modify instance class" — links to C-10 scaling page (cannot be done in-page — requires ECS stop + instance resize + restart)
- "View slow query log" → deep-links to C-11 Database Admin Dashboard filtered to this instance

**Multi-AZ status:**
- Multi-AZ enabled: ✅
- Standby AZ: ap-south-1b (primary is ap-south-1a)
- Failover SLA: < 60s

**Data Flow:**
- RDS metrics from CloudWatch `AWS/RDS` namespace
- PgBouncer stats from `pgbouncer_stats_api` endpoint (internal network)
- Replica lag: `ReplicaLag` metric from CloudWatch
- 30s poll

---

### Section 6 — ElastiCache Memcached Panel

**Purpose:** Memcached cluster health — cache layer for session keys, tenant metadata, rate-limit counters, and API response cache.

**Cluster Overview:**

| Node | Node ID | Memory Used | Memory Max | Hit Rate | Evictions/min | New Connections | Status |
|---|---|---|---|---|---|---|---|
| Node 1 | memcached-001 | 4.8 GB | 6.4 GB (75%) | 96.2% | 0 | 12 | ✅ OK |
| Node 2 | memcached-002 | 4.2 GB | 6.4 GB (66%) | 97.1% | 0 | 14 | ✅ OK |
| Node 3 | memcached-003 | 5.3 GB | 6.4 GB (83%) | 95.8% | 8 | 9 | ⚠ High memory |

**Alert Thresholds:**

| Metric | Amber | Red |
|---|---|---|
| Memory per node | > 80% | > 90% |
| Cache hit rate | < 90% | < 80% |
| Evictions/min | > 100 | > 1,000 |
| New connections/min | > 500 | > 1,000 |

**Cluster-level Metrics:**
- Overall hit rate: calculated from sum(CacheHits) / (sum(CacheHits) + sum(CacheMisses)) across all nodes
- Total memory used: sum across nodes
- Total evictions: sum across nodes (high evictions = cache pressure → consider adding node)

**Time-series Charts (last 1h):**
- Memory usage per node (stacked)
- Commands/sec (gets vs sets) — from ElastiCache CloudWatch `GetRequests` + `SetRequests`
- Hit/miss ratio (cluster-wide)
- Evictions (cluster-wide)

**Write Actions (Admin · DevOps):**
- "Add node to cluster" → scales out Memcached cluster by adding a new node (auto-rebalancing handled by ElastiCache) — 2FA required
- "Flush all cache" → `cache.clear()` via django.core.cache — clears all keys across cluster — 2FA required + confirmation modal (impact: next 60s will be cache-cold; DB load will spike)
- "Remove node" → scales in cluster by removing the least-loaded node — 2FA required + confirmation showing traffic impact estimate

---

### Section 7 — ALB (Application Load Balancer) Panel

**Purpose:** Request routing health, target group status, and error rate monitoring.

**Target Groups Table:**

| Target Group | Protocol | Healthy Targets | Unhealthy | Requests/min | 5xx/min | Latency P99 |
|---|---|---|---|---|---|---|
| Lambda-portal | HTTPS → Lambda | 3/3 | 0 | 4,200 | 2 | 180ms |
| Lambda-api | HTTPS → Lambda | 3/3 | 0 | 12,800 | 8 | 95ms |
| ECS-celery-flower | HTTP → ECS | 1/1 | 0 | 12 | 0 | 45ms |

**ALB Level Metrics:**
- Total requests/min (last 5 min)
- 4xx rate
- 5xx rate
- Active connections
- Processed bytes/min

**SSL Certificate Status:**
- Primary domain: `*.platform.in` — ACM Certificate — Expires: Sep 2027 ✅
- API domain: `api.platform.in` — ACM Certificate — Expires: Sep 2027 ✅
- 90-day renewal warning; ACM auto-renews managed certs

**Write Actions (Admin · DevOps):**
- "Drain target" — removes a specific Lambda ARN/ECS task from target group (routes no new requests; existing connections complete) — use for deployments without downtime
- "Re-register target" — adds back a drained target
- "View access logs (last 1h)" → S3 ALB access log tail (sampled)

---

### Section 8 — CloudFront Summary

**Purpose:** CDN health summary (read-only — detailed management is in C-06).

**Data shown:**
- 3 distributions: Portal · Static Assets · API Edge
- Each: cache hit rate (5 min) · requests/min · error rate
- Overall bandwidth (last 1h)
- Link: "Manage in CDN & Asset Manager →" (C-06)

**Write actions:** None on this page — all in C-06.

---

### Section 9 — S3 Buckets Summary

**Purpose:** Storage health across all platform S3 buckets.

**Buckets Table:**

| Bucket | Purpose | Size | Object Count | Access | Versioning | Status |
|---|---|---|---|---|---|---|
| platform-static-assets | CSS/JS/fonts | 12.4 GB | 84,200 | Public (CloudFront only) | ✅ | OK |
| platform-tenant-media | Tenant uploaded files | 2.1 TB | 8.4M | Private | ✅ | OK |
| platform-db-backups | RDS snapshots export | 840 GB | 1,240 | Private | ✅ | OK |
| platform-logs | Access + application logs | 3.8 TB | 42M | Private | ✅ | OK |
| platform-ai-datasets | AI training + job data | 280 GB | 128K | Private | ✅ | OK |
| platform-compliance | DPDPA/CERT-In docs | 24 GB | 8,400 | Private (read-Admin only) | ✅ | OK |

**Alerts:**
- Any bucket with public access not matching expected (static-assets): red alert
- Storage > 80% of estimated monthly quota: amber
- Bucket lifecycle policy missing on log/backup buckets: amber

**Write actions (Admin only):**
- "Set lifecycle policy" → dropdown of pre-configured policies (30-day backup → Glacier transition, 90-day logs → Glacier)
- "Block all public access" emergency toggle (for static-assets: warns that CDN will break)

---

### Section 10 — Infrastructure Cost Panel

**Purpose:** Daily infrastructure cost tracking to catch runaway spending early.

**Cost Summary:**

| Service | Today (est.) | Yesterday | MTD | Budget |
|---|---|---|---|---|
| Lambda invocations | ₹1,840 | ₹1,920 | ₹42,000 | ₹60,000 |
| RDS (db.r6g.2xlarge × 3) | ₹4,200 | ₹4,200 | ₹92,400 | ₹110,000 |
| ElastiCache (cache.r6g.xlarge × 6) | ₹2,100 | ₹2,100 | ₹46,200 | ₹55,000 |
| CloudFront | ₹1,200 | ₹1,150 | ₹24,800 | ₹35,000 |
| S3 | ₹480 | ₹470 | ₹10,200 | ₹15,000 |
| ALB | ₹180 | ₹175 | ₹3,900 | ₹5,000 |
| **Total** | **₹10,000** | **₹10,015** | **₹219,500** | **₹280,000** |

**Cost anomaly detection:**
- Day-over-day increase > 20%: amber alert
- MTD > 80% of budget: amber
- MTD > 95% of budget: red + notification to Platform Admin

**Data source:** AWS Cost Explorer (1-day delay); today's estimate is calculated from usage metrics × AWS pricing

---

## 5. User Flow

### Flow A — Exam Day Monitoring

1. DevOps opens Infrastructure Monitor 30 min before exam start
2. Exam Day Mode banner not yet active (no active exams)
3. Checks Lambda concurrency: exam-submit at 12% (pre-exam warm baseline)
4. Checks RDS connections: 240/5,000 (normal)
5. Checks Memcached memory: 75% / 66% / 83% — Node 3 noted as higher
6. Exam starts: Exam Day Mode banner activates, poll interval drops to 15s
7. Lambda concurrency climbs: exam-submit 420 → 680 → 840 (84% of reserved)
8. Amber alert: exam-submit concurrency > 80%
9. DevOps opens C-10 → increases reserved concurrency from 1,000 → 1,500
10. Concurrency drops to 56% — exam completes successfully

### Flow B — RDS Replica Lag Incident

1. RDS panel: replica-2 lag = 8.4s (amber → red in 2 min)
2. API Health Monitor (C-04): result-fetch P99 = 680ms (SLA: 500ms) — reads routed to slow replica
3. DevOps clicks "Promote Replica to Primary" — selects replica-1 (healthy) as new primary
4. 2FA confirmation modal
5. RDS failover initiates: ~55s downtime on write path
6. New primary: rds-replica-1 (now primary, lag = 0)
7. Old primary: rds-primary-1 now in recovery (becomes new replica-1)
8. C-18 incident created: "RDS failover — rds-primary-1 replaced due to replica cascade"

### Flow C — Memcached Node Memory Alert

1. Node 3 memory: 91% (red alert)
2. Evictions: 12/min (cache data being evicted under memory pressure)
3. DevOps reviews cluster metrics: high eviction rate indicates memory pressure from session + rate-limit keys
4. Opens C-03 System Config → reduces session timeout from 720 min to 480 min
5. Celery task: purges expired session cache keys
6. Memory drops to 74% within 30 min
7. Alternatively: Admin considers "Add node to cluster" from write action panel to scale out

---

## 6. Component Structure (Logical)

```
InfrastructureMonitorPage
├── PageHeader
│   ├── GlobalHealthMatrix (service × status grid)
│   ├── VerdictBanner
│   ├── ExamDayModeBanner (conditional)
│   └── ActionButtons (OpenIncident · ViewCost · AutoRefreshToggle)
├── KPIStrip × 6
├── LambdaConcurrencyPanel
│   ├── AccountLevelSummaryBar
│   └── FunctionConcurrencyTable (write actions inline)
├── ECSClusterPanel
│   └── ECSServiceTable (with write actions)
├── RDSPanel
│   ├── InstanceCards × 3 (Primary + 2 Replicas)
│   ├── PgBouncerPoolTable
│   └── WriteActionButtons
├── ElastiCachePanel
│   ├── NodeCards × 3
│   ├── ClusterLevelMetrics
│   └── TimeSeriesCharts
├── ALBPanel
│   ├── TargetGroupsTable
│   ├── ALBLevelMetrics
│   └── SSLCertStatus
├── CloudFrontSummary (read-only, link to C-06)
├── S3BucketsPanel
├── InfrastructureCostPanel
└── ActionsDrawer (right-side, 560px — opens for write actions)
    ├── ConfirmationForm
    ├── ImpactStatement
    └── TwoFAGate (for critical actions)
```

---

## 7. Data Model (High-Level)

### platform_infra_events (write action audit log)

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| service | ENUM | lambda/ecs/rds/elasticache/alb/s3 |
| action | VARCHAR(100) | e.g., `rds_failover_initiated` |
| resource_id | VARCHAR(200) | ARN or resource name |
| actor_id | UUID FK → platform_staff | |
| actor_ip | INET | |
| before_state | JSONB | metric snapshot before action |
| after_state | JSONB | metric snapshot 5 min after action |
| twofa_used | BOOLEAN | |
| reason | TEXT | nullable |
| created_at | TIMESTAMPTZ | |

---

## 8. Validation Rules

| Action | Validation |
|---|---|
| Change Lambda reserved concurrency | Min 10 · Max = account reserved concurrency limit · Cannot set exam-critical function to 0 (blocks exams) |
| Promote RDS replica to primary | Only allowed if replica lag < 30s · 2FA required · Confirmation with "writes unavailable for ~60s" warning |
| Memcached cache flush | Full cluster flush: 2FA required + confirmation "All cache cold for ~60s; DB load will spike" · No partial key-pattern flush (Memcached limitation — use C-03 targeted session/permission flush instead) |
| ECS scale down | Cannot scale below 1 for critical workers (celery-worker, celery-beat) |
| S3 block public access (static bucket) | Warning: "Blocking public access on the static assets bucket will break all CSS/JS/images on all 2,050 portals. Confirm?" + 2FA |
| Add Memcached node | Scales out cluster; ElastiCache handles key rebalancing automatically; single-AZ constraint shown if applicable |
| RDS add replica | Admin only · confirmation modal showing estimated 15–30 min provisioning time |

---

## 9. Security Considerations

| Control | Detail |
|---|---|
| AWS API calls | All AWS API calls made server-side via IAM role; no AWS credentials exposed to browser |
| Write action scope | IAM role for infra-monitor service has minimum necessary permissions: `lambda:PutFunctionConcurrency` · `rds:FailoverDBCluster` · `elasticache:AddTagsToResource` etc. — cannot delete resources |
| 2FA on critical writes | RDS failover, Memcached flush, Lambda concurrency change all require TOTP |
| Audit log | All write actions logged to `platform_infra_events` with before/after state snapshots |
| CERT-In compliance | Infrastructure events (especially failovers) retained in audit log for breach investigation evidence (6-hour CERT-In reporting window applies to data breaches, not infra events; but evidence retention is good practice) |
| Read replica promotion | Safeguard: cannot promote replica with lag > 30s without explicit override — prevents data loss window |
| S3 public access controls | Cannot enable public access on non-static buckets via this UI; only static-assets bucket has public toggle |

---

## 10. Edge Cases (System-Level)

| Scenario | Handling |
|---|---|
| CloudWatch API rate limiting | Batch all metrics into single GetMetricData call per service panel; 25s Memcached cache; amber "Metrics delayed" indicator if stale |
| AWS region partial outage (ap-south-1) | Infra monitor itself may be degraded; DR site (ap-southeast-1) procedures link shown in header; automatic failover is not triggered from this UI — requires manual DR decision |
| Lambda concurrency limit hit (account-wide) | Red banner: "Account Lambda concurrency limit reached. New invocations are being throttled. Request limit increase from AWS Support." + direct link |
| RDS storage full | Red alert + "CRITICAL: RDS storage full. Database writes are failing." + immediate escalation to DBA via email + C-18 auto-incident |
| PgBouncer pool exhaustion | Amber/red on connection queue > 50; write action available: "Restart PgBouncer pool" (ECS task restart) |
| ElastiCache node degraded | Node shows "Degraded" status; Memcached clients automatically skip degraded nodes (consistent hashing); cache miss rate may spike temporarily; no write action available during node recovery |
| S3 bucket access denied | Admin sees "Permission denied" in bucket size column; bucket may have policy override; investigate via CloudTrail |
| ECS task in STOPPED state cycling (crash loop) | Task count shows 8 desired / 6 running / 2 pending repeatedly; "crash loop" indicator on service row; "View task logs" button highlighted to help diagnose |

---

## 11. Performance & Scaling Strategy

| Concern | Strategy |
|---|---|
| CloudWatch API calls | One GetMetricData batch call per panel per poll cycle; each batch handles up to 500 metric queries; Memcached 25–30s cache prevents double-fetching |
| Page load with 8 panels | Each panel loaded via separate HTMX `?part=` request; panels load in parallel; page shell loads in < 100ms; panels fill in as CloudWatch data arrives |
| Exam day poll frequency | Poll interval halved (30s → 15s); additional Memcached cache keys created for exam-critical metrics at 15s TTL |
| Write action feedback | All write actions trigger async Celery job; UI shows "Action in progress" spinner; polls job status every 5s; completion notification in platform alert bell |
| Historical charts | Charts in drawer panels use CloudWatch GetMetricData with appropriate period (1-min for 1h range; 5-min for 6h; 1-hour for 7d); no DynamoDB/DB needed |
| Cost data | AWS Cost Explorer has 1-day delay; MTD estimate built from usage metrics × pricing table (calculated server-side); accuracy within 5% |

---

## Amendment — G4: Celery Queues Tab

**Gap addressed:** DevOps had no visibility into Celery worker count per queue, queue depth, failed task rate, dead-letter queue items, or worker restart capability.

### New Tab on Infrastructure Monitor — Celery Queues

**Access:** `/engineering/infrastructure/?tab=celery-queues` — top-level tab on the page.

**Queue Health Overview Table:**

| Column | Description |
|---|---|
| Queue Name | e.g., `default` · `exam_critical` · `low_priority` · `ai_pipeline` |
| Active Workers | Workers currently processing tasks from this queue |
| Idle Workers | Workers connected but not processing |
| Queue Depth | Messages waiting to be consumed (tasks enqueued but not yet picked up) |
| Processed/hr | Tasks completed in last 1 hour |
| Failed/hr | Tasks failed in last 1 hour |
| Avg Duration | Average task execution time (last 1h) |
| DLQ Count | Dead-letter queue items for this queue (failed + not retried) |
| Status | ✅ Healthy · ⚠ High depth · ❌ No workers |

**Alert thresholds:**
- Queue depth > 1,000: amber · > 10,000: red
- No active workers for a queue: red (critical — tasks silently accumulating)
- DLQ count > 0: amber (failed tasks not retried)

**Per-queue actions (DevOps · Admin):**
- **Pause/Resume queue:** Stops workers consuming from this queue (tasks remain enqueued); used before risky maintenance. No 2FA needed — reversible instantly.
- **Retry all DLQ:** Moves all DLQ items back to main queue for retry — confirmation modal showing DLQ item count.
- **View DLQ items:** Opens `celery-queue-drawer` with list of failed task entries (task name · error · first failed · retry count).

**Worker Detail (per queue, expandable row):**

| Column | Description |
|---|---|
| Worker Hostname | e.g., `celery@worker-01` |
| Current Task | Task name currently executing (or "idle") |
| Uptime | Duration since worker process started |
| Tasks Completed (session) | Since last restart |
| Actions | Restart worker (graceful: finish current task + restart · hard: SIGKILL immediately) |

**DLQ Item list (celery-queue-drawer):**
- Task name · exception type · error message · failed at · retry count (default: 3) · "Retry this task" individual action

**Data Flow:**
- Worker + queue data: Celery Inspect API (`celery.control.inspect`) polled every 30s — `active()`, `reserved()`, `stats()` per worker
- Queue depth: Celery `app.control.inspect().active_queues()` + broker queue stats (stored in `platform_celery_queue_stats` table, updated every 30s by Celery beat)
- DLQ: `platform_celery_task_results` table filtered to `status = failure AND retry_count >= 3`
- Note: Celery result backend is the Django ORM (DB), not Memcached/Redis — task results stored in `platform_celery_task_results` table

---

## Amendment — G23: ECS Task Definition Editor

**Gap addressed:** DevOps could not update a container's Docker image tag, CPU, or memory from the portal. Every container update required a full CI/CD pipeline run even when only the image tag needed to change.

### New Drawer — ECS Task Definition Editor

**Trigger:** Click on any ECS service row in the ECS Cluster Panel → opens `ecs-task-def-drawer` (640px)

**Drawer Tabs:**

**Tab 1 — Current Definition:**
- Task definition family: e.g., `platform-celery-worker`
- Current revision: e.g., `platform-celery-worker:47`
- Container table (one row per container in the task):

| Field | Value |
|---|---|
| Container Name | `celery-worker` |
| Docker Image URI | `123456789.dkr.ecr.ap-south-1.amazonaws.com/platform:celery-b47a3f2` |
| Image Tag | `celery-b47a3f2` |
| CPU (vCPUs) | 1.0 |
| Memory (MB) | 2048 |
| Essential | Yes |
| Environment Variables | Count: 8 (link to C-05 env vars) |

**Tab 2 — Edit Image Tag:**
- "New image tag" text input (e.g., `celery-c98d1e5`)
- Image URI preview: auto-builds full URI from registry + input tag
- "Validate Image" button → calls ECR `describeImages` API to verify tag exists before saving
- Cost impact: none (same CPU/memory; image tag change only)
- "Apply New Tag" → 2FA confirmation → calls AWS ECS `registerTaskDefinition` with new image URI → creates new revision (e.g., `:48`) → calls `updateService` with `forceNewDeployment: true` → rolling deployment begins
- Deployment progress: HTMX poll every 10s showing running task count (old revision → new revision)

**Tab 3 — Edit CPU / Memory:**
- CPU slider: 0.25 / 0.5 / 1.0 / 2.0 / 4.0 / 8.0 vCPUs (Fargate valid values)
- Memory slider: 512 / 1024 / 2048 / 4096 / 8192 MB (constrained by CPU selection)
- Cost impact estimate: shown inline in ₹/month (CPU/memory × ECS pricing × estimated hours)
- 2FA required for CPU/memory changes (higher blast radius than tag change)

**Tab 4 — Deployment History (last 10):**

| Column | Description |
|---|---|
| Revision | Task def revision number |
| Image Tag | Docker image tag deployed |
| CPU | vCPUs at time of deployment |
| Memory | MB at time of deployment |
| Deployed By | Staff name |
| Deployed At | Timestamp |
| Status | ✅ Active · ⬛ Replaced · ❌ Failed |
| Rollback | "Roll back to this revision" button (active for non-current revisions) |

**Rollback action:** Select any previous revision → "Roll back to revision :45" → calls ECS `updateService` with old revision ARN → rolling update begins → confirmation toast "Rolling back {service} to revision :45"
