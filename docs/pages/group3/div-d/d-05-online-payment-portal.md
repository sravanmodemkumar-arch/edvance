# D-05 — Online Payment Portal

> **URL:** `/school/fees/online-payments/`
> **File:** `d-05-online-payment-portal.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Accountant (S3) — full · Principal (S6) — full

---

## 1. Purpose

Manages parent-initiated online fee payments and their reconciliation with EduForge fee ledgers. Parents pay via the parent portal (or a school payment link) using UPI, credit/debit card, net banking, or wallet — powered by the school's configured payment gateway (Razorpay, PhonePe, or PayU — EduForge supports BYOG — Bring Your Own Gateway, per Module 57).

When a parent pays online:
1. Payment gateway processes the transaction
2. Webhook received by EduForge
3. Fee ledger auto-updated
4. Receipt auto-generated and sent to parent via WhatsApp + email

This page shows the Accountant the reconciliation status — all online payments received, auto-matched receipts, and failed/pending transactions needing manual attention.

---

## 2. Page Layout

### 2.1 Header
```
Online Payments — 2026–27                     [Reconcile Pending]  [Export]
Today: 26 Mar 2026  ·  Payments Received: 18  ·  ₹1,42,600
Auto-reconciled: 17 ✅  ·  Pending reconciliation: 1 ⚠️  ·  Failed: 0
Gateway: Razorpay  ·  Balance in gateway: ₹4,28,000  ·  Next settlement: 27 Mar 2026
```

### 2.2 Online Payment Log
| Ref No. | Student | Amount | Mode | Time | Status | Receipt |
|---|---|---|---|---|---|---|
| RPY-2026-98421 | Arjun Sharma | ₹5,350 | UPI | 10:23 AM | ✅ Auto-reconciled | R/2026/7834 |
| RPY-2026-98422 | Priya Venkat | ₹6,500 | Credit Card | 11:04 AM | ✅ Auto-reconciled | R/2026/7835 |
| RPY-2026-98423 | Unknown | ₹7,000 | Net Banking | 2:15 PM | ⚠️ Pending match | [Match Manually] |

---

## 3. Parent Payment Flow (from parent portal)

1. Parent logs into parent portal → Fees tab
2. Sees outstanding fee breakdown (same as D-04 but read-only)
3. Clicks [Pay Now ₹5,350]
4. Redirected to Razorpay checkout (or PayU / PhonePe based on gateway config)
5. Parent completes UPI / card / net banking payment
6. Razorpay webhook fires → EduForge updates fee ledger → receipt generated
7. Parent sees "Payment successful — Receipt R/2026/7834 — WhatsApp sent"

---

## 4. Manual Reconciliation

For the 1 unmatched payment (RPY-2026-98423 — ₹7,000 from unknown):
```
Manual Match Required

Payment Reference: RPY-2026-98423
Amount: ₹7,000
Gateway: Razorpay
Payer Name: RAJESH SHARMA (from bank)
Time: 26 Mar 2026, 2:15 PM

Possible matches:
  ● Rajesh Sharma — Father of Arjun Sharma (XI-A) — Q3 Tuition ₹5,250 outstanding
  ● Rajesh Mehta — Father of Rahul Mehta (IX-B) — Q4 Tuition ₹5,500 outstanding
  ● Manual entry (if neither match)

Note: Amount ₹7,000 doesn't match any standard installment — may be advance payment.

[Match to Arjun Sharma — ₹5,250 + advance ₹1,750]
[Match to custom student]
```

---

## 5. Gateway Settlement Tracking

```
Gateway Settlement Log — Razorpay

Settlement Date   Amount        Transactions  Status
26 Mar 2026       ₹4,28,000     38           ✅ Received in bank
25 Mar 2026       ₹2,86,000     24           ✅ Received
24 Mar 2026       ₹3,12,000     28           ✅ Received
```

Settlement amount matches bank statement → feeds D-18 Bank Reconciliation.

---

## 6. Failed Payment Handling

If a payment fails (bank decline, network timeout):
- Parent sees: "Payment failed — no amount deducted. Please try again."
- EduForge logs the attempt (reference, time, amount, reason) — for support if parent claims money was deducted
- No fee ledger update for failed payments
- Partial capture (rare) → flagged to Accountant for manual resolution

---

## 7. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/fees/online-payments/?date={date}` | Online payment log |
| 2 | `POST` | `/api/v1/school/{id}/fees/online-payments/webhook/razorpay/` | Razorpay webhook (internal) |
| 3 | `POST` | `/api/v1/school/{id}/fees/online-payments/{ref}/match/` | Manual reconciliation |
| 4 | `GET` | `/api/v1/school/{id}/fees/online-payments/settlements/` | Gateway settlement log |
| 5 | `GET` | `/api/v1/school/{id}/fees/online-payments/export/?year={year}` | Export online payment log |

---

## 8. Business Rules

- Payment gateway credentials (Razorpay API key/secret) are stored in school settings (encrypted); the school configures their own gateway (BYOG)
- Webhook endpoint is secured with gateway signature verification — prevents spoofed payments
- Auto-reconciliation matches based on: student mobile number (Razorpay stores payer number) + amount matches one of the student's outstanding installments
- 2% payment gateway fee is borne by the school (not added to student fee) — shows as an expense in D-19 Vendor Payments
- Refunds (rare but possible — e.g., duplicate payment) are processed through the gateway; EduForge marks the receipt as "Refunded" and reduces the student's paid amount

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division D*
