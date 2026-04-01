# div-a-08 — Financial Overview

## 1. Platform Scale Reference

| Dimension | Value |
|---|---|
| Total institutions | 2,050 |
| Annual Recurring Revenue (ARR) | ₹XX Cr (coaching: ₹15 Cr largest segment) |
| Monthly invoices generated | ~2,050 |
| Annual invoices | ~24,600 |
| Avg invoice amount | ₹5K–₹2L (plan-dependent) |
| Payment gateway | Razorpay |
| Overdue invoices (typical) | ~3–5% of monthly invoices |
| Tax: GST rate | 18% on all plans |
| Currency | INR (₹) only |
| Decimal precision | All financial values: `Decimal(28,2)` — NEVER float |

**What this page IS:** Financial Overview is a **revenue dashboard** — MRR/ARR trajectory, cash collections, overdue exposure, churn impact on revenue, and plan mix. It does NOT include COGS, gross margin, OpEx, or EBITDA.

**What it is NOT:** It is not a P&L. For a full investor-grade P&L with Gross Margin, EBITDA and burn rate, use [P&L Overview → `/exec/pnl/`](39-pnl-overview.md). For Razorpay settlement reconciliation, use [Razorpay Settlement Tracker → `/exec/settlements/`](33-razorpay-settlements.md).

Every rupee must be exact (Decimal, not float).

---

## 2. Page Metadata

| Field | Value |
|---|---|
| Page title | Financial Overview |
| Route | `/exec/financial-overview/` |
| Django view | `FinancialOverviewView` |
| Template | `exec/financial_overview.html` |
| Priority | P1 |
| Nav group | Finance |
| Required role | `exec`, `superadmin`, `finance` |
| 2FA required | No (read-only); Yes for manual invoice actions |
| HTMX poll | Revenue KPI: every 2 min |
| Cache | All aggregates Redis TTL 120s |

---

## 3. Wireframe

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ HEADER: Financial Overview                [Export P&L] [Date Range ▾]       │
├────────┬────────┬────────┬────────┬────────┬────────┬────────────────────── ┤
│  MRR   │  ARR   │ New MRR│ Churn  │ Net    │ Overdue│  Collections          │
│        │        │ (30d)  │ MRR    │ Rev    │ Bal.   │  Rate                 │
│ ₹42.8L │ ₹5.1Cr │ ₹3.2L  │ -₹1.1L │ ₹2.1L  │ ₹8.4L  │  96.2%               │
├────────┴────────┴────────┴────────┴────────┴────────┴────────────────────── ┤
│ TABS: [Revenue Trend] [MRR Movement] [Plan Mix] [Collections] [Forecast]    │
├──────────────────────────────────────────────────────────────────────────────┤
│ [Institution Type ▾] [Plan ▾] [State ▾] [Period ▾]                         │
├──────────────────────────────────────────────────────────────────────────────┤
│ TAB: REVENUE TREND                                                           │
│ ┌──────────────────────────────────────────────────────────────────────────┐ │
│ │  MRR Trend Line (last 24 months) + ARR secondary axis                   │ │
│ └──────────────────────────────────────────────────────────────────────────┘ │
│ ┌─────────────────────────┐ ┌────────────────────────────────────────────┐  │
│ │ Revenue by Type (pie)   │ │ Top 10 Revenue Institutions (bar + table)  │  │
│ └─────────────────────────┘ └────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Sections — Deep Specification

### 4.1 KPI Strip

**Container:** `flex gap-4 p-4` · 7 cards · poll every 2 min (pause guard on drawer/modal)
**All financial values:** `Decimal(28,2)` · formatted as `₹XX.X L` (lakhs) or `₹XX Cr` (crores)

| # | Card | Format | Delta | Alert |
|---|---|---|---|---|
| 1 | MRR | `₹42.8 L` | MoM delta green/red | — |
| 2 | ARR | `₹5.1 Cr` | YoY delta | — |
| 3 | New MRR (30d) | `+₹3.2 L` | vs prev 30d | — |
| 4 | Churned MRR (30d) | `-₹1.1 L` | vs prev 30d | > 5% of MRR = red |
| 5 | Net New MRR | `+₹2.1 L` | New − Churned | < 0 = red |
| 6 | Overdue Balance | `₹8.4 L` | vs last month | > ₹20 L = red |
| 7 | Collections Rate | `96.2%` | vs last month | < 90% = red |

**Delta reverse logic:** Churned MRR: increasing = bad (red) · Collections Rate: decreasing = bad (red)

**Amendment — Settlement Status Row (below KPI strip):**

```
SETTLEMENT STATUS  ·  Last Razorpay settlement: 14h ago  ·  ₹4.2L pending  [View Settlements →]
```

- One line, `bg-[#0D1B2E] border-t border-[#1E2D4A] px-4 py-2 text-sm text-[#8892A4]`
- "Last Razorpay settlement: {X}h ago" — sourced from `RazorpaySettlement.settled_at` (latest record)
- "₹4.2L pending" — sum of `RazorpaySettlement` records with `status=pending`
- `[View Settlements →]` link → `/exec/settlements/` (page 33)
- If no settlement in > 48h: amber text — "Last Razorpay settlement: 2d ago ⚠"
- If pending amount > ₹20L: amber text — "₹22.4L pending ⚠"

**Amendment — Page header correction:**
```
HEADER: Financial Overview (Revenue)          [Export Revenue Report] [View Full P&L →]
```
- "Export Revenue Report" replaces "Export P&L" (was misleading)
- "[View Full P&L →]" button: `text-[#6366F1] text-sm underline` → links to `/exec/pnl/`
- Tooltip on link: "P&L includes COGS, Gross Margin, and EBITDA. This page shows revenue only."

---

### 4.2 Filter Bar

`id="finance-filters"` · `flex flex-wrap gap-3 p-4 border-b border-[#1E2D4A]`

| Filter | Type | Options |
|---|---|---|
| Institution Type | Multi-select | All / School / College / Coaching / Group |
| Plan | Multi-select | Starter / Standard / Professional / Enterprise |
| State | Searchable multi-select | 28 states |
| Period | Dropdown + custom date range | Last 3M / 6M / 12M / 24M / Custom |

All filters: `hx-get="?part={active_tab}"` on change · `hx-include="#finance-filters"`

---

### 4.3 Tab: Revenue Trend

`id="tab-revenue"` · `hx-get="?part=revenue_trend"`

#### 4.3.1 MRR / ARR Trend Chart

**Chart:** Multi-line · Chart.js 4.4.2 · Canvas height 280px
**Canvas id:** `mrr-trend-chart`
**Destroy guard:** `window._charts?.mrrTrend?.destroy()`

**Series:**
| Series | Colour | Y-axis | Style |
|---|---|---|---|
| MRR | `#6366F1` | left (₹ L) | solid line fill below |
| ARR | `#22D3EE` | right (₹ Cr) | dashed `borderDash:[4,4]` |
| Target MRR | `#10B981` | left | dotted `borderDash:[2,6]` thin |

**Config:**
```js
plugins: {
  tooltip: {
    callbacks: {
      label: (ctx) => `₹${formatLakhs(ctx.parsed.y)} L`
    }
  },
  annotation: {
    annotations: {
      targetLine: { type: 'line', yMin: TARGET_MRR, yMax: TARGET_MRR,
                    borderColor: '#10B981', borderDash: [2,6], label: { content: 'Target' } }
    }
  }
}
```

**Zoom:** mouse-wheel zoom on X-axis (Chart.js zoom plugin)
**Crosshair:** vertical line following mouse cursor

#### 4.3.2 Revenue by Institution Type (Pie/Donut)

**Chart:** Doughnut · Canvas height 200px
**Segments:**
- Coaching: `#F59E0B`
- Schools: `#6366F1`
- Colleges: `#22D3EE`
- Groups: `#10B981`
**Center text:** Total ARR in Crores
**Click segment:** filters Revenue table + all other charts to that type
**Legend:** right of chart · each item shows: type + ARR + % of total

#### 4.3.3 Top 10 Institutions by Revenue (bar + table)

**Chart:** Horizontal bar · sorted by ARR desc · Canvas height 240px
**Bar colour:** `#6366F1`
**Click bar:** opens Institution Revenue Drawer (same as div-a-09)

**Below chart — summary table:**
| Institution | Type | Plan | MRR | ARR | YoY Growth |
|---|---|---|---|---|---|
| ABC Coaching | Coaching | Enterprise | ₹4.2L | ₹50.4L | +18% |

---

### 4.4 Tab: MRR Movement (Waterfall)

`id="tab-mrr"` · `hx-get="?part=mrr_movement"`

#### 4.4.1 MRR Waterfall Chart

**Purpose:** Show MRR bridge — how did MRR change this month?
**Chart type:** Waterfall (implemented as floating bar chart in Chart.js)
**Bars:**
- Opening MRR (blue base)
- New (green)
- Expansion (teal — existing customer upsells)
- Contraction (amber — existing customer downgrades)
- Churned (red)
- Closing MRR (blue)

**Each bar:** shows `+₹X.X L` or `-₹X.X L` label inside bar
**Period selector:** [This Month] [Last Month] [Custom Month]

#### 4.4.2 MRR Movement Table

| Category | Institutions | MRR Impact | # Deals |
|---|---|---|---|
| New | 12 | +₹3.2L | 12 |
| Expansion | 8 | +₹1.4L | 8 |
| Contraction | 3 | -₹0.8L | 3 |
| Churn | 2 | -₹1.1L | 2 |
| **Net New MRR** | | **+₹2.7L** | |

**Click row:** opens Institution Revenue Drawer for affected institutions

---

### 4.5 Tab: Plan Mix

`id="tab-planmix"` · `hx-get="?part=plan_mix"`

#### 4.5.1 Plan Distribution Chart

**Chart:** Grouped bar · X-axis: plan tiers (Starter/Standard/Professional/Enterprise)
**Series per bar:** Institutions count (left Y) vs MRR contribution (right Y)
**Legend:** Institutions `#6366F1` · MRR `#22D3EE`

#### 4.5.2 Plan Mix Trend (Stacked Area, 12 months)

**Chart:** Stacked area · one colour per plan
**Shows:** how plan mix has shifted over time (are Enterprise accounts growing as % of MRR?)

#### 4.5.3 Plan Summary Table

| Plan | Institutions | % of total | MRR | % of MRR | Avg MRR/inst |
|---|---|---|---|---|---|
| Starter | 820 | 40% | ₹4.1L | 10% | ₹500 |
| Standard | 850 | 41% | ₹12.8L | 30% | ₹1,506 |
| Professional | 280 | 14% | ₹11.2L | 26% | ₹4,000 |
| Enterprise | 100 | 5% | ₹14.7L | 34% | ₹14,700 |

**Row click:** filters Revenue Trend tab to that plan

---

### 4.6 Tab: Collections

`id="tab-collections"` · `hx-get="?part=collections"`

#### 4.6.1 Collections Summary Cards (3 cards)

| Card | Value |
|---|---|
| Total Invoiced (period) | `₹XX.X L` |
| Total Collected | `₹XX.X L` · collections rate % |
| Overdue Balance | `₹XX.X L` · aging breakdown |

#### 4.6.2 Aging Analysis Chart

**Chart:** Horizontal stacked bar (single bar) showing overdue by aging bucket:
- Current (< 30d): green
- 30–60d: amber
- 60–90d: orange
- > 90d: red
**Tooltip:** each segment amount + institution count

#### 4.6.3 Overdue Invoice Table

`id="overdue-table"` · `hx-get="?part=overdue_table"`

| Column | Detail |
|---|---|
| Institution | Name + type |
| Invoice # | Clickable → Invoice Drawer |
| Amount | `₹XX,XXX` right-aligned |
| Due Date | Date |
| Overdue by | Days (red if > 60) |
| Last reminder | Relative date |
| Actions ⋯ | Send Reminder / Mark Paid / Write Off |

**Sort:** Overdue days desc
**Filters:** Type · Aging bucket
**Pagination:** 25/page

**[Send Bulk Reminders]** button: sends payment reminder to all selected overdue institutions. Shows confirmation modal before sending.

#### 4.6.4 Collections Rate Trend (line chart, 12 months)

`#6366F1` line · dashed target line at 98% `#10B981`

---

### 4.7 Tab: Forecast

`id="tab-forecast"` · `hx-get="?part=forecast"`

#### 4.7.1 MRR Forecast Chart (12 months forward)

**Series:**
- Historical MRR: solid `#6366F1`
- Forecast (base case): dashed `#818CF8`
- Forecast upper bound: shaded area `rgba(99,102,241,0.1)`
- Forecast lower bound: shaded area
- YoY comparison: dotted `#475569`

**Forecast model inputs (sidebar):**
- Assumed growth rate (editable slider 0–50%)
- Churn rate (editable)
- Expansion rate (editable)
- [Recalculate] button → `hx-post="?part=forecast_calc"` with inputs

#### 4.7.2 Forecast Summary Table

| Metric | M+1 | M+3 | M+6 | M+12 |
|---|---|---|---|---|
| Projected MRR | ₹44.2L | ₹48.7L | ₹57.3L | ₹78.4L |
| Projected ARR | ₹5.3Cr | ₹5.8Cr | ₹6.9Cr | ₹9.4Cr |
| New institutions | +12 | +38 | +80 | +175 |

---

## 5. Drawers

### 5.1 Invoice Drawer (560 px)

Triggered from any invoice row.

**Header:** Invoice # + institution name + amount + status badge · `[×]`

**Section A — Invoice Details:**
- Invoice number · Issue date · Due date · Paid date (if paid)
- Billing period
- Institution: name + plan + type

**Section B — Line Items:**
| Description | Qty | Unit price | Amount |
|---|---|---|---|
| Standard Plan (Feb 2025) | 1 | ₹15,000 | ₹15,000 |
| Additional Students (200 × ₹5) | 200 | ₹5 | ₹1,000 |
| GST (18%) | | | ₹2,880 |
| **Total** | | | **₹18,880** |

**Section C — Payment history:** Timeline of reminders sent + payment received

**Section D — Actions:**
[Download PDF] [Send Reminder] [Mark as Paid] [Write Off] [Close]

**Mark as Paid:** requires reason + date + amount · 2FA required

---

### 5.2 Financial Period Drawer (480 px)

Triggered by clicking a month on the MRR trend chart.

Shows: MRR snapshot at that month · New/Churned/Expansion/Contraction breakdown · Top 10 revenue institutions that month · Notable events

---

## 6. Modals

### 6.1 Send Bulk Reminders Modal (480 px)

**Header:** "Send Payment Reminders"
**Body:** "Sending reminders to {N} institutions with overdue invoices totalling ₹XX.X L"
- Template preview (editable email template)
- CC to: billing contact / primary contact toggle
**Footer:** [Cancel] [Send Reminders]

---

### 6.2 Write-off Invoice Modal (480 px)

**Header:** "Write Off Invoice #{number}"
**Fields:**
- Amount to write off: `₹XX,XXX` (pre-filled, editable)
- Reason: Select (Bad debt / Goodwill / Error / Other)
- Notes: Textarea
- Auth: 2FA required

**Footer:** [Cancel] [Confirm Write-off]

---

## 7. HTMX Architecture

| Part param | Template | Trigger |
|---|---|---|
| `?part=kpi` | `exec/partials/finance_kpi.html` | Page load · poll 2 min |
| `?part=revenue_trend` | `exec/partials/finance_revenue.html` | Tab click · filter change |
| `?part=mrr_movement` | `exec/partials/finance_mrr.html` | Tab click · filter change |
| `?part=plan_mix` | `exec/partials/finance_plans.html` | Tab click · filter change |
| `?part=collections` | `exec/partials/finance_collections.html` | Tab click |
| `?part=overdue_table` | `exec/partials/finance_overdue.html` | Filter change · tab load |
| `?part=forecast` | `exec/partials/finance_forecast.html` | Tab click |
| `?part=forecast_calc` | JSON | Forecast recalculate POST |
| `?part=invoice_drawer&id={id}` | `exec/partials/invoice_drawer.html` | Invoice row click |
| `?part=period_drawer&month={ym}` | `exec/partials/period_drawer.html` | Chart month click |

**Django view dispatch:**
```python
class FinancialOverviewView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "portal.view_exec_finance"

    def get(self, request):
        ctx = self._build_context(request)
        if _is_htmx(request):
            part = request.GET.get("part", "")
            templates = {
                "kpi": "exec/partials/finance_kpi.html",
                "revenue_trend": "exec/partials/finance_revenue.html",
                "mrr_movement": "exec/partials/finance_mrr.html",
                "plan_mix": "exec/partials/finance_plans.html",
                "collections": "exec/partials/finance_collections.html",
                "overdue_table": "exec/partials/finance_overdue.html",
                "forecast": "exec/partials/finance_forecast.html",
                "invoice_drawer": "exec/partials/invoice_drawer.html",
                "period_drawer": "exec/partials/period_drawer.html",
            }
            if part in templates:
                return render(request, templates[part], ctx)
        return render(request, "exec/financial_overview.html", ctx)

    def post(self, request):
        part = request.GET.get("part", "")
        if part == "forecast_calc":
            return self._handle_forecast(request)
        return HttpResponseNotAllowed(["GET"])

    def _build_context(self, request):
        return {
            "kpi": finance_kpi_from_cache(),
            "filters": extract_filters(request.GET),
        }
```

**Poll pause:**
```html
<div id="finance-kpi"
     hx-get="/exec/financial-overview/?part=kpi"
     hx-trigger="every 120s[!document.querySelector('.drawer-open,.modal-open')]"
     hx-swap="innerHTML">
```

---

## 8. Performance Requirements

| Metric | Target | Critical |
|---|---|---|
| KPI strip | < 300 ms | > 800 ms |
| Revenue trend chart | < 600 ms | > 1.5 s |
| MRR waterfall | < 400 ms | > 1 s |
| Plan mix charts | < 400 ms | > 1 s |
| Overdue table (25 rows) | < 400 ms | > 1 s |
| Forecast chart | < 500 ms | > 1.2 s |
| Invoice drawer | < 300 ms | > 800 ms |
| Full page initial load | < 1.2 s | > 3 s |

**Decimal safety:** All Django ORM aggregations use `Sum(output_field=DecimalField(max_digits=28, decimal_places=2))`. No Python float arithmetic on financial values. Template formatting: `|floatformat:2` with custom `₹` prefix tag.

---

## 9. States & Edge Cases

| State | Behaviour |
|---|---|
| Net New MRR < 0 (shrinking) | Net New MRR card: red background `bg-[#450A0A]` + alert icon |
| Collections Rate < 90% | Collections Rate card: red background + alert |
| Overdue > ₹20L | Overdue Balance card: red background + amber banner at top of page |
| No invoices in selected period | Empty state per tab with CTA |
| Write-off: amount > ₹1L | Extra confirmation step: "This write-off exceeds ₹1L — confirm with reason" |
| Forecast: growth rate > 50% | Warning "High growth assumption — verify inputs" |
| Invoice already paid, marked paid again | Error toast "Invoice is already marked as paid" |
| Period with 0 revenue (new month, early) | Chart shows 0 bar, not null gap |

---

## 10. Keyboard Shortcuts

| Key | Action |
|---|---|
| `1`–`5` | Switch tabs |
| `F` | Focus filter bar |
| `R` | Refresh current tab |
| `E` | Export P&L report |
| `Esc` | Close drawer/modal |
| `?` | Keyboard shortcut help |

---

## 11. Template Files

| File | Purpose |
|---|---|
| `exec/financial_overview.html` | Full page shell |
| `exec/partials/finance_kpi.html` | KPI strip (7 cards) |
| `exec/partials/finance_revenue.html` | Revenue trend tab |
| `exec/partials/finance_mrr.html` | MRR waterfall tab |
| `exec/partials/finance_plans.html` | Plan mix tab |
| `exec/partials/finance_collections.html` | Collections tab |
| `exec/partials/finance_overdue.html` | Overdue invoice table |
| `exec/partials/finance_forecast.html` | Forecast tab |
| `exec/partials/invoice_drawer.html` | Invoice detail drawer |
| `exec/partials/period_drawer.html` | Financial period drawer |
| `exec/partials/bulk_reminder_modal.html` | Send reminders modal |
| `exec/partials/writeoff_modal.html` | Write-off confirmation modal |

---

## 12. Component References

| Component | Used in |
|---|---|
| `KpiCard` | §4.1 |
| `GlobalFilterBar` | §4.2 |
| `TabBar` | §4.3–4.7 |
| `MRRTrendChart` | §4.3.1 |
| `DonutChart` | §4.3.2 |
| `HorizontalBarChart` | §4.3.3 |
| `WaterfallChart` | §4.4.1 |
| `MRRMovementTable` | §4.4.2 |
| `StackedAreaChart` | §4.5.2 |
| `PlanSummaryTable` | §4.5.3 |
| `AgingAnalysisChart` | §4.6.2 |
| `OverdueTable` | §4.6.3 |
| `CollectionsTrendLine` | §4.6.4 |
| `ForecastChart` | §4.7.1 |
| `ForecastSlider` | §4.7.1 inputs |
| `DrawerPanel` | §5.1–5.2 |
| `ModalDialog` | §6.1–6.2 |
| `PaginationStrip` | All tables |
| `PollableContainer` | KPI strip |
