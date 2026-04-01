# P-03 — Payment Gateway Integration

> **URL:** `/coaching/partners/payments/`
> **File:** `p-03-payment-gateway.md`
> **Priority:** P2
> **Roles:** Accounts Manager (K5) · Branch Manager (K6) · IT Coordinator (K3)

---

## 1. Payment Gateway Overview

```
PAYMENT GATEWAY — Razorpay Integration
TCC Edu Pvt Ltd | Merchant ID: RZRPAY-TCC-001

  INTEGRATION STATUS: ✅ LIVE
  Uptime (Q3):      99.98% (0 failures in March 2026)
  Settlement:       T+2 business days → Axis Bank current account
  Transaction fee:  2% on UPI / 2% cards / ₹15 flat on netbanking

  PAYMENT METHODS ENABLED:
    ✅ UPI (Google Pay, PhonePe, Paytm, BHIM) — 68% of transactions
    ✅ Debit/Credit Card (Visa, Mastercard, RuPay) — 22% of transactions
    ✅ Net Banking (major banks) — 8% of transactions
    ✅ EMI (credit card EMI — for fee amounts > ₹5,000) — 2% of transactions
    ❌ Cash: Accepted at counter but NOT via gateway (separate cash register)
    ❌ Cheque: No longer accepted (discontinued Apr 2025 for operational simplicity)

  MONTHLY VOLUME (March 2026):
    Total transactions:    284
    Total amount:          ₹14.2 L
    Gateway fee:           ₹28,400 (2% avg)
    Settlement received:   ₹13.72 L (after gateway fee deduction)
    Failed transactions:     6 (2.1% failure rate — mostly UPI timeout)
    Refunds processed:       3 (₹28,500 total — G-06 refund module)
```

---

## 2. Payment Flow

```
PAYMENT FLOW — Student Fee Collection

  STUDENT INITIATES PAYMENT:
    Student portal (O-01) → "Pay Now" → Razorpay checkout page
    OR
    Reception counter → staff generates payment link → student scans QR / pays

  RAZORPAY CHECKOUT:
    ┌─────────────────────────────────────────────┐
    │  TOPPERS COACHING CENTRE                    │
    │  Amount: ₹8,000.00 (EMI instalment 2/4)    │
    │                                             │
    │  [PAY WITH UPI      ]  [CARD / NETBANKING] │
    │                                             │
    │  UPI ID: [student enters UPI ID or QR]     │
    │                                             │
    │  [PAY ₹8,000]                              │
    └─────────────────────────────────────────────┘

  PAYMENT PROCESSING:
    Student pays → Razorpay processes → success/failure
    On success: webhook sent to EduForge → fee record updated → receipt generated
    On failure: student notified → retry or alternate method

  RECEIPT GENERATION:
    Auto-generated: TCC-RCP-YYYY-XXXX format
    Contains: Student name, roll no, amount, payment method, date, GST breakup
    Delivered: Email + WhatsApp + available in student portal

  SETTLEMENT:
    Daily settlement report from Razorpay → Accounts Manager review → Tally entry
    Reconciliation: Razorpay dashboard total must match EduForge fee collected + bank credit
```

---

## 3. Reconciliation & Exceptions

```
PAYMENT RECONCILIATION — March 2026

  SUMMARY:
    EduForge fee module (total collected):  ₹14.20 L
    Razorpay dashboard (total processed):   ₹14.20 L ✅ Match
    Bank settlement received (T+2):         ₹13.72 L (after ₹0.28L gateway fee) ✅
    Manual cash collected (separate):       ₹ 0.48 L (cash register)
    GRAND TOTAL COLLECTED:                  ₹14.68 L

  EXCEPTIONS:
    Failed transactions (6):   Students retried — all eventually collected ✅
    Partial payment error (1): ₹3,999 charged instead of ₹4,000 (rounding in UPI)
                               — ₹1 collected separately via cash ✅ (documented)
    Refund processed (3):      ₹28,500 (G-06 refunds — course withdrawal × 2, overcharge × 1)

  PENDING SETTLEMENT:
    30–31 Mar transactions:    ₹1.84 L (T+2 = arrives Apr 2)
    Expected bank credit:      Apr 2, 2026 ✅ (standard settlement cycle)

  GATEWAY COST ANALYSIS:
    March gateway fee:  ₹28,400 (2% of ₹14.2L)
    Annual projection:  ₹3.4 L gateway fees
    Alternative (lower fee): HDFC payment gateway (1.8%) — saves ~₹0.3L/yr
    Decision: Razorpay preferred for its UPI success rate and dashboard UX
              Review at EduForge contract renewal (Dec 2026)
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `POST` | `/api/v1/coaching/{id}/payments/initiate/` | Create Razorpay payment order |
| 2 | `POST` | `/api/v1/coaching/{id}/payments/webhook/` | Razorpay webhook (success/failure callback) |
| 3 | `GET` | `/api/v1/coaching/{id}/payments/reconciliation/?month=2026-03` | Monthly reconciliation report |
| 4 | `POST` | `/api/v1/coaching/{id}/payments/refund/` | Initiate refund via gateway |
| 5 | `GET` | `/api/v1/coaching/{id}/payments/transactions/?month=2026-03` | Transaction history |
| 6 | `GET` | `/api/v1/coaching/{id}/payments/settlement/?date=2026-03-31` | Settlement status |

---

## 5. Business Rules

- The payment gateway webhook is the most critical integration point; when Razorpay processes a payment, it sends a webhook to EduForge's endpoint to update the fee record; if the webhook fails (network error, EduForge downtime), the payment was processed by Razorpay but EduForge shows no payment received — the student has paid but still shows as a defaulter; TCC's IT coordinator must monitor webhook delivery logs and manually reconcile any webhook failures daily; the Razorpay dashboard shows "delivered" vs "failed" webhook status; a failed webhook requires manual fee entry in EduForge with the Razorpay payment ID as reference
- PCI DSS compliance (Payment Card Industry Data Security Standard) requires that TCC never stores full card numbers, CVV, or payment credentials on TCC's systems; Razorpay's hosted checkout (the student pays on Razorpay's page, not TCC's) ensures TCC never touches raw card data; this hosted checkout model makes PCI DSS compliance much simpler — TCC is only required to be compliant at the "SAQ A" level (minimal self-assessment) rather than the full PCI audit; switching to a custom payment form where TCC collects card details would dramatically increase compliance requirements
- Refund processing through the gateway (₹28,500 in March) flows back to the original payment method; a student who paid via UPI receives the refund to the same UPI ID; a student who paid by card receives the refund to the same card (3–7 business days as per RBI); TCC cannot process the refund to a different account than the original payment source; if a student requests the refund to a different account ("send to my father's account"), the student must first receive the refund to their original payment source and then do their own transfer; this protects TCC from facilitating money laundering (refund to unknown beneficiary)
- The 2% gateway fee (₹3.4 lakh annually projected) is a legitimate business expense deductible for income tax purposes; it is classified as "bank charges" or "payment processing fees" in TCC's P&L; the gateway fee is captured in Tally when the daily settlement report is entered; the gross amount (₹14.2 lakh) is the revenue recognised; the gateway fee is the cost; netting only the settlement amount (₹13.72 lakh) as revenue would understate revenue and mismatch the student's fee receipt; the accounts team must enter gross revenue + gateway fee as separate line items in Tally
- The partial payment error (₹3,999 instead of ₹4,000 due to UPI rounding) illustrates a real-world edge case; some UPI apps round transaction amounts differently; the ₹1 shortfall was collected in cash and documented in the cash register with the reference Razorpay transaction ID; the student's fee record shows the full ₹4,000 received; the ₹1 cash entry closes the gap; this type of micro-reconciliation error is normal in high-volume collections and must be documented rather than ignored; ignored micro-discrepancies accumulate and create material reconciliation differences at year-end

---

*Last updated: 2026-03-31 · Group 5 — Coaching Portal · Division P*
