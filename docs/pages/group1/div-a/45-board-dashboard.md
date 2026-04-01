# 45 — Board / Investor Dashboard

---

## 1. Page Metadata

| Field | Value |
|---|---|
| Page title | Board / Investor Dashboard |
| Route | `/exec/board-dashboard/` |
| Django view | `BoardDashboardView` |
| Template | `exec/board_dashboard.html` |
| Priority | **P3** |
| Nav group | Strategic |
| Required roles | `ceo` · `cfo` · `superadmin` |
| All others | Denied — redirect with "Restricted to CEO and CFO" |
| HTMX poll | None (static board-period data) |
| Cache | Redis TTL 3600s |
| Theme tokens | bg-base `#040810` · surface-1 `#08101E` · accent `#6366F1` · success `#22C55E` · danger `#EF4444` |

---

## 2. Purpose & Business Logic

**The board deck problem:**

Every quarter, the CEO and CFO prepare a board/investor update. They currently pull numbers from 6 different systems (billing, support, platform health, mobile analytics, HR, financial software) and paste them into a Google Slides deck. This page consolidates all board-relevant KPIs into one view and enables one-click export to PDF or PPTX.

**Standard SaaS board metrics included:**
- ARR, ARR YoY%, MRR
- NRR, GRR (net/gross revenue retention)
- ARPU by segment
- Gross Margin %, EBITDA Margin %
- Customer Count, Churn Count, Net New
- CAC (Customer Acquisition Cost) by channel
- LTV (Lifetime Value), LTV:CAC ratio
- Payback Period (months)
- DAU/MAU (mobile)
- Headcount, Revenue per Employee

---

## 3. User Roles & Access

| Role | Can View | Can Act |
|---|---|---|
| CEO | All | Export PDF, Export PPTX, annotate quarters |
| CFO | All | Export PDF, Export PPTX |
| All others | No access | Redirect |

---

## 4. Section-wise UI Breakdown

---

### Section 1 — Period Selector & Export

```
Board / Investor Dashboard          [Q4 FY 2025–26 ▾]  [Export PDF]  [Export PPTX]
Last updated: 21 Mar 2026 by CFO
```

- Quarter selector: last 8 quarters available
- Export PDF: formatted A4 landscape, EduForge branding, page breaks between sections
- Export PPTX: 12-slide deck template (python-pptx), one metric per slide with YoY context
- "Last updated" line: shows who last entered manual data (e.g., CFO entered OpEx data for Q4)

---

### Section 2 — Top-Line KPI Grid

```
QUARTERLY SNAPSHOT — Q4 FY 2025–26
────────────────────────────────────────────────────────────────────────────
ARR             ₹60.0 Cr      ▲ +24% YoY    MRR: ₹5.0 Cr
NRR             112.4%         ▲ +2.1pp      ✅ Healthy expansion
GRR              96.2%         ▲ +0.8pp      ✅ Low churn
Gross Margin     84.2%         ▼ -0.4pp      ✅ Above 80% target
EBITDA Margin    44.6%         ▲ +2.0pp      ✅ Improving
Customers        2,050          ▲ +18% YoY   Net new: +312
Churn             38            ▼ -12 YoY    Churn rate: 1.9%
```

Each metric: large value + YoY delta + trend arrow + benchmark comparison.

---

### Section 3 — ARR Bridge

**Purpose:** Shows how ARR moved from start of quarter to end — the classic investor waterfall.

```
ARR BRIDGE — Q4 FY 2025–26                               (₹ Cr)
─────────────────────────────────────────────────────────────────────────────
Starting ARR (1 Jan)     ₹54.2 Cr
  + New Business         ₹ 4.8 Cr  (74 new institutions)
  + Expansion            ₹ 2.4 Cr  (existing inst. upgrading plans)
  - Contraction          ₹-0.8 Cr  (downgrade or seat reduction)
  - Churn                ₹-0.6 Cr  (38 institutions cancelled)
                        ─────────────
Ending ARR (31 Mar)      ₹60.0 Cr  (+10.7%)
```

Waterfall chart (Chart.js or custom SVG) — visual representation of the bridge.

---

### Section 4 — Unit Economics

```
UNIT ECONOMICS — LTM (Last Twelve Months)
────────────────────────────────────────────────────────────────────────────
                Schools      Colleges     Coaching     Overall
ARPU           ₹18,200      ₹15,500      ₹2,48,000    ₹29,268
CAC            ₹12,400       ₹9,800      ₹84,000      ₹18,200
LTV            ₹54,600      ₹46,500     ₹7,44,000    ₹87,800
LTV:CAC          4.4×         4.7×         8.9×         4.8×
Payback          8.1m         7.6m         4.1m         7.4m
```

- LTV = ARPU × Gross Margin × Average Contract Length
- CAC = Sales + Marketing spend / New customers in period
- All manual-entered by CFO per quarter in `BoardDataEntry` model

---

### Section 5 — Cohort Retention Heatmap

**Purpose:** Classic SaaS investor chart — for each cohort (month they signed), what % are still paying 12/24/36 months later?

```
COHORT RETENTION
                M1   M3   M6   M12  M18  M24
Jan 2024        100% 98%  96%  94%  91%  88%
Apr 2024        100% 97%  95%  92%   —    —
Jul 2024        100% 98%  96%   —    —    —
Oct 2024        100% 99%   —    —    —    —
Jan 2025        100%  —    —    —    —    —
```

Heatmap: green (> 95%) → yellow (90–95%) → orange (85–90%) → red (< 85%). Classic investor table.

---

### Section 6 — Growth & Efficiency

```
GROWTH & EFFICIENCY
────────────────────────────────────────────────────────────────────────────
ARR per Employee    ₹73.2 L    (60 employees · ₹60 Cr ARR)
Magic Number        1.82       (New ARR / Sales+Marketing Spend) — ✅ > 1.5
Rule of 40          66.6%      (ARR Growth 24% + EBITDA Margin 42.6%) — ✅ > 40%
```

---

## 5. Full Page Wireframe

```
╔══════════════════════════════════════════════════════════════════════════════╗
║  Board / Investor Dashboard         [Q4 FY 2025–26 ▾] [Export PDF] [PPTX]  ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  ARR: ₹60.0 Cr ▲+24%  NRR: 112.4%  GRR: 96.2%  GM: 84.2%  EBITDA: 44.6%  ║
║  Customers: 2,050 ▲+18%  Churn: 38 ▼-12  Net New: 312                      ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  ARR BRIDGE (Waterfall)             UNIT ECONOMICS                          ║
║  Start ₹54.2 +New ₹4.8             Schools: LTV:CAC 4.4×  PBP 8.1m        ║
║  +Exp ₹2.4 -Cont ₹0.8              Coaching: LTV:CAC 8.9× PBP 4.1m        ║
║  -Churn ₹0.6 = End ₹60.0           Overall: LTV:CAC 4.8×  PBP 7.4m        ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  COHORT RETENTION HEATMAP           GROWTH & EFFICIENCY                     ║
║  Jan'24: 100% 98% 96% 94% 91% 88%   Rule of 40: 66.6% ✅                   ║
║  Apr'24: 100% 97% 95% 92%  —   —    Magic Number: 1.82 ✅                   ║
║  Jul'24: 100% 98% 96%  —   —   —    ARR/Employee: ₹73.2L                   ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 6. Component Architecture

| Component | File | Props |
|---|---|---|
| `BoardKPIStrip` | `components/board/kpi_strip.html` | `kpis (list of {label, value, yoy_delta, benchmark, status})` |
| `ARRWaterfallChart` | `components/board/arr_waterfall.html` | `starting_arr, new_arr, expansion, contraction, churn, ending_arr` |
| `UnitEconomicsTable` | `components/board/unit_economics.html` | `segments (list of {name, arpu, cac, ltv, ltv_cac, payback_months})` |
| `CohortHeatmap` | `components/board/cohort_heatmap.html` | `cohorts (list of {month, retention_by_period})` |
| `GrowthEfficiency` | `components/board/growth_efficiency.html` | `rule_of_40, magic_number, arr_per_employee` |

---

## 7. HTMX Architecture

| `?part=` | Target | Trigger |
|---|---|---|
| `kpis` | `#board-kpis` | load + quarter change |
| `arr-bridge` | `#arr-bridge` | load + quarter change |
| `unit-economics` | `#unit-economics` | load + quarter change |
| `cohort` | `#cohort-heatmap` | load |
| `growth` | `#growth-efficiency` | load + quarter change |

No polling — all data is quarterly, static once entered.

---

## 8. Backend View & API

```python
class BoardDashboardView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "portal.view_board_dashboard"

    def get(self, request):
        if request.user.role not in {"ceo","cfo","superadmin"}:
            messages.warning(request, "Board dashboard restricted to CEO and CFO.")
            return redirect("exec:dashboard")

        quarter = request.GET.get("quarter", current_quarter())
        r = get_redis_connection()
        cache_key = f"board:data:{quarter}"
        ctx = json.loads(r.get(cache_key) or "{}")
        if not ctx:
            ctx = self._build_board_data(quarter)
            r.setex(cache_key, 3600, json.dumps(ctx))

        if _is_htmx(request):
            part = request.GET.get("part","")
            dispatch = {
                "kpis":           "exec/board/partials/kpis.html",
                "arr-bridge":     "exec/board/partials/arr_bridge.html",
                "unit-economics": "exec/board/partials/unit_economics.html",
                "cohort":         "exec/board/partials/cohort.html",
                "growth":         "exec/board/partials/growth.html",
            }
            if part in dispatch:
                return render(request, dispatch[part], ctx)
        return render(request, "exec/board_dashboard.html", ctx)
```

---

## 9. Database Schema

```python
class BoardDataEntry(models.Model):
    """Manual quarterly data entry by CFO for board metrics."""
    quarter         = models.CharField(max_length=10, unique=True)  # "2025-Q4"
    arr             = models.DecimalField(max_digits=14, decimal_places=2)
    mrr             = models.DecimalField(max_digits=12, decimal_places=2)
    nrr             = models.DecimalField(max_digits=6, decimal_places=2)
    grr             = models.DecimalField(max_digits=6, decimal_places=2)
    gross_margin    = models.DecimalField(max_digits=5, decimal_places=2)
    ebitda_margin   = models.DecimalField(max_digits=5, decimal_places=2)
    new_arr         = models.DecimalField(max_digits=12, decimal_places=2)
    expansion_arr   = models.DecimalField(max_digits=12, decimal_places=2)
    contraction_arr = models.DecimalField(max_digits=12, decimal_places=2)
    churn_arr       = models.DecimalField(max_digits=12, decimal_places=2)
    cac_schools     = models.DecimalField(max_digits=10, decimal_places=2)
    cac_colleges    = models.DecimalField(max_digits=10, decimal_places=2)
    cac_coaching    = models.DecimalField(max_digits=10, decimal_places=2)
    headcount       = models.IntegerField()
    entered_by      = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    entered_at      = models.DateTimeField(auto_now=True)
```

---

## 10. Security Considerations

- Most sensitive page in the platform — investor-grade financial data
- Access logs: every page view by CEO/CFO is logged in `AuditLog`
- PDF/PPTX export: email notification to CFO on every export (even by CEO)
- Cache uses opaque key `board:data:{quarter}` — no financial data in Redis key name
- Export rate-limited: 3 exports/day per user

---

## 11. Edge Cases

| State | Behaviour |
|---|---|
| Quarter data not yet entered | "Q4 FY 2025-26 data not yet entered. CFO can enter data [here →]" with link to data entry form. |
| ARR bridge doesn't sum to ending ARR | Validation error at data entry: "Starting ARR + movements do not equal ending ARR. Check figures." |
| Export during data entry | Export locked if any quarterly field is 0 (unintentional). Warning: "Some metrics are zero — data may be incomplete." |

---

## 12. Performance & Scaling

- Trivial data volume — 8 quarters × ~40 metrics = 320 data points
- Cached 1 hour — quarterly data does not change frequently
- PDF/PPTX export: Celery async task if > 5 seconds. User gets "Export ready — click to download."

---

*Last updated: 2026-03-20*
