# 46 — Domain Performance Overview

---

## 1. Page Metadata

| Field | Value |
|---|---|
| Page title | Domain Performance Overview |
| Route | `/exec/domain-performance/` |
| Django view | `DomainPerformanceView` |
| Template | `exec/domain_performance.html` |
| Priority | **P3** |
| Nav group | Strategic |
| Required roles | `ceo` · `coo` · `cto` · `superadmin` |
| All others | Denied — redirect with toast |
| HTMX poll | None (static periodic data) |
| Cache | Redis TTL 1800s |
| Theme tokens | bg-base `#040810` · surface-1 `#08101E` · accent `#6366F1` · success `#22C55E` · danger `#EF4444` · warn `#F59E0B` |

---

## 2. Purpose & Business Logic

EduForge serves institutions preparing students across multiple competitive exam domains. This page answers the CEO and COO's key strategic question: **which domains are growing, which are declining, and where should sales/product investment focus next?**

**Domains tracked:**
- **Government Jobs:** SSC (CGL/CHSL/MTS), RRB (NTPC/Group D/JE), UPSC, State PSC, Banking (IBPS PO/Clerk/SO, SBI PO)
- **Medical:** NEET UG, NEET PG, AIIMS
- **Engineering:** JEE Main, JEE Advanced, BITSAT
- **State Boards:** AP Intermediate (BIEAP), TS Intermediate (BIE Telangana), Maharashtra HSC, Karnataka PUC
- **Professional:** CA Foundation/Inter/Final, CS Foundation, CMA

**Key business questions answered:**
1. Which domain has the highest institution count and exam volume?
2. Which domain has the best ARR per institution (product-market fit)?
3. Which domain is growing fastest (new institution signups last 90 days)?
4. Which domain has the highest student engagement (DAU/enrolled)?
5. Which domains have low platform utilisation (at-risk for churn)?

---

## 3. User Roles & Access

| Role | Can View | Can Act |
|---|---|---|
| CEO | All data | Export PDF |
| COO | All data | Export PDF |
| CTO | All (read-only) | None |
| Others | No access | Redirect |

---

## 4. Section-wise UI Breakdown

---

### Section 1 — Header & Filters

```
Domain Performance Overview            [Period: Last 90 days ▾]  [Export PDF]
Last computed: 20 Mar 2026 02:18 IST
```

- Period selector: Last 30 / 90 / 180 / 365 days
- Export PDF: A4 portrait, one domain per page, EduForge branding
- "Last computed" shows when nightly aggregation ran

---

### Section 2 — Top-Line Domain Summary Grid

```
DOMAIN SUMMARY                                                (Last 90 days)
────────────────────────────────────────────────────────────────────────────
Domain          Institutions  Students     Exams/Month  ARR(Cr)  ARR/Inst
────────────────┼─────────────┼────────────┼────────────┼─────────┼─────────
SSC/RRB/Govt    820           9,40,000     2,40,000     ₹26.4    ₹3.22L
NEET/Medical    410           5,20,000     1,80,000     ₹15.8    ₹3.85L
JEE/Engg        280           2,80,000     95,000       ₹9.2     ₹3.28L
AP/TS Boards    310           8,60,000     3,20,000     ₹5.4     ₹1.74L
Banking         130           1,20,000     48,000       ₹2.4     ₹1.85L
CA/Prof         100           80,000       22,000       ₹0.8     ₹0.80L
────────────────┼─────────────┼────────────┼────────────┼─────────┼─────────
TOTAL           2,050         28,00,000    9,05,000     ₹60.0    ₹2.93L
```

- ARR/Inst column: colour-coded — > ₹3.5L green, ₹2L–₹3.5L neutral, < ₹2L amber
- Click any row → expanded domain detail drawer

---

### Section 3 — Growth Leaderboard

**Purpose:** Shows which domains are adding new institutions and revenue fastest.

```
GROWTH LEADERBOARD — New Institutions (Last 90 Days)
────────────────────────────────────────────────────────────────────────────
Domain          New Inst   Growth%   New Students    New ARR
────────────────┼──────────┼─────────┼────────────────┼───────────
NEET/Medical    +52        ▲ 14.5%   +68,000          ₹2.1 Cr   🔥 Fastest
JEE/Engg        +31        ▲ 12.5%   +38,000          ₹1.1 Cr
SSC/RRB/Govt    +48        ▲  6.2%   +72,000          ₹1.6 Cr
Banking         +12        ▲ 10.2%   +14,000          ₹0.2 Cr
AP/TS Boards     +8        ▲  2.6%    +9,000          ₹0.1 Cr
CA/Prof          +4        ▲  4.2%    +3,200          ₹0.04 Cr
```

- 🔥 badge: fastest-growing domain by Growth% this period
- Sortable by any column

---

### Section 4 — Engagement Heatmap

**Purpose:** For each domain, how actively are enrolled students actually using the platform? Low engagement = churn risk.

```
STUDENT ENGAGEMENT BY DOMAIN
────────────────────────────────────────────────────────────────────────────
Domain          Enrolled    DAU       DAU/MAU   Exams/Student/Mo   Status
────────────────┼───────────┼─────────┼─────────┼──────────────────┼──────
SSC/RRB/Govt    9,40,000    84,200    42.3%     2.8                ✅ High
NEET/Medical    5,20,000    62,400    40.8%     3.2                ✅ High
JEE/Engg        2,80,000    30,800    38.2%     2.6                ✅ Healthy
AP/TS Boards    8,60,000    38,200    14.8%     0.9               ⚠ Low
Banking         1,20,000    12,100    33.8%     1.9                ✅ Healthy
CA/Prof           80,000     5,800    24.2%     1.4               ⚠ Low
```

- DAU/MAU < 20%: amber; < 10%: red
- Exams/Student/Mo < 1.0: amber — indicates students are enrolled but not taking exams
- Low engagement domains: COO sees "Review CSM assignment" tooltip

---

### Section 5 — Revenue per Domain Trend (Chart)

**Purpose:** 12-month ARR trend per domain — stacked area chart.

```
ARR TREND — Last 12 Months (₹ Cr)
────────────────────────────────────────────────────────────────────────────
[Stacked area chart: Chart.js]
  Series: SSC/Govt (indigo), NEET (emerald), JEE (violet),
          AP/TS (amber), Banking (sky), CA/Prof (rose)
  X-axis: Apr 2025 → Mar 2026
  Y-axis: ₹ Cr (0 → 65)
  Tooltip: hover shows per-domain ARR for that month
```

---

### Section 6 — Domain Detail Drawer

Triggered by clicking any domain row in Section 2.

```
SSC / RRB / Govt Jobs Domain
────────────────────────────────────────────────────────────────────────────
Institutions:  820 active   |  Top State: Andhra Pradesh (214 inst)
Students:      9.4L         |  Avg class size: 1,146
ARR:           ₹26.4 Cr     |  ARPU: ₹3.22L / inst / year
Churn (90d):   8 inst lost  |  Churn Rate: 1.0%

TOP EXAM TYPES (by volume)
SSC CGL:         1,42,000 exams/mo  (59%)
SSC CHSL:          48,000 exams/mo  (20%)
RRB NTPC:          31,000 exams/mo  (13%)
Others:            19,000 exams/mo   (8%)

HEALTH DISTRIBUTION
✅ Healthy (80–100):   614 institutions  (74.9%)
🟡 At Risk (60–79):    148 institutions  (18.1%)
🔴 Critical (<60):      58 institutions   (7.1%)

AT-RISK INSTITUTIONS (Top 5 by ARR at risk)
Delhi Coaching Hub       ₹4.2L ARR  Score: 62  [View Health →]
Rajasthan SSC Academy    ₹3.8L ARR  Score: 58  [View Health →]
…
```

- Drawer links to Customer Health page (35) for each institution
- Health distribution bar (green/amber/red proportional widths)

---

## 5. Full Page Wireframe

```
╔══════════════════════════════════════════════════════════════════════════════╗
║  Domain Performance Overview        [Last 90 days ▾]  [Export PDF]          ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  DOMAIN SUMMARY                                                              ║
║  SSC/Govt: 820 inst  9.4L stu  ₹26.4Cr  ₹3.22L/inst                        ║
║  NEET:     410 inst  5.2L stu  ₹15.8Cr  ₹3.85L/inst  [fastest growing]      ║
║  JEE:      280 inst  2.8L stu   ₹9.2Cr  ₹3.28L/inst                         ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  GROWTH LEADERBOARD                  ENGAGEMENT HEATMAP                     ║
║  NEET:   +52 inst  ▲14.5% 🔥        SSC: DAU/MAU 42.3% ✅                   ║
║  SSC:    +48 inst  ▲ 6.2%           AP/TS: DAU/MAU 14.8% ⚠                  ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  ARR TREND — 12 Month (Stacked Area)                                        ║
║  [Chart.js stacked area: SSC(indigo) NEET(green) JEE(violet)…]              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 6. Component Architecture

| Component | File | Props |
|---|---|---|
| `DomainSummaryRow` | `components/domain/summary_row.html` | `domain_name, inst_count, student_count, exams_per_month, arr_cr, arr_per_inst` |
| `GrowthLeaderboardRow` | `components/domain/growth_row.html` | `domain_name, new_inst, growth_pct, new_students, new_arr, is_fastest` |
| `EngagementRow` | `components/domain/engagement_row.html` | `domain_name, enrolled, dau, dau_mau_pct, exams_per_student_mo, alert_level` |
| `ARRTrendChart` | `components/domain/arr_trend.html` | `months (list), series (list of {domain, monthly_arr})` |
| `DomainDetailDrawer` | `components/domain/detail_drawer.html` | `domain_data, top_exams, health_distribution, at_risk_institutions` |

---

## 7. HTMX Architecture

| `?part=` | Target | Trigger |
|---|---|---|
| `summary` | `#domain-summary` | load |
| `growth` | `#domain-growth` | load + period change |
| `engagement` | `#domain-engagement` | load + period change |
| `trend` | `#arr-trend` | load + period change |
| `domain-detail` | `#domain-drawer` | row click (hx-get with `?domain=ssc`) |

No polling — data is computed nightly.

---

## 8. Backend View & API

```python
class DomainPerformanceView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "portal.view_domain_performance"

    def get(self, request):
        if request.user.role not in {"ceo","coo","cto","superadmin"}:
            messages.warning(request, "Access restricted.")
            return redirect("exec:dashboard")

        period_days = int(request.GET.get("period", 90))
        r = get_redis_connection()
        cache_key = f"domain:perf:{period_days}"
        ctx = json.loads(r.get(cache_key) or "{}")
        if not ctx:
            ctx = self._build_domain_data(period_days)
            r.setex(cache_key, 1800, json.dumps(ctx))

        if _is_htmx(request):
            part = request.GET.get("part","")
            dispatch = {
                "summary":       "exec/domain/partials/summary.html",
                "growth":        "exec/domain/partials/growth.html",
                "engagement":    "exec/domain/partials/engagement.html",
                "trend":         "exec/domain/partials/trend.html",
                "domain-detail": "exec/domain/partials/detail_drawer.html",
            }
            if part in dispatch:
                domain_slug = request.GET.get("domain","")
                ctx["selected_domain"] = domain_slug
                return render(request, dispatch[part], ctx)
        return render(request, "exec/domain_performance.html", ctx)

    def _build_domain_data(self, period_days):
        since = now() - timedelta(days=period_days)
        domains = DomainSnapshot.objects.filter(period_days=period_days).order_by("-arr_cr")
        return {
            "domains": [d.to_dict() for d in domains],
            "period_days": period_days,
            "computed_at": DomainSnapshot.objects.latest("computed_at").computed_at.isoformat(),
        }
```

---

## 9. Database Schema

```python
class DomainSnapshot(models.Model):
    """Nightly computed snapshot of per-domain metrics."""
    domain_slug     = models.CharField(max_length=50)  # "ssc_rrb", "neet", "jee", etc.
    domain_label    = models.CharField(max_length=100)
    period_days     = models.IntegerField()             # 30, 90, 180, 365
    inst_count      = models.IntegerField()
    student_count   = models.IntegerField()
    exams_per_month = models.IntegerField()
    arr_cr          = models.DecimalField(max_digits=10, decimal_places=2)
    arr_per_inst    = models.DecimalField(max_digits=10, decimal_places=2)
    new_inst        = models.IntegerField()
    growth_pct      = models.DecimalField(max_digits=6, decimal_places=2)
    dau             = models.IntegerField()
    mau             = models.IntegerField()
    exams_per_student_mo = models.DecimalField(max_digits=6, decimal_places=2)
    computed_at     = models.DateTimeField(db_index=True)

    class Meta:
        unique_together = ("domain_slug","period_days","computed_at")
        indexes = [models.Index(fields=["period_days","computed_at"])]


class DomainMonthlyARR(models.Model):
    """Monthly ARR per domain for trend chart."""
    domain_slug     = models.CharField(max_length=50)
    year_month      = models.CharField(max_length=7)   # "2026-03"
    arr_cr          = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ("domain_slug","year_month")
```

**Celery task:**
```python
@shared_task
def compute_domain_snapshots():
    """Runs nightly at 01:00 IST. Aggregates per-domain metrics from Tenant schemas."""
    for period_days in [30, 90, 180, 365]:
        since = now() - timedelta(days=period_days)
        for domain_slug, domain_label in DOMAIN_CHOICES:
            insts = Institution.objects.filter(domain=domain_slug, is_active=True)
            snapshot = _aggregate_domain(insts, since, domain_slug, domain_label, period_days)
            DomainSnapshot.objects.update_or_create(
                domain_slug=domain_slug, period_days=period_days,
                computed_at=now().replace(hour=0,minute=0,second=0),
                defaults=snapshot,
            )
    # Invalidate Redis cache
    r = get_redis_connection()
    for days in [30, 90, 180, 365]:
        r.delete(f"domain:perf:{days}")
```

---

## 10. Security Considerations

- Financial ARR data — access logged in `AuditLog`
- Domain data is aggregated — no individual institution data visible without drawer interaction
- Drawer detail requires same role check (server-side, not just client-side show/hide)
- PDF export rate-limited: 5/day per user

---

## 11. Edge Cases

| State | Behaviour |
|---|---|
| Domain with 0 institutions | Row still shown with zeros — helps CEO see domain gaps |
| Engagement data unavailable (Firebase outage) | DAU/MAU column shows "—" with tooltip "Last synced Xh ago" |
| New domain added mid-period | Growth% computed from first institution date, not period start |

---

## 12. Performance & Scaling

- All data pre-computed nightly — no heavy queries on page load
- 2,050 institutions × 6 domains × 4 periods = manageable aggregation
- Stacked area chart: 12 months × 6 domains = 72 data points — trivial
- Redis TTL 1800s — refreshed every time nightly task runs
- Domain drawer: fetched on demand (hx-get) — not pre-loaded

---

*Last updated: 2026-03-20*
