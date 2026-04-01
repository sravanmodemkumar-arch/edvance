# 34 — GST & Tax Compliance

---

## 1. Page Metadata

| Field | Value |
|---|---|
| Page title | GST & Tax Compliance |
| Route | `/exec/gst-compliance/` |
| Django view | `GSTComplianceView` |
| Template | `exec/gst_compliance.html` |
| Priority | **P1** |
| Nav group | Financial |
| Required roles | `cfo` · `finance_manager` · `gst_consultant` · `ceo` · `superadmin` |
| COO access | Read-only (no actions) |
| CTO / Engineering | Denied — redirect to `/exec/dashboard/` |
| HTMX poll — filing calendar | No auto-poll (static schedule) |
| HTMX poll — liability strip | Every 120s |
| Cache | Liability strip: Redis TTL 115s · GSTR data: Redis TTL 1800s |
| Theme tokens | bg-base `#040810` · surface-1 `#08101E` · surface-2 `#0D1828` · accent `#6366F1` · success `#22C55E` · danger `#EF4444` · warn `#F59E0B` |

---

## 2. Purpose & Business Logic

**Why this page must exist:**

EduForge provides online education services under **SAC code 9993** (Education Services). Under Indian GST law:
- B2B sales to GST-registered institutions: **18% GST** (CGST 9% + SGST 9% for intra-state, IGST 18% for inter-state)
- The institution's GSTIN determines intra vs inter-state — this must be validated at onboarding
- EduForge must file **GSTR-1** (outward supplies) by the 11th of every month and **GSTR-3B** (summary return + tax payment) by the 20th of every month
- **TDS under Section 194J** applies to certain service payments EduForge receives (coaching centre contracts may attract TDS at 10%)
- **Input Tax Credit (ITC)** — EduForge can claim ITC on B2B expenses (AWS, Razorpay fees, office expenses) to offset output GST liability

**The operational risk:**

At Rs.60 Cr ARR with 2,050 institutions across all Indian states:
- A missed GSTR-3B filing = **Rs.50/day late fee** per return + interest at 18% p.a. on unpaid tax
- A GSTIN mismatch on an invoice = **ITC reversal risk** for the institution (they lose their tax credit if EduForge's invoice is wrong)
- ITC reconciliation failure (GSTR-2A mismatch) = **manual notice from GST department**
- Non-deduction of TDS where applicable = **30% disallowance** of the expense + penalty

The CFO and GST Consultant currently must cross-reference the GST portal, Tally/accounting software, and Razorpay data across 3 separate systems on the 10th of each month under deadline pressure. This page consolidates all three.

**What decisions this page enables:**
- Is GSTR-1 data ready to file by the 11th? → GST Consultant can see outstanding invoices not yet tagged with correct GSTIN
- Has GSTR-3B liability been computed and reviewed? → CFO approves before filing
- Which states have intra-state customers? → Finance confirms CGST/SGST split is correct
- Are there ITC mismatches between EduForge's books and GSTR-2A (supplier-reported)? → Finance raises with suppliers before the reconciliation window closes
- Is TDS deducted correctly from applicable coaching centre payments? → Prevents 194J notices

---

## 3. User Roles & Access

| Role | Can View | Can Act | Specific Capabilities |
|---|---|---|---|
| CEO / Platform Owner | All sections | Mark filing done, download reports | Cannot edit tax data |
| CFO | All sections | Approve GSTR-3B pre-filing checklist, flag mismatches, export | Read-only per Level 1 — no data mutation |
| Finance Manager (Level 1) | All sections | Same as CFO | Read-only |
| GST Consultant (Level 1) | All sections | Mark filing status, add notes per filing | Specialist read-only role |
| COO | All sections | Read-only | No financial actions |
| Billing Admin | No access | — | Redirect with message |
| CTO / Engineering | No access | — | Redirect with message |

**Role-based UI:**
- "Mark as Filed" button: GST Consultant / CFO / CEO only
- "Export GSTR data" (CSV for Tally import): CFO / Finance Manager only
- Amount fields: hidden for COO (sees filing status and deadlines only, not rupee values)

---

## 4. Section-wise UI Breakdown

---

### Section 1 — Page Header & Alert Bar

**Purpose:** Immediate deadline awareness. The CFO opening this page on the 9th of a month needs to see "GSTR-1 due in 2 days" before anything else.

**User interaction:**
- Date filter: select financial year (default current FY Apr–Mar)
- Month selector: default current month
- Alert bar auto-shows when a filing deadline is ≤ 5 days away

**UI elements:**
```
GST & Tax Compliance                    [FY 2025–26 ▾]  [Apr 2026 ▾]  [Export]
──────────────────────────────────────────────────────────────────────────────
🔴 GSTR-1 due in 2 days (11 Apr 2026) — 48 invoices pending tagging [Review →]
🟡 GSTR-3B due in 11 days (20 Apr 2026) — Liability computation ready [Review →]
```

- Alert bar: `bg-[#131F38] border-l-4 border-red-500 px-4 py-2 rounded` for red; amber variant for yellow
- Each alert is a full-width row with icon, text, and a `[Review →]` link that scrolls to the relevant section
- If no upcoming deadlines within 5 days: no alert bar shown (clean header)

**Data flow:**
- `filing_deadlines` computed at page load from the `GSTFilingCalendar` model (pre-seeded yearly)
- Days-until calculated against `now().date()`
- Alert shown if `days_until <= 5`

**Role-based behavior:** All roles see the alert bar. COO sees deadline alerts but no rupee amounts in the linked sections.

**Edge cases:**
- Filing already marked complete: alert bar shows green "✅ GSTR-1 filed 9 Apr 2026 · Reference: ARN-AA2604..." instead of red deadline
- Holiday falls on deadline: system uses next working day (pre-configured in `GSTFilingCalendar.deadline_adjusted`)

**Performance:** Alert bar computed from DB at page load (no Redis needed — < 10 records query).

**Mobile:** Alert bar stacks vertically. [Review →] becomes full-width button below each alert.

**Accessibility:** Alert bar has `role="alert" aria-live="assertive"` for red alerts, `aria-live="polite"` for amber.

---

### Section 2 — Tax Liability Strip (KPI Cards)

**Purpose:** "How much GST does EduForge owe this month, and is ITC going to reduce it?" — the CFO's primary financial question before a GSTR-3B filing.

**User interaction:** Read-only. Click "ITC Available" card → scrolls to ITC Reconciliation section.

**UI elements — 6 cards:**

```
╔══════════════╦══════════════╦══════════════╦══════════════╦══════════════╦══════════════╗
║ OUTPUT TAX   ║ CGST/SGST    ║ IGST         ║ ITC AVAILABLE║ NET PAYABLE  ║ TDS (194J)   ║
║              ║              ║              ║              ║              ║              ║
║  ₹22,46,400  ║  ₹18,32,100  ║  ₹4,14,300   ║  ₹3,18,200   ║  ₹19,28,200  ║  ₹1,24,000   ║
║  on ₹1.24 Cr ║  1,842 txns  ║  230 txns    ║  AWS+Rzrpy   ║  to deposit  ║  receivable  ║
╚══════════════╩══════════════╩══════════════╩══════════════╩══════════════╩══════════════╝
```

| Card | Formula | Alert |
|---|---|---|
| Output Tax (18%) | Sum of GST on all invoices in period | None — informational |
| CGST/SGST | Intra-state GST (9%+9%) from institutions in same state as EduForge registration | If > 85% of output tax: amber (unexpected state concentration) |
| IGST | Inter-state GST (18%) from out-of-state institutions | — |
| ITC Available | GST paid on AWS + Razorpay fees + other B2B expenses (from GSTR-2A) | If < 50% of expected: amber (ITC mismatch — may be reconciliation issue) |
| Net Payable | Output Tax − ITC Available | Red if Net Payable > previous month by > 20% (unusual spike) |
| TDS (194J) | TDS deducted at source by coaching centre clients on service fees | If TDS deducted ≠ expected (based on contract values): amber |

**HTMX:** `id="gst-liability-strip"` `hx-get="/exec/gst-compliance/?part=liability&fy={{ fy }}&month={{ month }}"` `hx-trigger="load, every 120s[!document.querySelector('.drawer-open,.modal-open')]"` `hx-swap="innerHTML"`

**Data flow:**
- Backend: aggregation query on `Invoice` model + `PurchaseExpense` model, cached in Redis `gst:liability:2026-04` TTL 115s
- CGST/SGST split: determined by `institution.state == company_registration_state` (pre-computed flag `is_intrastate` on the `Invoice` model)

**Role-based behavior:** All rupee values hidden for COO. Cards render with labels only + "Restricted" in value position.

**Edge cases:**
- ITC not yet reconciled for month: ITC card shows "Pending reconciliation" with amber border. Net Payable shows "~" prefix indicating estimate.
- Zero output tax (no invoices): all cards show ₹0.

**Performance:** Aggregation query indexed on `invoice_date`, `gst_period`. Cached 115s.

**Mobile:** Cards stack in 2×3 grid. Font sizes reduced.

**Accessibility:** Cards `role="region"`. ITC mismatch alert has `aria-live="polite"`.

---

### Section 3 — GSTR Filing Calendar

**Purpose:** The source of truth for what has been filed, what is due, and what is overdue. One row per filing type per month for the full financial year.

**User interaction:**
- Click any row → opens Filing Detail Drawer (480px) with: filing period, computed data summary, ARN number (if filed), filing date, notes
- "Mark as Filed" action per row (GST Consultant / CFO / CEO only)
- Filter: [All] [Pending] [Filed] [Overdue]

**UI elements:**
```
GSTR FILING CALENDAR — FY 2025–26          [Filter: All ▾]
──────────────────────────────────────────────────────────────────────────────
Filing Type   │ Period    │ Deadline   │ Status       │ ARN / Reference │ ⋯
──────────────┼───────────┼────────────┼──────────────┼─────────────────┼──
GSTR-1        │ Apr 2026  │ 11 Apr     │ ⏳ Due 2 days │ —               │ ⋯
GSTR-3B       │ Apr 2026  │ 20 Apr     │ ⏳ Due 11 days│ —               │ ⋯
GSTR-1        │ Mar 2026  │ 11 Mar     │ ✅ Filed      │ ARN-AA2603...   │ ⋯
GSTR-3B       │ Mar 2026  │ 20 Mar     │ ✅ Filed      │ ARN-BB2603...   │ ⋯
GSTR-1        │ Feb 2026  │ 11 Feb     │ ✅ Filed      │ ARN-AA2602...   │ ⋯
GSTR-3B       │ Feb 2026  │ 20 Feb     │ 🔴 Overdue   │ —               │ ⋯
...
```

**Column details:**

| Column | Width | Detail |
|---|---|---|
| Filing Type | 100px | GSTR-1 · GSTR-3B · GSTR-9 (annual) · TDS Return (26Q) |
| Period | 100px | Month name + year |
| Deadline | 100px | Date. Red if overdue, amber if ≤ 5 days |
| Status | 130px | Badge (see below) |
| ARN / Reference | 180px | `font-mono text-xs`. "—" if not filed. Click → copies to clipboard |
| ⋯ | 80px | View Detail · Mark as Filed · Add Note |

**Status badge definitions:**

| Status | Colour | Business meaning |
|---|---|---|
| Filed | Green | ARN received, confirmed filed |
| Due X days | Blue → Amber (≤ 5d) → Red (0d) | Filed not yet |
| Overdue | Red pulsing | Past deadline, not filed |
| Not Applicable | Grey | No supply/liability in this period (nil return) |
| Pending Computation | Amber | Month-end data not finalised |

**"Mark as Filed" modal:**
- Filing Type (pre-filled, read-only)
- Period (pre-filled, read-only)
- ARN Number (required, format validation: 15-char alphanumeric)
- Filing Date (date picker, required, cannot be future)
- Notes (optional, textarea)
- POST `/exec/gst-compliance/actions/mark-filed/` → creates `GSTFiling` record, updates calendar status, audit log

**HTMX:** `id="filing-calendar"` `hx-get="/exec/gst-compliance/?part=calendar&fy={{ fy }}"` `hx-trigger="load"` `hx-swap="innerHTML"` (no polling — static until user marks a filing)

**Data flow:** `GSTFilingCalendar.objects.filter(fy=fy).order_by('-period_end', 'filing_type')`

**Role-based behavior:** "Mark as Filed" in ⋯ menu: visible to GST Consultant / CFO / CEO. Hidden for COO.

**Edge cases:**
- Overdue row detected on load: auto-creates a `ComplianceAlert` if one doesn't exist (idempotent)
- ARN format validation: 15-char alphanumeric regex `^[A-Z]{2}[0-9]{2}[A-Z]{1}[0-9]{7}[A-Z]{1}[0-9]{2}[Z]{1}[0-9A-Z]{1}$` — not exact GST ARN format but catches obvious typos

**Performance:** Calendar has max 24 rows/FY (12 months × 2 filing types + 1 annual). Zero pagination, trivial query.

**Mobile:** Deadline and ARN columns hidden. Status shown as coloured dot + label. Full detail in drawer.

**Accessibility:** Table `role="grid"`. Overdue rows have `aria-label="Overdue"` on status cell. "Mark as Filed" button `aria-label="Mark GSTR-1 April 2026 as filed"`.

---

### Section 4 — State-wise GST Breakdown

**Purpose:** EduForge's output GST must be correctly split between CGST+SGST (intra-state) and IGST (inter-state) based on each institution's registered state vs EduForge's GSTIN state. A single wrong classification → wrong tax deposited → notice from GST department.

**User interaction:**
- Table showing all Indian states where EduForge has active institutions, with tax split
- Click any state row → opens a mini-drawer with list of institutions in that state + their individual invoice amounts and GSTIN status
- "Export to CSV" → downloads state-wise data formatted for GSTR-1 filing

**UI elements:**
```
STATE-WISE GST BREAKDOWN — Apr 2026        [Export for GSTR-1]
──────────────────────────────────────────────────────────────────────────────
State              │ Institutions │ Invoiced   │ Tax Type │ GST Amount  │ GSTIN ✓
───────────────────┼──────────────┼────────────┼──────────┼─────────────┼────────
Andhra Pradesh     │ 312          │ ₹48,20,400 │ IGST 18% │ ₹8,67,672   │ 311/312✅
Telangana          │ 280          │ ₹43,60,200 │ CGST+SGST│ ₹7,84,836   │ 280/280✅
Karnataka          │ 198          │ ₹31,24,800 │ IGST 18% │ ₹5,62,464   │ 196/198⚠
Maharashtra        │ 156          │ ₹24,48,600 │ IGST 18% │ ₹4,40,748   │ 156/156✅
...                │ ...          │ ...        │ ...      │ ...         │ ...
── Sub-total IGST  │ 1,680 inst.  │ ₹1,02,14,0 │ IGST     │ ₹18,38,52K  │
── Sub-total CGST  │ 370 inst.    │ ₹22,26,40K │ CGST+SGST│ ₹4,00,752   │
── TOTAL           │ 2,050 inst.  │ ₹1,24,40K  │          │ ₹22,46,400  │
```

**Column details:**

| Column | Detail |
|---|---|
| State | Indian state name |
| Institutions | Count of billed institutions in state this period |
| Invoiced | Total invoice value (ex-GST) in state. Hidden for COO. |
| Tax Type | IGST (inter-state) or CGST+SGST (intra-state, for EduForge's registration state) |
| GST Amount | Computed at 18%. Hidden for COO. |
| GSTIN ✓ | "X / Y ✅" where X = institutions with valid GSTIN on file, Y = total. Amber if X < Y. |

**GSTIN validation column logic:**
- Green ✅: All institutions in state have valid 15-digit GSTIN on file
- Amber ⚠: Some institutions missing GSTIN (will default to B2C treatment = no ITC for them)
- Red 🔴: One or more institutions have GSTIN that failed format validation

**HTMX:** `id="state-breakdown"` `hx-get="/exec/gst-compliance/?part=state-breakdown&month={{ month }}"` `hx-trigger="load"` `hx-swap="innerHTML"`

**Data flow:**
- `Invoice.objects.filter(period=month).values('institution__state').annotate(count=Count('id'), total=Sum('taxable_value'), gst=Sum('gst_amount'), valid_gstin=Count('id', filter=Q(institution__gstin_valid=True)))`
- Grouped into IGST vs CGST rows based on `institution.state == settings.COMPANY_GST_STATE`
- Cache: `gst:state-breakdown:2026-04` TTL 1800s

**Role-based behavior:** Invoiced and GST Amount columns hidden for COO.

**Edge cases:**
- Institution with missing state in profile: grouped under "Unknown State" row with red ⚠ badge. Clicking → shows list of institutions to fix.
- State total GSTIN mismatch: row gets amber background + "⚠ 2 institutions missing GSTIN — ITC impact for them" tooltip.

**Performance:** Aggregation query with `GROUP BY institution__state`. Index on `invoice.period` + `institution.state`. Cached 30 min — state breakdown doesn't change within a month.

**Mobile:** Invoiced and GSTIN columns hidden. State + Tax Type + GST Amount only.

**Accessibility:** Table has `<caption>State-wise GST breakdown for April 2026</caption>`. GSTIN status has `aria-label`.

---

### Section 5 — ITC Reconciliation

**Purpose:** EduForge claims Input Tax Credit on its B2B purchases (AWS, Razorpay, office vendors). The claimed ITC must match what suppliers have reported in their own GSTR-1 (visible in EduForge's GSTR-2A). Mismatches = ITC reversal risk.

**User interaction:**
- Table comparing EduForge's book ITC vs GSTR-2A (what suppliers reported)
- Each row: one vendor/supplier
- Click row → mini-drawer: individual invoices, amounts, match/mismatch detail
- "Flag Mismatch" action per row (for follow-up with supplier)

**UI elements:**
```
ITC RECONCILIATION — Apr 2026        Status: 3 mismatches found ⚠
──────────────────────────────────────────────────────────────────────────────
Vendor            │ Our Books (ITC) │ GSTR-2A (Supplier)│ Difference │ Status
──────────────────┼─────────────────┼───────────────────┼────────────┼────────
Amazon AWS        │ ₹1,24,200       │ ₹1,24,200          │ ₹0         │ ✅ Match
Razorpay          │ ₹18,400         │ ₹18,400            │ ₹0         │ ✅ Match
Exotel            │ ₹8,200          │ ₹6,400             │ -₹1,800    │ ⚠ Mismatch
Office Supplies   │ ₹4,100          │ ₹0                 │ -₹4,100    │ 🔴 Not in 2A
─────────────────────────────────────────────────────────────────────────────
Total ITC Claimed │ ₹1,54,900       │ ₹1,49,000          │ -₹5,900    │ ⚠ Review
```

**HTMX:** `id="itc-recon"` `hx-get="/exec/gst-compliance/?part=itc&month={{ month }}"` `hx-trigger="load"` `hx-swap="innerHTML"`

**Data flow:**
- EduForge book ITC: from `PurchaseExpense` model with `gst_claimed=True`
- GSTR-2A data: synced from GST portal via `GSTINClient` (Python library or GST Suvidha Provider API), stored in `GSTR2ARecord` model
- Comparison: `LEFT JOIN GSTR2ARecord ON vendor_gstin + invoice_number`

**Edge cases:**
- GSTR-2A not yet available (supplier hasn't filed): row shows "Supplier filing pending" — cannot reconcile yet
- Total mismatch > Rs.10,000: amber banner above table: "⚠ ITC mismatch of Rs.X may need reversal in GSTR-3B before filing"

**Performance:** ITC reconciliation runs as a Celery task (triggered on demand or daily at 10:00 IST after GSTR-2A auto-sync). Result cached in `gst:itc-recon:2026-04` TTL 1800s.

**Mobile:** "Our Books" and "GSTR-2A" columns collapse into a single "Difference" view. Mismatch rows shown with amber border.

**Accessibility:** Table caption "ITC Reconciliation April 2026". Mismatch rows have `role="row" aria-label="Mismatch"`.

---

### Section 6 — TDS Tracker (Section 194J)

**Purpose:** Some coaching centre clients (large B2B contracts) are required by law to deduct TDS at 10% on EduForge's service fees under Section 194J (Professional/Technical services). EduForge must track this deducted TDS — it's a tax credit that offsets EduForge's advance tax liability.

**User interaction:** Read-only table. Click row → mini-drawer with Form 16A details.

**UI elements:**
```
TDS DEDUCTED (SEC 194J) — FY 2025–26         Total: ₹1,24,000
──────────────────────────────────────────────────────────────────────────────
Deductor (Coaching Centre) │ Contract Value │ TDS @ 10% │ Deposited? │ Form 16A
───────────────────────────┼────────────────┼───────────┼────────────┼─────────
ABC Coaching Pvt Ltd       │ ₹4,00,000      │ ₹40,000   │ ✅ Q3       │ Received
XYZ Institute Ltd          │ ₹3,00,000      │ ₹30,000   │ ✅ Q3       │ Received
DEF Academy                │ ₹2,00,000      │ ₹20,000   │ ⚠ Pending  │ Not yet
GHI Tutorials              │ ₹3,40,000      │ ₹34,000   │ ✅ Q3       │ Received
```

- "Deposited?" column: ✅ Qn (deposited in quarter n) / ⚠ Pending (deducted but Form 26AS not updated yet) / 🔴 Not deducted
- "Form 16A" column: Received (linked to uploaded PDF) / Not yet / Disputed
- "Not deducted" row: red background — EduForge should follow up with deductor. Deductor's failure = EduForge cannot claim the credit.

**Data flow:** `TDSRecord` model — manually entered by Finance Manager from Form 16A / cross-checked against Form 26AS (income tax portal). No API sync (manual process).

**HTMX:** `id="tds-tracker"` `hx-get="/exec/gst-compliance/?part=tds&fy={{ fy }}"` `hx-trigger="load"` `hx-swap="innerHTML"`

**Mobile:** Contract Value and Form 16A columns hidden. Deductor + TDS amount + status only.

**Accessibility:** "Not deducted" rows `aria-label="TDS not deducted — action required"`.

---

## 5. Full Page Wireframe

```
╔══════════════════════════════════════════════════════════════════════════════╗
║  GST & Tax Compliance                  [FY 2025–26 ▾] [Apr 2026 ▾] [Export]║
║  🔴 GSTR-1 due in 2 days (11 Apr) — 48 invoices pending tagging [Review →] ║
║  🟡 GSTR-3B due in 11 days (20 Apr) — Liability ready [Review →]           ║
╠══════════╦══════════╦══════════╦══════════╦══════════╦══════════════════════╣
║ OUTPUT   ║ CGST/SGST║ IGST     ║ ITC AVAIL║ NET PAY  ║ TDS (194J)          ║
║ ₹22,46K  ║ ₹18,32K  ║ ₹4,14K   ║ ₹3,18K   ║ ₹19,28K  ║ ₹1,24K              ║
╠══════════╩══════════╩══════════╩══════════╩══════════╩══════════════════════╣
║  GSTR FILING CALENDAR — FY 2025–26           [Filter: All ▾]               ║
║  Filing Type │ Period   │ Deadline  │ Status        │ ARN / Reference       ║
║  GSTR-1      │ Apr 2026 │ 11 Apr    │ ⏳ Due 2 days  │ —           [⋯]      ║
║  GSTR-3B     │ Apr 2026 │ 20 Apr    │ ⏳ Due 11 days │ —           [⋯]      ║
║  GSTR-1      │ Mar 2026 │ 11 Mar    │ ✅ Filed       │ ARN-AA2603  [⋯]      ║
║  GSTR-3B     │ Feb 2026 │ 20 Feb    │ 🔴 Overdue    │ —           [⋯]      ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  STATE-WISE GST BREAKDOWN — Apr 2026       [Export for GSTR-1]             ║
║  State         │ Institutions │ Invoiced  │ Tax Type  │ GST Amount │ GSTIN✓ ║
║  Andhra Pradesh│ 312          │ ₹48,20K   │ IGST 18%  │ ₹8,67K     │ ✅     ║
║  Telangana     │ 280          │ ₹43,60K   │ CGST+SGST │ ₹7,84K     │ ✅     ║
║  Karnataka     │ 198          │ ₹31,24K   │ IGST 18%  │ ₹5,62K     │ ⚠ 2   ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  ITC RECONCILIATION — Apr 2026     ⚠ 3 mismatches found                   ║
║  Vendor       │ Our Books   │ GSTR-2A    │ Difference │ Status              ║
║  Amazon AWS   │ ₹1,24,200   │ ₹1,24,200  │ ₹0         │ ✅ Match            ║
║  Exotel       │ ₹8,200      │ ₹6,400     │ -₹1,800    │ ⚠ Mismatch         ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  TDS DEDUCTED (SEC 194J) — FY 2025–26         Total: ₹1,24,000            ║
║  Deductor             │ Contract Value │ TDS @10% │ Deposited? │ Form 16A  ║
║  ABC Coaching Pvt Ltd │ ₹4,00,000      │ ₹40,000  │ ✅ Q3       │ Received  ║
║  DEF Academy          │ ₹2,00,000      │ ₹20,000  │ ⚠ Pending  │ Not yet   ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 6. Drawers & Modals

### Drawer — Filing Detail (480px)

**Open trigger:** Click any row in GSTR Filing Calendar.

```
┌──────────────────────────────────────────────────────┐
│  GSTR-1 — April 2026                    ⏳ Due 2d [✕]│
│  ─────────────────────────────────────────────────── │
│  Filing period:   1 Apr – 30 Apr 2026                │
│  Deadline:        11 Apr 2026                         │
│  Status:          Pending                            │
│  ─────────────────────────────────────────────────── │
│  DATA SUMMARY                                        │
│  Total invoices:    312                              │
│  Total taxable:     ₹1,24,40,000                    │
│  Total GST:         ₹22,39,200                      │
│  IGST:              ₹18,25,200  (814 invoices)      │
│  CGST+SGST:         ₹4,14,000   (280 invoices)      │
│  ─────────────────────────────────────────────────── │
│  ISSUES                                              │
│  ⚠ 48 invoices missing GSTIN (will be B2C)          │
│  ⚠ 2 invoices with GSTIN validation failure         │
│  ─────────────────────────────────────────────────── │
│  ARN Number: [___________________________]           │
│  Filing Date: [11 Apr 2026  📅]                      │
│  Notes:       [_________________________]            │
│  ─────────────────────────────────────────────────── │
│  [Cancel]                       [Mark as Filed]      │
└──────────────────────────────────────────────────────┘
```

- "Mark as Filed" button: visible only to GST Consultant / CFO / CEO
- Issues section: amber box listing data quality problems that should be resolved before filing
- POST on "Mark as Filed": `/exec/gst-compliance/actions/mark-filed/`

### Modal — Flag ITC Mismatch (400px)

**Open trigger:** "Flag Mismatch" action in ITC Reconciliation table.

- Vendor (pre-filled, read-only)
- Mismatch amount (pre-filled, read-only)
- Action taken (select: "Contacted vendor" / "Awaiting correction" / "Reversing in 3B" / "Other")
- Notes (textarea, required)
- Expected resolution date (date picker)

POST `/exec/gst-compliance/actions/flag-itc-mismatch/` → creates `ITCMismatchRecord`, sends email to Finance Manager if escalation checkbox ticked.

---

## 7. Component Architecture

| Component | File | Props |
|---|---|---|
| `GSTLiabilityCard` | `components/gst/liability_card.html` | `label, value, subline, alert_level, can_view_amounts` |
| `FilingCalendarRow` | `components/gst/filing_row.html` | `filing, can_mark_filed, days_until` |
| `FilingStatusBadge` | `components/gst/filing_badge.html` | `status, days_until` |
| `StateBreakdownRow` | `components/gst/state_row.html` | `state, count, invoiced, tax_type, gst_amount, gstin_valid, gstin_total, can_view_amounts` |
| `ITCReconRow` | `components/gst/itc_row.html` | `vendor, book_amount, gstr2a_amount, difference, status` |
| `TDSTrackerRow` | `components/gst/tds_row.html` | `deductor, contract_value, tds_amount, deposited_quarter, form16a_status` |
| `FilingDrawer` | `components/gst/filing_drawer.html` | `filing_id, can_mark_filed` |
| `ITCMismatchModal` | `components/gst/itc_mismatch_modal.html` | `vendor_name, mismatch_amount` |
| `DeadlineAlertBar` | `components/gst/alert_bar.html` | `alerts (list of {type, deadline, days_until, message, review_anchor})` |

---

## 8. HTMX Architecture

**Page URL:** `/exec/gst-compliance/`
**All partials:** `/exec/gst-compliance/?part={name}`

| `?part=` | Target | Trigger | Poll | Swap |
|---|---|---|---|---|
| `liability` | `#gst-liability-strip` | load | Every 120s (pause on drawer/modal) | innerHTML |
| `calendar` | `#filing-calendar` | load | None | innerHTML |
| `state-breakdown` | `#state-breakdown` | load + month change | None | innerHTML |
| `itc` | `#itc-recon` | load + month change | None | innerHTML |
| `tds` | `#tds-tracker` | load + FY change | None | innerHTML |
| `filing-drawer` | `#drawer-container` | Calendar row click | None | innerHTML |

---

## 9. Backend View & API

```python
class GSTComplianceView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "portal.view_gst_compliance"

    FINANCE_ROLES = frozenset(["cfo", "finance_manager", "gst_consultant", "ceo", "superadmin"])

    def get(self, request):
        # Deny engineering roles
        if request.user.role in {"cto", "backend_engineer", "frontend_engineer",
                                  "devops", "security_engineer", "billing_admin"}:
            messages.warning(request, "GST data is restricted to Finance roles.")
            return redirect("exec:dashboard")

        fy    = request.GET.get("fy", current_fy())        # e.g. "2025-26"
        month = request.GET.get("month", current_month())  # e.g. "2026-04"
        can_view_amounts = request.user.role in self.FINANCE_ROLES

        if _is_htmx(request):
            part = request.GET.get("part", "")
            ctx  = self._build_context(request, fy, month, can_view_amounts)
            dispatch = {
                "liability":       "exec/gst/partials/liability.html",
                "calendar":        "exec/gst/partials/calendar.html",
                "state-breakdown": "exec/gst/partials/state_breakdown.html",
                "itc":             "exec/gst/partials/itc_recon.html",
                "tds":             "exec/gst/partials/tds_tracker.html",
                "filing-drawer":   "exec/gst/partials/filing_drawer.html",
            }
            if part in dispatch:
                return render(request, dispatch[part], ctx)
            return HttpResponseBadRequest("Unknown part")

        ctx = self._build_context(request, fy, month, can_view_amounts)
        return render(request, "exec/gst_compliance.html", ctx)

    def _build_context(self, request, fy, month, can_view_amounts):
        return {
            "fy": fy,
            "month": month,
            "can_view_amounts": can_view_amounts,
            "can_mark_filed": request.user.role in {"cfo", "finance_manager",
                                                     "gst_consultant", "ceo", "superadmin"},
            "deadline_alerts": self._get_deadline_alerts(month),
        }

    def _get_deadline_alerts(self, month):
        filings = GSTFilingCalendar.objects.filter(
            period_month=month, status__in=["pending", "overdue"]
        )
        alerts = []
        for f in filings:
            days = (f.deadline_adjusted - today()).days
            if days <= 5:
                alerts.append({
                    "type": f.filing_type,
                    "deadline": f.deadline_adjusted,
                    "days_until": days,
                    "review_anchor": f"#filing-{f.id}",
                })
        return alerts
```

**Action endpoints:**

| Method | URL | Permission | Action |
|---|---|---|---|
| POST | `/exec/gst-compliance/actions/mark-filed/` | `portal.manage_gst_filings` | Create `GSTFiling` record, update calendar status, audit log |
| POST | `/exec/gst-compliance/actions/flag-itc-mismatch/` | `portal.view_gst_compliance` | Create `ITCMismatchRecord`, optional email alert |
| GET | `/exec/gst-compliance/?part=export&type=gstr1` | `portal.export_gst_data` | CSV formatted for Tally/GST portal import |
| GET | `/exec/gst-compliance/?part=export&type=state-summary` | `portal.export_gst_data` | State-wise summary CSV |

---

## 10. Database Schema

```python
class GSTFilingCalendar(models.Model):
    """Pre-seeded at year start — one row per filing type per month."""
    FILING_TYPES = [("GSTR-1","GSTR-1"), ("GSTR-3B","GSTR-3B"),
                    ("GSTR-9","GSTR-9 Annual"), ("26Q","TDS Return 26Q")]

    filing_type       = models.CharField(max_length=10, choices=FILING_TYPES)
    period_month      = models.CharField(max_length=7)   # "2026-04"
    fy                = models.CharField(max_length=7)   # "2025-26"
    deadline          = models.DateField()
    deadline_adjusted = models.DateField()  # adjusted for holidays/weekends
    status = models.CharField(
        max_length=20,
        choices=[("pending","Pending"),("filed","Filed"),
                 ("overdue","Overdue"),("nil","Nil Return"),("na","Not Applicable")],
        default="pending"
    )
    arn_number        = models.CharField(max_length=20, blank=True)
    filing_date       = models.DateField(null=True)
    filed_by          = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,
                                          on_delete=models.SET_NULL)
    notes             = models.TextField(blank=True)

    class Meta:
        unique_together = ("filing_type", "period_month")
        indexes = [models.Index(fields=["fy", "status"])]


class GSTLiabilitySnapshot(models.Model):
    """Monthly snapshot of computed GST liability — written by Celery task."""
    period_month      = models.CharField(max_length=7, unique=True)
    output_tax        = models.DecimalField(max_digits=14, decimal_places=2)
    cgst_sgst         = models.DecimalField(max_digits=14, decimal_places=2)
    igst              = models.DecimalField(max_digits=14, decimal_places=2)
    itc_available     = models.DecimalField(max_digits=12, decimal_places=2)
    net_payable       = models.DecimalField(max_digits=14, decimal_places=2)
    tds_receivable    = models.DecimalField(max_digits=12, decimal_places=2)
    computed_at       = models.DateTimeField(auto_now=True)


class GSTR2ARecord(models.Model):
    """Supplier-reported ITC data synced from GST portal."""
    vendor_gstin      = models.CharField(max_length=15, db_index=True)
    vendor_name       = models.CharField(max_length=200)
    invoice_number    = models.CharField(max_length=50)
    invoice_date      = models.DateField()
    taxable_value     = models.DecimalField(max_digits=12, decimal_places=2)
    igst              = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cgst              = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    sgst              = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    period_month      = models.CharField(max_length=7, db_index=True)
    filing_status     = models.CharField(max_length=20)  # "filed", "pending"

    class Meta:
        unique_together = ("vendor_gstin", "invoice_number", "period_month")


class ITCMismatchRecord(models.Model):
    period_month      = models.CharField(max_length=7)
    vendor_gstin      = models.CharField(max_length=15)
    vendor_name       = models.CharField(max_length=200)
    book_amount       = models.DecimalField(max_digits=12, decimal_places=2)
    gstr2a_amount     = models.DecimalField(max_digits=12, decimal_places=2)
    difference        = models.DecimalField(max_digits=12, decimal_places=2)
    action_taken      = models.CharField(max_length=50)
    notes             = models.TextField()
    expected_resolution = models.DateField(null=True)
    raised_by         = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    created_at        = models.DateTimeField(auto_now_add=True)
    resolved_at       = models.DateTimeField(null=True)


class TDSRecord(models.Model):
    fy                = models.CharField(max_length=7)
    deductor_name     = models.CharField(max_length=200)
    deductor_tan      = models.CharField(max_length=10)  # TAN of coaching centre
    contract_value    = models.DecimalField(max_digits=14, decimal_places=2)
    tds_amount        = models.DecimalField(max_digits=12, decimal_places=2)
    quarter           = models.CharField(max_length=2,
                            choices=[("Q1","Q1"),("Q2","Q2"),("Q3","Q3"),("Q4","Q4")])
    deposited_status  = models.CharField(max_length=20,
                            choices=[("deposited","Deposited"),("pending","Pending"),
                                     ("not_deducted","Not Deducted")])
    form16a_status    = models.CharField(max_length=20,
                            choices=[("received","Received"),("pending","Pending"),
                                     ("disputed","Disputed")])
    form16a_document  = models.FileField(upload_to="tds/form16a/", null=True)
```

---

## 11. Validation Rules

| Action | Validation |
|---|---|
| Mark as Filed | ARN format: 15-char. Filing date: required, cannot be > today. Filing type + period must match the calendar row. One ARN per filing (duplicate ARN blocked with error "This ARN is already recorded"). |
| Flag ITC Mismatch | Notes required, min 20 chars. Action taken must be selected. Expected resolution must be in the future. |
| Export GSTR-1 data | Month required. Actor must have `portal.export_gst_data`. Rate-limited: 10 exports/hour per user. |

---

## 12. Security Considerations

| Concern | Implementation |
|---|---|
| Tax data access restriction | `can_view_amounts` set server-side. Template never renders rupee amounts for non-finance roles — values absent from DOM entirely. |
| ARN number privacy | ARN numbers (government filing references) are stored and displayed only to finance roles. COO sees filing status only (Filed/Pending), not the ARN. |
| GST portal API credentials | Stored in AWS Secrets Manager. Never in settings.py or any file. Celery tasks fetch from Secrets Manager at runtime. |
| GSTR-2A sync audit | Every GSTR-2A sync run creates a `GSTSyncLog` entry (timestamp, records fetched, errors). Immutable audit trail. |
| Mark-as-filed audit | Every filing status change creates `AuditLog` entry with actor, timestamp, ARN, old/new status. Immutable. |
| ITC mismatch records | Once created, `ITCMismatchRecord` cannot be deleted — only resolved. Ensures audit trail for tax department queries. |
| CSRF protection | All POST actions use `hx-headers` CSRF token. |
| Rate limiting | Export: 10/hour. Mark-as-filed: 20/hour per user (prevents accidental bulk updates). |

---

## 13. Edge Cases (System-Level)

| State | Behaviour |
|---|---|
| GST portal API down (GSTR-2A sync fails) | Celery task logs `GSTSyncError`. ITC section shows "GSTR-2A data unavailable — last synced X days ago. Reconciliation may be incomplete." No page crash. |
| GSTIN validation failure for institution | Invoice is treated as B2C (no GSTIN → no ITC for institution). Counter in state table increments. CFO alerted via `ComplianceAlert`. |
| Overdue filing detected on load | `ComplianceAlert` created (idempotent — no duplicates if already exists). CFO and GST Consultant receive email. Incident not created (compliance alert ≠ platform incident). |
| ITC mismatch > Rs.50,000 | Above `ITCMismatchRecord` creation: also creates `ComplianceAlert` of high severity. Finance Manager email sent immediately. |
| Duplicate ARN entry attempt | Backend validates uniqueness before saving. Returns `{"error": "ARN AA2604... is already recorded for GSTR-1 Apr 2026"}`. Toast shows error. |
| Filing marked for wrong month | Not possible — ARN field only active in the drawer of the specific filing row. Period is pre-filled read-only. |
| Financial year boundary (March → April) | FY selector allows "2024-25" and "2025-26". All queries respect `fy` param. GSTR-9 (annual) appears only in FY calendar, not monthly. |

---

## 14. Performance & Scaling

| Endpoint | Target | Critical Threshold |
|---|---|---|
| Page shell initial load | < 600ms | > 1.5s |
| `?part=liability` | < 200ms (Redis cache) | > 500ms |
| `?part=calendar` | < 150ms | > 400ms |
| `?part=state-breakdown` | < 300ms | > 800ms |
| `?part=itc` | < 400ms | > 1s |
| `?part=tds` | < 200ms | > 500ms |
| Filing drawer load | < 300ms | > 800ms |
| GSTR-1 CSV export | < 3s | > 10s |

**Scaling notes:**
- State breakdown aggregation: bounded at ~36 Indian states × 2,050 institutions = trivial GROUP BY
- ITC reconciliation is the most expensive query (join across `PurchaseExpense` + `GSTR2ARecord`). Cached 30 min. Celery task pre-warms cache daily at 10:00 IST.
- GSTR-2A sync via GST portal API: rate-limited by GST portal (100 req/min). Celery task uses exponential backoff on 429s. Sync runs at 06:00 IST (low-traffic, before Finance team starts work).
- Filing calendar: max 24 rows/year. Zero caching needed — trivial query.

---

*Last updated: 2026-03-20*
