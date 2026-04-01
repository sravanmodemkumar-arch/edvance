# A-08 — Scholarship & Student Loan

> **URL:** `/college/students/scholarship/`
> **File:** `a-08-scholarship-loan.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Scholarship Coordinator (S3) · Registrar (S4) · Accounts Officer (S3) · Student (S1) — own applications

---

## 1. Purpose

College students access multiple scholarship schemes and educational loans. This module manages:
- NSP (National Scholarship Portal) — Central schemes (OBC Pre/Post-Matric, ST/SC Scholarships, EBC scholarships)
- State government scholarships (TS ePASS — Telangana Post-Matric Scholarships)
- Prime Minister's Scholarship Scheme (PMSS) for central paramilitary/ex-servicemen wards
- AICTE scholarships (Pragati for girl students; Saksham for PwD)
- Institution-specific merit scholarships
- Educational loans (Vidyalakshmi portal; bank-specific schemes)
- Bonafide and fee certificates for loan applications

---

## 2. NSP Scholarship Application Tracking

```
NSP SCHOLARSHIP TRACKER — GCEH
Academic Year: 2026–27
Scholarship Coordinator: Ms. Jyothi P.

ELIGIBLE STUDENTS (by category and scheme):
  Scheme                        Category  Eligible  Applied  Verified  Approved
  NSP Central OBC Post-Matric   OBC-NCL   142       138       130       128
  NSP Central SC Post-Matric    SC         54        52        50        48
  NSP Central ST Post-Matric    ST         23        21        19        18
  NSP EBC (Economically Backward) General  16        14        12        11
  NSP Minority (Muslim/Christian) Minority  8         8         7         6
  AICTE Pragati (Girl students)  All        38        35        33        32
  AICTE Saksham (PwD)            PwD        5         5         5         4
  TS ePASS (State)               OBC+SC+ST 219       210       198       185
  ──────────────────────────────────────────────────────────────────────────
  TOTAL                                    505       483       454       432

AMOUNT EXPECTED (NSP approved):
  Central OBC Post-Matric: ₹10,000/year × 128 students = ₹12,80,000
  Central SC: ₹10,000/year × 48 = ₹4,80,000
  TS ePASS: ₹15,000–₹25,000/year × 185 (varies by course) = ₹34,50,000 (estimated)
  AICTE Pragati: ₹50,000/year × 32 = ₹16,00,000

SCHOLARSHIP AMOUNTS NOT RECEIVED (pending government release):
  TS ePASS (previous year Q3–Q4): ₹9,20,000 outstanding ← tracked as receivable
  This is the same government delay pattern as RTE reimbursement in schools.
```

---

## 3. Individual Scholarship Application

```
SCHOLARSHIP APPLICATION — Aakash Sharma (226J1A0541)
Academic Year: 2026–27

APPLICABLE SCHEMES:
  ● NSP Central OBC Post-Matric Scholarship
    Category: OBC-NCL  |  Income: ₹4,20,000 < ₹2.5L threshold? ← No (income >₹2.5L)
    NOTE: NSP OBC Post-Matric Central has income limit ₹2.5L for most central schemes
    Aakash's income: ₹4,20,000 → NOT eligible for Central OBC Post-Matric ✗

  ● TS ePASS (State — Telangana):
    Income limit: ₹2.5L (OBC) — Aakash: ₹4.2L → NOT eligible for TS ePASS ✗

  ● AICTE Pragati (Girls only) — N/A (male student) ✗

  ● Institution merit scholarship (GCEH):
    Criteria: CGPA ≥ 8.0 after Semester II
    Aakash CGPA: 7.76 (just below 8.0 threshold) → NOT eligible this cycle ✗
    → May become eligible after Semester III if CGPA improves ✅

  STATUS: No scholarship applicable for Aakash this year
  [Check again after Semester III results]

NOTE FOR COORDINATOR:
  Aakash is OBC-NCL management quota student; income ₹4.2L is above most
  central/state scheme thresholds; not unusual for management quota students.
  Monitor for CGPA improvement for merit scholarship eligibility.
```

---

## 4. Educational Loan Support

```
EDUCATIONAL LOAN — Aakash Sharma

LOAN NEED (assessed):
  Annual fee: ₹1,40,000 (management quota, AFRC-approved)
  4 years: ₹5,60,000
  Living expenses: ~₹1,20,000/year
  Total 4-year loan estimate: ~₹10,40,000

VIDYALAKSHMI PORTAL (Government of India centralised loan portal):
  Portal: vidyalakshmi.co.in
  Aakash's application: VID-2026-000412 (submitted 15 August 2026)
  Banks applied to: SBI Education Loan, Canara Bank Scholar Loan, HDFC Credila
  Status: SBI Scholar Loan — In process (documentation submitted) ✅

DOCUMENTS REQUIRED FROM COLLEGE:
  ✅ Bonafide certificate (A-03 → generates on request)
  ✅ Fee structure (official) for all 4 years
  ✅ Admission letter with seat type (management quota)
  ✅ AICTE approval letter (public document — from K-series)
  ✅ Affiliation letter from JNTU

[Generate all loan documents package]  [Download as ZIP]

BANK LOAN APPROVED: SBI Scholar Loan
  Amount: ₹10,00,000 @ 8.15% (with interest subsidy if eligible)
  Interest subsidy (central scheme): Not eligible (OBC income ₹4.2L > ₹4.5L limit)
  EMI starts: 1 year after course completion or 6 months after employment

INCOME TAX BENEFIT (parent / guarantor):
  Section 80E: Interest paid on education loan (full deduction — no upper limit)
  Available from the year repayment starts
  Bank issues interest certificate annually for IT purposes
```

---

## 5. College Merit Scholarship Register

```
MERIT SCHOLARSHIP — GCEH Internal

Annual scholarship (GCEH endowment):
  Criteria: Top 3 students in each year (by CGPA)
  Amount: ₹25,000/year (partial fee waiver)

MERIT SCHOLARSHIP AWARDEES — 2027–28 (based on Sem I + II CGPA):
  Year I (Sem I + II):
    Rank 1: STU-GCEH-0088  —  CGPA 9.12  —  ₹25,000 ✅
    Rank 2: STU-GCEH-0134  —  CGPA 9.04  —  ₹25,000 ✅
    Rank 3: STU-GCEH-0041  —  wait, Aakash = 7.76 → not in top 3

  Scholarship disbursement: Fee adjustment in Semester III
  [Notify awardees]  [Adjust fee ledger (C-series)]
```

---

## 6. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/college/{id}/scholarship/tracker/` | NSP/state scholarship tracking dashboard |
| 2 | `GET` | `/api/v1/college/{id}/students/{student_id}/scholarship/eligibility/` | Student scholarship eligibility check |
| 3 | `POST` | `/api/v1/college/{id}/scholarship/verify/{app_id}/` | Verify scholarship application |
| 4 | `GET` | `/api/v1/college/{id}/students/{student_id}/loan/documents/` | Generate loan support documents |
| 5 | `GET` | `/api/v1/college/{id}/scholarship/receivables/` | Pending government scholarship receivables |
| 6 | `POST` | `/api/v1/college/{id}/scholarship/merit-award/` | Process merit scholarship |

---

## 7. Business Rules

- NSP applications require the college to "verify" each application within the NSP portal; unverified applications are auto-rejected by NSP after the deadline; the Scholarship Coordinator must verify all applications within the NSP verification window (typically 30 days from application); this is a hard deadline — late verification = student loses scholarship
- Scholarship amounts are credited directly to students' bank accounts by the government (DBT — Direct Benefit Transfer); the college does NOT handle scholarship cash; however, for schemes where the college fee is covered by scholarship (tuition fee reimbursement), the money goes to the college's account; both flows must be tracked
- Government scholarship receivables (TS ePASS outstanding, NSP tuition fee reimbursement) are genuine receivables but with uncertain collection timelines; the college must maintain these as receivables in accounts (C-series) and not write them off; they are eventually paid, sometimes with 12–18 month delays
- Educational loans: The college has no formal role in loan approval (bank's decision); but the college must issue accurate bonafide certificates, fee structures, and admission letters as required; if the college provides incorrect documents to banks, they become liable under the Negotiable Instruments Act / bank lending fraud provisions

---

*Last updated: 2026-03-27 · Group 4 — College Portal · Division A*
