# C-06 — Document Collection Register

> **URL:** `/school/admissions/documents/`
> **File:** `c-06-document-collection.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Admission Officer (S3) — full · Administrative Officer (S3) — full · Class Teacher (S3) — own class · Academic Coordinator (S4) — read · Principal (S6) — full

---

## 1. Purpose

Tracks the status of every document that needs to be collected from students — at admission time and throughout the academic year. CBSE affiliation regulations require schools to maintain a document register with specific documents per student, and CBSE inspectors verify this register during affiliation renewal. The document register is also critical for:
- **TC (Transfer Certificate) received register:** CBSE mandates schools maintain a register of TCs received from previous schools for every transfer student
- **Board exam registration (B-33):** Aadhaar name-match, photo format, signatures must be verified before LOC submission
- **Government scholarships:** National Merit Scholarship, Pre-Matric/Post-Matric SC/ST scholarships require document verification
- **DPDPA compliance:** Schools must be able to demonstrate which documents they hold and why (data minimisation principle)

This page gives the Administrative Officer a checklist view of all students' document status, with the ability to mark documents as received, upload scans, and send reminders to parents for missing documents.

---

## 2. Page Layout

### 2.1 Header
```
Document Collection Register                  [+ Update Documents]  [Missing Documents Report]  [Export]
Academic Year: 2026–27  |  Class: [All ▼]  |  Filter: [Missing Docs ▼]
Students with All Docs: 312 (82%)  ·  Incomplete: 68 (18%)  ·  Critical Missing: 14
```

### 2.2 Student Document Status Grid
```
Class: XI-A (38 students)

Roll  Name             Birth  Aadhaar  TC      Photo  Caste  Health  Signature  Status
01    Anjali Das       ✅     ✅       ✅      ✅     N/A    ⬜      ✅         1 missing
02    Arjun Sharma     ✅     ✅       ✅      ✅     ✅     ⬜      ✅         1 missing
03    Priya Venkat     ✅     ✅       ✅      ✅     N/A    ✅      ✅         ✅ Complete
04    Rohit Kumar      ✅     ✅       ✅      ✅     N/A    ⬜      ✅         1 missing
...
```
Columns = document types (configurable per school).
Clicking any cell opens the upload/mark dialog.

---

## 3. Document Types

### 3.1 Standard Documents (All Students)
| Document | When Needed | When Required for Enrollment | Notes |
|---|---|---|---|
| Birth Certificate | Nursery–Class I | ✅ Mandatory before enrollment | GHMC / Municipal birth cert, or hospital cert for recent births |
| Student Aadhaar Card | All classes | ✅ Mandatory before enrollment | Original seen + photocopy retained |
| Father Aadhaar | All classes | ✅ Mandatory | For parent verification, scholarship applications |
| Mother Aadhaar | All classes | ✅ Mandatory | |
| Transfer Certificate (TC) | Class II+ transfers | ✅ Mandatory within 15 days | From previous school; CBSE format preferred |
| Passport Photos (4) | All | ✅ At enrollment | 35×45mm colour on white background |
| Previous Year Report Card | Class II+ | Recommended | Academic history |
| Migration Certificate | Board change (CBSE→State or vice versa) | ✅ If applicable | From previous board |

### 3.2 Category Documents
| Document | Required For | Notes |
|---|---|---|
| Caste Certificate | SC / ST / OBC-NCL students | Issued by Tahsildar/SDM |
| Income Certificate | EWS / RTE applicants | Below ₹1 lakh per year |
| Disability Certificate | CWSN students | From SADGURU / District Medical Board |
| Ex-Serviceman Certificate | Ward of ex-serviceman | |

### 3.3 For Board Exam Registration (Class IX → X registration, Class XI → XII)
| Document | Notes |
|---|---|
| Aadhaar Name (matches exactly) | Name in Aadhaar must match school records; discrepancy = B-33 block |
| 35×45mm Photo (CBSE specific) | Separate from admission photos; white background; recent |
| Student Signature | For hall ticket; uploaded in B-33 |
| Parent/Guardian Signature | |

### 3.4 Class XI Specific
| Document | Notes |
|---|---|
| Class X Mark Sheet (Original) | Required before Class XI stream allocation |
| Class X Pass Certificate | |
| Class X TC | If coming from another school |

---

## 4. Document Upload & Verification

Clicking any document cell:

```
Arjun Sharma  |  Class XI-A  |  Roll 02
Document: Student Aadhaar Card

Physical Original: ✅ Sighted on 25 Mar 2026 by Meera (Admission Officer)
Scanned Copy: [View PDF]  ·  Uploaded: 25 Mar 2026
Aadhaar Number: 9876 XXXX XXXX (last 4: 4521)
Name on Aadhaar: ARJUN SHARMA (matches school record: Arjun Sharma ✅)

[Replace Document]  [Mark Not Required]  [Request from Parent]
```

### Name Mismatch Alert
If the name on Aadhaar doesn't match the school record:
```
⚠️ Name Mismatch Detected
School Record: Arjun Sharma
Aadhaar:       ARJUN SHARMA RAJESH  (middle name mismatch)

Action Required: Either update school record (if school record is wrong)
or parent must apply for Aadhaar name correction.
Note: CBSE board exam registration (B-33) will block until resolved.

[Update School Record]  [Flag for Aadhaar Correction]  [Principal Override]
```

---

## 5. TC Received Register

A critical sub-register within this page — mandated by CBSE:

```
TC RECEIVED REGISTER — 2026–27
[School Name] — [Affiliation No.]

S.No.  TC No.         From School              Date Received  Class  Student Name         Filed
001    SM/TC/2026/089  St. Mary's, Hyderabad    20 Mar 2026    XI-A   Arjun Sharma         ✅
002    KVS/TC/425      Kendriya Vidyalaya, Pune  15 Feb 2026   IX-B   Suresh Kumar         ✅
003    —               [Unknown — student claims TC in transit]  —    VIII-A  Priya Das   ⚠️ Pending
```

- TC original must be physically filed in the school office
- CBSE inspection checks TC register against enrollment register for Classes IX–XII
- If TC not received within 15 days, automated reminder sent to parent
- If not received within 30 days, Academic Coordinator gets escalation alert

---

## 6. Missing Documents Report

[Missing Documents Report] → generates:

```
MISSING DOCUMENTS REPORT — 2026–27
As of 26 Mar 2026

Critical Missing (blocks board exam registration):
  Arjun Sharma (XI-A) — Aadhaar name mismatch, signature pending
  Priya Venkat (XI-B) — Photo 35×45mm not uploaded

TC Pending (> 15 days):
  Priya Das (VIII-A) — TC from KVS Pune — TC requested 10 Mar; 16 days elapsed

Caste Certificate Pending:
  Ravi Kumar (IX-A) — OBC-NCL, certificate requested 5 Mar

Health Certificate Pending (Optional):
  14 students across 6 classes

Actions:
  [Send WhatsApp Reminders to All Parents with Missing Docs]
  [Export Missing Docs List for Teacher]
```

---

## 7. Reminder to Parents

[Request from Parent] or bulk reminder:
- WhatsApp: "Dear [Parent], We request you to submit [Document Name] for [Student Name] at the school office at your earliest. This is required for [exam registration / scholarship / records]. Contact: [Office number]."
- Logged in student document history with date and channel

---

## 8. Document Retention & DPDPA Compliance

Per DPDPA 2023 and school records norms:
- Student documents retained for the full duration of enrollment + 5 years after leaving
- Aadhaar numbers stored encrypted (AES-256) in database; displayed masked (XXXX XXXX XXXX 4521)
- School can export a "Data Held" report per student for any subject access request

---

## 9. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/students/{student_id}/documents/` | Student document status |
| 2 | `POST` | `/api/v1/school/{id}/students/{student_id}/documents/` | Upload document |
| 3 | `PATCH` | `/api/v1/school/{id}/students/{student_id}/documents/{doc_id}/` | Update status / verification |
| 4 | `GET` | `/api/v1/school/{id}/students/documents/missing/?class_id={id}&year={year}` | Missing documents report |
| 5 | `GET` | `/api/v1/school/{id}/students/documents/tc-register/?year={year}` | TC received register |
| 6 | `POST` | `/api/v1/school/{id}/students/documents/remind/` | Send reminder to parents (bulk or individual) |
| 7 | `GET` | `/api/v1/school/{id}/students/documents/export/?class_id={id}` | Export class document status |

---

## 10. Business Rules

- Physical original of Transfer Certificate must be collected and held by the school — scanning is for reference only; the physical document is the record
- Aadhaar numbers must be stored encrypted; never log in plain text in application logs
- Health/medical certificate is "recommended" not mandatory for enrollment — but if CWSN accommodation is to be given (C-19), the disability certificate is required
- The TC received register is a physical register in most schools — this digital version mirrors it; both must be maintained; EduForge generates the printable TC register in CBSE prescribed format
- Documents cannot be deleted once uploaded — they can only be superseded by a newer version (creates version history for audit)

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division C*
