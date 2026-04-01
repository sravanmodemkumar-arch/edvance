# div-a-10 — Billing & Invoices

## 1. Platform Scale Reference

| Dimension | Value |
|---|---|
| Total institutions | 2,050 |
| Monthly invoices generated | ~2,050 |
| Annual invoices total | ~24,600 |
| Invoice amount range | ₹500 (Starter) – ₹2,00,000+ (Enterprise custom) |
| GST rate | 18% |
| Payment gateway | Razorpay |
| Overdue invoice rate | ~3–5% |
| Auto-retry on failed payments | 3 attempts (Day 1, Day 3, Day 7) |
| Currency | INR only |
| Decimal precision | `Decimal(28,2)` — never float |

**Why this matters:** Billing & Invoices is the receivables ledger. Finance uses it to chase overdue accounts, operations uses it to unlock suspended institutions post-payment, and the COO monitors collection health. Every invoice action (mark paid, write-off) must be audited.

---

## 2. Page Metadata

| Field | Value |
|---|---|
| Page title | Billing & Invoices |
| Route | `/exec/billing/` |
| Django view | `BillingInvoicesView` |
| Template | `exec/billing_invoices.html` |
| Priority | P1 |
| Nav group | Finance |
| Required role | `exec`, `superadmin`, `finance`, `ops` |
| 2FA required | Mark Paid / Write Off / Generate Invoice |
| HTMX poll | Overdue summary: every 5 min |

---

## 3. Wireframe

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ HEADER: Billing & Invoices              [+ Generate Invoice] [Export ▾]     │
├──────────┬──────────┬──────────┬──────────┬──────────┬──────────────────────┤
│ Total    │ Paid     │ Overdue  │ Overdue  │ Pending  │  Collections         │
│ Invoiced │ (period) │ Count    │ Balance  │ (draft)  │  Rate                │
│ ₹42.8 L  │ ₹38.4 L  │    62    │ ₹8.4 L   │   18     │  96.2%               │
├──────────┴──────────┴──────────┴──────────┴──────────┴──────────────────────┤
│ TABS: [All Invoices] [Overdue] [Pending] [Paid] [Draft]                     │
├──────────────────────────────────────────────────────────────────────────────┤
│ [🔍 Search institution, invoice #...]                                        │
│ [Type ▾] [Plan ▾] [Period ▾] [Status ▾] [Amount Range ▾]                   │
│ Active filters: Status: Overdue ×                               [Clear all] │
├──────────────────────────────────────────────────────────────────────────────┤
│ [☐] [Bulk: Send Reminder / Export]  Showing 1–25 / 62  Sort: [Due Date ▾]  │
├──────────────────────────────────────────────────────────────────────────────┤
│ ☐ │ Invoice # │ Institution │ Period │ Amount │ Due Date │ Status │ ⋯       │
│   │ INV-0841  │ ABC Coaching│ Mar 25 │ ₹42,480│ 01 Mar   │ ● Overd│         │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Sections — Deep Specification

### 4.1 KPI Strip

**Container:** `flex gap-4 p-4` · 6 cards · poll every 5 min
**All amounts:** Decimal formatted `₹XX.X L`

| # | Card | Detail | Alert |
|---|---|---|---|
| 1 | Total Invoiced (period) | Sum of all invoices in current period | — |
| 2 | Paid (period) | Sum of paid invoices | — |
| 3 | Overdue Count | Invoices past due date, status ≠ Paid | > 100 = amber |
| 4 | Overdue Balance | Sum of overdue invoice amounts | > ₹20L = red |
| 5 | Pending (draft/sent) | Count of not-yet-due invoices | — |
| 6 | Collections Rate | Paid ÷ Total Invoiced (period) | < 90% = red |

---

### 4.2 Tab Bar

Tabs: All Invoices · Overdue · Pending · Paid · Draft
**Count badges on Overdue and Draft tabs:** `ml-1.5 bg-[#EF4444] text-white text-xs px-1.5 rounded-full` (Overdue) · `bg-[#475569]` (Draft)
**Active tab:** `border-b-2 border-[#6366F1] text-white`
**Each tab click:** `hx-get="?part=invoice_table&status={tab_status}"` `hx-target="#invoice-table"` `hx-swap="innerHTML"`

---

### 4.3 Search & Filter Bar

**Search:** `<input>` full-width · placeholder "Search by institution name, invoice number, amount..." · debounced 400ms
**Filters (below search):**

| Filter | Type | Options |
|---|---|---|
| Institution Type | Multi-select | All / School / College / Coaching / Group |
| Plan | Multi-select | Starter / Standard / Professional / Enterprise |
| Billing Period | Month picker (range) | Any month/range |
| Status | Multi-select | Draft / Sent / Paid / Overdue / Partially Paid / Written Off |
| Amount Range | Range inputs | Min ₹ / Max ₹ |

**Active filter chips:** `flex flex-wrap gap-2 pb-2` · each chip `text-xs bg-[#1E2D4A]` with `×` remove

---

### 4.4 Invoice Table Toolbar

`flex items-center justify-between px-4 py-3 border-b border-[#1E2D4A]`

**Left:**
- Select-all checkbox (indeterminate state when partial)
- Bulk actions: [Send Reminder] [Export Selected] [Mark Paid] (bulk only for Finance role)
- Count badge "N selected"

**Right:**
- Sort dropdown: Due Date ↓ / Amount ↓ / Institution A–Z / Overdue Days ↓
- "Showing X–Y of Z invoices"

---

### 4.5 Invoice Table

`id="invoice-table"` · `hx-get="/exec/billing/?part=invoice_table"` on load

**Container:** `bg-[#0D1526] rounded-xl border border-[#1E2D4A] overflow-x-auto`
**Row click:** opens Invoice Detail Drawer (§5.1)

#### Column Specifications

| Column | Sort | Width | Detail |
|---|---|---|---|
| ☐ | — | 40px | Select checkbox |
| Invoice # | ✓ | 120px | `INV-XXXXX` · monospace · clickable |
| Institution | ✓ | 220px | Name + type icon · truncated |
| Billing Period | ✓ | 100px | e.g., "Feb 2025" |
| Subtotal | ✓ | 100px | Pre-GST · right-aligned `font-mono` |
| GST (18%) | — | 80px | GST amount · right-aligned |
| Total | ✓ | 100px | Including GST · right-aligned `font-mono font-semibold` |
| Due Date | ✓ | 100px | Date · red if past due |
| Paid Date | ✓ | 100px | Date or `—` |
| Overdue By | ✓ | 90px | Days (shown only if overdue) · red |
| Status | ✓ | 110px | Status badge (see below) |
| Actions ⋯ | — | 48px | Kebab menu |

**Status badge colours:**
- Paid: `bg-[#064E3B] text-[#34D399]`
- Overdue: `bg-[#450A0A] text-[#F87171]` + pulsing dot
- Pending/Sent: `bg-[#1E3A5F] text-[#60A5FA]`
- Draft: `bg-[#1E293B] text-[#475569]`
- Partially Paid: `bg-[#451A03] text-[#FCD34D]`
- Written Off: `bg-[#1E293B] text-[#94A3B8] line-through`

**Overdue row tint:** `bg-[#1A0A0A]` background on overdue rows

**Kebab menu actions:**
- View Invoice (opens drawer)
- Download PDF
- Send Reminder (if overdue/pending)
- Mark as Paid (requires 2FA; shown if not paid)
- Write Off (requires 2FA; Finance role only)
- Void Invoice (Draft only)
- Duplicate Invoice

---

### 4.6 Pagination Strip

`flex items-center justify-between px-4 py-3`
- "Showing X–Y of Z invoices" `text-sm text-[#94A3B8]`
- Page pills: [← Prev] [1] [2] … [N] [Next →]
- Per-page: 10 / 25 / 50 / 100
- HTMX: `hx-get="?part=invoice_table&page={n}&per_page={pp}&status={tab}"` `hx-target="#invoice-table"` `hx-push-url="true"`

---

## 5. Drawers

### 5.1 Invoice Detail Drawer (640 px)

`id="invoice-drawer"` · `w-[640px]` · right panel · `body.drawer-open`

**Header (72px):**
`flex items-center justify-between px-6 py-5 border-b border-[#1E2D4A]`
- Left: Invoice number `text-lg font-bold text-white` + Status badge
- Sub-line: Institution name · Billing period
- Right: `[Download PDF]` + `[×]`

**Section A — Invoice Details (grid 2-col):**
```
Invoice #   INV-00841          Issue Date    01 Feb 2025
Institution  ABC Coaching       Due Date      28 Feb 2025
Billing Period Feb 2025         Paid Date     —
Plan         Enterprise         PO Number     PO-2025-ABC-001
```

**Section B — Line Items:**
`<table class="w-full text-sm">`
| Description | Qty | Unit Price | Amount |
|---|---|---|---|
| Enterprise Plan — Feb 2025 | 1 | ₹1,40,000 | ₹1,40,000 |
| Additional API calls (1M × ₹0.01) | 1,000,000 | ₹0.01 | ₹10,000 |
| Subtotal | | | ₹1,50,000 |
| GST @ 18% | | | ₹27,000 |
| **Total** | | | **₹1,77,000** |

**Section C — Payment Timeline:**
Vertical timeline `flex flex-col gap-3`:
- `[dot] Invoice generated — 01 Feb 2025`
- `[dot] Invoice sent to billing@abc.com — 01 Feb 2025`
- `[dot amber] Reminder sent — 05 Mar 2025 (overdue by 5 days)`
- `[dot red] Still unpaid — as of today`

**Section D — Actions (footer 56px):**
`flex gap-3 px-6 py-4 border-t border-[#1E2D4A]`
[Download PDF] [Send Reminder] [Mark as Paid] [Write Off] [Close]

**Mark as Paid modal** (opens inline in drawer): Amount input (pre-filled) · Payment date · Payment mode (NEFT/IMPS/Razorpay/Cheque) · Reference number · Notes · 2FA required

---

## 6. Modals

### 6.1 Generate Invoice Modal (560 px)

Triggered by [+ Generate Invoice]. **2FA required.**

**Fields:**
| Field | Type | Detail |
|---|---|---|
| Institution | Searchable dropdown | Required |
| Billing period | Month/year picker | Default: current month |
| Line items | Repeatable rows | Description / Qty / Unit Price / Amount |
| [+ Add line item] | Button | Adds new row |
| Subtotal | Auto-calculated | Read-only |
| GST (18%) | Auto-calculated | Read-only |
| Total | Auto-calculated | Read-only bold |
| PO number | Text input | Optional |
| Due date | Date picker | Default: 30 days from today |
| Auto-send | Checkbox | Send to billing contact on creation |

**Footer:** [Cancel] [Save Draft] [Generate & Send]

---

### 6.2 Mark as Paid Modal (480 px)

| Field | Type | Validation |
|---|---|---|
| Invoice | Read-only display | |
| Amount paid | Decimal input | ≤ invoice total |
| Payment date | Date picker | Required |
| Payment mode | Select | NEFT / IMPS / UPI / Razorpay / Cheque / Other |
| Reference # | Text | Required |
| Notes | Textarea | Optional |
| 2FA code | OTP input | Required |

**Footer:** [Cancel] [Confirm Payment]

---

### 6.3 Bulk Send Reminders Modal (480 px)

"Send reminders to {N} overdue institutions?"
- Preview of email template (read-only with edit toggle)
- Total overdue amount shown: `₹XX.X L across {N} institutions`
**Footer:** [Cancel] [Send All Reminders]

---

## 7. HTMX Architecture

| Part param | Template | Trigger |
|---|---|---|
| `?part=kpi` | `exec/partials/billing_kpi.html` | Page load · poll 5 min |
| `?part=invoice_table` | `exec/partials/invoice_table.html` | Tab click · search · filter · sort · page |
| `?part=invoice_drawer&id={id}` | `exec/partials/invoice_drawer.html` | Row click |
| `?part=mark_paid&id={id}` | Modal POST | Mark Paid modal submit |
| `?part=generate_invoice` | Modal POST | Generate Invoice modal submit |

**Django view dispatch:**
```python
class BillingInvoicesView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "portal.view_billing"

    def get(self, request):
        ctx = self._build_context(request)
        if _is_htmx(request):
            part = request.GET.get("part", "")
            templates = {
                "kpi": "exec/partials/billing_kpi.html",
                "invoice_table": "exec/partials/invoice_table.html",
                "invoice_drawer": "exec/partials/invoice_drawer.html",
            }
            if part in templates:
                return render(request, templates[part], ctx)
        return render(request, "exec/billing_invoices.html", ctx)

    def post(self, request):
        part = request.GET.get("part", "")
        if part == "mark_paid":
            return self._handle_mark_paid(request)
        if part == "generate_invoice":
            return self._handle_generate(request)
        return HttpResponseNotAllowed(["GET"])
```

---

## 8. Performance Requirements

| Metric | Target | Critical |
|---|---|---|
| KPI strip | < 300 ms | > 800 ms |
| Invoice table (25 rows) | < 400 ms | > 1 s |
| Invoice drawer | < 250 ms | > 700 ms |
| PDF download generation | < 3 s | > 8 s |
| Full page initial load | < 1 s | > 2.5 s |

---

## 9. States & Edge Cases

| State | Behaviour |
|---|---|
| Invoice partially paid | Status = Partially Paid · amber badge · line items show partial amount |
| Invoice written off | Row strikethrough `line-through` · grey badge · cannot be reopened |
| Duplicate invoice generated for same period | Warning modal "An invoice for ABC Coaching for Feb 2025 already exists. Continue?" |
| Institution suspended for non-payment | Red banner on Institution detail (div-a-06) linking to this invoice |
| PDF generation failed | Toast "PDF generation failed — try again" · log error |
| Mark Paid: amount > invoice total | Error "Amount cannot exceed invoice total ₹X,XXX" |
| Bulk reminder: 0 selected | Button disabled |
| Auto-retry payment failed 3 times | Badge "Auto-pay failed" + alert to finance team |

---

## 10. Keyboard Shortcuts

| Key | Action |
|---|---|
| `N` | Generate new invoice |
| `F` | Focus search |
| `R` | Refresh table |
| `E` | Export filtered list |
| `↑` / `↓` | Navigate table rows |
| `Enter` | Open invoice drawer |
| `Esc` | Close drawer/modal |
| `?` | Keyboard shortcuts help |

---

## 11. Template Files

| File | Purpose |
|---|---|
| `exec/billing_invoices.html` | Full page shell |
| `exec/partials/billing_kpi.html` | KPI strip |
| `exec/partials/invoice_table.html` | Invoice table + pagination |
| `exec/partials/invoice_drawer.html` | Invoice detail drawer |
| `exec/partials/invoice_generate_modal.html` | Generate Invoice modal |
| `exec/partials/mark_paid_modal.html` | Mark Paid modal |
| `exec/partials/bulk_reminder_modal.html` | Bulk reminder confirmation |
| `exec/partials/writeoff_modal.html` | Write-off confirmation |

---

## 12. Component References

| Component | Used in |
|---|---|
| `KpiCard` | §4.1 |
| `TabBar` with count badges | §4.2 |
| `SearchInput` | §4.3 |
| `MultiSelectDropdown` | §4.3 filters |
| `FilterChip` | §4.3 chips |
| `BulkActionsBar` | §4.4 |
| `InvoiceTable` | §4.5 |
| `StatusBadge` | §4.5 Status column |
| `KebabMenu` | §4.5 Actions |
| `PaginationStrip` | §4.6 |
| `DrawerPanel` | §5.1 |
| `InvoiceLineItems` | §5.1 Section B |
| `PaymentTimeline` | §5.1 Section C |
| `ModalDialog` | §6.1–6.3 |
| `LineItemEditor` | §6.1 (repeatable rows) |
| `PollableContainer` | KPI strip |
