# Page 21 — QA Dashboard

**URL:** `/portal/product/qa-dashboard/`
**Permission:** `product.view_qa_dashboard`
**Priority:** P1
**Roles:** QA Engineer, PM Platform, PM Institution Portal

---

## Purpose

Central quality assurance operations hub for the SRAV platform. Provides the QA Engineering team with a unified view of test execution status, defect trends, release readiness, and test coverage across all platform surfaces (admin portal, institution portal, student portal, Flutter mobile app). Feeds directly into the Release Manager (page 03) through the QA Sign-off tab.

Core responsibilities:
- Track active test runs across all environments (staging, UAT, pre-production)
- Monitor test pass/fail rates and defect trends in real time
- Determine release readiness (green/amber/red gate per release)
- Manage test environment health
- Track regression suite coverage and flakiness rates
- Surface P0/P1 defect counts that block releases
- Provide QA sign-off workflow integrated with release management
- Export weekly and monthly QA health reports for management

**Scale:**
- 4 test environments (dev, staging, UAT, pre-production)
- 12,000+ test cases in the repository (page 23)
- 74K peak concurrent users — performance testing critical (page 24)
- Multiple releases per month with independent QA sign-off requirements
- Automated CI/CD test pipeline + manual exploratory testing
- Celery-orchestrated test run scheduling and notifications

---

## Page Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  "QA Dashboard"              Environment ▾  [Start Test Run]    │
├─────────────────────────────────────────────────────────────────┤
│  KPI Strip — 8 cards (auto-refresh every 60s)                   │
├─────────────────────────────────────────────────────────────────┤
│  Tab Bar:                                                       │
│  Overview · Test Runs · Release Gates · Defects                 │
│  Environments · Coverage · Automation Health                    │
├─────────────────────────────────────────────────────────────────┤
│  [Active Tab Content]                                           │
└─────────────────────────────────────────────────────────────────┘
```

---

## KPI Strip — 8 Cards (auto-refresh every 60s, poll paused during open drawer/modal)

| # | Label | Value | Colour | Delta | Click Action |
|---|---|---|---|---|---|
| 1 | Active Test Runs | Running test runs right now | Blue if > 0 | — | Opens Test Runs tab |
| 2 | Pass Rate (Last Run) | % of tests passed in most recent run | Green ≥95% · Amber 80–94% · Red <80% | vs previous run | Opens latest test run |
| 3 | Open P0 Defects | Critical blocking defects open | Red if > 0 · Green if 0 | — | Opens Defects filtered to P0 |
| 4 | Open P1 Defects | High priority defects open | Red if > 5 · Amber 1–5 | — | Opens Defects filtered to P1 |
| 5 | Test Coverage | % of test cases with a passing run in last 7 days | Green ≥90% · Amber 70–89% · Red <70% | vs last week | Opens Coverage tab |
| 6 | Flaky Tests | Tests with erratic pass/fail behaviour | Amber if > 10 · Red if > 25 | vs last week | Opens Automation Health |
| 7 | Releases Pending QA | Releases awaiting QA sign-off | Amber if > 0 | — | Opens Release Gates |
| 8 | Blocked Releases | Releases with failed QA gate (cannot deploy) | Red if > 0 · Green if 0 | — | Opens Release Gates filtered |

KPI values animate count-up on page load. Poll guard: `every 60s[!document.querySelector('.drawer-open,.modal-open')]`.

---

## Tab 1 — Overview

Quick-scan view of the current quality state across all environments.

### Environment Status Bar (top row)

4 environment cards in a row (or 2×2 on smaller screens):

| Environment | Card Content |
|---|---|
| Development | Last test run: timestamp · Pass rate: % · P0 defects: count · Active runs: count · Status badge |
| Staging | Last test run: timestamp · Pass rate: % · P0 defects: count · Last deploy: version + time · Status badge |
| UAT | Last test run: timestamp · Pass rate: % · Open defects: count · Client notes: Y/N · Status badge |
| Pre-Production | Last test run: timestamp · Pass rate: % · Release-blocking defects: count · Pending sign-off: Y/N · Status badge |

Status badge computation:
- **Green (✓ Healthy):** pass rate ≥ 95% AND zero P0 defects AND no failed migrations
- **Amber (⚠ Degraded):** pass rate 80–94% OR ≥ 1 P1 defect open OR pending migrations
- **Red (✗ Blocked):** pass rate < 80% OR any P0 defect open OR environment down

Card click → opens Environments tab, scrolls to that environment's section.

### Recent Test Runs Table (last 10 runs across all environments)

| Column | Detail |
|---|---|
| Run ID | Auto-generated ID (e.g. TR-2026-03-20-001) |
| Environment | Badge (Dev / Staging / UAT / Pre-Prod) |
| Trigger | Manual / CI/CD Pipeline / Scheduled |
| Suite | Full Regression / Smoke / Sanity / Feature-specific |
| Started By | User name or "CI Pipeline" |
| Start Time | Date and time (IST) |
| Duration | HH:MM:SS or "Running" with elapsed time |
| Tests Run | Total count |
| Passed | Count + % (green) |
| Failed | Count + % (red if > 0) |
| Skipped | Count + % (grey) |
| Status | Running (spinner) · Passed (green) · Failed (red) · Aborted (grey) |
| Actions | View Details · Re-run · Abort (if running) |

Row click → opens Test Run Detail Drawer (720px).

### Defect Trend Chart

Line chart: daily open defect count by severity (P0 / P1 / P2 / P3) over last 30 days. Multiple lines, colour-coded by severity (red / orange / amber / grey). Reference line at 0 for P0 (ideal state). Shows if defect backlog is growing or shrinking. X-axis: dates. Y-axis: count.

### Pass Rate Trend Chart

Line chart: test pass rate per run over last 30 days. Single blue line. Reference lines at 95% (green threshold, labelled "Target") and 80% (amber threshold, labelled "Warning"). Points are clickable and open the corresponding run in the Test Runs drawer.

### QA Quality Score (computed metric)

A single composite score (0–100) computed from weighted factors:
- Pass rate of last run: 40%
- P0 defect count (inverted): 30%
- Coverage %: 20%
- Flaky test rate: 10%

Displayed as a large number with colour (green ≥ 80 · amber 60–79 · red < 60). Shown with "vs last week" delta. Tooltip explains the formula.

---

## Tab 2 — Test Runs

Detailed management of all test runs.

### Toolbar

| Control | Options |
|---|---|
| Search | Run ID, trigger type |
| Environment | All / Dev / Staging / UAT / Pre-Prod |
| Status | All / Running / Passed / Failed / Aborted |
| Trigger | All / Manual / CI/CD / Scheduled |
| Suite | All / Full Regression / Smoke / Sanity / Feature-specific |
| Date range | Start date range (default: last 14 days) |

### "Start Test Run" Button

Opens **New Test Run Modal:**

**Step 1 — Target:**
- Environment selector (required): Dev / Staging / UAT / Pre-Prod
- Test suite selector (required):
  - Full Regression: all 12,000+ test cases
  - Smoke Test: ~120 critical-path tests (runs in ~10 min)
  - Sanity Check: ~40 core-feature tests (runs in ~4 min)
  - Feature-specific: dropdown of 18 feature areas → runs only test cases tagged for that feature
  - Release suite: selects all test cases linked to a specific release
  - Custom: multi-select individual test cases by ID, tag, or feature filter

**Step 2 — Configuration:**
- Parallel workers: 1 / 2 / 4 / 8 (higher = faster but more infrastructure cost)
- Browser: Chrome (default) / Firefox / Safari / All browsers (E2E tests only)
- Retry failed tests: 0 / 1 / 2 retries before marking as failed (reduces false failures from intermittent issues)
- Stop on first failure: Yes / No (for fast feedback on critical failures)
- Notes (optional — appears in run summary, useful for "testing PR #482 fix")

**Step 3 — Notifications:**
- Notify on completion: Yes / No
- Notify recipients: logged-in user + optional additional team members
- Channel: In-App / Email / Slack webhook (if configured)
- Notify on failure only: toggle (suppresses success notifications)

"Start Run" button → run queued in Celery, confirmation shown with run ID.

### Test Run Detail Drawer (720px)

Opened by clicking any run row.

**Header:** Run ID · Environment badge · Status badge (with live spinner if running) · Duration · Started by · Start/End time

**Progress bar** (if running): X% complete, animated. Shows: "Passed: N · Failed: N · Remaining: N".

#### Drawer Tab 1 — Summary

- 4 stat cards: Total / Passed / Failed / Skipped (with counts and %)
- Pie chart: passed vs failed vs skipped vs running (if live)
- Failure categories: grouped bar chart showing failure count by feature area (Exam Management / Student Management / Analytics / Payment / Authentication / etc.)
- Top 10 failing tests table: Test Name · Suite · Failure Reason (first 80 chars) · Duration · "View Log" link

**Pass rate comparison row (if re-run):**
"Comparison with previous run" section: side-by-side count of Passed/Failed/Skipped. Delta arrows show improvements and regressions.

**Action buttons in summary:**
- "Re-run Failed Tests" → starts a new run using only the failed tests from this run
- "Create Defect" → opens New Defect modal (page 25) pre-filled with run ID and environment
- "Export Report" → downloads PDF/CSV of run summary

#### Drawer Tab 2 — All Tests

Full list of tests in this run with search and filter.

| Column | Detail |
|---|---|
| Test Case ID | Link to test case in repository (page 23) |
| Test Name | Full name (may be long — truncated with expand) |
| Suite | Category badge |
| Feature Area | Module/feature tag |
| Type | Unit / Integration / E2E / Manual |
| Status | Passed (green) · Failed (red) · Skipped (grey) · Running (spinner) |
| Duration | Seconds (red if > 3x average duration — timeout risk) |
| Error Message | First 80 chars of error if failed; click to expand full error |
| Flaky | "Flaky" amber badge if this test has flakiness history |
| Actions | View Logs · Re-run Isolated · Create Defect |

**Search:** Filter by test name, ID, or error keyword. Results update inline.

**Filter bar:** Passed / Failed / Skipped / All; Flaky only; By feature area.

**Pagination:** 25 / 50 / 100 per page (full regression may have 12,000+ rows).

#### Drawer Tab 3 — Logs

Raw log output for the entire run.

- Monospace font, dark background
- Line numbers shown
- "Jump to first error" button → scrolls directly to first FAIL or ERROR line
- "Jump to next error" button → iterates through error lines
- Search within logs: ctrl+F style search with highlight
- Download as `.txt` button (full log, may be 10–50MB for full regression)
- Filter log level: All / INFO / WARNING / ERROR / CRITICAL

For individual test logs: clicking "View Logs" on a specific test row in Tab 2 opens a nested drawer (560px) showing only that test's log output.

#### Drawer Tab 4 — Defects Raised

List of defects opened during or after this run. Links to full Defect Tracker (page 25).

| Column | Detail |
|---|---|
| Defect ID | DEF-NNNN (link opens defect in new drawer layer) |
| Title | Short description |
| Severity | P0 / P1 / P2 / P3 badge |
| Status | Open / In Progress / Fixed / etc. |
| Assigned To | Engineer name |
| Linked Test | Test case that triggered the defect |
| Created | Timestamp |

"Create New Defect" button at bottom → opens New Defect modal pre-filled with run ID.

---

## Tab 3 — Release Gates

QA sign-off management integrated with releases. A release cannot be deployed to production until its QA gate is passed.

### Release Gates Table

| Column | Detail |
|---|---|
| Release | Version number (e.g. v4.2.1) + link to Release Manager (page 03) |
| Type | Major / Minor / Hotfix / Patch badge |
| Target Date | Scheduled deploy date |
| QA Status | Not Started / In Progress / Passed / Failed / Blocked |
| Test Coverage | % of release features covered by test cases |
| Last Test Run | Run ID + pass rate + timestamp |
| P0 Defects | Count (red if > 0) |
| P1 Defects | Count (amber if > configurable threshold) |
| Assigned QA | Engineer name |
| Sign-off | "Sign Off" button / "Signed Off ✓" green badge / "Blocked ✗" red badge |

Clicking a release row → expands inline to show full gate criteria checklist.

### Release Readiness Criteria (per release)

A release gate turns Green when ALL of:
1. Test coverage ≥ 90% for all features in the release (configurable threshold per release type)
2. Latest test run pass rate ≥ 95% (configurable — hotfixes may have a lower threshold of 85%)
3. Zero P0 defects open (hard requirement, no exception)
4. P1 defects ≤ 3 open (configurable per release type)
5. QA engineer has explicitly signed off via the confirmation modal

Criteria checklist shown inline per release (expanded row):

| Criterion | Status | Detail | Configurable? |
|---|---|---|---|
| Test Coverage ≥ 90% | ✓ | 94.3% coverage achieved | Yes — PM can set threshold |
| Latest Pass Rate ≥ 95% | ✓ | 97.1% on last staging run | Yes — hotfixes: 85% |
| Zero P0 Defects | ✗ | 1 P0 open: DEF-0482 (Exam submission timeout) | No — hard requirement |
| P1 Defects ≤ 3 | ✓ | 2 P1 defects open | Yes — default 3, configurable |
| QA Sign-off | Pending | Awaiting sign-off from Deepa Menon | N/A |

"Sign Off" button: disabled if any non-configurable criterion (zero P0) is not met. Shows tooltip explaining what is blocking sign-off. For configurable criteria that are failing, PM can override with documented justification.

### Override Gate Criterion

If a configurable criterion is failing but a release must proceed (e.g. emergency hotfix with 85% pass rate):
- "Override Criterion" button (PM Platform only)
- Requires: justification text (min 50 chars) + confirmation
- Override logged in audit log with: who, what, why, timestamp
- Release can proceed but sign-off confirmation shows "OVERRIDDEN CRITERIA" warning banner

### QA Sign-off Confirmation Modal

- "You are signing off release v4.2.1 for production deployment."
- Current gate status summary shown: X of Y criteria met, any overridden criteria flagged
- "Confirm you have reviewed all open defects and test results."
- Checkbox: "I confirm all required release criteria are met (or appropriately overridden)"
- Notes field (optional — recommended: add test run ID and any caveats)
- "Confirm Sign-off" button
- After sign-off: "QA Signed Off ✓" badge shown. Sign-off is logged with timestamp, engineer name, and notes. Sign-off can be revoked by PM Platform only (with documented reason).

---

## Tab 4 — Defects

Defect management view (lighter version of the full defect tracker on page 25). Provides QA engineers quick access without leaving the QA Dashboard.

### Toolbar

| Control | Options |
|---|---|
| Search | Defect title, ID |
| Severity | All / P0 / P1 / P2 / P3 |
| Status | All / Open / In Progress / Fixed / Closed / Deferred |
| Environment | Where discovered |
| Release | Linked release version |
| Assignee | Any / Me / Specific engineer |
| Source | All / Automated / Manual QA / Institution Reported / Monitoring |

### Defect Table — 10 columns

| Column | Detail |
|---|---|
| Defect ID | DEF-NNNN (link to defect detail in Defect Tracker page 25) |
| Title | Short description (truncated at 60 chars) |
| Severity | P0 (red) · P1 (orange) · P2 (amber) · P3 (grey) badge |
| Status | Colour-coded badge |
| Component | Affected feature area |
| Environment | Where found |
| Assigned To | Engineer name |
| Found In Run | Test run ID (link opens run in drawer) |
| Linked Release | Release version |
| Days Open | Count (red if > SLA threshold for severity) |

Row expand: Shows full description, steps to reproduce (first 3), expected vs actual behaviour, screenshot indicator.

**Quick actions on row:**
- Assign to me
- Change severity (with confirmation)
- Change status
- Link to release

**Pagination:** Showing X–Y of Z defects · page pills · per-page selector (25 / 50 / 100)

---

## Tab 5 — Environments

Detailed health and configuration of each test environment.

### Environment Health Cards (4 cards — one per environment)

Each card shows:
- Environment name + status badge (Healthy / Degraded / Down)
- URL (masked — e.g. staging.srav.internal)
- Last health check: timestamp + result (latency ms)
- Application version: v4.2.1 (with commit hash truncated to 8 chars)
- Database: PostgreSQL version + connection pool (X active / Y idle / Z max)
- Redis: ping status + memory usage (XMB / YММB) + keyspace hit rate
- Celery workers: count active / count idle / count in queue
- Storage: disk usage % for uploads/media
- Last deployed version: version + deploy timestamp
- Migrations status: "Up to date ✓" or "X pending migrations ⚠"
- Background jobs: last successful run of scheduled Celery tasks

### Environment Comparison Table

Side-by-side comparison of all 4 environments:

| Setting | Dev | Staging | UAT | Pre-Prod |
|---|---|---|---|---|
| App version | v4.2.1-dev | v4.2.1 | v4.2.0 | v4.1.9 |
| Django version | 4.2.11 | 4.2.11 | 4.2.10 | 4.2.10 |
| DB version | PG 15.4 | PG 15.4 | PG 15.3 | PG 15.3 |
| Redis version | 7.0.12 | 7.0.12 | 7.0.12 | 7.0.11 |
| Pending migrations | 0 | 0 | 2 | 0 |
| Feature flags | Dev overrides | Same as prod | Same as prod | Same as prod |
| Seed data | Synthetic test data | Sanitised production snapshot | Client-provided test data | Anonymised production snapshot |
| DB size | ~2GB | ~12GB | ~8GB | ~45GB |
| Last deployed | 1h ago | 6h ago | 2 days ago | 5 days ago |

Cells where environments diverge from staging are highlighted amber (version drift detection). DB version differences shown in amber.

### Environment Actions

Per environment card:
- **"Run Health Check"** button → triggers immediate health check probe (HTTP ping + DB query + Redis ping + Celery ping). Result shown inline within 10 seconds.
- **"Trigger Deployment"** button → opens Trigger Deployment Modal (links to Release Manager page 03 for version selection). Not available for Pre-Prod without PM approval.
- **"View Logs"** button → opens Live Log Tail Drawer (560px): streaming log output from application server + Celery workers + Nginx. Search, filter by log level, download.
- **"Reset to Snapshot"** button → dangerous action. Available to QA Engineer only for Dev and Staging. Requires typed confirmation: "reset [environment-name]". Celery async task; shows progress. Irreversible.
- **"Apply Pending Migrations"** button (shown only if pending migrations > 0) → runs `manage.py migrate`. Available to QA Engineer + Dev team. Shows migration names before confirming.

### Environment Status History Chart

Line chart: environment health status (0=Down, 1=Degraded, 2=Healthy) over last 7 days per environment. Each environment a separate line. Shows uptime patterns and recurring issues. X-axis: 24h segments. Y-axis: 0–2.

---

## Tab 6 — Coverage

Test coverage analysis: which parts of the platform have adequate test coverage.

### Coverage Summary Cards (4 cards)

| Card | Value |
|---|---|
| Overall Coverage | % of feature areas with at least 1 test type ≥ 90% pass rate |
| Automated Coverage | % of all feature areas covered by automated test cases |
| Manual-Only Coverage | % covered by manual test cases with no automation equivalent |
| Critical Path Coverage | % of the 12 defined critical user journeys with ≥ 90% pass rate |

### Coverage Heatmap

Grid: Feature areas (rows) × Test types (columns: Unit / Integration / E2E / Manual / Performance).

Cell content: pass rate %. Colour: ≥ 90% green · 70–89% amber · < 70% red · ✗ no coverage (white cell with dashed border).

Clicking a cell → opens filtered test case list (opens Test Case Repository page 23 in a new tab, pre-filtered to that feature area + test type).

Full coverage heatmap (18 feature areas × 5 test types = 90 cells):

| Feature Area | Unit | Integration | E2E | Manual | Performance |
|---|---|---|---|---|---|
| Student Login / Auth | 98% | 95% | 92% | ✓ | ✓ |
| Student Registration | 95% | 92% | 88% | ✓ | ✗ |
| Exam Attempt — MCQ | 87% | 90% | 88% | ✓ | ✓ |
| Exam Attempt — MSQ | 82% | 85% | 80% | ✓ | ✓ |
| Exam Submit | 99% | 97% | 95% | ✓ | ✓ |
| Result Calculation | 99% | 97% | 94% | ✓ | ✗ |
| Leaderboard | 88% | 84% | 80% | ✓ | ✗ |
| Payment Flow | 90% | 85% | 78% | ✓ | ✗ |
| Admin: Create Exam | 85% | 82% | 79% | ✓ | ✗ |
| Admin: Student Import | 92% | 89% | 85% | ✓ | ✗ |
| Mobile App Login | ✗ | 82% | 75% | ✓ | ✗ |
| Mobile App Exam | ✗ | 78% | 72% | ✓ | ✗ |
| Proctoring | ✗ | 70% | 68% | ✓ | ✗ |
| Notification Delivery | 80% | 75% | ✗ | ✓ | ✗ |
| Fee/Payment | 88% | 82% | 75% | ✓ | ✗ |
| Analytics — Dashboard | 70% | 65% | 60% | ✓ | ✗ |
| API — Public | ✗ | 80% | ✗ | ✗ | ✓ |
| Background Tasks | 75% | 70% | ✗ | ✓ | ✗ |

### Critical Path Coverage

Special section for highest-priority user journeys. Each critical path has a defined set of test cases that must all pass for the path to be "covered":

| Critical Path | Steps | Test Coverage | Last Full Pass | Status |
|---|---|---|---|---|
| Student: Login → Start Exam → Submit → View Result | 4 steps | 94% | 2h ago | ✓ |
| Admin: Create Exam → Schedule → Publish → Monitor | 4 steps | 88% | 4h ago | ⚠ |
| Institution: Sign Up → Onboard → First Exam Live | 8 steps | 72% | Yesterday | ⚠ |
| Student: Payment → Course Access → Exam Attempt | 5 steps | 85% | 6h ago | ✓ |
| Student: Mobile → Login → Take Exam → View Result | 5 steps | 68% | 2 days ago | ✗ |
| Admin: Create Question → Review → Publish Exam | 3 steps | 90% | 3h ago | ✓ |
| Institution Admin: Import Students → Create Batch → Schedule Exam | 3 steps | 88% | Yesterday | ✓ |
| Student: Retake Exam → Improved Score → Leaderboard Update | 4 steps | 80% | 3h ago | ✓ |
| Admin: Proctor Alert → Suspend Attempt → Notify Institution | 3 steps | 72% | 2 days ago | ⚠ |
| Student: Forgot Password → Reset → Login → Exam | 4 steps | 95% | 1h ago | ✓ |
| Institution: Raise Support → PM Acknowledges → Defect Created | 3 steps | 60% | 4 days ago | ✗ |
| Admin: Release Results → Notification Burst → 74K concurrent | 3 steps | 78% | Last week | ⚠ |

### Coverage Gap Report

Automatically generated list of coverage gaps:

| Gap | Feature Area | Missing Coverage | Recommended Action |
|---|---|---|---|
| No E2E tests for Notification Delivery | Notifications | E2E | Create 5 E2E test cases |
| No Performance tests for Leaderboard | Leaderboard | Performance | Add to load test scenario |
| No unit tests for Mobile App | Mobile | Unit | Add Flutter unit tests |
| Low E2E coverage for Proctoring (68%) | Proctoring | E2E | Add 8 E2E test cases |

---

## Tab 7 — Automation Health

Monitors the health of the automated test suite. Identifies unreliable tests that compromise CI/CD signal quality.

### Automation Summary Cards (5 cards)

| Card | Value |
|---|---|
| Total Automated Tests | 9,840 (of 12,000+ — 82% automation rate) |
| Passing Reliably | 9,210 (pass rate ≥ 99% over last 10 runs) |
| Flaky Tests | 430 (pass rate 80–98% — non-deterministic) |
| Consistently Failing | 200 (pass rate < 80% — need fix) |
| Avg Test Duration | 4.2 seconds per test |

### Flaky Tests Table

Tests that have inconsistent pass/fail behaviour across runs without code changes. Flakiness = pass rate 80–98% over last 20 runs.

| Column | Detail |
|---|---|
| Test Name | Full name (link to test case in repository) |
| Suite | Category badge |
| Feature Area | Module affected |
| Pass Rate (last 20 runs) | % — shown as colour bar (amber = flaky) |
| Last Pass | Relative time |
| Last Fail | Relative time |
| Failure Pattern | Intermittent / Environment-dependent / Timing-dependent / Data-dependent |
| Assigned To | QA engineer investigating (or "Unassigned") |
| Status | Under Investigation / Fix in Progress / Quarantined |
| Quarantine Date | When quarantined (if applicable) |
| Actions | Quarantine · Investigate · View History · Assign |

**"Quarantine" action:**
- Removes test from main pass/fail calculation without deleting it
- Quarantined tests shown in separate "Quarantined Tests" sub-section
- Prevents flaky test from blocking CI/CD pipeline
- Must set: quarantine reason + owner + expected resolution date
- Reviewed automatically: if quarantine date > 30 days with no resolution, PM is notified

**"View History" action:**
Opens a mini-drawer showing pass/fail result per run for last 20 runs. Timeline view showing pass (green) / fail (red) per run with run ID and date. Pattern is visually obvious.

### Consistently Failing Tests

Tests with pass rate < 80% — these are likely broken and need immediate fix:

| Test Name | Suite | Last Pass | Failure Count | Assigned To | Priority |
|---|---|---|---|---|---|
| test_proctoring_tab_detection | E2E | 5 days ago | 14/20 | Ramesh K | P1 |
| test_mobile_offline_submit | E2E Mobile | 8 days ago | 19/20 | Kavya R | P0 |
| test_bulk_student_import_10k | Integration | 3 days ago | 11/20 | Arjun P | P1 |

### Test Duration Trend Chart

Line chart: average test run duration (Full Regression suite) over time. X-axis: run dates (last 30 days). Y-axis: minutes. Reference line at historical baseline. Used to detect when tests are slowing down (database growth, network latency, test bloat). Alert threshold: > 20% above baseline.

### Suite Execution Order

Shows the CI/CD pipeline test execution sequence with timing benchmarks:

| Step | Suite | Tests | Avg Duration | Parallel Workers | Gate Behaviour |
|---|---|---|---|---|---|
| 1 | Unit tests | ~4,000 | 2–3 min | 4 | Fail: blocks next steps |
| 2 | API integration tests | ~2,500 | 8–12 min | 4 | Fail: blocks next steps |
| 3 | Smoke tests — critical paths | ~120 | 5–7 min | 2 | Fail: blocks next steps |
| 4 | Full regression | ~9,800 | 30–45 min | 8 | Fail: marks build as failed |
| 5 | E2E browser tests | ~800 | 15–20 min | 4 | Fail: marks build as failed |
| 6 | Performance baseline check | ~50 | 10 min | 1 | Fail if > 10% degradation |
| 7 | Security scan (OWASP ZAP) | Automated scan | 20 min | 1 | Fail on P0/P1 findings |

"Edit Execution Order" button (QA Engineer): drag-and-drop reorder, enable/disable steps. Changes apply to next pipeline run.

### Test Suite Health Metrics

| Suite | Tests | Automation % | Pass Rate (30d avg) | Avg Duration | Flaky Count |
|---|---|---|---|---|---|
| Authentication | 240 | 95% | 97.2% | 3.1s | 8 |
| Exam Management | 420 | 88% | 94.1% | 5.8s | 24 |
| Student Management | 380 | 82% | 96.4% | 4.2s | 12 |
| Payment | 180 | 90% | 93.8% | 6.1s | 18 |
| Analytics | 320 | 70% | 88.2% | 7.4s | 41 |
| Mobile App | 640 | 72% | 82.4% | 8.2s | 98 |
| Proctoring | 280 | 68% | 79.1% | 9.1s | 52 |
| Notifications | 160 | 75% | 91.3% | 4.8s | 14 |

---

## QA Report Export

Available from the page header "Export Report" button.

**Report Types:**

| Report | Content | Format | Audience |
|---|---|---|---|
| Weekly QA Summary | Pass rate trends, defect counts, flaky test count, test runs executed | PDF / Email | PM Platform, Engineering Lead |
| Release QA Report | Full coverage metrics, test run results, defect list, sign-off status for one release | PDF | PM, Stakeholders |
| Flaky Test Report | All flaky tests with patterns, owner, status, age | CSV / PDF | QA Team |
| Coverage Gap Report | Feature areas below threshold with recommended actions | PDF | PM + Engineering |
| Monthly QA Health | Month-over-month metrics including cycle time, MTTR, defect density | PDF | Engineering Director |

Reports generated asynchronously (Celery). Download link sent via in-app notification when ready.

---

## Integration Points

| Page | Integration |
|---|---|
| Page 03 — Release Manager | QA sign-off status shown in release checklist. Sign-off from QA Dashboard updates release gate in real time. |
| Page 23 — Test Case Repository | Test runs reference individual test case IDs. Clicking test case ID in run detail opens test case in repository. |
| Page 24 — Performance Test Dashboard | Performance baseline check step in automation suite suite links to performance test results. |
| Page 25 — Defect Tracker | "Create Defect" from any failed test run pre-fills defect form. Defect counts in KPI strip come from Defect Tracker live data. |
| Page 26 — Automation Monitor | Pipeline runs in CI/CD are also visible in Automation Monitor. QA Dashboard shows test result side, Automation Monitor shows pipeline health side. |

---

## Key Design Decisions

| Concern | Decision | Rationale |
|---|---|---|
| 8-card KPI strip | More than other pages | QA needs more KPIs at a glance — defects, pass rate, flaky count all critical and independent |
| 60s KPI refresh | Shorter than most pages | Test runs can flip status quickly; QA needs near-real-time visibility during active test runs |
| QA Quality Score composite | Weighted multi-factor score | Single number enables quick management communication — "we are at 82/100 today" |
| Release gate criteria | Configurable thresholds per release type | P1 defect threshold may vary (hotfix vs major release has different acceptable risk profiles) |
| Flaky test quarantine | Separate sub-section | Flaky tests blocking CI is a known productivity killer; quarantine prevents that without deleting test history |
| Environment comparison table | Side-by-side all 4 environments | Version drift between environments is a common source of bugs; the table makes it immediately obvious |
| QA sign-off confirmation | Separate modal with typed acknowledgement | High-stakes action — "I confirm" checkbox plus notes forces explicit acknowledgement; not accidental click |
| Critical path coverage | Separate from general coverage heatmap | Some paths are disproportionately important (login → exam → result); they deserve individual tracking |
| Coverage heatmap | Feature × Test type grid | Visually shows which feature areas lack automation (mobile, proctoring) at a glance |
| Run re-run failed tests only | Button in run summary | Saves CI time — retesting only failed tests after a fix instead of full regression |
| Override gate criterion | PM-only with documented justification | Emergency hotfixes may need to bypass a criterion; audit trail ensures accountability |
| Suite execution order | Configurable by QA Engineer | Optimising pipeline speed (fast gates first, slow suites last) is an ongoing concern |

---

## Tab 8 — Accessibility Testing

**Purpose:** At 2.4M–7.6M users, a significant portion have visual impairments, motor limitations, or rely on screen readers (JAWS, NVDA, TalkBack on Android). WCAG 2.1 AA compliance is the platform standard. This tab tracks accessibility test results per release, per feature area, so that QA Lead can certify accessibility compliance before a release ships.

**Why in QA Dashboard and not Design System (page 19):** Page 19 defines the *standards*. This tab tracks *test results against those standards*. Design tells QA what to test; QA records pass/fail.

---

### 8.1 Accessibility Test Runs Table

| Run ID | Release | Feature Area | Test Type | Tester | Date | Issues Found | Status |
|---|---|---|---|---|---|---|---|
| A11Y-2026-03-20 | v3.5.0 | Exam Interface | Screen Reader | Deepa | Mar 20 | 3 | ⚠ Open |
| A11Y-2026-03-14 | v3.4.2 | Result Page | Keyboard Nav | Arjun | Mar 14 | 0 | ✅ Pass |
| A11Y-2026-03-01 | v3.4.1 | Login / OTP | WCAG Contrast | Deepa | Mar 1 | 1 | ✅ Resolved |
| A11Y-2026-02-15 | v3.4.0 | Question Bank | Screen Reader | Arjun | Feb 15 | 5 | ✅ Resolved |

**Columns:** Run ID · Release · Feature Area · Test Type · Tester · Date · Issues Found · Status

**Test Types:**
- Screen Reader — NVDA (Windows), JAWS (Windows), TalkBack (Android), VoiceOver (iOS)
- Keyboard Navigation — Tab order, focus traps, skip-to-content, Esc-close
- Colour Contrast — WCAG AA minimum 4.5:1 normal text, 3:1 large text
- Motion / Animation — Prefers-reduced-motion respects
- Touch Target — Mobile: minimum 44×44px per WCAG 2.1 SC 2.5.5
- Zoom / Reflow — Page usable at 400% zoom without horizontal scroll
- ARIA Labels — All interactive elements have descriptive aria-label

---

### 8.2 Accessibility Issue Tracker

Each accessibility issue from any test run is recorded here. This is a sub-list of page 25 (Defect Tracker) filtered to `component=accessibility` — clicking any issue opens the full defect in page 25.

**Columns:**

| Issue ID | Description | Page / Component | WCAG Criterion | Severity | Assignee | Status |
|---|---|---|---|---|---|---|
| A11Y-INC-042 | Screen reader doesn't announce timer remaining | Exam Interface | 4.1.3 Status Messages | P1 | Ravi (Frontend) | Open |
| A11Y-INC-041 | Insufficient contrast: button text on dark bg | Question Card | 1.4.3 Contrast | P2 | Design | Resolved |
| A11Y-INC-040 | Modal focus trap missing — Tab leaves modal | Result Modal | 2.1.2 No Keyboard Trap | P1 | Backend | Resolved |

**Severity mapping:**
- P0: Completely unusable by screen reader users (blocks core flow like exam submission)
- P1: Significant barrier (WCAG A violation)
- P2: Moderate barrier (WCAG AA violation)
- P3: Enhancement (WCAG AAA or best practice)

---

### 8.3 Accessibility Coverage by Feature Area

| Feature Area | Last Tested | Screen Reader | Keyboard | Contrast | Touch | Overall |
|---|---|---|---|---|---|---|
| Login / OTP | Mar 1 | ✅ Pass | ✅ Pass | ✅ Pass | ✅ Pass | ✅ |
| Exam Interface | Mar 20 | ⚠ 3 open | ✅ Pass | ✅ Pass | ✅ Pass | ⚠ |
| Question Bank | Feb 15 | ✅ Pass | ✅ Pass | ✅ Pass | N/A | ✅ |
| Result Page | Mar 14 | ✅ Pass | ✅ Pass | ✅ Pass | ✅ Pass | ✅ |
| Institution Dashboard | Jan 20 | ✅ Pass | ⚠ 1 open | ✅ Pass | N/A | ⚠ |
| Mobile App | Feb 28 | N/A | N/A | ✅ Pass | ⚠ 2 open | ⚠ |
| Payment / Billing | Not tested | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |

Red `⬜` "Not tested" rows trigger a warning badge on the tab when a release containing that feature area is about to ship.

---

### 8.4 Accessibility Release Gate

**Gate rule:** A release cannot be marked QA Sign-off (page 03, Release Manager) if any P0 or P1 accessibility issues are open for feature areas included in that release.

**Gate status displayed in Release Gates tab (Tab 3):**
```
Accessibility Gate:  ⚠ OPEN  (1 P1 issue in Exam Interface — INC-042)
                     [View Issue →]
```

**Exemption process:** QA Lead can grant an exemption for a P1 issue with: justification text + milestone date for resolution + PM Platform sign-off. Exemption creates an audit entry.

---

## Tab 9 — Security Scan Results

**Purpose:** QA Engineer runs OWASP ZAP automated scans against Staging and Pre-Production environments as part of every release cycle. Results are tracked here. Findings are classified by OWASP risk rating (Critical/High/Medium/Low/Informational) and assigned to Engineering (Division C Security Engineer, Role 16) for remediation.

**Why in QA Dashboard (not Engineering):** QA initiates, tracks, and gates the scans. Security Engineer (Division C) remediates. QA verifies the fix. This is the same model as functional defects — QA owns the tracking, Engineering owns the fix.

---

### 9.1 Security Scan Runs Table

| Scan ID | Environment | Release | Scanner | Started | Duration | Critical | High | Medium | Status |
|---|---|---|---|---|---|---|---|---|---|
| SEC-2026-03-18 | Pre-Prod | v3.5.0 | OWASP ZAP | Mar 18 | 2h 14m | 0 | 1 | 3 | ⚠ High open |
| SEC-2026-02-28 | Staging | v3.4.2 | OWASP ZAP | Feb 28 | 1h 58m | 0 | 0 | 2 | ✅ Resolved |
| SEC-2026-02-01 | Staging | v3.4.1 | OWASP ZAP | Feb 1 | 2h 02m | 0 | 0 | 5 | ✅ Resolved |

**Scan triggers:** Automatic — every Pre-Production promotion in Release Manager triggers a scan. Manual — [Run Scan Now] button (QA Engineer only).

**[Run Scan Now]:** Opens modal — select environment (Staging/Pre-Prod) + scope (Full / API only / Frontend only) + notification recipients.

---

### 9.2 Security Findings Table

| Finding ID | Title | OWASP Category | Risk | Environment | Found In | Assignee | Status |
|---|---|---|---|---|---|---|---|
| SEC-F-088 | Missing CSRF token on admin action endpoint | OWASP A01 (Broken Access Control) | High | Pre-Prod | `/api/v1/flags/update/` | Kiran (Backend) | Open |
| SEC-F-087 | Clickjacking: X-Frame-Options header missing | OWASP A05 (Security Misconfiguration) | Medium | Staging | All pages | Ravi (Frontend) | Resolved |
| SEC-F-086 | Verbose error messages expose stack trace | OWASP A09 (Logging/Monitoring Failures) | Medium | Staging | `/api/v1/exams/` 500 responses | Kiran (Backend) | Resolved |

**OWASP categories tracked:** A01 Broken Access Control · A02 Cryptographic Failures · A03 Injection · A04 Insecure Design · A05 Security Misconfiguration · A06 Vulnerable Components · A07 Auth Failures · A08 Software Integrity Failures · A09 Logging Failures · A10 SSRF

**Risk badge colours:**
- Critical: `bg-[#450A0A] text-[#F87171] animate-pulse`
- High: `bg-[#450A0A] text-[#EF4444]`
- Medium: `bg-[#451A03] text-[#F59E0B]`
- Low: `bg-[#1E2D4A] text-[#94A3B8]`

**Security Release Gate:** A release cannot be QA sign-off approved if any Critical or High security findings are open. Medium findings require documented risk acceptance from CTO (Role 2 in Division A).
