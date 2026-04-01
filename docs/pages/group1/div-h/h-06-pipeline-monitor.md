# H-06 — Data Pipeline Monitor

> **Route:** `/analytics/pipelines/`
> **Division:** H — Data & Analytics
> **Primary Role:** Data Engineer (43) — full operational control
> **Supporting Roles:** Analytics Manager (42) — read-only monitoring; Platform Admin (10) — full
> **File:** `h-06-pipeline-monitor.md`
> **Priority:** P0 — if pipelines fail, all analytics pages serve stale data; Data Engineer must diagnose and recover same morning

---

## 1. Page Name & Route

**Page Name:** Data Pipeline Monitor
**Route:** `/analytics/pipelines/`
**Part-load routes:**
- `/analytics/pipelines/?part=health-overview` — pipeline health cards
- `/analytics/pipelines/?part=run-history` — execution history table
- `/analytics/pipelines/?part=data-freshness` — data freshness dashboard
- `/analytics/pipelines/?part=warehouse-explorer` — SQL explorer section
- `/analytics/pipelines/{job_name}/?part=job-detail` — job detail drawer

---

## 2. Purpose

H-06 is the **Data Engineer's workspace**. All analytics pages in Division H depend on nightly Celery aggregation jobs that scan 2,050 tenant schemas and write pre-computed metrics to the analytics schema. When any of these jobs fail:

- H-01 shows stale data (pipeline health strip goes red)
- H-02 through H-05 show outdated metrics
- H-08 generates reports from stale data
- Institution reports may be delivered with wrong numbers

H-06 gives the Data Engineer:
1. Immediate visibility into which pipelines failed and why
2. Tools to investigate root causes (logs, tenant failure breakdown)
3. Manual re-run capability for any failed or stale job
4. Data freshness gauges per analytics table
5. A read-only SQL explorer against the analytics schema for ad-hoc investigations

**Who needs this page:**
- Data Engineer (43) — primary operational user; full control
- Analytics Manager (42) — morning status check; escalation awareness

---

## 3. Layout

```
┌────────────────────────────────────────────────────────────────────┐
│  Page header: "Data Pipeline Monitor"   [Run All Pipelines Now]   │
│  Overall status: ✅ All 8 pipelines healthy · Last run: 01:47 IST │
├──────────────────────────────────────────────────────────────────┤
│  Pipeline Health Cards (one card per Celery task)                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │ Daily Metrics│  │ Question Stats│  │ Inst. Engage │           │
│  │ ✅ SUCCESS   │  │ ⚠ PARTIAL    │  │ ✅ SUCCESS   │           │
│  │ 01:47 IST    │  │ 02:31 IST    │  │ Sun 03:14    │           │
│  │ 4,102 tenants│  │ 2.1M Q's     │  │ 2,050 inst.  │           │
│  │ [View Runs]  │  │ [View Runs]  │  │ [View Runs]  │           │
│  └──────────────┘  └──────────────┘  └──────────────┘           │
├──────────────────────────────────────────────────────────────────┤
│  Run History Table (server-side paginated, 25 rows)              │
├──────────────────────────────────────────────────────────────────┤
│  Data Freshness Dashboard  │  Warehouse SQL Explorer             │
└────────────────────────────┴───────────────────────────────────┘
```

---

## 4. Section-Wise Detailed Breakdown

---

### Section A — Overall Status Banner

Single-line banner at top of page (below header).

| State | Display |
|---|---|
| All pipelines healthy | `✅ All 8 pipelines ran successfully. Last completed: {job_name} at {time} IST.` (green) |
| Any pipeline failed | `❌ {N} pipeline(s) failed. Data may be stale. Scroll to failed cards for details.` (red) |
| Any pipeline partial success | `⚠ {N} pipeline(s) completed with partial failures ({M} tenants failed). Review logs.` (amber) |
| Pipeline currently running | `⏳ {job_name} is currently running — started {N} min ago. {M}% complete.` (blue) |

---

### Section B — Pipeline Health Cards

One card per Celery analytics task. 8 tasks total — 4 analytics pipeline tasks (queues: `analytics`), 2 AI tasks (queue: `ai_generation`), 1 report task (queue: `reports`), 1 export task (queue: `exports`). Cards in a responsive grid, grouped by queue.

**Celery worker health strip** (above the cards, below the status banner):
| Queue | Workers Active | Workers Expected | Status |
|---|---|---|---|
| `analytics` | {N} | 2 | ✅ / ❌ |
| `ai_generation` | {N} | 3 | ✅ / ❌ |
| `reports` | {N} | 5 | ✅ / ❌ |
| `exports` | {N} | 2 | ✅ / ❌ |

Worker count read from Celery inspect API (cached 60s). If any queue has 0 active workers: ❌ red — "No workers on '{queue}' queue. Pipeline tasks will queue but not execute. Contact DevOps." Data Engineer and Platform Admin see this strip; Analytics Manager sees only the overall worker status (✅/❌), not the per-queue breakdown.

**Auto-escalation:** If any queue has 0 active workers for > 5 consecutive minutes, an in-app alert is sent to Platform Admin (10): "⚠ Celery queue '{queue}' has no active workers for 5+ minutes. Tasks are queuing but not executing. [View H-06 →]". This is separate from individual pipeline failure notifications. The "expected" worker count per queue is defined in an environment variable (`CELERY_WORKER_COUNT_{QUEUE}`) set during infrastructure provisioning.

**Card anatomy:**
- Job name (human-readable label)
- Status badge: ✅ SUCCESS / ❌ FAILED / ⚠ PARTIAL_SUCCESS / ⏳ RUNNING / ⬜ SKIPPED / — NEVER_RUN
- Last run time: "{time} IST {date}"
- Key metric from last run: e.g., "4,102 tenant schemas · 12M rows written"
- Card border colour: green (SUCCESS) / red (FAILED) / amber (PARTIAL) / blue (RUNNING) / grey (NEVER_RUN)
- [View Runs] — expands the run history table filtered to this job
- [Run Now] — Data Engineer only — triggers manual immediate run (see confirmation below)

**Schedule indicator:** Below the status: "Next scheduled: {time} IST {day}" (e.g., "Daily at 01:00 IST" or "Weekly — Sunday 03:00 IST")

**[Run Now] confirmation modal:**
- "Manually trigger `{job_name}` now? This will run the full pipeline including reading from {N} tenant schemas. Estimated duration: {est_duration}."
- Warning: "This pipeline is scheduled to run at {time} anyway. Manual runs are for recovery from failures."
- [Confirm] → triggers Celery task → card shows `⏳ RUNNING` state, with a progress indicator updated via HTMX polling every 15s

**[Run All Pipelines Now]** (header button, Data Engineer only): Triggers all 8 pipelines in their dependency order. Confirmation: "Run all analytics pipelines now? This will process all 2,050 tenant schemas across all tasks. Estimated total duration: 75–90 minutes. Cancel the Celery queue if you need to stop mid-run." Progress tracked in overall status banner.

---

### Section C — Run History Table

Server-side paginated, 25 rows per page. Source: `analytics_pipeline_run`.

| Column | Sortable | Notes |
|---|---|---|
| Job Name | Yes | Human-readable; badge colour per status |
| Run Type | No | SCHEDULED / MANUAL |
| Triggered By | No | "System (scheduled)" or user name |
| Started | Yes (default: DESC) | Datetime |
| Duration | Yes | `{min}m {sec}s` or "—" if still running |
| Status | Yes | Badge: SUCCESS / FAILED / PARTIAL_SUCCESS / RUNNING / SKIPPED |
| Rows Processed | Yes | Integer (bigint — cross-tenant totals) |
| Tenants Processed | No | e.g., "2,050 / 2,050" or "1,987 / 2,050" for partial |
| Tenants Failed | Yes | Red number if > 0 |
| Actions | — | [View Details →] opens job detail drawer |

**Filters:**
- Job Name (multiselect)
- Status (multiselect)
- Date Range
- Run Type

**Job Detail Drawer (460px):** Tabs: Summary | Tenant Failures | Error Log

**Summary Tab:**
- All columns from the table
- Rows written to analytics schema
- Celery task ID (for DevOps investigation)

**Tenant Failures Tab:**
Table of tenant schemas where the query failed during this run.
| Column | Notes |
|---|---|
| Tenant ID | — |
| Institution Name | Denormalized |
| Error Type | e.g., SCHEMA_LOCKED, CONNECTION_TIMEOUT, QUERY_ERROR |
| Error Message | First 200 chars; [Show Full] toggles |
| Retried | Yes/No |

If > 50 tenant failures: "Showing first 50 of {N} failures. [Download Full CSV]" — critical for understanding if it's a systemic issue vs isolated tenant issues.

**Error Log Tab:**
Full Python traceback from the Celery task, rendered in a `<pre>` code block with syntax highlighting. [Copy to Clipboard] button. Shows only if `status IN (FAILED, PARTIAL_SUCCESS)`.

---

### Section D — Data Freshness Dashboard

**Purpose:** Shows the current age of each analytics table, so Data Engineers and Analytics Managers can see exactly how stale each dataset is — even if the pipeline "succeeded" (a partial success may mean only 80% of tenants were processed).

| Table | Last Successful Full Run | Age | Freshness Status |
|---|---|---|---|
| `analytics_daily_snapshot` | Today 01:47 IST | 3h | ✅ Fresh (< 26h) |
| `analytics_question_stats` | Today 02:31 IST | 2h | ✅ Fresh |
| `analytics_institution_engagement` | Sunday 03:14 | 4 days | ✅ OK (weekly) |
| `analytics_cohort_snapshot` | 2024-09-01 | 18 days | ✅ OK (monthly) |
| `analytics_ai_batch` (status updates) | Live (5min Celery poll) | 4 min | ✅ Live |
| `analytics_infrastructure_event` | Today 01:47 IST (synced by Task 1 nightly) | 3h | ✅ Fresh (< 26h). Threshold: FRESH < 26h, STALE 26–48h, CRITICAL > 48h (same as daily snapshot — both synced by Task 1). |
| `analytics_report_template` | Live (on-save) | Real-time | ✅ Live |
| `analytics_pipeline_run` | Live | Real-time | ✅ Live |

**Freshness thresholds per table type (unified with H-01 staleness banner — both use the same thresholds):**
- Daily snapshot: FRESH < 26h, STALE 26–48h, CRITICAL > 48h. H-01 pipeline strip triggers at ≥ 26h (STALE threshold) — consistent.
- Weekly engagement: FRESH < 8 days, STALE 8–14 days, CRITICAL > 14 days
- Monthly cohort: FRESH < 35 days, STALE > 35 days
- Live tables: always FRESH

**[Force Refresh]** button on any row (Data Engineer only): triggers the specific pipeline for that table.

---

### Section E — Warehouse SQL Explorer

**Purpose:** A read-only SQL interface against the `analytics` schema (PostgreSQL). Allows Data Engineers (and Analytics Managers with read access) to run ad-hoc queries for investigations — without needing direct DB access or a BI tool.

**Important:** This is ANALYTICS schema only — no access to any tenant schema, no access to PII tables. Query runs as the PostgreSQL `analytics_reader` role — a DB-level read-only user created with `GRANT SELECT ON ALL TABLES IN SCHEMA analytics TO analytics_reader`. This is enforced at the database layer, not application string-checking, so it cannot be bypassed. The Django ORM connection for SQL Explorer uses a separate DB config entry pointing to `analytics_reader` credentials. Session-level `SET statement_timeout = '30000'` (30s) is applied before each query execution to enforce the timeout at the PostgreSQL level.

**UI:**
```
┌────────────────────────────────────────────────────────────────────┐
│  WAREHOUSE SQL EXPLORER                       [Saved Queries ▾]   │
│  ⚠ Read-only · analytics schema only · 30s timeout · 10,000 row limit│
├────────────────────────────────────────────────────────────────────┤
│  SELECT snapshot_date, metric_key, SUM(metric_value) as total     │
│  FROM analytics_daily_snapshot                                     │
│  WHERE snapshot_date >= CURRENT_DATE - 30                          │
│  GROUP BY snapshot_date, metric_key                               │
│  ORDER BY snapshot_date DESC;                                      │
│                                                                  [▶ Run (Ctrl+Enter)]│
├────────────────────────────────────────────────────────────────────┤
│  Results: 540 rows · 0.3s · [Download CSV]                        │
│  ┌───────────────┬─────────────────────────┬──────────┐           │
│  │ snapshot_date │ metric_key              │ total    │           │
│  │ 2024-09-30    │ exam_attempts_total     │ 324,000  │           │
│  └───────────────┴─────────────────────────┴──────────┘           │
└────────────────────────────────────────────────────────────────────┘
```

**Schema browser (left panel, collapsible):**
- Expandable tree of all analytics schema tables
- Click table name: auto-inserts `SELECT * FROM {table} LIMIT 10;` into editor
- Click column name: copies column name to clipboard

**Query execution:**
- Maximum execution time: 30 seconds (hard timeout — prevents long-running queries from blocking other analytics reads)
- Row limit: 10,000 rows (UI-enforced — full results available via CSV download)
- `SELECT` only — any DML or DDL is rejected: "Write queries are not permitted in the explorer."

**Saved queries:**
- [Save Query] — saves with name and optional description
- [Saved Queries ▾] dropdown — list of saved queries (personal + shared)
- Shared queries: Data Engineer can mark a query as "shared with Division H team"
- Queries stored in `analytics_saved_query` table (simple model: `name, sql, created_by, is_shared`)

**Query history:** Last 50 queries run by this user (ring-buffer, FIFO auto-deletion — stored in `analytics_query_history`), accessible from editor. Click to reload.

---

## 5. Access Control

| Gate | Rule |
|---|---|
| Page access | Data Engineer (43), Analytics Manager (42), Platform Admin (10) |
| [Run Now] single pipeline | Data Engineer (43), Platform Admin (10) |
| [Run All Pipelines Now] | Data Engineer (43), Platform Admin (10) — Analytics Manager cannot trigger runs |
| [Force Refresh] in freshness table | Data Engineer (43), Platform Admin (10) |
| SQL Explorer — run queries | Data Engineer (43), Platform Admin (10) |
| SQL Explorer — read-only for | Analytics Manager (42) — can view saved queries but cannot execute (schema structure visible, no query execution) |
| Error log full traceback | Data Engineer (43), Platform Admin (10) — Analytics Manager sees truncated error summary only |
| Tenant failures list | Data Engineer (43), Platform Admin (10) |
| Analytics Manager (42) | Read-only: pipeline cards, run history (no error tracebacks), freshness dashboard |

---

## 6. Edge Cases & Error States

| Scenario | Behaviour |
|---|---|
| A pipeline has never run (fresh install) | Card shows "— NEVER_RUN" state. Freshness table shows "No data yet." [Run Now] highlighted with pulsing attention state: "Run this pipeline to initialize analytics data." |
| Pipeline is still running from yesterday (stuck) | Card shows ⏳ RUNNING with elapsed time: "Running for 4h 32m — expected < 45m. May be stuck." [Force Stop] button (Data Engineer only) → sends Celery `revoke()` with `terminate=True`. Confirmation: "Stop the running task? Current progress will be lost. Partial analytics_daily_snapshot rows written so far will remain in the table — they represent valid data for the tenants that completed. The next full run will upsert over them. The analytics_pipeline_run record will be set to FAILED with reason 'Manually stopped'." |
| Manual run triggered while scheduled run is queued | System checks Celery queue: "A scheduled run of this pipeline is already queued for {time}. Triggering a manual run now will run both — the second run will overwrite the first. Continue?" |
| SQL query times out (> 30s) | Error displayed inline: "Query exceeded 30-second limit. Simplify your query or add a WHERE clause to filter data." No partial results shown. |
| SQL query returns > 10,000 rows | First 10,000 rows shown with banner: "Showing 10,000 of {N} total rows. [Download Full CSV] to get all results." |
| All 2,050 tenant schemas fail (mass failure) | Card shows ❌ FAILED with tenants_failed = 2,050. Alert banner on H-01 and H-06. In-app notification to Platform Admin (10) and all Division H roles. Likely cause: analytics schema down or Celery workers down. |
| Pipeline PARTIAL_SUCCESS with < 5% tenant failures | Shown as PARTIAL_SUCCESS (amber). Minor failures are expected (some tenants may have temporary locks). Analytics data is 95%+ complete. |
| PARTIAL_SUCCESS with > 20% tenant failures | Escalated severity — shown as near-FAILED with red tint. Banner: "⚠ Significant partial failure ({N} tenants failed). Analytics data may be unreliable. Investigate tenant failures." |

---

## 7. UI Patterns

### Loading States
- Pipeline health cards: skeleton 7 cards (same dimensions)
- Run history table: 10-row shimmer
- Freshness dashboard: table skeleton
- SQL explorer: code editor loads immediately (no data load)
- Results table: spinner while query executes

### Toasts
| Action | Toast |
|---|---|
| Pipeline triggered | ✅ "{job_name} started — tracking progress in pipeline cards" (4s) |
| Force stop sent | ⚠ "Stop signal sent to {job_name}. Task may take up to 30s to terminate." (5s) |
| SQL query run | No toast — results shown inline |
| Query saved | ✅ "Query saved: '{name}'" (3s) |

### Responsive
| Breakpoint | Behaviour |
|---|---|
| Desktop (≥1280px) | Full layout: health cards grid + split view for freshness + SQL explorer |
| Tablet | Health cards 2-per-row. Freshness + SQL explorer stacked. |
| Mobile | Health cards single column. SQL Explorer read-only display (no input). Note: "Pipeline management requires desktop." |

---

*Page spec complete.*
*H-06 covers: overall pipeline health banner → Celery worker health strip (per-queue) → 8 pipeline health cards (status / last run / metrics / manual trigger) → execution run history table → tenant failure breakdown drawer with full error log → data freshness dashboard per analytics table → read-only SQL explorer (PostgreSQL `analytics_reader` role, 30s `statement_timeout`, schema browser, saved queries, query history).*
