# L-01 — Staff Directory

> **URL:** `/school/hr/staff/`
> **File:** `l-01-staff-directory.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** HR Officer (S4) — full edit · Principal (S6) — full view · Class Teacher (S3) — view own record only + contact directory · Administrative Officer (S3) — view

---

## 1. Purpose

Central staff directory — master record of all employees. The directory is the authoritative source for:
- Contact information (for emergency response, timetable communication)
- Qualification and role information (for CBSE affiliation compliance)
- BGV and compliance status (K-05)
- Payroll identification

Every staff member has a unique Employee ID (format: TCH-001 for teaching, NTS-001 for non-teaching, DRV-001 for drivers, ESC-001 for escorts).

---

## 2. Page Layout

### 2.1 Header

```
Staff Directory                                      [+ Add Staff]  [Export Register]
Academic Year: [2026–27 ▼]

Total staff: 87
  Teaching: 45  ·  Non-teaching: 22  ·  Transport: 11  ·  Support: 9
Active: 84  ·  On leave: 2  ·  Separated (current year): 1
New joiners this year: 4
```

### 2.2 Directory List

```
Filter: Role [All ▼]  Department [All ▼]  Status [Active ▼]

EmpID    Name              Role              Dept           Qualification  Joined      Status
TCH-001  Ms. Meena Rao     Principal         Admin          M.Ed           2 Jan 2010  Active
TCH-002  Mr. Suresh K.     Vice Principal    Admin          M.Sc, B.Ed     5 Jun 2012  Active
TCH-022  Ms. Ananya K.     Counsellor        Welfare        M.Sc Psych.    1 Jun 2022  Active
TCH-031  Ms. Geeta Sharma  Class Teacher IX-B Social Science B.A, B.Ed     10 Jul 2018 Active
TCH-040  Mr. Ravi Kumar    Physics Teacher   Science        M.Sc, B.Ed     1 Apr 2020  Active
TCH-045  Mr. Suresh Reddy  Physics Teacher   Science        M.Sc, B.Ed     20 Mar 2026 Active (new)
NTS-001  Mr. Kishore P.    Administrative O. Administration B.Com          1 Aug 2015  Active
DRV-001  Raju Kumar        Driver            Transport      12th + HMV     15 Jun 2020 Active
ESC-001  Ms. Kavitha Rao   Escort            Transport      12th           1 Apr 2021  Active
...
```

---

## 3. Staff Profile

```
Staff Profile — Ms. Geeta Sharma

Employee ID: TCH-031  ·  Joined: 10 July 2018
Role: Class Teacher (IX-B) + Subject Teacher (Social Science — Classes IX & X)
Department: Secondary — Social Science
Reporting to: HOD Social Science / Academic Coordinator

Contact:
  Official email: geeta.sharma@greenfieldsschool.edu
  Mobile: +91 9876-XXXXX (HR record — not visible to students or parents)
  Emergency contact: Husband — Mr. Ramesh Sharma — +91 9765-XXXXX

Qualifications:
  B.A. (History) — Osmania University — 2005 ✅
  B.Ed. — Hyderabad Central University — 2007 ✅
  CTET: ✅ Certificate No. CTET/2018/XXXX (valid)

Employment details:
  Type: Permanent  ·  Probation completed: 10 July 2019 ✅
  Current designation: Senior Teacher (Grade II)
  Pay band: ₹35,000–₹55,000 (school scale)
  Current basic: ₹42,000

BGV: ✅ Completed 5 July 2018 · Renewal due July 2023 → Renewed July 2023 ✅
  Next renewal: July 2028

POCSO Training: ✅ Annual (last: Jun 2025)

Leave balance (see L-03): EL: 18 days · CL: 6 days · SL: 8 days

Assigned timetable (L-12): 22 periods/week (Social Science IX-B, IX-A, X-A, X-B)
  Class Teacher: IX-B (30 students)

Recent achievements:
  Best Teacher Award — School Day 2025 ✅
  Completed Cambridge Assessment Training (IGCSE methodology) — Oct 2025 ✅

[Edit Profile]  [View Service Book (L-11)]  [View Payroll (L-04)]  [View Leave (L-03)]
```

---

## 4. Add New Staff

```
[+ Add Staff]

Employee ID: TCH-046 (auto-generated)  ·  Type: ● Teaching  ○ Non-Teaching  ○ Transport

Personal details:
  Full name: [________________________]
  Gender: ● Female  ○ Male  ○ Other
  DOB: [___]  ·  Nationality: ● Indian  ○ Other
  PAN: [________________________] (mandatory for payroll)
  Aadhaar: [________________________] (for identity verification — masked after entry)
  Contact: [+91 ___-_______]  Emergency contact: [___________] [+91 ___-_______]

Employment:
  Designation: [________________________]
  Department: [Science/English/Maths... ▼]
  Date of joining: [___]
  Employment type: ● Permanent  ○ Probationary (6 months)  ○ Contractual
  Probation end date (if probationary): [___]

Qualifications:
  Degree: [B.Sc, B.Ed ▼ or type]  University: [___]  Year: [___]
  [+ Add qualification]
  CTET/STET: ○ Yes — [Certificate No. ___]  ○ In progress  ○ Not applicable (class > VIII)

Salary (L-05):
  Pay band: [Select ▼]  Starting basic: ₹[_____]
  Bank account: [A/c No.] [IFSC] [Bank name]

BGV status: ● Not yet submitted (joining < 30 days)  ○ Submitted [receipt no.]  ○ Cleared

Documents uploaded: [Upload appointment letter, qualification certs, BGV form]

[Create Employee Record]
```

---

## 5. Contact Directory (All Staff)

```
Contact Directory — Teaching Staff
[Visible to all teaching staff for professional communication]
[Mobile numbers NOT shown — only official email and extension]

Name                  Role              Dept           Email                     Ext
Ms. Meena Rao         Principal         Admin          principal@school.edu      101
Mr. Suresh K.         Vice Principal    Admin          vp@school.edu             102
Ms. Ananya K.         Counsellor        Welfare        counsellor@school.edu     108
Ms. Geeta Sharma      CT IX-B, Social   Secondary      geeta.s@school.edu        215
Mr. Ravi Kumar        Physics           Science        ravi.k@school.edu         218
...

[Export for staff phonebook — school use only]
Note: Personal mobile numbers are in the HR record (S4+) only; this directory
  contains only official contact methods.
```

---

## 6. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/hr/staff/` | Staff directory |
| 2 | `POST` | `/api/v1/school/{id}/hr/staff/` | Add new staff |
| 3 | `GET` | `/api/v1/school/{id}/hr/staff/{staff_id}/` | Staff profile |
| 4 | `PATCH` | `/api/v1/school/{id}/hr/staff/{staff_id}/` | Update staff details |
| 5 | `GET` | `/api/v1/school/{id}/hr/staff/directory/` | Public contact directory (email/ext only) |
| 6 | `GET` | `/api/v1/school/{id}/hr/staff/export/` | Export staff register for CBSE |

---

## 7. Business Rules

- Employee IDs are permanent and never reassigned; a departed employee's ID is retired, never given to a new employee
- Aadhaar and PAN are collected for payroll/TDS compliance; Aadhaar is masked after entry (only last 4 digits visible); full Aadhaar is accessible only to the Payroll Officer and HR Officer
- Staff personal mobile numbers are not visible to students, parents, or other teachers; the public-facing contact directory uses only official emails and extension numbers
- For CBSE inspection, the staff register must show: name, designation, qualifications, date of joining, B.Ed/TET status; EduForge generates this in CBSE format on demand
- When a staff member separates (L-10), their record is moved to "inactive" but never deleted; CBSE and income tax records require retention for 7 years
- The staff directory auto-updates when timetable (L-12) changes CT assignments or role changes are made; this ensures the directory always reflects current responsibilities

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division L*
