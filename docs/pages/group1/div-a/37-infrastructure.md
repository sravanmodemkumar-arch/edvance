# 37 — Infrastructure & Capacity

---

## 1. Page Metadata

| Field | Value |
|---|---|
| Page title | Infrastructure & Capacity |
| Route | `/exec/infrastructure/` |
| Django view | `InfrastructureView` |
| Template | `exec/infrastructure.html` |
| Priority | **P1** |
| Nav group | Engineering |
| Required roles | `cto` · `devops` · `sre` · `platform_admin` · `ceo` · `superadmin` |
| COO access | Read-only (no infra actions) |
| CFO access | Denied |
| HTMX poll — live metrics | Every 30s |
| HTMX poll — capacity forecast | Every 300s |
| Cache | Live metrics: Redis TTL 25s · Capacity forecast: Redis TTL 290s |
| Theme tokens | bg-base `#040810` · surface-1 `#08101E` · accent `#6366F1` · danger `#EF4444` · warn `#F59E0B` · success `#22C55E` |

---

## 2. Purpose & Business Logic

**Why this exists separately from Platform Health (02):**

Platform Health shows service-level uptime and latency — the customer-visible view. Infrastructure & Capacity shows the underlying resource utilization — the engineering view. Two different audiences, two different questions:

- Platform Health (02): "Is the Exam Engine working?" (SLA view)
- Infrastructure & Capacity (37): "Is Lambda approaching its concurrency ceiling? What is our RDS read replica lag? What is the next 7 days' exam load vs our current headroom?" (Resource planning view)

**The capacity planning problem:**

EduForge's exam schedule is known in advance. If 12 large coaching centres have scheduled exams for the same Saturday (peak: ~40,000 concurrent), the CTO needs to see — on Monday — that current Lambda reserved concurrency of 5,000 will be insufficient, and proactively scale before Saturday arrives.

This page answers: **"Are we provisioned correctly for the next 7 days?"**

---

## 3. User Roles & Access

| Role | Can View | Can Act |
|---|---|---|
| CEO | All metrics (read-only) | None |
| CTO | All sections | Scale Lambda, modify RDS instance, flush Redis, modify CDN config |
| DevOps / SRE | All sections | All actions except account-level changes |
| Platform Admin | All sections | Read + alert configuration |
| COO | Live metrics only (no infra config) | None |
| CFO | No access | Redirect |

---

## 4. Section-wise UI Breakdown

---

### Section 1 — Live Infrastructure Metrics Strip

**Purpose:** Current health of all infrastructure layers — Lambda, RDS, Redis, CDN — in one row. Same 6 metrics as War Room command strip but with more detail and longer history.

**User interaction:** Each card clickable → scrolls to the full section for that service.

**UI elements — 6 metric cards (30s poll):**

```
╔═══════════════╦═══════════════╦═══════════════╦═══════════════╦═══════════════╦═══════════════╗
║ LAMBDA CONC.  ║ COLD STARTS   ║ RDS POOL      ║ RDS LAG       ║ REDIS MEM     ║ CDN HIT RATIO ║
║  3,842/5,000  ║   2.1%        ║   412/500     ║  142ms        ║  68% of 32GB  ║   94.2%       ║
║  76.8% ⚠WARN  ║  ● Acceptable  ║  82.4% ⚠WARN  ║  ● OK         ║  ● OK         ║  ● OK         ║
╚═══════════════╩═══════════════╩═══════════════╩═══════════════╩═══════════════╩═══════════════╝
```

Zone thresholds identical to War Room (Section 2) — shared business logic, different page context.

**HTMX:** `id="infra-metrics-strip"` `hx-trigger="load, every 30s"` — all values from Redis (Celery beat, same keys as War Room).

---

### Section 2 — Lambda Deep Dive

**Purpose:** Full Lambda configuration + live utilization + cold start trend.

**UI elements:**
```
LAMBDA CONFIGURATION & UTILIZATION
─────────────────────────────────────────────────────────────────────────
Reserved Concurrency: 5,000   Account Limit: 15,000   Burst: +500/min
Current: 3,842 (76.8%)  ████████████████████░░░░   [⚡ Adjust Limit]

CONCURRENCY CHART (last 24h)     COLD START RATE (last 24h)
[Chart.js Line — hourly]         [Chart.js Line — % cold starts]
Peak: 4,102 (12:30 IST)          Avg: 1.8% · Peak: 4.2% (cold deploy)
```

- "Adjust Limit" button: CTO/DevOps only → modal: new concurrency value (validated: must not exceed account limit), reason field, cost estimate shown ("Increasing by 500 = +₹1,200/hr at peak")
- Cold start rate context: "< 5% is acceptable. > 10% = exam latency impact. > 20% = student experience degraded."

**Charts:**
- Concurrency: Chart.js Line, 24h, hourly, threshold lines at 60% (amber) and 85% (red)
- Cold start: Chart.js Line, 24h, % scale 0–25%

**HTMX:** `id="lambda-detail"` `hx-trigger="load, every 30s"` — data from Redis.

---

### Section 3 — RDS Deep Dive

**Purpose:** PostgreSQL cluster health — connections, replica lag, slow queries.

**UI elements:**
```
RDS POSTGRESQL CLUSTER
─────────────────────────────────────────────────────────────────────────
Primary: db.r6g.2xlarge  Replicas: 2  Region: ap-south-1
Connections: 412/500 (82.4%)  ████████████████░░  [Notify DevOps]

Read Replica 1 (ap-south-1a):  Lag: 142ms  ● OK
Read Replica 2 (ap-south-1b):  Lag: 388ms  ⚠ WARN (> 300ms)

TOP SLOW QUERIES (last 1h)
Query                                      Avg   P99   Count
SELECT * FROM exam_attempts WHERE...       82ms  420ms  4,820
SELECT * FROM institution_users WHERE...   45ms  210ms  2,100
```

- Replica lag alert: > 300ms = amber, > 1,000ms = red (read queries may return stale data)
- Slow query table: top 5 queries by P99 execution time. CTO can click → opens query detail with `EXPLAIN ANALYZE` output (read-only, pre-computed)
- "Notify DevOps" button (same as War Room gauge panel)

---

### Section 4 — Redis Deep Dive

**Purpose:** ElastiCache health — memory, eviction rate, hit ratio.

**UI elements:**
```
REDIS (ELASTICACHE)
─────────────────────────────────────────────────────────────────────────
Node: cache.r6g.xlarge  Memory: 21.8 GB / 32 GB (68%)
Hit Ratio: 97.4%  Eviction Rate: 0 keys/s  Connected Clients: 142

MEMORY USAGE CHART (last 24h)        KEY EXPIRY BREAKDOWN
[Chart.js Line]                      war:*           24 keys  TTL 4–10s
                                     sessions:*     8,420 keys TTL 1h
                                     health:*        180 keys  TTL 5m
                                     settlements:*    48 keys  TTL 5–60m
```

- Eviction alert: any eviction > 0/s = amber (cache stampede risk)
- Memory > 85% = amber, > 95% = red with "Flush least-recently-used keys" suggestion
- Key namespace breakdown: helps DevOps identify which module is consuming most memory

---

### Section 5 — CDN (CloudFront) Health

**UI elements:**
```
CDN — CLOUDFRONT
─────────────────────────────────────────────────────────────────────────
Cache Hit Ratio: 94.2%  Requests/min: 18,400  Bandwidth: 2.4 GB/hr
4xx Errors: 0.08%  5xx Errors: 0.00%

TOP UNCACHED PATHS (last 1h)
/api/exam/attempt/*/submit     12,420 misses  (dynamic — expected)
/static/js/htmx.min.js             84 misses  (⚠ should be cached)
```

- Top uncached paths: identify misconfigured cache rules. Static assets with many misses = config error
- "Flush cache" button (CTO only, for specific path patterns): POST `/exec/infrastructure/actions/flush-cdn/`

---

### Section 6 — 7-Day Capacity Forecast

**Purpose:** The CTO's planning view. Upcoming exam schedule vs current infrastructure headroom. Displays as a gantt-style chart or timeline.

**User interaction:** Read-only — planning tool, no actions here.

**UI elements:**
```
CAPACITY FORECAST — Next 7 Days                     ⚠ 2 risk days detected
─────────────────────────────────────────────────────────────────────────
Date        Scheduled Exams  Peak Concurrent  Headroom  Risk
────────────┼─────────────────┼─────────────────┼─────────┼──────────
Wed 22 Mar  18 exams          ~12,000          76%       ✅ OK
Thu 23 Mar   8 exams           ~4,000          92%       ✅ OK
Fri 24 Mar  24 exams          ~18,000          68%       ✅ OK
Sat 25 Mar  48 exams          ~41,000          18%       🔴 RISK
Sun 26 Mar  52 exams          ~44,000          12%       🔴 RISK
Mon 27 Mar  12 exams           ~6,000          88%       ✅ OK
Tue 28 Mar   9 exams           ~3,200          94%       ✅ OK
```

- Peak Concurrent: calculated from `sum(exam.enrolled_count * expected_concurrent_pct)` for all exams that day
- Headroom: `(Lambda reserved concurrency - predicted peak) / Lambda reserved concurrency * 100`
- Risk thresholds: < 30% headroom = red, 30–50% = amber, > 50% = green
- Red risk days auto-create `CapacityAlert` if not already acknowledged

**Chart:** Chart.js grouped bar — blue bars = predicted peak concurrent, horizontal red line = current Lambda limit. When bar approaches line = visual warning.

**HTMX:** `id="capacity-forecast"` `hx-trigger="load, every 300s"` — Celery task pre-computes daily.

---

## 5. Full Page Wireframe

```
╔══════════════════════════════════════════════════════════════════════════════╗
║  Infrastructure & Capacity                            [↺ Refresh]           ║
╠══════════╦══════════╦══════════╦══════════╦══════════╦══════════════════════╣
║ LAMBDA   ║ COLD ST. ║ RDS POOL ║ RDS LAG  ║ REDIS    ║ CDN HIT              ║
║ 3842/5K  ║  2.1%    ║ 412/500  ║  142ms   ║  68%mem  ║  94.2%               ║
╠══════════╩══════════╩══════════╩══════════╩══════════╩══════════════════════╣
║  LAMBDA DEEP DIVE                        RDS DEEP DIVE                      ║
║  Reserved: 5,000  Current: 3,842         Connections: 412/500               ║
║  ████████████████████░░░░  76.8%         Replica 1: 142ms ✅                 ║
║  [Concurrency 24h chart]                 Replica 2: 388ms ⚠                 ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  REDIS DEEP DIVE                         CDN (CLOUDFRONT)                   ║
║  Memory: 21.8/32GB (68%)                 Hit Ratio: 94.2%                   ║
║  Hit Ratio: 97.4%  Evictions: 0          4xx: 0.08%  5xx: 0.00%             ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  7-DAY CAPACITY FORECAST                           ⚠ 2 risk days            ║
║  Sat 25 Mar: 48 exams · ~41,000 concurrent · 18% headroom · 🔴 RISK         ║
║  Sun 26 Mar: 52 exams · ~44,000 concurrent · 12% headroom · 🔴 RISK         ║
║  [Bar chart: predicted peak vs Lambda limit]                                 ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 6. Component Architecture

| Component | File | Props |
|---|---|---|
| `InfraMetricCard` | `components/infra/metric_card.html` | `label, value, pct, zone, history_anchor` |
| `LambdaDeepDive` | `components/infra/lambda.html` | `concurrency, limit, cold_start_pct, chart_data` |
| `RDSDeepDive` | `components/infra/rds.html` | `connections, max_connections, replicas, slow_queries` |
| `RedisDeepDive` | `components/infra/redis.html` | `memory_used, memory_max, hit_ratio, eviction_rate, key_namespaces` |
| `CDNHealth` | `components/infra/cdn.html` | `hit_ratio, requests_per_min, errors_4xx, errors_5xx, uncached_paths` |
| `CapacityForecastRow` | `components/infra/forecast_row.html` | `date, exam_count, predicted_peak, headroom_pct, risk_level` |
| `AdjustLambdaModal` | `components/infra/adjust_lambda_modal.html` | `current_limit, account_limit, cost_per_100` |

---

## 7. HTMX Architecture

| `?part=` | Target | Poll | Trigger |
|---|---|---|---|
| `metrics-strip` | `#infra-metrics-strip` | 30s | load |
| `lambda` | `#lambda-detail` | 30s | load |
| `rds` | `#rds-detail` | 30s | load |
| `redis` | `#redis-detail` | 60s | load |
| `cdn` | `#cdn-detail` | 60s | load |
| `forecast` | `#capacity-forecast` | 300s | load |

---

## 8. Backend View & API

```python
class InfrastructureView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "portal.view_infrastructure"

    def get(self, request):
        allowed = {"cto","devops","sre","platform_admin","ceo","coo","superadmin"}
        if request.user.role not in allowed:
            return redirect("exec:dashboard")

        can_act = request.user.role in {"cto","devops","sre","superadmin"}

        if _is_htmx(request):
            part = request.GET.get("part","")
            ctx = {"can_act": can_act, **self._get_part_data(part)}
            dispatch = {
                "metrics-strip": "exec/infra/partials/metrics_strip.html",
                "lambda":        "exec/infra/partials/lambda.html",
                "rds":           "exec/infra/partials/rds.html",
                "redis":         "exec/infra/partials/redis.html",
                "cdn":           "exec/infra/partials/cdn.html",
                "forecast":      "exec/infra/partials/forecast.html",
            }
            if part in dispatch:
                return render(request, dispatch[part], ctx)
        return render(request, "exec/infrastructure.html",
                      {"can_act": can_act})

    def _get_part_data(self, part):
        r = get_redis_connection()
        if part in ("metrics-strip","lambda","rds","redis","cdn"):
            return {
                "lambda_current":  _read_metric(r, "war:lambda_concurrency"),
                "lambda_limit":    _read_metric(r, "war:lambda_limit"),
                "cold_start_rate": _read_metric(r, "infra:cold_start_rate"),
                "rds_connections": _read_metric(r, "war:rds_connections_current"),
                "rds_max":         _read_metric(r, "war:rds_connections_max"),
                "rds_replica_lag": _read_metric(r, "infra:rds_replica_lag"),
                "redis_memory_pct":_read_metric(r, "infra:redis_memory_pct"),
                "redis_hit_ratio": _read_metric(r, "war:redis_hit_ratio"),
                "cdn_hit_ratio":   _read_metric(r, "infra:cdn_hit_ratio"),
            }
        if part == "forecast":
            cached = r.get("infra:capacity_forecast")
            return {"forecast": json.loads(cached) if cached else []}
        return {}
```

**Action endpoints:**

| Method | URL | Permission | Action |
|---|---|---|---|
| POST | `/exec/infrastructure/actions/adjust-lambda/` | `portal.scale_lambda` (CTO only) | boto3 `put_function_concurrency`, audit log |
| POST | `/exec/infrastructure/actions/flush-cdn/` | `portal.manage_cdn` | CloudFront `create_invalidation`, audit log |
| POST | `/exec/infrastructure/actions/notify-devops/` | `portal.view_infrastructure` | PagerDuty + Slack |

---

## 9. Database Schema & Caching

**Celery Beat Tasks:**

```python
@app.task
def refresh_infra_metrics():
    """Every 25s — writes cold start rate, replica lag, CDN hit ratio to Redis."""
    r = get_redis_connection()
    ts = str(time.time())

    # Cold start rate from CloudWatch Lambda Invocations + InitDuration
    cold_pct = _compute_cold_start_rate()
    r.hset("infra:cold_start_rate", mapping={"value": cold_pct, "ts": ts})

    # RDS replica lag from CloudWatch ReplicaLag metric
    lag_ms = _compute_replica_lag()
    r.hset("infra:rds_replica_lag", mapping={"value": lag_ms, "ts": ts})

    # Redis memory from ElastiCache INFO
    mem_pct = _compute_redis_memory_pct()
    r.hset("infra:redis_memory_pct", mapping={"value": mem_pct, "ts": ts})

    # CDN hit ratio from CloudFront metrics
    hit_ratio = _compute_cdn_hit_ratio()
    r.hset("infra:cdn_hit_ratio", mapping={"value": hit_ratio, "ts": ts})


@app.task
def compute_capacity_forecast():
    """Every 5 min — computes 7-day capacity forecast from exam schedule."""
    forecast = []
    for day_offset in range(7):
        target_date = date.today() + timedelta(days=day_offset)
        exams = Exam.objects.filter(
            scheduled_date=target_date,
            status__in=["scheduled","live"]
        )
        predicted_peak = sum(
            e.enrolled_count * settings.EXPECTED_CONCURRENT_FRACTION
            for e in exams
        )
        lambda_limit = _get_lambda_reserved_concurrency()
        headroom = max(0, (lambda_limit - predicted_peak) / lambda_limit * 100)
        forecast.append({
            "date": target_date.isoformat(),
            "exam_count": exams.count(),
            "predicted_peak": int(predicted_peak),
            "lambda_limit": lambda_limit,
            "headroom_pct": round(headroom, 1),
            "risk": "red" if headroom < 30 else ("amber" if headroom < 50 else "green"),
        })

    r = get_redis_connection()
    r.setex("infra:capacity_forecast", 290, json.dumps(forecast))

    # Auto-create capacity alerts for red risk days
    for day in forecast:
        if day["risk"] == "red":
            CapacityAlert.objects.get_or_create(
                alert_date=day["date"],
                defaults={"headroom_pct": day["headroom_pct"],
                          "predicted_peak": day["predicted_peak"]}
            )
```

---

## 10. Validation Rules

| Action | Validation |
|---|---|
| Adjust Lambda | New limit must be > 0 and ≤ account-level limit (fetched from AWS API). Delta must not exceed +2,000 in single action (safety cap). Requires `portal.scale_lambda` — CTO only. |
| Flush CDN | Path pattern required (cannot flush `*` — partial flush only). Max 10 patterns per request (CloudFront limit). |

---

## 11. Security Considerations

| Concern | Implementation |
|---|---|
| Lambda scale actions | Logged to `AuditLog` with old limit, new limit, actor, timestamp, reason. `put_function_concurrency()` call uses IAM role with minimal permissions (only this action on this function ARN). |
| CDN flush | Creates `CDNFlushLog` record. Path validated server-side (no path traversal). |
| AWS credentials | Never in application code. Lambda execution role via IAM instance profile. All boto3 calls use this role. |
| Infra metrics sensitivity | Raw CloudWatch data treated as internal. Not exposed to any user below Level 4. |

---

## 12. Edge Cases

| State | Behaviour |
|---|---|
| CloudWatch API throttle | boto3 call returns `ThrottlingException` → Celery task backs off 15s, retries once. If both fail → stale data flag set. Page shows "AWS metrics delayed". |
| Lambda at account limit | "Adjust Limit" dropdown shows "Account limit reached (15,000). Contact AWS Support to increase." |
| RDS primary failover | Replica lag spikes to > 30,000ms during failover. Page shows "RDS failover in progress — read traffic may be degraded." Auto-creates P1 incident. |
| Redis memory > 95% | Auto-creates P1 incident. Shows "Emergency: Redis near capacity — exam sessions at risk. [Flush expired keys →]" with one-click action. |
| Forecast data unavailable | Celery task failed → "Capacity forecast unavailable — last computed X min ago. [Retry →]" with manual trigger button (CTO/DevOps only). |

---

## 13. Performance & Scaling

| Endpoint | Target |
|---|---|
| Metrics strip | < 80ms (Redis) |
| Lambda/RDS/Redis deep dives | < 100ms (Redis) |
| CDN health | < 100ms (Redis) |
| Capacity forecast | < 150ms (Redis) |
| Adjust Lambda action | < 3s (AWS API round-trip) |

---

*Last updated: 2026-03-20*
