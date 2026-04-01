# C-05 — Service Deployment Manager

> **Route:** `/engineering/deployments/`
> **Division:** C — Engineering
> **Primary Role:** Platform Admin (Role 10) · Backend Engineer (Role 11) · DevOps/SRE (Role 14)
> **Read Access:** Frontend Engineer (Role 12)
> **File:** `c-05-deployments.md`
> **Priority:** P1
> **Status:** ⬜ Amendment pending — G1 (Environment Variables tab) · G2 (Scheduled Jobs tab)

---

## 1. Page Name & Route

**Page Name:** Service Deployment Manager
**Route:** `/engineering/deployments/`
**Part-load routes:**
- `/engineering/deployments/?part=kpi` — deployment health KPI strip
- `/engineering/deployments/?part=table` — Lambda function version table
- `/engineering/deployments/?part=drawer&function={name}` — function detail drawer
- `/engineering/deployments/?part=canary-panel` — active canary deployments panel
- `/engineering/deployments/?part=deploy-modal` — new deployment modal

---

## 2. Purpose (Business Objective)

The Service Deployment Manager provides full control over Lambda function versions across all ~68 platform services. It is the operational bridge between what CI/CD (C-09) builds and what is actually serving live traffic. Engineers use this page to shift traffic between versions during canary deployments, roll back to a previous version when something goes wrong, and confirm that every Lambda alias is pointing to the correct version.

This page is most critical immediately after a deployment: the first 30 minutes after any production release are when engineers watch this page alongside C-04 API Health Monitor for any regression signal. A one-click rollback button that works under pressure — without needing to navigate to the AWS console — is the core value of this page.

**Business goals:**
- Make Lambda version management transparent and controllable from a single UI
- Enable blue/green canary traffic splitting (e.g., 95%/5%) without AWS console access
- Provide one-click rollback to any previous stable version during an incident
- Link deployments to CI/CD pipeline runs (C-09) and release manager (Div B page 03) for full traceability
- Ensure no deployment is promoted to 100% traffic without passing post-deploy health checks

---

## 3. User Roles

| Role | Access Level | Permissions |
|---|---|---|
| Platform Admin (10) | Level 5 | Full: deploy · rollback · traffic shift · alias management · force-promote |
| Backend Engineer (11) | Level 4 | Full: deploy · rollback · traffic shift · alias management |
| DevOps / SRE (14) | Level 4 | Full: deploy · rollback · traffic shift · alias management |
| Frontend Engineer (12) | Level 4 — Read | View deployment status and history; cannot trigger deployments |

---

## 4. Section-Wise Detailed Breakdown

---

### Section 1 — Page Header & Deployment Status

**Purpose:** Instant view of whether a deployment is in progress and the current production stability posture.

**Active Deployment Banner (conditional):**
- Shown whenever a canary deployment is in progress
- Amber: "🚀 Canary deployment in progress: {function-name} — v42 (95%) / v43 (5%) — Started 12 min ago"
- Red (if health check failing during canary): "🚨 Canary deployment unhealthy — v43 error rate 8% — Recommend rollback"

**Header elements:**
- H1 "Service Deployment Manager"
- "Deploy New Version" button (Admin · Backend · DevOps)
- "Rollback Last Deployment" quick-button (emergency shortcut — pre-selects most recent deployment)
- Total Lambda functions: "68 functions"
- Last deployment: "exam-service-submit · v44 · 2h ago by Priya Sharma"

**Role-Based Behavior:**
- Frontend Engineer: Deploy and Rollback buttons hidden; read-only notice shown

---

### Section 2 — KPI Strip

**Purpose:** Fleet-wide deployment health at a glance.

**KPI Cards:**

| Card | Metric | Alert |
|---|---|---|
| Functions on Latest | Count where alias `$LIVE` = latest published version | < 95% amber |
| Active Canaries | Count of functions with split traffic (in canary) | > 0 = info (blue) |
| Failed Health Checks | Functions where post-deploy check failed | > 0 = red |
| Deployments Today | Count of deployments in last 24h | — |
| Rollbacks Today | Count of rollbacks in last 24h | > 2 = amber |
| Last Deploy Time | Time since most recent deployment | — |

**Data Flow:**
- Lambda GetAliasConfiguration + ListVersionsByFunction API calls — batched per function
- Results cached Memcached 60s; Celery beat refreshes every 55s
- KPI poll: 60s HTMX interval

---

### Section 3 — Active Canary Deployments Panel

**Purpose:** Dedicated panel for any function currently in a canary (traffic-split) state.

**Always visible** when canary count > 0; collapsed (hidden) when no canaries active.

**Canary Card per active canary:**

| Element | Detail |
|---|---|
| Function name | e.g., `exam-service-submit` |
| Traffic split | v42 (stable): 95% · v43 (canary): 5% |
| Canary started | Relative time + initiating engineer |
| Canary health | P99 latency: stable vs canary comparison |
| Error rate | stable vs canary comparison |
| Cold starts | stable vs canary comparison |
| Recommendation | Auto-generated: "✅ Canary healthy — promote when ready" OR "⚠ Canary degraded — consider rollback" |

**Actions per canary card:**
- "Promote to 100%" — shifts all traffic to canary version; decommissions stable alias split
- "Increase to 25%" / "50%" / "75%" — manual traffic step-up
- "Rollback Canary" — shifts all traffic back to stable version; canary version decommissioned

**Auto-promote rules (configurable per function):**
- If canary version: P99 within SLA + error rate < 0.5% + no cold start storm for 30 min → auto-promote prompt appears (Admin/DevOps must still click Promote — no fully autonomous promotion)

---

### Section 4 — Lambda Function List Table

**Purpose:** All 68 Lambda functions with current version, alias configuration, and deployment history.

**Table Columns:**

| Column | Description | Sortable |
|---|---|---|
| Function Name | Lambda function name | ✅ |
| Service | High-level service group (exam · auth · result · tenant · ai · notif · billing) | ✅ |
| Live Version | Currently active version number on `$LIVE` alias | ✅ |
| Traffic Split | "100% v44" OR "95% v44 / 5% v45 (canary)" | — |
| Status | ✅ Stable · 🚀 Canary · ⚠ Degraded · ❌ Health Check Failed · 🔄 Deploying | ✅ |
| Last Deployed | Relative timestamp | ✅ |
| Deployed By | Engineer name | — |
| CI/CD Run | Build number (link to C-09 pipeline run) | — |
| Health Check | ✅ Passed · ❌ Failed · ⏳ Running · — N/A | ✅ |

**Row States:**
- Deploying (blue pulsing): deployment in progress
- Canary (amber): split traffic active
- Health Check Failed (red): last post-deploy check failed → rollback recommended
- Degraded (amber): high error rate or P99 breach detected after recent deployment

**Filter Bar:**
- Service group filter
- Status filter (Stable / Canary / Degraded / Health Check Failed)
- Deployed by filter (engineer name)
- "Show only recently deployed (24h)" quick toggle

**Data Flow:**
- Function list from `platform_deployment_registry` DB table (static function catalogue)
- Live version and alias from Lambda GetAliasConfiguration API (batched)
- Health check results from `platform_deploy_health_checks` table
- Table refresh: 30s HTMX poll (guard: no drawer open)

---

### Section 5 — Lambda Function Detail Drawer

**Purpose:** Full deployment history, version management, and traffic routing controls for a single Lambda function.

**Drawer Width:** 640px
**Tabs:**

---

#### Tab 1 — Versions

**Purpose:** Full version history with traffic routing controls.

**Version List:**

| Version | Published At | Published By | Code SHA | Size | Status | Traffic |
|---|---|---|---|---|---|---|
| v45 | 2h ago | Priya Sharma | `abc123ef` | 24.3 MB | Canary | 5% |
| v44 | 2 days ago | Rohan Dev | `def456ab` | 24.1 MB | Stable (live) | 95% |
| v43 | 5 days ago | Priya Sharma | `ghi789cd` | 23.9 MB | Previous | 0% |
| v42 | 8 days ago | Rohan Dev | `jkl012ef` | 23.8 MB | Previous | 0% |

**Per-version actions:**
- "Set as Live" (promote to 100% on `$LIVE` alias) — 2FA for Admin; no 2FA for Backend/DevOps
- "Start Canary at 5%" (split current live: 95%, this version: 5%)
- "View CloudWatch metrics for this version" (deep-link to C-04 filtered to this version)
- "View CI/CD pipeline run" (link to C-09)
- "Compare with current live" (side-by-side diff of environment variables + code SHA)

**Version retention:** Last 20 versions retained in Lambda; older versions shown as "archived" (still rollback-able but marked as outdated)

**Traffic routing display:**
- Visual bar: blue = stable version, green = canary version — proportional to traffic split
- Editable: click on percentage → inline number input → "Apply" (Admin/Backend/DevOps)

---

#### Tab 2 — Aliases

**Purpose:** Manage Lambda aliases (named pointers to versions).

**Aliases Table:**

| Alias | Points To | Traffic Split | Purpose |
|---|---|---|---|
| `$LIVE` | v44 (95%) + v45 (5%) | Canary | Production traffic |
| `$STABLE` | v44 | 100% | Rollback target |
| `$LATEST` | Latest published | 100% | CI/CD testing (not live traffic) |
| `staging` | v45 | 100% | Staging environment testing |
| `load-test` | v44 | 100% | Dedicated for k6 load testing |

**Actions (Admin/Backend/DevOps):**
- Edit alias target version (dropdown of available versions)
- Adjust traffic weights for `$LIVE` alias
- Create new alias (name + target version)
- Delete alias (confirmation modal; cannot delete `$LIVE` or `$STABLE`)

**`$STABLE` alias management rule:** `$STABLE` is automatically updated to the previous `$LIVE` version on every successful deployment. This ensures one-click rollback always works.

---

#### Tab 3 — Health Checks

**Purpose:** Post-deployment automated health check results for this function.

**Health Check Log Table:**

| Timestamp | Triggered By | Deployment | Status | Duration | Details |
|---|---|---|---|---|---|
| 2h ago | Auto (post-deploy) | v45 | ⏳ Running | 8 min | 3/5 checks passed |
| 2 days ago | Auto (post-deploy) | v44 | ✅ Passed | 12 min | All 5 checks passed |
| 5 days ago | Auto (post-deploy) | v43 | ❌ Failed | 4 min | Check 3 failed: P99 > 200ms |

**Health check types (configurable per function):**

| Check | Description | Pass Condition |
|---|---|---|
| Smoke test | Call endpoint with synthetic request | HTTP 200 returned |
| Latency check | 50 synthetic requests · measure P99 | P99 < SLA threshold |
| Error rate check | Monitor 5 min of live traffic | Error rate < 0.5% |
| Cold start check | Flush concurrency + invoke 10 times | All invocations < 2× SLA |
| Dependency check | Verify all downstream services responding | All deps healthy |

**Actions:**
- "Re-run Health Check" button (Admin/Backend/DevOps · triggers fresh health check run)
- "View check logs" (expandable per check run — shows raw output)
- "Override failed check" (Admin only · 2FA · reason required) — marks failed check as accepted; deployment proceeds

---

#### Tab 4 — Deployment Log

**Purpose:** Chronological log of every deployment action for this function.

**Columns:**

| Column | Description |
|---|---|
| Timestamp | ISO 8601 |
| Action | Deployed · Promoted · Rolled back · Traffic shifted · Alias updated · Health check run |
| Actor | Engineer name + email + IP |
| From Version | Previous version |
| To Version | New version |
| Traffic Before | Traffic split before action |
| Traffic After | Traffic split after action |
| CI/CD Run | Link to C-09 pipeline run |
| 2FA Used | ✅ / — |
| Notes | Optional engineer note |

**Pagination:** 25 entries per page · newest first
**Export:** CSV (Admin/Backend/DevOps)

---

### Section 6 — Deploy New Version Modal

**Purpose:** Guided flow to deploy a new Lambda function version to production.

**Trigger:** "Deploy New Version" button in page header or function-specific "Deploy" in drawer

**Modal Width:** 640px

---

#### Step 1 — Select Function & Version

**Fields:**
- Function: dropdown of all 68 registered Lambda functions (or pre-selected if triggered from drawer)
- Source: CI/CD Pipeline Run (select from recent successful runs in C-09) OR Direct Lambda version (version number input)
- Selected version summary: code SHA · built at · CI/CD run link · test results summary

**Validation:**
- Only versions that have passed CI/CD pipeline (Test + Lint + Build stages) can be deployed
- Versions that failed CI/CD: blocked with "This build has failing tests. Deployment blocked." (Admin can override with reason + 2FA)

---

#### Step 2 — Deployment Strategy

**Options:**

| Strategy | Description | Recommended For |
|---|---|---|
| Direct (immediate) | New version immediately gets 100% traffic | Non-critical functions · hotfixes |
| Canary 5% | 5% of traffic routed to new version; 95% to current stable | Standard feature releases |
| Canary 1% | 1% traffic split; very conservative | High-risk changes · exam-critical functions |
| Blue/Green scheduled | Deploy to 0%, manually promote when ready | Large schema changes |

**Environment variable override (optional):**
- Show current env vars (values masked for secrets)
- Add/modify env vars for this specific deployment (stored as Lambda version config)
- Changed vars highlighted with "Modified" chip

**Pre-deploy checklist:**
- Manual confirmation checkboxes (admin fills):
  - [ ] Release notes updated in Release Manager (Div B page 03)
  - [ ] DB migrations applied (if any)
  - [ ] QA sign-off obtained (link to C-09 QA gate)
  - [ ] No active exams in progress (exam window check)

---

#### Step 3 — Review & Confirm

**Summary card:**
- Function: `exam-service-submit`
- From: v44 → To: v45
- Strategy: Canary 5%
- Health checks: 5 automated checks will run post-deploy
- Estimated time to full promotion (if all checks pass): ~35 min

**2FA:** Not required for Backend/DevOps; required for Platform Admin (Level 5 accounts always 2FA for destructive actions)

**"Deploy" button:**
- On confirm: `POST /api/deployments/`
- Lambda UpdateAlias API called to set weighted traffic
- Post-deploy health checks queued in Celery
- Canary panel on main page updates immediately

---

### Section 7 — Rollback Flow

**Purpose:** One-click rollback to a previous stable version during an incident.

**Quick Rollback (from page header "Rollback Last Deployment"):**
- Pre-fills: most recent deployed function + previous version (`$STABLE` alias target)
- Confirmation modal: "Roll back {function-name} from v45 → v44? This will immediately shift 100% traffic to v44."
- No 2FA required (speed is critical during incident)
- Audit log entry: actor + timestamp + reason (optional quick reason field — 3 options: "Performance regression" · "Error rate spike" · "Incorrect behaviour")

**Full rollback (from function drawer Versions tab):**
- Select any previous version
- Confirmation modal
- Optional rollback note

**On rollback:**
- Lambda UpdateAlias API: `$LIVE` alias → target version, weight = 100%
- `$STABLE` NOT updated (stable pointer retained; rollback is to stable, not to previous-previous)
- Canary panel cleared for this function
- CloudWatch alarm acknowledges traffic shift
- C-18 auto-creates a deployment rollback record (not a full incident unless error rate continues)

**Post-rollback:**
- Health check runs automatically on the restored version
- If restored version also unhealthy: "Rollback version also showing issues. Consider rolling back to v{n-2}." — shows list of all available rollback targets

---

### Section 8 — Environment Variable Manager

**Purpose:** View and manage Lambda environment variables per function (values at version level).

**Access:** Admin + Backend + DevOps (view all non-secret vars); Secrets shown as `[SECRET — managed in C-14]`

**Layout (within function drawer or standalone section):**

**Variable Table:**

| Key | Value | Source | Last Modified | Modified By |
|---|---|---|---|---|
| `DJANGO_ENV` | `production` | Direct | 3 months ago | System |
| `DB_HOST` | `[SECRET — C-14]` | Secrets Manager | — | — |
| `MEMCACHED_URL` | `[SECRET — C-14]` | Secrets Manager | — | — |
| `LOG_LEVEL` | `INFO` | Direct | 2 weeks ago | Priya Sharma |
| `FEATURE_FLAGS_TTL` | `30` | Direct | 1 week ago | Rohan Dev |

**Add/Edit variable:**
- Key: text input (must be uppercase + underscores only)
- Value: text input OR toggle "Use Secrets Manager ARN"
- If Secrets Manager: ARN input (validated against known secret ARNs in C-14)
- Saved at: Lambda function level (applies to all future deployments unless overridden per-version)

**Note:** Environment variable changes require a new Lambda deployment to take effect — inline warning shown: "Changes to environment variables will take effect on next deployment."

---

## 5. User Flow

### Flow A — Standard Canary Deployment

1. CI/CD pipeline (C-09) completes: new version v45 built and tested for `exam-service-submit`
2. Backend Engineer opens `/engineering/deployments/`
3. Clicks "Deploy New Version"
4. Step 1: selects `exam-service-submit` · selects CI/CD run for v45
5. Step 2: strategy = "Canary 5%" · no env var changes
6. Pre-deploy checklist: all boxes checked
7. Step 3: reviews summary → confirms
8. Canary panel appears: v44 (95%) / v45 (5%)
9. Engineer switches to C-04 API Health Monitor — watches v45 error rate and P99
10. After 30 min of healthy metrics: returns to canary panel → "Promote to 100%"
11. Traffic shifts: v45 = 100% · deployment log entry created · `$STABLE` updated to v44

### Flow B — Emergency Rollback During Exam

1. DevOps on-call receives PagerDuty: exam submit error rate 12% after v45 deployment
2. Opens `/engineering/deployments/`
3. Active deployment banner: "🚨 Canary deployment unhealthy — v45 error rate 12%"
4. Clicks "Rollback Last Deployment" (page header button)
5. Confirmation modal pre-filled: `exam-service-submit` v45 → v44
6. Clicks "Rollback" · selects reason "Error rate spike"
7. Traffic: v44 = 100% within 5s
8. Error rate recovers on C-04
9. C-18 deployment rollback record created
10. Post-incident: team investigates v45 cause before re-deploying

### Flow C — Blue/Green for Schema Migration Deployment

1. DBA applies migration to all schemas (tracked in C-12)
2. Backend Engineer deploys new version to `$LIVE` at 0% (Blue/Green scheduled strategy)
3. Staging testing: `staging` alias points to new version; QA validates
4. After QA sign-off (C-09 gate): Backend Engineer sets traffic to 10% → monitors 15 min
5. Steps up: 25% → 50% → 75% → 100% with 10-min monitoring between each
6. Full promotion at 100%; deployment log updated

---

## 6. Component Structure (Logical)

```
DeploymentManagerPage
├── PageHeader
│   ├── PageTitle
│   ├── DeployNewVersionButton
│   ├── RollbackLastDeployButton (emergency)
│   └── LastDeployInfo
├── ActiveDeploymentBanner (conditional)
├── KPIStrip
│   └── KPICard × 6
├── ActiveCanaryPanel (conditional, amber border)
│   └── CanaryCard × N (per in-progress canary)
│       ├── FunctionName
│       ├── TrafficSplitBar
│       ├── HealthComparison (stable vs canary metrics)
│       ├── Recommendation
│       └── CanaryActions (Promote / Increase / Rollback)
├── FilterBar
├── LambdaFunctionTable
│   ├── TableHeader
│   └── FunctionRow × 68
│       ├── FunctionName
│       ├── ServiceLabel
│       ├── LiveVersionBadge
│       ├── TrafficSplitCell
│       ├── StatusBadge
│       ├── LastDeployedCell
│       ├── DeployedByCell
│       ├── CICDRunLink
│       └── HealthCheckBadge
├── FunctionDetailDrawer (640px)
│   └── DrawerTabs
│       ├── VersionsTab (list + traffic controls)
│       ├── AliasesTab
│       ├── HealthChecksTab
│       └── DeploymentLogTab
├── DeployNewVersionModal (3-step)
│   ├── Step1_SelectFunctionVersion
│   ├── Step2_Strategy (+ env var override + pre-deploy checklist)
│   └── Step3_ReviewConfirm
└── RollbackConfirmModal
```

---

## 7. Data Model (High-Level)

### platform_deployment_registry

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| function_name | VARCHAR(100) | matches Lambda function name |
| service_group | VARCHAR(50) | |
| live_version | INTEGER | current version on $LIVE alias |
| stable_version | INTEGER | current version on $STABLE alias |
| canary_version | INTEGER | nullable — active canary version |
| canary_traffic_pct | SMALLINT | 0–100 |
| last_deployed_at | TIMESTAMPTZ | |
| last_deployed_by | UUID FK → platform_staff | |
| last_cicd_run_id | VARCHAR(100) | link to C-09 |
| health_check_status | ENUM | pending/running/passed/failed/not_run |
| is_exam_critical | BOOLEAN | |
| created_at | TIMESTAMPTZ | |

### platform_deployment_log

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| function_name | VARCHAR(100) | |
| action | ENUM | deployed/promoted/rolled_back/traffic_shifted/alias_updated |
| actor_id | UUID FK → platform_staff | |
| actor_ip | INET | |
| from_version | INTEGER | nullable |
| to_version | INTEGER | |
| traffic_before | JSONB | `{v44: 100}` |
| traffic_after | JSONB | `{v44: 95, v45: 5}` |
| cicd_run_id | VARCHAR(100) | nullable |
| strategy | ENUM | direct/canary_5/canary_1/blue_green |
| reason | TEXT | nullable (rollback reason) |
| twofa_used | BOOLEAN | |
| created_at | TIMESTAMPTZ | |

### platform_deploy_health_checks

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| deployment_log_id | UUID FK | |
| function_name | VARCHAR(100) | |
| version | INTEGER | |
| status | ENUM | pending/running/passed/failed/overridden |
| checks_passed | SMALLINT | |
| checks_total | SMALLINT | |
| failed_check_name | VARCHAR(100) | nullable |
| failure_detail | TEXT | nullable |
| override_reason | TEXT | nullable |
| overridden_by | UUID FK → platform_staff | nullable |
| started_at | TIMESTAMPTZ | |
| completed_at | TIMESTAMPTZ | nullable |

---

## 8. Validation Rules

| Field | Rule |
|---|---|
| Version for deployment | Must be from a passed CI/CD run unless admin override with reason + 2FA |
| Canary traffic percentage | 1–50% only (cannot start canary at > 50% — that's a direct deploy, use Direct strategy) |
| Exam-critical function deploy | Additional pre-deploy check: if active exams > 0 → deployment blocked with "Exams in progress. Wait for exam window to close or proceed with explicit override." |
| Environment variable key | Uppercase letters and underscores only · max 128 chars · reserved keys (`AWS_*`, `LAMBDA_*`) blocked |
| Alias name | Lowercase alphanumeric + hyphens · max 50 chars · `$LIVE` and `$STABLE` are system aliases; cannot be deleted |
| Rollback | Cannot rollback to a version that failed health checks unless reason provided |
| Force promote failing canary | Admin only · 2FA · reason min 50 chars |

---

## 9. Security Considerations

| Control | Implementation |
|---|---|
| Lambda UpdateAlias permissions | Deployment service has IAM role with `lambda:UpdateAlias` and `lambda:UpdateFunctionCode` scoped to platform function ARN patterns; cannot deploy to non-platform functions |
| 2FA for Admin deploys | Platform Admin (Level 5) requires TOTP for all deployments; Backend and DevOps do not (speed during incident matters) |
| CI/CD validation gate | Version deployed must match a CI/CD run with `status = passed`; enforced server-side; cannot be bypassed via API directly |
| Rollback audit | Rollbacks always logged even without 2FA; actor + IP + timestamp + reason stored |
| Environment variable secrets | AWS Secrets Manager ARNs only in Lambda config; no plaintext secrets in env vars enforced by validation |
| Frontend Engineer read scope | Lambda GetAliasConfiguration API called server-side; Frontend Engineers never have direct AWS console access through this page |
| Deployment log immutability | `platform_deployment_log` INSERT-only; no UPDATE/DELETE allowed via application layer |

---

## 10. Edge Cases (System-Level)

| Scenario | Handling |
|---|---|
| Lambda API call fails during deployment | Deployment marked `failed`; retry option available; partial deployment state (alias not updated) — health check will catch if traffic wasn't actually shifted |
| Canary left running for > 24h without action | Daily reminder notification to deploying engineer and their team; after 48h: escalation to Platform Admin |
| Both stable and rollback versions failing | Drawer shows all available versions; engineer must manually select an older known-good version; system suggests last version with `health_check_status = passed` |
| Deploy during active exam (override used) | Extra audit log flag `deployed_during_exam = true`; post-incident review required (C-18 links) |
| Health check runs but CloudWatch data not yet available | Health check waits up to 10 min for CloudWatch data to populate; timeout after 15 min → status = `inconclusive` → admin prompted to manually verify |
| Two engineers deploy same function simultaneously | Optimistic lock on `platform_deployment_registry.function_name`; second deployer gets "Deployment already in progress for {function-name}. Wait for current deployment to complete." |
| Lambda version limit reached (10,000 versions) | Celery beat cleanup job removes versions older than 90 days that are not referenced by any alias; alert at 9,000 versions |

---

## 11. Performance & Scaling Strategy

| Concern | Strategy |
|---|---|
| Lambda API rate limits | AWS Lambda API: 100 requests/sec per region; batching function status queries using AWS SDK pagination; cached in Memcached 60s |
| 68 function status queries | Single `ListFunctions` call + parallel `GetAliasConfiguration` calls (100 concurrent via asyncio); total < 3s; cached 60s |
| Canary health comparison data | Sourced from C-04 KPI strip Memcached cache; no additional CloudWatch calls; same 25s cache |
| Deployment log page load | Index on `function_name + created_at`; 25 entries per page; < 50ms |
| Health check execution | Celery worker: runs 5 checks in parallel per deployment; each check is an async HTTP call or CloudWatch query; all 5 checks complete within 15 min |
| Real-time canary panel | 30s HTMX poll; data from Memcached (C-04 writes exam-critical metrics to Memcached); no extra CloudWatch calls for canary panel |

---

## Amendment — G1: Environment Variables Tab

**Gap addressed:** Backend Engineer could not view or edit Lambda environment variables (DB connection strings, API key references, feature toggles). C-05 covered version/routing only.

### New Tab in Lambda Function Drawer — Environment Variables

A new **Environment Variables** tab is added to the `lambda-function-drawer` (and also exposed as a standalone sub-page tab on the main deployment page for the selected function).

**Access:** `/engineering/deployments/?part=env-vars&function={name}`

**Tab layout:**

**Current Variables Table:**

| Column | Description |
|---|---|
| Key | Variable name (always visible) |
| Value | Masked by default (••••••••) — "Reveal" button shows plaintext for 30s (Admin + Backend only) · if value references Secrets Manager ARN — shown as `[SECRET — ARN]` badge |
| Source | Direct (stored in Lambda config) · Secrets Manager (value is ARN reference) |
| Last Modified | Timestamp + who |
| Actions | Edit · Delete (Admin + Backend) |

**Add Variable:** "Add Variable" button → inline row with key input + value input + source selector (Direct / Secrets Manager ARN) → "Save" per row.

**Edit Variable:** Click Edit on any row → inline edit → key is read-only after creation (to prevent accidental rename); value editable → "Save" applies change.

**Diff View:** "Compare with Live" toggle → two-column view showing current (what's deployed now) vs pending (what will be deployed) — green = added · amber = changed · red = removed.

**Deploy on Save:** After any edit, a "Deploy Changes" button appears in the drawer footer with a pre-deploy health check: checks if function is currently serving traffic above 1% of peak before allowing deploy.

**Restrictions:**
- Raw secret values never stored in Django DB — only ARN references stored; actual values fetched from Secrets Manager at Lambda runtime
- Reveal plaintext: only for Direct-source values; Secrets Manager values cannot be revealed from this UI (must use C-14)
- All changes: 2FA required from Backend Engineer and Admin; DevOps can view but not edit env vars (security boundary)

**Data Flow:**
- Existing variables: `GET /api/lambda/{function}/env-vars/` → calls AWS Lambda GetFunctionConfiguration API → returns env var map
- Save: `PATCH /api/lambda/{function}/env-vars/` → calls Lambda UpdateFunctionConfiguration → Celery job polls until configuration update completes → success toast

**Post-Deploy Feature Flag Actions:**

The deployment detail drawer shows a read-only "Post-deploy flag actions" panel at the bottom of the G1 Environment Variables tab. This panel lists any feature flags in C-21 that are linked to this function and configured to auto-enable on successful deployment:

| Flag Key | Flag Name | Environment | Action on Success |
|---|---|---|---|
| `new_exam_ui_v2` | New Exam UI Version 2 | Production | Enable (OFF → ON) |
| `new_grading_engine` | New Grading Engine | Staging | Enable (OFF → ON) |

When the deployment health check passes, the Celery post-deploy task automatically enables each linked flag in its configured environment and logs the action to `platform_flag_audit_log` with `action = "deployment_auto_enabled"`. If no flags are linked, this panel shows "No post-deploy flag actions configured." Engineers can link flags from the C-21 Feature Flag Manager (Flag Config tab → Linked Deployment field).

---

## Amendment — G2: Scheduled Jobs Tab

**Gap addressed:** No page showed scheduled background jobs (nightly aggregations, health checks, archival tasks). Nobody could pause, trigger, or audit Celery beat tasks.

### New Tab on Service Deployment Manager Page — Scheduled Jobs

**Access:** `/engineering/deployments/?tab=scheduled-jobs` — top-level tab on the main page, alongside the function list.

**Layout:**

**Celery Beat Task Registry Table:**

| Column | Description |
|---|---|
| Task Name | Full dotted Python path (e.g., `portal.tasks.aggregation.nightly_exam_summary`) |
| Queue | Celery queue name (e.g., `default` · `exam_critical` · `low_priority`) |
| Schedule | Human-readable: "Every day at 02:00 IST" · "Every 5 minutes" · "0 8 * * 1 (Mondays 08:00)" |
| Last Run Time | Timestamp of most recent execution start |
| Last Run Status | ✅ Success · ❌ Failed · ⚠ Partial · ⏳ Running · — Never run |
| Next Run Time | Calculated from schedule + last run |
| Average Duration | P50 duration over last 30 runs |
| Actions | Pause/Resume · Run Now · View History |

**Filters:** Queue · Status (Healthy/Failed/Paused/Never Run) · Schedule type (interval/cron)

**Per-task actions:**
- **Pause/Resume:** Removes/restores the beat entry without deleting it — paused tasks show amber badge; paused by / paused at shown in row tooltip; all pauses 2FA-gated (pausing nightly archival has data-growth consequences)
- **Run Now:** Triggers a manual immediate execution — confirmation modal with "This will run `{task}` immediately in queue `{queue}`. Confirm?" — no 2FA needed for Run Now
- **View History:** Opens `scheduled-job-drawer` showing last 30 runs: run start · duration · status · output summary · error (if failed)

**Task detail drawer (scheduled-job-drawer):**
- Schedule config: current cron expression + human-readable interpretation + "Edit Schedule" (Admin + DevOps only)
- Last 30 runs timeline: bar chart (duration) with colour (green/red) + table below
- Error log: full traceback for failed runs (last 5 failures shown)
- Queue depth at time of run (from C-08 Celery queue metrics)

**Data Source:** Django-Celery-Beat `PeriodicTask` model (ORM query — no Redis needed; beat schedule stored in DB with `select_related` on `ClockedSchedule` / `CrontabSchedule` / `IntervalSchedule`). Last run metadata from Celery task result backend (stored in `platform_celery_task_results` table, not Redis).

**Data Model Addition — platform_celery_task_results:**

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| task_name | VARCHAR(255) | dotted path |
| celery_task_id | VARCHAR(255) | |
| queue | VARCHAR(100) | |
| started_at | TIMESTAMPTZ | |
| completed_at | TIMESTAMPTZ | nullable |
| status | ENUM | success/failure/partial/running |
| duration_seconds | FLOAT | nullable |
| error_message | TEXT | nullable |
| triggered_by | ENUM | beat_schedule / manual_run / deployment |
| triggered_by_staff | UUID FK | nullable (for manual runs) |
