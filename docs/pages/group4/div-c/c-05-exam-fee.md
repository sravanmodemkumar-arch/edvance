# C-05 — Exam Fee Collection & Remittance

> **URL:** `/college/fees/exam/`
> **File:** `c-05-exam-fee.md`
> **Priority:** P1
> **Roles:** Accounts Officer (S3) · Examination Controller (S4) · Finance Manager (S4)

---

## 1. Exam Fee Management

```
EXAM FEE — JNTU Hyderabad (Semester II 2026–27)

EXAM FEE STRUCTURE:
  Regular exam: ₹120/subject (JNTU prescribed)
  Backlog exam: ₹200/subject
  Re-checking (post-result): ₹500/subject
  Personal copy (for revaluation): ₹600/paper (JNTU)
  Convocation fee (final year): ₹1,200 (batch; JNTU collects at convocation)

COLLECTION:
  Collection window: 15–30 March 2027
  Students: 332
  Average subjects: 9 per student
  Estimated collection: 332 × 9 × ₹120 = ₹3,58,560

COLLECTION STATUS:
  Collected: ₹3,52,080 (98.2%)
  Pending: ₹6,480 (6 students × 9 subjects × ₹120)
    Reason: Bank loan pending (3 students), hardship (3 students)
    [Deadline extended by 5 days for pending students]

REMITTANCE TO JNTU:
  Must remit by: 7 April 2027 (JNTU deadline)
  Mode: DD / NEFT to JNTU accounts
  Challan: JNTU online portal upload
  Status: ⬜ Pending (due 7 April)

[Generate JNTU remittance report]  [Submit to accounts for DD preparation]
```

---

## 2. Revaluation / Re-checking

```
REVALUATION — Post-Result Service
(After JNTU releases results)

Students who want revaluation:
  Applies for: Personal copy first (₹600/subject) → receives photostat of answer sheet
  Applies for: Revaluation (₹1,000/subject) after seeing personal copy
  JNTU re-evaluates the paper with a different examiner

  Process:
    Student applies through JNTU portal (JNTU online — not EduForge)
    Fee paid to JNTU directly (JNTU online payment)
    College's role: Facilitate, guide, provide bonafide

EduForge tracking:
  Students who applied for revaluation: [Tracked for internal record]
  Result changes after revaluation: [Updated in results module when JNTU releases]
```

---

## 3. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/college/{id}/fees/exam/collection-status/` | Exam fee collection status |
| 2 | `POST` | `/api/v1/college/{id}/fees/exam/remit/` | Record remittance to university |
| 3 | `GET` | `/api/v1/college/{id}/fees/exam/defaulters/` | Students with pending exam fee |

---

## 4. Business Rules

- Exam fee must be remitted to JNTU within the prescribed deadline; failure to remit results in hall tickets not being generated for students; a single day's delay by the accounts team can affect 300+ students; EduForge sends remittance deadline alerts 7 and 2 days before the due date
- Collecting exam fee above JNTU prescribed amount is prohibited; the college cannot add "processing charges" on top of the JNTU exam fee; the exact JNTU-prescribed amount is what students pay
- Students who cannot pay exam fee (genuine hardship) should be facilitated through the scholarship/welfare fund; denying hall ticket for exam fee default is legally problematic (right to education/examination is a fundamental entitlement)

---

*Last updated: 2026-03-27 · Group 4 — College Portal · Division C*
