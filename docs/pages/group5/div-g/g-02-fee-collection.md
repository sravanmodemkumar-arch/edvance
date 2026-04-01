# G-02 — Daily Fee Collection & Receipts

> **URL:** `/coaching/finance/collections/`
> **File:** `g-02-fee-collection.md`
> **Priority:** P1
> **Roles:** Accounts (K5) · Branch Manager (K6) · Receptionist (K1 — limited)

---

## 1. Today's Collection Summary

```
DAILY FEE COLLECTION — 30 March 2026
Toppers Coaching Centre, Hyderabad Main

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  TODAY'S COLLECTION:  ₹ 86,420   │  Transactions: 28   │ Time: 11:42 AM │
  └──────────────────────────────────────────────────────────────────────────┘

  BY PAYMENT MODE:
    UPI / QR Code:      ₹ 54,030  (16 transactions — 62.5%)
    Cash:               ₹ 18,000   (8 transactions — 28.6%)
    Card (POS):         ₹ 10,590   (3 transactions — 10.7%)
    Cheque/DD:          ₹  3,800   (1 transaction — 3.6%) — Axis Bank DD
    ─────────────────────────────────────────────────────
    TOTAL:              ₹ 86,420  (28 transactions)

  COLLECTION TYPE:
    New enrollment (Inst. 1):   ₹ 42,120  (4 students)
    Instalment payment:         ₹ 38,300  (22 students)
    Test series package:        ₹  6,000   (2 students)

  CASH-IN-HAND RECONCILIATION:
    Opening balance:   ₹  2,000
    Cash collected:    ₹ 18,000
    Cash expenses:     ₹    0
    Expected closing:  ₹ 20,000
    Actual counted:    ₹ 20,000 ✅ Matched
    Bank deposit due:  ₹ 18,000 (before 7 PM today)
```

---

## 2. Transaction Log

```
TRANSACTION LOG — 30 March 2026 (sorted by time)

  Time     │ Receipt No.       │ Student            │ Type            │ Mode  │ Amount
  ─────────┼───────────────────┼────────────────────┼─────────────────┼───────┼────────────
  09:12 AM │ TCC-RCP-2026-0834 │ Lakshmi T. (2409)  │ Installment 2   │ UPI   │ ₹  8,260
  09:28 AM │ TCC-RCP-2026-0835 │ Kiran S.   (2421)  │ Installment 2   │ Cash  │ ₹  9,000
  09:44 AM │ TCC-RCP-2026-0836 │ Ravi Singh (2403)  │ Installment 2   │ UPI   │ ₹  9,000
  10:05 AM │ TCC-RCP-2026-0837 │ Meena K.   (2499)  │ New enroll I1   │ UPI   │ ₹ 10,620
  10:12 AM │ TCC-RCP-2026-0838 │ Arun Kumar (2498)  │ New enroll I1   │ UPI   │ ₹ 11,800
  10:28 AM │ TCC-RCP-2026-0839 │ Priya K.   (2402)  │ Test pkg (CGL)  │ Card  │ ₹  1,768
  10:44 AM │ TCC-RCP-2026-0840 │ Deepak R.  (2488)  │ Installment 2   │ DD    │ ₹  3,800
  10:55 AM │ TCC-RCP-2026-0841 │ Anitha K.  (2408)  │ Installment 2   │ UPI   │ ₹  8,000
  ...  (20 more transactions)

  [Search by student] [Filter by mode] [Export CSV] [Download Day Report]
```

---

## 3. Issue Receipt

```
ISSUE RECEIPT — Manual / On-counter

  Student ID:     [TCC-2403      ] ← Lookup → Ravi Singh (SSC CGL Morning) ✅
  Payment for:    [Installment 2 ▼]   Balance before: ₹ 9,000
  Amount (₹):     [9,000         ]
  Mode:           (●) UPI   ( ) Cash   ( ) Card   ( ) DD/Cheque
  UPI UTR:        [306140YYYYY   ]   Date/time: 30 Mar 09:44 ✅ Confirmed

  GST CALCULATION:
    Taxable value:   ₹ 7,627.12  (₹9,000 ÷ 1.18)
    GST (18%):       ₹ 1,372.88
    Total received:  ₹ 9,000.00

  [Issue Receipt]  →  TCC-RCP-2026-0836 generated ✅
  Receipt delivery: (●) WhatsApp  (●) Email  ( ) Print only

  Balance after:  ₹ 0  (course fee fully paid ✅)
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/finance/collections/?date=2026-03-30` | Daily collection summary |
| 2 | `GET` | `/api/v1/coaching/{id}/finance/collections/transactions/?date=2026-03-30` | Transaction log for a day |
| 3 | `POST` | `/api/v1/coaching/{id}/finance/collections/receipt/` | Issue a fee receipt |
| 4 | `GET` | `/api/v1/coaching/{id}/finance/collections/receipt/{rid}/` | Retrieve receipt (PDF) |
| 5 | `GET` | `/api/v1/coaching/{id}/finance/collections/cash-reconcile/?date=2026-03-30` | Cash reconciliation for a day |
| 6 | `POST` | `/api/v1/coaching/{id}/finance/collections/bank-deposit/` | Log daily bank deposit |

---

## 5. Business Rules

- All fee transactions must be entered in the system at the time of collection; delayed entry (entering yesterday's cash collections today) is a red flag for misappropriation; the system timestamps every receipt at creation; the accounts team performs an end-of-day reconciliation where every cash receipt must match a physical cash note count; a discrepancy of more than ₹500 triggers an audit; receipts created outside working hours (10 PM–5 AM) are flagged for investigation
- Digital payments (UPI, card) are preferred and auto-reconciled; the UPI transaction UTR number is recorded with the receipt; at month-end, TCC's bank statement is reconciled against all UPI receipt UTRs; a receipt without a valid UTR is treated as unverified and flagged; card payments (POS) are reconciled against the POS settlement report; the convenience fee for card (1.8%) is waived by TCC as a policy — the POS cost is absorbed into operating expenses
- Cash deposit to the bank must happen by 7 PM on the same business day; if a business day ends with more than ₹5,000 in cash, it must be deposited; under-the-counter cash holding (keeping cash at the branch overnight) is a theft and audit risk; the Accounts team member who handles the deposit signs the deposit slip and logs the UTR in the system; the Branch Manager reviews the bank deposit log every Friday to confirm daily deposits were made
- Receipts once issued cannot be modified; if an error is made (wrong amount, wrong student), a credit note is issued against the original receipt and a new correct receipt is issued; the credit note and original receipt remain in the system together; a pattern of many credit notes from a specific accounts staff member is investigated; receipt cancellation without a corresponding credit note is blocked by the system — the audit trail cannot have gaps
- GST on fee receipts is calculated as the GST-inclusive amount divided back to arrive at the taxable value (reverse calculation); a student who pays ₹9,000 as an instalment has a taxable value of ₹7,627.12 and GST of ₹1,372.88; the GST invoice for this instalment shows these values; TCC's GSTIN appears on every invoice; the cumulative GST collected monthly is filed in GSTR-1 by the 11th of the following month; the Accounts team runs a GST collection report (G-07) monthly before filing

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division G*
