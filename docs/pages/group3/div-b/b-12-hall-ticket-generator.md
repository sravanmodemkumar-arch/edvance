# B-12 — Hall Ticket Generator

> **URL:** `/school/academic/exams/<exam_id>/hall-tickets/`
> **File:** `b-12-hall-ticket-generator.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Exam Cell Head (S4) — full · Principal (S6) — view/approve

---

## 1. Purpose

Generates hall tickets (admit cards) for all eligible students appearing in an exam. A hall ticket is a student's official permission-to-appear document — it carries the student's name, roll number, photograph, exam schedule (which subject on which date), hall/room number, and rules for the examination. In Indian schools, hall tickets are issued for every major exam (Half-Yearly, Annual, Board practicals) and sometimes for Periodic Tests. Students are not permitted to enter the exam hall without their hall ticket. The Exam Cell Head generates them in bulk, distributes them via class teachers, and marks them as collected.

**CBSE context:** For board exams, CBSE generates the official admit card directly — schools only need to collect and distribute them (tracked in B-33). This page handles internally-generated hall tickets for school-conducted exams.

---

## 2. Page Layout

### 2.1 Header
```
Hall Ticket Generator — Annual Exam 2025–26       [Generate All]  [Download PDF Bundle]  [Distribution Status]
Exam: Annual Exam 2025–26  ·  Date Range: 1–20 Mar 2026
Eligible Students: 2,182  ·  Generated: 2,180  ·  Distributed: 1,642  ·  Pending: 540
```

---

## 3. Generation Panel

### 3.1 Pre-Generation Checklist

Before hall tickets can be generated:

| # | Check | Status |
|---|---|---|
| 1 | Exam configuration approved by Principal | ✅ Done (12 Feb) |
| 2 | Student eligibility list finalized | ✅ Done (20 Feb) |
| 3 | Seating plan generated (room + seat numbers assigned) | ✅ Done (24 Feb) |
| 4 | All student photographs uploaded in profiles | ⚠️ 12 students missing photos |
| 5 | Hall ticket template selected | ✅ Done |

**12 students without photographs:** Hall tickets can still be generated but the photo slot will be blank — these students must bring a passport photograph for manual attachment. List of students shown with [Send Reminder to Class Teacher].

### 3.2 Generate Buttons

```
[Generate All (2,182)]   — single bulk operation, runs as background task
[Generate by Class] ▼    — generates for one section at a time
  → Class VI-A (42 students)
  → Class VI-B (40 students)
  → ...

[Regenerate (Clear & Redo)] — for corrections (deletes all existing and recreates)
```

Generation runs as a background task (AWS Lambda) — progress bar shown via HTMX polling. Completion notification sent in-app.

---

## 4. Hall Ticket Contents

Each hall ticket PDF contains:

```
┌─────────────────────────────────────────────────────────────────┐
│   [SCHOOL LOGO]          ANNUAL EXAMINATION 2025–26             │
│   ABC International School, Hyderabad                           │
│   CBSE Affiliation No. 1234567                                  │
├──────────────────────────────────────────────────────────────┬──┤
│   Name:    ARJUN SHARMA                                       │  │
│   Class:   XI-A                                              │📷│
│   Roll No: 2026/XI/001                                       │  │
│   DOB:     14 Aug 2008                                        │  │
│   Mother:  Mrs. Kavitha Sharma                                │  │
├──────────────────────────────────────────────────────────────┴──┤
│   EXAMINATION SCHEDULE                                          │
│   Date        Day    Subject           Time     Hall   Seat     │
│   01 Mar 2026  Mon   English           10:00–   A-101  A12      │
│   03 Mar 2026  Wed   Mathematics       10:00–   A-101  A12      │
│   04 Mar 2026  Thu   Physics           10:00–   A-101  A12      │
│   06 Mar 2026  Sat   Chemistry         10:00–   A-101  A12      │
│   09 Mar 2026  Mon   Biology           10:00–   A-101  A12      │
│   11 Mar 2026  Wed   Computer Science  10:00–   A-101  A12      │
│   13 Mar 2026  Fri   Hindi             10:00–   A-101  A12      │
├─────────────────────────────────────────────────────────────────┤
│   Rules: 1. Bring this hall ticket to every exam.              │
│   2. No electronic devices. 3. Arrive 15 min early.           │
│   4. Students found without hall ticket may be denied entry.   │
├─────────────────────────────────────────────────────────────────┤
│   Class Teacher Signature:______   Exam Cell Head Seal & Sign  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 5. Hall Ticket Preview

[View] on any student → opens `hall-ticket-preview` drawer (480px) showing the hall ticket exactly as it will print.

From the drawer:
- [Download Single PDF]
- [Mark as Distributed] — marks this hall ticket as collected by student
- [Reprint] — if student loses hall ticket; generates duplicate stamped "DUPLICATE"

---

## 6. Student List with Distribution Status

| Roll No | Student Name | Class | Section | Generated | Distributed | Collected | Issues |
|---|---|---|---|---|---|---|---|
| 2026/XI/001 | Arjun Sharma | XI | A | ✅ | ✅ | ✅ | — |
| 2026/XI/002 | Priya Venkat | XI | A | ✅ | ✅ | ⏳ Not confirmed | — |
| 2026/XI/003 | Rahul Gupta | XI | A | ✅ | ✅ | ✅ | — |
| 2026/XI/004 | Anjali Das | XI | A | ⚠️ | — | — | Photo missing |
| 2026/IX/015 | Deepak M | IX | B | ✅ | ✅ | ✅ | — |

**Distribution workflow:**
1. Exam Cell generates PDFs
2. Class teacher downloads class bundle and distributes to students
3. Class teacher marks them as distributed (bulk action by class)
4. Student confirms receipt (via parent app or class teacher notes)

---

## 7. Download PDF Bundle

[Download PDF Bundle] → options:
- **All students (single PDF):** All 2,182 hall tickets in one 2,182-page PDF (each page = one student); print in bulk
- **By class:** One PDF per section (42 pages for Class XI-A, etc.) — given to class teachers for distribution
- **Individual:** Download one student's hall ticket

PDFs are stored in Cloudflare R2 for 30 days post-exam date; then auto-archived.

---

## 8. Duplicate Hall Ticket

When a student loses their hall ticket:
1. Class teacher or parent requests reprint via the school office
2. Exam Cell Head generates a duplicate from this page: [Reprint] button on the student row
3. Duplicate is watermarked "DUPLICATE — Reprint Date: 26 Mar 2026"
4. Original hall ticket is not invalidated
5. Reprint is logged in the audit trail

---

## 9. Template Customisation

[Hall Ticket Template] → HOD/Exam Cell Head can configure:
- School logo and letterhead
- Rules text (editable per exam)
- Fields to show/hide (e.g., hide seat number if seating is flexible)
- Language: English / Regional language (e.g., Hindi/Telugu for regional schools)
- Paper size: A4 / A5 / Half-A4 (common for hall tickets)

---

## 10. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `POST` | `/api/v1/school/{id}/exams/{exam_id}/hall-tickets/generate/` | Trigger bulk generation (async) |
| 2 | `GET` | `/api/v1/school/{id}/exams/{exam_id}/hall-tickets/status/` | Generation + distribution status |
| 3 | `GET` | `/api/v1/school/{id}/exams/{exam_id}/hall-tickets/{student_id}/` | Single student hall ticket data |
| 4 | `GET` | `/api/v1/school/{id}/exams/{exam_id}/hall-tickets/{student_id}/pdf/` | Single hall ticket PDF |
| 5 | `GET` | `/api/v1/school/{id}/exams/{exam_id}/hall-tickets/bundle/?class_id={id}` | Class bundle PDF |
| 6 | `POST` | `/api/v1/school/{id}/exams/{exam_id}/hall-tickets/mark-distributed/` | Bulk mark as distributed |
| 7 | `POST` | `/api/v1/school/{id}/exams/{exam_id}/hall-tickets/{student_id}/reprint/` | Generate duplicate |
| 8 | `GET` | `/api/v1/school/{id}/exams/{exam_id}/hall-tickets/missing-photo/` | Students without photo |

---

## 11. Business Rules

- Hall tickets can only be generated after exam configuration is approved (Principal approval from B-11)
- Seating plan (B-13) must be generated before hall tickets, as hall/seat numbers are printed on them
- Students excluded from exam eligibility (below 75% attendance without condonation, fee-blocked if enabled) do not get hall tickets
- Hall ticket generation is idempotent — running it again doesn't create duplicates; it updates existing ones with latest seating data
- Duplicates are logged; more than 2 duplicates for the same student triggers a note to class teacher
- Hall tickets for board exams (CBSE) are not generated here; CBSE generates them directly and they are tracked in B-33

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division B*
