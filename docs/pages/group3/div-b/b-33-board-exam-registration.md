# B-33 — Board Exam Registration (LOC)

> **URL:** `/school/academic/exams/board-registration/`
> **File:** `b-33-board-exam-registration.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Exam Cell Head (S4) — full · Principal (S6) — approve/submit · VP Academic (S5) — read

---

## 1. Purpose

Manages the annual List of Candidates (LOC) submission to CBSE for Class X and Class XII board examinations — the mandatory process by which the school registers students to appear in CBSE board exams. This is one of the most consequential annual workflows: errors in student names (must match Aadhaar), DOB, subject groups, or photograph lead to board exam complications (mismatched mark sheets, court cases, re-checking costs). CBSE charges late fees and penalties for submission delays. The LOC window opens in September–October for the February–March board exams. This page also tracks CBSE admit card (hall ticket) distribution, CBSE result access, and migration certificate verification.

**Applies to:** CBSE-affiliated schools for Class X and XII. State board schools have equivalent workflows (AP ePass, Maharashtra CET portal, etc.) with different portal integrations.

---

## 2. Page Layout

### 2.1 Header
```
Board Exam Registration (LOC)                     [Check CBSE Portal]  [Export LOC Data]
Academic Year: 2025–26  ·  Board: CBSE
Class X LOC: ⚠️ Submission window open (deadline: 15 Oct 2025)
Class XII LOC: ⬜ Window opens 1 Oct 2025
```

---

## 3. LOC Submission Status Dashboard

| Batch | Class | Students | Data Complete | Validation | Submitted to CBSE | Fee Paid | Status |
|---|---|---|---|---|---|---|---|
| LOC 2025–26 Class X | X | 168 | 161/168 | ⚠️ 4 errors | ⬜ Not yet | ⬜ | 🔄 In progress |
| LOC 2025–26 Class XII | XII | 60 | 60/60 | ✅ All valid | ✅ 8 Oct 2025 | ✅ ₹36,000 | ✅ Submitted |

---

## 4. Student Data Preparation (Class X — 168 students)

### 4.1 Student List with Validation Status

| Roll No | Student Name | Aadhaar Match | Photo | Signature | Subjects Configured | Errors | Status |
|---|---|---|---|---|---|---|---|
| HY2025/X/001 | Arjun Sharma | ✅ | ✅ | ✅ | ✅ 5 subjects | — | ✅ Ready |
| HY2025/X/002 | Priya Venkataraman | ✅ | ✅ | ✅ | ✅ 5 subjects | — | ✅ Ready |
| HY2025/X/003 | Rahul Gupta | ⚠️ Name mismatch | ✅ | ✅ | ✅ | Name on Aadhaar: "RAHUL KUMAR GUPTA" | ❌ Fix needed |
| HY2025/X/004 | Anjali Das | ✅ | ❌ Missing | ✅ | ✅ | Photo not uploaded | ⚠️ Fix needed |
| HY2025/X/005 | Deepak M | ✅ | ✅ | ❌ Missing | ✅ | Signature not uploaded | ⚠️ Fix needed |
| HY2025/X/006 | Kavitha Reddy | ✅ | ✅ | ✅ | ❌ 4th subject not selected | Missing additional subject | ❌ Fix needed |

### 4.2 Error Resolution Panel

**7 errors to fix before LOC submission:**

| # | Student | Error | Action |
|---|---|---|---|
| 1 | Rahul Gupta | Name mismatch with Aadhaar | [Update Name to Aadhaar Spelling] |
| 2 | Anjali Das | Photo missing | [Send Reminder to Class Teacher] [Upload Photo] |
| 3 | Deepak M | Signature missing | [Upload Signature] |
| 4 | Kavitha Reddy | Subject group incomplete | [Complete Subject Selection] |
| 5 | Suhani K | DOB mismatch (Aadhaar: 15 Apr, School: 15 Mar) | [Raise DOB correction — Principal approval needed] |
| 6 | Arjun R | No Aadhaar uploaded | [Upload Aadhaar or request CBSE waiver] |
| 7 | Priya M | Additional subject not mapped to CBSE code | [Map to CBSE Subject Code] |

---

## 5. Student Data Entry / Verification

Click any student → opens verification form:

### Student: Arjun Sharma (Class X-A)

| Field | School Record | Aadhaar | CBSE Requirement | Status |
|---|---|---|---|---|
| Name | ARJUN SHARMA | ARJUN SHARMA | Match required | ✅ |
| Date of Birth | 14 Aug 2009 | 14 Aug 2009 | Match required | ✅ |
| Gender | Male | Male | Match required | ✅ |
| Mother's Name | Mrs. Kavitha Sharma | — | As per Aadhaar | — |
| Aadhaar No | 1234 5678 9012 (masked) | — | Mandatory | ✅ Uploaded |
| Photograph | [View] 35×45mm | — | CBSE specs: 35×45mm, white BG, recent | ✅ |
| Signature | [View] | — | Student's own signature on white paper | ✅ |
| CWSN Status | No | — | Disability certificate if yes | N/A |

### Subject Group Configuration

| Subject | CBSE Code | Category | Status |
|---|---|---|---|
| English (Core) | 101 | Compulsory | ✅ |
| Hindi (Core) | 002 | Compulsory | ✅ |
| Mathematics (Basic) | 241 | Compulsory | ✅ |
| Science | 086 | Compulsory | ✅ |
| Social Science | 087 | Compulsory | ✅ |
| Computer Applications | 165 | Additional (6th subject) | ✅ |

**Mathematics Basic vs Standard (CBSE Class X):** Student and parent must choose. Standard (041) allows Maths stream in XI; Basic (241) doesn't. This choice is locked at LOC time.

---

## 6. Photo & Signature Specifications

CBSE requires specific format:
- **Photograph:** 35mm × 45mm, white background, recent (within 3 months), clear face, no glasses, formal wear; file size < 100KB, JPG format
- **Signature:** Student's own signature on plain white paper, scanned; file size < 50KB, JPG format

EduForge validates file dimensions and size at upload. Non-compliant files show an error.

[Bulk Photo Upload] → ZIP file with photos named by roll number (e.g., `HY2025_X_001.jpg`). System matches to students automatically.

---

## 7. Fee Computation

| Item | Count | Rate | Amount |
|---|---|---|---|
| Class X Regular Candidates | 165 | ₹1,500 | ₹2,47,500 |
| Class X Additional Subject | 28 students × 1 subject | ₹300 | ₹8,400 |
| Class XII Regular Candidates | 60 | ₹1,500 | ₹90,000 |
| Late Fee (if applicable) | — | ₹2,000 | ₹0 |
| **Total Payable to CBSE** | | | **₹3,45,900** |

Payment via CBSE portal (net banking/NEFT from school account). Payment reference number logged here.

---

## 8. CBSE Portal Submission

[Submit to CBSE Portal] → Exam Cell Head exports the LOC data in CBSE-prescribed format (XML/CSV) and uploads to CBSE's Saras portal (saras.cbse.gov.in):

1. **Export LOC file** → EduForge generates CBSE-compliant XML with all student data
2. **Upload to Saras portal** → Exam Cell Head logs into CBSE Saras (external), uploads XML
3. **Log submission in EduForge** → Enter CBSE acknowledgement number + date

```
LOC Submission Log:
  Submitted by: Mr. Rajan Kumar (Exam Cell Head)
  Date: 8 Oct 2025  ·  Time: 3:42 PM
  CBSE Acknowledgement No: CBSE/LOC/2025/DLH/0038291
  Candidates: X — 168, XII — 60
  Fee Paid: ₹3,45,900  ·  UTR: HDFC0923810312
  Status: ✅ Accepted by CBSE
```

---

## 9. Admit Card Distribution Tracking

When CBSE releases admit cards (typically December–January for Feb–March exams):

[Download Admit Cards from CBSE] → Exam Cell Head downloads from Saras portal → uploads ZIP to EduForge → system distributes to class teachers

| Student | Hall Ticket No | Downloaded | Distributed | Collected by Student |
|---|---|---|---|---|
| Arjun Sharma | CBSE/X/2026/DLH/001234 | ✅ | ✅ Class teacher | ✅ 15 Jan 2026 |
| Priya V | CBSE/X/2026/DLH/001235 | ✅ | ✅ | ✅ |
| Rahul G | CBSE/X/2026/DLH/001236 | ✅ | ✅ | ⏳ Not collected yet |

---

## 10. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/board-registration/?year={year}` | LOC overview |
| 2 | `GET` | `/api/v1/school/{id}/board-registration/{batch_id}/students/` | Student list with validation |
| 3 | `PATCH` | `/api/v1/school/{id}/board-registration/{batch_id}/students/{student_id}/` | Update student LOC data |
| 4 | `POST` | `/api/v1/school/{id}/board-registration/{batch_id}/validate/` | Run validation |
| 5 | `GET` | `/api/v1/school/{id}/board-registration/{batch_id}/errors/` | Error list |
| 6 | `POST` | `/api/v1/school/{id}/board-registration/{batch_id}/photos/bulk-upload/` | Bulk photo upload |
| 7 | `GET` | `/api/v1/school/{id}/board-registration/{batch_id}/export-loc/` | Export CBSE LOC XML |
| 8 | `POST` | `/api/v1/school/{id}/board-registration/{batch_id}/log-submission/` | Log CBSE submission |
| 9 | `POST` | `/api/v1/school/{id}/board-registration/{batch_id}/admit-cards/upload/` | Upload CBSE admit cards |
| 10 | `GET` | `/api/v1/school/{id}/board-registration/{batch_id}/fee-computation/` | Fee breakdown |

---

## 11. Business Rules

- Student name in LOC must exactly match Aadhaar — CBSE will reject mismatches; the school bears responsibility for corrections (re-LOC fee applies)
- Mathematics Basic vs Standard selection is final once LOC is submitted to CBSE; changes require CBSE Level 2 correction procedure (fee + deadline)
- LOC submission without Principal approval is blocked — Principal must confirm [Approve LOC] before Exam Cell Head can export to CBSE
- CBSE LOC deadlines are non-negotiable — EduForge shows countdown timer (days remaining) prominently from August
- Students repeating a year (detained) or newly transferred into Class X/XII must be flagged; CBSE has special registration procedures for them
- This page applies to CBSE schools; for ISC (CISCE) schools, the workflow is similar but portal is CISCE's own system; for state boards, portal integrations vary by state

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division B*
