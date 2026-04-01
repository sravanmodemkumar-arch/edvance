# C-04 — API Health Monitor

> **Route:** `/engineering/api-health/`
> **Division:** C — Engineering
> **Primary Role:** Platform Admin (Role 10) · Backend Engineer (Role 11) · DevOps/SRE (Role 14)
> **Read Access:** Frontend Engineer (Role 12) · Security Engineer (Role 16)
> **File:** `c-04-api-health.md`
> **Priority:** P0 — Must be operational before first institution goes live
> **Status:** ✅ Spec done

---

## 1. Page Name & Route

**Page Name:** API Health Monitor
**Route:** `/engineering/api-health/`
**Part-load routes:**
- `/engineering/api-health/?part=kpi` — global health KPI strip
- `/engineering/api-health/?part=table` — endpoint list table
- `/engineering/api-health/?part=drawer&endpoint_id={id}` — endpoint detail drawer
- `/engineering/api-health/?part=sla-panel` — exam-critical SLA panel
- `/engineering/api-health/?part=deprecation-panel` — deprecation tracker
- `/engineering/api-health/?part=version-registry` — API version registry

---

## 2. Purpose (Business Objective)

The API Health Monitor provides real-time and historical performance visibility across all Lambda-backed API endpoints — approximately 60–80 functions across all services. It is the first screen engineers open during an incident: latency spikes, error rate increases, cold start storms, and throttle events all surface here before users start complaining.

During exam peak (74K concurrent submissions), the exam-critical SLA panel becomes the most-watched screen in the organisation. The exam submit endpoint must stay below 200ms P99, and the result fetch endpoint below 500ms — breaching either SLA during an exam triggers immediate escalation to C-18.

Beyond real-time monitoring, this page also manages the API version lifecycle — tracking which versions are active, deprecated, and sunset — so that institution integrators have clear migration timelines.

**Business goals:**
- Detect API degradation within 30 seconds of onset
- Enforce exam-critical SLA contracts (submit < 200ms · result < 500ms P99)
- Track cold start frequency to guide provisioned concurrency decisions (C-10)
- Manage API deprecation lifecycle with 90-day sunset windows
- Provide Backend and DevOps engineers a shared operational view

---

## 3. User Roles

| Role | Access Level | Permissions |
|---|---|---|
| Platform Admin (10) | Level 5 | Full view + write: configure SLA thresholds · manage deprecation · acknowledge alerts |
| Backend Engineer (11) | Level 4 | Full view + write: acknowledge alerts · update deprecation notes · configure SLA thresholds |
| DevOps / SRE (14) | Level 4 | Full view + write (same as Backend Engineer) |
| Frontend Engineer (12) | Level 4 — Read | View endpoint health relevant to frontend; cannot modify |
| Security Engineer (16) | Level 4 — Read | View error patterns for security analysis; cannot modify |

---

## 4. Section-Wise Detailed Breakdown

---

### Section 1 — Page Header & Global Status

**Purpose:** Instant system-wide API health verdict at page load.

**Global Status Indicator (large, top of page):**

| Verdict | Colour | Condition |
|---|---|---|
| ✅ All Systems Healthy | Green | All endpoints: error rate < 0.5%, P99 < SLA, no throttles |
| ⚠ Degraded Performance | Amber | 1–5 endpoints: P99 > SLA or error rate 0.5–2% |
| 🚨 Critical Incident | Red pulsing | Any exam-critical endpoint > SLA or any endpoint error rate > 5% |
| — | Grey | Monitoring data unavailable (CloudWatch API issue) |

**Header elements:**
- H1 "API Health Monitor"
- Global status badge (large, colour-coded)
- Total endpoint count: "68 endpoints monitored"
- Last data refresh: "Updated 23s ago"
- Auto-refresh toggle: ON/OFF (default ON — refreshes every 30s)
- "Open Incident" button (Admin/Backend/DevOps — pre-fills C-18 with current health data)

**Exam Day Mode Banner (shown when active exam detected):**
- Triggered when `platform:active_exam_count` Memcached key > 0
- Amber/red banner: "🎓 EXAM IN PROGRESS — {n} active exams · {k} submissions in last 5 min · SLA monitoring active"
- SLA panel auto-expands in exam day mode

---

### Section 2 — KPI Strip — Platform-Wide API Metrics

**Purpose:** 5-minute rolling window summary across all endpoints.

**KPI Cards:**

| Card | Metric | Calculation | Alert |
|---|---|---|---|
| Total Requests (5m) | Sum of all invocations | CloudWatch SUM | — |
| Error Rate | 4xx+5xx / total (5m) | % | > 1% amber · > 5% red |
| P99 Latency (global avg) | P99 across all endpoints | CloudWatch P99 | > 1,000ms amber · > 3,000ms red |
| Cold Starts (5m) | Lambda cold start count | CloudWatch `InitDuration` count | > 50 amber · > 200 red |
| Throttle Events (5m) | HTTP 429 count | CloudWatch | > 10 amber · > 100 red |
| Active Lambda Instances | Warm instance count | Lambda GetAccountSettings | < 50% reserved = amber |

**Data Flow:**
- KPI strip: `GET /engineering/api-health/?part=kpi` — 30s HTMX poll
- All metrics from CloudWatch Metrics API (GetMetricStatistics or GetMetricData batch)
- Results cached in Memcached 25s to avoid CloudWatch API rate limiting (400 requests/sec limit)

---

### Section 3 — Exam-Critical SLA Panel

**Purpose:** Dedicated high-visibility panel for the endpoints with strict SLA contracts during exam operations.

**Always visible** (expanded during active exams; collapsible otherwise)

**Exam-Critical Endpoints:**

| Endpoint | Route | SLA (P99) | Current P99 | Status |
|---|---|---|---|---|
| Exam Submit | `POST /api/exams/{id}/submit/` | 200ms | {live} | ✅/⚠/🚨 |
| Question Fetch | `GET /api/exams/{id}/questions/` | 300ms | {live} | ✅/⚠/🚨 |
| Answer Save (auto-save) | `PATCH /api/exams/{id}/answer/` | 150ms | {live} | ✅/⚠/🚨 |
| Result Fetch | `GET /api/results/{id}/` | 500ms | {live} | ✅/⚠/🚨 |
| Auth Token Refresh | `POST /api/auth/token/refresh/` | 100ms | {live} | ✅/⚠/🚨 |
| Exam Session Init | `POST /api/exams/{id}/start/` | 300ms | {live} | ✅/⚠/🚨 |

**Per-endpoint display:**
- Large P99 gauge (circular) — colour shifts: green → amber → red
- Mini sparkline: P99 over last 30 min (1-min buckets)
- Invocation rate: requests/min (last 5 min)
- Error rate: % (last 5 min)
- Cold start rate: cold starts / total invocations (%)
- Provisioned concurrency: allocated vs consumed

**SLA breach actions (auto-triggered):**
- P99 crosses SLA threshold: amber banner on SLA panel + notification to Backend + DevOps on-call
- P99 > 2× SLA: red banner + auto-creates P0 incident in C-18 + PagerDuty alert
- 3 consecutive breaches (3-min window): escalation to Platform Admin

**Data Flow:**
- SLA panel: `GET /engineering/api-health/?part=sla-panel` — 15s HTMX poll (faster than general table)
- During active exam: poll interval drops to 10s
- P99 data from CloudWatch Metrics; provisioned concurrency from Lambda GetFunctionConcurrency API
- Memcached key `platform:sla_breach_active` set to true on breach; cleared on recovery — drives the red banner

---

### Section 4 — Endpoint List Table

**Purpose:** Full listing of all ~68 API endpoints with current health metrics.

**User Interaction:**
- Click row → opens endpoint detail drawer (640px)
- Filter by service · method · status · SLA group
- Sort by P99 latency · error rate · invocation count
- "View in CloudWatch" link per row (opens CloudWatch console deep-link)

**Table Columns:**

| Column | Description | Sortable |
|---|---|---|
| Method | GET · POST · PATCH · DELETE (colour-coded) | — |
| Endpoint Path | e.g., `/api/exams/{id}/submit/` | ✅ A–Z |
| Service | Lambda function name (e.g., `exam-service`) | ✅ |
| API Version | v1 · v2 · v3 badge | ✅ |
| Status | ✅ Healthy · ⚠ Degraded · 🚨 Critical · 🔕 Deprecated | ✅ |
| P50 (ms) | 5-min rolling P50 | ✅ |
| P95 (ms) | 5-min rolling P95 | ✅ |
| P99 (ms) | 5-min rolling P99 (coloured by SLA) | ✅ |
| Error Rate | % 4xx + 5xx (5 min) | ✅ |
| Req/min | Invocation rate (5 min) | ✅ |
| Cold Starts | Count in last 5 min | ✅ |
| SLA Group | Exam-critical · Standard · Internal | ✅ |

**Row Colour Rules:**
- P99 > SLA threshold: amber row highlight
- P99 > 2× SLA: red row highlight
- Error rate > 5%: red row highlight
- Status Deprecated: grey italic row

**Filter Bar (above table):**

| Filter | Options |
|---|---|
| Service | All · auth-service · exam-service · result-service · tenant-service · ai-service · notification-service · billing-service · content-service |
| HTTP Method | All · GET · POST · PATCH · DELETE |
| Status | All · Healthy · Degraded · Critical · Deprecated |
| SLA Group | All · Exam-critical · Standard · Internal |
| API Version | All · v1 · v2 · v3 |
| Show only unhealthy | Toggle (quick filter for incident response) |

**Data Flow:**
- Table: `GET /engineering/api-health/?part=table` — 30s HTMX poll
- Metrics from CloudWatch (batched GetMetricData — one API call for all endpoints)
- Lambda function list from `platform_api_endpoint_registry` DB table (static config)
- 30s poll guard: `[!document.querySelector('.drawer-open')]`

**Performance:**
- 68 endpoints × 5 metrics = 340 data points per refresh
- Batched into single CloudWatch GetMetricData call (max 500 metrics/call)
- Results cached Memcached 25s

---

### Section 5 — Endpoint Detail Drawer

**Purpose:** Deep-dive metrics, configuration, and history for a single endpoint.

**Drawer Width:** 640px
**Tabs:**

---

#### Tab 1 — Metrics

**Purpose:** Detailed time-series charts for the selected endpoint.

**Charts:**
- Latency chart: P50 · P95 · P99 lines — time range selector: 5m / 15m / 1h / 6h / 24h / 7d
- Request rate chart: invocations/min
- Error rate chart: 4xx (blue) + 5xx (red) stacked bars
- Cold start chart: cold start count per minute + cold start latency (InitDuration)
- Throttle events: 429 count per minute
- Concurrent executions: live concurrency vs reserved concurrency limit

**Controls:**
- Time range selector (shared across all charts in this tab)
- "Compare with last week" toggle (overlays same time window from 7 days ago)
- "Export as PNG" per chart
- "View raw metrics in CloudWatch" link

**Key stats summary bar (above charts):**
- Last 5 min: P99 · error rate · req/min · cold start rate
- Last 24h: peak P99 · peak req/min · total invocations · total errors

**Data Flow:**
- Charts: CloudWatch GetMetricData with `period` matching selected time range
- Time range "5m": period = 30s buckets
- Time range "24h": period = 5min buckets
- Time range "7d": period = 1h buckets

---

#### Tab 2 — Configuration

**Purpose:** View and edit SLA threshold, endpoint metadata, and deprecation status.

**Fields:**

| Field | Value | Editable |
|---|---|---|
| Endpoint Path | `/api/exams/{id}/submit/` | Read-only |
| Lambda Function | `exam-service-submit` | Read-only |
| HTTP Method | POST | Read-only |
| API Version | v2 | ✅ Admin/Backend/DevOps |
| SLA Group | Exam-critical | ✅ Admin/Backend/DevOps |
| SLA Threshold (P99 ms) | 200 | ✅ Admin/Backend/DevOps |
| Throttle Alert Threshold | 50 events/5min | ✅ Admin/Backend/DevOps |
| Cold Start Alert Threshold | 20/5min | ✅ Admin/Backend/DevOps |
| Description | Short description | ✅ Admin/Backend |
| Tags | Multi-select | ✅ Admin/Backend |
| Owner Team | Select (Backend/DevOps/AI) | ✅ Admin/Backend |
| Deprecation Status | Active / Deprecated / Sunset | ✅ Admin/Backend (see deprecation section) |
| Notes | Textarea (internal) | ✅ Admin/Backend |

**Save:** Inline save per section; SLA threshold change logged in audit

---

#### Tab 3 — Live Logs

**Purpose:** Tail CloudWatch log stream for this Lambda function in real-time.

**Display:**
- Last 50 log lines (auto-scrolling)
- Colour coding: ERROR lines in red · WARN in amber · INFO in default
- JSON log lines: expandable (click to expand pretty-printed JSON)
- Correlation ID filter: input field — enter a request correlation ID to filter log stream to a single request trace
- Log level filter: ALL · ERROR · WARN · INFO · DEBUG
- "Pause scroll" toggle (so admin can read logs without auto-scroll)
- "Download last 1,000 lines" button

**Data Flow:**
- Live logs via CloudWatch Logs `FilterLogEvents` API with tail pattern
- Polled every 5s via HTMX (active only when this tab is open — no background polling for logs)
- Max 50 lines in DOM; older lines removed as new ones arrive (virtual list)

**Edge Cases:**
- CloudWatch Logs Insights API rate limit: max 5 concurrent queries; if exceeded → "CloudWatch query limit reached. Try again in 5s."
- Very high log volume (exam day): sampling applied — 1 in 10 INFO lines shown; all ERROR lines shown

---

#### Tab 4 — Dependency Map

**Purpose:** Visual graph of which services this endpoint calls and which endpoints call this one.

**Display:**
- Directed graph (node = service, edge = call relationship)
- Current endpoint highlighted in blue
- Upstream callers (who calls this endpoint)
- Downstream dependencies (what this endpoint calls): DynamoDB · RDS · Memcached · S3 · external APIs (Razorpay · SES · FCM)
- Each downstream node: health badge (green/amber/red) based on current status
- Edge labels: avg latency of that call leg (from X-Ray tracing)

**Data Flow:**
- Dependency data from AWS X-Ray Service Map API
- Refreshed every 5 min (not real-time — X-Ray has 1-min processing delay)
- Health of downstream services from CloudWatch alarms

**Interaction:**
- Click a node in the graph → navigates to that service's detail drawer (if it's another API endpoint in the registry)
- Hover over edge → shows: P50/P99 latency · call count/min

---

### Section 6 — API Version Registry

**Purpose:** Manage the platform's API version lifecycle across v1/v2/v3.

**Layout:** Separate tab/section (accessible from page navigation)

**Version Overview Table:**

| Version | Status | Endpoints | Launch Date | Deprecation Date | Sunset Date | Notes |
|---|---|---|---|---|---|---|
| v1 | Deprecated ⚠ | 24 | Jan 2023 | Jan 2025 | Apr 2025 | Legacy mobile clients |
| v2 | Active ✅ | 52 | Jun 2024 | — | — | Current stable |
| v3 | Beta 🔵 | 12 | Mar 2026 | — | — | AI endpoints only |

**Per-version detail (expandable row or drawer):**
- Endpoints list with current usage (req/day) — sorted by highest usage (helps prioritise migration)
- Active clients still on this version: count from JWT `api_version` claim analytics
- Migration guide link (external documentation)

**Deprecation Workflow (for adding a new deprecation):**

Triggered by: "Mark as Deprecated" button on any endpoint in the Configuration tab

1. Set deprecation date (must be ≥ 30 days from today)
2. Set sunset date (must be ≥ deprecation date + 60 days; total minimum 90-day window)
3. Deprecation notice message (shown in API response `Deprecation` header)
4. Migration target version (which version replaces this)
5. Automated email notification: sent to all API clients registered via Webhook Event Catalog (Div B)
6. Deprecation banner added to endpoint row in table

**Sunset enforcement:**
- At sunset date: Celery task sets endpoint status → `sunset`
- Calls to sunset endpoint: return HTTP 410 Gone with body `{"error": "This endpoint has been sunset. Please migrate to v{n}."}`
- 7-day warning before sunset: email reminder to all remaining clients on deprecated version
- 1-day warning: PagerDuty alert to Backend team

**Edge Cases:**
- Attempt to sunset endpoint still receiving > 100 req/day: blocked with warning "This endpoint is still receiving {n} requests/day. Sunset blocked until usage drops below 100 req/day or force-sunset is explicitly confirmed."
- Force sunset override: 2FA required + reason field

---

### Section 7 — Deprecation Tracker Panel

**Purpose:** Summary view of all deprecation timelines across all API versions.

**Layout:** Right-side panel or dedicated tab

**Deprecation Timeline View:**

| Endpoint | Version | Deprecated Since | Sunset Date | Days Remaining | Current Usage (req/day) | Migration Status |
|---|---|---|---|---|---|---|
| `POST /api/exams/v1/submit/` | v1 | Jan 2025 | Apr 2025 | 21 days | 2,400 | 🔴 High usage — at risk |
| `GET /api/results/v1/{id}/` | v1 | Jan 2025 | Apr 2025 | 21 days | 180 | ⚠ Moderate usage |
| `POST /api/auth/v1/login/` | v1 | Jan 2025 | Apr 2025 | 21 days | 45 | ✅ Low — safe to sunset |

**Colour-coded days-remaining:**
- > 60 days: green
- 30–60 days: amber
- < 30 days: red
- < 7 days: red pulsing

**Actions per row:**
- "Send migration reminder" — sends email to all clients still using this endpoint
- "Extend sunset date" (Admin/Backend · 2FA required · reason mandatory)
- "Force sunset" (Admin only · 2FA · confirmation modal)

---

### Section 8 — Alert Rules Configuration

**Purpose:** Define per-endpoint alert thresholds; control when PagerDuty is triggered vs platform notification only.

**Alert Rules Table:**

| Rule Name | Endpoint Pattern | Metric | Threshold | Window | Action |
|---|---|---|---|---|---|
| Exam submit P99 breach | `*/exams/*/submit/` | P99 latency | > 200ms | 2 consecutive | PagerDuty P1 + C-18 auto-incident |
| High error rate | All endpoints | Error rate | > 5% | 1 min | PagerDuty P2 + admin notification |
| Cold start storm | All exam endpoints | Cold starts | > 200/5min | 5 min | PagerDuty P2 |
| Throttle spike | All | 429 count | > 100/5min | 5 min | Admin notification |
| Zero traffic | Exam-critical endpoints | Req/min | = 0 | 3 consecutive minutes | PagerDuty P1 (exam endpoints should never have zero traffic during exam hours) |

**Add/Edit Rule (Admin · Backend · DevOps):**
- Endpoint pattern (supports wildcards)
- Metric: P50 / P95 / P99 / Error Rate / Cold Starts / Throttles / Request Count
- Threshold value
- Window (1 min · 5 min · 15 min)
- Consecutive breach count before firing
- Action: Admin notification only · PagerDuty P3 · PagerDuty P2 · PagerDuty P1 + C-18 auto-incident
- Enabled/disabled toggle

**Data Flow:**
- Alert rules stored in `platform_api_alert_rules` DB table
- Celery beat task evaluates all active rules every 60s using CloudWatch batch query
- PagerDuty integration via Events API v2

---

## 5. User Flow

### Flow A — Investigating a Latency Spike During Exam

1. On-call DevOps receives PagerDuty alert: "Exam submit P99 = 380ms (SLA: 200ms)"
2. Opens `/engineering/api-health/`
3. SLA panel shows: exam submit P99 = 380ms (red pulsing)
4. Clicks exam submit row → drawer opens → Metrics tab
5. Chart shows latency spike started 4 min ago; cold start count also spiked
6. Navigates to Dependency Map tab: sees RDS query leg showing 250ms average
7. Determines: RDS replica lag causing slow reads
8. Opens C-08 Infrastructure Monitor in new tab → confirms replica lag = 8s
9. Acknowledges alert in C-18, applies fix (promote replica or route to primary for read)
10. SLA panel shows P99 returning to 140ms within 3 min

### Flow B — API Deprecation Planning

1. Backend Engineer decides to deprecate v1 exam endpoints
2. Opens API Health Monitor → Version Registry tab
3. Selects `POST /api/exams/v1/submit/` → "Mark as Deprecated"
4. Sets: deprecation date (today) · sunset date (+90 days) · migration target: v2
5. Types deprecation message: "Please migrate to POST /api/exams/v2/submit/ by {sunset date}"
6. System sends email to all clients registered via Webhook catalog
7. Deprecation Tracker panel now shows endpoint with 90-day countdown
8. At 7 days before sunset: Celery sends reminder emails
9. On sunset date: endpoint returns HTTP 410 Gone

### Flow C — Pre-Exam Provisioned Concurrency Review

1. Platform Admin opens API Health Monitor before exam day
2. SLA panel: all exam-critical endpoints currently healthy
3. Checks cold start rate on exam submit endpoint: 12 cold starts in last hour
4. Navigates to Configuration tab of exam submit endpoint
5. Notes current provisioned concurrency: 50 (set in C-10)
6. Clicks "View in Auto-scaling & Capacity Planner" deep-link → C-10
7. Increases provisioned concurrency to 150 for exam window

---

## 6. Component Structure (Logical)

```
APIHealthMonitorPage
├── PageHeader
│   ├── GlobalStatusBadge (large)
│   ├── EndpointCountBadge
│   ├── LastRefreshTimestamp
│   ├── AutoRefreshToggle
│   └── OpenIncidentButton
├── ExamDayModeBanner (conditional)
├── KPIStrip
│   └── KPICard × 6
├── ExamCriticalSLAPanel
│   ├── SLACard × 6 (one per exam-critical endpoint)
│   │   ├── P99Gauge
│   │   ├── Sparkline (30 min)
│   │   ├── InvocationRate
│   │   ├── ErrorRate
│   │   └── ColdStartRate
│   └── SLABreachBanner (conditional)
├── FilterBar
├── EndpointTable
│   ├── TableHeader (sortable)
│   └── EndpointRow × 68
│       ├── MethodBadge
│       ├── EndpointPath
│       ├── ServiceLabel
│       ├── VersionBadge
│       ├── StatusBadge
│       ├── LatencyColumns (P50/P95/P99)
│       ├── ErrorRateCell
│       ├── ReqPerMinCell
│       ├── ColdStartCell
│       └── SLAGroupBadge
├── EndpointDetailDrawer (640px)
│   ├── DrawerHeader
│   └── DrawerTabs
│       ├── MetricsTab (time-series charts)
│       ├── ConfigurationTab
│       ├── LiveLogsTab
│       └── DependencyMapTab
├── APIVersionRegistry (tab/section)
│   ├── VersionOverviewTable
│   └── DeprecationWorkflowModal
├── DeprecationTrackerPanel
└── AlertRulesSection
```

---

## 7. Data Model (High-Level)

### platform_api_endpoint_registry

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| endpoint_path | VARCHAR(255) | e.g., `/api/exams/{id}/submit/` |
| http_method | ENUM | GET/POST/PATCH/DELETE/PUT |
| lambda_function_name | VARCHAR(100) | |
| service_name | VARCHAR(50) | e.g., `exam-service` |
| api_version | VARCHAR(10) | v1/v2/v3 |
| sla_group | ENUM | exam_critical/standard/internal |
| sla_threshold_p99_ms | INTEGER | nullable |
| throttle_alert_threshold | INTEGER | per 5 min |
| cold_start_alert_threshold | INTEGER | per 5 min |
| deprecation_status | ENUM | active/deprecated/sunset |
| deprecated_at | DATE | nullable |
| sunset_at | DATE | nullable |
| deprecation_message | TEXT | nullable |
| migration_target_version | VARCHAR(10) | nullable |
| owner_team | VARCHAR(50) | |
| description | TEXT | nullable |
| tags | JSONB | array of strings |
| is_active | BOOLEAN | soft-disable without sunset |
| created_at | TIMESTAMPTZ | |
| updated_at | TIMESTAMPTZ | |

### platform_api_alert_rules

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| rule_name | VARCHAR(100) | |
| endpoint_pattern | VARCHAR(255) | supports wildcards |
| metric | ENUM | p99/p95/p50/error_rate/cold_starts/throttles/req_count |
| threshold | DECIMAL | |
| window_minutes | SMALLINT | |
| consecutive_breach_count | SMALLINT | |
| action | ENUM | notify/pagerduty_p3/pagerduty_p2/pagerduty_p1_incident |
| is_enabled | BOOLEAN | |
| created_by | UUID FK → platform_staff | |
| created_at | TIMESTAMPTZ | |

---

## 8. Validation Rules

| Field | Rule |
|---|---|
| SLA threshold | Exam-critical endpoints: minimum 50ms · maximum 5,000ms; cannot set exam submit threshold > 500ms (above this is not an SLA — it's just a very slow endpoint) |
| Deprecation date | Must be ≥ today + 30 days |
| Sunset date | Must be ≥ deprecation date + 60 days (total window ≥ 90 days from today) |
| Force sunset | Blocked if current usage > 100 req/day without explicit override |
| Alert rule threshold | Cannot set error rate alert threshold > 10% (too high — would never fire usefully) |
| Alert rule window | Minimum 1 minute · maximum 60 minutes |
| CloudWatch deep-link | Auto-generated from Lambda function name + AWS region; validated format only |
| Endpoint pattern (alert rule) | Must be valid glob pattern; validated before save |

---

## 9. Security Considerations

| Control | Implementation |
|---|---|
| CloudWatch data access | Lambda execution role has `cloudwatch:GetMetricData` read-only; no write to CloudWatch from this page |
| Live log tail permissions | `logs:FilterLogEvents` scoped to specific log group ARNs; cannot query log groups outside platform namespace |
| X-Ray data access | `xray:GetServiceGraph` and `xray:GetTraceSummaries` read-only; no write |
| Force sunset 2FA | Prevents accidental client breakage; logged with reason |
| Alert rule write access | Frontend Engineer and Security Engineer read-only; cannot create alert rules |
| Log data sensitivity | Live logs may contain request parameters; logs truncated at 2KB per line to prevent PII exposure in UI; sensitive patterns (JWT, passwords) masked by Lambda log middleware before writing to CloudWatch |
| Deprecation email send | Sent via SES; email list derived from platform_webhook_subscribers (internal); no user-supplied email lists |

---

## 10. Edge Cases (System-Level)

| Scenario | Handling |
|---|---|
| CloudWatch API throttling (>400 req/s) | Batched GetMetricData calls; Memcached 25s cache prevents repeat calls; if throttled: stale data shown with amber "Metrics delayed" indicator |
| All endpoints show zero traffic | Could be CloudWatch delay (1–2 min) or genuine outage; system checks Lambda invocation count from a different source (Lambda GetFunctionStatistics) as second opinion |
| New Lambda function deployed not in registry | Deployment pipeline (C-09) auto-registers new functions in `platform_api_endpoint_registry`; until registered, function not monitored — deployment hook ensures registration before traffic is routed |
| Exam in progress and SLA breach | Auto-creates C-18 incident with P0 severity; PagerDuty fires; Div B war room link included in incident; all on-call engineers paged simultaneously |
| Deprecated endpoint still receiving high traffic near sunset | Sunset auto-blocked; system escalates with daily email to Backend lead; admin must explicitly force-sunset or extend timeline |
| X-Ray service map unavailable | Dependency Map tab shows "Service map unavailable — X-Ray data not yet processed. Try again in 5 min." — does not affect main health monitoring |
| Cold start storm (> 500 cold starts in 5 min) | PagerDuty alert fires; C-10 auto-scaling page deep-link included in alert; provisioned concurrency auto-increase can be triggered from C-10 |
| Endpoint with zero SLA threshold configured | Treated as "no SLA set" — metrics still shown, P99 not colour-coded, no automated SLA breach alerts |

---

## 11. Performance & Scaling Strategy

| Concern | Strategy |
|---|---|
| 68 endpoints × 5 metrics per refresh | Single batched CloudWatch GetMetricData call (supports up to 500 metric queries per call); one API call per 30s refresh cycle |
| CloudWatch cost | GetMetricData: $0.01 per 1,000 metrics requested; at 340 metrics × 2 calls/min = 720 metrics/min → ~$0.43/day; acceptable |
| Live log tail | CloudWatch FilterLogEvents called only when Log tab is open; not polled in background |
| SLA panel faster refresh (15s/10s) | Separate Memcached cache key for exam-critical 6 endpoints; smaller payload; independent of full 68-endpoint refresh |
| Exam day mode | No additional infrastructure needed; same monitoring stack; poll interval change only |
| X-Ray data latency | X-Ray has ~1-min processing delay; Dependency Map is not real-time by design — acceptable for dependency visualisation |
| Table virtual scroll | 68 rows is small; no virtual scroll needed; all rows loaded at once |
| Alerts evaluation | Celery beat runs alert rule evaluation every 60s; 68 endpoints × N rules = single batched CloudWatch query; evaluation < 2s |
| Page load target | KPI + SLA panel: < 300ms (served from Memcached); full table: < 600ms (CloudWatch batch query + Memcached cache) |
