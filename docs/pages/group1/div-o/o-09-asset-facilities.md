# O-09 — Asset Registry & Facilities Management

**Route:** `GET /hr/assets/`
**Method:** Django `TemplateView` + HTMX part-loads
**Primary role:** Office Administrator (#81)
**Also sees:** HR Manager (#79) — full access; DevOps/SRE Engineer (#14) — IT asset requests only via cross-link from O-04 task notifications (no direct portal access)

---

## Purpose

Office Administrator's primary working page. At 100–150 employees, managing IT and office assets manually (spreadsheets) fails — laptops go missing at exits, new joiners wait for equipment, and vendor AMC contracts lapse silently. This page provides the Office Admin with: a live asset register with full lifecycle tracking, vendor management with contract and invoice oversight, petty cash logging, and travel request coordination. Without this page the Office Admin has no primary tool — they currently only appear in O-01 (asset strip), O-02 (employee asset tab), and O-04 (onboarding tasks).

---

## Data Sources

| Section | Source | Cache TTL |
|---|---|---|
| Asset KPI strip | `hr_asset` aggregated by status | 5 min |
| Asset table | `hr_asset` JOIN `hr_employee` (assigned_to) | 5 min |
| Asset detail | `hr_asset` single row + `hr_asset_maintenance_log` | No cache |
| Vendor list | `hr_vendor` WHERE status='ACTIVE' | 10 min |
| Vendor invoice list | `hr_vendor_invoice` JOIN `hr_vendor` | 5 min |
| Petty cash log | `hr_petty_cash` ORDER BY transaction_date DESC | No cache |
| Travel requests | `hr_travel_request` JOIN `hr_employee` | 5 min |
| Upcoming expirations | `hr_vendor` WHERE contract_expiry <= today+30d + `hr_asset` WHERE warranty_expiry <= today+30d | 10 min |

---

## URL Parameters

| Param | Values | Default | Effect |
|---|---|---|---|
| `?tab` | `assets`, `vendors`, `petty_cash`, `travel`, `dashboard` | `dashboard` | Active section |
| `?asset_type` | `laptop`, `monitor`, `access_card`, `headset`, `projector`, `furniture`, `all` | `all` | Filter assets |
| `?asset_status` | `available`, `assigned`, `in_repair`, `retired`, `all` | `all` | Filter by lifecycle status |
| `?assigned_to` | UUID | — | Show all assets assigned to specific employee |
| `?q` | string | — | Search: serial number, asset type, employee name |
| `?invoice_status` | `pending`, `approved`, `paid`, `overdue`, `all` | `all` | Filter vendor invoices |
| `?travel_status` | `draft`, `approved`, `booked`, `completed`, `cancelled`, `all` | `pending` | Filter travel requests |
| `?sort` | `assigned_date_desc`, `type`, `serial`, `employee_name` | `assigned_date_desc` | Asset table sort |
| `?page` | integer | `1` | Pagination (25 per page) |
| `?export` | `assets_csv`, `invoice_register_csv` | — | Export (Office Admin + HR Manager) |

---

## HTMX Part-Load Routes

| Part | Route | Trigger | Target ID |
|---|---|---|---|
| Dashboard strip | `?part=dashboard` | Page load | `#o9-dashboard` |
| Asset table | `?part=asset_table` | Tab click + filter | `#o9-asset-table` |
| Asset detail drawer | `?part=asset_drawer&id={id}` | Row click | `#o9-asset-drawer` |
| Vendor list | `?part=vendors` | Tab click | `#o9-vendors` |
| Invoice list | `?part=invoices` | Tab click + filter | `#o9-invoices` |
| Petty cash log | `?part=petty_cash` | Tab click | `#o9-petty-cash` |
| Travel requests | `?part=travel` | Tab click + filter | `#o9-travel` |
| Add asset modal | `?part=add_asset_modal` | [+ Add Asset] click | `#modal-container` |
| Add vendor modal | `?part=add_vendor_modal` | [+ Add Vendor] click | `#modal-container` |
| Add invoice modal | `?part=add_invoice_modal&vendor_id={id}` | [+ Log Invoice] click | `#modal-container` |
| Add petty cash modal | `?part=add_petty_cash_modal` | [+ Log Transaction] click | `#modal-container` |
| Travel approval modal | `?part=travel_approval_modal&id={id}` | [Approve]/[Reject] | `#modal-container` |

---

## Page Layout

```
┌──────────────────────────────────────────────────────────────────────┐
│  Asset & Facilities                              [+ Add Asset]       │
├──────────────────────────────────────────────────────────────────────┤
│  DASHBOARD STRIP (KPI tiles + expiry alerts)                         │
├──────────────────────────────────────────────────────────────────────┤
│  [Dashboard] [Assets] [Vendors & Invoices] [Petty Cash] [Travel]    │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Dashboard Tab (default)

```
┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ 112          │ │ 8            │ │ 3            │ │ ₹12,400      │ │ 2            │
│ Assigned     │ │ Available    │ │ In Repair    │ │ Petty Cash   │ │ Pending      │
│ Assets       │ │ (laptops: 4) │ │              │ │ Balance      │ │ Travel Reqs  │
│              │ │              │ │              │ │ (this month) │ │              │
└──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘
```

### Expiry Alerts Panel

```
  Upcoming Expirations (next 30 days)
  ─────────────────────────────
  ⚠ Vendor contract    HouseClean Co.         Expires: 28 Mar 2026 (in 7d)    [Renew]
  ⚠ Asset warranty     Dell Latitude SN-78923  Expires: 2 Apr 2026 (in 12d)   —
    Vendor contract    Pantry Vendors Ltd.     Expires: 15 Apr 2026 (in 25d)  [Renew]
  [View all →]
```

Red row: ≤ 7 days. Amber row: ≤ 14 days.

### Pending Actions Panel

```
  4 travel requests pending approval
  2 vendor invoices overdue for payment
  3 assets unassigned to upcoming joiners (join date < 7 days away)
  [View →] links for each
```

---

## Assets Tab

### Asset Table

| Column | Description |
|---|---|
| Asset Type | Type badge (LAPTOP/MONITOR/ACCESS_CARD/etc.) |
| Serial # | Serial number (monospace) |
| Assigned To | Employee name (link → O-02 profile) or "Available" |
| Assigned Date | Date of last assignment |
| Condition | NEW / GOOD / FAIR / POOR |
| Status | AVAILABLE (green) / ASSIGNED (blue) / IN_REPAIR (amber) / RETIRED (grey) |
| Warranty | Expiry date or "Expired" (red) |
| Actions | [View] [Reassign] [Send for Repair] [Retire] |

Sortable by all columns. Multi-select for bulk export.

### Asset Lifecycle Transitions

```
  NEW → AVAILABLE (on procurement receipt)
  AVAILABLE → ASSIGNED (when assigned to employee in O-04 onboarding or manually here)
  ASSIGNED → AVAILABLE (on employee exit — mark returned in O-04 or directly here)
  ASSIGNED/AVAILABLE → IN_REPAIR (send for repair)
  IN_REPAIR → AVAILABLE (return from repair)
  AVAILABLE/IN_REPAIR → RETIRED (decommission)
```

**[Send for Repair]:** Opens maintenance log modal:
```
  Asset: Dell Latitude SN-78923
  Issue description* [Keyboard keys not working              ]
  Sent to vendor:    [Vendor: TechService AMC ▼]
  Sent date:         [21 Mar 2026]
  [Log & Send for Repair]
```
On submit: status → IN_REPAIR. If currently ASSIGNED, employee notified: "Your laptop [SN] has been sent for repair. A replacement will be assigned shortly."

**[Mark Returned from Repair]:** Prompts for: return date, repair cost, repaired by vendor. Status → AVAILABLE.

### Asset Detail Drawer

```
┌──────────────────────────────────────────────────────────────────┐
│  LAPTOP — Dell Latitude 5540                          [Edit] [×]  │
│  Serial: DL5540-78923   Condition: GOOD   Status: ASSIGNED        │
├──────────────────────────────────────────────────────────────────┤
│  Assigned to:    Rohan Verma (EF-0047, Backend Engineer)         │
│  Assigned since: 14 Jun 2024 (9 months)                          │
│  Purchase date:  10 Jun 2024   Cost: ₹82,000                     │
│  Vendor:         Dell India                                      │
│  Warranty:       Until 9 Jun 2027                                │
├──────────────────────────────────────────────────────────────────┤
│  Maintenance History:                                            │
│  No maintenance records.                                         │
├──────────────────────────────────────────────────────────────────┤
│  [Reassign to another employee]  [Send for Repair]  [Retire]    │
└──────────────────────────────────────────────────────────────────┘
```

### Add Asset Modal

```
┌──────────────────────────────────────────────────────────────────┐
│  Add Asset                                                       │
├──────────────────────────────────────────────────────────────────┤
│  Asset Type*        [LAPTOP                           ▼]         │
│  Serial Number*     [DL5540-NEW001                    ]          │
│  Make / Model*      [Dell Latitude 5540               ]          │
│  Condition*         [NEW                              ▼]         │
│  Purchase Date*     [2026-03-21                        ]         │
│  Purchase Cost (₹)* [82000                             ]         │
│  Vendor Name        [Dell India                        ]         │
│  Warranty Expiry    [2029-03-21                        ]         │
│  Assign to employee [Search employee...               ▼]         │
│  (leave blank if going to available pool)                        │
│                                                                  │
│  [Cancel]                                      [Add Asset]       │
└──────────────────────────────────────────────────────────────────┘
```

---

## Vendors & Invoices Tab

Two-panel layout: vendors list (left), invoices for selected vendor (right).

### Vendors List

```
  Vendors (11 active)
  ─────────────────────────────────────────────────────────────────
  HouseClean Co.        HOUSEKEEPING    Contract expires: 28 Mar ⚠  [View]
  Pantry Vendors Ltd.   PANTRY          Contract expires: 15 Apr     [View]
  TechService AMC       AMC             Contract expires: Jun 2026   [View]
  Rapidex Courier       COURIER         No contract — on-demand      [View]
  [+ Add Vendor]
```

### Vendor Detail Panel (right)

```
  Pantry Vendors Ltd.
  Category: PANTRY · Contact: Suresh Sharma · +91-98765-12345
  GSTIN: 36ABCDE1234F1ZH · Payment Terms: Net 15 days
  Contract: 15 Apr 2024 – 14 Apr 2026 (expires in 24 days)  [Renew]
  ─────────────────────────────────────────────────────────────────
  Recent Invoices
  Mar 2026   ₹24,500   PAID      Paid: 10 Mar   [View PDF]
  Feb 2026   ₹23,800   PAID      Paid: 9 Feb    [View PDF]
  Jan 2026   ₹25,200   PAID      Paid: 8 Jan    [View PDF]
  [+ Log New Invoice]
```

### Add Invoice Modal

```
┌──────────────────────────────────────────────────────────────────┐
│  Log Invoice — Pantry Vendors Ltd.                               │
├──────────────────────────────────────────────────────────────────┤
│  Invoice Number*   [PVL-2026-0098                    ]           │
│  Invoice Date*     [2026-03-31                        ]           │
│  Amount (₹)*       [24500                             ]           │
│  GST Amount (₹)    [4410    ] (18% GST auto-computed) │
│  Due Date*         [2026-04-15                        ]           │
│  Upload Invoice*   [Choose PDF...                     ]           │
│                                                                  │
│  [Cancel]                            [Log Invoice]               │
└──────────────────────────────────────────────────────────────────┘
```

**HR Manager approval gate:** Invoices > ₹25,000 require HR Manager approval before marking as approved for payment. Office Admin logs the invoice; HR Manager sees it in O-01 pending approvals strip.

**Payment flow:** After HR Manager approval, Office Admin marks invoice as PAID with payment reference. Finance Manager (#69) receives a monthly vendor payment summary via O-09 cross-portal API for P&L entry.

---

## Petty Cash Tab

Running ledger of petty cash transactions. Office Admin maintains a float of ₹10,000–₹20,000 (configured by HR Manager).

```
  Petty Cash Ledger — March 2026
  Opening Balance: ₹18,000 (replenished 1 Mar 2026)
  ─────────────────────────────────────────────────────────────────────
  Date       Description                Category        Amount    Balance
  21 Mar     Printer cartridges × 2     OFFICE_SUPPLIES  -₹1,200   ₹16,800
  18 Mar     Team lunch (exam day)      MISC             -₹3,400   ₹18,000
  15 Mar     Courier to client          COURIER            -₹280   ₹21,400
  10 Mar     Replenishment              —                +₹4,800   ₹21,680
  ─────────────────────────────────────────────────────────────────────
  Closing Balance (to date):  ₹16,800
  MTD Spend:                  ₹4,880
  [+ Log Transaction]   [Replenish Cash]   [Export Ledger]
```

### Log Transaction Modal

```
  Date*           [2026-03-21]
  Description*    [Printer cartridges × 2]
  Category*       [OFFICE_SUPPLIES ▼]
  Amount (₹)*     [1200    ]  (expense)
  Receipt Upload* [Choose image/PDF...]
  [Save Transaction]
```

**Receipt mandatory** for transactions > ₹500. Transactions > ₹2,000 require HR Manager approval. Monthly petty cash report auto-generated on 1st of next month and forwarded to Finance Manager (#69) for reconciliation.

**Replenishment:** [Replenish Cash] → logs a positive transaction, notifies Finance Manager to disburse the replenishment amount.

---

## Travel Tab

Employee travel requests managed by Office Admin. HR Manager approves; Office Admin books.

### Travel Request Table

| Column | Description |
|---|---|
| Employee | Name + division |
| From → To | Travel route |
| Departure | Date |
| Return | Date |
| Mode | AIR / TRAIN / ROAD badge |
| Purpose | (truncated) |
| Estimated Cost | ₹ |
| Status | DRAFT / APPROVED / BOOKED / COMPLETED / CANCELLED |
| Actions | [View] [Approve] (HR Mgr) / [Book] (Office Admin) |

### Travel Request Detail Drawer

```
  Travel Request — Rohan Verma (EF-0047)
  ─────────────────────────────────────────────────────────────────
  From: Hyderabad → To: Delhi (AWS re:Invent India conference)
  Departure: 5 Apr 2026 · Return: 8 Apr 2026 (4 days)
  Mode: AIR · Hotel required: Yes
  Purpose: "AWS re:Invent India — relevant to team's cloud upskilling plan"
  Estimated cost: ₹22,000 (flight ~₹14K + hotel ~₹8K)
  Advance requested: ₹20,000
  ─────────────────────────────────────────────────────────────────
  Status: APPROVED (by HR Manager on 20 Mar 2026)
  [Mark Booked]  [Add Booking Reference]  [Mark Completed]
```

**[Mark Booked]:** Office Admin enters booking reference numbers (flight PNR, hotel confirmation). Status → BOOKED.

**[Mark Completed]:** On employee return. Prompts for actual total cost (for expense reconciliation). If actual cost > estimated by > 20%, HR Manager notified.

**Travel Policy:**
- Air travel: Economy class only. Business class requires HR Manager + CEO approval.
- Hotel: up to ₹3,500/night (Tier 1 cities: Delhi, Mumbai, Bengaluru); ₹2,500/night (other cities)
- Daily allowance: ₹500/day (within India)
- Advance disbursed by Finance Manager (#69) within 2 working days of approval

---

## Empty States

| Condition | Message |
|---|---|
| No assets in registry | "No assets added yet. [+ Add Asset]" |
| No assets available for assignment | "No assets currently available. [+ Add Asset] or [Return from Repair]" |
| No active vendors | "No vendors configured. [+ Add Vendor]" |
| No overdue invoices | "No overdue invoices." with green checkmark |
| Petty cash balance below ₹2,000 | "⚠ Petty cash balance low (₹[balance]). [Replenish Cash]" — shown as amber banner |
| No pending travel requests | "No travel requests pending approval." |

---

## Toast Messages

| Action | Toast | Type |
|---|---|---|
| Asset added | "[Type] [Serial] added to asset register." | Green |
| Asset assigned | "[Type] assigned to [employee name]." | Green |
| Asset marked returned | "[Type] [Serial] returned by [employee]. Status: AVAILABLE." | Green |
| Asset sent for repair | "[Type] [Serial] sent for repair to [vendor]." | Amber |
| Invoice logged | "Invoice [number] logged for [vendor] — ₹[amount]. Pending approval." | Blue |
| Invoice approved | "Invoice [number] approved. Office Admin notified for payment." | Green |
| Petty cash transaction logged | "₹[amount] logged under [category]. Balance: ₹[balance]." | Green |
| Travel request approved | "[Employee]'s travel to [city] approved. Ready for booking." | Green |
| Travel request rejected | "[Employee]'s travel request rejected." | Amber |
| Contract expiry alert | "⚠ [Vendor] contract expires in [N] days. [Renew]" | Amber |

---

## Role-Based UI Visibility Summary

| Element | 79 HR Manager | 81 Office Admin |
|---|---|---|
| Dashboard strip (all tiles) | Yes | Yes |
| Expiry alerts panel | Yes | Yes |
| Pending actions panel | Yes | Yes |
| Asset table (all assets) | Yes | Yes |
| [+ Add Asset] | Yes | Yes |
| [Send for Repair] | Yes | Yes |
| [Retire Asset] | Yes | Yes |
| Vendor list (full) | Yes | Yes |
| [+ Add Vendor] | Yes | Yes |
| Invoice list (all) | Yes | Yes |
| [Approve Invoice > ₹25K] | Yes | No (disabled — tooltip) |
| [+ Log Invoice] | Yes | Yes |
| Petty cash ledger | Yes | Yes |
| [Log Transaction] | Yes | Yes |
| [Approve transaction > ₹2K] | Yes | No (auto-sends to HR Mgr) |
| Travel request table (all) | Yes | Yes |
| [Approve / Reject Travel] | Yes | No |
| [Mark Booked] | Yes | Yes |
| Export CSV | Yes | Yes |

---

## Performance Requirements

| Metric | Target | Notes |
|---|---|---|
| Asset table load (100+ assets) | < 1s P95 (cache: 5 min) | Server-side paginated |
| Dashboard strip | < 600ms P95 | Simple aggregates |
| Vendor invoice list | < 800ms P95 | Live data (no cache) |
| Petty cash export | < 2s | Generates ledger PDF |

---

## Authorization

**Route guard:** `@division_o_required(allowed_roles=[79, 81])` applied to `AssetFacilitiesView`.

| Scenario | Behaviour |
|---|---|
| [Approve Invoice > ₹25K] by Office Admin | 403 inline; button shown disabled with tooltip "Requires HR Manager approval" |
| [Approve Travel] by Office Admin | 403; button not rendered |
| Finance Manager (#69) cross-link | Monthly summary API endpoint: vendor payments total, petty cash spend — no individual transaction data |
| Unauthenticated | Redirect to `/login/?next=/hr/assets/` |

---

## Keyboard Shortcuts

| Key | Action |
|---|---|
| `g` `a` | Go to Asset & Facilities (O-09) |
| `t` `a` | Switch to Assets tab |
| `t` `v` | Switch to Vendors & Invoices tab |
| `t` `p` | Switch to Petty Cash tab |
| `t` `t` | Switch to Travel tab |
| `n` | [+ Add Asset] (when on Assets tab) |
| `Esc` | Close open drawer or modal |
| `?` | Show keyboard shortcut help overlay |
