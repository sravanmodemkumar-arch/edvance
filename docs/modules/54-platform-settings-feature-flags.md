# Module 54 — Platform Settings & Feature Flags

## 1. Purpose & Scope

Platform Settings & Feature Flags is the centralised configuration and runtime control layer for EduForge. It provides:

- **Feature flags** — kill switches, percentage rollouts, A/B tests — evaluated in microseconds via DynamoDB without touching PostgreSQL on every request
- **Remote config** — runtime-tunable values (model thresholds, cache TTLs, batch sizes) changeable without redeployment
- **Global platform settings** — defaults that every tenant inherits, with per-tenant override capability
- **Environment & secrets management** — SSM Parameter Store + Secrets Manager integration
- **Maintenance mode** — graceful platform-wide or module-level downtime control
- **Audit trail** — every settings change is immutable and attributable

This module underpins every other module. It is loaded first at service cold start and consulted on every feature evaluation path.

---

## 2. Feature Flag System

### 2.1 Flag Types

| Type | Description | Use Case |
|------|-------------|----------|
| `kill_switch` | Boolean on/off | Emergency disable, migration gate |
| `percentage_rollout` | 0–100%, consistent per tenant | Gradual feature rollout |
| `ab_test` | Named variants (A/B/C) | UI experiments, algorithm comparison |
| `targeting` | Rule-based (tenant, plan, state) | Beta access, regional rollout |

### 2.2 Flag Evaluation Engine

```python
# settings/feature_flags.py
import hashlib
import time
from functools import lru_cache
import boto3

dynamodb = boto3.resource("dynamodb")
FLAGS_TABLE = dynamodb.Table("eduforge_feature_flags")

# Local in-process LRU cache: 60-second TTL
_cache: dict[str, tuple[dict, float]] = {}
CACHE_TTL = 60  # seconds


def _get_flag_raw(flag_name: str) -> dict | None:
    """Load flag from DynamoDB with local cache."""
    now = time.monotonic()
    cached = _cache.get(flag_name)
    if cached and now - cached[1] < CACHE_TTL:
        return cached[0]
    try:
        resp = FLAGS_TABLE.get_item(Key={"flag_name": flag_name})
        flag = resp.get("Item")
        _cache[flag_name] = (flag, now)
        return flag
    except Exception as e:
        # DynamoDB unreachable: serve stale cache
        if cached:
            return cached[0]
        return None  # Will fall through to hardcoded default


def is_enabled(flag_name: str, context: dict | None = None) -> bool:
    """
    Evaluate a feature flag.

    context keys: tenant_id, user_id, role, plan_tier, institution_type, state
    """
    flag = _get_flag_raw(flag_name)
    if flag is None:
        return False  # Fail-closed: unknown flag = disabled

    # 1. User-level override
    user_id = (context or {}).get("user_id")
    if user_id and user_id in flag.get("user_overrides", {}):
        return flag["user_overrides"][user_id]

    # 2. Tenant-level override
    tenant_id = (context or {}).get("tenant_id")
    if tenant_id and tenant_id in flag.get("tenant_overrides", {}):
        return flag["tenant_overrides"][tenant_id]

    # 3. Targeting rules (institution_type, plan_tier, state)
    if _matches_targeting(flag.get("target_rules", []), context or {}):
        return True

    # 4. Percentage rollout (consistent hashing)
    rollout_pct = flag.get("rollout_pct", 0)
    if rollout_pct >= 100:
        return True
    if rollout_pct <= 0:
        return False
    hash_input = f"{tenant_id or ''}{flag_name}"
    bucket = int(hashlib.md5(hash_input.encode()).hexdigest(), 16) % 100
    return bucket < rollout_pct


def get_variant(flag_name: str, context: dict | None = None, default: str = "control") -> str:
    """Evaluate an A/B test flag. Returns variant name."""
    flag = _get_flag_raw(flag_name)
    if flag is None or flag.get("type") != "ab_test":
        return default
    variants = flag.get("variants", [])
    if not variants:
        return default
    # Consistent hash → variant index
    tenant_id = (context or {}).get("tenant_id", "")
    bucket = int(hashlib.md5(f"{tenant_id}{flag_name}".encode()).hexdigest(), 16) % len(variants)
    return variants[bucket]["name"]


def _matches_targeting(rules: list[dict], context: dict) -> bool:
    """Returns True if context matches any targeting rule."""
    for rule in rules:
        if _rule_matches(rule, context):
            return True
    return False


def _rule_matches(rule: dict, context: dict) -> bool:
    for key, allowed in rule.items():
        if isinstance(allowed, list):
            if context.get(key) not in allowed:
                return False
        else:
            if context.get(key) != allowed:
                return False
    return True
```

### 2.3 Emergency Kill Switch

```python
# For production incidents: direct DynamoDB write, bypasses UI approval
def emergency_kill_switch(flag_name: str, actor_id: str, reason: str):
    """
    Disable a flag immediately. Propagates to all services within 60s
    (LRU cache expiry). For immediate propagation, also writes to
    DynamoDB Streams → SQS → Lambda → cache invalidation broadcast.
    """
    FLAGS_TABLE.update_item(
        Key={"flag_name": flag_name},
        UpdateExpression="SET rollout_pct = :zero, is_emergency_kill = :true, "
                         "killed_by = :actor, killed_at = :ts, kill_reason = :reason",
        ExpressionAttributeValues={
            ":zero": 0, ":true": True,
            ":actor": actor_id, ":ts": datetime.utcnow().isoformat(),
            ":reason": reason,
        },
    )
    # Log to audit table
    AUDIT_TABLE.put_item(Item={
        "audit_id": str(uuid4()),
        "flag_name": flag_name,
        "changed_by": actor_id,
        "change_type": "emergency_kill",
        "reason": reason,
        "changed_at": datetime.utcnow().isoformat(),
    })
```

### 2.4 A/B Test Auto-Conclude

```python
# analytics/ab_test_evaluator.py  (runs nightly via EventBridge)
from scipy import stats

def evaluate_ab_test(flag_name: str):
    """
    If statistical significance reached (p < 0.05) and min sample size met,
    send winning variant recommendation to Slack.
    """
    variants = get_ab_test_metrics(flag_name)  # from Module 53 analytics
    if len(variants) < 2:
        return
    control = variants[0]
    for treatment in variants[1:]:
        if control["n"] < 1000 or treatment["n"] < 1000:
            continue  # Minimum sample size
        t_stat, p_value = stats.ttest_ind_from_stats(
            mean1=control["mean"], std1=control["std"], nobs1=control["n"],
            mean2=treatment["mean"], std2=treatment["std"], nobs2=treatment["n"],
        )
        if p_value < 0.05:
            winner = treatment if treatment["mean"] > control["mean"] else control
            notify_slack(
                channel="#product",
                message=(
                    f":trophy: A/B test *{flag_name}* reached significance "
                    f"(p={p_value:.4f}). Winner: *{winner['name']}* "
                    f"({winner['mean']:.2f} vs {control['mean']:.2f})"
                )
            )
```

### 2.5 Flag Lifecycle

```
create → staging → gradual rollout → 100% → cleanup → archive

- creation: name, description, type, default, owner, planned_cleanup_date (required)
- EventBridge rule created at planned_cleanup_date − 7 days → Slack DM to owner
- Flags unchanged > 90 days → auto-flagged for review (stale flag detection)
- After removal: archived (not hard-deleted) for 90 days → rollback safety window
- Max 500 active flags: creation blocked if exceeded
```

---

## 3. Remote Config

### 3.1 DynamoDB Schema

```
Table: eduforge_remote_config
PK: config_key (String)
SK: scope (String — "global" | tenant_id)

Attributes:
  value         (String | Number | Boolean | Map)
  value_type    (String — "string" | "integer" | "float" | "boolean" | "json")
  schema        (Map — type, min, max, allowed_values)
  description   (String)
  updated_by    (String)
  updated_at    (String — ISO8601)
  ttl           (Number — optional, for auto-expiring config)
```

### 3.2 Remote Config SDK

```python
# settings/remote_config.py
import boto3, json, time
from typing import Any

_dynamodb = boto3.resource("dynamodb")
_table = _dynamodb.Table("eduforge_remote_config")
_local_cache: dict[str, tuple[Any, float]] = {}
_CACHE_TTL = 60


def get(key: str, tenant_id: str | None = None, default: Any = None) -> Any:
    """
    Read a remote config value.
    Resolution: tenant-specific → global → hardcoded default
    """
    now = time.monotonic()

    # Try tenant-specific first
    if tenant_id:
        cache_key = f"{key}#{tenant_id}"
        cached = _local_cache.get(cache_key)
        if cached and now - cached[1] < _CACHE_TTL:
            return cached[0]
        try:
            resp = _table.get_item(Key={"config_key": key, "scope": tenant_id})
            if "Item" in resp:
                val = _coerce(resp["Item"]["value"], resp["Item"]["value_type"])
                _local_cache[cache_key] = (val, now)
                return val
        except Exception:
            if cached:
                return cached[0]

    # Global fallback
    global_key = f"{key}#global"
    cached = _local_cache.get(global_key)
    if cached and now - cached[1] < _CACHE_TTL:
        return cached[0]
    try:
        resp = _table.get_item(Key={"config_key": key, "scope": "global"})
        if "Item" in resp:
            val = _coerce(resp["Item"]["value"], resp["Item"]["value_type"])
            _local_cache[global_key] = (val, now)
            return val
    except Exception:
        if cached:
            return cached[0]

    return default


def set_value(key: str, value: Any, scope: str, updated_by: str, reason: str = ""):
    """Write a remote config value with schema validation and history log."""
    # Validate against schema
    schema = get_schema(key)
    if schema:
        validate_against_schema(value, schema)
    # Store previous value for history
    prev = _table.get_item(Key={"config_key": key, "scope": scope}).get("Item")
    _table.put_item(Item={
        "config_key": key,
        "scope": scope,
        "value": value,
        "value_type": infer_type(value),
        "updated_by": updated_by,
        "updated_at": datetime.utcnow().isoformat(),
    })
    # History log (PostgreSQL)
    db.execute("""
        INSERT INTO settings.remote_config_history
        (config_key, scope, old_value, new_value, changed_by, reason, changed_at)
        VALUES (%s, %s, %s, %s, %s, %s, NOW())
    """, [key, scope, prev["value"] if prev else None, str(value), updated_by, reason])
    # Invalidate local caches across all Lambda instances via SQS broadcast
    sqs.send_message(
        QueueUrl=CONFIG_INVALIDATION_QUEUE,
        MessageBody=json.dumps({"type": "remote_config_invalidate", "key": key, "scope": scope}),
    )


def _coerce(value: Any, value_type: str) -> Any:
    if value_type == "integer":  return int(value)
    if value_type == "float":    return float(value)
    if value_type == "boolean":  return value in (True, "true", "True", "1")
    if value_type == "json":     return json.loads(value) if isinstance(value, str) else value
    return value
```

### 3.3 Key Remote Config Values

| Key | Default | Type | Description |
|-----|---------|------|-------------|
| `doubt_cache_cosine_threshold` | `0.92` | float | pgvector cache hit threshold |
| `max_bedrock_tokens_per_hour` | `100000` | integer | Per-tenant hourly Bedrock token cap |
| `sagemaker_churn_batch_size` | `500` | integer | Churn risk prediction batch size |
| `pdf_watermark_enabled` | `true` | boolean | Add watermark to exported PDFs |
| `min_app_version_android` | `"3.2.0"` | string | Minimum Android app version |
| `min_app_version_ios` | `"3.2.0"` | string | Minimum iOS app version |
| `api_pagination_default_size` | `25` | integer | Default items per page |
| `session_idle_timeout_minutes` | `30` | integer | Admin portal idle logout |
| `doubt_solver_model_simple` | `"claude-haiku-4-5-20251001"` | string | Model for simple doubts |
| `doubt_solver_model_complex` | `"claude-opus-4-6"` | string | Model for complex doubts |
| `fee_grace_period_days` | `7` | integer | Days before suspension on payment failure |
| `otp_validity_minutes` | `10` | integer | OTP validity window |

---

## 4. Global Platform Settings

### 4.1 Platform Config Store

```python
# settings/platform_config.py
# Backed by PostgreSQL settings.platform_config + DynamoDB cache

PLATFORM_DEFAULTS = {
    # Identity
    "platform_name":        ("EduForge", "string"),
    "platform_tagline":     ("India's Education OS", "string"),
    "support_email":        ("support@eduforge.in", "email"),
    "legal_entity":         ("EduForge Technologies Pvt. Ltd.", "string"),

    # Locale
    "default_timezone":     ("Asia/Kolkata", "timezone"),
    "default_locale":       ("en-IN", "locale"),
    "date_format":          ("DD/MM/YYYY", "string"),
    "academic_year_start":  (4, "integer"),  # April

    # Security
    "password_min_length":  (8, "integer"),
    "password_expiry_days": (90, "integer"),
    "password_reuse_count": (5, "integer"),
    "otp_length":           (6, "integer"),
    "otp_max_attempts":     (5, "integer"),
    "max_sessions_student": (3, "integer"),
    "max_sessions_staff":   (5, "integer"),

    # Upload limits (bytes)
    "upload_limit_image":   (5 * 1024 * 1024, "integer"),
    "upload_limit_document":(50 * 1024 * 1024, "integer"),
    "upload_limit_video":   (2 * 1024 * 1024 * 1024, "integer"),

    # Trial & Billing
    "trial_duration_days":  (14, "integer"),
    "trial_default_plan":   ("starter", "string"),
    "grace_period_days":    (7, "integer"),

    # Communication
    "dnd_start_hour":       (22, "integer"),  # 10 PM IST
    "dnd_end_hour":         (7, "integer"),   # 7 AM IST

    # GST
    "gst_rate_pct":         (18, "integer"),
    "hsn_saas":             ("9984", "string"),  # HSN for SaaS services
}

def get_platform_config(key: str, tenant_id: str | None = None) -> Any:
    """
    Get config value with tenant override support.
    """
    # Check tenant override first
    if tenant_id:
        override = db.fetchone("""
            SELECT value FROM settings.tenant_config_overrides
            WHERE tenant_id = %s AND config_key = %s
        """, [tenant_id, key])
        if override:
            return override["value"]
    # Global platform config
    row = db.fetchone("""
        SELECT value FROM settings.platform_config WHERE config_key = %s
    """, [key])
    if row:
        return row["value"]
    # Hardcoded default (schema fallback)
    default, _ = PLATFORM_DEFAULTS.get(key, (None, None))
    return default
```

### 4.2 Tenant Config Override

```python
def set_tenant_override(
    tenant_id: str,
    config_key: str,
    value: Any,
    set_by: str,
    reason: str,
):
    """
    Super-admin sets a tenant-specific config override.
    """
    # Validate key is overridable
    if config_key not in OVERRIDABLE_KEYS:
        raise ValueError(f"Config key '{config_key}' cannot be overridden at tenant level")
    # Validate value against schema
    _, type_hint = PLATFORM_DEFAULTS[config_key]
    validate_type(value, type_hint)
    # Upsert
    db.execute("""
        INSERT INTO settings.tenant_config_overrides
        (tenant_id, config_key, value, set_by, set_at, reason)
        VALUES (%s, %s, %s, %s, NOW(), %s)
        ON CONFLICT (tenant_id, config_key)
        DO UPDATE SET value = EXCLUDED.value, set_by = EXCLUDED.set_by,
                      set_at = NOW(), reason = EXCLUDED.reason
    """, [tenant_id, config_key, str(value), set_by, reason])
    # Log to config_history
    log_config_change("tenant_override", config_key, str(value), set_by, tenant_id, reason)
```

---

## 5. Environment & Secrets Management

### 5.1 SSM Parameter Paths

```
/eduforge/{env}/database/primary_url
/eduforge/{env}/database/readonly_url
/eduforge/{env}/database/pgbouncer_url
/eduforge/{env}/jwt/public_key
/eduforge/{env}/cdn/r2_bucket
/eduforge/{env}/cdn/r2_public_url
/eduforge/{env}/sqs/doubt_queue_url
/eduforge/{env}/sqs/report_queue_url
/eduforge/{env}/sqs/analytics_ingest_url
/eduforge/{env}/bedrock/region
/eduforge/{env}/sagemaker/churn_endpoint
```

All SSM reads happen at Lambda cold start:

```python
# settings/ssm_loader.py
import boto3, os

def load_config():
    """
    Load all SSM parameters for this environment at cold start.
    Lambda layer caches these; subsequent invocations skip SSM call.
    """
    env = os.environ["APP_ENV"]  # prod, staging, dev
    ssm = boto3.client("ssm")
    resp = ssm.get_parameters_by_path(
        Path=f"/eduforge/{env}/",
        WithDecryption=True,
        Recursive=True,
    )
    config = {}
    for param in resp["Parameters"]:
        key = param["Name"].split("/")[-1]
        config[key] = param["Value"]
    return config

CONFIG = load_config()
```

### 5.2 Secrets Rotation

```python
# Secrets Manager rotation Lambda (called automatically by Secrets Manager)
def rotate_secret(event, context):
    secret_id = event["SecretId"]
    step = event["Step"]

    if "jwt" in secret_id:
        _rotate_jwt_secret(secret_id, step)
    elif "database" in secret_id:
        _rotate_db_password(secret_id, step)


def _rotate_jwt_secret(secret_id: str, step: str):
    """
    JWT rotation with 24-hour overlap window:
    - createSecret: generate new secret
    - setSecret: store new secret in DB
    - testSecret: verify new secret works
    - finishSecret: set new as AWSCURRENT, move old to AWSPREVIOUS (24h grace)
    """
    client = boto3.client("secretsmanager")
    if step == "createSecret":
        new_secret = secrets.token_urlsafe(64)
        client.put_secret_value(
            SecretId=secret_id,
            ClientRequestToken=event["ClientRequestToken"],
            SecretString=json.dumps({"jwt_secret": new_secret}),
            VersionStages=["AWSPENDING"],
        )
    elif step == "finishSecret":
        # Set PENDING as CURRENT; CURRENT becomes PREVIOUS (24h overlap)
        client.update_secret_version_stage(
            SecretId=secret_id,
            VersionStage="AWSCURRENT",
            MoveToVersionId=event["ClientRequestToken"],
            RemoveFromVersionId=_get_current_version(client, secret_id),
        )
```

### 5.3 Config Drift Detection

```python
# Nightly Lambda: compare CDK-expected SSM values vs. actual
def detect_config_drift():
    expected = load_expected_config_from_s3("config/expected-ssm-params.json")
    ssm = boto3.client("ssm")
    actual_params = ssm.get_parameters_by_path(Path="/eduforge/prod/", Recursive=True)
    actual = {p["Name"]: p["Value"] for p in actual_params["Parameters"]}

    drifted = []
    for key, expected_value in expected.items():
        if actual.get(key) != expected_value:
            drifted.append({"key": key, "expected": expected_value, "actual": actual.get(key)})

    if drifted:
        notify_slack(
            channel="#infra-alerts",
            message=f":warning: Config drift detected in production SSM: {len(drifted)} parameters"
                    f"\nDetails: ```{json.dumps(drifted, indent=2)[:1000]}```"
        )
```

---

## 6. Maintenance Mode

### 6.1 Mode Levels

```python
# Middleware — evaluated before all request handlers
MAINTENANCE_MODE_KEY = {"config_key": "platform_maintenance_mode", "scope": "global"}

async def maintenance_middleware(request: Request, call_next):
    mode = RemoteConfig.get("platform_maintenance_mode", default="off")

    if mode == "off":
        return await call_next(request)

    # Check bypass token
    token = request.headers.get("X-Maintenance-Bypass")
    if token and verify_maintenance_bypass_token(token):
        return await call_next(request)

    if mode == "full":
        return Response(
            content=MAINTENANCE_HTML,
            status_code=503,
            media_type="text/html",
            headers={"Retry-After": "3600"},
        )

    if mode == "readonly":
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return await call_next(request)
        return JSONResponse(
            {"error": "maintenance", "message": "Platform is in read-only maintenance mode"},
            status_code=503,
            headers={"Retry-After": "1800"},
        )

    return await call_next(request)
```

### 6.2 Scheduled Maintenance Windows

```python
def schedule_maintenance(
    start: datetime,
    end: datetime,
    mode: str,
    reason: str,
    notify_admins: bool = True,
):
    """
    Pre-schedule a maintenance window.
    EventBridge rules activate/deactivate the maintenance flag.
    """
    # Create EventBridge rule to enable maintenance at start
    events.put_rule(
        Name=f"maintenance-start-{start.strftime('%Y%m%d%H%M')}",
        ScheduleExpression=f"cron({start.minute} {start.hour} {start.day} {start.month} ? {start.year})",
        State="ENABLED",
    )
    events.put_targets(
        Rule=f"maintenance-start-{start.strftime('%Y%m%d%H%M')}",
        Targets=[{
            "Id": "set-maintenance",
            "Arn": MAINTENANCE_LAMBDA_ARN,
            "Input": json.dumps({"action": "enable", "mode": mode}),
        }],
    )
    # Create EventBridge rule to disable maintenance at end
    events.put_rule(
        Name=f"maintenance-end-{end.strftime('%Y%m%d%H%M')}",
        ScheduleExpression=f"cron({end.minute} {end.hour} {end.day} {end.month} ? {end.year})",
        State="ENABLED",
    )
    events.put_targets(
        Rule=f"maintenance-end-{end.strftime('%Y%m%d%H%M')}",
        Targets=[{
            "Id": "clear-maintenance",
            "Arn": MAINTENANCE_LAMBDA_ARN,
            "Input": json.dumps({"action": "disable"}),
        }],
    )
    # Notify all tenant admins 24h and 1h before
    if notify_admins:
        schedule_maintenance_notifications(start, reason)
```

### 6.3 Post-Maintenance Health Check

```python
def post_maintenance_smoke_test():
    """
    Runs 5 smoke tests after maintenance window ends.
    Alerts if any fail — prevents silently broken production.
    """
    tests = [
        ("DB connectivity", lambda: db.execute("SELECT 1")),
        ("Redis (DynamoDB)", lambda: dynamodb.get_item(Key={"pk": "health_check"})),
        ("Bedrock availability", lambda: bedrock.list_foundation_models()),
        ("S3 / R2 write", lambda: s3.put_object(Bucket=R2_BUCKET, Key="health_check", Body=b"ok")),
        ("SQS send", lambda: sqs.send_message(QueueUrl=HEALTH_CHECK_QUEUE, MessageBody="ok")),
    ]
    failures = []
    for name, test_fn in tests:
        try:
            test_fn()
        except Exception as e:
            failures.append(f"{name}: {e}")

    if failures:
        notify_slack(
            channel="#infra-alerts",
            message=f":rotating_light: Post-maintenance smoke tests FAILED:\n" +
                    "\n".join(f"• {f}" for f in failures)
        )
    else:
        notify_slack(channel="#infra-alerts", message=":white_check_mark: Post-maintenance smoke tests passed.")
```

---

## 7. Security Settings

### 7.1 IP Allowlist

```python
# middleware/ip_allowlist.py
async def ip_allowlist_middleware(request: Request, call_next):
    tenant_id = request.state.tenant_id
    if not tenant_id:
        return await call_next(request)

    allowlist = get_platform_config("admin_ip_allowlist", tenant_id)
    if not allowlist:
        return await call_next(request)  # No restriction configured

    client_ip = request.client.host
    allowed_cidrs = json.loads(allowlist)
    if any(ipaddress.ip_address(client_ip) in ipaddress.ip_network(cidr) for cidr in allowed_cidrs):
        return await call_next(request)

    return JSONResponse({"error": "ip_not_allowed"}, status_code=403)
```

### 7.2 MFA Enforcement

```python
def check_mfa_requirement(user: User, tenant_id: str) -> bool:
    """
    Returns True if MFA is required for this user.
    Super-admin can mandate MFA for all staff roles in a tenant.
    """
    mfa_required_roles = get_platform_config("mfa_required_roles", tenant_id)
    if mfa_required_roles:
        required_roles = json.loads(mfa_required_roles)
        if user.role in required_roles:
            return True
    # Super-admin always requires MFA
    if user.role in ("super_admin", "tsp_admin"):
        return True
    return False
```

### 7.3 Failed Login Lockout

```python
# auth/lockout.py
LOCKOUT_THRESHOLD = 5
LOCKOUT_DURATION_SECONDS = 900  # 15 minutes
PROGRESSIVE_DELAYS = [0, 2, 4, 8, 16]  # Seconds per attempt

def check_lockout(user_id: str) -> tuple[bool, int]:
    """
    Returns (is_locked, seconds_remaining).
    Progressive delay between attempts; full lockout at threshold.
    """
    record = dynamodb.get_item(
        TableName="login_attempts",
        Key={"user_id": user_id},
    ).get("Item")

    if not record:
        return False, 0

    attempts = int(record.get("attempt_count", 0))
    last_attempt = float(record.get("last_attempt_ts", 0))
    locked_until = float(record.get("locked_until", 0))

    now = time.time()
    if locked_until > now:
        return True, int(locked_until - now)

    # Progressive delay (not full lockout)
    if attempts < LOCKOUT_THRESHOLD:
        delay = PROGRESSIVE_DELAYS[min(attempts, len(PROGRESSIVE_DELAYS) - 1)]
        if now - last_attempt < delay:
            return True, int(delay - (now - last_attempt))

    return False, 0


def record_failed_attempt(user_id: str):
    record = dynamodb.get_item(
        TableName="login_attempts",
        Key={"user_id": user_id},
    ).get("Item", {})
    attempts = int(record.get("attempt_count", 0)) + 1
    locked_until = (time.time() + LOCKOUT_DURATION_SECONDS) if attempts >= LOCKOUT_THRESHOLD else 0
    dynamodb.put_item(
        TableName="login_attempts",
        Item={
            "user_id": user_id,
            "attempt_count": attempts,
            "last_attempt_ts": str(time.time()),
            "locked_until": str(locked_until),
            "ttl": int(time.time()) + 86400,  # Auto-expire after 24h
        },
    )
```

---

## 8. Module Toggles

### 8.1 Module Enable/Disable

```python
# settings/module_toggles.py
MODULE_DEPENDENCIES = {
    18: [17],   # Exam Paper Builder requires Question Bank
    19: [18],   # Exam Session requires Exam Paper Builder
    20: [19],   # Grading requires Exam Session
    21: [20],   # Report Cards require Grading
    22: [17],   # Mock Tests require Question Bank
    23: [22],   # Leaderboard requires Mock Tests
    46: [17],   # AI Doubt Solver optionally uses Question Bank
}

def disable_module(tenant_id: str, module_num: int, actor_id: str):
    """
    Disable a module for a tenant.
    Validates no dependent modules are currently enabled.
    """
    # Check dependents
    dependents_enabled = []
    for mod, deps in MODULE_DEPENDENCIES.items():
        if module_num in deps:
            if is_enabled(f"module_{mod}_enabled", {"tenant_id": tenant_id}):
                dependents_enabled.append(mod)

    if dependents_enabled:
        raise ValueError(
            f"Cannot disable Module {module_num}: "
            f"Modules {dependents_enabled} depend on it and are currently enabled"
        )

    # Set flag
    FLAGS_TABLE.update_item(
        Key={"flag_name": f"module_{module_num}_enabled"},
        UpdateExpression="SET tenant_overrides.#t = :false",
        ExpressionAttributeNames={"#t": tenant_id},
        ExpressionAttributeValues={":false": False},
    )
    log_config_change("module_disable", f"module_{module_num}_enabled", False, actor_id, tenant_id)
```

---

## 9. Audit & Change Management

### 9.1 Settings Change Audit

```python
# settings/audit.py
def log_config_change(
    change_type: str,
    config_key: str,
    new_value: Any,
    changed_by: str,
    tenant_id: str | None,
    reason: str = "",
):
    db.execute("""
        INSERT INTO settings.config_history
        (change_type, config_key, new_value, changed_by, tenant_id, reason, changed_at, source_ip)
        VALUES (%s, %s, %s, %s, %s, %s, NOW(), current_setting('app.source_ip', true))
    """, [change_type, config_key, str(new_value), changed_by, tenant_id, reason])
```

### 9.2 Dual-Approval for Critical Settings

```python
CRITICAL_SETTINGS = {
    "jwt_secret", "payment_gateway_primary", "mfa_required_roles",
    "admin_ip_allowlist", "platform_maintenance_mode",
    "gst_rate_pct", "dpdpa_consent_version",
}

def request_critical_change(key: str, new_value: Any, requester_id: str, reason: str) -> str:
    """
    Critical settings require approval from a second super-admin.
    Returns approval request ID.
    """
    approval_id = str(uuid4())
    db.execute("""
        INSERT INTO settings.approval_requests
        (approval_id, config_key, new_value, requested_by, reason, status, created_at)
        VALUES (%s, %s, %s, %s, %s, 'pending', NOW())
    """, [approval_id, key, str(new_value), requester_id, reason])
    # Notify other super-admins
    notify_super_admins(
        f"Settings change approval needed: `{key}` by {requester_id}\nReason: {reason}",
        action_url=f"/admin/settings/approvals/{approval_id}"
    )
    return approval_id


def approve_critical_change(approval_id: str, approver_id: str):
    req = db.fetchone("""
        SELECT * FROM settings.approval_requests WHERE approval_id = %s AND status = 'pending'
    """, [approval_id])
    if not req:
        raise ValueError("Invalid or already processed approval request")
    if req["requested_by"] == approver_id:
        raise ValueError("Approver cannot be the same as requester (4-eyes principle)")

    # Apply the change
    apply_platform_config(req["config_key"], req["new_value"], approver_id)
    db.execute("""
        UPDATE settings.approval_requests
        SET status = 'approved', approved_by = %s, approved_at = NOW()
        WHERE approval_id = %s
    """, [approver_id, approval_id])
```

### 9.3 Settings Rollback

```python
def rollback_config(config_key: str, target_history_id: int, actor_id: str, reason: str):
    """Roll back a config to a specific historical value."""
    target = db.fetchone("""
        SELECT new_value, tenant_id FROM settings.config_history
        WHERE history_id = %s AND config_key = %s
    """, [target_history_id, config_key])
    if not target:
        raise ValueError("History record not found")

    if config_key in CRITICAL_SETTINGS:
        return request_critical_change(config_key, target["new_value"], actor_id, f"Rollback: {reason}")
    apply_platform_config(config_key, target["new_value"], actor_id, target["tenant_id"])
```

---

## 10. Database Schema

```sql
-- PostgreSQL: settings schema

CREATE TABLE settings.platform_config (
    config_key          TEXT PRIMARY KEY,
    value               TEXT NOT NULL,
    value_type          TEXT NOT NULL,           -- string, integer, float, boolean, json
    description         TEXT,
    is_tenant_overridable BOOLEAN NOT NULL DEFAULT FALSE,
    updated_by          UUID,
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE settings.tenant_config_overrides (
    override_id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id           UUID NOT NULL,
    config_key          TEXT NOT NULL REFERENCES settings.platform_config(config_key),
    value               TEXT NOT NULL,
    set_by              UUID NOT NULL,
    set_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    reason              TEXT,
    UNIQUE (tenant_id, config_key)
);

CREATE TABLE settings.feature_flags (
    flag_name           TEXT PRIMARY KEY,
    flag_type           TEXT NOT NULL,           -- kill_switch, percentage_rollout, ab_test, targeting
    description         TEXT NOT NULL,
    default_value       BOOLEAN NOT NULL DEFAULT FALSE,
    rollout_pct         INTEGER NOT NULL DEFAULT 0 CHECK (rollout_pct BETWEEN 0 AND 100),
    target_rules        JSONB NOT NULL DEFAULT '[]',
    tenant_overrides    JSONB NOT NULL DEFAULT '{}',
    user_overrides      JSONB NOT NULL DEFAULT '{}',
    variants            JSONB,                   -- for ab_test: [{name, description}]
    ab_metric           TEXT,                    -- Module 53 metric key for auto-evaluation
    status              TEXT NOT NULL DEFAULT 'active', -- active, archived
    owner               TEXT NOT NULL,
    planned_cleanup_date DATE,
    risk_level          TEXT NOT NULL DEFAULT 'low',  -- low, medium, high
    rollback_procedure  TEXT,
    ticket_ref          TEXT,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE settings.feature_flag_audit (
    audit_id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    flag_name           TEXT NOT NULL,
    change_type         TEXT NOT NULL,           -- created, updated, emergency_kill, archived
    changed_by          UUID NOT NULL,
    old_value           JSONB,
    new_value           JSONB NOT NULL,
    reason              TEXT,
    source_ip           INET,
    changed_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
-- Append-only: no UPDATE or DELETE allowed
CREATE RULE no_update_flag_audit AS ON UPDATE TO settings.feature_flag_audit DO INSTEAD NOTHING;
CREATE RULE no_delete_flag_audit AS ON DELETE TO settings.feature_flag_audit DO INSTEAD NOTHING;

CREATE TABLE settings.config_history (
    history_id          BIGSERIAL PRIMARY KEY,
    change_type         TEXT NOT NULL,
    config_key          TEXT NOT NULL,
    old_value           TEXT,
    new_value           TEXT NOT NULL,
    changed_by          UUID NOT NULL,
    tenant_id           UUID,
    reason              TEXT,
    source_ip           INET,
    changed_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
-- Append-only
CREATE RULE no_update_config_history AS ON UPDATE TO settings.config_history DO INSTEAD NOTHING;
CREATE RULE no_delete_config_history AS ON DELETE TO settings.config_history DO INSTEAD NOTHING;

CREATE INDEX idx_config_history_key ON settings.config_history (config_key, changed_at DESC);
CREATE INDEX idx_config_history_tenant ON settings.config_history (tenant_id, changed_at DESC);

CREATE TABLE settings.remote_config_history (
    history_id          BIGSERIAL PRIMARY KEY,
    config_key          TEXT NOT NULL,
    scope               TEXT NOT NULL,           -- "global" | tenant_id
    old_value           TEXT,
    new_value           TEXT NOT NULL,
    changed_by          UUID NOT NULL,
    reason              TEXT,
    changed_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE settings.approval_requests (
    approval_id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    config_key          TEXT NOT NULL,
    new_value           TEXT NOT NULL,
    requested_by        UUID NOT NULL,
    reason              TEXT NOT NULL,
    status              TEXT NOT NULL DEFAULT 'pending',  -- pending, approved, rejected, expired
    approved_by         UUID,
    approved_at         TIMESTAMPTZ,
    rejected_by         UUID,
    rejected_at         TIMESTAMPTZ,
    rejection_reason    TEXT,
    expires_at          TIMESTAMPTZ NOT NULL DEFAULT NOW() + INTERVAL '24 hours',
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE settings.prompt_templates (
    template_id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    use_case            TEXT NOT NULL,           -- doubt_solver, content_generation, report_explanation
    model               TEXT NOT NULL,           -- Bedrock model ID
    version             INTEGER NOT NULL DEFAULT 1,
    content             TEXT NOT NULL,
    system_prompt       TEXT,
    is_active           BOOLEAN NOT NULL DEFAULT TRUE,
    created_by          UUID NOT NULL,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (use_case, model, version)
);
```

---

## 11. API Endpoints

```python
# settings/routes.py (FastAPI)
router = APIRouter(prefix="/admin/settings", tags=["Settings"])

# Platform config
@router.get("/platform-config")
async def list_platform_config(user=Depends(require_super_admin)):
    return db.fetchall("SELECT * FROM settings.platform_config ORDER BY config_key")

@router.put("/platform-config/{key}")
async def update_platform_config(
    key: str,
    payload: ConfigUpdateRequest,
    user=Depends(require_super_admin),
):
    if key in CRITICAL_SETTINGS:
        approval_id = request_critical_change(key, payload.value, user.id, payload.reason)
        return {"status": "pending_approval", "approval_id": approval_id}
    apply_platform_config(key, payload.value, user.id)
    return {"status": "applied"}

# Feature flags
@router.get("/flags")
async def list_flags(user=Depends(require_super_admin)):
    return db.fetchall("SELECT * FROM settings.feature_flags ORDER BY flag_name")

@router.post("/flags")
async def create_flag(payload: FeatureFlagCreate, user=Depends(require_super_admin)):
    count = db.fetchone("SELECT COUNT(*) AS n FROM settings.feature_flags WHERE status = 'active'")
    if count["n"] >= 500:
        raise HTTPException(400, "Maximum 500 active flags. Archive unused flags before creating new ones.")
    flag = flag_service.create(payload, user.id)
    return flag

@router.put("/flags/{flag_name}")
async def update_flag(flag_name: str, payload: FeatureFlagUpdate, user=Depends(require_super_admin)):
    if payload.rollout_pct == 0 and flag_name in CRITICAL_FLAGS:
        return request_critical_change(f"flag.{flag_name}", "disabled", user.id, payload.reason)
    flag_service.update(flag_name, payload, user.id)
    return {"status": "updated"}

@router.post("/flags/{flag_name}/emergency-kill")
async def emergency_kill(flag_name: str, payload: EmergencyKillRequest, user=Depends(require_super_admin)):
    emergency_kill_switch(flag_name, user.id, payload.reason)
    return {"status": "killed", "propagation_latency_seconds": 60}

# Remote config
@router.get("/remote-config")
async def list_remote_config(user=Depends(require_super_admin)):
    resp = dynamodb.scan(TableName="eduforge_remote_config")
    return resp["Items"]

@router.put("/remote-config/{key}")
async def update_remote_config(key: str, payload: RemoteConfigUpdate, user=Depends(require_super_admin)):
    RemoteConfig.set_value(key, payload.value, payload.scope or "global", user.id, payload.reason)
    return {"status": "applied"}

# Maintenance mode
@router.post("/maintenance")
async def set_maintenance(payload: MaintenanceRequest, user=Depends(require_super_admin)):
    if payload.scheduled_start:
        schedule_maintenance(payload.scheduled_start, payload.scheduled_end, payload.mode, payload.reason)
        return {"status": "scheduled"}
    RemoteConfig.set_value("platform_maintenance_mode", payload.mode, "global", user.id, payload.reason)
    return {"status": "applied", "mode": payload.mode}

# Approval workflow
@router.get("/approvals")
async def list_approvals(user=Depends(require_super_admin)):
    return db.fetchall("""
        SELECT * FROM settings.approval_requests
        WHERE status = 'pending' AND expires_at > NOW()
        ORDER BY created_at DESC
    """)

@router.post("/approvals/{approval_id}/approve")
async def approve(approval_id: str, user=Depends(require_super_admin)):
    approve_critical_change(approval_id, user.id)
    return {"status": "approved"}

# Config history & rollback
@router.get("/history/{key}")
async def config_history(key: str, user=Depends(require_super_admin)):
    return db.fetchall("""
        SELECT * FROM settings.config_history WHERE config_key = %s
        ORDER BY changed_at DESC LIMIT 50
    """, [key])

@router.post("/history/{key}/rollback/{history_id}")
async def rollback(key: str, history_id: int, payload: RollbackRequest, user=Depends(require_super_admin)):
    rollback_config(key, history_id, user.id, payload.reason)
    return {"status": "rollback_initiated"}
```

---

## 12. Cost Architecture

| Component | Monthly Cost | Notes |
|-----------|-------------|-------|
| DynamoDB (flags + remote config) | ~Rs. 800 | Low read volume + local LRU caching |
| DynamoDB (login_attempts) | ~Rs. 400 | TTL auto-purges old records |
| SSM Parameter Store | ~Rs. 200 | ~100 parameters, Standard tier free |
| Secrets Manager | ~Rs. 500 | ~20 secrets × rotation |
| Lambda (config invalidation, drift detection) | ~Rs. 300 | Infrequent execution |
| CloudWatch (alarms for flag evaluations) | ~Rs. 200 | |
| **Total** | **~Rs. 2,400/month** | ~Rs. 0.000048/student/month |

Feature flag evaluation cost is effectively **zero marginal cost per request** due to local LRU caching — DynamoDB is hit at most once per 60 seconds per Lambda instance.
