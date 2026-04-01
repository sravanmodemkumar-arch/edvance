# A-12 — Exam Calendar

> **URL:** `/school/admin/calendar/exams/`
> **File:** `a-12-exam-calendar.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Principal (S6) — full · VP Academic (S5) — full · Exam Cell Head (S4) — full · All staff (S3+) — view

---

## 1. Purpose

Master exam scheduling page for the school year. Lists all internal exams (Unit Tests, Formative Assessments, Summative Assessments, Pre-boards, Practicals) and external board exams (CBSE boards, state board, competitive entrance tests). Each exam entry here links to the detailed exam configuration in the Exam module (div-f). This calendar is the source of truth that parents, students, and staff refer to for the year's assessment schedule.

**Indian exam structure (CBSE example):**
- **Formative Assessment (FA/PT):** 3–4 times/year; class-level; 20–40 marks
- **Half-Yearly / Mid-Term:** After 6 months; school-level; 80–100 marks
- **Annual / Final Examination:** Year-end; determines promotion
- **Pre-board (IX–XII only):** Practice run 4–6 weeks before board exams
- **CBSE Board Practicals (XI–XII):** Conducted by external examiner; dates given by CBSE
- **CBSE Theory Board Exams (X, XII):** February–March; dates from CBSE datesheet
- **Competitive Tests (coaching schools):** JEE/NEET mock tests, topic-wise tests (monthly or weekly)

**State board structure varies:** AP/TS schools have SSC (class X) and Intermediate (XI–XII) exams with state-defined dates. Tamil Nadu has quarterly exams. Karnataka has SSLC with different term structure.

---

## 2. Page Layout

### 2.1 Header
```
Exam Calendar — 2025–26                      [+ Schedule Exam]  [Print Exam Schedule]  [Notify All Parents]
Academic year: Apr 2025 – Mar 2026           View: [Month ▼] [List] [By Class]
```

---

## 3. Month View

Calendar grid with exam events colour-coded:
| Colour | Exam Category |
|---|---|
| 🔵 Dark Blue | Board Exam (CBSE/ICSE/State) |
| 🟦 Medium Blue | Pre-Board / Trial Exam |
| 🟢 Green | Summative Assessment / Half-Yearly / Annual |
| 🟡 Yellow | Unit Test / Formative Assessment / Class Test |
| 🟠 Orange | Practical Exam / Lab Assessment |
| 🔴 Red | Competitive Mock Test (JEE/NEET) |
| ⚫ Dark | NTSE / Olympiad / External Competition |

Hover any event → tooltip: Exam name, classes, date range, exam head

---

## 4. List View (full exam schedule)

| Exam Name | Type | Classes | Start Date | End Date | Status | Config |
|---|---|---|---|---|---|---|
| Unit Test 1 — Q1 | Formative | I–VIII | 12 Jun 2025 | 15 Jun 2025 | Scheduled | [View Config] |
| Half-Yearly Exam | Summative | I–XII | 20 Sep 2025 | 4 Oct 2025 | Scheduled | [View Config] |
| Unit Test 2 — Q2 | Formative | I–VIII | 5 Nov 2025 | 8 Nov 2025 | Scheduled | [View Config] |
| Pre-Board Exam 1 | Pre-Board | IX–XII | 10 Jan 2026 | 20 Jan 2026 | Scheduled | [View Config] |
| Pre-Board Exam 2 | Pre-Board | X, XII | 5 Feb 2026 | 12 Feb 2026 | Scheduled | [View Config] |
| CBSE Class X Board | Board | X | 15 Feb 2026 | 18 Mar 2026 | Confirmed (CBSE) | [View] |
| CBSE Class XII Board | Board | XII | 15 Feb 2026 | 5 Apr 2026 | Confirmed (CBSE) | [View] |
| Annual Exam | Summative | I–IX, XI | 15 Mar 2026 | 30 Mar 2026 | Scheduled | [View Config] |

---

## 5. Schedule Exam Drawer (+ Schedule Exam)

**560px wide**

| Field | Description |
|---|---|
| Exam Name | Free text |
| Exam Type | Unit Test / Formative / Summative / Half-Yearly / Annual / Pre-Board / Board / Practical / Mock / Olympiad |
| Classes | Multi-select (all or specific) |
| Streams | All / Specific (for XI–XII) |
| Start Date | Date picker |
| End Date | Date picker |
| Daily Start Time | Time picker |
| Daily End Time | Time picker |
| Exam Head | Select from staff (Exam Cell Head or VP Academic) |
| Hall ticket required? | Yes / No |
| Parent notification? | Notify now / Schedule 15-day advance reminder |

On save: creates calendar event + creates exam record in div-f (Exam Module) with status SCHEDULED.

---

## 6. Board Exam Integration

**CBSE Board Exam Import:**
- [Import CBSE Datesheet] → school enters CBSE region; EduForge fetches datesheet from CBSE portal (if API available) or school uploads PDF
- Dates auto-populate for Class X and XII
- Parents notified automatically once board datesheet is confirmed

**State Board Exam Import:**
- Similar workflow for state board (TS/AP/MH/KA/TN etc.)

---

## 7. Exam Conflict Detection

When scheduling a new exam, system auto-checks:
- Is there another exam for the same class on the same date? → Warning: "Class IX already has Unit Test 2 on 5 Nov"
- Is the date a declared holiday? → Block: "5 Nov 2025 is Diwali (declared holiday). Choose another date."
- Does the exam overlap with a scheduled CBSE practical inspection? → Warning

---

## 8. Notifications

**[Notify All Parents]** button: sends exam schedule to all parents via WhatsApp/SMS/email.
- Generates per-student personalised message with their class's exam dates
- Parents can add to their phone calendar via ICS link in the message

---

## 9. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/exam-calendar/` | All scheduled exams |
| 2 | `POST` | `/api/v1/school/{id}/exam-calendar/` | Schedule new exam |
| 3 | `PATCH` | `/api/v1/school/{id}/exam-calendar/{exam_id}/` | Update exam dates |
| 4 | `DELETE` | `/api/v1/school/{id}/exam-calendar/{exam_id}/` | Cancel/delete exam |
| 5 | `POST` | `/api/v1/school/{id}/exam-calendar/import-cbse-datesheet/` | Import CBSE board dates |
| 6 | `POST` | `/api/v1/school/{id}/exam-calendar/notify-parents/` | Send exam schedule to parents |
| 7 | `GET` | `/api/v1/school/{id}/exam-calendar/conflicts/?start={date}&end={date}&classes={ids}` | Check scheduling conflicts |

---

## 10. Business Rules

- Board exam dates (CBSE/ICSE/State) are locked after import — cannot be edited; can only be deleted and re-imported
- Internal exam cancellation: if results are already entered in the system → cannot delete (can mark as CANCELLED and preserve records)
- Exam schedule changes after parent notification trigger an automatic re-notification: "Exam date change notice: Class IX Half-Yearly rescheduled from 20 Sep to 22 Sep"
- Exam start and end times are used by the online exam module (div-f) for real-time countdown and access window enforcement

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division A*
