# M-07 — Refund Queue

**Route:** `GET /finance/refunds/`
**Method:** Django `TemplateView` + HTMX part-loads; server-side pagination
**Primary role:** Refund Processing Exec (#73)
**Also sees:** Finance Manager (#69) full + approve > ₹10K; Billing Admin (#70) read-only + create requests

---

## Purpose

Refund lifecycle management workspace. Refunds originate from: (1) institution cancels subscription mid-cycle, (2) billing error (duplicate charge, wrong plan), (3) duplicate payment (institution paid twice), (4) goodwill credit after a major incident. Billing Admin (#70) or Finance Manager (#69) creates a refund request. Refund Processing Exec (#73) validates eligibility against policy, processes refunds under ₹10K via Razorpay API directly, and escalates refunds over ₹10K for Finance Manager approval first. Finance Manager approves high-value refunds and can directly process any refund.

At scale: ~5–15 refund requests per month. Total refund volume: ₹50K–₹5L per month. Every Razorpay refund must be tracked with its `refund_id` to ensure the credit reaches the institution's payment instrument.

---

## Data Sources

| Section | Source | Cache TTL |
|---|---|---|
| KPI strip | `finance_refund` aggregated by status (last 30 days) | 2 min |
| Refund table | `finance_refund` JOIN `institution` JOIN `finance_payment` JOIN auth_user | 2 min |
| Tab counts | `finance_refund` GROUP BY status | 2 min |
| Refund detail drawer | `finance_refund` + original `finance_payment` + `finance_invoice` | Live |

---

## URL Parameters

| Param | Values | Default | Effect |
|---|---|---|---|
| `?status` | `all`, `pending_review`, `approved`, `rejected`, `processing`, `processed`, `failed` | `pending_review` | Pre-selects tab; filters table |
| `?period` | `YYYY-MM` or range | last 3 months | Filter by created_at |
| `?q` | string ≥ 2 chars | — | ILIKE on institution_name, refund ID, Razorpay payment ID |
| `?approval` | `required`, `not_required` | — | Filter by approval_required field |
| `?sort` | `created_asc`, `created_desc`, `amount_desc`, `amount_asc` | `created_asc` | Table sort (oldest pending first) |
| `?page` | integer ≥ 1 | `1` | Pagination |

---

## HTMX Part-Load Routes

| Part | Route | Trigger | Target ID |
|---|---|---|---|
| KPI strip | `?part=kpi` | Page load + 2 min poll | `#ref-kpi` |
| Refund table | `?part=table` | Tab click · filter · sort · page | `#ref-table` |
| Tab counts | `?part=tab_counts` | After status change | `#ref-tabs` |
| Refund drawer | `?part=drawer&id={id}` | Row click | `#ref-drawer` |
| Create modal | `?part=create_modal` | [+ Request Refund] | `#modal-container` |
| Review modal | `?part=review_modal&id={id}` | [Approve/Reject] | `#modal-container` |
| Process modal | `?part=process_modal&id={id}` | [Process Refund] | `#modal-container` |

---

## Page Layout

```
┌────────────────────────────────────────────────────────────────┐
│  Refund Queue                          [+ Request Refund]      │
├────────────────────────────────────────────────────────────────┤
│  KPI STRIP (5 tiles)                                           │
├────────────────────────────────────────────────────────────────┤
│  [Pending Review(7)] [Approved(2)] [Processing(1)] [Processed(38)]│
│  [Failed(1)] [Rejected(3)]                                     │
├────────────────────────────────────────────────────────────────┤
│  [🔍 Search institution, refund ID...]  [Period▼] [Approval▼]  │
├────────────────────────────────────────────────────────────────┤
│  REFUND TABLE (sortable, server-side paginated)                 │
└────────────────────────────────────────────────────────────────┘
```

---

## KPI Strip (5 tiles)

```
┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│ 7        │ │ ₹4.8L    │ │ 2        │ │ ₹38.4L   │ │ 1        │
│ Pending  │ │ Pending  │ │ Awaiting │ │ Processed│ │ Failed   │
│ Review   │ │ Value    │ │ FM Appvl │ │ (30d)    │ │ (retry)  │
│ ↑+2 this │ │          │ │ > ₹10K   │ │ 38 refunds│ │ ⚠        │
│ week     │ └──────────┘ └──────────┘ └──────────┘ └──────────┘
└──────────┘
```

- **Tile 1 (Pending Review):** COUNT WHERE status='PENDING_REVIEW'. Amber if > 5; red if > 10.
- **Tile 2 (Pending Value):** SUM(amount_paise) WHERE status='PENDING_REVIEW'. Sub-label: N refunds.
- **Tile 3 (Awaiting FM Approval):** COUNT WHERE status='PENDING_REVIEW' AND approval_required=TRUE. This tile appears only for FM (#69) — they must see what's in their queue. Red if > 0.
- **Tile 4 (Processed MTD):** COUNT and SUM WHERE status='PROCESSED' AND processed_at in last 30 days.
- **Tile 5 (Failed — Retry):** COUNT WHERE status='FAILED'. Red if > 0. Click → `?status=failed` tab.

---

## Refund Table

25 rows per page. Default sort: oldest pending first (`created_asc` when on Pending tab; `created_desc` on Processed tab).

| Column | Width | Description |
|---|---|---|
| Refund ID | 140px | Internal ID: REF-YYYYNNNNN; monospace; click → drawer |
| Institution | 200px | Name + type badge |
| Amount (₹) | 100px | `amount_paise`; right-aligned; red text if > ₹10K (FM approval required) |
| Reason | 140px | Badge: BILLING_ERROR/DUPLICATE_PAYMENT/PLAN_CANCELLED/GOODWILL/OVERPAYMENT/OTHER |
| Requested By | 110px | Avatar + name |
| Requested On | 90px | Relative time / date |
| FM Approval | 80px | ⚑ flag if `approval_required=TRUE`; "Required" badge in red; "N/A" if not needed |
| Status | 120px | Status badge (see below) |
| Razorpay Refund ID | 140px | `razorpay_refund_id` if processed; "—" otherwise; monospace |
| Actions | 48px | Context-sensitive kebab |

**Status badge colours:**
- PENDING_REVIEW: `bg-amber-900/50 text-amber-300` + pulsing dot
- APPROVED: `bg-blue-900/50 text-blue-300`
- REJECTED: `bg-slate-800 text-slate-400 line-through`
- PROCESSING: `bg-indigo-900/50 text-indigo-300` + spinner icon
- PROCESSED: `bg-green-900/50 text-green-400`
- FAILED: `bg-red-900/50 text-red-400` + warning icon

**FM Approval Required rows:** Red left border + amber ⚑ flag in the FM Approval column. Tooltip: "Finance Manager approval required for refunds > ₹10,000."

---

### Kebab Menu Actions

| Action | Status | Role |
|---|---|---|
| View Refund Details | Always | All |
| Approve Refund | PENDING_REVIEW (approval_required=FALSE) | Refund Exec (#73); and if approval_required=TRUE then FM (#69) only |
| Reject Refund | PENDING_REVIEW | FM (#69) |
| Process Refund (Razorpay API) | APPROVED | Refund Exec (#73) + 2FA; FM (#69) can also process |
| Retry Failed Refund | FAILED | Refund Exec (#73) + 2FA |
| Cancel Refund Request | PENDING_REVIEW | Billing Admin (#70) — who created it; FM (#69) |
| Download Refund Receipt | PROCESSED | All |

---

## Refund Detail Drawer (640px)

```
┌──────────────────────────────────────────────────────────────────┐
│  REF-2026-00041  · PENDING_REVIEW (FM approval required)  [×]    │
├──────────────────────────────────────────────────────────────────┤
│  REFUND DETAILS                                                  │
│  Institution:  Delhi Coaching Hub · ENTERPRISE                   │
│  Amount:       ₹12,000  (FM approval required — > ₹10K)          │
│  Reason:       BILLING_ERROR                                     │
│  Notes:        "Charged ₹12,000 extra due to seat count error    │
│                on Jan invoice. Verified by Billing Admin Priya."  │
│  Requested by: Priya K. (Billing Admin)  on 20 Mar 2026          │
├──────────────────────────────────────────────────────────────────┤
│  ORIGINAL PAYMENT                                                │
│  Payment ID:   pay_IxxxxF                                        │
│  Amount:       ₹1,89,000   Captured: 01 Jan 2026                 │
│  Method:       UPI (upi_id: billing@delhicoaching.com)           │
│  Invoice:      INV-2026-00210 · Jan 2026 · PAID                  │
├──────────────────────────────────────────────────────────────────┤
│  VALIDATION CHECKLIST ✓                                          │
│  ✓ Original payment exists and status = CAPTURED                 │
│  ✓ Payment not already fully refunded                            │
│  ✓ Refund amount ≤ remaining refundable amount (₹1,89,000)       │
│  ✓ Refund reason documented                                      │
│  ✗ FM approval pending (₹12,000 > ₹10,000 threshold)            │
├──────────────────────────────────────────────────────────────────┤
│  ACTIONS                                                         │
│  [Approve & Request FM Sign-off]   [Reject Refund]              │
└──────────────────────────────────────────────────────────────────┘
```

**Validation Checklist:** Auto-computed on drawer open:
1. Original payment exists and status = CAPTURED — checks `finance_payment.status`
2. Payment not already fully refunded — checks SUM of existing refunds for this payment vs original amount
3. Refund amount ≤ remaining refundable amount
4. Refund reason documented (notes not empty)
5. FM approval — checks `approval_required` flag

All checks must pass before [Process Refund] button is enabled.

**For PROCESSED refunds:** Shows Razorpay refund ID, processed_at, refund timeline from Razorpay (typically 5–7 business days to appear in institution's bank account). [Download Receipt] button.

---

## Approve/Reject Modal (FM #69 — for refunds > ₹10K)

```
  Review Refund Request
  ────────────────────────────────────────────────────────
  REF-2026-00041  ·  Delhi Coaching Hub  ·  ₹12,000
  Reason: BILLING_ERROR
  Requested by: Priya K. (Billing Admin)
  ────────────────────────────────────────────────────────
  Original invoice:  INV-2026-00210  ·  ₹1,89,000  PAID
  ────────────────────────────────────────────────────────
  Review Notes*  [Verified billing error in seat count...]  ]
  ────────────────────────────────────────────────────────
  [Reject]                              [Approve Refund]
```

- Review Notes: required; min 10 chars
- On Approve: status → APPROVED; `reviewed_by_id`, `reviewed_at`, `review_notes` set. Notifies Refund Exec (#73) to process.
- On Reject: status → REJECTED; same fields set. Notifies Billing Admin (#70) with rejection reason.

---

## Process Refund Modal (Refund Exec #73 + FM #69, with 2FA)

```
  Process Refund via Razorpay
  ────────────────────────────────────────────────────────
  REF-2026-00041  ·  Delhi Coaching Hub  ·  ₹12,000
  Original Payment: pay_IxxxxF  ·  ₹1,89,000  (UPI)
  ────────────────────────────────────────────────────────
  Refund amount:   ₹12,000   (read-only from request)
  Razorpay Payment ID:  pay_IxxxxF  (read-only)
  Speed:  [NORMAL ▼]   (NORMAL = 5–7 days; INSTANT = same day, +1.8% fee)
  ────────────────────────────────────────────────────────
  ⚠ This will call Razorpay Refund API. This action
     cannot be undone once Razorpay processes it.
  ────────────────────────────────────────────────────────
  2FA code*  [      ]
  [Cancel]                         [Process Refund Now]
```

**Speed selector:**
- NORMAL: no extra fee; 5–7 business days to institution's bank
- INSTANT: available for UPI and some netbanking; same-day; Razorpay charges 1.8% extra fee; only shown if payment method supports instant refund

**On submit:**
1. POST `/finance/refunds/{id}/process/`. View calls Razorpay Refund API: `POST https://api.razorpay.com/v1/payments/{payment_id}/refund`
2. On API success (HTTP 200): status → PROCESSED; `razorpay_refund_id` stored; `processed_at` set. Toast: "Refund of ₹[amount] processed — Razorpay refund ID: rfnd_Xxxxx."
3. On API failure (HTTP 4xx/5xx): status → FAILED; `failed_reason` stores Razorpay error code + message. Toast: "Refund failed — [error]. [Retry]."
4. Webhook: Razorpay also sends `refund.processed` webhook (verified by HMAC-SHA256); webhook handler updates status to PROCESSED as a safety net if the API call response was lost.

---

## Create Refund Request Modal (Billing Admin #70 + FM #69)

```
  Request Refund
  ────────────────────────────────────────────────────────
  Institution*   [Search institution...              ]
  Razorpay Payment ID*  [pay_Ixxxxxx               ]
                        [Lookup →] (auto-fills amount)
  Refund Amount (₹)*   [12,000]
                       (Max refundable: ₹1,89,000)
  Reason*  [BILLING_ERROR ▼]
  Notes*   [Seat count error on Jan invoice...      ]
  ────────────────────────────────────────────────────────
  ⚑ Amount > ₹10,000: Finance Manager approval required.
  ────────────────────────────────────────────────────────
  [Cancel]                    [Submit Refund Request]
```

**[Lookup →]:** POST to `/finance/refunds/lookup-payment/` with payment_id. Returns amount, capture date, method, institution match, and remaining refundable amount. Auto-populates Refund Amount (editable). Validates institution_id matches the payment's institution.

**Institution mismatch validation:** If `finance_payment.institution_id ≠ selected institution_id`, lookup returns error inline below the Payment ID field: "Payment ID [pay_Ixxxxxx] does not belong to [selected institution]. Please verify the correct institution." The [Submit Refund Request] button remains disabled until the mismatch is resolved.

**Remaining refundable:** `finance_payment.amount_paise - SUM(finance_refund.amount_paise WHERE payment_id=this AND status NOT IN ('REJECTED','FAILED'))`. Validated server-side.

**On submit:** Creates `finance_refund` with status=PENDING_REVIEW. If `approval_required=TRUE`: sends in-app notification to FM (#69).

---

## Retry Failed Refund Modal (480px — Refund Exec #73 + FM #69, with 2FA)

```
  Retry Refund
  ────────────────────────────────────────────────────────
  REF-2026-00041  ·  Delhi Coaching Hub  ·  ₹12,000
  Original Payment: pay_IxxxxF  ·  ₹1,89,000  (UPI)
  ────────────────────────────────────────────────────────
  Previous failure reason:
  [Displayed from finance_refund.failed_reason, e.g.:
   "Razorpay error BAD_REQUEST_ERROR: The payment does
    not belong to this merchant."]
  ────────────────────────────────────────────────────────
  Speed: NORMAL  (INSTANT not available for retries)
  ────────────────────────────────────────────────────────
  2FA code*  [      ]
  [Cancel]                              [Retry Refund]
```

**On submit:** POST `/finance/refunds/{id}/retry/`. Calls Razorpay Refund API again with same parameters.
- On API success: status → PROCESSED (same cascade as Process — see Post-Refund cascade section)
- On API failure: status remains FAILED; `failed_reason` updated with new error message; `retry_count` incremented
- Maximum 3 retries allowed (`finance_refund.retry_count ≤ 3`). Beyond 3: retry button disabled; FM must manually investigate with Razorpay support.

Schema addition needed: `retry_count INTEGER NOT NULL DEFAULT 0` on `finance_refund`.

---

## Download Refund Receipt

For PROCESSED refunds. Generates a PDF receipt for the institution's records.

**Template:** `finance/templates/refund_receipt.html` (WeasyPrint server-side).

**Content:**
- EduForge header, logo, address
- Refund receipt number: `RFD-{YYYY}-{NNNNN}` (sequential, same scheme as invoice numbers)
- Date of processing (`processed_at`)
- Institution name, GSTIN, billing address
- Original invoice number and period
- Original payment: Razorpay payment ID, amount, date
- Refund amount (₹)
- Razorpay refund ID (`razorpay_refund_id`)
- Refund reason
- "This receipt confirms that EduForge Technologies Private Limited has processed the above refund. Please allow 5–7 business days for the amount to reflect in your account."

**Download:** GET `/finance/refunds/{id}/receipt/`. Streams PDF. Cached after first generation (S3 key stored in `finance_refund.receipt_pdf_path`).

---

## Post-Refund Invoice & Payment Status Cascade

When a refund transitions to PROCESSED, the following cascade runs in a single database transaction (Django atomic block):

**1. Update `finance_payment`:**
- `finance_payment.refunded_amount_paise += refund.amount_paise`
- If `refunded_amount_paise == amount_paise`: set `finance_payment.status = 'REFUNDED'`
- If `refunded_amount_paise < amount_paise` (partial): set `finance_payment.status = 'PARTIALLY_REFUNDED'`

**2. Update `finance_invoice` (based on linked invoice):**

| Scenario | Invoice Status Result |
|---|---|
| Full refund (refunded = invoice total) | `status = 'REFUNDED'`; `paid_amount_paise = 0`; `refunded_at` set |
| Partial refund (refunded < invoice total, invoice was PAID) | `status = 'PARTIALLY_REFUNDED'`; `paid_amount_paise -= refund.amount_paise` |
| Partial refund leaves unpaid balance > 0 | Triggers AR aging re-check (Task M-1 re-queued for this institution) |
| Write-off invoice (was WRITTEN_OFF) | Status unchanged; refund is logged but invoice status preserved |

**3. Update `finance_ar_aging`:**
- Re-calculate outstanding for the institution: `SELECT SUM(total_paise - paid_amount_paise) FROM finance_invoice WHERE institution_id = X AND status IN ('OVERDUE','PARTIALLY_REFUNDED')`
- Saves to `finance_ar_aging.total_outstanding_paise`

**4. Audit log entry:**
- `finance_audit_log` record: `table_name='finance_refund'`, `action='PROCESSED'`, `old_value_json={status:'APPROVED'}`, `new_value_json={status:'PROCESSED', razorpay_refund_id:'rfnd_XXX'}`, actor, IP

**5. Notification:**
- In-app + email to Billing Admin (#70) and institution billing contact: "Refund of ₹[amount] for invoice [inv#] processed successfully. Razorpay refund ID: rfnd_Xxxxx."

**Edge cases:**
- If Razorpay webhook arrives before API response (race condition): webhook handler checks idempotency using `razorpay_refund_id`; duplicate processing skipped.
- If partial refund later followed by another partial refund: `refunded_amount_paise` is accumulated across all PROCESSED refunds for the same payment.
- INSTANT refund fee (1.8%): charged to EduForge; NOT deducted from the institution's refund amount. Logged separately in `finance_razorpay_settlement` for the period.

---

## Empty States

| Condition | Message | CTA |
|---|---|---|
| No pending refunds | "Refund queue is clear — no pending requests." | — |
| Pending tab: no items | "No refund requests awaiting review." | [+ Request Refund] |
| Failed tab: no items | "No failed refunds." | — |
| Processed tab: no items yet | "No processed refunds for this period." | — |

---

## Toast Messages

| Action | Toast | Type |
|---|---|---|
| Refund request created | "Refund request REF-YYYY-NNNNN submitted." | Green |
| Refund approved (FM) | "Refund approved. Refund Exec notified to process." | Green |
| Refund rejected (FM) | "Refund request rejected." | Amber |
| Refund processed (API success) | "Refund of ₹[amount] processed. Razorpay ID: rfnd_Xxxxx." | Green |
| Refund failed (API error) | "Refund failed: [Razorpay error]. Click Retry to attempt again." | Red |
| Refund retried | "Retry initiated for REF-YYYY-NNNNN." | Amber |
| 2FA failed | "2FA verification failed. Please retry." | Red |
| FM approval notification sent | "Refund request sent to Finance Manager for approval." | Amber (info) |

---

## Authorization

**Route guard:** `@division_m_required(allowed_roles=[69, 70, 73])`.

| Scenario | Behaviour |
|---|---|
| Refund Exec (#73) | Approve (non-FM-required), process (approved refunds), retry (failed). Cannot create requests or reject. |
| Billing Admin (#70) | Create requests; read-only on table; cannot approve, process, or reject. |
| Finance Manager (#69) | Full access; exclusive: approve/reject FM-required refunds; cancel any pending request |
| Process endpoint without 2FA | 403 |
| Razorpay API key not found | 500 with alert to FM + Security Engineer (error logged to CloudWatch) |
| Finance Analyst (#101) | Not in allowed_roles — 403; they see refund data via M-01 strip and M-02 P&L only |

---

## Role-Based UI Visibility Summary

| Feature | 69 FM | 70 Billing Admin | 73 Refund Exec |
|---|---|---|---|
| All status tabs | Yes | Yes (read all) | Yes |
| [+ Request Refund] | Yes | Yes | No |
| Approve (non-FM-required) | Yes | No | Yes |
| Approve (FM-required > ₹10K) | Yes (exclusive) | No | No |
| Reject | Yes | Cancel own requests only | No |
| Process via Razorpay API | Yes + 2FA | No | Yes + 2FA |
| Retry Failed | Yes + 2FA | No | Yes + 2FA |
| FM Approval tile (KPI strip) | Yes (exclusive) | No | No |
| Validation checklist (drawer) | Yes | Yes (read) | Yes |
| [Download Receipt] (PROCESSED) | Yes | Yes | Yes |

---

## Performance Requirements

| Metric | Target | Notes |
|---|---|---|
| Initial page load (SSR) | < 2s P95 | KPI strip from cache; refund table live |
| KPI strip | < 400ms P95 (cache hit) | 2-min TTL |
| Refund table (25 rows) | < 400ms P95 | No Memcached; direct DB query |
| Refund detail drawer (live) | < 350ms P95 | `finance_refund` + `finance_payment` + `finance_invoice` |
| Razorpay Refund API call | < 3s P95 | External API; 10s timeout; error if Razorpay > 10s |
| Post-refund cascade (DB transaction) | < 500ms | Invoice + payment + AR aging update in single atomic block |
| [Download Receipt] PDF | < 2s P95 | WeasyPrint server-side; cached after first generation |

---

## Keyboard Shortcuts

| Key | Action |
|---|---|
| `g` `q` | Go to Refund Queue (M-07) |
| `n` | Open Request Refund modal (Billing Admin, FM) |
| `/` | Focus search (institution or refund ID) |
| `e` | Export CSV (FM) |
| `1`–`6` | Switch tab: ALL / PENDING_REVIEW / APPROVED / PROCESSED / REJECTED / FAILED |
| `←` / `→` | Previous / next page |
| `Esc` | Close open drawer or modal |
| `?` | Show keyboard shortcut help overlay |

