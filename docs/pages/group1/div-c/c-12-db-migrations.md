# C-12 — Backup & Migration Manager

> **Route:** `/engineering/db-migrations/`
> **Division:** C — Engineering
> **Primary Role:** Platform Admin (Role 10) · Database Administrator (Role 15) · Backend Engineer (Role 11)
> **Read Access:** DevOps/SRE (Role 14)
> **File:** `c-12-db-migrations.md`
> **Priority:** P1
> **Status:** ⬜ Amendment pending — G12 (Migration Matrix tab) · G13 (Restore Verification tab)

---

## 1. Page Name & Route

**Page Name:** Backup & Migration Manager
**Route:** `/engineering/db-migrations/`
**Part-load routes:**
- `/engineering/db-migrations/?part=kpi` — backup and migration health KPI
- `/engineering/db-migrations/?part=snapshots` — RDS snapshot management
- `/engineering/db-migrations/?part=migrations` — Django migration status panel
- `/engineering/db-migrations/?part=drawer&migration_id={id}` — migration detail drawer
- `/engineering/db-migrations/?part=pitr-panel` — PITR restore panel
- `/engineering/db-migrations/?part=archival` — data archival to Glacier

---

## 2. Purpose (Business Objective)

The Backup & Migration Manager controls two things that are both infrequent and extremely high-stakes: database backups and schema migrations.

Backups are the last line of defence after any data loss event. The DBA must know that automated daily snapshots are running, that PITR (Point-in-Time Recovery) is configured with the correct retention window, and that a manual snapshot was taken before any risky migration.

Schema migrations are equally high-risk: a Django migration that adds a column to 2,051 schemas is a ~30-minute operation that must not run during exam hours, must not lock tables, and must be reversible. This page gives the DBA and Backend Engineer visibility into which migrations are applied, which are pending, and which have failed — with the ability to apply migrations selectively per schema, monitor progress across all schemas, and roll back to the previous migration if something goes wrong.

**Business goals:**
- Guarantee automated daily snapshots with 30-day retention across all RDS instances
- Enable instant manual snapshot before any risky operation
- PITR restore to any second in the retention window with a guided workflow
- Full Django migration status visibility across all 2,051 schemas
- Safe, monitored migration execution with per-schema progress and failure handling
- Data archival to S3 Glacier for data older than 2 years (cost management)

---

## 3. User Roles

| Role | Access Level | Permissions |
|---|---|---|
| Platform Admin (10) | Level 5 | Full: snapshots · PITR · migrations · archival · delete snapshots |
| DBA (15) | Level 4 | Full: snapshots · PITR · migrations · archival · delete snapshots |
| Backend Engineer (11) | Level 4 | View migrations · apply migrations to staging/pre-prod; cannot delete snapshots |
| DevOps / SRE (14) | Level 4 — Read | View snapshots + migration status; no write |

---

## 4. Section-Wise Detailed Breakdown

---

### Section 1 — Page Header & Backup Status

**Purpose:** Instant confirmation that backup protection is active.

**Backup Status Banner:**

| State | Colour | Text |
|---|---|---|
| ✅ Backup healthy | Green | "Daily snapshots: active · Last snapshot: 6h ago · PITR enabled: 30 days" |
| ⚠ Snapshot missed | Amber | "Automated snapshot missed last window. Manual snapshot recommended." |
| 🚨 PITR disabled | Red | "PITR is not enabled! Data loss protection is degraded. Enable immediately." |

**Header elements:**
- H1 "Backup & Migration Manager"
- Backup status banner
- "Take Manual Snapshot Now" primary action button (DBA/Admin)
- Pending migrations count badge: "4 migrations pending across 12 schemas"
- Last backup: "RDS automated snapshot: 6h ago · Status: ✅"

---

### Section 2 — KPI Strip

**KPI Cards:**

| Card | Metric | Alert |
|---|---|---|
| Snapshots (last 30d) | Count of automated snapshots available | < 28 = amber (missed some days) |
| Latest Snapshot Age | Hours since most recent automated snapshot | > 26h = amber · > 48h = red |
| PITR Window | Days of point-in-time recovery available | < 28 days = amber |
| Pending Migrations | Schemas with unapplied migrations | > 0 = amber |
| Failed Migrations | Schemas where last migration run failed | > 0 = red |
| Archival Backlog | Data older than 2 years not yet archived | > 100 GB = amber |

---

### Section 3 — RDS Snapshot Management

**Purpose:** View, create, restore, and delete RDS database snapshots.

**Snapshot List Table:**

| Column | Description | Sortable |
|---|---|---|
| Name | Snapshot identifier | ✅ |
| Type | Automated · Manual | ✅ |
| Created | Timestamp | ✅ |
| Size | GB | ✅ |
| Status | Available ✅ · Creating 🔄 · Deleting 🗑 · Failed ❌ | — |
| Encrypted | ✅ / ❌ (all should be ✅) | — |
| Instance | Primary · Replica-1 · Replica-2 | ✅ |
| Retention | Expires in {n} days | ✅ |
| Source | Automated (RDS) · Manual (Admin) · Pre-migration | ✅ |
| Actions | Restore · Copy · Delete | — |

**Snapshot Source Tags:**
- Automated: RDS automated backup (daily)
- Manual: Triggered by DBA/Admin from this page
- Pre-migration: Created automatically by migration pipeline before running migrations (see Section 6)

**Filter bar:**
- Type: All / Automated / Manual / Pre-migration
- Status: All / Available / Creating
- Date range
- Instance: All / Primary / Replica-1 / Replica-2

**Take Manual Snapshot:**
- "Take Manual Snapshot Now" button → modal:
  - Snapshot name: pre-filled with `manual-{timestamp}`
  - Description: textarea (reason for snapshot — required)
  - Instance: Primary (default) / Replica-1 / Replica-2
  - Estimated time: "~15 min depending on database size"
- On confirm: RDS CreateDBSnapshot API → snapshot appears with "Creating" status → transitions to "Available"
- Manual snapshots: not subject to 30-day automated retention; retained until manually deleted

**Delete Snapshot:**
- Confirmation modal: "This snapshot cannot be recovered. Confirm deletion?"
- 2FA required for Admin only
- Pre-migration snapshots: deletion blocked if the migration they were taken for is < 30 days old

**Snapshot storage cost:**
- Displayed per snapshot: estimated ₹ per month for storage
- Total snapshot storage cost: shown in KPI strip

**Automated snapshot schedule:**
- Schedule display: "Daily at 02:00 IST · Retention: 30 days"
- Retention window progress bar: current available days vs 30-day maximum
- Edit: Admin only → RDS ModifyDBInstance (changes backup window + retention period)

---

### Section 4 — PITR (Point-in-Time Recovery) Panel

**Purpose:** Guided workflow for restoring the database to any second within the retention window.

**Access:** DBA + Admin only · 2FA required to initiate

**PITR Status Display:**
- PITR enabled: ✅ / ❌
- Earliest restorable time: {timestamp} (30 days ago)
- Latest restorable time: {timestamp} (5 min ago — WAL upload delay)
- PITR window visualization: horizontal timeline from earliest to latest restorable time

**Initiate PITR Restore:**

> ⚠ **CRITICAL WARNING**: PITR creates a new DB instance. Your current database continues running unchanged. You must manually switch application connections to the restored instance after validation. This is not a one-click rollback — it is a guided disaster recovery procedure.

**Step 1 — Target Time:**
- Date-time picker: select any second within PITR window
- "Restore to just before [event]" helper: select from event log (last 24h of major events: deployments, migrations, exam completions)
- "Current time - N minutes" quick buttons: -5 min · -15 min · -30 min · -1 hour · -6 hours

**Step 2 — Restore Target:**
- New instance identifier: text input (e.g., `restored-to-20260315-0915`)
- Instance class: pre-filled with same as primary (can downgrade for validation)
- Availability Zone: select
- Estimated restore time: "~20–45 minutes depending on database size"

**Step 3 — 2FA Confirmation:**
- TOTP input
- "Begin PITR Restore" button
- Written confirmation: type the target timestamp to confirm

**Post-restore workflow (shown after initiation):**
- Step A: PITR in progress (progress bar — polls RDS DescribeDBInstances)
- Step B: Instance available → "Connect and validate" (shows new instance endpoint for DBA to connect and verify data)
- Step C: "Switch application connections" → instructions to update `platform_system_config` DB connection string + restart Lambda workers
- Step D: "Decommission old primary" → option to stop/delete the pre-restore instance

**PITR history:** Last 5 PITR operations with: initiated by · target time · new instance ID · outcome

---

### Section 5 — Django Migration Status Panel

**Purpose:** Full visibility into Django migration state across all 2,051 schemas.

**Migration Overview:**

| Metric | Value |
|---|---|
| Schemas fully up to date | 2,039 |
| Schemas with pending migrations | 12 |
| Schemas with failed migrations | 0 |
| Latest migration (applied platform-wide) | `20260315_001_add_exam_correction_field` |
| Pending migration (awaiting application) | `20260315_002_add_student_analytics_index` |

**Pending Migrations Table:**

| Migration | App | Description | Applied On | Pending Schemas | Estimated Duration | Pre-snapshot | Status |
|---|---|---|---|---|---|---|---|
| 20260315_002 | exams | Add analytics index | 2,039 schemas ✅ | 12 schemas | ~30 min | ✅ Taken | ⏳ Partially applied |
| 20260401_001 | students | Add DPDPA consent field | 0 schemas | 2,051 schemas | ~45 min | ❌ Not taken | 📋 Ready to apply |

**Per-migration row actions:**
- "Apply to all pending schemas" → Celery job
- "Apply to specific schema" → schema search + apply to one
- "View affected schemas" → list of schemas where this migration is pending
- "View migration SQL" → SQL preview drawer

---

### Section 6 — Migration Detail Drawer

**Purpose:** Full detail for a specific Django migration.

**Drawer Width:** 560px
**Tabs:**

---

#### Tab 1 — SQL Preview

**Purpose:** Show the actual SQL that will be executed for this migration.

**SQL Preview:**
- Syntax-highlighted SQL (from `python manage.py sqlmigrate app_name migration_name`)
- Line count · estimated duration badge
- "Contains table lock?" indicator: ✅ Safe (uses `ADD COLUMN DEFAULT NULL` — no lock) OR ⚠ Lock risk (`ALTER COLUMN TYPE` — requires full table rewrite)
- If lock risk: red banner "This migration requires a table lock. It will block reads and writes for the estimated duration. Do not run during exam hours."

**Estimated Duration:** Based on historical migration times for similar operations × average table sizes across all schemas

---

#### Tab 2 — Affected Schemas

**Purpose:** Show exactly which schemas are affected and their current state.

**Table:**

| Schema | Tenant Name | Status | Last Migration Applied | Schema Size | Action |
|---|---|---|---|---|---|
| tenant_001_vibrant | Vibrant Academy | ✅ Applied | 20260315_002 | 12.4 GB | — |
| tenant_042_sunrise | Sunrise Academy | ⏳ Pending | 20260315_001 | 3.2 GB | Apply |
| tenant_099_alpha | Alpha Coaching | ⏳ Pending | 20260315_001 | 8.1 GB | Apply |

**Bulk action:** "Apply to all pending schemas" (with pre-snapshot prompt if no snapshot taken)

---

#### Tab 3 — History

**Purpose:** Full run history for this migration across all schemas.

**Table:**

| Timestamp | Schemas Attempted | Applied | Failed | Duration | Applied By | Celery Job ID |
|---|---|---|---|---|---|---|
| 2h ago | 2,039 | 2,039 | 0 | 28 min | Priya (Backend) | job-abc123 |

**Failed migration records (if any):**
- Schema name · error message · stack trace (expandable)
- "Retry failed schemas" action

---

### Section 7 — Apply Migrations Workflow

**Purpose:** Guided, safe flow for applying pending migrations to production.

**Trigger:** "Apply to all pending schemas" or "Apply to specific schema"

**Pre-flight Checklist (shown before every migration run):**

| Check | Status |
|---|---|
| Active exams | ✅ No active exams (or: ⚠ 3 exams in progress — migration not recommended) |
| Manual snapshot taken | ✅ Taken 2h ago (or: ⚠ No snapshot in last 24h — recommend taking snapshot first) |
| Migration SQL reviewed | ❓ DBA must check this box manually |
| Lock risk reviewed | ✅ No table locks in this migration |
| Off-peak window | ✅ Current time (02:15 IST) is within off-peak window (00:00–06:00) |
| Maintenance mode | ❓ Enable maintenance mode during migration? (Toggle) |

**"Begin Migration" button:**
- Only active if all critical checks pass (active exams = 0; snapshot taken in last 48h)
- Amber warnings for non-critical items (DBA can acknowledge and proceed)

**Migration Progress Tracker:**

- Header: "Applying 20260315_002 — 2,051 schemas"
- Progress bar: {n}/2,051 schemas complete
- Speed: "~12 schemas/min · Est. remaining: 28 min"
- Current schema being processed: shown live
- Completed schemas: running count ✅
- Failed schemas: running count ❌ (amber if > 0)

**On completion:**
- Success: "Migration applied to 2,051 schemas ✅ — Duration: 28 min"
- Partial failure: "Applied: 2,048 · Failed: 3 — View failed schemas and retry"
- Rollback option: "Apply rollback migration (migrate app_name 000{n-1}) to all schemas" (2FA required)

**Concurrent migration guard:**
- System blocks running two migrations simultaneously
- "Another migration is in progress: 20260315_002 — {n}/2,051 schemas done. Wait for completion."

---

### Section 8 — Migration Rollback

**Purpose:** Revert a migration if it caused issues.

**Trigger:** "Rollback last migration" button (DBA/Admin · 2FA required)

**Rollback types:**
- `python manage.py migrate app_name 000{n-1}` — rolls back to previous migration state
- Equivalent SQL: `DROP COLUMN / DROP INDEX / DROP TABLE` (shown in SQL preview)

**Rollback checklist:**
- Is the previous migration state compatible with current application code? (DBA must acknowledge — system cannot auto-determine this)
- Active exams: must be zero
- Snapshot: must exist from before the migration being rolled back

**Progress tracker:** Same as apply — shows {n}/2,051 schemas rolled back

**Data loss warning:**
- If rollback involves `DROP COLUMN` or `DROP TABLE`: red banner "⚠ DATA LOSS: Rolling back this migration will permanently delete data in the columns/tables being dropped. This data cannot be recovered unless PITR is used. Confirm?"
- Additional confirmation: type migration name to confirm

---

### Section 9 — Data Archival to S3 Glacier

**Purpose:** Move data older than 2 years from live PostgreSQL schemas to S3 Glacier for cost management and compliance.

**Archival Policy Configuration:**

| Data Type | Retention in DB | Archive After | Archive Target | Current Backlog |
|---|---|---|---|---|
| Exam submissions | Active 2 years | 2 years old | S3 Glacier | 4.2 GB |
| Student login history | Active 1 year | 1 year old | S3 Glacier | 8.4 GB |
| Audit log entries | Active 1 year | 1 year old | S3 Glacier (7-year retention for compliance) | 12.1 GB |
| Question bank history | Active 3 years | 3 years old | S3 Glacier | 0.8 GB |

**Archival job controls:**
- "Run archival now" → Celery job: SELECT + export to S3 Glacier + DELETE from live schema
- Schedule: auto-runs monthly at 03:00 IST on the 1st of each month (Celery beat)
- Scope: applies to all tenant schemas + shared schema

**Archival progress:**
- Progress per table per schema: "{n}/2,051 schemas processed"
- Data archived this run: GB counter (live update)
- Rows deleted from live DB: counter

**Archived data retrieval (emergency):**
- "Retrieve archived data" → modal: date range + schema + table
- S3 Glacier retrieval: Standard (3–5 hours) · Bulk (5–12 hours) · Expedited (1–5 minutes, higher cost)
- Cost estimate shown before retrieval
- Retrieved data restored to temporary staging schema for DBA access

**Compliance note:**
- Archived data retained per DPDPA 2023: student data retained 3 years after account closure
- Audit logs retained 7 years (CERT-In + IT Act requirement)
- Compliance retention periods enforced by S3 lifecycle policy (Object Lock — WORM mode for audit logs)

---

## 5. User Flow

### Flow A — Pre-Migration Backup + Apply

1. Backend Engineer creates new Django migration (in CI/CD pipeline)
2. DBA reviews migration SQL in Migration Detail Drawer → SQL Preview tab
3. No table locks detected — safe to apply
4. Pre-flight checklist: active exams = 0 ✅ · snapshot needed ⚠
5. DBA clicks "Take Manual Snapshot" → snapshot created (labelled "pre-migration-20260401_001")
6. After 15 min: snapshot available ✅
7. DBA clicks "Apply to all schemas"
8. Migration applied to 2,051 schemas in 32 min · 0 failures
9. DBA updates migration status in C-09 QA sign-off

### Flow B — PITR Recovery After Accidental Data Deletion

1. Incident reported: bulk student records accidentally deleted in tenant_042 at 14:32
2. DBA opens PITR panel — earliest restorable time: 30 days ago
3. Target time: 14:31 (1 min before deletion)
4. New instance identifier: `restored-tenant-042-1431`
5. 2FA confirmation → PITR initiated
6. 35 min later: new instance available at `restored-tenant-042-1431.rds.amazonaws.com`
7. DBA connects: student records confirmed present at 14:31 state
8. DBA exports specific tenant schema from restored instance
9. Imports deleted records back into live instance (surgical restore — no full switchover needed)
10. Restored instance decommissioned

### Flow C — Monthly Archival Run

1. Celery beat triggers archival job at 03:00 IST on the 1st
2. Archival Manager: "Running archival — exam submissions older than 2 years"
3. 2h 15 min later: 28.4 GB archived from 2,051 schemas
4. Live DB size reduced by 28.4 GB → RDS storage cost ₹2,400/month savings
5. DBA reviews archival report: 0 failures
6. S3 Glacier lifecycle: archived data stored at ₹0.004/GB/month (vs ₹0.115/GB/month in RDS)

---

## 6. Component Structure (Logical)

```
BackupMigrationManagerPage
├── PageHeader
│   ├── BackupStatusBanner
│   ├── PageTitle
│   ├── TakeSnapshotButton (primary CTA)
│   └── PendingMigrationsBadge
├── KPIStrip × 6
├── SnapshotManagement
│   ├── FilterBar
│   ├── SnapshotTable
│   └── TakeSnapshotModal
├── PITRPanel
│   ├── PITRStatusDisplay
│   ├── PITRTimeline (visual)
│   └── PITRRestoreWizard (3-step)
│       ├── Step1_TargetTime
│       ├── Step2_RestoreTarget
│       └── Step3_2FAConfirm
├── MigrationStatusPanel
│   ├── OverviewMetrics
│   └── PendingMigrationsTable
├── MigrationDetailDrawer (560px)
│   └── DrawerTabs
│       ├── SQLPreviewTab
│       ├── AffectedSchemasTab
│       └── HistoryTab
├── ApplyMigrationsWorkflow
│   ├── PreFlightChecklist
│   ├── MigrationProgressTracker
│   └── RollbackOption
└── DataArchivalPanel
    ├── ArchivalPolicyTable
    ├── ArchivalJobControls
    ├── ArchivalProgressDisplay
    └── RetrieveArchivedDataModal
```

---

## 7. Data Model (High-Level)

### platform_rds_snapshots (synced from AWS RDS API)

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| aws_snapshot_id | VARCHAR(255) | RDS snapshot identifier |
| snapshot_type | ENUM | automated/manual/pre_migration |
| instance_id | VARCHAR(100) | RDS instance identifier |
| status | ENUM | available/creating/deleting/failed |
| created_at | TIMESTAMPTZ | |
| size_gb | DECIMAL | |
| encrypted | BOOLEAN | |
| retention_expires_at | TIMESTAMPTZ | nullable (automated only) |
| description | TEXT | nullable (manual: reason field) |
| created_by | UUID FK → platform_staff | nullable (automated = null) |
| migration_id | UUID FK → platform_migrations | nullable (pre_migration type) |

### platform_migrations

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| app_name | VARCHAR(100) | Django app name |
| migration_name | VARCHAR(200) | e.g., `20260315_002_add_analytics_index` |
| description | TEXT | |
| sql_preview | TEXT | cached SQL from `manage.py sqlmigrate` |
| has_table_lock_risk | BOOLEAN | detected by SQL analysis |
| estimated_duration_minutes | INTEGER | |
| total_schemas | INTEGER | 2051 |
| applied_schemas | INTEGER | |
| failed_schemas | INTEGER | |
| status | ENUM | pending/running/completed/partial/failed/rolled_back |
| pre_snapshot_id | UUID FK → platform_rds_snapshots | nullable |
| applied_by | UUID FK → platform_staff | nullable |
| started_at | TIMESTAMPTZ | nullable |
| completed_at | TIMESTAMPTZ | nullable |

### platform_migration_schema_log

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| migration_id | UUID FK | |
| schema_name | VARCHAR(80) | |
| status | ENUM | pending/applied/failed/rolled_back |
| error_message | TEXT | nullable |
| applied_at | TIMESTAMPTZ | nullable |
| duration_ms | INTEGER | nullable |

---

## 8. Validation Rules

| Rule | Detail |
|---|---|
| Apply migration during active exam | Blocked if `platform:active_exam_count > 0` · Override: Admin only with 2FA + written reason |
| Apply migration without snapshot | Amber warning shown · DBA must acknowledge risk before proceeding · not hard-blocked (emergency migrations may be needed) |
| Apply lock-risk migration | Hard-blocked during business hours (07:00–22:00 IST) unless override · 2FA required for override |
| Delete snapshot | Cannot delete last 7 automated snapshots (minimum 7-day coverage retained) · Cannot delete pre-migration snapshot < 30 days old |
| Rollback with data loss | Type migration name to confirm · 2FA required · active exams must be zero |
| PITR restore | 2FA required · type target timestamp to confirm · Admin or DBA only |
| Archival job | Runs only in off-peak window (23:00–06:00 IST) · blocked if active exam detected |
| Snapshot during migration | Auto-snapshot blocked while migration is in progress (avoids capturing partially-migrated state) |

---

## 9. Security Considerations

| Control | Detail |
|---|---|
| PITR restore | Creates a new DB instance — never overwrites live data; manual connection switch step prevents accidental traffic routing to wrong instance |
| Snapshot encryption | All RDS snapshots encrypted at rest with AWS KMS CMK (same key as live RDS); cannot create unencrypted snapshots |
| Migration SQL visibility | SQL preview shown to DBA/Backend/Admin; never includes actual data samples; generated from `manage.py sqlmigrate` (schema-only) |
| Archival data in Glacier | WORM (Object Lock — Governance mode) for audit logs (7-year retention); cannot be deleted by any platform role without AWS account-level override |
| DB credential for migrations | Django migration runner uses dedicated DB role with `CREATE INDEX`, `ALTER TABLE`, `DROP COLUMN` privileges; `DROP SCHEMA` not available to this role |
| Cross-schema migration | Each schema migration runs in separate transaction; failure in one schema rolls back that schema only; does not affect other schemas |
| PITR audit | All PITR initiations logged in `platform_infra_events` with: actor · target time · reason · new instance ID |

---

## 10. Edge Cases (System-Level)

| Scenario | Handling |
|---|---|
| Migration fails on schema #842 out of 2,051 | Job continues with remaining schemas; failed schema recorded; "Retry failed schemas" available; partial success shown in progress tracker |
| New tenant provisioned during migration run | New tenant's schema is empty (just provisioned); migration runner adds it to the queue; typically the migration is already complete for the new schema from initial seed data |
| RDS snapshot quota exceeded | AWS default: 100 manual snapshots per account; amber warning at 90; "Delete oldest manual snapshots" suggestion shown |
| PITR restore target time in WAL gap | If continuous WAL archive has a gap (storage issue), earliest available time after gap is returned by AWS; user shown "Closest restorable time: {adjusted time}" |
| Two DBAs start migration simultaneously | DB-level lock on `platform_migrations` table row; second initiator gets "Migration already in progress" |
| Migration rollback beyond initial schema state | Django cannot rollback to before first migration for an app; system blocks rollback that would result in no applied migrations for an app |
| Archival job takes > 6h (very large dataset) | Celery task timeout extended for archival jobs; progress saved per-schema; job resumes from last completed schema if restarted |

---

## 11. Performance & Scaling Strategy

| Concern | Strategy |
|---|---|
| Migration across 2,051 schemas | Celery worker applies migrations sequentially per schema (not parallel — parallel schema migrations risk RDS connection exhaustion); 12–15 schemas/min throughput; total ~2.5–3h for full run |
| Migration progress display | Celery job updates `platform_migrations.applied_schemas` counter every 100 schemas; HTMX polls progress endpoint every 10s |
| Snapshot list (30-day window) | RDS DescribeDBSnapshots returns max 100 results per call; paginated; cached in Memcached 10 min |
| PITR restore duration | AWS handles restore; platform polls RDS DescribeDBInstances every 60s for status; no timeout (can take 45 min) |
| Schema archival | Bulk export to S3 via `COPY TO` command (PostgreSQL native); 200–500 MB/min per schema; S3 multipart upload for files > 100 MB |
| Snapshot size tracking | Snapshot sizes not available in real-time from AWS (delayed reporting); values cached 1h; shown with "(est.)" label |

---

## 12. Amendment — G12: Migration Matrix Tab

**Assigned gap:** G12 — Migration Matrix: full schema-by-schema migration state grid.

**Where it lives:** New tab added to the existing Migration Status Panel (Section 5). The panel gets two tabs: **Summary** (existing overview metrics + pending migrations table) and **Migration Matrix** (new grid described here).

---

### Migration Matrix Tab

**Purpose:** Give the DBA a complete, schema-level view of migration state across all 2,051 schemas — not just which migrations are pending platform-wide, but exactly which schemas are behind and by how much, per Django app.

**Grid layout:**

The matrix is a dense data grid — rows are schemas, columns are Django apps. Each cell shows the latest applied migration for that app in that schema, colour-coded by pending count.

**Column headers:**

- Schema Name (sticky left column)
- Tenant Name (sticky second column)
- One column per Django app (exams · students · billing · notifications · analytics · reports · platform · auth — 8 apps total)
- Total Pending (computed: sum of pending migrations across all apps for this schema)
- Last Migration Timestamp (most recent migration applied to any app in this schema)

**Cell content:**

Each app cell shows the short migration name (last applied) and a colour badge based on pending migration count for that app in that schema:

| Pending Count | Colour | Meaning |
|---|---|---|
| 0 | Green | Fully up to date |
| 1–3 | Amber | Slightly behind — low urgency |
| > 3 | Red | Significantly behind — investigate |

**Filtering and sorting:**

- Filter by: App name · Status (all / has pending / has red) · Tenant name search
- Sort by: Total Pending (desc by default) · Schema name · Last migration timestamp
- Pagination: 100 schemas per page (21 pages for all 2,051 schemas)
- "Show only schemas with pending migrations" toggle — collapses the view to only affected rows

**Drill-down:** Clicking any cell opens the Migration Detail Drawer (Section 6) pre-filtered to that schema and app combination, showing the specific pending migrations and their SQL preview.

**Bulk action — "Apply pending to all schemas" button:**

Located above the grid. Disabled if no schemas have pending migrations. On click:

1. Summary modal shows: total schemas with pending migrations · total pending migrations · estimated duration · snapshot status
2. If no recent snapshot: amber warning with "Take snapshot before continuing" button
3. Pre-flight checklist (same as Section 7) displayed inline — must pass before enabling "Begin"
4. On confirm: Celery job starts; progress modal appears over the grid (full-screen overlay):
   - Live progress bar: {n}/2,051 schemas processed
   - Current schema being processed: schema name + tenant name
   - Running totals: Applied ✅ · Failed ❌ · Skipped (no pending) ⏭
   - Speed: schemas/min · estimated time remaining
   - "Stop migration" button: halts job after current schema completes (not mid-schema)
5. On completion: progress modal shows final report with "View failed schemas" link if any failures

**Schema-level context menu (right-click or ⋯ on row):**

- Apply all pending migrations for this schema — runs Celery task for single schema only
- View migration history for this schema
- Copy schema name

**Data source:** `platform_migration_schema_log` joined with `platform_migrations` — queried fresh on tab load; no Memcached caching (migration state must be real-time accurate).

---

## 13. Amendment — G13: Restore Verification Tab

**Assigned gap:** G13 — Restore Verification: automated test-restore from RDS snapshot to ephemeral instance with integrity checks.

**Where it lives:** New tab added to the RDS Snapshot Management panel (Section 3). The panel gets two tabs: **Snapshot List** (existing) and **Restore Verification** (new, described here).

**Purpose:** The backup is only as good as the restore. This tab allows the DBA to trigger a non-destructive test restore from any RDS snapshot to an isolated ephemeral RDS instance, run automated integrity checks, and confirm that the backup is actually usable before an incident forces reliance on it.

---

### Restore Verification Tab

**Layout:** Three panels — Source Selection · Verification Status · Verification History

---

**Panel 1 — Source Selection**

The DBA selects a snapshot to test-restore from the existing snapshot list (filtered to "Available" status only). Selection shows:

- Snapshot name and creation timestamp
- Size (GB)
- Type (Automated / Manual / Pre-migration)
- Encrypted: ✅

Ephemeral instance configuration (pre-filled, not editable by default):
- Instance class: db.t3.medium (cost-optimised for verification — not production class)
- Region: same as primary RDS
- Multi-AZ: disabled (ephemeral; no HA needed)
- Estimated restore time: ~20–30 min for a db.t3.medium
- Estimated cost for verification run: ₹ per hour × estimated verification duration (shown before starting)

"Begin Restore Verification" button — requires DBA or Admin role. No 2FA required (read-only operation; ephemeral instance isolated from live traffic).

---

**Panel 2 — Verification Status**

Displayed once a verification run is in progress or recently completed. Shows a step-by-step progress tracker:

**Step 1 — Restore ephemeral instance**

- Triggers RDS RestoreDBInstanceFromDBSnapshot API to create a new isolated instance named `verify-{snapshot_id}-{timestamp}`
- Polls RDS DescribeDBInstances every 60s for "available" status
- Typically 20–30 min; progress shown as animated spinner + elapsed time

**Step 2 — Run verification checks**

Once the ephemeral instance is available, a Celery task connects to it using read-only DBA credentials and runs five automated checks:

| Check | Description | Pass Condition |
|---|---|---|
| Table count match | Count tables in each schema on ephemeral vs expected count from last known-good baseline | Ephemeral count ≥ baseline count (allows for new tables; flags missing tables) |
| Row count sample | Sample 10 tables per schema (largest by estimated row count); compare row counts to live DB within tolerance | Each sampled table row count within ±5% of live DB |
| Referential integrity — FK chain 1 | exam_submissions → students → tenants | 0 orphaned records |
| Referential integrity — FK chain 2 | question_answers → questions → question_banks | 0 orphaned records |
| Referential integrity — FK chain 3 | billing_invoices → tenant_subscriptions → tenants | 0 orphaned records |
| Referential integrity — FK chain 4 | audit_log_entries → platform_staff | 0 orphaned records |
| Referential integrity — FK chain 5 | exam_results → exam_sessions → exams | 0 orphaned records |

Each check shows: ✅ Pass · ❌ Fail · ⏳ Running · ⏭ Skipped (if prior step failed)

**Step 3 — Auto-decommission**

After all checks complete (pass or fail), the ephemeral RDS instance is automatically deleted:
- RDS DeleteDBInstance API with SkipFinalSnapshot = true
- Decommission confirmed once DescribeDBInstances returns "deleted" status
- If decommission fails (AWS API error): amber alert + "Retry decommission" button (DBA must not leave ephemeral instances running — billed hourly)

**Overall result:**

| Outcome | Display |
|---|---|
| All checks pass | Green banner — "Restore verification passed ✅ — Snapshot {name} confirmed restorable. Ephemeral instance decommissioned." |
| One or more checks fail | Red banner — "Restore verification failed ❌ — {n} check(s) failed. See detail below. Ephemeral instance decommissioned." |
| Restore itself failed | Red banner — "Ephemeral restore failed — AWS error: {message}. Snapshot may be corrupt." |

**Failed check detail:** Each failed check shows the exact discrepancy:
- Table count: "Expected 47 tables in tenant_001 — found 44 (missing: exam_correction_fields, analytics_snapshots, billing_adjustments)"
- Row count: "Table exam_submissions in tenant_042: ephemeral 412,300 rows vs live 498,200 rows — 17.3% deviation (threshold: 5%)"
- FK chain: "3 orphaned exam_submissions records found — exam_session_id references non-existent exam_sessions rows"

---

**Panel 3 — Verification History**

Table of the last 20 verification runs:

| Column | Description |
|---|---|
| Run Date | Timestamp when verification started |
| Snapshot | Snapshot name tested |
| Snapshot Date | When the snapshot was taken |
| Initiated By | DBA / Admin name |
| Duration | Total time from restore start to decommission |
| Result | ✅ All pass · ❌ {n} failures · ⚠ Restore failed |
| Detail | "View report" link → opens verification-report-drawer |

**Verification report drawer (verification-report-drawer):**
- Full check-by-check result breakdown
- Ephemeral instance ID used (for AWS CloudTrail audit trail)
- Cost of verification run (from AWS Cost Explorer — shown post-completion with 1h delay)
- "Retry verification with same snapshot" button

**Data model:**

**platform_restore_verifications**

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| snapshot_id | UUID FK → platform_rds_snapshots | |
| ephemeral_instance_id | VARCHAR(255) | AWS RDS instance identifier |
| status | ENUM | restoring / verifying / decommissioning / passed / failed / error |
| initiated_by | UUID FK → platform_staff | |
| started_at | TIMESTAMPTZ | |
| completed_at | TIMESTAMPTZ | nullable |
| duration_seconds | INTEGER | nullable |

**platform_restore_verification_checks**

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| verification_id | UUID FK → platform_restore_verifications | |
| check_name | VARCHAR(100) | table_count_match / row_count_sample / fk_chain_1..5 |
| status | ENUM | pending / running / passed / failed / skipped |
| detail | JSONB | discrepancy detail for failed checks |
| started_at | TIMESTAMPTZ | nullable |
| completed_at | TIMESTAMPTZ | nullable |
