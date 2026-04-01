# 39 — P&L Overview

---

## 1. Page Metadata

| Field | Value |
|---|---|
| Page title | P&L Overview |
| Route | `/exec/pnl/` |
| Django view | `PLOverviewView` |
| Template | `exec/pnl_overview.html` |
| Priority | **P2** |
| Nav group | Financial |
| Required roles | `cfo` · `finance_manager` · `ceo` · `superadmin` |
| COO / CTO | Denied |
| HTMX poll | None (static financial data — refreshed monthly) |
| Cache | Redis TTL 3600s (1 hour) |
| Theme tokens | bg-base `#040810` · surface-1 `#08101E` · accent `#6366F1` · success `#22C55E` · danger `#EF4444` · warn `#F59E0B` |

---

## 2. Purpose & Business Logic

**Investor-grade P&L for board and internal review.**

The Financial Overview (page 08) shows revenue. This page shows profitability. Key difference: this page includes COGS, OpEx, gross margin, EBITDA, and burn rate — the full income statement that the CFO presents to the board or investors.

**P&L structure for EduForge:**

```
Revenue
  ├─ Subscription Revenue (MRR × 12 = ARR)
  ├─ Setup / Onboarding Fees (one-time)
  └─ Add-on / Usage Fees

COGS (Cost of Goods Sold)
  ├─ AWS Infrastructure (Lambda, RDS, S3, CloudFront)
  ├─ SMS/WhatsApp Gateway (Exotel / Kaleyra)
  ├─ Razorpay Processing Fees
  └─ AI API Costs (MCQ generation)

Gross Profit = Revenue − COGS
Gross Margin % = Gross Profit / Revenue

OpEx (Operating Expenses)
  ├─ Salaries (81 headcount across phases)
  ├─ BGV Vendor Fees
  ├─ Office / Admin
  ├─ Marketing (Google/Meta Ads)
  └─ Legal / Compliance

EBITDA = Gross Profit − OpEx
Net Revenue Retention (NRR) = (Starting ARR + Expansion − Churn − Contraction) / Starting ARR
Gross Revenue Retention (GRR) = (Starting ARR − Churn − Contraction) / Starting ARR
```

---

## 3. User Roles & Access

| Role | Can View | Can Act |
|---|---|---|
| CEO | All sections | Export PDF/PPTX |
| CFO | All sections | Export, annotate quarters |
| Finance Manager | All sections | Export CSV |
| COO / CTO | No access | Redirect |

---

## 4. Section-wise UI Breakdown

---

### Section 1 — Page Header & Period Selector

**UI elements:**
```
P&L Overview                    [FY 2025–26 ▾]  [View: Quarterly ●  Monthly]
                                                  [Export PDF]  [Export PPTX]
```

- FY selector: last 3 financial years
- View toggle: Quarterly (default for board view) / Monthly (for CFO operational view)
- Export PDF: WeasyPrint formatted for board presentation (landscape, EduForge branding)
- Export PPTX: python-pptx formatted slide deck (CEO/CFO only)

---

### Section 2 — P&L Summary Table

**Purpose:** The full income statement in one table — structured exactly as a board P&L.

**UI elements:**
```
P&L SUMMARY — FY 2025–26                              (₹ Lakhs)
─────────────────────────────────────────────────────────────────────────────
                          Q1       Q2       Q3       Q4     FY Total
─────────────────────────────────────────────────────────────────────────────
REVENUE
  Subscription Revenue   820.4    964.2   1,082.6  1,240.8   4,108.0
  Setup / Onboarding      48.2     36.4     42.8     38.6     166.0
  Add-on / Usage          12.4     18.8     22.4     28.2      81.8
  ─────────────────────────────────────────────────────────────────────
  Total Revenue          881.0  1,019.4   1,147.8  1,307.6   4,355.8

COGS
  AWS Infrastructure      88.2    102.4    118.6    134.8     444.0
  SMS/WhatsApp Gateway    22.4     26.8     28.2     32.4     109.8
  Razorpay Fees           16.4     19.2     21.8     24.6      82.0
  AI API Costs             8.2     12.4     14.8     18.2      53.6
  ─────────────────────────────────────────────────────────────────────
  Total COGS             135.2    160.8    183.4    210.0     689.4

GROSS PROFIT             745.8    858.6    964.4  1,097.6   3,666.4
GROSS MARGIN %           84.7%    84.2%    84.0%    83.9%     84.2%

OPEX
  Salaries               320.4    348.2    380.6    412.8   1,462.0
  BGV Vendor Fees          8.4      8.4      8.4      8.4      33.6
  Office / Admin           18.2     18.2     18.2     18.2      72.8
  Marketing               42.4     48.6     54.2     62.4     207.6
  Legal / Compliance       12.4     12.4     12.4     12.4      49.6
  ─────────────────────────────────────────────────────────────────────
  Total OpEx             401.8    435.8    473.8    514.2   1,825.6

EBITDA                   344.0    422.8    490.6    583.4   1,840.8
EBITDA MARGIN %          39.0%    41.5%    42.7%    44.6%     42.3%
─────────────────────────────────────────────────────────────────────────────
```

- Row groupings: Revenue / COGS / Gross Profit / OpEx / EBITDA — each group collapsible (click group header)
- Gross Margin % and EBITDA Margin % rows: `text-[#6366F1] font-bold` — highlighted as key KPIs
- Negative values (if any quarter is loss-making): `text-red-400`
- All figures in ₹ Lakhs (standard Indian board reporting)
- YoY comparison: toggle `[vs FY 2024–25]` adds delta columns

**HTMX:** `id="pnl-table"` `hx-trigger="load"` `hx-swap="innerHTML"` — static, no polling.

---

### Section 3 — Gross Margin Trend Chart

**Purpose:** Visual trend of gross margin % over quarters. Target: maintain > 80%.

**UI elements:**
- Chart.js Bar + Line combo: bars = Gross Profit (₹L), line = Gross Margin % (secondary Y-axis)
- X-axis: 8 quarters (last 2 FYs)
- Target margin line: dashed horizontal at 80% `rgba(99,102,241,0.5)`

---

### Section 4 — NRR / GRR Tracker

**Purpose:** The investor's most important SaaS metrics. NRR > 100% means existing customers are expanding (healthy). GRR < 90% means too much churn.

**UI elements:**
```
NET REVENUE RETENTION (NRR)              GROSS REVENUE RETENTION (GRR)
Q1: 108.4%  Q2: 112.2%  Q3: 110.8%      Q1: 94.2%  Q2: 95.8%  Q3: 96.2%
[Trend chart]                             [Trend chart]
Target: > 110%  ✅                        Target: > 95%  ✅
```

- NRR formula: `(Start ARR + Expansion − Contraction − Churn) / Start ARR × 100`
- GRR formula: `(Start ARR − Contraction − Churn) / Start ARR × 100`
- Data sourced from `ARRMovement` model (monthly cohort tracking)

---

### Section 5 — ARPU by Segment

```
ARPU BY SEGMENT — FY 2025–26
─────────────────────────────────────────────────────────────────────────────
Segment    Institutions  Total ARR    ARPU        YoY change
Schools        1,000     ₹18.2 Cr     ₹18,200     ▲ +12%
Colleges         800     ₹12.4 Cr     ₹15,500     ▲ +8%
Coaching         100     ₹24.8 Cr    ₹2,48,000    ▲ +18%
Groups           150      ₹4.6 Cr     ₹30,667     ▲ +22%
─────────────────────────────────────────────────────────────────────────────
Total          2,050     ₹60.0 Cr     ₹29,268     ▲ +14%
```

---

## 5. Full Page Wireframe

```
╔══════════════════════════════════════════════════════════════════════════════╗
║  P&L Overview                  [FY 2025–26 ▾] [Quarterly ●] [Export PDF]   ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  P&L SUMMARY TABLE (₹ Lakhs)                                                ║
║                        Q1      Q2      Q3      Q4    FY Total                ║
║  Total Revenue       881.0  1019.4  1147.8  1307.6   4355.8                 ║
║  Total COGS          135.2   160.8   183.4   210.0    689.4                 ║
║  Gross Profit        745.8   858.6   964.4  1097.6   3666.4                 ║
║  Gross Margin %      84.7%   84.2%   84.0%   83.9%    84.2%                 ║
║  Total OpEx          401.8   435.8   473.8   514.2   1825.6                 ║
║  EBITDA              344.0   422.8   490.6   583.4   1840.8                 ║
║  EBITDA Margin %      39.0%   41.5%   42.7%   44.6%   42.3%                 ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  GROSS MARGIN TREND (8 quarters)    NRR / GRR                               ║
║  [Bar+Line combo chart]             NRR: 110.8% ✅  GRR: 96.2% ✅           ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  ARPU BY SEGMENT                                                            ║
║  Schools: ₹18,200  Colleges: ₹15,500  Coaching: ₹2,48,000  Groups: ₹30,667 ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 6. Component Architecture

| Component | File | Props |
|---|---|---|
| `PLTable` | `components/pnl/pl_table.html` | `periods, rows, view (quarterly/monthly), show_yoy` |
| `PLRow` | `components/pnl/pl_row.html` | `label, values, is_subtotal, is_pct, indent_level` |
| `MarginTrendChart` | `components/pnl/margin_trend.html` | `quarters (list of {label, gross_profit, margin_pct})` |
| `NRRGRRPanel` | `components/pnl/nrr_grr.html` | `quarters (list of {label, nrr, grr})` |
| `ARPUTable` | `components/pnl/arpu_table.html` | `segments (list of {name, count, arr, arpu, yoy_pct})` |

---

## 7. HTMX Architecture

| `?part=` | Target | Poll | Trigger |
|---|---|---|---|
| `pnl-table` | `#pnl-table` | None | load + FY/view change |
| `margin-trend` | `#margin-trend` | None | load |
| `nrr-grr` | `#nrr-grr` | None | load |
| `arpu` | `#arpu-table` | None | load + FY change |

---

## 8. Backend View & API

```python
class PLOverviewView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "portal.view_pnl"

    def get(self, request):
        allowed = {"cfo","finance_manager","ceo","superadmin"}
        if request.user.role not in allowed:
            return redirect("exec:dashboard")

        fy   = request.GET.get("fy", current_fy())
        view = request.GET.get("view", "quarterly")

        if _is_htmx(request):
            part = request.GET.get("part","")
            ctx  = self._build_pnl_context(fy, view)
            dispatch = {
                "pnl-table":    "exec/pnl/partials/pl_table.html",
                "margin-trend": "exec/pnl/partials/margin_trend.html",
                "nrr-grr":      "exec/pnl/partials/nrr_grr.html",
                "arpu":         "exec/pnl/partials/arpu.html",
            }
            if part in dispatch:
                return render(request, dispatch[part], ctx)
        ctx = self._build_pnl_context(fy, view)
        return render(request, "exec/pnl_overview.html", ctx)

    def _build_pnl_context(self, fy, view):
        r = get_redis_connection()
        cache_key = f"pnl:summary:{fy}:{view}"
        cached = r.get(cache_key)
        if cached:
            return json.loads(cached)
        data = self._compute_pnl(fy, view)
        r.setex(cache_key, 3600, json.dumps(data))
        return data
```

---

## 9. Database Schema

```python
class PLEntry(models.Model):
    """Manual-entry P&L line items — entered by Finance Manager monthly."""
    fy           = models.CharField(max_length=7)   # "2025-26"
    period       = models.CharField(max_length=7)   # "2026-01" (month) or "2025-Q1"
    category     = models.CharField(max_length=30)  # revenue/cogs/opex
    line_item    = models.CharField(max_length=100) # "AWS Infrastructure"
    amount       = models.DecimalField(max_digits=14, decimal_places=2)
    entered_by   = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    entered_at   = models.DateTimeField(auto_now_add=True)
    notes        = models.TextField(blank=True)

    class Meta:
        unique_together = ("fy", "period", "line_item")


class ARRMovement(models.Model):
    """Monthly ARR cohort tracking for NRR/GRR computation."""
    period         = models.CharField(max_length=7, unique=True)
    starting_arr   = models.DecimalField(max_digits=14, decimal_places=2)
    expansion_arr  = models.DecimalField(max_digits=14, decimal_places=2)
    contraction_arr= models.DecimalField(max_digits=14, decimal_places=2)
    churn_arr      = models.DecimalField(max_digits=14, decimal_places=2)
    ending_arr     = models.DecimalField(max_digits=14, decimal_places=2)
    nrr            = models.DecimalField(max_digits=6, decimal_places=2)
    grr            = models.DecimalField(max_digits=6, decimal_places=2)
```

---

## 10. Validation Rules

| Action | Validation |
|---|---|
| Export PDF | CFO / CEO / Finance Manager only. Logged in AuditLog. |
| Export PPTX | CEO / CFO only. Rate-limited: 5/day. |
| P&L data entry (Finance Manager) | Amount required, positive. Period must be valid. Line item must be from approved list. |

---

## 11. Security Considerations

- P&L data is investor-sensitive — any export logged in `AuditLog` with actor + timestamp + format
- P&L figures never exposed via API to non-finance roles. View-level redirect enforced.
- PDF/PPTX contain confidential financial data — export limited to 5/day with email notification to CFO on each export ("Finance Manager Priya exported P&L PDF for FY 2025-26")

---

## 12. Edge Cases

| State | Behaviour |
|---|---|
| COGS data not entered for a period | Period shows "—" for COGS lines with amber note "COGS not entered for Q3 — contact Finance Manager" |
| Revenue from subscription API differs from manual P&L | Cross-check warning: "Subscription revenue in P&L (₹1,082.6L) differs from billing system (₹1,081.2L) by ₹1.4L. [Reconcile →]" |
| EBITDA negative (loss quarter) | EBITDA row shows red value. EBITDA Margin % shows negative in red. CEO notified via email on month-close. |

---

## 13. Performance & Scaling

- P&L computations are expensive (cross-joining revenue, COGS, OpEx). Cached 1 hour in Redis — acceptable for financial data that changes at month-end.
- Quarterly aggregation at most 12 quarters × ~50 line items = trivial data volume.
- PDF/PPTX export: Celery async task if > 5 seconds. User gets "Generating export — will email when ready."

---

*Last updated: 2026-03-20*
