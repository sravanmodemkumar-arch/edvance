# C-17 — Centralized Log Viewer

> **Route:** `/engineering/logs/`
> **Division:** C — Engineering
> **Roles:** All Division C roles (10–17) — see access matrix
> **File:** `c-17-logs.md`
> **Priority:** P1
> **Status:** ✅ Spec done

---

## 1. Page Name & Route

**Page Name:** Centralized Log Viewer
**Route:** `/engineering/logs/`
**Part-load routes:**
- `/engineering/logs/?part=kpi` — log health KPI
- `/engineering/logs/?part=search` — log search results
- `/engineering/logs/?part=trace&correlation_id={id}` — correlation ID trace view
- `/engineering/logs/?part=alert-rules` — log-based alert rules
- `/engineering/logs/?part=retention-policy` — log retention config

---

## 2. Purpose (Business Objective)

The Centralized Log Viewer aggregates all CloudWatch Logs from every Lambda function, ECS task, and infrastructure component into a single searchable interface. The platform generates millions of log lines per day at peak; without a unified view, engineers must switch between dozens of CloudWatch log groups to trace a single user's exam submission across multiple Lambda hops.

The most powerful feature is correlation ID tracing: every API request generates a unique `correlation_id` (UUID) that is propagated through all downstream Lambda calls. A single correlation ID can be pasted into this page to reconstruct the full journey of one exam submission — from the student clicking "Submit" through authentication → question validation → answer persistence → result computation — across all services.

**Business goals:**
- Eliminate multi-tab CloudWatch navigation during incident response
- Enable single-request full-trace from correlation ID in < 10 seconds
- Support tenant-scoped log filtering (isolate logs for one institution's issue)
- Provide log-based alert rules (pattern → PagerDuty) without CloudWatch Alarms
- Give all engineering roles appropriate visibility into logs for their domain

---

## 3. User Roles

| Role | Access | Log Scope |
|---|---|---|
| Platform Admin (10) | Full: search · alerts · retention config | All log groups |
| Backend Engineer (11) | Search + saved queries + alerts | API service logs |
| Frontend Engineer (12) | Search + saved queries | Frontend/HTMX template logs |
| Mobile Engineer (13) | Search + saved queries | Mobile API + FCM logs |
| DevOps / SRE (14) | Full: search · alerts · retention config | All log groups |
| DBA (15) | Search + saved queries | Database query logs · PgBouncer logs |
| Security Engineer (16) | Full: search · alerts · export | All log groups (security investigation scope) |
| AI/ML Engineer (17) | Search + saved queries | AI pipeline logs · LLM API logs |

> **PII Note:** Log lines containing student PII are redacted by Lambda middleware before writing to CloudWatch. Student IDs are replaced with hashed IDs in logs. IP addresses are retained for security purposes.

---

## 4. Section-Wise Detailed Breakdown

---

### Section 1 — Page Header & Log Health

**Purpose:** Confirm log ingestion is working and provide quick access to common actions.

**Header elements:**
- H1 "Centralized Log Viewer"
- Log ingestion status: ✅ All log groups ingesting · ⚠ {n} log groups with errors · ❌ Log ingestion stopped
- "New Search" primary CTA (opens search panel)
- "Trace Correlation ID" quick-access (opens trace panel)
- Saved searches quick-access: dropdown of recently used saved searches
- Last log received: "Most recent log: 8s ago (exam-service-submit)"

**Log Volume Indicator:**
- "Log volume (last 5 min): 842K lines / 124 MB"
- Trend: ↑ compared to last 5 min baseline (exam day) or ↓ (normal day)

---

### Section 2 — KPI Strip

**KPI Cards:**

| Card | Metric | Alert |
|---|---|---|
| Error Rate (logs) | Count of ERROR-level lines / total (last 5 min) | > 1% amber · > 5% red |
| Log Volume (1h) | Total log lines ingested | Spike > 200% = amber |
| Log Ingestion Lag | Delay from Lambda write to CloudWatch availability | > 60s = amber |
| Active Alerts | Log-based alerts currently firing | > 0 = amber |
| Storage Used (MTD) | CloudWatch Logs storage this month | > 80% budget = amber |
| Saved Searches | Count of saved queries by this user | — |

---

### Section 3 — Log Search Interface

**Purpose:** The primary search surface — full-text search across all log groups.

**Search Bar:**
- Full-text search input (supports CloudWatch Logs Insights query syntax)
- Smart mode: simple text search (auto-wraps in `filter @message like "{term}"`)
- Expert mode: raw CloudWatch Logs Insights query syntax
- Toggle between modes

**Filter Panel (left sidebar):**

| Filter | Options |
|---|---|
| Log Group | All · Service groups (exam · auth · result · ai · billing · infra) · Individual log groups |
| Log Level | All · DEBUG · INFO · WARN · ERROR · CRITICAL |
| Time Range | Last 5m · Last 15m · Last 1h · Last 6h · Last 24h · Last 7d · Custom range |
| Service | Dropdown of all ~68 Lambda functions + ECS services |
| Tenant | Search by tenant schema name or institution name (filters for logs tagged with tenant_id) |
| Correlation ID | UUID input — triggers trace view |
| Request Path | e.g., `/api/exams/*/submit/` |
| HTTP Status | 200 · 4xx · 5xx |

**Log Results Table:**

| Column | Description |
|---|---|
| Timestamp | ISO 8601 with milliseconds |
| Level | DEBUG · INFO · WARN · ERROR · CRITICAL (colour-coded) |
| Service | Lambda function name / ECS service |
| Message | Log message (first 200 chars; click to expand) |
| Correlation ID | UUID (clickable — jumps to trace view) |
| Tenant ID | Hashed tenant identifier (if present) |
| Request ID | Lambda request ID |

**Results pagination:** 100 lines per page · newest first (default) · toggle to oldest first

**Line expand:** Click any log line → full log entry shown as formatted JSON (if structured) or plain text

**Export:** "Export results" → CSV download · max 10,000 lines per export · Security/Admin: up to 100,000 lines

**Highlighted search terms:** Search term highlighted in yellow within matching log lines

**Time distribution chart:** Small bar chart above results showing log volume distribution across the selected time window — helps identify when errors clustered

---

### Section 4 — Correlation ID Trace View

**Purpose:** Reconstruct the complete journey of a single request across all services.

**Trigger:** Click correlation ID in log results · OR paste UUID in "Trace Correlation ID" field in header

**Trace Timeline Display:**

```
Correlation ID: a1b2c3d4-e5f6-7890-abcd-ef1234567890
Request: POST /api/exams/exam_042/submit/  |  Student: student_hashed_84219  |  Duration: 284ms

▼ auth-service-token-verify           [+0ms]   [+12ms]    ✅ JWT validated
▼ exam-service-get-session            [+12ms]  [+18ms]    ✅ Exam session retrieved
▼ exam-service-validate-answers       [+30ms]  [+145ms]   ✅ 80 answers validated
  ▼ rds-query: SELECT exam_questions   [+31ms]  [+42ms]    ✅ 80 rows in 11ms
  ▼ rds-query: UPDATE exam_sessions    [+145ms] [+155ms]   ✅ Session updated
▼ result-service-compute-score        [+155ms] [+262ms]   ✅ Score computed
  ▼ rds-query: INSERT exam_submissions [+156ms] [+172ms]   ✅ Result persisted
▼ notification-service-queue-result   [+262ms] [+268ms]   ✅ Notification queued
▼ exam-service-return-response        [+268ms] [+284ms]   ✅ 200 OK returned
```

**Visual representation:**
- Waterfall chart (like browser DevTools Network tab but for microservices)
- Each service hop: service name · start offset · duration · status · colour (green/amber/red)
- DB queries shown as sub-spans indented below their parent service
- Slow spans (> 50% of total request time): highlighted amber

**Span detail (click any span):**
- Full log lines for that service during this request
- Input/output summary (where available from structured logs)
- Error details (if failed span)

**Failed request trace:**
- Failed spans shown in red
- "Root cause" indicator: first span that failed highlighted as probable root cause
- Downstream spans shown as "Skipped" (not executed due to upstream failure)

**Data Flow:**
- Correlation IDs propagated via `X-Correlation-ID` header in all inter-service calls
- Each Lambda logs `correlation_id` as structured field in every log line
- Trace view: CloudWatch Logs Insights query filters by correlation_id across all log groups
- Trace assembly: server-side sorting by timestamp + service topology
- Query time: typically < 5s for a 1h time window; longer for 24h+ windows

**Time window for trace:**
- Default: ±1 hour around first log line found with this correlation ID
- Expandable to ±24h if request was long-running (e.g., async background job)

---

### Section 5 — Service Log Group Browser

**Purpose:** Navigate directly to logs for a specific service without searching.

**Layout:** Left panel list of all log groups; click to load most recent logs for that group

**Log Group Hierarchy:**

```
📁 Lambda Functions (68)
  📄 /aws/lambda/exam-service-submit
  📄 /aws/lambda/exam-service-questions
  📄 /aws/lambda/auth-service-login
  ... (all 68)
📁 ECS Services (5)
  📄 /ecs/celery-worker
  📄 /ecs/celery-beat
  📄 /ecs/notification-worker
  📄 /ecs/ai-pipeline-worker
  📄 /ecs/flower-dashboard
📁 RDS / PgBouncer
  📄 /rds/primary/postgresql
  📄 /rds/pgbouncer
📁 Infrastructure
  📄 /alb/access-logs
  📄 /cloudfront/access-logs
  📄 /vpc/flow-logs
```

**On group click:**
- Latest 100 log lines load in the results panel
- All filter controls apply to this group

**Recent errors per group:**
- Each log group in the list has a mini indicator: green dot (no errors in 1h) · amber (errors in last 1h) · red (errors in last 5 min)

---

### Section 6 — Saved Search Queries

**Purpose:** Store frequently-used searches for quick reuse during incidents.

**Saved Search Table:**

| Name | Description | Log Group | Query | Created By | Shared | Last Used |
|---|---|---|---|---|---|---|
| Exam submit errors (last 1h) | All 5xx on exam submit | exam-service-submit | `filter @message like "error" and status = 500` | Priya | ✅ Team | 2h ago |
| Auth failures by tenant | Failed logins grouped by tenant | auth-service-login | `stats count(*) by tenant_id` | Rohan | ✅ Team | 1 day ago |
| Cold start storm detector | Cold starts in 5-min windows | All Lambda | `filter @initDuration > 0 | stats count(*) by bin(5min)` | DevOps | ✅ Team | 3 days ago |

**Actions:**
- "Run" — executes saved search immediately
- "Edit" — modifies query or filters
- "Share with team" — marks as visible to all Div C roles
- "Delete" — removes (own queries only; team queries: Admin/DevOps only)
- "Set as quick-access" — adds to header dropdown

**Create saved search:** After running a search → "Save search" button → name + description + share toggle

---

### Section 7 — Log-Based Alert Rules

**Purpose:** Trigger PagerDuty or platform notifications when specific patterns appear in logs.

**Alert Rules Table:**

| Rule Name | Log Group | Pattern | Threshold | Window | Action | Status |
|---|---|---|---|---|---|---|
| Database connection pool exhausted | rds/pgbouncer | `"no more connections allowed"` | 1 match | 1 min | PagerDuty P1 | ✅ Active |
| Exam submission error spike | exam-service-submit | `"status":500` | > 10 matches | 5 min | PagerDuty P2 + Slack | ✅ Active |
| JWT validation failure storm | auth-service | `"jwt_invalid":true` | > 100 matches | 5 min | PagerDuty P1 + C-18 auto | ✅ Active |
| AI pipeline worker crashed | ecs/ai-pipeline-worker | `"CRITICAL"` | 1 match | 1 min | Email AI/ML team | ✅ Active |
| S3 access denied | All Lambda | `"AccessDenied"` | 1 match | 1 min | Security Engineer email | ✅ Active |

**Add/Edit alert rule (Admin/DevOps/Security):**
- Log group scope (single or multiple)
- Pattern: text match OR regex
- Threshold: count of matches
- Window: 1 min · 5 min · 15 min · 60 min
- Action: Email · Slack · PagerDuty P3/P2/P1 · C-18 auto-incident
- Cooldown: don't re-fire within N minutes of last alert

**Alert rule evaluation:**
- Celery beat evaluates all active alert rules every 60s
- CloudWatch Logs Insights query per rule; batched where possible
- Evaluation lag: < 90s from log write to alert fire

---

### Section 8 — Log Retention Policy

**Purpose:** Configure how long logs are retained per log group (cost management).

**Retention Policy Table:**

| Log Group | Current Retention | Recommended | Storage/Month | Action |
|---|---|---|---|---|
| Lambda functions (68 groups) | 30 days | 30 days (security) | ₹2,400 | — |
| ECS services | 30 days | 14 days | ₹280 | Reduce |
| RDS PostgreSQL | 14 days | 7 days | ₹180 | Reduce |
| PgBouncer | 7 days | 7 days | ₹42 | — |
| ALB access logs | 90 days (CERT-In) | 90 days | ₹840 | — |
| CloudFront access logs | 90 days | 90 days | ₹620 | — |
| VPC flow logs | 30 days | 30 days | ₹380 | — |
| **Total** | | | **₹4,742/month** | |

**Edit retention (Admin/DevOps):**
- Click log group → retention period select
- Minimum enforcement: Lambda logs minimum 30 days (security/CERT-In requirement)
- ALB access logs minimum 90 days (CERT-In audit requirement)

**Cost vs retention trade-off:**
- CloudWatch Logs storage: ₹0.03/GB/month
- Current total: ~157 GB stored logs
- Reducing ECS retention 30 → 14 days: saves ~₹84/month

---

## 5. User Flow

### Flow A — Tracing a Failed Exam Submission (Incident Response)

1. DevOps receives alert: "Exam submit error spike — 24 errors in 5 min"
2. Opens `/engineering/logs/`
3. Searches: service = exam-service-submit · level = ERROR · time = last 15 min
4. Finds error log: "RDS connection timeout at exam_submission INSERT"
5. Clicks correlation_id on that log line
6. Trace view opens: shows full request span
7. Root cause highlighted: `rds-query: INSERT exam_submissions` — timed out after 30s
8. Sub-span for RDS query shows: "waiting for PgBouncer pool connection"
9. DevOps jumps to C-11 → confirms connection pool queue depth = 48
10. Takes action: terminates idle connections → pool clears → exam submissions resume

### Flow B — Security Investigation (JWT Attack)

1. Security Engineer triggered by alert: "JWT validation failures > 100 in 5 min"
2. Opens Logs → runs saved search "JWT failure storm"
3. Filter by correlation_id cluster: 842 JWT failures with same source IP subnet
4. Log lines show: `algorithm":"none"` in JWT header (algorithm confusion attack)
5. Confirms: all failures from 45.142.212.0/24
6. Jumps to C-13 → blocks subnet in WAF
7. Exports log search results as CSV → PDF → CERT-In report

### Flow C — DBA Investigating Slow Queries in Logs

1. DBA navigates to `/engineering/logs/`
2. Selects log group: `/rds/primary/postgresql`
3. Searches: `duration > 1000` (PostgreSQL slow query log format)
4. Finds: `SELECT * FROM exam_answers WHERE student_id = $1` taking 4.2s
5. Copies query text → navigates to C-11 → EXPLAIN plan
6. Confirms missing index → applies fix

---

## 6. Component Structure (Logical)

```
CentralizedLogViewerPage
├── PageHeader
│   ├── LogIngestionStatusBadge
│   ├── PageTitle
│   ├── NewSearchButton
│   ├── TraceCorrelationInput
│   └── SavedSearchesDropdown
├── KPIStrip × 6
├── SearchInterface
│   ├── SearchBar (simple/expert toggle)
│   ├── FilterPanel (left sidebar)
│   │   ├── LogGroupFilter
│   │   ├── LogLevelFilter
│   │   ├── TimeRangePicker
│   │   ├── ServiceFilter
│   │   ├── TenantFilter
│   │   └── CorrelationIDInput
│   ├── TimeDistributionChart
│   └── LogResultsTable
│       └── LogLineRow × N
│           └── ExpandedLogLineView (click)
├── CorrelationTraceView
│   ├── RequestSummaryHeader
│   ├── WaterfallChart (spans)
│   └── SpanDetailPanel
├── ServiceLogGroupBrowser (left panel)
│   └── LogGroupHierarchy
├── SavedSearchQueries
│   └── SavedSearchTable
├── AlertRulesSection
│   └── AlertRuleTable (with add/edit)
└── LogRetentionPolicySection
    └── RetentionPolicyTable
```

---

## 7. Data Model (High-Level)

### platform_saved_log_searches

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| name | VARCHAR(100) | |
| description | TEXT | nullable |
| log_group_scope | JSONB | array of log group names or null (all) |
| query_text | TEXT | CloudWatch Logs Insights syntax |
| level_filter | ENUM | null/debug/info/warn/error/critical |
| service_filter | VARCHAR(100) | nullable |
| time_range | VARCHAR(50) | e.g., "last_1h" |
| created_by | UUID FK → platform_staff | |
| is_shared | BOOLEAN | |
| last_used_at | TIMESTAMPTZ | nullable |
| created_at | TIMESTAMPTZ | |

### platform_log_alert_rules

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| rule_name | VARCHAR(100) | |
| log_group_pattern | VARCHAR(200) | supports wildcards |
| pattern | TEXT | text match or regex |
| is_regex | BOOLEAN | |
| threshold_count | INTEGER | |
| window_minutes | SMALLINT | |
| action | ENUM | email/slack/pagerduty_p3/p2/p1/c18_incident |
| cooldown_minutes | SMALLINT | |
| is_enabled | BOOLEAN | |
| last_fired_at | TIMESTAMPTZ | nullable |
| created_by | UUID FK → platform_staff | |

---

## 8. Validation Rules

| Rule | Detail |
|---|---|
| Correlation ID format | Must be valid UUID v4; auto-validated on input |
| Log search time range | Maximum 7 days for search (CloudWatch Logs Insights limit); wider ranges: link to S3 archived logs |
| Alert rule pattern | Regex patterns validated before save; invalid regex: inline error |
| Log retention minimum | Lambda logs: min 30 days · ALB access logs: min 90 days · cannot set below minimum regardless of Admin role |
| Log export limit | Standard roles: 10,000 lines max · Security/Admin: 100,000 lines max |
| Saved search names | Unique per user; team-shared names unique across all users |
| Alert rule cooldown | Minimum 5 min · Maximum 1 day |
| Search query length | Max 10,000 characters (CloudWatch Insights limit) |

---

## 9. Security Considerations

| Control | Detail |
|---|---|
| PII redaction | Lambda middleware replaces student PII (name, email, phone) with hashed IDs before writing to CloudWatch; confirmed at Lambda layer — not at this page |
| Log access scope | Backend Engineer cannot see auth-service or security logs beyond their service; enforced by log group permission filter per role |
| VPC flow logs | Accessible to Security Engineer + Admin only; contain IP-level network data |
| CloudTrail logs | Not in this viewer; separate CloudTrail UI in AWS console; API calls are logged there |
| Export audit | All log exports logged in `platform_audit_log` with: actor · query · time range · line count |
| Correlation ID linkability | Correlation IDs are UUIDs — no PII embedded; safe to share/log |
| CloudWatch API access | `logs:FilterLogEvents` + `logs:StartQuery` + `logs:GetQueryResults` scoped to `/aws/lambda/{platform-prefix}*` and `/ecs/*`; cannot access non-platform log groups |

---

## 10. Edge Cases (System-Level)

| Scenario | Handling |
|---|---|
| CloudWatch Logs Insights rate limit (20 concurrent queries/account) | Platform queues searches; user sees "Search queued — {n} searches ahead of yours"; timeout after 5 min in queue |
| Correlation ID not found (too old, log rotated) | "No logs found for this correlation ID in the selected time window. Logs older than 30 days may be in S3 archive." + link to S3 archive retrieval |
| Very high log volume search (7-day × all groups) | Warning before query: "This search may take 60–120s and consume CloudWatch query budget. Proceed?" |
| Alert rule fires repeatedly without cooldown | Cooldown enforced in `last_fired_at` field; Celery beat skips rule evaluation if within cooldown window |
| Log group not ingesting (Lambda logging disabled) | KPI shows "1 log group with errors"; page header shows amber banner listing affected log groups |
| Structured log line fails JSON parse | Displayed as raw text; JSON-expand button disabled; no loss of data |
| Trace view finds spans with duplicate timestamps | Sorted by service topology (dependency order) as tiebreaker; deterministic display |

---

## 11. Performance & Scaling Strategy

| Concern | Strategy |
|---|---|
| CloudWatch Logs Insights latency | Simple queries (last 1h, single log group): 2–5s · Complex queries (7 days, all groups): 30–120s; async query with polling |
| Concurrent search limit | Platform rate-limits to 10 concurrent CloudWatch Insights queries; queue remaining searches |
| Trace reconstruction | Server-side assembly: < 500ms after logs retrieved from CloudWatch |
| Real-time log tail | `FilterLogEvents` API (not Insights); polled every 5s when live tail mode active; only for single log group |
| Alert rule evaluation | 60s Celery beat; batched CloudWatch queries where multiple rules target same log group |
| Saved search execution | Same path as manual search; no special pre-computation |
| Waterfall chart rendering | Server-side SVG generation for trace view; < 200ms for typical 10-span trace |
| Log volume KPI | CloudWatch `IncomingLogEvents` metric; same batched CloudWatch call as C-08/C-04 |
