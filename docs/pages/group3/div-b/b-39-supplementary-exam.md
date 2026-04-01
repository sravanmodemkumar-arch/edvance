# B-39 — Supplementary / Compartment Exam Manager

> **URL:** `/school/academic/exams/supplementary/`
> **File:** `b-39-supplementary-exam.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Roles:** Exam Cell Head (S4) — full · Principal (S6) — approve · HOD (S4) — read

---

## 1. Purpose

Manages the supplementary/compartment exam cycle — the second chance exam offered to students who narrowly failed in the annual exam. For CBSE-affiliated schools, Class X and XII compartment exams are conducted by CBSE in July. For other classes (VI–IX, XI), the school may conduct its own supplementary exam to give students a chance to avoid detention. This page manages both:
1. **School supplementary exam** (Classes VI–IX, XI) — school-conducted, typically in May–June
2. **CBSE compartment exam** (Classes X, XII) — CBSE-conducted, July; school manages registration and logistics

---

## 2. Page Layout

### 2.1 Header
```
Supplementary / Compartment Exam Manager          [+ Create Supplementary Exam]
Academic Year: 2025–26  ·  Post-Annual Exam
Eligible Students (fail/compartment): 48  ·  Registered: 36  ·  Exam Date: May–Jul 2026
```

---

## 3. Eligibility List

Students identified from Annual Exam result computation (B-18):

| Student | Class | Result Type | Failed Subjects | Score | Eligible For |
|---|---|---|---|---|---|
| Deepak M | XI-A | Compartment | Chemistry (29/80) | 1 subject fail | School Supplementary |
| Ravi P | IX-C | Fail | Mathematics (25), Hindi (28) | 2 subjects fail | School Supplementary |
| Anand T | VII-B | Fail | Science (24/80) | 1 subject fail | School Supplementary |
| Suresh K | X-A | Compartment (CBSE) | Hindi (29/80) | 1 subject fail | CBSE Compartment (July) |
| Priya L | XII-B | Compartment (CBSE) | Mathematics (30/70) | 1 subject fail | CBSE Compartment (July) |
| Vijay K | VI-A | Fail | Mathematics (20), Sci (22) | 2 subjects fail | School Supplementary |

**CBSE compartment eligibility:** Class X/XII — fail in 1–2 subjects (3+ subjects = full fail; no compartment).
**School supplementary:** Classes VI–XI — school policy (typically fail in 1–2 subjects).

---

## 4. School Supplementary Exam (Classes VI–XI)

[+ Create Supplementary Exam] → setup form:

| Field | Value |
|---|---|
| Exam Name | "Annual Supplementary Exam 2025–26" |
| Classes | VI–XI (only failed students from those classes) |
| Date Range | 10–15 May 2026 |
| Max Marks | Same as main exam (80) or reduced (40) — school policy |
| Subjects | Only failed subjects per student |
| Pass Criteria | Same as main exam (33%) |

Registration:
- System auto-generates eligible list
- HOD and Class Teacher confirm which students are registered
- Parent acknowledgement required (auto-WhatsApp sent)

Workflow: Same as regular exam — hall tickets, seating (small group), marks entry, result.

**If student passes supplementary:**
- Promoted to next class
- "Passed in Supplementary" noted on report card (visible distinction)
- Result published in B-18/B-20

**If student fails supplementary:**
- Retained in same class (detained)
- Detention register updated
- Parent meeting mandatory

---

## 5. CBSE Compartment Exam (Classes X, XII)

For Classes X and XII, compartment is managed by CBSE. School's responsibilities:

### 5.1 Registration

| Step | Task | Deadline | Status |
|---|---|---|---|
| 1 | Identify compartment students from B-18 | As soon as results declared (May) | ✅ |
| 2 | Submit compartment registration to CBSE (Saras portal) | Per CBSE notification (typically May–Jun) | ⬜ |
| 3 | Pay CBSE compartment registration fee | Same deadline | ⬜ |
| 4 | CBSE assigns exam date and centre | June notification | ⬜ |
| 5 | CBSE sends admit cards | 2 weeks before exam | ⬜ |
| 6 | Distribute admit cards to students | Immediately | ⬜ |

### 5.2 Compartment Students Tracking

| Student | Class | Subject | Registration No | CBSE Admit Card | Exam Date | Result |
|---|---|---|---|---|---|---|
| Suresh K | X | Hindi | COMP/X/2026/AP/00234 | [Download] | 15 Jul 2026 | ⏳ Pending |
| Priya L | XII | Mathematics | COMP/XII/2026/AP/00235 | [Download] | 18 Jul 2026 | ⏳ Pending |

### 5.3 Result Recording

When CBSE declares compartment results (typically August):
- Exam Cell Head enters CBSE-declared result in EduForge
- Student's status updated: Pass → Promoted; Fail → Detained (or eligible for improvement attempt)
- Parent notified via WhatsApp

---

## 6. Detention Register

Students who failed both annual exam and supplementary/compartment:

| Student | Class | Academic Year | Detention Reason | Repeat? |
|---|---|---|---|---|
| Ravi P | IX-C | 2025–26 | Failed in 2+ subjects; supplementary also failed | No (first time) |
| Anand T | VII-B | 2025–26 | Failed Science; supplementary failed | Yes (2nd year in VII) |

**Note on NEP 2020:** NEP 2020 recommends against detention in Classes I–V. Classes VI–VIII detention policies vary by state (some states have passed No-Detention orders). CBSE currently allows detention from Class IX.

Students detained for 2 consecutive years in same class → counsellor referral + parent meeting with Principal.

---

## 7. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/supplementary/?year={year}` | Eligibility list + exam status |
| 2 | `POST` | `/api/v1/school/{id}/supplementary/school/` | Create school supplementary exam |
| 3 | `PATCH` | `/api/v1/school/{id}/supplementary/school/{exam_id}/register/` | Register students |
| 4 | `GET` | `/api/v1/school/{id}/supplementary/cbse/?year={year}` | CBSE compartment student list |
| 5 | `POST` | `/api/v1/school/{id}/supplementary/cbse/log-registration/` | Log CBSE registration |
| 6 | `PATCH` | `/api/v1/school/{id}/supplementary/cbse/{student_id}/result/` | Enter CBSE compartment result |
| 7 | `GET` | `/api/v1/school/{id}/supplementary/detention-register/` | Detention register |
| 8 | `GET` | `/api/v1/school/{id}/supplementary/export/` | Export supplementary register |

---

## 8. Business Rules

- CBSE compartment is for Classes X and XII only; school supplementary is for Classes VI–XI (Class XII supplementary students must use CBSE compartment process)
- Passing marks for school supplementary are the same as the regular exam — there is no "lower threshold" for the second attempt
- A student who passes in the supplementary exam is promoted but the supplementary pass is noted on records; it does not affect CBSE marks sheet (which shows the main exam marks)
- NEP 2020 no-detention policy: Schools in states that mandate no-detention (Classes I–VIII) must configure this in school settings; the system will then not generate a detention outcome for those class levels

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division B*
