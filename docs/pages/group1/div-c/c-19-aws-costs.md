# C-19 — AWS Infrastructure Cost Monitor

> **Route:** `/engineering/aws-costs/`
> **Division:** C — Engineering
> **Primary Role:** Platform Admin (Role 10) · DevOps/SRE (Role 14)
> **Read Access:** AI/ML Engineer (Role 17)
> **File:** `c-19-aws-costs.md`
> **Priority:** P1
> **Status:** ✅ Spec done

---

## 1. Page Name & Route

**Page Name:** AWS Infrastructure Cost Monitor
**Route:** `/engineering/aws-costs/`
**Part-load routes:**
- `/engineering/aws-costs/?part=kpi` — infrastructure cost KPI strip
- `/engineering/aws-costs/?part=summary` — monthly spend summary
- `/engineering/aws-costs/?part=by-service` — cost by AWS service table
- `/engineering/aws-costs/?part=trend` — month-over-month trend chart
- `/engineering/aws-costs/?part=anomalies` — cost anomaly alerts
- `/engineering/aws-costs/?part=ri-coverage` — Reserved Instance coverage
- `/engineering/aws-costs/?part=drawer&service={name}` — service cost drawer (aws-cost-drawer)
- `/engineering/aws-costs/?part=exam-events` — cost breakdown per exam peak event

---

## 2. Purpose (Business Objective)

AWS infrastructure costs are the platform's largest fixed operational expense at ₹70,000–₹90,000 per month. Unlike AI API costs (C-16) which scale with pipeline usage, infrastructure costs are driven by provisioned capacity, data transfer, and storage — often through invisible accumulators like CloudFront egress, RDS I/O, and S3 lifecycle transitions.

This page gives Platform Admins and DevOps Engineers a complete view of where infrastructure money is going, which services are trending up, and where Reserved Instance coverage can reduce costs. It pulls live data from the AWS Cost Explorer API rather than relying on AWS console access, which is locked down to a minimal set of IAM principals.

**Business goals:**
- Real-time and month-to-date visibility into AWS spend per service
- Month-over-month trend to identify cost regressions after deployments or scaling events
- Cost anomaly detection: catch unexpected spend spikes before they show up in the monthly invoice
- Reserved Instance coverage tracking: ensure committed spend is applied correctly to save 40–60% vs on-demand
- Cost attribution to exam peak events: understand how much each national exam day costs in infrastructure
- ₹ spend forecast for the current month based on burn rate

---

## 3. User Roles

| Role | Access Level | Permissions |
|---|---|---|
| Platform Admin (10) | Level 5 | Full view + write: Reserved Instance purchase recommendations · budget alerts |
| DevOps / SRE (14) | Level 4 | Full view; cannot modify budget alerts (read + export only) |
| AI/ML Engineer (17) | Level 4 — Read | View AI-relevant services only (Lambda, ECS AI workers) — to correlate with C-16 AI costs |

---

## 4. Section-Wise Detailed Breakdown

---

### Section 1 — Page Header & Monthly Cost Health

**Purpose:** Instant monthly spend status and forecast.

**Cost Health Banner:**

| State | Colour | Text |
|---|---|---|
| ✅ Within budget | Green | "MTD infra spend: ₹52,400 of ₹80,000 budget (65.5%) · On track" |
| ⚠ 80% alert | Amber | "MTD infra spend: ₹65,200 of ₹80,000 budget (81.5%) · Projected: ₹83,400 at month end" |
| 🚨 Budget overrun forecast | Red | "Projected month-end: ₹94,200 — exceeds ₹80,000 budget by ₹14,200" |

**Header elements:**
- H1 "AWS Infrastructure Cost Monitor"
- Cost health banner with % progress bar
- "Data as of: {timestamp}" — Cost Explorer API data is delayed 24–48h; shown as info note
- "Last refreshed: 2h ago" — Celery job refresh cadence
- "Export CSV" button → full cost breakdown for the selected period
- Date range selector: Current month · Last month · Last 3 months · Custom

---

### Section 2 — KPI Strip

**KPI Cards:**

| Card | Metric | Alert |
|---|---|---|
| MTD Infrastructure Spend | ₹ total from all AWS services | — |
| Projected Month-End | ₹ extrapolated from current burn rate | > monthly budget = red |
| vs Last Month | % change in total spend | > +20% = amber |
| RI Coverage | % of eligible hours covered by Reserved Instances | < 70% = amber |
| Cost Anomalies (7d) | Count of spend spikes above baseline | > 0 = amber |
| Savings vs On-Demand | ₹ saved via Reserved Instances vs equivalent on-demand pricing | — |

---

### Section 3 — Cost by AWS Service Table

**Purpose:** The primary view — how much each AWS service costs this month.

**Service Cost Table (MTD):**

| Service | MTD Cost (₹) | vs Last Month | Daily Avg | % of Total | Top Cost Driver | Actions |
|---|---|---|---|---|---|---|
| RDS (PostgreSQL) | ₹18,400 | +2.1% | ₹620 | 35.1% | Storage I/O + Multi-AZ | View detail |
| Lambda | ₹8,200 | -1.4% | ₹274 | 15.6% | Request count + duration | View detail |
| CloudFront | ₹7,400 | +4.8% | ₹246 | 14.1% | Data transfer out | View detail |
| ECS (Celery workers) | ₹6,100 | +0.8% | ₹203 | 11.6% | Fargate compute hours | View detail |
| S3 | ₹4,200 | -0.5% | ₹140 | 8.0% | Storage + PUT requests | View detail |
| ElastiCache (Memcached) | ₹2,800 | 0% | ₹93 | 5.3% | 3 cache.t3.medium nodes | View detail |
| SES | ₹1,200 | +12.4% | ₹40 | 2.3% | Email volume increase | View detail |
| Secrets Manager | ₹420 | 0% | ₹14 | 0.8% | API calls | View detail |
| ACM | ₹0 | — | ₹0 | 0% | Public certs free | — |
| Route53 | ₹840 | +1.2% | ₹28 | 1.6% | Hosted zone + queries | View detail |
| KMS | ₹380 | 0% | ₹12 | 0.7% | Key requests | View detail |
| CloudWatch | ₹680 | +8.4% | ₹22 | 1.3% | Logs storage + metrics | View detail |
| SNS / SQS | ₹260 | 0% | ₹8 | 0.5% | Queue operations | View detail |
| **Total** | **₹52,400** | **+1.8%** | **₹1,747** | **100%** | | |

**Colour rules:**
- vs Last Month: green if decrease · amber if +10–20% · red if > +20%
- % of Total: services > 30% of total cost get an amber flag (concentration risk)

**Filter/sort:** Sort by MTD Cost (default) · vs Last Month · Daily Avg · Service name

**"View detail" → opens aws-cost-drawer (560px)**

---

### Section 4 — AWS Cost Drawer (aws-cost-drawer)

**Purpose:** Deep dive into a specific AWS service's cost breakdown.

**Drawer Width:** 560px
**Tabs:** Daily Spend Chart · Top Cost Drivers · Forecast

---

#### Tab 1 — Daily Spend Chart

**Chart:** Bar chart — daily cost (₹) for this service over the last 30 days
- Colour: blue bars; red bar on days that exceeded daily budget for this service
- Overlay line: 7-day rolling average
- Annotations: "Exam day" markers on days with major exam events (from `platform_exam_events` table)

**Summary metrics for this service (MTD):**
- Total spend: ₹18,400
- Peak day: Mar 15 (₹840 — exam day, 2.4× avg)
- Lowest day: Mar 1 (₹290)
- Average daily: ₹620

---

#### Tab 2 — Top Cost Drivers

**Purpose:** Show which sub-components of the service are driving cost.

For RDS, the breakdown would be:

| Cost Component | MTD Cost | % of RDS Total | Notes |
|---|---|---|---|
| RDS instance hours (Multi-AZ) | ₹11,200 | 60.9% | db.r6g.xlarge × 3 instances (primary + 2 replicas) |
| Storage (gp3) | ₹2,800 | 15.2% | 2 TB provisioned + I/O |
| Backup storage | ₹2,100 | 11.4% | 30-day automated backups |
| Data transfer (in) | ₹840 | 4.6% | Replication + Lambda connections |
| Snapshot storage | ₹1,460 | 7.9% | Manual + pre-migration snapshots |

For Lambda:

| Cost Component | MTD Cost | % of Lambda Total |
|---|---|---|
| Request count | ₹1,240 | 15.1% |
| GB-seconds (compute duration) | ₹6,960 | 84.9% |

For CloudFront:

| Cost Component | MTD Cost | % of CloudFront Total |
|---|---|---|
| Data transfer out (India region) | ₹5,400 | 73.0% |
| HTTP request count | ₹1,200 | 16.2% |
| Data transfer to origin | ₹800 | 10.8% |

Data sourced from Cost Explorer with `GroupBy: USAGE_TYPE` dimension.

---

#### Tab 3 — Forecast

**Purpose:** Project end-of-month cost for this specific service.

| Metric | Value |
|---|---|
| MTD spend | ₹18,400 |
| Days elapsed | 20 of 31 |
| Daily burn rate (7-day avg) | ₹640 |
| Projected month-end | ₹18,400 + (11 × ₹640) = ₹25,440 |
| vs Last month actual | ₹24,200 (+5.1%) |
| vs Budget for this service | ₹26,000 (within budget) |

**Drivers of change:** "RDS cost increase driven by: +400 GB storage growth (question bank expansion) + 12% more I/O from new pgvector HNSW index queries."

---

### Section 5 — Month-over-Month Trend Chart

**Purpose:** Visual view of infrastructure cost evolution over the last 3 months.

**Chart type:** Grouped bar chart — one bar group per month, one bar per AWS service (colour-coded)
- Services with < 1% of total grouped into "Other"
- Toggle: Stacked view (absolute ₹) / Grouped view (per-service bars) / Line view (total only)

**Trend table (summary):**

| Month | Total Spend | vs Prior Month | Biggest Increase | Biggest Decrease |
|---|---|---|---|---|
| Jan 2026 | ₹71,200 | +3.4% | CloudFront (+18%) | S3 (-4%) |
| Feb 2026 | ₹74,800 | +5.1% | RDS (+8%) | Lambda (-2%) |
| Mar 2026 (MTD, proj.) | ₹79,200 | +5.9% | SES (+12%) | ECS (-1%) |

**Key events overlay:** Horizontal annotations on the chart — "Deployed pgvector index (Jan 8)" · "Moved to gp3 storage (Feb 14)" — pulled from `platform_infra_events` table.

---

### Section 6 — Cost Anomaly Alerts

**Purpose:** Surface unexpected spend spikes before they become large problems.

**Anomaly Detection Method:**
AWS Cost Anomaly Detection service monitors daily spend per service. A spend spike is flagged if daily cost deviates > 2 standard deviations from the 14-day rolling average for that service.

**Anomaly Log (last 30 days):**

| Date | Service | Expected Daily | Actual Daily | Deviation | Root Cause (manual) | Status |
|---|---|---|---|---|---|---|
| Mar 15 | CloudFront | ₹246 | ₹840 | +241% | JEE exam day traffic spike | ✅ Expected |
| Mar 8 | SES | ₹40 | ₹184 | +360% | Bulk exam reminder emails sent | ✅ Expected |
| Feb 22 | Lambda | ₹274 | ₹690 | +152% | Runaway AI job (duplicate trigger) | ❌ Unplanned — resolved |

**Actions per anomaly:**
- "Mark as expected" → removes from unresolved count; requires reason
- "Investigate" → links to C-08 Infrastructure Monitor for the affected service on that date
- "Create C-18 incident" → if the anomaly is caused by a real problem

**Anomaly alert configuration:**
- Alert threshold: configurable per service (default: > 2σ deviation)
- Alert recipient: Platform Admin + DevOps email
- AWS Cost Anomaly Detection service used as the detection engine; results synced to `platform_cost_anomalies` table hourly by Celery

---

### Section 7 — Reserved Instance Coverage

**Purpose:** Show how much of eligible compute usage is covered by Reserved Instances (RIs) vs on-demand pricing — and what savings are being generated.

**RI Coverage Summary:**

| Service | Eligible Instance Hours (MTD) | RI-Covered Hours | RI Coverage % | On-Demand Cost | RI Cost | Savings |
|---|---|---|---|---|---|---|
| RDS (db.r6g.xlarge) | 1,460 hours | 1,460 hours | 100% | ₹18,400 est. | ₹11,200 actual | ₹7,200 (39%) |
| ElastiCache (cache.t3.medium) | 2,190 hours | 2,190 hours | 100% | ₹4,200 est. | ₹2,800 actual | ₹1,400 (33%) |
| ECS Fargate | 3,600 vCPU-hours | 1,800 vCPU-hours | 50% | ₹12,200 est. | ₹6,100 actual | ₹6,100 (50%) |
| Lambda | N/A (no RI for Lambda) | — | — | ₹8,200 | ₹8,200 | ₹0 |

**Total RI savings MTD: ₹14,700**

**Coverage gaps:**
- ECS Fargate at 50% coverage: amber flag — "Consider purchasing additional Fargate Savings Plan to cover ~50% of on-demand compute"
- Estimated additional savings if 80% RI coverage on ECS: ₹2,440/month

**RI expiry calendar:**
- RDS RI expires: Dec 2026 (renewal recommended 60 days before)
- ElastiCache RI expires: Jan 2027

**Actions (Admin only):**
- "View RI purchase recommendations" → links to AWS console with pre-calculated recommendation (DevOps/Admin only; purchase is in AWS console, not in platform)
- "Set RI coverage alert" → alert if coverage drops below configurable % (e.g., < 70%)

---

### Section 8 — Exam Peak Event Cost Breakdown

**Purpose:** Understand the infrastructure cost per major exam event — the incremental cost of scaling up for a national exam day vs baseline.

**Exam Event Cost Table (last 6 events):**

| Exam | Date | Duration | Peak Concurrent Students | Incremental Lambda Cost | Incremental CloudFront Cost | Incremental RDS I/O | Total Incremental Cost |
|---|---|---|---|---|---|---|---|
| JEE Main Session 1 | Jan 22, 2026 | 3h | 84,200 | ₹2,840 | ₹1,200 | ₹420 | ₹4,460 |
| NEET Mock | Feb 5, 2026 | 2h | 22,400 | ₹840 | ₹320 | ₹120 | ₹1,280 |
| JEE Advanced | Mar 15, 2026 | 6h | 48,400 | ₹1,840 | ₹840 | ₹280 | ₹2,960 |

**Incremental cost calculation method:**
- Baseline daily cost established from the 7-day pre-event average
- Event day actual cost − baseline = incremental cost attributed to the exam event
- Cost data from AWS Cost Explorer with hourly granularity (filters to exam window hours)

**Per-student cost efficiency:**
- JEE Main: ₹4,460 / 84,200 students = ₹0.053 per student-exam
- JEE Advanced: ₹2,960 / 48,400 students = ₹0.061 per student-exam

**Cost efficiency trend:** If cost per student-exam is increasing over time, it may indicate over-provisioning or inefficient Lambda cold-start management during exam day.

**Use cases for this data:**
- Pricing model: understanding true infrastructure cost per exam session for institution pricing
- Capacity planning: sizing Lambda provisioned concurrency budgets for next exam season
- C-10 Scaling correlation: links to scaling actions taken in C-10 during each event

---

## 5. User Flow

### Flow A — Monthly Cost Review

1. DevOps Engineer opens `/engineering/aws-costs/` on the 20th of the month
2. KPI: MTD spend ₹52,400 · projected ₹79,200 · within ₹80,000 budget (green)
3. Service table: SES +12.4% vs last month (amber flag)
4. Clicks "View detail" on SES → aws-cost-drawer → Top Cost Drivers: email volume up 12%
5. Traces cause: new "exam day reminder" email feature (launched Mar 8) sending 3 emails per student vs previous 1
6. Notes in anomaly log: "Mar 8 SES spike = expected (feature launch)"
7. No action needed — projected cost still within budget
8. Exports CSV for monthly infrastructure report to Platform Admin

### Flow B — Cost Anomaly Investigation

1. Celery alert fires: "Lambda spend spike detected — ₹690 on Feb 22 (expected ₹274)"
2. DevOps opens anomaly log → finds unresolved anomaly
3. Clicks "Investigate" → links to C-08 Celery Queues tab (G4 amendment) for Feb 22
4. Identifies: 5 duplicate AI pipeline jobs ran simultaneously (same job triggered twice by bug)
5. Root cause: "Runaway AI job — duplicate trigger" → marks anomaly as resolved
6. Creates C-18 incident for the duplicate job trigger bug
7. Lambda spend returns to normal next day — ₹268

### Flow C — Reserved Instance Planning

1. Platform Admin reviews RI coverage quarterly
2. ECS Fargate: 50% coverage (amber)
3. DevOps calculates: additional Fargate Savings Plan at 80% coverage saves ₹2,440/month = ₹29,280/year
4. Platform Admin approves purchase — opens AWS console from "View RI recommendations" link
5. After purchase: ECS coverage moves to 80%; savings reflected in next day's cost data

---

## 6. Component Structure (Logical)

```
AWSCostMonitorPage
├── PageHeader
│   ├── CostHealthBanner
│   ├── PageTitle
│   ├── DataFreshnessNote
│   ├── DateRangeSelector
│   └── ExportCSVButton
├── KPIStrip × 6
├── ServiceCostTable
│   ├── FilterBar
│   └── ServiceRow × N
├── AWSCostDrawer (560px)
│   └── DrawerTabs
│       ├── DailySpendChartTab
│       ├── TopCostDriversTab
│       └── ForecastTab
├── MonthOverMonthTrendChart
│   └── TrendSummaryTable
├── CostAnomalyAlertsPanel
│   ├── AnomalyLog
│   └── AnomalyAlertConfig
├── ReservedInstanceCoveragePanel
│   ├── RICoverageTable
│   ├── RIExpiryCalendar
│   └── RISavingsGapsSection
└── ExamPeakEventCostPanel
    ├── ExamEventCostTable
    └── PerStudentEfficiencyMetrics
```

---

## 7. Data Model (High-Level)

### platform_aws_cost_daily (synced from Cost Explorer)

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| date | DATE | |
| service | VARCHAR(100) | AWS service name (e.g., "Amazon RDS") |
| usage_type | VARCHAR(200) | Sub-component (e.g., "RDS:GP3-Storage") |
| cost_inr | DECIMAL(10,2) | Converted from USD using daily exchange rate |
| cost_usd | DECIMAL(10,4) | Raw USD from Cost Explorer |
| region | VARCHAR(50) | ap-south-1 (most costs) |
| synced_at | TIMESTAMPTZ | When this row was last fetched from API |

### platform_cost_anomalies

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| date | DATE | |
| service | VARCHAR(100) | |
| expected_cost_inr | DECIMAL(10,2) | Based on 14-day rolling average |
| actual_cost_inr | DECIMAL(10,2) | |
| deviation_pct | DECIMAL(6,2) | |
| status | ENUM | unresolved/expected/unplanned_resolved |
| root_cause | TEXT | nullable (set by DevOps) |
| resolved_by | UUID FK → platform_staff | nullable |
| resolved_at | TIMESTAMPTZ | nullable |
| detected_at | TIMESTAMPTZ | |

### platform_ri_coverage

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| month | DATE | first day of month |
| service | VARCHAR(100) | |
| instance_type | VARCHAR(100) | |
| eligible_hours | DECIMAL(10,2) | |
| ri_covered_hours | DECIMAL(10,2) | |
| coverage_pct | DECIMAL(5,2) | |
| on_demand_cost_inr | DECIMAL(10,2) | what it would cost without RI |
| ri_cost_inr | DECIMAL(10,2) | actual cost with RI |
| savings_inr | DECIMAL(10,2) | on_demand - ri |
| synced_at | TIMESTAMPTZ | |

### platform_exam_event_costs

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| exam_event_id | UUID FK → platform_exam_events | |
| exam_name | VARCHAR(200) | |
| event_date | DATE | |
| duration_hours | SMALLINT | |
| peak_concurrent_students | INTEGER | |
| baseline_cost_inr | DECIMAL(10,2) | 7-day avg daily cost |
| actual_event_cost_inr | DECIMAL(10,2) | |
| incremental_cost_inr | DECIMAL(10,2) | actual - baseline |
| cost_per_student_inr | DECIMAL(8,4) | incremental / peak students |
| cost_breakdown | JSONB | per-service incremental costs |

---

## 8. Validation Rules

| Rule | Detail |
|---|---|
| Cost data freshness | AWS Cost Explorer API has 24–48h delay; all cost data shown with "as of" timestamp; page never claims real-time costs |
| Budget edit | Admin only; monthly infrastructure budget stored in `platform_infra_budget_config` table; 2FA required for > 50% budget change |
| Anomaly mark as expected | Requires reason (min 20 chars); logged with actor + timestamp |
| RI purchase | Not done within platform — only recommendations shown; purchase via AWS console (link out); no write access to AWS RI APIs from platform |
| Cost export | CSV export limited to 12 months of data; larger exports require Platform Admin approval |
| Exchange rate | USD→INR rate fetched daily from a fixed source (configurable in `platform_system_config`); applied at time of data sync |

---

## 9. Security Considerations

| Control | Detail |
|---|---|
| AWS Cost Explorer IAM | `ce:GetCostAndUsage` + `ce:GetCostAndUsagePredictions` + `ce:GetAnomalyDetectors` — read-only; no billing modification permissions |
| No AWS billing credentials in DB | Cost Explorer API calls made from a dedicated Lambda with IAM role (not access keys); role scoped to Cost Explorer only |
| Cost data sensitivity | AWS costs reveal infrastructure scale and architecture; page restricted to Admin + DevOps + limited AI/ML read; not visible to institution-facing roles |
| RI recommendation data | Contains instance type and usage details; same access restriction |
| Export CSV | Logged with actor + timestamp; exported file contains cost data only, not system architecture details |

---

## 10. Edge Cases (System-Level)

| Scenario | Handling |
|---|---|
| Cost Explorer API unavailable | Page loads from last-synced `platform_aws_cost_daily` data with "API unavailable — showing last synced data from {timestamp}" warning; Celery retries hourly |
| Exchange rate not available | Previous day's rate used with "(est.)" label; alert to DevOps if exchange rate has not been fetched for > 24h |
| New AWS service appears in bill | New service row appears in cost table automatically on next sync; "New" badge on first appearance; DevOps can add description/category |
| Cost anomaly during exam day | System auto-checks: if anomaly date has an `platform_exam_event` record → auto-tags as "Expected (exam day)" and moves to expected category without DevOps action |
| Multiple anomalies for same service in one day | Only the single highest-deviation anomaly shown per service per day; details in drawer |
| Reserved Instance purchased externally (not tracked) | RI coverage table shows lower coverage temporarily until next sync from AWS API |

---

## 11. Performance & Scaling Strategy

| Concern | Strategy |
|---|---|
| Cost data sync | Celery beat job runs every 6 hours; fetches last 7 days of Cost Explorer data (API has 24–48h delay anyway); incremental sync — only fetches dates where data changed |
| Service cost table | Pre-aggregated from `platform_aws_cost_daily` per month; single GROUP BY query < 30ms for 31 days × 15 services |
| Trend chart | Pre-aggregated monthly totals from same table; 3 months × 15 services = 45 rows; trivial query |
| Anomaly detection | AWS Cost Anomaly Detection service runs server-side (not in platform); platform only reads results via `GetAnomalyMonitors` API every 6 hours |
| Cost drawer daily chart | 30 rows per service; fetched on drawer open; < 20ms |
| Exam event correlation | `platform_exam_events` table joined with `platform_aws_cost_daily` on date; both tables small; < 50ms |
