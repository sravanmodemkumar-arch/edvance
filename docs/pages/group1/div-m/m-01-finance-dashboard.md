# M-01 — Finance Dashboard

**Route:** `GET /finance/`
**Method:** Django `TemplateView` + HTMX part-loads
**Primary roles:** Finance Manager (#69), Finance Analyst (#101)
**Also sees (restricted strips):** Billing Admin (#70) — billing strip; AR Exec (#71) — overdue/AR strip; GST Consultant (#72) — GST calendar strip; Refund Processing Exec (#73) — refund queue strip; Pricing Admin (#74) — plan performance strip; Collections Exec (#102) — collections strip

---

## Purpose

Central command view for the Finance division. Finance Manager uses this as the morning briefing screen — ARR/MRR health, collection rate, outstanding overdue balance, settlement reconciliation status, refund queue depth, and upcoming GST deadlines in a single viewport. Finance Analyst uses it to spot anomalies before building reports. Other roles see only the strips relevant to their function, eliminating the need to context-switch to M-03/M-05/M-08 for daily status checks.

---

## Data Sources

| Section | Source | Cache TTL |
|---|---|---|
| KPI strip | `analytics_revenue` last complete month + `finance_ar_aging` totals + `finance_refund` pending count | 5 min |
| ARR trend chart | `analytics_revenue` monthly for last 12 months WHERE segment='all' AND plan_tier='all' | 60 min |
| Revenue by segment chart | `analytics_revenue` monthly for last 12 months grouped by segment | 60 min |
| Billing vs Collections chart | `analytics_revenue` GROUP BY month: invoiced_paise vs collected_paise | 30 min |
| Top 10 overdue | `finance_ar_aging` JOIN `institution` ORDER BY total_outstanding_paise DESC LIMIT 10 | 5 min |
| Upcoming due invoices | `finance_invoice` WHERE status IN ('SENT') AND due_date BETWEEN today AND today+14d | 5 min |
| Settlement status | `finance_razorpay_settlement` WHERE payout_date >= today-7d grouped by reconciliation_status | 5 min |
| Refund queue | `finance_refund` WHERE status='PENDING_REVIEW' ORDER BY created_at ASC LIMIT 8 | 2 min |
| GST calendar | `finance_gst_return` WHERE due_date >= today ORDER BY due_date ASC LIMIT 5 | 60 min |
| Plan performance strip | `analytics_revenue` latest month breakdown by plan_tier | 30 min |

Cache keys scoped to `(user_id, period, segment)`. `?nocache=true` bypasses Memcached for FM (#69) and Analyst (#101) only.

---

## URL Parameters

| Param | Values | Default | Effect |
|---|---|---|---|
| `?period` | `this_month`, `last_month`, `this_quarter`, `last_quarter`, `ytd` | `last_month` | Reporting window for KPI strip and charts |
| `?segment` | `all`, `school`, `college`, `coaching`, `group` | `all` | Filters charts and overdue table to one institution type |
| `?nocache` | `true` | — | Bypass Memcached (FM #69 + Analyst #101 only) |

---

## HTMX Part-Load Routes

| Part | Route | Trigger | Auto-Refresh | Target ID |
|---|---|---|---|---|
| KPI strip | `?part=kpi` | Page load + period/segment change | 5 min | `#m-kpi-strip` |
| ARR trend | `?part=arr_trend` | Page load + period change | 60 min | `#m-arr-trend` |
| Revenue by segment | `?part=rev_segment` | Page load + period/segment change | 60 min | `#m-rev-segment` |
| Billing vs Collections | `?part=billing_collections` | Page load + period change | 30 min | `#m-billing-collections` |
| Top 10 overdue | `?part=overdue_table` | Page load | 5 min | `#m-overdue-table` |
| Upcoming due | `?part=upcoming_due` | Page load | 5 min | `#m-upcoming-due` |
| Settlement status | `?part=settlement_status` | Page load | 5 min | `#m-settlement-status` |
| Refund queue | `?part=refund_queue` | Page load | 2 min | `#m-refund-queue` |
| GST calendar | `?part=gst_calendar` | Page load | 60 min | `#m-gst-calendar` |
| Plan performance | `?part=plan_perf` | Page load | 30 min | `#m-plan-perf` |

All parts respond with HTML fragments only. `hx-push-url="true"` keeps URL in sync with period/segment filters.

---

## Page Layout

```
┌────────────────────────────────────────────────────────────────────┐
│  Finance Dashboard   Period: [Last Month ▼]  Segment: [All ▼]      │
├────────────────────────────────────────────────────────────────────┤
│  KPI STRIP (5 tiles)                                               │
├──────────────────────────────┬─────────────────────────────────────┤
│  ARR TREND (12 months, line) │  REVENUE BY SEGMENT (stacked bar)  │
├──────────────────────────────┴─────────────────────────────────────┤
│  BILLING VS COLLECTIONS (grouped bar, 12 months)                   │
├────────────────────┬───────────────────────┬───────────────────────┤
│  TOP 10 OVERDUE    │  UPCOMING DUE (14d)   │  SETTLEMENT STATUS    │
├────────────────────┴───────────────────────┴───────────────────────┤
│  REFUND QUEUE (pending)        │  GST FILING CALENDAR             │
└────────────────────────────────┴──────────────────────────────────┘
```

> Non-FM/Analyst roles see only their relevant strip(s) — the rest of the page is hidden.

---

## Components

### KPI Strip (5 tiles)

```
┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ ₹4.2Cr       │ │ ₹35.1L       │ │ 96.8%        │ │ ₹12.4L       │ │ 7            │
│ Total ARR    │ │ MRR          │ │ Collection   │ │ Overdue      │ │ Pending      │
│              │ │ (×12=₹4.2Cr) │ │ Rate         │ │ Balance      │ │ Refunds      │
│ ↑+₹18L MTD  │ │ ↑+₹1.2L MoM  │ │ ↑+0.3 pts    │ │ 63 insts.    │ │ ₹4.8L total  │
└──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘
```

**Tile 1 — Total ARR:** `analytics_revenue.arr_paise` WHERE segment='all' AND plan_tier='all' for the selected period. Formatted ₹X.XCr. Delta shows new_arr + expansion - contraction - churn vs previous period (`↑+₹18L` = net new ARR this month). Green if positive, red if negative. Tooltip: breakdown by plan tier (Starter/Standard/Professional/Enterprise). Clicking opens M-02.

**Tile 2 — MRR:** `analytics_revenue.mrr_paise` for the selected month. Sub-label: "×12 = ₹X.XCr run rate". Delta vs previous month. Green if increasing. Guard: if period is a quarter or YTD, shows the last complete month's MRR with a note "(as of [month])".

**Tile 3 — Collection Rate:** `(analytics_revenue.collected_paise / analytics_revenue.invoiced_paise) × 100` for the period. Formatted to 1 decimal. Target ≥ 96%. Green ≥ 96%, amber 90–95.9%, red < 90%. Delta vs previous period. Guard: if invoiced_paise = 0 (first month), shows "— (no invoices)" in grey. Clicking opens M-03?status=overdue.

**Tile 4 — Overdue Balance:** `SUM(finance_ar_aging.total_outstanding_paise)` across all institutions. Sub-label: "N institutions". Red if > ₹20L. Delta vs last Task M-1 run. Clicking opens M-05.

**Tile 5 — Pending Refunds:** `COUNT(finance_refund) WHERE status='PENDING_REVIEW'`. Sub-label: "₹X.XL total requested". Amber if > 5, red if > 15. Clicking opens M-07.

**Loading state:** Tiles show animated grey shimmer while HTMX partial loads. On auto-refresh failure, tiles retain stale values with a subtle grey border and "↻ Retry" link.

**Role-based tile behaviour:**
- Billing Admin (#70): Tile 1 (read) + Tile 4 (overdue, links to M-03?status=overdue). Tiles 2, 3, 5 hidden.
- AR Exec (#71): Tile 4 only.
- Refund Exec (#73): Tile 5 only.
- Pricing Admin (#74): Tile 1 (ARR) + Tile 2 (MRR). Tiles 3, 4, 5 hidden.
- Collections Exec (#102): Tile 4 only (scoped to their assigned institutions).
- GST Consultant (#72): No KPI tiles (they get the GST calendar strip directly).

---

### ARR Trend Chart

Line chart (Chart.js) — 12 months of monthly ARR.

- **Lines:** ARR (solid blue-500), MRR×12 run-rate (dashed blue-300), Target ARR (dashed amber-400 — from `finance_config['arr_target_paise']` or configurable in M-09)
- **X-axis:** month labels (MMM YY), last 12 months
- **Y-axis:** ₹ in lakhs (auto-scaled). Secondary Y-axis for MRR if range differs significantly.
- **Reference line:** horizontal dashed line at ₹18Cr (ARR milestone for Phase 3)
- **Area fill:** soft blue-900 fill under ARR line to make visual trend clear
- **Hover tooltip:** ARR · MRR run-rate · new ARR this month · churned ARR · net change
- **Null months:** broken line (insufficient data in early months)
- **Period selector:** clicking a bar on the chart sets the dashboard period filter to that month (`hx-push-url`)

**Finance Analyst (#101):** Additional toggle "Show NRR overlay" — adds a secondary Y-axis (right, green) showing NRR% per month (computed from `analytics_revenue` waterfall fields).

---

### Revenue by Segment Chart

Stacked bar chart (Chart.js) — 12 months, stacked by institution type.

- **Bars stacked:** School=blue-400 · College=violet-400 · Coaching=orange-400 · Group=teal-400
- **X-axis:** month labels
- **Y-axis:** ₹ in lakhs
- **Hover tooltip:** exact breakdown per segment for that month, total ARR
- **Legend toggle:** click a segment in the legend to show/hide that segment's bar component
- **Segment filter:** respects `?segment` URL param — when a specific segment is selected, that segment's bars are highlighted and others are muted.

---

### Billing vs Collections Chart

Grouped bar chart — 12 months showing billed amount vs collected amount side by side.

```
₹ (L)
 45 │     ┌──┐           ┌──┐
 40 │ ┌──┐│  │       ┌──┐│  │
 35 │ │  ││  │   ┌──┐│  ││  │
 30 │ │  ││  │ ┌─│──││──││──│
    │ │B ││C │ │B│  ││C ││B ││C │
     Oct   Nov   Dec   Jan   Feb
    [■ Billed]  [■ Collected]  --- 96% target line
```

- **Blue bars:** monthly billed (invoiced_paise)
- **Green bars:** monthly collected (collected_paise)
- **Gap between bars** = outstanding that month
- **Dashed reference line** at 96% collection rate computed per bar height
- **Hover tooltip:** billed · collected · collection rate % · outstanding amount
- **Red highlight** on any bar pair where collection rate < 90%

---

### Top 10 Overdue Institutions

Table showing the 10 institutions with the highest outstanding balance (from `finance_ar_aging`).

| Column | Description |
|---|---|
| Institution | Name (link → M-05?institution_id=X) + type badge |
| Overdue Balance | `total_outstanding_paise` formatted ₹X.XL; red if > ₹5L |
| Age | `oldest_invoice_days` days; amber if 31–60d, red if 61–90d, dark red if 90+ |
| 31–60d | `bucket_31_60_paise` |
| 61–90d | `bucket_61_90_paise` |
| 90+ days | `bucket_91plus_paise`; red text if > 0 |
| Last Follow-up | `finance_ar_followup.created_at` most recent for this institution. "Never" in red if no follow-up exists and invoice > 14 days overdue |
| Assigned To | AR Exec or Collections Exec avatar (from `finance_ar_aging.assigned_collector_id`) |
| Actions | [Log Follow-up] (AR Exec + Collections Exec); [Suspend Account] (Collections Exec + FM) |

**[View All Overdue →]** links to M-05.

**Segment filter:** respects `?segment` param.

**Role visibility:** FM (#69) and Analyst (#101) see all columns. AR Exec (#71) sees all but [Suspend Account]. Collections Exec (#102) sees own assigned institutions only; cannot see institutions assigned to AR Exec.

---

### Upcoming Due (14 Days)

Compact list of invoices due in the next 14 days (status='SENT').

```
  Delhi Coaching Hub       ₹1,18,000     Due: 22 Mar (in 1d)   [Send Reminder]
  Victory College          ₹42,480       Due: 25 Mar (in 4d)   —
  KIMS School Group        ₹2,34,000     Due: 28 Mar (in 7d)   —
  [View all upcoming →]
```

- Red row if due in ≤ 1 day
- Amber row if due in 2–3 days
- [Send Reminder] button available for Billing Admin (#70) only; AR Exec (#71) can also trigger
- [View all upcoming →] links to M-03?status=sent&due_before=+14d

**Empty state:** "No invoices due in the next 14 days."

---

### Settlement Status

Three-tile summary of Razorpay settlement reconciliation (last 7 days).

```
┌────────────────────┐  ┌────────────────────┐  ┌────────────────────┐
│ 12 matched         │  │ 3 unmatched         │  │ 1 pending          │
│ ₹38.4L             │  │ ₹2.1L  ⚠           │  │ ₹8.2L (in transit) │
│ AUTO + MANUAL      │  │ [Reconcile →]       │  │ Awaiting payout    │
└────────────────────┘  └────────────────────┘  └────────────────────┘
```

- Matched = AUTO_MATCHED + MANUALLY_MATCHED count and sum
- Unmatched = UNMATCHED count and sum; amber tile border if > 0; red if > 5
- Pending = settlements in RAZORPAY status 'pending' (not yet paid out)
- [Reconcile →] links to M-06
- "Last sync: [Task M-3 last_run_at]" sub-label; amber if > 26 hours ago

**Visible to:** FM (#69), Analyst (#101), Billing Admin (#70) read-only.

---

### Refund Queue

Compact list of `finance_refund` WHERE status='PENDING_REVIEW', oldest first (max 8 rows).

```
  Sunrise Academy         ₹12,000   BILLING_ERROR   3d ago   [Review]  ⚑ FM approval required
  Excel Coaching Hub      ₹4,800    DUPLICATE_PAYMENT 1d ago [Review]
  Delhi Public School     ₹6,000    GOODWILL          5h ago [Review]
  [View all refunds →]
```

- Rows where `approval_required=true` (> ₹10K) show a red flag icon — FM (#69) must approve
- Age shown in relative time; red if > 7 days pending
- [Review] links to M-07 refund detail drawer
- **Visible to:** FM (#69) full; Refund Exec (#73) full; Billing Admin (#70) read-only (no [Review] action)

**Empty state:** "Refund queue is clear." with green checkmark icon.

---

### GST Filing Calendar

Next 5 upcoming GST deadlines from `finance_gst_return`:

```
  GSTR-1   Jan 2026   Due: 11 Feb (in 3d)    UPCOMING  [View →]
  GSTR-3B  Jan 2026   Due: 20 Feb (in 12d)   UPCOMING  [View →]
  GSTR-1   Feb 2026   Due: 11 Mar (in 31d)   UPCOMING  —
  GSTR-3B  Feb 2026   Due: 20 Mar (in 40d)   UPCOMING  —
  GSTR-9   FY 2024-25 Due: 31 Dec (in 285d)  UPCOMING  —
```

- Red row if due in ≤ 3 days (high urgency)
- Amber row if due in 4–7 days
- OVERDUE rows shown with red "OVERDUE" badge and pulsing red dot
- FILED rows shown with green "FILED" badge and ARN number
- [View →] links to M-08 with that return_type + period pre-filtered
- **Visible to:** GST Consultant (#72) full; FM (#69) and Analyst (#101) read-only.

**Empty state:** (cannot happen — there are always future GST deadlines.)

---

### Plan Performance Strip *(Pricing Admin #74 + FM #69 + Analyst #101)*

Four compact tiles showing subscription count and ARR per plan tier for the current month.

```
┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐
│ Starter    │ │ Standard   │ │ Professional│ │ Enterprise │
│ 312 insts  │ │ 890 insts  │ │ 743 insts  │ │ 105 insts  │
│ ₹78L ARR   │ │ ₹5.3Cr ARR │ │ ₹14.9Cr    │ │ ₹23.8Cr    │
│ ↑+4 MoM    │ │ ↓-2 MoM    │ │ ↑+8 MoM    │ │ ↑+1 MoM    │
└────────────┘ └────────────┘ └────────────┘ └────────────┘
```

Delta shows net subscription count change vs previous month. Clicking any tile links to M-04?tier=<tier>.

---

## Empty States

| Section | Condition | Message |
|---|---|---|
| Top 10 Overdue | All institutions current (no overdue) | "No overdue balances — 100% collection rate this period!" with green shield icon |
| Upcoming Due | No invoices due in next 14 days | "No invoices due in the next 14 days." |
| Settlement Status — Unmatched | All settlements reconciled | "All settlements matched." with green checkmark |
| Refund Queue | No pending refunds | "Refund queue is clear." with green checkmark |

---

## Toast Messages

| Action | Toast | Type |
|---|---|---|
| Period filter changed | "Dashboard updated to [period]." | Blue (info) |
| Segment filter changed | "Showing [segment] institutions." | Blue (info) |
| `?nocache=true` used | "Cache bypassed — showing live financial data." | Blue (info) |
| Task M-3 sync result (real-time via Django Channels) | "Settlement sync: N matched, N unmatched. [View →]" | Green or Amber |
| Refund approved (real-time) | "Refund of ₹[amount] for [institution] approved by Finance Manager." | Green |
| New overdue invoice created (Task M-1) | "[institution] invoice INV-XXXXX is now overdue (N days)." | Amber |

---

## Authorization

**Route guard:** `@division_m_required(allowed_roles=[69, 70, 71, 72, 73, 74, 101, 102])` applied to `FinanceDashboardView`.

| Scenario | Behaviour |
|---|---|
| Unauthenticated | Redirect to `/login/?next=/finance/` |
| Role not in allowed list | 403 redirect to `/403/` |
| Analyst (#101) — `?nocache=true` | Allowed; bypasses Memcached |
| Collections Exec (#102) — Top 10 Overdue | Queryset filtered to `WHERE assigned_collector_id = request.user.id` |
| All HTMX partial routes | Same role enforcement; direct calls without session return 403 |

---

## Role-Based UI Visibility Summary

| Element | 69 FM | 101 Analyst | 70 Billing | 71 AR Exec | 72 GST | 73 Refund | 74 Pricing | 102 Collections |
|---|---|---|---|---|---|---|---|---|
| KPI strip — ARR/MRR tiles | Yes | Yes | Tiles 1+4 | Tile 4 only | None | Tile 5 only | Tiles 1+2 | Tile 4 (own) |
| KPI strip — Collection Rate | Yes | Yes | Yes (read) | No | No | No | No | No |
| ARR trend chart | Yes | Yes (+ NRR toggle) | No | No | No | No | Yes (read) | No |
| Revenue by segment chart | Yes | Yes | No | No | No | No | Yes (read) | No |
| Billing vs Collections chart | Yes | Yes | Yes (read) | Yes (read) | No | No | No | No |
| Top 10 Overdue table | Yes — all | Yes — all (read) | Yes | Yes | No | No | No | Own assigned only |
| Upcoming Due invoices | Yes | Yes | Yes + [Send Reminder] | Yes | No | No | No | No |
| Settlement status tiles | Yes | Yes | Yes (read) | No | Yes (TCS view) | No | No | No |
| Refund queue | Yes (full + approve) | Yes (read) | Yes (read) | No | No | Yes (full) | No | No |
| GST calendar | Yes (read) | Yes (read) | No | No | Yes (full) | No | No | No |
| Plan performance strip | Yes | Yes | No | No | No | No | Yes | No |
| [?nocache=true] | Yes | Yes | No | No | No | No | No | No |

---

## Performance Requirements

| Metric | Target | Notes |
|---|---|---|
| Initial page load (SSR) | < 2s P95 | All 9 HTMX strips issued in parallel; each strip fetches independently |
| KPI strip (each tile) | < 500ms P95 (cache hit) | 5-min Memcached TTL; first hit after expiry < 3s |
| ARR trend chart data | < 800ms P95 (cache hit) | 60-min TTL |
| Top 10 overdue table | < 400ms P95 | 5-min TTL; direct `finance_ar_aging` aggregation |
| `?nocache=true` full rebuild | < 10s | FM / Analyst only; all 9 parts re-fetched from DB |
| Concurrent users | Up to 20 simultaneous finance staff | No degradation expected; all heavy reads are cached |

---

## Keyboard Shortcuts

| Key | Action |
|---|---|
| `g` `f` | Go to Finance Dashboard (M-01) |
| `g` `i` | Go to Billing Invoices (M-03) |
| `g` `s` | Go to Subscriptions (M-04) |
| `g` `r` | Go to Revenue & P&L (M-02) |
| `/` | Focus search (if search input present on active strip) |
| `Esc` | Close open drawer or modal |
| `?` | Show keyboard shortcut help overlay |

