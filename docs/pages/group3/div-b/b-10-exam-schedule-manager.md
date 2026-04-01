# B-10 — Exam Schedule Manager

> **URL:** `/school/academic/exams/schedule/`
> **File:** `b-10-exam-schedule-manager.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Exam Cell Head (S4) — full · Academic Coordinator (S4) — full · HOD (S4) — read · Principal (S6) — approve · VP Academic (S5) — read · All teachers — read

---

## 1. Purpose

The master view of all examinations scheduled for the academic year — the Exam Cell Head's primary workspace. Lists every exam from Periodic Test 1 to the Annual Exam, with status, class applicability, date range, marks structure, and progress indicators. Exam scheduling is a high-stakes activity: dates must avoid clashes with each other, with board exam dates, with school events, with public holidays, and must give teachers adequate time to complete syllabus before each test. In CBSE schools, this schedule is submitted to the Principal and displayed on the school's official notice board.

---

## 2. Page Layout

### 2.1 Header
```
Exam Schedule Manager                             [+ Create Exam]  [Export Schedule]  [Import Board Dates]
Academic Year: 2025–26  ·  Term: [All ▼]  ·  Status: [All ▼]
Total Exams: 12  ·  Upcoming: 3  ·  In Progress: 1  ·  Completed: 8
```

---

## 3. Exam Calendar Strip (Monthly View)

Mini calendar showing exam dates at a glance across the year with colour-coded dots:

```
Apr  May  Jun  Jul  Aug  Sep  Oct  Nov  Dec  Jan  Feb  Mar
[PT1][   ][UT1][   ][PT2][   ][HY ][   ][PT3][UT2][ANN][   ]
```

Board exam dates imported from CBSE (A-12) shown in a different colour.

---

## 4. Exam List Table

| # | Exam Name | Type | Classes | Date Range | Max Marks | Status | Progress | Actions |
|---|---|---|---|---|---|---|---|---|
| 1 | Periodic Test 1 | Internal | I–XII | 15–20 Apr 2025 | 40 | ✅ Complete | Results published | [View] |
| 2 | Unit Test 1 | Internal | VI–X | 20–25 Jun 2025 | 25 | ✅ Complete | Results published | [View] |
| 3 | Periodic Test 2 | Internal | I–XII | 20–28 Aug 2025 | 40 | ✅ Complete | Results published | [View] |
| 4 | Half-Yearly | Major | VI–XII | 15–28 Oct 2025 | 80 | ✅ Complete | Results published | [View] |
| 5 | Periodic Test 3 | Internal | I–XII | 5–12 Jan 2026 | 40 | ✅ Complete | Results published | [View] |
| 6 | Unit Test 2 | Internal | VI–X | 10–15 Feb 2026 | 25 | 🔄 In Progress | Marks entry pending | [Manage] |
| 7 | Annual Exam | Major | VI–IX, XI | 1–20 Mar 2026 | 80 | ⏳ Upcoming | Hall tickets pending | [Manage] |
| 8 | CBSE Class X Boards | Board | X | 15 Feb–18 Mar 2026 | 80 | 🔄 In Progress | CBSE managed | [View LOC] |
| 9 | CBSE Class XII Boards | Board | XII | 15 Feb–4 Apr 2026 | 70/80 | 🔄 In Progress | CBSE managed | [View LOC] |
| 10 | Annual Exam | Major | I–V | 25–31 Mar 2026 | 50 | ⏳ Upcoming | — | [Manage] |

**Exam Types:**
- **Periodic Test (PT):** CBSE's 40-mark internal test (2 subjects × 40m typically)
- **Unit Test (UT):** Shorter internal test (25m per subject)
- **Half-Yearly / Mid-Term:** Major exam, 80m per subject
- **Annual:** End-of-year major exam
- **Board:** CBSE/ISC/State Board conducted external exams
- **Practical:** Science/CS/PE practicals (shown separately in B-35)
- **Supplementary:** Post-annual remedial exam (B-39)

---

## 5. Exam Detail View (Click any row)

Opens the `exam-config-detail` drawer (680px) or navigates to B-11 (Exam Configuration) for full management:

```
Annual Exam 2025–26
Type: Major  ·  Status: Upcoming
Classes: VI, VII, VIII, IX, XI (52 sections)  ·  Total Students: 2,182
Date Range: 1 Mar – 20 Mar 2026
Max Marks: 80 per subject
```

Tabs in the drawer:
1. **Overview** — dates, classes, marks, status
2. **Subject Schedule** — which subject on which date
3. **Checklist** — preparation tasks with status (see Section 6)
4. **Quick Links** → B-11, B-12, B-13, B-14, B-15, B-16

---

## 6. Exam Preparation Checklist

Per exam, a standard checklist tracks readiness:

| # | Task | Responsible | Status | Due Date |
|---|---|---|---|---|
| 1 | Datesheet finalized | Exam Cell Head | ✅ Done | 10 Feb |
| 2 | Principal approval | Principal | ✅ Done | 12 Feb |
| 3 | Datesheet circulated to students | Office Staff | ✅ Done | 14 Feb |
| 4 | Question papers submitted by teachers | All HODs | ⚠️ 3 pending | 20 Feb |
| 5 | Question papers reviewed by HODs | HODs | ⬜ Not started | 22 Feb |
| 6 | Hall tickets generated | Exam Cell Head | ⬜ Not started | 25 Feb |
| 7 | Seating plan ready | Exam Cell Head | ⬜ Not started | 28 Feb |
| 8 | Invigilation duty chart | Exam Cell Head | ⬜ Not started | 28 Feb |
| 9 | Answer books/OMR sheets ready | Office Staff | ⬜ Not started | 1 Mar |
| 10 | Exam stationery packed | Office Staff | ⬜ Not started | 28 Feb |

Overdue tasks highlighted in red. HODs and relevant staff notified automatically 2 days before due date.

---

## 7. Create Exam Wizard

[+ Create Exam] → 3-step wizard:

### Step 1 — Basic Details

| Field | Value |
|---|---|
| Exam Name | Text (e.g., "Periodic Test 2") |
| Type | Periodic Test / Unit Test / Half-Yearly / Annual / Practical / Board / Other |
| Academic Year | Auto-filled |
| Term | Term 1 / Term 2 / Term 3 |
| Applicable Classes | Multi-select: I–XII (with section granularity option) |
| Date Range | Start date → End date |
| Results Expected By | Date |

### Step 2 — Subject Schedule (Datesheet)

For each selected class group, specify:

| Date | Time Slot | Subject | Class Groups | Max Marks | Duration |
|---|---|---|---|---|---|
| 1 Mar 2026 | 10:00–12:20 | English | All (VI–XI) | 80 | 140 min |
| 3 Mar 2026 | 10:00–12:20 | Mathematics | VI–IX, XI MPC | 80 | 140 min |
| 4 Mar 2026 | 10:00–12:20 | Science | VI–VIII | 80 | 140 min |
| 4 Mar 2026 | 10:00–12:20 | Physics | IX, XI | 80 | 140 min |

Conflict detection: if a date+class combination already has another exam, warning shown.

### Step 3 — Configuration Options

| Field | Value |
|---|---|
| Hall Ticket Required | Yes / No |
| Seating Arrangement | Random / Class-wise / Roll number order |
| OMR / Answer Script | Answer Script / OMR |
| Grace Marks Applicable | Yes (CBSE rules) / No |
| IA Component | Link to Internal Assessment (B-31) |

---

## 8. Import Board Dates

[Import Board Dates] → pulls CBSE board exam dates from integrated database (updated annually):
- CBSE Class X datesheet
- CBSE Class XII datesheet
- State board dates (state-specific)

These are shown in read-only mode (school cannot edit board exam dates). They feed into A-12 (Exam Calendar) and appear as locked entries in the exam list.

---

## 9. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/exams/?year={year}&term={term}&status={status}` | Exam list |
| 2 | `POST` | `/api/v1/school/{id}/exams/` | Create exam |
| 3 | `GET` | `/api/v1/school/{id}/exams/{exam_id}/` | Exam detail |
| 4 | `PATCH` | `/api/v1/school/{id}/exams/{exam_id}/` | Update exam |
| 5 | `GET` | `/api/v1/school/{id}/exams/{exam_id}/checklist/` | Preparation checklist |
| 6 | `PATCH` | `/api/v1/school/{id}/exams/{exam_id}/checklist/{task_id}/` | Update checklist task |
| 7 | `POST` | `/api/v1/school/{id}/exams/import-board-dates/` | Import CBSE/board dates |
| 8 | `GET` | `/api/v1/school/{id}/exams/calendar/?year={year}` | Calendar strip data |
| 9 | `POST` | `/api/v1/school/{id}/exams/{exam_id}/submit-for-approval/` | Send to Principal |
| 10 | `POST` | `/api/v1/school/{id}/exams/{exam_id}/approve/` | Principal approves |
| 11 | `GET` | `/api/v1/school/{id}/exams/export/?year={year}` | Export schedule PDF |

---

## 10. Business Rules

- Exam schedule requires Principal approval before hall tickets or seating plans can be generated
- Board exam dates (CBSE/ISC/state) cannot be modified; they are imported read-only
- Two exams for the same class cannot overlap in dates — hard conflict, blocks creation
- An exam date cannot fall on a public holiday (auto-checked against A-11 Holiday Calendar)
- Once an exam status is "Complete" (results published), it cannot be moved to a different date — only the Audit Log records the original date
- The exam checklist auto-generates based on exam type; custom tasks can be added by the Exam Cell Head

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division B*
