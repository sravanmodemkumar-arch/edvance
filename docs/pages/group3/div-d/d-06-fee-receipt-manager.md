# D-06 — Fee Receipt Manager

> **URL:** `/school/fees/receipts/`
> **File:** `d-06-fee-receipt-manager.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Accountant (S3) — full · Fee Clerk (S2) — read own + reprint · Principal (S6) — full (cancel)

---

## 1. Purpose

The master register of all fee receipts — the complete audit trail of every payment received. CBSE inspection and financial audit both check the receipt register. This page enables: searching any receipt by number/student/date, reprinting lost receipts, and cancelling erroneous receipts (with Principal approval).

---

## 2. Page Layout

### 2.1 Header
```
Fee Receipt Register — 2026–27               [Export Register]  [Cancelled Receipts]
Total Receipts: 842  ·  Cancelled: 3  ·  Duplicate (reprints): 12
Total Amount: ₹1,24,28,000
```

### 2.2 Receipt Search
```
Search: [Receipt No. / Student Name / Father Name]
Date Range: [01 Apr 2026] to [31 Mar 2027]
Mode: [All ▼]  ·  Class: [All ▼]
```

### 2.3 Receipt List
| Receipt No. | Student | Class | Date | Amount | Mode | Collected By | Status |
|---|---|---|---|---|---|---|---|
| R/2026/7834 | Arjun Sharma | XI-A | 26 Mar 2026 | ₹5,350 | UPI | Online (auto) | ✅ Active |
| R/2026/7833 | Priya Venkat | XI-A | 26 Mar 2026 | ₹6,500 | Cash | Meera (Clerk) | ✅ Active |
| R/2026/0042 | Rohit Kumar | IX-B | 5 Apr 2026 | ₹8,200 | Cash | Meera (Clerk) | ❌ Cancelled |

---

## 3. Receipt Detail

Clicking a receipt:
```
Receipt R/2026/7834

Student: Arjun Sharma (STU-0001187) | Class XI-A | Roll 15
Date: 26 Mar 2026, 10:23 AM
Mode: UPI (Razorpay RPY-2026-98421)
Collected By: Online (parent self-pay)

Line Items:
  Q3 Tuition (Science XI)   ₹7,000
  Less: Merit Scholarship   -₹1,750 (25%)
  Net Tuition               ₹5,250
  Late Fee                  ₹100
  TOTAL                     ₹5,350

Education service — GST Exempt

[Reprint PDF]  [Send WhatsApp]  [Cancel Receipt (Principal)]
```

---

## 4. Reprint / Duplicate Receipt

[Reprint PDF] → generates PDF marked "DUPLICATE" if already printed once:
- First print: original
- Subsequent prints: "DUPLICATE COPY — Original issued: 26 Mar 2026"
- Reprint logged with reason (parent request / misplaced)

---

## 5. Receipt Cancellation

[Cancel Receipt] → requires Principal role:
```
Cancel Receipt R/2026/0042 — Rohit Kumar — ₹8,200 — 5 Apr 2026

Reason for Cancellation (required): Duplicate receipt — parent paid twice (mistake)
Cancellation Approved By: Principal Ms. Kavitha
Date: 8 Apr 2026

Effect:
  Student fee ledger: ₹8,200 reversed (marked as credit adjustment)
  Original receipt: Marked CANCELLED in register
  Parent refund: Processed via D-05 (gateway refund) OR adjustment in next installment

[Confirm Cancellation]
```

Cancelled receipts remain visible in register with red "CANCELLED" tag — cannot be deleted.

---

## 6. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/fees/receipts/?year={year}` | Receipt register |
| 2 | `GET` | `/api/v1/school/{id}/fees/receipts/{receipt_id}/` | Receipt detail |
| 3 | `GET` | `/api/v1/school/{id}/fees/receipts/{receipt_id}/pdf/` | Receipt PDF (reprint) |
| 4 | `POST` | `/api/v1/school/{id}/fees/receipts/{receipt_id}/cancel/` | Cancel receipt (Principal) |
| 5 | `GET` | `/api/v1/school/{id}/fees/receipts/export/?year={year}` | Export receipt register |

---

## 7. Business Rules

- Receipt numbers are sequential and immutable — gaps are explained by cancelled receipts
- Once a receipt is generated, the underlying data (amount, student, date) is immutable — only cancellation is possible
- 7-year retention: all receipts retained 7 years for financial audit
- Cancelled receipts remain in register permanently (never deleted) — required for audit

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division D*
