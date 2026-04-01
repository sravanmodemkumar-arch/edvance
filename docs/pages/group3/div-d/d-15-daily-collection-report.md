# D-15 — Daily Collection Report

> **URL:** `/school/fees/reports/daily/`
> **File:** `d-15-daily-collection-report.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Fee Clerk (S2) — own shifts · Accountant (S3) — full · Principal (S6) — full

---

## 1. Purpose

Day-end summary of all fee collections. The Accountant reviews this each evening to reconcile cash, verify online collections, and close the day. The Principal uses it for the A-20 fee dashboard.

---

## 2. Report Layout

```
Daily Collection Report — 26 March 2026

Mode             Receipts   Amount
─────────────────────────────────────
Cash                  12    ₹96,400
Cheque                 2    ₹18,000   (pending clearance)
UPI                   18   ₹1,42,600
NEFT/RTGS              6   ₹1,27,200
─────────────────────────────────────
TOTAL                 38   ₹3,84,200

Cash Reconciliation:
  Opening Float:      ₹10,000
  Cash Collected:     ₹96,400
  Total Cash:         ₹1,06,400
  Float Retained:     ₹10,000
  Cash to Deposit:    ₹96,400 ← to be deposited in school bank account today

Class-wise Breakdown:
  Nursery–V:    ₹84,200 (18 receipts)
  VI–VIII:      ₹96,000 (10 receipts)
  IX–X:         ₹82,000 (6 receipts)
  XI–XII:       ₹1,22,000 (4 receipts)

Fee Head Breakdown:
  Tuition (Q3):       ₹2,86,000
  Development:        ₹64,200
  Board Exam:         ₹18,000
  Late Fee:           ₹16,000

Cashier: Meera (Fee Clerk)  ·  Verified By: Ravi (Accountant)  ·  [Mark Day Closed]
```

---

## 3. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/fees/reports/daily/?date={date}` | Daily report for date |
| 2 | `GET` | `/api/v1/school/{id}/fees/reports/daily/export/?date={date}` | Export day report PDF |

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division D*
