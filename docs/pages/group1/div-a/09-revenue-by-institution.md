# div-a-09 — Revenue by Institution

## 1. Platform Scale Reference

| Dimension | Value |
|---|---|
| Schools | 1,000 · avg 1,000 students · max 5,000 |
| Colleges | 800 · avg 500 · max 2,000 |
| Coaching centres | 100 · avg 10,000 · max 15,000 |
| Groups | 150 · each owns 5–50 child institutions |
| **Total institutions** | **2,050** |
| Total students | 2.4M–7.6M |
| Total platform ARR | ₹60 Cr+ |
| ARR range per institution | ₹60K/yr (smallest school) – ₹1.8 Cr/yr (largest coaching) |
| Top 10 institutions by ARR | ~₹18 Cr combined (30% of total) |
| Revenue concentration risk | Top 100 institutions ≈ 70% of ARR (₹42 Cr) |
| Overage revenue (coaching) | ₹3–5 Cr/yr from seats exceeded |
| Group billing | Single invoice; total child ARR up to ₹8 Cr |
| Table rows | 2,050 max (all active); 25/page |

**Architect's note:** This page is the CFO's retention and expansion radar. The 100 institutions contributing ₹42 Cr must be immediately visible. A coaching centre at 95% seat capacity represents ₹2+ Cr in latent expansion ARR. Churn signals for an Enterprise institution mean ₹18 L/month revenue risk. Every UI interaction here has revenue consequences — the table sort, the churn risk badge, the upsell indicator. The group row expand must show child ARR inline so no child institution's risk is hidden behind a roll-up.

---

## 2. Institution Taxonomy — Revenue Context

| Type | Revenue model | Avg ARR | Expansion signal | Churn signal |
|---|---|---|---|---|
| School | Annual flat + overage if > seats | ₹2.4 L/yr | Student count growing YoY | Admin not logged in 30+ days |
| College | Annual flat | ₹3.75 L/yr | Adding new streams (Science→Commerce) | Fee-cycle liquidity stress |
| Coaching centre | Monthly postpaid + overage | ₹18 L/yr | Batch count growing; seats > 90% capacity | Students declining MoM |
| Group | Annual umbrella invoice | ₹12 L/yr | Adding child institutions | Leadership change at group level |

---

## 3. Page Metadata

| Field | Value |
|---|---|
| Route | `/exec/revenue/institutions/` |
| **Single page API** | **All partials from `/exec/revenue/institutions/?part={name}`** |
| View | `RevenueByInstitutionView` |
| Template | `exec/revenue_institutions_page.html` |
| Priority | P1 |
| Nav group | Finance |
| Roles | `exec`, `finance` |
| Default sort | ARR descending |
| Default year | Current fiscal year (Apr → Mar) |
| HTMX poll | None (on-demand only) |

---

## 4. Full Page Wireframe

```
╔══════════════════════════════════════════════════════════════════════════════╗
║ Revenue by Institution          [Export ▾]  [↺ Refresh]  [📅 FY 2025-26 ▾]║
╠════════════╦════════════╦════════════╦════════════╦════════════╦════════════╣
║ Total ARR  ║ Avg ARR    ║ Top 10 ARR ║ Overage    ║ At-Risk    ║ Upsell     ║
║ ₹59.8 Cr  ║ ₹2.9 L     ║ ₹18.4 Cr  ║ Revenue    ║ Revenue    ║ Pipeline   ║
║            ║ per inst.  ║ (30.8%)    ║ ₹4.2 Cr   ║ ₹6.8 Cr   ║ ₹8.2 Cr   ║
╠══════════════════════════════╦═════════════════════════════════════════════╣
║ ARR BY TYPE (stacked bar)    ║ ARR DISTRIBUTION (histogram)               ║
║ [3M] [6M] [12M ●]           ║                                             ║
║ School/College/Coach/Group   ║ 0–1L: 400  1–5L: 800  5–20L: 650          ║
║ stacked, last 12 months      ║ 20–50L: 150  50L+: 50                      ║
║ Click bar → filter table     ║ Click bucket → filter table                ║
╠══════════════════════════════╩═════════════════════════════════════════════╣
║ TOOLBAR                                                                      ║
║ [🔍 Search institution name or code...]  [Type▾] [State▾] [ARR Range▾]   ║
║ [Status▾] [Plan▾] [Risk▾]  ── [Columns ▾]  ── [Export ▾]                  ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ INSTITUTION REVENUE TABLE                                                    ║
║ # │ Institution   │Type│State│Plan │ Base ARR │Overage│Total ARR│MRR│Risk│⋯║
║ 1 │▶ABC Coaching  │🟡Co│ TN  │Ent. │ ₹1.62 Cr │₹18.4L │ ₹1.80Cr │15L │ 8 │⋯║
║   │ └─Child Inst1 │🔵Co│ TN  │Prof.│  ₹42.0 L │  ₹0   │  ₹42 L  │3.5L│12 │⋯║
║ 2 │  XYZ Coaching │🟡Co│ MH  │Ent. │ ₹1.44 Cr │₹12.6L │ ₹1.57Cr │13L │22 │⋯║
║   └─────────────────────────────────────────────────────────────────────┘  ║
║   Showing 1–25 of 2,050     [← 1 2 3 ... 82 →]   [25 ▾ per page]          ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 5. Sections — Deep Specification

### 5.1 Page Header

**[Export ▾] dropdown:**
Options: CSV (full 2,050 rows) · Excel (formatted with charts) · PDF (summary report, max 50 pages)
For CSV/Excel: sync (< 2s for 2,050 rows). For PDF: async if > 30 pages → toast "Export queued".
URL: `/exec/revenue/institutions/?part=export&format=csv&year={{ year }}&{filter_params}`

**[↺ Refresh]:** Re-fetches all partials with current filters. Spin animation.

**[📅 FY 2025-26 ▾] Fiscal Year picker:**
Options: FY 2025-26 (default) · FY 2024-25 · FY 2023-24 · Last 12 Months · Last 24 Months · Custom range
Change triggers: `hx-get="/exec/revenue/institutions/?part=all&year=FY2025-26"` — all 4 partials update.
Active selection shown in button label.

---

### 5.2 KPI Cards (strip of 6)

**HTMX:** `id="rev-kpi"` `hx-get="/exec/revenue/institutions/?part=kpi&year={{ year }}"` `hx-trigger="load"` `hx-swap="innerHTML"`

**Grid:** `grid grid-cols-6 gap-4` (same anatomy as other pages)

| # | Label | Formula | Precision | Delta basis | Alert |
|---|---|---|---|---|---|
| 1 | Total ARR | Σ all active institution ARRs | ₹1 | vs prior FY | None |
| 2 | Avg ARR per Institution | Total ARR ÷ active count | ₹100 | vs prior FY | None |
| 3 | Top 10 ARR | Sum of top 10 by ARR; shows "X% of total" below | ₹1 | vs prior FY | > 35% concentration = amber |
| 4 | Overage Revenue | Σ usage overage charges in period | ₹1 | vs prior FY | — |
| 5 | At-Risk Revenue | ARR of institutions with churn_risk > 60 | ₹1 | vs 30 days ago | > ₹5 Cr = red |
| 6 | Upsell Pipeline | AM-estimated expansion ARR; "Not set" if no AM entry | ₹1 | — | — |

**Hover tooltip:** Card 3: "Top 10 institutions: [list of names]"
**Card 5 click:** Filters table to `risk=high` automatically.
**Card 6 "Not set":** Grey text; tooltip "Account managers can set pipeline estimates in the institution detail."

---

### 5.3 ARR by Type Stacked Bar Chart

**HTMX:** `id="rev-chart"` `hx-get="/exec/revenue/institutions/?part=chart&range=12m&year={{ year }}"` `hx-trigger="load"` `hx-swap="innerHTML"`

**Time range toggle:** `[3M] [6M] [12M ●]` — click: `hx-get` with `range=6m` param.

**Chart.js Stacked Bar (v4.4.2):**
- `id="arr-type-chart"`, height 240px, width 100%
- X-axis: months (Jan–Dec or rolling)
- Y-axis: ARR in ₹ Cr, integer ticks
- Stacks (bottom to top): School `#3B82F6` · College `#6366F1` · Coaching `#F59E0B` · Group `#14B8A6`
- Legend: horizontal below chart, 12px labels
- Grid lines: `rgba(255,255,255,0.04)`
- Tooltip: "March 2026\nSchool: ₹16.2 Cr\nCollege: ₹14.8 Cr\nCoaching: ₹24.6 Cr\nGroup: ₹4.2 Cr\nTotal: ₹59.8 Cr"
- Click bar segment → `hx-get="/exec/revenue/institutions/?part=table&type=coaching&month=mar2026"` — filters table
- Window._charts registry: destroy then recreate on HTMX swap

---

### 5.4 ARR Distribution Histogram

**HTMX:** `id="rev-histogram"` `hx-get="/exec/revenue/institutions/?part=histogram&year={{ year }}"` `hx-trigger="load"` `hx-swap="innerHTML"`

**Chart.js Bar (horizontal orientation):**
- `id="arr-dist-chart"`, height 180px
- X-axis: institution count (integer)
- Y-axis: ARR buckets (5 categories)
- Bars: indigo `#6366F1`
- Data:

| Bucket | Label | Expected count |
|---|---|---|
| ₹0–₹1 L | "Starter" | ~400 |
| ₹1–₹5 L | "Small" | ~800 |
| ₹5–₹20 L | "Mid" | ~650 |
| ₹20–₹50 L | "Large" | ~150 |
| ₹50 L+ | "Whale" | ~50 |

- Tooltip: "₹50 L+: 50 institutions — Coaching centres + large Groups"
- Click bar → filters table to that ARR range (`arr_min=5000000&arr_max=20000000`)

---

### 5.5 Toolbar

**Search input:**
- Placeholder: "Search institution name or code…"
- Width: 280px desktop, full-width mobile
- Debounce 400ms: `hx-trigger="keyup changed delay:400ms"` → `hx-get="...?part=table&q={{ value }}"`
- Clear [✕] button inside input

**Institution Type dropdown (`[Type ▾]`):**
`<select>` · Options: All · School · College · Coaching · Group
Param: `type=coaching`

**State dropdown (`[State ▾]`):**
`<select>` · Options: All + 28 states + 2 UTs (alphabetical). E.g. "Tamil Nadu", "Maharashtra"
Param: `state=TN`

**ARR Range dropdown (`[ARR Range ▾]`):**
`<select>` Options:
- All
- Starter (< ₹1 L)
- Small (₹1–5 L)
- Mid (₹5–20 L)
- Large (₹20–50 L)
- Whale (₹50 L+)
- Custom range… → reveals two number inputs (₹ from / ₹ to)
Param: `arr_min=5000000&arr_max=20000000`

**Status dropdown (`[Status ▾]`):**
Options: All · Active · Trial · Suspended · Churned
Param: `status=active`

**Plan dropdown (`[Plan ▾]`):**
Options: All · Standard · Professional · Enterprise · Custom
Param: `plan=enterprise`

**Risk dropdown (`[Risk ▾]`):**
Options: All · High (> 60) · Medium (30–60) · Low (< 30) · No data
Param: `risk=high`

**[Columns ▾] visibility toggle:**
Checkbox list: Rank ✓ · Base ARR ✓ · Overage ✓ · Total ARR ✓ · MRR ✓ · Churn Risk ✓ · Last Invoice · Renewal Date · AM Name
Stored per user in localStorage.

**Active filter chips (below toolbar):**
```
[Enterprise ✕] [TN ✕] [Whale ✕] [High Risk ✕]    [Clear all]
```
Style: `bg-[#131F38] border border-[#1E2D4A] rounded text-xs text-white px-2 py-0.5` + ✕ per chip

---

### 5.6 Institution Revenue Table

**HTMX:** `id="rev-table-container"` `hx-get="/exec/revenue/institutions/?part=table&year={{ year }}&sort=-arr"` `hx-trigger="load"` `hx-swap="innerHTML"`

**Columns (default visibility):**

| Column | Width | Sortable | Detail |
|---|---|---|---|
| Rank | 50px | No (follows sort) | 1 = highest ARR; resets when sort changes |
| Institution Name | 220px | Yes | Clickable → Institution Revenue Drawer (§6.1). Group rows: ▶ expand icon left of name. |
| Type | 70px | Yes | School `#3B82F6` · College `#6366F1` · Coaching `#F59E0B` · Group `#14B8A6` — small badge |
| State | 50px | Yes | 2-letter ISO code (TN, MH, KA…) |
| Plan | 90px | Yes | Standard · Professional · Enterprise · Custom |
| Base ARR | 110px | Yes (default desc) | ₹ Indian number format (₹1,62,40,000 = ₹1.62 Cr). "₹0" for Trial/Churned |
| Overage YTD | 100px | Yes | ₹ amount; amber cell if > 20% of base ARR; tooltip explains |
| Total ARR | 110px | Yes | Base + Overage. This is the primary sort column by default. |
| MRR | 90px | Yes | Total ARR ÷ 12 |
| Status | 90px | Yes | Active `bg-green-900 text-green-300` · Trial `bg-blue-900 text-blue-300` · Suspended `bg-amber-900 text-amber-300` · Churned `bg-gray-800 text-gray-400` |
| Churn Risk | 80px | Yes | 0–100 badge. 0–30: `text-green-400` · 31–60: `text-amber-400` · 61–100: `text-red-400`. "New" badge for < 30 days |
| Actions ⋯ | 40px | No | View Detail · Create Invoice · Contact AM · Flag At-Risk · Copy Institution Code |

**Group row expand:**
- ▶ icon (8×8, `text-[#8892A4]`) left of institution name for Group type rows
- Click ▶: `hx-get="/exec/revenue/institutions/?part=children&group_id={{ id }}"` `hx-target="#group-children-{{ id }}"` `hx-swap="innerHTML"`
- Children render inline with 24px left indent: `pl-6 border-l-2 border-[#1E2D4A]`
- ▼ icon replaces ▶ when expanded; click again collapses
- Each child row has own ARR, risk score, status
- Group row Total ARR = Σ all children (Σ shown in bold)

**Row styling:**
- Default: `bg-[#0D1526]`
- Hover: `bg-[#131F38]`
- Churned: `opacity-50`
- High risk (> 60): subtle `border-l-4 border-amber-500`
- Trial: italic institution name

**Sort:**
- Default: Total ARR descending
- Sort icon in header: ↕ (unsorted) → ↑ (asc) → ↓ (desc) on click
- HTMX: `hx-get="...?part=table&sort=-arr"` (prefix `-` = desc)

**Row click (not ▶, not ⋯):** Opens Institution Revenue Drawer (§6.1)

**⋯ Actions menu:**
- View Detail → opens drawer
- Create Invoice → opens Create Invoice Modal (same as div-a-08)
- Contact Account Manager → opens email compose with institution context pre-filled
- Flag At-Risk → POST `/exec/revenue/institutions/{id}/flag/` → confirmation toast
- Copy Institution Code → copies to clipboard → "Copied!" toast

---

### 5.7 Pagination

**Rendered within `?part=table` partial:**

```
Showing 1–25 of 2,050 institutions          [←]  [1] [2] [3] ... [82]  [→]     [25 ▾]
```

Same pagination anatomy as all other pages:
- "Showing X–Y of Z": `text-[#8892A4] text-sm`
- Current page: `bg-[#6366F1] text-white rounded px-3 py-1 text-sm`
- Ellipsis: shown when > 7 pages, shows first/last ± 2 around current
- Per-page: `<select>` options 10 / 25 / 50 / 100; change resets to page 1
- Navigation: HTMX swap of `#rev-table-container`

---

## 6. Drawers

### 6.1 Institution Revenue Drawer (560 px)

**Open trigger:** Click institution name in table (not ▶ expand, not ⋯).

**HTMX:** `hx-get="/exec/revenue/institutions/?part=drawer&id={{ id }}"` `hx-target="#drawer-container"` `hx-swap="innerHTML"`

**Drawer header:**
```
┌────────────────────────────────────────────────────────────────────┐
│ ABC Coaching Centre         [🟡 Coaching] [Enterprise] [₹1.80 Cr] │
│ Tamil Nadu · Code: ABCC001                              [✕]        │
└────────────────────────────────────────────────────────────────────┘
```
- Type badge: `bg-amber-900 text-amber-300 rounded px-2 py-0.5 text-xs`
- Plan badge: `bg-violet-900 text-violet-300 rounded px-2 py-0.5 text-xs`
- ARR chip: `bg-[#131F38] text-white rounded-full px-3 py-1 text-sm font-medium`

**Tabs within drawer:**
```
[Revenue ●] [Invoices] [Usage vs Plan] [Expansion] [Churn Risk]
```
Active: `border-b-2 border-[#6366F1] text-white`
Inactive: `text-[#8892A4] hover:text-white cursor-pointer`
Click: `hx-get="/exec/revenue/institutions/?part=drawer-tab&id={{ id }}&tab=invoices"` `hx-target="#rev-drawer-tab"` `hx-swap="innerHTML"`

---

**Tab: Revenue Summary**

**12-month ARR sparkline:**
- Inline Chart.js Line, 520px × 80px
- Series: Base ARR `#6366F1` (solid) · Overage `#F59E0B` (dashed)
- No axes; just the line with dots at each month
- Tooltip: "March 2026 | Base: ₹1.62 Cr | Overage: ₹18.4 L"

**Metrics grid (2×3):**

| Base ARR | Overage YTD | Total ARR |
|---|---|---|
| ₹1,62,40,000 | ₹18,40,000 | ₹1,80,80,000 |

| MRR | Next Renewal | Contract End |
|---|---|---|
| ₹15,06,667 | Apr 1, 2027 | Mar 31, 2027 |

Values in Indian number format. All Decimal — never float.

**Plan details row:**
```
Enterprise · 10,000 base seats · ₹8/student/month overage · Annual prepaid
```

---

**Tab: Invoice History**

Last 24 months of invoices. Table within drawer (scrollable max-height 360px):

| Column | Detail |
|---|---|
| Period | "Apr 2025 – Mar 2026" |
| Amount | ₹ (Decimal, Indian format) |
| Status | Paid `green` · Pending `blue` · Overdue `red` · Failed `orange` |
| Due Date | Date; "X days overdue" in red |
| Paid On | Date or "—" |
| ⬇ | Download PDF icon → GET `/exec/invoices/{id}/pdf/` |

No pagination within drawer (max 24 rows visible). Scroll within `max-height: 360px overflow-y-auto`.

---

**Tab: Usage vs Plan**

**Primary usage bar:**
```
Student seats: 9,480 / 10,000 (94.8%)
[████████████████████████████░░] ← amber (> 80%)
```
Bar colours: `bg-green-500` (< 80%) → `bg-amber-500` (80–100%) → `bg-red-500` (> 100%)
Below bar: "1,200 seats used in overage this month — ₹9,600 overage charge"

If > 100%: red upsell prompt box:
```
⚠ Over plan limit by 480 seats
Upgrade to 12,000-seat plan: saves ₹X/month vs overage
[Request Upgrade →]
```

**Secondary usage bars (2 per row):**
- SMS Notifications: 4,200 / Unlimited
- Storage: 42 GB / 100 GB
- API Calls: 18,400 / 10,000/min peak (amber if > 80%)
- Proctoring: Included — unlimited

**Feature adoption score:** "Adoption: 8/10 features actively used ✅" — green chip

---

**Tab: Expansion Signals**

Positive signals (green check list):
- "✅ Student count +12% MoM (growing faster than plan)"
- "✅ 9 new exam series scheduled for Apr 2026"
- "✅ 94.8% seat utilisation — near capacity"
- "✅ Last admin login: 2 hours ago"
- "✅ 0 support tickets in last 90 days"

Estimated expansion ARR:
```
If upgraded to 12,000-seat plan: +₹28,000/month = +₹3.36 L/yr ARR
```
[Mark as Opportunity] button → AM pipeline tracking

---

**Tab: Churn Risk**

**Risk score gauge:**
```
Risk Score: 22 / 100
[████░░░░░░░░░░░░░░░░░░░░░░░] LOW RISK
```
Gauge bar: `bg-green-500` (0–30) · `bg-amber-500` (31–60) · `bg-red-500` (61–100)

**Score breakdown table:**

| Factor | Weight | Current score | Notes |
|---|---|---|---|
| Avg exam frequency (last 30d) | 25 pts | 2 pts | 8 exams/week — excellent |
| Admin last login | 20 pts | 0 pts | Logged in today |
| Student activity trend | 20 pts | 5 pts | Slightly declining this week |
| Invoice payment history | 20 pts | 0 pts | Always paid on time |
| Support tickets (90d) | 15 pts | 0 pts | 0 tickets |
| Feature adoption | 10 pts | 0 pts | 8/10 features used |
| **Total** | **100 pts** | **7 pts** | **LOW RISK** |

**Last 5 interactions:**
- "Mar 18, 2026 — Invoice paid ₹1.80 Cr"
- "Mar 15, 2026 — 14 exams completed this week"
- "Mar 10, 2026 — Admin login: Rajan Kumar"

**NPS (if available):** "NPS: 8/10 (Promoter) — collected Jan 2026"

---

**Drawer footer (sticky, always visible):**

```
[+ Create Invoice]  [📧 Contact AM]  [🚨 Flag At-Risk]  [Open Full Profile →]
```

- [Create Invoice]: opens Create Invoice Modal (inline, from drawer)
- [Contact AM]: opens email compose with pre-filled subject "Action needed: {institution_name}" + revenue context
- [Flag At-Risk]: POST flag, adds to At-Risk queue, confirmation toast
- [Open Full Profile →]: navigates to `/exec/institutions/{id}/`

---

## 7. States & Edge Cases

| State | Behaviour |
|---|---|
| Group row expand | Children render with 24px left indent, own ARR columns, own risk badge. Group row Total = Σ children in bold. Expand/collapse preserves scroll position. |
| Churned institution | Row: `opacity-50`, ARR = ₹0, Status = "Churned on {date}", all ⋯ actions except "View Detail" disabled. |
| Trial institution | ARR = "₹0 (Trial)". Status = "Trial · Expires {date}". Overage column = "—". No invoice history tab content. |
| Overage > 20% of base ARR | Overage cell: `bg-amber-900/30 text-amber-300`. Tooltip: "High overage — consider plan upgrade. {n} extra students × ₹8". |
| Group filter (ARR Range) | Group row shows if group total ARR is in range even if individual children are not. |
| State filter for Groups | Groups appear under state of billing/HQ address, even if children span multiple states. |
| Churn risk = 0 for new institution | Show "New" badge in bright indigo. Score breakdown shows "Insufficient data (< 30 days)". |
| AM upsell pipeline not set | Card 6 shows "Not set" in grey. Tooltip: "Set in institution detail." |
| Export all 2,050 | CSV: sync < 2s. Excel: sync < 5s. PDF: async → email. |
| No data for year | "No revenue data for FY 2023-24. Try FY 2024-25." empty state. |
| Network error on filter | Error state in table area: "⚠ Failed to load. [Retry]" |
| Mobile (< 768px) | Table collapses to cards (one per institution). Group expand hidden on mobile. Charts stack vertically. |

---

## 8. HTMX Architecture — One URL Per Page

**Page URL:** `/exec/revenue/institutions/`
**All partials from:** `/exec/revenue/institutions/?part={name}`

```python
class RevenueByInstitutionView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "portal.view_revenue_institutions"

    def get(self, request):
        ctx = self._build_context(request)
        if _is_htmx(request):
            part = request.GET.get("part", "")
            templates = {
                "kpi":        "exec/partials/rev_kpi.html",
                "chart":      "exec/partials/rev_chart.html",
                "histogram":  "exec/partials/rev_histogram.html",
                "table":      "exec/partials/rev_table.html",
                "children":   "exec/partials/rev_group_children.html",
                "drawer":     "exec/partials/rev_inst_drawer.html",
                "drawer-tab": "exec/partials/rev_inst_drawer_tab.html",
            }
            if part == "all":
                return render(request, "exec/partials/rev_all.html", ctx)
            if part in templates:
                return render(request, templates[part], ctx)
        return render(request, "exec/revenue_institutions_page.html", ctx)
```

| `?part=` | Trigger | Poll |
|---|---|---|
| `kpi` | Load + year change | No |
| `chart` | Load + time range toggle | No |
| `histogram` | Load + year change | No |
| `table` | Load + filter/sort/page change | No |
| `children` | Group row expand click | No |
| `drawer` | Institution name click | No |
| `drawer-tab` | Tab click within drawer | No |
| `all` | Year picker change, Refresh button | No |

**Key query params:** `year`, `type`, `state`, `arr_min`, `arr_max`, `status`, `plan`, `risk`, `q`, `page`, `per_page`, `sort`, `id` (for drawer), `tab` (for drawer tab), `group_id` (for children)

---

## 9. API Endpoints

| Method | URL | Key params | Response |
|---|---|---|---|
| GET | `/exec/revenue/institutions/` | All query params above | HTML partial or full page |
| GET | `/exec/revenue/institutions/?part=export` | `format`, filter params | File download or 202 Accepted |
| POST | `/exec/revenue/institutions/{id}/flag/` | `{reason}` | `{status: "flagged"}` |

---

## 10. Performance Requirements

| Metric | Target | Critical |
|---|---|---|
| `?part=kpi` | < 400 ms | > 1 s |
| `?part=chart` | < 600 ms | > 2 s |
| `?part=histogram` | < 400 ms | > 1 s |
| `?part=table` (25 rows, default sort) | < 600 ms | > 2 s |
| Table search (by name) | < 400 ms | > 1 s |
| Group children expand | < 300 ms | > 800 ms |
| Drawer load | < 500 ms | > 1.5 s |
| Drawer tab switch | < 400 ms | > 1 s |
| Export CSV (2,050 rows) | < 3 s | > 10 s = async |
| Churn risk (pre-computed nightly) | < 100 ms (read from cache) | > 2h nightly batch = alert |
| Full page initial load | < 1.5 s | > 4 s |
| Chart render (browser) | < 200 ms | > 500 ms |

**All ARR values must use Python `Decimal`, never `float`. A float rounding error on ₹1.62 Cr is a finance incident.**

---

## 11. Keyboard Shortcuts

| Key | Action |
|---|---|
| `F` | Focus search input |
| `E` | Open Export dropdown |
| `R` | Refresh all partials |
| `Y` | Open Year picker |
| `Esc` | Close open drawer |
| `↑` / `↓` | Navigate table rows |
| `Enter` (on row) | Open Institution Revenue Drawer |
| `Space` (on group row) | Expand / collapse group children |
| `Shift+C` | Quick-filter to Coaching type |
| `Shift+S` | Quick-filter to School type |
| `Shift+E` | Quick-filter to Enterprise plan |
| `Shift+R` | Quick-filter to High Risk |
| `?` | Keyboard shortcut help modal |

---

## 12. HTMX Template Files

| File | Purpose |
|---|---|
| `exec/revenue_institutions_page.html` | Page shell with toolbar + KPI/chart/table targets |
| `exec/partials/rev_kpi.html` | 6 KPI cards |
| `exec/partials/rev_chart.html` | ARR by type stacked bar + time range toggle |
| `exec/partials/rev_histogram.html` | ARR distribution histogram |
| `exec/partials/rev_table.html` | Toolbar active-filter chips + table + pagination |
| `exec/partials/rev_group_children.html` | Children rows for group expand (inserted inline) |
| `exec/partials/rev_inst_drawer.html` | Institution Revenue Drawer (560px) |
| `exec/partials/rev_inst_drawer_tab.html` | Inner tab content (Revenue/Invoices/Usage/Expansion/Churn) |
| `exec/partials/rev_all.html` | Wrapper for full refresh (kpi + chart + histogram + table) |

---

## 13. Component References

| Component | Reusable partial | Used in |
|---|---|---|
| `KpiCard` | `components/kpi_card.html` | §5.2 |
| `ChartStackedBar` | `components/chart_bar.html` | §5.3 ARR by type |
| `ChartHistogram` | `components/chart_bar.html` | §5.4 distribution |
| `SearchInput` | `components/search_input.html` | §5.5 toolbar |
| `FilterDropdown` | `components/filter_dropdown.html` | §5.5 each filter |
| `ActiveFilterChips` | `components/filter_chips.html` | §5.5 below toolbar |
| `RevenueTable` | `exec/partials/rev_table.html` | §5.6 |
| `GroupExpandRow` | `components/group_row.html` | §5.6 group rows |
| `StatusBadge` | `components/status_badge.html` | §5.6 status column |
| `ChurnRiskBadge` | `components/risk_badge.html` | §5.6, §6.1 Churn tab |
| `PaginationStrip` | `components/pagination.html` | §5.7 |
| `DrawerPanel` | `components/drawer.html` | §6.1 |
| `TabBar` | `components/tab_bar.html` | §6.1 drawer tabs |
| `SparkLine` | `components/sparkline.html` | §6.1 Revenue tab |
| `UsageMeterBar` | `components/usage_bar.html` | §6.1 Usage vs Plan tab |
| `RiskGauge` | `components/risk_gauge.html` | §6.1 Churn Risk tab |
| `ExportDropdown` | `components/export_dropdown.html` | §5.1 header |
| `LoadingSkeleton` | `components/skeleton.html` | Table + charts |
| `EmptyState` | `components/empty_state.html` | Table empty |
