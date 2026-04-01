# M-06 — Razorpay Settlements

**Route:** `GET /finance/settlements/`
**Method:** Django `TemplateView` + HTMX part-loads; server-side pagination
**Primary role:** Finance Manager (#69)
**Also sees:** Finance Analyst (#101) read-only; Billing Admin (#70) read-only; GST Consultant (#72) read-only (for TCS reconciliation)

---

## Purpose

Razorpay settlement reconciliation workspace. After a student or institution pays via Razorpay, Razorpay batches payments into settlements and transfers the net amount (after fees, GST on fees, and TCS deduction) to EduForge's bank account every T+2 to T+3 business days. Finance Manager uses this page to: (1) verify that each Razorpay payout has been correctly matched to EduForge's internal payment records, (2) investigate unmatched settlements (could be excess payments, misapplied amounts, or data sync failures), and (3) book the Razorpay fees and TCS in the accounting system. GST Consultant uses it to extract TCS data for Form 27C filings.

At ₹4Cr+ ARR, approximately 15–25 settlements per month land from Razorpay. Every unmatched rupee is revenue that isn't credited to the right institution's account — directly impacting P&L accuracy and investor reports.

---

## Data Sources

| Section | Source | Cache TTL |
|---|---|---|
| Reconciliation KPI strip | `finance_razorpay_settlement` last 30 days aggregated | 5 min |
| Settlement table | `finance_razorpay_settlement` JOIN reconciliation data | 5 min |
| Unmatched panel | `finance_razorpay_settlement` WHERE reconciliation_status='UNMATCHED' | 2 min |
| Settlement detail drawer | `finance_razorpay_settlement` + `finance_payment` rows matched to it | Live |
| Fee analysis chart | `finance_razorpay_settlement` monthly: fees_paise + tax_paise + tcs_paise | 60 min |
| Last Task M-3 sync | `finance_razorpay_settlement.created_at` MAX + task log | 5 min |

---

## URL Parameters

| Param | Values | Default | Effect |
|---|---|---|---|
| `?status` | `all`, `matched`, `unmatched`, `pending` | `all` | Filter by reconciliation_status |
| `?period` | `YYYY-MM` or range `YYYY-MM:YYYY-MM` | last 3 months | Date range for payout_date |
| `?q` | string | — | Search: Razorpay settlement ID |
| `?sort` | `payout_date_desc`, `payout_date_asc`, `amount_desc`, `unmatched_first` | `payout_date_desc` | Table sort |
| `?page` | integer ≥ 1 | `1` | Pagination |
| `?export` | `csv` | — | Export filtered settlements (FM + Analyst + GST Consultant) |

---

## HTMX Part-Load Routes

| Part | Route | Trigger | Target ID |
|---|---|---|---|
| KPI strip | `?part=kpi` | Page load + 5 min | `#settle-kpi` |
| Settlement table | `?part=table` | Filter · sort · page | `#settle-table` |
| Unmatched panel | `?part=unmatched` | Page load + 2 min poll | `#settle-unmatched` |
| Settlement drawer | `?part=drawer&id={id}` | Row click | `#settle-drawer` |
| Fee chart | `?part=fee_chart` | Page load | `#settle-fee-chart` |
| Manual match modal | `?part=match_modal&id={id}` | [Match] action | `#modal-container` |

---

## Page Layout

```
┌────────────────────────────────────────────────────────────────────┐
│  Razorpay Settlements    [Sync Now]  Last sync: 21 Mar 06:12 IST  │
├────────────────────────────────────────────────────────────────────┤
│  KPI STRIP (5 tiles)                                               │
├──────────────────────────────────────┬─────────────────────────────┤
│  SETTLEMENT TABLE (all / filter tabs)│  UNMATCHED PANEL ⚠          │
├──────────────────────────────────────┴─────────────────────────────┤
│  FEE ANALYSIS CHART (12 months — Razorpay fees + TCS trend)        │
└────────────────────────────────────────────────────────────────────┘
```

---

## KPI Strip (5 tiles)

```
┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│ ₹38.4L   │ │ 15       │ │ 3        │ │ ₹1.92L   │ │ ₹18,480  │
│ Net Rcvd │ │ Settlements│ Unmatched│ │ Razorpay │ │ TCS      │
│ (last30d)│ │ (last 30d)│ (₹2.1L)  │ │ Fees     │ │ Deducted │
│ 12 matched│ │          │ ⚠         │ │ (~0.5%)  │ │ (0.1%)   │
└──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘
```

- **Tile 1 (Net Received):** SUM `finance_razorpay_settlement.net_paise` WHERE payout_date in last 30 days. "Net" = gross - fees - tax. Sub-label: N settlements matched.
- **Tile 2 (Settlement Count):** Total settlements received in period.
- **Tile 3 (Unmatched):** COUNT and SUM of UNMATCHED settlements. Amber tile if > 0. Red if > 5. [Reconcile →] quick link to unmatched panel.
- **Tile 4 (Razorpay Fees):** SUM `fees_paise` + `tax_paise`. % of gross shown: "~0.5%" (Razorpay charges ~1.9–2.36% but EduForge may negotiate lower for B2B volumes).
- **Tile 5 (TCS Deducted):** SUM `tcs_paise`. TCS = Tax Collected at Source (1% deducted by Razorpay per IT Act Section 194-O for marketplace payments). GST Consultant uses this for Form 27C and claiming TCS credit.

---

## Settlement Table

25 rows per page, sorted by `payout_date DESC` by default.

| Column | Width | Description |
|---|---|---|
| Settlement ID | 160px | Razorpay settlement ID (e.g., setl_Ixxxxxx); monospace; click → drawer |
| Payout Date | 100px | Date Razorpay transferred to EduForge bank account |
| Gross (₹) | 110px | `amount_paise` right-aligned monospace |
| Fees (₹) | 90px | `fees_paise + tax_paise` (Razorpay fee + GST on fee) |
| TCS (₹) | 80px | `tcs_paise` |
| Net Received (₹) | 110px | `net_paise`; right-aligned bold |
| Payments Matched | 100px | COUNT of `finance_payment` linked to this settlement |
| Reconciliation | 130px | AUTO_MATCHED=green · MANUALLY_MATCHED=teal · UNMATCHED=red · PENDING=amber badge |
| Reconciled By | 100px | Actor name (system / user avatar) |
| Actions | 48px | 3-dot menu |

**UNMATCHED rows:** Red left border + faint `bg-red-950` tint. Tooltip: "This settlement has not been matched to internal payment records. Click [Match] to resolve."

**PENDING rows:** Settlement received from Razorpay but payout not yet credited to bank. Amber row tint.

---

### Kebab Menu Actions

| Action | Condition | Role |
|---|---|---|
| View Settlement Details | Always | All |
| Match to Payments | UNMATCHED | FM (#69), Billing Admin (#70) |
| Download Razorpay Report | Always | FM (#69) — CSV of raw Razorpay settlement data: settlement_id, payout_date, gross, fees, tax_on_fees, tcs, net, status; optional `?format=json` for JSON |
| Mark as Reviewed | AUTO_MATCHED | FM (#69) |
| Export Settlement CSV | Always | FM (#69), Analyst (#101), GST Consultant (#72) |

---

## Settlement Detail Drawer (640px)

```
┌──────────────────────────────────────────────────────────────────┐
│  setl_I29xKFRkRO7Bgt  ·  AUTO_MATCHED                [Close ×]   │
├──────────────────────────────────────────────────────────────────┤
│  SETTLEMENT SUMMARY                                              │
│  Payout Date:  15 Mar 2026                                       │
│  Gross:        ₹3,84,200   Fees: ₹7,684   Tax on fees: ₹1,383   │
│  TCS:          ₹3,842      Net:  ₹3,71,291                       │
│  Status:       SETTLED (credited to HDFC Current A/c **1234)     │
├──────────────────────────────────────────────────────────────────┤
│  MATCHED PAYMENTS (3)                                            │
│  pay_IxxxxA  Delhi Coaching Hub  ₹1,77,000  15 Mar  CAPTURED     │
│  pay_IxxxxB  KIMS School          ₹84,960   15 Mar  CAPTURED     │
│  pay_IxxxxC  Victory College      ₹1,22,240  15 Mar  CAPTURED     │
│  Total matched: ₹3,84,200 ✓ (equals gross)                       │
├──────────────────────────────────────────────────────────────────┤
│  TAX BREAKDOWN (for accounting)                                  │
│  Razorpay fee excl. GST:  ₹7,684                                 │
│  GST on Razorpay fee:     ₹1,383  (18% on ₹7,684)               │
│  TCS (194-O, 1%):         ₹3,842  (claimable in advance tax)     │
│  Net settlement:          ₹3,71,291                              │
├──────────────────────────────────────────────────────────────────┤
│  RECONCILIATION LOG                                              │
│  15 Mar 06:14 — AUTO_MATCHED by Task M-3                         │
└──────────────────────────────────────────────────────────────────┘
```

**Matched Payments section:** Each `finance_payment` linked to this settlement. Shows Razorpay payment_id, institution name (linked to M-03 invoice), amount, date, capture status. Total matched vs gross: must equal exactly (any difference = UNMATCHED reason).

**For UNMATCHED settlements:** Matched Payments section shows "0 payments matched. ₹X.XL unaccounted." [Match Manually] button opens the match modal.

---

## Manual Match Modal (560px)

For UNMATCHED settlements — allows Finance Manager or Billing Admin to manually link Razorpay payments to this settlement.

```
┌─────────────────────────────────────────────────────────────────┐
│  Match Settlement setl_Ixxxx                                    │
│  Settlement Gross: ₹2,12,400                                    │
├─────────────────────────────────────────────────────────────────┤
│  Search Razorpay payments to match:                             │
│  [🔍 Search by payment ID, institution, amount...]              │
│                                                                 │
│  ☐  pay_IxxxxD  Sunrise Academy   ₹1,18,000  14 Mar  CAPTURED   │
│  ☐  pay_IxxxxE  Excel Institute   ₹84,960    14 Mar  CAPTURED   │
│  ☐  pay_IxxxxF  Alpha School      ₹9,440     14 Mar  CAPTURED   │
│                                                                 │
│  Selected: ₹2,12,400  ✓ Matches settlement gross               │
├─────────────────────────────────────────────────────────────────┤
│  Match reason*  [Payment sync delay — matched manually  ]       │
├─────────────────────────────────────────────────────────────────┤
│  [Cancel]                          [Confirm Manual Match]       │
└─────────────────────────────────────────────────────────────────┘
```

- Search: finds `finance_payment` records WHERE settlement_id IS NULL AND status='CAPTURED' AND amount matches ±5% of settlement amount
- Checkboxes: multi-select; running total shown; [Confirm] enabled only when selected total = settlement gross ± ₹0 (exact match, zero tolerance — no rounding permitted). If payments don't sum exactly to settlement gross, the user must find the missing/extra transaction rather than accepting a partial match.
- Match reason: required; max 500 chars; stored in `finance_razorpay_settlement.notes`
- On confirm: PATCH `/finance/settlements/{id}/match/`. Sets `reconciliation_status=MANUALLY_MATCHED`, `reconciled_by_id`, `reconciled_at`. Links payment records to this settlement. Writes audit log.

---

## Unmatched Panel

Prominent fixed panel (right column on desktop, below table on mobile) showing all UNMATCHED settlements.

```
┌────────────────────────────────────────────────┐
│  Unmatched Settlements (3 · ₹2.1L)  ⚠          │
│  ────────────────────────────────────────────  │
│  setl_Ixxxx1  ₹84,960   13 Mar   [Match]       │
│  setl_Ixxxx2  ₹1,03,333  12 Mar  [Match]       │
│  setl_Ixxxx3  ₹1,18,000  10 Mar  [Match]       │
│  ────────────────────────────────────────────  │
│  ⚠ Unmatched settlements affect P&L accuracy.  │
└────────────────────────────────────────────────┘
```

Auto-refreshes every 2 minutes. Amber panel border if count > 0. Red border if count > 5. [Match] opens the manual match modal.

**Empty state:** "All settlements matched." green panel with checkmark.

---

## Fee Analysis Chart (12 months)

Line chart showing Razorpay cost breakdown over 12 months.

- **Solid orange line:** Monthly Razorpay fees (fees_paise + tax_paise)
- **Dashed orange line:** Monthly TCS deducted
- **Solid grey line:** Fee % of gross (right Y-axis, %) — should stay below 2.5%
- X-axis: month labels; Y-axis left: ₹L; right: %
- Hover: gross · fees · TCS · net · effective fee rate %
- **Annotation:** Arrow pointing to any month where fee rate > 2.5%: "Fee rate spike — check Razorpay pricing tier"

GST Consultant (#72) uses this chart to verify TCS amounts for quarterly Form 27C filing.

---

## [Sync Now] Button

Manual trigger for Task M-3 (Razorpay settlement sync). Available to FM (#69) only.

- Click: POST `/finance/settlements/sync/` → queues Celery task. Immediate response: amber toast "Settlement sync triggered — check back in 2–3 minutes." `hx-swap="none"`.
- On task completion: Django Channels pushes a notification "Sync complete: N settlements fetched, N auto-matched, N unmatched." Unmatched panel auto-refreshes.
- Rate limit: max 3 manual syncs per day (guard: `finance_config['settlement_sync_manual_count_today']`). Beyond that: "Maximum manual syncs (3) reached for today. Automatic sync runs at 6:00 AM IST."

---

## Export CSV

**Columns (14):** settlement_id, payout_date, gross_inr, fees_inr, tax_on_fees_inr, tcs_inr, net_inr, reconciliation_status, payments_matched_count, reconciled_by, reconciled_at, notes, created_at

**Available to:** FM (#69), Finance Analyst (#101), GST Consultant (#72). Billing Admin (#70) read-only — no export.

---

## Empty States

| Condition | Message |
|---|---|
| No settlements in period | "No settlements found for the selected period." |
| Unmatched panel: all matched | "All settlements matched." with green checkmark |
| No settlements at all | "No Razorpay settlements synced yet. Click [Sync Now] to fetch latest data." |

---

## Toast Messages

| Action | Toast | Type |
|---|---|---|
| Manual match confirmed | "Settlement setl_Ixxxx manually matched. Reconciliation updated." | Green |
| Sync triggered | "Settlement sync triggered — check back in 2–3 minutes." | Amber |
| Sync complete (via push) | "Sync complete: N settlements fetched, N matched, N unmatched." | Green or Amber |
| Rate limit hit | "Maximum manual syncs (3) reached today. Auto-sync at 6:00 AM IST." | Amber |
| Export downloaded | "Settlement data exported." | Green |

---

## Authorization

**Route guard:** `@division_m_required(allowed_roles=[69, 70, 72, 101])`.

| Scenario | Behaviour |
|---|---|
| Finance Manager (#69) | Full; [Sync Now]; match; mark reviewed |
| Billing Admin (#70) | Read + match UNMATCHED settlements; no export; no [Sync Now] |
| GST Consultant (#72) | Read-only; export (for TCS data); TCS breakdown visible |
| Finance Analyst (#101) | Read-only; export; fee analysis chart |
| Manual match POST by Billing Admin without FM | Allowed for UNMATCHED; audit logged |

---

## Role-Based UI Visibility Summary

| Element | 69 FM | 70 Billing | 72 GST | 101 Analyst |
|---|---|---|---|---|
| KPI strip (all 5) | Yes | Tiles 1–3 | TCS tile only | All (read) |
| Settlement table | Full | Full (read) | Full (read) | Full (read) |
| Unmatched panel | Yes + [Match] | Yes + [Match] | No | Yes (read) |
| Match modal | Yes | Yes | No | No |
| Fee analysis chart | Yes | No | Yes (TCS focus) | Yes |
| [Sync Now] | Yes | No | No | No |
| Export CSV | Yes | No | Yes | Yes |
| [Mark as Reviewed] | Yes | No | No | No |

---

## Performance Requirements

| Metric | Target | Notes |
|---|---|---|
| Initial page load (SSR) | < 2s P95 | KPI strip + table from cache; unmatched panel live |
| KPI strip | < 500ms P95 (cache hit) | 5-min TTL |
| Settlement table (25 rows) | < 400ms P95 (cache hit) | 5-min TTL |
| Unmatched panel | < 300ms P95 (cache hit) | 2-min TTL; auto-refresh |
| Settlement detail drawer (live) | < 400ms P95 | `finance_razorpay_settlement` + matched `finance_payment` rows |
| Fee analysis chart | < 800ms P95 (cache hit) | 60-min TTL; 12-month aggregation |
| Manual match modal search | < 500ms | Filtered `finance_payment` WHERE settlement_id IS NULL AND CAPTURED |
| [Sync Now] trigger | < 300ms (queue response) | Celery task queued; real result via Django Channels push |
| CSV export | < 2s for ≤ 500 rows | Streaming response |

---

## Keyboard Shortcuts

| Key | Action |
|---|---|
| `g` `t` | Go to Razorpay Settlements (M-06) |
| `r` | Trigger [Sync Now] (FM only) |
| `/` | Focus settlement ID search |
| `e` | Export CSV (FM, Analyst, GST Consultant) |
| `←` / `→` | Previous / next page in settlement table |
| `Esc` | Close open drawer or modal |
| `?` | Show keyboard shortcut help overlay |

