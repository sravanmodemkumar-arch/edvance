# Page 24 — Performance Test Dashboard

**URL:** `/portal/product/performance-tests/`
**Permission:** `product.view_performance_tests`
**Priority:** P1
**Roles:** QA Engineer, PM Platform

---

## Purpose

Manages and monitors all performance and load testing activities for the SRAV platform. With 74,000 peak concurrent users during major national exam result releases and simultaneous exam sessions across 1,950+ institutions, performance testing is not optional — it is a critical release gate. This page is where QA engineers design, execute, monitor, and analyse performance test scenarios to ensure the platform holds under peak load.

Core responsibilities:
- Design load test scenarios for realistic usage patterns
- Execute load tests against staging and pre-production environments
- Monitor real-time performance metrics during test execution
- Track performance baselines and flag regressions
- Simulate exam-day scenarios (peak load, concurrent submit storms, result release spikes)
- Validate infrastructure capacity before major releases
- Maintain performance SLAs and alert when results breach them

**Scale context for test design:**
- 74,000 peak concurrent users (during national exam result release)
- Normal peak: ~15,000 concurrent users
- Exam-day peak: 50,000+ concurrent users (multiple institutions running exams simultaneously)
- Result release spike: up to 74,000 concurrent users hitting results endpoint within 5 minutes
- API: 800K+ test attempts per month
- Database: 2M+ questions, 7M+ student records, 50M+ test attempt records

---

## Page Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  "Performance Test Dashboard"    Environment ▾  [New Test Run]  │
├─────────────────────────────────────────────────────────────────┤
│  KPI Strip — 6 cards                                            │
├─────────────────────────────────────────────────────────────────┤
│  Tab Bar:                                                       │
│  Overview · Test Runs · Scenarios · Baselines                   │
│  SLA Tracker · Infrastructure · Reports                         │
├─────────────────────────────────────────────────────────────────┤
│  [Active Tab Content]                                           │
└─────────────────────────────────────────────────────────────────┘
```

---

## KPI Strip — 6 Cards

| # | Label | Value | Colour | Delta | Click Action |
|---|---|---|---|---|---|
| 1 | Active Test Runs | Running performance tests right now | Blue if >0 | — | Opens Test Runs tab |
| 2 | Peak Concurrent (Last Run) | Peak concurrent users achieved in most recent run | Colour vs target | vs previous run | Opens latest run detail |
| 3 | P95 Response Time | 95th percentile response time in last run (ms) | Green <500ms · Amber 500–1000ms · Red >1000ms | vs SLA | Opens latest run detail |
| 4 | Error Rate (Last Run) | % of requests that returned error during last run | Red if >1% | vs SLA | Opens latest run detail |
| 5 | SLA Breaches (30d) | Count of SLA violations in last 30 days | Red if >0 | — | Opens SLA Tracker |
| 6 | Last Baseline Updated | Date of most recent performance baseline | — | — | Opens Baselines tab |

---

## Tab 1 — Overview

**Current Environment Status Bar**

4 cards: Staging / UAT / Pre-Production / Production (read-only for production)

Each card shows:
- Environment name
- Current CPU utilisation % (auto-refresh 30s)
- Current memory utilisation %
- Active database connections
- Redis memory usage
- Gunicorn workers: active / total
- Celery workers: active / idle

**Latest Test Run Summary**

Most recent completed performance test run summary:
- Run name, date, environment
- Scenario type (Load / Stress / Spike / Soak / Concurrent Exam Simulation)
- Virtual users: peak concurrent users reached
- Duration: total test duration
- Requests sent: total HTTP requests
- Throughput: requests/second
- P50 response time, P90, P95, P99
- Error rate %
- Pass / Fail vs SLA thresholds
- "View Full Report" button → opens Run Detail Drawer

**Performance Trend Charts (2 charts)**

*Response Time Trend (last 10 runs):*
Line chart showing P50/P95/P99 response time per test run. X-axis: run date. Y-axis: milliseconds. Reference lines at SLA thresholds (500ms P95). Helps visualise if performance is degrading over time.

*Throughput Trend (last 10 runs):*
Bar chart showing requests/second achieved per run. Should be stable or improving.

---

## Tab 2 — Test Runs

Full history of all performance test runs.

### Toolbar

| Control | Options |
|---|---|
| Search | Run name or ID |
| Environment | All / Staging / UAT / Pre-Production |
| Scenario | All / Load Test / Stress Test / Spike Test / Soak Test / Concurrent Exam / Result Release Simulation |
| Status | All / Running / Passed / Failed / Aborted |
| Date range | Start date range |

### Test Run Table — 10 columns

| Column | Detail |
|---|---|
| Run ID | PT-NNNN |
| Run Name | Descriptive name |
| Environment | Badge |
| Scenario | Badge |
| Peak VU | Peak virtual users |
| Duration | HH:MM:SS |
| Throughput | Requests/second |
| P95 Response | Milliseconds |
| Error Rate | % |
| Status | Passed (green) · Failed (red) · Running (spinner) |

**Pagination:** Showing X–Y of Z runs · per-page selector (10 / 25 / 50)

### Test Run Detail Drawer (840px)

Largest drawer — performance testing requires rich visualisation.

**Drawer Header:**
Run ID · Run name · Environment · Status · Start/End time · Duration

**Drawer Tab 1 — Live Metrics (if running) / Summary (if completed):**

*If Running (auto-refresh 5s):*
- Virtual users ramp: line chart showing VU count over time (current point highlighted)
- Response time: real-time P50/P95/P99 gauges
- Throughput: requests/second gauge
- Error count: rising counter
- "Abort Run" button (red) with confirmation

*If Completed:*
- Test configuration summary: VU count, ramp-up time, duration, environment
- Pass/Fail for each SLA criterion
- Overall verdict: PASSED / FAILED

**Drawer Tab 2 — Response Time Analysis:**

*Response Time Distribution Histogram:*
Histogram showing distribution of response times across all requests:
- X-axis: response time buckets (0–100ms / 100–200ms / 200–500ms / 500ms–1s / 1s–2s / 2s–5s / >5s)
- Y-axis: % of requests in that bucket

*Percentile Table:*
| Percentile | Response Time |
|---|---|
| P50 (median) | 145ms |
| P75 | 280ms |
| P90 | 420ms |
| P95 | 618ms |
| P99 | 1,240ms |
| P99.9 | 3,800ms |
| Max | 8,240ms |

*Response Time Over Test Duration:*
Line chart: P50/P95/P99 response time vs time elapsed during the test. Shows when latency spikes occurred.

**Drawer Tab 3 — Throughput & Errors:**

*Throughput Chart:*
Line chart: requests/second over test duration. Shows ramping up, plateau, and ramp-down phases.

*Error Breakdown Table:*
| Error Type | Count | % of Total Requests |
|---|---|---|
| HTTP 500 (Server Error) | 234 | 0.12% |
| HTTP 503 (Service Unavailable) | 45 | 0.02% |
| HTTP 429 (Rate Limited) | 18 | 0.01% |
| Connection Timeout | 12 | 0.006% |
| Total | 309 | 0.15% |

*Error Rate Over Time:*
Line chart showing error rate (%) vs time during test. Reference line at 1% SLA threshold.

**Drawer Tab 4 — Endpoint Breakdown:**

Table showing performance per API endpoint:
| Endpoint | Method | Requests | Avg Response | P95 | P99 | Error Rate |
|---|---|---|---|---|---|---|
| /api/exam/submit/ | POST | 42,340 | 234ms | 890ms | 2,100ms | 0.8% |
| /api/results/get/ | GET | 128,450 | 78ms | 210ms | 480ms | 0.01% |
| /api/student/login/ | POST | 74,200 | 145ms | 380ms | 820ms | 0.05% |
| /api/exam/next-question/ | GET | 890,340 | 42ms | 180ms | 340ms | 0% |
| /api/leaderboard/ | GET | 24,500 | 320ms | 1,240ms | 3,800ms | 1.2% |

Sorting by P95 descending immediately shows slowest endpoints.

**Drawer Tab 5 — Infrastructure Metrics:**

*CPU utilisation chart:* Per server over test duration (multi-line: web-1, web-2, db-primary, celery-1)
*Memory utilisation chart:* Same servers
*Database connection pool:* Active / waiting connections over time
*Redis memory:* Usage over time
*Gunicorn worker queue depth:* Requests waiting for a free worker

---

## Tab 3 — Scenarios

Library of pre-defined test scenarios. Reusable blueprints for common performance tests.

### Scenario List

| Scenario Name | Type | Virtual Users | Duration | Description |
|---|---|---|---|---|
| Normal Load | Load Test | 5,000 VU | 30 min | Typical weekday usage pattern |
| Peak Load | Load Test | 15,000 VU | 30 min | Typical peak (evening study hours) |
| Exam Day Peak | Load Test | 50,000 VU | 60 min | Multiple institutions running exams simultaneously |
| Result Release Spike | Spike Test | 0→74,000 in 5 min | 20 min | National result release: all students hit results at once |
| Stress Test | Stress Test | 100,000 VU | 30 min | Find the breaking point |
| Soak Test | Soak Test | 5,000 VU | 8 hours | Steady-state endurance (detect memory leaks) |
| Concurrent Submit Storm | Spike Test | 10,000 submit requests in 60 seconds | 5 min | All students in multiple institutions submit at exam end |
| API Regression Perf | API Test | 500 VU | 15 min | Ensures API endpoints haven't regressed |
| Mobile App Load | Load Test | 20,000 VU (simulating mobile) | 30 min | Flutter app endpoints under load |
| New Feature Baseline | Custom | Configurable | Configurable | Baseline test for newly released features |

### Scenario Detail Drawer (640px)

**Header:** Scenario name · Type · VU count · Duration

**Tab 1 — Config:**

| Setting | Value |
|---|---|
| Virtual Users | Target VU count |
| Ramp-up Duration | How long to take to reach target VU (e.g. 5 minutes for gradual, 30 seconds for spike) |
| Steady-state Duration | How long to hold at target VU |
| Ramp-down Duration | How long to reduce VU count to 0 |
| Think Time | Simulated pause between requests (realistic user behaviour) |
| User Behaviour Mix | % of VUs doing each action (see below) |
| Target Environment | Default environment |

**User Behaviour Mix (for the Exam Day Peak scenario):**
| Behaviour | % of VUs | Description |
|---|---|---|
| Active exam taker | 40% | Continuously answering questions (GET next-question, POST answer) |
| Browsing results | 25% | Viewing past exam results and leaderboard |
| Dashboard view | 15% | Institution admin monitoring live exam |
| Login/logout cycle | 10% | New sessions being created |
| Mobile app usage | 10% | Flutter app API calls pattern |

**Tab 2 — SLA Thresholds:**
Thresholds that must be met for this scenario to PASS:

| Metric | Threshold | Severity if Breached |
|---|---|---|
| P95 response time | < 1,000ms | Fail |
| P99 response time | < 3,000ms | Warn |
| Error rate | < 1% | Fail |
| Throughput | > 2,000 req/s | Warn |
| CPU utilisation | < 85% | Warn |
| Memory utilisation | < 80% | Warn |

**Tab 3 — Run History:**
Last 10 runs of this scenario with pass/fail and key metrics. Trend chart of P95 response time over runs.

---

## Tab 4 — Baselines

Performance baselines capture the expected performance characteristics of the system. New test results are compared against baselines to detect regressions.

### Baseline Summary

Current baselines table:

| Baseline Name | Set On | Set By | P95 Response | Throughput | Max VU | Status |
|---|---|---|---|---|---|---|
| v4.1 — Production | 1 Feb 2026 | Deepa Menon | 520ms | 2,840 req/s | 15,000 | Active |
| v4.2 — Staging | 15 Mar 2026 | Deepa Menon | 480ms | 3,120 req/s | 15,000 | Active (candidate) |
| Exam Day Baseline | 10 Nov 2025 | Deepa Menon | 880ms | 4,200 req/s | 50,000 | Active |
| Result Release Baseline | 14 Nov 2025 | CI Pipeline | 1,240ms | 5,400 req/s | 74,000 | Active |

**Baseline Comparison:**
For each active test run, a "vs Baseline" column shows:
- Green ✓: metric is same or better than baseline
- Amber ⚠: metric degraded by 5–20%
- Red ✗: metric degraded by > 20% — regression alert

### Set New Baseline Modal

After a test run passes all SLA thresholds, PM or QA can set it as the new baseline:
- Select which run to use
- Baseline name (e.g. "v4.2 Production")
- Notes
- Confirm: "This will be used for all future regression comparisons"

---

## Tab 5 — SLA Tracker

Central record of all performance SLAs and their current compliance status.

### Platform SLA Definitions

| SLA | Metric | Threshold | Priority |
|---|---|---|---|
| Portal page load | P95 time to first byte | < 500ms | P0 |
| Exam next-question API | P95 response | < 200ms | P0 |
| Exam submit API | P95 response | < 1,000ms | P0 |
| Result page load | P95 response | < 800ms | P0 |
| Login API | P95 response | < 300ms | P1 |
| Leaderboard API | P95 response | < 1,500ms | P1 |
| Dashboard load | P95 response | < 1,200ms | P1 |
| Error rate (any endpoint) | % of requests | < 1% | P0 |
| Uptime | Monthly availability | 99.9% | P0 |
| Peak concurrent support | Concurrent users | 74,000 | P1 |

### SLA Compliance Table

| SLA | Threshold | Last Measured | Current Value | Status | Trend |
|---|---|---|---|---|---|
| Exam next-question | < 200ms | 2h ago | 145ms | ✓ Compliant | Improving ↓ |
| Exam submit | < 1,000ms | 2h ago | 618ms | ✓ Compliant | Stable |
| Result page load | < 800ms | 2h ago | 890ms | ✗ Breaching | Degrading ↑ |
| Leaderboard | < 1,500ms | 2h ago | 1,240ms | ✓ Compliant | Stable |

Breaching SLAs shown with red row background.

**SLA Breach History:**

Table of all historical SLA breaches:
- SLA name · Breach date · Measured value · Threshold · Duration of breach · Root cause · Resolution

---

## Tab 6 — Infrastructure

Infrastructure capacity planning and current state.

### Capacity Summary

| Resource | Current | Peak (exam day) | Limit | Headroom |
|---|---|---|---|---|
| Web servers (Gunicorn) | 4 × 8 workers = 32 | 8 × 8 workers = 64 | 16 servers | 50% |
| Database connections | 240 active | 480 peak | 600 limit | 20% |
| Redis memory | 12 GB | 18 GB peak | 32 GB | 43% |
| Celery workers | 20 | 40 peak | 80 | 50% |
| Storage | 2.4 TB | — | 5 TB | 52% |

### Auto-scaling Configuration

| Resource | Trigger | Scale Up | Scale Down |
|---|---|---|---|
| Web servers | CPU > 70% for 2 min | +2 servers | CPU < 40% for 5 min → -1 server |
| Celery workers | Queue depth > 500 tasks | +5 workers | Queue depth < 50 for 5 min → -2 workers |
| Database replicas | Replica lag > 2s | Add read replica | Replica idle for 30 min → remove |

### Capacity Recommendations

Algorithm-generated recommendations based on performance test results and growth trends:
- "SSC result release on Apr 15 expected to generate 74K concurrent users. Pre-provision 16 web servers from 14:00 IST."
- "Database connection pool at 80% during peak. Recommend increasing max_connections from 600 to 800."

---

## Tab 7 — Reports

Generated performance reports for management and stakeholders.

### Available Reports

| Report Name | Content | Generated |
|---|---|---|
| Weekly Performance Summary | KPIs for last 7 days: response times, error rates, SLA compliance | Every Monday |
| Release Performance Report | Performance comparison before/after each release | After each release |
| Quarterly Capacity Review | Infrastructure usage trends and capacity planning recommendations | Quarterly |
| Exam Day Readiness Report | Pre-exam performance verification report | Before each major exam date |
| SLA Compliance Report | Monthly SLA compliance percentage | Monthly |

### "Generate Report" Button

Triggers report generation for a custom date range. Format: PDF / CSV.

---

## New Performance Test Run Modal

**Step 1 — Select Scenario:**
- Scenario selector (dropdown of all scenarios)
- Or "Custom" for ad-hoc configuration

**Step 2 — Configure (if Custom):**
- Virtual users
- Ramp-up time (seconds)
- Duration (minutes)
- Target environment
- User behaviour mix (sliders summing to 100%)

**Step 3 — SLA Thresholds:**
- Review default SLA thresholds for selected scenario
- Override any threshold for this specific run

**Step 4 — Start:**
- Run name (auto-generated but editable)
- "Start Run" button

After start: run appears in Test Runs tab with "Running" status. Real-time metrics shown in Run Detail Drawer.

---

## Performance Test Notifications

| Event | Recipients | Channel |
|---|---|---|
| Test run started | QA Lead + PM Platform | In-App |
| Test run completed — Passed | QA Lead | In-App |
| Test run completed — Failed | QA Lead + PM Platform + Engineering Lead | In-App + Email |
| SLA breach detected during run | PM Platform + Engineering Lead | In-App + Slack |
| New performance regression detected (vs baseline) | QA Lead + PM Platform | In-App + Email |
| Infrastructure auto-scaling triggered during test | PM Platform | In-App |
| Test run aborted | Initiator | In-App |

P0 SLA breaches during production monitoring (from real traffic) additionally notify the on-call engineer.

---

## Incident Response During Performance Test Failure

When a performance test run fails (P95 exceeds SLA or error rate > 1%):

**Immediate Actions panel (shown in Run Detail Drawer when run fails):**
1. "Abort Further Load" — ramp down VUs immediately to prevent infrastructure damage
2. "Create Incident" — opens incident report form pre-filled with run ID, failed metrics, and environment
3. "Notify Team" — sends performance failure notification to engineering Slack channel
4. "Compare with Last Pass" — side-by-side comparison of current failed run vs last passing run

**Root Cause Analysis checklist shown in drawer:**
- Database: slow queries? (link to DB explain output)
- Gunicorn workers: queue depth spike? (link to infrastructure tab)
- Celery: backup in task queue? (link to automation monitor)
- Redis: evictions? (link to infrastructure tab)
- Code changes since last baseline (link to deployment log)

---

## Test Data Management

Performance tests use synthetic test data that mirrors production scale.

### Test Data Inventory (for Staging/UAT)

| Data Type | Count | Refresh Frequency |
|---|---|---|
| Student accounts | 500,000 | Monthly |
| Institution accounts | 1,950 | Quarterly |
| Exam records | 50,000 | Monthly |
| Question bank | 2,000,000 | Static |
| Past attempt records | 50,000,000 | Annual |
| Active exam sessions (live during test) | 200 simultaneous | Created fresh per test |

**Data Generation:**
- Managed by Celery task "populate_performance_test_data"
- Synthetic data uses faker library with Indian name patterns, phone numbers, email domains
- DPDPA compliant: no real student PII in test environments
- Student passwords: all set to "TestPass123!" for performance test accounts

**"Refresh Test Data" button** (in Infrastructure tab): triggers Celery task to regenerate test data. Warning: takes 2–4 hours for full dataset. Available to QA Lead and PM Platform only.

---

## Integration with Release Management

Performance testing is a release gate. Integration with Release Manager (page 03):

- Every release has a "Performance Gate" criterion in the release checklist
- Performance Gate is passed when: latest performance test run for the release passes all SLA thresholds
- Test run can be "linked" to a release from the run detail drawer
- Release Manager shows: linked performance test run ID + pass/fail + key metrics (P95, error rate)
- Release cannot be deployed without a passed performance test (unless PM Platform explicitly overrides with justification)

### Performance Gate Criteria per Release Type

| Release Type | Required Scenario | VU Target | P95 Threshold |
|---|---|---|---|
| Major (M.0.0) | Exam Day Peak | 50,000 VU | < 1,000ms |
| Minor (M.M.0) | Peak Load | 15,000 VU | < 750ms |
| Patch (M.M.P) | Normal Load | 5,000 VU | < 500ms |
| Hotfix | Smoke Test only | 1,000 VU | < 500ms |

---

## Load Test Tool Integration

The SRAV platform uses k6 (Grafana k6) as the load test engine, orchestrated through the performance test dashboard.

**Tool configuration** (shown in Infrastructure tab under "Load Test Config"):
- k6 version: displayed
- Test script location: S3 bucket path (masked)
- VU scaling: k6 cloud or self-hosted k6 agents (configurable)
- Metrics destination: InfluxDB → Grafana dashboard (URL shown)
- Results also stored in SRAV's own database for this dashboard

**k6 Script Management:**
Scripts are version-controlled. When a QA engineer edits a scenario's configuration, the dashboard generates the updated k6 script automatically. The script is stored in S3 and can be downloaded from the Scenario Detail drawer for manual execution.

---

## Key Design Decisions

| Concern | Decision | Rationale |
|---|---|---|
| 74K peak as design target | Hardcoded as the benchmark | 74K represents the known worst-case (national result release); must be tested before each major release |
| Scenario library | Pre-defined scenarios | Most performance tests are repeatable; library saves setup time and ensures consistency |
| Baseline comparison | Automatic regression detection | Performance regressions are often invisible until production; baseline comparison makes them visible in pre-production |
| Endpoint breakdown table | Per-endpoint metrics | Slowest endpoints need targeted optimisation; aggregate metrics alone don't show what to fix |
| Infrastructure metrics in drawer | Co-located with test results | Understanding which server was saturated during a slow test is essential for root cause analysis |
| SLA Tracker as separate tab | Not embedded in test runs | SLAs are ongoing commitments; they need a dedicated view separate from individual test runs |
| Result release spike scenario | Separate scenario | The 0→74K in 5min spike pattern is unique and catastrophically different from gradual load; it deserves dedicated simulation |
| Performance gate per release type | Different VU targets per type | Hotfixes should not need a full 50K VU test; tiered requirements balance quality gate rigor with release speed |
| Incident response panel in drawer | Immediate action buttons on failure | Performance failures need fast triage; buttons reduce time from failure detection to action |
| Test data scale | 500K students, 50M attempts | Test data must mirror production scale or performance results are not representative |
| DPDPA compliance for test data | Synthetic data only, no real PII | Test environments cannot contain real student data — regulatory requirement |

| Concurrent submit storm | Dedicated scenario | All students submitting at exam end simultaneously is a real and predictable pattern that causes distinct load spikes |
