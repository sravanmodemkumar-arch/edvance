# D-20 — Petty Cash Register

> **URL:** `/school/fees/petty-cash/`
> **File:** `d-20-petty-cash.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Roles:** Accountant (S3) — full · Administrative Officer (S3) — entry · Principal (S6) — imprest replenishment

---

## 1. Purpose

Manages the daily small-expense cash fund maintained at the school office — imprest system. Petty cash covers small day-to-day expenses: courier charges, photocopying, minor stationery, plumber emergency call-out, tea for visitors, etc. These are too small to go through the formal vendor payment process (D-19) but must still be documented for audit.

The imprest amount (typically ₹5,000–₹10,000) is maintained at the school office. When it runs low, the Accountant requests replenishment from the Principal.

---

## 2. Page Layout

### 2.1 Header
```
Petty Cash Register — 2026–27               Current Balance: ₹3,240
Imprest Amount: ₹10,000  ·  Last Replenished: 20 Mar 2026 (₹6,800)
```

### 2.2 Petty Cash Book
| Voucher No. | Date | Description | Amount | Balance |
|---|---|---|---|---|
| PC/2026/042 | 26 Mar 2026 | Courier — TC dispatch to Bengaluru | ₹120 | ₹3,240 |
| PC/2026/041 | 25 Mar 2026 | Stationery — Red pen 12 pack | ₹240 | ₹3,360 |
| PC/2026/040 | 24 Mar 2026 | Tea/coffee — PTM parent refreshments | ₹800 | ₹3,600 |
| PC/2026/039 | 22 Mar 2026 | Electrician — emergency light fitting | ₹1,400 | ₹4,400 |
| **Replenishment** | 20 Mar 2026 | Imprest top-up | +₹6,800 | ₹10,000 |

---

## 3. Replenishment

When balance < ₹2,000:
```
Petty Cash Replenishment Request
Current Balance: ₹3,240
Expenses since last top-up: ₹6,800
Replenishment Required: ₹6,800

Supporting vouchers: 12 vouchers (PC/2026/031 to PC/2026/042)

[Approve Replenishment — Principal]  → Cheque / NEFT to Accountant
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/fees/petty-cash/?year={year}` | Petty cash register |
| 2 | `POST` | `/api/v1/school/{id}/fees/petty-cash/` | Add petty cash voucher |
| 3 | `POST` | `/api/v1/school/{id}/fees/petty-cash/replenish/` | Replenishment request |
| 4 | `GET` | `/api/v1/school/{id}/fees/petty-cash/export/?year={year}` | Export petty cash book |

---

## 5. Business Rules

- Single petty cash payment ≤ ₹2,000 (school-configurable limit); larger amounts must go through D-19 Vendor Payments
- Every petty cash voucher must have a supporting document (bill/receipt); if not available (e.g., auto-rickshaw fare), a self-certified note is accepted up to ₹200
- Petty cash book is audited quarterly by the school accountant and annually by the external auditor

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division D*
