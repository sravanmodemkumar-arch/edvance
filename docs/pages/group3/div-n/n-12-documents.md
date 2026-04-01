# N-12 — Child's Documents & Certificates (Parent View)

> **URL:** `/parent/documents/`
> **File:** `n-12-documents.md`
> **Template:** `parent_portal.html`
> **Priority:** P1
> **Roles:** Parent/Guardian (S1-P)

---

## 1. Purpose

Parents access official documents related to their child — bonafide certificates, fee certificates, transfer certificates (TC), report card PDFs, and other school-issued documents. Instead of visiting the school office for a bonafide certificate, parents request and download it online.

This module also handles TC (Transfer Certificate) applications — the most sensitive document issuance in a school, as TC means the child is leaving.

---

## 2. Available Documents

```
DOCUMENTS — Rahul Rao (Class X-A)

INSTANTLY AVAILABLE (self-service):
  Document                      Description                    Action
  ─────────────────────────────────────────────────────────────────────────────
  Bonafide Certificate          Confirms enrollment at school  [Request & Download]
  Fee Certificate (2025–26)     Annual tuition fee paid        [Download PDF]
  Fee Certificate (2024–25)     Previous year                  [Download PDF]
  Report Card — UT-1            Unit Test 1 (Feb 2026)         [Download PDF]
  Report Card — Term 1          June 2025                      [Download PDF]
  Attendance Certificate        Month-wise attendance summary   [Request & Download]
  Identity Card (school ID)     For external purposes          [Download PDF]

REQUEST-BASED (school processes within 1–3 days):
  Document                      Description                    Action
  ─────────────────────────────────────────────────────────────────────────────
  Character Certificate         For scholarship/competition use [Request →]
  Sports Achievement Letter     For external admissions        [Request →]
  Migration Certificate         For moving to another state    [Request →]
  Transfer Certificate (TC)     Withdrawal from school ⚠       [Request TC →]
  Study Certificate             For passport/visa purposes     [Request →]

CBSE DOCUMENTS (available after board exams):
  Document                      Status
  CBSE Admit Card (Class X)     March 2026 board — [Download] ✅
  CBSE Marksheet                Available post-result (May 2026)
  CBSE Migration Certificate    Available post-result (May 2026)
```

---

## 3. Bonafide Certificate

```
BONAFIDE CERTIFICATE — Self-Service

Request for: Rahul Rao (Class X-A)
Purpose (select): ● Scholarship application ○ Passport ○ Bank account ○ Other

GREENFIELDS SCHOOL
CBSE Affiliation No.: 1200XXX
Chaitanyapuri, Hyderabad — 500060

BONAFIDE CERTIFICATE

This is to certify that RAHUL RAO, son of SANJAY RAO and SUNITA RAO,
bearing Admission No. ADM-2022-0312, is a bonafide student of this school
studying in CLASS X — Section A, during the academic year 2025–26.

His date of birth as per our records is 14 July 2010.
His conduct and behaviour are satisfactory.

This certificate is issued for the purpose of SCHOLARSHIP APPLICATION.

Issued on: 27 March 2026
[Digital signature — Principal Ms. Meena Rao]
Certificate No.: BONA/2026/0412

[Download PDF]  [This certificate is valid for 90 days from date of issue]

Note: For official purposes requiring physical signature + school seal, the
  parent should collect a printed copy from the school office.
  This digitally signed certificate is valid for most online uses (DGILOCKER-style).
```

---

## 4. Transfer Certificate Request

```
TRANSFER CERTIFICATE — REQUEST
⚠ This action indicates your child is leaving Greenfields School.

Before you proceed, please confirm:
  "I am requesting a Transfer Certificate for Rahul Rao because:
    ○ We are relocating to another city/state
    ○ We are changing schools within Hyderabad
    ○ Rahul has completed Class XII and is leaving
    ● Other reason: [text field]"

IMPORTANT INFORMATION:
  ✅ TC is issued within 7 school days of request
  ✅ All dues must be cleared before TC is issued (fee outstanding: ₹8,400)
    [Pay outstanding first → N-04]
  ✅ TC request triggers a school exit checklist (library books, ID card return)
  ✅ Last attending date must be specified
  ⚠ TC once issued cannot be cancelled; the child is formally de-enrolled

  [Proceed with TC request →] — You will be contacted by the school office within 24 hours

SCHOOL PROCESS (after TC request):
  → School office contacts parent to confirm and collect outstanding items
  → Fee clearance verified (D-01)
  → TC issued with academic record up to last attending date
  → CBSE records updated (SLC/TC register — K-07)
```

---

## 5. Document Request History

```
DOCUMENT HISTORY — Rahul Rao (2025–26)

  Date        Document                   Requested By   Status
  27 Mar 2026 Bonafide Certificate       Parent (N-12)  ✅ Downloaded
  15 Jan 2026 Fee Certificate 2024–25    Parent         ✅ Downloaded
  10 Dec 2025 Bonafide Certificate       Parent         ✅ Downloaded
  30 Sep 2025 Report Card — Term 1       Auto-release   ✅ Downloaded
```

---

## 6. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/parent/{parent_id}/child/{student_id}/documents/` | List available documents |
| 2 | `GET` | `/api/v1/parent/{parent_id}/child/{student_id}/documents/{doc_type}/pdf/` | Download document PDF |
| 3 | `POST` | `/api/v1/parent/{parent_id}/child/{student_id}/documents/bonafide/` | Generate bonafide certificate |
| 4 | `POST` | `/api/v1/parent/{parent_id}/child/{student_id}/documents/request/` | Request custom document |
| 5 | `POST` | `/api/v1/parent/{parent_id}/child/{student_id}/documents/tc/` | Initiate TC request |
| 6 | `GET` | `/api/v1/parent/{parent_id}/child/{student_id}/documents/history/` | Document request history |

---

## 7. Business Rules

- Bonafide certificates generated through the portal carry a digital signature (using the school's PKI certificate); they are valid for most digital submission purposes; for physical submission (passport application, bank), the parent must collect a physically stamped copy from the school office; this workflow cannot yet be fully eliminated due to institutional requirements for wet signatures in India
- TC issuance is blocked until all fee dues are cleared (D-01 confirmation required); this is a standard school protection against non-payment at exit; however, for RTE students (zero fee), TC is issued without any delay; for hardship cases, the Principal can override the block
- TC documents are permanent records — they are not deleted from EduForge even after the student leaves; the issuing school retains the TC register entry; CBSE requires schools to maintain TC registers for 10 years
- Document downloads are watermarked with "Downloaded by [parent name] on [date]" — this is a DPDPA audit trail measure; it also deters misuse (e.g., a photoshopped bonafide certificate is harder to produce when the original has a visible watermark)
- The CBSE Admit Card (for board exams) is the most critical document — it is only available after CBSE confirms the student's registration and hall ticket number; the school downloads it from the CBSE portal and makes it available here; a student without a hall ticket cannot appear for board exams; EduForge sends reminders to parents to download and check the admit card (correct name, DOB, photograph) as soon as it is available

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division N*
