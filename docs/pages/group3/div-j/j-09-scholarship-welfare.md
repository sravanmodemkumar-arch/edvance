# J-09 — Scholarships & Welfare Schemes

> **URL:** `/school/welfare/scholarship/`
> **File:** `j-09-scholarship-welfare.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Administrative Officer (S3) — manage applications · Accounts Officer (S3) — track disbursements · Academic Coordinator (S4) — eligibility verification · Principal (S6) — approvals and certifications

---

## 1. Purpose

Tracks scholarships and welfare schemes available to students — central government, state government, school-internal, and external scholarships. India has a rich ecosystem of student scholarship programmes; many students and parents are unaware of schemes they are eligible for. This module:
- Maintains a scholarship directory (government + school-sponsored)
- Tracks student applications and their status
- Issues certificates required for scholarship applications (income, marks, attendance)
- Manages school-internal fee concessions (separate from fee module)
- Coordinates RTE scholarship/reimbursement claims from state government

---

## 2. Scholarship Directory

```
Scholarship Directory — 2026–27                      [+ Add New Scheme]

Government Scholarships:
  Scheme                     Authority      Eligibility              Amount         Deadline
  National Merit Scholarship  MHRD/MoE      Class X >60%, income cap  ₹1,200/yr      30 Nov 2026
  Pre-Matric SC/ST            MoSJE         SC/ST, Class IX-X         ₹3,500/yr      31 Oct 2026
  Post-Matric SC/ST           MoSJE         SC/ST, Class XI-XII       ₹7,000/yr      31 Oct 2026
  Minority Scholarship        MoMA          Minority communities      ₹10,000/yr     30 Sep 2026
  NSP (National Scholar.Portal) DoE         Multiple categories       Various        Varies
  State Govt Merit Award      TG Govt        Class X >90% (state board) ₹2,000 one-time Announced post-results

CBSE/Board related:
  NTSE (National Talent Search) NCERT       Class X — written exam    ₹1,250/mon     Feb 2027 (exam)
  INSPIRE (DST)               DST           Top 1% Class X — Science  ₹5,000/yr      Sep 2026
  Kishore Vaigyanik Protsahan IISC/DST      Class XI-XII — Science    ₹5,000/mon     Sep 2026 (exam)

School-Internal:
  Merit Scholarship           School Trust  Top 5 Class X/XII         ₹5,000 one-time Post-results
  Sports Excellence           School Trust  State/National sports reps ₹2,000/yr      Jun annually
  Financial Hardship           School        Case by case              Fee waiver      Rolling
```

---

## 3. Student Applications Tracker

```
Scholarship Applications — 2026–27

Student         Class  Scheme                  Applied   Status        Amount    Disbursed
Priya V.        XI-A   Post-Matric SC           Oct 2026  ✅ Approved   ₹7,000    ✅ Nov 2026
Rahul M.        XII-A  INSPIRE                  Sep 2026  ⏳ Pending    ₹5,000    —
Sunita K.       XII-A  Merit (school internal)  Apr 2026  ✅ Approved   ₹5,000    ✅ Apr 2026
Arjun S.        XI-A   KVPY                     Sep 2026  ❌ Not selected —        —
Meena D.        IX-A   Pre-Matric SC            Oct 2026  ✅ Approved   ₹3,500    ✅ Dec 2026
Chandana R.     XI-A   Minority scholarship     Oct 2026  ⏳ Pending    ₹10,000   —

Total approved this year: 8 students  ·  Total amount: ₹47,500
Pending (awaiting government action): 3
```

---

## 4. Certificate Generation for Scholarship Applications

```
Scholarship Certificate Requests

Certificates required for most government scholarship applications:
  1. School bonafide/enrollment certificate
  2. Previous year marksheet (school-certified copy)
  3. Attendance certificate (for schemes requiring 75%+)
  4. Caste/category certificate (government-issued; school certifies category as per records)
  5. Income certificate (parent's — government-issued; school does not issue this)
  6. Bank account details of student (for direct benefit transfer — DBT)

[Generate Certificates for Scholarship]

Student: [Priya V. — XI-A]
Scheme: Post-Matric SC Scholarship (MoSJE)

Certificates to generate:
  ☑ Bonafide Certificate — [Generate]
  ☑ Marks Certificate (Class X) — [Generate — pulls from C-07 academic history]
  ☑ Attendance Certificate (current year: 88.5% — ✅ meets ≥75% requirement)
    [Generate attendance certificate — pulls from E-01/E-09]
  ☑ Category Certificate (SC — as per admission records) — [Generate]

School certification note: The school certifies only what is in its records;
  income and caste certificates are government-issued — the school does not forge or
  vouch for external documents.

All certificates: Signed by Principal, school stamp, date of issue.
[Generate All]  [Download PDF pack]
```

---

## 5. National Scholarship Portal (NSP) Integration

```
NSP (National Scholarship Portal — scholarships.gov.in) Integration

India's NSP is the central portal for all centrally-sponsored scholarship schemes.
Students/parents apply on NSP; the school verifies and approves on NSP.

School NSP role:
  The school is a "verifying authority" on NSP for its enrolled students.
  Administrative Officer logs into NSP with school credentials (Aadhaar-linked).

Pending NSP verifications: 4 students (need school's approval on NSP portal)
  ● Verify and approve on NSP → [Open NSP portal — opens in new tab]
  ● Update status in EduForge after NSP action

  NSP verification checklist (per student):
    ☑ Student is enrolled in this school for the stated year
    ☑ Caste/category matches school records
    ☑ Attendance is ≥75% (as required by scheme)
    ☑ Previous year marks match school records
    [Verify on NSP]

Note: NSP is an external system (NIC/government); EduForge maintains a mirror
  of NSP applications for school's internal tracking; actual verification
  must be done on the official NSP portal.
```

---

## 6. RTE Scholarship / Reimbursement

```
RTE Section 12(1)(c) — State Government Reimbursement

Schools admitting RTE students (25% EWS/DG seats) are entitled to reimbursement
from the state government for the fees they cannot charge these students.

Reimbursement per student = State government per-student expenditure rate
(TS: approximately ₹12,000–₹18,000/year/student depending on class)

Enrolled RTE students: 14 (current year)
Reimbursement claimed: ₹2,10,000 (for 14 students × ₹15,000 average)
Reimbursement received: ₹1,68,000 (80% — 2 students' claims pending state audit)

Annual RTE claim process:
  1. Submit enrollment details to District Education Officer (DEO)
  2. Submit attendance records (minimum 75% for each student to be eligible)
  3. Provide fee structure certification
  4. Government audits and releases payment (typically 6–18 months delay — common problem)

[Generate RTE reimbursement application]  [Track payment status]

Note: Schools often face delays in RTE reimbursement; EduForge tracks pending amounts
  as accounts receivable from government in D-01 (Fee Register — government dues).
```

---

## 7. School-Internal Welfare Fund

```
School Welfare Fund — 2026–27

Purpose: Fee concession/waiver for students from economically weak backgrounds
  who do not qualify for government scholarships but are in genuine hardship.

Fund corpus: ₹5,00,000 (annual allocation from school management)
Disbursed: ₹2,45,000
Balance: ₹2,55,000

Active welfare support students: 8
  2 full fee waiver (extreme hardship — orphan/single parent)
  4 50% concession
  2 transport fee waiver only

Process for applying:
  Parent application → Counsellor/class teacher recommendation → Principal review
  No income proof required (school trusts; counsellor verifies through home visit or
  teacher's personal knowledge)

Confidentiality: The names of welfare fund beneficiaries are NOT published anywhere;
  other students do not know; this protects the dignity of the students.
  Even class teachers know only that "this student has a fee arrangement" — not that
  it is from the welfare fund specifically.

[Review pending applications]  [Approve concession]  [Export welfare fund report]
```

---

## 8. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/welfare/scholarship/directory/` | Scholarship directory |
| 2 | `GET` | `/api/v1/school/{id}/welfare/scholarship/applications/` | Student applications tracker |
| 3 | `POST` | `/api/v1/school/{id}/welfare/scholarship/applications/` | Log new application |
| 4 | `PATCH` | `/api/v1/school/{id}/welfare/scholarship/applications/{app_id}/status/` | Update status |
| 5 | `POST` | `/api/v1/school/{id}/welfare/scholarship/certificates/generate/` | Generate scholarship certificates |
| 6 | `GET` | `/api/v1/school/{id}/welfare/scholarship/rte-reimbursement/` | RTE claim tracking |
| 7 | `GET` | `/api/v1/school/{id}/welfare/scholarship/welfare-fund/` | Internal welfare fund summary |
| 8 | `POST` | `/api/v1/school/{id}/welfare/scholarship/welfare-fund/concession/` | Apply welfare concession |

---

## 9. Business Rules

- School certificates for scholarship applications must be signed by the Principal and bear the school's official stamp; no other staff member can sign these certificates
- The school verifies only what is within its records (enrollment, marks, attendance, category as per school records); the school cannot certify income, caste, or other facts that are government-domain — those require government-issued documents
- NSP verification: schools must verify applications within 30 days of submission; delayed verification causes the student's scholarship to be rejected; the Administrative Officer should check NSP at minimum weekly during the October–December application season
- RTE reimbursement claims: the school must maintain complete records to support the claim; documentation gaps (missing attendance, unsigned enrollment records) are the primary reason for reimbursement rejection; this module's records feed directly into the claim documents
- Welfare fund disbursements are internal financial transactions (D-07 adjustments); they do not appear as fee income but as a fund utilisation; the school's accounts show the fund outflow; the student's fee ledger shows a "welfare concession" (amount, not reason)
- DPDPA: scholarship applications contain sensitive information (caste category, income, disability status) — these are accessible only to the Administrative Officer handling the application and the Principal; subject teachers and class teachers do not have access

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division J*
