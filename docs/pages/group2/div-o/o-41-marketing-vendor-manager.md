# O-41 — Marketing Vendor & Agency Manager

> **URL:** `/group/marketing/admin/vendors/`
> **File:** `o-41-marketing-vendor-manager.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Role:** Group Admissions Campaign Manager (Role 119, G3) — primary operator; G4/G5 — contract approval authority

---

## 1. Purpose

The Marketing Vendor & Agency Manager is the centralised registry and performance tracking system for every external vendor and agency that a group engages for marketing and admissions campaigns. A typical large Indian education group (20–50 branches) works with 8–15 vendors simultaneously: a newspaper ad agency that books insertions across Eenadu, Sakshi, Deccan Chronicle, and Times of India; an outdoor/BTL agency handling 200–500 hoardings, bus shelters, and auto-rickshaw wraps across multiple cities; a digital marketing agency running Google Ads and Meta campaigns; a printing vendor producing 50,000 brochures, 500 flex banners, and 10,000 pamphlets per season; an event management company organising open days and felicitation ceremonies; a WhatsApp/SMS API provider (MSG91, Gupshup, Kaleyra) sending 5–20 lakh messages per season; a PR agency placing press releases in regional media; a creative/design agency producing artwork; and a photography/videography vendor covering events and producing testimonial videos.

The problems this page solves:

1. **No central vendor database:** Branch-level staff engage local vendors independently — the group has no visibility into who is being paid, for what, at what rates. The Campaign Manager discovers duplicate vendors (two branches hiring different printing vendors at 40% different rates) only when invoices arrive.

2. **Contract amnesia:** A newspaper agency contract signed 18 months ago auto-renewed at 15% higher rates because nobody tracked the renewal date. An outdoor agency contract includes a penalty clause for early termination that nobody read. The vendor manager tracks every contract term, renewal date, and auto-sends alerts 30/60/90 days before expiry.

3. **Deliverable slippage:** The printing vendor promised 50,000 brochures by January 15 for Phase 3 newspaper insertions. They delivered 30,000 by January 25. Without deliverable tracking, the Campaign Manager only discovered the shortfall when branches ran out of brochures during the peak walk-in week.

4. **Payment chaos and GST non-compliance:** Marketing services attract 18% GST (SAC 998361 — advertising services, SAC 998397 — event management). Many small vendors provide invoices without GSTIN or with incorrect HSN/SAC codes. TDS at 2% (Section 194C for contracts) or 10% (Section 194J for professional/technical services) must be deducted. Without structured tracking, the accounts team misses TDS deductions, the group faces 18% GST input credit disallowance, and vendor reconciliation at year-end becomes a nightmare.

5. **No performance accountability:** The digital agency claims "10,000 leads generated" but only 800 converted to walk-ins. The outdoor agency says "500 hoardings installed" but 120 were in low-traffic locations. Without structured performance ratings linked to actual campaign outcomes, groups keep renewing poor-performing vendors out of inertia.

**Scale:** 8–15 active vendors · 20–40 contracts/season · ₹50L–₹5Cr total vendor payments · 100–300 deliverables tracked · 200–500 invoices/season

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Admissions Campaign Manager | 119 | G3 | Full CRUD — add vendors, create contracts, track deliverables, record payments, rate vendors | Primary operator |
| Group Admission Data Analyst | 132 | G1 | Read + Export — vendor performance reports, spend analytics | No create/edit |
| Group Campaign Content Coordinator | 131 | G2 | Read — view vendor list and deliverable status for content-related vendors (printing, creative) | Cannot modify |
| Group CEO | — | G4 | Read + Approve contracts > ₹5L | Strategic oversight + high-value approval |
| Group Chairman | — | G5 | Read + Approve + Override | Final authority on vendor decisions |
| Group CFO / Finance Director | 30 | G1 | Read — payment tracking, GST compliance | Cross-division finance visibility |

> **Access enforcement:** `@require_role(min_level=G1, division='O')`. Vendor bank details and PAN visible only to role 119 and G4+. Payment recording: role 119 only. Contract approval thresholds enforced server-side.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  >  Marketing & Campaigns  >  Administration  >  Marketing Vendor & Agency Manager
```

### 3.2 Page Header
```
Marketing Vendor & Agency Manager                    [+ Add Vendor]  [+ New Contract]  [Export]
Campaign Manager — Ramesh Venkataraman
Season 2026-27 · Active Vendors: 12 · Active Contracts: 18 · Pending Payments: ₹14,80,000 · Overdue Deliverables: 3
```

### 3.3 Alert Banner (conditional)

| Condition | Banner Text | Severity |
|---|---|---|
| Contract expiring within 30 days | "[N] vendor contract(s) expiring within 30 days — review for renewal or termination" | High (amber) |
| Contract expired and not renewed | "[Vendor] contract expired on [Date] — services may be disrupted" | Critical (red) |
| Overdue deliverables > 0 | "[N] deliverables overdue — [Vendor]: [Deliverable] was due on [Date]" | High (amber) |
| Pending payments > ₹10L | "₹[X] in vendor payments pending — oldest invoice is [N] days old" | Medium (yellow) |
| Vendor GSTIN invalid/expired | "[Vendor] GSTIN validation failed — block payments until resolved" | Critical (red) |
| TDS not deducted on recent payment | "TDS not deducted on [Vendor] payment of ₹[X] — compliance risk" | Critical (red) |

---

## 4. KPI Summary Bar (6 cards)

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Active Vendors | Integer | COUNT(vendors) WHERE status = 'active' | Static blue | `#kpi-active-vendors` |
| 2 | Total Contracts | Integer | COUNT(contracts) WHERE status IN ('active', 'pending_approval') | Static blue | `#kpi-total-contracts` |
| 3 | Contract Value (Active) | ₹ Amount | SUM(contract_value) WHERE status = 'active' | Static blue | `#kpi-contract-value` |
| 4 | Pending Payments | ₹ Amount | SUM(invoice_amount - paid_amount) WHERE payment_status IN ('pending', 'partial') | Red > ₹20L, Amber ₹5L–₹20L, Green < ₹5L | `#kpi-pending-payments` |
| 5 | Overdue Deliverables | Integer | COUNT(deliverables) WHERE due_date < today AND status != 'delivered' | Red > 0, Green = 0 | `#kpi-overdue-deliverables` |
| 6 | Avg Vendor Rating | Decimal (1–5) | AVG(vendor_rating) across active vendors with ≥ 3 ratings | Green ≥ 4.0, Amber 3.0–3.9, Red < 3.0 | `#kpi-avg-rating` |

**HTMX:** `hx-get="/api/v1/group/{id}/marketing/admin/vendors/kpis/"` → `hx-trigger="load, every 300s"`

---

## 5. Sections

### 5.1 Tab: Vendor Directory

Master database of all vendors the group works with — past and present.

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Vendor Name | Text (link) | Yes | Click opens vendor detail drawer |
| Vendor Type | Badge | Yes | Newspaper Ad Agency / Outdoor-BTL Agency / Digital Marketing Agency / Printing Vendor / Event Management / PR Agency / Telecalling Agency / SMS-WhatsApp Provider / Creative-Design Agency / Photography-Videography |
| GSTIN | Text | No | 15-character GSTIN; validated format; `—` if unregistered (threshold exemption) |
| City | Text | Yes | Primary operating city |
| Contact Person | Text | No | Name + phone |
| Active Contracts | Integer | Yes | COUNT of active contracts with this vendor |
| Total Spend (Season) | ₹ Amount | Yes | SUM of payments this season |
| Pending Payments | ₹ Amount | Yes | Outstanding invoices |
| Rating | Stars (1–5) | Yes | Average rating across all rated deliverables |
| Status | Badge | Yes | Active / Inactive / Blacklisted |
| Actions | Buttons | No | [View] [+ Contract] [Rate] |

**Default sort:** Status (Active first) → Vendor Name ASC
**Pagination:** Server-side · 25/page
**Filters:** Vendor Type / Status / City / Rating range / Spend range

**Vendor types (complete list):**

| Vendor Type | Typical Services | GST SAC | TDS Section |
|---|---|---|---|
| Newspaper Ad Agency | Ad booking across publications, insertion scheduling, rate negotiation | 998361 (Advertising) | 194C (2%) or 194J (10%) |
| Outdoor / BTL Agency | Hoardings, bus shelters, auto wraps, flex banners, pamphlet distribution | 998361 | 194C (2%) |
| Digital Marketing Agency | Google Ads management, Meta campaigns, YouTube ads, SEO | 998314 (IT services) | 194J (10%) |
| Printing Vendor | Brochures, prospectus, flex banners, standees, visiting cards, ID cards | 998912 (Printing) | 194C (2%) |
| Event Management | Open days, felicitation ceremonies, school fairs, stall setup | 998397 (Event management) | 194C (2%) |
| PR Agency | Press releases, media relations, journalist coordination, crisis comm | 998361 | 194J (10%) |
| Telecalling Agency | Outsourced telecalling, appointment booking, survey calls | 998519 (Telecom services) | 194C (2%) |
| SMS / WhatsApp Provider | Bulk SMS, WhatsApp Business API, DLT templates, delivery reports | 998313 (Telecom) | 194J (10%) |
| Creative / Design Agency | Artwork, logo design, video editing, social media creatives | 998396 (Creative services) | 194J (10%) |
| Photography / Videography | Event photography, testimonial videos, campus shoots, drone footage | 998393 (Photography) | 194J (10%) |

### 5.2 Tab: Contracts

All vendor contracts — active, expired, and pending approval.

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Contract ID | Text | Yes | Auto-generated: `CNT-2026-001` |
| Vendor | Text (link) | Yes | Vendor name — click opens vendor drawer |
| Contract Title | Text | No | E.g., "Eenadu Newspaper Ads — Season 2026-27" |
| Scope | Text (truncated) | No | Brief description of services covered |
| Start Date | Date | Yes | Contract start |
| End Date | Date | Yes | Contract end |
| Contract Value | ₹ Amount | Yes | Total contracted amount |
| Spent | ₹ Amount | Yes | Payments made against this contract |
| Utilisation % | Progress bar | Yes | Spent / Contract Value × 100 |
| Remaining | ₹ Amount | Yes | Contract Value − Spent |
| Payment Terms | Badge | No | Advance / Milestone / Post-Campaign / Monthly Retainer |
| Deliverables | Fraction | Yes | Completed / Total (e.g., "8/12") |
| Status | Badge | Yes | Draft / Pending Approval / Active / Completed / Expired / Terminated |
| Days to Expiry | Integer | Yes | Red ≤ 30, Amber 31–60, Green > 60, Grey = expired |
| Actions | Buttons | No | [View] [Edit] [Renew] [Terminate] |

**Default sort:** Status (Active first) → End Date ASC (soonest expiry first)
**Pagination:** Server-side · 25/page
**Filters:** Vendor / Vendor Type / Status / Payment Terms / Date range / Value range

**Contract status lifecycle:**
```
DRAFT → PENDING_APPROVAL → ACTIVE → COMPLETED
                                  → EXPIRED (auto, if end_date passed without renewal)
                                  → TERMINATED (manual, with reason)
```

**Approval rules:**
- Contract value ≤ ₹1,00,000: Auto-approved by Campaign Manager (119)
- Contract value ₹1,00,001–₹5,00,000: Campaign Manager approval
- Contract value > ₹5,00,000: CEO (G4) approval required
- Any contract with auto-renewal clause: CEO approval regardless of value

### 5.3 Tab: Deliverables

Tracks every deliverable across all active contracts.

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Deliverable | Text | Yes | E.g., "50,000 brochures — 4-colour A4 tri-fold" |
| Contract | Text (link) | Yes | Parent contract |
| Vendor | Text | Yes | Vendor name |
| Due Date | Date | Yes | Expected delivery date |
| Delivered Date | Date | Yes | Actual delivery date (blank if pending) |
| Quantity Expected | Integer | No | Contracted quantity |
| Quantity Delivered | Integer | No | Actual quantity received |
| Quality Rating | Stars (1–5) | Yes | Post-delivery quality assessment |
| Status | Badge | Yes | Pending / In Progress / Delivered / Overdue / Rejected / Partially Delivered |
| Variance | Text | No | Quantity shortfall or delay in days |
| Actions | Buttons | No | [Mark Delivered] [Rate Quality] [Flag Issue] |

**Default sort:** Status (Overdue first) → Due Date ASC
**Pagination:** Server-side · 25/page
**Filters:** Vendor / Contract / Status / Due date range

**Deliverable status lifecycle:**
```
PENDING → IN_PROGRESS → DELIVERED → (Quality rated)
                      → PARTIALLY_DELIVERED → DELIVERED
                      → OVERDUE (auto, if due_date < today and not delivered)
                      → REJECTED (quality unacceptable, re-do required)
```

### 5.4 Tab: Payments

Invoice and payment ledger for all vendor transactions.

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Invoice # | Text | Yes | Vendor invoice number |
| Invoice Date | Date | Yes | Date on vendor invoice |
| Vendor | Text (link) | Yes | Vendor name |
| Contract | Text (link) | Yes | Linked contract |
| Description | Text | No | E.g., "Eenadu half-page ads — Jan 1–15 (6 insertions)" |
| Invoice Amount | ₹ Amount | Yes | Gross invoice amount |
| GST Amount | ₹ Amount | No | 18% GST on services (auto-calculated from base amount) |
| TDS Deducted | ₹ Amount | No | TDS amount (2% or 10% based on vendor type) |
| Net Payable | ₹ Amount | Yes | Invoice Amount − TDS |
| Paid Amount | ₹ Amount | Yes | Amount actually paid |
| Payment Date | Date | Yes | When payment was made |
| Payment Mode | Badge | No | NEFT / RTGS / Cheque / UPI |
| Payment Status | Badge | Yes | Pending / Partial / Paid / Overdue / Disputed |
| Due Date | Date | Yes | Payment due date per contract terms |
| Days Outstanding | Integer | Yes | Red > 30, Amber 15–30, Green ≤ 14 |
| Actions | Buttons | No | [Record Payment] [View Invoice] [Dispute] |

**Default sort:** Payment Status (Overdue first, then Pending) → Due Date ASC
**Pagination:** Server-side · 50/page
**Filters:** Vendor / Contract / Payment Status / Date range / Amount range

**GST compliance rules:**
- Vendor GSTIN must be validated against GST portal before first payment
- Invoice must contain: vendor GSTIN, SAC code, taxable value, CGST/SGST or IGST breakup
- If vendor is unregistered (turnover < ₹20L threshold), group may be liable for reverse charge on specified services
- All payments above ₹50,000 must have a valid invoice on file
- TDS certificates (Form 16A) generated quarterly for each vendor

### 5.5 Tab: Performance Scorecards

Aggregated vendor performance view.

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Vendor | Text | Yes | Vendor name |
| Vendor Type | Badge | Yes | Category |
| Contracts (All Time) | Integer | Yes | Total contracts |
| Total Spend (All Time) | ₹ Amount | Yes | Lifetime spend |
| On-Time Delivery % | Percentage | Yes | Deliverables delivered on or before due date / total deliverables |
| Avg Quality Rating | Stars (1–5) | Yes | Average across all rated deliverables |
| Payment Disputes | Integer | Yes | Count of payment disputes |
| Contract Renewals | Integer | Yes | How many times contract renewed (loyalty indicator) |
| Overall Score | Badge | Yes | Excellent (≥ 4.5) / Good (3.5–4.4) / Average (2.5–3.4) / Poor (< 2.5) |
| Recommendation | Badge | No | Renew / Review / Replace / Blacklist |
| Actions | Buttons | No | [View Details] [Compare] |

**Default sort:** Overall Score DESC
**Colour coding:**
- Green row: Excellent (≥ 4.5 score, ≥ 90% on-time)
- Amber row: Average (2.5–3.4 score, 70–89% on-time)
- Red row: Poor (< 2.5 score or < 70% on-time)

---

## 6. Drawers & Modals

### 6.1 Modal: `add-vendor` (560px)

- **Title:** "Add New Vendor"
- **Fields:**
  - Vendor name (text, required)
  - Vendor type (dropdown — 10 types from §5.1, required)
  - GSTIN (text, 15-char validated, optional — blank if unregistered)
  - PAN (text, 10-char validated, required — needed for TDS)
  - Contact person name (text, required)
  - Contact phone (text, required, Indian mobile validated)
  - Contact email (email, optional)
  - Address — Street, City, State, PIN (text fields, required)
  - Bank account name (text, required)
  - Bank name (text, required)
  - Account number (text, required)
  - IFSC code (text, 11-char validated, required)
  - Notes (textarea, optional)
- **Validation:**
  - GSTIN format: `^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$`
  - PAN format: `^[A-Z]{5}[0-9]{4}[A-Z]{1}$`
  - IFSC format: `^[A-Z]{4}0[A-Z0-9]{6}$`
  - Duplicate GSTIN check: warn if GSTIN already exists in vendor DB
  - Duplicate PAN check: warn if PAN already exists
- **Buttons:** Cancel · Add Vendor
- **Access:** Role 119 or G4+

### 6.2 Drawer: `vendor-detail` (720px, right-slide)

- **Title:** "[Vendor Name] — Vendor Profile"
- **Tabs:** Overview · Contracts · Deliverables · Payments · Ratings · Activity Log
- **Overview tab:**
  - Vendor details (name, type, GSTIN, PAN, contact, address, bank details)
  - Lifetime stats: total contracts, total spend, total deliverables, avg rating
  - Current season stats: active contracts, season spend, pending payments
  - Status badge with [Deactivate] / [Blacklist] buttons
- **Contracts tab:**
  - Table of all contracts with this vendor (same columns as §5.2, filtered)
  - [+ New Contract] button
- **Deliverables tab:**
  - Table of all deliverables across contracts (same columns as §5.3, filtered)
  - Status filter: All / Pending / Overdue / Delivered
- **Payments tab:**
  - Table of all payments to this vendor (same columns as §5.4, filtered)
  - Summary: Total invoiced, Total paid, Outstanding, TDS deducted (cumulative)
  - [Record Payment] button
- **Ratings tab:**
  - Timeline of all quality ratings given to this vendor
  - Each entry: deliverable name, date, rating (1–5 stars), reviewer, notes
  - Aggregate: overall score, on-time %, quality trend chart (sparkline)
- **Activity Log tab:**
  - Chronological log: contract created, deliverable marked, payment recorded, rating given
  - Filterable by activity type
- **Footer:** [Edit Vendor] [+ New Contract] [Record Payment] [Export Vendor Report]
- **Access:** Role 119 (full), 132 (read), 131 (read — content vendors only), G4+ (full read)

### 6.3 Modal: `add-contract` (640px)

- **Title:** "New Vendor Contract"
- **Fields:**
  - Vendor (dropdown from active vendor list, required)
  - Contract title (text, required — e.g., "Eenadu Newspaper Ads — Season 2026-27")
  - Scope of work (textarea, required — detailed description of services)
  - Start date (date, required)
  - End date (date, required)
  - Contract value (₹, required)
  - Payment terms (dropdown: Advance / Milestone / Post-Campaign / Monthly Retainer, required)
  - Payment schedule (textarea — e.g., "50% advance, 25% at mid-point, 25% on completion")
  - Auto-renewal (checkbox + renewal terms if checked)
  - Deliverables (repeater field):
    - Deliverable name (text)
    - Quantity (integer)
    - Due date (date)
    - Description (text)
  - Contract document upload (PDF, max 25 MB)
  - Notes (textarea, optional)
- **Approval preview:** "Contract value ₹[X] → [Auto-approved / Requires Campaign Manager approval / Requires CEO approval]"
- **Buttons:** Cancel · Save as Draft · Submit for Approval
- **Access:** Role 119 or G4+

### 6.4 Modal: `record-payment` (560px)

- **Title:** "Record Vendor Payment"
- **Fields:**
  - Vendor (dropdown, required — pre-filled if opened from vendor drawer)
  - Contract (dropdown — filtered to vendor's active contracts, required)
  - Invoice number (text, required)
  - Invoice date (date, required)
  - Invoice amount (₹, required — gross amount including GST)
  - Base amount (₹, auto-calculated — invoice amount / 1.18 if GST applicable)
  - GST amount (₹, auto-calculated — base amount × 0.18)
  - GST type (dropdown: CGST+SGST / IGST, auto-selected based on vendor state vs group state)
  - TDS section (auto-populated based on vendor type — 194C or 194J)
  - TDS rate (auto-populated — 2% or 10%)
  - TDS amount (₹, auto-calculated — base amount × TDS rate)
  - Net payable (₹, auto-calculated — invoice amount − TDS)
  - Payment amount (₹, required — can be partial)
  - Payment date (date, required)
  - Payment mode (dropdown: NEFT / RTGS / Cheque / UPI)
  - Payment reference (text — UTR number / cheque number)
  - Upload invoice scan (PDF/JPG, max 10 MB)
  - Notes (textarea, optional)
- **Validation:**
  - Payment amount ≤ net payable (warn if exceeding, allow with override)
  - Invoice date ≤ today
  - Duplicate invoice number check (same vendor + same invoice #)
  - GSTIN on invoice must match vendor GSTIN on file
- **Buttons:** Cancel · Record Payment
- **Access:** Role 119 only

### 6.5 Modal: `rate-deliverable` (480px)

- **Title:** "Rate Deliverable — [Deliverable Name]"
- **Fields:**
  - Vendor (read-only, pre-filled)
  - Deliverable (read-only, pre-filled)
  - Delivery date (date, required — when actually received)
  - Quantity delivered (integer, required)
  - Quality dimensions:
    - Accuracy to brief (1–5 stars)
    - Timeliness (1–5 stars, auto-suggested based on due vs delivery date)
    - Material quality (1–5 stars)
    - Communication during execution (1–5 stars)
    - Overall satisfaction (1–5 stars)
  - Issues found (multi-select: None / Colour mismatch / Quantity shortfall / Late delivery / Wrong specification / Material defect / Other)
  - Notes (textarea)
  - Re-do required? (checkbox — if yes, sets status to REJECTED)
- **Buttons:** Cancel · Submit Rating
- **Access:** Role 119 or G4+

---

## 7. Charts

### 7.1 Spend by Vendor Type (Donut)

| Property | Value |
|---|---|
| Chart type | Donut (Chart.js 4.x) |
| Title | "Spend by Vendor Type — Current Season" |
| Data | SUM(payments) grouped by vendor_type |
| Colour | Newspaper: `#EF4444` red / Digital: `#3B82F6` blue / Outdoor: `#F59E0B` amber / Printing: `#10B981` green / Event: `#8B5CF6` purple / PR: `#EC4899` pink / SMS-WhatsApp: `#06B6D4` cyan / Creative: `#F97316` orange / Photo-Video: `#6366F1` indigo / Telecalling: `#84CC16` lime |
| Centre text | Total spend ₹[X] |
| Tooltip | "[Type]: ₹[X] ([Y]%) — [N] vendors" |
| API | `GET /api/v1/group/{id}/marketing/admin/vendors/analytics/spend-by-type/` |

### 7.2 Vendor Performance Comparison (Horizontal Bar)

| Property | Value |
|---|---|
| Chart type | Horizontal bar (Chart.js 4.x) |
| Title | "Vendor Performance Scores — Active Vendors" |
| Data | Overall performance score (1–5) per active vendor |
| X-axis | Score (0–5) |
| Y-axis | Vendor name |
| Colour | Green ≥ 4.0, Amber 3.0–3.9, Red < 3.0 per bar |
| Benchmark line | 3.5 target (dashed grey vertical) |
| Tooltip | "[Vendor]: Score [X]/5 — On-time: [Y]%, Quality: [Z]/5" |
| API | `GET /api/v1/group/{id}/marketing/admin/vendors/analytics/performance-scores/` |

### 7.3 Payment Timeline (Stacked Area)

| Property | Value |
|---|---|
| Chart type | Stacked area (Chart.js 4.x) |
| Title | "Monthly Vendor Payments — Current Season" |
| Data | Monthly payment amount per vendor type (stacked) |
| X-axis | Month (season start → current) |
| Y-axis | ₹ Amount |
| Colour | Same vendor type palette as §7.1 |
| Tooltip | "[Month]: [Type] ₹[X] — Total: ₹[Y]" |
| Purpose | Identify payment concentration and seasonal spend pattern |
| API | `GET /api/v1/group/{id}/marketing/admin/vendors/analytics/payment-timeline/` |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Vendor added | "Vendor '[Name]' added to vendor directory" | Success | 3s |
| Vendor updated | "Vendor '[Name]' details updated" | Success | 2s |
| Vendor deactivated | "Vendor '[Name]' deactivated — active contracts preserved" | Info | 4s |
| Vendor blacklisted | "Vendor '[Name]' blacklisted — all active contracts flagged for review" | Warning | 5s |
| Contract created (draft) | "Contract '[Title]' saved as draft" | Info | 2s |
| Contract submitted | "Contract '[Title]' (₹[X]) submitted for approval" | Info | 3s |
| Contract approved | "Contract '[Title]' approved — vendor notified" | Success | 3s |
| Contract rejected | "Contract '[Title]' rejected — reason: [Reason]" | Warning | 5s |
| Contract renewed | "Contract '[Title]' renewed until [Date]" | Success | 3s |
| Payment recorded | "Payment of ₹[X] recorded for [Vendor] — TDS ₹[Y] deducted" | Success | 4s |
| Deliverable rated | "Deliverable rated [X]/5 — vendor overall score updated" | Success | 3s |
| Deliverable overdue alert | "[Vendor]: '[Deliverable]' is [N] days overdue — escalate immediately" | Error | 6s |
| Contract expiry alert | "[Vendor] contract expires in [N] days — review for renewal" | Warning | 5s |
| GSTIN validation failed | "[Vendor] GSTIN validation failed — verify with vendor before payment" | Error | 6s |
| Duplicate invoice warning | "Invoice #[X] already recorded for [Vendor] on [Date] — possible duplicate" | Warning | 5s |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| No vendors added | 🏢 | "No Vendors Yet" | "Add your marketing vendors and agencies to start tracking contracts, payments, and performance." | + Add Vendor |
| No contracts | 📄 | "No Contracts" | "Create your first vendor contract to start tracking deliverables and payments." | + New Contract |
| No deliverables | 📦 | "No Deliverables Tracked" | "Add deliverables to vendor contracts to track delivery timelines and quality." | — |
| No payments recorded | 💳 | "No Payments Recorded" | "Record your first vendor payment to start tracking spend and GST compliance." | Record Payment |
| No ratings given | ⭐ | "No Vendor Ratings" | "Rate vendor deliverables to build performance scorecards for informed renewal decisions." | — |
| Vendor search no results | 🔍 | "No Matching Vendors" | "No vendors match your search criteria. Try adjusting filters." | Clear Filters |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | 6 KPI shimmer cards + table skeleton (10 rows) |
| Vendor directory load | 10-row table skeleton with badge placeholders |
| Contracts tab | 8-row table skeleton |
| Deliverables tab | 10-row table skeleton |
| Payments tab | 15-row table skeleton |
| Vendor detail drawer | 720px skeleton: header + 6 tab placeholders |
| Performance scorecards | 8-row table skeleton with star placeholders |
| Add vendor modal | Form skeleton (12 fields) |
| Chart load | Grey canvas placeholder per chart |
| Payment recording | Button spinner → toast |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/marketing/admin/vendors/` | G1+ | List all vendors (paginated, filterable) |
| POST | `/api/v1/group/{id}/marketing/admin/vendors/` | G3+ (119) | Add new vendor |
| GET | `/api/v1/group/{id}/marketing/admin/vendors/{vendor_id}/` | G1+ | Vendor detail |
| PATCH | `/api/v1/group/{id}/marketing/admin/vendors/{vendor_id}/` | G3+ (119) | Update vendor |
| PATCH | `/api/v1/group/{id}/marketing/admin/vendors/{vendor_id}/status/` | G3+ (119) | Activate / Deactivate / Blacklist vendor |
| GET | `/api/v1/group/{id}/marketing/admin/vendors/{vendor_id}/activity/` | G1+ | Vendor activity log |
| GET | `/api/v1/group/{id}/marketing/admin/vendors/kpis/` | G1+ | KPI values |
| POST | `/api/v1/group/{id}/marketing/admin/vendors/contracts/` | G3+ (119) | Create new contract |
| GET | `/api/v1/group/{id}/marketing/admin/vendors/contracts/` | G1+ | List all contracts (paginated) |
| GET | `/api/v1/group/{id}/marketing/admin/vendors/contracts/{contract_id}/` | G1+ | Contract detail |
| PATCH | `/api/v1/group/{id}/marketing/admin/vendors/contracts/{contract_id}/` | G3+ (119) | Update contract |
| PATCH | `/api/v1/group/{id}/marketing/admin/vendors/contracts/{contract_id}/approval/` | G3+ (119/G4+) | Approve / Reject contract |
| POST | `/api/v1/group/{id}/marketing/admin/vendors/contracts/{contract_id}/renew/` | G3+ (119) | Renew contract |
| PATCH | `/api/v1/group/{id}/marketing/admin/vendors/contracts/{contract_id}/terminate/` | G3+ (119) | Terminate contract |
| GET | `/api/v1/group/{id}/marketing/admin/vendors/deliverables/` | G1+ | List all deliverables (paginated) |
| PATCH | `/api/v1/group/{id}/marketing/admin/vendors/deliverables/{del_id}/` | G3+ (119) | Mark delivered / update status |
| POST | `/api/v1/group/{id}/marketing/admin/vendors/deliverables/{del_id}/rate/` | G3+ (119) | Rate deliverable quality |
| GET | `/api/v1/group/{id}/marketing/admin/vendors/payments/` | G1+ | List all payments (paginated) |
| POST | `/api/v1/group/{id}/marketing/admin/vendors/payments/` | G3+ (119) | Record payment |
| GET | `/api/v1/group/{id}/marketing/admin/vendors/payments/{payment_id}/` | G1+ | Payment detail |
| GET | `/api/v1/group/{id}/marketing/admin/vendors/scorecards/` | G1+ | Vendor performance scorecards |
| GET | `/api/v1/group/{id}/marketing/admin/vendors/analytics/spend-by-type/` | G1+ | Spend by vendor type (donut) |
| GET | `/api/v1/group/{id}/marketing/admin/vendors/analytics/performance-scores/` | G1+ | Vendor performance bar chart |
| GET | `/api/v1/group/{id}/marketing/admin/vendors/analytics/payment-timeline/` | G1+ | Monthly payment area chart |
| POST | `/api/v1/group/{id}/marketing/admin/vendors/export/` | G1+ | Export vendor report (CSV/PDF) |
| GET | `/api/v1/group/{id}/marketing/admin/vendors/gstin-validate/{gstin}/` | G3+ (119) | Validate GSTIN against GST portal |

---

## 12. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load | `<div id="kpi-bar">` | `hx-get=".../vendors/kpis/"` | `#kpi-bar` | `innerHTML` | `hx-trigger="load, every 300s"` |
| Vendor directory | Tab click | `hx-get=".../vendors/?tab=directory"` | `#tab-content` | `innerHTML` | `hx-trigger="load"` |
| Contracts tab | Tab click | `hx-get=".../vendors/contracts/"` | `#tab-content` | `innerHTML` | `hx-trigger="click"` |
| Deliverables tab | Tab click | `hx-get=".../vendors/deliverables/"` | `#tab-content` | `innerHTML` | `hx-trigger="click"` |
| Payments tab | Tab click | `hx-get=".../vendors/payments/"` | `#tab-content` | `innerHTML` | `hx-trigger="click"` |
| Scorecards tab | Tab click | `hx-get=".../vendors/scorecards/"` | `#tab-content` | `innerHTML` | `hx-trigger="click"` |
| Add vendor | Form submit | `hx-post=".../vendors/"` | `#vendor-result` | `innerHTML` | Toast + directory refresh |
| Vendor detail drawer | Row click | `hx-get=".../vendors/{id}/"` | `#right-drawer` | `innerHTML` | `hx-trigger="click"` |
| Add contract | Form submit | `hx-post=".../vendors/contracts/"` | `#contract-result` | `innerHTML` | Toast + contracts tab refresh |
| Approve contract | Approve button | `hx-patch=".../vendors/contracts/{id}/approval/"` | `#contract-row-{id}` | `outerHTML` | Inline status update |
| Record payment | Form submit | `hx-post=".../vendors/payments/"` | `#payment-result` | `innerHTML` | Toast + payments tab refresh |
| Rate deliverable | Form submit | `hx-post=".../vendors/deliverables/{id}/rate/"` | `#del-row-{id}` | `outerHTML` | Inline rating update |
| Filter vendors | Filter controls | `hx-get` with filter params | `#tab-content` | `innerHTML` | `hx-trigger="change"` |
| Pagination | Page controls | `hx-get` with `?page={n}` | `#tab-content` | `innerHTML` | Table body replacement |
| GSTIN validate | GSTIN field blur | `hx-get=".../vendors/gstin-validate/{gstin}/"` | `#gstin-status` | `innerHTML` | `hx-trigger="blur"` — green tick or red warning |
| Chart load | Chart containers | `hx-get=".../vendors/analytics/..."` | `#chart-{name}` | `innerHTML` | `hx-trigger="load"` |

---

*Page spec version: 1.0 · Last updated: 2026-03-26*
