# N-04 — Fee Statement & Payment (Parent View)

> **URL:** `/parent/fees/`
> **File:** `n-04-fee-payment.md`
> **Template:** `parent_portal.html`
> **Priority:** P1
> **Roles:** Parent/Guardian (S1-P)

---

## 1. Purpose

Parents view their child's fee statement, outstanding dues, payment history, and pay online directly through the portal. This is the most transactional feature — every fee payment goes through here (or at the school cashier desk with a receipt that reconciles to this view).

Integration: Reads from D-01 (Fee Ledger) and D-02 (Fee Schedule); payment gateway calls write back to D-01.

---

## 2. Fee Statement

```
FEE STATEMENT — Rahul Rao (Class X-A)
Academic Year: 2025–26

FEE SCHEDULE (per D-02):
  Component          Annual     Term 1     Term 2     Term 3
  Tuition Fee        ₹42,000    ₹14,000    ₹14,000    ₹14,000
  Transport Fee       ₹7,200     ₹2,400     ₹2,400     ₹2,400
  Activity Fee        ₹2,400       ₹800       ₹800       ₹800
  Exam Fee            ₹1,200         —       ₹600       ₹600
  ──────────────────────────────────────────────────────────
  TOTAL              ₹52,800    ₹17,200    ₹17,800    ₹17,800

PAYMENT STATUS:
  Term 1: ₹17,200 — PAID (15 Apr 2025) ✅ [Receipt #RCP-2025-0412]
  Term 2: ₹17,800 — PAID (1 Oct 2025) ✅ [Receipt #RCP-2025-1234]
  Term 3: ₹17,800 — PENDING 🔴

  Last payment: ₹42,000 on 20 Mar 2026 (receipt #RCP-2026-1842)
    — Note: This payment was for a previous outstanding amount + advance.
    — Application: Term 3 remaining (₹8,400) + Term 3 complete (₹17,800) = error display

OUTSTANDING:
  Term 3 balance due: ₹8,400 (due by 31 March 2026 — 4 days remaining)

[Pay ₹8,400 Now]  [Pay custom amount]  [View receipt history]
```

---

## 3. Payment Gateway Flow

```
PAYMENT — ₹8,400 due (Term 3 balance)

Step 1: Amount confirmation
  Payment for: Rahul Rao (Class X-A)
  Amount: ₹8,400
  Due date: 31 March 2026
  Fee components included:
    Tuition (Term 3 balance): ₹6,400
    Activity (Term 3 balance): ₹800
    Exam fee (Term 3): ₹600
    Transport (Term 3 balance): ₹600

Step 2: Payment method
  ○ UPI (Google Pay, PhonePe, Paytm, any UPI app)
  ○ Net Banking (all major banks)
  ○ Credit / Debit Card (Visa, Mastercard, RuPay)
  ○ Pay at school cashier (generate challan for offline payment)

Step 3: UPI payment flow (most common):
  UPI ID: school@paysb (dynamically generated per transaction)
  QR Code: [QR displayed — scan to pay]
  Amount: ₹8,400.00
  Reference: TXN-2026-RAHUL-T3BAL

  After payment:
    ✅ Payment confirmed
    Receipt #RCP-2026-2104 generated
    WhatsApp receipt sent to registered mobile ✅
    Fee ledger updated in D-01 ✅

GST:
  School fees are exempt from GST (Notification 12/2017 — educational services)
  No GST applicable on this payment ✅

PAYMENT RECEIPT CONTENT:
  School name + affiliation number
  Student name, class, roll number
  Fee components + amounts
  Total paid, date, transaction ID
  Cashier signature (offline) / Digital signature (online)
  "Valid receipt — no signature required for online payments (Sec 5, IT Act 2000)"
```

---

## 4. Payment History

```
PAYMENT HISTORY — Rahul Rao (2025–26)

  Date        Amount    Mode    Receipt            Purpose
  15 Apr 2025 ₹17,200   UPI     RCP-2025-0412      Term 1 (full)
  1 Oct 2025  ₹17,800   Net     RCP-2025-1234      Term 2 (full)
  20 Mar 2026 ₹42,000   Card    RCP-2026-1842      Term 3 (balance) + advance
  ────────────────────────────────────────────────────────
  Total paid: ₹77,000  |  Annual total: ₹52,800  |  Balance: ₹0 ✅

[Download all receipts (ZIP)]  [Download fee certificate for tax purposes]

FEE CERTIFICATE (Section 80C — Income Tax):
  For parents who need a fee payment certificate for IT proof:
  Certificate confirms: Annual tuition fee paid (₹42,000) for Rahul Rao, Class X-A
  Financial year: 2025–26 (AY 2026–27)
  [Download fee certificate PDF]
  Note: Tuition fee (not transport, activity) is eligible under Sec 80C(2)(xv).
```

---

## 5. Concession / Sibling Discount View

```
FEE CONCESSION (if applicable)

Rahul Rao: No concession applicable (full-fee student)

If sibling discount applied:
  Sibling: Ms. Priya Rao (Class VII-C) — second child
  Sibling discount: 10% on tuition fee
  Rahul (first child): Full fee
  Priya (second child): 10% discount on tuition → ₹42,000 × 10% = ₹4,200 saved

If EWS concession (RTE Sec 12(1)(c)):
  Fee: ₹0 (full waiver)
  Transport: ₹0 (if RTE transport benefit applicable)
  Note: RTE students are not shown the fee structure (to preserve dignity)
```

---

## 6. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/parent/{parent_id}/child/{student_id}/fees/statement/` | Annual fee statement |
| 2 | `GET` | `/api/v1/parent/{parent_id}/child/{student_id}/fees/outstanding/` | Current outstanding amount |
| 3 | `POST` | `/api/v1/parent/{parent_id}/child/{student_id}/fees/payment/initiate/` | Initiate payment session |
| 4 | `POST` | `/api/v1/parent/{parent_id}/child/{student_id}/fees/payment/confirm/` | Confirm payment (webhook from PG) |
| 5 | `GET` | `/api/v1/parent/{parent_id}/child/{student_id}/fees/receipts/` | Payment history + receipts |
| 6 | `GET` | `/api/v1/parent/{parent_id}/child/{student_id}/fees/receipts/{receipt_id}/pdf/` | Download receipt PDF |
| 7 | `GET` | `/api/v1/parent/{parent_id}/child/{student_id}/fees/certificate/` | Fee certificate (income tax) |

---

## 7. Business Rules

- Online payment confirmation is via webhook from the payment gateway (Razorpay/PayU/Cashfree); the parent portal shows "Payment Processing" until the webhook confirms; if the webhook is delayed or fails, the parent sees a "Pending confirmation" status and the school's Accounts team verifies manually within 24 hours
- A parent cannot pay less than the outstanding amount for a specific fee component; partial payment of a component creates accounting complexity; the portal enforces full-component payment or allows an advance payment that is credited to the next due amount
- Fee receipts are generated as official school documents (school name, affiliation number, Principal's digital signature); they are valid for income tax Section 80C purposes; parents should be aware that only tuition fees are 80C-eligible (not transport, activity, exam fees)
- For EWS/RTE students, the fee module is either zero-balance (shows ₹0 due) or hidden; the parent does not see the fee structure applied to other students; this protects the dignity of RTE beneficiaries in a mixed-fee school
- Payment gateway integration must use TLS 1.2+ (PCI DSS); card data is never stored by EduForge — the payment gateway handles tokenization; EduForge only stores the transaction reference and status

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division N*
