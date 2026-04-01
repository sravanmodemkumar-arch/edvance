# 33 — Razorpay Settlement Tracker

---

## 1. Page Metadata

| Field | Value |
|---|---|
| Page title | Razorpay Settlement Tracker |
| Route | `/exec/settlements/` |
| Django view | `RazorpaySettlementView` |
| Template | `exec/settlements.html` |
| Priority | **P1** |
| Nav group | Financial |
| Required roles | `cfo` · `finance_manager` · `billing_admin` · `ceo` · `superadmin` |
| COO access | Read-only (no actions) |
| CTO access | Denied — redirect to `/exec/dashboard/` |
| HTMX poll — summary strip | Every 60s |
| HTMX poll — settlement table | No auto-poll (manual refresh or filter change) |
| Cache | Summary strip: Redis TTL 55s · Settlement rows: Redis TTL 300s |
| Theme tokens | bg-base `#040810` · surface-1 `#08101E` · surface-2 `#0D1828` · accent `#6366F1` · success `#22C55E` · danger `#EF4444` · warn `#F59E0B` |

---

## 2. Purpose & Business Logic

**The problem this page solves:**

EduForge processes subscription payments through Razorpay. Institutions pay monthly/annual subscriptions — Razorpay collects the payment, deducts its processing fee (typically 2–3%), and settles the net amount to EduForge's bank account in a batch 2–7 business days later.

At Rs.60 Cr+ ARR with ~2,050 institutions, the CFO faces three distinct operational risks daily:

1. **Reconciliation risk** — Has every Razorpay settlement actually hit the bank? Are any settlements missing, stuck, or short?
2. **Fee leakage risk** — Is EduForge paying the negotiated Razorpay fee rate, or are some transactions being charged at a higher tier? At Rs.60 Cr volume, a 0.1% fee overcharge = Rs.6 lakh/year lost.
3. **Refund exposure risk** — Refunds are deducted from future settlements. If the refund pipeline grows faster than collections (e.g., due to a billing dispute at a large coaching centre), EduForge's net settlement could go negative, creating a cash flow gap.

**What decisions this page enables:**
- Is the Rs.4.2L pending settlement actually 14 hours from now, or is it stuck? → CFO calls Razorpay account manager if > 24h late
- Which payment method (UPI vs card vs netbanking) has the highest failure rate? → Product team prioritises payment UX fix
- Is the refund volume this month > last month by > 20%? → Finance team investigates root cause before it becomes a cash flow issue
- Did Razorpay correctly apply the negotiated fee cap for Enterprise institutions? → Manual fee audit trigger

**Scale context:**
- ~2,050 institutions paying monthly/annual
- Peak payment events: renewal cycles (30+ institutions renewing same week = Rs.15L+ batch)
- Razorpay fee: ~2% average across all payment methods (negotiated cap for Enterprise tier)
- Expected settlement cycle: T+2 for UPI/cards, T+7 for netbanking
- Monthly transaction volume: ~1,200–2,400 payment events
- Annual settled amount: Rs.60 Cr+

---

## 3. User Roles & Access

| Role | Can View | Can Act | Specific Capabilities |
|---|---|---|---|
| CEO / Platform Owner | All sections | Mark dispute, download report | Cannot trigger refunds |
| CFO | All sections | All read actions + dispute flag + CSV export | Read-only (Level 1) — no payment mutations |
| Finance Manager (Level 1) | All sections | Same as CFO | Read-only |
| Billing Admin (Level 3) | All sections | Can view refund pipeline detail | Cannot raise disputes or export financials |
| COO | All sections | Read-only | No financial actions |
| CTO / Engineering | No access | — | Redirected with message |
| Ops Manager | No access | — | Redirected with message |

**Role-based UI differences:**
- "Flag Dispute" button: CFO / Finance Manager / CEO only
- "Export CSV / PDF" buttons: CFO / Finance Manager / CEO only
- Settlement row amount column: shown only to CFO / Finance Manager / CEO. Billing Admin sees "—" in the Amount column (privacy — amount data is restricted to finance roles)

---

## 4. Section-wise UI Breakdown

---

### Section 1 — Page Header

**Purpose:** Establish context, provide date range control, and surface the single most critical status: "Is EduForge's last settlement received on time?"

**User interaction:**
- User selects a date range → all sections reload with filtered data
- "Last Settlement" status badge is the first thing the CFO reads on arrival

**UI elements:**
```
Razorpay Settlement Tracker          [📅 Apr 2026 ▾]  [Export CSV]  [Export PDF]
Last settlement: Rs.4,28,300 · 2 Apr 2026 · 14h ago · ✅ On time (T+2)
```
- Title: 22px bold `text-white`
- Month picker (not date range — settlements are monthly review): `<select>` listing last 12 months + "All time". Default: current month. Change triggers `hx-get` on all sections with `?month=2026-04`
- "Last settlement" line: 13px, structured as: amount (bold `text-white`) · date · relative time · status badge. Status: `✅ On time` (green) / `⚠ Delayed` (amber — if > T+3) / `🔴 Missing` (red — if > T+7 with no settlement received)
- Export CSV: `hx-get="/exec/settlements/?part=export&format=csv&month={{ month }}"` — streams download
- Export PDF: same but PDF via WeasyPrint

**Data flow:**
- Last settlement status: read from `settlement:last_received` Redis hash (written by Celery beat daily at 08:00 IST by polling Razorpay Settlements API). Fields: `amount`, `date`, `status`, `razorpay_settlement_id`
- If key missing or stale > 25 hours: show "Data refresh pending" in amber

**Role-based behavior:** Export buttons hidden for Billing Admin and COO.

**Edge cases:**
- No settlements this month (new account, or first payment month): "No settlements received yet for Apr 2026. First payment expected ~Apr 15."
- Razorpay API key expired: red banner "Razorpay API connection error — settlements data may be stale. [Check API Key →]" (links to page 31 API Keys)

**Performance:** Header data from Redis — < 50ms render.

**Mobile:** Month picker becomes full-width. Export buttons collapse into a `[⋯]` menu. Last settlement line wraps to 2 lines.

**Accessibility:** Date picker has `aria-label="Filter by month"`. Last settlement status badge has `role="status" aria-label="Last settlement: On time"`.

---

### Section 2 — Summary Strip (KPI Cards)

**Purpose:** Give the CFO a one-line financial status for the selected month: total collected, total settled, pending, fees paid, refunds deducted. This answers "where is our money right now?"

**User interaction:** Cards are read-only. Each card is clickable and scrolls to the relevant section in the table below (e.g., "Pending" card scrolls to rows with status=pending).

**UI elements — 5 cards in a flex row:**

```
╔══════════════╦══════════════╦══════════════╦══════════════╦══════════════╗
║ COLLECTED    ║ SETTLED      ║ PENDING      ║ FEES PAID    ║ REFUNDS OUT  ║
║              ║              ║              ║              ║              ║
║  ₹1,24,80K   ║  ₹1,18,40K   ║  ₹6,40K      ║  ₹2,36K      ║  ₹48K        ║
║  312 payments║  3 batches   ║  2 batches   ║  1.89% avg   ║  8 refunds   ║
╚══════════════╩══════════════╩══════════════╩══════════════╩══════════════╝
```

| Card | Formula | Alert condition |
|---|---|---|
| Collected | Sum of all payment_captured events in period | None (informational) |
| Settled | Sum of Razorpay settlement payouts received | If < 90% of Collected for > T+7: amber |
| Pending | Collected − Settled | If Pending > 20% of Collected: amber. If Pending > 40%: red |
| Fees Paid | Sum of Razorpay deductions from settlements | If effective fee rate > 2.5% (negotiated cap): red with "Fee anomaly" label |
| Refunds Out | Sum of refunds issued in period | If > 5% of Collected: amber (unusual refund volume) |

**Card anatomy:**
- Label: 10px uppercase `text-[#8892A4]`
- Primary value: 26px bold `text-white`
- Subline: 11px `text-[#8892A4]`
- Alert state border: `ring-1 ring-amber-500` or `ring-red-500`

**HTMX:** `id="settlement-summary"` `hx-get="/exec/settlements/?part=summary&month={{ month }}"` `hx-trigger="load, every 60s[!document.querySelector('.drawer-open,.modal-open')]"` `hx-swap="innerHTML"`

**Data flow:**
- Backend queries `RazorpaySettlement` model + `RazorpayRefund` model, aggregated by month
- Results cached in Redis: `settlements:summary:2026-04` TTL 55s
- Fee rate calculation: `total_fees / total_collected * 100`

**Role-based behavior:** Amount values hidden for non-finance roles (Billing Admin, COO see card labels with "Restricted" in the value position).

**Edge cases:**
- Loading state: 5 grey skeleton cards with pulse animation
- All zero (no transactions): cards show ₹0 with subdued styling and "No transactions in this period"
- API data inconsistency (Collected < Settled — can happen with previous month carryover): amber banner "Settlement amount exceeds collections — possible carryover from previous month. Review carefully."

**Performance:** Aggregation query runs < 200ms with indexes on `payment_date` and `status`. Result cached 55s.

**Mobile:** Cards stack 2-per-row (top row: Collected + Settled, middle: Pending + Fees, bottom: Refunds). Font sizes reduce to 20px for primary values.

**Accessibility:** Each card has `role="region" aria-label="Collected: 1,24,800 rupees"`. Alert states include `aria-live="polite"` to announce changes.

---

### Section 3 — Settlement Timeline Table

**Purpose:** The core of the page. Every Razorpay settlement batch is one row. The CFO can see the exact progression: payment captured → settlement created → payout processed → bank received. This is the reconciliation audit trail.

**User interaction:**
- Click any row → opens Settlement Detail Drawer (Drawer-G, 560px) with full reconciliation breakdown
- Filter by status (All / Received / Processing / Failed / Disputed)
- Search by settlement ID or institution name
- Sort by Date, Amount, Status
- "Flag Dispute" action per row (CFO/Finance only)
- Pagination: 20 rows per page, server-side

**UI elements:**

```
SETTLEMENTS                              [Status: All ▾]  [🔍 Search...]
─────────────────────────────────────────────────────────────────────────
Settlement ID     │ Date      │ Payments │ Gross    │ Fees   │ Net    │ Status    │ ⋯
──────────────────┼───────────┼──────────┼──────────┼────────┼────────┼───────────┼──
SETL-2026-0412    │ 2 Apr     │ 48       │ ₹4,31,200│ ₹2,900 │ ₹4,28,300│ ✅ Received│ ⋯
SETL-2026-0408    │ 30 Mar    │ 61       │ ₹5,82,100│ ₹3,800 │ ₹5,78,300│ ✅ Received│ ⋯
SETL-2026-0404    │ 28 Mar    │ 12       │ ₹98,400  │ ₹640   │ ₹97,760 │ ⚠ Processing│ ⋯
SETL-2026-0401    │ 26 Mar    │ 3        │ ₹24,000  │ ₹160   │ ₹23,840 │ 🔴 Failed  │ ⋯
```

**Column details:**

| Column | Width | Type | Detail |
|---|---|---|---|
| Settlement ID | 160px | Code link | `font-mono text-[#6366F1]` — click → Drawer-G |
| Date | 100px | Date | Settlement date (when Razorpay processed it). Format: "2 Apr" + full date on hover |
| Payments | 80px | Integer | Count of individual payment_captured events in this batch |
| Gross | 100px | Currency | Total before Razorpay fee. Hidden for non-finance roles |
| Fees | 80px | Currency | Razorpay deduction. Red if fee rate > 2.5% |
| Net | 100px | Currency | Amount received in bank. Bold. Hidden for non-finance roles |
| Status | 120px | Badge | See status definitions below |
| ⋯ | 80px | Menu | View Detail · Flag Dispute · Download Statement |

**Status definitions:**

| Status | Badge style | Business meaning |
|---|---|---|
| Received | `bg-green-900/50 text-green-300` | Confirmed in bank account |
| Processing | `bg-blue-900/50 text-blue-300` | Razorpay has initiated payout, T+1–2 |
| Pending | `bg-[#131F38] text-[#8892A4]` | Not yet initiated (payment < 24h old) |
| Failed | `bg-red-900/50 text-red-300 animate-pulse` | Payout failed — action required |
| Disputed | `bg-amber-900/50 text-amber-300` | Manually flagged — under investigation |

**"Flag Dispute" action:**
- Available from ⋯ menu or Drawer-G footer
- Opens a 400px modal: Settlement ID (pre-filled, read-only), Dispute reason (textarea, required, max 500 chars), Escalate to Razorpay (checkbox)
- POST `/exec/settlements/actions/flag-dispute/` → updates `RazorpaySettlement.status = 'disputed'`, creates `SettlementDispute` record, optionally sends dispute via Razorpay API, creates `AuditLog` entry
- Disputed rows: amber background, sticky-sorted to top of table

**HTMX:** `id="settlement-table"` `hx-get="/exec/settlements/?part=table&month={{ month }}&status={{ status }}&page={{ page }}"` `hx-trigger="load"` `hx-swap="innerHTML"`
- Filter chip changes: `hx-trigger="click"` → swaps `#settlement-table`
- Search input: `hx-trigger="keyup changed delay:400ms"` → swaps `#settlement-table`

**Data flow:**
- Backend: `RazorpaySettlement.objects.filter(month=...)` with sorting + pagination
- Data source: synced from Razorpay Settlements API via Celery beat task (daily at 07:00 and 14:00 IST)
- Cache: `settlements:table:2026-04:all:1` Redis key TTL 300s (5 min — table data is relatively stable)

**Role-based behavior:**
- Gross, Fees, Net columns: visible to CFO/Finance Manager/CEO only. Other roles see "—" in those cells
- "Flag Dispute" menu item: visible to CFO/Finance Manager/CEO only. Hidden from Billing Admin/COO

**Edge cases:**
- 0 settlements in period: empty state "No settlements found for Apr 2026. Payments may not have been captured yet, or the Razorpay sync may be pending."
- Failed settlement row: row has `border-l-4 border-red-500 bg-red-950/20` — immediately visible
- Search returns 0 results: "No settlements match '{query}'. Try clearing the search or widening the date range."

**Performance:**
- Table query: `SELECT ... FROM razorpay_settlements WHERE DATE_TRUNC('month', settlement_date) = '2026-04-01'` — index on `settlement_date`
- 20 rows per page: minimal payload
- Redis cache means repeat loads (CFO refreshing the page) hit cache, not DB

**Mobile:** Table collapses to: Settlement ID + Status + Net amount. Other columns hidden. Full detail via Drawer-G (opens full-screen on mobile).

**Accessibility:** Table has `role="grid"`. Sort headers have `aria-sort`. Status badges have `aria-label` with full status text. Pagination buttons have `aria-label="Next page"`.

---

### Section 4 — Payment Method Split (Donut Chart)

**Purpose:** Shows CFO how their institutional clients are paying. Critical for two reasons: (1) different payment methods have different Razorpay fee rates (UPI = 0%, Card = ~2%, Netbanking = 1.5%), so the payment mix directly determines average fee rate; (2) payment method failure rates differ — high netbanking usage = higher retry rate.

**User interaction:**
- Donut chart segments clickable → filters the settlement table below to show only settlements containing that payment method
- Hover on segment → tooltip with: method name, amount, count, fee rate, failure rate

**UI elements:**
```
PAYMENT METHOD SPLIT                              FAILURE RATE BY METHOD
╭──────────────────────────────╮    Method      Success%   Fail%   Avg Fee
│         ░░░░░░               │    UPI           98.4%     1.6%    0.00%
│       ░░      ░░░            │    Credit Card   96.2%     3.8%    2.00%
│      ░         ░░            │    Debit Card    95.8%     4.2%    2.00%
│     ░  64%UPI  ░░            │    Net Banking   91.2%     8.8%    1.50%
│      ░         ░░            │    EMI            94.1%    5.9%    2.50%
│       ░░      ░░░            │    Wallet         99.1%    0.9%    1.80%
│         ░░░░░░               │
╰──────────────────────────────╯
```

- Left: Chart.js Doughnut, `id="payment-mix-chart"`, 200px × 200px
- Segment colours: UPI `#22C55E`, Card `#6366F1`, Debit `#8B5CF6`, Netbanking `#F59E0B`, EMI `#EF4444`, Wallet `#14B8A6`
- Centre label: largest method name + % (24px bold)
- Right: table `<table class="text-xs">` — method, success%, fail%, avg fee%. Fail% column: amber if > 5%, red if > 10%

**HTMX:** `id="payment-split"` `hx-get="/exec/settlements/?part=payment-split&month={{ month }}"` `hx-trigger="load"` `hx-swap="innerHTML"`. No polling — static for selected month.

**Data flow:**
- Backend: `Payment.objects.filter(month=...).values('method').annotate(count=Count('id'), total=Sum('amount'), failures=Count('id', filter=Q(status='failed'))))`
- Cache: `settlements:payment-split:2026-04` TTL 300s

**Role-based behavior:** All permitted roles see this section. No restrictions.

**Edge cases:**
- Single payment method (e.g., all UPI): donut shows full circle with "100% UPI", no other segments. Failure rate table still shows all methods with 0 for absent ones.
- Chart.js destroy-and-recreate pattern on HTMX swap (same as War Room throughput chart).

**Performance:** Aggregation query < 100ms. Chart render < 50ms.

**Mobile:** Donut chart and table stack vertically. Donut reduces to 150px.

**Accessibility:** Doughnut has `role="img" aria-label="Payment method split: 64% UPI, 22% Credit Card, ..."`. Table has standard `<th scope="col">` headers.

---

### Section 5 — Refund Pipeline

**Purpose:** Refunds are deducted from future settlements. The CFO needs to see the open refund queue — both requested refunds (not yet processed) and processed refunds (deducted from which settlement). Unexpected refund spikes are early indicators of billing disputes or product issues.

**User interaction:**
- Table of all refunds in the period, filterable by status (Requested / Processing / Settled / Failed)
- Each row: click → opens a mini-drawer showing the original payment, the institution, refund reason, and which settlement deducted it
- "Mark for Review" action — flags a refund for Finance Manager follow-up
- Trend indicator: "Refunds up 34% vs last month" amber banner if true

**UI elements:**
```
REFUND PIPELINE                          ⚠ Refunds up 34% vs Mar 2026
                                         [Status: All ▾]
Refund ID     │ Institution        │ Amount │ Reason          │ Status      │ Settlement
──────────────┼────────────────────┼────────┼─────────────────┼─────────────┼────────────
REF-2026-0841 │ ABC Coaching       │ ₹8,400 │ Plan downgrade  │ ✅ Settled  │ SETL-0412
REF-2026-0836 │ XYZ School         │ ₹1,200 │ Student unenrol │ ⏳ Processing│ Pending
REF-2026-0829 │ DEF College Group  │ ₹24,000│ Dispute         │ 🔴 Failed   │ —
```

- Column widths: ID 130px, Institution 180px, Amount 80px (hidden for non-finance), Reason 160px, Status 120px, Settlement ID 120px
- "Failed" refund rows: `border-l-4 border-red-500`
- Settlement ID column: if settled, shows the settlement ID as a link → opens Drawer-G for that settlement

**HTMX:** `id="refund-pipeline"` `hx-get="/exec/settlements/?part=refunds&month={{ month }}&status={{ status }}"` `hx-trigger="load"` `hx-swap="innerHTML"`

**Data flow:**
- `RazorpayRefund.objects.filter(created_at__month=...).select_related('institution', 'settlement').order_by('-created_at')`
- If `month_refund_total / prev_month_refund_total > 1.3`: backend sets `show_spike_banner=True` in context

**Role-based behavior:** Amount column hidden for Billing Admin/COO.

**Edge cases:**
- 0 refunds: "No refunds issued in Apr 2026. ✅"
- Large dispute refund (> Rs.50,000): row highlighted with amber border; tooltip "Large refund — Finance review recommended"

**Performance:** Refund table typically < 50 rows/month. No pagination needed. Query < 100ms.

**Mobile:** Collapses to: Institution + Amount + Status. Reason and Settlement ID visible in the mini-drawer.

**Accessibility:** Table `role="grid"`. Status badges `aria-label="Status: Settled"`. Spike banner `role="alert" aria-live="assertive"`.

---

### Section 6 — Gateway Fee Tracker

**Purpose:** Validates that Razorpay is charging the negotiated fee rate. EduForge has a custom pricing agreement with Razorpay (typically lower than standard rates at Rs.60 Cr volume). This section shows the effective fee rate month-by-month versus the contracted rate, flagging anomalies.

**User interaction:** Read-only section. No user actions — just a bar chart and a comparison table.

**UI elements:**
```
GATEWAY FEE TRACKER                              Contracted rate: 2.00% max
                                                 Current month: 1.89% ✅ Within contract
Bar chart: last 12 months effective fee %
Each bar labelled with %
Contracted cap: dashed horizontal line at 2.00%

Month breakdown table:
Month     │ Volume     │ Fees Paid   │ Effective Rate │ vs Contract
Apr 2026  │ ₹1,24,80K  │ ₹2,360      │ 1.89%          │ ✅ -0.11%
Mar 2026  │ ₹1,41,20K  │ ₹2,820      │ 2.00%          │ ✅ At limit
Feb 2026  │ ₹98,400    │ ₹2,460      │ 2.50%          │ 🔴 +0.50% OVER
```

- Chart: Chart.js Bar, `id="fee-tracker-chart"`, 100% wide × 160px tall
- Bar colour: green if < contract rate, amber if = contract rate, red if > contract rate
- Contract rate line: `borderDash: [4,4]` red 1px

- Table: compact `text-xs` table below chart
- "vs Contract" column: green/amber/red based on difference. Red rows = month where Razorpay over-charged

**HTMX:** `id="fee-tracker"` `hx-get="/exec/settlements/?part=fee-tracker"` `hx-trigger="load"` `hx-swap="innerHTML"`. No polling — static (recalculated daily by Celery beat).

**Data flow:**
- Pre-computed daily by `compute_settlement_fee_analysis` Celery beat task
- Results stored in `SettlementFeeAudit` model (one row per month)
- Served from Redis cache: `settlements:fee-tracker` TTL 3600s

**Role-based behavior:** All permitted roles see this section.

**Edge cases:**
- Over-contract month detected: automatic `SettlementAlert` record created with `type='fee_overcharge'`. CFO is notified via email (Celery async task). Section shows: "🔴 Fee overcharge detected in Feb 2026 — Rs.490 over contract. [Raise with Razorpay →]"
- No contracted rate configured: section shows "Contract rate not configured. [Configure in Settings →]" with link to page 31.

**Performance:** Cached data — 12 months of aggregated data, < 5KB. Render < 50ms.

**Mobile:** Chart reduces to 120px. Table shows Month + Rate + vs Contract only (Volume and Fees hidden).

**Accessibility:** Bar chart `role="img" aria-label="Gateway fee tracker: last 12 months, current 1.89%, within contracted 2% cap"`.

---

## 5. Full Page Wireframe

```
╔══════════════════════════════════════════════════════════════════════════════╗
║  Razorpay Settlement Tracker          [📅 Apr 2026 ▾]  [Export CSV] [PDF]   ║
║  Last settlement: ₹4,28,300 · 2 Apr 2026 · 14h ago · ✅ On time (T+2)      ║
╠══════════╦══════════╦══════════╦══════════╦══════════════════════════════════╣
║ COLLECTED║ SETTLED  ║ PENDING  ║ FEES PAID║ REFUNDS OUT                      ║
║ ₹1,24,8K ║ ₹1,18,4K ║ ₹6,4K    ║ ₹2.36K   ║ ₹48K                            ║
║ 312 pymts║ 3 batches║ 2 batches║ 1.89% avg║ 8 refunds                       ║
╠══════════╩══════════╩══════════╩══════════╩══════════════════════════════════╣
║  SETTLEMENTS                           [Status: All ▾] [🔍 Search...      ]  ║
║  Settlement ID   │ Date   │ Payments │ Gross    │ Fees  │ Net      │ Status  ║
║  SETL-2026-0412  │ 2 Apr  │ 48       │ ₹4,31,2K │ ₹2,9K │ ₹4,28,3K │ ✅ Rcvd ║
║  SETL-2026-0408  │ 30 Mar │ 61       │ ₹5,82,1K │ ₹3,8K │ ₹5,78,3K │ ✅ Rcvd ║
║  SETL-2026-0404  │ 28 Mar │ 12       │ ₹98,4K   │ ₹640  │ ₹97,76K  │ ⚠ Proc  ║
║  SETL-2026-0401  │ 26 Mar │ 3        │ ₹24K     │ ₹160  │ ₹23,84K  │ 🔴 Fail ║
║  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─  ║
║  [< Prev]  Page 1 of 3  [Next >]                                             ║
╠══════════════════════════════════╦═════════════════════════════════════════════╣
║  PAYMENT METHOD SPLIT            ║  REFUND PIPELINE          ⚠ Up 34% MoM    ║
║  ╭──────────╮                    ║  REF-0841 │ ABC Coaching │ ₹8,4K │ ✅ Stld ║
║  │  64% UPI │   UPI   0.00%      ║  REF-0836 │ XYZ School   │ ₹1,2K │ ⏳ Proc ║
║  │          │   Card  2.00%      ║  REF-0829 │ DEF Group    │ ₹24K  │ 🔴 Fail ║
║  ╰──────────╯   NBanking 1.50%  ║                                             ║
╠══════════════════════════════════╩═════════════════════════════════════════════╣
║  GATEWAY FEE TRACKER                       Contracted: 2.00% · Current 1.89% ║
║  ▐█ ▐█ ▐█ ▐█ ▐█ ▐█ ▐█ ▐█ ▐█ ▐█ ▐█ ▐█    – – – – – – (contract cap) – –   ║
║  May Jun Jul Aug Sep Oct Nov Dec Jan Feb Mar Apr                               ║
╚══════════════════════════════════════════════════════════════════════════════════╝
```

---

## 6. Drawer-G — Settlement Detail (560px)

**Open trigger:** Click any settlement row OR Settlement ID link.

**HTMX:** `hx-get="/exec/settlements/?part=settlement-drawer&id={{ settlement_id }}"` `hx-target="#drawer-container"` `hx-swap="innerHTML"`

**Structure:**
```
┌─────────────────────────────────────────────────────┐
│  Settlement SETL-2026-0412              ✅ Received [✕]│
│  ─────────────────────────────────────────────────── │
│  [Summary ●]  [Payments]  [Reconciliation]           │
│  ─────────────────────────────────────────────────── │
│  (tab content — scrollable)                          │
│  ─────────────────────────────────────────────────── │
│  [Flag Dispute]                    [Download Statement]│
└─────────────────────────────────────────────────────┘
```

**Tab — Summary:**
- Settlement date: 2 Apr 2026
- Razorpay Settlement ID: SETL-2026-0412 (copyable, `font-mono`)
- Payment cycle: 31 Mar – 1 Apr 2026 (payments captured in this window)
- Payments included: 48
- Gross collected: Rs.4,31,200
- Razorpay fee: Rs.2,900 (0.67% effective — breakdown: Rs.X card + Rs.Y netbanking + Rs.Z UPI)
- Net settled: Rs.4,28,300
- Refunds deducted: Rs.0 (or list)
- Bank receipt: "Confirmed 2 Apr 2026 14:22 IST" + bank reference number

**Tab — Payments:**
- Table of all individual payments in this settlement batch
- Columns: Payment ID · Institution · Amount · Method · Captured at
- Paginated: 20/page

**Tab — Reconciliation:**
- Checks: Gross − Fees − Refunds = Net settled → "✅ Reconciled" or "🔴 Discrepancy: Rs.X unaccounted"
- Invoice match: lists which EduForge invoices are covered by payments in this batch
- Invoice match status: "All 48 payments matched to invoices ✅" or "3 payments unmatched ⚠"

**Footer:**
- [Flag Dispute]: visible CFO/Finance/CEO only → opens dispute modal
- [Download Statement]: downloads Razorpay settlement statement PDF (fetched from Razorpay API on demand)

---

## 7. Component Architecture

| Component | File | Props |
|---|---|---|
| `SettlementSummaryCard` | `components/settlements/summary_card.html` | `label, value, subline, alert_level (none/warn/crit)` |
| `SettlementTableRow` | `components/settlements/settlement_row.html` | `settlement, can_view_amounts, can_dispute` |
| `SettlementStatusBadge` | `components/settlements/status_badge.html` | `status (received/processing/pending/failed/disputed)` |
| `PaymentMethodDonut` | `components/settlements/payment_donut.html` | `methods (list of {name, amount, count, fee_rate, fail_rate})` |
| `FailureRateTable` | `components/settlements/failure_rate_table.html` | `methods (same list)` |
| `RefundPipelineRow` | `components/settlements/refund_row.html` | `refund, can_view_amounts` |
| `FeeTrackerChart` | `components/settlements/fee_tracker.html` | `months (list of {month, volume, fees, effective_rate, contracted_rate})` |
| `SettlementDrawer` | `components/settlements/drawer.html` | `settlement_id` |
| `DisputeModal` | `components/settlements/dispute_modal.html` | `settlement_id, settlement_ref` |

---

## 8. HTMX Architecture

**Page URL:** `/exec/settlements/`
**All partials:** `/exec/settlements/?part={name}`

| `?part=` | Target | Trigger | Poll | Swap |
|---|---|---|---|---|
| `summary` | `#settlement-summary` | load | Every 60s (pause on drawer/modal) | innerHTML |
| `table` | `#settlement-table` | load + filter/search change | None | innerHTML |
| `payment-split` | `#payment-split` | load + month change | None | innerHTML |
| `refunds` | `#refund-pipeline` | load + status filter change | None | innerHTML |
| `fee-tracker` | `#fee-tracker` | load | None | innerHTML |
| `settlement-drawer` | `#drawer-container` | Row click | None | innerHTML |
| `export` | — (download) | Button click | — | none |

---

## 9. Backend View & API

```python
class RazorpaySettlementView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "portal.view_settlements"

    FINANCE_ROLES = frozenset(["cfo", "finance_manager", "ceo", "superadmin"])

    def get(self, request):
        if request.user.has_role("cto") or request.user.has_role("engineer"):
            messages.warning(request, "Financial data is restricted to Finance roles.")
            return redirect("exec:dashboard")

        month_str = request.GET.get("month", now().strftime("%Y-%m"))
        can_view_amounts = request.user.role in self.FINANCE_ROLES

        if _is_htmx(request):
            part = request.GET.get("part", "")
            ctx = self._build_context(request, month_str, can_view_amounts)

            dispatch = {
                "summary":           "exec/settlements/partials/summary.html",
                "table":             "exec/settlements/partials/table.html",
                "payment-split":     "exec/settlements/partials/payment_split.html",
                "refunds":           "exec/settlements/partials/refunds.html",
                "fee-tracker":       "exec/settlements/partials/fee_tracker.html",
                "settlement-drawer": "exec/settlements/partials/drawer.html",
            }

            if part == "export":
                return self._handle_export(request, month_str)

            if part in dispatch:
                return render(request, dispatch[part], ctx)

            return HttpResponseBadRequest("Unknown part")

        ctx = self._build_context(request, month_str, can_view_amounts)
        return render(request, "exec/settlements.html", ctx)

    def _build_context(self, request, month_str, can_view_amounts):
        r = get_redis_connection()

        # Try Redis cache first
        cache_key = f"settlements:summary:{month_str}"
        cached = r.get(cache_key)
        if cached:
            summary = json.loads(cached)
        else:
            summary = self._compute_summary(month_str)
            r.setex(cache_key, 55, json.dumps(summary))

        return {
            "month": month_str,
            "summary": summary,
            "can_view_amounts": can_view_amounts,
            "can_dispute": request.user.role in {"cfo", "finance_manager", "ceo", "superadmin"},
            "status_filter": request.GET.get("status", "all"),
            "search_query": request.GET.get("q", ""),
            "page": int(request.GET.get("page", 1)),
        }

    def _compute_summary(self, month_str):
        year, month = map(int, month_str.split("-"))
        qs = RazorpaySettlement.objects.filter(
            settlement_date__year=year,
            settlement_date__month=month
        )
        return {
            "collected":  qs.aggregate(v=Sum("gross_amount"))["v"] or 0,
            "settled":    qs.filter(status="received").aggregate(v=Sum("net_amount"))["v"] or 0,
            "pending":    qs.filter(status__in=["pending", "processing"]).aggregate(v=Sum("net_amount"))["v"] or 0,
            "fees":       qs.aggregate(v=Sum("razorpay_fee"))["v"] or 0,
            "refunds":    RazorpayRefund.objects.filter(
                              created_at__year=year,
                              created_at__month=month,
                              status="settled"
                          ).aggregate(v=Sum("amount"))["v"] or 0,
        }
```

**Action endpoints:**

| Method | URL | Permission | Action |
|---|---|---|---|
| POST | `/exec/settlements/actions/flag-dispute/` | `portal.manage_settlement_disputes` | Create `SettlementDispute`, set status=disputed, optional Razorpay API call |
| GET | `/exec/settlements/?part=export&format=csv` | `portal.export_settlements` | Stream CSV via `StreamingHttpResponse` |
| GET | `/exec/settlements/?part=export&format=pdf` | `portal.export_settlements` | WeasyPrint PDF or async queue |

---

## 10. Database & Caching

**Models:**

```python
class RazorpaySettlement(models.Model):
    razorpay_settlement_id = models.CharField(max_length=64, unique=True, db_index=True)
    settlement_date        = models.DateField(db_index=True)
    payment_cycle_start    = models.DateField()
    payment_cycle_end      = models.DateField()
    payment_count          = models.IntegerField()
    gross_amount           = models.DecimalField(max_digits=14, decimal_places=2)
    razorpay_fee           = models.DecimalField(max_digits=10, decimal_places=2)
    net_amount             = models.DecimalField(max_digits=14, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[("pending","Pending"),("processing","Processing"),
                 ("received","Received"),("failed","Failed"),("disputed","Disputed")],
        db_index=True
    )
    bank_reference         = models.CharField(max_length=128, blank=True)
    razorpay_raw_response  = models.JSONField()  # full API response for audit
    created_at             = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at             = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["settlement_date", "status"]),
        ]


class RazorpayRefund(models.Model):
    razorpay_refund_id = models.CharField(max_length=64, unique=True)
    institution        = models.ForeignKey("Institution", on_delete=models.PROTECT)
    payment            = models.ForeignKey("Payment", on_delete=models.PROTECT)
    settlement         = models.ForeignKey(RazorpaySettlement, null=True, blank=True, on_delete=models.SET_NULL)
    amount             = models.DecimalField(max_digits=12, decimal_places=2)
    reason             = models.CharField(max_length=500)
    status             = models.CharField(max_length=20, choices=[...], db_index=True)
    created_at         = models.DateTimeField(auto_now_add=True, db_index=True)


class SettlementDispute(models.Model):
    settlement    = models.ForeignKey(RazorpaySettlement, on_delete=models.PROTECT)
    raised_by     = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    reason        = models.TextField()
    escalated_to_razorpay = models.BooleanField(default=False)
    created_at    = models.DateTimeField(auto_now_add=True)
    resolved_at   = models.DateTimeField(null=True)
    status        = models.CharField(max_length=20, default="open")


class SettlementFeeAudit(models.Model):
    month              = models.DateField(unique=True)  # first day of month
    volume             = models.DecimalField(max_digits=14, decimal_places=2)
    fees_paid          = models.DecimalField(max_digits=10, decimal_places=2)
    effective_rate_pct = models.DecimalField(max_digits=5, decimal_places=3)
    contracted_rate_pct= models.DecimalField(max_digits=5, decimal_places=3)
    is_over_contract   = models.BooleanField(default=False)
    alert_sent         = models.BooleanField(default=False)
```

**Celery Beat Tasks:**

```python
@app.task
def sync_razorpay_settlements():
    """Runs at 07:00 and 14:00 IST daily. Polls Razorpay Settlements API."""
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    settlements = client.settlement.all({"count": 100, "from": yesterday_epoch()})
    for s in settlements["items"]:
        RazorpaySettlement.objects.update_or_create(
            razorpay_settlement_id=s["id"],
            defaults={
                "settlement_date": epoch_to_date(s["created_at"]),
                "gross_amount": s["amount"] / 100,
                "razorpay_fee": s["fee"] / 100,
                "net_amount": (s["amount"] - s["fee"] - s["tax"]) / 100,
                "status": map_razorpay_status(s["status"]),
                "razorpay_raw_response": s,
            }
        )
    # Invalidate cache
    r = get_redis_connection()
    r.delete(f"settlements:summary:{today_month()}")
    r.delete(f"settlements:table:{today_month()}:all:1")


@app.task
def compute_settlement_fee_analysis():
    """Runs daily at 09:00 IST. Computes effective fee rate per month."""
    for month_start in last_12_month_starts():
        qs = RazorpaySettlement.objects.filter(
            settlement_date__year=month_start.year,
            settlement_date__month=month_start.month
        )
        volume = qs.aggregate(v=Sum("gross_amount"))["v"] or 0
        fees = qs.aggregate(v=Sum("razorpay_fee"))["v"] or 0
        if volume > 0:
            rate = (fees / volume * 100)
            contracted = Decimal(settings.RAZORPAY_CONTRACTED_FEE_PCT)
            over = rate > contracted
            audit, _ = SettlementFeeAudit.objects.update_or_create(
                month=month_start,
                defaults={"volume": volume, "fees_paid": fees,
                          "effective_rate_pct": rate, "contracted_rate_pct": contracted,
                          "is_over_contract": over}
            )
            if over and not audit.alert_sent:
                send_fee_overcharge_alert.delay(audit.id)
                audit.alert_sent = True
                audit.save()
```

**Redis key schema:**

| Key | Type | TTL | Purpose |
|---|---|---|---|
| `settlements:summary:2026-04` | String (JSON) | 55s | Summary KPI cards |
| `settlements:table:2026-04:all:1` | String (JSON) | 300s | Table rows (paginated) |
| `settlements:payment-split:2026-04` | String (JSON) | 300s | Donut chart data |
| `settlements:fee-tracker` | String (JSON) | 3600s | 12-month fee analysis |
| `settlement:last_received` | Hash | None (overwritten daily) | Header "last settlement" line |

---

## 11. Validation Rules

| Action | Validation |
|---|---|
| Flag Dispute | `settlement_id` must exist. `reason` required, 10–500 chars. Actor must have `portal.manage_settlement_disputes`. A settlement can only be disputed once (no duplicate disputes). |
| CSV Export | `month` must be valid `YYYY-MM`. Max range: 12 months in single export. Actor must have `portal.export_settlements`. |
| PDF Export | Same as CSV. If > 500 rows, async queue with email notification. |

---

## 12. Security Considerations

| Concern | Implementation |
|---|---|
| Financial data access | `can_view_amounts` boolean set server-side from role check — never from client parameter. Template checks `{{ can_view_amounts }}` — not a GET param the user can spoof. |
| Amount display restriction | Gross/Net/Fees columns: Django template renders "—" for non-finance roles. The value is not in the DOM (not just CSS-hidden) — cannot be extracted by inspecting HTML. |
| Razorpay API key protection | Key never exposed in any page or export. Only used server-side in Celery tasks. Stored in `settings.RAZORPAY_KEY_SECRET` (from AWS Secrets Manager). |
| Export audit | Every export triggers `AuditLog` entry: actor, timestamp, month, format. CFO cannot export data without a traceable record. |
| Dispute action audit | Every dispute flag creates `SettlementDispute` record + `AuditLog` entry. Immutable once created. |
| CSRF protection | All POST actions include CSRF token via `hx-headers`. |
| CTO redirect | View-level redirect (not just UI hiding) for engineering roles. |
| Rate limiting | Export endpoint: 5 requests/hour per user (prevents bulk data exfiltration via repeated exports). |

---

## 13. Edge Cases (System-Level)

| State | Behaviour |
|---|---|
| Razorpay API key expired | Celery sync task fails → `RazorpayAPIError` alert email to CTO + Finance Manager. Page shows "Razorpay sync failed — data may be stale" amber banner with timestamp of last successful sync. |
| Settlement T+7 overdue | Celery task detects no new settlement for > 7 business days → creates `SettlementAlert` of type `overdue`, emails CFO, shows "🔴 Settlement overdue — contact Razorpay" in page header |
| Negative net settlement | Can occur if refunds in a batch > payments. Shows red "Negative settlement: Rs.X" — this means Razorpay carried over the negative to the next batch. Banner explains this. |
| Duplicate settlement ID | `update_or_create` with `razorpay_settlement_id` as unique key prevents duplicates even if Celery task runs twice (idempotent). |
| Very large month (500+ settlements) | Table paginates normally. Export uses `StreamingHttpResponse` (CSV) or async PDF to avoid memory spikes. |
| Bank reference missing | Some settlements arrive without bank reference initially (Razorpay API delay). Row shows "Reference pending" in bank ref field, updated on next sync. |
| Month with 0 collections | Summary cards all show ₹0. No empty state error — just zero values with informational text "No payments captured in this period." |

---

## 14. Performance & Scaling

| Endpoint | Target | Critical Threshold |
|---|---|---|
| Page shell initial load | < 500ms | > 1.5s |
| `?part=summary` | < 150ms (Redis cache) | > 400ms |
| `?part=table` (page 1) | < 300ms | > 800ms |
| `?part=payment-split` | < 200ms | > 500ms |
| `?part=refunds` | < 200ms | > 500ms |
| `?part=fee-tracker` | < 100ms (Redis cache) | > 300ms |
| Settlement drawer load | < 400ms | > 1s |
| CSV export (100 rows) | < 2s | > 10s |
| CSV export (1,000 rows) | Streamed, < 5s | > 15s = async |

**Scaling notes:**
- All read endpoints are Redis-first. DB is only hit when Redis misses (TTL expired or manual cache invalidation).
- The settlement table for any single month is bounded: max ~2,400 rows/month (2,050 institutions × avg 1.2 payments). Pagination at 20 rows makes each page response trivial.
- `StreamingHttpResponse` for CSV ensures large exports don't OOM the Lambda function.
- Celery beat sync tasks run at low-traffic times (07:00, 14:00 IST) to avoid contention with exam operations.

---

*Last updated: 2026-03-20*
