# Module 55 — Incident Management & SLA

## 1. Purpose & Scope

Incident Management & SLA is the operational reliability backbone of EduForge. It covers the full incident lifecycle — automatic detection, triage, response, customer communication, resolution, and post-mortem — aligned with contractual SLA commitments per tenant plan tier.

This module also handles:
- CERT-In mandatory cybersecurity incident reporting (6-hour rule, IT Amendment Act 2022)
- On-call rotation management and escalation policies
- Public and white-label status pages
- Runbook catalog and disaster recovery drills
- SLA credit calculation integrated with Module 56 (Platform Billing)

---

## 2. Incident Classification

### 2.1 Categories

| Category | Description |
|----------|-------------|
| Platform | Infrastructure failure, API outage, service degradation affecting multiple tenants |
| Tenant | Single-tenant data access issue, misconfiguration, isolated performance problem |
| Security | Unauthorized access, data breach, DDoS, phishing, ransomware |

### 2.2 Severity Levels & SLAs

| Severity | Description | Acknowledge | Resolve | Customer Update Cadence |
|----------|-------------|-------------|---------|------------------------|
| P0 | Full outage — core service unavailable | 15 min | 4h | Every 30 min |
| P1 | Major degradation — significant % of users affected | 30 min | 8h | Every 1h |
| P2 | Partial degradation — non-critical feature affected | 4h | 24h | On resolution only |
| P3 | Low impact — cosmetic or edge-case | 24h | 72h | None |

### 2.3 Incident States

```
detected → triaged → acknowledged → investigating → mitigating → resolved → closed → post_mortem_due
```

### 2.4 Incident ID Format

`INC-{YEAR}-{NNNNNN}` — e.g., `INC-2026-000142`. Human-readable, sequential, year-prefixed.

---

## 3. Auto-Detection

### 3.1 CloudWatch Alarm → Incident Pipeline

```python
# Lambda: incident-creator
# Triggered by CloudWatch Alarm → SNS

import boto3, json, time, hashlib
from datetime import datetime

db = get_db()
dynamodb = boto3.resource("dynamodb")
dedup_table = dynamodb.Table("incident_dedup")

ALARM_TO_INCIDENT = {
    "EduForge-HighErrorRate":      {"severity": "P1", "component": "API", "runbook": "RB-001"},
    "EduForge-HighLatencyP99":     {"severity": "P1", "component": "API", "runbook": "RB-002"},
    "EduForge-LambdaErrorRate":    {"severity": "P2", "component": "Lambda", "runbook": "RB-003"},
    "EduForge-RDS-HighCPU":        {"severity": "P1", "component": "Database", "runbook": "RB-004"},
    "EduForge-SQS-DLQDepth":       {"severity": "P2", "component": "SQS", "runbook": "RB-005"},
    "EduForge-ECS-TaskFailure":    {"severity": "P1", "component": "ECS", "runbook": "RB-006"},
    "EduForge-Bedrock-Unavailable":{"severity": "P1", "component": "AI Features", "runbook": "RB-007"},
    "EduForge-Canary-LoginFlow":   {"severity": "P0", "component": "Auth", "runbook": "RB-008"},
}

def handler(event, context):
    for record in event["Records"]:
        message = json.loads(record["Sns"]["Message"])
        alarm_name = message.get("AlarmName", "")
        new_state = message.get("NewStateValue", "")

        if new_state != "ALARM":
            # Alarm resolved — check if we should false-positive close
            handle_alarm_resolution(alarm_name)
            return

        config = ALARM_TO_INCIDENT.get(alarm_name)
        if not config:
            return  # Unknown alarm — log and skip

        # Deduplication: one incident per alarm per 5-minute window
        dedup_key = f"{alarm_name}:{int(time.time() // 300)}"
        dedup_hash = hashlib.md5(dedup_key.encode()).hexdigest()
        try:
            dedup_table.put_item(
                Item={"dedup_key": dedup_hash, "ttl": int(time.time()) + 600},
                ConditionExpression="attribute_not_exists(dedup_key)",
            )
        except dedup_table.meta.client.exceptions.ConditionalCheckFailedException:
            return  # Duplicate — skip

        create_incident(
            title=f"Auto-detected: {alarm_name}",
            severity=config["severity"],
            component=config["component"],
            runbook_id=config["runbook"],
            source="cloudwatch_alarm",
            alarm_name=alarm_name,
        )


def handle_alarm_resolution(alarm_name: str):
    """If alarm resolves within 2 min of incident creation, mark as false positive."""
    incident = db.fetchone("""
        SELECT id, created_at FROM incidents.incidents
        WHERE source_alarm = %s AND status = 'detected'
        AND created_at > NOW() - INTERVAL '2 minutes'
    """, [alarm_name])
    if incident:
        db.execute("""
            UPDATE incidents.incidents SET status = 'closed', tags = tags || '{"false_positive": true}',
            resolved_at = NOW(), closed_at = NOW()
            WHERE id = %s
        """, [incident["id"]])
```

### 3.2 Synthetic Monitoring

```python
# CloudWatch Canary: checks 5 critical user flows every 5 minutes
# Flows: login, student dashboard load, exam start, payment page, API health check

# canary/login_flow.py (CloudWatch Synthetics)
import synthetics_canarypublisher as canarypublisher
from selenium.webdriver import Chrome

def handler(event, context):
    with Chrome() as driver:
        driver.get("https://app.eduforge.in/login")
        driver.find_element("id", "email").send_keys("canary@test.eduforge.in")
        driver.find_element("id", "password").send_keys(CANARY_PASSWORD)
        driver.find_element("id", "login-btn").click()
        # Assert dashboard loaded within 3 seconds
        driver.implicitly_wait(3)
        assert "dashboard" in driver.current_url, "Login redirect failed"
    canarypublisher.add_execution_status(canarypublisher.SyntheticsConstants.CANARY_STATUS_SUCCESS)
```

### 3.3 Student-Reported Signal

```python
# If > 10 students click "Report Issue" within 5 minutes → auto-escalate to P1
def check_student_report_spike():
    count = dynamodb.query(
        TableName="student_issue_reports",
        KeyConditionExpression="report_minute = :m",
        ExpressionAttributeValues={":m": str(int(time.time() // 60))},
    )["Count"]
    if count > 10:
        create_or_escalate_incident(
            title="Student-reported service issue spike",
            severity="P1",
            component="Student Portal",
            source="student_feedback",
        )
```

---

## 4. SLA Tiers

### 4.1 SLA Per Plan

| Metric | Starter | Growth | Scale | Enterprise |
|--------|---------|--------|-------|------------|
| Monthly Uptime | 99.0% | 99.5% | 99.9% | 99.95% |
| Allowed downtime/month | ~7.2h | ~3.6h | ~43 min | ~22 min |
| P1 Support Response | 4h | 2h | 1h | 30 min |
| P2 Support Response | 24h | 12h | 4h | 2h |
| RTO (P0) | 4h | 2h | 1h | 30 min |
| RPO (data loss max) | 24h | 4h | 1h | 15 min |
| Dedicated CSM | No | No | Yes | Yes |
| Custom status page | No | No | No | Yes |

### 4.2 SLA Credit Calculation

```python
# billing/sla_credits.py  (runs on 1st of each month via EventBridge)
from decimal import Decimal

SLA_CREDIT_SCHEDULE = {
    1:  Decimal("5"),    # 1+ hour breach → 5% credit
    4:  Decimal("10"),   # 4+ hours → 10%
    8:  Decimal("25"),   # 8+ hours → 25%
}

def calculate_monthly_sla_credits(report_month: str):
    """
    For each tenant, calculate downtime from P0/P1 incidents in the month.
    Compare against their plan's SLA. Generate credit if exceeded.
    """
    tenants = db.fetchall("SELECT tenant_id, plan_tier, monthly_invoice_amount FROM subscriptions.tenant_subscriptions WHERE status = 'active'")

    for tenant in tenants:
        sla_minutes = get_sla_uptime_minutes(tenant["plan_tier"])
        actual_downtime_minutes = db.fetchone("""
            SELECT COALESCE(SUM(EXTRACT(EPOCH FROM (resolved_at - created_at)) / 60), 0) AS downtime_min
            FROM incidents.incidents i
            JOIN incidents.affected_tenants at ON at.incident_id = i.id
            WHERE at.tenant_id = %s
            AND DATE_TRUNC('month', i.created_at) = %s::date
            AND i.severity IN ('P0', 'P1')
            AND i.status = 'resolved'
            AND NOT (i.tags->>'maintenance_related')::boolean IS TRUE
            AND NOT (i.tags->>'false_positive')::boolean IS TRUE
        """, [tenant["tenant_id"], report_month])["downtime_min"]

        allowed_downtime_minutes = (1 - sla_minutes / (30 * 24 * 60)) * 30 * 24 * 60
        breach_hours = max(0, (actual_downtime_minutes - allowed_downtime_minutes) / 60)

        if breach_hours > 0:
            credit_pct = Decimal("0")
            for threshold_h, pct in sorted(SLA_CREDIT_SCHEDULE.items()):
                if breach_hours >= threshold_h:
                    credit_pct = pct

            credit_amount = tenant["monthly_invoice_amount"] * credit_pct / 100
            db.execute("""
                INSERT INTO incidents.sla_credits
                (tenant_id, report_month, breach_hours, credit_pct, credit_amount, created_at)
                VALUES (%s, %s, %s, %s, %s, NOW())
                ON CONFLICT (tenant_id, report_month) DO UPDATE
                SET breach_hours = EXCLUDED.breach_hours, credit_amount = EXCLUDED.credit_amount
            """, [tenant["tenant_id"], report_month, float(breach_hours), float(credit_pct), float(credit_amount)])
```

---

## 5. On-Call Management

### 5.1 Rotation Schema & Paging

```python
# incidents/oncall.py

def get_current_oncall() -> dict:
    """Get primary and secondary on-call for current time."""
    now = datetime.utcnow()
    schedule = db.fetchone("""
        SELECT s.primary_engineer_id, s.secondary_engineer_id
        FROM incidents.oncall_schedules s
        LEFT JOIN incidents.oncall_overrides o
            ON o.schedule_id = s.id
            AND NOW() BETWEEN o.override_start AND o.override_end
        WHERE s.rotation_start <= %s AND s.rotation_end > %s
        ORDER BY o.override_id DESC NULLS LAST
        LIMIT 1
    """, [now, now])
    # Apply override if exists
    return {
        "primary": schedule["primary_engineer_id"],
        "secondary": schedule["secondary_engineer_id"],
    }


def page_oncall(incident_id: str, severity: str):
    oncall = get_current_oncall()
    incident = db.fetchone("SELECT * FROM incidents.incidents WHERE id = %s", [incident_id])

    runbook_url = get_runbook_url(incident.get("runbook_id"))
    message = (
        f"[{severity}] EduForge Incident {incident['incident_ref']}: "
        f"{incident['title']}\n"
        f"Component: {incident['component']}\n"
        f"Runbook: {runbook_url}\n"
        f"Acknowledge: https://admin.eduforge.in/incidents/{incident_id}/ack"
    )

    # SMS + email via SNS
    sns.publish(
        TopicArn=ONCALL_SNS_TOPIC,
        Message=message,
        Subject=f"[{severity}] {incident['title']}",
        MessageAttributes={
            "engineer_id": {"DataType": "String", "StringValue": oncall["primary"]},
        },
    )
    # Slack DM
    send_slack_dm(oncall["primary"], message)

    # Schedule escalation if not acknowledged
    schedule_escalation_check(incident_id, severity, delay_minutes=10 if severity == "P0" else 15)


def escalate_if_unacknowledged(incident_id: str):
    incident = db.fetchone("""
        SELECT * FROM incidents.incidents WHERE id = %s AND acknowledged_at IS NULL
    """, [incident_id])
    if not incident:
        return  # Already acknowledged — no action

    oncall = get_current_oncall()
    # Page secondary
    page_engineer(oncall["secondary"], incident)
    # Page engineering manager + CTO for P0
    if incident["severity"] == "P0":
        page_engineering_leadership(incident)
    add_incident_update(incident_id, "AUTO", "Escalated: no acknowledgment within SLA window")
```

---

## 6. Incident Response Workflow

### 6.1 War Room Creation (P0/P1)

```python
# incidents/war_room.py
import slack_sdk

slack = slack_sdk.WebClient(token=SLACK_BOT_TOKEN)

def create_war_room(incident_id: str, severity: str) -> str:
    incident = db.fetchone("SELECT * FROM incidents.incidents WHERE id = %s", [incident_id])
    channel_name = f"incident-{incident['incident_ref'].lower()}"

    channel = slack.conversations_create(name=channel_name, is_private=True)
    channel_id = channel["channel"]["id"]

    # Invite on-call + relevant team leads
    members = get_incident_team(incident["component"])
    slack.conversations_invite(channel=channel_id, users=",".join(members))

    # Post initial message
    slack.chat_postMessage(
        channel=channel_id,
        text=(
            f"*{severity} Incident: {incident['title']}*\n"
            f"Incident: {incident['incident_ref']}\n"
            f"Component: {incident['component']}\n"
            f"Runbook: <{get_runbook_url(incident['runbook_id'])}|{incident['runbook_id']}>\n"
            f"Status page: <https://admin.eduforge.in/incidents/{incident_id}|View Incident>\n"
            f"\n*Roles*\n"
            f"• Incident Commander: TBD (first to join)\n"
            f"• Scribe: TBD\n"
            f"\n*Status Updates every 30 min (P0) / 60 min (P1)*"
        ),
    )
    # Save channel reference
    db.execute("UPDATE incidents.incidents SET slack_channel_id = %s WHERE id = %s", [channel_id, incident_id])
    return channel_id
```

### 6.2 CERT-In Report Generation

```python
# compliance/certin.py

CERT_IN_REPORT_TEMPLATE = """
CERT-In Mandatory Incident Report
Organisation: EduForge Technologies Pvt. Ltd.
Report Date: {report_date}
Incident Reference: {incident_ref}

1. Incident Type: {incident_type}
2. Date/Time of Detection: {detected_at} IST
3. Affected Systems: {affected_systems}
4. Estimated No. of Users Affected: {estimated_users}
5. Nature of Data Involved: {data_nature}
6. How Detected: {detection_method}
7. Immediate Action Taken: {immediate_actions}
8. Current Status: {current_status}
9. Further Action Planned: {planned_actions}

Point of Contact: {poc_name} | {poc_email} | {poc_phone}
"""

def create_certin_draft(incident_id: str) -> str:
    incident = db.fetchone("SELECT * FROM incidents.incidents WHERE id = %s", [incident_id])
    content = CERT_IN_REPORT_TEMPLATE.format(
        report_date=datetime.now().strftime("%Y-%m-%d %H:%M IST"),
        incident_ref=incident["incident_ref"],
        incident_type=incident["security_incident_type"] or "Security Incident",
        detected_at=incident["created_at"].strftime("%Y-%m-%d %H:%M"),
        affected_systems=incident["component"],
        estimated_users=incident.get("estimated_affected_users", "Under assessment"),
        data_nature=incident.get("data_nature", "Under assessment"),
        detection_method=incident["source"],
        immediate_actions=incident.get("immediate_actions", "Under assessment"),
        current_status=incident["status"],
        planned_actions="Under assessment",
        poc_name=get_platform_config("certin_poc_name"),
        poc_email=get_platform_config("certin_poc_email"),
        poc_phone=get_platform_config("certin_poc_phone"),
    )
    # Store draft in S3
    s3_key = f"certin-reports/{incident['incident_ref']}/draft.txt"
    s3.put_object(
        Bucket=COMPLIANCE_BUCKET,
        Key=s3_key,
        Body=content.encode(),
        ServerSideEncryption="AES256",
    )
    db.execute("""
        INSERT INTO incidents.certin_reports
        (incident_id, report_type, draft_s3_key, deadline, status, created_at)
        VALUES (%s, 'initial', %s, %s, 'draft', NOW())
    """, [incident_id, s3_key, incident["created_at"] + timedelta(hours=6)])
    return s3_key


def submit_certin_report(certin_report_id: str, actor_id: str):
    """Super-admin reviews draft and marks as submitted."""
    report = db.fetchone("SELECT * FROM incidents.certin_reports WHERE id = %s", [certin_report_id])
    # Hash for immutability proof
    content = s3.get_object(Bucket=COMPLIANCE_BUCKET, Key=report["draft_s3_key"])["Body"].read()
    sha256 = hashlib.sha256(content).hexdigest()
    # Archive as final (immutable)
    final_key = report["draft_s3_key"].replace("/draft.txt", f"/final_{sha256[:8]}.txt")
    s3.copy_object(
        CopySource={"Bucket": COMPLIANCE_BUCKET, "Key": report["draft_s3_key"]},
        Bucket=COMPLIANCE_BUCKET,
        Key=final_key,
    )
    db.execute("""
        UPDATE incidents.certin_reports
        SET status = 'submitted', submitted_by = %s, submitted_at = NOW(),
            final_s3_key = %s, sha256_hash = %s
        WHERE id = %s
    """, [actor_id, final_key, sha256, certin_report_id])
```

---

## 7. Status Page

### 7.1 Component Status Update

```python
# incidents/status_page.py

STATUS_PAGE_BUCKET = "eduforge-status-page"
STATUS_PAGE_DISTRIBUTION = "CLOUDFRONT_DIST_ID"

STATUS_COMPONENTS = [
    "API Gateway", "Web Portal", "Mobile App",
    "AI Features (Doubt Solver)", "AI Features (Analytics)",
    "Payment Processing", "Video Streaming",
    "Notifications (SMS/Email/WhatsApp)", "Exam Engine",
]

def update_status_page(incident_id: str | None = None):
    """
    Regenerate the status.json read by the static status page.
    Called on every incident status change.
    """
    # Get current component statuses
    component_statuses = db.fetchall("""
        SELECT component, status, last_updated_at
        FROM incidents.status_page_config
        ORDER BY component
    """)

    # Get recent incidents (last 90 days)
    recent_incidents = db.fetchall("""
        SELECT incident_ref, title, severity, component, created_at, resolved_at, status
        FROM incidents.incidents
        WHERE created_at > NOW() - INTERVAL '90 days'
        AND status != 'false_positive'
        ORDER BY created_at DESC
        LIMIT 100
    """)

    # Compute 90-day uptime per component
    uptime_pct = {}
    for comp in STATUS_COMPONENTS:
        downtime_min = db.fetchone("""
            SELECT COALESCE(SUM(EXTRACT(EPOCH FROM (LEAST(resolved_at, NOW()) - created_at)) / 60), 0) AS dm
            FROM incidents.incidents
            WHERE component = %s
            AND created_at > NOW() - INTERVAL '90 days'
            AND severity IN ('P0', 'P1')
            AND status = 'resolved'
        """, [comp])["dm"]
        total_min = 90 * 24 * 60
        uptime_pct[comp] = round((1 - downtime_min / total_min) * 100, 3)

    status_json = {
        "generated_at": datetime.utcnow().isoformat(),
        "components": [
            {
                "name": c["component"],
                "status": c["status"],
                "uptime_90d": uptime_pct.get(c["component"], 100.0),
            }
            for c in component_statuses
        ],
        "incidents": [
            {
                "ref": i["incident_ref"],
                "title": i["title"],
                "severity": i["severity"],
                "component": i["component"],
                "started_at": i["created_at"].isoformat(),
                "resolved_at": i["resolved_at"].isoformat() if i["resolved_at"] else None,
                "status": i["status"],
            }
            for i in recent_incidents
        ],
    }

    s3.put_object(
        Bucket=STATUS_PAGE_BUCKET,
        Key="status.json",
        Body=json.dumps(status_json).encode(),
        ContentType="application/json",
        CacheControl="max-age=30",
    )
    # Invalidate CloudFront
    cf.create_invalidation(
        DistributionId=STATUS_PAGE_DISTRIBUTION,
        InvalidationBatch={"Paths": {"Quantity": 1, "Items": ["/status.json"]}, "CallerReference": str(time.time())},
    )
    # Notify subscribers
    if incident_id:
        notify_status_subscribers(incident_id)
```

---

## 8. Runbook Catalog

### 8.1 Example Runbooks

**RB-004: RDS High CPU (> 90% for 5 min)**
```markdown
## Symptoms
- CloudWatch alarm: RDS CPU > 90%
- API latency P99 > 2s
- Connection timeouts in Lambda logs

## Diagnosis (ETA: 5 min)
1. CloudWatch Insights query (copy-paste):
   ```
   fields @timestamp, @message
   | filter @message like /connection/
   | stats count() by bin(1m)
   ```
2. Check pgBouncer pool:
   ```
   SELECT count(*), state FROM pg_stat_activity GROUP BY state;
   ```
3. Find slow queries:
   ```
   SELECT query, calls, mean_exec_time FROM pg_stat_statements
   ORDER BY mean_exec_time DESC LIMIT 10;
   ```

## Mitigation (ETA: 10 min)
1. Kill long-running queries (> 60s):
   ```sql
   SELECT pg_terminate_backend(pid) FROM pg_stat_activity
   WHERE state != 'idle' AND query_start < NOW() - INTERVAL '60 seconds';
   ```
2. If query spike from specific feature: disable via Remote Config
   (Feature flag: `module_{n}_enabled` → false for affected tenant)
3. If connection pool exhausted: increase `max_pool_size` via Remote Config

## Escalation
- If CPU still > 90% after 15 min: page DBA
- If data corruption suspected: escalate to P0

## Runbook ID: RB-004 | Owner: Platform Team | Last reviewed: 2026-03
```

---

## 9. Post-Mortem Process

### 9.1 Post-Mortem Template

```python
POSTMORTEM_SECTIONS = {
    "title":               "Descriptive title (not just the alarm name)",
    "incident_ref":        "INC-YYYY-NNNNNN",
    "severity":            "P0/P1",
    "duration":            "HH:MM (detected → resolved)",
    "impact":              "Number of affected tenants, students, feature unavailability",
    "timeline":            "Minute-by-minute (use incident_updates as source)",
    "root_cause":          "Technical cause — describe systems, not people",
    "contributing_factors":"What made this worse or harder to detect/fix",
    "detection_gap":       "Why wasn't this caught earlier? What monitoring was missing?",
    "resolution":          "What fixed it",
    "action_items":        "Each item: description, owner, due date, ticket link",
    "sla_impact":          "Breach? How many tenant-hours affected? Credit issued?",
    "lessons_learned":     "What did we learn about our system?",
}
```

### 9.2 Action Item Tracking

```python
def create_postmortem_action(
    postmortem_id: str,
    description: str,
    owner_id: str,
    due_date: date,
    ticket_url: str | None = None,
):
    action_id = db.fetchone("""
        INSERT INTO incidents.postmortem_actions
        (postmortem_id, description, owner_id, due_date, ticket_url, status, created_at)
        VALUES (%s, %s, %s, %s, %s, 'open', NOW())
        RETURNING action_id
    """, [postmortem_id, description, owner_id, due_date, ticket_url])["action_id"]

    # Schedule Slack reminder 3 days before due date
    schedule_slack_reminder(
        user_id=owner_id,
        message=f"Post-mortem action item due in 3 days: {description}\nTicket: {ticket_url}",
        send_at=datetime.combine(due_date - timedelta(days=3), time(9, 0)),
    )
    return action_id
```

---

## 10. Disaster Recovery

### 10.1 RPO/RTO by Plan

| Plan | RPO | RTO | DR Strategy |
|------|-----|-----|-------------|
| Starter | 24h | 4h | RDS daily backup, PITR |
| Growth | 4h | 2h | RDS PITR + cross-AZ |
| Scale | 1h | 1h | RDS PITR + cross-region read replica |
| Enterprise | 15 min | 30 min | RDS PITR + cross-region replica + hot standby |

### 10.2 DR Activation Runbook

```bash
# Step 1: Promote cross-region read replica (Singapore)
aws rds promote-read-replica \
  --db-instance-identifier eduforge-dr-singapore \
  --region ap-southeast-1

# Step 2: Update SSM endpoint to DR instance
aws ssm put-parameter \
  --name "/eduforge/prod/database/primary_url" \
  --value "postgresql://eduforge-dr-singapore.rds.amazonaws.com:5432/eduforge" \
  --overwrite \
  --region ap-south-1

# Step 3: Force Lambda cold start (picks up new SSM config)
# Tag Lambda functions to trigger redeployment via CodePipeline
aws lambda update-function-configuration \
  --function-name eduforge-api \
  --environment "Variables={FORCE_RELOAD=$(date +%s)}"

# Step 4: Update Route 53 to DR region
aws route53 change-resource-record-sets \
  --hosted-zone-id ZONE_ID \
  --change-batch '{"Changes":[{"Action":"UPSERT","ResourceRecordSet":{"Name":"api.eduforge.in.","Type":"CNAME","TTL":60,"ResourceRecords":[{"Value":"dr-api.eduforge.in"}]}}]}'

# Step 5: Run smoke tests
python scripts/smoke_test.py --endpoint https://api.eduforge.in
```

---

## 11. Database Schema

```sql
CREATE TABLE incidents.incidents (
    id                      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    incident_ref            TEXT NOT NULL UNIQUE,   -- INC-2026-000001
    title                   TEXT NOT NULL,
    description             TEXT,
    severity                TEXT NOT NULL,          -- P0, P1, P2, P3
    category                TEXT NOT NULL,          -- platform, tenant, security
    component               TEXT NOT NULL,
    status                  TEXT NOT NULL DEFAULT 'detected',
    source                  TEXT NOT NULL,          -- cloudwatch_alarm, canary, manual, student_feedback
    source_alarm            TEXT,                   -- CloudWatch alarm name if auto-detected
    runbook_id              TEXT REFERENCES incidents.runbooks(runbook_id),
    slack_channel_id        TEXT,
    incident_commander_id   UUID,
    scribe_id               UUID,
    detected_at             TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    acknowledged_at         TIMESTAMPTZ,
    acknowledged_by         UUID,
    investigating_at        TIMESTAMPTZ,
    resolved_at             TIMESTAMPTZ,
    closed_at               TIMESTAMPTZ,
    postmortem_due_at       TIMESTAMPTZ,
    tags                    JSONB NOT NULL DEFAULT '{}',
    security_incident_type  TEXT,
    estimated_affected_users INT,
    data_nature             TEXT,
    immediate_actions       TEXT,
    CONSTRAINT valid_severity CHECK (severity IN ('P0','P1','P2','P3')),
    CONSTRAINT valid_status CHECK (status IN (
        'detected','triaged','acknowledged','investigating',
        'mitigating','resolved','closed','post_mortem_due'
    ))
);

CREATE INDEX idx_incidents_severity ON incidents.incidents (severity, created_at DESC);
CREATE INDEX idx_incidents_status ON incidents.incidents (status) WHERE status NOT IN ('closed','resolved');
CREATE INDEX idx_incidents_component ON incidents.incidents (component, created_at DESC);

CREATE TABLE incidents.incident_updates (
    update_id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    incident_id             UUID NOT NULL REFERENCES incidents.incidents(id),
    author_id               UUID,                  -- NULL for system/auto updates
    author_type             TEXT NOT NULL DEFAULT 'engineer', -- engineer, system, customer
    content                 TEXT NOT NULL,
    is_customer_visible     BOOLEAN NOT NULL DEFAULT FALSE,
    created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
-- Append-only
CREATE RULE no_update_incident_updates AS ON UPDATE TO incidents.incident_updates DO INSTEAD NOTHING;
CREATE RULE no_delete_incident_updates AS ON DELETE TO incidents.incident_updates DO INSTEAD NOTHING;

CREATE TABLE incidents.affected_tenants (
    incident_id     UUID NOT NULL REFERENCES incidents.incidents(id),
    tenant_id       UUID NOT NULL,
    notified_at     TIMESTAMPTZ,
    notification_method TEXT,
    PRIMARY KEY (incident_id, tenant_id)
);

CREATE TABLE incidents.oncall_schedules (
    id                      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    rotation_start          TIMESTAMPTZ NOT NULL,
    rotation_end            TIMESTAMPTZ NOT NULL,
    primary_engineer_id     UUID NOT NULL,
    secondary_engineer_id   UUID NOT NULL,
    created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE incidents.oncall_overrides (
    override_id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    schedule_id             UUID NOT NULL REFERENCES incidents.oncall_schedules(id),
    override_start          TIMESTAMPTZ NOT NULL,
    override_end            TIMESTAMPTZ NOT NULL,
    original_engineer_id    UUID NOT NULL,
    replacement_engineer_id UUID NOT NULL,
    reason                  TEXT,
    created_by              UUID NOT NULL,
    created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE incidents.escalation_policies (
    policy_id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    severity                TEXT NOT NULL,
    step                    INTEGER NOT NULL,
    delay_minutes           INTEGER NOT NULL,
    contact_type            TEXT NOT NULL,  -- primary, secondary, manager, cto
    contact_id              UUID,
    contact_group           TEXT,
    UNIQUE (severity, step)
);

-- Insert default escalation policies
INSERT INTO incidents.escalation_policies (severity, step, delay_minutes, contact_type) VALUES
    ('P0', 1, 0,  'primary'),
    ('P0', 2, 10, 'secondary'),
    ('P0', 3, 15, 'manager'),
    ('P0', 4, 20, 'cto'),
    ('P1', 1, 0,  'primary'),
    ('P1', 2, 15, 'secondary'),
    ('P1', 3, 30, 'manager');

CREATE TABLE incidents.runbooks (
    runbook_id              TEXT PRIMARY KEY,  -- RB-001, RB-002 etc.
    title                   TEXT NOT NULL,
    component               TEXT NOT NULL,
    alarm_arns              TEXT[],            -- CloudWatch alarms this runbook maps to
    current_version         INTEGER NOT NULL DEFAULT 1,
    owner                   TEXT NOT NULL,
    last_reviewed_at        DATE,
    expected_resolution_min INTEGER,
    is_active               BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE incidents.runbook_versions (
    version_id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    runbook_id              TEXT NOT NULL REFERENCES incidents.runbooks(runbook_id),
    version                 INTEGER NOT NULL,
    content_markdown        TEXT NOT NULL,
    authored_by             UUID NOT NULL,
    created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (runbook_id, version)
);

CREATE TABLE incidents.postmortems (
    postmortem_id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    incident_id             UUID NOT NULL UNIQUE REFERENCES incidents.incidents(id),
    status                  TEXT NOT NULL DEFAULT 'draft', -- draft, review, published
    timeline                TEXT,
    root_cause              TEXT,
    contributing_factors    TEXT,
    detection_gap           TEXT,
    resolution              TEXT,
    lessons_learned         TEXT,
    rca_category            TEXT,  -- deployment, config_change, capacity, external_dep, code_bug, human_error, unknown
    authored_by             UUID,
    reviewed_by             UUID,
    published_at            TIMESTAMPTZ,
    due_at                  TIMESTAMPTZ NOT NULL,
    created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE incidents.postmortem_actions (
    action_id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    postmortem_id           UUID NOT NULL REFERENCES incidents.postmortems(postmortem_id),
    description             TEXT NOT NULL,
    owner_id                UUID NOT NULL,
    due_date                DATE NOT NULL,
    ticket_url              TEXT,
    status                  TEXT NOT NULL DEFAULT 'open',  -- open, in_progress, closed
    completed_at            TIMESTAMPTZ,
    created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE incidents.certin_reports (
    id                      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    incident_id             UUID NOT NULL REFERENCES incidents.incidents(id),
    report_type             TEXT NOT NULL,    -- initial, interim_15d, final_30d
    deadline                TIMESTAMPTZ NOT NULL,
    status                  TEXT NOT NULL DEFAULT 'draft', -- draft, review, submitted
    draft_s3_key            TEXT,
    final_s3_key            TEXT,
    sha256_hash             TEXT,
    submitted_by            UUID,
    submitted_at            TIMESTAMPTZ,
    created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE incidents.sla_credits (
    credit_id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id               UUID NOT NULL,
    report_month            DATE NOT NULL,
    breach_hours            NUMERIC(8,2) NOT NULL,
    credit_pct              NUMERIC(5,2) NOT NULL,
    credit_amount           NUMERIC(12,2) NOT NULL,
    applied_to_invoice_id   UUID,                  -- linked when credit note issued (Module 56)
    created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (tenant_id, report_month)
);

CREATE TABLE incidents.status_page_config (
    component               TEXT PRIMARY KEY,
    status                  TEXT NOT NULL DEFAULT 'operational',
    last_updated_at         TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT valid_status CHECK (status IN (
        'operational','degraded_performance','partial_outage','major_outage','maintenance'
    ))
);

CREATE TABLE incidents.status_page_subscribers (
    subscriber_id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email                   TEXT,
    webhook_url             TEXT,
    components              TEXT[] DEFAULT '{}',   -- empty = all components
    subscribed_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    unsubscribed_at         TIMESTAMPTZ,
    unsubscribe_token       TEXT NOT NULL DEFAULT encode(gen_random_bytes(16), 'hex')
);
```

---

## 12. API Endpoints

```python
# incidents/routes.py (FastAPI)
router = APIRouter(prefix="/incidents", tags=["Incidents"])

@router.post("/")
async def create_incident(payload: IncidentCreate, user=Depends(require_permission("incidents.write"))):
    incident = incident_service.create(payload, created_by=user.id)
    return incident

@router.get("/")
async def list_incidents(
    severity: str | None = None,
    status: str | None = None,
    component: str | None = None,
    from_date: date | None = None,
    user=Depends(require_permission("incidents.read")),
):
    return incident_service.list(severity=severity, status=status, component=component, from_date=from_date)

@router.patch("/{incident_id}")
async def update_incident(incident_id: str, payload: IncidentUpdate, user=Depends(require_permission("incidents.write"))):
    return incident_service.update(incident_id, payload, user.id)

@router.post("/{incident_id}/acknowledge")
async def acknowledge(incident_id: str, user=Depends(require_permission("incidents.write"))):
    return incident_service.acknowledge(incident_id, user.id)

@router.post("/{incident_id}/resolve")
async def resolve(incident_id: str, payload: IncidentResolve, user=Depends(require_permission("incidents.write"))):
    return incident_service.resolve(incident_id, user.id, payload.resolution_summary)

@router.get("/{incident_id}/pdf")
async def incident_pdf(incident_id: str, user=Depends(require_permission("incidents.read"))):
    pdf_bytes = incident_service.generate_pdf(incident_id)
    return Response(content=pdf_bytes, media_type="application/pdf",
                    headers={"Content-Disposition": f"attachment; filename={incident_id}.pdf"})

# On-call
@router.get("/oncall/current")
async def current_oncall(user=Depends(require_permission("incidents.read"))):
    return oncall_service.get_current_oncall()

@router.post("/oncall/override")
async def create_override(payload: OncallOverride, user=Depends(require_permission("incidents.write"))):
    return oncall_service.create_override(payload, user.id)

# Runbooks
@router.get("/runbooks")
async def list_runbooks(user=Depends(require_permission("incidents.read"))):
    return db.fetchall("SELECT * FROM incidents.runbooks WHERE is_active = TRUE ORDER BY component")

@router.get("/runbooks/{runbook_id}")
async def get_runbook(runbook_id: str, user=Depends(require_permission("incidents.read"))):
    return runbook_service.get_with_content(runbook_id)

# Post-mortems
@router.post("/{incident_id}/postmortem")
async def submit_postmortem(incident_id: str, payload: PostmortemSubmit, user=Depends(require_permission("incidents.write"))):
    return postmortem_service.submit(incident_id, payload, user.id)

# CERT-In
@router.get("/{incident_id}/certin-draft")
async def certin_draft(incident_id: str, user=Depends(require_permission("compliance.certin.read"))):
    return certin_service.get_draft(incident_id)

@router.post("/{incident_id}/certin-submit")
async def certin_submit(incident_id: str, user=Depends(require_permission("compliance.certin.submit"))):
    return certin_service.submit(incident_id, user.id)

# Public status page
@router.get("/public/status", include_in_schema=False)
async def public_status():
    """Unauthenticated — served from S3/CloudFront in production."""
    return s3_service.get_json("status.json")
```

---

## 13. Cost Architecture

| Component | Monthly Cost | Notes |
|-----------|-------------|-------|
| CloudWatch Alarms (50+) | ~Rs. 2,000 | Composite alarms |
| CloudWatch Canaries (5 canaries × 5 min) | ~Rs. 1,500 | 8,640 runs/canary/month |
| Route 53 Health Checks (3 regions) | ~Rs. 800 | |
| SNS (on-call alerts) | ~Rs. 500 | ~100 pages/month |
| Lambda (incident creation, SLA calc) | ~Rs. 300 | Infrequent |
| S3 (status page, CERT-In reports) | ~Rs. 200 | Minimal storage |
| SES (tenant notifications, credit notes) | ~Rs. 400 | ~5,000 emails/month |
| DynamoDB (dedup table) | ~Rs. 100 | Small, TTL-purged |
| **Total** | **~Rs. 5,800/month** | ~Rs. 0.00012/student/month |
