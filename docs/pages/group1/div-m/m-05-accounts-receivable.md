# M-05 — Accounts Receivable

**Route:** `GET /finance/ar/`
**Method:** Django `TemplateView` + HTMX part-loads; server-side pagination
**Primary roles:** AR Exec (#71), Collections Executive (#102)
**Also sees:** Finance Manager (#69) full access; Finance Analyst (#101) read-only

---

## Purpose

AR management workspace covering the full receivables lifecycle from first invoice overdue to final resolution. AR Exec (#71) owns the 0–60 day bucket: sending reminders, logging phone calls, recording promise-to-pay dates, and escalating chronic non-payers to Collections. Collections Executive (#102) owns the 60+ day bucket: outbound dunning calls, formal demand notices, payment plan negotiation, and suspension coordination. Finance Manager monitors overall collection health and approves write-offs. Finance Analyst uses the aging distribution for investor reporting and churn prediction.

At 2,050 institutions with 3–5% overdue rate (~60–100 institutions), this page drives the difference between a 93% and a 97% collection rate — a ₹50L+ swing in net collections at ₹4Cr+ ARR scale.

---

## Data Sources

| Section | Source | Cache TTL |
|---|---|---|
| Aging KPI strip | `finance_ar_aging` totals (latest Task M-1 run) | 5 min |
| Aging distribution chart | `finance_ar_aging` latest run, grouped by bucket | 5 min |
| AR table | `finance_ar_aging` JOIN `institution` JOIN `finance_invoice` (overdue rows) LEFT JOIN last `finance_ar_followup` | 5 min |
| Institution AR drawer | `finance_ar_aging` + `finance_invoice` (all overdue) + `finance_ar_followup` (all history) | Live |
| Promise-to-pay tracker | `finance_ar_followup` WHERE followup_type='PROMISE_TO_PAY' AND promise_to_pay_date >= today | 5 min |
| Collections queue | `finance_ar_aging` WHERE bucket_61_90_paise > 0 OR bucket_91plus_paise > 0 | 5 min |

Last Task M-1 run timestamp shown on page: "Aging data as of [computed_at]". If > 26 hours old: amber warning "Aging data may be stale — Task M-1 may have failed."

---

## URL Parameters

| Param | Values | Default | Effect |
|---|---|---|---|
| `?bucket` | `all`, `0_30`, `31_60`, `61_90`, `91plus` | `all` | Pre-selects aging bucket tab |
| `?type` | `school`, `college`, `coaching`, `group` (comma-sep) | — | Filter by institution type |
| `?collector` | `ar_exec`, `collections`, `unassigned` | — | Filter by assigned collector role |
| `?q` | string ≥ 2 chars | — | ILIKE on institution_name |
| `?sort` | `outstanding_desc`, `outstanding_asc`, `oldest_invoice_desc`, `institution_name`, `last_followup_asc` | `outstanding_desc` | Table sort |
| `?page` | integer ≥ 1 | `1` | Pagination |
| `?export` | `csv` | — | Export (FM + Analyst only for full; AR Exec for own bucket) |
| `?institution_id` | integer | — | Jump directly to an institution's AR drawer |

---

## HTMX Part-Load Routes

| Part | Route | Trigger | Target ID |
|---|---|---|---|
| Aging KPI strip | `?part=kpi` | Page load + 5 min poll | `#ar-kpi` |
| Aging chart | `?part=aging_chart` | Page load | `#ar-aging-chart` |
| AR table | `?part=table` | Tab click · filter · sort · page | `#ar-table` |
| Institution AR drawer | `?part=drawer&institution_id={id}` | Row click | `#ar-drawer` |
| Log Follow-up modal | `?part=followup_modal&institution_id={id}` | [Log Follow-up] | `#modal-container` |
| Promise-to-pay panel | `?part=promise_panel` | Page load | `#ar-promise-panel` |
| Collections queue | `?part=collections_queue` | Page load + 5 min poll | `#ar-collections` |

---

## Page Layout

```
┌────────────────────────────────────────────────────────────────────┐
│  Accounts Receivable   Aging: [Task M-1 as of 21 Mar, 02:14 IST]  │
├────────────────────────────────────────────────────────────────────┤
│  AGING KPI STRIP (5 tiles)                                         │
├──────────────────────────────────┬─────────────────────────────────┤
│  AGING DISTRIBUTION CHART        │  PROMISE-TO-PAY PANEL           │
├──────────────────────────────────┴─────────────────────────────────┤
│  [0–30d(31)] [31–60d(19)] [61–90d(8)] [90+d(5)] [All(63)]         │
├────────────────────────────────────────────────────────────────────┤
│  [🔍 Search institution...]  [Type▼] [Collector▼]  [Clear All]    │
├────────────────────────────────────────────────────────────────────┤
│  AR TABLE (sortable, server-side paginated)                         │
├────────────────────────────────────────────────────────────────────┤
│  COLLECTIONS QUEUE (60+ day bucket, prominent panel)               │
└────────────────────────────────────────────────────────────────────┘
```

---

## Aging KPI Strip (5 tiles)

```
┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│ ₹12.4L   │ │ ₹6.8L    │ │ ₹3.9L    │ │ ₹1.7L    │ │ 5        │
│ Total    │ │ 0–30d    │ │ 31–60d   │ │ 61–90d   │ │ 90+ days │
│ Overdue  │ │ (31 insts│ │ (19 insts│ │ (8 insts)│ │ (5 insts)│
│ 63 insts │ │ of total)│ │ ↓-₹1.2L  │ │ ↑+₹0.3L  │ │ ₹2.8L ⚠  │
└──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘
```

- Tile 1 (Total): SUM of all `finance_ar_aging.total_outstanding_paise`. Sub-label: N institutions. Red if > ₹20L.
- Tile 2 (0–30d): SUM `bucket_0_30_paise`. Normal — these are fresh overdue.
- Tile 3 (31–60d): SUM `bucket_31_60_paise`. Amber tile if > ₹5L or > 15 institutions.
- Tile 4 (61–90d): SUM `bucket_61_90_paise`. Red tile if > ₹2L or > 5 institutions.
- Tile 5 (90+ days): SUM `bucket_91plus_paise`. Always shown in red if > 0. Sub-label: "₹X.XL at risk of write-off".
- Each tile: click sets `?bucket=<bucket>` filter on the AR table.

**Delta display:** Each tile shows `↑+₹X.XL` or `↓-₹X.XL` vs the previous Task M-1 run (compare current `computed_at` vs prior row for the same institution). A decreasing balance in 31–60d and increasing in 0–30d = healthy collections. A growing 90+ bucket = problem escalation.

---

## Aging Distribution Chart

Stacked horizontal bar chart — one bar per institution type (School / College / Coaching / Group / Total).

```
Institution Type    0–30d          31–60d     61–90d  90+d
Total (63)         ████████████    ████████   █████   ████
Schools (20)       ██████          ████       ██      ██
Colleges (18)      █████           ████       ██      █
Coaching (15)      ████            ███        █       █
Groups (10)        ██████          ██         —       —
                 ₹6.8L           ₹3.9L     ₹1.7L  ₹2.8L
 [■ 0-30d] [■ 31-60d] [■ 61-90d] [■ 90+d]
```

Colours: 0–30d=amber-300 · 31–60d=orange-400 · 61–90d=red-400 · 90+d=red-700
Hover: exact amount + institution count for each bucket.
Clicking a segment: sets `?bucket=<bucket>&type=<type>` on the table.

---

## Aging Bucket Tabs

Five tabs: 0–30d · 31–60d · 61–90d · 90+ days · All. Count badge on each.

- 61–90d tab: amber badge border
- 90+ days tab: red badge border + pulsing dot
- Tab click filters table to `?bucket=<bucket>` via HTMX.

**AR Exec (#71) default view:** 0–30d and 31–60d tabs only. 61–90d and 90+ tabs visible but show "Escalate to Collections" prompt instead of [Log Follow-up].

**Collections Exec (#102) default view:** Lands on 61–90d tab. 0–30d and 31–60d tabs visible as read-only.

---

## AR Table

Server-side paginated, 25 rows per page. Sorted by `total_outstanding_paise DESC` by default.

| Column | Width | Description |
|---|---|---|
| Institution | 200px | Name (link → drawer) + type badge |
| Total Overdue (₹) | 120px | `total_outstanding_paise`; red text if > ₹5L |
| 0–30d (₹) | 90px | `bucket_0_30_paise`; amber if > 0 |
| 31–60d (₹) | 90px | `bucket_31_60_paise`; orange if > 0 |
| 61–90d (₹) | 90px | `bucket_61_90_paise`; red if > 0 |
| 90+ days (₹) | 90px | `bucket_91plus_paise`; dark red bold if > 0 |
| Oldest Invoice | 90px | `oldest_invoice_days` days; colour-coded |
| Last Follow-up | 100px | Relative time from `last_followup_date`; red if > 14 days |
| Assigned | 110px | Avatar + name of assigned collector (`assigned_collector_id`); "AR Exec" or "Collections" or "Unassigned" badge |
| Promise to Pay | 90px | `promise_to_pay_date` if set; amber if promise date is today, red if past |
| Actions | 48px | Context-sensitive kebab menu |

**Row visual cues:**
- Any row with 90+d bucket > 0: red left-border 3px + faint `bg-red-950` row tint
- Any row with promise_to_pay_date < today (broken promise): amber pulsing flag icon in Actions column

---

### Kebab Menu Actions

| Action | Available When | Role |
|---|---|---|
| View AR Details | Always | All |
| Log Follow-up | Always | AR Exec (#71), Collections Exec (#102), FM (#69) |
| Send Reminder (Email) | 0–30d, 31–60d bucket | AR Exec (#71); dispatched via F-06 |
| Log Phone Call | Always | AR Exec (#71), Collections Exec (#102) |
| Record Promise to Pay | Always | AR Exec (#71), Collections Exec (#102) |
| Escalate to Collections | 31–60d and above | AR Exec (#71) → sets `assigned_collector_id` to Collections Exec queue |
| Issue Demand Notice | 61+ day bucket | Collections Exec (#102), FM (#69) |
| Negotiate Payment Plan | 61+ day bucket | Collections Exec (#102) |
| Suspend Account | 90+ bucket | Collections Exec (#102) + FM (#69) + 2FA; redirects to M-04 suspend modal |
| View Subscription | Always | All → links to M-04 drawer |
| View Invoices | Always | All → links to M-03?q=<institution_name>&status=overdue |

---

## Institution AR Drawer (640px)

Full AR history for one institution.

```
┌──────────────────────────────────────────────────────────────────┐
│  Delhi Coaching Hub — Accounts Receivable            [Close ×]   │
│  ENTERPRISE · ₹12.4L ARR · 8,500 members                        │
├──────────────────────────────────────────────────────────────────┤
│  AGING SUMMARY                                                   │
│  0–30d: ₹0   31–60d: ₹0   61–90d: ₹1,77,000   90+d: ₹0         │
│  Total Outstanding: ₹1,77,000   Oldest: 62 days                 │
│  Assigned to: Priya K. (Collections Exec)                        │
├──────────────────────────────────────────────────────────────────┤
│  OVERDUE INVOICES                                                │
│  INV-2026-00841  Feb 2026  ₹1,77,000  62 days  [View] [Remind]  │
├──────────────────────────────────────────────────────────────────┤
│  FOLLOW-UP HISTORY (newest first)                                │
│  21 Mar  DEMAND_NOTICE  "Formal notice sent via email + cert."   │
│  14 Mar  PHONE_CALL     "Spoke with Dr. Ramesh; promised 20 Mar" │
│  05 Mar  REMINDER_EMAIL "Auto-reminder sent"                     │
│  [+ Log New Follow-up]                                           │
├──────────────────────────────────────────────────────────────────┤
│  PAYMENT PLAN                                                    │
│  Promise-to-pay: 30 Mar 2026 (in 9 days)                         │
│  Amount: ₹1,77,000 (full settlement)                             │
├──────────────────────────────────────────────────────────────────┤
│  ACTIONS                                                         │
│  [Issue Demand Notice]  [Negotiate Plan]  [Suspend Account]      │
└──────────────────────────────────────────────────────────────────┘
```

**Overdue Invoices section:** All `finance_invoice` WHERE institution_id=this AND status IN ('OVERDUE','PARTIALLY_PAID'). Shows invoice_number, billing_period, total, days_overdue, [View] → M-03 drawer, [Remind] → triggers email via F-06.

**Follow-up History:** All `finance_ar_followup` WHERE institution_id=this, newest first. Shows followup_type badge (colour-coded) + notes + created_by avatar + relative date. [+ Log New Follow-up] opens the Log Follow-up modal inline.

**Payment Plan section:** Only shown if `promise_to_pay_date IS NOT NULL`. Shows promise date, amount, and whether it's been honoured (checked against paid invoices on that date). "Promise BROKEN" badge in red if promise_date < today and invoice still unpaid.

---

## Log Follow-up Modal (480px)

Used by AR Exec (#71) and Collections Exec (#102).

```
  Log Follow-up
  ────────────────────────────────────────────────────────
  Institution: Delhi Coaching Hub (read-only)
  Invoice:     INV-2026-00841 (read-only or select)
  ────────────────────────────────────────────────────────
  Type*  [PHONE_CALL ▼]
         REMINDER_EMAIL / PHONE_CALL / WHATSAPP /
         DEMAND_NOTICE / PAYMENT_PLAN_AGREED / ESCALATED /
         SUSPENDED / PROMISE_TO_PAY
  Notes* [Spoke with billing manager; she said payment...]  ]
  ────────────────────────────────────────────────────────
  Next Follow-up Date  [28 Mar 2026]  (optional)
  ────────────────────────────────────────────────────────
  [If type=PROMISE_TO_PAY] ──────────────────────────────
  Promise Date*  [30 Mar 2026]
  Promise Amount*  [₹1,77,000]
  ────────────────────────────────────────────────────────
  [Cancel]                            [Log Follow-up]
```

**Validation:**
- Type: required
- Notes: required; min 10 chars; max 2000 chars; HTML-escaped on display
- Next Follow-up Date: optional; must be > today
- Promise Date (if type=PROMISE_TO_PAY): required; must be > today
- Promise Amount (if type=PROMISE_TO_PAY): required; > 0 paise; ≤ total_outstanding_paise

**On submit:** POST `/finance/ar/followup/`. Creates `finance_ar_followup` record. Updates `finance_ar_aging.last_followup_date`. If type=PROMISE_TO_PAY: sets `promise_to_pay_date` and `promise_amount_paise`. Toast: "Follow-up logged for [institution]."

---

## Promise-to-Pay Panel

Right-side panel showing all active promise-to-pay records.

```
┌────────────────────────────────────────────────┐
│  Promises to Pay (active: 8)                   │
│  ────────────────────────────────────────────  │
│  Delhi Coaching Hub  ₹1,77,000  Due: 30 Mar    │
│  (in 9 days)  Logged by Priya K.   [Mark Paid] │
│  ────────────────────────────────────────────  │
│  Sunrise Academy     ₹42,480    Due: 25 Mar    │
│  (TODAY)  ⚠ Payment expected today   [Verify] │
│  ────────────────────────────────────────────  │
│  Excel Coaching Hub  ₹84,960    Due: 15 Mar    │
│  BROKEN — promise date passed  [Escalate]      │
└────────────────────────────────────────────────┘
```

- "Due today" rows: amber row tint, pulsing clock icon
- "Broken promise" rows: red row tint; [Escalate] button → assigns to Collections Exec (#102) and logs ESCALATED follow-up
- [Mark Paid]: opens M-03 Mark Paid modal in a side drawer, pre-filled with `invoice_id` from the promise record, `amount_paid` = `promise_amount_paise`, `payment_date` = today. URL: `GET /finance/invoices/{invoice_id}/mark-paid/?from=promise_panel` — `from` param triggers "Return to AR" breadcrumb after save.
- [Verify]: AR Exec confirms whether payment was received — opens a confirmation dialog: "Has payment been received for this promise? [Yes, received] [No, still pending]". On "Yes": logs PHONE_CALL follow-up note "Payment verified as received." On "No": no change.

---

## Collections Queue

Prominent panel at the bottom of the page (or primary view for Collections Exec #102). Shows all institutions in 61–90d or 90+ bucket.

```
┌─────────────────────────────────────────────────────────────┐
│  Collections Queue (13 institutions · ₹4.5L outstanding)    │
│  ─────────────────────────────────────────────────────────  │
│  61–90 DAYS (8 institutions · ₹1.7L)                        │
│  ─────────────────────────────────────────────────────────  │
│  SR Commerce College   ₹42,480   67d   [Demand Notice] [Plan]│
│  Victory Institute     ₹84,960   65d   [Demand Notice] [Plan]│
│  ─────────────────────────────────────────────────────────  │
│  90+ DAYS (5 institutions · ₹2.8L)                          │
│  ─────────────────────────────────────────────────────────  │
│  Excel Coaching Hub    ₹1,77,000  112d  [Suspend] [Write-off]│
│  Alpha Institute       ₹84,960    98d   [Suspend] [Write-off]│
└─────────────────────────────────────────────────────────────┘
```

- **[Demand Notice]:** Creates a `finance_ar_followup` with type=DEMAND_NOTICE, generates a formal demand letter PDF (template-based), and sends via email + registered post tracking. Available to Collections Exec (#102) + FM (#69).
- **[Plan]:** Opens a payment plan negotiation form (inline): structured installment agreement. Splits outstanding into 2–3 tranches with due dates. Logged as PAYMENT_PLAN_AGREED follow-up.
- **[Suspend]:** Opens M-04 suspend modal (2FA required).
- **[Write-off]:** Available to FM (#69) only. Opens M-03 write-off modal.

**Collections Exec (#102) default view:** This panel is shown full-width at the top of the page (above the AR table) when role=#102.

---

## AR SLA Targets

Operational service-level targets for follow-up cadence. Displayed as an info bar above the AR table (visible to FM #69 and AR Exec #71). Collections Exec (#102) sees only buckets relevant to their scope.

| AR Bucket | SLA | Responsible Role | Breach Indicator |
|---|---|---|---|
| 0–30 days | First reminder within 24h of invoice becoming overdue | AR Exec (#71) | Amber row tint if `last_followup_date` is NULL and days_overdue > 1 |
| 31–60 days | Follow-up attempt within 48h of entering this bucket | AR Exec (#71) | Red row tint if `last_followup_date` < (entered_bucket_date + 2d) |
| 61–90 days | Demand notice issued within 5 business days of entering bucket; Collections Exec assigned within 24h | Collections Exec (#102) | Red row tint; alert sent to FM (#69) on SLA breach |
| 90+ days | Escalation decision (suspend or payment plan) within 3 business days of entering bucket | Collections Exec (#102) + FM (#69) approval | Red row tint; in-app alert to FM every 48h until resolved |

**SLA breach alerts:** Task M-1 (2AM daily run) checks `finance_ar_aging` for SLA breaches and queues in-app notifications. FM (#69) receives a daily digest if any SLA is breached.

---

## Demand Notice PDF Template

Generated by the `[Demand Notice]` action. Template file: `finance/templates/demand_notice.html` (WeasyPrint-rendered server-side).

**Template fields populated at generation time:**

| Field | Source |
|---|---|
| Notice Number | `DN-{YYYY}-{sequence}` auto-incremented per year |
| Date of Issue | `today` (IST) |
| Recipient Name | `institution.name` |
| Registered Address | `institution.billing_address` |
| GSTIN | `institution.gstin` |
| Outstanding Amount (₹) | `finance_ar_aging.total_outstanding_paise` |
| Overdue Since | Earliest overdue invoice `due_date` |
| Invoice List | All `finance_invoice` WHERE status=OVERDUE for this institution (inv#, date, amount) |
| Payment Due Deadline | Date of issue + 15 calendar days |
| EduForge Legal Entity | "EduForge Technologies Private Limited, Hyderabad, Telangana" |
| Signatory | FM (#69) name + designation auto-filled; signature image from `finance_config['fm_signature_path']` |

**Legal boilerplate (fixed text):**
```
This is a formal demand notice issued under Section 8 of the Insolvency and Bankruptcy
Code, 2016 and applicable contract terms. Failure to remit the outstanding amount within
15 calendar days of the date of this notice may result in suspension of your EduForge
platform subscription and initiation of legal recovery proceedings. EduForge Technologies
Private Limited reserves all rights to seek recovery of dues along with applicable interest
and legal costs.
```

**Delivery:** Email (institution billing_email) + PDF attachment. `finance_ar_followup` record created with type=DEMAND_NOTICE, `notice_pdf_path` set to S3 key of generated PDF.

---

## Export CSV

**Columns (16):** institution_id, institution_name, institution_type, plan_tier, arr_inr, total_outstanding_inr, bucket_0_30_inr, bucket_31_60_inr, bucket_61_90_inr, bucket_91plus_inr, oldest_invoice_days, last_followup_date, last_followup_type, promise_to_pay_date, assigned_collector, computed_at

**Available to:** FM (#69) full export; Finance Analyst (#101) full export; AR Exec (#71) own assigned institutions only; Collections Exec (#102) own assigned 60+ bucket only.

---

## Empty States

| Condition | Message |
|---|---|
| No overdue institutions | "AR is clean — no overdue balances. Collection rate: 100% this period!" |
| Bucket tab is empty | "No institutions in the [0–30d/31–60d/61–90d/90+d] bucket." |
| Collections queue empty | "Collections queue is clear. All accounts are current." |
| No promise-to-pay records | "No active payment promises." |

---

## Toast Messages

| Action | Toast | Type |
|---|---|---|
| Follow-up logged | "Follow-up logged for [institution]." | Green |
| Promise-to-pay recorded | "Promise to pay ₹[amount] by [date] recorded for [institution]." | Green |
| Reminder sent | "Payment reminder sent to [institution] billing contact." | Green |
| Demand notice issued | "Formal demand notice sent to [institution]." | Amber |
| Payment plan agreed | "Payment plan (N tranches) logged for [institution]." | Green |
| Escalated to collections | "[institution] escalated to collections queue (assigned to [name])." | Amber |
| Account suspended | "[institution] suspended. See M-04 for reactivation." | Red (warning) |
| Broken promise detected | "[institution] missed promised payment of ₹[amount] due [date]. Consider escalating." | Amber |

---

## Authorization

**Route guard:** `@division_m_required(allowed_roles=[69, 71, 101, 102])`.

| Scenario | Behaviour |
|---|---|
| AR Exec (#71) | Full write access to 0–60d bucket actions. 61+ day actions show "Escalate to Collections" only. |
| Collections Exec (#102) | Full write access to 60+ day actions only. 0–30d and 31–60d shown as read-only with "Assigned to AR Exec" label. |
| Finance Analyst (#101) | Full read-only across all buckets; export allowed. |
| Finance Manager (#69) | Full access to all buckets; write-off + suspend + approve payment plans. |
| Demand Notice PDF endpoint | Returns 403 for AR Exec (#71) — Collections Exec + FM only. |

---

## Role-Based UI Visibility Summary

| Element | 69 FM | 71 AR Exec | 101 Analyst | 102 Collections |
|---|---|---|---|---|
| All bucket tabs | Yes | Yes (0–60d write; 61+ read) | Yes (read all) | Yes (60+ write; 0–60 read) |
| Aging chart + KPI strip | Yes | Yes | Yes | Yes |
| Log Follow-up | Yes | Yes (any) | No | Yes (60+ bucket) |
| Send Reminder | Yes | Yes | No | No |
| Record Promise to Pay | Yes | Yes | No | Yes |
| Escalate to Collections | Yes | Yes | No | No |
| Issue Demand Notice | Yes | No | No | Yes |
| Negotiate Payment Plan | Yes | No | No | Yes |
| Suspend Account | Yes + 2FA | No | No | Yes + 2FA |
| Write-off shortcut | Yes (→ M-03) | No | No | No |
| Promise-to-Pay panel | Yes | Yes | Yes (read) | Yes |
| Collections Queue | Yes | Read only | Read only | Full (primary view) |
| Export CSV | Yes (full) | Yes (own) | Yes (full) | Yes (own 60+) |

---

## Performance Requirements

| Metric | Target | Notes |
|---|---|---|
| Initial page load (SSR) | < 2s P95 | Aging table from `finance_ar_aging` (pre-computed by Task M-1) |
| KPI strip + aging chart | < 500ms P95 (cache hit) | 5-min TTL; stale-data warning if Task M-1 ran > 26h ago |
| AR table (25 rows) | < 400ms P95 | Indexed on `institution_id`, bucket columns |
| Institution AR drawer (live) | < 400ms P95 | `finance_ar_aging` + `finance_ar_followup` + `finance_invoice` JOIN |
| Collections queue panel | < 500ms P95 (cache hit) | 2-min TTL; filtered to 61+ day buckets |
| Promise-to-Pay panel | < 400ms P95 (cache hit) | 5-min TTL |
| Demand Notice PDF generation | < 4s P95 | WeasyPrint server-side; emailed on completion |
| Export CSV | < 3s for ≤ 2,000 rows | Streaming response |

---

## Keyboard Shortcuts

| Key | Action |
|---|---|
| `g` `a` | Go to Accounts Receivable (M-05) |
| `n` | Log Follow-up (AR Exec, FM, Collections Exec — context-sensitive) |
| `/` | Focus institution search |
| `e` | Export CSV |
| `1`–`5` | Switch bucket tab: ALL / 0–30d / 31–60d / 61–90d / 90+ |
| `←` / `→` | Previous / next page in AR table |
| `Esc` | Close open drawer or modal |
| `?` | Show keyboard shortcut help overlay |

