# N-02 — Child's Attendance (Parent View)

> **URL:** `/parent/attendance/`
> **File:** `n-02-attendance-view.md`
> **Template:** `parent_portal.html`
> **Priority:** P1
> **Roles:** Parent/Guardian (S1-P)

---

## 1. Purpose

Parents see their child's attendance in real-time. The key use cases are:
- "Was my child marked present today?" (verification)
- "What is my child's attendance percentage?" (CBSE 75% eligibility tracking)
- "On which days was my child absent?" (accountability / reconciliation)
- "My child's attendance is at 78% — when should I worry?" (threshold alerting)

The parent view is derived from E-01 (school attendance) — parents cannot modify attendance; only the Class Teacher can.

---

## 2. Monthly Calendar View

```
ATTENDANCE — Rahul Rao (Class X-A)
Academic Year: 2025–26 | Working days: 220

MARCH 2026:
  Mon    Tue    Wed    Thu    Fri    Sat
  2 ✅   3 ✅   4 ✅   5 ✅   6 ✅   7 —
  9 ✅   10 ✅  11 ✅  12 🔴  13 ✅  14 —
  16 ✅  17 ✅  18 ✅  19 ✅  20 ✅  21 —
  23 ✅  24 ✅  25 ✅  26 ✅  27 ✅  28 —
  30 ✅  31 ✅

Legend: ✅ Present  🔴 Absent  🟡 Late  🔵 Half-day  — Holiday/Sunday

MARCH SUMMARY:
  Working days: 23  |  Present: 22  |  Absent: 1 (Thu 12 Mar)
  Monthly attendance: 95.7%

FULL YEAR SUMMARY (as of today):
  Working days completed: 220
  Days present: 197
  Days absent: 23 (7 with leave application, 16 without)
  Annual attendance: 89.5%

CBSE ELIGIBILITY STATUS:
  Current: 89.5% ✅ (Well above 75% minimum)
  Board exam eligibility: ✅ Eligible
  To drop below 75%, would need to miss: 32 more days (remaining: 0 — year complete)

ABSENCE DETAIL:
  Date    Absence Type   Leave Application   Parent Informed
  12 Mar  Absent         None (unnotified)  Class Teacher called — ✅
  4 Feb   Absent         School leave app   ✅ approved by CT
  [Full year list — 23 rows]
```

---

## 3. Attendance Alerts

```
ATTENDANCE ALERTS — CONFIGURED FOR Rahul Rao

Current alert settings:
  ✅ Any absence — notify parent immediately (day of)
  ✅ Monthly attendance <85% — alert at month-end
  ✅ Cumulative attendance <80% — alert (early warning)
  ✅ Cumulative attendance <75% — critical alert (CBSE board risk)

History of alerts this year:
  — No alerts triggered for Rahul (89.5% annual ✅)

[If attendance were below 80%:]
⚠ ATTENDANCE ALERT — [Student Name] — Class X-A
  "Your child's attendance has dropped to 78.4% (below the 80% warning threshold).
   CBSE minimum for board exam eligibility is 75%. If attendance continues at the
   current rate, your child may become ineligible. Please contact the school.
   [Contact Class Teacher]  [View attendance details]"
```

---

## 4. Leave Application (Parent-Initiated)

```
[See N-08 for full leave application flow]

QUICK LEAVE APPLICATION (from attendance view):
  If a parent knows the child will be absent tomorrow, they can apply here.

  Leave request:
    Child: Rahul Rao (Class X-A)
    From: 2 April 2026
    To: 3 April 2026 (2 days)
    Reason: Family function (marriage ceremony)
    Note to Class Teacher: "Will ensure Rahul completes any missed classwork on return."

  [Submit leave request → goes to Class Teacher for approval (N-08)]
```

---

## 5. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/parent/{parent_id}/child/{student_id}/attendance/monthly/?month=2026-03` | Monthly attendance |
| 2 | `GET` | `/api/v1/parent/{parent_id}/child/{student_id}/attendance/annual/` | Full year summary |
| 3 | `GET` | `/api/v1/parent/{parent_id}/child/{student_id}/attendance/eligibility/` | CBSE 75% eligibility status |
| 4 | `GET` | `/api/v1/parent/{parent_id}/child/{student_id}/attendance/absences/` | All absence dates with reasons |

---

## 6. Business Rules

- Attendance data shown to parents is read-only; parents cannot modify or challenge attendance through this view (they must contact the school directly for corrections; the Class Teacher makes corrections in E-01)
- Absence notification to parents: EduForge sends a WhatsApp/SMS notification for every absence by 9:30 AM on the day of absence; the parent attendance view is consistent with this notification
- For CBSE board classes (X and XII), the attendance percentage is shown with explicit "Board exam eligibility" status; this is a parent-anxiety trigger and an appropriate one — it motivates action before it's too late
- Leave applications submitted by parents appear in the Class Teacher's E-01/N-08 queue for approval; an approved leave request changes the absence marker from "Absent (unnotified)" to "Absent (approved leave)"; this distinction matters for welfare flagging — unnotified absences trigger welfare concern, approved leave does not

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division N*
