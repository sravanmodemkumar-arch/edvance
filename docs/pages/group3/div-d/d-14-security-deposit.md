# D-14 — Security Deposit Register

> **URL:** `/school/fees/security-deposit/`
> **File:** `d-14-security-deposit.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Roles:** Accountant (S3) — full · Administrative Officer (S3) — read · Principal (S6) — full

---

## 1. Purpose

Tracks refundable security deposits collected at admission. Many Indian schools collect a security deposit (₹5,000–₹25,000) at admission — refundable when the student graduates or leaves (subject to any deductions for damages, library books not returned, etc.). This is separate from the fee structure (D-01) because:
- It is a liability (school owes it back to parents), not income
- It must be tracked individually per student for accurate refund processing
- State FRAs regulate security deposits (some states cap at 3 months' tuition; some require interest payment on deposit held > 3 years)

---

## 2. Page Layout

### 2.1 Header
```
Security Deposit Register                    [Export Register]
Total Deposits Held: ₹42,50,000 (380 students × average ₹11,184)
Refunds Due This Year (withdrawals): ₹2,80,000 (Class XII graduates + exits)
```

### 2.2 Deposit Register
| Student | Class | Deposit Collected | Year | Deductions | Refundable | Status |
|---|---|---|---|---|---|---|
| Arjun Sharma | XI-A | ₹15,000 | 2015 (Class VI) | ₹0 | ₹15,000 | Active — refund on exit |
| Priya Das | — | ₹10,000 | 2021 (Class V) | ₹500 (library) | ₹9,500 | ⏳ Refund pending (withdrew Mar 2026) |

---

## 3. Refund Processing

When a student exits (C-12 Withdrawal or C-10 Graduation):
```
Security Deposit Refund — Priya Das (Withdrew 20 Mar 2026)

Deposit Held: ₹10,000 (collected Apr 2021)
Deductions:
  Library books not returned: ₹500 (2 books × ₹250 each)
  ─────────────────────────────────────────────
Net Refund Due: ₹9,500

Refund Mode: NEFT to father's account (Rajesh Das — SBI XXXXXX4521)
Processed By: Accountant Ravi
Date: 26 Mar 2026
NEFT Reference: SBIN262026XXXXX
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/fees/security-deposit/?year={year}` | Deposit register |
| 2 | `PATCH` | `/api/v1/school/{id}/fees/security-deposit/{deposit_id}/refund/` | Process refund |
| 3 | `GET` | `/api/v1/school/{id}/fees/security-deposit/export/` | Export register |

---

## 5. Business Rules

- Security deposit is a balance sheet liability — shown separately from fee revenue in D-16 and D-17
- Security deposit refunds are processed only after all fee dues are cleared (any outstanding fee is deducted from the deposit first, with parent consent)
- FRA states may require interest on deposits held > 3 years — system flags these deposits and computes the statutory interest based on state-configured rate

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division D*
