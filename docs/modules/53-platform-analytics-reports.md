# Module 53 — Platform Analytics & Reports

## 1. Purpose & Scope

Platform Analytics & Reports is the super-admin and TSP-level intelligence layer for EduForge. It aggregates data across all tenants, institution types, users, and services to produce actionable business intelligence, operational observability, financial reporting, and compliance evidence.

Unlike tenant-level analytics (Module 47 — AI Performance Analytics, which focuses on student outcomes inside a single institution), this module operates at the platform layer: revenue health, tenant churn risk, infrastructure cost allocation, AI spend tracking, compliance audit trails, and white-label reporting for TSPs.

Primary consumers:
- **EduForge super-admins** — full platform visibility
- **TSP admins** — their tenant portfolio and billing data only
- **Tenant admins** — their own institution data only (narrowly scoped)
- **Finance & Legal teams** — financial reports and compliance evidence

---

## 2. Data Pipeline Architecture

### 2.1 S3 Data Lake — Three Zones

```
Raw Zone (s3://analytics-eduforge/raw/)
  └── event_logs/year=/month=/day=/
  └── db_snapshots/year=/month=/day=/
  └── bedrock_usage/year=/month=/day=/

Curated Zone (s3://analytics-eduforge/curated/)
  └── fact_api_calls/       ← Parquet, partitioned tenant_id/date
  └── fact_exam_sessions/   ← Parquet, partitioned tenant_id/date
  └── fact_payments/        ← Parquet, partitioned tenant_id/date
  └── dim_tenants/          ← Parquet, full refresh nightly
  └── dim_users/            ← Parquet (anonymized), full refresh nightly

Aggregated Zone (s3://analytics-eduforge/aggregated/)
  └── daily_tenant_metrics/ ← Pre-computed rollups, tenant_id/date
  └── daily_platform_kpis/  ← Platform-wide daily KPIs
  └── monthly_revenue/      ← MRR components, monthly
```

All zones use **Apache Parquet** format with **Snappy** compression. Column pruning reduces Athena bytes-scanned by ~70% vs. raw JSON.

### 2.2 Ingestion Pipelines

**Pipeline A — Application Events:**
```
DynamoDB Streams (usage counters, subscription changes, feature gate hits)
  → EventBridge Pipes (filter + transform)
  → SQS analytics-ingest queue
  → Lambda analytics-writer (batch of 100 events)
  → S3 raw zone (JSON, partitioned by hour)
```

**Pipeline B — Transactional Database:**
```
PostgreSQL (pglogical logical replication)
  → Lambda pg-cdc-reader (reads replication slot)
  → Debezium-format JSON → S3 raw zone
  → (Tables: tenants, subscriptions, payments, fee_invoices, staff, audit_log)
```

**Pipeline C — Infrastructure Metrics:**
```
CloudWatch Metrics → CloudWatch Metric Streams
  → Kinesis Data Firehose (parquet conversion)
  → S3 raw zone (Lambda usage, API Gateway, ECS, RDS)
```

**Pipeline D — AI Cost Events:**
```
Bedrock invocation logs (enabled via CloudTrail)
  → S3 → Glue ETL → curated/fact_bedrock_usage (tenant_id, model, tokens_in, tokens_out, cost_usd)
```

### 2.3 AWS Glue ETL Jobs

| Job | Schedule | Input | Output |
|-----|----------|-------|--------|
| `raw-to-curated-events` | Every 15 min | raw/event_logs | curated/fact_api_calls |
| `raw-to-curated-payments` | Hourly | raw/db_snapshots (payments) | curated/fact_payments |
| `curated-to-aggregated-daily` | 01:00 IST | curated/* | aggregated/daily_tenant_metrics |
| `curated-to-aggregated-monthly` | 1st of month 02:00 IST | aggregated/daily | aggregated/monthly_revenue |
| `dim-refresh-tenants` | 00:30 IST | db_snapshots/tenants | dim_tenants |

Each Glue job uses **job bookmarks** — only new S3 objects since last run are processed. No full reprocessing.

Glue ETL SLA: nightly jobs must complete by 02:00 IST. CloudWatch alarm fires if any job overruns past 02:30 IST.

### 2.4 Athena Query Governance

Three Athena **workgroups** enforce cost controls:

```python
WORKGROUP_LIMITS = {
    "super_admin":    None,        # Unlimited (trusted)
    "tsp_admin":      100 * GB,    # Max 100 GB per query
    "tenant_admin":   10 * GB,     # Max 10 GB per query
}
```

All queries by non-super-admin roles are routed through a Lambda query proxy that appends a `WHERE tenant_id = ?` partition filter before execution — preventing cross-tenant data leakage regardless of the user's SQL.

```python
# analytics/query_proxy.py
def safe_query(sql: str, tenant_id: str, role: str) -> str:
    """
    Inject tenant_id filter into all non-super-admin queries.
    """
    if role == "super_admin":
        return sql
    # Parse and inject tenant filter
    ast = sqlparse.parse(sql)[0]
    safe_sql = inject_partition_filter(ast, "tenant_id", tenant_id)
    validate_scan_limit(safe_sql, WORKGROUP_LIMITS[role])
    return safe_sql
```

Query result cache: Athena caches results for 30 minutes. Dashboard queries that haven't changed parameters re-use cached results, reducing cost and latency.

---

## 3. Revenue Analytics

### 3.1 MRR Components

```sql
-- aggregated/monthly_revenue schema (Athena)
SELECT
    report_month,
    SUM(CASE WHEN change_type = 'new'       THEN mrr_delta ELSE 0 END) AS new_mrr,
    SUM(CASE WHEN change_type = 'expansion' THEN mrr_delta ELSE 0 END) AS expansion_mrr,
    SUM(CASE WHEN change_type = 'contraction' THEN mrr_delta ELSE 0 END) AS contraction_mrr,
    SUM(CASE WHEN change_type = 'churned'   THEN mrr_delta ELSE 0 END) AS churned_mrr,
    SUM(mrr_delta) AS net_new_mrr,
    starting_mrr + SUM(mrr_delta) AS ending_mrr
FROM aggregated.monthly_mrr_changes
WHERE report_month = DATE_TRUNC('month', CURRENT_DATE)
GROUP BY report_month, starting_mrr;
```

**Net Revenue Retention (NRR):**
```
NRR = (Expansion + Retained − Churned) / Prior MRR × 100
```
Target > 110% (expansion from existing tenants more than offsets churn).

**Gross Revenue Retention (GRR):**
```
GRR = Retained / Prior MRR × 100
```
Target > 85% (floor metric — excludes expansion).

### 3.2 Churn Cohort Heatmap

For tenants acquired in month X, what percentage remain active at months 1, 3, 6, 12, 24:

```sql
SELECT
    DATE_TRUNC('month', first_paid_date) AS cohort_month,
    months_since_start,
    COUNT(*) AS active_tenants,
    COUNT(*) * 100.0 / first_value(COUNT(*)) OVER (
        PARTITION BY DATE_TRUNC('month', first_paid_date)
        ORDER BY months_since_start
    ) AS retention_pct
FROM (
    SELECT
        t.tenant_id,
        t.first_paid_date,
        EXTRACT(MONTH FROM AGE(s.activity_month, t.first_paid_date)) AS months_since_start
    FROM dim_tenants t
    JOIN aggregated.monthly_tenant_activity s USING (tenant_id)
    WHERE s.is_active = TRUE
) sub
GROUP BY 1, 2
ORDER BY 1, 2;
```

### 3.3 Revenue Forecasting

```python
# analytics/forecasting.py
import numpy as np
from sklearn.linear_model import Ridge

def forecast_mrr(monthly_mrr_series: list[float], months_ahead: int = 3) -> list[float]:
    """
    Ridge regression with seasonality features for MRR forecasting.
    Academic year: April/May spike (new admissions), Dec/Jan dip.
    """
    n = len(monthly_mrr_series)
    X = []
    for i in range(n):
        month_of_year = (i % 12) + 1
        X.append([
            i,                             # Trend
            np.sin(2 * np.pi * i / 12),   # Annual seasonality (sin)
            np.cos(2 * np.pi * i / 12),   # Annual seasonality (cos)
            1 if month_of_year in (4, 5) else 0,   # Admission season bump
            1 if month_of_year in (12, 1) else 0,  # Year-end dip
        ])
    y = monthly_mrr_series
    model = Ridge(alpha=1.0).fit(X, y)

    forecasts = []
    for i in range(n, n + months_ahead):
        month_of_year = (i % 12) + 1
        x = [
            i,
            np.sin(2 * np.pi * i / 12),
            np.cos(2 * np.pi * i / 12),
            1 if month_of_year in (4, 5) else 0,
            1 if month_of_year in (12, 1) else 0,
        ]
        forecasts.append(float(model.predict([x])[0]))
    return forecasts
```

### 3.4 GST Data Export

```sql
-- GSTR-1 B2B invoice export for monthly GST filing
SELECT
    p.gstin AS recipient_gstin,
    SUM(p.base_amount) AS taxable_value,
    SUM(p.cgst_amount) AS cgst,
    SUM(p.sgst_amount) AS sgst,
    SUM(p.igst_amount) AS igst,
    p.invoice_month
FROM curated.fact_payments p
WHERE p.invoice_month = :filing_month
    AND p.payment_status = 'captured'
    AND p.gstin IS NOT NULL
GROUP BY p.gstin, p.invoice_month
ORDER BY p.gstin;
```

---

## 4. Tenant Health Score

### 4.1 Score Computation

```python
# analytics/tenant_health.py
from dataclasses import dataclass

@dataclass
class HealthComponents:
    login_frequency: float       # 0–20: active days / 30 days × 20
    feature_breadth: float       # 0–20: distinct modules used / 10 × 20
    student_growth: float        # 0–20: student MoM growth; 0% = 0, +10% = 20
    payment_history: float       # 0–20: 20 if no failed payments in 90 days
    support_burden: float        # 0–20: 20 if 0 tickets; 0 if ≥ 5 tickets/month

def compute_health_score(components: HealthComponents) -> float:
    return (
        components.login_frequency +
        components.feature_breadth +
        components.student_growth +
        components.payment_history +
        components.support_burden
    )

def health_tier(score: float) -> str:
    if score < 40:  return "RED"
    if score < 70:  return "YELLOW"
    return "GREEN"
```

### 4.2 Churn Risk Classifier

```python
# SageMaker XGBoost churn risk model (trained offline, deployed serverless)
FEATURES = [
    "health_score", "login_frequency_score", "feature_breadth_score",
    "student_growth_score", "payment_history_score", "support_burden_score",
    "days_since_last_login", "months_as_customer", "plan_tier_ordinal",
    "num_students", "tickets_last_30d", "bedrock_usage_pct_of_limit"
]

# Inference: SageMaker Serverless Endpoint (scales to zero)
def predict_churn_risk(tenant_features: dict) -> float:
    """Returns churn probability 0.0–1.0 within 30 days."""
    payload = [tenant_features[f] for f in FEATURES]
    response = sm_runtime.invoke_endpoint(
        EndpointName="churn-risk-serverless",
        Body=json.dumps({"instances": [payload]}),
        ContentType="application/json",
    )
    return json.loads(response["Body"].read())["predictions"][0]
```

Automated action: if `churn_probability > 0.7` → SQS message → Lambda creates CS task in PostgreSQL `cs_tasks` table + sends Slack notification to `#churn-risk` channel.

---

## 5. Platform Usage Metrics

### 5.1 DAU/MAU Stickiness

```python
# Computed nightly in aggregated zone
def compute_dau_mau(tenant_id: str, date: date) -> dict:
    dau = count_distinct_users(tenant_id, date, date)
    mau_start = date.replace(day=1)
    mau = count_distinct_users(tenant_id, mau_start, date)
    return {
        "dau": dau,
        "mau": mau,
        "stickiness": round(dau / mau, 4) if mau > 0 else 0.0
    }
# Target stickiness > 0.40 (40%) for healthy product engagement
```

### 5.2 AI Cost Per Student

```python
# Computed monthly per tenant
def ai_cost_per_student(tenant_id: str, month: str) -> dict:
    bedrock_cost = query_athena(f"""
        SELECT SUM(cost_usd) FROM curated.fact_bedrock_usage
        WHERE tenant_id = '{tenant_id}' AND invoice_month = '{month}'
    """)
    sagemaker_cost = query_athena(f"""
        SELECT SUM(cost_usd) FROM curated.fact_sagemaker_usage
        WHERE tenant_id = '{tenant_id}' AND invoice_month = '{month}'
    """)
    active_students = query_athena(f"""
        SELECT active_student_count FROM aggregated.monthly_tenant_metrics
        WHERE tenant_id = '{tenant_id}' AND report_month = '{month}'
    """)
    total_ai_cost_inr = (bedrock_cost + sagemaker_cost) * 84  # USD→INR
    per_student = total_ai_cost_inr / active_students if active_students > 0 else 0
    return {
        "bedrock_cost_inr": bedrock_cost * 84,
        "sagemaker_cost_inr": sagemaker_cost * 84,
        "active_students": active_students,
        "ai_cost_per_student_inr": round(per_student, 4),
        "target_inr": 0.10,
        "within_target": per_student <= 0.10,
    }
```

---

## 6. Report Generation Engine

### 6.1 Report Catalog

50+ pre-built report templates stored in `analytics.report_definitions`:

| Category | Example Reports |
|----------|----------------|
| Financial | MRR Waterfall, Churn Cohort, GST GSTR-1, Invoice Ageing, LTV Analysis |
| Operational | API Latency Summary, Lambda Cost Breakdown, R2 Storage by Tenant, Bedrock Usage |
| Compliance | DPDPA Consent Audit, POCSO Incident Summary, CERT-In Incident Log, BGV Completion |
| Academic | Platform Pass Rate Trends, AI Doubt Solver Resolution Rate, Feature Adoption |
| TSP | TSP Portfolio Health, TSP Billing Summary, White-label Domain Health |

### 6.2 Async Report Generation

```python
# analytics/report_runner.py
import boto3, uuid
from weasyprint import HTML
import openpyxl

class ReportRunner:
    def __init__(self):
        self.sqs = boto3.client("sqs")
        self.s3 = boto3.client("s3")

    def request_report(
        self,
        report_def_id: str,
        params: dict,
        requester_id: str,
        tenant_id: str,
        output_format: str = "pdf",
    ) -> str:
        job_id = str(uuid.uuid4())
        # Store job record
        db.execute("""
            INSERT INTO analytics.report_jobs
            (job_id, report_def_id, params, requester_id, tenant_id, status, output_format, created_at)
            VALUES (%s, %s, %s, %s, %s, 'queued', %s, NOW())
        """, [job_id, report_def_id, json.dumps(params), requester_id, tenant_id, output_format])
        # Enqueue
        self.sqs.send_message(
            QueueUrl=REPORT_QUEUE_URL,
            MessageGroupId=tenant_id,   # FIFO: 3 concurrent workers per tenant
            MessageBody=json.dumps({"job_id": job_id}),
        )
        return job_id

    def generate_pdf(self, html_content: str, job_id: str, tenant_id: str) -> str:
        pdf_bytes = HTML(string=html_content).write_pdf()
        s3_key = f"reports/{tenant_id}/{job_id}.pdf"
        self.s3.put_object(
            Bucket=REPORTS_BUCKET,
            Key=s3_key,
            Body=pdf_bytes,
            ContentType="application/pdf",
            ServerSideEncryption="AES256",
        )
        return s3_key

    def generate_excel(self, data: list[dict], sheet_name: str, job_id: str, tenant_id: str) -> str:
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = sheet_name
        if data:
            ws.append(list(data[0].keys()))  # Header row
            for row in data:
                ws.append(list(row.values()))
        from io import BytesIO
        buf = BytesIO()
        wb.save(buf)
        s3_key = f"reports/{tenant_id}/{job_id}.xlsx"
        self.s3.put_object(
            Bucket=REPORTS_BUCKET,
            Key=s3_key,
            Body=buf.getvalue(),
            ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            ServerSideEncryption="AES256",
        )
        return s3_key
```

### 6.3 Scheduled Reports via EventBridge

```python
# EventBridge rule per scheduled subscription
# Created when user subscribes to a report

def create_report_schedule(subscription: ReportSubscription):
    cron_map = {
        "daily":   "cron(0 6 * * ? *)",     # 06:00 IST = 00:30 UTC
        "weekly":  "cron(0 6 ? * MON *)",
        "monthly": "cron(0 6 1 * ? *)",
    }
    events_client.put_rule(
        Name=f"report-{subscription.id}",
        ScheduleExpression=cron_map[subscription.frequency],
        State="ENABLED",
    )
    events_client.put_targets(
        Rule=f"report-{subscription.id}",
        Targets=[{
            "Id": "lambda",
            "Arn": REPORT_SCHEDULER_LAMBDA_ARN,
            "Input": json.dumps({
                "subscription_id": subscription.id,
                "report_def_id": subscription.report_def_id,
                "params": subscription.params,
            }),
        }],
    )
```

Delivery: generated report stored in S3 → SES email with S3 pre-signed URL (7-day expiry) → in-app notification.

---

## 7. Custom Dashboards

### 7.1 Super-Admin Master Dashboard

```html
<!-- HTMX auto-refresh dashboard panels -->
<div class="dashboard-grid">

  <!-- Revenue KPIs - refreshes every 60s -->
  <div hx-get="/analytics/api/kpi/revenue"
       hx-trigger="every 60s"
       hx-swap="innerHTML">
    <!-- MRR, ARR, NRR, Churn Rate -->
  </div>

  <!-- Tenant Health Distribution -->
  <div hx-get="/analytics/api/kpi/tenant-health"
       hx-trigger="every 60s"
       hx-swap="innerHTML">
    <!-- RED/YELLOW/GREEN donut chart -->
  </div>

  <!-- Platform API Health -->
  <div hx-get="/analytics/api/kpi/api-health"
       hx-trigger="every 30s"
       hx-swap="innerHTML">
    <!-- P99 latency, 5xx rate, Lambda errors -->
  </div>

  <!-- AI Cost This Month -->
  <div hx-get="/analytics/api/kpi/ai-cost"
       hx-trigger="every 60s"
       hx-swap="innerHTML">
    <!-- Bedrock + SageMaker cost vs. budget -->
  </div>

  <!-- Real-time Activity Feed -->
  <div hx-get="/analytics/api/activity-feed"
       hx-trigger="every 15s"
       hx-swap="innerHTML">
    <!-- Last 20 significant events -->
  </div>

</div>
```

### 7.2 Custom Report Builder

```python
# analytics/custom_builder.py
ALLOWED_METRICS = {
    "active_tenants", "new_tenants", "churned_tenants", "mrr", "arr",
    "dau", "mau", "stickiness", "api_requests", "api_error_rate",
    "bedrock_cost_inr", "sagemaker_cost_inr", "r2_storage_gb",
    "exam_sessions", "doubts_resolved", "certificates_issued",
}

ALLOWED_DIMENSIONS = {
    "tenant_id", "institution_type", "state", "plan_tier", "date", "month",
}

def build_custom_query(metrics: list[str], dimensions: list[str], filters: dict, date_range: tuple) -> str:
    # Validate inputs against allowlists
    if not set(metrics).issubset(ALLOWED_METRICS):
        raise ValueError("Invalid metric requested")
    if not set(dimensions).issubset(ALLOWED_DIMENSIONS):
        raise ValueError("Invalid dimension requested")
    if len(metrics) > 10:
        raise ValueError("Maximum 10 metrics per custom report")

    select_cols = ", ".join(dimensions + [f"SUM({m}) AS {m}" for m in metrics])
    group_cols = ", ".join(dimensions)
    sql = f"""
        SELECT {select_cols}
        FROM aggregated.daily_tenant_metrics
        WHERE date BETWEEN DATE '{date_range[0]}' AND DATE '{date_range[1]}'
        GROUP BY {group_cols}
        ORDER BY date
    """
    return sql
```

---

## 8. Alerting & Anomaly Detection

### 8.1 CloudWatch Composite Alarms

```python
# infrastructure/alerts.py (CDK)
from aws_cdk import aws_cloudwatch as cw

# Composite: high error rate = 5xx > 1% AND P99 > 3s for 5 minutes
high_error_rate = cw.CompositeAlarm(
    scope, "HighErrorRate",
    alarm_rule=cw.AlarmRule.all_of(
        cw.AlarmRule.from_alarm(api_5xx_alarm, cw.AlarmState.ALARM),
        cw.AlarmRule.from_alarm(api_p99_alarm, cw.AlarmState.ALARM),
    ),
    composite_alarm_name="EduForge-HighErrorRate",
)
high_error_rate.add_alarm_action(
    cw_actions.SnsAction(operations_sns_topic)
)
```

### 8.2 Bedrock Cost Spike Detection

```python
# analytics/cost_anomaly.py
def check_bedrock_spike(tenant_id: str):
    """
    Alert if today's Bedrock token usage > 3× 7-day rolling average.
    Runs every hour via EventBridge scheduled rule.
    """
    today = query_athena(f"""
        SELECT SUM(input_tokens + output_tokens) AS total_tokens
        FROM curated.fact_bedrock_usage
        WHERE tenant_id = '{tenant_id}'
        AND usage_date = CURRENT_DATE
    """)
    avg_7d = query_athena(f"""
        SELECT AVG(daily_tokens) FROM (
            SELECT SUM(input_tokens + output_tokens) AS daily_tokens
            FROM curated.fact_bedrock_usage
            WHERE tenant_id = '{tenant_id}'
            AND usage_date BETWEEN CURRENT_DATE - INTERVAL '7' DAY AND CURRENT_DATE - INTERVAL '1' DAY
            GROUP BY usage_date
        )
    """)
    if avg_7d and today > avg_7d * 3:
        sns_client.publish(
            TopicArn=COST_ANOMALY_SNS,
            Message=json.dumps({
                "alert": "bedrock_cost_spike",
                "tenant_id": tenant_id,
                "today_tokens": today,
                "avg_7d_tokens": avg_7d,
                "spike_multiple": round(today / avg_7d, 1),
            }),
            Subject=f"Bedrock spike: tenant {tenant_id} ({round(today/avg_7d, 1)}× normal)",
        )
```

### 8.3 Tenant MAU Drop Alert

```python
def check_mau_drop(tenant_id: str):
    """
    Alert if tenant's MAU drops > 30% MoM — early churn signal.
    """
    mau_this = get_mau(tenant_id, month_offset=0)
    mau_prev = get_mau(tenant_id, month_offset=-1)
    if mau_prev and mau_this < mau_prev * 0.70:
        drop_pct = round((1 - mau_this / mau_prev) * 100, 1)
        create_cs_task(tenant_id, f"MAU dropped {drop_pct}% MoM ({mau_prev}→{mau_this})")
        notify_slack(
            channel="#churn-risk",
            message=f":red_circle: *{tenant_id}* MAU dropped {drop_pct}% MoM. CS follow-up created."
        )
```

---

## 9. Compliance & Audit Reports

### 9.1 DPDPA Consent Audit

```sql
-- Monthly DPDPA consent audit report
SELECT
    tenant_id,
    COUNT(*) FILTER (WHERE consent_status = 'given')    AS valid_consents,
    COUNT(*) FILTER (WHERE consent_status = 'expired')  AS expired_consents,
    COUNT(*) FILTER (WHERE consent_status = 'revoked')  AS revocations_this_month,
    COUNT(*) AS total_users,
    ROUND(COUNT(*) FILTER (WHERE consent_status = 'given') * 100.0 / COUNT(*), 1) AS consent_pct
FROM analytics.user_consent_summary
WHERE report_month = :month
GROUP BY tenant_id
ORDER BY consent_pct ASC;  -- Lowest compliance tenants first
```

### 9.2 GST GSTR-1 Export

```python
# compliance/gst_export.py
def generate_gstr1(filing_month: str) -> pd.DataFrame:
    """
    Generate GSTR-1 B2B invoice summary for GST filing.
    Grouped by recipient GSTIN as required by GSTN format.
    """
    df = athena_to_df(f"""
        SELECT
            recipient_gstin,
            SUM(base_amount)  AS taxable_value,
            SUM(cgst_amount)  AS cgst,
            SUM(sgst_amount)  AS sgst,
            SUM(igst_amount)  AS igst,
            COUNT(*)          AS invoice_count
        FROM curated.fact_payments
        WHERE invoice_month = '{filing_month}'
            AND payment_status = 'captured'
            AND recipient_gstin IS NOT NULL
        GROUP BY recipient_gstin
        ORDER BY recipient_gstin
    """)
    # Validate: every GSTIN must be 15 chars
    invalid = df[df["recipient_gstin"].str.len() != 15]
    if not invalid.empty:
        logger.error(f"Invalid GSTINs in GSTR-1 export: {invalid['recipient_gstin'].tolist()}")
    return df
```

### 9.3 CERT-In Incident Report

```sql
-- CERT-In incident compliance report
SELECT
    incident_id,
    incident_type,
    severity,
    detected_at,
    reported_to_certin_at,
    EXTRACT(EPOCH FROM (reported_to_certin_at - detected_at)) / 3600 AS hours_to_report,
    CASE
        WHEN EXTRACT(EPOCH FROM (reported_to_certin_at - detected_at)) / 3600 <= 6
        THEN 'COMPLIANT'
        ELSE 'BREACH'
    END AS reporting_compliance,
    resolved_at,
    resolution_summary
FROM compliance.certin_incidents
WHERE DATE_TRUNC('month', detected_at) = :month
ORDER BY detected_at;
```

---

## 10. Student Outcome Analytics (Aggregated)

All student-level analytics are **k-anonymized (k ≥ 5)** — no cohort smaller than 5 students is reported. Students in `analytics_opt_out` are excluded from all aggregate reports (DPDPA compliance).

```python
# analytics/student_outcomes.py
def get_platform_pass_rate(subject: str, class_level: str, month: str) -> dict | None:
    """
    Returns platform-wide exam pass rate for a subject/class.
    Returns None if fewer than 5 students in cohort (k-anonymization).
    """
    result = query_athena(f"""
        SELECT
            COUNT(*) AS total_attempts,
            COUNT(*) FILTER (WHERE score >= passing_score) AS passes,
            AVG(score) AS avg_score
        FROM curated.fact_exam_sessions e
        JOIN dim_tenants t USING (tenant_id)
        WHERE e.subject = '{subject}'
            AND e.class_level = '{class_level}'
            AND e.exam_month = '{month}'
            AND e.student_id NOT IN (
                SELECT student_id FROM analytics.analytics_opt_out
            )
    """)
    if result["total_attempts"] < 5:
        return None   # k-anonymization: suppress small cohorts
    return {
        "subject": subject,
        "class_level": class_level,
        "total_attempts": result["total_attempts"],
        "pass_rate_pct": round(result["passes"] * 100.0 / result["total_attempts"], 1),
        "avg_score": round(result["avg_score"], 1),
    }
```

---

## 11. TSP Analytics

### 11.1 TSP Portfolio Dashboard

```python
# analytics/tsp_dashboard.py
def get_tsp_portfolio_summary(tsp_id: str) -> dict:
    tenants = db.fetchall("""
        SELECT
            t.tenant_id, t.name, t.plan_tier, t.active_student_count,
            ths.health_score, ths.churn_probability,
            tbc.net_amount AS monthly_billing
        FROM tsp.tsp_tenants tt
        JOIN tenants t USING (tenant_id)
        LEFT JOIN analytics.tenant_health_scores ths USING (tenant_id)
        LEFT JOIN tsp.tsp_billing_cycles tbc
            ON tbc.tsp_id = tt.tsp_id
            AND tbc.billing_month = DATE_TRUNC('month', CURRENT_DATE)
        WHERE tt.tsp_id = %s
        ORDER BY tbc.net_amount DESC
    """, [tsp_id])

    return {
        "total_tenants": len(tenants),
        "health_distribution": {
            "green":  sum(1 for t in tenants if t["health_score"] >= 70),
            "yellow": sum(1 for t in tenants if 40 <= t["health_score"] < 70),
            "red":    sum(1 for t in tenants if t["health_score"] < 40),
        },
        "at_risk_tenants": [t for t in tenants if t["churn_probability"] > 0.5],
        "total_mrr": sum(t["monthly_billing"] or 0 for t in tenants),
        "tenants": tenants,
    }
```

### 11.2 White-Label Domain Health Report

```python
def get_domain_health_report(tsp_id: str) -> list[dict]:
    """
    Check TLS expiry and Cloudflare hostname status for all TSP domains.
    Alerts if any cert expires within 30 days.
    """
    domains = db.fetchall("""
        SELECT
            tbp.custom_domain,
            tbp.tls_status,
            tbp.tls_cert_expiry,
            tbp.cloudflare_hostname_id,
            CURRENT_DATE - tbp.tls_cert_expiry AS days_until_expiry
        FROM tsp.tsp_brand_profiles tbp
        JOIN tsp.tsps ts ON ts.tsp_id = tbp.tsp_id
        WHERE ts.tsp_id = %s
            AND tbp.custom_domain IS NOT NULL
    """, [tsp_id])

    for domain in domains:
        if domain["days_until_expiry"] <= 30:
            domain["alert"] = f"TLS cert expires in {domain['days_until_expiry']} days"
        else:
            domain["alert"] = None

    return domains
```

---

## 12. Data Governance

### 12.1 AWS Macie PII Monitoring

AWS Macie is configured on the analytics S3 bucket to detect accidental PII exposure:

```python
# infrastructure/macie_config.py (CDK)
macie_session = macie2.CfnSession(scope, "MacieSession", finding_publishing_frequency="FIFTEEN_MINUTES")

# Custom data identifier for Indian PII
macie2.CfnCustomDataIdentifier(
    scope, "IndianMobilePattern",
    name="IndianMobileNumber",
    regex=r"\b[6-9]\d{9}\b",
    maximum_match_distance=300,
)

# Alert to security SNS topic
macie2.CfnFindingsFilter(
    scope, "PiiFindings",
    action="ARCHIVE",
    name="PiiAlertFilter",
    # SNS notification via EventBridge rule on Macie findings
)
```

### 12.2 Analytics Data Retention

| Data Type | Retention | Storage Class | Reason |
|-----------|-----------|---------------|--------|
| Raw event logs | 90 days | S3 Standard → Glacier IA | Debugging window |
| Curated daily aggregates | 2 years | S3 Standard-IA | Trend analysis |
| Financial monthly rollups | 7 years | S3 Glacier | CGST Act requirement |
| Audit logs | 5 years | S3 Glacier | IT Act + DPDPA |
| Report PDFs | Permanent | S3 Glacier | Compliance evidence |

### 12.3 Right to Erasure in Analytics

```python
# analytics/erasure.py
def process_erasure_request(user_id: str, tenant_id: str):
    """
    DPDPA: Anonymize user from curated and aggregated analytics zones.
    Nightly batch — must complete within 30 days of request.
    """
    # Curated zone: replace user_id with NULL in Parquet files
    glue_client.start_job_run(
        JobName="anonymize-user-analytics",
        Arguments={
            "--user_id": user_id,
            "--tenant_id": tenant_id,
            "--curated_prefix": f"s3://analytics-eduforge/curated/",
        }
    )
    # Aggregated zone: aggregates are already non-individual, no action needed
    # Log completion
    db.execute("""
        UPDATE analytics.analytics_erasure_requests
        SET status = 'processing', processing_started_at = NOW()
        WHERE user_id = %s
    """, [user_id])
```

---

## 13. Database Schema

```sql
-- PostgreSQL: Report catalog and job management
CREATE TABLE analytics.report_definitions (
    report_def_id       UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name                TEXT NOT NULL,
    category            TEXT NOT NULL,  -- financial, operational, compliance, academic, tsp
    description         TEXT,
    query_template      TEXT NOT NULL,  -- Athena SQL with :param placeholders
    params_schema       JSONB NOT NULL DEFAULT '{}',  -- JSON Schema for parameters
    output_formats      TEXT[] NOT NULL DEFAULT '{pdf,xlsx,csv}',
    required_permission TEXT NOT NULL,  -- e.g., 'analytics.financial.read'
    schedule_options    TEXT[] DEFAULT '{daily,weekly,monthly}',
    is_active           BOOLEAN NOT NULL DEFAULT TRUE,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE analytics.report_jobs (
    job_id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    report_def_id       UUID NOT NULL REFERENCES analytics.report_definitions,
    tenant_id           UUID,           -- NULL = super-admin (platform-wide) report
    requester_id        UUID NOT NULL,
    params              JSONB NOT NULL DEFAULT '{}',
    status              TEXT NOT NULL DEFAULT 'queued',  -- queued, running, done, failed
    output_format       TEXT NOT NULL DEFAULT 'pdf',
    s3_key              TEXT,           -- populated when done
    presigned_url       TEXT,           -- 7-day expiry URL, regenerated on download
    error_message       TEXT,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    started_at          TIMESTAMPTZ,
    completed_at        TIMESTAMPTZ,
    file_size_bytes     BIGINT,
    CONSTRAINT valid_status CHECK (status IN ('queued','running','done','failed'))
);

CREATE INDEX idx_report_jobs_tenant ON analytics.report_jobs (tenant_id, created_at DESC);
CREATE INDEX idx_report_jobs_requester ON analytics.report_jobs (requester_id, created_at DESC);
CREATE INDEX idx_report_jobs_status ON analytics.report_jobs (status) WHERE status IN ('queued','running');

CREATE TABLE analytics.report_subscriptions (
    subscription_id     UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    report_def_id       UUID NOT NULL REFERENCES analytics.report_definitions,
    subscriber_id       UUID NOT NULL,
    tenant_id           UUID,
    params              JSONB NOT NULL DEFAULT '{}',
    frequency           TEXT NOT NULL,  -- daily, weekly, monthly
    delivery_email      TEXT,
    delivery_inapp      BOOLEAN NOT NULL DEFAULT TRUE,
    eventbridge_rule    TEXT,           -- EventBridge rule name for cleanup
    is_active           BOOLEAN NOT NULL DEFAULT TRUE,
    last_sent_at        TIMESTAMPTZ,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Pre-aggregated daily platform metrics (primary dashboard source)
CREATE TABLE analytics.platform_metrics_daily (
    metric_date         DATE NOT NULL,
    tenant_id           UUID,           -- NULL = platform-wide aggregate
    metric_name         TEXT NOT NULL,
    metric_value        NUMERIC(20, 4) NOT NULL,
    dimension_1         TEXT,           -- e.g., plan_tier, institution_type
    dimension_2         TEXT,           -- e.g., state, model_id
    computed_at         TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (metric_date, COALESCE(tenant_id, '00000000-0000-0000-0000-000000000000'), metric_name, COALESCE(dimension_1, ''), COALESCE(dimension_2, ''))
) PARTITION BY RANGE (metric_date);

CREATE TABLE analytics.platform_metrics_daily_2026
    PARTITION OF analytics.platform_metrics_daily
    FOR VALUES FROM ('2026-01-01') TO ('2027-01-01');

-- Tenant health scores (computed nightly)
CREATE TABLE analytics.tenant_health_scores (
    tenant_id               UUID PRIMARY KEY,
    health_score            NUMERIC(5,2) NOT NULL,
    health_tier             TEXT NOT NULL,  -- RED, YELLOW, GREEN
    churn_probability       NUMERIC(5,4),
    login_frequency_score   NUMERIC(5,2),
    feature_breadth_score   NUMERIC(5,2),
    student_growth_score    NUMERIC(5,2),
    payment_history_score   NUMERIC(5,2),
    support_burden_score    NUMERIC(5,2),
    computed_at             TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Analytics erasure requests (DPDPA right to erasure)
CREATE TABLE analytics.analytics_erasure_requests (
    request_id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id             UUID NOT NULL,
    tenant_id           UUID NOT NULL,
    requested_at        TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    status              TEXT NOT NULL DEFAULT 'pending',  -- pending, processing, completed
    processing_started_at TIMESTAMPTZ,
    completed_at        TIMESTAMPTZ,
    glue_job_run_id     TEXT,
    CONSTRAINT must_complete_in_30d CHECK (
        completed_at IS NULL OR
        EXTRACT(DAY FROM completed_at - requested_at) <= 30
    )
);

-- Dashboard sharing tokens
CREATE TABLE analytics.dashboard_share_tokens (
    token_id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    token_hash          TEXT NOT NULL UNIQUE,  -- HMAC-SHA256
    dashboard_id        TEXT NOT NULL,
    params              JSONB NOT NULL DEFAULT '{}',
    created_by          UUID NOT NULL,
    expires_at          TIMESTAMPTZ NOT NULL DEFAULT NOW() + INTERVAL '24 hours',
    access_count        INT NOT NULL DEFAULT 0,
    max_access_count    INT NOT NULL DEFAULT 100
);
```

---

## 14. API Endpoints

```python
# analytics/routes.py (FastAPI)
from fastapi import APIRouter, Depends
router = APIRouter(prefix="/analytics", tags=["Analytics"])

# KPI panels (HTMX fragments)
@router.get("/api/kpi/revenue")
async def kpi_revenue(user=Depends(require_permission("analytics.revenue.read"))):
    return kpi_service.get_revenue_kpis()

@router.get("/api/kpi/tenant-health")
async def kpi_tenant_health(user=Depends(require_permission("analytics.tenants.read"))):
    return kpi_service.get_tenant_health_distribution()

@router.get("/api/kpi/ai-cost")
async def kpi_ai_cost(user=Depends(require_permission("analytics.costs.read"))):
    return kpi_service.get_ai_cost_summary()

# Reports
@router.get("/reports", response_model=list[ReportDefinitionSummary])
async def list_reports(user=Depends(get_current_user)):
    """Returns reports accessible to the user's role."""
    return report_service.list_accessible(user.role, user.tenant_id)

@router.post("/reports/{report_def_id}/run")
async def run_report(
    report_def_id: str,
    params: ReportRunRequest,
    user=Depends(get_current_user),
):
    job_id = report_runner.request_report(
        report_def_id, params.dict(),
        requester_id=user.id,
        tenant_id=user.tenant_id,
        output_format=params.output_format,
    )
    return {"job_id": job_id, "status": "queued"}

@router.get("/reports/jobs/{job_id}")
async def get_report_job(job_id: str, user=Depends(get_current_user)):
    job = report_service.get_job(job_id, user.tenant_id)
    if job.status == "done" and not job.presigned_url:
        job.presigned_url = s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": REPORTS_BUCKET, "Key": job.s3_key},
            ExpiresIn=604800,  # 7 days
        )
    return job

@router.post("/reports/subscriptions")
async def subscribe_report(
    payload: ReportSubscriptionRequest,
    user=Depends(get_current_user),
):
    sub = report_service.create_subscription(payload, user.id, user.tenant_id)
    return sub

# Custom report builder
@router.post("/custom-query")
async def run_custom_query(
    payload: CustomQueryRequest,
    user=Depends(require_permission("analytics.custom.read")),
):
    """Restricted to super-admin and TSP admin roles."""
    sql = custom_builder.build_custom_query(
        payload.metrics, payload.dimensions,
        payload.filters, payload.date_range
    )
    # Proxy through safe query (injects tenant filter if not super-admin)
    safe_sql = query_proxy.safe_query(sql, user.tenant_id, user.role)
    results = athena_service.run_query(safe_sql, workgroup=WORKGROUP_LIMITS[user.role])
    return {"data": results, "query": safe_sql if user.role == "super_admin" else None}

# TSP analytics
@router.get("/tsp/portfolio")
async def tsp_portfolio(user=Depends(require_permission("tsp.analytics.read"))):
    return tsp_analytics.get_tsp_portfolio_summary(user.tsp_id)

@router.get("/tsp/domain-health")
async def tsp_domain_health(user=Depends(require_permission("tsp.analytics.read"))):
    return tsp_analytics.get_domain_health_report(user.tsp_id)

# Compliance
@router.get("/compliance/dpdpa-consent-audit")
async def dpdpa_audit(month: str, user=Depends(require_permission("compliance.audit.read"))):
    return compliance_service.dpdpa_consent_audit(month)

@router.get("/compliance/gst-export")
async def gst_export(month: str, user=Depends(require_permission("finance.gst.export"))):
    df = gst_service.generate_gstr1(month)
    csv_bytes = df.to_csv(index=False).encode()
    return Response(
        content=csv_bytes,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=GSTR1_{month}.csv"},
    )
```

---

## 15. Cost Architecture

| Component | Monthly Cost (50M students, 5K tenants) | Notes |
|-----------|----------------------------------------|-------|
| Amazon Athena | ~Rs. 8,000 | ~1 TB queries/day × Rs. 25/TB |
| AWS Glue ETL | ~Rs. 6,000 | Nightly jobs, DPU-hour billing |
| S3 Data Lake | ~Rs. 12,000 | 5 TB analytics data, Intelligent-Tiering |
| Lambda (pipelines) | ~Rs. 4,000 | Ingest + report workers |
| SageMaker Serverless | ~Rs. 3,000 | Churn risk model |
| CloudWatch / alarms | ~Rs. 2,000 | Metrics, alarms, dashboards |
| SES (report emails) | ~Rs. 500 | ~10K report emails/month |
| **Total** | **~Rs. 35,500/month** | ~Rs. 0.0007/student/month |

Cost controls:
- Athena workgroup scan limits prevent runaway queries
- Glue job bookmarks: incremental ETL only — no full reprocessing
- Pre-aggregated rollup tables: 95% of dashboard queries never touch raw zone
- S3 Intelligent-Tiering: raw data auto-migrates to Glacier IA after 30 days
- All resources tagged `Module=53, CostCenter=Analytics` for FinOps cost allocation
