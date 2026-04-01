# Page 26 — Automation Monitor

**URL:** `/portal/product/automation-monitor/`
**Permission:** `product.view_automation_monitor`
**Priority:** P2
**Roles:** QA Engineer, PM Platform

---

## Purpose

Real-time visibility into the complete CI/CD automation pipeline — from code commit through build, automated test execution, deployment, and post-deploy health verification. Gives QA engineers and PMs a unified view of pipeline health, test automation performance, deployment status across all environments, and infrastructure metrics immediately after each deployment. Connects with the QA Dashboard (page 21), Release Manager (page 03), and Performance Test Dashboard (page 24).

Core responsibilities:
- Monitor all CI/CD pipeline runs in real time (auto-refresh every 30 seconds)
- Track automated test execution within pipeline stages
- Alert on pipeline failures, test regressions, and deployment anomalies
- Measure automation coverage (% of code changes validated automatically before merge)
- Manage scheduled jobs: nightly regression, hourly smoke tests, weekly performance baseline
- Detect build time regressions (pipeline getting slower over time)
- Track flaky pipeline steps distinct from flaky tests
- Post-deploy infrastructure monitoring: CPU, memory, error rate correlated with deploy events
- Provide a deployment impact view: did this deploy cause any degradation?

**Scale:**
- 20–50 pipeline runs per day across feature branches, staging, UAT, pre-production
- 12,000+ automated tests per full regression run
- 4 test environments: Dev · Staging · UAT · Pre-Production
- Pipeline stack: GitHub Actions · Django test runner (Pytest) · Selenium/Playwright (E2E) · Locust (performance) · Docker build

---

## Page Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  "Automation Monitor"           Environment ▾  [Trigger Pipeline]│
├─────────────────────────────────────────────────────────────────┤
│  KPI Strip — 6 cards (auto-refresh every 30s)                   │
├─────────────────────────────────────────────────────────────────┤
│  Tab Bar:                                                       │
│  Live Pipelines · Pipeline History · Scheduled Jobs             │
│  Code Coverage · Alert Rules · Infrastructure · Audit Log       │
├─────────────────────────────────────────────────────────────────┤
│  [Active Tab Content]                                           │
└─────────────────────────────────────────────────────────────────┘
```

---

## KPI Strip — 6 Cards (auto-refresh every 30s)

| # | Label | Value | Colour | Delta | Click Action |
|---|---|---|---|---|---|
| 1 | Active Pipelines | Pipelines currently running | Blue > 0 | — | Opens Live Pipelines |
| 2 | Last Pipeline Status | Pass/Fail badge of most recently completed | Green/Red | — | Opens that run's detail |
| 3 | Pass Rate (7d) | % of pipeline runs that passed in last 7 days | Green ≥90% · Amber 80% · Red <80% | vs prev 7d | Opens Pipeline History |
| 4 | Avg Build Time (7d) | Mean total pipeline duration | Green if improving | vs prev 7d | Opens Pipeline History |
| 5 | Failed Scheduled Jobs (24h) | Scheduled jobs that failed in last 24 hours | Red > 0 | — | Opens Scheduled Jobs |
| 6 | Code Coverage | % of codebase covered by automated tests | — | vs last week | Opens Code Coverage |

---

## Tab 1 — Live Pipelines

Real-time view of running and recently completed pipeline runs. Auto-refresh every 10 seconds when pipelines are running; every 60 seconds otherwise.

### Running Pipelines Panel

For each running pipeline, a full card:

**Card layout:**
```
[Pipeline Name]                              [Abort]  [View Details]
Branch: feature/exam-v2  |  Commit: a3f9c2d  |  Triggered by: Arjun Kumar (Push)
Started: 14:32:01  |  Elapsed: 00:08:42  |  Est. remaining: ~20 min

Stage Progress:
[✓ Lint 2m] → [✓ Unit Tests 3m] → [✓ Integration 8m] → [⟳ Build Docker ~4m] → [○ Deploy] → [○ Smoke] → [○ E2E]

Overall: ▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░ 45% complete
```

**Stage icons:**
- ✓ Passed (green, with duration)
- ✗ Failed (red, with duration)
- ⟳ Running (animated spinner, with elapsed)
- ○ Pending (grey)
- ⊘ Skipped (grey, dashed border)

**Abort button:** Opens confirmation: "Abort this pipeline run? Any deployed changes will not be automatically rolled back."

**When no pipelines running:**
- Green banner: "No active pipelines. All systems idle."
- Auto-refresh continues but at 60s interval

### Recently Completed (last 10)

Compact table below running pipelines:

| Pipeline ID | Branch | Status | Duration | Completed | Triggered By | Failed Stage | Actions |
|---|---|---|---|---|---|---|---|
| PL-2026-03-20-012 | main | ✓ Passed | 28m 14s | 2h ago | CI (PR #492 merge) | — | View · Re-run |
| PL-2026-03-20-011 | feature/exam-v2 | ✗ Failed | 8m 02s | 4h ago | Push (Deepa Menon) | E2E Tests | View · Re-run |
| PL-2026-03-19-008 | v4.2.1-rc2 | ✓ Passed | 31m 45s | Yesterday | Release pipeline | — | View |

---

## Tab 2 — Pipeline History

Full searchable history of all pipeline runs.

### Toolbar

| Control | Options |
|---|---|
| Search | Branch name, commit hash, pipeline ID |
| Status | All / Passed / Failed / Aborted / Running |
| Environment / Branch type | All / main / staging-deploy / UAT / feature branches |
| Trigger | All / Git Push / Pull Request / Scheduled / Manual |
| Date range | Start date range picker |

### Pipeline History Table — 11 columns

| Column | Detail |
|---|---|
| Pipeline ID | Auto-generated (PL-YYYY-MM-DD-NNN) |
| Branch | Git branch name |
| Commit | Short hash + first 50 chars of commit message |
| Triggered By | User avatar + name + trigger type badge |
| Environment | Badge |
| Status | Passed (green) · Failed (red) · Aborted (grey) · Running (spinner) |
| Started | Timestamp |
| Duration | HH:MM:SS |
| Tests | Passed/Total count (e.g. 11,998/12,000) |
| Failed Stage | Stage name if failed, "—" if passed |
| Actions | View Details · Re-run · Copy ID |

**Pagination:** Showing X–Y of Z runs · page pills · per-page selector (25 / 50 / 100)

### Pipeline Detail Drawer (840px)

**Header:**
Pipeline ID · Branch · Commit hash (linked to GitHub) · Status badge · Started/Ended · Duration

**Drawer Tab 1 — Stage Breakdown:**

| Stage | Status | Started | Duration | Parallel Jobs | Retried | Actions |
|---|---|---|---|---|---|---|
| Lint & Code Style | ✓ Passed | 14:32:01 | 0:02:14 | 1 | No | View Logs |
| Unit Tests | ✓ Passed | 14:34:15 | 0:03:45 | 4 parallel | No | View Results |
| Integration Tests | ✓ Passed | 14:38:00 | 0:08:12 | 2 parallel | No | View Results |
| Build Docker Image | ✓ Passed | 14:46:12 | 0:04:30 | 1 | No | View Logs |
| Push to Registry | ✓ Passed | 14:50:42 | 0:01:10 | 1 | No | View Logs |
| Deploy to Staging | ✓ Passed | 14:51:52 | 0:02:30 | 1 | No | View Logs |
| DB Migrations | ✓ Passed | 14:54:22 | 0:01:15 | 1 | No | View Logs |
| Smoke Tests | ✓ Passed | 14:55:37 | 0:05:30 | 1 | No | View Results |
| E2E Tests | ✗ Failed | 14:59:37 | 0:08:23 | 3 parallel | Yes (1x) | View Results |
| Performance Check | ⊘ Skipped | — | — | — | — | — |

**Stage Duration Bar Chart** (below table): Horizontal bars showing relative duration of each stage. Longest bars immediately visible. "Linting took 2m; E2E took 8m" at a glance.

**Drawer Tab 2 — Test Results:**

**Test Suite Summary:**

| Suite | Tests Run | Passed | Failed | Skipped | Duration | Pass Rate |
|---|---|---|---|---|---|---|
| Unit Tests | 3,240 | 3,238 | 2 | 0 | 3m 45s | 99.9% |
| Integration Tests | 1,820 | 1,819 | 1 | 0 | 8m 12s | 99.9% |
| Smoke Tests | 80 | 80 | 0 | 0 | 5m 30s | 100% |
| E2E Tests (partial—aborted on failure) | 420 | 398 | 22 | 0 | 8m 23s | 94.8% |
| **Total** | **5,560** | **5,535** | **25** | **0** | **25m 50s** | **99.6%** |

**Failed Tests List:**

| Test Name | Suite | Failure Message (first line) | Duration | Known Flaky | Actions |
|---|---|---|---|---|---|
| test_exam_submit_result_page_load | E2E | TimeoutError: result page took 8.4s (threshold: 3s) | 12s | No | View Logs |
| test_leaderboard_ordering_after_submit | E2E | AssertionError: rank 1 shows incorrect student after tie | 8s | Yes | View Logs |

"Create Defect from Failure" button on each failed test row → pre-fills New Defect form (page 25) with test name, failure message, and pipeline link.

**Drawer Tab 3 — Raw Logs:**

Stage selector dropdown → shows full raw log for selected stage.
- Monospace font
- Error lines highlighted red · Warning lines highlighted amber · Success lines highlighted green
- Search within log (Ctrl+F equivalent)
- "Jump to first error" button
- Download full log as `.txt`
- Line count shown in footer

**Drawer Tab 4 — Deployment Details:**

Shown only if pipeline included a deployment step.

| Field | Value |
|---|---|
| Deployed To | Staging environment |
| Deployment Started | 14:51:52 |
| Deployment Completed | 14:54:22 |
| Duration | 2m 30s |
| Previous Version | v4.2.0-staging |
| New Version | v4.2.1-staging |
| Migrations Applied | 2 migrations |
| Migration Names | 0048_add_exam_pattern_section_order.py · 0049_alter_testseriesexam_order.py |
| Rollback Available | Yes — v4.2.0-staging snapshot retained for 7 days |
| Post-deploy Smoke | ✓ Passed (80/80 tests, 5m 30s) |

**Drawer Tab 5 — Artifacts:**

Files generated by this pipeline run:

| Artifact | Size | Generated At | Download |
|---|---|---|---|
| Unit test results (JUnit XML) | 48 KB | 14:38:00 | Download |
| Integration test results (HTML) | 1.2 MB | 14:46:12 | Download |
| E2E test results (HTML + screenshots) | 8.4 MB | 15:07:00 | Download |
| Docker image digest | — | 14:50:42 | Copy digest |
| Code coverage report (HTML) | 2.1 MB | 14:46:12 | Download |
| Lint report (JSON) | 18 KB | 14:34:15 | Download |

---

## Tab 3 — Scheduled Jobs

All automation jobs running on a schedule. Independent of PR-triggered pipelines.

### Scheduled Jobs Table

| Job Name | Schedule (IST) | Description | Last Run | Last Status | Next Run | Duration | Actions |
|---|---|---|---|---|---|---|---|
| Hourly Smoke — Staging | Every 1h | 80-test smoke on staging | 1h ago | ✓ Passed | 0h 58m | ~6m | Run Now · Pause · Edit |
| Nightly Full Regression | Daily 1:00am | Complete 12K test suite on staging | Yesterday | ✓ Passed | Tonight 1:00am | ~35m | Run Now · Pause · Edit |
| Weekly Perf Baseline | Sunday 2:00am | Locust performance test vs stored baseline | 4 days ago | ✓ Passed | In 3 days | ~45m | Run Now · Pause · Edit |
| Daily DB Backup Verify | Daily 3:00am | Verify backup file integrity + restoration test | Yesterday | ✓ Passed | Tonight 3:00am | ~8m | Run Now · Pause · Edit |
| Weekly E2E on UAT | Friday 8:00pm | Full E2E on UAT environment | 3 days ago | ⚠ Warning | In 4 days | ~20m | Run Now · Pause · Edit |
| Daily Security Scan | Daily 4:00am | OWASP dependency + secrets scan | Yesterday | ✓ Passed | Tonight 4:00am | ~12m | Run Now · Pause · Edit |
| Hourly API Health Check | Every 1h | 20 critical API endpoints probed | 45m ago | ✓ Passed | 15m | ~2m | Run Now · Pause · Edit |
| Monthly SAST Scan | 1st of month | Static application security testing | 20 days ago | ✓ Passed | In 10 days | ~25m | Run Now · Pause · Edit |

**Status colours:** ✓ Passed (green) · ⚠ Warning (amber — tests passed but some skipped) · ✗ Failed (red) · ⊘ Paused (grey)

### Scheduled Job Detail Drawer (560px)

**Header:** Job name · Schedule expression · Status · Last 10-run pass rate

**Tab 1 — Configuration:**

| Setting | Value |
|---|---|
| Cron expression | `0 1 * * *` (with human-readable "Daily at 1:00am IST") |
| Target environment | Staging |
| Test suite | Full Regression (all 12,000 cases) |
| Parallel workers | 8 |
| Max runtime | 60 minutes (kill job if exceeded) |
| Retry on failure | 1 retry if infrastructure error (not test failure) |
| Notify on failure | Slack #qa-alerts + Deepa Menon email |
| Notify on recovery | Yes (when job passes after previous failure) |
| Active | Yes |

**Tab 2 — Run History:**

Last 30 runs table: Timestamp · Status · Duration · Pass rate · Failure reason (if any)

Pass rate trend chart: line chart of pass rate over last 30 runs. Downward trend = quality degradation.

**Tab 3 — Alerts Sent:**

History of all alerts sent for this job: timestamp · channel · message · acknowledged by · acknowledged at.

---

## Tab 4 — Code Coverage

Code coverage tracking. Updated after each full pipeline run that includes the test suite.

### Coverage Summary Cards

| Card | Value | Trend |
|---|---|---|
| Django Backend | % lines covered by tests | Arrow + delta vs last week |
| Flutter Mobile | % lines covered by tests | Arrow + delta |
| JavaScript Frontend | % lines covered by tests | Arrow + delta |
| Overall Combined | Weighted average | Arrow + delta |

**Minimum acceptable coverage:** 80% for all modules (configurable per module in settings section of this tab).

### Coverage Trend Chart

Line chart: overall code coverage % over last 30 pipeline runs. X-axis: run date. Y-axis: %. Reference line at 80% minimum threshold. Downward trend = uncovered code being added.

### Coverage by Module Table

| Module Path | Lines | Covered | Coverage % | vs Last Run | Threshold | Status |
|---|---|---|---|---|---|---|
| exam/models.py | 1,420 | 1,374 | 96.8% | ↑ 0.2% | 85% | ✓ |
| exam/views/ | 2,840 | 2,441 | 85.9% | → | 80% | ✓ |
| api/v1/ | 1,980 | 1,921 | 97.0% | ↑ 0.5% | 90% | ✓ |
| payments/ | 620 | 484 | 78.1% | ↓ 1.9% | 80% | ✗ |
| notifications/ | 480 | 326 | 67.9% | → | 70% | ✗ |
| mobile/flutter/ | 8,240 | 6,257 | 75.9% | ↑ 1.2% | 75% | ✓ |
| portal/views/product/ | 3,420 | 2,864 | 83.7% | → | 80% | ✓ |

Rows with coverage below threshold: red background.
Rows where coverage dropped vs last run: amber left border.

### Pull Request Coverage Gate

Every PR shows a coverage delta before merge is allowed:
- Coverage delta threshold: must not decrease by more than 2% vs main
- PRs breaching this threshold: blocked from merging until reviewed
- PM can configure threshold per module in Coverage Settings section

**Coverage Settings:**

| Module | Min Coverage % | Block PR if drops > | Exemptions |
|---|---|---|---|
| exam/ (critical) | 85% | 1% | None |
| api/ (critical) | 90% | 0.5% | None |
| payments/ | 80% | 2% | None |
| Other modules | 75% | 3% | Test-only files exempt |

---

## Tab 5 — Alert Rules

Rules that trigger notifications when pipeline or coverage thresholds are breached.

### Alert Rules Table

| Rule Name | Condition | Channels | Priority | Suppression | Active |
|---|---|---|---|---|---|
| Main branch pipeline failed | Main branch pipeline status = Failed | Slack #eng-critical + All PMs email | P0 | 15 min dedup | Yes |
| Nightly regression failed | Nightly job status = Failed | Slack #qa-alerts + QA team email | P1 | 30 min dedup | Yes |
| E2E failure rate > 5% | E2E tests failed > 5% in run | Slack #qa-alerts | P1 | 60 min | Yes |
| Coverage drops > 2% | Coverage regression in any module > 2% | PR comment + Slack #qa-alerts | P2 | Per-PR | Yes |
| Performance regression > 10% | P95 response time worsens > 10% vs baseline | Slack #platform-alerts + PM Platform email | P1 | 60 min | Yes |
| Staging smoke test failed | Staging hourly smoke = Failed | Slack #qa-alerts | P0 | 30 min | Yes |
| Scheduled job failed twice | Same scheduled job fails 2 consecutive runs | QA team email + Slack #qa-alerts | P1 | 4 hours | Yes |
| Build time increased > 25% | Pipeline duration > 125% of 7-day avg | Slack #platform-alerts | P2 | 4 hours | Yes |
| Security scan found critical | SAST scan severity = Critical | Slack #security + CTO email | P0 | None (always alert) | Yes |
| DB migration failed | Migration stage = Failed | Slack #eng-critical + DBA email | P0 | None | Yes |

### Alert Rule Edit Drawer (480px)

**Fields:**
- Rule name (max 80 chars)
- Trigger condition: metric selector + comparator + threshold value
- Alert message template (markdown, variables: `{{pipeline_id}}`, `{{branch}}`, `{{failure_reason}}`)
- Channels:
  - Slack channels (comma-separated, e.g. `#qa-alerts,#platform-alerts`)
  - Email addresses (comma-separated)
  - PagerDuty integration: Yes / No (for P0 rules)
- Priority: P0 / P1 / P2 / P3
- Suppression window: minutes after which a duplicate alert fires again (0 = always fire)
- Auto-resolve: Yes (send recovery notification when condition clears) / No
- Active toggle

---

## Tab 6 — Infrastructure

Post-deploy infrastructure monitoring. Shows how each deployment affected server health.

### Deployment Impact Timeline Chart

Full-width chart combining multiple metrics over a configurable time range (last 24h / 7d / 30d):

- **Top lane:** CPU utilisation % (all web servers average) — blue line
- **Second lane:** Memory utilisation % — purple line
- **Third lane:** HTTP 5xx error rate % — red line
- **Fourth lane:** P95 response time (ms) — amber line
- **Vertical markers:** Each deployment event drawn as a vertical dashed line labelled with version number

This chart answers: "Did the v4.2.1 deploy that happened at 3pm cause the CPU spike at 3:05pm?"

### Current Infrastructure Health Cards

4 environment cards (Dev / Staging / UAT / Pre-Production), each showing:

| Metric | Value | Colour |
|---|---|---|
| CPU (avg all servers) | 34% | Green < 60% · Amber 60–80% · Red > 80% |
| Memory (avg) | 58% | Same thresholds |
| DB connections | 148 / 400 max | Amber > 70% of max |
| Redis memory | 8.2 GB / 32 GB | Green |
| Gunicorn workers | 28 active / 32 total | |
| Celery queue | 12 pending tasks | Amber > 100 |
| Last deploy | v4.2.1 · 2h ago | |
| App status | ✓ Healthy | |

### Auto-scaling Event Log (last 7 days)

| Timestamp | Environment | Event | Resource | Scale | Trigger |
|---|---|---|---|---|---|
| 20 Mar 18:30 | Staging | Scale Up | Web servers | 4 → 6 instances | CPU > 70% for 2 min |
| 20 Mar 16:15 | Staging | Scale Down | Web servers | 6 → 4 instances | CPU < 40% for 5 min |
| 20 Mar 14:05 | Staging | Scale Up | Celery workers | 20 → 30 | Queue depth > 500 tasks |
| 19 Mar 21:00 | Staging | Scale Down | Celery workers | 30 → 20 | Queue depth < 50 for 5 min |

### Error Rate Trend

Line chart: HTTP 5xx error rate % per hour over last 7 days. Reference line at 1% alert threshold. Deployment markers overlay.

Clicking any spike on the error rate chart → opens the pipeline that deployed most recently before the spike, for correlation analysis.

---

## Tab 7 — Audit Log

Every change to pipeline configurations, scheduled jobs, and alert rules.

### Filters
- Date range
- Admin name
- Action: Pipeline Triggered Manually / Scheduled Job Paused / Alert Rule Modified / Coverage Threshold Changed / Job Config Updated

### Audit Table

| Timestamp | Admin | Action | Target | Change Summary |
|---|---|---|---|---|
| 20 Mar 09:15 | Deepa Menon | Alert Rule Modified | E2E failure rate rule | Threshold changed: 10% → 5% |
| 19 Mar 14:30 | Rahul Nair | Scheduled Job Paused | Weekly Perf Baseline | Paused during v4.2 release freeze |
| 18 Mar 11:00 | Deepa Menon | Pipeline Triggered | PL-2026-03-18-004 | Manual re-run, main branch, staging |
| 15 Mar 09:00 | Arjun Kumar | Coverage Threshold Changed | payments/ module | Min threshold: 75% → 80% |

Pagination: 25 / 50 / 100 per page. CSV export.

---

## "Trigger Pipeline" Modal

**Fields:**
- Branch: text input with autocomplete (recent branches + main)
- Environment: Staging / UAT / Pre-Production
- Pipeline type: Full (all stages) / Smoke only / E2E only / Custom (select stages)
- Skip stages: multi-select checkboxes (e.g. skip Performance Check for quick test)
- Notes (optional, logged in audit)

"Trigger" button → creates pipeline run and opens Live Pipelines tab showing the new run.

---

## Flaky Pipeline Steps Tracking

Distinct from flaky tests — these are pipeline infrastructure steps that fail intermittently (network timeouts, registry pull failures, ephemeral runner issues) rather than actual test failures.

### Flaky Step Summary Table

| Step Name | Flakiness Rate (30d) | Consecutive Failures | Avg Retry Delay | Root Cause Category | Status |
|---|---|---|---|---|---|
| Push to Registry | 4.2% | 0 | 8s | Docker Hub rate limit | Monitoring |
| Deploy to UAT | 2.1% | 0 | 15s | SSH timeout intermittent | Monitoring |
| DB Migrations (UAT) | 1.8% | 0 | — | Schema lock contention | Investigating |
| Selenium Grid Connect | 6.4% | 0 | 10s | Grid warm-up latency | Action Required |
| SAST Scan | 1.2% | 0 | 30s | External API rate limit | Monitoring |

**Flaky step threshold:** Any step with flakiness > 5% over 30 days triggers an auto-created investigation task on the responsible team's backlog.

**Distinct from flaky tests:** Flaky pipeline steps are infrastructure failures unrelated to code quality. They are tracked separately so engineers do not confuse infrastructure flakiness with test code quality issues.

---

## Build Time Regression Tracking

Pipeline duration creep is tracked to catch performance regressions in the build process itself — not just in the application.

### Build Time Trend Chart

Line chart: mean pipeline duration (minutes) per week over last 12 weeks. Separate lines for:
- Main branch pipelines (most stable, best baseline)
- Feature branch pipelines (expected variance)
- Scheduled nightly regressions

Reference bands:
- Green band: ±10% of 4-week rolling average (acceptable variance)
- Amber band: 10–25% above average (investigate)
- Red threshold line: 25% above average (alert fires)

### Stage-Level Duration Breakdown (last 30 days)

| Stage | Min | P50 | P90 | P95 | Max | 4-week Trend |
|---|---|---|---|---|---|---|
| Lint & Code Style | 1m 45s | 2m 10s | 2m 40s | 2m 55s | 4m 12s | → Stable |
| Unit Tests | 3m 00s | 3m 45s | 4m 30s | 5m 00s | 8m 20s | ↑ +12% — investigate |
| Integration Tests | 7m 00s | 8m 15s | 10m 30s | 11m 45s | 16m 00s | → Stable |
| Build Docker Image | 3m 30s | 4m 15s | 5m 30s | 6m 00s | 9m 45s | → Stable |
| E2E Tests | 18m 00s | 21m 30s | 26m 00s | 28m 30s | 38m 00s | ↑ +8% |
| Total Pipeline | 26m | 31m | 38m | 42m | 56m | ↑ +5% |

**Annotation:** When a stage P95 duration increases > 15% week-over-week, an amber flag appears next to that stage in the Pipeline Detail Drawer Stage Breakdown tab.

**Root cause hints displayed in the UI:**
- Slow unit tests: "New test count increased by 240 in this period. Review test isolation and database fixture overhead."
- Slow E2E: "E2E test count increased by 44. Consider parallelising further."

---

## Notification Rules

| Event | Recipients | Channel | Priority | Suppression |
|---|---|---|---|---|
| Main branch pipeline failed | All PMs + All QA + CTO (if 3rd consecutive failure) | Slack #eng-critical + Email | P0 | 15 min dedup |
| Staging smoke test failed | QA Engineer on duty | Slack #qa-alerts | P0 | 30 min |
| Nightly regression failed | QA team | Slack #qa-alerts + Email | P1 | 1 run (not 30-minute window) |
| E2E failure rate > 5% in a run | QA Engineer + PM Platform | Slack #qa-alerts | P1 | 60 min |
| Scheduled job failed twice consecutively | QA team | Email + Slack | P1 | 4h |
| Build time regressed > 25% | QA Engineer + Tech Lead | Slack #platform-alerts | P2 | 4h |
| Coverage dropped below module threshold | PR author + QA | GitHub PR comment + Slack | P2 | Per-PR |
| Security scan: critical finding | CTO + Security team | Slack #security + PagerDuty | P0 | Never suppress |
| DB migration failed | DBA + Tech Lead + PM Platform | Slack #eng-critical + PagerDuty | P0 | Never suppress |
| Flaky step threshold breached | QA Engineer | Slack #qa-alerts | P2 | Weekly digest |
| Pipeline recovered after failure | Previous alert recipients | Slack (recovery message) | Info | — |

---

## Integration Points

| Integration | Direction | Data Exchanged | Reference |
|---|---|---|---|
| QA Dashboard (page 21) | Bi-directional | Pipeline test results populate QA pass rates; QA override gate status blocks pipeline merge | Page 21 |
| Release Manager (page 03) | Consuming | Pipeline status gate controls release promotion; build version labels match release tags | Page 03 |
| Performance Test Dashboard (page 24) | Consuming | Weekly performance baseline job results flow into performance trend charts | Page 24 |
| Test Case Repository (page 23) | Consuming | Failed test IDs linked to test case records for traceability | Page 23 |
| Defect Tracker (page 25) | Producing | "Create Defect from Failure" populates defect with test name, failure, and pipeline link | Page 25 |
| GitHub (external) | Consuming | Commit hashes, PR status, branch names; pipeline run status written back to PR checks | External |
| PagerDuty (external) | Producing | P0 alerts for main branch failure, DB migration failure, security scan critical | External |
| Slack (external) | Producing | All alert rules send to configured Slack channels | External |

---

## Key Design Decisions

| Concern | Decision | Rationale |
|---|---|---|
| 30s KPI refresh | Shorter than most pages | CI/CD pipelines change state in seconds; near-real-time awareness is necessary |
| Stage duration bar chart | Visual in drawer | Longest stage is the optimization target; bar chart makes it obvious without reading numbers |
| Deployment impact timeline | Overlays deploys with metrics | The most common post-deploy question: "did this deploy cause problems?" — answered visually |
| "Create Defect from Failure" | Button in failed test list | Frictionless path from test failure to defect — prevents manual copy-paste errors |
| Code coverage module thresholds | Configurable per module | Critical modules (payments, exam) deserve higher minimum than utility modules |
| Alert suppression windows | Configurable per rule | A failing pipeline retrying 50 times should not spam 50 Slack messages |
| Security scan → CTO alert | Direct escalation | Critical security findings bypass engineering queue; immediate executive visibility |
| DB migration failure alert | P0 immediate | A failed migration can leave the database in a broken state; this is always a P0 |
| Recovery notifications | Optional per rule | When a failing pipeline recovers, teams need to know it's resolved — avoids checking manually |
| Flaky steps vs flaky tests | Separate tracking | Infrastructure flakiness (registry timeouts, SSH drops) is categorically different from test code quality — mixing them misleads the team on where to focus |
| Build time P95 tracking | P95 not mean | Mean can be dragged down by fast feature-branch runs; P95 of main branch runs shows the tail latency engineers actually wait through |
| Post-deploy correlation chart | Metrics overlaid with deploy markers | Reduces mean time to root cause; the correlation from deploy event to metric spike is visually immediate rather than requiring log cross-referencing |
| HTMX auto-refresh poll guard | No refresh during open drawer/modal | Prevents live data refreshing the underlying table while a detail drawer is open, which would disorient engineers mid-investigation |
