# C-11 — Database Admin Dashboard

> **Route:** `/engineering/database/`
> **Division:** C — Engineering
> **Primary Role:** Platform Admin (Role 10) · Database Administrator (Role 15)
> **Read Access:** Backend Engineer (Role 11) · DevOps/SRE (Role 14)
> **File:** `c-11-database.md`
> **Priority:** P0 — Required before first institution goes live
> **Status:** ⬜ Amendment pending — G5 (DB Configuration tab) · G20 (Manual VACUUM action) · G26 (Index Create/Drop actions)

---

## 1. Page Name & Route

**Page Name:** Database Admin Dashboard
**Route:** `/engineering/database/`
**Part-load routes:**
- `/engineering/database/?part=kpi` — database health KPI
- `/engineering/database/?part=slow-queries` — slow query log
- `/engineering/database/?part=connections` — connection monitor
- `/engineering/database/?part=schema-browser` — tenant schema browser
- `/engineering/database/?part=index-health` — index health report
- `/engineering/database/?part=vacuum-status` — autovacuum status
- `/engineering/database/?part=locks` — lock monitor
- `/engineering/database/?part=query-drawer&query_id={id}` — query explain drawer
- `/engineering/database/?part=replication` — replication lag panel

---

## 2. Purpose (Business Objective)

The Database Admin Dashboard is the DBA's primary workspace for maintaining the health and performance of all 2,051 PostgreSQL schemas (2,050 tenant schemas + 1 shared platform schema). Each schema is a fully independent data namespace serving potentially millions of rows; at platform scale, even a single poorly performing schema can cascade into global degraded performance through shared connection pools.

The DBA uses this page daily: triage slow queries, confirm autovacuum is running, ensure no lock storms are forming, and verify that replica lag is not affecting read-heavy workloads. Before any exam day, the DBA runs an index health check and verifies connection pool headroom.

**Business goals:**
- Zero database-induced exam failures through proactive health maintenance
- Slow query identification and EXPLAIN-plan analysis without direct psql access
- Index health enforcement across all 2,051 schemas
- Autovacuum monitoring to prevent table bloat and stat staleness
- Lock storm detection and manual resolution capability
- Replication lag monitoring (critical for read replica routing decisions)

---

## 3. User Roles

| Role | Access Level | Permissions |
|---|---|---|
| Platform Admin (10) | Level 5 | Full view + all write: kill query · force vacuum · kill lock · index rebuild |
| DBA (15) | Level 4 | Full view + all write actions |
| Backend Engineer (11) | Level 4 — Read | View slow queries + explain plans for own service's queries |
| DevOps / SRE (14) | Level 4 — Read | View connection counts + replication lag |

---

## 4. Section-Wise Detailed Breakdown

---

### Section 1 — Page Header & Database Health

**Purpose:** Instant PostgreSQL health verdict.

**Header elements:**
- H1 "Database Admin Dashboard"
- Global health badge: ✅ Healthy · ⚠ Degraded · 🚨 Critical
- Instance selector: Primary · Replica-1 · Replica-2 (applies to relevant sections)
- PostgreSQL version: "PostgreSQL 15.4"
- RDS instance class: "db.r6g.2xlarge"
- "Run Index Health Check (All Schemas)" button (DBA/Admin · long-running job · progress shown)
- Last schema scan: "Last index health scan: 2 hours ago"

---

### Section 2 — KPI Strip

**KPI Cards:**

| Card | Metric | Alert |
|---|---|---|
| Slow Queries (> 1s) | Count in last 15 min | > 10 amber · > 50 red |
| Active Connections | Primary connections in use | > 80% max_connections = amber |
| Replication Lag (max) | Highest lag across all replicas | > 2s amber · > 10s red |
| Long-Running Locks | Locks held > 30s | > 0 = amber |
| Vacuum Needed | Tables with > 20% dead tuple ratio | > 5 = amber |
| Index Bloat | Indexes with > 50% bloat ratio | > 10 = amber |

---

### Section 3 — Slow Query Log

**Purpose:** Surface all queries taking > 1s (configurable threshold) for performance investigation.

**Threshold controls:**
- Current threshold: 1s (configurable: 100ms / 500ms / 1s / 5s / 10s)
- Auto-reset: threshold applies to `pg_stat_statements.calls` where mean duration > threshold

**Slow Queries Table:**

| Column | Description | Sortable |
|---|---|---|
| Duration (P99) | Worst-case duration in last 1h | ✅ |
| Duration (Mean) | Mean duration | ✅ |
| Call Count | How many times executed (last 1h) | ✅ |
| Query Preview | First 120 chars of query (parameters replaced with $1, $2) | — |
| Schema | Tenant schema name (or `platform_shared`) | ✅ |
| Wait Events | Most common wait event type | — |
| Total Time (cumulative) | Duration × calls | ✅ |
| First Seen | When this query pattern first appeared | ✅ |
| Service | Inferred from application name (Django ORM tag) | — |

**Click row → opens Query Detail Drawer (db-query-drawer)**

**Filter bar:**
- Schema filter: All / Specific schema search
- Duration filter: > 100ms / > 500ms / > 1s / > 5s / > 10s
- Service filter: exam-service / auth-service / result-service / etc.
- Wait event filter: all / Lock / IO / CPU

**Top 10 by total time:** Separate card above table — the queries consuming the most DB resources (not necessarily the slowest per call, but high call frequency × moderate duration = highest total load)

**Data Flow:**
- Source: `pg_stat_statements` extension on primary RDS instance
- Queried via `psycopg2` from DBA service Lambda (internal only, not public API)
- Results cached Memcached 2 min per threshold setting
- 60s HTMX poll when slow query tab is active

---

### Section 4 — Query Detail Drawer (db-query-drawer)

**Purpose:** Full analysis of a specific slow query pattern.

**Drawer Width:** 640px
**Tabs:**

---

#### Tab 1 — Explain Plan

**Purpose:** Visual query execution plan for the selected query.

**Explain Plan Display:**
- Full `EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)` output rendered as human-readable tree
- Node types colour-coded: Seq Scan (red — likely missing index) · Index Scan (green) · Hash Join (amber) · Nested Loop (amber)
- Each node shows: rows estimated vs actual · loops · exclusive time · inclusive time · cost
- "Expensive node" detection: nodes consuming > 50% of total query time highlighted

**Query normalised text:**
- Full query shown with $1/$2 parameter placeholders
- Syntax highlighted

**Actions:**
- "Add suggested index" — system suggests index based on WHERE/JOIN columns in the plan; DBA can review and apply via `CREATE INDEX CONCURRENTLY` (Celery job — non-blocking)
- "Copy to clipboard" — copies EXPLAIN output for sharing

**Historical trend:**
- Chart: mean duration of this query pattern over last 7 days (1h buckets)
- Helps identify if degradation is recent (new data volume) or chronic

---

#### Tab 2 — Index Suggestions

**Purpose:** Automated index recommendations for this query pattern.

**Suggestions (generated by hypopg extension or pg_idx_advisor):**

| Column(s) | Table | Index Type | Estimated Benefit | Action |
|---|---|---|---|---|
| `(student_id, exam_id)` | `exam_answers` | B-tree | 94% faster (7s → 0.4s) | Apply Index |
| `(created_at)` | `exam_submissions` | B-tree | 45% faster | Apply Index |

**"Apply Index" action:**
- Runs `CREATE INDEX CONCURRENTLY idx_exam_answers_student_exam ON tenant_{id}.exam_answers(student_id, exam_id)`
- Runs concurrently — does not lock table; safe for production
- Progress bar shown (can take 5–30 min for large tables)
- Celery job; DBA notified on completion

**Cross-schema application:**
- For multi-tenant schemas: "Apply to: This schema only / All 2,050 tenant schemas"
- If all schemas: Celery job applies index to each schema sequentially; progress: "{n}/2,050 schemas done"

---

#### Tab 3 — Historical Trend

**Purpose:** How this query's performance has changed over time.

**Chart:** P50 · P95 · P99 latency per hour — last 7 days
**Overlay:** Schema data size growth (from `pg_total_relation_size`) — helps identify if slowdown correlates with data growth

---

### Section 5 — Connection Monitor

**Purpose:** Real-time visibility into PostgreSQL connections across all pools and schemas.

**PgBouncer Pool Summary:**

| Pool | Mode | Max Server Conn | Active Server | Idle Server | Client Conn | Queue | Status |
|---|---|---|---|---|---|---|---|
| Primary | Transaction | 300 | 248 | 52 | 1,840 | 0 | ✅ OK |
| Replica-1 | Transaction | 200 | 118 | 82 | 920 | 0 | ✅ OK |
| Replica-2 | Transaction | 200 | 134 | 66 | 1,020 | 12 | ⚠ Queue |

**Per-schema connection counts:**
- Top 20 schemas by connection count (from `pg_stat_activity` grouped by `search_path`)
- Shows: schema name · active connections · idle connections · idle-in-transaction connections
- Idle-in-transaction alert: any schema with idle-in-transaction > 5 min → amber highlight (connection holding transaction open = block risk)

**Connection type breakdown (primary):**
- Active (executing query): {n}
- Idle: {n}
- Idle in transaction: {n}
- Waiting for lock: {n} (alert if > 10)

**Write Actions (DBA/Admin):**
- "Terminate idle connections (> 30 min)" → `SELECT pg_terminate_backend(pid) WHERE state = 'idle' AND state_change < now() - interval '30 min'`
- "Terminate idle-in-transaction (> 5 min)" → targets `idle in transaction` state
- 2FA required for bulk termination (affects all tenants)
- Per-connection "Kill" button for individual connections in the per-schema table

**Connection limit display:**
- `max_connections` setting on primary: 5,000
- PgBouncer server connection ceiling (set in pgbouncer.ini): 300
- Effective ceiling: PgBouncer server connections (300) — PostgreSQL max_connections is not the actual limit since all traffic goes through PgBouncer

---

### Section 6 — Tenant Schema Browser

**Purpose:** Tenant-by-tenant schema health overview for DBA investigations.

**Table:**

| Schema | Tenant Name | Tables | Total Size | Largest Table | Last Migration | Pending Migrations | Status |
|---|---|---|---|---|---|---|---|
| tenant_001_vibrant | Vibrant Academy | 48 | 12.4 GB | exam_answers (8.2 GB) | 20260315_001 | 0 | ✅ |
| tenant_002_alpha | Alpha Coaching | 48 | 8.1 GB | exam_submissions | 20260315_001 | 0 | ✅ |
| tenant_042_sunrise | Sunrise Academy | 48 | 3.2 GB | student_profiles | 20260314_003 | 1 | ⚠ |

**Click row → opens tenant schema detail panel:**
- Table list with sizes (sorted by largest)
- Index list with health (used / unused / bloated)
- Autovacuum status per table
- Link to Tenant Manager (C-01) for business context

**Filters:**
- Search schema/tenant name
- Status: All / Pending migrations / Index issues / Large schemas (> 5 GB)
- Sort: Size · Tenant name · Last migration date

**Data Flow:**
- Schema sizes: `pg_total_relation_size(schemaname)` across all 2,051 schemas
- Expensive query — run as Celery job every 2h; results cached in `platform_schema_stats` table
- Pending migrations: from C-12 migrations registry
- Last refresh timestamp shown: "Schema stats last refreshed: 1h 43m ago"

---

### Section 7 — Index Health Report

**Purpose:** Identify indexes that are unused, missing, or bloated across all 2,051 schemas.

**Triggered by:** "Run Index Health Check" button (long-running Celery job · 15–30 min for all schemas)

**Report Summary (from last scan):**

| Category | Count | Action |
|---|---|---|
| Missing indexes (identified from slow query analysis) | 12 | Review and create |
| Unused indexes (not used in last 30 days) | 84 | Review and drop (saves space + write overhead) |
| Bloated indexes (bloat > 50%) | 28 | Rebuild with REINDEX CONCURRENTLY |
| Duplicate indexes (same columns covered twice) | 6 | Drop duplicates |

**Details table per category:**

For each index issue:
| Schema | Table | Index Name | Issue | Estimated Benefit | Recommended Action |
|---|---|---|---|---|---|
| tenant_042_sunrise | exam_answers | idx_exam_ans_old | Unused (0 scans in 30d) | Drop saves 240 MB | Drop Index |
| tenant_001_vibrant | student_profiles | idx_students_name | Bloat 73% | Faster reads | REINDEX CONCURRENTLY |

**Bulk actions:**
- "Drop all unused indexes" → confirmation modal listing all 84 indexes → Celery batch job (CONCURRENT drops)
- "Rebuild all bloated indexes" → Celery batch job (REINDEX CONCURRENTLY — non-blocking)
- Individual actions per row

**Note on cross-schema operations:**
- Operations applied to 1 schema are instant (seconds)
- Operations applied to all 2,051 schemas: Celery job with progress bar "{n}/2,051 schemas done"
- DBA notified by email on completion

---

### Section 8 — Autovacuum Status

**Purpose:** Verify autovacuum is keeping tables healthy (preventing bloat and stat staleness).

**Tables Needing Attention (sorted by dead tuple ratio):**

| Schema | Table | Live Tuples | Dead Tuples | Dead Ratio | Last Vacuum | Last Autovacuum | Autovacuum Enabled | Action |
|---|---|---|---|---|---|---|---|---|
| tenant_001_vibrant | exam_answers | 48M | 12M | 25% | 3 days ago | 6h ago | ✅ | Force Vacuum |
| platform_shared | platform_audit_log | 2.1M | 480K | 23% | 4 days ago | 12h ago | ✅ | Force Vacuum |

**Alert threshold:** Tables with dead tuple ratio > 20% shown in this list (amber: 20–35%, red: > 35%)

**Autovacuum configuration display:**
- `autovacuum_vacuum_threshold`: 50 (default)
- `autovacuum_vacuum_scale_factor`: 0.2 (20% of table size before auto-vacuum triggers)
- `autovacuum_max_workers`: 3 (shared across all schemas)
- "With 2,051 schemas, autovacuum workers may not keep pace during high write periods. Consider increasing `autovacuum_max_workers` during peak exam windows."

**Write Actions (DBA/Admin):**
- "Force VACUUM ANALYZE" per table → `VACUUM ANALYZE schema.table` → Celery job (runs during low-traffic window if not emergency)
- "Force VACUUM FULL" per table → ⚠ requires table lock (blocks all reads/writes) → 2FA required · confirmation "This will lock {table} for an estimated {n} minutes. Are you exam windows clear?"

**Autovacuum worker activity (live):**
- Current autovacuum workers: {n}/3 active
- Each active worker: schema · table · phase (heap/index · elapsed time)

---

### Section 9 — Lock Monitor

**Purpose:** Detect and resolve lock contention before it cascades into a lock storm.

**Active Locks Table:**

| Locked Object | Lock Type | Granted | Waiting PID | Holding PID | Wait Duration | Blocking Query (snippet) |
|---|---|---|---|---|---|---|
| tenant_042.exam_submissions | RowExclusiveLock | ❌ Waiting | PID 84210 | PID 84198 | 1m 24s | `UPDATE exam_submissions SET...` |
| tenant_001.student_profiles | ShareLock | ❌ Waiting | PID 84315 | PID 84302 | 0m 12s | `ALTER TABLE student_profiles...` |

**Alert:** Any lock held > 30s → amber highlight; > 5 min → red highlight + auto-notification to DBA

**Lock graph (visualisation):**
- Directed graph: nodes = PIDs · edges = "waiting for" relationships
- Deadlock detection: if cycle exists in graph → red banner "Deadlock detected"

**Write Actions (DBA/Admin):**
- "Kill holding process" per row → `SELECT pg_terminate_backend({pid})`
- 2FA required if the PID is actively executing (not idle)
- Confirmation: "Killing PID {pid} will rollback its transaction. The tenant {n} may see a brief error. Confirm?"

**Lock history:** Last 24h of resolved locks (held > 30s) with resolution time and method

---

### Section 10 — Replication Lag Panel

**Purpose:** Monitor primary-to-replica replication lag for the two read replicas.

**Replication Status:**

| Replica | LSN Lag | Time Lag | Replication Slot | Wal Receiver Status | Status |
|---|---|---|---|---|---|
| rds-replica-1 | 0 bytes | 0.3s | Active | Streaming | ✅ OK |
| rds-replica-2 | 128 MB | 4.2s | Active | Streaming | ⚠ Lag |

**Lag trend chart:**
- Line chart: replication lag (seconds) for each replica over last 2 hours
- Alerts on chart when lag crossed threshold

**Write lag vs replay lag distinction:**
- Write lag: time for primary to write WAL segment
- Replay lag: time for replica to apply WAL to data files
- Both shown separately (replay lag is what matters for query freshness)

**Alert thresholds:**
- > 2s: amber notification
- > 10s: red notification + API health monitor (C-04) alerted to stop routing reads to lagged replica
- > 30s: auto-creates C-18 incident

**Actions:**
- "Pause replication slot" → temporarily pauses streaming (used before large schema operations); 2FA required; auto-resumes after 4h
- "Drop replication slot" → Admin only · 2FA · "This will cause the standby to require a full resync. Data at risk." confirmation

---

## 5. User Flow

### Flow A — Pre-Exam Database Health Check

1. DBA opens `/engineering/database/` morning before major exam
2. KPI strip: all green except "Slow Queries (> 1s): 14" — amber
3. Navigates to Slow Query Log → top 3 slow queries
4. Click on slowest query (P99: 8.4s) → Query Drawer → Explain Plan
5. Explain Plan shows: Seq Scan on `exam_answers` table (12M rows)
6. Index Suggestions tab: "Add index (student_id, exam_id) → estimated 94% improvement"
7. Clicks "Apply to all schemas" → Celery job starts (2,050 schemas)
8. After 25 min: index applied; slow query P99 drops to 0.3s
9. Autovacuum status: 2 tables with dead ratio > 25% → force VACUUM ANALYZE on both
10. Lock Monitor: clean (no active waits) → exam day ready

### Flow B — Lock Storm During Exam

1. C-18 incident created: "Exam submissions stalling — database issue suspected"
2. DBA opens Database Admin Dashboard → Lock Monitor
3. Lock graph shows: 42 PIDs waiting on PID 84199 (holding lock for 3 min)
4. Holding query: `ALTER TABLE exam_answers ADD COLUMN correction_notes TEXT`
5. DBA: schema migration was accidentally run during exam window (C-12 issue)
6. DBA kills PID 84199 → all 42 waiting PIDs proceed
7. Exam submissions recover within 30s
8. DBA adds lock-during-exam detection to schema migration safeguards in C-12

### Flow C — Index Health Audit (Weekly)

1. DBA clicks "Run Index Health Check (All Schemas)"
2. Celery job runs for 22 min (2,051 schemas)
3. Report: 84 unused indexes · 28 bloated indexes
4. DBA reviews unused indexes list — confirms 80 are safe to drop
5. Clicks "Drop all unused indexes" → selects 80 of 84 (excludes 4 that are recent and may just not have been used yet)
6. Celery batch drop job: 80 indexes × 2,050 schemas = ~164,000 DROP INDEX CONCURRENTLY operations
7. Job runs over 3 hours (off-peak, scheduled for 02:00)
8. Space reclaimed: 18 GB across all schemas

---

## 6. Component Structure (Logical)

```
DatabaseAdminDashboardPage
├── PageHeader
│   ├── PageTitle
│   ├── GlobalHealthBadge
│   ├── InstanceSelector (Primary/Replica-1/Replica-2)
│   ├── RunIndexHealthCheckButton
│   └── LastScanTimestamp
├── KPIStrip × 6
├── SlowQueryLog
│   ├── ThresholdControl
│   ├── Top10ByTotalTime (summary cards)
│   └── SlowQueryTable (sortable + filterable)
├── QueryDetailDrawer (640px)
│   └── DrawerTabs
│       ├── ExplainPlanTab (tree + node colours)
│       ├── IndexSuggestionsTab
│       └── HistoricalTrendTab
├── ConnectionMonitor
│   ├── PgBouncerPoolTable
│   ├── PerSchemaConnectionTable
│   ├── ConnectionBreakdownSummary
│   └── WriteActions (bulk terminate)
├── TenantSchemaBrowser
│   ├── SearchFilterBar
│   └── SchemaTable (+ inline detail panel)
├── IndexHealthReport
│   ├── ReportSummaryCards × 4
│   └── IndexIssueTable (per category tab)
├── AutovacuumStatus
│   ├── ConfigDisplay
│   ├── TablesNeedingAttention
│   └── ActiveWorkerDisplay
├── LockMonitor
│   ├── ActiveLocksTable
│   ├── LockGraph (directed)
│   └── LockHistory
└── ReplicationLagPanel
    ├── ReplicaStatusTable
    ├── LagTrendChart
    └── ReplicationActions
```

---

## 7. Data Model (High-Level)

### platform_schema_stats (cached schema metadata)

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| schema_name | VARCHAR(80) | |
| tenant_id | UUID FK → platform_tenants | |
| total_size_bytes | BIGINT | from pg_total_relation_size |
| table_count | SMALLINT | |
| row_estimate | BIGINT | from pg_stat_user_tables |
| index_health_status | ENUM | clean/issues/scan_needed |
| pending_migrations | SMALLINT | from C-12 |
| last_migration | VARCHAR(100) | |
| scanned_at | TIMESTAMPTZ | |

### platform_index_health_reports

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| scan_started_at | TIMESTAMPTZ | |
| scan_completed_at | TIMESTAMPTZ | nullable |
| scan_status | ENUM | running/completed/failed |
| run_by | UUID FK → platform_staff | |
| missing_indexes | JSONB | array of {schema, table, columns, estimated_benefit} |
| unused_indexes | JSONB | array of {schema, table, index_name, last_used} |
| bloated_indexes | JSONB | array of {schema, table, index_name, bloat_pct} |
| duplicate_indexes | JSONB | array of {schema, table, index_names} |
| total_schemas_scanned | INTEGER | |

---

## 8. Validation Rules

| Rule | Detail |
|---|---|
| Force VACUUM FULL | Requires 2FA · must confirm exam windows are clear · blocked if active exam in progress (`platform:active_exam_count > 0`) |
| Kill connection PID | 2FA required for active executing connections (idle connections: no 2FA) |
| Drop index | Cannot drop indexes on tables with active write transactions > 10/sec (risk of making write performance worse during drop operation) |
| Add index via suggestion | "Apply to all schemas" capped at 2,051 schemas; Celery job must run during off-peak window (02:00–05:00 IST) by default; override available with confirmation |
| Index health scan | Cannot run during active exam period; blocked with "Exam in progress — health scans deferred" |
| Slow query threshold | Minimum: 100ms · Maximum: 60s (lower values produce too much noise) |
| Replication slot pause | Auto-resumes after 4h maximum; cannot be manually held beyond 4h without re-pausing (prevents WAL accumulation) |

---

## 9. Security Considerations

| Control | Detail |
|---|---|
| DB access | All queries executed via dedicated DBA-service Lambda with `SELECT` on `pg_stat_statements`, `pg_stat_activity`, `pg_locks`, `information_schema`; DDL executed via separate migration Lambda role |
| EXPLAIN ANALYZE | Runs against a separate read replica (not primary) to avoid performance impact; actual row counts from replica may differ slightly from primary |
| Query text display | Query parameters replaced with $1/$2 in all displays — no actual parameter values shown (could contain PII) |
| Kill connection | Logged in `platform_infra_events` with PID + tenant + actor + reason |
| Index creation | `CREATE INDEX CONCURRENTLY` used exclusively — never blocking `CREATE INDEX`; guarded by application layer |
| Cross-schema operations | DBA role has access to all schemas; all cross-schema queries logged in audit log |
| `pg_terminate_backend` | Backed by IAM-scoped RDS Data API; DBA Lambda can only terminate connections from the platform's application user, not RDS admin |

---

## 10. Edge Cases (System-Level)

| Scenario | Handling |
|---|---|
| `pg_stat_statements` not enabled | Error shown: "pg_stat_statements not available. Slow query log cannot be displayed. Contact DevOps to enable extension." |
| Schema browser scan fails on specific schema | Partial results shown; failed schema marked with error icon; DBA can click "Re-scan schema" |
| Index create CONCURRENTLY fails midway | Leaves an invalid index in `pg_indexes` with `indisvalid = false`; system detects this in next health scan and flags as "Invalid index — requires cleanup" |
| Large table VACUUM FULL during off-hours | Lock can last 2–8 hours for 10GB+ tables; DBA reminded to schedule during confirmed maintenance window |
| Replica falls too far behind (> 100 MB WAL lag) | Auto-pause replication slot is suggested (pausing stops WAL from being deleted); without this, RDS storage fills with WAL; DBA notified |
| New tenant schema not yet in schema browser | Celery scan runs every 2h; newly provisioned schemas appear within 2h; "Force re-scan" button available for DBA |
| Lock graph deadlock cycle | System automatically detects cycle in the waiting-for graph and highlights it in red; "Break deadlock" button terminates the youngest transaction in the cycle |

---

## 11. Performance & Scaling Strategy

| Concern | Strategy |
|---|---|
| pg_stat_statements query | Single query on primary; results cached Memcached 2 min; at 2,051 schemas × 50+ tables each, stat_statements can have thousands of rows — limited to top-500 by mean duration for display |
| Schema browser (2,051 schemas) | Pre-computed by Celery every 2h; stored in `platform_schema_stats` table; page query: < 50ms against this table |
| Index health scan (2,051 schemas) | Celery job with progress tracking; runs exclusively at off-peak (configured 02:00–05:00); skips active tenant schemas with high write load |
| Connection monitor live data | `pg_stat_activity` query runs every 30s; targeted query (only columns needed, not `*`); cached 25s in Memcached |
| Lock monitor | `pg_locks` joined with `pg_stat_activity`; fast query (locks table is always small); 15s poll when lock monitor tab is open |
| Replication lag | CloudWatch RDS `ReplicaLag` metric (30s granularity); supplemented by direct `pg_stat_replication` query for byte-level precision |
| Autovacuum status | `pg_stat_user_tables` grouped by dead tuple ratio; one query per instance; cached 5 min |

---

## Amendment — G5: DB Configuration Tab

**Gap addressed:** DBA could monitor but not change RDS parameter groups (work_mem, max_connections, autovacuum settings) or PgBouncer pool sizes from the portal.

### New Top-Level Tab — DB Configuration

**Access:** `/engineering/database/?tab=db-config`

**Section A — RDS Parameter Group Editor:**

| Parameter | Current Value | Pending Value | Requires Restart | Editable By |
|---|---|---|---|---|
| `work_mem` | 4MB | — | No | DBA + Admin |
| `shared_buffers` | 25% of RAM | — | Yes | Admin only |
| `max_connections` | 500 | — | Yes | Admin only |
| `autovacuum_vacuum_scale_factor` | 0.05 | — | No | DBA + Admin |
| `checkpoint_completion_target` | 0.9 | — | No | DBA + Admin |
| `effective_cache_size` | 75% of RAM | — | No | DBA + Admin |
| `random_page_cost` | 1.1 | — | No | DBA + Admin |

**Edit flow:** Inline edit per row → "Apply" button → if `Requires Restart = Yes`: 2FA required + confirmation "This change requires an RDS reboot. All connections will be dropped for ~60s during reboot. Confirm?" → queued as Celery job → calls AWS RDS `ModifyDBParameterGroup` API. **Non-restart changes:** Applied immediately via `ModifyDBParameterGroup` with `ApplyMethod: immediate`.

**"Pending Reboot" indicator:** If any restart-required changes are pending but not yet applied: amber banner "2 parameter changes pending RDS reboot. Schedule during maintenance window."

**Section B — PgBouncer Configuration Editor:**

| Setting | Current Value | Description | Editable By |
|---|---|---|---|
| `pool_size` (default per DB) | 10 | Max server connections per pool | DBA + Admin |
| `max_client_conn` | 10,000 | Maximum client connections to PgBouncer | Admin only |
| `pool_mode` | transaction | Pooling mode: transaction/session/statement | Admin only (requires PgBouncer restart) |
| `server_idle_timeout` | 600s | Seconds before idle server connection closed | DBA + Admin |
| `query_timeout` | 0 (disabled) | Max query duration before disconnect | DBA + Admin |

**Per-tenant pool override:** Table showing all 2,050 tenant schemas with their individual `pool_size` override (if any). "Add override" → tenant selector + pool_size value → saves to PgBouncer config.

**"Reload PgBouncer config" button (DBA + Admin · no 2FA):** Sends SIGHUP to PgBouncer process (ECS task signal) → reloads config without dropping connections.

**Section C — PostgreSQL Role/Grant Manager:**

Read-only tree showing grant hierarchy per tenant schema. Actions:
- "Grant read-only role to {staff}" → creates `GRANT SELECT ON ALL TABLES IN SCHEMA tenant_{id} TO {role}` — 2FA required
- "Revoke access from {role}" — 2FA required
- "Create reporting user" → generates read-only DB user with scoped schema access

All DDL logged in `platform_dba_audit_log` table.

---

## Amendment — G20: Manual VACUUM ANALYZE Action

**Gap addressed:** DBA could see autovacuum status per table but could not trigger a manual VACUUM ANALYZE from the portal. Had to SSH directly into RDS, creating an audit gap and access control risk.

### Context Menu Action — Manual VACUUM on Table Row

**Trigger:** Right-click or ⋮ menu on any table row in the autovacuum status view → "Trigger VACUUM ANALYZE"

**Confirmation Modal:**
- Table name (full schema-qualified)
- Estimated duration: based on last vacuum duration for this table + current dead tuple count
- Last autovacuum: timestamp of last autovacuum run
- Dead tuples: current dead tuple count (from `pg_stat_user_tables.n_dead_tup`)
- Warning if table is > 1GB: "Large table. VACUUM may run 30–90 min. PostgreSQL will continue serving reads/writes during VACUUM (no table lock)."
- "Confirm VACUUM ANALYZE" button (DBA + Admin · no 2FA for VACUUM — it's a maintenance operation)

**Execution:**
- Celery task: connects to RDS via dedicated DBA superuser role (fetched from AWS Secrets Manager at task runtime) using a direct connection (bypasses PgBouncer — VACUUM must run on dedicated connection)
- Executes: `VACUUM (ANALYZE, VERBOSE) schema_name.table_name`
- Progress: `pg_stat_progress_vacuum` polled every 5s → HTMX push to `vacuum-progress-drawer` showing:
  - Phase: scanning / vacuuming / index cleanup / heap cleanup
  - Heap blks total / scanned / vacuumed (% complete)
  - Rows removed / dead tuples removed
- On completion: result summary (rows processed · dead tuples removed · index pages reclaimed · duration) logged to `platform_dba_audit_log`

**Schema-wide VACUUM (Platform Admin only · 2FA required):**
Available from the Schema tab header: "VACUUM all tables in this schema" → runs VACUUM ANALYZE on all tables sequentially in a single Celery job.

---

## Amendment — G26: Index Create/Drop Actions

**Gap addressed:** DBA could not create or drop indexes from the portal. Had to access RDS directly, bypassing audit controls.

### Context Menu Actions — Index Management on Index Health Table Row

**Trigger A — Create Index (from table context menu):**

**Index Create Drawer (index-action-drawer · 480px):**
- Table selector (pre-filled from context menu row)
- Column(s) multi-select (from schema introspection of that table's columns)
- Index type: btree (default) · hash · gin (for JSONB/array) · gist (for geometric/full-text) · brin (for large time-series)
- Optional partial WHERE condition: text input (e.g., `WHERE status = 'active'`)
- Index name: auto-suggested (`idx_{table}_{columns}`) + editable
- Concurrency: always `CREATE INDEX CONCURRENTLY` (no table lock) — not configurable
- Estimated build time: computed from table row count × pg_stats estimate (shown before confirm)
- Estimated size: computed from column data types × row count × fill factor
- "Create Index" button (DBA + Admin · 2FA required for production indexes)

**Execution:**
- Celery task: executes `CREATE INDEX CONCURRENTLY {name} ON {schema}.{table} ({columns}) WHERE {condition}` via DBA superuser role
- Progress: polled every 10s from `pg_stat_progress_create_index` → HTMX push showing: phase · blocks done / total · tuples done
- On completion: success toast + `platform_dba_audit_log` entry (DDL statement · actor · duration · index size)

**Trigger B — Drop Index (from index health table context menu · red trash icon):**

**Index Drop Confirmation Modal:**
- Index name (full schema-qualified)
- Index size on disk
- Last used timestamp (from `pg_stat_user_indexes.idx_scan` last scan time)
- Warning if last used < 7 days: amber "This index was used recently. Dropping may cause query slowdowns."
- Warning if index is a PRIMARY KEY or UNIQUE constraint: "Cannot drop constraint index via this action. Use ALTER TABLE instead."
- Confirmation: must type index name to confirm
- 2FA required
- Executes: `DROP INDEX CONCURRENTLY {schema}.{index_name}` (concurrent drop available in PG 12+)

**REINDEX Action (from ⋮ menu on bloated indexes):**
- "REINDEX index" → `REINDEX INDEX CONCURRENTLY {schema}.{index_name}` — rebuilds index without dropping it; use for bloated/corrupted indexes
- No confirmation required (read-heavy safe operation) · DBA + Admin · logged in audit table

**All DDL logged in platform_dba_audit_log:**

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| schema_name | VARCHAR(80) | |
| table_name | VARCHAR(100) | |
| ddl_statement | TEXT | full SQL |
| operation | ENUM | create_index / drop_index / reindex / vacuum / vacuum_analyze / grant / revoke / param_change |
| actor_id | UUID FK → platform_staff | |
| celery_task_id | VARCHAR(255) | |
| duration_seconds | FLOAT | nullable |
| result_summary | JSONB | nullable |
| created_at | TIMESTAMPTZ | |
