# M-03 — Billing & Invoices

**Route:** `GET /finance/invoices/`
**Method:** Django `TemplateView` + HTMX part-loads; server-side pagination
**Primary role:** Billing Admin (#70)
**Also sees:** Finance Manager (#69) full read + write-off; Finance Analyst (#101) read-only aggregated; AR Exec (#71) read overdue only; Collections Exec (#102) read overdue only; GST Consultant (#72) read (for GSTR filing)

---

## Purpose

Operational invoice management workspace. Billing Admin uses this daily: generate invoices for new subscriptions, send to institution billing contacts, track payment status, handle partial payments, void drafts, and write off irrecoverable balances. Finance Manager uses it to approve write-offs and audit invoice accuracy before investor reporting. AR Exec and Collections Exec use the overdue tab to prioritise follow-up. GST Consultant uses the period filter to pull invoice lists for GSTR-1 filing preparation. At 2,050 monthly invoices, this page must load the table in < 500ms even with heavy filters.

---

## Data Sources

| Section | Source | Cache TTL |
|---|---|---|
| KPI strip | `analytics_revenue` latest month (invoiced, collected, overdue counts) | 5 min |
| Invoice table | `finance_invoice` JOIN `institution` JOIN auth_user (created_by); live — no Memcached | Live |
| Tab counts (status badges) | `finance_invoice` GROUP BY status WHERE period matches tab filter | 5 min |
| Invoice detail drawer | `finance_invoice` + `finance_payment` + `finance_ar_followup` for institution | Live |
| GST column data | `finance_invoice.(cgst_paise, sgst_paise, igst_paise)` | Live |

Invoice table itself is never Memcached because billing state (paid/overdue/void) must reflect real-time. Tab count badges use a 5-min cache to avoid GROUP BY on every keystroke.

---

## URL Parameters

| Param | Values | Default | Effect |
|---|---|---|---|
| `?status` | `all`, `draft`, `sent`, `paid`, `overdue`, `partially_paid`, `written_off`, `void` | `all` | Pre-selects the tab and filters table |
| `?type` | `school`, `college`, `coaching`, `group` (comma-sep) | — | Filter by institution type |
| `?tier` | `STARTER`, `STANDARD`, `PROFESSIONAL`, `ENTERPRISE` (comma-sep) | — | Filter by plan tier |
| `?period` | `YYYY-MM` or range `YYYY-MM:YYYY-MM` | — | Billing period filter |
| `?due_before` | `YYYY-MM-DD` | — | Show invoices with due_date ≤ date |
| `?q` | string ≥ 2 chars | — | Search: ILIKE on institution_name, invoice_number |
| `?sort` | `due_date_asc`, `due_date_desc`, `amount_asc`, `amount_desc`, `institution_name`, `created_desc` | `due_date_asc` | Table sort |
| `?page` | integer ≥ 1 | `1` | Pagination |
| `?export` | `csv` | — | Export filtered list (FM + Billing Admin + GST Consultant) |

---

## HTMX Part-Load Routes

| Part | Route | Trigger | Target ID |
|---|---|---|---|
| KPI strip | `?part=kpi` | Page load + 5 min poll | `#inv-kpi` |
| Invoice table | `?part=table` | Tab click · search · filter · sort · page | `#inv-table` |
| Tab counts | `?part=tab_counts` | After invoice create/status change | `#inv-tabs` |
| Invoice drawer | `?part=drawer&id={id}` | Row click / [View] action | `#inv-drawer` |
| Generate Invoice modal | `?part=generate_modal` | [+ Generate Invoice] click | `#modal-container` |
| Mark Paid modal | `?part=mark_paid_modal&id={id}` | [Mark Paid] kebab action | `#modal-container` |
| Write-off modal | `?part=writeoff_modal&id={id}` | [Write Off] kebab action | `#modal-container` |
| Void modal | `?part=void_modal&id={id}` | [Void] kebab action | `#modal-container` |

---

## Page Layout

```
┌──────────────────────────────────────────────────────────────────────┐
│  Billing & Invoices                          [+ Generate Invoice]    │
├──────────────────────────────────────────────────────────────────────┤
│  KPI STRIP (6 tiles)                                                 │
├──────────────────────────────────────────────────────────────────────┤
│  [All(2050)] [Draft(12)] [Sent(284)] [Overdue(63)▲] [Paid(1680)]    │
│  [Partially Paid(8)] [Written Off(3)] [Void(0)]                      │
├──────────────────────────────────────────────────────────────────────┤
│  FILTER BAR                                                          │
│  [🔍 Search institution, invoice #...]                               │
│  [Type▼] [Plan Tier▼] [Period▼] [Due Before▼] [Amount Range▼]       │
│  Active filters: Status: Overdue ×                      [Clear All] │
├──────────────────────────────────────────────────────────────────────┤
│  [☐ Select All]  N selected  [Bulk: Send Reminder | Export | Paid]  │
│  Showing 1–25 of 63   Sort: [Due Date ↑▼]              [Export CSV] │
├──────────────────────────────────────────────────────────────────────┤
│  ☐ │ Invoice # │ Institution │ Period │ Amount │ Due │ Status │ ⋯  │
│  ☐ │ INV-0841  │ ABC Coaching│ Mar 26 │ ₹42,480│01Mar│● Overd │ ⋯  │
└──────────────────────────────────────────────────────────────────────┘
```

---

## KPI Strip (6 tiles)

```
┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│ ₹4.28Cr  │ │ ₹4.11Cr  │ │ 63       │ │ ₹12.4L   │ │ 18       │ │ 96.8%    │
│ Invoiced │ │ Collected│ │ Overdue  │ │ Overdue  │ │ Draft/   │ │Collection│
│ (MTD)    │ │ (MTD)    │ │ Count    │ │ Balance  │ │ Pending  │ │ Rate     │
│ 2,050 inv│ │          │ │          │ │          │ │ (unsent) │ │          │
└──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘
```

- **Overdue Count:** > 100 = amber; > 200 = red
- **Overdue Balance:** > ₹20L = red
- **Collection Rate:** ≥ 96% = green; 90–95.9% = amber; < 90% = red
- Tile click links to pre-filtered table (Tile 3 → ?status=overdue, Tile 4 → ?status=draft)

---

## Tab Bar

Eight tabs: All · Draft · Sent · Overdue · Paid · Partially Paid · Written Off · Void

Count badge on each tab (from 5-min cache). Overdue tab badge: red background, pulsing dot. Draft tab badge: grey. Paid tab badge: green. Active tab: border-bottom-2 accent colour.

Tab click sets `?status=<status>` and reloads the table partial via HTMX (`hx-push-url="true"`).

**Overdue tab:** highlighted with amber top border even when not selected — persistent visual cue that there are pending collections.

---

## Filter Bar

**Search field:** ILIKE `%q%` on `finance_invoice.invoice_number` and `institution.name`. Min 2 chars; 300ms debounce.

**Type filter:** Multi-select. School / College / Coaching / Group.

**Plan Tier filter:** Multi-select. Starter / Standard / Professional / Enterprise. Translates to `finance_subscription.plan_tier` via JOIN.

**Period filter:** Month/year picker (range). Two inputs: "From" and "To" (YYYY-MM format). Default: current month. Quick-select chips: "This Month" · "Last Month" · "This Quarter" · "This FY".

**Due Before:** Date picker. Useful for AR/Collections Exec to filter invoices due in the next N days.

**Amount Range:** Min ₹ / Max ₹ text inputs. Applies to `finance_invoice.total_paise`.

**Active filter chips:** Each applied filter shown as removable chip below the filter row.

**Clear All:** Resets all filters except the active tab selection.

---

## Invoice Table

Server-side paginated, 25 rows per page. All columns sortable.

| Column | Width | Description |
|---|---|---|
| Checkbox | 32px | Row selection; select-all selects current page (max 50 for bulk ops) |
| Invoice # | 130px | `INV-YYYY-NNNNN` monospace; click → opens drawer |
| Institution | 200px | Name (link → M-04 subscription detail) + type badge; city on 2nd line |
| Billing Period | 100px | "Feb 2026" |
| Subtotal (₹) | 100px | Pre-GST, right-aligned monospace |
| GST (₹) | 80px | CGST+SGST or IGST, right-aligned; tooltip: breakdown |
| Total (₹) | 110px | Incl. GST, right-aligned bold monospace |
| Due Date | 100px | Date; red if past due and status ≠ PAID |
| Paid Date | 90px | Date or "—" |
| Overdue By | 80px | Days integer if overdue; amber if 1–30d, red if 31–60d, dark red if 60+d |
| Status | 110px | Status badge (see colours below) |
| Actions | 48px | 3-dot kebab menu |

**Status badge colours:**
- PAID: `bg-green-900/50 text-green-400`
- OVERDUE: `bg-red-900/50 text-red-400` + pulsing dot
- SENT: `bg-blue-900/50 text-blue-300`
- DRAFT: `bg-slate-800 text-slate-400`
- PARTIALLY_PAID: `bg-amber-900/50 text-amber-300`
- WRITTEN_OFF: `bg-slate-800 text-slate-500 line-through`
- VOID: `bg-slate-800 text-slate-600 italic`

**Row background tints:**
- OVERDUE rows: faint `bg-red-950`
- DRAFT rows: faint `bg-slate-900`

**Stale overdue rows (>60d):** left border 3px red; tooltip: "60+ days overdue — consider escalating to Collections."

---

### Kebab Menu Actions

| Action | Available When | Requires |
|---|---|---|
| View Invoice | Always | — |
| Download PDF | Always | — |
| Send / Resend | SENT, OVERDUE, DRAFT | Billing Admin (#70), FM (#69) |
| Mark as Paid | SENT, OVERDUE, PARTIALLY_PAID | Billing Admin (#70), FM (#69) + 2FA |
| Record Partial Payment | SENT, OVERDUE | Billing Admin (#70), FM (#69) + 2FA |
| Write Off | OVERDUE, PARTIALLY_PAID | FM (#69) only + 2FA |
| Void | DRAFT only | Billing Admin (#70), FM (#69) |
| Duplicate | Any non-VOID | Billing Admin (#70) |
| Log Follow-up | OVERDUE only | AR Exec (#71), Collections Exec (#102) |
| Create Refund Request | PAID, PARTIALLY_PAID | Billing Admin (#70), FM (#69) |

---

## Bulk Actions

Available to Billing Admin (#70) and FM (#69). Appears when ≥ 1 row selected. Max 50 rows at a time.

| Bulk Action | Behaviour |
|---|---|
| Send Reminder | Confirmation modal: "Send reminders to N institutions?" with email preview. POST `/finance/invoices/bulk-remind/`. Logs each send in `finance_invoice.send_count`. Toast: "Reminders sent to N institutions." |
| Export Selected | Synchronous CSV of the ≤ 50 selected rows (bypasses async threshold). |
| Mark as Paid (bulk) | Opens bulk-pay modal: batch payment reference + date input. All selected invoices must be in SENT or OVERDUE status (validation: mixed-status selection shows error "Cannot bulk-pay invoices in multiple statuses — filter to SENT or OVERDUE first"). FM + 2FA required. |
| Send to Collections | Billing Admin can bulk-assign overdue invoices to Collections Exec (#102) — sets `finance_ar_aging.assigned_collector_id`. Confirmation: "Assign N overdue invoices to collections queue?" |

---

## Invoice Detail Drawer (640px)

Right-side drawer opened by row click or [View Invoice] action.

```
┌──────────────────────────────────────────────────────┐
│  INV-2026-00841  ● OVERDUE                 [×]  [PDF]│
│  ABC Coaching Centre · Feb 2026                      │
├──────────────────────────────────────────────────────┤
│  INVOICE DETAILS                                     │
│  Issue: 01 Feb 2026    Due: 28 Feb 2026  (22d over.) │
│  Billing Period: Feb 2026    Plan: Enterprise        │
│  PO Number: PO-2026-ABC-001                          │
├──────────────────────────────────────────────────────┤
│  LINE ITEMS                                          │
│  Enterprise Plan — Feb 2026     1 × ₹1,40,000        │
│  Additional API calls (1M)      1 × ₹10,000          │
│  Subtotal                               ₹1,50,000    │
│  CGST @ 9%                              ₹13,500      │
│  SGST @ 9%                              ₹13,500      │
│  Total                                  ₹1,77,000    │
│  Paid to date                           ₹0           │
│  Outstanding                            ₹1,77,000    │
├──────────────────────────────────────────────────────┤
│  PAYMENT TIMELINE                                    │
│  ● Invoice generated — 01 Feb 2026                   │
│  ● Sent to billing@abc.com — 01 Feb 2026             │
│  ⚠ Reminder sent — 05 Mar 2026 (6d overdue)          │
│  ✗ Still unpaid — as of today (22 days overdue)      │
├──────────────────────────────────────────────────────┤
│  FOLLOW-UP LOG (from finance_ar_followup)            │
│  14 Mar — Phone Call — "Promised to pay by 20 Mar"   │
│  05 Mar — Reminder Email — auto                      │
├──────────────────────────────────────────────────────┤
│  ACTIONS                                             │
│  [Mark as Paid] [Send Reminder] [Write Off] [Close]  │
└──────────────────────────────────────────────────────┘
```

**Line Items section:** Shows all items from `finance_invoice.line_items_json`. For auto-generated invoices, single line item = plan name + billing period. For manually generated: multiple items.

**GST display logic:** If `cgst_paise > 0 AND sgst_paise > 0` → show as CGST @ 9% + SGST @ 9% (intra-state). If `igst_paise > 0` → show as IGST @ 18% (inter-state). Never show both simultaneously.

**Payment Timeline:** Chronological list of events: `created_at` (generated), `last_sent_at` (sent), any `finance_ar_followup` records, and current status. Most recent event at bottom. Green dot = positive, amber = warning, red = negative.

**Follow-up Log:** Lists `finance_ar_followup` records for this invoice (newest first). Shows followup_type badge + notes + created_by name + date. [+ Log Follow-up] button for AR Exec (#71) and Collections Exec (#102).

---

## Generate Invoice Modal (560px)

Triggered by [+ Generate Invoice]. Requires Billing Admin (#70) or FM (#69).

```
┌─────────────────────────────────────────────────────────┐
│  Generate Invoice                                        │
├─────────────────────────────────────────────────────────┤
│  Institution*   [Search institution...              ]    │
│  Billing Period* [Month ▼] [Year ▼]   (Feb 2026)        │
│  Plan Tier       [Auto-detected from subscription]       │
│  GST Type*       [CGST+SGST ▼]  (CGST+SGST or IGST)    │
│  Line Items                                              │
│  ┌─────────────────────────────┬──────┬────────┬──────┐ │
│  │ Description                 │ Qty  │ Unit ₹ │ Amt  │ │
│  │ [Enterprise Plan — Feb 26]  │ [1]  │[1,40,000]│ auto│ │
│  └─────────────────────────────┴──────┴────────┴──────┘ │
│  [+ Add Line Item]                                       │
│                                Subtotal:   ₹1,40,000    │
│                                CGST 9%:    ₹12,600      │
│                                SGST 9%:    ₹12,600      │
│                                Total:      ₹1,65,200    │
│  PO Number (optional)   [PO-2026-XXX                ]   │
│  Due Date*  [28 Feb 2026]  (30 days from today default) │
│  Auto-Send ☑  (email invoice on generation)             │
├─────────────────────────────────────────────────────────┤
│  ⚠ An invoice for this institution + period already     │
│  exists (INV-2026-00841, status: OVERDUE). Generating   │
│  a new one will create a duplicate — are you sure?      │
├─────────────────────────────────────────────────────────┤
│  [Cancel]          [Save Draft]     [Generate & Send]   │
└─────────────────────────────────────────────────────────┘
```

**Field validation:**
- Institution: required; typeahead search on `institution.name`; loads existing subscription details on selection (plan tier, ARR, billing contact)
- Billing Period: required; month+year picker; defaults to current month
- GST Type: required; auto-suggested based on institution's state vs EduForge's registered state (Telangana). If institution.state == 'Telangana' → CGST+SGST; else → IGST. User can override.
- Line Items: at least one required; Description min 3 chars; Qty ≥ 1 integer; Unit Price ≥ 0 paise
- Total auto-computes in real-time as line items are modified
- PO Number: optional; max 100 chars
- Due Date: required; must be ≥ today; default: today + 30 days
- Auto-Send: checkbox; if checked, triggers email + `send_count++` on save

**Duplicate guard:** On institution selection, server checks for existing non-VOID invoice for that institution + billing period. If found: amber warning with existing invoice_number. User must explicitly confirm to proceed.

**Invoice number auto-generation:** Format is `INV-{YYYY}-{NNNNN}` (e.g., `INV-2026-00841`). Sequence is global per calendar year, zero-padded to 5 digits. Implementation uses PostgreSQL sequence `finance_invoice_number_seq_{year}` (created at first invoice of each year). Concurrency-safe: number assigned at INSERT using `nextval('finance_invoice_number_seq_{year}')` inside the transaction; no application-level locking needed. Year rollover: sequence name includes year, so `INV-2027-00001` resets automatically. VOID invoices do NOT release their sequence number back (gaps acceptable for audit trail integrity).

**Invoice PDF template:** Server-side WeasyPrint render. Template: `finance/templates/invoice.html`. Fields: invoice_number, issue_date, due_date, institution_name, institution_gstin, billing_address, line_items_json (rendered as table: description, HSN/SAC 9993, quantity, rate, amount), subtotal, CGST 9% + SGST 9% (intra-state) **OR** IGST 18% (inter-state) — never both, total, payment_instructions, EduForge bank details, terms & conditions. PDF filename: `INV-{number}.pdf`.

**[Save Draft]:** POST `/finance/invoices/create/?action=draft`. Creates DRAFT invoice. No email sent. Toast: "Invoice saved as draft — INV-YYYY-NNNNN."

**[Generate & Send]:** POST `/finance/invoices/create/?action=send`. Creates SENT invoice. Triggers email to institution billing contact (via F-06 Notification Manager). Toast: "Invoice INV-YYYY-NNNNN generated and sent to [email]."

---

## Mark as Paid Modal (480px)

| Field | Type | Validation |
|---|---|---|
| Invoice | Read-only (invoice_number + total) | — |
| Amount paid (₹)* | Decimal input (₹, converts to paise) | > 0; ≤ invoice outstanding; if < outstanding: status → PARTIALLY_PAID |
| Payment date* | Date picker | Required; ≤ today |
| Payment mode* | Select | NEFT / IMPS / UPI / RAZORPAY / CHEQUE / OTHER |
| Reference #* | Text | Required; min 4 chars |
| Notes | Textarea | Optional; max 500 chars; HTML-escaped on display |
| 2FA code* | TOTP input | Required |

**Partial payment accumulation:** `paid_amount_paise` is **accumulated** across multiple payments, not replaced. Example: Invoice total ₹2L → first payment ₹1L sets `paid_amount_paise=100000`; second payment ₹0.8L sets `paid_amount_paise=180000`; third payment ₹0.2L sets `paid_amount_paise=200000` and `status=PAID`. The "Amount paid" input on this modal is validated against `invoice.total_paise - invoice.paid_amount_paise` (current outstanding), not invoice total.

**Submit:** PATCH `/finance/invoices/{id}/status/`. Updates `paid_amount_paise` (appended), `status`, `paid_date`, `payment_reference`, `payment_mode`. Creates `finance_payment` record. If `paid_amount_paise < total_paise`: status = PARTIALLY_PAID. If `paid_amount_paise >= total_paise`: status = PAID.

Toast (on success): "Payment of ₹[amount] recorded for INV-[number]. Status updated to [PAID/PARTIALLY_PAID]."

---

## Write-Off Modal (480px — FM #69 only, with 2FA)

```
  Write Off Invoice
  ─────────────────────────────────────────────────────
  INV-2026-00841 · ₹1,77,000 · ABC Coaching · 90+ days
  ─────────────────────────────────────────────────────
  Outstanding balance:   ₹1,77,000
  Reason*  [IRRECOVERABLE_DEBT ▼]
  Notes*   [Institution closed; contact unresponsive... ]
  2FA code*  [      ]

  ⚠ This action is PERMANENT and cannot be reversed.
  The outstanding balance will be removed from AR.
  ─────────────────────────────────────────────────────
  [Cancel]                          [Confirm Write Off]
```

- Reason dropdown: IRRECOVERABLE_DEBT / GOODWILL / BILLING_ERROR / DUPLICATE / OTHER
- Notes required (min 20 chars)
- 2FA required (TOTP)
- On confirm: `finance_invoice.status → WRITTEN_OFF`, `voided_by_id`, `voided_at`, `void_reason` set. Writes to `finance_audit_log`.
- Notifies AR Exec (#71) and Collections Exec (#102) assigned to that institution.

---

## Export CSV

**Columns (22):** invoice_id, invoice_number, institution_id, institution_name, institution_type, plan_tier, billing_period, issue_date, due_date, paid_date, subtotal_inr, cgst_inr, sgst_inr, igst_inr, total_inr, paid_amount_inr, status, overdue_days, payment_mode, payment_reference, created_by, auto_generated

**Sync export (≤ 500 rows):** Immediate download. **Async export (> 500 rows):** Celery task, email with signed S3 URL.

**Role restriction:** FM (#69), Billing Admin (#70), GST Consultant (#72) can export. AR Exec (#71), Analyst (#101) read only — no bulk export of payment reference data.

---

## Empty States

| Condition | Message | CTA |
|---|---|---|
| No invoices match filters | "No invoices match your current filters." | [Clear Filters] |
| Overdue tab: no overdue invoices | "No overdue invoices — collection rate is 100% this period!" | — |
| Draft tab: no drafts | "No draft invoices." | [+ Generate Invoice] |
| Void tab: no void invoices | "No void invoices." | — |

---

## Toast Messages

| Action | Toast | Type |
|---|---|---|
| Invoice generated (draft) | "Draft invoice INV-YYYY-NNNNN created." | Green |
| Invoice generated + sent | "Invoice INV-YYYY-NNNNN sent to [email]." | Green |
| Payment recorded | "₹[amount] payment recorded — status: [PAID/PARTIALLY_PAID]." | Green |
| Invoice sent/resent | "Invoice resent to [email]." | Green |
| Bulk reminder sent | "Reminders sent to N institutions." | Green |
| Write-off confirmed | "Invoice INV-YYYY-NNNNN written off." | Amber (warning) |
| Invoice voided | "Invoice INV-YYYY-NNNNN voided." | Amber |
| Duplicate invoice warning | "An invoice for [institution] + [period] already exists." | Amber (non-blocking) |
| 2FA failed | "2FA verification failed. Please retry." | Red |
| Export queued | "Export queued — download link will be emailed to [email]." | Amber |

---

## Authorization

**Route guard:** `@division_m_required(allowed_roles=[69, 70, 71, 72, 73, 101, 102])`.

| Scenario | Behaviour |
|---|---|
| Billing Admin (#70) | Full CRUD on invoices. Cannot write off (FM only). |
| AR Exec (#71) | Read-only on OVERDUE tab only. No create/edit/send. Can log follow-ups. |
| GST Consultant (#72) | Read-only across all tabs; can filter by period for GSTR-1 prep; export allowed. |
| Collections Exec (#102) | Read OVERDUE only; can log follow-ups; [Suspend Account] action visible |
| Finance Analyst (#101) | Read-only across all; no aggregated-only restriction (can see individual invoices); no export of payment reference data |
| Finance Manager (#69) | Full; exclusive: write-off + bulk write-off |
| Write endpoint without 2FA header | 403 for mark-paid/write-off operations |

---

## Role-Based UI Visibility Summary

| Feature | 69 FM | 70 Billing | 71 AR Exec | 72 GST | 101 Analyst | 102 Collections |
|---|---|---|---|---|---|---|
| All tabs visible | Yes | Yes | Overdue only | Yes (read) | Yes (read) | Overdue only |
| [+ Generate Invoice] | Yes | Yes | No | No | No | No |
| Send / Resend | Yes | Yes | No | No | No | No |
| Mark as Paid | Yes + 2FA | Yes + 2FA | No | No | No | No |
| Record Partial Payment | Yes + 2FA | Yes + 2FA | No | No | No | No |
| Write Off | Yes + 2FA | No | No | No | No | No |
| Void (Draft) | Yes | Yes | No | No | No | No |
| Log Follow-up | No (FM uses other tools) | No | Yes | No | No | Yes |
| Create Refund Request | Yes | Yes | No | No | No | No |
| Send to Collections (bulk) | Yes | Yes | No | No | No | No |
| Export CSV | Yes | Yes | No | Yes (for GSTR) | No | No |
| Invoice Detail Drawer | Full | Full | Partial (no actions) | Full (read) | Full (read) | Partial (follow-up only) |
| [?nocache=true] | Yes | No | No | No | Yes | No |

---

## Performance Requirements

| Metric | Target | Notes |
|---|---|---|
| Initial page load (SSR) | < 1.5s P95 | Invoice table is live (no cache); status tab counts cached 1 min |
| Invoice table (25 rows) | < 400ms P95 | No Memcached; direct DB query with indexed filters |
| Invoice detail drawer (live) | < 300ms P95 | `finance_invoice` + `finance_payment` + `finance_ar_followup` JOIN |
| Invoice PDF generation | < 3s P95 | WeasyPrint server-side; synchronous for single invoice |
| CSV export (≤ 500 rows) | < 3s P95 | Synchronous streaming response |
| CSV export (> 500 rows) | Async; email within 3 min | Celery task |
| Bulk send reminder (≤ 50) | < 5s P95 | Queued to notification service |
| Concurrent invoice actions | Up to 10 simultaneous Billing Admin writes | Optimistic lock on `finance_invoice.updated_at` prevents double-pay |

---

## Keyboard Shortcuts

| Key | Action |
|---|---|
| `g` `i` | Go to Billing Invoices (M-03) |
| `n` | Open Generate Invoice modal (Billing Admin, FM) |
| `/` | Focus institution search |
| `e` | Export CSV (FM, Billing Admin, GST Consultant) |
| `1`–`8` | Switch to tab 1–8 (ALL, DRAFT, SENT … WRITTEN_OFF) |
| `←` / `→` | Previous / next page in invoice table |
| `Esc` | Close open drawer or modal |
| `?` | Show keyboard shortcut help overlay |

