# F-05 — Fee Collection at Enrollment

> **URL:** `/coaching/admissions/fee/`
> **File:** `f-05-fee-collection.md`
> **Priority:** P2
> **Roles:** Admissions Counsellor (K3) · Accounts (K5) · Branch Manager (K6)

---

## 1. Fee Structure

```
FEE STRUCTURE — Toppers Coaching Centre (2026–27 Batches)

  COURSE               │ Full Fee    │ GST (18%)  │ Total      │ Installment Plan
  ─────────────────────┼─────────────┼────────────┼────────────┼──────────────────────────────
  SSC CGL (10 months)  │ ₹ 18,000   │ ₹  3,240   │ ₹ 21,240  │ 2 parts: ₹10,620 + ₹10,620
  SSC CHSL (8 months)  │ ₹ 14,000   │ ₹  2,520   │ ₹ 16,520  │ 2 parts: ₹ 8,260 + ₹ 8,260
  Banking PO (10 mo.)  │ ₹ 20,000   │ ₹  3,600   │ ₹ 23,600  │ 2 parts: ₹11,800 + ₹11,800
  Banking Clerk (8 mo.)│ ₹ 16,000   │ ₹  2,880   │ ₹ 18,880  │ 2 parts: ₹ 9,440 + ₹ 9,440
  RRB NTPC (8 months)  │ ₹ 14,000   │ ₹  2,520   │ ₹ 16,520  │ 2 parts: ₹ 8,260 + ₹ 8,260
  Foundation (6 months)│ ₹ 10,000   │ ₹  1,800   │ ₹ 11,800  │ 2 parts: ₹ 5,900 + ₹ 5,900
  ─────────────────────┴─────────────┴────────────┴────────────┴──────────────────────────────

  DISCOUNTS AVAILABLE (applied before GST):
    Early-bird (enroll 60+ days before batch start):  ₹ 1,000 off base fee
    Alumni discount (TCC alumni re-enrolling):         ₹ 500 off
    Referral discount (referred by existing student):  ₹ 500 off
    SC/ST/OBC-NCL (BPL category):                     ₹ 2,000 off (document required)

  Note: Discounts are NOT combinable. Max one discount per enrollment.
```

---

## 2. Payment Collection Form

```
FEE COLLECTION — LEAD-1842: Suresh Babu Rao
Course: SSC CGL 2026–27  |  Counsellor: Ms. Ananya Roy

  BASE FEE:              ₹ 18,000
  DISCOUNT APPLIED:      Early-bird (enroll 60+ days before May batch) — ₹ 1,000 off
  DISCOUNTED FEE:        ₹ 17,000
  GST (18%):             ₹  3,060
  TOTAL PAYABLE:         ₹ 20,060

  INSTALLMENT PLAN:
    Instalment 1 (today):     ₹ 10,030  (50% incl. GST) — DUE NOW
    Instalment 2 (1 Aug):     ₹ 10,030  (50% incl. GST) — due on batch midpoint

  PAYMENT MODE:
    (●) UPI / QR Code    [Scan TCC QR → ₹10,030]
    ( ) Cash             [Print receipt after counting]
    ( ) DD / Cheque      [Payable to "Toppers Coaching Centre Pvt Ltd"]
    ( ) Card (POS)       [Swipe at reception desk — 1.8% convenience fee waived]
    ( ) Net Banking      [NEFT/RTGS — reference: TCC-2026-2501]

  UPI PAYMENT:
    ┌────────────────────────────────────┐
    │         [ QR CODE ]                │
    │  TCC-UPI-MAIN@sbi                  │
    │  Amount: ₹ 10,030                  │
    │  Ref: ENROLL-2026-2501             │
    └────────────────────────────────────┘

  [Payment Received ✅]  |  Amount confirmed: ₹ 10,030 via UPI (10:12 AM)
  Receipt No:  TCC-RCP-2026-0842
  GST Invoice: Auto-generated and sent to suresh.rao@gmail.com ✅
```

---

## 3. Fee Receipt

```
RECEIPT — TCC-RCP-2026-0842
Toppers Coaching Centre Pvt Ltd
GSTIN: 36AABCT1234F1Z8 | SAC: 9992
Date: 30 March 2026

  Student:      Suresh Babu Rao (TCC-2026-2501)
  Course:       SSC CGL 2026–27 Full Batch
  Batch:        SSC CGL Morning, May 2026

  Description              │ Amount
  ─────────────────────────┼──────────────
  Tuition fee (Inst. 1)    │ ₹  8,500.00
  Early-bird discount      │ ₹ (  500.00)  [Note: discount split 50-50 across instalments]
  Taxable value            │ ₹  8,500.00
  GST @ 18% (CGST 9% + SGST 9%) │ ₹  1,530.00
  TOTAL RECEIVED           │ ₹ 10,030.00

  Mode: UPI | UTR: 306140XXXXX | Time: 10:12:34 AM

  Next payment: ₹ 10,030 due on 01 August 2026
  Balance outstanding: ₹ 10,030

  [Download PDF]   [Send to email]   [Send to WhatsApp]
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/fee/structure/` | Fee structure for all courses |
| 2 | `POST` | `/api/v1/coaching/{id}/admissions/enroll/{eid}/payment/` | Record fee payment |
| 3 | `GET` | `/api/v1/coaching/{id}/admissions/enroll/{eid}/receipts/` | All receipts for an enrollment |
| 4 | `GET` | `/api/v1/coaching/{id}/admissions/enroll/{eid}/balance/` | Outstanding balance |
| 5 | `POST` | `/api/v1/coaching/{id}/admissions/enroll/{eid}/discount/` | Apply discount to enrollment |
| 6 | `GET` | `/api/v1/coaching/{id}/fee/collections/?date=2026-03-30` | Day-wise fee collection summary |

---

## 5. Business Rules

- GST at 18% applies to all coaching services following the 2021 GST Council ruling that removed the education exemption for coaching institutes; TCC is registered under SAC 9992 (commercial training and coaching services); the GST component is non-negotiable — a counsellor who offers "GST-free" pricing to convince a student to enrol is creating a GST evasion record; the system enforces GST calculation and cannot issue a receipt without it; all fee waivers or discounts are on the pre-GST base fee only
- Cash payments are accepted but must be entered in the system immediately by the counsellor, verified by the accounts team at the end of day, and deposited to TCC's bank account by the next business morning; a cash-in-hand reconciliation mismatch of more than ₹500 triggers an audit; the counsellor who collected the cash is responsible until the deposit is confirmed; TCC's internal policy does not allow counsellors to hold cash overnight — it must be handed to the accounts desk before 7 PM
- Discounts are pre-approved categories — counsellors cannot offer custom discounts ("I'll give you ₹800 off since you're a good student") without Branch Manager approval; an unauthorised discount is a financial loss to TCC; the system allows only approved discount codes (early-bird, alumni, referral, BPL); a custom discount requires Branch Manager to create a one-time discount code with a justification; this prevents ad-hoc revenue loss and ensures all discounts are tracked and approved
- The instalment schedule is set at enrollment and cannot be changed by the counsellor; if a student requests a modified instalment plan (e.g., 3 instalments instead of 2), it requires Accounts team approval and a modified schedule is generated; the modified plan must still collect the full fee amount within the batch duration; "pay whatever you can, whenever you can" is not an acceptable arrangement — it creates fee collection chaos and revenue uncertainty
- Fee receipts generated by EduForge are GST-compliant B2C invoices (since all students are individuals, not businesses); the GSTIN field shows TCC's GSTIN; no student GSTIN is required for B2C; receipts are archived for 7 years per Income Tax Act record-keeping requirements; even if a student loses their copy, TCC must be able to reproduce the receipt from archives upon request; the accounts team conducts a quarterly audit of fee receipts against the bank statement

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division F*
