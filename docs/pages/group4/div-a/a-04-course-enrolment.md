# A-04 — Course Enrolment & Electives

> **URL:** `/college/students/enrolment/`
> **File:** `a-04-course-enrolment.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Registrar (S4) · Academic Coordinator (S4) · Faculty Advisor (S3) · Student (S1) — self-enrolment for electives

---

## 1. Purpose

Each semester, students must enrol in their courses. For core/mandatory courses, enrolment is automatic. For electives (which expand significantly under NEP 2020's choice-based and multi-disciplinary approach), students choose from a menu. This module manages:
- Mandatory course registration (auto-enrolment by programme)
- Elective registration (student choice, seat caps)
- Open elective / Value-added courses (inter-department)
- Credit accounting (against graduation requirement)
- Fee implications (if electives carry additional cost)
- Pre-requisite enforcement (cannot enrol in Subject B without passing Subject A)

---

## 2. Course Registration — Student View

```
COURSE REGISTRATION — Aakash Sharma (GCEH-2026-CSE-0041)
Semester II — Jan–May 2027

MANDATORY COURSES (auto-enrolled):
  Code      Course                         Credits  Faculty
  MA201     Engineering Mathematics II     4        Dr. R. Patel
  CS201     Data Structures & Algorithms   4        Dr. Anita K.
  CS203     Digital Logic Design           3        Mr. Suresh V.
  CS205     Computer Organisation          3        Dr. Ramesh M.
  EE201     Basic Electrical Engineering   3        Mr. Pradeep T.
  HS201     English Communication Skills   2        Ms. Neeraja R.
  CS207     DS Lab                         1.5      Dr. Anita K. (Lab)
  CS209     Digital Logic Lab              1.5      Mr. Suresh V. (Lab)
  ───────────────────────────────────────────────────────────────
  Mandatory total: 22 credits

ELECTIVE REGISTRATION (choose 1 from list):
  Open Elective Group OE-2 (2 credits, inter-department)
  Available options:
    ○ OE201  Environmental Science          (Seats: 38/60 filled)
    ● OE203  Entrepreneurship & Innovation  (Seats: 42/50 filled) ← SELECTED
    ○ OE205  Indian Constitution & Society  (Seats: 20/60 filled)
    ○ OE207  Psychology of Learning        (Seats: 15/40 filled)

  [Register for OE203] ← Confirm selection

TOTAL CREDITS REGISTERED: 24 / 24 required ✅

[Confirm Registration]  [Fee implications: ₹0 for selected courses]
Registration deadline: 5 January 2027
```

---

## 3. Elective Seat Management

```
ELECTIVE SEAT MANAGEMENT — Semester II 2026–27
(Registrar view)

Course    Title                        Capacity  Enrolled  Waitlist  Status
OE201     Environmental Science        60        38        0         Open
OE203     Entrepreneurship & Innovation 50       43        3         🟡 Near full
OE205     Indian Constitution          60        20        0         Open
OE207     Psychology of Learning       40        15        0         Open
PE201     Constitution Law (audit)     30        12        0         Open
PE203     Yoga & Wellness              25        18        0         Open

OE203 WAITLIST:
  3 students on waitlist → If a registered student drops before deadline (5 Jan),
  waitlisted student is auto-enrolled and notified.

SEAT CAPS RATIONALE:
  Room capacity / faculty bandwidth:
    OE203 (50): Seminar room (capacity 55); instructor comfort with 50 max
  Seats NOT artificially restricted — only physical/pedagogical limits enforced
```

---

## 4. Pre-requisite Enforcement

```
PRE-REQUISITE CHECK — Semester III Registration (illustrative)

CS301 Advanced Algorithms:
  Pre-requisite: CS201 Data Structures & Algorithms (Semester II)
  Aakash's status (after Sem II): Passed with SGPA 7.8 → CS201 credited ✅
  → CS301 registration: ALLOWED ✅

CS303 Database Management:
  Pre-requisite: CS201 (passed) ✅ + CS203 (passed) ✅
  → CS303 registration: ALLOWED ✅

CS305 Computer Networks:
  Pre-requisite: CS201 (passed) ✅ + EE201 (passed) ✅
  → CS305 registration: ALLOWED ✅

If a student has a backlog (failed) in a pre-requisite:
  CS301 blocked — "CS201 backlog pending; register CS201 backlog exam first"
  [Backlog re-exam registration link → A-06]
```

---

## 5. NEP 2020 — Multi-Exit & Credit Framework

```
NEP 2020 DEGREE STRUCTURE (4-Year UG with multiple exits)

EXIT OPTIONS:
  After Year 1 (2 semesters): Certificate (if ≥40 credits + exit exam) ← Minor exit
  After Year 2 (4 semesters): Diploma (if ≥80 credits + exit exam)
  After Year 3 (6 semesters): B.Tech (Honours standard — 120 credits)
  After Year 4 (8 semesters): B.Tech (Honours with Research — 160 credits)

CREDIT REQUIREMENTS (JNTU Hyderabad B.Tech 2026 scheme):
  Programme core:        80 credits
  Open electives:        20 credits
  Value-added courses:    8 credits
  Internship/project:    12 credits
  Research (Year 4 only): 20 credits (Honours with Research)
  ───────────────────────────────────────────
  Year 4 exit total:    160 credits

CURRENT STATUS (Aakash — After 1 semester):
  Credits earned:   22 (Semester I — results pending)
  Credits planned (Sem II): 24
  Running total (projected): 46 credits after Sem II
  Year 2 exit (Diploma): 80 credits — on track ✅
```

---

## 6. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/college/{id}/enrolment/courses/?student={id}&semester={sem}` | Available courses for registration |
| 2 | `POST` | `/api/v1/college/{id}/enrolment/register/` | Register courses (student or batch) |
| 3 | `DELETE` | `/api/v1/college/{id}/enrolment/{enrolment_id}/` | Drop course (before deadline) |
| 4 | `GET` | `/api/v1/college/{id}/enrolment/electives/seats/` | Elective seat status |
| 5 | `GET` | `/api/v1/college/{id}/enrolment/prerequisites/?student={id}&course={code}` | Check prerequisite eligibility |
| 6 | `GET` | `/api/v1/college/{id}/enrolment/credit-summary/?student={id}` | Credit accumulation summary |

---

## 7. Business Rules

- Pre-requisite enforcement is hard by default — a student with a backlog in a pre-requisite course cannot register for the dependent course; the faculty advisor can override in documented exceptional cases (e.g., student has attempted the pre-req 3 times but needs to progress for other reasons); all overrides are logged with reason
- Elective seat caps are set by the department based on room capacity and faculty-student ratio; the system does NOT over-allocate beyond cap; waitlisting is automatic and position is first-come-first-served within the registration window
- Under NEP 2020, students can exit early (Certificate/Diploma); a student who intends to exit must formally notify the Registrar; the system generates the appropriate credential (Certificate or Diploma) with the earned credits for ABC upload; this exit cannot be undone — a student who exits with a Diploma and wants to return later is treated as a fresh lateral entry
- Course registration without fee payment (if semester fee is pending) is blocked after a 7-day grace period from semester start; the Registrar can extend for individual hardship cases with documentation

---

*Last updated: 2026-03-27 · Group 4 — College Portal · Division A*
