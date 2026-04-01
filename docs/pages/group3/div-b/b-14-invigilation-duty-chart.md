# B-14 — Invigilation Duty Chart

> **URL:** `/school/academic/exams/<exam_id>/invigilators/`
> **File:** `b-14-invigilation-duty-chart.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Exam Cell Head (S4) — full · Timetable Coordinator (S3) — view · All teachers — view own duty · Principal (S6) — approve

---

## 1. Purpose

Assigns invigilators (examination supervisors) to exam halls for each exam session. Every exam period requires teachers to monitor halls to prevent unfair means — the number of invigilators per hall is typically 1 per 30–40 students (CBSE recommendation: 1 per 25 students for senior classes). The duty chart must be fair across staff (no teacher should repeatedly bear the burden), must avoid a teacher invigilating the class they teach (conflict of interest for that subject's paper), and must be published in advance so teachers can plan accordingly. The invigilation duty chart is a statutory register in CBSE schools.

---

## 2. Page Layout

### 2.1 Header
```
Invigilation Duty Chart — Annual Exam 2025–26     [Auto-Assign]  [Download Chart]  [Notify Staff]
Exam: Annual Exam 2025–26  ·  Sessions: 14 (1–20 Mar, 1 session/day)
Staff Available: 62  ·  Invigilators Needed/Session: 14 (1 per hall) + 2 relievers
Status: ⚠️ Draft — Pending Principal Approval
```

---

## 3. Duty Chart Grid (Main View)

Rows = Exam dates/sessions · Columns = Exam Halls:

| Date | Subject (session) | Hall A | Hall B | Hall C | Hall D | Hall E | Reliever 1 | Reliever 2 |
|---|---|---|---|---|---|---|---|---|
| 1 Mar | English (All) | Ms. Suma | Mr. Rajan | Ms. Leela | Dr. Anand | Ms. Kavitha | Mr. Bala | Ms. Pooja |
| 3 Mar | Maths | Ms. Priya | Ms. Deepa | Mr. Kumar | Ms. Meena | Mr. Suresh | Mr. Ravi | Ms. Anjali |
| 4 Mar | Physics/Sci | Mr. Ramesh | Ms. Leela | Mr. Dinesh | Ms. Suma | Mr. Bala | Ms. Priya | Mr. Kumar |
| 6 Mar | Chemistry | Ms. Kavitha | Mr. Anand | Ms. Pooja | Mr. Rajan | Ms. Deepa | Mr. Suresh | Mr. Ramesh |

Cells are clickable to swap invigilators.

**Colour flags:**
- 🔴 Teacher assigned to invigilate a hall where their own subject students are seated (conflict of interest)
- 🟡 Teacher has already invigilated 5+ times this exam (high load)
- 🟢 Normal assignment

---

## 4. Auto-Assign Logic

[Auto-Assign] → runs the assignment algorithm:

**Constraints (hard):**
- A teacher cannot invigilate a hall containing students from a class they currently teach the same subject (e.g., Physics teacher Ms. Lakshmi cannot invigilate during Physics exam in any hall — too close to the content and students)
- No teacher can be assigned to two halls simultaneously
- A teacher on leave that day cannot be assigned (checks A-17 leave calendar)

**Constraints (soft/preferences):**
- Distribute duty load evenly across staff (count-based fairness)
- Senior staff (S4+) preferred for XII exam halls
- Fresh joiners not assigned as sole invigilator — pair with experienced invigilator
- Form teachers (class teachers) avoided for their own class's halls

**Result:** System suggests assignments; Exam Cell Head can manually override any cell.

---

## 5. Invigilation Load Analysis

| Teacher | Total Duties Assigned | Duties This Exam | Last Duty Date | Status |
|---|---|---|---|---|
| Mr. Ramesh (Hindi) | 18 this year | 3 | 4 Mar | 🟡 Medium load |
| Ms. Suma (English) | 20 this year | 4 | 6 Mar | 🟡 Medium load |
| Ms. Anjali (Biology) | 8 this year | 2 | 3 Mar | ✅ Normal |
| Mr. Dinesh (CS) | 4 this year | 1 | 4 Mar | ✅ Normal |

Shows whether the duty has been fairly distributed. Exam Cell Head reviews this before finalizing.

---

## 6. Teacher's Own View

When a teacher (Subject Teacher S3) accesses this page, they see only their own duty:

```
Your Invigilation Duties — Annual Exam 2025–26

  Date         Session    Hall      Reporting Time  Notes
  1 Mar 2026   English    Hall A    09:45 AM        Please collect duty register from Exam Cell
  6 Mar 2026   Chemistry  Hall B    09:45 AM        —
  11 Mar 2026  History    Hall C    09:45 AM        —
```

[Acknowledge Duty] → teacher confirms they have seen their schedule (used to confirm receipt without a physical register signature).

---

## 7. Invigilator Instructions Sheet

[Download Chart] → generates two documents:

**Document 1 — Master Duty Chart:** Full grid, all sessions, all halls. Printed and displayed in the staff common room.

**Document 2 — Individual Duty Slips:** One slip per teacher listing only their assigned duties. Given to each teacher at the start of the exam.

Both documents include:
- Invigilator instructions (report time, duty register signing, mobile phone policy, UFM procedure reference)
- Emergency contacts (Exam Cell Head, Vice Principal)
- Instructions for students found without hall tickets

---

## 8. Notify Staff

[Notify Staff] → sends notification to all assigned invigilators:
- In-app notification: "Your invigilation duty for Annual Exam 2025–26 has been published"
- WhatsApp: Summary of their duties
- Option to send duty slip PDF via WhatsApp

---

## 9. Invigilation Attendance Register

On each exam day, the duty chart doubles as an attendance register for invigilators:

| Hall | Assigned | Reported | Reported Time | Notes |
|---|---|---|---|---|
| Hall A | Ms. Suma | ✅ | 09:42 | — |
| Hall B | Mr. Rajan | ✅ | 09:48 | Late by 3 min |
| Hall C | Ms. Leela | ❌ Absent | — | Substitute: Mr. Kumar |

This view is managed by the Exam Cell Head on exam day. Absent invigilators are replaced from the reliever pool.

---

## 10. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/exams/{exam_id}/invigilators/` | Full duty chart |
| 2 | `POST` | `/api/v1/school/{id}/exams/{exam_id}/invigilators/auto-assign/` | Run auto-assignment |
| 3 | `PATCH` | `/api/v1/school/{id}/exams/{exam_id}/invigilators/cell/` | Update a single cell (swap) |
| 4 | `GET` | `/api/v1/school/{id}/exams/{exam_id}/invigilators/load-analysis/` | Load analysis per teacher |
| 5 | `GET` | `/api/v1/school/{id}/exams/{exam_id}/invigilators/teacher/{teacher_id}/` | Teacher's own duties |
| 6 | `POST` | `/api/v1/school/{id}/exams/{exam_id}/invigilators/teacher/{teacher_id}/acknowledge/` | Teacher acknowledgement |
| 7 | `POST` | `/api/v1/school/{id}/exams/{exam_id}/invigilators/notify/` | Send duty notifications |
| 8 | `GET` | `/api/v1/school/{id}/exams/{exam_id}/invigilators/export/` | Download duty chart PDF |
| 9 | `PATCH` | `/api/v1/school/{id}/exams/{exam_id}/invigilators/attendance/` | Mark day-of attendance |

---

## 11. Business Rules

- Auto-assignment respects the "teacher cannot invigilate their own subject's exam" rule as a hard constraint — a Physics teacher cannot be assigned to any hall during the Physics exam regardless of what other classes are in that hall
- A teacher on approved leave cannot be assigned; if leave is applied after assignment, the system flags the conflict
- The duty chart requires Principal approval before being distributed to staff
- Teacher acknowledgements are logged and visible to the Exam Cell Head — unacknowledged duties (within 48 hours of notification) trigger a reminder
- Invigilation attendance register entries (reporting time, absences) feed into the Audit Log (A-34)

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division B*
