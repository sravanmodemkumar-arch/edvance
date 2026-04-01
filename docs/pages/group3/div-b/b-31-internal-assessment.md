# B-31 — Internal Assessment Manager

> **URL:** `/school/academic/ia/`
> **File:** `b-31-internal-assessment.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Exam Cell Head (S4) — full · HOD (S4) — own dept input · Subject Teacher (S3) — enter own · Class Teacher (S3) — view own class · Principal (S6) — full

---

## 1. Purpose

Manages the internal assessment (IA) marks that form a mandatory component of CBSE and many state board final scores. For CBSE Classes IX–X, 20 marks out of 100 come from Internal Assessment. For Classes XI–XII, 30 marks come from IA. These are not exam marks — they are computed from a student's performance across the entire year: periodic test performance, notebook/portfolio maintenance, and subject enrichment activities. Without accurate IA management, a school cannot generate correct CBSE-format report cards or submit marks to the board.

**CBSE IA Breakdown (IX–X, per subject):**
- Periodic Tests (best of 3): 10 marks
- Notebook/Portfolio: 5 marks
- Subject Enrichment Activity: 5 marks
- **Total IA: 20 marks**

**CBSE IA Breakdown (XI–XII, per subject):**
- Periodic Tests (best of 2): 10 marks
- Practical/Project/Research Activity: 20 marks
- **Total IA: 30 marks**

*(Exact structure varies by subject — Computer Science has different proportions; Physical Education has its own 40-mark IA. All configurable.)*

---

## 2. Page Layout

### 2.1 Header
```
Internal Assessment Manager                       [Export IA Register]  [Lock IA Marks]
Academic Year: 2025–26  ·  Class: [All ▼]  Subject: [All ▼]
CBSE Classes IX–X: 20 marks  ·  Classes XI–XII: 30 marks
Lock Status: ⚠️ Not yet locked (marks can still be edited)
```

---

## 3. IA Overview Table

| Class | Section | Subject | Teacher | PT1 | PT2 | PT3 | Best of 3 | Notebook | Enrichment | IA Total | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| IX | A | Mathematics | Mr. Arjun | 10 | 10 | 10 | 10/10 | 4.6 | 4.8 | 19.4/20 | 🔄 In progress |
| IX | A | Physics | Ms. Lakshmi | 10 | 10 | — | — | — | — | — | ⬜ PT3 pending |
| IX | A | Chemistry | Mr. Ravi | 9 | 10 | 10 | 10/10 | 4.2 | 4.6 | 18.8/20 | 🔄 In progress |
| IX | A | English | Ms. Suma | 8 | 9 | 10 | 9/10 | 4.8 | 4.4 | 18.2/20 | 🔄 In progress |
| XII | A | Physics | Ms. Lakshmi | 18 | 20 | — | 19/20 | — | 28/30 | — | 🔄 Practical pending |

Click any row → opens the IA detail drawer for that subject-class combination.

---

## 4. Periodic Test Marks Entry

IA marks are linked to Periodic Test results from B-16. When a PT exam is run and marks approved in B-17, the system auto-populates PT scores in the IA module. Manual entry is also possible for schools not using B-16 for PT marks.

### IA Drawer — Class IX-A Mathematics

```
Internal Assessment: Mathematics — Class IX-A
Teacher: Mr. Arjun  ·  Max IA: 20 marks

Student List:
Roll  Name             PT1(10) PT2(10) PT3(10) Best2  Notebook(5)  Enrichmt(5)  IA Total
001   Arjun Sharma     8       9       10      19→9.5  5.0          4.8          19.3
002   Priya Venkat     7       8       9       17→8.5  4.6          4.6          17.7
003   Rahul Gupta      5       6       7       13→6.5  3.8          4.0          14.3
...

Notes on computation:
• Best of 3 PTs computed to 10 marks: (best 2 PT scores / 20) × 10
• Notebook: HOD-rated 1–5 scale; entered directly
• Enrichment: HOD-rated 1–5 scale; entered directly
• IA Total = (Best of 3) + Notebook + Enrichment
```

**Note:** CBSE takes best of 3 for IX–X; for XI–XII it's best of 2. The system handles both structures.

---

## 5. Notebook / Portfolio Rating Entry

Notebook and Subject Enrichment marks are teacher-assigned qualitative ratings (1–5 scale, which is scaled to the mark range):

[Enter Notebook Marks] → opens a grid:

```
Notebook Assessment: Chemistry — Class IX-A
Assessment Period: Annual 2025–26  (Enter once per year before IA lock)

Roll  Name                  Notebook  Completeness  Neatness  Composite(5)
001   Arjun Sharma          ✅ Present  ●●●●○ 4/5    ●●●●● 5/5   4.5
002   Priya Venkat          ✅ Present  ●●●●● 5/5    ●●●●● 5/5   5.0
003   Rahul Gupta           ✅ Present  ●●●○○ 3/5    ●●●○○ 3/5   3.0
012   Anjali Das            ❌ Missing  —             —            0.0
```

Subject Enrichment activity (project/assignment/lab report/debate/seminar participation):
- Teacher rates on what the student did for the activity
- Can attach a brief note per student

---

## 6. Practical / Project Marks (XI–XII)

For Classes XI–XII, the practical/project component (20 marks) is entered separately:

[Enter Practical Marks] → grid for practical assessment:

```
Practical Assessment: Physics — Class XII-A
Practical Type: Lab Practical + Viva (CBSE format)
External Examiner: Dr. Kishore (CBSE-appointed)

Roll  Name          File/Record(5)  Practical(10)  Viva(5)  Total(30)*  (* project excluded here)
001   Arjun Sharma  4               8              4        28
002   Priya Venkat  5               9              5        30
```

For subjects without practicals (History, Economics), this section shows "Project Report" submission tracking instead:

```
Project Assessment: History — Class XI-A
Topic assigned: Impact of Colonialism on Indian Economy
Submission deadline: 15 Feb 2026

Roll  Name          Submitted  Score(20)  Presentation(10)  Total(30)
001   Arjun Sharma  ✅ 12 Feb  17         8                 25
002   Priya Venkat  ✅ 10 Feb  19         9                 28
003   Rahul Gupta   ❌ Not sub  0         0                 0
```

---

## 7. IA Final Computation

After all components are entered, the system computes final IA marks:

| Class | Section | Subject | IA Max | Avg IA | Below 50% | Complete | Action |
|---|---|---|---|---|---|---|---|
| IX-A | A | Mathematics | 20 | 18.4 | 2 students | ✅ Yes | [View] |
| IX-A | A | Physics | 20 | 17.1 | 1 student | ✅ Yes | [View] |
| XII-A | A | Chemistry | 30 | 26.4 | 0 | ✅ Yes | [View] |
| XII-A | A | History | 30 | — | — | ❌ No (project pending) | [Enter] |

---

## 8. IA Lock

[Lock IA Marks] — Principal or Exam Cell Head action:

Once locked:
- No further edits to IA marks for the academic year
- IA marks flow into B-18 (Result Computation) and become part of the final marks
- CBSE requires IA marks to be locked before board exam result submission

**Warning before lock:** "Locking IA marks is irreversible. 4 incomplete entries exist. Do you want to proceed?"

---

## 9. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/ia/?year={year}&class={c}&subject={s}` | IA overview table |
| 2 | `GET` | `/api/v1/school/{id}/ia/{subject_id}/{class_id}/` | IA detail for a subject-class |
| 3 | `PATCH` | `/api/v1/school/{id}/ia/{subject_id}/{class_id}/notebook/` | Enter notebook marks |
| 4 | `PATCH` | `/api/v1/school/{id}/ia/{subject_id}/{class_id}/enrichment/` | Enter enrichment marks |
| 5 | `PATCH` | `/api/v1/school/{id}/ia/{subject_id}/{class_id}/practical/` | Enter practical/project marks |
| 6 | `GET` | `/api/v1/school/{id}/ia/{subject_id}/{class_id}/compute/` | Compute IA totals |
| 7 | `POST` | `/api/v1/school/{id}/ia/lock/` | Lock all IA marks (Principal/Exam Cell) |
| 8 | `GET` | `/api/v1/school/{id}/ia/export/?year={year}` | IA register export PDF |

---

## 10. Business Rules

- PT marks are pulled automatically from B-16/B-17 when a Periodic Test exam is marked complete; manual entry is the fallback if not using B-16 for PTs
- The "best of N" computation is automatic; the system takes the highest N scores
- IA marks are per academic year, not per term — one final IA score per subject per student
- IA lock is irreversible at the school level; Platform Admin can unlock in exceptional cases (CBSE data correction scenarios)
- Students who were absent for all PTs get 0 for the PT component — this is not a system error; must be reviewed by the Exam Cell Head before lock
- CBSE submission format (IA data for board marks submission) is generated from this module — CBSE portal requires IA in a specific XML/CSV format which EduForge generates

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division B*
