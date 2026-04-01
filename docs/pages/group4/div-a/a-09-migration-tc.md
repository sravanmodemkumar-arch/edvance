# A-09 — Migration, TC & Lateral Entry

> **URL:** `/college/students/migration/`
> **File:** `a-09-migration-tc.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Registrar (S4) · Examination Controller (S4) · Principal/Director (S6) — approve TC

---

## 1. Purpose

Manages student transfers in two directions:
1. **Outgoing:** Students leaving the college (TC + migration certificate for university)
2. **Incoming lateral entry:** Diploma holders joining B.Tech in Semester III (AICTE/TGCHE lateral entry scheme)

College-specific nuances:
- TC from affiliated college requires university migration certificate (separate from college TC)
- Lateral entry students join a different semester and have a different roll number format
- Credit transfer from other institutions (NEP 2020 ABC mechanism)

---

## 2. Transfer Certificate — Outgoing Student

```
TC REQUEST — Mr. Arjun T. (226J1A0503)

Reason for leaving: "Transferred to NIT Warangal (NIT seat allotted via JEE Advanced Round 4)"

COLLEGE TC PROCESS:
  All dues cleared: Fee outstanding: ₹0 ✅
  University exam fee pending: ₹0 ✅
  Library books: Returned ✅ (2 books — cleared)
  Hostel dues: ₹0 ✅ (day scholar)
  Lab deposits: ₹2,000 refunded (paid at admission — returned with TC) ✅

  No disciplinary case pending ✅
  No backlog exams pending (student is moving before any exams) ✅

COLLEGE TC:
  TRANSFER CERTIFICATE
  Greenfields College of Engineering
  This is to certify that Mr. Arjun T. (Roll No. 226J1A0503), son of Mr. [X],
  was a student of this college in B.Tech CSE (Semester I, 2026–27).
  He has been a student of good conduct.
  He has been issued this TC on [Date] for the purpose of joining another institution.

  Date of joining: 10 August 2026
  Date of leaving: 30 March 2027 (after Semester I results)
  Remarks: Transferred to NIT Warangal — voluntarily

  [College seal + Principal digital signature]
  TC No.: GCEH/TC/2027/0018

UNIVERSITY MIGRATION CERTIFICATE (JNTU):
  Required for: Transferring to a non-JNTU affiliated institution
  Application process:
    College submits migration application to JNTU on student's behalf
    JNTU issues migration certificate (₹500 fee — remitted by student)
    Time: 15–30 days from JNTU receipt
  Status: Applied ✅ — JNTU processing
```

---

## 3. Lateral Entry — Incoming

```
LATERAL ENTRY — B.Tech Semester III (2027–28)

AICTE/TGCHE Lateral Entry Scheme:
  Diploma holders (3-year Polytechnic) can join B.Tech in Semester III
  (skipping Semesters I and II — credits granted as Lateral Entry exemption)

LATERAL ENTRY INTAKE (2027–28):
  Seats: 10% of approved intake per programme (AICTE norm)
  CSE lateral entry seats: 12 (10% of 120)

ELIGIBILITY:
  3-year Diploma in relevant engineering discipline (Polytechnic Board TS)
  Minimum 45% marks in Diploma (40% for SC/ST)
  Application through TGCHE-LAWCET/lateral entry counselling

LATERAL ENTRY STUDENT — EXAMPLE:
  Student: Ms. Kavitha D.
  Diploma: Electronics & Communication (SBTET, 2027) — 78.4%
  Joined: B.Tech ECE, Semester III, 2027–28

  Roll No. Format (JNTU lateral entry): 227J5A0401
    22 = batch 2022 Diploma  |  7 = LE year  |  J5 = GCEH ECE  |  04 = serial 4

  CREDIT EXEMPTION:
    Semester I and II exempted (Diploma equivalence)
    ABC credits from Diploma: Recognised under NEP 2020 credit transfer
    Lateral entry students' ABC: Show Diploma credits as prior learning

  REGISTRATION:
    Lateral entry students register for all Semester III courses
    They must catch up on any Semester I/II pre-requisite content independently
    (College may arrange a bridge course for the first 2 weeks of Semester III)
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `POST` | `/api/v1/college/{id}/students/{student_id}/tc/` | Initiate TC process |
| 2 | `GET` | `/api/v1/college/{id}/students/{student_id}/tc/status/` | TC status and checklist |
| 3 | `POST` | `/api/v1/college/{id}/students/{student_id}/migration/` | Apply for university migration certificate |
| 4 | `POST` | `/api/v1/college/{id}/lateral-entry/enrol/` | Enrol lateral entry student |
| 5 | `GET` | `/api/v1/college/{id}/lateral-entry/` | Lateral entry intake status |

---

## 5. Business Rules

- TC cannot be issued until all dues are cleared — this is industry-wide practice; the standard list of clearances (library, hostel, lab deposit, fee) must all be complete; EduForge enforces this as a checklist — TC generation is blocked until all items are checked
- University migration certificate from JNTU is a separate document from the college TC; a student who only has the college TC but not the JNTU migration certificate may face issues at universities that require JNTU's migration certificate for admissions; the college must proactively advise students about this and initiate the university application simultaneously with the college TC
- Lateral entry students have a different roll number format; university registration, hall tickets, and results must correctly identify them as lateral entry (JNTU distinguishes LE students in their database); incorrect registration format can cause issues at results publication
- Under NEP 2020, prior learning credit recognition is expanding; a student with a relevant Diploma may get specific subject credits recognised (beyond just the Semester I/II block exemption); this requires academic council approval and is not yet standardised across all universities; EduForge tracks such credit recognition decisions for ABC upload

---

*Last updated: 2026-03-27 · Group 4 — College Portal · Division A*
