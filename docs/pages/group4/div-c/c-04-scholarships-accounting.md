# C-04 — Scholarship Fee Accounting

> **URL:** `/college/fees/scholarships/`
> **File:** `c-04-scholarships-accounting.md`
> **Priority:** P1
> **Roles:** Accounts Officer (S3) · Finance Manager (S4) · Scholarship Coordinator (S3)

---

## 1. Scholarship Accounting Model

```
SCHOLARSHIP FEE ACCOUNTING

TWO MODELS for scholarship fee handling:

Model 1 — Fee Waiver (student pays nothing):
  College issues admission and waives the fee for the scholarship student
  Government later reimburses the college the student's tuition fee
  Example: TS ePASS (government pays tuition fee to college on student's behalf)
  Accounting: Dr. TS ePASS Receivable / Cr. Fee Revenue
  Risk: Government delay (18+ months) — college fronts the money

Model 2 — Student Pays, Scholarship Credited Later (NSP):
  Student pays the fee (or gets a loan)
  Government releases scholarship amount directly to student's bank account (DBT)
  College is not the beneficiary — it's between government and student
  Accounting: No impact on college accounts (student payment = normal)
  Note: NSP Central OBC/SC/ST Post-Matric works this way (DBT to student)

GCEH SCHOLARSHIP ACCOUNTING:
  TS ePASS (Model 1): 185 students → ₹34,50,000 receivable from state
  NSP (Model 2): 142 OBC students → No college impact (DBT to students)
  Merit scholarship (internal): 12 students → ₹3,00,000 fee waiver from college corpus
  AICTE Pragati (girl students): 32 students → ₹16,00,000 (AICTE → college directly)

OUTSTANDING RECEIVABLES:
  TS ePASS (2024–25 balance): ₹9,20,000 (state — overdue 18 months) ← tracked
  AICTE Pragati 2025–26: ₹5,20,000 (pending Q3 release) ← being followed up
```

---

## 2. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/college/{id}/fees/scholarships/receivables/` | Government scholarship receivables |
| 2 | `POST` | `/api/v1/college/{id}/fees/scholarships/waiver/` | Apply fee waiver for scholarship student |
| 3 | `GET` | `/api/v1/college/{id}/fees/scholarships/summary/` | Scholarship accounting summary |

---

## 3. Business Rules

- Fee waivers for scholarship students must be recorded correctly in accounts; the college cannot show a "nil fee" student as paying revenue — it is a receivable from the government; conflating this leads to inaccurate revenue recognition (accounts must follow Ind AS / ICAI standards)
- TS ePASS scholarship amounts are fixed by the government per programme; the college cannot top-up or reduce the scholarship; if the government-approved scholarship amount is less than the AFRC fee, the student pays the difference; if more (unlikely), the excess goes to the student
- AICTE Pragati scholarship: The college must verify girl students' eligibility (annual family income <₹8L, government institution preferred but private AICTE also covered) and submit claims to AICTE on time; late AICTE claims are sometimes rejected

---

*Last updated: 2026-03-27 · Group 4 — College Portal · Division C*
