# A-03 — Student Directory & Profile

> **URL:** `/college/students/directory/`
> **File:** `a-03-student-directory.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Registrar (S4) — full access · Faculty (S3) — own department/class · Student (S1) — own profile · Dean of Students (S5) — full read

---

## 1. Purpose

Maintains the authoritative record of every enrolled student — profile, admission details, academic history, category documents, contact information, and current status. In a college context, the student directory also tracks programme-level data (semester, SGPA, backlogs, academic standing) and is the source of truth for university registration.

---

## 2. Student Profile

```
STUDENT PROFILE — GREENFIELDS COLLEGE OF ENGINEERING

Student ID: GCEH-2026-CSE-0041
Name: Mr. Aakash Sharma
Programme: B.Tech Computer Science & Engineering
Batch: 2026–30  |  Current Semester: I (2026–27 Odd semester)
Category: OBC-NCL  |  Admission type: Management quota
Section: CSE-A  |  Roll No.: 226J1A0541

PERSONAL DETAILS:
  Date of Birth: 14 July 2007 (18 yrs 8 months)
  Gender: Male
  Aadhaar: XXXX-XXXX-1234 (masked — original verified on admission)
  Blood Group: B+ (from admission form)
  PwD: No  |  First-generation college student: No

CONTACT:
  Local address (Hyderabad): [Hostel Room 214 — if hostel; or local address]
  Permanent address: [From admission form]
  Parent mobile: +91 98XXXXXX (Mrs. Sharma — mother — primary contact)
  Student mobile: +91 99XXXXXX
  Emergency contact: Same as parent
  College email: 226j1a0541@gceh.ac.in [auto-provisioned on admission]

QUALIFYING EXAM:
  Class XII: CBSE 2025 — PCM 94.2% ✅
  JEE Main Percentile: 88.4 | Registration No.: 25XXXXXXXX

CATEGORY DOCUMENTS:
  OBC-NCL certificate: Verified ✅ (MRO Secunderabad, 15 Mar 2025)
  Income certificate: ₹4,20,000 (verified ✅)
  Category document expiry: None (caste certificates don't expire; income re-verified annually for NCL)

FINANCIAL AID:
  Scholarship: NSP OBC Scholarship (applied — NSP-2026-OBC-XXXXXX) — pending
  Fee concession: None (management quota — full fee)
  Loan: None

STATUS: Active | Expected graduation: April 2030
```

---

## 3. Academic Standing

```
ACADEMIC STANDING — Aakash Sharma (GCEH-2026-CSE-0041)
(Updated each semester after results)

Semester  SGPA   CGPA   Backlogs  Academic Standing
I         —      —      —         In progress (exams: Dec 2026)
[Previous semesters — not applicable (freshmen)]

ATTENDANCE ALERT:
  Current semester attendance (Odd 2026–27): 3 weeks in
  Attendance so far: 92% (above 75% UGC minimum ✅)
  Subjects below 75% individual:
    None ✅

ACADEMIC BANK OF CREDITS (ABC — NEP 2020):
  ABC ID: ABC-2026-GCEH-0041
  Credits registered this semester: 22 (out of 24 planned)
  [ABC account active — linked to NAD/Digilocker]
```

---

## 4. ID Card & Documents

```
STUDENT ID CARD — GCEH-2026-CSE-0041
  ┌────────────────────────────────────────────────┐
  │ GREENFIELDS COLLEGE OF ENGINEERING             │
  │ AICTE Approved | Affiliated: JNTU Hyderabad    │
  │                                                │
  │ [PHOTO]  Aakash Sharma                         │
  │          B.Tech CSE — Batch 2026–30            │
  │          ID: GCEH-2026-CSE-0041                │
  │          DOB: 14 Jul 2007                      │
  │          Blood Group: B+                       │
  │          Emergency: +91 98XXXXXX               │
  │                                                │
  │  [QR Code — scans to verify ID authenticity]  │
  │  Valid: June 2026 – April 2030                 │
  └────────────────────────────────────────────────┘

[Download ID Card PDF]  [Print ID Card]  [Regenerate if lost]
```

---

## 5. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/college/{id}/students/` | Student directory (with filters) |
| 2 | `GET` | `/api/v1/college/{id}/students/{student_id}/` | Student profile |
| 3 | `PATCH` | `/api/v1/college/{id}/students/{student_id}/` | Update student details |
| 4 | `GET` | `/api/v1/college/{id}/students/{student_id}/academic-standing/` | SGPA/CGPA/backlog status |
| 5 | `GET` | `/api/v1/college/{id}/students/{student_id}/id-card/pdf/` | Download ID card |
| 6 | `GET` | `/api/v1/college/{id}/students/?programme={prog}&semester={sem}&category={cat}` | Filtered directory |

---

## 6. Business Rules

- Student enrollment number (Roll No.) format must follow the affiliating university's specification; JNTU Hyderabad uses the format YY-institution code-programme code-serial (e.g., 226J1A0541 = 22 batch, 6J1A = GCEH CSE code, 0541 = serial); a wrong format causes problems at university registration and results upload
- Category document validity: Caste certificates (SC/ST/OBC) are lifelong and do not expire; however, "non-creamy layer" status (for OBC-NCL) must be re-verified annually by checking income — a student admitted as OBC-NCL who crosses the creamy layer threshold during their study may become ineligible for OBC fee benefits (but not expelled)
- The college email (auto-provisioned on admission day 1) is the official communication channel; all notices, circulars, hall tickets, and results are sent here; students are responsible for monitoring their college email; this is stated in the admission letter
- ABC (Academic Bank of Credits) account creation is mandatory under NEP 2020 for all students enrolled in degree programmes; the NAD (National Academic Depository) integration creates the ABC ID at enrolment; NAAC accreditation now evaluates whether the institution has implemented ABC

---

*Last updated: 2026-03-27 · Group 4 — College Portal · Division A*
