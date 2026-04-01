# D-07 — Student Fee Ledger

> **URL:** `/school/fees/students/{student_id}/ledger/`
> **File:** `d-07-student-fee-ledger.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Fee Clerk (S2) — read · Accountant (S3) — full · Principal (S6) — full

---

## 1. Purpose

The complete fee account for a single student — all charges, payments, discounts, late fees, and balance. This is the primary reference for: parents asking about their fee status, the Accountant doing collections, and the CBSE/FRA auditor checking fee records. Every fee event (charge, payment, concession, waiver, late fee, refund) is a line item in this ledger.

---

## 2. Page Layout

```
Arjun Sharma (STU-0001187) — Class XI-A — 2026–27
Father: Rajesh Sharma · 9876543210

Fee Summary:
Annual Charges:    ₹1,04,200
Concessions:      -₹21,000  (Merit 25% tuition)
Net Annual Due:    ₹83,200
Total Paid:        ₹62,400  (Q1 + Q2 + Q3)
Outstanding:       ₹20,800  (Q4 Jan 2027)
Late Fee:         ₹0
Status:            ✅ Current (Q4 due Jan 1 2027)

[Collect Fee]  [Add Concession]  [View Receipts]  [Print Statement]
```

---

## 3. Detailed Ledger

```
Date        Description                         Charge     Credit     Balance
──────────────────────────────────────────────────────────────────────────────
01 Apr 2026  Q1 Charges:
              Tuition (Science XI)               ₹7,000
              Development Fee                    ₹8,000
              Lab Fee                            ₹1,500
              Computer Lab                       ₹1,000
              Exam Fee                           ₹500
              Library Fee                        ₹500
              Sports Fee                         ₹800
              ─────────────────────────────────────────
              Total Q1 Charges                  ₹19,300                ₹19,300

01 Apr 2026  Merit Scholarship (25% Tuition)                -₹1,750   ₹17,550

05 Apr 2026  Q1 Payment — Cash — R/2026/0042               ₹17,550       ₹0

01 Jul 2026  Q2 Charges:
              Tuition (Science XI)               ₹7,000
              Annual Day Fee                     ₹1,200
              Board Exam Fee                     ₹1,500
              Merit Scholarship (25% Tuition)               -₹1,750
              ─────────────────────────────────────────
              Net Q2                             ₹7,950                ₹7,950

08 Jul 2026  Q2 Payment — UPI — R/2026/1824                ₹7,950        ₹0

01 Oct 2026  Q3 Tuition                          ₹7,000                ₹7,000
01 Oct 2026  Merit Scholarship (25%)                       -₹1,750    ₹5,250
16 Oct 2026  Late Fee (15 days grace expired)    ₹100                  ₹5,350
26 Mar 2026  Q3 Payment — UPI — R/2026/7834                ₹5,350        ₹0

01 Jan 2027  Q4 Tuition                          ₹7,000                ₹7,000
01 Jan 2027  Merit Scholarship (25%)                       -₹1,750    ₹5,250
                                                ═══════════════════════════════
Current Balance:                                                       ₹5,250
(Q4 due; no late fee yet — within grace period)
```

---

## 4. Annual Statement

[Print Statement] → A4 PDF statement for the full year:
- Used by parents for income tax benefit (Section 80C deduction on tuition)
- Used for scholarship applications requiring proof of fee paid
- Used in CBSE/FRA audits

---

## 5. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/fees/students/{student_id}/ledger/?year={year}` | Full ledger |
| 2 | `GET` | `/api/v1/school/{id}/fees/students/{student_id}/outstanding/?year={year}` | Current outstanding + late fee |
| 3 | `GET` | `/api/v1/school/{id}/fees/students/{student_id}/statement/?year={year}` | Annual fee statement PDF |

---

## 6. Business Rules

- Ledger is immutable — all entries are append-only; corrections are done via reversal entries (credit lines), never by modifying existing lines
- Security deposit is shown as a separate ledger (not mixed with fee ledger) — to make refund tracking clear
- When a student is promoted to next class (C-10), the new year's fee ledger is initialised automatically in April

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division D*
