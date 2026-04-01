# C-09 — CI/CD Pipeline Manager

> **Route:** `/engineering/cicd/`
> **Division:** C — Engineering
> **Primary Role:** Platform Admin (Role 10) · DevOps/SRE (Role 14)
> **Read Access:** Backend Engineer (Role 11) · Frontend Engineer (Role 12) · Mobile Engineer (Role 13) · AI/ML Engineer (Role 17)
> **File:** `c-09-cicd.md`
> **Priority:** P0 — Required before first production deployment
> **Status:** ✅ Spec done

---

## 1. Page Name & Route

**Page Name:** CI/CD Pipeline Manager
**Route:** `/engineering/cicd/`
**Part-load routes:**
- `/engineering/cicd/?part=kpi` — pipeline health KPI
- `/engineering/cicd/?part=runs` — pipeline run list
- `/engineering/cicd/?part=drawer&run_id={id}` — pipeline run detail drawer
- `/engineering/cicd/?part=grid` — parallel pipeline grid view
- `/engineering/cicd/?part=dora` — DORA metrics panel
- `/engineering/cicd/?part=approval-queue` — production deployment approval queue

---

## 2. Purpose (Business Objective)

The CI/CD Pipeline Manager is the unified view of all GitHub Actions workflows across all 12 platform repositories. Every code change follows the same path: Test → Lint → Build → Deploy Staging → QA Gate → Pre-Prod → Prod — and each step is visible, traceable, and controllable from this page.

The production deployment stage requires a manual approval gate. No code reaches production without a human clicking "Approve" in the approval queue on this page. This creates a clear ceremony around production releases and prevents accidental auto-deploys.

DORA metrics on this page give engineering leadership visibility into deployment frequency, change failure rate, lead time, and MTTR — the four metrics that define elite engineering performance.

**Business goals:**
- Unified multi-repo pipeline visibility (12 repos on one page)
- Manual approval gate for all production deployments
- Failed pipeline instant diagnosis: failed step, log, and rollback suggestion
- Integration with QA sign-off (C-11 / Div B page 21) and Release Manager (Div B page 03)
- DORA metrics tracking for engineering excellence programme

---

## 3. User Roles

| Role | Access Level | Permissions |
|---|---|---|
| Platform Admin (10) | Level 5 | Full: view · approve · reject · cancel · re-run · configure |
| DevOps / SRE (14) | Level 4 | Full: view · approve · reject · cancel · re-run · configure |
| Backend Engineer (11) | Level 4 — Read | View all pipeline runs; re-run own failed pipelines |
| Frontend Engineer (12) | Level 4 — Read | View; re-run own frontend pipeline failures |
| Mobile Engineer (13) | Level 4 — Read | View mobile repo pipelines; re-run mobile failures |
| AI/ML Engineer (17) | Level 4 — Read | View AI pipeline runs |

---

## 4. Section-Wise Detailed Breakdown

---

### Section 1 — Page Header & Pipeline Status

**Purpose:** Immediately show if any production deployment is waiting for approval or if a critical pipeline is failing.

**Header elements:**
- H1 "CI/CD Pipeline Manager"
- "Approval Queue" badge: "2 deployments awaiting approval" (amber · click to jump to approval queue)
- Active runs counter: "8 pipelines running"
- "Run history" date range selector
- Repo filter tabs: All · portal · mobile · infra · content · ai-pipeline · auth · results · (scrollable)

**Critical Banners:**
- If main branch of any repo has failing pipeline: red banner "🚨 Main branch broken: {repo} — {step} failed"
- If approval queue has items > 4h old: amber banner "Deployment approval pending for > 4 hours. Review now."

---

### Section 2 — KPI Strip — Pipeline Health

**KPI Cards:**

| Card | Metric | Alert |
|---|---|---|
| Pipelines Running | Count of active runs | — |
| Success Rate (24h) | % successful runs in last 24h | < 80% amber |
| Avg Build Time (24h) | Mean duration across all pipelines | > 120% of 7-day avg = amber |
| Failed Pipelines (24h) | Count of failures | > 5 = amber |
| Pending Approvals | Count in approval queue | > 0 = amber (requires action) |
| Deployments to Prod (today) | Count of successful prod deployments | — (DORA: deployment frequency) |

---

### Section 3 — Parallel Pipeline Grid View

**Purpose:** Visual overview of all 12 repos' current pipeline state — which are running, passing, or failing simultaneously.

**Layout:** 12 repo cards in a 4×3 or 6×2 grid

**Each Repo Card shows:**
- Repo name + icon
- Branch being built (main / release/x.x / hotfix/x)
- Current pipeline status: ✅ Passing · ❌ Failing · 🔄 Running · ⏸ Waiting Approval · ⬜ No recent activity
- Current stage (if running): e.g., "Running: Unit Tests"
- Last run: relative time
- Duration of current run
- Last committer name + commit message (truncated at 80 chars)

**Click a card:** jumps to filtered pipeline run list for that repo

**Data Flow:**
- Grid state: GitHub Actions API `GET /repos/{owner}/{repo}/actions/runs?per_page=1` for each of 12 repos (12 concurrent API calls)
- Cached in Memcached 30s
- HTMX poll 30s

---

### Section 4 — Pipeline Run List Table

**Purpose:** All pipeline runs across all repos (or filtered by repo/branch/status).

**Table Columns:**

| Column | Description | Sortable |
|---|---|---|
| Status | ✅ · ❌ · 🔄 · ⏸ · 🚫 | ✅ |
| Repo | Repository name | ✅ |
| Branch | Git branch name | ✅ |
| Commit | Short SHA + message (truncated) | — |
| Author | Committer name | — |
| Pipeline | Workflow file name | — |
| Stage | Current / last completed stage | — |
| Duration | HH:MM:SS | ✅ |
| Started | Relative timestamp | ✅ |
| Actions | Re-run · Cancel · View logs · Approve (if pending) | — |

**Filter Bar:**
- Repo: multi-select (12 repos)
- Branch: main / release/* / hotfix/* / develop / feature/* / All
- Status: All / Success / Failed / Running / Waiting Approval / Cancelled
- Author: engineer name
- Date range
- Stage: failed at (dropdown of all pipeline stages)

**Pagination:** 50 runs per page · newest first

**Failed run row:** red left border + "Re-run" button highlighted

**Waiting Approval row:** amber left border + "Review & Approve" button

---

### Section 5 — Pipeline Run Detail Drawer

**Purpose:** Full stage-by-stage breakdown, log access, and approval actions for a single pipeline run.

**Drawer Width:** 720px
**Tabs:**

---

#### Tab 1 — Stages

**Purpose:** Step-by-step pipeline stage view with timing and status.

**Standard Pipeline Stages:**

| Stage | Description | Typical Duration |
|---|---|---|
| Checkout | Git checkout + cache restore | 15–45s |
| Unit Tests | pytest / jest / flutter test | 2–8 min |
| Lint | flake8 / eslint / dart analyze | 30–90s |
| Type Check | mypy / TypeScript tsc | 1–3 min |
| Build | Docker build / Flutter build / webpack | 5–15 min |
| Security Scan | pip-audit / npm audit / Snyk | 1–3 min |
| Deploy Staging | Lambda update / ECS deploy | 2–5 min |
| Integration Tests | API tests against staging | 5–15 min |
| QA Gate | Check QA sign-off status (Div B page 21) | Manual (0s to 24h) |
| Pre-Prod Deploy | Deploy to pre-prod environment | 2–5 min |
| Prod Approval | Manual approval gate | Manual (0s to 24h) |
| Prod Deploy | Production Lambda/ECS deploy | 2–5 min |
| Post-Deploy Health | Automated health checks (C-05) | 5–15 min |

**Visual representation:**
- Horizontal stepper for stages
- Each stage: icon (✅/❌/🔄/⏸) + name + duration
- Current stage: pulsing blue border
- Failed stage: red border + error badge
- Skipped stages (after failure): grey

**Failed Stage Detail:**
- Expands to show: error message · failed command · exit code · log snippet (last 20 lines)
- "View full logs" link → Logs tab filtered to failed stage

---

#### Tab 2 — Logs

**Purpose:** Full GitHub Actions log for this pipeline run.

**Layout:**
- Stage selector dropdown (jump to stage's log section)
- ANSI-rendered log output (colours preserved)
- Search within logs (client-side text search)
- "Download full log" button
- Log auto-scrolls to first ERROR line on open

**Log retention:**
- Live runs: logs streamed from GitHub Actions API (30s poll)
- Completed runs: logs fetched from GitHub Actions and stored in S3 (90-day retention)
- Runs > 90 days: S3-only (archived; still accessible but slower load)

---

#### Tab 3 — Artifacts

**Purpose:** Build artifacts produced by this pipeline run.

**Artifact Table:**

| Name | Type | Size | Retention | Download |
|---|---|---|---|---|
| lambda-exam-service.zip | Lambda deployment package | 24.3 MB | 30 days | ⬇ |
| test-coverage-report.html | HTML report | 1.2 MB | 30 days | ⬇ |
| docker-manifest.json | Docker image manifest | 4 KB | 90 days | ⬇ |
| security-scan-results.json | pip-audit + Snyk output | 28 KB | 90 days | ⬇ |

**Download:** Presigned S3 URL (1-hour expiry) — artifacts stored in `platform-cicd-artifacts` S3 bucket

---

#### Tab 4 — Approvals

**Purpose:** Manage the manual approval gate for production deployment.

**Approval Status:**

| Gate | Status | Reviewer | Reviewed At | Notes |
|---|---|---|---|---|
| QA Sign-off | ✅ Approved | Anita QA Lead | 2h ago | 847 tests passed · 0 failures |
| Security Scan | ✅ Passed (auto) | Automated | 2h ago | No critical CVEs |
| Pre-Prod Smoke Test | ✅ Passed (auto) | Automated | 1h ago | All 5 checks passed |
| Production Approval | ⏳ Awaiting | — | — | — |

**Production Approval Actions (Admin · DevOps):**
- "Approve" button → confirmation modal (shows what will be deployed: repo · branch · commit · diff summary)
- "Reject" button → reason field (required) → pipeline marked as rejected; author notified via email
- "Request changes" → free text note sent to pipeline author; pipeline paused

**Approve confirmation modal shows:**
- Repo + branch + commit SHA + author
- Files changed: count + link to GitHub diff
- Related release ticket: if linked via commit message `[Release #42]`
- Time since pipeline started (age of the build being promoted)

**Automatic approval bypass (configurable per repo):**
- Hotfix branches (`hotfix/*`): can be configured to auto-approve after automated checks pass (Admin configures this in alert rules; requires explicit opt-in)
- Feature branches to staging: no approval gate (only production has manual gate)

---

### Section 6 — Production Approval Queue

**Purpose:** Dedicated view of all pipeline runs currently waiting for production deployment approval.

**Access:** Visible at top of page when pending approvals > 0; also accessible via sidebar navigation

**Queue Table:**

| Repo | Branch | Commit | Author | Waiting Since | QA Status | Security | Actions |
|---|---|---|---|---|---|---|---|
| portal | release/3.8.1 | `abc123` "Add exam timer UI" | Priya | 2h 14m | ✅ | ✅ | Approve · Reject |
| auth-service | main | `def456` "Fix token refresh" | Rohan | 47m | ✅ | ✅ | Approve · Reject |

**SLA:** Approval queue items older than 4h trigger amber banner and daily digest email to Admin/DevOps team

**Batch approve:** "Approve All" button (2FA required for batch; individual approvals do not require 2FA but are logged)

---

### Section 7 — DORA Metrics Panel

**Purpose:** Track engineering delivery performance using the four DORA (DevOps Research and Assessment) metrics.

**Time range selector:** Last 7 days · Last 30 days · Last 90 days

**DORA Metrics Cards:**

| Metric | Value | DORA Level | Trend |
|---|---|---|---|
| Deployment Frequency | 4.2 deploys/day | Elite (> 1/day) | ↑ +12% |
| Lead Time for Changes | 2.4 hours | Elite (< 1 day) | ↑ better |
| Change Failure Rate | 3.1% | High (5–15%) | ↓ improving |
| MTTR (Mean Time to Restore) | 38 min | Elite (< 1 hour) | → stable |

**DORA Level definitions shown as tooltips:**
- Elite: Deployment frequency > 1/day; Lead time < 1 day; CFR < 5%; MTTR < 1h
- High: DFq > 1/week; LT < 1 week; CFR 5–15%; MTTR < 24h
- Medium: DFq > 1/month; LT < 1 month; CFR 15–30%; MTTR < 1 week
- Low: DFq < 1/month; LT > 1 month; CFR > 30%; MTTR > 1 week

**Charts (time-series):**
- Deployment frequency: bar chart (deploys per day, last 30 days)
- Lead time: box plot showing distribution (min · median · P90 · max)
- Change failure rate: line chart (% rollbacks + hotfixes / total deploys)
- MTTR: scatter plot (individual incident restoration times)

**Per-repo DORA table:**

| Repo | Dep. Freq. | Lead Time | CFR | MTTR |
|---|---|---|---|---|
| portal | 2.1/day | 1.8h | 2.4% | 22 min |
| auth-service | 0.8/day | 3.2h | 5.1% | 55 min |
| mobile | 0.3/day | 8.4h | 1.2% | 45 min |

**Data sources:**
- Deployment frequency: count of successful prod deployments from `platform_deployment_log` (C-05)
- Lead time: time from first commit on branch to prod deployment
- CFR: count of rollbacks + hotfixes / total deployments (from `platform_deployment_log`)
- MTTR: from C-18 incident resolution times (incident created at detection → resolved)

---

### Section 8 — Pipeline Configuration

**Purpose:** Manage pipeline settings, notification rules, and integration points.

**Repo Settings Table:**

| Repo | Default Branch | Protected Branches | Required Reviewers | Auto-Deploy Staging | Approval Gate | Slack Notify Channel |
|---|---|---|---|---|---|---|
| portal | main | main · release/* | 1 | ✅ | ✅ | #deploy-portal |
| auth-service | main | main | 1 | ✅ | ✅ | #deploy-backend |
| mobile | main | main · release/* | 2 | ❌ | ✅ | #deploy-mobile |

**Edit settings (Admin · DevOps):**
- Toggle auto-deploy to staging
- Toggle approval gate (cannot disable for repos containing exam-critical services)
- Set required reviewer count
- Set Slack/email notification channel

**Pipeline health alert rules:**
- "Notify on main branch failure": always ON for all repos (cannot disable)
- "Notify on approval queue > 4h": configurable (default: ON)
- "Page on-call for exam-critical service failure": configurable per repo

---

## 5. User Flow

### Flow A — Reviewing and Approving a Production Deployment

1. DevOps receives email: "portal v3.8.1 awaiting production approval (1h 20m)"
2. Opens `/engineering/cicd/` → Approval Queue shows portal release/3.8.1
3. Clicks "Review & Approve" → drawer opens → Approvals tab
4. Reviews: QA sign-off ✅ · Security scan ✅ · Pre-prod smoke test ✅
5. Clicks "View GitHub diff" → reviews file changes in new tab
6. Returns → confirms no concerns → clicks "Approve"
7. Confirmation modal: "Deploy portal release/3.8.1 (commit abc123) to production?"
8. Clicks "Confirm" → pipeline resumes → Prod Deploy stage starts
9. Stage status updates: Prod Deploy ✅ (3 min) → Post-Deploy Health ✅
10. DORA metrics updated: deployment count +1

### Flow B — Diagnosing a Failed Pipeline

1. Red banner: "🚨 Main branch broken: auth-service — Unit Tests failed"
2. Opens auth-service pipeline run → Stages tab
3. Failed stage: "Unit Tests" — error: "ModuleNotFoundError: No module named 'jwt'"
4. Switches to Logs tab → filtered to Unit Tests stage
5. Log shows: dependency install step succeeded but wrong version installed
6. Backend Engineer notified via Slack (#deploy-backend)
7. Engineer fixes dependency pinning → pushes commit → new pipeline starts
8. New pipeline: all stages pass → awaits approval

### Flow C — DORA Metrics Review (Monthly Engineering Meeting)

1. Engineering lead opens `/engineering/cicd/` → DORA Metrics panel
2. Time range: Last 30 days
3. Deployment frequency: 3.8/day (Elite ✅)
4. Lead time: 2.8h (Elite ✅)
5. Change failure rate: 7.2% (High — not yet Elite) → investigates CFR chart
6. Identifies: auth-service has 5 rollbacks in 30 days → discusses with Backend team
7. MTTR: 45 min (Elite ✅) — team is recovering well when things fail
8. Sets goal: reduce auth-service CFR to < 5% next month

---

## 6. Component Structure (Logical)

```
CICDPipelineManagerPage
├── PageHeader
│   ├── PageTitle
│   ├── ApprovalQueueBadge
│   ├── ActiveRunsCounter
│   ├── RepoFilterTabs
│   └── CriticalBanners
├── KPIStrip × 6
├── ParallelPipelineGrid
│   └── RepoCard × 12
├── FilterBar
├── PipelineRunTable
│   └── PipelineRunRow × N
│       └── (all columns + inline actions)
├── PipelineRunDrawer (720px)
│   └── DrawerTabs
│       ├── StagesTab (stepper)
│       ├── LogsTab
│       ├── ArtifactsTab
│       └── ApprovalsTab
├── ProductionApprovalQueue
│   ├── QueueTable
│   └── BatchApproveButton
├── DORAPIPanel
│   ├── MetricCards × 4
│   ├── Charts × 4
│   └── PerRepoDoraTable
└── PipelineConfigSection
    └── RepoSettingsTable
```

---

## 7. Data Model (High-Level)

### platform_cicd_runs (synced from GitHub Actions webhooks)

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| github_run_id | BIGINT | unique |
| repo | VARCHAR(100) | |
| branch | VARCHAR(200) | |
| commit_sha | CHAR(40) | |
| commit_message | TEXT | |
| author | VARCHAR(100) | |
| workflow_name | VARCHAR(200) | |
| status | ENUM | queued/in_progress/completed/waiting_approval |
| conclusion | ENUM | success/failure/cancelled/skipped/null (if running) |
| current_stage | VARCHAR(100) | |
| duration_seconds | INTEGER | nullable |
| started_at | TIMESTAMPTZ | |
| completed_at | TIMESTAMPTZ | nullable |
| artifacts_json | JSONB | list of artifact names/sizes |

### platform_cicd_approvals

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| cicd_run_id | UUID FK | |
| gate_name | VARCHAR(100) | e.g., `production`, `qa_sign_off` |
| status | ENUM | pending/approved/rejected/bypassed |
| reviewer_id | UUID FK → platform_staff | nullable |
| reviewed_at | TIMESTAMPTZ | nullable |
| notes | TEXT | nullable |
| created_at | TIMESTAMPTZ | |

---

## 8. Validation Rules

| Rule | Detail |
|---|---|
| Production approval | Cannot approve own pipeline (committer cannot be sole approver) |
| Approval gate bypass | Only `hotfix/*` branches can be configured for auto-approval; requires Admin to enable; logged |
| Batch approve | 2FA required for batch approval of > 3 pipelines simultaneously |
| Re-run | Can only re-run from the last failed stage (not full restart by default); full restart available as separate option |
| Pipeline age | Warning if approving a pipeline run that is > 48h old: "This build is 52 hours old. Code may have drifted from current main. Consider re-running." |
| Exam-critical repo approval gate | Cannot disable approval gate for repos tagged as `exam-critical` (portal, auth-service, exam-service) |

---

## 9. Security Considerations

| Control | Detail |
|---|---|
| GitHub Actions webhook validation | Webhook payloads validated via HMAC-SHA256 signature (GitHub `X-Hub-Signature-256` header) |
| Approval cannot be self-served | Committer cannot approve their own pipeline run; enforced server-side |
| Artifact download | Presigned S3 URLs (1-hour expiry); artifacts stored in private bucket; no public access |
| GitHub PAT scope | GitHub Personal Access Token used by platform has minimum scope: `repo:read`, `actions:read`, `actions:write` (for re-run); no write to repo content |
| Pipeline log sensitive data | GitHub Actions automatically masks secrets in logs; additional platform-side masking applied for known patterns (JWT regex, API key patterns) |
| DORA metrics data | Derived from internal platform tables; no external data source required |

---

## 10. Edge Cases (System-Level)

| Scenario | Handling |
|---|---|
| GitHub API rate limit | GitHub API: 5,000 req/hour authenticated; 12 repos × polling = 24 req/min = well within limit; Memcached 30s cache prevents excess calls |
| GitHub itself down | Cached last-known status shown with "GitHub data unavailable" amber banner; approval queue still functional (stored in platform DB) |
| Approval queue item expires (pipeline auto-cancelled by GitHub after 72h) | Platform marks approval as "expired"; logs entry; author notified to re-run pipeline |
| Two engineers approve same pending deployment simultaneously | First approval succeeds; second returns "Already approved" notice; duplicate approval logged |
| Exam-critical pipeline fails on main branch | Auto-creates P0 incident in C-18; pages on-call DevOps; deployment to prod blocked until fixed |
| Pipeline stuck in "Running" for > 2h | Auto-timeout rule: Celery beat marks pipeline as `timeout` after 3h; admin and author notified; manual cancel available |
| Deployment to prod during active exam | Pre-deploy check: if `platform:active_exam_count > 0` → amber warning in approval modal: "Exam in progress. Production deployment during live exam is high risk." → Admin must explicitly confirm |

---

## 11. Performance & Scaling Strategy

| Concern | Strategy |
|---|---|
| 12 repo status polling | 12 parallel GitHub API calls (async); results cached Memcached 30s; total fetch < 500ms |
| Pipeline run table | 50 rows per page; index on `repo + started_at + status`; < 50ms query |
| Live stage updates (running pipelines) | GitHub Actions API polled every 30s; running stage status stored in Memcached with 35s TTL |
| DORA metrics calculation | Pre-computed nightly by Celery beat; stored in `platform_dora_snapshots` table; page load reads from snapshot (< 10ms) |
| Log streaming | GitHub Actions log endpoint streams chunked response; 30s poll for running; one-time fetch for completed |
| Approval queue | Always < 20 items (small team); no pagination needed; in-memory sort |
| Grid view card state | 12 cards × single-field status — lightweight; full refresh < 200ms |
