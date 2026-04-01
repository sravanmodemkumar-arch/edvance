# B-19 — Report Card Generator

> **URL:** `/school/academic/results/<exam_id>/report-cards/`
> **File:** `b-19-report-card-generator.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Exam Cell Head (S4) — generate · Class Teacher (S3) — view/sign own class · Principal (S6) — approve/sign

---

## 1. Purpose

Generates the official student report cards (progress reports) from computed results. In Indian schools, the report card is given to parents at the end of each term and is the primary official communication of a student's academic performance. CBSE has a prescribed report card format — the digital version must match this format exactly, including grade display, CGPA computation, co-scholastic activities, and teacher remarks. The Principal signs the report card and it bears the school seal. This page generates them in bulk, sends them to parents digitally, and tracks which physical copies have been distributed.

---

## 2. Page Layout

### 2.1 Header
```
Report Card Generator — Annual Exam 2025–26       [Generate All]  [Download Bundle]  [Send to Parents]
Exam: Annual Exam 2025–26  ·  Status: ✅ Results Published
Total Students: 2,182  ·  Generated: 2,180  ·  Distributed: 1,210  ·  Pending: 972
```

---

## 3. Pre-Generation Requirements

| # | Check | Status |
|---|---|---|
| 1 | Results published | ✅ Published (28 Mar 2026) |
| 2 | Co-scholastic marks entered (VI–X CBSE) | ✅ Done |
| 3 | Class teacher remarks entered | ⚠️ 8 classes pending |
| 4 | Report card template configured | ✅ CBSE Standard Template |
| 5 | Principal signature image uploaded | ✅ Done |
| 6 | School stamp/seal image uploaded | ✅ Done |

**8 classes pending teacher remarks** — [Send Reminder to Class Teachers] → WhatsApp/in-app notification to 8 class teachers to enter their remarks.

---

## 4. Teacher Remarks Entry

Before report cards are generated, class teachers enter per-student remarks:

**My Classes — Remarks Entry Status (Class Teacher view):**

| Student | Academic Remark | Conduct | Attendance | Remarks Entered |
|---|---|---|---|---|
| Arjun Sharma | ✅ | ✅ | ✅ | ✅ Done |
| Priya V | ✅ | ✅ | ✅ | ✅ Done |
| Rahul G | ⬜ | ⬜ | ✅ | ⬜ Pending |

**Remark templates for quick entry:**
- "Shows consistent effort and improvement throughout the year."
- "Excellent performance. Should continue maintaining this standard."
- "Needs to focus more on [subject]. Remedial support recommended."
- "Good participation in class activities. Academic improvement expected."
- [Custom remark — free text]

---

## 5. Report Card Format — CBSE Standard (Class IX–X)

```
┌─────────────────────────────────────────────────────────────────┐
│  [SCHOOL LOGO]    ABC INTERNATIONAL SCHOOL, HYDERABAD           │
│  CBSE Affil: 1234567  ·  UDISE: 36140100102                     │
│                    REPORT CARD  2025–26                         │
├─────────────────────────────────────────────────────────────────┤
│  Name: ARJUN SHARMA                  Class: IX-A               │
│  Roll No: 2026/IX/001                DOB: 14 Aug 2009          │
│  Father: Mr. Vijay Sharma            Mother: Mrs. Kavitha       │
├───────────────────────────────────────────────────────────────┤
│  SCHOLASTIC AREAS (Theory)                                      │
│  Subject        PT1 PT2 PT3 HY  Annual  IA  TOTAL  Grade CGPA  │
│  English         8   9  10  34   72    19    91     A1    10   │
│  Hindi           7   8  9   30   68    18    86     A2     9   │
│  Mathematics     9  10  10  36   74    19    93     A1    10   │
│  Science         7   9  10  32   70    19    89     A2     9   │
│  Social Studies  8   8  9   33   68    19    87     A2     9   │
│                                                                 │
│  Overall Percentage: 89.2%   CGPA: 9.4   Result: PASS          │
├─────────────────────────────────────────────────────────────────┤
│  CO-SCHOLASTIC AREAS                                            │
│  Work Education: A   Art Education: A+   Health & Physical: A  │
│  Discipline: A       Inclusive Education: A                     │
├─────────────────────────────────────────────────────────────────┤
│  ATTENDANCE: Present: 196/220 (89.1%)                          │
├─────────────────────────────────────────────────────────────────┤
│  Class Teacher Remarks:                                         │
│  Arjun has shown excellent academic performance this year.      │
│  His participation in Science Exhibition was commendable.       │
├─────────────────────────────────────────────────────────────────┤
│  Class Teacher: ___________    Principal: ___________  [Seal]  │
│  Date: 30 March 2026                                           │
└─────────────────────────────────────────────────────────────────┘
```

---

## 6. Co-Scholastic Areas Entry

CBSE mandates co-scholastic grades for Classes VI–X (Work Education, Art, Health/Physical Education, Discipline):

[Enter Co-Scholastic] → grid per class:

| Student | Work Education | Art Education | Health & PE | Discipline |
|---|---|---|---|---|
| Arjun Sharma | A | A+ | A | A |
| Priya V | A+ | A+ | A+ | A+ |
| Rahul G | B | A | B | B |

Grades: A+ / A / B / C (CBSE co-scholastic grading scale)

---

## 7. Generate Report Cards

[Generate All] → background task:
- Generates one PDF per student
- Each PDF is school-letterhead formatted, ready to print or send digitally
- Stored in Cloudflare R2 with student ID + exam ID path
- Progress bar via HTMX polling

[Generate by Class] → generates for one section at a time (useful for staggered distribution).

---

## 8. Report Card Preview

`report-card-preview` drawer (640px) — triggered by [Preview] or clicking student name:

Shows the complete report card exactly as it will print. From this drawer:
- [Download PDF]
- [Mark as Distributed] — marks physical copy as given to student/parent
- [Send Digitally] — sends PDF link via parent's WhatsApp/email

---

## 9. Distribution Tracking

| Student | Class | Generated | Sent Digitally | Physical Copy Given | Date |
|---|---|---|---|---|---|
| Arjun Sharma | IX-A | ✅ | ✅ WhatsApp | ✅ PTM (29 Mar) | 29 Mar |
| Priya V | IX-A | ✅ | ✅ Email | ⬜ Not yet | — |
| Rahul G | IX-A | ✅ | ⬜ Not sent | ⬜ Not yet | — |

Class teachers mark physical distribution at PTM or on report card day.

---

## 10. Send to Parents (Bulk)

[Send to Parents] → options:
- **WhatsApp:** PDF link sent via WhatsApp to parent's registered number (via SQS queue)
- **Email:** PDF attached to email to parent's email ID
- **In-app (Student/Parent portal):** Report card visible in portal immediately on publication
- **SMS:** Brief result summary + download link (for parents without smartphones)

Select classes → send. Delivery status tracked per student.

---

## 11. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `POST` | `/api/v1/school/{id}/exams/{exam_id}/report-cards/generate/` | Trigger bulk generation |
| 2 | `GET` | `/api/v1/school/{id}/exams/{exam_id}/report-cards/status/` | Generation + distribution status |
| 3 | `GET` | `/api/v1/school/{id}/exams/{exam_id}/report-cards/{student_id}/` | Individual report card data |
| 4 | `GET` | `/api/v1/school/{id}/exams/{exam_id}/report-cards/{student_id}/pdf/` | Report card PDF |
| 5 | `POST` | `/api/v1/school/{id}/exams/{exam_id}/report-cards/send/` | Send to parents (bulk) |
| 6 | `PATCH` | `/api/v1/school/{id}/exams/{exam_id}/report-cards/{student_id}/remarks/` | Update teacher remarks |
| 7 | `PATCH` | `/api/v1/school/{id}/exams/{exam_id}/report-cards/{student_id}/co-scholastic/` | Update co-scholastic marks |
| 8 | `POST` | `/api/v1/school/{id}/exams/{exam_id}/report-cards/{student_id}/mark-distributed/` | Mark physical distribution |
| 9 | `GET` | `/api/v1/school/{id}/exams/{exam_id}/report-cards/bundle/?class_id={id}` | Class bundle PDF |

---

## 12. Business Rules

- Report cards can only be generated after results are published (B-18)
- Co-scholastic grades and teacher remarks are not mandatory for report card generation — missing items show blank on the card with a watermark "Remarks Pending"
- Once a report card is generated and sent to parents, regenerating it (for corrections) requires Principal approval and the new version is clearly marked "Revised"
- CBSE format report cards for Class X and XII must use exactly the CBSE prescribed format — the system enforces this with a locked template when board = CBSE
- Attendance percentage on the report card is pulled from the attendance module; it cannot be manually overridden on the report card (must be corrected in the attendance records)

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division B*
