# C-02 — Online Fee Payment

> **URL:** `/parent/fees/pay/`
> **File:** `c-02-online-payment.md`
> **Priority:** P1
> **Roles:** Parent (initiate & complete payment) · Institution Accounts Office (reconciliation) · EduForge Finance (gateway settlement)

---

## 1. Payment Initiation — Select Child & Fee Heads

```
ONLINE FEE PAYMENT — Mrs. Lakshmi Devi

  ── SELECT CHILD ─────────────────────────────────────────────────────────
  (o) Ravi Kumar — GCEH Hyderabad    Pending: Rs. 1,00,000
  ( ) Priya Kumar — Sri Chaitanya    Pending: Rs. 27,250
  ( ) Ravi Kumar — TopRank Academy   Auto-debit active (no manual payment needed)

  ── SELECTED: RAVI KUMAR — GCEH HYDERABAD ───────────────────────────────
  2nd Instalment (Due: 15 Jan 2026)

  Fee Head             Amount      Select
  ─────────────────    ─────────   ──────
  Tuition Fee          42,500      [x]
  Special Fee           7,500      [x]
  Exam Fee             10,000      [x]
  Hostel Fee           40,000      [x]
  ─────────────────    ─────────
  Selected Total     1,00,000

  PAYMENT OPTIONS:
  (o) Pay full instalment — Rs. 1,00,000
  ( ) Pay selected heads only — choose above
  ( ) Pay partial amount — enter custom amount (min Rs. 5,000)

  ── PARTIAL PAYMENT / EMI ────────────────────────────────────────────────
  GCEH allows partial payment with prior approval.
  Approved partial plan for Ravi Kumar:
    Part 1: Rs. 50,000 by 15 Jan 2026
    Part 2: Rs. 50,000 by 15 Feb 2026 (+ Rs. 600 late fee on Part 2)

  ( ) Use approved partial plan — pay Rs. 50,000 now

  [Proceed to Payment →]
```

---

## 2. Payment Gateway — Method Selection & Checkout

```
PAYMENT CHECKOUT

  Amount: Rs. 1,00,000
  For:    Ravi Kumar — GCEH Hyderabad — 2nd Instalment 2025–26
  Ref:    GCEH/FEE/2025-26/RK-3CSE/INS2

  ── SELECT PAYMENT METHOD ────────────────────────────────────────────────

  UPI (Recommended — no convenience fee)
  ┌──────────────────────────────────────────────────────┐
  │  (o) GPay          UPI ID: [ lakshmi.devi@okicici  ] │
  │  ( ) PhonePe       UPI ID: [                       ] │
  │  ( ) Paytm UPI     UPI ID: [                       ] │
  │  ( ) Other UPI     UPI ID: [                       ] │
  │                                                      │
  │  UPI Limit Note: Most banks allow Rs. 1,00,000/txn   │
  │  for education payments (enhanced limit category)     │
  └──────────────────────────────────────────────────────┘

  Net Banking
  ┌──────────────────────────────────────────────────────┐
  │  Popular: SBI | HDFC | ICICI | Axis | Kotak          │
  │  All Banks ▼                                         │
  │  Convenience fee: Rs. 0 (absorbed by institution)    │
  └──────────────────────────────────────────────────────┘

  Credit / Debit Card
  ┌──────────────────────────────────────────────────────┐
  │  Card Number:  [                                   ] │
  │  Expiry:       [MM/YY]    CVV: [   ]                 │
  │  Name on Card: [                                   ] │
  │                                                      │
  │  Credit Card EMI available (HDFC, ICICI, SBI):       │
  │  3 months — Rs. 33,890/mo (0% interest, processing   │
  │             fee Rs. 670)                              │
  │  6 months — Rs. 17,270/mo (0% interest, processing   │
  │             fee Rs. 1,120)                            │
  │                                                      │
  │  Convenience fee: 1.2% (Rs. 1,200) for credit card   │
  │  Debit card: Rs. 0 convenience fee                   │
  └──────────────────────────────────────────────────────┘

  ── ORDER SUMMARY ────────────────────────────────────────────────────────
  Fee Amount:                        Rs. 1,00,000
  Convenience Fee:                   Rs.        0   (UPI — no charge)
  ─────────────────────────────────  ─────────────
  Total Payable:                     Rs. 1,00,000

  Gateway: Razorpay (Secure — PCI DSS Level 1)
  Institution GSTIN: 36AABCG1234H1ZQ

  [Pay Rs. 1,00,000 →]

  By proceeding, you agree to the payment terms. Refund policy:
  fee refunds are processed by the institution, not EduForge.
```

---

## 3. Payment Confirmation & Post-Payment

```
PAYMENT SUCCESSFUL

  ── TRANSACTION DETAILS ──────────────────────────────────────────────────
  Transaction ID:     RZP-20260115-GCEH-4829371
  EduForge Ref:       EF-PAY-2026-0115-98432
  Institution Ref:    GCEH/FEE/2025-26/RK-3CSE/INS2
  Date & Time:        15 Jan 2026, 10:23:47 IST
  Amount Paid:        Rs. 1,00,000
  Payment Method:     UPI — lakshmi.devi@okicici
  Status:             SUCCESS

  ── FEE HEADS CLEARED ────────────────────────────────────────────────────
  Tuition Fee          Rs. 42,500    ✅
  Special Fee          Rs.  7,500    ✅
  Exam Fee             Rs. 10,000    ✅
  Hostel Fee           Rs. 40,000    ✅

  ── UPDATED BALANCE ──────────────────────────────────────────────────────
  Ravi Kumar — GCEH:   Rs. 0 pending (fully paid for 2025–26)

  [Download Receipt (PDF)]   [Share via WhatsApp]   [View Dashboard]

  SMS sent to +91-98765-XXXXX: "Rs. 1,00,000 paid for Ravi Kumar at GCEH.
  Ref: RZP-20260115-GCEH-4829371. Receipt: eduforge.in/r/98432"
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|--------|----------|-------------|
| 1 | `POST` | `/api/v1/parent/fees/pay/initiate/` | Create payment order (child_id, fee_heads, amount) |
| 2 | `GET` | `/api/v1/parent/fees/pay/{order_id}/methods/` | Available payment methods for the order amount |
| 3 | `POST` | `/api/v1/parent/fees/pay/{order_id}/execute/` | Submit payment via selected gateway + method |
| 4 | `GET` | `/api/v1/parent/fees/pay/{order_id}/status/` | Poll payment status (pending/success/failed) |
| 5 | `POST` | `/api/v1/parent/fees/pay/{order_id}/retry/` | Retry a failed payment with same or different method |
| 6 | `GET` | `/api/v1/parent/fees/pay/history/` | All past payment transactions for the parent |
| 7 | `POST` | `/api/v1/parent/fees/pay/partial-plan/request/` | Request partial payment plan approval from institution |

---

## 5. Business Rules

- Payment gateway selection follows a dual-gateway architecture where Razorpay is the primary gateway and Paytm Payment Gateway serves as the fallback; when the parent clicks "Pay", the system first attempts to create an order on Razorpay, and if the Razorpay API returns an error or does not respond within 5 seconds, the system seamlessly falls back to Paytm PG without the parent noticing any delay; this failover is essential for high-volume periods like July (college admission season) and January (second instalment season) when gateway load is heavy; the gateway used is recorded against the transaction for reconciliation, and EduForge's finance module settles with the institution within T+2 business days regardless of which gateway processed the payment.

- UPI payment for education fees benefits from the NPCI enhanced transaction limit of Rs. 1,00,000 for education-category merchants, compared to the standard Rs. 1,00,000 general UPI limit; the system sets the merchant category code (MCC) to 8211 (Elementary and Secondary Schools) or 8220 (Colleges/Universities) as appropriate so that the UPI transaction is classified under the education category; convenience fees are zero for UPI and debit cards as per institution policy (the institution absorbs the MDR), while credit card payments carry a 1.2% convenience fee that is clearly disclosed before the parent confirms payment; credit card EMI options at 0% interest are available through pre-negotiated arrangements with HDFC, ICICI, and SBI credit cards for transactions above Rs. 25,000.

- Partial payment and instalment flexibility must be governed by each institution's specific policy, not by EduForge's platform defaults; GCEH allows partial payment only with prior written approval from the accounts office (the parent requests this through the platform, and the accounts office approves or rejects within 48 hours), Sri Chaitanya does not allow partial payment within a quarterly instalment (the full quarter must be paid at once), and TopRank's coaching subscription is a fixed Rs. 299/month with no partial option; when partial payment is approved, the system creates a payment plan with specific due dates and automatically calculates the late fee that will apply to deferred portions based on the institution's late fee rate; the parent sees this breakdown before accepting the plan.

- Transaction reconciliation across the three-party flow (parent to gateway, gateway to EduForge, EduForge to institution) requires deterministic reference tracking; every payment generates three reference numbers: the gateway transaction ID (e.g., RZP-20260115-GCEH-4829371), the EduForge platform reference (e.g., EF-PAY-2026-0115-98432), and the institution's fee receipt number (e.g., GCEH/FEE/2025-26/RK-3CSE/INS2); if a payment succeeds at the gateway but the callback to EduForge fails (network issue), the system runs a reconciliation job every 15 minutes that polls the gateway API for pending transactions and matches them against the institution's fee ledger; the parent receives the success confirmation only after the institution's ledger is updated, ensuring the institution's accounts office never has a discrepancy between online payments and their fee management system.

---

*Last updated: 2026-03-31 · Group 8 — Parents Portal · Division C*
