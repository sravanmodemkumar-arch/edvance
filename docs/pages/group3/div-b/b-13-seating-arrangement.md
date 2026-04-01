# B-13 — Seating Arrangement

> **URL:** `/school/academic/exams/<exam_id>/seating/`
> **File:** `b-13-seating-arrangement.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Exam Cell Head (S4) — full · Principal (S6) — view

---

## 1. Purpose

Generates seating arrangements for the exam — assigns each eligible student to a specific hall (room) and seat number. Proper seating arrangement prevents students of the same class from sitting adjacent to each other (to prevent copying), optimally fills available exam halls, and produces the seating plan for posting outside each hall. This is a standard examination control measure in Indian schools. The seating plan feeds into B-12 (hall tickets show hall and seat numbers) and B-14 (invigilators know their hall layout).

---

## 2. Page Layout

### 2.1 Header
```
Seating Arrangement — Annual Exam 2025–26         [Generate Seating]  [Download All Plans]
Exam: Annual Exam 2025–26  ·  Total Students: 2,182  ·  Exam Halls: 14
Status: ⬜ Not Generated
```

---

## 3. Exam Halls Configuration

Before generation, configure which rooms are exam halls:

| Hall | Room | Capacity | Assigned | Remaining | Status |
|---|---|---|---|---|---|
| Hall A | Room 101 | 45 | 45 | 0 | ✅ Full |
| Hall B | Room 102 | 45 | 45 | 0 | ✅ Full |
| Hall C | Room 103 | 45 | 44 | 1 | ✅ Full |
| Hall D | Room 201 | 48 | 48 | 0 | ✅ Full |
| Hall E | Room 202 | 48 | 45 | 3 | ✅ Full |
| Hall F | Room 203 | 48 | 45 | 3 | ✅ Full |
| Hall G | Room 204 | 48 | 40 | 8 | 🟡 Partial |

[+ Add Hall] → select from B-29 room registry
[Set Capacity Override] → override if reduced capacity for spacing requirements (COVID-era feature still used)

---

## 4. Seating Generation Options

[Generate Seating] → options panel:

| Option | Description | Default |
|---|---|---|
| Method | Roll number order / Alphabetical / Random | Roll number order |
| Mix classes | Students from different classes/sections in same hall | ✅ Yes (CBSE recommended — prevents same-class adjacency) |
| Separate boys/girls | Boys and girls in separate halls or alternating seats | School config |
| Leave empty seats | Leave every N-th seat empty for spacing | No |
| Fix a student to specific seat | Manual pin before bulk generation | Per HOD request |

**"Mix classes" logic** (recommended): Instead of filling Hall A with all Class IX-A students then Hall B with IX-B, students from different sections/classes are interleaved. Roll number allocation interleaves: IX-A seat 1, IX-B seat 2, X-A seat 3, IX-A seat 4, IX-B seat 5...

This is the standard practice in Indian schools specifically to deter copying between classmates.

---

## 5. Generated Seating Plan

After generation, the seating is displayed per hall:

### Hall A (Room 101) — 45 Seats

```
Row 1:  A1: Arjun Sharma(XI-A)  A2: Priya V(IX-B)   A3: Rajan T(X-A)    A4: Suresh M(XI-B)  A5: Deepa K(IX-A)
Row 2:  A6: Kavitha R(X-B)      A7: Anand P(XI-A)   A8: Meena S(IX-B)   A9: Vijay K(X-A)    A10: Pooja D(XI-B)
Row 3:  ...
```

Visual grid view with seat numbers and student names + class.

```
              [View as Grid]  [Download Hall Plan PDF]  [Post Outside Hall]
```

**Hall Plan PDF** → A3/A2 size poster showing the seating grid — printed and posted outside the exam hall so students can find their seats.

---

## 6. Seating Plan Drawer (`seating-plan-view`, 560px)

Triggered by clicking any hall name:

- **Visual grid** of the room layout showing actual rows/columns of benches
- Each cell shows: Seat#, Student Name, Class-Section, Roll Number
- Empty seats shown as blank
- HOD can manually drag-and-drop to swap two students
- [Print Hall Plan] — A3 PDF of this hall only

---

## 7. Student-wise Seating Lookup

Search a student by name or roll number → shows their hall + seat number.

Used by:
- Students checking where to sit
- Teachers finding a student during exam
- Office staff when a student reports lost hall ticket

---

## 8. Special Needs Seating

Students with certified disabilities or medical conditions requiring special accommodation:

| Student | Class | Condition | Accommodation | Hall | Seat |
|---|---|---|---|---|---|
| Ravi Kumar | XI-A | Low vision | Front row, extra lighting | Hall A | A1 |
| Priya M | X-B | Hearing impairment | Front row, near invigilator | Hall B | B1 |
| Arjun D | IX-A | Dyslexia | Separate room with scribe | Hall G | G1 |

These students are pinned to specific seats before bulk generation — the system preserves their assignment when generating.

---

## 9. Seating Plan Regeneration

If the student list changes (new student added, student withdrawn, condonation granted after initial generation):
- [Regenerate] → rebuilds entire plan (warns that hall ticket seat numbers will change and hall tickets must be reprinted)
- [Add Student Manually] → adds a single student to the next available seat in a hall (for late additions)

---

## 10. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `POST` | `/api/v1/school/{id}/exams/{exam_id}/seating/generate/` | Generate seating plan |
| 2 | `GET` | `/api/v1/school/{id}/exams/{exam_id}/seating/` | Seating overview (all halls) |
| 3 | `GET` | `/api/v1/school/{id}/exams/{exam_id}/seating/hall/{hall_id}/` | Hall detail + seat grid |
| 4 | `GET` | `/api/v1/school/{id}/exams/{exam_id}/seating/student/{student_id}/` | Student's seat lookup |
| 5 | `PATCH` | `/api/v1/school/{id}/exams/{exam_id}/seating/swap/` | Swap two students' seats |
| 6 | `GET` | `/api/v1/school/{id}/exams/{exam_id}/seating/hall/{hall_id}/pdf/` | Hall seating plan PDF |
| 7 | `GET` | `/api/v1/school/{id}/exams/{exam_id}/seating/all/pdf/` | All halls seating plans PDF bundle |

---

## 11. Business Rules

- Seating plan must be generated before hall tickets are generated (B-12 reads hall and seat numbers from here)
- If seating is regenerated after hall tickets are printed, all hall tickets must be reprinted — the system warns and creates a reprint task in the Exam Cell Head's task list
- Manual seat swaps (drag-and-drop) are logged in the audit trail (who swapped, when, reason if provided)
- Special needs seating assignments from the student's profile (disability/medical certificate) are respected automatically — these students' seat assignments cannot be changed without Principal override
- Seating plan PDFs are generated once and cached in R2; on-demand re-generation is triggered by any change

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division B*
