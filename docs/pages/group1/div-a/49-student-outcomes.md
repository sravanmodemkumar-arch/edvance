# 49 — Student Outcomes Analytics

---

## 1. Page Metadata

| Field | Value |
|---|---|
| Page title | Student Outcomes Analytics |
| Route | `/exec/student-outcomes/` |
| Django view | `StudentOutcomesView` |
| Template | `exec/student_outcomes.html` |
| Priority | **P3** |
| Nav group | Strategic |
| Required roles | `ceo` · `coo` · `superadmin` |
| CTO / CFO | Denied |
| HTMX poll | None (aggregated data) |
| Cache | Redis TTL 3600s |
| Theme tokens | bg-base `#040810` · surface-1 `#08101E` · accent `#6366F1` · success `#22C55E` · danger `#EF4444` · warn `#F59E0B` |

---

## 2. Purpose & Business Logic

**Why this page matters:**

EduForge is an exam preparation platform. The ultimate product promise is: "students who use EduForge improve their exam performance." This page answers the CEO's core question: **is the platform actually delivering measurable learning outcomes?**

Institutions renew subscriptions (or churn) based on whether their students see improvement. If pass rates, rank distributions, and score improvements are trending positively, EduForge has a powerful retention and sales narrative. If declining, there is a product problem.

**Metrics tracked:**
- **Pass Rate** — % of students who score above the exam's passing threshold
- **Score Improvement** — average score in latest attempt vs first attempt (for multi-attempt exams)
- **Rank Distribution** — for competitive exams (JEE/NEET/SSC), where students rank in a simulated percentile
- **Attempt Coverage** — % of enrolled students who have attempted ≥ 1 exam (unused students = value not delivered)
- **YoY Improvement** — are outcomes better this year vs last year?

---

## 3. User Roles & Access

| Role | Can View | Can Act |
|---|---|---|
| CEO | All | Export PDF |
| COO | All | Export PDF |
| Others | No access | Redirect |

---

## 4. Section-wise UI Breakdown

---

### Section 1 — Header & Filters

```
Student Outcomes Analytics     [Domain: All ▾]  [Period: FY 2025–26 ▾]  [Export PDF]
Platform-wide: 28,00,000 enrolled · 19,60,000 active (70.0%) · 1,42,80,000 exams taken
```

- Domain filter: All / SSC-Govt / NEET-Medical / JEE-Engg / AP-TS Boards / Banking / CA-Prof
- Period: Current FY / Last FY / Last 90 days / Custom quarter
- Active = attempted ≥ 1 exam in period

---

### Section 2 — Top-Line Outcome Strip

```
PLATFORM OUTCOMES — FY 2025–26
────────────────────────────────────────────────────────────────────────────
Avg Pass Rate     Score Improvement    Rank (Top 10%)   Attempt Coverage
   71.4%          ▲ +8.2 pts avg       28.4% of active  70.0% enrolled
   ▲ +3.1pp YoY   (1st → latest)                        ▲ +4.2pp YoY
   ✅ Improving   ✅ Significant gain   ✅ Strong         ⚠ 30% unused
```

| Metric | Amber | Red |
|---|---|---|
| Pass Rate | < 60% | < 45% |
| Score Improvement | < 2 pts | Negative delta |
| Attempt Coverage | < 60% | < 40% |

---

### Section 3 — Outcomes by Domain

**Purpose:** Compare student performance across exam categories — identifies where the platform adds most/least value.

```
OUTCOMES BY DOMAIN
────────────────────────────────────────────────────────────────────────────
Domain          Students  Attempted  Pass Rate   Score Improv   YoY Pass%
────────────────┼─────────┼──────────┼───────────┼──────────────┼──────────
SSC/RRB/Govt    9,40,000  6,58,000   74.2%       ▲ +9.4 pts     ▲ +4.1pp
NEET/Medical    5,20,000  4,16,000   68.4%       ▲ +7.8 pts     ▲ +2.8pp
JEE/Engg        2,80,000  1,96,000   62.1%       ▲ +6.2 pts     ▲ +1.8pp
AP/TS Boards    8,60,000  4,30,000   78.4%       ▲ +8.8 pts     ▲ +3.4pp
Banking         1,20,000    84,000   72.8%        ▲ +8.4 pts    ▲ +3.8pp
CA/Prof           80,000    40,000   58.4%       ▲ +5.2 pts     ▲ +1.2pp ⚠
```

- JEE and CA: lower pass rates are expected (harder exams) — contextual note shown: "Industry benchmark: JEE Pass ~55–65%, CA Foundation ~50–60%"
- Click domain row → Domain Outcomes Drawer

---

### Section 4 — Score Distribution Histogram

**Purpose:** For a given domain, how are students distributed by score band? CEO wants to see a right-shift (students moving from lower to higher score bands) as evidence of learning.

```
SSC / RRB / GOVT — Score Distribution Comparison
────────────────────────────────────────────────────────────────────────────
Score Band    First Attempt (Jul–Sep 2025)    Latest Attempt (Jan–Mar 2026)
0–20%         ████░░░░░░░░░░░░░░░░░  18.2%    ██░░░░░░░░░░░░░░░░░░░  8.4%  ▼
20–40%        ████████░░░░░░░░░░░░░  24.1%    ████░░░░░░░░░░░░░░░░░  14.2% ▼
40–60%        ████████████░░░░░░░░░  29.8%    ████████████░░░░░░░░░  28.4%
60–80%        ██████████░░░░░░░░░░░  19.4%    ████████████████░░░░░  31.2% ▲
80–100%       ████░░░░░░░░░░░░░░░░░   8.5%    ████████████░░░░░░░░░  17.8% ▲ 🔥
```

- "Right shift" (mass moving to higher bands) is the success indicator
- Chart.js grouped bar chart; toggle between domains
- "Cohort shown: students who took ≥ 2 exams — sample size: 4,28,000"

---

### Section 5 — Attempt Coverage Analysis

**Purpose:** 30% of enrolled students have never taken an exam — wasted seats and churn risk.

```
ATTEMPT COVERAGE
────────────────────────────────────────────────────────────────────────────
                         Count      %       YoY
Active (≥1 exam)        19,60,000   70.0%   ▲ +4.2pp ✅
Never attempted          8,40,000   30.0%   ▼ -4.2pp ✅
  - Onboarded < 30 days    1,20,000  (new — expected)
  - Onboarded 30–90 days     84,000  (low priority)
  - Onboarded > 90 days    6,36,000  ⚠ AT RISK — students not engaging

TOP INSTITUTIONS WITH LOW COVERAGE (> 90 days enrolled, < 40% attempt rate)
Institution               Enrolled  Attempted  Coverage   Health Score
─────────────────────────┼─────────┼──────────┼──────────┼────────────
Sunrise Coaching Centre  1,200     240        20.0%      62  [View →]
Noble Academy AP          980      186        19.0%      58  [View →]
… (Top 20 shown)
```

- "Never attempted > 90 days": highest churn signal — links to Customer Health page
- COO uses this to prioritise CSM intervention

---

### Section 6 — YoY Trend Chart

```
PASS RATE TREND — Platform-wide (Last 8 Quarters)
────────────────────────────────────────────────────────────────────────────
[Line chart: Chart.js]
  Q1 FY24: 62.1%
  Q2 FY24: 64.4%
  Q3 FY24: 66.2%
  Q4 FY24: 68.3%
  Q1 FY25: 68.8%
  Q2 FY25: 69.4%
  Q3 FY25: 70.2%
  Q4 FY25: 71.4%  ← current

Trend annotation: "Pass rate has improved +9.3pp over 8 quarters — 1.16pp/quarter average"
```

- CEO uses this chart for board presentations — shows consistent platform improvement
- Links to Board Dashboard (page 45) "Use as slide"

---

## 5. Full Page Wireframe

```
╔══════════════════════════════════════════════════════════════════════════════╗
║  Student Outcomes Analytics    [Domain: All ▾]  [FY 2025–26 ▾]  [PDF]      ║
║  28,00,000 enrolled · 19,60,000 active · 1,42,80,000 exams taken            ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  Pass Rate: 71.4% ▲+3.1pp  |  Score Improv: +8.2pts  |  Coverage: 70% ⚠   ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  OUTCOMES BY DOMAIN                   SCORE DISTRIBUTION                    ║
║  SSC: 74.2% pass  ▲+4.1pp YoY         [First Attempt vs Latest]             ║
║  NEET: 68.4% pass ▲+2.8pp YoY         0–40%: ▼ reducing (good)             ║
║  JEE: 62.1% pass  ▲+1.8pp YoY         60–100%: ▲ growing (good)            ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  ATTEMPT COVERAGE: 70% active  30% never attempted                          ║
║  At-risk (>90d no exam): 6,36,000 students  Top 20 institutions shown       ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  PASS RATE TREND (8 Quarters): 62.1% → 71.4%  +9.3pp total                 ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 6. Component Architecture

| Component | File | Props |
|---|---|---|
| `OutcomeStrip` | `components/outcomes/outcome_strip.html` | `pass_rate, pass_rate_yoy, score_improvement, attempt_coverage, coverage_yoy` |
| `OutcomeByDomainRow` | `components/outcomes/domain_row.html` | `domain, students, attempted, pass_rate, score_improvement, yoy_pass_delta` |
| `ScoreDistributionChart` | `components/outcomes/score_dist.html` | `bands (list), first_attempt_pct, latest_attempt_pct, sample_size` |
| `CoverageAnalysis` | `components/outcomes/coverage.html` | `active_count, never_count, at_risk_count, at_risk_institutions` |
| `PassRateTrendChart` | `components/outcomes/trend.html` | `quarters (list of {label, pass_rate})` |

---

## 7. HTMX Architecture

| `?part=` | Target | Trigger |
|---|---|---|
| `summary` | `#outcomes-summary` | load + filter change |
| `domains` | `#outcomes-domains` | load + filter change |
| `score-dist` | `#score-distribution` | load + domain change |
| `coverage` | `#coverage-analysis` | load + filter change |
| `trend` | `#pass-trend` | load |

No polling — data computed nightly.

---

## 8. Backend View & API

```python
class StudentOutcomesView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "portal.view_student_outcomes"

    def get(self, request):
        if request.user.role not in {"ceo","coo","superadmin"}:
            return redirect("exec:dashboard")

        domain = request.GET.get("domain","all")
        period = request.GET.get("period","fy_current")
        cache_key = f"student:outcomes:{domain}:{period}"

        r = get_redis_connection()
        ctx = json.loads(r.get(cache_key) or "{}")
        if not ctx:
            ctx = self._build_outcomes_ctx(domain, period)
            r.setex(cache_key, 3600, json.dumps(ctx))

        if _is_htmx(request):
            part = request.GET.get("part","")
            dispatch = {
                "summary":    "exec/outcomes/partials/summary.html",
                "domains":    "exec/outcomes/partials/domains.html",
                "score-dist": "exec/outcomes/partials/score_dist.html",
                "coverage":   "exec/outcomes/partials/coverage.html",
                "trend":      "exec/outcomes/partials/trend.html",
            }
            if part in dispatch:
                return render(request, dispatch[part], ctx)
        return render(request, "exec/student_outcomes.html", ctx)
```

---

## 9. Database Schema

```python
class OutcomeSnapshot(models.Model):
    """Nightly computed outcomes per domain per fiscal period."""
    domain_slug         = models.CharField(max_length=50)  # "all", "ssc_rrb", etc.
    period_key          = models.CharField(max_length=20)  # "fy_2025_26", "q4_fy2526"
    enrolled_count      = models.IntegerField()
    attempted_count     = models.IntegerField()
    pass_rate           = models.FloatField()
    pass_rate_yoy_delta = models.FloatField(null=True)
    avg_score_first     = models.FloatField()
    avg_score_latest    = models.FloatField()
    score_improvement   = models.FloatField()    # latest - first
    top_10_pct          = models.FloatField()    # % scoring in top decile
    computed_at         = models.DateTimeField()

    class Meta:
        unique_together = ("domain_slug","period_key","computed_at")
        indexes = [models.Index(fields=["domain_slug","period_key"])]


class ScoreBandSnapshot(models.Model):
    """Score distribution by band for first vs latest attempt."""
    domain_slug     = models.CharField(max_length=50)
    period_key      = models.CharField(max_length=20)
    band_label      = models.CharField(max_length=20)   # "0-20", "20-40", etc.
    first_pct       = models.FloatField()
    latest_pct      = models.FloatField()
    computed_at     = models.DateTimeField()

    class Meta:
        unique_together = ("domain_slug","period_key","band_label","computed_at")


class AtRiskStudentAgg(models.Model):
    """Aggregated count of never-attempted students per institution."""
    institution     = models.ForeignKey("Institution", on_delete=models.CASCADE)
    period_key      = models.CharField(max_length=20)
    enrolled        = models.IntegerField()
    attempted       = models.IntegerField()
    coverage_pct    = models.FloatField()
    days_since_onboard = models.IntegerField()
    computed_at     = models.DateTimeField()

    class Meta:
        indexes = [models.Index(fields=["coverage_pct","days_since_onboard"])]
```

**Celery task:**
```python
@shared_task
def compute_student_outcomes():
    """Nightly at 02:30 IST. Aggregates exam attempt data per domain and period."""
    for period_key, date_range in OUTCOME_PERIODS.items():
        for domain_slug in ["all"] + [d[0] for d in DOMAIN_CHOICES]:
            snapshot = _compute_domain_outcome(domain_slug, period_key, date_range)
            OutcomeSnapshot.objects.update_or_create(
                domain_slug=domain_slug, period_key=period_key,
                computed_at=today_midnight(),
                defaults=snapshot,
            )
    # Invalidate all cached outcomes
    r = get_redis_connection()
    for key in r.scan_iter("student:outcomes:*"):
        r.delete(key)
```

---

## 10. Security Considerations

- Outcome data is platform-wide aggregate — no individual student records visible
- Institution-level attempt coverage table (Section 5): only shows institution name + aggregate count, not student identities
- DPDP Act 2023: pass/fail rates do not expose personal data
- Export PDF: logged in `AuditLog`

---

## 11. Edge Cases

| State | Behaviour |
|---|---|
| New domain with < 100 students | Pass rate shown with "Low sample size" tooltip — not statistically significant |
| YoY data unavailable (platform < 1 year old for a domain) | YoY column shows "—" |
| Score improvement negative for a domain | Red badge + tooltip "Avg score declined — investigate exam difficulty calibration" |
| Institution onboarded today | Excluded from "at-risk" analysis (grace period: 90 days from onboarding) |

---

## 12. Performance & Scaling

- 28M enrolled students, 142M exams: full aggregation runs nightly — not on-demand
- Snapshot model pattern: heavy compute done in Celery, page reads pre-computed rows
- Score distribution: 5 bands × N domains × M periods — trivial data volume
- Redis TTL 3600s — hourly refresh acceptable for strategic metrics
- At-risk institution table: limit 20 rows on page; full list available via export

---

*Last updated: 2026-03-20*
