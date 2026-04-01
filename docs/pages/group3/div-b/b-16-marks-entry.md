# B-16 — Marks Entry

> **URL:** `/school/academic/marks/<exam_id>/`
> **File:** `b-16-marks-entry.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Subject Teacher (S3) — enter own subject marks · Class Teacher (S3) — enter all subjects for own class · Exam Cell Head (S4) — full all · Principal (S6) — full

---

## 1. Purpose

The marks entry interface where teachers enter student scores after evaluation of answer scripts. This is where the examined data first enters the system — everything downstream (result computation, report cards, analytics) depends on accurate marks entry. The design must handle scale (40 students × 8 subjects = 320 marks entries per class, across 52 sections = 16,640 entries per exam), support entry by multiple teachers simultaneously, prevent duplicate entries, allow corrections within the review window, and flag anomalies (a score above maximum, suspiciously high standard deviation, absent student with marks entered).

**Indian context:** Teachers are used to entering marks either student-by-student in a tabulation sheet or subject-by-subject per class. Both modes are supported. CBSE mandates marks are entered at subject level (not overall total) for IX–XII.

---

## 2. Page Layout

### 2.1 Header
```
Marks Entry — Unit Test 2, 2025–26               [My Assignments]  [Summary Report]
Exam: Unit Test 2  ·  Max Marks: 25 per subject  ·  Date: 10–15 Feb 2026
Status: 🔄 In Progress  ·  Overall: 68 of 104 subject-class combinations entered  ·  65.4% complete
```

---

## 3. Entry Progress Overview

Table showing all subject-class entry assignments:

| Subject | Class | Max Marks | Teacher | Status | Entered | Absent | Pending | Action |
|---|---|---|---|---|---|---|---|---|
| Mathematics | IX-A | 25 | Mr. Arjun | ✅ Done | 42 | 2 | 0 | [Review] |
| Physics | IX-A | 25 | Ms. Lakshmi | ✅ Done | 40 | 4 | 0 | [Review] |
| Chemistry | IX-A | 25 | Mr. Ravi | 🔄 In Progress | 28 | 1 | 13 | [Continue] |
| Biology | IX-A | 25 | Ms. Anjali | ⬜ Not Started | 0 | 0 | 42 | [Enter Marks] |
| English | IX-A | 25 | Ms. Suma | ✅ Done | 42 | 0 | 0 | [Review] |
| Hindi | IX-A | 25 | Mr. Ramesh | ⬜ Not Started | 0 | 0 | 42 | [Enter Marks] |

Click [Enter Marks] → opens `marks-entry-class` drawer (760px) for full grid entry.

---

## 4. Marks Entry Grid (Drawer — 760px)

The primary entry interface: a spreadsheet-like grid for one subject in one class.

```
Marks Entry: Chemistry — Class IX-A — Unit Test 2 (Max: 25)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Roll  Student Name          Marks    Absent   Flag
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
001   Arjun Sharma           22       ☐
002   Priya Venkataraman     19       ☐
003   Rahul Gupta             [   ]   ☐         ← cursor here
004   Anjali Das             18       ☐
005   Deepak Mohan            [   ]   ☐
006   Kavitha Reddy          21       ☐
007   Rohit Kumar            23       ☐
...
040   Suresh M               ——       ☑ Absent  ← absent checked
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Save Draft]    [Submit for Review]    [Clear All]
```

**Keyboard navigation:** Tab moves to next cell, Enter saves and moves down — designed for rapid keyboard-only entry.

**Absent checkbox:** Marking a student as absent sets marks to null (not zero). "Absent" and "0 marks" are distinct states — zero means they appeared and scored nothing.

**Real-time validation per cell:**
- Value > Max Marks → red highlight: "Cannot exceed 25"
- Non-numeric input → red highlight
- Decimal not allowed (integer marks only; configurable)

**Flag column:** Auto-flags anomalous entries:
- 🔴 Score above max
- 🟡 Score = 0 but not marked absent (unusual; may be correct but prompts review)
- 🟡 Score in top 5% but student was in bottom 20% last exam

---

## 5. Entry Modes

Toggle between two entry modes:

### Mode A — Grid (default)
One subject, one class. Full spreadsheet grid as shown above. Best for teachers entering marks for their subject across an entire class.

### Mode B — Student-wise
One student, all subjects. Used by class teacher to verify completeness for their class or enter marks for absent teachers.

```
Student: Arjun Sharma (IX-A, Roll 001)

Subject        Max  Marks  Absent  Teacher        Status
Mathematics    25   22     —       Mr. Arjun      ✅ Entered
Physics        25   19     —       Ms. Lakshmi    ✅ Entered
Chemistry      25   [  ]   —       Mr. Ravi       ⬜ Pending
Biology        25   [  ]   —       Ms. Anjali     ⬜ Pending
English        25   21     —       Ms. Suma       ✅ Entered
Hindi          25   [  ]   —       Mr. Ramesh     ⬜ Pending
Total          150  62     —                      Incomplete
```

---

## 6. Save Draft vs Submit for Review

**[Save Draft]** → marks are saved but not yet submitted. Teacher can continue editing. Other teachers cannot see the draft marks.

**[Submit for Review]** → marks are locked from teacher editing and move to HOD/Exam Cell Head for review (B-17). A submitted batch cannot be edited by the teacher without HOD returning it.

Submission rules:
- At least 80% of students must have marks (or absent checkbox) before submission is allowed
- Remaining students can be "Pending" — if a student was writing a make-up test, their marks can be entered later

---

## 7. Anomaly Detection

After submission, the system runs anomaly checks and flags for reviewer (B-17):

| Anomaly Type | Threshold | Example |
|---|---|---|
| Class avg dramatically higher than last exam | +15% | Class avg jumped from 52% to 79% |
| Class avg dramatically lower | -15% | Class avg dropped from 74% to 48% |
| All students scored same marks | — | 35 of 42 students scored exactly 18/25 |
| Teacher changed 3+ marks within 1 hour of submission | — | Rapid sequential edits |
| SD (standard deviation) extremely low | SD < 1.5 for 20+ students | Suspicious uniformity |

Anomalies don't block submission — they flag the batch for closer HOD review.

---

## 8. Marks Correction Workflow

If a teacher needs to correct marks after submission:
1. Teacher clicks [Request Correction] → form with reason
2. HOD reviews and either [Return for Correction] or [Reject Request]
3. If returned: teacher can edit the specific student's marks and resubmit
4. All corrections are logged in Audit Log (A-34) with before/after values

---

## 9. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/exams/{exam_id}/marks/` | Entry progress overview |
| 2 | `GET` | `/api/v1/school/{id}/exams/{exam_id}/marks/{subject_id}/{class_id}/` | Class marks entry grid |
| 3 | `PATCH` | `/api/v1/school/{id}/exams/{exam_id}/marks/{subject_id}/{class_id}/` | Save marks (draft or submit) |
| 4 | `POST` | `/api/v1/school/{id}/exams/{exam_id}/marks/{subject_id}/{class_id}/submit/` | Submit for review |
| 5 | `GET` | `/api/v1/school/{id}/exams/{exam_id}/marks/student/{student_id}/` | Student-wise all-subject view |
| 6 | `GET` | `/api/v1/school/{id}/exams/{exam_id}/marks/anomalies/` | Anomaly flags |
| 7 | `POST` | `/api/v1/school/{id}/exams/{exam_id}/marks/{subject_id}/{class_id}/request-correction/` | Correction request |
| 8 | `GET` | `/api/v1/school/{id}/exams/{exam_id}/marks/summary/` | Completion summary for Exam Cell |

---

## 10. Business Rules

- Teachers can only enter marks for subjects and classes assigned to them in B-30 (Subject Allocation); any attempt to enter marks for an unassigned subject is blocked
- Class Teacher (S3) can enter marks for all subjects of their own class — used when a subject teacher is unavailable
- Marks entry window closes N days after the exam's last date (configurable per exam, default 10 days)
- Submitted (not draft) marks cannot be edited by the teacher; corrections require HOD return
- "Absent" is not zero — system treats absent students as non-participants in average computation; they are listed separately in result
- Marks once approved by HOD cannot be edited at all; any correction after approval requires Principal authorisation via A-23 (Approval Hub)

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division B*
