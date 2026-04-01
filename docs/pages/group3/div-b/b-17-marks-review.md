# B-17 — Marks Review & Approval

> **URL:** `/school/academic/marks/<exam_id>/review/`
> **File:** `b-17-marks-review.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** HOD (S4) — review/approve own dept subjects · Exam Cell Head (S4) — full all · Principal (S6) — full

---

## 1. Purpose

The HOD and Exam Cell Head review submitted marks batches for anomalies, accuracy, and completeness before approving them for result computation. This is the quality gate between raw marks entry and official results. In Indian schools, the HOD's signature on the marks tabulation register is a legal requirement — this digital approval is the equivalent. Once approved here, marks flow into B-18 (Result Computation) and cannot be changed without Principal authorisation. The review step catches data entry errors (transpose errors, marks-above-max that slipped through, suspicious uniformity) before they become published results.

---

## 2. Page Layout

### 2.1 Header
```
Marks Review & Approval — Unit Test 2, 2025–26   [Export Tabulation Sheet]
Exam: Unit Test 2  ·  Max Marks: 25 per subject
Submitted: 104 batches  ·  Approved: 72  ·  Pending Review: 24  ·  Returned: 8
```

---

## 3. Review Queue

| Subject | Class | Teacher | Students | Avg Score | Anomalies | Submitted | Status | Action |
|---|---|---|---|---|---|---|---|---|
| Chemistry | IX-A | Mr. Ravi | 42/42 | 62.4% | ✅ None | 2h ago | ⚠️ Pending | [Review] |
| Biology | XI-B | Ms. Anjali | 40/40 | 48.2% | 🟡 Low avg | 3h ago | ⚠️ Pending | [Review] |
| Physics | XII-A | Ms. Lakshmi | 38/38 | 81.4% | ✅ None | 4h ago | ⚠️ Pending | [Review] |
| Mathematics | X-B | Mr. Arjun | 40/38 | 72.8% | 🔴 2 students > max | 5h ago | ⚠️ Pending | [Review] |
| Hindi | VII-B | Mr. Ramesh | 44/44 | 55.6% | ✅ None | 6h ago | ✅ Approved | [View] |

Anomaly icons:
- 🔴 Hard anomaly (marks above max, impossible values) — must resolve before approving
- 🟡 Soft anomaly (low avg, unusual distribution) — can approve with note
- ✅ Clean — no flags

---

## 4. Review Drawer (`result-review`, 640px)

Opened by [Review] on any pending batch:

### Section A — Batch Summary

```
Marks Review: Chemistry — Class IX-A — Unit Test 2
Teacher: Mr. Ravi Kumar  ·  Submitted: 26 Mar 14:22  ·  Max Marks: 25

Students: 42 (40 appeared, 2 absent)
  Present & Marks Entered: 40
  Absent (null marks):     2

Score Distribution:
  0–5:    1 student (2.5%)
  6–10:   2 students (5%)
  11–15:  8 students (20%)
  16–20:  18 students (45%)
  21–25:  11 students (27.5%)
  Above max: 0

Statistics:
  Average:  15.6 / 25  (62.4%)
  Median:   17
  SD:       4.2
  Highest:  24
  Lowest:   4

vs Last Exam (PT2):  Average was 14.8 — current is slightly higher ✅
```

### Section B — Student-wise Marks (Scrollable Table)

| Roll | Student Name | Marks | Absent | Flags |
|---|---|---|---|---|
| 001 | Arjun Sharma | 22 | — | — |
| 002 | Priya Venkat | 19 | — | — |
| 003 | Rahul Gupta | 4 | — | 🟡 Very low — was 18 last exam |
| 004 | Anjali Das | — | ✅ Absent | — |
| ... | ... | ... | ... | ... |
| 042 | Vijay K | 24 | — | — |

Click any flagged row → shows student's marks history for context.

### Section C — HOD Action

```
Anomalies to resolve:
  ⚠️ Rahul Gupta: 4/25 — very low score. Previous test: 18/25. Verify if correct.

Reviewer Notes:
[ Teacher confirmed Rahul was unwell — score is correct                        ]

Approval Action:
  [✅ Approve]   [🔄 Return to Teacher (with note)]   [🔴 Escalate to Principal]
```

**[Approve]** → batch status = Approved; marks locked; feeds into B-18.
**[Return to Teacher]** → batch goes back to Mr. Ravi with HOD's note; teacher corrects and resubmits.
**[Escalate to Principal]** → rare; for serious data integrity concerns.

---

## 5. HOD Scope

HOD only sees batches for their own department's subjects. A Science HOD reviews Physics, Chemistry, Biology marks. An English HOD reviews English marks.

Multi-department subjects (e.g., General Science in classes VI–VIII taught by multiple department teachers) are reviewed by the Academic Coordinator.

---

## 6. Exam Cell Head View (Full Access)

Exam Cell Head sees all batches across all subjects and departments. Their responsibility:
- Ensure all batches are reviewed and approved before result computation deadline
- Chase overdue HOD reviews
- Spot cross-department anomalies (e.g., a student with 0 in every subject — might indicate a non-appearance issue vs data entry error)

```
Approval Progress:
  Science dept HOD:    24/26 approved, 2 pending (Chemistry XI-A, Biology XII-B)
  Maths dept HOD:      18/18 approved ✅
  Languages dept HOD:  22/22 approved ✅
  Commerce dept HOD:   12/14 approved, 2 returned (awaiting teacher resubmission)
```

---

## 7. Marks Tabulation Export

[Export Tabulation Sheet] → generates the official marks tabulation register:
- Format: One sheet per class, rows = students, columns = subjects, final column = total
- All column totals computed
- "HOD Reviewed by:" and "Exam Cell Head:" signature rows at the bottom
- Used for Principal presentation, CBSE inspection, and office record

---

## 8. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/exams/{exam_id}/marks/review/` | Full review queue |
| 2 | `GET` | `/api/v1/school/{id}/exams/{exam_id}/marks/review/{batch_id}/` | Batch detail with student marks |
| 3 | `POST` | `/api/v1/school/{id}/exams/{exam_id}/marks/review/{batch_id}/approve/` | Approve batch |
| 4 | `POST` | `/api/v1/school/{id}/exams/{exam_id}/marks/review/{batch_id}/return/` | Return to teacher |
| 5 | `GET` | `/api/v1/school/{id}/exams/{exam_id}/marks/review/progress/` | Approval progress by dept |
| 6 | `GET` | `/api/v1/school/{id}/exams/{exam_id}/marks/review/export/` | Tabulation sheet PDF |

---

## 9. Business Rules

- HOD can only approve batches for their own department; Exam Cell Head can approve any
- Batches with hard anomalies (marks above maximum) cannot be approved without first correcting the data — the [Approve] button is disabled until hard anomalies are resolved
- Soft anomalies can be approved with a reviewer note (note becomes part of audit trail)
- Once approved, marks are immutable; subsequent corrections require Principal authorisation via A-23
- If the HOD hasn't reviewed within 3 days of submission, Exam Cell Head gets an auto-alert; after 5 days, Principal is notified
- Result computation (B-18) can only begin when all batches for the exam are in Approved state

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division B*
