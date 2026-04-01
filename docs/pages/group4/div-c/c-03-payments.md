# C-03 — Fee Payment & Gateway

> **URL:** `/college/fees/payments/`
> **File:** `c-03-payments.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Student (S1) — pay own fees · Accounts Officer (S3) — verify payments · Finance Manager (S4)

---

## 1. Payment Methods

```
PAYMENT GATEWAY — GCEH Fee Payment

ONLINE PAYMENT (student self-service):
  UPI: Google Pay, PhonePe, Paytm, BHIM (most common for amounts <₹1L)
  Net Banking: All major banks
  Credit/Debit Card: Visa, Mastercard, RuPay
  Payment Gateway: Razorpay (primary) / PayU (fallback)

OFFLINE PAYMENT:
  RTGS/NEFT: For large amounts (management quota ₹1.4L — most parents pay via NEFT)
    Bank: SBI (College Account — provided on admission letter)
    Account: GCEH Fee Account  |  IFSC: SBIN0XXXXXX
    Unique reference: Student Roll No. as NEFT remarks
  Demand Draft: DD in favour of "Principal, GCEH, payable at Hyderabad"
    (Some management parents still use DD — accepted with verification)
  Cash: Accepted at college cashier for amounts ≤₹10,000

LARGE PAYMENT (>₹1L — management quota full year):
  Preferred: NEFT/RTGS (bank-to-bank, traceable, no gateway charges)
  UPI: Max ₹1L per transaction (NPCI UPI limit) — may need 2 transactions
  Card: ₹1,40,000+ on card → 2% payment gateway surcharge → college may absorb or pass through

GST:
  Education service: Exempt (Notification 12/2017) ✅
  No GST on any fee component ✅
  Payment gateway transaction charges: Not passed to student (college's cost)

RECEIPT:
  Online: Auto-generated receipt PDF; WhatsApp delivery ✅
  NEFT/RTGS: Receipt generated after accounts team verifies bank statement (1–2 business days)
  Offline/DD: Counter receipt issued immediately; system receipt after DD clearance (2–5 days)
```

---

## 2. Payment Flow

```
PAYMENT FLOW — Online (UPI Example):

Student → clicks "Pay ₹78,500" in portal
  → Razorpay modal opens
  → Student selects UPI
  → Enters UPI ID or scans QR
  → Completes payment on phone (UPI app)
  → Razorpay receives payment confirmation
  → Webhook sent to EduForge backend (within 30 seconds)
  → EduForge updates fee ledger (C-02) ✅
  → Receipt generated (PDF) ✅
  → WhatsApp receipt to student + parent ✅
  → Display: "Payment of ₹78,500 received. Thank you."

WEBHOOK FAILURE HANDLING:
  If webhook fails or is delayed (rare):
    Student sees "Payment processing — please wait"
    EduForge polls Razorpay order status every 5 minutes (up to 30 minutes)
    If still unconfirmed at 30 min: Flag for manual reconciliation (Accounts team)
    Student is advised not to re-pay (duplicate payment risk)
    Accounts team reconciles with bank statement within 24 hours
    Student is notified once confirmed

DUPLICATE PAYMENT:
  If student accidentally pays twice: Full refund of the extra payment within 5 working days
  (UGC/AICTE — refund policy: same mode, within 5 days)
```

---

## 3. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `POST` | `/api/v1/college/{id}/fees/payments/initiate/` | Create payment order |
| 2 | `POST` | `/api/v1/college/{id}/fees/payments/webhook/` | Payment gateway webhook |
| 3 | `POST` | `/api/v1/college/{id}/fees/payments/manual/` | Record offline payment (NEFT/DD/cash) |
| 4 | `GET` | `/api/v1/college/{id}/fees/payments/receipt/{receipt_id}/pdf/` | Download receipt |

---

## 4. Business Rules

- TDS on payment gateway charges: If Razorpay (or any PG) charges are above ₹30,000/year (likely for a college), TDS Sec 194J (professional fees) or Sec 194C (contract) applies; Accounts team must compute and deduct applicable TDS from PG payments
- PCI DSS compliance: Card data is never stored by EduForge; all card processing is done by Razorpay's PCI-compliant vault; EduForge only stores transaction references
- Receipt under IT Act Sec 5: Digital receipts are valid legal evidence; for dispute purposes (student claims they paid; college denies), the Razorpay transaction ID + webhook receipt is the evidence; physical receipt books are not required for online payments

---

*Last updated: 2026-03-27 · Group 4 — College Portal · Division C*
