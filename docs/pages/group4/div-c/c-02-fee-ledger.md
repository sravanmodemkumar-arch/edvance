# C-02 — Student Fee Ledger

> **URL:** `/college/fees/ledger/`
> **File:** `c-02-fee-ledger.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Accounts Officer (S3) · Finance Manager (S4) · Student (S1) — own ledger

---

## 1. Student Fee Account

```
FEE LEDGER — Aakash Sharma (226J1A0541)
Programme: B.Tech CSE | Quota: Management | Year: I (2026–27)

ANNUAL FEE DEMAND:
  Semester 1 (Aug 2026): ₹78,500 (50% of ₹1,57,000)
  Semester 2 (Jan 2027): ₹78,500
  Total Annual: ₹1,57,000 + ₹5,000 Caution Deposit (first year) = ₹1,62,000

PAYMENT HISTORY:
  Date          Amount     Mode   Receipt         Purpose
  10 Aug 2026   ₹78,500    UPI    RCP-2026-0041   Semester 1 fee (full)
  10 Jan 2027   ₹78,500    NEFT   RCP-2027-0041   Semester 2 fee (full)
  ──────────────────────────────────────────────────────────
  Total paid:   ₹1,57,000  (excluding caution deposit ₹5,000 paid at admission)
  Outstanding:  ₹0 ✅

SCHOLARSHIP ADJUSTMENT:
  No scholarship (Aakash is management quota — income ₹4.2L, above threshold)

CAUTION DEPOSIT:
  Paid: ₹5,000 (admission, 10 Aug 2026)
  Refundable on graduation / TC (after clearance of all dues)

LOAN DISBURSEMENT (if student has bank loan):
  SBI Scholar Loan — disbursement to college:
  Aug 2026: ₹78,500 (Semester 1) — directly from SBI to college account ✅
  Aakash's personal liability: ₹0 this semester (loan covers full fee) ✅
```

---

## 2. Accounts Officer View — Outstanding Summary

```
FEE OUTSTANDING — B.Tech 2026–27 (As of March 2027)

Total fee billed (all students, Year I):
  332 students × ₹1,57,000 = ₹5,21,24,000 (Year I annual, both quotas blended avg)

Fee collected:    ₹4,98,60,000 (95.7%)
Outstanding:      ₹22,64,000 (4.3%) — 18 students

OUTSTANDING BY REASON:
  Bank loan pending disbursement: 8 students (₹12,40,000) — expected within 30 days
  Scholarship fee waiver pending: 3 students (₹3,60,000) — TS ePASS pending
  Hardship / payment plan: 5 students (₹4,60,000) — approved payment plan active
  No response / defaulter: 2 students (₹2,04,000) — FINAL NOTICE issued

[View defaulter detail]  [Issue reminder]  [Suspend services for defaulters]

NOTE: "Suspend services" for fee defaulters:
  Allowed: Block non-essential services (library, hostel services)
  Not allowed: Deny attendance registration, deny university exam registration
  (A college that refuses to register a student for exams due to fee default
   is acting improperly — the student has a right to appear for exams;
   fee recovery is a separate civil matter)
```

---

## 3. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/college/{id}/fees/ledger/{student_id}/` | Student fee ledger |
| 2 | `GET` | `/api/v1/college/{id}/fees/outstanding/` | All outstanding fee summary |
| 3 | `GET` | `/api/v1/college/{id}/fees/outstanding/?reason=bank-loan` | Filtered outstanding |
| 4 | `POST` | `/api/v1/college/{id}/fees/payment-plan/` | Create payment plan for student |

---

## 4. Business Rules

- A college cannot deny university exam hall ticket to a student solely for fee default (Madras HC, Delhi HC — multiple precedents); fee recovery is a civil matter; denying education/exam access is a fundamental rights issue; the college can pursue recovery through other means (legal notice, court, withholding degree certificate after graduation)
- Scholarship fee reimbursement (TS ePASS, NSP) pending from government is NOT a student's fault; the student is treated as paid-up for purpose of exams and services while the government reimbursement is pending; the college accounts team tracks this as a government receivable
- Bank loan disbursements are between bank and college; the student should not be held liable for bank processing delays; a "pending bank loan disbursement" is treated as an expected payment, not a default

---

*Last updated: 2026-03-27 · Group 4 — College Portal · Division C*
