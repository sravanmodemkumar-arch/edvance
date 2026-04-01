# E-03 — Invoices & Payment History

> **URL:** `/tsp/admin/billing/invoices/`
> **File:** `e-03-invoices.md`
> **Priority:** P1
> **Roles:** TSP Admin · TSP Finance Manager · EduForge Finance Team

---

## 1. Invoice List & Details

```
INVOICES — TopRank Academy
EduForge platform invoices (what EduForge charges you)

  ── INVOICE HISTORY ─────────────────────────────────────────────────────────

  ┌──────────────────────────────────────────────────────────────────────────┐
  │ Inv #        │ Date       │ Period          │ Amount     │ Status       │
  │──────────────┼────────────┼─────────────────┼────────────┼──────────────│
  │ EF/2026/0312 │ 01 Mar 26  │ Mar 2026        │ ₹47,198.82│ ✅ Paid      │
  │ EF/2026/0211 │ 01 Feb 26  │ Feb 2026        │ ₹47,198.82│ ✅ Paid      │
  │ EF/2026/0115 │ 01 Jan 26  │ Jan 2026        │ ₹44,839.82│ ✅ Paid      │
  │ EF/2025/1218 │ 01 Dec 25  │ Dec 2025        │ ₹44,839.82│ ✅ Paid      │
  │ EF/2025/1120 │ 01 Nov 25  │ Nov 2025        │ ₹41,299.82│ ✅ Paid      │
  │ EF/2025/1019 │ 01 Oct 25  │ Oct 2025        │ ₹41,299.82│ ✅ Paid      │
  │ EF/2025/0922 │ 01 Sep 25  │ Sep 2025        │ ₹38,939.82│ ✅ Paid      │
  │ EF/2025/0817 │ 01 Aug 25  │ Aug 2025        │ ₹35,399.82│ ✅ Paid      │
  │ EF/2025/0714 │ 01 Jul 25  │ Jul 2025        │ ₹35,399.82│ ✅ Paid      │
  │ EF/2025/0616 │ 15 Jun 25  │ Jun 2025 (pro)  │ ₹19,466.41│ ✅ Paid      │
  └──────────────────────────────────────────────────────────────────────────┘

  Showing 10 of 10 invoices  │  Filter: [All ▼]  [FY 2025-26 ▼]
  [Download All as ZIP]  [Export to Tally XML]  [Export CSV]

  ── ANNUAL SUMMARY (FY 2025-26) ────────────────────────────────────────────

  ┌───────────────────────────────────────────────────────────────────────┐
  │  Total invoiced (Apr 2025 – Mar 2026):  ₹4,62,263.16               │
  │  Total paid:                            ₹4,62,263.16               │
  │  Outstanding:                           ₹       0.00               │
  │  Total GST paid (input credit):         ₹   70,514.72              │
  │                                                                     │
  │  Note: GST input credit of ₹70,514.72 can be claimed against       │
  │  your GST output liability. Ensure your CA reconciles these         │
  │  invoices during GSTR-2B matching.                                  │
  │                                                                     │
  │  [Download FY 2025-26 GST Summary]  [Download GSTR-2B Report]      │
  └───────────────────────────────────────────────────────────────────────┘
```

---

## 2. Invoice Detail View

```
INVOICE DETAIL — EF/2026/0312

  ┌───────────────────────────────────────────────────────────────────────┐
  │                          TAX INVOICE                                │
  │                                                                     │
  │  From:                          To:                                 │
  │  EduForge Technologies Pvt Ltd  TopRank Academy                     │
  │  Regd Office: Plot 42,          Prop: Suresh Reddy                  │
  │  Hitec City, Hyderabad          Door 15-3-22, MG Road               │
  │  Telangana 500081               Vijayawada, AP 520010               │
  │  GSTIN: 36AADCE1234F1ZP        GSTIN: 37AABFT5678G1ZQ             │
  │  PAN: AADCE1234F               PAN: AABFT5678G                     │
  │  SAC: 998314                    State: Andhra Pradesh (37)          │
  │  (Online content services)                                          │
  │                                                                     │
  │  Invoice #:   EF/2026/0312                                         │
  │  Date:        01 March 2026                                        │
  │  Due date:    01 March 2026 (auto-debit)                           │
  │  Period:      01 Mar 2026 – 31 Mar 2026                            │
  │  Place of supply: Andhra Pradesh (37)                              │
  │                                                                     │
  │ ─────────────────────────────────────────────────────────────────── │
  │ #  Description                    HSN/SAC   Qty    Rate    Amount  │
  │ ─────────────────────────────────────────────────────────────────── │
  │ 1  EduForge Growth Plan           998314     1   ₹24,999  ₹24,999 │
  │    (Platform subscription –                                        │
  │    up to 5,000 students)                                           │
  │                                                                     │
  │ 2  Content Licence Fee            998314  3,000     ₹5    ₹15,000 │
  │    (Question pool access –                                         │
  │    per student per month)                                          │
  │ ─────────────────────────────────────────────────────────────────── │
  │                                   Subtotal:          ₹39,999.00   │
  │                                                                     │
  │    Since supplier (Telangana 36) and recipient (AP 37) are in      │
  │    different states → IGST applies:                                │
  │                                                                     │
  │                                   IGST @ 18%:        ₹ 7,199.82   │
  │                                   ──────────────────────────────── │
  │                                   TOTAL:             ₹47,198.82   │
  │                                                                     │
  │    Amount in words: Rupees Forty-Seven Thousand One Hundred        │
  │    Ninety-Eight and Eighty-Two Paise Only                          │
  │                                                                     │
  │ ─────────────────────────────────────────────────────────────────── │
  │  PAYMENT DETAILS:                                                   │
  │  Payment method: Razorpay Auto-debit (HDFC Bank ****4521)          │
  │  Transaction ID: pay_NxQz7kLm2v8T1a                                │
  │  Payment date: 01 March 2026, 00:15 IST                           │
  │  Status: ✅ PAID                                                    │
  │                                                                     │
  │  BANK DETAILS (for manual payment):                                │
  │  EduForge Technologies Pvt Ltd                                     │
  │  ICICI Bank, Hitec City Branch, Hyderabad                          │
  │  A/c No: 1234 5678 9012 3456                                      │
  │  IFSC: ICIC0001234                                                 │
  │  UPI: eduforge@icici                                               │
  │                                                                     │
  │  [Download PDF]  [Download JSON (e-invoice)]  [Send to Email]      │
  │  [Report Issue with Invoice]                                       │
  └───────────────────────────────────────────────────────────────────────┘

  ── GST BREAKUP (INTER-STATE vs INTRA-STATE) ───────────────────────────────

  ┌───────────────────────────────────────────────────────────────────────┐
  │  EduForge is registered in Telangana (State Code: 36)               │
  │  TopRank Academy is registered in Andhra Pradesh (State Code: 37)   │
  │                                                                     │
  │  Since states differ → IGST applies (not CGST + SGST)              │
  │                                                                     │
  │  If same state (e.g., both in Telangana):                          │
  │    CGST @ 9%:  ₹3,599.91                                          │
  │    SGST @ 9%:  ₹3,599.91                                          │
  │    Total GST:  ₹7,199.82                                          │
  │                                                                     │
  │  Current (inter-state):                                            │
  │    IGST @ 18%: ₹7,199.82                                          │
  │    Total GST:  ₹7,199.82                                          │
  │                                                                     │
  │  Note: Total GST amount is the same; only the split changes.       │
  │  Your CA should claim IGST input credit under GSTR-3B.             │
  └───────────────────────────────────────────────────────────────────────┘
```

---

## 3. Payment History & Receipts

```
PAYMENT HISTORY — TopRank Academy
All payments made to EduForge

  ── PAYMENT LOG ─────────────────────────────────────────────────────────────

  ┌──────────────────────────────────────────────────────────────────────────┐
  │ Date       │ Invoice      │ Amount     │ Method         │ Txn ID       │
  │────────────┼──────────────┼────────────┼────────────────┼──────────────│
  │ 01 Mar 26  │ EF/2026/0312 │ ₹47,198.82│ Razorpay Auto  │ pay_NxQz7k.. │
  │ 01 Feb 26  │ EF/2026/0211 │ ₹47,198.82│ Razorpay Auto  │ pay_MwPy6j.. │
  │ 01 Jan 26  │ EF/2026/0115 │ ₹44,839.82│ Razorpay Auto  │ pay_LvOx5i.. │
  │ 01 Dec 25  │ EF/2025/1218 │ ₹44,839.82│ Razorpay Auto  │ pay_KuNw4h.. │
  │ 01 Nov 25  │ EF/2025/1120 │ ₹41,299.82│ NEFT           │ HDFC0211..   │
  │            │              │            │ (manual — auto │              │
  │            │              │            │  debit failed) │              │
  │ 01 Oct 25  │ EF/2025/1019 │ ₹41,299.82│ Razorpay Auto  │ pay_JtMv3g.. │
  │ 01 Sep 25  │ EF/2025/0922 │ ₹38,939.82│ Razorpay Auto  │ pay_IsLu2f.. │
  │ 01 Aug 25  │ EF/2025/0817 │ ₹35,399.82│ Razorpay Auto  │ pay_HrKt1e.. │
  │ 01 Jul 25  │ EF/2025/0714 │ ₹35,399.82│ Razorpay Auto  │ pay_GqJs0d.. │
  │ 15 Jun 25  │ EF/2025/0616 │ ₹19,466.41│ NEFT (onboard) │ HDFC0615..   │
  └──────────────────────────────────────────────────────────────────────────┘

  Payment health: 9/10 auto-debit successful (90%) — 1 manual fallback

  ── UPCOMING PAYMENTS ───────────────────────────────────────────────────────

  ┌───────────────────────────────────────────────────────────────────────┐
  │  Next invoice: EF/2026/0413                                        │
  │  Date: 01 April 2026                                               │
  │  Estimated amount: ₹47,198.82                                      │
  │  (Growth ₹24,999 + Content 3,000 x ₹5 + GST 18%)                 │
  │                                                                     │
  │  Payment method: Razorpay Auto-debit (HDFC Bank ****4521)          │
  │  Mandate status: ✅ Active (expires: 14 Jun 2026 — renewal needed) │
  │                                                                     │
  │  ⚠️  Auto-debit mandate expires in 75 days.                        │
  │  [Renew Mandate Now]  [Switch to Annual Billing (save ₹49,998)]    │
  └───────────────────────────────────────────────────────────────────────┘

  ── TDS DEDUCTION (SECTION 194J / 194O) ─────────────────────────────────────

  ┌───────────────────────────────────────────────────────────────────────┐
  │  If your organisation deducts TDS on SaaS payments:                 │
  │                                                                     │
  │  Applicable section: 194J (Fee for technical services) or           │
  │                      194O (if via e-commerce operator)              │
  │  TDS rate: 2% (194J) or 1% (194O)                                 │
  │                                                                     │
  │  Example (194J @ 2%):                                              │
  │  Invoice amount (pre-GST): ₹39,999.00                             │
  │  TDS @ 2%:                 ₹   799.98                              │
  │  Net payable:              ₹39,199.02                              │
  │  GST (on full amount):     ₹ 7,199.82                             │
  │  Total remitted:           ₹46,398.84                              │
  │                                                                     │
  │  EduForge PAN: AADCE1234F                                         │
  │  Please issue TDS certificate (Form 16A) quarterly.                │
  │                                                                     │
  │  TDS enabled for your account: (○) Yes  (●) No                    │
  │  [Enable TDS Deduction]                                            │
  └───────────────────────────────────────────────────────────────────────┘
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/tsp/billing/invoices/` | List all EduForge invoices for this TSP |
| 2 | `GET` | `/api/v1/tsp/billing/invoices/{invoice_id}/` | Get invoice detail with line items and GST |
| 3 | `GET` | `/api/v1/tsp/billing/invoices/{invoice_id}/pdf/` | Download invoice as PDF |
| 4 | `GET` | `/api/v1/tsp/billing/invoices/{invoice_id}/json/` | Download invoice as JSON (e-invoice format) |
| 5 | `GET` | `/api/v1/tsp/billing/payments/` | List all payments made to EduForge |
| 6 | `GET` | `/api/v1/tsp/billing/payments/{payment_id}/receipt/` | Download payment receipt |
| 7 | `GET` | `/api/v1/tsp/billing/gst-summary/` | GST summary for a financial year (input credit) |
| 8 | `GET` | `/api/v1/tsp/billing/gst-summary/gstr2b/` | GSTR-2B reconciliation report |
| 9 | `POST` | `/api/v1/tsp/billing/invoices/{invoice_id}/dispute/` | Raise a dispute on an invoice |
| 10 | `PATCH` | `/api/v1/tsp/billing/tds/config/` | Enable or disable TDS deduction on payments |
| 11 | `GET` | `/api/v1/tsp/billing/invoices/export/tally/` | Export invoices in Tally-compatible XML format |

---

## 5. Business Rules

- Every invoice EduForge issues to a TSP is a GST-compliant tax invoice under the Goods and Services Tax Act, 2017; invoices include the mandatory fields: supplier GSTIN (EduForge, 36AADCE1234F1ZP, Telangana), recipient GSTIN (TSP's registered GSTIN), SAC code 998314 (online content and software services), place of supply, and HSN/SAC-wise tax breakup; if the TSP is in the same state as EduForge (Telangana), the invoice shows CGST 9% + SGST 9%; if the TSP is in a different state (like TopRank in Andhra Pradesh), the invoice shows IGST 18%; the total GST amount is identical in both cases but the classification matters for GSTR-3B filing; EduForge generates e-invoices via the NIC (National Informatics Centre) portal for all B2B invoices above ₹5 crore aggregate turnover as mandated by GST rules, and provides IRN (Invoice Reference Number) and QR code on each invoice

- Payment collection from TSPs follows a strict auto-debit-first approach; on the 1st of each month at 00:15 IST, EduForge's billing system generates the invoice and initiates a Razorpay auto-debit against the TSP's registered bank account or card; if the auto-debit fails (insufficient funds, mandate expired, bank decline), the system retries on day 3 and day 5; simultaneously, the TSP Admin and TSP Finance Manager receive email, SMS, and WhatsApp notifications with a manual payment link; if payment is not received by day 10, the TSP's portal enters "payment pending" mode — a subtle banner appears on the TSP admin dashboard (not visible to students) warning of impending suspension; on day 15, if still unpaid, new student registrations are paused but existing students retain access; on day 30, the TSP portal is fully suspended (students see a maintenance page) until payment is received; this graduated escalation protects students from sudden disruption while ensuring EduForge collects its dues

- The Tally XML export and GSTR-2B reconciliation features are critical for Indian TSPs whose chartered accountants (CAs) use Tally ERP or Tally Prime for bookkeeping; the export formats follow Tally's XML schema version 7.2 and include all necessary ledger mappings — EduForge appears as a sundry creditor, platform fees map to "Software Subscription Expenses" under indirect expenses, and GST components auto-map to the appropriate CGST/SGST/IGST input credit ledgers; the GSTR-2B report compares EduForge's filed GSTR-1 (supplier return) against the TSP's auto-populated GSTR-2B to flag mismatches — for example, if EduForge filed an invoice for ₹47,198.82 but the TSP's books show ₹46,398.84 (because they deducted TDS), the mismatch report highlights the ₹799.98 difference as a TDS-related variance that the CA can reconcile

- TDS (Tax Deducted at Source) applicability depends on the TSP's organisational structure and annual payment volume; individual proprietors paying less than ₹30,000 per transaction (or ₹1,00,000 aggregate per year) to EduForge are not required to deduct TDS under Section 194J; however, companies, LLPs, and trusts must deduct TDS at 2% under Section 194J on the pre-GST invoice amount; some TSPs operating as e-commerce entities may fall under Section 194O at 1%; EduForge supports both scenarios — when TDS is enabled in the TSP billing settings, the auto-debit amount is reduced by the TDS percentage, and EduForge's finance team reconciles TDS credits quarterly using Form 26AS; the TSP must issue Form 16A (TDS certificate) to EduForge within 15 days of filing TDS returns, failing which EduForge may add the TDS amount back to the next invoice as per the partnership agreement

---

*Last updated: 2026-03-31 · Group 7 — TSP White-Label Portal · Division E*
