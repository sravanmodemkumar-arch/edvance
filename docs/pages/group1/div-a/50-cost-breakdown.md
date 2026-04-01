# 50 — Cost Center Breakdown

---

## 1. Page Metadata

| Field | Value |
|---|---|
| Page title | Cost Center Breakdown |
| Route | `/exec/cost-breakdown/` |
| Django view | `CostBreakdownView` |
| Template | `exec/cost_breakdown.html` |
| Priority | **P3** |
| Nav group | Finance |
| Required roles | `cfo` · `superadmin` |
| CEO | Read-only (totals visible, line-item costs hidden) |
| All others | Denied — redirect |
| HTMX poll | None (monthly data) |
| Cache | Redis TTL 3600s |
| Theme tokens | bg-base `#040810` · surface-1 `#08101E` · accent `#6366F1` · success `#22C55E` · danger `#EF4444` · warn `#F59E0B` |

---

## 2. Purpose & Business Logic

**The OpEx visibility problem:**

EduForge's primary cost drivers span 5 external vendors: AWS (infrastructure), SMS gateway providers (Exotel/MSG91), Razorpay (payment gateway fees), AI API providers (OpenAI/Anthropic), and SaaS tools. The CFO needs a monthly view of spending per cost center, trend over time, and unit economics (cost per student, cost per exam, cost per MCQ).

This page consolidates costs from:
1. **AWS Cost Explorer API** — Lambda, RDS, Redis (ElastiCache), CloudFront, S3, other
2. **Razorpay Settlement Reports** — gateway fees per transaction
3. **SMS/OTP Providers** — Exotel + MSG91 monthly invoices (manual entry or API)
4. **AI API Providers** — OpenAI + Anthropic monthly billing (API or manual entry)
5. **SaaS Tools** — Freshdesk, PagerDuty, Sentry, GitHub, Figma (manual entry)
6. **HR/Salary** — manual entry by CFO (not broken down below team level for privacy)

**Unit economics targets:**
| Metric | Target | Threshold |
|---|---|---|
| AWS cost per exam | < ₹0.30 | > ₹0.50 = amber |
| SMS cost per OTP | < ₹0.50 | > ₹0.80 = amber |
| AI cost per MCQ | < ₹1.00 | > ₹1.50 = amber |
| Razorpay fee rate | < 1.8% of GMV | > 2.2% = amber |
| Total OpEx / ARR | < 55% | > 65% = red |

---

## 3. User Roles & Access

| Role | Can View | Can Act |
|---|---|---|
| CFO | All line items, all amounts | Enter manual costs, export PDF/CSV |
| CEO | Total per category only (no line-item breakdown) | Export PDF |
| Others | No access | Redirect |

Role check implementation: `can_view_line_items = request.user.role in {"cfo","superadmin"}` — amounts absent from DOM for non-CFO roles (not CSS-hidden).

---

## 4. Section-wise UI Breakdown

---

### Section 1 — Header & Period Selector

```
Cost Center Breakdown          [Month: March 2026 ▾]  [Export PDF]  [Export CSV]
Last updated: AWS synced 20 Mar 06:12 IST · Manual costs: entered 18 Mar by CFO
```

- Month selector: last 13 months available
- Export CSV: full line-item data for CFO reconciliation
- "Manual costs entered" — shows last manual entry timestamp; if > 45 days stale, amber badge

---

### Section 2 — Total Cost Summary Strip

```
TOTAL OPEX — March 2026                                          (₹ Lakhs)
────────────────────────────────────────────────────────────────────────────
AWS           SMS/OTP      Razorpay Fees   AI APIs       SaaS+Tools    HR/Salary
₹10.2 L       ₹3.8 L       ₹12.4 L         ₹4.2 L        ₹1.8 L        ₹42.0 L
▲ +8.4%       ▼ -2.1%      ▲ +4.2%          ▲ +12.4%      — stable      ▲ +2.1%
(MoM)         (MoM)        (MoM)             ⚠ rising      (MoM)         (MoM)
────────────────────────────────────────────────────────────────────────────
TOTAL OpEx: ₹74.4 L    ARR this month: ₹5.0 Cr    OpEx/ARR: 14.9%   ✅ Healthy
```

- OpEx/ARR compares monthly OpEx vs Monthly Recurring Revenue
- AI APIs ▲ +12.4% MoM: amber — faster than revenue growth
- MoM arrows: compared to previous month

---

### Section 3 — AWS Cost Breakdown

```
AWS COSTS — March 2026                                           (₹)
────────────────────────────────────────────────────────────────────────────
Service           Cost (₹)     % of AWS    MoM       Per-exam unit cost
────────────────┼─────────────┼───────────┼─────────┼────────────────────
Lambda            ₹4,20,000    41.2%       ▲ +9.1%  ₹0.047/exam
RDS               ₹2,80,000    27.5%       ▲ +4.2%  ₹0.031/exam
ElastiCache       ₹1,40,000    13.7%       — stable  ₹0.016/exam
CloudFront        ₹ 60,000     5.9%        ▲ +6.4%  ₹0.007/exam
S3                ₹ 40,000     3.9%        ▲ +2.1%  ₹0.004/exam
Secrets Manager   ₹ 20,000     2.0%        — stable  —
Other             ₹ 60,000     5.9%        ▼ -1.4%  —
────────────────┼─────────────┼───────────┼─────────┼────────────────────
TOTAL AWS         ₹10,20,000             ▲ +8.4%   ₹0.113/exam  ✅
```

- Data sourced from AWS Cost Explorer API (synced daily at 06:00 IST)
- Per-exam cost = service cost / total exam submissions this month
- Target: total AWS cost < ₹0.30/exam — current ₹0.113 = well within target
- Click any row → 30-day daily cost chart for that service

---

### Section 4 — SMS / OTP Cost Breakdown

```
SMS / OTP COSTS — March 2026
────────────────────────────────────────────────────────────────────────────
Provider     OTPs Sent    SMS Sent    Cost (₹)     Rate/OTP    Rate/SMS
────────────┼────────────┼───────────┼────────────┼───────────┼───────────
Exotel       8,24,000     1,24,000    ₹1,24,000    ₹0.42      ₹0.38
MSG91        1,24,000       42,000    ₹ 56,200     ₹0.44      ₹0.41
────────────┼────────────┼───────────┼────────────┼───────────┼───────────
TOTAL        9,48,000     1,66,000    ₹1,80,200    ₹0.43 avg  ₹0.39 avg

Unit cost per OTP: ₹0.43  ✅ (target < ₹0.50)
OTP volume trend: [mini sparkline — 4 weeks]
```

- Exotel: primary gateway (lower cost for bulk OTP)
- MSG91: backup gateway (higher rate, used for failover)
- If OTP cost/unit > ₹0.80: amber alert — contract renegotiation flag

---

### Section 5 — Razorpay Fee Analysis

```
RAZORPAY GATEWAY FEES — March 2026
────────────────────────────────────────────────────────────────────────────
Total Payments Processed   ₹7.84 Cr      (GMV)
Razorpay Fees Charged      ₹12,40,000    (1.58% of GMV)
Contracted Rate            1.60%
Effective Rate             1.58%          ✅ Below contracted cap

FEES BY PAYMENT METHOD
Method          GMV          Fee Rate    Fee Amount
────────────────┼────────────┼───────────┼────────────
UPI              ₹4.12 Cr    0.00%       ₹0  (free)
Netbanking       ₹1.82 Cr    1.80%       ₹3,27,600
Credit Card      ₹1.08 Cr    2.00%       ₹2,16,000
Debit Card       ₹0.64 Cr    0.40%       ₹25,600
EMI              ₹0.18 Cr    1.00%       ₹18,000
────────────────┼────────────┼───────────┼────────────
TOTAL            ₹7.84 Cr    1.58%       ₹5,87,200

Fee overcharge check: ✅ No overcharge detected this month.
```

- Sourced from `SettlementFeeAudit` model (page 33 — Razorpay Settlements)
- If effective_rate > contracted_rate: red alert + "Dispute fees" action link
- UPI 0% encourages institutions to use UPI — CFO uses this for payment method nudge decisions

---

### Section 6 — AI API Cost Breakdown

```
AI API COSTS — March 2026
────────────────────────────────────────────────────────────────────────────
Provider         MCQs Gen     Explanations   Other      Cost (₹)    Cost/MCQ
────────────────┼────────────┼──────────────┼──────────┼───────────┼─────────
OpenAI GPT-4o    28,420        —             —          ₹2,84,200   ₹1.00
OpenAI GPT-3.5    8,200        —             42,000     ₹ 41,000    ₹0.16
Anthropic Claude 12,100       12,000         —          ₹1,21,000   ₹1.00
────────────────┼────────────┼──────────────┼──────────┼───────────┼─────────
TOTAL            48,720       12,000         42,000     ₹4,46,200   ₹0.82

Budget this month: ₹5.00L    Consumed: ₹4.46L (89.2%)  ⚠ Approaching limit
```

- Sourced from `AIAPICallLog` model (page 48 — AI/ML Operations)
- Budget progress bar: green < 70% → amber 70–90% → red > 90%
- Cost/MCQ > ₹1.50: amber — prompt engineering or model choice review needed

---

### Section 7 — SaaS Tools & HR Summary

```
SAAS TOOLS — March 2026 (CFO manual entry)
────────────────────────────────────────────────────────────────────────────
Tool            Cost (₹)     Seats/Usage     Cost/User    Notes
────────────────┼────────────┼───────────────┼────────────┼──────────────
Freshdesk        ₹48,000      12 agents       ₹4,000/mo   Enterprise plan
PagerDuty        ₹36,000      —               —            Platform tier
Sentry           ₹18,000      —               —            Business tier
GitHub           ₹21,000      42 devs         ₹500/mo      Team plan
Figma            ₹12,000       8 designers    ₹1,500/mo    Professional
Zoom             ₹ 9,600      —               —            Business
Other            ₹36,400      —               —            Misc SaaS
────────────────────────────────────────────────────────────────────────────
TOTAL SaaS       ₹1,81,000                               ✅ Within budget

HR / SALARY (CFO entry — aggregated, not per-person)
Total Headcount:    60 employees
Total Salary Cost:  ₹42.0 L/month
Revenue/Employee:   ₹73.2 L ARR/employee  ✅ Healthy
```

- SaaS costs: manually entered by CFO via `/admin/cost/saastoolcost/` (Django Admin)
- HR total: single aggregated entry — no per-employee breakdown on this page (privacy)
- Revenue/Employee from Board Dashboard (page 45) — shown in context

---

### Section 8 — Monthly Cost Trend Chart

```
TOTAL OPEX TREND — Last 12 Months (₹ Lakhs)
────────────────────────────────────────────────────────────────────────────
[Stacked bar chart: Chart.js]
  Stacks: AWS (indigo) / SMS (violet) / Razorpay (emerald) / AI (amber) / SaaS (sky) / HR (slate)
  Apr 25: ₹58.2L  May: ₹59.4L  Jun: ₹60.8L  Jul: ₹63.2L  Aug: ₹64.4L
  Sep: ₹64.8L  Oct: ₹65.2L  Nov: ₹66.4L  Dec: ₹68.8L  Jan 26: ₹70.2L
  Feb: ₹72.8L  Mar: ₹74.4L

MoM growth (OpEx): ▲ +2.2% avg    MRR growth: ▲ +3.4% avg
Revenue growing faster than costs ✅ — improving operational leverage.
```

---

## 5. Full Page Wireframe

```
╔══════════════════════════════════════════════════════════════════════════════╗
║  Cost Center Breakdown              [March 2026 ▾]  [Export PDF]  [CSV]     ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  AWS: ₹10.2L  SMS: ₹3.8L  Razorpay: ₹12.4L  AI: ₹4.2L ⚠  HR: ₹42.0L     ║
║  Total OpEx: ₹74.4L   OpEx/ARR: 14.9% ✅                                   ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  AWS BREAKDOWN                        SMS / OTP COSTS                       ║
║  Lambda: ₹4.2L  ₹0.047/exam ✅        Exotel: ₹0.42/OTP  MSG91: ₹0.44/OTP ║
║  RDS: ₹2.8L  CloudFront: ₹0.6L        Total: ₹0.43/OTP ✅                  ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  RAZORPAY FEES                        AI API COSTS                          ║
║  GMV: ₹7.84Cr  Fee: 1.58% ✅          MTD: ₹4.46L / ₹5.0L (89%) ⚠         ║
║  UPI: 0% free  Netbanking: 1.80%      GPT-4o: ₹1.00/MCQ  Claude: ₹1.00/MCQ ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  SAAS + HR: Freshdesk ₹48K  GitHub ₹21K  HR Total ₹42.0L                   ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  OPEX TREND — 12 Months (Stacked Bar: AWS/SMS/Razorpay/AI/SaaS/HR)         ║
║  ₹58.2L → ₹74.4L  OpEx growth +2.2%/mo vs Revenue +3.4%/mo ✅              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 6. Component Architecture

| Component | File | Props |
|---|---|---|
| `CostSummaryStrip` | `components/cost/summary_strip.html` | `categories (list of {name, cost_l, mom_pct, alert_level}), total_opex, opex_arr_pct` |
| `AWSBreakdownTable` | `components/cost/aws_table.html` | `services (list of {name, cost, pct, mom_pct, per_exam_cost})` |
| `SMSCostTable` | `components/cost/sms_table.html` | `providers (list of {name, otp_sent, sms_sent, cost, rate_per_otp})` |
| `RazorpayCostTable` | `components/cost/razorpay_table.html` | `gmv, fee_rate, contracted_rate, fees_by_method` |
| `AICostTable` | `components/cost/ai_table.html` | `providers, total_cost, budget, cost_per_mcq` |
| `OpExTrendChart` | `components/cost/trend.html` | `months (list of {month, costs_by_category})` |

---

## 7. HTMX Architecture

| `?part=` | Target | Trigger |
|---|---|---|
| `summary` | `#cost-summary` | load |
| `aws` | `#aws-costs` | load + month change |
| `sms` | `#sms-costs` | load + month change |
| `razorpay` | `#razorpay-costs` | load + month change |
| `ai` | `#ai-costs` | load + month change |
| `saas-hr` | `#saas-hr-costs` | load + month change |
| `trend` | `#cost-trend` | load |

No polling — monthly data.

---

## 8. Backend View & API

```python
class CostBreakdownView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "portal.view_cost_breakdown"

    CFO_ROLES = {"cfo","superadmin"}
    CEO_ROLES = {"ceo"}

    def get(self, request):
        if request.user.role not in self.CFO_ROLES | self.CEO_ROLES:
            return redirect("exec:dashboard")

        can_view_line_items = request.user.role in self.CFO_ROLES
        year_month = request.GET.get("month", current_year_month())

        cache_key = f"cost:breakdown:{year_month}:{can_view_line_items}"
        r = get_redis_connection()
        ctx = json.loads(r.get(cache_key) or "{}")
        if not ctx:
            ctx = self._build_cost_ctx(year_month, can_view_line_items)
            r.setex(cache_key, 3600, json.dumps(ctx))

        ctx["can_view_line_items"] = can_view_line_items

        if _is_htmx(request):
            part = request.GET.get("part","")
            dispatch = {
                "summary":  "exec/cost/partials/summary.html",
                "aws":      "exec/cost/partials/aws.html",
                "sms":      "exec/cost/partials/sms.html",
                "razorpay": "exec/cost/partials/razorpay.html",
                "ai":       "exec/cost/partials/ai.html",
                "saas-hr":  "exec/cost/partials/saas_hr.html",
                "trend":    "exec/cost/partials/trend.html",
            }
            if part in dispatch:
                return render(request, dispatch[part], ctx)
        return render(request, "exec/cost_breakdown.html", ctx)
```

---

## 9. Database Schema

```python
class AWSServiceCost(models.Model):
    """Daily AWS cost per service from Cost Explorer API."""
    year_month   = models.CharField(max_length=7)
    service      = models.CharField(max_length=100)
    cost_inr     = models.DecimalField(max_digits=12, decimal_places=2)
    fetched_at   = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("year_month","service")


class SMSProviderCost(models.Model):
    """Monthly SMS/OTP cost per provider (API or manual entry)."""
    year_month   = models.CharField(max_length=7)
    provider     = models.CharField(max_length=50)  # "exotel","msg91"
    otp_sent     = models.IntegerField(default=0)
    sms_sent     = models.IntegerField(default=0)
    cost_inr     = models.DecimalField(max_digits=12, decimal_places=2)
    source       = models.CharField(max_length=20,
                    choices=[("api","API"),("manual","Manual CFO Entry")])
    entered_by   = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,
                                      on_delete=models.SET_NULL)
    entered_at   = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("year_month","provider")


class SaaSToolCost(models.Model):
    """Monthly SaaS tool cost — manual entry by CFO."""
    year_month   = models.CharField(max_length=7)
    tool_name    = models.CharField(max_length=100)
    cost_inr     = models.DecimalField(max_digits=10, decimal_places=2)
    seats        = models.IntegerField(null=True)
    notes        = models.CharField(max_length=200, blank=True)
    entered_by   = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,
                                      on_delete=models.SET_NULL)
    entered_at   = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("year_month","tool_name")


class HRCostEntry(models.Model):
    """Aggregated monthly HR/salary cost — CFO manual entry, no per-employee breakdown."""
    year_month       = models.CharField(max_length=7, unique=True)
    total_cost_inr   = models.DecimalField(max_digits=14, decimal_places=2)
    headcount        = models.IntegerField()
    entered_by       = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,
                                          on_delete=models.SET_NULL)
    entered_at       = models.DateTimeField(auto_now=True)
```

**Celery tasks:**
```python
@shared_task
def sync_aws_costs():
    """Daily at 06:30 IST. Fetches previous day's costs from AWS Cost Explorer."""
    ce = boto3.client("ce", region_name="ap-south-1")
    response = ce.get_cost_and_usage(
        TimePeriod={"Start": yesterday(), "End": today()},
        Granularity="MONTHLY",
        GroupBy=[{"Type":"DIMENSION","Key":"SERVICE"}],
        Metrics=["UnblendedCost"],
    )
    INR_RATE = Decimal(settings.AWS_COST_INR_RATE)  # fetched from config, e.g. 83.5
    for group in response["ResultsByTime"][0]["Groups"]:
        service = group["Keys"][0]
        usd = Decimal(group["Metrics"]["UnblendedCost"]["Amount"])
        AWSServiceCost.objects.update_or_create(
            year_month=current_year_month(), service=service,
            defaults={"cost_inr": usd * INR_RATE}
        )
    # Invalidate Redis
    r = get_redis_connection()
    r.delete(f"cost:breakdown:{current_year_month()}:True")
    r.delete(f"cost:breakdown:{current_year_month()}:False")
```

---

## 10. Security Considerations

- Most sensitive page after Board Dashboard (investor-grade financials + supplier contracts)
- Every page view by CFO/CEO logged in `AuditLog`
- Line-item costs (individual service breakdown) absent from DOM for CEO role — not CSS-hidden
- HR total: deliberately not shown per-employee; only aggregate to prevent compensation speculation
- Razorpay contracted rate: visible only to CFO/superadmin (competitive contract terms)
- CSV export: rate-limited 3/day; email notification to CFO on every export

---

## 11. Edge Cases

| State | Behaviour |
|---|---|
| AWS Cost Explorer API unavailable | Shows previous day's data with "Cost data as of X days ago" notice |
| Manual SMS cost not entered for month | SMS row shows "Manual entry required" with link to entry form (CFO only) |
| AI budget exceeded mid-month | Cost card turns red; pipeline auto-pause already triggered (page 48); note shown here |
| Month not yet complete (current month) | All figures shown as "MTD" (Month to Date) with % of month elapsed |
| Razorpay effective rate exceeds contracted | Red alert on Razorpay section + link to Settlements page dispute action |

---

## 12. Performance & Scaling

- AWS cost sync: daily Celery task, < 5s API call
- All data pre-aggregated by month — page load is simple DB reads
- Trend chart: 12 months × 6 cost categories = 72 data points — trivial
- Redis TTL 3600s — monthly data changes only once/day (AWS sync) or on CFO manual entry
- CSV export: synchronous for monthly data (trivial volume); no async needed

---

*Last updated: 2026-03-20*
