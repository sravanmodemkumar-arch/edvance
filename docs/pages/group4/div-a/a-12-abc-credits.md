# A-12 — Academic Bank of Credits (NEP 2020)

> **URL:** `/college/students/abc/`
> **File:** `a-12-abc-credits.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Roles:** Registrar (S4) · Academic Coordinator (S4) · Student (S1) — view own ABC account

---

## 1. Purpose

The Academic Bank of Credits (ABC) is a NEP 2020 initiative — a national digital repository where every student's academic credits from any registered institution are stored. Students can:
- Accumulate credits from multiple institutions
- Carry forward credits if they switch institutions
- Use ABC for multiple-exit degrees
- Transfer credits between institutions in the same ABC ecosystem

AICTE/UGC requirement: All degree-awarding institutions must upload credits to ABC after each semester; NAAC now checks ABC implementation.

---

## 2. ABC Account — Student View

```
ACADEMIC BANK OF CREDITS — Aakash Sharma
ABC ID: ABC-2026-GCEH-0041
Digilocker linked: ✅ (ABCID visible in Digilocker)
NAD (National Academic Depository) account: ✅ Active

CREDITS ON DEPOSIT:

Institution          Programme        Period      Credits Deposited
GCEH (current)       B.Tech CSE       Sem I       22 (uploaded Jul 2027)
GCEH (current)       B.Tech CSE       Sem II      24 (uploaded Jul 2027)
─────────────────────────────────────────────────────────────────
TOTAL CREDITS:       46 (of 160 required for B.Tech Honours with Research)

MULTIPLE EXIT STATUS:
  Certificate exit (40 credits): Not eligible yet (46 > 40 ✅ — has > Certificate threshold)
    Wait — this means: eligible for Certificate exit if desired ✅ (but continuing)
  Diploma exit (80 credits): Not yet (need 34 more credits)
  B.Tech 3-year (120 credits): Not yet (need 74 more credits)
  B.Tech 4-year Honours (160 credits): Target (expected 2030)

CREDIT TRANSFER REQUESTS:
  None submitted ← (no prior institution)

ONLINE COURSE CREDITS (approved external courses):
  If student completed SWAYAM/NPTEL course in Semester II:
  NPTEL "Programming in Python" (12-week): 4 credits (if approved by GCEH academic council)
  Aakash: No NPTEL course this semester
```

---

## 3. College ABC Administration

```
ABC ADMINISTRATION — GCEH
Semester II Batch Upload (2027)

Upload status:
  Students: 332
  Uploaded: 332 ✅
  Errors: 0 ✅
  Upload date: 20 July 2027
  ABC batch reference: ABC-GCEH-SEM2-2027-BATCH-001

NPTEL/SWAYAM COURSE CREDIT RECOGNITION:
  Students who completed NPTEL courses this semester: 24
  Courses recognised (approved by Academic Council): 18
  Credits granted: 2–4 credits per course (per GCEH/JNTU mapping)
  Uploaded to ABC: ✅

PENDING CREDIT TRANSFER REQUESTS (from other institutions):
  None pending ✅

QUALITY CHECK (NAAC criterion 2.6):
  ABC upload timely (within 30 days of results): ✅
  All enrolled students have ABC ID: 332/332 ✅
  NAAC evidence: [Download upload confirmations for NAAC SSR]
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/college/{id}/students/{student_id}/abc/` | Student ABC credit summary |
| 2 | `POST` | `/api/v1/college/{id}/abc/batch-upload/` | Batch upload semester credits to ABC/NAD |
| 3 | `GET` | `/api/v1/college/{id}/abc/upload-status/` | Upload status for current semester |
| 4 | `POST` | `/api/v1/college/{id}/abc/credit-transfer/approve/` | Approve incoming credit transfer |
| 5 | `GET` | `/api/v1/college/{id}/abc/naac-evidence/` | NAAC-ready ABC implementation evidence |

---

## 5. Business Rules

- ABC ID creation happens at enrolment (Day 1 of Semester I); if a student has an existing ABC ID (from a previous institution or Digilocker), it must be linked rather than creating a duplicate; duplicate ABC IDs cause reconciliation problems in NAD
- Every semester's credits must be uploaded within 30 days of result declaration; this is a compliance obligation under NEP 2020 implementation guidelines; NAAC criterion 2.6 specifically evaluates "implementation of ABC" and missing uploads are noted as gaps
- NPTEL/SWAYAM courses: Students may request credit recognition for online courses; the institution's academic council must formally approve each course mapping (which NPTEL course = which institution course credit); not all NPTEL courses are automatically credit-worthy; the council's decision is recorded and uploaded to ABC
- Credit transfer from another institution (if a student transfers in) requires: (a) the sending institution's ABC-uploaded credits, (b) the receiving institution's academic council approval for equivalence mapping, (c) ABC update; without this formal process, a transferred student may lose credits

---

*Last updated: 2026-03-27 · Group 4 — College Portal · Division A*
