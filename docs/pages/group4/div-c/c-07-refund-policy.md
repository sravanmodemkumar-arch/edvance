# C-07 — Refund Policy & Processing

> **URL:** `/college/fees/refunds/`
> **File:** `c-07-refund-policy.md`
> **Priority:** P1
> **Roles:** Accounts Officer (S3) · Finance Manager (S4) · Principal/Director (S6) — approve refund

---

## 1. AICTE Refund Policy

```
AICTE REFUND POLICY (2016 Circular — mandatory for all AICTE colleges)

IF STUDENT WITHDRAWS:
  Before 31 July (before academic year start):  100% refund of tuition fee
  From 1 August to 31 August:                    80% refund
  From 1 September to 30 September:              50% refund
  From 1 October to 30 November:                 0% refund (no refund)
  After 30 November:                             0%

  Development fee: Fully refundable before academic year start; non-refundable after
  Caution deposit: Fully refundable anytime (within 30 days of TC)

SPECIAL CASES:
  Medical ground withdrawal (doctor-certified serious illness):
    May apply to AICTE for special refund consideration
  NRI quota student: No refund after reporting (AICTE circular NRI seats)
  Government seat (convener quota): TGCHE refund policy applies (state-specific)

REFUND TIMELINE (after application):
  Approved refunds must be processed within 5 working days (AICTE circular)
  Mode: Same as original payment (UPI refund / NEFT to student's bank)
  TDS on refund: No TDS (it's a fee refund, not income)
```

---

## 2. Refund Application

```
REFUND APPLICATION — Mr. Arjun T. (226J1A0503)
Application date: 30 March 2027
Reason: Transferred to NIT Warangal (JEE Advanced seat)

Fee paid (Semester 1):  ₹78,500 (10 August 2026)
Fee paid (Semester 2):  ₹78,500 (10 January 2027)
Caution deposit:         ₹5,000

REFUND CALCULATION:
  Withdrawal date: 30 March 2027 (after Semester I complete — mid-Semester II)
  AICTE policy: Semester II begins January 2027; withdrawal in March (>90 days in semester)
  → 0% refund on Semester II tuition ✗

  But: Arjun is in Semester II still; actually the policy applies to the YEAR, not semester
  AICTE 2016: After 30 November = 0% for that academic year
  → Semester II fee (₹78,500): 0% refund ✗
  → Caution deposit (₹5,000): 100% refundable ✅

  NET REFUND: ₹5,000 (caution deposit only)

STATUS: Principal approved ✅ | Processing by Accounts | Payment within 5 working days

UNIVERSITY EXAM FEE (₹1,080 for Semester II exams):
  Application submitted before exam: Partial refund from JNTU possible (JNTU process)
  EduForge: Tracks and follows up with JNTU
```

---

## 3. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `POST` | `/api/v1/college/{id}/fees/refund/apply/` | Student refund application |
| 2 | `GET` | `/api/v1/college/{id}/fees/refund/{refund_id}/` | Refund status |
| 3 | `POST` | `/api/v1/college/{id}/fees/refund/{refund_id}/approve/` | Approve and process refund |

---

## 4. Business Rules

- AICTE refund policy dates are absolute; a college that violates these (e.g., refuses refund when student withdraws before 31 July) is exposed to consumer forum complaints under Consumer Protection Act 2019; National Consumer Disputes Redressal Commission (NCDRC) has consistently ruled in favour of students on fee refund matters
- The 5-day processing timeline is mandatory; delays must be justified in writing; a student who has to wait months for a refund can file a consumer complaint which attracts interest on the delayed refund
- Capitation fee (illegal one-time payment) is never refundable because it should never have been collected; however, in practice, students who paid illegal capitation and then withdrew have successfully recovered it through consumer forums by proving they were coerced; EduForge's prohibition on capitation collection protects the college from this exposure

---

*Last updated: 2026-03-27 · Group 4 — College Portal · Division C*
