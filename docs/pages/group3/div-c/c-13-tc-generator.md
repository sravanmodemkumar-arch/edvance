# C-13 — Transfer Certificate Generator

> **URL:** `/school/students/tc/`
> **File:** `c-13-tc-generator.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Administrative Officer (S3) — draft + issue · Principal (S6) — sign + issue

---

## 1. Purpose

Generates Transfer Certificates (TC) for students leaving the school. TC is one of the most legally important documents a school issues — it is the student's proof of having studied at the school, and any new school they join must collect and retain the original TC. CBSE affiliation regulations mandate a specific TC format. Issues with TC (wrong date, wrong class, name mismatch, missing seal) can prevent a student from joining a new school or appearing for competitive exams.

Every TC issued must be logged sequentially in the TC Issue Register — a mandatory school record. CBSE inspectors check: (a) sequential TC numbering with no unexplained gaps, (b) TC register has all issued TCs, (c) no TC has been issued without Principal signature.

In Indian schools, TC is needed:
- When a student transfers to another school
- When a Class XII student applies to college (many colleges require original TC + pass certificate)
- When a student takes up a job (some employers still ask for TC)
- For passport application
- For admission to NDA, police, armed forces (require original school TC)

Schools issue 20–50 TCs per year on average; large schools issue 80–100.

---

## 2. Page Layout

### 2.1 Header
```
Transfer Certificate Register — 2025–26      [+ Issue New TC]  [Export TC Register]
TC Issued This Year: 18
Pending Signature: 2  ·  Issued (Collected by Parent): 14  ·  Issued (Uncollected): 2  ·  Duplicate: 1
```

### 2.2 TC Register Table
| TC No. | Student | Class | Issue Date | Parent Collected | TC Status | Remarks |
|---|---|---|---|---|---|---|
| TC/2026/018 | Priya Das | VIII-A | 22 Mar 2026 | ✅ 24 Mar 2026 | Collected | — |
| TC/2026/017 | Suresh K. | X-B | 20 Mar 2026 | ⬜ — | Issued/Uncollected | Father on travel |
| TC/2026/016 | Ravi M. | XII-A | 10 Jun 2026 | ✅ 10 Jun 2026 | Collected | Post-board |
| TC/2026/001D | Arjun P. | IX-A | 5 Feb 2026 | ✅ 5 Feb 2026 | Duplicate | Original lost — ₹200 duplicate fee |

---

## 3. Issue New TC — Prerequisite Check

[+ Issue New TC] → first shows prerequisite check:

```
Prerequisite Check for TC Issuance:

Step 1: Withdrawal recorded?
  Priya Das — Withdrawal W-2026-018 ✅ (20 Mar 2026)

Step 2: Fee account cleared?
  Outstanding: ₹0 ✅

Step 3: Documents on record?
  Original TC from previous school: ✅ (filed)
  Photo on record: ✅

Step 4: Principal signature available?
  Active Principal: Ms. Kavitha (Principal) ✅

All prerequisites met. [Proceed to Generate TC]
```

If any step fails, the process is blocked with the required action.

---

## 4. TC Form — Data Entry

Most fields auto-populated from student profile (C-08); Admin Officer reviews and confirms:

| Field | Auto-filled? | Value | CBSE Requirement |
|---|---|---|---|
| TC Number | Auto (sequential) | TC/2026/018 | Sequential, unique |
| School Name | Auto | [School Name] | |
| School CBSE Affiliation No. | Auto | AP2000123 | |
| School Address | Auto | | |
| Student Name | Auto from C-08 | Priya Das | As per birth certificate |
| Father's Name | Auto | Mr. Rajan Das | |
| Mother's Name | Auto | Mrs. Sulochana Das | |
| Date of Birth | Auto | 14 Aug 2012 | In words also |
| Nationality | Auto | Indian | |
| Category | Auto | SC | CBSE TC includes category |
| Aadhaar No. | Auto (masked) | XXXX XXXX 4521 | Optional but recommended |
| Class Last Attended | Manual (confirm) | VIII (Eight) | In words |
| Section | Auto | A | |
| Academic Year | Auto | 2025–26 | |
| Date of Admission to School | Auto from enrollment | 5 Apr 2021 | |
| Date of Leaving School | From C-12 | 20 Mar 2026 | |
| Reason for Leaving | From C-12 | Transfer — Family Relocation | |
| Whether Failed Any Class | Auto from history | No | |
| Last Annual Exam Appeared | Auto | Class VII — 2024–25 | |
| Result of Last Exam | Auto from B-18 | Passed | |
| Class Qualified for | Auto (computed) | Class IX | Next class after last passed |
| General Conduct | Manual | Good | |
| Whether NCC/Scout/Guide | Manual | No | |
| Any Dues Outstanding | Auto | No | |
| Date of Issue of TC | Auto | 22 Mar 2026 | |
| Remarks | Manual | Shift to Bengaluru | Optional |

---

## 5. TC Preview

Before generating the PDF, the Admin Officer sees a preview:

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│               [SCHOOL LOGO]           TRANSFER CERTIFICATE                              │
│                          [SCHOOL NAME, ADDRESS, PHONE]                                  │
│               CBSE Affiliation No.: AP2000123  |  UDISE Code: 28030600101              │
│                                                                                         │
│  TC No.: TC/2026/018                                          Date: 22 March 2026       │
│                                                                                         │
│  1. Name of Student:       PRIYA DAS                                                   │
│  2. Mother's Name:         SULOCHANA DAS                                                │
│  3. Father's Name:         RAJAN DAS                                                    │
│  4. Date of Birth:         14-08-2012  (Fourteen August Two Thousand Twelve)            │
│  5. Nationality:           Indian                                                       │
│  6. Category:              SC                                                           │
│  7. Date of Admission:     05-04-2021                                                   │
│  8. Class in which admitted: Class V                                                    │
│  9. Class Last Attended:   Class VIII  (Eight)                                          │
│  10. Section:              A                                                             │
│  11. Year:                 2025–26                                                      │
│  12. Whether failed: No                                                                 │
│  13. Last Annual Exam Appeared: Class VII (2024–25)                                     │
│  14. Result: Pass                                                                       │
│  15. Qualified for admission to: Class IX                                               │
│  16. General Conduct: Good                                                              │
│  17. Date of leaving: 20-03-2026                                                        │
│  18. Reason for leaving: Family Relocation                                              │
│  19. Dues outstanding: No                                                               │
│  20. Any other remarks: Family relocating to Bengaluru                                  │
│                                                                                         │
│                                              ____________________________               │
│                                              Principal / Head of Institution            │
│                                              [School Seal]                              │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

[Generate TC PDF] → produces A4 PDF stored in R2 + downloaded.

---

## 6. Principal Signature

The TC PDF has a signature placeholder. Two options:
1. **Physical sign:** Print the TC, Principal signs + stamps, then scan or distribute as printed
2. **Digital signature (if configured):** Principal uses digital signature configured in A-35; PDF is digitally signed (DSC-compliant)

Most Indian schools currently use physical signatures; digital TC is emerging.

When Principal confirms TC is signed:
[Mark as Signed by Principal] → TC status updates to "Ready for Collection".

---

## 7. TC Dispatch (Parent Collection)

```
Dispatch Record — TC/2026/018

TC Generated:  22 Mar 2026 by Meera (Admin Officer)
Principal Signed: 22 Mar 2026 (physical)
Collected by: Rajan Das (Father)  ·  Date: 24 Mar 2026
ID Verified: ✅ Aadhaar card checked
Signature of Receiver: [captured]
```

If TC is to be sent by post (rare but happens for distant relocations):
```
Dispatched by Registered Post:  Ref: AP2026/REG/04821  ·  Date: 22 Mar 2026
```

---

## 8. Duplicate TC

If original TC is lost, a duplicate can be issued:
- Fee: School-configured (typically ₹100–₹500)
- TC number: Same base number + "D" suffix (TC/2026/001D)
- Header shows "DUPLICATE — ISSUED AGAINST APPLICATION DATED [Date]"
- Fee collected logged

---

## 9. TC Register Export

[Export TC Register] → CBSE prescribed format:

```
TC ISSUE REGISTER — 2025–26
[School Name] | Affiliation: AP2000123

TC No.        Student Name    Class  Date of Issue  Date of Collect.  Collected By  Remarks
TC/2026/001   Arun Kumar      XI     5 Apr 2025     5 Apr 2025        Father        Post-board XI
TC/2026/001D  Arun Kumar      XI     5 Feb 2026     5 Feb 2026        Father        Duplicate — original lost
...
TC/2026/018   Priya Das       VIII   22 Mar 2026    24 Mar 2026       Father        Relocation
```

---

## 10. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/students/tc/?year={year}` | TC register list |
| 2 | `POST` | `/api/v1/school/{id}/students/tc/` | Initiate TC generation |
| 3 | `GET` | `/api/v1/school/{id}/students/tc/{tc_id}/` | TC detail |
| 4 | `GET` | `/api/v1/school/{id}/students/tc/{tc_id}/pdf/` | Generate/fetch TC PDF |
| 5 | `PATCH` | `/api/v1/school/{id}/students/tc/{tc_id}/sign/` | Mark TC as principal-signed |
| 6 | `PATCH` | `/api/v1/school/{id}/students/tc/{tc_id}/dispatch/` | Record collection/dispatch |
| 7 | `POST` | `/api/v1/school/{id}/students/tc/{tc_id}/duplicate/` | Issue duplicate TC |
| 8 | `GET` | `/api/v1/school/{id}/students/tc/export/?year={year}` | Export TC register PDF |

---

## 11. Business Rules

- TC can only be generated if the student is recorded as withdrawn in C-12 — no TC for currently active students (active student TC would allow double enrollment)
- TC numbering is sequential, auto-incremented — Admin Officer cannot manually choose TC number; gaps in sequence (from voided TCs) must be noted in the register
- TC PDF is stored permanently in R2 (not deleted even after parent collects) — CBSE may ask for TC copies during inspection
- TC is NOT issued for graduating Class XII students (they get a Pass Certificate from CBSE); TC is for mid-school transfers and junior classes only — the system enforces this
- A school cannot refuse to issue TC even if fees are outstanding — under RTE Act, refusal to issue TC is grounds for de-affiliation; the system allows TC issuance despite dues but requires Principal override and logs it prominently

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division C*
