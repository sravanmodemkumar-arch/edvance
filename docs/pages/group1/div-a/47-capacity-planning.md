# 47 — Capacity Planning & Forecasting

---

## 1. Page Metadata

| Field | Value |
|---|---|
| Page title | Capacity Planning & Forecasting |
| Route | `/exec/capacity-planning/` |
| Django view | `CapacityPlanningView` |
| Template | `exec/capacity_planning.html` |
| Priority | **P3** |
| Nav group | Engineering |
| Required roles | `cto` · `platform_engineer` · `superadmin` |
| CEO / COO | Read-only summary only (no infra detail) |
| HTMX poll | None (computed on demand) |
| Cache | Redis TTL 300s (forecast recomputes every 5 min) |
| Theme tokens | bg-base `#040810` · surface-1 `#08101E` · accent `#6366F1` · success `#22C55E` · danger `#EF4444` · warn `#F59E0B` |

---

## 2. Purpose & Business Logic

**The capacity problem:**

EduForge runs 74K+ concurrent exam submissions at peak. Lambda concurrency limits, RDS connection pools, and Redis memory are hard ceilings — if any is breached during an exam, students lose their attempts. This page gives the CTO a 30-day forward view of scheduled exam load vs infrastructure capacity, with automatic alerting when any day is forecast to exceed safe thresholds.

**Forecast methodology:**
```
predicted_peak_concurrency(day) =
    Σ over all exams scheduled on that day:
        exam.enrolled_students × EXPECTED_CONCURRENT_FRACTION

EXPECTED_CONCURRENT_FRACTION = 0.72   # 72% of enrolled students attempt simultaneously at peak
LAMBDA_SAFE_CEILING = 0.80            # alert if forecast exceeds 80% of reserved concurrency
```

**Infrastructure ceilings:**
| Resource | Current Limit | Safe Threshold (80%) |
|---|---|---|
| Lambda Reserved Concurrency | 10,000 | 8,000 |
| RDS max_connections (r6g.2xlarge) | 500 | 400 |
| Redis max memory (cache.r6g.2xlarge) | 26.32 GB | 21 GB |
| CloudFront bandwidth | 50 Gbps | 40 Gbps |

---

## 3. User Roles & Access

| Role | Can View | Can Act |
|---|---|---|
| CTO | All sections | Trigger capacity scale-up, acknowledge alerts |
| Platform Engineer | All sections | Same as CTO |
| CEO / COO | Summary strip only | None |
| Others | No access | Redirect |

---

## 4. Section-wise UI Breakdown

---

### Section 1 — 30-Day Forecast Heatmap

**Purpose:** Calendar-style heatmap — one cell per day, colour = peak concurrency vs Lambda ceiling. Instantly shows which days are "exam heavy."

```
CAPACITY FORECAST — Next 30 Days                    [Recompute Now]
────────────────────────────────────────────────────────────────────────────
         Mon    Tue    Wed    Thu    Fri    Sat    Sun
Week 1    —     2,400  1,800  5,200  9,100  12,400  4,200
                                           🔴HIGH  🟡MED
Week 2   3,100  4,800  6,200  8,400  7,200  11,800  2,100
                                           🟡MED  🔴HIGH
Week 3   2,400  3,800  4,100  5,600  6,800   9,200  1,800
Week 4   3,200  5,100  7,400  6,200  8,100  13,400  3,600
                                            🟡    🔴HIGH
────────────────────────────────────────────────────────────────────────────
Colour key: ■ > 9,600 (>96% ceiling) 🔴CRITICAL  ■ 8,000–9,600 🟡WARNING
            ■ 4,000–7,999 LOW RISK  ■ < 4,000 SAFE
```

- Click any cell → Day Detail modal (Section 5)
- 🔴 days: `CapacityAlert` already created; badge shows "Alert raised"
- "Recompute Now" button: POST `/exec/capacity-planning/actions/recompute/` → enqueues `compute_capacity_forecast()` Celery task immediately (rate-limited once per 5 min)

---

### Section 2 — Active Capacity Alerts

```
CAPACITY ALERTS                                               [Acknowledge All]
────────────────────────────────────────────────────────────────────────────
⚠ Sat 28 Mar   Lambda: forecast 12,400 (124% of 10K limit)  [Ack] [Plan Scale-Up]
⚠ Sat 04 Apr   Lambda: forecast 11,800 (118% of 10K limit)  [Ack] [Plan Scale-Up]
⚠ Sat 11 Apr   Lambda: forecast 13,400 (134% of 10K limit)  [Ack] [Plan Scale-Up]
```

- "Plan Scale-Up" → opens Scale-Up Modal (Section 4)
- Acknowledged alerts: moved to "Reviewed" tab, not deleted (audit trail)
- Alerts auto-email CTO when first created

---

### Section 3 — Resource Utilisation Trend

**Purpose:** Last 30 days of actual vs forecast — how accurate are predictions?

```
RESOURCE UTILISATION — Last 30 Days
────────────────────────────────────────────────────────────────────────────
[4-panel chart grid: Chart.js line charts]

Lambda Concurrency        RDS Connections
Peak: 7,840 / 10,000     Peak: 412 / 500
Avg: 2,210 / 10,000      Avg: 89 / 500
[Line: actual vs forecast vs ceiling]

Redis Memory              Bandwidth (CloudFront)
Peak: 18.2 GB / 26 GB    Peak: 28.4 Gbps / 50 Gbps
Avg: 9.8 GB / 26 GB      Avg: 4.2 Gbps / 50 Gbps
```

- "Forecast vs Actual" overlay: shows prediction accuracy (dashed = forecast, solid = actual)
- Forecast accuracy badge: "Avg error: ±8.4% over last 30 days" — helps CTO trust the model

---

### Section 4 — Scale-Up Planner

**Purpose:** CTO can pre-plan a capacity increase for a specific high-load day.

```
SCALE-UP PLAN — Sat 28 Mar 2026
────────────────────────────────────────────────────────────────────────────
Current Config           Recommended              Max (hard limit)
Lambda: 10,000           15,000 (+5,000)          20,000
RDS: r6g.2xlarge         r6g.4xlarge (+2× conns)  r6g.8xlarge
Redis: cache.r6g.2xlarge cache.r6g.4xlarge         cache.r6g.8xlarge

Cost delta (that day):   ₹ 8,200 extra
Annual cost if permanent: ₹ 29.9 L/yr

[Schedule Scale-Up: 24h before exam day]  [Cancel]
```

- Scale-up is scheduled, not immediate — runs via Terraform/AWS API at specified time
- "Schedule Scale-Up" → POST `/exec/capacity-planning/actions/schedule-scale/` → creates `ScaleUpPlan` record
- Confirmation required: CTO types exam date to confirm
- Auto-scale-down scheduled for 6h after exam window

---

### Section 5 — Day Detail Modal

Triggered by clicking any calendar cell.

```
Saturday, 28 March 2026 — Capacity Detail
────────────────────────────────────────────────────────────────────────────
Scheduled Exams: 14

Institution              Exam Name           Enrolled   Exam Start  Peak Window
─────────────────────────┼───────────────────┼──────────┼───────────┼──────────
Sai Krishna Academy      SSC CGL Mock #8     4,200      10:00 AM    10:00–10:30
Delhi Coaching Centre    RRB NTPC Full Test  3,800      10:00 AM    10:00–10:30
Narayana IIT Academy     JEE Main Series 4   6,100      02:00 PM    02:00–02:30
… (11 more)

PEAK CONCURRENCY BREAKDOWN
10:00–10:30 AM:  ████████████████████░░░░  8,640  (86.4% of limit)
02:00–02:30 PM:  ████████████████████████  9,760  (97.6% of limit)  ⚠ CRITICAL
────────────────────────────────────────────────────────────────────────────
Recommendation: Schedule Scale-Up by 27 Mar to reach 15,000 Lambda concurrency.
```

---

### Section 6 — Cost Forecast

**Purpose:** CFO-facing view (read-only for CEO/COO) of monthly AWS cost driven by exam volume.

```
AWS COST FORECAST — Next 3 Months
────────────────────────────────────────────────────────────────────────────
                Mar 2026     Apr 2026     May 2026
Lambda          ₹4.2 L       ₹4.8 L       ₹3.9 L
RDS             ₹2.8 L       ₹3.1 L       ₹2.6 L
Redis           ₹1.4 L       ₹1.4 L       ₹1.4 L
CloudFront      ₹0.6 L       ₹0.8 L       ₹0.5 L
Other           ₹1.2 L       ₹1.2 L       ₹1.2 L
────────────────────────────────────────────────────────────────────────────
TOTAL           ₹10.2 L      ₹11.3 L      ₹9.6 L
Exam volume     4.2 Cr stu   4.8 Cr stu   3.9 Cr stu
Cost/exam       ₹0.24        ₹0.24        ₹0.25
```

- Cost data sourced from `AWSCostForecast` model (populated from AWS Cost Explorer API daily)
- Cost/exam trend: if rising, CTO is alerted (efficiency regression)

---

## 5. Full Page Wireframe

```
╔══════════════════════════════════════════════════════════════════════════════╗
║  Capacity Planning & Forecasting                        [Recompute Now]      ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  CAPACITY FORECAST — Next 30 Days (Heatmap)                                 ║
║  Mon Tue Wed Thu  Fri   Sat    Sun                                           ║
║  —   2.4K 1.8K 5.2K 9.1K  12.4K🔴 4.2K                                     ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  ACTIVE ALERTS                        RESOURCE UTILISATION TREND            ║
║  ⚠ 28 Mar: Lambda 124%  [Plan →]      Lambda: Peak 7,840/10,000             ║
║  ⚠ 04 Apr: Lambda 118%  [Plan →]      RDS: Peak 412/500                     ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  AWS COST FORECAST                                                          ║
║  Mar: ₹10.2L  Apr: ₹11.3L  May: ₹9.6L  Cost/exam: ₹0.24                   ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 6. Component Architecture

| Component | File | Props |
|---|---|---|
| `CapacityHeatmap` | `components/capacity/heatmap.html` | `days (list of {date, forecast_concurrency, pct_of_limit, alert_level})` |
| `CapacityAlertRow` | `components/capacity/alert_row.html` | `alert_date, resource, forecast_value, limit_value, pct, is_acked, can_act` |
| `ResourceTrendChart` | `components/capacity/resource_trend.html` | `resource_name, days (list of {date, actual, forecast, limit})` |
| `ScaleUpModal` | `components/capacity/scale_up_modal.html` | `target_date, current_config, recommended_config, cost_delta` |
| `DayDetailModal` | `components/capacity/day_detail_modal.html` | `date, exams (list), peak_windows (list)` |
| `CostForecastTable` | `components/capacity/cost_forecast.html` | `months (list of {month, costs_by_service, total, exam_count})` |

---

## 7. HTMX Architecture

| `?part=` | Target | Trigger |
|---|---|---|
| `heatmap` | `#capacity-heatmap` | load |
| `alerts` | `#capacity-alerts` | load |
| `resource-trend` | `#resource-trend` | load |
| `cost-forecast` | `#cost-forecast` | load |
| `day-detail` | `#day-modal` | cell click (hx-get `?part=day-detail&date=2026-03-28`) |

No polling — data is pre-computed. CTO triggers recompute manually or via scheduled task.

---

## 8. Backend View & API

```python
class CapacityPlanningView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "portal.view_capacity_planning"

    FULL_ROLES = {"cto","platform_engineer","superadmin"}
    READ_ROLES = {"ceo","coo"}

    def get(self, request):
        if request.user.role not in self.FULL_ROLES | self.READ_ROLES:
            return redirect("exec:dashboard")
        can_act = request.user.role in self.FULL_ROLES

        r = get_redis_connection()
        cache_key = "capacity:forecast:v1"
        ctx = json.loads(r.get(cache_key) or "{}")
        if not ctx:
            ctx = self._build_forecast_ctx()
            r.setex(cache_key, 300, json.dumps(ctx))

        ctx["can_act"] = can_act
        ctx["is_summary_only"] = request.user.role in self.READ_ROLES

        if _is_htmx(request):
            part = request.GET.get("part","")
            dispatch = {
                "heatmap":        "exec/capacity/partials/heatmap.html",
                "alerts":         "exec/capacity/partials/alerts.html",
                "resource-trend": "exec/capacity/partials/resource_trend.html",
                "cost-forecast":  "exec/capacity/partials/cost_forecast.html",
                "day-detail":     "exec/capacity/partials/day_detail.html",
            }
            if part in dispatch:
                if part == "day-detail":
                    ctx["detail_date"] = request.GET.get("date")
                return render(request, dispatch[part], ctx)
        return render(request, "exec/capacity_planning.html", ctx)
```

**Action endpoints:**

| Method | URL | Permission | Action |
|---|---|---|---|
| POST | `/exec/capacity-planning/actions/recompute/` | CTO/Platform Eng | Enqueue `compute_capacity_forecast()` immediately (rate-limited 1/5min) |
| POST | `/exec/capacity-planning/actions/schedule-scale/` | CTO/Platform Eng | Create `ScaleUpPlan` → triggers Terraform Lambda at scheduled time |
| POST | `/exec/capacity-planning/actions/ack-alert/` | CTO/Platform Eng | Mark `CapacityAlert.acknowledged_at`, `acknowledged_by` |

---

## 9. Database Schema

```python
class CapacityForecastDay(models.Model):
    """One row per day in the 30-day forecast window."""
    forecast_date         = models.DateField(db_index=True)
    scheduled_exam_count  = models.IntegerField()
    total_enrolled        = models.IntegerField()
    peak_concurrency      = models.IntegerField()
    lambda_limit          = models.IntegerField()
    pct_of_lambda_limit   = models.FloatField()
    rds_peak_connections  = models.IntegerField()
    computed_at           = models.DateTimeField()

    class Meta:
        unique_together = ("forecast_date","computed_at")


class CapacityAlert(models.Model):
    SEVERITY = [("warning","Warning"),("critical","Critical")]
    forecast_date    = models.DateField()
    resource         = models.CharField(max_length=50)  # "lambda", "rds", "redis"
    forecast_value   = models.IntegerField()
    resource_limit   = models.IntegerField()
    pct_of_limit     = models.FloatField()
    severity         = models.CharField(max_length=20, choices=SEVERITY)
    acknowledged_at  = models.DateTimeField(null=True)
    acknowledged_by  = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,
                                          on_delete=models.SET_NULL)
    notified_at      = models.DateTimeField(null=True)  # email sent timestamp
    created_at       = models.DateTimeField(auto_now_add=True)


class ScaleUpPlan(models.Model):
    target_date       = models.DateField()
    resource          = models.CharField(max_length=50)
    from_config       = models.JSONField()    # {"lambda_concurrency": 10000}
    to_config         = models.JSONField()    # {"lambda_concurrency": 15000}
    scale_up_at       = models.DateTimeField()   # 24h before exam day
    scale_down_at     = models.DateTimeField()   # 6h after exam window
    created_by        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    executed_at       = models.DateTimeField(null=True)
    status            = models.CharField(max_length=20,
                          choices=[("scheduled","Scheduled"),("executed","Executed"),("failed","Failed")])


class AWSCostForecast(models.Model):
    year_month   = models.CharField(max_length=7)   # "2026-03"
    service      = models.CharField(max_length=50)  # "lambda", "rds", "redis", "cloudfront"
    cost_inr_l   = models.DecimalField(max_digits=10, decimal_places=2)  # in Lakhs
    exam_count   = models.BigIntegerField(default=0)
    fetched_at   = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("year_month","service")
```

**Celery tasks:**
```python
@shared_task
def compute_capacity_forecast():
    """Runs every 5 min, and at 03:00 IST nightly for the 30-day window."""
    from_date = now().date()
    to_date = from_date + timedelta(days=30)
    exams = ScheduledExam.objects.filter(
        scheduled_at__date__range=(from_date, to_date),
        status="scheduled"
    ).select_related("institution")

    days = defaultdict(lambda: {"exams": [], "enrolled": 0})
    for exam in exams:
        day_key = exam.scheduled_at.date()
        days[day_key]["enrolled"] += exam.enrolled_count
        days[day_key]["exams"].append(exam)

    FRACTION = 0.72
    LAMBDA_LIMIT = 10000
    bulk = []
    for day, data in days.items():
        peak = int(data["enrolled"] * FRACTION)
        pct = peak / LAMBDA_LIMIT * 100
        bulk.append(CapacityForecastDay(
            forecast_date=day,
            scheduled_exam_count=len(data["exams"]),
            total_enrolled=data["enrolled"],
            peak_concurrency=peak,
            lambda_limit=LAMBDA_LIMIT,
            pct_of_lambda_limit=pct,
            computed_at=now(),
        ))
        if pct > 80:
            CapacityAlert.objects.get_or_create(
                forecast_date=day, resource="lambda",
                defaults={"forecast_value": peak, "resource_limit": LAMBDA_LIMIT,
                          "pct_of_limit": pct,
                          "severity": "critical" if pct > 96 else "warning"}
            )
    CapacityForecastDay.objects.bulk_create(
        bulk, update_conflicts=True,
        update_fields=["peak_concurrency","pct_of_lambda_limit","computed_at"],
        unique_fields=["forecast_date","computed_at"]
    )
    get_redis_connection().delete("capacity:forecast:v1")
```

---

## 10. Security Considerations

- Infrastructure limits are sensitive operational data — access restricted to engineering roles
- Scale-up actions log to `AuditLog` with before/after config values
- Scale-up plan confirmation requires typing exam date — prevents accidental trigger
- Terraform Lambda (execute scale-up) uses IAM role with least-privilege Lambda:PutFunctionConcurrency only
- Scale-up actions during active exam (war_room active): extra warning modal — scaling Lambda mid-exam can cause brief cold-start spike

---

## 11. Edge Cases

| State | Behaviour |
|---|---|
| Exam cancelled after scale-up scheduled | `ScaleUpPlan` status shows "Stale — exam cancelled". CTO notified. |
| Lambda concurrency raised but exam still exceeds | Alert re-raised with new config values. CTO email resent. |
| Cost Explorer API unavailable | Previous month's actuals shown with "Cost data as of X days ago" notice. |
| Recompute triggered too frequently | Rate-limited to 1 per 5 minutes. Button disabled with countdown. |

---

## 12. Performance & Scaling

- Forecast computation: O(n) over scheduled exams for 30 days — < 2s for 10,000 scheduled exams
- Heatmap: 30 cells, pre-computed — instant render
- Resource trend: 30 days × 4 resources = 120 data points — trivial
- Redis TTL 300s — acceptable lag for planning decisions (not real-time)
- Scale-up execution: Terraform Lambda called asynchronously — CTO sees status update on next page refresh

---

*Last updated: 2026-03-20*
