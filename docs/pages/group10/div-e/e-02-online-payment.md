# E-02 — Online Payment

> **URL:** `/student/fees/pay/{institution_id}`
> **File:** `e-02-online-payment.md`
> **Priority:** P1
> **Roles:** Student (S3–S6, 16+ for direct payment; 18+ for full access) · Parent (pays on behalf)

---

## Overview

Unified payment interface for institution fees, EduForge subscriptions, and any other charges. Powered by Razorpay with Paytm as fallback. Supports UPI (62% of payments), debit/credit cards, net banking, and wallets. Each institution's payment flows through their Razorpay sub-merchant account — EduForge acts as a payment facilitator, not a collector; money goes directly to the institution with EduForge's 2.5% platform commission deducted. Subscription payments go to EduForge directly. The payment page must handle 2,40,000 concurrent payment sessions during peak fee collection windows (June start-of-year).

---

## 1. Payment Flow — Institution Fee

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  PAY FEE — TopRank JEE Academy, Ameerpet                                    │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │  Fee Details                                                           │  │
│  │  ─────────────────────────────────────────────────────────────────    │  │
│  │  Monthly coaching fee — April 2026           ₹8,500.00               │  │
│  │  GST (18%)                                   Included                │  │
│  │  Late fee                                    ₹0 (pay before 10-Apr) │  │
│  │  ──────────────────────────────────────────────────────              │  │
│  │  Total payable                               ₹8,500.00               │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  ── PAYMENT METHOD ──────────────────────────────────────────────────────   │
│                                                                              │
│  (o) UPI — Pay directly from your bank account                              │
│      ┌────────────────────────────────────────────────────────────────┐     │
│      │  Pay via:                                                       │     │
│      │  [GPay]  [PhonePe]  [Paytm]  [BHIM]  [Other UPI App]         │     │
│      │                                                                 │     │
│      │  Or enter UPI ID: [ ravi.kumar@ybl                         ]   │     │
│      └────────────────────────────────────────────────────────────────┘     │
│                                                                              │
│  ( ) Debit Card                                                              │
│  ( ) Credit Card  (No-cost EMI available on HDFC, ICICI, SBI for ₹5,000+) │
│  ( ) Net Banking                                                             │
│  ( ) Wallet (Paytm / Amazon Pay / Freecharge)                               │
│                                                                              │
│  ── PARTIAL PAYMENT (if allowed by institution) ─────────────────────────   │
│  TopRank allows partial payment (minimum ₹2,000):                          │
│  Pay amount: [ ₹8,500 ]  (full amount pre-filled)                         │
│  Remaining after partial: ₹0                                               │
│                                                                              │
│  ☐ Save this payment method for future payments                            │
│                                                                              │
│                        [ Pay ₹8,500 → ]                                     │
│                                                                              │
│  🔒 Secure payment via Razorpay · PCI DSS Level 1 compliant                │
│  Money goes directly to TopRank JEE Academy's bank account.               │
│  EduForge does not store your card/UPI details.                            │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Payment Success

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  ✅ PAYMENT SUCCESSFUL                                                       │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │                                                                        │  │
│  │  Amount:     ₹8,500.00                                                │  │
│  │  Paid to:    TopRank JEE Academy, Ameerpet                            │  │
│  │  For:        Monthly coaching fee — April 2026                        │  │
│  │  Method:     UPI (ravi.kumar@ybl)                                     │  │
│  │  Txn ID:     PAY-2026040100847231                                     │  │
│  │  Date:       01-Apr-2026, 09:12 AM IST                                │  │
│  │  UTR:        612345678901                                              │  │
│  │                                                                        │  │
│  │  Receipt sent to: +91 98765-43210 (WhatsApp) & ravi.kumar2007@gmail  │  │
│  │                                                                        │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  [Download Receipt PDF ↓]  [View Fee Statement →]  [Go to Dashboard →]    │
│                                                                              │
│  ── TAX RECEIPT ─────────────────────────────────────────────────────────   │
│  80C tax benefit receipt for education fees:                                │
│  Available for school/college tuition fees paid by parent.                  │
│  [Download 80C Receipt ↓] (shows parent name as payee)                     │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Payment Failure / Retry

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  ⚠️ PAYMENT FAILED                                                          │
│                                                                              │
│  Your payment of ₹8,500 to TopRank JEE Academy could not be processed.    │
│                                                                              │
│  Reason: UPI transaction timed out (bank server did not respond in 60s)    │
│  Txn ID: PAY-2026040100847232 · Status: FAILED                             │
│                                                                              │
│  ⚠️ If money was deducted from your account, it will be automatically      │
│  refunded within 3–5 business days. No action needed.                      │
│                                                                              │
│  [Retry Payment →]  [Try Different Method →]  [Contact Support →]          │
│                                                                              │
│  Common fixes:                                                               │
│  • Switch to a different UPI app (GPay → PhonePe)                          │
│  • Check if your bank's UPI service is down (common with BSNL/SBI)         │
│  • Try debit card or net banking instead                                    │
│  • Ensure sufficient balance (₹8,500 + ₹1 Razorpay verification)          │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|--------|----------|-------------|
| 1 | `POST` | `/api/v1/student/fees/pay/create-order` | Create Razorpay order for fee payment |
| 2 | `POST` | `/api/v1/student/fees/pay/verify` | Verify Razorpay payment signature |
| 3 | `GET` | `/api/v1/student/fees/payments` | Payment history (all institutions + subs) |
| 4 | `GET` | `/api/v1/student/fees/payments/{txn_id}/receipt` | Download payment receipt PDF |
| 5 | `GET` | `/api/v1/student/fees/payments/{txn_id}/80c-receipt` | Download 80C tax receipt PDF |
| 6 | `POST` | `/api/v1/student/fees/pay/refund-check/{txn_id}` | Check refund status for failed payment |

---

## 5. Business Rules

- Payment routing uses Razorpay's Route API (split payment) — when Ravi pays ₹8,500 to TopRank, the payment is processed by Razorpay and split: ₹8,287.50 (97.5%) goes to TopRank's linked bank account and ₹212.50 (2.5%) goes to EduForge's commission account; the student sees only "₹8,500 paid to TopRank" — the commission is invisible to them; settlement to the institution happens within T+2 business days; this model means EduForge never holds institution fees in its own account, reducing regulatory and trust concerns.

- UPI is the dominant payment method (62%) and requires special handling: UPI intent flow (deep-linking to GPay/PhonePe) must work on 78% of students' Android phones (version 8+); the collect request flow (entering UPI ID) is the fallback; UPI transaction timeout is set to 5 minutes (not the default 60 seconds) because bank servers in India frequently experience delays during peak hours; if the transaction is "pending" after 5 minutes, the system polls Razorpay's payment status API every 30 seconds for up to 30 minutes before marking it as failed.

- Auto-refund for failed payments where money was deducted: EduForge's payment webhook detects "payment.failed" events where the bank debited the student's account but Razorpay didn't receive confirmation; the system initiates an automatic refund via Razorpay's refund API; the student sees "Money will be refunded in 3–5 business days" immediately; if the refund doesn't process within 5 days, the support team is auto-notified to investigate; this is critical because many students (especially in Tier-3 towns) panic when ₹8,500 disappears from their account without the fee being marked as paid.

- 80C tax receipt generation: for school and college tuition fees paid by the parent, EduForge generates a receipt formatted for Section 80C income tax deduction; the receipt shows the parent's name as the payee (not the student's), the institution's name, PAN, and the tuition component (excluding lab fees, sports fees, and other non-tuition charges which are not eligible for 80C); the PDF is digitally signed and available for download from the payment history; this feature is highly valued by parents and was specifically requested by institutions as a competitive differentiator.

---

*Last updated: 2026-03-31 · Group 10 — Student Unified Portal · Division E*
