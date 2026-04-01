# C-09 — APAAR & Aadhaar Linkage

> **URL:** `/school/students/apaar-aadhaar/`
> **File:** `c-09-apaar-aadhaar-linkage.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Administrative Officer (S3) — full · Class Teacher (S3) — view own class · Principal (S6) — full

---

## 1. Purpose

Manages the government-mandated linkage of two national identity systems for students:

**APAAR ID (Academic Bank of Credits — ABCs):** A unique 12-digit academic identity number for every student in India, introduced under NEP 2020. APAAR ID is seeded with Aadhaar (for consent-based linkage) and enables:
- Academic credit transfer across schools and colleges
- DigiLocker storage of academic records
- Government scholarship eligibility verification
- Seamless school transfer (student's academic history moves with the ID)
- Integration with UDISE+ for accurate national student census

**Aadhaar Seeding:** Linking the student's Aadhaar with the school's student record for:
- RTE reimbursement claims (government verifies per-student)
- PM Scholarship, ST Pre-Matric/Post-Matric scholarship applications
- CBSE board exam registration (Aadhaar-verified name on hall ticket)
- DigiLocker document access

**DPDPA 2023 compliance:** Aadhaar linkage requires explicit written/digital consent from parent/guardian. Schools must maintain consent records.

---

## 2. Page Layout

### 2.1 Header
```
APAAR & Aadhaar Linkage                       [Bulk Upload APAAR IDs]  [Generate Consent Forms]  [Export]
Class: [All ▼]  |  Year: 2026–27
APAAR IDs Registered: 312 / 380 (82%)  ·  Aadhaar Linked: 354 / 380 (93%)
Consent Collected: 354  ·  Consent Pending: 26
```

### 2.2 Class-wise Summary
| Class | Students | APAAR Registered | Aadhaar Linked | Consent Obtained | Pending |
|---|---|---|---|---|---|
| Nursery | 40 | 32 | 38 | 38 | 2 |
| LKG | 38 | 30 | 36 | 36 | 2 |
| Class I | 41 | 35 | 39 | 39 | 2 |
| ... | | | | | |
| Class XI | 76 | 58 | 72 | 72 | 4 |
| Class XII | 72 | 62 | 68 | 68 | 4 |

---

## 3. Student List View (per class)

```
Class XI-A — 38 students

Roll  Name             APAAR ID              Aadhaar Seeded  Consent  Status
01    Anjali Das       AP2026001234567890    ✅               ✅       ✅ Complete
02    Arjun Sharma     AP2026001234567891    ✅               ✅       ✅ Complete
03    Priya Venkat     —                     ✅               ✅       ⚠️ APAAR pending
04    Rohit Kumar      AP2026001234567892    ⬜ Not linked    ✅       ⚠️ Aadhaar not seeded
05    Suresh M.        —                     ⬜               ⬜       ❌ Not started
```

---

## 4. APAAR ID Registration

### 4.1 Single Registration
Clicking a student row → APAAR registration drawer:

```
Arjun Sharma  |  STU-0001187  |  Class XI-A

──── APAAR Registration ─────────────────────────
Step 1: Consent
  Parent/Guardian Consent:  ✅ Collected (Digital — 25 Mar 2026)
  Consent Reference: CST/2026/1187

Step 2: Aadhaar Verification
  Aadhaar No. (masked): XXXX XXXX 4521
  Name on Aadhaar: ARJUN SHARMA RAJESH
  Name in School Record: Arjun Sharma
  Match: ⚠️ Partial match — middle name difference
  → Action: [Override — names are same student]  [Request Aadhaar correction]

Step 3: APAAR ID Assigned
  APAAR ID: AP2026001234567891
  DigiLocker linked: ✅
  Issued: 25 Mar 2026

[Update Profile]  [Send APAAR ID to Parent via WhatsApp]
```

### 4.2 Bulk APAAR ID Upload
[Bulk Upload APAAR IDs] → for schools receiving a bulk assignment file from the state's APAAR implementation agency:
- Upload CSV: `student_apaar_bulk.csv` (columns: student_id or aadhaar, apaar_id)
- System validates: APAAR format (12 digits), student match, no duplicates
- Preview conflicts before committing

---

## 5. Consent Management

### 5.1 Consent Form Generation
[Generate Consent Forms] → generates class-wise consent forms:

```
AADHAAR / APAAR CONSENT FORM
[School Name] — [UDISE Code]

I, [Parent Name], parent/guardian of [Student Name] (Roll No. [X], Class [X]),
hereby give consent for:

☑ Linking my child's Aadhaar number with the school's EduForge student record system
☑ Registration of my child's APAAR Academic Identity (Academic Bank of Credits)
☑ Sharing anonymized academic records with UDISE+ (National Education Census)
☑ Access to mark sheets/certificates via DigiLocker (linked to APAAR ID)

I understand this information will be protected under the DPDPA 2023.
I can withdraw consent at any time by contacting the school office.

Parent Signature: ___________  Date: ___________
School Use Only: Collected by ___  Date: ___  Reference: ___
```

- Bulk generation: one form per student; download as multi-page PDF
- After physical collection, Admin Officer marks consent collected per student

### 5.2 Digital Consent (via Parent App)
If parent app module is enabled:
- Consent sent via in-app notification
- Parent reviews and taps [Give Consent] — logged with timestamp and device info

---

## 6. DigiLocker Integration

If APAAR ID and Aadhaar are linked:
- School can push academic documents to student's DigiLocker:
  - Report cards (from B-19)
  - Mark sheets (board results)
  - Transfer certificates (from C-13)
  - Participation certificates (from B-25 CCA)

[Push to DigiLocker] button (per document or bulk) — calls DigiLocker API.

Status shown:
```
DigiLocker Status — Arjun Sharma
  Report Card 2025–26:    ✅ Pushed (25 Jun 2026)
  Class X Mark Sheet:     ✅ Pushed (10 Jun 2026)
  TC:                     ⬜ Not pushed (TC not yet issued)
```

---

## 7. Aadhaar Name Mismatch Report

[Export] → includes:

**Name Mismatch Students:**
| Student | Class | School Name | Aadhaar Name | Mismatch Type | Action |
|---|---|---|---|---|---|
| Arjun Sharma | XI-A | Arjun Sharma | ARJUN SHARMA RAJESH | Middle name | Override / Correction |
| Priya V. | XI-B | Priya Venkata | PRIYA VENKATARAMAN | Short form | Override / Correction |

Schools must resolve all mismatches before CBSE board exam registration (B-33) — board exam hall ticket name = Aadhaar name.

---

## 8. APAAR Compliance Report

Required for state education department:
```
APAAR Registration Status — [School Name] — [UDISE Code]
As of 26 Mar 2026

Total Students: 380
APAAR Registered: 312 (82%)
Aadhaar Linked: 354 (93%)
Consent Collected: 354 (93%)

Class-wise breakdown: [table]

Submitted to: State APAAR Implementation Agency
Submitted by: [Principal Name]
Date: [Date]
```

---

## 9. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/students/apaar/?class_id={id}` | APAAR/Aadhaar linkage status |
| 2 | `PATCH` | `/api/v1/school/{id}/students/{student_id}/apaar/` | Update APAAR ID |
| 3 | `PATCH` | `/api/v1/school/{id}/students/{student_id}/aadhaar/link/` | Mark Aadhaar as seeded |
| 4 | `POST` | `/api/v1/school/{id}/students/apaar/bulk-upload/` | Bulk APAAR ID upload |
| 5 | `POST` | `/api/v1/school/{id}/students/{student_id}/consent/` | Record consent |
| 6 | `GET` | `/api/v1/school/{id}/students/apaar/consent-forms/?class_id={id}` | Generate consent form PDFs |
| 7 | `POST` | `/api/v1/school/{id}/students/{student_id}/digilocker/push/` | Push document to DigiLocker |
| 8 | `GET` | `/api/v1/school/{id}/students/apaar/mismatch-report/` | Aadhaar name mismatch list |
| 9 | `GET` | `/api/v1/school/{id}/students/apaar/compliance-report/` | APAAR compliance report |

---

## 10. Business Rules

- APAAR registration without parent consent is prohibited under DPDPA 2023 — the system enforces this by blocking APAAR registration if consent is not marked as collected
- Aadhaar numbers are stored AES-256 encrypted; only decrypted during DigiLocker push operations (server-side, never sent to browser)
- Name mismatches are flagged but can be overridden by Principal with a reason note — override log is retained for audit
- APAAR IDs, once assigned, are nationally unique and immutable — the school records the ID assigned by the government; it does not generate the ID
- If a student transfers to another school, their APAAR ID follows them — the new school just links to the same APAAR ID
- DigiLocker integration requires the school to be registered with DigiLocker Issuer System — if not registered, push buttons are hidden with a configuration note

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division C*
